---
source: MySQL 5.7 Reference
title: 00_Overview
---

The system tablespace is the storage area for the InnoDB data dictionary, the doublewrite buffer, the change buffer, and undo logs. It may also contain table and index data if tables are created in the system tablespace rather than file-per-table or general tablespaces.

The system tablespace can have one or more data files. By default, a single system tablespace data file, named ibdata1, is created in the data directory. The size and number of system tablespace data files is defined by the innodb\_data\_file\_path startup option. For configuration information, see [System Tablespace Data File Configuration.](#page-86-0)

Additional information about the system tablespace is provided under the following topics in the section:

- [Resizing the System Tablespace](#page-48-2)
- [Using Raw Disk Partitions for the System Tablespace](#page-50-0)

#### <span id="page-48-2"></span>**Resizing the System Tablespace**

This section describes how to increase or decrease the size of the system tablespace.

### **Increasing the Size of the System Tablespace**

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

![](_page_49_Picture_15.jpeg)

#### **Note**

You cannot increase the size of an existing system tablespace data file by changing its size attribute. For example, changing the innodb\_data\_file\_path setting from ibdata1:10M:autoextend to ibdata1:12M:autoextend produces the following error when starting the server:

```
[ERROR] [MY-012263] [InnoDB] The Auto-extending innodb_system
data file './ibdata1' is of a different size 640 pages (rounded down to MB) than
specified in the .cnf file: initial 768 pages, max 0 (relevant if non-zero) pages!
```

The error indicates that the existing data file size (expressed in InnoDB pages) is different from the data file size specified in the configuration file. If you encounter this error, restore the previous innodb\_data\_file\_path setting, and refer to the system tablespace resizing instructions.

#### **Decreasing the Size of the InnoDB System Tablespace**

You cannot remove a data file from the system tablespace. To decrease the system tablespace size, use this procedure:

1. Use mysqldump to dump all of your InnoDB tables, including InnoDB tables located in the mysql schema. Identify InnoDB tables in the mysql schema using the following query:

```
mysql> SELECT TABLE_NAME from INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='mysql' and ENGINE='InnoDB';
+---------------------------+
| TABLE_NAME |
+---------------------------+
| engine_cost |
| gtid_executed |
| help_category |
| help_keyword |
| help_relation |
| help_topic |
| innodb_index_stats |
| innodb_table_stats |
| plugin |
| server_cost |
| servers |
| slave_master_info |
| slave_relay_log_info |
| slave_worker_info |
| time_zone |
| time_zone_leap_second |
| time_zone_name |
| time_zone_transition |
| time_zone_transition_type |
+---------------------------+
```

- 2. Stop the server.
- 3. Remove all of the existing tablespace files (\*.ibd), including the ibdata and ib\_log files. Do not forget to remove \*.ibd files for tables located in the mysql schema.
- 4. Remove any .frm files for InnoDB tables.
- 5. Configure the data files for the new system tablespace. See [System Tablespace Data File](#page-86-0) [Configuration](#page-86-0).
- 6. Restart the server.
- 7. Import the dump files.

![](_page_50_Picture_9.jpeg)

#### **Note**

If your databases only use the InnoDB engine, it may be simpler to dump **all** databases, stop the server, remove all databases and InnoDB log files, restart the server, and import the dump files.

To avoid a large system tablespace, consider using file-per-table tablespaces or general tablespaces for your data. File-per-table tablespaces are the default tablespace type and are used implicitly when creating an InnoDB table. Unlike the system tablespace, file-per-table tablespaces return disk space to the operating system when they are truncated or dropped. For more information, see [Section 14.6.3.2,](#page-51-0) ["File-Per-Table Tablespaces"](#page-51-0). General tablespaces are multi-table tablespaces that can also be used as an alternative to the system tablespace. See [Section 14.6.3.3, "General Tablespaces"](#page-53-0).

#### <span id="page-50-0"></span>**Using Raw Disk Partitions for the System Tablespace**

Raw disk partitions can be used as system tablespace data files. This technique enables nonbuffered I/ O on Windows and some Linux and Unix systems without file system overhead. Perform tests with and without raw partitions to verify whether they improve performance on your system.

When using a raw disk partition, ensure that the user ID that runs the MySQL server has read and write privileges for that partition. For example, if running the server as the mysql user, the partition must be readable and writeable by mysql. If running the server with the --memlock option, the server must be run as root, so the partition must be readable and writeable by root.

The procedures described below involve option file modification. For additional information, see Section 4.2.2.2, "Using Option Files".

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

## <span id="page-51-0"></span>**14.6.3.2 File-Per-Table Tablespaces**

A file-per-table tablespace contains data and indexes for a single InnoDB table, and is stored on the file system in a single data file.

File-per-table tablespace characteristics are described under the following topics in this section:

- [File-Per-Table Tablespace Configuration](#page-51-1)
- [File-Per-Table Tablespace Data Files](#page-52-0)
- [File-Per-Table Tablespace Advantages](#page-52-1)
- [File-Per-Table Tablespace Disadvantages](#page-53-1)

#### <span id="page-51-1"></span>**File-Per-Table Tablespace Configuration**

InnoDB creates tables in file-per-table tablespaces by default. This behavior is controlled by the innodb\_file\_per\_table variable. Disabling innodb\_file\_per\_table causes InnoDB to create tables in the system tablespace.

An innodb\_file\_per\_table setting can be specified in an option file or configured at runtime using a SET GLOBAL statement. Changing the setting at runtime requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges".

### Option file:

```
[mysqld]
innodb_file_per_table=ON
```

Using SET GLOBAL at runtime:

```
mysql> SET GLOBAL innodb_file_per_table=ON;
```

innodb\_file\_per\_table is enabled by default in MySQL 5.6 and higher. You might consider disabling it if backward compatibility with earlier versions of MySQL is a concern.

![](_page_52_Picture_3.jpeg)

#### **Warning**

Disabling innodb\_file\_per\_table prevents table-copying ALTER TABLE operations from implicitly moving a table that resides in the system tablespace to a file-per-table tablespace. A table-copying ALTER TABLE operation recreates the table using the current innodb\_file\_per\_table setting. This behavior does not apply when adding or dropping secondary indexes, nor does it apply to ALTER TABLE operations that use the INPLACE algorithm, or to tables added to the system tablespace using CREATE TABLE ... TABLESPACE or ALTER TABLE ... TABLESPACE syntax.

# <span id="page-52-0"></span>**File-Per-Table Tablespace Data Files**

A file-per-table tablespace is created in an .ibd data file in a schema directory under the MySQL data directory. The .ibd file is named for the table (table\_name.ibd). For example, the data file for table test.t1 is created in the test directory under the MySQL data directory:

```
mysql> USE test;
mysql> CREATE TABLE t1 (
 id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(100)
 ) ENGINE = InnoDB;
$> cd /path/to/mysql/data/test
$> ls
t1.ibd
```

You can use the DATA DIRECTORY clause of the CREATE TABLE statement to implicitly create a fileper-table tablespace data file outside of the data directory. For more information, see [Section 14.6.1.2,](#page-20-1) ["Creating Tables Externally".](#page-20-1)

#### <span id="page-52-1"></span>**File-Per-Table Tablespace Advantages**

File-per-table tablespaces have the following advantages over shared tablespaces such as the system tablespace or general tablespaces.

- Disk space is returned to the operating system after truncating or dropping a table created in a fileper-table tablespace. Truncating or dropping a table stored in a shared tablespace creates free space within the shared tablespace data file, which can only be used for InnoDB data. In other words, a shared tablespace data file does not shrink in size after a table is truncated or dropped.
- A table-copying ALTER TABLE operation on a table that resides in a shared tablespace can increase the amount of disk space occupied by the tablespace. Such operations may require as much additional space as the data in the table plus indexes. This space is not released back to the operating system as it is for file-per-table tablespaces.
- TRUNCATE TABLE performance is better when executed on tables that reside in file-per-table tablespaces.
- File-per-table tablespace data files can be created on separate storage devices for I/O optimization, space management, or backup purposes. See [Section 14.6.1.2, "Creating Tables Externally"](#page-20-1).
- You can import a table that resides in a file-per-table tablespace from another MySQL instance. See [Section 14.6.1.3, "Importing InnoDB Tables"](#page-22-3).
- Tables created in file-per-table tablespaces use the Barracuda file format. See [Section 14.10,](#page-140-0) ["InnoDB File-Format Management"](#page-140-0). The Barracuda file format enables features associated with DYNAMIC and COMPRESSED row formats. See [Section 14.11, "InnoDB Row Formats"](#page-145-1).

- Tables stored in individual tablespace data files can save time and improve chances for a successful recovery when data corruption occurs, when backups or binary logs are unavailable, or when the MySQL server instance cannot be restarted.
- You can backup or restore tables created in file-per-table tablespaces quickly using MySQL Enterprise Backup, without interrupting the use of other InnoDB tables. This is beneficial for tables on varying backup schedules or that require backup less frequently. See [Making a Partial Backup](https://dev.mysql.com/doc/mysql-enterprise-backup/4.1/en/partial.md) for details.
- File-per-table tablespaces permit monitoring table size on the file system by monitoring the size of the tablespace data file.
- Common Linux file systems do not permit concurrent writes to a single file such as a shared tablespace data file when innodb\_flush\_method is set to O\_DIRECT. As a result, there are possible performance improvements when using file-per-table tablespaces in conjunction with this setting.
- Tables in a shared tablespace are limited in size by the 64TB tablespace size limit. By comparison, each file-per-table tablespace has a 64TB size limit, which provides plenty of room for individual tables to grow in size.

#### <span id="page-53-1"></span>**File-Per-Table Tablespace Disadvantages**

File-per-table tablespaces have the following disadvantages compared to shared tablespaces such as the system tablespace or general tablespaces.

- With file-per-table tablespaces, each table may have unused space that can only be utilized by rows of the same table, which can lead to wasted space if not properly managed.
- fsync operations are performed on multiple file-per-table data files instead of a single shared tablespace data file. Because fsync operations are per file, write operations for multiple tables cannot be combined, which can result in a higher total number of fsync operations.
- mysqld must keep an open file handle for each file-per-table tablespace, which may impact performance if you have numerous tables in file-per-table tablespaces.
- More file descriptors are required when each table has its own data file.
- There is potential for more fragmentation, which can impede DROP TABLE and table scan performance. However, if fragmentation is managed, file-per-table tablespaces can improve performance for these operations.
- The buffer pool is scanned when dropping a table that resides in a file-per-table tablespace, which can take several seconds for large buffer pools. The scan is performed with a broad internal lock, which may delay other operations.
- The [innodb\\_autoextend\\_increment](#page-191-1) variable, which defines the increment size for extending the size of an auto-extending shared tablespace file when it becomes full, does not apply to file-per-table tablespace files, which are auto-extending regardless of the [innodb\\_autoextend\\_increment](#page-191-1) setting. Initial file-per-table tablespace extensions are by small amounts, after which extensions occur in increments of 4MB.

# <span id="page-53-0"></span>**14.6.3.3 General Tablespaces**

A general tablespace is a shared InnoDB tablespace that is created using CREATE TABLESPACE syntax. General tablespace capabilities and features are described under the following topics in this section:

- [General Tablespace Capabilities](#page-54-1)
- [Creating a General Tablespace](#page-54-0)

- [Adding Tables to a General Tablespace](#page-55-0)
- [General Tablespace Row Format Support](#page-55-1)
- [Moving Tables Between Tablespaces Using ALTER TABLE](#page-56-0)
- [Dropping a General Tablespace](#page-57-0)
- [General Tablespace Limitations](#page-58-1)

## <span id="page-54-1"></span>**General Tablespace Capabilities**

General tablespaces provide the following capabilities:

- Similar to the system tablespace, general tablespaces are shared tablespaces capable of storing data for multiple tables.
- General tablespaces have a potential memory advantage over [file-per-table tablespaces](#page-51-0). The server keeps tablespace metadata in memory for the lifetime of a tablespace. Multiple tables in fewer general tablespaces consume less memory for tablespace metadata than the same number of tables in separate file-per-table tablespaces.
- General tablespace data files can be placed in a directory relative to or independent of the MySQL data directory, which provides you with many of the data file and storage management capabilities of [file-per-table tablespaces.](#page-51-0) As with file-per-table tablespaces, the ability to place data files outside of the MySQL data directory allows you to manage performance of critical tables separately, setup RAID or DRBD for specific tables, or bind tables to particular disks, for example.
- General tablespaces support both Antelope and Barracuda file formats, and therefore support all table row formats and associated features. With support for both file formats, general tablespaces have no dependence on innodb\_file\_format or innodb\_file\_per\_table settings, nor do these variables have any effect on general tablespaces.
- The TABLESPACE option can be used with CREATE TABLE to create tables in a general tablespaces, file-per-table tablespace, or in the system tablespace.
- The TABLESPACE option can be used with ALTER TABLE to move tables between general tablespaces, file-per-table tablespaces, and the system tablespace.

# <span id="page-54-0"></span>**Creating a General Tablespace**

General tablespaces are created using CREATE TABLESPACE syntax.

```
CREATE TABLESPACE tablespace_name
 ADD DATAFILE 'file_name'
 [FILE_BLOCK_SIZE = value]
 [ENGINE [=] engine_name]
```

A general tablespace can be created in the data directory or outside of it. To avoid conflicts with implicitly created file-per-table tablespaces, creating a general tablespace in a subdirectory under the data directory is not supported. When creating a general tablespace outside of the data directory, the directory must exist prior to creating the tablespace.

An .isl file is created in the MySQL data directory when a general tablespace is created outside of the MySQL data directory.

Examples:

Creating a general tablespace in the data directory:

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;
```

Creating a general tablespace in a directory outside of the data directory:

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE '/my/tablespace/directory/ts1.ibd' Engine=InnoDB;
```

You can specify a path that is relative to the data directory as long as the tablespace directory is not under the data directory. In this example, the my\_tablespace directory is at the same level as the data directory:

mysql> **CREATE TABLESPACE `ts1` ADD DATAFILE '../my\_tablespace/ts1.ibd' Engine=InnoDB;**

![](_page_55_Picture_3.jpeg)

#### **Note**

The ENGINE = InnoDB clause must be defined as part of the CREATE TABLESPACE statement, or InnoDB must be defined as the default storage engine (default\_storage\_engine=InnoDB).

### <span id="page-55-0"></span>**Adding Tables to a General Tablespace**

After creating a general tablespace, CREATE TABLE tbl\_name ... TABLESPACE [=] tablespace\_name or ALTER TABLE tbl\_name TABLESPACE [=] tablespace\_name statements can be used to add tables to the tablespace, as shown in the following examples:

CREATE TABLE:

mysql> **CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1;**

ALTER TABLE:

mysql> **ALTER TABLE t2 TABLESPACE ts1;**

![](_page_55_Picture_12.jpeg)

#### **Note**

Support for adding table partitions to shared tablespaces was deprecated in MySQL 5.7.24; expect it to be removed in a future version of MySQL. Shared tablespaces include the InnoDB system tablespace and general tablespaces.

For detailed syntax information, see CREATE TABLE and ALTER TABLE.

### <span id="page-55-1"></span>**General Tablespace Row Format Support**

General tablespaces support all table row formats (REDUNDANT, COMPACT, DYNAMIC, COMPRESSED) with the caveat that compressed and uncompressed tables cannot coexist in the same general tablespace due to different physical page sizes.

For a general tablespace to contain compressed tables (ROW\_FORMAT=COMPRESSED), the FILE\_BLOCK\_SIZE option must be specified, and the FILE\_BLOCK\_SIZE value must be a valid compressed page size in relation to the innodb\_page\_size value. Also, the physical page size of the compressed table (KEY\_BLOCK\_SIZE) must be equal to FILE\_BLOCK\_SIZE/1024. For example, if innodb\_page\_size=16KB and FILE\_BLOCK\_SIZE=8K, the KEY\_BLOCK\_SIZE of the table must be 8.

The following table shows permitted innodb\_page\_size, FILE\_BLOCK\_SIZE, and KEY\_BLOCK\_SIZE combinations. FILE\_BLOCK\_SIZE values may also be specified in bytes. To determine a valid KEY\_BLOCK\_SIZE value for a given FILE\_BLOCK\_SIZE, divide the FILE\_BLOCK\_SIZE value by 1024. Table compression is not support for 32K and 64K InnoDB page sizes. For more information about KEY\_BLOCK\_SIZE, see CREATE TABLE, and [Section 14.9.1.2,](#page-123-1) ["Creating Compressed Tables".](#page-123-1)

**Table 14.3 Permitted Page Size, FILE\_BLOCK\_SIZE, and KEY\_BLOCK\_SIZE Combinations for Compressed Tables**

| InnoDB Page Size<br>Permitted FILE_BLOCK_SIZE<br>(innodb_page_size)<br>Value |             | Permitted KEY_BLOCK_SIZE<br>Value |
|------------------------------------------------------------------------------|-------------|-----------------------------------|
| 64KB                                                                         | 64K (65536) | Compression is not supported      |
| 32KB                                                                         | 32K (32768) | Compression is not supported      |

| InnoDB Page Size<br>(innodb_page_size) | Permitted FILE_BLOCK_SIZE<br>Value | Permitted KEY_BLOCK_SIZE<br>Value                                                                                 |
|----------------------------------------|------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 16KB                                   | 16K (16384)                        | None. If innodb_page_size<br>is equal to FILE_BLOCK_SIZE,<br>the tablespace cannot contain a<br>compressed table. |
| 16KB                                   | 8K (8192)                          | 8                                                                                                                 |
| 16KB                                   | 4K (4096)                          | 4                                                                                                                 |
| 16KB                                   | 2K (2048)                          | 2                                                                                                                 |
| 16KB                                   | 1K (1024)                          | 1                                                                                                                 |
| 8KB                                    | 8K (8192)                          | None. If innodb_page_size<br>is equal to FILE_BLOCK_SIZE,<br>the tablespace cannot contain a<br>compressed table. |
| 8KB                                    | 4K (4096)                          | 4                                                                                                                 |
| 8KB                                    | 2K (2048)                          | 2                                                                                                                 |
| 8KB                                    | 1K (1024)                          | 1                                                                                                                 |
| 4KB                                    | 4K (4096)                          | None. If innodb_page_size<br>is equal to FILE_BLOCK_SIZE,<br>the tablespace cannot contain a<br>compressed table. |
| 4K                                     | 2K (2048)                          | 2                                                                                                                 |
| 4KB                                    | 1K (1024)                          | 1                                                                                                                 |

This example demonstrates creating a general tablespace and adding a compressed table. The example assumes a default innodb\_page\_size of 16KB. The FILE\_BLOCK\_SIZE of 8192 requires that the compressed table have a KEY\_BLOCK\_SIZE of 8.

```
mysql> CREATE TABLESPACE `ts2` ADD DATAFILE 'ts2.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;
mysql> CREATE TABLE t4 (c1 INT PRIMARY KEY) TABLESPACE ts2 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
```

If you do not specify FILE\_BLOCK\_SIZE when creating a general tablespace, FILE\_BLOCK\_SIZE defaults to innodb\_page\_size. When FILE\_BLOCK\_SIZE is equal to innodb\_page\_size, the tablespace may only contain tables with an uncompressed row format (COMPACT, REDUNDANT, and DYNAMIC row formats).

#### <span id="page-56-0"></span>**Moving Tables Between Tablespaces Using ALTER TABLE**

ALTER TABLE with the TABLESPACE option can be used to move a table to an existing general tablespace, to a new file-per-table tablespace, or to the system tablespace.

![](_page_56_Picture_7.jpeg)

#### **Note**

Support for placing table partitions in shared tablespaces was deprecated in MySQL 5.7.24; expect it to be removed in a future version of MySQL. Shared tablespaces include the InnoDB system tablespace and general tablespaces.

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

The DATA DIRECTORY clause is permitted with CREATE TABLE ... TABLESPACE=innodb\_file\_per\_table but is otherwise not supported for use in combination with the TABLESPACE option.

Restrictions apply when moving tables from encrypted tablespaces. See [Encryption Limitations.](#page-178-1)

#### <span id="page-57-0"></span>**Dropping a General Tablespace**

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

If a DROP TABLESPACE operation on an empty general tablespace returns an error, the tablespace may contain an orphan temporary or intermediate table that was left by an ALTER TABLE operation that was interrupted by a server exit. For more information, see Section 14.22.3, "Troubleshooting InnoDB Data Dictionary Operations".

A general InnoDB tablespace is not deleted automatically when the last table in the tablespace is dropped. The tablespace must be dropped explicitly using DROP TABLESPACE tablespace\_name.

A general tablespace does not belong to any particular database. A DROP DATABASE operation can drop tables that belong to a general tablespace but it cannot drop the tablespace, even if the DROP DATABASE operation drops all tables that belong to the tablespace.

Similar to the system tablespace, truncating or dropping tables stored in a general tablespace creates free space internally in the general tablespace .ibd data file which can only be used for new InnoDB data. Space is not released back to the operating system as it is when a file-per-table tablespace is deleted during a DROP TABLE operation.

This example demonstrates how to drop an InnoDB general tablespace. The general tablespace ts1 is created with a single table. The table must be dropped before dropping the tablespace.

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1 Engine=InnoDB;
mysql> DROP TABLE t1;
```

mysql> **DROP TABLESPACE ts1;**

![](_page_58_Picture_2.jpeg)

#### **Note**

tablespace\_name is a case-sensitive identifier in MySQL.

### <span id="page-58-1"></span>**General Tablespace Limitations**

- A generated or existing tablespace cannot be changed to a general tablespace.
- Creation of temporary general tablespaces is not supported.
- General tablespaces do not support temporary tables.
- Tables stored in a general tablespace may only be opened in MySQL releases that support general tablespaces.
- Similar to the system tablespace, truncating or dropping tables stored in a general tablespace creates free space internally in the general tablespace .ibd data file which can only be used for new InnoDB data. Space is not released back to the operating system as it is for file-per-table tablespaces.

Additionally, a table-copying ALTER TABLE operation on table that resides in a shared tablespace (a general tablespace or the system tablespace) can increase the amount of space used by the tablespace. Such operations require as much additional space as the data in the table plus indexes. The additional space required for the table-copying ALTER TABLE operation is not released back to the operating system as it is for file-per-table tablespaces.

- ALTER TABLE ... DISCARD TABLESPACE and ALTER TABLE ...IMPORT TABLESPACE are not supported for tables that belong to a general tablespace.
- Support for placing table partitions in general tablespaces was deprecated in MySQL 5.7.24; expect it to be removed in a future version of MySQL.
- The ADD DATAFILE clause is not supported in a replication environment where the source and replica reside on the same host, as it would cause the source and replica to create a tablespace of the same name in the same location.

## <span id="page-58-0"></span>**14.6.3.4 Undo Tablespaces**

Undo tablespaces contain undo logs, which are collections of records containing information about how to undo the latest change by a transaction to a clustered index record.

Undo logs are stored in the system tablespace by default but can be stored in one or more undo tablespaces instead. Using undo tablespaces can reducing the amount of space required for undo logs in any one tablespace. The I/O patterns for undo logs also make undo tablespaces good candidates for SSD storage.

The number of undo tablespaces used by InnoDB is controlled by the innodb\_undo\_tablespaces option. This option can only be configured when initializing the MySQL instance. It cannot be changed afterward.

![](_page_58_Picture_19.jpeg)

# **Note**

The innodb\_undo\_tablespaces option is deprecated; expect it to be removed in a future release.

Undo tablespaces and individual segments inside those tablespaces cannot be dropped. However, undo logs stored in undo tablespaces can be truncated. For more information, see [Truncating Undo](#page-59-0) [Tablespaces.](#page-59-0)

#### **Configuring Undo Tablespaces**

This procedure describes how to configure undo tablespaces. When undo tablespaces are configured, undo logs are stored in the undo tablespaces instead of the system tablespace.

The number of undo tablespaces can only be configured when initializing a MySQL instance and is fixed for the life of the instance, so it is recommended that you perform the following procedure on a test instance with a representative workload before deploying the configuration to a production system.

To configure undo tablespaces:

- 1. Specify a directory location for undo tablespaces using the innodb\_undo\_directory variable. If a directory location is not specified, undo tablespaces are created in the data directory.
- 2. Define the number of rollback segments using the innodb\_rollback\_segments variable. Start with a relatively low value and increase it incrementally over time to examine the effect on performance. The default setting for innodb\_rollback\_segments is 128, which is also the maximum value.

One rollback segment is always assigned to the system tablespace, and 32 rollback segments are reserved for the temporary tablespace (ibtmp1). Therefore, to allocate rollback segments to undo tablespaces, set innodb\_rollback\_segments to a value greater than 33. For example, if you have two undo tablespaces, set innodb\_rollback\_segments to 35 to assign one rollback segment to each of the two undo tablespaces. Rollback segments are distributed among undo tablespaces in a circular fashion.

When you add undo tablespaces, the rollback segment in the system tablespace is rendered inactive.

- 3. Define the number of undo tablespaces using the innodb\_undo\_tablespaces option. The specified number of undo tablespaces is fixed for the life of the MySQL instance, so if you are uncertain about an optimal value, estimate on the high side.
- 4. Create a new MySQL test instance using the configuration settings you have chosen.
- 5. Use a realistic workload on your test instance with data volume similar to your production servers to test the configuration.
- 6. Benchmark the performance of I/O intensive workloads.
- 7. Periodically increase the value of innodb\_rollback\_segments and rerun performance tests until there are no further improvements in I/O performance.

# <span id="page-59-0"></span>**Truncating Undo Tablespaces**

Truncating undo tablespaces requires that the MySQL instance have a minimum of two active undo tablespaces, which ensures that one undo tablespace remains active while the other is taken offline to be truncated. The number of undo tablespaces is defined by the innodb\_undo\_tablespaces variable. The default value is 0. Use this statement to check the value of innodb\_undo\_tablespaces:

```
mysql> SELECT @@innodb_undo_tablespaces;
+---------------------------+
| @@innodb_undo_tablespaces |
+---------------------------+
| 2 |
+---------------------------+
```

To have undo tablespaces truncated, enable the innodb\_undo\_log\_truncate variable. For example:

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

- 1. Undo tablespaces that exceed the innodb\_max\_undo\_log\_size setting are marked for truncation. Selection of an undo tablespace for truncation is performed in a circular fashion to avoid truncating the same undo tablespace each time.
- 2. Rollback segments residing in the selected undo tablespace are made inactive so that they are not assigned to new transactions. Existing transactions that are currently using rollback segments are permitted to finish.
- 3. The purge system empties rollback segments by freeing undo logs that are no longer in use.
- 4. After all rollback segments in the undo tablespace are freed, the truncate operation runs and truncates the undo tablespace to its initial size. The initial size of an undo tablespace depends on the innodb\_page\_size value. For the default 16KB page size, the initial undo tablespace file size is 10MiB. For 4KB, 8KB, 32KB, and 64KB page sizes, the initial undo tablespace files sizes are 7MiB, 8MiB, 20MiB, and 40MiB, respectively.

The size of an undo tablespace after a truncate operation may be larger than the initial size due to immediate use following the completion of the operation.

The innodb\_undo\_directory variable defines the location of undo tablespace files. If the innodb\_undo\_directory variable is undefined, undo tablespaces reside in the data directory.

5. Rollback segments are reactivated so that they can be assigned to new transactions.

#### **Expediting Truncation of Undo Tablespaces**

The purge thread is responsible for emptying and truncating undo tablespaces. By default, the purge thread looks for undo tablespaces to truncate once every 128 times that purge is invoked. The frequency with which the purge thread looks for undo tablespaces to truncate is controlled by the innodb\_purge\_rseg\_truncate\_frequency variable, which has a default setting of 128.

```
mysql> SELECT @@innodb_purge_rseg_truncate_frequency;
+----------------------------------------+
| @@innodb_purge_rseg_truncate_frequency |
+----------------------------------------+
| 128 |
+----------------------------------------+
```

To increase the frequency, decrease the innodb\_purge\_rseg\_truncate\_frequency setting. For example, to have the purge thread look for undo tabespaces once every 32 timees that purge is invoked, set innodb\_purge\_rseg\_truncate\_frequency to 32.

```
mysql> SET GLOBAL innodb_purge_rseg_truncate_frequency=32;
```

When the purge thread finds an undo tablespace that requires truncation, the purge thread returns with increased frequency to quickly empty and truncate the undo tablespace.

#### **Performance Impact of Truncating Undo Tablespace Files**

When an undo tablespace is truncated, the rollback segments in the undo tablespace are deactivated. The active rollback segments in other undo tablespaces assume responsibility for the entire system

load, which may result in a slight performance degradation. The extent to which performance is affected depends on a number of factors:

- Number of undo tablespaces
- Number of undo logs
- Undo tablespace size
- Speed of the I/O susbsystem
- Existing long running transactions
- System load

The easiest way to avoid the potential performance impact is to increase the number of undo tablespaces.

Also, two checkpoint operations are performed during an undo tablespace truncate operation. The first checkpoint operation removes the old undo tablespace pages from the buffer pool. The second checkpoint flushes the initial pages of the new undo tablespace to disk. On a busy system, the first checkpoint in particular can temporarily affect system performance if there is a large number of pages to remove.

### **Undo Tablespace Truncation Recovery**

An undo tablespace truncate operation creates a temporary undo\_space\_number\_trunc.log file in the server log directory. That log directory is defined by innodb\_log\_group\_home\_dir. If a system failure occurs during the truncate operation, the temporary log file permits the startup process to identify undo tablespaces that were being truncated and to continue the operation.