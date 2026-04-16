# Oracle 11g - functions220
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions220.htm

[Go to main content](#BEGIN)

260/522 

# TRUNC (date)

Syntax

trunc\_date::=

Purpose

The `TRUNC` (date) function returns `date` with the time portion of the day truncated to the unit specified by the format model `fmt`. This function is not sensitive to the `NLS_CALENDAR` session parameter. It operates according to the rules of the Gregorian calendar. The value returned is always of data type `DATE`, even if you specify a different datetime data type for `date`. If you omit `fmt`, then the default format model '`DD`' is used and the value returned is `date` truncated to the day with a time of midnight. Refer to ["ROUND and TRUNC Date Functions"](functions255.md#i1002084) for the permitted format models to use in `fmt`.

Examples

The following example truncates a date:

```
SELECT TRUNC(TO_DATE('27-OCT-92','DD-MON-YY'), 'YEAR')
  "New Year" FROM DUAL;
 
New Year
---------
01-JAN-92
```

Scripting on this page enhances content navigation, but does not change the content in any way.