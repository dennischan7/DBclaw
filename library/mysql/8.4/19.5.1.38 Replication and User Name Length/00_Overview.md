---
source: MySQL 8.4 Reference
title: 00_Overview
---

The maximum length for user names in MySQL 8.4 is 32 characters. Replication of user names longer than 16 characters fails when the replica runs a version of MySQL previous to 5.7, because those versions support only shorter user names. This occurs only when replicating from a newer source to an older replica, which is not a recommended configuration.