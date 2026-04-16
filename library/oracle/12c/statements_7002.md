# Oracle 12c - statements_7002
Source: https://docs.oracle.com/database/121/SQLRF/statements_7002.htm

Semantics

relational\_table

GLOBAL TEMPORARY

Specify `GLOBAL` `TEMPORARY` to indicate that the table is temporary and that its definition is visible to all sessions with appropriate privileges. The data in a temporary table is visible only to the session that inserts the data into the table.

When you first create a temporary table, its table metadata is stored in the data dictionary, but no space is allocated for table data. Space is allocated for the table segment at the time of the first DML operation on the table. The temporary table definition persists in the same way as the definitions of regular tables, but the table segment and any data the table contains are either session-specific or transaction-specific data. You specify whether the table segment and data are session- or transaction-specific with the [ON COMMIT](#i2189569) keywords.

You can perform DDL operations (such as `ALTER` `TABLE`, `DROP` `TABLE`, `CREATE` `INDEX`) on a temporary table only when no session is bound to it. A session becomes bound to a temporary table by performing an `INSERT` operation on the table. A session becomes unbound to the temporary table by issuing a `TRUNCATE` statement or at session termination, or, for a transaction-specific temporary table, by issuing a `COMMIT` or `ROLLBACK` statement.

Restrictions on Temporary Tables Temporary tables are subject to the following restrictions:

* Temporary tables cannot be partitioned, clustered, or index organized.
* You cannot specify any foreign key constraints on temporary tables.
* Temporary tables cannot contain columns of nested table.
* You cannot specify the following clauses of the `LOB_storage_clause`: `TABLESPACE`, `storage_clause`, or `logging_clause`.
* Parallel `UPDATE`, `DELETE` and `MERGE` are not supported for temporary tables.
* The only part of the `segment_attributes_clause` you can specify for a temporary table is `TABLESPACE`, which allows you to specify a single temporary tablespace.
* Distributed transactions are not supported for temporary tables.
* A temporary table cannot contain `INVISIBLE` columns.

schema

Specify the schema to contain the table. If you omit `schema`, then the database creates the table in your own schema.

table

Specify the name of the table or object table to be created. The name must satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570).

relational\_properties

The relational properties describe the components of a relational table.

column\_definition

The `column_definition` clause lets you define the characteristics of the column.

Specifying column\_definition with AS subquery If you specify the `AS` `subquery` clause, and each column returned by `subquery` has a column name or is an expression with a specified column alias, then you can omit the `column_definition` clause. In this case, the names of the columns of table are the same as the names of the columns returned by `subquery`. The exception is creating an index-organized table, for which you must specify the `column_definition` clause, because you must designate a primary key column. Regardless of the table type, if you specify the `column_definition` clause and the `AS` `subquery` clause, then you must omit `datatype` from the `column_definition` clause.

column

Specify the name of a column of the table.

If you also specify `AS` `subquery`, then you can omit `column` and `datatype` unless you are creating an index-organized table. If you specify `AS` `subquery` when creating an index-organized table, then you must specify `column`, and you must omit `datatype`.

The absolute maximum number of columns in a table is 1000. When you create an object table or a relational table with columns of object, nested table, varray, or `REF` type, Oracle Database maps the columns of the user-defined types to relational columns, in effect creating hidden columns that count toward the 1000-column limit.

datatype

Specify the data type of a column.

In general, you must specify `datatype`. However, the following exceptions apply:

* You must omit `datatype` if you specify the `AS` `subquery` clause.
* You can also omit `datatype` if the statement designates the column as part of a foreign key in a referential integrity constraint. Oracle Database automatically assigns to the column the data type of the corresponding column of the referenced key of the referential integrity constraint.

Restrictions on Table Column Data Types The following restrictions apply to the data types of table columns:

* Do not create a table with `LONG` columns. Use LOB columns (`CLOB`, `NCLOB`, `BLOB`) instead. `LONG` columns are supported only for backward compatibility.
* You can specify a column of type `ROWID`, but Oracle Database does not guarantee that the values in such columns are valid rowids.

See Also:

