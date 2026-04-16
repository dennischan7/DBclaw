---
source: MySQL 5.7 Reference
title: 00_Overview
---

InnoDB tables are created using the CREATE TABLE statement; for example:

```
CREATE TABLE t1 (a INT, b CHAR (20), PRIMARY KEY (a)) ENGINE=InnoDB;
```

The ENGINE=InnoDB clause is not required when InnoDB is defined as the default storage engine, which it is by default. However, the ENGINE clause is useful if the CREATE TABLE statement is to be replayed on a different MySQL Server instance where the default storage engine is not InnoDB or is unknown. You can determine the default storage engine on a MySQL Server instance by issuing the following statement:

```
mysql> SELECT @@default_storage_engine;
+--------------------------+
| @@default_storage_engine |
+--------------------------+
| InnoDB |
+--------------------------+
```

InnoDB tables are created in file-per-table tablespaces by default. To create an InnoDB table in the InnoDB system tablespace, disable the innodb\_file\_per\_table variable before creating the table. To create an InnoDB table in a general tablespace, use CREATE TABLE ... TABLESPACE syntax. For more information, see [Section 14.6.3, "Tablespaces"](#page-48-0).

#### **.frm Files**

MySQL stores data dictionary information for tables in .frm files in database directories. Unlike other MySQL storage engines, InnoDB also encodes information about the table in its own internal data dictionary inside the system tablespace. When MySQL drops a table or a database, it deletes one or more .frm files as well as the corresponding entries inside the InnoDB data dictionary. You cannot move InnoDB tables between databases simply by moving the .frm files. For information about moving InnoDB tables, see [Section 14.6.1.4, "Moving or Copying InnoDB Tables".](#page-28-0)

#### **Row Formats**

The row format of an InnoDB table determines how its rows are physically stored on disk. InnoDB supports four row formats, each with different storage characteristics. Supported row formats include REDUNDANT, COMPACT, DYNAMIC, and COMPRESSED. The DYNAMIC row format is the default. For information about row format characteristics, see [Section 14.11, "InnoDB Row Formats"](#page-145-1).

The innodb\_default\_row\_format variable defines the default row format. The row format of a table can also be defined explicitly using the ROW\_FORMAT table option in a CREATE TABLE or ALTER TABLE statement. See [Defining the Row Format of a Table.](#page-150-0)

### **Primary Keys**

It is recommended that you define a primary key for each table that you create. When selecting primary key columns, choose columns with the following characteristics:

- Columns that are referenced by the most important queries.
- Columns that are never left blank.
- Columns that never have duplicate values.
- Columns that rarely if ever change value once inserted.

For example, in a table containing information about people, you would not create a primary key on (firstname, lastname) because more than one person can have the same name, a name column may be left blank, and sometimes people change their names. With so many constraints, often there is not an obvious set of columns to use as a primary key, so you create a new column with a numeric ID to serve as all or part of the primary key. You can declare an auto-increment column so that ascending values are filled in automatically as rows are inserted:

```
# The value of ID can act like a pointer between related items in different tables.
CREATE TABLE t5 (id INT AUTO_INCREMENT, b CHAR (20), PRIMARY KEY (id));
# The primary key can consist of more than one column. Any autoinc column must come first.
CREATE TABLE t6 (id INT AUTO_INCREMENT, a INT, b CHAR (20), PRIMARY KEY (id,a));
```

For more information about auto-increment columns, see [Section 14.6.1.6, "AUTO\\_INCREMENT](#page-35-0) [Handling in InnoDB"](#page-35-0).

Although a table works correctly without defining a primary key, the primary key is involved with many aspects of performance and is a crucial design aspect for any large or frequently used table. It is recommended that you always specify a primary key in the CREATE TABLE statement. If you create the table, load data, and then run ALTER TABLE to add a primary key later, that operation is much slower than defining the primary key when creating the table. For more information about primary keys, see [Section 14.6.2.1, "Clustered and Secondary Indexes"](#page-41-1).

#### **Viewing InnoDB Table Properties**

To view the properties of an InnoDB table, issue a SHOW TABLE STATUS statement:

```
mysql> SHOW TABLE STATUS FROM test LIKE 't%' \G;
*************************** 1. row ***************************
 Name: t1
```

```
 Engine: InnoDB
 Version: 10
 Row_format: Dynamic
 Rows: 0
 Avg_row_length: 0
 Data_length: 16384
Max_data_length: 0
 Index_length: 0
 Data_free: 0
 Auto_increment: NULL
 Create_time: 2021-02-18 12:18:28
 Update_time: NULL
 Check_time: NULL
 Collation: utf8mb4_0900_ai_ci
 Checksum: NULL
 Create_options: 
 Comment:
```

For information about SHOW TABLE STATUS output, see Section 13.7.5.36, "SHOW TABLE STATUS Statement".

You can also access InnoDB table properties by querying the InnoDB Information Schema system tables:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES WHERE NAME='test/t1' \G
*************************** 1. row ***************************
 TABLE_ID: 45
 NAME: test/t1
 FLAG: 1
 N_COLS: 5
 SPACE: 35
 FILE_FORMAT: Barracuda
 ROW_FORMAT: Dynamic
ZIP_PAGE_SIZE: 0
 SPACE_TYPE: Single
```

For more information, see Section 14.16.3, "InnoDB INFORMATION\_SCHEMA System Tables".

# <span id="page-20-1"></span>**14.6.1.2 Creating Tables Externally**

There are different reasons for creating InnoDB tables externally; that is, creating tables outside of the data directory. Those reasons might include space management, I/O optimization, or placing tables on a storage device with particular performance or capacity characteristics, for example.

InnoDB supports the following methods for creating tables externally:

- [Using the DATA DIRECTORY Clause](#page-20-0)
- [Using CREATE TABLE ... TABLESPACE Syntax](#page-22-0)
- [Creating a Table in an External General Tablespace](#page-22-1)

#### <span id="page-20-0"></span>**Using the DATA DIRECTORY Clause**

You can create an InnoDB table in an external directory by specifying a DATA DIRECTORY clause in the CREATE TABLE statement.

```
CREATE TABLE t1 (c1 INT PRIMARY KEY) DATA DIRECTORY = '/external/directory';
```

The DATA DIRECTORY clause is supported for tables created in file-per-table tablespaces. Tables are implicitly created in file-per-table tablespaces when the innodb\_file\_per\_table variable is enabled, which it is by default.

```
mysql> SELECT @@innodb_file_per_table;
+-------------------------+
| @@innodb_file_per_table |
```

```
+-------------------------+
| 1 |
+-------------------------+
```

For more information about file-per-table tablespaces, see [Section 14.6.3.2, "File-Per-Table](#page-51-0) [Tablespaces"](#page-51-0).

Be sure of the directory location you choose, as the DATA DIRECTORY clause cannot be used with ALTER TABLE to change the location later.

When you specify a DATA DIRECTORY clause in a CREATE TABLE statement, the table's data file (table\_name.ibd) is created in a schema directory under the specified directory, and an .isl file (table\_name.isl) that contains the data file path is created in the schema directory under the MySQL data directory. An .isl file is similar in function to a symbolic link. (Actual symbolic links are not supported for use with InnoDB data files.)

The following example demonstrates creating a table in an external directory using the DATA DIRECTORY clause. It is assumed that the innodb\_file\_per\_table variable is enabled.

```
mysql> USE test;
Database changed
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) DATA DIRECTORY = '/external/directory';
# MySQL creates the table's data file in a schema directory
# under the external directory
$> cd /external/directory/test
$> ls
t1.ibd
# An .isl file that contains the data file path is created
# in the schema directory under the MySQL data directory
$> cd /path/to/mysql/data/test
$> ls
db.opt t1.frm t1.isl
```

### **Usage Notes:**

• MySQL initially holds the tablespace data file open, preventing you from dismounting the device, but might eventually close the file if the server is busy. Be careful not to accidentally dismount an external device while MySQL is running, or start MySQL while the device is disconnected. Attempting to access a table when the associated data file is missing causes a serious error that requires a server restart.

A server restart might fail if the data file is not found at the expected path. In this case, manually remove the .isl file from the schema directory. After restarting, drop the table to remove the .frm file and the information about the table from the data dictionary.

- Before placing a table on an NFS-mounted volume, review potential issues outlined in Using NFS with MySQL.
- If using an LVM snapshot, file copy, or other file-based mechanism to back up the table's data file, always use the FLUSH TABLES ... FOR EXPORT statement first to ensure that all changes buffered in memory are flushed to disk before the backup occurs.
- Using the DATA DIRECTORY clause to create a table in an external directory is an alternative to using symbolic links, which InnoDB does not support.
- The DATA DIRECTORY clause is not supported in a replication environment where the source and replica reside on the same host. The DATA DIRECTORY clause requires a full directory path. Replicating the path in this case would cause the source and replica to create the table in same location.

#### <span id="page-22-0"></span>**Using CREATE TABLE ... TABLESPACE Syntax**

CREATE TABLE ... TABLESPACE syntax can be used in combination with the DATA DIRECTORY clause to create a table in an external directory. To do so, specify innodb\_file\_per\_table as the tablespace name.

```
mysql> CREATE TABLE t2 (c1 INT PRIMARY KEY) TABLESPACE = innodb_file_per_table
 DATA DIRECTORY = '/external/directory';
```

This method is supported only for tables created in file-per-table tablespaces, but does not require the innodb\_file\_per\_table variable to be enabled. In all other respects, this method is equivalent to the CREATE TABLE ... DATA DIRECTORY method described above. The same usage notes apply.

#### <span id="page-22-1"></span>**Creating a Table in an External General Tablespace**

You can create a table in a general tablespace that resides in an external directory.

- For information about creating a general tablespace in an external directory, see [Creating a General](#page-54-0) [Tablespace.](#page-54-0)
- For information about creating a table in a general tablespace, see [Adding Tables to a General](#page-55-0) [Tablespace.](#page-55-0)

# <span id="page-22-3"></span>**14.6.1.3 Importing InnoDB Tables**

This section describes how to import tables using the Transportable Tablespaces feature, which permits importing tables, partitioned tables, or individual table partitions that reside in file-per-table tablespaces. There are many reasons why you might want to import tables:

- To run reports on a non-production MySQL server instance to avoid placing extra load on a production server.
- To copy data to a new replica server.
- To restore a table from a backed-up tablespace file.
- As a faster way of moving data than importing a dump file, which requires reinserting data and rebuilding indexes.
- To move a data to a server with storage media that is better suited to your storage requirements. For example, you might move busy tables to an SSD device, or move large tables to a high-capacity HDD device.

The Transportable Tablespaces feature is described under the following topics in this section:

- [Prerequisites](#page-22-2)
- [Importing Tables](#page-23-0)
- [Importing Partitioned Tables](#page-24-0)
- [Importing Table Partitions](#page-25-0)
- [Limitations](#page-27-0)
- [Usage Notes](#page-27-1)
- [Internals](#page-27-2)

#### <span id="page-22-2"></span>**Prerequisites**

- The innodb\_file\_per\_table variable must be enabled, which it is by default.
- The page size of the tablespace must match the page size of the destination MySQL server instance. InnoDB page size is defined by the innodb\_page\_size variable, which is configured when initializing a MySQL server instance.

- If the table has a foreign key relationship, foreign\_key\_checks must be disabled before executing DISCARD TABLESPACE. Also, you should export all foreign key related tables at the same logical point in time, as ALTER TABLE ... IMPORT TABLESPACE does not enforce foreign key constraints on imported data. To do so, stop updating the related tables, commit all transactions, acquire shared locks on the tables, and perform the export operations.
- When importing a table from another MySQL server instance, both MySQL server instances must have General Availability (GA) status and must be the same version. Otherwise, the table must be created on the same MySQL server instance into which it is being imported.
- If the table was created in an external directory by specifying the DATA DIRECTORY clause in the CREATE TABLE statement, the table that you replace on the destination instance must be defined with the same DATA DIRECTORY clause. A schema mismatch error is reported if the clauses do not match. To determine if the source table was defined with a DATA DIRECTORY clause, use SHOW CREATE TABLE to view the table definition. For information about using the DATA DIRECTORY clause, see [Section 14.6.1.2, "Creating Tables Externally"](#page-20-1).
- If a ROW\_FORMAT option is not defined explicitly in the table definition or ROW\_FORMAT=DEFAULT is used, the innodb\_default\_row\_format setting must be the same on the source and destination instances. Otherwise, a schema mismatch error is reported when you attempt the import operation. Use SHOW CREATE TABLE to check the table definition. Use SHOW VARIABLES to check the innodb\_default\_row\_format setting. For related information, see [Defining the Row Format of a](#page-150-0) [Table](#page-150-0).

#### <span id="page-23-0"></span>**Importing Tables**

This example demonstrates how to import a regular non-partitioned table that resides in a file-per-table tablespace.

1. On the destination instance, create a table with the same definition as the table you intend to import. (You can obtain the table definition using SHOW CREATE TABLE syntax.) If the table definition does not match, a schema mismatch error is reported when you attempt the import operation.

```
mysql> USE test;
mysql> CREATE TABLE t1 (c1 INT) ENGINE=INNODB;
```

2. On the destination instance, discard the tablespace of the table that you just created. (Before importing, you must discard the tablespace of the receiving table.)

```
mysql> ALTER TABLE t1 DISCARD TABLESPACE;
```

3. On the source instance, run FLUSH TABLES ... FOR EXPORT to quiesce the table you intend to import. When a table is quiesced, only read-only transactions are permitted on the table.

```
mysql> USE test;
mysql> FLUSH TABLES t1 FOR EXPORT;
```

FLUSH TABLES ... FOR EXPORT ensures that changes to the named table are flushed to disk so that a binary table copy can be made while the server is running. When FLUSH TABLES ... FOR EXPORT is run, InnoDB generates a .cfg metadata file in the schema directory of the table. The .cfg file contains metadata that is used for schema verification during the import operation.

![](_page_23_Picture_14.jpeg)

#### **Note**

The connection executing FLUSH TABLES ... FOR EXPORT must remain open while the operation is running; otherwise, the .cfg file is removed as locks are released upon connection closure.

4. Copy the .ibd file and .cfg metadata file from the source instance to the destination instance. For example:

\$> scp /path/to/datadir/test/t1.{ibd,cfg} destination-server:/path/to/datadir/test

The .ibd file and .cfg file must be copied before releasing the shared locks, as described in the next step.

![](_page_24_Picture_2.jpeg)

#### **Note**

If you are importing a table from an encrypted tablespace, InnoDB generates a .cfp file in addition to a .cfg metadata file. The .cfp file must be copied to the destination instance together with the .cfg file. The .cfp file contains a transfer key and an encrypted tablespace key. On import, InnoDB uses the transfer key to decrypt the tablespace key. For related information, see [Section 14.14, "InnoDB Data-at-Rest Encryption".](#page-174-0)

5. On the source instance, use UNLOCK TABLES to release the locks acquired by the FLUSH TABLES ... FOR EXPORT statement:

```
mysql> USE test;
mysql> UNLOCK TABLES;
```

The UNLOCK TABLES operation also removes the .cfg file.

6. On the destination instance, import the tablespace:

```
mysql> USE test;
mysql> ALTER TABLE t1 IMPORT TABLESPACE;
```

### <span id="page-24-0"></span>**Importing Partitioned Tables**

This example demonstrates how to import a partitioned table, where each table partition resides in a file-per-table tablespace.

1. On the destination instance, create a partitioned table with the same definition as the partitioned table that you want to import. (You can obtain the table definition using SHOW CREATE TABLE syntax.) If the table definition does not match, a schema mismatch error is reported when you attempt the import operation.

```
mysql> USE test;
mysql> CREATE TABLE t1 (i int) ENGINE = InnoDB PARTITION BY KEY (i) PARTITIONS 3;
```

In the /datadir/test directory, there is a tablespace .ibd file for each of the three partitions.

```
mysql> \! ls /path/to/datadir/test/
db.opt t1.frm t1#P#p0.ibd t1#P#p1.ibd t1#P#p2.ibd
```

2. On the destination instance, discard the tablespace for the partitioned table. (Before the import operation, you must discard the tablespace of the receiving table.)

```
mysql> ALTER TABLE t1 DISCARD TABLESPACE;
```

The three tablespace .ibd files of the partitioned table are discarded from the /datadir/test directory, leaving the following files:

```
mysql> \! ls /path/to/datadir/test/
db.opt t1.frm
```

3. On the source instance, run FLUSH TABLES ... FOR EXPORT to quiesce the partitioned table that you intend to import. When a table is quiesced, only read-only transactions are permitted on the table.

```
mysql> USE test;
mysql> FLUSH TABLES t1 FOR EXPORT;
```

FLUSH TABLES ... FOR EXPORT ensures that changes to the named table are flushed to disk so that binary table copy can be made while the server is running. When FLUSH TABLES ...

FOR EXPORT is run, InnoDB generates .cfg metadata files in the schema directory of the table for each of the table's tablespace files.

```
mysql> \! ls /path/to/datadir/test/
db.opt t1#P#p0.ibd t1#P#p1.ibd t1#P#p2.ibd
t1.frm t1#P#p0.cfg t1#P#p1.cfg t1#P#p2.cfg
```

The .cfg files contain metadata that is used for schema verification when importing the tablespace. FLUSH TABLES ... FOR EXPORT can only be run on the table, not on individual table partitions.

4. Copy the .ibd and .cfg files from the source instance schema directory to the destination instance schema directory. For example:

```
$>scp /path/to/datadir/test/t1*.{ibd,cfg} destination-server:/path/to/datadir/test
```

The .ibd and .cfg files must be copied before releasing the shared locks, as described in the next step.

![](_page_25_Picture_7.jpeg)

#### **Note**

If you are importing a table from an encrypted tablespace, InnoDB generates a .cfp files in addition to a .cfg metadata files. The .cfp files must be copied to the destination instance together with the .cfg files. The .cfp files contain a transfer key and an encrypted tablespace key. On import, InnoDB uses the transfer key to decrypt the tablespace key. For related information, see [Section 14.14, "InnoDB Data-at-Rest Encryption".](#page-174-0)

5. On the source instance, use UNLOCK TABLES to release the locks acquired by FLUSH TABLES ... FOR EXPORT:

```
mysql> USE test;
mysql> UNLOCK TABLES;
```

6. On the destination instance, import the tablespace of the partitioned table:

```
mysql> USE test;
mysql> ALTER TABLE t1 IMPORT TABLESPACE;
```

#### <span id="page-25-0"></span>**Importing Table Partitions**

This example demonstrates how to import individual table partitions, where each partition resides in a file-per-table tablespace file.

In the following example, two partitions (p2 and p3) of a four-partition table are imported.

1. On the destination instance, create a partitioned table with the same definition as the partitioned table that you want to import partitions from. (You can obtain the table definition using SHOW CREATE TABLE syntax.) If the table definition does not match, a schema mismatch error is reported when you attempt the import operation.

```
mysql> USE test;
mysql> CREATE TABLE t1 (i int) ENGINE = InnoDB PARTITION BY KEY (i) PARTITIONS 4;
```

In the /datadir/test directory, there is a tablespace .ibd file for each of the four partitions.

```
mysql> \! ls /path/to/datadir/test/
db.opt t1.frm t1#P#p0.ibd t1#P#p1.ibd t1#P#p2.ibd t1#P#p3.ibd
```

2. On the destination instance, discard the partitions that you intend to import from the source instance. (Before importing partitions, you must discard the corresponding partitions from the receiving partitioned table.)

```
mysql> ALTER TABLE t1 DISCARD PARTITION p2, p3 TABLESPACE;
```

The tablespace .ibd files for the two discarded partitions are removed from the /datadir/test directory on the destination instance, leaving the following files:

```
mysql> \! ls /path/to/datadir/test/
db.opt t1.frm t1#P#p0.ibd t1#P#p1.ibd
```

![](_page_26_Picture_3.jpeg)

#### **Note**

When ALTER TABLE ... DISCARD PARTITION ... TABLESPACE is run on subpartitioned tables, both partition and subpartition table names are permitted. When a partition name is specified, subpartitions of that partition are included in the operation.

3. On the source instance, run FLUSH TABLES ... FOR EXPORT to quiesce the partitioned table. When a table is quiesced, only read-only transactions are permitted on the table.

```
mysql> USE test;
mysql> FLUSH TABLES t1 FOR EXPORT;
```

FLUSH TABLES ... FOR EXPORT ensures that changes to the named table are flushed to disk so that binary table copy can be made while the instance is running. When FLUSH TABLES ... FOR EXPORT is run, InnoDB generates a .cfg metadata file for each of the table's tablespace files in the schema directory of the table.

```
mysql> \! ls /path/to/datadir/test/
db.opt t1#P#p0.ibd t1#P#p1.ibd t1#P#p2.ibd t1#P#p3.ibd
t1.frm t1#P#p0.cfg t1#P#p1.cfg t1#P#p2.cfg t1#P#p3.cfg
```

The .cfg files contain metadata that used for schema verification during the import operation. FLUSH TABLES ... FOR EXPORT can only be run on the table, not on individual table partitions.

4. Copy the .ibd and .cfg files for partition p2 and partition p3 from the source instance schema directory to the destination instance schema directory.

```
$> scp t1#P#p2.ibd t1#P#p2.cfg t1#P#p3.ibd t1#P#p3.cfg destination-server:/path/to/datadir/test
```

The .ibd and .cfg files must be copied before releasing the shared locks, as described in the next step.

![](_page_26_Picture_14.jpeg)

### **Note**

If you are importing partitions from an encrypted tablespace, InnoDB generates a .cfp files in addition to a .cfg metadata files. The .cfp files must be copied to the destination instance together with the .cfg files. The .cfp files contain a transfer key and an encrypted tablespace key. On import, InnoDB uses the transfer key to decrypt the tablespace key. For related information, see [Section 14.14, "InnoDB Data-at-Rest Encryption".](#page-174-0)

5. On the source instance, use UNLOCK TABLES to release the locks acquired by FLUSH TABLES ... FOR EXPORT:

```
mysql> USE test;
mysql> UNLOCK TABLES;
```

6. On the destination instance, import table partitions p2 and p3:

```
mysql> USE test;
mysql> ALTER TABLE t1 IMPORT PARTITION p2, p3 TABLESPACE;
```

![](_page_26_Picture_21.jpeg)

#### **Note**

When ALTER TABLE ... IMPORT PARTITION ... TABLESPACE is run on subpartitioned tables, both partition and subpartition table names are permitted. When a partition name is specified, subpartitions of that partition are included in the operation.

### <span id="page-27-0"></span>**Limitations**

- The Transportable Tablespaces feature is only supported for tables that reside in file-per-table tablespaces. It is not supported for the tables that reside in the system tablespace or general tablespaces. Tables in shared tablespaces cannot be quiesced.
- FLUSH TABLES ... FOR EXPORT is not supported on tables with a FULLTEXT index, as fulltext search auxiliary tables cannot be flushed. After importing a table with a FULLTEXT index, run OPTIMIZE TABLE to rebuild the FULLTEXT indexes. Alternatively, drop FULLTEXT indexes before the export operation and recreate the indexes after importing the table on the destination instance.
- Due to a .cfg metadata file limitation, schema mismatches are not reported for partition type or partition definition differences when importing a partitioned table. Column differences are reported.

### <span id="page-27-1"></span>**Usage Notes**

• ALTER TABLE ... IMPORT TABLESPACE does not require a .cfg metadata file to import a table. However, metadata checks are not performed when importing without a .cfg file, and a warning similar to the following is issued:

```
Message: InnoDB: IO Read error: (2, No such file or directory) Error opening '.\
test\t.cfg', will attempt to import without schema verification
1 row in set (0.00 sec)
```

Importing a table without a .cfg metadata file should only be considered if no schema mismatches are expected. The ability to import without a .cfg file could be useful in crash recovery scenarios where metadata is not accessible.

• On Windows, InnoDB stores database, tablespace, and table names internally in lowercase. To avoid import problems on case-sensitive operating systems such as Linux and Unix, create all databases, tablespaces, and tables using lowercase names. A convenient way to accomplish this is to add lower\_case\_table\_names=1 to the [mysqld] section of your my.cnf or my.ini file before creating databases, tablespaces, or tables:

```
[mysqld]
lower_case_table_names=1
```

• When running ALTER TABLE ... DISCARD PARTITION ... TABLESPACE and ALTER TABLE ... IMPORT PARTITION ... TABLESPACE on subpartitioned tables, both partition and subpartition table names are permitted. When a partition name is specified, subpartitions of that partition are included in the operation.

# <span id="page-27-2"></span>**Internals**

The following information describes internals and messages written to the error log during a table import procedure.

When ALTER TABLE ... DISCARD TABLESPACE is run on the destination instance:

- The table is locked in X mode.
- The tablespace is detached from the table.

When FLUSH TABLES ... FOR EXPORT is run on the source instance:

- The table being flushed for export is locked in shared mode.
- The purge coordinator thread is stopped.
- Dirty pages are synchronized to disk.

• Table metadata is written to the binary .cfg file.

Expected error log messages for this operation:

```
[Note] InnoDB: Sync to disk of '"test"."t1"' started.
[Note] InnoDB: Stopping purge
[Note] InnoDB: Writing table metadata to './test/t1.cfg'
[Note] InnoDB: Table '"test"."t1"' flushed to disk
```

When UNLOCK TABLES is run on the source instance:

- The binary .cfg file is deleted.
- The shared lock on the table or tables being imported is released and the purge coordinator thread is restarted.

Expected error log messages for this operation:

```
[Note] InnoDB: Deleting the meta-data file './test/t1.cfg'
[Note] InnoDB: Resuming purge
```

When ALTER TABLE ... IMPORT TABLESPACE is run on the destination instance, the import algorithm performs the following operations for each tablespace being imported:

- Each tablespace page is checked for corruption.
- The space ID and log sequence numbers (LSNs) on each page are updated.
- Flags are validated and LSN updated for the header page.
- Btree pages are updated.
- The page state is set to dirty so that it is written to disk.

Expected error log messages for this operation:

```
[Note] InnoDB: Importing tablespace for table 'test/t1' that was exported
from host 'host_name'
[Note] InnoDB: Phase I - Update all pages
[Note] InnoDB: Sync to disk
[Note] InnoDB: Sync to disk - done!
[Note] InnoDB: Phase III - Flush changes to disk
[Note] InnoDB: Phase IV - Flush complete
```

![](_page_28_Picture_17.jpeg)

#### **Note**

You may also receive a warning that a tablespace is discarded (if you discarded the tablespace for the destination table) and a message stating that statistics could not be calculated due to a missing .ibd file:

```
[Warning] InnoDB: Table "test"."t1" tablespace is set as discarded.
7f34d9a37700 InnoDB: cannot calculate statistics for table
"test"."t1" because the .ibd file is missing. For help, please refer to
http://dev.mysql.com/doc/refman/5.7/en/innodb-troubleshooting.html
```

# <span id="page-28-0"></span>**14.6.1.4 Moving or Copying InnoDB Tables**

This section describes techniques for moving or copying some or all InnoDB tables to a different server or instance. For example, you might move an entire MySQL instance to a larger, faster server; you might clone an entire MySQL instance to a new replica server; you might copy individual tables to another instance to develop and test an application, or to a data warehouse server to produce reports.

On Windows, InnoDB always stores database and table names internally in lowercase. To move databases in a binary format from Unix to Windows or from Windows to Unix, create all databases and tables using lowercase names. A convenient way to accomplish this is to add the following line to the [mysqld] section of your my.cnf or my.ini file before creating any databases or tables:

```
[mysqld]
lower_case_table_names=1
```

Techniques for moving or copying InnoDB tables include:

- [Importing Tables](#page-29-0)
- [MySQL Enterprise Backup](#page-29-1)
- [Copying Data Files \(Cold Backup Method\)](#page-29-2)
- [Restoring from a Logical Backup](#page-30-0)

### <span id="page-29-0"></span>**Importing Tables**

A table that resides in a file-per-table tablespace can be imported from another MySQL server instance or from a backup using the Transportable Tablespace feature. See [Section 14.6.1.3, "Importing InnoDB](#page-22-3) [Tables"](#page-22-3).

### <span id="page-29-1"></span>**MySQL Enterprise Backup**

The MySQL Enterprise Backup product lets you back up a running MySQL database with minimal disruption to operations while producing a consistent snapshot of the database. When MySQL Enterprise Backup is copying tables, reads and writes can continue. In addition, MySQL Enterprise Backup can create compressed backup files, and back up subsets of tables. In conjunction with the MySQL binary log, you can perform point-in-time recovery. MySQL Enterprise Backup is included as part of the MySQL Enterprise subscription.

For more details about MySQL Enterprise Backup, see Section 28.1, "MySQL Enterprise Backup Overview".

### <span id="page-29-2"></span>**Copying Data Files (Cold Backup Method)**

You can move an InnoDB database simply by copying all the relevant files listed under "Cold Backups" in Section 14.19.1, "InnoDB Backup".

InnoDB data and log files are binary-compatible on all platforms having the same floating-point number format. If the floating-point formats differ but you have not used FLOAT or DOUBLE data types in your tables, then the procedure is the same: simply copy the relevant files.

When you move or copy file-per-table .ibd files, the database directory name must be the same on the source and destination systems. The table definition stored in the InnoDB shared tablespace includes the database name. The transaction IDs and log sequence numbers stored in the tablespace files also differ between databases.

To move an .ibd file and the associated table from one database to another, use a RENAME TABLE statement:

```
RENAME TABLE db1.tbl_name TO db2.tbl_name;
```

If you have a "clean" backup of an .ibd file, you can restore it to the MySQL installation from which it originated as follows:

- 1. The table must not have been dropped or truncated since you copied the .ibd file, because doing so changes the table ID stored inside the tablespace.
- 2. Issue this ALTER TABLE statement to delete the current .ibd file:

```
ALTER TABLE tbl_name DISCARD TABLESPACE;
```

- 3. Copy the backup .ibd file to the proper database directory.
- 4. Issue this ALTER TABLE statement to tell InnoDB to use the new .ibd file for the table:

ALTER TABLE tbl\_name IMPORT TABLESPACE;

![](_page_30_Picture_2.jpeg)

#### **Note**

The ALTER TABLE ... IMPORT TABLESPACE feature does not enforce foreign key constraints on imported data.

In this context, a "clean" .ibd file backup is one for which the following requirements are satisfied:

- There are no uncommitted modifications by transactions in the .ibd file.
- There are no unmerged insert buffer entries in the .ibd file.
- Purge has removed all delete-marked index records from the .ibd file.
- mysqld has flushed all modified pages of the .ibd file from the buffer pool to the file.

You can make a clean backup .ibd file using the following method:

- 1. Stop all activity from the mysqld server and commit all transactions.
- 2. Wait until SHOW ENGINE INNODB STATUS shows that there are no active transactions in the database, and the main thread status of InnoDB is Waiting for server activity. Then you can make a copy of the .ibd file.

Another method for making a clean copy of an .ibd file is to use the MySQL Enterprise Backup product:

- 1. Use MySQL Enterprise Backup to back up the InnoDB installation.
- 2. Start a second mysqld server on the backup and let it clean up the .ibd files in the backup.

### <span id="page-30-0"></span>**Restoring from a Logical Backup**

You can use a utility such as mysqldump to perform a logical backup, which produces a set of SQL statements that can be executed to reproduce the original database object definitions and table data for transfer to another SQL server. Using this method, it does not matter whether the formats differ or if your tables contain floating-point data.

To improve the performance of this method, disable autocommit when importing data. Perform a commit only after importing an entire table or segment of a table.