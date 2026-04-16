# Oracle 12c - statements_8012
Source: https://docs.oracle.com/database/121/SQLRF/statements_8012.htm

[Go to main content](#BEGIN)

467/555 

# DROP DIMENSION

Purpose

Use the `DROP` `DIMENSION` statement to remove the named dimension.

This statement does not invalidate materialized views that use relationships specified in dimensions. However, requests that have been rewritten by query rewrite may be invalidated, and subsequent operations on such views may execute more slowly.

Prerequisites

The dimension must be in your own schema or you must have the `DROP` `ANY` `DIMENSION` system privilege to use this statement.

Semantics

schema

Specify the name of the schema in which the dimension is located. If you omit `schema`, then Oracle Database assumes the dimension is in your own schema.

dimension

Specify the name of the dimension you want to drop. The dimension must already exist.

Examples

Dropping a Dimension: Example This example drops the `sh.customers_dim` dimension:

```
DROP DIMENSION customers_dim;
```

Scripting on this page enhances content navigation, but does not change the content in any way.