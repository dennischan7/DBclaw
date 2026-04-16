---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The core PostgreSQL distribution includes the GIN operator classes previously shown in [Table 70.1.](#page-139-0) The following contrib modules also contain GIN operator classes:

```
btree_gin
    B-tree equivalent functionality for several data types
hstore
    Module for storing (key, value) pairs
intarray
    Enhanced support for int[]
pg_trgm
```

Text similarity using trigram matching

# <span id="page-146-0"></span>**Chapter 71. BRIN Indexes**