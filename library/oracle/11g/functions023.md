# Oracle 11g - functions023
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions023.htm

# CAST

Syntax

Purpose

`CAST` converts one built-in data type or collection-typed value into another built-in data type or collection-typed value.

`CAST` lets you convert built-in data types or collection-typed values of one type into another built-in data type or collection type. You can cast an unnamed operand (such as a date or the result set of a subquery) or a named collection (such as a varray or a nested table) into a type-compatible data type or named collection. The `type_name` must be the name of a built-in data type or collection type and the operand must be a built-in data type or must evaluate to a collection value.

For the operand, `expr` can be either a built-in data type, a collection type, or an instance of an `ANYDATA` type. If `expr` is an instance of an `ANYDATA` type, then `CAST` tries to extract the value of the `ANYDATA` instance and return it if it matches the cast target type, otherwise, null will be returned. `MULTISET` informs Oracle Database to take the result set of the subquery and return a collection value. [Table 5-1](#g1514003) shows which built-in data types can be cast into which other built-in data types. (`CAST` does not support `LONG`, `LONG` `RAW`, or the Oracle-supplied types.)

`CAST` does not directly support any of the LOB data types. When you use `CAST` to convert a `CLOB` value into a character data type or a `BLOB` value into the `RAW` data type, the database implicitly converts the LOB value to character or raw data and then explicitly casts the resulting value into the target data type. If the resulting value is larger than the target type, then the database returns an error.

When you use `CAST` ... `MULTISET` to get a collection value, each select list item in the query passed to the `CAST` function is converted to the corresponding attribute type of the target collection element type.

Table 5-1 Casting Built-In Data Types

|  | from BINARY\_FLOAT, BINARY\_DOUBLE | from CHAR, VARCHAR2 | fromNUMBER | from DATETIME / INTERVAL (Note 1) | fromRAW | from ROWID, UROWID (Note 2) | from NCHAR, NVARCHAR2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| to BINARY\_FLOAT, BINARY\_DOUBLE | `X` | `X` | `X` | `--` | `--` | `--` | `X` |
| to CHAR, VARCHAR2 | `X` | `X` | `X` | `X` | `X` | `X` | `--` |
| to NUMBER | `X` | `X` | `X` | `--` | `--` | `--` | `X` |
| to DATE, TIMESTAMP, INTERVAL | `--` | `X` | `--` | `X` | `--` | `--` | `--` |
| to RAW | `--` | `X` | `--` | `--` | `X` | `--` | `--` |
| to ROWID, UROWID | `--` | `X` | `--` | `--` | `--` | `X` | `--` |
| to NCHAR, NVARCHAR2 | `X` | `--` | `X` | `X` | `X` | `X` | `X` |

Note 1: Datetime/interval includes `DATE`, `TIMESTAMP`, `TIMESTAMP` `WITH` `TIMEZONE`, `INTERVAL` `DAY` `TO` `SECOND`, and `INTERVAL` `YEAR` `TO` `MONTH`.

Note 2: You cannot cast a `UROWID` to a `ROWID` if the `UROWID` contains the value of a `ROWID` of an index-organized table.

If you want to cast a named collection type into another named collection type, then the elements of both collections must be of the same type.

If the result set of `subquery` can evaluate to multiple rows, then you must specify the `MULTISET` keyword. The rows resulting from the subquery form the elements of the collection value into which they are cast. Without the `MULTISET` keyword, the subquery is treated as a scalar subquery.

Built-In Data Type Examples

The following examples use the `CAST` function with scalar data types. The first example converts text to a timestamp value by applying the format model provided in the session parameter `NLS_TIMESTAMP_FORMAT`. If you want to avoid dependency on this NLS parameter, then you can use the `TO_DATE` as shown in the second example.

```
SELECT CAST('22-OCT-1997'
       AS TIMESTAMP WITH LOCAL TIME ZONE) 
  FROM DUAL;

SELECT CAST(TO_DATE('22-Oct-1997', 'DD-Mon-YYYY')
       AS TIMESTAMP WITH LOCAL TIME ZONE)
  FROM DUAL;
```

In the preceding example, `TO_DATE` converts from text to `DATE`, and `CAST` converts from `DATE` to `TIMESTAMP` `WITH` `LOCAL` `TIME` `ZONE`, interpreting the date in the session time zone (`SESSIONTIMEZONE`).

```
SELECT product_id, CAST(ad_sourcetext AS VARCHAR2(30)) text
  FROM print_media
  ORDER BY product_id;
```

Collection Examples

The `CAST` examples that follow build on the `cust_address_typ` found in the sample order entry schema, `oe`.

```
CREATE TYPE address_book_t AS TABLE OF cust_address_typ;
/
CREATE TYPE address_array_t AS VARRAY(3) OF cust_address_typ;
/
CREATE TABLE cust_address (
  custno            NUMBER, 
  street_address    VARCHAR2(40), 
  postal_code       VARCHAR2(10), 
  city              VARCHAR2(30),
  state_province    VARCHAR2(10), 
  country_id        CHAR(2));

CREATE TABLE cust_short (custno NUMBER, name VARCHAR2(31));

CREATE TABLE states (state_id NUMBER, addresses address_array_t);
```

This example casts a subquery:

```
SELECT s.custno, s.name,
       CAST(MULTISET(SELECT ca.street_address,   
                            ca.postal_code, 
                            ca.city, 
                            ca.state_province, 
                            ca.country_id
                       FROM cust_address ca
                       WHERE s.custno = ca.custno)
       AS address_book_t)
  FROM cust_short s
  ORDER BY s.custno;
```

`CAST` converts a varray type column into a nested table:

```
SELECT CAST(s.addresses AS address_book_t)
  FROM states s 
  WHERE s.state_id = 111;
```

The following objects create the basis of the example that follows:

```
CREATE TABLE projects 
  (employee_id NUMBER, project_name VARCHAR2(10));

CREATE TABLE emps_short 
  (employee_id NUMBER, last_name VARCHAR2(10));

CREATE TYPE project_table_typ AS TABLE OF VARCHAR2(10);
/
```

The following example of a `MULTISET` expression uses these objects:

```
SELECT e.last_name,
       CAST(MULTISET(SELECT p.project_name
                       FROM projects p 
                       WHERE p.employee_id = e.employee_id
                       ORDER BY p.project_name)
       AS project_table_typ)
  FROM emps_short e
  ORDER BY e.last_name;
```