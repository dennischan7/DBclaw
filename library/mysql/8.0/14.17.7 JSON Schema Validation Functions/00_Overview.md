---
source: MySQL 8.0 Reference
title: 00_Overview
---

Beginning with MySQL 8.0.17, MySQL supports validation of JSON documents against JSON schemas conforming to [Draft 4 of the JSON Schema specification.](https://json-schema.org/specification-links.md#draft-4) This can be done using either of the functions detailed in this section, both of which take two arguments, a JSON schema, and a JSON document which is validated against the schema. [JSON\\_SCHEMA\\_VALID\(\)](#page-154-0) returns true if the document validates against the schema, and false if it does not; [JSON\\_SCHEMA\\_VALIDATION\\_REPORT\(\)](#page-157-0) provides a report in JSON format on the validation.

Both functions handle null or invalid input as follows:

- If at least one of the arguments is NULL, the function returns NULL.
- If at least one of the arguments is not valid JSON, the function raises an error ([ER\\_INVALID\\_TYPE\\_FOR\\_JSON](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_type_for_json))
- In addition, if the schema is not a valid JSON object, the function returns [ER\\_INVALID\\_JSON\\_TYPE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_invalid_json_type).

MySQL supports the required attribute in JSON schemas to enforce the inclusion of required properties (see the examples in the function descriptions).

MySQL supports the id, \$schema, description, and type attributes in JSON schemas but does not require any of these.

MySQL does not support external resources in JSON schemas; using the \$ref keyword causes JSON\_SCHEMA\_VALID() to fail with [ER\\_NOT\\_SUPPORTED\\_YET](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_supported_yet).

![](_page_154_Picture_3.jpeg)

### **Note**

MySQL supports regular expression patterns in JSON schema, which supports but silently ignores invalid patterns (see the description of JSON\_SCHEMA\_VALID() for an example).

These functions are described in detail in the following list:

<span id="page-154-0"></span>• [JSON\\_SCHEMA\\_VALID\(](#page-154-0)schema,document)

Validates a JSON document against a JSON schema. Both schema and document are required. The schema must be a valid JSON object; the document must be a valid JSON document. Provided that these conditions are met: If the document validates against the schema, the function returns true (1); otherwise, it returns false (0).

In this example, we set a user variable @schema to the value of a JSON schema for geographical coordinates, and another one @document to the value of a JSON document containing one such coordinate. We then verify that @document validates according to @schema by using them as the arguments to JSON\_SCHEMA\_VALID():

```
mysql> SET @schema = '{
 '> "id": "http://json-schema.org/geo",
 '> "$schema": "http://json-schema.org/draft-04/schema#",
 '> "description": "A geographical coordinate",
 '> "type": "object",
 '> "properties": {
 '> "latitude": {
 '> "type": "number",
 '> "minimum": -90,
 '> "maximum": 90
 '> },
 '> "longitude": {
 '> "type": "number",
 '> "minimum": -180,
 '> "maximum": 180
 '> }
 '> },
 '> "required": ["latitude", "longitude"]
 '>}';
Query OK, 0 rows affected (0.01 sec)
mysql> SET @document = '{
 '> "latitude": 63.444697,
 '> "longitude": 10.445118
 '>}';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_SCHEMA_VALID(@schema, @document);
+---------------------------------------+
| JSON_SCHEMA_VALID(@schema, @document) |
+---------------------------------------+
| 1 |
+---------------------------------------+
1 row in set (0.00 sec)
```

Since @schema contains the required attribute, we can set @document to a value that is otherwise valid but does not contain the required properties, then test it against @schema, like this:

```
mysql> SET @document = '{}';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_SCHEMA_VALID(@schema, @document);
```

```
+---------------------------------------+
| JSON_SCHEMA_VALID(@schema, @document) |
+---------------------------------------+
| 0 |
+---------------------------------------+
1 row in set (0.00 sec)
```

If we now set the value of @schema to the same JSON schema but without the required attribute, @document validates because it is a valid JSON object, even though it contains no properties, as shown here:

```
mysql> SET @schema = '{
 '> "id": "http://json-schema.org/geo",
 '> "$schema": "http://json-schema.org/draft-04/schema#",
 '> "description": "A geographical coordinate",
 '> "type": "object",
 '> "properties": {
 '> "latitude": {
 '> "type": "number",
 '> "minimum": -90,
 '> "maximum": 90
 '> },
 '> "longitude": {
 '> "type": "number",
 '> "minimum": -180,
 '> "maximum": 180
 '> }
 '> }
 '>}';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_SCHEMA_VALID(@schema, @document);
+---------------------------------------+
| JSON_SCHEMA_VALID(@schema, @document) |
+---------------------------------------+
| 1 |
+---------------------------------------+
1 row in set (0.00 sec)
```

**JSON\_SCHEMA\_VALID() and CHECK constraints.** JSON\_SCHEMA\_VALID() can also be used to enforce CHECK constraints.

Consider the table geo created as shown here, with a JSON column coordinate representing a point of latitude and longitude on a map, governed by the JSON schema used as an argument in a JSON\_SCHEMA\_VALID() call which is passed as the expression for a CHECK constraint on this table:

```
mysql> CREATE TABLE geo (
 -> coordinate JSON,
 -> CHECK(
 -> JSON_SCHEMA_VALID(
 -> '{
 '> "type":"object",
 '> "properties":{
 '> "latitude":{"type":"number", "minimum":-90, "maximum":90},
 '> "longitude":{"type":"number", "minimum":-180, "maximum":180}
 '> },
 '> "required": ["latitude", "longitude"]
 '> }',
 -> coordinate
 -> )
 -> )
 -> );
```

Query OK, 0 rows affected (0.45 sec)

![](_page_156_Picture_2.jpeg)

### **Note**

Because a MySQL CHECK constraint cannot contain references to variables, you must pass the JSON schema to JSON\_SCHEMA\_VALID() inline when using it to specify such a constraint for a table.

We assign JSON values representing coordinates to three variables, as shown here:

```
mysql> SET @point1 = '{"latitude":59, "longitude":18}';
Query OK, 0 rows affected (0.00 sec)
mysql> SET @point2 = '{"latitude":91, "longitude":0}';
Query OK, 0 rows affected (0.00 sec)
mysql> SET @point3 = '{"longitude":120}';
Query OK, 0 rows affected (0.00 sec)
```

The first of these values is valid, as can be seen in the following INSERT statement:

```
mysql> INSERT INTO geo VALUES(@point1);
Query OK, 1 row affected (0.05 sec)
```

The second JSON value is invalid and so fails the constraint, as shown here:

```
mysql> INSERT INTO geo VALUES(@point2);
ERROR 3819 (HY000): Check constraint 'geo_chk_1' is violated.
```

In MySQL 8.0.19 and later, you can obtain precise information about the nature of the failure—in this case, that the latitude value exceeds the maximum defined in the schema—by issuing a SHOW WARNINGS statement:

```
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Error
 Code: 3934
Message: The JSON document location '#/latitude' failed requirement 'maximum' at
JSON Schema location '#/properties/latitude'.
*************************** 2. row ***************************
 Level: Error
 Code: 3819
Message: Check constraint 'geo_chk_1' is violated.
2 rows in set (0.00 sec)
```

The third coordinate value defined above is also invalid, since it is missing the required latitude property. As before, you can see this by attempting to insert the value into the geo table, then issuing SHOW WARNINGS afterwards:

```
mysql> INSERT INTO geo VALUES(@point3);
ERROR 3819 (HY000): Check constraint 'geo_chk_1' is violated.
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Error
 Code: 3934
Message: The JSON document location '#' failed requirement 'required' at JSON
Schema location '#'.
*************************** 2. row ***************************
 Level: Error
 Code: 3819
Message: Check constraint 'geo_chk_1' is violated.
2 rows in set (0.00 sec)
```

See Section 15.1.20.6, "CHECK Constraints", for more information.

JSON Schema has support for specifying regular expression patterns for strings, but the implementation used by MySQL silently ignores invalid patterns. This means that JSON\_SCHEMA\_VALID() can return true even when a regular expression pattern is invalid, as shown here:

```
mysql> SELECT JSON_SCHEMA_VALID('{"type":"string","pattern":"("}', '"abc"');
+---------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type":"string","pattern":"("}', '"abc"') |
+---------------------------------------------------------------+
| 1 |
+---------------------------------------------------------------+
1 row in set (0.04 sec)
```

<span id="page-157-0"></span>• [JSON\\_SCHEMA\\_VALIDATION\\_REPORT\(](#page-157-0)schema,document)

Validates a JSON document against a JSON schema. Both schema and document are required. As with JSON\_VALID\_SCHEMA(), the schema must be a valid JSON object, and the document must be a valid JSON document. Provided that these conditions are met, the function returns a report, as a JSON document, on the outcome of the validation. If the JSON document is considered valid according to the JSON Schema, the function returns a JSON object with one property valid having the value "true". If the JSON document fails validation, the function returns a JSON object which includes the properties listed here:

- valid: Always "false" for a failed schema validation
- reason: A human-readable string containing the reason for the failure
- schema-location: A JSON pointer URI fragment identifier indicating where in the JSON schema the validation failed (see Note following this list)
- document-location: A JSON pointer URI fragment identifier indicating where in the JSON document the validation failed (see Note following this list)
- schema-failed-keyword: A string containing the name of the keyword or property in the JSON schema that was violated

![](_page_157_Picture_10.jpeg)

### **Note**

JSON pointer URI fragment identifiers are defined in [RFC 6901 - JavaScript](https://tools.ietf.org/html/rfc6901#page-5) [Object Notation \(JSON\) Pointer.](https://tools.ietf.org/html/rfc6901#page-5) (These are not the same as the JSON path notation used by [JSON\\_EXTRACT\(\)](#page-123-1) and other MySQL JSON functions.) In this notation, # represents the entire document, and #/myprop represents the portion of the document included in the top-level property named myprop. See the specification just cited and the examples shown later in this section for more information.

In this example, we set a user variable @schema to the value of a JSON schema for geographical coordinates, and another one @document to the value of a JSON document containing one such coordinate. We then verify that @document validates according to @schema by using them as the arguments to JSON\_SCHEMA\_VALIDATION\_REORT():

```
mysql> SET @schema = '{
 '> "id": "http://json-schema.org/geo",
 '> "$schema": "http://json-schema.org/draft-04/schema#",
 '> "description": "A geographical coordinate",
 '> "type": "object",
 '> "properties": {
 '> "latitude": {
 '> "type": "number",
 '> "minimum": -90,
 '> "maximum": 90
 '> },
 '> "longitude": {
 '> "type": "number",
 '> "minimum": -180,
 '> "maximum": 180
 '> }
```

```
 '> },
 '> "required": ["latitude", "longitude"]
 '>}';
Query OK, 0 rows affected (0.01 sec)
mysql> SET @document = '{
 '> "latitude": 63.444697,
 '> "longitude": 10.445118
 '>}';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_SCHEMA_VALIDATION_REPORT(@schema, @document);
+---------------------------------------------------+
| JSON_SCHEMA_VALIDATION_REPORT(@schema, @document) |
+---------------------------------------------------+
| {"valid": true} |
+---------------------------------------------------+
1 row in set (0.00 sec)
```

Now we set @document such that it specifies an illegal value for one of its properties, like this:

```
mysql> SET @document = '{
 '> "latitude": 63.444697,
 '> "longitude": 310.445118
 '> }';
```

Validation of @document now fails when tested with JSON\_SCHEMA\_VALIDATION\_REPORT(). The output from the function call contains detailed information about the failure (with the function wrapped by [JSON\\_PRETTY\(\)](#page-159-0) to provide better formatting), as shown here:

```
mysql> SELECT JSON_PRETTY(JSON_SCHEMA_VALIDATION_REPORT(@schema, @document))\G
*************************** 1. row ***************************
JSON_PRETTY(JSON_SCHEMA_VALIDATION_REPORT(@schema, @document)): {
 "valid": false,
 "reason": "The JSON document location '#/longitude' failed requirement 'maximum' at JSON Schema location '#/properties/longitude'",
 "schema-location": "#/properties/longitude",
 "document-location": "#/longitude",
 "schema-failed-keyword": "maximum"
}
1 row in set (0.00 sec)
```

Since @schema contains the required attribute, we can set @document to a value that is otherwise valid but does not contain the required properties, then test it against @schema. The output of JSON\_SCHEMA\_VALIDATION\_REPORT() shows that validation fails due to lack of a required element, like this:

```
mysql> SET @document = '{}';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_PRETTY(JSON_SCHEMA_VALIDATION_REPORT(@schema, @document))\G
*************************** 1. row ***************************
JSON_PRETTY(JSON_SCHEMA_VALIDATION_REPORT(@schema, @document)): {
 "valid": false,
 "reason": "The JSON document location '#' failed requirement 'required' at JSON Schema location '#'",
 "schema-location": "#",
 "document-location": "#",
 "schema-failed-keyword": "required"
}
1 row in set (0.00 sec)
```

If we now set the value of @schema to the same JSON schema but without the required attribute, @document validates because it is a valid JSON object, even though it contains no properties, as shown here:

```
mysql> SET @schema = '{
 '> "id": "http://json-schema.org/geo",
 '> "$schema": "http://json-schema.org/draft-04/schema#",
 '> "description": "A geographical coordinate",
 '> "type": "object",
```

```
 '> "properties": {
 '> "latitude": {
 '> "type": "number",
 '> "minimum": -90,
 '> "maximum": 90
 '> },
 '> "longitude": {
 '> "type": "number",
 '> "minimum": -180,
 '> "maximum": 180
 '> }
 '> }
 '>}';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT JSON_SCHEMA_VALIDATION_REPORT(@schema, @document);
+---------------------------------------------------+
| JSON_SCHEMA_VALIDATION_REPORT(@schema, @document) |
+---------------------------------------------------+
| {"valid": true} |
+---------------------------------------------------+
1 row in set (0.00 sec)
```

# <span id="page-159-1"></span>**14.17.8 JSON Utility Functions**

This section documents utility functions that act on JSON values, or strings that can be parsed as JSON values. [JSON\\_PRETTY\(\)](#page-159-0) prints out a JSON value in a format that is easy to read. [JSON\\_STORAGE\\_SIZE\(\)](#page-162-0) and [JSON\\_STORAGE\\_FREE\(\)](#page-160-0) show, respectively, the amount of storage space used by a given JSON value and the amount of space remaining in a JSON column following a partial update.

<span id="page-159-0"></span>• [JSON\\_PRETTY\(](#page-159-0)json\_val)

Provides pretty-printing of JSON values similar to that implemented in PHP and by other languages and database systems. The value supplied must be a JSON value or a valid string representation of a JSON value. Extraneous whitespaces and newlines present in this value have no effect on the output. For a NULL value, the function returns NULL. If the value is not a JSON document, or if it cannot be parsed as one, the function fails with an error.

Formatting of the output from this function adheres to the following rules:

- Each array element or object member appears on a separate line, indented by one additional level as compared to its parent.
- Each level of indentation adds two leading spaces.
- A comma separating individual array elements or object members is printed before the newline that separates the two elements or members.
- The key and the value of an object member are separated by a colon followed by a space (': ').
- An empty object or array is printed on a single line. No space is printed between the opening and closing brace.
- Special characters in string scalars and key names are escaped employing the same rules used by the [JSON\\_QUOTE\(\)](#page-121-2) function.

```
mysql> SELECT JSON_PRETTY('123'); # scalar
+--------------------+
| JSON_PRETTY('123') |
+--------------------+
| 123 |
+--------------------+
mysql> SELECT JSON_PRETTY("[1,3,5]"); # array
+------------------------+
```

```
| JSON_PRETTY("[1,3,5]") |
+------------------------+
| [
 1,
 3,
 5
] |
+------------------------+
mysql> SELECT JSON_PRETTY('{"a":"10","b":"15","x":"25"}'); # object
+---------------------------------------------+
| JSON_PRETTY('{"a":"10","b":"15","x":"25"}') |
+---------------------------------------------+
| {
 "a": "10",
 "b": "15",
 "x": "25"
} |
+---------------------------------------------+
mysql> SELECT JSON_PRETTY('["a",1,{"key1":
 '> "value1"},"5", "77" ,
 '> {"key2":["value3","valueX",
 '> "valueY"]},"j", "2" ]')\G # nested arrays and objects
*************************** 1. row ***************************
JSON_PRETTY('["a",1,{"key1":
 "value1"},"5", "77" ,
 {"key2":["value3","valuex",
 "valuey"]},"j", "2" ]'): [
 "a",
 1,
 {
 "key1": "value1"
 },
 "5",
 "77",
 {
 "key2": [
 "value3",
 "valuex",
 "valuey"
 ]
 },
 "j",
 "2"
]
```

### <span id="page-160-0"></span>• [JSON\\_STORAGE\\_FREE\(](#page-160-0)json\_val)

For a JSON column value, this function shows how much storage space was freed in its binary representation after it was updated in place using [JSON\\_SET\(\)](#page-144-0), [JSON\\_REPLACE\(\)](#page-143-1), or [JSON\\_REMOVE\(\)](#page-143-0). The argument can also be a valid JSON document or a string which can be parsed as one—either as a literal value or as the value of a user variable—in which case the function returns 0. It returns a positive, nonzero value if the argument is a JSON column value which has been updated as described previously, such that its binary representation takes up less space than it did prior to the update. For a JSON column which has been updated such that its binary representation is the same as or larger than before, or if the update was not able to take advantage of a partial update, it returns 0; it returns NULL if the argument is NULL.

If json\_val is not NULL, and neither is a valid JSON document nor can be successfully parsed as one, an error results.

In this example, we create a table containing a JSON column, then insert a row containing a JSON object:

```
mysql> CREATE TABLE jtable (jcol JSON);
Query OK, 0 rows affected (0.38 sec)
mysql> INSERT INTO jtable VALUES
```

```
 -> ('{"a": 10, "b": "wxyz", "c": "[true, false]"}');
Query OK, 1 row affected (0.04 sec)
mysql> SELECT * FROM jtable;
+----------------------------------------------+
| jcol |
+----------------------------------------------+
| {"a": 10, "b": "wxyz", "c": "[true, false]"} |
+----------------------------------------------+
1 row in set (0.00 sec)
```

Now we update the column value using JSON\_SET() such that a partial update can be performed; in this case, we replace the value pointed to by the c key (the array [true, false]) with one that takes up less space (the integer 1):

```
mysql> UPDATE jtable
 -> SET jcol = JSON_SET(jcol, "$.a", 10, "$.b", "wxyz", "$.c", 1);
Query OK, 1 row affected (0.03 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT * FROM jtable;
+--------------------------------+
| jcol |
+--------------------------------+
| {"a": 10, "b": "wxyz", "c": 1} |
+--------------------------------+
1 row in set (0.00 sec)
mysql> SELECT JSON_STORAGE_FREE(jcol) FROM jtable;
+-------------------------+
| JSON_STORAGE_FREE(jcol) |
+-------------------------+
| 14 |
+-------------------------+
1 row in set (0.00 sec)
```

The effects of successive partial updates on this free space are cumulative, as shown in this example using JSON\_SET() to reduce the space taken up by the value having key b (and making no other changes):

```
mysql> UPDATE jtable
 -> SET jcol = JSON_SET(jcol, "$.a", 10, "$.b", "wx", "$.c", 1);
Query OK, 1 row affected (0.03 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT JSON_STORAGE_FREE(jcol) FROM jtable;
+-------------------------+
| JSON_STORAGE_FREE(jcol) |
+-------------------------+
| 16 |
+-------------------------+
1 row in set (0.00 sec)
```

Updating the column without using JSON\_SET(), JSON\_REPLACE(), or JSON\_REMOVE() means that the optimizer cannot perform the update in place; in this case, JSON\_STORAGE\_FREE() returns 0, as shown here:

```
mysql> UPDATE jtable SET jcol = '{"a": 10, "b": 1}';
Query OK, 1 row affected (0.05 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT JSON_STORAGE_FREE(jcol) FROM jtable;
+-------------------------+
| JSON_STORAGE_FREE(jcol) |
+-------------------------+
| 0 |
+-------------------------+
```

```
1 row in set (0.00 sec)
```

Partial updates of JSON documents can be performed only on column values. For a user variable that stores a JSON value, the value is always completely replaced, even when the update is performed using JSON\_SET():

```
mysql> SET @j = '{"a": 10, "b": "wxyz", "c": "[true, false]"}';
Query OK, 0 rows affected (0.00 sec)
mysql> SET @j = JSON_SET(@j, '$.a', 10, '$.b', 'wxyz', '$.c', '1');
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @j, JSON_STORAGE_FREE(@j) AS Free;
+----------------------------------+------+
| @j | Free |
+----------------------------------+------+
| {"a": 10, "b": "wxyz", "c": "1"} | 0 |
+----------------------------------+------+
1 row in set (0.00 sec)
```

For a JSON literal, this function always returns 0:

```
mysql> SELECT JSON_STORAGE_FREE('{"a": 10, "b": "wxyz", "c": "1"}') AS Free;
+------+
| Free |
+------+
| 0 |
+------+
1 row in set (0.00 sec)
```

<span id="page-162-0"></span>• [JSON\\_STORAGE\\_SIZE\(](#page-162-0)json\_val)

This function returns the number of bytes used to store the binary representation of a JSON document. When the argument is a JSON column, this is the space used to store the JSON document as it was inserted into the column, prior to any partial updates that may have been performed on it afterwards. json\_val must be a valid JSON document or a string which can be parsed as one. In the case where it is string, the function returns the amount of storage space in the JSON binary representation that is created by parsing the string as JSON and converting it to binary. It returns NULL if the argument is NULL.

An error results when json\_val is not NULL, and is not—or cannot be successfully parsed as—a JSON document.

To illustrate this function's behavior when used with a JSON column as its argument, we create a table named jtable containing a JSON column jcol, insert a JSON value into the table, then obtain the storage space used by this column with JSON\_STORAGE\_SIZE(), as shown here:

```
mysql> CREATE TABLE jtable (jcol JSON);
Query OK, 0 rows affected (0.42 sec)
mysql> INSERT INTO jtable VALUES
 -> ('{"a": 1000, "b": "wxyz", "c": "[1, 3, 5, 7]"}');
Query OK, 1 row affected (0.04 sec)
mysql> SELECT
 -> jcol,
 -> JSON_STORAGE_SIZE(jcol) AS Size,
 -> JSON_STORAGE_FREE(jcol) AS Free
 -> FROM jtable;
+-----------------------------------------------+------+------+
| jcol | Size | Free |
+-----------------------------------------------+------+------+
| {"a": 1000, "b": "wxyz", "c": "[1, 3, 5, 7]"} | 47 | 0 |
+-----------------------------------------------+------+------+
```

```
1 row in set (0.00 sec)
```

According to the output of JSON\_STORAGE\_SIZE(), the JSON document inserted into the column takes up 47 bytes. We also checked the amount of space freed by any previous partial updates of the column using [JSON\\_STORAGE\\_FREE\(\)](#page-160-0); since no updates have yet been performed, this is 0, as expected.

Next we perform an UPDATE on the table that should result in a partial update of the document stored in jcol, and then test the result as shown here:

```
mysql> UPDATE jtable SET jcol = 
 -> JSON_SET(jcol, "$.b", "a");
Query OK, 1 row affected (0.04 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT
 -> jcol,
 -> JSON_STORAGE_SIZE(jcol) AS Size,
 -> JSON_STORAGE_FREE(jcol) AS Free
 -> FROM jtable;
+--------------------------------------------+------+------+
| jcol | Size | Free |
+--------------------------------------------+------+------+
| {"a": 1000, "b": "a", "c": "[1, 3, 5, 7]"} | 47 | 3 |
+--------------------------------------------+------+------+
1 row in set (0.00 sec)
```

The value returned by JSON\_STORAGE\_FREE() in the previous query indicates that a partial update of the JSON document was performed, and that this freed 3 bytes of space used to store it. The result returned by JSON\_STORAGE\_SIZE() is unchanged by the partial update.

Partial updates are supported for updates using [JSON\\_SET\(\)](#page-144-0), [JSON\\_REPLACE\(\)](#page-143-1), or [JSON\\_REMOVE\(\)](#page-143-0). The direct assignment of a value to a JSON column cannot be partially updated; following such an update, JSON\_STORAGE\_SIZE() always shows the storage used for the newlyset value:

```
mysql> UPDATE jtable
mysql> SET jcol = '{"a": 4.55, "b": "wxyz", "c": "[true, false]"}';
Query OK, 1 row affected (0.04 sec)
Rows matched: 1 Changed: 1 Warnings: 0
mysql> SELECT
 -> jcol,
 -> JSON_STORAGE_SIZE(jcol) AS Size,
 -> JSON_STORAGE_FREE(jcol) AS Free
 -> FROM jtable;
+------------------------------------------------+------+------+
| jcol | Size | Free |
+------------------------------------------------+------+------+
| {"a": 4.55, "b": "wxyz", "c": "[true, false]"} | 56 | 0 |
+------------------------------------------------+------+------+
1 row in set (0.00 sec)
```

A JSON user variable cannot be partially updated. This means that this function always shows the space currently used to store a JSON document in a user variable:

```
mysql> SET @j = '[100, "sakila", [1, 3, 5], 425.05]';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @j, JSON_STORAGE_SIZE(@j) AS Size;
+------------------------------------+------+
| @j | Size |
+------------------------------------+------+
| [100, "sakila", [1, 3, 5], 425.05] | 45 |
+------------------------------------+------+
1 row in set (0.00 sec)
mysql> SET @j = JSON_SET(@j, '$[1]', "json");
```

```
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @j, JSON_STORAGE_SIZE(@j) AS Size;
+----------------------------------+------+
| @j | Size |
+----------------------------------+------+
| [100, "json", [1, 3, 5], 425.05] | 43 |
+----------------------------------+------+
1 row in set (0.00 sec)
mysql> SET @j = JSON_SET(@j, '$[2][0]', JSON_ARRAY(10, 20, 30));
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @j, JSON_STORAGE_SIZE(@j) AS Size;
+---------------------------------------------+------+
| @j | Size |
+---------------------------------------------+------+
| [100, "json", [[10, 20, 30], 3, 5], 425.05] | 56 |
+---------------------------------------------+------+
1 row in set (0.00 sec)
```

For a JSON literal, this function always returns the current storage space used:

```
mysql> SELECT
 -> JSON_STORAGE_SIZE('[100, "sakila", [1, 3, 5], 425.05]') AS A,
 -> JSON_STORAGE_SIZE('{"a": 1000, "b": "a", "c": "[1, 3, 5, 7]"}') AS B,
 -> JSON_STORAGE_SIZE('{"a": 1000, "b": "wxyz", "c": "[1, 3, 5, 7]"}') AS C,
 -> JSON_STORAGE_SIZE('[100, "json", [[10, 20, 30], 3, 5], 425.05]') AS D;
+----+----+----+----+
| A | B | C | D |
+----+----+----+----+
| 45 | 44 | 47 | 56 |
+----+----+----+----+
1 row in set (0.00 sec)
```