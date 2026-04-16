# Oracle 12c - statements_6002
Source: https://docs.oracle.com/database/121/SQLRF/statements_6002.htm

Semantics

schema

Specify the schema to contain the materialized view. If you omit `schema`, then Oracle Database creates the materialized view in your schema.

materialized\_view

Specify the name of the materialized view to be created. The name must satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570). Oracle Database generates names for the table and indexes used to maintain the materialized view by adding a prefix or suffix to the materialized view name.

column\_alias

You can specify a column alias for each column of the materialized view. The column alias list explicitly resolves any column name conflict, eliminating the need to specify aliases in the `SELECT` clause of the materialized view. If you specify any column alias in this clause, then you must specify an alias for each data source referenced in the `SELECT` clause.

ENCRYPT clause  Use this clause to encrypt this column of the materialized view. Refer to the `CREATE` `TABLE` clause [encryption\_spec](statements_7002.md#CEGDFHBD) for more information on column encryption.

OF object\_type

The `OF` `object_type` clause lets you explicitly create an object materialized view of type `object_type`.

See Also:

See

`CREATE` `TABLE`

...

[object\_table](statements_7002.md#i2159410)

for more information on the

`OF` `type_name`

clause

scoped\_table\_ref\_constraint

Use the `SCOPE` `FOR` clause to restrict the scope of references to a single object table. You can refer either to the table name with `scope_table_name` or to a column alias. The values in the `REF` column or attribute point to objects in `scope_table_name` or `c_alias`, in which object instances of the same type as the `REF` column are stored. If you specify aliases, then they must have a one-to-one correspondence with the columns in the `SELECT` list of the defining query of the materialized view.

ON PREBUILT TABLE Clause

The `ON` `PREBUILT` `TABLE` clause lets you register an existing table as a preinitialized materialized view. This clause is particularly useful for registering large materialized views in a data warehousing environment. The table must have the same name and be in the same schema as the resulting materialized view.

If the materialized view is dropped, then the preexisting table reverts to its identity as a table.

Caution:

This clause assumes that the table object reflects the materialization of a subquery. Oracle strongly recommends that you ensure that this assumption is true in order to ensure that the materialized view correctly reflects the data in its master tables.

The `ON` `PREBUILT` `TABLE` clause could be useful in the following scenarios:

* You have a table representing the result of a query. Creating the table was an expensive operation that possibly took a long time. You want to create a materialized view on the query. You can use the `ON` `PREBUILT` `TABLE` clause to avoid the expense of executing the query and populating the container for the materialized view.
* You temporarily discontinue having a materialized view, but keep its container table, using the `DROP` `MATERIALIZED` `VIEW` ... `PRESERVE` `TABLE` statement. You then decide to recreate the materialized view and you know that the master tables of the view have not changed. You can create the materialized view using the `ON` `PREBUILT` `TABLE` clause. This avoids the expense and time of creating and populating the container table for the materialized view.

If you specify `ON` `PREBUILT` `TABLE`, then Oracle database does not create the `I_SNAP$` index. This index improves fast refresh performance. If you want the benefits of this index, then you can create it manually. Refer to [Oracle Database Data Warehousing Guide](../DWHSG/basicmv.md#DWHSG8216) for more information.

WITH REDUCED PRECISION Specify `WITH` `REDUCED` `PRECISION` to authorize the loss of precision that will result if the precision of the table or materialized view columns do not exactly match the precision returned by `subquery`.

WITHOUT REDUCED PRECISION Specify `WITHOUT` `REDUCED` `PRECISION` to require that the precision of the table or materialized view columns match exactly the precision returned by `subquery`, or the create operation will fail. This is the default.

Restrictions on Using Prebuilt Tables Prebuilt tables are subject to the following restrictions:

* Each column alias in `subquery` must correspond to a column in the prebuilt table, and corresponding columns must have matching data types.
* If you specify this clause, then you cannot specify a `NOT` `NULL` constraint for any column that is not referenced in `subquery` unless you also specify a default value for that column.
* You cannot specify the `ON` `PREBUILT` `TABLE` clause when creating a rowid materialized view.

physical\_properties\_clause

The components of the `physical_properties_clause` have the same semantics for materialized views that they have for tables, with exceptions and additions described in the sections that follow.

Restriction on the physical\_properties\_clause You cannot specify `ORGANIZATION` `EXTERNAL` for a materialized view.

deferred\_segment\_creation

Use this clause to determine when the segment for this materialized view should be created. See the `CREATE` `TABLE` clause [deferred\_segment\_creation](statements_7002.md#CEGJHDEB) for more information.

segment\_attributes\_clause

Use the `segment_attributes_clause` to establish values for the `PCTFREE`, `PCTUSED`, and `INITRANS` parameters, the storage characteristics for the materialized view, to assign a tablespace, and to specify whether logging is to occur. In the `USING` `INDEX` clause, you cannot specify `PCTFREE` or `PCTUSED`.

TABLESPACE Clause  Specify the tablespace in which the materialized view is to be created. If you omit this clause, then Oracle Database creates the materialized view in the default tablespace of the schema containing the materialized view.

logging\_clause Specify `LOGGING` or `NOLOGGING` to establish the logging characteristics for the materialized view. The logging characteristic affects the creation of the materialized view and any nonatomic refresh that is initiated by way of the `DBMS_REFRESH` package. The default is the logging characteristic of the tablespace in which the materialized view resides.

table\_compression

Use the `table_compression` clause to instruct the database whether to compress data segments to reduce disk and memory use. This clause has the same semantics in `CREATE` `MATERIALIZED` `VIEW` and `CREATE` `TABLE`. Refer to the [table\_compression](statements_7002.md#i2128733) clause in the documentation on `CREATE` `TABLE` for the full semantics of this clause.

inmemory\_table\_clause

Use the `inmemory_table_clause` to enable or disable the materialized view for the In-Memory Column Store (IM column store). This clause has the same semantics as the [inmemory\_table\_clause](statements_7002.md#CEGBCAAE) in the `CREATE` `TABLE` documentation.

inmemory\_column\_clause

Use the `inmemory_column_clause` to disable specific materialized view columns for the IM column store, and to specify the data compression method for specific columns. In order to specify this clause, the materialized view must be enabled for the IM column store. This clause has the same semantics as the [inmemory\_column\_clause](statements_7002.md#CEGJEEBB) in the `CREATE` `TABLE` documentation, with the following addition: If you specify the `inmemory_column_clause`, then you must also specify a `column_alias` for each column in the materialized view.

index\_org\_table\_clause

The `ORGANIZATION` `INDEX` clause lets you create an index-organized materialized view. In such a materialized view, data rows are stored in an index defined on the primary key of the materialized view. You can specify index organization for the following types of materialized views:

* Read-only and updatable object materialized views. You must ensure that the master table has a primary key.
* Read-only and updatable primary key materialized views.
* Read-only rowid materialized views.

The keywords and parameters of the `index_org_table_clause` have the same semantics as described in `CREATE` `TABLE`, with the restrictions that follow.

Restrictions on Index-Organized Materialized Views Index-organized materialized views are subject to the following restrictions:

* You cannot specify the following `CREATE` `MATERIALIZED` `VIEW` clauses: `CACHE` or `NOCACHE`, `CLUSTER`, or `ON` `PREBUILT` `TABLE`.
* In the `index_org_table_clause`:

  + You cannot specify the `mapping_table_clause`.
  + You can specify `COMPRESS` only for a materialized view based on a composite primary key. You can specify `NOCOMPRESS` for a materialized view based on either a simple or composite primary key.

CLUSTER Clause

The `CLUSTER` clause lets you create the materialized view as part of the specified cluster. A cluster materialized view uses the space allocation of the cluster. Therefore, you do not specify physical attributes or the `TABLESPACE` clause with the `CLUSTER` clause.

Restriction on Cluster Materialized Views If you specify `CLUSTER`, then you cannot specify the `table_partitioning_clauses` in `materialized_view_props`.

materialized\_view\_props

Use these property clauses to describe a materialized view that is not based on an existing table. To create a materialized view that is based on an existing table, use the `ON` `PREBUILT` `TABLE` clause.

column\_properties

The `column_properties` clause lets you specify the storage characteristics of a LOB, nested table, varray, or `XMLType` column. The `object_type_col_properties` are not relevant for a materialized view.

See Also:

[CREATE TABLE](statements_7002.md#i2095331)

for detailed information about specifying the parameters of this clause

table\_partitioning\_clauses

The `table_partitioning_clauses` let you specify that the materialized view is partitioned on specified ranges of values or on a hash function. Partitioning of materialized views is the same as partitioning of tables.

CACHE | NOCACHE

For data that will be accessed frequently, `CACHE` specifies that the blocks retrieved for this table are placed at the most recently used end of the least recently used (LRU) list in the buffer cache when a full table scan is performed. This attribute is useful for small lookup tables. `NOCACHE` specifies that the blocks are placed at the least recently used end of the LRU list.

Note:

`NOCACHE`

has no effect on materialized views for which you specify

`KEEP`

in the

`storage_clause`

.

See Also:

[CREATE TABLE](statements_7002.md#i2095331)

for information about specifying

`CACHE`

or

`NOCACHE`

parallel\_clause

The `parallel_clause` lets you indicate whether parallel operations will be supported for the materialized view and sets the default degree of parallelism for queries and DML on the materialized view after creation.

For complete information on this clause, refer to [parallel\_clause](statements_7002.md#i2159323) in the documentation on `CREATE` `TABLE`.

build\_clause

The `build_clause` lets you specify when to populate the materialized view.

IMMEDIATE Specify `IMMEDIATE` to indicate that the materialized view is to be populated immediately. This is the default.

DEFERRED Specify `DEFERRED` to indicate that the materialized view is to be populated by the next `REFRESH` operation. The first (deferred) refresh must always be a complete refresh. Until then, the materialized view has a staleness value of `UNUSABLE`, so it cannot be used for query rewrite.

USING INDEX Clause

The `USING` `INDEX` clause lets you establish the value of the `INITRANS` and `STORAGE` parameters for the default index Oracle Database uses to maintain the materialized view data. If `USING` `INDEX` is not specified, then default values are used for the index. Oracle Database uses the default index to speed up incremental (`FAST`) refresh of the materialized view.

Restriction on USING INDEX clause You cannot specify the `PCTUSED` parameter in this clause.

USING NO INDEX Clause

Specify `USING` `NO` `INDEX` to suppress the creation of the default index. You can create an alternative index explicitly by using the `CREATE` `INDEX` statement. You should create such an index if you specify `USING` `NO` `INDEX` and you are creating the materialized view with the fast refresh method (`REFRESH` `FAST`).

create\_mv\_refresh

Use the `create_mv_refresh` clause to specify the default methods, modes, and times for the database to refresh the materialized view. If the master tables of a materialized view are modified, then the data in the materialized view must be updated to make the materialized view accurately reflect the data currently in its master tables. This clause lets you schedule the times and specify the method and mode for the database to refresh the materialized view.

Restriction on Synchronous Refresh If you are using the synchronous refresh method, then you must specify `ON` `DEMAND` and `USING` `TRUSTED` `CONSTRAINTS`.

FAST Clause

Specify `FAST` to indicate the fast refresh method, which performs the refresh according to the changes that have occurred to the master tables. The changes for conventional DML changes are stored in the materialized view log associated with the master table. The changes for direct-path `INSERT` operations are stored in the direct loader log.

If you specify `REFRESH` `FAST`, then the `CREATE` statement will fail unless materialized view logs already exist for the materialized view master tables. Oracle Database creates the direct loader log automatically when a direct-path `INSERT` takes place. No user intervention is needed.

For both conventional DML changes and for direct-path `INSERT` operations, other conditions may restrict the eligibility of a materialized view for fast refresh.

Restrictions on FAST Refresh `FAST` refresh is subject to the following restrictions:

* When you specify `FAST` refresh at create time, Oracle Database verifies that the materialized view you are creating is eligible for fast refresh. When you change the refresh method to `FAST` in an `ALTER` `MATERIALIZED` `VIEW` statement, Oracle Database does not perform this verification. If the materialized view is not eligible for fast refresh, then Oracle Database returns an error when you attempt to refresh this view.
* Materialized views are not eligible for fast refresh if the defining query contains an analytic function or the `XMLTable` function.
* Materialized views are not eligible for fast refresh if the defining query references a table on which an `XMLIndex` index is defined.
* You cannot fast refresh a materialized view if any of its columns is encrypted.

COMPLETE Clause

Specify `COMPLETE` to indicate the complete refresh method, which is implemented by executing the defining query of the materialized view. If you request a complete refresh, then Oracle Database performs a complete refresh even if a fast refresh is possible.

FORCE Clause

Specify `FORCE` to indicate that when a refresh occurs, Oracle Database will perform a fast refresh if one is possible or a complete refresh if fast refresh is not possible. If you do not specify a refresh method (`FAST`, `COMPLETE`, or `FORCE`), then `FORCE` is the default.

ON COMMIT Clause

Specify `ON` `COMMIT` to indicate that a refresh is to occur whenever the database commits a transaction that operates on a master table of the materialized view. This clause may increase the time taken to complete the commit, because the database performs the refresh operation as part of the commit process.

You cannot specify both `ON` `COMMIT` and `ON` `DEMAND`. If you specify `ON` `COMMIT`, then you cannot also specify `START` `WITH` or `NEXT`.

Restrictions on Refreshing ON COMMIT

* This clause is not supported for materialized views containing object types or Oracle-supplied types.
* This clause is not supported for materialized views with remote tables.
* If you specify this clause, then you cannot subsequently execute a distributed transaction on any master table of this materialized view. For example, you cannot insert into the master by selecting from a remote table. The `ON` `DEMAND` clause does not impose this restriction on subsequent distributed transactions on master tables.

ON DEMAND Clause

Specify `ON` `DEMAND` to indicate that database will not refresh the materialized view unless the user manually launches a refresh through one of the three `DBMS_MVIEW` refresh procedures.

You cannot specify both `ON` `COMMIT` and `ON` `DEMAND`. If you omit both `ON` `COMMIT` and `ON` `DEMAND`, then `ON` `DEMAND` is the default. You can override this default setting by specifying the `START` `WITH` or `NEXT` clauses, either in the same `CREATE` `MATERIALIZED` `VIEW` statement or a subsequent `ALTER` `MATERIALIZED` `VIEW` statement.

`START` `WITH` and `NEXT` take precedence over `ON` `DEMAND`. Therefore, in most circumstances it is not meaningful to specify `ON` `DEMAND` when you have specified `START` `WITH` or `NEXT`.

START WITH Clause

Specify a datetime expression for the first automatic refresh time.

NEXT Clause

Specify a datetime expression for calculating the interval between automatic refreshes.

Both the `START` `WITH` and `NEXT` values must evaluate to a time in the future. If you omit the `START` `WITH` value, then the database determines the first automatic refresh time by evaluating the `NEXT` expression with respect to the creation time of the materialized view. If you specify a `START` `WITH` value but omit the `NEXT` value, then the database refreshes the materialized view only once. If you omit both the `START` `WITH` and `NEXT` values, or if you omit the `create_mv_refresh` entirely, then the database does not automatically refresh the materialized view.

WITH PRIMARY KEY Clause

Specify `WITH PRIMARY` `KEY` to create a primary key materialized view. This is the default and should be used in all cases except those described for `WITH` `ROWID`. Primary key materialized views allow materialized view master tables to be reorganized without affecting the eligibility of the materialized view for fast refresh. The master table must contain an enabled primary key constraint, and the defining query of the materialized view must specify all of the primary key columns directly. In the defining query, the primary key columns cannot be specified as the argument to a function such as `UPPER`.

Restriction on Primary Key Materialized Views You cannot specify this clause for an object materialized view. Oracle Database implicitly refreshes objects materialized `WITH` `OBJECT` `ID`.

WITH ROWID Clause

Specify `WITH` `ROWID` to create a rowid materialized view. Rowid materialized views are useful if the materialized view does not include all primary key columns of the master tables. Rowid materialized views must be based on a single table and cannot contain any of the following:

The `WITH` `ROWID` clause has no effect if there are multiple master tables in the defining query.

Rowid materialized views are not eligible for fast refresh after a master table reorganization until a complete refresh has been performed.

Restriction on Rowid Materialized Views You cannot specify this clause for an object materialized view. Oracle Database implicitly refreshes objects materialized `WITH` `OBJECT` `ID`.

USING ROLLBACK SEGMENT Clause

This clause is not valid if your database is in automatic undo mode, because in that mode Oracle Database uses undo tablespaces instead of rollback segments. Oracle strongly recommends that you use automatic undo mode. This clause is supported for backward compatibility with replication environments containing older versions of Oracle Database that still use rollback segments.

For `rollback_segment`, specify the remote rollback segment to be used during materialized view refresh.

DEFAULT `DEFAULT` specifies that Oracle Database will choose automatically which rollback segment to use. If you specify `DEFAULT`, then you cannot specify `rollback_segment`. `DEFAULT` is most useful when modifying, rather than creating, a materialized view.

MASTER `MASTER` specifies the remote rollback segment to be used at the remote master site for the individual materialized view.

LOCAL `LOCAL` specifies the remote rollback segment to be used for the local refresh group that contains the materialized view. This is the default.

If you omit `rollback_segment`, then the database automatically chooses the rollback segment to be used. One master rollback segment is stored for each materialized view and is validated during materialized view creation and refresh. If the materialized view is complex, then the database ignores any master rollback segment you specify.

USING ... CONSTRAINTS Clause

The `USING` ... `CONSTRAINTS` clause lets Oracle Database choose more rewrite options during the refresh operation, resulting in more efficient refresh execution. The clause lets Oracle Database use unenforced constraints, such as dimension relationships or constraints in the `RELY` state, rather than relying only on enforced constraints during the refresh operation.

The `USING` `TRUSTED` `CONSTRAINTS` clause enables you to create a materialized view on top of a table that has a non-NULL Virtual Private Database (VPD) policy on it. In this case, you must ensure that the materialized view behaves correctly. Materialized view results are computed based on the rows and columns filtered by VPD policy. Therefore, you must coordinate the materialized view definition with the VPD policy to ensure the correct results. Without the `USING` `TRUSTED` `CONSTRAINTS` clause, any VPD policy on a master table will prevent a materialized view from being created.

Caution:

The

`USING` `TRUSTED` `CONSTRAINTS`

clause lets Oracle Database use dimension and constraint information that has been declared trustworthy by the database administrator but that has not been validated by the database. If the dimension and constraint information is valid, then performance may improve. However, if this information is invalid, then the refresh procedure may corrupt the materialized view even though it returns a success status.

If you omit this clause, then the default is `USING` `ENFORCED` `CONSTRAINTS.`

NEVER REFRESH Clause

Specify `NEVER` `REFRESH` to prevent the materialized view from being refreshed with any Oracle Database refresh mechanism or packaged procedure. Oracle Database will ignore any `REFRESH` statement on the materialized view issued from such a procedure. If you specify this clause, then you can perform DML operations on the materialized view. To reverse this clause, you must issue an `ALTER` `MATERIALIZED` `VIEW` ... `REFRESH` statement.

FOR UPDATE Clause

Specify `FOR` `UPDATE` to allow a subquery, primary key, object, or rowid materialized view to be updated. When used in conjunction with Advanced Replication, these updates will be propagated to the master.

evaluation\_edition\_clause

You must specify this clause if `subquery` references an editioned object. Use this clause to specify the edition that is searched during name resolution of the editioned object—the evaluation edition.

* Specify `CURRENT` `EDITION` to search the edition in which this DDL statement is executed.
* Specify `EDITION` `edition` to search `edition`.
* Specifying `NULL` `EDITION` is equivalent to omitting the `evaluation_edition_clause`.

If you omit the `evaluation_edition_clause`, then editioned objects are invisible during name resolution and an error will result. Dropping the evaluation edition invalidates the materialized view.

query\_rewrite\_clause

The `query_rewrite_clause` lets you specify whether the materialized view is eligible to be used for query rewrite.

ENABLE Clause Specify `ENABLE` to enable the materialized view for query rewrite. If you also specify the `unusable_editions_clause`, then the materialized view is not enabled for query rewrite in the unusable editions.

Restrictions on Enabling Query Rewrite Enabling of query rewrite is subject to the following restrictions:

* You can enable query rewrite only if all user-defined functions in the materialized view are `DETERMINISTIC`.
* You can enable query rewrite only if expressions in the statement are repeatable. For example, you cannot include `CURRENT_TIME` or `USER`, sequence values (such as the `CURRVAL` or `NEXTVAL` pseudocolumns), or the `SAMPLE` clause (which may sample different rows as the contents of the materialized view change).

Notes:

* Query rewrite is disabled by default, so you must specify this clause to make materialized views eligible for query rewrite.
* After you create the materialized view, you must collect statistics on it using the `DBMS_STATS` package. Oracle Database needs the statistics generated by this package to optimize query rewrite.

DISABLE Clause Specify `DISABLE` to indicate that the materialized view is not eligible for use by query rewrite. A disabled materialized view can be refreshed.

unusable\_editions\_clause This clause lets you specify that the materialized view is not eligible for query rewrite in one or more editions. You can specify this clause regardless of whether you specify the `ENABLE` or `DISABLE` clause. If you specify the `DISABLE` clause, then this clause will take effect if the materialized view is subsequently enabled for query rewrite using the `ALTER` `MATERIALIZED` `VIEW` ... `ENABLE` `QUERY` `REWRITE` statement.

UNUSABLE BEFORE Clause This clause lets you specify that the materialized view is not eligible for query rewrite in the ancestors of an edition.

* If you specify `CURRENT` `EDITION`, then the materialized view is not eligible for query rewrite in the ancestors of the current edition.
* If you specify `EDITION` `edition`, then the materialized view is not eligible for query rewrite in the ancestors of the specified `edition`.

UNUSABLE BEGINNING WITH Clause This clause lets you specify that the materialized view is not eligible for query rewrite in an edition and its descendants.

* If you specify `CURRENT` `EDITION`, then the materialized view is not eligible for query rewrite in the current edition and its descendants.
* If you specify `EDITION` `edition`, then the materialized view is not eligible for query rewrite in the specified edition and its descendants.
* Specifying `NULL` `EDITION` is equivalent to omitting the `UNUSABLE` `BEGINNING` `WITH` clause.

The materialized view has a dependency on each edition in which it is not eligible for query rewrite. If such an edition is subsequently dropped, then the dependency is removed. However, the materialized view is not invalidated.

AS subquery

Specify the defining query of the materialized view. When you create the materialized view, Oracle Database executes this subquery and places the results in the materialized view. This subquery is any valid SQL subquery. However, not all subqueries are fast refreshable, nor are all subqueries eligible for query rewrite.

Notes on the Defining Query of a Materialized View The following notes apply to materialized views:

* Oracle Database does not execute the defining query immediately if you specify `BUILD` `DEFERRED`.
* Oracle recommends that you qualify each table and view in the `FROM` clause of the defining query of the materialized view with the schema containing it.
* In order to create a materialized view whose defining query selects from a master table that has a Virtual Private Database (VPD) policy, you must specify the `REFRESH` `USING` `TRUSTED` `CONSTRAINTS` clause.

Restrictions on the Defining Query of a Materialized View The materialized view query is subject to the following restrictions:

* The defining query of a materialized view can select from tables, views, or materialized views owned by the user `SYS`, but you cannot enable `QUERY` `REWRITE` on such a materialized view.
* The defining query of a materialized view cannot select from a `V$` view or a `GV$` view.
* You cannot define a materialized view with a subquery in the select list of the defining query. You can, however, include subqueries elsewhere in the defining query, such as in the `WHERE` clause.
* You cannot use the `AS` `OF` clause of the `flashback_query_clause` in the defining query of a materialized view.
* Materialized join views and materialized aggregate views with a `GROUP` `BY` clause cannot select from an index-organized table.
* Materialized views cannot contain columns of data type `LONG` or `LONG` `RAW`.
* Materialized views cannot contain virtual columns.
* You cannot create a materialized view log on a temporary table. Therefore, if the defining query references a temporary table, then this materialized view will not be eligible for `FAST` refresh, nor can you specify the `QUERY` `REWRITE` clause in this statement.
* If the `FROM` clause of the defining query references another materialized view, then you must always refresh the materialized view referenced in the defining query before refreshing the materialized view you are creating in this statement.
* Materialized views with join expressions in the defining query cannot have XML data type columns. The XML data types include `XMLType` and URI data type columns.

If you are creating a materialized view enabled for query rewrite, then:

* The defining query cannot contain, either directly or through a view, references to `ROWNUM`, `USER`, `SYSDATE`, remote tables, sequences, or PL/SQL functions that write or read database or package state.
* Neither the materialized view nor the master tables of the materialized view can be remote.

If you want the materialized view to be eligible for fast refresh using a materialized view log, or synchronous refresh using a staging log, then some additional restrictions apply.

Examples

The following examples require the materialized logs that are created in the "Examples" section of [CREATE MATERIALIZED VIEW LOG](statements_6003.md#i2064649).

Creating a Simple Materialized View: Example The following statement creates a very simple materialized view based on the `employees` and table in the `hr` schema:

```
CREATE MATERIALIZED VIEW mv1 AS SELECT * FROM hr.employees;
```

By default, Oracle Database creates a primary key materialized view with refresh on demand only. If a materialized view log exists on `employees`, then `mv1` can be altered to be capable of fast refresh. If no such log exists, then only full refresh of `mv1` is possible. Oracle Database uses default storage properties for `mv1`. The only privileges required for this operation are the `CREATE` `MATERIALIZED` `VIEW` system privilege, and the `READ` or `SELECT` object privilege on `hr`.`employees`.

Creating Subquery Materialized Views: Example The following statement creates a subquery materialized view based on the `customers` and `countries` tables in the `sh` schema at the `remote` database:

```
CREATE MATERIALIZED VIEW foreign_customers FOR UPDATE
   AS SELECT * FROM sh.customers@remote cu
   WHERE EXISTS
     (SELECT * FROM sh.countries@remote co
      WHERE co.country_id = cu.country_id);
```

Creating Materialized Aggregate Views: Example The following statement creates and populates a materialized aggregate view on the sample `sh.sales` table and specifies the default refresh method, mode, and time. It uses the materialized view log created in ["Creating a Materialized View Log for Fast Refresh: Examples"](statements_6003.md#i2098404), as well as the two additional logs shown here:

```
CREATE MATERIALIZED VIEW LOG ON times
   WITH ROWID, SEQUENCE (time_id, calendar_year)
   INCLUDING NEW VALUES;

CREATE MATERIALIZED VIEW LOG ON products
   WITH ROWID, SEQUENCE (prod_id)
   INCLUDING NEW VALUES;

CREATE MATERIALIZED VIEW sales_mv
   BUILD IMMEDIATE
   REFRESH FAST ON COMMIT
   AS SELECT t.calendar_year, p.prod_id, 
      SUM(s.amount_sold) AS sum_sales
      FROM times t, products p, sales s
      WHERE t.time_id = s.time_id AND p.prod_id = s.prod_id
      GROUP BY t.calendar_year, p.prod_id;
```

Creating Materialized Join Views: Example The following statement creates and populates the materialized aggregate view `sales_by_month_by_state` using tables in the sample `sh` schema. The materialized view will be populated with data as soon as the statement executes successfully. By default, subsequent refreshes will be accomplished by reexecuting the defining query of the materialized view:

```
CREATE MATERIALIZED VIEW sales_by_month_by_state
     TABLESPACE example
     PARALLEL 4
     BUILD IMMEDIATE
     REFRESH COMPLETE
     ENABLE QUERY REWRITE
     AS SELECT t.calendar_month_desc, c.cust_state_province,
        SUM(s.amount_sold) AS sum_sales
        FROM times t, sales s, customers c
        WHERE s.time_id = t.time_id AND s.cust_id = c.cust_id
        GROUP BY t.calendar_month_desc, c.cust_state_province;
```

Creating Prebuilt Materialized Views: Example The following statement creates a materialized aggregate view for the preexisting summary table, `sales_sum_table`:

```
CREATE TABLE sales_sum_table
   (month VARCHAR2(8), state VARCHAR2(40), sales NUMBER(10,2));

CREATE MATERIALIZED VIEW sales_sum_table
   ON PREBUILT TABLE WITH REDUCED PRECISION
   ENABLE QUERY REWRITE
   AS SELECT t.calendar_month_desc AS month, 
             c.cust_state_province AS state,
             SUM(s.amount_sold) AS sales
      FROM times t, customers c, sales s
      WHERE s.time_id = t.time_id AND s.cust_id = c.cust_id
      GROUP BY t.calendar_month_desc, c.cust_state_province;
```

In the preceding example, the materialized view has the same name and also has the same number of columns with the same data types as the prebuilt table. The `WITH` `REDUCED` `PRECISION` clause allows for differences between the precision of the materialized view columns and the precision of the values returned by the subquery.

Creating Primary Key Materialized Views: Example The following statement creates the primary key materialized view `catalog` on the sample table `oe.product_information`:

```
CREATE MATERIALIZED VIEW catalog   
   REFRESH FAST START WITH SYSDATE NEXT SYSDATE + 1/4096 
   WITH PRIMARY KEY 
   AS SELECT * FROM product_information;
```

Creating Rowid Materialized Views: Example The following statement creates a rowid materialized view on the sample table `oe.orders`:

```
CREATE MATERIALIZED VIEW order_data REFRESH WITH ROWID 
   AS SELECT * FROM orders;
```

Periodic Refresh of Materialized Views: Example The following statement creates the primary key materialized view `emp_data` and populates it with data from the sample table `hr.employees`:

```
CREATE MATERIALIZED VIEW LOG ON employees
   WITH PRIMARY KEY
   INCLUDING NEW VALUES;

CREATE MATERIALIZED VIEW emp_data 
   PCTFREE 5 PCTUSED 60 
   TABLESPACE example 
   STORAGE (INITIAL 50K)
   REFRESH FAST NEXT sysdate + 7 
   AS SELECT * FROM employees;
```

The preceding statement does not include a `START` `WITH` parameter, so Oracle Database determines the first automatic refresh time by evaluating the `NEXT` value using the current `SYSDATE`. A materialized view log was created for the employee table, so Oracle Database performs a fast refresh of the materialized view every 7 days, beginning 7 days after the materialized view is created.

Because the materialized view conforms to the conditions for fast refresh, the database will perform a fast refresh. The preceding statement also establishes storage characteristics that the database uses to maintain the materialized view.

Automatic Refresh Times for Materialized Views: Example The following statement creates the complex materialized view `all_customers` that queries the employee tables on the `remote` and `local` databases:

```
CREATE MATERIALIZED VIEW all_customers
   PCTFREE 5 PCTUSED 60 
   TABLESPACE example 
   STORAGE (INITIAL 50K) 
   USING INDEX STORAGE (INITIAL 25K)
   REFRESH START WITH ROUND(SYSDATE + 1) + 11/24 
   NEXT NEXT_DAY(TRUNC(SYSDATE), 'MONDAY') + 15/24 
   AS SELECT * FROM sh.customers@remote 
         UNION
      SELECT * FROM sh.customers@local;
```

Oracle Database automatically refreshes this materialized view tomorrow at 11:00 a.m. and subsequently every Monday at 3:00 p.m. The default refresh method is `FORCE`. The defining query contains a `UNION` operator, which is not supported for fast refresh, so the database will automatically perform a complete refresh.

The preceding statement also establishes storage characteristics for both the materialized view and the index that the database uses to maintain it:

* The first `STORAGE` clause establishes the sizes of the first and second extents of the materialized view as 50 kilobytes each.
* The second `STORAGE` clause, appearing with the `USING` `INDEX` clause, establishes the sizes of the first and second extents of the index as 25 kilobytes each.

Creating a Fast Refreshable Materialized View: Example The following statement creates a fast-refreshable materialized view that selects columns from the `order_items` table in the sample `oe` schema, using the `UNION` set operator to restrict the rows returned from the `product_information` and `inventories` tables using `WHERE` conditions. The materialized view logs for `order_items` and `product_information` were created in the ["Examples"](statements_6003.md#i2064930) section of `CREATE` `MATERIALIZED` `VIEW` `LOG`. This example also requires a materialized view log on `oe.inventories`.

```
CREATE MATERIALIZED VIEW LOG ON inventories
   WITH (quantity_on_hand);

CREATE MATERIALIZED VIEW warranty_orders REFRESH FAST AS
  SELECT order_id, line_item_id, product_id FROM order_items o
    WHERE EXISTS
    (SELECT * FROM inventories i WHERE o.product_id = i.product_id
      AND i.quantity_on_hand IS NOT NULL)
  UNION
    SELECT order_id, line_item_id, product_id FROM order_items
    WHERE quantity > 5;
```

The materialized view `warranty_orders` requires that materialized view logs be defined on `order_items` (with `product_id` as a join column) and on inventories (with `quantity_on_hand` as a filter column). See ["Specifying Filter Columns for Materialized View Logs: Example"](statements_6003.md#i2098358) and ["Specifying Join Columns for Materialized View Logs: Example"](statements_6003.md#i2098379).

Creating a Nested Materialized View: Example The following example uses the materialized view from the preceding example as a master table to create a materialized view tailored for a particular sales representative in the sample `oe` schema:

```
CREATE MATERIALIZED VIEW my_warranty_orders
   AS SELECT w.order_id, w.line_item_id, o.order_date
   FROM warranty_orders w, orders o
   WHERE o.order_id = o.order_id
   AND o.sales_rep_id = 165;
```