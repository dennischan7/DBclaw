# Oracle 12c - functions059
Source: https://docs.oracle.com/database/121/SQLRF/functions059.htm

[Go to main content](#BEGIN)

132/555 

# DELETEXML

Note:

The

`DELETEXML`

function is deprecated. It is still supported for backward compatibility. However, Oracle recommends that you use XQuery Update instead. See

[Oracle XML DB Developer's Guide](../ADXDB/xdb_xquery.md#ADXDB1700)

for more information.

Syntax

Purpose

`DELETEXML` deletes the node or nodes matched by the XPath expression in the target XML.

* `XMLType_instance` is an instance of `XMLType`.
* `XPath_string` is an Xpath expression indicating one or more nodes that are to be deleted. You can specify an absolute `XPath_string` with an initial slash or a relative `XPath_string` by omitting the initial slash. If you omit the initial slash, then the context of the relative path defaults to the root node. Any child nodes of the nodes specified by `XPath_string` are also deleted.
* The optional `namespace_string` provides namespace information for the `XPath_string`. This parameter must be of type `VARCHAR2`.

Examples

The following example removes the `/Owner` node from the `warehouse_spec` of one of the warehouses modified in the example for [APPENDCHILDXML](functions012.md#CIHEGIFE):

```
UPDATE warehouses
  SET warehouse_spec = DELETEXML(warehouse_spec, '/Warehouse/Building/Owner')
  WHERE warehouse_id = 2;

SELECT warehouse_id, warehouse_spec
  FROM warehouses  WHERE warehouse_id in (2,3);

        ID WAREHOUSE_SPEC
---------- -----------------------------------
         2 <?xml version="1.0"?>
           <Warehouse>
             <Building>Rented</Building>
             <Area>50000</Area>
             <Docks>1</Docks>
             <DockType>Side load</DockType>
             <WaterAccess>Y</WaterAccess>
             <RailAccess>N</RailAccess>
             <Parking>Lot</Parking>
             <VClearance>12 ft</VClearance>
           </Warehouse>
 
         3 <?xml version="1.0"?>
           <Warehouse>
             <Building>Rented<Owner>Grandco</Owner>
             </Building>
             <Area>85700</Area>
             <DockType/>
             <WaterAccess>N</WaterAccess>
             <RailAccess>N</RailAccess>
             <Parking>Street</Parking>
             <VClearance>11.5 ft</VClearance>
           </Warehouse>
```

Scripting on this page enhances content navigation, but does not change the content in any way.