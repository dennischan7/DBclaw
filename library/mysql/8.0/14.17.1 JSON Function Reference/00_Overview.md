---
source: MySQL 8.0 Reference
title: 00_Overview
---

**Table 14.22 JSON Functions**

| Name                 | Description                                                                                                                           | Deprecated |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------|------------|
| ->                   | Return value from JSON column<br>after evaluating path; equivalent<br>to JSON_EXTRACT().                                              |            |
| ->>                  | Return value from JSON<br>column after evaluating<br>path and unquoting the<br>result; equivalent to<br>JSON_UNQUOTE(JSON_EXTRACT()). |            |
| JSON_ARRAY()         | Create JSON array                                                                                                                     |            |
| JSON_ARRAY_APPEND()  | Append data to JSON document                                                                                                          |            |
| JSON_ARRAY_INSERT()  | Insert into JSON array                                                                                                                |            |
| JSON_CONTAINS()      | Whether JSON document<br>contains specific object at path                                                                             |            |
| JSON_CONTAINS_PATH() | Whether JSON document<br>contains any data at path                                                                                    |            |
| JSON_DEPTH()         | Maximum depth of JSON<br>document                                                                                                     |            |
| JSON_EXTRACT()       | Return data from JSON<br>document                                                                                                     |            |
| JSON_INSERT()        | Insert data into JSON document                                                                                                        |            |
| JSON_KEYS()          | Array of keys from JSON<br>document                                                                                                   |            |
| JSON_LENGTH()        | Number of elements in JSON<br>document                                                                                                |            |
| JSON_MERGE()         | Merge JSON documents,<br>preserving duplicate keys.                                                                                   | Yes        |

| Name                  | Description                                                                                                                                                                                         | Deprecated |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
|                       | Deprecated synonym for<br>JSON_MERGE_PRESERVE()                                                                                                                                                     |            |
| JSON_MERGE_PATCH()    | Merge JSON documents,<br>replacing values of duplicate<br>keys                                                                                                                                      |            |
| JSON_MERGE_PRESERVE() | Merge JSON documents,<br>preserving duplicate keys                                                                                                                                                  |            |
| JSON_OBJECT()         | Create JSON object                                                                                                                                                                                  |            |
| JSON_OVERLAPS()       | Compares two JSON<br>documents, returns TRUE (1) if<br>these have any key-value pairs<br>or array elements in common,<br>otherwise FALSE (0)                                                        |            |
| JSON_PRETTY()         | Print a JSON document in<br>human-readable format                                                                                                                                                   |            |
| JSON_QUOTE()          | Quote JSON document                                                                                                                                                                                 |            |
| JSON_REMOVE()         | Remove data from JSON<br>document                                                                                                                                                                   |            |
| JSON_REPLACE()        | Replace values in JSON<br>document                                                                                                                                                                  |            |
| JSON_SCHEMA_VALID()   | Validate JSON document against<br>JSON schema; returns TRUE/1<br>if document validates against<br>schema, or FALSE/0 if it does<br>not                                                              |            |
|                       | JSON_SCHEMA_VALIDATION_REPORT() Validate JSON document against<br>JSON schema; returns report<br>in JSON format on outcome on<br>validation including success or<br>failure and reasons for failure |            |
| JSON_SEARCH()         | Path to value within JSON<br>document                                                                                                                                                               |            |
| JSON_SET()            | Insert data into JSON document                                                                                                                                                                      |            |
| JSON_STORAGE_FREE()   | Freed space within binary<br>representation of JSON column<br>value following partial update                                                                                                        |            |
| JSON_STORAGE_SIZE()   | Space used for storage of<br>binary representation of a JSON<br>document                                                                                                                            |            |
| JSON_TABLE()          | Return data from a JSON<br>expression as a relational table                                                                                                                                         |            |
| JSON_TYPE()           | Type of JSON value                                                                                                                                                                                  |            |
| JSON_UNQUOTE()        | Unquote JSON value                                                                                                                                                                                  |            |
| JSON_VALID()          | Whether JSON value is valid                                                                                                                                                                         |            |
| JSON_VALUE()          | Extract value from JSON<br>document at location pointed<br>to by path provided; return this<br>value as VARCHAR(512) or<br>specified type                                                           |            |

