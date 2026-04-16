# Oracle 12c - functions064
Source: https://docs.oracle.com/database/121/SQLRF/functions064.htm

[Go to main content](#BEGIN)

137/555 

# EMPTY\_BLOB, EMPTY\_CLOB

Syntax

empty\_LOB::=

Purpose

`EMPTY_BLOB` and `EMPTY_CLOB` return an empty LOB locator that can be used to initialize a LOB variable or, in an `INSERT` or `UPDATE` statement, to initialize a LOB column or attribute to `EMPTY`. `EMPTY` means that the LOB is initialized, but not populated with data.

Restriction on LOB Locators You cannot use the locator returned from this function as a parameter to the `DBMS_LOB` package or the OCI.

Examples

The following example initializes the `ad_photo` column of the sample `pm.print_media` table to `EMPTY`:

```
UPDATE print_media
  SET ad_photo = EMPTY_BLOB();
```

Scripting on this page enhances content navigation, but does not change the content in any way.