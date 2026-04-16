---
source: MySQL 5.7 Reference
title: 00_Overview
---

TCP/IP is the default transport mechanism for all connections between nodes in an NDB Cluster. Normally it is not necessary to define TCP/IP connections; NDB Cluster automatically sets up such connections for all data nodes, management nodes, and SQL or API nodes.

![](_page_155_Picture_7.jpeg)

#### **Note**

For an exception to this rule, see [Section 21.4.3.11, "NDB Cluster TCP/IP](#page-161-0) [Connections Using Direct Connections".](#page-161-0)

To override the default connection parameters, it is necessary to define a connection using one or more [tcp] sections in the config.ini file. Each [tcp] section explicitly defines a TCP/IP connection between two NDB Cluster nodes, and must contain at a minimum the parameters [NodeId1](#page-156-0) and [NodeId2](#page-157-1), as well as any connection parameters to override.

It is also possible to change the default values for these parameters by setting them in the [tcp default] section.

![](_page_155_Picture_12.jpeg)

### **Important**

Any [tcp] sections in the config.ini file should be listed last, following all other sections in the file. However, this is not required for a [tcp default] section. This requirement is a known issue with the way in which the config.ini file is read by the NDB Cluster management server.

Connection parameters which can be set in [tcp] and [tcp default] sections of the config.ini file are listed here:

# <span id="page-155-2"></span>• Checksum

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

This parameter is a boolean parameter (enabled by setting it to Y or 1, disabled by setting it to N or 0). It is disabled by default. When it is enabled, checksums for all messages are calculated before they placed in the send buffer. This feature ensures that messages are not corrupted while waiting in the send buffer, or by the transport mechanism.

<span id="page-155-1"></span>• Group

When [ndb\\_optimized\\_node\\_selection](#page-131-2) is enabled, node proximity is used in some cases to select which node to connect to. This parameter can be used to influence proximity by setting it to a lower value, which is interpreted as "closer". See the description of the system variable for more information.

### <span id="page-156-2"></span>• HostName1

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

The HostName1 and [HostName2](#page-156-1) parameters can be used to specify specific network interfaces to be used for a given TCP connection between two nodes. The values used for these parameters can be host names or IP addresses.

### <span id="page-156-1"></span>• HostName2

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

The [HostName1](#page-156-2) and HostName2 parameters can be used to specify specific network interfaces to be used for a given TCP connection between two nodes. The values used for these parameters can be host names or IP addresses.

### <span id="page-156-0"></span>• NodeId1

| Version (or<br>later) | NDB 7.5.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | numeric                                        |
| Default               | [none]                                         |
| Range                 | 1 - 255                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 7.5.0)

To identify a connection between two nodes it is necessary to provide their node IDs in the [tcp] section of the configuration file as the values of NodeId1 and [NodeId2](#page-157-1). These are the same unique Id values for each of these nodes as described in [Section 21.4.3.7, "Defining SQL and Other API](#page-98-1) [Nodes in an NDB Cluster"](#page-98-1).

### <span id="page-157-1"></span>• NodeId2

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | [none]                                                                           |
| Range                 | 1 - 255                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

To identify a connection between two nodes it is necessary to provide their node IDs in the [tcp] section of the configuration file as the values of [NodeId1](#page-156-0) and NodeId2. These are the same unique Id values for each of these nodes as described in [Section 21.4.3.7, "Defining SQL and Other API](#page-98-1) [Nodes in an NDB Cluster"](#page-98-1).

### <span id="page-157-2"></span>• [NodeIdServer](#page-157-2)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | [none]                                                                           |
| Range                 | 1 - 63                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Set the server side of a TCP connection.

# <span id="page-157-0"></span>• OverloadLimit

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

When more than this many unsent bytes are in the send buffer, the connection is considered overloaded.

This parameter can be used to determine the amount of unsent data that must be present in the send buffer before the connection is considered overloaded. See [Section 21.4.3.13, "Configuring](#page-170-0) [NDB Cluster Send Buffer Parameters",](#page-170-0) for more information.

## • PortNumber (OBSOLETE)

This parameter formerly specified the port number to be used for listening for connections from other nodes. It is now deprecated (and removed in NDB Cluster 7.5); use the [ServerPort](#page-12-0) data node configuration parameter for this purpose instead (Bug #77405, Bug #21280456).

### <span id="page-158-0"></span>• [PreSendChecksum](#page-158-0)

| Version (or<br>later) | NDB 7.6.6                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Added                 | NDB 7.6.6                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

If this parameter and [Checksum](#page-155-2) are both enabled, perform pre-send checksum checks, and check all TCP signals between nodes for errors. Has no effect if Checksum is not also enabled.

### <span id="page-158-1"></span>• [Proxy](#page-158-1)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | string                                                                           |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Set a proxy for the TCP connection.

### <span id="page-158-2"></span>• [ReceiveBufferMemory](#page-158-2)

| Version (or<br>later) | NDB 7.5.0                           |
|-----------------------|-------------------------------------|
| Type or units         | bytes                               |
| Default               | 2M                                  |
| Range                 | 16K -<br>4294967039<br>(0xFFFFFEFF) |

| Restart Type | Node Restart:   |
|--------------|-----------------|
|              | Requires a      |
|              | rolling restart |
|              | of the cluster. |
|              | (NDB 7.5.0)     |

Specifies the size of the buffer used when receiving data from the TCP/IP socket.

The default value of this parameter is 2MB. The minimum possible value is 16KB; the theoretical maximum is 4GB.

### <span id="page-159-0"></span>• [SendBufferMemory](#page-159-0)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 2M                                                                               |
| Range                 | 256K -<br>4294967039<br>(0xFFFFFEFF)                                             |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

TCP transporters use a buffer to store all messages before performing the send call to the operating system. When this buffer reaches 64KB its contents are sent; these are also sent when a round of messages have been executed. To handle temporary overload situations it is also possible to define a bigger send buffer.

If this parameter is set explicitly, then the memory is not dedicated to each transporter; instead, the value used denotes the hard limit for how much memory (out of the total available memory —that is, TotalSendBufferMemory) that may be used by a single transporter. For more information about configuring dynamic transporter send buffer memory allocation in NDB Cluster, see [Section 21.4.3.13, "Configuring NDB Cluster Send Buffer Parameters"](#page-170-0).

The default size of the send buffer is 2MB, which is the size recommended in most situations. The minimum size is 64 KB; the theoretical maximum is 4 GB.

### • SendSignalId

| Version (or<br>later) | NDB 7.5.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | boolean                                        |
| Default               | false (debug<br>builds: true)                  |
| Range                 | true, false                                    |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 7.5.0)

To be able to retrace a distributed message datagram, it is necessary to identify each message. When this parameter is set to Y, message IDs are transported over the network. This feature is disabled by default in production builds, and enabled in -debug builds.

• TcpBind\_INADDR\_ANY

Setting this parameter to TRUE or 1 binds IP\_ADDR\_ANY so that connections can be made from anywhere (for autogenerated connections). The default is FALSE (0).

<span id="page-160-0"></span>• [TCP\\_MAXSEG\\_SIZE](#page-160-0)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 0 - 2G                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Determines the size of the memory set during TCP transporter initialization. The default is recommended for most common usage cases.

### <span id="page-160-1"></span>• [TCP\\_RCV\\_BUF\\_SIZE](#page-160-1)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 0 - 2G                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Determines the size of the receive buffer set during TCP transporter initialization. The default and minimum value is 0, which allows the operating system or platform to set this value. The default is recommended for most common usage cases.

# <span id="page-160-2"></span>• [TCP\\_SND\\_BUF\\_SIZE](#page-160-2)

| Version (or<br>later) | NDB 7.5.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | unsigned                                       |
| Default               | 0                                              |
| Range                 | 0 - 2G                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 7.5.0)

Determines the size of the send buffer set during TCP transporter initialization. The default and minimum value is 0, which allows the operating system or platform to set this value. The default is recommended for most common usage cases.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 21.19 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 21.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |

# <span id="page-161-0"></span>**21.4.3.11 NDB Cluster TCP/IP Connections Using Direct Connections**

Setting up a cluster using direct connections between data nodes requires specifying explicitly the crossover IP addresses of the data nodes so connected in the [tcp] section of the cluster config.ini file.

In the following example, we envision a cluster with at least four hosts, one each for a management server, an SQL node, and two data nodes. The cluster as a whole resides on the 172.23.72.\* subnet of a LAN. In addition to the usual network connections, the two data nodes are connected directly using a standard crossover cable, and communicate with one another directly using IP addresses in the 1.1.0.\* address range as shown:

```
# Management Server
[ndb_mgmd]
Id=1
HostName=172.23.72.20
# SQL Node
[mysqld]
Id=2
HostName=172.23.72.21
# Data Nodes
[ndbd]
Id=3
HostName=172.23.72.22
[ndbd]
Id=4
HostName=172.23.72.23
# TCP/IP Connections
[tcp]
NodeId1=3
NodeId2=4
HostName1=1.1.0.1
HostName2=1.1.0.2
```

The [HostName1](#page-156-2) and [HostName2](#page-156-1) parameters are used only when specifying direct connections.

The use of direct TCP connections between data nodes can improve the cluster's overall efficiency by enabling the data nodes to bypass an Ethernet device such as a switch, hub, or router, thus cutting down on the cluster's latency.

![](_page_162_Picture_2.jpeg)

#### **Note**

To take the best advantage of direct connections in this fashion with more than two data nodes, you must have a direct connection between each data node and every other data node in the same node group.

# <span id="page-162-0"></span>**21.4.3.12 NDB Cluster Shared Memory Connections**

Communications between NDB cluster nodes are normally handled using TCP/IP. The shared memory (SHM) transporter is distinguished by the fact that signals are transmitted by writing in memory rather than on a socket. The shared-memory transporter (SHM) can improve performance by negating up to 20% of the overhead required by a TCP connection when running an API node (usually an SQL node) and a data node together on the same host. You can enable a shared memory connection in either of the two ways listed here:

- By setting the [UseShm](#page-46-0) data node configuration parameter to 1, and setting [HostName](#page-11-0) for the data node and [HostName](#page-101-0) for the API node to the same value.
- By using [shm] sections in the cluster configuration file, each containing settings for [NodeId1](#page-165-0) and [NodeId2](#page-165-1). This method is described in more detail later in this section.

Suppose a cluster is running a data node which has node ID 1 and an SQL node having node ID 51 on the same host computer at 10.0.0.1. To enable an SHM connection between these two nodes, all that is necessary is to insure that the following entries are included in the cluster configuration file:

```
[ndbd]
NodeId=1
HostName=10.0.0.1
UseShm=1
[mysqld]
NodeId=51
HostName=10.0.0.1
```

![](_page_162_Picture_11.jpeg)

### **Important**

The two entries just shown are in addition to any other entries and parameter settings needed by the cluster. A more complete example is shown later in this section.

Before starting data nodes that use SHM connections, it is also necessary to make sure that the operating system on each computer hosting such a data node has sufficient memory allocated to shared memory segments. See the documentation for your operating platform for information regarding this. In setups where multiple hosts are each running a data node and an API node, it is possible to enable shared memory on all such hosts by setting UseShm in the [ndbd default] section of the configuration file. This is shown in the example later in this section.

While not strictly required, tuning for all SHM connections in the cluster can be done by setting one or more of the following parameters in the [shm default] section of the cluster configuration (config.ini) file:

- [ShmSize](#page-168-0): Shared memory size
- [ShmSpinTime](#page-169-0): Time in µs to spin before sleeping
- [SendBufferMemory](#page-167-0): Size of buffer for signals sent from this node, in bytes.
- [SendSignalId](#page-167-1): Indicates that a signal ID is included in each signal sent through the transporter.

- [Checksum](#page-164-0): Indicates that a checksum is included in each signal sent through the transporter.
- [PreSendChecksum](#page-167-2): Checks of the checksum are made prior to sending the signal; Checksum must also be enabled for this to work

This example shows a simple setup with SHM connections definied on multiple hosts, in an NDB Cluster using 3 computers listed here by host name, hosting the node types shown:

- 1. 10.0.0.0: The management server
- 2. 10.0.0.1: A data node and an SQL node
- 3. 10.0.0.2: A data node and an SQL node

In this scenario, each data node communicates with both the management server and the other data node using TCP transporters; each SQL node uses a shared memory transporter to communicate with the data nodes that is local to it, and a TCP transporter to communicate with the remote data node. A basic configuration reflecting this setup is enabled by the config.ini file whose contents are shown here:

```
[ndbd default]
DataDir=/path/to/datadir
UseShm=1
[shm default]
ShmSize=8M
ShmSpintime=200
SendBufferMemory=4M
[tcp default]
SendBufferMemory=8M
[ndb_mgmd]
NodeId=49
Hostname=10.0.0.0
DataDir=/path/to/datadir
[ndbd]
NodeId=1
Hostname=10.0.0.1
DataDir=/path/to/datadir
[ndbd]
NodeId=2
Hostname=10.0.0.2
DataDir=/path/to/datadir
[mysqld]
NodeId=51
Hostname=10.0.0.1
[mysqld]
NodeId=52
Hostname=10.0.0.2
[api]
[api]
```

Parameters affecting all shared memory transporters are set in the [shm default] section; these can be overridden on a per-connection basis in one or more [shm] sections. Each such section must be associated with a given SHM connection using [NodeId1](#page-165-0) and [NodeId2](#page-165-1); the values required for these parameters are the node IDs of the two nodes connected by the transporter. You can also identify the nodes by host name using [HostName1](#page-164-1) and [HostName2](#page-165-2), but these parameters are not required.

The API nodes for which no host names are set use the TCP transporter to communicate with data nodes independent of the hosts on which they are started; the parameters and values set in the [tcp default] section of the configuration file apply to all TCP transporters in the cluster.

For optimum performance, you can define a spin time for the SHM transporter ([ShmSpinTime](#page-169-0) parameter); this affects both the data node receiver thread and the poll owner (receive thread or user thread) in NDB.

### <span id="page-164-0"></span>• Checksum

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | true                                                                             |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

This parameter is a boolean (Y/N) parameter which is disabled by default. When it is enabled, checksums for all messages are calculated before being placed in the send buffer.

This feature prevents messages from being corrupted while waiting in the send buffer. It also serves as a check against data being corrupted during transport.

### • Group

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 35                                                                               |
| Range                 | 0 - 200                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Determines the group proximity; a smaller value is interpreted as being closer. The default value is sufficient for most conditions.

# <span id="page-164-1"></span>• HostName1

| Version (or<br>later) | NDB 7.5.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | name or IP<br>address                          |
| Default               | []                                             |
| Range                 |                                                |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

| of the cluster. |
|-----------------|
| (NDB 7.5.0)     |

The HostName1 and [HostName2](#page-165-2) parameters can be used to specify specific network interfaces to be used for a given SHM connection between two nodes. The values used for these parameters can be host names or IP addresses.

### <span id="page-165-2"></span>• HostName2

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

The [HostName1](#page-164-1) and HostName2 parameters can be used to specify specific network interfaces to be used for a given SHM connection between two nodes. The values used for these parameters can be host names or IP addresses.

### <span id="page-165-0"></span>• NodeId1

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | [none]                                                                           |
| Range                 | 1 - 255                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

To identify a connection between two nodes it is necessary to provide node identifiers for each of them, as NodeId1 and [NodeId2](#page-165-1).

# <span id="page-165-1"></span>• NodeId2

| Version (or<br>later) | NDB 7.5.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | numeric                                        |
| Default               | [none]                                         |
| Range                 | 1 - 255                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

| of the cluster. |
|-----------------|
| (NDB 7.5.0)     |

To identify a connection between two nodes it is necessary to provide node identifiers for each of them, as [NodeId1](#page-165-0) and NodeId2.

### • NodeIdServer

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | [none]                                                                           |
| Range                 | 1 - 63                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Identify the server end of a shared memory connection. By default, this is the node ID of the data node.

### • OverloadLimit

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

When more than this many unsent bytes are in the send buffer, the connection is considered overloaded.

This parameter can be used to determine the amount of unsent data that must be present in the send buffer before the connection is considered overloaded. See [Section 21.4.3.13, "Configuring](#page-170-0) [NDB Cluster Send Buffer Parameters",](#page-170-0) and Section 21.6.15.44, "The ndbinfo transporters Table", for more information.

### <span id="page-166-0"></span>• [PortNumber](#page-166-0)

| Version (or<br>later) | NDB 7.5.0          |
|-----------------------|--------------------|
| Type or units         | unsigned           |
| Default               | []                 |
| Range                 | 0 - 64K            |
| Removed               | NDB 7.5.1          |
| Restart Type          | System<br>Restart: |

| Requires a     |
|----------------|
| complete       |
| shutdown and   |
| restart of the |
| cluster. (NDB  |
| 7.5.0)         |
|                |

Set the port to be used by the SHM transporter.

### <span id="page-167-2"></span>• [PreSendChecksum](#page-167-2)

| Version (or<br>later) | NDB 7.6.6                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Added                 | NDB 7.6.6                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

If this parameter and [Checksum](#page-164-0) are both enabled, perform pre-send checksum checks, and check all SHM signals between nodes for errors. Has no effect if Checksum is not also enabled.

### <span id="page-167-0"></span>• [SendBufferMemory](#page-167-0)

| Version (or<br>later) | NDB 7.6.6                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 2M                                                                               |
| Range                 | 256K -<br>4294967039<br>(0xFFFFFEFF)                                             |
| Added                 | NDB 7.6.6                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Size (in bytes) of the shared memory buffer for signals sent from this node using a shared memory connection.

### <span id="page-167-1"></span>• SendSignalId

| Version (or<br>later) | NDB 7.5.0   |
|-----------------------|-------------|
| Type or units         | boolean     |
| Default               | false       |
| Range                 | true, false |

| Restart Type | Node Restart:   |
|--------------|-----------------|
|              | Requires a      |
|              | rolling restart |
|              | of the cluster. |
|              | (NDB 7.5.0)     |

To retrace the path of a distributed message, it is necessary to provide each message with a unique identifier. Setting this parameter to Y causes these message IDs to be transported over the network as well. This feature is disabled by default in production builds, and enabled in -debug builds.

### <span id="page-168-1"></span>• [ShmKey](#page-168-1)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

When setting up shared memory segments, a node ID, expressed as an integer, is used to identify uniquely the shared memory segment to use for the communication. There is no default value. If [UseShm](#page-46-0) is enabled, the shared memory key is calculated automatically by NDB.

### <span id="page-168-0"></span>• [ShmSize](#page-168-0)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 1M                                                                               |
| Range                 | 64K -<br>4294967039<br>(0xFFFFFEFF)                                              |
| Version (or<br>later) | NDB 7.6.6                                                                        |
| Type or units         | bytes                                                                            |
| Default               | 4M                                                                               |
| Range                 | 64K -<br>4294967039<br>(0xFFFFFEFF)                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Each SHM connection has a shared memory segment where messages between nodes are placed by the sender and read by the reader. The size of this segment is defined by [ShmSize](#page-168-0). The default value in NDB 7.6 is 4MB.

### <span id="page-169-0"></span>• [ShmSpinTime](#page-169-0)

| Version (or<br>later) | NDB 7.6.6                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 2000                                                                         |
| Added                 | NDB 7.6.6                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

When receiving, the time to wait before sleeping, in microseconds.

### <span id="page-169-1"></span>• [SigNum](#page-169-1)

| Version (or<br>later) | NDB 7.5.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | []                                                                               |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Deprecated            | NDB 7.6.6                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

This parameter is no longer used in NDB 7.6, in which any setting for it is ignored.

The following applies only in NDB 7.5 (and earlier):

When using the shared memory transporter, a process sends an operating system signal to the other process when there is new data available in the shared memory. Should that signal conflict with an existing signal, this parameter can be used to change it. This is a possibility when using SHM due to the fact that different operating systems use different signal numbers.

The default value of [SigNum](#page-169-1) is 0; therefore, it must be set to avoid errors in the cluster log when using the shared memory transporter. Typically, this parameter is set to 10 in the [shm default] section of the config.ini file.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 21.20 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 21.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |

| Symbol | Restart Type | Description                                                                                                   |
|--------|--------------|---------------------------------------------------------------------------------------------------------------|
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                       |

# <span id="page-170-0"></span>**21.4.3.13 Configuring NDB Cluster Send Buffer Parameters**

The NDB kernel employs a unified send buffer whose memory is allocated dynamically from a pool shared by all transporters. This means that the size of the send buffer can be adjusted as necessary. Configuration of the unified send buffer can accomplished by setting the following parameters:

• **TotalSendBufferMemory.** This parameter can be set for all types of NDB Cluster nodes—that is, it can be set in the [ndbd], [mgm], and [api] (or [mysql]) sections of the config.ini file. It represents the total amount of memory (in bytes) to be allocated by each node for which it is set for use among all configured transporters. If set, its minimum is 256KB; the maximum is 4294967039.

To be backward-compatible with existing configurations, this parameter takes as its default value the sum of the maximum send buffer sizes of all configured transporters, plus an additional 32KB (one page) per transporter. The maximum depends on the type of transporter, as shown in the following table:

**Table 21.21 Transporter types with maximum send buffer sizes**

| Transporter | Maximum Send Buffer Size (bytes) |
|-------------|----------------------------------|
| TCP         | SendBufferMemory (default = 2M)  |
| SHM         | 20K                              |

This enables existing configurations to function in close to the same way as they did with NDB Cluster 6.3 and earlier, with the same amount of memory and send buffer space available to each transporter. However, memory that is unused by one transporter is not available to other transporters.

- **OverloadLimit.** This parameter is used in the config.ini file [tcp] section, and denotes the amount of unsent data (in bytes) that must be present in the send buffer before the connection is considered overloaded. When such an overload condition occurs, transactions that affect the overloaded connection fail with NDB API Error 1218 (Send Buffers overloaded in NDB kernel) until the overload status passes. The default value is 0, in which case the effective overload limit is calculated as SendBufferMemory \* 0.8 for a given connection. The maximum value for this parameter is 4G.
- **SendBufferMemory.** This value denotes a hard limit for the amount of memory that may be used by a single transporter out of the entire pool specified by [TotalSendBufferMemory](#page-93-0). However, the sum of SendBufferMemory for all configured transporters may be greater than the [TotalSendBufferMemory](#page-93-0) that is set for a given node. This is a way to save memory when many nodes are in use, as long as the maximum amount of memory is never required by all transporters at the same time.
- **ReservedSendBufferMemory.** Removed prior to NDB 7.5 GA.

| Version (or<br>later) | NDB 7.5.0 |
|-----------------------|-----------|
| Type or units         | bytes     |
| Default               | 256K      |

| Range        | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
|--------------|----------------------------------------------------------------------------------|
| Removed      | NDB 7.5.2                                                                        |
| Restart Type | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 7.5.0) |

Previously, this data node parameter was present, but not actually used (Bug #77404, Bug #21280428).

You can use the ndbinfo.transporters table to monitor send buffer memory usage, and to detect slowdown and overload conditions that can adversely affect performance.