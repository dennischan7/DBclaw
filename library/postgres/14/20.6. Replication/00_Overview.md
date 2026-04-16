---
source: PostgreSQL 14 Reference
title: 00_Overview
---

These settings control the behavior of the built-in *streaming replication* feature (see [Section 27.2.5](#page-185-0)). Servers will be either a primary or a standby server. Primaries can send data, while standbys are always receivers of replicated data. When cascading replication (see [Section 27.2.7\)](#page-187-0) is used, standby servers can also be senders, as well as receivers. Parameters are mainly for sending and standby servers, though some parameters have meaning only on the primary server. Settings may vary across the cluster without problems if that is required.