---
source: MySQL 8.4 Reference
title: 00_Overview
---

# <span id="page-25-0"></span>**15.2.1 CALL Statement**

```
CALL sp_name([parameter[,...]])
CALL sp_name[()]
```

The [CALL](#page-25-0) statement invokes a stored procedure that was defined previously with CREATE PROCEDURE.

Stored procedures that take no arguments can be invoked without parentheses. That is, CALL p() and CALL p are equivalent.

[CALL](#page-25-0) can pass back values to its caller using parameters that are declared as OUT or INOUT parameters. When the procedure returns, a client program can also obtain the number of rows affected for the final statement executed within the routine: At the SQL level, call the ROW\_COUNT() function; from the C API, call the [mysql\\_affected\\_rows\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-affected-rows.md) function.

For information about the effect of unhandled conditions on procedure parameters, see Section 15.6.7.8, "Condition Handling and OUT or INOUT Parameters".

To get back a value from a procedure using an OUT or INOUT parameter, pass the parameter by means of a user variable, and then check the value of the variable after the procedure returns. (If you are calling the procedure from within another stored procedure or function, you can also pass a routine parameter or local routine variable as an IN or INOUT parameter.) For an INOUT parameter, initialize its value before passing it to the procedure. The following procedure has an OUT parameter that the procedure sets to the current server version, and an INOUT value that the procedure increments by one from its current value:

```
DELIMITER //
CREATE PROCEDURE p (OUT ver_param VARCHAR(25), INOUT incr_param INT)
BEGIN
 # Set value of OUT parameter
 SELECT VERSION() INTO ver_param;
 # Increment value of INOUT parameter
 SET incr_param = incr_param + 1;
END //
DELIMITER ;
```

Before calling the procedure, initialize the variable to be passed as the INOUT parameter. After calling the procedure, you can see that the values of the two variables are set or modified:

```
mysql> SET @increment = 10;
mysql> CALL p(@version, @increment);
mysql> SELECT @version, @increment;
+----------+------------+
| @version | @increment |
+----------+------------+
| 8.4.8 | 11 |
+----------+------------+
```

In prepared [CALL](#page-25-0) statements used with [PREPARE](#page-174-0) and [EXECUTE](#page-176-0), placeholders can be used for IN parameters, OUT, and INOUT parameters. These types of parameters can be used as follows:

```
mysql> SET @increment = 10;
mysql> PREPARE s FROM 'CALL p(?, ?)';
mysql> EXECUTE s USING @version, @increment;
mysql> SELECT @version, @increment;
+----------+------------+
| @version | @increment |
+----------+------------+
| 8.4.8 | 11 |
+----------+------------+
```

To write C programs that use the [CALL](#page-25-0) SQL statement to execute stored procedures that produce result sets, the CLIENT\_MULTI\_RESULTS flag must be enabled. This is because each [CALL](#page-25-0) returns a result to indicate the call status, in addition to any result sets that might be returned by statements executed within the procedure. CLIENT\_MULTI\_RESULTS must also be enabled if [CALL](#page-25-0) is used to execute any stored procedure that contains prepared statements. It cannot be determined when such a procedure is loaded whether those statements produce result sets, so it is necessary to assume that they do so.

```
CLIENT_MULTI_RESULTS can be enabled when you call mysql_real_connect(),
either explicitly by passing the CLIENT_MULTI_RESULTS flag itself, or implicitly by
passing CLIENT_MULTI_STATEMENTS (which also enables CLIENT_MULTI_RESULTS).
CLIENT_MULTI_RESULTS is enabled by default.
```

To process the result of a [CALL](#page-25-0) statement executed using [mysql\\_query\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-query.md) or [mysql\\_real\\_query\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-query.md), use a loop that calls [mysql\\_next\\_result\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-next-result.md) to determine whether there are more results. For an example, see [Multiple Statement Execution Support](https://dev.mysql.com/doc/c-api/8.4/en/c-api-multiple-queries.md).

C programs can use the prepared-statement interface to execute [CALL](#page-25-0) statements and access OUT and INOUT parameters. This is done by processing the result of a [CALL](#page-25-0) statement using a loop that calls [mysql\\_stmt\\_next\\_result\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-stmt-next-result.md) to determine whether there are more results. For an example, see [Prepared CALL Statement Support.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-prepared-call-statements.md) Languages that provide a MySQL interface can use prepared [CALL](#page-25-0) statements to directly retrieve OUT and INOUT procedure parameters.

Metadata changes to objects referred to by stored programs are detected and cause automatic reparsing of the affected statements when the program is next executed. For more information, see Section 10.10.3, "Caching of Prepared Statements and Stored Programs".

# <span id="page-27-0"></span>**15.2.2 DELETE Statement**

[DELETE](#page-27-0) is a DML statement that removes rows from a table.

A [DELETE](#page-27-0) statement can start with a [WITH](#page-114-0) clause to define common table expressions accessible within the [DELETE](#page-27-0). See [Section 15.2.20, "WITH \(Common Table Expressions\)"](#page-114-0).

# **Single-Table Syntax**

```
DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name [[AS] tbl_alias]
 [PARTITION (partition_name [, partition_name] ...)]
 [WHERE where_condition]
 [ORDER BY ...]
 [LIMIT row_count]
```

The DELETE statement deletes rows from tbl\_name and returns the number of deleted rows. To check the number of deleted rows, call the ROW\_COUNT() function described in Section 14.15, "Information Functions".

# **Main Clauses**

The conditions in the optional WHERE clause identify which rows to delete. With no WHERE clause, all rows are deleted.

where\_condition is an expression that evaluates to true for each row to be deleted. It is specified as described in [Section 15.2.13, "SELECT Statement".](#page-70-0)

If the ORDER BY clause is specified, the rows are deleted in the order that is specified. The LIMIT clause places a limit on the number of rows that can be deleted. These clauses apply to single-table deletes, but not multi-table deletes.

## **Multiple-Table Syntax**

```
DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
 tbl_name[.*] [, tbl_name[.*]] ...
 FROM table_references
 [WHERE where_condition]
DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
 FROM tbl_name[.*] [, tbl_name[.*]] ...
 USING table_references
 [WHERE where_condition]
```

## **Privileges**

You need the DELETE privilege on a table to delete rows from it. You need only the SELECT privilege for any columns that are only read, such as those named in the WHERE clause.

# **Performance**

When you do not need to know the number of deleted rows, the [TRUNCATE TABLE](#page-24-0) statement is a faster way to empty a table than a [DELETE](#page-27-0) statement with no WHERE clause. Unlike [DELETE](#page-27-0), [TRUNCATE TABLE](#page-24-0) cannot be used within a transaction or if you have a lock on the table. See [Section 15.1.37, "TRUNCATE TABLE Statement"](#page-24-0) and [Section 15.3.6, "LOCK TABLES and UNLOCK](#page-131-0) [TABLES Statements"](#page-131-0).

The speed of delete operations may also be affected by factors discussed in Section 10.2.5.3, "Optimizing DELETE Statements".

To ensure that a given [DELETE](#page-27-0) statement does not take too much time, the MySQL-specific LIMIT row\_count clause for [DELETE](#page-27-0) specifies the maximum number of rows to be deleted. If the number of rows to delete is larger than the limit, repeat the DELETE statement until the number of affected rows is less than the LIMIT value.

# **Subqueries**

You cannot delete from a table and select from the same table in a subquery.

## **Partitioned Table Support**

DELETE supports explicit partition selection using the PARTITION clause, which takes a list of the comma-separated names of one or more partitions or subpartitions (or both) from which to select rows to be dropped. Partitions not included in the list are ignored. Given a partitioned table t with a partition named p0, executing the statement DELETE FROM t PARTITION (p0) has the same effect on the table as executing ALTER TABLE t TRUNCATE PARTITION (p0); in both cases, all rows in partition p0 are dropped.

PARTITION can be used along with a WHERE condition, in which case the condition is tested only on rows in the listed partitions. For example, DELETE FROM t PARTITION (p0) WHERE c < 5 deletes rows only from partition p0 for which the condition c < 5 is true; rows in any other partitions are not checked and thus not affected by the DELETE.

The PARTITION clause can also be used in multiple-table DELETE statements. You can use up to one such option per table named in the FROM option.

For more information and examples, see Section 26.5, "Partition Selection".

# **Auto-Increment Columns**

If you delete the row containing the maximum value for an AUTO\_INCREMENT column, the value is not reused for a MyISAM or InnoDB table. If you delete all rows in the table with DELETE FROM tbl\_name (without a WHERE clause) in autocommit mode, the sequence starts over for all storage engines except InnoDB and MyISAM. There are some exceptions to this behavior for InnoDB tables, as discussed in Section 17.6.1.6, "AUTO\_INCREMENT Handling in InnoDB".

For MyISAM tables, you can specify an AUTO\_INCREMENT secondary column in a multiple-column key. In this case, reuse of values deleted from the top of the sequence occurs even for MyISAM tables. See Section 5.6.9, "Using AUTO\_INCREMENT".

## **Modifiers**

The [DELETE](#page-27-0) statement supports the following modifiers:

- If you specify the LOW\_PRIORITY modifier, the server delays execution of the [DELETE](#page-27-0) until no other clients are reading from the table. This affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE).
- For MyISAM tables, if you use the QUICK modifier, the storage engine does not merge index leaves during delete, which may speed up some kinds of delete operations.
- The IGNORE modifier causes MySQL to ignore ignorable errors during the process of deleting rows. (Errors encountered during the parsing stage are processed in the usual manner.) Errors that are ignored due to the use of IGNORE are returned as warnings. For more information, see The Effect of IGNORE on Statement Execution.

## **Order of Deletion**

If the [DELETE](#page-27-0) statement includes an ORDER BY clause, rows are deleted in the order specified by the clause. This is useful primarily in conjunction with LIMIT. For example, the following statement finds

rows matching the WHERE clause, sorts them by timestamp\_column, and deletes the first (oldest) one:

```
DELETE FROM somelog WHERE user = 'jcole'
ORDER BY timestamp_column LIMIT 1;
```

ORDER BY also helps to delete rows in an order required to avoid referential integrity violations.

# **InnoDB Tables**

If you are deleting many rows from a large table, you may exceed the lock table size for an InnoDB table. To avoid this problem, or simply to minimize the time that the table remains locked, the following strategy (which does not use [DELETE](#page-27-0) at all) might be helpful:

1. Select the rows not to be deleted into an empty table that has the same structure as the original table:

```
INSERT INTO t_copy SELECT * FROM t WHERE ... ;
```

2. Use [RENAME TABLE](#page-22-2) to atomically move the original table out of the way and rename the copy to the original name:

```
RENAME TABLE t TO t_old, t_copy TO t;
```

3. Drop the original table:

```
DROP TABLE t_old;
```

No other sessions can access the tables involved while [RENAME TABLE](#page-22-2) executes, so the rename operation is not subject to concurrency problems. See [Section 15.1.36, "RENAME TABLE Statement".](#page-22-2)

# **MyISAM Tables**

In MyISAM tables, deleted rows are maintained in a linked list and subsequent [INSERT](#page-36-0) operations reuse old row positions. To reclaim unused space and reduce file sizes, use the OPTIMIZE TABLE statement or the myisamchk utility to reorganize tables. OPTIMIZE TABLE is easier to use, but myisamchk is faster. See Section 15.7.3.4, "OPTIMIZE TABLE Statement", and Section 6.6.4, "myisamchk — MyISAM Table-Maintenance Utility".

The QUICK modifier affects whether index leaves are merged for delete operations. DELETE QUICK is most useful for applications where index values for deleted rows are replaced by similar index values from rows inserted later. In this case, the holes left by deleted values are reused.

DELETE QUICK is not useful when deleted values lead to underfilled index blocks spanning a range of index values for which new inserts occur again. In this case, use of QUICK can lead to wasted space in the index that remains unreclaimed. Here is an example of such a scenario:

- 1. Create a table that contains an indexed AUTO\_INCREMENT column.
- 2. Insert many rows into the table. Each insert results in an index value that is added to the high end of the index.
- 3. Delete a block of rows at the low end of the column range using DELETE QUICK.

In this scenario, the index blocks associated with the deleted index values become underfilled but are not merged with other index blocks due to the use of QUICK. They remain underfilled when new inserts occur, because new rows do not have index values in the deleted range. Furthermore, they remain underfilled even if you later use [DELETE](#page-27-0) without QUICK, unless some of the deleted index values happen to lie in index blocks within or adjacent to the underfilled blocks. To reclaim unused index space under these circumstances, use OPTIMIZE TABLE.

If you are going to delete many rows from a table, it might be faster to use DELETE QUICK followed by OPTIMIZE TABLE. This rebuilds the index rather than performing many index block merge operations.

# **Multi-Table Deletes**

You can specify multiple tables in a [DELETE](#page-27-0) statement to delete rows from one or more tables depending on the condition in the WHERE clause. You cannot use ORDER BY or LIMIT in a multipletable DELETE. The table\_references clause lists the tables involved in the join, as described in [Section 15.2.13.2, "JOIN Clause".](#page-79-0)

For the first multiple-table syntax, only matching rows from the tables listed before the FROM clause are deleted. For the second multiple-table syntax, only matching rows from the tables listed in the FROM clause (before the USING clause) are deleted. The effect is that you can delete rows from many tables at the same time and have additional tables that are used only for searching:

```
DELETE t1, t2 FROM t1 INNER JOIN t2 INNER JOIN t3
WHERE t1.id=t2.id AND t2.id=t3.id;
```

#### Or:

```
DELETE FROM t1, t2 USING t1 INNER JOIN t2 INNER JOIN t3
WHERE t1.id=t2.id AND t2.id=t3.id;
```

These statements use all three tables when searching for rows to delete, but delete matching rows only from tables t1 and t2.

The preceding examples use INNER JOIN, but multiple-table [DELETE](#page-27-0) statements can use other types of join permitted in [SELECT](#page-70-0) statements, such as LEFT JOIN. For example, to delete rows that exist in t1 that have no match in t2, use a LEFT JOIN:

```
DELETE t1 FROM t1 LEFT JOIN t2 ON t1.id=t2.id WHERE t2.id IS NULL;
```

The syntax permits .\* after each tbl\_name for compatibility with Access.

If you use a multiple-table [DELETE](#page-27-0) statement involving InnoDB tables for which there are foreign key constraints, the MySQL optimizer might process tables in an order that differs from that of their parent/ child relationship. In this case, the statement fails and rolls back. Instead, you should delete from a single table and rely on the ON DELETE capabilities that InnoDB provides to cause the other tables to be modified accordingly.

![](_page_30_Picture_12.jpeg)

## **Note**

If you declare an alias for a table, you must use the alias when referring to the table:

```
DELETE t1 FROM test AS t1, test2 WHERE ...
```

Table aliases in a multiple-table [DELETE](#page-27-0) should be declared only in the table\_references part of the statement. Elsewhere, alias references are permitted but not alias declarations.

#### Correct:

```
DELETE a1, a2 FROM t1 AS a1 INNER JOIN t2 AS a2
WHERE a1.id=a2.id;
DELETE FROM a1, a2 USING t1 AS a1 INNER JOIN t2 AS a2
WHERE a1.id=a2.id;
```

#### Incorrect:

```
DELETE t1 AS a1, t2 AS a2 FROM t1 INNER JOIN t2
WHERE a1.id=a2.id;
DELETE FROM t1 AS a1, t2 AS a2 USING t1 INNER JOIN t2
WHERE a1.id=a2.id;
```

Table aliases are also supported for single-table DELETE statements.

# <span id="page-31-0"></span>**15.2.3 DO Statement**

```
DO expr [, expr] ...
```

[DO](#page-31-0) executes the expressions but does not return any results. In most respects, [DO](#page-31-0) is shorthand for SELECT expr, ..., but has the advantage that it is slightly faster when you do not care about the result.

[DO](#page-31-0) is useful primarily with functions that have side effects, such as RELEASE\_LOCK().

Example: This [SELECT](#page-70-0) statement pauses, but also produces a result set:

```
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
| 0 |
+----------+
1 row in set (5.02 sec)
```

[DO](#page-31-0), on the other hand, pauses without producing a result set.:

```
mysql> DO SLEEP(5);
Query OK, 0 rows affected (4.99 sec)
```

This could be useful, for example in a stored function or trigger, which prohibit statements that produce result sets.

[DO](#page-31-0) only executes expressions. It cannot be used in all cases where SELECT can be used. For example, DO id FROM t1 is invalid because it references a table.

# <span id="page-31-1"></span>**15.2.4 EXCEPT Clause**

```
query_expression_body EXCEPT [ALL | DISTINCT] query_expression_body
 [EXCEPT [ALL | DISTINCT] query_expression_body]
 [...]
query_expression_body:
 See Section 15.2.14, "Set Operations with UNION, INTERSECT, and EXCEPT"
```

[EXCEPT](#page-31-1) limits the result from the first query block to those rows which are (also) not found in the second. As with [UNION](#page-111-0) and [INTERSECT](#page-46-0), either query block can make use of any of [SELECT](#page-70-0), [TABLE](#page-105-0), or [VALUES](#page-112-0). An example using the tables a, b, and c defined in [Section 15.2.8, "INTERSECT Clause",](#page-46-0) is shown here:

```
mysql> TABLE a EXCEPT TABLE b;
+------+------+
| m | n |
+------+------+
| 2 | 3 |
+------+------+
1 row in set (0.00 sec)
mysql> TABLE a EXCEPT TABLE c;
+------+------+
| m | n |
+------+------+
| 1 | 2 |
| 2 | 3 |
+------+------+
2 rows in set (0.00 sec)
mysql> TABLE b EXCEPT TABLE c;
+------+------+
| m | n |
+------+------+
| 1 | 2 |
```

```
+------+------+
1 row in set (0.00 sec)
```

As with [UNION](#page-111-0) and [INTERSECT](#page-46-0), if neither DISTINCT nor ALL is specified, the default is DISTINCT.

DISTINCT removes duplicates found on either side of the relation, as shown here:

```
mysql> TABLE c EXCEPT DISTINCT TABLE a;
+------+------+
| m | n |
+------+------+
| 1 | 3 |
+------+------+
1 row in set (0.00 sec)
mysql> TABLE c EXCEPT ALL TABLE a;
+------+------+
| m | n |
+------+------+
| 1 | 3 |
| 1 | 3 |
+------+------+
2 rows in set (0.00 sec)
```

(The first statement has the same effect as TABLE c EXCEPT TABLE a.)

Unlike UNION or INTERSECT, EXCEPT is not commutative—that is, the result depends on the order of the operands, as shown here:

```
mysql> TABLE a EXCEPT TABLE c;
+------+------+
| m | n |
+------+------+
| 1 | 2 |
| 2 | 3 |
+------+------+
2 rows in set (0.00 sec)
mysql> TABLE c EXCEPT TABLE a;
+------+------+
| m | n |
+------+------+
| 1 | 3 |
+------+------+
1 row in set (0.00 sec)
```

As with UNION, the result sets to be compared must have the same number of columns. Result set column types are also determined as for UNION.

# <span id="page-32-0"></span>**15.2.5 HANDLER Statement**

```
HANDLER tbl_name OPEN [ [AS] alias]
HANDLER tbl_name READ index_name { = | <= | >= | < | > } (value1,value2,...)
 [ WHERE where_condition ] [LIMIT ... ]
HANDLER tbl_name READ index_name { FIRST | NEXT | PREV | LAST }
 [ WHERE where_condition ] [LIMIT ... ]
HANDLER tbl_name READ { FIRST | NEXT }
 [ WHERE where_condition ] [LIMIT ... ]
HANDLER tbl_name CLOSE
```

The HANDLER statement provides direct access to table storage engine interfaces. It is available for InnoDB and MyISAM tables.

The HANDLER ... OPEN statement opens a table, making it accessible using subsequent HANDLER ... READ statements. This table object is not shared by other sessions and is not closed until the session calls HANDLER ... CLOSE or the session terminates.

If you open the table using an alias, further references to the open table with other HANDLER statements must use the alias rather than the table name. If you do not use an alias, but open the table using a table name qualified by the database name, further references must use the unqualified table name. For example, for a table opened using mydb.mytable, further references must use mytable.

The first HANDLER ... READ syntax fetches a row where the index specified satisfies the given values and the WHERE condition is met. If you have a multiple-column index, specify the index column values as a comma-separated list. Either specify values for all the columns in the index, or specify values for a leftmost prefix of the index columns. Suppose that an index my\_idx includes three columns named col\_a, col\_b, and col\_c, in that order. The HANDLER statement can specify values for all three columns in the index, or for the columns in a leftmost prefix. For example:

```
HANDLER ... READ my_idx = (col_a_val,col_b_val,col_c_val) ...
HANDLER ... READ my_idx = (col_a_val,col_b_val) ...
HANDLER ... READ my_idx = (col_a_val) ...
```

To employ the HANDLER interface to refer to a table's PRIMARY KEY, use the quoted identifier `PRIMARY`:

```
HANDLER tbl_name READ `PRIMARY` ...
```

The second HANDLER ... READ syntax fetches a row from the table in index order that matches the WHERE condition.

The third HANDLER ... READ syntax fetches a row from the table in natural row order that matches the WHERE condition. It is faster than HANDLER tbl\_name READ index\_name when a full table scan is desired. Natural row order is the order in which rows are stored in a MyISAM table data file. This statement works for InnoDB tables as well, but there is no such concept because there is no separate data file.

Without a LIMIT clause, all forms of HANDLER ... READ fetch a single row if one is available. To return a specific number of rows, include a LIMIT clause. It has the same syntax as for the [SELECT](#page-70-0) statement. See [Section 15.2.13, "SELECT Statement"](#page-70-0).

HANDLER ... CLOSE closes a table that was opened with HANDLER ... OPEN.

There are several reasons to use the HANDLER interface instead of normal [SELECT](#page-70-0) statements:

- HANDLER is faster than [SELECT](#page-70-0):
  - A designated storage engine handler object is allocated for the HANDLER ... OPEN. The object is reused for subsequent HANDLER statements for that table; it need not be reinitialized for each one.
  - There is less parsing involved.
  - There is no optimizer or query-checking overhead.
  - The handler interface does not have to provide a consistent look of the data (for example, dirty reads are permitted), so the storage engine can use optimizations that [SELECT](#page-70-0) does not normally permit.
- HANDLER makes it easier to port to MySQL applications that use a low-level ISAM-like interface.
- HANDLER enables you to traverse a database in a manner that is difficult (or even impossible) to accomplish with [SELECT](#page-70-0). The HANDLER interface is a more natural way to look at data when working with applications that provide an interactive user interface to the database.

HANDLER is a somewhat low-level statement. For example, it does not provide consistency. That is, HANDLER ... OPEN does not take a snapshot of the table, and does not lock the table. This means that after a HANDLER ... OPEN statement is issued, table data can be modified (by the current session or other sessions) and these modifications might be only partially visible to HANDLER ... NEXT or HANDLER ... PREV scans.

An open handler can be closed and marked for reopen, in which case the handler loses its position in the table. This occurs when both of the following circumstances are true:

- Any session executes FLUSH TABLES or DDL statements on the handler's table.
- The session in which the handler is open executes non-HANDLER statements that use tables.

[TRUNCATE TABLE](#page-24-0) for a table closes all handlers for the table that were opened with [HANDLER OPEN](#page-32-0).

If a table is flushed with FLUSH TABLES tbl\_name WITH READ LOCK was opened with HANDLER, the handler is implicitly flushed and loses its position.

# <span id="page-34-0"></span>**15.2.6 IMPORT TABLE Statement**

```
IMPORT TABLE FROM sdi_file [, sdi_file] ...
```

The [IMPORT TABLE](#page-34-0) statement imports MyISAM tables based on information contained in .sdi (serialized dictionary information) metadata files. [IMPORT TABLE](#page-34-0) requires the FILE privilege to read the .sdi and table content files, and the CREATE privilege for the table to be created.

Tables can be exported from one server using mysqldump to write a file of SQL statements and imported into another server using mysql to process the dump file. [IMPORT TABLE](#page-34-0) provides a faster alternative using the "raw" table files.

Prior to import, the files that provide the table content must be placed in the appropriate schema directory for the import server, and the .sdi file must be located in a directory accessible to the server. For example, the .sdi file can be placed in the directory named by the secure\_file\_priv system variable, or (if secure\_file\_priv is empty) in a directory under the server data directory.

The following example describes how to export MyISAM tables named employees and managers from the hr schema of one server and import them into the hr schema of another server. The example uses these assumptions (to perform a similar operation on your own system, modify the path names as appropriate):

- For the export server, export\_basedir represents its base directory, and its data directory is export\_basedir/data.
- For the import server, import\_basedir represents its base directory, and its data directory is import\_basedir/data.
- Table files are exported from the export server into the /tmp/export directory and this directory is secure (not accessible to other users).
- The import server uses /tmp/mysql-files as the directory named by its secure\_file\_priv system variable.

To export tables from the export server, use this procedure:

1. Ensure a consistent snapshot by executing this statement to lock the tables so that they cannot be modified during export:

```
mysql> FLUSH TABLES hr.employees, hr.managers WITH READ LOCK;
```

While the lock is in effect, the tables can still be used, but only for read access.

- 2. At the file system level, copy the .sdi and table content files from the hr schema directory to the secure export directory:
  - The .sdi file is located in the hr schema directory, but might not have exactly the same basename as the table name. For example, the .sdi files for the employees and managers tables might be named employees\_125.sdi and managers\_238.sdi.

• For a MyISAM table, the content files are its .MYD data file and .MYI index file.

Given those file names, the copy commands look like this:

```
$> cd export_basedir/data/hr
$> cp employees_125.sdi /tmp/export
$> cp managers_238.sdi /tmp/export
$> cp employees.{MYD,MYI} /tmp/export
$> cp managers.{MYD,MYI} /tmp/export
```

3. Unlock the tables:

```
mysql> UNLOCK TABLES;
```

To import tables into the import server, use this procedure:

1. The import schema must exist. If necessary, execute this statement to create it:

```
mysql> CREATE SCHEMA hr;
```

2. At the file system level, copy the .sdi files to the import server secure\_file\_priv directory, / tmp/mysql-files. Also, copy the table content files to the hr schema directory:

```
$> cd /tmp/export
$> cp employees_125.sdi /tmp/mysql-files
$> cp managers_238.sdi /tmp/mysql-files
$> cp employees.{MYD,MYI} import_basedir/data/hr
$> cp managers.{MYD,MYI} import_basedir/data/hr
```

3. Import the tables by executing an [IMPORT TABLE](#page-34-0) statement that names the .sdi files:

```
mysql> IMPORT TABLE FROM
 '/tmp/mysql-files/employees.sdi',
 '/tmp/mysql-files/managers.sdi';
```

The .sdi file need not be placed in the import server directory named by the secure\_file\_priv system variable if that variable is empty; it can be in any directory accessible to the server, including the schema directory for the imported table. If the .sdi file is placed in that directory, however, it may be rewritten; the import operation creates a new .sdi file for the table, which overwrites the old .sdi file if the operation uses the same file name for the new file.

Each sdi\_file value must be a string literal that names the .sdi file for a table or is a pattern that matches .sdi files. If the string is a pattern, any leading directory path and the .sdi file name suffix must be given literally. Pattern characters are permitted only in the base name part of the file name:

- ? matches any single character
- \* matches any sequence of characters, including no characters

Using a pattern, the previous [IMPORT TABLE](#page-34-0) statement could have been written like this (assuming that the /tmp/mysql-files directory contains no other .sdi files matching the pattern):

```
IMPORT TABLE FROM '/tmp/mysql-files/*.sdi';
```

To interpret the location of .sdi file path names, the server uses the same rules for [IMPORT TABLE](#page-34-0) as the server-side rules for [LOAD DATA](#page-47-0) (that is, the non-LOCAL rules). See [Section 15.2.9, "LOAD](#page-47-0) [DATA Statement"](#page-47-0), paying particular attention to the rules used to interpret relative path names.

[IMPORT TABLE](#page-34-0) fails if the .sdi or table files cannot be located. After importing a table, the server attempts to open it and reports as warnings any problems detected. To attempt a repair to correct any reported issues, use REPAIR TABLE.

[IMPORT TABLE](#page-34-0) is not written to the binary log.

# **Restrictions and Limitations**

[IMPORT TABLE](#page-34-0) applies only to non-TEMPORARY MyISAM tables. It does not apply to tables created with a transactional storage engine, tables created with CREATE TEMPORARY TABLE, or views.

An .sdi file used in an import operation must be generated on a server with the same data dictionary version and sdi version as the import server. The version information of the generating server is found in the .sdi file:

```
{
 "mysqld_version_id":80019,
 "dd_version":80017,
 "sdi_version":80016,
 ...
}
```

To determine the data dictionary and sdi version of the import server, you can check the .sdi file of a recently created table on the import server.

The table data and index files must be placed in the schema directory for the import server prior to the import operation, unless the table as defined on the export server uses the DATA DIRECTORY or INDEX DIRECTORY table options. In that case, modify the import procedure using one of these alternatives before executing the [IMPORT TABLE](#page-34-0) statement:

- Put the data and index files into the same directory on the import server host as on the export server host, and create symlinks in the import server schema directory to those files.
- Put the data and index files into an import server host directory different from that on the export server host, and create symlinks in the import server schema directory to those files. In addition, modify the .sdi file to reflect the different file locations.
- Put the data and index files into the schema directory on the import server host, and modify the .sdi file to remove the data and index directory table options.

Any collation IDs stored in the .sdi file must refer to the same collations on the export and import servers.

Trigger information for a table is not serialized into the table .sdi file, so triggers are not restored by the import operation.

Some edits to an .sdi file are permissible prior to executing the [IMPORT TABLE](#page-34-0) statement, whereas others are problematic or may even cause the import operation to fail:

- Changing the data directory and index directory table options is required if the locations of the data and index files differ between the export and import servers.
- Changing the schema name is required to import the table into a different schema on the import server than on the export server.
- Changing schema and table names may be required to accommodate differences between file system case-sensitivity semantics on the export and import servers or differences in lower\_case\_table\_names settings. Changing the table names in the .sdi file may require renaming the table files as well.
- In some cases, changes to column definitions are permitted. Changing data types is likely to cause problems.

# <span id="page-36-0"></span>**15.2.7 INSERT Statement**

```
INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
```

```
 { {VALUES | VALUE} (value_list) [, (value_list)] ... }
 [AS row_alias[(col_alias [, col_alias] ...)]]
 [ON DUPLICATE KEY UPDATE assignment_list]
INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 SET assignment_list
 [AS row_alias[(col_alias [, col_alias] ...)]]
 [ON DUPLICATE KEY UPDATE assignment_list]
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 { SELECT ... 
 | TABLE table_name
 | VALUES row_constructor_list
 }
 [ON DUPLICATE KEY UPDATE assignment_list]
value:
 {expr | DEFAULT}
value_list:
 value [, value] ...
row_constructor_list:
 ROW(value_list)[, ROW(value_list)][, ...]
assignment:
 col_name = 
 value
 | [row_alias.]col_name
 | [tbl_name.]col_name
 | [row_alias.]col_alias
assignment_list:
 assignment [, assignment] ...
```

[INSERT](#page-36-0) inserts new rows into an existing table. The [INSERT ... VALUES](#page-36-0), [INSERT ... VALUES](#page-112-0) [ROW\(\)](#page-112-0), and [INSERT ... SET](#page-36-0) forms of the statement insert rows based on explicitly specified values. The [INSERT ... SELECT](#page-41-0) form inserts rows selected from another table or tables. You can also use [INSERT ... TABLE](#page-105-0) to insert rows from a single table. [INSERT](#page-36-0) with an ON DUPLICATE KEY UPDATE clause enables existing rows to be updated if a row to be inserted would cause a duplicate value in a UNIQUE index or PRIMARY KEY. A row alias with one or more optional column aliases can be used with ON DUPLICATE KEY UPDATE to refer to the row to be inserted.

For additional information about [INSERT ... SELECT](#page-41-0) and [INSERT ... ON DUPLICATE KEY](#page-42-0) [UPDATE](#page-42-0), see [Section 15.2.7.1, "INSERT ... SELECT Statement",](#page-41-0) and [Section 15.2.7.2, "INSERT ... ON](#page-42-0) [DUPLICATE KEY UPDATE Statement".](#page-42-0)

In MySQL 8.4, the DELAYED keyword is accepted but ignored by the server. For the reasons for this, see [Section 15.2.7.3, "INSERT DELAYED Statement",](#page-46-1)

Inserting into a table requires the INSERT privilege for the table. If the ON DUPLICATE KEY UPDATE clause is used and a duplicate key causes an [UPDATE](#page-108-0) to be performed instead, the statement requires the UPDATE privilege for the columns to be updated. For columns that are read but not modified you need only the SELECT privilege (such as for a column referenced only on the right hand side of an col\_name=expr assignment in an ON DUPLICATE KEY UPDATE clause).

When inserting into a partitioned table, you can control which partitions and subpartitions accept new rows. The PARTITION clause takes a list of the comma-separated names of one or more partitions or subpartitions (or both) of the table. If any of the rows to be inserted by a given [INSERT](#page-36-0) statement do not match one of the partitions listed, the [INSERT](#page-36-0) statement fails with the error Found a row not matching the given partition set. For more information and examples, see Section 26.5, "Partition Selection".

tbl\_name is the table into which rows should be inserted. Specify the columns for which the statement provides values as follows:

- Provide a parenthesized list of comma-separated column names following the table name. In this case, a value for each named column must be provided by the VALUES list, [VALUES ROW\(\)](#page-112-0) list, or [SELECT](#page-70-0) statement. For the INSERT TABLE form, the number of columns in the source table must match the number of columns to be inserted.
- If you do not specify a list of column names for [INSERT ... VALUES](#page-36-0) or [INSERT ... SELECT](#page-41-0), values for every column in the table must be provided by the VALUES list, [SELECT](#page-70-0) statement, or [TABLE](#page-105-0) statement. If you do not know the order of the columns in the table, use DESCRIBE tbl\_name to find out.
- A SET clause indicates columns explicitly by name, together with the value to assign each one.

Column values can be given in several ways:

• If strict SQL mode is not enabled, any column not explicitly given a value is set to its default (explicit or implicit) value. For example, if you specify a column list that does not name all the columns in the table, unnamed columns are set to their default values. Default value assignment is described in Section 13.6, "Data Type Default Values".

If strict SQL mode is enabled, an [INSERT](#page-36-0) statement generates an error if it does not specify an explicit value for every column that has no default value. See Section 7.1.11, "Server SQL Modes".

• If both the column list and the VALUES list are empty, [INSERT](#page-36-0) creates a row with each column set to its default value:

```
INSERT INTO tbl_name () VALUES();
```

If strict mode is not enabled, MySQL uses the implicit default value for any column that has no explicitly defined default. If strict mode is enabled, an error occurs if any column has no default value.

- Use the keyword DEFAULT to set a column explicitly to its default value. This makes it easier to write [INSERT](#page-36-0) statements that assign values to all but a few columns, because it enables you to avoid writing an incomplete VALUES list that does not include a value for each column in the table. Otherwise, you must provide the list of column names corresponding to each value in the VALUES list.
- If a generated column is inserted into explicitly, the only permitted value is DEFAULT. For information about generated columns, see Section 15.1.20.8, "CREATE TABLE and Generated Columns".
- In expressions, you can use DEFAULT(col\_name) to produce the default value for column col\_name.
- Type conversion of an expression expr that provides a column value might occur if the expression data type does not match the column data type. Conversion of a given value can result in different inserted values depending on the column type. For example, inserting the string '1999.0e-2' into an INT, FLOAT, DECIMAL(10,6), or YEAR column inserts the value 1999, 19.9921, 19.992100, or 1999, respectively. The value stored in the INT and YEAR columns is 1999 because the string-tonumber conversion looks only at as much of the initial part of the string as may be considered a valid integer or year. For the FLOAT and DECIMAL columns, the string-to-number conversion considers the entire string a valid numeric value.
- An expression expr can refer to any column that was set earlier in a value list. For example, you can do this because the value for col2 refers to col1, which has previously been assigned:

```
INSERT INTO tbl_name (col1,col2) VALUES(15,col1*2);
```

But the following is not legal, because the value for col1 refers to col2, which is assigned after col1:

```
INSERT INTO tbl_name (col1,col2) VALUES(col2*2,15);
```

An exception occurs for columns that contain AUTO\_INCREMENT values. Because AUTO\_INCREMENT values are generated after other value assignments, any reference to an AUTO\_INCREMENT column in the assignment returns a 0.

[INSERT](#page-36-0) statements that use VALUES syntax can insert multiple rows. To do this, include multiple lists of comma-separated column values, with lists enclosed within parentheses and separated by commas. Example:

```
INSERT INTO tbl_name (a,b,c)
 VALUES(1,2,3), (4,5,6), (7,8,9);
```

Each values list must contain exactly as many values as are to be inserted per row. The following statement is invalid because it contains one list of nine values, rather than three lists of three values each:

```
INSERT INTO tbl_name (a,b,c) VALUES(1,2,3,4,5,6,7,8,9);
```

VALUE is a synonym for VALUES in this context. Neither implies anything about the number of values lists, nor about the number of values per list. Either may be used whether there is a single values list or multiple lists, and regardless of the number of values per list.

[INSERT](#page-36-0) statements using [VALUES ROW\(\)](#page-112-0) syntax can also insert multiple rows. In this case, each value list must be contained within a ROW() (row constructor), like this:

```
INSERT INTO tbl_name (a,b,c)
 VALUES ROW(1,2,3), ROW(4,5,6), ROW(7,8,9);
```

The affected-rows value for an [INSERT](#page-36-0) can be obtained using the ROW\_COUNT() SQL function or the [mysql\\_affected\\_rows\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-affected-rows.md) C API function. See Section 14.15, "Information Functions", and [mysql\\_affected\\_rows\(\).](https://dev.mysql.com/doc/c-api/8.4/en/mysql-affected-rows.md)

If you use [INSERT ... VALUES](#page-36-0) or INSERT ... VALUES ROW() with multiple value lists, or [INSERT ... SELECT](#page-41-0) or INSERT ... TABLE, the statement returns an information string in this format:

```
Records: N1 Duplicates: N2 Warnings: N3
```

If you are using the C API, the information string can be obtained by invoking the [mysql\\_info\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md) function. See [mysql\\_info\(\).](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md)

Records indicates the number of rows processed by the statement. (This is not necessarily the number of rows actually inserted because Duplicates can be nonzero.) Duplicates indicates the number of rows that could not be inserted because they would duplicate some existing unique index value. Warnings indicates the number of attempts to insert column values that were problematic in some way. Warnings can occur under any of the following conditions:

- Inserting NULL into a column that has been declared NOT NULL. For multiple-row [INSERT](#page-36-0) statements or [INSERT INTO ... SELECT](#page-41-0) statements, the column is set to the implicit default value for the column data type. This is 0 for numeric types, the empty string ('') for string types, and the "zero" value for date and time types. [INSERT INTO ... SELECT](#page-41-0) statements are handled the same way as multiple-row inserts because the server does not examine the result set from the [SELECT](#page-70-0) to see whether it returns a single row. (For a single-row [INSERT](#page-36-0), no warning occurs when NULL is inserted into a NOT NULL column. Instead, the statement fails with an error.)
- Setting a numeric column to a value that lies outside the column range. The value is clipped to the closest endpoint of the range.
- Assigning a value such as '10.34 a' to a numeric column. The trailing nonnumeric text is stripped off and the remaining numeric part is inserted. If the string value has no leading numeric part, the column is set to 0.

- Inserting a string into a string column (CHAR, VARCHAR, TEXT, or BLOB) that exceeds the column maximum length. The value is truncated to the column maximum length.
- Inserting a value into a date or time column that is illegal for the data type. The column is set to the appropriate zero value for the type.
- For [INSERT](#page-36-0) examples involving AUTO\_INCREMENT column values, see Section 5.6.9, "Using AUTO\_INCREMENT".

If [INSERT](#page-36-0) inserts a row into a table that has an AUTO\_INCREMENT column, you can find the value used for that column by using the LAST\_INSERT\_ID() SQL function or the [mysql\\_insert\\_id\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-insert-id.md) C API function.

![](_page_40_Picture_5.jpeg)

#### **Note**

These two functions do not always behave identically. The behavior of [INSERT](#page-36-0) statements with respect to AUTO\_INCREMENT columns is discussed further in Section 14.15, "Information Functions", and [mysql\\_insert\\_id\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-insert-id.md).

The [INSERT](#page-36-0) statement supports the following modifiers:

• If you use the LOW\_PRIORITY modifier, execution of the [INSERT](#page-36-0) is delayed until no other clients are reading from the table. This includes other clients that began reading while existing clients are reading, and while the INSERT LOW\_PRIORITY statement is waiting. It is possible, therefore, for a client that issues an INSERT LOW\_PRIORITY statement to wait for a very long time.

LOW\_PRIORITY affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE).

![](_page_40_Picture_11.jpeg)

#### **Note**

LOW\_PRIORITY should normally not be used with MyISAM tables because doing so disables concurrent inserts. See Section 10.11.3, "Concurrent Inserts".

• If you specify HIGH\_PRIORITY, it overrides the effect of the --low-priority-updates option if the server was started with that option. It also causes concurrent inserts not to be used. See Section 10.11.3, "Concurrent Inserts".

HIGH\_PRIORITY affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE).

• If you use the IGNORE modifier, ignorable errors that occur while executing the [INSERT](#page-36-0) statement are ignored. For example, without IGNORE, a row that duplicates an existing UNIQUE index or PRIMARY KEY value in the table causes a duplicate-key error and the statement is aborted. With IGNORE, the row is discarded and no error occurs. Ignored errors generate warnings instead.

IGNORE has a similar effect on inserts into partitioned tables where no partition matching a given value is found. Without IGNORE, such [INSERT](#page-36-0) statements are aborted with an error. When [INSERT](#page-36-0) [IGNORE](#page-36-0) is used, the insert operation fails silently for rows containing the unmatched value, but inserts rows that are matched. For an example, see Section 26.2.2, "LIST Partitioning".

Data conversions that would trigger errors abort the statement if IGNORE is not specified. With IGNORE, invalid values are adjusted to the closest values and inserted; warnings are produced but the statement does not abort. You can determine with the [mysql\\_info\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md) C API function how many rows were actually inserted into the table.

For more information, see The Effect of IGNORE on Statement Execution.

You can use [REPLACE](#page-67-0) instead of [INSERT](#page-36-0) to overwrite old rows. [REPLACE](#page-67-0) is the counterpart to [INSERT IGNORE](#page-36-0) in the treatment of new rows that contain unique key values that duplicate old rows: The new rows replace the old rows rather than being discarded. See [Section 15.2.12,](#page-67-0) ["REPLACE Statement".](#page-67-0)

- If you specify ON DUPLICATE KEY UPDATE, and a row is inserted that would cause a duplicate value in a UNIQUE index or PRIMARY KEY, an [UPDATE](#page-108-0) of the old row occurs. The affected-rows value per row is 1 if the row is inserted as a new row, 2 if an existing row is updated, and 0 if an existing row is set to its current values. If you specify the CLIENT\_FOUND\_ROWS flag to the [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-connect.md) C API function when connecting to mysqld, the affected-rows value is 1 (not 0) if an existing row is set to its current values. See [Section 15.2.7.2, "INSERT ... ON](#page-42-0) [DUPLICATE KEY UPDATE Statement".](#page-42-0)
- [INSERT DELAYED](#page-46-1) was deprecated in MySQL 5.6, and is scheduled for eventual removal. In MySQL 8.4, the DELAYED modifier is accepted but ignored. Use INSERT (without DELAYED) instead. See [Section 15.2.7.3, "INSERT DELAYED Statement".](#page-46-1)

# <span id="page-41-0"></span>**15.2.7.1 INSERT ... SELECT Statement**

```
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 { SELECT ... 
 | TABLE table_name
 | VALUES row_constructor_list
 }
 [ON DUPLICATE KEY UPDATE assignment_list]
value:
 {expr | DEFAULT}
value_list:
 value [, value] ...
row_constructor_list:
 ROW(value_list)[, ROW(value_list)][, ...]
assignment:
 col_name = 
 value
 | [row_alias.]col_name
 | [tbl_name.]col_name
 | [row_alias.]col_alias
assignment_list:
 assignment [, assignment] ...
```

With [INSERT ... SELECT](#page-41-0), you can quickly insert many rows into a table from the result of a [SELECT](#page-70-0) statement, which can select from one or many tables. For example:

```
INSERT INTO tbl_temp2 (fld_id)
 SELECT tbl_temp1.fld_order_id
 FROM tbl_temp1 WHERE tbl_temp1.fld_order_id > 100;
```

[TABLE](#page-105-0) statement in place of [SELECT](#page-70-0), as shown here:

```
INSERT INTO ta TABLE tb;
```

TABLE tb is equivalent to SELECT \* FROM tb. It can be useful when inserting all columns from the source table into the target table, and no filtering with WHERE is required. In addition, the rows from [TABLE](#page-105-0) can be ordered by one or more columns using ORDER BY, and the number of rows inserted can be limited using a LIMIT clause. For more information, see [Section 15.2.16, "TABLE Statement".](#page-105-0)

The following conditions hold for [INSERT ... SELECT](#page-41-0) statements, and, except where noted, for INSERT ... TABLE as well:

• Specify IGNORE to ignore rows that would cause duplicate-key violations.

• The target table of the [INSERT](#page-36-0) statement may appear in the FROM clause of the [SELECT](#page-70-0) part of the query, or as the table named by [TABLE](#page-105-0). However, you cannot insert into a table and select from the same table in a subquery.

When selecting from and inserting into the same table, MySQL creates an internal temporary table to hold the rows from the [SELECT](#page-70-0) and then inserts those rows into the target table. However, you cannot use INSERT INTO t ... SELECT ... FROM t when t is a TEMPORARY table, because TEMPORARY tables cannot be referred to twice in the same statement. For the same reason, you cannot use INSERT INTO t ... TABLE t when t is a temporary table. See Section 10.4.4, "Internal Temporary Table Use in MySQL", and Section B.3.6.2, "TEMPORARY Table Problems".

- AUTO\_INCREMENT columns work as usual.
- To ensure that the binary log can be used to re-create the original tables, MySQL does not permit concurrent inserts for [INSERT ... SELECT](#page-41-0) or INSERT ... TABLE statements (see Section 10.11.3, "Concurrent Inserts").
- To avoid ambiguous column reference problems when the [SELECT](#page-70-0) and the [INSERT](#page-36-0) refer to the same table, provide a unique alias for each table used in the [SELECT](#page-70-0) part, and qualify column names in that part with the appropriate alias.

The [TABLE](#page-105-0) statement does not support aliases.

You can explicitly select which partitions or subpartitions (or both) of the source or target table (or both) are to be used with a PARTITION clause following the name of the table. When PARTITION is used with the name of the source table in the [SELECT](#page-70-0) portion of the statement, rows are selected only from the partitions or subpartitions named in its partition list. When PARTITION is used with the name of the target table for the [INSERT](#page-36-0) portion of the statement, it must be possible to insert all rows selected into the partitions or subpartitions named in the partition list following the option. Otherwise, the INSERT ... SELECT statement fails. For more information and examples, see Section 26.5, "Partition Selection".

[TABLE](#page-105-0) does not support a PARTITION clause.

For [INSERT ... SELECT](#page-42-0) statements, see [Section 15.2.7.2, "INSERT ... ON DUPLICATE KEY](#page-42-0) [UPDATE Statement"](#page-42-0) for conditions under which the [SELECT](#page-70-0) columns can be referred to in an ON DUPLICATE KEY UPDATE clause. This also works for INSERT ... TABLE.

The order in which a [SELECT](#page-70-0) or [TABLE](#page-105-0) statement with no ORDER BY clause returns rows is nondeterministic. This means that, when using replication, there is no guarantee that such a [SELECT](#page-70-0) returns rows in the same order on the source and the replica, which can lead to inconsistencies between them. To prevent this from occurring, always write INSERT ... SELECT or INSERT ... TABLE statements that are to be replicated using an ORDER BY clause that produces the same row order on the source and the replica. See also Section 19.5.1.18, "Replication and LIMIT".

Due to this issue, [INSERT ... SELECT ON DUPLICATE KEY UPDATE](#page-42-0) and [INSERT IGNORE ...](#page-41-0) [SELECT](#page-41-0) statements are flagged as unsafe for statement-based replication. Such statements produce a warning in the error log when using statement-based mode and are written to the binary log using the row-based format when using MIXED mode. (Bug #11758262, Bug #50439)

See also Section 19.2.1.1, "Advantages and Disadvantages of Statement-Based and Row-Based Replication".

## <span id="page-42-0"></span>**15.2.7.2 INSERT ... ON DUPLICATE KEY UPDATE Statement**

If you specify an ON DUPLICATE KEY UPDATE clause and a row to be inserted would cause a duplicate value in a UNIQUE index or PRIMARY KEY, an [UPDATE](#page-108-0) of the old row occurs. For example, if column a is declared as UNIQUE and contains the value 1, the following two statements have similar effect:

INSERT INTO t1 (a,b,c) VALUES (1,2,3)

```
 ON DUPLICATE KEY UPDATE c=c+1;
UPDATE t1 SET c=c+1 WHERE a=1;
```

The effects are not quite identical: For an InnoDB table where a is an auto-increment column, the INSERT statement increases the auto-increment value but the UPDATE does not.

If column b is also unique, the [INSERT](#page-36-0) is equivalent to this [UPDATE](#page-108-0) statement instead:

```
UPDATE t1 SET c=c+1 WHERE a=1 OR b=2 LIMIT 1;
```

If a=1 OR b=2 matches several rows, only one row is updated. In general, you should try to avoid using an ON DUPLICATE KEY UPDATE clause on tables with multiple unique indexes.

With ON DUPLICATE KEY UPDATE, the affected-rows value per row is 1 if the row is inserted as a new row, 2 if an existing row is updated, and 0 if an existing row is set to its current values. If you specify the CLIENT\_FOUND\_ROWS flag to the [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-connect.md) C API function when connecting to mysqld, the affected-rows value is 1 (not 0) if an existing row is set to its current values.

If a table contains an AUTO\_INCREMENT column and [INSERT ... ON DUPLICATE KEY UPDATE](#page-42-0) inserts or updates a row, the LAST\_INSERT\_ID() function returns the AUTO\_INCREMENT value.

The ON DUPLICATE KEY UPDATE clause can contain multiple column assignments, separated by commas.

It is possible to use IGNORE with ON DUPLICATE KEY UPDATE in an INSERT statement, but this may not behave as you expect when inserting multiple rows into a table that has multiple unique keys. This becomes apparent when an updated value is itself a duplicate key value. Consider the table t, created and populated by the statements shown here:

```
mysql> CREATE TABLE t (a SERIAL, b BIGINT NOT NULL, UNIQUE KEY (b));;
Query OK, 0 rows affected (0.03 sec)
mysql> INSERT INTO t VALUES ROW(1,1), ROW(2,2);
Query OK, 2 rows affected (0.01 sec)
Records: 2 Duplicates: 0 Warnings: 0
mysql> TABLE t;
+---+---+
| a | b |
+---+---+
| 1 | 1 |
| 2 | 2 |
+---+---+
2 rows in set (0.00 sec)
```

Now we attempt to insert two rows, one of which contains a duplicate key value, using ON DUPLICATE KEY UPDATE, where the UPDATE clause itself results in a duplicate key value:

```
mysql> INSERT INTO t VALUES ROW(2,3), ROW(3,3) ON DUPLICATE KEY UPDATE a=a+1, b=b-1;
ERROR 1062 (23000): Duplicate entry '1' for key 't.b'
mysql> TABLE t;
+---+---+
| a | b |
+---+---+
| 1 | 1 |
| 2 | 2 |
+---+---+
2 rows in set (0.00 sec)
```

The first row contains a duplicate value for one of the table's unique keys (column a), but b=b+1 in the UPDATE clause results in a unique key violation for column b; the statement is immediately rejected with an error, and no rows are updated. Let us repeat the statement, this time adding the **IGNORE** keyword, like this:

```
mysql> INSERT IGNORE INTO t VALUES ROW(2,3), ROW(3,3)
 -> ON DUPLICATE KEY UPDATE a=a+1, b=b-1;
```

```
Query OK, 1 row affected, 1 warning (0.00 sec)
Records: 2 Duplicates: 1 Warnings: 1
```

This time, the previous error is demoted to a warning, as shown here:

```
mysql> SHOW WARNINGS;
+---------+------+-----------------------------------+
| Level | Code | Message |
+---------+------+-----------------------------------+
| Warning | 1062 | Duplicate entry '1' for key 't.b' |
+---------+------+-----------------------------------+
1 row in set (0.00 sec)
```

Because the statement was not rejected, execution continues. This means that the second row is inserted into t, as we can see here:

```
mysql> TABLE t;
+---+---+
| a | b |
+---+---+
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
+---+---+
3 rows in set (0.00 sec)
```

In assignment value expressions in the ON DUPLICATE KEY UPDATE clause, you can use the VALUES(col\_name) function to refer to column values from the [INSERT](#page-36-0) portion of the [INSERT ...](#page-42-0) [ON DUPLICATE KEY UPDATE](#page-42-0) statement. In other words, VALUES(col\_name) in the ON DUPLICATE KEY UPDATE clause refers to the value of col\_name that would be inserted, had no duplicate-key conflict occurred. This function is especially useful in multiple-row inserts. The VALUES() function is meaningful only as an introducer for INSERT statement value lists, or in the ON DUPLICATE KEY UPDATE clause of an [INSERT](#page-36-0) statement, and returns NULL otherwise. For example:

```
INSERT INTO t1 (a,b,c) VALUES (1,2,3),(4,5,6)
 ON DUPLICATE KEY UPDATE c=VALUES(a)+VALUES(b);
```

That statement is identical to the following two statements:

```
INSERT INTO t1 (a,b,c) VALUES (1,2,3)
 ON DUPLICATE KEY UPDATE c=3;
INSERT INTO t1 (a,b,c) VALUES (4,5,6)
 ON DUPLICATE KEY UPDATE c=9;
```

![](_page_44_Picture_10.jpeg)

## **Note**

The use of VALUES() to refer to the new row and columns is deprecated, and subject to removal in a future version of MySQL. Instead, use row and column aliases, as described in the next few paragraphs of this section.

It is possible to use an alias for the row, with, optionally, one or more of its columns to be inserted, following the VALUES or SET clause, and preceded by the AS keyword. Using the row alias new, the statement shown previously using VALUES() to access the new column values can be written in the form shown here:

```
INSERT INTO t1 (a,b,c) VALUES (1,2,3),(4,5,6) AS new
 ON DUPLICATE KEY UPDATE c = new.a+new.b;
```

If, in addition, you use the column aliases m, n, and p, you can omit the row alias in the assignment clause and write the same statement like this:

```
INSERT INTO t1 (a,b,c) VALUES (1,2,3),(4,5,6) AS new(m,n,p)
 ON DUPLICATE KEY UPDATE c = m+n;
```

When using column aliases in this fashion, you must still use a row alias following the VALUES clause, even if you do not make direct use of it in the assignment clause.

An INSERT ... SELECT ... ON DUPLICATE KEY UPDATE statement that uses VALUES() in the UPDATE clause, like this one, throws a warning:

```
INSERT INTO t1
 SELECT c, c+d FROM t2
 ON DUPLICATE KEY UPDATE b = VALUES(b);
```

You can eliminate such warnings by using a subquery instead, like this:

```
INSERT INTO t1
 SELECT * FROM (SELECT c, c+d AS e FROM t2) AS dt
 ON DUPLICATE KEY UPDATE b = e;
```

You can also use row and column aliases with a SET clause, as mentioned previously. Employing SET instead of VALUES in the two INSERT ... ON DUPLICATE KEY UPDATE statements just shown can be done as shown here:

```
INSERT INTO t1 SET a=1,b=2,c=3 AS new
 ON DUPLICATE KEY UPDATE c = new.a+new.b;
INSERT INTO t1 SET a=1,b=2,c=3 AS new(m,n,p)
 ON DUPLICATE KEY UPDATE c = m+n;
```

The row alias must not be the same as the name of the table. If column aliases are not used, or if they are the same as the column names, they must be distinguished using the row alias in the ON DUPLICATE KEY UPDATE clause. Column aliases must be unique with regard to the row alias to which they apply (that is, no column aliases referring to columns of the same row may be the same).

For [INSERT ... SELECT](#page-42-0) statements, these rules apply regarding acceptable forms of SELECT query expressions that you can refer to in an ON DUPLICATE KEY UPDATE clause:

- References to columns from queries on a single table, which may be a derived table.
- References to columns from queries on a join over multiple tables.
- References to columns from DISTINCT queries.
- References to columns in other tables, as long as the [SELECT](#page-70-0) does not use GROUP BY. One side effect is that you must qualify references to nonunique column names.

References to columns from a [UNION](#page-111-0) are not supported. To work around this restriction, rewrite the [UNION](#page-111-0) as a derived table so that its rows can be treated as a single-table result set. For example, this statement produces an error:

```
INSERT INTO t1 (a, b)
 SELECT c, d FROM t2
 UNION
 SELECT e, f FROM t3
ON DUPLICATE KEY UPDATE b = b + c;
```

Instead, use an equivalent statement that rewrites the [UNION](#page-111-0) as a derived table:

```
INSERT INTO t1 (a, b)
SELECT * FROM
 (SELECT c, d FROM t2
 UNION
 SELECT e, f FROM t3) AS dt
ON DUPLICATE KEY UPDATE b = b + c;
```

The technique of rewriting a query as a derived table also enables references to columns from GROUP BY queries.

Because the results of [INSERT ... SELECT](#page-41-0) statements depend on the ordering of rows from the [SELECT](#page-70-0) and this order cannot always be guaranteed, it is possible when logging [INSERT ...](#page-42-0) [SELECT ON DUPLICATE KEY UPDATE](#page-42-0) statements for the source and the replica to diverge. Thus, [INSERT ... SELECT ON DUPLICATE KEY UPDATE](#page-42-0) statements are flagged as unsafe

for statement-based replication. Such statements produce a warning in the error log when using statement-based mode and are written to the binary log using the row-based format when using MIXED mode. An [INSERT ... ON DUPLICATE KEY UPDATE](#page-42-0) statement against a table having more than one unique or primary key is also marked as unsafe. (Bug #11765650, Bug #58637)

See also Section 19.2.1.1, "Advantages and Disadvantages of Statement-Based and Row-Based Replication".

# <span id="page-46-1"></span>**15.2.7.3 INSERT DELAYED Statement**

```
INSERT DELAYED ...
```

The DELAYED option for the [INSERT](#page-36-0) statement is a MySQL extension to standard SQL. In previous versions of MySQL, it can be used for certain kinds of tables (such as MyISAM), such that when a client uses [INSERT DELAYED](#page-46-1), it gets an okay from the server at once, and the row is queued to be inserted when the table is not in use by any other thread.

DELAYED inserts and replaces were deprecated in MySQL 5.6. In MySQL 8.4, DELAYED is not supported. The server recognizes but ignores the DELAYED keyword, handles the insert as a nondelayed insert, and generates an [ER\\_WARN\\_LEGACY\\_SYNTAX\\_CONVERTED](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_warn_legacy_syntax_converted) warning: INSERT DELAYED is no longer supported. The statement was converted to INSERT. The DELAYED keyword is scheduled for removal in a future release.

# <span id="page-46-0"></span>**15.2.8 INTERSECT Clause**

```
query_expression_body INTERSECT [ALL | DISTINCT] query_expression_body
 [INTERSECT [ALL | DISTINCT] query_expression_body]
 [...]
query_expression_body:
 See Section 15.2.14, "Set Operations with UNION, INTERSECT, and EXCEPT"
```

INTERSECT limits the result from multiple query blocks to those rows which are common to all. Example:

```
mysql> TABLE a;
+------+------+
| m | n |
+------+------+
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |
+------+------+
3 rows in set (0.00 sec)
mysql> TABLE b;
+------+------+
| m | n |
+------+------+
| 1 | 2 |
| 1 | 3 |
| 3 | 4 |
+------+------+
3 rows in set (0.00 sec)
mysql> TABLE c;
+------+------+
| m | n |
+------+------+
| 1 | 3 |
| 1 | 3 |
| 3 | 4 |
+------+------+
3 rows in set (0.00 sec)
mysql> TABLE a INTERSECT TABLE b;
+------+------+
```

```
| m | n |
+------+------+
| 1 | 2 |
| 3 | 4 |
+------+------+
2 rows in set (0.00 sec)
mysql> TABLE a INTERSECT TABLE c;
+------+------+
| m | n |
+------+------+
| 3 | 4 |
+------+------+
1 row in set (0.00 sec)
```

As with [UNION](#page-111-0) and [EXCEPT](#page-31-1), if neither DISTINCT nor ALL is specified, the default is DISTINCT.

DISTINCT can remove duplicates from either side of the intersection, as shown here:

```
mysql> TABLE c INTERSECT DISTINCT TABLE c;
+------+------+
| m | n |
+------+------+
| 1 | 3 |
| 3 | 4 |
+------+------+
2 rows in set (0.00 sec)
mysql> TABLE c INTERSECT ALL TABLE c;
+------+------+
| m | n |
+------+------+
| 1 | 3 |
| 1 | 3 |
| 3 | 4 |
+------+------+
3 rows in set (0.00 sec)
```

(TABLE c INTERSECT TABLE c is the equivalent of the first of the two statements just shown.)

As with UNION, the operands must have the same number of columns. Result set column types are also determined as for UNION.

INTERSECT has greater precedence than and is evaluated before UNION and EXCEPT, so that the two statements shown here are equivalent:

```
TABLE r EXCEPT TABLE s INTERSECT TABLE t;
TABLE r EXCEPT (TABLE s INTERSECT TABLE t);
```

For INTERSECT ALL, the maximum supported number of duplicates of any unique row in the left hand table is 4294967295.

# <span id="page-47-0"></span>**15.2.9 LOAD DATA Statement**

```
LOAD DATA
 [LOW_PRIORITY | CONCURRENT] [LOCAL]
 INFILE 'file_name'
 [REPLACE | IGNORE]
 INTO TABLE tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [CHARACTER SET charset_name]
 [{FIELDS | COLUMNS}
 [TERMINATED BY 'string']
 [[OPTIONALLY] ENCLOSED BY 'char']
 [ESCAPED BY 'char']
 ]
 [LINES
 [STARTING BY 'string']
```

```
 [TERMINATED BY 'string']
 ]
 [IGNORE number {LINES | ROWS}]
 [(col_name_or_user_var
 [, col_name_or_user_var] ...)]
 [SET col_name={expr | DEFAULT}
 [, col_name={expr | DEFAULT}] ...]
```

The [LOAD DATA](#page-47-0) statement reads rows from a text file into a table at a very high speed. The file can be read from the server host or the client host, depending on whether the LOCAL modifier is given. LOCAL also affects data interpretation and error handling.

[LOAD DATA](#page-47-0) is the complement of [SELECT ... INTO OUTFILE](#page-76-0). (See [Section 15.2.13.1, "SELECT ...](#page-76-0) [INTO Statement".](#page-76-0)) To write data from a table to a file, use [SELECT ... INTO OUTFILE](#page-76-0). To read the file back into a table, use [LOAD DATA](#page-47-0). The syntax of the FIELDS and LINES clauses is the same for both statements.

The mysqlimport utility provides another way to load data files; it operates by sending a [LOAD DATA](#page-47-0) statement to the server. See Section 6.5.5, "mysqlimport — A Data Import Program".

For information about the efficiency of [INSERT](#page-36-0) versus [LOAD DATA](#page-47-0) and speeding up [LOAD DATA](#page-47-0), see Section 10.2.5.1, "Optimizing INSERT Statements".

- [Non-LOCAL Versus LOCAL Operation](#page-48-0)
- [Input File Character Set](#page-49-0)
- [Input File Location](#page-49-1)
- [Security Requirements](#page-50-0)
- [Duplicate-Key and Error Handling](#page-50-1)
- [Index Handling](#page-50-2)
- [Field and Line Handling](#page-51-0)
- [Column List Specification](#page-55-0)
- [Input Preprocessing](#page-55-1)
- [Column Value Assignment](#page-56-0)
- [Partitioned Table Support](#page-57-0)
- [Concurrency Considerations](#page-57-1)
- [Statement Result Information](#page-58-0)
- [Replication Considerations](#page-58-1)
- [Miscellaneous Topics](#page-58-2)

## <span id="page-48-0"></span>**Non-LOCAL Versus LOCAL Operation**

The LOCAL modifier affects these aspects of [LOAD DATA](#page-47-0), compared to non-LOCAL operation:

- It changes the expected location of the input file; see [Input File Location](#page-49-1).
- It changes the statement security requirements; see [Security Requirements](#page-50-0).
- Unless REPLACE is also specified, LOCAL has the same effect as the IGNORE modifier on the interpretation of input file contents and error handling; see [Duplicate-Key and Error Handling](#page-50-1), and [Column Value Assignment.](#page-56-0)

LOCAL works only if the server and your client both have been configured to permit it. For example, if mysqld was started with the local\_infile system variable disabled, LOCAL produces an error. See Section 8.1.6, "Security Considerations for LOAD DATA LOCAL".

# <span id="page-49-0"></span>**Input File Character Set**

The file name must be given as a literal string. On Windows, specify backslashes in path names as forward slashes or doubled backslashes. The server interprets the file name using the character set indicated by the character\_set\_filesystem system variable.

By default, the server interprets the file contents using the character set indicated by the character\_set\_database system variable. If the file contents use a character set different from this default, it is a good idea to specify that character set by using the CHARACTER SET clause. A character set of binary specifies "no conversion."

SET NAMES and the setting of character\_set\_client do not affect interpretation of file contents.

[LOAD DATA](#page-47-0) interprets all fields in the file as having the same character set, regardless of the data types of the columns into which field values are loaded. For proper interpretation of the file, you must ensure that it was written with the correct character set. For example, if you write a data file with mysqldump -T or by issuing a [SELECT ... INTO OUTFILE](#page-76-0) statement in mysql, be sure to use a --default-character-set option to write output in the character set to be used when the file is loaded with [LOAD DATA](#page-47-0).

![](_page_49_Picture_7.jpeg)

#### **Note**

It is not possible to load data files that use the ucs2, utf16, utf16le, or utf32 character set.

# <span id="page-49-1"></span>**Input File Location**

These rules determine the [LOAD DATA](#page-47-0) input file location:

- If LOCAL is not specified, the file must be located on the server host. The server reads the file directly, locating it as follows:
  - If the file name is an absolute path name, the server uses it as given.
  - If the file name is a relative path name with leading components, the server looks for the file relative to its data directory.
  - If the file name has no leading components, the server looks for the file in the database directory of the default database.
- If LOCAL is specified, the file must be located on the client host. The client program reads the file, locating it as follows:
  - If the file name is an absolute path name, the client program uses it as given.
  - If the file name is a relative path name, the client program looks for the file relative to its invocation directory.

When LOCAL is used, the client program reads the file and sends its contents to the server. The server creates a copy of the file in the directory where it stores temporary files. See Section B.3.3.5, "Where MySQL Stores Temporary Files". Lack of sufficient space for the copy in this directory can cause the [LOAD DATA LOCAL](#page-47-0) statement to fail.

The non-LOCAL rules mean that the server reads a file named as ./myfile.txt relative to its data directory, whereas it reads a file named as myfile.txt from the database directory of the default database. For example, if the following [LOAD DATA](#page-47-0) statement is executed while db1 is the default database, the server reads the file data.txt from the database directory for db1, even though the statement explicitly loads the file into a table in the db2 database:

LOAD DATA INFILE 'data.txt' INTO TABLE db2.my\_table;

![](_page_50_Picture_2.jpeg)

#### **Note**

The server also uses the non-LOCAL rules to locate .sdi files for the [IMPORT](#page-34-0) [TABLE](#page-34-0) statement.

# <span id="page-50-0"></span>**Security Requirements**

For a non-LOCAL load operation, the server reads a text file located on the server host, so these security requirements must be satisfied:

- You must have the FILE privilege. See Section 8.2.2, "Privileges Provided by MySQL".
- The operation is subject to the secure\_file\_priv system variable setting:
  - If the variable value is a nonempty directory name, the file must be located in that directory.
  - If the variable value is empty (which is insecure), the file need only be readable by the server.

For a LOCAL load operation, the client program reads a text file located on the client host. Because the file contents are sent over the connection by the client to the server, using LOCAL is a bit slower than when the server accesses the file directly. On the other hand, you do not need the FILE privilege, and the file can be located in any directory the client program can access.

# <span id="page-50-1"></span>**Duplicate-Key and Error Handling**

The REPLACE and IGNORE modifiers control handling of new (input) rows that duplicate existing table rows on unique key values (PRIMARY KEY or UNIQUE index values):

- With REPLACE, new rows that have the same value as a unique key value in an existing row replace the existing row. See [Section 15.2.12, "REPLACE Statement"](#page-67-0).
- With IGNORE, new rows that duplicate an existing row on a unique key value are discarded. For more information, see The Effect of IGNORE on Statement Execution.

The LOCAL modifier has the same effect as IGNORE. This occurs because the server has no way to stop transmission of the file in the middle of the operation.

If none of REPLACE, IGNORE, or LOCAL is specified, an error occurs when a duplicate key value is found, and the rest of the text file is ignored.

In addition to affecting duplicate-key handling as just described, IGNORE and LOCAL also affect error handling:

- When neither IGNORE nor LOCAL is specified, data-interpretation errors terminate the operation.
- When IGNORE—or LOCAL without REPLACE—is specified, data interpretation errors become warnings and the load operation continues, even if the SQL mode is restrictive. For examples, see [Column Value Assignment.](#page-56-0)

## <span id="page-50-2"></span>**Index Handling**

To ignore foreign key constraints during the load operation, execute a SET foreign\_key\_checks = 0 statement before executing [LOAD DATA](#page-47-0).

If you use [LOAD DATA](#page-47-0) on an empty MyISAM table, all nonunique indexes are created in a separate batch (as for REPAIR TABLE). Normally, this makes [LOAD DATA](#page-47-0) much faster when you have many indexes. In some extreme cases, you can create the indexes even faster by turning them off with ALTER TABLE ... DISABLE KEYS before loading the file into the table and re-creating the indexes with ALTER TABLE ... ENABLE KEYS after loading the file. See Section 10.2.5.1, "Optimizing INSERT Statements".

## <span id="page-51-0"></span>**Field and Line Handling**

For both the [LOAD DATA](#page-47-0) and [SELECT ... INTO OUTFILE](#page-76-0) statements, the syntax of the FIELDS and LINES clauses is the same. Both clauses are optional, but FIELDS must precede LINES if both are specified.

If you specify a FIELDS clause, each of its subclauses (TERMINATED BY, [OPTIONALLY] ENCLOSED BY, and ESCAPED BY) is also optional, except that you must specify at least one of them. Arguments to these clauses are permitted to contain only ASCII characters.

If you specify no FIELDS or LINES clause, the defaults are the same as if you had written this:

```
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

Backslash is the MySQL escape character within strings in SQL statements. Thus, to specify a literal backslash, you must specify two backslashes for the value to be interpreted as a single backslash. The escape sequences '\t' and '\n' specify tab and newline characters, respectively.

In other words, the defaults cause [LOAD DATA](#page-47-0) to act as follows when reading input:

- Look for line boundaries at newlines.
- Do not skip any line prefix.
- Break lines into fields at tabs.
- Do not expect fields to be enclosed within any quoting characters.
- Interpret characters preceded by the escape character \ as escape sequences. For example, \t, \n, and \\ signify tab, newline, and backslash, respectively. See the discussion of FIELDS ESCAPED BY later for the full list of escape sequences.

Conversely, the defaults cause [SELECT ... INTO OUTFILE](#page-76-0) to act as follows when writing output:

- Write tabs between fields.
- Do not enclose fields within any quoting characters.
- Use \ to escape instances of tab, newline, or \ that occur within field values.
- Write newlines at the ends of lines.

![](_page_51_Picture_18.jpeg)

#### **Note**

For a text file generated on a Windows system, proper file reading might require LINES TERMINATED BY '\r\n' because Windows programs typically use two characters as a line terminator. Some programs, such as WordPad, might use \r as a line terminator when writing files. To read such files, use LINES TERMINATED BY '\r'.

If all the input lines have a common prefix that you want to ignore, you can use LINES STARTING BY 'prefix\_string' to skip the prefix and anything before it. If a line does not include the prefix, the entire line is skipped. Suppose that you issue the following statement:

```
LOAD DATA INFILE '/tmp/test.txt' INTO TABLE test
 FIELDS TERMINATED BY ',' LINES STARTING BY 'xxx';
```

If the data file looks like this:

```
xxx"abc",1
something xxx"def",2
"ghi",3
```

The resulting rows are ("abc",1) and ("def",2). The third row in the file is skipped because it does not contain the prefix.

The IGNORE number LINES clause can be used to ignore lines at the start of the file. For example, you can use IGNORE 1 LINES to skip an initial header line containing column names:

```
LOAD DATA INFILE '/tmp/test.txt' INTO TABLE test IGNORE 1 LINES;
```

When you use [SELECT ... INTO OUTFILE](#page-76-0) in tandem with [LOAD DATA](#page-47-0) to write data from a database into a file and then read the file back into the database later, the field- and line-handling options for both statements must match. Otherwise, [LOAD DATA](#page-47-0) does not interpret the contents of the file properly. Suppose that you use [SELECT ... INTO OUTFILE](#page-76-0) to write a file with fields delimited by commas:

```
SELECT * INTO OUTFILE 'data.txt'
 FIELDS TERMINATED BY ','
 FROM table2;
```

To read the comma-delimited file, the correct statement is:

```
LOAD DATA INFILE 'data.txt' INTO TABLE table2
 FIELDS TERMINATED BY ',';
```

If instead you tried to read the file with the statement shown following, it would not work because it instructs [LOAD DATA](#page-47-0) to look for tabs between fields:

```
LOAD DATA INFILE 'data.txt' INTO TABLE table2
 FIELDS TERMINATED BY '\t';
```

The likely result is that each input line would be interpreted as a single field.

[LOAD DATA](#page-47-0) can be used to read files obtained from external sources. For example, many programs can export data in comma-separated values (CSV) format, such that lines have fields separated by commas and enclosed within double quotation marks, with an initial line of column names. If the lines in such a file are terminated by carriage return/newline pairs, the statement shown here illustrates the field- and line-handling options you would use to load the file:

```
LOAD DATA INFILE 'data.txt' INTO TABLE tbl_name
 FIELDS TERMINATED BY ',' ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n'
 IGNORE 1 LINES;
```

If the input values are not necessarily enclosed within quotation marks, use OPTIONALLY before the ENCLOSED BY option.

Any of the field- or line-handling options can specify an empty string (''). If not empty, the FIELDS [OPTIONALLY] ENCLOSED BY and FIELDS ESCAPED BY values must be a single character. The FIELDS TERMINATED BY, LINES STARTING BY, and LINES TERMINATED BY values can be more than one character. For example, to write lines that are terminated by carriage return/linefeed pairs, or to read a file containing such lines, specify a LINES TERMINATED BY '\r\n' clause.

To read a file containing jokes that are separated by lines consisting of %%, you can do this

```
CREATE TABLE jokes
 (a INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 joke TEXT NOT NULL);
LOAD DATA INFILE '/tmp/jokes.txt' INTO TABLE jokes
 FIELDS TERMINATED BY ''
 LINES TERMINATED BY '\n%%\n' (joke);
```

FIELDS [OPTIONALLY] ENCLOSED BY controls quoting of fields. For output ([SELECT ... INTO](#page-76-0) [OUTFILE](#page-76-0)), if you omit the word OPTIONALLY, all fields are enclosed by the ENCLOSED BY character. An example of such output (using a comma as the field delimiter) is shown here:

```
"1","a string","100.20"
"2","a string containing a , comma","102.20"
"3","a string containing a \" quote","102.20"
"4","a string containing a \", quote and comma","102.20"
```

If you specify OPTIONALLY, the ENCLOSED BY character is used only to enclose values from columns that have a string data type (such as CHAR, BINARY, TEXT, or ENUM):

```
1,"a string",100.20
2,"a string containing a , comma",102.20
3,"a string containing a \" quote",102.20
4,"a string containing a \", quote and comma",102.20
```

Occurrences of the ENCLOSED BY character within a field value are escaped by prefixing them with the ESCAPED BY character. Also, if you specify an empty ESCAPED BY value, it is possible to inadvertently generate output that cannot be read properly by [LOAD DATA](#page-47-0). For example, the preceding output just shown would appear as follows if the escape character is empty. Observe that the second field in the fourth line contains a comma following the quote, which (erroneously) appears to terminate the field:

```
1,"a string",100.20
2,"a string containing a , comma",102.20
3,"a string containing a " quote",102.20
4,"a string containing a ", quote and comma",102.20
```

For input, the ENCLOSED BY character, if present, is stripped from the ends of field values. (This is true regardless of whether OPTIONALLY is specified; OPTIONALLY has no effect on input interpretation.) Occurrences of the ENCLOSED BY character preceded by the ESCAPED BY character are interpreted as part of the current field value.

If the field begins with the ENCLOSED BY character, instances of that character are recognized as terminating a field value only if followed by the field or line TERMINATED BY sequence. To avoid ambiguity, occurrences of the ENCLOSED BY character within a field value can be doubled and are interpreted as a single instance of the character. For example, if ENCLOSED BY '"' is specified, quotation marks are handled as shown here:

```
"The ""BIG"" boss" -> The "BIG" boss
The "BIG" boss -> The "BIG" boss
The ""BIG"" boss -> The ""BIG"" boss
```

FIELDS ESCAPED BY controls how to read or write special characters:

• For input, if the FIELDS ESCAPED BY character is not empty, occurrences of that character are stripped and the following character is taken literally as part of a field value. Some two-character sequences that are exceptions, where the first character is the escape character. These sequences are shown in the following table (using \ for the escape character). The rules for NULL handling are described later in this section.

| Character | Escape Sequence                |
|-----------|--------------------------------|
| \0        | An ASCII NUL (X'00') character |
| \b        | A backspace character          |
| \n        | A newline (linefeed) character |
| \r        | A carriage return character    |
| \t        | A tab character.               |
| \Z        | ASCII 26 (Control+Z)           |
| \N        | NULL                           |

For more information about \-escape syntax, see Section 11.1.1, "String Literals".

If the FIELDS ESCAPED BY character is empty, escape-sequence interpretation does not occur.

- For output, if the FIELDS ESCAPED BY character is not empty, it is used to prefix the following characters on output:
  - The FIELDS ESCAPED BY character.

- The FIELDS [OPTIONALLY] ENCLOSED BY character.
- The first character of the FIELDS TERMINATED BY and LINES TERMINATED BY values, if the ENCLOSED BY character is empty or unspecified.
- ASCII 0 (what is actually written following the escape character is ASCII 0, not a zero-valued byte).

If the FIELDS ESCAPED BY character is empty, no characters are escaped and NULL is output as NULL, not \N. It is probably not a good idea to specify an empty escape character, particularly if field values in your data contain any of the characters in the list just given.

In certain cases, field- and line-handling options interact:

- If LINES TERMINATED BY is an empty string and FIELDS TERMINATED BY is nonempty, lines are also terminated with FIELDS TERMINATED BY.
- If the FIELDS TERMINATED BY and FIELDS ENCLOSED BY values are both empty (''), a fixedrow (nondelimited) format is used. With fixed-row format, no delimiters are used between fields (but you can still have a line terminator). Instead, column values are read and written using a field width wide enough to hold all values in the field. For TINYINT, SMALLINT, MEDIUMINT, INT, and BIGINT, the field widths are 4, 6, 8, 11, and 20, respectively, no matter what the declared display width is.

LINES TERMINATED BY is still used to separate lines. If a line does not contain all fields, the rest of the columns are set to their default values. If you do not have a line terminator, you should set this to ''. In this case, the text file must contain all fields for each row.

Fixed-row format also affects handling of NULL values, as described later.

![](_page_54_Picture_10.jpeg)

#### **Note**

Fixed-size format does not work if you are using a multibyte character set.

Handling of NULL values varies according to the FIELDS and LINES options in use:

- For the default FIELDS and LINES values, NULL is written as a field value of \N for output, and a field value of \N is read as NULL for input (assuming that the ESCAPED BY character is \).
- If FIELDS ENCLOSED BY is not empty, a field containing the literal word NULL as its value is read as a NULL value. This differs from the word NULL enclosed within FIELDS ENCLOSED BY characters, which is read as the string 'NULL'.
- If FIELDS ESCAPED BY is empty, NULL is written as the word NULL.
- With fixed-row format (which is used when FIELDS TERMINATED BY and FIELDS ENCLOSED BY are both empty), NULL is written as an empty string. This causes both NULL values and empty strings in the table to be indistinguishable when written to the file because both are written as empty strings. If you need to be able to tell the two apart when reading the file back in, you should not use fixed-row format.

An attempt to load NULL into a NOT NULL column produces either a warning or an error according to the rules described in [Column Value Assignment.](#page-56-0)

Some cases are not supported by [LOAD DATA](#page-47-0):

- Fixed-size rows (FIELDS TERMINATED BY and FIELDS ENCLOSED BY both empty) and BLOB or TEXT columns.
- If you specify one separator that is the same as or a prefix of another, [LOAD DATA](#page-47-0) cannot interpret the input properly. For example, the following FIELDS clause would cause problems:

```
FIELDS TERMINATED BY '"' ENCLOSED BY '"'
```

• If FIELDS ESCAPED BY is empty, a field value that contains an occurrence of FIELDS ENCLOSED BY or LINES TERMINATED BY followed by the FIELDS TERMINATED BY value causes [LOAD](#page-47-0) [DATA](#page-47-0) to stop reading a field or line too early. This happens because [LOAD DATA](#page-47-0) cannot properly determine where the field or line value ends.

# <span id="page-55-0"></span>**Column List Specification**

The following example loads all columns of the persondata table:

```
LOAD DATA INFILE 'persondata.txt' INTO TABLE persondata;
```

By default, when no column list is provided at the end of the [LOAD DATA](#page-47-0) statement, input lines are expected to contain a field for each table column. If you want to load only some of a table's columns, specify a column list:

```
LOAD DATA INFILE 'persondata.txt' INTO TABLE persondata
(col_name_or_user_var [, col_name_or_user_var] ...);
```

You must also specify a column list if the order of the fields in the input file differs from the order of the columns in the table. Otherwise, MySQL cannot tell how to match input fields with table columns.

## <span id="page-55-1"></span>**Input Preprocessing**

Each instance of col\_name\_or\_user\_var in [LOAD DATA](#page-47-0) syntax is either a column name or a user variable. With user variables, the SET clause enables you to perform preprocessing transformations on their values before assigning the result to columns.

User variables in the SET clause can be used in several ways. The following example uses the first input column directly for the value of t1.column1, and assigns the second input column to a user variable that is subjected to a division operation before being used for the value of t1.column2:

```
LOAD DATA INFILE 'file.txt'
 INTO TABLE t1
 (column1, @var1)
 SET column2 = @var1/100;
```

The SET clause can be used to supply values not derived from the input file. The following statement sets column3 to the current date and time:

```
LOAD DATA INFILE 'file.txt'
 INTO TABLE t1
 (column1, column2)
 SET column3 = CURRENT_TIMESTAMP;
```

You can also discard an input value by assigning it to a user variable and not assigning the variable to any table column:

```
LOAD DATA INFILE 'file.txt'
 INTO TABLE t1
 (column1, @dummy, column2, @dummy, column3);
```

Use of the column/variable list and SET clause is subject to the following restrictions:

- Assignments in the SET clause should have only column names on the left hand side of assignment operators.
- You can use subqueries in the right hand side of SET assignments. A subquery that returns a value to be assigned to a column may be a scalar subquery only. Also, you cannot use a subquery to select from the table that is being loaded.
- Lines ignored by an IGNORE number LINES clause are not processed for the column/variable list or SET clause.

• User variables cannot be used when loading data with fixed-row format because user variables do not have a display width.

## <span id="page-56-0"></span>**Column Value Assignment**

To process an input line, [LOAD DATA](#page-47-0) splits it into fields and uses the values according to the column/ variable list and the SET clause, if they are present. Then the resulting row is inserted into the table. If there are BEFORE INSERT or AFTER INSERT triggers for the table, they are activated before or after inserting the row, respectively.

Interpretation of field values and assignment to table columns depends on these factors:

- The SQL mode (the value of the sql\_mode system variable). The mode can be nonrestrictive, or restrictive in various ways. For example, strict SQL mode can be enabled, or the mode can include values such as NO\_ZERO\_DATE or NO\_ZERO\_IN\_DATE.
- Presence or absence of the IGNORE and LOCAL modifiers.

Those factors combine to produce restrictive or nonrestrictive data interpretation by [LOAD DATA](#page-47-0):

- Data interpretation is restrictive if the SQL mode is restrictive and neither the IGNORE nor the LOCAL modifier is specified. Errors terminate the load operation.
- Data interpretation is nonrestrictive if the SQL mode is nonrestrictive or the IGNORE or LOCAL modifier is specified. (In particular, either modifier if specified overrides a restrictive SQL mode when the REPLACE modifier is omitted.) Errors become warnings and the load operation continues.

Restrictive data interpretation uses these rules:

- Too many or too few fields results an error.
- Assigning NULL (that is, \N) to a non-NULL column results in an error.
- A value that is out of range for the column data type results in an error.
- Invalid values produce errors. For example, a value such as 'x' for a numeric column results in an error, not conversion to 0.

By contrast, nonrestrictive data interpretation uses these rules:

- If an input line has too many fields, the extra fields are ignored and the number of warnings is incremented.
- If an input line has too few fields, the columns for which input fields are missing are assigned their default values. Default value assignment is described in Section 13.6, "Data Type Default Values".
- Assigning NULL (that is, \N) to a non-NULL column results in assignment of the implicit default value for the column data type. Implicit default values are described in Section 13.6, "Data Type Default Values".
- Invalid values produce warnings rather than errors, and are converted to the "closest" valid value for the column data type. Examples:
  - A value such as 'x' for a numeric column results in conversion to 0.
  - An out-of-range numeric or temporal value is clipped to the closest endpoint of the range for the column data type.
  - An invalid value for a DATETIME, DATE, or TIME column is inserted as the implicit default value, regardless of the SQL mode NO\_ZERO\_DATE setting. The implicit default is the appropriate "zero" value for the type ('0000-00-00 00:00:00', '0000-00-00', or '00:00:00'). See Section 13.2, "Date and Time Data Types".

- [LOAD DATA](#page-47-0) interprets an empty field value differently from a missing field:
  - For string types, the column is set to the empty string.
  - For numeric types, the column is set to 0.
  - For date and time types, the column is set to the appropriate "zero" value for the type. See Section 13.2, "Date and Time Data Types".

These are the same values that result if you assign an empty string explicitly to a string, numeric, or date or time type explicitly in an [INSERT](#page-36-0) or [UPDATE](#page-108-0) statement.

TIMESTAMP columns are set to the current date and time only if there is a NULL value for the column (that is, \N) and the column is not declared to permit NULL values, or if the TIMESTAMP column default value is the current timestamp and it is omitted from the field list when a field list is specified.

[LOAD DATA](#page-47-0) regards all input as strings, so you cannot use numeric values for ENUM or SET columns the way you can with [INSERT](#page-36-0) statements. All ENUM and SET values must be specified as strings.

BIT values cannot be loaded directly using binary notation (for example, b'011010'). To work around this, use the SET clause to strip off the leading b' and trailing ' and perform a base-2 to base-10 conversion so that MySQL loads the values into the BIT column properly:

```
$> cat /tmp/bit_test.txt
b'10'
b'1111111'
$> mysql test
mysql> LOAD DATA INFILE '/tmp/bit_test.txt'
 INTO TABLE bit_test (@var1)
 SET b = CAST(CONV(MID(@var1, 3, LENGTH(@var1)-3), 2, 10) AS UNSIGNED);
Query OK, 2 rows affected (0.00 sec)
Records: 2 Deleted: 0 Skipped: 0 Warnings: 0
mysql> SELECT BIN(b+0) FROM bit_test;
+----------+
| BIN(b+0) |
+----------+
| 10 |
| 1111111 |
+----------+
2 rows in set (0.00 sec)
```

For BIT values in 0b binary notation (for example, 0b011010), use this SET clause instead to strip off the leading 0b:

```
SET b = CAST(CONV(MID(@var1, 3, LENGTH(@var1)-2), 2, 10) AS UNSIGNED)
```

# <span id="page-57-0"></span>**Partitioned Table Support**

[LOAD DATA](#page-47-0) supports explicit partition selection using the PARTITION clause with a list of one or more comma-separated names of partitions, subpartitions, or both. When this clause is used, if any rows from the file cannot be inserted into any of the partitions or subpartitions named in the list, the statement fails with the error Found a row not matching the given partition set. For more information and examples, see Section 26.5, "Partition Selection".

## <span id="page-57-1"></span>**Concurrency Considerations**

With the LOW\_PRIORITY modifier, execution of the [LOAD DATA](#page-47-0) statement is delayed until no other clients are reading from the table. This affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE).

With the CONCURRENT modifier and a MyISAM table that satisfies the condition for concurrent inserts (that is, it contains no free blocks in the middle), other threads can retrieve data from the table while

[LOAD DATA](#page-47-0) is executing. This modifier affects the performance of [LOAD DATA](#page-47-0) a bit, even if no other thread is using the table at the same time.

# <span id="page-58-0"></span>**Statement Result Information**

When the [LOAD DATA](#page-47-0) statement finishes, it returns an information string in the following format:

```
Records: 1 Deleted: 0 Skipped: 0 Warnings: 0
```

Warnings occur under the same circumstances as when values are inserted using the [INSERT](#page-36-0) statement (see [Section 15.2.7, "INSERT Statement"](#page-36-0)), except that [LOAD DATA](#page-47-0) also generates warnings when there are too few or too many fields in the input row.

You can use SHOW WARNINGS to get a list of the first max\_error\_count warnings as information about what went wrong. See Section 15.7.7.42, "SHOW WARNINGS Statement".

If you are using the C API, you can get information about the statement by calling the [mysql\\_info\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md) function. See [mysql\\_info\(\).](https://dev.mysql.com/doc/c-api/8.4/en/mysql-info.md)

# <span id="page-58-1"></span>**Replication Considerations**

[LOAD DATA](#page-47-0) is considered unsafe for statement-based replication. If you use [LOAD DATA](#page-47-0) with binlog\_format=STATEMENT, each replica on which the changes are to be applied creates a temporary file containing the data. This temporary file is not encrypted, even if binary log encryption is active on the source, If encryption is required, use row-based or mixed binary logging format instead, for which replicas do not create the temporary file. For more information on the interaction between [LOAD DATA](#page-47-0) and replication, see Section 19.5.1.19, "Replication and LOAD DATA".

# <span id="page-58-2"></span>**Miscellaneous Topics**

On Unix, if you need [LOAD DATA](#page-47-0) to read from a pipe, you can use the following technique (the example loads a listing of the / directory into the table db1.t1):

```
mkfifo /mysql/data/db1/ls.dat
chmod 666 /mysql/data/db1/ls.dat
find / -ls > /mysql/data/db1/ls.dat &
mysql -e "LOAD DATA INFILE 'ls.dat' INTO TABLE t1" db1
```

Here you must run the command that generates the data to be loaded and the mysql commands either on separate terminals, or run the data generation process in the background (as shown in the preceding example). If you do not do this, the pipe blocks until data is read by the mysql process.

# <span id="page-58-3"></span>**15.2.10 LOAD XML Statement**

```
LOAD XML
 [LOW_PRIORITY | CONCURRENT] [LOCAL]
 INFILE 'file_name'
 [REPLACE | IGNORE]
 INTO TABLE [db_name.]tbl_name
 [CHARACTER SET charset_name]
 [ROWS IDENTIFIED BY '<tagname>']
 [IGNORE number {LINES | ROWS}]
 [(field_name_or_user_var
 [, field_name_or_user_var] ...)]
 [SET col_name={expr | DEFAULT}
 [, col_name={expr | DEFAULT}] ...]
```

The [LOAD XML](#page-58-3) statement reads data from an XML file into a table. The file\_name must be given as a literal string. The tagname in the optional ROWS IDENTIFIED BY clause must also be given as a literal string, and must be surrounded by angle brackets (< and >).

[LOAD XML](#page-58-3) acts as the complement of running the mysql client in XML output mode (that is, starting the client with the --xml option). To write data from a table to an XML file, you can invoke the mysql client with the --xml and -e options from the system shell, as shown here:

```
$> mysql --xml -e 'SELECT * FROM mydb.mytable' > file.xml
```

To read the file back into a table, use [LOAD XML](#page-58-3). By default, the <row> element is considered to be the equivalent of a database table row; this can be changed using the ROWS IDENTIFIED BY clause.

This statement supports three different XML formats:

• Column names as attributes and column values as attribute values:

```
<row column1="value1" column2="value2" .../>
```

• Column names as tags and column values as the content of these tags:

```
<row>
 <column1>value1</column1>
 <column2>value2</column2>
</row>
```

• Column names are the name attributes of <field> tags, and values are the contents of these tags:

```
<row>
 <field name='column1'>value1</field>
 <field name='column2'>value2</field>
</row>
```

This is the format used by other MySQL tools, such as mysqldump.

All three formats can be used in the same XML file; the import routine automatically detects the format for each row and interprets it correctly. Tags are matched based on the tag or attribute name and the column name.

The following clauses work essentially the same way for [LOAD XML](#page-58-3) as they do for [LOAD DATA](#page-47-0):

- LOW\_PRIORITY or CONCURRENT
- LOCAL
- REPLACE or IGNORE
- CHARACTER SET
- SET

See [Section 15.2.9, "LOAD DATA Statement",](#page-47-0) for more information about these clauses.

(field\_name\_or\_user\_var, ...) is a list of one or more comma-separated XML fields or user variables. The name of a user variable used for this purpose must match the name of a field from the XML file, prefixed with @. You can use field names to select only desired fields. User variables can be employed to store the corresponding field values for subsequent re-use.

The IGNORE number LINES or IGNORE number ROWS clause causes the first number rows in the XML file to be skipped. It is analogous to the [LOAD DATA](#page-47-0) statement's IGNORE ... LINES clause.

Suppose that we have a table named person, created as shown here:

```
USE test;
CREATE TABLE person (
 person_id INT NOT NULL PRIMARY KEY,
 fname VARCHAR(40) NULL,
 lname VARCHAR(40) NULL,
 created TIMESTAMP
);
```

Suppose further that this table is initially empty.

Now suppose that we have a simple XML file person.xml, whose contents are as shown here:

```
<list>
 <person person_id="1" fname="Kapek" lname="Sainnouine"/>
 <person person_id="2" fname="Sajon" lname="Rondela"/>
 <person person_id="3"><fname>Likame</fname><lname>Örrtmons</lname></person>
 <person person_id="4"><fname>Slar</fname><lname>Manlanth</lname></person>
 <person><field name="person_id">5</field><field name="fname">Stoma</field>
 <field name="lname">Milu</field></person>
 <person><field name="person_id">6</field><field name="fname">Nirtam</field>
 <field name="lname">Sklöd</field></person>
 <person person_id="7"><fname>Sungam</fname><lname>Dulbåd</lname></person>
 <person person_id="8" fname="Sraref" lname="Encmelt"/>
</list>
```

Each of the permissible XML formats discussed previously is represented in this example file.

To import the data in person.xml into the person table, you can use this statement:

```
mysql> LOAD XML LOCAL INFILE 'person.xml'
 -> INTO TABLE person
 -> ROWS IDENTIFIED BY '<person>';
Query OK, 8 rows affected (0.00 sec)
Records: 8 Deleted: 0 Skipped: 0 Warnings: 0
```

Here, we assume that person.xml is located in the MySQL data directory. If the file cannot be found, the following error results:

```
ERROR 2 (HY000): File '/person.xml' not found (Errcode: 2)
```

The ROWS IDENTIFIED BY '<person>' clause means that each <person> element in the XML file is considered equivalent to a row in the table into which the data is to be imported. In this case, this is the person table in the test database.

As can be seen by the response from the server, 8 rows were imported into the test.person table. This can be verified by a simple [SELECT](#page-70-0) statement:

```
mysql> SELECT * FROM person;
+-----------+--------+------------+---------------------+
| person_id | fname | lname | created |
+-----------+--------+------------+---------------------+
| 1 | Kapek | Sainnouine | 2007-07-13 16:18:47 |
| 2 | Sajon | Rondela | 2007-07-13 16:18:47 |
| 3 | Likame | Örrtmons | 2007-07-13 16:18:47 |
| 4 | Slar | Manlanth | 2007-07-13 16:18:47 |
| 5 | Stoma | Nilu | 2007-07-13 16:18:47 |
| 6 | Nirtam | Sklöd | 2007-07-13 16:18:47 |
| 7 | Sungam | Dulbåd | 2007-07-13 16:18:47 |
| 8 | Sreraf | Encmelt | 2007-07-13 16:18:47 |
+-----------+--------+------------+---------------------+
8 rows in set (0.00 sec)
```

This shows, as stated earlier in this section, that any or all of the 3 permitted XML formats may appear in a single file and be read using [LOAD XML](#page-58-3).

The inverse of the import operation just shown—that is, dumping MySQL table data into an XML file can be accomplished using the mysql client from the system shell, as shown here:

```
$> mysql --xml -e "SELECT * FROM test.person" > person-dump.xml
$> cat person-dump.xml
<?xml version="1.0"?>
<resultset statement="SELECT * FROM test.person" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <row>
 <field name="person_id">1</field>
 <field name="fname">Kapek</field>
 <field name="lname">Sainnouine</field>
```

```
 </row>
 <row>
 <field name="person_id">2</field>
 <field name="fname">Sajon</field>
 <field name="lname">Rondela</field>
 </row>
 <row>
 <field name="person_id">3</field>
 <field name="fname">Likema</field>
 <field name="lname">Örrtmons</field>
 </row>
 <row>
 <field name="person_id">4</field>
 <field name="fname">Slar</field>
 <field name="lname">Manlanth</field>
 </row>
 <row>
 <field name="person_id">5</field>
 <field name="fname">Stoma</field>
 <field name="lname">Nilu</field>
 </row>
 <row>
 <field name="person_id">6</field>
 <field name="fname">Nirtam</field>
 <field name="lname">Sklöd</field>
 </row>
 <row>
 <field name="person_id">7</field>
 <field name="fname">Sungam</field>
 <field name="lname">Dulbåd</field>
 </row>
 <row>
 <field name="person_id">8</field>
 <field name="fname">Sreraf</field>
 <field name="lname">Encmelt</field>
 </row>
</resultset>
```

![](_page_61_Picture_2.jpeg)

#### **Note**

The --xml option causes the mysql client to use XML formatting for its output; the -e option causes the client to execute the SQL statement immediately following the option. See Section 6.5.1, "mysql — The MySQL Command-Line Client".

You can verify that the dump is valid by creating a copy of the person table and importing the dump file into the new table, like this:

```
mysql> USE test;
mysql> CREATE TABLE person2 LIKE person;
Query OK, 0 rows affected (0.00 sec)
mysql> LOAD XML LOCAL INFILE 'person-dump.xml'
 -> INTO TABLE person2;
Query OK, 8 rows affected (0.01 sec)
Records: 8 Deleted: 0 Skipped: 0 Warnings: 0
mysql> SELECT * FROM person2;
+-----------+--------+------------+---------------------+
| person_id | fname | lname | created |
+-----------+--------+------------+---------------------+
| 1 | Kapek | Sainnouine | 2007-07-13 16:18:47 |
| 2 | Sajon | Rondela | 2007-07-13 16:18:47 |
| 3 | Likema | Örrtmons | 2007-07-13 16:18:47 |
```

```
| 4 | Slar | Manlanth | 2007-07-13 16:18:47 |
| 5 | Stoma | Nilu | 2007-07-13 16:18:47 |
| 6 | Nirtam | Sklöd | 2007-07-13 16:18:47 |
| 7 | Sungam | Dulbåd | 2007-07-13 16:18:47 |
| 8 | Sreraf | Encmelt | 2007-07-13 16:18:47 |
+-----------+--------+------------+---------------------+
8 rows in set (0.00 sec)
```

There is no requirement that every field in the XML file be matched with a column in the corresponding table. Fields which have no corresponding columns are skipped. You can see this by first emptying the person2 table and dropping the created column, then using the same [LOAD XML](#page-58-3) statement we just employed previously, like this:

```
mysql> TRUNCATE person2;
Query OK, 8 rows affected (0.26 sec)
mysql> ALTER TABLE person2 DROP COLUMN created;
Query OK, 0 rows affected (0.52 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql> SHOW CREATE TABLE person2\G
*************************** 1. row ***************************
 Table: person2
Create Table: CREATE TABLE `person2` (
 `person_id` int NOT NULL,
 `fname` varchar(40) DEFAULT NULL,
 `lname` varchar(40) DEFAULT NULL,
 PRIMARY KEY (`person_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql> LOAD XML LOCAL INFILE 'person-dump.xml'
 -> INTO TABLE person2;
Query OK, 8 rows affected (0.01 sec)
Records: 8 Deleted: 0 Skipped: 0 Warnings: 0
mysql> SELECT * FROM person2;
+-----------+--------+------------+
| person_id | fname | lname |
+-----------+--------+------------+
| 1 | Kapek | Sainnouine |
| 2 | Sajon | Rondela |
| 3 | Likema | Örrtmons |
| 4 | Slar | Manlanth |
| 5 | Stoma | Nilu |
| 6 | Nirtam | Sklöd |
| 7 | Sungam | Dulbåd |
| 8 | Sreraf | Encmelt |
+-----------+--------+------------+
8 rows in set (0.00 sec)
```

The order in which the fields are given within each row of the XML file does not affect the operation of [LOAD XML](#page-58-3); the field order can vary from row to row, and is not required to be in the same order as the corresponding columns in the table.

As mentioned previously, you can use a (field\_name\_or\_user\_var, ...) list of one or more XML fields (to select desired fields only) or user variables (to store the corresponding field values for later use). User variables can be especially useful when you want to insert data from an XML file into table columns whose names do not match those of the XML fields. To see how this works, we first create a table named individual whose structure matches that of the person table, but whose columns are named differently:

```
mysql> CREATE TABLE individual (
 -> individual_id INT NOT NULL PRIMARY KEY,
 -> name1 VARCHAR(40) NULL,
 -> name2 VARCHAR(40) NULL,
 -> made TIMESTAMP
 -> );
Query OK, 0 rows affected (0.42 sec)
```

In this case, you cannot simply load the XML file directly into the table, because the field and column names do not match:

```
mysql> LOAD XML INFILE '../bin/person-dump.xml' INTO TABLE test.individual;
ERROR 1263 (22004): Column set to default value; NULL supplied to NOT NULL column 'individual_id' at row 1
```

This happens because the MySQL server looks for field names matching the column names of the target table. You can work around this problem by selecting the field values into user variables, then setting the target table's columns equal to the values of those variables using SET. You can perform both of these operations in a single statement, as shown here:

```
mysql> LOAD XML INFILE '../bin/person-dump.xml'
 -> INTO TABLE test.individual (@person_id, @fname, @lname, @created)
 -> SET individual_id=@person_id, name1=@fname, name2=@lname, made=@created;
Query OK, 8 rows affected (0.05 sec)
Records: 8 Deleted: 0 Skipped: 0 Warnings: 0
mysql> SELECT * FROM individual;
+---------------+--------+------------+---------------------+
| individual_id | name1 | name2 | made |
+---------------+--------+------------+---------------------+
| 1 | Kapek | Sainnouine | 2007-07-13 16:18:47 |
| 2 | Sajon | Rondela | 2007-07-13 16:18:47 |
| 3 | Likema | Örrtmons | 2007-07-13 16:18:47 |
| 4 | Slar | Manlanth | 2007-07-13 16:18:47 |
| 5 | Stoma | Nilu | 2007-07-13 16:18:47 |
| 6 | Nirtam | Sklöd | 2007-07-13 16:18:47 |
| 7 | Sungam | Dulbåd | 2007-07-13 16:18:47 |
| 8 | Srraf | Encmelt | 2007-07-13 16:18:47 |
+---------------+--------+------------+---------------------+
8 rows in set (0.00 sec)
```

The names of the user variables must match those of the corresponding fields from the XML file, with the addition of the required @ prefix to indicate that they are variables. The user variables need not be listed or assigned in the same order as the corresponding fields.

Using a ROWS IDENTIFIED BY '<tagname>' clause, it is possible to import data from the same XML file into database tables with different definitions. For this example, suppose that you have a file named address.xml which contains the following XML:

```
<?xml version="1.0"?>
<list>
 <person person_id="1">
 <fname>Robert</fname>
 <lname>Jones</lname>
 <address address_id="1" street="Mill Creek Road" zip="45365" city="Sidney"/>
 <address address_id="2" street="Main Street" zip="28681" city="Taylorsville"/>
 </person>
 <person person_id="2">
 <fname>Mary</fname>
 <lname>Smith</lname>
 <address address_id="3" street="River Road" zip="80239" city="Denver"/>
 <!-- <address address_id="4" street="North Street" zip="37920" city="Knoxville"/> -->
 </person>
</list>
```

You can again use the test.person table as defined previously in this section, after clearing all the existing records from the table and then showing its structure as shown here:

```
mysql< TRUNCATE person;
Query OK, 0 rows affected (0.04 sec)
mysql< SHOW CREATE TABLE person\G
*************************** 1. row ***************************
 Table: person
Create Table: CREATE TABLE `person` (
```

```
 `person_id` int(11) NOT NULL,
 `fname` varchar(40) DEFAULT NULL,
 `lname` varchar(40) DEFAULT NULL,
 `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (`person_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

Now create an address table in the test database using the following CREATE TABLE statement:

```
CREATE TABLE address (
 address_id INT NOT NULL PRIMARY KEY,
 person_id INT NULL,
 street VARCHAR(40) NULL,
 zip INT NULL,
 city VARCHAR(40) NULL,
 created TIMESTAMP
);
```

To import the data from the XML file into the person table, execute the following [LOAD XML](#page-58-3) statement, which specifies that rows are to be specified by the <person> element, as shown here;

```
mysql> LOAD XML LOCAL INFILE 'address.xml'
 -> INTO TABLE person
 -> ROWS IDENTIFIED BY '<person>';
Query OK, 2 rows affected (0.00 sec)
Records: 2 Deleted: 0 Skipped: 0 Warnings: 0
```

You can verify that the records were imported using a [SELECT](#page-70-0) statement:

```
mysql> SELECT * FROM person;
+-----------+--------+-------+---------------------+
| person_id | fname | lname | created |
+-----------+--------+-------+---------------------+
| 1 | Robert | Jones | 2007-07-24 17:37:06 |
| 2 | Mary | Smith | 2007-07-24 17:37:06 |
+-----------+--------+-------+---------------------+
2 rows in set (0.00 sec)
```

Since the <address> elements in the XML file have no corresponding columns in the person table, they are skipped.

To import the data from the <address> elements into the address table, use the [LOAD XML](#page-58-3) statement shown here:

```
mysql> LOAD XML LOCAL INFILE 'address.xml'
 -> INTO TABLE address
 -> ROWS IDENTIFIED BY '<address>';
Query OK, 3 rows affected (0.00 sec)
Records: 3 Deleted: 0 Skipped: 0 Warnings: 0
```

You can see that the data was imported using a [SELECT](#page-70-0) statement such as this one:

```
mysql> SELECT * FROM address;
+------------+-----------+-----------------+-------+--------------+---------------------+
| address_id | person_id | street | zip | city | created |
+------------+-----------+-----------------+-------+--------------+---------------------+
| 1 | 1 | Mill Creek Road | 45365 | Sidney | 2007-07-24 17:37:37 |
| 2 | 1 | Main Street | 28681 | Taylorsville | 2007-07-24 17:37:37 |
| 3 | 2 | River Road | 80239 | Denver | 2007-07-24 17:37:37 |
+------------+-----------+-----------------+-------+--------------+---------------------+
3 rows in set (0.00 sec)
```

The data from the <address> element that is enclosed in XML comments is not imported. However, since there is a person\_id column in the address table, the value of the person\_id attribute from the parent <person> element for each <address> is imported into the address table.

**Security Considerations.** As with the [LOAD DATA](#page-47-0) statement, the transfer of the XML file from the client host to the server host is initiated by the MySQL server. In theory, a patched server could be built that would tell the client program to transfer a file of the server's choosing rather than the file named by the client in the [LOAD XML](#page-58-3) statement. Such a server could access any file on the client host to which the client user has read access.

In a Web environment, clients usually connect to MySQL from a Web server. A user that can run any command against the MySQL server can use [LOAD XML LOCAL](#page-58-3) to read any files to which the Web server process has read access. In this environment, the client with respect to the MySQL server is actually the Web server, not the remote program being run by the user who connects to the Web server.

You can disable loading of XML files from clients by starting the server with --local-infile=0 or --local-infile=OFF. This option can also be used when starting the mysql client to disable [LOAD](#page-58-3) [XML](#page-58-3) for the duration of the client session.

To prevent a client from loading XML files from the server, do not grant the FILE privilege to the corresponding MySQL user account, or revoke this privilege if the client user account already has it.

![](_page_65_Picture_5.jpeg)

# **Important**

Revoking the FILE privilege (or not granting it in the first place) keeps the user only from executing the [LOAD XML](#page-58-3) statement (as well as the LOAD\_FILE() function; it does not prevent the user from executing [LOAD XML LOCAL](#page-58-3). To disallow this statement, you must start the server or the client with --localinfile=OFF.

In other words, the FILE privilege affects only whether the client can read files on the server; it has no bearing on whether the client can read files on the local file system.