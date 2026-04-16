---
source: MySQL 5.7 Reference
title: 00_Overview
---

Depending on the details of your tables, columns, indexes, and the conditions in your WHERE clause, the MySQL optimizer considers many techniques to efficiently perform the lookups involved in an SQL query. A query on a huge table can be performed without reading all the rows; a join involving several tables can be performed without comparing every combination of rows. The set of operations that the optimizer chooses to perform the most efficient query is called the "query execution plan", also known as the EXPLAIN plan. Your goals are to recognize the aspects of the EXPLAIN plan that indicate a query is optimized well, and to learn the SQL syntax and indexing techniques to improve the plan if you see some inefficient operations.

## <span id="page-68-0"></span>**8.8.1 Optimizing Queries with EXPLAIN**

The EXPLAIN statement provides information about how MySQL executes statements:

- EXPLAIN works with SELECT, DELETE, INSERT, REPLACE, and UPDATE statements.
- When EXPLAIN is used with an explainable statement, MySQL displays information from the optimizer about the statement execution plan. That is, MySQL explains how it would process the statement, including information about how tables are joined and in which order. For information about using EXPLAIN to obtain execution plan information, see [Section 8.8.2, "EXPLAIN Output](#page-69-0) [Format"](#page-69-0).
- When EXPLAIN is used with FOR CONNECTION connection\_id rather than an explainable statement, it displays the execution plan for the statement executing in the named connection. See [Section 8.8.4, "Obtaining Execution Plan Information for a Named Connection".](#page-84-0)
- For SELECT statements, EXPLAIN produces additional execution plan information that can be displayed using SHOW WARNINGS. See [Section 8.8.3, "Extended EXPLAIN Output Format".](#page-82-0)
- EXPLAIN is useful for examining queries involving partitioned tables. See Section 22.3.5, "Obtaining Information About Partitions".
- The FORMAT option can be used to select the output format. TRADITIONAL presents the output in tabular format. This is the default if no FORMAT option is present. JSON format displays the information in JSON format.

 With the help of EXPLAIN, you can see where you should add indexes to tables so that the statement executes faster by using indexes to find rows. You can also use EXPLAIN to check whether the optimizer joins the tables in an optimal order. To give a hint to the optimizer to use a join order corresponding to the order in which the tables are named in a SELECT statement, begin the statement with SELECT STRAIGHT\_JOIN rather than just SELECT. (See Section 13.2.9, "SELECT Statement".)

However, STRAIGHT\_JOIN may prevent indexes from being used because it disables semijoin transformations. See [Section 8.2.2.1, "Optimizing Subqueries, Derived Tables, and View References](#page-13-1) [with Semijoin Transformations"](#page-13-1).

The optimizer trace may sometimes provide information complementary to that of EXPLAIN. However, the optimizer trace format and content are subject to change between versions. For details, see [Section 8.15, "Tracing the Optimizer"](#page-151-0).

If you have a problem with indexes not being used when you believe that they should be, run ANALYZE TABLE to update table statistics, such as cardinality of keys, that can affect the choices the optimizer makes. See Section 13.7.2.1, "ANALYZE TABLE Statement".

![](_page_69_Picture_4.jpeg)

#### **Note**

EXPLAIN can also be used to obtain information about the columns in a table. EXPLAIN tbl\_name is synonymous with DESCRIBE tbl\_name and SHOW COLUMNS FROM tbl\_name. For more information, see Section 13.8.1, "DESCRIBE Statement", and Section 13.7.5.5, "SHOW COLUMNS Statement".

## <span id="page-69-0"></span>**8.8.2 EXPLAIN Output Format**

The EXPLAIN statement provides information about how MySQL executes statements. EXPLAIN works with SELECT, DELETE, INSERT, REPLACE, and UPDATE statements.

EXPLAIN returns a row of information for each table used in the SELECT statement. It lists the tables in the output in the order that MySQL would read them while processing the statement. MySQL resolves all joins using a nested-loop join method. This means that MySQL reads a row from the first table, and then finds a matching row in the second table, the third table, and so on. When all tables are processed, MySQL outputs the selected columns and backtracks through the table list until a table is found for which there are more matching rows. The next row is read from this table and the process continues with the next table.

EXPLAIN output includes partition information. Also, for SELECT statements, EXPLAIN generates extended information that can be displayed with SHOW WARNINGS following the EXPLAIN (see [Section 8.8.3, "Extended EXPLAIN Output Format"](#page-82-0)).

![](_page_69_Picture_11.jpeg)

#### **Note**

In older MySQL releases, partition and extended information was produced using EXPLAIN PARTITIONS and EXPLAIN EXTENDED. Those syntaxes are still recognized for backward compatibility but partition and extended output is now enabled by default, so the PARTITIONS and EXTENDED keywords are superfluous and deprecated. Their use results in a warning; expect them to be removed from EXPLAIN syntax in a future MySQL release.

You cannot use the deprecated PARTITIONS and EXTENDED keywords together in the same EXPLAIN statement. In addition, neither of these keywords can be used together with the FORMAT option.

![](_page_69_Picture_15.jpeg)

### **Note**

MySQL Workbench has a Visual Explain capability that provides a visual representation of EXPLAIN output. See [Tutorial: Using Explain to Improve](https://dev.mysql.com/doc/workbench/en/wb-tutorial-visual-explain-dbt3.md) [Query Performance](https://dev.mysql.com/doc/workbench/en/wb-tutorial-visual-explain-dbt3.md).

- [EXPLAIN Output Columns](#page-70-0)
- [EXPLAIN Join Types](#page-73-2)
- [EXPLAIN Extra Information](#page-75-2)

### • [EXPLAIN Output Interpretation](#page-80-0)

### <span id="page-70-0"></span>**EXPLAIN Output Columns**

This section describes the output columns produced by EXPLAIN. Later sections provide additional information about the [type](#page-73-2) and [Extra](#page-75-2) columns.

Each output row from EXPLAIN provides information about one table. Each row contains the values summarized in [Table 8.1, "EXPLAIN Output Columns",](#page-70-1) and described in more detail following the table. Column names are shown in the table's first column; the second column provides the equivalent property name shown in the output when FORMAT=JSON is used.

**Table 8.1 EXPLAIN Output Columns**

<span id="page-70-1"></span>

| Column        | JSON Name     | Meaning                                           |
|---------------|---------------|---------------------------------------------------|
| id            | select_id     | The SELECT identifier                             |
| select_type   | None          | The SELECT type                                   |
| table         | table_name    | The table for the output row                      |
| partitions    | partitions    | The matching partitions                           |
| type          | access_type   | The join type                                     |
| possible_keys | possible_keys | The possible indexes to choose                    |
| key           | key           | The index actually chosen                         |
| key_len       | key_length    | The length of the chosen key                      |
| ref           | ref           | The columns compared to the<br>index              |
| rows          | rows          | Estimate of rows to be examined                   |
| filtered      | filtered      | Percentage of rows filtered by<br>table condition |
| Extra         | None          | Additional information                            |

![](_page_70_Picture_7.jpeg)

#### **Note**

JSON properties which are NULL are not displayed in JSON-formatted EXPLAIN output.

<span id="page-70-2"></span>• id (JSON name: select\_id)

The SELECT identifier. This is the sequential number of the SELECT within the query. The value can be NULL if the row refers to the union result of other rows. In this case, the table column shows a value like <unionM,N> to indicate that the row refers to the union of the rows with id values of M and N.

<span id="page-70-3"></span>• select\_type (JSON name: none)

The type of SELECT, which can be any of those shown in the following table. A JSON-formatted EXPLAIN exposes the SELECT type as a property of a query\_block, unless it is SIMPLE or PRIMARY. The JSON names (where applicable) are also shown in the table.

| select_type Value | JSON Name | Meaning                                          |
|-------------------|-----------|--------------------------------------------------|
| SIMPLE            | None      | Simple SELECT (not using<br>UNION or subqueries) |
| PRIMARY           | None      | Outermost SELECT                                 |
| UNION             | None      | Second or later SELECT<br>statement in a UNION   |

| select_type Value    | JSON Name                                       | Meaning                                                                                                            |
|----------------------|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| DEPENDENT UNION      | dependent (true)                                | Second or later SELECT<br>statement in a UNION,<br>dependent on outer query                                        |
| UNION RESULT         | union_result                                    | Result of a UNION.                                                                                                 |
| SUBQUERY             | None                                            | First SELECT in subquery                                                                                           |
| DEPENDENT SUBQUERY   | dependent (true)                                | First SELECT in subquery,<br>dependent on outer query                                                              |
| DERIVED              | None                                            | Derived table                                                                                                      |
| MATERIALIZED         | materialized_from_subqueryMaterialized subquery |                                                                                                                    |
| UNCACHEABLE SUBQUERY | cacheable (false)                               | A subquery for which the result<br>cannot be cached and must be<br>re-evaluated for each row of the<br>outer query |
| UNCACHEABLE UNION    | cacheable (false)                               | The second or later select in<br>a UNION that belongs to an<br>uncacheable subquery (see<br>UNCACHEABLE SUBQUERY)  |

DEPENDENT typically signifies the use of a correlated subquery. See Section 13.2.10.7, "Correlated Subqueries".

DEPENDENT SUBQUERY evaluation differs from UNCACHEABLE SUBQUERY evaluation. For DEPENDENT SUBQUERY, the subquery is re-evaluated only once for each set of different values of the variables from its outer context. For UNCACHEABLE SUBQUERY, the subquery is re-evaluated for each row of the outer context.

Cacheability of subqueries differs from caching of query results in the query cache (which is described in [Section 8.10.3.1, "How the Query Cache Operates"](#page-107-0)). Subquery caching occurs during query execution, whereas the query cache is used to store results only after query execution finishes.

When you specify FORMAT=JSON with EXPLAIN, the output has no single property directly equivalent to select\_type; the query\_block property corresponds to a given SELECT. Properties equivalent to most of the SELECT subquery types just shown are available (an example being materialized\_from\_subquery for MATERIALIZED), and are displayed when appropriate. There are no JSON equivalents for SIMPLE or PRIMARY.

The select\_type value for non-SELECT statements displays the statement type for affected tables. For example, select\_type is DELETE for DELETE statements.

<span id="page-71-0"></span>• table (JSON name: table\_name)

The name of the table to which the row of output refers. This can also be one of the following values:

- <unionM,N>: The row refers to the union of the rows with id values of M and N.
- <derivedN>: The row refers to the derived table result for the row with an id value of N. A derived table may result, for example, from a subquery in the FROM clause.
- <subqueryN>: The row refers to the result of a materialized subquery for the row with an id value of N. See [Section 8.2.2.2, "Optimizing Subqueries with Materialization".](#page-16-0)
- <span id="page-71-1"></span>• partitions (JSON name: partitions)

The partitions from which records would be matched by the query. The value is NULL for nonpartitioned tables. See Section 22.3.5, "Obtaining Information About Partitions".

<span id="page-72-0"></span>• type (JSON name: access\_type)

The join type. For descriptions of the different types, see EXPLAIN [Join Types.](#page-73-2)

<span id="page-72-1"></span>• possible\_keys (JSON name: possible\_keys)

The possible\_keys column indicates the indexes from which MySQL can choose to find the rows in this table. Note that this column is totally independent of the order of the tables as displayed in the output from EXPLAIN. That means that some of the keys in possible\_keys might not be usable in practice with the generated table order.

If this column is NULL (or undefined in JSON-formatted output), there are no relevant indexes. In this case, you may be able to improve the performance of your query by examining the WHERE clause to check whether it refers to some column or columns that would be suitable for indexing. If so, create an appropriate index and check the query with EXPLAIN again. See Section 13.1.8, "ALTER TABLE Statement".

To see what indexes a table has, use SHOW INDEX FROM tbl\_name.

<span id="page-72-2"></span>• key (JSON name: key)

The key column indicates the key (index) that MySQL actually decided to use. If MySQL decides to use one of the possible\_keys indexes to look up rows, that index is listed as the key value.

It is possible for key to name an index that is not present in the possible\_keys value. This can happen if none of the possible\_keys indexes are suitable for looking up rows, but all the columns selected by the query are columns of some other index. That is, the named index covers the selected columns, so although it is not used to determine which rows to retrieve, an index scan is more efficient than a data row scan.

For InnoDB, a secondary index might cover the selected columns even if the query also selects the primary key because InnoDB stores the primary key value with each secondary index. If key is NULL, MySQL found no index to use for executing the query more efficiently.

To force MySQL to use or ignore an index listed in the possible\_keys column, use FORCE INDEX, USE INDEX, or IGNORE INDEX in your query. See [Section 8.9.4, "Index Hints"](#page-96-0).

For MyISAM tables, running ANALYZE TABLE helps the optimizer choose better indexes. For MyISAM tables, myisamchk --analyze does the same. See Section 13.7.2.1, "ANALYZE TABLE Statement", and Section 7.6, "MyISAM Table Maintenance and Crash Recovery".

<span id="page-72-3"></span>• key\_len (JSON name: key\_length)

The key\_len column indicates the length of the key that MySQL decided to use. The value of key\_len enables you to determine how many parts of a multiple-part key MySQL actually uses. If the key column says NULL, the key\_len column also says NULL.

Due to the key storage format, the key length is one greater for a column that can be NULL than for a NOT NULL column.

<span id="page-72-4"></span>• ref (JSON name: ref)

The ref column shows which columns or constants are compared to the index named in the key column to select rows from the table.

If the value is func, the value used is the result of some function. To see which function, use SHOW WARNINGS following EXPLAIN to see the extended EXPLAIN output. The function might actually be an operator such as an arithmetic operator.

<span id="page-73-3"></span>• rows (JSON name: rows)

The rows column indicates the number of rows MySQL believes it must examine to execute the query.

For InnoDB tables, this number is an estimate, and may not always be exact.

<span id="page-73-4"></span>• filtered (JSON name: filtered)

The filtered column indicates an estimated percentage of table rows filtered by the table condition. The maximum value is 100, which means no filtering of rows occurred. Values decreasing from 100 indicate increasing amounts of filtering. rows shows the estimated number of rows examined and rows × filtered shows the number of rows joined with the following table. For example, if rows is 1000 and filtered is 50.00 (50%), the number of rows to be joined with the following table is 1000 × 50% = 500.

<span id="page-73-5"></span>• Extra (JSON name: none)

This column contains additional information about how MySQL resolves the query. For descriptions of the different values, see EXPLAIN [Extra Information.](#page-75-2)

There is no single JSON property corresponding to the Extra column; however, values that can occur in this column are exposed as JSON properties, or as the text of the message property.

### <span id="page-73-2"></span>**EXPLAIN Join Types**

The type column of EXPLAIN output describes how tables are joined. In JSON-formatted output, these are found as values of the access\_type property. The following list describes the join types, ordered from the best type to the worst:

<span id="page-73-6"></span>• [system](#page-73-6)

The table has only one row (= system table). This is a special case of the [const](#page-73-0) join type.

<span id="page-73-0"></span>• [const](#page-73-0)

The table has at most one matching row, which is read at the start of the query. Because there is only one row, values from the column in this row can be regarded as constants by the rest of the optimizer. [const](#page-73-0) tables are very fast because they are read only once.

[const](#page-73-0) is used when you compare all parts of a PRIMARY KEY or UNIQUE index to constant values. In the following queries, tbl\_name can be used as a [const](#page-73-0) table:

```
SELECT * FROM tbl_name WHERE primary_key=1;
SELECT * FROM tbl_name
 WHERE primary_key_part1=1 AND primary_key_part2=2;
```

<span id="page-73-1"></span>• [eq\\_ref](#page-73-1)

One row is read from this table for each combination of rows from the previous tables. Other than the [system](#page-73-6) and [const](#page-73-0) types, this is the best possible join type. It is used when all parts of an index are used by the join and the index is a PRIMARY KEY or UNIQUE NOT NULL index.

[eq\\_ref](#page-73-1) can be used for indexed columns that are compared using the = operator. The comparison value can be a constant or an expression that uses columns from tables that are read before this table. In the following examples, MySQL can use an [eq\\_ref](#page-73-1) join to process ref\_table:

```
SELECT * FROM ref_table,other_table
 WHERE ref_table.key_column=other_table.column;
SELECT * FROM ref_table,other_table
 WHERE ref_table.key_column_part1=other_table.column
 AND ref_table.key_column_part2=1;
```

<span id="page-74-3"></span>• [ref](#page-74-3)

All rows with matching index values are read from this table for each combination of rows from the previous tables. [ref](#page-74-3) is used if the join uses only a leftmost prefix of the key or if the key is not a PRIMARY KEY or UNIQUE index (in other words, if the join cannot select a single row based on the key value). If the key that is used matches only a few rows, this is a good join type.

[ref](#page-74-3) can be used for indexed columns that are compared using the = or <=> operator. In the following examples, MySQL can use a [ref](#page-74-3) join to process ref\_table:

```
SELECT * FROM ref_table WHERE key_column=expr;
SELECT * FROM ref_table,other_table
 WHERE ref_table.key_column=other_table.column;
SELECT * FROM ref_table,other_table
 WHERE ref_table.key_column_part1=other_table.column
 AND ref_table.key_column_part2=1;
```

<span id="page-74-4"></span>• [fulltext](#page-74-4)

The join is performed using a FULLTEXT index.

<span id="page-74-0"></span>• [ref\\_or\\_null](#page-74-0)

This join type is like [ref](#page-74-3), but with the addition that MySQL does an extra search for rows that contain NULL values. This join type optimization is used most often in resolving subqueries. In the following examples, MySQL can use a [ref\\_or\\_null](#page-74-0) join to process ref\_table:

```
SELECT * FROM ref_table
 WHERE key_column=expr OR key_column IS NULL;
```

See [Section 8.2.1.13, "IS NULL Optimization"](#page-0-1).

<span id="page-74-5"></span>• [index\\_merge](#page-74-5)

This join type indicates that the Index Merge optimization is used. In this case, the key column in the output row contains a list of indexes used, and key\_len contains a list of the longest key parts for the indexes used. For more information, see Section 8.2.1.3, "Index Merge Optimization".

<span id="page-74-1"></span>• [unique\\_subquery](#page-74-1)

This type replaces [eq\\_ref](#page-73-1) for some IN subqueries of the following form:

```
value IN (SELECT primary_key FROM single_table WHERE some_expr)
```

[unique\\_subquery](#page-74-1) is just an index lookup function that replaces the subquery completely for better efficiency.

<span id="page-74-2"></span>• [index\\_subquery](#page-74-2)

This join type is similar to [unique\\_subquery](#page-74-1). It replaces IN subqueries, but it works for nonunique indexes in subqueries of the following form:

```
value IN (SELECT key_column FROM single_table WHERE some_expr)
```

#### <span id="page-75-0"></span>• [range](#page-75-0)

Only rows that are in a given range are retrieved, using an index to select the rows. The key column in the output row indicates which index is used. The key\_len contains the longest key part that was used. The ref column is NULL for this type.

[range](#page-75-0) can be used when a key column is compared to a constant using any of the =, <>, >, >=, <, <=, IS NULL, <=>, BETWEEN, LIKE, or IN() operators:

```
SELECT * FROM tbl_name
 WHERE key_column = 10;
SELECT * FROM tbl_name
 WHERE key_column BETWEEN 10 and 20;
SELECT * FROM tbl_name
 WHERE key_column IN (10,20,30);
SELECT * FROM tbl_name
 WHERE key_part1 = 10 AND key_part2 IN (10,20,30);
```

#### <span id="page-75-3"></span>• [index](#page-75-3)

The index join type is the same as [ALL](#page-75-1), except that the index tree is scanned. This occurs two ways:

- If the index is a covering index for the queries and can be used to satisfy all data required from the table, only the index tree is scanned. In this case, the Extra column says Using index. An index-only scan usually is faster than [ALL](#page-75-1) because the size of the index usually is smaller than the table data.
- A full table scan is performed using reads from the index to look up data rows in index order. Uses index does not appear in the Extra column.

MySQL can use this join type when the query uses only columns that are part of a single index.

<span id="page-75-1"></span>• [ALL](#page-75-1)

A full table scan is done for each combination of rows from the previous tables. This is normally not good if the table is the first table not marked [const](#page-73-0), and usually very bad in all other cases. Normally, you can avoid [ALL](#page-75-1) by adding indexes that enable row retrieval from the table based on constant values or column values from earlier tables.

## <span id="page-75-2"></span>**EXPLAIN Extra Information**

The Extra column of EXPLAIN output contains additional information about how MySQL resolves the query. The following list explains the values that can appear in this column. Each item also indicates for JSON-formatted output which property displays the Extra value. For some of these, there is a specific property. The others display as the text of the message property.

If you want to make your queries as fast as possible, look out for Extra column values of Using filesort and Using temporary, or, in JSON-formatted EXPLAIN output, for using\_filesort and using\_temporary\_table properties equal to true.

• Child of 'table' pushed join@1 (JSON: message text)

This table is referenced as the child of table in a join that can be pushed down to the NDB kernel. Applies only in NDB Cluster, when pushed-down joins are enabled. See the description of the ndb\_join\_pushdown server system variable for more information and examples.

• const row not found (JSON property: const\_row\_not\_found)

For a query such as SELECT ... FROM tbl\_name, the table was empty.

• Deleting all rows (JSON property: message)

For DELETE, some storage engines (such as MyISAM) support a handler method that removes all table rows in a simple and fast way. This Extra value is displayed if the engine uses this optimization.

• Distinct (JSON property: distinct)

MySQL is looking for distinct values, so it stops searching for more rows for the current row combination after it has found the first matching row.

• FirstMatch(tbl\_name) (JSON property: first\_match)

The semijoin FirstMatch join shortcutting strategy is used for tbl\_name.

• Full scan on NULL key (JSON property: message)

This occurs for subquery optimization as a fallback strategy when the optimizer cannot use an indexlookup access method.

• Impossible HAVING (JSON property: message)

The HAVING clause is always false and cannot select any rows.

• Impossible WHERE (JSON property: message)

The WHERE clause is always false and cannot select any rows.

• Impossible WHERE noticed after reading const tables (JSON property: message)

MySQL has read all [const](#page-73-0) (and [system](#page-73-6)) tables and notice that the WHERE clause is always false.

• LooseScan(m..n) (JSON property: message)

The semijoin LooseScan strategy is used. m and n are key part numbers.

• No matching min/max row (JSON property: message)

No row satisfies the condition for a query such as SELECT MIN(...) FROM ... WHERE condition.

• no matching row in const table (JSON property: message)

For a query with a join, there was an empty table or a table with no rows satisfying a unique index condition.

• No matching rows after partition pruning (JSON property: message)

For DELETE or UPDATE, the optimizer found nothing to delete or update after partition pruning. It is similar in meaning to Impossible WHERE for SELECT statements.

• No tables used (JSON property: message)

The query has no FROM clause, or has a FROM DUAL clause.

For INSERT or REPLACE statements, EXPLAIN displays this value when there is no SELECT part. For example, it appears for EXPLAIN INSERT INTO t VALUES(10) because that is equivalent to EXPLAIN INSERT INTO t SELECT 10 FROM DUAL.

• Not exists (JSON property: message)

MySQL was able to do a LEFT JOIN optimization on the query and does not examine more rows in this table for the previous row combination after it finds one row that matches the LEFT JOIN criteria. Here is an example of the type of query that can be optimized this way:

```
SELECT * FROM t1 LEFT JOIN t2 ON t1.id=t2.id
 WHERE t2.id IS NULL;
```

Assume that t2.id is defined as NOT NULL. In this case, MySQL scans t1 and looks up the rows in t2 using the values of t1.id. If MySQL finds a matching row in t2, it knows that t2.id can never be NULL, and does not scan through the rest of the rows in t2 that have the same id value. In other words, for each row in t1, MySQL needs to do only a single lookup in t2, regardless of how many rows actually match in t2.

• Plan isn't ready yet (JSON property: none)

This value occurs with [EXPLAIN FOR CONNECTION](#page-84-0) when the optimizer has not finished creating the execution plan for the statement executing in the named connection. If execution plan output comprises multiple lines, any or all of them could have this Extra value, depending on the progress of the optimizer in determining the full execution plan.

• Range checked for each record (index map: N) (JSON property: message)

MySQL found no good index to use, but found that some of indexes might be used after column values from preceding tables are known. For each row combination in the preceding tables, MySQL checks whether it is possible to use a [range](#page-75-0) or [index\\_merge](#page-74-5) access method to retrieve rows. This is not very fast, but is faster than performing a join with no index at all. The applicability criteria are as described in Section 8.2.1.2, "Range Optimization", and Section 8.2.1.3, "Index Merge Optimization", with the exception that all column values for the preceding table are known and considered to be constants.

Indexes are numbered beginning with 1, in the same order as shown by SHOW INDEX for the table. The index map value N is a bitmask value that indicates which indexes are candidates. For example, a value of 0x19 (binary 11001) means that indexes 1, 4, and 5 are considered.

• Scanned N databases (JSON property: message)

This indicates how many directory scans the server performs when processing a query for INFORMATION\_SCHEMA tables, as described in [Section 8.2.3, "Optimizing](#page-23-0) [INFORMATION\\_SCHEMA Queries"](#page-23-0). The value of N can be 0, 1, or all.

• Select tables optimized away (JSON property: message)

The optimizer determined 1) that at most one row should be returned, and 2) that to produce this row, a deterministic set of rows must be read. When the rows to be read can be read during the optimization phase (for example, by reading index rows), there is no need to read any tables during query execution.

The first condition is fulfilled when the query is implicitly grouped (contains an aggregate function but no GROUP BY clause). The second condition is fulfilled when one row lookup is performed per index used. The number of indexes read determines the number of rows to read.

Consider the following implicitly grouped query:

```
SELECT MIN(c1), MIN(c2) FROM t1;
```

Suppose that MIN(c1) can be retrieved by reading one index row and MIN(c2) can be retrieved by reading one row from a different index. That is, for each column c1 and c2, there exists an index where the column is the first column of the index. In this case, one row is returned, produced by reading two deterministic rows.

This Extra value does not occur if the rows to read are not deterministic. Consider this query:

```
SELECT MIN(c2) FROM t1 WHERE c1 <= 10;
```

Suppose that (c1, c2) is a covering index. Using this index, all rows with c1 <= 10 must be scanned to find the minimum c2 value. By contrast, consider this query:

```
SELECT MIN(c2) FROM t1 WHERE c1 = 10;
```

In this case, the first index row with c1 = 10 contains the minimum c2 value. Only one row must be read to produce the returned row.

For storage engines that maintain an exact row count per table (such as MyISAM, but not InnoDB), this Extra value can occur for COUNT(\*) queries for which the WHERE clause is missing or always true and there is no GROUP BY clause. (This is an instance of an implicitly grouped query where the storage engine influences whether a deterministic number of rows can be read.)

• Skip\_open\_table, Open\_frm\_only, Open\_full\_table (JSON property: message)

These values indicate file-opening optimizations that apply to queries for INFORMATION\_SCHEMA tables, as described in [Section 8.2.3, "Optimizing INFORMATION\\_SCHEMA Queries"](#page-23-0).

- Skip\_open\_table: Table files do not need to be opened. The information has already become available within the query by scanning the database directory.
- Open\_frm\_only: Only the table's .frm file need be opened.
- Open\_full\_table: The unoptimized information lookup. The .frm, .MYD, and .MYI files must be opened.
- Start temporary, End temporary (JSON property: message)

This indicates temporary table use for the semijoin Duplicate Weedout strategy.

• unique row not found (JSON property: message)

For a query such as SELECT ... FROM tbl\_name, no rows satisfy the condition for a UNIQUE index or PRIMARY KEY on the table.

• Using filesort (JSON property: using\_filesort)

MySQL must do an extra pass to find out how to retrieve the rows in sorted order. The sort is done by going through all rows according to the join type and storing the sort key and pointer to the row for all rows that match the WHERE clause. The keys then are sorted and the rows are retrieved in sorted order. See [Section 8.2.1.14, "ORDER BY Optimization".](#page-0-0)

• Using index (JSON property: using\_index)

The column information is retrieved from the table using only information in the index tree without having to do an additional seek to read the actual row. This strategy can be used when the query uses only columns that are part of a single index.

For InnoDB tables that have a user-defined clustered index, that index can be used even when Using index is absent from the Extra column. This is the case if type is [index](#page-75-3) and key is PRIMARY.

• Using index condition (JSON property: using\_index\_condition)

Tables are read by accessing index tuples and testing them first to determine whether to read full table rows. In this way, index information is used to defer ("push down") reading full table rows unless it is necessary. See Section 8.2.1.5, "Index Condition Pushdown Optimization".

• Using index for group-by (JSON property: using\_index\_for\_group\_by)

Similar to the Using index table access method, Using index for group-by indicates that MySQL found an index that can be used to retrieve all columns of a GROUP BY or DISTINCT query without any extra disk access to the actual table. Additionally, the index is used in the most efficient way so that for each group, only a few index entries are read. For details, see [Section 8.2.1.15,](#page-5-1) ["GROUP BY Optimization".](#page-5-1)

• Using join buffer (Block Nested Loop), Using join buffer (Batched Key Access) (JSON property: using\_join\_buffer)

Tables from earlier joins are read in portions into the join buffer, and then their rows are used from the buffer to perform the join with the current table. (Block Nested Loop) indicates use of the Block Nested-Loop algorithm and (Batched Key Access) indicates use of the Batched Key Access algorithm. That is, the keys from the table on the preceding line of the EXPLAIN output are buffered, and the matching rows are fetched in batches from the table represented by the line in which Using join buffer appears.

In JSON-formatted output, the value of using\_join\_buffer is always either one of Block Nested Loop or Batched Key Access.

For more information about these algorithms, see Block Nested-Loop Join Algorithm, and Batched Key Access Joins.

• Using MRR (JSON property: message)

Tables are read using the Multi-Range Read optimization strategy. See Section 8.2.1.10, "Multi-Range Read Optimization".

• Using sort\_union(...), Using union(...), Using intersect(...) (JSON property: message)

These indicate the particular algorithm showing how index scans are merged for the [index\\_merge](#page-74-5) join type. See Section 8.2.1.3, "Index Merge Optimization".

• Using temporary (JSON property: using\_temporary\_table)

To resolve the query, MySQL needs to create a temporary table to hold the result. This typically happens if the query contains GROUP BY and ORDER BY clauses that list columns differently.

• Using where (JSON property: attached\_condition)

A WHERE clause is used to restrict which rows to match against the next table or send to the client. Unless you specifically intend to fetch or examine all rows from the table, you may have something wrong in your query if the Extra value is not Using where and the table join type is [ALL](#page-75-1) or [index](#page-75-3).

Using where has no direct counterpart in JSON-formatted output; the attached\_condition property contains any WHERE condition used.

• Using where with pushed condition (JSON property: message)

This item applies to NDB tables only. It means that NDB Cluster is using the Condition Pushdown optimization to improve the efficiency of a direct comparison between a nonindexed column and a constant. In such cases, the condition is "pushed down" to the cluster's data nodes and is evaluated on all data nodes simultaneously. This eliminates the need to send nonmatching rows over the network, and can speed up such queries by a factor of 5 to 10 times over cases where Condition

Pushdown could be but is not used. For more information, see Section 8.2.1.4, "Engine Condition Pushdown Optimization".

• Zero limit (JSON property: message)

The query had a LIMIT 0 clause and cannot select any rows.

## <span id="page-80-0"></span>**EXPLAIN Output Interpretation**

You can get a good indication of how good a join is by taking the product of the values in the rows column of the EXPLAIN output. This should tell you roughly how many rows MySQL must examine to execute the query. If you restrict queries with the max\_join\_size system variable, this row product also is used to determine which multiple-table SELECT statements to execute and which to abort. See Section 5.1.1, "Configuring the Server".

The following example shows how a multiple-table join can be optimized progressively based on the information provided by EXPLAIN.

Suppose that you have the SELECT statement shown here and that you plan to examine it using EXPLAIN:

```
EXPLAIN SELECT tt.TicketNumber, tt.TimeIn,
 tt.ProjectReference, tt.EstimatedShipDate,
 tt.ActualShipDate, tt.ClientID,
 tt.ServiceCodes, tt.RepetitiveID,
 tt.CurrentProcess, tt.CurrentDPPerson,
 tt.RecordVolume, tt.DPPrinted, et.COUNTRY,
 et_1.COUNTRY, do.CUSTNAME
 FROM tt, et, et AS et_1, do
 WHERE tt.SubmitTime IS NULL
 AND tt.ActualPC = et.EMPLOYID
 AND tt.AssignedPC = et_1.EMPLOYID
 AND tt.ClientID = do.CUSTNMBR;
```

For this example, make the following assumptions:

• The columns being compared have been declared as follows.

| Table | Column     | Data Type |
|-------|------------|-----------|
| tt    | ActualPC   | CHAR(10)  |
| tt    | AssignedPC | CHAR(10)  |
| tt    | ClientID   | CHAR(10)  |
| et    | EMPLOYID   | CHAR(15)  |
| do    | CUSTNMBR   | CHAR(15)  |

• The tables have the following indexes.

| Table | Index                  |
|-------|------------------------|
| tt    | ActualPC               |
| tt    | AssignedPC             |
| tt    | ClientID               |
| et    | EMPLOYID (primary key) |
| do    | CUSTNMBR (primary key) |

• The tt.ActualPC values are not evenly distributed.

Initially, before any optimizations have been performed, the EXPLAIN statement produces the following information:

```
table type possible_keys key key_len ref rows Extra
et ALL PRIMARY NULL NULL NULL 74
do ALL PRIMARY NULL NULL NULL 2135
et_1 ALL PRIMARY NULL NULL NULL 74
tt ALL AssignedPC, NULL NULL NULL 3872
 ClientID,
 ActualPC
 Range checked for each record (index map: 0x23)
```

Because type is [ALL](#page-75-1) for each table, this output indicates that MySQL is generating a Cartesian product of all the tables; that is, every combination of rows. This takes quite a long time, because the product of the number of rows in each table must be examined. For the case at hand, this product is 74 × 2135 × 74 × 3872 = 45,268,558,720 rows. If the tables were bigger, you can only imagine how long it would take.

One problem here is that MySQL can use indexes on columns more efficiently if they are declared as the same type and size. In this context, VARCHAR and CHAR are considered the same if they are declared as the same size. tt.ActualPC is declared as CHAR(10) and et.EMPLOYID is CHAR(15), so there is a length mismatch.

To fix this disparity between column lengths, use ALTER TABLE to lengthen ActualPC from 10 characters to 15 characters:

```
mysql> ALTER TABLE tt MODIFY ActualPC VARCHAR(15);
```

Now tt.ActualPC and et.EMPLOYID are both VARCHAR(15). Executing the EXPLAIN statement again produces this result:

```
table type possible_keys key key_len ref rows Extra
tt ALL AssignedPC, NULL NULL NULL 3872 Using
 ClientID, where
 ActualPC
do ALL PRIMARY NULL NULL NULL 2135
 Range checked for each record (index map: 0x1)
et_1 ALL PRIMARY NULL NULL NULL 74
 Range checked for each record (index map: 0x1)
et eq_ref PRIMARY PRIMARY 15 tt.ActualPC 1
```

This is not perfect, but is much better: The product of the rows values is less by a factor of 74. This version executes in a couple of seconds.

A second alteration can be made to eliminate the column length mismatches for the tt.AssignedPC = et\_1.EMPLOYID and tt.ClientID = do.CUSTNMBR comparisons:

```
mysql> ALTER TABLE tt MODIFY AssignedPC VARCHAR(15),
 MODIFY ClientID VARCHAR(15);
```

After that modification, EXPLAIN produces the output shown here:

```
table type possible_keys key key_len ref rows Extra
et ALL PRIMARY NULL NULL NULL 74
tt ref AssignedPC, ActualPC 15 et.EMPLOYID 52 Using
 ClientID, where
 ActualPC
et_1 eq_ref PRIMARY PRIMARY 15 tt.AssignedPC 1
do eq_ref PRIMARY PRIMARY 15 tt.ClientID 1
```

At this point, the query is optimized almost as well as possible. The remaining problem is that, by default, MySQL assumes that values in the tt.ActualPC column are evenly distributed, and that is not the case for the tt table. Fortunately, it is easy to tell MySQL to analyze the key distribution:

```
mysql> ANALYZE TABLE tt;
```

With the additional index information, the join is perfect and EXPLAIN produces this result:

```
table type possible_keys key key_len ref rows Extra
```

```
tt ALL AssignedPC NULL NULL NULL 3872 Using
 ClientID, where
 ActualPC
et eq_ref PRIMARY PRIMARY 15 tt.ActualPC 1
et_1 eq_ref PRIMARY PRIMARY 15 tt.AssignedPC 1
do eq_ref PRIMARY PRIMARY 15 tt.ClientID 1
```

 The rows column in the output from EXPLAIN is an educated guess from the MySQL join optimizer. Check whether the numbers are even close to the truth by comparing the rows product with the actual number of rows that the query returns. If the numbers are quite different, you might get better performance by using STRAIGHT\_JOIN in your SELECT statement and trying to list the tables in a different order in the FROM clause. (However, STRAIGHT\_JOIN may prevent indexes from being used because it disables semijoin transformations. See [Section 8.2.2.1, "Optimizing Subqueries, Derived](#page-13-1) [Tables, and View References with Semijoin Transformations".](#page-13-1))

It is possible in some cases to execute statements that modify data when EXPLAIN SELECT is used with a subquery; for more information, see Section 13.2.10.8, "Derived Tables".

## <span id="page-82-0"></span>**8.8.3 Extended EXPLAIN Output Format**

For SELECT statements, the EXPLAIN statement produces extra ("extended") information that is not part of EXPLAIN output but can be viewed by issuing a SHOW WARNINGS statement following EXPLAIN. The Message value in SHOW WARNINGS output displays how the optimizer qualifies table and column names in the SELECT statement, what the SELECT looks like after the application of rewriting and optimization rules, and possibly other notes about the optimization process.

The extended information displayable with a SHOW WARNINGS statement following EXPLAIN is produced only for SELECT statements. SHOW WARNINGS displays an empty result for other explainable statements (DELETE, INSERT, REPLACE, and UPDATE).

![](_page_82_Picture_7.jpeg)

### **Note**

In older MySQL releases, extended information was produced using EXPLAIN EXTENDED. That syntax is still recognized for backward compatibility but extended output is now enabled by default, so the EXTENDED keyword is superfluous and deprecated. Its use results in a warning; expect it to be removed from EXPLAIN syntax in a future MySQL release.

Here is an example of extended EXPLAIN output:

```
mysql> EXPLAIN
 SELECT t1.a, t1.a IN (SELECT t2.a FROM t2) FROM t1\G
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 4
 filtered: 100.00
 Extra: Using index
*************************** 2. row ***************************
 id: 2
 select_type: SUBQUERY
 table: t2
 type: index
possible_keys: a
 key: a
 key_len: 5
 ref: NULL
 rows: 3
 filtered: 100.00
 Extra: Using index
```

```
2 rows in set, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Note
 Code: 1003
Message: /* select#1 */ select `test`.`t1`.`a` AS `a`,
 <in_optimizer>(`test`.`t1`.`a`,`test`.`t1`.`a` in
 ( <materialize> (/* select#2 */ select `test`.`t2`.`a`
 from `test`.`t2` where 1 having 1 ),
 <primary_index_lookup>(`test`.`t1`.`a` in
 <temporary table> on <auto_key>
 where ((`test`.`t1`.`a` = `materialized-subquery`.`a`))))) AS `t1.a
 IN (SELECT t2.a FROM t2)` from `test`.`t1`
1 row in set (0.00 sec)
```

Because the statement displayed by SHOW WARNINGS may contain special markers to provide information about query rewriting or optimizer actions, the statement is not necessarily valid SQL and is not intended to be executed. The output may also include rows with Message values that provide additional non-SQL explanatory notes about actions taken by the optimizer.

The following list describes special markers that can appear in the extended output displayed by SHOW WARNINGS:

• <auto\_key>

An automatically generated key for a temporary table.

• <cache>(expr)

The expression (such as a scalar subquery) is executed once and the resulting value is saved in memory for later use. For results consisting of multiple values, a temporary table may be created and you might see <temporary table> instead.

• <exists>(query fragment)

The subquery predicate is converted to an EXISTS predicate and the subquery is transformed so that it can be used together with the EXISTS predicate.

• <in\_optimizer>(query fragment)

This is an internal optimizer object with no user significance.

• <index\_lookup>(query fragment)

The query fragment is processed using an index lookup to find qualifying rows.

• <if>(condition, expr1, expr2)

If the condition is true, evaluate to expr1, otherwise expr2.

• <is\_not\_null\_test>(expr)

A test to verify that the expression does not evaluate to NULL.

• <materialize>(query fragment)

Subquery materialization is used.

• `materialized-subquery`.col\_name

A reference to the column col\_name in an internal temporary table materialized to hold the result from evaluating a subquery.

• <primary\_index\_lookup>(query fragment)

The query fragment is processed using a primary key lookup to find qualifying rows.

• <ref\_null\_helper>(expr)

This is an internal optimizer object with no user significance.

• /\* select#N \*/ select\_stmt

The SELECT is associated with the row in non-extended EXPLAIN output that has an id value of N.

• outer\_tables semi join (inner\_tables)

A semijoin operation. inner\_tables shows the tables that were not pulled out. See [Section 8.2.2.1, "Optimizing Subqueries, Derived Tables, and View References with Semijoin](#page-13-1) [Transformations".](#page-13-1)

• <temporary table>

This represents an internal temporary table created to cache an intermediate result.

When some tables are of [const](#page-73-0) or [system](#page-73-6) type, expressions involving columns from these tables are evaluated early by the optimizer and are not part of the displayed statement. However, with FORMAT=JSON, some [const](#page-73-0) table accesses are displayed as a [ref](#page-74-3) access that uses a const value.

## <span id="page-84-0"></span>**8.8.4 Obtaining Execution Plan Information for a Named Connection**

To obtain the execution plan for an explainable statement executing in a named connection, use this statement:

```
EXPLAIN [options] FOR CONNECTION connection_id;
```

[EXPLAIN FOR CONNECTION](#page-84-0) returns the EXPLAIN information that is currently being used to execute a query in a given connection. Because of changes to data (and supporting statistics) it may produce a different result from running EXPLAIN on the equivalent query text. This difference in behavior can be useful in diagnosing more transient performance problems. For example, if you are running a statement in one session that is taking a long time to complete, using [EXPLAIN FOR CONNECTION](#page-84-0) in another session may yield useful information about the cause of the delay.

connection\_id is the connection identifier, as obtained from the INFORMATION\_SCHEMA PROCESSLIST table or the SHOW PROCESSLIST statement. If you have the PROCESS privilege, you can specify the identifier for any connection. Otherwise, you can specify the identifier only for your own connections.

If the named connection is not executing a statement, the result is empty. Otherwise, EXPLAIN FOR CONNECTION applies only if the statement being executed in the named connection is explainable. This includes SELECT, DELETE, INSERT, REPLACE, and UPDATE. (However, EXPLAIN FOR CONNECTION does not work for prepared statements, even prepared statements of those types.)

If the named connection is executing an explainable statement, the output is what you would obtain by using EXPLAIN on the statement itself.

If the named connection is executing a statement that is not explainable, an error occurs. For example, you cannot name the connection identifier for your current session because EXPLAIN is not explainable:

```
mysql> SELECT CONNECTION_ID();
+-----------------+
| CONNECTION_ID() |
+-----------------+
| 373 |
+-----------------+
1 row in set (0.00 sec)
```

```
mysql> EXPLAIN FOR CONNECTION 373;
ERROR 1889 (HY000): EXPLAIN FOR CONNECTION command is supported
only for SELECT/UPDATE/INSERT/DELETE/REPLACE
```

The Com\_explain\_other status variable indicates the number of EXPLAIN FOR CONNECTION statements executed.