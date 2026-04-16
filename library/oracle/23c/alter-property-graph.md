# Oracle 23c - alter-property-graph
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/alter-property-graph.html

IF EXISTS

Specify `IF EXISTS` to alter an existing property graph.

If you specify `IF NOT EXISTS` with `ALTER`, the command fails with the error message: `Incorrect IF EXISTS clause for ALTER/DROP statement`.

COMPILE

Use `ALTER PROPERTY GRAPH COMPILE` to revalidate a graph that reports an invalid state even though it is actually valid. This happens because the dependencies of the graph to its underlying objects may be too coarse. In such cases, it may be enough to use `ALTER PROPERTY GRAPH COMPILE` to revalidate the property graph.

Example: How a Valid Graph May Falsely Report an Invalid State

```
SQL> create table tbl1(c1 number primary key, c2 number, c3 number, c4 as (c2/c3), c5 as (1 / (c2+c3)));

Table created.

SQL> create property graph g vertex tables(tbl1 properties(c2, c3, c5));

Property graph created.

SQL> select object_name, object_type, status from user_objects where object_type in ('PROPERTY GRAPH', 'TABLE');

OBJECT_NAME OBJECT_TYPE STATUS
-------------------- ----------------------- -------
G PROPERTY GRAPH VALID
TBL1 TABLE VALID

SQL> alter table tbl1 drop column c4;

Table altered.

SQL> select object_name, object_type, status from user_objects where object_type in ('PROPERTY GRAPH', 'TABLE');

OBJECT_NAME OBJECT_TYPE STATUS
-------------------- ----------------------- -------
G PROPERTY GRAPH INVALID
TBL1 TABLE VALID

SQL> alter property graph g compile;

Property graph altered.

SQL> select object_name, object_type, status from user_objects where object_type in ('PROPERTY GRAPH', 'TABLE');

OBJECT_NAME OBJECT_TYPE STATUS
-------------------- ----------------------- -------
G PROPERTY GRAPH VALID
TBL1 TABLE VALID

SQL>
```

If `ALTER PROPERTY GRAPH COMPILE` fails to revalidate the graph, then the graph enters the error state. You must then redefine the graph with `CREATE OR REPLACE PROPERTY GRAPH` .