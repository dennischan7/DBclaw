# Oracle 12c - functions138
Source: https://docs.oracle.com/database/121/SQLRF/functions138.htm

[Go to main content](#BEGIN)

211/555 

# ORA\_INVOKING\_USERID

Syntax

Purpose

`ORA_INVOKING_USERID` returns the identifier of the database user who invoked the current statement or view. This function takes into account the `BEQUEATH` property of intervening views referenced in the statement.

This function returns a `NUMBER` value.

Examples

The following example returns the identifier of the database user who invoked the statement:

```
SELECT ORA_INVOKING_USERID FROM DUAL;
```

Scripting on this page enhances content navigation, but does not change the content in any way.