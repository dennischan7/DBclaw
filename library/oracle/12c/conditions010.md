# Oracle 12c - conditions010
Source: https://docs.oracle.com/database/121/SQLRF/conditions010.htm

# JSON Conditions

JavaScript Object Notation (JSON) conditions allow you to test JSON data as follows:

JSON\_condition::=

Note:

The JSON conditions are available starting with Oracle Database 12

c

Release 1 (12.1.0.2).

## IS JSON Condition

Use this condition to test whether an expression is syntactically correct, or well-formed, JSON data.

* If you specify `IS` `JSON`, then this condition returns `TRUE` if the expression is well-formed JSON data and `FALSE` if the expression is not well-formed JSON data.
* If you specify `IS` `NOT` `JSON`, then this condition returns `TRUE` if the expression is not well-formed JSON data and `FALSE` if the expression is well-formed JSON data.

is\_JSON\_condition::=

* Use `expr` to specify the JSON data to be evaluated. Specify an expression that evaluates to a text literal. If `expr` is a column, then the column must be of data type `VARCHAR2`, `CLOB`, or `BLOB`. If `expr` evaluates to null or a text literal of length zero, then this condition returns `UNKNOWN`.
* You must specify `FORMAT` `JSON` if `expr` is a column of data type `BLOB`.
* If you specify `STRICT`, then this condition considers only strict JSON syntax to be well-formed JSON data. If you specify `LAX`, then this condition also considers lax JSON syntax to be well-formed JSON data. The default is `LAX`. Refer to [Oracle XML DB Developer's Guide](../ADXDB/json.md#ADXDB6259) for more information on strict and lax JSON syntax.
* If you specify `WITH` `UNIQUE` `KEYS`, then this condition considers JSON data to be well-formed only if key names are unique within each object. If you specify `WITHOUT` `UNIQUE` `KEYS`, then this condition considers JSON data to be well-formed even if duplicate key names occur within an object. A `WITHOUT` `UNIQUE` `KEYS` test performs faster than a `WITH` `UNIQUE` `KEYS` test. The default is `WITHOUT` `UNIQUE` `KEYS`.

Examples

Testing for STRICT or LAX JSON Syntax: Example The following statement creates table `t` with column `col1`:

```
CREATE TABLE t (col1 VARCHAR2(100));
```

The following statements insert values into column `col1` of table `t`:

```
INSERT INTO t VALUES ( '[ "LIT192", "CS141", "HIS160" ]' );
INSERT INTO t VALUES ( '{ "Name": "John" }' );
INSERT INTO t VALUES ( '{ "Grade Values" : { A : 4.0, B : 3.0, C : 2.0 } }');
INSERT INTO t VALUES ( '{ "isEnrolled" : true }' );
INSERT INTO t VALUES ( '{ "isMatriculated" : False }' );
INSERT INTO t VALUES (NULL);
INSERT INTO t VALUES ('This is not well-formed JSON data');
```

The following statement queries table `t` and returns `col1` values that are well-formed JSON data. Because neither the `STRICT` nor `LAX` keyword is specified, this example uses the default `LAX` setting. Therefore, this query returns values that use strict or lax JSON syntax.

```
SELECT col1
  FROM t
  WHERE col1 IS JSON;

COL1
--------------------------------------------------
[ "LIT192", "CS141", "HIS160" ]
{ "Name": "John" }
{ "Grade Values" : { A : 4.0, B : 3.0, C : 2.0 } }
{ "isEnrolled" : true }
{ "isMatriculated" : False }
```

The following statement queries table `t` and returns `col1` values that are well-formed JSON data. This example specifies the `STRICT` setting. Therefore, this query returns only values that use strict JSON syntax.

```
SELECT col1
  FROM t
  WHERE col1 IS JSON STRICT;

COL1
--------------------------------------------------
[ "LIT192", "CS141", "HIS160" ]
{ "Name": "John" }
{ "isEnrolled" : true }
```

The following statement queries table `t` and returns `col1` values that use lax JSON syntax, but omits `col1` values that use strict JSON syntax. Therefore, this query returns only values that contain the exceptions allowed in lax JSON syntax.

```
SELECT col1
  FROM t
  WHERE col1 IS NOT JSON STRICT AND col1 IS JSON LAX;

COL1
--------------------------------------------------
{ "Grade Values" : { A : 4.0, B : 3.0, C : 2.0 } }
{ "isMatriculated" : False }
```

Testing for Unique Keys: Example The following statement creates table `t` with column `col1`:

```
CREATE TABLE t (col1 VARCHAR2(100));
```

The following statements insert values into column `col1` of table `t`:

```
INSERT INTO t VALUES ('{a:100, b:200, c:300}');
INSERT INTO t VALUES ('{a:100, a:200, b:300}');
INSERT INTO t VALUES ('{a:100, b : {a:100, c:300}}');
```

The following statement queries table t and returns `col1` values that are well-formed JSON data with unique key names within each object:

```
SELECT col1 FROM t
  WHERE col1 IS JSON WITH UNIQUE KEYS;

COL1
---------------------------
{a:100, b:200, c:300}
{a:100, b : {a:100, c:300}}
```

The second row is returned because, while the key name `a` appears twice, it is in two different objects.

The following statement queries table `t` and returns `col1` values that are well-formed JSON data, regardless of whether there are unique key names within each object:

```
SELECT col1 FROM t
  WHERE col1 IS JSON WITHOUT UNIQUE KEYS;

COL1
---------------------------
{a:100, b:200, c:300}
{a:100, a:200, b:300}
{a:100, b : {a:100, c:300}}
```

Using IS JSON as a Check Constraint: Example The following statement creates table `j_purchaseorder`, which will store JSON data in column `po_document`. The statement uses the `IS` `JSON` condition as a check constraint to ensure that only well-formed JSON is stored in column `po_document`.

```
CREATE TABLE j_purchaseorder
  (id RAW (16) NOT NULL,
   date_loaded TIMESTAMP(6) WITH TIME ZONE,
   po_document CLOB CONSTRAINT ensure_json CHECK (po_document IS JSON));
```

## JSON\_EXISTS Condition

Use the `JSON_EXISTS` condition to test whether a specified JSON value exists in JSON data. This condition returns `TRUE` if the JSON value exists and `FALSE` if the JSON value does not exist.

JSON\_exists\_condition::=

[JSON\_path\_expression](#BABGHIIC)::=

[object\_step](#BABDFEAC)::=

[array\_step](#BABHCAHC)::=

[JSON\_exists\_on\_error\_clause](#BABHJEDF)::=

expr

Use this clause to specify the JSON data to be evaluated. For `expr`, specify an expression that evaluates to a text literal. If `expr` is a column, then the column must be of data type `VARCHAR2`, `CLOB`, or `BLOB`. If `expr` evaluates to null or a text literal of length zero, then the condition returns `UNKNOWN`.

If `expr` is not a text literal of well-formed JSON data using strict or lax syntax, then the condition returns `FALSE` by default. You can use the `JSON_exists_on_error_clause` to override this default behavior. Refer to the [JSON\_exists\_on\_error\_clause](#BABHJEDF).

FORMAT JSON

You must specify `FORMAT` `JSON` if `expr` is a column of data type `BLOB`.

JSON\_path\_expression

Use this clause to specify a JSON path expression. The condition uses the path expression to evaluate `expr` and determine if a JSON value that matches, or satisfies, the path expression exists. The path expression must be a text literal.

The path expression must begin with a dollar sign (`$`), which represents the context item, that is, the expression specified by `expr`. The dollar sign is followed by zero or more steps, each of which can be an object step or an array step. The condition attempts to match the first step in the path expression to the context item. If the first step results in a match, then the condition attempts to match the second step to the JSON value(s) that matched the first step. If the second step results in a match, then the condition attempts to match the third step to the JSON value(s) that matched the second step, and so on. If the final step results in a match, then the condition returns `TRUE`. If any step in the path expression does not result in a match, then the condition returns `FALSE`. A path expression that consists of a dollar sign followed by zero steps (`'$'`) matches the entire context item.

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

JSON\_exists\_on\_error\_clause

Use this clause to specify the value returned by this condition when `expr` is not well-formed JSON data.

You can specify the following clauses:

* `ERROR` `ON` `ERROR` - Returns the appropriate Oracle error when `expr` is not well-formed JSON data.
* `TRUE` `ON` `ERROR` - Returns `TRUE` when `expr` is not well-formed JSON data.
* `FALSE` `ON` `ERROR` - Returns `FALSE` when `expr` is not well-formed JSON data. This is the default.

Examples

The following statement creates table `t` with column `name`:

```
CREATE TABLE t (name VARCHAR2(100));
```

The following statements insert values into column `name` of table `t`:

```
INSERT INTO t VALUES ('[{first:"John"}, {middle:"Mark"}, {last:"Smith"}]');
INSERT INTO t VALUES ('[{first:"Mary"}, {last:"Jones"}]');
INSERT INTO t VALUES ('[{first:"Jeff"}, {last:"Williams"}]');
INSERT INTO t VALUES ('[{first:"Jean"}, {middle:"Anne"}, {last:"Brown"}]');
INSERT INTO t VALUES (NULL);
INSERT INTO t VALUES ('This is not well-formed JSON data');
```

The following statement queries column `name` in table `t` and returns JSON data that consists of an array whose first element is an object with property name `first`. The `ON` `ERROR` clause is not specified. Therefore, the `JSON_EXISTS` condition returns `FALSE` for values that are not well-formed JSON data.

```
SELECT name FROM t
  WHERE JSON_EXISTS(name, '$[0].first');

NAME
--------------------------------------------------
[{first:"John"}, {middle:"Mark"}, {last:"Smith"}]
[{first:"Mary"}, {last:"Jones"}]
[{first:"Jeff"}, {last:"Williams"}]
[{first:"Jean"}, {middle:"Anne"}, {last:"Brown"}]
```

The following statement queries column `name` in table `t` and returns JSON data that consists of an array whose second element is an object with property name `middle`. The `ON` `ERROR` clause is not specified. Therefore, the `JSON_EXISTS` condition returns `FALSE` for values that are not well-formed JSON data.

```
SELECT name FROM t
  WHERE JSON_EXISTS(name, '$[1].middle');

NAME
--------------------------------------------------------------------------------
[{first:"John"}, {middle:"Mark"}, {last:"Smith"}]
[{first:"Jean"}, {middle:"Anne"}, {last:"Brown"}]
```

The following statement is similar to the previous statement, except that the `TRUE` `ON` `ERROR` clause is specified. Therefore, the `JSON_EXISTS` condition returns `TRUE` for values that are not well-formed JSON data.

```
SELECT name FROM t
  WHERE JSON_EXISTS(name, '$[1].middle' TRUE ON ERROR);

NAME
--------------------------------------------------------------------------------
[{first:"John"}, {middle:"Mark"}, {last:"Smith"}]
[{first:"Jean"}, {middle:"Anne"}, {last:"Brown"}]
This is not well-formed JSON data
```

The following statement queries column `name` in table `t` and returns JSON data that consists of an array that contains an element that is an object with property name `last`. The wildcard symbol (`*`) is specified for the array index. Therefore, the query returns arrays that contain such an object, regardless of its index number in the array.

```
SELECT name FROM t
  WHERE JSON_EXISTS(name, '$[*].last');

NAME
--------------------------------------------------
[{first:"John"}, {middle:"Mark"}, {last:"Smith"}]
[{first:"Mary"}, {last:"Jones"}]
[{first:"Jeff"}, {last:"Williams"}]
[{first:"Jean"}, {middle:"Anne"}, {last:"Brown"}]
```

## JSON\_TEXTCONTAINS Condition

Use the `JSON_TEXTCONTAINS` condition to test whether a specified character string exists in JSON property values. You can use this condition to filter JSON data on a specific word or number.

This condition takes the following arguments:

* A table or view column that contains JSON data. A JSON search index, which is an Oracle Text index designed specifically for use with JSON data, must be defined on the column. Each row of JSON data in the column is referred to as a JSON document.
* A JSON path expression. The path expression is applied to each JSON document in an attempt to match a specific JSON object within the document. The path expression can contain only JSON object steps; it cannot contain JSON array steps.
* A character string. The condition searches for the character string in all of the string and numeric property values in the matched JSON object, including array values. The string must exist as a separate word in the property value. For example, if you search for 'beth', then a match will be found for string property value "beth smith", but not for "elizabeth smith". If you search for '10', then a match will be found for numeric property value 10 or string property value "10 main street", but a match will not be found for numeric property value 110 or string property value "102 main street".

This condition returns `TRUE` if a match is found, and `FALSE` if a match is not found.

JSON\_textcontains\_condition::=

[JSON\_path\_expression](#BABCGGEF)::=

(`JSON_TEXTCONTAINS` does not support `array_step`)

[object\_step](#BABCDAFA)::=

column

Specify the name of the table or view column containing the JSON data to be tested. The column must be of data type `VARCHAR2`, `CLOB`, or `BLOB`. A JSON search index, which is an Oracle Text index designed specifically for use with JSON data, must be defined on the column. If a column value is a null or a text literal of length zero, then the condition returns `UNKNOWN`.

If a column value is not a text literal of well-formed JSON data using strict or lax syntax, then the condition returns `FALSE`.

JSON\_path\_expression

Use this clause to specify a JSON path expression. The condition uses the path expression to evaluate `column` and determine if a JSON value that matches, or satisfies, the path expression exists. The path expression must be a text literal.

The path expression must begin with a dollar sign (`$`), which represents the context item, that is, `column`. The dollar sign is followed by zero or more object steps.

The condition attempts to match the first step in the path expression to the context item. If the first step results in a match, then the condition attempts to match the second step to the JSON value(s) that matched the first step. If the second step results in a match, then the condition attempts to match the third step to the JSON value(s) that matched the second step, and so on. If any step in the path expression does not result in a match, then the condition returns `FALSE`. If the final step results in a match and the matched value contains `string`, then the condition returns `TRUE`. Otherwise, the condition returns `FALSE`.

A path expression that consists of a dollar sign followed by zero object steps (`'$'`) matches the entire context item.

object\_step Use this clause to specify an object step.

* Use `simple_name` or `complex_name` to specify a property name. If a member with that property name exists in the JSON object being evaluated, then the object step results in a match to the property value of that member. Otherwise, the object step does not result in a match. Both types of names are case-sensitive. Therefore, a match will result only if the alphabetic character cases match in the object step and the JSON data.

  A `simple_name` can contain only alphanumeric characters and must begin with an alphabetic character. A `complex_name` can contain only alphanumeric characters and spaces, and must begin with an alphanumeric character. A `complex_name` must be enclosed in double quotation marks.
* Use the asterisk wildcard symbol (`*`) to specify all property names. If the JSON object being evaluated contains at least one member, then the object step results in a match to the values of all members. Otherwise, the object step does not result in a match.

If you apply an object step to a JSON array, then the array is implicitly unwrapped and the elements of the array are evaluated using the object step. This is called JSON path expression relaxation. Refer to [Oracle XML DB Developer's Guide](../ADXDB/json.md#ADXDB6373) for more information.

If the JSON value being evaluated is not a JSON object, then the object step does not result in a match.

string

The condition searches for the character string specified by `string`. The string must be enclosed in single quotation marks.

Examples

The following statement creates table `families` with column `family_doc`:

```
CREATE TABLE families (family_doc VARCHAR2(200));
```

The following statement creates a JSON search index on column `family_doc`:

```
CREATE INDEX ix
  ON families(family_doc)
  INDEXTYPE IS CTXSYS.CONTEXT
  PARAMETERS ('SECTION GROUP CTXSYS.JSON_SECTION_GROUP SYNC (ON COMMIT)');
```

The following statements insert JSON documents that describe families into column `family_doc`:

```
INSERT INTO families
VALUES ('{family : {id:10, ages:[40,38,12], address : {street : "10 Main Street"}}}');

INSERT INTO families
VALUES ('{family : {id:11, ages:[42,40,10,5], address : {street : "200 East Street", apt : 20}}}');

INSERT INTO families
VALUES ('{family : {id:12, ages:[25,23], address : {street : "300 Oak Street", apt : 10}}}');
```

The following statement commits the transaction:

```
COMMIT;
```

The following query returns the JSON documents that contain `10` in any property value in the document:

```
SELECT family_doc FROM families
  WHERE JSON_TEXTCONTAINS(family_doc, '$', '10');

FAMILY_DOC
--------------------------------------------------------------------------------
{family : {id:10, ages:[40,38,12], address : {street : "10 Main Street"}}}
{family : {id:11, ages:[42,40,10,5], address : {street : "200 East Street", apt : 20}}}
{family : {id:12, ages:[25,23], address : {street : "300 Oak Street", apt : 10}}}
```

The following query returns the JSON documents that contain 10 in the `id` property value:

```
SELECT family_doc FROM families
  where json_textcontains(family_doc, '$.family.id', '10');

FAMILY_DOC
--------------------------------------------------------------------------------
{family : {id:10, ages:[40,38,12], address : {street : "10 Main Street"}}}
```

The following query returns the JSON documents that have a 10 in the array of values for the `ages` property:

```
SELECT family_doc FROM families
  WHERE JSON_TEXTCONTAINS(family_doc, '$.family.ages', '10');

FAMILY_DOC
--------------------------------------------------------------------------------
{family : {id:11, ages:[42,40,10,5], address : {street : "200 East Street", apt : 20}}}
```

The following query returns the JSON documents that have a 10 in the `address` property value:

```
SELECT family_doc FROM families
  WHERE JSON_TEXTCONTAINS(family_doc, '$.family.address', '10');

FAMILY_DOC
--------------------------------------------------------------------------------
{family : {id:10, ages:[40,38,12], address : {street : "10 Main Street"}}}
{family : {id:12, ages:[25,23], address : {street : "300 Oak Street", apt : 10}}}
```

The following query returns the JSON documents that have a 10 in the `apt` property value:

```
SELECT family_doc FROM families
  WHERE JSON_TEXTCONTAINS(family_doc, '$.family.address.apt', '10');

FAMILY_DOC
--------------------------------------------------------------------------------
{family : {id:12, ages:[25,23], address : {street : "300 Oak Street", apt : 10}}}
```