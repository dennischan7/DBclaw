---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Logical replication requires several configuration options to be set. Most options are relevant only on one side of the replication. However, max\_replication\_slots is used on both the publisher and the subscriber, but it has a different meaning for each.