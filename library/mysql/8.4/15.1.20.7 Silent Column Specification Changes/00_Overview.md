---
source: MySQL 8.4 Reference
title: 00_Overview
---

In some cases, MySQL silently changes column specifications from those given in a [CREATE TABLE](#page-145-0) or [ALTER TABLE](#page-88-1) statement. These might be changes to a data type, to attributes associated with a data type, or to an index specification.

All changes are subject to the internal row-size limit of 65,535 bytes, which may cause some attempts at data type changes to fail. See Section 10.4.7, "Limits on Table Column Count and Row Size".

- Columns that are part of a PRIMARY KEY are made NOT NULL even if not declared that way.
- Trailing spaces are automatically deleted from ENUM and SET member values when the table is created.

- MySQL maps certain data types used by other SQL database vendors to MySQL types. See Section 13.9, "Using Data Types from Other Database Engines".
- If you include a USING clause to specify an index type that is not permitted for a given storage engine, but there is another index type available that the engine can use without affecting query results, the engine uses the available type.
- If strict SQL mode is not enabled, a VARCHAR column with a length specification greater than 65535 is converted to TEXT, and a VARBINARY column with a length specification greater than 65535 is converted to BLOB. Otherwise, an error occurs in either of these cases.
- Specifying the CHARACTER SET binary attribute for a character data type causes the column to be created as the corresponding binary data type: CHAR becomes BINARY, VARCHAR becomes VARBINARY, and TEXT becomes BLOB. For the ENUM and SET data types, this does not occur; they are created as declared. Suppose that you specify a table using this definition:

```
CREATE TABLE t
(
 c1 VARCHAR(10) CHARACTER SET binary,
 c2 TEXT CHARACTER SET binary,
 c3 ENUM('a','b','c') CHARACTER SET binary
);
```

The resulting table has this definition:

```
CREATE TABLE t
(
 c1 VARBINARY(10),
 c2 BLOB,
 c3 ENUM('a','b','c') CHARACTER SET binary
);
```

To see whether MySQL used a data type other than the one you specified, issue a DESCRIBE or SHOW CREATE TABLE statement after creating or altering the table.

Certain other data type changes can occur if you compress a table using myisampack. See Section 18.2.3.3, "Compressed Table Characteristics".

# <span id="page-185-0"></span>**15.1.20.8 CREATE TABLE and Generated Columns**

[CREATE TABLE](#page-145-0) supports the specification of generated columns. Values of a generated column are computed from an expression included in the column definition.

Generated columns are also supported by the NDB storage engine.

The following simple example shows a table that stores the lengths of the sides of right triangles in the sidea and sideb columns, and computes the length of the hypotenuse in sidec (the square root of the sums of the squares of the other sides):

```
CREATE TABLE triangle (
 sidea DOUBLE,
 sideb DOUBLE,
 sidec DOUBLE AS (SQRT(sidea * sidea + sideb * sideb))
);
INSERT INTO triangle (sidea, sideb) VALUES(1,1),(3,4),(6,8);
```

Selecting from the table yields this result:

```
mysql> SELECT * FROM triangle;
+-------+-------+--------------------+
| sidea | sideb | sidec |
+-------+-------+--------------------+
| 1 | 1 | 1.4142135623730951 |
| 3 | 4 | 5 |
| 6 | 8 | 10 |
+-------+-------+--------------------+
```

Any application that uses the triangle table has access to the hypotenuse values without having to specify the expression that calculates them.

Generated column definitions have this syntax:

```
col_name data_type [GENERATED ALWAYS] AS (expr)
 [VIRTUAL | STORED] [NOT NULL | NULL]
 [UNIQUE [KEY]] [[PRIMARY] KEY]
 [COMMENT 'string']
```

AS (expr) indicates that the column is generated and defines the expression used to compute column values. AS may be preceded by GENERATED ALWAYS to make the generated nature of the column more explicit. Constructs that are permitted or prohibited in the expression are discussed later.

The VIRTUAL or STORED keyword indicates how column values are stored, which has implications for column use:

• VIRTUAL: Column values are not stored, but are evaluated when rows are read, immediately after any BEFORE triggers. A virtual column takes no storage.

InnoDB supports secondary indexes on virtual columns. See [Section 15.1.20.9, "Secondary Indexes](#page-188-0) [and Generated Columns"](#page-188-0).

• STORED: Column values are evaluated and stored when rows are inserted or updated. A stored column does require storage space and can be indexed.

The default is VIRTUAL if neither keyword is specified.

It is permitted to mix VIRTUAL and STORED columns within a table.

Other attributes may be given to indicate whether the column is indexed or can be NULL, or provide a comment.

Generated column expressions must adhere to the following rules. An error occurs if an expression contains disallowed constructs.

- Literals, deterministic built-in functions, and operators are permitted. A function is deterministic if, given the same data in tables, multiple invocations produce the same result, independently of the connected user. Examples of functions that are nondeterministic and fail this definition: CONNECTION\_ID(), CURRENT\_USER(), NOW().
- Stored functions and loadable functions are not permitted.
- Stored procedure and function parameters are not permitted.
- Variables (system variables, user-defined variables, and stored program local variables) are not permitted.
- Subqueries are not permitted.
- A generated column definition can refer to other generated columns, but only those occurring earlier in the table definition. A generated column definition can refer to any base (nongenerated) column in the table whether its definition occurs earlier or later.
- The AUTO\_INCREMENT attribute cannot be used in a generated column definition.
- An AUTO\_INCREMENT column cannot be used as a base column in a generated column definition.
- If expression evaluation causes truncation or provides incorrect input to a function, the [CREATE](#page-145-0) [TABLE](#page-145-0) statement terminates with an error and the DDL operation is rejected.

If the expression evaluates to a data type that differs from the declared column type, implicit coercion to the declared type occurs according to the usual MySQL type-conversion rules. See Section 14.3, "Type Conversion in Expression Evaluation".

If a generated column uses the TIMESTAMP data type, the setting for explicit\_defaults\_for\_timestamp is ignored. In such cases, if this variable is disabled then NULL is not converted to CURRENT\_TIMESTAMP. If the column is also declared as NOT NULL, attempting to insert NULL is explicitly rejected with [ER\\_BAD\\_NULL\\_ERROR](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_bad_null_error).

![](_page_187_Picture_2.jpeg)

#### **Note**

Expression evaluation uses the SQL mode in effect at evaluation time. If any component of the expression depends on the SQL mode, different results may occur for different uses of the table unless the SQL mode is the same during all uses.

For [CREATE TABLE ... LIKE](#page-171-0), the destination table preserves generated column information from the original table.

For [CREATE TABLE ... SELECT](#page-172-0), the destination table does not preserve information about whether columns in the selected-from table are generated columns. The SELECT part of the statement cannot assign values to generated columns in the destination table.

Partitioning by generated columns is permitted. See [Table Partitioning.](#page-164-0)

A foreign key constraint on a stored generated column cannot use CASCADE, SET NULL, or SET DEFAULT as ON UPDATE referential actions, nor can it use SET NULL or SET DEFAULT as ON DELETE referential actions.

A foreign key constraint on the base column of a stored generated column cannot use CASCADE, SET NULL, or SET DEFAULT as ON UPDATE or ON DELETE referential actions.

A foreign key constraint cannot reference a virtual generated column.

Triggers cannot use NEW.col\_name or use OLD.col\_name to refer to generated columns.

For INSERT, REPLACE, and UPDATE, if a generated column is inserted into, replaced, or updated explicitly, the only permitted value is DEFAULT.

A generated column in a view is considered updatable because it is possible to assign to it. However, if such a column is updated explicitly, the only permitted value is DEFAULT.

Generated columns have several use cases, such as these:

- Virtual generated columns can be used as a way to simplify and unify queries. A complicated condition can be defined as a generated column and referred to from multiple queries on the table to ensure that all of them use exactly the same condition.
- Stored generated columns can be used as a materialized cache for complicated conditions that are costly to calculate on the fly.
- Generated columns can simulate functional indexes: Use a generated column to define a functional expression and index it. This can be useful for working with columns of types that cannot be indexed directly, such as JSON columns; see [Indexing a Generated Column to Provide a JSON Column](#page-188-1) [Index](#page-188-1), for a detailed example.

For stored generated columns, the disadvantage of this approach is that values are stored twice; once as the value of the generated column and once in the index.

• If a generated column is indexed, the optimizer recognizes query expressions that match the column definition and uses indexes from the column as appropriate during query execution, even if a query does not refer to the column directly by name. For details, see Section 10.3.11, "Optimizer Use of Generated Column Indexes".

Example:

Suppose that a table t1 contains first\_name and last\_name columns and that applications frequently construct the full name using an expression like this:

```
SELECT CONCAT(first_name,' ',last_name) AS full_name FROM t1;
```

One way to avoid writing out the expression is to create a view v1 on t1, which simplifies applications by enabling them to select full\_name directly without using an expression:

```
CREATE VIEW v1 AS
SELECT *, CONCAT(first_name,' ',last_name) AS full_name FROM t1;
SELECT full_name FROM v1;
```

A generated column also enables applications to select full\_name directly without the need to define a view:

```
CREATE TABLE t1 (
 first_name VARCHAR(10),
 last_name VARCHAR(10),
 full_name VARCHAR(255) AS (CONCAT(first_name,' ',last_name))
);
SELECT full_name FROM t1;
```

# <span id="page-188-0"></span>**15.1.20.9 Secondary Indexes and Generated Columns**

InnoDB supports secondary indexes on virtual generated columns. Other index types are not supported. A secondary index defined on a virtual column is sometimes referred to as a "virtual index".

A secondary index may be created on one or more virtual columns or on a combination of virtual columns and regular columns or stored generated columns. Secondary indexes that include virtual columns may be defined as UNIQUE.

When a secondary index is created on a virtual generated column, generated column values are materialized in the records of the index. If the index is a covering index (one that includes all the columns retrieved by a query), generated column values are retrieved from materialized values in the index structure instead of computed "on the fly".

There are additional write costs to consider when using a secondary index on a virtual column due to computation performed when materializing virtual column values in secondary index records during INSERT and UPDATE operations. Even with additional write costs, secondary indexes on virtual columns may be preferable to generated stored columns, which are materialized in the clustered index, resulting in larger tables that require more disk space and memory. If a secondary index is not defined on a virtual column, there are additional costs for reads, as virtual column values must be computed each time the column's row is examined.

Values of an indexed virtual column are MVCC-logged to avoid unnecessary recomputation of generated column values during rollback or during a purge operation. The data length of logged values is limited by the index key limit of 767 bytes for COMPACT and REDUNDANT row formats, and 3072 bytes for DYNAMIC and COMPRESSED row formats.

Adding or dropping a secondary index on a virtual column is an in-place operation.

### <span id="page-188-1"></span>**Indexing a Generated Column to Provide a JSON Column Index**

As noted elsewhere, JSON columns cannot be indexed directly. To create an index that references such a column indirectly, you can define a generated column that extracts the information that should be indexed, then create an index on the generated column, as shown in this example:

```
mysql> CREATE TABLE jemp (
 -> c JSON,
 -> g INT GENERATED ALWAYS AS (c->"$.id"),
 -> INDEX i (g)
 -> );
Query OK, 0 rows affected (0.28 sec)
```

```
mysql> INSERT INTO jemp (c) VALUES
 > ('{"id": "1", "name": "Fred"}'), ('{"id": "2", "name": "Wilma"}'),
 > ('{"id": "3", "name": "Barney"}'), ('{"id": "4", "name": "Betty"}');
Query OK, 4 rows affected (0.04 sec)
Records: 4 Duplicates: 0 Warnings: 0
mysql> SELECT c->>"$.name" AS name
 > FROM jemp WHERE g > 2;
+--------+
| name |
+--------+
| Barney |
| Betty |
+--------+
2 rows in set (0.00 sec)
mysql> EXPLAIN SELECT c->>"$.name" AS name
 > FROM jemp WHERE g > 2\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: jemp
 partitions: NULL
 type: range
possible_keys: i
 key: i
 key_len: 5
 ref: NULL
 rows: 2
 filtered: 100.00
 Extra: Using where
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Note
 Code: 1003
Message: /* select#1 */ select json_unquote(json_extract(`test`.`jemp`.`c`,'$.name'))
AS `name` from `test`.`jemp` where (`test`.`jemp`.`g` > 2)
1 row in set (0.00 sec)
```

(We have wrapped the output from the last statement in this example to fit the viewing area.)

When you use EXPLAIN on a SELECT or other SQL statement containing one or more expressions that use the -> or ->> operator, these expressions are translated into their equivalents using JSON\_EXTRACT() and (if needed) JSON\_UNQUOTE() instead, as shown here in the output from SHOW WARNINGS immediately following this EXPLAIN statement:

```
mysql> EXPLAIN SELECT c->>"$.name"
 > FROM jemp WHERE g > 2 ORDER BY c->"$.name"\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: jemp
 partitions: NULL
 type: range
possible_keys: i
 key: i
 key_len: 5
 ref: NULL
 rows: 2
 filtered: 100.00
 Extra: Using where; Using filesort
1 row in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Note
 Code: 1003
Message: /* select#1 */ select json_unquote(json_extract(`test`.`jemp`.`c`,'$.name')) AS
```

```
`c->>"$.name"` from `test`.`jemp` where (`test`.`jemp`.`g` > 2) order by
json_extract(`test`.`jemp`.`c`,'$.name')
1 row in set (0.00 sec)
```

See the descriptions of the -> and ->> operators, as well as those of the JSON\_EXTRACT() and JSON\_UNQUOTE() functions, for additional information and examples.

This technique also can be used to provide indexes that indirectly reference columns of other types that cannot be indexed directly, such as GEOMETRY columns.

It is also possible to create an index on a JSON column using the JSON\_VALUE() function with an expression that can be used to optimize queries employing the expression. See the description of that function for more information and examples.

### **JSON columns and indirect indexing in NDB Cluster**

 It is also possible to use indirect indexing of JSON columns in MySQL NDB Cluster, subject to the following conditions:

- 1. NDB handles a JSON column value internally as a BLOB. This means that any NDB table having one or more JSON columns must have a primary key, else it cannot be recorded in the binary log.
- 2. The NDB storage engine does not support indexing of virtual columns. Since the default for generated columns is VIRTUAL, you must specify explicitly the generated column to which to apply the indirect index as STORED.

The **CREATE TABLE** statement used to create the table jempn shown here is a version of the jemp table shown previously, with modifications making it compatible with NDB:

```
CREATE TABLE jempn (
 a BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 c JSON DEFAULT NULL,
 g INT GENERATED ALWAYS AS (c->"$.id") STORED,
 INDEX i (g)
) ENGINE=NDB;
```

We can populate this table using the following INSERT statement:

```
INSERT INTO jempn (c) VALUES
 ('{"id": "1", "name": "Fred"}'),
 ('{"id": "2", "name": "Wilma"}'),
 ('{"id": "3", "name": "Barney"}'),
 ('{"id": "4", "name": "Betty"}');
```

Now NDB can use index i, as shown here:

```
mysql> EXPLAIN SELECT c->>"$.name" AS name
 -> FROM jempn WHERE g > 2\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: jempn
 partitions: p0,p1,p2,p3
 type: range
possible_keys: i
 key: i
 key_len: 5
 ref: NULL
 rows: 3
 filtered: 100.00
 Extra: Using pushed condition (`test`.`jempn`.`g` > 2)
1 row in set, 1 warning (0.01 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Note
 Code: 1003
Message: /* select#1 */ select
```

```
json_unquote(json_extract(`test`.`jempn`.`c`,'$.name')) AS `name` from
`test`.`jempn` where (`test`.`jempn`.`g` > 2) 
1 row in set (0.00 sec)
```

You should keep in mind that a stored generated column, as well as any index on such a column, uses DataMemory.

# <span id="page-191-0"></span>**15.1.20.10 Invisible Columns**

MySQL 8.4 supports invisible columns. An invisible column is normally hidden to queries, but can be accessed if explicitly referenced.

As an illustration of when invisible columns may be useful, suppose that an application uses SELECT \* queries to access a table, and must continue to work without modification even if the table is altered to add a new column that the application does not expect to be there. In a SELECT \* query, the \* evaluates to all table columns, except those that are invisible, so the solution is to add the new column as an invisible column. The column remains "hidden" from SELECT \* queries, and the application continues to work as previously. A newer version of the application can refer to the invisible column if necessary by explicitly referencing it.

The following sections detail how MySQL treats invisible columns.

- [DDL Statements and Invisible Columns](#page-191-1)
- [DML Statements and Invisible Columns](#page-192-0)
- [Invisible Column Metadata](#page-193-0)
- [The Binary Log and Invisible Columns](#page-194-0)

# <span id="page-191-1"></span>**DDL Statements and Invisible Columns**

Columns are visible by default. To explicitly specify visibility for a new column, use a VISIBLE or INVISIBLE keyword as part of the column definition for [CREATE TABLE](#page-145-0) or [ALTER TABLE](#page-88-1):

```
CREATE TABLE t1 (
 i INT,
 j DATE INVISIBLE
) ENGINE = InnoDB;
ALTER TABLE t1 ADD COLUMN k INT INVISIBLE;
```

To alter the visibility of an existing column, use a VISIBLE or INVISIBLE keyword with one of the ALTER TABLE column-modification clauses:

```
ALTER TABLE t1 CHANGE COLUMN j j DATE VISIBLE;
ALTER TABLE t1 MODIFY COLUMN j DATE INVISIBLE;
ALTER TABLE t1 ALTER COLUMN j SET VISIBLE;
```

A table must have at least one visible column. Attempting to make all columns invisible produces an error.

Invisible columns support the usual column attributes: NULL, NOT NULL, AUTO\_INCREMENT, and so forth.

Generated columns can be invisible.

Index definitions can name invisible columns, including definitions for PRIMARY KEY and UNIQUE indexes. Although a table must have at least one visible column, an index definition need not have any visible columns.

An invisible column dropped from a table is dropped in the usual way from any index definition that names the column.

Foreign key constraints can be defined on invisible columns, and foreign key constraints can reference invisible columns.

CHECK constraints can be defined on invisible columns. For new or modified rows, violation of a CHECK constraint on an invisible column produces an error.

CREATE TABLE ... LIKE includes invisible columns, and they are invisible in the new table.

CREATE TABLE ... SELECT does not include invisible columns, unless they are explicitly referenced in the SELECT part. However, even if explicitly referenced, a column that is invisible in the existing table is visible in the new table:

```
mysql> CREATE TABLE t1 (col1 INT, col2 INT INVISIBLE);
mysql> CREATE TABLE t2 AS SELECT col1, col2 FROM t1;
mysql> SHOW CREATE TABLE t2\G
************************************
```

If invisibility should be preserved, provide a definition for the invisible column in the CREATE TABLE part of the CREATE TABLE ... SELECT statement:

```
mysql> CREATE TABLE t1 (col1 INT, col2 INT INVISIBLE);
mysql> CREATE TABLE t2 (col2 INT INVISIBLE) AS SELECT col1, col2 FROM t1;
mysql> SHOW CREATE TABLE t2\G
************************************
```

Views can refer to invisible columns by explicitly referencing them in the SELECT statement that defines the view. Changing a column's visibility subsequent to defining a view that references the column does not change view behavior.

#### <span id="page-192-0"></span>**DML Statements and Invisible Columns**

For SELECT statements, an invisible column is not part of the result set unless explicitly referenced in the select list. In a select list, the \* and tbl\_name.\* shorthands do not include invisible columns. Natural joins do not include invisible columns.

Consider the following statement sequence:

```
mysql> CREATE TABLE t1 (col1 INT, col2 INT INVISIBLE);
mysql> INSERT INTO t1 (col1, col2) VALUES(1, 2), (3, 4);

mysql> SELECT * FROM t1;
+----+
| col1 |
+----+
| 1 |
| 3 |
+----+
| col1 | col2 |
+----+
| col1 | col2 |
+-----+
| 1 | 2 |
| 3 | 4 |
+-----+
```

The first SELECT does not reference the invisible column col2 in the select list (because \* does not include invisible columns), so col2 does not appear in the statement result. The second SELECT explicitly references col2, so the column appears in the result.

The statement TABLE t1 produces the same output as the first SELECT statement. Since there is no way to specify columns in a TABLE statement, TABLE never displays invisible columns.

For statements that create new rows, an invisible column is assigned its implicit default value unless explicitly referenced and assigned a value. For information about implicit defaults, see Implicit Default Handling.

For INSERT (and REPLACE, for non-replaced rows), implicit default assignment occurs with a missing column list, an empty column list, or a nonempty column list that does not include the invisible column:

```
CREATE TABLE t1 (col1 INT, col2 INT INVISIBLE);
INSERT INTO t1 VALUES(...);
INSERT INTO t1 () VALUES(...);
INSERT INTO t1 (col1) VALUES(...);
```

For the first two INSERT statements, the VALUES() list must provide a value for each visible column and no invisible column. For the third INSERT statement, the VALUES() list must provide the same number of values as the number of named columns; the same is true when you use VALUES ROW() rather than VALUES().

For LOAD DATA and LOAD XML, implicit default assignment occurs with a missing column list or a nonempty column list that does not include the invisible column. Input rows should not include a value for the invisible column.

To assign a value other than the implicit default for the preceding statements, explicitly name the invisible column in the column list and provide a value for it.

INSERT INTO ... SELECT \* and REPLACE INTO ... SELECT \* do not include invisible columns because \* does not include invisible columns. Implicit default assignment occurs as described previously.

For statements that insert or ignore new rows, or that replace or modify existing rows, based on values in a PRIMARY KEY or UNIQUE index, MySQL treats invisible columns the same as visible columns: Invisible columns participate in key value comparisons. Specifically, if a new row has the same value as an existing row for a unique key value, these behaviors occur whether the index columns are visible or invisible:

- With the IGNORE modifier, INSERT, LOAD DATA, and LOAD XML ignore the new row.
- REPLACE replaces the existing row with the new row. With the REPLACE modifier, LOAD DATA and LOAD XML do the same.
- INSERT ... ON DUPLICATE KEY UPDATE updates the existing row.

To update invisible columns for UPDATE statements, name them and assign a value, just as for visible columns.

### <span id="page-193-0"></span>**Invisible Column Metadata**

Information about whether a column is visible or invisible is available from the EXTRA column of the Information Schema COLUMNS table or SHOW COLUMNS output. For example:

```
mysql> SELECT TABLE_NAME, COLUMN_NAME, EXTRA
 FROM INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_SCHEMA = 'test' AND TABLE_NAME = 't1';
+------------+-------------+-----------+
| TABLE_NAME | COLUMN_NAME | EXTRA |
+------------+-------------+-----------+
| t1 | i | |
| t1 | j | |
| t1 | k | INVISIBLE |
+------------+-------------+-----------+
```

Columns are visible by default, so in that case, EXTRA displays no visibility information. For invisible columns, EXTRA displays INVISIBLE.

SHOW CREATE TABLE displays invisible columns in the table definition, with the INVISIBLE keyword in a version-specific comment:

```
mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
 Table: t1
Create Table: CREATE TABLE `t1` (
 `i` int DEFAULT NULL,
 `j` int DEFAULT NULL,
 `k` int DEFAULT NULL /*!80023 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

mysqldump uses SHOW CREATE TABLE, so they include invisible columns in dumped table definitions. They also include invisible column values in dumped data.

Reloading a dump file into an older version of MySQL that does not support invisible columns causes the version-specific comment to be ignored, which creates any invisible columns as visible.

# <span id="page-194-0"></span>**The Binary Log and Invisible Columns**

MySQL treats invisible columns as follows with respect to events in the binary log:

- Table-creation events include the INVISIBLE attribute for invisible columns.
- Invisible columns are treated like visible columns in row events. They are included if needed according to the binlog\_row\_image system variable setting.
- When row events are applied, invisible columns are treated like visible columns in row events.
- Invisible columns are treated like visible columns when computing writesets. In particular, writesets include indexes defined on invisible columns.
- The mysqlbinlog command includes visibility in column metadata.