["Data Types"](sql_elements001.md#i45441)

for information on

`LONG`

columns and on Oracle-supplied data types

SORT

The `SORT` keyword is valid only if you are creating this table as part of a hash cluster and only for columns that are also cluster columns.

This clause instructs the database to sort the rows of the cluster on this column after applying the hash function when performing a DML operation. Doing so may improve response time during subsequent operations on the clustered data.

VISIBLE | INVISIBLE

Use this clause to specify whether `column` is `VISIBLE` or `INVISIBLE`. The default is `VISIBLE`.

`INVISIBLE` columns are user-specified hidden columns. To display or assign a value to an `INVISIBLE` column, you must specify its name explicitly. For example:

* The `SELECT` `*` syntax will not display an `INVISIBLE` column. However, if you include an `INVISIBLE` column in the select list of a `SELECT` statement, then the column will be displayed.
* You cannot implicitly specify a value for an `INVISIBLE` column in the `VALUES` clause of an `INSERT` statement. You must specify the `INVISIBLE` column in the column list.
* You must explicitly specify an `INVISIBLE` column in Oracle Call Interface (OCI) describes.
* You can configure SQL\*Plus to allow `INVISIBLE` column information to be viewed with the `DESCRIBE` command. Refer to [SQL\*Plus User's Guide and Reference](../SQPUG/ch_twelve040.md#SQPUG303) for more information.

Notes on VISIBLE and INVISIBLE Columns The following notes apply to `VISIBLE` and `INVISIBLE` columns:

* An `INVISIBLE` column can be used as a partitioning key when specified as part of `CREATE` `TABLE`.
* You can specify `INVISIBLE` columns in a `column_expression`.
* A virtual column can be an `INVISIBLE` column.
* PL/SQL `%ROWTYPE` attributes do not show `INVISIBLE` columns.
* The `COLUMN_ID` column of the `ALL_`, `DBA_`, and `USER_TAB_COLUMNS` data dictionary views determines the order in which a `SELECT` `*` query returns columns for a table, view, or materialized view. The value of `COLUMN_ID` is NULL for `INVISIBLE` columns. When you make an invisible column visible, it will be assigned the next highest available `COLUMN_ID` value. When you make a visible column invisible, its `COLUMN_ID` value is set to NULL and `COLUMN_ID` is decremented by 1 for any columns with a higher `COLUMN_ID`.

Restrictions on VISIBLE and INVISIBLE Columns The following restrictions apply to `VISIBLE` and `INVISIBLE` columns:

* `INVISIBLE` columns are not supported in external tables, cluster tables, or temporary tables.
* You cannot make a system-generated hidden column visible.

  Note:

  To determine whether a column is a system-generated hidden column, query the

  `HIDDEN_COLUMN`

  and

  `USER_GENERATED`

  columns of the

  `ALL_`

  ,

  `DBA_`

  , and

  `USER_TAB_COLS`

  data dictionary views. Refer to

  [Oracle Database Reference](../REFRN/GUID-85036F42-140A-406B-BE11-0AC49A00DBA3.md#REFRN20276)

  for more information.

DEFAULT

The `DEFAULT` clause lets you specify a value to be assigned to the column if a subsequent `INSERT` statement omits a value for the column. The data type of the expression must match the data type specified for the column. The column must also be large enough to hold this expression.

The `DEFAULT` expression can include any SQL function as long as the function does not return a literal argument, a column reference, or a nested function invocation.

The `DEFAULT` expression can include the sequence pseudocolumns `CURRVAL` and `NEXTVAL`, as long as the sequence exists and you have the privileges necessary to access it. Users who perform subsequent inserts that use the `DEFAULT` expression must have the `INSERT` privilege on the table and the `SELECT` privilege on the sequence. If the sequence is later dropped, then subsequent `INSERT` statements where the `DEFAULT` expression is used will result in an error. If you do not fully qualify the sequence by specifying the sequence owner, for example, `SCOTT`.`SEQ1`, then Oracle Database will default the sequence owner to be the user who issues the `CREATE` `TABLE` statement. For example, if user `MARY` creates `SCOTT`.`TABLE` and refers to a sequence that is not fully qualified, such as `SEQ2`, then the column will use sequence `MARY`.`SEQ2`. Synonyms on sequences undergo a full name resolution and are stored as the fully qualified sequence in the data dictionary; this is true for public and private synonyms. For example, if user `BETH` adds a column referring to public or private synonym `SYN1` and the synonym refers to `PETER`.`SEQ7`, then the column will store `PETER`.`SEQ7` as the default.

Restrictions on Default Column Values Default column values are subject to the following restrictions:

* A `DEFAULT` expression cannot contain references to PL/SQL functions or to other columns, the pseudocolumns `LEVEL`, `PRIOR`, and `ROWNUM`, or date constants that are not fully specified.
* The expression can be of any form except a scalar subquery expression.

ON NULL If you specify the `ON` `NULL` clause, then Oracle Database assigns the `DEFAULT` column value when a subsequent `INSERT` statement attempts to assign a value that evaluates to NULL.

When you specify `ON` `NULL`, the `NOT` `NULL` constraint and `NOT` `DEFERRABLE` constraint state are implicitly specified. If you specify an inline constraint that conflicts with `NOT` `NULL` and `NOT` `DEFERRABLE`, then an error is raised.

Restriction on the ON NULL Clause You cannot specify this clause for an object type column or a REF column.

identity\_clause

Use this clause to specify an identity column. The identity column will be assigned an increasing or decreasing integer value from a sequence generator for each subsequent `INSERT` statement. You can use the `identity_options` clause to configure the sequence generator.

ALWAYS If you specify `ALWAYS`, then Oracle Database always uses the sequence generator to assign a value to the column. If you attempt to explicitly assign a value to the column using `INSERT` or `UPDATE`, then an error will be returned. This is the default.

BY DEFAULT If you specify `BY` `DEFAULT`, then Oracle Database uses the sequence generator to assign a value to the column by default, but you can also explicitly assign a specified value to the column. If you specify `ON` `NULL`, then Oracle Database uses the sequence generator to assign a value to the column when a subsequent `INSERT` statement attempts to assign a value that evaluates to NULL.

identity\_options

Use the `identity_options` clause to configure the sequence generator. The `identity_options` clause has the same parameters as the `CREATE` `SEQUENCE` statement. Refer to [CREATE SEQUENCE](statements_6017.md#i2067093) for a full description of these parameters and characteristics. The exception is `START` `WITH` `LIMIT VALUE`, which is specific to `identity_options` and can only be used with `ALTER` `TABLE` `MODIFY`. Refer to [identity\_options](statements_3001.md#CJABEJEF) for more information.

Note:

When you create an identity column, Oracle recommends that you specify the

`CACHE`

clause with a value higher than the default of 20 to enhance performance.

Restrictions on Identity Columns Identity columns are subject to the following restrictions:

* You can specify only one identity column per table.
* If you specify `identity_clause`, then you must specify a numeric data type for `datatype` in the `column_definition` clause. You cannot specify a user-defined data type.
* If you specify `identity_clause`, then you cannot specify the `DEFAULT` clause in the `column_definition` clause.
* When you specify `identity_clause`, the `NOT` `NULL` constraint and `NOT` `DEFERRABLE` constraint state are implicitly specified. If you specify an inline constraint that conflicts with `NOT` `NULL` and `NOT` `DEFERRABLE`, then an error is raised.
* If an identity column is encrypted, then the encryption algorithm may be inferred. Oracle recommends that you use a strong encryption algorithm on identity columns.
* `CREATE` `TABLE` `AS` `SELECT` will not inherit the identity property on a column.

encryption\_spec

The `ENCRYPT` clause lets you use the Transparent Data Encryption (TDE) feature to encrypt the column you are defining. You can encrypt columns of type `CHAR`, `NCHAR`, `VARCHAR2`, `NVARCHAR2`, `NUMBER`, `DATE`, LOB, and `RAW`. The data does not appear in its encrypted form to authorized users, such as the user who encrypts the column.

Note:

Column encryption requires that a system administrator with appropriate privileges has initialized the security module, opened a keystore, and set an encryption key. Refer to

[Oracle Database Advanced Security Guide](../ASOAG/introduction-to-transparent-data-encryption.md#ASOAG10137)

for general information about column encryption and to

[security\_clauses](statements_2017.md#BGBCEDHJ)

for related

`ALTER` `SYSTEM`

statements.

USING 'encrypt\_algorithm' Use this clause to specify the name of the algorithm to be used. Valid algorithms are `AES256`, `AES192`, `AES128` and `3DES168`. If you omit this clause, then the database uses `AES192`. If you encrypt more than one column in the same table, and if you specify the `USING` clause for one of the columns, then you must specify the same encryption algorithm for all the encrypted columns.

IDENTIFIED BY password If you specify this clause, then the database derives the column key from the specified password.

'integrity\_algorithm' Use this clause to specify the integrity algorithm to be used. Valid integrity algorithms are `SHA-1` and `NOMAC`.

* If you specify `SHA-1`, then TDE uses the Secure Hash Algorithm (SHA-1) and adds a 20-byte Message Authentication Code (MAC) to each encrypted value for integrity checking. This is the default.
* If you specify `NOMAC`, then TDE does not add a MAC and does not perform the integrity check. This saves 20 bytes of disk space per encrypted value. Refer to [Oracle Database Advanced Security Guide](../ASOAG/configuring-transparent-data-encryption.md#ASOAG10146) for more information on using `NOMAC` to save disk space and improve performance.

All encrypted columns in a table must use the same integrity algorithm. If you already have a table column using the `SHA-1` algorithm, then you cannot use the `NOMAC` parameter to encrypt another column in the same table. Refer to the [REKEY encryption\_spec](statements_3001.md#CJAEGJGI) clause of `ALTER` `TABLE` to learn how to change the integrity algorithm used by all encrypted columns in a table.

SALT | NO SALT Specify `SALT` to instruct the database to append a random string, called "salt," to the clear text of the column before encrypting it. This is the default.

Specify `NO` `SALT` to prevent the database from appending salt to the clear text of the column before encrypting it.

The following considerations apply when specifying `SALT` or `NO` `SALT` for encrypted columns:

* If you want to use the column as an index key, then you must specify `NO` `SALT`. Refer to [Oracle Database Advanced Security Guide](../ASOAG/configuring-transparent-data-encryption.md#ASOAG9538) for a description of "salt" in this context.
* If you specify table compression for the table, then the database does not compress the data in encrypted columns with `SALT`.

You cannot specify `SALT` or `NO` `SALT` for LOB encryption.

Restrictions on encryption\_spec: The following restrictions apply to column encryption:

* Transparent Data Encryption is not supported by the traditional import and export utilities or by transportable-tablespace-based export. Use the Data Pump import and export utilities with encrypted columns instead.
* To encrypt a column in an external table, the table must use `ORACLE_DATAPUMP` as its access type.
* You cannot encrypt a column in tables owned by `SYS`.
* You cannot encrypt a foreign key column.

virtual\_column\_definition

The `virtual_column_definition` clause lets you create a virtual column. A virtual column is not stored on disk. Rather, the database derives the values in a virtual column on demand by computing a set of expressions or functions. Virtual columns can be used in queries, DML, and DDL statements. They can be indexed, and you can collect statistics on them. Thus, they can be treated much as other columns. Exceptions and restrictions are listed below in ["Notes on Virtual Columns"](#BABIJIHJ) and ["Restrictions on Virtual Columns"](#BABIIGBD).

column For `column`, specify the name of the virtual column.

datatype You can optionally specify the data type of the virtual column. If you omit `datatype`, then the database determines the data type of the column based on the data type of the underlying expressions. All Oracle scalar data types and `XMLType` are supported.

VISIBLE | INVISIBLE Use this clause to specify whether virtual column is `VISIBLE` or `INVISIBLE`. The default is `VISIBLE`. For complete information, refer to ["VISIBLE | INVISIBLE"](#CJAGDBIC).

GENERATED ALWAYS The optional keywords `GENERATED` `ALWAYS` are provided for semantic clarity. They indicate that the column is not stored on disk, but is evaluated on demand.

column\_expression The `AS` `column_expression` clause determines the content of the column. Refer to ["Column Expressions"](expressions005.md#BABIGHHI) for more information on `column_expression`.

VIRTUAL The optional keyword `VIRTUAL` is provided for semantic clarity.

evaluation\_edition\_clause You must specify this clause if `column_expression` refers to an editioned PL/SQL function. Use this clause to specify the edition that is searched during name resolution of the editioned PL/SQL function—the evaluation edition.

* Specify `CURRENT` `EDITION` to search the edition in which this DDL statement is executed.
* Specify `EDITION` `edition` to search `edition`.
* Specifying `NULL` `EDITION` is equivalent to omitting the `evaluation_edition_clause`.

If you omit the `evaluation_edition_clause`, then editioned objects are invisible during name resolution and an error will result. If the evaluation edition is dropped, then a subsequent query on the virtual column will result in an error.

The database does not maintain dependencies on the functions referenced by a virtual column. Therefore, if a virtual column refers to a noneditioned function, and the function becomes editioned, then the following operations may raise an error:

* Querying the virtual column
* Updating a row that includes the virtual column
* Firing a trigger that accesses the virtual column

unusable\_editions\_clause This clause lets you specify that the virtual column expression is unusable for evaluating queries in one or more editions. The remaining editions form a range of editions in which it is safe for the optimizer to use the virtual column expression to evaluate queries.

For example, suppose you define a function-based index on the virtual column. The optimizer can use the function-based index to evaluate queries that contain the virtual column expression in their `WHERE` clause. If a query is compiled in an edition that is in the usable range of editions for the virtual column, then the optimizer will consider using the index to evaluate the query. If a query is compiled in an edition outside the usable range of editions for the virtual column, then the optimizer will not consider using the index.

UNUSABLE BEFORE Clause This clause lets you specify that the virtual column expression is unusable for evaluating queries in the ancestors of an edition.

* If you specify `CURRENT` `EDITION`, then the virtual column expression is unusable in the ancestors of the edition in which this DDL statement is executed.
* If you specify `EDITION` `edition`, then the virtual column expression is unusable in the ancestors of the specified `edition`.

UNUSABLE BEGINNING WITH Clause This clause lets you specify that the virtual column expression is unusable for evaluating queries in an edition and its descendants.

* If you specify `CURRENT` `EDITION`, then the virtual column expression is unusable in the edition in which this DDL statement is executed and its descendants.
* If you specify `EDITION` `edition`, then the virtual column expression is unusable in the specified `edition` and its descendants.
* Specifying `NULL` `EDITION` is equivalent to omitting the `UNUSABLE` `BEGINNING` `WITH` clause.

If an edition specified in this clause is subsequently dropped, there is no effect on the virtual column.

Notes on Virtual Columns

* If `column_expression` refers to a column on which column-level security is implemented, then the virtual column does not inherit the security rules of the base column. In such a case, you must ensure that data in the virtual column is protected, either by duplicating a column-level security policy on the virtual column or by applying a function that implicitly masks the data. For example, it is common for credit card numbers to be protected by a column-level security policy, while still allowing call center employees to view the last four digits of the credit card number for validation purposes. In such a case, you could define the virtual column to take a substring of the last four digits of the credit card number.
* A table index defined on a virtual column is equivalent to a function-based index on the table.
* You cannot directly update a virtual column. Thus, you cannot specify a virtual column in the `SET` clause of an `UPDATE` statement. However, you can specify a virtual column in the `WHERE` clause of an `UPDATE` statement. Likewise, you can specify a virtual column in the `WHERE` clause of a `DELETE` statement to delete rows from a table based on the derived value of the virtual column.
* A query that specifies in its `FROM` clause a table containing a virtual column is eligible for result caching. Refer to ["RESULT\_CACHE Hint"](sql_elements006.md#BABIFIGC) for more information on result caching.
* The `column_expression` can refer to a PL/SQL function if the function is explicitly designated `DETERMINISTIC` during its creation. However, if the function is subsequently replaced, definitions dependent on the virtual column are not invalidated. In such a case, if the table contains data, queries that reference the virtual column may return incorrect results if the virtual column is used in the definition of constraints, indexes, or materialized views or for result caching. Therefore, in order to replace the deterministic PL/SQL function for a virtual column.

  + Disable and re-enable any constraints on the virtual column.
  + Rebuild any indexes on the virtual column.
  + Fully refresh materialized views accessing the virtual column.
  + Flush the result cache if cached queries have accessed the virtual column.
  + Regather statistics on the table.
* A virtual column can be an `INVISIBLE` column. The `column_expression` can contain `INVISIBLE` columns.

Restrictions on Virtual Columns

* You can create virtual columns only in relational heap tables. Virtual columns are not supported for index-organized, external, object, cluster, or temporary tables.
* The `column_expression` in the `AS` clause has the following restrictions:

  + It cannot refer to another virtual column by name.
  + Any columns referenced in `column_expression` must be defined on the same table.
  + It can refer to a deterministic user-defined function, but if it does, then you cannot use the virtual column as a partitioning key column.
  + The output of `column_expression` must be a scalar value.
* The virtual column cannot be an Oracle supplied data type, a user-defined type, or LOB or `LONG` `RAW`.
* You cannot specify a call to a PL/SQL function in the defining expression for a virtual column that you want to use as a partitioning column.

period\_definition

Use the `period_definition` clause to create a valid time dimension for `table`.

This clause implements Temporal Validity support for `table`. If you specify this clause, then one column in `table`, the start time column, contains a start date or timestamp, and another column in `table`, the end time column, contains an end date or timestamp. These two columns define a valid time dimension for `table`—that is, a period of time for which each row is considered valid. You can use Oracle Flashback Query to retrieve rows from `table` based on whether they are considered valid as of a specified time, before a specified time, or during a specified time period.

You can specify at most one valid time dimension when you create a table. You can subsequently add additional valid time dimensions to a table with the [add\_period\_clause](statements_3001.md#CJAEGCFI) of `ALTER` `TABLE`.

valid\_time\_column Specify the name of the valid time dimension. The name must satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570). Oracle Database creates an `INVISIBLE` virtual column with this name of data type `NUMBER` in `table`.

start\_time\_column and end\_time\_column You can optionally specify these clauses as follows:

* Use `start_time_column` to specify the name of the start time column, which contains the start date or timestamp.
* Use `end_time_column` to specify the name of the end time column, which contains the end date or timestamp.

The names you specify for `start_time_column` and `end_time_column` must satisfy the requirements listed in ["Database Object Naming Rules"](sql_elements008.md#i27570).

If you specify these clauses, then you must define `start_time_column` and `end_time_column` in the `column_definition` clause of `CREATE` `TABLE`. Each column must be of a datetime data type (`DATE`, `TIMESTAMP`, `TIMESTAMP` `WITH` `TIME` `ZONE`, or `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`) and can be `VISIBLE` or `INVISIBLE`.

If you do not specify these clauses, then Oracle Database creates a start time column named `valid_time_column``_START`, and an end time column named `valid_time_column``_END`. These columns are of data type `TIMESTAMP` `WITH` `TIME` `ZONE` and are `INVISIBLE`.

You can insert and update values in the start time column and end time column as you would any column, with the following considerations:

* If the value of the start time column is NULL, then the row is considered valid for all time values that occur before, but not including, the value of the end time column.
* If the value of the end time column is NULL, then the row is considered valid for all time values that occur on or after the value of the start time column.
* If the value of neither column is NULL, then the value of the start time column must be earlier than the value of the end time column. The row is considered valid for all time values that occur on or after the value of the start time column, and up to, but not including, the value of the end time column.
* If the value of both columns is NULL, then the row is considered valid for all time values.

Restrictions on Valid Time Dimension Columns The following restrictions apply to valid time dimension columns:

* The `valid_time_column` is for internal use only. You cannot perform DDL or DML operations on it with one exception: You can drop the column by using the `drop_period_clause` of `ALTER` `TABLE`.
* You can drop the start time column and end time column only by using the `drop_period_clause` of `ALTER` `TABLE`.
* If the start time column and end time column are automatically created by Oracle Database, then they are `INVISIBLE` and you cannot subsequently make them `VISIBLE`.

Constraint Clauses

Use these clauses to create constraints on the table columns. You must specify a `PRIMARY` `KEY` constraint for an index-organized table, and it cannot be `DEFERRABLE`. Refer to [constraint](clauses002.md#g1053592) for syntax and description of these constraints as well as examples.

inline\_ref\_constraint and out\_of\_line\_ref\_constraint  These clauses let you describe a column of type `REF`. The only difference between these clauses is that you specify `out_of_line_ref_constraint` from the table level, so you must identify the `REF` column or attribute you are defining. Specify `inline_ref_constraint` as part of the definition of the `REF` column or attribute.

inline\_constraint  Use the `inline_constraint` to define an integrity constraint as part of the column definition.

You can create `UNIQUE`, `PRIMARY` `KEY`, and `REFERENCES` constraints on scalar attributes of object type columns. You can also create `NOT` `NULL` constraints on object type columns and `CHECK` constraints that reference object type columns or any attribute of an object type column.

out\_of\_line\_constraint  Use the `out_of_line_constraint` syntax to define an integrity constraint as part of the table definition.

supplemental\_logging\_props

The `supplemental_logging_props` clause lets you instruct the database to put additional data into the log stream to support log-based tools.

supplemental\_log\_grp\_clause Use this clause to create a named log group.

* The `NO` `LOG` clause lets you omit from the redo log one or more columns that would otherwise be included in the redo for the named log group. You must specify at least one fixed-length column without `NO` `LOG` in the named log group.
* If you specify `ALWAYS`, then during an update, the database includes in the redo all columns in the log group. This is called an unconditional log group (sometimes called an "always log group"), because Oracle Database supplementally logs all the columns in the log group when the associated row is modified. If you omit `ALWAYS`, then the database supplementally logs all the columns in the log group only if any column in the log group is modified. This is called a conditional log group.

You can query the appropriate `USER_`, `ALL_`, or `DBA_LOG_GROUP_COLUMNS` data dictionary view to determine whether any supplemental logging has already been specified.

supplemental\_id\_key\_clause Use this clause to specify that all or a combination of the primary key, unique key, and foreign key columns should be supplementally logged. Oracle Database will generate either an unconditional log group or a conditional log group. With an unconditional log group, the database supplementally logs all the columns in the log group when the associated row is modified. With a conditional log group, the database supplementally logs all the columns in the log group only if any column in the log group is modified.

* If you specify `ALL` `COLUMNS`, then the database includes in the redo log all the fixed-length maximum size columns of that row. Such a redo log is a system-generated unconditional log group.
* If you specify `PRIMARY` `KEY` `COLUMNS`, then for all tables with a primary key, the database places into the redo log all columns of the primary key whenever an update is performed. Oracle Database evaluates which columns to supplementally log as follows:

  + First the database chooses columns of the primary key constraint, if the constraint is validated or marked `RELY` and is not marked as `DISABLED` or `INITIALLY` `DEFERRED`.
  + If no primary key columns exist, then the database looks for the smallest `UNIQUE` index with at least one `NOT` `NULL` column and uses the columns in that index.
  + If no such index exists, then the database supplementally logs all scalar columns of the table.
* If you specify `UNIQUE` `COLUMNS`, then for all tables with a unique key or a bitmap index, if any of the unique key or bitmap index columns are modified, the database places into the redo log all other columns belonging to the unique key or bitmap index. Such a log group is a system-generated conditional log group.
* If you specify `FOREIGN` `KEY` `COLUMNS`, then for all tables with a foreign key, if any foreign key columns are modified, the database places into the redo log all other columns belonging to the foreign key. Such a redo log is a system-generated conditional log group.

If you specify this clause multiple times, then the database creates a separate log group for each specification. You can query the appropriate `USER_`, `ALL_`, or `DBA_LOG_GROUPS` data dictionary view to determine whether any supplemental logging data has already been specified.

ON COMMIT

The `ON` `COMMIT` clause is relevant only if you are creating a temporary table. This clause specifies whether the data in the temporary table persists for the duration of a transaction or a session.

DELETE ROWS Specify `DELETE` `ROWS` for a transaction-specific temporary table. This is the default. Oracle Database will truncate the table (delete all its rows) after each commit.

PRESERVE ROWS Specify `PRESERVE` `ROWS` for a session-specific temporary table. Oracle Database will truncate the table (delete all its rows) when you terminate the session.

physical\_properties

The physical properties relate to the treatment of extents and segments and to the storage characteristics of the table.

deferred\_segment\_creation

Use this clause to determine when the database should create the segment(s) for this table:

* `SEGMENT` `CREATION` `DEFERRED`: This clause defers creation of the table segment — as well as segments for any LOB columns of the table, any indexes created implicitly as part of table creation, and any indexes subsequently explicitly created on the table — until the first row of data is inserted into the table. At that time, the segments for the table, LOB columns and indexes, and explicitly created indexes are all materialized and inherit any storage properties specified in this `CREATE` `TABLE` statement or, in the case of explicitly created indexes, the `CREATE` `INDEX` statement. These segments are created regardless whether the initial insert operation is uncommitted or rolled back. This is the default value.

  Caution:

  When creating many tables with deferred segment creation, ensure that you allocate enough space for your database so that when the first rows are inserted, there is enough space for all the new segments.
* `SEGMENT` `CREATION` `IMMEDIATE`: The table segment is created as part of this `CREATE` `TABLE` statement.

Immediate segment creation is useful, for example, if your application depends upon the object appearing in the `DBA_`, `USER_`, and `ALL_SEGMENTS` data dictionary views, because the object will not appear in those views until the segment is created. This clause overrides the setting of the `DEFERRED_SEGMENT_CREATION` initialization parameter.

To determine whether a segment has been created for an existing table or its LOB columns or indexes, query the `SEGMENT_CREATED` column of `USER_TABLES`, `USER_INDEXES`, or `USER_LOBS`.

Notes on Tables Without Segments  The following rules apply to a table whose segment has not yet been materialized:

* If you create this table with `CREATE` `TABLE` ... `AS` `subquery`, then if the source table has no rows, segment creation of the new table is deferred. If the source table has rows, then segment creation of the new table is not deferred.
* If you specify `ALTER` `TABLE` ... `ALLOCATE` `EXTENT` before the segment is materialized, then the segment is materialized and then an extent is allocated. However the `ALLOCATE` `EXTENT` clause in a DDL statement on any indexes of the table will return an error.
* In a DDL statement on the table or its LOB columns or indexes, any specification of `DEALLOCATE` `UNUSED` is silently ignored.
* `ONLINE` operations on indexes of a table or table partition without a segment will silently be disabled; that is, they will proceed `OFFLINE`.
* If any of the following DDL statements are executed on a table with one or more LOB columns, then the resulting partition(s) or subpartition(s) will be materialized:

  + `ALTER` `TABLE` `SPLIT` `[SUB]PARTITION`
  + `ALTER` `TABLE` `MERGE` `[SUB]PARTITIONS`
  + `ALTER` `TABLE` `ADD` `[SUB]PARTITION` (hash partitions only)
  + `ALTER` `TABLE` `COALESCE` `[SUB]PARTITION` (hash partitions only)

Restrictions on Deferred Segment Creation This clause is subject to the following restrictions:

* You cannot defer segment creation for the following types of tables: index-organized tables, clustered tables, global temporary tables, session-specific temporary tables, internal tables, object tables, `XMLType` tables, AQ tables, external tables, and tables owned by `SYS`, `SYSTEM`, `PUBLIC`, `OUTLN`, or `XDB`.
* Deferred segment creation is not supported for bitmap join indexes and domain indexes.
* Deferred segment creation is not supported in dictionary-managed tablespaces.
* Deferred segment creation is not supported in the `SYSTEM` tablespace.
* Serializable transactions do not work with deferred segment creation. Trying to insert data into an empty table with no segment created causes an error.
* When a global index is marked `UNUSABLE` during a partition maintenance operation, the database does not drop the unusable index segments.

segment\_attributes\_clause

The `segment_attributes_clause` lets you specify physical attributes and tablespace storage for the table.

physical\_attributes\_clause The `physical_attributes_clause` lets you specify the value of the `PCTFREE`, `PCTUSED`, and `INITRANS` parameters and the storage characteristics of the table.

* For a nonpartitioned table, each parameter and storage characteristic you specify determines the actual physical attribute of the segment associated with the table.
* For partitioned tables, the value you specify for the parameter or storage characteristic is the default physical attribute of the segments associated with all partitions specified in this `CREATE` statement (and in subsequent `ALTER` `TABLE` ... `ADD` `PARTITION` statements), unless you explicitly override that value in the `PARTITION` clause of the statement that creates the partition.

If you omit this clause, then Oracle Database sets `PCTFREE` to 10, `PCTUSED` to 40, and `INITRANS` to 1.

TABLESPACE  Specify the tablespace in which Oracle Database creates the table, object table `OIDINDEX`, partition, LOB data segment, LOB index segment, or index-organized table overflow data segment. If you omit `TABLESPACE`, then the database creates that item in the default tablespace of the owner of the schema containing the table.

For a heap-organized table with one or more LOB columns, if you omit the `TABLESPACE` clause for LOB storage, then the database creates the LOB data and index segments in the tablespace where the table is created.

For an index-organized table with one or more LOB columns, if you omit `TABLESPACE`, then the LOB data and index segments are created in the tablespace in which the primary key index segment of the index-organized table is created.

For nonpartitioned tables, the value specified for `TABLESPACE` is the actual physical attribute of the segment associated with the table. For partitioned tables, the value specified for `TABLESPACE` is the default physical attribute of the segments associated with all partitions specified in the `CREATE` statement and on subsequent `ALTER` `TABLE` ... `ADD` `PARTITION` statements, unless you specify `TABLESPACE` in the `PARTITION` description.

logging\_clause

Specify whether the creation of the table and of any indexes required because of constraints, partition, or LOB storage characteristics will be logged in the redo log file (`LOGGING`) or not (`NOLOGGING`).The logging attribute of the table is independent of that of its indexes.

This attribute also specifies whether subsequent direct loader (SQL\*Loader) and direct-path `INSERT` operations against the table, partition, or LOB storage are logged (`LOGGING`) or not logged (`NOLOGGING`).

Refer to [logging\_clause](clauses005.md#i999782) for a full description of this clause.

table\_compression

The `table_compression` clause is valid only for heap-organized tables. Use this clause to instruct the database whether to compress data segments to reduce disk use. The `COMPRESS` clauses enable table compression. The `NOCOMPRESS` clause disables table compression. The default is `NOCOMPRESS`.

COMPRESS Specifying only the keyword `COMPRESS` is equivalent to specifying `ROW` `STORE` `COMPRESS` `BASIC` and enables basic table compression.

ROW STORE COMPRESS BASIC When you enable table compression by specifying either `ROW` `STORE` `COMPRESS` or `ROW` `STORE` `COMPRESS` `BASIC`, you enable basic table compression. Oracle Database attempts to compress data during direct-path `INSERT` operations when it is productive to do so. The original import utility (imp) does not support direct-path `INSERT`, and therefore cannot import data in a compressed format.

Tables with basic table compression use a `PCTFREE` value of 0 to maximize compression, unless you explicitly set a value for `PCTFREE` in the `physical_attributes_clause`.

In earlier releases, basic table compression was enabled using `COMPRESS` `BASIC`. This syntax is still supported for backward compatibility.

ROW STORE COMPRESS ADVANCED When you enable table compression by specifying `ROW` `STORE` `COMPRESS` `ADVANCED`, you enable Advanced Row Compression. Oracle Database compresses data during all DML operations on the table. This form of compression is recommended for OLTP environments.

Tables with `ROW` `STORE` `COMPRESS` `ADVANCED` or `NOCOMPRESS` use the `PCTFREE` default value of 10, to maximize compress while still allowing for some future DML changes to the data, unless you override this default explicitly.

In earlier releases, Advanced Row Compression was called OLTP table compression and was enabled using `COMPRESS` `FOR` `OLTP`. This syntax is still supported for backward compatibility.

COLUMN STORE COMPRESS FOR { QUERY | ARCHIVE } When you specify `COLUMN` `STORE` `COMPRESS` `FOR` `QUERY` or `COLUMN` `STORE` `COMPRESS` `FOR` `ARCHIVE`, you enable Hybrid Columnar Compression. With Hybrid Columnar Compression, data can be compressed during bulk load operations. During the load process, data is transformed into a column-oriented format and then compressed. Oracle Database uses a compression algorithm appropriate for the level you specify. In general, the higher the level, the greater the compression ratio. Hybrid Columnar Compression can result in higher compression ratios, at a greater CPU cost. Therefore, this form of compression is recommended for data that is not frequently updated.

`COLUMN` `STORE` `COMPRESS` `FOR` `QUERY` is useful in data warehousing environments. Valid values are `LOW` and `HIGH`, with `HIGH` providing a higher compression ratio. The default is `HIGH`.

`COLUMN` `STORE` `COMPRESS` `FOR` `ARCHIVE` uses higher compression ratios than `COLUMN` `STORE` `COMPRESS` `FOR` `QUERY`, and is useful for compressing data that will be stored for long periods of time. Valid values are `LOW` and `HIGH`, with `HIGH` providing the highest possible compression ratio. The default is `LOW`.

Specifying `COLUMN` `STORE` `COMPRESS` is equivalent to specifying `COLUMN` `STORE` `COMPRESS` `FOR` `QUERY` `HIGH`.

Tables with `COLUMN` `STORE` `COMPRESS` `FOR` `QUERY` or `COLUMN` `STORE` `COMPRESS` `FOR` `ARCHIVE` use a `PCTFREE` value of 0 to maximize compression, unless you explicitly set a value for `PCTFREE` in the `physical_attributes_clause`. For these tables, `PCTFREE` has no effect for blocks loaded using direct-path `INSERT`. `PCTFREE` is honored for blocks loaded using conventional `INSERT`, and for blocks created as a result of DML operations on blocks originally loaded using direct-path `INSERT`.

[NO] ROW LEVEL LOCKING If you specify `ROW` `LEVEL` `LOCKING`, then Oracle Database uses row-level locking during DML operations. This improves the performance of these operations when accessing Hybrid Columnar Compressed data. If you specify `NO` `ROW` `LEVEL` `LOCKING`, then row-level locking is not used. The default is `NO` `ROW` `LEVEL` `LOCKING`.

In earlier releases, Hybrid Columnar Compression was enabled using `COMPRESS` `FOR` `QUERY` and `COMPRESS` `FOR` `ARCHIVE`. This syntax is still supported for backward compatibility.

See Also:

[Oracle Database Concepts](../CNCPT/tablecls.md#CNCPT89198)

for more information on Hybrid Columnar Compression, which is a feature of certain Oracle storage systems

Notes on Table Compression: You can specify table compression for the following portions of a heap-organized table:

* For an entire table, in the `physical_properties` clause of `relational_table` or `object_table`
* For a range partition, in the `table_partition_description` of the `range_partitions` clause
* For a composite range partition, in the `table_partition_description` of the `range_partition_desc` clause
* For a composite list partition, in the `table_partition_description` of the `list_partition_desc` clause
* For a list partition, in the `table_partition_description` of the `list_partitions` clause
* For a system or reference partition, in the `table_partition_description` of the `reference_partition_desc` clause
* For the storage table of a nested table, in the `nested_table_col_properties` clause

Restrictions on Table Compression Table compression is subject to the following restrictions:

* Data segments of BasicFiles LOBs are not compressed. For information on compression of SecureFiles LOBs, see [LOB\_compression\_clause](#BABIJJHI).
* You cannot drop a column from a table that uses `COMPRESS` `BASIC`, although you can set such a column as unused. All of the operations of the `ALTER` `TABLE` ... `drop_column_clause` are valid for tables that use `ROW` `STORE` `COMPRESS` `ADVANCED`, `COLUMN` `STORE` `COMPRESS` `FOR` `QUERY`, and `COLUMN` `STORE` `COMPRESS` `FOR` `ARCHIVE`.
* You cannot specify any type of table compression for an index-organized table, any overflow segment or partition of an overflow segment, or any mapping table segment of an index-organized table.
* You cannot specify any type of table compression for external tables or for tables that are part of a cluster.
* You cannot specify any type of table compression for tables with `LONG` or `LONG` `RAW` columns, tables that are owned by the `SYS` schema and reside in the `SYSTEM` tablespace, or tables with `ROWDEPENDENCIES` enabled.
* You cannot specify Hybrid Columnar Compression on tables that are enabled for flashback archiving.
* You cannot specify Hybrid Columnar Compression on the following object-relational features: object tables, `XMLType` tables, columns with abstract data types, collections stored as tables, or OPAQUE types, including `XMLType` columns stored as objects.
* When you update a row in a table compressed with Hybrid Columnar Compression, the `ROWID` of the row may change.
* In tables compressed with Hybrid Columnar Compression, updates to a single row may result in locks on multiple rows. Concurrency for write transactions may therefore be affected.
* If a table compressed with Hybrid Columnar Compression has a foreign key constraint, and you insert data using `INSERT` with the `APPEND` hint, then the data will be compressed to a lesser level than is typical with Hybrid Columnar Compression. To compress the data with Hybrid Columnar Compression, disable the foreign key constraint, insert the data using `INSERT` with the `APPEND` hint, and then reenable the foreign key constraint.

inmemory\_table\_clause

Use this clause to enable or disable the table for the In-Memory Column Store (IM column store). The IM column store is an optional, static SGA pool that stores copies of tables and partitions in a special columnar format optimized for rapid scans. The IM column store does not replace the buffer cache, but acts as a supplement so that both memory areas can store the same data in different formats. The IM column store is available starting with Oracle Database 12c Release 1 (12.1.0.2).

* Specify `INMEMORY` to enable the table for the IM column store.

  You can optionally use the `inmemory_parameters` clause to specify how table data is stored in the IM column store. This clause enables you to specify the data compression method and the data population priority. In an Oracle RAC environment, it also enables you to specify how the data is distributed and duplicated across Oracle RAC instances. Refer to the [inmemory\_parameters](#CEGIDFIC) clause for more information.

  You can optionally use the `inmemory_column_clause` to disable specific table columns for the IM column store, and to specify the data compression method for specific columns. Refer to the [inmemory\_column\_clause](#CEGJEEBB) for more information.
* Specify `NO` `INMEMORY` to disable the table for the IM column store.

If you omit this clause, then the table is assigned the default IM column store settings for the tablespace in which it is created. Refer to the [inmemory\_clause](statements_7003.md#CEGCFHJD) of `CREATE` `TABLESPACE` for more information on specifying the default IM column store settings for a tablespace.

Note:

The

`INMEMORY_CLAUSE_DEFAULT`

initialization parameter enables you to specify a default IM column store clause for new tables and materialized views. Refer to

[Oracle Database Reference](../REFRN/GUID-5772F775-2A3E-4BC8-AA03-B8FF383BEE52.md#REFRN10350)

for more information on the

`INMEMORY_CLAUSE_DEFAULT`

initialization parameter.

Restrictions on the In-Memory Column Store The following restrictions apply to the In-Memory Column Store:

* You cannot specify the `INMEMORY` clause for tables that are owned by the `SYS` schema and reside in the `SYSTEM` or `SYSAUX` tablespace.
* The IM column store does not support `LONG` or `LONG` `RAW` columns, out-of-line columns (LOBs, varrays, nested table columns), virtual columns, or extended data type columns. If you enable a table for the IM column store and it contains any of these types of columns, then the columns will not be populated in the IM column store.

inmemory\_parameters

Use the `inmemory_memcompress`, `inmemory_priority`, `inmemory_distribute`, and `inmemory_duplicate` clauses to specify how table data is stored in the IM column store.

inmemory\_memcompress Use this clause to specify the compression method for table data stored in the IM column store. This data is called in-memory data. To instruct the database to not compress in-memory data, specify `NO` `MEMCOMPRESS`. To instruct the database to compress in-memory data, specify `MEMCOMPRESS` `FOR` followed by one of the following methods:

* `DML` - This method is optimized for DML operations and performs little or no data compression.
* `QUERY` - Specifying `QUERY` is equivalent to specifying `QUERY` `LOW`.
* `QUERY` `LOW` - This method compresses in-memory data the least (except for `DML`) and results in the best query performance. This is the default.
* `QUERY` `HIGH` -This method compress in-memory data more than `QUERY` `LOW`, but less than `CAPACITY` `LOW`.
* `CAPACITY` - Specifying `CAPACITY` is equivalent to specifying `CAPACITY` `LOW`.
* `CAPACITY` `LOW` - This method compresses in-memory data more than `QUERY` `HIGH`, but less than `CAPACITY` `HIGH`, and results in excellent query performance.
* `CAPACITY` `HIGH` - This method compresses in-memory data the most and results in good query performance.

inmemory\_priority Use the `PRIORITY` clause to specify the data population priority for table data in the IM column store. This clause controls the priority of population, but not the speed of population.

* Specify `NONE` for on-demand population. In this case, the database populates table data in the IM column store when the table it is accessed through a full table scan. If the table is never accessed, or if it is accessed only through an index scan or fetch by rowid, then population never occurs. This is the default.
* Specify one of the following priority levels for priority-based population: `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`. In this case, the database automatically populates table data in the IM column store using an internally managed priority queue; a full scan is not a necessary condition for population. The database queues population of the table data based on the specified priority level. For example, a table with the setting `INMEMORY` `PRIORITY` `CRITICAL` takes precedence over a table with the setting `INMEMORY` `PRIORITY` `HIGH`, which in turn takes precedence over a table with the setting `INMEMORY` `PRIORITY` `LOW`, and so on. If the IM column store has insufficient space, then the database does not populate additional table data until space is available.

inmemory\_distribute The `DISTRIBUTE` clause is applicable only if you are using Oracle Real Application Clusters (Oracle RAC). It controls how table data in the IM column store is distributed across Oracle RAC instances. You can specify the following options:

* `AUTO` - Oracle Database controls how data is distributed across Oracle RAC instances. Large tables are distributed across Oracle RAC instances depending on their access patterns. Smaller tables may be distributed between instances. If you specify only the `DISTRIBUTE` keyword or omit the `inmemory_distribute` clause entirely, then `AUTO` is the default.
* `BY` `ROWID` `RANGE` - Data in certain ranges of rowids is distributed to different Oracle RAC instances.
* `BY` `PARTITION` - Data in partitions is distributed to different Oracle RAC instances.
* `BY` `SUBPARTITION` - Data in subpartitions is distributed to different Oracle RAC instances.

inmemory\_duplicate The `DUPLICATE` clause is applicable only if you are using Oracle Real Application Clusters (Oracle RAC) on an engineered system. It controls how table data in the IM column store is duplicated across Oracle RAC instances. You can specify the following options:

* `DUPLICATE` - Data is duplicated on one Oracle RAC instance, resulting in the data existing on a total of two Oracle RAC instances.
* `DUPLICATE` `ALL` - Data is duplicated across all Oracle RAC instances. If you specify `DUPLICATE` `ALL`, then the database uses the `DISTRIBUTE` `AUTO` setting, regardless of whether or how you specify the `inmemory_distribute` clause.
* `NO` `DUPLICATE` - Data is not duplicated across Oracle RAC instances. This is the default.

inmemory\_column\_clause

Use this clause to disable specific table columns for the IM column store, and to specify the data compression method for specific columns. In order to specify this clause, the table must be enabled for the IM column store.

* Specify `INMEMORY` to enable the specified table columns for the IM column store.

  You can optionally use the `inmemory_memcompress` clause to specify the data compression method for specific columns. See [inmemory\_memcompress](#CEGEIIGJ). If you omit the `inmemory_memcompress` clause, then the table column uses the data compression method for the table. You cannot specify the `PRIORITY`, `DISTRIBUTE`, or `DUPLICATE` settings for a specific table column. These settings are the same for all table columns as they are for the table.
* Specify `NO` `INMEMORY` to disable the specified table columns for the IM column store.

If you omit the `inmemory_column_clause`, then all table columns use the IM column store settings for the table.

Restriction on inmemory\_column\_clause You cannot specify this clause for a `LONG` or `LONG` `RAW` column, an out-of-line column (LOB, varray, nested table column), a virtual column, or an extended data type column.

inmemory\_clause

Use this clause to enable or disable a table partition for the IM column store. In order to specify this clause, the table must be enabled for the IM column store. If you omit this clause, then the table partition uses the IM column store settings for the table.

The `inmemory_parameters` clause has the same semantics for table partitions as for tables. Refer to the [inmemory\_parameters](#CEGIDFIC) clause for full information.

ilm\_clause

Use this clause to add an Automatic Data Optimization policy to `table`.

This clause has the same semantics in `CREATE` `TABLE` and `ALTER` `TABLE`, with the following additional restriction: You can specify only the `ADD` `POLICY` clause for `CREATE` `TABLE`. Refer to the [ilm\_clause](statements_3001.md#CJADBBDI) for the full semantics of this clause.

Restrictions on Automatic Data Optimization Automatic Data Optimization is subject to the following restrictions:

* Automatic Data Optimization is not supported for tables that contain object types, index-organized tables, clustered tables, or materialized views.
* Automatic Data Optimization is not supported in multitenant container databases (CDBs).
* Row-level policies are not supported for tables that support Temporal Validity or tables that are enabled for row archiving for In-Database Archiving.

ilm\_policy\_clause

Use this clause to describe the Automatic Data Optimization policy.

This clause has the same semantics in `CREATE` `TABLE` and `ALTER` `TABLE`. Refer to [ilm\_policy\_clause](statements_3001.md#CJAJGGED) for the full semantics of this clause.

RECOVERABLE | UNRECOVERABLE

These keywords are deprecated and have been replaced with `LOGGING` and `NOLOGGING`, respectively. Although `RECOVERABLE` and `UNRECOVERABLE` are supported for backward compatibility, Oracle strongly recommends that you use the `LOGGING` and `NOLOGGING` keywords.

Restrictions on [UN]RECOVERABLE This clause is subject to the following restrictions:

* You cannot specify `RECOVERABLE` for partitioned tables or LOB storage characteristics.
* You cannot specify `UNRECOVERABLE` for partitioned or index-organized tables.
* You can specify `UNRECOVERABLE` only with `AS` `subquery`.

ORGANIZATION

The `ORGANIZATION` clause lets you specify the order in which the data rows of the table are stored.

HEAP `HEAP` indicates that the data rows of `table` are stored in no particular order. This is the default.

INDEX `INDEX` indicates that `table` is created as an index-organized table. In an index-organized table, the data rows are held in an index defined on the primary key for the table.

EXTERNAL `EXTERNAL` indicates that table is a read-only table located outside the database.

index\_org\_table\_clause

Use the `index_org_table_clause` to create an index-organized table. Oracle Database maintains the table rows, both primary key column values and nonkey column values, in an index built on the primary key. Index-organized tables are therefore best suited for primary key-based access and manipulation. An index-organized table is an alternative to:

* A noncluster table indexed on the primary key by using the `CREATE` `INDEX` statement
* A cluster table stored in an indexed cluster that has been created using the `CREATE` `CLUSTER` statement that maps the primary key for the table to the cluster key

You must specify a primary key for an index-organized table, because the primary key uniquely identifies a row. The primary key cannot be `DEFERRABLE`. Use the primary key instead of the rowid for directly accessing index-organized rows.

If an index-organized table is partitioned and contains LOB columns, then you should specify the `index_org_table_clause` first, then the `LOB_storage_clause`, and then the appropriate `table_partitioning_clauses`.

You cannot use the `TO_LOB` function to convert a `LONG` column to a LOB column in the subquery of a `CREATE` `TABLE` ... `AS` `SELECT` statement if you are creating an index-organized table. Instead, create the index-organized table without the `LONG` column, and then use the `TO_LOB` function in an `INSERT` ... `AS` `SELECT` statement.

The `ROWID` pseudocolumn of an index-organized table returns logical rowids instead of physical rowids. A column that you create with the data type `ROWID` cannot store the logical rowids of the IOT. The only data you can store in a column of type `ROWID` is rowids from heap-organized tables. If you want to store the logical rowids of an IOT, then create a column of type `UROWID` instead. A column of type `UROWID` can store both physical and logical rowids.

Restrictions on Index-Organized Tables Index-organized tables are subject to the following restrictions:

* You cannot define a virtual column for an index-organized table.
* You cannot specify the `composite_range_partitions`, `composite_list_partitions`, or `composite_hash_partitions` clauses for an index-organized table.
* If the index-organized table is a nested table or varray, then you cannot specify `table_partitioning_clauses`.

PCTTHRESHOLD integer Specify the percentage of space reserved in the index block for an index-organized table row. `PCTTHRESHOLD` must be large enough to hold the primary key. All trailing columns of a row, starting with the column that causes the specified threshold to be exceeded, are stored in the overflow segment. `PCTTHRESHOLD` must be a value from 1 to 50. If you do not specify `PCTTHRESHOLD`, then the default is 50.

Restriction on PCTTHRESHOLD You cannot specify `PCTTHRESHOLD` for individual partitions of an index-organized table.

mapping\_table\_clauses Specify `MAPPING` `TABLE` to instruct the database to create a mapping of local to physical `ROWID`s and store them in a heap-organized table. This mapping is needed in order to create a bitmap index on the index-organized table. If the index-organized table is partitioned, then the mapping table is also partitioned and its partitions have the same name and physical attributes as the base table partitions.

Oracle Database creates the mapping table or mapping table partition in the same tablespace as its parent index-organized table or partition. You cannot query, perform DML operations on, or modify the storage characteristics of the mapping table or its partitions.

prefix\_compression The `prefix_compression` clauses let you enable or disable prefix compression for index-organized tables.

* Specify `COMPRESS` to enable prefix compression, also known as key compression, for an index-organized table, which eliminates repeated occurrence of primary key column values in index-organized tables. Use `integer` to specify the prefix length, which is the number of prefix columns to compress.

  The valid range of prefix length values is from 1 to the number of primary key columns minus 1. The default prefix length is the number of primary key columns minus 1.
* Specify `NOCOMPRESS` to disable prefix compression in index-organized tables. This is the default.

Restriction on Prefix Compression of Index-organized Tables At the partition level, you can specify `COMPRESS`, but you cannot specify the prefix length with `integer`.

index\_org\_overflow\_clause  The `index_org_overflow_clause` lets you instruct the database that index-organized table data rows exceeding the specified threshold are placed in the data segment specified in this clause.

* When you create an index-organized table, Oracle Database evaluates the maximum size of each column to estimate the largest possible row. If an overflow segment is needed but you have not specified `OVERFLOW`, then the database raises an error and does not execute the `CREATE` `TABLE` statement. This checking function guarantees that subsequent DML operations on the index-organized table will not fail because an overflow segment is lacking.
* All physical attributes and storage characteristics you specify in this clause after the `OVERFLOW` keyword apply only to the overflow segment of the table. Physical attributes and storage characteristics for the index-organized table itself, default values for all its partitions, and values for individual partitions must be specified before this keyword.
* If the index-organized table contains one or more LOB columns, then the LOBs will be stored out-of-line unless you specify `OVERFLOW`, even if they would otherwise be small enough be to stored inline.
* If `table` is partitioned, then the database equipartitions the overflow data segments with the primary key index segments.

INCLUDING column\_name Specify a column at which to divide an index-organized table row into index and overflow portions. The primary key columns are always stored in the index. `column_name` can be either the last primary key column or any non primary key column. All non primary key columns that follow `column_name` are stored in the overflow data segment.

If an attempt to divide a row at `column_name` causes the size of the index portion of the row to exceed the specified or default `PCTTHRESHOLD` value, then the database breaks up the row based on the `PCTTHRESHOLD` value.

Restriction on the INCLUDING Clause You cannot specify this clause for individual partitions of an index-organized table.

external\_table\_clause

Use the `external_table_clause` to create an external table, which is a read-only table whose metadata is stored in the database but whose data in stored outside the database. Among other capabilities, external tables let you query data without first loading it into the database.

Because external tables have no data in the database, you define them with a small subset of the clauses normally available when creating tables.

* Within the `relational_properties` clause, you can specify only `column` and `datatype`.
* Within the `physical_properties_clause`, you can specify only the organization of the table (`ORGANIZATION` `EXTERNAL` `external_table_clause`).
* Within the `table_properties` clause, you can specify only the `parallel_clause`. The `parallel_clause` lets you parallelize subsequent queries on the external data and subsequent operations that populate the external table.
* You can populate the external table at create time by using the `AS` `subquery` clause.

No other clauses are permitted in the same `CREATE` `TABLE` statement.

Restrictions on External Tables External tables are subject to the following restrictions:

* An external table cannot be a temporary table.
* You cannot specify constraints on an external table.
* You cannot create an index on an external table.
* An external table cannot contain virtual columns or `INVISIBLE` columns.
* An external table cannot have object type, varray, or `LONG` columns. However, you can populate LOB columns of an external table with varray or `LONG` data from an internal database table.

TYPE  `TYPE` `access_driver_type` indicates the access driver of the external table. The access driver is the API that interprets the external data for the database. Oracle Database provides two access drivers: `ORACLE_LOADER` and `ORACLE_DATAPUMP`. If you do not specify `TYPE`, then the database uses `ORACLE_LOADER` as the default access driver. You must specify the `ORACLE_DATAPUMP` access driver if you specify the `AS` `subquery` clause to unload data from one Oracle Database and reload it into the same or a different Oracle Database.

DEFAULT DIRECTORY `DEFAULT` `DIRECTORY` lets you specify a default directory object corresponding to a directory on the file system where the external data sources may reside. The default directory can also be used by the access driver to store auxiliary files such as error logs.

ACCESS PARAMETERS The optional `ACCESS` `PARAMETERS` clause lets you assign values to the parameters of the specific access driver for this external table.

* The `opaque_format_spec` specifies all access parameters for the `ORACLE_LOADER` and `ORACLE_DATAPUMP` access drivers. See [Oracle Database Utilities](../SUTIL/GUID-07D30CE6-128D-426F-8B76-B13E1C53BD5A.md#SUTIL1358) for descriptions of these parameters.

  Field names specified in the `opaque_format_spec` must match columns in the table definition. Oracle Database ignores any field in the `opaque_format_spec` that is not matched by a column in the table definition.
* `USING` `CLOB` `subquery` lets you derive the parameters and their values through a subquery. The subquery cannot contain any set operators or an `ORDER` `BY` clause. It must return one row containing a single item of data type `CLOB`.

Whether you specify the parameters in an `opaque_format_spec` or derive them using a subquery, the database does not interpret anything in this clause. It is up to the access driver to interpret this information in the context of the external data.

LOCATION The `LOCATION` clause lets you specify one or more external data sources. Usually the `location_specifier` is a file, but it need not be. Oracle Database does not interpret this clause. It is up to the access driver to interpret this information in the context of the external data.

REJECT LIMIT The `REJECT` `LIMIT` clause lets you specify how many conversion errors can occur during a query of the external data before an Oracle Database error is returned and the query is aborted. The default value is 0.

CLUSTER Clause

The `CLUSTER` clause indicates that the table is to be part of `cluster`. The columns listed in this clause are the table columns that correspond to the cluster columns. Generally, the cluster columns of a table are the column or columns that make up its primary key or a portion of its primary key. Refer to [CREATE CLUSTER](statements_5002.md#BABDBDEE) for more information.

Specify one column from the table for each column in the cluster key. The columns are matched by position, not by name.

A cluster table uses the space allocation of the cluster. Therefore, do not use the `PCTFREE`, `PCTUSED`, or `INITRANS` parameters, the `TABLESPACE` clause, or the `storage_clause` with the `CLUSTER` clause.

Restrictions on Cluster Tables Cluster tables are subject to the following restrictions:

* Object tables and tables containing LOB columns or columns of the `Any*` Oracle-supplied types cannot be part of a cluster.
* You cannot specify the `parallel_clause` or `CACHE` or `NOCACHE` for a table that is part of a cluster.
* You cannot specify `CLUSTER` with either `ROWDEPENDENCIES` or `NOROWDEPENDENCIES` unless the cluster has been created with the same `ROWDEPENDENCIES` or `NOROWDEPENDENCIES` setting.
* A cluster table cannot contain `INVISIBLE` columns.

table\_properties

The `table_properties` further define the characteristics of the table.

column\_properties

Use the `column_properties` clauses to specify the storage attributes of a column.

object\_type\_col\_properties

The `object_type_col_properties` determine storage characteristics of an object column or attribute or of an element of a collection column or attribute.

column For `column`, specify an object column or attribute.

substitutable\_column\_clause The `substitutable_column_clause` indicates whether object columns or attributes in the same hierarchy are substitutable for each other. You can specify that a column is of a particular type, or whether it can contain instances of its subtypes, or both.

* If you specify `ELEMENT`, then you constrain the element type of a collection column or attribute to a subtype of its declared type.
* The `IS` `OF` `[TYPE]` `(ONLY` `type``)` clause constrains the type of the object column to a subtype of its declared type.
* `NOT` `SUBSTITUTABLE` `AT` `ALL` `LEVELS` indicates that the object column cannot hold instances corresponding to any of its subtypes. Also, substitution is disabled for any embedded object attributes and elements of embedded nested tables and varrays. The default is `SUBSTITUTABLE` `AT` `ALL` `LEVELS`.

Restrictions on the substitutable\_column\_clause This clause is subject to the following restrictions:

* You cannot specify this clause for an attribute of an object column. However, you can specify this clause for a object type column of a relational table and for an object column of an object table if the substitutability of the object table itself has not been set.
* For a collection type column, the only part of this clause you can specify is `[NOT]` `SUBSTITUTABLE` `AT` `ALL` `LEVELS`.

LOB\_storage\_clause

The `LOB_storage_clause` lets you specify the storage attributes of LOB data segments. You must specify at least one clause after the `STORE` `AS` keywords. If you specify more than one clause, then you must specify them in the order shown in the syntax diagram, from top to bottom.

For a nonpartitioned table, this clause specifies the storage attributes of LOB data segments of the table.

For a partitioned table, Oracle Database implements this clause depending on where it is specified:

* For a partitioned table specified at the table level—when specified in the `physical_properties` clause along with one of the partitioning clauses—this clause specifies the default storage attributes for LOB data segments associated with each partition or subpartition. These storage attributes apply to all partitions or subpartitions unless overridden by a `LOB_storage_clause` at the partition or subpartition level.
* For an individual partition of a partitioned table—when specified as part of a `table_partition_description`—this clause specifies the storage attributes of the data segments of the partition or the default storage attributes of any subpartitions of the partition. A partition-level `LOB_storage_clause` overrides a table-level `LOB_storage_clause`.
* For an individual subpartition of a partitioned table—when specified as part of `subpartition_by_hash` or `subpartition_by_list`—this clause specifies the storage attributes of the data segments of the subpartition. A subpartition-level `LOB_storage_clause` overrides both partition-level and table-level `LOB_storage_clauses`.

Restriction on the LOB\_storage\_clause: Only the `TABLESPACE` clause is allowed when specifying the `LOB_storage_clause` in a subpartition.

LOB\_item

Specify the LOB column name or LOB object attribute for which you are explicitly defining tablespace and storage characteristics that are different from those of the table. Oracle Database automatically creates a system-managed index for each `LOB_item` you create.

SECUREFILE | BASICFILE

Use this clause to specify the type of LOB storage, either high-performance LOB (SecureFiles), or the traditional LOB (BasicFiles).

Note:

You cannot convert a LOB from one type of storage to the other. Instead you must migrate to SecureFiles or BasicFiles by using online redefinition or partition exchange.

LOB\_segname

Specify the name of the LOB data segment. You cannot use `LOB_segname` if you specify more than one `LOB_item`.

LOB\_storage\_parameters

The `LOB_storage_parameters` clause lets you specify various elements of LOB storage.

TABLESPACE Clause  Use this clause to specify the tablespace in which LOB data is to be stored.

storage\_clause  Use the `storage_clause` to specify various aspects of LOB segment storage. Of particular interest in the context of LOB storage is the `MAXSIZE` clause of the `storage_clause`, which can be used in combination with the `LOB_retention_clause` of `LOB_parameters`. Refer to [storage\_clause](clauses009.md#i997450) for more information.

LOB\_parameters

Several of the `LOB_parameters` are no longer needed if you are using SecureFiles for LOB storage. The `PCTVERSION` and `FREEPOOLS` parameters are valid and useful only if you are using BasicFiles LOB storage.

ENABLE STORAGE IN ROW  If you enable storage in row, then the LOB value is stored in the row (inline) if its length is less than approximately 4000 bytes minus system control information. This is the default.

Restriction on Enabling Storage in Row For an index-organized table, you cannot specify this parameter unless you have specified an `OVERFLOW` segment in the `index_org_table_clause`.

DISABLE STORAGE IN ROW  If you disable storage in row, then the LOB value is stored outside of the row out of line regardless of the length of the LOB value.

The LOB locator is always stored inline regardless of where the LOB value is stored. You cannot change the value of `STORAGE` `IN` `ROW` once it is set except by moving the table. See the [move\_table\_clause](statements_3001.md#i2085301) in the `ALTER` `TABLE` documentation for more information.

CHUNK integer  Specify the number of bytes to be allocated for LOB manipulation. If `integer` is not a multiple of the database block size, then the database rounds up in bytes to the next multiple. For example, if the database block size is 2048 and `integer` is 2050, then the database allocates 4096 bytes (2 blocks). The maximum value is 32768 (32K), which is the largest Oracle Database block size allowed. The default `CHUNK` size is one Oracle Database block.

The value of `CHUNK` must be less than or equal to the value of `NEXT`, either the default value or that specified in the `storage_clause`. If `CHUNK` exceeds the value of `NEXT`, then the database returns an error. You cannot change the value of `CHUNK` once it is set.

PCTVERSION integer  

Specify the maximum percentage of overall LOB storage space used for maintaining old versions of the LOB. If the database is running in manual undo mode, then the default value is 10, meaning that older versions of the LOB data are not overwritten until they consume 10% of the overall LOB storage space.

You can specify the `PCTVERSION` parameter whether the database is running in manual or automatic undo mode. `PCTVERSION` is the default in manual undo mode. `RETENTION` is the default in automatic undo mode. You cannot specify both `PCTVERSION` and `RETENTION`.

This clause is not valid if you have specified `SECUREFILE`. If you specify both `SECUREFILE` and `PCTVERSION`, then the database silently ignores the `PCTVERSION` parameter.

LOB\_retention\_clause  Use this clause to specify whether you want the LOB segment retained for flashback purposes, consistent-read purposes, both, or neither.

You can specify the `RETENTION` parameter only if the database is running in automatic undo mode. Oracle Database uses the value of the `UNDO_RETENTION` initialization parameter to determine the amount of committed undo data to retain in the database. In automatic undo mode, `RETENTION` is the default value unless you specify `PCTVERSION`. You cannot specify both `PCTVERSION` and `RETENTION`.

You can specify the optional settings after `RETENTION` only if you are using SecureFiles. The `SECUREFILE` parameter of the `LOB_storage_clause` indicates that the database will use SecureFiles to manage storage dynamically, taking into account factors such as the undo mode of the database.

* Specify `MAX` to signify that the undo should be retained until the LOB segment has reached `MAXSIZE`. If you specify `MAX`, then you must also specify the `MAXSIZE` clause in the `storage_clause`.
* Specify `MIN` if the database is in flashback mode to limit the undo retention duration for the specific LOB segment to `n` seconds.
* Specify `AUTO` if you want to retain undo sufficient for consistent read purposes only.
* Specify `NONE` if no undo is required for either consistent read or flashback purposes.

If you do not specify the `RETENTION` parameter, or you specify `RETENTION` with no optional settings, then `RETENTION` is set to `DEFAULT`, which is functionally equivalent to `AUTO`.

FREEPOOLS integer  Specify the number of groups of free lists for the LOB segment. Normally `integer` will be the number of instances in an Oracle Real Application Clusters environment or 1 for a single-instance database.

You can specify this parameter only if the database is running in automatic undo mode. In this mode, `FREEPOOLS` is the default unless you specify the `FREELIST` `GROUPS` parameter of the `storage_clause`. If you specify neither `FREEPOOLS` nor `FREELIST` `GROUPS`, then the database uses a default of `FREEPOOLS` `1` if the database is in automatic undo management mode and a default of `FREELIST` `GROUPS` `1` if the database is in manual undo management mode.

This clause is not valid if you have specified `SECUREFILE`. If you specify both `SECUREFILE` and `FREEPOOLS`, then the database silently ignores the `FREEPOOLS` parameter.

Restriction on FREEPOOLS You cannot specify both `FREEPOOLS` and the `FREELIST` `GROUPS` parameter of the `storage_clause`.

LOB\_deduplicate\_clause  This clause is valid only for SecureFiles LOBs. Use the `LOB_deduplicate_clause` to enable or disable LOB deduplication, which is the elimination of duplicate LOB data.

The `DEDUPLICATE` keyword instructs the database to eliminate duplicate copies of LOBs. Using a secure hash index to detect duplication, the database coalesces LOBs with identical content into a single copy, reducing storage consumption and simplifying storage management.

If you omit this clause, then LOB deduplication is disabled by default.

This clause implements LOB deduplication for the entire LOB segment. To enable or disable deduplication for an individual LOB, use the `DBMS_LOB.SETOPTIONS` procedure.

LOB\_compression\_clause  This clause is valid only for SecureFiles LOBs, not for BasicFiles LOBs. Use the `LOB_compression_clause` to instruct the database to enable or disable server-side LOB compression. Random read/write access is possible on server-side compressed LOB segments. LOB compression is independent from table compression or index compression. If you omit this clause, then the default is `NOCOMPRESS`.

You can specify `HIGH`, `MEDIUM`, or `LOW` to vary the degree of compression. The `HIGH` degree of compression incurs higher latency than `MEDIUM` but provides better compression. The `LOW` degree results in significantly higher decompression and compression speeds, at the cost of slightly lower compression ratio than either `HIGH` or `MEDIUM`. If you omit this optional parameter, then the default is `MEDIUM`.

This clause implements server-side LOB compression for the entire LOB segment. To enable or disable compression on an individual LOB, use the `DBMS_LOB.SETOPTIONS` procedure.

ENCRYPT | DECRYPT  These clauses are valid only for LOBs that are using SecureFiles for LOB storage. Specify `ENCRYPT` to encrypt all LOBs in the column. Specify `DECRYPT` to keep the LOB in cleartext. If you omit this clause, then `DECRYPT` is the default.

Refer to [encryption\_spec](#CEGDFHBD) for general information on that clause. When applied to a LOB column, `encryption_spec` is specific to the individual LOB column, so the encryption algorithm can differ from that of other LOB columns and other non-LOB columns. Use the `encryption_spec` as part of the `column_definition` to encrypt the entire LOB column. Use the `encryption_spec` as part of the `LOB_storage_clause` in the `table_partition_description` to encrypt a LOB partition.

Restriction on encryption\_spec for LOBs You cannot specify the `SALT` or `NO` `SALT` clauses of `encryption_spec` for LOB encryption.

CACHE | NOCACHE | CACHE READS  Refer to [CACHE | NOCACHE | CACHE READS](#i2215507) for information on these clauses.

LOB\_partition\_storage

The `LOB_partition_storage` clause lets you specify a separate `LOB_storage_clause` or `varray_col_properties` clause for each partition. You must specify the partitions in the order of partition position. You can find the order of the partitions by querying the `PARTITION_NAME` and `PARTITION_POSITION` columns of the `USER_IND_PARTITIONS` view.

If you do not specify a `LOB_storage_clause` or `varray_col_properties` clause for a particular partition, then the storage characteristics are those specified for the LOB item at the table level. If you also did not specify any storage characteristics for the LOB item at the table level, then Oracle Database stores the LOB data partition in the same tablespace as the table partition to which it corresponds.

Restrictions on LOB\_partition\_storage: `LOB_partition_storage` is subject to the following restrictions:

* In the `LOB_parameters` of the `LOB_storage_clause`, you cannot specify `encryption_spec`, because it is invalid to specify an encryption algorithm for partitions and subpartitions.
* You can only specify the `TABLESPACE` clause for hash partitions and all types of subpartitions.

varray\_col\_properties

The `varray_col_properties` let you specify separate storage characteristics for the LOB in which a varray will be stored. If `varray_item` is a multilevel collection, then the database stores all collection items nested within `varray_item` in the same LOB in which `varray_item` is stored.

* For a nonpartitioned table—when specified in the `physical_properties` clause without any of the partitioning clauses—this clause specifies the storage attributes of the LOB data segments of the varray.
* For a partitioned table specified at the table level—when specified in the `physical_properties` clause along with one of the partitioning clauses—this clause specifies the default storage attributes for the varray LOB data segments associated with each partition (or its subpartitions, if any).
* For an individual partition of a partitioned table—when specified as part of a `table_partition_description`—this clause specifies the storage attributes of the varray LOB data segments of that partition or the default storage attributes of the varray LOB data segments of any subpartitions of this partition. A partition-level `varray_col_properties` overrides a table-level `varray_col_properties`.
* For an individual subpartition of a partitioned table—when specified as part of `subpartition_by_hash` or `subpartition_by_list`—this clause specifies the storage attributes of the varray data segments of this subpartition. A subpartition-level `varray_col_properties` overrides both partition-level and table-level `varray_col_properties`.

STORE AS [SECUREFILE | BASICFILE] LOB Clause If you specify `STORE` `AS` `LOB`, then:

* If the maximum varray size is less than approximately 4000 bytes, then the database stores the varray as an inline LOB unless you have disabled storage in row.
* If the maximum varray size is greater than approximately 4000 bytes or if you have disabled storage in row, then the database stores in the varray as an out-of-line LOB.

If you do not specify `STORE` `AS` `LOB`, then storage is based on the maximum possible size of the varray rather than on the actual size of a varray column. The maximum size of the varray is the number of elements times the element size, plus a small amount for system control information. If you omit this clause, then:

* If the maximum size of the varray is less than approximately 4000 bytes, then the database does not store the varray as a LOB, but as inline data.
* If the maximum size is greater than approximately 4000 bytes, then the database always stores the varray as a LOB.

  + If the actual size is less than approximately 4000 bytes, then it is stored as an inline LOB
  + If the actual size is greater than approximately 4000 bytes, then it is stored as an out-of-line LOB, as is true for other LOB columns.

substitutable\_column\_clause The `substitutable_column_clause` has the same behavior as described for [object\_type\_col\_properties](#i2128922).

Restriction on Varray Column Properties  You cannot specify this clause on an interval partitioned table.

nested\_table\_col\_properties

The `nested_table_col_properties` let you specify separate storage characteristics for a nested table, which in turn enables you to define the nested table as an index-organized table. Unless you explicitly specify otherwise in this clause:

* For a nonpartitioned table, the storage table is created in the same schema and the same tablespace as the parent table.
* For a partitioned table, the storage table is created in the default tablespace of the schema. By default, nested tables are equipartitioned with the partitioned base table.
* In either case, the storage table uses default storage characteristics, and stores the nested table values of the column for which it was created.

You must include this clause when creating a table with columns or column attributes whose type is a nested table. Clauses within `nested_table_col_properties` that function the same way they function for the parent table are not repeated here.

nested\_item Specify the name of a column, or of a top-level attribute of the object type of the tables, whose type is a nested table.

COLUMN\_VALUE If the nested table is a multilevel collection, then the inner nested table or varray may not have a name. In this case, specify `COLUMN_VALUE` in place of the `nested_item` name.

LOCAL | GLOBAL Specify `LOCAL` to equipartition the nested table with the base table. This is the default. Oracle Database automatically creates a local partitioned index for the partitioned nested table.

Specify `GLOBAL` to indicate that the nested table is a nonpartitioned nested table of a partitioned base table.

storage\_table Specify the name of the table where the rows of `nested_item` reside.

You cannot query or perform DML statements on `storage_table` directly, but you can modify its storage characteristics by specifying its name in an `ALTER` `TABLE` statement.

See Also:

[ALTER TABLE](statements_3001.md#CJAHHIBI)

for information about modifying nested table column storage characteristics

RETURN [AS] Specify what Oracle Database returns as the result of a query.

* `VALUE` returns a copy of the nested table itself.
* `LOCATOR` returns a collection locator to the copy of the nested table.

  The locator is scoped to the session and cannot be used across sessions. Unlike a LOB locator, the collection locator cannot be used to modify the collection instance.

If you do not specify the `segment_attributes_clause` or the `LOB_storage_clause`, then the nested table is heap organized and is created with default storage characteristics.

Restrictions on Nested Table Column Properties Nested table column properties are subject to the following restrictions:

* You cannot specify this clause for a temporary table.
* You cannot specify this clause on an interval partitioned table.
* You cannot specify the `oid_clause`.
* At create time, you cannot use `object_properties` to specify an `out_of_line_ref_constraint`, `inline_ref_constraint`, or foreign key constraint for the attributes of a nested table. However, you can modify a nested table to add such constraints using `ALTER` `TABLE`.

XMLType\_column\_properties

The `XMLType_column_properties` let you specify storage attributes for an `XMLTYPE` column.

XMLType\_storage `XMLType` data can be stored in binary XML, `CLOB`, or object-relational columns.

* Specify `BINARY` `XML` to store the XML data in compact binary XML format.

  Any LOB parameters you specify are applied to the underlying `BLOB` column created for storing the binary XML encoded value.

  In earlier releases, binary XML data is stored by default in a BasicFiles LOB. Beginning with Oracle Database 11g Release 2 (11.2.0.2), if the `COMPATIBLE` initialization parameter is 11.2 or higher and you do not specify `BASICFILE` or `SECUREFILE`, then binary XML data is stored in a SecureFiles LOB whenever possible. If SecureFiles LOB storage is not possible then the binary XML data is stored in a BasicFiles LOB. This can occur if either of the following is true:

  + The tablespace for the `XMLType` table does not use automatic segment space management.
  + A setting in file `init`.`ora` prevents SecureFiles LOB storage. For example, see parameter `DB_SECUREFILE` in [Oracle Database Reference](../REFRN/GUID-6F7C5E21-3929-4AB1-9C72-1BB9BDDB011F.md#REFRN10290).
* Specify `CLOB` if you want the database to store the `XMLType` data in a `CLOB` column. Storing data in a `CLOB` column preserves the original content and enhances retrieval time.

  If you specify LOB storage, then you can specify either LOB parameters or the `XMLSchema_spec` clause, but not both. Specify the `XMLSchema_spec` clause if you want to restrict the table or column to particular schema-based XML instances.

  If you do not specify `BASICFILE` or `SECUREFILE` with this clause, then the `CLOB` column is stored in a BasicFiles LOB.

  Note:

  Oracle recommends against storing

  `XMLType`

  data in a

  `CLOB`

  column.

  `CLOB`

  storage of

  `XMLType`

  is deprecated. Use binary XML storage of

  `XMLType`

  instead.
* Specify `OBJECT` `RELATIONAL` if you want the database to store the `XMLType` data in object-relational columns. Storing data objects relationally lets you define indexes on the relational columns and enhances query performance.

  If you specify object-relational storage, then you must also specify the `XMLSchema_spec` clause.

Use the `ALL` `VARRAYS` `AS` clause if you want the database to store all varrays in an `XMLType` column.

In earlier releases, `XMLType` data is stored in a `CLOB` column in a BasicFiles LOB by default. Beginning with Oracle Database 11g Release 2 (11.2.0.2), if the `COMPATIBLE` initialization parameter is 11.2 or higher and you do not specify the `XMLType_storage` clause, then `XMLType` data is stored in a binary XML column in a SecureFiles LOB. If SecureFiles LOB storage is not possible, then it is stored in a binary XML column in a BasicFiles LOB.

XMLSchema\_spec  

Refer to the [XMLSchema\_spec](#i2215293) for the full semantics of this clause.

XMLType\_virtual\_columns

This clause is valid only for `XMLType` tables with binary XML storage, which you designate in the `XMLType_storage` clause. Specify the `VIRTUAL` `COLUMNS` clause to define virtual columns, which can be used as in a function-based index or in the definition of a constraint. You cannot define a constraint on such a virtual column during creation of the table, but you can use a subsequent `ALTER` `TABLE` statement to add a constraint to the column.

indexing\_clause

The `indexing_clause` is valid only for partitioned tables. Use this clause to set the indexing property for a table, table partition, or table subpartition.

The indexing property determines whether table partitions and subpartitions are included in partial indexes on the table.

* For simple partitioned tables, partitions with an indexing property of `ON` are included in partial indexes on the table. Partitions with an indexing property of `OFF` are excluded.
* For composite-partitioned tables, subpartitions with an indexing property of `ON` are included in partial indexes on the table. Subpartitions with an indexing property of `OFF` are excluded.

You can specify the `indexing_clause` at the table, partition, or subpartition level. When you specify the `indexing_clause` at the table level, in the `table_properties` clause, you set the default indexing property for the table. Interval partitions, which are automatically created by the database, always inherit the default indexing property for the table. Other types of partitions and subpartitions inherit the default indexing property as follows:

* For simple partitioned tables, partitions inherit the default indexing property for the table. You can override this behavior by specifying the `indexing_clause` for an individual partition:

  + For a range partition, in the `table_partition_description` of the `range_partitions` clause
  + For a hash partition, in the `individual_hash_partitions` clause of the `hash_partitions` clause
  + For a list partition, in the `table_partition_description` of the `list_partitions` clause
  + For a reference partition, in the `table_partition_description` of the `reference_partition_desc` clause of the `reference_partitioning` clause
  + For a system partition, in the `table_partition_description` of the `reference_partition_desc` clause of the `system_partitioning` clause
* For composite-partitioned tables, subpartitions inherit the default indexing property for the table. You can override this behavior by specifying the `indexing_clause` for an individual partition or subpartition.

  If you specify the `indexing_clause` for a partition, then its subpartitions inherit the indexing property of the partition:

  + For composite range partitions, in the `table_partition_description` of the `composite_range_partitions` clause
  + For composite list partitions, in the `table_partition_description` of the `composite_list_partitions` clause
  + For composite hash partitions, in the `individual_hash_partitions` clause of the `composite_hash_partitions` clause

  You can set the indexing property of a subpartition by specifying the `indexing_clause` for the subpartition:

  + For range subpartitions, in the `range_subpartition_desc` clause of the `composite_range_partitions` clause
  + For list subpartitions, in the `list_subpartition_desc` clause of the `composite_list_partitions` clause
  + For hash subpartitions, in the `individual_hash_subparts` clause of the `composite_hash_partitions` clause

See Also:

[Oracle Database Reference](../REFRN/toc.md)

for information on viewing the indexing property of a table, table partition, or table subpartition.

* To view the default indexing property of a table, query the `DEF_INDEXING` column of the `*_PART_TABLES` views.
* To view the indexing property of a table partition, query the `INDEXING` column of the `*_TAB_PARTITIONS` views.
* To view the indexing property of a table subpartition, query the `INDEXING` column of the `*_TAB_SUBPARTITIONS` views.

Restrictions on the indexing\_clause The `indexing_clause` is subject to the following restrictions:

table\_partitioning\_clauses

Use the `table_partitioning_clauses` to create a partitioned table.

Notes on Partitioning in General The following notes pertain to all types of partitioning:

* You can specify up to a total of 1024K-1 partitions and subpartitions.
* You can create a partitioned table with just one partition. A table with one partition is different from a nonpartitioned table. For example, you cannot add a partition to a nonpartitioned table.
* You can specify a name for every table and LOB partition and for every table and LOB subpartition, but you need not do so. If you omit the name, then the database generates names as follows:

  + If you omit a partition name, then the database generates a name of the form `SYS_P``n`. System-generated names for LOB data and LOB index partitions take the form `SYS_LOB_P``n` and `SYS_IL_P``n`, respectively.
  + If you specify a subpartition name in `subpartition_template`, then for each subpartition created with that template, the database generates a name by concatenating the partition name with the template subpartition name. For LOB subpartitions, the generated LOB subpartition name is a concatenation of the partition name and the template LOB segment name. In either case, if the concatenation exceeds 30 characters, then the database returns an error and the statement fails.
  + If you omit a subpartition name when specifying an individual subpartition, and you have not specified `subpartition_template`, then the database generates a name of the form `SYS_SUBP``n`. The corresponding system-generated names for LOB data and index subpartitions are `SYS_LOB_SUBP``n` and `SYS_IL_SUBP``n`, respectively.
* Tablespace storage can be specified at various levels in the `CREATE` `TABLE` statement for both table segments and LOB segments. The number of tablespaces does not have to equal the number of partitions or subpartitions. If the number of partitions or subpartitions is greater than the number of tablespaces, then the database cycles through the names of the tablespaces.

  The database evaluates tablespace storage in the following order of descending priority:

  + Tablespace storage specified at the individual table subpartition or LOB subpartition level has the highest priority, followed by storage specified for the partition or LOB in the `subpartition_template`.
  + Tablespace storage specified at the individual table partition or LOB partition level. Storage parameters specified here take precedence over the `subpartition_template`.
  + Tablespace storage specified for the table
  + Default tablespace storage specified for the user
* By default, nested tables are equipartitioned with the partitioned base table.

Restrictions on Partitioning in General All partitioning is subject to the following restrictions:

* You cannot partition a table that is part of a cluster.
* You cannot partition a nested table or varray that is defined as an index-organized table.
* You cannot partition a table containing any `LONG` or `LONG` `RAW` columns.

The storage of partitioned database entities in tablespaces of different block sizes is subject to several restrictions. Refer to [Oracle Database VLDB and Partitioning Guide](../VLDBG/GUID-24050391-B7C5-4AE2-86D4-B5438412C3F6.md#VLDBG00306) for a discussion of these restrictions.

range\_partitions

Use the `range_partitions` clause to partition the table on ranges of values from the column list. For an index-organized table, the column list must be a subset of the primary key columns of the table.

column

Specify an ordered list of columns used to determine into which partition a row belongs. These columns are the partitioning key. You can specify virtual columns and `INVISIBLE` columns as partitioning key columns.

INTERVAL Clause

Use this clause to establish interval partitioning for the table. Interval partitions are partitions based on a numeric range or datetime interval. They extend range partitioning by instructing the database to create partitions of the specified range or interval automatically when data inserted into the table exceeds all of the range partitions. For each automatically created partition, the database generates a name of the form `SYS_P``n`. The database guarantees that automatically generated partition names are unique and do not violate namespace rules.

* For `expr`, specify a valid number or interval expression.
* The optional `STORE` `IN` clause lets you specify one or more tablespaces into which the database will store interval partition data.
* You must also specify at least one range partition using the `PARTITION` clause of `range_partitions`. The range partition key value determines the high value of the range partitions, which is called the transition point, and the database creates interval partitions for data beyond that transition point.

Restrictions on Interval Partitioning The `INTERVAL` clause is subject to the restrictions listed in ["Restrictions on Partitioning in General"](#BABIICCD) and ["Restrictions on Range Partitioning"](#CJAEBCJE). The following additional restrictions apply:

* You can specify only one partitioning key column, and it must be of type `NUMBER`, `DATE`, `FLOAT`, or `TIMESTAMP`.
* This clause is not supported for index-organized tables.
* This clause is not supported for tables containing nested table columns, varray columns, or `XMLType` columns.
* Interval partitioning is not supported at the subpartition level.
* Serializable transactions do not work with interval partitioning. Trying to insert data into a partition of an interval partitioned table that does not yet have a segment causes an error.
* In the `VALUES` clause:

  + You cannot specify `MAXVALUE` (an infinite upper bound), because doing so would defeat the purpose of the automatic addition of partitions as needed.
  + You cannot specify `NULL` values for the partitioning key column.

PARTITION partition

If you specify a partition name, then the name `partition` must conform to the rules for naming schema objects and their part as described in ["Database Object Naming Rules"](sql_elements008.md#i27570). If you omit `partition`, then the database generates a name as described in ["Notes on Partitioning in General"](#CHDFAGGH).

range\_values\_clause

Specify the noninclusive upper bound for the current partition. The value list is an ordered list of literal values corresponding to the column list in the `range_partitions` clause. You can substitute the keyword `MAXVALUE` for any literal in the value list. `MAXVALUE` specifies a maximum value that will always sort higher than any other value, including null.

Specifying a value other than `MAXVALUE` for the highest partition bound imposes an implicit integrity constraint on the table.

Note:

If

`table`

is partitioned on a

`DATE`

column, and if the date format does not specify the first two digits of the year, then you must use the

`TO_DATE`

function with the

`YYYY`

4-character format mask for the year. The

`RRRR`

format mask is not supported in this clause. The date format is determined implicitly by

`NLS_TERRITORY`

or explicitly by

`NLS_DATE_FORMAT`

. Refer to

[Oracle Database Globalization Support Guide](../NLSPG/ch3globenv.md#NLSPG003)

for more information on these initialization parameters.

table\_partition\_description

Use the `table_partition_description` to define the physical and storage characteristics of the table.

The clauses `deferred_segment_creation`, `segment_attributes_clause`, `table_compression`, `inmemory_clause`, and `ilm_clause` have the same function as described for the [physical\_properties](#i2128663) of the table as a whole.

Use the `indexing_clause` to set the indexing property for a range, list, system, or reference table partition. Refer to the [indexing\_clause](#CJAFJABE) for more information.

The `prefix_compression` clause and `OVERFLOW` clause, have the same function as described for the [index\_org\_table\_clause](#i2128766) .

LOB\_storage\_clause The `LOB_storage_clause` lets you specify LOB storage characteristics for one or more LOB items in this partition or in any range or list subpartitions of this partition. If you do not specify the `LOB_storage_clause` for a LOB item, then the database generates a name for each LOB data partition as described in ["Notes on Partitioning in General"](#CHDFAGGH).

varray\_col\_properties The `varray_col_properties` let you specify storage characteristics for one or more varray items in this partition or in any range or list subpartitions of this partition.

nested\_table\_col\_properties The `nested_table_col_properties` let you specify storage characteristics for one or more nested table storage table items in this partition or in any range or list subpartitions of this partition. Storage characteristics specified in this clause override any storage attributes specified at the table level.

partitioning\_storage\_clause

Use the `partitioning_storage_clause` to specify storage characteristics for hash partitions and for range, hash, and list subpartitions.

Restrictions on partitioning\_storage\_clause This clause is subject to the following restrictions:

* The `OVERFLOW` clause is relevant only for index-organized partitioned tables and is valid only within the `individual_hash_partitions` clause. It is not valid for range or hash partitions or for subpartitions of any type.
* You cannot specify the `advanced_index_compression` clause of the `index_compression` clause.
* You can specify the `prefix_compression` clause of the `indexing_clause` only for partitions of index-organized tables and you can specify `COMPRESS` or `NOCOMPRESS`, but you cannot specify the prefix length with `integer`.

Restrictions on Range Partitioning Range partitioning is subject to the restrictions listed in ["Restrictions on Partitioning in General"](#BABIICCD). The following additional restrictions apply:

* You cannot specify more than 16 partitioning key columns.
* Partitioning key columns must be of type `CHAR`, `NCHAR`, `VARCHAR2`, `NVARCHAR2`, `VARCHAR`, `NUMBER`, `FLOAT`, `DATE`, `TIMESTAMP`, `TIMESTAMP` `WITH` `LOCAL` `TIMEZONE`, or `RAW`.
* You cannot specify NULL in the `VALUES` clause.

list\_partitions

Use the `list_partitions` clause to partition the table on lists of literal values from `column`. List partitioning is useful for controlling how individual rows map to specific partitions.

list\_values\_clause The `list_values_clause` of each partition must have at least one value. No value, including `NULL`, can appear in more than one partition. List partitions are not ordered.

If you specify the literal `NULL` for a partition value in the `VALUES` clause, then to access data in that partition in subsequent queries, you must use an `IS` `NULL` condition in the `WHERE` clause, rather than a comparison condition.

The `DEFAULT` keyword creates a partition into which the database will insert any row that does not map to another partition. Therefore, you can specify `DEFAULT` for only one partition, and you cannot specify any other values for that partition. Further, the default partition must be the last partition you define. The use of `DEFAULT` is similar to the use of `MAXVALUE` for range partitions.

The string comprising the list of values for each partition can be up to 4K bytes. The total number of values for all partitions cannot exceed 64K-1.

The partitioning key column for a list partition can be an extended data type column, which has a maximum size of 32767 bytes. In this case, the list of values that you want to specify for a partition may exceed the 4K byte limit. You can work around this limitation by using one of the following methods:

* Use the `DEFAULT` partition for values that exceed the 4K byte limit.
* Use a hash function, such as `STANDARD_HASH`, in the partition key column to create unique identifiers of lengths less than 4K bytes. See [STANDARD\_HASH](functions183.md#BABCCAFF) for more information.

table\_partition\_description  The subclauses of the `table_partition_description` have the same behavior as described for range partitions in [table\_partition\_description](#BABHFEGC).

Restrictions on List Partitioning List partitioning is subject to the restrictions listed in ["Restrictions on Partitioning in General"](#BABIICCD). The following additional restrictions apply:

* You can specify only one partitioning key column.
* The partitioning key column must be of type `CHAR`, `NCHAR`, `VARCHAR2`, `NVARCHAR2`, `VARCHAR`, `NUMBER`, `FLOAT`, `DATE`, `TIMESTAMP`, `TIMESTAMP` `WITH` `LOCAL` `TIMEZONE`, or `RAW`.

hash\_partitions

Use the `hash_partitions` clause to specify that the table is to be partitioned using the hash method. Oracle Database assigns rows to partitions using a hash function on values found in columns designated as the partitioning key. You can specify individual hash partitions, or you can specify how many hash partitions the database should create.

column Specify an ordered list of columns used to determine into which partition a row belongs (the partitioning key).

individual\_hash\_partitions  Use this clause to specify individual partitions by name.

Use the `indexing_clause` to set the indexing property for a hash partition. Refer to the [indexing\_clause](#CJAFJABE) for more information.

Restriction on Specifying Individual Hash Partitions The only clauses you can specify in the `partitioning_storage_clause` are the `TABLESPACE` clause and table compression.

Note:

If your enterprise has or will have databases using different character sets, then use caution when partitioning on character columns. The sort sequence of characters is not identical in all character sets. Refer to

[Oracle Database Globalization Support Guide](../NLSPG/applocaledata.md#NLSPG014)

for more information on character set support.

hash\_partitions\_by\_quantity An alternative to defining individual partitions is to specify the number of hash partitions. In this case, the database assigns partition names of the form `SYS_P``n`. The `STORE` `IN` clause lets you specify one or more tablespaces where the hash partition data is to be stored. The number of tablespaces need not equal the number of partitions. If the number of partitions is greater than the number of tablespaces, then the database cycles through the names of the tablespaces.

For both methods of hash partitioning, for optimal load balancing you should specify a number of partitions that is a power of 2. When you specify individual hash partitions, you can specify both `TABLESPACE` and table compression in the `partitioning_storage_clause`. When you specify hash partitions by quantity, you can specify only `TABLESPACE`. Hash partitions inherit all other attributes from table-level defaults.

The `table_compression` clause has the same function as described for the [table\_properties](#i2128916) of the table as a whole.

The `prefix_compression` clause and the `OVERFLOW` clause have the same function as described for the [index\_org\_table\_clause](#i2128766) .

Tablespace storage specified at the table level is overridden by tablespace storage specified at the partition level, which in turn is overridden by tablespace storage specified at the subpartition level.

In the `individual_hash_partitions` clause, the `TABLESPACE` clause of the `partitioning_storage_clause` determines tablespace storage only for the individual partition being created. In the `hash_partitions_by_quantity` clause, the `STORE` `IN` clause determines placement of partitions as the table is being created and the default storage location for subsequently added partitions.

Restriction on Specifying Hash Partitions by Quantity You cannot specify the `advanced_index_compression` clause of the `index_compression` clause.

Restrictions on Hash Partitioning Hash partitioning is subject to the restrictions listed in ["Restrictions on Partitioning in General"](#BABIICCD). The following additional restrictions apply:

* You cannot specify more than 16 partitioning key columns.
* Partitioning key columns must be of type `CHAR`, `NCHAR`, `VARCHAR2`, `NVARCHAR2`, `VARCHAR`, `NUMBER`, `FLOAT`, `DATE`, `TIMESTAMP`, `TIMESTAMP` `WITH` `LOCAL` `TIMEZONE`, or `RAW`.

composite\_range\_partitions

Use the `composite_range_partitions` clause to first partition `table` by range, and then partition the partitions further into range, hash, or list subpartitions.

The `INTERVAL` clause has the same semantics for composite range partitioning that it has for range partitioning. Refer to ["INTERVAL Clause"](#BABGCEFI) for more information.

Specify [subpartition\_by\_range](#BABIHBBF), [subpartition\_by\_hash](#BABJAFIB) or [subpartition\_by\_list](#BABEGDBF) to indicate the type of subpartitioning you want for each composite range partition. Within these clauses you can specify a subpartition template, which establishes default subpartition characteristics for subpartitions created as part of this statement or subsequently created subpartitions.

After establishing the type of subpartitioning you want for the table, and optionally a subpartition template, you must define at least one range partition.

* You must specify the [range\_values\_clause](#BABGHDFA) , which has the same requirements as for noncomposite range partitions.
* Use the [table\_partition\_description](#BABFBIHA) to define the physical and storage characteristics of the each partition.
* In the `range_partition_desc`, use `range_subpartition_desc`, `list_subpartition_desc`, `individual_hash_subparts`, or `hash_subparts_by_quantity` to specify characteristics for the individual subpartitions of the partition. The values you specify in these clauses supersede for these subpartitions any values you have specified in the `subpartition_template`.
* The only characteristics you can specify for a hash or list subpartition or any LOB subpartition are `TABLESPACE` and `table_compression`.

Restrictions on Composite Range Partitioning Regardless of the type of subpartitioning, composite range partitioning is subject to the following restrictions:

* The only physical attributes you can specify at the subpartition level are `TABLESPACE` and table compression.
* You cannot specify composite partitioning for an index-organized table. Therefore, the `OVERFLOW` clause of the `table_partition_description` is not valid for composite-partitioned tables.
* You cannot specify composite partitioning for tables containing `XMLType` columns.

composite\_list\_partitions

Use the `composite_list_partitions` clause to first partition `table` by list, and then partition the partitions further into range, hash, or list subpartitions.

Specify [subpartition\_by\_range](#BABIHBBF), [subpartition\_by\_hash](#BABJAFIB) or [subpartition\_by\_list](#BABEGDBF) to indicate the type of subpartitioning you want for each composite list partition. Within these clauses you can specify a subpartition template, which establishes default subpartition characteristics for subpartitions created as part of this statement and for subsequently created subpartitions.

After establishing the type of subpartitioning you want for each composite partition, and optionally defining a subpartition template, you must define at least one list partition.

* In the `list_partition_desc`, you must specify the [list\_values\_clause](#BABCDDIA), which has the same requirements as for noncomposite list partitions.
* Use the [table\_partition\_description](#BABFBIHA) to define the physical and storage characteristics of the each partition.
* In the `list_partition_desc`, use `range_subpartition_desc`, `list_subpartition_desc`, `individual_hash_subparts`, or `hash_subparts_by_quantity` to specify characteristics for the individual subpartitions of the partition. The values you specify in these clauses supersede the for these subpartitions any values you have specified in the `subpartition_template`.

Restrictions on Composite List Partitioning Composite list partitioning is subject to the same restrictions as described in ["Restrictions on Composite Range Partitioning"](#CHDFBDBC).

composite\_hash\_partitions

Use the `composite_hash_partitions` clause to first partition `table` using the hash method, and then partition the partitions further into range, hash, or list subpartitions.

Specify [subpartition\_by\_range](#BABIHBBF), [subpartition\_by\_hash](#BABJAFIB) or [subpartition\_by\_list](#BABEGDBF) to indicate the type of subpartitioning you want for each composite range partition. Within these clauses you can specify a subpartition template, which establishes default subpartition characteristics for subpartitions created as part of this statement or subsequently created subpartitions.

After establishing the type of subpartitioning you want for the table, you must specify [individual\_hash\_partitions](#CJAFBCJC) or [hash\_partitions\_by\_quantity](#CJACBFBI).

Restrictions on Composite Hash Partitioning Composite hash partitioning is subject to the same restrictions as described in ["Restrictions on Composite Range Partitioning"](#CHDFBDBC).

subpartition\_template The `subpartition_template` is an optional element of range, list, and hash subpartitioning. The template lets you define default subpartitions for each table partition. Oracle Database will create these default subpartition characteristics in any partition for which you do not explicitly define subpartitions. This clause is useful for creating symmetric partitions. You can override this clause by explicitly defining subpartitions at the partition level, in the `range_subpartition_desc`, `list_subpartition_desc`, `individual_hash_subparts`, or `hash_subparts_by_quantity` clause.

When defining subpartitions with a template, you can explicitly define range, list, or hash subpartitions, or you can define a quantity of hash subpartitions.

* To explicitly define subpartitions, use `range_subpartition_desc`, `list_subpartition_desc`, or `individual_hash_subparts`. You must specify a name for each subpartition. If you specify the `LOB_partitioning_clause` of the `partitioning_storage_clause`, then you must specify `LOB_segname`.
* To define a quantity of hash subpartitions, specify a positive integer for `hash_subpartition_quantity`. The database creates that number of subpartitions in each partition and assigns subpartition names of the form `SYS_SUBP``n`.

Note:

When you specify tablespace storage for the subpartition template, it does not override any tablespace storage you have specified explicitly for the partitions of

`table`

. To specify tablespace storage for subpartitions, do one of these things:

Restrictions on Subpartition Templates Subpartition templates are subject to the following restrictions:

* If you specify `TABLESPACE` for one LOB subpartition, then you must specify `TABLESPACE` for all of the LOB subpartitions of that LOB column. You can specify the same tablespace for more than one LOB subpartition.
* If you specify separate LOB storage for list subpartitions using the `partitioning_storage_clause`, either in the `subpartition_template` or when defining individual subpartitions, then you must specify `LOB_segname` for both LOB and varray columns.

subpartition\_by\_range

Use the `subpartition_by_range` clause to indicate that the database should subpartition by range each partition in `table`. The subpartitioning column list is unrelated to the partitioning key but is subject to the same restrictions (see [column](#BABGEHCB)).

You can use the `subpartition_template` to specify default subpartition characteristic values. See [subpartition\_template](#BABHJECD). The database uses these values for any subpartition in this partition for which you do not explicitly specify the characteristic.

You can also define range subpartitions individually for each partition using the `range_subpartition_desc` of `range_partition_desc` or `list_partition_desc`. If you omit both `subpartition_template` and the `range_subpartition_desc`, then the database creates a single `MAXVALUE` subpartition.

subpartition\_by\_list

Use the `subpartition_by_list` clause to indicate that the database should subpartition each partition in `table` by literal values from `column`. You can specify only one list subpartitioning key column.

You can use the `subpartition_template` to specify default subpartition characteristic values. See [subpartition\_template](#BABHJECD). The database uses these values for any subpartition in this partition for which you do not explicitly specify the characteristic.

You can also define list subpartitions individually for each partition using the `list_subpartition_desc` of `range_partition_desc` or `list_partition_desc`. If you omit both `subpartition_template` and the `list_subpartition_desc`, then the database creates a single `DEFAULT` subpartition.

Restrictions on List Subpartitioning List subpartitioning is subject to the same restrictions as described in [Restrictions on Composite Range Partitioning](#CHDFBDBC).

subpartition\_by\_hash

Use the `subpartition_by_hash` clause to indicate that the database should subpartition by hash each partition in `table`. The subpartitioning column list is unrelated to the partitioning key but is subject to the same restrictions (see [column](#BABJHGCA)).

You can define the subpartitions using the `subpartition_template` or the `SUBPARTITIONS` `integer` clause. See [subpartition\_template](#BABHJECD). In either case, for optimal load balancing you should specify a number of partitions that is a power of 2.

If you specify `SUBPARTITIONS` `integer`, then you determine the default number of subpartitions in each partition of `table`, and optionally one or more tablespaces in which they are to be stored. The default value is 1. If you omit both this clause and `subpartition_template`, then the database will create each partition with one hash subpartition.

Notes on Composite Partitions The following notes apply to composite partitions:

* For all subpartitions, you can use the `range_subpartition_desc`, `list_subpartition_desc`, `individual_hash_subparts`, or `hash_subparts_by_quantity` to specify individual subpartitions by name, and optionally some other characteristics.
* Alternatively, for hash and list subpartitions:

  + You can specify the number of subpartitions and optionally one or more tablespaces where they are to be stored. In this case, Oracle Database assigns subpartition names of the form `SYS_SUBPn`.
  + If you omit the subpartition description and if you have created a subpartition template, then the database uses the template to create subpartitions. If you have not created a subpartition template, then the database creates one hash subpartition or one `DEFAULT` list subpartition.
* For all types of subpartitions, if you omit the subpartitions description entirely, then the database assigns subpartition names as follows:

  + If you have specified a subpartition template and you have specified partition names, then the database generates subpartition names of the form `partition_name` underscore (\_) `subpartition_name` (for example, `P1_SUB1`).
  + If you have not specified a subpartition template or if you have specified a subpartition template but did not specify partition names, then the database generates subpartition names of the form `SYS_SUBP``n`.

reference\_partitioning

Use this clause to partition the table by reference. Partitioning by reference is a method of equipartitioning the table being created (the child table) by a referential constraint to an existing partitioned table (the parent table). When you partition a table by reference, partition maintenance operations subsequently performed on the parent table automatically cascade to the child table. Therefore, you cannot perform partition maintenance operations on a reference-partitioned table directly.

If the parent table is an interval-partitioned table, then partitions in the reference-partitioned child table that correspond to interval partitions in the parent table will be created during inserts into the child table. When an interval partition in a child table is created, the partition name is inherited from the associated parent table partition. If the child table has a table-level default tablespace, then it will be used as the tablespace for the new interval partition. Otherwise, the tablespace will be inherited from the parent table partition. Refer to [Oracle Database VLDB and Partitioning Guide](../VLDBG/GUID-52397EF9-EC3B-4E80-8211-77E683263530.md#VLDBG14103) for more information on referencing an interval-partitioned table.

constraint  The partitioning referential constraint must meet the following conditions:

* You must specify a referential integrity constraint defined on the table being created, which must refer to a primary key or unique constraint on the parent table. The constraint must be in `ENABLE` `VALIDATE` `NOT` `DEFERRABLE` state, which is the default when you specify a referential integrity constraint during table creation.
* All foreign key columns referenced in the constraint must be `NOT` `NULL`.
* When you specify the constraint, you cannot specify the `ON` `DELETE` `SET` `NULL` clause of the `references_clause`.
* The parent table referenced in the constraint must be an existing partitioned table. It can be partitioned by any method.
* The foreign and parent keys cannot contain any virtual columns that reference PL/SQL functions or LOB columns.

reference\_partition\_desc  Use this optional clause to specify partition names and to define the physical and storage characteristics of the partition. The subclauses of the `table_partition_description` have the same behavior as described for range partitions in [table\_partition\_description](#BABFBIHA).

If you specify this clause when creating a reference-partitioned child table whose parent is an interval-partitioned table, then the partition descriptors are used for the child table's non-interval partitions. Partition descriptors cannot be specified for interval partitions.

Restrictions on Reference Partitioning Reference partitioning is subject to the restrictions listed in ["Restrictions on Partitioning in General"](#BABIICCD). The following additional restrictions apply:

* Restrictions for reference partitioning are derived from the partitioning strategy of the parent table.
* You cannot specify this clause for an index-organized table, an external table, or a domain index storage table.
* The parent table can be partitioned by reference, but `constraint` cannot be self-referential. The table being created cannot be partitioned based on a reference to itself.
* If `ROW` `MOVEMENT` is enabled for the parent table, it must also be enabled for the child table.

system\_partitioning

Use this clause to create system partitions. System partitioning does not entail any partitioning key columns, nor do system partitions have any range or list bounds or hash algorithms. Rather, they provide a way to equipartition dependent tables such as nested table or domain index storage tables with partitioned base tables.

* If you specify only `PARTITION` `BY` `SYSTEM`, then the database creates one partition with a system-generated name of the form `SYS_P``n`.
* If you specify `PARTITION` `BY` `SYSTEM` `PARTITIONS` `integer`, then the database creates as many partitions as you specify in `integer`, which can range from 1 to 1024K-1.
* The description of the partition takes the same syntax as reference partitions, so they share the `reference_partition_desc`. You can specify additional partition attributes with the `reference_partition_desc` syntax. However, within the `table_partition_description`, you cannot specify the `OVERFLOW` clause.

Restrictions on System Partitioning System partitioning is subject to the following restrictions:

* You cannot system partition an index-organized table or a table that is part of a cluster.
* Composite partitioning is not supported with system partitioning.
* You cannot split a system partition.
* You cannot specify system partitioning in a `CREATE` `TABLE` ... `AS` `SELECT` statement.
* To insert data into a system-partitioned table using an `INSERT` `INTO` ... `AS` `subquery` statement, you must use partition-extended syntax to specify the partition into which the values returned by the subquery will be inserted.

attribute\_clustering\_clause

Note:

The

`attribute_clustering_clause`

is available starting with Oracle Database 12

c

Release 1 (12.1.0.2).

Use this clause to enable the table for attribute clustering. Attribute clustering lets you cluster data in close physical proximity based on the content of specified columns.

Attribute clustering can be based only on columns in `table` or on joined values from other tables. The latter is called join attribute clustering.

clustering\_join

Use this clause to specify join attribute clustering. Use the `JOIN` clause to specify the joined values from other tables on which to base the attribute clustering. You can specify a maximum of four `JOIN` clauses.

cluster\_clause

Use this clause to specify the type of ordering to use for the table: linear ordering or interleaved ordering. If you do not specify the `LINEAR` or `INTERLEAVED` keyword, then the default is `LINEAR`.

BY LINEAR ORDER Use this clause to specify linear ordering. This type of ordering stores data according to the order of the specified columns. If you specify this clause, then you can specify only one clustering column group, which can contain at most 10 columns.

BY INTERLEAVED ORDER Use this clause to specify interleaved ordering. This type of ordering uses a special multidimensional clustering technique, similar to z-ordering, that permits multicolumn clustering. If you specify this clause, then you can specify at most four clustering column groups, with a maximum of 40 columns across all groups.

clustering\_columns

Use this clause to specify one or more clustering column groups.

clustering\_column\_group

Use this clause to specify one or more columns to be included in the clustering column group.

clustering\_when

Use these clauses to allow or disallow attribute clustering during direct-path insert operations and data movement operations.

ON LOAD Specify `YES` `ON` `LOAD` to allow, or `NO` `ON` `LOAD` to disallow, attribute clustering during direct-path inserts (serial or parallel) resulting either from an `INSERT` or a `MERGE` operation. The default is `NO` `ON` `LOAD`.

ON DATA MOVEMENT Specify `YES` `ON` `DATA` `MOVEMENT` to allow, or `NO` `ON` `DATA` `MOVEMENT` to disallow, attribute clustering for data movement that occurs during the following operations:

* Data redefinition using the `DBMS_REDEFINITION` package
* Table partition maintenance operations that are specified by the following clauses of `ALTER` `TABLE`: `coalesce_table`, `merge_table_partitions`, `move_table_partition`, and `split_table_partition`

The default is `NO` `ON` `DATA` `MOVEMENT`.

zonemap\_clause

Use this clause to create a zone map on the table. The zone map tracks the columns specified in the `clustering_columns` clause.

* Specify `WITH` `MATERIALIZED` `ZONEMAP` to create a zone map. For `zonemap_name`, specify the name of the zone map to be created. If you omit `zonemap_name`, then the name of the zone map is `ZMAP$_``table`.
* Specify `WITHOUT` `MATERIALIZED` `ZONEMAP` to not create a zone map. This is the default.

If you subsequently drop the table or use the `ALTER` `TABLE` statement to `DROP` `CLUSTERING` or `MODIFY` `CLUSTERING` ... `WITHOUT` `MATERIALIZED` `ZONEMAP`, then the zone map will be dropped.

Restrictions on Attribute Clustering The following restrictions apply to attribute clustering:

* Attribute clustering is not supported for temporary tables or external tables.
* The table being created must be a heap-organized table. However, tables specified in the `clustering_join` clause can be heap-organized or index-organized tables.
* Clustering columns must be of a scalar data type and cannot be encrypted.
* If you specify `BY` `LINEAR` `ORDER`, then you can specify only one clustering column group, which can contain at most 10 columns.
* If you specify `BY` `INTERLEAVED` `ORDER`, then you can specify at most four clustering column groups, with a maximum of 40 columns across all groups.
* For join attribute clustering:
* Attribute clustering will not order rows that are inserted using `MERGE` statements or multitable insert operations.

CACHE | NOCACHE | CACHE READS

Use these clauses to indicate how Oracle Database should store blocks in the buffer cache. For LOB storage, you can specify `CACHE`, `NOCACHE`, or `CACHE` `READS`. For other types of storage, you can specify only `CACHE` or `NOCACHE`.

If you omit these clauses, then:

* In a `CREATE` `TABLE` statement, `NOCACHE` is the default.
* In an `ALTER` `TABLE` statement, the existing value is not changed.

The behavior of `CACHE` and `NOCACHE` described in this section does not apply when Oracle Database chooses to use direct reads or to perform table scans using parallel query.

CACHE For data that is accessed frequently, this clause indicates that the blocks retrieved for this table are placed at the most recently used end of the least recently used (LRU) list in the buffer cache when a full table scan is performed. This attribute is useful for small lookup tables.

See Also:

[Oracle Database Concepts](../CNCPT/memory.md#CNCPT1223)

for more information on how the database maintains the least recently used (LRU) list

As a parameter in the `LOB_storage_clause`, `CACHE` specifies that the database places LOB data values in the buffer cache for faster access. The database evaluates this parameter in conjunction with the `logging_clause`. If you omit this clause, then the default value for both BasicFiles and SecureFiles LOBs is `NOCACHE` `LOGGING`.

Restriction on CACHE You cannot specify `CACHE` for an index-organized table. However, index-organized tables implicitly provide `CACHE` behavior.

NOCACHE For data that is not accessed frequently, this clause indicates that the blocks retrieved for this table are placed at the least recently used end of the LRU list in the buffer cache when a full table scan is performed. `NOCACHE` is the default for LOB storage.

As a parameter in the `LOB_storage_clause`, `NOCACHE` specifies that the LOB values are not brought into the buffer cache. `NOCACHE` is the default for LOB storage.

Restriction on NOCACHE You cannot specify `NOCACHE` for an index-organized table.

CACHE READS `CACHE` `READS` applies only to LOB storage. It specifies that LOB values are brought into the buffer cache only during read operations but not during write operations.

logging\_clause Use this clause to indicate whether the storage of data blocks should be logged or not.

See Also:

[logging\_clause](clauses005.md#i999782)

for a description of the

`logging_clause`

when specified as part of

`LOB_parameters`

RESULT\_CACHE Clause

Use this clause to determine whether the results of statements or query blocks that name this table are considered for storage in the result cache. Two modes of result caching are available:

* `DEFAULT`: Result caching is not determined at the table level. The query is considered for result caching if the `RESULT_CACHE_MODE` initialization parameter is set to `FORCE`, or if that parameter is set to `MANUAL` and the `RESULT_CACHE` hint is specified in the query. This is the default if you omit this clause.
* `FORCE`: If all tables names in the query have this setting, then the query is always considered for caching unless the `NO_RESULT_CACHE` hint is specified for the query. If one or more tables named in the query are set to `DEFAULT`, then the effective table annotation for that query is considered to be `DEFAULT`, with the semantics described above.

You can query the `RESULT_CACHE` column of the `DBA_`, `ALL_`, and `USER_TABLES` data dictionary views to learn the result cache mode of the table.

The `RESULT_CACHE` and `NO_RESULT_CACHE` SQL hints take precedence over these result cache table annotations and the `RESULT_CACHE_MODE` initialization parameter. The `RESULT_CACHE_MODE` setting of `FORCE` in turn takes precedence over this table annotation clause.

Note:

The

`RESULT_CACHE_MODE`

setting of

`FORCE`

is not recommended, as it can cause significant performance and latching overhead, as database and clients will try to cache all queries.

parallel\_clause

The `parallel_clause` lets you parallelize creation of the table and set the default degree of parallelism for queries and the DML `INSERT`, `UPDATE`, `DELETE`, and `MERGE` after table creation.

Note:

The syntax of the

`parallel_clause`

supersedes syntax appearing in earlier releases of Oracle. Superseded syntax is still supported for backward compatibility but may result in slightly different behavior from that documented.

NOPARALLEL Specify `NOPARALLEL` for serial execution. This is the default.

PARALLEL  Specify `PARALLEL` if you want Oracle to select a degree of parallelism equal to the number of CPUs available on all participating instances times the value of the `PARALLEL_THREADS_PER_CPU` initialization parameter.

PARALLEL integer Specification of `integer` indicates the degree of parallelism, which is the number of parallel threads used in the parallel operation. Each parallel thread may use one or two parallel execution servers. Normally Oracle calculates the optimum degree of parallelism, so it is not necessary for you to specify `integer`.

NOROWDEPENDENCIES | ROWDEPENDENCIES

This clause lets you specify whether `table` will use row-level dependency tracking. With this feature, each row in the table has a system change number (SCN) that represents a time greater than or equal to the commit time of the last transaction that modified the row. You cannot change this setting after `table` is created.

ROWDEPENDENCIES Specify `ROWDEPENDENCIES` if you want to enable row-level dependency tracking. This setting is useful primarily to allow for parallel propagation in replication environments. It increases the size of each row by 6 bytes.

Restriction on the ROWDEPENDENCIES Clause Oracle does not support table compression for tables that use row-level dependency tracking. If you specify both the `ROWDEPENDENCIES` clause and the `table_compression` clause, then the `table_compression` clause is ignored. To remove the `ROWDEPENDENCIES` attribute, you must redefine the table using the `DBMS_REDEFINITION` package or recreate the table.

NOROWDEPENDENCIES Specify `NOROWDEPENDENCIES` if you do not want `table` to use the row-level dependency tracking feature. This is the default.

enable\_disable\_clause

The `enable_disable_clause` lets you specify whether Oracle Database should apply a constraint. By default, constraints are created in `ENABLE` `VALIDATE` state.

Restrictions on Enabling and Disabling Constraints Enabling and disabling constraints are subject to the following restrictions:

* To enable or disable any integrity constraint, you must have defined the constraint in this or a previous statement.
* You cannot enable a foreign key constraint unless the referenced unique or primary key constraint is already enabled.
* In the `index_properties` clause of the `using_index_clause`, the `INDEXTYPE` `IS` ... clause is not valid in the definition of a constraint.

ENABLE Clause Use this clause if you want the constraint to be applied to the data in the table. This clause is described fully in ["ENABLE Clause"](clauses002.md#i1010237) in the documentation on constraints.

DISABLE Clause Use this clause if you want to disable the integrity constraint. This clause is described fully in ["DISABLE Clause"](clauses002.md#i1002349) in the documentation on constraints.

UNIQUE  The `UNIQUE` clause lets you enable or disable the unique constraint defined on the specified column or combination of columns.

PRIMARY KEY  The `PRIMARY` `KEY` clause lets you enable or disable the primary key constraint defined on the table.

CONSTRAINT  The `CONSTRAINT` clause lets you enable or disable the integrity constraint named `constraint_name`.

KEEP | DROP INDEX This clause lets you either preserve or drop the index Oracle Database has been using to enforce a unique or primary key constraint.

Restriction on Preserving and Dropping Indexes You can specify this clause only when disabling a unique or primary key constraint.

using\_index\_clause  The `using_index_clause` lets you specify an index for Oracle Database to use to enforce a unique or primary key constraint, or lets you instruct the database to create the index used to enforce the constraint. This clause is discussed fully in [using\_index\_clause](clauses002.md#i1002419) in the documentation on constraints.

CASCADE  Specify `CASCADE` to disable any integrity constraints that depend on the specified integrity constraint. To disable a primary or unique key that is part of a referential integrity constraint, you must specify this clause.

Restriction on CASCADE You can specify `CASCADE` only if you have specified `DISABLE`.

row\_movement\_clause

The `row_movement_clause` lets you specify whether the database can move a table row. It is possible for a row to move, for example, during table compression or an update operation on partitioned data.

Caution:

If you need static rowids for data access, then do not enable row movement. For a normal (heap-organized) table, moving a row changes the rowid of the row. For a moved row in an index-organized table, the logical rowid remains valid, although the physical guess component of the logical rowid becomes inaccurate.

* Specify `ENABLE` to allow the database to move a row, thus changing the rowid.
* Specify `DISABLE` if you want to prevent the database from moving a row, thus preventing a change of rowid.

If you omit this clause, then the database disables row movement.

Restriction on Row Movement You cannot specify this clause for a nonpartitioned index-organized table.

flashback\_archive\_clause

You must have the `FLASHBACK` `ARCHIVE` object privilege on the specified flashback data archive to specify this clause. Use this clause to enable or disable historical tracking for the table.

* Specify `FLASHBACK` `ARCHIVE` to enable tracking for the table. You can specify `flashback_archive` to designate a particular flashback data archive for this table. The flashback data archive you specify much already exist.

  If you omit `flashback_archive`, then the database uses the default flashback data archive designated for the system. If no default flashback data archive has been designated for the system, then you must specify `flashback_archive`.
* Specify `NO` `FLASHBACK` `ARCHIVE` to disable tracking for the table. This is the default.

Restrictions on flashback\_archive\_clause Flashback data archives are subject to the following restrictions:

* You cannot specify this clause for a nested table, clustered table, temporary table, remote table, or external table.
* You cannot specify this clause for a table compressed with Hybrid Columnar Compression.
* The table for which you are specifying this clause cannot contain any `LONG` or nested table columns.
* If you specify this clause and subsequently copy the table to a different database—using the export and import utilities or the transportable tablespace feature—then the copied table will not be enabled for tracking and the archived data for the original table will not be available for the copied table.

See Also:

* [Oracle Database Development Guide](../ADFNS/adfns_flashback.md#ADFNS01011) for general information on using flashback data archives
* [ALTER FLASHBACK ARCHIVE](statements_1010.md#BABGBHGE) for information on changing the quota and retention attributes of the flashback data archive, as well as adding or changing tablespace storage for the flashback data archive

ROW ARCHIVAL

Specify this clause to enable `table` for row archival. This clause lets you implement In-Database Archiving, which allows you to designate table rows as active or archived. You can then perform queries on only the active rows within the table.

When you specify this clause, a hidden column `ORA_ARCHIVE_STATE` is created in the table. The column is of data type `VARCHAR2`. You can specify a value of `0` or `1` for this column to indicate whether a row is active (`0`) or archived (`1`). If you do not specify a value for `ORA_ARCHIVE_STATE` when inserting data into the table, then the value is set to `0`.

* If `ROW` `ARCHIVE` `VISIBILITY` `=` `ACTIVE` for the session, then the database will consider only active rows when performing queries on the table.
* If `ROW` `ARCHIVE` `VISIBILITY` `=` `ALL` for the session, then the database will consider all rows when performing queries on the table.

See Also:

* The `ALTER` `SESSION` [ROW ARCHIVAL VISIBILITY](statements_2015.md#CCHEHEJJ) clause to learn how to configure row archival visibility for a session
* The `ALTER` `TABLE` [[NO] ROW ARCHIVAL](statements_3001.md#CJABCCEH) clause to learn how to enable or disable an existing table for row archival
* Oracle Database VLDB and Partitioning Guide for more information on In-Database Archiving

AS subquery

Specify a subquery to determine the contents of the table. The rows returned by the subquery are inserted into the table upon its creation.

For object tables, `subquery` can contain either one expression corresponding to the table type, or the number of top-level attributes of the table type. Refer to [SELECT](statements_10002.md#i2065646) for more information.

If `subquery` returns the equivalent of part or all of an existing materialized view, then the database may rewrite the query to use the materialized view in place of one or more tables specified in `subquery`.

Oracle Database derives data types and lengths from the subquery. Oracle Database follows the following rules for integrity constraints and other column and table attributes:

* Oracle Database automatically defines on columns in the new table any `NOT` `NULL` constraints that have a state of `NOT` `DEFERRABLE` and `VALIDATE`, and were explicitly created on the corresponding columns of the selected table if the subquery selects the column rather than an expression containing the column. If any rows violate the constraint, then the database does not create the table and returns an error.
* `NOT` `NULL` constraints that were implicitly created by Oracle Database on columns of the selected table (for example, for primary keys) are not carried over to the new table.
* In addition, primary keys, unique keys, foreign keys, check constraints, partitioning criteria, indexes, and column default values are not carried over to the new table.
* If the selected table is partitioned, then you can choose whether the new table will be partitioned the same way, partitioned differently, or not partitioned. Partitioning is not carried over to the new table. Specify any desired partitioning as part of the `CREATE` `TABLE` statement before the `AS` `subquery` clause.
* A column that is encrypted using Transparent Data Encryption in the selected table will not be encrypted in the new table unless you define the column in the new table as encrypted at create time.

  Note:

  Oracle recommends that you encrypt sensitive columns before populating them with data. This will avoid creating clear text copies of sensitive data.

If each column returned by `subquery` has a column name or is an expression with a specified column alias, then you can omit the columns from the table definition entirely. In this case, the names of the columns of `table` are the same as the columns in `subquery`. The exception is creating an index-organized table, for which you must specify the columns in the table definition because you must specify a primary key column.

You can use `subquery` in combination with the `TO_LOB` function to convert the values in a `LONG` column in another table to LOB values in a column of the table you are creating.

parallel\_clause If you specify the `parallel_clause` in this statement, then the database will ignore any value you specify for the `INITIAL` storage parameter and will instead use the value of the `NEXT` parameter.

ORDER BY The `ORDER` `BY` clause lets you order rows returned by the subquery.

When specified with `CREATE` `TABLE`, this clause does not necessarily order data across the entire table. For example, it does not order across partitions. Specify this clause if you intend to create an index on the same key as the `ORDER` `BY` key column. Oracle Database will cluster data on the `ORDER` `BY` key so that it corresponds to the index key.

Restrictions on the Defining Query of a Table The table query is subject to the following restrictions:

* The number of columns in the table must equal the number of expressions in the subquery.
* The column definitions can specify only column names, default values, and integrity constraints, not data types.
* You cannot define a foreign key constraint in a `CREATE` `TABLE` statement that contains `AS` `subquery` unless the table is reference partitioned and the constraint is the table's partitioning referential constraint. In all other cases, you must create the table without the constraint and then add it later with an `ALTER` `TABLE` statement.

object\_table

The `OF` clause lets you explicitly create an object table of type `object_type`. The columns of an object table correspond to the top-level attributes of type `object_type`. Each row will contain an object instance, and each instance will be assigned a unique, system-generated object identifier when a row is inserted. If you omit `schema`, then the database creates the object table in your own schema.

Object tables, as well as `XMLType` tables, object views, and `XMLType` views, do not have any column names specified for them. Therefore, Oracle defines a system-generated pseudocolumn `OBJECT_ID`. You can use this column name in queries and to create object views with the `WITH` `OBJECT` `IDENTIFIER` clause.

object\_table\_substitution

Use the `object_table_substitution` clause to specify whether row objects corresponding to subtypes can be inserted into this object table.

NOT SUBSTITUTABLE AT ALL LEVELS `NOT` `SUBSTITUTABLE` `AT` `ALL` `LEVELS` indicates that the object table being created is not substitutable. In addition, substitution is disabled for all embedded object attributes and elements of embedded nested tables and arrays. The default is `SUBSTITUTABLE` `AT` `ALL` `LEVELS`.

object\_properties

The properties of object tables are essentially the same as those of relational tables. However, instead of specifying columns, you specify attributes of the object.

For `attribute`, specify the qualified column name of an item in an object.

oid\_clause

The `oid_clause` lets you specify whether the object identifier of the object table should be system generated or should be based on the primary key of the table. The default is `SYSTEM` `GENERATED`.

Restrictions on the oid\_clause This clause is subject to the following restrictions:

Note:

A primary key object identifier is locally unique but not necessarily globally unique. If you require a globally unique identifier, then you must ensure that the primary key is globally unique.

oid\_index\_clause

This clause is relevant only if you have specified the `oid_clause` as `SYSTEM` `GENERATED`. It specifies an index, and optionally its storage characteristics, on the hidden object identifier column.

For `index`, specify the name of the index on the hidden system-generated object identifier column. If you omit `index`, then the database generates a name.

physical\_properties and table\_properties

The semantics of these clauses are documented in the corresponding sections under relational tables. See [physical\_properties](#i2128663) and [table\_properties](#i2128916).

XMLType\_table

Use the `XMLType_table` syntax to create a table of data type `XMLType`. Most of the clauses used to create an `XMLType` table have the same semantics that exist for object tables. The clauses specific to `XMLType` tables are described in this section.

Object tables, as well as `XMLType` tables, object views, and `XMLType` views, do not have any column names specified for them. Therefore, Oracle defines a system-generated pseudocolumn `OBJECT_ID`. You can use this column name in queries and to create object views with the `WITH` `OBJECT` `IDENTIFIER` clause.

XMLSchema\_spec

This clause lets you specify the URL of a registered XMLSchema, either in the `XMLSCHEMA` clause or as part of the `ELEMENT` clause, and an XML element name.

You must specify an element, although the XMLSchema URL is optional. If you do specify an XMLSchema URL, then you must already have registered the XMLSchema using the `DBMS_XMLSCHEMA` package.

The optional `STORE` `ALL` `VARRAYS` `AS` clause lets you specify how all varrays in the `XMLType` table or column are to be stored.

The optional `ALLOW` | `DISALLOW` clauses are valid only if you have specified `BINARY` `XML` storage.

* `ALLOW` `NONSCHEMA` indicates that non-schema-based documents can be stored in the `XMLType` column.
* `DISALLOW` `NONSCHEMA` indicates that non-schema-based documents cannot be stored in the `XMLType` column. This is the default.
* `ALLOW` `ANYSCHEMA` indicates that any schema-based document can be stored in the `XMLType` column.
* `DISALLOW` `ANYSCHEMA` indicates that any schema-based document cannot be stored in the `XMLType` column. This is the default.

Examples

Creating Tables: General Examples

This statement shows how the `employees` table owned by the sample human resources (`hr`) schema was created. A hypothetical name is given to the table and constraints so that you can duplicate this example in your test database:

```
CREATE TABLE employees_demo
    ( employee_id    NUMBER(6)
    , first_name     VARCHAR2(20)
    , last_name      VARCHAR2(25) 
         CONSTRAINT emp_last_name_nn_demo NOT NULL
    , email          VARCHAR2(25) 
         CONSTRAINT emp_email_nn_demo     NOT NULL
    , phone_number   VARCHAR2(20)
    , hire_date      DATE  DEFAULT SYSDATE 
         CONSTRAINT emp_hire_date_nn_demo  NOT NULL
    , job_id         VARCHAR2(10)
       CONSTRAINT     emp_job_nn_demo  NOT NULL
    , salary         NUMBER(8,2)
       CONSTRAINT     emp_salary_nn_demo  NOT NULL
    , commission_pct NUMBER(2,2)
    , manager_id     NUMBER(6)
    , department_id  NUMBER(4)
    , dn             VARCHAR2(300)
    , CONSTRAINT     emp_salary_min_demo
                     CHECK (salary > 0) 
    , CONSTRAINT     emp_email_uk_demo
                     UNIQUE (email)
    ) ;
```

This table contains twelve columns. The `employee_id` column is of data type `NUMBER`. The `hire_date` column is of data type `DATE` and has a default value of `SYSDATE`. The `last_name` column is of type `VARCHAR2` and has a `NOT` `NULL` constraint, and so on.

Creating a Table: Storage Example To define the same `employees_demo` table in the `example` tablespace with a small storage capacity, issue the following statement:

```
CREATE TABLE employees_demo
    ( employee_id    NUMBER(6)
    , first_name     VARCHAR2(20)
    , last_name      VARCHAR2(25) 
         CONSTRAINT emp_last_name_nn_demo NOT NULL
    , email          VARCHAR2(25) 
         CONSTRAINT emp_email_nn_demo     NOT NULL
    , phone_number   VARCHAR2(20)
    , hire_date      DATE  DEFAULT SYSDATE 
         CONSTRAINT emp_hire_date_nn_demo  NOT NULL
    , job_id         VARCHAR2(10)
       CONSTRAINT     emp_job_nn_demo  NOT NULL
    , salary         NUMBER(8,2)
       CONSTRAINT     emp_salary_nn_demo  NOT NULL
    , commission_pct NUMBER(2,2)
    , manager_id     NUMBER(6)
    , department_id  NUMBER(4)
    , dn             VARCHAR2(300)
    , CONSTRAINT     emp_salary_min_demo
                     CHECK (salary > 0) 
    , CONSTRAINT     emp_email_uk_demo
                     UNIQUE (email)
    ) 
   TABLESPACE example 
   STORAGE (INITIAL 8M);
```

Creating a Table with a DEFAULT ON NULL Column Value: Example 

The following statement creates a table `myemp`, which can be used to store employee data. The `department_id` column is defined with a `DEFAULT` `ON` `NULL` column value of 50. Therefore, if a subsequent `INSERT` statement attempts to assign a NULL value to `department_id`, then the value of 50 will be assigned instead.

```
CREATE TABLE myemp (employee_id number, last_name varchar2(25),
                    department_id NUMBER DEFAULT ON NULL 50 NOT NULL);
```

In the `employees` table, `employee_id` 178 has a NULL value for `department_id`:

```
SELECT employee_id, last_name, department_id
  FROM employees
  WHERE department_id IS NULL;

EMPLOYEE_ID LAST_NAME                 DEPARTMENT_ID
----------- ------------------------- -------------
        178 Grant
```

Populate the `myemp` table with the `employee_id`, `last_name`, and `department_id` column data from the `employees` table:

```
INSERT INTO myemp (employee_id, last_name, department_id)
  (SELECT employee_id, last_name, department_id from employees);
```

In the `myemp` table, `employee_id` 178 has a value of 50 for `department_id`:

```
SELECT employee_id, last_name, department_id
  FROM myemp
  WHERE employee_id = 178;
 
EMPLOYEE_ID LAST_NAME                 DEPARTMENT_ID
----------- ------------------------- -------------
        178 Grant                                50
```

Creating a Table with an Identity Column: Examples 

The following statement creates a table `t1` with an identity column `id`. The sequence generator will always assign increasing integer values to `id`, starting with `1`.

```
CREATE TABLE t1 (id NUMBER GENERATED AS IDENTITY);
```

The following statement creates a table `t2` with an identity column `id`. The sequence generator will, by default, assign increasing integer values to `id` in increments of 10 starting with 100.

```
CREATE TABLE t2 (id NUMBER GENERATED BY DEFAULT AS IDENTITY (START WITH 100 INCREMENT BY 10));
```

Creating a Table: Temporary Table Example The following statement creates a temporary table `today_sales` for use by sales representatives in the sample database. Each sales representative session can store its own sales data for the day in the table. The temporary data is deleted at the end of the session.

```
CREATE GLOBAL TEMPORARY TABLE today_sales
   ON COMMIT PRESERVE ROWS 
   AS SELECT * FROM orders WHERE order_date = SYSDATE;
```

Creating a Table with Deferred Segment Creation: Example The following statement creates a table with deferred segment creation. Oracle Database will not create a segment for the data of this table until data is inserted into the table:

```
CREATE TABLE later (col1 NUMBER, col2 VARCHAR2(20))    SEGMENT CREATION DEFERRED;
```

Substitutable Table and Column Examples The following statements create a type hierarchy, which can be used to create a substitutable table. Type `employee_t` inherits the `name` and `ssn` attributes from type `person_t` and in addition has `department_id` and `salary` attributes. Type `part_time_emp_t` inherits all of the attributes from `employee_t` and, through `employee_t`, those of `person_t` and in addition has a `num_hrs` attribute. Type `part_time_emp_t` is final by default, so no further subtypes can be created under it.

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn NUMBER) 
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t 
   (department_id NUMBER, salary NUMBER) NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs NUMBER);
/
```

The following statement creates a substitutable table from the `person_t` type:

```
CREATE TABLE persons OF person_t;
```

The following statement creates a table with a substitutable column of type `person_t`:

```
CREATE TABLE books (title VARCHAR2(100), author person_t);
```

When you insert into `persons` or `books`, you can specify values for the attributes of `person_t` or any of its subtypes. Examples of insert statements appear in ["Inserting into a Substitutable Tables and Columns: Examples"](statements_9015.md#i2085891).

You can extract data from such tables using built-in functions and conditions. For examples, see the functions [TREAT](functions234.md#i1018806) and [SYS\_TYPEID](functions204.md#i1044156), and the ["IS OF type Condition"](conditions015.md#i1051274) condition.

Creating a Table: Parallelism Examples The following statement creates a table using an optimum number of parallel execution servers to scan `employees` and to populate `dept_80`:

```
CREATE TABLE dept_80
   PARALLEL
   AS SELECT * FROM employees
   WHERE department_id = 80;
```

Using parallelism speeds up the creation of the table, because the database uses parallel execution servers to create the table. After the table is created, querying the table is also faster, because the same degree of parallelism is used to access the table.

The following statement creates the same table serially. Subsequent DML and queries on the table will also be serially executed.

```
CREATE TABLE dept_80
   AS SELECT * FROM employees
   WHERE department_id = 80;
```

Creating a Table: ENABLE/DISABLE Examples The following statement shows how the sample table `departments` was created. The example defines a `NOT` `NULL` constraint, and places it in `ENABLE` `VALIDATE` state. A hypothetical name is given to the table so that you can duplicate this example in your test database:

```
CREATE TABLE departments_demo
    ( department_id    NUMBER(4)
    , department_name  VARCHAR2(30)
           CONSTRAINT  dept_name_nn  NOT NULL
    , manager_id       NUMBER(6)
    , location_id      NUMBER(4)
    , dn               VARCHAR2(300)
    ) ;
```

The following statement creates the same `departments_demo` table but also defines a disabled primary key constraint:

```
CREATE TABLE departments_demo
    ( department_id    NUMBER(4)   PRIMARY KEY DISABLE
    , department_name  VARCHAR2(30)
           CONSTRAINT  dept_name_nn  NOT NULL
    , manager_id       NUMBER(6)
    , location_id      NUMBER(4)
    , dn               VARCHAR2(300)
    ) ;
```

Nested Table Example The following statement shows how the sample table `pm.print_media` was created with a nested table column `ad_textdocs_ntab`:

```
CREATE TABLE print_media
    ( product_id        NUMBER(6)
    , ad_id             NUMBER(6)
    , ad_composite      BLOB
    , ad_sourcetext     CLOB
    , ad_finaltext      CLOB
    , ad_fltextn        NCLOB
    , ad_textdocs_ntab  textdoc_tab
    , ad_photo          BLOB
    , ad_graphic        BFILE
    , ad_header         adheader_typ
    ) NESTED TABLE ad_textdocs_ntab STORE AS textdocs_nestedtab;
```

Creating a Table: Multilevel Collection Example The following example shows how an account manager might create a table of customers using two levels of nested tables:

```
CREATE TYPE phone AS OBJECT (telephone NUMBER);
/
CREATE TYPE phone_list AS TABLE OF phone;
/
CREATE TYPE my_customers AS OBJECT (
   cust_name VARCHAR2(25),
   phones phone_list);
/
CREATE TYPE customer_list AS TABLE OF my_customers;
/
CREATE TABLE business_contacts (
   company_name VARCHAR2(25),
   company_reps customer_list)
   NESTED TABLE company_reps STORE AS outer_ntab
   (NESTED TABLE phones STORE AS inner_ntab);
```

The following variation of this example shows how to use the `COLUMN_VALUE` keyword if the inner nested table has no column or attribute name:

```
CREATE TYPE phone AS TABLE OF NUMBER;    
/
CREATE TYPE phone_list AS TABLE OF phone;
/
CREATE TABLE my_customers (
   name VARCHAR2(25),
   phone_numbers phone_list)
   NESTED TABLE phone_numbers STORE AS outer_ntab
   (NESTED TABLE COLUMN_VALUE STORE AS inner_ntab);
```

Creating a Table: LOB Column Example The following statement is a variation of the statement that created the `pm.print_media` table with some added LOB storage characteristics:

```
CREATE TABLE print_media_new
    ( product_id        NUMBER(6)
    , ad_id             NUMBER(6)
    , ad_composite      BLOB
    , ad_sourcetext     CLOB
    , ad_finaltext      CLOB
    , ad_fltextn        NCLOB
    , ad_textdocs_ntab  textdoc_tab
    , ad_photo          BLOB
    , ad_graphic        BFILE
    , ad_header         adheader_typ
    ) NESTED TABLE ad_textdocs_ntab STORE AS textdocs_nestedtab_new
    LOB (ad_sourcetext, ad_finaltext) STORE AS
      (TABLESPACE example
       STORAGE (INITIAL 6144)
       CHUNK 4000
       NOCACHE LOGGING);
```

In the example, the database rounds the value of `CHUNK` up to 4096 (the nearest multiple of the block size of 2048).

Index-Organized Table Example The following statement is a variation of the sample table `hr.countries`, which is index organized:

```
CREATE TABLE countries_demo
    ( country_id      CHAR(2)
      CONSTRAINT country_id_nn_demo NOT NULL
    , country_name    VARCHAR2(40)
    , currency_name   VARCHAR2(25)
    , currency_symbol VARCHAR2(3)
    , region          VARCHAR2(15)
    , CONSTRAINT    country_c_id_pk_demo
                    PRIMARY KEY (country_id ) )
    ORGANIZATION INDEX 
    INCLUDING   country_name 
    PCTTHRESHOLD 2 
    STORAGE 
     ( INITIAL  4K ) 
   OVERFLOW 
    STORAGE 
      ( INITIAL  4K );
```

External Table Example The following statement creates an external table that represents a subset of the sample table `hr.departments`. The `TYPE` clause specifies that the access driver type for the table is `ORACLE_LOADER`. The `ACCESS` `PARAMETERS()` clause specifies parameter values for the `ORACLE_LOADER` access driver. These parameters are shown in italics and form the `opaque_format_spec`. The syntax for `opaque_format_spec` depends on the access driver type and is outside the scope of this document. Refer to [Oracle Database Utilities](../SUTIL/GUID-EA56D498-E8BB-4E02-8ABF-12E7083ED9D5.md#SUTIL012) for details on the `ORACLE_LOADER` access driver and the `opaque_format_spec` syntax.

```
CREATE TABLE dept_external (
   deptno     NUMBER(6),
   dname      VARCHAR2(20),
   loc        VARCHAR2(25) 
)
ORGANIZATION EXTERNAL
(TYPE ORACLE_LOADER
 DEFAULT DIRECTORY admin
 ACCESS PARAMETERS
 (
  RECORDS DELIMITED BY newline
  BADFILE 'ulcase1.bad'
  DISCARDFILE 'ulcase1.dis'
  LOGFILE 'ulcase1.log'
  SKIP 20
  FIELDS TERMINATED BY ","  OPTIONALLY ENCLOSED BY '"'
  (
   deptno     INTEGER EXTERNAL(6),
   dname      CHAR(20),
   loc        CHAR(25)
  )
 )
 LOCATION ('ulcase1.ctl')
)
REJECT LIMIT UNLIMITED;
```

XMLType Examples

This section contains brief examples of creating an `XMLType` table or `XMLType` column. For a more expanded version of these examples, refer to ["Using XML in SQL Statements"](ap_examples002.md#i686084).

XMLType Table Examples The following example creates a very simple `XMLType` table with one implicit binary XML column:

```
CREATE TABLE xwarehouses OF XMLTYPE;
```

The following example creates an XMLSchema-based table. The XMLSchema must already have been created (see ["Using XML in SQL Statements"](ap_examples002.md#i686084) for more information):

```
CREATE TABLE xwarehouses OF XMLTYPE
   XMLSCHEMA "http://www.example.com/xwarehouses.xsd"
   ELEMENT "Warehouse";
```

You can define constraints on an XMLSchema-based table, and you can also create indexes on XMLSchema-based tables, which greatly enhance subsequent queries. You can create object-relational views on `XMLType` tables, and you can create `XMLType` views on object-relational tables.

XMLType Column Examples The following example creates a table with an `XMLType` column stored as a `CLOB`. This table does not require an XMLSchema, so the content structure is not predetermined:

```
CREATE TABLE xwarehouses (
   warehouse_id        NUMBER,
   warehouse_spec      XMLTYPE)
   XMLTYPE warehouse_spec STORE AS CLOB
   (TABLESPACE example
    STORAGE (INITIAL 6144)
    CHUNK 4000
    NOCACHE LOGGING);
```

The following example creates a similar table, but stores `XMLType` data in an object relational `XMLType` column whose structure is determined by the specified schema:

```
CREATE TABLE xwarehouses (
   warehouse_id    NUMBER,
   warehouse_spec  XMLTYPE)
   XMLTYPE warehouse_spec STORE AS OBJECT RELATIONAL
      XMLSCHEMA "http://www.example.com/xwarehouses.xsd"
      ELEMENT "Warehouse";
```

The following example creates another similar table with an `XMLType` column stored as a SecureFiles `CLOB`. This table does not require an XMLSchema, so the content structure is not predetermined. SecureFiles LOBs require a tablespace with automatic segment-space management, so the example uses the tablespace created in ["Specifying Segment Space Management for a Tablespace: Example"](statements_7003.md#i2153459).

```
CREATE TABLE xwarehouses (
  warehouse_id   NUMBER,
  warehouse_spec XMLTYPE)
  XMLTYPE        warehouse_spec STORE AS SECUREFILE CLOB
  (TABLESPACE auto_seg_ts
  STORAGE (INITIAL 6144)
  CACHE);
```

Partitioning Examples

Range Partitioning Example The `sales` table in the sample schema `sh` is partitioned by range. The following example shows an abbreviated variation of the `sales` table. Constraints and storage elements have been omitted from the example.

```
CREATE TABLE range_sales
    ( prod_id        NUMBER(6)
    , cust_id        NUMBER
    , time_id        DATE
    , channel_id     CHAR(1)
    , promo_id       NUMBER(6)
    , quantity_sold  NUMBER(3)
    , amount_sold         NUMBER(10,2)
    ) 
PARTITION BY RANGE (time_id)
  (PARTITION SALES_Q1_1998 VALUES LESS THAN (TO_DATE('01-APR-1998','DD-MON-YYYY')),
   PARTITION SALES_Q2_1998 VALUES LESS THAN (TO_DATE('01-JUL-1998','DD-MON-YYYY')),
   PARTITION SALES_Q3_1998 VALUES LESS THAN (TO_DATE('01-OCT-1998','DD-MON-YYYY')),
   PARTITION SALES_Q4_1998 VALUES LESS THAN (TO_DATE('01-JAN-1999','DD-MON-YYYY')),
   PARTITION SALES_Q1_1999 VALUES LESS THAN (TO_DATE('01-APR-1999','DD-MON-YYYY')),
   PARTITION SALES_Q2_1999 VALUES LESS THAN (TO_DATE('01-JUL-1999','DD-MON-YYYY')),
   PARTITION SALES_Q3_1999 VALUES LESS THAN (TO_DATE('01-OCT-1999','DD-MON-YYYY')),
   PARTITION SALES_Q4_1999 VALUES LESS THAN (TO_DATE('01-JAN-2000','DD-MON-YYYY')),
   PARTITION SALES_Q1_2000 VALUES LESS THAN (TO_DATE('01-APR-2000','DD-MON-YYYY')),
   PARTITION SALES_Q2_2000 VALUES LESS THAN (TO_DATE('01-JUL-2000','DD-MON-YYYY')),
   PARTITION SALES_Q3_2000 VALUES LESS THAN (TO_DATE('01-OCT-2000','DD-MON-YYYY')),
   PARTITION SALES_Q4_2000 VALUES LESS THAN (MAXVALUE))
;
```

For information about partitioned table maintenance operations, see [Oracle Database VLDB and Partitioning Guide](../VLDBG/GUID-F2C99CFA-1090-4A62-B452-D4E116A40A34.md#VLDBG003).

Interval Partitioning Example The following example creates a variation of the `oe.customers` table that is partitioned by interval on the `credit_limit` column. One range partition is created to establish the transition point. All of the original data in the table is within the bounds of the range partition. Then data is added that exceeds the range partition, and the database creates a new interval partition.

```
CREATE TABLE customers_demo (
  customer_id number(6),
  cust_first_name varchar2(20),
  cust_last_name varchar2(20),
  credit_limit number(9,2))
PARTITION BY RANGE (credit_limit)
INTERVAL (1000)
(PARTITION p1 VALUES LESS THAN (5001));
 
INSERT INTO customers_demo
  (customer_id, cust_first_name, cust_last_name, credit_limit)
  (select customer_id, cust_first_name, cust_last_name, credit_limit
  from customers);
```

Query the `USER_TAB_PARTITIONS` data dictionary view before the database creates the interval partition:

```
SELECT partition_name, high_value FROM user_tab_partitions  WHERE table_name = 'CUSTOMERS_DEMO';

PARTITION_NAME                 HIGH_VALUE
------------------------------ ---------------
P1                             5001
```

Insert data into the table that exceeds the high value of the range partition:

```
INSERT INTO customers_demo
  VALUES (699, 'Fred', 'Flintstone', 5500);
```

Query the `USER_TAB_PARTITIONS` view again after the insert to learn the system-generated name of the interval partition created to accommodate the inserted data. (The system-generated name will vary for each session.)

```
SELECT partition_name, high_value FROM user_tab_partitions
  WHERE table_name = 'CUSTOMERS_DEMO'
  ORDER BY partition_name;

PARTITION_NAME                 HIGH_VALUE
------------------------------ ---------------
P1                             5001
SYS_P44                        6001
```

List Partitioning Example The following statement shows how the sample table `oe.customers` might have been created as a list-partitioned table. Some columns and all constraints of the sample table have been omitted in this example.

```
CREATE TABLE list_customers 
   ( customer_id             NUMBER(6)
   , cust_first_name         VARCHAR2(20) 
   , cust_last_name          VARCHAR2(20)
   , cust_address            CUST_ADDRESS_TYP
   , nls_territory           VARCHAR2(30)
   , cust_email              VARCHAR2(40))
   PARTITION BY LIST (nls_territory) (
   PARTITION asia VALUES ('CHINA', 'THAILAND'),
   PARTITION europe VALUES ('GERMANY', 'ITALY', 'SWITZERLAND'),
   PARTITION west VALUES ('AMERICA'),
   PARTITION east VALUES ('INDIA'),
   PARTITION rest VALUES (DEFAULT));
```

Partitioned Table with LOB Columns Example This statement creates a partitioned table `print_media_demo` with two partitions `p1` and `p2`, and a number of LOB columns. The statement uses the sample table `pm.print_media`.

```
CREATE TABLE print_media_demo
   ( product_id NUMBER(6)
   , ad_id NUMBER(6)
   , ad_composite BLOB
   , ad_sourcetext CLOB
   , ad_finaltext CLOB
   , ad_fltextn NCLOB
   , ad_textdocs_ntab textdoc_tab
   , ad_photo BLOB
   , ad_graphic BFILE
   , ad_header adheader_typ
   ) NESTED TABLE ad_textdocs_ntab STORE AS textdocs_nestedtab_demo
      LOB (ad_composite, ad_photo, ad_finaltext)
      STORE AS(STORAGE (INITIAL 20M))
   PARTITION BY RANGE (product_id)
      (PARTITION p1 VALUES LESS THAN (3000) TABLESPACE tbs_01
         LOB (ad_composite, ad_photo)
         STORE AS (TABLESPACE tbs_02 STORAGE (INITIAL 10M))
         NESTED TABLE ad_textdocs_ntab STORE AS nt_p1 (TABLESPACE example),
       PARTITION P2 VALUES LESS THAN (MAXVALUE)
         LOB (ad_composite, ad_finaltext)
         STORE AS SECUREFILE (TABLESPACE auto_seg_ts)
         NESTED TABLE ad_textdocs_ntab STORE AS nt_p2
       )
   TABLESPACE tbs_03;
```

Partition `p1` will be in tablespace `tbs_01`. The LOB data partitions for `ad_composite` and `ad_photo` will be in tablespace `tbs_02`. The LOB data partition for the remaining LOB columns will be in tablespace `tbs_01`. The storage attribute `INITIAL` is specified for LOB columns `ad_composite` and `ad_photo`. Other attributes will be inherited from the default table-level specification. The default LOB storage attributes not specified at the table level will be inherited from the tablespace `tbs_02` for columns `ad_composite` and `ad_photo` and from tablespace `tbs_01` for the remaining LOB columns. LOB index partitions will be in the same tablespaces as the corresponding LOB data partitions. Other storage attributes will be based on values of the corresponding attributes of the LOB data partitions and default attributes of the tablespace where the index partitions reside. The nested table partition for ad\_textdocs\_ntab will be stored as `nt_p1` in tablespace `example`.

Partition `p2` will be in the default tablespace `tbs_03`. The LOB data for `ad_composite` and `ad_finaltext` will be in tablespace `auto_seg_ts` as SecureFiles LOBs. The LOB data for the remaining LOB columns will be in tablespace `tbs_03`. The LOB index for columns `ad_composite` and `ad_finaltext` will be in tablespace `auto_seg_ts`. The LOB index for the remaining LOB columns will be in tablespace `tbs_03`. The nested table partition for `ad_textdocs_ntab` will be stored as `nt_p2` in the default tablespace `tbs_03`.

Hash Partitioning Example The sample table `oe.product_information` is not partitioned. However, you might want to partition such a large table by hash for performance reasons, as shown in this example. The tablespace names are hypothetical in this example.

```
CREATE TABLE hash_products 
    ( product_id          NUMBER(6)   PRIMARY KEY
    , product_name        VARCHAR2(50) 
    , product_description VARCHAR2(2000) 
    , category_id         NUMBER(2) 
    , weight_class        NUMBER(1) 
    , warranty_period     INTERVAL YEAR TO MONTH 
    , supplier_id         NUMBER(6) 
    , product_status      VARCHAR2(20) 
    , list_price          NUMBER(8,2) 
    , min_price           NUMBER(8,2) 
    , catalog_url         VARCHAR2(50) 
    , CONSTRAINT          product_status_lov_demo 
                          CHECK (product_status in ('orderable' 
                                                  ,'planned' 
                                                  ,'under development' 
                                                  ,'obsolete') 
 ) ) 
 PARTITION BY HASH (product_id) 
 PARTITIONS 4 
 STORE IN (tbs_01, tbs_02, tbs_03, tbs_04);
```

Reference Partitioning Example The next statement uses the `hash_products` partitioned table created in the preceding example. It creates a variation of the `oe.order_items` table that is partitioned by reference to the hash partitioning on the product id of `hash_products`. The resulting child table will be created with five partitions. For each row of the child table `part_order_items`, the database evaluates the foreign key value (`product_id`) to determine the partition number of the parent table `hash_products` to which the referenced key belongs. The `part_order_items` row is placed in its corresponding partition.

```
CREATE TABLE part_order_items (
    order_id        NUMBER(12) PRIMARY KEY,
    line_item_id    NUMBER(3),
    product_id      NUMBER(6) NOT NULL,
    unit_price      NUMBER(8,2),
    quantity        NUMBER(8),
    CONSTRAINT product_id_fk
    FOREIGN KEY (product_id) REFERENCES hash_products(product_id))
 PARTITION BY REFERENCE (product_id_fk);
```

Composite-Partitioned Table Examples The table created in the ["Range Partitioning Example"](#i2093664) divides data by time of sale. If you plan to access recent data according to distribution channel as well as time, then composite partitioning might be more appropriate. The following example creates a copy of that `range_sales` table but specifies range-hash composite partitioning. The partitions with the most recent data are subpartitioned with both system-generated and user-defined subpartition names. Constraints and storage attributes have been omitted from the example.

```
CREATE TABLE composite_sales
    ( prod_id        NUMBER(6)
    , cust_id        NUMBER
    , time_id        DATE
    , channel_id     CHAR(1)
    , promo_id       NUMBER(6)
    , quantity_sold  NUMBER(3)
    , amount_sold         NUMBER(10,2)
    ) 
PARTITION BY RANGE (time_id)
SUBPARTITION BY HASH (channel_id)
  (PARTITION SALES_Q1_1998 VALUES LESS THAN (TO_DATE('01-APR-1998','DD-MON-YYYY')),
   PARTITION SALES_Q2_1998 VALUES LESS THAN (TO_DATE('01-JUL-1998','DD-MON-YYYY')),
   PARTITION SALES_Q3_1998 VALUES LESS THAN (TO_DATE('01-OCT-1998','DD-MON-YYYY')),
   PARTITION SALES_Q4_1998 VALUES LESS THAN (TO_DATE('01-JAN-1999','DD-MON-YYYY')),
   PARTITION SALES_Q1_1999 VALUES LESS THAN (TO_DATE('01-APR-1999','DD-MON-YYYY')),
   PARTITION SALES_Q2_1999 VALUES LESS THAN (TO_DATE('01-JUL-1999','DD-MON-YYYY')),
   PARTITION SALES_Q3_1999 VALUES LESS THAN (TO_DATE('01-OCT-1999','DD-MON-YYYY')),
   PARTITION SALES_Q4_1999 VALUES LESS THAN (TO_DATE('01-JAN-2000','DD-MON-YYYY')),
   PARTITION SALES_Q1_2000 VALUES LESS THAN (TO_DATE('01-APR-2000','DD-MON-YYYY')),
   PARTITION SALES_Q2_2000 VALUES LESS THAN (TO_DATE('01-JUL-2000','DD-MON-YYYY'))
      SUBPARTITIONS 8,
   PARTITION SALES_Q3_2000 VALUES LESS THAN (TO_DATE('01-OCT-2000','DD-MON-YYYY'))
     (SUBPARTITION ch_c,
      SUBPARTITION ch_i,
      SUBPARTITION ch_p,
      SUBPARTITION ch_s,
      SUBPARTITION ch_t),
   PARTITION SALES_Q4_2000 VALUES LESS THAN (MAXVALUE)
      SUBPARTITIONS 4)
;
```

The following examples creates a partitioned table of customers based on the sample table `oe.customers`. In this example, the table is partitioned on the `credit_limit` column and list subpartitioned on the `nls_territory` column. The subpartition template determines the subpartitioning of any subsequently added partitions, unless you override the template by defining individual subpartitions. This composite partitioning makes it possible to query the table based on a credit limit range within a specified region:

```
CREATE TABLE customers_part (
   customer_id        NUMBER(6),
   cust_first_name    VARCHAR2(20),
   cust_last_name     VARCHAR2(20),
   nls_territory      VARCHAR2(30),
   credit_limit       NUMBER(9,2)) 
   PARTITION BY RANGE (credit_limit)
   SUBPARTITION BY LIST (nls_territory)
      SUBPARTITION TEMPLATE 
         (SUBPARTITION east  VALUES 
            ('CHINA', 'JAPAN', 'INDIA', 'THAILAND'),
          SUBPARTITION west VALUES 
             ('AMERICA', 'GERMANY', 'ITALY', 'SWITZERLAND'),
          SUBPARTITION other VALUES (DEFAULT))
      (PARTITION p1 VALUES LESS THAN (1000),
       PARTITION p2 VALUES LESS THAN (2500),
       PARTITION p3 VALUES LESS THAN (MAXVALUE));
```

Object Column and Table Examples

Creating Object Tables: Examples Consider object type `department_typ`:

```
CREATE TYPE department_typ AS OBJECT
   ( d_name   VARCHAR2(100), 
     d_address VARCHAR2(200) );
/
```

Object table `departments_obj_t` holds department objects of type `department_typ`:

```
CREATE TABLE departments_obj_t OF department_typ;
```

The following statement creates object table `salesreps` with a user-defined object type, `salesrep_typ`:

```
CREATE OR REPLACE TYPE salesrep_typ AS OBJECT
  ( repId NUMBER,
    repName VARCHAR2(64));

CREATE TABLE salesreps OF salesrep_typ;
```

Creating a Table with a User-Defined Object Identifier: Example This example creates an object type and a corresponding object table whose object identifier is primary key based:

```
CREATE TYPE employees_typ AS OBJECT 
   (e_no NUMBER, e_address CHAR(30));
/

CREATE TABLE employees_obj_t OF employees_typ (e_no PRIMARY KEY)
   OBJECT IDENTIFIER IS PRIMARY KEY;
```

You can subsequently reference the `employees_obj_t` object table using either `inline_ref_constraint` or `out_of_line_ref_constraint` syntax:

```
CREATE TABLE departments_t 
   (d_no    NUMBER,
    mgr_ref REF employees_typ SCOPE IS employees_obj_t);

CREATE TABLE departments_t (
    d_no NUMBER,
    mgr_ref REF employees_typ 
       CONSTRAINT mgr_in_emp REFERENCES employees_obj_t);
```

Specifying Constraints on Type Columns: Example The following example shows how to define constraints on attributes of an object type column:

```
CREATE TYPE address_t AS OBJECT
  ( hno    NUMBER,
    street VARCHAR2(40),
    city   VARCHAR2(20),
    zip    VARCHAR2(5),
    phone  VARCHAR2(10) );
/

CREATE TYPE person AS OBJECT
  ( name        VARCHAR2(40),
    dateofbirth DATE,
    homeaddress address_t,
    manager     REF person );
/

CREATE TABLE persons OF person
  ( homeaddress NOT NULL,
      UNIQUE (homeaddress.phone),
      CHECK (homeaddress.zip IS NOT NULL),
      CHECK (homeaddress.city <> 'San Francisco') );
```