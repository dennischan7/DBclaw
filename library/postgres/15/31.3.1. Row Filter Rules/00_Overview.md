---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Row filters are applied *before* publishing the changes. If the row filter evaluates to false or NULL then the row is not replicated. The WHERE clause expression is evaluated with the same role used for the replication connection (i.e. the role specified in the CONNECTION clause of the CREATE SUBSCRIPTION). Row filters have no effect for TRUNCATE command.