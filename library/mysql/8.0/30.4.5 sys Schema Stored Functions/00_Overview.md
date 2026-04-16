---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following sections describe sys schema stored functions.

## <span id="page-8-0"></span>**30.4.5.1 The extract\_schema\_from\_file\_name() Function**

Given a file path name, returns the path component that represents the schema name. This function assumes that the file name lies within the schema directory. For this reason, it does not work with partitions or tables defined using their own DATA\_DIRECTORY table option.

This function is useful when extracting file I/O information from the Performance Schema that includes file path names. It provides a convenient way to display schema names, which can be more easily understood than full path names, and can be used in joins against object schema names.

### **Parameters**

• path VARCHAR(512): The full path to a data file from which to extract the schema name.

### **Return Value**

A VARCHAR(64) value.

## **Example**

```
mysql> SELECT sys.extract_schema_from_file_name('/usr/local/mysql/data/world/City.ibd');
+---------------------------------------------------------------------------+
| sys.extract_schema_from_file_name('/usr/local/mysql/data/world/City.ibd') |
+---------------------------------------------------------------------------+
| world |
+---------------------------------------------------------------------------+
```

## <span id="page-9-1"></span>**30.4.5.2 The extract\_table\_from\_file\_name() Function**

Given a file path name, returns the path component that represents the table name.

This function is useful when extracting file I/O information from the Performance Schema that includes file path names. It provides a convenient way to display table names, which can be more easily understood than full path names, and can be used in joins against object table names.

### **Parameters**

• path VARCHAR(512): The full path to a data file from which to extract the table name.

## **Return Value**

A VARCHAR(64) value.

### **Example**

```
mysql> SELECT sys.extract_table_from_file_name('/usr/local/mysql/data/world/City.ibd');
+--------------------------------------------------------------------------+
| sys.extract_table_from_file_name('/usr/local/mysql/data/world/City.ibd') |
+--------------------------------------------------------------------------+
| City |
+--------------------------------------------------------------------------+
```

## <span id="page-9-2"></span><span id="page-9-0"></span>**30.4.5.3 The format\_bytes() Function**

![](_page_9_Picture_18.jpeg)

#### **Note**

