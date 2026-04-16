# Oracle 11g - functions143
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions143.htm

[Go to main content](#BEGIN)

183/522 

# RAWTOHEX

Syntax

Purpose

`RAWTOHEX` converts `raw` to a character value containing its hexadecimal representation.

As a SQL built-in function, `RAWTOHEX` accepts an argument of any scalar data type other than `LONG`, `LONG` `RAW`, `CLOB`, `BLOB`, or `BFILE`. It returns a `VARCHAR2` value with the hexadecimal representation of bytes that make up the value of `raw`. Each byte is represented by two hexadecimal digits.

Examples

The following hypothetical example returns the hexadecimal equivalent of a `RAW` column value:

```
SELECT RAWTOHEX(raw_column) "Graphics"
   FROM graphics;

Graphics
--------
7D
```

Scripting on this page enhances content navigation, but does not change the content in any way.