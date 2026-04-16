---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes restrictions and limitations of the InnoDB storage engine.

• You cannot create a table with a column name that matches the name of an internal InnoDB column (including DB\_ROW\_ID, DB\_TRX\_ID, and DB\_ROLL\_PTR. This restriction applies to use of the names in any lettercase.

```
mysql> CREATE TABLE t1 (c1 INT, db_row_id INT) ENGINE=INNODB;
ERROR 1166 (42000): Incorrect column name 'db_row_id'
```

- SHOW TABLE STATUS does not provide accurate statistics for InnoDB tables except for the physical size reserved by the table. The row count is only a rough estimate used in SQL optimization.
- InnoDB does not keep an internal count of rows in a table because concurrent transactions might "see" different numbers of rows at the same time. Consequently, SELECT COUNT(\*) statements only count rows visible to the current transaction.

For information about how InnoDB processes SELECT COUNT(\*) statements, refer to the COUNT() description in Section 14.19.1, "Aggregate Function Descriptions".

- ROW\_FORMAT=COMPRESSED is unsupported for page sizes greater than 16KB.
- A MySQL instance using a particular InnoDB page size ([innodb\\_page\\_size](#page-52-0)) cannot use data files or log files from an instance that uses a different page size.
- For limitations associated with importing tables using the Transportable Tablespaces feature, see Table Import Limitations.
- For limitations associated with online DDL, see Section 17.12.8, "Online DDL Limitations".
- For limitations associated with general tablespaces, see General Tablespace Limitations.
- For limitations associated with data-at-rest encryption, see Encryption Limitations.

# Chapter 18 Alternative Storage Engines

# **Table of Contents**

| 18.1 Setting the Storage Engine 3544                     |      |
|----------------------------------------------------------|------|
| 18.2 The MyISAM Storage Engine 3545                      |      |
| 18.2.1 MyISAM Startup Options 3548                       |      |
| 18.2.2 Space Needed for Keys 3549                        |      |
| 18.2.3 MyISAM Table Storage Formats 3549                 |      |
| 18.2.4 MyISAM Table Problems 3552                        |      |
| 18.3 The MEMORY Storage Engine 3553                      |      |
| 18.4 The CSV Storage Engine                              | 3558 |
| 18.4.1 Repairing and Checking CSV Tables 3558            |      |
| 18.4.2 CSV Limitations 3559                              |      |
| 18.5 The ARCHIVE Storage Engine 3559                     |      |
| 18.6 The BLACKHOLE Storage Engine                        | 3561 |
| 18.7 The MERGE Storage Engine 3563                       |      |
| 18.7.1 MERGE Table Advantages and Disadvantages 3565     |      |
| 18.7.2 MERGE Table Problems 3566                         |      |
| 18.8 The FEDERATED Storage Engine 3568                   |      |
| 18.8.1 FEDERATED Storage Engine Overview 3568            |      |
| 18.8.2 How to Create FEDERATED Tables 3569               |      |
| 18.8.3 FEDERATED Storage Engine Notes and Tips 3572      |      |
| 18.8.4 FEDERATED Storage Engine Resources 3573           |      |
| 18.9 The EXAMPLE Storage Engine 3573                     |      |
| 18.10 Other Storage Engines 3574                         |      |
| 18.11 Overview of MySQL Storage Engine Architecture 3574 |      |
| 18.11.1 Pluggable Storage Engine Architecture 3575       |      |
| 18.11.2 The Common Database Server Layer 3575            |      |

Storage engines are MySQL components that handle the SQL operations for different table types. InnoDB is the default and most general-purpose storage engine, and Oracle recommends using it for tables except for specialized use cases. (The CREATE TABLE statement in MySQL 8.0 creates InnoDB tables by default.)

MySQL Server uses a pluggable storage engine architecture that enables storage engines to be loaded into and unloaded from a running MySQL server.

To determine which storage engines your server supports, use the SHOW ENGINES statement. The value in the Support column indicates whether an engine can be used. A value of YES, NO, or DEFAULT indicates that an engine is available, not available, or available and currently set as the default storage engine.

```
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
 Engine: PERFORMANCE_SCHEMA
 Support: YES
 Comment: Performance Schema
Transactions: NO
 XA: NO
 Savepoints: NO
*************************** 2. row ***************************
 Engine: InnoDB
 Support: DEFAULT
 Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
 XA: YES
```

```
Savepoints: YES
                ******* 3. row *************
    Engine: MRG MYISAM
    Support: YES
   Comment: Collection of identical MyISAM tables
Transactions: NO
        XA: NO
 Savepoints: NO
               ****** 4. row **************
    Engine: BLACKHOLE
    Support: YES
   Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
        YZ · NO
 Savepoints: NO
                  ****** 5. row ***************
    Engine: MyISAM
    Support: YES
   Comment: MyISAM storage engine
Transactions: NO
        XA: NO
 Savepoints: NO
```

This chapter covers use cases for special-purpose MySQL storage engines. It does not cover the default InnoDB storage engine or the NDB storage engine which are covered in Chapter 17, *The InnoDB Storage Engine* and Chapter 25, *MySQL NDB Cluster 8.0*. For advanced users, it also contains a description of the pluggable storage engine architecture (see Section 18.11, "Overview of MySQL Storage Engine Architecture").

For information about features offered in commercial MySQL Server binaries, see *MySQL Editions*, on the MySQL website. The storage engines available might depend on which edition of MySQL you are using.

For answers to commonly asked questions about MySQL storage engines, see Section A.2, "MySQL 8.0 FAQ: Storage Engines".

# **MySQL 8.0 Supported Storage Engines**

- InnoDB: The default storage engine in MySQL 8.0. InnoDB is a transaction-safe (ACID compliant) storage engine for MySQL that has commit, rollback, and crash-recovery capabilities to protect user data. InnoDB row-level locking (without escalation to coarser granularity locks) and Oracle-style consistent nonlocking reads increase multi-user concurrency and performance. InnoDB stores user data in clustered indexes to reduce I/O for common queries based on primary keys. To maintain data integrity, InnoDB also supports FOREIGN KEY referential-integrity constraints. For more information about InnoDB, see Chapter 17, The InnoDB Storage Engine.
- MyISAM: These tables have a small footprint. Table-level locking limits the performance in read/write workloads, so it is often used in read-only or read-mostly workloads in Web and data warehousing configurations.
- Memory: Stores all data in RAM, for fast access in environments that require quick lookups of non-critical data. This engine was formerly known as the HEAP engine. Its use cases are decreasing;
   InnoDB with its buffer pool memory area provides a general-purpose and durable way to keep most or all data in memory, and NDBCLUSTER provides fast key-value lookups for huge distributed data sets.
- CSV: Its tables are really text files with comma-separated values. CSV tables let you import or dump data in CSV format, to exchange data with scripts and applications that read and write that same format. Because CSV tables are not indexed, you typically keep the data in InnobB tables during normal operation, and only use CSV tables during the import or export stage.
- Archive: These compact, unindexed tables are intended for storing and retrieving large amounts of seldom-referenced historical, archived, or security audit information.

- [Blackhole](#page-190-0): The Blackhole storage engine accepts but does not store data, similar to the Unix / dev/null device. Queries always return an empty set. These tables can be used in replication configurations where DML statements are sent to replica servers, but the source server does not keep its own copy of the data.
- NDB (also known as NDBCLUSTER): This clustered database engine is particularly suited for applications that require the highest possible degree of uptime and availability.
- [Merge](#page-192-0): Enables a MySQL DBA or developer to logically group a series of identical MyISAM tables and reference them as one object. Good for VLDB environments such as data warehousing.
- [Federated](#page-197-0): Offers the ability to link separate MySQL servers to create one logical database from many physical servers. Very good for distributed or data mart environments.
- Example: This engine serves as an example in the MySQL source code that illustrates how to begin writing new storage engines. It is primarily of interest to developers. The storage engine is a "stub" that does nothing. You can create tables with this engine, but no data can be stored in them or retrieved from them.

You are not restricted to using the same storage engine for an entire server or schema. You can specify the storage engine for any table. For example, an application might use mostly InnoDB tables, with one CSV table for exporting data to a spreadsheet and a few MEMORY tables for temporary workspaces.

## **Choosing a Storage Engine**

The various storage engines provided with MySQL are designed with different use cases in mind. The following table provides an overview of some storage engines provided with MySQL, with clarifying notes following the table.

**Table 18.1 Storage Engines Feature Summary**

| Feature                                      | MyISAM       | Memory       | InnoDB       | Archive      | NDB          |
|----------------------------------------------|--------------|--------------|--------------|--------------|--------------|
| B-tree indexes                               | Yes          | Yes          | Yes          | No           | No           |
| Backup/point<br>in-time recovery<br>(note 1) | Yes          | Yes          | Yes          | Yes          | Yes          |
| Cluster<br>database<br>support               | No           | No           | No           | No           | Yes          |
| Clustered<br>indexes                         | No           | No           | Yes          | No           | No           |
| Compressed<br>data                           | Yes (note 2) | No           | Yes          | Yes          | No           |
| Data caches                                  | No           | N/A          | Yes          | No           | Yes          |
| Encrypted data                               | Yes (note 3) | Yes (note 3) | Yes (note 4) | Yes (note 3) | Yes (note 5) |
| Foreign key<br>support                       | No           | No           | Yes          | No           | Yes          |
| Full-text search<br>indexes                  | Yes          | No           | Yes (note 6) | No           | No           |
| Geospatial data<br>type support              | Yes          | No           | Yes          | Yes          | Yes          |
| Geospatial<br>indexing<br>support            | Yes          | No           | Yes (note 7) | No           | No           |

| Feature                                     | MyISAM | Memory           | InnoDB      | Archive | NDB   |
|---------------------------------------------|--------|------------------|-------------|---------|-------|
| Hash indexes                                | No     | Yes              | No (note 8) | No      | Yes   |
| Index caches                                | Yes    | N/A              | Yes         | No      | Yes   |
| Locking<br>granularity                      | Table  | Table            | Row         | Row     | Row   |
| MVCC                                        | No     | No               | Yes         | No      | No    |
| Replication<br>support (note 1)             | Yes    | Limited (note 9) | Yes         | Yes     | Yes   |
| Storage limits                              | 256TB  | RAM              | 64TB        | None    | 384EB |
| T-tree indexes                              | No     | No               | No          | No      | Yes   |
| Transactions                                | No     | No               | Yes         | No      | Yes   |
| Update<br>statistics for<br>data dictionary | Yes    | Yes              | Yes         | Yes     | Yes   |

#### **Notes:**

- 1. Implemented in the server, rather than in the storage engine.
- 2. Compressed MyISAM tables are supported only when using the compressed row format. Tables using the compressed row format with MyISAM are read only.
- 3. Implemented in the server via encryption functions.
- 4. Implemented in the server via encryption functions; In MySQL 5.7 and later, data-at-rest encryption is supported.
- 5. Implemented in the server via encryption functions; encrypted NDB backups as of NDB 8.0.22; transparent NDB file system encryption supported in NDB 8.0.29 and later.
- 6. Support for FULLTEXT indexes is available in MySQL 5.6 and later.
- 7. Support for geospatial indexing is available in MySQL 5.7 and later.
- 8. InnoDB utilizes hash indexes internally for its Adaptive Hash Index feature.
- 9. See the discussion later in this section.

# <span id="page-173-0"></span>**18.1 Setting the Storage Engine**

When you create a new table, you can specify which storage engine to use by adding an ENGINE table option to the CREATE TABLE statement:

```
-- ENGINE=INNODB not needed unless you have set a different
-- default storage engine.
CREATE TABLE t1 (i INT) ENGINE = INNODB;
-- Simple table definitions can be switched from one to another.
CREATE TABLE t2 (i INT) ENGINE = CSV;
CREATE TABLE t3 (i INT) ENGINE = MEMORY;
```

When you omit the ENGINE option, the default storage engine is used. The default engine is InnoDB in MySQL 8.0. You can specify the default engine by using the --default-storage-engine server startup option, or by setting the default-storage-engine option in the my.cnf configuration file.

You can set the default storage engine for the current session by setting the default\_storage\_engine variable:

```
SET default_storage_engine=NDBCLUSTER;
```

The storage engine for TEMPORARY tables created with CREATE TEMPORARY TABLE can be set separately from the engine for permanent tables by setting the default\_tmp\_storage\_engine, either at startup or at runtime.

To convert a table from one storage engine to another, use an ALTER TABLE statement that indicates the new engine:

```
ALTER TABLE t ENGINE = InnoDB;
```

See Section 15.1.20, "CREATE TABLE Statement", and Section 15.1.9, "ALTER TABLE Statement".

If you try to use a storage engine that is not compiled in or that is compiled in but deactivated, MySQL instead creates a table using the default storage engine. For example, in a replication setup, perhaps your source server uses InnoDB tables for maximum safety, but the replica servers use other storage engines for speed at the expense of durability or concurrency.

By default, a warning is generated whenever CREATE TABLE or ALTER TABLE cannot use the default storage engine. To prevent confusing, unintended behavior if the desired engine is unavailable, enable the NO\_ENGINE\_SUBSTITUTION SQL mode. If the desired engine is unavailable, this setting produces an error instead of a warning, and the table is not created or altered. See Section 7.1.11, "Server SQL Modes".

MySQL may store a table's index and data in one or more other files, depending on the storage engine. Table and column definitions are stored in the MySQL data dictionary. Individual storage engines create any additional files required for the tables that they manage. If a table name contains special characters, the names for the table files contain encoded versions of those characters as described in Section 11.2.4, "Mapping of Identifiers to File Names".

# <span id="page-174-0"></span>**18.2 The MyISAM Storage Engine**

MyISAM is based on the older (and no longer available) ISAM storage engine but has many useful extensions.

**Table 18.2 MyISAM Storage Engine Features**

| Feature                                                                                          | Support                                                                                                                                                            |
|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| B-tree indexes                                                                                   | Yes                                                                                                                                                                |
| Backup/point-in-time recovery (Implemented in<br>the server, rather than in the storage engine.) | Yes                                                                                                                                                                |
| Cluster database support                                                                         | No                                                                                                                                                                 |
| Clustered indexes                                                                                | No                                                                                                                                                                 |
| Compressed data                                                                                  | Yes (Compressed MyISAM tables are supported<br>only when using the compressed row format.<br>Tables using the compressed row format with<br>MyISAM are read only.) |
| Data caches                                                                                      | No                                                                                                                                                                 |
| Encrypted data                                                                                   | Yes (Implemented in the server via encryption<br>functions.)                                                                                                       |
| Foreign key support                                                                              | No                                                                                                                                                                 |
| Full-text search indexes                                                                         | Yes                                                                                                                                                                |
| Geospatial data type support                                                                     | Yes                                                                                                                                                                |
| Geospatial indexing support                                                                      | Yes                                                                                                                                                                |
| Hash indexes                                                                                     | No                                                                                                                                                                 |

| Feature                                                                                | Support |
|----------------------------------------------------------------------------------------|---------|
| Index caches                                                                           | Yes     |
| Locking granularity                                                                    | Table   |
| MVCC                                                                                   | No      |
| Replication support (Implemented in the server,<br>rather than in the storage engine.) | Yes     |
| Storage limits                                                                         | 256TB   |
| T-tree indexes                                                                         | No      |
| Transactions                                                                           | No      |
| Update statistics for data dictionary                                                  | Yes     |

Each MyISAM table is stored on disk in two files. The files have names that begin with the table name and have an extension to indicate the file type. The data file has an .MYD (MYData) extension. The index file has an .MYI (MYIndex) extension. The table definition is stored in the MySQL data dictionary.

To specify explicitly that you want a MyISAM table, indicate that with an ENGINE table option:

```
CREATE TABLE t (i INT) ENGINE = MYISAM;
```

In MySQL 8.0, it is normally necessary to use ENGINE to specify the MyISAM storage engine because InnoDB is the default engine.

You can check or repair MyISAM tables with the mysqlcheck client or myisamchk utility. You can also compress MyISAM tables with myisampack to take up much less space. See Section 6.5.3, "mysqlcheck — A Table Maintenance Program", Section 6.6.4, "myisamchk — MyISAM Table-Maintenance Utility", and Section 6.6.6, "myisampack — Generate Compressed, Read-Only MyISAM Tables".

In MySQL 8.0, the MyISAM storage engine provides no partitioning support. Partitioned MyISAM tables created in previous versions of MySQL cannot be used in MySQL 8.0. For more information, see Section 26.6.2, "Partitioning Limitations Relating to Storage Engines". For help with upgrading such tables so that they can be used in MySQL 8.0, see Section 3.5, "Changes in MySQL 8.0".

MyISAM tables have the following characteristics:

• All data values are stored with the low byte first. This makes the data machine and operating system independent. The only requirements for binary portability are that the machine uses two'scomplement signed integers and IEEE floating-point format. These requirements are widely used among mainstream machines. Binary compatibility might not be applicable to embedded systems, which sometimes have peculiar processors.

There is no significant speed penalty for storing data low byte first; the bytes in a table row normally are unaligned and it takes little more processing to read an unaligned byte in order than in reverse order. Also, the code in the server that fetches column values is not time critical compared to other code.

- All numeric key values are stored with the high byte first to permit better index compression.
- Large files (up to 63-bit file length) are supported on file systems and operating systems that support large files.
- There is a limit of (232) 2 (1.844E+19) rows in a MyISAM table.
- The maximum number of indexes per MyISAM table is 64.

The maximum number of columns per index is 16.

- The maximum key length is 1000 bytes. This can also be changed by changing the source and recompiling. For the case of a key longer than 250 bytes, a larger key block size than the default of 1024 bytes is used.
- When rows are inserted in sorted order (as when you are using an AUTO\_INCREMENT column), the index tree is split so that the high node only contains one key. This improves space utilization in the index tree.
- Internal handling of one AUTO\_INCREMENT column per table is supported. MyISAM automatically updates this column for INSERT and UPDATE operations. This makes AUTO\_INCREMENT columns faster (at least 10%). Values at the top of the sequence are not reused after being deleted. (When an AUTO\_INCREMENT column is defined as the last column of a multiple-column index, reuse of values deleted from the top of a sequence does occur.) The AUTO\_INCREMENT value can be reset with ALTER TABLE or myisamchk.
- Dynamic-sized rows are much less fragmented when mixing deletes with updates and inserts. This is done by automatically combining adjacent deleted blocks and by extending blocks if the next block is deleted.
- MyISAM supports concurrent inserts: If a table has no free blocks in the middle of the data file, you can INSERT new rows into it at the same time that other threads are reading from the table. A free block can occur as a result of deleting rows or an update of a dynamic length row with more data than its current contents. When all free blocks are used up (filled in), future inserts become concurrent again. See Section 10.11.3, "Concurrent Inserts".
- You can put the data file and index file in different directories on different physical devices to get more speed with the DATA DIRECTORY and INDEX DIRECTORY table options to CREATE TABLE. See Section 15.1.20, "CREATE TABLE Statement".
- BLOB and TEXT columns can be indexed.
- NULL values are permitted in indexed columns. This takes 0 to 1 bytes per key.
- Each character column can have a different character set. See Chapter 12, Character Sets, Collations, Unicode.
- There is a flag in the MyISAM index file that indicates whether the table was closed correctly. If mysqld is started with the myisam\_recover\_options system variable set, MyISAM tables are automatically checked when opened, and are repaired if the table wasn't closed properly.
- myisamchk marks tables as checked if you run it with the --update-state option. myisamchk --fast checks only those tables that don't have this mark.
- myisamchk --analyze stores statistics for portions of keys, as well as for entire keys.
- myisampack can pack BLOB and VARCHAR columns.

MyISAM also supports the following features:

- Support for a true VARCHAR type; a VARCHAR column starts with a length stored in one or two bytes.
- Tables with VARCHAR columns may have fixed or dynamic row length.
- The sum of the lengths of the VARCHAR and CHAR columns in a table may be up to 64KB.
- Arbitrary length UNIQUE constraints.

## **Additional Resources**

• A forum dedicated to the MyISAM storage engine is available at [https://forums.mysql.com/list.php?](https://forums.mysql.com/list.php?21) [21](https://forums.mysql.com/list.php?21).

## <span id="page-177-0"></span>**18.2.1 MyISAM Startup Options**

The following options to mysqld can be used to change the behavior of MyISAM tables. For additional information, see Section 7.1.7, "Server Command Options".

**Table 18.3 MyISAM Option and Variable Reference**

| Name                        | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|----------|-------------|------------|------------|-----------|---------|
| bulk_insert_buffer_size Yes |          | Yes         | Yes        |            | Both      | Yes     |
| concurrent_insert Yes       |          | Yes         | Yes        |            | Global    | Yes     |
| delay_key_writeYes          |          | Yes         | Yes        |            | Global    | Yes     |
| have_rtree_keys             |          |             | Yes        |            | Global    | No      |
| key_buffer_sizeYes          |          | Yes         | Yes        |            | Global    | Yes     |
| log-isam                    | Yes      | Yes         |            |            |           |         |
| myisam<br>block-size        | Yes      | Yes         |            |            |           |         |
| myisam_data_pointer_size    | Yes      | Yes         | Yes        |            | Global    | Yes     |
| myisam_max_sort_file_size   | Yes      | Yes         | Yes        |            | Global    | Yes     |
| myisam_mmap_size Yes        |          | Yes         | Yes        |            | Global    | No      |
| myisam_recover_options      | Yes      | Yes         | Yes        |            | Global    | No      |
| myisam_sort_buffer_size     | Yes      | Yes         | Yes        |            | Both      | Yes     |
| myisam_stats_method Yes     |          | Yes         | Yes        |            | Both      | Yes     |
| myisam_use_mmap Yes         |          | Yes         | Yes        |            | Global    | Yes     |
| tmp_table_sizeYes           |          | Yes         | Yes        |            | Both      | Yes     |

The following system variables affect the behavior of MyISAM tables. For additional information, see Section 7.1.8, "Server System Variables".

• bulk\_insert\_buffer\_size

The size of the tree cache used in bulk insert optimization.

![](_page_177_Picture_8.jpeg)

## **Note**

This is a limit per thread!

• delay\_key\_write=ALL

Don't flush key buffers between writes for any MyISAM table.

![](_page_177_Picture_13.jpeg)

## **Note**

If you do this, you should not access MyISAM tables from another program (such as from another MySQL server or with myisamchk) when the tables are in use. Doing so risks index corruption. Using --external-locking does not eliminate this risk.

• myisam\_max\_sort\_file\_size

The maximum size of the temporary file that MySQL is permitted to use while re-creating a MyISAM index (during REPAIR TABLE, ALTER TABLE, or LOAD DATA). If the file size would be larger than this value, the index is created using the key cache instead, which is slower. The value is given in bytes.

• myisam\_recover\_options=mode

Set the mode for automatic recovery of crashed MyISAM tables.

• myisam\_sort\_buffer\_size

Set the size of the buffer used when recovering tables.

Automatic recovery is activated if you start mysqld with the myisam\_recover\_options system variable set. In this case, when the server opens a MyISAM table, it checks whether the table is marked as crashed or whether the open count variable for the table is not 0 and you are running the server with external locking disabled. If either of these conditions is true, the following happens:

- The server checks the table for errors.
- If the server finds an error, it tries to do a fast table repair (with sorting and without re-creating the data file).
- If the repair fails because of an error in the data file (for example, a duplicate-key error), the server tries again, this time re-creating the data file.
- If the repair still fails, the server tries once more with the old repair option method (write row by row without sorting). This method should be able to repair any type of error and has low disk space requirements.

If the recovery wouldn't be able to recover all rows from previously completed statements and you didn't specify FORCE in the value of the myisam\_recover\_options system variable, automatic repair aborts with an error message in the error log:

```
Error: Couldn't repair table: test.g00pages
```

If you specify FORCE, a warning like this is written instead:

```
Warning: Found 344 of 354 rows when repairing ./test/g00pages
```

If the automatic recovery value includes BACKUP, the recovery process creates files with names of the form tbl\_name-datetime.BAK. You should have a cron script that automatically moves these files from the database directories to backup media.

# <span id="page-178-0"></span>**18.2.2 Space Needed for Keys**

MyISAM tables use B-tree indexes. You can roughly calculate the size for the index file as (key\_length+4)/0.67, summed over all keys. This is for the worst case when all keys are inserted in sorted order and the table doesn't have any compressed keys.

String indexes are space compressed. If the first index part is a string, it is also prefix compressed. Space compression makes the index file smaller than the worst-case figure if a string column has a lot of trailing space or is a VARCHAR column that is not always used to the full length. Prefix compression is used on keys that start with a string. Prefix compression helps if there are many strings with an identical prefix.

In MyISAM tables, you can also prefix compress numbers by specifying the PACK\_KEYS=1 table option when you create the table. Numbers are stored with the high byte first, so this helps when you have many integer keys that have an identical prefix.

# <span id="page-178-1"></span>**18.2.3 MyISAM Table Storage Formats**

MyISAM supports three different storage formats. Two of them, fixed and dynamic format, are chosen automatically depending on the type of columns you are using. The third, compressed format, can be created only with the myisampack utility (see Section 6.6.6, "myisampack — Generate Compressed, Read-Only MyISAM Tables").

When you use CREATE TABLE or ALTER TABLE for a table that has no BLOB or TEXT columns, you can force the table format to FIXED or DYNAMIC with the ROW\_FORMAT table option.

See Section 15.1.20, "CREATE TABLE Statement", for information about ROW\_FORMAT.

You can decompress (unpack) compressed MyISAM tables using myisamchk --unpack; see Section 6.6.4, "myisamchk — MyISAM Table-Maintenance Utility", for more information.