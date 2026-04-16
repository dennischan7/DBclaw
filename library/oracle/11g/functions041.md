# Oracle 11g - functions041
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions041.htm

# COVAR\_SAMP

Syntax

Purpose

`COVAR_SAMP` returns the sample covariance of a set of number pairs. You can use it as an aggregate or analytic function.

This function takes as arguments any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. Oracle determines the argument with the highest numeric precedence, implicitly converts the remaining arguments to that data type, and returns that data type.

Oracle Database applies the function to the set of (`expr1`, `expr2`) pairs after eliminating all pairs for which either `expr1` or `expr2` is null. Then Oracle makes the following computation:

```
(SUM(expr1 * expr2) - SUM(expr1) * SUM(expr2) / n) / (n-1)
```

where `n` is the number of (`expr1`, `expr2`) pairs where neither `expr1` nor `expr2` is null.

The function returns a value of type `NUMBER`. If the function is applied to an empty set, then it returns null.

Aggregate Example

Refer to the aggregate example for [COVAR\_POP](functions040.md#i1008854).

Analytic Example

Refer to the analytic example for [COVAR\_POP](functions040.md#i1008854).