# Oracle 12c - functions069
Source: https://docs.oracle.com/database/121/SQLRF/functions069.htm

# EXTRACTVALUE

Note:

The

`EXTRACTVALUE`

function is deprecated. It is still supported for backward compatibility. However, Oracle recommends that you use the

`XMLTABLE`

function, or the

`XMLCAST`

and

`XMLQUERY`

functions instead. See

[XMLTABLE](functions269.md#CIHGGHFB)

,

[XMLCAST](functions252.md#CIHHHACJ)

, and

[XMLQUERY](functions265.md#CIHHFFGG)

for more information.

Syntax

The `EXTRACTVALUE` function takes as arguments an `XMLType` instance and an XPath expression and returns a scalar value of the resultant node. The result must be a single node and be either a text node, attribute, or element. If the result is an element, then the element must have a single text node as its child, and it is this value that the function returns. You can specify an absolute `XPath_string` with an initial slash or a relative `XPath_string` by omitting the initial slash. If you omit the initial slash, the context of the relative path defaults to the root node.

If the specified XPath points to a node with more than one child, or if the node pointed to has a non-text node child, then Oracle returns an error. The optional `namespace_string` must resolve to a `VARCHAR2` value that specifies a default mapping or namespace mapping for prefixes, which Oracle uses when evaluating the XPath expression(s).

For documents based on XML schemas, if Oracle can infer the type of the return value, then a scalar value of the appropriate type is returned. Otherwise, the result is of type `VARCHAR2`. For documents that are not based on XML schemas, the return type is always `VARCHAR2`.

Examples

The following example takes as input the same arguments as the example for [EXTRACT (XML)](functions068.md#i1006712). Instead of returning an XML fragment, as does the `EXTRACT` function, it returns the scalar value of the XML fragment:

```
SELECT warehouse_name, EXTRACTVALUE(e.warehouse_spec, '/Warehouse/Docks') "Docks"
  FROM warehouses e 
  WHERE warehouse_spec IS NOT NULL
  ORDER BY warehouse_name;

WAREHOUSE_NAME       Docks
-------------------- ------------
New Jersey
San Francisco        1
Seattle, Washington  3
Southlake, Texas     2
```