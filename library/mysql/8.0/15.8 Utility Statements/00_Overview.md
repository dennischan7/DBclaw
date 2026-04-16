---
source: MySQL 8.0 Reference
title: 00_Overview
---

# <span id="page-163-0"></span>**15.8.1 DESCRIBE Statement**

The [DESCRIBE](#page-163-0) and [EXPLAIN](#page-163-1) statements are synonyms, used either to obtain information about table structure or query execution plans. For more information, see [Section 15.7.7.5, "SHOW COLUMNS](#page-99-0) [Statement",](#page-99-0) and [Section 15.8.2, "EXPLAIN Statement".](#page-163-1)

## <span id="page-163-1"></span>**15.8.2 EXPLAIN Statement**

```
{EXPLAIN | DESCRIBE | DESC}
 tbl_name [col_name | wild]
{EXPLAIN | DESCRIBE | DESC}
 [explain_type]
 {explainable_stmt | FOR CONNECTION connection_id}
{EXPLAIN | DESCRIBE | DESC} ANALYZE [explain_type] select_stmt
explain_type: {
 FORMAT = format_name
}
format_name: {
 TRADITIONAL
 | JSON
 | TREE
}
explainable_stmt: {
 select_stmt
 | TABLE ...
 | DELETE ...
 | INSERT ...
 | REPLACE ...
 | UPDATE ...
}
select_stmt:
 SELECT ...
```

The [DESCRIBE](#page-163-0) and [EXPLAIN](#page-163-1) statements are synonyms. In practice, the [DESCRIBE](#page-163-0) keyword is more often used to obtain information about table structure, whereas [EXPLAIN](#page-163-1) is used to obtain a query execution plan (that is, an explanation of how MySQL would execute a query).

The following discussion uses the [DESCRIBE](#page-163-0) and [EXPLAIN](#page-163-1) keywords in accordance with those uses, but the MySQL parser treats them as completely synonymous.

- [Obtaining Table Structure Information](#page-164-0)
- [Obtaining Execution Plan Information](#page-164-1)
- [Obtaining Information with EXPLAIN ANALYZE](#page-167-0)

## <span id="page-164-0"></span>**Obtaining Table Structure Information**

[DESCRIBE](#page-163-0) provides information about the columns in a table:

| +++++++<br>  Field<br>  Type<br>  Null   Key   Default   Extra<br> <br>+++++++<br>  Id<br>  int(11)   NO<br>  PRI   NULL<br>  auto_increment  <br>  Name<br>  char(35)   NO<br> <br> <br> <br> <br>  Country<br>  char(3)   NO<br>  UNI  <br> <br> <br>  District<br>  char(20)   YES   MUL  <br> <br> <br>  Population   int(11)   NO<br> <br>  0<br> <br> <br>+++++++ | mysql> DESCRIBE City; |  |  |  |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|--|--|--|
|                                                                                                                                                                                                                                                                                                                                                                         |                       |  |  |  |
|                                                                                                                                                                                                                                                                                                                                                                         |                       |  |  |  |

[DESCRIBE](#page-163-0) is a shortcut for [SHOW COLUMNS](#page-99-0). These statements also display information for views. The description for [SHOW COLUMNS](#page-99-0) provides more information about the output columns. See [Section 15.7.7.5, "SHOW COLUMNS Statement".](#page-99-0)

By default, [DESCRIBE](#page-163-0) displays information about all columns in the table. col\_name, if given, is the name of a column in the table. In this case, the statement displays information only for the named column. wild, if given, is a pattern string. It can contain the SQL % and \_ wildcard characters. In this case, the statement displays output only for the columns with names matching the string. There is no need to enclose the string within quotation marks unless it contains spaces or other special characters.

The [DESCRIBE](#page-163-0) statement is provided for compatibility with Oracle.

The [SHOW CREATE TABLE](#page-103-0), [SHOW TABLE STATUS](#page-141-0), and [SHOW INDEX](#page-118-0) statements also provide information about tables. See [Section 15.7.7, "SHOW Statements"](#page-95-1).

The explain\_format system variable, added in MySQL 8.0.32, has no effect on the output of EXPLAIN when used to obtain information about table columns.

## <span id="page-164-1"></span>**Obtaining Execution Plan Information**

The [EXPLAIN](#page-163-1) statement provides information about how MySQL executes statements:

- [EXPLAIN](#page-163-1) works with SELECT, DELETE, INSERT, REPLACE, and UPDATE statements. In MySQL 8.0.19 and later, it also works with TABLE statements.
- When [EXPLAIN](#page-163-1) is used with an explainable statement, MySQL displays information from the optimizer about the statement execution plan. That is, MySQL explains how it would process the statement, including information about how tables are joined and in which order. For information about using [EXPLAIN](#page-163-1) to obtain execution plan information, see Section 10.8.2, "EXPLAIN Output Format".
- When [EXPLAIN](#page-163-1) is used with FOR CONNECTION connection\_id rather than an explainable statement, it displays the execution plan for the statement executing in the named connection. See Section 10.8.4, "Obtaining Execution Plan Information for a Named Connection".
- For explainable statements, [EXPLAIN](#page-163-1) produces additional execution plan information that can be displayed using [SHOW WARNINGS](#page-148-0). See Section 10.8.3, "Extended EXPLAIN Output Format".
- [EXPLAIN](#page-163-1) is useful for examining queries involving partitioned tables. See Section 26.3.5, "Obtaining Information About Partitions".
- The FORMAT option can be used to select the output format. TRADITIONAL presents the output in tabular format. This is the default if no FORMAT option is present. JSON format displays the

information in JSON format. In MySQL 8.0.16 and later, TREE provides tree-like output with more precise descriptions of query handling than the TRADITIONAL format; it is the only format which shows hash join usage (see Section 10.2.1.4, "Hash Join Optimization") and is always used for EXPLAIN ANALYZE.

As of MySQL 8.0.32, the default output format used by EXPLAIN (that is, when it has no FORMAT option) is determined by the value of the explain\_format system variable. The precise effects of this variable are described later in this section.

For complex statements, the JSON output can be quite large; in particular, it can be difficult when reading it to pair the closing bracket and opening brackets; to cause the JSON structure's key, if it has one, to be repeated near the closing bracket, set end\_markers\_in\_json=ON. You should be aware that while this makes the output easier to read, it also renders the JSON invalid, causing JSON functions to raise an error.

[EXPLAIN](#page-163-1) requires the same privileges required to execute the explained statement. Additionally, [EXPLAIN](#page-163-1) also requires the SHOW VIEW privilege for any explained view. [EXPLAIN ... FOR](#page-163-1) [CONNECTION](#page-163-1) also requires the PROCESS privilege if the specified connection belongs to a different user.

The explain\_format system variable introduced in MySQL 8.0.32 determines the format of the output from EXPLAIN when used to display a query execution plan. This variable can take any of the values used with the FORMAT option, with the addition of DEFAULT as a synonym for TRADITIONAL. The following example uses the country table from the world database which can be obtained from [MySQL: Other Downloads](https://dev.mysql.com/doc/index-other.md):

```
mysql> USE world; # Make world the current database
Database changed
```

Checking the value of explain\_format, we see that it has the default value, and that EXPLAIN (with no FORMAT option) therefore uses the traditional tabular output:

```
mysql> SELECT @@explain_format;
+------------------+
| @@explain_format |
+------------------+
| TRADITIONAL |
+------------------+
1 row in set (0.00 sec)
mysql> EXPLAIN SELECT Name FROM country WHERE Code Like 'A%';
+----+-------------+---------+------------+-------+---------------+---------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
+----+-------------+---------+------------+-------+---------------+---------+---------+------+------+----------+-------------+
| 1 | SIMPLE | country | NULL | range | PRIMARY | PRIMARY | 12 | NULL | 17 | 100.00 | Using where |
+----+-------------+---------+------------+-------+---------------+---------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)
```

If we set the value of explain\_format to TREE, then rerun the same EXPLAIN statement, the output uses the tree-like format:

```
mysql> SET @@explain_format=TREE;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@explain_format;
+------------------+
| @@explain_format |
+------------------+
| TREE |
+------------------+
1 row in set (0.00 sec)
mysql> EXPLAIN SELECT Name FROM country WHERE Code LIKE 'A%';
+--------------------------------------------------------------------------------------------------------------+
| EXPLAIN |
```

```
+--------------------------------------------------------------------------------------------------------------+
| -> Filter: (country.`Code` like 'A%') (cost=3.67 rows=17)
 -> Index range scan on country using PRIMARY over ('A' <= Code <= 'A????????') (cost=3.67 rows=17) |
+--------------------------------------------------------------------------------------------------------------+
1 row in set, 1 warning (0.00 sec)
```

As stated previously, the FORMAT option overrides this setting. Executing the same EXPLAIN statement using FORMAT=JSON instead of FORMAT=TREE shows that this is the case:

```
mysql> EXPLAIN FORMAT=JSON SELECT Name FROM country WHERE Code LIKE 'A%';
+------------------------------------------------------------------------------+
| EXPLAIN |
+------------------------------------------------------------------------------+
| {
 "query_block": {
 "select_id": 1,
 "cost_info": {
 "query_cost": "3.67"
 },
 "table": {
 "table_name": "country",
 "access_type": "range",
 "possible_keys": [
 "PRIMARY"
 ],
 "key": "PRIMARY",
 "used_key_parts": [
 "Code"
 ],
 "key_length": "12",
 "rows_examined_per_scan": 17,
 "rows_produced_per_join": 17,
 "filtered": "100.00",
 "cost_info": {
 "read_cost": "1.97",
 "eval_cost": "1.70",
 "prefix_cost": "3.67",
 "data_read_per_join": "16K"
 },
 "used_columns": [
 "Code",
 "Name"
 ],
 "attached_condition": "(`world`.`country`.`Code` like 'A%')"
 }
 }
} |
+------------------------------------------------------------------------------+
1 row in set, 1 warning (0.00 sec)
```

To return the default output of EXPLAIN to the tabular format, set explain\_format to TRADITIONAL. Alternatively, you can set it to DEFAULT, which has the same effect, as shown here:

```
mysql> SET @@explain_format=DEFAULT;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@explain_format;
+------------------+
| @@explain_format |
+------------------+
| TRADITIONAL |
+------------------+
1 row in set (0.00 sec)
```

With the help of [EXPLAIN](#page-163-1), you can see where you should add indexes to tables so that the statement executes faster by using indexes to find rows. You can also use [EXPLAIN](#page-163-1) to check whether the optimizer joins the tables in an optimal order. To give a hint to the optimizer to use a join order corresponding to the order in which the tables are named in a SELECT statement, begin the statement with SELECT STRAIGHT\_JOIN rather than just SELECT. (See Section 15.2.13, "SELECT Statement".) The optimizer trace may sometimes provide information complementary to that of [EXPLAIN](#page-163-1). However, the optimizer trace format and content are subject to change between versions. For details, see Section 10.15, "Tracing the Optimizer".

If you have a problem with indexes not being used when you believe that they should be, run [ANALYZE](#page-69-0) [TABLE](#page-69-0) to update table statistics, such as cardinality of keys, that can affect the choices the optimizer makes. See [Section 15.7.3.1, "ANALYZE TABLE Statement"](#page-69-0).

![](_page_167_Picture_3.jpeg)

## **Note**

MySQL Workbench has a Visual Explain capability that provides a visual representation of [EXPLAIN](#page-163-1) output. See [Tutorial: Using Explain to Improve](https://dev.mysql.com/doc/workbench/en/wb-tutorial-visual-explain-dbt3.md) [Query Performance](https://dev.mysql.com/doc/workbench/en/wb-tutorial-visual-explain-dbt3.md).

## <span id="page-167-0"></span>**Obtaining Information with EXPLAIN ANALYZE**

MySQL 8.0.18 introduces EXPLAIN ANALYZE, which runs a statement and produces [EXPLAIN](#page-164-1) output along with timing and additional, iterator-based, information about how the optimizer's expectations matched the actual execution. For each iterator, the following information is provided:

• Estimated execution cost

(Some iterators are not accounted for by the cost model, and so are not included in the estimate.)

- Estimated number of returned rows
- Time to return first row
- Time spent executing this iterator (including child iterators, but not parent iterators), in milliseconds. (When there are multiple loops, this figure shows the average time per loop.)
- Number of rows returned by the iterator
- Number of loops

The query execution information is displayed using the TREE output format, in which nodes represent iterators. EXPLAIN ANALYZE always uses the TREE output format. In MySQL 8.0.21 and later, this can optionally be specified explicitly using FORMAT=TREE; formats other than TREE remain unsupported.

EXPLAIN ANALYZE can be used with SELECT statements, as well as with multi-table UPDATE and DELETE statements. Beginning with MySQL 8.0.19, it can also be used with TABLE statements.

Beginning with MySQL 8.0.20, you can terminate this statement using [KILL QUERY](#page-158-0) or **CTRL-C**.

EXPLAIN ANALYZE cannot be used with FOR CONNECTION.

#### Example output:

```
mysql> EXPLAIN ANALYZE SELECT * FROM t1 JOIN t2 ON (t1.c1 = t2.c2)\G
*************************** 1. row ***************************
EXPLAIN: -> Inner hash join (t2.c2 = t1.c1) (cost=4.70 rows=6)
(actual time=0.032..0.035 rows=6 loops=1)
 -> Table scan on t2 (cost=0.06 rows=6)
(actual time=0.003..0.005 rows=6 loops=1)
 -> Hash
 -> Table scan on t1 (cost=0.85 rows=6)
(actual time=0.018..0.022 rows=6 loops=1)
mysql> EXPLAIN ANALYZE SELECT * FROM t3 WHERE i > 8\G
*************************** 1. row ***************************
EXPLAIN: -> Filter: (t3.i > 8) (cost=1.75 rows=5)
(actual time=0.019..0.021 rows=6 loops=1)
 -> Table scan on t3 (cost=1.75 rows=15)
(actual time=0.017..0.019 rows=15 loops=1)
```

```
mysql> EXPLAIN ANALYZE SELECT * FROM t3 WHERE pk > 17\G
*************************** 1. row ***************************
EXPLAIN: -> Filter: (t3.pk > 17) (cost=1.26 rows=5)
(actual time=0.013..0.016 rows=5 loops=1)
 -> Index range scan on t3 using PRIMARY (cost=1.26 rows=5)
(actual time=0.012..0.014 rows=5 loops=1)
```

The tables used in the example output were created by the statements shown here:

```
CREATE TABLE t1 (
 c1 INTEGER DEFAULT NULL,
 c2 INTEGER DEFAULT NULL
);
CREATE TABLE t2 (
 c1 INTEGER DEFAULT NULL,
 c2 INTEGER DEFAULT NULL
);
CREATE TABLE t3 (
 pk INTEGER NOT NULL PRIMARY KEY,
 i INTEGER DEFAULT NULL
);
```

Values shown for actual time in the output of this statement are expressed in milliseconds.

As of MySQL 8.0.32, the explain\_format system variable has the following effects on EXPLAIN ANALYZE:

- If the value of this variable is TRADITIONAL or TREE (or the synonym DEFAULT), EXPLAIN ANALYZE uses the TREE format. This ensures that this statement continues to use the TREE format by default, as it did prior to the introduction of explain\_format.
- If the value of explain\_format is JSON, EXPLAIN ANALYZE returns an error unless FORMAT=TREE is specified as part of the statement. This is due to the fact that EXPLAIN ANALYZE supports only the TREE output format.

We illustrate the behavior described in the second point here, re-using the last EXPLAIN ANALYZE statement from the previous example:

```
mysql> SET @@explain_format=JSON;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @@explain_format;
+------------------+
| @@explain_format |
+------------------+
| JSON |
+------------------+
1 row in set (0.00 sec)
mysql> EXPLAIN ANALYZE SELECT * FROM t3 WHERE pk > 17\G
ERROR 1235 (42000): This version of MySQL doesn't yet support 'EXPLAIN ANALYZE with JSON format'
mysql> EXPLAIN ANALYZE FORMAT=TRADITIONAL SELECT * FROM t3 WHERE pk > 17\G
ERROR 1235 (42000): This version of MySQL doesn't yet support 'EXPLAIN ANALYZE with TRADITIONAL format'
mysql> EXPLAIN ANALYZE FORMAT=TREE SELECT * FROM t3 WHERE pk > 17\G
*************************** 1. row ***************************
EXPLAIN: -> Filter: (t3.pk > 17) (cost=1.26 rows=5)
(actual time=0.013..0.016 rows=5 loops=1)
 -> Index range scan on t3 using PRIMARY (cost=1.26 rows=5)
(actual time=0.012..0.014 rows=5 loops=1)
```

Using FORMAT=TRADITIONAL or FORMAT=JSON with EXPLAIN ANALYZE always raises an error, regardless of the value of explain\_format.

Beginning with MySQL 8.0.33, numbers in the output of EXPLAIN ANALYZE and EXPLAIN FORMAT=TREE are formatted according to the following rules:

• Numbers in the range 0.001-999999.5 are printed as decimal numbers.

Decimal numbers less than 1000 have three significant digits; the remainder have four, five, or six.

- Numbers outside the range 0.001-999999.5 are printed in engineering format. Examples of such values are 1.23e+9 and 934e-6.
- No trailing zeros are printed. For example, we print 2.3 rather than 2.30, and 1.2e+6 rather than 1.20e+6.
- Numbers less than 1e-12 are printed as 0.

## <span id="page-169-0"></span>**15.8.3 HELP Statement**

```
HELP 'search_string'
```

The [HELP](#page-169-0) statement returns online information from the MySQL Reference Manual. Its proper operation requires that the help tables in the mysql database be initialized with help topic information (see Section 7.1.17, "Server-Side Help Support").

The [HELP](#page-169-0) statement searches the help tables for the given search string and displays the result of the search. The search string is not case-sensitive.

The search string can contain the wildcard characters % and \_. These have the same meaning as for pattern-matching operations performed with the LIKE operator. For example, HELP 'rep%' returns a list of topics that begin with rep.

The HELP statement does not require a terminator such as ; or \G.

The HELP statement understands several types of search strings:

• At the most general level, use contents to retrieve a list of the top-level help categories:

```
HELP 'contents'
```

• For a list of topics in a given help category, such as Data Types, use the category name:

```
HELP 'data types'
```

• For help on a specific help topic, such as the ASCII() function or the CREATE TABLE statement, use the associated keyword or keywords:

```
HELP 'ascii'
HELP 'create table'
```

In other words, the search string matches a category, many topics, or a single topic. The following descriptions indicate the forms that the result set can take.

• Empty result

No match could be found for the search string.

```
Example: HELP 'fake'
```

Yields:

```
Nothing found
Please try to run 'help contents' for a list of all accessible topics
```

• Result set containing a single row

This means that the search string yielded a hit for the help topic. The result includes the following items:

- name: The topic name.
- description: Descriptive help text for the topic.
- example: One or more usage examples. (May be empty.)

Example: HELP 'log'

#### Yields:

```
Name: 'LOG'
Description:
Syntax:
LOG(X), LOG(B,X)
If called with one parameter, this function returns the natural
logarithm of X. If X is less than or equal to 0.0E0, the function
returns NULL and a warning "Invalid argument for logarithm" is
reported. Returns NULL if X or B is NULL.
The inverse of this function (when called with a single argument) is
the EXP() function.
URL: https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html
Examples:
mysql> SELECT LOG(2);
 -> 0.69314718055995
mysql> SELECT LOG(-2);
 -> NULL
```

• List of topics.

This means that the search string matched multiple help topics.

Example: HELP 'status'

#### Yields:

```
Many help items for your request exist.
To make a more specific request, please type 'help <item>',
where <item> is one of the following topics:
 FLUSH
 SHOW
 SHOW ENGINE
 SHOW FUNCTION STATUS
 SHOW MASTER STATUS
 SHOW PROCEDURE STATUS
 SHOW REPLICA STATUS
 SHOW SLAVE STATUS
 SHOW STATUS
 SHOW TABLE STATUS
```

• List of topics.

A list is also displayed if the search string matches a category.

```
Example: HELP 'functions'
```

## Yields:

```
You asked for help about help category: "Functions"
For more information, type 'help <item>', where <item> is one of the following
categories:
 Aggregate Functions and Modifiers
 Bit Functions
 Cast Functions and Operators
 Comparison Operators
```

```
 Date and Time Functions
 Encryption Functions
 Enterprise Encryption Functions
 Flow Control Functions
 GROUP BY Functions and Modifiers
 GTID
 Information Functions
 Internal Functions
 Locking Functions
 Logical Operators
 Miscellaneous Functions
 Numeric Functions
 Performance Schema Functions
 Spatial Functions
 String Functions
 Window Functions
 XML
```

# <span id="page-171-0"></span>**15.8.4 USE Statement**

```
USE db_name
```

The [USE](#page-171-0) statement tells MySQL to use the named database as the default (current) database for subsequent statements. This statement requires some privilege for the database or some object within it.

The named database remains the default until the end of the session or another [USE](#page-171-0) statement is issued:

```
USE db1;
SELECT COUNT(*) FROM mytable; # selects from db1.mytable
USE db2;
SELECT COUNT(*) FROM mytable; # selects from db2.mytable
```

The database name must be specified on a single line. Newlines in database names are not supported.

Making a particular database the default by means of the [USE](#page-171-0) statement does not preclude accessing tables in other databases. The following example accesses the author table from the db1 database and the editor table from the db2 database:

```
USE db1;
SELECT author_name,editor_name FROM author,db2.editor
 WHERE author.editor_id = db2.editor.editor_id;
```

# Chapter 16 MySQL Data Dictionary

# **Table of Contents**

| 16.1 Data Dictionary Schema 3143                             |      |
|--------------------------------------------------------------|------|
| 16.2 Removal of File-based Metadata Storage 3144             |      |
| 16.3 Transactional Storage of Dictionary Data 3145           |      |
| 16.4 Dictionary Object Cache 3145                            |      |
| 16.5 INFORMATION_SCHEMA and Data Dictionary Integration 3146 |      |
| 16.6 Serialized Dictionary Information (SDI)                 | 3148 |
| 16.7 Data Dictionary Usage Differences 3148                  |      |
| 16.8 Data Dictionary Limitations 3150                        |      |

MySQL Server incorporates a transactional data dictionary that stores information about database objects. In previous MySQL releases, dictionary data was stored in metadata files, nontransactional tables, and storage engine-specific data dictionaries.

This chapter describes the main features, benefits, usage differences, and limitations of the data dictionary. For other implications of the data dictionary feature, refer to the "Data Dictionary Notes" section in the [MySQL 8.0 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/).

Benefits of the MySQL data dictionary include:

- Simplicity of a centralized data dictionary schema that uniformly stores dictionary data. See [Section 16.1, "Data Dictionary Schema".](#page-172-0)
- Removal of file-based metadata storage. See [Section 16.2, "Removal of File-based Metadata](#page-173-0) [Storage"](#page-173-0).
- Transactional, crash-safe storage of dictionary data. See [Section 16.3, "Transactional Storage of](#page-174-0) [Dictionary Data".](#page-174-0)
- Uniform and centralized caching for dictionary objects. See [Section 16.4, "Dictionary Object Cache"](#page-174-1).
- A simpler and improved implementation for some INFORMATION\_SCHEMA tables. See [Section 16.5,](#page-175-0) ["INFORMATION\\_SCHEMA and Data Dictionary Integration".](#page-175-0)
- Atomic DDL. See Section 15.1.1, "Atomic Data Definition Statement Support".

![](_page_172_Picture_12.jpeg)

#### **Important**

A data dictionary-enabled server entails some general operational differences compared to a server that does not have a data dictionary; see [Section 16.7,](#page-177-1) ["Data Dictionary Usage Differences"](#page-177-1). Also, for upgrades to MySQL 8.0, the upgrade procedure differs somewhat from previous MySQL releases and requires that you verify the upgrade readiness of your installation by checking specific prerequisites. For more information, see Chapter 3, Upgrading MySQL, particularly Section 3.6, "Preparing Your Installation for Upgrade".

# <span id="page-172-0"></span>**16.1 Data Dictionary Schema**

Data dictionary tables are protected and may only be accessed in debug builds of MySQL. However, MySQL supports access to data stored in data dictionary tables through INFORMATION\_SCHEMA tables and [SHOW](#page-95-1) statements. For an overview of the tables that comprise the data dictionary, see Data Dictionary Tables.

MySQL system tables still exist in MySQL 8.0 and can be viewed by issuing a [SHOW TABLES](#page-144-0) statement on the mysql system database. Generally, the difference between MySQL data dictionary tables and system tables is that data dictionary tables contain metadata required to execute SQL queries, whereas system tables contain auxiliary data such as time zone and help information. MySQL system tables and data dictionary tables also differ in how they are upgraded. The MySQL server manages data dictionary upgrades. See [How the Data Dictionary is Upgraded](#page-173-1). Upgrading MySQL system tables requires running the full MySQL upgrade procedure. See Section 3.4, "What the MySQL Upgrade Process Upgrades".

## <span id="page-173-1"></span>**How the Data Dictionary is Upgraded**

New versions of MySQL may include changes to data dictionary table definitions. Such changes are present in newly installed versions of MySQL, but when performing an in-place upgrade of MySQL binaries, changes are applied when the MySQL server is restarted using the new binaries. At startup, the data dictionary version of the server is compared to the version information stored in the data dictionary to determine if data dictionary tables should be upgraded. If an upgrade is necessary and supported, the server creates data dictionary tables with updated definitions, copies persisted metadata to the new tables, atomically replaces the old tables with the new ones, and reinitializes the data dictionary. If an upgrade is not necessary, startup continues without updating the data dictionary tables.

Upgrade of data dictionary tables is an atomic operation, which means that all of the data dictionary tables are upgraded as necessary or the operation fails. If the upgrade operation fails, server startup fails with an error. In this case, the old server binaries can be used with the old data directory to start the server. When the new server binaries are used again to start the server, the data dictionary upgrade is reattempted.

Generally, after data dictionary tables are successfully upgraded, it is not possible to restart the server using the old server binaries. As a result, downgrading MySQL server binaries to a previous MySQL version is not supported after data dictionary tables are upgraded.

The mysqld --no-dd-upgrade option can be used to prevent automatic upgrade of data dictionary tables at startup. When --no-dd-upgrade is specified, and the server finds that the data dictionary version of the server is different from the version stored in the data dictionary, startup fails with an error stating that the data dictionary upgrade is prohibited.

# **Viewing Data Dictionary Tables Using a Debug Build of MySQL**

Data dictionary tables are protected by default but can be accessed by compiling MySQL with debugging support (using the -DWITH\_DEBUG=1 CMake option) and specifying the +d,skip\_dd\_table\_access\_check debug option and modifier. For information about compiling debug builds, see Section 7.9.1.1, "Compiling MySQL for Debugging".

![](_page_173_Picture_9.jpeg)

#### **Warning**

Modifying or writing to data dictionary tables directly is not recommended and may render your MySQL instance inoperable.

After compiling MySQL with debugging support, use this SET statement to make data dictionary tables visible to the mysql client session:

```
mysql> SET SESSION debug='+d,skip_dd_table_access_check';
```

Use this query to retrieve a list of data dictionary tables:

```
mysql> SELECT name, schema_id, hidden, type FROM mysql.tables where schema_id=1 AND hidden='System';
```

Use [SHOW CREATE TABLE](#page-103-0) to view data dictionary table definitions. For example:

```
mysql> SHOW CREATE TABLE mysql.catalogs\G
```

# <span id="page-173-0"></span>**16.2 Removal of File-based Metadata Storage**

In previous MySQL releases, dictionary data was partially stored in metadata files. Issues with filebased metadata storage included expensive file scans, susceptibility to file system-related bugs,

complex code for handling of replication and crash recovery failure states, and a lack of extensibility that made it difficult to add metadata for new features and relational objects.

The metadata files listed below are removed from MySQL. Unless otherwise noted, data previously stored in metadata files is now stored in data dictionary tables.

- .frm files: Table metadata files. With the removal of .frm files:
  - The 64KB table definition size limit imposed by the .frm file structure is removed.
  - The Information Schema TABLES table's VERSION column reports a hardcoded value of 10, which is the last .frm file version used in MySQL 5.7.
- .par files: Partition definition files. InnoDB stopped using partition definition files in MySQL 5.7 with the introduction of native partitioning support for InnoDB tables.
- .TRN files: Trigger namespace files.
- .TRG files: Trigger parameter files.
- .isl files: InnoDB Symbolic Link files containing the location of file-per-table tablespace files created outside of the data directory.
- db.opt files: Database configuration files. These files, one per database directory, contained database default character set attributes.
- ddl\_log.log file: The file contained records of metadata operations generated by data definition statements such as DROP TABLE and ALTER TABLE.

# <span id="page-174-0"></span>**16.3 Transactional Storage of Dictionary Data**

The data dictionary schema stores dictionary data in transactional (InnoDB) tables. Data dictionary tables are located in the mysql database together with non-data dictionary system tables.

Data dictionary tables are created in a single InnoDB tablespace named mysql.ibd, which resides in the MySQL data directory. The mysql.ibd tablespace file must reside in the MySQL data directory and its name cannot be modified or used by another tablespace.

Dictionary data is protected by the same commit, rollback, and crash-recovery capabilities that protect user data that is stored in InnoDB tables.

# <span id="page-174-1"></span>**16.4 Dictionary Object Cache**

The dictionary object cache is a shared global cache that stores previously accessed data dictionary objects in memory to enable object reuse and minimize disk I/O. Similar to other cache mechanisms used by MySQL, the dictionary object cache uses an LRU-based eviction strategy to evict least recently used objects from memory.

The dictionary object cache comprises cache partitions that store different object types. Some cache partition size limits are configurable, whereas others are hardcoded.

- **tablespace definition cache partition**: Stores tablespace definition objects. The tablespace\_definition\_cache option sets a limit for the number of tablespace definition objects that can be stored in the dictionary object cache. The default value is 256.
- **schema definition cache partition**: Stores schema definition objects. The schema\_definition\_cache option sets a limit for the number of schema definition objects that can be stored in the dictionary object cache. The default value is 256.
- **table definition cache partition**: Stores table definition objects. The object limit is set to the value of max\_connections, which has a default value of 151.

The table definition cache partition exists in parallel with the table definition cache that is configured using the table\_definition\_cache configuration option. Both caches store table definitions but serve different parts of the MySQL server. Objects in one cache have no dependence on the existence of objects in the other.

• **stored program definition cache partition**: Stores stored program definition objects. The stored\_program\_definition\_cache option sets a limit for the number of stored program definition objects that can be stored in the dictionary object cache. The default value is 256.

The stored program definition cache partition exists in parallel with the stored procedure and stored function caches that are configured using the stored\_program\_cache option.

The stored\_program\_cache option sets a soft upper limit for the number of cached stored procedures or functions per connection, and the limit is checked each time a connection executes a stored procedure or function. The stored program definition cache partition, on the other hand, is a shared cache that stores stored program definition objects for other purposes. The existence of objects in the stored program definition cache partition has no dependence on the existence of objects in the stored procedure cache or stored function cache, and vice versa.

- **character set definition cache partition**: Stores character set definition objects and has a hardcoded object limit of 256.
- **collation definition cache partition**: Stores collation definition objects and has a hardcoded object limit of 256.

For information about valid values for dictionary object cache configuration options, refer to Section 7.1.8, "Server System Variables".

# <span id="page-175-0"></span>**16.5 INFORMATION\_SCHEMA and Data Dictionary Integration**

With the introduction of the data dictionary, the following INFORMATION\_SCHEMA tables are implemented as views on data dictionary tables:

- CHARACTER\_SETS
- CHECK\_CONSTRAINTS
- COLLATIONS
- COLLATION\_CHARACTER\_SET\_APPLICABILITY
- COLUMNS
- COLUMN\_STATISTICS
- EVENTS
- FILES
- INNODB\_COLUMNS
- INNODB\_DATAFILES
- INNODB\_FIELDS
- INNODB\_FOREIGN
- INNODB\_FOREIGN\_COLS
- INNODB\_INDEXES
- INNODB\_TABLES
- INNODB\_TABLESPACES

- INNODB\_TABLESPACES\_BRIEF
- INNODB\_TABLESTATS
- KEY\_COLUMN\_USAGE
- KEYWORDS
- PARAMETERS
- PARTITIONS
- REFERENTIAL\_CONSTRAINTS
- RESOURCE\_GROUPS
- ROUTINES
- SCHEMATA
- STATISTICS
- ST\_GEOMETRY\_COLUMNS
- ST\_SPATIAL\_REFERENCE\_SYSTEMS
- TABLES
- TABLE\_CONSTRAINTS
- TRIGGERS
- VIEWS
- VIEW\_ROUTINE\_USAGE
- VIEW\_TABLE\_USAGE

Queries on those tables are now more efficient because they obtain information from data dictionary tables rather than by other, slower means. In particular, for each INFORMATION\_SCHEMA table that is a view on data dictionary tables:

- The server no longer must create a temporary table for each query of the INFORMATION\_SCHEMA table.
- When the underlying data dictionary tables store values previously obtained by directory scans (for example, to enumerate database names or table names within databases) or file-opening operations (for example, to read information from .frm files), INFORMATION\_SCHEMA queries for those values now use table lookups instead. (Additionally, even for a non-view INFORMATION\_SCHEMA table, values such as database and table names are retrieved by lookups from the data dictionary and do not require directory or file scans.)
- Indexes on the underlying data dictionary tables permit the optimizer to construct efficient query execution plans, something not true for the previous implementation that processed the INFORMATION\_SCHEMA table using a temporary table per query.

The preceding improvements also apply to [SHOW](#page-95-1) statements that display information corresponding to the INFORMATION\_SCHEMA tables that are views on data dictionary tables. For example, [SHOW](#page-106-0) [DATABASES](#page-106-0) displays the same information as the SCHEMATA table.

In addition to the introduction of views on data dictionary tables, table statistics contained in the STATISTICS and TABLES tables is now cached to improve INFORMATION\_SCHEMA query performance. The information\_schema\_stats\_expiry system variable defines the period of time before cached table statistics expire. The default is 86400 seconds (24 hours). If there are no cached statistics or statistics have expired, statistics are retrieved from storage engine when querying table statistics columns. To update cached values at any time for a given table, use [ANALYZE TABLE](#page-69-0)

information\_schema\_stats\_expiry can be set to 0 to have INFORMATION\_SCHEMA queries retrieve the latest statistics directly from the storage engine, which is not as fast as retrieving cached statistics.

For more information, see Section 10.2.3, "Optimizing INFORMATION\_SCHEMA Queries".

INFORMATION\_SCHEMA tables in MySQL 8.0 are closely tied to the data dictionary, resulting in several usage differences. See [Section 16.7, "Data Dictionary Usage Differences"](#page-177-1).

# <span id="page-177-0"></span>**16.6 Serialized Dictionary Information (SDI)**

In addition to storing metadata about database objects in the data dictionary, MySQL stores it in serialized form. This data is referred to as serialized dictionary information (SDI). InnoDB stores SDI data within its tablespace files. NDBCLUSTER stores SDI data in the NDB dictionary. Other storage engines store SDI data in .sdi files that are created for a given table in the table's database directory. SDI data is generated in a compact JSON format.

Serialized dictionary information (SDI) is present in all InnoDB tablespace files except for temporary tablespace and undo tablespace files. SDI records in an InnoDB tablespace file only describe table and tablespace objects contained within the tablespace.

SDI data is updated by DDL operations on a table or [CHECK TABLE FOR UPGRADE](#page-74-1). SDI data is not updated when the MySQL server is upgraded to a new release or version.

The presence of SDI data provides metadata redundancy. For example, if the data dictionary becomes unavailable, object metadata can be extracted directly from InnoDB tablespace files using the ibd2sdi tool.

For InnoDB, an SDI record requires a single index page, which is 16KB in size by default. However, SDI data is compressed to reduce the storage footprint.

For partitioned InnoDB tables comprised of multiple tablespaces, SDI data is stored in the tablespace file of the first partition.

The MySQL server uses an internal API that is accessed during DDL operations to create and maintain SDI records.

The IMPORT TABLE statement imports MyISAM tables based on information contained in .sdi files. For more information, see Section 15.2.6, "IMPORT TABLE Statement".

# <span id="page-177-1"></span>**16.7 Data Dictionary Usage Differences**

Use of a data dictionary-enabled MySQL server entails some operational differences compared to a server that does not have a data dictionary:

- Previously, enabling the innodb\_read\_only system variable prevented creating and dropping tables only for the InnoDB storage engine. As of MySQL 8.0, enabling innodb\_read\_only prevents these operations for all storage engines. Table creation and drop operations for any storage engine modify data dictionary tables in the mysql system database, but those tables use the InnoDB storage engine and cannot be modified when innodb\_read\_only is enabled. The same principle applies to other table operations that require modifying data dictionary tables. Examples:
  - [ANALYZE TABLE](#page-69-0) fails because it updates table statistics, which are stored in the data dictionary.
  - ALTER TABLE tbl\_name ENGINE=engine\_name fails because it updates the storage engine designation, which is stored in the data dictionary.

![](_page_177_Picture_18.jpeg)

#### **Note**

Enabling innodb\_read\_only also has important implications for nondata dictionary tables in the mysql system database. For details, see the description of innodb\_read\_only in Section 17.14, "InnoDB Startup Options and System Variables"

- Previously, tables in the mysql system database were visible to DML and DDL statements. As of MySQL 8.0, data dictionary tables are invisible and cannot be modified or queried directly. However, in most cases there are corresponding INFORMATION\_SCHEMA tables that can be queried instead. This enables the underlying data dictionary tables to be changed as server development proceeds, while maintaining a stable INFORMATION\_SCHEMA interface for application use.
- INFORMATION\_SCHEMA tables in MySQL 8.0 are closely tied to the data dictionary, resulting in several usage differences:
  - Previously, INFORMATION\_SCHEMA queries for table statistics in the STATISTICS and TABLES tables retrieved statistics directly from storage engines. As of MySQL 8.0, cached table statistics are used by default. The information\_schema\_stats\_expiry system variable defines the period of time before cached table statistics expire. The default is 86400 seconds (24 hours). (To update the cached values at any time for a given table, use [ANALYZE TABLE](#page-69-0).) If there are no cached statistics or statistics have expired, statistics are retrieved from storage engines when querying table statistics columns. To always retrieve the latest statistics directly from storage engines, set information\_schema\_stats\_expiry to 0. For more information, see Section 10.2.3, "Optimizing INFORMATION\_SCHEMA Queries".
  - Several INFORMATION\_SCHEMA tables are views on data dictionary tables, which enables the optimizer to use indexes on those underlying tables. Consequently, depending on optimizer choices, the row order of results for INFORMATION\_SCHEMA queries might differ from previous results. If a query result must have specific row ordering characteristics, include an ORDER BY clause.
  - Queries on INFORMATION\_SCHEMA tables may return column names in a different lettercase than in earlier MySQL series. Applications should test result set column names in case-insensitive fashion. If that is not feasible, a workaround is to use column aliases in the select list that return column names in the required lettercase. For example:

```
SELECT TABLE_SCHEMA AS table_schema, TABLE_NAME AS table_name
FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users';
```

- mysqldump and mysqlpump no longer dump the INFORMATION\_SCHEMA database, even if explicitly named on the command line.
- CREATE TABLE dst\_tbl LIKE src\_tbl requires that src\_tbl be a base table and fails if it is an INFORMATION\_SCHEMA table that is a view on data dictionary tables.
- Previously, result set headers of columns selected from INFORMATION\_SCHEMA tables used the capitalization specified in the query. This query produces a result set with a header of table\_name:

```
SELECT table_name FROM INFORMATION_SCHEMA.TABLES;
```

As of MySQL 8.0, these headers are capitalized; the preceding query produces a result set with a header of TABLE\_NAME. If necessary, a column alias can be used to achieve a different lettercase. For example:

```
SELECT table_name AS 'table_name' FROM INFORMATION_SCHEMA.TABLES;
```

- The data directory affects how mysqldump and mysqlpump dump information from the mysql system database:
  - Previously, it was possible to dump all tables in the mysql system database. As of MySQL 8.0, mysqldump and mysqlpump dump only non-data dictionary tables in that database.
  - Previously, the --routines and --events options were not required to include stored routines and events when using the --all-databases option: The dump included the mysql system database, and therefore also the proc and event tables containing stored routine and event definitions. As of MySQL 8.0, the event and proc tables are not used. Definitions for the corresponding objects are stored in data dictionary tables, but those tables are not dumped. To include stored routines and events in a dump made using --all-databases, use the - routines and --events options explicitly.
  - Previously, the --routines option required the SELECT privilege for the proc table. As of MySQL 8.0, that table is not used; --routines requires the global SELECT privilege instead.
  - Previously, it was possible to dump stored routine and event definitions together with their creation and modification timestamps, by dumping the proc and event tables. As of MySQL 8.0, those tables are not used, so it is not possible to dump timestamps.
- Previously, creating a stored routine that contains illegal characters produced a warning. As of MySQL 8.0, this is an error.

# <span id="page-179-0"></span>**16.8 Data Dictionary Limitations**

This section describes temporary limitations introduced with the MySQL data dictionary.

- Manual creation of database directories under the data directory (for example, with mkdir) is unsupported. Manually created database directories are not recognized by the MySQL Server.
- DDL operations take longer due to writing to storage, undo logs, and redo logs instead of .frm files.

# <span id="page-180-0"></span>Chapter 17 The InnoDB Storage Engine

# **Table of Contents**

| 17.1         | Introduction to innobe                                                       | 3152 |
|--------------|------------------------------------------------------------------------------|------|
|              | 17.1.1 Benefits of Using InnoDB Tables                                       | 3154 |
|              | 17.1.2 Best Practices for InnoDB Tables                                      | 3155 |
|              | 17.1.3 Verifying that InnoDB is the Default Storage Engine                   | 3155 |
|              | 17.1.4 Testing and Benchmarking with InnoDB                                  |      |
| 17.2         | InnoDB and the ACID Model                                                    |      |
|              | InnoDB Multi-Versioning                                                      |      |
|              | InnoDB Architecture                                                          |      |
|              | InnoDB In-Memory Structures                                                  |      |
|              | 17.5.1 Buffer Pool                                                           |      |
|              | 17.5.2 Change Buffer                                                         |      |
|              | 17.5.3 Adaptive Hash Index                                                   |      |
|              | 17.5.4 Log Buffer                                                            |      |
| 17 6         | InnoDB On-Disk Structures                                                    |      |
| 17.0         | 17.6.1 Tables                                                                |      |
|              | 17.6.2 Indexes                                                               |      |
|              | 17.6.3 Tablespaces                                                           |      |
|              | 17.6.4 Doublewrite Buffer                                                    |      |
|              | 17.6.5 Redo Log                                                              |      |
|              | 17.6.6 Undo Logs                                                             |      |
| 177          | InnoDB Locking and Transaction Model                                         |      |
| 17.7         | 17.7.1 InnoDB Locking                                                        |      |
|              | 17.7.2 InnoDB Transaction Model                                              |      |
|              | 17.7.3 Locks Set by Different SQL Statements in InnoDB                       | 2245 |
|              |                                                                              |      |
|              | 17.7.4 Phantom Rows                                                          |      |
|              |                                                                              |      |
| 4 <b>7</b> 0 | 17.7.6 Transaction Scheduling                                                |      |
| 17.8         | InnoDB Configuration                                                         |      |
|              | 17.8.1 InnoDB Startup Configuration                                          | 3233 |
|              | 17.8.2 Configuring InnoDB for Read-Only Operation                            |      |
|              | 17.8.3 InnoDB Buffer Pool Configuration                                      |      |
|              | 17.8.4 Configuring Thread Concurrency for InnoDB                             |      |
|              | 17.8.5 Configuring the Number of Background InnoDB I/O Threads               |      |
|              | 17.8.6 Using Asynchronous I/O on Linux                                       |      |
|              | 17.8.7 Configuring InnoDB I/O Capacity                                       |      |
|              | 17.8.8 Configuring Spin Lock Polling                                         |      |
|              | 17.8.9 Purge Configuration                                                   |      |
|              | 17.8.10 Configuring Optimizer Statistics for InnoDB                          |      |
|              | 17.8.11 Configuring the Merge Threshold for Index Pages                      |      |
|              | 17.8.12 Enabling Automatic InnoDB Configuration for a Dedicated MySQL Server |      |
| 17.9         | InnoDB Table and Page Compression                                            |      |
|              | 17.9.1 InnoDB Table Compression                                              |      |
|              | 17.9.2 InnoDB Page Compression                                               |      |
|              | 0 InnoDB Row Formats                                                         | 3316 |
| 17.1°        | 1 InnoDB Disk I/O and File Space Management                                  |      |
|              | 17.11.1 InnoDB Disk I/O                                                      | 3323 |
|              | 17.11.2 File Space Management                                                | 3323 |
|              | 17.11.3 InnoDB Checkpoints                                                   | 3325 |
|              | 17.11.4 Defragmenting a Table                                                | 3325 |
|              | 17.11.5 Reclaiming Disk Space with TRUNCATE TABLE                            | 3326 |
| 17.12        | 2 InnoDB and Online DDL                                                      |      |
|              | 17.12.1 Online DDL Operations                                                | 3327 |
|              |                                                                              |      |

| 17.12.2 Online DDL Performance and Concurrency 3343                                     |      |
|-----------------------------------------------------------------------------------------|------|
| 17.12.3 Online DDL Space Requirements 3346                                              |      |
| 17.12.4 Online DDL Memory Management 3347                                               |      |
| 17.12.5 Configuring Parallel Threads for Online DDL Operations 3347                     |      |
| 17.12.6 Simplifying DDL Statements with Online DDL 3348                                 |      |
| 17.12.7 Online DDL Failure Conditions 3348                                              |      |
| 17.12.8 Online DDL Limitations                                                          | 3349 |
| 17.13 InnoDB Data-at-Rest Encryption 3349                                               |      |
| 17.14 InnoDB Startup Options and System Variables                                       | 3358 |
| 17.15 InnoDB INFORMATION_SCHEMA Tables 3448                                             |      |
| 17.15.1 InnoDB INFORMATION_SCHEMA Tables about Compression 3448                         |      |
| 17.15.2 InnoDB INFORMATION_SCHEMA Transaction and Locking Information 3449              |      |
| 17.15.3 InnoDB INFORMATION_SCHEMA Schema Object Tables 3457                             |      |
| 17.15.4 InnoDB INFORMATION_SCHEMA FULLTEXT Index Tables 3462                            |      |
| 17.15.5 InnoDB INFORMATION_SCHEMA Buffer Pool Tables 3465                               |      |
| 17.15.6 InnoDB INFORMATION_SCHEMA Metrics Table 3469                                    |      |
|                                                                                         |      |
| 17.15.7 InnoDB INFORMATION_SCHEMA Temporary Table Info Table 3478                       |      |
| 17.15.8 Retrieving InnoDB Tablespace Metadata from INFORMATION_SCHEMA.FILES 3479        |      |
| 17.16 InnoDB Integration with MySQL Performance Schema 3480                             |      |
| 17.16.1 Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance Schema 3482 |      |
| 17.16.2 Monitoring InnoDB Mutex Waits Using Performance Schema 3484                     |      |
| 17.17 InnoDB Monitors 3487                                                              |      |
| 17.17.1 InnoDB Monitor Types 3487                                                       |      |
| 17.17.2 Enabling InnoDB Monitors 3488                                                   |      |
| 17.17.3 InnoDB Standard Monitor and Lock Monitor Output 3489                            |      |
| 17.18 InnoDB Backup and Recovery                                                        | 3494 |
| 17.18.1 InnoDB Backup 3494                                                              |      |
| 17.18.2 InnoDB Recovery 3495                                                            |      |
| 17.19 InnoDB and MySQL Replication 3497                                                 |      |
| 17.20 InnoDB memcached Plugin 3499                                                      |      |
| 17.20.1 Benefits of the InnoDB memcached Plugin 3499                                    |      |
| 17.20.2 InnoDB memcached Architecture 3500                                              |      |
| 17.20.3 Setting Up the InnoDB memcached Plugin 3502                                     |      |
| 17.20.4 InnoDB memcached Multiple get and Range Query Support 3507                      |      |
| 17.20.5 Security Considerations for the InnoDB memcached Plugin 3509                    |      |
| 17.20.6 Writing Applications for the InnoDB memcached Plugin 3511                       |      |
| 17.20.7 The InnoDB memcached Plugin and Replication                                     | 3523 |
| 17.20.8 InnoDB memcached Plugin Internals                                               | 3526 |
| 17.20.9 Troubleshooting the InnoDB memcached Plugin 3531                                |      |
| 17.21 InnoDB Troubleshooting 3533                                                       |      |
| 17.21.1 Troubleshooting InnoDB I/O Problems 3534                                        |      |
| 17.21.2 Troubleshooting Recovery Failures 3534                                          |      |
| 17.21.3 Forcing InnoDB Recovery                                                         | 3534 |
| 17.21.4 Troubleshooting InnoDB Data Dictionary Operations 3536                          |      |
| 17.21.5 InnoDB Error Handling 3537                                                      |      |
| 17.22 InnoDB Limits 3537                                                                |      |
| 17.23 InnoDB Restrictions and Limitations                                               | 3539 |

# <span id="page-181-0"></span>**17.1 Introduction to InnoDB**

InnoDB is a general-purpose storage engine that balances high reliability and high performance. In MySQL 8.0, InnoDB is the default MySQL storage engine. Unless you have configured a different default storage engine, issuing a CREATE TABLE statement without an ENGINE clause creates an InnoDB table.

# **Key Advantages of InnoDB**

- Its DML operations follow the ACID model, with transactions featuring commit, rollback, and crashrecovery capabilities to protect user data. See [Section 17.2, "InnoDB and the ACID Model".](#page-185-1)
- Row-level locking and Oracle-style consistent reads increase multi-user concurrency and performance. See Section 17.7, "InnoDB Locking and Transaction Model".
- InnoDB tables arrange your data on disk to optimize queries based on primary keys. Each InnoDB table has a primary key index called the clustered index that organizes the data to minimize I/O for primary key lookups. See Section 17.6.2.1, "Clustered and Secondary Indexes".
- To maintain data integrity, InnoDB supports FOREIGN KEY constraints. With foreign keys, inserts, updates, and deletes are checked to ensure they do not result in inconsistencies across related tables. See Section 15.1.20.5, "FOREIGN KEY Constraints".

**Table 17.1 InnoDB Storage Engine Features**

| Feature                                                                                          | Support                                                                                                                       |
|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| B-tree indexes                                                                                   | Yes                                                                                                                           |
| Backup/point-in-time recovery (Implemented in<br>the server, rather than in the storage engine.) | Yes                                                                                                                           |
| Cluster database support                                                                         | No                                                                                                                            |
| Clustered indexes                                                                                | Yes                                                                                                                           |
| Compressed data                                                                                  | Yes                                                                                                                           |
| Data caches                                                                                      | Yes                                                                                                                           |
| Encrypted data                                                                                   | Yes (Implemented in the server via encryption<br>functions; In MySQL 5.7 and later, data-at-rest<br>encryption is supported.) |
| Foreign key support                                                                              | Yes                                                                                                                           |
| Full-text search indexes                                                                         | Yes (Support for FULLTEXT indexes is available<br>in MySQL 5.6 and later.)                                                    |
| Geospatial data type support                                                                     | Yes                                                                                                                           |
| Geospatial indexing support                                                                      | Yes (Support for geospatial indexing is available in<br>MySQL 5.7 and later.)                                                 |
| Hash indexes                                                                                     | No (InnoDB utilizes hash indexes internally for its<br>Adaptive Hash Index feature.)                                          |
| Index caches                                                                                     | Yes                                                                                                                           |
| Locking granularity                                                                              | Row                                                                                                                           |
| MVCC                                                                                             | Yes                                                                                                                           |
| Replication support (Implemented in the server,<br>rather than in the storage engine.)           | Yes                                                                                                                           |
| Storage limits                                                                                   | 64TB                                                                                                                          |
| T-tree indexes                                                                                   | No                                                                                                                            |
| Transactions                                                                                     | Yes                                                                                                                           |
| Update statistics for data dictionary                                                            | Yes                                                                                                                           |

To compare the features of InnoDB with other storage engines provided with MySQL, see the Storage Engine Features table in Chapter 18, Alternative Storage Engines.

## **InnoDB Enhancements and New Features**

For information about InnoDB enhancements and new features, refer to:

- The InnoDB enhancements list in Section 1.3, "What Is New in MySQL 8.0".
- The [Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/)

## **Additional InnoDB Information and Resources**

- For InnoDB-related terms and definitions, see the MySQL Glossary.
- For a forum dedicated to the InnoDB storage engine, see [MySQL Forums::InnoDB.](http://forums.mysql.com/list.php?22)
- InnoDB is published under the same GNU GPL License Version 2 (of June 1991) as MySQL. For more information on MySQL licensing, see<http://www.mysql.com/company/legal/licensing/>.

# <span id="page-183-0"></span>**17.1.1 Benefits of Using InnoDB Tables**

InnoDB tables have the following benefits:

- If the server unexpectedly exits because of a hardware or software issue, regardless of what was happening in the database at the time, you don't need to do anything special after restarting the database. InnoDB crash recovery automatically finalizes changes that were committed before the time of the crash, and undoes changes that were in process but not committed, permitting you to restart and continue from where you left off. See Section 17.18.2, "InnoDB Recovery".
- The InnoDB storage engine maintains its own buffer pool that caches table and index data in main memory as data is accessed. Frequently used data is processed directly from memory. This cache applies to many types of information and speeds up processing. On dedicated database servers, up to 80% of physical memory is often assigned to the buffer pool. See [Section 17.5.1, "Buffer Pool"](#page-188-2).
- If you split up related data into different tables, you can set up foreign keys that enforce referential integrity. See Section 15.1.20.5, "FOREIGN KEY Constraints".
- If data becomes corrupted on disk or in memory, a checksum mechanism alerts you to the bogus data before you use it. The innodb\_checksum\_algorithm variable defines the checksum algorithm used by InnoDB.
- When you design a database with appropriate primary key columns for each table, operations involving those columns are automatically optimized. It is very fast to reference the primary key columns in WHERE clauses, ORDER BY clauses, GROUP BY clauses, and join operations. See Section 17.6.2.1, "Clustered and Secondary Indexes".
- Inserts, updates, and deletes are optimized by an automatic mechanism called change buffering. InnoDB not only allows concurrent read and write access to the same table, it caches changed data to streamline disk I/O. See [Section 17.5.2, "Change Buffer".](#page-193-0)
- Performance benefits are not limited to large tables with long-running queries. When the same rows are accessed over and over from a table, the Adaptive Hash Index takes over to make these lookups even faster, as if they came out of a hash table. See [Section 17.5.3, "Adaptive Hash Index".](#page-196-0)
- You can compress tables and associated indexes. See Section 17.9, "InnoDB Table and Page Compression".
- You can encrypt your data. See Section 17.13, "InnoDB Data-at-Rest Encryption".
- You can create and drop indexes and perform other DDL operations with much less impact on performance and availability. See Section 17.12.1, "Online DDL Operations".
- Truncating a file-per-table tablespace is very fast and can free up disk space for the operating system to reuse rather than only InnoDB. See Section 17.6.3.2, "File-Per-Table Tablespaces".

- The storage layout for table data is more efficient for BLOB and long text fields, with the DYNAMIC row format. See Section 17.10, "InnoDB Row Formats".
- You can monitor the internal workings of the storage engine by querying INFORMATION\_SCHEMA tables. See Section 17.15, "InnoDB INFORMATION\_SCHEMA Tables".
- You can monitor the performance details of the storage engine by querying Performance Schema tables. See Section 17.16, "InnoDB Integration with MySQL Performance Schema".
- You can mix InnoDB tables with tables from other MySQL storage engines, even within the same statement. For example, you can use a join operation to combine data from InnoDB and MEMORY tables in a single query.
- InnoDB has been designed for CPU efficiency and maximum performance when processing large data volumes.
- InnoDB tables can handle large quantities of data, even on operating systems where file size is limited to 2GB.

For InnoDB-specific tuning techniques you can apply to your MySQL server and application code, see Section 10.5, "Optimizing for InnoDB Tables".

## <span id="page-184-0"></span>**17.1.2 Best Practices for InnoDB Tables**

This section describes best practices when using InnoDB tables.

- Specify a primary key for every table using the most frequently queried column or columns, or an auto-increment value if there is no obvious primary key.
- Use joins wherever data is pulled from multiple tables based on identical ID values from those tables. For fast join performance, define foreign keys on the join columns, and declare those columns with the same data type in each table. Adding foreign keys ensures that referenced columns are indexed, which can improve performance. Foreign keys also propagate deletes and updates to all affected tables, and prevent insertion of data in a child table if the corresponding IDs are not present in the parent table.
- Turn off autocommit. Committing hundreds of times a second puts a cap on performance (limited by the write speed of your storage device).
- Group sets of related DML operations into transactions by bracketing them with START TRANSACTION and COMMIT statements. While you don't want to commit too often, you also don't want to issue huge batches of INSERT, UPDATE, or DELETE statements that run for hours without committing.
- Do not use LOCK TABLES statements. InnoDB can handle multiple sessions all reading and writing to the same table at once without sacrificing reliability or high performance. To get exclusive write access to a set of rows, use the SELECT ... FOR UPDATE syntax to lock just the rows you intend to update.
- Enable the innodb\_file\_per\_table variable or use general tablespaces to put the data and indexes for tables into separate files instead of the system tablespace. The innodb\_file\_per\_table variable is enabled by default.
- Evaluate whether your data and access patterns benefit from the InnoDB table or page compression features. You can compress InnoDB tables without sacrificing read/write capability.
- Run the server with the --sql\_mode=NO\_ENGINE\_SUBSTITUTION option to prevent tables from being created with storage engines that you do not want to use.

# <span id="page-184-1"></span>**17.1.3 Verifying that InnoDB is the Default Storage Engine**

Issue the [SHOW ENGINES](#page-110-0) statement to view the available MySQL storage engines. Look for DEFAULT in the SUPPORT column.

```
mysql> SHOW ENGINES;
```

Alternatively, query the Information Schema ENGINES table.

```
mysql> SELECT * FROM INFORMATION_SCHEMA.ENGINES;
```

## <span id="page-185-0"></span>**17.1.4 Testing and Benchmarking with InnoDB**

If InnoDB is not the default storage engine, you can determine if your database server and applications work correctly with InnoDB by restarting the server with --default-storage-engine=InnoDB defined on the command line or with default-storage-engine=innodb defined in the [mysqld] section of the MySQL server option file.

Since changing the default storage engine only affects newly created tables, run your application installation and setup steps to confirm that everything installs properly, then exercise the application features to make sure the data loading, editing, and querying features work. If a table relies on a feature that is specific to another storage engine, you receive an error. In this case, add the ENGINE=other\_engine\_name clause to the CREATE TABLE statement to avoid the error.

If you did not make a deliberate decision about the storage engine, and you want to preview how certain tables work when created using InnoDB, issue the command ALTER TABLE table\_name ENGINE=InnoDB; for each table. Alternatively, to run test queries and other statements without disturbing the original table, make a copy:

```
CREATE TABLE ... ENGINE=InnoDB AS SELECT * FROM other_engine_table;
```

To assess performance with a full application under a realistic workload, install the latest MySQL server and run benchmarks.

Test the full application lifecycle, from installation, through heavy usage, and server restart. Kill the server process while the database is busy to simulate a power failure, and verify that the data is recovered successfully when you restart the server.

Test any replication configurations, especially if you use different MySQL versions and options on the source server and replicas.

# <span id="page-185-1"></span>**17.2 InnoDB and the ACID Model**

The ACID model is a set of database design principles that emphasize aspects of reliability that are important for business data and mission-critical applications. MySQL includes components such as the InnoDB storage engine that adhere closely to the ACID model so that data is not corrupted and results are not distorted by exceptional conditions such as software crashes and hardware malfunctions. When you rely on ACID-compliant features, you do not need to reinvent the wheel of consistency checking and crash recovery mechanisms. In cases where you have additional software safeguards, ultrareliable hardware, or an application that can tolerate a small amount of data loss or inconsistency, you can adjust MySQL settings to trade some of the ACID reliability for greater performance or throughput.

The following sections discuss how MySQL features, in particular the InnoDB storage engine, interact with the categories of the ACID model:

- **A**: atomicity.
- **C**: consistency.
- **I:**: isolation.
- **D**: durability.

# **Atomicity**

The **atomicity** aspect of the ACID model mainly involves InnoDB transactions. Related MySQL features include:

- The autocommit setting.
- The COMMIT statement.
- The ROLLBACK statement.

## **Consistency**

The **consistency** aspect of the ACID model mainly involves internal InnoDB processing to protect data from crashes. Related MySQL features include:

- The InnoDB doublewrite buffer. See Section 17.6.4, "Doublewrite Buffer".
- InnoDB crash recovery. See InnoDB Crash Recovery.

## **Isolation**

The **isolation** aspect of the ACID model mainly involves InnoDB transactions, in particular the isolation level that applies to each transaction. Related MySQL features include:

- The autocommit setting.
- Transaction isolation levels and the SET TRANSACTION statement. See Section 17.7.2.1, "Transaction Isolation Levels".
- The low-level details of InnoDB locking. Details can be viewed in the INFORMATION\_SCHEMA tables (see Section 17.15.2, "InnoDB INFORMATION\_SCHEMA Transaction and Locking Information") and Performance Schema data\_locks and data\_lock\_waits tables.

# **Durability**

The **durability** aspect of the ACID model involves MySQL software features interacting with your particular hardware configuration. Because of the many possibilities depending on the capabilities of your CPU, network, and storage devices, this aspect is the most complicated to provide concrete guidelines for. (And those guidelines might take the form of "buy new hardware".) Related MySQL features include:

- The InnoDB doublewrite buffer. See Section 17.6.4, "Doublewrite Buffer".
- The innodb\_flush\_log\_at\_trx\_commit variable.
- The sync\_binlog variable.
- The innodb\_file\_per\_table variable.
- The write buffer in a storage device, such as a disk drive, SSD, or RAID array.
- A battery-backed cache in a storage device.
- The operating system used to run MySQL, in particular its support for the fsync() system call.
- An uninterruptible power supply (UPS) protecting the electrical power to all computer servers and storage devices that run MySQL servers and store MySQL data.
- Your backup strategy, such as frequency and types of backups, and backup retention periods.
- For distributed or hosted data applications, the particular characteristics of the data centers where the hardware for the MySQL servers is located, and network connections between the data centers.

# <span id="page-186-0"></span>**17.3 InnoDB Multi-Versioning**

InnoDB is a multi-version storage engine. It keeps information about old versions of changed rows to support transactional features such as concurrency and rollback. This information is stored in undo

tablespaces in a data structure called a rollback segment. See Section 17.6.3.4, "Undo Tablespaces". InnoDB uses the information in the rollback segment to perform the undo operations needed in a transaction rollback. It also uses the information to build earlier versions of a row for a consistent read. See Section 17.7.2.3, "Consistent Nonlocking Reads".

Internally, InnoDB adds three fields to each row stored in the database:

- A 6-byte DB\_TRX\_ID field indicates the transaction identifier for the last transaction that inserted or updated the row. Also, a deletion is treated internally as an update where a special bit in the row is set to mark it as deleted.
- A 7-byte DB\_ROLL\_PTR field called the roll pointer. The roll pointer points to an undo log record written to the rollback segment. If the row was updated, the undo log record contains the information necessary to rebuild the content of the row before it was updated.
- A 6-byte DB\_ROW\_ID field contains a row ID that increases monotonically as new rows are inserted. If InnoDB generates a clustered index automatically, the index contains row ID values. Otherwise, the DB\_ROW\_ID column does not appear in any index.

Undo logs in the rollback segment are divided into insert and update undo logs. Insert undo logs are needed only in transaction rollback and can be discarded as soon as the transaction commits. Update undo logs are used also in consistent reads, but they can be discarded only after there is no transaction present for which InnoDB has assigned a snapshot that in a consistent read could require the information in the update undo log to build an earlier version of a database row. For additional information about undo logs, see Section 17.6.6, "Undo Logs".

It is recommend that you commit transactions regularly, including transactions that issue only consistent reads. Otherwise, InnoDB cannot discard data from the update undo logs, and the rollback segment may grow too big, filling up the undo tablespace in which it resides. For information about managing undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

The physical size of an undo log record in the rollback segment is typically smaller than the corresponding inserted or updated row. You can use this information to calculate the space needed for your rollback segment.

In the InnoDB multi-versioning scheme, a row is not physically removed from the database immediately when you delete it with an SQL statement. InnoDB only physically removes the corresponding row and its index records when it discards the update undo log record written for the deletion. This removal operation is called a purge, and it is quite fast, usually taking the same order of time as the SQL statement that did the deletion.

If you insert and delete rows in smallish batches at about the same rate in the table, the purge thread can start to lag behind and the table can grow bigger and bigger because of all the "dead" rows, making everything disk-bound and very slow. In such cases, throttle new row operations, and allocate more resources to the purge thread by tuning the innodb\_max\_purge\_lag system variable. For more information, see Section 17.8.9, "Purge Configuration".

# **Multi-Versioning and Secondary Indexes**

InnoDB multiversion concurrency control (MVCC) treats secondary indexes differently than clustered indexes. Records in a clustered index are updated in-place, and their hidden system columns point undo log entries from which earlier versions of records can be reconstructed. Unlike clustered index records, secondary index records do not contain hidden system columns nor are they updated in-place.

When a secondary index column is updated, old secondary index records are delete-marked, new records are inserted, and delete-marked records are eventually purged. When a secondary index record is delete-marked or the secondary index page is updated by a newer transaction, InnoDB looks up the database record in the clustered index. In the clustered index, the record's DB\_TRX\_ID is checked, and the correct version of the record is retrieved from the undo log if the record was modified after the reading transaction was initiated.

If a secondary index record is marked for deletion or the secondary index page is updated by a newer transaction, the covering index technique is not used. Instead of returning values from the index structure, InnoDB looks up the record in the clustered index.

However, if the index condition pushdown (ICP) optimization is enabled, and parts of the WHERE condition can be evaluated using only fields from the index, the MySQL server still pushes this part of the WHERE condition down to the storage engine where it is evaluated using the index. If no matching records are found, the clustered index lookup is avoided. If matching records are found, even among delete-marked records, InnoDB looks up the record in the clustered index.

# <span id="page-188-0"></span>**17.4 InnoDB Architecture**

The following diagram shows in-memory and on-disk structures that comprise the InnoDB storage engine architecture. For information about each structure, see [Section 17.5, "InnoDB In-Memory](#page-188-1) [Structures",](#page-188-1) and [Section 17.6, "InnoDB On-Disk Structures"](#page-197-1).

**Figure 17.1 InnoDB Architecture**

# <span id="page-188-1"></span>**17.5 InnoDB In-Memory Structures**

This section describes InnoDB in-memory structures and related topics.

# <span id="page-188-2"></span>**17.5.1 Buffer Pool**

The buffer pool is an area in main memory where InnoDB caches table and index data as it is accessed. The buffer pool permits frequently used data to be accessed directly from memory, which speeds up processing. On dedicated servers, up to 80% of physical memory is often assigned to the buffer pool.

For efficiency of high-volume read operations, the buffer pool is divided into pages that can potentially hold multiple rows. For efficiency of cache management, the buffer pool is implemented as a linked list of pages; data that is rarely used is aged out of the cache using a variation of the least recently used (LRU) algorithm.

Knowing how to take advantage of the buffer pool to keep frequently accessed data in memory is an important aspect of MySQL tuning.

## **Buffer Pool LRU Algorithm**

The buffer pool is managed as a list using a variation of the LRU algorithm. When room is needed to add a new page to the buffer pool, the least recently used page is evicted and a new page is added to the middle of the list. This midpoint insertion strategy treats the list as two sublists:

- At the head, a sublist of new ("young") pages that were accessed recently
- At the tail, a sublist of old pages that were accessed less recently

**Figure 17.2 Buffer Pool List**

![](_page_189_Picture_8.jpeg)

The algorithm keeps frequently used pages in the new sublist. The old sublist contains less frequently used pages; these pages are candidates for eviction.

By default, the algorithm operates as follows:

- 3/8 of the buffer pool is devoted to the old sublist.
- The midpoint of the list is the boundary where the tail of the new sublist meets the head of the old sublist.

- When InnoDB reads a page into the buffer pool, it initially inserts it at the midpoint (the head of the old sublist). A page can be read because it is required for a user-initiated operation such as an SQL query, or as part of a read-ahead operation performed automatically by InnoDB.
- Accessing a page in the old sublist makes it "young", moving it to the head of the new sublist. If the page was read because it was required by a user-initiated operation, the first access occurs immediately and the page is made young. If the page was read due to a read-ahead operation, the first access does not occur immediately and might not occur at all before the page is evicted.
- As the database operates, pages in the buffer pool that are not accessed "age" by moving toward the tail of the list. Pages in both the new and old sublists age as other pages are made new. Pages in the old sublist also age as pages are inserted at the midpoint. Eventually, a page that remains unused reaches the tail of the old sublist and is evicted.

By default, pages read by queries are immediately moved into the new sublist, meaning they stay in the buffer pool longer. A table scan, performed for a mysqldump operation or a SELECT statement with no WHERE clause, for example, can bring a large amount of data into the buffer pool and evict an equivalent amount of older data, even if the new data is never used again. Similarly, pages that are loaded by the read-ahead background thread and accessed only once are moved to the head of the new list. These situations can push frequently used pages to the old sublist where they become subject to eviction. For information about optimizing this behavior, see Section 17.8.3.3, "Making the Buffer Pool Scan Resistant", and Section 17.8.3.4, "Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)".

InnoDB Standard Monitor output contains several fields in the BUFFER POOL AND MEMORY section regarding operation of the buffer pool LRU algorithm. For details, see [Monitoring the Buffer Pool Using](#page-190-0) [the InnoDB Standard Monitor.](#page-190-0)

## **Buffer Pool Configuration**

You can configure the various aspects of the buffer pool to improve performance.

- Ideally, you set the size of the buffer pool to as large a value as practical, leaving enough memory for other processes on the server to run without excessive paging. The larger the buffer pool, the more InnoDB acts like an in-memory database, reading data from disk once and then accessing the data from memory during subsequent reads. See Section 17.8.3.1, "Configuring InnoDB Buffer Pool Size".
- On 64-bit systems with sufficient memory, you can split the buffer pool into multiple parts to minimize contention for memory structures among concurrent operations. For details, see Section 17.8.3.2, "Configuring Multiple Buffer Pool Instances".
- You can keep frequently accessed data in memory regardless of sudden spikes of activity from operations that would bring large amounts of infrequently accessed data into the buffer pool. For details, see Section 17.8.3.3, "Making the Buffer Pool Scan Resistant".
- You can control how and when to perform read-ahead requests to prefetch pages into the buffer pool asynchronously in anticipation of impending need for them. For details, see Section 17.8.3.4, "Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)".
- You can control when background flushing occurs and whether or not the rate of flushing is dynamically adjusted based on workload. For details, see Section 17.8.3.5, "Configuring Buffer Pool Flushing".
- You can configure how InnoDB preserves the current buffer pool state to avoid a lengthy warmup period after a server restart. For details, see Section 17.8.3.6, "Saving and Restoring the Buffer Pool State".

## <span id="page-190-0"></span>**Monitoring the Buffer Pool Using the InnoDB Standard Monitor**

InnoDB Standard Monitor output, which can be accessed using SHOW ENGINE INNODB STATUS, provides metrics regarding operation of the buffer pool. Buffer pool metrics are located in the BUFFER POOL AND MEMORY section of InnoDB Standard Monitor output:

```
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 2198863872
Dictionary memory allocated 776332
Buffer pool size 131072
Free buffers 124908
Database pages 5720
Old database pages 2071
Modified db pages 910
Pending reads 0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 4, not young 0
0.10 youngs/s, 0.00 non-youngs/s
Pages read 197, created 5523, written 5060
0.00 reads/s, 190.89 creates/s, 244.94 writes/s
Buffer pool hit rate 1000 / 1000, young-making rate 0 / 1000 not
0 / 1000
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read
ahead 0.00/s
LRU len: 5720, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
```

The following table describes buffer pool metrics reported by the InnoDB Standard Monitor.

Per second averages provided in InnoDB Standard Monitor output are based on the elapsed time since InnoDB Standard Monitor output was last printed.

**Table 17.2 InnoDB Buffer Pool Metrics**

| Name                        | Description                                                                                                                                          |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| Total memory allocated      | The total memory allocated for the buffer pool in<br>bytes.                                                                                          |
| Dictionary memory allocated | The total memory allocated for the InnoDB data<br>dictionary in bytes.                                                                               |
| Buffer pool size            | The total size in pages allocated to the buffer pool.                                                                                                |
| Free buffers                | The total size in pages of the buffer pool free list.                                                                                                |
| Database pages              | The total size in pages of the buffer pool LRU list.                                                                                                 |
| Old database pages          | The total size in pages of the buffer pool old LRU<br>sublist.                                                                                       |
| Modified db pages           | The current number of pages modified in the<br>buffer pool.                                                                                          |
| Pending reads               | The number of buffer pool pages waiting to be<br>read into the buffer pool.                                                                          |
| Pending writes LRU          | The number of old dirty pages within the buffer<br>pool to be written from the bottom of the LRU list.                                               |
| Pending writes flush list   | The number of buffer pool pages to be flushed<br>during checkpointing.                                                                               |
| Pending writes single page  | The number of pending independent page writes<br>within the buffer pool.                                                                             |
| Pages made young            | The total number of pages made young in the<br>buffer pool LRU list (moved to the head of sublist<br>of "new" pages).                                |
| Pages made not young        | The total number of pages not made young in the<br>buffer pool LRU list (pages that have remained in<br>the "old" sublist without being made young). |
| youngs/s                    | The per second average of accesses to old pages<br>in the buffer pool LRU list that have resulted in                                                 |

| Name                         | Description                                                                                                                                                                                   |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                              | making pages young. See the notes that follow<br>this table for more information.                                                                                                             |
| non-youngs/s                 | The per second average of accesses to old pages<br>in the buffer pool LRU list that have resulted in not<br>making pages young. See the notes that follow<br>this table for more information. |
| Pages read                   | The total number of pages read from the buffer<br>pool.                                                                                                                                       |
| Pages created                | The total number of pages created within the<br>buffer pool.                                                                                                                                  |
| Pages written                | The total number of pages written from the buffer<br>pool.                                                                                                                                    |
| reads/s                      | The per second average number of buffer pool<br>page reads per second.                                                                                                                        |
| creates/s                    | The average number of buffer pool pages created<br>per second.                                                                                                                                |
| writes/s                     | The average number of buffer pool page writes<br>per second.                                                                                                                                  |
| Buffer pool hit rate         | The buffer pool page hit rate for pages read from<br>the buffer pool vs from disk storage.                                                                                                    |
| young-making rate            | The average hit rate at which page accesses have<br>resulted in making pages young. See the notes<br>that follow this table for more information.                                             |
| not (young-making rate)      | The average hit rate at which page accesses<br>have not resulted in making pages young. See the<br>notes that follow this table for more information.                                         |
| Pages read ahead             | The per second average of read ahead<br>operations.                                                                                                                                           |
| Pages evicted without access | The per second average of the pages evicted<br>without being accessed from the buffer pool.                                                                                                   |
| Random read ahead            | The per second average of random read ahead<br>operations.                                                                                                                                    |
| LRU len                      | The total size in pages of the buffer pool LRU list.                                                                                                                                          |
| unzip_LRU len                | The length (in pages) of the buffer pool<br>unzip_LRU list.                                                                                                                                   |
| I/O sum                      | The total number of buffer pool LRU list pages<br>accessed.                                                                                                                                   |
| I/O cur                      | The total number of buffer pool LRU list pages<br>accessed in the current interval.                                                                                                           |
| I/O unzip sum                | The total number of buffer pool unzip_LRU list<br>pages decompressed.                                                                                                                         |
| I/O unzip cur                | The total number of buffer pool unzip_LRU list<br>pages decompressed in the current interval.                                                                                                 |

#### **Notes**:

• The youngs/s metric is applicable only to old pages. It is based on the number of page accesses. There can be multiple accesses for a given page, all of which are counted. If you see very low youngs/s values when there are no large scans occurring, consider reducing the delay time or increasing the percentage of the buffer pool used for the old sublist. Increasing the percentage

makes the old sublist larger so that it takes longer for pages in that sublist to move to the tail, which increases the likelihood that those pages are accessed again and made young. See Section 17.8.3.3, "Making the Buffer Pool Scan Resistant".

- The non-youngs/s metric is applicable only to old pages. It is based on the number of page accesses. There can be multiple accesses for a given page, all of which are counted. If you do not see a higher non-youngs/s value when performing large table scans (and a higher youngs/s value), increase the delay value. See Section 17.8.3.3, "Making the Buffer Pool Scan Resistant".
- The young-making rate accounts for all buffer pool page accesses, not just accesses for pages in the old sublist. The young-making rate and not rate do not normally add up to the overall buffer pool hit rate. Page hits in the old sublist cause pages to move to the new sublist, but page hits in the new sublist cause pages to move to the head of the list only if they are a certain distance from the head.
- not (young-making rate) is the average hit rate at which page accesses have not resulted in making pages young due to the delay defined by innodb\_old\_blocks\_time not being met, or due to page hits in the new sublist that did not result in pages being moved to the head. This rate accounts for all buffer pool page accesses, not just accesses for pages in the old sublist.

Buffer pool server status variables and the INNODB\_BUFFER\_POOL\_STATS table provide many of the same buffer pool metrics found in InnoDB Standard Monitor output. For more information, see Example 17.10, "Querying the INNODB\_BUFFER\_POOL\_STATS Table".

# <span id="page-193-0"></span>**17.5.2 Change Buffer**

The change buffer is a special data structure that caches changes to secondary index pages when those pages are not in the buffer pool. The buffered changes, which may result from INSERT, UPDATE, or DELETE operations (DML), are merged later when the pages are loaded into the buffer pool by other read operations.

**Figure 17.3 Change Buffer**

Unlike clustered indexes, secondary indexes are usually nonunique, and inserts into secondary indexes happen in a relatively random order. Similarly, deletes and updates may affect secondary index pages that are not adjacently located in an index tree. Merging cached changes at a later time, when affected pages are read into the buffer pool by other operations, avoids substantial random access I/O that would be required to read secondary index pages into the buffer pool from disk.

Periodically, the purge operation that runs when the system is mostly idle, or during a slow shutdown, writes the updated index pages to disk. The purge operation can write disk blocks for a series of index values more efficiently than if each value were written to disk immediately.

Change buffer merging may take several hours when there are many affected rows and numerous secondary indexes to update. During this time, disk I/O is increased, which can cause a significant slowdown for disk-bound queries. Change buffer merging may also continue to occur after a transaction is committed, and even after a server shutdown and restart (see Section 17.21.3, "Forcing InnoDB Recovery" for more information).

In memory, the change buffer occupies part of the buffer pool. On disk, the change buffer is part of the system tablespace, where index changes are buffered when the database server is shut down.

The type of data cached in the change buffer is governed by the innodb\_change\_buffering variable. For more information, see [Configuring Change Buffering.](#page-194-0) You can also configure the maximum change buffer size. For more information, see [Configuring the Change Buffer Maximum Size](#page-195-0).

Change buffering is not supported for a secondary index if the index contains a descending index column or if the primary key includes a descending index column.

For answers to frequently asked questions about the change buffer, see Section A.16, "MySQL 8.0 FAQ: InnoDB Change Buffer".

## <span id="page-194-0"></span>**Configuring Change Buffering**

When INSERT, UPDATE, and DELETE operations are performed on a table, the values of indexed columns (particularly the values of secondary keys) are often in an unsorted order, requiring substantial I/O to bring secondary indexes up to date. The change buffer caches changes to secondary index entries when the relevant page is not in the buffer pool, thus avoiding expensive I/O operations by not immediately reading in the page from disk. The buffered changes are merged when the page is loaded into the buffer pool, and the updated page is later flushed to disk. The InnoDB main thread merges buffered changes when the server is nearly idle, and during a slow shutdown.

Because it can result in fewer disk reads and writes, change buffering is most valuable for workloads that are I/O-bound; for example, applications with a high volume of DML operations such as bulk inserts benefit from change buffering.

However, the change buffer occupies a part of the buffer pool, reducing the memory available to cache data pages. If the working set almost fits in the buffer pool, or if your tables have relatively few secondary indexes, it may be useful to disable change buffering. If the working data set fits entirely within the buffer pool, change buffering does not impose extra overhead, because it only applies to pages that are not in the buffer pool.

The innodb\_change\_buffering variable controls the extent to which InnoDB performs change buffering. You can enable or disable buffering for inserts, delete operations (when index records are initially marked for deletion) and purge operations (when index records are physically deleted). An update operation is a combination of an insert and a delete. The default innodb\_change\_buffering value is all.

Permitted innodb\_change\_buffering values include:

• **all**

The default value: buffer inserts, delete-marking operations, and purges.

• **none**

Do not buffer any operations.

• **inserts**

Buffer insert operations.

• **deletes**

Buffer delete-marking operations.

• **changes**

Buffer both inserts and delete-marking operations.

• **purges**

Buffer the physical deletion operations that happen in the background.

You can set the innodb\_change\_buffering variable in the MySQL option file (my.cnf or my.ini) or change it dynamically with the [SET GLOBAL](#page-90-0) statement, which requires privileges sufficient to set global system variables. See Section 7.1.9.1, "System Variable Privileges". Changing the setting affects the buffering of new operations; the merging of existing buffered entries is not affected.

## <span id="page-195-0"></span>**Configuring the Change Buffer Maximum Size**

The innodb\_change\_buffer\_max\_size variable permits configuring the maximum size of the change buffer as a percentage of the total size of the buffer pool. By default, innodb\_change\_buffer\_max\_size is set to 25. The maximum setting is 50.

Consider increasing innodb\_change\_buffer\_max\_size on a MySQL server with heavy insert, update, and delete activity, where change buffer merging does not keep pace with new change buffer entries, causing the change buffer to reach its maximum size limit.

Consider decreasing innodb\_change\_buffer\_max\_size on a MySQL server with static data used for reporting, or if the change buffer consumes too much of the memory space shared with the buffer pool, causing pages to age out of the buffer pool sooner than desired.

Test different settings with a representative workload to determine an optimal configuration. The innodb\_change\_buffer\_max\_size variable is dynamic, which permits modifying the setting without restarting the server.

## **Monitoring the Change Buffer**

The following options are available for change buffer monitoring:

• InnoDB Standard Monitor output includes change buffer status information. To view monitor data, issue the SHOW ENGINE INNODB STATUS statement.

```
mysql> SHOW ENGINE INNODB STATUS\G
```

Change buffer status information is located under the INSERT BUFFER AND ADAPTIVE HASH INDEX heading and appears similar to the following:

```
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 0, seg size 2, 0 merges
merged operations:
 insert 0, delete mark 0, delete 0
discarded operations:
 insert 0, delete mark 0, delete 0
Hash table size 4425293, used cells 32, node heap has 1 buffer(s)
13577.57 hash searches/s, 202.47 non-hash searches/s
```

For more information, see Section 17.17.3, "InnoDB Standard Monitor and Lock Monitor Output".

• The Information Schema INNODB\_METRICS table provides most of the data points found in InnoDB Standard Monitor output plus other data points. To view change buffer metrics and a description of each, issue the following query:

mysql> **SELECT NAME, COMMENT FROM INFORMATION\_SCHEMA.INNODB\_METRICS WHERE NAME LIKE '%ibuf%'\G**

See Section 17.15.6, "InnoDB INFORMATION\_SCHEMA Metrics Table".

• The Information Schema INNODB\_BUFFER\_PAGE table provides metadata about each page in the buffer pool, including change buffer index and change buffer bitmap pages. Change buffer pages are identified by PAGE\_TYPE. IBUF\_INDEX is the page type for change buffer index pages, and IBUF\_BITMAP is the page type for change buffer bitmap pages.

![](_page_196_Picture_4.jpeg)

#### **Warning**

Querying the INNODB\_BUFFER\_PAGE table can introduce significant performance overhead. To avoid impacting performance, reproduce the issue you want to investigate on a test instance and run your queries on the test instance.

For example, you can query the INNODB\_BUFFER\_PAGE table to determine the approximate number of IBUF\_INDEX and IBUF\_BITMAP pages as a percentage of total buffer pool pages.

```
mysql> SELECT (SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE PAGE_TYPE LIKE 'IBUF%') AS change_buffer_pages,
 (SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE) AS total_pages,
 (SELECT ((change_buffer_pages/total_pages)*100))
 AS change_buffer_page_percentage;
+---------------------+-------------+-------------------------------+
| change_buffer_pages | total_pages | change_buffer_page_percentage |
+---------------------+-------------+-------------------------------+
| 25 | 8192 | 0.3052 |
+---------------------+-------------+-------------------------------+
```

For information about other data provided by the INNODB\_BUFFER\_PAGE table, see Section 28.4.2, "The INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE Table". For related usage information, see Section 17.15.5, "InnoDB INFORMATION\_SCHEMA Buffer Pool Tables".

• Performance Schema provides change buffer mutex wait instrumentation for advanced performance monitoring. To view change buffer instrumentation, issue the following query:

```
mysql> SELECT * FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%wait/synch/mutex/innodb/ibuf%';
+-------------------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------------------------------------------------+---------+-------+
| wait/synch/mutex/innodb/ibuf_bitmap_mutex | YES | YES |
| wait/synch/mutex/innodb/ibuf_mutex | YES | YES |
| wait/synch/mutex/innodb/ibuf_pessimistic_insert_mutex | YES | YES |
+-------------------------------------------------------+---------+-------+
```

For information about monitoring InnoDB mutex waits, see Section 17.16.2, "Monitoring InnoDB Mutex Waits Using Performance Schema".

# <span id="page-196-0"></span>**17.5.3 Adaptive Hash Index**

The adaptive hash index enables InnoDB to perform more like an in-memory database on systems with appropriate combinations of workload and sufficient memory for the buffer pool without sacrificing transactional features or reliability. The adaptive hash index is enabled by the innodb\_adaptive\_hash\_index variable, or turned off at server startup by --skip-innodbadaptive-hash-index.

Based on the observed pattern of searches, a hash index is built using a prefix of the index key. The prefix can be any length, and it may be that only some values in the B-tree appear in the hash index. Hash indexes are built on demand for the pages of the index that are accessed often.

If a table fits almost entirely in main memory, a hash index speeds up queries by enabling direct lookup of any element, turning the index value into a sort of pointer. InnoDB has a mechanism that monitors

index searches. If InnoDB notices that queries could benefit from building a hash index, it does so automatically.

With some workloads, the speedup from hash index lookups greatly outweighs the extra work to monitor index lookups and maintain the hash index structure. Access to the adaptive hash index can sometimes become a source of contention under heavy workloads, such as multiple concurrent joins. Queries with LIKE operators and % wildcards also tend not to benefit. For workloads that do not benefit from the adaptive hash index, turning it off reduces unnecessary performance overhead. Because it is difficult to predict in advance whether the adaptive hash index is appropriate for a particular system and workload, consider running benchmarks with it enabled and disabled.

The adaptive hash index feature is partitioned. Each index is bound to a specific partition, and each partition is protected by a separate latch. Partitioning is controlled by the innodb\_adaptive\_hash\_index\_parts variable. The innodb\_adaptive\_hash\_index\_parts variable is set to 8 by default. The maximum setting is 512.

You can monitor adaptive hash index use and contention in the SEMAPHORES section of [SHOW ENGINE](#page-107-0) [INNODB STATUS](#page-107-0) output. If there are numerous threads waiting on rw-latches created in btr0sea.c, consider increasing the number of adaptive hash index partitions or disabling the adaptive hash index.

For information about the performance characteristics of hash indexes, see Section 10.3.9, "Comparison of B-Tree and Hash Indexes".

## <span id="page-197-0"></span>**17.5.4 Log Buffer**

The log buffer is the memory area that holds data to be written to the log files on disk. Log buffer size is defined by the innodb\_log\_buffer\_size variable. The default size is 16MB. The contents of the log buffer are periodically flushed to disk. A large log buffer enables large transactions to run without the need to write redo log data to disk before the transactions commit. Thus, if you have transactions that update, insert, or delete many rows, increasing the size of the log buffer saves disk I/O.

The innodb\_flush\_log\_at\_trx\_commit variable controls how the contents of the log buffer are written and flushed to disk. The innodb\_flush\_log\_at\_timeout variable controls log flushing frequency.

For related information, see Memory Configuration, and Section 10.5.4, "Optimizing InnoDB Redo Logging".

# <span id="page-197-1"></span>**17.6 InnoDB On-Disk Structures**

This section describes InnoDB on-disk structures and related topics.

## <span id="page-197-2"></span>**17.6.1 Tables**

This section covers topics related to InnoDB tables.