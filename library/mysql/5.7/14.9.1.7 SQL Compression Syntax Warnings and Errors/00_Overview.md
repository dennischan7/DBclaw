---
source: MySQL 5.7 Reference
title: 00_Overview
---

This section describes syntax warnings and errors that you may encounter when using the table compression feature with file-per-table tablespaces and general tablespaces.

#### **SQL Compression Syntax Warnings and Errors for File-Per-Table Tablespaces**

When innodb\_strict\_mode is enabled (the default), specifying ROW\_FORMAT=COMPRESSED or KEY\_BLOCK\_SIZE in CREATE TABLE or ALTER TABLE statements produces the following error if innodb\_file\_per\_table is disabled or if innodb\_file\_format is set to Antelope rather than Barracuda.

ERROR 1031 (HY000): Table storage engine for 't1' does not have this option

![](_page_133_Picture_13.jpeg)

#### **Note**

The table is not created if the current configuration does not permit using compressed tables.

When innodb\_strict\_mode is disabled, specifying ROW\_FORMAT=COMPRESSED or KEY\_BLOCK\_SIZE in CREATE TABLE or ALTER TABLE statements produces the following warnings if innodb\_file\_per\_table is disabled.

mysql> **SHOW WARNINGS;**

| ++++<br>  Level<br>  Code   Message<br>++++                                                                                                                                                                                                                                               |           |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| Warning   1478   InnoDB: KEY_BLOCK_SIZE requires innodb_file_per_table.<br>  Warning   1478   InnoDB: ignoring KEY_BLOCK_SIZE=4.<br>  Warning   1478   InnoDB: ROW_FORMAT=COMPRESSED requires innodb_file_per_table.  <br>  Warning   1478   InnoDB: assuming ROW_FORMAT=DYNAMIC.<br>++++ | <br> <br> |

Similar warnings are issued if innodb\_file\_format is set to Antelope rather than Barracuda.

![](_page_134_Picture_3.jpeg)

### **Note**

These messages are only warnings, not errors, and the table is created without compression, as if the options were not specified.

The "non-strict" behavior lets you import a mysqldump file into a database that does not support compressed tables, even if the source database contained compressed tables. In that case, MySQL creates the table in ROW\_FORMAT=COMPACT instead of preventing the operation.

To import the dump file into a new database, and have the tables re-created as they exist in the original database, ensure the server has the proper settings for the configuration parameters innodb\_file\_format and innodb\_file\_per\_table.

The attribute KEY\_BLOCK\_SIZE is permitted only when ROW\_FORMAT is specified as COMPRESSED or is omitted. Specifying a KEY\_BLOCK\_SIZE with any other ROW\_FORMAT generates a warning that you can view with SHOW WARNINGS. However, the table is non-compressed; the specified KEY\_BLOCK\_SIZE is ignored).

| Level   | Code | Message                 |  |
|---------|------|-------------------------|--|
| Warning | 1478 | InnoDB: ignoring        |  |
|         |      | KEY_BLOCK_SIZE=n unless |  |
|         |      | ROW_FORMAT=COMPRESSED.  |  |

If you are running with innodb\_strict\_mode enabled, the combination of a KEY\_BLOCK\_SIZE with any ROW\_FORMAT other than COMPRESSED generates an error, not a warning, and the table is not created.

