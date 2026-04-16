---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following list includes command-line options, system variables, and status variables applicable within mysqld when it is running as an SQL node in an NDB Cluster. For a reference to all commandline options, system variables, and status variables used with or relating to mysqld, see Section 7.1.4, "Server Option, System Variable, and Status Variable Reference".

- Com\_show\_ndb\_status: Count of SHOW NDB STATUS statements.
- Handler\_discover: Number of times that tables have been discovered.
- ndb-applier-allow-skip-epoch: Lets replication applier skip epochs.
- ndb-batch-size: Size (in bytes) to use for NDB transaction batches.
- ndb-blob-read-batch-bytes: Specifies size in bytes that large BLOB reads should be batched into. 0 = no limit.
- ndb-blob-write-batch-bytes: Specifies size in bytes that large BLOB writes should be batched into. 0 = no limit.
- ndb-cluster-connection-pool: Number of connections to cluster used by MySQL.
- ndb-cluster-connection-pool-nodeids: Comma-separated list of node IDs for connections to cluster used by MySQL; number of nodes in list must match value set for --ndb-cluster-connectionpool.
- ndb-connectstring: Address of NDB management server distributing configuration information for this cluster.
- ndb-default-column-format: Use this value (FIXED or DYNAMIC) by default for COLUMN\_FORMAT and ROW\_FORMAT options when creating or adding table columns.
- ndb-deferred-constraints: Specifies that constraint checks on unique indexes (where these are supported) should be deferred until commit time. Not normally needed or used; for testing purposes only.

- ndb-distribution: Default distribution for new tables in NDBCLUSTER (KEYHASH or LINHASH, default is KEYHASH).
- ndb-log-apply-status: Cause MySQL server acting as replica to log mysql.ndb\_apply\_status updates received from its immediate source in its own binary log, using its own server ID. Effective only if server is started with --ndbcluster option.
- ndb-log-empty-epochs: When enabled, causes epochs in which there were no changes to be written to ndb\_apply\_status and ndb\_binlog\_index tables, even when --log-slave-updates is enabled.
- ndb-log-empty-update: When enabled, causes updates that produced no changes to be written to ndb\_apply\_status and ndb\_binlog\_index tables, even when --log-slave-updates is enabled.
- ndb-log-exclusive-reads: Log primary key reads with exclusive locks; allow conflict resolution based on read conflicts.
- ndb-log-fail-terminate: Terminate mysqld process if complete logging of all found row events is not possible.
- ndb-log-orig: Log originating server id and epoch in mysql.ndb\_binlog\_index table.
- ndb-log-transaction-dependency: Make binary log thread calculate transaction dependencies for every transaction it writes to binary log.
- ndb-log-transaction-id: Write NDB transaction IDs in binary log. Requires --log-bin-v1 events=OFF.
- ndb-log-update-minimal: Log updates in minimal format.
- ndb-log-updated-only: Log updates only (ON) or complete rows (OFF).
- ndb-log-update-as-write: Toggles logging of updates on source between updates (OFF) and writes (ON).
- ndb-mgm-tls: Whether TLS connection requirements are strict or relaxed.
- ndb-mgmd-host: Set host (and port, if desired) for connecting to management server.
- ndb-nodeid: NDB Cluster node ID for this MySQL server.
- ndb-optimized-node-selection: Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable.
- ndb-tls-search-path: Directories to search for NDB TLS CAs and private keys.
- ndb-transid-mysql-connection-map: Enable or disable ndb\_transid\_mysql\_connection\_map plugin; that is, enable or disable INFORMATION\_SCHEMA table having that name.
- ndb-wait-connected: Time (in seconds) for MySQL server to wait for connection to cluster management and data nodes before accepting MySQL client connections.
- ndb-wait-setup: Time (in seconds) for MySQL server to wait for NDB engine setup to complete.
- ndb-allow-copying-alter-table: Set to OFF to keep ALTER TABLE from using copying operations on NDB tables.
- Ndb\_api\_adaptive\_send\_deferred\_count: Number of adaptive send calls not actually sent by this MySQL Server (SQL node).
- Ndb\_api\_adaptive\_send\_deferred\_count\_session: Number of adaptive send calls not actually sent in this client session.
- Ndb\_api\_adaptive\_send\_deferred\_count\_replica: Number of adaptive send calls not actually sent by this replica.

