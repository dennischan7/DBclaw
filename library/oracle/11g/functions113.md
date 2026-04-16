# Oracle 11g - functions113
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions113.htm

# NLSSORT

Syntax

Purpose

`NLSSORT` returns the string of bytes used to sort `char`.

Both `char` and `'nlsparam'` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, or `NVARCHAR2`.

The value of `'nlsparam'` can have the form

```
'NLS_SORT = sort'
```

where `sort` is a linguistic sort sequence (collation) or `BINARY`. If you omit `'nlsparam'`, then this function uses the default sort sequence for your session. If you specify `BINARY`, then this function returns `char`.

If you specify `'nlsparam'`, then you can append to the linguistic sort name the suffix `_ai` to request an accent-insensitive sort or `_ci` to request a case-insensitive sort. Refer to [Oracle Database Globalization Support Guide](../../server.112/e10729/ch5lingsort.md#NLSPG005) for more information on accent- and case-insensitive sorting.

The string returned, also known as the collation key, is of `RAW` data type. The length of the collation key resulting from a given `char` value for a given collation may exceed 2000 bytes, which is the maximum length of the `RAW` value returned by `NLSSORT`. In this case, `NLSSORT` calculates the collation key for a maximum prefix, or initial substring, of `char` so that the calculated result does not exceed 2000 bytes. For monolingual collations, for example `FRENCH`, the prefix length is typically 1000 characters. For multilingual collations, for example `GENERIC_M`, the prefix is typically 500 characters. The exact length may be lower or higher depending on the collation and the characters contained in `char`.

This behavior implies that two character values whose collation keys (`NLSSORT` results) are compared to find the linguistic ordering are considered equal if they do not differ in the prefix even though they may differ at some further character position. Because the `NLSSORT` function is used implicitly to find linguistic ordering for comparison conditions, the `BETWEEN` condition, the `IN` condition, `ORDER` `BY`, `GROUP` `BY`, and `COUNT`(`DISTINCT`), those operations may return results that are only approximate for long character values. This is a restriction of the current comparison architecture. Currently, the only way to guarantee precise linguistic comparison results is to not compare character values that are longer than 499 characters for monolingual collations and 249 characters for multilingual collations.

This function does not support `CLOB` data directly. However, `CLOB`s can be passed in as arguments through implicit data conversion.

Examples

This function can be used to specify sorting and comparison operations based on a linguistic sort sequence rather than on the binary value of a string. The following example creates a test table containing two values and shows how the values returned can be ordered by the `NLSSORT` function:

```
CREATE TABLE test (name VARCHAR2(15));
INSERT INTO test VALUES ('Gaardiner');
INSERT INTO test VALUES ('Gaberd');
INSERT INTO test VALUES ('Gaasten');

SELECT *
  FROM test
  ORDER BY name;

NAME
---------------
Gaardiner
Gaasten
Gaberd

SELECT *
  FROM test
  ORDER BY NLSSORT(name, 'NLS_SORT = XDanish');

NAME
---------------
Gaberd
Gaardiner
Gaasten
```

The following example shows how to use the `NLSSORT` function in comparison operations:

```
SELECT *
  FROM test
  WHERE name > 'Gaberd'
  ORDER BY name;

no rows selected

SELECT *
  FROM test
  WHERE NLSSORT(name, 'NLS_SORT = XDanish') > 
        NLSSORT('Gaberd', 'NLS_SORT = XDanish')
  ORDER BY name;

NAME
---------------
Gaardiner
Gaasten
```

If you frequently use `NLSSORT` in comparison operations with the same linguistic sort sequence, then consider this more efficient alternative: Set the `NLS_COMP` parameter (either for the database or for the current session) to `LINGUISTIC`, and set the `NLS_SORT` parameter for the session to the desired sort sequence. Oracle Database will use that sort sequence by default for all sorting and comparison operations during the current session:

```
ALTER SESSION SET NLS_COMP = 'LINGUISTIC';
ALTER SESSION SET NLS_SORT = 'XDanish';

SELECT *
  FROM test
  WHERE name > 'Gaberd'
  ORDER BY name;

NAME
---------------
Gaardiner
Gaasten
```