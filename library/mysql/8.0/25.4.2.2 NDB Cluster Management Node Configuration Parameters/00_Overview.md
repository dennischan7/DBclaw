---
source: MySQL 8.0 Reference
title: 00_Overview
---

The listing in this section provides information about parameters used in the [ndb\_mgmd] or [mgm] section of a config.ini file for configuring NDB Cluster management nodes. For detailed descriptions and other additional information about each of these parameters, see [Section 25.4.3.5,](#page-55-0) ["Defining an NDB Cluster Management Server".](#page-55-0)

- [ArbitrationDelay](#page-61-0): When asked to arbitrate, arbitrator waits this long before voting (milliseconds).
- [ArbitrationRank](#page-60-0): If 0, then management node is not arbitrator. Kernel selects arbitrators in order 1, 2.
- [DataDir](#page-61-1): Data directory for this node.
- [ExecuteOnComputer](#page-57-0): String referencing earlier defined COMPUTER.
- [ExtraSendBufferMemory](#page-62-0): Memory to use for send buffers in addition to any allocated by TotalSendBufferMemory or SendBufferMemory. Default (0) allows up to 16MB.
- [HeartbeatIntervalMgmdMgmd](#page-63-0): Time between management-node-to-management-node heartbeats; connection between management nodes is considered lost after 3 missed heartbeats.
- [HeartbeatThreadPriority](#page-62-1): Set heartbeat thread policy and priority for management nodes; see manual for allowed values.
- [HostName](#page-58-0): Host name or IP address for this management node.
- [Id](#page-56-0): Number identifying management node. Now deprecated; use NodeId instead.
- [LocationDomainId](#page-58-1): Assign this management node to specific availability domain or zone. 0 (default) leaves this unset.
- [LogDestination](#page-59-0): Where to send log messages: console, system log, or specified log file.
- [NodeId](#page-56-1): Number uniquely identifying management node among all nodes in cluster.
- [PortNumber](#page-57-1): Port number to send commands to and fetch configuration from management server.
- [PortNumberStats](#page-61-2): Port number used to get statistical information from management server.
- [TotalSendBufferMemory](#page-63-1): Total memory to use for all transporter send buffers.
- [wan](#page-62-2): Use WAN TCP setting as default.

![](_page_33_Picture_17.jpeg)

#### **Note**

After making changes in a management node's configuration, it is necessary to perform a rolling restart of the cluster for the new configuration to take effect. See [Section 25.4.3.5, "Defining an NDB Cluster Management Server",](#page-55-0) for more information.

To add new management servers to a running NDB Cluster, it is also necessary perform a rolling restart of all cluster nodes after modifying any existing config.ini files. For more information about issues arising when using multiple management nodes, see Section 25.2.7.10, "Limitations Relating to Multiple NDB Cluster Nodes".