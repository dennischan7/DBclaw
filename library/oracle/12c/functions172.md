# Oracle 12c - functions172
Source: https://docs.oracle.com/database/121/SQLRF/functions172.htm

[Go to main content](#BEGIN)

245/555 

# ROWIDTONCHAR

Syntax

Purpose

`ROWIDTONCHAR` converts a rowid value to `NVARCHAR2` data type. The result of this conversion is always in the national character set and is 18 characters long.

Examples

The following example converts a rowid value to an `NVARCHAR2` string:

```
SELECT LENGTHB( ROWIDTONCHAR(ROWID) ) Length, ROWIDTONCHAR(ROWID) 
   FROM employees
   ORDER BY length; 

    LENGTH ROWIDTONCHAR(ROWID
---------- ------------------
        36 AAAL52AAFAAAABSABD
        36 AAAL52AAFAAAABSABV
. . .
```

Scripting on this page enhances content navigation, but does not change the content in any way.