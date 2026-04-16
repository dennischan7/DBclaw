# Oracle 12c - functions241
Source: https://docs.oracle.com/database/121/SQLRF/functions241.htm

# UPDATEXML

Note:

The

`UPDATEXML`

function is deprecated. It is still supported for backward compatibility. However, Oracle recommends that you use XQuery Update instead. See

[Oracle XML DB Developer's Guide](../ADXDB/xdb_xquery.md#ADXDB1700)

for more information.

Syntax

Purpose

`UPDATEXML` takes as arguments an `XMLType` instance and an XPath-value pair and returns an `XMLType` instance with the updated value. If `XPath_string` is an XML element, then the corresponding `value_expr` must be an `XMLType` instance. If `XPath_string` is an attribute or text node, then the `value_expr` can be any scalar data type. You can specify an absolute `XPath_string` with an initial slash or a relative `XPath_string` by omitting the initial slash. If you omit the initial slash, then the context of the relative path defaults to the root node.

The data types of the target of each `XPath_string` and its corresponding `value_expr` must match. The optional `namespace_string` must resolve to a `VARCHAR2` value that specifies a default mapping or namespace mapping for prefixes, which Oracle Database uses when evaluating the XPath expression(s).

If you update an XML element to null, then Oracle removes the attributes and children of the element, and the element becomes empty. If you update the text node of an element to null, Oracle removes the text value of the element, and the element itself remains but is empty.

In most cases, this function materializes an XML document in memory and updates the value. However, `UPDATEXML` is optimized for `UPDATE` statements on object-relational columns so that the function updates the value directly in the column. This optimization requires the following conditions:

Examples

The following example updates to 4 the number of docks in the San Francisco warehouse in the sample schema `OE`, which has a `warehouse_spec` column of type `XMLType`:

```
SELECT warehouse_name,
   EXTRACT(warehouse_spec, '/Warehouse/Docks')
   "Number of Docks"
   FROM warehouses 
   WHERE warehouse_name = 'San Francisco';

WAREHOUSE_NAME       Number of Docks
-------------------- --------------------
San Francisco        <Docks>1</Docks>

UPDATE warehouses SET warehouse_spec =
   UPDATEXML(warehouse_spec,
   '/Warehouse/Docks/text()',4)
   WHERE warehouse_name = 'San Francisco';

1 row updated.

SELECT warehouse_name,
   EXTRACT(warehouse_spec, '/Warehouse/Docks')
   "Number of Docks"
   FROM warehouses 
   WHERE warehouse_name = 'San Francisco';

WAREHOUSE_NAME       Number of Docks
-------------------- --------------------
San Francisco        <Docks>4</Docks>
```