- Ndb\_api\_adaptive\_send\_deferred\_count\_slave: Number of adaptive send calls not actually sent by this replica.
- Ndb\_api\_adaptive\_send\_forced\_count: Number of adaptive sends with forced-send set sent by this MySQL Server (SQL node).
- Ndb\_api\_adaptive\_send\_forced\_count\_session: Number of adaptive sends with forcedsend set in this client session.
- Ndb\_api\_adaptive\_send\_forced\_count\_replica: Number of adaptive sends with forcedsend set sent by this replica.
- Ndb\_api\_adaptive\_send\_forced\_count\_slave: Number of adaptive sends with forced-send set sent by this replica.
- Ndb\_api\_adaptive\_send\_unforced\_count: Number of adaptive sends without forced-send sent by this MySQL Server (SQL node).
- Ndb\_api\_adaptive\_send\_unforced\_count\_session: Number of adaptive sends without forced-send in this client session.
- Ndb\_api\_adaptive\_send\_unforced\_count\_replica: Number of adaptive sends without forced-send sent by this replica.
- Ndb\_api\_adaptive\_send\_unforced\_count\_slave: Number of adaptive sends without forcedsend sent by this replica.
- Ndb\_api\_bytes\_received\_count: Quantity of data (in bytes) received from data nodes by this MySQL Server (SQL node).
- Ndb\_api\_bytes\_received\_count\_session: Quantity of data (in bytes) received from data nodes in this client session.
- Ndb\_api\_bytes\_received\_count\_replica: Quantity of data (in bytes) received from data nodes by this replica.
- Ndb\_api\_bytes\_received\_count\_slave: Quantity of data (in bytes) received from data nodes by this replica.
- Ndb\_api\_bytes\_sent\_count: Quantity of data (in bytes) sent to data nodes by this MySQL Server (SQL node).
- Ndb\_api\_bytes\_sent\_count\_session: Quantity of data (in bytes) sent to data nodes in this client session.
- Ndb\_api\_bytes\_sent\_count\_replica: Qunatity of data (in bytes) sent to data nodes by this replica.
- Ndb\_api\_bytes\_sent\_count\_slave: Qunatity of data (in bytes) sent to data nodes by this replica.
- Ndb\_api\_event\_bytes\_count: Number of bytes of events received by this MySQL Server (SQL node).
- Ndb\_api\_event\_bytes\_count\_injector: Number of bytes of event data received by NDB binary log injector thread.
- Ndb\_api\_event\_data\_count: Number of row change events received by this MySQL Server (SQL node).
- Ndb\_api\_event\_data\_count\_injector: Number of row change events received by NDB binary log injector thread.

