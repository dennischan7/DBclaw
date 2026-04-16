# Oracle 11g - functions090
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions090.htm

[Go to main content](#BEGIN)

130/522 

# LN

Syntax

Purpose

`LN` returns the natural logarithm of `n`, where `n` is greater than 0.

This function takes as an argument any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If the argument is `BINARY_FLOAT`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns the same numeric data type as the argument.

Examples

The following example returns the natural logarithm of 95:

```
SELECT LN(95) "Natural log of 95"
  FROM DUAL;

Natural log of 95
-----------------
       4.55387689
```

Scripting on this page enhances content navigation, but does not change the content in any way.