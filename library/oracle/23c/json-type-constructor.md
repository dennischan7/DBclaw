# Oracle 23c - json-type-constructor
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/json-type-constructor.html

Purpose

The JSON data type constructor, JSON, takes as input a textual JSON value (a scalar, object, or array), parses it, and returns the value as an instance of JSON type. Alternatively, the input can be an instance of SQL type VECTOR, a user-defined PL/SQL type, or a SQL aggregate type.

You can use the JSON data type constructor `JSON` to parse textual JSON input ( a scalar, object, or array), and return it as an instance of type `JSON`.

Input values must pass the `IS JSON` test. Input values that fail the `IS JSON` test are rejected with a syntax error.

To filter out duplicate input values, you must run the `IS JSON (WITH UNIQUE KEYS)` check on the textual JSON input before using the `JSON`  constructor.

expr

The input in `expr` must be a syntactically valid textual representation of type `VARCHAR2`, `CLOB` and `BLOB`. It can also be a literal SQL string. A SQL `NULL` input value results in a JSON type instance of SQL `NULL`.