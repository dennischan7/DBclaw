---
source: PostgreSQL 16 Reference
title: 00_Overview
---

```
CLOSE DATABASE
```

This statement closes the current connection. In fact, this is a synonym for ECPG's DISCONNECT CURRENT:

```
$CLOSE DATABASE; /* close the current connection
   */
  EXEC SQL CLOSE DATABASE;
FREE cursor_name
```

Due to differences in how ECPG works compared to Informix's ESQL/C (namely, which steps are purely grammar transformations and which steps rely on the underlying run-time library) there is no FREE cursor\_name statement in ECPG. This is because in ECPG, DECLARE CURSOR doesn't translate to a function call into the run-time library that uses to the cursor name. This means that there's no run-time bookkeeping of SQL cursors in the ECPG run-time library, only in the PostgreSQL server.

```
FREE statement_name
   FREE statement_name is a synonym for DEALLOCATE PREPARE statement_name.
```