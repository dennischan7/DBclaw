---
source: MySQL 5.7 Reference
title: 00_Overview
---

To prevent possible crashes or data corruptions when InnoDB opens an ib-file set, it checks that it can fully support the file formats in use within the ib-file set. If the system is restarted following a crash, or

a "fast shutdown" (i.e., innodb\_fast\_shutdown is greater than zero), there may be on-disk data structures (such as redo or undo entries, or doublewrite pages) that are in a "too-new" format for the current software. During the recovery process, serious damage can be done to your data files if these data structures are accessed. The startup check of the file format occurs before any recovery process begins, thereby preventing consistency issues with the new tables or startup problems for the MySQL server.

Beginning with version InnoDB 1.0.1, the system tablespace records an identifier or tag for the "highest" file format used by any table in any of the tablespaces that is part of the ibfile set. Checks against this file format tag are controlled by the configuration parameter innodb\_file\_format\_check, which is ON by default.

If the file format tag in the system tablespace is newer or higher than the highest version supported by the particular currently executing software and if innodb\_file\_format\_check is ON, the following error is issued when the server is started:

```
InnoDB: Error: the system tablespace is in a
file format that this version doesn't support
```

You can also set innodb\_file\_format to a file format name. Doing so prevents InnoDB from starting if the current software does not support the file format specified. It also sets the "high water mark" to the value you specify. The ability to set innodb\_file\_format\_check is useful (with future releases) if you manually "downgrade" all of the tables in an ib-file set. You can then rely on the file format check at startup if you subsequently use an older version of InnoDB to access the ib-file set.

In some limited circumstances, you might want to start the server and use an ib-file set that is in a new file format that is not supported by the software you are using. If you set the configuration parameter innodb\_file\_format\_check to OFF, InnoDB opens the database, but issues this warning message in the error log:

```
InnoDB: Warning: the system tablespace is in a
file format that this version doesn't support
```

![](_page_143_Picture_8.jpeg)

#### **Note**

This is a dangerous setting, as it permits the recovery process to run, possibly corrupting your database if the previous shutdown was an unexpected exit or "fast shutdown". You should only set innodb\_file\_format\_check to OFF if you are sure that the previous shutdown was done with innodb\_fast\_shutdown=0, so that essentially no recovery process occurs.

The parameter innodb\_file\_format\_check affects only what happens when a database is opened, not subsequently. Conversely, the parameter innodb\_file\_format (which enables a specific format) only determines whether or not a new table can be created in the enabled format and has no effect on whether or not a database can be opened.

