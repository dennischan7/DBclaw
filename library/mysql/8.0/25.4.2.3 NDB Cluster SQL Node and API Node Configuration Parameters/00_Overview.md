---
source: MySQL 8.0 Reference
title: 00_Overview
---

The listing in this section provides information about parameters used in the [mysqld] and [api] sections of a config.ini file for configuring NDB Cluster SQL nodes and API nodes. For detailed descriptions and other additional information about each of these parameters, see [Section 25.4.3.7,](#page-162-1) ["Defining SQL and Other API Nodes in an NDB Cluster".](#page-162-1)

- [ApiVerbose](#page-172-0): Enable NDB API debugging; for NDB development.
- [ArbitrationDelay](#page-166-0): When asked to arbitrate, arbitrator waits this many milliseconds before voting.
- [ArbitrationRank](#page-166-1): If 0, then API node is not arbitrator. Kernel selects arbitrators in order 1, 2.

- [AutoReconnect](#page-169-0): Specifies whether an API node should reconnect fully when disconnected from cluster.
- [BatchByteSize](#page-167-0): Default batch size in bytes.
- [BatchSize](#page-167-1): Default batch size in number of records.
- [ConnectBackoffMaxTime](#page-171-0): Specifies longest time in milliseconds (~100ms resolution) to allow between connection attempts to any given data node by this API node. Excludes time elapsed while connection attempts are ongoing, which in worst case can take several seconds. Disable by setting to 0. If no data nodes are currently connected to this API node, StartConnectBackoffMaxTime is used instead.
- [ConnectionMap](#page-163-0): Specifies which data nodes to connect.
- [DefaultHashMapSize](#page-170-0): Set size (in buckets) to use for table hash maps. Three values are supported: 0, 240, and 3840.
- [DefaultOperationRedoProblemAction](#page-169-1): How operations are handled in event that RedoOverCommitCounter is exceeded.
- [ExecuteOnComputer](#page-164-0): String referencing earlier defined COMPUTER.
- [ExtraSendBufferMemory](#page-167-2): Memory to use for send buffers in addition to any allocated by TotalSendBufferMemory or SendBufferMemory. Default (0) allows up to 16MB.
- [HeartbeatThreadPriority](#page-168-0): Set heartbeat thread policy and priority for API nodes; see manual for allowed values.
- [HostName](#page-165-0): Host name or IP address for this SQL or API node.
- [Id](#page-163-1): Number identifying MySQL server or API node (Id). Now deprecated; use NodeId instead.
- [LocationDomainId](#page-165-1): Assign this API node to specific availability domain or zone. 0 (default) leaves this unset.
- [MaxScanBatchSize](#page-168-1): Maximum collective batch size for one scan.
- [NodeId](#page-164-1): Number uniquely identifying SQL node or API node among all nodes in cluster.
- [StartConnectBackoffMaxTime](#page-171-1): Same as ConnectBackoffMaxTime except that this parameter is used in its place if no data nodes are connected to this API node.
- [TotalSendBufferMemory](#page-169-2): Total memory to use for all transporter send buffers.
- [wan](#page-170-1): Use WAN TCP setting as default.

For a discussion of MySQL server options for NDB Cluster, see [MySQL Server Options for NDB](#page-174-1) [Cluster.](#page-174-1) For information about MySQL server system variables relating to NDB Cluster, see [NDB](#page-187-0) [Cluster System Variables](#page-187-0).

![](_page_34_Picture_20.jpeg)

#### **Note**

To add new SQL or API nodes to the configuration of a running NDB Cluster, it is necessary to perform a rolling restart of all cluster nodes after adding new [mysqld] or [api] sections to the config.ini file (or files, if you are using more than one management server). This must be done before the new SQL or API nodes can connect to the cluster.

It is not necessary to perform any restart of the cluster if new SQL or API nodes can employ previously unused API slots in the cluster configuration to connect to the cluster.