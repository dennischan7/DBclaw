# Oracle 11g - functions246
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions246.htm

[Go to main content](#BEGIN)

286/522 

# XMLPARSE

Syntax

Purpose

`XMLParse` parses and generates an XML instance from the evaluated result of `value_expr`. The `value_expr` must resolve to a string. If `value_expr` resolves to null, then the function returns null.

* If you specify `DOCUMENT`, then `value_expr` must resolve to a singly rooted XML document.
* If you specify `CONTENT`, then `value_expr` must resolve to a valid XML value.
* When you specify `WELLFORMED`, you are guaranteeing that `value_expr` resolves to a well-formed XML document, so the database does not perform validity checks to ensure that the input is well formed.

Examples

The following example uses the `DUAL` table to illustrate the syntax of `XMLParse`:

```
SELECT XMLPARSE(CONTENT '124 <purchaseOrder poNo="12435"> 
   <customerName> Acme Enterprises</customerName>
   <itemNo>32987457</itemNo>
   </purchaseOrder>' 
WELLFORMED) AS PO FROM DUAL;
 
PO
-----------------------------------------------------------------
124 <purchaseOrder poNo="12435">
   <customerName> Acme Enterprises</customerName>
   <itemNo>32987457</itemNo>
   </purchaseOrder>
```

Scripting on this page enhances content navigation, but does not change the content in any way.