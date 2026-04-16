---
source: PostgreSQL 14 Reference
title: 00_Overview
---

Vacuum maintains a visibility map for each table to keep track of which pages contain only tuples that are known to be visible to all active transactions (and all future transactions, until the page is again modified). This has two purposes. First, vacuum itself can skip such pages on the next run, since there is nothing to clean up.

Second, it allows PostgreSQL to answer some queries using only the index, without reference to the underlying table. Since PostgreSQL indexes don't contain tuple visibility information, a normal index scan fetches the heap tuple for each matching index entry, to check whether it should be seen by the current transaction. An *index-only scan*, on the other hand, checks the visibility map first. If it's known that all tuples on the page are visible, the heap fetch can be skipped. This is most useful on large data sets where the visibility map can prevent disk accesses. The visibility map is vastly smaller than the heap, so it can easily be cached even when the heap is very large.

# <span id="page-154-0"></span>**25.1.5. Preventing Transaction ID Wraparound Failures**

PostgreSQL's MVCC transaction semantics depend on being able to compare transaction ID (XID) numbers: a row version with an insertion XID greater than the current transaction's XID is "in the future" and should not be visible to the current transaction. But since transaction IDs have limited size (32 bits) a cluster that runs for a long time (more than 4 billion transactions) would suffer *transaction ID wraparound*: the XID counter wraps around to zero, and all of a sudden transactions that were in the past appear to be in the future — which means their output become invisible. In short, catastrophic data loss. (Actually the data is still there, but that's cold comfort if you cannot get at it.) To avoid this, it is necessary to vacuum every table in every database at least once every two billion transactions.

The reason that periodic vacuuming solves the problem is that VACUUM will mark rows as *frozen*, indicating that they were inserted by a transaction that committed sufficiently far in the past that the effects of the inserting transaction are certain to be visible to all current and future transactions. Normal XIDs are compared using modulo-232 arithmetic. This means that for every normal XID, there are two billion XIDs that are "older" and two billion that are "newer"; another way to say it is that the normal XID space is circular with no endpoint. Therefore, once a row version has been created with a particular normal XID, the row version will appear to be "in the past" for the next two billion transactions, no matter which normal XID we are talking about. If the row version still exists after more than two billion transactions, it will suddenly appear to be in the future. To prevent this, PostgreSQL reserves a special XID, FrozenTransactionId, which does not follow the normal XID comparison rules and is always considered older than every normal XID. Frozen row versions are treated as if the inserting XID were FrozenTransactionId, so that they will appear to be "in the past" to all normal transactions regardless of wraparound issues, and so such row versions will be valid until deleted, no matter how long that is.

### **Note**

In PostgreSQL versions before 9.4, freezing was implemented by actually replacing a row's insertion XID with FrozenTransactionId, which was visible in the row's xmin system column. Newer versions just set a flag bit, preserving the row's original xmin for possible forensic use. However, rows with xmin equal to FrozenTransactionId (2) may still be found in databases pg\_upgrade'd from pre-9.4 versions.

Also, system catalogs may contain rows with xmin equal to BootstrapTransactionId (1), indicating that they were inserted during the first phase of initdb. Like FrozenTransactionId, this special XID is treated as older than every normal XID.

[vacuum\\_freeze\\_min\\_age](#page-79-0) controls how old an XID value has to be before rows bearing that XID will be frozen. Increasing this setting may avoid unnecessary work if the rows that would otherwise be frozen will soon be modified again, but decreasing this setting increases the number of transactions that can elapse before the table must be vacuumed again.

VACUUM uses the visibility map to determine which pages of a table must be scanned. Normally, it will skip pages that don't have any dead row versions even if those pages might still have row versions with old XID values. Therefore, normal VACUUMs won't always freeze every old row version in the table. Periodically, VACUUM will perform an *aggressive vacuum*, skipping only those pages which contain neither dead rows nor any unfrozen XID or MXID values. [vacuum\\_freeze\\_table\\_age](#page-79-1) controls when VACUUM does that: all-visible but not all-frozen pages are scanned if the number of transactions that have passed since the last such scan is greater than vacuum\_freeze\_table\_age minus vacuum\_freeze\_min\_age. Setting vacuum\_freeze\_table\_age to 0 forces VACUUM to use this more aggressive strategy for all scans.

The maximum time that a table can go unvacuumed is two billion transactions minus the vacuum\_freeze\_min\_age value at the time of the last aggressive vacuum. If it were to go unvacuumed for longer than that, data loss could result. To ensure that this does not happen, autovacuum is invoked on any table that might contain unfrozen rows with XIDs older than the age specified by the configuration parameter [autovacuum\\_freeze\\_max\\_age.](#page-74-0) (This will happen even if autovacuum is disabled.)

This implies that if a table is not otherwise vacuumed, autovacuum will be invoked on it approximately once every autovacuum\_freeze\_max\_age minus vacuum\_freeze\_min\_age transactions. For tables that are regularly vacuumed for space reclamation purposes, this is of little importance. However, for static tables (including tables that receive inserts, but no updates or deletes), there is no need to vacuum for space reclamation, so it can be useful to try to maximize the interval between forced autovacuums on very large static tables. Obviously one can do this either by increasing autovacuum\_freeze\_max\_age or decreasing vacuum\_freeze\_min\_age.

The effective maximum for vacuum\_freeze\_table\_age is 0.95 \* autovacuum\_freeze\_max\_age; a setting higher than that will be capped to the maximum. A value higher than autovacuum\_freeze\_max\_age wouldn't make sense because an anti-wraparound autovacuum would be triggered at that point anyway, and the 0.95 multiplier leaves some breathing room to run a manual VACUUM before that happens. As a rule of thumb, vacuum\_freeze\_table\_age should be set to a value somewhat below autovacuum\_freeze\_max\_age, leaving enough gap so that a regularly scheduled VACUUM or an autovacuum triggered by normal delete and update activity is run in that window. Setting it too close could lead to anti-wraparound autovacuums, even though the table was recently vacuumed to reclaim space, whereas lower values lead to more frequent aggressive vacuuming.

The sole disadvantage of increasing autovacuum\_freeze\_max\_age (and vacuum\_freeze\_table\_age along with it) is that the pg\_xact and pg\_commit\_ts subdirectories of the database cluster will take more space, because it must store the commit status and (if track\_commit\_timestamp is enabled) timestamp of all transactions back to the autovacuum\_freeze\_max\_age horizon. The commit status uses two bits per transaction, so if autovacuum\_freeze\_max\_age is set to its maximum allowed value of two billion, pg\_xact can be expected to grow to about half a gigabyte and pg\_commit\_ts to about 20GB. If this is trivial compared to your total database size, setting autovacuum\_freeze\_max\_age to its maximum allowed value is recommended. Otherwise, set it depending on what you are willing to allow for pg\_xact and pg\_commit\_ts storage. (The default, 200 million transactions, translates to about 50MB of pg\_xact storage and about 2GB of pg\_commit\_ts storage.)

One disadvantage of decreasing vacuum\_freeze\_min\_age is that it might cause VACUUM to do useless work: freezing a row version is a waste of time if the row is modified soon thereafter (causing it to acquire a new XID). So the setting should be large enough that rows are not frozen until they are unlikely to change any more.

To track the age of the oldest unfrozen XIDs in a database, VACUUM stores XID statistics in the system tables pg\_class and pg\_database. In particular, the relfrozenxid column of a table's pg\_class row contains the freeze cutoff XID that was used by the last aggressive VACUUM for that table. All rows inserted by transactions with XIDs older than this cutoff XID are guaranteed to have been frozen. Similarly, the datfrozenxid column of a database's pg\_database row is a lower bound on the unfrozen XIDs appearing in that database — it is just the minimum of the pertable relfrozenxid values within the database. A convenient way to examine this information is to execute queries such as:

```
SELECT c.oid::regclass as table_name,
 greatest(age(c.relfrozenxid),age(t.relfrozenxid)) as age
FROM pg_class c
LEFT JOIN pg_class t ON c.reltoastrelid = t.oid
WHERE c.relkind IN ('r', 'm');
SELECT datname, age(datfrozenxid) FROM pg_database;
```

The age column measures the number of transactions from the cutoff XID to the current transaction's XID.

VACUUM normally only scans pages that have been modified since the last vacuum, but relfrozenxid can only be advanced when every page of the table that might contain unfrozen XIDs is scanned. This happens when relfrozenxid is more than vacuum\_freeze\_table\_age transactions old, when VACUUM's FREEZE option is used, or when all pages that are not already all-frozen happen to require vacuuming to remove dead row versions. When VACUUM scans every page in the table that is not already all-frozen, it should set age(relfrozenxid) to a value just a little more than the vacuum\_freeze\_min\_age setting that was used (more by the number of transactions started since the VACUUM started). If no relfrozenxid-advancing VACUUM is issued on the table until autovacuum\_freeze\_max\_age is reached, an autovacuum will soon be forced for the table.

If for some reason autovacuum fails to clear old XIDs from a table, the system will begin to emit warning messages like this when the database's oldest XIDs reach forty million transactions from the wraparound point:

#### Routine Database Maintenance Tasks

WARNING: database "mydb" must be vacuumed within 39985967 transactions

HINT: To avoid a database shutdown, execute a database-wide VACUUM in that database.

(A manual VACUUM should fix the problem, as suggested by the hint; but note that the VACUUM should be performed by a superuser, else it will fail to process system catalogs, which prevent it from being able to advance the database's datfrozenxid.) If these warnings are ignored, the system will refuse to assign new XIDs once there are fewer than three million transactions left until wraparound:

ERROR: database is not accepting commands to avoid wraparound data loss in database "mydb"

HINT: Stop the postmaster and vacuum that database in single-user mode.

In this condition any transactions already in progress can continue, but only read-only transactions can be started. Operations that modify database records or truncate relations will fail. The VACUUM command can still be run normally. Contrary to what the hint states, it is not necessary or desirable to stop the postmaster or enter single user-mode in order to restore normal operation. Instead, follow these steps:

- 1. Resolve old prepared transactions. You can find these by checking pg\_prepared\_xacts for rows where age(transactionid) is large. Such transactions should be committed or rolled back.
- 2. End long-running open transactions. You can find these by checking pg\_stat\_activity for rows where age(backend\_xid) or age(backend\_xmin) is large. Such transactions should be committed or rolled back, or the session can be terminated using pg\_terminate\_backend.
- 3. Drop any old replication slots. Use pg\_stat\_replication to find slots where age(xmin) or age(catalog\_xmin) is large. In many cases, such slots were created for replication to servers that no longer exist, or that have been down for a long time. If you drop a slot for a server that still exists and might still try to connect to that slot, that replica may need to be rebuilt.
- 4. Execute VACUUM in the target database. A database-wide VACUUM is simplest; to reduce the time required, it as also possible to issue manual VACUUM commands on the tables where relminxid is oldest. Do not use VACUUM FULL in this scenario, because it requires an XID and will therefore fail, except in super-user mode, where it will instead consume an XID and thus increase the risk of transaction ID wraparound. Do not use VACUUM FREEZE either, because it will do more than the minimum amount of work required to restore normal operation.
- 5. Once normal operation is restored, ensure that autovacuum is properly configured in the target database in order to avoid future problems.

### **Note**

In earlier versions, it was sometimes necessary to stop the postmaster and VACUUM the database in a single-user mode. In typical scenarios, this is no longer necessary, and should be avoided whenever possible, since it involves taking the system down. It is also riskier, since it disables transaction ID wraparound safeguards that are designed to prevent data loss. The only reason to use single-user mode in this scenario is if you wish to TRUNCATE or DROP unneeded tables to avoid needing to VACUUM them. The three-million-transaction safety margin exists to let the administrator do this. See the postgres reference page for details about using single-user mode.

### <span id="page-157-0"></span>**25.1.5.1. Multixacts and Wraparound**

*Multixact IDs* are used to support row locking by multiple transactions. Since there is only limited space in a tuple header to store lock information, that information is encoded as a "multiple transaction ID", or multixact ID for short, whenever there is more than one transaction concurrently locking a row. Information about which transaction IDs are included in any particular multixact ID is stored separately in the pg\_multixact subdirectory, and only the multixact ID appears in the xmax field in the tuple header. Like transaction IDs, multixact IDs are implemented as a 32-bit counter and corresponding storage, all of which requires careful aging management, storage cleanup, and wraparound handling. There is a separate storage area which holds the list of members in each multixact, which also uses a 32-bit counter and which must also be managed. The system function pg\_get\_multixact\_members() described in Table 9.76 can be used to examine the transaction IDs associated with a multixact ID.

Whenever VACUUM scans any part of a table, it will replace any multixact ID it encounters which is older than [vacuum\\_multixact\\_freeze\\_min\\_age](#page-80-0) by a different value, which can be the zero value, a single transaction ID, or a newer multixact ID. For each table, pg\_class.relminmxid stores the oldest possible multixact ID still appearing in any tuple of that table. If this value is older than [vacuum\\_multixact\\_freeze\\_table\\_age](#page-80-1), an aggressive vacuum is forced. As discussed in the previous section, an aggressive vacuum means that only those pages which are known to be all-frozen will be skipped. mxid\_age() can be used on pg\_class.relminmxid to find its age.

Aggressive VACUUM scans, regardless of what causes them, enable advancing the value for that table. Eventually, as all tables in all databases are scanned and their oldest multixact values are advanced, on-disk storage for older multixacts can be removed.

As a safety device, an aggressive vacuum scan will occur for any table whose multixact-age is greater than [autovacuum\\_multixact\\_freeze\\_max\\_age.](#page-75-1) Also, if the storage occupied by multixacts members exceeds about 10GB, aggressive vacuum scans will occur more often for all tables, starting with those that have the oldest multixact-age. Both of these kinds of aggressive scans will occur even if autovacuum is nominally disabled. The members storage area can grow up to about 20GB before reaching wraparound.

Similar to the XID case, if autovacuum fails to clear old MXIDs from a table, the system will begin to emit warning messages when the database's oldest MXIDs reach forty million transactions from the wraparound point. And, just as an the XID case, if these warnings are ignored, the system will refuse to generate new MXIDs once there are fewer than three million left until wraparound.

Normal operation when MXIDs are exhausted can be restored in much the same way as when XIDs are exhausted. Follow the same steps in the previous section, but with the following differences:

- 1. Running transactions and prepared transactions can be ignored if there is no chance that they might appear in a multixact.
- 2. MXID information is not directly visible in system views such as pg\_stat\_activity; however, looking for old XIDs is still a good way of determining which transactions are causing MXID wraparound problems.
- 3. XID exhaustion will block all write transactions, but MXID exhaustion will only block a subset of write transactions, specifically those that involve row locks that require an MXID.

# <span id="page-158-0"></span>**25.1.6. The Autovacuum Daemon**

PostgreSQL has an optional but highly recommended feature called *autovacuum*, whose purpose is to automate the execution of VACUUM and ANALYZE commands. When enabled, autovacuum checks for tables that have had a large number of inserted, updated or deleted tuples. These checks use the statistics collection facility; therefore, autovacuum cannot be used unless [track\\_counts](#page-72-0) is set to true. In the default configuration, autovacuuming is enabled and the related configuration parameters are appropriately set.

The "autovacuum daemon" actually consists of multiple processes. There is a persistent daemon process, called the *autovacuum launcher*, which is in charge of starting *autovacuum worker* processes

#### Routine Database Maintenance Tasks

for all databases. The launcher will distribute the work across time, attempting to start one worker within each database every [autovacuum\\_naptime](#page-74-1) seconds. (Therefore, if the installation has N databases, a new worker will be launched every autovacuum\_naptime/N seconds.) A maximum of [autovacuum\\_max\\_workers](#page-73-0) worker processes are allowed to run at the same time. If there are more than autovacuum\_max\_workers databases to be processed, the next database will be processed as soon as the first worker finishes. Each worker process will check each table within its database and execute VACUUM and/or ANALYZE as needed. [log\\_autovacuum\\_min\\_duration](#page-65-0) can be set to monitor autovacuum workers' activity.

If several large tables all become eligible for vacuuming in a short amount of time, all autovacuum workers might become occupied with vacuuming those tables for a long period. This would result in other tables and databases not being vacuumed until a worker becomes available. There is no limit on how many workers might be in a single database, but workers do try to avoid repeating work that has already been done by other workers. Note that the number of running workers does not count towards [max\\_connections](#page-22-0) or [superuser\\_reserved\\_connections](#page-22-4) limits.

Tables whose relfrozenxid value is more than [autovacuum\\_freeze\\_max\\_age](#page-74-0) transactions old are always vacuumed (this also applies to those tables whose freeze max age has been modified via storage parameters; see below). Otherwise, if the number of tuples obsoleted since the last VACUUM exceeds the "vacuum threshold", the table is vacuumed. The vacuum threshold is defined as:

```
vacuum threshold = vacuum base threshold + vacuum scale factor *
 number of tuples
```

where the vacuum base threshold is [autovacuum\\_vacuum\\_threshold](#page-74-2), the vacuum scale factor is [auto](#page-74-3)[vacuum\\_vacuum\\_scale\\_factor,](#page-74-3) and the number of tuples is pg\_class.reltuples.

The table is also vacuumed if the number of tuples inserted since the last vacuum has exceeded the defined insert threshold, which is defined as:

```
vacuum insert threshold = vacuum base insert threshold + vacuum
 insert scale factor * number of tuples
```

where the vacuum insert base threshold is [autovacuum\\_vacuum\\_insert\\_threshold,](#page-74-4) and vacuum insert scale factor is [autovacuum\\_vacuum\\_insert\\_scale\\_factor](#page-74-5). Such vacuums may allow portions of the table to be marked as *all visible* and also allow tuples to be frozen, which can reduce the work required in subsequent vacuums. For tables which receive INSERT operations but no or almost no UPDATE/ DELETE operations, it may be beneficial to lower the table's autovacuum\_freeze\_min\_age as this may allow tuples to be frozen by earlier vacuums. The number of obsolete tuples and the number of inserted tuples are obtained from the statistics collector; it is a semi-accurate count updated by each UPDATE, DELETE and INSERT operation. (It is only semi-accurate because some information might be lost under heavy load.) If the relfrozenxid value of the table is more than vacuum\_freeze\_table\_age transactions old, an aggressive vacuum is performed to freeze old tuples and advance relfrozenxid; otherwise, only pages that have been modified since the last vacuum are scanned.

For analyze, a similar condition is used: the threshold, defined as:

```
analyze threshold = analyze base threshold + analyze scale factor *
 number of tuples
```

is compared to the total number of tuples inserted, updated, or deleted since the last ANALYZE.

Partitioned tables do not directly store tuples and consequently are not processed by autovacuum. (Autovacuum does process table partitions just like other tables.) Unfortunately, this means that autovacuum does not run ANALYZE on partitioned tables, and this can cause suboptimal plans for queries that reference partitioned table statistics. You can work around this problem by manually running ANALYZE on partitioned tables when they are first populated, and again whenever the distribution of data in their partitions changes significantly.

Temporary tables cannot be accessed by autovacuum. Therefore, appropriate vacuum and analyze operations should be performed via session SQL commands.

The default thresholds and scale factors are taken from postgresql.conf, but it is possible to override them (and many other autovacuum control parameters) on a per-table basis; see Storage Parameters for more information. If a setting has been changed via a table's storage parameters, that value is used when processing that table; otherwise the global settings are used. See [Section 20.10](#page-73-2) for more details on the global settings.

When multiple workers are running, the autovacuum cost delay parameters (see [Section 20.4.4\)](#page-32-1) are "balanced" among all the running workers, so that the total I/O impact on the system is the same regardless of the number of workers actually running. However, any workers processing tables whose pertable autovacuum\_vacuum\_cost\_delay or autovacuum\_vacuum\_cost\_limit storage parameters have been set are not considered in the balancing algorithm.

Autovacuum workers generally don't block other commands. If a process attempts to acquire a lock that conflicts with the SHARE UPDATE EXCLUSIVE lock held by autovacuum, lock acquisition will interrupt the autovacuum. For conflicting lock modes, see Table 13.2. However, if the autovacuum is running to prevent transaction ID wraparound (i.e., the autovacuum query name in the pg\_stat\_activity view ends with (to prevent wraparound)), the autovacuum is not automatically interrupted.

### **Warning**

Regularly running commands that acquire locks conflicting with a SHARE UPDATE EX-CLUSIVE lock (e.g., ANALYZE) can effectively prevent autovacuums from ever completing.