- Ndb\_api\_event\_nondata\_count: Number of events received, other than row change events, by this MySQL Server (SQL node).
- Ndb\_api\_event\_nondata\_count\_injector: Number of events received, other than row change events, by NDB binary log injector thread.
- Ndb\_api\_pk\_op\_count: Number of operations based on or using primary keys by this MySQL Server (SQL node).
- Ndb\_api\_pk\_op\_count\_session: Number of operations based on or using primary keys in this client session.
- Ndb\_api\_pk\_op\_count\_replica: Number of operations based on or using primary keys by this replica.
- Ndb\_api\_pk\_op\_count\_slave: Number of operations based on or using primary keys by this replica.
- Ndb\_api\_pruned\_scan\_count: Number of scans that have been pruned to one partition by this MySQL Server (SQL node).
- Ndb\_api\_pruned\_scan\_count\_session: Number of scans that have been pruned to one partition in this client session.
- Ndb\_api\_pruned\_scan\_count\_replica: Number of scans that have been pruned to one partition by this replica.
- Ndb\_api\_pruned\_scan\_count\_slave: Number of scans that have been pruned to one partition by this replica.
- Ndb\_api\_range\_scan\_count: Number of range scans that have been started by this MySQL Server (SQL node).
- Ndb\_api\_range\_scan\_count\_session: Number of range scans that have been started in this client session.
- Ndb\_api\_range\_scan\_count\_replica: Number of range scans that have been started by this replica.
- Ndb\_api\_range\_scan\_count\_slave: Number of range scans that have been started by this replica.
- Ndb\_api\_read\_row\_count: Total number of rows that have been read by this MySQL Server (SQL node).
- Ndb\_api\_read\_row\_count\_session: Total number of rows that have been read in this client session.
- Ndb\_api\_read\_row\_count\_replica: Total number of rows that have been read by this replica.
- Ndb\_api\_read\_row\_count\_slave: Total number of rows that have been read by this replica.
- Ndb\_api\_scan\_batch\_count: Number of batches of rows received by this MySQL Server (SQL node).
- Ndb\_api\_scan\_batch\_count\_session: Number of batches of rows received in this client session.
- Ndb\_api\_scan\_batch\_count\_replica: Number of batches of rows received by this replica.
- Ndb\_api\_scan\_batch\_count\_slave: Number of batches of rows received by this replica.
- Ndb\_api\_table\_scan\_count: Number of table scans that have been started, including scans of internal tables, by this MySQL Server (SQL node).

- Ndb\_api\_table\_scan\_count\_session: Number of table scans that have been started, including scans of internal tables, in this client session.
- Ndb\_api\_table\_scan\_count\_replica: Number of table scans that have been started, including scans of internal tables, by this replica.
- Ndb\_api\_table\_scan\_count\_slave: Number of table scans that have been started, including scans of internal tables, by this replica.
- Ndb\_api\_trans\_abort\_count: Number of transactions aborted by this MySQL Server (SQL node).
- Ndb\_api\_trans\_abort\_count\_session: Number of transactions aborted in this client session.
- Ndb\_api\_trans\_abort\_count\_replica: Number of transactions aborted by this replica.
- Ndb\_api\_trans\_abort\_count\_slave: Number of transactions aborted by this replica.
- Ndb\_api\_trans\_close\_count: Number of transactions closed by this MySQL Server (SQL node); may be greater than sum of TransCommitCount and TransAbortCount.
- Ndb\_api\_trans\_close\_count\_session: Number of transactions aborted (may be greater than sum of TransCommitCount and TransAbortCount) in this client session.
- Ndb\_api\_trans\_close\_count\_replica: Number of transactions aborted (may be greater than sum of TransCommitCount and TransAbortCount) by this replica.
- Ndb\_api\_trans\_close\_count\_slave: Number of transactions aborted (may be greater than sum of TransCommitCount and TransAbortCount) by this replica.
- Ndb\_api\_trans\_commit\_count: Number of transactions committed by this MySQL Server (SQL node).
- Ndb\_api\_trans\_commit\_count\_session: Number of transactions committed in this client session.
- Ndb\_api\_trans\_commit\_count\_replica: Number of transactions committed by this replica.
- Ndb\_api\_trans\_commit\_count\_slave: Number of transactions committed by this replica.
- Ndb\_api\_trans\_local\_read\_row\_count: Total number of rows that have been read by this MySQL Server (SQL node).
- Ndb\_api\_trans\_local\_read\_row\_count\_session: Total number of rows that have been read in this client session.
- Ndb\_api\_trans\_local\_read\_row\_count\_replica: Total number of rows that have been read by this replica.
- Ndb\_api\_trans\_local\_read\_row\_count\_slave: Total number of rows that have been read by this replica.
- Ndb\_api\_trans\_start\_count: Number of transactions started by this MySQL Server (SQL node).
- Ndb\_api\_trans\_start\_count\_session: Number of transactions started in this client session.
- Ndb\_api\_trans\_start\_count\_replica: Number of transactions started by this replica.
- Ndb\_api\_trans\_start\_count\_slave: Number of transactions started by this replica.
- Ndb\_api\_uk\_op\_count: Number of operations based on or using unique keys by this MySQL Server (SQL node).

