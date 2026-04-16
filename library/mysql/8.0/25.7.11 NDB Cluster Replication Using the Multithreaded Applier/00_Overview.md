---
source: MySQL 8.0 Reference
title: 00_Overview
---

• [Requirements](#page-65-0)

- [MTA Configuration: Source](#page-65-1)
- [MTA Configuration: Replica](#page-66-0)
- [Transaction Dependency and Writeset Handling](#page-66-1)
- [Writeset Tracking Memory Usage](#page-67-0)
- [Known Limitations](#page-67-1)

Beginning with NDB 8.0.33, NDB replication supports the use of the generic MySQL Server Multithreaded Applier mechanism (MTA), which allows independent binary log transactions to be applied in parallel on a replica, increasing peak replication throughput.

### <span id="page-65-0"></span>**Requirements**

The MySQL Server MTA implementation delegates the processing of separate binary log transactions to a pool of worker threads (whose size is configurable), and coordinates the worker threads to ensure that transaction dependencies encoded in the binary log are respected, and that commit ordering is maintained if required (see Section 19.2.3, "Replication Threads"). To use this functionality with NDB Cluster, it is necessary that the following three conditions be met:

1. Binary log transaction dependencies are determined at the source.

For this to be true, the binlog\_transaction\_dependency\_tracking server system variable must be set to WRITESET on the source. This is supported by NDB 8.0.33 and later. (The default is COMMIT\_ORDER.)

Writeset maintenance work in NDB is performed by the MySQL binary log injector thread as part of preparing and committing each epoch transaction to the binary log. This requires extra resources, and may reduce peak throughput.

2. Transaction dependencies are encoded into the binary log.

NDB 8.0.33 and later supports the --ndb-log-transaction-dependency startup option for mysqld; set this option to ON to enable writing of NDB transaction dependencies into the binary log.

3. The replica is configured to use multiple worker threads.

NDB 8.0.33 and later supports setting replica\_parallel\_workers to nonzero values to control the number of worker threads on the replica. The default is 4.

### <span id="page-65-1"></span>**MTA Configuration: Source**

Source mysqld configuration for the NDB MTA must include the following explicit settings:

- binlog\_transaction\_dependency\_tracking must be set to WRITESET.
- The replication source mysqld must be started with --ndb-log-transaction-dependency=ON.

If set, replica\_parallel\_type must be LOGICAL\_CLOCK (the default value).

![](_page_65_Picture_21.jpeg)

#### **Note**

NDB does not support replica\_parallel\_type=DATABASE.

In addition, it is recommended that you set the amount of memory used to track binary log transaction writesets on the source (binlog\_transaction\_dependency\_history\_size) to E \* P, where E is the average epoch size (as the number of operations per epoch) and P is the maximum expected parallelism. See [Writeset Tracking Memory Usage](#page-67-0), for more information.

## <span id="page-66-0"></span>**MTA Configuration: Replica**

Replica mysqld configuration for the NDB MTA requires that replica\_parallel\_workers is greater than 1. The recommended starting value when first enabling MTA is 4, which is the default.

In addition, replica\_preserve\_commit\_order must be ON. This is also the default value.

## <span id="page-66-1"></span>**Transaction Dependency and Writeset Handling**

Transaction dependencies are detected using analysis of each transaction's writeset, that is, the set of rows (table, key values) written by the transaction. Where two transactions modify the same row they are considered to be dependent, and must be applied in order (in other words, serially) to avoid deadlocks or incorrect results. Where a table has secondary unique keys, these values are also added to the transaction's writeset to detect the case where there are transaction dependencies implied by different transactions affecting the same unique key value, and so requiring ordering. Where dependencies cannot be efficiently determined, mysqld falls back to considering transactions dependent for reasons of safety.

Transaction dependencies are encoded in the binary log by the source mysqld. Dependencies are encoded in an ANONYMOUS\_GTID event using a scheme called 'Logical clock'. (See Section 19.1.4.1, "Replication Mode Concepts".)

The writeset implementation employed by MySQL (and NDB Cluster) uses hash-based conflict detection based on matching 64-bit row hashes of relevant table and index values. This detects reliably when the same key is seen twice, but can also produce false positives if different table and index values hash to the same 64-bit value; this may result in artificial dependencies which can reduce the available parallelism.

Transaction dependencies are forced by any of the following:

- DDL statements
- Binary log rotation or encountering binary log file boundaries
- Writeset history size limitations
- Writes which reference parent foreign keys in the target table

More specifically, transactions which perform inserts, updates, and deletes on foreign key parent tables are serialized relative to all preceding and following transactions, and not just to those transactions affecting tables involved in a constraint relationship. Conversely, transactions performing inserts, updates and deletes on foreign key child tables (referencing) are not especially serialized with regard to one another.

The MySQL MTA implementation attempts to apply independent binary log transactions in parallel. NDB records all changes occurring in all user transactions committing in an epoch (TimeBetweenEpochs, default 100 milliseconds), in one binary log transaction, referred to as an epoch transaction. Therefore, for two consecutive epoch transactions to be independent, and possible to apply in parallel, it is required that no row is modified in both epochs. If any single row is modified in both epochs, then they are dependent, and are applied serially, which can limit the expolitable parallelism available.

Epoch transactions are considered independent based on the set of rows modified on the source cluster in the epoch, but not including the generated mysql.ndb\_apply\_status WRITE\_ROW events that convey epoch metadata. This avoids every epoch transaction being trivially dependent on the preceding epoch, but does require that the binlog is applied at the replica with the commit order preserved. This also implies that an NDB binary log with writeset dependencies is not suitable for use by a replica database using a different MySQL storage engine.

It may be possible or desirable to modify application transaction behavior to avoid patterns of repeated modifications to the same rows, in separate transactions over a short time period, to increase exploitable apply parallelism.

## <span id="page-67-0"></span>**Writeset Tracking Memory Usage**

The amount of memory used to track binary log transaction writesets can be set using the binlog\_transaction\_dependency\_history\_size server system variable, which defaults to 25000 row hashes.

If an average binary log transaction modifies N rows, then to be able to identify independent (parallelizable) transactions up to a parallelism level of P, we need binlog\_transaction\_dependency\_history\_size to be at least N \* P. (The maximum is 1000000.)

The finite size of the history results in a finite maximum dependency length that can be reliably determined, giving a finite parallelism that can be expressed. Any row not found in the history may be dependent on the last transaction purged from the history.

Writeset history does not act like a sliding window over the last N transactions; rather, it is a finite buffer which is allowed to fill up completely, then its contents entirely discarded when it becomes full. This means that the history size follows a sawtooth pattern over time, and therefore the maximum detectable dependency length also follows a sawtooth pattern over time, such that independent transactions may still be marked as dependent if the writeset history buffer has been reset between their being processed.

In this scheme, each transaction in a binary log file is annotated with a sequence\_number (1, 2, 3, ...), and as well as the sequence number of the most recent binary log transaction that it depends on, to which we refer as last\_committed.

Within a given binary log file, the first transaction has sequence\_number 1 and last\_committed 0.

Where a binary log transaction depends on its immediate predecessor, its application is serialized. If the dependency is on an earlier transaction then it may be possible to apply the transaction in parallel with the preceding independent transactions.

The content of ANONYMOUS\_GTID events, including sequence\_number and last\_committed (and thus the transaction dependencies), can be seen using mysqlbinlog.

The ANONYMOUS\_GTID events generated on the source are handled separately from the compressed transaction payload with bulk BEGIN, TABLE\_MAP\*, WRITE\_ROW\*, UPDATE\_ROW\*, DELETE\_ROW\*, and COMMIT events, allowing dependencies to be determined prior to decompression. This means that the replica coordinator thread can delegate transaction payload decompression to a worker thread, providing automatic parallel decompression of independent transactions on the replica.

### <span id="page-67-1"></span>**Known Limitations**

**Secondary unique columns.** Tables with secondary unique columns (that is, unique keys other than the primary key) have all columns sent to the source so that unique-key related conflicts can be detected.

Where the current binary logging mode does not include all columns, but only changed columns (- ndb-log-updated-only=OFF, --ndb-log-update-minimal=ON, --ndb-log-update-aswrite=OFF), this can increase the volume of data sent from data nodes to SQL nodes.

The impact depends on both the rate of modification (update or delete) of rows in such tables and the volume of data in columns which are not actually modified.

**Replicating NDB to InnoDB.** NDB binary log injector transaction dependency tracking intentionally ignores the inter-transaction dependencies created by generated mysql.ndb\_apply\_status metadata events, which are handled separately as part of the commit of the epoch transaction on the replica applier. For replication to InnoDB, there is no special handling; this may result in reduced performance or other issues when using an InnoDB multithreaded applier to consume an NDB MTA binary log.

## <span id="page-68-0"></span>**25.7.12 NDB Cluster Replication Conflict Resolution**

- [Requirements](#page-68-1)
- [Source Column Control](#page-69-2)
- [Conflict Resolution Control](#page-69-0)
- [Conflict Resolution Functions](#page-69-1)
- [Conflict Resolution Exceptions Table](#page-75-0)
- [Conflict Detection Status Variables](#page-77-0)
- [Examples](#page-77-1)

When using a replication setup involving multiple sources (including circular replication), it is possible that different sources may try to update the same row on the replica with different data. Conflict resolution in NDB Cluster Replication provides a means of resolving such conflicts by permitting a userdefined resolution column to be used to determine whether or not an update on a given source should be applied on the replica.

Some types of conflict resolution supported by NDB Cluster (NDB\$OLD(), NDB\$MAX(), and NDB\$MAX\_DELETE\_WIN(); additionally, in NDB 8.0.30 and later, NDB\$MAX\_INS() and NDB \$MAX\_DEL\_WIN\_INS()) implement this user-defined column as a "timestamp" column (although its type cannot be TIMESTAMP, as explained later in this section). These types of conflict resolution are always applied a row-by-row basis rather than a transactional basis. The epoch-based conflict resolution functions NDB\$EPOCH() and NDB\$EPOCH\_TRANS() compare the order in which epochs are replicated (and thus these functions are transactional). Different methods can be used to compare resolution column values on the replica when conflicts occur, as explained later in this section; the method used can be set to act on a single table, database, or server, or on a set of one or more tables using pattern matching. See [Matching with wildcards,](#page-46-0) for information about using pattern matches in the db, table\_name, and server\_id columns of the mysql.ndb\_replication table.

You should also keep in mind that it is the application's responsibility to ensure that the resolution column is correctly populated with relevant values, so that the resolution function can make the appropriate choice when determining whether to apply an update.

### <span id="page-68-1"></span>**Requirements**

Preparations for conflict resolution must be made on both the source and the replica. These tasks are described in the following list:

• On the source writing the binary logs, you must determine which columns are sent (all columns or only those that have been updated). This is done for the MySQL Server as a whole by applying the mysqld startup option --ndb-log-updated-only (described later in this section), or on one or more specific tables by placing the proper entries in the mysql.ndb\_replication table (see [ndb\\_replication Table\)](#page-43-0).

![](_page_68_Picture_15.jpeg)

#### **Note**

If you are replicating tables with very large columns (such as TEXT or BLOB columns), --ndb-log-updated-only can also be useful for reducing the size of the binary logs and avoiding possible replication failures due to exceeding max\_allowed\_packet.

See Section 19.5.1.20, "Replication and max\_allowed\_packet", for more information about this issue.

• On the replica, you must determine which type of conflict resolution to apply ("latest timestamp wins", "same timestamp wins", "primary wins", "primary wins, complete transaction", or none). This is done

using the mysql.ndb\_replication system table, and applies to one or more specific tables (see [ndb\\_replication Table\)](#page-43-0).

- NDB Cluster also supports read conflict detection, that is, detecting conflicts between reads of a given row in one cluster and updates or deletes of the same row in another cluster. This requires exclusive read locks obtained by setting ndb\_log\_exclusive\_reads equal to 1 on the replica. All rows read by a conflicting read are logged in the exceptions table. For more information, see [Read](#page-79-0) [conflict detection and resolution](#page-79-0).
- Prior to NDB 8.0.30, NDB applied WRITE\_ROW events strictly as inserts, requiring that there was not already any such row; that is, an incoming write was always rejected if the row already existed. (This is still the case when using any conflict resolution function other than NDB\$MAX\_INS() or NDB \$MAX\_DEL\_WIN\_INS().)

Beginning with NDB 8.0.30, when using NDB\$MAX\_INS() or NDB\$MAX\_DEL\_WIN\_INS(), NDB can apply WRITE\_ROW events idempotently, mapping such an event to an insert when the incoming row does not already exist, or to an update if it does.

When using the functions NDB\$OLD(), NDB\$MAX(), and NDB\$MAX\_DELETE\_WIN() for timestampbased conflict resolution (as well as NDB\$MAX\_INS() and NDB\$MAX\_DEL\_WIN\_INS(), beginning with NDB 8.0.30), we often refer to the column used for determining updates as a "timestamp" column. However, the data type of this column is never TIMESTAMP; instead, its data type should be INT (INTEGER) or BIGINT. The "timestamp" column should also be UNSIGNED and NOT NULL.

The NDB\$EPOCH() and NDB\$EPOCH\_TRANS() functions discussed later in this section work by comparing the relative order of replication epochs applied on a primary and secondary NDB Cluster, and do not make use of timestamps.

## <span id="page-69-2"></span>**Source Column Control**

 We can see update operations in terms of "before" and "after" images—that is, the states of the table before and after the update is applied. Normally, when updating a table with a primary key, the "before" image is not of great interest; however, when we need to determine on a per-update basis whether or not to use the updated values on a replica, we need to make sure that both images are written to the source's binary log. This is done with the --ndb-log-update-as-write option for mysqld, as described later in this section.

![](_page_69_Picture_9.jpeg)

### **Important**

Whether logging of complete rows or of updated columns only is done is decided when the MySQL server is started, and cannot be changed online; you must either restart mysqld, or start a new mysqld instance with different logging options.

### <span id="page-69-0"></span>**Conflict Resolution Control**

 Conflict resolution is usually enabled on the server where conflicts can occur. Like logging method selection, it is enabled by entries in the mysql.ndb\_replication table.

NBT\_UPDATED\_ONLY\_MINIMAL and NBT\_UPDATED\_FULL\_MINIMAL can be used with NDB \$EPOCH(), NDB\$EPOCH2(), and NDB\$EPOCH\_TRANS(), because these do not require "before" values of columns which are not primary keys. Conflict resolution algorithms requiring the old values, such as NDB\$MAX() and NDB\$OLD(), do not work correctly with these binlog\_type values.

## <span id="page-69-1"></span>**Conflict Resolution Functions**

This section provides detailed information about the functions which can be used for conflict detection and resolution with NDB Replication.

• [NDB\\$OLD\(\)](#page-70-0)

- [NDB\\$MAX\(\)](#page-70-1)
- [NDB\\$MAX\\_DELETE\\_WIN\(\)](#page-70-2)
- [NDB\\$MAX\\_INS\(\)](#page-71-0)
- [NDB\\$MAX\\_DEL\\_WIN\\_INS\(\)](#page-71-1)
- [NDB\\$EPOCH\(\)](#page-72-0)
- [NDB\\$EPOCH\\_TRANS\(\)](#page-74-0)
- [NDB\\$EPOCH2\(\)](#page-74-1)
- [NDB\\$EPOCH2\\_TRANS\(\)](#page-74-2)

### <span id="page-70-0"></span>**NDB\$OLD()**

 If the value of column\_name is the same on both the source and the replica, then the update is applied; otherwise, the update is not applied on the replica and an exception is written to the log. This is illustrated by the following pseudocode:

```
if (source_old_column_value == replica_current_column_value)
 apply_update();
else
 log_exception();
```

 This function can be used for "same value wins" conflict resolution. This type of conflict resolution ensures that updates are not applied on the replica from the wrong source.

![](_page_70_Picture_13.jpeg)

### **Important**

The column value from the source's "before" image is used by this function.

#### <span id="page-70-1"></span>**NDB\$MAX()**

 For an update or delete operation, if the "timestamp" column value for a given row coming from the source is higher than that on the replica, it is applied; otherwise it is not applied on the replica. This is illustrated by the following pseudocode:

```
if (source_new_column_value > replica_current_column_value)
 apply_update();
```

 This function can be used for "greatest timestamp wins" conflict resolution. This type of conflict resolution ensures that, in the event of a conflict, the version of the row that was most recently updated is the version that persists.

This function has no effects on conflicts between write operations, other than that a write operation with the same primary key as a previous write is always rejected; it is accepted and applied only if no write operation using the same primary key already exists. Beginning with NDB 8.0.30, you can use [NDB](#page-71-0) [\\$MAX\\_INS\(\)](#page-71-0) to handle conflict resolution between writes.

![](_page_70_Picture_21.jpeg)

#### **Important**

The column value from the sources's "after" image is used by this function.

### <span id="page-70-2"></span>**NDB\$MAX\_DELETE\_WIN()**

 This is a variation on NDB\$MAX(). Due to the fact that no timestamp is available for a delete operation, a delete using NDB\$MAX() is in fact processed as NDB\$OLD, but for some use cases, this is not optimal. For NDB\$MAX\_DELETE\_WIN(), if the "timestamp" column value for a given row adding or updating an existing row coming from the source is higher than that on the replica, it is applied.

However, delete operations are treated as always having the higher value. This is illustrated by the following pseudocode:

```
if ( (source_new_column_value > replica_current_column_value)
 ||
 operation.type == "delete")
 apply_update();
```

 This function can be used for "greatest timestamp, delete wins" conflict resolution. This type of conflict resolution ensures that, in the event of a conflict, the version of the row that was deleted or (otherwise) most recently updated is the version that persists.

![](_page_71_Picture_4.jpeg)

#### **Note**

As with NDB\$MAX(), the column value from the source's "after" image is the value used by this function.

## <span id="page-71-0"></span>**NDB\$MAX\_INS()**

 This function provides support for resolution of conflicting write operations. Such conflicts are handled by "NDB\$MAX\_INS()" as follows:

- 1. If there is no conflicting write, apply this one (this is the same as NDB\$MAX()).
- 2. Otherwise, apply "greatest timestamp wins" conflict resolution, as follows:
  - a. If the timestamp for the incoming write is greater than that of the conflicting write, apply the incoming operation.
  - b. If the timestamp for the incoming write is not greater, reject the incoming write operation.

When handling an insert operation, NDB\$MAX\_INS() compares timestamps from the source and replica as illustrated by the following pseudocode:

```
if (source_new_column_value > replica_current_column_value)
 apply_insert();
else
 log_exception();
```

For an update operation, the updated timestamp column value from the source is compared with the replica's timestamp column value, as shown here:

```
if (source_new_column_value > replica_current_column_value)
 apply_update();
else
 log_exception();
```

This is the same as performed by [NDB\\$MAX\(\)](#page-70-1).

For delete operations, the handling is also the same as that performed by NDB\$MAX() (and thus the same as NDB\$OLD()), and is done like this:

```
if (source_new_column_value == replica_current_column_value)
 apply_delete();
else
 log_exception();
```

NDB\$MAX\_INS() was added in NDB 8.0.30.

#### <span id="page-71-1"></span>**NDB\$MAX\_DEL\_WIN\_INS()**

 This function provides support for resolution of conflicting write operations, along with "delete wins" resolution like that of [NDB\\$MAX\\_DELETE\\_WIN\(\)](#page-70-2). Write conflicts are handled by NDB \$MAX\_DEL\_WIN\_INS() as shown here:

- 1. If there is no conflicting write, apply this one (this is the same as NDB\$MAX\_DELETE\_WIN()).
- 2. Otherwise, apply "greatest timestamp wins" conflict resolution, as follows:
  - a. If the timestamp for the incoming write is greater than that of the conflicting write, apply the incoming operation.
  - b. If the timestamp for the incoming write is not greater, reject the incoming write operation.

Handling of insert operations as performed by NDB\$MAX\_DEL\_WIN\_INS() can be represented in pseudocode as shown here:

```
if (source_new_column_value > replica_current_column_value)
 apply_insert();
else
 log_exception();
```

For update operations, the source's updated timestamp column value is compared with replica's timestamp column value, like this (again using pseudocode):

```
if (source_new_column_value > replica_current_column_value)
 apply_update();
else
 log_exception();
```

Deletes are handled using a "delete always wins" strategy (the same as NDB\$MAX\_DELETE\_WIN()); a DELETE is always applied without any regard to any timestamp values, as illustrated by this pseudocode:

```
if (operation.type == "delete")
 apply_delete();
```

For conflicts between update and delete operations, this function behaves identically to NDB \$MAX\_DELETE\_WIN().

NDB\$MAX\_DEL\_WIN\_INS() was added in NDB 8.0.30.

### <span id="page-72-0"></span>**NDB\$EPOCH()**

 The NDB\$EPOCH() function tracks the order in which replicated epochs are applied on a replica cluster relative to changes originating on the replica. This relative ordering is used to determine whether changes originating on the replica are concurrent with any changes that originate locally, and are therefore potentially in conflict.

Most of what follows in the description of NDB\$EPOCH() also applies to NDB\$EPOCH\_TRANS(). Any exceptions are noted in the text.

NDB\$EPOCH() is asymmetric, operating on one NDB Cluster in a bidirectional replication configuration (sometimes referred to as "active-active" replication). We refer here to cluster on which it operates as the primary, and the other as the secondary. The replica on the primary is responsible for detecting and handling conflicts, while the replica on the secondary is not involved in any conflict detection or handling.

When the replica on the primary detects conflicts, it injects events into its own binary log to compensate for these; this ensures that the secondary NDB Cluster eventually realigns itself with the primary and so keeps the primary and secondary from diverging. This compensation and realignment mechanism requires that the primary NDB Cluster always wins any conflicts with the secondary—that is, that the primary's changes are always used rather than those from the secondary in event of a conflict. This "primary always wins" rule has the following implications:

• Operations that change data, once committed on the primary, are fully persistent and are not undone or rolled back by conflict detection and resolution.

- Data read from the primary is fully consistent. Any changes committed on the Primary (locally or from the replica) are not reverted later.
- Operations that change data on the secondary may later be reverted if the primary determines that they are in conflict.
- Individual rows read on the secondary are self-consistent at all times, each row always reflecting either a state committed by the secondary, or one committed by the primary.
- Sets of rows read on the secondary may not necessarily be consistent at a given single point in time. For NDB\$EPOCH\_TRANS(), this is a transient state; for NDB\$EPOCH(), it can be a persistent state.
- Assuming a period of sufficient length without any conflicts, all data on the secondary NDB Cluster (eventually) becomes consistent with the primary's data.

NDB\$EPOCH() and NDB\$EPOCH\_TRANS() do not require any user schema modifications, or application changes to provide conflict detection. However, careful thought must be given to the schema used, and the access patterns used, to verify that the complete system behaves within specified limits.

Each of the NDB\$EPOCH() and NDB\$EPOCH\_TRANS() functions can take an optional parameter; this is the number of bits to use to represent the lower 32 bits of the epoch, and should be set to no less than the value calculated as shown here:

```
CEIL( LOG2( TimeBetweenGlobalCheckpoints / TimeBetweenEpochs ), 1)
```

For the default values of these configuration parameters (2000 and 100 milliseconds, respectively), this gives a value of 5 bits, so the default value (6) should be sufficient, unless other values are used for TimeBetweenGlobalCheckpoints, TimeBetweenEpochs, or both. A value that is too small can result in false positives, while one that is too large could lead to excessive wasted space in the database.

Both NDB\$EPOCH() and NDB\$EPOCH\_TRANS() insert entries for conflicting rows into the relevant exceptions tables, provided that these tables have been defined according to the same exceptions table schema rules as described elsewhere in this section (see [NDB\\$OLD\(\)](#page-70-0)). You must create any exceptions table before creating the data table with which it is to be used.

As with the other conflict detection functions discussed in this section, NDB\$EPOCH() and NDB \$EPOCH\_TRANS() are activated by including relevant entries in the mysql.ndb\_replication table (see [ndb\\_replication Table\)](#page-43-0). The roles of the primary and secondary NDB Clusters in this scenario are fully determined by mysql.ndb\_replication table entries.

Because the conflict detection algorithms employed by NDB\$EPOCH() and NDB\$EPOCH\_TRANS() are asymmetric, you must use different values for the server\_id entries of the primary and secondary replicas.

A conflict between DELETE operations alone is not sufficient to trigger a conflict using NDB\$EPOCH() or NDB\$EPOCH\_TRANS(), and the relative placement within epochs does not matter.

#### **Limitations on NDB\$EPOCH()**

The following limitations currently apply when using NDB\$EPOCH() to perform conflict detection:

• Conflicts are detected using NDB Cluster epoch boundaries, with granularity proportional to TimeBetweenEpochs (default: 100 milliseconds). The minimum conflict window is the minimum time during which concurrent updates to the same data on both clusters always report a conflict. This is always a nonzero length of time, and is roughly proportional to 2 \* (latency + queueing + TimeBetweenEpochs). This implies that—assuming the default for TimeBetweenEpochs and ignoring any latency between clusters (as well as any queuing delays)—the minimum conflict window size is approximately 200 milliseconds. This minimum window should be considered when looking at expected application "race" patterns.

- Additional storage is required for tables using the NDB\$EPOCH() and NDB\$EPOCH\_TRANS() functions; from 1 to 32 bits extra space per row is required, depending on the value passed to the function.
- Conflicts between delete operations may result in divergence between the primary and secondary. When a row is deleted on both clusters concurrently, the conflict can be detected, but is not recorded, since the row is deleted. This means that further conflicts during the propagation of any subsequent realignment operations are not detected, which can lead to divergence.

Deletes should be externally serialized, or routed to one cluster only. Alternatively, a separate row should be updated transactionally with such deletes and any inserts that follow them, so that conflicts can be tracked across row deletes. This may require changes in applications.

- Only two NDB Clusters in a bidirectional "active-active" configuration are currently supported when using NDB\$EPOCH() or NDB\$EPOCH\_TRANS() for conflict detection.
- Tables having BLOB or TEXT columns are not currently supported with NDB\$EPOCH() or NDB \$EPOCH\_TRANS().

### <span id="page-74-0"></span>**NDB\$EPOCH\_TRANS()**

NDB\$EPOCH\_TRANS() extends the NDB\$EPOCH() function. Conflicts are detected and handled in the same way using the "primary wins all" rule (see [NDB\\$EPOCH\(\)](#page-72-0)) but with the extra condition that any other rows updated in the same transaction in which the conflict occurred are also regarded as being in conflict. In other words, where NDB\$EPOCH() realigns individual conflicting rows on the secondary, NDB\$EPOCH\_TRANS() realigns conflicting transactions.

In addition, any transactions which are detectably dependent on a conflicting transaction are also regarded as being in conflict, these dependencies being determined by the contents of the secondary cluster's binary log. Since the binary log contains only data modification operations (inserts, updates, and deletes), only overlapping data modifications are used to determine dependencies between transactions.

NDB\$EPOCH\_TRANS() is subject to the same conditions and limitations as NDB\$EPOCH(), and in addition requires that all transaction IDs are recorded in the secondary's binary log, using --ndb-logtransaction-id set to ON. This adds a variable amount of overhead (up to 13 bytes per row).

The deprecated log\_bin\_use\_v1\_row\_events system variable, which defaults to OFF, must not be set to ON with NDB\$EPOCH\_TRANS().

See [NDB\\$EPOCH\(\)](#page-72-0).

#### <span id="page-74-1"></span>**NDB\$EPOCH2()**

 The NDB\$EPOCH2() function is similar to NDB\$EPOCH(), except that NDB\$EPOCH2() provides for delete-delete handling with a bidirectional replication topology. In this scenario, primary and secondary roles are assigned to the two sources by setting the ndb\_slave\_conflict\_role system variable to the appropriate value on each source (usually one each of PRIMARY, SECONDARY). When this is done, modifications made by the secondary are reflected by the primary back to the secondary which then conditionally applies them.

### <span id="page-74-2"></span>**NDB\$EPOCH2\_TRANS()**

NDB\$EPOCH2\_TRANS() extends the NDB\$EPOCH2() function. Conflicts are detected and handled in the same way, and assigning primary and secondary roles to the replicating clusters, but with the extra condition that any other rows updated in the same transaction in which the conflict occurred are also regarded as being in conflict. That is, NDB\$EPOCH2() realigns individual conflicting rows on the secondary, while NDB\$EPOCH\_TRANS() realigns conflicting transactions.

Where NDB\$EPOCH() and NDB\$EPOCH\_TRANS() use metadata that is specified per row, per last modified epoch, to determine on the primary whether an incoming replicated row change from the

secondary is concurrent with a locally committed change; concurrent changes are regarded as conflicting, with subsequent exceptions table updates and realignment of the secondary. A problem arises when a row is deleted on the primary so there is no longer any last-modified epoch available to determine whether any replicated operations conflict, which means that conflicting delete operations are not detected. This can result in divergence, an example being a delete on one cluster which is concurrent with a delete and insert on the other; this why delete operations can be routed to only one cluster when using NDB\$EPOCH() and NDB\$EPOCH\_TRANS().

NDB\$EPOCH2() bypasses the issue just described—storing information about deleted rows on the PRIMARY—by ignoring any delete-delete conflict, and by avoiding any potential resultant divergence as well. This is accomplished by reflecting any operation successfully applied on and replicated from the secondary back to the secondary. On its return to the secondary, it can be used to reapply an operation on the secondary which was deleted by an operation originating from the primary.

When using NDB\$EPOCH2(), you should keep in mind that the secondary applies the delete from the primary, removing the new row until it is restored by a reflected operation. In theory, the subsequent insert or update on the secondary conflicts with the delete from the primary, but in this case, we choose to ignore this and allow the secondary to "win", in the interest of preventing divergence between the clusters. In other words, after a delete, the primary does not detect conflicts, and instead adopts the secondary's following changes immediately. Because of this, the secondary's state can revisit multiple previous committed states as it progresses to a final (stable) state, and some of these may be visible.

You should also be aware that reflecting all operations from the secondary back to the primary increases the size of the primary's logbinary log, as well as demands on bandwidth, CPU usage, and disk I/O.

Application of reflected operations on the secondary depends on the state of the target row on the secondary. Whether or not reflected changes are applied on the secondary can be tracked by checking the Ndb\_conflict\_reflected\_op\_prepare\_count and Ndb\_conflict\_reflected\_op\_discard\_count status variables. The number of changes applied is simply the difference between these two values (note that Ndb\_conflict\_reflected\_op\_prepare\_count is always greater than or equal to Ndb\_conflict\_reflected\_op\_discard\_count).

Events are applied if and only if both of the following conditions are true:

- The existence of the row—that is, whether or not it exists—is in accordance with the type of event. For delete and update operations, the row must already exist. For insert operations, the row must not exist.
- The row was last modified by the primary. It is possible that the modification was accomplished through the execution of a reflected operation.

If both of these conditions are not met, the reflected operation is discarded by the secondary.

### <span id="page-75-0"></span>**Conflict Resolution Exceptions Table**

 To use the NDB\$OLD() conflict resolution function, it is also necessary to create an exceptions table corresponding to each NDB table for which this type of conflict resolution is to be employed. This is also true when using NDB\$EPOCH() or NDB\$EPOCH\_TRANS(). The name of this table is that of the table for which conflict resolution is to be applied, with the string \$EX appended. (For example, if the name of the original table is mytable, the name of the corresponding exceptions table name should be mytable\$EX.) The syntax for creating the exceptions table is as shown here:

```
CREATE TABLE original_table$EX (
 [NDB$]server_id INT UNSIGNED,
 [NDB$]source_server_id INT UNSIGNED,
 [NDB$]source_epoch BIGINT UNSIGNED,
 [NDB$]count INT UNSIGNED,
 [NDB$OP_TYPE ENUM('WRITE_ROW','UPDATE_ROW', 'DELETE_ROW',
 'REFRESH_ROW', 'READ_ROW') NOT NULL,]
```

```
 [NDB$CFT_CAUSE ENUM('ROW_DOES_NOT_EXIST', 'ROW_ALREADY_EXISTS',
 'DATA_IN_CONFLICT', 'TRANS_IN_CONFLICT') NOT NULL,]
 [NDB$ORIG_TRANSID BIGINT UNSIGNED NOT NULL,]
 original_table_pk_columns,
 [orig_table_column|orig_table_column$OLD|orig_table_column$NEW,]
 [additional_columns,]
 PRIMARY KEY([NDB$]server_id, [NDB$]source_server_id, [NDB$]source_epoch, [NDB$]count)
) ENGINE=NDB;
```

The first four columns are required. The names of the first four columns and the columns matching the original table's primary key columns are not critical; however, we suggest for reasons of clarity and consistency, that you use the names shown here for the server\_id, source\_server\_id, source\_epoch, and count columns, and that you use the same names as in the original table for the columns matching those in the original table's primary key.

If the exceptions table uses one or more of the optional columns NDB\$OP\_TYPE, NDB\$CFT\_CAUSE, or NDB\$ORIG\_TRANSID discussed later in this section, then each of the required columns must also be named using the prefix NDB\$. If desired, you can use the NDB\$ prefix to name the required columns even if you do not define any optional columns, but in this case, all four of the required columns must be named using the prefix.

Following these columns, the columns making up the original table's primary key should be copied in the order in which they are used to define the primary key of the original table. The data types for the columns duplicating the primary key columns of the original table should be the same as (or larger than) those of the original columns. A subset of the primary key columns may be used.

The exceptions table must use the NDB storage engine. (An example that uses NDB\$OLD() with an exceptions table is shown later in this section.)

Additional columns may optionally be defined following the copied primary key columns, but not before any of them; any such extra columns cannot be NOT NULL. NDB Cluster supports three additional, predefined optional columns NDB\$OP\_TYPE, NDB\$CFT\_CAUSE, and NDB\$ORIG\_TRANSID, which are described in the next few paragraphs.

NDB\$OP\_TYPE: This column can be used to obtain the type of operation causing the conflict. If you use this column, define it as shown here:

```
NDB$OP_TYPE ENUM('WRITE_ROW', 'UPDATE_ROW', 'DELETE_ROW',
 'REFRESH_ROW', 'READ_ROW') NOT NULL
```

The WRITE\_ROW, UPDATE\_ROW, and DELETE\_ROW operation types represent user-initiated operations. REFRESH\_ROW operations are operations generated by conflict resolution in compensating transactions sent back to the originating cluster from the cluster that detected the conflict. READ\_ROW operations are user-initiated read tracking operations defined with exclusive row locks.

NDB\$CFT\_CAUSE: You can define an optional column NDB\$CFT\_CAUSE which provides the cause of the registered conflict. This column, if used, is defined as shown here:

```
NDB$CFT_CAUSE ENUM('ROW_DOES_NOT_EXIST', 'ROW_ALREADY_EXISTS',
 'DATA_IN_CONFLICT', 'TRANS_IN_CONFLICT') NOT NULL
```

ROW\_DOES\_NOT\_EXIST can be reported as the cause for UPDATE\_ROW and WRITE\_ROW operations; ROW\_ALREADY\_EXISTS can be reported for WRITE\_ROW events. DATA\_IN\_CONFLICT is reported when a row-based conflict function detects a conflict; TRANS\_IN\_CONFLICT is reported when a transactional conflict function rejects all of the operations belonging to a complete transaction.

NDB\$ORIG\_TRANSID: The NDB\$ORIG\_TRANSID column, if used, contains the ID of the originating transaction. This column should be defined as follows:

```
NDB$ORIG_TRANSID BIGINT UNSIGNED NOT NULL
```

NDB\$ORIG\_TRANSID is a 64-bit value generated by NDB. This value can be used to correlate multiple exceptions table entries belonging to the same conflicting transaction from the same or different exceptions tables.

Additional reference columns which are not part of the original table's primary key can be named colname\$OLD or colname\$NEW. colname\$OLD references old values in update and delete operations—that is, operations containing DELETE\_ROW events. colname\$NEW can be used to reference new values in insert and update operations—in other words, operations using WRITE\_ROW events, UPDATE\_ROW events, or both types of events. Where a conflicting operation does not supply a value for a given reference column that is not a primary key, the exceptions table row contains either NULL, or a defined default value for that column.

![](_page_77_Picture_3.jpeg)

#### **Important**

The mysql.ndb\_replication table is read when a data table is set up for replication, so the row corresponding to a table to be replicated must be inserted into mysql.ndb\_replication before the table to be replicated is created.

### <span id="page-77-0"></span>**Conflict Detection Status Variables**

 Several status variables can be used to monitor conflict detection. You can see how many rows have been found in conflict by NDB\$EPOCH() since this replica was last restarted from the current value of the Ndb\_conflict\_fn\_epoch system status variable.

Ndb\_conflict\_fn\_epoch\_trans provides the number of rows that have been found directly in conflict by NDB\$EPOCH\_TRANS(). Ndb\_conflict\_fn\_epoch2 and Ndb\_conflict\_fn\_epoch2\_trans show the number of rows found in conflict by NDB\$EPOCH2() and NDB\$EPOCH2\_TRANS(), respectively. The number of rows actually realigned, including those affected due to their membership in or dependency on the same transactions as other conflicting rows, is given by Ndb\_conflict\_trans\_row\_reject\_count.

Another server status variable Ndb\_conflict\_fn\_max provides a count of the number of times that a row was not applied on the current SQL node due to "greatest timestamp wins" conflict resolution since the last time that mysqld was started. Ndb\_conflict\_fn\_max\_del\_win provides a count of the number of times that conflict resolution based on the outcome of NDB\$MAX\_DELETE\_WIN() has been applied.

NDB 8.0.30 and later provides Ndb\_conflict\_fn\_max\_ins for tracking the number of times that "greater timestamp wins" handling has been applied to write operations (using NDB \$MAX\_INS()); a count of the number of times that "same timestamp wins" handling of writes has been applied (as implemented by NDB\$MAX\_DEL\_WIN\_INS()), is provided by the status variable Ndb\_conflict\_fn\_max\_del\_win\_ins.

The number of times that a row was not applied as the result of "same timestamp wins" conflict resolution on a given mysqld since the last time it was restarted is given by the global status variable Ndb\_conflict\_fn\_old. In addition to incrementing Ndb\_conflict\_fn\_old, the primary key of the row that was not used is inserted into an exceptions table, as explained elsewhere in this section.

See also NDB Cluster Status Variables.

### <span id="page-77-1"></span>**Examples**

The following examples assume that you have already a working NDB Cluster replication setup, as described in [Section 25.7.5, "Preparing the NDB Cluster for Replication",](#page-47-0) and [Section 25.7.6, "Starting](#page-49-0) [NDB Cluster Replication \(Single Replication Channel\)".](#page-49-0)

**NDB\$MAX() example.** Suppose you wish to enable "greatest timestamp wins" conflict resolution on table test.t1, using column mycol as the "timestamp". This can be done using the following steps:

1. Make sure that you have started the source mysqld with --ndb-log-update-as-write=OFF.

2. On the source, perform this INSERT statement:

```
INSERT INTO mysql.ndb_replication
 VALUES ('test', 't1', 0, NULL, 'NDB$MAX(mycol)');
```

![](_page_78_Picture_3.jpeg)

#### **Note**

If the ndb\_replication table does not already exist, you must create it. See [ndb\\_replication Table](#page-43-0).

Inserting a 0 into the server\_id column indicates that all SQL nodes accessing this table should use conflict resolution. If you want to use conflict resolution on a specific mysqld only, use the actual server ID.

Inserting NULL into the binlog\_type column has the same effect as inserting 0 (NBT\_DEFAULT); the server default is used.

3. Create the test.t1 table:

```
CREATE TABLE test.t1 (
 columns
 mycol INT UNSIGNED,
 columns
) ENGINE=NDB;
```

Now, when updates are performed on this table, conflict resolution is applied, and the version of the row having the greatest value for mycol is written to the replica.

![](_page_78_Picture_11.jpeg)

#### **Note**

Other binlog\_type options such as NBT\_UPDATED\_ONLY\_USE\_UPDATE (6) should be used to control logging on the source using the ndb\_replication table rather than by using command-line options.

**NDB\$OLD() example.** Suppose an NDB table such as the one defined here is being replicated, and you wish to enable "same timestamp wins" conflict resolution for updates to this table:

```
CREATE TABLE test.t2 (
 a INT UNSIGNED NOT NULL,
 b CHAR(25) NOT NULL,
 columns,
 mycol INT UNSIGNED NOT NULL,
 columns,
 PRIMARY KEY pk (a, b)
) ENGINE=NDB;
```

The following steps are required, in the order shown:

1. First—and prior to creating test.t2—you must insert a row into the [mysql.ndb\\_replication](#page-43-0) table, as shown here:

```
INSERT INTO mysql.ndb_replication
 VALUES ('test', 't2', 0, 0, 'NDB$OLD(mycol)');
```

Possible values for the binlog\_type column are shown earlier in this section; in this case, we use 0 to specify that the server default logging behavior be used. The value 'NDB\$OLD(mycol)' should be inserted into the conflict\_fn column.

2. Create an appropriate exceptions table for test.t2. The table creation statement shown here includes all required columns; any additional columns must be declared following these columns, and before the definition of the table's primary key.

```
CREATE TABLE test.t2$EX (
 server_id INT UNSIGNED,
 source_server_id INT UNSIGNED,
```

```
 source_epoch BIGINT UNSIGNED,
 count INT UNSIGNED,
 a INT UNSIGNED NOT NULL,
 b CHAR(25) NOT NULL,
 [additional_columns,]
 PRIMARY KEY(server_id, source_server_id, source_epoch, count)
) ENGINE=NDB;
```

We can include additional columns for information about the type, cause, and originating transaction ID for a given conflict. We are also not required to supply matching columns for all primary key columns in the original table. This means you can create the exceptions table like this:

```
CREATE TABLE test.t2$EX (
 NDB$server_id INT UNSIGNED,
 NDB$source_server_id INT UNSIGNED,
 NDB$source_epoch BIGINT UNSIGNED,
 NDB$count INT UNSIGNED,
 a INT UNSIGNED NOT NULL,
 NDB$OP_TYPE ENUM('WRITE_ROW','UPDATE_ROW', 'DELETE_ROW',
 'REFRESH_ROW', 'READ_ROW') NOT NULL,
 NDB$CFT_CAUSE ENUM('ROW_DOES_NOT_EXIST', 'ROW_ALREADY_EXISTS',
 'DATA_IN_CONFLICT', 'TRANS_IN_CONFLICT') NOT NULL,
 NDB$ORIG_TRANSID BIGINT UNSIGNED NOT NULL,
 [additional_columns,]
 PRIMARY KEY(NDB$server_id, NDB$source_server_id, NDB$source_epoch, NDB$count)
) ENGINE=NDB;
```

![](_page_79_Picture_4.jpeg)

#### **Note**

The NDB\$ prefix is required for the four required columns since we included at least one of the columns NDB\$OP\_TYPE, NDB\$CFT\_CAUSE, or NDB \$ORIG\_TRANSID in the table definition.

3. Create the table test.t2 as shown previously.

These steps must be followed for every table for which you wish to perform conflict resolution using NDB\$OLD(). For each such table, there must be a corresponding row in mysql.ndb\_replication, and there must be an exceptions table in the same database as the table being replicated.

<span id="page-79-0"></span>**Read conflict detection and resolution.** NDB Cluster also supports tracking of read operations, which makes it possible in circular replication setups to manage conflicts between reads of a given row in one cluster and updates or deletes of the same row in another. This example uses employee and department tables to model a scenario in which an employee is moved from one department to another on the source cluster (which we refer to hereafter as cluster A) while the replica cluster (hereafter B) updates the employee count of the employee's former department in an interleaved transaction.

The data tables have been created using the following SQL statements:

```
# Employee table
CREATE TABLE employee (
 id INT PRIMARY KEY,
 name VARCHAR(2000),
 dept INT NOT NULL
) ENGINE=NDB;
# Department table
CREATE TABLE department (
 id INT PRIMARY KEY,
 name VARCHAR(2000),
 members INT
) ENGINE=NDB;
```

The contents of the two tables include the rows shown in the (partial) output of the following SELECT statements:

```
mysql> SELECT id, name, dept FROM employee;
+---------------+------+
| id | name | dept |
+------+--------+------+
...
| 998 | Mike | 3 |
| 999 | Joe | 3 |
| 1000 | Mary | 3 |
...
+------+--------+------+
mysql> SELECT id, name, members FROM department;
+-----+-------------+---------+
| id | name | members |
+-----+-------------+---------+
...
| 3 | Old project | 24 |
...
+-----+-------------+---------+
```

We assume that we are already using an exceptions table that includes the four required columns (and these are used for this table's primary key), the optional columns for operation type and cause, and the original table's primary key column, created using the SQL statement shown here:

```
CREATE TABLE employee$EX (
 NDB$server_id INT UNSIGNED,
 NDB$source_server_id INT UNSIGNED,
 NDB$source_epoch BIGINT UNSIGNED,
 NDB$count INT UNSIGNED,
 NDB$OP_TYPE ENUM( 'WRITE_ROW','UPDATE_ROW', 'DELETE_ROW',
 'REFRESH_ROW','READ_ROW') NOT NULL,
 NDB$CFT_CAUSE ENUM( 'ROW_DOES_NOT_EXIST',
 'ROW_ALREADY_EXISTS',
 'DATA_IN_CONFLICT',
 'TRANS_IN_CONFLICT') NOT NULL,
 id INT NOT NULL,
 PRIMARY KEY(NDB$server_id, NDB$source_server_id, NDB$source_epoch, NDB$count)
) ENGINE=NDB;
```

Suppose there occur the two simultaneous transactions on the two clusters. On cluster A, we create a new department, then move employee number 999 into that department, using the following SQL statements:

```
BEGIN;
 INSERT INTO department VALUES (4, "New project", 1);
 UPDATE employee SET dept = 4 WHERE id = 999;
COMMIT;
```

At the same time, on cluster B, another transaction reads from employee, as shown here:

```
BEGIN;
 SELECT name FROM employee WHERE id = 999;
 UPDATE department SET members = members - 1 WHERE id = 3;
commit;
```

The conflicting transactions are not normally detected by the conflict resolution mechanism, since the conflict is between a read (SELECT) and an update operation. You can circumvent this issue by executing SET ndb\_log\_exclusive\_reads = 1 on the replica cluster. Acquiring exclusive read locks in this way causes any rows read on the source to be flagged as needing conflict resolution on the replica cluster. If we enable exclusive reads in this way prior to the logging of these transactions, the read on cluster B is tracked and sent to cluster A for resolution; the conflict on the employee row is subsequently detected and the transaction on cluster B is aborted.

The conflict is registered in the exceptions table (on cluster A) as a READ\_ROW operation (see [Conflict](#page-75-0) [Resolution Exceptions Table,](#page-75-0) for a description of operation types), as shown here:

```
mysql> SELECT id, NDB$OP_TYPE, NDB$CFT_CAUSE FROM employee$EX;
+-------+-------------+-------------------+
| id | NDB$OP_TYPE | NDB$CFT_CAUSE |
+-------+-------------+-------------------+
...
| 999 | READ_ROW | TRANS_IN_CONFLICT |
+-------+-------------+-------------------+
```

Any existing rows found in the read operation are flagged. This means that multiple rows resulting from the same conflict may be logged in the exception table, as shown by examining the effects a conflict between an update on cluster A and a read of multiple rows on cluster B from the same table in simultaneous transactions. The transaction executed on cluster A is shown here:

```
BEGIN;
 INSERT INTO department VALUES (4, "New project", 0);
 UPDATE employee SET dept = 4 WHERE dept = 3;
 SELECT COUNT(*) INTO @count FROM employee WHERE dept = 4;
 UPDATE department SET members = @count WHERE id = 4;
COMMIT;
```

Concurrently a transaction containing the statements shown here runs on cluster B:

```
SET ndb_log_exclusive_reads = 1; # Must be set if not already enabled
...
BEGIN;
 SELECT COUNT(*) INTO @count FROM employee WHERE dept = 3 FOR UPDATE;
 UPDATE department SET members = @count WHERE id = 3;
COMMIT;
```

In this case, all three rows matching the WHERE condition in the second transaction's SELECT are read, and are thus flagged in the exceptions table, as shown here:

```
mysql> SELECT id, NDB$OP_TYPE, NDB$CFT_CAUSE FROM employee$EX;
+-------+-------------+-------------------+
| id | NDB$OP_TYPE | NDB$CFT_CAUSE |
+-------+-------------+-------------------+
...
| 998 | READ_ROW | TRANS_IN_CONFLICT |
| 999 | READ_ROW | TRANS_IN_CONFLICT |
| 1000 | READ_ROW | TRANS_IN_CONFLICT |
...
+-------+-------------+-------------------+
```

Read tracking is performed on the basis of existing rows only. A read based on a given condition track conflicts only of any rows that are found and not of any rows that are inserted in an interleaved transaction. This is similar to how exclusive row locking is performed in a single instance of NDB Cluster.

**Insert conflict detection and resolution example (NDB 8.0.30 and later).** The following example illustrates the use of the insert conflict detection functions added in NDB 8.0.30. We assume that we are replicating two tables t1 and t2 in database test, and that we wish to use insert conflict detection with NDB\$MAX\_INS() for t1 and NDB\$MAX\_DEL\_WIN\_INS() for t2. The two data tables are not created until later in the setup process.

Setting up insert conflict resolution is similar to setting up other conflict detection and resolution algorithms as shown in the previous examples. If the mysql.ndb\_replication table used to configure binary logging and conflict resolution, does not already exist, it is first necessary to create it, as shown here:

```
CREATE TABLE mysql.ndb_replication (
 db VARBINARY(63),
 table_name VARBINARY(63),
 server_id INT UNSIGNED,
 binlog_type INT UNSIGNED,
```

```
 conflict_fn VARBINARY(128),
 PRIMARY KEY USING HASH (db, table_name, server_id)
) ENGINE=NDB 
PARTITION BY KEY(db,table_name);
```

The ndb\_replication table acts on a per-table basis; that is, we need to insert a row containing table information, a binlog\_type value, the conflict resolution function to be employed, and the name of the timestamp column (X) for each table to be set up, like this:

```
INSERT INTO mysql.ndb_replication VALUES ("test", "t1", 0, 7, "NDB$MAX_INS(X)");
INSERT INTO mysql.ndb_replication VALUES ("test", "t2", 0, 7, "NDB$MAX_DEL_WIN_INS(X)");
```

Here we have set the binlog\_type as NBT\_FULL\_USE\_UPDATE (7) which means that full rows are always logged. See [ndb\\_replication Table](#page-43-0), for other possible values.

You can also create an exceptions table corresponding to each NDB table for which conflict resolution is to be employed. An exceptions table records all rows rejected by the conflict resolution function for a given table. Exceptions tables for replication conflict detection for tables t1 and t2 can be created using the following two SQL statements:

```
CREATE TABLE `t1$EX` (
 NDB$server_id INT UNSIGNED,
 NDB$master_server_id INT UNSIGNED,
 NDB$master_epoch BIGINT UNSIGNED,
 NDB$count INT UNSIGNED,
 NDB$OP_TYPE ENUM('WRITE_ROW', 'UPDATE_ROW', 'DELETE_ROW', 
 'REFRESH_ROW', 'READ_ROW') NOT NULL,
 NDB$CFT_CAUSE ENUM('ROW_DOES_NOT_EXIST', 'ROW_ALREADY_EXISTS',
 'DATA_IN_CONFLICT', 'TRANS_IN_CONFLICT') NOT NULL,
 a INT NOT NULL,
 PRIMARY KEY(NDB$server_id, NDB$master_server_id, 
 NDB$master_epoch, NDB$count)
) ENGINE=NDB;
CREATE TABLE `t2$EX` (
 NDB$server_id INT UNSIGNED,
 NDB$master_server_id INT UNSIGNED,
 NDB$master_epoch BIGINT UNSIGNED,
 NDB$count INT UNSIGNED,
 NDB$OP_TYPE ENUM('WRITE_ROW', 'UPDATE_ROW', 'DELETE_ROW',
 'REFRESH_ROW', 'READ_ROW') NOT NULL,
 NDB$CFT_CAUSE ENUM( 'ROW_DOES_NOT_EXIST', 'ROW_ALREADY_EXISTS',
 'DATA_IN_CONFLICT', 'TRANS_IN_CONFLICT') NOT NULL,
 a INT NOT NULL,
 PRIMARY KEY(NDB$server_id, NDB$master_server_id, 
 NDB$master_epoch, NDB$count)
) ENGINE=NDB;
```

Finally, after creating the exception tables just shown, you can create the data tables to be replicated and subject to conflict resolution control, using the following two SQL statements:

```
CREATE TABLE t1 (
 a INT PRIMARY KEY, 
 b VARCHAR(32), 
 X INT UNSIGNED
) ENGINE=NDB;
CREATE TABLE t2 (
 a INT PRIMARY KEY, 
 b VARCHAR(32), 
 X INT UNSIGNED
) ENGINE=NDB;
```

For each table, the X column is used as the timestamp column.

Once created on the source, t1 and t2 are replicated and can be assumed to exist on both the source and the replica. In the remainder of this example, we use mysqlS> to indicate a mysql client connected to the source, and mysqlR> to indicate a mysql client running on the replica.

First we insert one row each into the tables on the source, like this:

```
mysqlS> INSERT INTO t1 VALUES (1, 'Initial X=1', 1);
Query OK, 1 row affected (0.01 sec)
mysqlS> INSERT INTO t2 VALUES (1, 'Initial X=1', 1);
Query OK, 1 row affected (0.01 sec)
```

We can be certain that these two rows are replicated without causing any conflicts, since the tables on the replica did not contain any rows prior to issuing the INSERT statements on the source. We can verify this by selecting from the tables on the replica as shown here:

```
mysqlR> TABLE t1 ORDER BY a;
+---+-------------+------+
| a | b | X |
+---+-------------+------+
| 1 | Initial X=1 | 1 |
+---+-------------+------+
1 row in set (0.00 sec)
mysqlR> TABLE t2 ORDER BY a;
+---+-------------+------+
| a | b | X |
+---+-------------+------+
| 1 | Initial X=1 | 1 |
+---+-------------+------+
1 row in set (0.00 sec)
```

Next, we insert new rows into the tables on the replica, like this:

```
mysqlR> INSERT INTO t1 VALUES (2, 'Replica X=2', 2);
Query OK, 1 row affected (0.01 sec)
mysqlR> INSERT INTO t2 VALUES (2, 'Replica X=2', 2);
Query OK, 1 row affected (0.01 sec)
```

Now we insert conflicting rows into the tables on the source having greater timestamp (X) column values, using the statements shown here:

```
mysqlS> INSERT INTO t1 VALUES (2, 'Source X=20', 20);
Query OK, 1 row affected (0.01 sec)
mysqlS> INSERT INTO t2 VALUES (2, 'Source X=20', 20);
Query OK, 1 row affected (0.01 sec)
```

Now we observe the results by selecting (again) from both tables on the replica, as shown here:

```
mysqlR> TABLE t1 ORDER BY a;
+---+-------------+-------+
| a | b | X |
+---+-------------+-------+
| 1 | Initial X=1 | 1 |
+---+-------------+-------+
| 2 | Source X=20 | 20 |
+---+-------------+-------+
2 rows in set (0.00 sec)
mysqlR> TABLE t2 ORDER BY a;
+---+-------------+-------+
| a | b | X |
+---+-------------+-------+
| 1 | Initial X=1 | 1 |
+---+-------------+-------+
| 1 | Source X=20 | 20 |
+---+-------------+-------+
2 rows in set (0.00 sec)
```

The rows inserted on the source, having greater timestamps than those in the conflicting rows on the replica, have replaced those rows. On the replica, we next insert two new rows which do not conflict with any existing rows in t1 or t2, like this:

```
mysqlR> INSERT INTO t1 VALUES (3, 'Slave X=30', 30);
Query OK, 1 row affected (0.01 sec)
mysqlR> INSERT INTO t2 VALUES (3, 'Slave X=30', 30);
Query OK, 1 row affected (0.01 sec)
```

Inserting more rows on the source with the same primary key value (3) brings about conflicts as before, but this time we use a value for the timestamp column less than that in same column in the conflicting rows on the replica.

```
mysqlS> INSERT INTO t1 VALUES (3, 'Source X=3', 3);
Query OK, 1 row affected (0.01 sec)
mysqlS> INSERT INTO t2 VALUES (3, 'Source X=3', 3);
Query OK, 1 row affected (0.01 sec)
```

We can see by querying the tables that both inserts from the source were rejected by the replica, and the rows inserted on the replica previously have not been overwritten, as shown here in the mysql client on the replica:

```
mysqlR> TABLE t1 ORDER BY a;
+---+--------------+-------+
| a | b | X |
+---+--------------+-------+
| 1 | Initial X=1 | 1 |
+---+--------------+-------+
| 2 | Source X=20 | 20 |
+---+--------------+-------+
| 3 | Replica X=30 | 30 |
+---+--------------+-------+
3 rows in set (0.00 sec)
mysqlR> TABLE t2 ORDER BY a;
+---+--------------+-------+
| a | b | X |
+---+--------------+-------+
| 1 | Initial X=1 | 1 |
+---+--------------+-------+
| 2 | Source X=20 | 20 |
+---+--------------+-------+
| 3 | Replica X=30 | 30 |
+---+--------------+-------+
3 rows in set (0.00 sec)
```

You can see information about the rows that were rejected in the exception tables, as shown here:

```
mysqlR> SELECT NDB$server_id, NDB$master_server_id, NDB$count,
 > NDB$OP_TYPE, NDB$CFT_CAUSE, a
 > FROM t1$EX
 > ORDER BY NDB$count\G
*************************** 1. row ***************************
NDB$server_id : 2
NDB$master_server_id: 1
NDB$count : 1
NDB$OP_TYPE : WRITE_ROW
NDB$CFT_CAUSE : DATA_IN_CONFLICT
a : 3
1 row in set (0.00 sec)
mysqlR> SELECT NDB$server_id, NDB$master_server_id, NDB$count,
 > NDB$OP_TYPE, NDB$CFT_CAUSE, a
 > FROM t2$EX
 > ORDER BY NDB$count\G
*************************** 1. row ***************************
NDB$server_id : 2
NDB$master_server_id: 1
NDB$count : 1
NDB$OP_TYPE : WRITE_ROW
NDB$CFT_CAUSE : DATA_IN_CONFLICT
a : 3
1 row in set (0.00 sec)
```

As we saw earlier, no other rows inserted on the source were rejected by the replica, only those rows having a lesser timestamp value than the rows in conflict on the replica.