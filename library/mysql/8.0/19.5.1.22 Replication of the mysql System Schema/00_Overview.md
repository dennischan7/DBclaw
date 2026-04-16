---
source: MySQL 8.0 Reference
title: 00_Overview
---

Data modification statements made to tables in the mysql schema are replicated according to the value of binlog\_format; if this value is MIXED, these statements are replicated using row-based format. However, statements that would normally update this information indirectly—such GRANT, REVOKE, and statements manipulating triggers, stored routines, and views—are replicated to replicas using statement-based replication.