| Name        | Description                                                                                                                           | Deprecated |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------|------------|
| MEMBER OF() | Returns true (1) if first operand<br>matches any element of<br>JSON array passed as second<br>operand, otherwise returns false<br>(0) |            |

MySQL supports two aggregate JSON functions [JSON\\_ARRAYAGG\(\)](#page-186-0) and [JSON\\_OBJECTAGG\(\)](#page-187-0). See [Section 14.19, "Aggregate Functions",](#page-181-1) for descriptions of these.

MySQL also supports "pretty-printing" of JSON values in an easy-to-read format, using the [JSON\\_PRETTY\(\)](#page-159-0) function. You can see how much storage space a given JSON value takes up, and how much space remains for additional storage, using [JSON\\_STORAGE\\_SIZE\(\)](#page-162-0) and [JSON\\_STORAGE\\_FREE\(\)](#page-160-0), respectively. For complete descriptions of these functions, see [Section 14.17.8, "JSON Utility Functions".](#page-159-1)

## <span id="page-121-0"></span>**14.17.2 Functions That Create JSON Values**

The functions listed in this section compose JSON values from component elements.

• [JSON\\_ARRAY\(\[](#page-121-0)val[, val] ...])

Evaluates a (possibly empty) list of values and returns a JSON array containing those values.

```
mysql> SELECT JSON_ARRAY(1, "abc", NULL, TRUE, CURTIME());
+---------------------------------------------+
| JSON_ARRAY(1, "abc", NULL, TRUE, CURTIME()) |
+---------------------------------------------+
| [1, "abc", null, true, "11:30:24.000000"] |
+---------------------------------------------+
```

<span id="page-121-1"></span>• [JSON\\_OBJECT\(\[](#page-121-1)key, val[, key, val] ...])

Evaluates a (possibly empty) list of key-value pairs and returns a JSON object containing those pairs. An error occurs if any key name is NULL or the number of arguments is odd.

```
mysql> SELECT JSON_OBJECT('id', 87, 'name', 'carrot');
+-----------------------------------------+
| JSON_OBJECT('id', 87, 'name', 'carrot') |
+-----------------------------------------+
| {"id": 87, "name": "carrot"} |
+-----------------------------------------+
```

<span id="page-121-2"></span>• [JSON\\_QUOTE\(](#page-121-2)string)

Quotes a string as a JSON value by wrapping it with double quote characters and escaping interior quote and other characters, then returning the result as a utf8mb4 string. Returns NULL if the argument is NULL.

This function is typically used to produce a valid JSON string literal for inclusion within a JSON document.

Certain special characters are escaped with backslashes per the escape sequences shown in [Table 14.23, "JSON\\_UNQUOTE\(\) Special Character Escape Sequences"](#page-145-1).

```
mysql> SELECT JSON_QUOTE('null'), JSON_QUOTE('"null"');
+--------------------+----------------------+
| JSON_QUOTE('null') | JSON_QUOTE('"null"') |
+--------------------+----------------------+
| "null" | "\"null\"" |
+--------------------+----------------------+
mysql> SELECT JSON_QUOTE('[1, 2, 3]');
+-------------------------+
| JSON_QUOTE('[1, 2, 3]') |
+-------------------------+
```

```
| "[1, 2, 3]" |
+-------------------------+
```

You can also obtain JSON values by casting values of other types to the JSON type using CAST(value [AS JSON\)](#page-13-0); see Converting between JSON and non-JSON values, for more information.

Two aggregate functions generating JSON values are available. [JSON\\_ARRAYAGG\(\)](#page-186-0) returns a result set as a single JSON array, and [JSON\\_OBJECTAGG\(\)](#page-187-0) returns a result set as a single JSON object. For more information, see [Section 14.19, "Aggregate Functions"](#page-181-1).