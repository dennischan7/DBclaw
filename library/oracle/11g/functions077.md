# Oracle 11g - functions077
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions077.htm

[Go to main content](#BEGIN)

117/522 

# INSERTCHILDXMLBEFORE

Syntax

Purpose

`INSERTXMLCHILDBEFORE` inserts one or more collection elements as children of target parent elements. The insertion for each target occurs immediately before a specified existing collection element. The existing XML document that is the target of the insertion can be schema-based or non-schema-based.

* `XMLType_instance` identifies the XML data that is the target of the insertion.
* `XPath_string` locates the parent elements within target-data; child-data is inserted under each parent element.
* `child_expr` is a relative XPath 1.0 expression that locates the existing child that will follow the inserted child-data. It must name a child element of the element indicated by parent-xpath, and it can include a predicate.
* `value_expr` is the XMLType child element data to insert. Each top-level element node in this argument must have the same data type as the element indicated by child\_expr.
* The optional `namespace_string` specifies the namespace for the parent elements, existing child element, and child element XML data to be inserted.

Examples

The following example is similar to that for `INSERTCHILDXML`, but it adds a third `/Owner` node before the `/Owner` node added in the other example. The output of the query has been formatted for readability.

```
UPDATE warehouses
  SET warehouse_spec = INSERTCHILDXMLBEFORE(warehouse_spec, '/Warehouse/Building',
    'Owner[2]', XMLType('<Owner>ThirdOwner</Owner>'))
  WHERE warehouse_id = 3;

SELECT warehouse_name,
       EXTRACT(warehouse_spec, '/Warehouse/Building/Owner') "Owners"
  FROM warehouses
  WHERE warehouse_id = 3;

WAREHOUSE_NAME                      Owners
----------------------------------- ------------------------------
New Jersey                          <Owner>GrandCo</Owner>
                                    <Owner>ThirdOwner</Owner>
                                    <Owner>LesserCo</Owner>
```

Scripting on this page enhances content navigation, but does not change the content in any way.