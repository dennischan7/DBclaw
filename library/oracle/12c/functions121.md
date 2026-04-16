# Oracle 12c - functions121
Source: https://docs.oracle.com/database/121/SQLRF/functions121.htm

[Go to main content](#BEGIN)

194/555 

# NLS\_CHARSET\_NAME

Syntax

Purpose

`NLS_CHARSET_NAME` returns the name of the character set corresponding to ID number `number`. The character set name is returned as a `VARCHAR2` value in the database character set.

If `number` is not recognized as a valid character set ID, then this function returns null.

Examples

The following example returns the character set corresponding to character set ID number 2:

```
SELECT NLS_CHARSET_NAME(2)
  FROM DUAL;

NLS_CH 
------ 
WE8DEC
```

Scripting on this page enhances content navigation, but does not change the content in any way.