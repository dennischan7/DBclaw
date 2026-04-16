# Oracle 11g - functions226
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions226.htm

[Go to main content](#BEGIN)

266/522 

# UPPER

Syntax

Purpose

`UPPER` returns `char`, with all letters uppercase. `char` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. The return value is the same data type as `char`. The database sets the case of the characters based on the binary mapping defined for the underlying character set. For linguistic-sensitive uppercase, refer to [NLS\_UPPER](functions112.md#i89889).

Examples

The following example returns each employee's last name in uppercase:

```
SELECT UPPER(last_name) "Uppercase"
   FROM employees;
```

Scripting on this page enhances content navigation, but does not change the content in any way.