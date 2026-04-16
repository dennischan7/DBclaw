# Oracle 12c - functions023
Source: https://docs.oracle.com/database/121/SQLRF/functions023.htm

[Go to main content](#BEGIN)

96/555 

# CARDINALITY

Syntax

Purpose

`CARDINALITY` returns the number of elements in a nested table. The return type is `NUMBER`. If the nested table is empty, or is a null collection, then `CARDINALITY` returns `NULL`.

Examples

The following example shows the number of elements in the nested table column `ad_textdocs_ntab` of the sample table `pm.print_media`:

```
SELECT product_id, CARDINALITY(ad_textdocs_ntab) cardinality
  FROM print_media
  ORDER BY product_id;

PRODUCT_ID CARDINALITY
---------- -----------
      2056           3
      2268           3
      3060           3
      3106           3
```

Scripting on this page enhances content navigation, but does not change the content in any way.