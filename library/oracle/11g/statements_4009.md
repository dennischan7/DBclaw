# Oracle 11g - statements_4009
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_4009.htm

Purpose

Use the `COMMENT` statement to add to the data dictionary a comment about a table or table column, view, materialized view, operator, indextype, mining model, or edition.

To drop a comment from the database, set it to the empty string ' '.

Semantics

COLUMN Clause

Specify the name of the column of a table, view, or materialized view to be commented. If you omit `schema`, then Oracle Database assumes the table, view, or materialized view is in your own schema.

You can view the comments on a particular table or column by querying the data dictionary views `USER_TAB_COMMENTS`, `DBA_TAB_COMMENTS`, or `ALL_TAB_COMMENTS` or `USER_COL_COMMENTS`, `DBA_COL_COMMENTS`, or `ALL_COL_COMMENTS`.

EDITION Clause

Specify the name of an existing edition to be commented.

You can query the data dictionary view `ALL_EDITION_COMMENTS` to view comments associated with editions that are accessible to the current user. You can query `DBA_EDITION_COMMENTS` to view comments associated with all editions in the database.

TABLE Clause

Specify the schema and name of the table or materialized view to be commented. If you omit `schema`, then Oracle Database assumes the table or materialized view is in your own schema.

Note:

In earlier releases, you could use this clause to create a comment on a materialized view. You should now use the

`COMMENT` `ON` `MATERIALIZED` `VIEW`

clause for materialized views.

INDEXTYPE Clause

Specify the name of the indextype to be commented. If you omit `schema`, then Oracle Database assumes the indextype is in your own schema.

You can view the comments on a particular indextype by querying the data dictionary views `USER_INDEXTYPE_COMMENTS`, `DBA_INDEXTYPE_COMMENTS`, or `ALL_INDEXTYPE_COMMENTS`.

MATERIALIZED VIEW Clause

Specify the name of the materialized view to be commented. If you omit `schema`, then Oracle Database assumes the materialized view is in your own schema.

You can view the comments on a particular materialized view by querying the data dictionary views `USER_MVIEW_COMMENTS`, `DBA_MVIEW_COMMENTS`, or `ALL_MVIEW_COMMENTS`.

MINING MODEL

Specify the name of the mining model to be commented. You must have the `COMMENT` `ANY` `MINING` `MODEL` system privilege to specify this clause.

OPERATOR Clause

Specify the name of the operator to be commented. If you omit `schema`, then Oracle Database assumes the operator is in your own schema.

You can view the comments on a particular operator by querying the data dictionary views `USER_OPERATOR_COMMENTS`, `DBA_OPERATOR_COMMENTS`, or `ALL_OPERATOR_COMMENTS`.

IS 'string'

Specify the text of the comment. Refer to ["Text Literals"](sql_elements003.md#i42617) for a syntax description of `'string'`.

Example

Creating Comments: Example To insert an explanatory remark on the `job_id` column of the `employees` table, you might issue the following statement:

```
COMMENT ON COLUMN employees.job_id 
   IS 'abbreviated job title';
```

To drop this comment from the database, issue the following statement:

```
COMMENT ON COLUMN employees.job_id IS ' ';
```