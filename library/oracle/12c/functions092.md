# Oracle 12c - functions092
Source: https://docs.oracle.com/database/121/SQLRF/functions092.htm

# JSON\_TABLE

Note:

The

`JSON_TABLE`

function is available starting with Oracle Database 12

c

Release 1 (12.1.0.2).

Syntax

([JSON\_path\_expression::=](#CJABACJA), [JSON\_table\_on\_error\_clause::=](#CJAGFDBA), [JSON\_columns\_clause::=](#CJAHEFGD))

[JSON\_path\_expression](functions091.md#CJAGCJHA)::=

[object\_step](functions091.md#CJADGEEA)::=

[array\_step](functions091.md#CJAIIJJC)::=

[JSON\_table\_on\_error\_clause](#CJABIHAJ)::=

[JSON\_columns\_clause](#CJAEAAHA)::=

JSON\_column\_definition::=

[JSON\_exists\_column](#CJAGEFIB)::=

(The syntax and semantics of these clauses are described in the `JSON_EXISTS` and `JSON_VALUE` documentation: [JSON\_value\_return\_type::=](functions093.md#CJABCIJE), [JSON\_path\_expression::=](#CJABACJA), [JSON\_exists\_on\_error\_clause::=](conditions010.md#BABGJJFD))

[JSON\_query\_column](#CJAGFHCI)::=

(The syntax and semantics of these clauses are described in the `JSON_QUERY` documentation: [JSON\_query\_return\_type::=](functions091.md#CJADJIIJ), [JSON\_query\_wrapper\_clause::=](functions091.md#CJAGGHHG), [JSON\_path\_expression::=](functions091.md#CJAFCHID), [JSON\_query\_on\_error\_clause::=](functions091.md#CJACIDGJ))

[JSON\_value\_column](#CJAHAAFJ)::=

(The syntax and semantics of these clauses are described in the `JSON_VALUE` documentation: [JSON\_value\_return\_type::=](functions093.md#CJABCIJE), [JSON\_path\_expression::=](functions093.md#CJAIIDIE), [JSON\_value\_on\_error\_clause::=](functions093.md#CJAHCAIE))

[JSON\_nested\_path](#CJAGFIBD)::=

([JSON\_path\_expression::=](#CJABACJA), [JSON\_columns\_clause::=](#CJAHEFGD))

[ordinality\_column](#CJAGCABF)::=

Purpose

`JSON_TABLE` creates a relational view of JSON data. It maps the result of a JSON data evaluation into relational rows and columns. You can query the result returned by the function as a virtual relational table using SQL. The main purpose of `JSON_TABLE` is to create a row of relational data for each object inside a JSON array and output JSON values from within that object as individual SQL column values.

You can specify `JSON_TABLE` only in the `FROM` clause of a `SELECT` statement. The function first applies a JSON path expression, called a row path expression, to the supplied JSON data. The JSON value that matches the row path expression is called a row source in that it generates a row of relational data. The `COLUMNS` clause evaluates the row source, finds specific JSON values within the row source, and returns those JSON values as SQL values in individual columns of a row of relational data.

The `COLUMNS` clause enables you to search for JSON values in different ways by using the following clauses:

* `JSON_exists_column` - Evaluates JSON data in the same manner as the `JSON_EXISTS` condition, that is, determines if a specified JSON value exists, and returns either a `VARCHAR2` column of values '`true`' or '`false`', or a `NUMBER` column of values 1 or 0.
* `JSON_query_column` - Evaluates JSON data in the same manner as the `JSON_QUERY` function, that is, finds one or more specified JSON values, and returns a column of character strings that contain those JSON values.
* `JSON_value_column` - Evaluates JSON data in the same manner as the `JSON_VALUE` function, that is, finds a specified scalar JSON value, and returns a column of those JSON values as SQL values.
* `JSON_nested_path` - Allows you to flatten JSON values in a nested JSON object or JSON array into individual columns in a single row along with JSON values from the parent object or array. You can use this clause recursively to project data from multiple layers of nested objects or arrays into a single row.
* `ordinality_column` - Returns a column of generated row numbers.

The column definition clauses allow you to specify a name for each column of data that they return. You can reference these column names elsewhere in the `SELECT` statement, such as in the `SELECT` list and the `WHERE` clause.

expr

Use this clause to specify the JSON data to be evaluated. For `expr`, specify an expression that evaluates to a text literal. If `expr` is a column, then the column must be of data type `VARCHAR2`, `CLOB`, or `BLOB`. If `expr` is null, then the function returns null.

If `expr` is not a text literal of well-formed JSON data using strict or lax syntax, then the function returns null by default. You can use the `JSON_table_on_error_clause` to override this default behavior. Refer to [JSON\_table\_on\_error\_clause](#CJABIHAJ).

FORMAT JSON

You must specify `FORMAT` `JSON` if `expr` is a column of data type `BLOB`.

JSON\_path\_expression

Use this clause to specify the row path expression. The function uses the row path expression to evaluate `expr` and find the a JSON value, called the row source, that matches, or satisfy, the path expression. This row source is then evaluated by the `COLUMNS` clause. The path expression must be a text literal.

The `JSON_path_expression` clause has the same semantics for `JSON_TABLE` and `JSON_QUERY`. For the full semantics of this clause, refer to [JSON\_path\_expression](functions091.md#CJAGCJHA) in the documentation on `JSON_QUERY`.

JSON\_table\_on\_error\_clause

Use this clause to specify the value returned by this function when the following errors occur:

You can specify the following clauses:

* `NULL` `ON` `ERROR` - Returns null when an error occurs. This is the default.
* `ERROR` `ON` `ERROR` - Returns the appropriate Oracle error when an error occurs.
* `DEFAULT` `literal` `ON` `ERROR` - Returns `literal` when an error occurs. If the data type of the value returned by this function is `VARCHAR2`, then you must specify a text literal. If the data type is `NUMBER`, then you must specify a numeric literal.

JSON\_columns\_clause

Use the `COLUMNS` clause to define the columns in the virtual relational table returned by the `JSON_TABLE` function.

JSON\_exists\_column This clause evaluates JSON data in the same manner as the `JSON_EXISTS` condition, that is, it determines if a specified JSON value exists. It returns either a `VARCHAR2` column of values '`true`' or '`false`', or a `NUMBER` column of values 1 or 0. A value of '`true`' or 1 indicates that the JSON value exists and a value of '`false`' or 0 indicates that the JSON value does not exist.

You can use the `JSON_value_return_type` clause to control the data type of the returned column. If you omit this clause, then the data type is `VARCHAR2(4000)`. Use `column_name` to specify the name of the returned column. The rest of the clauses of `JSON_exists_column` have the same semantics here as they have for the `JSON_EXISTS` condition. For full information on these clauses, refer to ["JSON\_EXISTS Condition"](conditions010.md#BABHAGEG). Also see ["Using JSON\_exists\_column: Examples"](#CJAJGGJC) for an example.

JSON\_query\_column This clause evaluates JSON data in the same manner as the `JSON_QUERY` function, that is, it finds one or more specified JSON values, and returns a column of character strings that contain those JSON values.

Use `column_name` to specify the name of the returned column. The rest of the clauses of `JSON_query_column` have the same semantics here as they have for the `JSON_QUERY` function. For full information on these clauses, refer to [JSON\_QUERY](functions091.md#CJACGHBJ). Also see ["Using JSON\_query\_column: Example"](#CJAEJCEF) for an example.

JSON\_value\_column This clause evaluates JSON data in the same manner as the `JSON_VALUE` function, that is, it finds a specified scalar JSON value, and returns a column of those JSON values as SQL values.

Use `column_name` to specify the name of the returned column. The rest of the clauses of `JSON_value_column` have the same semantics here as they have for the `JSON_VALUE` function. For full information on these clauses, refer to [JSON\_VALUE](functions093.md#CJAGGCJH). Also see ["Using JSON\_value\_column: Example"](#CJAFACBH) for an example.

JSON\_nested\_path Use this clause to flatten JSON values in a nested JSON object or JSON array into individual columns in a single row along with JSON values from the parent object or array. You can use this clause recursively to project data from multiple layers of nested objects or arrays into a single row.

Specify the `JSON_path_expression` clause to match the nested object or array. This path expression is relative to the row path expression specified in the `JSON_TABLE` function.

Use the `COLUMNS` clause to define the columns of the nested object or array to be returned. This clause is recursive—you can specify the `JSON_nested_path` clause within another `JSON_nested_path` clause. Also see ["Using JSON\_nested\_path: Examples"](#CJAJAEJD) for an example.

ordinality\_column This clause returns a column of generated row numbers of data type `NUMBER`. You can specify at most one `ordinality_column`. Also see ["Using JSON\_value\_column: Example"](#CJAFACBH) for an example of using the `ordinality_column` clause.

Examples

Creating a Table That Contains a JSON Document: Example This example shows how to create and populate table `j_purchaseorder`, which is used in the rest of the `JSON_TABLE` examples in this section.

The following statement creates table `j_purchaseorder`. Column `po_document` is for storing JSON data and, therefore, has an `IS` `JSON` check constraint to ensure that only well-formed JSON is stored in the column.

```
CREATE TABLE j_purchaseorder
  (id RAW (16) NOT NULL,
   date_loaded TIMESTAMP(6) WITH TIME ZONE,
   po_document CLOB CONSTRAINT ensure_json CHECK (po_document IS JSON));
```

The following statement inserts one row, or one JSON document, into table `j_purchaseorder`:

```
INSERT INTO j_purchaseorder
  VALUES (
    SYS_GUID(),
    SYSTIMESTAMP,
    '{"PONumber"              : 1600,
      "Reference"             : "ABULL-20140421",
       "Requestor"            : "Alexis Bull",
       "User"                 : "ABULL",
       "CostCenter"           : "A50",
       "ShippingInstructions" : {"name"   : "Alexis Bull",
                                 "Address": {"street"   : "200 Sporting Green",
                                              "city"    : "South San Francisco",
                                              "state"   : "CA",
                                              "zipCode" : 99236,
                                              "country" : "United States of America"},
                                 "Phone" : [{"type" : "Office", "number" : "909-555-7307"},
                                            {"type" : "Mobile", "number" : "415-555-1234"}]},
       "Special Instructions" : null,
       "AllowPartialShipment" : true,
       "LineItems" : [{"ItemNumber" : 1,
                       "Part" : {"Description" : "One Magic Christmas",
                                 "UnitPrice"   : 19.95,
                                 "UPCCode"     : 13131092899},
                       "Quantity" : 9.0},
                      {"ItemNumber" : 2,
                       "Part" : {"Description" : "Lethal Weapon",
                                 "UnitPrice"   : 19.95,
                                 "UPCCode"     : 85391628927},
                       "Quantity" : 5.0}]}');
```

Using JSON\_query\_column: Example The statement in this example queries JSON data for a specific JSON property using the `JSON_query_column` clause, and returns the property value in a column.

The statement first applies a row path expression to column `po_document`, which results in a match to the `ShippingInstructions` property. The `COLUMNS` clause then uses the `JSON_query_column` clause to return the `Phone` property value in a `VARCHAR2(100)` column.

```
SELECT jt.phones
FROM j_purchaseorder,
JSON_TABLE(po_document, '$.ShippingInstructions'
COLUMNS
  (phones VARCHAR2(100) FORMAT JSON PATH '$.Phone')) AS jt;
```

```
PHONES
-------------------------------------------------------------------------------------
[{"type":"Office","number":"909-555-7307"},{"type":"Mobile","number":"415-555-1234"}]
```

Using JSON\_value\_column: Example The statement in this example refines the statement in the previous example by querying JSON data for specific JSON values using the `JSON_value_column` clause, and returns the JSON values as SQL values in relational rows and columns.

The statement first applies a row path expression to column `po_document`, which results in a match to the elements in the JSON array `Phone`. These elements are JSON objects that contain two members named `type` and `number`. The statement uses the `COLUMNS` clause to return the `type` value for each object in a `VARCHAR2(10)` column called `phone_type`, and the `number` value for each object in a `VARCHAR2(20)` column called `phone_num`. The statement also returns an ordinal column named `row_number`.

```
SELECT jt.*
FROM j_purchaseorder,
JSON_TABLE(po_document, '$.ShippingInstructions.Phone[*]'
COLUMNS (row_number FOR ORDINALITY,
         phone_type VARCHAR2(10) PATH '$.type',
         phone_num VARCHAR2(20) PATH '$.number'))
AS jt;

ROW_NUMBER PHONE_TYPE PHONE_NUM
---------- ---------- --------------------
         1 Office     909-555-7307
         2 Mobile     415-555-1234
```

Using JSON\_exists\_column: Examples The statements in this example test whether a JSON value exists in JSON data using the `JSON_exists_column` clause. The first example returns the result of the test as a '`true`' or '`false`' value in a column. The second example uses the result of the test in the `WHERE` clause.

The following statement first applies a row path expression to column `po_document`, which results in a match to the entire context item, or JSON document. It then uses the `COLUMNS` clause to return the requestor's name and a string value of '`true`' or '`false`' indicating whether the JSON data for that requestor contains a zip code. The `COLUMNS` clause first uses the `JSON_value_column` clause to return the `Requestor` value in a `VARCHAR2(32)` column called `requestor`. It then uses the `JSON_exists_column` clause to determine if the `zipCode` object exists and returns the result in a `VARCHAR2(5)` column called `has_zip`.

```
SELECT requestor, has_zip
FROM j_purchaseorder,
JSON_TABLE(po_document, '$'
COLUMNS
  (requestor VARCHAR2(32) PATH '$.Requestor',
   has_zip VARCHAR2(5) EXISTS PATH '$.ShippingInstructions.Address.zipCode'));

REQUESTOR                        HAS_ZIP
-------------------------------- -------
Alexis Bull                      true
```

The following statement is similar to the previous statement, except that it uses the value of `has_zip` in the `WHERE` clause to determine whether to return the `Requestor` value:

```
SELECT requestor
FROM j_purchaseorder,
JSON_TABLE(po_document, '$'
COLUMNS
  (requestor VARCHAR2(32) PATH '$.Requestor',
   has_zip VARCHAR2(5) EXISTS PATH '$.ShippingInstructions.Address.zipCode'))
WHERE (has_zip = 'true');

REQUESTOR
--------------------------------
Alexis Bull
```

Using JSON\_nested\_path: Examples The following two simple statements demonstrate the functionality of the `JSON_nested_path` clause. They operate on a simple JSON array that contains three elements. The first two elements are numbers. The third element is a nested JSON array that contains two string value elements.

The following statement does not use the `JSON_nested_path` clause. It returns the three elements in the array in a single row. The nested array is returned in its entirety.

```
SELECT *
FROM JSON_TABLE('[1,2,["a","b"]]', '$'
COLUMNS (outer_value_0 NUMBER PATH '$[0]',
         outer_value_1 NUMBER PATH '$[1]', 
         outer_value_2 VARCHAR2(20) FORMAT JSON PATH '$[2]'));

OUTER_VALUE_0 OUTER_VALUE_1 OUTER_VALUE_2
------------- ------------- --------------------
            1             2 ["a","b"]
```

The following statement is different from the previous statement because it uses the `JSON_nested_path` clause to return the individual elements of the nested array in individual columns in a single row along with the parent array elements.

```
SELECT *
FROM JSON_TABLE('[1,2,["a","b"]]', '$'
COLUMNS (outer_value_0 NUMBER PATH '$[0]',
         outer_value_1 NUMBER PATH '$[1]',
         NESTED PATH '$[2]'
         COLUMNS (nested_value_0 VARCHAR2(1) PATH '$[0]',
                  nested_value_1 VARCHAR2(1) PATH '$[1]')));

OUTER_VALUE_0 OUTER_VALUE_1 NESTED_VALUE_0 NESTED_VALUE_1
------------- ------------- -------------- --------------
            1             2 a              b
```

The previous example shows how to use `JSON_nested_path` with a nested JSON array. The following example shows how to use the `JSON_nested_path` clause with a nested JSON object by returning the individual elements of the nested object in individual columns in a single row along with the parent object elements.

```
SELECT *
FROM JSON_TABLE('{a:100, b:200, c:{d:300, e:400}}', '$'
COLUMNS (outer_value_0 NUMBER PATH '$.a',
         outer_value_1 NUMBER PATH '$.b',
         NESTED PATH '$.c'
         COLUMNS (nested_value_0 NUMBER PATH '$.d',
                  nested_value_1 NUMBER PATH '$.e')));

OUTER_VALUE_0 OUTER_VALUE_1 NESTED_VALUE_0 NESTED_VALUE_1
------------- ------------- -------------- --------------
          100           200            300            400
```

The following statement uses the `JSON_nested_path` clause when querying the `j_purchaseorder` table. It first applies a row path expression to column `po_document`, which results in a match to the entire context item, or JSON document. It then uses the `COLUMNS` clause to return the `Requestor` value in a `VARCHAR2(32)` column called `requestor`. It then uses the `JSON_nested_path` clause to return the property values of the individual objects in each member of the nested `Phone` array. Note that a row is generated for each member of the nested array, and each row contains the corresponding `Requestor` value.

```
SELECT jt.*
FROM j_purchaseorder,
JSON_TABLE(po_document, '$'
COLUMNS
  (requestor VARCHAR2(32) PATH '$.Requestor',
   NESTED PATH '$.ShippingInstructions.Phone[*]'
     COLUMNS (phone_type VARCHAR2(32) PATH '$.type',
              phone_num VARCHAR2(20) PATH '$.number')))
AS jt;
 
 
REQUESTOR            PHONE_TYPE           PHONE_NUM
-------------------- -------------------- ---------------
Alexis Bull          Office               909-555-7307
Alexis Bull          Mobile               415-555-1234
```