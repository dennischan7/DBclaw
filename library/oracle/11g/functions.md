# Oracle 11g - functions
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions.htm

[Go to main content](#BEGIN)

40/522

# 5 Functions

Functions are similar to operators in that they manipulate data items and return a result. Functions differ from operators in the format of their arguments. This format enables them to operate on zero, one, two, or more arguments:

```
function(argument, argument, ...)
```

A function without any arguments is similar to a pseudocolumn (refer to [Chapter 2, "Pseudocolumns"](pseudocolumns.md#g1020307)). However, a pseudocolumn typically returns a different value for each row in the result set, whereas a function without any arguments typically returns the same value for each row.

This chapter contains these sections:

Scripting on this page enhances content navigation, but does not change the content in any way.