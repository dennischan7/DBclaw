# Oracle 12c - functions171
Source: https://docs.oracle.com/database/121/SQLRF/functions171.htm

[Go to main content](#BEGIN)

244/555 

# ROWIDTOCHAR

Syntax

Purpose

`ROWIDTOCHAR` converts a rowid value to `VARCHAR2` data type. The result of this conversion is always 18 characters long.

Examples

The following example converts a rowid value in the `employees` table to a character value. (Results vary for each build of the sample database.)

```
SELECT ROWID FROM employees 
   WHERE ROWIDTOCHAR(ROWID) LIKE '%JAAB%'
   ORDER BY ROWID;

ROWID
------------------
AAAFfIAAFAAAABSAAb
```

Scripting on this page enhances content navigation, but does not change the content in any way.