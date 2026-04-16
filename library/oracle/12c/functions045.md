# Oracle 12c - functions045
Source: https://docs.oracle.com/database/121/SQLRF/functions045.htm

[Go to main content](#BEGIN)

118/555 

# COSH

Syntax

Purpose

`COSH` returns the hyperbolic cosine of `n`.

This function takes as an argument any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If the argument is `BINARY_FLOAT`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns the same numeric data type as the argument.

Examples

The following example returns the hyperbolic cosine of zero:

```
SELECT COSH(0) "Hyperbolic cosine of 0"
  FROM DUAL;

Hyperbolic cosine of 0
----------------------
                     1
```

Scripting on this page enhances content navigation, but does not change the content in any way.