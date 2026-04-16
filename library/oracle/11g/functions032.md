# Oracle 11g - functions032
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions032.htm

# COMPOSE

Syntax

Purpose

`COMPOSE` takes as its argument a string, or an expression that resolves to a string, in any data type, and returns a Unicode string in the same character set as the input. `char` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. For example, an `o` code point qualified by an umlaut code point will be returned as the o-umlaut code point.

`COMPOSE` returns the string in NFC normal form. For a more exclusive setting, you can first call `DECOMPOSE` with the `CANONICAL` setting and then `COMPOSE`. This combination returns the string in NFKC normal form.

`CLOB` and `NCLOB` values are supported through implicit conversion. If `char` is a character LOB value, then it is converted to a `VARCHAR` value before the `COMPOSE` operation. The operation will fail if the size of the LOB value exceeds the supported length of the `VARCHAR` in the particular development environment.

Examples

The following example returns the o-umlaut code point:

```
SELECT COMPOSE( 'o' || UNISTR('\0308') )
  FROM DUAL; 

CO 
-- 
ö
```