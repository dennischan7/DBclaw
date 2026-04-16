# Oracle 19c - SELECT
Source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html

Purpose

Use a `SELECT` statement or subquery to retrieve data from one or more tables, object tables, views, object views, materialized views, analytic views, or hierarchies.

If part or all of the result of a `SELECT` statement is equivalent to an existing materialized view, then Oracle Database may use the materialized view in place of one or more tables specified in the `SELECT` statement. This substitution is called query rewrite. It takes place only if cost optimization is enabled and the `QUERY_REWRITE_ENABLED` parameter is set to `TRUE`. To determine whether query rewrite has occurred, use the `EXPLAIN` `PLAN` statement.

Prerequisites

For you to select data from a table, materialized view, analytic view, or hierarchy, the object must be in your own schema or you must have the `READ` or `SELECT` privilege on the table, materialized view, analytic view, or hierarchy.

For you to select rows from the base tables of a view:

* The object must be in your own schema or you must have the `READ` or `SELECT` privilege on it, and
* Whoever owns the schema containing the object must have the `READ` or `SELECT` privilege on the base tables.

The `READ` `ANY` `TABLE` or `SELECT` `ANY` `TABLE` system privilege also allows you to select data from any table, materialized view, analytic view, or hierarchy, or the base table of any materialized view, analytic view, or hierarchy.

To specify the `FOR` `UPDATE` clause, the preceding prerequisites apply with the following exception: The `READ` and `READ` `ANY` `TABLE` privileges, where mentioned, do not allow you to specify the `FOR` `UPDATE` clause.

To issue an Oracle Flashback Query using the `flashback_query_clause`, you must have the `READ` or `SELECT` privilege on the objects in the select list. In addition, either you must have `FLASHBACK` object privilege on the objects in the select list, or you must have `FLASHBACK` `ANY` `TABLE` system privilege.

with\_clause::=

Note:

You cannot specify only the `WITH` keyword. You must specify at least one of the clauses `plsql_declarations`, `subquery_factoring_clause`, or `subav_factoring_clause`.

subquery\_factoring\_clause::=

subav\_factoring\_clause::=

flashback\_query\_clause::=

inline\_external\_table\_properties::=

modified\_external\_table::=

modify\_external\_table\_properties::=

partition\_extension\_clause::=

subquery\_restriction\_clause::=

table\_collection\_expression::=

query\_partition\_clause::=

hierarchical\_query\_clause::=

