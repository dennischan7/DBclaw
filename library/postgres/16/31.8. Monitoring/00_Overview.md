---
source: PostgreSQL 16 Reference
title: 00_Overview
---

Because logical replication is based on a similar architecture as [physical streaming replication](#page-17-0), the monitoring on a publication node is similar to monitoring of a physical replication primary (see [Sec](#page-19-1)[tion 27.2.5.2\)](#page-19-1).

The monitoring information about subscription is visible in [pg\\_stat\\_subscription](#page-56-1). This view contains one row for every subscription worker. A subscription can have zero or more active subscription workers depending on its state.

Normally, there is a single apply process running for an enabled subscription. A disabled subscription or a crashed subscription will have zero rows in this view. If the initial data synchronization of any table is in progress, there will be additional workers for the tables being synchronized. Moreover, if the streaming transaction is applied in parallel, there may be additional parallel apply workers.