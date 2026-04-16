---
source: PostgreSQL 16 Reference
title: 00_Overview
---

These parameters can be set on the primary server that is to send replication data to one or more standby servers. Note that in addition to these parameters, [wal\\_level](#page-60-1) must be set appropriately on the primary server, and optionally WAL archiving can be enabled as well (see [Section 20.5.3\)](#page-66-3). The values of these parameters on standby servers are irrelevant, although you may wish to set them there in preparation for the possibility of a standby becoming the primary.

```
synchronous_standby_names (string)
```

Specifies a list of standby servers that can support *synchronous replication*, as described in Section 27.2.8. There will be one or more active synchronous standbys; transactions waiting for commit will be allowed to proceed after these standby servers confirm receipt of their data. The synchronous standbys will be those whose names appear in this list, and that are both currently connected and streaming data in real-time (as shown by a state of streaming in the pg\_stat\_replication view). Specifying more than one synchronous standby can allow for very high availability and protection against data loss.

The name of a standby server for this purpose is the application\_name setting of the standby, as set in the standby's connection information. In case of a physical replication standby, this should be set in the primary\_conninfo setting; the default is the setting of [cluster\\_name](#page-97-0) if set, else walreceiver. For logical replication, this can be set in the connection information of the subscription, and it defaults to the subscription name. For other replication stream consumers, consult their documentation.

This parameter specifies a list of standby servers using either of the following syntaxes:

```
[FIRST] num_sync ( standby_name [, ...] )
ANY num_sync ( standby_name [, ...] )
standby_name [, ...]
```

where num\_sync is the number of synchronous standbys that transactions need to wait for replies from, and standby\_name is the name of a standby server. FIRST and ANY specify the method to choose synchronous standbys from the listed servers.

The keyword FIRST, coupled with num\_sync, specifies a priority-based synchronous replication and makes transaction commits wait until their WAL records are replicated to num\_sync synchronous standbys chosen based on their priorities. For example, a setting of FIRST 3 (s1, s2, s3, s4) will cause each commit to wait for replies from three higher-priority standbys chosen from standby servers s1, s2, s3 and s4. The standbys whose names appear earlier in the list are given higher priority and will be considered as synchronous. Other standby servers appearing later in this list represent potential synchronous standbys. If any of the current synchronous standbys disconnects for whatever reason, it will be replaced immediately with the nexthighest-priority standby. The keyword FIRST is optional.

The keyword ANY, coupled with num\_sync, specifies a quorum-based synchronous replication and makes transaction commits wait until their WAL records are replicated to *at least* num\_sync listed standbys. For example, a setting of ANY 3 (s1, s2, s3, s4) will cause each commit to proceed as soon as at least any three standbys of s1, s2, s3 and s4 reply.

FIRST and ANY are case-insensitive. If these keywords are used as the name of a standby server, its standby\_name must be double-quoted.

The third syntax was used before PostgreSQL version 9.6 and is still supported. It's the same as the first syntax with FIRST and num\_sync equal to 1. For example, FIRST 1 (s1, s2) and s1, s2 have the same meaning: either s1 or s2 is chosen as a synchronous standby.

The special entry \* matches any standby name.

There is no mechanism to enforce uniqueness of standby names. In case of duplicates one of the matching standbys will be considered as higher priority, though exactly which one is indeterminate.

### **Note**

Each standby\_name should have the form of a valid SQL identifier, unless it is \*. You can use double-quoting if necessary. But note that standby\_names are compared to standby application names case-insensitively, whether double-quoted or not.

If no synchronous standby names are specified here, then synchronous replication is not enabled and transaction commits will not wait for replication. This is the default configuration. Even when synchronous replication is enabled, individual transactions can be configured not to wait for replication by setting the [synchronous\\_commit](#page-61-0) parameter to local or off.

This parameter can only be set in the postgresql.conf file or on the server command line.

## <span id="page-73-0"></span>**20.6.3. Standby Servers**

These settings control the behavior of a standby server that is to receive replication data. Their values on the primary server are irrelevant.

```
primary_conninfo (string)
```

Specifies a connection string to be used for the standby server to connect with a sending server. This string is in the format described in Section 34.1.1. If any option is unspecified in this string, then the corresponding environment variable (see Section 34.15) is checked. If the environment variable is not set either, then defaults are used.

The connection string should specify the host name (or address) of the sending server, as well as the port number if it is not the same as the standby server's default. Also specify a user name corresponding to a suitably-privileged role on the sending server (see Section 27.2.5.1). A password needs to be provided too, if the sender demands password authentication. It can be provided in the primary\_conninfo string, or in a separate ~/.pgpass file on the standby server (use replication as the database name). Do not specify a database name in the primary\_conninfo string.

This parameter can only be set in the postgresql.conf file or on the server command line. If this parameter is changed while the WAL receiver process is running, that process is signaled to shut down and expected to restart with the new setting (except if primary\_conninfo is an empty string). This setting has no effect if the server is not in standby mode.

```
primary_slot_name (string)
```

Optionally specifies an existing replication slot to be used when connecting to the sending server via streaming replication to control resource removal on the upstream node (see Section 27.2.6). This parameter can only be set in the postgresql.conf file or on the server command line. If this parameter is changed while the WAL receiver process is running, that process is signaled to shut down and expected to restart with the new setting. This setting has no effect if primary\_conninfo is not set or the server is not in standby mode.

```
hot_standby (boolean)
```

Specifies whether or not you can connect and run queries during recovery, as described in Section 27.4. The default value is on. This parameter can only be set at server start. It only has effect during archive recovery or in standby mode.

```
max_standby_archive_delay (integer)
```

When hot standby is active, this parameter determines how long the standby server should wait before canceling standby queries that conflict with about-to-be-applied WAL entries, as described in Section 27.4.2. max\_standby\_archive\_delay applies when WAL data is being read from WAL archive (and is therefore not current). If this value is specified without units, it is taken as milliseconds. The default is 30 seconds. A value of -1 allows the standby to wait forever for conflicting queries to complete. This parameter can only be set in the postgresql.conf file or on the server command line.

Note that max\_standby\_archive\_delay is not the same as the maximum length of time a query can run before cancellation; rather it is the maximum total time allowed to apply any one WAL segment's data. Thus, if one query has resulted in significant delay earlier in the WAL segment, subsequent conflicting queries will have much less grace time.

```
max_standby_streaming_delay (integer)
```

When hot standby is active, this parameter determines how long the standby server should wait before canceling standby queries that conflict with about-to-be-applied WAL entries, as described in Section 27.4.2. max\_standby\_streaming\_delay applies when WAL data is being received via streaming replication. If this value is specified without units, it is taken as milliseconds. The default is 30 seconds. A value of -1 allows the standby to wait forever for conflicting queries to complete. This parameter can only be set in the postgresql.conf file or on the server command line.

Note that max\_standby\_streaming\_delay is not the same as the maximum length of time a query can run before cancellation; rather it is the maximum total time allowed to apply WAL data once it has been received from the primary server. Thus, if one query has resulted in significant delay, subsequent conflicting queries will have much less grace time until the standby server has caught up again.

```
wal_receiver_create_temp_slot (boolean)
```

Specifies whether the WAL receiver process should create a temporary replication slot on the remote instance when no permanent replication slot to use has been configured (using [primary\\_s](#page-73-2)[lot\\_name](#page-73-2)). The default is off. This parameter can only be set in the postgresql.conf file or on the server command line. If this parameter is changed while the WAL receiver process is running, that process is signaled to shut down and expected to restart with the new setting.

```
wal_receiver_status_interval (integer)
```

Specifies the minimum frequency for the WAL receiver process on the standby to send information about replication progress to the primary or upstream standby, where it can be seen using the pg\_stat\_replication view. The standby will report the last write-ahead log location it has written, the last position it has flushed to disk, and the last position it has applied. This parameter's value is the maximum amount of time between reports. Updates are sent each time the write or flush positions change, or as often as specified by this parameter if set to a non-zero value. There are additional cases where updates are sent while ignoring this parameter; for example, when processing of the existing WAL completes or when synchronous\_commit is set to remote\_apply. Thus, the apply position may lag slightly behind the true position. If this value is specified without units, it is taken as seconds. The default value is 10 seconds. This parameter can only be set in the postgresql.conf file or on the server command line.

```
hot_standby_feedback (boolean)
```

Specifies whether or not a hot standby will send feedback to the primary or upstream standby about queries currently executing on the standby. This parameter can be used to eliminate query cancels caused by cleanup records, but can cause database bloat on the primary for some workloads. Feedback messages will not be sent more frequently than once per wal\_receiver\_status\_interval. The default value is off. This parameter can only be set in the postgresql.conf file or on the server command line.

If cascaded replication is in use the feedback is passed upstream until it eventually reaches the primary. Standbys make no other use of feedback they receive other than to pass upstream.

This setting does not override the behavior of old\_snapshot\_threshold on the primary; a snapshot on the standby which exceeds the primary's age threshold can become invalid, resulting in cancellation of transactions on the standby. This is because old\_snapshot\_threshold is intended to provide an absolute limit on the time which dead rows can contribute to bloat, which would otherwise be violated because of the configuration of a standby.

```
wal_receiver_timeout (integer)
```

Terminate replication connections that are inactive for longer than this amount of time. This is useful for the receiving standby server to detect a primary node crash or network outage. If this value is specified without units, it is taken as milliseconds. The default value is 60 seconds. A value of zero disables the timeout mechanism. This parameter can only be set in the postgresql.conf file or on the server command line.

```
wal_retrieve_retry_interval (integer)
```

Specifies how long the standby server should wait when WAL data is not available from any sources (streaming replication, local pg\_wal or WAL archive) before trying again to retrieve WAL data. If this value is specified without units, it is taken as milliseconds. The default value is 5 seconds. This parameter can only be set in the postgresql.conf file or on the server command line.

This parameter is useful in configurations where a node in recovery needs to control the amount of time to wait for new WAL data to be available. For example, in archive recovery, it is possible to make the recovery more responsive in the detection of a new WAL file by reducing the value of this parameter. On a system with low WAL activity, increasing it reduces the amount of requests necessary to access WAL archives, something useful for example in cloud environments where the number of times an infrastructure is accessed is taken into account.

In logical replication, this parameter also limits how often a failing replication apply worker will be respawned.

```
recovery_min_apply_delay (integer)
```

By default, a standby server restores WAL records from the sending server as soon as possible. It may be useful to have a time-delayed copy of the data, offering opportunities to correct data loss errors. This parameter allows you to delay recovery by a specified amount of time. For example, if you set this parameter to 5min, the standby will replay each transaction commit only when the system time on the standby is at least five minutes past the commit time reported by the primary. If this value is specified without units, it is taken as milliseconds. The default is zero, adding no delay.

It is possible that the replication delay between servers exceeds the value of this parameter, in which case no delay is added. Note that the delay is calculated between the WAL time stamp as written on primary and the current time on the standby. Delays in transfer because of network lag or cascading replication configurations may reduce the actual wait time significantly. If the system clocks on primary and standby are not synchronized, this may lead to recovery applying records earlier than expected; but that is not a major issue because useful settings of this parameter are much larger than typical time deviations between servers.

The delay occurs only on WAL records for transaction commits. Other records are replayed as quickly as possible, which is not a problem because MVCC visibility rules ensure their effects are not visible until the corresponding commit record is applied.

The delay occurs once the database in recovery has reached a consistent state, until the standby is promoted or triggered. After that the standby will end recovery without further waiting.

WAL records must be kept on the standby until they are ready to be applied. Therefore, longer delays will result in a greater accumulation of WAL files, increasing disk space requirements for the standby's pg\_wal directory.

This parameter is intended for use with streaming replication deployments; however, if the parameter is specified it will be honored in all cases except crash recovery. hot\_standby\_feedback will be delayed by use of this feature which could lead to bloat on the primary; use both together with care.

### **Warning**

Synchronous replication is affected by this setting when synchronous\_commit is set to remote\_apply; every COMMIT will need to wait to be applied.

This parameter can only be set in the postgresql.conf file or on the server command line.