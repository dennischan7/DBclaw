# Oracle 12c - functions242
Source: https://docs.oracle.com/database/121/SQLRF/functions242.htm

[Go to main content](#BEGIN)

315/555 

# UPPER

Syntax

Purpose

`UPPER` returns `char`, with all letters uppercase. `char` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. The return value is the same data type as `char`. The database sets the case of the characters based on the binary mapping defined for the underlying character set. For linguistic-sensitive uppercase, refer to [NLS\_UPPER](functions124.md#i89889).

Examples

The following example returns each employee's last name in uppercase:

```
SELECT UPPER(last_name) "Uppercase"
   FROM employees;
```

Scripting on this page enhances content navigation, but does not change the content in any way.