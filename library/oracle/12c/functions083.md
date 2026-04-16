# Oracle 12c - functions083
Source: https://docs.oracle.com/database/121/SQLRF/functions083.htm

# INITCAP

Syntax

Purpose

`INITCAP` returns `char`, with the first letter of each word in uppercase, all other letters in lowercase. Words are delimited by white space or characters that are not alphanumeric.

`char` can be of any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`. The return value is the same data type as `char`. The database sets the case of the initial characters based on the binary mapping defined for the underlying character set. For linguistic-sensitive uppercase and lowercase, refer to [NLS\_INITCAP](functions122.md#i89841).

This function does not support `CLOB` data directly. However, `CLOB`s can be passed in as arguments through implicit data conversion.

Examples

The following example capitalizes each word in the string:

```
SELECT INITCAP('the soap') "Capitals"
  FROM DUAL; 

Capitals
---------
The Soap
```