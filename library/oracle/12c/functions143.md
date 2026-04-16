# Oracle 12c - functions143
Source: https://docs.oracle.com/database/121/SQLRF/functions143.htm

[Go to main content](#BEGIN)

216/555 

# POWER

Syntax

Purpose

`POWER` returns `n2` raised to the `n1` power. The base `n2` and the exponent `n1` can be any numbers, but if `n2` is negative, then `n1` must be an integer.

This function takes as arguments any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If any argument is `BINARY_FLOAT` or `BINARY_DOUBLE`, then the function returns `BINARY_DOUBLE`. Otherwise, the function returns `NUMBER`.

Examples

The following example returns 3 squared:

```
SELECT POWER(3,2) "Raised"
  FROM DUAL;

    Raised
----------
         9
```

Scripting on this page enhances content navigation, but does not change the content in any way.