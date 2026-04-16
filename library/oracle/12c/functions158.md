# Oracle 12c - functions158
Source: https://docs.oracle.com/database/121/SQLRF/functions158.htm

[Go to main content](#BEGIN)

231/555 

# RAWTONHEX

Syntax

Purpose

`RAWTONHEX` converts `raw` to a character value containing its hexadecimal representation. `RAWTONHEX(``raw``)` is equivalent to `TO_NCHAR(RAWTOHEX(``raw``))`. The value returned is always in the national character set.

Examples

The following hypothetical example returns the hexadecimal equivalent of a `RAW` column value:

```
SELECT RAWTONHEX(raw_column),
   DUMP ( RAWTONHEX (raw_column) ) "DUMP" 
   FROM graphics; 

RAWTONHEX(RA)           DUMP 
----------------------- ------------------------------ 
7D                      Typ=1 Len=4: 0,55,0,68
```

Scripting on this page enhances content navigation, but does not change the content in any way.