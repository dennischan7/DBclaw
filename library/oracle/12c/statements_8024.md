# Oracle 12c - statements_8024
Source: https://docs.oracle.com/database/121/SQLRF/statements_8024.htm

[Go to main content](#BEGIN)

479/555 

# DROP MATERIALIZED ZONEMAP

Note:

The

`DROP` `MATERIALIZED` `ZONEMAP`

statement is available starting with Oracle Database 12

c

Release 1 (12.1.0.2).

Purpose

Use the `DROP` `MATERIALIZED` `ZONEMAP` statement to remove an existing zone map from the database.

Prerequisites

The zone map must be in your own schema or you must have the `DROP` `ANY` `MATERIALIZED` `VIEW` system privilege. You must also have the privileges to drop the internal table and indexes that the database uses to maintain the zone map data.

See Also:

[DROP TABLE](statements_9003.md#i2061306)

and

[DROP INDEX](statements_8018.md#i2066885)

for information on privileges required to drop objects that the database uses to maintain the zone map

Semantics

schema

Specify the schema containing the zone map. If you omit `schema`, then Oracle Database assumes the zone map is in your own schema.

zonemap\_name

Specify the name of the existing zone map to be dropped.

Example

Dropping a Zone Map: Examples The following statement drops the zone map `sales_zmap`:

```
DROP MATERIALIZED ZONEMAP sales_zmap;
```

Scripting on this page enhances content navigation, but does not change the content in any way.