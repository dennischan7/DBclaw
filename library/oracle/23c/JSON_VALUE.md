# Oracle 23c - JSON_VALUE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/JSON_VALUE.html

JSON\_value\_returning\_clause::=

JSON\_value\_return\_type::=

JSON\_value\_return\_object\_instance ::=

JSON\_value\_on\_error\_clause::=

JSON\_value\_on\_empty\_clause::=

JSON\_value\_on\_mismatch\_clause::=

SQL/JSON function `JSON_VALUE` selects JSON data and returns a SQL scalar or an instance of a user-defined SQL object type or SQL collection type (varray, nested table)

The first argument to `JSON_VALUE` `expr` is a SQL expression that returns an instance of a scalar SQL data type (that is, not an object or collection data type). A scalar value returned from`JSON_VALUE` can be of any of these data types: `BINARY_DOUBLE`, `BINARY_FLOAT`, `BOOLEAN`, `CHAR`, `CLOB`, `DATE`, `INTERVAL DAY TO SECOND`, `INTERVAL YEAR TO MONTH`, `NCHAR`, `NCLOB`, `NVARCHAR2`, `NUMBER`, `RAW1`, `SDO_GEOMETRY`, `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`, `VARCHAR2`, and `VECTOR`.

If `expr` is not a text literal of well-formed JSON data using strict or lax syntax, then the function returns null by default. You can use the `JSON_value_on_error_clause` to override this default behavior. Refer to the [JSON\_value\_on\_error\_clause](JSON_VALUE.md#GUID-C7F19D36-1E75-4CB2-AE67-ADFBAD23CBC2__CJAHDAFG).

You must specify `FORMAT` `JSON` if `expr` is a column of data type `BLOB`.

JSON\_basic\_path\_expression

Use this clause to specify a SQL/JSON path expression. The function uses the path expression to evaluate `expr` and find a scalar JSON value that matches, or satisfies, the path expression. The path expression must be a text literal. See [Oracle Database JSON Developer's Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADJSN-GUID-7B610884-39CD-4910-85E7-C251D342D879) for the full semantics of `JSON_basic_path_expression`.

JSON\_value\_returning\_clause

Use this clause to specify the data type and format of the value returned by this function.

RETURNING

Use the `RETURNING` clause to specify the data type of the return value. If you omit this clause, then `JSON_VALUE` returns a value of type `VARCHAR2(4000)`.

JSON\_value\_return\_type ::=

You can use `JSON_value_return_type` to specify the following data types:

* `VARCHAR2[(``size` `[BYTE,CHAR])]`

  If you specify this data type, then the scalar value returned by this function can be a character or number value. A number value will be implicitly converted to a `VARCHAR2`. When specifying the `VARCHAR2` data type elsewhere in SQL, you are required to specify a size. However, in this clause you can omit the size. In this case, `JSON_VALUE` returns a value of type `VARCHAR2(4000)`.

  Specify the optional `TRUNCATE` clause immediately after `VARCHAR2(N)` to truncate the return value to `N` characters, if the return value is greater than `N` characters.

  Notes on the `TRUNCATE` clause :

  + If the string value is too long, then `ORA-40478` is raised.
  + If `TRUNCATE` is present, and the return value is not a character type, then a compile time error is raised.
  + If `TRUNCATE` is present with `FORMAT JSON`, then the return value may contain data that is not syntactically correct JSON.
  + `TRUNCATE` does not work with `EXISTS`.
* `CLOB`

  Specify this data type to return a character large object containing single-byte or multi-byte characters.
* `NUMBER[(``precision` `[,` `scale``])]`

  If you specify this data type, then the scalar value returned by this function must be a number value. The scalar value returned can also be a JSON Boolean value. Note however, that returning `NUMBER` for a JSON Boolean value is deprecated.
* `DATE`

  If you specify this data type, then the scalar value returned by this function must be a character value that can be implicitly converted to a `DATE` data type. If the JSON input represents a date with a time component, specify `DATE PRESERVE` `TIME` to retain the time component. If you do not want to retain the time component, specify `DATE TRUNCATE` `TIME`.

  If you specify neither `PRESERVE TIME` nor `TRUNCATE TIME`, the time component is not preserved.
* `TIMESTAMP`

  If you specify this data type, then the scalar value returned by this function must be a character value that can be implicitly converted to a `TIMESTAMP` data type.
* `TIMESTAMP` `WITH` `TIME` `ZONE`

  If you specify this data type, then the scalar value returned by this function must be a character value that can be implicitly converted to a `TIMESTAMP` `WITH` `TIME` `ZONE` data type.
* `BOOLEAN`

  Specify `BOOLEAN` to return true, false, or unknown.
* `SDO_GEOMETRY`

  This data type is used for Oracle Spatial and Graph data. If you specify this data type, then `expr` must evaluate to a text literal containing GeoJSON data, which is a format for encoding geographic data in JSON. If you specify this data type, then the scalar value returned by this function must be an object of type `SDO_GEOMETRY`.
* JSON\_value\_return\_object\_instance

  If `JSON_VALUE` targets a JSON object, and you specify a user-defined SQL object type as the return type, then `JSON_VALUE` returns an instance of that object type in object\_type\_name.

  For examples see [Using JSON\_VALUE To Instantiate a User-Defined Object Type Instance](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADJSN-GUID-622170D8-7BAD-4F5F-86BF-C328451FC3BE) of the JSON Developer's Guide.

See Also:

* [SQL/JSON Function JSON\_VALUE](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADJSN-GUID-0565F0EE-5F13-44DD-8321-2AC142959215) for a conceptual understanding in the JSON Developer's Guide.
* Refer to "[Data Types](Data-Types.md#GUID-A3C0D836-BADB-44E5-A5D4-265BA5968483)" for more information on the preceding data types.
* If the data type is not large enough to hold the return value, then this function returns null by default. You can use the `JSON_value_on_error_clause` to override this default behavior. Refer to the [JSON\_value\_on\_error\_clause](JSON_VALUE.md#GUID-C7F19D36-1E75-4CB2-AE67-ADFBAD23CBC2__CJAHDAFG).

Specify `ASCII` to automatically escape any non-ASCII Unicode characters in the return value, using standard ASCII Unicode escape sequences.

JSON\_value\_on\_error\_clause

Use this clause to specify the value returned by this function when the following errors occur:

* `expr` is not well-formed JSON data using strict or lax JSON syntax
* A nonscalar value is found when the JSON data is evaluated using the SQL/JSON path expression
* No match is found when the JSON data is evaluated using the SQL/JSON path expression. You can override the behavior for this type of error by specifying the `JSON_value_on_empty_clause`.
* The return value data type is not large enough to hold the return value

You can specify the following clauses:

* `NULL` `ON` `ERROR` - Returns null when an error occurs. This is the default.
* `ERROR` `ON` `ERROR` - Returns the appropriate Oracle error when an error occurs.
* `DEFAULT` `literal` `ON` `ERROR` - Returns `literal` when an error occurs. The data type of `literal` must match the data type of the value returned by this function.

JSON\_value\_on\_empty\_clause

Use this clause to specify the value returned by this function if no match is found when the JSON data is evaluated using the SQL/JSON path expression. This clause allows you to specify a different outcome for this type of error than the outcome specified with the `JSON_value_on_error_clause`.

You can specify the following clauses:

* `NULL` `ON` `EMPTY` - Returns null when no match is found.
* `ERROR` `ON` `EMPTY` - Returns the appropriate Oracle error when no match is found.
* `DEFAULT` `literal` `ON` `EMPTY` - Returns `literal` when no match is found. The data type of `literal` must match the data type of the value returned by this function.

If you omit this clause, then the `JSON_value_on_error_clause` determines the value returned when no match is found.

JSON\_value\_on\_mismatch\_clause

The `JSON_value_on_mismatch_clause` applies when a type conversion fails, for example when you try to convert a JSON number to a SQL date.

If the return type of `JSON_VALUE` is a SQL scalar like `NUMBER` or `DATE` , then `ON MISMATCH` applies for all type conversion errors - no further specification is required. `ERROR` and `NULL` are valid options.

Example 1

```
select json_value( '{a:"cat"}','$.a.number()'  NULL ON EMPTY                                                 
 ERROR ON  MISMATCH  DEFAULT -1 ON ERROR ) from dual;
 ORA-01722: invalid number
```

If the return type is an object type, then `ON MISMATCH` can be further specified with `MISSING DATA`, `EXTRA DATA` and `TYPE ERROR`. You can use it generally to apply to all error cases, or you can use it case by case by specifying different `ON MISMATCH` clauses for each case.

Example 2

```
IGNORE ON MISMATCH (EXTRA DATA)
```

```
ERROR ON MISMATCH ( MISSING DATA, TYPE ERROR)
```

The option `IGNORE` is only valid when the return type is an object type.

The following query returns the value of the member with property name `a`. Because the `RETURNING` clause is not specified, the value is returned as a `VARCHAR2(4000)` data type:

```
SELECT JSON_VALUE('{a:100}', '$.a') AS value
  FROM DUAL;

VALUE
-----
100
```

The following query returns the value of the member with property name `a`. Because the `RETURNING` `NUMBER` clause is specified, the value is returned as a `NUMBER` data type:

```
SELECT JSON_VALUE('{a:100}', '$.a' RETURNING NUMBER) AS value
  FROM DUAL;

     VALUE
----------
       100
```

The following query returns the value of the member with property name `b`, which is in the value of the member with property name `a`:

```
SELECT JSON_VALUE('{a:{b:100}}', '$.a.b') AS value
  FROM DUAL;

VALUE
-----
100
```

The following query returns the value of the member with property name `d` in any object:

```
SELECT JSON_VALUE('{a:{b:100}, c:{d:200}, e:{f:300}}', '$.*.d') AS value
  FROM DUAL;

VALUE
-----
200
```

The following query returns the value of the first element in an array:

```
SELECT JSON_VALUE('[0, 1, 2, 3]', '$[0]') AS value
  FROM DUAL;

VALUE
-----
0
```

The following query returns the value of the third element in an array. The array is the value of the member with property name `a`.

```
SELECT JSON_VALUE('{a:[5, 10, 15, 20]}', '$.a[2]') AS value
  FROM DUAL;

VALUE
-----
15
```

The following query returns the value of the member with property name `a` in the second object in an array:

```
SELECT JSON_VALUE('[{a:100}, {a:200}, {a:300}]', '$[1].a') AS value
  FROM DUAL;

VALUE
-----
200
```

The following query returns the value of the member with property name `c` in any object in an array:

```
SELECT JSON_VALUE('[{a:100}, {b:200}, {c:300}]', '$[*].c') AS value
  FROM DUAL;

VALUE
-----
300
```

The following query attempts to return the value of the member that has property name `lastname`. However, such a member does not exist in the specified JSON data, resulting in no match. Because the `ON` `ERROR` clause is not specified, the statement uses the default `NULL` `ON` `ERROR` and returns null.

```
SELECT JSON_VALUE('{firstname:"John"}', '$.lastname') AS "Last Name"
  FROM DUAL;

Last Name
---------
```

The following query results in an error because it attempts to return the value of the member with property name `lastname`, which does not exist in the specified JSON. Because the `ON` `ERROR` clause is specified, the statement returns the specified text literal.

```
SELECT JSON_VALUE('{firstname:"John"}', '$.lastname'
                  DEFAULT 'No last name found' ON ERROR) AS "Last Name"
  FROM DUAL;

Last Name
---------
No last name found
```