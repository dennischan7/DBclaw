---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The transaction IDs of currently executing transactions are shown in pg\_locks in columns virtualxid and transactionid. Read-only transactions will have virtualxids but NULL transactionids, while both columns will be set in read-write transactions.

Some lock types wait on virtualxid, while other types wait on transactionid. Row-level read and write locks are recorded directly in the locked rows and can be inspected using the pgrowlocks extension. Row-level read locks might also require the assignment of multixact IDs (mxid; see Section 25.1.5.1).