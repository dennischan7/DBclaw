# Oracle 23c - JSON_DATAGUIDE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/JSON_DATAGUIDE.html

format options

Use the format options to specify the format of the data guide that will be returned. It must be one of the following values:

* `dbms_json.format_flat` for a flat format.
* `dbms_json.format_hierarchical` for a hierarchical format.
* `dbms_json.format_schema` for a data guide of a JSON schema that you can use to validate JSON documents.

If the parameter is the absent, the default is `dbms_json.format_flat`.

See [Data-Guide Formats and Ways of Creating a Data Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADJSN-GUID-B57975A8-3000-4F21-BB22-DC413F06D6DB)   of the JSON Developer's Guide.

The following example uses the `j_purchaseorder` table, which is created in "[Creating a Table That Contains a JSON Document: Example](JSON_TABLE.md#GUID-3C8E63B5-0B94-4E86-A2D3-3D4831B67C62__CJAHAAJE)". This table contains a column of JSON data called `po_document`. This example returns a flat data guide for each year group.

```
SELECT EXTRACT(YEAR FROM date_loaded) YEAR,
       JSON_DATAGUIDE(po_document) "DATA GUIDE"
  FROM j_purchaseorder
  GROUP BY extract(YEAR FROM date_loaded)
  ORDER BY extract(YEAR FROM date_loaded) DESC;

YEAR DATA GUIDE
---- ------------------------------------------
2016 [
       {
         "o:path" : "$.PO_ID",
         "type" : "number",
         "o:length" : 4
       },
       {
         "o:path" : "$.PO_Ref",
         "type" : "string",
         "o:length" : 16
       },
       {
         "o:path" : "$.PO_Items",
         "type" : "array",
         "o:length" : 64
       },
       {
         "o:path" : "$.PO_Items.Part_No",
         "type" : "number",
         "o:length" : 16
       },
       {
         "o:path" : "$.PO_Items.Item_Quantity",
         "type" : "number",
         "o:length" : 2
       }
     ]
. . .
```