# Oracle 11g - functions012
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions012.htm

[Go to main content](#BEGIN)

52/522 

# APPENDCHILDXML

Syntax

Purpose

`APPENDCHILDXML` appends a user-supplied value onto the target XML as the child of the node indicated by an XPath expression.

* `XMLType_instance` is an instance of `XMLType`.
* `XPath_string` is an Xpath expression indicating one or more nodes onto which one or more child nodes are to be appended. You can specify an absolute `XPath_string` with an initial slash or a relative `XPath_string` by omitting the initial slash. If you omit the initial slash, then the context of the relative path defaults to the root node.
* `value_expr` specifies one or more nodes of `XMLType`. It must resolve to a string.
* The optional `namespace_string` provides namespace information for the `XPath_string`. This parameter must be of type `VARCHAR2`.

Examples

The following example adds an `/Owner` node to the `/Warehouse/Building` node of `warehouse_spec` in the `oe.warehouses` table if the value of the `/Building` node is "Rented":

```
UPDATE warehouses
  SET warehouse_spec = APPENDCHILDXML(warehouse_spec, 'Warehouse/Building',
    XMLType('<Owner>Grandco</Owner>'))
  WHERE EXTRACTVALUE(warehouse_spec, '/Warehouse/Building') = 'Rented';

SELECT warehouse_id,
       warehouse_name,
       EXTRACTVALUE(warehouse_spec, '/Warehouse/Building/Owner') "Prop.Owner"
  FROM warehouses
  WHERE EXISTSNODE(warehouse_spec, '/Warehouse/Building/Owner') = 1;

WAREHOUSE_ID WAREHOUSE_NAME  Prop.Owner
------------ --------------- ----------
           2 San Francisco   Grandco
           3 New Jersey      Grandco
```

Scripting on this page enhances content navigation, but does not change the content in any way.