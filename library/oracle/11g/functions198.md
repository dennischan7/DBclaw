# Oracle 11g - functions198
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions198.htm

[Go to main content](#BEGIN)

238/522 

# TO\_BLOB

Syntax

to\_blob::=

Purpose

`TO_BLOB` converts `LONG` `RAW` and `RAW` values to `BLOB` values.

From within a PL/SQL package, you can use `TO_BLOB` to convert `RAW` and `BLOB` values to `BLOB`.

Examples

The following hypothetical example returns the `BLOB` of a `RAW` column value:

```
SELECT TO_BLOB(raw_column) blob FROM raw_table;

BLOB
-----------------------
00AADD343CDBBD
```

Scripting on this page enhances content navigation, but does not change the content in any way.