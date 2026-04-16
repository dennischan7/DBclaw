---
source: PostgreSQL 16 Reference
title: 00_Overview
---

max\_replication\_slots must be set to at least the number of subscriptions that will be added to the subscriber, plus some reserve for table synchronization.

max\_logical\_replication\_workers must be set to at least the number of subscriptions (for leader apply workers), plus some reserve for the table synchronization workers and parallel apply workers.

max\_worker\_processes may need to be adjusted to accommodate for replication workers, at least (max\_logical\_replication\_workers + 1). Note, some extensions and parallel queries also take worker slots from max\_worker\_processes.

max\_sync\_workers\_per\_subscription controls the amount of parallelism of the initial data copy during the subscription initialization or when new tables are added.

max\_parallel\_apply\_workers\_per\_subscription controls the amount of parallelism for streaming of in-progress transactions with subscription parameter streaming = parallel.

Logical replication workers are also affected by wal\_receiver\_timeout, wal\_receiver\_status\_interval and wal\_retrieve\_retry\_interval.