# Oracle 11g - functions057
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions057.htm

# EXISTSNODE

Note:

The

`EXISTSNODE`

function is deprecated. It is still supported for backward compatibility. However, Oracle recommends that you use the

`XMLEXISTS`

function instead. See

[XMLEXISTS](functions243.md#CIHDEFCD)

for more information.

Syntax

Purpose

`EXISTSNODE` determines whether traversal of an XML document using a specified path results in any nodes. It takes as arguments the `XMLType` instance containing an XML document and a `VARCHAR2` XPath string designating a path. The optional `namespace_string` must resolve to a `VARCHAR2` value that specifies a default mapping or namespace mapping for prefixes, which Oracle Database uses when evaluating the XPath expression(s).

The `namespace_string` argument defaults to the namespace of the root element. If you refer to any subelement in `Xpath_string`, then you must specify `namespace_string`, and you must specify the "who" prefix in both of these arguments.

The return value is `NUMBER`:

Examples

The following example tests for the existence of the `/Warehouse/Dock` node in the XML path of the `warehouse_spec` column of the sample table `oe.warehouses`:

```
SELECT warehouse_id, warehouse_name
  FROM warehouses
  WHERE EXISTSNODE(warehouse_spec, '/Warehouse/Docks') = 1
  ORDER BY warehouse_id;

WAREHOUSE_ID WAREHOUSE_NAME
------------ -----------------------------------
           1 Southlake, Texas
           2 San Francisco
           4 Seattle, Washington
```