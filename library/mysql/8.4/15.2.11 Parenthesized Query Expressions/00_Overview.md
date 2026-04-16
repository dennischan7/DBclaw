---
source: MySQL 8.4 Reference
title: 00_Overview
---

```
parenthesized_query_expression:
 ( query_expression [order_by_clause] [limit_clause] )
 [order_by_clause]
 [limit_clause]
 [into_clause]
query_expression:
 query_block [set_op query_block [set_op query_block ...]]
 [order_by_clause]
 [limit_clause]
 [into_clause]
query_block:
 SELECT ... | TABLE | VALUES
order_by_clause:
 ORDER BY as for SELECT
limit_clause:
 LIMIT as for SELECT
into_clause:
 INTO as for SELECT
set_op:
 UNION | INTERSECT | EXCEPT
```

MySQL 8.4 supports parenthesized query expressions according to the preceding syntax. At its simplest, a parenthesized query expression contains a single [SELECT](#page-70-0) or other statement returning a result set and no following optional clauses:

```
(SELECT 1);
(SELECT * FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'mysql');
```

```
TABLE t;
VALUES ROW(2, 3, 4), ROW(1, -2, 3);
```

A parenthesized query expression can also contain queries linked by one or more set operations such as [UNION](#page-111-0), and end with any or all of the optional clauses:

```
mysql> (SELECT 1 AS result UNION SELECT 2);
+--------+
| result |
+--------+
| 1 |
| 2 |
+--------+
mysql> (SELECT 1 AS result UNION SELECT 2) LIMIT 1;
+--------+
| result |
+--------+
| 1 |
+--------+
mysql> (SELECT 1 AS result UNION SELECT 2) LIMIT 1 OFFSET 1;
+--------+
| result |
+--------+
| 2 |
+--------+
mysql> (SELECT 1 AS result UNION SELECT 2)
 ORDER BY result DESC LIMIT 1;
+--------+
| result |
+--------+
| 2 |
+--------+
mysql> (SELECT 1 AS result UNION SELECT 2)
 ORDER BY result DESC LIMIT 1 OFFSET 1;
+--------+
| result |
+--------+
| 1 |
+--------+
mysql> (SELECT 1 AS result UNION SELECT 3 UNION SELECT 2)
 ORDER BY result LIMIT 1 OFFSET 1 INTO @var;
mysql> SELECT @var;
+------+
| @var |
+------+
| 2 |
+------+
```

INTERSECT acts before UNION and EXCEPT, so that the following two statements are equivalent:

```
SELECT a FROM t1 EXCEPT SELECT b FROM t2 INTERSECT SELECT c FROM t3;
SELECT a FROM t1 EXCEPT (SELECT b FROM t2 INTERSECT SELECT c FROM t3);
```

Parenthesized query expressions are also used as query expressions, so a query expression, usually composed of query blocks, may also consist of parenthesized query expressions:

```
(TABLE t1 ORDER BY a) UNION (TABLE t2 ORDER BY b) ORDER BY z;
```

Query blocks may have trailing ORDER BY and LIMIT clauses, which are applied before the outer set operation, ORDER BY, and LIMIT.

You cannot have a query block with a trailing ORDER BY or LIMIT without wrapping it in parentheses but parentheses may be used for enforcement in various ways:

• To enforce LIMIT on each query block:

```
(SELECT 1 LIMIT 1) UNION (VALUES ROW(2) LIMIT 1);
```

```
(VALUES ROW(1), ROW(2) LIMIT 2) EXCEPT (SELECT 2 LIMIT 1);
```

• To enforce LIMIT on both query blocks and the entire query expression:

```
(SELECT 1 LIMIT 1) UNION (SELECT 2 LIMIT 1) LIMIT 1;
```

• To enforce LIMIT on the entire query expression (with no parentheses):

```
VALUES ROW(1), ROW(2) INTERSECT VALUES ROW(2), ROW(1) LIMIT 1;
```

• Hybrid enforcement: LIMIT on the first query block and on the entire query expression:

```
(SELECT 1 LIMIT 1) UNION SELECT 2 LIMIT 1;
```

The syntax described in this section is subject to certain restrictions:

- A trailing INTO clause for a query expression is not permitted if there is another INTO clause inside parentheses.
- An ORDER BY or LIMIT within a parenthesized query expression which is also applied in the outer query is handled in accordance with the SQL standard.

Nested parenthesized query expressions are permitted. The maximum level of nesting supported is 63; this is after any simplifications or merges have been performed by the parser.

An example of such a statement is shown here:

```
mysql> (SELECT 'a' UNION SELECT 'b' LIMIT 2) LIMIT 3;
+---+
| a |
+---+
| a |
| b |
+---+
2 rows in set (0.00 sec)
```

You should be aware that, when collapsing parenthesized expression bodies, MySQL follows SQL standard semantics, so that a higher outer limit cannot override an inner lower one. For example, (SELECT ... LIMIT 5) LIMIT 10 can return no more than five rows.

# <span id="page-67-0"></span>**15.2.12 REPLACE Statement**

```
REPLACE [LOW_PRIORITY | DELAYED]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 { {VALUES | VALUE} (value_list) [, (value_list)] ...
 |
 VALUES row_constructor_list
 }
REPLACE [LOW_PRIORITY | DELAYED]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 SET assignment_list
REPLACE [LOW_PRIORITY | DELAYED]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 {SELECT ... | TABLE table_name}
value:
 {expr | DEFAULT}
value_list:
 value [, value] ...
```

```
row_constructor_list:
 ROW(value_list)[, ROW(value_list)][, ...]
assignment:
 col_name = value
assignment_list:
 assignment [, assignment] ...
```

[REPLACE](#page-67-0) works exactly like [INSERT](#page-36-0), except that if an old row in the table has the same value as a new row for a PRIMARY KEY or a UNIQUE index, the old row is deleted before the new row is inserted. See [Section 15.2.7, "INSERT Statement"](#page-36-0).

[REPLACE](#page-67-0) is a MySQL extension to the SQL standard. It either inserts, or deletes and inserts. For another MySQL extension to standard SQL—that either inserts or updates—see [Section 15.2.7.2,](#page-42-0) ["INSERT ... ON DUPLICATE KEY UPDATE Statement".](#page-42-0)

DELAYED inserts and replaces were deprecated in MySQL 5.6. In MySQL 8.4, DELAYED is not supported. The server recognizes but ignores the DELAYED keyword, handles the replace as a nondelayed replace, and generates an [ER\\_WARN\\_LEGACY\\_SYNTAX\\_CONVERTED](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_warn_legacy_syntax_converted) warning: REPLACE DELAYED is no longer supported. The statement was converted to REPLACE. The DELAYED keyword is scheduled for removal in a future release. release.

![](_page_68_Picture_5.jpeg)

#### **Note**

[REPLACE](#page-67-0) makes sense only if a table has a PRIMARY KEY or UNIQUE index. Otherwise, it becomes equivalent to [INSERT](#page-36-0), because there is no index to be used to determine whether a new row duplicates another.

Values for all columns are taken from the values specified in the [REPLACE](#page-67-0) statement. Any missing columns are set to their default values, just as happens for [INSERT](#page-36-0). You cannot refer to values from the current row and use them in the new row. If you use an assignment such as SET col\_name = col\_name + 1, the reference to the column name on the right hand side is treated as DEFAULT(col\_name), so the assignment is equivalent to SET col\_name = DEFAULT(col\_name) + 1.

You can specify the column values that REPLACE attempts to insert using [VALUES ROW\(\)](#page-112-0).

To use [REPLACE](#page-67-0), you must have both the INSERT and DELETE privileges for the table.

If a generated column is replaced explicitly, the only permitted value is DEFAULT. For information about generated columns, see Section 15.1.20.8, "CREATE TABLE and Generated Columns".

REPLACE supports explicit partition selection using the PARTITION clause with a list of commaseparated names of partitions, subpartitions, or both. As with [INSERT](#page-36-0), if it is not possible to insert the new row into any of these partitions or subpartitions, the REPLACE statement fails with the error Found a row not matching the given partition set. For more information and examples, see Section 26.5, "Partition Selection".

The [REPLACE](#page-67-0) statement returns a count to indicate the number of rows affected. This is the sum of the rows deleted and inserted. If the count is 1 for a single-row [REPLACE](#page-67-0), a row was inserted and no rows were deleted. If the count is greater than 1, one or more old rows were deleted before the new row was inserted. It is possible for a single row to replace more than one old row if the table contains multiple unique indexes and the new row duplicates values for different old rows in different unique indexes.

The affected-rows count makes it easy to determine whether [REPLACE](#page-67-0) only added a row or whether it also replaced any rows: Check whether the count is 1 (added) or greater (replaced).

If you are using the C API, the affected-rows count can be obtained using the [mysql\\_affected\\_rows\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-affected-rows.md) function.

You cannot replace into a table and select from the same table in a subquery.

MySQL uses the following algorithm for [REPLACE](#page-67-0) (and [LOAD DATA ... REPLACE](#page-47-0)):

- 1. Try to insert the new row into the table
- 2. While the insertion fails because a duplicate-key error occurs for a primary key or unique index:
  - a. Delete from the table the conflicting row that has the duplicate key value
  - b. Try again to insert the new row into the table

It is possible that in the case of a duplicate-key error, a storage engine may perform the REPLACE as an update rather than a delete plus insert, but the semantics are the same. There are no user-visible effects other than a possible difference in how the storage engine increments Handler\_xxx status variables.

Because the results of REPLACE ... SELECT statements depend on the ordering of rows from the [SELECT](#page-70-0) and this order cannot always be guaranteed, it is possible when logging these statements for the source and the replica to diverge. For this reason, REPLACE ... SELECT statements are flagged as unsafe for statement-based replication. such statements produce a warning in the error log when using statement-based mode and are written to the binary log using the row-based format when using MIXED mode. See also Section 19.2.1.1, "Advantages and Disadvantages of Statement-Based and Row-Based Replication".

MySQL 8.4 supports [TABLE](#page-105-0) as well as [SELECT](#page-70-0) with REPLACE, just as it does with [INSERT](#page-36-0). See [Section 15.2.7.1, "INSERT ... SELECT Statement"](#page-41-0), for more information and examples.

When modifying an existing table that is not partitioned to accommodate partitioning, or, when modifying the partitioning of an already partitioned table, you may consider altering the table's primary key (see Section 26.6.1, "Partitioning Keys, Primary Keys, and Unique Keys"). You should be aware that, if you do this, the results of REPLACE statements may be affected, just as they would be if you modified the primary key of a nonpartitioned table. Consider the table created by the following CREATE TABLE statement:

```
CREATE TABLE test (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 data VARCHAR(64) DEFAULT NULL,
 ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
);
```

When we create this table and run the statements shown in the mysql client, the result is as follows:

```
mysql> REPLACE INTO test VALUES (1, 'Old', '2014-08-20 18:47:00');
Query OK, 1 row affected (0.04 sec)
mysql> REPLACE INTO test VALUES (1, 'New', '2014-08-20 18:47:42');
Query OK, 2 rows affected (0.04 sec)
mysql> SELECT * FROM test;
+----+------+---------------------+
| id | data | ts |
+----+------+---------------------+
| 1 | New | 2014-08-20 18:47:42 |
+----+------+---------------------+
1 row in set (0.00 sec)
```

Now we create a second table almost identical to the first, except that the primary key now covers 2 columns, as shown here (emphasized text):

```
CREATE TABLE test2 (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 data VARCHAR(64) DEFAULT NULL,
```

```
 ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (id, ts)
);
```

When we run on test2 the same two REPLACE statements as we did on the original test table, we obtain a different result:

```
mysql> REPLACE INTO test2 VALUES (1, 'Old', '2014-08-20 18:47:00');
Query OK, 1 row affected (0.05 sec)
mysql> REPLACE INTO test2 VALUES (1, 'New', '2014-08-20 18:47:42');
Query OK, 1 row affected (0.06 sec)
mysql> SELECT * FROM test2;
+----+------+---------------------+
| id | data | ts |
+----+------+---------------------+
| 1 | Old | 2014-08-20 18:47:00 |
| 1 | New | 2014-08-20 18:47:42 |
+----+------+---------------------+
2 rows in set (0.00 sec)
```

This is due to the fact that, when run on test2, both the id and ts column values must match those of an existing row for the row to be replaced; otherwise, a row is inserted.

# <span id="page-70-0"></span>**15.2.13 SELECT Statement**

```
SELECT
 [ALL | DISTINCT | DISTINCTROW ]
 [HIGH_PRIORITY]
 [STRAIGHT_JOIN]
 [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
 [SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
 select_expr [, select_expr] ...
 [into_option]
 [FROM table_references
 [PARTITION partition_list]]
 [WHERE where_condition]
 [GROUP BY [ {col_name | expr | position}, ... [WITH ROLLUP]
 | ROLLUP ({col_name | expr | position}, ...)] ]
 [HAVING where_condition]
 [WINDOW window_name AS (window_spec)
 [, window_name AS (window_spec)] ...]
 [ORDER BY {col_name | expr | position}
 [ASC | DESC], ... [WITH ROLLUP]]
 [LIMIT {[offset,] row_count | row_count OFFSET offset}]
 [into_option]
 [FOR {UPDATE | SHARE}
 [OF tbl_name [, tbl_name] ...]
 [NOWAIT | SKIP LOCKED]
 | LOCK IN SHARE MODE]
 [into_option]
into_option: {
 INTO OUTFILE 'file_name'
 [CHARACTER SET charset_name]
 export_options
 | INTO DUMPFILE 'file_name'
 | INTO var_name [, var_name] ...
}
export_options:
 [{FIELDS | COLUMNS}
 [TERMINATED BY 'string']
 [[OPTIONALLY] ENCLOSED BY 'char']
 [ESCAPED BY 'char']
 ]
 [LINES
 [STARTING BY 'string']
 [TERMINATED BY 'string']
 ]
```

[SELECT](#page-70-0) is used to retrieve rows selected from one or more tables, and can include [UNION](#page-111-0) operations and subqueries. [INTERSECT](#page-46-0) and [EXCEPT](#page-31-1) operations are also supported. The UNION, INTERSECT, and EXCEPT operators are described in more detail later in this section. See also [Section 15.2.15,](#page-90-0) ["Subqueries"](#page-90-0).

A [SELECT](#page-70-0) statement can start with a [WITH](#page-114-0) clause to define common table expressions accessible within the [SELECT](#page-70-0). See [Section 15.2.20, "WITH \(Common Table Expressions\)"](#page-114-0).

The most commonly used clauses of [SELECT](#page-70-0) statements are these:

- Each select\_expr indicates a column that you want to retrieve. There must be at least one select\_expr.
- table\_references indicates the table or tables from which to retrieve rows. Its syntax is described in [Section 15.2.13.2, "JOIN Clause"](#page-79-0).
- SELECT supports explicit partition selection using the PARTITION clause with a list of partitions or subpartitions (or both) following the name of the table in a table\_reference (see [Section 15.2.13.2, "JOIN Clause"\)](#page-79-0). In this case, rows are selected only from the partitions listed, and any other partitions of the table are ignored. For more information and examples, see Section 26.5, "Partition Selection".
- The WHERE clause, if given, indicates the condition or conditions that rows must satisfy to be selected. where\_condition is an expression that evaluates to true for each row to be selected. The statement selects all rows if there is no WHERE clause.

In the WHERE expression, you can use any of the functions and operators that MySQL supports, except for aggregate (group) functions. See Section 11.5, "Expressions", and Chapter 14, Functions and Operators.

[SELECT](#page-70-0) can also be used to retrieve rows computed without reference to any table.

For example:

```
mysql> SELECT 1 + 1;
 -> 2
```

 You are permitted to specify DUAL as a dummy table name in situations where no tables are referenced:

```
mysql> SELECT 1 + 1 FROM DUAL;
 -> 2
```

DUAL is purely for the convenience of people who require that all [SELECT](#page-70-0) statements should have FROM and possibly other clauses. MySQL may ignore the clauses. MySQL does not require FROM DUAL if no tables are referenced.

In general, clauses used must be given in exactly the order shown in the syntax description. For example, a HAVING clause must come after any GROUP BY clause and before any ORDER BY clause. The INTO clause, if present, can appear in any position indicated by the syntax description, but within a given statement can appear only once, not in multiple positions. For more information about INTO, see [Section 15.2.13.1, "SELECT ... INTO Statement"](#page-76-0).

The list of select\_expr terms comprises the select list that indicates which columns to retrieve. Terms specify a column or expression or can use \*-shorthand:

• A select list consisting only of a single unqualified \* can be used as shorthand to select all columns from all tables:

```
SELECT * FROM t1 INNER JOIN t2 ...
```

• tbl\_name.\* can be used as a qualified shorthand to select all columns from the named table:

```
SELECT t1.*, t2.* FROM t1 INNER JOIN t2 ...
```

- If a table has invisible columns, \* and tbl\_name.\* do not include them. To be included, invisible columns must be referenced explicitly.
- Use of an unqualified \* with other items in the select list may produce a parse error. For example:

```
SELECT id, * FROM t1
```

To avoid this problem, use a qualified tbl\_name.\* reference:

```
SELECT id, t1.* FROM t1
```

Use qualified tbl\_name.\* references for each table in the select list:

```
SELECT AVG(score), t1.* FROM t1 ...
```

The following list provides additional information about other SELECT clauses:

• A select\_expr can be given an alias using AS alias\_name. The alias is used as the expression's column name and can be used in GROUP BY, ORDER BY, or HAVING clauses. For example:

```
SELECT CONCAT(last_name,', ',first_name) AS full_name
 FROM mytable ORDER BY full_name;
```

The AS keyword is optional when aliasing a select\_expr with an identifier. The preceding example could have been written like this:

```
SELECT CONCAT(last_name,', ',first_name) full_name
 FROM mytable ORDER BY full_name;
```

However, because the AS is optional, a subtle problem can occur if you forget the comma between two select\_expr expressions: MySQL interprets the second as an alias name. For example, in the following statement, columnb is treated as an alias name:

```
SELECT columna columnb FROM mytable;
```

For this reason, it is good practice to be in the habit of using AS explicitly when specifying column aliases.

It is not permissible to refer to a column alias in a WHERE clause, because the column value might not yet be determined when the WHERE clause is executed. See Section B.3.4.4, "Problems with Column Aliases".

• The FROM table\_references clause indicates the table or tables from which to retrieve rows. If you name more than one table, you are performing a join. For information on join syntax, see [Section 15.2.13.2, "JOIN Clause".](#page-79-0) For each table specified, you can optionally specify an alias.

```
tbl_name [[AS] alias] [index_hint]
```

The use of index hints provides the optimizer with information about how to choose indexes during query processing. For a description of the syntax for specifying these hints, see Section 10.9.4, "Index Hints".

You can use SET max\_seeks\_for\_key=value as an alternative way to force MySQL to prefer key scans instead of table scans. See Section 7.1.8, "Server System Variables".

• You can refer to a table within the default database as tbl\_name, or as db\_name.tbl\_name to specify a database explicitly. You can refer to a column as col\_name, tbl\_name.col\_name, or db\_name.tbl\_name.col\_name. You need not specify a tbl\_name or db\_name.tbl\_name prefix for a column reference unless the reference would be ambiguous. See Section 11.2.2, "Identifier Qualifiers", for examples of ambiguity that require the more explicit column reference forms.

• A table reference can be aliased using tbl\_name AS alias\_name or tbl\_name alias\_name. These statements are equivalent:

```
SELECT t1.name, t2.salary FROM employee AS t1, info AS t2
 WHERE t1.name = t2.name;
SELECT t1.name, t2.salary FROM employee t1, info t2
 WHERE t1.name = t2.name;
```

• Columns selected for output can be referred to in ORDER BY and GROUP BY clauses using column names, column aliases, or column positions. Column positions are integers and begin with 1:

```
SELECT college, region, seed FROM tournament
 ORDER BY region, seed;
SELECT college, region AS r, seed AS s FROM tournament
 ORDER BY r, s;
SELECT college, region, seed FROM tournament
 ORDER BY 2, 3;
```

To sort in reverse order, add the DESC (descending) keyword to the name of the column in the ORDER BY clause that you are sorting by. The default is ascending order; this can be specified explicitly using the ASC keyword.

If ORDER BY occurs within a parenthesized query expression and also is applied in the outer query, the results are undefined and may change in a future version of MySQL.

Use of column positions is deprecated because the syntax has been removed from the SQL standard.

- When you use ORDER BY or GROUP BY to sort a column in a [SELECT](#page-70-0), the server sorts values using only the initial number of bytes indicated by the max\_sort\_length system variable.
- MySQL extends the use of GROUP BY to permit selecting fields that are not mentioned in the GROUP BY clause. If you are not getting the results that you expect from your query, please read the description of GROUP BY found in Section 14.19, "Aggregate Functions".
- The HAVING clause, like the WHERE clause, specifies selection conditions. The WHERE clause specifies conditions on columns in the select list, but cannot refer to aggregate functions. The HAVING clause specifies conditions on groups, typically formed by the GROUP BY clause. The query result includes only groups satisfying the HAVING conditions. (If no GROUP BY is present, all rows implicitly form a single aggregate group.)

The HAVING clause is applied nearly last, just before items are sent to the client, with no optimization. (LIMIT is applied after HAVING.)

The SQL standard requires that HAVING must reference only columns in the GROUP BY clause or columns used in aggregate functions. However, MySQL supports an extension to this behavior, and permits HAVING to refer to columns in the [SELECT](#page-70-0) list and columns in outer subqueries as well.

If the HAVING clause refers to a column that is ambiguous, a warning occurs. In the following statement, col2 is ambiguous because it is used as both an alias and a column name:

```
SELECT COUNT(col1) AS col2 FROM t GROUP BY col2 HAVING col2 = 2;
```

Preference is given to standard SQL behavior, so if a HAVING column name is used both in GROUP BY and as an aliased column in the select column list, preference is given to the column in the GROUP BY column.

• Do not use HAVING for items that should be in the WHERE clause. For example, do not write the following:

```
SELECT col_name FROM tbl_name HAVING col_name > 0;
```

Write this instead:

```
SELECT col_name FROM tbl_name WHERE col_name > 0;
```

• The HAVING clause can refer to aggregate functions, which the WHERE clause cannot:

```
SELECT user, MAX(salary) FROM users
 GROUP BY user HAVING MAX(salary) > 10;
```

(This did not work in some older versions of MySQL.)

• MySQL permits duplicate column names. That is, there can be more than one select\_expr with the same name. This is an extension to standard SQL. Because MySQL also permits GROUP BY and HAVING to refer to select\_expr values, this can result in an ambiguity:

```
SELECT 12 AS a, a FROM t GROUP BY a;
```

In that statement, both columns have the name a. To ensure that the correct column is used for grouping, use different names for each select\_expr.

- The WINDOW clause, if present, defines named windows that can be referred to by window functions. For details, see Section 14.20.4, "Named Windows".
- MySQL resolves unqualified column or alias references in ORDER BY clauses by searching in the select\_expr values, then in the columns of the tables in the FROM clause. For GROUP BY or HAVING clauses, it searches the FROM clause before searching in the select\_expr values. (For GROUP BY and HAVING, this differs from the pre-MySQL 5.0 behavior that used the same rules as for ORDER BY.)
- The LIMIT clause can be used to constrain the number of rows returned by the [SELECT](#page-70-0) statement. LIMIT takes one or two numeric arguments, which must both be nonnegative integer constants, with these exceptions:
  - Within prepared statements, LIMIT parameters can be specified using ? placeholder markers.
  - Within stored programs, LIMIT parameters can be specified using integer-valued routine parameters or local variables.

With two arguments, the first argument specifies the offset of the first row to return, and the second specifies the maximum number of rows to return. The offset of the initial row is 0 (not 1):

```
SELECT * FROM tbl LIMIT 5,10; # Retrieve rows 6-15
```

To retrieve all rows from a certain offset up to the end of the result set, you can use some large number for the second parameter. This statement retrieves all rows from the 96th row to the last:

```
SELECT * FROM tbl LIMIT 95,18446744073709551615;
```

With one argument, the value specifies the number of rows to return from the beginning of the result set:

```
SELECT * FROM tbl LIMIT 5; # Retrieve first 5 rows
```

In other words, LIMIT row\_count is equivalent to LIMIT 0, row\_count.

For prepared statements, you can use placeholders. The following statements return one row from the tbl table:

```
SET @a=1;
PREPARE STMT FROM 'SELECT * FROM tbl LIMIT ?';
EXECUTE STMT USING @a;
```

The following statements return the second to sixth rows from the tbl table:

```
SET @skip=1; SET @numrows=5;
PREPARE STMT FROM 'SELECT * FROM tbl LIMIT ?, ?';
EXECUTE STMT USING @skip, @numrows;
```

For compatibility with PostgreSQL, MySQL also supports the LIMIT row\_count OFFSET offset syntax.

If LIMIT occurs within a parenthesized query expression and also is applied in the outer query, the results are undefined and may change in a future version of MySQL.

- The [SELECT ... INTO](#page-76-0) form of [SELECT](#page-70-0) enables the query result to be written to a file or stored in variables. For more information, see [Section 15.2.13.1, "SELECT ... INTO Statement".](#page-76-0)
- If you use FOR UPDATE with a storage engine that uses page or row locks, rows examined by the query are write-locked until the end of the current transaction.

You cannot use FOR UPDATE as part of the [SELECT](#page-70-0) in a statement such as CREATE TABLE new\_table SELECT ... FROM old\_table .... (If you attempt to do so, the statement is rejected with the error Can't update table 'old\_table' while 'new\_table' is being created.)

FOR SHARE and LOCK IN SHARE MODE set shared locks that permit other transactions to read the examined rows but not to update or delete them. FOR SHARE and LOCK IN SHARE MODE are equivalent. However, FOR SHARE, like FOR UPDATE, supports NOWAIT, SKIP LOCKED, and OF tbl\_name options. FOR SHARE is a replacement for LOCK IN SHARE MODE, but LOCK IN SHARE MODE remains available for backward compatibility.

NOWAIT causes a FOR UPDATE or FOR SHARE query to execute immediately, returning an error if a row lock cannot be obtained due to a lock held by another transaction.

SKIP LOCKED causes a FOR UPDATE or FOR SHARE query to execute immediately, excluding rows from the result set that are locked by another transaction.

NOWAIT and SKIP LOCKED options are unsafe for statement-based replication.

![](_page_75_Picture_11.jpeg)

#### **Note**

Queries that skip locked rows return an inconsistent view of the data. SKIP LOCKED is therefore not suitable for general transactional work. However, it may be used to avoid lock contention when multiple sessions access the same queue-like table.

OF tbl\_name applies FOR UPDATE and FOR SHARE queries to named tables. For example:

```
SELECT * FROM t1, t2 FOR SHARE OF t1 FOR UPDATE OF t2;
```

All tables referenced by the query block are locked when OF tbl\_name is omitted. Consequently, using a locking clause without OF tbl\_name in combination with another locking clause returns an error. Specifying the same table in multiple locking clauses returns an error. If an alias is specified as the table name in the SELECT statement, a locking clause may only use the alias. If the SELECT statement does not specify an alias explicitly, the locking clause may only specify the actual table name.

For more information about FOR UPDATE and FOR SHARE, see Section 17.7.2.4, "Locking Reads". For additional information about NOWAIT and SKIP LOCKED options, see Locking Read Concurrency with NOWAIT and SKIP LOCKED.

Following the [SELECT](#page-70-0) keyword, you can use a number of modifiers that affect the operation of the statement. HIGH\_PRIORITY, STRAIGHT\_JOIN, and modifiers beginning with SQL\_ are MySQL extensions to standard SQL.

• The ALL and DISTINCT modifiers specify whether duplicate rows should be returned. ALL (the default) specifies that all matching rows should be returned, including duplicates. DISTINCT specifies removal of duplicate rows from the result set. It is an error to specify both modifiers. DISTINCTROW is a synonym for DISTINCT.

DISTINCT can be used with a query that also uses WITH ROLLUP.

• HIGH\_PRIORITY gives the [SELECT](#page-70-0) higher priority than a statement that updates a table. You should use this only for queries that are very fast and must be done at once. A SELECT HIGH\_PRIORITY query that is issued while the table is locked for reading runs even if there is an update statement waiting for the table to be free. This affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE).

HIGH\_PRIORITY cannot be used with [SELECT](#page-70-0) statements that are part of a [UNION](#page-111-0).

• STRAIGHT\_JOIN forces the optimizer to join the tables in the order in which they are listed in the FROM clause. You can use this to speed up a query if the optimizer joins the tables in nonoptimal order. STRAIGHT\_JOIN also can be used in the table\_references list. See [Section 15.2.13.2,](#page-79-0) ["JOIN Clause"](#page-79-0).

STRAIGHT\_JOIN does not apply to any table that the optimizer treats as a const or system table. Such a table produces a single row, is read during the optimization phase of query execution, and references to its columns are replaced with the appropriate column values before query execution proceeds. These tables appear first in the query plan displayed by EXPLAIN. See Section 10.8.1, "Optimizing Queries with EXPLAIN". This exception may not apply to const or system tables that are used on the NULL-complemented side of an outer join (that is, the right-side table of a LEFT JOIN or the left-side table of a RIGHT JOIN.

- SQL\_BIG\_RESULT or SQL\_SMALL\_RESULT can be used with GROUP BY or DISTINCT to tell the optimizer that the result set has many rows or is small, respectively. For SQL\_BIG\_RESULT, MySQL directly uses disk-based temporary tables if they are created, and prefers sorting to using a temporary table with a key on the GROUP BY elements. For SQL\_SMALL\_RESULT, MySQL uses in-memory temporary tables to store the resulting table instead of using sorting. This should not normally be needed.
- SQL\_BUFFER\_RESULT forces the result to be put into a temporary table. This helps MySQL free the table locks early and helps in cases where it takes a long time to send the result set to the client. This modifier can be used only for top-level [SELECT](#page-70-0) statements, not for subqueries or following [UNION](#page-111-0).
- SQL\_CALC\_FOUND\_ROWS tells MySQL to calculate how many rows there would be in the result set, disregarding any LIMIT clause. The number of rows can then be retrieved with SELECT FOUND\_ROWS(). See Section 14.15, "Information Functions".

![](_page_76_Picture_10.jpeg)

## **Note**

The SQL\_CALC\_FOUND\_ROWS query modifier and accompanying FOUND\_ROWS() function are deprecated; expect them to be removed in a future version of MySQL. See the description of FOUND\_ROWS() for information about an alternative strategy.

• The SQL\_CACHE and SQL\_NO\_CACHE modifiers were used with the query cache prior to MySQL 8.4. The query cache was removed in MySQL 8.4. The SQL\_CACHE modifier was removed as well. SQL\_NO\_CACHE is deprecated, and has no effect; expect it to be removed in a future MySQL release.

# <span id="page-76-0"></span>**15.2.13.1 SELECT ... INTO Statement**

The [SELECT ... INTO](#page-76-0) form of [SELECT](#page-70-0) enables a query result to be stored in variables or written to a file:

- SELECT ... INTO var\_list selects column values and stores them into variables.
- SELECT ... INTO OUTFILE writes the selected rows to a file. Column and line terminators can be specified to produce a specific output format.
- SELECT ... INTO DUMPFILE writes a single row to a file without any formatting.

A given [SELECT](#page-70-0) statement can contain at most one INTO clause, although as shown by the [SELECT](#page-70-0) syntax description (see [Section 15.2.13, "SELECT Statement"](#page-70-0)), the INTO can appear in different positions:

• Before FROM. Example:

```
SELECT * INTO @myvar FROM t1;
```

• Before a trailing locking clause. Example:

```
SELECT * FROM t1 INTO @myvar FOR UPDATE;
```

• At the end of the [SELECT](#page-70-0). Example:

```
SELECT * FROM t1 FOR UPDATE INTO @myvar;
```

The INTO position at the end of the statement is the preferred position. The position before a locking clause is deprecated; expect support for it to be removed in a future version of MySQL. In other words, INTO after FROM but not at the end of the [SELECT](#page-70-0) produces a warning.

An INTO clause should not be used in a nested [SELECT](#page-70-0) because such a [SELECT](#page-70-0) must return its result to the outer context. There are also constraints on the use of INTO within [UNION](#page-111-0) statements; see [Section 15.2.18, "UNION Clause".](#page-111-0)

For the INTO var\_list variant:

- var\_list names a list of one or more variables, each of which can be a user-defined variable, stored procedure or function parameter, or stored program local variable. (Within a prepared SELECT ... INTO var\_list statement, only user-defined variables are permitted; see [Section 15.6.4.2, "Local Variable Scope and Resolution"](#page-179-0).)
- The selected values are assigned to the variables. The number of variables must match the number of columns. The query should return a single row. If the query returns no rows, a warning with error code 1329 occurs (No data), and the variable values remain unchanged. If the query returns multiple rows, error 1172 occurs (Result consisted of more than one row). If it is possible that the statement may retrieve multiple rows, you can use LIMIT 1 to limit the result set to a single row.

```
SELECT id, data INTO @x, @y FROM test.t1 LIMIT 1;
```

INTO var\_list can also be used with a [TABLE](#page-105-0) statement, subject to these restrictions:

- The number of variables must match the number of columns in the table.
- If the table contains more than one row, you must use LIMIT 1 to limit the result set to a single row. LIMIT 1 must precede the INTO keyword.

An example of such a statement is shown here:

```
TABLE employees ORDER BY lname DESC LIMIT 1
 INTO @id, @fname, @lname, @hired, @separated, @job_code, @store_id;
```

You can also select values from a [VALUES](#page-112-0) statement that generates a single row into a set of user variables. In this case, you must employ a table alias, and you must assign each value from the value list to a variable. Each of the two statements shown here is equivalent to SET @x=2, @y=4, @z=8:

```
SELECT * FROM (VALUES ROW(2,4,8)) AS t INTO @x,@y,@z;
```

```
SELECT * FROM (VALUES ROW(2,4,8)) AS t(a,b,c) INTO @x,@y,@z;
```

User variable names are not case-sensitive. See Section 11.4, "User-Defined Variables".

The [SELECT ... INTO OUTFILE '](#page-76-0)file\_name' form of [SELECT](#page-70-0) writes the selected rows to a file. The file is created on the server host, so you must have the FILE privilege to use this syntax. file\_name cannot be an existing file, which among other things prevents files such as /etc/passwd and database tables from being modified. The character\_set\_filesystem system variable controls the interpretation of the file name.

The [SELECT ... INTO OUTFILE](#page-76-0) statement is intended to enable dumping a table to a text file on the server host. To create the resulting file on some other host, [SELECT ... INTO OUTFILE](#page-76-0) normally is unsuitable because there is no way to write a path to the file relative to the server host file system, unless the location of the file on the remote host can be accessed using a network-mapped path on the server host file system.

Alternatively, if the MySQL client software is installed on the remote host, you can use a client command such as mysql -e "SELECT ..." > file\_name to generate the file on that host.

[SELECT ... INTO OUTFILE](#page-76-0) is the complement of [LOAD DATA](#page-47-0). Column values are written converted to the character set specified in the CHARACTER SET clause. If no such clause is present, values are dumped using the binary character set. In effect, there is no character set conversion. If a result set contains columns in several character sets, so is the output data file, and it may not be possible to reload the file correctly.

The syntax for the export\_options part of the statement consists of the same FIELDS and LINES clauses that are used with the [LOAD DATA](#page-47-0) statement. For more detailed information about the FIELDS and LINES clauses, including their default values and permissible values, see [Section 15.2.9, "LOAD](#page-47-0) [DATA Statement"](#page-47-0).

FIELDS ESCAPED BY controls how to write special characters. If the FIELDS ESCAPED BY character is not empty, it is used when necessary to avoid ambiguity as a prefix that precedes following characters on output:

- The FIELDS ESCAPED BY character
- The FIELDS [OPTIONALLY] ENCLOSED BY character
- The first character of the FIELDS TERMINATED BY and LINES TERMINATED BY values
- ASCII NUL (the zero-valued byte; what is actually written following the escape character is ASCII 0, not a zero-valued byte)

The FIELDS TERMINATED BY, ENCLOSED BY, ESCAPED BY, or LINES TERMINATED BY characters must be escaped so that you can read the file back in reliably. ASCII NUL is escaped to make it easier to view with some pagers.

The resulting file need not conform to SQL syntax, so nothing else need be escaped.

If the FIELDS ESCAPED BY character is empty, no characters are escaped and NULL is output as NULL, not \N. It is probably not a good idea to specify an empty escape character, particularly if field values in your data contain any of the characters in the list just given.

INTO OUTFILE can also be used with a [TABLE](#page-105-0) statement when you want to dump all columns of a table into a text file. In this case, the ordering and number of rows can be controlled using ORDER BY and LIMIT; these clauses must precede INTO OUTFILE. TABLE ... INTO OUTFILE supports the same export\_options as does SELECT ... INTO OUTFILE, and it is subject to the same restrictions on writing to the file system. An example of such a statement is shown here:

```
TABLE employees ORDER BY lname LIMIT 1000
 INTO OUTFILE '/tmp/employee_data_1.txt'
 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"', ESCAPED BY '\'
 LINES TERMINATED BY '\n';
```

You can also use SELECT ... INTO OUTFILE with a [VALUES](#page-112-0) statement to write values directly into a file. An example is shown here:

```
SELECT * FROM (VALUES ROW(1,2,3),ROW(4,5,6),ROW(7,8,9)) AS t
 INTO OUTFILE '/tmp/select-values.txt';
```

You must use a table alias; column aliases are also supported, and can optionally be used to write values only from desired columns. You can also use any or all of the export options supported by SELECT ... INTO OUTFILE to format the output to the file.

Here is an example that produces a file in the comma-separated values (CSV) format used by many programs:

```
SELECT a,b,a+b INTO OUTFILE '/tmp/result.txt'
 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
 LINES TERMINATED BY '\n'
 FROM test_table;
```

If you use INTO DUMPFILE instead of INTO OUTFILE, MySQL writes only one row into the file, without any column or line termination and without performing any escape processing. This is useful for selecting a BLOB value and storing it in a file.

[TABLE](#page-105-0) also supports INTO DUMPFILE. If the table contains more than one row, you must also use LIMIT 1 to limit the output to a single row. INTO DUMPFILE can also be used with SELECT \* FROM (VALUES ROW()[, ...]) AS table\_alias [LIMIT 1]. See [Section 15.2.19, "VALUES](#page-112-0) [Statement".](#page-112-0)

![](_page_79_Picture_8.jpeg)

#### **Note**

Any file created by INTO OUTFILE or INTO DUMPFILE is owned by the operating system user under whose account mysqld runs. (You should never run mysqld as root for this and other reasons.) The umask for file creation is 0640; you must have sufficient access privileges to manipulate the file contents.

If the secure\_file\_priv system variable is set to a nonempty directory name, the file to be written must be located in that directory.

In the context of [SELECT ... INTO](#page-76-0) statements that occur as part of events executed by the Event Scheduler, diagnostics messages (not only errors, but also warnings) are written to the error log, and, on Windows, to the application event log. For additional information, see Section 27.4.5, "Event Scheduler Status".

Support is provided for periodic synchronization of output files written to by SELECT INTO OUTFILE and SELECT INTO DUMPFILE, enabled by setting the select\_into\_disk\_sync server system variable introduced in that version. Output buffer size and optional delay can be set using, respectively, select\_into\_buffer\_size and select\_into\_disk\_sync\_delay. For more information, see the descriptions of these system variables.

## <span id="page-79-0"></span>**15.2.13.2 JOIN Clause**

MySQL supports the following JOIN syntax for the table\_references part of [SELECT](#page-70-0) statements and multiple-table [DELETE](#page-27-0) and [UPDATE](#page-108-0) statements:

```
table_references:
 escaped_table_reference [, escaped_table_reference] ...
escaped_table_reference: {
 table_reference
 | { OJ table_reference }
}
table_reference: {
 table_factor
 | joined_table
}
```

```
table_factor: {
 tbl_name [PARTITION (partition_names)]
 [[AS] alias] [index_hint_list]
 | [LATERAL] table_subquery [AS] alias [(col_list)]
 | ( table_references )
}
joined_table: {
 table_reference {[INNER | CROSS] JOIN | STRAIGHT_JOIN} table_factor [join_specification]
 | table_reference {LEFT|RIGHT} [OUTER] JOIN table_reference join_specification
 | table_reference NATURAL [INNER | {LEFT|RIGHT} [OUTER]] JOIN table_factor
}
join_specification: {
 ON search_condition
 | USING (join_column_list)
}
join_column_list:
 column_name[, column_name] ...
index_hint_list:
 index_hint[ index_hint] ...
index_hint: {
 USE {INDEX|KEY}
 [FOR {JOIN|ORDER BY|GROUP BY}] ([index_list])
 | {IGNORE|FORCE} {INDEX|KEY}
 [FOR {JOIN|ORDER BY|GROUP BY}] (index_list)
}
index_list:
 index_name [, index_name] ...
```

A table reference is also known as a join expression.

A table reference (when it refers to a partitioned table) may contain a PARTITION clause, including a list of comma-separated partitions, subpartitions, or both. This option follows the name of the table and precedes any alias declaration. The effect of this option is that rows are selected only from the listed partitions or subpartitions. Any partitions or subpartitions not named in the list are ignored. For more information and examples, see Section 26.5, "Partition Selection".

The syntax of table\_factor is extended in MySQL in comparison with standard SQL. The standard accepts only table\_reference, not a list of them inside a pair of parentheses.

This is a conservative extension if each comma in a list of table\_reference items is considered as equivalent to an inner join. For example:

```
SELECT * FROM t1 LEFT JOIN (t2, t3, t4)
 ON (t2.a = t1.a AND t3.b = t1.b AND t4.c = t1.c)
```

is equivalent to:

```
SELECT * FROM t1 LEFT JOIN (t2 CROSS JOIN t3 CROSS JOIN t4)
 ON (t2.a = t1.a AND t3.b = t1.b AND t4.c = t1.c)
```

In MySQL, JOIN, CROSS JOIN, and INNER JOIN are syntactic equivalents (they can replace each other). In standard SQL, they are not equivalent. INNER JOIN is used with an ON clause, CROSS JOIN is used otherwise.

In general, parentheses can be ignored in join expressions containing only inner join operations. MySQL also supports nested joins. See Section 10.2.1.8, "Nested Join Optimization".

Index hints can be specified to affect how the MySQL optimizer makes use of indexes. For more information, see Section 10.9.4, "Index Hints". Optimizer hints and the optimizer\_switch system variable are other ways to influence optimizer use of indexes. See Section 10.9.3, "Optimizer Hints", and Section 10.9.2, "Switchable Optimizations".

The following list describes general factors to take into account when writing joins:

• A table reference can be aliased using tbl\_name AS alias\_name or tbl\_name alias\_name:

```
SELECT t1.name, t2.salary
 FROM employee AS t1 INNER JOIN info AS t2 ON t1.name = t2.name;
SELECT t1.name, t2.salary
 FROM employee t1 INNER JOIN info t2 ON t1.name = t2.name;
```

• A table\_subquery is also known as a derived table or subquery in the FROM clause. See [Section 15.2.15.8, "Derived Tables"](#page-97-0). Such subqueries must include an alias to give the subquery result a table name, and may optionally include a list of table column names in parentheses. A trivial example follows:

```
SELECT * FROM (SELECT 1, 2, 3) AS t1;
```

- The maximum number of tables that can be referenced in a single join is 61. This includes a join handled by merging derived tables and views in the FROM clause into the outer query block (see Section 10.2.2.4, "Optimizing Derived Tables, View References, and Common Table Expressions with Merging or Materialization").
- INNER JOIN and , (comma) are semantically equivalent in the absence of a join condition: both produce a Cartesian product between the specified tables (that is, each and every row in the first table is joined to each and every row in the second table).

However, the precedence of the comma operator is less than that of INNER JOIN, CROSS JOIN, LEFT JOIN, and so on. If you mix comma joins with the other join types when there is a join condition, an error of the form Unknown column 'col\_name' in 'on clause' may occur. Information about dealing with this problem is given later in this section.

- The search\_condition used with ON is any conditional expression of the form that can be used in a WHERE clause. Generally, the ON clause serves for conditions that specify how to join tables, and the WHERE clause restricts which rows to include in the result set.
- If there is no matching row for the right table in the ON or USING part in a LEFT JOIN, a row with all columns set to NULL is used for the right table. You can use this fact to find rows in a table that have no counterpart in another table:

```
SELECT left_tbl.*
 FROM left_tbl LEFT JOIN right_tbl ON left_tbl.id = right_tbl.id
 WHERE right_tbl.id IS NULL;
```

This example finds all rows in left\_tbl with an id value that is not present in right\_tbl (that is, all rows in left\_tbl with no corresponding row in right\_tbl). See Section 10.2.1.9, "Outer Join Optimization".

• The USING(join\_column\_list) clause names a list of columns that must exist in both tables. If tables a and b both contain columns c1, c2, and c3, the following join compares corresponding columns from the two tables:

```
a LEFT JOIN b USING (c1, c2, c3)
```

- The NATURAL [LEFT] JOIN of two tables is defined to be semantically equivalent to an INNER JOIN or a LEFT JOIN with a USING clause that names all columns that exist in both tables.
- RIGHT JOIN works analogously to LEFT JOIN. To keep code portable across databases, it is recommended that you use LEFT JOIN instead of RIGHT JOIN.
- The { OJ ... } syntax shown in the join syntax description exists only for compatibility with ODBC. The curly braces in the syntax should be written literally; they are not metasyntax as used elsewhere in syntax descriptions.

```
SELECT left_tbl.*
```

```
 FROM { OJ left_tbl LEFT OUTER JOIN right_tbl
 ON left_tbl.id = right_tbl.id }
 WHERE right_tbl.id IS NULL;
```

You can use other types of joins within { OJ ... }, such as INNER JOIN or RIGHT OUTER JOIN. This helps with compatibility with some third-party applications, but is not official ODBC syntax.

• STRAIGHT\_JOIN is similar to JOIN, except that the left table is always read before the right table. This can be used for those (few) cases for which the join optimizer processes the tables in a suboptimal order.

Some join examples:

```
SELECT * FROM table1, table2;
SELECT * FROM table1 INNER JOIN table2 ON table1.id = table2.id;
SELECT * FROM table1 LEFT JOIN table2 ON table1.id = table2.id;
SELECT * FROM table1 LEFT JOIN table2 USING (id);
SELECT * FROM table1 LEFT JOIN table2 ON table1.id = table2.id
 LEFT JOIN table3 ON table2.id = table3.id;
```

Natural joins and joins with USING, including outer join variants, are processed according to the SQL:2003 standard:

• Redundant columns of a NATURAL join do not appear. Consider this set of statements:

```
CREATE TABLE t1 (i INT, j INT);
CREATE TABLE t2 (k INT, j INT);
INSERT INTO t1 VALUES(1, 1);
INSERT INTO t2 VALUES(1, 1);
SELECT * FROM t1 NATURAL JOIN t2;
SELECT * FROM t1 JOIN t2 USING (j);
```

In the first [SELECT](#page-70-0) statement, column j appears in both tables and thus becomes a join column, so, according to standard SQL, it should appear only once in the output, not twice. Similarly, in the second SELECT statement, column j is named in the USING clause and should appear only once in the output, not twice.

Thus, the statements produce this output:

```
+------+------+------+
| j | i | k |
+------+------+------+
| 1 | 1 | 1 |
+------+------+------+
+------+------+------+
| j | i | k |
+------+------+------+
| 1 | 1 | 1 |
+------+------+------+
```

Redundant column elimination and column ordering occurs according to standard SQL, producing this display order:

- First, coalesced common columns of the two joined tables, in the order in which they occur in the first table
- Second, columns unique to the first table, in order in which they occur in that table
- Third, columns unique to the second table, in order in which they occur in that table

The single result column that replaces two common columns is defined using the coalesce operation. That is, for two t1.a and t2.a the resulting single join column a is defined as a = COALESCE(t1.a, t2.a), where:

```
COALESCE(x, y) = (CASE WHEN x IS NOT NULL THEN x ELSE y END)
```

If the join operation is any other join, the result columns of the join consist of the concatenation of all columns of the joined tables.

A consequence of the definition of coalesced columns is that, for outer joins, the coalesced column contains the value of the non-NULL column if one of the two columns is always NULL. If neither or both columns are NULL, both common columns have the same value, so it doesn't matter which one is chosen as the value of the coalesced column. A simple way to interpret this is to consider that a coalesced column of an outer join is represented by the common column of the inner table of a JOIN. Suppose that the tables t1(a, b) and t2(a, c) have the following contents:

```
t1 t2
---- ----
1 x 2 z
2 y 3 w
```

Then, for this join, column a contains the values of t1.a:

```
mysql> SELECT * FROM t1 NATURAL LEFT JOIN t2;
+------+------+------+
| a | b | c |
+------+------+------+
| 1 | x | NULL |
| 2 | y | z |
+------+------+------+
```

By contrast, for this join, column a contains the values of t2.a.

```
mysql> SELECT * FROM t1 NATURAL RIGHT JOIN t2;
+------+------+------+
| a | c | b |
+------+------+------+
| 2 | z | y |
| 3 | w | NULL |
+------+------+------+
```

Compare those results to the otherwise equivalent queries with JOIN ... ON:

```
mysql> SELECT * FROM t1 LEFT JOIN t2 ON (t1.a = t2.a);
+------+------+------+------+
| a | b | a | c |
+------+------+------+------+
| 1 | x | NULL | NULL |
| 2 | y | 2 | z |
+------+------+------+------+
```

```
mysql> SELECT * FROM t1 RIGHT JOIN t2 ON (t1.a = t2.a);
+------+------+------+------+
| a | b | a | c |
+------+------+------+------+
| 2 | y | 2 | z |
| NULL | NULL | 3 | w |
+------+------+------+------+
```

• A USING clause can be rewritten as an ON clause that compares corresponding columns. However, although USING and ON are similar, they are not quite the same. Consider the following two queries:

```
a LEFT JOIN b USING (c1, c2, c3)
```

```
a LEFT JOIN b ON a.c1 = b.c1 AND a.c2 = b.c2 AND a.c3 = b.c3
```

With respect to determining which rows satisfy the join condition, both joins are semantically identical.

With respect to determining which columns to display for SELECT \* expansion, the two joins are not semantically identical. The USING join selects the coalesced value of corresponding columns, whereas the ON join selects all columns from all tables. For the USING join, SELECT \* selects these values:

```
COALESCE(a.c1, b.c1), COALESCE(a.c2, b.c2), COALESCE(a.c3, b.c3)
```

For the ON join, SELECT \* selects these values:

```
a.c1, a.c2, a.c3, b.c1, b.c2, b.c3
```

With an inner join, COALESCE(a.c1, b.c1) is the same as either a.c1 or b.c1 because both columns have the same value. With an outer join (such as LEFT JOIN), one of the two columns can be NULL. That column is omitted from the result.

• An ON clause can refer only to its operands.

#### Example:

```
CREATE TABLE t1 (i1 INT);
CREATE TABLE t2 (i2 INT);
CREATE TABLE t3 (i3 INT);
SELECT * FROM t1 JOIN t2 ON (i1 = i3) JOIN t3;
```

The statement fails with an Unknown column 'i3' in 'on clause' error because i3 is a column in t3, which is not an operand of the ON clause. To enable the join to be processed, rewrite the statement as follows:

```
SELECT * FROM t1 JOIN t2 JOIN t3 ON (i1 = i3);
```

• JOIN has higher precedence than the comma operator (,), so the join expression t1, t2 JOIN t3 is interpreted as (t1, (t2 JOIN t3)), not as ((t1, t2) JOIN t3). This affects statements that use an ON clause because that clause can refer only to columns in the operands of the join, and the precedence affects interpretation of what those operands are.

#### Example:

```
CREATE TABLE t1 (i1 INT, j1 INT);
CREATE TABLE t2 (i2 INT, j2 INT);
CREATE TABLE t3 (i3 INT, j3 INT);
INSERT INTO t1 VALUES(1, 1);
INSERT INTO t2 VALUES(1, 1);
INSERT INTO t3 VALUES(1, 1);
SELECT * FROM t1, t2 JOIN t3 ON (t1.i1 = t3.i3);
```

The JOIN takes precedence over the comma operator, so the operands for the ON clause are t2 and t3. Because t1.i1 is not a column in either of the operands, the result is an Unknown column 't1.i1' in 'on clause' error.

To enable the join to be processed, use either of these strategies:

• Group the first two tables explicitly with parentheses so that the operands for the ON clause are (t1, t2) and t3:

```
SELECT * FROM (t1, t2) JOIN t3 ON (t1.i1 = t3.i3);
```

• Avoid the use of the comma operator and use JOIN instead:

```
SELECT * FROM t1 JOIN t2 JOIN t3 ON (t1.i1 = t3.i3);
```

The same precedence interpretation also applies to statements that mix the comma operator with INNER JOIN, CROSS JOIN, LEFT JOIN, and RIGHT JOIN, all of which have higher precedence than the comma operator.

• A MySQL extension compared to the SQL:2003 standard is that MySQL permits you to qualify the common (coalesced) columns of NATURAL or USING joins, whereas the standard disallows that.

# <span id="page-85-0"></span>**15.2.14 Set Operations with UNION, INTERSECT, and EXCEPT**

- [Result Set Column Names and Data Types](#page-86-0)
- [Set Operations with TABLE and VALUES Statements](#page-87-0)
- [Set Operations using DISTINCT and ALL](#page-88-0)
- [Set Operations with ORDER BY and LIMIT](#page-88-1)
- [Limitations of Set Operations](#page-89-0)

SQL set operations combine the results of multiple query blocks into a single result. A query block, sometimes also known as a simple table, is any SQL statement that returns a result set, such as [SELECT](#page-70-0). MySQL 8.4 also supports [TABLE](#page-105-0) and [VALUES](#page-112-0) statements. See the individual descriptions of these statements elsewhere in this chapter for additional information.

The SQL standard defines the following three set operations:

- [UNION](#page-111-0): Combine all results from two query blocks into a single result, omitting any duplicates.
- [INTERSECT](#page-46-0): Combine only those rows which the results of two query blocks have in common, omitting any duplicates.
- [EXCEPT](#page-31-1): For two query blocks A and B, return all results from A which are not also present in B, omitting any duplicates.

(Some database systems, such as Oracle, use MINUS for the name of this operator. This is not supported in MySQL.)

MySQL supports UNION, INTERSECT, and EXCEPT.

Each of these set operators supports an ALL modifier. When the ALL keyword follows a set operator, this causes duplicates to be included in the result. See the following sections covering the individual operators for more information and examples.

All three set operators also support a DISTINCT keyword, which suppresses duplicates in the result. Since this is the default behavior for set operators, it is usually not necessary to specify DISTINCT explicitly.

In general, query blocks and set operations can be combined in any number and order. A greatly simplified representation is shown here:

```
query_block [set_op query_block] [set_op query_block] ...
query_block:
 SELECT | TABLE | VALUES
set_op:
 UNION | INTERSECT | EXCEPT
```

This can be represented more accurately, and in greater detail, like this:

```
query_expression:
 [with_clause] /* WITH clause */ 
 query_expression_body
 [order_by_clause] [limit_clause] [into_clause]
query_expression_body:
 query_term
 | query_expression_body UNION [ALL | DISTINCT] query_term
 | query_expression_body EXCEPT [ALL | DISTINCT] query_term
query_term:
 query_primary
 | query_term INTERSECT [ALL | DISTINCT] query_primary
query_primary:
 query_block
 | '(' query_expression_body [order_by_clause] [limit_clause] [into_clause] ')'
query_block: /* also known as a simple table */
 query_specification /* SELECT statement */
 | table_value_constructor /* VALUES statement */
 | explicit_table /* TABLE statement */
```

You should be aware that INTERSECT is evaluated before UNION or EXCEPT. This means that, for example, TABLE x UNION TABLE y INTERSECT TABLE z is always evaluated as TABLE x UNION (TABLE y INTERSECT TABLE z). See [Section 15.2.8, "INTERSECT Clause",](#page-46-0) for more information.

In addition, you should keep in mind that, while the UNION and INTERSECT set operators are commutative (ordering is not significant), EXCEPT is not (order of operands affects the outcome). In other words, all of the following statements are true:

- TABLE x UNION TABLE y and TABLE y UNION TABLE x produce the same result, although the ordering of the rows may differ. You can force them to be the same using ORDER BY; see [Set](#page-88-1) [Operations with ORDER BY and LIMIT](#page-88-1).
- TABLE x INTERSECT TABLE y and TABLE y INTERSECT TABLE x return the same result.
- TABLE x EXCEPT TABLE y and TABLE y EXCEPT TABLE x do not yield the same result. See [Section 15.2.4, "EXCEPT Clause"](#page-31-1), for an example.

More information and examples can be found in the sections that follow.

# <span id="page-86-0"></span>**Result Set Column Names and Data Types**

The column names for the result of a set operation are taken from the column names of the first query block. Example:

```
mysql> CREATE TABLE t1 (x INT, y INT);
Query OK, 0 rows affected (0.04 sec)
mysql> INSERT INTO t1 VALUES ROW(4,-2), ROW(5,9);
Query OK, 2 rows affected (0.00 sec)
Records: 2 Duplicates: 0 Warnings: 0
mysql> CREATE TABLE t2 (a INT, b INT);
Query OK, 0 rows affected (0.04 sec)
mysql> INSERT INTO t2 VALUES ROW(1,2), ROW(3,4);
Query OK, 2 rows affected (0.01 sec)
Records: 2 Duplicates: 0 Warnings: 0
mysql> TABLE t1 UNION TABLE t2;
+------+------+
| x | y |
+------+------+
| 4 | -2 |
| 5 | 9 |
```

```
| 1 | 2 |
| 3 | 4 |
+------+------+
4 rows in set (0.00 sec)
mysql> TABLE t2 UNION TABLE t1;
+------+------+
| a | b |
+------+------+
| 1 | 2 |
| 3 | 4 |
| 4 | -2 |
| 5 | 9 |
+------+------+
4 rows in set (0.00 sec)
```

This is true for UNION, EXCEPT, and INTERSECT queries.

Selected columns listed in corresponding positions of each query block should have the same data type. For example, the first column selected by the first statement should have the same type as the first column selected by the other statements. If the data types of corresponding result columns do not match, the types and lengths of the columns in the result take into account the values retrieved by all of the query blocks. For example, the column length in the result set is not constrained to the length of the value from the first statement, as shown here:

```
mysql> SELECT REPEAT('a',1) UNION SELECT REPEAT('b',20);
+----------------------+
| REPEAT('a',1) |
+----------------------+
| a |
| bbbbbbbbbbbbbbbbbbbb |
+----------------------+
```

# <span id="page-87-0"></span>**Set Operations with TABLE and VALUES Statements**

You can also use a [TABLE](#page-105-0) statement or [VALUES](#page-112-0) statement wherever you can employ the equivalent [SELECT](#page-70-0) statement. Assume that tables t1 and t2 are created and populated as shown here:

```
CREATE TABLE t1 (x INT, y INT);
INSERT INTO t1 VALUES ROW(4,-2),ROW(5,9);
CREATE TABLE t2 (a INT, b INT);
INSERT INTO t2 VALUES ROW(1,2),ROW(3,4);
```

The preceding being the case, and disregarding the column names in the output of the queries beginning with [VALUES](#page-112-0), all of the following UNION queries yield the same result:

```
SELECT * FROM t1 UNION SELECT * FROM t2;
TABLE t1 UNION SELECT * FROM t2;
VALUES ROW(4,-2), ROW(5,9) UNION SELECT * FROM t2;
SELECT * FROM t1 UNION TABLE t2;
TABLE t1 UNION TABLE t2;
VALUES ROW(4,-2), ROW(5,9) UNION TABLE t2;
SELECT * FROM t1 UNION VALUES ROW(4,-2),ROW(5,9);
TABLE t1 UNION VALUES ROW(4,-2),ROW(5,9);
VALUES ROW(4,-2), ROW(5,9) UNION VALUES ROW(4,-2),ROW(5,9);
```

To force the column names to be the same, wrap the query block on the left-hand side in a SELECT statement, and use aliases, like this:

```
mysql> SELECT * FROM (TABLE t2) AS t(x,y) UNION TABLE t1;
+------+------+
| x | y |
+------+------+
| 1 | 2 |
| 3 | 4 |
| 4 | -2 |
| 5 | 9 |
```

```
+------+------+
4 rows in set (0.00 sec)
```

# <span id="page-88-0"></span>**Set Operations using DISTINCT and ALL**

By default, duplicate rows are removed from results of set operations. The optional DISTINCT keyword has the same effect but makes it explicit. With the optional ALL keyword, duplicate-row removal does not occur and the result includes all matching rows from all queries in the union.

You can mix ALL and DISTINCT in the same query. Mixed types are treated such that a set operation using DISTINCT overrides any such operation using ALL to its left. A DISTINCT set can be produced explicitly by using DISTINCT with [UNION](#page-111-0), [INTERSECT](#page-46-0), or [EXCEPT](#page-31-1), or implicitly by using the set operations with no following DISTINCT or ALL keyword.

Set operations work the same way when one or more [TABLE](#page-105-0) statements, [VALUES](#page-112-0) statements, or both, are used to generate the set.

# <span id="page-88-1"></span>**Set Operations with ORDER BY and LIMIT**

To apply an ORDER BY or LIMIT clause to an individual query block used as part of a union, intersection, or other set operation, parenthesize the query block, placing the clause inside the parentheses, like this:

```
(SELECT a FROM t1 WHERE a=10 AND b=1 ORDER BY a LIMIT 10)
UNION
(SELECT a FROM t2 WHERE a=11 AND b=2 ORDER BY a LIMIT 10);
(TABLE t1 ORDER BY x LIMIT 10) 
INTERSECT 
(TABLE t2 ORDER BY a LIMIT 10);
```

Use of ORDER BY for individual query blocks or statements implies nothing about the order in which the rows appear in the final result because the rows produced by a set operation are by default unordered. Therefore, ORDER BY in this context typically is used in conjunction with LIMIT, to determine the subset of the selected rows to retrieve, even though it does not necessarily affect the order of those rows in the final result. If ORDER BY appears without LIMIT within a query block, it is optimized away because it has no effect in any case.

To use an ORDER BY or LIMIT clause to sort or limit the entire result of a set operation, place the ORDER BY or LIMIT after the last statement:

```
SELECT a FROM t1
EXCEPT
SELECT a FROM t2 WHERE a=11 AND b=2
ORDER BY a LIMIT 10;
TABLE t1
UNION 
TABLE t2
ORDER BY a LIMIT 10;
```

If one or more individual statements make use of ORDER BY, LIMIT, or both, and, in addition, you wish to apply an ORDER BY, LIMIT, or both to the entire result, then each such individual statement must be enclosed in parentheses.

```
(SELECT a FROM t1 WHERE a=10 AND b=1)
EXCEPT
(SELECT a FROM t2 WHERE a=11 AND b=2)
ORDER BY a LIMIT 10;
(TABLE t1 ORDER BY a LIMIT 10) 
UNION 
TABLE t2 
ORDER BY a LIMIT 10;
```

A statement with no ORDER BY or LIMIT clause does need to be parenthesized; replacing TABLE t2 with (TABLE t2) in the second statement of the two just shown does not alter the result of the UNION.

You can also use ORDER BY and LIMIT with [VALUES](#page-112-0) statements in set operations, as shown in this example using the mysql client:

```
mysql> VALUES ROW(4,-2), ROW(5,9), ROW(-1,3)
 -> UNION
 -> VALUES ROW(1,2), ROW(3,4), ROW(-1,3)
 -> ORDER BY column_0 DESC LIMIT 3;
+----------+----------+
| column_0 | column_1 |
+----------+----------+
| 5 | 9 |
| 4 | -2 |
| 3 | 4 |
+----------+----------+
3 rows in set (0.00 sec)
```

(You should keep in mind that neither TABLE statements nor VALUES statements accept a WHERE clause.)

This kind of ORDER BY cannot use column references that include a table name (that is, names in tbl\_name.col\_name format). Instead, provide a column alias in the first query block, and refer to the alias in the ORDER BY clause. (You can also refer to the column in the ORDER BY clause using its column position, but such use of column positions is deprecated, and thus subject to eventual removal in a future MySQL release.)

If a column to be sorted is aliased, the ORDER BY clause must refer to the alias, not the column name. The first of the following statements is permitted, but the second fails with an Unknown column 'a' in 'order clause' error:

```
(SELECT a AS b FROM t) UNION (SELECT ...) ORDER BY b;
(SELECT a AS b FROM t) UNION (SELECT ...) ORDER BY a;
```

To cause rows in a [UNION](#page-111-0) result to consist of the sets of rows retrieved by each query block one after the other, select an additional column in each query block to use as a sort column and add an ORDER BY clause that sorts on that column following the last query block:

```
(SELECT 1 AS sort_col, col1a, col1b, ... FROM t1)
UNION
(SELECT 2, col2a, col2b, ... FROM t2) ORDER BY sort_col;
```

To maintain sort order within individual results, add a secondary column to the ORDER BY clause:

```
(SELECT 1 AS sort_col, col1a, col1b, ... FROM t1)
UNION
(SELECT 2, col2a, col2b, ... FROM t2) ORDER BY sort_col, col1a;
```

Use of an additional column also enables you to determine which query block each row comes from. Extra columns can provide other identifying information as well, such as a string that indicates a table name.

## <span id="page-89-0"></span>**Limitations of Set Operations**

Set operations in MySQL are subject to some limitations, which are described in the next few paragraphs.

Set operations including [SELECT](#page-70-0) statements have the following limitations:

- HIGH\_PRIORITY in the first SELECT has no effect. HIGH\_PRIORITY in any subsequent SELECT produces a syntax error.
- Only the last SELECT statement can use an INTO clause. However, the entire UNION result is written to the INTO output destination.

These two UNION variants containing INTO are deprecated; you should expect support for them to be removed in a future version of MySQL:

• In the trailing query block of a query expression, use of INTO before FROM produces a warning. Example:

```
... UNION SELECT * INTO OUTFILE 'file_name' FROM table_name;
```

• In a parenthesized trailing block of a query expression, use of INTO (regardless of its position relative to FROM) produces a warning. Example:

```
... UNION (SELECT * INTO OUTFILE 'file_name' FROM table_name);
```

Those variants are deprecated because they are confusing, as if they collect information from the named table rather than the entire query expression (the UNION).

Set operations with an aggregate function in an ORDER BY clause are rejected with [ER\\_AGGREGATE\\_ORDER\\_FOR\\_UNION](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_aggregate_order_for_union). Although the error name might suggest that this is exclusive to UNION queries, the preceding is also true for EXCEPT and INTERSECT queries, as shown here:

```
mysql> TABLE t1 INTERSECT TABLE t2 ORDER BY MAX(x);
ERROR 3028 (HY000): Expression #1 of ORDER BY contains aggregate function and applies to a UNION, EXCEPT or INTERSECT
```

A locking clause (such as FOR UPDATE or LOCK IN SHARE MODE) applies to the query block it follows. This means that, in a SELECT statement used with set operations, a locking clause can be used only if the query block and locking clause are enclosed in parentheses.

# <span id="page-90-0"></span>**15.2.15 Subqueries**

A subquery is a [SELECT](#page-70-0) statement within another statement.

All subquery forms and operations that the SQL standard requires are supported, as well as a few features that are MySQL-specific.

Here is an example of a subquery:

```
SELECT * FROM t1 WHERE column1 = (SELECT column1 FROM t2);
```

In this example, SELECT \* FROM t1 ... is the outer query (or outer statement), and (SELECT column1 FROM t2) is the subquery. We say that the subquery is nested within the outer query, and in fact it is possible to nest subqueries within other subqueries, to a considerable depth. A subquery must always appear within parentheses.

The main advantages of subqueries are:

- They allow queries that are structured so that it is possible to isolate each part of a statement.
- They provide alternative ways to perform operations that would otherwise require complex joins and unions.
- Many people find subqueries more readable than complex joins or unions. Indeed, it was the innovation of subqueries that gave people the original idea of calling the early SQL "Structured Query Language."

Here is an example statement that shows the major points about subquery syntax as specified by the SQL standard and supported in MySQL:

```
DELETE FROM t1
WHERE s11 > ANY
 (SELECT COUNT(*) /* no hint */ FROM t2
 WHERE NOT EXISTS
 (SELECT * FROM t3
 WHERE ROW(5*t2.s1,77)=
 (SELECT 50,11*s1 FROM t4 UNION SELECT 50,77 FROM
```

```
 (SELECT * FROM t5) AS t5)));
```

A subquery can return a scalar (a single value), a single row, a single column, or a table (one or more rows of one or more columns). These are called scalar, column, row, and table subqueries. Subqueries that return a particular kind of result often can be used only in certain contexts, as described in the following sections.

There are few restrictions on the type of statements in which subqueries can be used. A subquery can contain many of the keywords or clauses that an ordinary [SELECT](#page-70-0) can contain: DISTINCT, GROUP BY, ORDER BY, LIMIT, joins, index hints, [UNION](#page-111-0) constructs, comments, functions, and so on.

[TABLE](#page-105-0) and [VALUES](#page-112-0) statements can be used in subqueries. Subqueries using VALUES are generally more verbose versions of subqueries that can be rewritten more compactly using set notation, or with [SELECT](#page-70-0) or TABLE syntax; assuming that table ts is created using the statement CREATE TABLE ts VALUES ROW(2), ROW(4), ROW(6), the statements shown here are all equivalent:

```
SELECT * FROM tt
 WHERE b > ANY (VALUES ROW(2), ROW(4), ROW(6));
SELECT * FROM tt
 WHERE b > ANY (SELECT * FROM ts);
SELECT * FROM tt
 WHERE b > ANY (TABLE ts);
```

Examples of [TABLE](#page-105-0) subqueries are shown in the sections that follow.

A subquery's outer statement can be any one of: [SELECT](#page-70-0), [INSERT](#page-36-0), [UPDATE](#page-108-0), [DELETE](#page-27-0), SET, or [DO](#page-31-0).

For information about how the optimizer handles subqueries, see Section 10.2.2, "Optimizing Subqueries, Derived Tables, View References, and Common Table Expressions". For a discussion of restrictions on subquery use, including performance issues for certain forms of subquery syntax, see [Section 15.2.15.12, "Restrictions on Subqueries"](#page-104-0).