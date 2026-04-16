# Oracle 11g - functions110
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions110.htm

# NLS\_INITCAP

Syntax

Purpose

`NLS_INITCAP` returns `char`, with the first letter of each word in uppercase, all other letters in lowercase. Words are delimited by white space or characters that are not alphanumeric.

Both `char` and `'nlsparam'` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`. The string returned is of `VARCHAR2` data type and is in the same character set as `char`.

The value of `'nlsparam'` can have this form:

```
'NLS_SORT = sort'
```

where `sort` is either a linguistic sort sequence or `BINARY`. The linguistic sort sequence handles special linguistic requirements for case conversions. These requirements can result in a return value of a different length than the `char`. If you omit `'nlsparam'`, then this function uses the default sort sequence for your session.

This function does not support `CLOB` data directly. However, `CLOB`s can be passed in as arguments through implicit data conversion.

Examples

The following examples show how the linguistic sort sequence results in a different return value from the function:

```
SELECT NLS_INITCAP('ijsland') "InitCap"
  FROM DUAL;

InitCap
-------
Ijsland

SELECT NLS_INITCAP('ijsland', 'NLS_SORT = XDutch') "InitCap"
  FROM DUAL;

InitCap
-------
IJsland
```