- Ndb\_api\_uk\_op\_count\_session: Number of operations based on or using unique keys in this client session.
- Ndb\_api\_uk\_op\_count\_replica: Number of operations based on or using unique keys by this replica.
- Ndb\_api\_uk\_op\_count\_slave: Number of operations based on or using unique keys by this replica.
- Ndb\_api\_wait\_exec\_complete\_count: Number of times thread has been blocked while waiting for operation execution to complete by this MySQL Server (SQL node).
- Ndb\_api\_wait\_exec\_complete\_count\_session: Number of times thread has been blocked while waiting for operation execution to complete in this client session.
- Ndb\_api\_wait\_exec\_complete\_count\_replica: Number of times thread has been blocked while waiting for operation execution to complete by this replica.
- Ndb\_api\_wait\_exec\_complete\_count\_slave: Number of times thread has been blocked while waiting for operation execution to complete by this replica.
- Ndb\_api\_wait\_meta\_request\_count: Number of times thread has been blocked waiting for metadata-based signal by this MySQL Server (SQL node).
- Ndb\_api\_wait\_meta\_request\_count\_session: Number of times thread has been blocked waiting for metadata-based signal in this client session.
- Ndb\_api\_wait\_meta\_request\_count\_replica: Number of times thread has been blocked waiting for metadata-based signal by this replica.
- Ndb\_api\_wait\_meta\_request\_count\_slave: Number of times thread has been blocked waiting for metadata-based signal by this replica.
- Ndb\_api\_wait\_nanos\_count: Total time (in nanoseconds) spent waiting for some type of signal from data nodes by this MySQL Server (SQL node).
- Ndb\_api\_wait\_nanos\_count\_session: Total time (in nanoseconds) spent waiting for some type of signal from data nodes in this client session.
- Ndb\_api\_wait\_nanos\_count\_replica: Total time (in nanoseconds) spent waiting for some type of signal from data nodes by this replica.
- Ndb\_api\_wait\_nanos\_count\_slave: Total time (in nanoseconds) spent waiting for some type of signal from data nodes by this replica.
- Ndb\_api\_wait\_scan\_result\_count: Number of times thread has been blocked while waiting for scan-based signal by this MySQL Server (SQL node).
- Ndb\_api\_wait\_scan\_result\_count\_session: Number of times thread has been blocked while waiting for scan-based signal in this client session.
- Ndb\_api\_wait\_scan\_result\_count\_replica: Number of times thread has been blocked while waiting for scan-based signal by this replica.
- Ndb\_api\_wait\_scan\_result\_count\_slave: Number of times thread has been blocked while waiting for scan-based signal by this replica.
- ndb\_autoincrement\_prefetch\_sz: NDB auto-increment prefetch size.
- ndb\_clear\_apply\_status: Causes RESET SLAVE/RESET REPLICA to clear all rows from ndb\_apply\_status table; ON by default.
- Ndb\_cluster\_node\_id: Node ID of this server when acting as NDB Cluster SQL node.

