---
source: MySQL 8.4 Reference
title: 00_Overview
---

The system tablespace is the storage area for the change buffer. It may also contain table and index data if tables are created in the system tablespace rather than file-per-table or general tablespaces.

The system tablespace can have one or more data files. By default, a single system tablespace data file, named ibdata1, is created in the data directory. The size and number of system tablespace data files is defined by the innodb\_data\_file\_path startup option. For configuration information, see [System Tablespace Data File Configuration.](#page-83-0)

Additional information about the system tablespace is provided under the following topics in the section:

- [Resizing the System Tablespace](#page-28-0)
- [Using Raw Disk Partitions for the System Tablespace](#page-29-0)

## <span id="page-28-0"></span>**Resizing the System Tablespace**

This section describes how to increase or decrease the size of the system tablespace.

#### **Increasing the Size of the System Tablespace**

The easiest way to increase the size of the system tablespace is to configure it to be auto-extending. To do so, specify the autoextend attribute for the last data file in the innodb\_data\_file\_path setting, and restart the server. For example:

```
innodb_data_file_path=ibdata1:10M:autoextend
```

When the autoextend attribute is specified, the data file automatically increases in size by 8MB increments as space is required. The [innodb\\_autoextend\\_increment](#page-191-1) variable controls the increment size.

You can also increase system tablespace size by adding another data file. To do so:

- 1. Stop the MySQL server.
- 2. If the last data file in the innodb\_data\_file\_path setting is defined with the autoextend attribute, remove it, and modify the size attribute to reflect the current data file size. To determine the appropriate data file size to specify, check your file system for the file size, and round that value down to the closest MB value, where a MB is equal to 1024 x 1024 bytes.
- 3. Append a new data file to the innodb\_data\_file\_path setting, optionally specifying the autoextend attribute. The autoextend attribute can be specified only for the last data file in the innodb\_data\_file\_path setting.
- 4. Start the MySQL server.

For example, this tablespace has one auto-extending data file:

```
innodb_data_home_dir =
innodb_data_file_path = /ibdata/ibdata1:10M:autoextend
```

Suppose that the data file has grown to 988MB over time. This is the innodb\_data\_file\_path setting after modifying the size attribute to reflect the current data file size, and after specifying a new 50MB auto-extending data file:

```
innodb_data_home_dir =
innodb_data_file_path = /ibdata/ibdata1:988M;/disk2/ibdata2:50M:autoextend
```

When adding a new data file, do not specify an existing file name. InnoDB creates and initializes the new data file when you start the server.

![](_page_29_Picture_4.jpeg)

#### **Note**

You cannot increase the size of an existing system tablespace data file by changing its size attribute. For example, changing the innodb\_data\_file\_path setting from ibdata1:10M:autoextend to ibdata1:12M:autoextend produces the following error when starting the server:

```
[ERROR] [MY-012263] [InnoDB] The Auto-extending innodb_system
data file './ibdata1' is of a different size 640 pages (rounded down to MB) than
specified in the .cnf file: initial 768 pages, max 0 (relevant if non-zero) pages!
```

The error indicates that the existing data file size (expressed in InnoDB pages) is different from the data file size specified in the configuration file. If you encounter this error, restore the previous innodb\_data\_file\_path setting, and refer to the system tablespace resizing instructions.

#### **Decreasing the Size of the InnoDB System Tablespace**

Decreasing the size of an existing system tablespace is not supported. The only option to achieve a smaller system tablespace is to restore your data from a backup to a new MySQL instance created with the desired system tablespace size configuration.

For information about creating backups, see Section 17.18.1, "InnoDB Backup".

For information about configuring data files for a new system tablespace. See [System Tablespace Data](#page-83-0) [File Configuration](#page-83-0).

To avoid a large system tablespace, consider using file-per-table tablespaces or general tablespaces for your data. File-per-table tablespaces are the default tablespace type and are used implicitly when creating an InnoDB table. Unlike the system tablespace, file-per-table tablespaces return disk space to the operating system when they are truncated or dropped. For more information, see [Section 17.6.3.2,](#page-30-0) ["File-Per-Table Tablespaces"](#page-30-0). General tablespaces are multi-table tablespaces that can also be used as an alternative to the system tablespace. See [Section 17.6.3.3, "General Tablespaces"](#page-32-0).

## <span id="page-29-0"></span>**Using Raw Disk Partitions for the System Tablespace**

Raw disk partitions can be used as system tablespace data files. This technique enables nonbuffered I/ O on Windows and some Linux and Unix systems without file system overhead. Perform tests with and without raw partitions to verify whether they improve performance on your system.

When using a raw disk partition, ensure that the user ID that runs the MySQL server has read and write privileges for that partition. For example, if running the server as the mysql user, the partition must be readable and writeable by mysql. If running the server with the --memlock option, the server must be run as root, so the partition must be readable and writeable by root.

The procedures described below involve option file modification. For additional information, see Section 6.2.2.2, "Using Option Files".

#### **Allocating a Raw Disk Partition on Linux and Unix Systems**

1. To use a raw device for a new server instance, first prepare the configuration file by setting innodb\_data\_file\_path with the raw keyword. For example:

```
[mysqld]
innodb_data_home_dir=
innodb_data_file_path=/dev/hdd1:3Graw;/dev/hdd2:2Graw
```

The partition must be at least as large as the size that you specify. Note that 1MB in InnoDB is 1024 × 1024 bytes, whereas 1MB in disk specifications usually means 1,000,000 bytes.

- 2. Then initialize the server for the first time by using --initialize or --initialize-insecure. InnoDB notices the raw keyword and initializes the new partition, and then it stops the server.
- 3. Now restart the server. InnoDB now permits changes to be made.

#### **Allocating a Raw Disk Partition on Windows**

On Windows systems, the same steps and accompanying guidelines described for Linux and Unix systems apply except that the innodb\_data\_file\_path setting differs slightly on Windows. For example:

```
[mysqld]
innodb_data_home_dir=
innodb_data_file_path=//./D::10Graw
```

The //./ corresponds to the Windows syntax of \\.\ for accessing physical drives. In the example above, D: is the drive letter of the partition.

# <span id="page-30-0"></span>**17.6.3.2 File-Per-Table Tablespaces**

A file-per-table tablespace contains data and indexes for a single InnoDB table, and is stored on the file system in a single data file.

File-per-table tablespace characteristics are described under the following topics in this section:

- [File-Per-Table Tablespace Configuration](#page-30-1)
- [File-Per-Table Tablespace Data Files](#page-30-2)
- [File-Per-Table Tablespace Advantages](#page-31-0)
- [File-Per-Table Tablespace Disadvantages](#page-32-1)

### <span id="page-30-1"></span>**File-Per-Table Tablespace Configuration**

InnoDB creates tables in file-per-table tablespaces by default. This behavior is controlled by the innodb\_file\_per\_table variable. Disabling innodb\_file\_per\_table causes InnoDB to create tables in the system tablespace.

An innodb\_file\_per\_table setting can be specified in an option file or configured at runtime using a SET GLOBAL statement. Changing the setting at runtime requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges".

Option file:

```
[mysqld]
innodb_file_per_table=ON
Using SET GLOBAL at runtime:
mysql> SET GLOBAL innodb_file_per_table=ON;
```

### <span id="page-30-2"></span>**File-Per-Table Tablespace Data Files**

A file-per-table tablespace is created in an .ibd data file in a schema directory under the MySQL data directory. The .ibd file is named for the table (table\_name.ibd). For example, the data file for table test.t1 is created in the test directory under the MySQL data directory:

```
mysql> USE test;
```

```
mysql> CREATE TABLE t1 (
 -> id INT PRIMARY KEY AUTO_INCREMENT,
 -> name VARCHAR(100)
 -> ) ENGINE = InnoDB;
mysql> EXIT;
$> cd /path/to/mysql/data/test
$> ls
t1.ibd
```

You can use the DATA DIRECTORY clause of the CREATE TABLE statement to implicitly create a fileper-table tablespace data file outside of the data directory. For more information, see Section 17.6.1.2, "Creating Tables Externally".

### <span id="page-31-0"></span>**File-Per-Table Tablespace Advantages**

File-per-table tablespaces have the following advantages over shared tablespaces such as the system tablespace or general tablespaces.

- Disk space is returned to the operating system after truncating or dropping a table created in a fileper-table tablespace. Truncating or dropping a table stored in a shared tablespace creates free space within the shared tablespace data file, which can only be used for InnoDB data. In other words, a shared tablespace data file does not shrink in size after a table is truncated or dropped.
- A table-copying ALTER TABLE operation on a table that resides in a shared tablespace can increase the amount of disk space occupied by the tablespace. Such operations may require as much additional space as the data in the table plus indexes. This space is not released back to the operating system as it is for file-per-table tablespaces.
- TRUNCATE TABLE performance is better when executed on tables that reside in file-per-table tablespaces.
- File-per-table tablespace data files can be created on separate storage devices for I/O optimization, space management, or backup purposes. See Section 17.6.1.2, "Creating Tables Externally".
- You can import a table that resides in file-per-table tablespace from another MySQL instance. See [Section 17.6.1.3, "Importing InnoDB Tables"](#page-0-0).
- Tables created in file-per-table tablespaces support features associated with DYNAMIC and COMPRESSED row formats, which are not supported by the system tablespace. See [Section 17.10,](#page-141-0) ["InnoDB Row Formats"](#page-141-0).
- Tables stored in individual tablespace data files can save time and improve chances for a successful recovery when data corruption occurs, when backups or binary logs are unavailable, or when the MySQL server instance cannot be restarted.
- Tables created in file-per-table tablespaces can be backed up or restored quickly using MySQL Enterprise Backup, without interrupting the use of other InnoDB tables. This is beneficial for tables on varying backup schedules or that require backup less frequently. See [Making a Partial Backup](https://dev.mysql.com/doc/mysql-enterprise-backup/8.4/en/partial.md) for details.
- File-per-table tablespaces permit monitoring table size on the file system by monitoring the size of the tablespace data file.
- Common Linux file systems do not permit concurrent writes to a single file such as a shared tablespace data file when innodb\_flush\_method is set to O\_DIRECT. As a result, there are possible performance improvements when using file-per-table tablespaces in conjunction with this setting.
- Tables in a shared tablespace are limited in size by the 64TB tablespace size limit. By comparison, each file-per-table tablespace has a 64TB size limit, which provides plenty of room for individual tables to grow in size.

### <span id="page-32-1"></span>**File-Per-Table Tablespace Disadvantages**

File-per-table tablespaces have the following disadvantages compared to shared tablespaces such as the system tablespace or general tablespaces.

- With file-per-table tablespaces, each table may have unused space that can only be utilized by rows of the same table, which can lead to wasted space if not properly managed.
- fsync operations are performed on multiple file-per-table data files instead of a single shared tablespace data file. Because fsync operations are per file, write operations for multiple tables cannot be combined, which can result in a higher total number of fsync operations.
- mysqld must keep an open file handle for each file-per-table tablespace, which may impact performance if you have numerous tables in file-per-table tablespaces.
- More file descriptors are required when each table has its own data file.
- There is potential for more fragmentation, which can impede DROP TABLE and table scan performance. However, if fragmentation is managed, file-per-table tablespaces can improve performance for these operations.
- The buffer pool is scanned when dropping a table that resides in a file-per-table tablespace, which can take several seconds for large buffer pools. The scan is performed with a broad internal lock, which may delay other operations.
- The [innodb\\_autoextend\\_increment](#page-191-1) variable, which defines the increment size for extending the size of an auto-extending shared tablespace file when it becomes full, does not apply to file-per-table tablespace files, which are auto-extending regardless of the [innodb\\_autoextend\\_increment](#page-191-1) setting. Initial file-per-table tablespace extensions are by small amounts, after which extensions occur in increments of 4MB.

## <span id="page-32-0"></span>**17.6.3.3 General Tablespaces**

A general tablespace is a shared InnoDB tablespace that is created using CREATE TABLESPACE syntax. General tablespace capabilities and features are described under the following topics in this section:

- [General Tablespace Capabilities](#page-32-2)
- [Creating a General Tablespace](#page-33-0)
- [Adding Tables to a General Tablespace](#page-34-0)
- [General Tablespace Row Format Support](#page-34-1)
- [Moving Tables Between Tablespaces Using ALTER TABLE](#page-35-0)
- [Renaming a General Tablespace](#page-36-0)
- [Dropping a General Tablespace](#page-36-1)
- [General Tablespace Limitations](#page-36-2)

### <span id="page-32-2"></span>**General Tablespace Capabilities**

General tablespaces provide the following capabilities:

- Similar to the system tablespace, general tablespaces are shared tablespaces capable of storing data for multiple tables.
- General tablespaces have a potential memory advantage over [file-per-table tablespaces](#page-30-0). The server keeps tablespace metadata in memory for the lifetime of a tablespace. Multiple tables in fewer

general tablespaces consume less memory for tablespace metadata than the same number of tables in separate file-per-table tablespaces.

- General tablespace data files can be placed in a directory relative to or independent of the MySQL data directory, which provides you with many of the data file and storage management capabilities of [file-per-table tablespaces.](#page-30-0) As with file-per-table tablespaces, the ability to place data files outside of the MySQL data directory allows you to manage performance of critical tables separately, setup RAID or DRBD for specific tables, or bind tables to particular disks, for example.
- General tablespaces support all table row formats and associated features.
- The TABLESPACE option can be used with CREATE TABLE to create tables in a general tablespaces, file-per-table tablespace, or in the system tablespace.
- The TABLESPACE option can be used with ALTER TABLE to move tables between general tablespaces, file-per-table tablespaces, and the system tablespace.

# <span id="page-33-0"></span>**Creating a General Tablespace**

General tablespaces are created using CREATE TABLESPACE syntax.

```
CREATE TABLESPACE tablespace_name
 [ADD DATAFILE 'file_name']
 [FILE_BLOCK_SIZE = value]
 [ENGINE [=] engine_name]
```

A general tablespace can be created in the data directory or outside of it. To avoid conflicts with implicitly created file-per-table tablespaces, creating a general tablespace in a subdirectory under the data directory is not supported. When creating a general tablespace outside of the data directory, the directory must exist and must be known to InnoDB prior to creating the tablespace. To make an unknown directory known to InnoDB, add the directory to the innodb\_directories argument value. innodb\_directories is a read-only startup option. Configuring it requires restarting the server.

### Examples:

Creating a general tablespace in the data directory:

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;
or
mysql> CREATE TABLESPACE `ts1` Engine=InnoDB;
```

The ADD DATAFILE clause is optional. If the ADD DATAFILE clause is not specified when creating a tablespace, a tablespace data file with a unique file name is created implicitly. The unique file name is a 128 bit UUID formatted into five groups of hexadecimal numbers separated by dashes (aaaaaaaabbbb-cccc-dddd-eeeeeeeeeeee). General tablespace data files include an .ibd file extension. In a replication environment, the data file name created on the source is not the same as the data file name created on the replica.

Creating a general tablespace in a directory outside of the data directory:

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE '/my/tablespace/directory/ts1.ibd' Engine=InnoDB;
```

You can specify a path that is relative to the data directory as long as the tablespace directory is not under the data directory. In this example, the my\_tablespace directory is at the same level as the data directory:

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE '../my_tablespace/ts1.ibd' Engine=InnoDB;
```

![](_page_33_Picture_18.jpeg)

#### **Note**

The ENGINE = InnoDB clause must be defined as part of the CREATE TABLESPACE statement, or InnoDB must be defined as the default storage engine (default\_storage\_engine=InnoDB).

### <span id="page-34-0"></span>**Adding Tables to a General Tablespace**

After creating a general tablespace, CREATE TABLE tbl\_name ... TABLESPACE [=] tablespace\_name or ALTER TABLE tbl\_name TABLESPACE [=] tablespace\_name statements can be used to add tables to the tablespace, as shown in the following examples:

CREATE TABLE:

mysql> **CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1;**

ALTER TABLE:

mysql> **ALTER TABLE t2 TABLESPACE ts1;**

Adding table partitions to shared tablespaces is not supported. Shared tablespaces include the InnoDB system tablespace and general tablespaces.

For detailed syntax information, see CREATE TABLE and ALTER TABLE.

### <span id="page-34-1"></span>**General Tablespace Row Format Support**

General tablespaces support all table row formats (REDUNDANT, COMPACT, DYNAMIC, COMPRESSED) with the caveat that compressed and uncompressed tables cannot coexist in the same general tablespace due to different physical page sizes.

For a general tablespace to contain compressed tables (ROW\_FORMAT=COMPRESSED), the FILE\_BLOCK\_SIZE option must be specified, and the FILE\_BLOCK\_SIZE value must be a valid compressed page size in relation to the innodb\_page\_size value. Also, the physical page size of the compressed table (KEY\_BLOCK\_SIZE) must be equal to FILE\_BLOCK\_SIZE/1024. For example, if innodb\_page\_size=16KB and FILE\_BLOCK\_SIZE=8K, the KEY\_BLOCK\_SIZE of the table must be 8.

The following table shows permitted innodb\_page\_size, FILE\_BLOCK\_SIZE, and KEY\_BLOCK\_SIZE combinations. FILE\_BLOCK\_SIZE values may also be specified in bytes. To determine a valid KEY\_BLOCK\_SIZE value for a given FILE\_BLOCK\_SIZE, divide the FILE\_BLOCK\_SIZE value by 1024. Table compression is not support for 32K and 64K InnoDB page sizes. For more information about KEY\_BLOCK\_SIZE, see CREATE TABLE, and [Section 17.9.1.2,](#page-125-0) ["Creating Compressed Tables".](#page-125-0)

**Table 17.3 Permitted Page Size, FILE\_BLOCK\_SIZE, and KEY\_BLOCK\_SIZE Combinations for Compressed Tables**

| InnoDB Page Size<br>(innodb_page_size) | Permitted FILE_BLOCK_SIZE<br>Value | Permitted KEY_BLOCK_SIZE<br>Value                                                                                 |
|----------------------------------------|------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 64KB                                   | 64K (65536)                        | Compression is not supported                                                                                      |
| 32KB                                   | 32K (32768)                        | Compression is not supported                                                                                      |
| 16KB                                   | 16K (16384)                        | None. If innodb_page_size<br>is equal to FILE_BLOCK_SIZE,<br>the tablespace cannot contain a<br>compressed table. |
| 16KB                                   | 8K (8192)                          | 8                                                                                                                 |
| 16KB                                   | 4K (4096)                          | 4                                                                                                                 |
| 16KB                                   | 2K (2048)                          | 2                                                                                                                 |
| 16KB                                   | 1K (1024)                          | 1                                                                                                                 |
| 8KB                                    | 8K (8192)                          | None. If innodb_page_size<br>is equal to FILE_BLOCK_SIZE,<br>the tablespace cannot contain a<br>compressed table. |

| InnoDB Page Size<br>(innodb_page_size) | Permitted FILE_BLOCK_SIZE<br>Value | Permitted KEY_BLOCK_SIZE<br>Value                                                                                 |
|----------------------------------------|------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 8KB                                    | 4K (4096)                          | 4                                                                                                                 |
| 8KB                                    | 2K (2048)                          | 2                                                                                                                 |
| 8KB                                    | 1K (1024)                          | 1                                                                                                                 |
| 4KB                                    | 4K (4096)                          | None. If innodb_page_size<br>is equal to FILE_BLOCK_SIZE,<br>the tablespace cannot contain a<br>compressed table. |
| 4KB                                    | 2K (2048)                          | 2                                                                                                                 |
| 4KB                                    | 1K (1024)                          | 1                                                                                                                 |

This example demonstrates creating a general tablespace and adding a compressed table. The example assumes a default innodb\_page\_size of 16KB. The FILE\_BLOCK\_SIZE of 8192 requires that the compressed table have a KEY\_BLOCK\_SIZE of 8.

```
mysql> CREATE TABLESPACE `ts2` ADD DATAFILE 'ts2.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;
mysql> CREATE TABLE t4 (c1 INT PRIMARY KEY) TABLESPACE ts2 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
```

If you do not specify FILE\_BLOCK\_SIZE when creating a general tablespace, FILE\_BLOCK\_SIZE defaults to innodb\_page\_size. When FILE\_BLOCK\_SIZE is equal to innodb\_page\_size, the tablespace may only contain tables with an uncompressed row format (COMPACT, REDUNDANT, and DYNAMIC row formats).

# <span id="page-35-0"></span>**Moving Tables Between Tablespaces Using ALTER TABLE**

ALTER TABLE with the TABLESPACE option can be used to move a table to an existing general tablespace, to a new file-per-table tablespace, or to the system tablespace.

Adding table partitions to shared tablespaces is not supported. Shared tablespaces include the InnoDB system tablespace and general tablespaces.

To move a table from a file-per-table tablespace or from the system tablespace to a general tablespace, specify the name of the general tablespace. The general tablespace must exist. See ALTER TABLESPACE for more information.

```
ALTER TABLE tbl_name TABLESPACE [=] tablespace_name;
```

To move a table from a general tablespace or file-per-table tablespace to the system tablespace, specify innodb\_system as the tablespace name.

```
ALTER TABLE tbl_name TABLESPACE [=] innodb_system;
```

To move a table from the system tablespace or a general tablespace to a file-per-table tablespace, specify innodb\_file\_per\_table as the tablespace name.

```
ALTER TABLE tbl_name TABLESPACE [=] innodb_file_per_table;
```

ALTER TABLE ... TABLESPACE operations cause a full table rebuild, even if the TABLESPACE attribute has not changed from its previous value.

ALTER TABLE ... TABLESPACE syntax does not support moving a table from a temporary tablespace to a persistent tablespace.

The DATA DIRECTORY clause is permitted with CREATE TABLE ... TABLESPACE=innodb\_file\_per\_table but is otherwise not supported for use in combination with the TABLESPACE option. The directory specified in a DATA DIRECTORY clause must be known to InnoDB. For more information, see Using the DATA DIRECTORY Clause.

Restrictions apply when moving tables from encrypted tablespaces. See [Encryption Limitations.](#page-181-0)

### <span id="page-36-0"></span>**Renaming a General Tablespace**

Renaming a general tablespace is supported using ALTER TABLESPACE ... RENAME TO syntax.

```
ALTER TABLESPACE s1 RENAME TO s2;
```

The CREATE TABLESPACE privilege is required to rename a general tablespace.

RENAME TO operations are implicitly performed in autocommit mode regardless of the autocommit setting.

A RENAME TO operation cannot be performed while LOCK TABLES or FLUSH TABLES WITH READ LOCK is in effect for tables that reside in the tablespace.

Exclusive metadata locks are taken on tables within a general tablespace while the tablespace is renamed, which prevents concurrent DDL. Concurrent DML is supported.

### <span id="page-36-1"></span>**Dropping a General Tablespace**

The DROP TABLESPACE statement is used to drop an InnoDB general tablespace.

All tables must be dropped from the tablespace prior to a DROP TABLESPACE operation. If the tablespace is not empty, DROP TABLESPACE returns an error.

Use a query similar to the following to identify tables in a general tablespace.

```
mysql> SELECT a.NAME AS space_name, b.NAME AS table_name FROM INFORMATION_SCHEMA.INNODB_TABLESPACES a,
 INFORMATION_SCHEMA.INNODB_TABLES b WHERE a.SPACE=b.SPACE AND a.NAME LIKE 'ts1';
+------------+------------+
| space_name | table_name |
+------------+------------+
| ts1 | test/t1 |
| ts1 | test/t2 |
| ts1 | test/t3 |
+------------+------------+
```

A general InnoDB tablespace is not deleted automatically when the last table in the tablespace is dropped. The tablespace must be dropped explicitly using DROP TABLESPACE tablespace\_name.

A general tablespace does not belong to any particular database. A DROP DATABASE operation can drop tables that belong to a general tablespace but it cannot drop the tablespace, even if the DROP DATABASE operation drops all tables that belong to the tablespace.

Similar to the system tablespace, truncating or dropping tables stored in a general tablespace creates free space internally in the general tablespace .ibd data file which can only be used for new InnoDB data. Space is not released back to the operating system as it is when a file-per-table tablespace is deleted during a DROP TABLE operation.

This example demonstrates how to drop an InnoDB general tablespace. The general tablespace ts1 is created with a single table. The table must be dropped before dropping the tablespace.

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1 Engine=InnoDB;
mysql> DROP TABLE t1;
mysql> DROP TABLESPACE ts1;
```

![](_page_36_Picture_18.jpeg)

#### **Note**

tablespace\_name is a case-sensitive identifier in MySQL.

### <span id="page-36-2"></span>**General Tablespace Limitations**

• A generated or existing tablespace cannot be changed to a general tablespace.

- Creation of temporary general tablespaces is not supported.
- General tablespaces do not support temporary tables.
- Similar to the system tablespace, truncating or dropping tables stored in a general tablespace creates free space internally in the general tablespace .ibd data file which can only be used for new InnoDB data. Space is not released back to the operating system as it is for file-per-table tablespaces.

Additionally, a table-copying ALTER TABLE operation on table that resides in a shared tablespace (a general tablespace or the system tablespace) can increase the amount of space used by the tablespace. Such operations require as much additional space as the data in the table plus indexes. The additional space required for the table-copying ALTER TABLE operation is not released back to the operating system as it is for file-per-table tablespaces.

- ALTER TABLE ... DISCARD TABLESPACE and ALTER TABLE ...IMPORT TABLESPACE are not supported for tables that belong to a general tablespace.
- Placing table partitions in general tablespaces is not supported.
- The ADD DATAFILE clause is not supported in a replication environment where the source and replica reside on the same host, as it would cause the source and replica to create a tablespace of the same name in the same location, which is not supported. However, if the ADD DATAFILE clause is omitted, the tablespace is created in the data directory with a generated file name that is unique, which is permitted.
- General tablespaces cannot be created in the undo tablespace directory (innodb\_undo\_directory) unless that directly is known to InnoDB. Known directories are those defined by the datadir, innodb\_data\_home\_dir, and innodb\_directories variables.

## <span id="page-37-1"></span>**17.6.3.4 Undo Tablespaces**

Undo tablespaces contain undo logs, which are collections of records containing information about how to undo the latest change by a transaction to a clustered index record.

Undo tablespaces are described under the following topics in this section:

- [Default Undo Tablespaces](#page-37-0)
- [Undo Tablespace Size](#page-38-0)
- [Adding Undo Tablespaces](#page-38-1)
- [Dropping Undo Tablespaces](#page-39-0)
- [Moving Undo Tablespaces](#page-39-1)
- [Configuring the Number of Rollback Segments](#page-40-0)
- [Truncating Undo Tablespaces](#page-40-1)
- [Undo Tablespace Status Variables](#page-42-0)

### <span id="page-37-0"></span>**Default Undo Tablespaces**

Two default undo tablespaces are created when the MySQL instance is initialized. Default undo tablespaces are created at initialization time to provide a location for rollback segments that must exist before SQL statements can be accepted. A minimum of two undo tablespaces is required to support automated truncation of undo tablespaces. See [Truncating Undo Tablespaces.](#page-40-1)

Default undo tablespaces are created in the location defined by the innodb\_undo\_directory variable. If the innodb\_undo\_directory variable is undefined, default undo tablespaces are created in the data directory. Default undo tablespace data files are named undo\_001 and undo\_002. The

corresponding undo tablespace names defined in the data dictionary are innodb\_undo\_001 and innodb\_undo\_002.

Additional undo tablespaces can be created at runtime using SQL statements. See [Adding Undo](#page-38-1) [Tablespaces.](#page-38-1)

### <span id="page-38-0"></span>**Undo Tablespace Size**

The initial undo tablespace size is normally 16MiB. The initial size may differ when a new undo tablespace is created by a truncate operation. In this case, if the file extension size is larger than 16MB, and the previous file extension occurred within the last second, the new undo tablespace is created at a quarter of the size defined by the innodb\_max\_undo\_log\_size variable.

An undo tablespace is extended by a minimum of 16MB. To handle aggressive growth, the file extension size is doubled if the previous file extension happened less than 0.1 seconds earlier. Doubling of the extension size can occur multiple times to a maximum of 256MB. If the previous file extension occurred more than 0.1 seconds earlier, the extension size is reduced by half, which can also occur multiple times, to a minimum of 16MB. If the AUTOEXTEND\_SIZE option is defined for an undo tablespace, it is extended by the greater of the AUTOEXTEND\_SIZE setting and the extension size determined by the logic described above. For information about the AUTOEXTEND\_SIZE option, see [Section 17.6.3.9, "Tablespace AUTOEXTEND\\_SIZE Configuration"](#page-47-0).

### <span id="page-38-1"></span>**Adding Undo Tablespaces**

Because undo logs can become large during long-running transactions, creating additional undo tablespaces can help prevent individual undo tablespaces from becoming too large. Additional undo tablespaces can be created at runtime using CREATE UNDO TABLESPACE syntax.

```
CREATE UNDO TABLESPACE tablespace_name ADD DATAFILE 'file_name.ibu';
```

The undo tablespace file name must have an .ibu extension. It is not permitted to specify a relative path when defining the undo tablespace file name. A fully qualified path is permitted, but the path must be known to InnoDB. Known paths are those defined by the innodb\_directories variable. Unique undo tablespace file names are recommended to avoid potential file name conflicts when moving or cloning data.

![](_page_38_Picture_10.jpeg)

#### **Note**

In a replication environment, the source and each replica must have its own undo tablespace file directory. Replicating the creation of an undo tablespace file to a common directory would cause a file name conflict.

At startup, directories defined by the innodb\_directories variable are scanned for undo tablespace files. (The scan also traverses subdirectories.) Directories defined by the innodb\_data\_home\_dir, innodb\_undo\_directory, and datadir variables are automatically appended to the innodb\_directories value regardless of whether the innodb\_directories variable is defined explicitly. An undo tablespace can therefore reside in paths defined by any of those variables.

If the undo tablespace file name does not include a path, the undo tablespace is created in the directory defined by the innodb\_undo\_directory variable. If that variable is undefined, the undo tablespace is created in the data directory.

![](_page_38_Picture_15.jpeg)

#### **Note**

The InnoDB recovery process requires that undo tablespace files reside in known directories. Undo tablespace files must be discovered and opened before redo recovery and before other data files are opened to permit uncommitted transactions and data dictionary changes to be rolled back. An undo tablespace not found before recovery cannot be used, which can lead to database inconsistencies. An error message is reported at startup if an undo tablespace known to the data dictionary is not found. The known directory

requirement also supports undo tablespace portability. See [Moving Undo](#page-39-1) [Tablespaces.](#page-39-1)

To create undo tablespaces in a path relative to the data directory, set the innodb\_undo\_directory variable to the relative path, and specify the file name only when creating an undo tablespace.

To view undo tablespace names and paths, query INFORMATION\_SCHEMA.FILES:

```
SELECT TABLESPACE_NAME, FILE_NAME FROM INFORMATION_SCHEMA.FILES
 WHERE FILE_TYPE LIKE 'UNDO LOG';
```

A MySQL instance supports up to 127 undo tablespaces including the two default undo tablespaces created when the MySQL instance is initialized.

Undo tablespaces can be dropped using DROP UNDO TABALESPACE syntax. See [Dropping Undo](#page-39-0) [Tablespaces.](#page-39-0)

## <span id="page-39-0"></span>**Dropping Undo Tablespaces**

Undo tablespaces created using CREATE UNDO TABLESPACE syntax can be dropped at runtime using DROP UNDO TABALESPACE syntax.

An undo tablespace must be empty before it can be dropped. To empty an undo tablespace, the undo tablespace must first be marked as inactive using ALTER UNDO TABLESPACE syntax so that the tablespace is no longer used for assigning rollback segments to new transactions.

```
ALTER UNDO TABLESPACE tablespace_name SET INACTIVE;
```

After an undo tablespace is marked as inactive, transactions currently using rollback segments in the undo tablespace are permitted to finish, as are any transactions started before those transactions are completed. After transactions are completed, the purge system frees the rollback segments in the undo tablespace, and the undo tablespace is truncated to its initial size. (The same process is used when truncating undo tablespaces. See [Truncating Undo Tablespaces.](#page-40-1)) Once the undo tablespace is empty, it can be dropped.

DROP UNDO TABLESPACE tablespace\_name;

![](_page_39_Picture_13.jpeg)

#### **Note**

Alternatively, the undo tablespace can be left in an empty state and reactivated later, if needed, by issuing an ALTER UNDO TABLESPACE tablespace\_name SET ACTIVE statement.

The state of an undo tablespace can be monitored by querying the Information Schema INNODB\_TABLESPACES table.

```
SELECT NAME, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES
 WHERE NAME LIKE 'tablespace_name';
```

An inactive state indicates that rollback segments in an undo tablespace are no longer used by new transactions. An empty state indicates that an undo tablespace is empty and ready to be dropped, or ready to be made active again using an ALTER UNDO TABLESPACE tablespace\_name SET ACTIVE statement. Attempting to drop an undo tablespace that is not empty returns an error.

The default undo tablespaces (innodb\_undo\_001 and innodb\_undo\_002) created when the MySQL instance is initialized cannot be dropped. They can, however, be made inactive using an ALTER UNDO TABLESPACE tablespace\_name SET INACTIVE statement. Before a default undo tablespace can be made inactive, there must be an undo tablespace to take its place. A minimum of two active undo tablespaces are required at all times to support automated truncation of undo tablespaces.

## <span id="page-39-1"></span>**Moving Undo Tablespaces**

Undo tablespaces created with CREATE UNDO TABLESPACE syntax can be moved while the server is offline to any known directory. Known directories are those defined by the innodb\_directories variable. Directories defined by innodb\_data\_home\_dir, innodb\_undo\_directory, and datadir are automatically appended to the innodb\_directories value regardless of whether the innodb\_directories variable is defined explicitly. Those directories and their subdirectories are scanned at startup for undo tablespaces files. An undo tablespace file moved to any of those directories is discovered at startup and assumed to be the undo tablespace that was moved.

The default undo tablespaces (innodb\_undo\_001 and innodb\_undo\_002) created when the MySQL instance is initialized must reside in the directory defined by the innodb\_undo\_directory variable. If the innodb\_undo\_directory variable is undefined, default undo tablespaces reside in the data directory. If default undo tablespaces are moved while the server is offline, the server must be started with the innodb\_undo\_directory variable configured to the new directory.

The I/O patterns for undo logs make undo tablespaces good candidates for SSD storage.

### <span id="page-40-0"></span>**Configuring the Number of Rollback Segments**

The innodb\_rollback\_segments variable defines the number of rollback segments allocated to each undo tablespace and to the global temporary tablespace. The innodb\_rollback\_segments variable can be configured at startup or while the server is running.

The default setting for innodb\_rollback\_segments is 128, which is also the maximum value. For information about the number of transactions that a rollback segment supports, see [Section 17.6.6,](#page-56-0) ["Undo Logs"](#page-56-0).

### <span id="page-40-1"></span>**Truncating Undo Tablespaces**

There are two methods of truncating undo tablespaces, which can be used individually or in combination to manage undo tablespace size. One method is automated, enabled using configuration variables. The other method is manual, performed using SQL statements.

The automated method does not require monitoring undo tablespace size and, once enabled, it performs deactivation, truncation, and reactivation of undo tablespaces without manual intervention. The manual truncation method may be preferable if you want to control when undo tablespaces are taken offline for truncation. For example, you may want to avoid truncating undo tablespaces during peak workload times.

#### **Automated Truncation**

Automated truncation of undo tablespaces requires a minimum of two active undo tablespaces, which ensures that one undo tablespace remains active while the other is taken offline to be truncated. By default, two undo tablespaces are created when the MySQL instance is initialized.

To have undo tablespaces automatically truncated, enable the innodb\_undo\_log\_truncate variable. For example:

```
mysql> SET GLOBAL innodb_undo_log_truncate=ON;
```

When the innodb\_undo\_log\_truncate variable is enabled, undo tablespaces that exceed the size limit defined by the innodb\_max\_undo\_log\_size variable are subject to truncation. The innodb\_max\_undo\_log\_size variable is dynamic and has a default value of 1073741824 bytes (1024 MiB).

```
mysql> SELECT @@innodb_max_undo_log_size;
+----------------------------+
| @@innodb_max_undo_log_size |
+----------------------------+
| 1073741824 |
+----------------------------+
```

When the innodb\_undo\_log\_truncate variable is enabled:

1. Default and user-defined undo tablespaces that exceed the innodb\_max\_undo\_log\_size setting are marked for truncation. Selection of an undo tablespace for truncation is performed in a circular fashion to avoid truncating the same undo tablespace each time.

- 2. Rollback segments residing in the selected undo tablespace are made inactive so that they are not assigned to new transactions. Existing transactions that are currently using rollback segments are permitted to finish.
- 3. The purge system empties rollback segments by freeing undo logs that are no longer in use.
- 4. After all rollback segments in the undo tablespace are freed, the truncate operation runs and truncates the undo tablespace to 16MB.

The innodb\_undo\_directory variable defines the location of default undo tablespace files. If the innodb\_undo\_directory variable is undefined, default undo tablespaces reside in the data directory. The location of all undo tablespace files including user-defined undo tablespaces created using CREATE UNDO TABLESPACE syntax can be determined by querying the Information Schema FILES table:

```
SELECT TABLESPACE_NAME, FILE_NAME FROM INFORMATION_SCHEMA.FILES WHERE FILE_TYPE LIKE 'UNDO LOG';
```

5. Rollback segments are reactivated so that they can be assigned to new transactions.

### **Manual Truncation**

Manual truncation of undo tablespaces requires a minimum of three active undo tablespaces. Two active undo tablespaces are required at all times to support the possibility that automated truncation is enabled. A minimum of three undo tablespaces satisfies this requirement while permitting an undo tablespace to be taken offline manually.

To manually initiate truncation of an undo tablespace, deactivate the undo tablespace by issuing the following statement:

```
ALTER UNDO TABLESPACE tablespace_name SET INACTIVE;
```

After the undo tablespace is marked as inactive, transactions currently using rollback segments in the undo tablespace are permitted to finish, as are any transactions started before those transactions are completed. After transactions are completed, the purge system frees the rollback segments in the undo tablespace, the undo tablespace is truncated to its initial size, and the undo tablespace state changes from inactive to empty.

![](_page_41_Picture_12.jpeg)

#### **Note**

When an ALTER UNDO TABLESPACE tablespace\_name SET INACTIVE statement deactivates an undo tablespace, the purge thread looks for that undo tablespace at the next opportunity. Once the undo tablespace is found and marked for truncation, the purge thread returns with increased frequency to quickly empty and truncate the undo tablespace.

To check the state of an undo tablespace, query the Information Schema INNODB\_TABLESPACES table.

```
SELECT NAME, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES
 WHERE NAME LIKE 'tablespace_name';
```

Once the undo tablespace is in an empty state, it can be reactivated by issuing the following statement:

```
ALTER UNDO TABLESPACE tablespace_name SET ACTIVE;
```

An undo tablespace in an empty state can also be dropped. See [Dropping Undo Tablespaces](#page-39-0).

#### **Expediting Automated Truncation of Undo Tablespaces**

The purge thread is responsible for emptying and truncating undo tablespaces. By default, the purge thread looks for undo tablespaces to truncate once every 128 times that purge is invoked. The frequency with which the purge thread looks for undo tablespaces to truncate is controlled by the innodb\_purge\_rseg\_truncate\_frequency variable, which has a default setting of 128.

```
mysql> SELECT @@innodb_purge_rseg_truncate_frequency;
+----------------------------------------+
| @@innodb_purge_rseg_truncate_frequency |
+----------------------------------------+
| 128 |
+----------------------------------------+
```

To increase the frequency, decrease the innodb\_purge\_rseg\_truncate\_frequency setting. For example, to have the purge thread look for undo tablespaces once every 32 times that purge is invoked, set innodb\_purge\_rseg\_truncate\_frequency to 32.

```
mysql> SET GLOBAL innodb_purge_rseg_truncate_frequency=32;
```

#### **Performance Impact of Truncating Undo Tablespace Files**

When an undo tablespace is truncated, the rollback segments in the undo tablespace are deactivated. The active rollback segments in other undo tablespaces assume responsibility for the entire system load, which may result in a slight performance degradation. The extent to which performance is affected depends on a number of factors:

- Number of undo tablespaces
- Number of undo logs
- Undo tablespace size
- Speed of the I/O subsystem
- Existing long running transactions
- System load

The easiest way to avoid the potential performance impact is to increase the number of undo tablespaces.

#### **Monitoring Undo Tablespace Truncation**

undo and purge subsystem counters are provided for monitoring background activities associated with undo log truncation. For counter names and descriptions, query the Information Schema INNODB\_METRICS table.

```
SELECT NAME, SUBSYSTEM, COMMENT FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME LIKE '%truncate%';
```

For information about enabling counters and querying counter data, see Section 17.15.6, "InnoDB INFORMATION\_SCHEMA Metrics Table".

#### **Undo Tablespace Truncation Limit**

The number of truncate operations on the same undo tablespace between checkpoints is limited to 64. The limit prevents potential issues caused by an excessive number of undo tablespace truncate operations, which can occur if innodb\_max\_undo\_log\_size is set too low on a busy system, for example. If the limit is exceeded, an undo tablespace can still be made inactive, but it is not truncated until after the next checkpoint. In MySQL 8.4 the limit is 50000.

#### **Undo Tablespace Truncation Recovery**

An undo tablespace truncate operation creates a temporary undo\_space\_number\_trunc.log file in the server log directory. That log directory is defined by innodb\_log\_group\_home\_dir. If a system failure occurs during the truncate operation, the temporary log file permits the startup process to identify undo tablespaces that were being truncated and to continue the operation.

### <span id="page-42-0"></span>**Undo Tablespace Status Variables**

The following status variables permit tracking the total number of undo tablespaces, implicit (InnoDBcreated) undo tablespaces, explicit (user-created) undo tablespaces, and the number of active undo tablespaces:

```
mysql> SHOW STATUS LIKE 'Innodb_undo_tablespaces%';
+----------------------------------+-------+
| Variable_name | Value |
+----------------------------------+-------+
| Innodb_undo_tablespaces_total | 2 |
| Innodb_undo_tablespaces_implicit | 2 |
| Innodb_undo_tablespaces_explicit | 0 |
| Innodb_undo_tablespaces_active | 2 |
+----------------------------------+-------+
```

For status variable descriptions, see Section 7.1.10, "Server Status Variables".