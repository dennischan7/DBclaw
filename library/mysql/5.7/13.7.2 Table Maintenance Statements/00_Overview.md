---
source: MySQL 5.7 Reference
title: 00_Overview
---

# <span id="page-116-0"></span>**13.7.2.1 ANALYZE TABLE Statement**

```
ANALYZE [NO_WRITE_TO_BINLOG | LOCAL]
 TABLE tbl_name [, tbl_name] ...
```

[ANALYZE TABLE](#page-116-0) performs a key distribution analysis and stores the distribution for the named table or tables. For MyISAM tables, this statement is equivalent to using myisamchk --analyze.

This statement requires SELECT and INSERT privileges for the table.

[ANALYZE TABLE](#page-116-0) works with InnoDB, NDB, and MyISAM tables. It does not work with views.

[ANALYZE TABLE](#page-116-0) is supported for partitioned tables, and you can use ALTER TABLE ... ANALYZE PARTITION to analyze one or more partitions; for more information, see Section 13.1.8, "ALTER TABLE Statement", and Section 22.3.4, "Maintenance of Partitions".

During the analysis, the table is locked with a read lock for InnoDB and MyISAM.

[ANALYZE TABLE](#page-116-0) removes the table from the table definition cache, which requires a flush lock. If there are long running statements or transactions still using the table, subsequent statements and transactions must wait for those operations to finish before the flush lock is released. Because [ANALYZE TABLE](#page-116-0) itself typically finishes quickly, it may not be apparent that delayed transactions or statements involving the same table are due to the remaining flush lock.

By default, the server writes [ANALYZE TABLE](#page-116-0) statements to the binary log so that they replicate to replicas. To suppress logging, specify the optional NO\_WRITE\_TO\_BINLOG keyword or its alias LOCAL.

- [ANALYZE TABLE Output](#page-117-0)
- [Key Distribution Analysis](#page-117-1)
- [Other Considerations](#page-117-2)

### <span id="page-117-0"></span>**ANALYZE TABLE Output**

[ANALYZE TABLE](#page-116-0) returns a result set with the columns shown in the following table.

| Column   | Value                                 |
|----------|---------------------------------------|
| Table    | The table name                        |
| Op       | Always analyze                        |
| Msg_type | status, error, info, note, or warning |
| Msg_text | An informational message              |

### <span id="page-117-1"></span>**Key Distribution Analysis**

If the table has not changed since the last key distribution analysis, the table is not analyzed again.

MySQL uses the stored key distribution to decide the table join order for joins on something other than a constant. In addition, key distributions can be used when deciding which indexes to use for a specific table within a query.

To check the stored key distribution cardinality, use the [SHOW INDEX](#page-154-1) statement or the INFORMATION\_SCHEMA STATISTICS table. See [Section 13.7.5.22, "SHOW INDEX Statement"](#page-154-1), and Section 24.3.24, "The INFORMATION\_SCHEMA STATISTICS Table".

For InnoDB tables, [ANALYZE TABLE](#page-116-0) determines index cardinality by performing random dives on each of the index trees and updating index cardinality estimates accordingly. Because these are only estimates, repeated runs of [ANALYZE TABLE](#page-116-0) could produce different numbers. This makes [ANALYZE](#page-116-0) [TABLE](#page-116-0) fast on InnoDB tables but not 100% accurate because it does not take all rows into account.

You can make the statistics collected by [ANALYZE TABLE](#page-116-0) more precise and more stable by enabling innodb\_stats\_persistent, as explained in Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters". When innodb\_stats\_persistent is enabled, it is important to run [ANALYZE](#page-116-0) [TABLE](#page-116-0) after major changes to index column data, as statistics are not recalculated periodically (such as after a server restart).

If innodb\_stats\_persistent is enabled, you can change the number of random dives by modifying the innodb\_stats\_persistent\_sample\_pages system variable. If innodb\_stats\_persistent is disabled, modify innodb\_stats\_transient\_sample\_pages instead.

For more information about key distribution analysis in InnoDB, see Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters", and Section 14.8.11.3, "Estimating ANALYZE TABLE Complexity for InnoDB Tables".

MySQL uses index cardinality estimates in join optimization. If a join is not optimized in the right way, try running [ANALYZE TABLE](#page-116-0). In the few cases that [ANALYZE TABLE](#page-116-0) does not produce values good enough for your particular tables, you can use FORCE INDEX with your queries to force the use of a particular index, or set the max\_seeks\_for\_key system variable to ensure that MySQL prefers index lookups over table scans. See Section B.3.5, "Optimizer-Related Issues".

# <span id="page-117-2"></span>**Other Considerations**

ANALYZE TABLE clears table statistics from the Information Schema INNODB\_SYS\_TABLESTATS table and sets the STATS\_INITIALIZED column to Uninitialized. Statistics are collected again the next time the table is accessed.

# <span id="page-118-0"></span>**13.7.2.2 CHECK TABLE Statement**

```
CHECK TABLE tbl_name [, tbl_name] ... [option] ...
option: {
 FOR UPGRADE
 | QUICK
 | FAST
 | MEDIUM
 | EXTENDED
 | CHANGED
}
```

[CHECK TABLE](#page-118-0) checks a table or tables for errors. For MyISAM tables, the key statistics are updated as well. [CHECK TABLE](#page-118-0) can also check views for problems, such as tables that are referenced in the view definition that no longer exist.

To check a table, you must have some privilege for it.

[CHECK TABLE](#page-118-0) works for InnoDB, MyISAM, ARCHIVE, and CSV tables.

Before running [CHECK TABLE](#page-118-0) on InnoDB tables, see [CHECK TABLE Usage Notes for InnoDB Tables](#page-121-0).

[CHECK TABLE](#page-118-0) is supported for partitioned tables, and you can use ALTER TABLE ... CHECK PARTITION to check one or more partitions; for more information, see Section 13.1.8, "ALTER TABLE Statement", and Section 22.3.4, "Maintenance of Partitions".

[CHECK TABLE](#page-118-0) ignores virtual generated columns that are not indexed.

- [CHECK TABLE Output](#page-118-1)
- [Checking Version Compatibility](#page-118-2)
- [Checking Data Consistency](#page-119-0)
- [CHECK TABLE Usage Notes for InnoDB Tables](#page-121-0)
- [CHECK TABLE Usage Notes for MyISAM Tables](#page-121-1)

### <span id="page-118-1"></span>**CHECK TABLE Output**

[CHECK TABLE](#page-118-0) returns a result set with the columns shown in the following table.

| Column   | Value                                 |
|----------|---------------------------------------|
| Table    | The table name                        |
| Op       | Always check                          |
| Msg_type | status, error, info, note, or warning |
| Msg_text | An informational message              |

The statement might produce many rows of information for each checked table. The last row has a Msg\_type value of status and the Msg\_text normally should be OK. For a MyISAM table, if you don't get OK or Table is already up to date, you should normally run a repair of the table. See Section 7.6, "MyISAM Table Maintenance and Crash Recovery". Table is already up to date means that the storage engine for the table indicated that there was no need to check the table.

### <span id="page-118-2"></span>**Checking Version Compatibility**

The FOR UPGRADE option checks whether the named tables are compatible with the current version of MySQL. With FOR UPGRADE, the server checks each table to determine whether there have been any incompatible changes in any of the table's data types or indexes since the table was created. If not, the check succeeds. Otherwise, if there is a possible incompatibility, the server runs a full check on the

table (which might take some time). If the full check succeeds, the server marks the table's .frm file with the current MySQL version number. Marking the .frm file ensures that further checks for the table with the same version of the server are fast.

Incompatibilities might occur because the storage format for a data type has changed or because its sort order has changed. Our aim is to avoid these changes, but occasionally they are necessary to correct problems that would be worse than an incompatibility between releases.

FOR UPGRADE discovers these incompatibilities:

- The indexing order for end-space in TEXT columns for InnoDB and MyISAM tables changed between MySQL 4.1 and 5.0.
- The storage method of the new DECIMAL data type changed between MySQL 5.0.3 and 5.0.5.
- If your table was created by a different version of the MySQL server than the one you are currently running, FOR UPGRADE indicates that the table has an .frm file with an incompatible version. In this case, the result set returned by [CHECK TABLE](#page-118-0) contains a line with a Msg\_type value of error and a Msg\_text value of Table upgrade required. Please do "REPAIR TABLE `tbl\_name`" to fix it!
- Changes are sometimes made to character sets or collations that require table indexes to be rebuilt. For details about such changes, see Section 2.10.3, "Changes in MySQL 5.7". For information about rebuilding tables, see Section 2.10.12, "Rebuilding or Repairing Tables or Indexes".
- The YEAR(2) data type is deprecated and support for it is removed in MySQL 5.7.5. For tables containing YEAR(2) columns, [CHECK TABLE](#page-118-0) recommends [REPAIR TABLE](#page-125-0), which converts 2-digit YEAR(2) columns to 4-digit YEAR columns.
- As of MySQL 5.7.2, trigger creation time is maintained. If run against a table that has triggers, [CHECK](#page-118-0) [TABLE ... FOR UPGRADE](#page-118-0) displays this warning for each trigger created before MySQL 5.7.2:

```
Trigger db_name.tbl_name.trigger_name does not have CREATED attribute.
```

The warning is informational only. No change is made to the trigger.

• As of MySQL 5.7.7, a table is reported as needing a rebuild if it contains old temporal columns in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision) and the avoid\_temporal\_upgrade system variable is disabled. This helps the MySQL upgrade procedure detect and upgrade tables containing old temporal columns. If avoid\_temporal\_upgrade is enabled, FOR UPGRADE ignores the old temporal columns present in the table; consequently, the upgrade procedure does not upgrade them.

To check for tables that contain such temporal columns and need a rebuild, disable avoid\_temporal\_upgrade before executing [CHECK TABLE ... FOR UPGRADE](#page-118-0).

• Warnings are issued for tables that use nonnative partitioning because nonnative partitioning is deprecated in MySQL 5.7 and removed in MySQL 8.0. See Chapter 22, Partitioning.

### <span id="page-119-0"></span>**Checking Data Consistency**

The following table shows the other check options that can be given. These options are passed to the storage engine, which may use or ignore them.

| Type  | Meaning                                                                                                                  |
|-------|--------------------------------------------------------------------------------------------------------------------------|
| QUICK | Do not scan the rows to check for incorrect links.<br>Applies to InnoDB and MyISAM tables and views.                     |
| FAST  | Check only tables that have not been closed<br>properly. Ignored for InnoDB; applies only to<br>MyISAM tables and views. |

| Type     | Meaning                                                                                                                                                                                                                                |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CHANGED  | Check only tables that have been changed since<br>the last check or that have not been closed<br>properly. Ignored for InnoDB; applies only to<br>MyISAM tables and views.                                                             |
| MEDIUM   | Scan rows to verify that deleted links are valid.<br>This also calculates a key checksum for the rows<br>and verifies this with a calculated checksum for<br>the keys. Ignored for InnoDB; applies only to<br>MyISAM tables and views. |
| EXTENDED | Do a full key lookup for all keys for each row. This<br>ensures that the table is 100% consistent, but<br>takes a long time. Ignored for InnoDB; applies<br>only to MyISAM tables and views.                                           |

If none of the options QUICK, MEDIUM, or EXTENDED are specified, the default check type for dynamicformat MyISAM tables is MEDIUM. This has the same result as running myisamchk --medium-check tbl\_name on the table. The default check type also is MEDIUM for static-format MyISAM tables, unless CHANGED or FAST is specified. In that case, the default is QUICK. The row scan is skipped for CHANGED and FAST because the rows are very seldom corrupted.

You can combine check options, as in the following example that does a quick check on the table to determine whether it was closed properly:

CHECK TABLE test\_table FAST QUICK;

![](_page_120_Picture_5.jpeg)

#### **Note**

If [CHECK TABLE](#page-118-0) finds no problems with a table that is marked as "corrupted" or "not closed properly", [CHECK TABLE](#page-118-0) may remove the mark.

If a table is corrupted, the problem is most likely in the indexes and not in the data part. All of the preceding check types check the indexes thoroughly and should thus find most errors.

To check a table that you assume is okay, use no check options or the QUICK option. The latter should be used when you are in a hurry and can take the very small risk that QUICK does not find an error in the data file. (In most cases, under normal usage, MySQL should find any error in the data file. If this happens, the table is marked as "corrupted" and cannot be used until it is repaired.)

FAST and CHANGED are mostly intended to be used from a script (for example, to be executed from cron) to check tables periodically. In most cases, FAST is to be preferred over CHANGED. (The only case when it is not preferred is when you suspect that you have found a bug in the MyISAM code.)

EXTENDED is to be used only after you have run a normal check but still get errors from a table when MySQL tries to update a row or find a row by key. This is very unlikely if a normal check has succeeded.

Use of [CHECK TABLE ... EXTENDED](#page-118-0) might influence execution plans generated by the query optimizer.

Some problems reported by [CHECK TABLE](#page-118-0) cannot be corrected automatically:

• Found row where the auto\_increment column has the value 0.

This means that you have a row in the table where the AUTO\_INCREMENT index column contains the value 0. (It is possible to create a row where the AUTO\_INCREMENT column is 0 by explicitly setting the column to 0 with an [UPDATE](#page-8-0) statement.)

This is not an error in itself, but could cause trouble if you decide to dump the table and restore it or do an ALTER TABLE on the table. In this case, the AUTO\_INCREMENT column changes value

according to the rules of AUTO\_INCREMENT columns, which could cause problems such as a duplicate-key error.

To get rid of the warning, execute an [UPDATE](#page-8-0) statement to set the column to some value other than 0.

### <span id="page-121-0"></span>**CHECK TABLE Usage Notes for InnoDB Tables**

The following notes apply to InnoDB tables:

- If [CHECK TABLE](#page-118-0) encounters a corrupt page, the server exits to prevent error propagation (Bug #10132). If the corruption occurs in a secondary index but table data is readable, running [CHECK](#page-118-0) [TABLE](#page-118-0) can still cause a server exit.
- If [CHECK TABLE](#page-118-0) encounters a corrupted DB\_TRX\_ID or DB\_ROLL\_PTR field in a clustered index, [CHECK TABLE](#page-118-0) can cause InnoDB to access an invalid undo log record, resulting in an MVCCrelated server exit.
- If [CHECK TABLE](#page-118-0) encounters errors in InnoDB tables or indexes, it reports an error, and usually marks the index and sometimes marks the table as corrupted, preventing further use of the index or table. Such errors include an incorrect number of entries in a secondary index or incorrect links.
- If [CHECK TABLE](#page-118-0) finds an incorrect number of entries in a secondary index, it reports an error but does not cause a server exit or prevent access to the file.
- [CHECK TABLE](#page-118-0) surveys the index page structure, then surveys each key entry. It does not validate the key pointer to a clustered record or follow the path for BLOB pointers.
- When an InnoDB table is stored in its own .ibd file, the first 3 pages of the .ibd file contain header information rather than table or index data. The [CHECK TABLE](#page-118-0) statement does not detect inconsistencies that affect only the header data. To verify the entire contents of an InnoDB .ibd file, use the innochecksum command.
- When running [CHECK TABLE](#page-118-0) on large InnoDB tables, other threads may be blocked during [CHECK](#page-118-0) [TABLE](#page-118-0) execution. To avoid timeouts, the semaphore wait threshold (600 seconds) is extended by 2 hours (7200 seconds) for [CHECK TABLE](#page-118-0) operations. If InnoDB detects semaphore waits of 240 seconds or more, it starts printing InnoDB monitor output to the error log. If a lock request extends beyond the semaphore wait threshold, InnoDB aborts the process. To avoid the possibility of a semaphore wait timeout entirely, run [CHECK TABLE QUICK](#page-118-0) instead of [CHECK TABLE](#page-118-0).
- [CHECK TABLE](#page-118-0) functionality for InnoDB SPATIAL indexes includes an R-tree validity check and a check to ensure that the R-tree row count matches the clustered index.
- [CHECK TABLE](#page-118-0) supports secondary indexes on virtual generated columns, which are supported by InnoDB.

## <span id="page-121-1"></span>**CHECK TABLE Usage Notes for MyISAM Tables**

The following notes apply to MyISAM tables:

- [CHECK TABLE](#page-118-0) updates key statistics for MyISAM tables.
- If [CHECK TABLE](#page-118-0) output does not return OK or Table is already up to date, you should normally run a repair of the table. See Section 7.6, "MyISAM Table Maintenance and Crash Recovery".
- If none of the [CHECK TABLE](#page-118-0) options QUICK, MEDIUM, or EXTENDED are specified, the default check type for dynamic-format MyISAM tables is MEDIUM. This has the same result as running myisamchk --medium-check tbl\_name on the table. The default check type also is MEDIUM for static-format MyISAM tables, unless CHANGED or FAST is specified. In that case, the default is QUICK. The row scan is skipped for CHANGED and FAST because the rows are very seldom corrupted.

# <span id="page-122-1"></span>**13.7.2.3 CHECKSUM TABLE Statement**

```
CHECKSUM TABLE tbl_name [, tbl_name] ... [QUICK | EXTENDED]
```

[CHECKSUM TABLE](#page-122-1) reports a checksum for the contents of a table. You can use this statement to verify that the contents are the same before and after a backup, rollback, or other operation that is intended to put the data back to a known state.

This statement requires the SELECT privilege for the table.

This statement is not supported for views. If you run [CHECKSUM TABLE](#page-122-1) against a view, the Checksum value is always NULL, and a warning is returned.

For a nonexistent table, [CHECKSUM TABLE](#page-122-1) returns NULL and generates a warning.

During the checksum operation, the table is locked with a read lock for InnoDB and MyISAM.

### **Performance Considerations**

By default, the entire table is read row by row and the checksum is calculated. For large tables, this could take a long time, thus you would only perform this operation occasionally. This row-by-row calculation is what you get with the EXTENDED clause, with InnoDB and all other storage engines other than MyISAM, and with MyISAM tables not created with the CHECKSUM=1 clause.

For MyISAM tables created with the CHECKSUM=1 clause, [CHECKSUM TABLE](#page-122-1) or [CHECKSUM](#page-122-1) [TABLE ... QUICK](#page-122-1) returns the "live" table checksum that can be returned very fast. If the table does not meet all these conditions, the QUICK method returns NULL. The QUICK method is not supported with InnoDB tables. See Section 13.1.18, "CREATE TABLE Statement" for the syntax of the CHECKSUM clause.

The checksum value depends on the table row format. If the row format changes, the checksum also changes. For example, the storage format for temporal types such as TIME, DATETIME, and TIMESTAMP changed in MySQL 5.6 prior to MySQL 5.6.5, so if a 5.5 table is upgraded to MySQL 5.6, the checksum value may change.

![](_page_122_Picture_12.jpeg)

### **Important**

If the checksums for two tables are different, then it is almost certain that the tables are different in some way. However, because the hashing function used by [CHECKSUM TABLE](#page-122-1) is not guaranteed to be collision-free, there is a slight chance that two tables which are not identical can produce the same checksum.

# <span id="page-122-0"></span>**13.7.2.4 OPTIMIZE TABLE Statement**

```
OPTIMIZE [NO_WRITE_TO_BINLOG | LOCAL]
 TABLE tbl_name [, tbl_name] ...
```

[OPTIMIZE TABLE](#page-122-0) reorganizes the physical storage of table data and associated index data, to reduce storage space and improve I/O efficiency when accessing the table. The exact changes made to each table depend on the storage engine used by that table.

Use [OPTIMIZE TABLE](#page-122-0) in these cases, depending on the type of table:

- After doing substantial insert, update, or delete operations on an InnoDB table that has its own .ibd file because it was created with the innodb\_file\_per\_table option enabled. The table and indexes are reorganized, and disk space can be reclaimed for use by the operating system.
- After doing substantial insert, update, or delete operations on columns that are part of a FULLTEXT index in an InnoDB table. Set the configuration option innodb\_optimize\_fulltext\_only=1 first. To keep the index maintenance period to a

reasonable time, set the innodb\_ft\_num\_word\_optimize option to specify how many words to update in the search index, and run a sequence of OPTIMIZE TABLE statements until the search index is fully updated.

• After deleting a large part of a MyISAM or ARCHIVE table, or making many changes to a MyISAM or ARCHIVE table with variable-length rows (tables that have VARCHAR, VARBINARY, BLOB, or TEXT columns). Deleted rows are maintained in a linked list and subsequent INSERT operations reuse old row positions. You can use [OPTIMIZE TABLE](#page-122-0) to reclaim the unused space and to defragment the data file. After extensive changes to a table, this statement may also improve performance of statements that use the table, sometimes significantly.

This statement requires SELECT and INSERT privileges for the table.

[OPTIMIZE TABLE](#page-122-0) works for InnoDB, MyISAM, and ARCHIVE tables. [OPTIMIZE TABLE](#page-122-0) is also supported for dynamic columns of in-memory NDB tables. It does not work for fixed-width columns of inmemory tables, nor does it work for Disk Data tables. The performance of OPTIMIZE on NDB Cluster tables can be tuned using --ndb-optimization-delay, which controls the length of time to wait between processing batches of rows by [OPTIMIZE TABLE](#page-122-0). For more information, see [Previous NDB](https://dev.mysql.com/doc/refman/8.0/en/mysql-cluster-limitations-resolved.md) [Cluster Issues Resolved in NDB Cluster 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-cluster-limitations-resolved.md).

For NDB Cluster tables, [OPTIMIZE TABLE](#page-122-0) can be interrupted by (for example) killing the SQL thread performing the OPTIMIZE operation.

By default, [OPTIMIZE TABLE](#page-122-0) does not work for tables created using any other storage engine and returns a result indicating this lack of support. You can make [OPTIMIZE TABLE](#page-122-0) work for other storage engines by starting mysqld with the --skip-new option. In this case, [OPTIMIZE TABLE](#page-122-0) is just mapped to ALTER TABLE.

This statement does not work with views.

[OPTIMIZE TABLE](#page-122-0) is supported for partitioned tables. For information about using this statement with partitioned tables and table partitions, see Section 22.3.4, "Maintenance of Partitions".

By default, the server writes [OPTIMIZE TABLE](#page-122-0) statements to the binary log so that they replicate to replicas. To suppress logging, specify the optional NO\_WRITE\_TO\_BINLOG keyword or its alias LOCAL.

- [OPTIMIZE TABLE Output](#page-123-0)
- [InnoDB Details](#page-124-0)
- [MyISAM Details](#page-124-1)
- [Other Considerations](#page-124-2)

### <span id="page-123-0"></span>**OPTIMIZE TABLE Output**

[OPTIMIZE TABLE](#page-122-0) returns a result set with the columns shown in the following table.

| Column   | Value                                 |
|----------|---------------------------------------|
| Table    | The table name                        |
| Op       | Always optimize                       |
| Msg_type | status, error, info, note, or warning |
| Msg_text | An informational message              |

[OPTIMIZE TABLE](#page-122-0) table catches and throws any errors that occur while copying table statistics from the old file to the newly created file. For example. if the user ID of the owner of the .frm, .MYD, or .MYI file is different from the user ID of the mysqld process, [OPTIMIZE TABLE](#page-122-0) generates a "cannot change ownership of the file" error unless mysqld is started by the root user.

### <span id="page-124-0"></span>**InnoDB Details**

For InnoDB tables, [OPTIMIZE TABLE](#page-122-0) is mapped to ALTER TABLE ... FORCE, which rebuilds the table to update index statistics and free unused space in the clustered index. This is displayed in the output of [OPTIMIZE TABLE](#page-122-0) when you run it on an InnoDB table, as shown here:

```
mysql> OPTIMIZE TABLE foo;
+----------+----------+----------+-------------------------------------------------------------------+
| Table | Op | Msg_type | Msg_text |
+----------+----------+----------+-------------------------------------------------------------------+
| test.foo | optimize | note | Table does not support optimize, doing recreate + analyze instead |
| test.foo | optimize | status | OK |
+----------+----------+----------+-------------------------------------------------------------------+
```

[OPTIMIZE TABLE](#page-122-0) uses online DDL for regular and partitioned InnoDB tables, which reduces downtime for concurrent DML operations. The table rebuild triggered by [OPTIMIZE TABLE](#page-122-0) is completed in place. An exclusive table lock is only taken briefly during the prepare phase and the commit phase of the operation. During the prepare phase, metadata is updated and an intermediate table is created. During the commit phase, table metadata changes are committed.

[OPTIMIZE TABLE](#page-122-0) rebuilds the table using the table copy method under the following conditions:

- When the old\_alter\_table system variable is enabled.
- When the server is started with the --skip-new option.

[OPTIMIZE TABLE](#page-122-0) using online DDL is not supported for InnoDB tables that contain FULLTEXT indexes. The table copy method is used instead.

InnoDB stores data using a page-allocation method and does not suffer from fragmentation in the same way that legacy storage engines (such as MyISAM) do. When considering whether or not to run OPTIMIZE TABLE, consider the workload of transactions that your server is expected to process:

- Some level of fragmentation is expected. InnoDB fills pages only 93% full, to leave room for updates without having to split pages.
- Delete operations might leave gaps that leave pages less filled than desired, which could make it worthwhile to optimize the table.
- Updates to rows usually rewrite the data within the same page, depending on the data type and row format, when sufficient space is available. See Section 14.9.1.5, "How Compression Works for InnoDB Tables" and Section 14.11, "InnoDB Row Formats".
- High-concurrency workloads might leave gaps in indexes over time, as InnoDB retains multiple versions of the same data due through its MVCC mechanism. See Section 14.3, "InnoDB Multi-Versioning".

### <span id="page-124-1"></span>**MyISAM Details**

For MyISAM tables, [OPTIMIZE TABLE](#page-122-0) works as follows:

- 1. If the table has deleted or split rows, repair the table.
- 2. If the index pages are not sorted, sort them.
- 3. If the table's statistics are not up to date (and the repair could not be accomplished by sorting the index), update them.

### <span id="page-124-2"></span>**Other Considerations**

[OPTIMIZE TABLE](#page-122-0) is performed online for regular and partitioned InnoDB tables. Otherwise, MySQL locks the table during the time [OPTIMIZE TABLE](#page-122-0) is running.

[OPTIMIZE TABLE](#page-122-0) does not sort R-tree indexes, such as spatial indexes on POINT columns. (Bug #23578)

## <span id="page-125-0"></span>**13.7.2.5 REPAIR TABLE Statement**

```
REPAIR [NO_WRITE_TO_BINLOG | LOCAL]
 TABLE tbl_name [, tbl_name] ...
 [QUICK] [EXTENDED] [USE_FRM]
```

[REPAIR TABLE](#page-125-0) repairs a possibly corrupted table, for certain storage engines only.

This statement requires SELECT and INSERT privileges for the table.

Although normally you should never have to run [REPAIR TABLE](#page-125-0), if disaster strikes, this statement is very likely to get back all your data from a MyISAM table. If your tables become corrupted often, try to find the reason for it, to eliminate the need to use [REPAIR TABLE](#page-125-0). See Section B.3.3.3, "What to Do If MySQL Keeps Crashing", and Section 15.2.4, "MyISAM Table Problems".

[REPAIR TABLE](#page-125-0) checks the table to see whether an upgrade is required. If so, it performs the upgrade, following the same rules as [CHECK TABLE ... FOR UPGRADE](#page-118-0). See [Section 13.7.2.2, "CHECK](#page-118-0) [TABLE Statement"](#page-118-0), for more information.

![](_page_125_Picture_8.jpeg)

### **Important**

- Make a backup of a table before performing a table repair operation; under some circumstances the operation might cause data loss. Possible causes include but are not limited to file system errors. See Chapter 7, Backup and Recovery.
- If the server exits during a [REPAIR TABLE](#page-125-0) operation, it is essential after restarting it that you immediately execute another [REPAIR TABLE](#page-125-0) statement for the table before performing any other operations on it. In the worst case, you might have a new clean index file without information about the data file, and then the next operation you perform could overwrite the data file. This is an unlikely but possible scenario that underscores the value of making a backup first.
- In the event that a table on the source becomes corrupted and you run [REPAIR TABLE](#page-125-0) on it, any resulting changes to the original table are not propagated to replicas.
- [REPAIR TABLE Storage Engine and Partitioning Support](#page-125-1)
- [REPAIR TABLE Options](#page-126-0)
- [REPAIR TABLE Output](#page-126-1)
- [Table Repair Considerations](#page-127-0)

### <span id="page-125-1"></span>**REPAIR TABLE Storage Engine and Partitioning Support**

[REPAIR TABLE](#page-125-0) works for MyISAM, ARCHIVE, and CSV tables. For MyISAM tables, it has the same effect as myisamchk --recover tbl\_name by default. This statement does not work with views.

[REPAIR TABLE](#page-125-0) is supported for partitioned tables. However, the USE\_FRM option cannot be used with this statement on a partitioned table.

You can use ALTER TABLE ... REPAIR PARTITION to repair one or more partitions; for more information, see Section 13.1.8, "ALTER TABLE Statement", and Section 22.3.4, "Maintenance of Partitions".

# <span id="page-126-0"></span>**REPAIR TABLE Options**

• NO\_WRITE\_TO\_BINLOG or LOCAL

By default, the server writes [REPAIR TABLE](#page-125-0) statements to the binary log so that they replicate to replicas. To suppress logging, specify the optional NO\_WRITE\_TO\_BINLOG keyword or its alias LOCAL.

• QUICK

If you use the QUICK option, [REPAIR TABLE](#page-125-0) tries to repair only the index file, and not the data file. This type of repair is like that done by myisamchk --recover --quick.

• EXTENDED

If you use the EXTENDED option, MySQL creates the index row by row instead of creating one index at a time with sorting. This type of repair is like that done by myisamchk --safe-recover.

• USE\_FRM

The USE\_FRM option is available for use if the .MYI index file is missing or if its header is corrupted. This option tells MySQL not to trust the information in the .MYI file header and to re-create it using information from the .frm file. This kind of repair cannot be done with myisamchk.

![](_page_126_Picture_10.jpeg)

#### **Caution**

Use the USE\_FRM option only if you cannot use regular REPAIR modes. Telling the server to ignore the .MYI file makes important table metadata stored in the .MYI unavailable to the repair process, which can have deleterious consequences:

- The current AUTO\_INCREMENT value is lost.
- The link to deleted records in the table is lost, which means that free space for deleted records remain unoccupied thereafter.
- The .MYI header indicates whether the table is compressed. If the server ignores this information, it cannot tell that a table is compressed and repair can cause change or loss of table contents. This means that USE\_FRM should not be used with compressed tables. That should not be necessary, anyway: Compressed tables are read only, so they should not become corrupt.

If you use USE\_FRM for a table that was created by a different version of the MySQL server than the one you are currently running, [REPAIR TABLE](#page-125-0) does not attempt to repair the table. In this case, the result set returned by [REPAIR](#page-125-0) [TABLE](#page-125-0) contains a line with a Msg\_type value of error and a Msg\_text value of Failed repairing incompatible .FRM file.

If USE\_FRM is used, [REPAIR TABLE](#page-125-0) does not check the table to see whether an upgrade is required.

### <span id="page-126-1"></span>**REPAIR TABLE Output**

[REPAIR TABLE](#page-125-0) returns a result set with the columns shown in the following table.

| Column | Value          |
|--------|----------------|
| Table  | The table name |
| Op     | Always repair  |

| Column   | Value                                 |
|----------|---------------------------------------|
| Msg_type | status, error, info, note, or warning |
| Msg_text | An informational message              |

The [REPAIR TABLE](#page-125-0) statement might produce many rows of information for each repaired table. The last row has a Msg\_type value of status and Msg\_test normally should be OK. For a MyISAM table, if you do not get OK, you should try repairing it with myisamchk --safe-recover. ([REPAIR TABLE](#page-125-0) does not implement all the options of myisamchk. With myisamchk --safe-recover, you can also use options that [REPAIR TABLE](#page-125-0) does not support, such as --max-record-length.)

[REPAIR TABLE](#page-125-0) table catches and throws any errors that occur while copying table statistics from the old corrupted file to the newly created file. For example. if the user ID of the owner of the .frm, .MYD, or .MYI file is different from the user ID of the mysqld process, [REPAIR TABLE](#page-125-0) generates a "cannot change ownership of the file" error unless mysqld is started by the root user.

### <span id="page-127-0"></span>**Table Repair Considerations**

[REPAIR TABLE](#page-125-0) upgrades a table if it contains old temporal columns in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision) and the avoid\_temporal\_upgrade system variable is disabled. If avoid\_temporal\_upgrade is enabled, [REPAIR TABLE](#page-125-0) ignores the old temporal columns present in the table and does not upgrade them.

To upgrade tables that contain such temporal columns, disable avoid\_temporal\_upgrade before executing [REPAIR TABLE](#page-125-0).

You may be able to increase [REPAIR TABLE](#page-125-0) performance by setting certain system variables. See Section 8.6.3, "Optimizing REPAIR TABLE Statements".