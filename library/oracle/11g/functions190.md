# Oracle 11g - functions190
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions190.htm

# SYS\_XMLGEN

Syntax

Purpose

`SYS_XMLGen` takes an expression that evaluates to a particular row and column of the database, and returns an instance of type `XMLType` containing an XML document. The `expr` can be a scalar value, a user-defined type, or an `XMLType` instance.

* If `expr` is a scalar value, then the function returns an XML element containing the scalar value.
* If `expr` is a type, then the function maps the user-defined type attributes to XML elements.
* If `expr` is an `XMLType` instance, then the function encloses the document in an XML element whose default tag name is `ROW`.

By default the elements of the XML document match the elements of `expr`. For example, if `expr` resolves to a column name, then the enclosing XML element will be the same column name. If you want to format the XML document differently, then specify `fmt`, which is an instance of the `XMLFormat` object.

See Also:

["XML Format Model"](sql_elements004.md#i54997)

for a description of the

`XMLFormat`

type and how to use its attributes to format

`SYS_XMLGen`

results

Examples

The following example retrieves the employee email ID from the sample table `oe.employees` where the `employee_id` value is 205, and generates an instance of an `XMLType` containing an XML document with an `EMAIL` element.

```
SELECT SYS_XMLGEN(email)      
   FROM employees
   WHERE employee_id = 205;

SYS_XMLGEN(EMAIL)
-------------------------------------------------------------------
<?xml version="1.0"?>
<EMAIL>SHIGGINS</EMAIL>
```