---
source: PostgreSQL 14 Reference
title: 00_Overview
---

For additional information on tuning these settings, see Section 30.5.

## <span id="page-37-2"></span><span id="page-37-1"></span>**20.5.1. Settings**

```
wal_level (enum)
```

wal\_level determines how much information is written to the WAL. The default value is replica, which writes enough data to support WAL archiving and replication, including running read-only queries on a standby server. minimal removes all logging except the information required to recover from a crash or immediate shutdown. Finally, logical adds information necessary to support logical decoding. Each level includes the information logged at all lower levels. This parameter can only be set at server start.

The minimal level generates the least WAL volume. It logs no row information for permanent relations in transactions that create or rewrite them. This can make operations much faster (see Section 14.4.7). Operations that initiate this optimization include:

```
ALTER ... SET TABLESPACE
CLUSTER
CREATE TABLE
REFRESH MATERIALIZED VIEW (without CONCURRENTLY)
REINDEX
TRUNCATE
```

However, minimal WAL does not contain sufficient information for point-in-time recovery, so replica or higher must be used to enable continuous archiving ([archive\\_mode](#page-42-0)) and streaming binary replication. In fact, the server will not even start in this mode if max\_wal\_senders is non-zero. Note that changing wal\_level to minimal makes previous base backups unusable for point-in-time recovery and standby servers.

In logical level, the same information is logged as with replica, plus information needed to extract logical change sets from the WAL. Using a level of logical will increase the WAL volume, particularly if many tables are configured for REPLICA IDENTITY FULL and many UPDATE and DELETE statements are executed.

In releases prior to 9.6, this parameter also allowed the values archive and hot\_standby. These are still accepted but mapped to replica.

```
fsync (boolean)
```

If this parameter is on, the PostgreSQL server will try to make sure that updates are physically written to disk, by issuing fsync() system calls or various equivalent methods (see [wal\\_sync\\_method\)](#page-39-0). This ensures that the database cluster can recover to a consistent state after an operating system or hardware crash.

While turning off fsync is often a performance benefit, this can result in unrecoverable data corruption in the event of a power failure or system crash. Thus it is only advisable to turn off fsync if you can easily recreate your entire database from external data.

Examples of safe circumstances for turning off fsync include the initial loading of a new database cluster from a backup file, using a database cluster for processing a batch of data after which the database will be thrown away and recreated, or for a read-only database clone which gets recreated frequently and is not used for failover. High quality hardware alone is not a sufficient justification for turning off fsync.

For reliable recovery when changing fsync off to on, it is necessary to force all modified buffers in the kernel to durable storage. This can be done while the cluster is shutdown or while fsync is on by running initdb --sync-only, running sync, unmounting the file system, or rebooting the server.

In many situations, turning off [synchronous\\_commit](#page-38-0) for noncritical transactions can provide much of the potential performance benefit of turning off fsync, without the attendant risks of data corruption.

fsync can only be set in the postgresql.conf file or on the server command line. If you turn this parameter off, also consider turning off [full\\_page\\_writes](#page-39-1).

```
synchronous_commit (enum)
```

Specifies how much WAL processing must complete before the database server returns a "success" indication to the client. Valid values are remote\_apply, on (the default), remote\_write, local, and off.

If synchronous\_standby\_names is empty, the only meaningful settings are on and off; remote\_apply, remote\_write and local all provide the same local synchronization level as on. The local behavior of all non-off modes is to wait for local flush of WAL to disk. In off mode, there is no waiting, so there can be a delay between when success is reported to the client and when the transaction is later guaranteed to be safe against a server crash. (The maximum delay is three times [wal\\_writer\\_delay](#page-40-0).) Unlike [fsync,](#page-37-0) setting this parameter to off does not create any risk of database inconsistency: an operating system or database crash might result in some recent allegedly-committed transactions being lost, but the database state will be just the same as if those transactions had been aborted cleanly. So, turning synchronous\_commit off can be a useful alternative when performance is more important than exact certainty about the durability of a transaction. For more discussion see Section 30.4.

If [synchronous\\_standby\\_names](#page-48-0) is non-empty, synchronous\_commit also controls whether transaction commits will wait for their WAL records to be processed on the standby server(s).

When set to remote\_apply, commits will wait until replies from the current synchronous standby(s) indicate they have received the commit record of the transaction and applied it, so that it has become visible to queries on the standby(s), and also written to durable storage on the standbys. This will cause much larger commit delays than previous settings since it waits for WAL replay. When set to on, commits wait until replies from the current synchronous standby(s) indicate they have received the commit record of the transaction and flushed it to durable storage. This ensures the transaction will not be lost unless both the primary and all synchronous standbys suffer corruption of their database storage. When set to remote\_write, commits will wait until replies from the current synchronous standby(s) indicate they have received the commit record of the transaction and written it to their file systems. This setting ensures data preservation if a standby instance of PostgreSQL crashes, but not if the standby suffers an operating-system-level crash because the data has not necessarily reached durable storage on the standby. The setting local causes commits to wait for local flush to disk, but not for replication. This is usually not desirable when synchronous replication is in use, but is provided for completeness.

This parameter can be changed at any time; the behavior for any one transaction is determined by the setting in effect when it commits. It is therefore possible, and useful, to have some transactions commit synchronously and others asynchronously. For example, to make a single multistatement transaction commit asynchronously when the default is the opposite, issue SET LOCAL synchronous\_commit TO OFF within the transaction.

<span id="page-39-2"></span>[Table 20.1](#page-39-2) summarizes the capabilities of the synchronous\_commit settings.

**Table 20.1. synchronous\_commit Modes**

| synchronous_commit<br>setting | local durable<br>commit | standby<br>durable com<br>mit after PG<br>crash | standby<br>durable com<br>mit after OS<br>crash | standby query<br>consistency |
|-------------------------------|-------------------------|-------------------------------------------------|-------------------------------------------------|------------------------------|
| remote_apply                  | •                       | •                                               | •                                               | •                            |
| on                            | •                       | •                                               | •                                               |                              |
| remote_write                  | •                       | •                                               |                                                 |                              |
| local                         | •                       |                                                 |                                                 |                              |
| off                           |                         |                                                 |                                                 |                              |

<span id="page-39-0"></span>wal\_sync\_method (enum)

Method used for forcing WAL updates out to disk. If fsync is off then this setting is irrelevant, since WAL file updates will not be forced out at all. Possible values are:

- open\_datasync (write WAL files with open() option O\_DSYNC)
- fdatasync (call fdatasync() at each commit)
- fsync (call fsync() at each commit)
- fsync\_writethrough (call fsync() at each commit, forcing write-through of any disk write cache)
- open\_sync (write WAL files with open() option O\_SYNC)

The open\_\* options also use O\_DIRECT if available. Not all of these choices are available on all platforms. The default is the first method in the above list that is supported by the platform, except that fdatasync is the default on Linux and FreeBSD. The default is not necessarily ideal; it might be necessary to change this setting or other aspects of your system configuration in order to create a crash-safe configuration or achieve optimal performance. These aspects are discussed in Section 30.1. This parameter can only be set in the postgresql.conf file or on the server command line.

<span id="page-39-1"></span>full\_page\_writes (boolean)

When this parameter is on, the PostgreSQL server writes the entire content of each disk page to WAL during the first modification of that page after a checkpoint. This is needed because a page write that is in process during an operating system crash might be only partially completed, leading to an on-disk page that contains a mix of old and new data. The row-level change data normally stored in WAL will not be enough to completely restore such a page during post-crash recovery. Storing the full page image guarantees that the page can be correctly restored, but at the price of increasing the amount of data that must be written to WAL. (Because WAL replay always starts from a checkpoint, it is sufficient to do this during the first change of each page after a checkpoint. Therefore, one way to reduce the cost of full-page writes is to increase the checkpoint interval parameters.)

Turning this parameter off speeds normal operation, but might lead to either unrecoverable data corruption, or silent data corruption, after a system failure. The risks are similar to turning off fsync, though smaller, and it should be turned off only based on the same circumstances recommended for that parameter.

Turning off this parameter does not affect use of WAL archiving for point-in-time recovery (PITR) (see [Section 26.3](#page-167-0)).

This parameter can only be set in the postgresql.conf file or on the server command line. The default is on.

```
wal_log_hints (boolean)
```

When this parameter is on, the PostgreSQL server writes the entire content of each disk page to WAL during the first modification of that page after a checkpoint, even for non-critical modifications of so-called hint bits.

If data checksums are enabled, hint bit updates are always WAL-logged and this setting is ignored. You can use this setting to test how much extra WAL-logging would occur if your database had data checksums enabled.

This parameter can only be set at server start. The default value is off.

```
wal_compression (boolean)
```

When this parameter is on, the PostgreSQL server compresses full page images written to WAL (e.g. when [full\\_page\\_writes](#page-39-1) is on, during a base backup, etc.). A compressed page image will be decompressed during WAL replay. The default value is off. Only superusers can change this setting.

Turning this parameter on can reduce the WAL volume without increasing the risk of unrecoverable data corruption, but at the cost of some extra CPU spent on the compression during WAL logging and on the decompression during WAL replay.

```
wal_init_zero (boolean)
```

If set to on (the default), this option causes new WAL files to be filled with zeroes. On some file systems, this ensures that space is allocated before we need to write WAL records. However, *Copy-On-Write* (COW) file systems may not benefit from this technique, so the option is given to skip the unnecessary work. If set to off, only the final byte is written when the file is created so that it has the expected size.

```
wal_recycle (boolean)
```

If set to on (the default), this option causes WAL files to be recycled by renaming them, avoiding the need to create new ones. On COW file systems, it may be faster to create new ones, so the option is given to disable this behavior.

```
wal_buffers (integer)
```

The amount of shared memory used for WAL data that has not yet been written to disk. The default setting of -1 selects a size equal to 1/32nd (about 3%) of [shared\\_buffers](#page-28-0), but not less than 64kB nor more than the size of one WAL segment, typically 16MB. This value can be set manually if the automatic choice is too large or too small, but any positive value less than 32kB will be treated as 32kB. If this value is specified without units, it is taken as WAL blocks, that is XLOG\_BLCKSZ bytes, typically 8kB. This parameter can only be set at server start.

The contents of the WAL buffers are written out to disk at every transaction commit, so extremely large values are unlikely to provide a significant benefit. However, setting this value to at least a few megabytes can improve write performance on a busy server where many clients are committing at once. The auto-tuning selected by the default setting of -1 should give reasonable results in most cases.

```
wal_writer_delay (integer)
```

Specifies how often the WAL writer flushes WAL, in time terms. After flushing WAL the writer sleeps for the length of time given by wal\_writer\_delay, unless woken up sooner by an asynchronously committing transaction. If the last flush happened less than wal\_writer\_delay ago and less than wal\_writer\_flush\_after worth of WAL has been produced since, then WAL is only written to the operating system, not flushed to disk. If this value is specified without units, it is taken as milliseconds. The default value is 200 milliseconds (200ms). Note that on many systems, the effective resolution of sleep delays is 10 milliseconds; setting wal\_writer\_delay to a value that is not a multiple of 10 might have the same results as setting it to the next higher multiple of 10. This parameter can only be set in the postgresql.conf file or on the server command line.

```
wal_writer_flush_after (integer)
```

Specifies how often the WAL writer flushes WAL, in volume terms. If the last flush happened less than wal\_writer\_delay ago and less than wal\_writer\_flush\_after worth of WAL has been produced since, then WAL is only written to the operating system, not flushed to disk. If wal\_writer\_flush\_after is set to 0 then WAL data is always flushed immediately. If this value is specified without units, it is taken as WAL blocks, that is XLOG\_BLCKSZ bytes, typically 8kB. The default is 1MB. This parameter can only be set in the postgresql.conf file or on the server command line.

```
wal_skip_threshold (integer)
```

When wal\_level is minimal and a transaction commits after creating or rewriting a permanent relation, this setting determines how to persist the new data. If the data is smaller than this setting, write it to the WAL log; otherwise, use an fsync of affected files. Depending on the properties of your storage, raising or lowering this value might help if such commits are slowing concurrent transactions. If this value is specified without units, it is taken as kilobytes. The default is two megabytes (2MB).

```
commit_delay (integer)
```

Setting commit\_delay adds a time delay before a WAL flush is initiated. This can improve group commit throughput by allowing a larger number of transactions to commit via a single WAL flush, if system load is high enough that additional transactions become ready to commit within the given interval. However, it also increases latency by up to the commit\_delay for each WAL flush. Because the delay is just wasted if no other transactions become ready to commit, a delay is only performed if at least commit\_siblings other transactions are active when a flush is about to be initiated. Also, no delays are performed if fsync is disabled. If this value is specified without units, it is taken as microseconds. The default commit\_delay is zero (no delay). Only superusers can change this setting.

In PostgreSQL releases prior to 9.3, commit\_delay behaved differently and was much less effective: it affected only commits, rather than all WAL flushes, and waited for the entire configured delay even if the WAL flush was completed sooner. Beginning in PostgreSQL 9.3, the first process that becomes ready to flush waits for the configured interval, while subsequent processes wait only until the leader completes the flush operation.

```
commit_siblings (integer)
```

Minimum number of concurrent open transactions to require before performing the commit\_delay delay. A larger value makes it more probable that at least one other transaction will become ready to commit during the delay interval. The default is five transactions.