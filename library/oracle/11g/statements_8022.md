# Oracle 11g - statements_8022
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8022.htm

[Go to main content](#BEGIN)

450/522 

# DROP MATERIALIZED VIEW LOG

Purpose

Use the `DROP` `MATERIALIZED` `VIEW` `LOG` statement to remove a materialized view log from the database.

Note:

The keyword

`SNAPSHOT`

is supported in place of

`MATERIALIZED` `VIEW`

for backward compatibility.

Prerequisites

To drop a materialized view log, you must have the privileges needed to drop a table.

Semantics

schema

Specify the schema containing the materialized view log and its master table. If you omit `schema`, then Oracle Database assumes the materialized view log and master table are in your own schema.

table

Specify the name of the master table associated with the materialized view log to be dropped.

After you drop a materialized view log, some materialized views based on the materialized view log master table can no longer be fast refreshed. These materialized views include rowid materialized views, primary key materialized views, and subquery materialized views.

Examples

Dropping a Materialized View Log: Example The following statement drops the materialized view log on the `oe.customers` master table:

```
DROP MATERIALIZED VIEW LOG ON customers;
```

Scripting on this page enhances content navigation, but does not change the content in any way.