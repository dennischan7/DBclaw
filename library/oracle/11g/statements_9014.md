# Oracle 11g - statements_9014
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_9014.htm

Semantics

hint

Specify a comment that passes instructions to the optimizer on choosing an execution plan for the statement.

For a multitable insert, if you specify the `PARALLEL` hint for any target table, then the entire multitable insert statement is parallelized even if the target tables have not been created or altered with `PARALLEL` specified. If you do not specify the `PARALLEL` hint, then the insert operation will not be parallelized unless all target tables were created or altered with `PARALLEL` specified.

single\_table\_insert

In a single-table insert, you insert values into one row of a table, view, or materialized view by specifying values explicitly or by retrieving the values through a subquery.

You can use the `flashback_query_clause` in `subquery` to insert past data into `table`. Refer to the [flashback\_query\_clause](statements_10002.md#i2112818) of `SELECT` for more information on this clause.

Restriction on Single-table Inserts If you retrieve values through a subquery, then the select list of the subquery must have the same number of columns as the column list of the `INSERT` statement. If you omit the column list, then the subquery must provide values for every column in the table.

insert\_into\_clause

Use the `INSERT` `INTO` clause to specify the target object or objects into which the database is to insert data.

DML\_table\_expression\_clause

Use the `INTO` `DML_table_expression_clause` to specify the objects into which data is being inserted.

schema Specify the schema containing the table, view, or materialized view. If you omit `schema`, then the database assumes the object is in your own schema.

table | view | materialized\_view | subquery Specify the name of the table or object table, view or object view, materialized view, or the column or columns returned by a subquery, into which rows are to be inserted. If you specify a view or object view, then the database inserts rows into the base table of the view.

You cannot insert rows into a read-only materialized view. If you insert rows into a writable materialized view, then the database inserts the rows into the underlying container table. However, the insertions are overwritten at the next refresh operation. If you insert rows into an updatable materialized view that is part of a materialized view group, then the database also inserts the corresponding rows into the master table.

If any value to be inserted is a `REF` to an object table, and if the object table has a primary key object identifier, then the column into which you insert the `REF` must be a `REF` column with a referential integrity or `SCOPE` constraint to the object table.

If `table`, or the base table of `view`, contains one or more domain index columns, then this statement executes the appropriate indextype insert routine.

Issuing an `INSERT` statement against a table fires any `INSERT` triggers defined on the table.

Restrictions on the DML\_table\_expression\_clause This clause is subject to the following restrictions:

* You cannot execute this statement if `table` or the base table of `view` contains any domain indexes marked `IN_PROGRESS` or `FAILED`.
* You cannot insert into a partition if any affected index partitions are marked `UNUSABLE`.
* With regard to the `ORDER` `BY` clause of the `subquery` in the `DML_table_expression_clause`, ordering is guaranteed only for the rows being inserted, and only within each extent of the table. Ordering of new rows with respect to existing rows is not guaranteed.
* If a view was created using the `WITH` `CHECK` `OPTION`, then you can insert into the view only rows that satisfy the defining query of the view.
* If a view was created using a single base table, then you can insert rows into the view and then retrieve those values using the `returning_clause`.
* You cannot insert rows into a view except with `INSTEAD` `OF` triggers if the defining query of the view contains one of the following constructs:

  :   A set operator
  :   A `DISTINCT` operator
  :   An aggregate or analytic function
  :   A `GROUP` `BY`, `ORDER` `BY`, `MODEL`, `CONNECT` `BY`, or `START` `WITH` clause
  :   A collection expression in a `SELECT` list
  :   A subquery in a `SELECT` list
  :   A subquery designated `WITH READ ONLY`
  :   Joins, with some exceptions, as documented in [Oracle Database Administrator's Guide](../../server.112/e25494/views.md#ADMIN020)
* If you specify an index, index partition, or index subpartition that has been marked `UNUSABLE`, then the `INSERT` statement will fail unless the `SKIP_UNUSABLE_INDEXES` session parameter has been set to `TRUE`. Refer to [ALTER SESSION](statements_2013.md#i2231814) for information on the `SKIP_UNUSABLE_INDEXES` session parameter.

partition\_extension\_clause  Specify the name or partition key value of the partition or subpartition within `table`, or the base table of `view`, targeted for inserts.

If a row to be inserted does not map into a specified partition or subpartition, then the database returns an error.

Restriction on Target Partitions and Subpartitions This clause is not valid for object tables or object views.

dblink  Specify a complete or partial name of a database link to a remote database where the table or view is located. You can insert rows into a remote table or view only if you are using Oracle Database distributed functionality.

If you omit `dblink`, then Oracle Database assumes that the table or view is on the local database.

subquery\_restriction\_clause Use the `subquery_restriction_clause` to restrict the subquery in one of the following ways:

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

t\_alias

Specify a correlation name, which is an alias for the table, view, materialized view, or subquery to be referenced elsewhere in the statement.

Restriction on Table Aliases You cannot specify `t_alias` during a multitable insert.

column

Specify a column of the table, view, or materialized view. In the inserted row, each column in this list is assigned a value from the `values_clause` or the subquery.

If you omit one or more of the table's columns from this list, then the column value of that column for the inserted row is the column default value as specified when the table was created or last altered. If any omitted column has a `NOT` `NULL` constraint and no default value, then the database returns an error indicating that the constraint has been violated and rolls back the `INSERT` statement. Refer to [CREATE TABLE](statements_7002.md#i2095331) for more information on default column values.

If you omit the column list altogether, then the `values_clause` or query must specify values for all columns in the table.

values\_clause

For a single-table insert operation, specify a row of values to be inserted into the table or view. You must specify a value in the `values_clause` for each column in the column list. If you omit the column list, then the `values_clause` must provide values for every column in the table.

For a multitable insert operation, each expression in the `values_clause` must refer to columns returned by the select list of the subquery. If you omit the `values_clause`, then the select list of the subquery determines the values to be inserted, so it must have the same number of columns as the column list of the corresponding `insert_into_clause`. If you do not specify a column list in the `insert_into_clause`, then the computed row must provide values for all columns in the target table.

For both types of insert operations, if you specify a column list in the `insert_into_clause`, then the database assigns to each column in the list a corresponding value from the values clause or the subquery. You can specify `DEFAULT` for any value in the `values_clause`. If you have specified a default value for the corresponding column of the table or view, then that value is inserted. If no default value for the corresponding column has been specified, then the database inserts null. Refer to ["About SQL Expressions"](expressions001.md#i1002626) and [SELECT](statements_10002.md#i2065646) for syntax of valid expressions.

Restrictions on Inserted Values The value are subject to the following restrictions:

* You cannot insert a `BFILE` value until you have initialized the `BFILE` locator to null or to a directory name and filename.
* When inserting into a list-partitioned table, you cannot insert a value into the partitioning key column that does not already exist in the `partition_key_value` list of one of the partitions.
* You cannot specify `DEFAULT` when inserting into a view.
* If you insert string literals into a `RAW` column, then during subsequent queries Oracle Database will perform a full table scan rather than using any index that might exist on the `RAW` column.

returning\_clause

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

multi\_table\_insert

In a multitable insert, you insert computed rows derived from the rows returned from the evaluation of a subquery into one or more tables.

Table aliases are not defined by the select list of the subquery. Therefore, they are not visible in the clauses dependent on the select list. For example, this can happen when trying to refer to an object column in an expression. To use an expression with a table alias, you must put the expression into the select list with a column alias, and then refer to the column alias in the `VALUES` clause or `WHEN` condition of the multitable insert.

ALL into\_clause

Specify `ALL` followed by multiple `insert_into_clauses` to perform an unconditional multitable insert. Oracle Database executes each `insert_into_clause` once for each row returned by the subquery.

conditional\_insert\_clause

Specify the `conditional_insert_clause` to perform a conditional multitable insert. Oracle Database filters each `insert_into_clause` through the corresponding `WHEN` condition, which determines whether that `insert_into_clause` is executed. Each expression in the `WHEN` condition must refer to columns returned by the select list of the subquery. A single multitable insert statement can contain up to 127 `WHEN` clauses.

ALL If you specify `ALL`, the default value, then the database evaluates each `WHEN` clause regardless of the results of the evaluation of any other `WHEN` clause. For each `WHEN` clause whose condition evaluates to true, the database executes the corresponding `INTO` clause list.

FIRST If you specify `FIRST`, then the database evaluates each `WHEN` clause in the order in which it appears in the statement. For the first `WHEN` clause that evaluates to true, the database executes the corresponding `INTO` clause and skips subsequent `WHEN` clauses for the given row.

ELSE clause For a given row, if no `WHEN` clause evaluates to true, then:

* If you have specified an `ELSE` clause, then the database executes the `INTO` clause list associated with the `ELSE` clause.
* If you did not specify an else clause, then the database takes no action for that row.

Restrictions on Multitable Inserts Multitable inserts are subject to the following restrictions:

* You can perform multitable inserts only on tables, not on views or materialized views.
* You cannot perform a multitable insert into a remote table.
* You cannot specify a `TABLE` collection expression when performing a multitable insert.
* Multitable inserts are not parallelized if any target table is index organized or if any target table has a bitmap index defined on it.
* Plan stability is not supported for multitable insert statements.
* You cannot specify a sequence in any part of a multitable insert statement. A multitable insert is considered a single SQL statement. Therefore, the first reference to `NEXTVAL` generates the next number, and all subsequent references in the statement return the same number.

subquery

Specify a subquery that returns rows that are inserted into the table. The subquery can refer to any table, view, or materialized view, including the target tables of the `INSERT` statement. If the subquery selects no rows, then the database inserts no rows into the table.

You can use `subquery` in combination with the `TO_LOB` function to convert the values in a `LONG` column to LOB values in another column in the same or another table.

* To migrate `LONG` values to LOB values in another column in a view, you must perform the migration on the base table and then add the LOB column to the view.
* To migrate `LONG` values on a remote table to LOB values in a local table, you must perform the migration on the remote table using the `TO_LOB` function, and then perform an `INSERT` ... `subquery` operation to copy the LOB values from the remote table into the local table.

Notes on Inserting with a Subquery The following notes apply when inserting with a subquery:

* If `subquery` returns the partial or total equivalent of a materialized view, then the database may use the materialized view for query rewrite in place of one or more tables specified in `subquery`.
* If `subquery` refers to remote objects, then the `INSERT` operation can run in parallel as long as the reference does not loop back to an object on the local database. However, if the `subquery` in the `DML_table_expression_clause` refers to any remote objects, then the `INSERT` operation will run serially without notification. See [parallel\_clause](statements_7002.md#i2159323) for more information.

error\_logging\_clause

The `error_logging_clause` lets you capture DML errors and the log column values of the affected rows and save them in an error logging table.

INTO table Specify the name of the error logging table. If you omit this clause, then the database assigns the default name generated by the `DBMS_ERRLOG` package. The default error log table name is `ERR$_` followed by the first 25 characters of the name of the table upon which the DML operation is being executed.

simple\_expression Specify the value to be used as a statement tag, so that you can identify the errors from this statement in the error logging table. The expression can be either a text literal, a number literal, or a general SQL expression such as a bind variable. You can also use a function expression if you convert it to a text literal — for example, `TO_CHAR(SYSDATE)`.

REJECT LIMIT This clause lets you specify an integer as an upper limit for the number of errors to be logged before the statement terminates and rolls back any changes made by the statement. The default rejection limit is zero. For parallel DML operations, the reject limit is applied to each parallel server.

Restrictions on DML Error Logging

* The following conditions cause the statement to fail and roll back without invoking the error logging capability:

  + Violated deferred constraints.
  + Any direct-path `INSERT` or `MERGE` operation that raises a unique constraint or index violation.
  + Any update operation `UPDATE` or `MERGE` that raises a unique constraint or index violation.
* You cannot track errors in the error logging table for `LONG`, LOB, or object type columns. However, the table that is the target of the DML operation can contain these types of columns.

  + If you create or modify the corresponding error logging table so that it contains a column of an unsupported type, and if the name of that column corresponds to an unsupported column in the target DML table, then the DML statement fails at parse time.
  + If the error logging table does not contain any unsupported column types, then all DML errors are logged until the reject limit of errors is reached. For rows on which errors occur, column values with corresponding columns in the error logging table are logged along with the control information.

Examples

Inserting Values into Tables: Examples The following statement inserts a row into the sample table `departments`:

```
INSERT INTO departments
   VALUES (280, 'Recreation', 121, 1700);
```

If the `departments` table had been created with a default value of 121 for the `manager_id` column, then you could issue the same statement as follows:

```
INSERT INTO departments
   VALUES (280, 'Recreation', DEFAULT, 1700);
```

The following statement inserts a row with six columns into the `employees` table. One of these columns is assigned `NULL` and another is assigned a number in scientific notation:

```
INSERT INTO employees (employee_id, last_name, email, 
      hire_date, job_id, salary, commission_pct) 
   VALUES (207, 'Gregory', 'pgregory@example.com', 
      sysdate, 'PU_CLERK', 1.2E3, NULL);
```

The following statement has the same effect as the preceding example, but uses a subquery in the `DML_table_expression_clause`:

```
INSERT INTO 
   (SELECT employee_id, last_name, email, hire_date, job_id, 
      salary, commission_pct FROM employees) 
   VALUES (207, 'Gregory', 'pgregory@example.com', 
      sysdate, 'PU_CLERK', 1.2E3, NULL);
```

Inserting Values with a Subquery: Example The following statement copies employees whose commission exceeds 25% of their salary into the `bonuses` table, which was created in ["Merging into a Table: Example"](statements_9016.md#i2091840):

```
INSERT INTO bonuses
   SELECT employee_id, salary*1.1 
   FROM employees
   WHERE commission_pct > 0.25;
```

Inserting Into a Table with Error Logging: Example The following statements create a `raises` table in the sample schema `hr`, create an error logging table using the `DBMS_ERRLOG` package, and populate the `raises` table with data from the `employees` table. One of the inserts violates the check constraint on `raises`, and that row can be seen in `errlog`. If more than ten errors had occurred, then the statement would have aborted, rolling back any insertions made:

```
CREATE TABLE raises (emp_id NUMBER, sal NUMBER 
   CONSTRAINT check_sal CHECK(sal > 8000));

EXECUTE DBMS_ERRLOG.CREATE_ERROR_LOG('raises', 'errlog');
```

```
INSERT INTO raises
   SELECT employee_id, salary*1.1 FROM employees
   WHERE commission_pct > .2
   LOG ERRORS INTO errlog ('my_bad') REJECT LIMIT 10;

SELECT ORA_ERR_MESG$, ORA_ERR_TAG$, emp_id, sal FROM errlog;

ORA_ERR_MESG$               ORA_ERR_TAG$         EMP_ID SAL
--------------------------- -------------------- ------ -------
ORA-02290: check constraint my_bad               161    7700
 (HR.SYS_C004266) violated
```

Inserting into a Remote Database: Example The following statement inserts a row into the `employees` table owned by the user `hr` on the database accessible by the database link `remote`:

```
INSERT INTO employees@remote
   VALUES (8002, 'Juan', 'Fernandez', 'juanf@example.com', NULL, 
   TO_DATE('04-OCT-1992', 'DD-MON-YYYY'), 'SH_CLERK', 3000, 
   NULL, 121, 20);
```

Inserting Sequence Values: Example The following statement inserts a new row containing the next value of the `departments_seq` sequence into the `departments` table:

```
INSERT INTO departments 
   VALUES  (departments_seq.nextval, 'Entertainment', 162, 1400);
```

Inserting Using Bind Variables: Example The following example returns the values of the inserted rows into output bind variables :`bnd1` and :`bnd2`. The bind variables must first be declared.

```
INSERT INTO employees 
      (employee_id, last_name, email, hire_date, job_id, salary)
   VALUES 
   (employees_seq.nextval, 'Doe', 'john.doe@example.com', 
       SYSDATE, 'SH_CLERK', 2400) 
   RETURNING salary*12, job_id INTO :bnd1, :bnd2;
```

Inserting into a Substitutable Tables and Columns: Examples The following example inserts into the `persons` table, which is created in ["Substitutable Table and Column Examples"](statements_7002.md#i2090577). The first statement uses the root type `person_t`. The second insert uses the `employee_t` subtype of `person_t`, and the third insert uses the `part_time_emp_t` subtype of `employee_t`:

```
INSERT INTO persons VALUES (person_t('Bob', 1234));
INSERT INTO persons VALUES (employee_t('Joe', 32456, 12, 100000));
INSERT INTO persons VALUES (
   part_time_emp_t('Tim', 5678, 13, 1000, 20));
```

The following example inserts into the `books` table, which was created in ["Substitutable Table and Column Examples"](statements_7002.md#i2090577). Notice that specification of the attribute values is identical to that for the substitutable table example:

```
INSERT INTO books VALUES (
   'An Autobiography', person_t('Bob', 1234));
INSERT INTO books VALUES (
   'Business Rules', employee_t('Joe', 3456, 12, 10000));
INSERT INTO books VALUES (
   'Mixing School and Work', 
   part_time_emp_t('Tim', 5678, 13, 1000, 20));
```

You can extract data from substitutable tables and columns using built-in functions and conditions. For examples, see the functions [TREAT](functions218.md#i1018806) and [SYS\_TYPEID](functions188.md#i1044156), and ["IS OF type Condition"](conditions014.md#i1051274).

Inserting Using the TO\_LOB Function: Example The following example copies `LONG` data to a LOB column in the following `long_tab` table:

```
CREATE TABLE long_tab (pic_id NUMBER, long_pics LONG RAW);
```

First you must create a table with a LOB.

```
CREATE TABLE lob_tab (pic_id NUMBER, lob_pics BLOB);
```

Next, use an `INSERT` ... `SELECT` statement to copy the data in all rows for the `LONG` column into the newly created LOB column:

```
INSERT INTO lob_tab 
   SELECT pic_id, TO_LOB(long_pics) FROM long_tab;
```

When you are confident that the migration has been successful, you can drop the `long_pics` table. Alternatively, if the table contains other columns, then you can simply drop the `LONG` column from the table as follows:

```
ALTER TABLE long_tab DROP COLUMN long_pics;
```

Multitable Inserts: Examples  The following example uses the multitable insert syntax to insert into the sample table `sh.sales` some data from an input table with a different structure.

Note:

A number of

`NOT` `NULL`

constraints on the

`sales`

table have been disabled for purposes of this example, because the example ignores a number of table columns for the sake of brevity.

The input table looks like this:

```
SELECT * FROM sales_input_table;

PRODUCT_ID CUSTOMER_ID WEEKLY_ST  SALES_SUN  SALES_MON  SALES_TUE  SALES_WED SALES_THU  SALES_FRI  SALES_SAT
---------- ----------- --------- ---------- ---------- ---------- -------------------- ---------- ----------
       111         222 01-OCT-00        100        200        300        400       500        600        700
       222         333 08-OCT-00        200        300        400        500       600        700        800
       333         444 15-OCT-00        300        400        500        600       700        800        900
```

```

```

The multitable insert statement looks like this:

```
INSERT ALL
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date, sales_sun)
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date+1, sales_mon)
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date+2, sales_tue)
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date+3, sales_wed)
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date+4, sales_thu)
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date+5, sales_fri)
      INTO sales (prod_id, cust_id, time_id, amount)
      VALUES (product_id, customer_id, weekly_start_date+6, sales_sat)
   SELECT product_id, customer_id, weekly_start_date, sales_sun,
      sales_mon, sales_tue, sales_wed, sales_thu, sales_fri, sales_sat
      FROM sales_input_table;
```

Assuming these are the only rows in the `sales` table, the contents now look like this:

```
SELECT * FROM sales
   ORDER BY prod_id, cust_id, time_id;

   PROD_ID    CUST_ID TIME_ID   C   PROMO_ID QUANTITY_SOLD     AMOUNT       COST
---------- ---------- --------- - ---------- ------------- ---------- ----------
       111        222 01-OCT-00                                   100
       111        222 02-OCT-00                                   200
       111        222 03-OCT-00                                   300
       111        222 04-OCT-00                                   400
       111        222 05-OCT-00                                   500
       111        222 06-OCT-00                                   600
       111        222 07-OCT-00                                   700
       222        333 08-OCT-00                                   200
       222        333 09-OCT-00                                   300
       222        333 10-OCT-00                                   400
       222        333 11-OCT-00                                   500
       222        333 12-OCT-00                                   600
       222        333 13-OCT-00                                   700
       222        333 14-OCT-00                                   800
       333        444 15-OCT-00                                   300
       333        444 16-OCT-00                                   400
       333        444 17-OCT-00                                   500
       333        444 18-OCT-00                                   600
       333        444 19-OCT-00                                   700
       333        444 20-OCT-00                                   800
       333        444 21-OCT-00                                   900
```

The next examples insert into multiple tables. Suppose you want to provide to sales representatives some information on orders of various sizes. The following example creates tables for small, medium, large, and special orders and populates those tables with data from the sample table `oe.orders`:

```
CREATE TABLE small_orders 
   (order_id       NUMBER(12)   NOT NULL,
    customer_id    NUMBER(6)    NOT NULL,
    order_total    NUMBER(8,2),
    sales_rep_id   NUMBER(6)
   );

CREATE TABLE medium_orders AS SELECT * FROM small_orders;

CREATE TABLE large_orders AS SELECT * FROM small_orders;

CREATE TABLE special_orders 
   (order_id       NUMBER(12)    NOT NULL,
    customer_id    NUMBER(6)     NOT NULL,
    order_total    NUMBER(8,2),
    sales_rep_id   NUMBER(6),
    credit_limit   NUMBER(9,2),
    cust_email     VARCHAR2(30)
   );
```

The first multitable insert populates only the tables for small, medium, and large orders:

```
INSERT ALL
   WHEN order_total <= 100000 THEN
      INTO small_orders
   WHEN order_total > 100000 AND order_total <= 200000 THEN
      INTO medium_orders
   WHEN order_total > 200000 THEN
      INTO large_orders
   SELECT order_id, order_total, sales_rep_id, customer_id
      FROM orders;
```

You can accomplish the same thing using the `ELSE` clause in place of the insert into the `large_orders` table:

```
INSERT ALL
   WHEN order_total <= 100000 THEN
      INTO small_orders
   WHEN order_total > 100000 AND order_total <= 200000 THEN
      INTO medium_orders
   ELSE
      INTO large_orders
   SELECT order_id, order_total, sales_rep_id, customer_id
      FROM orders;
```

The next example inserts into the small, medium, and large tables, as in the preceding example, and also puts orders greater than 290,000 into the `special_orders` table. This table also shows how to use column aliases to simplify the statement:

```
INSERT ALL
   WHEN ottl <= 100000 THEN
      INTO small_orders
         VALUES(oid, ottl, sid, cid)
   WHEN ottl > 100000 and ottl <= 200000 THEN
      INTO medium_orders 
         VALUES(oid, ottl, sid, cid)
   WHEN ottl > 200000 THEN
      into large_orders
         VALUES(oid, ottl, sid, cid)
   WHEN ottl > 290000 THEN
      INTO special_orders
   SELECT o.order_id oid, o.customer_id cid, o.order_total ottl,
      o.sales_rep_id sid, c.credit_limit cl, c.cust_email cem
      FROM orders o, customers c
      WHERE o.customer_id = c.customer_id;
```

Finally, the next example uses the `FIRST` clause to put orders greater than 290,000 into the `special_orders` table and exclude those orders from the `large_orders` table:

```
INSERT FIRST
   WHEN ottl <= 100000 THEN
      INTO small_orders
         VALUES(oid, ottl, sid, cid)
   WHEN ottl > 100000 and ottl <= 200000 THEN
      INTO medium_orders
         VALUES(oid, ottl, sid, cid)
   WHEN ottl > 290000 THEN
      INTO special_orders
   WHEN ottl > 200000 THEN
      INTO large_orders
         VALUES(oid, ottl, sid, cid)
   SELECT o.order_id oid, o.customer_id cid, o.order_total ottl,
      o.sales_rep_id sid, c.credit_limit cl, c.cust_email cem
      FROM orders o, customers c
      WHERE o.customer_id = c.customer_id;
```