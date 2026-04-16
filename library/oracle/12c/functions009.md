# Oracle 12c - functions009
Source: https://docs.oracle.com/database/121/SQLRF/functions009.htm

[Go to main content](#BEGIN)

82/555 

# ABS

Syntax

Purpose

`ABS` returns the absolute value of `n`.

This function takes as an argument any numeric data type or any nonnumeric data type that can be implicitly converted to a numeric data type. The function returns the same data type as the numeric data type of the argument.

Examples

The following example returns the absolute value of -15:

```
SELECT ABS(-15) "Absolute"
  FROM DUAL;

  Absolute
----------
        15
```

Scripting on this page enhances content navigation, but does not change the content in any way.