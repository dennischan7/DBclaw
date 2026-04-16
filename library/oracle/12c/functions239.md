# Oracle 12c - functions239
Source: https://docs.oracle.com/database/121/SQLRF/functions239.htm

[Go to main content](#BEGIN)

312/555 

# UID

Syntax

Purpose

`UID` returns an integer that uniquely identifies the session user (the user who logged on).

See Also:

[USER](functions243.md#i79833)

to learn how Oracle Database determines the session user

Examples

The following example returns the UID of the session user:

```
SELECT UID FROM DUAL;
```

Scripting on this page enhances content navigation, but does not change the content in any way.