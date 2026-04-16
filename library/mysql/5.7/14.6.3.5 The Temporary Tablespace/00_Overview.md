---
source: MySQL 5.7 Reference
title: 00_Overview
---

Non-compressed, user-created temporary tables and on-disk internal temporary tables are created in a shared temporary tablespace. The innodb\_temp\_data\_file\_path variable defines the relative path, name, size, and attributes for temporary tablespace data files. If no value is specified for innodb\_temp\_data\_file\_path, the default behavior is to create an auto-extending data file named ibtmp1 in the innodb\_data\_home\_dir directory that is slightly larger than 12MB.

![](_page_61_Picture_14.jpeg)

#### **Note**

In MySQL 5.6, non-compressed temporary tables are created in individual fileper-table tablespaces in the temporary file directory, or in the InnoDB system tablespace in the data directory if innodb\_file\_per\_table is disabled. The introduction of a shared temporary tablespace in MySQL 5.7 removes performance costs associated with creating and removing a file-per-table tablespace for each temporary table. A dedicated temporary tablespace also means that it is no longer necessary to save temporary table metadata to the InnoDB system tables.

Compressed temporary tables, which are temporary tables created using the ROW\_FORMAT=COMPRESSED attribute, are created in file-per-table tablespaces in the temporary file directory.

The temporary tablespace is removed on normal shutdown or on an aborted initialization, and is recreated each time the server is started. The temporary tablespace receives a dynamically generated space ID when it is created. Startup is refused if the temporary tablespace cannot be created. The temporary tablespace is not removed if the server halts unexpectedly. In this case, a database administrator can remove the temporary tablespace manually or restart the server, which removes and recreates the temporary tablespace automatically.

The temporary tablespace cannot reside on a raw device.

The Information Schema FILES table provides metadata about the InnoDB temporary tablespace. Issue a query similar to this one to view temporary tablespace metadata:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.FILES WHERE TABLESPACE_NAME='innodb_temporary'\G
```

The Information Schema INNODB\_TEMP\_TABLE\_INFO table provides metadata about user-created temporary tables that are currently active within an InnoDB instance.

# <span id="page-62-0"></span>**Managing Temporary Tablespace Data File Size**

By default, the temporary tablespace data file is autoextending and increases in size as necessary to accommodate on-disk temporary tables. For example, if an operation creates a temporary table that is 20MB in size, the temporary tablespace data file, which is 12MB in size by default when created, extends in size to accommodate it. When temporary tables are dropped, freed space can be reused for new temporary tables, but the data file remains at the extended size.

An autoextending temporary tablespace data file can become large in environments that use large temporary tables or that use temporary tables extensively. A large data file can also result from long running queries that use temporary tables.

To determine if a temporary tablespace data file is autoextending, check the innodb\_temp\_data\_file\_path setting:

```
mysql> SELECT @@innodb_temp_data_file_path;
+------------------------------+
| @@innodb_temp_data_file_path |
+------------------------------+
| ibtmp1:12M:autoextend |
+------------------------------+
```

To check the size of temporary tablespace data files, query the Information Schema FILES table using a query similar to this:

```
mysql> SELECT FILE_NAME, TABLESPACE_NAME, ENGINE, INITIAL_SIZE, TOTAL_EXTENTS*EXTENT_SIZE
 AS TotalSizeBytes, DATA_FREE, MAXIMUM_SIZE FROM INFORMATION_SCHEMA.FILES
 WHERE TABLESPACE_NAME = 'innodb_temporary'\G
*************************** 1. row ***************************
 FILE_NAME: ./ibtmp1
TABLESPACE_NAME: innodb_temporary
 ENGINE: InnoDB
 INITIAL_SIZE: 12582912
 TotalSizeBytes: 12582912
 DATA_FREE: 6291456
 MAXIMUM_SIZE: NULL
```

The TotalSizeBytes value reports the current size of the temporary tablespace data file. For information about other field values, see Section 24.3.9, "The INFORMATION\_SCHEMA FILES Table".

Alternatively, check the temporary tablespace data file size on your operating system. By default, the temporary tablespace data file is located in the directory defined by the innodb\_temp\_data\_file\_path configuration option. If a value was not specified for this option explicitly, a temporary tablespace data file named ibtmp1 is created in innodb\_data\_home\_dir, which defaults to the MySQL data directory if unspecified.

To reclaim disk space occupied by a temporary tablespace data file, restart the MySQL server. Restarting the server removes and recreates the temporary tablespace data file according to the attributes defined by innodb\_temp\_data\_file\_path.

To prevent the temporary data file from becoming too large, you can configure the innodb\_temp\_data\_file\_path variable to specify a maximum file size. For example:

```
[mysqld]
innodb_temp_data_file_path=ibtmp1:12M:autoextend:max:500M
```

When the data file reaches the maximum size, queries fail with an error indicating that the table is full. Configuring innodb\_temp\_data\_file\_path requires restarting the server.

Alternatively, configure the default\_tmp\_storage\_engine and internal\_tmp\_disk\_storage\_engine variables, which define the storage engine to use for user-created and on-disk internal temporary tables, respectively. Both variables are set to InnoDB by default. The MyISAM storage engine uses an individual file for each temporary table, which is removed when the temporary table is dropped.

# <span id="page-63-0"></span>**14.6.4 InnoDB Data Dictionary**

The InnoDB data dictionary is comprised of internal system tables that contain metadata used to keep track of objects such as tables, indexes, and table columns. The metadata is physically located in the InnoDB system tablespace. For historical reasons, data dictionary metadata overlaps to some degree with information stored in InnoDB table metadata files (.frm files).

# <span id="page-63-1"></span>**14.6.5 Doublewrite Buffer**

The doublewrite buffer is a storage area where InnoDB writes pages flushed from the buffer pool before writing the pages to their proper positions in the InnoDB data files. If there is an operating system, storage subsystem, or unexpected mysqld process exit in the middle of a page write, InnoDB can find a good copy of the page from the doublewrite buffer during crash recovery.

Although data is written twice, the doublewrite buffer does not require twice as much I/O overhead or twice as many I/O operations. Data is written to the doublewrite buffer in a large sequential chunk, with a single fsync() call to the operating system (except in the case that innodb\_flush\_method is set to O\_DIRECT\_NO\_FSYNC).

The doublewrite buffer is enabled by default in most cases. To disable the doublewrite buffer, set innodb\_doublewrite to 0.

If system tablespace files ("ibdata files") are located on Fusion-io devices that support atomic writes, doublewrite buffering is automatically disabled and Fusion-io atomic writes are used for all data files. Because the doublewrite buffer setting is global, doublewrite buffering is also disabled for data files residing on non-Fusion-io hardware. This feature is only supported on Fusion-io hardware and is only enabled for Fusion-io NVMFS on Linux. To take full advantage of this feature, an innodb\_flush\_method setting of O\_DIRECT is recommended.

# <span id="page-63-2"></span>**14.6.6 Redo Log**

The redo log is a disk-based data structure used during crash recovery to correct data written by incomplete transactions. During normal operations, the redo log encodes requests to change table data that result from SQL statements or low-level API calls. Modifications that did not finish updating the data files before an unexpected shutdown are replayed automatically during initialization, and before connections are accepted. For information about the role of the redo log in crash recovery, see Section 14.19.2, "InnoDB Recovery".

By default, the redo log is physically represented on disk by two files named ib\_logfile0 and ib\_logfile1. MySQL writes to the redo log files in a circular fashion. Data in the redo log is encoded in terms of records affected; this data is collectively referred to as redo. The passage of data through the redo log is represented by an ever-increasing LSN value.

Information and procedures related to redo logs are described under the following topics in the section:

- [Changing the Number or Size of InnoDB Redo Log Files](#page-63-3)
- [Related Topics](#page-64-1)

## <span id="page-63-3"></span>**Changing the Number or Size of InnoDB Redo Log Files**

To change the number or the size of your InnoDB redo log files, perform the following steps:

- 1. Stop the MySQL server and make sure that it shuts down without errors.
- 2. Edit my.cnf to change the log file configuration. To change the log file size, configure innodb\_log\_file\_size. To increase the number of log files, configure innodb\_log\_files\_in\_group.
- 3. Start the MySQL server again.

If InnoDB detects that the innodb\_log\_file\_size differs from the redo log file size, it writes a log checkpoint, closes and removes the old log files, creates new log files at the requested size, and opens the new log files.

# <span id="page-64-1"></span>**Related Topics**

- [Redo Log File Configuration](#page-87-0)
- Section 8.5.4, "Optimizing InnoDB Redo Logging"

# <span id="page-64-0"></span>**14.6.7 Undo Logs**

An undo log is a collection of undo log records associated with a single read-write transaction. An undo log record contains information about how to undo the latest change by a transaction to a clustered index record. If another transaction needs to see the original data as part of a consistent read operation, the unmodified data is retrieved from undo log records. Undo logs exist within undo log segments, which are contained within rollback segments. Rollback segments reside in the system tablespace, in undo tablespaces, and in the temporary tablespace.

Undo logs that reside in the temporary tablespace are used for transactions that modify data in userdefined temporary tables. These undo logs are not redo-logged, as they are not required for crash recovery. They are used only for rollback while the server is running. This type of undo log benefits performance by avoiding redo logging I/O.

InnoDB supports a maximum of 128 rollback segments, 32 of which are allocated to the temporary tablespace. This leaves 96 rollback segments that can be assigned to transactions that modify data in regular tables. The innodb\_rollback\_segments variable defines the number of rollback segments used by InnoDB.

The number of transactions that a rollback segment supports depends on the number of undo slots in the rollback segment and the number of undo logs required by each transaction. The number of undo slots in a rollback segment differs according to InnoDB page size.

| InnoDB Page Size | Number of Undo Slots in a Rollback Segment<br>(InnoDB Page Size / 16) |
|------------------|-----------------------------------------------------------------------|
| 4096 (4KB)       | 256                                                                   |
| 8192 (8KB)       | 512                                                                   |
| 16384 (16KB)     | 1024                                                                  |
| 32768 (32KB)     | 2048                                                                  |
| 65536 (64KB)     | 4096                                                                  |

A transaction is assigned up to four undo logs, one for each of the following operation types:

- 1. INSERT operations on user-defined tables
- 2. UPDATE and DELETE operations on user-defined tables
- 3. INSERT operations on user-defined temporary tables
- 4. UPDATE and DELETE operations on user-defined temporary tables

Undo logs are assigned as needed. For example, a transaction that performs INSERT, UPDATE, and DELETE operations on regular and temporary tables requires a full assignment of four undo logs. A transaction that performs only INSERT operations on regular tables requires a single undo log.

A transaction that performs operations on regular tables is assigned undo logs from an assigned system tablespace or undo tablespace rollback segment. A transaction that performs operations on temporary tables is assigned undo logs from an assigned temporary tablespace rollback segment.

An undo log assigned to a transaction remains attached to the transaction for its duration. For example, an undo log assigned to a transaction for an INSERT operation on a regular table is used for all INSERT operations on regular tables performed by that transaction.

Given the factors described above, the following formulas can be used to estimate the number of concurrent read-write transactions that InnoDB is capable of supporting.

![](_page_65_Picture_5.jpeg)

#### **Note**

It is possible to encounter a concurrent transaction limit error before reaching the number of concurrent read-write transactions that InnoDB is capable of supporting. This occurs when the rollback segment assigned to a transaction runs out of undo slots. In such cases, try rerunning the transaction.

When transactions perform operations on temporary tables, the number of concurrent read-write transactions that InnoDB is capable of supporting is constrained by the number of rollback segments allocated to the temporary tablespace, which is 32.

• If each transaction performs either an INSERT **or** an UPDATE or DELETE operation, the number of concurrent read-write transactions that InnoDB is capable of supporting is:

```
(innodb_page_size / 16) * (innodb_rollback_segments - 32)
```

• If each transaction performs an INSERT **and** an UPDATE or DELETE operation, the number of concurrent read-write transactions that InnoDB is capable of supporting is:

```
(innodb_page_size / 16 / 2) * (innodb_rollback_segments - 32)
```

• If each transaction performs an INSERT operation on a temporary table, the number of concurrent read-write transactions that InnoDB is capable of supporting is:

```
(innodb_page_size / 16) * 32
```

• If each transaction performs an INSERT **and** an UPDATE or DELETE operation on a temporary table, the number of concurrent read-write transactions that InnoDB is capable of supporting is:

```
(innodb_page_size / 16 / 2) * 32
```

# <span id="page-65-0"></span>**14.7 InnoDB Locking and Transaction Model**

To implement a large-scale, busy, or highly reliable database application, to port substantial code from a different database system, or to tune MySQL performance, it is important to understand InnoDB locking and the InnoDB transaction model.

This section discusses several topics related to InnoDB locking and the InnoDB transaction model with which you should be familiar.

- [Section 14.7.1, "InnoDB Locking"](#page-66-0) describes lock types used by InnoDB.
- [Section 14.7.2, "InnoDB Transaction Model"](#page-70-0) describes transaction isolation levels and the locking strategies used by each. It also discusses the use of autocommit, consistent non-locking reads, and locking reads.

- [Section 14.7.3, "Locks Set by Different SQL Statements in InnoDB"](#page-77-0) discusses specific types of locks set in InnoDB for various statements.
- [Section 14.7.4, "Phantom Rows"](#page-81-0) describes how InnoDB uses next-key locking to avoid phantom rows.
- [Section 14.7.5, "Deadlocks in InnoDB"](#page-81-1) provides a deadlock example, discusses deadlock detection, and provides tips for minimizing and handling deadlocks in InnoDB.

# <span id="page-66-0"></span>**14.7.1 InnoDB Locking**

This section describes lock types used by InnoDB.

- [Shared and Exclusive Locks](#page-66-1)
- [Intention Locks](#page-66-2)
- [Record Locks](#page-67-0)
- [Gap Locks](#page-67-1)
- [Next-Key Locks](#page-68-0)
- [Insert Intention Locks](#page-69-0)
- [AUTO-INC Locks](#page-69-1)
- [Predicate Locks for Spatial Indexes](#page-70-2)

# <span id="page-66-1"></span>**Shared and Exclusive Locks**

InnoDB implements standard row-level locking where there are two types of locks, shared (S) locks and exclusive (X) locks.

- A shared (S) lock permits the transaction that holds the lock to read a row.
- An exclusive (X) lock permits the transaction that holds the lock to update or delete a row.

If transaction T1 holds a shared (S) lock on row r, then requests from some distinct transaction T2 for a lock on row r are handled as follows:

- A request by T2 for an S lock can be granted immediately. As a result, both T1 and T2 hold an S lock on r.
- A request by T2 for an X lock cannot be granted immediately.

If a transaction T1 holds an exclusive (X) lock on row r, a request from some distinct transaction T2 for a lock of either type on r cannot be granted immediately. Instead, transaction T2 has to wait for transaction T1 to release its lock on row r.

# <span id="page-66-2"></span>**Intention Locks**

InnoDB supports multiple granularity locking which permits coexistence of row locks and table locks. For example, a statement such as LOCK TABLES ... WRITE takes an exclusive lock (an X lock) on the specified table. To make locking at multiple granularity levels practical, InnoDB uses intention locks. Intention locks are table-level locks that indicate which type of lock (shared or exclusive) a transaction requires later for a row in a table. There are two types of intention locks:

- An intention shared lock (IS) indicates that a transaction intends to set a shared lock on individual rows in a table.
- An intention exclusive lock (IX) indicates that a transaction intends to set an exclusive lock on individual rows in a table.

For example, SELECT ... LOCK IN SHARE MODE sets an IS lock, and SELECT ... FOR UPDATE sets an IX lock.

The intention locking protocol is as follows:

- Before a transaction can acquire a shared lock on a row in a table, it must first acquire an IS lock or stronger on the table.
- Before a transaction can acquire an exclusive lock on a row in a table, it must first acquire an IX lock on the table.

Table-level lock type compatibility is summarized in the following matrix.

|    | X        | IX         | S          | IS         |
|----|----------|------------|------------|------------|
| X  | Conflict | Conflict   | Conflict   | Conflict   |
| IX | Conflict | Compatible | Conflict   | Compatible |
| S  | Conflict | Conflict   | Compatible | Compatible |
| IS | Conflict | Compatible | Compatible | Compatible |

A lock is granted to a requesting transaction if it is compatible with existing locks, but not if it conflicts with existing locks. A transaction waits until the conflicting existing lock is released. If a lock request conflicts with an existing lock and cannot be granted because it would cause deadlock, an error occurs.

Intention locks do not block anything except full table requests (for example, LOCK TABLES ... WRITE). The main purpose of intention locks is to show that someone is locking a row, or going to lock a row in the table.

Transaction data for an intention lock appears similar to the following in SHOW ENGINE INNODB STATUS and InnoDB monitor output:

```
TABLE LOCK table `test`.`t` trx id 10080 lock mode IX
```

# <span id="page-67-0"></span>**Record Locks**

A record lock is a lock on an index record. For example, SELECT c1 FROM t WHERE c1 = 10 FOR UPDATE; prevents any other transaction from inserting, updating, or deleting rows where the value of t.c1 is 10.

Record locks always lock index records, even if a table is defined with no indexes. For such cases, InnoDB creates a hidden clustered index and uses this index for record locking. See [Section 14.6.2.1,](#page-41-1) ["Clustered and Secondary Indexes"](#page-41-1).

Transaction data for a record lock appears similar to the following in SHOW ENGINE INNODB STATUS and InnoDB monitor output:

```
RECORD LOCKS space id 58 page no 3 n bits 72 index `PRIMARY` of table `test`.`t`
trx id 10078 lock_mode X locks rec but not gap
Record lock, heap no 2 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 8000000a; asc ;;
 1: len 6; hex 00000000274f; asc 'O;;
 2: len 7; hex b60000019d0110; asc ;;
```

## <span id="page-67-1"></span>**Gap Locks**

A gap lock is a lock on a gap between index records, or a lock on the gap before the first or after the last index record. For example, SELECT c1 FROM t WHERE c1 BETWEEN 10 and 20 FOR UPDATE; prevents other transactions from inserting a value of 15 into column t.c1, whether or not there was already any such value in the column, because the gaps between all existing values in the range are locked.

A gap might span a single index value, multiple index values, or even be empty.

Gap locks are part of the tradeoff between performance and concurrency, and are used in some transaction isolation levels and not others.

Gap locking is not needed for statements that lock rows using a unique index to search for a unique row. (This does not include the case that the search condition includes only some columns of a multiple-column unique index; in that case, gap locking does occur.) For example, if the id column has a unique index, the following statement uses only an index-record lock for the row having id value 100 and it does not matter whether other sessions insert rows in the preceding gap:

```
SELECT * FROM child WHERE id = 100;
```

If id is not indexed or has a nonunique index, the statement does lock the preceding gap.

It is also worth noting here that conflicting locks can be held on a gap by different transactions. For example, transaction A can hold a shared gap lock (gap S-lock) on a gap while transaction B holds an exclusive gap lock (gap X-lock) on the same gap. The reason conflicting gap locks are allowed is that if a record is purged from an index, the gap locks held on the record by different transactions must be merged.

Gap locks in InnoDB are "purely inhibitive", which means that their only purpose is to prevent other transactions from inserting to the gap. Gap locks can co-exist. A gap lock taken by one transaction does not prevent another transaction from taking a gap lock on the same gap. There is no difference between shared and exclusive gap locks. They do not conflict with each other, and they perform the same function.

Gap locking can be disabled explicitly. This occurs if you change the transaction isolation level to [READ](#page-71-0) [COMMITTED](#page-71-0) or enable the innodb\_locks\_unsafe\_for\_binlog system variable (which is now deprecated). In this case, gap locking is disabled for searches and index scans and is used only for foreign-key constraint checking and duplicate-key checking.

There are also other effects of using the [READ COMMITTED](#page-71-0) isolation level or enabling innodb\_locks\_unsafe\_for\_binlog. Record locks for nonmatching rows are released after MySQL has evaluated the WHERE condition. For UPDATE statements, InnoDB does a "semi-consistent" read, such that it returns the latest committed version to MySQL so that MySQL can determine whether the row matches the WHERE condition of the UPDATE.

## <span id="page-68-0"></span>**Next-Key Locks**

A next-key lock is a combination of a record lock on the index record and a gap lock on the gap before the index record.

InnoDB performs row-level locking in such a way that when it searches or scans a table index, it sets shared or exclusive locks on the index records it encounters. Thus, the row-level locks are actually index-record locks. A next-key lock on an index record also affects the "gap" before that index record. That is, a next-key lock is an index-record lock plus a gap lock on the gap preceding the index record. If one session has a shared or exclusive lock on record R in an index, another session cannot insert a new index record in the gap immediately before R in the index order.

Suppose that an index contains the values 10, 11, 13, and 20. The possible next-key locks for this index cover the following intervals, where a round bracket denotes exclusion of the interval endpoint and a square bracket denotes inclusion of the endpoint:

```
(negative infinity, 10]
(10, 11]
(11, 13]
(13, 20]
(20, positive infinity)
```

For the last interval, the next-key lock locks the gap above the largest value in the index and the "supremum" pseudo-record having a value higher than any value actually in the index. The supremum is not a real index record, so, in effect, this next-key lock locks only the gap following the largest index value.

By default, InnoDB operates in [REPEATABLE READ](#page-70-3) transaction isolation level. In this case, InnoDB uses next-key locks for searches and index scans, which prevents phantom rows (see [Section 14.7.4,](#page-81-0) ["Phantom Rows"](#page-81-0)).

Transaction data for a next-key lock appears similar to the following in SHOW ENGINE INNODB STATUS and InnoDB monitor output:

```
RECORD LOCKS space id 58 page no 3 n bits 72 index `PRIMARY` of table `test`.`t`
trx id 10080 lock_mode X
Record lock, heap no 1 PHYSICAL RECORD: n_fields 1; compact format; info bits 0
 0: len 8; hex 73757072656d756d; asc supremum;;
Record lock, heap no 2 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 8000000a; asc ;;
 1: len 6; hex 00000000274f; asc 'O;;
 2: len 7; hex b60000019d0110; asc ;;
