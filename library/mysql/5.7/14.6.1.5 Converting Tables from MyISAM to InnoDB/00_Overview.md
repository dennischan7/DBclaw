---
source: MySQL 5.7 Reference
title: 00_Overview
---

If you have MyISAM tables that you want to convert to [InnoDB](#page-0-0) for better reliability and scalability, review the following guidelines and tips before converting.

- [Adjusting Memory Usage for MyISAM and InnoDB](#page-31-0)
- [Handling Too-Long Or Too-Short Transactions](#page-31-1)
- [Handling Deadlocks](#page-32-0)
- [Storage Layout](#page-32-1)
- [Converting an Existing Table](#page-32-2)
- [Cloning the Structure of a Table](#page-33-0)
- [Transferring Data](#page-33-1)
- [Storage Requirements](#page-33-2)
- [Defining Primary Keys](#page-34-0)

- [Application Performance Considerations](#page-34-1)
- [Understanding Files Associated with InnoDB Tables](#page-35-1)

#### <span id="page-31-0"></span>**Adjusting Memory Usage for MyISAM and InnoDB**

As you transition away from MyISAM tables, lower the value of the key\_buffer\_size configuration option to free memory no longer needed for caching results. Increase the value of the [innodb\\_buffer\\_pool\\_size](#page-196-0) configuration option, which performs a similar role of allocating cache memory for InnoDB tables. The InnoDB buffer pool caches both table data and index data, speeding up lookups for queries and keeping query results in memory for reuse. For guidance regarding buffer pool size configuration, see Section 8.12.4.1, "How MySQL Uses Memory".

On a busy server, run benchmarks with the query cache turned off. The InnoDB buffer pool provides similar benefits, so the query cache might be tying up memory unnecessarily. For information about the query cache, see Section 8.10.3, "The MySQL Query Cache".

### <span id="page-31-1"></span>**Handling Too-Long Or Too-Short Transactions**

Because MyISAM tables do not support transactions, you might not have paid much attention to the autocommit configuration option and the COMMIT and ROLLBACK statements. These keywords are important to allow multiple sessions to read and write InnoDB tables concurrently, providing substantial scalability benefits in write-heavy workloads.

While a transaction is open, the system keeps a snapshot of the data as seen at the beginning of the transaction, which can cause substantial overhead if the system inserts, updates, and deletes millions of rows while a stray transaction keeps running. Thus, take care to avoid transactions that run for too long:

- If you are using a mysql session for interactive experiments, always COMMIT (to finalize the changes) or ROLLBACK (to undo the changes) when finished. Close down interactive sessions rather than leave them open for long periods, to avoid keeping transactions open for long periods by accident.
- Make sure that any error handlers in your application also ROLLBACK incomplete changes or COMMIT completed changes.
- ROLLBACK is a relatively expensive operation, because INSERT, UPDATE, and DELETE operations are written to InnoDB tables prior to the COMMIT, with the expectation that most changes are committed successfully and rollbacks are rare. When experimenting with large volumes of data, avoid making changes to large numbers of rows and then rolling back those changes.
- When loading large volumes of data with a sequence of INSERT statements, periodically COMMIT the results to avoid having transactions that last for hours. In typical load operations for data warehousing, if something goes wrong, you truncate the table (using TRUNCATE TABLE) and start over from the beginning rather than doing a ROLLBACK.

The preceding tips save memory and disk space that can be wasted during too-long transactions. When transactions are shorter than they should be, the problem is excessive I/O. With each COMMIT, MySQL makes sure each change is safely recorded to disk, which involves some I/O.

- For most operations on InnoDB tables, you should use the setting autocommit=0. From an efficiency perspective, this avoids unnecessary I/O when you issue large numbers of consecutive INSERT, UPDATE, or DELETE statements. From a safety perspective, this allows you to issue a ROLLBACK statement to recover lost or garbled data if you make a mistake on the mysql command line, or in an exception handler in your application.
- autocommit=1 is suitable for InnoDB tables when running a sequence of queries for generating reports or analyzing statistics. In this situation, there is no I/O penalty related to COMMIT or ROLLBACK, and InnoDB can automatically optimize the read-only workload.

- If you make a series of related changes, finalize all the changes at once with a single COMMIT at the end. For example, if you insert related pieces of information into several tables, do a single COMMIT after making all the changes. Or if you run many consecutive INSERT statements, do a single COMMIT after all the data is loaded; if you are doing millions of INSERT statements, perhaps split up the huge transaction by issuing a COMMIT every ten thousand or hundred thousand records, so the transaction does not grow too large.
- Remember that even a SELECT statement opens a transaction, so after running some report or debugging queries in an interactive mysql session, either issue a COMMIT or close the mysql session.

For related information, see [Section 14.7.2.2, "autocommit, Commit, and Rollback".](#page-73-0)

### <span id="page-32-0"></span>**Handling Deadlocks**

You might see warning messages referring to "deadlocks" in the MySQL error log, or the output of SHOW ENGINE INNODB STATUS. A deadlock is not a serious issue for InnoDB tables, and often does not require any corrective action. When two transactions start modifying multiple tables, accessing the tables in a different order, they can reach a state where each transaction is waiting for the other and neither can proceed. When deadlock detection is enabled (the default), MySQL immediately detects this condition and cancels (rolls back) the "smaller" transaction, allowing the other to proceed. If deadlock detection is disabled using the innodb\_deadlock\_detect configuration option, InnoDB relies on the innodb\_lock\_wait\_timeout setting to roll back transactions in case of a deadlock.

Either way, your applications need error-handling logic to restart a transaction that is forcibly cancelled due to a deadlock. When you re-issue the same SQL statements as before, the original timing issue no longer applies. Either the other transaction has already finished and yours can proceed, or the other transaction is still in progress and your transaction waits until it finishes.

If deadlock warnings occur constantly, you might review the application code to reorder the SQL operations in a consistent way, or to shorten the transactions. You can test with the innodb\_print\_all\_deadlocks option enabled to see all deadlock warnings in the MySQL error log, rather than only the last warning in the SHOW ENGINE INNODB STATUS output.

For more information, see [Section 14.7.5, "Deadlocks in InnoDB".](#page-81-1)

#### <span id="page-32-1"></span>**Storage Layout**

To get the best performance from InnoDB tables, you can adjust a number of parameters related to storage layout.

When you convert MyISAM tables that are large, frequently accessed, and hold vital data, investigate and consider the innodb\_file\_per\_table, innodb\_file\_format, and innodb\_page\_size variables, and the ROW\_FORMAT and [KEY\\_BLOCK\\_SIZE](#page-145-1) clauses of the CREATE TABLE statement.

During your initial experiments, the most important setting is innodb\_file\_per\_table. When this setting is enabled, which is the default as of MySQL 5.6.6, new InnoDB tables are implicitly created in file-per-table tablespaces. In contrast with the InnoDB system tablespace, file-per-table tablespaces allow disk space to be reclaimed by the operating system when a table is truncated or dropped. Fileper-table tablespaces also support the Barracuda file format and associated features such as table compression, efficient off-page storage for long variable-length columns, and large index prefixes. For more information, see [Section 14.6.3.2, "File-Per-Table Tablespaces".](#page-51-0)

You can also store InnoDB tables in a shared general tablespace. General tablespaces support the Barracuda file format and can contain multiple tables. For more information, see [Section 14.6.3.3,](#page-53-0) ["General Tablespaces".](#page-53-0)

#### <span id="page-32-2"></span>**Converting an Existing Table**

To convert a non-InnoDB table to use InnoDB use ALTER TABLE:

ALTER TABLE table\_name ENGINE=InnoDB;

![](_page_33_Picture_1.jpeg)

#### **Warning**

Do not convert MySQL system tables in the mysql database from MyISAM to InnoDB tables. This is an unsupported operation. If you do this, MySQL does not restart until you restore the old system tables from a backup or regenerate them by reinitializing the data directory (see Section 2.9.1, "Initializing the Data Directory").

#### <span id="page-33-0"></span>**Cloning the Structure of a Table**

You might make an InnoDB table that is a clone of a MyISAM table, rather than using ALTER TABLE to perform conversion, to test the old and new table side-by-side before switching.

Create an empty InnoDB table with identical column and index definitions. Use SHOW CREATE TABLE table\_name\G to see the full CREATE TABLE statement to use. Change the ENGINE clause to ENGINE=INNODB.

#### <span id="page-33-1"></span>**Transferring Data**

To transfer a large volume of data into an empty InnoDB table created as shown in the previous section, insert the rows with INSERT INTO innodb\_table SELECT \* FROM myisam\_table ORDER BY primary\_key\_columns.

You can also create the indexes for the InnoDB table after inserting the data. Historically, creating new secondary indexes was a slow operation for InnoDB, but now you can create the indexes after the data is loaded with relatively little overhead from the index creation step.

If you have UNIQUE constraints on secondary keys, you can speed up a table import by turning off the uniqueness checks temporarily during the import operation:

```
SET unique_checks=0;
... import operation ...
SET unique_checks=1;
```

For big tables, this saves disk I/O because InnoDB can use its change buffer to write secondary index records as a batch. Be certain that the data contains no duplicate keys. unique\_checks permits but does not require storage engines to ignore duplicate keys.

For better control over the insertion process, you can insert big tables in pieces:

```
INSERT INTO newtable SELECT * FROM oldtable
 WHERE yourkey > something AND yourkey <= somethingelse;
```

After all records are inserted, you can rename the tables.

During the conversion of big tables, increase the size of the InnoDB buffer pool to reduce disk I/O. Typically, the recommended buffer pool size is 50 to 75 percent of system memory. You can also increase the size of InnoDB log files.

#### <span id="page-33-2"></span>**Storage Requirements**

If you intend to make several temporary copies of your data in InnoDB tables during the conversion process, it is recommended that you create the tables in file-per-table tablespaces so that you can reclaim the disk space when you drop the tables. When the innodb\_file\_per\_table configuration option is enabled (the default), newly created InnoDB tables are implicitly created in file-per-table tablespaces.

Whether you convert the MyISAM table directly or create a cloned InnoDB table, make sure that you have sufficient disk space to hold both the old and new tables during the process. **InnoDB tables require more disk space than MyISAM tables.** If an ALTER TABLE operation runs out of space, it starts a rollback, and that can take hours if it is disk-bound. For inserts, InnoDB uses the insert buffer to merge secondary index records to indexes in batches. That saves a lot of disk I/O. For rollback, no such mechanism is used, and the rollback can take 30 times longer than the insertion.

In the case of a runaway rollback, if you do not have valuable data in your database, it may be advisable to kill the database process rather than wait for millions of disk I/O operations to complete. For the complete procedure, see Section 14.22.2, "Forcing InnoDB Recovery".

#### <span id="page-34-0"></span>**Defining Primary Keys**

The PRIMARY KEY clause is a critical factor affecting the performance of MySQL queries and the space usage for tables and indexes. The primary key uniquely identifies a row in a table. Every row in the table should have a primary key value, and no two rows can have the same primary key value.

These are guidelines for the primary key, followed by more detailed explanations.

- Declare a PRIMARY KEY for each table. Typically, it is the most important column that you refer to in WHERE clauses when looking up a single row.
- Declare the PRIMARY KEY clause in the original CREATE TABLE statement, rather than adding it later through an ALTER TABLE statement.
- Choose the column and its data type carefully. Prefer numeric columns over character or string ones.
- Consider using an auto-increment column if there is not another stable, unique, non-null, numeric column to use.
- An auto-increment column is also a good choice if there is any doubt whether the value of the primary key column could ever change. Changing the value of a primary key column is an expensive operation, possibly involving rearranging data within the table and within each secondary index.

Consider adding a primary key to any table that does not already have one. Use the smallest practical numeric type based on the maximum projected size of the table. This can make each row slightly more compact, which can yield substantial space savings for large tables. The space savings are multiplied if the table has any secondary indexes, because the primary key value is repeated in each secondary index entry. In addition to reducing data size on disk, a small primary key also lets more data fit into the buffer pool, speeding up all kinds of operations and improving concurrency.

If the table already has a primary key on some longer column, such as a VARCHAR, consider adding a new unsigned AUTO\_INCREMENT column and switching the primary key to that, even if that column is not referenced in queries. This design change can produce substantial space savings in the secondary indexes. You can designate the former primary key columns as UNIQUE NOT NULL to enforce the same constraints as the PRIMARY KEY clause, that is, to prevent duplicate or null values across all those columns.

If you spread related information across multiple tables, typically each table uses the same column for its primary key. For example, a personnel database might have several tables, each with a primary key of employee number. A sales database might have some tables with a primary key of customer number, and other tables with a primary key of order number. Because lookups using the primary key are very fast, you can construct efficient join queries for such tables.

If you leave the PRIMARY KEY clause out entirely, MySQL creates an invisible one for you. It is a 6 byte value that might be longer than you need, thus wasting space. Because it is hidden, you cannot refer to it in queries.

## <span id="page-34-1"></span>**Application Performance Considerations**

The reliability and scalability features of InnoDB require more disk storage than equivalent MyISAM tables. You might change the column and index definitions slightly, for better space utilization, reduced I/O and memory consumption when processing result sets, and better query optimization plans making efficient use of index lookups.

If you set up a numeric ID column for the primary key, use that value to cross-reference with related values in any other tables, particularly for join queries. For example, rather than accepting a country name as input and doing queries searching for the same name, do one lookup to determine the country ID, then do other queries (or a single join query) to look up relevant information across several tables.

Rather than storing a customer or catalog item number as a string of digits, potentially using up several bytes, convert it to a numeric ID for storing and querying. A 4-byte unsigned INT column can index over 4 billion items (with the US meaning of billion: 1000 million). For the ranges of the different integer types, see Section 11.1.2, "Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT".

#### <span id="page-35-1"></span>**Understanding Files Associated with InnoDB Tables**

InnoDB files require more care and planning than MyISAM files do.

- You must not delete the ibdata files that represent the InnoDB system tablespace.
- Methods of moving or copying InnoDB tables to a different server are described in [Section 14.6.1.4,](#page-28-0) ["Moving or Copying InnoDB Tables".](#page-28-0)

# <span id="page-35-0"></span>**14.6.1.6 AUTO\_INCREMENT Handling in InnoDB**

InnoDB provides a configurable locking mechanism that can significantly improve scalability and performance of SQL statements that add rows to tables with AUTO\_INCREMENT columns. To use the AUTO\_INCREMENT mechanism with an InnoDB table, an AUTO\_INCREMENT column must be defined as the first or only column of some index such that it is possible to perform the equivalent of an indexed SELECT MAX(ai\_col) lookup on the table to obtain the maximum column value. The index is not required to be a PRIMARY KEY or UNIQUE, but to avoid duplicate values in the AUTO\_INCREMENT column, those index types are recommended.

This section describes the AUTO\_INCREMENT lock modes, usage implications of different AUTO\_INCREMENT lock mode settings, and how InnoDB initializes the AUTO\_INCREMENT counter.

- [InnoDB AUTO\\_INCREMENT Lock Modes](#page-35-2)
- [InnoDB AUTO\\_INCREMENT Lock Mode Usage Implications](#page-38-0)
- [InnoDB AUTO\\_INCREMENT Counter Initialization](#page-40-0)
- [Notes](#page-41-2)

#### <span id="page-35-2"></span>**InnoDB AUTO\_INCREMENT Lock Modes**

This section describes the AUTO\_INCREMENT lock modes used to generate auto-increment values, and how each lock mode affects replication. The auto-increment lock mode is configured at startup using the [innodb\\_autoinc\\_lock\\_mode](#page-191-0) variable.

The following terms are used in describing [innodb\\_autoinc\\_lock\\_mode](#page-191-0) settings:

• "INSERT-like" statements

All statements that generate new rows in a table, including INSERT, INSERT ... SELECT, REPLACE, REPLACE ... SELECT, and LOAD DATA. Includes "simple-inserts", "bulk-inserts", and "mixed-mode" inserts.

• "Simple inserts"

Statements for which the number of rows to be inserted can be determined in advance (when the statement is initially processed). This includes single-row and multiple-row INSERT and REPLACE statements that do not have a nested subquery, but not INSERT ... ON DUPLICATE KEY UPDATE.

• "Bulk inserts"

Statements for which the number of rows to be inserted (and the number of required autoincrement values) is not known in advance. This includes INSERT ... SELECT, REPLACE ... SELECT, and LOAD DATA statements, but not plain INSERT. InnoDB assigns new values for the AUTO\_INCREMENT column one at a time as each row is processed.

• "Mixed-mode inserts"

These are "simple insert" statements that specify the auto-increment value for some (but not all) of the new rows. An example follows, where c1 is an AUTO\_INCREMENT column of table t1:

```
INSERT INTO t1 (c1,c2) VALUES (1,'a'), (NULL,'b'), (5,'c'), (NULL,'d');
```

Another type of "mixed-mode insert" is INSERT ... ON DUPLICATE KEY UPDATE, which in the worst case is in effect an INSERT followed by a UPDATE, where the allocated value for the AUTO\_INCREMENT column may or may not be used during the update phase.

There are three possible settings for the [innodb\\_autoinc\\_lock\\_mode](#page-191-0) variable. The settings are 0, 1, or 2, for "traditional", "consecutive", or "interleaved" lock mode, respectively.

• innodb\_autoinc\_lock\_mode = 0 ("traditional" lock mode)

The traditional lock mode provides the same behavior that existed before the [innodb\\_autoinc\\_lock\\_mode](#page-191-0) variable was introduced. The traditional lock mode option is provided for backward compatibility, performance testing, and working around issues with "mixedmode inserts", due to possible differences in semantics.

In this lock mode, all "INSERT-like" statements obtain a special table-level AUTO-INC lock for inserts into tables with AUTO\_INCREMENT columns. This lock is normally held to the end of the statement (not to the end of the transaction) to ensure that auto-increment values are assigned in a predictable and repeatable order for a given sequence of INSERT statements, and to ensure that auto-increment values assigned by any given statement are consecutive.

In the case of statement-based replication, this means that when an SQL statement is replicated on a replica server, the same values are used for the auto-increment column as on the source server. The result of execution of multiple INSERT statements is deterministic, and the replica reproduces the same data as on the source. If auto-increment values generated by multiple INSERT statements were interleaved, the result of two concurrent INSERT statements would be nondeterministic, and could not reliably be propagated to a replica server using statement-based replication.

To make this clear, consider an example that uses this table:

```
CREATE TABLE t1 (
 c1 INT(11) NOT NULL AUTO_INCREMENT,
 c2 VARCHAR(10) DEFAULT NULL,
 PRIMARY KEY (c1)
) ENGINE=InnoDB;
```

Suppose that there are two transactions running, each inserting rows into a table with an AUTO\_INCREMENT column. One transaction is using an INSERT ... SELECT statement that inserts 1000 rows, and another is using a simple INSERT statement that inserts one row:

```
Tx1: INSERT INTO t1 (c2) SELECT 1000 rows from another table ...
Tx2: INSERT INTO t1 (c2) VALUES ('xxx');
```

InnoDB cannot tell in advance how many rows are retrieved from the SELECT in the INSERT statement in Tx1, and it assigns the auto-increment values one at a time as the statement proceeds. With a table-level lock, held to the end of the statement, only one INSERT statement referring to table t1 can execute at a time, and the generation of auto-increment numbers by different statements is not interleaved. The auto-increment values generated by the Tx1 INSERT ... SELECT statement are consecutive, and the (single) auto-increment value used by the INSERT statement in Tx2 is either smaller or larger than all those used for Tx1, depending on which statement executes first.

As long as the SQL statements execute in the same order when replayed from the binary log (when using statement-based replication, or in recovery scenarios), the results are the same as they were when Tx1 and Tx2 first ran. Thus, table-level locks held until the end of a statement make INSERT statements using auto-increment safe for use with statement-based replication. However, those

table-level locks limit concurrency and scalability when multiple transactions are executing insert statements at the same time.

In the preceding example, if there were no table-level lock, the value of the auto-increment column used for the INSERT in Tx2 depends on precisely when the statement executes. If the INSERT of Tx2 executes while the INSERT of Tx1 is running (rather than before it starts or after it completes), the specific auto-increment values assigned by the two INSERT statements are nondeterministic, and may vary from run to run.

Under the [consecutive](#page-37-0) lock mode, InnoDB can avoid using table-level AUTO-INC locks for "simple insert" statements where the number of rows is known in advance, and still preserve deterministic execution and safety for statement-based replication.

If you are not using the binary log to replay SQL statements as part of recovery or replication, the [interleaved](#page-37-1) lock mode can be used to eliminate all use of table-level AUTO-INC locks for even greater concurrency and performance, at the cost of permitting gaps in auto-increment numbers assigned by a statement and potentially having the numbers assigned by concurrently executing statements interleaved.

<span id="page-37-0"></span>• innodb\_autoinc\_lock\_mode = 1 ("consecutive" lock mode)

This is the default lock mode. In this mode, "bulk inserts" use the special AUTO-INC table-level lock and hold it until the end of the statement. This applies to all INSERT ... SELECT, REPLACE ... SELECT, and LOAD DATA statements. Only one statement holding the AUTO-INC lock can execute at a time. If the source table of the bulk insert operation is different from the target table, the AUTO-INC lock on the target table is taken after a shared lock is taken on the first row selected from the source table. If the source and target of the bulk insert operation are the same table, the AUTO-INC lock is taken after shared locks are taken on all selected rows.

"Simple inserts" (for which the number of rows to be inserted is known in advance) avoid table-level AUTO-INC locks by obtaining the required number of auto-increment values under the control of a mutex (a light-weight lock) that is only held for the duration of the allocation process, not until the statement completes. No table-level AUTO-INC lock is used unless an AUTO-INC lock is held by another transaction. If another transaction holds an AUTO-INC lock, a "simple insert" waits for the AUTO-INC lock, as if it were a "bulk insert".

This lock mode ensures that, in the presence of INSERT statements where the number of rows is not known in advance (and where auto-increment numbers are assigned as the statement progresses), all auto-increment values assigned by any "INSERT-like" statement are consecutive, and operations are safe for statement-based replication.

Simply put, this lock mode significantly improves scalability while being safe for use with statementbased replication. Further, as with "traditional" lock mode, auto-increment numbers assigned by any given statement are consecutive. There is no change in semantics compared to "traditional" mode for any statement that uses auto-increment, with one important exception.

The exception is for "mixed-mode inserts", where the user provides explicit values for an AUTO\_INCREMENT column for some, but not all, rows in a multiple-row "simple insert". For such inserts, InnoDB allocates more auto-increment values than the number of rows to be inserted. However, all values automatically assigned are consecutively generated (and thus higher than) the auto-increment value generated by the most recently executed previous statement. "Excess" numbers are lost.

<span id="page-37-1"></span>• innodb\_autoinc\_lock\_mode = 2 ("interleaved" lock mode)

In this lock mode, no "INSERT-like" statements use the table-level AUTO-INC lock, and multiple statements can execute at the same time. This is the fastest and most scalable lock mode, but it is not safe when using statement-based replication or recovery scenarios when SQL statements are replayed from the binary log.

In this lock mode, auto-increment values are guaranteed to be unique and monotonically increasing across all concurrently executing "INSERT-like" statements. However, because multiple statements can be generating numbers at the same time (that is, allocation of numbers is interleaved across statements), the values generated for the rows inserted by any given statement may not be consecutive.

If the only statements executing are "simple inserts" where the number of rows to be inserted is known ahead of time, there are no gaps in the numbers generated for a single statement, except for "mixed-mode inserts". However, when "bulk inserts" are executed, there may be gaps in the autoincrement values assigned by any given statement.

### <span id="page-38-0"></span>**InnoDB AUTO\_INCREMENT Lock Mode Usage Implications**

• Using auto-increment with replication

If you are using statement-based replication, set [innodb\\_autoinc\\_lock\\_mode](#page-191-0) to 0 or 1 and use the same value on the source and its replicas. Auto-increment values are not ensured to be the same on the replicas as on the source if you use [innodb\\_autoinc\\_lock\\_mode](#page-191-0) = 2 ("interleaved") or configurations where the source and replicas do not use the same lock mode.

If you are using row-based or mixed-format replication, all of the auto-increment lock modes are safe, since row-based replication is not sensitive to the order of execution of the SQL statements (and the mixed format uses row-based replication for any statements that are unsafe for statement-based replication).

• "Lost" auto-increment values and sequence gaps

In all lock modes (0, 1, and 2), if a transaction that generated auto-increment values rolls back, those auto-increment values are "lost". Once a value is generated for an auto-increment column, it cannot be rolled back, whether or not the "INSERT-like" statement is completed, and whether or not the containing transaction is rolled back. Such lost values are not reused. Thus, there may be gaps in the values stored in an AUTO\_INCREMENT column of a table.

• Specifying NULL or 0 for the AUTO\_INCREMENT column

In all lock modes (0, 1, and 2), if a user specifies NULL or 0 for the AUTO\_INCREMENT column in an INSERT, InnoDB treats the row as if the value was not specified and generates a new value for it.

• Assigning a negative value to the AUTO\_INCREMENT column

In all lock modes (0, 1, and 2), the behavior of the auto-increment mechanism is undefined if you assign a negative value to the AUTO\_INCREMENT column.

• If the AUTO\_INCREMENT value becomes larger than the maximum integer for the specified integer type

In all lock modes (0, 1, and 2), the behavior of the auto-increment mechanism is undefined if the value becomes larger than the maximum integer that can be stored in the specified integer type.

• Gaps in auto-increment values for "bulk inserts"

With [innodb\\_autoinc\\_lock\\_mode](#page-191-0) set to 0 ("traditional") or 1 ("consecutive"), the auto-increment values generated by any given statement are consecutive, without gaps, because the table-level AUTO-INC lock is held until the end of the statement, and only one such statement can execute at a time.

With [innodb\\_autoinc\\_lock\\_mode](#page-191-0) set to 2 ("interleaved"), there may be gaps in the autoincrement values generated by "bulk inserts," but only if there are concurrently executing "INSERTlike" statements.

For lock modes 1 or 2, gaps may occur between successive statements because for bulk inserts the exact number of auto-increment values required by each statement may not be known and overestimation is possible.

• Auto-increment values assigned by "mixed-mode inserts"

Consider a "mixed-mode insert," where a "simple insert" specifies the auto-increment value for some (but not all) resulting rows. Such a statement behaves differently in lock modes 0, 1, and 2. For example, assume c1 is an AUTO\_INCREMENT column of table t1, and that the most recent automatically generated sequence number is 100.

```
mysql> CREATE TABLE t1 (
 -> c1 INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
 -> c2 CHAR(1)
 -> ) ENGINE = INNODB;
```

Now, consider the following "mixed-mode insert" statement:

```
mysql> INSERT INTO t1 (c1,c2) VALUES (1,'a'), (NULL,'b'), (5,'c'), (NULL,'d');
```

With [innodb\\_autoinc\\_lock\\_mode](#page-191-0) set to 0 ("traditional"), the four new rows are:

```
mysql> SELECT c1, c2 FROM t1 ORDER BY c2;
+-----+------+
| c1 | c2 |
+-----+------+
| 1 | a |
| 101 | b |
| 5 | c |
| 102 | d |
+-----+------+
```

The next available auto-increment value is 103 because the auto-increment values are allocated one at a time, not all at once at the beginning of statement execution. This result is true whether or not there are concurrently executing "INSERT-like" statements (of any type).

With [innodb\\_autoinc\\_lock\\_mode](#page-191-0) set to 1 ("consecutive"), the four new rows are also:

```
mysql> SELECT c1, c2 FROM t1 ORDER BY c2;
+-----+------+
| c1 | c2 |
+-----+------+
| 1 | a |
| 101 | b |
| 5 | c |
| 102 | d |
+-----+------+
```

However, in this case, the next available auto-increment value is 105, not 103 because four autoincrement values are allocated at the time the statement is processed, but only two are used. This result is true whether or not there are concurrently executing "INSERT-like" statements (of any type).

With [innodb\\_autoinc\\_lock\\_mode](#page-191-0) set to 2 ("interleaved"), the four new rows are:

```
mysql> SELECT c1, c2 FROM t1 ORDER BY c2;
+-----+------+
| c1 | c2 |
+-----+------+
| 1 | a |
| x | b |
| 5 | c |
| y | d |
```

+-----+------+

The values of x and y are unique and larger than any previously generated rows. However, the specific values of x and y depend on the number of auto-increment values generated by concurrently executing statements.

Finally, consider the following statement, issued when the most-recently generated sequence number is 100:

```
mysql> INSERT INTO t1 (c1,c2) VALUES (1,'a'), (NULL,'b'), (101,'c'), (NULL,'d');
```

With any [innodb\\_autoinc\\_lock\\_mode](#page-191-0) setting, this statement generates a duplicate-key error 23000 (Can't write; duplicate key in table) because 101 is allocated for the row (NULL, 'b') and insertion of the row (101, 'c') fails.

• Modifying AUTO\_INCREMENT column values in the middle of a sequence of INSERT statements

In all lock modes (0, 1, and 2), modifying an AUTO\_INCREMENT column value in the middle of a sequence of INSERT statements could lead to "Duplicate entry" errors. For example, if you perform an UPDATE operation that changes an AUTO\_INCREMENT column value to a value larger than the current maximum auto-increment value, subsequent INSERT operations that do not specify an unused auto-increment value could encounter "Duplicate entry" errors. This behavior is demonstrated in the following example.

```
mysql> CREATE TABLE t1 (
 -> c1 INT NOT NULL AUTO_INCREMENT,
 -> PRIMARY KEY (c1)
 -> ) ENGINE = InnoDB;
mysql> INSERT INTO t1 VALUES(0), (0), (3);
mysql> SELECT c1 FROM t1;
+----+
| c1 |
+----+
| 1 |
| 2 |
| 3 |
+----+
mysql> UPDATE t1 SET c1 = 4 WHERE c1 = 1;
mysql> SELECT c1 FROM t1;
+----+
| c1 |
+----+
| 2 |
| 3 |
| 4 |
+----+
mysql> INSERT INTO t1 VALUES(0);
ERROR 1062 (23000): Duplicate entry '4' for key 'PRIMARY'
```

## <span id="page-40-0"></span>**InnoDB AUTO\_INCREMENT Counter Initialization**

This section describes how InnoDB initializes AUTO\_INCREMENT counters.

If you specify an AUTO\_INCREMENT column for an InnoDB table, the table handle in the InnoDB data dictionary contains a special counter called the auto-increment counter that is used in assigning new values for the column. This counter is stored only in main memory, not on disk.

To initialize an auto-increment counter after a server restart, InnoDB executes the equivalent of the following statement on the first insert into a table containing an AUTO\_INCREMENT column.

```
SELECT MAX(ai_col) FROM table_name FOR UPDATE;
```

InnoDB increments the value retrieved by the statement and assigns it to the column and to the auto-increment counter for the table. By default, the value is incremented by 1. This default can be overridden by the auto\_increment\_increment configuration setting.

If the table is empty, InnoDB uses the value 1. This default can be overridden by the auto\_increment\_offset configuration setting.

If a SHOW TABLE STATUS statement examines the table before the auto-increment counter is initialized, InnoDB initializes but does not increment the value. The value is stored for use by later inserts. This initialization uses a normal exclusive-locking read on the table and the lock lasts to the end of the transaction. InnoDB follows the same procedure for initializing the auto-increment counter for a newly created table.

After the auto-increment counter has been initialized, if you do not explicitly specify a value for an AUTO\_INCREMENT column, InnoDB increments the counter and assigns the new value to the column. If you insert a row that explicitly specifies the column value, and the value is greater than the current counter value, the counter is set to the specified column value.

InnoDB uses the in-memory auto-increment counter as long as the server runs. When the server is stopped and restarted, InnoDB reinitializes the counter for each table for the first INSERT to the table, as described earlier.

A server restart also cancels the effect of the AUTO\_INCREMENT = N table option in CREATE TABLE and ALTER TABLE statements, which you can use with InnoDB tables to set the initial counter value or alter the current counter value.

#### <span id="page-41-2"></span>**Notes**

- When an AUTO\_INCREMENT integer column runs out of values, a subsequent INSERT operation returns a duplicate-key error. This is general MySQL behavior.
- When you restart the MySQL server, InnoDB may reuse an old value that was generated for an AUTO\_INCREMENT column but never stored (that is, a value that was generated during an old transaction that was rolled back).

# <span id="page-41-0"></span>**14.6.2 Indexes**

This section covers topics related to InnoDB indexes.

# <span id="page-41-1"></span>**14.6.2.1 Clustered and Secondary Indexes**

Each InnoDB table has a special index called the clustered index that stores row data. Typically, the clustered index is synonymous with the primary key. To get the best performance from queries, inserts, and other database operations, it is important to understand how InnoDB uses the clustered index to optimize the common lookup and DML operations.

- When you define a PRIMARY KEY on a table, InnoDB uses it as the clustered index. A primary key should be defined for each table. If there is no logical unique and non-null column or set of columns to use a the primary key, add an auto-increment column. Auto-increment column values are unique and are added automatically as new rows are inserted.
- If you do not define a PRIMARY KEY for a table, InnoDB uses the first UNIQUE index with all key columns defined as NOT NULL as the clustered index.
- If a table has no PRIMARY KEY or suitable UNIQUE index, InnoDB generates a hidden clustered index named GEN\_CLUST\_INDEX on a synthetic column that contains row ID values. The rows are ordered by the row ID that InnoDB assigns. The row ID is a 6-byte field that increases monotonically as new rows are inserted. Thus, the rows ordered by the row ID are physically in order of insertion.

#### **How the Clustered Index Speeds Up Queries**

Accessing a row through the clustered index is fast because the index search leads directly to the page that contains the row data. If a table is large, the clustered index architecture often saves a disk I/O

operation when compared to storage organizations that store row data using a different page from the index record.

#### **How Secondary Indexes Relate to the Clustered Index**

Indexes other than the clustered index are known as secondary indexes. In InnoDB, each record in a secondary index contains the primary key columns for the row, as well as the columns specified for the secondary index. InnoDB uses this primary key value to search for the row in the clustered index.

If the primary key is long, the secondary indexes use more space, so it is advantageous to have a short primary key.

For guidelines to take advantage of InnoDB clustered and secondary indexes, see Section 8.3, "Optimization and Indexes".