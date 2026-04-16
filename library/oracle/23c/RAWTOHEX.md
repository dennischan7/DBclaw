# Oracle 23c - RAWTOHEX
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/RAWTOHEX.html

`RAWTOHEX` converts `raw` to a character value containing its hexadecimal representation.

As a SQL built-in function, `RAWTOHEX` accepts an argument of any scalar data type other than `LONG`, `LONG` `RAW`, `CLOB`, `NCLOB`, `BLOB`, or `BFILE`. If the argument is of a data type other than `RAW`, then this function converts the argument value, which is represented using some number of data bytes, into a `RAW` value with the same number of data bytes. The data itself is not modified in any way, but the data type is recast to a `RAW` data type.

This function returns a `VARCHAR2` value with the hexadecimal representation of bytes that make up the value of `raw`. Each byte is represented by two hexadecimal digits.