The file format tag is a "high water mark", and as such it is increased after the server is started, if a table in a "higher" format is created or an existing table is accessed for read or write (assuming its format is supported). If you access an existing table in a format higher than the format the running software supports, the system tablespace tag is not updated, but table-level compatibility checking applies (and an error is issued), as described in [Section 14.10.2.2, "Compatibility Check When a Table](#page-143-0) [Is Opened"](#page-143-0). Any time the high water mark is updated, the value of innodb\_file\_format\_check is updated as well, so the command SELECT @@innodb\_file\_format\_check; displays the name of the latest file format known to be used by tables in the currently open ib-file set and supported by the currently executing software.

## <span id="page-143-0"></span>**14.10.2.2 Compatibility Check When a Table Is Opened**

When a table is first accessed, InnoDB (including some releases prior to InnoDB 1.0) checks that the file format of the tablespace in which the table is stored is fully supported. This check prevents crashes or corruptions that would otherwise occur when tables using a "too new" data structure are encountered.

All tables using any file format supported by a release can be read or written (assuming the user has sufficient privileges). The setting of the system configuration parameter innodb\_file\_format can prevent creating a new table that uses a specific file format, even if the file format is supported by a given release. Such a setting might be used to preserve backward compatibility, but it does not prevent accessing any table that uses a supported format.

Versions of MySQL older than 5.0.21 cannot reliably use database files created by newer versions if a new file format was used when a table was created. To prevent various error conditions or corruptions, InnoDB checks file format compatibility when it opens a file (for example, upon first access to a table). If the currently running version of InnoDB does not support the file format identified by the table type in the InnoDB data dictionary, MySQL reports the following error:

```
ERROR 1146 (42S02): Table 'test.t1' doesn't exist
```

InnoDB also writes a message to the error log:

```
InnoDB: table test/t1: unknown table type 33
```

The table type should be equal to the tablespace flags, which contains the file format version as discussed in [Section 14.10.3, "Identifying the File Format in Use"](#page-144-0).

Versions of InnoDB prior to MySQL 4.1 did not include table format identifiers in the database files, and versions prior to MySQL 5.0.21 did not include a table format compatibility check. Therefore, there is no way to ensure proper operations if a table in a newer file format is used with versions of InnoDB prior to 5.0.21.

The file format management capability in InnoDB 1.0 and higher (tablespace tagging and run-time checks) allows InnoDB to verify as soon as possible that the running version of software can properly process the tables existing in the database.

If you permit InnoDB to open a database containing files in a format it does not support (by setting the parameter innodb\_file\_format\_check to OFF), the table-level checking described in this section still applies.

Users are strongly urged not to use database files that contain Barracuda file format tables with releases of InnoDB older than the MySQL 5.1 with the InnoDB Plugin. It may be possible to rebuild such tables to use the Antelope format.

# <span id="page-144-0"></span>**14.10.3 Identifying the File Format in Use**

If you enable a different file format using the innodb\_file\_format configuration option, the change only applies to newly created tables. Also, when you create a new table, the tablespace containing the table is tagged with the "earliest" or "simplest" file format that is required to support the table's features. For example, if you enable the Barracuda file format, and create a new table that does not use the Dynamic or Compressed row format, the new tablespace that contains the table is tagged as using the Antelope file format .

It is easy to identify the file format used by a given table. The table uses the Antelope file format if the row format reported by SHOW TABLE STATUS is either Compact or Redundant. The table uses the Barracuda file format if the row format reported by SHOW TABLE STATUS is either Compressed or Dynamic.

```
mysql> SHOW TABLE STATUS\G
*************************** 1. row ***************************
 Name: t1
 Engine: InnoDB
 Version: 10
 Row_format: Compact
 Rows: 0
 Avg_row_length: 0
```

```
 Data_length: 16384
Max_data_length: 0
 Index_length: 16384
 Data_free: 0
 Auto_increment: 1
 Create_time: 2014-11-03 13:32:10
 Update_time: NULL
 Check_time: NULL
 Collation: latin1_swedish_ci
 Checksum: NULL
 Create_options:
 Comment:
```

You can also identify the file format used by a given table or tablespace using InnoDB INFORMATION\_SCHEMA tables. For example:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES WHERE NAME='test/t1'\G
*************************** 1. row ***************************
 TABLE_ID: 44
 NAME: test/t1
 FLAG: 1
 N_COLS: 6
 SPACE: 30
 FILE_FORMAT: Antelope
 ROW_FORMAT: Compact
ZIP_PAGE_SIZE: 0
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES WHERE NAME='test/t1'\G
*************************** 1. row ***************************
 SPACE: 30
 NAME: test/t1
 FLAG: 0
 FILE_FORMAT: Antelope
 ROW_FORMAT: Compact or Redundant
 PAGE_SIZE: 16384
ZIP_PAGE_SIZE: 0
```

# <span id="page-145-0"></span>**14.10.4 Modifying the File Format**

Each InnoDB tablespace file (with a name matching \*.ibd) is tagged with the file format used to create its table and indexes. The way to modify the file format is to re-create the table and its indexes. The easiest way to recreate a table and its indexes is to use the following command on each table that you want to modify:

```
ALTER TABLE t ROW_FORMAT=format_name;
```

If you are modifying the file format to downgrade to an older MySQL version, there may be incompatibilities in table storage formats that require additional steps. For information about downgrading to a previous MySQL version, see Section 2.11, "Downgrading MySQL".

# <span id="page-145-1"></span>**14.11 InnoDB Row Formats**

The row format of a table determines how its rows are physically stored, which in turn can affect the performance of queries and DML operations. As more rows fit into a single disk page, queries and index lookups can work faster, less cache memory is required in the buffer pool, and less I/O is required to write out updated values.

The data in each table is divided into pages. The pages that make up each table are arranged in a tree data structure called a B-tree index. Table data and secondary indexes both use this type of structure. The B-tree index that represents an entire table is known as the clustered index, which is organized according to the primary key columns. The nodes of a clustered index data structure contain the values of all columns in the row. The nodes of a secondary index structure contain the values of index columns and primary key columns.

Variable-length columns are an exception to the rule that column values are stored in B-tree index nodes. Variable-length columns that are too long to fit on a B-tree page are stored on separately

allocated disk pages called overflow pages. Such columns are referred to as off-page columns. The values of off-page columns are stored in singly-linked lists of overflow pages, with each such column having its own list of one or more overflow pages. Depending on column length, all or a prefix of variable-length column values are stored in the B-tree to avoid wasting storage and having to read a separate page.

The InnoDB storage engine supports four row formats: REDUNDANT, COMPACT, DYNAMIC, and COMPRESSED.

**Table 14.9 InnoDB Row Format Overview**

| Row Format     | Compact<br>Storage<br>Characteristics | Enhanced<br>Variable<br>Length<br>Column<br>Storage | Large Index<br>Key Prefix<br>Support | Compression<br>Support | Supported<br>Tablespace<br>Types      | Required<br>File Format  |
|----------------|---------------------------------------|-----------------------------------------------------|--------------------------------------|------------------------|---------------------------------------|--------------------------|
| REDUNDANT      | No                                    | No                                                  | No                                   | No                     | system, file<br>per-table,<br>general | Antelope or<br>Barracuda |
| COMPACT        | Yes                                   | No                                                  | No                                   | No                     | system, file<br>per-table,<br>general | Antelope or<br>Barracuda |
| DYNAMIC        | Yes                                   | Yes                                                 | Yes                                  | No                     | system, file<br>per-table,<br>general | Barracuda                |
| COMPRESSED Yes |                                       | Yes                                                 | Yes                                  | Yes                    | file-per-table,<br>general            | Barracuda                |

The topics that follow describe row format storage characteristics and how to define and determine the row format of a table.

- [REDUNDANT Row Format](#page-146-0)
- [COMPACT Row Format](#page-147-0)
- [DYNAMIC Row Format](#page-148-0)
- [COMPRESSED Row Format](#page-149-0)
- [Defining the Row Format of a Table](#page-150-0)
- [Determining the Row Format of a Table](#page-151-0)

# <span id="page-146-0"></span>**REDUNDANT Row Format**

The REDUNDANT format provides compatibility with older versions of MySQL.

The REDUNDANT row format is supported by both InnoDB file formats (Antelope and Barracuda). For more information, see [Section 14.10, "InnoDB File-Format Management"](#page-140-0).

Tables that use the REDUNDANT row format store the first 768 bytes of variable-length column values (VARCHAR, VARBINARY, and BLOB and TEXT types) in the index record within the B-tree node, with the remainder stored on overflow pages. Fixed-length columns greater than or equal to 768 bytes are encoded as variable-length columns, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the maximum byte length of the character set is greater than 3, as it is with utf8mb4.

If the value of a column is 768 bytes or less, an overflow page is not used, and some savings in I/O may result, since the value is stored entirely in the B-tree node. This works well for relatively short

BLOB column values, but may cause B-tree nodes to fill with data rather than key values, reducing their efficiency. Tables with many BLOB columns could cause B-tree nodes to become too full, and contain too few rows, making the entire index less efficient than if rows were shorter or column values were stored off-page.

# **REDUNDANT Row Format Storage Characteristics**

The REDUNDANT row format has the following storage characteristics:

- Each index record contains a 6-byte header. The header is used to link together consecutive records, and for row-level locking.
- Records in the clustered index contain fields for all user-defined columns. In addition, there is a 6 byte transaction ID field and a 7-byte roll pointer field.
- If no primary key is defined for a table, each clustered index record also contains a 6-byte row ID field.
- Each secondary index record contains all the primary key columns defined for the clustered index key that are not in the secondary index.
- A record contains a pointer to each field of the record. If the total length of the fields in a record is less than 128 bytes, the pointer is one byte; otherwise, two bytes. The array of pointers is called the record directory. The area where the pointers point is the data part of the record.
- Internally, fixed-length character columns such as CHAR(10) are stored in fixed-length format. Trailing spaces are not truncated from VARCHAR columns.
- Fixed-length columns greater than or equal to 768 bytes are encoded as variable-length columns, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the maximum byte length of the character set is greater than 3, as it is with utf8mb4.
- An SQL NULL value reserves one or two bytes in the record directory. An SQL NULL value reserves zero bytes in the data part of the record if stored in a variable-length column. For a fixed-length column, the fixed length of the column is reserved in the data part of the record. Reserving fixed space for NULL values permits columns to be updated in place from NULL to non-NULL values without causing index page fragmentation.

# <span id="page-147-0"></span>**COMPACT Row Format**

The COMPACT row format reduces row storage space by about 20% compared to the REDUNDANT row format, at the cost of increasing CPU use for some operations. If your workload is a typical one that is limited by cache hit rates and disk speed, COMPACT format is likely to be faster. If the workload is limited by CPU speed, compact format might be slower.

The COMPACT row format is supported by both InnoDB file formats (Antelope and Barracuda). For more information, see [Section 14.10, "InnoDB File-Format Management"](#page-140-0).

Tables that use the COMPACT row format store the first 768 bytes of variable-length column values (VARCHAR, VARBINARY, and BLOB and TEXT types) in the index record within the B-tree node, with the remainder stored on overflow pages. Fixed-length columns greater than or equal to 768 bytes are encoded as variable-length columns, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the maximum byte length of the character set is greater than 3, as it is with utf8mb4.

If the value of a column is 768 bytes or less, an overflow page is not used, and some savings in I/O may result, since the value is stored entirely in the B-tree node. This works well for relatively short BLOB column values, but may cause B-tree nodes to fill with data rather than key values, reducing their efficiency. Tables with many BLOB columns could cause B-tree nodes to become too full, and contain too few rows, making the entire index less efficient than if rows were shorter or column values were stored off-page.

# <span id="page-148-1"></span>**COMPACT Row Format Storage Characteristics**

The COMPACT row format has the following storage characteristics:

- Each index record contains a 5-byte header that may be preceded by a variable-length header. The header is used to link together consecutive records, and for row-level locking.
- The variable-length part of the record header contains a bit vector for indicating NULL columns. If the number of columns in the index that can be NULL is N, the bit vector occupies CEILING(N/8) bytes. (For example, if there are anywhere from 9 to 16 columns that can be NULL, the bit vector uses two bytes.) Columns that are NULL do not occupy space other than the bit in this vector. The variablelength part of the header also contains the lengths of variable-length columns. Each length takes one or two bytes, depending on the maximum length of the column. If all columns in the index are NOT NULL and have a fixed length, the record header has no variable-length part.
- For each non-NULL variable-length field, the record header contains the length of the column in one or two bytes. Two bytes are only needed if part of the column is stored externally in overflow pages or the maximum length exceeds 255 bytes and the actual length exceeds 127 bytes. For an externally stored column, the 2-byte length indicates the length of the internally stored part plus the 20-byte pointer to the externally stored part. The internal part is 768 bytes, so the length is 768+20. The 20-byte pointer stores the true length of the column.
- The record header is followed by the data contents of non-NULL columns.
- Records in the clustered index contain fields for all user-defined columns. In addition, there is a 6 byte transaction ID field and a 7-byte roll pointer field.
- If no primary key is defined for a table, each clustered index record also contains a 6-byte row ID field.
- Each secondary index record contains all the primary key columns defined for the clustered index key that are not in the secondary index. If any of the primary key columns are variable length, the record header for each secondary index has a variable-length part to record their lengths, even if the secondary index is defined on fixed-length columns.
- Internally, for nonvariable-length character sets, fixed-length character columns such as CHAR(10) are stored in a fixed-length format.

Trailing spaces are not truncated from VARCHAR columns.

• Internally, for variable-length character sets such as utf8mb3 and utf8mb4, InnoDB attempts to store CHAR(N) in N bytes by trimming trailing spaces. If the byte length of a CHAR(N) column value exceeds N bytes, trailing spaces are trimmed to a minimum of the column value byte length. The maximum length of a CHAR(N) column is the maximum character byte length × N.

A minimum of N bytes is reserved for CHAR(N). Reserving the minimum space N in many cases enables column updates to be done in place without causing index page fragmentation. By comparison, CHAR(N) columns occupy the maximum character byte length × N when using the REDUNDANT row format.

Fixed-length columns greater than or equal to 768 bytes are encoded as variable-length fields, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the maximum byte length of the character set is greater than 3, as it is with utf8mb4.

# <span id="page-148-0"></span>**DYNAMIC Row Format**

The DYNAMIC row format offers the same storage characteristics as the COMPACT row format but adds enhanced storage capabilities for long variable-length columns and supports large index key prefixes.

The Barracuda file format supports the DYNAMIC row format. See [Section 14.10, "InnoDB File-Format](#page-140-0) [Management".](#page-140-0)

When a table is created with ROW\_FORMAT=DYNAMIC, InnoDB can store long variable-length column values (for VARCHAR, VARBINARY, and BLOB and TEXT types) fully off-page, with the clustered index record containing only a 20-byte pointer to the overflow page. Fixed-length fields greater than or equal to 768 bytes are encoded as variable-length fields. For example, a CHAR(255) column can exceed 768 bytes if the maximum byte length of the character set is greater than 3, as it is with utf8mb4.

Whether columns are stored off-page depends on the page size and the total size of the row. When a row is too long, the longest columns are chosen for off-page storage until the clustered index record fits on the B-tree page. TEXT and BLOB columns that are less than or equal to 40 bytes are stored in line.

The DYNAMIC row format maintains the efficiency of storing the entire row in the index node if it fits (as do the COMPACT and REDUNDANT formats), but the DYNAMIC row format avoids the problem of filling B-tree nodes with a large number of data bytes of long columns. The DYNAMIC row format is based on the idea that if a portion of a long data value is stored off-page, it is usually most efficient to store the entire value off-page. With DYNAMIC format, shorter columns are likely to remain in the B-tree node, minimizing the number of overflow pages required for a given row.

The DYNAMIC row format supports index key prefixes up to 3072 bytes. This feature is controlled by the innodb\_large\_prefix variable, which is enabled by default. See the innodb\_large\_prefix variable description for more information.

Tables that use the DYNAMIC row format can be stored in the system tablespace, file-per-table tablespaces, and general tablespaces. To store DYNAMIC tables in the system tablespace, either disable innodb\_file\_per\_table and use a regular CREATE TABLE or ALTER TABLE statement, or use the TABLESPACE [=] innodb\_system table option with CREATE TABLE or ALTER TABLE. The innodb\_file\_per\_table and innodb\_file\_format variables are not applicable to general tablespaces, nor are they applicable when using the TABLESPACE [=] innodb\_system table option to store DYNAMIC tables in the system tablespace.

# **DYNAMIC Row Format Storage Characteristics**

The DYNAMIC row format is a variation of the COMPACT row format. For storage characteristics, see [COMPACT Row Format Storage Characteristics.](#page-148-1)

# <span id="page-149-0"></span>**COMPRESSED Row Format**

The COMPRESSED row format offers the same storage characteristics and capabilities as the DYNAMIC row format but adds support for table and index data compression.

The Barracuda file format supports the COMPRESSED row format. See [Section 14.10, "InnoDB File-](#page-140-0)[Format Management"](#page-140-0).

The COMPRESSED row format uses similar internal details for off-page storage as the DYNAMIC row format, with additional storage and performance considerations from the table and index data being compressed and using smaller page sizes. With the COMPRESSED row format, the KEY\_BLOCK\_SIZE option controls how much column data is stored in the clustered index, and how much is placed on overflow pages. For more information about the COMPRESSED row format, see [Section 14.9, "InnoDB](#page-122-0) [Table and Page Compression".](#page-122-0)

The COMPRESSED row format supports index key prefixes up to 3072 bytes. This feature is controlled by the innodb\_large\_prefix variable, which is enabled by default. See the innodb\_large\_prefix variable description for more information.

Tables that use the COMPRESSED row format can be created in file-per-table tablespaces or general tablespaces. The system tablespace does not support the COMPRESSED row format. To store a COMPRESSED table in a file-per-table tablespace, the innodb\_file\_per\_table variable must be enabled and innodb\_file\_format must be set to Barracuda. The innodb\_file\_per\_table and innodb\_file\_format variables are not applicable to general tablespaces. General tablespaces support all row formats with the caveat that compressed and uncompressed tables cannot coexist in

the same general tablespace due to different physical page sizes. For more information about, see [Section 14.6.3.3, "General Tablespaces".](#page-53-0)

# **Compressed Row Format Storage Characteristics**

The COMPRESSED row format is a variation of the COMPACT row format. For storage characteristics, see [COMPACT Row Format Storage Characteristics.](#page-148-1)

# <span id="page-150-0"></span>**Defining the Row Format of a Table**

The default row format for InnoDB tables is defined by innodb\_default\_row\_format variable, which has a default value of DYNAMIC. The default row format is used when the ROW\_FORMAT table option is not defined explicitly or when ROW\_FORMAT=DEFAULT is specified.

The row format of a table can be defined explicitly using the ROW\_FORMAT table option in a CREATE TABLE or ALTER TABLE statement. For example:

```
CREATE TABLE t1 (c1 INT) ROW_FORMAT=DYNAMIC;
```

An explicitly defined ROW\_FORMAT setting overrides the default row format. Specifying ROW\_FORMAT=DEFAULT is equivalent to using the implicit default.

The innodb\_default\_row\_format variable can be set dynamically:

```
mysql> SET GLOBAL innodb_default_row_format=DYNAMIC;
```

Valid innodb\_default\_row\_format options include DYNAMIC, COMPACT, and REDUNDANT. The COMPRESSED row format, which is not supported for use in the system tablespace, cannot be defined as the default. It can only be specified explicitly in a CREATE TABLE or ALTER TABLE statement. Attempting to set the innodb\_default\_row\_format variable to COMPRESSED returns an error:

```
mysql> SET GLOBAL innodb_default_row_format=COMPRESSED;
ERROR 1231 (42000): Variable 'innodb_default_row_format'
can't be set to the value of 'COMPRESSED'
```

Newly created tables use the row format defined by the innodb\_default\_row\_format variable when a ROW\_FORMAT option is not specified explicitly, or when ROW\_FORMAT=DEFAULT is used. For example, the following CREATE TABLE statements use the row format defined by the innodb\_default\_row\_format variable.

```
CREATE TABLE t1 (c1 INT);
CREATE TABLE t2 (c1 INT) ROW_FORMAT=DEFAULT;
```

When a ROW\_FORMAT option is not specified explicitly, or when ROW\_FORMAT=DEFAULT is used, an operation that rebuilds a table silently changes the row format of the table to the format defined by the innodb\_default\_row\_format variable.

Table-rebuilding operations include ALTER TABLE operations that use ALGORITHM=COPY or ALGORITHM=INPLACE where table rebuilding is required. See [Section 14.13.1, "Online DDL](#page-156-0) [Operations"](#page-156-0) for more information. OPTIMIZE TABLE is also a table-rebuilding operation.

The following example demonstrates a table-rebuilding operation that silently changes the row format of a table created without an explicitly defined row format.

```
mysql> SELECT @@innodb_default_row_format;
+-----------------------------+
| @@innodb_default_row_format |
+-----------------------------+
| dynamic |
+-----------------------------+
mysql> CREATE TABLE t1 (c1 INT);
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES WHERE NAME LIKE 'test/t1' \G
*************************** 1. row ***************************
```

```
 TABLE_ID: 54
 NAME: test/t1
 FLAG: 33
 N_COLS: 4
 SPACE: 35
 FILE_FORMAT: Barracuda
 ROW_FORMAT: Dynamic
ZIP_PAGE_SIZE: 0
 SPACE_TYPE: Single
mysql> SET GLOBAL innodb_default_row_format=COMPACT;
mysql> ALTER TABLE t1 ADD COLUMN (c2 INT);
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES WHERE NAME LIKE 'test/t1' \G
*************************** 1. row ***************************
 TABLE_ID: 55
 NAME: test/t1
 FLAG: 1
 N_COLS: 5
 SPACE: 36
 FILE_FORMAT: Antelope
 ROW_FORMAT: Compact
ZIP_PAGE_SIZE: 0
 SPACE_TYPE: Single
```

Consider the following potential issues before changing the row format of existing tables from REDUNDANT or COMPACT to DYNAMIC.

• The REDUNDANT and COMPACT row formats support a maximum index key prefix length of 767 bytes whereas DYNAMIC and COMPRESSED row formats support an index key prefix length of 3072 bytes. In a replication environment, if the innodb\_default\_row\_format variable is set to DYNAMIC on the source, and set to COMPACT on the replica, the following DDL statement, which does not explicitly define a row format, succeeds on the source but fails on the replica:

```
CREATE TABLE t1 (c1 INT PRIMARY KEY, c2 VARCHAR(5000), KEY i1(c2(3070)));
```

For related information, see Section 14.23, "InnoDB Limits".

• Importing a table that does not explicitly define a row format results in a schema mismatch error if the innodb\_default\_row\_format setting on the source server differs from the setting on the destination server. For more information, [Section 14.6.1.3, "Importing InnoDB Tables".](#page-22-3)

# <span id="page-151-0"></span>**Determining the Row Format of a Table**

To determine the row format of a table, use SHOW TABLE STATUS:

```
mysql> SHOW TABLE STATUS IN test1\G
*************************** 1. row ***************************
 Name: t1
 Engine: InnoDB
 Version: 10
 Row_format: Dynamic
 Rows: 0
 Avg_row_length: 0
 Data_length: 16384
Max_data_length: 0
 Index_length: 16384
 Data_free: 0
 Auto_increment: 1
 Create_time: 2016-09-14 16:29:38
 Update_time: NULL
 Check_time: NULL
 Collation: latin1_swedish_ci
 Checksum: NULL
 Create_options:
 Comment:
```

Alternatively, query the Information Schema INNODB\_SYS\_TABLES table:

```
mysql> SELECT NAME, ROW_FORMAT FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES WHERE NAME='test1/t1';
+----------+------------+
| NAME | ROW_FORMAT |
+----------+------------+
| test1/t1 | Dynamic |
+----------+------------+
```

# <span id="page-152-0"></span>**14.12 InnoDB Disk I/O and File Space Management**

As a DBA, you must manage disk I/O to keep the I/O subsystem from becoming saturated, and manage disk space to avoid filling up storage devices. The ACID design model requires a certain amount of I/O that might seem redundant, but helps to ensure data reliability. Within these constraints, InnoDB tries to optimize the database work and the organization of disk files to minimize the amount of disk I/O. Sometimes, I/O is postponed until the database is not busy, or until everything needs to be brought to a consistent state, such as during a database restart after a fast shutdown.

This section discusses the main considerations for I/O and disk space with the default kind of MySQL tables (also known as InnoDB tables):

- Controlling the amount of background I/O used to improve query performance.
- Enabling or disabling features that provide extra durability at the expense of additional I/O.
- Organizing tables into many small files, a few larger files, or a combination of both.
- Balancing the size of redo log files against the I/O activity that occurs when the log files become full.
- How to reorganize a table for optimal query performance.

# <span id="page-152-1"></span>**14.12.1 InnoDB Disk I/O**

InnoDB uses asynchronous disk I/O where possible, by creating a number of threads to handle I/O operations, while permitting other database operations to proceed while the I/O is still in progress. On Linux and Windows platforms, InnoDB uses the available OS and library functions to perform "native" asynchronous I/O. On other platforms, InnoDB still uses I/O threads, but the threads may actually wait for I/O requests to complete; this technique is known as "simulated" asynchronous I/O.

## **Read-Ahead**

If InnoDB can determine there is a high probability that data might be needed soon, it performs readahead operations to bring that data into the buffer pool so that it is available in memory. Making a few large read requests for contiguous data can be more efficient than making several small, spread-out requests. There are two read-ahead heuristics in InnoDB:

- In sequential read-ahead, if InnoDB notices that the access pattern to a segment in the tablespace is sequential, it posts in advance a batch of reads of database pages to the I/O system.
- In random read-ahead, if InnoDB notices that some area in a tablespace seems to be in the process of being fully read into the buffer pool, it posts the remaining reads to the I/O system.

For information about configuring read-ahead heuristics, see [Section 14.8.3.4, "Configuring InnoDB](#page-97-0) [Buffer Pool Prefetching \(Read-Ahead\)".](#page-97-0)

## **Doublewrite Buffer**

InnoDB uses a novel file flush technique involving a structure called the doublewrite buffer, which is enabled by default in most cases (innodb\_doublewrite=ON). It adds safety to recovery following an unexpected exit or power outage, and improves performance on most varieties of Unix by reducing the need for fsync() operations.

Before writing pages to a data file, InnoDB first writes them to a contiguous tablespace area called the doublewrite buffer. Only after the write and the flush to the doublewrite buffer has completed

does InnoDB write the pages to their proper positions in the data file. If there is an operating system, storage subsystem, or unexpected mysqld process exit in the middle of a page write (causing a torn page condition), InnoDB can later find a good copy of the page from the doublewrite buffer during recovery.

If system tablespace files ("ibdata files") are located on Fusion-io devices that support atomic writes, doublewrite buffering is automatically disabled and Fusion-io atomic writes are used for all data files. Because the doublewrite buffer setting is global, doublewrite buffering is also disabled for data files residing on non-Fusion-io hardware. This feature is only supported on Fusion-io hardware and is only enabled for Fusion-io NVMFS on Linux. To take full advantage of this feature, an innodb\_flush\_method setting of O\_DIRECT is recommended.

# <span id="page-153-0"></span>**14.12.2 File Space Management**

The data files that you define in the configuration file using the innodb\_data\_file\_path configuration option form the InnoDB system tablespace. The files are logically concatenated to form the system tablespace. There is no striping in use. You cannot define where within the system tablespace your tables are allocated. In a newly created system tablespace, InnoDB allocates space starting from the first data file.

To avoid the issues that come with storing all tables and indexes inside the system tablespace, you can enable the innodb\_file\_per\_table configuration option (the default), which stores each newly created table in a separate tablespace file (with extension .ibd). For tables stored this way, there is less fragmentation within the disk file, and when the table is truncated, the space is returned to the operating system rather than still being reserved by InnoDB within the system tablespace. For more information, see [Section 14.6.3.2, "File-Per-Table Tablespaces"](#page-51-0).

You can also store tables in general tablespaces. General tablespaces are shared tablespaces created using CREATE TABLESPACE syntax. They can be created outside of the MySQL data directory, are capable of holding multiple tables, and support tables of all row formats. For more information, see [Section 14.6.3.3, "General Tablespaces".](#page-53-0)

# **Pages, Extents, Segments, and Tablespaces**

Each tablespace consists of database pages. Every tablespace in a MySQL instance has the same page size. By default, all tablespaces have a page size of 16KB; you can reduce the page size to 8KB or 4KB by specifying the innodb\_page\_size option when you create the MySQL instance. You can also increase the page size to 32KB or 64KB. For more information, refer to the innodb\_page\_size documentation.

The pages are grouped into extents of size 1MB for pages up to 16KB in size (64 consecutive 16KB pages, or 128 8KB pages, or 256 4KB pages). For a page size of 32KB, extent size is 2MB. For page size of 64KB, extent size is 4MB. The "files" inside a tablespace are called segments in InnoDB. (These segments are different from the rollback segment, which actually contains many tablespace segments.)

When a segment grows inside the tablespace, InnoDB allocates the first 32 pages to it one at a time. After that, InnoDB starts to allocate whole extents to the segment. InnoDB can add up to 4 extents at a time to a large segment to ensure good sequentiality of data.

Two segments are allocated for each index in InnoDB. One is for nonleaf nodes of the B-tree, the other is for the leaf nodes. Keeping the leaf nodes contiguous on disk enables better sequential I/O operations, because these leaf nodes contain the actual table data.

Some pages in the tablespace contain bitmaps of other pages, and therefore a few extents in an InnoDB tablespace cannot be allocated to segments as a whole, but only as individual pages.

When you ask for available free space in the tablespace by issuing a SHOW TABLE STATUS statement, InnoDB reports the extents that are definitely free in the tablespace. InnoDB always reserves some extents for cleanup and other internal purposes; these reserved extents are not included in the free space.

When you delete data from a table, InnoDB contracts the corresponding B-tree indexes. Whether the freed space becomes available for other users depends on whether the pattern of deletes frees individual pages or extents to the tablespace. Dropping a table or deleting all rows from it is guaranteed to release the space to other users, but remember that deleted rows are physically removed only by the purge operation, which happens automatically some time after they are no longer needed for transaction rollbacks or consistent reads. (See [Section 14.3, "InnoDB Multi-Versioning"](#page-7-0).)

# **How Pages Relate to Table Rows**

The maximum row length is slightly less than half a database page for 4KB, 8KB, 16KB, and 32KB innodb\_page\_size settings. For example, the maximum row length is slightly less than 8KB for the default 16KB InnoDB page size. For 64KB pages, the maximum row length is slightly less than 16KB.

If a row does not exceed the maximum row length, all of it is stored locally within the page. If a row exceeds the maximum row length, variable-length columns are chosen for external off-page storage until the row fits within the maximum row length limit. External off-page storage for variable-length columns differs by row format:

#### • COMPACT and REDUNDANT Row Formats

When a variable-length column is chosen for external off-page storage, InnoDB stores the first 768 bytes locally in the row, and the rest externally into overflow pages. Each such column has its own list of overflow pages. The 768-byte prefix is accompanied by a 20-byte value that stores the true length of the column and points into the overflow list where the rest of the value is stored. See [Section 14.11, "InnoDB Row Formats".](#page-145-1)

#### • DYNAMIC and COMPRESSED Row Formats

When a variable-length column is chosen for external off-page storage, InnoDB stores a 20-byte pointer locally in the row, and the rest externally into overflow pages. See [Section 14.11, "InnoDB](#page-145-1) [Row Formats".](#page-145-1)

LONGBLOB and LONGTEXT columns must be less than 4GB, and the total row length, including BLOB and TEXT columns, must be less than 4GB.

# <span id="page-154-0"></span>**14.12.3 InnoDB Checkpoints**

Making your log files very large may reduce disk I/O during checkpointing. It often makes sense to set the total size of the log files as large as the buffer pool or even larger. Although in the past large log files could make crash recovery take excessive time, starting with MySQL 5.5, performance enhancements to crash recovery make it possible to use large log files with fast startup after a crash. (Strictly speaking, this performance improvement is available for MySQL 5.1 with the InnoDB Plugin 1.0.7 and higher. It is with MySQL 5.5 that this improvement is available in the default InnoDB storage engine.)

## **How Checkpoint Processing Works**

InnoDB implements a checkpoint mechanism known as fuzzy checkpointing. InnoDB flushes modified database pages from the buffer pool in small batches. There is no need to flush the buffer pool in one single batch, which would disrupt processing of user SQL statements during the checkpointing process.

During crash recovery, InnoDB looks for a checkpoint label written to the log files. It knows that all modifications to the database before the label are present in the disk image of the database. Then InnoDB scans the log files forward from the checkpoint, applying the logged modifications to the database.

# <span id="page-154-1"></span>**14.12.4 Defragmenting a Table**

Random insertions into or deletions from a secondary index can cause the index to become fragmented. Fragmentation means that the physical ordering of the index pages on the disk is not close to the index ordering of the records on the pages, or that there are many unused pages in the 64-page blocks that were allocated to the index.

One symptom of fragmentation is that a table takes more space than it "should" take. How much that is exactly, is difficult to determine. All InnoDB data and indexes are stored in B-trees, and their fill factor may vary from 50% to 100%. Another symptom of fragmentation is that a table scan such as this takes more time than it "should" take:

```
SELECT COUNT(*) FROM t WHERE non_indexed_column <> 12345;
```

The preceding query requires MySQL to perform a full table scan, the slowest type of query for a large table.

To speed up index scans, you can periodically perform a "null" ALTER TABLE operation, which causes MySQL to rebuild the table:

```
ALTER TABLE tbl_name ENGINE=INNODB
```

You can also use ALTER TABLE tbl\_name FORCE to perform a "null" alter operation that rebuilds the table.

Both ALTER TABLE tbl\_name ENGINE=INNODB and ALTER TABLE tbl\_name FORCE use [online](#page-155-1) [DDL](#page-155-1). For more information, see [Section 14.13, "InnoDB and Online DDL"](#page-155-1).

Another way to perform a defragmentation operation is to use mysqldump to dump the table to a text file, drop the table, and reload it from the dump file.

If the insertions into an index are always ascending and records are deleted only from the end, the InnoDB filespace management algorithm guarantees that fragmentation in the index does not occur.

# <span id="page-155-0"></span>**14.12.5 Reclaiming Disk Space with TRUNCATE TABLE**

To reclaim operating system disk space when truncating an InnoDB table, the table must be stored in its own .ibd file. For a table to be stored in its own .ibd file, innodb\_file\_per\_table must enabled when the table is created. Additionally, there cannot be a foreign key constraint between the table being truncated and other tables, otherwise the TRUNCATE TABLE operation fails. A foreign key constraint between two columns in the same table, however, is permitted.

When a table is truncated, it is dropped and re-created in a new .ibd file, and the freed space is returned to the operating system. This is in contrast to truncating InnoDB tables that are stored within the InnoDB system tablespace (tables created when innodb\_file\_per\_table=OFF) and tables stored in shared general tablespaces, where only InnoDB can use the freed space after the table is truncated.

The ability to truncate tables and return disk space to the operating system also means that physical backups can be smaller. Truncating tables that are stored in the system tablespace (tables created when innodb\_file\_per\_table=OFF) or in a general tablespace leaves blocks of unused space in the tablespace.

# <span id="page-155-1"></span>**14.13 InnoDB and Online DDL**

The online DDL feature provides support for in-place table alterations and concurrent DML. Benefits of this feature include:

- Improved responsiveness and availability in busy production environments, where making a table unavailable for minutes or hours is not practical.
- The ability to adjust the balance between performance and concurrency during DDL operations using the LOCK clause. See [The LOCK clause](#page-168-1).

• Less disk space usage and I/O overhead than the table-copy method.

Typically, you do not need to do anything special to enable online DDL. By default, MySQL performs the operation in place, as permitted, with as little locking as possible.

You can control aspects of a DDL operation using the ALGORITHM and LOCK clauses of the ALTER TABLE statement. These clauses are placed at the end of the statement, separated from the table and column specifications by commas. For example:

```
ALTER TABLE tbl_name ADD PRIMARY KEY (column), ALGORITHM=INPLACE, LOCK=NONE;
```

The LOCK clause is useful for fine-tuning the degree of concurrent access to the table. The ALGORITHM clause is primarily intended for performance comparisons and as a fallback to the older table-copying behavior in case you encounter any issues. For example:

- To avoid accidentally making the table unavailable for reads, writes, or both, specify a clause on the ALTER TABLE statement such as LOCK=NONE (permit reads and writes) or LOCK=SHARED (permit reads). The operation halts immediately if the requested level of concurrency is not available.
- To compare performance between algorithms, run a statement with ALGORITHM=INPLACE and ALGORITHM=COPY. Alternatively, run a statement with the old\_alter\_table configuration option disabled and enabled.
- To avoid tying up the server with an ALTER TABLE operation that copies the table, include ALGORITHM=INPLACE. The statement halts immediately if it cannot use the in-place mechanism.

# <span id="page-156-0"></span>**14.13.1 Online DDL Operations**

Online support details, syntax examples, and usage notes for DDL operations are provided under the following topics in this section.

- [Index Operations](#page-156-1)
- [Primary Key Operations](#page-158-0)
- [Column Operations](#page-159-0)
- [Generated Column Operations](#page-162-0)
- [Foreign Key Operations](#page-163-0)
- [Table Operations](#page-164-0)
- [Tablespace Operations](#page-165-0)
- [Partitioning Operations](#page-166-0)

## <span id="page-156-1"></span>**Index Operations**

The following table provides an overview of online DDL support for index operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-157-0) [Notes](#page-157-0).

**Table 14.10 Online DDL Support for Index Operations**

| Operation                               | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|-----------------------------------------|----------|----------------|---------------------------|---------------------------|
| Creating or adding<br>a secondary index | Yes      | No             | Yes                       | No                        |
| Dropping an index                       | Yes      | No             | Yes                       | Yes                       |

| Operation                  | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|----------------------------|----------|----------------|---------------------------|---------------------------|
| Renaming an index Yes      |          | No             | Yes                       | Yes                       |
| Adding a<br>FULLTEXT index | Yes*     | No*            | No                        | No                        |
| Adding a SPATIAL<br>index  | Yes      | No             | No                        | No                        |
| Changing the index<br>type | Yes      | No             | Yes                       | Yes                       |

#### <span id="page-157-0"></span>**Syntax and Usage Notes**

• Creating or adding a secondary index

```
CREATE INDEX name ON table (col_list);
ALTER TABLE tbl_name ADD INDEX name (col_list);
```

The table remains available for read and write operations while the index is being created. The CREATE INDEX statement only finishes after all transactions that are accessing the table are completed, so that the initial state of the index reflects the most recent contents of the table.

Online DDL support for adding secondary indexes means that you can generally speed the overall process of creating and loading a table and associated indexes by creating the table without secondary indexes, then adding secondary indexes after the data is loaded.

A newly created secondary index contains only the committed data in the table at the time the CREATE INDEX or ALTER TABLE statement finishes executing. It does not contain any uncommitted values, old versions of values, or values marked for deletion but not yet removed from the old index.

If the server exits while creating a secondary index, upon recovery, MySQL drops any partially created indexes. You must re-run the ALTER TABLE or CREATE INDEX statement.

Some factors affect the performance, space usage, and semantics of this operation. For details, see [Section 14.13.6, "Online DDL Limitations".](#page-173-0)

• Dropping an index

```
DROP INDEX name ON table;
ALTER TABLE tbl_name DROP INDEX name;
```

The table remains available for read and write operations while the index is being dropped. The DROP INDEX statement only finishes after all transactions that are accessing the table are completed, so that the initial state of the index reflects the most recent contents of the table.

• Renaming an index

```
ALTER TABLE tbl_name RENAME INDEX old_index_name TO new_index_name, ALGORITHM=INPLACE, LOCK=NONE;
```

• Adding a FULLTEXT index

```
CREATE FULLTEXT INDEX name ON table(column);
```

Adding the first FULLTEXT index rebuilds the table if there is no user-defined FTS\_DOC\_ID column. Additional FULLTEXT indexes may be added without rebuilding the table.

• Adding a SPATIAL index

```
CREATE TABLE geom (g GEOMETRY NOT NULL);
```

ALTER TABLE geom ADD SPATIAL INDEX(g), ALGORITHM=INPLACE, LOCK=SHARED;

• Changing the index type (USING {BTREE | HASH})

ALTER TABLE tbl\_name DROP INDEX i1, ADD INDEX i1(key\_part,...) USING BTREE, ALGORITHM=INPLACE;

## <span id="page-158-0"></span>**Primary Key Operations**

The following table provides an overview of online DDL support for primary key operations. An asterisk indicates additional information, an exception, or a dependency. See [Syntax and Usage Notes](#page-158-1).

**Table 14.11 Online DDL Support for Primary Key Operations**

| Operation                                       | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|-------------------------------------------------|----------|----------------|---------------------------|---------------------------|
| Adding a primary<br>key                         | Yes*     | Yes*           | Yes                       | No                        |
| Dropping a primary<br>key                       | No       | Yes            | No                        | No                        |
| Dropping a primary<br>key and adding<br>another | Yes      | Yes            | Yes                       | No                        |

### <span id="page-158-1"></span>**Syntax and Usage Notes**

• Adding a primary key

ALTER TABLE tbl\_name ADD PRIMARY KEY (column), ALGORITHM=INPLACE, LOCK=NONE;

Rebuilds the table in place. Data is reorganized substantially, making it an expensive operation. ALGORITHM=INPLACE is not permitted under certain conditions if columns have to be converted to NOT NULL.

Restructuring the clustered index always requires copying of table data. Thus, it is best to define the primary key when you create a table, rather than issuing ALTER TABLE ... ADD PRIMARY KEY later.

When you create a UNIQUE or PRIMARY KEY index, MySQL must do some extra work. For UNIQUE indexes, MySQL checks that the table contains no duplicate values for the key. For a PRIMARY KEY index, MySQL also checks that none of the PRIMARY KEY columns contains a NULL.

When you add a primary key using the ALGORITHM=COPY clause, MySQL converts NULL values in the associated columns to default values: 0 for numbers, an empty string for character-based columns and BLOBs, and 0000-00-00 00:00:00 for DATETIME. This is a non-standard behavior that Oracle recommends you not rely on. Adding a primary key using ALGORITHM=INPLACE is only permitted when the SQL\_MODE setting includes the strict\_trans\_tables or strict\_all\_tables flags; when the SQL\_MODE setting is strict, ALGORITHM=INPLACE is permitted, but the statement can still fail if the requested primary key columns contain NULL values. The ALGORITHM=INPLACE behavior is more standard-compliant.

If you create a table without a primary key, InnoDB chooses one for you, which can be the first UNIQUE key defined on NOT NULL columns, or a system-generated key. To avoid uncertainty and the potential space requirement for an extra hidden column, specify the PRIMARY KEY clause as part of the CREATE TABLE statement.

MySQL creates a new clustered index by copying the existing data from the original table to a temporary table that has the desired index structure. Once the data is completely copied to the temporary table, the original table is renamed with a different temporary table name. The temporary table comprising the new clustered index is renamed with the name of the original table, and the original table is dropped from the database.

The online performance enhancements that apply to operations on secondary indexes do not apply to the primary key index. The rows of an InnoDB table are stored in a clustered index organized based on the primary key, forming what some database systems call an "index-organized table". Because the table structure is closely tied to the primary key, redefining the primary key still requires copying the data.

When an operation on the primary key uses ALGORITHM=INPLACE, even though the data is still copied, it is more efficient than using ALGORITHM=COPY because:

- No undo logging or associated redo logging is required for ALGORITHM=INPLACE. These operations add overhead to DDL statements that use ALGORITHM=COPY.
- The secondary index entries are pre-sorted, and so can be loaded in order.
- The change buffer is not used, because there are no random-access inserts into the secondary indexes.

If the server exits while creating a new clustered index, no data is lost, but you must complete the recovery process using the temporary tables that exist during the process. Since it is rare to recreate a clustered index or re-define primary keys on large tables, or to encounter a system crash during this operation, this manual does not provide information on recovering from this scenario.

• Dropping a primary key

```
ALTER TABLE tbl_name DROP PRIMARY KEY, ALGORITHM=COPY;
```

Only ALGORITHM=COPY supports dropping a primary key without adding a new one in the same ALTER TABLE statement.

• Dropping a primary key and adding another

```
ALTER TABLE tbl_name DROP PRIMARY KEY, ADD PRIMARY KEY (column), ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

## <span id="page-159-0"></span>**Column Operations**

The following table provides an overview of online DDL support for column operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-160-0) [Notes](#page-160-0).

**Table 14.12 Online DDL Support for Column Operations**

| Operation                           | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|-------------------------------------|----------|----------------|---------------------------|---------------------------|
| Adding a column                     | Yes      | Yes            | Yes*                      | No                        |
| Dropping a column                   | Yes      | Yes            | Yes                       | No                        |
| Renaming a<br>column                | Yes      | No             | Yes*                      | Yes                       |
| Reordering<br>columns               | Yes      | Yes            | Yes                       | No                        |
| Setting a column<br>default value   | Yes      | No             | Yes                       | Yes                       |
| Changing the<br>column data type    | No       | Yes            | No                        | No                        |
| Extending<br>VARCHAR column<br>size | Yes      | No             | Yes                       | Yes                       |

| Operation                                                  | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|------------------------------------------------------------|----------|----------------|---------------------------|---------------------------|
| Dropping the<br>column default<br>value                    | Yes      | No             | Yes                       | Yes                       |
| Changing the auto<br>increment value                       | Yes      | No             | Yes                       | No*                       |
| Making a column<br>NULL                                    | Yes      | Yes*           | Yes                       | No                        |
| Making a column<br>NOT NULL                                | Yes*     | Yes*           | Yes                       | No                        |
| Modifying the<br>definition of an<br>ENUM or SET<br>column | Yes      | No             | Yes                       | Yes                       |

### <span id="page-160-0"></span>**Syntax and Usage Notes**

• Adding a column

```
ALTER TABLE tbl_name ADD COLUMN column_name column_definition, ALGORITHM=INPLACE, LOCK=NONE;
```

Concurrent DML is not permitted when adding an auto-increment column. Data is reorganized substantially, making it an expensive operation. At a minimum, ALGORITHM=INPLACE, LOCK=SHARED is required.

• Dropping a column

```
ALTER TABLE tbl_name DROP COLUMN column_name, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

• Renaming a column

```
ALTER TABLE tbl CHANGE old_col_name new_col_name data_type, ALGORITHM=INPLACE, LOCK=NONE;
```

To permit concurrent DML, keep the same data type and only change the column name.

When you keep the same data type and [NOT] NULL attribute, only changing the column name, the operation can always be performed online.

You can also rename a column that is part of a foreign key constraint. The foreign key definition is automatically updated to use the new column name. Renaming a column participating in a foreign key only works with ALGORITHM=INPLACE. If you use the ALGORITHM=COPY clause, or some other condition causes the operation to use ALGORITHM=COPY, the ALTER TABLE statement fails.

ALGORITHM=INPLACE is not supported for renaming a generated column.

• Reordering columns

To reorder columns, use FIRST or AFTER in CHANGE or MODIFY operations.

```
ALTER TABLE tbl_name MODIFY COLUMN col_name column_definition FIRST, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

• Changing the column data type

```
ALTER TABLE tbl_name CHANGE c1 c1 BIGINT, ALGORITHM=COPY;
```

Changing the column data type is only supported with ALGORITHM=COPY.

• Extending VARCHAR column size

```
ALTER TABLE tbl_name CHANGE COLUMN c1 c1 VARCHAR(255), ALGORITHM=INPLACE, LOCK=NONE;
```

The number of length bytes required by a VARCHAR column must remain the same. For VARCHAR columns of 0 to 255 bytes in size, one length byte is required to encode the value. For VARCHAR columns of 256 bytes in size or more, two length bytes are required. As a result, in-place ALTER TABLE only supports increasing VARCHAR column size from 0 to 255 bytes, or from 256 bytes to a greater size. In-place ALTER TABLE does not support increasing the size of a VARCHAR column from less than 256 bytes to a size equal to or greater than 256 bytes. In this case, the number of required length bytes changes from 1 to 2, which is only supported by a table copy (ALGORITHM=COPY). For example, attempting to change VARCHAR column size for a single byte character set from VARCHAR(255) to VARCHAR(256) using in-place ALTER TABLE returns this error:

ALTER TABLE tbl\_name ALGORITHM=INPLACE, CHANGE COLUMN c1 c1 VARCHAR(256); ERROR 0A000: ALGORITHM=INPLACE is not supported. Reason: Cannot change column type INPLACE. Try ALGORITHM=COPY.

![](_page_161_Picture_5.jpeg)

#### **Note**

The byte length of a VARCHAR column is dependant on the byte length of the character set.

Decreasing VARCHAR size using in-place ALTER TABLE is not supported. Decreasing VARCHAR size requires a table copy (ALGORITHM=COPY).

• Setting a column default value

```
ALTER TABLE tbl_name ALTER COLUMN col SET DEFAULT literal, ALGORITHM=INPLACE, LOCK=NONE;
```

Only modifies table metadata. Default column values are stored in the .frm file for the table, not the InnoDB data dictionary.

• Dropping a column default value

```
ALTER TABLE tbl ALTER COLUMN col DROP DEFAULT, ALGORITHM=INPLACE, LOCK=NONE;
```

• Changing the auto-increment value

```
ALTER TABLE table AUTO_INCREMENT=next_value, ALGORITHM=INPLACE, LOCK=NONE;
```

Modifies a value stored in memory, not the data file.

In a distributed system using replication or sharding, you sometimes reset the auto-increment counter for a table to a specific value. The next row inserted into the table uses the specified value for its auto-increment column. You might also use this technique in a data warehousing environment where you periodically empty all the tables and reload them, and restart the autoincrement sequence from 1.

• Making a column NULL

```
ALTER TABLE tbl_name MODIFY COLUMN column_name data_type NULL, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table in place. Data is reorganized substantially, making it an expensive operation.

• Making a column NOT NULL

```
ALTER TABLE tbl_name MODIFY COLUMN column_name data_type NOT NULL, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table in place. STRICT\_ALL\_TABLES or STRICT\_TRANS\_TABLES SQL\_MODE is required for the operation to succeed. The operation fails if the column contains NULL values. The server prohibits changes to foreign key columns that have the potential to cause loss of referential integrity. See Section 13.1.8, "ALTER TABLE Statement". Data is reorganized substantially, making it an expensive operation.

• Modifying the definition of an ENUM or SET column

```
CREATE TABLE t1 (c1 ENUM('a', 'b', 'c'));
ALTER TABLE t1 MODIFY COLUMN c1 ENUM('a', 'b', 'c', 'd'), ALGORITHM=INPLACE, LOCK=NONE;
```

Modifying the definition of an ENUM or SET column by adding new enumeration or set members to the end of the list of valid member values may be performed in place, as long as the storage size of the data type does not change. For example, adding a member to a SET column that has 8 members changes the required storage per value from 1 byte to 2 bytes; this requires a table copy. Adding members in the middle of the list causes renumbering of existing members, which requires a table copy.

# <span id="page-162-0"></span>**Generated Column Operations**

The following table provides an overview of online DDL support for generated column operations. For details, see [Syntax and Usage Notes.](#page-162-1)

**Table 14.13 Online DDL Support for Generated Column Operations**

| Operation                            | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|--------------------------------------|----------|----------------|---------------------------|---------------------------|
| Adding a STORED<br>column            | No       | Yes            | No                        | No                        |
| Modifying STORED<br>column order     | No       | Yes            | No                        | No                        |
| Dropping a<br>STORED column          | Yes      | Yes            | Yes                       | No                        |
| Adding a VIRTUAL<br>column           | Yes      | No             | Yes                       | Yes                       |
| Modifying<br>VIRTUAL column<br>order | No       | Yes            | No                        | No                        |
| Dropping a<br>VIRTUAL column         | Yes      | No             | Yes                       | Yes                       |

#### <span id="page-162-1"></span>**Syntax and Usage Notes**

• Adding a STORED column

```
ALTER TABLE t1 ADD COLUMN (c2 INT GENERATED ALWAYS AS (c1 + 1) STORED), ALGORITHM=COPY;
```

ADD COLUMN is not an in-place operation for stored columns (done without using a temporary table) because the expression must be evaluated by the server.

• Modifying STORED column order

```
ALTER TABLE t1 MODIFY COLUMN c2 INT GENERATED ALWAYS AS (c1 + 1) STORED FIRST, ALGORITHM=COPY;
```

Rebuilds the table in place.

• Dropping a STORED column

```
ALTER TABLE t1 DROP COLUMN c2, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table in place.

• Adding a VIRTUAL column

```
ALTER TABLE t1 ADD COLUMN (c2 INT GENERATED ALWAYS AS (c1 + 1) VIRTUAL), ALGORITHM=INPLACE, LOCK=NONE;
```

Adding a virtual column is an in-place operation for non-partitioned tables. However, adding a virtual column cannot be combined with other ALTER TABLE actions.

Adding a VIRTUAL is not an in-place operation for partitioned tables.

• Modifying VIRTUAL column order

ALTER TABLE t1 MODIFY COLUMN c2 INT GENERATED ALWAYS AS (c1 + 1) VIRTUAL FIRST, ALGORITHM=COPY;

• Dropping a VIRTUAL column

```
ALTER TABLE t1 DROP COLUMN c2, ALGORITHM=INPLACE, LOCK=NONE;
```

Dropping a VIRTUAL column is an in-place operation for non-partitioned tables. However, dropping a virtual column cannot be combined with other ALTER TABLE actions.

Dropping a VIRTUAL is not an in-place operation for partitioned tables.

# <span id="page-163-0"></span>**Foreign Key Operations**

The following table provides an overview of online DDL support for foreign key operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-163-1) [Notes](#page-163-1).

**Table 14.14 Online DDL Support for Foreign Key Operations**

| Operation                            | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|--------------------------------------|----------|----------------|---------------------------|---------------------------|
| Adding a foreign<br>key constraint   | Yes*     | No             | Yes                       | Yes                       |
| Dropping a foreign<br>key constraint | Yes      | No             | Yes                       | Yes                       |

### <span id="page-163-1"></span>**Syntax and Usage Notes**

• Adding a foreign key constraint

The INPLACE algorithm is supported when foreign\_key\_checks is disabled. Otherwise, only the COPY algorithm is supported.

```
ALTER TABLE tbl1 ADD CONSTRAINT fk_name FOREIGN KEY index (col1)
 REFERENCES tbl2(col2) referential_actions;
```

• Dropping a foreign key constraint

```
ALTER TABLE tbl DROP FOREIGN KEY fk_name;
```

Dropping a foreign key can be performed online with the foreign\_key\_checks option enabled or disabled.

If you do not know the names of the foreign key constraints on a particular table, issue the following statement and find the constraint name in the CONSTRAINT clause for each foreign key:

```
SHOW CREATE TABLE table\G
```

Or, query the Information Schema TABLE\_CONSTRAINTS table and use the CONSTRAINT\_NAME and CONSTRAINT\_TYPE columns to identify the foreign key names.

You can also drop a foreign key and its associated index in a single statement:

```
ALTER TABLE table DROP FOREIGN KEY constraint, DROP INDEX index;
```

![](_page_164_Picture_1.jpeg)

#### **Note**

If foreign keys are already present in the table being altered (that is, it is a child table containing a FOREIGN KEY ... REFERENCE clause), additional restrictions apply to online DDL operations, even those not directly involving the foreign key columns:

- An ALTER TABLE on the child table could wait for another transaction to commit, if a change to the parent table causes associated changes in the child table through an ON UPDATE or ON DELETE clause using the CASCADE or SET NULL parameters.
- In the same way, if a table is the parent table in a foreign key relationship, even though it does not contain any FOREIGN KEY clauses, it could wait for the ALTER TABLE to complete if an INSERT, UPDATE, or DELETE statement causes an ON UPDATE or ON DELETE action in the child table.

# <span id="page-164-0"></span>**Table Operations**

The following table provides an overview of online DDL support for table operations. An asterisk indicates additional information, an exception, or a dependency. For details, see [Syntax and Usage](#page-164-1) [Notes](#page-164-1).

**Table 14.15 Online DDL Support for Table Operations**

| Operation                              | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|----------------------------------------|----------|----------------|---------------------------|---------------------------|
| Changing the<br>ROW_FORMAT             | Yes      | Yes            | Yes                       | No                        |
| Changing the<br>KEY_BLOCK_SIZE         | Yes      | Yes            | Yes                       | No                        |
| Setting persistent<br>table statistics | Yes      | No             | Yes                       | Yes                       |
| Specifying a<br>character set          | Yes      | Yes*           | Yes                       | No                        |
| Converting a<br>character set          | No       | Yes*           | No                        | No                        |
| Optimizing a table                     | Yes*     | Yes            | Yes                       | No                        |
| Rebuilding with the<br>FORCE option    | Yes*     | Yes            | Yes                       | No                        |
| Performing a null<br>rebuild           | Yes*     | Yes            | Yes                       | No                        |
| Renaming a table                       | Yes      | No             | Yes                       | Yes                       |

#### <span id="page-164-1"></span>**Syntax and Usage Notes**

• Changing the ROW\_FORMAT

```
ALTER TABLE tbl_name ROW_FORMAT = row_format, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

For additional information about the ROW\_FORMAT option, see Table Options.

• Changing the KEY\_BLOCK\_SIZE

```
ALTER TABLE tbl_name KEY_BLOCK_SIZE = value, ALGORITHM=INPLACE, LOCK=NONE;
```

Data is reorganized substantially, making it an expensive operation.

For additional information about the KEY\_BLOCK\_SIZE option, see Table Options.

• Setting persistent table statistics options

```
ALTER TABLE tbl_name STATS_PERSISTENT=0, STATS_SAMPLE_PAGES=20, STATS_AUTO_RECALC=1, ALGORITHM=INPLACE, LOCK=NONE;
```

Only modifies table metadata.

Persistent statistics include STATS\_PERSISTENT, STATS\_AUTO\_RECALC, and STATS\_SAMPLE\_PAGES. For more information, see [Section 14.8.11.1, "Configuring Persistent](#page-110-0) [Optimizer Statistics Parameters"](#page-110-0).

• Specifying a character set

```
ALTER TABLE tbl_name CHARACTER SET = charset_name, ALGORITHM=INPLACE, LOCK=NONE;
```

Rebuilds the table if the new character encoding is different.

• Converting a character set

```
ALTER TABLE tbl_name CONVERT TO CHARACTER SET charset_name, ALGORITHM=COPY;
```

Rebuilds the table if the new character encoding is different.

• Optimizing a table

```
OPTIMIZE TABLE tbl_name;
```

In-place operation is not supported for tables with FULLTEXT indexes. The operation uses the INPLACE algorithm, but ALGORITHM and LOCK syntax is not permitted.

• Rebuilding a table with the FORCE option

```
ALTER TABLE tbl_name FORCE, ALGORITHM=INPLACE, LOCK=NONE;
```

Uses ALGORITHM=INPLACE as of MySQL 5.6.17. ALGORITHM=INPLACE is not supported for tables with FULLTEXT indexes.

• Performing a "null" rebuild

```
ALTER TABLE tbl_name ENGINE=InnoDB, ALGORITHM=INPLACE, LOCK=NONE;
```

Uses ALGORITHM=INPLACE as of MySQL 5.6.17. ALGORITHM=INPLACE is not supported for tables with FULLTEXT indexes.

• Renaming a table

```
ALTER TABLE old_tbl_name RENAME TO new_tbl_name, ALGORITHM=INPLACE, LOCK=NONE;
```

MySQL renames files that correspond to the table tbl\_name without making a copy. (You can also use the RENAME TABLE statement to rename tables. See Section 13.1.33, "RENAME TABLE Statement".) Privileges granted specifically for the renamed table are not migrated to the new name. They must be changed manually.

## <span id="page-165-0"></span>**Tablespace Operations**

The following table provides an overview of online DDL support for tablespace operations. For details, see [Syntax and Usage Notes.](#page-166-1)

**Table 14.16 Online DDL Support for Tablespace Operations**

| Operation                                                           | In Place | Rebuilds Table | Permits<br>Concurrent DML | Only Modifies<br>Metadata |
|---------------------------------------------------------------------|----------|----------------|---------------------------|---------------------------|
| Enabling or<br>disabling file-per<br>table tablespace<br>encryption | No       | Yes            | No                        | No                        |

#### <span id="page-166-1"></span>**Syntax and Usage Notes**

Enabling or disabling file-per-table tablespace encryption

ALTER TABLE tbl\_name ENCRYPTION='Y', ALGORITHM=COPY;

Encryption is only supported for file-per-table tablespaces. For related information, see [Section 14.14,](#page-174-0) ["InnoDB Data-at-Rest Encryption"](#page-174-0).

# <span id="page-166-0"></span>**Partitioning Operations**

With the exception of most ALTER TABLE partitioning clauses, online DDL operations for partitioned InnoDB tables follow the same rules that apply to regular InnoDB tables.

Most ALTER TABLE partitioning clauses do not go through the same internal online DDL API as regular non-partitioned InnoDB tables. As a result, online support for ALTER TABLE partitioning clauses varies.

The following table shows the online status for each ALTER TABLE partitioning statement. Regardless of the online DDL API that is used, MySQL attempts to minimize data copying and locking where possible.

ALTER TABLE partitioning options that use ALGORITHM=COPY or that only permit "ALGORITHM=DEFAULT, LOCK=DEFAULT", repartition the table using the COPY algorithm. In other words, a new partitioned table is created with the new partitioning scheme. The newly created table includes any changes applied by the ALTER TABLE statement, and table data is copied into the new table structure.

**Table 14.17 Online DDL Support for Partitioning Operations**

| Partitioning Clause | In Place | Permits DML | Notes                                                                                                                                                                                                                                                                           |
|---------------------|----------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PARTITION BY        | No       | No          | Permits<br>ALGORITHM=COPY,<br>LOCK={DEFAULT <br>SHARED EXCLUSIVE}                                                                                                                                                                                                               |
| ADD PARTITION       | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT. Does<br>not copy existing data<br>for tables partitioned<br>by RANGE or LIST.<br>Concurrent queries are<br>permitted for tables<br>partitioned by HASH or<br>LIST. MySQL copies<br>the data while holding a<br>shared lock. |
| DROP PARTITION      | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT. Does<br>not copy existing data                                                                                                                                                                                              |

| Partitioning Clause     | In Place | Permits DML | Notes                                                                                                                                                                                                                                        |
|-------------------------|----------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                         |          |             | for tables partitioned by<br>RANGE or LIST.                                                                                                                                                                                                  |
| DISCARD PARTITION       | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT                                                                                                                                                                                           |
| IMPORT PARTITION        | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT                                                                                                                                                                                           |
| TRUNCATE PARTITION      | Yes      | Yes         | Does not copy existing<br>data. It merely deletes<br>rows; it does not alter<br>the definition of the table<br>itself, or of any of its<br>partitions.                                                                                       |
| COALESCE PARTITION      | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT.<br>Concurrent queries are<br>permitted for tables<br>partitioned by HASH or<br>LIST, as MySQL copies<br>the data while holding a<br>shared lock.                                         |
| REORGANIZE<br>PARTITION | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT.<br>Concurrent queries<br>are permitted for<br>tables partitioned by<br>LINEAR HASH or LIST.<br>MySQL copies data<br>from affected partitions<br>while holding a shared<br>metadata lock. |
| EXCHANGE PARTITION      | Yes      | Yes         |                                                                                                                                                                                                                                              |
| ANALYZE PARTITION       | Yes      | Yes         |                                                                                                                                                                                                                                              |
| CHECK PARTITION         | Yes      | Yes         |                                                                                                                                                                                                                                              |
| OPTIMIZE PARTITION      | No       | No          | ALGORITHM and<br>LOCK clauses are<br>ignored. Rebuilds<br>the entire table.<br>See Section 22.3.4,<br>"Maintenance of<br>Partitions".                                                                                                        |
| REBUILD PARTITION       | No       | No          | Only permits<br>ALGORITHM=DEFAULT,<br>LOCK=DEFAULT.<br>Concurrent queries<br>are permitted for<br>tables partitioned by<br>LINEAR HASH or LIST.<br>MySQL copies data<br>from affected partitions                                             |

| Partitioning Clause | In Place | Permits DML | Notes                                    |
|---------------------|----------|-------------|------------------------------------------|
|                     |          |             | while holding a shared<br>metadata lock. |
| REPAIR PARTITION    | Yes      | Yes         |                                          |
| REMOVE              | No       | No          | Permits                                  |
| PARTITIONING        |          |             | ALGORITHM=COPY,                          |
|                     |          |             | LOCK={DEFAULT                            |
|                     |          |             | SHARED EXCLUSIVE}                        |

Non-partitioning online ALTER TABLE operations on partitioned tables follow the same rules that apply to regular tables. However, ALTER TABLE performs online operations on each table partition, which causes increased demand on system resources due to operations being performed on multiple partitions.

For additional information about ALTER TABLE partitioning clauses, see Partitioning Options, and Section 13.1.8.1, "ALTER TABLE Partition Operations". For information about partitioning in general, see Chapter 22, Partitioning.

# <span id="page-168-0"></span>**14.13.2 Online DDL Performance and Concurrency**

Online DDL improves several aspects of MySQL operation:

- Applications that access the table are more responsive because queries and DML operations on the table can proceed while the DDL operation is in progress. Reduced locking and waiting for MySQL server resources leads to greater scalability, even for operations that are not involved in the DDL operation.
- In-place operations avoid the disk I/O and CPU cycles associated with the table-copy method, which minimizes overall load on the database. Minimizing load helps maintain good performance and high throughput during the DDL operation.
- In-place operations read less data into the buffer pool than the table-copy operations, which reduces purging of frequently accessed data from memory. Purging of frequently accessed data can cause a temporary performance dip after a DDL operation.

# <span id="page-168-1"></span>**The LOCK clause**

By default, MySQL uses as little locking as possible during a DDL operation. The LOCK clause can be specified to enforce more restrictive locking, if required. If the LOCK clause specifies a less restrictive level of locking than is permitted for a particular DDL operation, the statement fails with an error. LOCK clauses are described below, in order of least to most restrictive:

# • LOCK=NONE:

Permits concurrent queries and DML.

For example, use this clause for tables involving customer signups or purchases, to avoid making the tables unavailable during lengthy DDL operations.

#### • LOCK=SHARED:

Permits concurrent queries but blocks DML.

For example, use this clause on data warehouse tables, where you can delay data load operations until the DDL operation is finished, but queries cannot be delayed for long periods.

# • LOCK=DEFAULT:

Permits as much concurrency as possible (concurrent queries, DML, or both). Omitting the LOCK clause is the same as specifying LOCK=DEFAULT.

Use this clause when you know that the default locking level of the DDL statement does not cause availability problems for the table.

#### • LOCK=EXCLUSIVE:

Blocks concurrent queries and DML.

Use this clause if the primary concern is finishing the DDL operation in the shortest amount of time possible, and concurrent query and DML access is not necessary. You might also use this clause if the server is supposed to be idle, to avoid unexpected table accesses.

# **Online DDL and Metadata Locks**

Online DDL operations can be viewed as having three phases:

#### • Phase 1: Initialization

In the initialization phase, the server determines how much concurrency is permitted during the operation, taking into account storage engine capabilities, operations specified in the statement, and user-specified ALGORITHM and LOCK options. During this phase, a shared upgradeable metadata lock is taken to protect the current table definition.

#### • Phase 2: Execution

In this phase, the statement is prepared and executed. Whether the metadata lock is upgraded to exclusive depends on the factors assessed in the initialization phase. If an exclusive metadata lock is required, it is only taken briefly during statement preparation.

#### • Phase 3: Commit Table Definition

In the commit table definition phase, the metadata lock is upgraded to exclusive to evict the old table definition and commit the new one. Once granted, the duration of the exclusive metadata lock is brief.

Due to the exclusive metadata lock requirements outlined above, an online DDL operation may have to wait for concurrent transactions that hold metadata locks on the table to commit or rollback. Transactions started before or during the DDL operation can hold metadata locks on the table being altered. In the case of a long running or inactive transaction, an online DDL operation can time out waiting for an exclusive metadata lock. Additionally, a pending exclusive metadata lock requested by an online DDL operation blocks subsequent transactions on the table.

The following example demonstrates an online DDL operation waiting for an exclusive metadata lock, and how a pending metadata lock blocks subsequent transactions on the table.

### Session 1:

```
mysql> CREATE TABLE t1 (c1 INT) ENGINE=InnoDB;
mysql> START TRANSACTION;
mysql> SELECT * FROM t1;
```

The session 1 SELECT statement takes a shared metadata lock on table t1.

#### Session 2:

```
mysql> ALTER TABLE t1 ADD COLUMN x INT, ALGORITHM=INPLACE, LOCK=NONE;
```

The online DDL operation in session 2, which requires an exclusive metadata lock on table t1 to commit table definition changes, must wait for the session 1 transaction to commit or roll back.

#### Session 3:

```
mysql> SELECT * FROM t1;
```

The SELECT statement issued in session 3 is blocked waiting for the exclusive metadata lock requested by the ALTER TABLE operation in session 2 to be granted.

You can use SHOW FULL PROCESSLIST to determine if transactions are waiting for a metadata lock.

```
mysql> SHOW FULL PROCESSLIST\G
...
*************************** 2. row ***************************
 Id: 5
 User: root
 Host: localhost
 db: test
Command: Query
 Time: 44
 State: Waiting for table metadata lock
 Info: ALTER TABLE t1 ADD COLUMN x INT, ALGORITHM=INPLACE, LOCK=NONE
...
*************************** 4. row ***************************
 Id: 7
 User: root
 Host: localhost
 db: test
Command: Query
 Time: 5
 State: Waiting for table metadata lock
 Info: SELECT * FROM t1
4 rows in set (0.00 sec)
```

Metadata lock information is also exposed through the Performance Schema metadata\_locks table, which provides information about metadata lock dependencies between sessions, the metadata lock a session is waiting for, and the session that currently holds the metadata lock. For more information, see Section 25.12.12.1, "The metadata\_locks Table".

## **Online DDL Performance**

The performance of a DDL operation is largely determined by whether the operation is performed in place and whether it rebuilds the table.

To assess the relative performance of a DDL operation, you can compare results using ALGORITHM=INPLACE with results using ALGORITHM=COPY. Alternatively, you can compare results with old\_alter\_table disabled and enabled.

For DDL operations that modify table data, you can determine whether a DDL operation performs changes in place or performs a table copy by looking at the "rows affected" value displayed after the command finishes. For example:

• Changing the default value of a column (fast, does not affect the table data):

```
Query OK, 0 rows affected (0.07 sec)
```

• Adding an index (takes time, but 0 rows affected shows that the table is not copied):

```
Query OK, 0 rows affected (21.42 sec)
```

• Changing the data type of a column (takes substantial time and requires rebuilding all the rows of the table):

```
Query OK, 1671168 rows affected (1 min 35.54 sec)
```

Before running a DDL operation on a large table, check whether the operation is fast or slow as follows:

- 1. Clone the table structure.
- 2. Populate the cloned table with a small amount of data.

- 3. Run the DDL operation on the cloned table.
- 4. Check whether the "rows affected" value is zero or not. A nonzero value means the operation copies table data, which might require special planning. For example, you might do the DDL operation during a period of scheduled downtime, or on each replica server one at a time.

![](_page_171_Picture_3.jpeg)

#### **Note**

For a greater understanding of the MySQL processing associated with a DDL operation, examine Performance Schema and INFORMATION\_SCHEMA tables related to InnoDB before and after DDL operations to see the number of physical reads, writes, memory allocations, and so on.

Performance Schema stage events can be used to monitor ALTER TABLE progress. See Section 14.17.1, "Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance Schema".

Because there is some processing work involved with recording the changes made by concurrent DML operations, then applying those changes at the end, an online DDL operation could take longer overall than the table-copy mechanism that blocks table access from other sessions. The reduction in raw performance is balanced against better responsiveness for applications that use the table. When evaluating the techniques for changing table structure, consider end-user perception of performance, based on factors such as load times for web pages.

# <span id="page-171-0"></span>**14.13.3 Online DDL Space Requirements**

Online DDL operations have the following space requirements:

• Temporary log files:

A temporary log file records concurrent DML when an online DDL operation creates an index or alters a table. The temporary log file is extended as required by the value of innodb\_sort\_buffer\_size up to a maximum specified by innodb\_online\_alter\_log\_max\_size. If the operation takes a long time and concurrent DML modifies the table so much that the size of the temporary log file exceeds the value of innodb\_online\_alter\_log\_max\_size, the online DDL operation fails with a DB\_ONLINE\_LOG\_TOO\_BIG error and uncommitted concurrent DML operations are rolled back. A large innodb\_online\_alter\_log\_max\_size setting permits more DML during an online DDL operation, but it also extends the period of time at the end of the DDL operation when the table is locked to apply logged DML.

The innodb\_sort\_buffer\_size variable also defines the size of the temporary log file read buffer and write buffer.

• Temporary sort files:

Online DDL operations that rebuild the table write temporary sort files to the MySQL temporary directory (\$TMPDIR on Unix, %TEMP% on Windows, or the directory specified by --tmpdir) during index creation. Temporary sort files are not created in the directory that contains the original table. Each temporary sort file is large enough to hold one column of data, and each sort file is removed when its data is merged into the final table or index. Operations involving temporary sort files may require temporary space equal to the amount of data in the table plus indexes. An error is reported if online DDL operation uses all of the available disk space on the file system where the data directory resides.

If the MySQL temporary directory is not large enough to hold the sort files, set tmpdir to a different directory. Alternatively, define a separate temporary directory for online DDL operations using innodb\_tmpdir. This option was introduced in MySQL 5.7.11 to help avoid temporary directory overflows that could occur as a result of large temporary sort files.

• Intermediate table files:

Some online DDL operations that rebuild the table create a temporary intermediate table file in the same directory as the original table. An intermediate table file may require space equal to the size of the original table. Intermediate table file names begin with #sql-ib prefix and only appear briefly during the online DDL operation.

The innodb\_tmpdir option is not applicable to intermediate table files.

# <span id="page-172-0"></span>**14.13.4 Simplifying DDL Statements with Online DDL**

Before the introduction of online DDL, it was common practice to combine many DDL operations into a single ALTER TABLE statement. Because each ALTER TABLE statement involved copying and rebuilding the table, it was more efficient to make several changes to the same table at once, since those changes could all be done with a single rebuild operation for the table. The downside was that SQL code involving DDL operations was harder to maintain and to reuse in different scripts. If the specific changes were different each time, you might have to construct a new complex ALTER TABLE for each slightly different scenario.

For DDL operations that can be done in place, you can separate them into individual ALTER TABLE statements for easier scripting and maintenance, without sacrificing efficiency. For example, you might take a complicated statement such as:

```
ALTER TABLE t1 ADD INDEX i1(c1), ADD UNIQUE INDEX i2(c2),
 CHANGE c4_old_name c4_new_name INTEGER UNSIGNED;
```

and break it down into simpler parts that can be tested and performed independently, such as:

```
ALTER TABLE t1 ADD INDEX i1(c1);
ALTER TABLE t1 ADD UNIQUE INDEX i2(c2);
ALTER TABLE t1 CHANGE c4_old_name c4_new_name INTEGER UNSIGNED NOT NULL;
```

You might still use multi-part ALTER TABLE statements for:

- Operations that must be performed in a specific sequence, such as creating an index followed by a foreign key constraint that uses that index.
- Operations all using the same specific LOCK clause, that you want to either succeed or fail as a group.
- Operations that cannot be performed in place, that is, that still use the table-copy method.
- Operations for which you specify ALGORITHM=COPY or old\_alter\_table=1, to force the tablecopying behavior if needed for precise backward-compatibility in specialized scenarios.

# <span id="page-172-1"></span>**14.13.5 Online DDL Failure Conditions**

The failure of an online DDL operation is typically due to one of the following conditions:

- An ALGORITHM clause specifies an algorithm that is not compatible with the particular type of DDL operation or storage engine.
- A LOCK clause specifies a low degree of locking (SHARED or NONE) that is not compatible with the particular type of DDL operation.
- A timeout occurs while waiting for an exclusive lock on the table, which may be needed briefly during the initial and final phases of the DDL operation.
- The tmpdir or innodb\_tmpdir file system runs out of disk space, while MySQL writes temporary sort files on disk during index creation. For more information, see [Section 14.13.3, "Online DDL](#page-171-0) [Space Requirements".](#page-171-0)
- The operation takes a long time and concurrent DML modifies the table so much that the size of the temporary online log exceeds the value of the innodb\_online\_alter\_log\_max\_size configuration option. This condition causes a DB\_ONLINE\_LOG\_TOO\_BIG error.

• Concurrent DML makes changes to the table that are allowed with the original table definition, but not with the new one. The operation only fails at the very end, when MySQL tries to apply all the changes from concurrent DML statements. For example, you might insert duplicate values into a column while a unique index is being created, or you might insert NULL values into a column while creating a primary key index on that column. The changes made by the concurrent DML take precedence, and the ALTER TABLE operation is effectively rolled back.

# <span id="page-173-0"></span>**14.13.6 Online DDL Limitations**

The following limitations apply to online DDL operations:

- The table is copied when creating an index on a TEMPORARY TABLE.
- The ALTER TABLE clause LOCK=NONE is not permitted if there are ON...CASCADE or ON...SET NULL constraints on the table.
- Before an online DDL operation can finish, it must wait for transactions that hold metadata locks on the table to commit or roll back. An online DDL operation may briefly require an exclusive metadata lock on the table during its execution phase, and always requires one in the final phase of the operation when updating the table definition. Consequently, transactions holding metadata locks on the table can cause an online DDL operation to block. The transactions that hold metadata locks on the table may have been started before or during the online DDL operation. A long running or inactive transaction that holds a metadata lock on the table can cause an online DDL operation to timeout.
- An online DDL operation on a table in a foreign key relationship does not wait for a transaction executing on the other table in the foreign key relationship to commit or rollback. The transaction holds an exclusive metadata lock on the table it is updating and shared metadata lock on the foreign-key-related table (required for foreign key checking). The shared metadata lock permits the online DDL operation to proceed but blocks the operation in its final phase, when an exclusive metadata lock is required to update the table definition. This scenario can result in deadlocks as other transactions wait for the online DDL operation to finish.
- When running an online DDL operation, the thread that runs the ALTER TABLE statement applies an online log of DML operations that were run concurrently on the same table from other connection threads. When the DML operations are applied, it is possible to encounter a duplicate key entry error (ERROR 1062 (23000): Duplicate entry), even if the duplicate entry is only temporary and would be reverted by a later entry in the online log. This is similar to the idea of a foreign key constraint check in InnoDB in which constraints must hold during a transaction.
- OPTIMIZE TABLE for an InnoDB table is mapped to an ALTER TABLE operation to rebuild the table and update index statistics and free unused space in the clustered index. Secondary indexes are not created as efficiently because keys are inserted in the order they appeared in the primary key. OPTIMIZE TABLE is supported with the addition of online DDL support for rebuilding regular and partitioned InnoDB tables.
- Tables created before MySQL 5.6 that include temporal columns (DATE, DATETIME or TIMESTAMP) and have not been rebuilt using ALGORITHM=COPY do not support ALGORITHM=INPLACE. In this case, an ALTER TABLE ... ALGORITHM=INPLACE operation returns the following error:

```
ERROR 1846 (0A000): ALGORITHM=INPLACE is not supported.
Reason: Cannot change column type INPLACE. Try ALGORITHM=COPY.
```

- The following limitations are generally applicable to online DDL operations on large tables that involve rebuilding the table:
  - There is no mechanism to pause an online DDL operation or to throttle I/O or CPU usage for an online DDL operation.
  - Rollback of an online DDL operation can be expensive should the operation fail.

• Long running online DDL operations can cause replication lag. An online DDL operation must finish running on the source before it is run on the replica. Also, DML that was processed concurrently on the source is only processed on the replica after the DDL operation on the replica is completed.

For additional information related to running online DDL operations on large tables, see [Section 14.13.2, "Online DDL Performance and Concurrency"](#page-168-0).

# <span id="page-174-0"></span>**14.14 InnoDB Data-at-Rest Encryption**

InnoDB supports data-at-rest encryption for file-per-table tablespaces.

- [About Data-at-Rest Encryption](#page-174-1)
- [Encryption Prerequisites](#page-175-0)
- [Enabling File-Per-Table Tablespace Encryption](#page-175-1)
- [Master Key Rotation](#page-176-0)
- [Encryption and Recovery](#page-176-1)
- [Exporting Encrypted Tablespaces](#page-176-2)
- [Encryption and Replication](#page-177-0)
- [Identifying Encrypted Tablespaces](#page-177-1)
- [Encryption Usage Notes](#page-177-2)
- [Encryption Limitations](#page-178-1)

# <span id="page-174-1"></span>**About Data-at-Rest Encryption**

InnoDB uses a two tier encryption key architecture, consisting of a master encryption key and tablespace keys. When a tablespace is encrypted, a tablespace key is encrypted and stored in the tablespace header. When an application or authenticated user wants to access encrypted data, InnoDB uses a master encryption key to decrypt the tablespace key. The decrypted version of a tablespace key never changes, but the master encryption key can be changed as required. This action is referred to as master key rotation.

The data-at-rest encryption feature relies on a keyring plugin for master encryption key management.

All MySQL editions provide a keyring\_file plugin, which stores keyring data in a file local to the server host.

MySQL Enterprise Edition offers additional keyring plugins:

- keyring\_encrypted\_file: Stores keyring data in an encrypted, password-protected file local to the server host.
- keyring\_okv: A KMIP 1.1 plugin for use with KMIP-compatible back end keyring storage products. Supported KMIP-compatible products include centralized key management solutions such as Oracle Key Vault, Gemalto KeySecure, Thales Vormetric key management server, and Fornetix Key Orchestration.
- keyring\_aws: Communicates with the Amazon Web Services Key Management Service (AWS KMS) as a back end for key generation and uses a local file for key storage.

![](_page_174_Picture_23.jpeg)

#### **Warning**

For encryption key management, the keyring\_file and keyring\_encrypted\_file plugins are not intended as a regulatory compliance solution. Security standards such as PCI, FIPS, and others require use of key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs).

A secure and robust encryption key management solution is critical for security and for compliance with various security standards. When the data-at-rest encryption feature uses a centralized key management solution, the feature is referred to as "MySQL Enterprise Transparent Data Encryption (TDE)".

The data-at-rest encryption feature supports the Advanced Encryption Standard (AES) block-based encryption algorithm. It uses Electronic Codebook (ECB) block encryption mode for tablespace key encryption and Cipher Block Chaining (CBC) block encryption mode for data encryption.

For frequently asked questions about the data-at-rest encryption feature, see Section A.17, "MySQL 5.7 FAQ: InnoDB Data-at-Rest Encryption".

# <span id="page-175-0"></span>**Encryption Prerequisites**

• A keyring plugin must be installed and configured. Keyring plugin installation is performed at startup using the early-plugin-load option. Early loading ensures that the plugin is available prior to initialization of the InnoDB storage engine. For keyring plugin installation and configuration instructions, see Section 6.4.4, "The MySQL Keyring".

Only one keyring plugin should be enabled at a time. Enabling multiple keyring plugins is unsupported and results may not be as anticipated.

![](_page_175_Picture_8.jpeg)

#### **Important**

Once encrypted tablespaces are created in a MySQL instance, the keyring plugin that was loaded when creating the encrypted tablespace must continue to be loaded at startup using the early-plugin-load option. Failing to do so results in errors when starting the server and during InnoDB recovery.

To verify that a keyring plugin is active, use the SHOW PLUGINS statement or query the Information Schema PLUGINS table. For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE 'keyring%';
+--------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------+---------------+
| keyring_file | ACTIVE |
+--------------+---------------+
```

• When encrypting production data, ensure that you take steps to prevent loss of the master encryption key. If the master encryption key is lost, data stored in encrypted tablespace files is unrecoverable. If you use the keyring\_file or keyring\_encrypted\_file plugin, create a backup of the keyring data file immediately after creating the first encrypted tablespace, before master key rotation, and after master key rotation. The keyring\_file\_data configuration option defines the keyring data file location for the keyring\_file plugin. The keyring\_encrypted\_file\_data configuration option defines the keyring data file location for the keyring\_encrypted\_file plugin. If you use the keyring\_okv or keyring\_aws plugin, ensure that you have performed the necessary configuration. For instructions, see Section 6.4.4, "The MySQL Keyring".

# <span id="page-175-1"></span>**Enabling File-Per-Table Tablespace Encryption**

To enable encryption for a new file-per-table tablespace, specify the ENCRYPTION option in a CREATE TABLE statement. The following example assumes that innodb\_file\_per\_table is enabled.

```
mysql> CREATE TABLE t1 (c1 INT) ENCRYPTION='Y';
```

To enable encryption for an existing file-per-table tablespace, specify the ENCRYPTION option in an ALTER TABLE statement.

```
mysql> ALTER TABLE t1 ENCRYPTION='Y';
```

To disable encryption for file-per-table tablespace, set ENCRYPTION='N' using ALTER TABLE.

```
mysql> ALTER TABLE t1 ENCRYPTION='N';
```

# <span id="page-176-0"></span>**Master Key Rotation**

The master encryption key should be rotated periodically and whenever you suspect that the key has been compromised.

Master key rotation is an atomic, instance-level operation. Each time the master encryption key is rotated, all tablespace keys in the MySQL instance are re-encrypted and saved back to their respective tablespace headers. As an atomic operation, re-encryption must succeed for all tablespace keys once a rotation operation is initiated. If master key rotation is interrupted by a server failure, InnoDB rolls the operation forward on server restart. For more information, see [Encryption and Recovery.](#page-176-1)

Rotating the master encryption key only changes the master encryption key and re-encrypts tablespace keys. It does not decrypt or re-encrypt associated tablespace data.

Rotating the master encryption key requires the SUPER privilege.

To rotate the master encryption key, run:

```
mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

ALTER INSTANCE ROTATE INNODB MASTER KEY supports concurrent DML. However, it cannot be run concurrently with tablespace encryption operations, and locks are taken to prevent conflicts that could arise from concurrent execution. If an ALTER INSTANCE ROTATE INNODB MASTER KEY operation is running, it must finish before a tablespace encryption operation can proceed, and vice versa.

# <span id="page-176-1"></span>**Encryption and Recovery**

If a server failure occurs during an encryption operation, the operation is rolled forward when the server is restarted.

If a server failure occurs during master key rotation, InnoDB continues the operation on server restart.

The keyring plugin must be loaded prior to storage engine initialization so that the information necessary to decrypt tablespace data pages can be retrieved from tablespace headers before InnoDB initialization and recovery activities access tablespace data. (See [Encryption Prerequisites](#page-175-0).)

When InnoDB initialization and recovery begin, the master key rotation operation resumes. Due to the server failure, some tablespace keys may already be encrypted using the new master encryption key. InnoDB reads the encryption data from each tablespace header, and if the data indicates that the tablespace key is encrypted using the old master encryption key, InnoDB retrieves the old key from the keyring and uses it to decrypt the tablespace key. InnoDB then re-encrypts the tablespace key using the new master encryption key and saves the re-encrypted tablespace key back to the tablespace header.

# <span id="page-176-2"></span>**Exporting Encrypted Tablespaces**

When an encrypted tablespace is exported, InnoDB generates a transfer key that is used to encrypt the tablespace key. The encrypted tablespace key and transfer key are stored in a tablespace\_name.cfp file. This file together with the encrypted tablespace file is required to perform an import operation. On import, InnoDB uses the transfer key to decrypt the tablespace key in the tablespace\_name.cfp file. For related information, see [Section 14.6.1.3, "Importing InnoDB](#page-22-3) [Tables"](#page-22-3).

# <span id="page-177-0"></span>**Encryption and Replication**

- The ALTER INSTANCE ROTATE INNODB MASTER KEY statement is only supported in replication environments where the source and replicas run a version of MySQL that supports at-rest data encryption.
- Successful ALTER INSTANCE ROTATE INNODB MASTER KEY statements are written to the binary log for replication on replicas.
- If an ALTER INSTANCE ROTATE INNODB MASTER KEY statement fails, it is not logged to the binary log and is not replicated on replicas.
- Replication of an ALTER INSTANCE ROTATE INNODB MASTER KEY operation fails if the keyring plugin is installed on the source but not on the replica.
- If the keyring\_file or keyring\_encrypted\_file plugin is installed on both the source and a replica but the replica does not have a keyring data file, the replicated ALTER INSTANCE ROTATE INNODB MASTER KEY statement creates the keyring data file on the replica, assuming the keyring file data is not cached in memory. ALTER INSTANCE ROTATE INNODB MASTER KEY uses keyring file data that is cached in memory, if available.

# <span id="page-177-1"></span>**Identifying Encrypted Tablespaces**

When the ENCRYPTION option is specified in a CREATE TABLE or ALTER TABLE statement, it is recorded in the CREATE\_OPTIONS column of the Information Schema TABLES table. This column can be queried to identify tables that reside in encrypted file-per-table tablespaces.

```
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES
 WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';
+--------------+------------+----------------+
| TABLE_SCHEMA | TABLE_NAME | CREATE_OPTIONS |
+--------------+------------+----------------+
| test | t1 | ENCRYPTION="Y" |
+--------------+------------+----------------+
```

Query INFORMATION\_SCHEMA.INNODB\_SYS\_TABLESPACES to retrieve information about the tablespace associated with a particular schema and table.

```
mysql> SELECT SPACE, NAME, SPACE_TYPE FROM INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES WHERE NAME='test/t1';
+-------+---------+------------+
| SPACE | NAME | SPACE_TYPE |
+-------+---------+------------+
| 3 | test/t1 | Single |
+-------+---------+------------+
```

# <span id="page-177-2"></span>**Encryption Usage Notes**

- Plan appropriately when altering an existing tablespace with the ENCRYPTION option. The table is rebuilt using the COPY algorithm. The INPLACE algorithm is not supported.
- If the server exits or is stopped during normal operation, it is recommended to restart the server using the same encryption settings that were configured previously.
- The first master encryption key is generated when the first new or existing tablespace is encrypted.
- Master key rotation re-encrypts tablespaces keys but does not change the tablespace key itself. To change a tablespace key, you must disable and re-enable encryption, which is an ALGORITHM=COPY operation that rebuilds the table.
- If a table is created with both the COMPRESSION and ENCRYPTION options, compression is performed before tablespace data is encrypted.

- If a keyring data file (the file named by keyring\_file\_data or keyring\_encrypted\_file\_data) is empty or missing, the first execution of ALTER INSTANCE ROTATE INNODB MASTER KEY creates a master encryption key.
- Uninstalling the keyring\_file or keyring\_encrypted\_file plugin does not remove an existing keyring data file.
- It is recommended that you not place a keyring data file under the same directory as tablespace data files.
- Modifying the keyring\_file\_data or keyring\_encrypted\_file\_data setting at runtime or when restarting the server can cause previously encrypted tablespaces to become inaccessible, resulting in lost data.

# <span id="page-178-1"></span>**Encryption Limitations**

- Advanced Encryption Standard (AES) is the only supported encryption algorithm. InnoDB dataat-rest encryption uses Electronic Codebook (ECB) block encryption mode for tablespace key encryption and Cipher Block Chaining (CBC) block encryption mode for data encryption. Padding is not used with CBC block encryption mode. Instead, InnoDB ensures that the text to be encrypted is a multiple of the block size.
- Altering the ENCRYPTION attribute of a table is performed using the COPY algorithm. The INPLACE algorithm is not supported.
- Encryption is only supported for file-per-table tablespaces. Encryption is not supported for other tablespace types including general tablespaces and the system tablespace.
- You cannot move or copy a table from an encrypted file-per-table tablespace to a tablespace type that does not support encryption.
- Encryption only applies to data in the tablespace. Data is not encrypted in the redo log, undo log, or binary log.
- It is not permitted to change the storage engine of a table that resides in, or previously resided in, an encrypted tablespace.
- Encryption is not supported for the InnoDB FULLTEXT index tables that are created implicitly when adding a FULLTEXT index. For related information, see [InnoDB Full-Text Index Tables](#page-44-1).

# <span id="page-178-0"></span>**14.15 InnoDB Startup Options and System Variables**

- System variables that are true or false can be enabled at server startup by naming them, or disabled by using a --skip- prefix. For example, to enable or disable the InnoDB adaptive hash index, you can use [--innodb-adaptive-hash-index](#page-188-0) or [--skip-innodb](#page-188-0)[adaptive-hash-index](#page-188-0) on the command line, or [innodb\\_adaptive\\_hash\\_index](#page-188-0) or skip\_innodb\_adaptive\_hash\_index in an option file.
- System variables that take a numeric value can be specified as --var\_name=value on the command line or as var\_name=value in option files.
- Many system variables can be changed at runtime (see Section 5.1.8.2, "Dynamic System Variables").
- For information about GLOBAL and SESSION variable scope modifiers, refer to the SET statement documentation.
- Certain options control the locations and layout of the InnoDB data files. [Section 14.8.1, "InnoDB](#page-84-1) [Startup Configuration"](#page-84-1) explains how to use these options.
- Some options, which you might not use initially, help tune InnoDB performance characteristics based on machine capacity and your database workload.

• For more information on specifying options and system variables, see Section 4.2.2, "Specifying Program Options".

**Table 14.18 InnoDB Option and Variable Reference**

| Name                      | Cmd-Line                                   | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|--------------------------------------------|-------------|------------|------------|-----------|---------|
|                           | daemon_memcached_enable_binlog<br>Yes      | Yes         | Yes        |            | Global    | No      |
|                           | daemon_memcached_engine_lib_name<br>Yes    | Yes         | Yes        |            | Global    | No      |
|                           | daemon_memcached_engine_lib_path<br>Yes    | Yes         | Yes        |            | Global    | No      |
|                           | daemon_memcached_option<br>Yes             | Yes         | Yes        |            | Global    | No      |
|                           | daemon_memcached_r_batch_size<br>Yes       | Yes         | Yes        |            | Global    | No      |
|                           | daemon_memcached_w_batch_size<br>Yes       | Yes         | Yes        |            | Global    | No      |
| foreign_key_checks        |                                            |             | Yes        |            | Both      | Yes     |
| ignore_builtin_innodb Yes |                                            | Yes         | Yes        |            | Global    | No      |
| innodb                    | Yes                                        | Yes         |            |            |           |         |
| innodb_adaptive_flushing  | Yes                                        | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_adaptive_flushing_lwm<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_adaptive_hash_index<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_adaptive_hash_index_parts<br>Yes    | Yes         | Yes        |            | Global    | No      |
|                           | innodb_adaptive_max_sleep_delay<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_api_bk_commit_interval<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_api_disable_rowlock<br>Yes          | Yes         | Yes        |            | Global    | No      |
|                           | innodb_api_enable_binlog<br>Yes            | Yes         | Yes        |            | Global    | No      |
| innodb_api_enable_mdl Yes |                                            | Yes         | Yes        |            | Global    | No      |
| innodb_api_trx_level Yes  |                                            | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_autoextend_increment<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_autoinc_lock_mode<br>Yes            | Yes         | Yes        |            | Global    | No      |
|                           | Innodb_available_undo_logs                 |             |            | Yes        | Global    | No      |
|                           | innodb_background_drop_list_empty<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                           | Innodb_buffer_pool_bytes_data              |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_bytes_dirty             |             |            | Yes        | Global    | No      |
|                           | innodb_buffer_pool_chunk_size<br>Yes       | Yes         | Yes        |            | Global    | No      |
|                           | innodb_buffer_pool_dump_at_shutdown<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_dump_now<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_dump_pct<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | Innodb_buffer_pool_dump_status             |             |            | Yes        | Global    | No      |
|                           | innodb_buffer_pool_filename<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_instances<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                           | innodb_buffer_pool_load_abort<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_load_at_startup<br>Yes  | Yes         | Yes        |            | Global    | No      |
|                           | innodb_buffer_pool_load_now<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | Innodb_buffer_pool_load_status             |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_pages_data              |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_pages_dirty             |             |            | Yes        | Global    | No      |

| Name                       | Cmd-Line                                        | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|-------------------------------------------------|-------------|------------|------------|-----------|---------|
|                            | Innodb_buffer_pool_pages_flushed                |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_pages_free                   |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_pages_latched                |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_pages_misc                   |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_pages_total                  |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_ahead                   |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_ahead_evicted           |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_ahead_rnd               |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_requests                |             |            | Yes        | Global    | No      |
| Innodb_buffer_pool_reads   |                                                 |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_resize_status                |             |            | Yes        | Global    | No      |
| innodb_buffer_pool_size    | Yes                                             | Yes         | Yes        |            | Global    | Varies  |
|                            | Innodb_buffer_pool_wait_free                    |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_write_requests               |             |            | Yes        | Global    | No      |
|                            | innodb_change_buffer_max_size<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
| innodb_change_buffering    | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_change_buffering_debug<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_checksum_algorithm<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
| innodb_checksums Yes       |                                                 | Yes         | Yes        |            | Global    | No      |
|                            | innodb_cmp_per_index_enabled<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_commit_concurrency<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
| innodb_compress_debug      | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_compression_failure_threshold_pct<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_compression_level   | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_compression_pad_pct_max<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| innodb_concurrency_tickets | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_data_file_path Yes  |                                                 | Yes         | Yes        |            | Global    | No      |
| Innodb_data_fsyncs         |                                                 |             |            | Yes        | Global    | No      |
| innodb_data_home_dir Yes   |                                                 | Yes         | Yes        |            | Global    | No      |
|                            | Innodb_data_pending_fsyncs                      |             |            | Yes        | Global    | No      |
|                            | Innodb_data_pending_reads                       |             |            | Yes        | Global    | No      |
|                            | Innodb_data_pending_writes                      |             |            | Yes        | Global    | No      |
| Innodb_data_read           |                                                 |             |            | Yes        | Global    | No      |
| Innodb_data_reads          |                                                 |             |            | Yes        | Global    | No      |
| Innodb_data_writes         |                                                 |             |            | Yes        | Global    | No      |
| Innodb_data_written        |                                                 |             |            | Yes        | Global    | No      |
|                            | Innodb_dblwr_pages_written                      |             |            | Yes        | Global    | No      |
| Innodb_dblwr_writes        |                                                 |             |            | Yes        | Global    | No      |
| innodb_deadlock_detect     | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_default_row_format  | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_disable_resize_buffer_pool_debug<br>Yes  | Yes         | Yes        |            | Global    | Yes     |

| Name                       | Cmd-Line                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|---------------------------------------------|-------------|------------|------------|-----------|---------|
|                            | innodb_disable_sort_file_cache<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
| innodb_doublewrite Yes     |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_fast_shutdown Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_fil_make_page_dirty_debug<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| innodb_file_format Yes     |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_file_format_check   | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_file_format_max Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_file_per_table Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_fill_factor Yes     |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_flush_log_at_timeout<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_flush_log_at_trx_commit<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
| innodb_flush_method Yes    |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_flush_neighbors Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_flush_sync Yes      |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_flushing_avg_loops  | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_force_load_corrupted<br>Yes          | Yes         | Yes        |            | Global    | No      |
| innodb_force_recovery Yes  |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_ft_aux_table        |                                             |             | Yes        |            | Global    | Yes     |
| innodb_ft_cache_size Yes   |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_ft_enable_diag_print<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_ft_enable_stopword<br>Yes            | Yes         | Yes        |            | Both      | Yes     |
| innodb_ft_max_token_size   | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_ft_min_token_size   | Yes                                         | Yes         | Yes        |            | Global    | No      |
|                            | innodb_ft_num_word_optimize<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_ft_result_cache_limit<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_ft_server_stopword_table<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
| innodb_ft_sort_pll_degree  | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_ft_total_cache_size | Yes                                         | Yes         | Yes        |            | Global    | No      |
|                            | innodb_ft_user_stopword_table<br>Yes        | Yes         | Yes        |            | Both      | Yes     |
|                            | Innodb_have_atomic_builtins                 |             |            | Yes        | Global    | No      |
| innodb_io_capacity Yes     |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_io_capacity_max     | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
| innodb_large_prefix Ys     |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_limit_optimistic_insert_debug<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_lock_wait_timeout   | Yes                                         | Yes         | Yes        |            | Both      | Yes     |
|                            | innodb_locks_unsafe_for_binlog<br>Yes       | Yes         | Yes        |            | Global    | No      |
| innodb_log_buffer_size Yes |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_log_checkpoint_now<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
| innodb_log_checksums Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_log_compressed_pages<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_log_file_size Yes   |                                             | Yes         | Yes        |            | Global    | No      |

| Name                       | Cmd-Line                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|---------------------------------------------|-------------|------------|------------|-----------|---------|
| innodb_log_files_in_group  | Yes                                         | Yes         | Yes        |            | Global    | No      |
|                            | innodb_log_group_home_dir<br>Yes            | Yes         | Yes        |            | Global    | No      |
| Innodb_log_waits           |                                             |             |            | Yes        | Global    | No      |
|                            | innodb_log_write_ahead_size<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                            | Innodb_log_write_requests                   |             |            | Yes        | Global    | No      |
| Innodb_log_writes          |                                             |             |            | Yes        | Global    | No      |
| innodb_lru_scan_depth Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_dirty_pages_pct<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_dirty_pages_pct_lwm<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
| innodb_max_purge_lag Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_purge_lag_delay<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_undo_log_size<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_merge_threshold_set_all_debug<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_disable Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_enable Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_reset Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_reset_all   | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
| Innodb_num_open_files      |                                             |             |            | Yes        | Global    | No      |
| innodb_numa_interleave     | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_old_blocks_pct Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_old_blocks_time Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_online_alter_log_max_size<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| innodb_open_files Yes      |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_optimize_fulltext_only<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
| Innodb_os_log_fsyncs       |                                             |             |            | Yes        | Global    | No      |
|                            | Innodb_os_log_pending_fsyncs                |             |            | Yes        | Global    | No      |
|                            | Innodb_os_log_pending_writes                |             |            | Yes        | Global    | No      |
| Innodb_os_log_written      |                                             |             |            | Yes        | Global    | No      |
| innodb_page_cleaners Yes   |                                             | Yes         | Yes        |            | Global    | No      |
| Innodb_page_size           |                                             |             |            | Yes        | Global    | No      |
| innodb_page_size Yes       |                                             | Yes         | Yes        |            | Global    | No      |
| Innodb_pages_created       |                                             |             |            | Yes        | Global    | No      |
| Innodb_pages_read          |                                             |             |            | Yes        | Global    | No      |
| Innodb_pages_written       |                                             |             |            | Yes        | Global    | No      |
|                            | innodb_print_all_deadlocks<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| innodb_purge_batch_size    | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_purge_rseg_truncate_frequency<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_purge_threads Yes   |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_random_read_ahead<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_read_ahead_threshold<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_read_io_threads     | Yes                                         | Yes         | Yes        |            | Global    | No      |

| Name                        | Cmd-Line                                       | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|------------------------------------------------|-------------|------------|------------|-----------|---------|
| innodb_read_only Yes        |                                                | Yes         | Yes        |            | Global    | No      |
| innodb_replication_delay    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_rollback_on_timeout<br>Yes              | Yes         | Yes        |            | Global    | No      |
| innodb_rollback_segments    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
|                             | Innodb_row_lock_current_waits                  |             |            | Yes        | Global    | No      |
| Innodb_row_lock_time        |                                                |             |            | Yes        | Global    | No      |
| Innodb_row_lock_time_avg    |                                                |             |            | Yes        | Global    | No      |
|                             | Innodb_row_lock_time_max                       |             |            | Yes        | Global    | No      |
| Innodb_row_lock_waits       |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_deleted         |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_inserted        |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_read            |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_updated         |                                                |             |            | Yes        | Global    | No      |
|                             | innodb_saved_page_number_debug<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_sort_buffer_size Yes |                                                | Yes         | Yes        |            | Global    | No      |
| innodb_spin_wait_delay Yes  |                                                | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_auto_recalc    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_include_delete_marked<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_method Yes     |                                                | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_on_metadata    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_persistent Yes |                                                | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_persistent_sample_pages<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_sample_pages<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_transient_sample_pages<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| innodb<br>status-file       | Yes                                            | Yes         |            |            |           |         |
| innodb_status_output Yes    |                                                | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_status_output_locks<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
| innodb_strict_mode Yes      |                                                | Yes         | Yes        |            | Both      | Yes     |
| innodb_support_xa Yes       |                                                | Yes         | Yes        |            | Both      | Yes     |
| innodb_sync_array_size      | Yes                                            | Yes         | Yes        |            | Global    | No      |
| innodb_sync_debug Yes       |                                                | Yes         | Yes        |            | Global    | No      |
| innodb_sync_spin_loops      | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| innodb_table_locks Yes      |                                                | Yes         | Yes        |            | Both      | Yes     |
|                             | innodb_temp_data_file_path<br>Yes              | Yes         | Yes        |            | Global    | No      |
|                             | innodb_thread_concurrency<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
| innodb_thread_sleep_delay   | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| innodb_tmpdir Yes           |                                                | Yes         | Yes        |            | Both      | Yes     |
|                             | Innodb_truncated_status_writes                 |             |            | Yes        | Global    | No      |
|                             | innodb_trx_purge_view_update_only_debug<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_trx_rseg_n_slots_debug<br>Yes           | Yes         | Yes        |            | Global    | Yes     |

| Name                      | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|----------|-------------|------------|------------|-----------|---------|
| innodb_undo_directory Yes |          | Yes         | Yes        |            | Global    | No      |
| innodb_undo_log_truncate  | Yes      | Yes         | Yes        |            | Global    | Yes     |
| innodb_undo_logs Yes      |          | Yes         | Yes        |            | Global    | Yes     |
| innodb_undo_tablespaces   | Yes      | Yes         | Yes        |            | Global    | No      |
| innodb_use_native_aio Yes |          | Yes         | Yes        |            | Global    | No      |
| innodb_version            |          |             | Yes        |            | Global    | No      |
| innodb_write_io_threads   | Yes      | Yes         | Yes        |            | Global    | No      |
| unique_checks             |          |             | Yes        |            | Both      | Yes     |

# <span id="page-184-0"></span>**InnoDB Command Options**

• [--innodb\[=](#page-184-0)value]

| Command-Line Format | innodb[=value] |
|---------------------|----------------|
| Deprecated          | Yes            |
| Type                | Enumeration    |
| Default Value       | ON             |
| Valid Values        | OFF            |
|                     | ON             |
|                     | FORCE          |

Controls loading of the InnoDB storage engine, if the server was compiled with InnoDB support. This option has a tristate format, with possible values of OFF, ON, or FORCE. See Section 5.5.1, "Installing and Uninstalling Plugins".

To disable InnoDB, use [--innodb=OFF](#page-184-0) or [--skip-innodb](#page-184-0). In this case, because the default storage engine is [InnoDB](#page-0-0), the server does not start unless you also use --default-storageengine and --default-tmp-storage-engine to set the default to some other engine for both permanent and TEMPORARY tables.

The InnoDB storage engine can no longer be disabled, and the [--innodb=OFF](#page-184-0) and [--skip](#page-184-0)[innodb](#page-184-0) options are deprecated and have no effect. Their use results in a warning. You should expect these options to be removed in a future MySQL release.

<span id="page-184-1"></span>• [--innodb-status-file](#page-184-1)

| Command-Line Format | innodb-status-file[={OFF ON}] |
|---------------------|-------------------------------|
| Type                | Boolean                       |
| Default Value       | OFF                           |

The --innodb-status-file startup option controls whether InnoDB creates a file named innodb\_status.pid in the data directory and writes SHOW ENGINE INNODB STATUS output to it every 15 seconds, approximately.

The innodb\_status.pid file is not created by default. To create it, start mysqld with the - innodb-status-file option. InnoDB removes the file when the server is shut down normally. If an abnormal shutdown occurs, the status file may have to be removed manually.

The --innodb-status-file option is intended for temporary use, as SHOW ENGINE INNODB STATUS output generation can affect performance, and the innodb\_status.pid file can become quite large over time.

For related information, see Section 14.18.2, "Enabling InnoDB Monitors".

• [--skip-innodb](#page-184-0)

Disable the InnoDB storage engine. See the description of [--innodb](#page-184-0).

# <span id="page-185-0"></span>**InnoDB System Variables**

• [daemon\\_memcached\\_enable\\_binlog](#page-185-0)

| Command-Line Format | daemon-memcached-enable<br>binlog[={OFF ON}] |
|---------------------|----------------------------------------------|
| System Variable     | daemon_memcached_enable_binlog               |
| Scope               | Global                                       |
| Dynamic             | No                                           |
| Type                | Boolean                                      |
| Default Value       | OFF                                          |

Enable this option on the source server to use the InnoDB memcached plugin (daemon\_memcached) with the MySQL binary log. This option can only be set at server startup. You must also enable the MySQL binary log on the source server using the --log-bin option.

For more information, see Section 14.21.6, "The InnoDB memcached Plugin and Replication".

<span id="page-185-1"></span>• [daemon\\_memcached\\_engine\\_lib\\_name](#page-185-1)

| Command-Line Format | daemon-memcached-engine-lib<br>name=file_name |
|---------------------|-----------------------------------------------|
| System Variable     | daemon_memcached_engine_lib_name              |
| Scope               | Global                                        |
| Dynamic             | No                                            |
| Type                | File name                                     |
| Default Value       | innodb_engine.so                              |

Specifies the shared library that implements the InnoDB memcached plugin.

For more information, see Section 14.21.3, "Setting Up the InnoDB memcached Plugin".

<span id="page-185-2"></span>• [daemon\\_memcached\\_engine\\_lib\\_path](#page-185-2)

| Command-Line Format | daemon-memcached-engine-lib<br>path=dir_name |
|---------------------|----------------------------------------------|
| System Variable     | daemon_memcached_engine_lib_path             |
| Scope               | Global                                       |
| Dynamic             | No                                           |
| Type                | Directory name                               |
| Default Value       | NULL                                         |

The path of the directory containing the shared library that implements the InnoDB memcached plugin. The default value is NULL, representing the MySQL plugin directory. You should not need to modify this parameter unless specifying a memcached plugin for a different storage engine that is located outside of the MySQL plugin directory.

For more information, see Section 14.21.3, "Setting Up the InnoDB memcached Plugin".

<span id="page-186-0"></span>• [daemon\\_memcached\\_option](#page-186-0)

| Command-Line Format | daemon-memcached-option=options |
|---------------------|---------------------------------|
| System Variable     | daemon_memcached_option         |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | String                          |
| Default Value       |                                 |

Used to pass space-separated memcached options to the underlying memcached memory object caching daemon on startup. For example, you might change the port that memcached listens on, reduce the maximum number of simultaneous connections, change the maximum memory size for a key-value pair, or enable debugging messages for the error log.

See Section 14.21.3, "Setting Up the InnoDB memcached Plugin" for usage details. For information about memcached options, refer to the memcached man page.

<span id="page-186-1"></span>• [daemon\\_memcached\\_r\\_batch\\_size](#page-186-1)

| Command-Line Format | daemon-memcached-r-batch-size=# |
|---------------------|---------------------------------|
| System Variable     | daemon_memcached_r_batch_size   |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | Integer                         |
| Default Value       | 1                               |
| Minimum Value       | 1                               |
| Maximum Value       | 1073741824                      |

Specifies how many memcached read operations (get operations) to perform before doing a COMMIT to start a new transaction. Counterpart of [daemon\\_memcached\\_w\\_batch\\_size](#page-186-2).

This value is set to 1 by default, so that any changes made to the table through SQL statements are immediately visible to memcached operations. You might increase it to reduce the overhead from frequent commits on a system where the underlying table is only being accessed through the memcached interface. If you set the value too large, the amount of undo or redo data could impose some storage overhead, as with any long-running transaction.

For more information, see Section 14.21.3, "Setting Up the InnoDB memcached Plugin".

<span id="page-186-2"></span>• [daemon\\_memcached\\_w\\_batch\\_size](#page-186-2)

| Command-Line Format | daemon-memcached-w-batch-size=# |
|---------------------|---------------------------------|
| System Variable     | daemon_memcached_w_batch_size   |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | Integer                         |
| Default Value       | 1                               |
| Minimum Value       | 1                               |
| Maximum Value       | 1048576                         |

Specifies how many memcached write operations, such as add, set, and incr, to perform before doing a COMMIT to start a new transaction. Counterpart of [daemon\\_memcached\\_r\\_batch\\_size](#page-186-1).

This value is set to 1 by default, on the assumption that data being stored is important to preserve in case of an outage and should immediately be committed. When storing non-critical data, you might increase this value to reduce the overhead from frequent commits; but then the last N-1 uncommitted write operations could be lost if an unexpected exit occurs.

For more information, see Section 14.21.3, "Setting Up the InnoDB memcached Plugin".

#### <span id="page-187-2"></span>• ignore\_builtin\_innodb

| Command-Line Format | ignore-builtin-innodb[={OFF ON}] |
|---------------------|----------------------------------|
| Deprecated          | Yes                              |
| System Variable     | ignore_builtin_innodb            |
| Scope               | Global                           |
| Dynamic             | No                               |
| Type                | Boolean                          |

In earlier versions of MySQL, enabling this variable caused the server to behave as if the built-in InnoDB were not present, which enabled the InnoDB Plugin to be used instead. In MySQL 5.7, InnoDB is the default storage engine and InnoDB Plugin is not used, so this variable is ignored.

#### <span id="page-187-1"></span>• [innodb\\_adaptive\\_flushing](#page-187-1)

| Command-Line Format | innodb-adaptive-flushing[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_adaptive_flushing                |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | Boolean                                 |
| Default Value       | ON                                      |

Specifies whether to dynamically adjust the rate of flushing dirty pages in the InnoDB buffer pool based on the workload. Adjusting the flush rate dynamically is intended to avoid bursts of I/O activity. This setting is enabled by default. See [Section 14.8.3.5, "Configuring Buffer Pool Flushing"](#page-98-0) for more information. For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

#### <span id="page-187-0"></span>• [innodb\\_adaptive\\_flushing\\_lwm](#page-187-0)

| Command-Line Format | innodb-adaptive-flushing-lwm=# |
|---------------------|--------------------------------|
| System Variable     | innodb_adaptive_flushing_lwm   |
| Scope               | Global                         |
| Dynamic             | Yes                            |
| Type                | Integer                        |
| Default Value       | 10                             |
| Minimum Value       | 0                              |
| Maximum Value       | 70                             |

Defines the low water mark representing percentage of redo log capacity at which adaptive flushing is enabled. For more information, see [Section 14.8.3.5, "Configuring Buffer Pool Flushing".](#page-98-0)

<span id="page-188-0"></span>• [innodb\\_adaptive\\_hash\\_index](#page-188-0)

| Command-Line Format | innodb-adaptive-hash-index[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | innodb_adaptive_hash_index                |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Boolean                                   |
| Default Value       | ON                                        |

Whether the InnoDB adaptive hash index is enabled or disabled. It may be desirable, depending on your workload, to dynamically enable or disable adaptive hash indexing to improve query performance. Because the adaptive hash index may not be useful for all workloads, conduct benchmarks with it both enabled and disabled, using realistic workloads. See [Section 14.5.3,](#page-17-0) ["Adaptive Hash Index"](#page-17-0) for details.

This variable is enabled by default. You can modify this parameter using the SET GLOBAL statement, without restarting the server. Changing the setting at runtime requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges". You can also use --skip-innodb-adaptive-hash-index at server startup to disable it.

Disabling the adaptive hash index empties the hash table immediately. Normal operations can continue while the hash table is emptied, and executing queries that were using the hash table access the index B-trees directly instead. When the adaptive hash index is re-enabled, the hash table is populated again during normal operation.

<span id="page-188-1"></span>• [innodb\\_adaptive\\_hash\\_index\\_parts](#page-188-1)

| Command-Line Format | innodb-adaptive-hash-index-parts=# |
|---------------------|------------------------------------|
| System Variable     | innodb_adaptive_hash_index_parts   |
| Scope               | Global                             |
| Dynamic             | No                                 |
| Type                | Numeric                            |
| Default Value       | 8                                  |
| Minimum Value       | 1                                  |
| Maximum Value       | 512                                |

Partitions the adaptive hash index search system. Each index is bound to a specific partition, with each partition protected by a separate latch.

In earlier releases, the adaptive hash index search system was protected by a single latch (btr\_search\_latch) which could become a point of contention. With the introduction of the [innodb\\_adaptive\\_hash\\_index\\_parts](#page-188-1) option, the search system is partitioned into 8 parts by default. The maximum setting is 512.

For related information, see [Section 14.5.3, "Adaptive Hash Index"](#page-17-0).

<span id="page-188-2"></span>• [innodb\\_adaptive\\_max\\_sleep\\_delay](#page-188-2)

| Command-Line Format | innodb-adaptive-max-sleep-delay=# |
|---------------------|-----------------------------------|
| System Variable     | innodb_adaptive_max_sleep_delay   |
| Scope               | Global                            |
| Dynamic             | 2561<br>Yes                       |

| Type          | Integer      |
|---------------|--------------|
| Default Value | 150000       |
| Minimum Value | 0            |
| Maximum Value | 1000000      |
| Unit          | microseconds |

Permits InnoDB to automatically adjust the value of innodb\_thread\_sleep\_delay up or down according to the current workload. Any nonzero value enables automated, dynamic adjustment of the innodb\_thread\_sleep\_delay value, up to the maximum value specified in the [innodb\\_adaptive\\_max\\_sleep\\_delay](#page-188-2) option. The value represents the number of microseconds. This option can be useful in busy systems, with greater than 16 InnoDB threads. (In practice, it is most valuable for MySQL systems with hundreds or thousands of simultaneous connections.)

For more information, see [Section 14.8.5, "Configuring Thread Concurrency for InnoDB"](#page-104-0).

<span id="page-189-0"></span>• [innodb\\_api\\_bk\\_commit\\_interval](#page-189-0)

| Command-Line Format | innodb-api-bk-commit-interval=# |
|---------------------|---------------------------------|
| System Variable     | innodb_api_bk_commit_interval   |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Integer                         |
| Default Value       | 5                               |
| Minimum Value       | 1                               |
| Maximum Value       | 1073741824                      |
| Unit                | seconds                         |

How often to auto-commit idle connections that use the InnoDB memcached interface, in seconds. For more information, see Section 14.21.5.4, "Controlling Transactional Behavior of the InnoDB memcached Plugin".

<span id="page-189-1"></span>• [innodb\\_api\\_disable\\_rowlock](#page-189-1)

| Command-Line Format | innodb-api-disable-rowlock[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | innodb_api_disable_rowlock                |
| Scope               | Global                                    |
| Dynamic             | No                                        |
| Type                | Boolean                                   |
| Default Value       | OFF                                       |

Use this option to disable row locks when InnoDB memcached performs DML operations. By default, [innodb\\_api\\_disable\\_rowlock](#page-189-1) is disabled, which means that memcached requests row locks for get and set operations. When [innodb\\_api\\_disable\\_rowlock](#page-189-1) is enabled, memcached requests a table lock instead of row locks.

[innodb\\_api\\_disable\\_rowlock](#page-189-1) is not dynamic. It must be specified on the mysqld command line or entered in the MySQL configuration file. Configuration takes effect when the plugin is installed, which occurs when the MySQL server is started.

For more information, see Section 14.21.5.4, "Controlling Transactional Behavior of the InnoDB memcached Plugin".

<span id="page-190-0"></span>• [innodb\\_api\\_enable\\_binlog](#page-190-0)

| Command-Line Format | innodb-api-enable-binlog[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_api_enable_binlog                |
| Scope               | Global                                  |
| Dynamic             | No                                      |
| Type                | Boolean                                 |
| Default Value       | OFF                                     |

Lets you use the InnoDB memcached plugin with the MySQL binary log. For more information, see Enabling the InnoDB memcached Binary Log.

<span id="page-190-1"></span>• [innodb\\_api\\_enable\\_mdl](#page-190-1)

| Command-Line Format | innodb-api-enable-mdl[={OFF ON}] |
|---------------------|----------------------------------|
| System Variable     | innodb_api_enable_mdl            |
| Scope               | Global                           |
| Dynamic             | No                               |
| Type                | Boolean                          |
| Default Value       | OFF                              |

Locks the table used by the InnoDB memcached plugin, so that it cannot be dropped or altered by DDL through the SQL interface. For more information, see Section 14.21.5.4, "Controlling Transactional Behavior of the InnoDB memcached Plugin".

<span id="page-190-2"></span>• [innodb\\_api\\_trx\\_level](#page-190-2)

| Command-Line Format | innodb-api-trx-level=# |
|---------------------|------------------------|
| System Variable     | innodb_api_trx_level   |
| Scope               | Global                 |
| Dynamic             | Yes                    |
| Type                | Integer                |
| Default Value       | 0                      |
| Minimum Value       | 0                      |
| Maximum Value       | 3                      |

Controls the transaction isolation level on queries processed by the memcached interface. The constants corresponding to the familiar names are:

- 0 = [READ UNCOMMITTED](#page-73-2)
- 1 = [READ COMMITTED](#page-71-0)
- 2 = [REPEATABLE READ](#page-70-3)
- 3 = [SERIALIZABLE](#page-73-1)

For more information, see Section 14.21.5.4, "Controlling Transactional Behavior of the InnoDB memcached Plugin".

<span id="page-191-1"></span>• [innodb\\_autoextend\\_increment](#page-191-1)

| Command-Line Format | innodb-autoextend-increment=# |
|---------------------|-------------------------------|
| System Variable     | innodb_autoextend_increment   |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | Integer                       |
| Default Value       | 64                            |
| Minimum Value       | 1                             |
| Maximum Value       | 1000                          |
| Unit                | megabytes                     |

The increment size (in megabytes) for extending the size of an auto-extending InnoDB system tablespace file when it becomes full. The default value is 64. For related information, see [System](#page-86-0) [Tablespace Data File Configuration,](#page-86-0) and [Resizing the System Tablespace](#page-48-2).

The [innodb\\_autoextend\\_increment](#page-191-1) setting does not affect file-per-table tablespace files or general tablespace files. These files are auto-extending regardless of the [innodb\\_autoextend\\_increment](#page-191-1) setting. The initial extensions are by small amounts, after which extensions occur in increments of 4MB.

<span id="page-191-0"></span>• [innodb\\_autoinc\\_lock\\_mode](#page-191-0)

| Command-Line Format | innodb-autoinc-lock-mode=# |
|---------------------|----------------------------|
| System Variable     | innodb_autoinc_lock_mode   |
| Scope               | Global                     |
| Dynamic             | No                         |
| Type                | Integer                    |
| Default Value       | 1                          |
| Valid Values        | 0                          |
|                     | 1                          |
|                     | 2                          |

The lock mode to use for generating auto-increment values. Permissible values are 0, 1, or 2, for traditional, consecutive, or interleaved, respectively. The default setting is 1 (consecutive). For the characteristics of each lock mode, see [InnoDB AUTO\\_INCREMENT Lock Modes.](#page-35-2)

<span id="page-191-2"></span>• [innodb\\_background\\_drop\\_list\\_empty](#page-191-2)

| Command-Line Format | innodb-background-drop-list<br>empty[={OFF ON}] |
|---------------------|-------------------------------------------------|
| System Variable     | innodb_background_drop_list_empty               |
| Scope               | Global                                          |
| Dynamic             | Yes                                             |
| Type                | Boolean                                         |
| Default Value       | OFF                                             |

Enabling the [innodb\\_background\\_drop\\_list\\_empty](#page-191-2) debug option helps avoid test case failures by delaying table creation until the background drop list is empty. For example, if test case A <sup>2564</sup> places table t1 on the background drop list, test case B waits until the background drop list is empty before creating table t1.

<span id="page-192-0"></span>• [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0)

| Command-Line Format | innodb-buffer-pool-chunk-size=#                           |
|---------------------|-----------------------------------------------------------|
| System Variable     | innodb_buffer_pool_chunk_size                             |
| Scope               | Global                                                    |
| Dynamic             | No                                                        |
| Type                | Integer                                                   |
| Default Value       | 134217728                                                 |
| Minimum Value       | 1048576                                                   |
| Maximum Value       | innodb_buffer_pool_size /<br>innodb_buffer_pool_instances |
| Unit                | bytes                                                     |

[innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) defines the chunk size for InnoDB buffer pool resizing operations.

To avoid copying all buffer pool pages during resizing operations, the operation is performed in "chunks". By default, [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) is 128MB (134217728 bytes). The number of pages contained in a chunk depends on the value of innodb\_page\_size. [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) can be increased or decreased in units of 1MB (1048576 bytes).

The following conditions apply when altering the [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) value:

- If [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0) is larger than the current buffer pool size when the buffer pool is initialized, [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) is truncated to [innodb\\_buffer\\_pool\\_size](#page-196-0) / [innodb\\_buffer\\_pool\\_instances](#page-194-0).
- Buffer pool size must always be equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). If you alter [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0), [innodb\\_buffer\\_pool\\_size](#page-196-0) is automatically rounded to a value that is equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). The adjustment occurs when the buffer pool is initialized.

![](_page_192_Picture_9.jpeg)

#### **Important**

Care should be taken when changing [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0), as changing this value can automatically increase the size of the buffer pool. Before changing [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0), calculate the effect it has on [innodb\\_buffer\\_pool\\_size](#page-196-0) to ensure that the resulting buffer pool size is acceptable.

To avoid potential performance issues, the number of chunks ([innodb\\_buffer\\_pool\\_size](#page-196-0) / [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0)) should not exceed 1000.

The [innodb\\_buffer\\_pool\\_size](#page-196-0) variable is dynamic, which permits resizing the buffer pool while the server is online. However, the buffer pool size must be equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0), and changing either of those variable settings requires restarting the server.

See [Section 14.8.3.1, "Configuring InnoDB Buffer Pool Size"](#page-91-1) for more information.

<span id="page-192-1"></span>• [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1)

| Command-Line Format | innodb-buffer-pool-dump-at<br>shutdown[={OFF ON}] |
|---------------------|---------------------------------------------------|
| System Variable     | innodb_buffer_pool_dump_at_shutdown               |
| Scope               | Global                                            |
| Dynamic             | Yes                                               |
| Type                | Boolean                                           |
| Default Value       | ON                                                |

Specifies whether to record the pages cached in the InnoDB buffer pool when the MySQL server is shut down, to shorten the warmup process at the next restart. Typically used in combination with [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0). The [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) option defines the percentage of most recently used buffer pool pages to dump.

Both [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1) and [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0) are enabled by default.

For more information, see [Section 14.8.3.6, "Saving and Restoring the Buffer Pool State"](#page-100-0).

<span id="page-193-1"></span>• [innodb\\_buffer\\_pool\\_dump\\_now](#page-193-1)

| Command-Line Format | innodb-buffer-pool-dump-now[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | innodb_buffer_pool_dump_now                |
| Scope               | Global                                     |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | OFF                                        |

Immediately makes a record of pages cached in the InnoDB buffer pool. Typically used in combination with [innodb\\_buffer\\_pool\\_load\\_now](#page-196-1).

Enabling [innodb\\_buffer\\_pool\\_dump\\_now](#page-193-1) triggers the recording action but does not alter the variable setting, which always remains OFF or 0. To view buffer pool dump status after triggering a dump, query the Innodb\_buffer\_pool\_dump\_status variable.

For more information, see [Section 14.8.3.6, "Saving and Restoring the Buffer Pool State"](#page-100-0).

<span id="page-193-0"></span>• [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0)

| Command-Line Format | innodb-buffer-pool-dump-pct=# |
|---------------------|-------------------------------|
| System Variable     | innodb_buffer_pool_dump_pct   |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | Integer                       |
| Default Value       | 25                            |
| Minimum Value       | 1                             |
| Maximum Value       | 100                           |

Specifies the percentage of the most recently used pages for each buffer pool to read out and dump. The range is 1 to 100. The default value is 25. For example, if there are 4 buffer pools with 100

pages each, and [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) is set to 25, the 25 most recently used pages from each buffer pool are dumped.

The change to the [innodb\\_buffer\\_pool\\_dump\\_pct](#page-193-0) default value coincides with default value changes for [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1) and [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0), which are both enabled by default in MySQL 5.7.

<span id="page-194-1"></span>• [innodb\\_buffer\\_pool\\_filename](#page-194-1)

| Command-Line Format | innodb-buffer-pool<br>filename=file_name |
|---------------------|------------------------------------------|
| System Variable     | innodb_buffer_pool_filename              |
| Scope               | Global                                   |
| Dynamic             | Yes                                      |
| Type                | File name                                |
| Default Value       | ib_buffer_pool                           |

Specifies the name of the file that holds the list of tablespace IDs and page IDs produced by [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1) or [innodb\\_buffer\\_pool\\_dump\\_now](#page-193-1). Tablespace IDs and page IDs are saved in the following format: space, page\_id. By default, the file is named ib\_buffer\_pool and is located in the InnoDB data directory. A non-default location must be specified relative to the data directory.

A file name can be specified at runtime, using a SET statement:

```
SET GLOBAL innodb_buffer_pool_filename='file_name';
```

You can also specify a file name at startup, in a startup string or MySQL configuration file. When specifying a file name at startup, the file must exist or InnoDB returns a startup error indicating that there is no such file or directory.

For more information, see [Section 14.8.3.6, "Saving and Restoring the Buffer Pool State"](#page-100-0).

<span id="page-194-0"></span>• [innodb\\_buffer\\_pool\\_instances](#page-194-0)

| Command-Line Format                       | innodb-buffer-pool-instances=#               |
|-------------------------------------------|----------------------------------------------|
| System Variable                           | innodb_buffer_pool_instances                 |
| Scope                                     | Global                                       |
| Dynamic                                   | No                                           |
| Type                                      | Integer                                      |
| Default Value (Windows, 32-bit platforms) | see description                              |
| Default Value (Other)                     | 8 (or 1 if innodb_buffer_pool_size <<br>1GB) |
| Minimum Value                             | 1                                            |
| Maximum Value                             | 64                                           |

The number of regions that the InnoDB buffer pool is divided into. For systems with buffer pools in the multi-gigabyte range, dividing the buffer pool into separate instances can improve concurrency, by reducing contention as different threads read and write to cached pages. Each page that is stored in or read from the buffer pool is assigned to one of the buffer pool instances randomly, using a hashing function. Each buffer pool instance manages its own free lists, flush lists, LRUs, and all other data structures connected to a buffer pool, and is protected by its own buffer pool mutex.

This option only takes effect when setting [innodb\\_buffer\\_pool\\_size](#page-196-0) to 1GB or more. The total buffer pool size is divided among all the buffer pools. For best efficiency, specify a combination of

[innodb\\_buffer\\_pool\\_instances](#page-194-0) and [innodb\\_buffer\\_pool\\_size](#page-196-0) so that each buffer pool instance is at least 1GB.

The default value on 32-bit Windows systems depends on the value of [innodb\\_buffer\\_pool\\_size](#page-196-0), as described below:

- If [innodb\\_buffer\\_pool\\_size](#page-196-0) is greater than 1.3GB, the default for [innodb\\_buffer\\_pool\\_instances](#page-194-0) is [innodb\\_buffer\\_pool\\_size](#page-196-0)/128MB, with individual memory allocation requests for each chunk. 1.3GB was chosen as the boundary at which there is significant risk for 32-bit Windows to be unable to allocate the contiguous address space needed for a single buffer pool.
- Otherwise, the default is 1.

On all other platforms, the default value is 8 when [innodb\\_buffer\\_pool\\_size](#page-196-0) is greater than or equal to 1GB. Otherwise, the default is 1.

For related information, see [Section 14.8.3.1, "Configuring InnoDB Buffer Pool Size"](#page-91-1).

<span id="page-195-1"></span>• [innodb\\_buffer\\_pool\\_load\\_abort](#page-195-1)

| Command-Line Format | innodb-buffer-pool-load<br>abort[={OFF ON}] |
|---------------------|---------------------------------------------|
| System Variable     | innodb_buffer_pool_load_abort               |
| Scope               | Global                                      |
| Dynamic             | Yes                                         |
| Type                | Boolean                                     |
| Default Value       | OFF                                         |

Interrupts the process of restoring InnoDB buffer pool contents triggered by [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0) or [innodb\\_buffer\\_pool\\_load\\_now](#page-196-1).

Enabling [innodb\\_buffer\\_pool\\_load\\_abort](#page-195-1) triggers the abort action but does not alter the variable setting, which always remains OFF or 0. To view buffer pool load status after triggering an abort action, query the Innodb\_buffer\_pool\_load\_status variable.

For more information, see [Section 14.8.3.6, "Saving and Restoring the Buffer Pool State"](#page-100-0).

<span id="page-195-0"></span>• [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0)

| Command-Line Format | innodb-buffer-pool-load-at<br>startup[={OFF ON}] |
|---------------------|--------------------------------------------------|
| System Variable     | innodb_buffer_pool_load_at_startup               |
| Scope               | Global                                           |
| Dynamic             | No                                               |
| Type                | Boolean                                          |
| Default Value       | ON                                               |

Specifies that, on MySQL server startup, the InnoDB buffer pool is automatically warmed up by loading the same pages it held at an earlier time. Typically used in combination with [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1).

Both [innodb\\_buffer\\_pool\\_dump\\_at\\_shutdown](#page-192-1) and [innodb\\_buffer\\_pool\\_load\\_at\\_startup](#page-195-0) are enabled by default. <span id="page-196-1"></span>• innodb buffer pool load now

| Command-Line Format | innodb-buffer-pool-load-now[={OFF  ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_buffer_pool_load_now             |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Туре                | Boolean                                 |
| Default Value       | OFF                                     |

Immediately warms up the InnoDB buffer pool by loading data pages without waiting for a server restart. Can be useful to bring cache memory back to a known state during benchmarking or to ready the MySQL server to resume its normal workload after running queries for reports or maintenance.

Enabling innodb\_buffer\_pool\_load\_now triggers the load action but does not alter the variable setting, which always remains OFF or 0. To view buffer pool load progress after triggering a load, query the Innodb buffer pool load status variable.

For more information, see Section 14.8.3.6, "Saving and Restoring the Buffer Pool State".

<span id="page-196-0"></span>• innodb buffer pool size

| Command-Line Format              | innodb-buffer-pool-size=# |
|----------------------------------|---------------------------|
| System Variable                  | innodb_buffer_pool_size   |
| Scope                            | Global                    |
| Dynamic                          | Yes                       |
| Туре                             | Integer                   |
| Default Value                    | 134217728                 |
| Minimum Value                    | 5242880                   |
| Maximum Value (64-bit platforms) | 2**64-1                   |
| Maximum Value (32-bit platforms) | 2**32-1                   |
| Unit                             | bytes                     |

The size in bytes of the buffer pool, the memory area where <code>InnoDB</code> caches table and index data. The default value is 134217728 bytes (128MB). The maximum value depends on the CPU architecture; the maximum is 4294967295 (2<sup>32</sup>-1) on 32-bit systems and 18446744073709551615 (2<sup>64</sup>-1) on 64-bit systems. On 32-bit systems, the CPU architecture and operating system may impose a lower practical maximum size than the stated maximum. When the size of the buffer pool is greater than 1GB, setting <code>innodb\_buffer\_pool\_instances</code> to a value greater than 1 can improve the scalability on a busy server.

A larger buffer pool requires less disk I/O to access the same table data more than once. On a dedicated database server, you might set the buffer pool size to 80% of the machine's physical memory size. Be aware of the following potential issues when configuring buffer pool size, and be prepared to scale back the size of the buffer pool if necessary.

- · Competition for physical memory can cause paging in the operating system.
- InnoDB reserves additional memory for buffers and control structures, so that the total allocated space is approximately 10% greater than the specified buffer pool size.
- Address space for the buffer pool must be contiguous, which can be an issue on Windows systems with DLLs that load at specific addresses.

• The time to initialize the buffer pool is roughly proportional to its size. On instances with large buffer pools, initialization time might be significant. To reduce the initialization period, you can save the buffer pool state at server shutdown and restore it at server startup. See [Section 14.8.3.6,](#page-100-0) ["Saving and Restoring the Buffer Pool State"](#page-100-0).

When you increase or decrease buffer pool size, the operation is performed in chunks. Chunk size is defined by the [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) variable, which has a default of 128 MB.

Buffer pool size must always be equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0). If you alter the buffer pool size to a value that is not equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0), buffer pool size is automatically adjusted to a value that is equal to or a multiple of [innodb\\_buffer\\_pool\\_chunk\\_size](#page-192-0) \* [innodb\\_buffer\\_pool\\_instances](#page-194-0).

[innodb\\_buffer\\_pool\\_size](#page-196-0) can be set dynamically, which allows you to resize the buffer pool without restarting the server. The Innodb\_buffer\_pool\_resize\_status status variable reports the status of online buffer pool resizing operations. See [Section 14.8.3.1, "Configuring InnoDB Buffer](#page-91-1) [Pool Size"](#page-91-1) for more information.

<span id="page-197-1"></span>• [innodb\\_change\\_buffer\\_max\\_size](#page-197-1)

| Command-Line Format | innodb-change-buffer-max-size=# |
|---------------------|---------------------------------|
| System Variable     | innodb_change_buffer_max_size   |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Integer                         |
| Default Value       | 25                              |
| Minimum Value       | 0                               |
| Maximum Value       | 50                              |

Maximum size for the InnoDB change buffer, as a percentage of the total size of the buffer pool. You might increase this value for a MySQL server with heavy insert, update, and delete activity, or decrease it for a MySQL server with unchanging data used for reporting. For more information, see [Section 14.5.2, "Change Buffer".](#page-14-0) For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-197-0"></span>• [innodb\\_change\\_buffering](#page-197-0)

| Command-Line Format | innodb-change-buffering=value |
|---------------------|-------------------------------|
| System Variable     | innodb_change_buffering       |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | Enumeration                   |
| Default Value       | all                           |
| Valid Values        | none                          |
|                     | inserts                       |
|                     | deletes                       |
|                     | changes                       |
|                     | purges                        |

all

Whether InnoDB performs change buffering, an optimization that delays write operations to secondary indexes so that the I/O operations can be performed sequentially. Permitted values are described in the following table.

**Table 14.19 Permitted Values for innodb\_change\_buffering**

| Value   | Description                                                                                                                                |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------|
| none    | Do not buffer any operations.                                                                                                              |
| inserts | Buffer insert operations.                                                                                                                  |
| deletes | Buffer delete marking operations; strictly<br>speaking, the writes that mark index records for<br>later deletion during a purge operation. |
| changes | Buffer inserts and delete-marking operations.                                                                                              |
| purges  | Buffer the physical deletion operations that<br>happen in the background.                                                                  |
| all     | The default. Buffer inserts, delete-marking<br>operations, and purges.                                                                     |

For more information, see [Section 14.5.2, "Change Buffer".](#page-14-0) For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-198-1"></span>• [innodb\\_change\\_buffering\\_debug](#page-198-1)

| Command-Line Format | innodb-change-buffering-debug=# |
|---------------------|---------------------------------|
| System Variable     | innodb_change_buffering_debug   |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Integer                         |
| Default Value       | 0                               |
| Minimum Value       | 0                               |
| Maximum Value       | 2                               |

Sets a debug flag for InnoDB change buffering. A value of 1 forces all changes to the change buffer. A value of 2 causes an unexpected exit at merge. A default value of 0 indicates that the change buffering debug flag is not set. This option is only available when debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-198-0"></span>• [innodb\\_checksum\\_algorithm](#page-198-0)

| Command-Line Format | innodb-checksum-algorithm=value |
|---------------------|---------------------------------|
| System Variable     | innodb_checksum_algorithm       |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Enumeration                     |
| Default Value       | crc32                           |
| Valid Values        | crc32                           |
|                     | strict_crc32                    |

| innodb        |
|---------------|
| strict_innodb |
| none          |
| strict_none   |

Specifies how to generate and verify the checksum stored in the disk blocks of InnoDB tablespaces. crc32 is the default value as of MySQL 5.7.7.

[innodb\\_checksum\\_algorithm](#page-198-0) replaces the innodb\_checksums option. The following values were provided for compatibility, up to and including MySQL 5.7.6:

- innodb\_checksums=ON is the same as [innodb\\_checksum\\_algorithm=innodb](#page-198-0).
- innodb\_checksums=OFF is the same as [innodb\\_checksum\\_algorithm=none](#page-198-0).

As of MySQL 5.7.7, with a default [innodb\\_checksum\\_algorithm](#page-198-0) value of crc32, innodb\_checksums=ON is now the same as [innodb\\_checksum\\_algorithm=crc32](#page-198-0). innodb\_checksums=OFF is still the same as [innodb\\_checksum\\_algorithm=none](#page-198-0).

To avoid conflicts, remove references to innodb\_checksums from MySQL configuration files and startup scripts.

The value innodb is backward-compatible with earlier versions of MySQL. The value crc32 uses an algorithm that is faster to compute the checksum for every modified block, and to check the checksums for each disk read. It scans blocks 64 bits at a time, which is faster than the innodb checksum algorithm, which scans blocks 8 bits at a time. The value none writes a constant value in the checksum field rather than computing a value based on the block data. The blocks in a tablespace can use a mix of old, new, and no checksum values, being updated gradually as the data is modified; once blocks in a tablespace are modified to use the crc32 algorithm, the associated tables cannot be read by earlier versions of MySQL.

The strict form of a checksum algorithm reports an error if it encounters a valid but non-matching checksum value in a tablespace. It is recommended that you only use strict settings in a new instance, to set up tablespaces for the first time. Strict settings are somewhat faster, because they do not need to compute all checksum values during disk reads.

![](_page_199_Picture_10.jpeg)

#### **Note**

Prior to MySQL 5.7.8, a strict mode setting for [innodb\\_checksum\\_algorithm](#page-198-0) caused InnoDB to halt when encountering a valid but non-matching checksum. In MySQL 5.7.8 and later, only an error message is printed, and the page is accepted as valid if it has a valid innodb, crc32 or none checksum.

The following table shows the difference between the none, innodb, and crc32 option values, and their strict counterparts. none, innodb, and crc32 write the specified type of checksum value into each data block, but for compatibility accept other checksum values when verifying a block during a read operation. Strict settings also accept valid checksum values but print an error message when a valid non-matching checksum value is encountered. Using the strict form

can make verification faster if all InnoDB data files in an instance are created under an identical innodb\_checksum\_algorithm value.

**Table 14.20 Permitted innodb\_checksum\_algorithm Values**

| Value         | Generated checksum (when<br>writing)                                                         | Permitted checksums (when<br>reading)                                                                                                                        |
|---------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| none          | A constant number.                                                                           | Any of the checksums<br>generated by none, innodb, or<br>crc32.                                                                                              |
| innodb        | A checksum calculated in<br>software, using the original<br>algorithm from InnoDB.           | Any of the checksums<br>generated by none, innodb, or<br>crc32.                                                                                              |
| crc32         | A checksum calculated using<br>the crc32 algorithm, possibly<br>done with a hardware assist. | Any of the checksums<br>generated by none, innodb, or<br>crc32.                                                                                              |
| strict_none   | A constant number                                                                            | Any of the checksums<br>generated by none, innodb,<br>or crc32. InnoDB prints an<br>error message if a valid but<br>non-matching checksum is<br>encountered. |
| strict_innodb | A checksum calculated in<br>software, using the original<br>algorithm from InnoDB.           | Any of the checksums<br>generated by none, innodb,<br>or crc32. InnoDB prints an<br>error message if a valid but<br>non-matching checksum is<br>encountered. |
| strict_crc32  | A checksum calculated using<br>the crc32 algorithm, possibly<br>done with a hardware assist. | Any of the checksums<br>generated by none, innodb,<br>or crc32. InnoDB prints an<br>error message if a valid but<br>non-matching checksum is<br>encountered. |

Versions of MySQL Enterprise Backup up to 3.8.0 do not support backing up tablespaces that use CRC32 checksums. MySQL Enterprise Backup adds CRC32 checksum support in 3.8.1, with some limitations. Refer to the MySQL Enterprise Backup 3.8.1 Change History for more information.

### <span id="page-0-0"></span>• [innodb\\_checksums](#page-0-0)

| Command-Line Format | innodb-checksums[={OFF ON}] |
|---------------------|-----------------------------|
| Deprecated          | Yes                         |
| System Variable     | innodb_checksums            |
| Scope               | Global                      |
| Dynamic             | No                          |
| Type                | Boolean                     |
| Default Value       | ON                          |

InnoDB can use checksum validation on all tablespace pages read from disk to ensure extra fault tolerance against hardware faults or corrupted data files. This validation is enabled by default. Under specialized circumstances (such as when running benchmarks) this safety feature can be disabled

with --skip-innodb-checksums. You can specify the method of calculating the checksum using the innodb\_checksum\_algorithm option.

[innodb\\_checksums](#page-0-0) is deprecated, replaced by innodb\_checksum\_algorithm.

Prior to MySQL 5.7.7, [innodb\\_checksums=ON](#page-0-0) is the same as innodb\_checksum\_algorithm=innodb. As of MySQL 5.7.7, the innodb\_checksum\_algorithm default value is crc32, and [innodb\\_checksums=ON](#page-0-0) is the same as innodb\_checksum\_algorithm=crc32. [innodb\\_checksums=OFF](#page-0-0) is the same as innodb\_checksum\_algorithm=none.

Remove any [innodb\\_checksums](#page-0-0) options from your configuration files and startup scripts to avoid conflicts with innodb\_checksum\_algorithm. [innodb\\_checksums=OFF](#page-0-0) automatically sets innodb\_checksum\_algorithm=none. [innodb\\_checksums=ON](#page-0-0) is ignored and overridden by any other setting for innodb\_checksum\_algorithm.

<span id="page-1-0"></span>• [innodb\\_cmp\\_per\\_index\\_enabled](#page-1-0)

| Command-Line Format | innodb-cmp-per-index<br>enabled[={OFF ON}] |
|---------------------|--------------------------------------------|
| System Variable     | innodb_cmp_per_index_enabled               |
| Scope               | Global                                     |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | OFF                                        |

Enables per-index compression-related statistics in the Information Schema INNODB\_CMP\_PER\_INDEX table. Because these statistics can be expensive to gather, only enable this option on development, test, or replica instances during performance tuning related to InnoDB compressed tables.

For more information, see Section 24.4.7, "The INFORMATION\_SCHEMA INNODB\_CMP\_PER\_INDEX and INNODB\_CMP\_PER\_INDEX\_RESET Tables", and Section 14.9.1.4, "Monitoring InnoDB Table Compression at Runtime".

<span id="page-1-1"></span>• [innodb\\_commit\\_concurrency](#page-1-1)

| Command-Line Format | innodb-commit-concurrency=# |
|---------------------|-----------------------------|
| System Variable     | innodb_commit_concurrency   |
| Scope               | Global                      |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 0                           |
| Minimum Value       | 0                           |
| Maximum Value       | 1000                        |

The number of threads that can commit at the same time. A value of 0 (the default) permits any number of transactions to commit simultaneously.

The value of [innodb\\_commit\\_concurrency](#page-1-1) cannot be changed at runtime from zero to nonzero or vice versa. The value can be changed from one nonzero value to another.

<span id="page-1-2"></span>• [innodb\\_compress\\_debug](#page-1-2)

| Command-Line Format | innodb-compress-debug=value |
|---------------------|-----------------------------|
|---------------------|-----------------------------|

| System Variable | innodb_compress_debug |
|-----------------|-----------------------|
| Scope           | Global                |
| Dynamic         | Yes                   |
| Type            | Enumeration           |
| Default Value   | none                  |
| Valid Values    | none                  |
|                 | zlib                  |
|                 | lz4                   |
|                 | lz4hc                 |

Compresses all tables using a specified compression algorithm without having to define a COMPRESSION attribute for each table. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

For related information, see Section 14.9.2, "InnoDB Page Compression".

<span id="page-2-0"></span>• [innodb\\_compression\\_failure\\_threshold\\_pct](#page-2-0)

| Command-Line Format | innodb-compression-failure<br>threshold-pct=# |
|---------------------|-----------------------------------------------|
| System Variable     | innodb_compression_failure_threshold_pct      |
| Scope               | Global                                        |
| Dynamic             | Yes                                           |
| Type                | Integer                                       |
| Default Value       | 5                                             |
| Minimum Value       | 0                                             |
| Maximum Value       | 100                                           |

Defines the compression failure rate threshold for a table, as a percentage, at which point MySQL begins adding padding within compressed pages to avoid expensive compression failures. When this threshold is passed, MySQL begins to leave additional free space within each new compressed page, dynamically adjusting the amount of free space up to the percentage of page size specified by [innodb\\_compression\\_pad\\_pct\\_max](#page-3-0). A value of zero disables the mechanism that monitors compression efficiency and dynamically adjusts the padding amount.

For more information, see Section 14.9.1.6, "Compression for OLTP Workloads".

<span id="page-2-1"></span>• [innodb\\_compression\\_level](#page-2-1)

| Command-Line Format | innodb-compression-level=# |
|---------------------|----------------------------|
| System Variable     | innodb_compression_level   |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 6                          |
| Minimum Value       | 0                          |

| Maximum Value | 9 |
|---------------|---|
|---------------|---|

Specifies the level of zlib compression to use for InnoDB compressed tables and indexes. A higher value lets you fit more data onto a storage device, at the expense of more CPU overhead during compression. A lower value lets you reduce CPU overhead when storage space is not critical, or you expect the data is not especially compressible.

For more information, see Section 14.9.1.6, "Compression for OLTP Workloads".

<span id="page-3-0"></span>• [innodb\\_compression\\_pad\\_pct\\_max](#page-3-0)

| Command-Line Format | innodb-compression-pad-pct-max=# |
|---------------------|----------------------------------|
| System Variable     | innodb_compression_pad_pct_max   |
| Scope               | Global                           |
| Dynamic             | Yes                              |
| Type                | Integer                          |
| Default Value       | 50                               |
| Minimum Value       | 0                                |
| Maximum Value       | 75                               |

Specifies the maximum percentage that can be reserved as free space within each compressed page, allowing room to reorganize the data and modification log within the page when a compressed table or index is updated and the data might be recompressed. Only applies when [innodb\\_compression\\_failure\\_threshold\\_pct](#page-2-0) is set to a nonzero value, and the rate of compression failures passes the cutoff point.

For more information, see Section 14.9.1.6, "Compression for OLTP Workloads".

<span id="page-3-1"></span>• [innodb\\_concurrency\\_tickets](#page-3-1)

| Command-Line Format | innodb-concurrency-tickets=# |
|---------------------|------------------------------|
| System Variable     | innodb_concurrency_tickets   |
| Scope               | Global                       |
| Dynamic             | Yes                          |
| Type                | Integer                      |
| Default Value       | 5000                         |
| Minimum Value       | 1                            |
| Maximum Value       | 4294967295                   |

Determines the number of threads that can enter InnoDB concurrently. A thread is placed in a queue when it tries to enter InnoDB if the number of threads has already reached the concurrency limit. When a thread is permitted to enter InnoDB, it is given a number of " tickets" equal to the value of [innodb\\_concurrency\\_tickets](#page-3-1), and the thread can enter and leave InnoDB freely until it has used up its tickets. After that point, the thread again becomes subject to the concurrency check (and possible queuing) the next time it tries to enter InnoDB. The default value is 5000.

With a small [innodb\\_concurrency\\_tickets](#page-3-1) value, small transactions that only need to process a few rows compete fairly with larger transactions that process many rows. The disadvantage of a small [innodb\\_concurrency\\_tickets](#page-3-1) value is that large transactions must loop through the

queue many times before they can complete, which extends the amount of time required to complete their task.

With a large [innodb\\_concurrency\\_tickets](#page-3-1) value, large transactions spend less time waiting for a position at the end of the queue (controlled by [innodb\\_thread\\_concurrency](#page-50-0)) and more time retrieving rows. Large transactions also require fewer trips through the queue to complete their task. The disadvantage of a large [innodb\\_concurrency\\_tickets](#page-3-1) value is that too many large transactions running at the same time can starve smaller transactions by making them wait a longer time before executing.

With a nonzero [innodb\\_thread\\_concurrency](#page-50-0) value, you may need to adjust the [innodb\\_concurrency\\_tickets](#page-3-1) value up or down to find the optimal balance between larger and smaller transactions. The SHOW ENGINE INNODB STATUS report shows the number of tickets remaining for an executing transaction in its current pass through the queue. This data may also be obtained from the TRX\_CONCURRENCY\_TICKETS column of the Information Schema INNODB\_TRX table.

For more information, see Section 14.8.5, "Configuring Thread Concurrency for InnoDB".

<span id="page-4-0"></span>• [innodb\\_data\\_file\\_path](#page-4-0)

| Command-Line Format | innodb-data-file-path=file_name |
|---------------------|---------------------------------|
| System Variable     | innodb_data_file_path           |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | String                          |
| Default Value       | ibdata1:12M:autoextend          |

Defines the name, size, and attributes of InnoDB system tablespace data files.. If you do not specify a value for [innodb\\_data\\_file\\_path](#page-4-0), the default behavior is to create a single auto-extending data file, slightly larger than 12MB, named ibdata1.

The full syntax for a data file specification includes the file name, file size, autoextend attribute, and max attribute:

```
file_name:file_size[:autoextend[:max:max_file_size]]
```

File sizes are specified in kilobytes, megabytes, or gigabytes by appending K, M or G to the size value. If specifying the data file size in kilobytes, do so in multiples of 1024. Otherwise, KB values are rounded to nearest megabyte (MB) boundary. The sum of file sizes must be, at a minimum, slightly larger than 12MB.

For additional configuration information, see System Tablespace Data File Configuration. For resizing instructions, see Resizing the System Tablespace.

<span id="page-4-1"></span>• [innodb\\_data\\_home\\_dir](#page-4-1)

| Command-Line Format | innodb-data-home-dir=dir_name |
|---------------------|-------------------------------|
| System Variable     | innodb_data_home_dir          |
| Scope               | Global                        |
| Dynamic             | No                            |
| Type                | Directory name                |

The common part of the directory path for InnoDB system tablespace data files. The default value is the MySQL data directory. The setting is concatenated with the [innodb\\_data\\_file\\_path](#page-4-0)

setting. If you specify the value as an empty string, you can specify an absolute path for [innodb\\_data\\_file\\_path](#page-4-0).

A trailing slash is required when specifying a value for [innodb\\_data\\_home\\_dir](#page-4-1). For example:

```
[mysqld]
innodb_data_home_dir = /path/to/myibdata/
```

This setting does not affect the location of file-per-table tablespaces.

For related information, see Section 14.8.1, "InnoDB Startup Configuration".

<span id="page-5-0"></span>• [innodb\\_deadlock\\_detect](#page-5-0)

| Command-Line Format | innodb-deadlock-detect[={OFF ON}] |
|---------------------|-----------------------------------|
| System Variable     | innodb_deadlock_detect            |
| Scope               | Global                            |
| Dynamic             | Yes                               |
| Type                | Boolean                           |
| Default Value       | ON                                |

This option is used to disable deadlock detection. On high concurrency systems, deadlock detection can cause a slowdown when numerous threads wait for the same lock. At times, it may be more efficient to disable deadlock detection and rely on the [innodb\\_lock\\_wait\\_timeout](#page-22-0) setting for transaction rollback when a deadlock occurs.

For related information, see Section 14.7.5.2, "Deadlock Detection".

<span id="page-5-1"></span>• [innodb\\_default\\_row\\_format](#page-5-1)

| Command-Line Format | innodb-default-row-format=value |
|---------------------|---------------------------------|
| System Variable     | innodb_default_row_format       |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Enumeration                     |
| Default Value       | DYNAMIC                         |
| Valid Values        | REDUNDANT                       |
|                     | COMPACT                         |
|                     | DYNAMIC                         |

The [innodb\\_default\\_row\\_format](#page-5-1) option defines the default row format for InnoDB tables and user-created temporary tables. The default setting is DYNAMIC. Other permitted values are COMPACT and REDUNDANT. The COMPRESSED row format, which is not supported for use in the system tablespace, cannot be defined as the default.

Newly created tables use the row format defined by [innodb\\_default\\_row\\_format](#page-5-1) when a ROW\_FORMAT option is not specified explicitly or when ROW\_FORMAT=DEFAULT is used.

When a ROW\_FORMAT option is not specified explicitly or when ROW\_FORMAT=DEFAULT is used, any operation that rebuilds a table also silently changes the row format of the table to the format defined by [innodb\\_default\\_row\\_format](#page-5-1). For more information, see Defining the Row Format of a Table.

Internal InnoDB temporary tables created by the server to process queries use the DYNAMIC row 2578 format, regardless of the [innodb\\_default\\_row\\_format](#page-5-1) setting.

<span id="page-6-0"></span>• [innodb\\_disable\\_sort\\_file\\_cache](#page-6-0)

| Command-Line Format | innodb-disable-sort-file<br>cache[={OFF ON}] |
|---------------------|----------------------------------------------|
| System Variable     | innodb_disable_sort_file_cache               |
| Scope               | Global                                       |
| Dynamic             | Yes                                          |
| Type                | Boolean                                      |
| Default Value       | OFF                                          |

Disables the operating system file system cache for merge-sort temporary files. The effect is to open such files with the equivalent of O\_DIRECT.

<span id="page-6-1"></span>• [innodb\\_disable\\_resize\\_buffer\\_pool\\_debug](#page-6-1)

| Command-Line Format | innodb-disable-resize-buffer-pool<br>debug[={OFF ON}] |
|---------------------|-------------------------------------------------------|
| System Variable     | innodb_disable_resize_buffer_pool_debug               |
| Scope               | Global                                                |
| Dynamic             | Yes                                                   |
| Type                | Boolean                                               |
| Default Value       | ON                                                    |

Disables resizing of the InnoDB buffer pool. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-6-2"></span>• [innodb\\_doublewrite](#page-6-2)

| Command-Line Format | innodb-doublewrite[={OFF ON}] |
|---------------------|-------------------------------|
| System Variable     | innodb_doublewrite            |
| Scope               | Global                        |
| Dynamic             | No                            |
| Type                | Boolean                       |
| Default Value       | ON                            |

When enabled (the default), InnoDB stores all data twice, first to the doublewrite buffer, then to the actual data files. This variable can be turned off with --skip-innodb-doublewrite for benchmarks or cases when top performance is needed rather than concern for data integrity or possible failures.

If system tablespace data files (ibdata\* files) are located on Fusion-io devices that support atomic writes, doublewrite buffering is automatically disabled and Fusion-io atomic writes are used for all data files. Because the doublewrite buffer setting is global, doublewrite buffering is also disabled for data files residing on non-Fusion-io hardware. This feature is only supported on Fusion-io hardware and only enabled for Fusion-io NVMFS on Linux. To take full advantage of this feature, an [innodb\\_flush\\_method](#page-12-0) setting of O\_DIRECT is recommended.

For related information, see Section 14.6.5, "Doublewrite Buffer".

<span id="page-6-3"></span>• [innodb\\_fast\\_shutdown](#page-6-3)

| Command-Line Format | innodb-fast-shutdown=# |
|---------------------|------------------------|
| System Variable     | innodb_fast_shutdown   |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | Yes     |
| Type          | Integer |
| Default Value | 1       |
| Valid Values  | 0       |
|               | 1       |
|               | 2       |

The InnoDB shutdown mode. If the value is 0, InnoDB does a slow shutdown, a full purge and a change buffer merge before shutting down. If the value is 1 (the default), InnoDB skips these operations at shutdown, a process known as a fast shutdown. If the value is 2, InnoDB flushes its logs and shuts down cold, as if MySQL had crashed; no committed transactions are lost, but the crash recovery operation makes the next startup take longer.

The slow shutdown can take minutes, or even hours in extreme cases where substantial amounts of data are still buffered. Use the slow shutdown technique before upgrading or downgrading between MySQL major releases, so that all data files are fully prepared in case the upgrade process updates the file format.

Use [innodb\\_fast\\_shutdown=2](#page-6-3) in emergency or troubleshooting situations, to get the absolute fastest shutdown if data is at risk of corruption.

<span id="page-7-0"></span>• [innodb\\_fil\\_make\\_page\\_dirty\\_debug](#page-7-0)

| Command-Line Format | innodb-fil-make-page-dirty-debug=# |
|---------------------|------------------------------------|
| System Variable     | innodb_fil_make_page_dirty_debug   |
| Scope               | Global                             |
| Dynamic             | Yes                                |
| Type                | Integer                            |
| Default Value       | 0                                  |
| Minimum Value       | 0                                  |
| Maximum Value       | 2**32-1                            |

By default, setting [innodb\\_fil\\_make\\_page\\_dirty\\_debug](#page-7-0) to the ID of a tablespace immediately dirties the first page of the tablespace. If [innodb\\_saved\\_page\\_number\\_debug](#page-41-0) is set to a nondefault value, setting [innodb\\_fil\\_make\\_page\\_dirty\\_debug](#page-7-0) dirties the specified page. The [innodb\\_fil\\_make\\_page\\_dirty\\_debug](#page-7-0) option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-7-1"></span>• [innodb\\_file\\_format](#page-7-1)

| Command-Line Format | innodb-file-format=value |
|---------------------|--------------------------|
| Deprecated          | Yes                      |
| System Variable     | innodb_file_format       |
| Scope               | Global                   |
| Dynamic             | Yes                      |
| Type                | String                   |
| Default Value       | Barracuda                |
| Valid Values        | Antelope                 |

Barracuda

Enables an InnoDB file format for file-per-table tablespaces. Supported file formats are Antelope and Barracuda. Antelope is the original InnoDB file format, which supports REDUNDANT and COMPACT row formats. Barracuda is the newer file format, which supports COMPRESSED and DYNAMIC row formats.

COMPRESSED and DYNAMIC row formats enable important storage features for InnoDB tables. See Section 14.11, "InnoDB Row Formats".

Changing the [innodb\\_file\\_format](#page-7-1) setting does not affect the file format of existing InnoDB tablespace files.

The [innodb\\_file\\_format](#page-7-1) setting does not apply to general tablespaces, which support tables of all row formats. See Section 14.6.3.3, "General Tablespaces".

The [innodb\\_file\\_format](#page-7-1) default value was changed to Barracuda in MySQL 5.7.

The [innodb\\_file\\_format](#page-7-1) setting is ignored when creating tables that use the DYNAMIC row format. A table created using the DYNAMIC row format always uses the Barracuda file format, regardless of the [innodb\\_file\\_format](#page-7-1) setting. To use the COMPRESSED row format, [innodb\\_file\\_format](#page-7-1) must be set to Barracuda.

The [innodb\\_file\\_format](#page-7-1) option is deprecated; expect it to be removed in a future release. The purpose of the [innodb\\_file\\_format](#page-7-1) option was to allow users to downgrade to the built-in version of InnoDB in earlier versions of MySQL. Now that those versions of MySQL have reached the end of their product lifecycles, downgrade support provided by this option is no longer necessary.

For more information, see Section 14.10, "InnoDB File-Format Management".

<span id="page-8-0"></span>• [innodb\\_file\\_format\\_check](#page-8-0)

| Command-Line Format | innodb-file-format-check[={OFF |
|---------------------|--------------------------------|
|                     | ON}]                           |
| Deprecated          | Yes                            |
| System Variable     | innodb_file_format_check       |
| Scope               | Global                         |
| Dynamic             | No                             |
| Type                | Boolean                        |
| Default Value       | ON                             |

This variable can be set to 1 or 0 at server startup to enable or disable whether InnoDB checks the file format tag in the system tablespace (for example, Antelope or Barracuda). If the tag is checked and is higher than that supported by the current version of InnoDB, an error occurs and InnoDB does not start. If the tag is not higher, InnoDB sets the value of [innodb\\_file\\_format\\_max](#page-9-0) to the file format tag.

![](_page_8_Picture_13.jpeg)

#### **Note**

Despite the default value sometimes being displayed as ON or OFF, always use the numeric values 1 or 0 to turn this option on or off in your configuration file or command line string.

For more information, see Section 14.10.2.1, "Compatibility Check When InnoDB Is Started".

The [innodb\\_file\\_format\\_check](#page-8-0) option is deprecated together with the [innodb\\_file\\_format](#page-7-1) option. You should expect both options to be removed in a future release.

<span id="page-9-0"></span>• [innodb\\_file\\_format\\_max](#page-9-0)

| Command-Line Format | innodb-file-format-max=value |
|---------------------|------------------------------|
| Deprecated          | Yes                          |
| System Variable     | innodb_file_format_max       |
| Scope               | Global                       |
| Dynamic             | Yes                          |
| Type                | String                       |
| Default Value       | Barracuda                    |
| Valid Values        | Antelope                     |
|                     | Barracuda                    |

At server startup, InnoDB sets the value of this variable to the file format tag in the system tablespace (for example, Antelope or Barracuda). If the server creates or opens a table with a "higher" file format, it sets the value of [innodb\\_file\\_format\\_max](#page-9-0) to that format.

For related information, see Section 14.10, "InnoDB File-Format Management".

The [innodb\\_file\\_format\\_max](#page-9-0) option is deprecated together with the [innodb\\_file\\_format](#page-7-1) option. You should expect both options to be removed in a future release.

<span id="page-9-1"></span>• [innodb\\_file\\_per\\_table](#page-9-1)

| Command-Line Format | innodb-file-per-table[={OFF ON}] |
|---------------------|----------------------------------|
| System Variable     | innodb_file_per_table            |
| Scope               | Global                           |
| Dynamic             | Yes                              |
| Type                | Boolean                          |
| Default Value       | ON                               |

When [innodb\\_file\\_per\\_table](#page-9-1) is enabled, tables are created in file-per-table tablespaces by default. When disabled, tables are created in the system tablespace by default. For information about file-per-table tablespaces, see Section 14.6.3.2, "File-Per-Table Tablespaces". For information about the InnoDB system tablespace, see Section 14.6.3.1, "The System Tablespace".

The [innodb\\_file\\_per\\_table](#page-9-1) variable can be configured at runtime using a SET GLOBAL statement, specified on the command line at startup, or specified in an option file. Configuration at runtime requires privileges sufficient to set global system variables (see Section 5.1.8.1, "System Variable Privileges") and immediately affects the operation of all connections.

When a table that resides in a file-per-table tablespace is truncated or dropped, the freed space is returned to the operating system. Truncating or dropping a table that resides in the system tablespace only frees space in the system tablespace. Freed space in the system tablespace can be used again for InnoDB data but is not returned to the operating system, as system tablespace data files never shrink.

When [innodb\\_file\\_per\\_table](#page-9-1) is enabled, a table-copying ALTER TABLE operation on a table that resides in the system tablespace implicitly re-creates the table in a file-per-table tablespace. To prevent this from occurring, disable [innodb\\_file\\_per\\_table](#page-9-1) before executing table-copying ALTER TABLE operations on tables that reside in the system tablespace.

The [innodb\\_file\\_per-table](#page-9-1) setting does not affect the creation of temporary tables. Temporary tables are created in the temporary tablespace. See Section 14.6.3.5, "The Temporary Tablespace".

### <span id="page-10-0"></span>• [innodb\\_fill\\_factor](#page-10-0)

| Command-Line Format | innodb-fill-factor=# |
|---------------------|----------------------|
| System Variable     | innodb_fill_factor   |
| Scope               | Global               |
| Dynamic             | Yes                  |
| Type                | Integer              |
| Default Value       | 100                  |
| Minimum Value       | 10                   |
| Maximum Value       | 100                  |

InnoDB performs a bulk load when creating or rebuilding indexes. This method of index creation is known as a "sorted index build".

[innodb\\_fill\\_factor](#page-10-0) defines the percentage of space on each B-tree page that is filled during a sorted index build, with the remaining space reserved for future index growth. For example, setting [innodb\\_fill\\_factor](#page-10-0) to 80 reserves 20 percent of the space on each B-tree page for future index growth. Actual percentages may vary. The [innodb\\_fill\\_factor](#page-10-0) setting is interpreted as a hint rather than a hard limit.

An [innodb\\_fill\\_factor](#page-10-0) setting of 100 leaves 1/16 of the space in clustered index pages free for future index growth.

[innodb\\_fill\\_factor](#page-10-0) applies to both B-tree leaf and non-leaf pages. It does not apply to external pages used for TEXT or BLOB entries.

For more information, see Section 14.6.2.3, "Sorted Index Builds".

### <span id="page-10-1"></span>• [innodb\\_flush\\_log\\_at\\_timeout](#page-10-1)

| Command-Line Format | innodb-flush-log-at-timeout=# |
|---------------------|-------------------------------|
| System Variable     | innodb_flush_log_at_timeout   |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | Integer                       |
| Default Value       | 1                             |
| Minimum Value       | 1                             |
| Maximum Value       | 2700                          |
| Unit                | seconds                       |

Write and flush the logs every N seconds. [innodb\\_flush\\_log\\_at\\_timeout](#page-10-1) allows the timeout period between flushes to be increased in order to reduce flushing and avoid impacting performance of binary log group commit. The default setting for [innodb\\_flush\\_log\\_at\\_timeout](#page-10-1) is once per second.

### <span id="page-10-2"></span>• [innodb\\_flush\\_log\\_at\\_trx\\_commit](#page-10-2)

| Command-Line Format | innodb-flush-log-at-trx-commit=# |
|---------------------|----------------------------------|
| System Variable     | innodb_flush_log_at_trx_commit   |
| Scope               | Global                           |
| Dynamic             | Yes                              |
| Type                | Enumeration                      |

| Default Value | 1 |
|---------------|---|
| Valid Values  | 0 |
|               | 1 |
|               | 2 |

Controls the balance between strict ACID compliance for commit operations and higher performance that is possible when commit-related I/O operations are rearranged and done in batches. You can achieve better performance by changing the default value but then you can lose transactions in a crash.

- The default setting of 1 is required for full ACID compliance. Logs are written and flushed to disk at each transaction commit.
- With a setting of 0, logs are written and flushed to disk once per second. Transactions for which logs have not been flushed can be lost in a crash.
- With a setting of 2, logs are written after each transaction commit and flushed to disk once per second. Transactions for which logs have not been flushed can be lost in a crash.
- For settings 0 and 2, once-per-second flushing is not 100% guaranteed. Flushing may occur more frequently due to DDL changes and other internal InnoDB activities that cause logs to be flushed independently of the [innodb\\_flush\\_log\\_at\\_trx\\_commit](#page-10-2) setting, and sometimes less frequently due to scheduling issues. If logs are flushed once per second, up to one second of transactions can be lost in a crash. If logs are flushed more or less frequently than once per second, the amount of transactions that can be lost varies accordingly.
- Log flushing frequency is controlled by [innodb\\_flush\\_log\\_at\\_timeout](#page-10-1), which allows you to set log flushing frequency to N seconds (where N is 1 ... 2700, with a default value of 1). However, any unexpected mysqld process exit can erase up to N seconds of transactions.
- DDL changes and other internal InnoDB activities flush the log independently of the [innodb\\_flush\\_log\\_at\\_trx\\_commit](#page-10-2) setting.
- InnoDB crash recovery works regardless of the [innodb\\_flush\\_log\\_at\\_trx\\_commit](#page-10-2) setting. Transactions are either applied entirely or erased entirely.

For durability and consistency in a replication setup that uses InnoDB with transactions:

- If binary logging is enabled, set sync\_binlog=1.
- Always set [innodb\\_flush\\_log\\_at\\_trx\\_commit=1](#page-10-2).

For information on the combination of settings on a replica that is most resilient to unexpected halts, see Section 16.3.2, "Handling an Unexpected Halt of a Replica".

![](_page_11_Picture_14.jpeg)

#### **Caution**

Many operating systems and some disk hardware fool the flush-to-disk operation. They may tell mysqld that the flush has taken place, even though it has not. In this case, the durability of transactions is not guaranteed even with the recommended settings, and in the worst case, a power outage can corrupt InnoDB data. Using a battery-backed disk cache in the SCSI disk controller or in the disk itself speeds up file flushes, and makes the operation safer. You can also try to disable the caching of disk writes in hardware caches.

<span id="page-12-0"></span>• [innodb\\_flush\\_method](#page-12-0)

| Command-Line Format    | innodb-flush-method=value |
|------------------------|---------------------------|
| System Variable        | innodb_flush_method       |
| Scope                  | Global                    |
| Dynamic                | No                        |
| Type                   | String                    |
| Default Value          | NULL                      |
| Valid Values (Unix)    | fsync                     |
|                        | O_DSYNC                   |
|                        | littlesync                |
|                        | nosync                    |
|                        | O_DIRECT                  |
|                        | O_DIRECT_NO_FSYNC         |
| Valid Values (Windows) | async_unbuffered          |
|                        | normal                    |
|                        | unbuffered                |

Defines the method used to flush data to InnoDB data files and log files, which can affect I/O throughput.

If [innodb\\_flush\\_method](#page-12-0) is set to NULL on a Unix-like system, the fsync option is used by default. If [innodb\\_flush\\_method](#page-12-0) is set to NULL on Windows, the async\_unbuffered option is used by default.

The [innodb\\_flush\\_method](#page-12-0) options for Unix-like systems include:

- fsync: InnoDB uses the fsync() system call to flush both the data and log files. fsync is the default setting.
- O\_DSYNC: InnoDB uses O\_SYNC to open and flush the log files, and fsync() to flush the data files. InnoDB does not use O\_DSYNC directly because there have been problems with it on many varieties of Unix.
- littlesync: This option is used for internal performance testing and is currently unsupported. Use at your own risk.
- nosync: This option is used for internal performance testing and is currently unsupported. Use at your own risk.
- O\_DIRECT: InnoDB uses O\_DIRECT (or directio() on Solaris) to open the data files, and uses fsync() to flush both the data and log files. This option is available on some GNU/Linux versions, FreeBSD, and Solaris.
- O\_DIRECT\_NO\_FSYNC: InnoDB uses O\_DIRECT during flushing I/O, but skips the fsync() system call after each write operation.

Prior to MySQL 5.7.25, this setting is not suitable for file systems such as XFS and EXT4, which require an fsync() system call to synchronize file system metadata changes. If you are not sure whether your file system requires an fsync() system call to synchronize file system metadata changes, use O\_DIRECT instead.

As of MySQL 5.7.25, fsync() is called after creating a new file, after increasing file size, and after closing a file, to ensure that file system metadata changes are synchronized. The fsync() system call is still skipped after each write operation.

Data loss is possible if redo log files and data files reside on different storage devices, and an unexpected exit occurs before data file writes are flushed from a device cache that is not batterybacked. If you use or intend to use different storage devices for redo log files and data files, and your data files reside on a device with a cache that is not battery-backed, use O\_DIRECT instead.

The [innodb\\_flush\\_method](#page-12-0) options for Windows systems include:

• async\_unbuffered: InnoDB uses Windows asynchronous I/O and non-buffered I/O. async\_unbuffered is the default setting on Windows systems.

Running MySQL server on a 4K sector hard drive on Windows is not supported with async\_unbuffered. The workaround is to use [innodb\\_flush\\_method=normal](#page-12-0).

- normal: InnoDB uses simulated asynchronous I/O and buffered I/O.
- unbuffered: InnoDB uses simulated asynchronous I/O and non-buffered I/O.

How each setting affects performance depends on hardware configuration and workload. Benchmark your particular configuration to decide which setting to use, or whether to keep the default setting. Examine the Innodb\_data\_fsyncs status variable to see the overall number of fsync() calls for each setting. The mix of read and write operations in your workload can affect how a setting performs. For example, on a system with a hardware RAID controller and battery-backed write cache, O\_DIRECT can help to avoid double buffering between the InnoDB buffer pool and the operating system file system cache. On some systems where InnoDB data and log files are located on a SAN, the default value or O\_DSYNC might be faster for a read-heavy workload with mostly SELECT statements. Always test this parameter with hardware and workload that reflect your production environment. For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/ O".

<span id="page-13-0"></span>• [innodb\\_flush\\_neighbors](#page-13-0)

| Command-Line Format | innodb-flush-neighbors=# |
|---------------------|--------------------------|
| System Variable     | innodb_flush_neighbors   |
| Scope               | Global                   |
| Dynamic             | Yes                      |
| Type                | Enumeration              |
| Default Value       | 1                        |
| Valid Values        | 0                        |
|                     | 1                        |
|                     | 2                        |

Specifies whether flushing a page from the InnoDB buffer pool also flushes other dirty pages in the same extent.

- A setting of 0 disables [innodb\\_flush\\_neighbors](#page-13-0). Dirty pages in the same extent are not flushed.
- The default setting of 1 flushes contiguous dirty pages in the same extent.

• A setting of 2 flushes dirty pages in the same extent.

When the table data is stored on a traditional HDD storage device, flushing such neighbor pages in one operation reduces I/O overhead (primarily for disk seek operations) compared to flushing individual pages at different times. For table data stored on SSD, seek time is not a significant factor and you can turn this setting off to spread out write operations. For related information, see Section 14.8.3.5, "Configuring Buffer Pool Flushing".

<span id="page-14-0"></span>• [innodb\\_flush\\_sync](#page-14-0)

| Command-Line Format | innodb-flush-sync[={OFF ON}] |
|---------------------|------------------------------|
| System Variable     | innodb_flush_sync            |
| Scope               | Global                       |
| Dynamic             | Yes                          |
| Type                | Boolean                      |
| Default Value       | ON                           |

The [innodb\\_flush\\_sync](#page-14-0) variable, which is enabled by default, causes the [innodb\\_io\\_capacity](#page-20-0) setting to be ignored during bursts of I/O activity that occur at checkpoints. To adhere to the I/O rate defined by the [innodb\\_io\\_capacity](#page-20-0) setting, disable [innodb\\_flush\\_sync](#page-14-0).

For information about configuring the [innodb\\_flush\\_sync](#page-14-0) variable, see Section 14.8.8, "Configuring InnoDB I/O Capacity".

<span id="page-14-1"></span>• [innodb\\_flushing\\_avg\\_loops](#page-14-1)

| Command-Line Format | innodb-flushing-avg-loops=# |
|---------------------|-----------------------------|
| System Variable     | innodb_flushing_avg_loops   |
| Scope               | Global                      |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 30                          |
| Minimum Value       | 1                           |
| Maximum Value       | 1000                        |

Number of iterations for which InnoDB keeps the previously calculated snapshot of the flushing state, controlling how quickly adaptive flushing responds to changing workloads. Increasing the value makes the rate of flush operations change smoothly and gradually as the workload changes. Decreasing the value makes adaptive flushing adjust quickly to workload changes, which can cause spikes in flushing activity if the workload increases and decreases suddenly.

For related information, see Section 14.8.3.5, "Configuring Buffer Pool Flushing".

<span id="page-14-2"></span>• [innodb\\_force\\_load\\_corrupted](#page-14-2)

| Command-Line Format | innodb-force-load-corrupted[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | innodb_force_load_corrupted                |
| Scope               | Global                                     |
| Dynamic             | No                                         |
| Type                | Boolean                                    |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

Permits InnoDB to load tables at startup that are marked as corrupted. Use only during troubleshooting, to recover data that is otherwise inaccessible. When troubleshooting is complete, disable this setting and restart the server.

<span id="page-15-0"></span>• [innodb\\_force\\_recovery](#page-15-0)

| Command-Line Format | innodb-force-recovery=# |
|---------------------|-------------------------|
| System Variable     | innodb_force_recovery   |
| Scope               | Global                  |
| Dynamic             | No                      |
| Type                | Integer                 |
| Default Value       | 0                       |
| Minimum Value       | 0                       |
| Maximum Value       | 6                       |

The crash recovery mode, typically only changed in serious troubleshooting situations. Possible values are from 0 to 6. For the meanings of these values and important information about [innodb\\_force\\_recovery](#page-15-0), see [Section 14.22.2, "Forcing InnoDB Recovery".](#page-140-0)

![](_page_15_Picture_6.jpeg)

#### **Warning**

Only set this variable to a value greater than 0 in an emergency situation so that you can start InnoDB and dump your tables. As a safety measure, InnoDB prevents INSERT, UPDATE, or DELETE operations when [innodb\\_force\\_recovery](#page-15-0) is greater than 0. An [innodb\\_force\\_recovery](#page-15-0) setting of 4 or greater places InnoDB into readonly mode.

These restrictions may cause replication administration commands to fail with an error because replication settings such as relay\_log\_info\_repository=TABLE and master\_info\_repository=TABLE store information in InnoDB tables.

<span id="page-15-1"></span>• [innodb\\_ft\\_aux\\_table](#page-15-1)

| System Variable | innodb_ft_aux_table |
|-----------------|---------------------|
| Scope           | Global              |
| Dynamic         | Yes                 |
| Type            | String              |

Specifies the qualified name of an InnoDB table containing a FULLTEXT index. This variable is intended for diagnostic purposes and can only be set at runtime. For example:

```
SET GLOBAL innodb_ft_aux_table = 'test/t1';
```

After you set this variable to a name in the format db\_name/table\_name, the INFORMATION\_SCHEMA tables INNODB\_FT\_INDEX\_TABLE, INNODB\_FT\_INDEX\_CACHE, INNODB\_FT\_CONFIG, INNODB\_FT\_DELETED, and INNODB\_FT\_BEING\_DELETED show information about the search index for the specified table.

For more information, see [Section 14.16.4, "InnoDB INFORMATION\\_SCHEMA FULLTEXT Index](#page-70-0) [Tables"](#page-70-0).

<span id="page-15-2"></span>• [innodb\\_ft\\_cache\\_size](#page-15-2)

| Command-Line Format | innodb-ft-cache-size=# |
|---------------------|------------------------|
| System Variable     | innodb_ft_cache_size   |
| Scope               | Global                 |
| Dynamic             | No                     |
| Type                | Integer                |
| Default Value       | 8000000                |
| Minimum Value       | 1600000                |
| Maximum Value       | 80000000               |
| Unit                | bytes                  |

The memory allocated, in bytes, for the InnoDB FULLTEXT search index cache, which holds a parsed document in memory while creating an InnoDB FULLTEXT index. Index inserts and updates are only committed to disk when the [innodb\\_ft\\_cache\\_size](#page-15-2) size limit is reached. [innodb\\_ft\\_cache\\_size](#page-15-2) defines the cache size on a per table basis. To set a global limit for all tables, see [innodb\\_ft\\_total\\_cache\\_size](#page-19-0).

For more information, see InnoDB Full-Text Index Cache.

<span id="page-16-0"></span>• [innodb\\_ft\\_enable\\_diag\\_print](#page-16-0)

| Command-Line Format | innodb-ft-enable-diag-print[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | innodb_ft_enable_diag_print                |
| Scope               | Global                                     |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | OFF                                        |

Whether to enable additional full-text search (FTS) diagnostic output. This option is primarily intended for advanced FTS debugging and is not of interest to most users. Output is printed to the error log and includes information such as:

• FTS index sync progress (when the FTS cache limit is reached). For example:

```
FTS SYNC for table test, deleted count: 100 size: 10000 bytes
SYNC words: 100
```

• FTS optimize progress. For example:

```
FTS start optimize test
FTS_OPTIMIZE: optimize "mysql"
FTS_OPTIMIZE: processed "mysql"
```

• FTS index build progress. For example:

```
Number of doc processed: 1000
```

• For FTS queries, the query parsing tree, word weight, query processing time, and memory usage are printed. For example:

```
FTS Search Processing time: 1 secs: 100 millisec: row(s) 10000
Full Search Memory: 245666 (bytes), Row: 10000
```

<span id="page-17-0"></span>• [innodb\\_ft\\_enable\\_stopword](#page-17-0)

| Command-Line Format | innodb-ft-enable-stopword[={OFF <br>ON}] |
|---------------------|------------------------------------------|
| System Variable     | innodb_ft_enable_stopword                |
| Scope               | Global, Session                          |
| Dynamic             | Yes                                      |
| Type                | Boolean                                  |
| Default Value       | ON                                       |

Specifies that a set of stopwords is associated with an InnoDB FULLTEXT index at the time the index is created. If the [innodb\\_ft\\_user\\_stopword\\_table](#page-20-1) option is set, the stopwords are taken from that table. Else, if the [innodb\\_ft\\_server\\_stopword\\_table](#page-18-0) option is set, the stopwords are taken from that table. Otherwise, a built-in set of default stopwords is used.

For more information, see Section 12.9.4, "Full-Text Stopwords".

<span id="page-17-1"></span>• [innodb\\_ft\\_max\\_token\\_size](#page-17-1)

| Command-Line Format | innodb-ft-max-token-size=# |
|---------------------|----------------------------|
| System Variable     | innodb_ft_max_token_size   |
| Scope               | Global                     |
| Dynamic             | No                         |
| Type                | Integer                    |
| Default Value       | 84                         |
| Minimum Value       | 10                         |
| Maximum Value       | 84                         |

Maximum character length of words that are stored in an InnoDB FULLTEXT index. Setting a limit on this value reduces the size of the index, thus speeding up queries, by omitting long keywords or arbitrary collections of letters that are not real words and are not likely to be search terms.

For more information, see Section 12.9.6, "Fine-Tuning MySQL Full-Text Search".

<span id="page-17-2"></span>• [innodb\\_ft\\_min\\_token\\_size](#page-17-2)

| Command-Line Format | innodb-ft-min-token-size=# |
|---------------------|----------------------------|
| System Variable     | innodb_ft_min_token_size   |
| Scope               | Global                     |
| Dynamic             | No                         |
| Type                | Integer                    |
| Default Value       | 3                          |
| Minimum Value       | 0                          |
| Maximum Value       | 16                         |

Minimum length of words that are stored in an InnoDB FULLTEXT index. Increasing this value reduces the size of the index, thus speeding up queries, by omitting common words that are unlikely to be significant in a search context, such as the English words "a" and "to". For content using a CJK (Chinese, Japanese, Korean) character set, specify a value of 1.

<span id="page-18-1"></span>• [innodb\\_ft\\_num\\_word\\_optimize](#page-18-1)

| Command-Line Format | innodb-ft-num-word-optimize=# |
|---------------------|-------------------------------|
| System Variable     | innodb_ft_num_word_optimize   |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | Integer                       |
| Default Value       | 2000                          |
| Minimum Value       | 1000                          |
| Maximum Value       | 10000                         |

Number of words to process during each OPTIMIZE TABLE operation on an InnoDB FULLTEXT index. Because a bulk insert or update operation to a table containing a full-text search index could require substantial index maintenance to incorporate all changes, you might do a series of OPTIMIZE TABLE statements, each picking up where the last left off.

For more information, see Section 12.9.6, "Fine-Tuning MySQL Full-Text Search".

<span id="page-18-2"></span>• [innodb\\_ft\\_result\\_cache\\_limit](#page-18-2)

| Command-Line Format | innodb-ft-result-cache-limit=# |
|---------------------|--------------------------------|
| System Variable     | innodb_ft_result_cache_limit   |
| Scope               | Global                         |
| Dynamic             | Yes                            |
| Type                | Integer                        |
| Default Value       | 2000000000                     |
| Minimum Value       | 1000000                        |
| Maximum Value       | 2**32-1                        |
| Unit                | bytes                          |

The InnoDB full-text search query result cache limit (defined in bytes) per full-text search query or per thread. Intermediate and final InnoDB full-text search query results are handled in memory. Use [innodb\\_ft\\_result\\_cache\\_limit](#page-18-2) to place a size limit on the full-text search query result cache to avoid excessive memory consumption in case of very large InnoDB full-text search query results (millions or hundreds of millions of rows, for example). Memory is allocated as required when a fulltext search query is processed. If the result cache size limit is reached, an error is returned indicating that the query exceeds the maximum allowed memory.

The maximum value of [innodb\\_ft\\_result\\_cache\\_limit](#page-18-2) for all platform types and bit sizes is 2\*\*32-1.

<span id="page-18-0"></span>• [innodb\\_ft\\_server\\_stopword\\_table](#page-18-0)

| Command-Line Format | innodb-ft-server-stopword<br>table=db_name/table_name |
|---------------------|-------------------------------------------------------|
| System Variable     | innodb_ft_server_stopword_table                       |
| Scope               | Global                                                |
| Dynamic             | Yes                                                   |
| Type                | String                                                |

| Default Value | NULL |
|---------------|------|
|---------------|------|

This option is used to specify your own InnoDB FULLTEXT index stopword list for all InnoDB tables. To configure your own stopword list for a specific InnoDB table, use [innodb\\_ft\\_user\\_stopword\\_table](#page-20-1).

Set [innodb\\_ft\\_server\\_stopword\\_table](#page-18-0) to the name of the table containing a list of stopwords, in the format db\_name/table\_name.

The stopword table must exist before you configure [innodb\\_ft\\_server\\_stopword\\_table](#page-18-0). [innodb\\_ft\\_enable\\_stopword](#page-17-0) must be enabled and [innodb\\_ft\\_server\\_stopword\\_table](#page-18-0) option must be configured before you create the FULLTEXT index.

The stopword table must be an InnoDB table, containing a single VARCHAR column named value.

For more information, see Section 12.9.4, "Full-Text Stopwords".

<span id="page-19-1"></span>• [innodb\\_ft\\_sort\\_pll\\_degree](#page-19-1)

| Command-Line Format | innodb-ft-sort-pll-degree=# |
|---------------------|-----------------------------|
| System Variable     | innodb_ft_sort_pll_degree   |
| Scope               | Global                      |
| Dynamic             | No                          |
| Type                | Integer                     |
| Default Value       | 2                           |
| Minimum Value       | 1                           |
| Maximum Value       | 16                          |

Number of threads used in parallel to index and tokenize text in an InnoDB FULLTEXT index when building a search index.

For related information, see Section 14.6.2.4, "InnoDB Full-Text Indexes", and [innodb\\_sort\\_buffer\\_size](#page-41-1).

<span id="page-19-0"></span>• [innodb\\_ft\\_total\\_cache\\_size](#page-19-0)

| Command-Line Format | innodb-ft-total-cache-size=# |
|---------------------|------------------------------|
| System Variable     | innodb_ft_total_cache_size   |
| Scope               | Global                       |
| Dynamic             | No                           |
| Type                | Integer                      |
| Default Value       | 640000000                    |
| Minimum Value       | 32000000                     |
| Maximum Value       | 1600000000                   |
| Unit                | bytes                        |

The total memory allocated, in bytes, for the InnoDB full-text search index cache for all tables. Creating numerous tables, each with a FULLTEXT search index, could consume a significant portion of available memory. [innodb\\_ft\\_total\\_cache\\_size](#page-19-0) defines a global memory limit for all fulltext search indexes to help avoid excessive memory consumption. If the global limit is reached by an index operation, a forced sync is triggered.

<span id="page-20-1"></span>• [innodb\\_ft\\_user\\_stopword\\_table](#page-20-1)

| Command-Line Format | innodb-ft-user-stopword<br>table=db_name/table_name |
|---------------------|-----------------------------------------------------|
| System Variable     | innodb_ft_user_stopword_table                       |
| Scope               | Global, Session                                     |
| Dynamic             | Yes                                                 |
| Type                | String                                              |
| Default Value       | NULL                                                |

This option is used to specify your own InnoDB FULLTEXT index stopword list on a specific table. To configure your own stopword list for all InnoDB tables, use [innodb\\_ft\\_server\\_stopword\\_table](#page-18-0).

Set [innodb\\_ft\\_user\\_stopword\\_table](#page-20-1) to the name of the table containing a list of stopwords, in the format db\_name/table\_name.

The stopword table must exist before you configure [innodb\\_ft\\_user\\_stopword\\_table](#page-20-1). [innodb\\_ft\\_enable\\_stopword](#page-17-0) must be enabled and [innodb\\_ft\\_user\\_stopword\\_table](#page-20-1) must be configured before you create the FULLTEXT index.

The stopword table must be an InnoDB table, containing a single VARCHAR column named value.

For more information, see Section 12.9.4, "Full-Text Stopwords".

<span id="page-20-0"></span>• [innodb\\_io\\_capacity](#page-20-0)

| Command-Line Format              | innodb-io-capacity=# |
|----------------------------------|----------------------|
| System Variable                  | innodb_io_capacity   |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 200                  |
| Minimum Value                    | 100                  |
| Maximum Value (64-bit platforms) | 2**64-1              |
| Maximum Value                    | 2**32-1              |

The [innodb\\_io\\_capacity](#page-20-0) variable defines the number of I/O operations per second (IOPS) available to InnoDB background tasks, such as flushing pages from the buffer pool and merging data from the change buffer.

For information about configuring the [innodb\\_io\\_capacity](#page-20-0) variable, see Section 14.8.8, "Configuring InnoDB I/O Capacity".

<span id="page-20-2"></span>• [innodb\\_io\\_capacity\\_max](#page-20-2)

| Command-Line Format | innodb-io-capacity-max=#                |
|---------------------|-----------------------------------------|
| System Variable     | innodb_io_capacity_max                  |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | Integer                                 |
| Default Value       | 2 * innodb_io_capacity, min of 20002593 |

| Minimum Value                          | 100     |
|----------------------------------------|---------|
| Maximum Value (Unix, 64-bit platforms) | 2**64-1 |
| Maximum Value (Other)                  | 2**32-1 |

If flushing activity falls behind, InnoDB can flush more aggressively, at a higher rate of I/ O operations per second (IOPS) than defined by the [innodb\\_io\\_capacity](#page-20-0) variable. The [innodb\\_io\\_capacity\\_max](#page-20-2) variable defines a maximum number of IOPS performed by InnoDB background tasks in such situations.

For information about configuring the [innodb\\_io\\_capacity\\_max](#page-20-2) variable, see Section 14.8.8, "Configuring InnoDB I/O Capacity".

<span id="page-21-0"></span>• [innodb\\_large\\_prefix](#page-21-0)

| Command-Line Format | innodb-large-prefix[={OFF ON}] |
|---------------------|--------------------------------|
| Deprecated          | Yes                            |
| System Variable     | innodb_large_prefix            |
| Scope               | Global                         |
| Dynamic             | Yes                            |
| Type                | Boolean                        |
| Default Value       | ON                             |

When this option is enabled, index key prefixes longer than 767 bytes (up to 3072 bytes) are allowed for InnoDB tables that use DYNAMIC or COMPRESSED row format. See [Section 14.23, "InnoDB](#page-146-0) [Limits"](#page-146-0) for maximums associated with index key prefixes under various settings.

For tables that use REDUNDANT or COMPACT row format, this option does not affect the permitted index key prefix length.

[innodb\\_large\\_prefix](#page-21-0) is enabled by default in MySQL 5.7. This change coincides with the default value change for [innodb\\_file\\_format](#page-7-1), which is set to Barracuda by default in MySQL 5.7. Together, these default value changes allow larger index key prefixes to be created when using DYNAMIC or COMPRESSED row format. If either option is set to a non-default value, index key prefixes larger than 767 bytes are silently truncated.

[innodb\\_large\\_prefix](#page-21-0) is deprecated; expect it to be removed in a future release. [innodb\\_large\\_prefix](#page-21-0) was introduced to disable large index key prefixes for compatibility with earlier versions of InnoDB that do not support large index key prefixes.

<span id="page-21-1"></span>• [innodb\\_limit\\_optimistic\\_insert\\_debug](#page-21-1)

| Command-Line Format | innodb-limit-optimistic-insert<br>debug=# |
|---------------------|-------------------------------------------|
| System Variable     | innodb_limit_optimistic_insert_debug      |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Integer                                   |
| Default Value       | 0                                         |
| Minimum Value       | 0                                         |

| Maximum Value | 2**32-1 |  |
|---------------|---------|--|
|               |         |  |

Limits the number of records per B-tree page. A default value of 0 means that no limit is imposed. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-22-0"></span>• [innodb\\_lock\\_wait\\_timeout](#page-22-0)

| Command-Line Format | innodb-lock-wait-timeout=# |
|---------------------|----------------------------|
| System Variable     | innodb_lock_wait_timeout   |
| Scope               | Global, Session            |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 50                         |
| Minimum Value       | 1                          |
| Maximum Value       | 1073741824                 |
| Unit                | seconds                    |

The length of time in seconds an InnoDB transaction waits for a row lock before giving up. The default value is 50 seconds. A transaction that tries to access a row that is locked by another InnoDB transaction waits at most this many seconds for write access to the row before issuing the following error:

```
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

When a lock wait timeout occurs, the current statement is rolled back (not the entire transaction). To have the entire transaction roll back, start the server with the [--innodb-rollback-on-timeout](#page-40-0) option. See also [Section 14.22.4, "InnoDB Error Handling".](#page-146-1)

You might decrease this value for highly interactive applications or OLTP systems, to display user feedback quickly or put the update into a queue for processing later. You might increase this value for long-running back-end operations, such as a transform step in a data warehouse that waits for other large insert or update operations to finish.

[innodb\\_lock\\_wait\\_timeout](#page-22-0) applies to InnoDB row locks only. A MySQL table lock does not happen inside InnoDB and this timeout does not apply to waits for table locks.

The lock wait timeout value does not apply to deadlocks when [innodb\\_deadlock\\_detect](#page-5-0) is enabled (the default) because InnoDB detects deadlocks immediately and rolls back one of the deadlocked transactions. When [innodb\\_deadlock\\_detect](#page-5-0) is disabled, InnoDB relies on [innodb\\_lock\\_wait\\_timeout](#page-22-0) for transaction rollback when a deadlock occurs. See Section 14.7.5.2, "Deadlock Detection".

[innodb\\_lock\\_wait\\_timeout](#page-22-0) can be set at runtime with the SET GLOBAL or SET SESSION statement. Changing the GLOBAL setting requires privileges sufficient to set global system variables (see Section 5.1.8.1, "System Variable Privileges") and affects the operation of all clients that subsequently connect. Any client can change the SESSION setting for [innodb\\_lock\\_wait\\_timeout](#page-22-0), which affects only that client.

<span id="page-22-1"></span>• [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1)

| Command-Line Format | innodb-locks-unsafe-for<br>binlog[={OFF ON}] |
|---------------------|----------------------------------------------|
| Deprecated          | Yes                                          |
| System Variable     | innodb_locks_unsafe_for_binlog               |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | No      |
| Type          | Boolean |
| Default Value | OFF     |

This variable affects how InnoDB uses gap locking for searches and index scans. [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is deprecated; expect it to be removed in a future MySQL release.

Normally, InnoDB uses an algorithm called next-key locking that combines index-row locking with gap locking. InnoDB performs row-level locking in such a way that when it searches or scans a table index, it sets shared or exclusive locks on the index records it encounters. Thus, row-level locks are actually index-record locks. In addition, a next-key lock on an index record also affects the gap before the index record. That is, a next-key lock is an index-record lock plus a gap lock on the gap preceding the index record. If one session has a shared or exclusive lock on record R in an index, another session cannot insert a new index record in the gap immediately before R in the index order. See Section 14.7.1, "InnoDB Locking".

By default, the value of [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is 0 (disabled), which means that gap locking is enabled: InnoDB uses next-key locks for searches and index scans. To enable the variable, set it to 1. This causes gap locking to be disabled: InnoDB uses only index-record locks for searches and index scans.

Enabling [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) does not disable the use of gap locking for foreign-key constraint checking or duplicate-key checking.

The effects of enabling [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) are the same as setting the transaction isolation level to READ COMMITTED, with these exceptions:

- Enabling [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is a global setting and affects all sessions, whereas the isolation level can be set globally for all sessions, or individually per session.
- [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) can be set only at server startup, whereas the isolation level can be set at startup or changed at runtime.

READ COMMITTED therefore offers finer and more flexible control than [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1). For more information about the effect of isolation level on gap locking, see Section 14.7.2.1, "Transaction Isolation Levels".

Enabling [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) may cause phantom problems because other sessions can insert new rows into the gaps when gap locking is disabled. Suppose that there is an index on the id column of the child table and that you want to read and lock all rows from the table having an identifier value larger than 100, with the intention of updating some column in the selected rows later:

```
SELECT * FROM child WHERE id > 100 FOR UPDATE;
```

The query scans the index starting from the first record where the id is greater than 100. If the locks set on the index records in that range do not lock out inserts made in the gaps, another session can insert a new row into the table. Consequently, if you were to execute the same SELECT again within the same transaction, you would see a new row in the result set returned by the query. This also means that if new items are added to the database, InnoDB does not guarantee serializability. Therefore, if [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is enabled, InnoDB guarantees at most an

isolation level of READ COMMITTED. (Conflict serializability is still guaranteed.) For more information about phantoms, see Section 14.7.4, "Phantom Rows".

Enabling [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) has additional effects:

- For UPDATE or DELETE statements, InnoDB holds locks only for rows that it updates or deletes. Record locks for nonmatching rows are released after MySQL has evaluated the WHERE condition. This greatly reduces the probability of deadlocks, but they can still happen.
- For UPDATE statements, if a row is already locked, InnoDB performs a "semi-consistent" read, returning the latest committed version to MySQL so that MySQL can determine whether the row matches the WHERE condition of the UPDATE. If the row matches (must be updated), MySQL reads the row again and this time InnoDB either locks it or waits for a lock on it.

Consider the following example, beginning with this table:

```
CREATE TABLE t (a INT NOT NULL, b INT) ENGINE = InnoDB;
INSERT INTO t VALUES (1,2),(2,3),(3,2),(4,3),(5,2);
COMMIT;
```

In this case, table has no indexes, so searches and index scans use the hidden clustered index for record locking (see Section 14.6.2.1, "Clustered and Secondary Indexes").

Suppose that one client performs an UPDATE using these statements:

```
SET autocommit = 0;
UPDATE t SET b = 5 WHERE b = 3;
```

Suppose also that a second client performs an UPDATE by executing these statements following those of the first client:

```
SET autocommit = 0;
UPDATE t SET b = 4 WHERE b = 2;
```

As InnoDB executes each UPDATE, it first acquires an exclusive lock for each row, and then determines whether to modify it. If InnoDB does not modify the row and [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is enabled, it releases the lock. Otherwise, InnoDB retains the lock until the end of the transaction. This affects transaction processing as follows.

If [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is disabled, the first UPDATE acquires x-locks and does not release any of them:

```
x-lock(1,2); retain x-lock
x-lock(2,3); update(2,3) to (2,5); retain x-lock
x-lock(3,2); retain x-lock
x-lock(4,3); update(4,3) to (4,5); retain x-lock
x-lock(5,2); retain x-lock
```

The second UPDATE blocks as soon as it tries to acquire any locks (because the first update has retained locks on all rows), and does not proceed until the first UPDATE commits or rolls back:

```
x-lock(1,2); block and wait for first UPDATE to commit or roll back
```

If [innodb\\_locks\\_unsafe\\_for\\_binlog](#page-22-1) is enabled, the first UPDATE acquires x-locks and releases those for rows that it does not modify:

```
x-lock(1,2); unlock(1,2)
x-lock(2,3); update(2,3) to (2,5); retain x-lock
x-lock(3,2); unlock(3,2)
x-lock(4,3); update(4,3) to (4,5); retain x-lock
```

```
x-lock(5,2); unlock(5,2)
```

For the second UPDATE, InnoDB does a "semi-consistent" read, returning the latest committed version of each row to MySQL so that MySQL can determine whether the row matches the WHERE condition of the UPDATE:

```
x-lock(1,2); update(1,2) to (1,4); retain x-lock
x-lock(2,3); unlock(2,3)
x-lock(3,2); update(3,2) to (3,4); retain x-lock
x-lock(4,3); unlock(4,3)
x-lock(5,2); update(5,2) to (5,4); retain x-lock
```

### <span id="page-25-0"></span>• [innodb\\_log\\_buffer\\_size](#page-25-0)

| Command-Line Format | innodb-log-buffer-size=# |
|---------------------|--------------------------|
| System Variable     | innodb_log_buffer_size   |
| Scope               | Global                   |
| Dynamic             | No                       |
| Type                | Integer                  |
| Default Value       | 16777216                 |
| Minimum Value       | 1048576                  |
| Maximum Value       | 4294967295               |

The size in bytes of the buffer that InnoDB uses to write to the log files on disk. The default value changed from 8MB to 16MB with the introduction of 32KB and 64KB [innodb\\_page\\_size](#page-36-0) values. A large log buffer enables large transactions to run without the need to write the log to disk before the transactions commit. Thus, if you have transactions that update, insert, or delete many rows, making the log buffer larger saves disk I/O. For related information, see Memory Configuration, and Section 8.5.4, "Optimizing InnoDB Redo Logging". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

### <span id="page-25-1"></span>• [innodb\\_log\\_checkpoint\\_now](#page-25-1)

| Command-Line Format | innodb-log-checkpoint-now[={OFF <br>ON}] |
|---------------------|------------------------------------------|
| System Variable     | innodb_log_checkpoint_now                |
| Scope               | Global                                   |
| Dynamic             | Yes                                      |
| Type                | Boolean                                  |
| Default Value       | OFF                                      |

Enable this debug option to force InnoDB to write a checkpoint. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

### <span id="page-25-2"></span>• [innodb\\_log\\_checksums](#page-25-2)

| Command-Line Format | innodb-log-checksums[={OFF ON}] |
|---------------------|---------------------------------|
| System Variable     | innodb_log_checksums            |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Boolean                         |
| Default Value       | ON                              |

Enables or disables checksums for redo log pages.

[innodb\\_log\\_checksums=ON](#page-25-2) enables the CRC-32C checksum algorithm for redo log pages. When [innodb\\_log\\_checksums](#page-25-2) is disabled, the contents of the redo log page checksum field are ignored.

Checksums on the redo log header page and redo log checkpoint pages are never disabled.

<span id="page-26-0"></span>• [innodb\\_log\\_compressed\\_pages](#page-26-0)

| Command-Line Format | innodb-log-compressed-pages[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | innodb_log_compressed_pages                |
| Scope               | Global                                     |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | ON                                         |

Specifies whether images of re-compressed pages are written to the redo log. Re-compression may occur when changes are made to compressed data.

[innodb\\_log\\_compressed\\_pages](#page-26-0) is enabled by default to prevent corruption that could occur if a different version of the zlib compression algorithm is used during recovery. If you are certain that the zlib version is not subject to change, you can disable [innodb\\_log\\_compressed\\_pages](#page-26-0) to reduce redo log generation for workloads that modify compressed data.

To measure the effect of enabling or disabling [innodb\\_log\\_compressed\\_pages](#page-26-0), compare redo log generation for both settings under the same workload. Options for measuring redo log generation include observing the Log sequence number (LSN) in the LOG section of SHOW ENGINE INNODB STATUS output, or monitoring Innodb\_os\_log\_written status for the number of bytes written to the redo log files.

For related information, see Section 14.9.1.6, "Compression for OLTP Workloads".

<span id="page-26-1"></span>• [innodb\\_log\\_file\\_size](#page-26-1)

| Command-Line Format | innodb-log-file-size=#            |
|---------------------|-----------------------------------|
| System Variable     | innodb_log_file_size              |
| Scope               | Global                            |
| Dynamic             | No                                |
| Type                | Integer                           |
| Default Value       | 50331648                          |
| Minimum Value       | 4194304                           |
| Maximum Value       | 512GB / innodb_log_files_in_group |
| Unit                | bytes                             |

The size in bytes of each log file in a log group. The combined size of log files ([innodb\\_log\\_file\\_size](#page-26-1) \* [innodb\\_log\\_files\\_in\\_group](#page-27-0)) cannot exceed a maximum value that is slightly less than 512GB. A pair of 255 GB log files, for example, approaches the limit but does not exceed it. The default value is 48MB.

Generally, the combined size of the log files should be large enough that the server can smooth out peaks and troughs in workload activity, which often means that there is enough redo log space to handle more than an hour of write activity. The larger the value, the less checkpoint flush activity is required in the buffer pool, saving disk I/O. Larger log files also make crash recovery slower.

The minimum [innodb\\_log\\_file\\_size](#page-26-1) value was increased from 1MB to 4MB in MySQL 5.7.11.

For related information, see Redo Log File Configuration. For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-27-0"></span>• [innodb\\_log\\_files\\_in\\_group](#page-27-0)

| Command-Line Format | innodb-log-files-in-group=# |
|---------------------|-----------------------------|
| System Variable     | innodb_log_files_in_group   |
| Scope               | Global                      |
| Dynamic             | No                          |
| Type                | Integer                     |
| Default Value       | 2                           |
| Minimum Value       | 2                           |
| Maximum Value       | 100                         |

The number of log files in the log group. InnoDB writes to the files in a circular fashion. The default (and recommended) value is 2. The location of the files is specified by [innodb\\_log\\_group\\_home\\_dir](#page-27-1). The combined size of log files ([innodb\\_log\\_file\\_size](#page-26-1) \* [innodb\\_log\\_files\\_in\\_group](#page-27-0)) can be up to 512GB.

For related information, see Redo Log File Configuration.

<span id="page-27-1"></span>• [innodb\\_log\\_group\\_home\\_dir](#page-27-1)

| Command-Line Format | innodb-log-group-home-dir=dir_name |
|---------------------|------------------------------------|
| System Variable     | innodb_log_group_home_dir          |
| Scope               | Global                             |
| Dynamic             | No                                 |
| Type                | Directory name                     |

The directory path to the InnoDB redo log files, whose number is specified by [innodb\\_log\\_files\\_in\\_group](#page-27-0). If you do not specify any InnoDB log variables, the default is to create two files named ib\_logfile0 and ib\_logfile1 in the MySQL data directory. Log file size is given by the [innodb\\_log\\_file\\_size](#page-26-1) system variable.

For related information, see Redo Log File Configuration.

<span id="page-27-2"></span>• [innodb\\_log\\_write\\_ahead\\_size](#page-27-2)

| Command-Line Format | innodb-log-write-ahead-size=# |
|---------------------|-------------------------------|
| System Variable     | innodb_log_write_ahead_size   |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | Integer                       |
| Default Value       | 8192                          |
| Minimum Value       | 512 (log file block size)     |
| Maximum Value       | Equal to innodb_page_size     |
| Unit                | bytes                         |

Defines the write-ahead block size for the redo log, in bytes. To avoid "read-on-write", set [innodb\\_log\\_write\\_ahead\\_size](#page-27-2) to match the operating system or file system cache block size. The default setting is 8192 bytes. Read-on-write occurs when redo log blocks are not entirely cached to the operating system or file system due to a mismatch between write-ahead block size for the redo log and operating system or file system cache block size.

Valid values for [innodb\\_log\\_write\\_ahead\\_size](#page-27-2) are multiples of the InnoDB log file block size (2<sup>n</sup> ). The minimum value is the InnoDB log file block size (512). Write-ahead does not occur when the minimum value is specified. The maximum value is equal to the [innodb\\_page\\_size](#page-36-0) value. If you specify a value for [innodb\\_log\\_write\\_ahead\\_size](#page-27-2) that is larger than the [innodb\\_page\\_size](#page-36-0) value, the [innodb\\_log\\_write\\_ahead\\_size](#page-27-2) setting is truncated to the [innodb\\_page\\_size](#page-36-0) value.

Setting the [innodb\\_log\\_write\\_ahead\\_size](#page-27-2) value too low in relation to the operating system or file system cache block size results in "read-on-write". Setting the value too high may have a slight impact on fsync performance for log file writes due to several blocks being written at once.

For related information, see Section 8.5.4, "Optimizing InnoDB Redo Logging".

<span id="page-28-0"></span>• [innodb\\_lru\\_scan\\_depth](#page-28-0)

| Command-Line Format              | innodb-lru-scan-depth=# |
|----------------------------------|-------------------------|
| System Variable                  | innodb_lru_scan_depth   |
| Scope                            | Global                  |
| Dynamic                          | Yes                     |
| Type                             | Integer                 |
| Default Value                    | 1024                    |
| Minimum Value                    | 100                     |
| Maximum Value (64-bit platforms) | 2**64-1                 |
| Maximum Value                    | 2**32-1                 |

A parameter that influences the algorithms and heuristics for the flush operation for the InnoDB buffer pool. Primarily of interest to performance experts tuning I/O-intensive workloads. It specifies, per buffer pool instance, how far down the buffer pool LRU page list the page cleaner thread scans looking for dirty pages to flush. This is a background operation performed once per second.

A setting smaller than the default is generally suitable for most workloads. A value that is much higher than necessary may impact performance. Only consider increasing the value if you have spare I/O capacity under a typical workload. Conversely, if a write-intensive workload saturates your I/O capacity, decrease the value, especially in the case of a large buffer pool.

When tuning [innodb\\_lru\\_scan\\_depth](#page-28-0), start with a low value and configure the setting upward with the goal of rarely seeing zero free pages. Also, consider adjusting [innodb\\_lru\\_scan\\_depth](#page-28-0) when changing the number of buffer pool instances, since [innodb\\_lru\\_scan\\_depth](#page-28-0) \* innodb\_buffer\_pool\_instances defines the amount of work performed by the page cleaner thread each second.

For related information, see Section 14.8.3.5, "Configuring Buffer Pool Flushing". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-28-1"></span>• [innodb\\_max\\_dirty\\_pages\\_pct](#page-28-1)

| Command-Line Format | innodb-max-dirty-pages-pct=# |
|---------------------|------------------------------|
| System Variable     | innodb_max_dirty_pages_pct   |
| Scope               | Global                       |
| Dynamic             | Yes                          |
| Type                | Numeric                      |

| Default Value | 75     |
|---------------|--------|
| Minimum Value | 0      |
| Maximum Value | 99.999 |

InnoDB tries to flush data from the buffer pool so that the percentage of dirty pages does not exceed this value. The default value is 75.

The [innodb\\_max\\_dirty\\_pages\\_pct](#page-28-1) setting establishes a target for flushing activity. It does not affect the rate of flushing. For information about managing the rate of flushing, see Section 14.8.3.5, "Configuring Buffer Pool Flushing".

For related information, see Section 14.8.3.5, "Configuring Buffer Pool Flushing". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-29-0"></span>• [innodb\\_max\\_dirty\\_pages\\_pct\\_lwm](#page-29-0)

| Command-Line Format | innodb-max-dirty-pages-pct-lwm=# |
|---------------------|----------------------------------|
| System Variable     | innodb_max_dirty_pages_pct_lwm   |
| Scope               | Global                           |
| Dynamic             | Yes                              |
| Type                | Numeric                          |
| Default Value       | 0                                |
| Minimum Value       | 0                                |
| Maximum Value       | 99.999                           |

Defines a low water mark representing the percentage of dirty pages at which preflushing is enabled to control the dirty page ratio. The default of 0 disables the pre-flushing behavior entirely. The configured value should always be lower than the [innodb\\_max\\_dirty\\_pages\\_pct](#page-28-1) value. For more information, see Section 14.8.3.5, "Configuring Buffer Pool Flushing".

<span id="page-29-1"></span>• [innodb\\_max\\_purge\\_lag](#page-29-1)

| Command-Line Format | innodb-max-purge-lag=# |
|---------------------|------------------------|
| System Variable     | innodb_max_purge_lag   |
| Scope               | Global                 |
| Dynamic             | Yes                    |
| Type                | Integer                |
| Default Value       | 0                      |
| Minimum Value       | 0                      |
| Maximum Value       | 4294967295             |

Defines the desired maximum purge lag. If this value is exceeded, a delay is imposed on INSERT, UPDATE, and DELETE operations to allow time for purge to catch up. The default value is 0, which means there is no maximum purge lag and no delay.

For more information, see Section 14.8.10, "Purge Configuration".

<span id="page-29-2"></span>• [innodb\\_max\\_purge\\_lag\\_delay](#page-29-2)

| Command-Line Format | innodb-max-purge-lag-delay=# |
|---------------------|------------------------------|
| System Variable     | innodb_max_purge_lag_delay   |
| Scope               | Global                       |

| Dynamic       | Yes          |
|---------------|--------------|
| Type          | Integer      |
| Default Value | 0            |
| Minimum Value | 0            |
| Maximum Value | 10000000     |
| Unit          | microseconds |

Specifies the maximum delay in microseconds for the delay imposed when the [innodb\\_max\\_purge\\_lag](#page-29-1) threshold is exceeded. The specified [innodb\\_max\\_purge\\_lag\\_delay](#page-29-2) value is an upper limit on the delay period calculated by the [innodb\\_max\\_purge\\_lag](#page-29-1) formula.

For more information, see Section 14.8.10, "Purge Configuration".

<span id="page-30-0"></span>• [innodb\\_max\\_undo\\_log\\_size](#page-30-0)

| Command-Line Format | innodb-max-undo-log-size=# |
|---------------------|----------------------------|
| System Variable     | innodb_max_undo_log_size   |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 1073741824                 |
| Minimum Value       | 10485760                   |
| Maximum Value       | 2**64-1                    |
| Unit                | bytes                      |

Defines a threshold size for undo tablespaces. If an undo tablespace exceeds the threshold, it can be marked for truncation when [innodb\\_undo\\_log\\_truncate](#page-53-0) is enabled. The default value is 1073741824 bytes (1024 MiB).

For more information, see Truncating Undo Tablespaces.

<span id="page-30-1"></span>• [innodb\\_merge\\_threshold\\_set\\_all\\_debug](#page-30-1)

| Command-Line Format | innodb-merge-threshold-set-all<br>debug=# |
|---------------------|-------------------------------------------|
| System Variable     | innodb_merge_threshold_set_all_debug      |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Integer                                   |
| Default Value       | 50                                        |
| Minimum Value       | 1                                         |
| Maximum Value       | 50                                        |

Defines a page-full percentage value for index pages that overrides the current MERGE\_THRESHOLD setting for all indexes that are currently in the dictionary cache. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option. For related information, see Section 14.8.12, "Configuring the Merge Threshold for Index Pages".

<span id="page-31-0"></span>• [innodb\\_monitor\\_disable](#page-31-0)

| Command-Line Format | innodb-monitor-disable={counter <br>module pattern all} |
|---------------------|---------------------------------------------------------|
| System Variable     | innodb_monitor_disable                                  |
| Scope               | Global                                                  |
| Dynamic             | Yes                                                     |
| Type                | String                                                  |

This variable acts as a switch, disabling InnoDB metrics counters. Counter data may be queried using the Information Schema INNODB\_METRICS table. For usage information, see [Section 14.16.6,](#page-77-0) ["InnoDB INFORMATION\\_SCHEMA Metrics Table".](#page-77-0)

[innodb\\_monitor\\_disable='latch'](#page-31-0) disables statistics collection for SHOW ENGINE INNODB MUTEX. For more information, see Section 13.7.5.15, "SHOW ENGINE Statement".

<span id="page-31-1"></span>• [innodb\\_monitor\\_enable](#page-31-1)

| Command-Line Format | innodb-monitor-enable={counter <br>module pattern all} |
|---------------------|--------------------------------------------------------|
| System Variable     | innodb_monitor_enable                                  |
| Scope               | Global                                                 |
| Dynamic             | Yes                                                    |
| Type                | String                                                 |

This variable acts as a switch, enabling InnoDB metrics counters. Counter data may be queried using the Information Schema INNODB\_METRICS table. For usage information, see [Section 14.16.6,](#page-77-0) ["InnoDB INFORMATION\\_SCHEMA Metrics Table".](#page-77-0)

[innodb\\_monitor\\_enable='latch'](#page-31-1) enables statistics collection for SHOW ENGINE INNODB MUTEX. For more information, see Section 13.7.5.15, "SHOW ENGINE Statement".

<span id="page-31-2"></span>• [innodb\\_monitor\\_reset](#page-31-2)

| Command-Line Format | innodb-monitor-reset={counter <br>module pattern all} |
|---------------------|-------------------------------------------------------|
| System Variable     | innodb_monitor_reset                                  |
| Scope               | Global                                                |
| Dynamic             | Yes                                                   |
| Type                | Enumeration                                           |
| Default Value       | NULL                                                  |
| Valid Values        | counter                                               |
|                     | module                                                |
|                     | pattern                                               |

all

This variable acts as a switch, resetting the count value for InnoDB metrics counters to zero. Counter data may be queried using the Information Schema INNODB\_METRICS table. For usage information, see [Section 14.16.6, "InnoDB INFORMATION\\_SCHEMA Metrics Table".](#page-77-0)

[innodb\\_monitor\\_reset='latch'](#page-31-2) resets statistics reported by SHOW ENGINE INNODB MUTEX. For more information, see Section 13.7.5.15, "SHOW ENGINE Statement".

<span id="page-32-0"></span>• [innodb\\_monitor\\_reset\\_all](#page-32-0)

| Command-Line Format | innodb-monitor-reset-all={counter <br>module pattern all} |
|---------------------|-----------------------------------------------------------|
| System Variable     | innodb_monitor_reset_all                                  |
| Scope               | Global                                                    |
| Dynamic             | Yes                                                       |
| Type                | Enumeration                                               |
| Default Value       | NULL                                                      |
| Valid Values        | counter                                                   |
|                     | module                                                    |
|                     | pattern                                                   |
|                     | all                                                       |

This variable acts as a switch, resetting all values (minimum, maximum, and so on) for InnoDB metrics counters. Counter data may be queried using the Information Schema INNODB\_METRICS table. For usage information, see [Section 14.16.6, "InnoDB INFORMATION\\_SCHEMA Metrics](#page-77-0) [Table"](#page-77-0).

<span id="page-32-1"></span>• [innodb\\_numa\\_interleave](#page-32-1)

| Command-Line Format | innodb-numa-interleave[={OFF ON}] |
|---------------------|-----------------------------------|
| System Variable     | innodb_numa_interleave            |
| Scope               | Global                            |
| Dynamic             | No                                |
| Type                | Boolean                           |
| Default Value       | OFF                               |

Enables the NUMA interleave memory policy for allocation of the InnoDB buffer pool. When [innodb\\_numa\\_interleave](#page-32-1) is enabled, the NUMA memory policy is set to MPOL\_INTERLEAVE for the mysqld process. After the InnoDB buffer pool is allocated, the NUMA memory policy is set back to MPOL\_DEFAULT. For the [innodb\\_numa\\_interleave](#page-32-1) option to be available, MySQL must be compiled on a NUMA-enabled Linux system.

As of MySQL 5.7.17, CMake sets the default WITH\_NUMA value based on whether the current platform has NUMA support. For more information, see Section 2.8.7, "MySQL Source-Configuration Options".

<span id="page-32-2"></span>• [innodb\\_old\\_blocks\\_pct](#page-32-2)

| Command-Line Format | innodb-old-blocks-pct=# |
|---------------------|-------------------------|
| System Variable     | innodb_old_blocks_pct   |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | Yes     |
| Type          | Integer |
| Default Value | 37      |
| Minimum Value | 5       |
| Maximum Value | 95      |

Specifies the approximate percentage of the InnoDB buffer pool used for the old block sublist. The range of values is 5 to 95. The default value is 37 (that is, 3/8 of the pool). Often used in combination with [innodb\\_old\\_blocks\\_time](#page-33-0).

For more information, see Section 14.8.3.3, "Making the Buffer Pool Scan Resistant". For information about buffer pool management, the LRU algorithm, and eviction policies, see Section 14.5.1, "Buffer Pool".

<span id="page-33-0"></span>• [innodb\\_old\\_blocks\\_time](#page-33-0)

| Command-Line Format | innodb-old-blocks-time=# |
|---------------------|--------------------------|
| System Variable     | innodb_old_blocks_time   |
| Scope               | Global                   |
| Dynamic             | Yes                      |
| Type                | Integer                  |
| Default Value       | 1000                     |
| Minimum Value       | 0                        |
| Maximum Value       | 2**32-1                  |
| Unit                | milliseconds             |

Non-zero values protect against the buffer pool being filled by data that is referenced only for a brief period, such as during a full table scan. Increasing this value offers more protection against full table scans interfering with data cached in the buffer pool.

Specifies how long in milliseconds a block inserted into the old sublist must stay there after its first access before it can be moved to the new sublist. If the value is 0, a block inserted into the old sublist moves immediately to the new sublist the first time it is accessed, no matter how soon after insertion the access occurs. If the value is greater than 0, blocks remain in the old sublist until an access occurs at least that many milliseconds after the first access. For example, a value of 1000 causes blocks to stay in the old sublist for 1 second after the first access before they become eligible to move to the new sublist.

The default value is 1000.

This variable is often used in combination with [innodb\\_old\\_blocks\\_pct](#page-32-2). For more information, see Section 14.8.3.3, "Making the Buffer Pool Scan Resistant". For information about buffer pool management, the LRU algorithm, and eviction policies, see Section 14.5.1, "Buffer Pool".

<span id="page-33-1"></span>• [innodb\\_online\\_alter\\_log\\_max\\_size](#page-33-1)

| Command-Line Format | innodb-online-alter-log-max-size=# |
|---------------------|------------------------------------|
| System Variable     | innodb_online_alter_log_max_size   |
| Scope               | Global                             |
| Dynamic             | Yes                                |
| Type                | Integer                            |

| Default Value | 134217728 |
|---------------|-----------|
| Minimum Value | 65536     |
| Maximum Value | 2**64-1   |
| Unit          | bytes     |

Specifies an upper limit in bytes on the size of the temporary log files used during online DDL operations for InnoDB tables. There is one such log file for each index being created or table being altered. This log file stores data inserted, updated, or deleted in the table during the DDL operation. The temporary log file is extended when needed by the value of [innodb\\_sort\\_buffer\\_size](#page-41-1), up to the maximum specified by [innodb\\_online\\_alter\\_log\\_max\\_size](#page-33-1). If a temporary log file exceeds the upper size limit, the ALTER TABLE operation fails and all uncommitted concurrent DML operations are rolled back. Thus, a large value for this option allows more DML to happen during an online DDL operation, but also extends the period of time at the end of the DDL operation when the table is locked to apply the data from the log.

<span id="page-34-0"></span>• [innodb\\_open\\_files](#page-34-0)

| Command-Line Format | innodb-open-files=#                                            |
|---------------------|----------------------------------------------------------------|
| System Variable     | innodb_open_files                                              |
| Scope               | Global                                                         |
| Dynamic             | No                                                             |
| Type                | Integer                                                        |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value       | 10                                                             |
| Maximum Value       | 2147483647                                                     |

Specifies the maximum number of files that InnoDB can have open at one time. The minimum value is 10. If [innodb\\_file\\_per\\_table](#page-9-1) is disabled, the default value is 300; otherwise, the default value is 300 or the table\_open\_cache setting, whichever is higher.

<span id="page-34-1"></span>• [innodb\\_optimize\\_fulltext\\_only](#page-34-1)

| Command-Line Format | innodb-optimize-fulltext<br>only[={OFF ON}] |
|---------------------|---------------------------------------------|
| System Variable     | innodb_optimize_fulltext_only               |
| Scope               | Global                                      |
| Dynamic             | Yes                                         |
| Type                | Boolean                                     |
| Default Value       | OFF                                         |

Changes the way OPTIMIZE TABLE operates on InnoDB tables. Intended to be enabled temporarily, during maintenance operations for InnoDB tables with FULLTEXT indexes.

By default, OPTIMIZE TABLE reorganizes data in the clustered index of the table. When this option is enabled, OPTIMIZE TABLE skips the reorganization of table data, and instead processes newly added, deleted, and updated token data for InnoDB FULLTEXT indexes. For more information, see Optimizing InnoDB Full-Text Indexes.

<span id="page-34-2"></span>• [innodb\\_page\\_cleaners](#page-34-2)

| Command-Line Format | innodb-page-cleaners=# |
|---------------------|------------------------|
|                     |                        |
|                     |                        |

| System Variable | innodb_page_cleaners |
|-----------------|----------------------|
| Scope           | Global               |
| Dynamic         | No                   |
| Type            | Integer              |
| Default Value   | 4                    |
| Minimum Value   | 1                    |
| Maximum Value   | 64                   |

The number of page cleaner threads that flush dirty pages from buffer pool instances. Page cleaner threads perform flush list and LRU flushing. A single page cleaner thread was introduced in MySQL 5.6 to offload buffer pool flushing work from the InnoDB master thread. In MySQL 5.7, InnoDB provides support for multiple page cleaner threads. A value of 1 maintains the pre-MySQL 5.7 configuration in which there is a single page cleaner thread. When there are multiple page cleaner threads, buffer pool flushing tasks for each buffer pool instance are dispatched to idle page cleaner threads. The [innodb\\_page\\_cleaners](#page-34-2) default value was changed from 1 to 4 in MySQL 5.7. If the number of page cleaner threads exceeds the number of buffer pool instances, [innodb\\_page\\_cleaners](#page-34-2) is automatically set to the same value as innodb\_buffer\_pool\_instances.

If your workload is write-IO bound when flushing dirty pages from buffer pool instances to data files, and if your system hardware has available capacity, increasing the number of page cleaner threads may help improve write-IO throughput.

Multithreaded page cleaner support is extended to shutdown and recovery phases in MySQL 5.7.

The setpriority() system call is used on Linux platforms where it is supported, and where the mysqld execution user is authorized to give page\_cleaner threads priority over other MySQL and InnoDB threads to help page flushing keep pace with the current workload. setpriority() support is indicated by this InnoDB startup message:

```
[Note] InnoDB: If the mysqld execution user is authorized, page cleaner
thread priority can be changed. See the man page of setpriority().
```

For systems where server startup and shutdown is not managed by systemd, mysqld execution user authorization can be configured in /etc/security/limits.conf. For example, if mysqld is run under the mysql user, you can authorize the mysql user by adding these lines to /etc/ security/limits.conf:

```
mysql hard nice -20
mysql soft nice -20
```

For systemd managed systems, the same can be achieved by specifying LimitNICE=-20 in a localized systemd configuration file. For example, create a file named override.conf in /etc/ systemd/system/mysqld.service.d/override.conf and add this entry:

```
[Service]
LimitNICE=-20
```

After creating or changing override.conf, reload the systemd configuration, then tell systemd to restart the MySQL service:

```
systemctl daemon-reload
systemctl restart mysqld # RPM platforms
```

```
systemctl restart mysql # Debian platforms
```

For more information about using a localized systemd configuration file, see Configuring systemd for MySQL.

After authorizing the mysqld execution user, use the cat command to verify the configured Nice limits for the mysqld process:

```
$> cat /proc/mysqld_pid/limits | grep nice
Max nice priority 18446744073709551596 18446744073709551596
```

<span id="page-36-0"></span>• [innodb\\_page\\_size](#page-36-0)

| Command-Line Format | innodb-page-size=# |
|---------------------|--------------------|
| System Variable     | innodb_page_size   |
| Scope               | Global             |
| Dynamic             | No                 |
| Type                | Enumeration        |
| Default Value       | 16384              |
| Valid Values        | 4096               |
|                     | 8192               |
|                     | 16384              |
|                     | 32768              |
|                     | 65536              |

Specifies the page size for InnoDB tablespaces. Values can be specified in bytes or kilobytes. For example, a 16 kilobyte page size value can be specified as 16384, 16KB, or 16k.

[innodb\\_page\\_size](#page-36-0) can only be configured prior to initializing the MySQL instance and cannot be changed afterward. If no value is specified, the instance is initialized using the default page size. See Section 14.8.1, "InnoDB Startup Configuration".

Support for 32KB and 64KB page sizes was added in MySQL 5.7. For both 32KB and 64KB page sizes, the maximum row length is approximately 16000 bytes. ROW\_FORMAT=COMPRESSED is not supported when [innodb\\_page\\_size](#page-36-0) is set to 32KB or 64KB. For [innodb\\_page\\_size=32k](#page-36-0), extent size is 2MB. For [innodb\\_page\\_size=64KB](#page-36-0), extent size is 4MB. [innodb\\_log\\_buffer\\_size](#page-25-0) should be set to at least 16M (the default) when using 32KB or 64KB page sizes.

The default 16KB page size or larger is appropriate for a wide range of workloads, particularly for queries involving table scans and DML operations involving bulk updates. Smaller page sizes might be more efficient for OLTP workloads involving many small writes, where contention can be an issue when single pages contain many rows. Smaller pages might also be efficient with SSD storage devices, which typically use small block sizes. Keeping the InnoDB page size close to the storage device block size minimizes the amount of unchanged data that is rewritten to disk.

The minimum file size for the first system tablespace data file (ibdata1) differs depending on the [innodb\\_page\\_size](#page-36-0) value. See the [innodb\\_data\\_file\\_path](#page-4-0) option description for more information.

A MySQL instance using a particular InnoDB page size cannot use data files or log files from an instance that uses a different page size.

For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-37-0"></span>• [innodb\\_print\\_all\\_deadlocks](#page-37-0)

| Command-Line Format | innodb-print-all-deadlocks[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | innodb_print_all_deadlocks                |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Boolean                                   |
| Default Value       | OFF                                       |

When this option is enabled, information about all deadlocks in InnoDB user transactions is recorded in the mysqld error log. Otherwise, you see information about only the last deadlock, using the SHOW ENGINE INNODB STATUS command. An occasional InnoDB deadlock is not necessarily an issue, because InnoDB detects the condition immediately and rolls back one of the transactions automatically. You might use this option to troubleshoot why deadlocks are occurring if an application does not have appropriate error-handling logic to detect the rollback and retry its operation. A large number of deadlocks might indicate the need to restructure transactions that issue DML or SELECT ... FOR UPDATE statements for multiple tables, so that each transaction accesses the tables in the same order, thus avoiding the deadlock condition.

For related information, see Section 14.7.5, "Deadlocks in InnoDB".

<span id="page-37-1"></span>• [innodb\\_purge\\_batch\\_size](#page-37-1)

| Command-Line Format | innodb-purge-batch-size=# |
|---------------------|---------------------------|
| System Variable     | innodb_purge_batch_size   |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Integer                   |
| Default Value       | 300                       |
| Minimum Value       | 1                         |
| Maximum Value       | 5000                      |

Defines the number of undo log pages that purge parses and processes in one batch from the history list. In a multithreaded purge configuration, the coordinator purge thread divides [innodb\\_purge\\_batch\\_size](#page-37-1) by [innodb\\_purge\\_threads](#page-37-2) and assigns that number of pages to each purge thread. The [innodb\\_purge\\_batch\\_size](#page-37-1) variable also defines the number of undo log pages that purge frees after every 128 iterations through the undo logs.

The [innodb\\_purge\\_batch\\_size](#page-37-1) option is intended for advanced performance tuning in combination with the [innodb\\_purge\\_threads](#page-37-2) setting. Most users need not change [innodb\\_purge\\_batch\\_size](#page-37-1) from its default value.

For related information, see Section 14.8.10, "Purge Configuration".

<span id="page-37-2"></span>• [innodb\\_purge\\_threads](#page-37-2)

| Command-Line Format | innodb-purge-threads=# |
|---------------------|------------------------|
| System Variable     | innodb_purge_threads   |
| Scope               | Global                 |
| Dynamic             | No                     |
| Type                | Integer                |

| Default Value | 4  |
|---------------|----|
| Minimum Value | 1  |
| Maximum Value | 32 |

The number of background threads devoted to the InnoDB purge operation. Increasing the value creates additional purge threads, which can improve efficiency on systems where DML operations are performed on multiple tables.

For related information, see Section 14.8.10, "Purge Configuration".

<span id="page-38-0"></span>• [innodb\\_purge\\_rseg\\_truncate\\_frequency](#page-38-0)

| Command-Line Format | innodb-purge-rseg-truncate<br>frequency=# |
|---------------------|-------------------------------------------|
| System Variable     | innodb_purge_rseg_truncate_frequency      |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Integer                                   |
| Default Value       | 128                                       |
| Minimum Value       | 1                                         |
| Maximum Value       | 128                                       |

Defines the frequency with which the purge system frees rollback segments in terms of the number of times that purge is invoked. An undo tablespace cannot be truncated until its rollback segments are freed. Normally, the purge system frees rollback segments once every 128 times that purge is invoked. The default value is 128. Reducing this value increases the frequency with which the purge thread frees rollback segments.

[innodb\\_purge\\_rseg\\_truncate\\_frequency](#page-38-0) is intended for use with [innodb\\_undo\\_log\\_truncate](#page-53-0). For more information, see Truncating Undo Tablespaces.

<span id="page-38-1"></span>• [innodb\\_random\\_read\\_ahead](#page-38-1)

| Command-Line Format | innodb-random-read-ahead[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_random_read_ahead                |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | Boolean                                 |
| Default Value       | OFF                                     |

Enables the random read-ahead technique for optimizing InnoDB I/O.

For details about performance considerations for different types of read-ahead requests, see Section 14.8.3.4, "Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-38-2"></span>• [innodb\\_read\\_ahead\\_threshold](#page-38-2)

| Command-Line Format | innodb-read-ahead-threshold=# |
|---------------------|-------------------------------|
| System Variable     | innodb_read_ahead_threshold   |
| Scope               | Global<br>2611                |

| Dynamic       | Yes     |
|---------------|---------|
| Type          | Integer |
| Default Value | 56      |
| Minimum Value | 0       |
| Maximum Value | 64      |

Controls the sensitivity of linear read-ahead that InnoDB uses to prefetch pages into the buffer pool. If InnoDB reads at least [innodb\\_read\\_ahead\\_threshold](#page-38-2) pages sequentially from an extent (64 pages), it initiates an asynchronous read for the entire following extent. The permissible range of values is 0 to 64. A value of 0 disables read-ahead. For the default of 56, InnoDB must read at least 56 pages sequentially from an extent to initiate an asynchronous read for the following extent.

Knowing how many pages are read through the read-ahead mechanism, and how many of these pages are evicted from the buffer pool without ever being accessed, can be useful when fine-tuning the [innodb\\_read\\_ahead\\_threshold](#page-38-2) setting. SHOW ENGINE INNODB STATUS output displays counter information from the Innodb\_buffer\_pool\_read\_ahead and Innodb\_buffer\_pool\_read\_ahead\_evicted global status variables, which report the number of pages brought into the buffer pool by read-ahead requests, and the number of such pages evicted from the buffer pool without ever being accessed, respectively. The status variables report global values since the last server restart.

SHOW ENGINE INNODB STATUS also shows the rate at which the read-ahead pages are read and the rate at which such pages are evicted without being accessed. The per-second averages are based on the statistics collected since the last invocation of SHOW ENGINE INNODB STATUS and are displayed in the BUFFER POOL AND MEMORY section of the SHOW ENGINE INNODB STATUS output.

For more information, see Section 14.8.3.4, "Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

<span id="page-39-0"></span>• [innodb\\_read\\_io\\_threads](#page-39-0)

| Command-Line Format | innodb-read-io-threads=# |
|---------------------|--------------------------|
| System Variable     | innodb_read_io_threads   |
| Scope               | Global                   |
| Dynamic             | No                       |
| Type                | Integer                  |
| Default Value       | 4                        |
| Minimum Value       | 1                        |
| Maximum Value       | 64                       |

The number of I/O threads for read operations in InnoDB. Its counterpart for write threads is [innodb\\_write\\_io\\_threads](#page-56-0). For more information, see Section 14.8.6, "Configuring the Number of Background InnoDB I/O Threads". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

![](_page_39_Picture_9.jpeg)

### **Note**

On Linux systems, running multiple MySQL servers (typically more than 12) with default settings for [innodb\\_read\\_io\\_threads](#page-39-0), [innodb\\_write\\_io\\_threads](#page-56-0), and the Linux aio-max-nr setting can exceed system limits. Ideally, increase the aio-max-nr setting; as a workaround, you might reduce the settings for one or both of the MySQL variables.

### <span id="page-40-1"></span>• [innodb\\_read\\_only](#page-40-1)

| Command-Line Format | innodb-read-only[={OFF ON}] |
|---------------------|-----------------------------|
| System Variable     | innodb_read_only            |
| Scope               | Global                      |
| Dynamic             | No                          |
| Type                | Boolean                     |
| Default Value       | OFF                         |

Starts InnoDB in read-only mode. For distributing database applications or data sets on read-only media. Can also be used in data warehouses to share the same data directory between multiple instances. For more information, see Section 14.8.2, "Configuring InnoDB for Read-Only Operation".

### <span id="page-40-2"></span>• [innodb\\_replication\\_delay](#page-40-2)

| Command-Line Format | innodb-replication-delay=# |
|---------------------|----------------------------|
| System Variable     | innodb_replication_delay   |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 0                          |
| Minimum Value       | 0                          |
| Maximum Value       | 4294967295                 |
| Unit                | milliseconds               |

The replication thread delay in milliseconds on a replica server if [innodb\\_thread\\_concurrency](#page-50-0) is reached.

### <span id="page-40-0"></span>• [innodb\\_rollback\\_on\\_timeout](#page-40-0)

| Command-Line Format | innodb-rollback-on-timeout[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | innodb_rollback_on_timeout                |
| Scope               | Global                                    |
| Dynamic             | No                                        |
| Type                | Boolean                                   |
| Default Value       | OFF                                       |

InnoDB rolls back only the last statement on a transaction timeout by default. If [--innodb](#page-40-0)[rollback-on-timeout](#page-40-0) is specified, a transaction timeout causes InnoDB to abort and roll back the entire transaction.

For more information, see [Section 14.22.4, "InnoDB Error Handling".](#page-146-1)

### <span id="page-40-3"></span>• [innodb\\_rollback\\_segments](#page-40-3)

| Command-Line Format | innodb-rollback-segments=# |
|---------------------|----------------------------|
| System Variable     | innodb_rollback_segments   |
| Scope               | Global                     |
| Dynamic             | 2613<br>Yes                |

| Type          | Integer |
|---------------|---------|
| Default Value | 128     |
| Minimum Value | 1       |
| Maximum Value | 128     |

Defines the number of rollback segments used by InnoDB for transactions that generate undo records. The number of transactions that each rollback segment supports depends on the InnoDB page size and the number of undo logs assigned to each transaction. For more information, see Section 14.6.7, "Undo Logs".

One rollback segment is always assigned to the system tablespace, and 32 rollback segments are reserved for use by temporary tables and reside in the temporary tablespace (ibtmp1). To allocate additional rollback segment, [innodb\\_rollback\\_segments](#page-40-3) must be set to a value greater than 33. If you configure separate undo tablespaces, the rollback segment in the system tablespace is rendered inactive.

When [innodb\\_rollback\\_segments](#page-40-3) is set to 32 or less, InnoDB assigns one rollback segment to the system tablespace and 32 to the temporary tablespace.

When [innodb\\_rollback\\_segments](#page-40-3) is set to a value greater than 32, InnoDB assigns one rollback segment to the system tablespace, 32 to the temporary tablespace, and additional rollback segments to undo tablespaces, if present. If undo tablespaces are not present, additional rollback segments are assigned to the system tablespace.

Although you can increase or decrease the number of rollback segments used by InnoDB, the number of rollback segments physically present in the system never decreases. Thus, you might start with a low value and gradually increase it to avoid allocating rollback segments that are not required. The [innodb\\_rollback\\_segments](#page-40-3) default and maximum value is 128.

For related information, see Section 14.3, "InnoDB Multi-Versioning". For information about configuring separate undo tablespaces, see Section 14.6.3.4, "Undo Tablespaces".

<span id="page-41-0"></span>• [innodb\\_saved\\_page\\_number\\_debug](#page-41-0)

| Command-Line Format | innodb-saved-page-number-debug=# |
|---------------------|----------------------------------|
| System Variable     | innodb_saved_page_number_debug   |
| Scope               | Global                           |
| Dynamic             | Yes                              |
| Type                | Integer                          |
| Default Value       | 0                                |
| Minimum Value       | 0                                |
| Maximum Value       | 2**32-1                          |

Saves a page number. Setting the [innodb\\_fil\\_make\\_page\\_dirty\\_debug](#page-7-0) option dirties the page defined by [innodb\\_saved\\_page\\_number\\_debug](#page-41-0). The [innodb\\_saved\\_page\\_number\\_debug](#page-41-0) option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-41-1"></span>• [innodb\\_sort\\_buffer\\_size](#page-41-1)

| Command-Line Format | innodb-sort-buffer-size=# |
|---------------------|---------------------------|
| System Variable     | innodb_sort_buffer_size   |
| Scope               | Global                    |
| Dynamic             | No                        |

| Type          | Integer  |
|---------------|----------|
| Default Value | 1048576  |
| Minimum Value | 65536    |
| Maximum Value | 67108864 |
| Unit          | bytes    |

#### This variable defines:

- The sort buffer size for online DDL operations that create or rebuild secondary indexes.
- The amount by which the temporary log file is extended when recording concurrent DML during an online DDL operation, and the size of the temporary log file read buffer and write buffer.

For related information, see Section 14.13.3, "Online DDL Space Requirements".

<span id="page-42-0"></span>• [innodb\\_spin\\_wait\\_delay](#page-42-0)

| Command-Line Format              | innodb-spin-wait-delay=# |
|----------------------------------|--------------------------|
| System Variable                  | innodb_spin_wait_delay   |
| Scope                            | Global                   |
| Dynamic                          | Yes                      |
| Type                             | Integer                  |
| Default Value                    | 6                        |
| Minimum Value                    | 0                        |
| Maximum Value (64-bit platforms) | 2**64-1                  |
| Maximum Value (32-bit platforms) | 2**32-1                  |

The maximum delay between polls for a spin lock. The low-level implementation of this mechanism varies depending on the combination of hardware and operating system, so the delay does not correspond to a fixed time interval. For more information, see Section 14.8.9, "Configuring Spin Lock Polling".

<span id="page-42-1"></span>• [innodb\\_stats\\_auto\\_recalc](#page-42-1)

| Command-Line Format | innodb-stats-auto-recalc[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_stats_auto_recalc                |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | Boolean                                 |
| Default Value       | ON                                      |

Causes InnoDB to automatically recalculate persistent statistics after the data in a table is changed substantially. The threshold value is 10% of the rows in the table. This setting applies to tables created when the [innodb\\_stats\\_persistent](#page-44-0) option is enabled. Automatic statistics recalculation may also be configured by specifying STATS\_AUTO\_RECALC=1 in a CREATE TABLE or ALTER TABLE statement. The amount of data sampled to produce the statistics is controlled by the [innodb\\_stats\\_persistent\\_sample\\_pages](#page-44-1) variable.

For more information, see Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters".

<span id="page-42-2"></span>• [innodb\\_stats\\_include\\_delete\\_marked](#page-42-2)

| Command-Line Format | innodb-stats-include-delete<br>marked[={OFF ON}] |
|---------------------|--------------------------------------------------|
| System Variable     | innodb_stats_include_delete_marked               |
| Scope               | Global                                           |
| Dynamic             | Yes                                              |
| Type                | Boolean                                          |
| Default Value       | OFF                                              |

By default, InnoDB reads uncommitted data when calculating statistics. In the case of an uncommitted transaction that deletes rows from a table, InnoDB excludes records that are delete-marked when calculating row estimates and index statistics, which can lead to nonoptimal execution plans for other transactions that are operating on the table concurrently using a transaction isolation level other than READ UNCOMMITTED. To avoid this scenario, [innodb\\_stats\\_include\\_delete\\_marked](#page-42-2) can be enabled to ensure that InnoDB includes delete-marked records when calculating persistent optimizer statistics.

When [innodb\\_stats\\_include\\_delete\\_marked](#page-42-2) is enabled, ANALYZE TABLE considers deletemarked records when recalculating statistics.

[innodb\\_stats\\_include\\_delete\\_marked](#page-42-2) is a global setting that affects all InnoDB tables. It is only applicable to persistent optimizer statistics.

For related information, see Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters".

### <span id="page-43-0"></span>• [innodb\\_stats\\_method](#page-43-0)

| Command-Line Format | innodb-stats-method=value |
|---------------------|---------------------------|
| System Variable     | innodb_stats_method       |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Enumeration               |
| Default Value       | nulls_equal               |
| Valid Values        | nulls_equal               |
|                     | nulls_unequal             |
|                     | nulls_ignored             |

How the server treats NULL values when collecting statistics about the distribution of index values for InnoDB tables. Permitted values are nulls\_equal, nulls\_unequal, and nulls\_ignored. For nulls\_equal, all NULL index values are considered equal and form a single value group with a size equal to the number of NULL values. For nulls\_unequal, NULL values are considered unequal, and each NULL forms a distinct value group of size 1. For nulls\_ignored, NULL values are ignored.

The method used to generate table statistics influences how the optimizer chooses indexes for query execution, as described in Section 8.3.7, "InnoDB and MyISAM Index Statistics Collection".

### <span id="page-43-1"></span>• [innodb\\_stats\\_on\\_metadata](#page-43-1)

| Command-Line Format | innodb-stats-on-metadata[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_stats_on_metadata                |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | Yes     |
| Type          | Boolean |
| Default Value | OFF     |

This option only applies when optimizer statistics are configured to be non-persistent. Optimizer statistics are not persisted to disk when [innodb\\_stats\\_persistent](#page-44-0) is disabled or when individual tables are created or altered with STATS\_PERSISTENT=0. For more information, see Section 14.8.11.2, "Configuring Non-Persistent Optimizer Statistics Parameters".

When [innodb\\_stats\\_on\\_metadata](#page-43-1) is enabled, InnoDB updates non-persistent statistics when metadata statements such as SHOW TABLE STATUS or when accessing the Information Schema TABLES or STATISTICS tables. (These updates are similar to what happens for ANALYZE TABLE.) When disabled, InnoDB does not update statistics during these operations. Leaving the setting disabled can improve access speed for schemas that have a large number of tables or indexes. It can also improve the stability of execution plans for queries that involve InnoDB tables.

To change the setting, issue the statement SET GLOBAL innodb\_stats\_on\_metadata=mode, where mode is either ON or OFF (or 1 or 0). Changing the setting requires privileges sufficient to set global system variables (see Section 5.1.8.1, "System Variable Privileges") and immediately affects the operation of all connections.

<span id="page-44-0"></span>• [innodb\\_stats\\_persistent](#page-44-0)

| Command-Line Format | innodb-stats-persistent[={OFF ON}] |
|---------------------|------------------------------------|
| System Variable     | innodb_stats_persistent            |
| Scope               | Global                             |
| Dynamic             | Yes                                |
| Type                | Boolean                            |
| Default Value       | ON                                 |

Specifies whether InnoDB index statistics are persisted to disk. Otherwise, statistics may be recalculated frequently which can lead to variations in query execution plans. This setting is stored with each table when the table is created. You can set [innodb\\_stats\\_persistent](#page-44-0) at the global level before creating a table, or use the STATS\_PERSISTENT clause of the CREATE TABLE and ALTER TABLE statements to override the system-wide setting and configure persistent statistics for individual tables.

For more information, see Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters".

<span id="page-44-1"></span>• [innodb\\_stats\\_persistent\\_sample\\_pages](#page-44-1)

| Command-Line Format | innodb-stats-persistent-sample<br>pages=# |
|---------------------|-------------------------------------------|
| System Variable     | innodb_stats_persistent_sample_pages      |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Integer                                   |
| Default Value       | 20                                        |
| Minimum Value       | 1                                         |

| Maximum Value | 18446744073709551615 |
|---------------|----------------------|
|---------------|----------------------|

The number of index pages to sample when estimating cardinality and other statistics for an indexed column, such as those calculated by ANALYZE TABLE. Increasing the value improves the accuracy of index statistics, which can improve the query execution plan, at the expense of increased I/O during the execution of ANALYZE TABLE for an InnoDB table. For more information, see Section 14.8.11.1, "Configuring Persistent Optimizer Statistics Parameters".

![](_page_45_Picture_3.jpeg)

#### **Note**

Setting a high value for [innodb\\_stats\\_persistent\\_sample\\_pages](#page-44-1) could result in lengthy ANALYZE TABLE execution time. To estimate the number of database pages accessed by ANALYZE TABLE, see Section 14.8.11.3, "Estimating ANALYZE TABLE Complexity for InnoDB Tables".

[innodb\\_stats\\_persistent\\_sample\\_pages](#page-44-1) only applies when [innodb\\_stats\\_persistent](#page-44-0) is enabled for a table; when [innodb\\_stats\\_persistent](#page-44-0) is disabled, [innodb\\_stats\\_transient\\_sample\\_pages](#page-45-0) applies instead.

<span id="page-45-1"></span>• [innodb\\_stats\\_sample\\_pages](#page-45-1)

| Command-Line Format | innodb-stats-sample-pages=# |
|---------------------|-----------------------------|
| Deprecated          | Yes                         |
| System Variable     | innodb_stats_sample_pages   |
| Scope               | Global                      |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 8                           |
| Minimum Value       | 1                           |
| Maximum Value       | 2**64-1                     |

Deprecated. Use [innodb\\_stats\\_transient\\_sample\\_pages](#page-45-0) instead.

<span id="page-45-0"></span>• [innodb\\_stats\\_transient\\_sample\\_pages](#page-45-0)

| Command-Line Format | innodb-stats-transient-sample<br>pages=# |
|---------------------|------------------------------------------|
| System Variable     | innodb_stats_transient_sample_pages      |
| Scope               | Global                                   |
| Dynamic             | Yes                                      |
| Type                | Integer                                  |
| Default Value       | 8                                        |
| Minimum Value       | 1                                        |
| Maximum Value       | 18446744073709551615                     |

The number of index pages to sample when estimating cardinality and other statistics for an indexed column, such as those calculated by ANALYZE TABLE. The default value is 8. Increasing the value improves the accuracy of index statistics, which can improve the query execution plan, at

the expense of increased I/O when opening an InnoDB table or recalculating statistics. For more information, see Section 14.8.11.2, "Configuring Non-Persistent Optimizer Statistics Parameters".

![](_page_46_Picture_2.jpeg)

### **Note**

Setting a high value for [innodb\\_stats\\_transient\\_sample\\_pages](#page-45-0) could result in lengthy ANALYZE TABLE execution time. To estimate the number of database pages accessed by ANALYZE TABLE, see Section 14.8.11.3, "Estimating ANALYZE TABLE Complexity for InnoDB Tables".

[innodb\\_stats\\_transient\\_sample\\_pages](#page-45-0) only applies when [innodb\\_stats\\_persistent](#page-44-0) is disabled for a table; when [innodb\\_stats\\_persistent](#page-44-0) is enabled, [innodb\\_stats\\_persistent\\_sample\\_pages](#page-44-1) applies instead. Takes the place of [innodb\\_stats\\_sample\\_pages](#page-45-1). For more information, see Section 14.8.11.2, "Configuring Non-Persistent Optimizer Statistics Parameters".

<span id="page-46-0"></span>• [innodb\\_status\\_output](#page-46-0)

| Command-Line Format | innodb-status-output[={OFF ON}] |
|---------------------|---------------------------------|
| System Variable     | innodb_status_output            |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Boolean                         |
| Default Value       | OFF                             |

Enables or disables periodic output for the standard InnoDB Monitor. Also used in combination with [innodb\\_status\\_output\\_locks](#page-46-1) to enable or disable periodic output for the InnoDB Lock Monitor. For more information, see [Section 14.18.2, "Enabling InnoDB Monitors"](#page-95-0).

<span id="page-46-1"></span>• [innodb\\_status\\_output\\_locks](#page-46-1)

| Command-Line Format | innodb-status-output-locks[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | innodb_status_output_locks                |
| Scope               | Global                                    |
| Dynamic             | Yes                                       |
| Type                | Boolean                                   |
| Default Value       | OFF                                       |

Enables or disables the InnoDB Lock Monitor. When enabled, the InnoDB Lock Monitor prints additional information about locks in SHOW ENGINE INNODB STATUS output and in periodic output printed to the MySQL error log. Periodic output for the InnoDB Lock Monitor is printed as part of the standard InnoDB Monitor output. The standard InnoDB Monitor must therefore be enabled for the InnoDB Lock Monitor to print data to the MySQL error log periodically. For more information, see [Section 14.18.2, "Enabling InnoDB Monitors".](#page-95-0)

<span id="page-46-2"></span>• [innodb\\_strict\\_mode](#page-46-2)

| Command-Line Format | innodb-strict-mode[={OFF ON}] |
|---------------------|-------------------------------|
| System Variable     | innodb_strict_mode            |
| Scope               | Global, Session               |
| Dynamic             | Yes                           |
| Type                | Boolean<br>2619               |

| Default Value | ON |
|---------------|----|
|---------------|----|

When [innodb\\_strict\\_mode](#page-46-2) is enabled, InnoDB returns errors rather than warnings when checking for invalid or incompatible table options.

It checks that KEY\_BLOCK\_SIZE, ROW\_FORMAT, DATA DIRECTORY, TEMPORARY, and TABLESPACE options are compatible with each other and other settings.

innodb\_strict\_mode=ON also enables a row size check when creating or altering a table, to prevent INSERT or UPDATE from failing due to the record being too large for the selected page size.

You can enable or disable [innodb\\_strict\\_mode](#page-46-2) on the command line when starting mysqld, or in a MySQL configuration file. You can also enable or disable [innodb\\_strict\\_mode](#page-46-2) at runtime with the statement SET [GLOBAL|SESSION] innodb\_strict\_mode=mode, where mode is either ON or OFF. Changing the GLOBAL setting requires privileges sufficient to set global system variables (see Section 5.1.8.1, "System Variable Privileges") and affects the operation of all clients that subsequently connect. Any client can change the SESSION setting for [innodb\\_strict\\_mode](#page-46-2), and the setting affects only that client.

<span id="page-47-0"></span>• [innodb\\_support\\_xa](#page-47-0)

| Command-Line Format | innodb-support-xa[={OFF ON}] |
|---------------------|------------------------------|
| Deprecated          | Yes                          |
| System Variable     | innodb_support_xa            |
| Scope               | Global, Session              |
| Dynamic             | Yes                          |
| Type                | Boolean                      |
| Default Value       | ON                           |

Enables InnoDB support for two-phase commit in XA transactions, causing an extra disk flush for transaction preparation. The XA mechanism is used internally and is essential for any server that has its binary log turned on and is accepting changes to its data from more than one thread. If you disable [innodb\\_support\\_xa](#page-47-0), transactions can be written to the binary log in a different order than the live database is committing them, which can produce different data when the binary log is replayed in disaster recovery or on a replica. Do not disable [innodb\\_support\\_xa](#page-47-0) on a replication source server unless you have an unusual setup where only one thread is able to change data.

[innodb\\_support\\_xa](#page-47-0) is deprecated; expect it to be removed in a future MySQL release. InnoDB support for two-phase commit in XA transactions is always enabled as of MySQL 5.7.10. Disabling [innodb\\_support\\_xa](#page-47-0) is no longer permitted as it makes replication unsafe and prevents performance gains associated with binary log group commit.

<span id="page-47-1"></span>• [innodb\\_sync\\_array\\_size](#page-47-1)

| Command-Line Format | innodb-sync-array-size=# |
|---------------------|--------------------------|
| System Variable     | innodb_sync_array_size   |
| Scope               | Global                   |
| Dynamic             | No                       |
| Type                | Integer                  |
| Default Value       | 1                        |
| Minimum Value       | 1                        |

| Maximum Value | 1024 |  |
|---------------|------|--|
|---------------|------|--|

Defines the size of the mutex/lock wait array. Increasing the value splits the internal data structure used to coordinate threads, for higher concurrency in workloads with large numbers of waiting threads. This setting must be configured when the MySQL instance is starting up, and cannot be changed afterward. Increasing the value is recommended for workloads that frequently produce a large number of waiting threads, typically greater than 768.

<span id="page-48-0"></span>• [innodb\\_sync\\_spin\\_loops](#page-48-0)

| Command-Line Format | innodb-sync-spin-loops=# |
|---------------------|--------------------------|
| System Variable     | innodb_sync_spin_loops   |
| Scope               | Global                   |
| Dynamic             | Yes                      |
| Type                | Integer                  |
| Default Value       | 30                       |
| Minimum Value       | 0                        |
| Maximum Value       | 4294967295               |

The number of times a thread waits for an InnoDB mutex to be freed before the thread is suspended.

<span id="page-48-1"></span>• [innodb\\_sync\\_debug](#page-48-1)

| Command-Line Format | innodb-sync-debug[={OFF ON}] |
|---------------------|------------------------------|
| System Variable     | innodb_sync_debug            |
| Scope               | Global                       |
| Dynamic             | No                           |
| Type                | Boolean                      |
| Default Value       | OFF                          |

Enables sync debug checking for the InnoDB storage engine. This option is available only if debugging support is compiled in using the WITH\_DEBUG CMake option.

Previously, enabling InnoDB sync debug checking required that the Debug Sync facility be enabled using the ENABLE\_DEBUG\_SYNC CMake option, which has since been removed. This requirement was removed in MySQL 5.7 with the introduction of this variable.

<span id="page-48-2"></span>• [innodb\\_table\\_locks](#page-48-2)

| Command-Line Format | innodb-table-locks[={OFF ON}] |
|---------------------|-------------------------------|
| System Variable     | innodb_table_locks            |
| Scope               | Global, Session               |
| Dynamic             | Yes                           |
| Type                | Boolean                       |
| Default Value       | ON                            |

If autocommit = 0, InnoDB honors LOCK TABLES; MySQL does not return from LOCK TABLES ... WRITE until all other threads have released all their locks to the table. The default value of [innodb\\_table\\_locks](#page-48-2) is 1, which means that LOCK TABLES causes InnoDB to lock a table internally if autocommit = 0.

[innodb\\_table\\_locks = 0](#page-48-2) has no effect for tables locked explicitly with LOCK TABLES ... WRITE. It does have an effect for tables locked for read or write by LOCK TABLES ... WRITE implicitly (for example, through triggers) or by LOCK TABLES ... READ.

For related information, see Section 14.7, "InnoDB Locking and Transaction Model".

<span id="page-49-0"></span>• [innodb\\_temp\\_data\\_file\\_path](#page-49-0)

| Command-Line Format | innodb-temp-data-file<br>path=file_name |
|---------------------|-----------------------------------------|
| System Variable     | innodb_temp_data_file_path              |
| Scope               | Global                                  |
| Dynamic             | No                                      |
| Type                | String                                  |
| Default Value       | ibtmp1:12M:autoextend                   |

Defines the relative path, name, size, and attributes of InnoDB temporary tablespace data files. If you do not specify a value for [innodb\\_temp\\_data\\_file\\_path](#page-49-0), the default behavior is to create a single, auto-extending data file named ibtmp1 in the MySQL data directory. The initial file size is slightly larger than 12MB.

The full syntax for a temporary tablespace data file specification includes the file name, file size, and autoextend and max attributes:

```
file_name:file_size[:autoextend[:max:max_file_size]]
```

The temporary tablespace data file cannot have the same name as another InnoDB data file. Any inability or error creating a temporary tablespace data file is treated as fatal and server startup is refused. The temporary tablespace has a dynamically generated space ID, which can change on each server restart.

File sizes are specified KB, MB or GB (1024MB) by appending K, M or G to the size value. The sum of the sizes of the files must be slightly larger than 12MB.

The size limit of individual files is determined by your operating system. You can set the file size to more than 4GB on operating systems that support large files. Use of raw disk partitions for temporary tablespace data files is not supported.

The autoextend and max attributes can be used only for the data file that is specified last in the [innodb\\_temp\\_data\\_file\\_path](#page-49-0) setting. For example:

[mysqld]

```
innodb_temp_data_file_path=ibtmp1:50M;ibtmp2:12M:autoextend:max:500M
```

If you specify the autoextend option, InnoDB extends the data file if it runs out of free space. The autoextend increment is 64MB by default. To modify the increment, change the innodb\_autoextend\_increment system variable.

The full directory path for temporary tablespace data files is formed by concatenating the paths defined by [innodb\\_data\\_home\\_dir](#page-4-1) and [innodb\\_temp\\_data\\_file\\_path](#page-49-0).

The temporary tablespace is shared by all non-compressed InnoDB temporary tables. Compressed temporary tables reside in file-per-table tablespace files created in the temporary file directory, which is defined by the tmpdir configuration option.

Before running InnoDB in read-only mode, set [innodb\\_temp\\_data\\_file\\_path](#page-49-0) to a location outside of the data directory. The path must be relative to the data directory. For example:

```
--innodb-temp-data-file-path=../../../tmp/ibtmp1:12M:autoextend
```

Metadata about active InnoDB temporary tables is located in the Information Schema INNODB\_TEMP\_TABLE\_INFO table.

For related information, see Section 14.6.3.5, "The Temporary Tablespace".

<span id="page-50-0"></span>• [innodb\\_thread\\_concurrency](#page-50-0)

| Command-Line Format | innodb-thread-concurrency=# |
|---------------------|-----------------------------|
| System Variable     | innodb_thread_concurrency   |
| Scope               | Global                      |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 0                           |
| Minimum Value       | 0                           |
| Maximum Value       | 1000                        |

Defines the maximum number of threads permitted inside of InnoDB. A value of 0 (the default) is interpreted as infinite concurrency (no limit). This variable is intended for performance tuning on high concurrency systems.

InnoDB tries to keep the number of threads inside InnoDB less than or equal to the [innodb\\_thread\\_concurrency](#page-50-0) limit. Threads waiting for locks are not counted in the number of concurrently executing threads.

The correct setting depends on workload and computing environment. Consider setting this variable if your MySQL instance shares CPU resources with other applications or if your workload or number of concurrent users is growing. Test a range of values to determine the setting that provides the best performance. [innodb\\_thread\\_concurrency](#page-50-0) is a dynamic variable, which permits experimenting with different settings on a live test system. If a particular setting performs poorly, you can quickly set [innodb\\_thread\\_concurrency](#page-50-0) back to 0.

Use the following guidelines to help find and maintain an appropriate setting:

- If the number of concurrent user threads for a workload is consistently small and does not affect performance, set [innodb\\_thread\\_concurrency=0](#page-50-0) (no limit).
- If your workload is consistently heavy or occasionally spikes, set an [innodb\\_thread\\_concurrency](#page-50-0) value and adjust it until you find the number of threads that provides the best performance. For example, suppose that your system typically has 40 to 50 users, but periodically the number increases to 60, 70, or more. Through testing, you find

that performance remains largely stable with a limit of 80 concurrent users. In this case, set [innodb\\_thread\\_concurrency](#page-50-0) to 80.

• If you do not want InnoDB to use more than a certain number of virtual CPUs for user threads (20 virtual CPUs, for example), set [innodb\\_thread\\_concurrency](#page-50-0) to this number (or possibly lower, depending on performance testing). If your goal is to isolate MySQL from other applications, consider binding the mysqld process exclusively to the virtual CPUs. Be aware, however, that exclusive binding can result in non-optimal hardware usage if the mysqld process is not consistently busy. In this case, you can bind the mysqld process to the virtual CPUs but allow other applications to use some or all of the virtual CPUs.

![](_page_51_Picture_3.jpeg)

#### **Note**

From an operating system perspective, using a resource management solution to manage how CPU time is shared among applications may be preferable to binding the mysqld process. For example, you could assign 90% of virtual CPU time to a given application while other critical processes are not running, and scale that value back to 40% when other critical processes are running.

- In some cases, the optimal [innodb\\_thread\\_concurrency](#page-50-0) setting can be smaller than the number of virtual CPUs.
- An [innodb\\_thread\\_concurrency](#page-50-0) value that is too high can cause performance regression due to increased contention on system internals and resources.
- Monitor and analyze your system regularly. Changes to workload, number of users, or computing environment may require that you adjust the [innodb\\_thread\\_concurrency](#page-50-0) setting.

A value of 0 disables the queries inside InnoDB and queries in queue counters in the ROW OPERATIONS section of SHOW ENGINE INNODB STATUS output.

For related information, see Section 14.8.5, "Configuring Thread Concurrency for InnoDB".

<span id="page-51-0"></span>• [innodb\\_thread\\_sleep\\_delay](#page-51-0)

| Command-Line Format | innodb-thread-sleep-delay=# |
|---------------------|-----------------------------|
| System Variable     | innodb_thread_sleep_delay   |
| Scope               | Global                      |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 10000                       |
| Minimum Value       | 0                           |
| Maximum Value       | 1000000                     |
| Unit                | microseconds                |

Defines how long InnoDB threads sleep before joining the InnoDB queue, in microseconds. The default value is 10000. A value of 0 disables sleep. You can set innodb\_adaptive\_max\_sleep\_delay to the highest value you would allow for [innodb\\_thread\\_sleep\\_delay](#page-51-0), and InnoDB automatically adjusts [innodb\\_thread\\_sleep\\_delay](#page-51-0) up or down depending on current thread-scheduling activity. This dynamic adjustment helps the thread scheduling mechanism to work smoothly during times when the system is lightly loaded or when it is operating near full capacity.

For more information, see Section 14.8.5, "Configuring Thread Concurrency for InnoDB".

<span id="page-51-1"></span>• [innodb\\_tmpdir](#page-51-1)

| Command-Line Format | innodb-tmpdir=dir_name |
|---------------------|------------------------|
| System Variable     | innodb_tmpdir          |
| Scope               | Global, Session        |
| Dynamic             | Yes                    |
| Type                | Directory name         |
| Default Value       | NULL                   |

Used to define an alternate directory for temporary sort files created during online ALTER TABLE operations that rebuild the table.

Online ALTER TABLE operations that rebuild the table also create an intermediate table file in the same directory as the original table. The [innodb\\_tmpdir](#page-51-1) option is not applicable to intermediate table files.

A valid value is any directory path other than the MySQL data directory path. If the value is NULL (the default), temporary files are created MySQL temporary directory (\$TMPDIR on Unix, %TEMP % on Windows, or the directory specified by the --tmpdir configuration option). If a directory is specified, existence of the directory and permissions are only checked when [innodb\\_tmpdir](#page-51-1) is configured using a SET statement. If a symlink is provided in a directory string, the symlink is resolved and stored as an absolute path. The path should not exceed 512 bytes. An online ALTER TABLE operation reports an error if [innodb\\_tmpdir](#page-51-1) is set to an invalid directory. [innodb\\_tmpdir](#page-51-1) overrides the MySQL tmpdir setting but only for online ALTER TABLE operations.

The FILE privilege is required to configure [innodb\\_tmpdir](#page-51-1).

The [innodb\\_tmpdir](#page-51-1) option was introduced to help avoid overflowing a temporary file directory located on a tmpfs file system. Such overflows could occur as a result of large temporary sort files created during online ALTER TABLE operations that rebuild the table.

In replication environments, only consider replicating the [innodb\\_tmpdir](#page-51-1) setting if all servers have the same operating system environment. Otherwise, replicating the [innodb\\_tmpdir](#page-51-1) setting could result in a replication failure when running online ALTER TABLE operations that rebuild the table. If server operating environments differ, it is recommended that you configure [innodb\\_tmpdir](#page-51-1) on each server individually.

For more information, see Section 14.13.3, "Online DDL Space Requirements". For information about online ALTER TABLE operations, see Section 14.13, "InnoDB and Online DDL".

<span id="page-52-0"></span>• [innodb\\_trx\\_purge\\_view\\_update\\_only\\_debug](#page-52-0)

| Command-Line Format | innodb-trx-purge-view-update-only<br>debug[={OFF ON}] |
|---------------------|-------------------------------------------------------|
| System Variable     | innodb_trx_purge_view_update_only_debug               |
| Scope               | Global                                                |
| Dynamic             | Yes                                                   |
| Type                | Boolean                                               |
| Default Value       | OFF                                                   |

Pauses purging of delete-marked records while allowing the purge view to be updated. This option artificially creates a situation in which the purge view is updated but purges have not yet been performed. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-53-1"></span>• [innodb\\_trx\\_rseg\\_n\\_slots\\_debug](#page-53-1)

| Command-Line Format | innodb-trx-rseg-n-slots-debug=# |
|---------------------|---------------------------------|
| System Variable     | innodb_trx_rseg_n_slots_debug   |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | Integer                         |
| Default Value       | 0                               |
| Minimum Value       | 0                               |
| Maximum Value       | 1024                            |

Sets a debug flag that limits TRX\_RSEG\_N\_SLOTS to a given value for the trx\_rsegf\_undo\_find\_free function that looks for free slots for undo log segments. This option is only available if debugging support is compiled in using the WITH\_DEBUG CMake option.

<span id="page-53-2"></span>• [innodb\\_undo\\_directory](#page-53-2)

| Command-Line Format | innodb-undo-directory=dir_name |
|---------------------|--------------------------------|
| System Variable     | innodb_undo_directory          |
| Scope               | Global                         |
| Dynamic             | No                             |
| Type                | Directory name                 |

The path where InnoDB creates undo tablespaces. Typically used to place undo logs on a different storage device. Used in conjunction with [innodb\\_rollback\\_segments](#page-40-3) and [innodb\\_undo\\_tablespaces](#page-54-0).

There is no default value (it is NULL). If a path is not specified, undo tablespaces are created in the MySQL data directory, as defined by datadir.

For more information, see Section 14.6.3.4, "Undo Tablespaces".

<span id="page-53-0"></span>• [innodb\\_undo\\_log\\_truncate](#page-53-0)

| Command-Line Format | innodb-undo-log-truncate[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | innodb_undo_log_truncate                |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | Boolean                                 |
| Default Value       | OFF                                     |

When enabled, undo tablespaces that exceed the threshold value defined by [innodb\\_max\\_undo\\_log\\_size](#page-30-0) are marked for truncation. Only undo tablespaces can be truncated. Truncating undo logs that reside in the system tablespace is not supported. For truncation to occur, there must be at least two undo tablespaces and two redo-enabled undo logs configured to use undo tablespaces. This means that [innodb\\_undo\\_tablespaces](#page-54-0) must be set to a value equal to or greater than 2, and [innodb\\_rollback\\_segments](#page-40-3) must set to a value equal to or greater than 35.

The [innodb\\_purge\\_rseg\\_truncate\\_frequency](#page-38-0) variable can be used to expedite truncation of undo tablespaces.

### <span id="page-54-1"></span>• [innodb\\_undo\\_logs](#page-54-1)

| Command-Line Format | innodb-undo-logs=# |
|---------------------|--------------------|
| Deprecated          | Yes                |
| System Variable     | innodb_undo_logs   |
| Scope               | Global             |
| Dynamic             | Yes                |
| Type                | Integer            |
| Default Value       | 128                |
| Minimum Value       | 1                  |
| Maximum Value       | 128                |

![](_page_54_Picture_3.jpeg)

#### **Note**

[innodb\\_undo\\_logs](#page-54-1) is deprecated; expect it to be removed in a future MySQL release.

Defines the number of rollback segments used by InnoDB. The [innodb\\_undo\\_logs](#page-54-1) option is an alias for [innodb\\_rollback\\_segments](#page-40-3). For more information, see the description of [innodb\\_rollback\\_segments](#page-40-3).

### <span id="page-54-0"></span>• [innodb\\_undo\\_tablespaces](#page-54-0)

| Command-Line Format | innodb-undo-tablespaces=# |
|---------------------|---------------------------|
| Deprecated          | Yes                       |
| System Variable     | innodb_undo_tablespaces   |
| Scope               | Global                    |
| Dynamic             | No                        |
| Type                | Integer                   |
| Default Value       | 0                         |
| Minimum Value       | 0                         |
| Maximum Value       | 95                        |

The number of undo tablespaces used by InnoDB. The default value is 0.

![](_page_54_Picture_10.jpeg)

#### **Note**

[innodb\\_undo\\_tablespaces](#page-54-0) is deprecated; expect it to be removed in a future MySQL release.

Because undo logs can become large during long-running transactions, having undo logs in multiple tablespaces reduces the maximum size of any one tablespace. The undo tablespace files are created in the location defined by [innodb\\_undo\\_directory](#page-53-2), with names in the form of undoN, where N is a sequential series of integers (including leading zeros) representing the space ID.

The initial size of an undo tablespace file depends on the [innodb\\_page\\_size](#page-36-0) value. For the default 16KB InnoDB page size, the initial undo tablespace file size is 10MiB. For 4KB, 8KB, 32KB, and 64KB page sizes, the initial undo tablespace files sizes are 7MiB, 8MiB, 20MiB, and 40MiB, respectively.

A minimum of two undo tablespaces is required to enable truncation of undo logs. See Truncating Undo Tablespaces.

![](_page_55_Picture_3.jpeg)

#### **Important**

[innodb\\_undo\\_tablespaces](#page-54-0) can only be configured prior to initializing the MySQL instance and cannot be changed afterward. If no value is specified, the instance is initialized using the default setting of 0. Attempting to restart InnoDB with a greater number of undo tablespaces than specified when the MySQL instance was initialized results in a startup failure and an error stating that InnoDB did not find the expected number of undo tablespaces.

32 of 128 rollback segments are reserved for temporary tables, as described in Section 14.6.7, "Undo Logs". One rollback segment is always assigned to the system tablespace, which leaves 95 rollback segments available for undo tablespaces. This means the [innodb\\_undo\\_tablespaces](#page-54-0) maximum limit is 95.

For more information, see Section 14.6.3.4, "Undo Tablespaces".

<span id="page-55-0"></span>• [innodb\\_use\\_native\\_aio](#page-55-0)

| Command-Line Format | innodb-use-native-aio[={OFF ON}] |
|---------------------|----------------------------------|
| System Variable     | innodb_use_native_aio            |
| Scope               | Global                           |
| Dynamic             | No                               |
| Type                | Boolean                          |
| Default Value       | ON                               |

Specifies whether to use the Linux asynchronous I/O subsystem. This variable applies to Linux systems only, and cannot be changed while the server is running. Normally, you do not need to configure this option, because it is enabled by default.

The asynchronous I/O capability that InnoDB has on Windows systems is available on Linux systems. (Other Unix-like systems continue to use synchronous I/O calls.) This feature improves the scalability of heavily I/O-bound systems, which typically show many pending reads/writes in SHOW ENGINE INNODB STATUS\G output.

Running with a large number of InnoDB I/O threads, and especially running multiple such instances on the same server machine, can exceed capacity limits on Linux systems. In this case, you may receive the following error:

EAGAIN: The specified maxevents exceeds the user's limit of available events.

You can typically address this error by writing a higher limit to /proc/sys/fs/aio-max-nr.

However, if a problem with the asynchronous I/O subsystem in the OS prevents InnoDB from starting, you can start the server with [innodb\\_use\\_native\\_aio=0](#page-55-0). This option may also be disabled automatically during startup if InnoDB detects a potential problem such as a combination of tmpdir location, tmpfs file system, and Linux kernel that does not support AIO on tmpfs.

For more information, see Section 14.8.7, "Using Asynchronous I/O on Linux".

<span id="page-55-1"></span>• [innodb\\_version](#page-55-1)

The InnoDB version number. In MySQL 5.7, separate version numbering for InnoDB does not apply and this value is the same the version number of the server.

<span id="page-56-0"></span>• [innodb\\_write\\_io\\_threads](#page-56-0)

| Command-Line Format | innodb-write-io-threads=# |
|---------------------|---------------------------|
| System Variable     | innodb_write_io_threads   |
| Scope               | Global                    |
| Dynamic             | No                        |
| Type                | Integer                   |
| Default Value       | 4                         |
| Minimum Value       | 1                         |
| Maximum Value       | 64                        |

The number of I/O threads for write operations in InnoDB. The default value is 4. Its counterpart for read threads is [innodb\\_read\\_io\\_threads](#page-39-0). For more information, see Section 14.8.6, "Configuring the Number of Background InnoDB I/O Threads". For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".

![](_page_56_Picture_4.jpeg)

### **Note**

On Linux systems, running multiple MySQL servers (typically more than 12) with default settings for [innodb\\_read\\_io\\_threads](#page-39-0), [innodb\\_write\\_io\\_threads](#page-56-0), and the Linux aio-max-nr setting can exceed system limits. Ideally, increase the aio-max-nr setting; as a workaround, you might reduce the settings for one or both of the MySQL variables.

Also take into consideration the value of sync\_binlog, which controls synchronization of the binary log to disk.

For general I/O tuning advice, see Section 8.5.8, "Optimizing InnoDB Disk I/O".