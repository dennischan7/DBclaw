# Oracle 12c - functions176
Source: https://docs.oracle.com/database/121/SQLRF/functions176.htm

[Go to main content](#BEGIN)

249/555 

# SESSIONTIMEZONE

Syntax

Purpose

`SESSIONTIMEZONE` returns the time zone of the current session. The return type is a time zone offset (a character type in the format `'[+|-]TZH:TZM'`) or a time zone region name, depending on how the user specified the session time zone value in the most recent `ALTER` `SESSION` statement.

Note:

The default client session time zone is an offset even if the client operating system uses a named time zone. If you want the default session time zone to use a named time zone, then set the

`ORA_SDTZ`

variable in the client environment to an Oracle time zone region name. Refer to

[Oracle Database Globalization Support Guide](../NLSPG/ch3globenv.md#NLSPG003)

for more information on this variable.

Examples

The following example returns the time zone of the current session:

```
SELECT SESSIONTIMEZONE FROM DUAL;

SESSION
-------
-08:00
```

Scripting on this page enhances content navigation, but does not change the content in any way.