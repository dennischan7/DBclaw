---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes syntax warnings and errors that you may encounter when using the table compression feature with file-per-table tablespaces and general tablespaces.

## **SQL Compression Syntax Warnings and Errors for File-Per-Table Tablespaces**

When innodb\_strict\_mode is enabled (the default), specifying ROW\_FORMAT=COMPRESSED or KEY\_BLOCK\_SIZE in CREATE TABLE or ALTER TABLE statements produces the following error if innodb\_file\_per\_table is disabled.

ERROR 1031 (HY000): Table storage engine for 't1' doesn't have this option

![](_page_135_Picture_10.jpeg)

#### **Note**

The table is not created if the current configuration does not permit using compressed tables.

When innodb\_strict\_mode is disabled, specifying ROW\_FORMAT=COMPRESSED or KEY\_BLOCK\_SIZE in CREATE TABLE or ALTER TABLE statements produces the following warnings if innodb\_file\_per\_table is disabled.

![](_page_135_Picture_14.jpeg)

![](_page_135_Picture_15.jpeg)

#### **Note**

These messages are only warnings, not errors, and the table is created without compression, as if the options were not specified.

The "non-strict" behavior lets you import a mysqldump file into a database that does not support compressed tables, even if the source database contained compressed tables. In that case, MySQL creates the table in ROW\_FORMAT=DYNAMIC instead of preventing the operation.

To import the dump file into a new database, and have the tables re-created as they exist in the original database, ensure the server has the proper setting for the innodb\_file\_per\_table configuration parameter.

The attribute KEY\_BLOCK\_SIZE is permitted only when ROW\_FORMAT is specified as COMPRESSED or is omitted. Specifying a KEY\_BLOCK\_SIZE with any other ROW\_FORMAT generates a warning that you can view with SHOW WARNINGS. However, the table is non-compressed; the specified KEY\_BLOCK\_SIZE is ignored).

| Level   | Code<br>Message |                         |
|---------|-----------------|-------------------------|
| Warning | 1478            | InnoDB: ignoring        |
|         |                 | KEY_BLOCK_SIZE=n unless |
|         |                 | ROW_FORMAT=COMPRESSED.  |

If you are running with innodb\_strict\_mode enabled, the combination of a KEY\_BLOCK\_SIZE with any ROW\_FORMAT other than COMPRESSED generates an error, not a warning, and the table is not created.

[Table 17.11, "ROW\\_FORMAT and KEY\\_BLOCK\\_SIZE Options"](#page-136-0) provides an overview the ROW\_FORMAT and KEY\_BLOCK\_SIZE options that are used with CREATE TABLE or ALTER TABLE.

**Table 17.11 ROW\_FORMAT and KEY\_BLOCK\_SIZE Options**

<span id="page-136-0"></span>

| Option                | Usage Notes                                 | Description                                                                                                                                                                                                       |
|-----------------------|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ROW_FORMAT=REDUNDANT  | Storage format used prior to<br>MySQL 5.0.3 | Less efficient than<br>ROW_FORMAT=COMPACT; for<br>backward compatibility                                                                                                                                          |
| ROW_FORMAT=COMPACT    | Default storage format since<br>MySQL 5.0.3 | Stores a prefix of 768 bytes<br>of long column values in the<br>clustered index page, with the<br>remaining bytes stored in an<br>overflow page                                                                   |
| ROW_FORMAT=DYNAMIC    |                                             | Store values within the clustered<br>index page if they fit; if not,<br>stores only a 20-byte pointer to<br>an overflow page (no prefix)                                                                          |
| ROW_FORMAT=COMPRESSED |                                             | Compresses the table and<br>indexes using zlib                                                                                                                                                                    |
| KEY_BLOCK_SIZE=n      |                                             | Specifies compressed<br>page size of 1, 2, 4, 8<br>or 16 kilobytes; implies<br>ROW_FORMAT=COMPRESSED.<br>For general tablespaces, a<br>KEY_BLOCK_SIZE value equal<br>to the InnoDB page size is not<br>permitted. |

[Table 17.12, "CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF"](#page-137-0) summarizes error conditions that occur with certain combinations of configuration parameters and options on the CREATE TABLE or ALTER TABLE statements, and how the options appear in the output of SHOW TABLE STATUS.

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

**Table 17.12 CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF**

<span id="page-137-0"></span>

| Syntax                                                                           | Warning or Error Condition                                                                                                                                                                  | Resulting ROW_FORMAT,<br>as shown in SHOW TABLE<br>STATUS                                                           |  |  |
|----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|--|--|
| ROW_FORMAT=REDUNDANT                                                             | None                                                                                                                                                                                        | REDUNDANT                                                                                                           |  |  |
| ROW_FORMAT=COMPACT                                                               | None                                                                                                                                                                                        | COMPACT                                                                                                             |  |  |
| ROW_FORMAT=COMPRESSED<br>or ROW_FORMAT=DYNAMIC or<br>KEY_BLOCK_SIZE is specified | Ignored for file-per<br>table tablespaces unless<br>innodb_file_per_table is<br>enabled. General tablespaces<br>support all row formats. See<br>Section 17.6.3.3, "General<br>Tablespaces". | the default row format<br>for file-per-table<br>tablespaces; the<br>specified row format for<br>general tablespaces |  |  |
| Invalid KEY_BLOCK_SIZE is<br>specified (not 1, 2, 4, 8 or 16)                    | KEY_BLOCK_SIZE is ignored                                                                                                                                                                   | the specified row format, or the<br>default row format                                                              |  |  |
| ROW_FORMAT=COMPRESSED<br>and valid KEY_BLOCK_SIZE are<br>specified               | None; KEY_BLOCK_SIZE<br>specified is used                                                                                                                                                   | COMPRESSED                                                                                                          |  |  |
| KEY_BLOCK_SIZE is specified<br>with REDUNDANT, COMPACT or<br>DYNAMIC row format  | KEY_BLOCK_SIZE is ignored                                                                                                                                                                   | REDUNDANT, COMPACT or<br>DYNAMIC                                                                                    |  |  |
| ROW_FORMAT is not one<br>of REDUNDANT, COMPACT,<br>DYNAMIC or COMPRESSED         | Ignored if recognized by the<br>MySQL parser. Otherwise, an<br>error is issued.                                                                                                             | the default row format or N/A                                                                                       |  |  |

When innodb\_strict\_mode is ON, MySQL rejects invalid ROW\_FORMAT or KEY\_BLOCK\_SIZE parameters and issues errors. Strict mode is ON by default. When innodb\_strict\_mode is OFF, MySQL issues warnings instead of errors for ignored invalid parameters.

It is not possible to see the chosen KEY\_BLOCK\_SIZE using SHOW TABLE STATUS. The statement SHOW CREATE TABLE displays the KEY\_BLOCK\_SIZE (even if it was ignored when creating the table). The real compressed page size of the table cannot be displayed by MySQL.

### **SQL Compression Syntax Warnings and Errors for General Tablespaces**

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

innodb\_strict\_mode is not applicable to general tablespaces. Tablespace management rules for general tablespaces are strictly enforced independently of innodb\_strict\_mode. For more information, see Section 15.1.21, "CREATE TABLESPACE Statement".

For more information about using compressed tables with general tablespaces, see [Section 17.6.3.3,](#page-32-0) ["General Tablespaces".](#page-32-0)