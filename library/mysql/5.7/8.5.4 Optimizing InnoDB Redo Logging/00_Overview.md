---
source: MySQL 5.7 Reference
title: 00_Overview
---

Consider the following guidelines for optimizing redo logging:

• Make your redo log files big, even as big as the buffer pool. When InnoDB has written the redo log files full, it must write the modified contents of the buffer pool to disk in a checkpoint. Small redo log files cause many unnecessary disk writes. Although historically big redo log files caused lengthy recovery times, recovery is now much faster and you can confidently use large redo log files.

The size and number of redo log files are configured using the innodb\_log\_file\_size and innodb\_log\_files\_in\_group configuration options. For information about modifying an existing redo log file configuration, see Changing the Number or Size of InnoDB Redo Log Files.

- Consider increasing the size of the log buffer. A large log buffer enables large transactions to run without a need to write the log to disk before the transactions commit. Thus, if you have transactions that update, insert, or delete many rows, making the log buffer larger saves disk I/O. Log buffer size is configured using the innodb\_log\_buffer\_size configuration option.
- Configure the innodb\_log\_write\_ahead\_size configuration option to avoid "read-on-write". This option defines the write-ahead block size for the redo log. Set innodb\_log\_write\_ahead\_size to match the operating system or file system cache block size. Read-on-write occurs when redo log blocks are not entirely cached to the operating system or file system due to a mismatch between write-ahead block size for the redo log and operating system or file system cache block size.

Valid values for innodb\_log\_write\_ahead\_size are multiples of the InnoDB log file block size (2<sup>n</sup> ). The minimum value is the InnoDB log file block size (512). Write-ahead does not occur when the minimum value is specified. The maximum value is equal to the innodb\_page\_size value. If you specify a value for innodb\_log\_write\_ahead\_size that is larger than the innodb\_page\_size value, the innodb\_log\_write\_ahead\_size setting is truncated to the innodb\_page\_size value.

Setting the innodb\_log\_write\_ahead\_size value too low in relation to the operating system or file system cache block size results in read-on-write. Setting the value too high may have a slight impact on fsync performance for log file writes due to several blocks being written at once.

# <span id="page-57-0"></span>**8.5.5 Bulk Data Loading for InnoDB Tables**

These performance tips supplement the general guidelines for fast inserts in [Section 8.2.4.1,](#page-28-0) ["Optimizing INSERT Statements".](#page-28-0)

• When importing data into InnoDB, turn off autocommit mode, because it performs a log flush to disk for every insert. To disable autocommit during your import operation, surround it with SET autocommit and COMMIT statements:

```
SET autocommit=0;
... SQL import statements ...
COMMIT;
```

The mysqldump option --opt creates dump files that are fast to import into an InnoDB table, even without wrapping them with the SET autocommit and COMMIT statements.

• If you have UNIQUE constraints on secondary keys, you can speed up table imports by temporarily turning off the uniqueness checks during the import session:

```
SET unique_checks=0;
... SQL import statements ...
SET unique_checks=1;
```

For big tables, this saves a lot of disk I/O because InnoDB can use its change buffer to write secondary index records in a batch. Be certain that the data contains no duplicate keys.

• If you have FOREIGN KEY constraints in your tables, you can speed up table imports by turning off the foreign key checks for the duration of the import session:

```
SET foreign_key_checks=0;
... SQL import statements ...
SET foreign_key_checks=1;
```

For big tables, this can save a lot of disk I/O.

• Use the multiple-row INSERT syntax to reduce communication overhead between the client and the server if you need to insert many rows:

```
INSERT INTO yourtable VALUES (1,2), (5,5), ...;
```

This tip is valid for inserts into any table, not just InnoDB tables.

- When doing bulk inserts into tables with auto-increment columns, set innodb\_autoinc\_lock\_mode to 2 instead of the default value 1. See Section 14.6.1.6, "AUTO\_INCREMENT Handling in InnoDB" for details.
- When performing bulk inserts, it is faster to insert rows in PRIMARY KEY order. InnoDB tables use a clustered index, which makes it relatively fast to use data in the order of the PRIMARY KEY. Performing bulk inserts in PRIMARY KEY order is particularly important for tables that do not fit entirely within the buffer pool.
- For optimal performance when loading data into an InnoDB FULLTEXT index, follow this set of steps:
  - 1. Define a column FTS\_DOC\_ID at table creation time, of type BIGINT UNSIGNED NOT NULL, with a unique index named FTS\_DOC\_ID\_INDEX. For example:

```
CREATE TABLE t1 (
FTS_DOC_ID BIGINT unsigned NOT NULL AUTO_INCREMENT,
title varchar(255) NOT NULL DEFAULT '',
text mediumtext NOT NULL,
PRIMARY KEY (`FTS_DOC_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE UNIQUE INDEX FTS_DOC_ID_INDEX on t1(FTS_DOC_ID);
```

- 2. Load the data into the table.
- 3. Create the FULLTEXT index after the data is loaded.

![](_page_58_Picture_14.jpeg)

## **Note**

When adding FTS\_DOC\_ID column at table creation time, ensure that the FTS\_DOC\_ID column is updated when the FULLTEXT indexed column is updated, as the FTS\_DOC\_ID must increase monotonically with each INSERT or UPDATE. If you choose not to add the FTS\_DOC\_ID at table creation time and have InnoDB manage DOC IDs for you, InnoDB adds the FTS\_DOC\_ID as a hidden column with the next CREATE FULLTEXT INDEX call. This approach, however, requires a table rebuild which can impact performance.