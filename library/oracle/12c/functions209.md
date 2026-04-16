# Oracle 12c - functions209
Source: https://docs.oracle.com/database/121/SQLRF/functions209.htm

[Go to main content](#BEGIN)

282/555 

# TAN

Syntax

Purpose

`TAN` returns the tangent of `n` (an angle expressed in radians).

This function takes as an argument any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If the argument is `BINARY_FLOAT`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns the same numeric data type as the argument.

Examples

The following example returns the tangent of 135 degrees:

```
SELECT TAN(135 * 3.14159265359/180)
   "Tangent of 135 degrees"  FROM DUAL;

Tangent of 135 degrees
----------------------
                   - 1
```

Scripting on this page enhances content navigation, but does not change the content in any way.