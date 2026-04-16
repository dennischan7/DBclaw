# Oracle 11g - functions144
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/functions144.htm

[Go to main content](#BEGIN)

184/522 

# RAWTONHEX

Syntax

Purpose

`RAWTONHEX` converts `raw` to a character value containing its hexadecimal representation. `RAWTONHEX` (`raw`) is equivalent to `TO_NCHAR`(`RAWTOHEX`(`raw`)). The value returned is always in the national character set.

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