- Ndb\_config\_from\_host: NDB Cluster management server host name or IP address.
- Ndb\_config\_from\_port: Port for connecting to NDB Cluster management server.
- Ndb\_config\_generation: Generation number of the current configuration of the cluster.
- Ndb\_conflict\_fn\_epoch: Number of rows that have been found in conflict by NDB\$EPOCH() NDB replication conflict detection function.
- Ndb\_conflict\_fn\_epoch2: Number of rows that have been found in conflict by NDB replication NDB\$EPOCH2() conflict detection function.
- Ndb\_conflict\_fn\_epoch2\_trans: Number of rows that have been found in conflict by NDB replication NDB\$EPOCH2\_TRANS() conflict detection function.
- Ndb\_conflict\_fn\_epoch\_trans: Number of rows that have been found in conflict by NDB \$EPOCH\_TRANS() conflict detection function.
- Ndb\_conflict\_fn\_max: Number of times that NDB replication conflict resolution based on "greater timestamp wins" has been applied to update and delete operations.
- Ndb\_conflict\_fn\_max\_del\_win: Number of times that NDB replication conflict resolution based on outcome of NDB\$MAX\_DELETE\_WIN() has been applied to update and delete operations.
- Ndb\_conflict\_fn\_max\_ins: Number of times that NDB replication conflict resolution based on "greater timestamp wins" has been applied to insert operations.
- Ndb\_conflict\_fn\_max\_del\_win\_ins: Number of times that NDB replication conflict resolution based on outcome of NDB\$MAX\_DEL\_WIN\_INS() has been applied to insert operations.
- Ndb\_conflict\_fn\_old: Number of times that NDB replication "same timestamp wins" conflict resolution has been applied.
- Ndb\_conflict\_last\_conflict\_epoch: Most recent NDB epoch on this replica in which some conflict was detected.
- Ndb\_conflict\_last\_stable\_epoch: Most recent epoch containing no conflicts.
- Ndb\_conflict\_reflected\_op\_discard\_count: Number of reflected operations that were not applied due error during execution.
- Ndb\_conflict\_reflected\_op\_prepare\_count: Number of reflected operations received that have been prepared for execution.
- Ndb\_conflict\_refresh\_op\_count: Number of refresh operations that have been prepared.
- ndb\_conflict\_role: Role for replica to play in conflict detection and resolution. Value is one of PRIMARY, SECONDARY, PASS, or NONE (default). Can be changed only when replication SQL thread is stopped. See documentation for further information.
- Ndb\_conflict\_trans\_conflict\_commit\_count: Number of epoch transactions committed after requiring transactional conflict handling.
- Ndb\_conflict\_trans\_detect\_iter\_count: Number of internal iterations required to commit epoch transaction. Should be (slightly) greater than or equal to Ndb\_conflict\_trans\_conflict\_commit\_count.
- Ndb\_conflict\_trans\_reject\_count: Number of transactions rejected after being found in conflict by transactional conflict function.
- Ndb\_conflict\_trans\_row\_conflict\_count: Number of rows found in conflict by transactional conflict function. Includes any rows included in or dependent on conflicting transactions.

- Ndb\_conflict\_trans\_row\_reject\_count: Total number of rows realigned after being found in conflict by transactional conflict function. Includes Ndb\_conflict\_trans\_row\_conflict\_count and any rows included in or dependent on conflicting transactions.
- ndb\_data\_node\_neighbour: Specifies cluster data node "closest" to this MySQL Server, for transaction hinting and fully replicated tables.
- ndb\_default\_column\_format: Sets default row format and column format (FIXED or DYNAMIC) used for new NDB tables.
- ndb\_deferred\_constraints: Specifies that constraint checks should be deferred (where these are supported). Not normally needed or used; for testing purposes only.
- ndb\_dbg\_check\_shares: Check for any lingering shares (debug builds only).
- ndb-schema-dist-timeout: How long to wait before detecting timeout during schema distribution.
- ndb\_distribution: Default distribution for new tables in NDBCLUSTER (KEYHASH or LINHASH, default is KEYHASH).
- Ndb\_epoch\_delete\_delete\_count: Number of delete-delete conflicts detected (delete operation is applied, but row does not exist).
- ndb\_eventbuffer\_free\_percent: Percentage of free memory that should be available in event buffer before resumption of buffering, after reaching limit set by ndb\_eventbuffer\_max\_alloc.
- ndb\_eventbuffer\_max\_alloc: Maximum memory that can be allocated for buffering events by NDB API. Defaults to 0 (no limit).
- Ndb\_execute\_count: Number of round trips to NDB kernel made by operations.
- ndb\_extra\_logging: Controls logging of NDB Cluster schema, connection, and data distribution events in MySQL error log.
- Ndb\_fetch\_table\_stats: Number of times table statistics were fetched from tables rather than cache.
- ndb\_force\_send: Forces sending of buffers to NDB immediately, without waiting for other threads.
- ndb\_fully\_replicated: Whether new NDB tables are fully replicated.
- ndb\_index\_stat\_enable: Use NDB index statistics in query optimization.
- ndb\_index\_stat\_option: Comma-separated list of tunable options for NDB index statistics; list should contain no spaces.
- ndb\_join\_pushdown: Enables pushing down of joins to data nodes.
- Ndb\_last\_commit\_epoch\_server: Epoch most recently committed by NDB.
- Ndb\_last\_commit\_epoch\_session: Epoch most recently committed by this NDB client.
- ndb\_log\_apply\_status: Whether or not MySQL server acting as replica logs mysql.ndb\_apply\_status updates received from its immediate source in its own binary log, using its own server ID.
- ndb\_log\_bin: Write updates to NDB tables in binary log. Effective only if binary logging is enabled with --log-bin.
- ndb\_log\_binlog\_index: Insert mapping between epochs and binary log positions into ndb\_binlog\_index table. Defaults to ON. Effective only if binary logging is enabled.
- ndb\_log\_cache\_size: Set size of transaction cache used for recording NDB binary log.

