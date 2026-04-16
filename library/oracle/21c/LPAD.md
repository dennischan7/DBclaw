# Oracle 21c - LPAD
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/LPAD.html

`LPAD` returns `expr1`, left-padded to length `n` characters with the sequence of characters in `expr2`. This function is useful for formatting the output of a query.

Both `expr1` and `expr2` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. The string returned is of `VARCHAR2` data type if `expr1` is a character data type, `NVARCHAR2` if `expr1` is a national character data type, and a LOB if `expr1` is a LOB data type. The string returned is in the same character set as `expr1`. The argument `n` must be a `NUMBER` integer or a value that can be implicitly converted to a `NUMBER` integer.

If you do not specify `expr2`, then the default is a single blank. If `expr1` is longer than `n`, then this function returns the portion of `expr1` that fits in `n`.

The argument `n` is the total length of the return value as it is displayed on your terminal screen. In most character sets, this is also the number of characters in the return value. However, in some multibyte character sets, the display length of a character string can differ from the number of characters in the string.

The following example left-pads a string with the asterisk (\*) and period (.) characters:

```
SELECT LPAD('Page 1',15,'*.') "LPAD example"
  FROM DUAL;

LPAD example
---------------
*.*.*.*.*Page 1
```