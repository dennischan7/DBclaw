---
source: PostgreSQL 14 Reference
title: 00_Overview
---

Logical replication requires several configuration options to be set.

On the publisher side, wal\_level must be set to logical, and max\_replication\_slots must be set to at least the number of subscriptions expected to connect, plus some reserve for table synchronization. And max\_wal\_senders should be set to at least the same as max\_replication\_slots plus the number of physical replicas that are connected at the same time.

max\_replication\_slots must also be set on the subscriber. It should be set to at least the number of subscriptions that will be added to the subscriber, plus some reserve for table synchronization. max\_logical\_replication\_workers must be set to at least the number of subscriptions, again plus some reserve for the table synchronization. Additionally the max\_worker\_processes may need to be adjusted to accommodate for replication workers, at least (max\_logical\_replication\_workers + 1). Note that some extensions and parallel queries also take worker slots from max\_worker\_processes.