# Oracle 11g - functions017
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions017.htm

[Go to main content](#BEGIN)

57/522 

# ATAN2

Syntax

Purpose

`ATAN2` returns the arc tangent of `n1` and `n2`. The argument `n1` can be in an unbounded range and returns a value in the range of -pi to pi, depending on the signs of `n1` and `n2`, expressed in radians.

This function takes as arguments any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. If any argument is `BINARY_FLOAT` or `BINARY_DOUBLE`, then the function returns `BINARY_DOUBLE`. Otherwise the function returns `NUMBER`.

Examples

The following example returns the arc tangent of .3 and .2:

```
SELECT ATAN2(.3, .2) "Arc_Tangent2"
  FROM DUAL;
 
Arc_Tangent2
------------
  .982793723
```

Scripting on this page enhances content navigation, but does not change the content in any way.