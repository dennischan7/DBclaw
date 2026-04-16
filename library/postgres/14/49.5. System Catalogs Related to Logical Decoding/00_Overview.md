---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The pg\_replication\_slots view and the pg\_stat\_replication view provide information about the current state of replication slots and streaming replication connections respectively. These views apply to both physical and logical replication. The pg\_stat\_replication\_slots view provides statistics information about the logical replication slots.

## <span id="page-74-2"></span>**49.6. Logical Decoding Output Plugins**

An example output plugin can be found in the contrib/test\_decoding subdirectory of the PostgreSQL source tree.