---
source: MySQL 8.4 Reference
title: 00_Overview
---

The listing in this section provides information about parameters used in the [ndb\_mgmd] or [mgm] section of a config.ini file for configuring NDB Cluster management nodes. For detailed descriptions and other additional information about each of these parameters, see [Section 25.4.3.5,](#page-140-0) ["Defining an NDB Cluster Management Server".](#page-140-0)

- [ArbitrationDelay](#page-146-0): When asked to arbitrate, arbitrator waits this long before voting (milliseconds).
- [ArbitrationRank](#page-145-0): If 0, then management node is not arbitrator. Kernel selects arbitrators in order 1, 2.

- [DataDir](#page-146-1): Data directory for this node.
- [ExecuteOnComputer](#page-142-0): String referencing earlier defined COMPUTER.
- [ExtraSendBufferMemory](#page-147-0): Memory to use for send buffers in addition to any allocated by TotalSendBufferMemory or SendBufferMemory. Default (0) allows up to 16MB.
- [HeartbeatIntervalMgmdMgmd](#page-148-1): Time between management-node-to-management-node heartbeats; connection between management nodes is considered lost after 3 missed heartbeats.
- [HeartbeatThreadPriority](#page-147-1): Set heartbeat thread policy and priority for management nodes; see manual for allowed values.
- [HostName](#page-143-0): Host name or IP address for this management node.
- [Id](#page-141-0): Number identifying management node. Now deprecated; use NodeId instead.
- [LocationDomainId](#page-143-1): Assign this management node to specific availability domain or zone. 0 (default) leaves this unset.
- [LogDestination](#page-144-0): Where to send log messages: console, system log, or specified log file.
- [NodeId](#page-141-1): Number uniquely identifying management node among all nodes in cluster.
- [PortNumber](#page-142-1): Port number to send commands to and fetch configuration from management server.
- [PortNumberStats](#page-146-2): Port number used to get statistical information from management server.
- [RequireTls](#page-148-0): Client connection must authenticate with TLS before being used otherwise.
- [TotalSendBufferMemory](#page-148-2): Total memory to use for all transporter send buffers.
- [wan](#page-147-2): Use WAN TCP setting as default.

![](_page_118_Picture_16.jpeg)

### **Note**

After making changes in a management node's configuration, it is necessary to perform a rolling restart of the cluster for the new configuration to take effect. See [Section 25.4.3.5, "Defining an NDB Cluster Management Server",](#page-140-0) for more information.

To add new management servers to a running NDB Cluster, it is also necessary perform a rolling restart of all cluster nodes after modifying any existing config.ini files. For more information about issues arising when using multiple management nodes, see [Section 25.2.7.10, "Limitations Relating to](#page-80-0) [Multiple NDB Cluster Nodes"](#page-80-0).