```

# <span id="page-69-0"></span>**Insert Intention Locks**

An insert intention lock is a type of gap lock set by INSERT operations prior to row insertion. This lock signals the intent to insert in such a way that multiple transactions inserting into the same index gap need not wait for each other if they are not inserting at the same position within the gap. Suppose that there are index records with values of 4 and 7. Separate transactions that attempt to insert values of 5 and 6, respectively, each lock the gap between 4 and 7 with insert intention locks prior to obtaining the exclusive lock on the inserted row, but do not block each other because the rows are nonconflicting.

The following example demonstrates a transaction taking an insert intention lock prior to obtaining an exclusive lock on the inserted record. The example involves two clients, A and B.

Client A creates a table containing two index records (90 and 102) and then starts a transaction that places an exclusive lock on index records with an ID greater than 100. The exclusive lock includes a gap lock before record 102:

```
mysql> CREATE TABLE child (id int(11) NOT NULL, PRIMARY KEY(id)) ENGINE=InnoDB;
mysql> INSERT INTO child (id) values (90),(102);
mysql> START TRANSACTION;
mysql> SELECT * FROM child WHERE id > 100 FOR UPDATE;
+-----+
| id |
+-----+
| 102 |
+-----+
```

Client B begins a transaction to insert a record into the gap. The transaction takes an insert intention lock while it waits to obtain an exclusive lock.

```
mysql> START TRANSACTION;
mysql> INSERT INTO child (id) VALUES (101);
```

Transaction data for an insert intention lock appears similar to the following in SHOW ENGINE INNODB STATUS and InnoDB monitor output:

```
RECORD LOCKS space id 31 page no 3 n bits 72 index `PRIMARY` of table `test`.`child`
trx id 8731 lock_mode X locks gap before rec insert intention waiting
Record lock, heap no 3 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 80000066; asc f;;
 1: len 6; hex 000000002215; asc " ;;
 2: len 7; hex 9000000172011c; asc r ;;...
```

## <span id="page-69-1"></span>**AUTO-INC Locks**

An AUTO-INC lock is a special table-level lock taken by transactions inserting into tables with AUTO\_INCREMENT columns. In the simplest case, if one transaction is inserting values into the table, any other transactions must wait to do their own inserts into that table, so that rows inserted by the first transaction receive consecutive primary key values.

The [innodb\\_autoinc\\_lock\\_mode](#page-191-0) variable controls the algorithm used for auto-increment locking. It allows you to choose how to trade off between predictable sequences of auto-increment values and maximum concurrency for insert operations.

For more information, see [Section 14.6.1.6, "AUTO\\_INCREMENT Handling in InnoDB"](#page-35-0).

# <span id="page-70-2"></span>**Predicate Locks for Spatial Indexes**

InnoDB supports SPATIAL indexing of columns containing spatial data (see Section 11.4.8, "Optimizing Spatial Analysis").

To handle locking for operations involving SPATIAL indexes, next-key locking does not work well to support [REPEATABLE READ](#page-70-3) or [SERIALIZABLE](#page-73-1) transaction isolation levels. There is no absolute ordering concept in multidimensional data, so it is not clear which is the "next" key.

To enable support of isolation levels for tables with SPATIAL indexes, InnoDB uses predicate locks. A SPATIAL index contains minimum bounding rectangle (MBR) values, so InnoDB enforces consistent read on the index by setting a predicate lock on the MBR value used for a query. Other transactions cannot insert or modify a row that would match the query condition.

# <span id="page-70-0"></span>**14.7.2 InnoDB Transaction Model**

The InnoDB transaction model aims combine the best properties of a multi-versioning database with traditional two-phase locking. InnoDB performs locking at the row level and runs queries as nonlocking consistent reads by default, in the style of Oracle. The lock information in InnoDB is stored spaceefficiently so that lock escalation is not needed. Typically, several users are permitted to lock every row in InnoDB tables, or any random subset of the rows, without causing InnoDB memory exhaustion.

# <span id="page-70-1"></span>**14.7.2.1 Transaction Isolation Levels**

Transaction isolation is one of the foundations of database processing. Isolation is the I in the acronym ACID; the isolation level is the setting that fine-tunes the balance between performance and reliability, consistency, and reproducibility of results when multiple transactions are making changes and performing queries at the same time.

InnoDB offers all four transaction isolation levels described by the SQL:1992 standard: [READ](#page-73-2) [UNCOMMITTED](#page-73-2), [READ COMMITTED](#page-71-0), [REPEATABLE READ](#page-70-3), and [SERIALIZABLE](#page-73-1). The default isolation level for InnoDB is [REPEATABLE READ](#page-70-3).

A user can change the isolation level for a single session or for all subsequent connections with the SET TRANSACTION statement. To set the server's default isolation level for all connections, use the - transaction-isolation option on the command line or in an option file. For detailed information about isolation levels and level-setting syntax, see Section 13.3.6, "SET TRANSACTION Statement".

InnoDB supports each of the transaction isolation levels described here using different locking strategies. You can enforce a high degree of consistency with the default [REPEATABLE READ](#page-70-3) level, for operations on crucial data where ACID compliance is important. Or you can relax the consistency rules with [READ COMMITTED](#page-71-0) or even [READ UNCOMMITTED](#page-73-2), in situations such as bulk reporting where precise consistency and repeatable results are less important than minimizing the amount of overhead for locking. [SERIALIZABLE](#page-73-1) enforces even stricter rules than [REPEATABLE READ](#page-70-3), and is used mainly in specialized situations, such as with XA transactions and for troubleshooting issues with concurrency and deadlocks.

The following list describes how MySQL supports the different transaction levels. The list goes from the most commonly used level to the least used.

#### <span id="page-70-3"></span>• REPEATABLE READ

This is the default isolation level for InnoDB. Consistent reads within the same transaction read the snapshot established by the first read. This means that if you issue several plain (nonlocking) SELECT statements within the same transaction, these SELECT statements are consistent also with respect to each other. See [Section 14.7.2.3, "Consistent Nonlocking Reads".](#page-74-0)

For locking reads (SELECT with FOR UPDATE or LOCK IN SHARE MODE), UPDATE, and DELETE statements, locking depends on whether the statement uses a unique index with a unique search condition or a range-type search condition.

- For a unique index with a unique search condition, InnoDB locks only the index record found, not the gap before it.
- For other search conditions, InnoDB locks the index range scanned, using gap locks or next-key locks to block insertions by other sessions into the gaps covered by the range. For information about gap locks and next-key locks, see [Section 14.7.1, "InnoDB Locking".](#page-66-0)

It is not recommended to mix locking statements (UPDATE, INSERT, DELETE, or SELECT ... FOR ...) with non-locking SELECT statements in a single [REPEATABLE READ](#page-70-3) transaction, because typically in such cases you want [SERIALIZABLE](#page-73-1) instead. This is because a non-locking SELECT statement presents the state of the database from a read-view which consists of transactions committed before the read-view was created and before the current transaction's own writes, while the locking statements see and modify the most recent state of the database to use locking. In general, these two different table states are inconsistent with each other and difficult to parse.

#### <span id="page-71-0"></span>• READ COMMITTED

Each consistent read, even within the same transaction, sets and reads its own fresh snapshot. For information about consistent reads, see [Section 14.7.2.3, "Consistent Nonlocking Reads".](#page-74-0)

For locking reads (SELECT with FOR UPDATE or LOCK IN SHARE MODE), UPDATE statements, and DELETE statements, InnoDB locks only index records, not the gaps before them, and thus permits the free insertion of new records next to locked records. Gap locking is only used for foreign-key constraint checking and duplicate-key checking.

Because gap locking is disabled, phantom row problems may occur, as other sessions can insert new rows into the gaps. For information about phantom rows, see [Section 14.7.4, "Phantom Rows".](#page-81-0)

Only row-based binary logging is supported with the READ COMMITTED isolation level. If you use READ COMMITTED with binlog\_format=MIXED, the server automatically uses row-based logging.

Using READ COMMITTED has additional effects:

- For UPDATE or DELETE statements, InnoDB holds locks only for rows that it updates or deletes. Record locks for nonmatching rows are released after MySQL has evaluated the WHERE condition. This greatly reduces the probability of deadlocks, but they can still happen.
- For UPDATE statements, if a row is already locked, InnoDB performs a "semi-consistent" read, returning the latest committed version to MySQL so that MySQL can determine whether the row matches the WHERE condition of the UPDATE. If the row matches (must be updated), MySQL reads the row again and this time InnoDB either locks it or waits for a lock on it.

Consider the following example, beginning with this table:

```
CREATE TABLE t (a INT NOT NULL, b INT) ENGINE = InnoDB;
INSERT INTO t VALUES (1,2),(2,3),(3,2),(4,3),(5,2);
COMMIT;
```

In this case, the table has no indexes, so searches and index scans use the hidden clustered index for record locking (see [Section 14.6.2.1, "Clustered and Secondary Indexes"\)](#page-41-1) rather than indexed columns.

Suppose that one session performs an UPDATE using these statements:

```
# Session A
```

```
START TRANSACTION;
UPDATE t SET b = 5 WHERE b = 3;
```

Suppose also that a second session performs an UPDATE by executing this statement following those of the first session:

```
# Session B
UPDATE t SET b = 4 WHERE b = 2;
```

As [InnoDB](#page-0-0) executes each UPDATE, it first acquires an exclusive lock for each row that it reads, and then determines whether to modify it. If [InnoDB](#page-0-0) does not modify the row, it releases the lock. Otherwise, [InnoDB](#page-0-0) retains the lock until the end of the transaction. This affects transaction processing as follows.

When using the default REPEATABLE READ isolation level, the first UPDATE acquires an x-lock on each row that it reads and does not release any of them:

```
x-lock(1,2); retain x-lock
x-lock(2,3); update(2,3) to (2,5); retain x-lock
x-lock(3,2); retain x-lock
x-lock(4,3); update(4,3) to (4,5); retain x-lock
x-lock(5,2); retain x-lock
```

The second UPDATE blocks as soon as it tries to acquire any locks (because first update has retained locks on all rows), and does not proceed until the first UPDATE commits or rolls back:

```
x-lock(1,2); block and wait for first UPDATE to commit or roll back
```

If READ COMMITTED is used instead, the first UPDATE acquires an x-lock on each row that it reads and releases those for rows that it does not modify:

```
x-lock(1,2); unlock(1,2)
x-lock(2,3); update(2,3) to (2,5); retain x-lock
x-lock(3,2); unlock(3,2)
x-lock(4,3); update(4,3) to (4,5); retain x-lock
x-lock(5,2); unlock(5,2)
```

For the second UPDATE, InnoDB does a "semi-consistent" read, returning the latest committed version of each row that it reads to MySQL so that MySQL can determine whether the row matches the WHERE condition of the UPDATE:

```
x-lock(1,2); update(1,2) to (1,4); retain x-lock
x-lock(2,3); unlock(2,3)
x-lock(3,2); update(3,2) to (3,4); retain x-lock
x-lock(4,3); unlock(4,3)
x-lock(5,2); update(5,2) to (5,4); retain x-lock
```

However, if the WHERE condition includes an indexed column, and InnoDB uses the index, only the indexed column is considered when taking and retaining record locks. In the following example, the first UPDATE takes and retains an x-lock on each row where b = 2. The second UPDATE blocks when it tries to acquire x-locks on the same records, as it also uses the index defined on column b.

```
CREATE TABLE t (a INT NOT NULL, b INT, c INT, INDEX (b)) ENGINE = InnoDB;
INSERT INTO t VALUES (1,2,3),(2,2,4);
COMMIT;
# Session A
START TRANSACTION;
UPDATE t SET b = 3 WHERE b = 2 AND c = 3;
# Session B
```

```
UPDATE t SET b = 4 WHERE b = 2 AND c = 4;
```

The effects of using the READ COMMITTED isolation level are the same as enabling the deprecated innodb\_locks\_unsafe\_for\_binlog variable, with these exceptions:

- Enabling innodb\_locks\_unsafe\_for\_binlog is a global setting and affects all sessions, whereas the isolation level can be set globally for all sessions, or individually per session.
- innodb\_locks\_unsafe\_for\_binlog can be set only at server startup, whereas the isolation level can be set at startup or changed at runtime.

READ COMMITTED therefore offers finer and more flexible control than innodb\_locks\_unsafe\_for\_binlog.

<span id="page-73-2"></span>• READ UNCOMMITTED

SELECT statements are performed in a nonlocking fashion, but a possible earlier version of a row might be used. Thus, using this isolation level, such reads are not consistent. This is also called a dirty read. Otherwise, this isolation level works like [READ COMMITTED](#page-71-0).

<span id="page-73-1"></span>• SERIALIZABLE

This level is like [REPEATABLE READ](#page-70-3), but InnoDB implicitly converts all plain SELECT statements to SELECT ... LOCK IN SHARE MODE if autocommit is disabled. If autocommit is enabled, the SELECT is its own transaction. It therefore is known to be read only and can be serialized if performed as a consistent (nonlocking) read and need not block for other transactions. (To force a plain SELECT to block if other transactions have modified the selected rows, disable autocommit.)

## <span id="page-73-0"></span>**14.7.2.2 autocommit, Commit, and Rollback**

In InnoDB, all user activity occurs inside a transaction. If autocommit mode is enabled, each SQL statement forms a single transaction on its own. By default, MySQL starts the session for each new connection with autocommit enabled, so MySQL does a commit after each SQL statement if that statement did not return an error. If a statement returns an error, the commit or rollback behavior depends on the error. See Section 14.22.4, "InnoDB Error Handling".

A session that has autocommit enabled can perform a multiple-statement transaction by starting it with an explicit START TRANSACTION or BEGIN statement and ending it with a COMMIT or ROLLBACK statement. See Section 13.3.1, "START TRANSACTION, COMMIT, and ROLLBACK Statements".

If autocommit mode is disabled within a session with SET autocommit = 0, the session always has a transaction open. A COMMIT or ROLLBACK statement ends the current transaction and a new one starts.

If a session that has autocommit disabled ends without explicitly committing the final transaction, MySQL rolls back that transaction.

Some statements implicitly end a transaction, as if you had done a COMMIT before executing the statement. For details, see Section 13.3.3, "Statements That Cause an Implicit Commit".

A COMMIT means that the changes made in the current transaction are made permanent and become visible to other sessions. A ROLLBACK statement, on the other hand, cancels all modifications made by the current transaction. Both COMMIT and ROLLBACK release all InnoDB locks that were set during the current transaction.

#### **Grouping DML Operations with Transactions**

By default, connection to the MySQL server begins with autocommit mode enabled, which automatically commits every SQL statement as you execute it. This mode of operation might be unfamiliar if you have experience with other database systems, where it is standard practice to issue a sequence of DML statements and commit them or roll them back all together.

To use multiple-statement transactions, switch autocommit off with the SQL statement SET autocommit = 0 and end each transaction with COMMIT or ROLLBACK as appropriate. To leave autocommit on, begin each transaction with START TRANSACTION and end it with COMMIT or ROLLBACK. The following example shows two transactions. The first is committed; the second is rolled back.

```
$> mysql test
mysql> CREATE TABLE customer (a INT, b CHAR (20), INDEX (a));
Query OK, 0 rows affected (0.00 sec)
mysql> -- Do a transaction with autocommit turned on.
mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO customer VALUES (10, 'Heikki');
Query OK, 1 row affected (0.00 sec)
mysql> COMMIT;
Query OK, 0 rows affected (0.00 sec)
mysql> -- Do another transaction with autocommit turned off.
mysql> SET autocommit=0;
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO customer VALUES (15, 'John');
Query OK, 1 row affected (0.00 sec)
mysql> INSERT INTO customer VALUES (20, 'Paul');
Query OK, 1 row affected (0.00 sec)
mysql> DELETE FROM customer WHERE b = 'Heikki';
Query OK, 1 row affected (0.00 sec)
mysql> -- Now we undo those last 2 inserts and the delete.
mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM customer;
+------+--------+
| a | b |
+------+--------+
| 10 | Heikki |
+------+--------+
1 row in set (0.00 sec)
mysql>
```

#### **Transactions in Client-Side Languages**

In APIs such as PHP, Perl DBI, JDBC, ODBC, or the standard C call interface of MySQL, you can send transaction control statements such as COMMIT to the MySQL server as strings just like any other SQL statements such as SELECT or INSERT. Some APIs also offer separate special transaction commit and rollback functions or methods.

## <span id="page-74-0"></span>**14.7.2.3 Consistent Nonlocking Reads**

A consistent read means that InnoDB uses multi-versioning to present to a query a snapshot of the database at a point in time. The query sees the changes made by transactions that committed before that point in time, and no changes made by later or uncommitted transactions. The exception to this rule is that the query sees the changes made by earlier statements within the same transaction. This exception causes the following anomaly: If you update some rows in a table, a SELECT sees the latest version of the updated rows, but it might also see older versions of any rows. If other sessions simultaneously update the same table, the anomaly means that you might see the table in a state that never existed in the database.

If the transaction isolation level is [REPEATABLE READ](#page-70-3) (the default level), all consistent reads within the same transaction read the snapshot established by the first such read in that transaction. You can get a fresher snapshot for your queries by committing the current transaction and after that issuing new queries.

With [READ COMMITTED](#page-71-0) isolation level, each consistent read within a transaction sets and reads its own fresh snapshot.

Consistent read is the default mode in which InnoDB processes SELECT statements in [READ](#page-71-0) [COMMITTED](#page-71-0) and [REPEATABLE READ](#page-70-3) isolation levels. A consistent read does not set any locks on the tables it accesses, and therefore other sessions are free to modify those tables at the same time a consistent read is being performed on the table.

Suppose that you are running in the default [REPEATABLE READ](#page-70-3) isolation level. When you issue a consistent read (that is, an ordinary SELECT statement), InnoDB gives your transaction a timepoint according to which your query sees the database. If another transaction deletes a row and commits after your timepoint was assigned, you do not see the row as having been deleted. Inserts and updates are treated similarly.

![](_page_75_Picture_3.jpeg)

#### **Note**

The snapshot of the database state applies to SELECT statements within a transaction, not necessarily to DML statements. If you insert or modify some rows and then commit that transaction, a DELETE or UPDATE statement issued from another concurrent REPEATABLE READ transaction could affect those justcommitted rows, even though the session could not query them. If a transaction does update or delete rows committed by a different transaction, those changes do become visible to the current transaction. For example, you might encounter a situation like the following:

```
SELECT COUNT(c1) FROM t1 WHERE c1 = 'xyz';
-- Returns 0: no rows match.
DELETE FROM t1 WHERE c1 = 'xyz';
-- Deletes several rows recently committed by other transaction.
SELECT COUNT(c2) FROM t1 WHERE c2 = 'abc';
-- Returns 0: no rows match.
UPDATE t1 SET c2 = 'cba' WHERE c2 = 'abc';
-- Affects 10 rows: another txn just committed 10 rows with 'abc' values.
SELECT COUNT(c2) FROM t1 WHERE c2 = 'cba';
-- Returns 10: this txn can now see the rows it just updated.
```

You can advance your timepoint by committing your transaction and then doing another SELECT or START TRANSACTION WITH CONSISTENT SNAPSHOT.

This is called multi-versioned concurrency control.

In the following example, session A sees the row inserted by B only when B has committed the insert and A has committed as well, so that the timepoint is advanced past the commit of B.

```
 Session A Session B
 SET autocommit=0; SET autocommit=0;
time
| SELECT * FROM t;
| empty set
| INSERT INTO t VALUES (1, 2);
|
v SELECT * FROM t;
 empty set
 COMMIT;
 SELECT * FROM t;
 empty set
 COMMIT;
 SELECT * FROM t;
 ---------------------
 | 1 | 2 |
 ---------------------
