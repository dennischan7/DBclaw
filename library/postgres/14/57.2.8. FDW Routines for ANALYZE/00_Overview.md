---
source: PostgreSQL 14 Reference
title: 00_Overview
---

```
bool
AnalyzeForeignTable(Relation relation,
 AcquireSampleRowsFunc *func,
```

```
 BlockNumber *totalpages);
```

This function is called when ANALYZE is executed on a foreign table. If the FDW can collect statistics for this foreign table, it should return true, and provide a pointer to a function that will collect sample rows from the table in func, plus the estimated size of the table in pages in totalpages. Otherwise, return false.

If the FDW does not support collecting statistics for any tables, the AnalyzeForeignTable pointer can be set to NULL.

If provided, the sample collection function must have the signature

```
int
AcquireSampleRowsFunc(Relation relation,
 int elevel,
 HeapTuple *rows,
 int targrows,
 double *totalrows,
 double *totaldeadrows);
```

A random sample of up to targrows rows should be collected from the table and stored into the caller-provided rows array. The actual number of rows collected must be returned. In addition, store estimates of the total numbers of live and dead rows in the table into the output parameters totalrows and totaldeadrows. (Set totaldeadrows to zero if the FDW does not have any concept of dead rows.)