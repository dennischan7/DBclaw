# Oracle 11g - functions157
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions157.htm

[Go to main content](#BEGIN)

197/522 

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