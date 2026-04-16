# Oracle 21c - INSERT
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/INSERT.html

DML\_table\_expression\_clause

Use the `INTO` `DML_table_expression_clause` to specify the objects into which data is being inserted.

schema

Specify the schema containing the table, view, or materialized view. If you omit `schema`, then the database assumes the object is in your own schema.

table | view | materialized\_view | subquery

Specify the name of the table or object table, view or object view, materialized view, or the column or columns returned by a subquery, into which rows are to be inserted. If you specify a view or object view, then the database inserts rows into the base table of the view.

You cannot insert rows into a read-only materialized view. If you insert rows into a writable materialized view, then the database inserts the rows into the underlying container table. However, the insertions are overwritten at the next refresh operation. If you insert rows into an updatable materialized view that is part of a materialized view group, then the database also inserts the corresponding rows into the master table.

If any value to be inserted is a `REF` to an object table, and if the object table has a primary key object identifier, then the column into which you insert the `REF` must be a `REF` column with a referential integrity or `SCOPE` constraint to the object table.

If `table`, or the base table of `view`, contains one or more domain index columns, then this statement executes the appropriate indextype insert routine.

Issuing an `INSERT` statement against a table fires any `INSERT` triggers defined on the table.

Restrictions on the DML\_table\_expression\_clause

This clause is subject to the following restrictions:

