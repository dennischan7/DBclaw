# Oracle 21c - checksum
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/checksum.html

Purpose

Use `CHECKSUM` to detect changes in a table. The order of the rows in the table does not affect the result. You can use `CHECKSUM` with `DISTINCT`, as part of a `GROUP BY` query, as a window function, or an analytical function.

Semantics

`ALL`: Applies the aggregate function to all values. `ALL` is the default option.

`DISTINCT` or `UNIQUE`: Returns the checksum of unique values. `UNIQUE` is an Oracle-specific keyword and not an ANSI standard.

`expr`: Can be a column, constant, bind variable, or an expression involving them. All data types except ADT and JSON are supported.

The return data type is an Oracle number (converted from an (8-byte) signed long long) regardless of the data type of `expr`.

NULL values in `expr` column are ignored.

It returns NULL if `expr` is NULL.

The output of the `CHECKSUM` function is deterministic and independent of the ordering of the input rows.