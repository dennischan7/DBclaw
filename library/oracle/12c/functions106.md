# Oracle 12c - functions106
Source: https://docs.oracle.com/database/121/SQLRF/functions106.htm

[Go to main content](#BEGIN)

179/555 

# LOWER

Syntax

Purpose

`LOWER` returns `char`, with all letters lowercase. `char` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. The return value is the same data type as `char`. The database sets the case of the characters based on the binary mapping defined for the underlying character set. For linguistic-sensitive lowercase, refer to [NLS\_LOWER](functions123.md#i78373).

Examples

The following example returns a string in lowercase:

```
SELECT LOWER('MR. SCOTT MCMILLAN') "Lowercase"
  FROM DUAL;

Lowercase
--------------------
mr. scott mcmillan
```

Scripting on this page enhances content navigation, but does not change the content in any way.