[Table 14.6, "ROW\\_FORMAT and KEY\\_BLOCK\\_SIZE Options"](#page-134-0) provides an overview the ROW\_FORMAT and KEY\_BLOCK\_SIZE options that are used with CREATE TABLE or ALTER TABLE.

**Table 14.6 ROW\_FORMAT and KEY\_BLOCK\_SIZE Options**

<span id="page-134-0"></span>

| Option                | Usage Notes                                                            | Description                                                                                                                                     |
|-----------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| ROW_FORMAT=REDUNDANT  | Storage format used prior to<br>MySQL 5.0.3                            | Less efficient than<br>ROW_FORMAT=COMPACT; for<br>backward compatibility                                                                        |
| ROW_FORMAT=COMPACT    | Default storage format since<br>MySQL 5.0.3                            | Stores a prefix of 768 bytes<br>of long column values in the<br>clustered index page, with the<br>remaining bytes stored in an<br>overflow page |
| ROW_FORMAT=DYNAMIC    | File-per-table tablespaces<br>require innodb_file<br>_format=Barracuda | Store values within the clustered<br>index page if they fit; if not,<br>stores only a 20-byte pointer to<br>an overflow page (no prefix)        |
| ROW_FORMAT=COMPRESSED | File-per-table tablespaces<br>require innodb_file<br>_format=Barracuda | Compresses the table and<br>indexes using zlib                                                                                                  |

| Option           | Usage Notes                                                            | Description                                                                                                                                                                                                       |
|------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| KEY_BLOCK_SIZE=n | File-per-table tablespaces<br>require innodb_file<br>_format=Barracuda | Specifies compressed<br>page size of 1, 2, 4, 8<br>or 16 kilobytes; implies<br>ROW_FORMAT=COMPRESSED.<br>For general tablespaces, a<br>KEY_BLOCK_SIZE value equal<br>to the InnoDB page size is not<br>permitted. |

[Table 14.7, "CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF"](#page-135-0) summarizes error conditions that occur with certain combinations of configuration parameters and options on the CREATE TABLE or ALTER TABLE statements, and how the options appear in the output of SHOW TABLE STATUS.

When innodb\_strict\_mode is OFF, MySQL creates or alters the table, but ignores certain settings as shown below. You can see the warning messages in the MySQL error log. When innodb\_strict\_mode is ON, these specified combinations of options generate errors, and the table is not created or altered. To see the full description of the error condition, issue the SHOW ERRORS statement: example:

```
mysql> CREATE TABLE x (id INT PRIMARY KEY, c INT)
-> ENGINE=INNODB KEY_BLOCK_SIZE=33333;
ERROR 1005 (HY000): Can't create table 'test.x' (errno: 1478)
mysql> SHOW ERRORS;
+-------+------+-------------------------------------------+
| Level | Code | Message |
+-------+------+-------------------------------------------+
| Error | 1478 | InnoDB: invalid KEY_BLOCK_SIZE=33333. |
| Error | 1005 | Can't create table 'test.x' (errno: 1478) |
+-------+------+-------------------------------------------+
```

**Table 14.7 CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF**

<span id="page-135-0"></span>

| Syntax                                                                           | Warning or Error Condition                                                                                                                                                                                                                                                                                                                     | Resulting ROW_FORMAT,<br>as shown in SHOW TABLE<br>STATUS                                                           |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| ROW_FORMAT=REDUNDANT                                                             | None                                                                                                                                                                                                                                                                                                                                           | REDUNDANT                                                                                                           |
| ROW_FORMAT=COMPACT                                                               | None                                                                                                                                                                                                                                                                                                                                           | COMPACT                                                                                                             |
| ROW_FORMAT=COMPRESSED<br>or ROW_FORMAT=DYNAMIC or<br>KEY_BLOCK_SIZE is specified | Ignored for file-per-table<br>tablespaces unless both<br>innodb_file_format=Barracuda<br>and innodb_file_per_table<br>are enabled. General<br>tablespaces support all<br>row formats (with some<br>restrictions) regardless of<br>innodb_file_format and<br>innodb_file_per_table<br>settings. See Section 14.6.3.3,<br>"General Tablespaces". | the default row format<br>for file-per-table<br>tablespaces; the<br>specified row format for<br>general tablespaces |
| Invalid KEY_BLOCK_SIZE is<br>specified (not 1, 2, 4, 8 or 16)                    | KEY_BLOCK_SIZE is ignored                                                                                                                                                                                                                                                                                                                      | the specified row format, or the<br>default row format                                                              |
| ROW_FORMAT=COMPRESSED<br>and valid KEY_BLOCK_SIZE are<br>specified               | None; KEY_BLOCK_SIZE<br>specified is used                                                                                                                                                                                                                                                                                                      | COMPRESSED                                                                                                          |

| Syntax                                                                          | Warning or Error Condition                                                      | Resulting ROW_FORMAT,<br>as shown in SHOW TABLE<br>STATUS |
|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-----------------------------------------------------------|
| KEY_BLOCK_SIZE is specified<br>with REDUNDANT, COMPACT or<br>DYNAMIC row format | KEY_BLOCK_SIZE is ignored                                                       | REDUNDANT, COMPACT or<br>DYNAMIC                          |
| ROW_FORMAT is not one<br>of REDUNDANT, COMPACT,<br>DYNAMIC or COMPRESSED        | Ignored if recognized by the<br>MySQL parser. Otherwise, an<br>error is issued. | the default row format or N/A                             |

When innodb\_strict\_mode is ON, MySQL rejects invalid ROW\_FORMAT or KEY\_BLOCK\_SIZE parameters and issues errors. When innodb\_strict\_mode is OFF, MySQL issues warnings instead of errors for ignored invalid parameters. innodb\_strict\_mode is ON by default.

When innodb\_strict\_mode is ON, MySQL rejects invalid ROW\_FORMAT or KEY\_BLOCK\_SIZE parameters. For compatibility with earlier versions of MySQL, strict mode is not enabled by default; instead, MySQL issues warnings (not errors) for ignored invalid parameters.

It is not possible to see the chosen KEY\_BLOCK\_SIZE using SHOW TABLE STATUS. The statement SHOW CREATE TABLE displays the KEY\_BLOCK\_SIZE (even if it was ignored when creating the table). The real compressed page size of the table cannot be displayed by MySQL.

#### **SQL Compression Syntax Warnings and Errors for General Tablespaces**

• If FILE\_BLOCK\_SIZE was not defined for the general tablespace when the tablespace was created, the tablespace cannot contain compressed tables. If you attempt to add a compressed table, an error is returned, as shown in the following example:

```
mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;
mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1 ROW_FORMAT=COMPRESSED
 KEY_BLOCK_SIZE=8;
ERROR 1478 (HY000): InnoDB: Tablespace `ts1` cannot contain a COMPRESSED table
```

• Attempting to add a table with an invalid KEY\_BLOCK\_SIZE to a general tablespace returns an error, as shown in the following example:

```
mysql> CREATE TABLESPACE `ts2` ADD DATAFILE 'ts2.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;
mysql> CREATE TABLE t2 (c1 INT PRIMARY KEY) TABLESPACE ts2 ROW_FORMAT=COMPRESSED
 KEY_BLOCK_SIZE=4;
ERROR 1478 (HY000): InnoDB: Tablespace `ts2` uses block size 8192 and cannot
contain a table with physical page size 4096
```

For general tablespaces, the KEY\_BLOCK\_SIZE of the table must be equal to the FILE\_BLOCK\_SIZE of the tablespace divided by 1024. For example, if the FILE\_BLOCK\_SIZE of the tablespace is 8192, the KEY\_BLOCK\_SIZE of the table must be 8.

• Attempting to add a table with an uncompressed row format to a general tablespace configured to store compressed tables returns an error, as shown in the following example:

```
mysql> CREATE TABLESPACE `ts3` ADD DATAFILE 'ts3.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;
mysql> CREATE TABLE t3 (c1 INT PRIMARY KEY) TABLESPACE ts3 ROW_FORMAT=COMPACT;
ERROR 1478 (HY000): InnoDB: Tablespace `ts3` uses block size 8192 and cannot
contain a table with physical page size 16384
```

innodb\_strict\_mode is not applicable to general tablespaces. Tablespace management rules for general tablespaces are strictly enforced independently of innodb\_strict\_mode. For more information, see Section 13.1.19, "CREATE TABLESPACE Statement".

For more information about using compressed tables with general tablespaces, see [Section 14.6.3.3,](#page-53-0) ["General Tablespaces".](#page-53-0)

# <span id="page-137-0"></span>**14.9.2 InnoDB Page Compression**

InnoDB supports page-level compression for tables that reside in file-per-table tablespaces. This feature is referred to as Transparent Page Compression. Page compression is enabled by specifying the COMPRESSION attribute with CREATE TABLE or ALTER TABLE. Supported compression algorithms include Zlib and LZ4.

## **Supported Platforms**

Page compression requires sparse file and hole punching support. Page compression is supported on Windows with NTFS, and on the following subset of MySQL-supported Linux platforms where the kernel level provides hole punching support:

- RHEL 7 and derived distributions that use kernel version 3.10.0-123 or higher
- OEL 5.10 (UEK2) kernel version 2.6.39 or higher
- OEL 6.5 (UEK3) kernel version 3.8.13 or higher
- OEL 7.0 kernel version 3.8.13 or higher
- SLE11 kernel version 3.0-x
- SLE12 kernel version 3.12-x
- OES11 kernel version 3.0-x
- Ubuntu 14.0.4 LTS kernel version 3.13 or higher
- Ubuntu 12.0.4 LTS kernel version 3.2 or higher
- Debian 7 kernel version 3.2 or higher

![](_page_137_Picture_15.jpeg)

#### **Note**

All of the available file systems for a given Linux distribution may not support hole punching.

## **How Page Compression Works**

When a page is written, it is compressed using the specified compression algorithm. The compressed data is written to disk, where the hole punching mechanism releases empty blocks from the end of the page. If compression fails, data is written out as-is.

## **Hole Punch Size on Linux**

On Linux systems, the file system block size is the unit size used for hole punching. Therefore, page compression only works if page data can be compressed to a size that is less than or equal to the InnoDB page size minus the file system block size. For example, if innodb\_page\_size=16K and the file system block size is 4K, page data must compress to less than or equal to 12K to make hole punching possible.

## **Hole Punch Size on Windows**

On Windows systems, the underlying infrastructure for sparse files is based on NTFS compression. Hole punching size is the NTFS compression unit, which is 16 times the NTFS cluster size. Cluster sizes and their compression units are shown in the following table:

**Table 14.8 Windows NTFS Cluster Size and Compression Units**

| Cluster Size | Compression Unit |
|--------------|------------------|
| 512 Bytes    | 8 KB             |

| Cluster Size | Compression Unit |
|--------------|------------------|
| 1 KB         | 16 KB            |
| 2 KB         | 32 KB            |
| 4 KB         | 64 KB            |

Page compression on Windows systems only works if page data can be compressed to a size that is less than or equal to the InnoDB page size minus the compression unit size.

The default NTFS cluster size is 4KB, for which the compression unit size is 64KB. This means that page compression has no benefit for an out-of-the box Windows NTFS configuration, as the maximum innodb\_page\_size is also 64KB.

For page compression to work on Windows, the file system must be created with a cluster size smaller than 4K, and the innodb\_page\_size must be at least twice the size of the compression unit. For example, for page compression to work on Windows, you could build the file system with a cluster size of 512 Bytes (which has a compression unit of 8KB) and initialize InnoDB with an innodb\_page\_size value of 16K or greater.

# **Enabling Page Compression**

To enable page compression, specify the COMPRESSION attribute in the CREATE TABLE statement. For example:

```
CREATE TABLE t1 (c1 INT) COMPRESSION="zlib";
```

You can also enable page compression in an ALTER TABLE statement. However, ALTER TABLE ... COMPRESSION only updates the tablespace compression attribute. Writes to the tablespace that occur after setting the new compression algorithm use the new setting, but to apply the new compression algorithm to existing pages, you must rebuild the table using OPTIMIZE TABLE.

```
ALTER TABLE t1 COMPRESSION="zlib";
OPTIMIZE TABLE t1;
```

## **Disabling Page Compression**

To disable page compression, set COMPRESSION=None using ALTER TABLE. Writes to the tablespace that occur after setting COMPRESSION=None no longer use page compression. To uncompress existing pages, you must rebuild the table using OPTIMIZE TABLE after setting COMPRESSION=None.

```
ALTER TABLE t1 COMPRESSION="None";
OPTIMIZE TABLE t1;
```

## **Page Compression Metadata**

Page compression metadata is found in the Information Schema INNODB\_SYS\_TABLESPACES table, in the following columns:

- FS\_BLOCK\_SIZE: The file system block size, which is the unit size used for hole punching.
- FILE\_SIZE: The apparent size of the file, which represents the maximum size of the file, uncompressed.
- ALLOCATED\_SIZE: The actual size of the file, which is the amount of space allocated on disk.

![](_page_138_Picture_18.jpeg)

# **Note**

On Unix-like systems, ls -l tablespace\_name.ibd shows the apparent file size (equivalent to FILE\_SIZE) in bytes. To view the actual amount of space allocated on disk (equivalent to ALLOCATED\_SIZE), use du --block-size=1 tablespace\_name.ibd. The --block-size=1 option prints the allocated space in bytes instead of blocks, so that it can be compared to ls -l output.

Use SHOW CREATE TABLE to view the current page compression setting (Zlib, Lz4, or None). A table may contain a mix of pages with different compression settings.

In the following example, page compression metadata for the employees table is retrieved from the Information Schema INNODB\_SYS\_TABLESPACES table.

```
# Create the employees table with Zlib page compression
CREATE TABLE employees (
 emp_no INT NOT NULL,
 birth_date DATE NOT NULL,
 first_name VARCHAR(14) NOT NULL,
 last_name VARCHAR(16) NOT NULL,
 gender ENUM ('M','F') NOT NULL,
 hire_date DATE NOT NULL,
 PRIMARY KEY (emp_no)
) COMPRESSION="zlib";
# Insert data (not shown)
# Query page compression metadata in INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES
mysql> SELECT SPACE, NAME, FS_BLOCK_SIZE, FILE_SIZE, ALLOCATED_SIZE FROM
 INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES WHERE NAME='employees/employees'\G
*************************** 1. row ***************************
SPACE: 45
NAME: employees/employees
FS_BLOCK_SIZE: 4096
FILE_SIZE: 23068672
ALLOCATED_SIZE: 19415040
```

Page compression metadata for the employees table shows that the apparent file size is 23068672 bytes while the actual file size (with page compression) is 19415040 bytes. The file system block size is 4096 bytes, which is the block size used for hole punching.

# **Identifying Tables Using Page Compression**

To identify tables for which page compression is enabled, you can query the Information Schema TABLES table's CREATE\_OPTIONS column for tables defined with the COMPRESSION attribute:

```
mysql> SELECT TABLE_NAME, TABLE_SCHEMA, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES 
 WHERE CREATE_OPTIONS LIKE '%COMPRESSION=%';
+------------+--------------+--------------------+
| TABLE_NAME | TABLE_SCHEMA | CREATE_OPTIONS |
+------------+--------------+--------------------+
| employees | test | COMPRESSION="zlib" |
+------------+--------------+--------------------+
```

SHOW CREATE TABLE also shows the COMPRESSION attribute, if used.

## **Page Compression Limitations and Usage Notes**

- Page compression is disabled if the file system block size (or compression unit size on Windows) \* 2 > innodb\_page\_size.
- Page compression is not supported for tables that reside in shared tablespaces, which include the system tablespace, the temporary tablespace, and general tablespaces.
- Page compression is not supported for undo log tablespaces.
- Page compression is not supported for redo log pages.
- R-tree pages, which are used for spatial indexes, are not compressed.
- Pages that belong to compressed tables (ROW\_FORMAT=COMPRESSED) are left as-is.

- During recovery, updated pages are written out in an uncompressed form.
- Loading a page-compressed tablespace on a server that does not support the compression algorithm that was used causes an I/O error.
- Before downgrading to an earlier version of MySQL that does not support page compression, uncompress the tables that use the page compression feature. To uncompress a table, run ALTER TABLE ... COMPRESSION=None and OPTIMIZE TABLE.
- Page-compressed tablespaces can be copied between Linux and Windows servers if the compression algorithm that was used is available on both servers.
- Preserving page compression when moving a page-compressed tablespace file from one host to another requires a utility that preserves sparse files.
- Better page compression may be achieved on Fusion-io hardware with NVMFS than on other platforms, as NVMFS is designed to take advantage of punch hole functionality.
- Using the page compression feature with a large InnoDB page size and relatively small file system block size could result in write amplification. For example, a maximum InnoDB page size of 64KB with a 4KB file system block size may improve compression but may also increase demand on the buffer pool, leading to increased I/O and potential write amplification.

# <span id="page-140-0"></span>**14.10 InnoDB File-Format Management**

As InnoDB evolves, data file formats that are not compatible with prior versions of InnoDB are sometimes required to support new features. To help manage compatibility in upgrade and downgrade situations, and systems that run different versions of MySQL, InnoDB uses named file formats. InnoDB currently supports two named file formats, Antelope and Barracuda.

- Antelope is the original InnoDB file format, which previously did not have a name. It supports the COMPACT and REDUNDANT row formats for InnoDB tables.
- Barracuda is the newest file format. It supports all InnoDB row formats including the newer COMPRESSED and DYNAMIC row formats. The features associated with COMPRESSED and DYNAMIC row formats include compressed tables, efficient storage of off-page columns, and index key prefixes up to 3072 bytes (innodb\_large\_prefix). See [Section 14.11, "InnoDB Row](#page-145-1) [Formats"](#page-145-1).

This section discusses enabling InnoDB file formats for new InnoDB tables, verifying compatibility of different file formats between MySQL releases, and identifying the file format in use.

InnoDB file format settings do not apply to tables stored in [general tablespaces.](#page-53-0) General tablespaces provide support for all row formats and associated features. For more information, see [Section 14.6.3.3, "General Tablespaces".](#page-53-0)

![](_page_140_Picture_14.jpeg)

#### **Note**

The following file format configuration parameters have new default values:

- The innodb\_file\_format default value was changed to Barracuda. The previous default value was Antelope.
- The innodb\_large\_prefix default value was changed to ON. The previous default was OFF.

The following file format configuration parameters are deprecated in and may be removed in a future release:

- innodb\_file\_format
- innodb\_file\_format\_check

- innodb\_file\_format\_max
- innodb\_large\_prefix

The file format configuration parameters were provided for creating tables compatible with earlier versions of InnoDB in MySQL 5.1. Now that MySQL 5.1 has reached the end of its product lifecycle, the parameters are no longer required.

# <span id="page-141-0"></span>**14.10.1 Enabling File Formats**

The innodb\_file\_format configuration option enables an InnoDB file format for file-per-table tablespaces.

Barracuda is the default innodb\_file\_format setting. In earlier releases, the default file format was Antelope.

![](_page_141_Picture_7.jpeg)

#### **Note**

The innodb\_file\_format configuration option is deprecated and may be removed in a future release. For more information, see [Section 14.10, "InnoDB](#page-140-0) [File-Format Management".](#page-140-0)

You can set the value of innodb\_file\_format on the command line when you start mysqld, or in the option file (my.cnf on Unix, my.ini on Windows). You can also change it dynamically with a SET GLOBAL statement.

SET GLOBAL innodb\_file\_format=Barracuda;

# **Usage notes**

- InnoDB file format settings do not apply to tables stored in [general tablespaces](#page-53-0). General tablespaces provide support for all row formats and associated features. For more information, see [Section 14.6.3.3, "General Tablespaces".](#page-53-0)
- The innodb\_file\_format setting is not applicable when using the TABLESPACE [=] innodb\_system table option with CREATE TABLE or ALTER TABLE to store a DYNAMIC table in the system tablespace.
- The innodb\_file\_format setting is ignored when creating tables that use the DYNAMIC row format. For more information, see [DYNAMIC Row Format](#page-148-0).

# <span id="page-141-1"></span>**14.10.2 Verifying File Format Compatibility**

InnoDB incorporates several checks to guard against the possible crashes and data corruptions that might occur if you run an old release of the MySQL server on InnoDB data files that use a newer file format. These checks take place when the server is started, and when you first access a table. This section describes these checks, how you can control them, and error and warning conditions that might arise.

# **Backward Compatibility**

You only need to consider backward file format compatibility when using a recent version of InnoDB (MySQL 5.5 and higher with InnoDB) alongside an older version (MySQL 5.1 or earlier, with the builtin InnoDB rather than the InnoDB Plugin). To minimize the chance of compatibility issues, you can standardize on the InnoDB Plugin for all your MySQL 5.1 and earlier database servers.

In general, a newer version of InnoDB may create a table or index that cannot safely be read or written with an older version of InnoDB without risk of crashes, hangs, wrong results or corruptions. InnoDB includes a mechanism to guard against these conditions, and to help preserve compatibility among

database files and versions of InnoDB. This mechanism lets you take advantage of some new features of an InnoDB release (such as performance improvements and bug fixes), and still preserve the option of using your database with an old version of InnoDB, by preventing accidental use of new features that create downward-incompatible disk files.

If a version of InnoDB supports a particular file format (whether or not that format is the default), you can query and update any table that requires that format or an earlier format. Only the creation of new tables using new features is limited based on the particular file format enabled. Conversely, if a tablespace contains a table or index that uses a file format that is not supported, it cannot be accessed at all, even for read access.

The only way to "downgrade" an InnoDB tablespace to the earlier Antelope file format is to copy the data to a new table, in a tablespace that uses the earlier format.

The easiest way to determine the file format of an existing InnoDB tablespace is to examine the properties of the table it contains, using the SHOW TABLE STATUS command or querying the table INFORMATION\_SCHEMA.TABLES. If the Row\_format of the table is reported as 'Compressed' or 'Dynamic', the tablespace containing the table supports the Barracuda format.

# **Internal Details**

Every InnoDB file-per-table tablespace (represented by a \*.ibd file) file is labeled with a file format identifier. The system tablespace (represented by the ibdata files) is tagged with the "highest" file format in use in a group of InnoDB database files, and this tag is checked when the files are opened.

Creating a compressed table, or a table with ROW\_FORMAT=DYNAMIC, updates the file header of the corresponding file-per-table .ibd file and the table type in the InnoDB data dictionary with the identifier for the Barracuda file format. From that point forward, the table cannot be used with a version of InnoDB that does not support the Barracuda file format. To protect against anomalous behavior, InnoDB performs a compatibility check when the table is opened. (In many cases, the ALTER TABLE statement recreates a table and thus changes its properties. The special case of adding or dropping indexes without rebuilding the table is described in [Section 14.13.1, "Online DDL Operations".](#page-156-0))

General tablespaces, which are also represented by a \*.ibd file, support both Antelope and Barracuda file formats. For more information about general tablespaces, see [Section 14.6.3.3,](#page-53-0) ["General Tablespaces".](#page-53-0)

## **Definition of ib-file set**

To avoid confusion, for the purposes of this discussion we define the term "ib-file set" to mean the set of operating system files that InnoDB manages as a unit. The ib-file set includes the following files:

- The system tablespace (one or more ibdata files) that contain internal system information (including internal catalogs and undo information) and may include user data and indexes.
- Zero or more single-table tablespaces (also called "file per table" files, named \*.ibd files).
- InnoDB log files; usually two, ib\_logfile0 and ib\_logfile1. Used for crash recovery and in backups.

An "ib-file set" does not include the corresponding .frm files that contain metadata about InnoDB tables. The .frm files are created and managed by MySQL, and can sometimes get out of sync with the internal metadata in InnoDB.

Multiple tables, even from more than one database, can be stored in a single "ib-file set". (In MySQL, a "database" is a logical collection of tables, what other systems refer to as a "schema" or "catalog".)