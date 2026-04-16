# Oracle 12c - functions210
Source: https://docs.oracle.com/database/121/SQLRF/functions210.htm

[Go to main content](#BEGIN)

283/555 

# TANH

Syntax

Purpose

`TANH` returns the hyperbolic tangent of `n`.

This function takes as an argument any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If the argument is `BINARY_FLOAT`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns the same numeric data type as the argument.

Examples

The following example returns the hyperbolic tangent of .5:

```
SELECT TANH(.5) "Hyperbolic tangent of .5" 
   FROM DUAL;

Hyperbolic tangent of .5
------------------------
              .462117157
```

Scripting on this page enhances content navigation, but does not change the content in any way.