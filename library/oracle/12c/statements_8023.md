# Oracle 12c - statements_8023
Source: https://docs.oracle.com/database/121/SQLRF/statements_8023.htm

Semantics

schema

Specify the schema containing the materialized view log and its master table. If you omit `schema`, then Oracle Database assumes the materialized view log and master table are in your own schema.

table

Specify the name of the master table associated with the materialized view log to be dropped.

After you drop a materialized view log that was created `FOR` `FAST` `REFRESH`, some materialized views based on the materialized view log master table can no longer be fast refreshed. These materialized views include rowid materialized views, primary key materialized views, and subquery materialized views.

After you drop a materialized view log that was created `FOR` `SYNCHRONOUS` `REFRESH` (a staging log), the materialized views based on the staging log master table can no longer be synchronous refreshed.

Examples

Dropping a Materialized View Log: Example The following statement drops the materialized view log on the `oe.customers` master table:

```
DROP MATERIALIZED VIEW LOG ON customers;
```