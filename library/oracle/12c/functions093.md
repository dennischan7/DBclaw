# Oracle 12c - functions093
Source: https://docs.oracle.com/database/121/SQLRF/functions093.htm

# JSON\_VALUE

Note:

The

`JSON_VALUE`

function is available starting with Oracle Database 12

c

Release 1 (12.1.0.2).

Syntax

[JSON\_path\_expression](#CJAJDGGJ)::=

[object\_step](#CJAHGEGE)::=

[array\_step](#CJAICBIF)::=

[JSON\_value\_returning\_clause](#CJABADIE)::=

JSON\_value\_return\_type::=

[JSON\_value\_on\_error\_clause](#CJAHDAFG)::=

Purpose

`JSON_VALUE` finds a specified scalar JSON value in JSON data and returns it as a SQL value.

expr

Use this clause to specify the JSON data to be evaluated. For `expr`, specify an expression that evaluates to a text literal. If `expr` is a column, then the column must be of data type `VARCHAR2`, `CLOB`, or `BLOB`. If `expr` is null, then the function returns null.

If `expr` is not a text literal of well-formed JSON data using strict or lax syntax, then the function returns null by default. You can use the `JSON_value_on_error_clause` to override this default behavior. Refer to the [JSON\_value\_on\_error\_clause](#CJAHDAFG).

FORMAT JSON

You must specify `FORMAT` `JSON` if `expr` is a column of data type `BLOB`.

JSON\_path\_expression

Use this clause to specify a JSON path expression. The function uses the path expression to evaluate `expr` and find a scalar JSON value that matches, or satisfies, the path expression. The path expression must be a text literal.

The path expression must begin with a dollar sign (`$`), which represents the context item, that is, the expression specified by `expr`. The dollar sign is followed by zero or more steps, each of which can be an object step or an array step.

The function attempts to match the first step in the path expression to the context item. If the first step results in a match, then the function attempts to match the second step to the JSON value(s) that matched the first step. If the second step results in a match, then the function attempts to match the third step to the JSON value(s) that matched the second step, and so on. If the final step matches a scalar JSON value, then the function returns that value as a SQL value. A path expression that consists of a dollar sign followed by zero steps (`'$'`) matches the entire context item.

You can specify the `JSON_value_returning_clause` to control the data type and format of the returned SQL value. Refer to the [JSON\_value\_returning\_clause](#CJABADIE).

If any step in the path expression does not result in a match, or if the final step matches a nonscalar value, then the function returns null by default. You can use the `JSON_value_on_error_clause` to override this default behavior. Refer to the [JSON\_value\_on\_error\_clause](#CJAHDAFG).

object\_step Use this clause to specify an object step.

* Use `simple_name` or `complex_name` to specify a property name. If a member with that property name exists in the JSON object being evaluated, then the object step results in a match to the property value of that member. Otherwise, the object step does not result in a match. Both types of names are case-sensitive. Therefore, a match will result only if the alphabetic character cases match in the object step and the JSON data.

  A `simple_name` can contain only alphanumeric characters and must begin with an alphabetic character. A `complex_name` can contain only alphanumeric characters and spaces, and must begin with an alphanumeric character. A `complex_name` must be enclosed in double quotation marks.
* Use the asterisk wildcard symbol (`*`) to specify all property names. If the JSON object being evaluated contains at least one member, then the object step results in a match to the values of all members. Otherwise, the object step does not result in a match.

If you apply an object step to a JSON array, then the array is implicitly unwrapped and the elements of the array are evaluated using the object step. This is called JSON path expression relaxation. Refer to [Oracle XML DB Developer's Guide](../ADXDB/json.md#ADXDB6373) for more information.

If the JSON value being evaluated is not a JSON object, then the object step does not result in a match.

array\_step Use this clause to specify an array step.

* Use `integer` to specify the element at index `integer` in a JSON array. Use `integer` `TO` `integer` to specify the range of elements between the two index `integer` values, inclusive. If the specified elements exist in the JSON array being evaluated, then the array step results in a match to those elements. Otherwise, the array step does not result in a match. The first element in a JSON array has index 0.
* Use the asterisk wildcard symbol (`*`) to specify all elements in a JSON array. If the JSON array being evaluated contains at least one element, then the array step results in a match to all elements in the JSON array. Otherwise, the array step does not result in a match.

If the JSON data being evaluated is not a JSON array, then the data is implicitly wrapped in an array and then evaluated using the array step. This is called JSON path expression relaxation. Refer to [Oracle XML DB Developer's Guide](../ADXDB/json.md#ADXDB6373) for more information.

JSON\_value\_returning\_clause

Use this clause to specify the data type and format of the value returned by this function.

RETURNING Use the `RETURNING` clause to specify the data type of the return value. If you omit this clause, then `JSON_VALUE` returns a value of type `VARCHAR2(4000)`.

You can use `JSON_value_return_type` to specify the following data types:

* `VARCHAR2[(``size` `[BYTE,CHAR])]`

  If you specify this data type, then the scalar value returned by this function can be a character or number value. A number value will be implicitly converted to a `VARCHAR2`. When specifying the `VARCHAR2` data type elsewhere in SQL, you are required to specify a size. However, in this clause you can omit the size. In this case, `JSON_VALUE` returns a value of type `VARCHAR2(4000)`.

  Refer to ["VARCHAR2 Data Type"](sql_elements001.md#i45694) for more information.
* `NUMBER[(``precision` `[,` `scale``])]`

  If you specify this data type, then the scalar value returned by this function must be a number value.

  Refer to ["NUMBER Data Type"](sql_elements001.md#CHDHDHGB) for more information.

If the data type is not large enough to hold the return value, then this function returns null by default. You can use the `JSON_value_on_error_clause` to override this default behavior. Refer to the [JSON\_value\_on\_error\_clause](#CJAHDAFG).

ASCII Specify `ASCII` to automatically escape any non-ASCII Unicode characters in the return value, using standard ASCII Unicode escape sequences.

JSON\_value\_on\_error\_clause

Use this clause to specify the value returned by this function when any of the following errors occur:

* `expr` is not well-formed JSON data using strict or lax JSON syntax
* A nonscalar value or no match is found when the JSON data is evaluated using the JSON path expression
* The return value data type is not large enough to hold the return value

You can specify the following clauses:

* `NULL` `ON` `ERROR` - Returns null when an error occurs. This is the default.
* `ERROR` `ON` `ERROR` - Returns the appropriate Oracle error when an error occurs.
* `DEFAULT` `literal` `ON` `ERROR` - Returns `literal` when an error occurs. If the data type of the value returned by this function is `VARCHAR2`, then you must specify a text literal. If the data type is `NUMBER`, then you must specify a numeric literal.

Examples

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