# Oracle 11g - functions202
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions202.htm

# TO\_CLOB

Syntax

Purpose

`TO_CLOB` converts `NCLOB` values in a LOB column or other character strings to `CLOB` values. `char` can be any of the data types `CHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB`. Oracle Database executes this function by converting the underlying LOB data from the national character set to the database character set.

From within a PL/SQL package, you can use the `TO_CLOB` function to convert `RAW`, `CHAR`, `VARCHAR`, `VARCHAR2`, `NCHAR`, `NVARCHAR2`, `CLOB`, or `NCLOB` values to `CLOB` or `NCLOB` values.

Examples

The following statement converts `NCLOB` data from the sample `pm.print_media` table to `CLOB` and inserts it into a `CLOB` column, replacing existing data in that column.

```
UPDATE PRINT_MEDIA 
   SET AD_FINALTEXT = TO_CLOB (AD_FLTEXTN);
```