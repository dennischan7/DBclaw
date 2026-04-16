# Oracle 21c - JSON_SERIALIZE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/JSON_SERIALIZE.html

`json_serialize` takes JSON data of any SQL data type (`JSON`, `VARCHAR2`, `CLOB`, or `BLOB`) as input and returns a textual representation of it. You typically use it to transform the result of a query.

You can use `json_serialize` to convert binary JSON data to textual form (`CLOB` or `VARCHAR2`), or to transform textual JSON data by pretty-printing it or escaping non-ASCII Unicode characters in it.

expr

`expr` is the input expression. Can be any one of type `JSON`, `VARCHAR2`, `CLOB`, or `BLOB`.

JSON\_returning\_clause::=

You can use the `JSON_returning_clause` to specify the return type of the function. One of `VARCHAR2`, `CLOB`, or `BLOB`.

The default return type is `VARCHAR2(4000)`.

If the return type is `RAW` or `BLOB`, it contains `UTF8` encoded JSON text.

PRETTY

Specify `PRETTY` if you want the result to be formatted for human readability.

ASCII

Specify `ASCII` if you want non-ASCII characters to be output using JSON escape sequences.

TRUNCATE

Specify `TRUNCATE`, if you want the textual output in the result document to fit into the buffer of the specified return type .

JSON\_on\_error\_clause::=

Specify `JSON_on_error_clause` to control the handling of processing errors.

`ERROR ON ERROR` is the default.

`EMPTY ON ERROR` is not supported.

If you specify `TRUNCATE` with `JSON_on_error_clause`, then a value too large for the return type will be truncated to fit into the buffer instead of raising an error.

Example

```
SELECT JSON_SERIALIZE ('{a:[1,2,3,4]}' RETURNING VARCHAR2(3) TRUNCATE ERROR ON ERROR) from dual
–-------
{"a
```