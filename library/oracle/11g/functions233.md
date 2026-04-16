# Oracle 11g - functions233
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions233.htm

[Go to main content](#BEGIN)

273/522 

# VSIZE

Syntax

Purpose

`VSIZE` returns the number of bytes in the internal representation of `expr`. If `expr` is null, then this function returns null.

This function does not support `CLOB` data directly. However, `CLOB`s can be passed in as arguments through implicit data conversion.

Examples

The following example returns the number of bytes in the `last_name` column of the employees in department 10:

```
SELECT last_name, VSIZE (last_name) "BYTES"      
  FROM employees
  WHERE department_id = 10
  ORDER BY employee_id;
 
LAST_NAME            BYTES
--------------- ----------
Whalen                   6
```

Scripting on this page enhances content navigation, but does not change the content in any way.