(`condition` can be any condition as described in [Conditions](Conditions.md#GUID-C2E3ED44-16E7-4924-9125-E1693B1022A8))

grouping\_expression\_list::=

cell\_reference\_options::=

single\_column\_for\_loop::=

row\_pattern\_partition\_by::=

row\_pattern\_measure\_column::=

row\_pattern\_rows\_per\_match::=

row\_pattern\_quantifier::=

row\_pattern\_subset\_clause::=

row\_pattern\_subset\_item::=

row\_pattern\_definition\_list::=

row\_pattern\_definition::=

row\_pattern\_classifier\_func::=

row\_pattern\_match\_num\_func::=

row\_pattern\_nav\_logical::=

row\_pattern\_nav\_physical::=

row\_pattern\_nav\_compound::=

row\_pattern\_aggregate\_func::=

with\_clause

Use the `with_clause` to define the following:

* PL/SQL procedures and functions (using the `plsql_declarations` clause)
* Subquery blocks (using `subquery_factoring_clause` or `subav_factoring_clause`, or both)

plsql\_declarations

The `plsql_declarations` clause lets you declare and define PL/SQL functions and procedures. You can then reference the PL/SQL functions in the query in which you specify this clause, as well as its subqueries, if any. For the purposes of name resolution, these function names have precedence over schema-level stored functions.

If the query in which you specify this clause is not a top-level `SELECT` statement, then the following rules apply to the top-level SQL statement that contains the query:

* If the top-level statement is a `SELECT` statement, then it must have either a `WITH` `plsql_declarations` clause or the `WITH_PLSQL` hint.
* If the top-level statement is a `DELETE`, `MERGE`, `INSERT`, or `UPDATE` statement, then it must have the `WITH_PLSQL` hint.

The `WITH_PLSQL` hint only enables you to specify the `WITH` `plsql_declarations` clause within the statement. It is not an optimizer hint.

subquery\_factoring\_clause

The `subquery_factoring_clause` lets you assign a name (`query_name`) to a subquery block. You can then reference the subquery block multiple places in the query by specifying `query_name`. Oracle Database optimizes the query by treating the `query_name` as either an inline view or as a temporary table. The `query_name` is subject to the same naming conventions and restrictions as database schema objects. Refer to "[Database Object Naming Rules](Database-Object-Names-and-Qualifiers.md#GUID-75337742-67FD-4EC0-985F-741C93D918DA)" for information on database object names.

The column aliases following the `query_name` and the set operators separating multiple subqueries in the `AS` clause are valid and required for recursive subquery factoring. The `search_clause` and `cycle_clause` are valid only for recursive subquery factoring but are not required. See "[Recursive Subquery Factoring](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BCEJGIBG)".

You can specify this clause in any top-level `SELECT` statement and in most types of subqueries. The query name is visible to the main query and to all subsequent subqueries. For recursive subquery factoring, the query name is even visible to the subquery that defines the query name itself.

Recursive Subquery Factoring

If a `subquery_factoring_clause` refers to its own `query_name` in the subquery that defines it, then the `subquery_factoring_clause` is said to be recursive. A recursive `subquery_factoring_clause` must contain two query blocks: the first is the anchor member and the second is the recursive member. The anchor member must appear before the recursive member, and it cannot reference `query_name`. The anchor member can be composed of one or more query blocks combined by the set operators: `UNION` `ALL`, `UNION`, `INTERSECT` or `MINUS`. The recursive member must follow the anchor member and must reference `query_name` exactly once. You must combine the recursive member with the anchor member using the `UNION` `ALL` set operator.

The number of column aliases following `WITH` `query_name` and the number of columns in the `SELECT` lists of the anchor and recursive query blocks must be the same.

The recursive member cannot contain any of the following elements:

* The `DISTINCT` keyword or a `GROUP` `BY` clause
* The `model_clause`
* An aggregate function. However, analytic functions are permitted in the select list.
* Subqueries that refer to `query_name`.
* Outer joins that refer to `query_name` as the right table.

In previous releases of Oracle Database, the recursive member of a recursive `WITH` clause ran serially regardless of the parallelism of the entire query (also known as the top-level `SELECT` statement). Beginning with Oracle Database 12c Release 2 (12.2), the recursive member runs in parallel if the optimizer determines that the top-level `SELECT` statement can be executed in parallel.

search\_clause

Use the `SEARCH` clause to specify an ordering for the rows.

* Specify `BREADTH` `FIRST` `BY` if you want sibling rows returned before any child rows are returned.
* Specify `DEPTH` `FIRST` `BY` if you want child rows returned before any siblings rows are returned.
* Sibling rows are ordered by the columns listed after the `BY` keyword.
* The `c_alias` list following the `SEARCH` keyword must contain column names from the column alias list for `query_name`.
* The `ordering_column` is automatically added to the column list for the query name. The query that selects from `query_name` can include an `ORDER` `BY` on `ordering_column` to return the rows in the order that was specified by the `SEARCH` clause.

cycle\_clause

Use the `CYCLE` clause to mark cycles in the recursion.

* The `c_alias` list following the `CYCLE` keyword must contain column names from the column alias list for `query_name`. Oracle Database uses these columns to detect a cycle.
* `cycle_value` and `no_cycle_value` should be character strings of length 1.
* If a cycle is detected, then the cycle mark column specified by `cycle_mark_c_alias` for the row causing the cycle is set to the value specified for `cycle_value`. The recursion will then stop for this row. That is, it will not look for child rows for the offending row, but it will continue for other noncyclic rows.
* If no cycles are found, then the cycle mark column is set to the default value specified for `no_cycle_value`.
* The cycle mark column is automatically added to the column list for the `query_name`.
* A row is considered to form a cycle if one of its ancestor rows has the same values for the cycle columns.

If you omit the `CYCLE` clause, then the recursive `WITH` clause returns an error if cycles are discovered. In this case, a row forms a cycle if one of its ancestor rows has the same values for all the columns in the column alias list for `query_name` that are referenced in the `WHERE` clause of the recursive member.

Restrictions on Subquery Factoring

This clause is subject to the following restrictions:

* You can specify only one `subquery_factoring_clause` in a single SQL statement. Any `query_name` defined in the `subquery_factoring_clause` can be used in any subsequent named query block in the `subquery_factoring_clause`.
* In a compound query with set operators, you cannot use the `query_name` for any of the component queries, but you can use the `query_name` in the `FROM` clause of any of the component queries.
* You cannot specify duplicate names in the column alias list for `query_name`.
* The name used for the `ordering_column` has to be different from the name used for `cycle_mark_c_alias`.
* The `ordering_column` and cycle mark column names cannot already be in the column alias list for `query_name`.

subav\_factoring\_clause

With the `subav_factoring_clause`, you can define a transitory analytic view that filters fact data prior to aggregation or adds calculated measures to a query of an analytic view. The `subav_name` argument assigns a name to the transitory analytic view. You can then reference the transitory analytic view multiple places in the query by specifying `subav_name`. The `subav_name` is subject to the same naming conventions and restrictions as database schema objects. Refer to "[Database Object Naming Rules](Database-Object-Names-and-Qualifiers.md#GUID-75337742-67FD-4EC0-985F-741C93D918DA)" for information on database object names.

You can specify this clause in any top-level `SELECT` statement and in most types of subqueries. The query name is visible to the main query and to all subsequent subqueries.

The `subav_clause` argument defines a transitory analytic view.

subav\_clause

With the `USING` keyword, specify the name of an analytic view, which may be a transitory analytic view previously defined in the `WITH` clause or it may be a persistent analytic view. A persistent analytic view is defined in a `CREATE` `ANALYTIC` `VIEW` statement. If the analytic view is a persistent one, then the current user must have select access on it.

hierarchies\_clause

The `hierarchies_clause` specifies the hierarchies of the base analytic view that the results of the transitory analytic view are dimensioned by. With the `HIERARCHIES` keyword, specify the alias of one or more hierarchies of the base analytic view.

If you do not specify a `HIERARCHIES` clause, then the default hierarchies of the base analytic view are used.

filter\_clauses

You may specify a given `hier_alias` in at most one `filter_clause`.

filter\_clause

The filter clause applies the specified predicate condition to the fact table, which reduces the number of rows returned from the table before aggregation of the measure values. The predicate may contain any SQL row function or operation. The predicate may refer to any attribute of the specified hierarchy or it may refer to a measure of the analytic view if you specify the `MEASURES` keyword.

For example, the following clause restricts the aggregation of measure values to those for the first and second quarters of every year of a time hierarchy.

```
FILTER FACT (time_hier TO quarter_of_year IN (1,2))
```

If you then select from the transitory analytic view the sales for the years 2000 and 2001, the values returned are the aggregated values of the first and second quarters only.

An example of specifying a predicate for a measure in the filter clause is the following.

```
FILTER FACT (MEASURES TO sales BETWEEN 100 AND 200)
```

attr\_dim\_alias

The alias of an attribute dimension in the base analytic view. The `USER_ANALYTIC_VIEW_DIMENSIONS` view contains the aliases of the attribute dimensions in an analytic view.

hier\_alias

The alias of a hierarchy in the base analytic view. The `USER_ANALYTIC_VIEW_HIERS` view contains the aliases of the hierarchies in an analytic view.

add\_calcs\_clause

With the `ADD` `MEASURES` keywords, you may add calculated measures to the transitory analytic view.

calc\_meas\_clause

Specify a name for the calculated measure and an analytic view expression that specifies values for the calculated measure. The analytic view expression can be any valid `calc_meas_expression` as described in [Analytic View Expressions](analytic-view-measure-expressions.md#GUID-F8C7ED67-A4EC-479C-975F-12F1F4B8CBA0 "You can use analytic view expressions to create calculated measures within the definition of an analytic view or in a query that selects from an analytic view."). For example, the following adds a calculated measure named âshare\_sales.â

```
ADD MEASURES (share_sales AS (SHARE_OF(sales HIERARCHY time_hier PARENT)))
```

hint

Specify a comment that passes instructions to the optimizer on choosing an execution plan for the statement.

See Also:

"[Hints](Comments.md#GUID-D316D545-89E2-4D54-977F-FC97815CD62E)" for the syntax and description of hints

DISTINCT | UNIQUE

Specify `DISTINCT` or `UNIQUE` if you want the database to return only one copy of each set of duplicate rows selected. These two keywords are synonymous. Duplicate rows are those with matching values for each expression in the select list.

Restrictions on DISTINCT and UNIQUE Queries

These types of queries are subject to the following restrictions:

* When you specify `DISTINCT` or `UNIQUE`, the total number of bytes in all select list expressions is limited to the size of a data block minus some overhead. This size is specified by the initialization parameter `DB_BLOCK_SIZE`.
* You cannot specify `DISTINCT` if the `select_list` contains LOB columns.

ALL

Specify `ALL` if you want the database to return all rows selected, including all copies of duplicates. The default is `ALL`.

select\_list

The `select_list` lets you specify the columns you want to retrieve from the database.

\* (all-column wildcard)

Specify the all-column wildcard (asterisk) to select all columns, excluding pseudocolumns and `INVISIBLE` columns, from all tables, views, or materialized views listed in the `FROM` clause. The columns are returned in the order indicated by the `COLUMN_ID` column of the `*_TAB_COLUMNS` data dictionary view for the table, view, or materialized view.

If you are selecting from a table rather than from a view or a materialized view, then columns that have been marked as `UNUSED` by the `ALTER` `TABLE` `SET` `UNUSED` statement are not selected.

query\_name.\*

Specify `query_name` followed by a period and the asterisk to select all columns from the specified subquery block. For `query_name`, specify a subquery block name already specified in the `subquery_factoring_clause`. You must have specified the `subquery_factoring_clause` in order to specify `query_name` in the `select_list`. If you specify `query_name` in the `select_list`, then you also must specify `query_name` in the `query_table_expression` (`FROM` clause).

table.\* | view.\* | materialized view.\*

Specify the object name followed by a period and the asterisk to select all columns from the specified table, view, or materialized view. Oracle Database returns a set of columns in the order in which the columns were specified when the object was created. A query that selects rows from two or more tables, views, or materialized views is a join.

You can use the schema qualifier to select from a table, view, or materialized view in a schema other than your own. If you omit `schema`, then the database assumes the table, view, or materialized view is in your own schema.

t\_alias .\*

Specify a correlation name (alias) followed by a period and the asterisk to select all columns from the object with that correlation name specified in the `FROM` clause of the same subquery. The object can be a table, view, materialized view, or subquery. Oracle Database returns a set of columns in the order in which the columns were specified when the object was created. A query that selects rows from two or more objects is a join.

expr

Specify an expression representing the information you want to select. A column name in this list can be qualified with `schema` only if the table, view, or materialized view containing the column is qualified with `schema` in the `FROM` clause. If you specify a member method of an object type, then you must follow the method name with parentheses even if the method takes no arguments.

The expression can also hold a scalar value that can be return values of PL/SQLfunctions, subqueries that return a single value per row, and SQL macros.

c\_alias

Specify an alias for the column expression. Oracle Database will use this alias in the column heading of the result set. The `AS` keyword is optional. The alias effectively renames the select list item for the duration of the query. The alias can be used in the `order_by_clause` but not other clauses in the query.

Restrictions on the Select List

The select list is subject to the following restrictions:

* If you also specify a [group\_by\_clause](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2182483) in this statement, then this select list can contain only the following types of expressions:

  + Constants
  + Aggregate functions and the functions `USER`, `UID`, and `SYSDATE`
  + Expressions identical to those in the `group_by_clause`. If the `group_by_clause` is in a subquery, then all columns in the select list of the subquery must match the `GROUP` `BY` columns in the subquery. If the select list and `GROUP` `BY` columns of a top-level query or of a subquery do not match, then the statement results in ORA-00979.
  + Expressions involving the preceding expressions that evaluate to the same value for all rows in a group
* You can select a rowid from a join view only if the join has one and only one key-preserved table. The rowid of that table becomes the rowid of the view.
* If two or more tables have some column names in common, and if you are specifying a join in the `FROM` clause, then you must qualify column names with names of tables or table aliases.

FROM Clause

The `FROM` clause lets you specify the objects from which data is selected.

You can invoke a polymorphic table function (PTF) in the query block of the `FROM` clause like other existing table functions. A PTF is a table function whose operands can have more than one type. .

Starting with Oracle Database Release 19c, version 19.7, you can write table valued macros and use them inside the `FROM` clause, where it would be legal to call a PL/SQL function. SQL table macros are expressions, typically used in a `FROM` clause, to act like a kind of polymorphic (parameterized) views. You must define these macro functions in PL/SQL and call them from SQL for them to function as macros.

ONLY

The `ONLY` clause applies only to views. Specify `ONLY` if the view in the `FROM` clause is a view belonging to a hierarchy and you do not want to include rows from any of its subviews.

query\_table\_expression

Use the `query_table_expression` clause to identify a subquery block, table, view, materialized view, analytic view, hierarchy, partition, or subpartition, or to specify a subquery that identifies the objects. In order to specify a subquery block, you must have specified the subquery block name (`query_name` in the `subquery_factoring_clause` or `subav_name` in the `subav_factoring_clause` ).

The analytic view in the expression may be a transitory analytic view defined in the `with_clause` or a persistent analytic view.

LATERAL

Specify `LATERAL` to designate `subquery` as a lateral inline view. Within a lateral inline view, you can specify tables that appear to the left of the lateral inline view in the `FROM` clause of a query. You can specify this left correlation anywhere within `subquery` (such as the `SELECT`, `FROM`, and `WHERE` clauses) and at any nesting level.

Restrictions on LATERAL

Lateral inline views are subject to the following restrictions:

* If you specify `LATERAL`, then you cannot specify the `pivot_clause`, the `unpivot_clause`, or a pattern in the `table_reference` clause.
* If a lateral inline view contains the `query_partition_clause`, and it is the right side of a join clause, then it cannot contain a left correlation to the left table in the join clause. However, it can contain a left correlation to a table to its left in the `FROM` clause that is not the left table.
* A lateral inline view cannot contain a left correlation to the first table in a right outer join or full outer join.

inline\_external\_table

Specify this clause to inline an external table in a query. You must specify the table columns and properties for the external table that will be inlined in the query.

inline\_external\_table\_properties

This clause extends the `external_table_data_props` with the `REJECT LIMIT` and `access_driver_type` options. Use this clause to specify the properties of the external table.

In addition to supporting external data residing in operating file systems and Big Data sources and formats such as HDFS and Hive, Oracle supports external data residing in objects.

modified\_external\_table

You can use this clause to override some external table properties specified by the `CREATE TABLE` or `ALTER TABLE` statements from within a query.

You can override external table parameters at runtime.

Restrictions

* You must specify the key words `EXTERNAL MODIFY` in the query. If you do not specify the keywords, you will see a `Missing or invalid option` error.
* You must reference an external table in the query. If you do not, you will see an error.
* You must specify at least one property in the query. One of `DEFAULT DIRECTORY`, `LOCATION`, `ACCESS PARAMETERS`, or `REJECT LIMIT`.
* If you specify more than one external table properties, they must be listed in order. First the `DEFAULT DIRECTORY` must be specified, followed by the `ACCESS PARAMETERS`, `LOCATION` and `REJECT LIMIT`. Otherwise an error will be raised.
* In the `DEFAULT DIRECTORY` clause, you must specify only one proper default directory. Otherwise a `Missing DEFAULT keyword` error will occur.
* You must enclose a filename in the `LOCATION` clause within quotes. Otherwise a `Missing keyword` error will occur. Note that the access driver will decide whether or not to allow a `LOCATION` clause in the query. If the clause is disallowed for a particular access driver, an error will be raised.
* For `ORACLE_LOADER` and `ORACLE_DATAPUMP` access drivers, the external file location in the `LOCATION` clause must be specified in the following format: directory: location, i.e, the directory and location must be separated by a colon. Multiple locations in the clause must be separated by a comma. Otherwise, a `Missing keyword` error will occur.
* Note that `LOCATION` will be made optional in `CREATE TABLE`, and must be specified either when creating or querying the external table. Otherwise an error will be raised in the access driver.
* When populating external data using `ORACLE DATAPUMP` via `CTAS`, the external file location must be specified. This will be the only case where `LOCATION` clause is mandatory in `CREATE TABLE`.
* When overriding access parameters, a proper access parameter list must be provided in the `ACCESS PARAMETERS` clause, with enclosing parentheses.

  Note that the syntax and allowable values for the access parameters in the `modified_external_table` clause are the same as for the external table DDL for each access driver. For more see [Oracle Database Utilities](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/19/sqlrf&id=SUTIL)for additional details regarding syntax and permissible values.
* If you specify the `REJECT LIMIT`, then it must either be `UNLIMITED` or some valid value that is within range. Otherwise a `Reject limit out of range` error will be raised.

modify\_external\_table\_properties

You can specify the external table properties that you want to modify at run time using this clause. The parameters that you can modify are `DEFAULT DIRECTORY`, `LOCATION`, `ACCESS PARAMETERS (BADFILE, LOGFILE, DISCARDFILE)` and `REJECT LIMIT`.

Example: Overriding External Table Parameters in a Query

```
  SELECT * FROM
  sales_external EXTERNAL MODIFY (LOCATION 'sales_9.csvâ REJECT LIMIT UNLIMITED);
```

flashback\_query\_clause

Use the `flashback_query_clause` to retrieve data from a table, view, or materialized view based on time dimensions associated with the data.

This clause implements SQL-driven Flashback, which lets you specify the following:

* A different system change number or timestamp for each object in the select list, using the clauses `VERSIONS` `BETWEEN` `{` `SCN` `|` `TIMESTAMP` `}` or `VERSIONS` `AS` `OF` `{` `SCN` `|` `TIMESTAMP` `}`. You can also implement session-level Flashback using the `DBMS_FLASHBACK` package.
* A valid time period for each object in the select list, using the clauses `VERSIONS` `PERIOD` `FOR` or `AS` `OF` `PERIOD` `FOR`. You can also implement valid-time session-level Flashback using the `DBMS_FLASHBACK_ARCHIVE` package.

A Flashback Query lets you retrieve a history of changes made to a row. You can retrieve the corresponding identifier of the transaction that made the change using the `VERSIONS_XID` pseudocolumn. You can also retrieve information about the transaction that resulted in a particular row version by issuing an Oracle Flashback Transaction Query. You do this by querying the `FLASHBACK_TRANSACTION_QUERY` data dictionary view for a particular transaction ID.

VERSIONS BETWEEN { SCN | TIMESTAMP }

Specify `VERSIONS` `BETWEEN` to retrieve multiple versions of the rows returned by the query. Oracle Database returns all committed versions of the rows that existed between two SCNs or between two timestamp values. The first specified SCN or timestamp must be earlier than the second specified SCN or timestamp. The rows returned include deleted and subsequently reinserted versions of the rows.

* Specify `VERSIONS` `BETWEEN` `SCN` ... to retrieve the versions of the row that existed between two SCNs. Both expressions must evaluate to a number and cannot evaluate to NULL. `MINVALUE` and `MAXVALUE` resolve to the SCN of the oldest and most recent data available, respectively.
* Specify `VERSIONS` `BETWEEN` `TIMESTAMP` ... to retrieve the versions of the row that existed between two timestamps. Both expressions must evaluate to a timestamp value and cannot evaluate to NULL. `MINVALUE` and `MAXVALUE` resolve to the timestamp of the oldest and most recent data available, respectively.

AS OF { SCN | TIMESTAMP }

Specify `AS` `OF` to retrieve the single version of the rows returned by the query at a particular change number (SCN) or timestamp. If you specify `SCN`, then `expr` must evaluate to a number. If you specify `TIMESTAMP`, then `expr` must evaluate to a timestamp value. In either case, `expr` cannot evaluate to NULL. Oracle Database returns rows as they existed at the specified system change number or time.

Oracle Database provides a group of version query pseudocolumns that let you retrieve additional information about the various row versions. Refer to "[Version Query Pseudocolumns](Version-Query-Pseudocolumns.md#GUID-F4DB0235-43A9-4AA2-8E9C-F2D9699D4AAD)" for more information.

When both clauses are used together, the `AS` `OF` clause determines the SCN or moment in time from which the database issues the query. The `VERSIONS` clause determines the versions of the rows as seen from the `AS` `OF` point. The database returns null for a row version if the transaction started before the first `BETWEEN` value or ended after the `AS` `OF` point.

VERSIONS PERIOD FOR

Specify `VERSIONS` `PERIOD` `FOR` to retrieve rows from `table` based on whether they are considered valid during the specified time period. In order to use this clause, `table` must support Temporal Validity.

* For `valid_time_column`, specify the name of the valid time dimension column for `table`.
* Use the `BETWEEN` clause to specify the time period during which rows are considered valid. Both expressions must evaluate to a timestamp value and cannot evaluate to NULL. `MINVALUE` resolves to the earliest date or timestamp in the start time column of `table`. `MAXVALUE` resolves to latest date or timestamp in the end time column of `table`.

AS OF PERIOD FOR

Specify `AS` `OF` `PERIOD` `FOR` to retrieve rows from `table` based on whether they are considered valid as of the specified time. In order to use this clause, `table` must support Temporal Validity.

* For `valid_time_column`, specify the name of the valid time dimension column for `table`.
* Use `expr` to specify the time as of which rows are considered valid. The expression must evaluate to a timestamp value and cannot evaluate to NULL.

See Also:

* [Oracle Database Development Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/19/sqlrf&id=ADFNS967) for more information on Temporal Validity
* `CREATE` `TABLE` [period\_definition](CREATE-TABLE.md#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6__CJADHJHB) to learn how to configure a table to support Temporal Validity and for information about the `valid_time_column`, start time column, and end time column

Note on Flashback Queries

When performing a flashback query, Oracle Database might not use query optimizations that it would use for other types of queries, which could have a negative impact on performance. In particular, this occurs when you specify multiple flashback queries in a hierarchical query.

Restrictions on Flashback Queries

These queries are subject to the following restrictions:

* You cannot specify a column expression or a subquery in the expression of the `AS` `OF` clause.
* You cannot specify the `AS` `OF` clause if you have specified the `for_update_clause`.
* You cannot use the `AS` `OF` clause in the defining query of a materialized view.
* You cannot use the `VERSIONS` clause in flashback queries to temporary or external tables, or tables that are part of a cluster.
* You cannot use the `VERSIONS` clause in flashback queries to views. However, you can use the `VERSIONS` syntax in the defining query of a view.
* You cannot specify the `flashback_query_clause` if you have specified `query_name` in the `query_table_expression`.

partition\_extension\_clause

For `PARTITION` or `SUBPARTITION`, specify the name or key value of the partition or subpartition within `table` from which you want to retrieve data.

For range- and list-partitioned data, as an alternative to this clause, you can specify a condition in the `WHERE` clause that restricts the retrieval to one or more partitions of `table`. Oracle Database will interpret the condition and fetch data from only those partitions. It is not possible to formulate such a `WHERE` condition for hash-partitioned data.

dblink

For `dblink`, specify the complete or partial name for a database link to a remote database where the table, view, or materialized view is located. This database need not be an Oracle Database.

If you omit `dblink`, then the database assumes that the table, view, or materialized view is on the local database.

Restrictions on Database Links

Database links are subject to the following restrictions:

* You cannot query a user-defined type or an object `REF` on a remote table.
* You cannot query columns of type `ANYTYPE`, `ANYDATA`, or `ANYDATASET` from remote tables.

table | view | materialized\_view | analytic\_view | hierarchy

Specify the name of a table, view, materialized view, analytic view, or hierarchy from which data is selected.

analytic\_view

A persistent analytic view defined with the `CREATE` `ANALYTIC` `VIEW` statement or a transitory analytic view defined in a `WITH` clause.

hierarchy

A hierarchy defined with the `CREATE` `HIERARCHY` statement.

sample\_clause

The `sample_clause` lets you instruct the database to select from a random sample of data from the table, rather than from the entire table.

BLOCK

`BLOCK` instructs the database to attempt to perform random block sampling instead of random row sampling.

Block sampling is possible only during full table scans or index fast full scans. If a more efficient execution path exists, then Oracle Database does not perform block sampling. If you want to guarantee block sampling for a particular table or index, then use the `FULL` or `INDEX_FFS` hint.

Beginning with Oracle Database 12c Release 2 (12.2.), you can specify block sampling for external tables. In earlier releases, specifying block sampling for external tables had no effect; row sampling was performed.

sample\_percent

For `sample_percent`, specify the percentage of the total row or block count to be included in the sample. The value must be in the range .000001 to, but not including, 100. This percentage indicates the probability of each row, or each cluster of rows in the case of block sampling, being selected as part of the sample. It does not mean that the database will retrieve exactly `sample_percent` of the rows of `table`.

WARNING:

The use of statistically incorrect assumptions when using this feature can lead to incorrect or undesirable results.

SEED seed\_value

Specify this clause to instruct the database to attempt to return the same sample from one execution to the next. The `seed_value` must be an integer between 0 and 4294967295. If you omit this clause, then the resulting sample will change from one execution to the next.

Restrictions on sample\_clause

The following restrictions apply to the `SAMPLE` clause:

* You cannot specify the `SAMPLE` clause in a subquery in a DML statement.
* You can specify the `SAMPLE` clause in a query on a base table, a container table of a materialized view, or a view that is key preserving. You cannot specify this clause on a view that is not key preserving.

subquery\_restriction\_clause

The `subquery_restriction_clause` lets you restrict the subquery in one of the following ways:

WITH READ ONLY

Specify `WITH READ ONLY` to indicate that the table or view cannot be updated.

WITH CHECK OPTION

Specify `WITH CHECK OPTION` to indicate that Oracle Database prohibits any changes to the table or view that would produce rows that are not included in the subquery. When used in the subquery of a DML statement, you can specify this clause in a subquery in the `FROM` clause but not in subquery in the `WHERE` clause.

CONSTRAINT constraint

Specify the name of the `CHECK OPTION` constraint. If you omit this identifier, then Oracle automatically assigns the constraint a name of the form `SYS_C``n`, where n is an integer that makes the constraint name unique within the database.

table\_collection\_expression

The `table_collection_expression` lets you inform Oracle that the value of `collection_expression` should be treated as a table for purposes of query and DML operations. The `collection_expression` can be a subquery, a column, a function, or a collection constructor. Regardless of its form, it must return a collection valueâthat is, a value whose type is nested table or varray. This process of extracting the elements of a collection is called collection unnesting.

The optional plus (+) is relevant if you are joining the `TABLE` collection expression with the parent table. The + creates an outer join of the two, so that the query returns rows from the outer table even if the collection expression is null.

Note:

In earlier releases of Oracle, when `collection_expression` was a subquery, `table_collection_expression` was expressed as `THE` `subquery`. That usage is now deprecated.

The `collection_expression` can reference columns of tables defined to its left in the `FROM` clause. This is called left correlation. Left correlation can occur only in `table_collection_expression`. Other subqueries cannot contains references to columns defined outside the subquery.

The optional `(+)` lets you specify that `table_collection_expression` should return a row with all fields set to null if the collection is null or empty. The `(+)` is valid only if `collection_expression` uses left correlation. The result is similar to that of an outer join.

When you use the `(+)` syntax in the `WHERE` clause of a subquery in an `UPDATE` or `DELETE` operation, you must specify two tables in the `FROM` clause of the subquery. Oracle Database ignores the outer join syntax unless there is a join in the subquery itself.

t\_alias

Specify a correlation name, which is an alias for the table, view, materialized view, or subquery for evaluating the query. This alias is required if the select list references any object type attributes or object type methods. Correlation names are most often used in a correlated query. Other references to the table, view, or materialized view throughout the query must refer to this alias.

pivot\_clause

The `pivot_clause` lets you write cross-tabulation queries that rotate rows into columns, aggregating data in the process of the rotation. The output of a pivot operation typically includes more columns and fewer rows than the starting data set. The `pivot_clause` performs the following steps:

1. The `pivot_clause` computes the aggregation functions specified at the beginning of the clause. Aggregation functions must specify a `GROUP` `BY` clause to return multiple values, yet the `pivot_clause` does not contain an explicit `GROUP` `BY` clause. Instead, the `pivot_clause` performs an implicit `GROUP` `BY`. The implicit grouping is based on all the columns not referred to in the `pivot_clause`, along with the set of values specified in the `pivot_in_clause`.). If you specify more than one aggregation function, then you must provide aliases for at least all but one of the aggregation functions.
2. The grouping columns and aggregated values calculated in Step 1 are configured to produce the following cross-tabular output:

   1. All the implicit grouping columns not referred to in the `pivot_clause`, followed by
   2. New columns corresponding to values in the `pivot_in_clause`. Each aggregated value is transposed to the appropriate new column in the cross-tabulation. If you specify the `XML` keyword, then the result is a single new column that expresses the data as an XML string. The database generates a name for each new column. If you do not provide an alias for an aggregation function, then the database uses each pivot column value as the name for each new column to which that aggregated value is transposed. If you provide an alias for an aggregation function, then the database generates a name for each new column to which that aggregated value is transposed by concatenating the pivot column name, the underscore character (\_), and the aggregation function alias. If a generated column name exceeds the maximum length of a column name, then an ORA-00918 error is returned. To avoid this issue, specify a shorter alias for the pivot column heading, the aggregation function, or both.

The subclauses of the `pivot_clause` have the following semantics:

XML

The optional `XML` keyword generates XML output for the query. The `XML` keyword permits the `pivot_in_clause` to contain either a subquery or the wildcard keyword `ANY`. Subqueries and `ANY` wildcards are useful when the `pivot_in_clause` values are not known in advance. With XML output, the values of the pivot column are evaluated at execution time. You cannot specify `XML` when you specify explicit pivot values using expressions in the `pivot_in_clause`.

When XML output is generated, the aggregate function is applied to each distinct pivot value, and the database returns a column of `XMLType` containing an XML string for all value and measure pairs.

expr

For `expr`, specify an expression that evaluates to a constant value of a pivot column. You can optionally provide an alias for each pivot column value. If there is no alias, the column heading becomes a quoted identifier.

subquery

A subquery is used only in conjunction with the `XML` keyword. When you specify a subquery, all values found by the subquery are used for pivoting. The output is not the same cross-tabular format returned by non-XML pivot queries. Instead of multiple columns specified in the `pivot_in_clause`, the subquery produces a single XML string column. The XML string for each row holds aggregated data corresponding to the implicit `GROUP` `BY` value of that row. The XML string for each output row includes all pivot values found by the subquery, even if there are no corresponding rows in the input data.

The subquery must return a list of unique values at the execution time of the pivot query. If the subquery does not return a unique value, then Oracle Database raises a run-time error. Use the `DISTINCT` keyword in the subquery if you are not sure the query will return unique values.

ANY

The `ANY` keyword is used only in conjunction with the `XML` keyword. The `ANY` keyword acts as a wildcard and is similar in effect to `subquery`. The output is not the same cross-tabular format returned by non-XML pivot queries. Instead of multiple columns specified in the `pivot_in_clause`, the `ANY` keyword produces a single XML string column. The XML string for each row holds aggregated data corresponding to the implicit `GROUP` `BY` value of that row. However, in contrast to the behavior when you specify `subquery`, the `ANY` wildcard produces an XML string for each output row that includes only the pivot values found in the input data corresponding to that row.

unpivot\_clause

The `unpivot_clause` rotates columns into rows.

* The `INCLUDE` | `EXCLUDE` `NULLS` clause gives you the option of including or excluding null-valued rows. `INCLUDE` `NULLS` causes the unpivot operation to include null-valued rows; `EXCLUDE` `NULLS` eliminates null-values rows from the return set. If you omit this clause, then the unpivot operation excludes nulls.
* For `column`, specify a name for each output column that will hold measure values, such as `sales_quantity`.
* In the `pivot_for_clause`, specify a name for each output column that will hold descriptor values, such as quarter or product.
* In the `unpivot_in_clause`, specify the input data columns whose names will become values in the output columns of the `pivot_for_clause`. These input data columns have names specifying a category value, such as Q1, Q2, Q3, Q4. The optional `AS` clause lets you map the input data column names to the specified `literal` values in the output columns.

The unpivot operation turns a set of value columns into one column. Therefore, the data types of all the value columns must be in the same data type group, such as numeric or character.

* If all the value columns are `CHAR`, then the unpivoted column is `CHAR`. If any value column is `VARCHAR2`, then the unpivoted column is `VARCHAR2`.
* If all the value columns are `NUMBER`, then the unpivoted column is `NUMBER`. If any value column is `BINARY_DOUBLE`, then the unpivoted column is `BINARY_DOUBLE`. If no value column is `BINARY_DOUBLE` but any value column is `BINARY_FLOAT`, then the unpivoted column is `BINARY_FLOAT`.

containers\_clause

The `CONTAINERS` clause is useful in a multitenant container database (CDB). This clause lets you query data in the specified table or view across all containers in a CDB.

* To query data in a CDB, you must be a common user connected to the CDB root, and the table or view must exist in the root and all PDBs. The query returns all rows from the table or view in the CDB root and in all open PDBs.
* To query data in an application container, you must be a common user connected to the application root, and the table or view must exist in the application root and all PDBs in the application container. The query returns all rows from the table or view in the application root and in all open PDBs in the application container.

The table or view must be in your own schema. It is not necessary to specify `schema`, but if you do then you must specify your own schema.

The query returns all rows from the table or view in the root and in all open PDBs, except PDBs that are open in `RESTRICTED` mode. If the queried table or view does not already contain a `CON_ID` column, then the query adds a `CON_ID` column to the query result, which identifies the container whose data a given row represents.

shards\_clause

Use the `shards_clause` to query Oracle supplied objects such as `V$`, `DBA/USER/ALL` views, and dictionary tables across shards. You can execute a query with the `shards_clause` only on the shard catalog database.

This feature enables easier centralized management by providing the ability to execute queries across all shards from a central shard catalog.

join\_clause

Use the appropriate `join_clause` syntax to identify tables that are part of a join from which to select data. The `inner_cross_join_clause` lets you specify an inner or cross join. The `outer_join_clause` lets you specify an outer join. The `cross_outer_apply_clause` lets you specify a variation of an ANSI `CROSS` `JOIN` or an ANSI `LEFT` `OUTER` `JOIN` with left correlation support.

When you join more than two row sources, you can use parentheses to override default precedence. For example, the following syntax:

```
SELECT ... FROM a JOIN (b JOIN c) ...
```

results in a join of `b` and `c`, and then a join of that result set with `a`.

inner\_cross\_join\_clause

Inner joins return only those rows that satisfy the join condition.

INNER

Specify `INNER` to explicitly specify an inner join.

JOIN

The `JOIN` keyword explicitly states that a join is being performed. You can use this syntax to replace the comma-delimited table expressions used in `WHERE` clause joins with `FROM` clause join syntax.

ON condition

Use the `ON` clause to specify a join condition. Doing so lets you specify join conditions separate from any search or filter conditions in the `WHERE` clause.

USING (column)

When you are specifying an equijoin of columns that have the same name in both tables, the `USING` `column` clause indicates the columns to be used. You can use this clause only if the join columns in both tables have the same name. Within this clause, do not qualify the column name with a table name or table alias.

CROSS

The `CROSS` keyword indicates that a cross join is being performed. A cross join produces the cross-product of two relations and is essentially the same as the comma-delimited Oracle Database notation.

NATURAL

The `NATURAL` keyword indicates that a natural join is being performed. Refer to [NATURAL](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABHGCAE) for the full semantics of this clause.

outer\_join\_clause

Outer joins return all rows that satisfy the join condition and also return some or all of those rows from one table for which no rows from the other satisfy the join condition. You can specify two types of outer joins: a conventional outer join using the `table_reference` syntax on both sides of the join, or a partitioned outer join using the `query_partition_clause` on one side or the other. A partitioned outer join is similar to a conventional outer join except that the join takes place between the outer table and each partition of the inner table. This type of join lets you selectively make sparse data more dense along the dimensions of interest. This process is called data densification.

query\_partition\_clause

The `query_partition_clause` lets you define a partitioned outer join. Such a join extends the conventional outer join syntax by applying the outer join to partitions returned by the query. Oracle Database creates a partition of rows for each expression you specify in the `PARTITION` `BY` clause. The rows in each query partition have same value for the `PARTITION` `BY` expression.

The `query_partition_clause` can be on either side of the outer join. The result of a partitioned outer join is a `UNION` of the outer joins of each of the partitions in the partitioned result set and the table on the other side of the join. This type of result is useful for filling gaps in sparse data, which simplifies analytic calculations.

If you omit this clause, then the database treats the entire table expressionâeverything specified in `table_reference`âas a single partition, resulting in a conventional outer join.

To use the `query_partition_clause` in an analytic function, use the upper branch of the syntax (without parentheses). To use this clause in a model query (in the `model_column_clauses`) or a partitioned outer join (in the `outer_join_clause`), use the lower branch of the syntax (with parentheses).

Restrictions on Partitioned Outer Joins

Partitioned outer joins are subject to the following restrictions:

* You can specify the `query_partition_clause` on either the right or left side of the join, but not both.
* You cannot specify a `FULL` partitioned outer join.
* If you specify the `query_partition_clause` in an outer join with an `ON` clause, then you cannot specify a subquery in the `ON` condition.

NATURAL

The `NATURAL` keyword indicates that a natural join is being performed. A natural join is based on all columns in the two tables that have the same name. It selects rows from the two tables that have equal values in the relevant columns. If two columns with the same name do not have compatible data types, then an error is raised. When specifying columns that are involved in the natural join, do not qualify the column name with a table name or table alias.

On occasion, the table pairings in natural or cross joins may be ambiguous. For example, consider the following join syntax:

```
   a NATURAL LEFT JOIN b LEFT JOIN c ON b.c1 = c.c1
```

This example can be interpreted in either of the following ways:

```
   a NATURAL LEFT JOIN (b LEFT JOIN c ON b.c1 = c.c1) 
   (a NATURAL LEFT JOIN b) LEFT JOIN c ON b.c1 = c.c1
```

To avoid this ambiguity, you can use parentheses to specify the pairings of joined tables. In the absence of such parentheses, the database uses left associativity, pairing the tables from left to right.

Restriction on Natural Joins

You cannot specify a LOB column, columns of `ANYTYPE`, `ANYDATA`, or `ANYDATASET`, or a collection column as part of a natural join.

outer\_join\_type

The `outer_join_type` indicates the kind of outer join being performed:

* Specify `RIGHT` to indicate a right outer join.
* Specify `LEFT` to indicate a left outer join.
* Specify `FULL` to indicate a full or two-sided outer join. In addition to the inner join, rows from both tables that have not been returned in the result of the inner join will be preserved and extended with nulls.
* You can specify the optional `OUTER` keyword following `RIGHT`, `LEFT`, or `FULL` to explicitly clarify that an outer join is being performed.

ON condition

Use the `ON` clause to specify a join condition. Doing so lets you specify join conditions separate from any search or filter conditions in the `WHERE` clause.

Restriction on the ON condition Clause

You cannot specify this clause with a `NATURAL` outer join.

USING column

In an outer join with the `USING` clause, the query returns a single column that coalesces the two matching columns in the join. The coalesce function is as follows:

```
COALESCE (a, b) = a if a NOT NULL, else b.
```

Therefore:

* A left outer join returns all the common column values from the left table in the `FROM` clause.
* A right outer join returns all the common column values from the right table in the `FROM` clause.
* A full outer join returns all the common column values from both joined tables.

Restriction on the USING column Clause

The `USING` `column` clause is subject to the following restrictions:

* Within this clause, do not qualify the column name with a table name or table alias.
* You cannot specify a LOB column or a collection column in the `USING` `column` clause.
* You cannot specify this clause with a `NATURAL` outer join.

cross\_outer\_apply\_clause

This clause allows you to perform a variation of an ANSI `CROSS` `JOIN` or an ANSI `LEFT` `OUTER` `JOIN` with left correlation support. You can specify a `table_reference` or `collection_expression` to the right of the `APPLY` keyword. The `table_reference` can be a table, inline view, or `TABLE` collection expression. The `collection_expression` can be a subquery, a column, a function, or a collection constructor. Regardless of its form, it must return a collection valueâthat is, a value whose type is nested table or varray. The `table_reference` or `collection_expression` can reference columns of tables defined in the `FROM` clause to the left of the `APPLY` keyword. This is called left correlation.

* Specify `CROSS` `APPLY` to perform a variation of an ANSI `CROSS` `JOIN`. Only rows from the table on the left side of the join that produce a result set from `table_reference` or `collection_expression` are returned.
* Specify `OUTER` `APPLY` to perform a variation of an ANSI `LEFT` `OUTER` `JOIN`. All rows from the table on the left side of the join are returned. Rows that do not produce a result set from `table_reference` or `collection_expression` have the NULL value in the corresponding column(s).

Restriction on the cross\_outer\_apply\_clause

The `table_reference` cannot be a lateral inline view.

inline\_analytic\_view

An inline analytic view is a transitory analytic view that is specified in the `FROM` clause. To create an inline analytic view, use the `ANALYTIC` `VIEW` keyword and specify a `subav_clause` that defines the analytic view. Optionally, you may specify an `inline_av_alias`, which is an alias for the inline analytic view. The rules for the `inline_av_alias` are the same as the rules for an inline view alias.

where\_clause

The `WHERE` condition lets you restrict the rows selected to those that satisfy one or more conditions. For `condition`, specify any valid SQL condition.

If you omit this clause, then the database returns all rows from the tables, views, or materialized views in the `FROM` clause.

Note:

If this clause refers to a `DATE` column of a partitioned table or index, then the database performs partition pruning only if:

* You created the table or index partitions by fully specifying the year using the `TO_DATE` function with a 4-digit format mask, and
* You specify the date in the `where_clause` of the query using the `TO_DATE` function and either a 2- or 4-digit format mask.

hierarchical\_query\_clause

The `hierarchical_query_clause` lets you select rows in a hierarchical order.

`SELECT` statements that contain hierarchical queries can contain the `LEVEL` pseudocolumn in the select list. `LEVEL` returns the value 1 for a root node, 2 for a child node of a root node, 3 for a grandchild, and so on. The number of levels returned by a hierarchical query may be limited by available user memory.

Oracle processes hierarchical queries as follows:

* A join, if present, is evaluated first, whether the join is specified in the `FROM` clause or with `WHERE` clause predicates.
* The `CONNECT` `BY` condition is evaluated.
* Any remaining `WHERE` clause predicates are evaluated.

If you specify this clause, then do not specify either `ORDER` `BY` or `GROUP` `BY`, because they will destroy the hierarchical order of the `CONNECT` `BY` results. If you want to order rows of siblings of the same parent, then use the `ORDER` `SIBLINGS` `BY` clause.

START WITH Clause

Specify a condition that identifies the row(s) to be used as the root(s) of a hierarchical query. The `condition` can be any condition as described in [Conditions](Conditions.md#GUID-C2E3ED44-16E7-4924-9125-E1693B1022A8). Oracle Database uses as root(s) all rows that satisfy this condition. If you omit this clause, then the database uses all rows in the table as root rows.

CONNECT BY Clause

Specify a condition that identifies the relationship between parent rows and child rows of the hierarchy. The `condition` can be any condition as described in [Conditions](Conditions.md#GUID-C2E3ED44-16E7-4924-9125-E1693B1022A8). However, it must use the `PRIOR` operator to refer to the parent row.

group\_by\_clause

Specify the `GROUP` `BY` clause if you want the database to group the selected rows based on the value of `expr`(s) for each row and return a single row of summary information for each group. If this clause contains `CUBE` or `ROLLUP` extensions, then the database produces superaggregate groupings in addition to the regular groupings.

Expressions in the `GROUP` `BY` clause can contain any columns of the tables, views, or materialized views in the `FROM` clause, regardless of whether the columns appear in the select list.

The `GROUP` `BY` clause groups rows but does not guarantee the order of the result set. To order the groupings, use the `ORDER` `BY` clause.

ROLLUP

The `ROLLUP` operation in the `simple_grouping_clause` groups the selected rows based on the values of the first n, n-1, n-2, ... 0 expressions in the `GROUP` `BY` specification, and returns a single row of summary for each group. You can use the `ROLLUP` operation to produce subtotal values by using it with the `SUM` function. When used with `SUM`, `ROLLUP` generates subtotals from the most detailed level to the grand total. Aggregate functions such as `COUNT` can be used to produce other kinds of superaggregates.

For example, given three expressions (n=3) in the `ROLLUP` clause of the `simple_grouping_clause`, the operation results in n+1 = 3+1 = 4 groupings.

Rows grouped on the values of the first `n` expressions are called regular rows, and the others are called superaggregate rows.

CUBE

The `CUBE` operation in the `simple_grouping_clause` groups the selected rows based on the values of all possible combinations of expressions in the specification. It returns a single row of summary information for each group. You can use the `CUBE` operation to produce cross-tabulation values.

For example, given three expressions (n=3) in the `CUBE` clause of the `simple_grouping_clause`, the operation results in 2n = 23 = 8 groupings. Rows grouped on the values of `n` expressions are called regular rows, and the rest are called superaggregate rows.

GROUPING SETS

`GROUPING` `SETS` are a further extension of the `GROUP` `BY` clause that let you specify multiple groupings of data. Doing so facilitates efficient aggregation by pruning the aggregates you do not need. You specify just the desired groups, and the database does not need to perform the full set of aggregations generated by `CUBE` or `ROLLUP`. Oracle Database computes all groupings specified in the `GROUPING` `SETS` clause and combines the results of individual groupings with a `UNION` `ALL` operation. The `UNION` `ALL` means that the result set can include duplicate rows.

Within the `GROUP` `BY` clause, you can combine expressions in various ways:

* To specify composite columns, group columns within parentheses so that the database treats them as a unit while computing `ROLLUP` or `CUBE` operations.
* To specify concatenated grouping sets, separate multiple grouping sets, `ROLLUP`, and `CUBE` operations with commas so that the database combines them into a single `GROUP` `BY` clause. The result is a cross-product of groupings from each grouping set.

HAVING Clause

Use the `HAVING` clause to restrict the groups of returned rows to those groups for which the specified `condition` is `TRUE`. If you omit this clause, then the database returns summary rows for all groups.

Specify `GROUP` `BY` and `HAVING` after the `where_clause` and `hierarchical_query_clause`. If you specify both `GROUP` `BY` and `HAVING`, then they can appear in either order.

Restrictions on the GROUP BY Clause

This clause is subject to the following restrictions:

* You cannot specify LOB columns, nested tables, or varrays as part of `expr`.
* The expressions can be of any form except scalar subquery expressions.
* If the `group_by_clause` references any object type columns, then the query will not be parallelized.

model\_clause

The `model_clause` lets you view selected rows as a multidimensional array and randomly access cells within that array. Using the `model_clause`, you can specify a series of cell assignments, referred to as rules, that invoke calculations on individual cells and ranges of cells. These rules operate on the results of a query and do not update any database tables.

When using the `model_clause` in a query, the `SELECT` and `ORDER` `BY` clauses must refer only to those columns defined in the `model_column_clauses`.

main\_model

The `main_model` clause defines how the selected rows will be viewed in a multidimensional array and what rules will operate on which cells in that array.

model\_column\_clauses

The `model_column_clauses` define and classify the columns of a query into three groups: partition columns, dimension columns, and measure columns. For `expr`, you can specify a column, constant, host variable, single-row function, aggregate function, or any expression involving them. If `expr` is a column, then the column alias (`c_alias`) is optional. If `expr` is not a column, then the column alias is required. If you specify a column alias, then you must use the alias to refer to the column in the `model_rules_clause`, `SELECT` list, and the query `ORDER` `BY` clauses.

PARTITION BY

The `PARTITION` `BY` clause specifies the columns that will be used to divide the selected rows into partitions based on the values of the specified columns.

DIMENSION BY

The `DIMENSION` `BY` clause specifies the columns that will identify a row within a partition. The values of the dimension columns, along with those of the partition columns, serve as array indexes to the measure columns within a row.

MEASURES

The `MEASURES` clause identifies the columns on which the calculations can be performed. Measure columns in individual rows are treated like cells that you can reference, by specifying the values for the partition and dimension columns, and update.

cell\_reference\_options

Use the `cell_reference_options` clause to specify how null and absent values are treated in rules and how column uniqueness is constrained.

IGNORE NAV

When you specify `IGNORE` `NAV`, the database returns the following values for the null and absent values of the data type specified:

* Zero for numeric data types
* 01-JAN-2000 for datetime data types
* An empty string for character data types
* Null for all other data types

KEEP NAV

When you specify `KEEP` `NAV`, the database returns null for both null and absent cell values. `KEEP` `NAV` is the default.

UNIQUE SINGLE REFERENCE

When you specify `UNIQUE` `SINGLE` `REFERENCE`, the database checks only single-cell references on the right-hand side of the rule for uniqueness, not the entire query result set.

UNIQUE DIMENSION

When you specify `UNIQUE` `DIMENSION`, the database checks that the `PARTITION` `BY` and `DIMENSION` `BY` columns form a unique key to the query. `UNIQUE` `DIMENSION` is the default.

model\_rules\_clause

Use the `model_rules_clause` to specify the cells to be updated, the rules for updating those cells, and optionally, how the rules are to be applied and processed.

Each rule represents an assignment and consists of a left-hand side and right-hand side. The left-hand side of the rule identifies the cells to be updated by the right-hand side of the rule. The right-hand side of the rule evaluates to the values to be assigned to the cells specified on the left-hand side of the rule.

UPSERT ALL

`UPSERT` `ALL` allows `UPSERT` behavior for a rule with both positional and symbolic references on the left-hand side of the rule. When evaluating an `UPSERT` `ALL` rule, Oracle performs the following steps to create a list of cell references to be upserted:

1. Find the existing cells that satisfy all the symbolic predicates of the cell reference.
2. Using just the dimensions that have symbolic references, find the distinct dimension value combinations of these cells.
3. Perform a cross product of these value combinations with the dimension values specified by way of positional references.

Refer to [Oracle Database Data Warehousing Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/19/sqlrf&id=DWHSG0222) for more information on the semantics of `UPSERT` `ALL`.

UPSERT

When you specify `UPSERT`, the database applies the rules to those cells referenced on the left-hand side of the rule that exist in the multidimensional array, and inserts new rows for those that do not exist. `UPSERT` behavior applies only when positional referencing is used on the left-hand side and a single cell is referenced. `UPSERT` is the default. Refer to [cell\_assignment](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2168603) for more information on positional referencing and single-cell references.

`UPDATE` and `UPSERT` can be specified for individual rules as well. When either `UPDATE` or `UPSERT` is specified for a specific rule, it takes precedence over the option specified in the `RULES` clause.

Note:

If an `UPSERT` `ALL`, `UPSERT`, or `UPDATE` rule does not contain the appropriate predicates, then the database may implicitly convert it to a different type of rule:

* If an `UPSERT` rule contains an existential predicate, then the rule is treated as an `UPDATE` rule.
* An `UPSERT` `ALL` rule must have at least one existential predicate and one qualified predicate on its left side. If it has no existential predicate, then it is treated as an `UPSERT` rule. If it has no qualified predicate, then it is treated as an `UPDATE` rule

UPDATE

When you specify `UPDATE`, the database applies the rules to those cells referenced on the left-hand side of the rule that exist in the multidimensional array. If the cells do not exist, then the assignment is ignored.

AUTOMATIC ORDER

When you specify `AUTOMATIC` `ORDER`, the database evaluates the rules based on their dependency order. In this case, a cell can be assigned a value once only.

SEQUENTIAL ORDER

When you specify `SEQUENTIAL` `ORDER`, the database evaluates the rules in the order they appear. In this case, a cell can be assigned a value more than once. `SEQUENTIAL` `ORDER` is the default.

ITERATE ... [UNTIL]

Use `ITERATE` ... [`UNTIL`] to specify the number of times to cycle through the rules and, optionally, an early termination condition. The parentheses around the `UNTIL` condition are optional.

When you specify `ITERATE` ... [`UNTIL`], rules are evaluated in the order in which they appear. Oracle Database returns an error if both `AUTOMATIC` `ORDER` and `ITERATE` ... `[UNTIL]` are specified in the `model_rules_clause`.

cell\_assignment

The `cell_assignment` clause, which is the left-hand side of the rule, specifies one or more cells to be updated. When a `cell_assignment` references a single cell, it is called a single-cell reference. When more than one cell is referenced, it is called a multiple-cell reference.

All dimension columns defined in the `model_clause` must be qualified in the `cell_assignment` clause. A dimension can be qualified using either symbolic or positional referencing.

A symbolic reference qualifies a single dimension column using a Boolean condition like `dimension_column``=``constant`. A positional reference is one where the dimension column is implied by its position in the `DIMENSION` `BY` clause. The only difference between symbolic references and positional references is in the treatment of nulls.

Using a single-cell symbolic reference such as `a[x=null,y=2000]`, no cells qualify because `x=null` evaluates to `FALSE`. However, using a single-cell positional reference such as `a[null,2000]`, a cell where `x` is null and `y` is 2000 qualifies because null = null evaluates to `TRUE`. With single-cell positional referencing, you can reference, update, and insert cells where dimension columns are null.

You can specify a condition or an expression representing a dimension column value using either symbolic or positional referencing. `condition` cannot contain aggregate functions or the `CV` function, and `condition` must reference a single dimension column. `expr` cannot contain a subquery. Refer to "[Model Expressions](Model-Expressions.md#GUID-83D3FD56-8346-4D3F-A49E-5FE41FE19257)" for information on model expressions.

single\_column\_for\_loop

The `single_column_for_loop` clause lets you specify a range of cells to be updated within a single dimension column.

The `IN` clause lets you specify the values of the dimension column as either a list of values or as a subquery. When using `subquery`, it cannot:

The `FROM` clause lets you specify a range of values for a dimension column with discrete increments within the range. The `FROM` clause can only be used for those columns with a data type for which addition and subtraction is supported. The `INCREMENT` and `DECREMENT` values must be positive.

Optionally, you can specify the `LIKE` clause within the `FROM` clause. In the `LIKE` clause, `pattern` is a character string containing a single pattern-matching character `%`. This character is replaced during execution with the current incremented or decremented value in the `FROM` clause.

If all dimensions other than those used by a `FOR` loop involve a single-cell reference, then the expressions can insert new rows. The number of dimension value combinations generated by `FOR` loops is counted as part of the 10,000 row limit of the `MODEL` clause.

multi\_column\_for\_loop

The `multi_column_for_loop` clause lets you specify a range of cells to be updated across multiple dimension columns. The `IN` clause lets you specify the values of the dimension columns as either multiple lists of values or as a subquery. When using `subquery`, it cannot:

If all dimensions other than those used by a `FOR` loop involve a single-cell reference, then the expressions can insert new rows. The number of dimension value combinations generated by `FOR` loops is counted as part of the 10,000 row limit of the `MODEL` clause.

order\_by\_clause

Use the `ORDER` `BY` clause to specify the order in which cells on the left-hand side of the rule are to be evaluated. The `expr` must resolve to a dimension or measure column. If the `ORDER` `BY` clause is not specified, then the order defaults to the order of the columns as specified in the `DIMENSION` `BY` clause. See [order\_by\_clause](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2171079) for more information.

Restrictions on the order\_by\_clause

Use of the `ORDER` `BY` clause in the model rule is subject to the following restrictions:

* You cannot specify `SIBLINGS`, `position`, or `c_alias` in the `order_by_clause` of the `model_clause`.
* You cannot specify this clause on the left-hand side of the model rule and also specify a `FOR` loop on the right-hand side of the rule.

expr

Specify an expression representing the value or values of the cell or cells specified on the right-hand side of the rule. `expr` cannot contain a subquery. Refer to "[Model Expressions](Model-Expressions.md#GUID-83D3FD56-8346-4D3F-A49E-5FE41FE19257)" for information on model expressions.

return\_rows\_clause

The `return_rows_clause` lets you specify whether to return all rows selected or only those rows updated by the model rules. `ALL` is the default.

reference\_model

Use the `reference_model` clause when you need to access multiple arrays from inside the `model_clause`. This clause defines a read-only multidimensional array based on the results of a query.

The subclauses of the `reference_model` clause have the same semantics as for the `main_model` clause. Refer to [model\_column\_clauses](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2168561) and [cell\_reference\_options](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2168572).

Restrictions on the reference\_model Clause

This clause is subject to the following restrictions:

Set Operators: UNION, UNION ALL, INTERSECT, MINUS

The set operators combine the rows returned by two `SELECT` statements into a single result. The number and data types of the columns selected by each component query must be the same, but the column lengths can be different. The names of the columns in the result set are the names of the expressions in the select list preceding the set operator.

If you combine more than two queries with set operators, then the database evaluates adjacent queries from left to right. The parentheses around the subquery are optional. You can use them to specify a different order of evaluation.

Refer to "[The UNION [ALL], INTERSECT, MINUS Operators](The-UNION-ALL-INTERSECT-MINUS-Operators.md#GUID-B64FE747-586E-4513-945F-80CB197125EE)" for information on these operators, including restrictions on their use.

order\_by\_clause

Use the `ORDER` `BY` clause to order rows returned by the statement. Without an `order_by_clause`, no guarantee exists that the same query executed more than once will retrieve rows in the same order.

SIBLINGS

The `SIBLINGS` keyword is valid only if you also specify the `hierarchical_query_clause` (`CONNECT` `BY`). `ORDER` `SIBLINGS` `BY` preserves any ordering specified in the hierarchical query clause and then applies the `order_by_clause` to the siblings of the hierarchy.

expr

`expr` orders rows based on their value for `expr`. The expression is based on columns in the select list or columns in the tables, views, or materialized views in the `FROM` clause.

position

Specify `position` to order rows based on their value for the expression in this position of the select list. The `position` value must be an integer.

You can specify multiple expressions in the `order_by_clause`. Oracle Database first sorts rows based on their values for the first expression. Rows with the same value for the first expression are then sorted based on their values for the second expression, and so on. The database sorts nulls following all others in ascending order and preceding all others in descending order. Refer to "[Sorting Query Results](Sorting-Query-Results.md#GUID-E45EF993-20AC-4552-860C-4D74EADB5BF2)" for a discussion of ordering query results.

ASC | DESC

Specify whether the ordering sequence is ascending or descending. `ASC` is the default.

NULLS FIRST | NULLS LAST

Specify whether returned rows containing null values should appear first or last in the ordering sequence.

`NULLS` `LAST` is the default for ascending order, and `NULLS` `FIRST` is the default for descending order.

Restrictions on the ORDER BY Clause

The following restrictions apply to the `ORDER` `BY` clause:

* If you have specified the `DISTINCT` operator in this statement, then this clause cannot refer to columns unless they appear in the select list.
* An `order_by_clause` can contain no more than 255 expressions.
* You cannot order by a LOB, `LONG`, or `LONG` `RAW` column, nested table, or varray.
* If you specify a [group\_by\_clause](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__I2182483) in the same statement, then this `order_by_clause` is restricted to the following expressions:

  + Constants
  + Aggregate functions
  + Analytic functions
  + The functions `USER`, `UID`, and `SYSDATE`
  + Expressions identical to those in the `group_by_clause`
  + Expressions comprising the preceding expressions that evaluate to the same value for all rows in a group

row\_limiting\_clause

The `row_limiting_clause` allows you to limit the rows returned by the query. You can specify an offset, and the number of rows or percentage of rows to return. You can use this clause to implement top-N reporting. For consistent results, specify the `order_by_clause` to ensure a deterministic sort order.

OFFSET

Use this clause to specify the number of rows to skip before row limiting begins. `offset` must be a number or an expression that evaluates to a numeric value. If you specify a negative number, then `offset` is treated as 0. If you specify NULL, or a number greater than or equal to the number of rows returned by the query, then 0 rows are returned. If `offset` includes a fraction, then the fractional portion is truncated. If you do not specify this clause, then `offset` is 0 and row limiting begins with the first row.

ROW | ROWS

These keywords can be used interchangeably and are provided for semantic clarity.

FETCH

Use this clause to specify the number of rows or percentage of rows to return. If you do not specify this clause, then all rows are returned, beginning at row `offset` + 1.

FIRST | NEXT

These keywords can be used interchangeably and are provided for semantic clarity.

rowcount | percent PERCENT

Use `rowcount` to specify the number of rows to return. `rowcount` must be a number or an expression that evaluates to a numeric value. If you specify a negative number, then `rowcount` is treated as 0. If `rowcount` is greater than the number of rows available beginning at row `offset` + 1, then all available rows are returned. If `rowcount` includes a fraction, then the fractional portion is truncated. If `rowcount` is NULL, then 0 rows are returned.

Use `percent` `PERCENT` to specify the percentage of the total number of selected rows to return. `percent` must be a number or an expression that evaluates to a numeric value. If you specify a negative number, then `percent` is treated as 0. If `percent` is NULL, then 0 rows are returned.

If you do not specify `rowcount` or `percent` `PERCENT`, then 1 row is returned.

ROW | ROWS

These keywords can be used interchangeably and are provided for semantic clarity.

ONLY | WITH TIES

Specify `ONLY` to return exactly the specified number of rows or percentage of rows.

Specify `WITH` `TIES` to return additional rows with the same sort key as the last row fetched. If you specify `WITH` `TIES`, then you must specify the `order_by_clause`. If you do not specify the `order_by_clause`, then no additional rows will be returned.

Restrictions on the row\_limiting\_clause

This clause is subject to the following restrictions:

* You cannot specify this clause with the `for_update_clause`.
* If you specify this clause, then the select list cannot contain the sequence pseudocolumns `CURRVAL` or `NEXTVAL`.
* Materialized views are not eligible for an incremental refresh if the defining query contains the `row_limiting_clause`.
* If the select list contains columns with identical names and you specify the `row_limiting_clause`, then an ORA-00918 error occurs. This error occurs whether the identically named columns are in the same table or in different tables. You can work around this issue by specifying unique column aliases for the identically named columns.

for\_update\_clause

The `FOR` `UPDATE` clause lets you lock the selected rows so that other users cannot lock or update the rows until you end your transaction. You can specify this clause only in a top-level `SELECT` statement, not in subqueries.

Note:

Prior to updating a LOB value, you must lock the row containing the LOB. One way to lock the row is with an embedded `SELECT` ... `FOR` `UPDATE` statement. You can do this using one of the programmatic languages or `DBMS_LOB` package. For more information on lock rows before writing to a LOB, see [Oracle Database SecureFiles and Large Objects Developer's Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/19/sqlrf&id=ADLOB1004).

Nested table rows are not locked as a result of locking the parent table rows. If you want the nested table rows to be locked, then you must lock them explicitly.

Restrictions on the FOR UPDATE Clause

This clause is subject to the following restrictions:

* You cannot specify this clause with the following other constructs: the `DISTINCT` operator, `CURSOR` expression, set operators, `group_by_clause`, or aggregate functions.
* The tables locked by this clause must all be located on the same database and on the same database as any `LONG` columns and sequences referenced in the same statement.

Using the FOR UPDATE Clause on Views

In general, this clause is not supported on views. However, in some cases, a `SELECT` ... `FOR` `UPDATE` query on a view can succeed without any errors. This occurs when the view has been merged to its containing query block internally by the query optimizer, and `SELECT` ... `FOR` `UPDATE` succeeds on the internally transformed query. The examples in this section illustrate when using the `FOR` `UPDATE` clause on a view can succeed or fail.

* Using the `FOR` `UPDATE` clause on merged views

  An error can occur when you use the `FOR` `UPDATE` clause on a merged view if both of the following conditions apply:

  The following statement succeeds because the underlying column of the view is not an expression:

  ```
  SELECT employee_id FROM (SELECT * FROM employees)
     FOR UPDATE OF employee_id;
  ```

  The following statement succeeds because, while the underlying column of the view is an expression, the `FOR` `UPDATE` clause does not apply to a column list:

  ```
  SELECT employee_id FROM (SELECT employee_id+1 AS employee_id FROM employees)
     FOR UPDATE;
  ```

  The following statement fails because the underlying column of the view is an expression and the `FOR` `UPDATE` clause applies to a column list:

  ```
  SELECT employee_id FROM (SELECT employee_id+1 AS employee_id FROM employees)
     FOR UPDATE OF employee_id;
                   *
  Error at line 2:
  ORA-01733: virtual column not allowed here
  ```
* Using the `FOR` `UPDATE` clause on non-merged views

  Since the `FOR` `UPDATE` clause is not supported on views, anything that prevents view merging, such as the `NO_MERGE` hint, parameters that disallow view merging, or something in the query structure that prevents view merging, will result in an `ORA-02014` error.

  In the following example, the `GROUP` `BY` statement prevents view merging, which causes an error:

  ```
  SELECT avgsal
     FROM (SELECT AVG(salary) AS avgsal FROM employees GROUP BY job_id)
     FOR UPDATE;
  FROM (SELECT AVG(salary) AS avgsal FROM employees GROUP BY job_id)
       *
  ERROR at line 2:
  ORA-02014: cannot select FOR UPDATE from view with DISTINCT, GROUP BY, etc.
  ```

Note:

Due to the complexity of the view merging mechanism, Oracle recommends against using the `FOR` `UPDATE` clause on views.

OF ... column

Use the `OF` ... `column` clause to lock the select rows only for a particular table or view in a join. The columns in the `OF` clause only indicate which table or view rows are locked. The specific columns that you specify are not significant. However, you must specify an actual column name, not a column alias. If you omit this clause, then the database locks the selected rows from all the tables in the query.

NOWAIT | WAIT

The `NOWAIT` and `WAIT` clauses let you tell the database how to proceed if the `SELECT` statement attempts to lock a row that is locked by another user.

If you specify neither `WAIT` nor `NOWAIT`, then the database waits until the row is available and then returns the results of the `SELECT` statement.

SKIP LOCKED

`SKIP` `LOCKED` is an alternative way to handle a contending transaction that is locking some rows of interest. Specify `SKIP` `LOCKED` to instruct the database to attempt to lock the rows specified by the `WHERE` clause and to skip any rows that are found to be already locked by another transaction. This feature is designed for use in multiconsumer queue environments. It enables queue consumers to skip rows that are locked by other consumers and obtain unlocked rows without waiting for the other consumers to finish. Refer to [Oracle Database Advanced Queuing User's Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/19/sqlrf&id=ADQUE2835) for more information.

Note on the WAIT and SKIP LOCKED Clauses

If you specify `WAIT` or `SKIP` `LOCKED` and the table is locked in exclusive mode, then the database will not return the results of the `SELECT` statement until the lock on the table is released. In the case of `WAIT`, the `SELECT` `FOR` `UPDATE` clause is blocked regardless of the wait time specified.

row\_pattern\_clause

The `MATCH_RECOGNIZE` clause lets you perform pattern matching. Use this clause to recognize patterns in a sequence of rows in `table`, which is called the row pattern input table. The result of a query that uses the `MATCH_RECOGNIZE` clause is called the row pattern output table.

The `MATCH_RECOGNIZE` enables you to do the following tasks:

* Logically partition and order the data with the `PARTITION` `BY` and `ORDER` `BY` clauses.
* Define measures, which are expressions usable in other parts of the SQL query, in the `MEASURES` clause.
* Define patterns of rows to seek using the `PATTERN` clause. These patterns use regular expression syntax, a powerful and expressive feature, applied to the pattern variables you define.
* Specify the logical conditions required to map a row to a row pattern variable in the `DEFINE` clause.

row\_pattern\_partition\_by

Specify `PARTITION` `BY` to divide the rows in the row pattern input table into logical groups called row pattern partitions. Use `column` to specify one or more partitioning columns. Each partition consists of the set of rows in the row pattern input table that have the same value(s) on the partitioning column(s).

If you specify this clause, then matches are found within partitions and do not cross partition boundaries. If you do not specify this clause, then all rows of the row input table constitute a single row pattern partition.

row\_pattern\_order\_by

Specify `ORDER` `BY` to order rows within each row pattern partition. Use `column` to specify one or more ordering columns. If you specify multiple columns, then Oracle Database first sorts rows based on their values for the first column. Rows with the same value for the first column are then sorted based on their values for the second column, and so on. Oracle Database sorts nulls following all others in ascending order.

If you do not specify this clause, then the result of the `row_pattern_clause` is nondeterministic and you may get inconsistent results each time you run the query.

row\_pattern\_measures

Use the `MEASURES` clause to define one or more row pattern measure columns. These columns are included in the row pattern output table and contain values that are useful for analyzing data.

When you define a row pattern measure column, using the `row_pattern_measure_column` clause, you specify its pattern measure expression. The values in the column are calculated by evaluating the pattern measure expression whenever a match is found.

row\_pattern\_measure\_column

Use this clause to define a row pattern measure column.

* For `expr`, specify the pattern measure expression. A pattern measure expression is an expression as described in [Expressions](Expressions.md#GUID-E7A5363C-AEE9-4809-99C1-1A9C6E3AE017) that can contain only the following elements:

  + Constants: Text literals and numeric literals
  + References to any column of the row pattern input table
  + The `CLASSIFIER` function, which returns the name of the primary row pattern variable to which the row is mapped. Refer to [row\_pattern\_classifier\_func](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABBGAAB) for more information.
  + The `MATCH_NUMBER` function, which returns the sequential number of a row pattern match within the row pattern partition. Refer to [row\_pattern\_match\_num\_func](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABBEEBD) for more information.
  + Row pattern navigation functions: `PREV`, `NEXT`, `FIRST`, and `LAST`. Refer to [row\_pattern\_navigation\_func](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABGCIIA) for more information.
  + Row pattern aggregate functions: [AVG](AVG.md#GUID-B64BCBF1-DAA0-4D88-9821-2C4D3FDE5E4A), [COUNT](COUNT.md#GUID-AEF08B79-024D-4E3A-B362-9715FB011776), [MAX](MAX.md#GUID-E5372020-A6DA-44BF-93BE-DA8C3F74CD01), [MIN](MIN.md#GUID-F7F04E18-1AD8-4D15-9491-4622AD847A74), or [SUM](SUM.md#GUID-5610BE2C-CFE5-446F-A1F7-B924B5663220). Refer to [row\_pattern\_aggregate\_func](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABIDJGB) for more information.
* For `c_alias`, specify the alias for the pattern measure expression. Oracle Database uses this alias in the column heading of the row pattern output table. The `AS` keyword is optional. The alias can be used in other parts of the query, such as the `SELECT` ... `ORDER` `BY` clause.

row\_pattern\_rows\_per\_match

This clause lets you specify whether the row pattern output table includes summary or detailed data about each match.

* If you specify `ONE` `ROW` `PER` `MATCH`, then each match produces one summary row. This is the default.
* If you specify `ALL` `ROWS` `PER` `MATCH`, then each match that spans multiple rows will produce one output row for each row in the match.

row\_pattern\_skip\_to

This clause lets you specify the point to resume row pattern matching after a non-empty match is found.

* Specify `AFTER` `MATCH` `SKIP` `TO` `NEXT` `ROW` to resume pattern matching at the row after the first row of the current match.
* Specify `AFTER` `MATCH` `SKIP` `PAST` `LAST` `ROW` to resume pattern matching at the next row after the last row of the current match. This is the default.
* Specify `AFTER` `MATCH` `SKIP` `TO` `FIRST` `variable_name` to resume pattern matching at the first row that is mapped to pattern variable `variable_name`. The `variable_name` must be defined in the `DEFINE` clause.
* Specify `AFTER` `MATCH` `SKIP` `TO` `LAST` `variable_name` to resume pattern matching at the last row that is mapped to pattern variable `variable_name`. The `variable_name` must be defined in the `DEFINE` clause.
* `AFTER` `MATCH` `SKIP` `TO` `variable_name` has the same behavior as `AFTER` `MATCH` `SKIP` `TO` `LAST` `variable_name`.

PATTERN

Use the `PATTERN` clause to define which pattern variables must be matched, the sequence in which they must be matched, and the quantity of rows that must be matched for each pattern variable.

A row pattern match consists of a set of contiguous rows in a row pattern partition. Each row of the match is mapped to a pattern variable. The mapping of rows to pattern variables must conform to the regular expression specified in the `row_pattern` clause, and all conditions in the `DEFINE` clause must be true.

Note:

It is outside the scope of this document to explain regular expression concepts and details. If you are not familiar with regular expressions, then you are encouraged to familiarize yourself with the topic using other sources.

The precedence of the elements that you specify in the regular expression of the `PATTERNS` clause, in decreasing order, is as follows:

* Row pattern elements (specified in the `row_pattern_primary` clause)
* Row pattern quantifiers (specified in the `row_pattern_quantifier` clause)
* Concatenation (specified in the `row_pattern_term` clause)
* Alternation (specified in the `row_pattern` clause)

row\_pattern

Use this clause to specify the row pattern. A row pattern is a regular expression that can take one of the following forms:

* A single row pattern term

  For example: `PATTERN(A)`
* A row pattern, a vertical bar, and a row pattern term

  For example: `PATTERN(A|B)`
* A recursively built row pattern, a vertical bar, and a row pattern term

  For example: `PATTERN(A|B|C)`

The vertical bar in this clause represents alternation. Alternation matches a single regular expression from a list of several possible regular expressions. Alternatives are preferred in the order they are specified. For example, if you specify `PATTERN(A|B|C)`, then Oracle Database attempts to match `A` first. If `A` is not matched, then it attempts to match `B`. If `B` is not matched, then it attempts to match `C`.

row\_pattern\_term

This clause lets you specify a row pattern term. A row pattern term can take one of the following forms:

* A single row pattern factor

  For example: `PATTERN(A)`
* A row pattern term followed by a row pattern factor.

  For example: `PATTERN(A B)`
* A recursively built row pattern term followed by a row pattern factor

  For example: `PATTERN(A B C)`

The syntax used in the second and third examples represents concatenation. Concatenation is used to list two or more items in a pattern to be matched and the order in which they are to be matched. For example, if you specify `PATTERN(A B C)`, then Oracle Database first matches `A`, then uses the resulting matched rows to match `B`, then uses the resulting matched rows to match `C`. Only rows that match `A`, `B`, and `C`, are included in the row pattern match.

row\_pattern\_factor

This clause lets you specify a row pattern factor. A row pattern factor consists of a row pattern element, specified using the `row_pattern_primary` clause, and an optional row pattern quantifier, specified using the `row_pattern_quantifier` clause.

row\_pattern\_primary

Use this clause to specify the row pattern element. [Table 19-1](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABIDGEJ "First column lists row pattern quantifiers; second column provides descriptions.") lists the valid row pattern elements and their descriptions.

Table 19-1 Row Pattern Elements

| Row Pattern Element | Description |
| --- | --- |
| `variable_name` | Specify a primary pattern variable name that is defined in the `row_pattern_definition` clause. You cannot specify a union pattern variable that is defined in the `row_pattern_subset_item` clause. |
| `$` | `$` matches the position after the last row in the partition. This element is an anchor. Anchors work in terms of positions rather than rows. |
| `^` | `^` matches the position before the first row in the partition. This element is an anchor. Anchors work in terms of positions rather than rows |
| `(` `[``row_pattern``]` `)` | Use `row_pattern` to specify the row pattern to be matched. An empty pattern `()` matches an empty set of rows. |
| `{-` `row_pattern` `-}` | Exclusion syntax. Use `row_pattern` to specify parts of the pattern to be excluded from the output of `ALL` `ROWS` `PER` `MATCH`. |
| `row_pattern_permute` | Use `row_pattern_permute` to specify a pattern that is a permutation of row pattern elements. Refer to [row\_pattern\_permute](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABEEAJJ) for the full semantics of this clause. |

row\_pattern\_permute

Use the `PERMUTE` clause to express a pattern that is a permutation of the specified row pattern elements. For example, `PATTERN` `(PERMUTE` `(A,` `B,` `C))` is equivalent to an alternation of all permutations of the three row pattern elements `A`, `B`, and `C`, similar to the following:

```
PATTERN (A B C | A C B | B A C | B C A | C A B | C B A)
```

Note that the row pattern elements are expanded lexicographically and that each element to permute must be separated by a comma from the other elements.

row\_pattern\_quantifier

Use this clause to specify the row pattern quantifier, which is a postfix operator that defines the number of iterations accepted for a match.

Row pattern quantifiers are referred to as greedy; they will attempt to match as many instances of the regular expression on which they are applied as possible. The exception is row pattern quantifiers that have a question mark (`?`) as a suffix, which are referred to as reluctant. They will attempt to match as few instances as possible of the regular expression on which they are applied.

[Table 19-2](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABGAGEF "First column lists row pattern quantifiers; second column provides descriptions.") lists the valid row pattern quantifiers and the number of iterations they accept for a match. In this table, `n` and `m` represent unsigned integers.

Table 19-2 Row Pattern Quantifiers

| Row Pattern Quantifier | Number of Iterations Accepted for a Match |
| --- | --- |
| `*` | 0 or more iterations (greedy) |
| `*?` | 0 or more iterations (reluctant) |
| `+` | 1 or more iterations (greedy) |
| `+?` | 1 or more iterations (reluctant) |
| `?` | 0 or 1 iterations (greedy) |
| `??` | 0 or 1 iterations (reluctant) |
| `{``n``,}` | `n` or more iterations, (`n` >= 0) (greedy) |
| `{``n``,}?` | `n` or more iterations, (`n` >= 0) (reluctant) |
| `{``n``,``m``}` | Between `n` and `m` iterations, inclusive, (0 <= `n` <= `m`, 0 < `m`) (greedy) |
| `{``n``,``m``}?` | Between `n` and `m` iterations, inclusive, (0 <= `n` <= `m`, 0 < `m`) (reluctant) |
| `{,``m``}` | Between 0 and `m` iterations, inclusive (`m` > 0) (greedy) |
| `{,``m``}?` | Between 0 and `m` iterations, inclusive (`m` > 0) (reluctant) |
| `{``n``}?` | `n` iterations, (`n` > 0) |

row\_pattern\_subset\_clause

The `SUBSET` clause lets you specify one or more union row pattern variables. Use the `row_pattern_subset_item` clause to declare each union row pattern variable.

You can specify union row pattern variables in the following clauses:

* `MEASURES` clause: In the expression for a row pattern measure column. That is, in expression `expr` of the `row_pattern_measure_column` clause.
* `DEFINE` clause: In the condition that defines a primary pattern variable. That is, in `condition` of the `row_pattern_definition` clause

row\_pattern\_subset\_item

This clause lets you create a grouping of multiple pattern variables that can be referred to with a variable name of its own. The variable name that refers to this grouping is called a union row pattern variable.

* For `variable_name` on the left side of the equal sign, specify the name of the union row pattern variable.
* On the right side of the equal sign, specify a comma-separated list of distinct primary row pattern variables within parentheses. This list cannot include any union row pattern variables.

DEFINE

Use the `DEFINE` clause to specify one or more row pattern definitions. A row pattern definition specifies the conditions that a row must meet in order to be mapped to a specific pattern variable.

The `DEFINE` clause only supports running semantics.

row\_pattern\_definition\_list

This clause lets you specify one or more row pattern definitions.

row\_pattern\_definition

This clause lets you specify a row pattern definition, which contains the conditions that a row must meet in order to be mapped to the specified pattern variable.

row\_pattern\_rec\_func

This clause comprises the following clauses, which let you specify row pattern recognition functions:

* `row_pattern_classifier_func`: Use this clause to specify the `CLASSIFIER` function, which returns a character string whose value is the name of the variable to which the row is mapped.
* `row_pattern_match_num_func`: Use this clause to specify the `MATCH_NUMBER` function, which returns a numeric value with scale 0 (zero) whose value is the sequential number of the match within the row pattern partition.
* `row_pattern_navigation_func`: Use this clause to specify functions that perform row pattern navigation operations.
* `row_pattern_aggregate_func`: Use this clause to specify an aggregate function in the expression for a row pattern measure column or in the condition that defines a primary pattern variable.

You can specify row pattern recognition functions in the following clauses:

* `MEASURES` clause: In the expression for a row pattern measure column. That is, in expression `expr` of the `row_pattern_measure_column` clause.
* `DEFINE` clause: In the condition that defines a primary pattern variable. That is, in `condition` of the `row_pattern_definition` clause

A row pattern recognition function may behave differently depending whether you specify it in the `MEASURES` or `DEFINE` clause. These details are explained in the semantics for each clause.

row\_pattern\_classifier\_func

The `CLASSIFIER` function returns a character string whose value is the name of the variable to which the row is mapped.

* In the `MEASURES` clause:

  + If you specify `ONE` `ROW` `PER` `MATCH`, then the query uses the last row of the match when processing the `MEASURES` clause, so the `CLASSIFIER` function returns the name of the pattern variable to which the last row of the match is mapped.
  + If you specify `ALL` `ROWS` `PER` `MATCH`, then for each row of the match found, the `CLASSIFIER` function returns the name of the pattern variable to which the row is mapped.

  For empty matchesâthat is, matches that contain no rows, the `CLASSIFER` function returns NULL.
* In the `DEFINE` clause, the `CLASSIFIER` function returns the name of the primary pattern variable to which the current row is mapped.

row\_pattern\_match\_num\_func

The `MATCH_NUMBER` function returns a numeric value with scale 0 (zero) whose value is the sequential number of the match within the row pattern partition.

Matches within a row pattern partition are numbered sequentially starting with 1 in the order in which they are found. If multiple rows satisfy a match, then they are all assigned the same match number. Note that match numbering starts over again at 1 in each row pattern partition, because there is no inherent ordering between row pattern partitions.

* In the `MEASURES` clause: You can use `MATCH_NUMBER` to obtain the sequential number of the match within the row pattern.
* In the `DEFINE` clause: You can use `MATCH_NUMBER` to define conditions that depend upon the match number.

row\_pattern\_navigation\_func

This clause lets you perform the following row pattern navigation operations:

* Navigate among the group of rows mapped to a pattern variable using the `FIRST` and `LAST` functions of the `row_pattern_nav_logical` clause.
* Navigate among all rows in a row pattern partition using the `PREV` and `NEXT` functions of the `row_pattern_nav_physical` clause
* Nest the `FIRST` or `LAST` function within the `PREV` or `NEXT` function using the `row_pattern_nav_compound` clause.

row\_pattern\_nav\_logical

This clause lets you use the `FIRST` and `LAST` functions to navigate among the group of rows mapped to a pattern variable using an optional logical offset.

* The `FIRST` function returns the value of expression `expr` when evaluated in the first row of the group of rows mapped to the pattern variable that is specified in `expr`. If no rows are mapped to the pattern variable, then the `FIRST` function returns NULL.
* The `LAST` function returns the value of expression `expr` when evaluated in the last row of the group of rows mapped to the pattern variable that is specified in `expr`. If no rows are mapped to the pattern variable, then the `LAST` function returns NULL.
* Use `expr` to specify the expression to be evaluated. It must contain at least one row pattern column reference. If it contains more than one row pattern column reference, then all must refer to the same pattern variable.
* Use the optional `offset` to specify the logical offset within the set of rows mapped to the pattern variable. When specified with the `FIRST` function, the offset is the number of rows from the first row, in ascending order. When specified with the `LAST` function, the offset is the number of rows from the last row in descending order. The default offset is 0.

  For `offset`, specify a non-negative integer. It must be a runtime constant (literal, bind variable, or expressions involving them), but not a column or subquery.

  If you specify an `offset` that is greater than or equal to the number of rows mapped to the pattern variable minus 1, then the function returns NULL.

You can specify running or final semantics for the `FIRST` and `LAST` functions as follows:

* The `MEASURES` clause supports running and final semantics. Specify `RUNNING` for running semantics. Specify `FINAL` for final semantics. The default is `RUNNING`.
* The `DEFINE` clause supports only running semantics. Therefore, running semantics will be used whether you specify or omit `RUNNING`. You cannot specify `FINAL`.

row\_pattern\_nav\_physical

This clause lets you use the `PREV` and `NEXT` functions to navigate all rows in a row pattern partition using an optional physical offset.

* The `PREV` function returns the value of expression `expr` when evaluated in the previous row in the partition. If there is no previous row in the partition, then the `PREV` function returns NULL.
* The `NEXT` function returns the value of expression `expr` when evaluated in the next row in the partition. If there is no next row in the partition, then the NEXT function returns NULL.
* Use `expr` to specify the expression to be evaluated. It must contain at least one row pattern column reference. If it contains more than one row pattern column reference, then all must refer to the same pattern variable.
* Use the optional `offset` to specify the physical offset within the partition. When specified with the `PREV` function, it is the number of rows before the current row. When specified with the `NEXT` function, it is the number of rows after the current row. The default is 1. If you specify an offset of 0, then the current row is evaluated.

  For `offset`, specify a non-negative integer. It must be a runtime constant (literal, bind variable, or expressions involving them), but not a column or subquery.

The `PREV` and `NEXT` functions always use running semantics. Therefore, you cannot specify the `RUNNING` or `FINAL` keywords with this clause.

row\_pattern\_nav\_compound

This clause lets you nest the `row_pattern_nav_logical` clause within the `row_pattern_nav_physical` clause. That is, it lets you nest the `FIRST` or `LAST` function within the `PREV` or `NEXT` function. The `row_pattern_nav_logical` clause is evaluated first and then the result is supplied to the `row_pattern_nav_physical` clause.

Refer to [row\_pattern\_nav\_logical](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABHCBFE) and [row\_pattern\_nav\_physical](SELECT.md#GUID-CFA006CA-6FF1-4972-821E-6996142A51C6__BABFIFBC) for the full semantics of these clauses.

row\_pattern\_aggregate\_func

This clause lets you use an aggregate function in the expression for a row pattern measure column or in the condition that defines a primary pattern variable.

For `aggregate_function`, specify any one of the [AVG](AVG.md#GUID-B64BCBF1-DAA0-4D88-9821-2C4D3FDE5E4A), [COUNT](COUNT.md#GUID-AEF08B79-024D-4E3A-B362-9715FB011776), [MAX](MAX.md#GUID-E5372020-A6DA-44BF-93BE-DA8C3F74CD01), [MIN](MIN.md#GUID-F7F04E18-1AD8-4D15-9491-4622AD847A74), or [SUM](SUM.md#GUID-5610BE2C-CFE5-446F-A1F7-B924B5663220) functions. The `DISTINCT` keyword is not supported.

You can specify running or final semantics for aggregate functions as follows:

* The `MEASURES` clause supports running and final semantics. Specify `RUNNING` for running semantics. Specify `FINAL` for final semantics. The default is `RUNNING`.
* The `DEFINE` clause supports only running semantics. Therefore, running semantics will be used whether you specify or omit `RUNNING`. You cannot specify `FINAL`.

Examples

SQL Macros - Table Valued Macros: Examples

The macro function `budget` computes the amount of each department's budget for a given job. It returns the number of employees in each department with the specified job title.

```
create or replace function budget(job varchar2) return varchar2 SQL_MACRO is
begin
  return q'{
     select deptno, sum(sal) budget 
     from emp 
     where job = budget.job
     group by deptno
  }';
end;
/
```

```
SELECT * FROM budget ('MANAGER');
   DEPTNO     BUDGET
–----------  –-------
     20       2975
     30       2850
     10       2450
```

Using a PL/SQL Function in the WITH Clause: Examples

The following example declares and defines a PL/SQL function `get_domain` in the `WITH` clause. The `get_domain` function returns the domain name from a URL string, assuming that the URL string has the "`www`" prefix immediately preceding the domain name, and the domain name is separated by dots on the left and right. The `SELECT` statement uses `get_domain` to find distinct catalog domain names from the `orders` table in the `oe` schema.

```
WITH
 FUNCTION get_domain(url VARCHAR2) RETURN VARCHAR2 IS
   pos BINARY_INTEGER;
   len BINARY_INTEGER;
 BEGIN
   pos := INSTR(url, 'www.');
   len := INSTR(SUBSTR(url, pos + 4), '.') - 1;
   RETURN SUBSTR(url, pos + 4, len);
 END;
SELECT DISTINCT get_domain(catalog_url)
  FROM product_information;
/
```

Subquery Factoring: Example

The following statement creates the query names `dept_costs` and `avg_cost` for the initial query block containing a join, and then uses the query names in the body of the main query.

```
WITH 
   dept_costs AS (
      SELECT department_name, SUM(salary) dept_total
         FROM employees e, departments d
         WHERE e.department_id = d.department_id
      GROUP BY department_name),
   avg_cost AS (
      SELECT SUM(dept_total)/COUNT(*) avg
      FROM dept_costs)
SELECT * FROM dept_costs
   WHERE dept_total >
      (SELECT avg FROM avg_cost)
      ORDER BY department_name;

DEPARTMENT_NAME                DEPT_TOTAL
------------------------------ ----------
Sales                              304500
Shipping                           156400
```

Recursive Subquery Factoring: Examples

The following statement shows the employees who directly or indirectly report to employee 101 and their reporting level.

```
WITH
  reports_to_101 (eid, emp_last, mgr_id, reportLevel) AS
  (
     SELECT employee_id, last_name, manager_id, 0 reportLevel
     FROM employees
     WHERE employee_id = 101
   UNION ALL
     SELECT e.employee_id, e.last_name, e.manager_id, reportLevel+1
     FROM reports_to_101 r, employees e
     WHERE r.eid = e.manager_id
  )
SELECT eid, emp_last, mgr_id, reportLevel
FROM reports_to_101
ORDER BY reportLevel, eid;

       EID EMP_LAST                      MGR_ID REPORTLEVEL
---------- ------------------------- ---------- -----------
       101 Kochhar                          100           0
       108 Greenberg                        101           1
       200 Whalen                           101           1
       203 Mavris                           101           1
       204 Baer                             101           1
       205 Higgins                          101           1
       109 Faviet                           108           2
       110 Chen                             108           2
       111 Sciarra                          108           2
       112 Urman                            108           2
       113 Popp                             108           2
       206 Gietz                            205           2
```

The following statement shows employees who directly or indirectly report to employee 101, their reporting level, and their management chain.

```
WITH
  reports_to_101 (eid, emp_last, mgr_id, reportLevel, mgr_list) AS
  (
     SELECT employee_id, last_name, manager_id, 0 reportLevel,
            CAST(manager_id AS VARCHAR2(2000))
     FROM employees
     WHERE employee_id = 101
  UNION ALL
     SELECT e.employee_id, e.last_name, e.manager_id, reportLevel+1,
            CAST(mgr_list || ',' || manager_id AS VARCHAR2(2000))
     FROM reports_to_101 r, employees e
     WHERE r.eid = e.manager_id
  )
SELECT eid, emp_last, mgr_id, reportLevel, mgr_list
FROM reports_to_101
ORDER BY reportLevel, eid;

        EID EMP_LAST                      MGR_ID REPORTLEVEL MGR_LIST
 ---------- ------------------------- ---------- ----------- --------
       101 Kochhar                          100           0  100
       108 Greenberg                        101           1  100,101
       200 Whalen                           101           1  100,101
       203 Mavris                           101           1  100,101
       204 Baer                             101           1  100,101
       205 Higgins                          101           1  100,101
       109 Faviet                           108           2  100,101,108
       110 Chen                             108           2  100,101,108
       111 Sciarra                          108           2  100,101,108
       112 Urman                            108           2  100,101,108
       113 Popp                             108           2  100,101,108
       206 Gietz                            205           2  100,101,205
```

The following statement shows the employees who directly or indirectly report to employee 101 and their reporting level. It stops at reporting level 1.

```
WITH
  reports_to_101 (eid, emp_last, mgr_id, reportLevel) AS
  (
    SELECT employee_id, last_name, manager_id, 0 reportLevel
    FROM employees
    WHERE employee_id = 101
  UNION ALL
    SELECT e.employee_id, e.last_name, e.manager_id, reportLevel+1
    FROM reports_to_101 r, employees e
    WHERE r.eid = e.manager_id
  )
SELECT eid, emp_last, mgr_id, reportLevel
FROM reports_to_101
WHERE reportLevel <= 1
ORDER BY reportLevel, eid;

       EID EMP_LAST                      MGR_ID REPORTLEVEL
---------- ------------------------- ---------- -----------
       101 Kochhar                          100           0
       108 Greenberg                        101           1
       200 Whalen                           101           1
       203 Mavris                           101           1
       204 Baer                             101           1
       205 Higgins                          101           1
```

The following statement shows the entire organization, indenting for each level of management.

```
WITH
  org_chart (eid, emp_last, mgr_id, reportLevel, salary, job_id) AS
  (
    SELECT employee_id, last_name, manager_id, 0 reportLevel, salary, job_id
    FROM employees
    WHERE manager_id is null
  UNION ALL
    SELECT e.employee_id, e.last_name, e.manager_id,
           r.reportLevel+1 reportLevel, e.salary, e.job_id
    FROM org_chart r, employees e
    WHERE r.eid = e.manager_id
  )
  SEARCH DEPTH FIRST BY emp_last SET order1
SELECT lpad(' ',2*reportLevel)||emp_last emp_name, eid, mgr_id, salary, job_id
FROM org_chart
ORDER BY order1;

EMP_NAME                    EID     MGR_ID     SALARY JOB_ID
-------------------- ---------- ---------- ---------- ----------
King                        100                 24000 AD_PRES
  Cambrault                 148        100      11000 SA_MAN
    Bates                   172        148       7300 SA_REP
    Bloom                   169        148      10000 SA_REP
    Fox                     170        148       9600 SA_REP
    Kumar                   173        148       6100 SA_REP
    Ozer                    168        148      11500 SA_REP
    Smith                   171        148       7400 SA_REP
  De Haan                   102        100      17000 AD_VP
    Hunold                  103        102       9000 IT_PROG
      Austin                105        103       4800 IT_PROG
      Ernst                 104        103       6000 IT_PROG
      Lorentz               107        103       4200 IT_PROG
      Pataballa             106        103       4800 IT_PROG
  Errazuriz                 147        100      12000 SA_MAN
    Ande                    166        147       6400 SA_REP
. . .
```

The following statement shows the entire organization, indenting for each level of management, with each level ordered by `hire_date`. The value of `is_cycle` is set to `Y` for any employee who has the same `hire_date` as any manager above him in the management chain.

```
WITH
  dup_hiredate (eid, emp_last, mgr_id, reportLevel, hire_date, job_id) AS
  (
    SELECT employee_id, last_name, manager_id, 0 reportLevel, hire_date, job_id
    FROM employees
    WHERE manager_id is null
  UNION ALL
    SELECT e.employee_id, e.last_name, e.manager_id,
           r.reportLevel+1 reportLevel, e.hire_date, e.job_id
    FROM dup_hiredate r, employees e
    WHERE r.eid = e.manager_id
  )
  SEARCH DEPTH FIRST BY hire_date SET order1
  CYCLE hire_date SET is_cycle TO 'Y' DEFAULT 'N'
SELECT lpad(' ',2*reportLevel)||emp_last emp_name, eid, mgr_id,
       hire_date, job_id, is_cycle
FROM dup_hiredate
ORDER BY order1;

EMP_NAME                    EID     MGR_ID HIRE_DATE JOB_ID     IS_CYCLE
-------------------- ---------- ---------- --------- ---------- --------
King                        100            17-JUN-03 AD_PRES           N
  De Haan                   102        100 13-JAN-01 AD_VP             N
    Hunold                  103        102 03-JAN-06 IT_PROG           N
      Austin                105        103 25-JUN-05 IT_PROG           N
. . .
  Kochhar                   101        100 21-SEP-05 AD_VP             N
    Mavris                  203        101 07-JUN-02 HR_REP            N
    Baer                    204        101 07-JUN-02 PR_REP            N
    Higgins                 205        101 07-JUN-02 AC_MGR            N
      Gietz                 206        205 07-JUN-02 AC_ACCOUNT        Y
    Greenberg               108        101 17-AUG-02 FI_MGR            N
      Faviet                109        108 16-AUG-02 FI_ACCOUNT        N
      Chen                  110        108 28-SEP-05 FI_ACCOUNT        N
. . .
```

The following statement counts the number of employees under each manager.

```
WITH
  emp_count (eid, emp_last, mgr_id, mgrLevel, salary, cnt_employees) AS
  (
    SELECT employee_id, last_name, manager_id, 0 mgrLevel, salary, 0 cnt_employees
    FROM employees
  UNION ALL
    SELECT e.employee_id, e.last_name, e.manager_id,
           r.mgrLevel+1 mgrLevel, e.salary, 1 cnt_employees
    FROM emp_count r, employees e
    WHERE e.employee_id = r.mgr_id
  )
  SEARCH DEPTH FIRST BY emp_last SET order1
SELECT emp_last, eid, mgr_id, salary, sum(cnt_employees), max(mgrLevel) mgrLevel
FROM emp_count
GROUP BY emp_last, eid, mgr_id, salary
HAVING max(mgrLevel) > 0
ORDER BY mgr_id NULLS FIRST, emp_last;

EMP_LAST                  EID     MGR_ID     SALARY SUM(CNT_EMPLOYEES)   MGRLEVEL
------------------ ---------- ---------- ---------- ------------------ ----------
King                      100                 24000                106          3
Cambrault                 148        100      11000                  7          2
De Haan                   102        100      17000                  5          2
Errazuriz                 147        100      12000                  6          1
Fripp                     121        100       8200                  8          1
Hartstein                 201        100      13000                  1          1
Kaufling                  122        100       7900                  8          1
. . .
```

Analytic Views: Examples

The following statement uses the persistent analytic view sales\_av. The query selects the `member_name` hierarchical attribute of time\_hier, which is the alias of a hierarchy of the same name, and values from the sales and units measures of the analytic view that are dimensioned by the time attribute dimension used by the time\_hier hierarchy.. The results of the selection are filtered to those for the YEAR level of the hierarchy. The results are returned in hierarchical order.

```
SELECT time_hier.member_name as TIME,
 sales,
 units
FROM
 sales_av HIERARCHIES(time_hier)
WHERE time_hier.level_name = 'YEAR'
ORDER BY time_hier.hier_order;
```

The results of the query are the following:

```
TIME    SALES           UNITS
------  -------------  ---------
CY2011  6755115980.73  24462444
CY2012  6901682398.95  24400619
CY2013  7240938717.57  24407259
CY2014  7579746352.89  24402666
CY2015  7941102885.15  24475206
```

Transitory Analytic View Examples

The following statement defines the transitory analytic view my\_av in the `WITH` clause. The transitory analytic view is based on the persistent analytic view sales\_av. The lag\_sales calculated measure is a `LAG` calculation that is used at query time.

```
WITH
  my_av ANALYTIC VIEW AS (
    USING sales_av HIERARCHIES (time_hier)
    ADD MEASURES (
      lag_sales AS (LAG(sales) OVER (HIERARCHY time_hier OFFSET 1))
    )
  )
SELECT time_hier.member_name time, sales, lag_sales
FROM my_av HIERARCHIES (time_hier)
WHERE time_hier.level_name = 'YEAR'
ORDER BY time_hier.hier_order;
```

The results of the query are the following:

```
TIME         SALES   LAG_SALES
------  ----------  ----------
CY2011  6755115981      (null)
CY2012  6901682399  6755115981
CY2013  7240938718  6901682399
CY2014  7579746353  7240938718
CY2015  7941102885  7579746353
```

The following statement defines a transitory analytic view that uses a filter clause.

```
WITH
  my_av ANALYTIC VIEW AS (
    USING sales_av HIERARCHIES (time_hier)
    FILTER FACT (
      time_hier TO quarter_of_year IN (1, 2) 
        AND year_name IN ('CY2011', 'CY2012')
    )
  )
SELECT time_hier.member_name time, sales
  FROM my_av HIERARCHIES (time_hier)
  WHERE time_hier.level_name IN ('YEAR', 'QUARTER')
  ORDER BY time_hier.hier_order;
```

The results of the query are the following:

```
TIME           SALES
--------  ----------
CY2011    3340459835
Q1CY2011  1625299627
Q2CY2011  1715160208
CY2012    3397271965
Q1CY2012  1644857783
Q2CY2012  1752414182
```

Inline Analytic View Example

The following statement defines an inline analytic view in the `FROM` clause. The transitory analytic view is based on the persistent analytic view sales\_av. The lag\_sales calculated measure is a `LAG` calculation that is used at query time.

```
SELECT time_hier.member_name time, sales, lag_sales
FROM
  ANALYTIC VIEW (
    USING sales_av HIERARCHIES (time_hier)
    ADD MEASURES (
      lag_sales AS (LAG(sales) OVER (HIERARCHY time_hier OFFSET 1))
    )
  )
WHERE time_hier.level_name = 'YEAR'
ORDER BY time_hier.hier_order;
```

The results of the query are the following:

```
TIME         SALES   LAG_SALES
------  ----------  ----------
CY2011  6755115981      (null)
CY2012  6901682399  6755115981
CY2013  7240938718  6901682399
CY2014  7579746353  7240938718
CY2015  7941102885  7579746353
```

Simple Query Examples

The following statement selects rows from the `employees` table with the department number of 30:

```
SELECT * 
   FROM employees 
   WHERE department_id = 30
   ORDER BY last_name;
```

The following statement selects the name, job, salary and department number of all employees except purchasing clerks from department number 30:

```
SELECT last_name, job_id, salary, department_id 
   FROM employees 
   WHERE NOT (job_id = 'PU_CLERK' AND department_id = 30)
   ORDER BY last_name;
```

The following statement selects from subqueries in the `FROM` clause and for each department returns the total employees and salaries as a decimal value of all the departments:

```
SELECT a.department_id "Department",
   a.num_emp/b.total_count "%_Employees",
   a.sal_sum/b.total_sal "%_Salary"
FROM
(SELECT department_id, COUNT(*) num_emp, SUM(salary) sal_sum
   FROM employees
   GROUP BY department_id) a,
(SELECT COUNT(*) total_count, SUM(salary) total_sal
   FROM employees) b
ORDER BY a.department_id;
```

Selecting from a Partition: Example

You can select rows from a single partition of a partitioned table by specifying the keyword `PARTITION` in the `FROM` clause. This SQL statement assigns an alias for and retrieves rows from the `sales_q2_2000` partition of the sample table `sh.sales`:

```
SELECT * FROM sales PARTITION (sales_q2_2000) s
   WHERE s.amount_sold > 1500
   ORDER BY cust_id, time_id, channel_id;
```

The following example selects rows from the `oe.orders` table for orders earlier than a specified date:

```
SELECT * FROM orders
   WHERE order_date < TO_DATE('2006-06-15', 'YYYY-MM-DD');
```

Selecting a Sample: Examples

The following query estimates the number of orders in the `oe.orders` table:

```
SELECT COUNT(*) * 10 FROM orders SAMPLE (10);

COUNT(*)*10
-----------
         70
```

Because the query returns an estimate, the actual return value may differ from one query to the next.

```
SELECT COUNT(*) * 10 FROM orders SAMPLE (10);

COUNT(*)*10
-----------
         80
```

The following query adds a seed value to the preceding query. Oracle Database always returns the same estimate given the same seed value:

```
SELECT COUNT(*) * 10 FROM orders SAMPLE(10) SEED (1);

COUNT(*)*10
-----------
        130

SELECT COUNT(*) * 10 FROM orders SAMPLE(10) SEED(4);

COUNT(*)*10
-----------
        120

SELECT COUNT(*) * 10 FROM orders SAMPLE(10) SEED (1);

COUNT(*)*10
-----------
        130
```

Using Flashback Queries: Example

The following statements show a current value from the sample table `hr.employees` and then change the value. The intervals used in these examples are very short for demonstration purposes. Time intervals in your own environment are likely to be larger.

```
SELECT salary FROM employees
   WHERE last_name = 'Chung';
   
    SALARY
----------
      3800

UPDATE employees SET salary = 4000
   WHERE last_name = 'Chung';
1 row updated.

SELECT salary FROM employees
   WHERE last_name = 'Chung';

    SALARY
----------
      4000
```

To learn what the value was before the update, you can use the following Flashback Query:

```
SELECT salary FROM employees
   AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' MINUTE)
   WHERE last_name = 'Chung';
   
    SALARY
----------
      3800
```

To learn what the values were during a particular time period, you can use a version Flashback Query:

```
SELECT salary FROM employees
  VERSIONS BETWEEN TIMESTAMP
    SYSTIMESTAMP - INTERVAL '10' MINUTE AND
    SYSTIMESTAMP - INTERVAL '1' MINUTE
  WHERE last_name = 'Chung';
```

To revert to the earlier value, use the Flashback Query as the subquery of another `UPDATE` statement:

```
UPDATE employees SET salary =      
   (SELECT salary FROM employees
   AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' MINUTE)
   WHERE last_name = 'Chung')
   WHERE last_name = 'Chung';
1 row updated.

SELECT salary FROM employees
   WHERE last_name = 'Chung';
   
    SALARY
----------
      3800
```

Using the GROUP BY Clause: Examples

To return the minimum and maximum salaries for each department in the `employees` table, issue the following statement:

```
SELECT department_id, MIN(salary), MAX (salary)
     FROM employees
     GROUP BY department_id
   ORDER BY department_id;
```

To return the minimum and maximum salaries for the clerks in each department, issue the following statement:

```
SELECT department_id, MIN(salary), MAX (salary)
     FROM employees
     WHERE job_id = 'PU_CLERK'
     GROUP BY department_id
   ORDER BY department_id;
```

Using the GROUP BY CUBE Clause: Example

To return the number of employees and their average yearly salary across all possible combinations of department and job category, issue the following query on the sample tables `hr.employees` and `hr.departments`:

```
SELECT DECODE(GROUPING(department_name), 1, 'All Departments',
      department_name) AS department_name,
   DECODE(GROUPING(job_id), 1, 'All Jobs', job_id) AS job_id,
   COUNT(*) "Total Empl", AVG(salary) * 12 "Average Sal"
   FROM employees e, departments d
   WHERE d.department_id = e.department_id
   GROUP BY CUBE (department_name, job_id)
   ORDER BY department_name, job_id;

DEPARTMENT_NAME                JOB_ID     Total Empl Average Sal
------------------------------ ---------- ---------- -----------
Accounting                     AC_ACCOUNT          1       99600
Accounting                     AC_MGR              1      144000
Accounting                     All Jobs            2      121800
Administration                 AD_ASST             1       52800
. . .
Shipping                       ST_CLERK           20       33420
Shipping                       ST_MAN              5       87360
```

Using the GROUPING SETS Clause: Example

The following example finds the sum of sales aggregated for three precisely specified groups:

* `(channel_desc, calendar_month_desc, country_id)`
* `(channel_desc, country_id)`
* `(calendar_month_desc, country_id)`

Without the `GROUPING` `SETS` syntax, you would have to write less efficient queries with more complicated SQL. For example, you could run three separate queries and `UNION` them, or run a query with a `CUBE(channel_desc, calendar_month_desc, country_id)` operation and filter out five of the eight groups it would generate.

```
SELECT channel_desc, calendar_month_desc, co.country_id,
      TO_CHAR(sum(amount_sold) , '9,999,999,999') SALES$
   FROM sales, customers, times, channels, countries co
   WHERE sales.time_id=times.time_id 
      AND sales.cust_id=customers.cust_id 
      AND sales.channel_id= channels.channel_id 
      AND customers.country_id = co.country_id
      AND channels.channel_desc IN ('Direct Sales', 'Internet') 
      AND times.calendar_month_desc IN ('2000-09', '2000-10')
      AND co.country_iso_code IN ('UK', 'US')
  GROUP BY GROUPING SETS( 
      (channel_desc, calendar_month_desc, co.country_id), 
      (channel_desc, co.country_id), 
      (calendar_month_desc, co.country_id) );

CHANNEL_DESC         CALENDAR COUNTRY_ID     SALES$
-------------------- -------- ----------     ----------
Internet             2000-09       52790        124,224
Direct Sales         2000-09       52790        638,201
Internet             2000-10       52790        137,054
Direct Sales         2000-10       52790        682,297
                     2000-09       52790        762,425
                     2000-10       52790        819,351
Internet                           52790        261,278
Direct Sales                       52790      1,320,497
```

Hierarchical Query Examples

The following query with a `CONNECT` `BY` clause defines a hierarchical relationship in which the `employee_id` value of the parent row is equal to the `manager_id` value of the child row:

```
SELECT last_name, employee_id, manager_id FROM employees
   CONNECT BY employee_id = manager_id
   ORDER BY last_name;
```

In the following `CONNECT` `BY` clause, the `PRIOR` operator applies only to the `employee_id` value. To evaluate this condition, the database evaluates `employee_id` values for the parent row and `manager_id`, `salary`, and `commission_pct` values for the child row:

```
SELECT last_name, employee_id, manager_id FROM employees
   CONNECT BY PRIOR employee_id = manager_id
   AND salary > commission_pct
   ORDER BY last_name;
```

To qualify as a child row, a row must have a `manager_id` value equal to the `employee_id` value of the parent row and it must have a `salary` value greater than its `commission_pct` value.

Using the HAVING Condition: Example

To return the minimum and maximum salaries for the employees in each department whose lowest salary is less than $5,000, issue the next statement:

```
SELECT department_id, MIN(salary), MAX (salary)
   FROM employees
   GROUP BY department_id
   HAVING MIN(salary) < 5000
   ORDER BY department_id;

DEPARTMENT_ID MIN(SALARY) MAX(SALARY)
------------- ----------- -----------
           10        4400        4400
           30        2500       11000
           50        2100        8200
           60        4200        9000
```

The following example uses a correlated subquery in a `HAVING` clause that eliminates from the result set any departments without managers and managers without departments:

```
SELECT department_id, manager_id 
   FROM employees 
   GROUP BY department_id, manager_id HAVING (department_id, manager_id) IN
   (SELECT department_id, manager_id FROM employees x 
      WHERE x.department_id = employees.department_id)
   ORDER BY department_id;
```

Using the ORDER BY Clause: Examples

To select all purchasing clerk records from `employees` and order the results by salary in descending order, issue the following statement:

```
SELECT * 
   FROM employees
   WHERE job_id = 'PU_CLERK' 
   ORDER BY salary DESC;
```

To select information from `employees` ordered first by ascending department number and then by descending salary, issue the following statement:

```
SELECT last_name, department_id, salary
   FROM employees
   ORDER BY department_id ASC, salary DESC, last_name;
```

To select the same information as the previous `SELECT` and use the positional `ORDER` `BY` notation, issue the following statement, which orders by ascending `department_id`, then descending `salary`, and finally alphabetically by `last_name`:

```
SELECT last_name, department_id, salary 
   FROM employees 
   ORDER BY 2 ASC, 3 DESC, 1;
```

The MODEL clause: Examples

The view created below is based on the sample `sh` schema and is used by the example that follows.

```
CREATE OR REPLACE VIEW sales_view_ref AS
  SELECT country_name country,
         prod_name prod,
         calendar_year year,
         SUM(amount_sold) sale,
         COUNT(amount_sold) cnt
    FROM sales,times,customers,countries,products
    WHERE sales.time_id = times.time_id
      AND sales.prod_id = products.prod_id
      AND sales.cust_id = customers.cust_id
      AND customers.country_id = countries.country_id
      AND ( customers.country_id = 52779
            OR customers.country_id = 52776 )
      AND ( prod_name = 'Standard Mouse'
            OR prod_name = 'Mouse Pad' )
    GROUP BY country_name,prod_name,calendar_year;

SELECT country, prod, year, sale
  FROM sales_view_ref
  ORDER BY country, prod, year;

COUNTRY       PROD                                         YEAR        SALE
----------    -----------------------------------      --------   ---------
France        Mouse Pad                                    1998     2509.42
France        Mouse Pad                                    1999     3678.69
France        Mouse Pad                                    2000     3000.72
France        Mouse Pad                                    2001     3269.09
France        Standard Mouse                               1998     2390.83
France        Standard Mouse                               1999     2280.45
France        Standard Mouse                               2000     1274.31
France        Standard Mouse                               2001     2164.54
Germany       Mouse Pad                                    1998     5827.87
Germany       Mouse Pad                                    1999     8346.44
Germany       Mouse Pad                                    2000     7375.46
Germany       Mouse Pad                                    2001     9535.08
Germany       Standard Mouse                               1998     7116.11
Germany       Standard Mouse                               1999     6263.14
Germany       Standard Mouse                               2000     2637.31
Germany       Standard Mouse                               2001     6456.13
 
16 rows selected.
```

The next example creates a multidimensional array from `sales_view_ref` with columns containing country, product, year, and sales. It also:

* Assigns the sum of the sales of the Mouse Pad for years 1999 and 2000 to the sales of the Mouse Pad for year 2001, if a row containing sales of the Mouse Pad for year 2001 exists.
* Assigns the value of sales of the Standard Mouse for year 2001 to sales of the Standard Mouse for year 2002, creating a new row if a row containing sales of the Standard Mouse for year 2002 does not exist.

```
SELECT country,prod,year,s
  FROM sales_view_ref
  MODEL
    PARTITION BY (country)
    DIMENSION BY (prod, year)
    MEASURES (sale s)
    IGNORE NAV
    UNIQUE DIMENSION
    RULES UPSERT SEQUENTIAL ORDER
    (
      s[prod='Mouse Pad', year=2001] =
        s['Mouse Pad', 1999] + s['Mouse Pad', 2000],
      s['Standard Mouse', 2002] = s['Standard Mouse', 2001]
    )
  ORDER BY country, prod, year;
 
COUNTRY       PROD                                         YEAR        SALE
----------    -----------------------------------      --------   ---------
France        Mouse Pad                                    1998     2509.42
France        Mouse Pad                                    1999     3678.69
France        Mouse Pad                                    2000     3000.72
France        Mouse Pad                                    2001     6679.41
France        Standard Mouse                               1998     2390.83
France        Standard Mouse                               1999     2280.45
France        Standard Mouse                               2000     1274.31
France        Standard Mouse                               2001     2164.54
France        Standard Mouse                               2002     2164.54
Germany       Mouse Pad                                    1998     5827.87
Germany       Mouse Pad                                    1999     8346.44
Germany       Mouse Pad                                    2000     7375.46
Germany       Mouse Pad                                    2001     15721.9
Germany       Standard Mouse                               1998     7116.11
Germany       Standard Mouse                               1999     6263.14
Germany       Standard Mouse                               2000     2637.31
Germany       Standard Mouse                               2001     6456.13
Germany       Standard Mouse                               2002     6456.13

18 rows selected.
```

The first rule uses `UPDATE` behavior because symbolic referencing is used on the left-hand side of the rule. The rows represented by the left-hand side of the rule exist, so the measure columns are updated. If the rows did not exist, then no action would have been taken.

The second rule uses `UPSERT` behavior because positional referencing is used on the left-hand side and a single cell is referenced. The rows do not exist, so new rows are inserted and the related measure columns are updated. If the rows did exist, then the measure columns would have been updated.

The next example uses the same `sales_view_ref` view and the analytic function `SUM` to calculate a cumulative sum (`csum`) of sales per country and per year.

```
SELECT country, year, sale, csum
   FROM 
   (SELECT country, year, SUM(sale) sale
    FROM sales_view_ref
    GROUP BY country, year
   )
   MODEL DIMENSION BY (country, year)
         MEASURES (sale, 0 csum) 
         RULES (csum[any, any]= 
                  SUM(sale) OVER (PARTITION BY country 
                                  ORDER BY year 
                                  ROWS UNBOUNDED PRECEDING) 
                )
   ORDER BY country, year;

COUNTRY               YEAR       SALE       CSUM
--------------- ---------- ---------- ----------
France                1998    4900.25    4900.25
France                1999    5959.14   10859.39
France                2000    4275.03   15134.42
France                2001    5433.63   20568.05
Germany               1998   12943.98   12943.98
Germany               1999   14609.58   27553.56
Germany               2000   10012.77   37566.33
Germany               2001   15991.21   53557.54
 
8 rows selected.
```

Row Limiting: Examples

The following statement returns the 5 employees with the lowest `employee_id` values:

```
SELECT employee_id, last_name
  FROM employees
  ORDER BY employee_id
  FETCH FIRST 5 ROWS ONLY;

EMPLOYEE_ID LAST_NAME
----------- -------------------------
        100 King
        101 Kochhar
        102 De Haan
        103 Hunold
        104 Ernst
```

The following statement returns the next 5 employees with the lowest `employee_id` values:

```
SELECT employee_id, last_name
  FROM employees
  ORDER BY employee_id
  OFFSET 5 ROWS FETCH NEXT 5 ROWS ONLY;

EMPLOYEE_ID LAST_NAME
----------- -------------------------
        105 Austin
        106 Pataballa
        107 Lorentz
        108 Greenberg
        109 Faviet
```

The following statement returns the 5 percent of employees with the lowest salaries:

```
SELECT employee_id, last_name, salary
  FROM employees
  ORDER BY salary
  FETCH FIRST 5 PERCENT ROWS ONLY;

EMPLOYEE_ID LAST_NAME                     SALARY
----------- ------------------------- ----------
        132 Olson                           2100
        128 Markle                          2200
        136 Philtanker                      2200
        127 Landry                          2400
        135 Gee                             2400
        119 Colmenares                      2500
```

Because `WITH` `TIES` is specified, the following statement returns the 5 percent of employees with the lowest salaries, plus all additional employees with the same salary as the last row fetched in the previous example:

```
SELECT employee_id, last_name, salary
  FROM employees
  ORDER BY salary
  FETCH FIRST 5 PERCENT ROWS WITH TIES;

EMPLOYEE_ID LAST_NAME                     SALARY
----------- ------------------------- ----------
        132 Olson                           2100
        128 Markle                          2200
        136 Philtanker                      2200
        127 Landry                          2400
        135 Gee                             2400
        119 Colmenares                      2500
        131 Marlow                          2500
        140 Patel                           2500
        144 Vargas                          2500
        182 Sullivan                        2500
        191 Perkins                         2500
```

Using the FOR UPDATE Clause: Examples

The following statement locks rows in the `employees` table with purchasing clerks located in Oxford, which has `location_id` 2500, and locks rows in the `departments` table with departments in Oxford that have purchasing clerks:

```
SELECT e.employee_id, e.salary, e.commission_pct
   FROM employees e, departments d
   WHERE job_id = 'SA_REP'
   AND e.department_id = d.department_id
   AND location_id = 2500
   ORDER BY e.employee_id
   FOR UPDATE;
```

The following statement locks only those rows in the `employees` table with purchasing clerks located in Oxford. No rows are locked in the `departments` table:

```
SELECT e.employee_id, e.salary, e.commission_pct
   FROM employees e JOIN departments d
   USING (department_id)
   WHERE job_id = 'SA_REP'
   AND location_id = 2500
   ORDER BY e.employee_id
   FOR UPDATE OF e.salary;
```

Using the WITH CHECK OPTION Clause: Example

The following statement is legal even though the third value inserted violates the condition of the subquery `where_clause`:

```
INSERT INTO (SELECT department_id, department_name, location_id
   FROM departments WHERE location_id < 2000)
   VALUES (9999, 'Entertainment', 2500);
```

However, the following statement is illegal because it contains the `WITH` `CHECK` `OPTION` clause:

```
INSERT INTO (SELECT department_id, department_name, location_id
   FROM departments WHERE location_id < 2000 WITH CHECK OPTION)
   VALUES (9999, 'Entertainment', 2500);
     *
ERROR at line 2:
ORA-01402: view WITH CHECK OPTION where-clause violation
```

Using PIVOT and UNPIVOT: Examples

The `oe.orders` table contains information about when an order was placed (`order_date`), how it was place (`order_mode`), and the total amount of the order (`order_total`), as well as other information. The following example shows how to use the `PIVOT` clause to pivot `order_mode` values into columns, aggregating `order_total` data in the process, to get yearly totals by order mode:

```
CREATE TABLE pivot_table AS
SELECT * FROM
(SELECT EXTRACT(YEAR FROM order_date) year, order_mode, order_total FROM orders)
PIVOT
(SUM(order_total) FOR order_mode IN ('direct' AS Store, 'online' AS Internet));

SELECT * FROM pivot_table ORDER BY year;

      YEAR      STORE   INTERNET
---------- ---------- ----------
      2004     5546.6
      2006   371895.5   100056.6
      2007  1274078.8  1271019.5
      2008   252108.3   393349.4
```

The `UNPIVOT` clause lets you rotate specified columns so that the input column headings are output as values of one or more descriptor columns, and the input column values are output as values of one or more measures columns. The first query that follows shows that nulls are excluded by default. The second query shows that you can include nulls using the `INCLUDE` `NULLS` clause.

```
SELECT * FROM pivot_table
  UNPIVOT (yearly_total FOR order_mode IN (store AS 'direct',
           internet AS 'online'))
  ORDER BY year, order_mode;

      YEAR ORDER_ YEARLY_TOTAL
---------- ------ ------------
      2004 direct       5546.6
      2006 direct     371895.5
      2006 online     100056.6
      2007 direct    1274078.8
      2007 online    1271019.5
      2008 direct     252108.3
      2008 online     393349.4

7 rows selected.

SELECT * FROM pivot_table
  UNPIVOT INCLUDE NULLS 
    (yearly_total FOR order_mode IN (store AS 'direct', internet AS 'online'))
  ORDER BY year, order_mode;

      YEAR ORDER_ YEARLY_TOTAL
---------- ------ ------------
      2004 direct       5546.6
      2004 online
      2006 direct     371895.5
      2006 online     100056.6
      2007 direct    1274078.8
      2007 online    1271019.5
      2008 direct     252108.3
      2008 online     393349.4

8 rows selected.
```

Using Join Queries: Examples

The following examples show various ways of joining tables in a query. In the first example, an equijoin returns the name and job of each employee and the number and name of the department in which the employee works:

```
SELECT last_name, job_id, departments.department_id, department_name
   FROM employees, departments
   WHERE employees.department_id = departments.department_id
   ORDER BY last_name, job_id;

LAST_NAME           JOB_ID     DEPARTMENT_ID DEPARTMENT_NAME
------------------- ---------- ------------- ----------------------
Abel                 SA_REP               80 Sales
Ande                 SA_REP               80 Sales
Atkinson             ST_CLERK             50 Shipping
Austin               IT_PROG              60 IT
. . .
```

You must use a join to return this data because employee names and jobs are stored in a different table than department names. Oracle Database combines rows of the two tables according to this join condition:

```
employees.department_id = departments.department_id
```

The following equijoin returns the name, job, department number, and department name of all sales managers:

```
SELECT last_name, job_id, departments.department_id, department_name
   FROM employees, departments
   WHERE employees.department_id = departments.department_id
   AND job_id = 'SA_MAN'
   ORDER BY last_name;

LAST_NAME           JOB_ID     DEPARTMENT_ID DEPARTMENT_NAME
------------------- ---------- ------------- -----------------------
Cambrault           SA_MAN                80 Sales
Errazuriz           SA_MAN                80 Sales
Partners            SA_MAN                80 Sales
Russell             SA_MAN                80 Sales
Zlotkey             SA_MAN                80 Sales
```

This query is identical to the preceding example, except that it uses an additional `where_clause` condition to return only rows with a `job` value of '`SA_MAN`'.

Using Subqueries: Examples

To determine who works in the same department as employee '`Lorentz`', issue the following statement:

```
SELECT last_name, department_id FROM employees
   WHERE department_id =
     (SELECT department_id FROM employees
      WHERE last_name = 'Lorentz')
   ORDER BY last_name, department_id;
```

To give all employees in the `employees` table a 10% raise if they have changed jobsâif they appear in the `job_history` tableâissue the following statement:

```
UPDATE employees 
    SET salary = salary * 1.1
    WHERE employee_id IN (SELECT employee_id FROM job_history);
```

To create a second version of the `departments` table `new_departments`, with only three of the columns of the original table, issue the following statement:

```
CREATE TABLE new_departments 
   (department_id, department_name, location_id)
   AS SELECT department_id, department_name, location_id 
   FROM departments;
```

Using Self Joins: Example

The following query uses a self join to return the name of each employee along with the name of the employee's manager. A `WHERE` clause is added to shorten the output.

```
SELECT e1.last_name||' works for '||e2.last_name 
   "Employees and Their Managers"
   FROM employees e1, employees e2 
   WHERE e1.manager_id = e2.employee_id
      AND e1.last_name LIKE 'R%'
   ORDER BY e1.last_name;

Employees and Their Managers   
-------------------------------
Rajs works for Mourgos
Raphaely works for King
Rogers works for Kaufling
Russell works for King
```

The join condition for this query uses the aliases `e1` and `e2` for the sample table `employees`:

```
e1.manager_id = e2.employee_id
```

Using Outer Joins: Examples

The following example shows how a partitioned outer join fills data gaps in rows to facilitate analytic function specification and reliable report formatting. The example first creates a small data table to be used in the join:

```
SELECT d.department_id, e.last_name
   FROM departments d LEFT OUTER JOIN employees e
   ON d.department_id = e.department_id
   ORDER BY d.department_id, e.last_name;
```

Users familiar with the traditional Oracle Database outer joins syntax will recognize the same query in this form:

```
SELECT d.department_id, e.last_name
   FROM departments d, employees e
   WHERE d.department_id = e.department_id(+)
   ORDER BY d.department_id, e.last_name;
```

Oracle strongly recommends that you use the more flexible `FROM` clause join syntax shown in the former example.

The left outer join returns all departments, including those without any employees. The same statement with a right outer join returns all employees, including those not yet assigned to a department:

Note:

The employee Zeuss was added to the employees table for these examples, and is not part of the sample data.

```
SELECT d.department_id, e.last_name
   FROM departments d RIGHT OUTER JOIN employees e
   ON d.department_id = e.department_id
   ORDER BY d.department_id, e.last_name;

DEPARTMENT_ID LAST_NAME
------------- -------------------------
. . .
          110 Gietz
          110 Higgins
              Grant
              Zeuss
```

It is not clear from this result whether employees Grant and Zeuss have `department_id` `NULL`, or whether their `department_id` is not in the `departments` table. To determine this requires a full outer join:

```
SELECT d.department_id as d_dept_id, e.department_id as e_dept_id,
      e.last_name
   FROM departments d FULL OUTER JOIN employees e
   ON d.department_id = e.department_id
   ORDER BY d.department_id, e.last_name;

 D_DEPT_ID  E_DEPT_ID LAST_NAME
---------- ---------- -------------------------
  . . .
       110        110 Gietz
       110        110 Higgins
  . . .
       260
       270
                  999 Zeuss
                      Grant
```

Because the column names in this example are the same in both tables in the join, you can also use the common column feature by specifying the `USING` clause of the join syntax. The output is the same as for the preceding example except that the `USING` clause coalesces the two matching columns `department_id` into a single column output:

```
SELECT department_id AS d_e_dept_id, e.last_name
   FROM departments d FULL OUTER JOIN employees e
   USING (department_id)
   ORDER BY department_id, e.last_name;

D_E_DEPT_ID LAST_NAME
----------- -------------------------
  . . .
        110 Higgins
        110 Gietz
  . . .
        260
        270
        999 Zeuss
            Grant
```

Using Partitioned Outer Joins: Examples

The following example shows how a partitioned outer join fills in gaps in rows to facilitate analytic calculation specification and reliable report formatting. The example first creates and populates a simple table to be used in the join:

```
CREATE TABLE inventory (time_id    DATE,
                        product    VARCHAR2(10),
                        quantity   NUMBER);

INSERT INTO inventory VALUES (TO_DATE('01/04/01', 'DD/MM/YY'), 'bottle', 10);
INSERT INTO inventory VALUES (TO_DATE('06/04/01', 'DD/MM/YY'), 'bottle', 10);
INSERT INTO inventory VALUES (TO_DATE('01/04/01', 'DD/MM/YY'), 'can', 10);
INSERT INTO inventory VALUES (TO_DATE('04/04/01', 'DD/MM/YY'), 'can', 10);

SELECT times.time_id, product, quantity FROM inventory 
   PARTITION BY  (product) 
   RIGHT OUTER JOIN times ON (times.time_id = inventory.time_id) 
   WHERE times.time_id BETWEEN TO_DATE('01/04/01', 'DD/MM/YY') 
      AND TO_DATE('06/04/01', 'DD/MM/YY') 
   ORDER BY  2,1; 

TIME_ID   PRODUCT      QUANTITY
--------- ---------- ----------
01-APR-01 bottle             10
02-APR-01 bottle
03-APR-01 bottle
04-APR-01 bottle
05-APR-01 bottle
06-APR-01 bottle             10
01-APR-01 can                10
02-APR-01 can
03-APR-01 can
04-APR-01 can                10
05-APR-01 can
06-APR-01 can

12 rows selected.
```

The data is now more dense along the time dimension for each partition of the product dimension. However, each of the newly added rows within each partition is null in the quantity column. It is more useful to see the nulls replaced by the preceding non-`NULL` value in time order. You can achieve this by applying the analytic function `LAST_VALUE` on top of the query result:

```
SELECT time_id, product, LAST_VALUE(quantity IGNORE NULLS) 
   OVER (PARTITION BY product ORDER BY time_id) quantity 
   FROM ( SELECT times.time_id, product, quantity 
             FROM inventory PARTITION BY  (product) 
                RIGHT OUTER JOIN times ON (times.time_id = inventory.time_id) 
   WHERE times.time_id BETWEEN TO_DATE('01/04/01', 'DD/MM/YY') 
      AND TO_DATE('06/04/01', 'DD/MM/YY')) 
   ORDER BY  2,1; 

TIME_ID   PRODUCT      QUANTITY
--------- ---------- ----------
01-APR-01 bottle             10
02-APR-01 bottle             10
03-APR-01 bottle             10
04-APR-01 bottle             10
05-APR-01 bottle             10
06-APR-01 bottle             10
01-APR-01 can                10
02-APR-01 can                10
03-APR-01 can                10
04-APR-01 can                10
05-APR-01 can                10
06-APR-01 can                10

12 rows selected.
```

Using Antijoins: Example

The following example selects a list of employees who are not in a particular set of departments:

```
SELECT * FROM employees 
   WHERE department_id NOT IN 
   (SELECT department_id FROM departments 
       WHERE location_id = 1700)
   ORDER BY last_name;
```

Using Semijoins: Example

In the following example, only one row needs to be returned from the `departments` table, even though many rows in the `employees` table might match the subquery. If no index has been defined on the `salary` column in `employees`, then a semijoin can be used to improve query performance.

```
SELECT * FROM departments 
   WHERE EXISTS 
   (SELECT * FROM employees 
       WHERE departments.department_id = employees.department_id 
       AND employees.salary > 2500)
   ORDER BY department_name;
```

Using CROSS APPLY and OUTER APPLY Joins: Examples

The following statement uses the `CROSS` `APPLY` clause of the `cross_outer_apply_clause`. The join returns only rows from the table on the left side of the join (`departments`) that produce a result from the inline view on the right side of the join. That is, the join returns only the departments that have at least one employee. The `WHERE` clause restricts the result set to include only the Marketing, Operations, and Public Relations departments. However, the Operations department is not included in the result set because it has no employees.

```
SELECT d.department_name, v.employee_id, v.last_name
  FROM departments d CROSS APPLY (SELECT * FROM employees e
                                  WHERE e.department_id = d.department_id) v
  WHERE d.department_name IN ('Marketing', 'Operations', 'Public Relations')
  ORDER BY d.department_name, v.employee_id;

DEPARTMENT_NAME                EMPLOYEE_ID LAST_NAME
------------------------------ ----------- -------------------------
Marketing                      201         Hartstein
Marketing                      202         Fay
Public Relations               204         Baer
```

The following statement uses the `OUTER` `APPLY` clause of the `cross_outer_apply_clause`. The join returns all rows from the table on the left side of the join (`departments`) regardless of whether they produce a result from the inline view on the right side of the join. That is, the join returns all departments regardless of whether the departments have any employees. The `WHERE` clause restricts the result set to include only the Marketing, Operations, and Public Relations departments. The Operations department is included in the result set even though it has no employees.

```
SELECT d.department_name, v.employee_id, v.last_name
  FROM departments d OUTER APPLY (SELECT * FROM employees e
                                  WHERE e.department_id = d.department_id) v
  WHERE d.department_name IN ('Marketing', 'Operations', 'Public Relations')
  ORDER by d.department_name, v.employee_id;

DEPARTMENT_NAME                EMPLOYEE_ID LAST_NAME
------------------------------ ----------- -------------------------
Marketing                      201         Hartstein
Marketing                      202         Fay
Operations
Public Relations               204         Baer
```

Using Lateral Inline Views: Example

The following example shows a join with two operands. The second operand is an inline view that specifies the first operand, table `e`, in the `WHERE` clause. This results in an error.

```
SELECT * FROM employees e, (SELECT * FROM departments d
                            WHERE e.department_id = d.department_id);
ORA-00904: "E"."DEPARTMENT_ID": invalid identifier
```

The following example shows a join with two operands. The second operand is a lateral inline view that specifies the first operand, table `e`, in the `WHERE` clause and succeeds without an error.

```
SELECT * FROM employees e, LATERAL(SELECT * FROM departments d
                                   WHERE e.department_id = d.department_id);
```

Table Collections: Examples

You can perform DML operations on nested tables only if they are defined as columns of a table. Therefore, when the `query_table_expr_clause` of an `INSERT`, `DELETE`, or `UPDATE` statement is a `table_collection_expression`, the collection expression must be a subquery that uses the `TABLE` collection expression to select the nested table column of the table. The examples that follow are based on the following scenario:

Suppose the database contains a table `hr_info` with columns `department_id`, `location_id`, and `manager_id`, and a column of nested table type `people` which has `last_name`, `department_id`, and `salary` columns for all the employees of each respective manager:

```
CREATE TYPE people_typ AS OBJECT (
   last_name      VARCHAR2(25),
   department_id  NUMBER(4),
   salary         NUMBER(8,2));
/
CREATE TYPE people_tab_typ AS TABLE OF people_typ;
/
CREATE TABLE hr_info (
   department_id   NUMBER(4),
   location_id     NUMBER(4),
   manager_id      NUMBER(6),
   people          people_tab_typ)
   NESTED TABLE people STORE AS people_stor_tab;

INSERT INTO hr_info VALUES (280, 1800, 999, people_tab_typ());
```

The following example inserts into the `people` nested table column of the `hr_info` table for department 280:

```
INSERT INTO TABLE(SELECT h.people FROM hr_info h
   WHERE h.department_id = 280)
   VALUES ('Smith', 280, 1750);
```

The next example updates the department 280 `people` nested table:

```
UPDATE TABLE(SELECT h.people FROM hr_info h
   WHERE h.department_id = 280) p
   SET p.salary = p.salary + 100;
```

The next example deletes from the department 280 `people` nested table:

```
DELETE TABLE(SELECT h.people FROM hr_info h
   WHERE h.department_id = 280) p
   WHERE p.salary > 1700;
```

Collection Unnesting: Examples

To select data from a nested table column, use the `TABLE` collection expression to treat the nested table as columns of a table. This process is called collection unnesting.

You could get all the rows from `hr_info`, which was created in the preceding example, and all the rows from the `people` nested table column of `hr_info` using the following statement:

```
SELECT t1.department_id, t2.* FROM hr_info t1, TABLE(t1.people) t2
   WHERE t2.department_id = t1.department_id;
```

Now suppose that `people` is not a nested table column of `hr_info`, but is instead a separate table with columns `last_name`, `department_id`, `address`, `hiredate`, and `salary`. You can extract the same rows as in the preceding example with this statement:

```
SELECT t1.department_id, t2.* 
   FROM hr_info t1, TABLE(CAST(MULTISET(
      SELECT t3.last_name, t3.department_id, t3.salary 
         FROM people t3
      WHERE t3.department_id = t1.department_id)
      AS people_tab_typ)) t2;
```

Finally, suppose that `people` is neither a nested table column of table `hr_info` nor a table itself. Instead, you have created a function `people_func` that extracts from various sources the name, department, and salary of all employees. You can get the same information as in the preceding examples with the following query:

```
SELECT t1.department_id, t2.* FROM hr_info t1, TABLE(CAST
   (people_func( ... ) AS people_tab_typ)) t2;
```

Using the LEVEL Pseudocolumn: Examples

The following statement returns all employees in hierarchical order. The root row is defined to be the employee whose job is `AD_VP`. The child rows of a parent row are defined to be those who have the employee number of the parent row as their manager number.

```
SELECT LPAD(' ',2*(LEVEL-1)) || last_name org_chart, 
        employee_id, manager_id, job_id
    FROM employees
    START WITH job_id = 'AD_VP' 
    CONNECT BY PRIOR employee_id = manager_id; 

ORG_CHART          EMPLOYEE_ID MANAGER_ID JOB_ID
------------------ ----------- ---------- ----------
Kochhar                    101        100 AD_VP
  Greenberg                108        101 FI_MGR
    Faviet                 109        108 FI_ACCOUNT
    Chen                   110        108 FI_ACCOUNT
    Sciarra                111        108 FI_ACCOUNT
    Urman                  112        108 FI_ACCOUNT
    Popp                   113        108 FI_ACCOUNT
  Whalen                   200        101 AD_ASST
  Mavris                   203        101 HR_REP
  Baer                     204        101 PR_REP
  Higgins                  205        101 AC_MGR
    Gietz                  206        205 AC_ACCOUNT
De Haan                    102        100 AD_VP
  Hunold                   103        102 IT_PROG
    Ernst                  104        103 IT_PROG
    Austin                 105        103 IT_PROG
    Pataballa              106        103 IT_PROG
    Lorentz                107        103 IT_PROG
```

The following statement is similar to the previous one, except that it does not select employees with the job `FI_MGR`.

```
SELECT LPAD(' ',2*(LEVEL-1)) || last_name org_chart, 
        employee_id, manager_id, job_id
    FROM employees
    WHERE job_id != 'FI_MGR'
    START WITH job_id = 'AD_VP' 
    CONNECT BY PRIOR employee_id = manager_id; 

ORG_CHART          EMPLOYEE_ID MANAGER_ID JOB_ID
------------------ ----------- ---------- ----------
Kochhar                    101        100 AD_VP
    Faviet                 109        108 FI_ACCOUNT
    Chen                   110        108 FI_ACCOUNT
    Sciarra                111        108 FI_ACCOUNT
    Urman                  112        108 FI_ACCOUNT
    Popp                   113        108 FI_ACCOUNT
  Whalen                   200        101 AD_ASST
  Mavris                   203        101 HR_REP
  Baer                     204        101 PR_REP
  Higgins                  205        101 AC_MGR
    Gietz                  206        205 AC_ACCOUNT
De Haan                    102        100 AD_VP
  Hunold                   103        102 IT_PROG
    Ernst                  104        103 IT_PROG
    Austin                 105        103 IT_PROG
    Pataballa              106        103 IT_PROG
    Lorentz                107        103 IT_PROG
```

Oracle Database does not return the manager `Greenberg`, although it does return employees who are managed by `Greenberg`.

The following statement is similar to the first one, except that it uses the `LEVEL` pseudocolumn to select only the first two levels of the management hierarchy:

```
SELECT LPAD(' ',2*(LEVEL-1)) || last_name org_chart, 
employee_id, manager_id, job_id 
    FROM employees
    START WITH job_id = 'AD_PRES' 
    CONNECT BY PRIOR employee_id = manager_id AND LEVEL <= 2; 

ORG_CHART          EMPLOYEE_ID MANAGER_ID JOB_ID
------------------ ----------- ---------- ----------
King                       100            AD_PRES
  Kochhar                  101        100 AD_VP
  De Haan                  102        100 AD_VP
  Raphaely                 114        100 PU_MAN
  Weiss                    120        100 ST_MAN
  Fripp                    121        100 ST_MAN
  Kaufling                 122        100 ST_MAN
  Vollman                  123        100 ST_MAN
  Mourgos                  124        100 ST_MAN
  Russell                  145        100 SA_MAN
  Partners                 146        100 SA_MAN
  Errazuriz                147        100 SA_MAN
  Cambrault                148        100 SA_MAN
  Zlotkey                  149        100 SA_MAN
  Hartstein                201        100 MK_MAN
```

Using Distributed Queries: Example

This example shows a query that joins the `departments` table on the local database with the `employees` table on the `remote` database:

```
SELECT last_name, department_name 
   FROM employees@remote, departments
   WHERE employees.department_id = departments.department_id;
```

Using Correlated Subqueries: Examples

The following examples show the general syntax of a correlated subquery:

```
SELECT select_list 
    FROM table1 t_alias1 
    WHERE expr operator 
        (SELECT column_list 
            FROM table2 t_alias2 
            WHERE t_alias1.column 
               operator t_alias2.column); 

UPDATE table1 t_alias1 
    SET column = 
        (SELECT expr 
            FROM table2 t_alias2 
            WHERE t_alias1.column = t_alias2.column); 

DELETE FROM table1 t_alias1 
    WHERE column operator 
        (SELECT expr 
            FROM table2 t_alias2 
            WHERE t_alias1.column = t_alias2.column);
```

The following statement returns data about employees whose salaries exceed their department average. The following statement assigns an alias to `employees`, the table containing the salary information, and then uses the alias in a correlated subquery:

```
SELECT department_id, last_name, salary 
   FROM employees x 
   WHERE salary > (SELECT AVG(salary) 
      FROM employees 
      WHERE x.department_id = department_id) 
   ORDER BY department_id;
```

For each row of the `employees` table, the parent query uses the correlated subquery to compute the average salary for members of the same department. The correlated subquery performs the following steps for each row of the `employees` table:

1. The `department_id` of the row is determined.
2. The `department_id` is then used to evaluate the parent query.
3. If the salary in that row is greater than the average salary of the departments of that row, then the row is returned.

The subquery is evaluated once for each row of the `employees` table.

Selecting from the DUAL Table: Example

The following statement returns the current date:

```
SELECT SYSDATE FROM DUAL;
```

You could select `SYSDATE` from the `employees` table, but the database would return 14 rows of the same `SYSDATE`, one for every row of the `employees` table. Selecting from `DUAL` is more convenient.

Selecting Sequence Values: Examples

The following statement increments the `employees_seq` sequence and returns the new value:

```
SELECT employees_seq.nextval 
    FROM DUAL;
```

The following statement selects the current value of `employees_seq`:

```
SELECT employees_seq.currval 
    FROM DUAL;
```

Row Pattern Matching: Example

This example uses row pattern matching to query stock price data. The following statements create table `Ticker` and inserts stock price data into the table:

```
CREATE TABLE Ticker (SYMBOL VARCHAR2(10), tstamp DATE, price NUMBER);

INSERT INTO Ticker VALUES('ACME', '01-Apr-11', 12);
INSERT INTO Ticker VALUES('ACME', '02-Apr-11', 17);
INSERT INTO Ticker VALUES('ACME', '03-Apr-11', 19);
INSERT INTO Ticker VALUES('ACME', '04-Apr-11', 21);
INSERT INTO Ticker VALUES('ACME', '05-Apr-11', 25);
INSERT INTO Ticker VALUES('ACME', '06-Apr-11', 12);
INSERT INTO Ticker VALUES('ACME', '07-Apr-11', 15);
INSERT INTO Ticker VALUES('ACME', '08-Apr-11', 20);
INSERT INTO Ticker VALUES('ACME', '09-Apr-11', 24);
INSERT INTO Ticker VALUES('ACME', '10-Apr-11', 25);
INSERT INTO Ticker VALUES('ACME', '11-Apr-11', 19);
INSERT INTO Ticker VALUES('ACME', '12-Apr-11', 15);
INSERT INTO Ticker VALUES('ACME', '13-Apr-11', 25);
INSERT INTO Ticker VALUES('ACME', '14-Apr-11', 25);
INSERT INTO Ticker VALUES('ACME', '15-Apr-11', 14);
INSERT INTO Ticker VALUES('ACME', '16-Apr-11', 12);
INSERT INTO Ticker VALUES('ACME', '17-Apr-11', 14);
INSERT INTO Ticker VALUES('ACME', '18-Apr-11', 24);
INSERT INTO Ticker VALUES('ACME', '19-Apr-11', 23);
INSERT INTO Ticker VALUES('ACME', '20-Apr-11', 22);
```

The following query uses row pattern matching to find all cases where stock prices dipped to a bottom price and then rose. This is generally called a V-shape. The resulting output contains only three rows because the query specifies `ONE` `ROW` `PER` `MATCH`, and three matches were found.

```
SELECT *
FROM Ticker MATCH_RECOGNIZE (
     PARTITION BY symbol
     ORDER BY tstamp
     MEASURES STRT.tstamp AS start_tstamp,
              LAST(DOWN.tstamp) AS bottom_tstamp,
              LAST(UP.tstamp) AS end_tstamp
     ONE ROW PER MATCH
     AFTER MATCH SKIP TO LAST UP
     PATTERN (STRT DOWN+ UP+)
     DEFINE
        DOWN AS DOWN.price < PREV(DOWN.price),
        UP AS UP.price > PREV(UP.price)
     ) MR
ORDER BY MR.symbol, MR.start_tstamp;

SYMBOL     START_TST BOTTOM_TS END_TSTAM
---------- --------- --------- ---------
ACME       05-APR-11 06-APR-11 10-APR-11
ACME       10-APR-11 12-APR-11 13-APR-11
ACME       14-APR-11 16-APR-11 18-APR-11
```