# Oracle 12c - functions056
Source: https://docs.oracle.com/database/121/SQLRF/functions056.htm

[Go to main content](#BEGIN)

129/555 

# DBTIMEZONE

Syntax

Purpose

`DBTIMEZONE` returns the value of the database time zone. The return type is a time zone offset (a character type in the format `'[+|-]TZH:TZM'`) or a time zone region name, depending on how the user specified the database time zone value in the most recent `CREATE` `DATABASE` or `ALTER` `DATABASE` statement.

Examples

The following example assumes that the database time zone is set to UTC time zone:

```
SELECT DBTIMEZONE
  FROM DUAL;

DBTIME
------
+00:00
```

Scripting on this page enhances content navigation, but does not change the content in any way.