# Oracle 12c - functions180
Source: https://docs.oracle.com/database/121/SQLRF/functions180.htm

[Go to main content](#BEGIN)

253/555 

# SINH

Syntax

Purpose

`SINH` returns the hyperbolic sine of `n`.

This function takes as an argument any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If the argument is `BINARY_FLOAT`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns the same numeric data type as the argument.

Examples

The following example returns the hyperbolic sine of 1:

```
SELECT SINH(1) "Hyperbolic sine of 1" FROM DUAL;

Hyperbolic sine of 1
--------------------
          1.17520119
```

Scripting on this page enhances content navigation, but does not change the content in any way.