- ndb\_log\_empty\_epochs: When enabled, epochs in which there were no changes are written to ndb\_apply\_status and ndb\_binlog\_index tables, even when log\_replica\_updates or log\_slave\_updates is enabled.
- ndb\_log\_empty\_update: When enabled, updates which produce no changes are written to ndb\_apply\_status and ndb\_binlog\_index tables, even when log\_replica\_updates or log\_slave\_updates is enabled.
- ndb\_log\_exclusive\_reads: Log primary key reads with exclusive locks; allow conflict resolution based on read conflicts.
- ndb\_log\_orig: Whether id and epoch of originating server are recorded in mysql.ndb\_binlog\_index table. Set using --ndb-log-orig option when starting mysqld.
- ndb\_log\_transaction\_id: Whether NDB transaction IDs are written into binary log (Read-only).
- ndb\_log\_transaction\_compression: Whether to compress NDB binary log; can also be enabled on startup by enabling --binlog-transaction-compression option.
- ndb\_log\_transaction\_compression\_level\_zstd: The ZSTD compression level to use when writing compressed transactions to the NDB binary log.
- ndb\_metadata\_check: Enable auto-detection of NDB metadata changes with respect to MySQL data dictionary; enabled by default.
- ndb\_metadata\_check\_interval: Interval in seconds to perform check for NDB metadata changes with respect to MySQL data dictionary.
- Ndb\_metadata\_detected\_count: Number of times NDB metadata change monitor thread has detected changes.
- Ndb\_metadata\_excluded\_count: Number of NDB metadata objects that NDB binlog thread has failed to synchronize.
- ndb\_metadata\_sync: Triggers immediate synchronization of all changes between NDB dictionary and MySQL data dictionary; causes ndb\_metadata\_check and ndb\_metadata\_check\_interval values to be ignored. Resets to false when synchronization is complete.
- Ndb\_metadata\_synced\_count: Number of NDB metadata objects which have been synchronized.
- Ndb\_number\_of\_data\_nodes: Number of data nodes in this NDB cluster; set only if server participates in cluster.
- ndb-optimization-delay: Number of milliseconds to wait between processing sets of rows by OPTIMIZE TABLE on NDB tables.
- ndb\_optimized\_node\_selection: Determines how SQL node chooses cluster data node to use as transaction coordinator.
- Ndb\_pruned\_scan\_count: Number of scans executed by NDB since cluster was last started where partition pruning could be used.
- Ndb\_pushed\_queries\_defined: Number of joins that API nodes have attempted to push down to data nodes.
- Ndb\_pushed\_queries\_dropped: Number of joins that API nodes have tried to push down, but failed.
- Ndb\_pushed\_queries\_executed: Number of joins successfully pushed down and executed on data nodes.
- Ndb\_pushed\_reads: Number of reads executed on data nodes by pushed-down joins.

