# Oracle 23c - json_scalar
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/json_scalar.html

Purpose

`JSON_SCALAR` accepts a SQL scalar value as input and returns a corresponding JSON scalar value as a `JSON` type instance. The value can be an Oracle-specific JSON-language type, such as a date, which is not part of the JSON standard.

To use `JSON_SCALAR` you must set the database initialization parameter `compatible` is at least `20`. Otherwise it raises an error.

The argument to `JSON_SCALAR` can be an instance of any of these SQL data types: `BINARY_DOUBLE`, `BINARY_FLOAT`, `BLOB`, `CLOB`, `DATE`, `INTERVAL YEAR TO MONTH`, `INTERVAL DAY TO SECOND`, `JSON`, `NUMBER`, `RAW`, `TIMESTAMP`, `VARCHAR`, `VARCHAR2`, or `VECTOR`.

The returned `JSON` type instance is a JSON-language scalar value supported by Oracle.

If the argument to `JSON_SCALAR` is a SQL NULL value, then you can obtain a return value as follows:

* SQL `NULL`, the default behavior
* JSON `null`, using keywords `NULL ON NULL`
* An empty JSON string, " ", using keywords `EMPTY STRING ON NULL`

The default behavior of returning SQL `NULL` is the only exception to the rule that a JSON scalar value is returned.