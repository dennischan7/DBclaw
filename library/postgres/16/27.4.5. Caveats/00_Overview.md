---
source: PostgreSQL 16 Reference
title: 00_Overview
---

There are several limitations of hot standby. These can and probably will be fixed in future releases:

- Full knowledge of running transactions is required before snapshots can be taken. Transactions that use large numbers of subtransactions (currently greater than 64) will delay the start of read-only connections until the completion of the longest running write transaction. If this situation occurs, explanatory messages will be sent to the server log.
- Valid starting points for standby queries are generated at each checkpoint on the primary. If the standby is shut down while the primary is in a shutdown state, it might not be possible to re-enter hot standby until the primary is started up, so that it generates further starting points in the WAL logs. This situation isn't a problem in the most common situations where it might happen. Generally, if the primary is shut down and not available anymore, that's likely due to a serious failure that requires the standby being converted to operate as the new primary anyway. And in situations where the primary is being intentionally taken down, coordinating to make sure the standby becomes the new primary smoothly is also standard procedure.
- At the end of recovery, AccessExclusiveLocks held by prepared transactions will require twice the normal number of lock table entries. If you plan on running either a large number of concurrent prepared transactions that normally take AccessExclusiveLocks, or you plan on having one large transaction that takes many AccessExclusiveLocks, you are advised to select a larger value of max\_locks\_per\_transaction, perhaps as much as twice the value of the parameter on the primary server. You need not consider this at all if your setting of max\_prepared\_transactions is 0.

| hot standby mode will generate an error. |  |  |
|------------------------------------------|--|--|
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |
|                                          |  |  |