```

If you want to see the "freshest" state of the database, use either the [READ COMMITTED](#page-71-0) isolation level or a locking read:

```
SELECT * FROM t LOCK IN SHARE MODE;
```

With [READ COMMITTED](#page-71-0) isolation level, each consistent read within a transaction sets and reads its own fresh snapshot. With LOCK IN SHARE MODE, a locking read occurs instead: A SELECT blocks until the transaction containing the freshest rows ends (see [Section 14.7.2.4, "Locking Reads"](#page-76-0)).

Consistent read does not work over certain DDL statements:

- Consistent read does not work over DROP TABLE, because MySQL cannot use a table that has been dropped and InnoDB destroys the table.
- Consistent read does not work over ALTER TABLE operations that make a temporary copy of the original table and delete the original table when the temporary copy is built. When you reissue a consistent read within a transaction, rows in the new table are not visible because those rows did not exist when the transaction's snapshot was taken. In this case, the transaction returns an error: [ER\\_TABLE\\_DEF\\_CHANGED](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_table_def_changed), "Table definition has changed, please retry transaction".

The type of read varies for selects in clauses like INSERT INTO ... SELECT, UPDATE ... (SELECT), and CREATE TABLE ... SELECT that do not specify FOR UPDATE or LOCK IN SHARE MODE:

- By default, InnoDB uses stronger locks in those statements and the SELECT part acts like [READ](#page-71-0) [COMMITTED](#page-71-0), where each consistent read, even within the same transaction, sets and reads its own fresh snapshot.
- To perform a nonlocking read in such cases, enable the innodb\_locks\_unsafe\_for\_binlog option and set the isolation level of the transaction to [READ UNCOMMITTED](#page-73-2), [READ COMMITTED](#page-71-0), or [REPEATABLE READ](#page-70-3) to avoid setting locks on rows read from the selected table.

## <span id="page-76-0"></span>**14.7.2.4 Locking Reads**

If you query data and then insert or update related data within the same transaction, the regular SELECT statement does not give enough protection. Other transactions can update or delete the same rows you just queried. InnoDB supports two types of locking reads that offer extra safety:

• SELECT ... LOCK IN SHARE MODE

Sets a shared mode lock on any rows that are read. Other sessions can read the rows, but cannot modify them until your transaction commits. If any of these rows were changed by another transaction that has not yet committed, your query waits until that transaction ends and then uses the latest values.

• SELECT ... FOR UPDATE

For index records the search encounters, locks the rows and any associated index entries, the same as if you issued an UPDATE statement for those rows. Other transactions are blocked from updating those rows, from doing SELECT ... LOCK IN SHARE MODE, or from reading the data in certain transaction isolation levels. Consistent reads ignore any locks set on the records that exist in the read view. (Old versions of a record cannot be locked; they are reconstructed by applying undo logs on an in-memory copy of the record.)

These clauses are primarily useful when dealing with tree-structured or graph-structured data, either in a single table or split across multiple tables. You traverse edges or tree branches from one place to another, while reserving the right to come back and change any of these "pointer" values.

All locks set by LOCK IN SHARE MODE and FOR UPDATE queries are released when the transaction is committed or rolled back.

![](_page_76_Picture_16.jpeg)

#### **Note**

Locking reads are only possible when autocommit is disabled (either by beginning transaction with START TRANSACTION or by setting autocommit to 0.

A locking read clause in an outer statement does not lock the rows of a table in a nested subquery unless a locking read clause is also specified in the subquery. For example, the following statement does not lock rows in table t2.

```
SELECT * FROM t1 WHERE c1 = (SELECT c1 FROM t2) FOR UPDATE;
```

To lock rows in table t2, add a locking read clause to the subquery:

```
SELECT * FROM t1 WHERE c1 = (SELECT c1 FROM t2 FOR UPDATE) FOR UPDATE;
```

#### **Locking Read Examples**

Suppose that you want to insert a new row into a table child, and make sure that the child row has a parent row in table parent. Your application code can ensure referential integrity throughout this sequence of operations.

First, use a consistent read to query the table PARENT and verify that the parent row exists. Can you safely insert the child row to table CHILD? No, because some other session could delete the parent row in the moment between your SELECT and your INSERT, without you being aware of it.

To avoid this potential issue, perform the SELECT using LOCK IN SHARE MODE:

```
SELECT * FROM parent WHERE NAME = 'Jones' LOCK IN SHARE MODE;
```

After the LOCK IN SHARE MODE query returns the parent 'Jones', you can safely add the child record to the CHILD table and commit the transaction. Any transaction that tries to acquire an exclusive lock in the applicable row in the PARENT table waits until you are finished, that is, until the data in all tables is in a consistent state.

For another example, consider an integer counter field in a table CHILD\_CODES, used to assign a unique identifier to each child added to table CHILD. Do not use either consistent read or a shared mode read to read the present value of the counter, because two users of the database could see the same value for the counter, and a duplicate-key error occurs if two transactions attempt to add rows with the same identifier to the CHILD table.

Here, LOCK IN SHARE MODE is not a good solution because if two users read the counter at the same time, at least one of them ends up in deadlock when it attempts to update the counter.

To implement reading and incrementing the counter, first perform a locking read of the counter using FOR UPDATE, and then increment the counter. For example:

```
SELECT counter_field FROM child_codes FOR UPDATE;
UPDATE child_codes SET counter_field = counter_field + 1;
```

A SELECT ... FOR UPDATE reads the latest available data, setting exclusive locks on each row it reads. Thus, it sets the same locks a searched SQL UPDATE would set on the rows.

The preceding description is merely an example of how SELECT ... FOR UPDATE works. In MySQL, the specific task of generating a unique identifier actually can be accomplished using only a single access to the table:

```
UPDATE child_codes SET counter_field = LAST_INSERT_ID(counter_field + 1);
SELECT LAST_INSERT_ID();
```

The SELECT statement merely retrieves the identifier information (specific to the current connection). It does not access any table.

# <span id="page-77-0"></span>**14.7.3 Locks Set by Different SQL Statements in InnoDB**

A locking read, an UPDATE, or a DELETE generally set record locks on every index record that is scanned in the processing of an SQL statement. It does not matter whether there are WHERE conditions in the statement that would exclude the row. InnoDB does not remember the exact WHERE condition, but only knows which index ranges were scanned. The locks are normally nextkey locks that also block inserts into the "gap" immediately before the record. However, gap locking can be disabled explicitly, which causes next-key locking not to be used. For more information, see

[Section 14.7.1, "InnoDB Locking".](#page-66-0) The transaction isolation level can also affect which locks are set; see [Section 14.7.2.1, "Transaction Isolation Levels"](#page-70-1).

If a secondary index is used in a search and the index record locks to be set are exclusive, InnoDB also retrieves the corresponding clustered index records and sets locks on them.

If you have no indexes suitable for your statement and MySQL must scan the entire table to process the statement, every row of the table becomes locked, which in turn blocks all inserts by other users to the table. It is important to create good indexes so that your queries do not scan more rows than necessary.

InnoDB sets specific types of locks as follows.

- SELECT ... FROM is a consistent read, reading a snapshot of the database and setting no locks unless the transaction isolation level is set to [SERIALIZABLE](#page-73-1). For [SERIALIZABLE](#page-73-1) level, the search sets shared next-key locks on the index records it encounters. However, only an index record lock is required for statements that lock rows using a unique index to search for a unique row.
- For SELECT ... FOR UPDATE or SELECT ... LOCK IN SHARE MODE, locks are acquired for scanned rows, and expected to be released for rows that do not qualify for inclusion in the result set (for example, if they do not meet the criteria given in the WHERE clause). However, in some cases, rows might not be unlocked immediately because the relationship between a result row and its original source is lost during query execution. For example, in a UNION, scanned (and locked) rows from a table might be inserted into a temporary table before evaluating whether they qualify for the result set. In this circumstance, the relationship of the rows in the temporary table to the rows in the original table is lost and the latter rows are not unlocked until the end of query execution.
- SELECT ... LOCK IN SHARE MODE sets shared next-key locks on all index records the search encounters. However, only an index record lock is required for statements that lock rows using a unique index to search for a unique row.
- SELECT ... FOR UPDATE sets an exclusive next-key lock on every record the search encounters. However, only an index record lock is required for statements that lock rows using a unique index to search for a unique row.

For index records the search encounters, SELECT ... FOR UPDATE blocks other sessions from doing SELECT ... LOCK IN SHARE MODE or from reading in certain transaction isolation levels. Consistent reads ignore any locks set on the records that exist in the read view.

- UPDATE ... WHERE ... sets an exclusive next-key lock on every record the search encounters. However, only an index record lock is required for statements that lock rows using a unique index to search for a unique row.
- When UPDATE modifies a clustered index record, implicit locks are taken on affected secondary index records. The UPDATE operation also takes shared locks on affected secondary index records when performing duplicate check scans prior to inserting new secondary index records, and when inserting new secondary index records.
- DELETE FROM ... WHERE ... sets an exclusive next-key lock on every record the search encounters. However, only an index record lock is required for statements that lock rows using a unique index to search for a unique row.
- INSERT sets an exclusive lock on the inserted row. This lock is an index-record lock, not a next-key lock (that is, there is no gap lock) and does not prevent other sessions from inserting into the gap before the inserted row.

Prior to inserting the row, a type of gap lock called an insert intention gap lock is set. This lock signals the intent to insert in such a way that multiple transactions inserting into the same index gap need not wait for each other if they are not inserting at the same position within the gap. Suppose that there are index records with values of 4 and 7. Separate transactions that attempt to insert values of 5 and 6 each lock the gap between 4 and 7 with insert intention locks prior to obtaining the exclusive lock on the inserted row, but do not block each other because the rows are nonconflicting.

If a duplicate-key error occurs, a shared lock on the duplicate index record is set. This use of a shared lock can result in deadlock should there be multiple sessions trying to insert the same row if another session already has an exclusive lock. This can occur if another session deletes the row. Suppose that an InnoDB table t1 has the following structure:

```
CREATE TABLE t1 (i INT, PRIMARY KEY (i)) ENGINE = InnoDB;
```

Now suppose that three sessions perform the following operations in order:

#### Session 1:

```
START TRANSACTION;
INSERT INTO t1 VALUES(1);
```

#### Session 2:

```
START TRANSACTION;
INSERT INTO t1 VALUES(1);
```

#### Session 3:

```
START TRANSACTION;
INSERT INTO t1 VALUES(1);
```

#### Session 1:

ROLLBACK;

The first operation by session 1 acquires an exclusive lock for the row. The operations by sessions 2 and 3 both result in a duplicate-key error and they both request a shared lock for the row. When session 1 rolls back, it releases its exclusive lock on the row and the queued shared lock requests for sessions 2 and 3 are granted. At this point, sessions 2 and 3 deadlock: Neither can acquire an exclusive lock for the row because of the shared lock held by the other.

A similar situation occurs if the table already contains a row with key value 1 and three sessions perform the following operations in order:

#### Session 1:

```
START TRANSACTION;
DELETE FROM t1 WHERE i = 1;
```

#### Session 2:

```
START TRANSACTION;
INSERT INTO t1 VALUES(1);
```

#### Session 3:

```
START TRANSACTION;
INSERT INTO t1 VALUES(1);
```

#### Session 1:

```
COMMIT;
```

The first operation by session 1 acquires an exclusive lock for the row. The operations by sessions 2 and 3 both result in a duplicate-key error and they both request a shared lock for the row. When session 1 commits, it releases its exclusive lock on the row and the queued shared lock requests for sessions 2 and 3 are granted. At this point, sessions 2 and 3 deadlock: Neither can acquire an exclusive lock for the row because of the shared lock held by the other.

• INSERT ... ON DUPLICATE KEY UPDATE differs from a simple INSERT in that an exclusive lock rather than a shared lock is placed on the row to be updated when a duplicate-key error occurs. An

exclusive index-record lock is taken for a duplicate primary key value. An exclusive next-key lock is taken for a duplicate unique key value.

- REPLACE is done like an INSERT if there is no collision on a unique key. Otherwise, an exclusive next-key lock is placed on the row to be replaced.
- INSERT INTO T SELECT ... FROM S WHERE ... sets an exclusive index record lock (without a gap lock) on each row inserted into T. If the transaction isolation level is [READ COMMITTED](#page-71-0), or innodb\_locks\_unsafe\_for\_binlog is enabled and the transaction isolation level is not [SERIALIZABLE](#page-73-1), InnoDB does the search on S as a consistent read (no locks). Otherwise, InnoDB sets shared next-key locks on rows from S. InnoDB has to set locks in the latter case: During rollforward recovery using a statement-based binary log, every SQL statement must be executed in exactly the same way it was done originally.

```
CREATE TABLE ... SELECT ... performs the SELECT with shared next-key locks or as a
consistent read, as for INSERT ... SELECT.
```

When a SELECT is used in the constructs REPLACE INTO t SELECT ... FROM s WHERE ... or UPDATE t ... WHERE col IN (SELECT ... FROM s ...), InnoDB sets shared next-key locks on rows from table s.

• InnoDB sets an exclusive lock on the end of the index associated with the AUTO\_INCREMENT column while initializing a previously specified AUTO\_INCREMENT column on a table.

With [innodb\\_autoinc\\_lock\\_mode=0](#page-191-0), InnoDB uses a special AUTO-INC table lock mode where the lock is obtained and held to the end of the current SQL statement (not to the end of the entire transaction) while accessing the auto-increment counter. Other clients cannot insert into the table while the AUTO-INC table lock is held. The same behavior occurs for "bulk inserts" with [innodb\\_autoinc\\_lock\\_mode=1](#page-191-0). Table-level AUTO-INC locks are not used with [innodb\\_autoinc\\_lock\\_mode=2](#page-191-0). For more information, See [Section 14.6.1.6,](#page-35-0) ["AUTO\\_INCREMENT Handling in InnoDB"](#page-35-0).

InnoDB fetches the value of a previously initialized AUTO\_INCREMENT column without setting any locks.

- If a FOREIGN KEY constraint is defined on a table, any insert, update, or delete that requires the constraint condition to be checked sets shared record-level locks on the records that it looks at to check the constraint. InnoDB also sets these locks in the case where the constraint fails.
- LOCK TABLES sets table locks, but it is the higher MySQL layer above the InnoDB layer that sets these locks. InnoDB is aware of table locks if innodb\_table\_locks = 1 (the default) and autocommit = 0, and the MySQL layer above InnoDB knows about row-level locks.

Otherwise, InnoDB's automatic deadlock detection cannot detect deadlocks where such table locks are involved. Also, because in this case the higher MySQL layer does not know about row-level locks, it is possible to get a table lock on a table where another session currently has row-level locks. However, this does not endanger transaction integrity, as discussed in [Section 14.7.5.2, "Deadlock](#page-83-0) [Detection".](#page-83-0)

• LOCK TABLES acquires two locks on each table if innodb\_table\_locks=1 (the default). In addition to a table lock on the MySQL layer, it also acquires an InnoDB table lock. To avoid acquiring InnoDB table locks, set innodb\_table\_locks=0. If no InnoDB table lock is acquired, LOCK TABLES completes even if some records of the tables are being locked by other transactions.

```
In MySQL 5.7, innodb_table_locks=0 has no effect for tables locked explicitly with LOCK
TABLES ... WRITE. It does have an effect for tables locked for read or write by LOCK
TABLES ... WRITE implicitly (for example, through triggers) or by LOCK TABLES ... READ.
```

• All InnoDB locks held by a transaction are released when the transaction is committed or aborted. Thus, it does not make much sense to invoke LOCK TABLES on InnoDB tables in autocommit=1 mode because the acquired InnoDB table locks would be released immediately.

• You cannot lock additional tables in the middle of a transaction because LOCK TABLES performs an implicit COMMIT and UNLOCK TABLES.

# <span id="page-81-0"></span>**14.7.4 Phantom Rows**

The so-called phantom problem occurs within a transaction when the same query produces different sets of rows at different times. For example, if a SELECT is executed twice, but returns a row the second time that was not returned the first time, the row is a "phantom" row.

Suppose that there is an index on the id column of the child table and that you want to read and lock all rows from the table having an identifier value larger than 100, with the intention of updating some column in the selected rows later:

```
SELECT * FROM child WHERE id > 100 FOR UPDATE;
```

The query scans the index starting from the first record where id is bigger than 100. Let the table contain rows having id values of 90 and 102. If the locks set on the index records in the scanned range do not lock out inserts made in the gaps (in this case, the gap between 90 and 102), another session can insert a new row into the table with an id of 101. If you were to execute the same SELECT within the same transaction, you would see a new row with an id of 101 (a "phantom") in the result set returned by the query. If we regard a set of rows as a data item, the new phantom child would violate the isolation principle of transactions that a transaction should be able to run so that the data it has read does not change during the transaction.

To prevent phantoms, InnoDB uses an algorithm called next-key locking that combines index-row locking with gap locking. InnoDB performs row-level locking in such a way that when it searches or scans a table index, it sets shared or exclusive locks on the index records it encounters. Thus, the rowlevel locks are actually index-record locks. In addition, a next-key lock on an index record also affects the "gap" before the index record. That is, a next-key lock is an index-record lock plus a gap lock on the gap preceding the index record. If one session has a shared or exclusive lock on record R in an index, another session cannot insert a new index record in the gap immediately before R in the index order.

When InnoDB scans an index, it can also lock the gap after the last record in the index. Just that happens in the preceding example: To prevent any insert into the table where id would be bigger than 100, the locks set by InnoDB include a lock on the gap following id value 102.

You can use next-key locking to implement a uniqueness check in your application: If you read your data in share mode and do not see a duplicate for a row you are going to insert, then you can safely insert your row and know that the next-key lock set on the successor of your row during the read prevents anyone meanwhile inserting a duplicate for your row. Thus, the next-key locking enables you to "lock" the nonexistence of something in your table.

Gap locking can be disabled as discussed in [Section 14.7.1, "InnoDB Locking"](#page-66-0). This may cause phantom problems because other sessions can insert new rows into the gaps when gap locking is disabled.

# <span id="page-81-1"></span>**14.7.5 Deadlocks in InnoDB**

A deadlock is a situation in which multiple transactions are unable to proceed because each transaction holds a lock that is needed by another one. Because all transactions involved are waiting for the same resource to become available, none of them ever releases the lock it holds.

A deadlock can occur when transactions lock rows in multiple tables (through statements such as UPDATE or SELECT ... FOR UPDATE), but in the opposite order. A deadlock can also occur when such statements lock ranges of index records and gaps, with each transaction acquiring some locks but not others due to a timing issue. For a deadlock example, see [Section 14.7.5.1, "An InnoDB Deadlock](#page-82-0) [Example"](#page-82-0).

To reduce the possibility of deadlocks, use transactions rather than LOCK TABLES statements; keep transactions that insert or update data small enough that they do not stay open for long periods

of time; when different transactions update multiple tables or large ranges of rows, use the same order of operations (such as SELECT ... FOR UPDATE) in each transaction; create indexes on the columns used in SELECT ... FOR UPDATE and UPDATE ... WHERE statements. The possibility of deadlocks is not affected by the isolation level, because the isolation level changes the behavior of read operations, while deadlocks occur because of write operations. For more information about avoiding and recovering from deadlock conditions, see [Section 14.7.5.3, "How to Minimize and Handle](#page-83-1) [Deadlocks"](#page-83-1).

When deadlock detection is enabled (the default) and a deadlock does occur, InnoDB detects the condition and rolls back one of the transactions (the victim). If deadlock detection is disabled using the innodb\_deadlock\_detect variable, InnoDB relies on the innodb\_lock\_wait\_timeout setting to roll back transactions in case of a deadlock. Thus, even if your application logic is correct, you must still handle the case where a transaction must be retried. To view the last deadlock in an InnoDB user transaction, use SHOW ENGINE INNODB STATUS. If frequent deadlocks highlight a problem with transaction structure or application error handling, enable innodb\_print\_all\_deadlocks to print information about all deadlocks to the mysqld error log. For more information about how deadlocks are automatically detected and handled, see [Section 14.7.5.2, "Deadlock Detection".](#page-83-0)

## <span id="page-82-0"></span>**14.7.5.1 An InnoDB Deadlock Example**

The following example illustrates how an error can occur when a lock request causes a deadlock. The example involves two clients, A and B.

First, client A creates a table containing one row, and then begins a transaction. Within the transaction, A obtains an S lock on the row by selecting it in share mode:

```
mysql> CREATE TABLE t (i INT) ENGINE = InnoDB;
Query OK, 0 rows affected (1.07 sec)
mysql> INSERT INTO t (i) VALUES(1);
Query OK, 1 row affected (0.09 sec)
mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM t WHERE i = 1 LOCK IN SHARE MODE;
+------+
| i |
+------+
| 1 |
+------+
```

Next, client B begins a transaction and attempts to delete the row from the table:

```
mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)
mysql> DELETE FROM t WHERE i = 1;
```

The delete operation requires an X lock. The lock cannot be granted because it is incompatible with the S lock that client A holds, so the request goes on the queue of lock requests for the row and client B blocks.

Finally, client A also attempts to delete the row from the table:

```
mysql> DELETE FROM t WHERE i = 1;
```

Deadlock occurs here because client A needs an X lock to delete the row. However, that lock request cannot be granted because client B already has a request for an X lock and is waiting for client A to release its S lock. Nor can the S lock held by A be upgraded to an X lock because of the prior request by B for an X lock. As a result, InnoDB generates an error for one of the clients and releases its locks. The client returns this error:

```
ERROR 1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```

At that point, the lock request for the other client can be granted and it deletes the row from the table.

# <span id="page-83-0"></span>**14.7.5.2 Deadlock Detection**

When deadlock detection is enabled (the default), InnoDB automatically detects transaction deadlocks and rolls back a transaction or transactions to break the deadlock. InnoDB tries to pick small transactions to roll back, where the size of a transaction is determined by the number of rows inserted, updated, or deleted.

InnoDB is aware of table locks if innodb\_table\_locks = 1 (the default) and autocommit = 0, and the MySQL layer above it knows about row-level locks. Otherwise, InnoDB cannot detect deadlocks where a table lock set by a MySQL LOCK TABLES statement or a lock set by a storage engine other than InnoDB is involved. Resolve these situations by setting the value of the innodb\_lock\_wait\_timeout system variable.

If the LATEST DETECTED DEADLOCK section of InnoDB Monitor output includes a message stating, "TOO DEEP OR LONG SEARCH IN THE LOCK TABLE WAITS-FOR GRAPH, WE WILL ROLL BACK FOLLOWING TRANSACTION," this indicates that the number of transactions on the wait-for list has reached a limit of 200. A wait-for list that exceeds 200 transactions is treated as a deadlock and the transaction attempting to check the wait-for list is rolled back. The same error may also occur if the locking thread must look at more than 1,000,000 locks owned by transactions on the wait-for list.

For techniques to organize database operations to avoid deadlocks, see [Section 14.7.5, "Deadlocks in](#page-81-1) [InnoDB".](#page-81-1)

### **Disabling Deadlock Detection**

On high concurrency systems, deadlock detection can cause a slowdown when numerous threads wait for the same lock. At times, it may be more efficient to disable deadlock detection and rely on the innodb\_lock\_wait\_timeout setting for transaction rollback when a deadlock occurs. Deadlock detection can be disabled using the innodb\_deadlock\_detect variable.

# <span id="page-83-1"></span>**14.7.5.3 How to Minimize and Handle Deadlocks**

This section builds on the conceptual information about deadlocks in [Section 14.7.5.2, "Deadlock](#page-83-0) [Detection".](#page-83-0) It explains how to organize database operations to minimize deadlocks and the subsequent error handling required in applications.

Deadlocks are a classic problem in transactional databases, but they are not dangerous unless they are so frequent that you cannot run certain transactions at all. Normally, you must write your applications so that they are always prepared to re-issue a transaction if it gets rolled back because of a deadlock.

InnoDB uses automatic row-level locking. You can get deadlocks even in the case of transactions that just insert or delete a single row. That is because these operations are not really "atomic"; they automatically set locks on the (possibly several) index records of the row inserted or deleted.

You can cope with deadlocks and reduce the likelihood of their occurrence with the following techniques:

- At any time, issue SHOW ENGINE INNODB STATUS to determine the cause of the most recent deadlock. That can help you to tune your application to avoid deadlocks.
- If frequent deadlock warnings cause concern, collect more extensive debugging information by enabling the innodb\_print\_all\_deadlocks variable. Information about each deadlock, not just the latest one, is recorded in the MySQL error log. Disable this option when you are finished debugging.
- Always be prepared to re-issue a transaction if it fails due to deadlock. Deadlocks are not dangerous. Just try again.
- Keep transactions small and short in duration to make them less prone to collision.

- Commit transactions immediately after making a set of related changes to make them less prone to collision. In particular, do not leave an interactive mysql session open for a long time with an uncommitted transaction.
- If you use locking reads (SELECT ... FOR UPDATE or SELECT ... LOCK IN SHARE MODE), try using a lower isolation level such as [READ COMMITTED](#page-71-0).
- When modifying multiple tables within a transaction, or different sets of rows in the same table, do those operations in a consistent order each time. Then transactions form well-defined queues and do not deadlock. For example, organize database operations into functions within your application, or call stored routines, rather than coding multiple similar sequences of INSERT, UPDATE, and DELETE statements in different places.
- Add well-chosen indexes to your tables so that your queries scan fewer index records and set fewer locks. Use EXPLAIN SELECT to determine which indexes the MySQL server regards as the most appropriate for your queries.
- Use less locking. If you can afford to permit a SELECT to return data from an old snapshot, do not add a FOR UPDATE or LOCK IN SHARE MODE clause to it. Using the [READ COMMITTED](#page-71-0) isolation level is good here, because each consistent read within the same transaction reads from its own fresh snapshot.
- If nothing else helps, serialize your transactions with table-level locks. The correct way to use LOCK TABLES with transactional tables, such as InnoDB tables, is to begin a transaction with SET autocommit = 0 (not START TRANSACTION) followed by LOCK TABLES, and to not call UNLOCK TABLES until you commit the transaction explicitly. For example, if you need to write to table t1 and read from table t2, you can do this:

```
SET autocommit=0;
LOCK TABLES t1 WRITE, t2 READ, ...;
... do something with tables t1 and t2 here ...
COMMIT;
UNLOCK TABLES;
```

Table-level locks prevent concurrent updates to the table, avoiding deadlocks at the expense of less responsiveness for a busy system.

• Another way to serialize transactions is to create an auxiliary "semaphore" table that contains just a single row. Have each transaction update that row before accessing other tables. In that way, all transactions happen in a serial fashion. Note that the InnoDB instant deadlock detection algorithm also works in this case, because the serializing lock is a row-level lock. With MySQL table-level locks, the timeout method must be used to resolve deadlocks.

# <span id="page-84-0"></span>**14.8 InnoDB Configuration**

This section provides configuration information and procedures for InnoDB initialization, startup, and various components and features of the InnoDB storage engine. For information about optimizing database operations for InnoDB tables, see Section 8.5, "Optimizing for InnoDB Tables".

# <span id="page-84-1"></span>**14.8.1 InnoDB Startup Configuration**

The first decisions to make about InnoDB configuration involve the configuration of data files, log files, page size, and memory buffers, which should be configured before initializing InnoDB. Modifying the configuration after InnoDB is initialized may involve non-trivial procedures.

This section provides information about specifying InnoDB settings in a configuration file, viewing InnoDB initialization information, and important storage considerations.

- [Specifying Options in a MySQL Configuration File](#page-85-0)
- [Viewing InnoDB Initialization Information](#page-85-1)

- [Important Storage Considerations](#page-85-2)
- [System Tablespace Data File Configuration](#page-86-0)
- [Redo Log File Configuration](#page-87-0)
- [Undo Tablespace Configuration](#page-88-0)
- [Temporary Tablespace Configuration](#page-88-1)
- [Page Size Configuration](#page-89-1)
- [Memory Configuration](#page-89-0)

# <span id="page-85-0"></span>**Specifying Options in a MySQL Configuration File**

Because MySQL uses data file, log file, and page size settings to initialize InnoDB, it is recommended that you define these settings in an option file that MySQL reads at startup, prior to initializing InnoDB. Normally, InnoDB is initialized when the MySQL server is started for the first time.

You can place InnoDB settings in the [mysqld] group of any option file that your server reads when it starts. The locations of MySQL option files are described in Section 4.2.2.2, "Using Option Files".

To make sure that mysqld reads options only from a specific file, use the --defaults-file option as the first option on the command line when starting the server:

mysqld --defaults-file=path\_to\_option\_file

# <span id="page-85-1"></span>**Viewing InnoDB Initialization Information**

To view InnoDB initialization information during startup, start mysqld from a command prompt, which prints initialization information to the console.

For example, on Windows, if mysqld is located in C:\Program Files\MySQL\MySQL Server 5.7\bin, start the MySQL server like this:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld" --console
```

