# Oracle 12c - queries010
Source: https://docs.oracle.com/database/121/SQLRF/queries010.htm

[Go to main content](#BEGIN)

366/555 

# Distributed Queries

The Oracle distributed database management system architecture lets you access data in remote databases using Oracle Net and an Oracle Database server. You can identify a remote table, view, or materialized view by appending @`dblink` to the end of its name. The `dblink` must be a complete or partial name for a database link to the database containing the remote table, view, or materialized view.

Restrictions on Distributed Queries  Distributed queries are currently subject to the restriction that all tables locked by a `FOR` `UPDATE` clause and all tables with `LONG` columns selected by the query must be located on the same database. In addition, Oracle Database currently does not support distributed queries that select user-defined types or object `REF` data types on remote tables.

Scripting on this page enhances content navigation, but does not change the content in any way.