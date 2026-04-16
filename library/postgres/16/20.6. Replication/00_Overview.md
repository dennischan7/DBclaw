---
source: PostgreSQL 16 Reference
title: 00_Overview
---

These settings control the behavior of the built-in *streaming replication* feature (see Section 27.2.5), and the built-in *logical replication* feature (see Chapter 31).

For *streaming replication*, servers will be either a primary or a standby server. Primaries can send data, while standbys are always receivers of replicated data. When cascading replication (see Section 27.2.7) is used, standby servers can also be senders, as well as receivers. Parameters are mainly for sending and standby servers, though some parameters have meaning only on the primary server. Settings may vary across the cluster without problems if that is required.

For *logical replication*, *publishers* (servers that do CREATE PUBLICATION) replicate data to *subscribers* (servers that do CREATE SUBSCRIPTION). Servers can also be publishers and subscribers at the same time. Note, the following sections refer to publishers as "senders". For more details about logical replication configuration settings refer to Section 31.10.