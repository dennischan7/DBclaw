# Oracle 11g - functions025
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions025.htm

[Go to main content](#BEGIN)

65/522 

# CHARTOROWID

Syntax

Purpose

`CHARTOROWID` converts a value from `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2` data type to `ROWID` data type.

This function does not support `CLOB` data directly. However, `CLOB`s can be passed in as arguments through implicit data conversion.

Examples

The following example converts a character rowid representation to a rowid. (The actual rowid is different for each database instance.)

```
SELECT last_name
  FROM employees
  WHERE ROWID = CHARTOROWID('AAAFd1AAFAAAABSAA/');
 
LAST_NAME
-------------------------
Greene
```

Scripting on this page enhances content navigation, but does not change the content in any way.