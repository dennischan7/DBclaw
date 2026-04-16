---
source: MySQL 8.0 Reference
title: 00_Overview
---

Two [INFORMATION\\_SCHEMA](#page-192-0) tables provide information that is of particular use when managing an NDB Cluster. The FILES table provides information about NDB Cluster Disk Data files (see

Section 25.6.11.1, "NDB Cluster Disk Data Objects"). The ndb\_transid\_mysql\_connection\_map table provides a mapping between transactions, transaction coordinators, and API nodes.

Additional statistical and other data about NDB Cluster transactions, operations, threads, blocks, and other aspects of performance can be obtained from the tables in the ndbinfo database. For information about these tables, see Section 25.6.16, "ndbinfo: The NDB Cluster Information Database".