* You cannot execute this statement if `table` or the base table of `view` contains any domain indexes marked `IN_PROGRESS` or `FAILED`.
* You cannot insert into a partition if any affected index partitions are marked `UNUSABLE`.
* With regard to the `ORDER` `BY` clause of the `subquery` in the `DML_table_expression_clause`, ordering is guaranteed only for the rows being inserted, and only within each extent of the table. Ordering of new rows with respect to existing rows is not guaranteed.
* If a view was created using the `WITH` `CHECK` `OPTION`, then you can insert into the view only rows that satisfy the defining query of the view.
* If a view was created using a single base table, then you can insert rows into the view and then retrieve those values using the `returning_clause`.
* You cannot insert rows into a view except with `INSTEAD` `OF` triggers if the defining query of the view contains one of the following constructs:

  + A set operator
  + A `DISTINCT` operator
  + An aggregate or analytic function
  + A `GROUP` `BY`, `ORDER` `BY`, `MODEL`, `CONNECT` `BY`, or `START` `WITH` clause
  + A collection expression in a `SELECT` list
  + A subquery in a `SELECT` list
  + A subquery designated `WITH READ ONLY`
  + Joins, with some exceptions, as documented in [Oracle Database Administrator's Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/21/sqlrf&id=ADMIN020)
* If you specify an index, index partition, or index subpartition that has been marked `UNUSABLE`, then the `INSERT` statement will fail unless the `SKIP_UNUSABLE_INDEXES` session parameter has been set to `TRUE`. Refer to [ALTER SESSION](ALTER-SESSION.md#GUID-27186B28-7EFC-4998-B1ED-2B905CC0211B) for information on the `SKIP_UNUSABLE_INDEXES` session parameter.

partition\_extension\_clause

Specify the name or partition key value of the partition or subpartition within `table`, or the base table of `view`, targeted for inserts.

If a row to be inserted does not map into a specified partition or subpartition, then the database returns an error.

Restriction on Target Partitions and Subpartitions

This clause is not valid for object tables or object views.

dblink

Specify a complete or partial name of a database link to a remote database where the table or view is located.

You can insert rows into a remote table or view only if you are using Oracle Database distributed functionality.

To insert rows into a remote table you must have both `INSERT` and `SELECT` privileges on the table.

If you omit `dblink`, then Oracle Database assumes that the table or view is on the local database. You can insert rows into a local table with just the `INSERT` privilege.

subquery\_restriction\_clause

Use the `subquery_restriction_clause` to restrict the subquery in one of the following ways:

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

t\_alias

Specify a correlation name, which is an alias for the table, view, materialized view, or subquery to be referenced elsewhere in the statement.

Restriction on Table Aliases

You cannot specify `t_alias` during a multitable insert.

column

Specify a column of the table, view, or materialized view. In the inserted row, each column in this list is assigned a value from the `values_clause` or the subquery. If you want to assign a value to an `INVISIBLE` column, then you must include the column in this list.

If you omit one or more of the table's columns from this list, then the column value of that column for the inserted row is the column default value as specified when the table was created or last altered. If any omitted column has a `NOT` `NULL` constraint and no default value, then the database returns an error indicating that the constraint has been violated and rolls back the `INSERT` statement. Refer to [CREATE TABLE](CREATE-TABLE.md#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6) for more information on default column values.

If you omit the column list altogether, then the `values_clause` or query must specify values for all columns in the table.

Examples

Inserting Values into Tables: Examples

The following statement inserts a row into the sample table `departments`:

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

Inserting Values with a Subquery: Example

The following statement copies employees whose commission exceeds 25% of their salary into the `bonuses` table, which was created in "[Merging into a Table: Example](MERGE.md#GUID-5692CCB7-24D9-4C0E-81A7-A22436DC968F__I2091840)":

```
INSERT INTO bonuses
   SELECT employee_id, salary*1.1 
   FROM employees
   WHERE commission_pct > 0.25;
```

Inserting Into a Table with Error Logging: Example

The following statements create a `raises` table in the sample schema `hr`, create an error logging table using the `DBMS_ERRLOG` package, and populate the `raises` table with data from the `employees` table. One of the inserts violates the check constraint on `raises`, and that row can be seen in `errlog`. If more than ten errors had occurred, then the statement would have aborted, rolling back any insertions made:

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

Inserting into a Remote Database: Example

The following statement inserts a row into the `employees` table owned by the user `hr` on the database accessible by the database link `remote`:

```
INSERT INTO employees@remote
   VALUES (8002, 'Juan', 'Fernandez', 'juanf@example.com', NULL, 
   TO_DATE('04-OCT-1992', 'DD-MON-YYYY'), 'SH_CLERK', 3000, 
   NULL, 121, 20);
```

Inserting Sequence Values: Example

The following statement inserts a new row containing the next value of the `departments_seq` sequence into the `departments` table:

```
INSERT INTO departments 
   VALUES  (departments_seq.nextval, 'Entertainment', 162, 1400);
```

Inserting Using Bind Variables: Example

The following example returns the values of the inserted rows into output bind variables :`bnd1` and :`bnd2`. The bind variables must first be declared.

```
INSERT INTO employees 
      (employee_id, last_name, email, hire_date, job_id, salary)
   VALUES 
   (employees_seq.nextval, 'Doe', 'john.doe@example.com', 
       SYSDATE, 'SH_CLERK', 2400) 
   RETURNING salary*12, job_id INTO :bnd1, :bnd2;
```

Inserting into a Substitutable Tables and Columns: Examples

The following example inserts into the `persons` table, which is created in "[Substitutable Table and Column Examples](CREATE-TABLE.md#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6__I2090577)". The first statement uses the root type `person_t`. The second insert uses the `employee_t` subtype of `person_t`, and the third insert uses the `part_time_emp_t` subtype of `employee_t`:

```
INSERT INTO persons VALUES (person_t('Bob', 1234));
INSERT INTO persons VALUES (employee_t('Joe', 32456, 12, 100000));
INSERT INTO persons VALUES (
   part_time_emp_t('Tim', 5678, 13, 1000, 20));
```

The following example inserts into the `books` table, which was created in "[Substitutable Table and Column Examples](CREATE-TABLE.md#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6__I2090577)". Notice that specification of the attribute values is identical to that for the substitutable table example:

```
INSERT INTO books VALUES (
   'An Autobiography', person_t('Bob', 1234));
INSERT INTO books VALUES (
   'Business Rules', employee_t('Joe', 3456, 12, 10000));
INSERT INTO books VALUES (
   'Mixing School and Work', 
   part_time_emp_t('Tim', 5678, 13, 1000, 20));
```

You can extract data from substitutable tables and columns using built-in functions and conditions. For examples, see the functions [TREAT](TREAT.md#GUID-037C0CD3-C256-4A02-80E0-C6F15147C5BF) and [SYS\_TYPEID](SYS_TYPEID.md#GUID-4E3D45A1-7433-495D-9062-88505A1496E0), and "[IS OF type Condition](IS-OF-type-Condition.md#GUID-7254E4C7-0194-4C1F-A3B2-2CFB0AD907CD)".

Inserting Using the TO\_LOB Function: Example

The following example copies `LONG` data to a LOB column in the following `long_tab` table:

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

Multitable Inserts: Examples

The following example uses the multitable insert syntax to insert into the sample table `sh.sales` some data from an input table with a different structure.

Note:

A number of `NOT` `NULL` constraints on the `sales` table have been disabled for purposes of this example, because the example ignores a number of table columns for the sake of brevity.

The input table looks like this:

```
SELECT * FROM sales_input_table;
```

```
PRODUCT_ID CUSTOMER_ID WEEKLY_ST  SALES_SUN  SALES_MON  SALES_TUE  SALES_WED SALES_THU  SALES_FRI  SALES_SAT
---------- ----------- --------- ---------- ---------- ---------- -------------------- ---------- ----------
       111         222 01-OCT-00        100        200        300        400       500        600        700
       222         333 08-OCT-00        200        300        400        500       600        700        800
       333         444 15-OCT-00        300        400        500        600       700        800        900
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
    cust_email     VARCHAR2(40)
   );
```

The first multitable insert populates only the tables for small, medium, and large orders:

```
INSERT ALL
   WHEN order_total <= 100000 THEN
      INTO small_orders
   WHEN order_total > 1000000 AND order_total <= 200000 THEN
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

Inserting Multiple Rows Using a Single Statement: Example

The following statements create three tables named people, patients and staff:

```
CREATE TABLE people ( 
  person_id   INTEGER NOT NULL PRIMARY KEY, 
  given_name  VARCHAR2(100) NOT NULL, 
  family_name VARCHAR2(100) NOT NULL, 
  title       VARCHAR2(20), 
  birth_date  DATE 
);

CREATE TABLE patients ( 
  patient_id          INTEGER NOT NULL PRIMARY KEY REFERENCES people (person_id), 
  last_admission_date DATE 
);

CREATE TABLE staff ( 
  staff_id   INTEGER NOT NULL PRIMARY KEY REFERENCES people (person_id), 
  hired_date DATE 
);
```

The following statement inserts a row into the people table:

```
INSERT INTO people 
VALUES (1, 'Dave', 'Badger', 'Mr', date'1960-05-01');
```

The following statement returns an error as there is no value provided for the birth\_date column:

```
INSERT INTO people 
VALUES (2, 'Simon', 'Fox', 'Mr');
```

The following statement inserts a row into the people table:

```
INSERT INTO people (person_id, given_name, family_name, title) 
VALUES (2, 'Simon', 'Fox', 'Mr');
```

The following statement inserts a row into the people table and the value for the title column is populated by selecting a static value from the dual table:

```
INSERT INTO people (person_id, given_name, family_name, title) 
VALUES (3, 'Dave', 'Frog', (SELECT 'Mr' FROM dual));
```

The following statement inserts multiple rows into the people table using âSELECTâ statement:

```
INSERT INTO people (person_id, given_name, family_name, title) 
  WITH names AS ( 
    SELECT 4, 'Ruth',     'Fox',      'Mrs'    FROM dual UNION ALL 
    SELECT 5, 'Isabelle', 'Squirrel', 'Miss'   FROM dual UNION ALL 
    SELECT 6, 'Justin',   'Frog',     'Master' FROM dual UNION ALL 
    SELECT 7, 'Lisa',     'Owl',      'Dr'     FROM dual 
  ) 
  SELECT * FROM names;
```

The following statement rolls back all the previous DML operations:

```
ROLLBACK;
```

The following statement inserts multiple rows into the people table using âSELECTâ statement with a âWHEREâ condition:

```
INSERT INTO people (person_id, given_name, family_name, title) 
  WITH names AS ( 
    SELECT 4, 'Ruth',     'Fox' family_name,      'Mrs'    FROM dual UNION ALL 
    SELECT 5, 'Isabelle', 'Squirrel' family_name, 'Miss'   FROM dual UNION ALL 
    SELECT 6, 'Justin',   'Frog' family_name,     'Master' FROM dual UNION ALL 
    SELECT 7, 'Lisa',     'Owl' family_name,      'Dr'     FROM dual 
  ) 
  SELECT * FROM names 
  WHERE  family_name LIKE 'F%';
```

The following statement rolls back all the previous DML operations:

```
ROLLBACK;
```

The following statement inserts multiple rows into people, patients and staff table using âINSERT ALLâ statement:

```
INSERT ALL 
  /* Every one is a person */ 
  INTO people (person_id, given_name, family_name, title) 
    VALUES (id, given_name, family_name, title) 
  INTO patients (patient_id, last_admission_date) 
    VALUES (id, admission_date) 
  INTO staff (staff_id, hired_date) 
    VALUES (id, hired_date) 
  WITH names AS ( 
    SELECT 4 id, 'Ruth' given_name, 'Fox' family_name, 'Mrs' title, 
           NULL hired_date, DATE'2009-12-31' admission_date 
    FROM   dual UNION ALL 
    SELECT 5 id, 'Isabelle' given_name, 'Squirrel' family_name, 'Miss' title , 
           NULL hired_date, DATE'2014-01-01' admission_date 
    FROM   dual UNION ALL 
    SELECT 6 id, 'Justin' given_name, 'Frog' family_name, 'Master' title, 
           NULL hired_date, DATE'2015-04-22' admission_date 
    FROM   dual UNION ALL 
    SELECT 7 id, 'Lisa' given_name, 'Owl' family_name, 'Dr' title, 
           DATE'2015-01-01' hired_date, NULL admission_date 
    FROM   dual 
  ) 
  SELECT * FROM names;
```

The following statement rolls back all the previous DML operations:

```
ROLLBACK;
```

The following statement inserts multiple rows into people, patients and staff table using âINSERT ALLâ statement with various conditions:

```
INSERT ALL 
  /* Everyone is a person, so insert all rows into people */ 
  WHEN 1=1 THEN 
    INTO people (person_id, given_name, family_name, title) 
    VALUES (id, given_name, family_name, title) 
  /* Only people with an admission date are patients */ 
  WHEN admission_date IS NOT NULL THEN 
    INTO patients (patient_id, last_admission_date) 
    VALUES (id, admission_date) 
  /* Only people with a hired date are staff */ 
  WHEN hired_date IS NOT NULL THEN 
    INTO staff (staff_id, hired_date) 
    VALUES (id, hired_date) 
  WITH names AS ( 
    SELECT 4 id, 'Ruth' given_name, 'Fox' family_name, 'Mrs' title, 
           NULL hired_date, DATE'2009-12-31' admission_date 
    FROM   dual UNION ALL 
    SELECT 5 id, 'Isabelle' given_name, 'Squirrel' family_name, 'Miss' title , 
           NULL hired_date, DATE'2014-01-01' admission_date 
    FROM   dual UNION ALL 
    SELECT 6 id, 'Justin' given_name, 'Frog' family_name, 'Master' title, 
           NULL hired_date, DATE'2015-04-22' admission_date 
    FROM   dual UNION ALL 
    SELECT 7 id, 'Lisa' given_name, 'Owl' family_name, 'Dr' title, 
           DATE'2015-01-01' hired_date, NULL admission_date 
    FROM   dual 
  ) 
  SELECT * FROM names;
```