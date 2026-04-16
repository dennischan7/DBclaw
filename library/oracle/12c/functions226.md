# Oracle 12c - functions226
Source: https://docs.oracle.com/database/121/SQLRF/functions226.htm

[Go to main content](#BEGIN)

299/555 

# TO\_NCLOB

Syntax

Purpose

`TO_NCLOB` converts `CLOB` values in a LOB column or other character strings to `NCLOB` values. `char` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. Oracle Database implements this function by converting the character set of `char` from the database character set to the national character set.

Examples

The following example inserts some character data into an `NCLOB` column of the `pm.print_media` table by first converting the data with the `TO_NCLOB` function:

```
INSERT INTO print_media (product_id, ad_id, ad_fltextn)
   VALUES (3502, 31001, 
      TO_NCLOB('Placeholder for new product description'));
```

Scripting on this page enhances content navigation, but does not change the content in any way.