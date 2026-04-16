# Oracle 12c - functions
Source: https://docs.oracle.com/database/121/SQLRF/functions.htm

[Go to main content](#BEGIN)

73/555

# 7 Functions

Functions are similar to operators in that they manipulate data items and return a result. Functions differ from operators in the format of their arguments. This format enables them to operate on zero, one, two, or more arguments:

```
function(argument, argument, ...)
```

A function without any arguments is similar to a pseudocolumn (refer to [Chapter 3, "Pseudocolumns"](pseudocolumns.md#g1020307)). However, a pseudocolumn typically returns a different value for each row in the result set, whereas a function without any arguments typically returns the same value for each row.

This chapter contains these sections:

Scripting on this page enhances content navigation, but does not change the content in any way.