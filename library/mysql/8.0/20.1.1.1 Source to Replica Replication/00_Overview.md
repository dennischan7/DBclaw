---
source: MySQL 8.0 Reference
title: 00_Overview
---

Traditional MySQL Replication provides a simple source to replica approach to replication. The source is the primary, and there are one or more replicas, which are secondaries. The source applies transactions, commits them and then they are later (thus asynchronously) sent to the replicas to be either re-executed (in statement-based replication) or applied (in row-based replication). It is a sharednothing system, where all servers have a full copy of the data by default.

**Figure 20.1 MySQL Asynchronous Replication**

![](_page_85_Figure_2.jpeg)

There is also semisynchronous replication, which adds one synchronization step to the protocol. This means that the primary waits, at apply time, for the secondary to acknowledge that it has received the transaction. Only then does the primary resume the commit operation.

**Figure 20.2 MySQL Semisynchronous Replication**

![](_page_85_Figure_5.jpeg)

In the two pictures there is a diagram of the classic asynchronous MySQL Replication protocol (and its semisynchronous variant as well). The arrows between the different instances represent messages exchanged between servers or messages exchanged between servers and the client application.