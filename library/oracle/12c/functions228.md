# Oracle 12c - functions228
Source: https://docs.oracle.com/database/121/SQLRF/functions228.htm

[Go to main content](#BEGIN)

301/555 

# TO\_SINGLE\_BYTE

Syntax

Purpose

`TO_SINGLE_BYTE` returns `char` with all of its multibyte characters converted to their corresponding single-byte characters. `char` can be of data type `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`. The value returned is in the same data type as `char`.

Any multibyte characters in `char` that have no single-byte equivalents appear in the output as multibyte characters. This function is useful only if your database character set contains both single-byte and multibyte characters.

This function does not support `CLOB` data directly. However, `CLOB`s can be passed in as arguments through implicit data conversion.

Examples

The following example illustrates going from a multibyte `A` in UTF8 to a single byte ASCII `A`:

```
SELECT TO_SINGLE_BYTE( CHR(15711393)) FROM DUAL; 

T 
- 
A
```

Scripting on this page enhances content navigation, but does not change the content in any way.