- ndb\_read\_backup: Enable read from any replica for all NDB tables; use NDB\_TABLE=READ\_BACKUP={0|1} with CREATE TABLE or ALTER TABLE to enable or disable for individual NDB tables.
- ndb\_recv\_thread\_activation\_threshold: Activation threshold when receive thread takes over polling of cluster connection (measured in concurrently active threads).
- ndb\_recv\_thread\_cpu\_mask: CPU mask for locking receiver threads to specific CPUs; specified as hexadecimal. See documentation for details.
- Ndb\_replica\_max\_replicated\_epoch: Most recently committed NDB epoch on this replica. When this value is greater than or equal to Ndb\_conflict\_last\_conflict\_epoch, no conflicts have yet been detected.
- ndb\_replica\_batch\_size: Batch size in bytes for replica applier.
- ndb\_report\_thresh\_binlog\_epoch\_slip: NDB 7.5 and later: Threshold for number of epochs completely buffered, but not yet consumed by binlog injector thread which when exceeded generates BUFFERED\_EPOCHS\_OVER\_THRESHOLD event buffer status message; prior to NDB 7.5: Threshold for number of epochs to lag behind before reporting binary log status.
- ndb\_report\_thresh\_binlog\_mem\_usage: Threshold for percentage of free memory remaining before reporting binary log status.
- ndb\_row\_checksum: When enabled, set row checksums; enabled by default.
- Ndb\_scan\_count: Total number of scans executed by NDB since cluster was last started.
- ndb\_schema\_dist\_lock\_wait\_timeout: Time during schema distribution to wait for lock before returning error.
- ndb\_schema\_dist\_timeout: Time to wait before detecting timeout during schema distribution.
- ndb\_schema\_dist\_upgrade\_allowed: Allow schema distribution table upgrade when connecting to NDB.
- Ndb\_schema\_participant\_count: Number of MySQL servers participating in NDB schema change distribution.
- ndb\_show\_foreign\_key\_mock\_tables: Show mock tables used to support foreign\_key\_checks=0.
- ndb\_slave\_conflict\_role: Role for replica to play in conflict detection and resolution. Value is one of PRIMARY, SECONDARY, PASS, or NONE (default). Can be changed only when replication SQL thread is stopped. See documentation for further information.
- Ndb\_slave\_max\_replicated\_epoch: Most recently committed NDB epoch on this replica. When this value is greater than or equal to Ndb\_conflict\_last\_conflict\_epoch, no conflicts have yet been detected.
- Ndb\_system\_name: Configured cluster system name; empty if server not connected to NDB.
- ndb\_table\_no\_logging: NDB tables created when this setting is enabled are not checkpointed to disk (although table schema files are created). Setting in effect when table is created with or altered to use NDBCLUSTER persists for table's lifetime.
- ndb\_table\_temporary: NDB tables are not persistent on disk: no schema files are created and tables are not logged.
- Ndb\_trans\_hint\_count\_session: Number of transactions using hints that have been started in this session.
- ndb\_use\_copying\_alter\_table: Use copying ALTER TABLE operations in NDB Cluster.

- ndb\_use\_exact\_count: Forces NDB to use a count of records during SELECT COUNT(\*) query planning to speed up this type of query.
- ndb\_use\_transactions: Set to OFF, to disable transaction support by NDB. Not recommended except in certain special cases; see documentation for details.
- ndb\_version: Shows build and NDB engine version as an integer.
- ndb\_version\_string: Shows build information including NDB engine version in ndb-x.y.z format.
- ndbcluster: Enable NDB Cluster (if this version of MySQL supports it). Disabled by --skipndbcluster.
- ndbinfo: Enable ndbinfo plugin, if supported.
- ndbinfo\_database: Name used for NDB information database; read only.
- ndbinfo\_max\_bytes: Used for debugging only.
- ndbinfo\_max\_rows: Used for debugging only.
- ndbinfo\_offline: Put ndbinfo database into offline mode, in which no rows are returned from tables or views.
- ndbinfo\_show\_hidden: Whether to show ndbinfo internal base tables in mysql client; default is OFF.
- ndbinfo\_table\_prefix: Prefix to use for naming ndbinfo internal base tables; read only.
- ndbinfo\_version: ndbinfo engine version; read only.
- replica\_allow\_batching: Turns update batching on and off for replica.
- server\_id\_bits: Number of least significant bits in server\_id actually used for identifying server, permitting NDB API applications to store application data in most significant bits. server\_id must be less than 2 to power of this value.
- skip-ndbcluster: Disable NDB Cluster storage engine.
- slave\_allow\_batching: Turns update batching on and off for replica.
- transaction\_allow\_batching: Allows batching of statements within one transaction. Disable AUTOCOMMIT to use.

