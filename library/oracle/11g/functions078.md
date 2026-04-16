# Oracle 11g - functions078
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions078.htm

# INSERTXMLAFTER

Syntax

Purpose

`INSERTXMLAFTER` inserts one or more nodes of any kind immediately after a target node that is not an attribute node. The XML document that is the target of the insertion can be schema-based or non-schema-based. This function is similar to insertXMLbefore, but it inserts after, not before, the target node.

* `XMLType_instance` specifies the target node of the of the insertion.
* `XPath_string` is an XPath 1.0 expression that locates in the target node zero or more nodes of any kind except attribute nodes. XML-data is inserted immediately after each of these nodes; that is, each node specified becomes the preceding sibling node of a node specified in `value_expr`.
* `value_expr` is the XML data to be inserted. You can specify one or more nodes of any kind. The order of the nodes is preserved after the insertion.
* The optional `namespace_string` is the namespace for the target node.

Examples

The following example is similar to that for `INSERTCHILDXML`, but it adds a third `/Owner` node after the `/Owner` node added in the other example. The output of the query has been formatted for readability.

```
UPDATE warehouses
  SET warehouse_spec = INSERTXMLAFTER(warehouse_spec,
    '/Warehouse/Building/Owner[1]', XMLType('<Owner>SecondOwner</Owner>'))
  WHERE warehouse_id = 3;

SELECT warehouse_name,
       EXTRACT(warehouse_spec, '/Warehouse/Building/Owner') "Owners"
  FROM warehouses
  WHERE warehouse_id = 3;

WAREHOUSE_NAME                      Owners
----------------------------------- ------------------------------
New Jersey                          <Owner>GrandCo</Owner>
                                    <Owner>SecondOwner</Owner>
                                    <Owner>LesserCo</Owner>
```