As of MySQL 8.0.16, [format\\_bytes\(\)](#page-9-0) is deprecated and subject to removal in a future MySQL version. Applications that use it should be migrated to use the built-in FORMAT\_BYTES() function instead. See Section 14.21, "Performance Schema Functions"

Given a byte count, converts it to human-readable format and returns a string consisting of a value and a units indicator. Depending on the size of the value, the units part is bytes, KiB (kibibytes), MiB (mebibytes), GiB (gibibytes), TiB (tebibytes), or PiB (pebibytes).

### **Parameters**

• bytes TEXT: The byte count to format.

### **Return Value**

A TEXT value.

### **Example**

```
mysql> SELECT sys.format_bytes(512), sys.format_bytes(18446644073709551615);
+-----------------------+----------------------------------------+
| sys.format_bytes(512) | sys.format_bytes(18446644073709551615) |
+-----------------------+----------------------------------------+
| 512 bytes | 16383.91 PiB |
+-----------------------+----------------------------------------+
```

## <span id="page-10-1"></span>**30.4.5.4 The format\_path() Function**

Given a path name, returns the modified path name after replacing subpaths that match the values of the following system variables, in order:

```
datadir
tmpdir
slave_load_tmpdir or replica_load_tmpdir
innodb_data_home_dir
innodb_log_group_home_dir
innodb_undo_directory
basedir
```

A value that matches the value of system variable sysvar is replaced with the string @@GLOBAL.sysvar.

### **Parameters**

• path VARCHAR(512): The path name to format.

## **Return Value**

A VARCHAR(512) CHARACTER SET utf8mb3 value.

### **Example**

```
mysql> SELECT sys.format_path('/usr/local/mysql/data/world/City.ibd');
+---------------------------------------------------------+
| sys.format_path('/usr/local/mysql/data/world/City.ibd') |
+---------------------------------------------------------+
| @@datadir/world/City.ibd |
+---------------------------------------------------------+
```

## <span id="page-10-2"></span><span id="page-10-0"></span>**30.4.5.5 The format\_statement() Function**

Given a string (normally representing an SQL statement), reduces it to the length given by the statement\_truncate\_len configuration option, and returns the result. No truncation occurs if the string is shorter than statement\_truncate\_len. Otherwise, the middle part of the string is replaced by an ellipsis (...).

This function is useful for formatting possibly lengthy statements retrieved from Performance Schema tables to a known fixed maximum length.

### **Parameters**

• statement LONGTEXT: The statement to format.

## **Configuration Options**

[format\\_statement\(\)](#page-10-0) operation can be modified using the following configuration options or their corresponding user-defined variables (see Section 30.4.2.1, "The sys\_config Table"):

• statement\_truncate\_len, @sys.statement\_truncate\_len

The maximum length of statements returned by the [format\\_statement\(\)](#page-10-0) function. Longer statements are truncated to this length. The default is 64.

## **Return Value**

A LONGTEXT value.

### **Example**

By default, [format\\_statement\(\)](#page-10-0) truncates statements to be no more than 64 characters. Setting @sys.statement\_truncate\_len changes the truncation length for the current session:

```
mysql> SET @stmt = 'SELECT variable, value, set_time, set_by FROM sys_config';
mysql> SELECT sys.format_statement(@stmt);
+----------------------------------------------------------+
| sys.format_statement(@stmt) |
+----------------------------------------------------------+
| SELECT variable, value, set_time, set_by FROM sys_config |
+----------------------------------------------------------+
mysql> SET @sys.statement_truncate_len = 32;
mysql> SELECT sys.format_statement(@stmt);
+-----------------------------------+
| sys.format_statement(@stmt) |
+-----------------------------------+
| SELECT variabl ... ROM sys_config |
+-----------------------------------+
```

## <span id="page-11-2"></span><span id="page-11-0"></span>**30.4.5.6 The format\_time() Function**

![](_page_11_Picture_9.jpeg)

#### **Note**

As of MySQL 8.0.16, [format\\_time\(\)](#page-11-0) is deprecated and subject to removal in a future MySQL version. Applications that use it should be migrated to use the built-in FORMAT\_PICO\_TIME() function instead. See Section 14.21, "Performance Schema Functions"

Given a Performance Schema latency or wait time in picoseconds, converts it to human-readable format and returns a string consisting of a value and a units indicator. Depending on the size of the value, the units part is ps (picoseconds), ns (nanoseconds), us (microseconds), ms (milliseconds), s (seconds), m (minutes), h (hours), d (days), or w (weeks).

## **Parameters**

• picoseconds TEXT: The picoseconds value to format.

## **Return Value**

A TEXT value.

### **Example**

```
mysql> SELECT sys.format_time(3501), sys.format_time(188732396662000);
+-----------------------+----------------------------------+
| sys.format_time(3501) | sys.format_time(188732396662000) |
+-----------------------+----------------------------------+
| 3.50 ns | 3.15 m |
+-----------------------+----------------------------------+
```

## <span id="page-11-1"></span>**30.4.5.7 The list\_add() Function**

Adds a value to a comma-separated list of values and returns the result.

This function and [list\\_drop\(\)](#page-12-0) can be useful for manipulating the value of system variables such as sql\_mode and optimizer\_switch that take a comma-separated list of values.

### **Parameters**

- in\_list TEXT: The list to be modified.
- in\_add\_value TEXT: The value to add to the list.

### **Return Value**

A TEXT value.

## **Example**

```
mysql> SELECT @@sql_mode;
+----------------------------------------+
| @@sql_mode |
+----------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES |
+----------------------------------------+
mysql> SET @@sql_mode = sys.list_add(@@sql_mode, 'NO_ENGINE_SUBSTITUTION');
mysql> SELECT @@sql_mode;
+---------------------------------------------------------------+
| @@sql_mode |
+---------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION |
+---------------------------------------------------------------+
mysql> SET @@sql_mode = sys.list_drop(@@sql_mode, 'ONLY_FULL_GROUP_BY');
mysql> SELECT @@sql_mode;
+--------------------------------------------+
| @@sql_mode |
+--------------------------------------------+
| STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION |
+--------------------------------------------+
```

## <span id="page-12-0"></span>**30.4.5.8 The list\_drop() Function**

Removes a value from a comma-separated list of values and returns the result. For more information, see the description of [list\\_add\(\)](#page-11-1)

### **Parameters**

- in\_list TEXT: The list to be modified.
- in\_drop\_value TEXT: The value to drop from the list.

### **Return Value**

A TEXT value.