# <span id="page-131-0"></span>**25.4.3 NDB Cluster Configuration Files**

Configuring NDB Cluster requires working with two files:

- my.cnf: Specifies options for all NDB Cluster executables. This file, with which you should be familiar with from previous work with MySQL, must be accessible by each executable running in the cluster.
- config.ini: This file, sometimes known as the global configuration file, is read only by the NDB Cluster management server, which then distributes the information contained therein to all processes participating in the cluster. config.ini contains a description of each node involved in the cluster. This includes configuration parameters for data nodes and configuration parameters for connections between all nodes in the cluster. For a quick reference to the sections that can appear in this file, and what sorts of configuration parameters may be placed in each section, see [Sections of the](#page-134-0) [config.ini](#page-134-0) File.

**Caching of configuration data.** NDB uses stateful configuration. Rather than reading the global configuration file every time the management server is restarted, the management server caches the configuration the first time it is started, and thereafter, the global configuration file is read only when one of the following conditions is true:

- **The management server is started using the --initial option.** When --initial is used, the global configuration file is re-read, any existing cache files are deleted, and the management server creates a new configuration cache.
- **The management server is started using the --reload option.** The --reload option causes the management server to compare its cache with the global configuration file. If they differ, the management server creates a new configuration cache; any existing configuration cache is preserved, but not used. If the management server's cache and the global configuration file contain the same configuration data, then the existing cache is used, and no new cache is created.
- **The management server is started using --config-cache=FALSE.** This disables config-cache (enabled by default), and can be used to force the management server to bypass configuration caching altogether. In this case, the management server ignores any configuration files that may be present, always reading its configuration data from the config.ini file instead.
- **No configuration cache is found.** In this case, the management server reads the global configuration file and creates a cache containing the same configuration data as found in the file.

**Configuration cache files.** The management server by default creates configuration cache files in a directory named mysql-cluster in the MySQL installation directory. (If you build NDB Cluster from source on a Unix system, the default location is /usr/local/mysql-cluster.) This can be overridden at runtime by starting the management server with the --configdir option. Configuration cache files are binary files named according to the pattern ndb\_node\_id\_config.bin.seq\_id, where node\_id is the management server's node ID in the cluster, and seq\_id is a cache identifier. Cache files are numbered sequentially using seq\_id, in the order in which they are created. The management server uses the latest cache file as determined by the seq\_id.

![](_page_132_Picture_7.jpeg)

# **Note**

It is possible to roll back to a previous configuration by deleting later configuration cache files, or by renaming an earlier cache file so that it has a higher seq\_id. However, since configuration cache files are written in a binary format, you should not attempt to edit their contents by hand.

For more information about the --configdir, --config-cache, --initial, and --reload options for the NDB Cluster management server, see Section 25.5.4, "ndb\_mgmd — The NDB Cluster Management Server Daemon".

We are continuously making improvements in NDB Cluster configuration and attempting to simplify this process. Although we strive to maintain backward compatibility, there may be times when introduce an incompatible change. In such cases we try to let NDB Cluster users know in advance if a change is not backward compatible. If you find such a change and we have not documented it, please report it in the MySQL bugs database using the instructions given in Section 1.6, "How to Report Bugs or Problems".