# Oracle 11g - statements_8005
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8005.htm

Semantics

hint

Specify a comment that passes instructions to the optimizer on choosing an execution plan for the statement.

See Also:

["Hints"](sql_elements006.md#i35922)

for the syntax and description of hints

from\_clause

Use the `FROM` clause to specify the database objects from which you are deleting rows.

The `ONLY` syntax is relevant only for views. Use the `ONLY` clause if the view in the `FROM` clause belongs to a view hierarchy and you do not want to delete rows from any of its subviews.

DML\_table\_expression\_clause

Use this clause to specify the objects from which data is being deleted.

schema

Specify the schema containing the table or view. If you omit `schema`, then Oracle Database assumes the table or view is in your own schema.

table | view | materialized view | subquery

Specify the name of a table, view, materialized view, or the column or columns resulting from a subquery, from which the rows are to be deleted.

When you delete rows from an updatable view, Oracle Database deletes rows from the base table.

You cannot delete rows from a read-only materialized view. If you delete rows from a writable materialized view, then the database removes the rows from the underlying container table. However, the deletions are overwritten at the next refresh operation. If you delete rows from an updatable materialized view that is part of a materialized view group, then the database also removes the corresponding rows from the master table.

If `table` or the base table of `view` or the master table of `materialized_view` contains one or more domain index columns, then this statement executes the appropriate indextype delete routine.

Issuing a `DELETE` statement against a table fires any `DELETE` triggers defined on the table.

All table or index space released by the deleted rows is retained by the table and index.

partition\_extension\_clause

Specify the name or partition key value of the partition or subpartition targeted for deletes within the object.

You need not specify the partition name when deleting values from a partitioned object. However, in some cases, specifying the partition name is more efficient than a complicated `where_clause`.

dblink

Specify the complete or partial name of a database link to a remote database where the object is located. You can delete rows from a remote object only if you are using Oracle Database distributed functionality.

If you omit `dblink`, then the database assumes that the object is located on the local database.

subquery\_restriction\_clause

The `subquery_restriction_clause` lets you restrict the subquery in one of the following ways:

WITH READ ONLY Specify `WITH READ ONLY` to indicate that the table or view cannot be updated.

WITH CHECK OPTION Specify `WITH CHECK OPTION` to indicate that Oracle Database prohibits any changes to the table or view that would produce rows that are not included in the subquery. When used in the subquery of a DML statement, you can specify this clause in a subquery in the `FROM` clause but not in subquery in the `WHERE` clause.

CONSTRAINT constraint Specify the name of the `CHECK OPTION` constraint. If you omit this identifier, then Oracle automatically assigns the constraint a name of the form `SYS_C``n`, where n is an integer that makes the constraint name unique within the database.

table\_collection\_expression

The `table_collection_expression` lets you inform Oracle that the value of `collection_expression` should be treated as a table for purposes of query and DML operations. The `collection_expression` can be a subquery, a column, a function, or a collection constructor. Regardless of its form, it must return a collection value—that is, a value whose type is nested table or varray. This process of extracting the elements of a collection is called collection unnesting.

The optional plus (+) is relevant if you are joining the `TABLE` collection expression with the parent table. The + creates an outer join of the two, so that the query returns rows from the outer table even if the collection expression is null.

Note:

In earlier releases of Oracle, when

`collection_expression`

was a subquery,

`table_collection_expression`

was expressed as

`THE` `subquery`

. That usage is now deprecated.

You can use a `table_collection_expression` in a correlated subquery to delete rows with values that also exist in another table.

collection\_expression Specify a subquery that selects a nested table column from the object from which you are deleting.

Restrictions on the dml\_table\_expression\_clause Clause This clause is subject to the following restrictions:

* You cannot execute this statement if `table` or the base or master table of `view` or `materialized_view` contains any domain indexes marked `IN_PROGRESS` or `FAILED.`
* You cannot insert into a partition if any affected index partitions are marked `UNUSABLE`.
* You cannot specify the `ORDER` `BY` clause in the subquery of the `DML_table_expression_clause`.
* You cannot delete from a view except through `INSTEAD` `OF` triggers if the defining query of the view contains one of the following constructs:

  :   A set operator
  :   A `DISTINCT` operator
  :   An aggregate or analytic function
  :   A `GROUP` `BY`, `ORDER` `BY`, `MODEL`, `CONNECT` `BY`, or `START` `WITH` clause
  :   A collection expression in a `SELECT` list
  :   A subquery in a `SELECT` list
  :   A subquery designated `WITH READ ONLY`
  :   Joins, with some exceptions, as documented in [Oracle Database Administrator's Guide](../../server.112/e25494/views.md#ADMIN020)

If you specify an index, index partition, or index subpartition that has been marked `UNUSABLE`, then the `DELETE` statement will fail unless the `SKIP_UNUSABLE_INDEXES` initialization parameter has been set to `true`.

where\_clause

Use the `where_clause` to delete only rows that satisfy the condition. The condition can reference the object from which you are deleting and can contain a subquery. You can delete rows from a remote object only if you are using Oracle Database distributed functionality. Refer to [Chapter 7, "Conditions"](conditions.md#g1077361) for the syntax of `condition`.

If this clause contains a `subquery` that refers to remote objects, then the `DELETE` operation can run in parallel as long as the reference does not loop back to an object on the local database. However, if the `subquery` in the `DML_table_expression_clause` refers to any remote objects, then the `DELETE` operation will run serially without notification. Refer to the [parallel\_clause](statements_7002.md#i2159323) in the `CREATE` `TABLE` documentation for additional information.

If you omit `dblink`, then the database assumes that the table or view is located on the local database.

If you omit the `where_clause`, then the database deletes all rows of the object.

t\_alias  Provide a correlation name for the table, view, materialized view, subquery, or collection value to be referenced elsewhere in the statement. This alias is required if the `DML_table_expression_clause` references any object type attributes or object type methods. Table aliases are generally used in `DELETE` statements with correlated queries.

returning\_clause

This clause lets you return values from deleted columns, and thereby eliminate the need to issue a `SELECT` statement following the `DELETE` statement.

The returning clause retrieves the rows affected by a DML statement. You can specify this clause for tables and materialized views and for views with a single base table.

When operating on a single row, a DML statement with a `returning_clause` can retrieve column expressions using the affected row, rowid, and `REFs` to the affected row and store them in host variables or PL/SQL variables.

When operating on multiple rows, a DML statement with the `returning_clause` stores values from expressions, rowids, and `REFs` involving the affected rows in bind arrays.

expr Each item in the `expr` list must be a valid expression syntax.

INTO The `INTO` clause indicates that the values of the changed rows are to be stored in the variable(s) specified in `data_item` list.

data\_item Each `data_item` is a host variable or PL/SQL variable that stores the retrieved `expr` value.

For each expression in the `RETURNING` list, you must specify a corresponding type-compatible PL/SQL variable or host variable in the `INTO` list.

Restrictions The following restrictions apply to the `RETURNING` clause:

* The `expr` is restricted as follows:

  + For `UPDATE` and `DELETE` statements each `expr` must be a simple expression or a single-set aggregate function expression. You cannot combine simple expressions and single-set aggregate function expressions in the same `returning_clause`. For `INSERT` statements, each `expr` must be a simple expression. Aggregate functions are not supported in an `INSERT` statement `RETURNING` clause.
  + Single-set aggregate function expressions cannot include the `DISTINCT` keyword.
* If the `expr` list contains a primary key column or other `NOT` `NULL` column, then the update statement fails if the table has a `BEFORE` `UPDATE` trigger defined on it.
* You cannot specify the `returning_clause` for a multitable insert.
* You cannot use this clause with parallel DML or with remote objects.
* You cannot retrieve `LONG` types with this clause.
* You cannot specify this clause for a view on which an `INSTEAD` `OF` trigger has been defined.

error\_logging\_clause

The `error_logging_clause` has the same behavior in `DELETE` statement as it does in an `INSERT` statement. Refer to the `INSERT` statement [error\_logging\_clause](statements_9014.md#BGBEIACB) for more information.

Examples

Deleting Rows: Examples The following statement deletes all rows from the sample table `oe.product_descriptions` where the value of the `language_id` column is `AR`:

```
DELETE FROM product_descriptions
   WHERE language_id = 'AR';
```

The following statement deletes from the sample table `hr.employees` purchasing clerks whose commission rate is less than 10%:

```
DELETE FROM employees
   WHERE job_id = 'SA_REP'
   AND commission_pct < .2;
```

The following statement has the same effect as the preceding example, but uses a subquery:

```
DELETE FROM (SELECT * FROM employees)
   WHERE job_id = 'SA_REP'
   AND commission_pct < .2;
```

Deleting Rows from a Remote Database: Example The following statement deletes specified rows from the `locations` table owned by the user `hr` on a database accessible by the database link `remote`:

```
DELETE FROM hr.locations@remote
   WHERE location_id > 3000;
```

Deleting Nested Table Rows: Example For an example that deletes nested table rows, refer to ["Table Collections: Examples"](statements_10002.md#i2071643).

Deleting Rows from a Partition: Example The following example removes rows from partition `sales_q1_1998` of the `sh.sales` table:

```
DELETE FROM sales PARTITION (sales_q1_1998)
   WHERE amount_sold > 1000;
```

Using the RETURNING Clause: Example 

The following example returns column `salary` from the deleted rows and stores the result in bind variable `:bnd1`. The bind variable must already have been declared.

```
DELETE FROM employees
   WHERE job_id = 'SA_REP' 
   AND hire_date + TO_YMINTERVAL('01-00') < SYSDATE 
   RETURNING salary INTO :bnd1;
```