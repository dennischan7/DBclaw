# Oracle 12c - functions105
Source: https://docs.oracle.com/database/121/SQLRF/functions105.htm

[Go to main content](#BEGIN)

178/555 

# LOG

Syntax

Purpose

`LOG` returns the logarithm, base `n2`, of `n1`. The base `n2` can be any positive value other than 0 or 1 and `n1` can be any positive value.

This function takes as arguments any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If any argument is `BINARY_FLOAT` or `BINARY_DOUBLE`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns `NUMBER`.

Examples

The following example returns the log of 100:

```
SELECT LOG(10,100) "Log base 10 of 100"
  FROM DUAL;

Log base 10 of 100
------------------
                 2
```

Scripting on this page enhances content navigation, but does not change the content in any way.