On Unix-like systems, mysqld is located in the bin directory of your MySQL installation:

```
$> bin/mysqld --user=mysql &
```

If you do not send server output to the console, check the error log after startup to see the initialization information InnoDB printed during the startup process.

For information about starting MySQL using other methods, see Section 2.9.5, "Starting and Stopping MySQL Automatically".

![](_page_85_Picture_21.jpeg)

#### **Note**

InnoDB does not open all user tables and associated data files at startup. However, InnoDB does check for the existence of tablespace files referenced in the data dictionary. If a tablespace file is not found, InnoDB logs an error and continues the startup sequence. Tablespace files referenced in the redo log may be opened during crash recovery for redo application.

## <span id="page-85-2"></span>**Important Storage Considerations**

Review the following storage-related considerations before proceeding with your startup configuration.

• In some cases, you can improve database performance by placing data and log files on separate physical disks. You can also use raw disk partitions (raw devices) for InnoDB data files, which may speed up I/O. See [Using Raw Disk Partitions for the System Tablespace](#page-50-0).

• InnoDB is a transaction-safe (ACID compliant) storage engine with commit, rollback, and crashrecovery capabilities to protect user data. **However, it cannot do so** if the underlying operating system or hardware does not work as advertised. Many operating systems or disk subsystems may delay or reorder write operations to improve performance. On some operating systems, the very fsync() system call that should wait until all unwritten data for a file has been flushed might actually return before the data has been flushed to stable storage. Because of this, an operating system crash or a power outage may destroy recently committed data, or in the worst case, even corrupt the database because write operation have been reordered. If data integrity is important to you, perform "pull-the-plug" tests before using anything in production. On macOS, InnoDB uses a special fcntl() file flush method. Under Linux, it is advisable to **disable the write-back cache**.

On ATA/SATA disk drives, a command such hdparm -W0 /dev/hda may work to disable the write-back cache. **Beware that some drives or disk controllers may be unable to disable the write-back cache.**

- With regard to InnoDB recovery capabilities that protect user data, InnoDB uses a file flush technique involving a structure called the doublewrite buffer, which is enabled by default (innodb\_doublewrite=ON). The doublewrite buffer adds safety to recovery following an unexpected exit or power outage, and improves performance on most varieties of Unix by reducing the need for fsync() operations. It is recommended that the innodb\_doublewrite option remains enabled if you are concerned with data integrity or possible failures. For information about the doublewrite buffer, see [Section 14.12.1, "InnoDB Disk I/O"](#page-152-1).
- Before using NFS with InnoDB, review potential issues outlined in Using NFS with MySQL.
- Running MySQL server on a 4K sector hard drive on Windows is not supported with innodb\_flush\_method=async\_unbuffered, which is the default setting. The workaround is to use innodb\_flush\_method=normal.

# <span id="page-86-0"></span>**System Tablespace Data File Configuration**

The innodb\_data\_file\_path option defines the name, size, and attributes of InnoDB system tablespace data files. If you do not configure this option prior to initializing the MySQL server, the default behavior is to create a single auto-extending data file, slightly larger than 12MB, named ibdata1:

```
mysql> SHOW VARIABLES LIKE 'innodb_data_file_path';
+-----------------------+------------------------+
| Variable_name | Value |
+-----------------------+------------------------+
| innodb_data_file_path | ibdata1:12M:autoextend |
+-----------------------+------------------------+
```

The full data file specification syntax includes the file name, file size, autoextend attribute, and max attribute:

```
file_name:file_size[:autoextend[:max:max_file_size]]
```

File sizes are specified in kilobytes, megabytes, or gigabytes by appending K, M or G to the size value. If specifying the data file size in kilobytes, do so in multiples of 1024. Otherwise, kilobyte values are rounded to nearest megabyte (MB) boundary. The sum of file sizes must be, at a minimum, slightly larger than 12MB.

You can specify more than one data file using a semicolon-separated list. For example:

```
[mysqld]
innodb_data_file_path=ibdata1:50M;ibdata2:50M:autoextend
```

The autoextend and max attributes can be used only for the data file that is specified last.

When the autoextend attribute is specified, the data file automatically increases in size by 64MB increments as space is required. The [innodb\\_autoextend\\_increment](#page-191-1) variable controls the increment size.

To specify a maximum size for an auto-extending data file, use the max attribute following the autoextend attribute. Use the max attribute only in cases where constraining disk usage is of critical importance. The following configuration permits ibdata1 to grow to a limit of 500MB:

```
[mysqld]
innodb_data_file_path=ibdata1:12M:autoextend:max:500M
```

A minimum file size is enforced for the first system tablespace data file to ensure that there is enough space for doublewrite buffer pages. The following table shows minimum file sizes for each InnoDB page size. The default InnoDB page size is 16384 (16KB).

| Page Size (innodb_page_size) | Minimum File Size |
|------------------------------|-------------------|
| 16384 (16KB) or less         | 3MB               |
| 32768 (32KB)                 | 6MB               |
| 65536 (64KB)                 | 12MB              |

If your disk becomes full, you can add a data file on another disk. For instructions, see [Resizing the](#page-48-2) [System Tablespace.](#page-48-2)

The size limit for individual files is determined by your operating system. You can set the file size to more than 4GB on operating systems that support large files. You can also use raw disk partitions as data files. See [Using Raw Disk Partitions for the System Tablespace.](#page-50-0)

InnoDB is not aware of the file system maximum file size, so be cautious on file systems where the maximum file size is a small value such as 2GB.

System tablespace files are created in the data directory by default (datadir). To specify an alternate location, use the innodb\_data\_home\_dir option. For example, to create a system tablespace data file in a directory named myibdata, use this configuration:

```
[mysqld]
innodb_data_home_dir = /myibdata/
innodb_data_file_path=ibdata1:50M:autoextend
```

A trailing slash is required when specifying a value for innodb\_data\_home\_dir. InnoDB does not create directories, so ensure that the specified directory exists before you start the server. Also, ensure sure that the MySQL server has the proper access rights to create files in the directory.

InnoDB forms the directory path for each data file by textually concatenating the value of innodb\_data\_home\_dir to the data file name. If innodb\_data\_home\_dir is not defined, the default value is "./", which is the data directory. (The MySQL server changes its current working directory to the data directory when it begins executing.)

If you specify innodb\_data\_home\_dir as an empty string, you can specify absolute paths for data files listed in the innodb\_data\_file\_path value. The following configuration is equivalent to the preceding one:

```
[mysqld]
innodb_data_home_dir =
innodb_data_file_path=/myibdata/ibdata1:50M:autoextend
```

## <span id="page-87-0"></span>**Redo Log File Configuration**

InnoDB creates two 5MB redo log files named ib\_logfile0 and ib\_logfile1 in the data directory by default.

The following options can be used to modify the default configuration:

• innodb\_log\_group\_home\_dir defines directory path to the InnoDB log files. If this option is not configured, InnoDB log files are created in the MySQL data directory (datadir).

You might use this option to place InnoDB log files in a different physical storage location than InnoDB data files to avoid potential I/O resource conflicts. For example:

[mysqld] innodb\_log\_group\_home\_dir = /dr3/iblogs

![](_page_88_Picture_3.jpeg)

#### **Note**

InnoDB does not create directories, so make sure that the log directory exists before you start the server. Use the Unix or DOS mkdir command to create any necessary directories.

Make sure that the MySQL server has the proper access rights to create files in the log directory. More generally, the server must have access rights in any directory where it needs to create log files.

- innodb\_log\_files\_in\_group defines the number of log files in the log group. The default and recommended value is 2.
- innodb\_log\_file\_size defines the size in bytes of each log file in the log group. The combined log file size (innodb\_log\_file\_size \* innodb\_log\_files\_in\_group) cannot exceed the maximum value, which is slightly less than 512GB. A pair of 255 GB log files, for example, approaches the limit but does not exceed it. The default log file size is 48MB. Generally, the combined size of the log files should be large enough that the server can smooth out peaks and troughs in workload activity, which often means that there is enough redo log space to handle more than an hour of write activity. A larger log file size means less checkpoint flush activity in the buffer pool, which reduces disk I/O. For additional information, see Section 8.5.4, "Optimizing InnoDB Redo Logging".

## <span id="page-88-0"></span>**Undo Tablespace Configuration**

Undo logs are part of the system tablespace by default. However, you can choose to store undo logs in one or more separate undo tablespaces, typically on a different storage device.

The innodb\_undo\_directory configuration option defines the path where InnoDB creates separate tablespaces for the undo logs. This option is typically used in conjunction with the innodb\_rollback\_segments and innodb\_undo\_tablespaces options, which determine the disk layout of the undo logs outside the system tablespace.

![](_page_88_Picture_12.jpeg)

#### **Note**

innodb\_undo\_tablespaces is deprecated; expect it to be removed in a future release.

For more information, see [Section 14.6.3.4, "Undo Tablespaces"](#page-58-0).

## <span id="page-88-1"></span>**Temporary Tablespace Configuration**

A single auto-extending temporary tablespace data file named ibtmp1 is created in the innodb\_data\_home\_dir directory by default. The initial file size is slightly larger than 12MB. The default temporary tablespace data file configuration can be modified at startup using the innodb\_temp\_data\_file\_path configuration option.

The innodb\_temp\_data\_file\_path option specifies the path, file name, and file size for temporary tablespace data files. The full directory path is formed by concatenating innodb\_data\_home\_dir to the path specified by innodb\_temp\_data\_file\_path. File size is specified in KB, MB, or GB (1024MB) by appending K, M, or G to the size value. The file size or combined file size must be slightly larger than 12MB.

The innodb\_data\_home\_dir default value is the MySQL data directory (datadir).

An autoextending temporary tablespace data file can become large in environments that use large temporary tables or that use temporary tables extensively. A large data file can also result from long running queries that use temporary tables. To prevent the temporary data file from becoming too large, configure the innodb\_temp\_data\_file\_path option to specify a maximum data file size. For more information see [Managing Temporary Tablespace Data File Size.](#page-62-0)

## <span id="page-89-1"></span>**Page Size Configuration**

The innodb\_page\_size option specifies the page size for all InnoDB tablespaces in a MySQL instance. This value is set when the instance is created and remains constant afterward. Valid values are 64KB, 32KB, 16KB (the default), 8KB, and 4KB. Alternatively, you can specify page size in bytes (65536, 32768, 16384, 8192, 4096).

The default 16KB page size is appropriate for a wide range of workloads, particularly for queries involving table scans and DML operations involving bulk updates. Smaller page sizes might be more efficient for OLTP workloads involving many small writes, where contention can be an issue when a single page contains many rows. Smaller pages can also be more efficient for SSD storage devices, which typically use small block sizes. Keeping the InnoDB page size close to the storage device block size minimizes the amount of unchanged data that is rewritten to disk.

![](_page_89_Picture_5.jpeg)

#### **Important**

innodb\_page\_size can be set only when initializing the data directory. See the description of this variable for more information.

# <span id="page-89-0"></span>**Memory Configuration**

MySQL allocates memory to various caches and buffers to improve performance of database operations. When allocating memory for InnoDB, always consider memory required by the operating system, memory allocated to other applications, and memory allocated for other MySQL buffers and caches. For example, if you use MyISAM tables, consider the amount of memory allocated for the key buffer (key\_buffer\_size). For an overview of MySQL buffers and caches, see Section 8.12.4.1, "How MySQL Uses Memory".

Buffers specific to InnoDB are configured using the following parameters:

• [innodb\\_buffer\\_pool\\_size](#page-196-0) defines size of the buffer pool, which is the memory area that holds cached data for InnoDB tables, indexes, and other auxiliary buffers. The size of the buffer pool is important for system performance, and it is typically recommended that [innodb\\_buffer\\_pool\\_size](#page-196-0) is configured to 50 to 75 percent of system memory. The default buffer pool size is 128MB. For additional guidance, see Section 8.12.4.1, "How MySQL Uses Memory". For information about how to configure InnoDB buffer pool size, see [Section 14.8.3.1,](#page-91-1) ["Configuring InnoDB Buffer Pool Size"](#page-91-1). Buffer pool size can be configured at startup or dynamically.

On systems with a large amount of memory, you can improve concurrency by dividing the buffer pool into multiple buffer pool instances. The number of buffer pool instances is controlled by the by [innodb\\_buffer\\_pool\\_instances](#page-194-0) option. By default, InnoDB creates one buffer pool instance. The number of buffer pool instances can be configured at startup. For more information, see [Section 14.8.3.2, "Configuring Multiple Buffer Pool Instances".](#page-96-1)

• innodb\_log\_buffer\_size defines the size of the buffer that InnoDB uses to write to the log files on disk. The default size is 16MB. A large log buffer enables large transactions to run without writing the log to disk before the transactions commit. If you have transactions that update, insert, or delete many rows, you might consider increasing the size of the log buffer to save disk I/O. innodb\_log\_buffer\_size can be configured at startup. For related information, see Section 8.5.4, "Optimizing InnoDB Redo Logging".

![](_page_89_Picture_14.jpeg)

#### **Warning**

On 32-bit GNU/Linux x86, if memory usage is set too high, glibc may permit the process heap to grow over the thread stacks, causing a server failure. It is a risk if the memory allocated to the mysqld process for global and per-thread buffers and caches is close to or exceeds 2GB.

A formula similar to the following that calculates global and per-thread memory allocation for MySQL can be used to estimate MySQL memory usage. You may need to modify the formula to account for buffers and caches in your MySQL version and configuration. For an overview of MySQL buffers and caches, see Section 8.12.4.1, "How MySQL Uses Memory".

```
innodb_buffer_pool_size
+ key_buffer_size
+ max_connections*(sort_buffer_size+read_buffer_size+binlog_cache_size)
+ max_connections*2MB
```

Each thread uses a stack (often 2MB, but only 256KB in MySQL binaries provided by Oracle Corporation.) and in the worst case also uses sort\_buffer\_size + read\_buffer\_size additional memory.

On Linux, if the kernel is enabled for large page support, InnoDB can use large pages to allocate memory for its buffer pool. See Section 8.12.4.3, "Enabling Large Page Support".

# <span id="page-90-0"></span>**14.8.2 Configuring InnoDB for Read-Only Operation**

You can query InnoDB tables where the MySQL data directory is on read-only media by enabling the --innodb-read-only configuration option at server startup.

## **How to Enable**

To prepare an instance for read-only operation, make sure all the necessary information is flushed to the data files before storing it on the read-only medium. Run the server with change buffering disabled ([innodb\\_change\\_buffering=0](#page-197-0)) and do a slow shutdown.

To enable read-only mode for an entire MySQL instance, specify the following configuration options at server startup:

- --innodb-read-only=1
- If the instance is on read-only media such as a DVD or CD, or the /var directory is not writeable by all: --pid-file=path\_on\_writeable\_media and --event-scheduler=disabled
- --innodb-temp-data-file-path. This option specifies the path, file name, and file size for InnoDB temporary tablespace data files. The default setting is ibtmp1:12M:autoextend, which creates the ibtmp1 temporary tablespace data file in the data directory. To prepare an instance for read-only operation, set innodb\_temp\_data\_file\_path to a location outside of the data directory. The path must be relative to the data directory. For example:

```
--innodb-temp-data-file-path=../../../tmp/ibtmp1:12M:autoextend
```

## **Usage Scenarios**

This mode of operation is appropriate in situations such as:

- Distributing a MySQL application, or a set of MySQL data, on a read-only storage medium such as a DVD or CD.
- Multiple MySQL instances querying the same data directory simultaneously, typically in a data warehousing configuration. You might use this technique to avoid bottlenecks that can occur with a heavily loaded MySQL instance, or you might use different configuration options for the various instances to tune each one for particular kinds of queries.
- Querying data that has been put into a read-only state for security or data integrity reasons, such as archived backup data.

![](_page_91_Picture_1.jpeg)

#### **Note**

This feature is mainly intended for flexibility in distribution and deployment, rather than raw performance based on the read-only aspect. See Section 8.5.3, "Optimizing InnoDB Read-Only Transactions" for ways to tune the performance of read-only queries, which do not require making the entire server read-only.

# **How It Works**

When the server is run in read-only mode through the --innodb-read-only option, certain InnoDB features and components are reduced or turned off entirely:

- No change buffering is done, in particular no merges from the change buffer. To make sure the change buffer is empty when you prepare the instance for read-only operation, disable change buffering ([innodb\\_change\\_buffering=0](#page-197-0)) and do a slow shutdown first.
- There is no crash recovery phase at startup. The instance must have performed a slow shutdown before being put into the read-only state.
- Because the redo log is not used in read-only operation, you can set innodb\_log\_file\_size to the smallest size possible (1 MB) before making the instance read-only.
- Most background threads are turned off. I/O read threads remain, as well as I/O write threads and a page cleaner thread for writes to temporary files, which are permitted in read-only mode.
- Information about deadlocks, monitor output, and so on is not written to temporary files. As a consequence, SHOW ENGINE INNODB STATUS does not produce any output.
- If the MySQL server is started with --innodb-read-only but the data directory is still on writeable media, the root user can still perform DCL operations such as GRANT and REVOKE.
- Changes to configuration option settings that would normally change the behavior of write operations, have no effect when the server is in read-only mode.
- The MVCC processing to enforce isolation levels is turned off. All queries read the latest version of a record, because update and deletes are not possible.
- The undo log is not used. Disable any settings for the innodb\_undo\_tablespaces and innodb\_undo\_directory configuration options.

# <span id="page-91-0"></span>**14.8.3 InnoDB Buffer Pool Configuration**

This section provides configuration and tuning information for the InnoDB buffer pool.

## <span id="page-91-1"></span>**14.8.3.1 Configuring InnoDB Buffer Pool Size**

You can configure InnoDB buffer pool size offline or while the server is running. Behavior described in this section applies to both methods. For additional information about configuring buffer pool size online, see [Configuring InnoDB Buffer Pool Size Online.](#page-94-0)

When increasing or decreasing [innodb\\_buffer\\_pool\\_size](#page-196-0), the operation is performed in chunks. Chunk size is defined by the [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) configuration option, which has a default of 128M. For more information, see [Configuring InnoDB Buffer Pool Chunk Size](#page-92-0).

Buffer pool size must always be equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). If you configure [innodb\\_buffer\\_pool\\_size](#page-196-0) to a value that is not equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0), buffer pool size is automatically adjusted to a value that is equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0).

In the following example, [innodb\\_buffer\\_pool\\_size](#page-196-0) is set to 8G, and [innodb\\_buffer\\_pool\\_instances](#page-194-0) is set to 16. [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) is 128M, which is the default value.

8G is a valid [innodb\\_buffer\\_pool\\_size](#page-196-0) value because 8G is a multiple of [innodb\\_buffer\\_pool\\_instances=16](#page-194-0) \* [innodb\\_buffer\\_pool\\_chunk\\_size=128M](#page-192-0), which is 2G.

\$> **mysqld --innodb-buffer-pool-size=8G --innodb-buffer-pool-instances=16**

```
mysql> SELECT @@innodb_buffer_pool_size/1024/1024/1024;
+------------------------------------------+
| @@innodb_buffer_pool_size/1024/1024/1024 |
+------------------------------------------+
| 8.000000000000 |
+------------------------------------------+
```

In this example, [innodb\\_buffer\\_pool\\_size](#page-196-0) is set to 9G, and [innodb\\_buffer\\_pool\\_instances](#page-194-0) is set to 16. [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) is 128M, which is the default value. In this case, 9G is not a multiple of [innodb\\_buffer\\_pool\\_instances=16](#page-194-0) \* [innodb\\_buffer\\_pool\\_chunk\\_size=128M](#page-192-0), so [innodb\\_buffer\\_pool\\_size](#page-196-0) is adjusted to 10G, which is a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0).

```
$> mysqld --innodb-buffer-pool-size=9G --innodb-buffer-pool-instances=16
```

```
mysql> SELECT @@innodb_buffer_pool_size/1024/1024/1024;
+------------------------------------------+
| @@innodb_buffer_pool_size/1024/1024/1024 |
+------------------------------------------+
| 10.000000000000 |
+------------------------------------------+
```

#### <span id="page-92-0"></span>**Configuring InnoDB Buffer Pool Chunk Size**

[innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) can be increased or decreased in 1MB (1048576 byte) units but can only be modified at startup, in a command line string or in a MySQL configuration file.

#### Command line:

```
$> mysqld --innodb-buffer-pool-chunk-size=134217728
```

#### Configuration file:

```
[mysqld]
innodb_buffer_pool_chunk_size=134217728
```

The following conditions apply when altering [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0):

• If the new [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) value \* [innodb\\_buffer\\_pool\\_instances](#page-194-0) is larger than the current buffer pool size when the buffer pool is initialized, [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) is truncated to [innodb\\_buffer\\_pool\\_size](#page-196-0) / [innodb\\_buffer\\_pool\\_instances](#page-194-0).

For example, if the buffer pool is initialized with a size of 2GB (2147483648 bytes), 4 buffer pool instances, and a chunk size of 1GB (1073741824 bytes), chunk size is truncated to a value equal to [innodb\\_buffer\\_pool\\_size](#page-196-0) / [innodb\\_buffer\\_pool\\_instances](#page-194-0), as shown below:

```
$> mysqld --innodb-buffer-pool-size=2147483648 --innodb-buffer-pool-instances=4
--innodb-buffer-pool-chunk-size=1073741824;
```

```
mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
| 2147483648 |
+---------------------------+
mysql> SELECT @@innodb_buffer_pool_instances;
+--------------------------------+
| @@innodb_buffer_pool_instances |
```

```
+--------------------------------+
| 4 |
+--------------------------------+
# Chunk size was set to 1GB (1073741824 bytes) on startup but was
# truncated to innodb_buffer_pool_size / innodb_buffer_pool_instances
mysql> SELECT @@innodb_buffer_pool_chunk_size;
+---------------------------------+
| @@innodb_buffer_pool_chunk_size |
+---------------------------------+
| 536870912 |
+---------------------------------+
```

• Buffer pool size must always be equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). If you alter [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0), [innodb\\_buffer\\_pool\\_size](#page-196-0) is automatically adjusted to a value that is equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). The adjustment occurs when the buffer pool is initialized. This behavior is demonstrated in the following example:

```
# The buffer pool has a default size of 128MB (134217728 bytes)
mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
| 134217728 |
+---------------------------+
# The chunk size is also 128MB (134217728 bytes)
mysql> SELECT @@innodb_buffer_pool_chunk_size;
+---------------------------------+
| @@innodb_buffer_pool_chunk_size |
+---------------------------------+
| 134217728 |
+---------------------------------+
# There is a single buffer pool instance
mysql> SELECT @@innodb_buffer_pool_instances;
+--------------------------------+
| @@innodb_buffer_pool_instances |
+--------------------------------+
| 1 |
+--------------------------------+
# Chunk size is decreased by 1MB (1048576 bytes) at startup
# (134217728 - 1048576 = 133169152):
$> mysqld --innodb-buffer-pool-chunk-size=133169152
mysql> SELECT @@innodb_buffer_pool_chunk_size;
+---------------------------------+
| @@innodb_buffer_pool_chunk_size |
+---------------------------------+
| 133169152 |
+---------------------------------+
# Buffer pool size increases from 134217728 to 266338304
# Buffer pool size is automatically adjusted to a value that is equal to
# or a multiple of innodb_buffer_pool_chunk_size * innodb_buffer_pool_instances
mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
| 266338304 |
+---------------------------+
```

This example demonstrates the same behavior but with multiple buffer pool instances:

```
# The buffer pool has a default size of 2GB (2147483648 bytes)
mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
| 2147483648 |
+---------------------------+
# The chunk size is .5 GB (536870912 bytes)
mysql> SELECT @@innodb_buffer_pool_chunk_size;
+---------------------------------+
| @@innodb_buffer_pool_chunk_size |
+---------------------------------+
| 536870912 |
+---------------------------------+
# There are 4 buffer pool instances
mysql> SELECT @@innodb_buffer_pool_instances;
+--------------------------------+
| @@innodb_buffer_pool_instances |
+--------------------------------+
| 4 |
+--------------------------------+
# Chunk size is decreased by 1MB (1048576 bytes) at startup
# (536870912 - 1048576 = 535822336):
$> mysqld --innodb-buffer-pool-chunk-size=535822336
mysql> SELECT @@innodb_buffer_pool_chunk_size;
+---------------------------------+
| @@innodb_buffer_pool_chunk_size |
+---------------------------------+
| 535822336 |
+---------------------------------+
# Buffer pool size increases from 2147483648 to 4286578688
# Buffer pool size is automatically adjusted to a value that is equal to
# or a multiple of innodb_buffer_pool_chunk_size * innodb_buffer_pool_instances
mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
| 4286578688 |
+---------------------------+
```

Care should be taken when changing [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0), as changing this value can increase the size of the buffer pool, as shown in the examples above. Before you change [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0), calculate the effect on [innodb\\_buffer\\_pool\\_size](#page-196-0) to ensure that the resulting buffer pool size is acceptable.

![](_page_94_Picture_3.jpeg)

#### **Note**

To avoid potential performance issues, the number of chunks ([innodb\\_buffer\\_pool\\_size](#page-196-0) / [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0)) should not exceed 1000.

#### <span id="page-94-0"></span>**Configuring InnoDB Buffer Pool Size Online**

The [innodb\\_buffer\\_pool\\_size](#page-196-0) configuration option can be set dynamically using a SET statement, allowing you to resize the buffer pool without restarting the server. For example:

```
mysql> SET GLOBAL innodb_buffer_pool_size=402653184;
```

![](_page_95_Picture_1.jpeg)

#### **Note**

The buffer pool size must be equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). Changing those variable settings requires restarting the server.

Active transactions and operations performed through InnoDB APIs should be completed before resizing the buffer pool. When initiating a resizing operation, the operation does not start until all active transactions are completed. Once the resizing operation is in progress, new transactions and operations that require access to the buffer pool must wait until the resizing operation finishes. The exception to the rule is that concurrent access to the buffer pool is permitted while the buffer pool is defragmented and pages are withdrawn when buffer pool size is decreased. A drawback of allowing concurrent access is that it could result in a temporary shortage of available pages while pages are being withdrawn.

![](_page_95_Picture_5.jpeg)

#### **Note**

Nested transactions could fail if initiated after the buffer pool resizing operation begins.

# **Monitoring Online Buffer Pool Resizing Progress**

The Innodb\_buffer\_pool\_resize\_status reports buffer pool resizing progress. For example:

```
mysql> SHOW STATUS WHERE Variable_name='InnoDB_buffer_pool_resize_status';
+----------------------------------+----------------------------------+
| Variable_name | Value |
+----------------------------------+----------------------------------+
| Innodb_buffer_pool_resize_status | Resizing also other hash tables. |
+----------------------------------+----------------------------------+
```

Buffer pool resizing progress is also logged in the server error log. This example shows notes that are logged when increasing the size of the buffer pool:

```
[Note] InnoDB: Resizing buffer pool from 134217728 to 4294967296. (unit=134217728)
[Note] InnoDB: disabled adaptive hash index.
[Note] InnoDB: buffer pool 0 : 31 chunks (253952 blocks) was added.
[Note] InnoDB: buffer pool 0 : hash tables were resized.
[Note] InnoDB: Resized hash tables at lock_sys, adaptive hash index, dictionary.
[Note] InnoDB: completed to resize buffer pool from 134217728 to 4294967296.
[Note] InnoDB: re-enabled adaptive hash index.
```

This example shows notes that are logged when decreasing the size of the buffer pool:

```
[Note] InnoDB: Resizing buffer pool from 4294967296 to 134217728. (unit=134217728)
[Note] InnoDB: disabled adaptive hash index.
[Note] InnoDB: buffer pool 0 : start to withdraw the last 253952 blocks.
[Note] InnoDB: buffer pool 0 : withdrew 253952 blocks from free list. tried to relocate 0 pages.
(253952/253952)
[Note] InnoDB: buffer pool 0 : withdrawn target 253952 blocks.
[Note] InnoDB: buffer pool 0 : 31 chunks (253952 blocks) was freed.
[Note] InnoDB: buffer pool 0 : hash tables were resized.
[Note] InnoDB: Resized hash tables at lock_sys, adaptive hash index, dictionary.
[Note] InnoDB: completed to resize buffer pool from 4294967296 to 134217728.
[Note] InnoDB: re-enabled adaptive hash index.
```

#### **Online Buffer Pool Resizing Internals**

The resizing operation is performed by a background thread. When increasing the size of the buffer pool, the resizing operation:

- Adds pages in chunks (chunk size is defined by [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0))
- Converts hash tables, lists, and pointers to use new addresses in memory
- Adds new pages to the free list

While these operations are in progress, other threads are blocked from accessing the buffer pool.

When decreasing the size of the buffer pool, the resizing operation:

- Defragments the buffer pool and withdraws (frees) pages
- Removes pages in chunks (chunk size is defined by [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0))
- Converts hash tables, lists, and pointers to use new addresses in memory

Of these operations, only defragmenting the buffer pool and withdrawing pages allow other threads to access to the buffer pool concurrently.

# <span id="page-96-1"></span>**14.8.3.2 Configuring Multiple Buffer Pool Instances**

For systems with buffer pools in the multi-gigabyte range, dividing the buffer pool into separate instances can improve concurrency, by reducing contention as different threads read and write to cached pages. This feature is typically intended for systems with a buffer pool size in the multi-gigabyte range. Multiple buffer pool instances are configured using the [innodb\\_buffer\\_pool\\_instances](#page-194-0) configuration option, and you might also adjust the [innodb\\_buffer\\_pool\\_size](#page-196-0) value.

When the InnoDB buffer pool is large, many data requests can be satisfied by retrieving from memory. You might encounter bottlenecks from multiple threads trying to access the buffer pool at once. You can enable multiple buffer pools to minimize this contention. Each page that is stored in or read from the buffer pool is assigned to one of the buffer pools randomly, using a hashing function. Each buffer pool manages its own free lists, flush lists, LRUs, and all other data structures connected to a buffer pool, and is protected by its own buffer pool mutex.

To enable multiple buffer pool instances, set the innodb\_buffer\_pool\_instances configuration option to a value greater than 1 (the default) up to 64 (the maximum). This option takes effect only when you set innodb\_buffer\_pool\_size to a size of 1GB or more. The total size you specify is divided among all the buffer pools. For best efficiency, specify a combination of [innodb\\_buffer\\_pool\\_instances](#page-194-0) and [innodb\\_buffer\\_pool\\_size](#page-196-0) so that each buffer pool instance is at least 1GB.

For information about modifying InnoDB buffer pool size, see [Section 14.8.3.1, "Configuring InnoDB](#page-91-1) [Buffer Pool Size"](#page-91-1).

# <span id="page-96-0"></span>**14.8.3.3 Making the Buffer Pool Scan Resistant**

Rather than using a strict LRU algorithm, InnoDB uses a technique to minimize the amount of data that is brought into the buffer pool and never accessed again. The goal is to make sure that frequently accessed ("hot") pages remain in the buffer pool, even as read-ahead and full table scans bring in new blocks that might or might not be accessed afterward.

Newly read blocks are inserted into the middle of the LRU list. All newly read pages are inserted at a location that by default is 3/8 from the tail of the LRU list. The pages are moved to the front of the list (the most-recently used end) when they are accessed in the buffer pool for the first time. Thus, pages that are never accessed never make it to the front portion of the LRU list, and "age out" sooner than with a strict LRU approach. This arrangement divides the LRU list into two segments, where the pages downstream of the insertion point are considered "old" and are desirable victims for LRU eviction.

For an explanation of the inner workings of the InnoDB buffer pool and specifics about the LRU algorithm, see [Section 14.5.1, "Buffer Pool"](#page-9-1).

You can control the insertion point in the LRU list and choose whether InnoDB applies the same optimization to blocks brought into the buffer pool by table or index scans. The configuration parameter innodb\_old\_blocks\_pct controls the percentage of "old" blocks in the LRU list. The default value of innodb\_old\_blocks\_pct is 37, corresponding to the original fixed ratio of 3/8. The value range is 5 (new pages in the buffer pool age out very quickly) to 95 (only 5% of the buffer pool is reserved for hot pages, making the algorithm close to the familiar LRU strategy).

The optimization that keeps the buffer pool from being churned by read-ahead can avoid similar problems due to table or index scans. In these scans, a data page is typically accessed a few times in quick succession and is never touched again. The configuration parameter innodb\_old\_blocks\_time specifies the time window (in milliseconds) after the first access to a page during which it can be accessed without being moved to the front (most-recently used end) of the LRU list. The default value of innodb\_old\_blocks\_time is 1000. Increasing this value makes more and more blocks likely to age out faster from the buffer pool.

Both innodb\_old\_blocks\_pct and innodb\_old\_blocks\_time can be specified in the MySQL option file (my.cnf or my.ini) or changed at runtime with the SET GLOBAL statement. Changing the value at runtime requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges".

To help you gauge the effect of setting these parameters, the SHOW ENGINE INNODB STATUS command reports buffer pool statistics. For details, see [Monitoring the Buffer Pool Using the InnoDB](#page-11-0) [Standard Monitor.](#page-11-0)

Because the effects of these parameters can vary widely based on your hardware configuration, your data, and the details of your workload, always benchmark to verify the effectiveness before changing these settings in any performance-critical or production environment.

In mixed workloads where most of the activity is OLTP type with periodic batch reporting queries which result in large scans, setting the value of innodb\_old\_blocks\_time during the batch runs can help keep the working set of the normal workload in the buffer pool.

When scanning large tables that cannot fit entirely in the buffer pool, setting innodb\_old\_blocks\_pct to a small value keeps the data that is only read once from consuming a significant portion of the buffer pool. For example, setting innodb\_old\_blocks\_pct=5 restricts this data that is only read once to 5% of the buffer pool.

When scanning small tables that do fit into memory, there is less overhead for moving pages around within the buffer pool, so you can leave innodb\_old\_blocks\_pct at its default value, or even higher, such as innodb\_old\_blocks\_pct=50.

The effect of the innodb\_old\_blocks\_time parameter is harder to predict than the innodb\_old\_blocks\_pct parameter, is relatively small, and varies more with the workload. To arrive at an optimal value, conduct your own benchmarks if the performance improvement from adjusting innodb\_old\_blocks\_pct is not sufficient.

## <span id="page-97-0"></span>**14.8.3.4 Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)**

A read-ahead request is an I/O request to prefetch multiple pages in the buffer pool asynchronously, in anticipation that these pages are needed soon. The requests bring in all the pages in one extent. InnoDB uses two read-ahead algorithms to improve I/O performance:

**Linear** read-ahead is a technique that predicts what pages might be needed soon based on pages in the buffer pool being accessed sequentially. You control when InnoDB performs a read-ahead operation by adjusting the number of sequential page accesses required to trigger an asynchronous read request, using the configuration parameter innodb\_read\_ahead\_threshold. Before this parameter was added, InnoDB would only calculate whether to issue an asynchronous prefetch request for the entire next extent when it read the last page of the current extent.

The configuration parameter innodb\_read\_ahead\_threshold controls how sensitive InnoDB is in detecting patterns of sequential page access. If the number of pages read sequentially from an extent is greater than or equal to innodb\_read\_ahead\_threshold, InnoDB initiates an asynchronous read-ahead operation of the entire following extent. innodb\_read\_ahead\_threshold can be set to any value from 0-64. The default value is 56. The higher the value, the more strict the access pattern check. For example, if you set the value to 48, InnoDB triggers a linear read-ahead request only when 48 pages in the current extent have been accessed sequentially. If the value is 8, InnoDB triggers an asynchronous read-ahead even if as few as 8 pages in the extent are accessed sequentially. You can set the value of this parameter in the MySQL configuration file, or change it dynamically with

the SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges".

**Random** read-ahead is a technique that predicts when pages might be needed soon based on pages already in the buffer pool, regardless of the order in which those pages were read. If 13 consecutive pages from the same extent are found in the buffer pool, InnoDB asynchronously issues a request to prefetch the remaining pages of the extent. To enable this feature, set the configuration variable innodb\_random\_read\_ahead to ON.

The SHOW ENGINE INNODB STATUS command displays statistics to help you evaluate the effectiveness of the read-ahead algorithm. Statistics include counter information for the following global status variables:

- Innodb\_buffer\_pool\_read\_ahead
- Innodb\_buffer\_pool\_read\_ahead\_evicted
- Innodb\_buffer\_pool\_read\_ahead\_rnd

This information can be useful when fine-tuning the innodb\_random\_read\_ahead setting.

For more information about I/O performance, see Section 8.5.8, "Optimizing InnoDB Disk I/O" and Section 8.12.2, "Optimizing Disk I/O".

## <span id="page-98-0"></span>**14.8.3.5 Configuring Buffer Pool Flushing**

InnoDB performs certain tasks in the background, including flushing of dirty pages from the buffer pool. Dirty pages are those that have been modified but are not yet written to the data files on disk.

In MySQL 5.7, buffer pool flushing is performed by page cleaner threads. The number of page cleaner threads is controlled by the innodb\_page\_cleaners variable, which has a default value of 4. However, if the number of page cleaner threads exceeds the number of buffer pool instances, innodb\_page\_cleaners is automatically set to the same value as [innodb\\_buffer\\_pool\\_instances](#page-194-0).

Buffer pool flushing is initiated when the percentage of dirty pages reaches the low water mark value defined by the innodb\_max\_dirty\_pages\_pct\_lwm variable. The default low water mark is 0, which disables this early flushing behaviour.

The purpose of the innodb\_max\_dirty\_pages\_pct\_lwm threshold is to control the percentage dirty pages in the buffer pool and to prevent the amount of dirty pages from reaching the threshold defined by the innodb\_max\_dirty\_pages\_pct variable, which has a default value of 75. InnoDB aggressively flushes buffer pool pages if the percentage of dirty pages in the buffer pool reaches the innodb\_max\_dirty\_pages\_pct threshold.

When configuring innodb\_max\_dirty\_pages\_pct\_lwm, the value should always be lower than the innodb\_max\_dirty\_pages\_pct value.

Additional variables permit fine-tuning of buffer pool flushing behavior:

- The innodb\_flush\_neighbors variable defines whether flushing a page from the buffer pool also flushes other dirty pages in the same extent.
  - A setting of 0 disables innodb\_flush\_neighbors. Dirty pages in the same extent are not flushed.
  - The default setting of 1 flushes contiguous dirty pages in the same extent.
  - A setting of 2 flushes dirty pages in the same extent.

When table data is stored on a traditional HDD storage device, flushing neighbor pages in one operation reduces I/O overhead (primarily for disk seek operations) compared to flushing individual pages at different times. For table data stored on SSD, seek time is not a significant factor and you can disable this setting to spread out write operations.

• The innodb\_lru\_scan\_depth variable specifies, per buffer pool instance, how far down the buffer pool LRU list the page cleaner thread scans looking for dirty pages to flush. This is a background operation performed by a page cleaner thread once per second.

A setting smaller than the default is generally suitable for most workloads. A value that is significantly higher than necessary may impact performance. Only consider increasing the value if you have spare I/O capacity under a typical workload. Conversely, if a write-intensive workload saturates your I/O capacity, decrease the value, especially in the case of a large buffer pool.

When tuning innodb\_lru\_scan\_depth, start with a low value and configure the setting upward with the goal of rarely seeing zero free pages. Also, consider adjusting innodb\_lru\_scan\_depth when changing the number of buffer pool instances, since innodb\_lru\_scan\_depth \* [innodb\\_buffer\\_pool\\_instances](#page-194-0) defines the amount of work performed by the page cleaner thread each second.

The innodb\_flush\_neighbors and innodb\_lru\_scan\_depth variables are primarily intended for write-intensive workloads. With heavy DML activity, flushing can fall behind if it is not aggressive enough, or disk writes can saturate I/O capacity if flushing is too aggressive. The ideal settings depend on your workload, data access patterns, and storage configuration (for example, whether data is stored on HDD or SSD devices).

# **Adaptive Flushing**

InnoDB uses an adaptive flushing algorithm to dynamically adjust the rate of flushing based on the speed of redo log generation and the current rate of flushing. The intent is to smooth overall performance by ensuring that flushing activity keeps pace with the current workload. Automatically adjusting the flushing rate helps avoid sudden dips in throughput that can occur when bursts of I/O activity due to buffer pool flushing affects the I/O capacity available for ordinary read and write activity.

Sharp checkpoints, which are typically associated with write-intensive workloads that generate a lot of redo entries, can cause a sudden change in throughput, for example. A sharp checkpoint occurs when InnoDB wants to reuse a portion of a log file. Before doing so, all dirty pages with redo entries in that portion of the log file must be flushed. If log files become full, a sharp checkpoint occurs, causing a temporary reduction in throughput. This scenario can occur even if innodb\_max\_dirty\_pages\_pct threshold is not reached.

The adaptive flushing algorithm helps avoid such scenarios by tracking the number of dirty pages in the buffer pool and the rate at which redo log records are being generated. Based on this information, it decides how many dirty pages to flush from the buffer pool each second, which permits it to manage sudden changes in workload.

The [innodb\\_adaptive\\_flushing\\_lwm](#page-187-0) variable defines a low water mark for redo log capacity. When that threshold is crossed, adaptive flushing is enabled, even if the [innodb\\_adaptive\\_flushing](#page-187-1) variable is disabled.

Internal benchmarking has shown that the algorithm not only maintains throughput over time, but can also improve overall throughput significantly. However, adaptive flushing can affect the I/O pattern of a workload significantly and may not be appropriate in all cases. It gives the most benefit when the redo log is in danger of filling up. If adaptive flushing is not appropriate to the characteristics of your workload, you can disable it. Adaptive flushing controlled by the [innodb\\_adaptive\\_flushing](#page-187-1) variable, which is enabled by default.

innodb\_flushing\_avg\_loops defines the number of iterations that InnoDB keeps the previously calculated snapshot of the flushing state, controlling how quickly adaptive flushing responds to foreground workload changes. A high innodb\_flushing\_avg\_loops value means that InnoDB keeps the previously calculated snapshot longer, so adaptive flushing responds more slowly. When setting a high value it is important to ensure that redo log utilization does not reach 75% (the

hardcoded limit at which asynchronous flushing starts), and that the innodb\_max\_dirty\_pages\_pct threshold keeps the number of dirty pages to a level that is appropriate for the workload.

Systems with consistent workloads, a large log file size (innodb\_log\_file\_size), and small spikes that do not reach 75% log space utilization should use a high innodb\_flushing\_avg\_loops value to keep flushing as smooth as possible. For systems with extreme load spikes or log files that do not provide a lot of space, a smaller value allows flushing to closely track workload changes, and helps to avoid reaching 75% log space utilization.

Be aware that if flushing falls behind, the rate of buffer pool flushing can exceed the I/O capacity available to InnoDB, as defined by innodb\_io\_capacity setting. The innodb\_io\_capacity\_max value defines an upper limit on I/O capacity in such situations, so that a spike in I/O activity does not consume the entire I/O capacity of the server.

The innodb\_io\_capacity setting is applicable to all buffer pool instances. When dirty pages are flushed, I/O capacity is divided equally among buffer pool instances.

# <span id="page-100-0"></span>**14.8.3.6 Saving and Restoring the Buffer Pool State**

To reduce the warmup period after restarting the server, InnoDB saves a percentage of the most recently used pages for each buffer pool at server shutdown and restores these pages at server startup. The percentage of recently used pages that is stored is defined by the [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) configuration option.

After restarting a busy server, there is typically a warmup period with steadily increasing throughput, as disk pages that were in the buffer pool are brought back into memory (as the same data is queried, updated, and so on). The ability to restore the buffer pool at startup shortens the warmup period by reloading disk pages that were in the buffer pool before the restart rather than waiting for DML operations to access corresponding rows. Also, I/O requests can be performed in large batches, making the overall I/O faster. Page loading happens in the background, and does not delay database startup.

In addition to saving the buffer pool state at shutdown and restoring it at startup, you can save and restore the buffer pool state at any time, while the server is running. For example, you can save the state of the buffer pool after reaching a stable throughput under a steady workload. You could also restore the previous buffer pool state after running reports or maintenance jobs that bring data pages into the buffer pool that are only requited for those operations, or after running some other non-typical workload.

Even though a buffer pool can be many gigabytes in size, the buffer pool data that InnoDB saves to disk is tiny by comparison. Only tablespace IDs and page IDs necessary to locate the appropriate pages are saved to disk. This information is derived from the INNODB\_BUFFER\_PAGE\_LRU INFORMATION\_SCHEMA table. By default, tablespace ID and page ID data is saved in a file named ib\_buffer\_pool, which is saved to the InnoDB data directory. The file name and location can be modified using the [innodb\\_buffer\\_pool\\_filename](#page-194-1) configuration parameter.

Because data is cached in and aged out of the buffer pool as it is with regular database operations, there is no problem if the disk pages are recently updated, or if a DML operation involves data that has not yet been loaded. The loading mechanism skips requested pages that no longer exist.

The underlying mechanism involves a background thread that is dispatched to perform the dump and load operations.

Disk pages from compressed tables are loaded into the buffer pool in their compressed form. Pages are uncompressed as usual when page contents are accessed during DML operations. Because uncompressing pages is a CPU-intensive process, it is more efficient for concurrency to perform the operation in a connection thread rather than in the single thread that performs the buffer pool restore operation.

Operations related to saving and restoring the buffer pool state are described in the following topics:

• [Configuring the Dump Percentage for Buffer Pool Pages](#page-101-0)

- [Saving the Buffer Pool State at Shutdown and Restoring it at Startup](#page-101-1)
- [Saving and Restoring the Buffer Pool State Online](#page-101-2)
- [Displaying Buffer Pool Dump Progress](#page-101-3)
- [Displaying Buffer Pool Load Progress](#page-102-0)
- [Aborting a Buffer Pool Load Operation](#page-102-1)
- [Monitoring Buffer Pool Load Progress Using Performance Schema](#page-102-2)

### <span id="page-101-0"></span>**Configuring the Dump Percentage for Buffer Pool Pages**

Before dumping pages from the buffer pool, you can configure the percentage of most-recentlyused buffer pool pages that you want to dump by setting the [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) option. If you plan to dump buffer pool pages while the server is running, you can configure the option dynamically:

```
SET GLOBAL innodb_buffer_pool_dump_pct=40;
```

If you plan to dump buffer pool pages at server shutdown, set [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) in your configuration file.

```
[mysqld]
innodb_buffer_pool_dump_pct=40
```

The [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) default value was changed from 100 (dump all pages) to 25 (dump 25% of most-recently-used pages) in MySQL 5.7 when [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1) and [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0) were enabled by default.

### <span id="page-101-1"></span>**Saving the Buffer Pool State at Shutdown and Restoring it at Startup**

To save the state of the buffer pool at server shutdown, issue the following statement prior to shutting down the server:

```
SET GLOBAL innodb_buffer_pool_dump_at_shutdown=ON;
```

[innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1) is enabled by default.

To restore the buffer pool state at server startup, specify the --innodb-buffer-pool-load-atstartup option when starting the server:

```
mysqld --innodb-buffer-pool-load-at-startup=ON;
```

[innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0) is enabled by default.

#### <span id="page-101-2"></span>**Saving and Restoring the Buffer Pool State Online**

To save the state of the buffer pool while MySQL server is running, issue the following statement:

```
SET GLOBAL innodb_buffer_pool_dump_now=ON;
```

To restore the buffer pool state while MySQL is running, issue the following statement:

```
SET GLOBAL innodb_buffer_pool_load_now=ON;
```

### <span id="page-101-3"></span>**Displaying Buffer Pool Dump Progress**

To display progress when saving the buffer pool state to disk, issue the following statement:

```
SHOW STATUS LIKE 'Innodb_buffer_pool_dump_status';
```

If the operation has not yet started, "not started" is returned. If the operation is complete, the completion time is printed (e.g. Finished at 110505 12:18:02). If the operation is in progress, status information is provided (e.g. Dumping buffer pool 5/7, page 237/2873).

#### <span id="page-102-0"></span>**Displaying Buffer Pool Load Progress**

To display progress when loading the buffer pool, issue the following statement:

```
SHOW STATUS LIKE 'Innodb_buffer_pool_load_status';
```

If the operation has not yet started, "not started" is returned. If the operation is complete, the completion time is printed (e.g. Finished at 110505 12:23:24). If the operation is in progress, status information is provided (e.g. Loaded 123/22301 pages).

#### <span id="page-102-1"></span>**Aborting a Buffer Pool Load Operation**

To abort a buffer pool load operation, issue the following statement:

```
SET GLOBAL innodb_buffer_pool_load_abort=ON;
```

### <span id="page-102-2"></span>**Monitoring Buffer Pool Load Progress Using Performance Schema**

You can monitor buffer pool load progress using Performance Schema.

The following example demonstrates how to enable the stage/innodb/buffer pool load stage event instrument and related consumer tables to monitor buffer pool load progress.

For information about buffer pool dump and load procedures used in this example, see [Section 14.8.3.6, "Saving and Restoring the Buffer Pool State"](#page-100-0). For information about Performance Schema stage event instruments and related consumers, see Section 25.12.5, "Performance Schema Stage Event Tables".

1. Enable the stage/innodb/buffer pool load instrument:

```
mysql> UPDATE performance_schema.setup_instruments SET ENABLED = 'YES' 
 WHERE NAME LIKE 'stage/innodb/buffer%';
```

2. Enable the stage event consumer tables, which include events\_stages\_current, events\_stages\_history, and events\_stages\_history\_long.

```
mysql> UPDATE performance_schema.setup_consumers SET ENABLED = 'YES' 
 WHERE NAME LIKE '%stages%';
```

3. Dump the current buffer pool state by enabling [innodb\\_buffer\\_pool\\_dump\\_now](#page-193-1).

```
mysql> SET GLOBAL innodb_buffer_pool_dump_now=ON;
```

4. Check the buffer pool dump status to ensure that the operation has completed.

```
mysql> SHOW STATUS LIKE 'Innodb_buffer_pool_dump_status'\G
*************************** 1. row ***************************
Variable_name: Innodb_buffer_pool_dump_status
 Value: Buffer pool(s) dump completed at 150202 16:38:58
```

5. Load the buffer pool by enabling [innodb\\_buffer\\_pool\\_load\\_now](#page-196-1):

```
mysql> SET GLOBAL innodb_buffer_pool_load_now=ON;
```

6. Check the current status of the buffer pool load operation by querying the Performance Schema events\_stages\_current table. The WORK\_COMPLETED column shows the number of buffer pool pages loaded. The WORK\_ESTIMATED column provides an estimate of the remaining work, in pages.

```
mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED
 FROM performance_schema.events_stages_current;
+-------------------------------+----------------+----------------+
| EVENT_NAME | WORK_COMPLETED | WORK_ESTIMATED |
+-------------------------------+----------------+----------------+
| stage/innodb/buffer pool load | 5353 | 7167 |
```

+-------------------------------+----------------+----------------+

The events\_stages\_current table returns an empty set if the buffer pool load operation has completed. In this case, you can check the events\_stages\_history table to view data for the completed event. For example:

```
mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED 
 FROM performance_schema.events_stages_history;
+-------------------------------+----------------+----------------+
| EVENT_NAME | WORK_COMPLETED | WORK_ESTIMATED |
+-------------------------------+----------------+----------------+
| stage/innodb/buffer pool load | 7167 | 7167 |
+-------------------------------+----------------+----------------+
```

![](_page_103_Picture_4.jpeg)

#### **Note**

You can also monitor buffer pool load progress using Performance Schema when loading the buffer pool at startup using [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0). In this case, the stage/ innodb/buffer pool load instrument and related consumers must be enabled at startup. For more information, see Section 25.3, "Performance Schema Startup Configuration".

# <span id="page-103-0"></span>**14.8.4 Configuring the Memory Allocator for InnoDB**

When InnoDB was developed, the memory allocators supplied with operating systems and run-time libraries were often lacking in performance and scalability. At that time, there were no memory allocator libraries tuned for multi-core CPUs. Therefore, InnoDB implemented its own memory allocator in the mem subsystem. This allocator is guarded by a single mutex, which may become a bottleneck. InnoDB also implements a wrapper interface around the system allocator (malloc and free) that is likewise guarded by a single mutex.

Today, as multi-core systems have become more widely available, and as operating systems have matured, significant improvements have been made in the memory allocators provided with operating systems. These new memory allocators perform better and are more scalable than they were in the past. Most workloads, especially those where memory is frequently allocated and released (such as multi-table joins), benefit from using a more highly tuned memory allocator as opposed to the internal, InnoDB-specific memory allocator.

You can control whether InnoDB uses its own memory allocator or an allocator of the operating system, by setting the value of the system configuration parameter innodb\_use\_sys\_malloc in the MySQL option file (my.cnf or my.ini). If set to ON or 1 (the default), InnoDB uses the malloc and free functions of the underlying system rather than manage memory pools itself. This parameter is not dynamic, and takes effect only when the system is started. To continue to use the InnoDB memory allocator, set innodb\_use\_sys\_malloc to 0.

When the InnoDB memory allocator is disabled, InnoDB ignores the value of the parameter innodb\_additional\_mem\_pool\_size. The InnoDB memory allocator uses an additional memory pool for satisfying allocation requests without having to fall back to the system memory allocator. When the InnoDB memory allocator is disabled, all such allocation requests are fulfilled by the system memory allocator.

On Unix-like systems that use dynamic linking, replacing the memory allocator may be as easy as making the environment variable LD\_PRELOAD or LD\_LIBRARY\_PATH point to the dynamic library that implements the allocator. On other systems, some relinking may be necessary. Please refer to the documentation of the memory allocator library of your choice.

Since InnoDB cannot track all memory use when the system memory allocator is used (innodb\_use\_sys\_malloc is ON), the section "BUFFER POOL AND MEMORY" in the output of the SHOW ENGINE INNODB STATUS command only includes the buffer pool statistics in the "Total memory allocated". Any memory allocated using the mem subsystem or using ut\_malloc is excluded.

![](_page_104_Picture_1.jpeg)

#### **Note**

innodb\_use\_sys\_malloc and innodb\_additional\_mem\_pool\_size were deprecated in MySQL 5.6 and removed in MySQL 5.7.

For more information about the performance implications of InnoDB memory usage, see Section 8.10, "Buffering and Caching".

# <span id="page-104-0"></span>**14.8.5 Configuring Thread Concurrency for InnoDB**

InnoDB uses operating system threads to process requests from user transactions. (Transactions may issue many requests to InnoDB before they commit or roll back.) On modern operating systems and servers with multi-core processors, where context switching is efficient, most workloads run well without any limit on the number of concurrent threads. Scalability improvements in MySQL 5.5 and up reduce the need to limit the number of concurrently executing threads inside InnoDB.

In situations where it is helpful to minimize context switching between threads, InnoDB can use a number of techniques to limit the number of concurrently executing operating system threads (and thus the number of requests that are processed at any one time). When InnoDB receives a new request from a user session, if the number of threads concurrently executing is at a pre-defined limit, the new request sleeps for a short time before it tries again. Threads waiting for locks are not counted in the number of concurrently executing threads.

You can limit the number of concurrent threads by setting the configuration parameter innodb\_thread\_concurrency. Once the number of executing threads reaches this limit, additional threads sleep for a number of microseconds, set by the configuration parameter innodb\_thread\_sleep\_delay, before being placed into the queue.

Previously, it required experimentation to find the optimal value for innodb\_thread\_sleep\_delay, and the optimal value could change depending on the workload. In MySQL 5.6.3 and higher, you can set the configuration option [innodb\\_adaptive\\_max\\_sleep\\_delay](#page-188-2) to the highest value you would allow for innodb\_thread\_sleep\_delay, and InnoDB automatically adjusts innodb\_thread\_sleep\_delay up or down depending on the current thread-scheduling activity. This dynamic adjustment helps the thread scheduling mechanism to work smoothly during times when the system is lightly loaded and when it is operating near full capacity.

The default value for innodb\_thread\_concurrency and the implied default limit on the number of concurrent threads has been changed in various releases of MySQL and InnoDB. The default value of innodb\_thread\_concurrency is 0, so that by default there is no limit on the number of concurrently executing threads.

InnoDB causes threads to sleep only when the number of concurrent threads is limited. When there is no limit on the number of threads, all contend equally to be scheduled. That is, if innodb\_thread\_concurrency is 0, the value of innodb\_thread\_sleep\_delay is ignored.

When there is a limit on the number of threads (when innodb\_thread\_concurrency is > 0), InnoDB reduces context switching overhead by permitting multiple requests made during the execution of a single SQL statement to enter InnoDB without observing the limit set by innodb\_thread\_concurrency. Since an SQL statement (such as a join) may comprise multiple row operations within InnoDB, InnoDB assigns a specified number of "tickets" that allow a thread to be scheduled repeatedly with minimal overhead.

When a new SQL statement starts, a thread has no tickets, and it must observe innodb\_thread\_concurrency. Once the thread is entitled to enter InnoDB, it is assigned a number of tickets that it can use for subsequently entering InnoDB to perform row operations. If the tickets run out, the thread is evicted, and innodb\_thread\_concurrency is observed again which may place the thread back into the first-in/first-out queue of waiting threads. When the thread is once again entitled to enter InnoDB, tickets are assigned again. The number of tickets assigned is specified by the global option innodb\_concurrency\_tickets, which is 5000 by default. A thread that is waiting for a lock is given one ticket once the lock becomes available.

The correct values of these variables depend on your environment and workload. Try a range of different values to determine what value works for your applications. Before limiting the number of concurrently executing threads, review configuration options that may improve the performance of InnoDB on multi-core and multi-processor computers, such as [innodb\\_adaptive\\_hash\\_index](#page-188-0).

For general performance information about MySQL thread handling, see Section 5.1.11.1, "Connection Interfaces".

# <span id="page-105-0"></span>**14.8.6 Configuring the Number of Background InnoDB I/O Threads**

InnoDB uses background threads to service various types of I/O requests. You can configure the number of background threads that service read and write I/O on data pages using the innodb\_read\_io\_threads and innodb\_write\_io\_threads configuration parameters. These parameters signify the number of background threads used for read and write requests, respectively. They are effective on all supported platforms. You can set values for these parameters in the MySQL option file (my.cnf or my.ini); you cannot change values dynamically. The default value for these parameters is 4 and permissible values range from 1-64.

The purpose of these configuration options to make InnoDB more scalable on high end systems. Each background thread can handle up to 256 pending I/O requests. A major source of background I/O is read-ahead requests. InnoDB tries to balance the load of incoming requests in such way that most background threads share work equally. InnoDB also attempts to allocate read requests from the same extent to the same thread, to increase the chances of coalescing the requests. If you have a high end I/O subsystem and you see more than 64 × innodb\_read\_io\_threads pending read requests in SHOW ENGINE INNODB STATUS output, you might improve performance by increasing the value of innodb\_read\_io\_threads.

On Linux systems, InnoDB uses the asynchronous I/O subsystem by default to perform read-ahead and write requests for data file pages, which changes the way that InnoDB background threads service these types of I/O requests. For more information, see [Section 14.8.7, "Using Asynchronous I/O on](#page-105-1) [Linux"](#page-105-1).

For more information about InnoDB I/O performance, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

# <span id="page-105-1"></span>**14.8.7 Using Asynchronous I/O on Linux**

InnoDB uses the asynchronous I/O subsystem (native AIO) on Linux to perform read-ahead and write requests for data file pages. This behavior is controlled by the innodb\_use\_native\_aio configuration option, which applies to Linux systems only and is enabled by default. On other Unixlike systems, InnoDB uses synchronous I/O only. Historically, InnoDB only used asynchronous I/O on Windows systems. Using the asynchronous I/O subsystem on Linux requires the libaio library.

With synchronous I/O, query threads queue I/O requests, and InnoDB background threads retrieve the queued requests one at a time, issuing a synchronous I/O call for each. When an I/O request is completed and the I/O call returns, the InnoDB background thread that is handling the request calls an I/O completion routine and returns to process the next request. The number of requests that can be processed in parallel is n, where n is the number of InnoDB background threads. The number of InnoDB background threads is controlled by innodb\_read\_io\_threads and innodb\_write\_io\_threads. See [Section 14.8.6, "Configuring the Number of Background InnoDB I/](#page-105-0) [O Threads".](#page-105-0)

With native AIO, query threads dispatch I/O requests directly to the operating system, thereby removing the limit imposed by the number of background threads. InnoDB background threads wait for I/O events to signal completed requests. When a request is completed, a background thread calls an I/ O completion routine and resumes waiting for I/O events.

The advantage of native AIO is scalability for heavily I/O-bound systems that typically show many pending reads/writes in SHOW ENGINE INNODB STATUS\G output. The increase in parallel processing when using native AIO means that the type of I/O scheduler or properties of the disk array controller have a greater influence on I/O performance.

A potential disadvantage of native AIO for heavily I/O-bound systems is lack of control over the number of I/O write requests dispatched to the operating system at once. Too many I/O write requests dispatched to the operating system for parallel processing could, in some cases, result in I/O read starvation, depending on the amount of I/O activity and system capabilities.

If a problem with the asynchronous I/O subsystem in the OS prevents InnoDB from starting, you can start the server with innodb\_use\_native\_aio=0. This option may also be disabled automatically during startup if InnoDB detects a potential problem such as a combination of tmpdir location, tmpfs file system, and Linux kernel that does not support asynchronous I/O on tmpfs.

# <span id="page-106-0"></span>**14.8.8 Configuring InnoDB I/O Capacity**

The InnoDB master thread and other threads perform various tasks in the background, most of which are I/O related, such as flushing dirty pages from the buffer pool and writing changes from the change buffer to the appropriate secondary indexes. InnoDB attempts to perform these tasks in a way that does not adversely affect the normal working of the server. It tries to estimate the available I/O bandwidth and tune its activities to take advantage of available capacity.

The innodb\_io\_capacity variable defines the overall I/O capacity available to InnoDB. It should be set to approximately the number of I/O operations that the system can perform per second (IOPS). When innodb\_io\_capacity is set, InnoDB estimates the I/O bandwidth available for background tasks based on the set value.

You can set innodb\_io\_capacity to a value of 100 or greater. The default value is 200. Typically, values around 100 are appropriate for consumer-level storage devices, such as hard drives up to 7200 RPMs. Faster hard drives, RAID configurations, and solid state drives (SSDs) benefit from higher values.

Ideally, keep the setting as low as practical, but not so low that background activities fall behind. If the value is too high, data is removed from the buffer pool and change buffer too quickly for caching to provide a significant benefit. For busy systems capable of higher I/O rates, you can set a higher value to help the server handle the background maintenance work associated with a high rate of row changes. Generally, you can increase the value as a function of the number of drives used for InnoDB I/O. For example, you can increase the value on systems that use multiple disks or SSDs.

The default setting of 200 is generally sufficient for a lower-end SSD. For a higher-end, bus-attached SSD, consider a higher setting such as 1000, for example. For systems with individual 5400 RPM or 7200 RPM drives, you might lower the value to 100, which represents an estimated proportion of the I/ O operations per second (IOPS) available to older-generation disk drives that can perform about 100 IOPS.

Although you can specify a high value such as a million, in practice such large values have little benefit. Generally, a value higher than 20000 is not recommended unless you are certain that lower values are insufficient for your workload.

Consider write workload when tuning innodb\_io\_capacity. Systems with large write workloads are likely to benefit from a higher setting. A lower setting may be sufficient for systems with a small write workload.

The innodb\_io\_capacity setting is not a per buffer pool instance setting. Available I/O capacity is distributed equally among buffer pool instances for flushing activities.

You can set the innodb\_io\_capacity value in the MySQL option file (my.cnf or my.ini) or modify it at runtime using a SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges".

## **Ignoring I/O Capacity at Checkpoints**

The innodb\_flush\_sync variable, which is enabled by default, causes the innodb\_io\_capacity setting to be ignored during bursts of I/O activity that occur at checkpoints. To adhere to the I/O rate defined by the innodb\_io\_capacity setting, disable innodb\_flush\_sync.

You can set the innodb\_flush\_sync value in the MySQL option file (my.cnf or my.ini) or modify it at runtime using a SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges".

# **Configuring an I/O Capacity Maximum**

If flushing activity falls behind, InnoDB can flush more aggressively, at a higher rate of I/ O operations per second (IOPS) than defined by the innodb\_io\_capacity variable. The innodb\_io\_capacity\_max variable defines a maximum number of IOPS performed by InnoDB background tasks in such situations.

If you specify an innodb\_io\_capacity setting at startup but do not specify a value for innodb\_io\_capacity\_max, innodb\_io\_capacity\_max defaults to twice the value of innodb\_io\_capacity or 2000, whichever value is greater.

When configuring innodb\_io\_capacity\_max, twice the innodb\_io\_capacity is often a good starting point. The default value of 2000 is intended for workloads that use an SSD or more than one regular disk drive. A setting of 2000 is likely too high for workloads that do not use SSDs or multiple disk drives, and could allow too much flushing. For a single regular disk drive, a setting between 200 and 400 is recommended. For a high-end, bus-attached SSD, consider a higher setting such as 2500. As with the innodb\_io\_capacity setting, keep the setting as low as practical, but not so low that InnoDB cannot sufficiently extend rate of IOPS beyond the innodb\_io\_capacity setting.

Consider write workload when tuning innodb\_io\_capacity\_max. Systems with large write workloads may benefit from a higher setting. A lower setting may be sufficient for systems with a small write workload.

innodb\_io\_capacity\_max cannot be set to a value lower than the innodb\_io\_capacity value.

Setting innodb\_io\_capacity\_max to DEFAULT using a SET statement (SET GLOBAL innodb\_io\_capacity\_max=DEFAULT) sets innodb\_io\_capacity\_max to the maximum value.

The innodb\_io\_capacity\_max limit applies to all buffer pool instances. It is not a per buffer pool instance setting.

# <span id="page-107-0"></span>**14.8.9 Configuring Spin Lock Polling**

InnoDB mutexes and rw-locks are typically reserved for short intervals. On a multi-core system, it can be more efficient for a thread to continuously check if it can acquire a mutex or rw-lock for a period of time before it sleeps. If the mutex or rw-lock becomes available during this period, the thread can continue immediately, in the same time slice. However, too-frequent polling of a shared object such as a mutex or rw-lock by multiple threads can cause "cache ping pong", which results in processors invalidating portions of each other's cache. InnoDB minimizes this issue by forcing a random delay between polls to desychronize polling activity. The random delay is implemented as a spin-wait loop.

The duration of a spin-wait loop is determined by the number of PAUSE instructions that occur in the loop. That number is generated by randomly selecting an integer ranging from 0 up to but not including the innodb\_spin\_wait\_delay value, and multiplying that value by 50. For example, an integer is randomly selected from the following range for an innodb\_spin\_wait\_delay setting of 6:

```
{0,1,2,3,4,5}
```

The selected integer is multiplied by 50, resulting in one of six possible PAUSE instruction values:

```
{0,50,100,150,200,250}
```

For that set of values, 250 is the maximum number of PAUSE instructions that can occur in a spinwait loop. An innodb\_spin\_wait\_delay setting of 5 results in a set of five possible values {0,50,100,150,200}, where 200 is the maximum number of PAUSE instructions, and so on. In this way, the innodb\_spin\_wait\_delay setting controls the maximum delay between spin lock polls.

The duration of the delay loop depends on the C compiler and the target processor. In the 100MHz Pentium era, an innodb\_spin\_wait\_delay unit was calibrated to be equivalent to one microsecond. That time equivalence did not hold, but PAUSE instruction duration has remained fairly constant in terms of processor cycles relative to other CPU instructions on most processor architectures.

On a system where all processor cores share a fast cache memory, you might reduce the maximum delay or disable the busy loop altogether by setting innodb\_spin\_wait\_delay=0. On a system with multiple processor chips, the effect of cache invalidation can be more significant and you might increase the maximum delay.

The innodb\_spin\_wait\_delay variable is dynamic. It can be specified in a MySQL option file or modified at runtime using a SET GLOBAL statement. Runtime modification requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges".

# <span id="page-108-0"></span>**14.8.10 Purge Configuration**

InnoDB does not physically remove a row from the database immediately when you delete it with an SQL statement. A row and its index records are only physically removed when InnoDB discards the undo log record written for the deletion. This removal operation, which only occurs after the row is no longer required for multi-version concurrency control (MVCC) or rollback, is called a purge.

Purge runs on a periodic schedule. It parses and processes undo log pages from the history list, which is a list of undo log pages for committed transactions that is maintained by the InnoDB transaction system. Purge frees the undo log pages from the history list after processing them.

# **Configuring Purge Threads**

Purge operations are performed in the background by one or more purge threads. The number of purge threads is controlled by the innodb\_purge\_threads variable. The default value is 4. If DML action is concentrated on a single table, purge operations for the table are performed by a single purge thread. If DML action is concentrated on a few tables, keep the innodb\_purge\_threads setting low so that the threads do not contend with each other for access to the busy tables. If DML operations are spread across many tables, consider a higher innodb\_purge\_threads setting. The maximum number of purge threads is 32.

The innodb\_purge\_threads setting is the maximum number of purge threads permitted. The purge system automatically adjusts the number of purge threads that are used.

# **Configuring Purge Batch Size**

The innodb\_purge\_batch\_size variable defines the number of undo log pages that purge parses and processes in one batch from the history list. The default value is 300. In a multithreaded purge configuration, the coordinator purge thread divides innodb\_purge\_batch\_size by innodb\_purge\_threads and assigns that number of pages to each purge thread.

The purge system also frees the undo log pages that are no longer required. It does so every 128 iterations through the undo logs. In addition to defining the number of undo log pages parsed and processed in a batch, the innodb\_purge\_batch\_size variable defines the number of undo log pages that purge frees every 128 iterations through the undo logs.

The innodb\_purge\_batch\_size variable is intended for advanced performance tuning and experimentation. Most users need not change innodb\_purge\_batch\_size from its default value.

## **Configuring the Maximum Purge Lag**

The innodb\_max\_purge\_lag variable defines the desired maximum purge lag. When the purge lag exceeds the innodb\_max\_purge\_lag threshold, a delay is imposed on INSERT, UPDATE, and DELETE operations to allow time for purge operations to catch up. The default value is 0, which means there is no maximum purge lag and no delay.

The InnoDB transaction system maintains a list of transactions that have index records delete-marked by UPDATE or DELETE operations. The length of the list is the purge lag. The purge lag delay is calculated by the following formula, which results in a minimum delay of 5000 microseconds:

```
(purge lag/innodb_max_purge_lag - 0.5) * 10000
```

The delay is calculated at the beginning of a purge batch

A typical innodb\_max\_purge\_lag setting for a problematic workload might be 1000000 (1 million), assuming that transactions are small, only 100 bytes in size, and it is permissible to have 100MB of unpurged table rows.

The purge lag is presented as the History list length value in the TRANSACTIONS section of SHOW ENGINE INNODB STATUS output.

```
mysql> SHOW ENGINE INNODB STATUS;
...
------------
TRANSACTIONS
------------
Trx id counter 0 290328385
Purge done for trx's n:o < 0 290315608 undo n:o < 0 17
History list length 20
```

The History list length is typically a low value, usually less than a few thousand, but a writeheavy workload or long running transactions can cause it to increase, even for transactions that are read only. The reason that a long running transaction can cause the History list length to increase is that under a consistent read transaction isolation level such as REPEATABLE READ, a transaction must return the same result as when the read view for that transaction was created. Consequently, the InnoDB multi-version concurrency control (MVCC) system must keep a copy of the data in the undo log until all transactions that depend on that data have completed. The following are examples of long running transactions that could cause the History list length to increase:

- A mysqldump operation that uses the --single-transaction option while there is a significant amount of concurrent DML.
- Running a SELECT query after disabling autocommit, and forgetting to issue an explicit COMMIT or ROLLBACK.

To prevent excessive delays in extreme situations where the purge lag becomes huge, you can limit the delay by setting the innodb\_max\_purge\_lag\_delay variable. The innodb\_max\_purge\_lag\_delay variable specifies the maximum delay in microseconds for the delay imposed when the innodb\_max\_purge\_lag threshold is exceeded. The specified innodb\_max\_purge\_lag\_delay value is an upper limit on the delay period calculated by the innodb\_max\_purge\_lag formula.

## **Purge and Undo Tablespace Truncation**

The purge system is also responsible for truncating undo tablespaces. You can configure the innodb\_purge\_rseg\_truncate\_frequency variable to control the frequency with which the purge system looks for undo tablespaces to truncate. For more information, see [Truncating Undo](#page-59-0) [Tablespaces.](#page-59-0)

# <span id="page-109-0"></span>**14.8.11 Configuring Optimizer Statistics for InnoDB**

This section describes how to configure persistent and non-persistent optimizer statistics for InnoDB tables.

Persistent optimizer statistics are persisted across server restarts, allowing for greater plan stability and more consistent query performance. Persistent optimizer statistics also provide control and flexibility with these additional benefits:

- You can use the innodb\_stats\_auto\_recalc configuration option to control whether statistics are updated automatically after substantial changes to a table.
- You can use the STATS\_PERSISTENT, STATS\_AUTO\_RECALC, and STATS\_SAMPLE\_PAGES clauses with CREATE TABLE and ALTER TABLE statements to configure optimizer statistics for individual tables.
- You can query optimizer statistics data in the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables.
- You can view the last\_update column of the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables to see when statistics were last updated.
- You can manually modify the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables to force a specific query optimization plan or to test alternative plans without modifying the database.

The persistent optimizer statistics feature is enabled by default (innodb\_stats\_persistent=ON).

Non-persistent optimizer statistics are cleared on each server restart and after some other operations, and recomputed on the next table access. As a result, different estimates could be produced when recomputing statistics, leading to different choices in execution plans and variations in query performance.

This section also provides information about estimating ANALYZE TABLE complexity, which may be useful when attempting to achieve a balance between accurate statistics and ANALYZE TABLE execution time.

# <span id="page-110-0"></span>**14.8.11.1 Configuring Persistent Optimizer Statistics Parameters**

The persistent optimizer statistics feature improves plan stability by storing statistics to disk and making them persistent across server restarts so that the optimizer is more likely to make consistent choices each time for a given query.

Optimizer statistics are persisted to disk when innodb\_stats\_persistent=ON or when individual tables are defined with STATS\_PERSISTENT=1. innodb\_stats\_persistent is enabled by default.

Formerly, optimizer statistics were cleared when restarting the server and after some other types of operations, and recomputed on the next table access. Consequently, different estimates could be produced when recalculating statistics leading to different choices in query execution plans and variation in query performance.

Persistent statistics are stored in the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables. See [InnoDB Persistent Statistics Tables.](#page-112-0)

If you prefer not to persist optimizer statistics to disk, see [Section 14.8.11.2, "Configuring Non-](#page-117-0)[Persistent Optimizer Statistics Parameters"](#page-117-0)

#### **Configuring Automatic Statistics Calculation for Persistent Optimizer Statistics**

The innodb\_stats\_auto\_recalc variable, which is enabled by default, controls whether statistics are calculated automatically when a table undergoes changes to more than 10% of its rows. You can also configure automatic statistics recalculation for individual tables by specifying the STATS\_AUTO\_RECALC clause when creating or altering a table.

Because of the asynchronous nature of automatic statistics recalculation, which occurs in the background, statistics may not be recalculated instantly after running a DML operation that affects more than 10% of a table, even when innodb\_stats\_auto\_recalc is enabled. Statistics recalculation can be delayed by few seconds in some cases. If up-to-date statistics are required immediately, run ANALYZE TABLE to initiate a synchronous (foreground) recalculation of statistics.

If innodb\_stats\_auto\_recalc is disabled, you can ensure the accuracy of optimizer statistics by executing the ANALYZE TABLE statement after making substantial changes to indexed columns. You might also consider adding ANALYZE TABLE to setup scripts that you run after loading data, and running ANALYZE TABLE on a schedule at times of low activity.

When an index is added to an existing table, or when a column is added or dropped, index statistics are calculated and added to the innodb\_index\_stats table regardless of the value of innodb\_stats\_auto\_recalc.

### **Configuring Optimizer Statistics Parameters for Individual Tables**

innodb\_stats\_persistent, innodb\_stats\_auto\_recalc, and innodb\_stats\_persistent\_sample\_pages are global variables. To override these systemwide settings and configure optimizer statistics parameters for individual tables, you can define STATS\_PERSISTENT, STATS\_AUTO\_RECALC, and STATS\_SAMPLE\_PAGES clauses in CREATE TABLE or ALTER TABLE statements.

- STATS\_PERSISTENT specifies whether to enable persistent statistics for an InnoDB table. The value DEFAULT causes the persistent statistics setting for the table to be determined by the innodb\_stats\_persistent setting. A value of 1 enables persistent statistics for the table, while a value of 0 disables the feature. After enabling persistent statistics for an individual table, use ANALYZE TABLE to calculate statistics after table data is loaded.
- STATS\_AUTO\_RECALC specifies whether to automatically recalculate persistent statistics. The value DEFAULT causes the persistent statistics setting for the table to be determined by the innodb\_stats\_auto\_recalc setting. A value of 1 causes statistics to be recalculated when 10% of table data has changed. A value 0 prevents automatic recalculation for the table. When using a value of 0, use ANALYZE TABLE to recalculate statistics after making substantial changes to the table.
- STATS\_SAMPLE\_PAGES specifies the number of index pages to sample when cardinality and other statistics are calculated for an indexed column, by an ANALYZE TABLE operation, for example.

All three clauses are specified in the following CREATE TABLE example:

```
CREATE TABLE `t1` (
`id` int(8) NOT NULL auto_increment,
`data` varchar(255),
`date` datetime,
PRIMARY KEY (`id`),
INDEX `DATE_IX` (`date`)
) ENGINE=InnoDB,
 STATS_PERSISTENT=1,
 STATS_AUTO_RECALC=1,
 STATS_SAMPLE_PAGES=25;
```

#### **Configuring the Number of Sampled Pages for InnoDB Optimizer Statistics**

The optimizer uses estimated statistics about key distributions to choose the indexes for an execution plan, based on the relative selectivity of the index. Operations such as ANALYZE TABLE cause InnoDB to sample random pages from each index on a table to estimate the cardinality of the index. This sampling technique is known as a random dive.

The innodb\_stats\_persistent\_sample\_pages controls the number of sampled pages. You can adjust the setting at runtime to manage the quality of statistics estimates used by the optimizer. The default value is 20. Consider modifying the setting when encountering the following issues:

1. Statistics are not accurate enough and the optimizer chooses suboptimal plans, as shown in EXPLAIN output. You can check the accuracy of statistics by comparing the actual cardinality of an index (determined by running SELECT DISTINCT on the index columns) with the estimates in the mysql.innodb\_index\_stats table.

If it is determined that statistics are not accurate enough, the value of innodb\_stats\_persistent\_sample\_pages should be increased until the statistics estimates are sufficiently accurate. Increasing innodb\_stats\_persistent\_sample\_pages too much, however, could cause ANALYZE TABLE to run slowly.

2. ANALYZE TABLE is too slow. In this case innodb\_stats\_persistent\_sample\_pages should be decreased until ANALYZE TABLE execution time is acceptable. Decreasing the value too much, however, could lead to the first problem of inaccurate statistics and suboptimal query execution plans.

If a balance cannot be achieved between accurate statistics and ANALYZE TABLE execution time, consider decreasing the number of indexed columns in the table or limiting the number of partitions to reduce ANALYZE TABLE complexity. The number of columns in the table's primary key is also important to consider, as primary key columns are appended to each nonunique index.

For related information, see [Section 14.8.11.3, "Estimating ANALYZE TABLE Complexity for](#page-118-0) [InnoDB Tables"](#page-118-0).

#### **Including Delete-marked Records in Persistent Statistics Calculations**

By default, InnoDB reads uncommitted data when calculating statistics. In the case of an uncommitted transaction that deletes rows from a table, delete-marked records are excluded when calculating row estimates and index statistics, which can lead to non-optimal execution plans for other transactions that are operating on the table concurrently using a transaction isolation level other than [READ](#page-73-2) [UNCOMMITTED](#page-73-2). To avoid this scenario, innodb\_stats\_include\_delete\_marked can be enabled to ensure that delete-marked records are included when calculating persistent optimizer statistics.

When innodb\_stats\_include\_delete\_marked is enabled, ANALYZE TABLE considers deletemarked records when recalculating statistics.

innodb\_stats\_include\_delete\_marked is a global setting that affects all InnoDB tables, and it is only applicable to persistent optimizer statistics.

innodb\_stats\_include\_delete\_marked was introduced in MySQL 5.7.16.

# <span id="page-112-0"></span>**InnoDB Persistent Statistics Tables**

The persistent statistics feature relies on the internally managed tables in the mysql database, named innodb\_table\_stats and innodb\_index\_stats. These tables are set up automatically in all install, upgrade, and build-from-source procedures.

**Table 14.4 Columns of innodb\_table\_stats**

| Column name              | Description                                                 |
|--------------------------|-------------------------------------------------------------|
| database_name            | Database name                                               |
| table_name               | Table name, partition name, or subpartition name            |
| last_update              | A timestamp indicating the last time the row was<br>updated |
| n_rows                   | The number of rows in the table                             |
| clustered_index_size     | The size of the primary index, in pages                     |
| sum_of_other_index_sizes | The total size of other (non-primary) indexes, in<br>pages  |

**Table 14.5 Columns of innodb\_index\_stats**

| Column name   | Description                                      |
|---------------|--------------------------------------------------|
| database_name | Database name                                    |
| table_name    | Table name, partition name, or subpartition name |
| index_name    | Index name                                       |

| Column name      | Description                                                                       |
|------------------|-----------------------------------------------------------------------------------|
| last_update      | A timestamp indicating the last time that InnoDB<br>updated this row              |
| stat_name        | The name of the statistic, whose value is reported<br>in the stat_value column    |
| stat_value       | The value of the statistic that is named in<br>stat_name column                   |
| sample_size      | The number of pages sampled for the estimate<br>provided in the stat_value column |
| stat_description | Description of the statistic that is named in the<br>stat_name column             |

The innodb\_table\_stats and innodb\_index\_stats tables include a last\_update column that shows when index statistics were last updated:

```
mysql> SELECT * FROM innodb_table_stats \G
*************************** 1. row ***************************
 database_name: sakila
 table_name: actor
 last_update: 2014-05-28 16:16:44
 n_rows: 200
 clustered_index_size: 1
sum_of_other_index_sizes: 1
...
```

```
mysql> SELECT * FROM innodb_index_stats \G
*************************** 1. row ***************************
 database_name: sakila
 table_name: actor
 index_name: PRIMARY
 last_update: 2014-05-28 16:16:44
 stat_name: n_diff_pfx01
 stat_value: 200
 sample_size: 1
 ...
```

The innodb\_table\_stats and innodb\_index\_stats tables can be updated manually, which makes it possible to force a specific query optimization plan or test alternative plans without modifying the database. If you manually update statistics, use the FLUSH TABLE tbl\_name statement to load the updated statistics.

Persistent statistics are considered local information, because they relate to the server instance. The innodb\_table\_stats and innodb\_index\_stats tables are therefore not replicated when automatic statistics recalculation takes place. If you run ANALYZE TABLE to initiate a synchronous recalculation of statistics, this statement is replicated (unless you suppressed logging for it), and recalculation takes place on the replicas.

#### <span id="page-113-0"></span>**InnoDB Persistent Statistics Tables Example**

The innodb\_table\_stats table contains one row for each table. The following example demonstrates the type of data collected.

Table t1 contains a primary index (columns a, b) secondary index (columns c, d), and unique index (columns e, f):

```
CREATE TABLE t1 (
a INT, b INT, c INT, d INT, e INT, f INT,
PRIMARY KEY (a, b), KEY i1 (c, d), UNIQUE KEY i2uniq (e, f)
) ENGINE=INNODB;
```

After inserting five rows of sample data, table t1 appears as follows:

```
mysql> SELECT * FROM t1;
```

```
+---+---+------+------+------+------+
| a | b | c | d | e | f |
+---+---+------+------+------+------+
| 1 | 1 | 10 | 11 | 100 | 101 |
| 1 | 2 | 10 | 11 | 200 | 102 |
| 1 | 3 | 10 | 11 | 100 | 103 |
| 1 | 4 | 10 | 12 | 200 | 104 |
| 1 | 5 | 10 | 12 | 100 | 105 |
+---+---+------+------+------+------+
```

To immediately update statistics, run ANALYZE TABLE (if innodb\_stats\_auto\_recalc is enabled, statistics are updated automatically within a few seconds assuming that the 10% threshold for changed table rows is reached):

```
mysql> ANALYZE TABLE t1;
+---------+---------+----------+----------+
| Table | Op | Msg_type | Msg_text |
+---------+---------+----------+----------+
| test.t1 | analyze | status | OK |
+---------+---------+----------+----------+
```

Table statistics for table t1 show the last time InnoDB updated the table statistics (2014-03-14 14:36:34), the number of rows in the table (5), the clustered index size (1 page), and the combined size of the other indexes (2 pages).

```
mysql> SELECT * FROM mysql.innodb_table_stats WHERE table_name like 't1'\G
*************************** 1. row ***************************
 database_name: test
 table_name: t1
 last_update: 2014-03-14 14:36:34
 n_rows: 5
 clustered_index_size: 1
sum_of_other_index_sizes: 2
```

The innodb\_index\_stats table contains multiple rows for each index. Each row in the innodb\_index\_stats table provides data related to a particular index statistic which is named in the stat\_name column and described in the stat\_description column. For example:

```
mysql> SELECT index_name, stat_name, stat_value, stat_description
 FROM mysql.innodb_index_stats WHERE table_name like 't1';
+------------+--------------+------------+-----------------------------------+
| index_name | stat_name | stat_value | stat_description |
+------------+--------------+------------+-----------------------------------+
| PRIMARY | n_diff_pfx01 | 1 | a |
| PRIMARY | n_diff_pfx02 | 5 | a,b |
| PRIMARY | n_leaf_pages | 1 | Number of leaf pages in the index |
| PRIMARY | size | 1 | Number of pages in the index |
| i1 | n_diff_pfx01 | 1 | c |
| i1 | n_diff_pfx02 | 2 | c,d |
| i1 | n_diff_pfx03 | 2 | c,d,a |
| i1 | n_diff_pfx04 | 5 | c,d,a,b |
| i1 | n_leaf_pages | 1 | Number of leaf pages in the index |
| i1 | size | 1 | Number of pages in the index |
| i2uniq | n_diff_pfx01 | 2 | e |
| i2uniq | n_diff_pfx02 | 5 | e,f |
| i2uniq | n_leaf_pages | 1 | Number of leaf pages in the index |
| i2uniq | size | 1 | Number of pages in the index |
+------------+--------------+------------+-----------------------------------+
```

The stat\_name column shows the following types of statistics:

- size: Where stat\_name=size, the stat\_value column displays the total number of pages in the index.
- n\_leaf\_pages: Where stat\_name=n\_leaf\_pages, the stat\_value column displays the number of leaf pages in the index.
- n\_diff\_pfxNN: Where stat\_name=n\_diff\_pfx01, the stat\_value column displays the number of distinct values in the first column of the index. Where stat\_name=n\_diff\_pfx02, the

stat\_value column displays the number of distinct values in the first two columns of the index, and so on. Where stat\_name=n\_diff\_pfxNN, the stat\_description column shows a comma separated list of the index columns that are counted.

To further illustrate the n\_diff\_pfxNN statistic, which provides cardinality data, consider once again the t1 table example that was introduced previously. As shown below, the t1 table is created with a primary index (columns a, b), a secondary index (columns c, d), and a unique index (columns e, f):

```
CREATE TABLE t1 (
 a INT, b INT, c INT, d INT, e INT, f INT,
 PRIMARY KEY (a, b), KEY i1 (c, d), UNIQUE KEY i2uniq (e, f)
) ENGINE=INNODB;
```

After inserting five rows of sample data, table t1 appears as follows:

```
mysql> SELECT * FROM t1;
+---+---+------+------+------+------+
| a | b | c | d | e | f |
+---+---+------+------+------+------+
| 1 | 1 | 10 | 11 | 100 | 101 |
| 1 | 2 | 10 | 11 | 200 | 102 |
| 1 | 3 | 10 | 11 | 100 | 103 |
| 1 | 4 | 10 | 12 | 200 | 104 |
| 1 | 5 | 10 | 12 | 100 | 105 |
+---+---+------+------+------+------+
```

When you query the index\_name, stat\_name, stat\_value, and stat\_description, where stat\_name LIKE 'n\_diff%', the following result set is returned:

```
mysql> SELECT index_name, stat_name, stat_value, stat_description
 FROM mysql.innodb_index_stats
 WHERE table_name like 't1' AND stat_name LIKE 'n_diff%';
+------------+--------------+------------+------------------+
| index_name | stat_name | stat_value | stat_description |
+------------+--------------+------------+------------------+
| PRIMARY | n_diff_pfx01 | 1 | a |
| PRIMARY | n_diff_pfx02 | 5 | a,b |
| i1 | n_diff_pfx01 | 1 | c |
| i1 | n_diff_pfx02 | 2 | c,d |
| i1 | n_diff_pfx03 | 2 | c,d,a |
| i1 | n_diff_pfx04 | 5 | c,d,a,b |
| i2uniq | n_diff_pfx01 | 2 | e |
| i2uniq | n_diff_pfx02 | 5 | e,f |
+------------+--------------+------------+------------------+
```

For the PRIMARY index, there are two n\_diff% rows. The number of rows is equal to the number of columns in the index.

![](_page_115_Picture_9.jpeg)

#### **Note**

For nonunique indexes, InnoDB appends the columns of the primary key.

- Where index\_name=PRIMARY and stat\_name=n\_diff\_pfx01, the stat\_value is 1, which indicates that there is a single distinct value in the first column of the index (column a). The number of distinct values in column a is confirmed by viewing the data in column a in table t1, in which there is a single distinct value (1). The counted column (a) is shown in the stat\_description column of the result set.
- Where index\_name=PRIMARY and stat\_name=n\_diff\_pfx02, the stat\_value is 5, which indicates that there are five distinct values in the two columns of the index (a,b). The number of distinct values in columns a and b is confirmed by viewing the data in columns a and b in table t1, in which there are five distinct values: (1,1), (1,2), (1,3), (1,4) and (1,5). The counted columns (a,b) are shown in the stat\_description column of the result set.

For the secondary index (i1), there are four n\_diff% rows. Only two columns are defined for the secondary index (c,d) but there are four n\_diff% rows for the secondary index because InnoDB suffixes all nonunique indexes with the primary key. As a result, there are four n\_diff% rows instead of two to account for the both the secondary index columns (c,d) and the primary key columns (a,b).

- Where index\_name=i1 and stat\_name=n\_diff\_pfx01, the stat\_value is 1, which indicates that there is a single distinct value in the first column of the index (column c). The number of distinct values in column c is confirmed by viewing the data in column c in table t1, in which there is a single distinct value: (10). The counted column (c) is shown in the stat\_description column of the result set.
- Where index\_name=i1 and stat\_name=n\_diff\_pfx02, the stat\_value is 2, which indicates that there are two distinct values in the first two columns of the index (c,d). The number of distinct values in columns c an d is confirmed by viewing the data in columns c and d in table t1, in which there are two distinct values: (10,11) and (10,12). The counted columns (c,d) are shown in the stat\_description column of the result set.
- Where index\_name=i1 and stat\_name=n\_diff\_pfx03, the stat\_value is 2, which indicates that there are two distinct values in the first three columns of the index (c,d,a). The number of distinct values in columns c, d, and a is confirmed by viewing the data in column c, d, and a in table t1, in which there are two distinct values: (10,11,1) and (10,12,1). The counted columns (c,d,a) are shown in the stat\_description column of the result set.
- Where index\_name=i1 and stat\_name=n\_diff\_pfx04, the stat\_value is 5, which indicates that there are five distinct values in the four columns of the index (c,d,a,b). The number of distinct values in columns c, d, a and b is confirmed by viewing the data in columns c, d, a, and b in table t1, in which there are five distinct values: (10,11,1,1), (10,11,1,2), (10,11,1,3), (10,12,1,4), and (10,12,1,5). The counted columns (c,d,a,b) are shown in the stat\_description column of the result set.

For the unique index (i2uniq), there are two n\_diff% rows.

- Where index\_name=i2uniq and stat\_name=n\_diff\_pfx01, the stat\_value is 2, which indicates that there are two distinct values in the first column of the index (column e). The number of distinct values in column e is confirmed by viewing the data in column e in table t1, in which there are two distinct values: (100) and (200). The counted column (e) is shown in the stat\_description column of the result set.
- Where index\_name=i2uniq and stat\_name=n\_diff\_pfx02, the stat\_value is 5, which indicates that there are five distinct values in the two columns of the index (e,f). The number of distinct values in columns e and f is confirmed by viewing the data in columns e and f in table t1, in which there are five distinct values: (100,101), (200,102), (100,103), (200,104), and (100,105). The counted columns (e,f) are shown in the stat\_description column of the result set.

# **Retrieving Index Size Using the innodb\_index\_stats Table**

You can retrieve the index size for tables, partitions, or subpartitions can using the innodb\_index\_stats table. In the following example, index sizes are retrieved for table t1. For a definition of table t1 and corresponding index statistics, see [InnoDB Persistent Statistics Tables](#page-113-0) [Example.](#page-113-0)

```
mysql> SELECT SUM(stat_value) pages, index_name,
 SUM(stat_value)*@@innodb_page_size size
 FROM mysql.innodb_index_stats WHERE table_name='t1'
 AND stat_name = 'size' GROUP BY index_name;
+-------+------------+-------+
| pages | index_name | size |
+-------+------------+-------+
| 1 | PRIMARY | 16384 |
| 1 | i1 | 16384 |
| 1 | i2uniq | 16384 |
+-------+------------+-------+
```

For partitions or subpartitions, you can use the same query with a modified WHERE clause to retrieve index sizes. For example, the following query retrieves index sizes for partitions of table t1:

```
mysql> SELECT SUM(stat_value) pages, index_name,
 SUM(stat_value)*@@innodb_page_size size
 FROM mysql.innodb_index_stats WHERE table_name like 't1#P%'
 AND stat_name = 'size' GROUP BY index_name;
```

## <span id="page-117-0"></span>**14.8.11.2 Configuring Non-Persistent Optimizer Statistics Parameters**

This section describes how to configure non-persistent optimizer statistics. Optimizer statistics are not persisted to disk when innodb\_stats\_persistent=OFF or when individual tables are created or altered with STATS\_PERSISTENT=0. Instead, statistics are stored in memory, and are lost when the server is shut down. Statistics are also updated periodically by certain operations and under certain conditions.

As of MySQL 5.6.6, optimizer statistics are persisted to disk by default, enabled by the innodb\_stats\_persistent configuration option. For information about persistent optimizer statistics, see [Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters"](#page-110-0).

### **Optimizer Statistics Updates**

Non-persistent optimizer statistics are updated when:

- Running ANALYZE TABLE.
- Running SHOW TABLE STATUS, SHOW INDEX, or querying the Information Schema TABLES or STATISTICS tables with the innodb\_stats\_on\_metadata option enabled.

The default setting for innodb\_stats\_on\_metadata was changed to OFF when persistent optimizer statistics were enabled by default in MySQL 5.6.6. Enabling innodb\_stats\_on\_metadata may reduce access speed for schemas that have a large number of tables or indexes, and reduce stability of execution plans for queries that involve InnoDB tables. innodb\_stats\_on\_metadata is configured globally using a SET statement.

SET GLOBAL innodb\_stats\_on\_metadata=ON

![](_page_117_Picture_11.jpeg)

## **Note**

innodb\_stats\_on\_metadata only applies when optimizer statistics are configured to be non-persistent (when innodb\_stats\_persistent is disabled).

• Starting a mysql client with the --auto-rehash option enabled, which is the default. The autorehash option causes all InnoDB tables to be opened, and the open table operations cause statistics to be recalculated.

To improve the start up time of the mysql client and to updating statistics, you can turn off autorehash using the --disable-auto-rehash option. The auto-rehash feature enables automatic name completion of database, table, and column names for interactive users.

- A table is first opened.
- InnoDB detects that 1 / 16 of table has been modified since the last time statistics were updated.

### **Configuring the Number of Sampled Pages**

The MySQL query optimizer uses estimated statistics about key distributions to choose the indexes for an execution plan, based on the relative selectivity of the index. When InnoDB updates optimizer statistics, it samples random pages from each index on a table to estimate the cardinality of the index. (This technique is known as random dives.)

To give you control over the quality of the statistics estimate (and thus better information for the query optimizer), you can change the number of sampled pages using the parameter innodb\_stats\_transient\_sample\_pages. The default number of sampled pages is 8, which could be insufficient to produce an accurate estimate, leading to poor index choices by the query

optimizer. This technique is especially important for large tables and tables used in joins. Unnecessary full table scans for such tables can be a substantial performance issue. See Section 8.2.1.20, "Avoiding Full Table Scans" for tips on tuning such queries. innodb\_stats\_transient\_sample\_pages is a global parameter that can be set at runtime.

The value of innodb\_stats\_transient\_sample\_pages affects the index sampling for all InnoDB tables and indexes when innodb\_stats\_persistent=0. Be aware of the following potentially significant impacts when you change the index sample size:

- Small values like 1 or 2 can result in inaccurate estimates of cardinality.
- Increasing the innodb\_stats\_transient\_sample\_pages value might require more disk reads. Values much larger than 8 (say, 100), can cause a significant slowdown in the time it takes to open a table or execute SHOW TABLE STATUS.
- The optimizer might choose very different query plans based on different estimates of index selectivity.

Whatever value of innodb\_stats\_transient\_sample\_pages works best for a system, set the option and leave it at that value. Choose a value that results in reasonably accurate estimates for all tables in your database without requiring excessive I/O. Because the statistics are automatically recalculated at various times other than on execution of ANALYZE TABLE, it does not make sense to increase the index sample size, run ANALYZE TABLE, then decrease sample size again.

Smaller tables generally require fewer index samples than larger tables. If your database has many large tables, consider using a higher value for innodb\_stats\_transient\_sample\_pages than if you have mostly smaller tables.

## <span id="page-118-0"></span>**14.8.11.3 Estimating ANALYZE TABLE Complexity for InnoDB Tables**

ANALYZE TABLE complexity for InnoDB tables is dependent on:

- The number of pages sampled, as defined by innodb\_stats\_persistent\_sample\_pages.
- The number of indexed columns in a table
- The number of partitions. If a table has no partitions, the number of partitions is considered to be 1.

Using these parameters, an approximate formula for estimating ANALYZE TABLE complexity would be:

The value of innodb\_stats\_persistent\_sample\_pages \* number of indexed columns in a table \* the number of partitions

Typically, the greater the resulting value, the greater the execution time for ANALYZE TABLE.

![](_page_118_Picture_16.jpeg)

### **Note**

innodb\_stats\_persistent\_sample\_pages defines the number of pages sampled at a global level. To set the number of pages sampled for an individual table, use the STATS\_SAMPLE\_PAGES option with CREATE TABLE or ALTER TABLE. For more information, see [Section 14.8.11.1, "Configuring Persistent](#page-110-0) [Optimizer Statistics Parameters".](#page-110-0)

If innodb\_stats\_persistent=OFF, the number of pages sampled is defined by innodb\_stats\_transient\_sample\_pages. See [Section 14.8.11.2,](#page-117-0) ["Configuring Non-Persistent Optimizer Statistics Parameters"](#page-117-0) for additional information.

For a more in-depth approach to estimating ANALYZE TABLE complexity, consider the following example.

In [Big O notation](http://en.wikipedia.org/wiki/Big_O_notation), ANALYZE TABLE complexity is described as:

```
O(n_sample
 * (n_cols_in_uniq_i
 + n_cols_in_non_uniq_i
 + n_cols_in_pk * (1 + n_non_uniq_i))
 * n_part)
```

#### where:

- n\_sample is the number of pages sampled (defined by innodb\_stats\_persistent\_sample\_pages)
- n\_cols\_in\_uniq\_i is total number of all columns in all unique indexes (not counting the primary key columns)
- n\_cols\_in\_non\_uniq\_i is the total number of all columns in all nonunique indexes
- n\_cols\_in\_pk is the number of columns in the primary key (if a primary key is not defined, InnoDB creates a single column primary key internally)
- n\_non\_uniq\_i is the number of nonunique indexes in the table
- n\_part is the number of partitions. If no partitions are defined, the table is considered to be a single partition.

Now, consider the following table (table t), which has a primary key (2 columns), a unique index (2 columns), and two nonunique indexes (two columns each):

```
CREATE TABLE t (
 a INT,
 b INT,
 c INT,
 d INT,
 e INT,
 f INT,
 g INT,
 h INT,
 PRIMARY KEY (a, b),
 UNIQUE KEY i1uniq (c, d),
 KEY i2nonuniq (e, f),
 KEY i3nonuniq (g, h)
);
```

For the column and index data required by the algorithm described above, query the mysql.innodb\_index\_stats persistent index statistics table for table t. The n\_diff\_pfx% statistics show the columns that are counted for each index. For example, columns a and b are counted for the primary key index. For the nonunique indexes, the primary key columns (a,b) are counted in addition to the user defined columns.

![](_page_119_Picture_12.jpeg)

### **Note**

For additional information about the InnoDB persistent statistics tables, see [Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters"](#page-110-0)

```
mysql> SELECT index_name, stat_name, stat_description
 FROM mysql.innodb_index_stats WHERE
 database_name='test' AND
 table_name='t' AND
 stat_name like 'n_diff_pfx%';
 +------------+--------------+------------------+
 | index_name | stat_name | stat_description |
 +------------+--------------+------------------+
 | PRIMARY | n_diff_pfx01 | a |
 | PRIMARY | n_diff_pfx02 | a,b |
 | i1uniq | n_diff_pfx01 | c |
 | i1uniq | n_diff_pfx02 | c,d |
 | i2nonuniq | n_diff_pfx01 | e |
 | i2nonuniq | n_diff_pfx02 | e,f |
```

```
 | i2nonuniq | n_diff_pfx03 | e,f,a |
 | i2nonuniq | n_diff_pfx04 | e,f,a,b |
 | i3nonuniq | n_diff_pfx01 | g |
 | i3nonuniq | n_diff_pfx02 | g,h |
 | i3nonuniq | n_diff_pfx03 | g,h,a |
 | i3nonuniq | n_diff_pfx04 | g,h,a,b |
 +------------+--------------+------------------+
```

Based on the index statistics data shown above and the table definition, the following values can be determined:

- n\_cols\_in\_uniq\_i, the total number of all columns in all unique indexes not counting the primary key columns, is 2 (c and d)
- n\_cols\_in\_non\_uniq\_i, the total number of all columns in all nonunique indexes, is 4 (e, f, g and h)
- n\_cols\_in\_pk, the number of columns in the primary key, is 2 (a and b)
- n\_non\_uniq\_i, the number of nonunique indexes in the table, is 2 (i2nonuniq and i3nonuniq))
- n\_part, the number of partitions, is 1.

You can now calculate innodb\_stats\_persistent\_sample\_pages \* (2 + 4 + 2 \* (1 + 2)) \* 1 to determine the number of leaf pages that are scanned. With innodb\_stats\_persistent\_sample\_pages set to the default value of 20, and with a default page size of 16 KiB (innodb\_page\_size=16384), you can then estimate that 20 \* 12 \* 16384 bytes are read for table t, or about 4 MiB.

![](_page_120_Picture_9.jpeg)

#### **Note**

All 4 MiB may not be read from disk, as some leaf pages may already be cached in the buffer pool.

# <span id="page-120-0"></span>**14.8.12 Configuring the Merge Threshold for Index Pages**

You can configure the MERGE\_THRESHOLD value for index pages. If the "page-full" percentage for an index page falls below the MERGE\_THRESHOLD value when a row is deleted or when a row is shortened by an UPDATE operation, InnoDB attempts to merge the index page with a neighboring index page. The default MERGE\_THRESHOLD value is 50, which is the previously hardcoded value. The minimum MERGE\_THRESHOLD value is 1 and the maximum value is 50.

When the "page-full" percentage for an index page falls below 50%, which is the default MERGE\_THRESHOLD setting, InnoDB attempts to merge the index page with a neighboring page. If both pages are close to 50% full, a page split can occur soon after the pages are merged. If this mergesplit behavior occurs frequently, it can have an adverse affect on performance. To avoid frequent merge-splits, you can lower the MERGE\_THRESHOLD value so that InnoDB attempts page merges at a lower "page-full" percentage. Merging pages at a lower page-full percentage leaves more room in index pages and helps reduce merge-split behavior.

The MERGE\_THRESHOLD for index pages can be defined for a table or for individual indexes. A MERGE\_THRESHOLD value defined for an individual index takes priority over a MERGE\_THRESHOLD value defined for the table. If undefined, the MERGE\_THRESHOLD value defaults to 50.

## **Setting MERGE\_THRESHOLD for a Table**

You can set the MERGE\_THRESHOLD value for a table using the table\_option COMMENT clause of the CREATE TABLE statement. For example:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id)
) COMMENT='MERGE_THRESHOLD=45';
```

You can also set the MERGE\_THRESHOLD value for an existing table using the table\_option COMMENT clause with ALTER TABLE:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id)
);
ALTER TABLE t1 COMMENT='MERGE_THRESHOLD=40';
```

# **Setting MERGE\_THRESHOLD for Individual Indexes**

To set the MERGE\_THRESHOLD value for an individual index, you can use the index\_option COMMENT clause with CREATE TABLE, ALTER TABLE, or CREATE INDEX, as shown in the following examples:

• Setting MERGE\_THRESHOLD for an individual index using CREATE TABLE:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id) COMMENT 'MERGE_THRESHOLD=40'
);
```

• Setting MERGE\_THRESHOLD for an individual index using ALTER TABLE:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id)
);
ALTER TABLE t1 DROP KEY id_index;
ALTER TABLE t1 ADD KEY id_index (id) COMMENT 'MERGE_THRESHOLD=40';
```

• Setting MERGE\_THRESHOLD for an individual index using CREATE INDEX:

```
CREATE TABLE t1 (id INT);
CREATE INDEX id_index ON t1 (id) COMMENT 'MERGE_THRESHOLD=40';
```

![](_page_121_Picture_11.jpeg)

# **Note**

You cannot modify the MERGE\_THRESHOLD value at the index level for GEN\_CLUST\_INDEX, which is the clustered index created by InnoDB when an InnoDB table is created without a primary key or unique key index. You can only modify the MERGE\_THRESHOLD value for GEN\_CLUST\_INDEX by setting MERGE\_THRESHOLD for the table.

# **Querying the MERGE\_THRESHOLD Value for an Index**

The current MERGE\_THRESHOLD value for an index can be obtained by querying the INNODB\_SYS\_INDEXES table. For example:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_INDEXES WHERE NAME='id_index' \G
*************************** 1. row ***************************
 INDEX_ID: 91
 NAME: id_index
 TABLE_ID: 68
 TYPE: 0
 N_FIELDS: 1
 PAGE_NO: 4
 SPACE: 57
MERGE_THRESHOLD: 40
```

You can use SHOW CREATE TABLE to view the MERGE\_THRESHOLD value for a table, if explicitly defined using the table\_option COMMENT clause:

```
mysql> SHOW CREATE TABLE t2 \G
*************************** 1. row ***************************
 Table: t2
```

```
Create Table: CREATE TABLE `t2` (
 `id` int(11) DEFAULT NULL,
 KEY `id_index` (`id`) COMMENT 'MERGE_THRESHOLD=40'
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

![](_page_122_Picture_2.jpeg)

#### **Note**

A MERGE\_THRESHOLD value defined at the index level takes priority over a MERGE\_THRESHOLD value defined for the table. If undefined, MERGE\_THRESHOLD defaults to 50% (MERGE\_THRESHOLD=50, which is the previously hardcoded value.

Likewise, you can use SHOW INDEX to view the MERGE\_THRESHOLD value for an index, if explicitly defined using the index\_option COMMENT clause:

```
mysql> SHOW INDEX FROM t2 \G
*************************** 1. row ***************************
 Table: t2
 Non_unique: 1
 Key_name: id_index
 Seq_in_index: 1
 Column_name: id
 Collation: A
 Cardinality: 0
 Sub_part: NULL
 Packed: NULL
 Null: YES
 Index_type: BTREE
 Comment:
Index_comment: MERGE_THRESHOLD=40
```

# **Measuring the Effect of MERGE\_THRESHOLD Settings**

The INNODB\_METRICS table provides two counters that can be used to measure the effect of a MERGE\_THRESHOLD setting on index page merges.

```
mysql> SELECT NAME, COMMENT FROM INFORMATION_SCHEMA.INNODB_METRICS
 WHERE NAME like '%index_page_merge%';
+-----------------------------+----------------------------------------+
| NAME | COMMENT |
+-----------------------------+----------------------------------------+
| index_page_merge_attempts | Number of index page merge attempts |
| index_page_merge_successful | Number of successful index page merges |
+-----------------------------+----------------------------------------+
```

When lowering the MERGE\_THRESHOLD value, the objectives are:

- A smaller number of page merge attempts and successful page merges
- A similar number of page merge attempts and successful page merges

A MERGE\_THRESHOLD setting that is too small could result in large data files due to an excessive amount of empty page space.

For information about using INNODB\_METRICS counters, see Section 14.16.6, "InnoDB INFORMATION\_SCHEMA Metrics Table".

# <span id="page-122-0"></span>**14.9 InnoDB Table and Page Compression**

This section provides information about the InnoDB table compression and InnoDB page compression features. The page compression feature is referred to as transparent page compression.

Using the compression features of InnoDB, you can create tables where the data is stored in compressed form. Compression can help to improve both raw performance and scalability. The compression means less data is transferred between disk and memory, and takes up less space on disk and in memory. The benefits are amplified for tables with secondary indexes, because index data is compressed also. Compression can be especially important for SSD storage devices, because they tend to have lower capacity than HDD devices.

# <span id="page-123-0"></span>**14.9.1 InnoDB Table Compression**

This section describes InnoDB table compression, which is supported with InnoDB tables that reside in file\_per\_table tablespaces or general tablespaces. Table compression is enabled using the ROW\_FORMAT=COMPRESSED attribute with CREATE TABLE or ALTER TABLE.