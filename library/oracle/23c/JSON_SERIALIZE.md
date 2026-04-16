# Oracle 23c - JSON_SERIALIZE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/JSON_SERIALIZE.html

`json_serialize` takes JSON data of any SQL data type ( `BLOB`,`CLOB`, `JSON`, or `VARCHAR2` ) as input and returns a textual representation of it. You typically use it to transform the result of a query.

You can use `json_serialize` to convert binary JSON data to textual form (`CLOB` or `VARCHAR2`), or to transform textual JSON data by pretty-printing it or escaping non-ASCII Unicode characters in it.

When Oracle SQL function `vector_serialize` is applied to a JSON type instance, any non- standard Oracle scalar JSON value is returned as a standard JSON scalar value.

When you apply `vector_serialize` to a `VECTOR` type instance, it returns a textual JSON array of numbers.

Note:

You can serialize a `VECTOR` instance to a textual JSON array of numbers using SQL function `vector_serialize`. (Function json\_serialize serializes only JSON data.) See [VECTOR\_SERIALIZE](vector_serialize.md#GUID-9E3FFB34-F924-4C02-B35D-30B9FA1DA1A3 "VECTOR_SERIALIZE is synonymous with FROM_VECTOR.")

expr

`expr` is the input expression. Can be any one of type `JSON`, `VARCHAR2`, `CLOB`, or `BLOB`.

JSON\_returning\_clause::=

You can use the `JSON_returning_clause` to specify the return type of the function. One of `BOOLEAN`, `BLOB`, `CLOB`, `JSON`, or `VARCHAR2`.

The default return type is `VARCHAR2(4000)`.

If the return type is `RAW` or `BLOB`, it contains `UTF8` encoded JSON text.

PRETTY

Specify `PRETTY` if you want the result to be formatted for human readability.

ASCII

Specify `ASCII` if you want non-ASCII characters to be output using JSON escape sequences.

ORDERED

Specify `ORDERED` if you want to reorder key-value pairs alphabetically in ascending order. You can combine `ORDERED` with `PRETTY` and `ASCII`.

Example

```
SELECT JSON_SERIALIZE('{price:20, currency:" â¬"}' ASCII PRETTY ORDERED) from dual;
{
  "currency" : "\u20AC",
  "price" : 20
}
```

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