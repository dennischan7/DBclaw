# Oracle 12c - functions220
Source: https://docs.oracle.com/database/121/SQLRF/functions220.htm

# TO\_DSINTERVAL

Syntax

sql\_format::=

ds\_iso\_format::=

Note:

In earlier releases, the

`TO_DSINTERVAL`

function accepted an optional

`nlsparam`

clause. This clause is still accepted for backward compatibility, but has no effect.

Purpose

`TO_DSINTERVAL` converts a character string of `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type to an `INTERVAL` `DAY` `TO` `SECOND` type.

`TO_DSINTERVAL` accepts argument in one of the two formats:

In the SQL format, `days` is an integer between 0 and 999999999, `hours` is an integer between 0 and 23, and `minutes` and `seconds` are integers between 0 and 59. `frac_secs` is the fractional part of seconds between .0 and .999999999. One or more blanks separate days from hours. Additional blanks are allowed between format elements.

In the ISO format, `days`, `hours`, `minutes` and `seconds` are integers between 0 and 999999999. `frac_secs` is the fractional part of seconds between .0 and .999999999. No blanks are allowed in the value. If you specify `T`, then you must specify at least one of the `hours`, `minutes`, or `seconds` values.

Examples

The following example uses the SQL format to select from the `hr.employees` table the employees who had worked for the company for at least 100 days on November 1, 2002:

```
SELECT employee_id, last_name FROM employees
   WHERE hire_date + TO_DSINTERVAL('100 00:00:00')
   <= DATE '2002-11-01'
   ORDER BY employee_id;

EMPLOYEE_ID LAST_NAME
----------- ---------------
        102 De Haan
        203 Mavris
        204 Baer
        205 Higgins
        206 Giet
```

The following example uses the ISO format to display the timestamp 100 days and 5 hours after the beginning of the year 2009:

```
SELECT TO_CHAR(TIMESTAMP '2009-01-01 00:00:00' + TO_DSINTERVAL('P100DT05H'),
   'YYYY-MM-DD HH24:MI:SS') "Time Stamp"
     FROM DUAL;

Time Stamp
-------------------
2009-04-11 05:00:00
```