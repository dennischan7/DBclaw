# Oracle 12c - functions137
Source: https://docs.oracle.com/database/121/SQLRF/functions137.htm

[Go to main content](#BEGIN)

210/555 

# ORA\_INVOKING\_USER

Syntax

Purpose

`ORA_INVOKING_USER` returns the name of the database user who invoked the current statement or view. This function takes into account the `BEQUEATH` property of intervening views referenced in the statement. If this function is invoked from within a definer's rights context, then it returns the name of the owner of the definer's rights object. If the invoking user is a Real Application Security user, then it returns user `XS$NULL`.

This function returns a `VARCHAR2` value.

Examples

The following example returns the name of the database user who invoked the statement:

```
SELECT ORA_INVOKING_USER FROM DUAL;
```

Scripting on this page enhances content navigation, but does not change the content in any way.