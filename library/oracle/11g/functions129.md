# Oracle 11g - functions129
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions129.htm

[Go to main content](#BEGIN)

169/522 

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