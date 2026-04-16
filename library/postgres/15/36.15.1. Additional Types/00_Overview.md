---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The Informix-special "string" pseudo-type for storing right-trimmed character string data is now supported in Informix-mode without using typedef. In fact, in Informix-mode, ECPG refuses to process source files that contain typedef sometype string;

```
EXEC SQL BEGIN DECLARE SECTION;
string userid; /* this variable will contain trimmed data */
EXEC SQL END DECLARE SECTION;
EXEC SQL FETCH MYCUR INTO :userid;
```