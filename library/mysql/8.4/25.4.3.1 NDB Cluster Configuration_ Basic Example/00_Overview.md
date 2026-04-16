---
source: MySQL 8.4 Reference
title: 00_Overview
---

To support NDB Cluster, you should update my.cnf as shown in the following example. You may also specify these parameters on the command line when invoking the executables.

![](_page_132_Picture_14.jpeg)

#### **Note**

The options shown here should not be confused with those that are used in config.ini global configuration files. Global configuration options are discussed later in this section.

```
# my.cnf
# example additions to my.cnf for NDB Cluster
# (valid in MySQL 8.4)
```

```
# enable ndbcluster storage engine, and provide connection string for
# management server host (default port is 1186)
[mysqld]
ndbcluster
ndb-connectstring=ndb_mgmd.mysql.com
# provide connection string for management server host (default port: 1186)
[ndbd]
connect-string=ndb_mgmd.mysql.com
# provide connection string for management server host (default port: 1186)
[ndb_mgm]
connect-string=ndb_mgmd.mysql.com
# provide location of cluster configuration file
# IMPORTANT: When starting the management server with this option in the
# configuration file, the use of --initial or --reload on the command line when
# invoking ndb_mgmd is also required.
[ndb_mgmd]
config-file=/etc/config.ini
```

(For more information on connection strings, see [Section 25.4.3.3, "NDB Cluster Connection Strings"](#page-138-0).)

```
# my.cnf
# example additions to my.cnf for NDB Cluster
# (works on all versions)
# enable ndbcluster storage engine, and provide connection string for management
# server host to the default port 1186
[mysqld]
ndbcluster
ndb-connectstring=ndb_mgmd.mysql.com:1186
```

![](_page_133_Picture_4.jpeg)

#### **Important**

Once you have started a mysqld process with the [NDBCLUSTER](#page-50-0) and ndbconnectstring parameters in the [mysqld] in the my.cnf file as shown previously, you cannot execute any CREATE TABLE or ALTER TABLE statements without having actually started the cluster. Otherwise, these statements fail with an error. This is by design.

You may also use a separate [mysql\_cluster] section in the cluster my.cnf file for settings to be read and used by all executables:

```
# cluster-specific settings
[mysql_cluster]
ndb-connectstring=ndb_mgmd.mysql.com:1186
```

For additional [NDB](#page-50-0) variables that can be set in the my.cnf file, see NDB Cluster System Variables.

The NDB Cluster global configuration file is by convention named config.ini (but this is not required). If needed, it is read by ndb\_mgmd at startup and can be placed in any location that can be read by it. The location and name of the configuration are specified using --configfile=path\_name with ndb\_mgmd on the command line. This option has no default value, and is ignored if ndb\_mgmd uses the configuration cache.

The global configuration file for NDB Cluster uses INI format, which consists of sections preceded by section headings (surrounded by square brackets), followed by the appropriate parameter names and values. One deviation from the standard INI format is that the parameter name and value can be separated by a colon (:) as well as the equal sign (=); however, the equal sign is preferred. Another deviation is that sections are not uniquely identified by section name. Instead, unique sections (such as two different nodes of the same type) are identified by a unique ID specified as a parameter within the section.

Default values are defined for most parameters, and can also be specified in config.ini. To create a default value section, simply add the word default to the section name. For example, an [ndbd]

section contains parameters that apply to a particular data node, whereas an [ndbd default] section contains parameters that apply to all data nodes. Suppose that all data nodes should use the same data memory size. To configure them all, create an [ndbd default] section that contains a [DataMemory](#page-156-0) line to specify the data memory size.

If used, the [ndbd default] section must precede any [ndbd] sections in the configuration file. This is also true for default sections of any other type.

![](_page_134_Picture_3.jpeg)

#### **Note**

In some older releases of NDB Cluster, there was no default value for [NoOfReplicas](#page-153-0), which always had to be specified explicitly in the [ndbd default] section. Although this parameter now has a default value of 2, which is the recommended setting in most common usage scenarios, it is still recommended practice to set this parameter explicitly.

The global configuration file must define the computers and nodes involved in the cluster and on which computers these nodes are located. An example of a simple configuration file for a cluster consisting of one management server, two data nodes and two MySQL servers is shown here:

```
# file "config.ini" - 2 data nodes and 2 SQL nodes
# This file is placed in the startup directory of ndb_mgmd (the
# management server)
# The first MySQL Server can be started from any host. The second
# can be started only on the host mysqld_5.mysql.com
[ndbd default]
NoOfReplicas= 2
DataDir= /var/lib/mysql-cluster
[ndb_mgmd]
Hostname= ndb_mgmd.mysql.com
DataDir= /var/lib/mysql-cluster
[ndbd]
HostName= ndbd_2.mysql.com
[ndbd]
HostName= ndbd_3.mysql.com
[mysqld]
[mysqld]
HostName= mysqld_5.mysql.com
```

![](_page_134_Picture_8.jpeg)

#### **Note**

The preceding example is intended as a minimal starting configuration for purposes of familiarization with NDB Cluster , and is almost certain not to be sufficient for production settings. See [Section 25.4.3.2, "Recommended Starting](#page-135-0) [Configuration for NDB Cluster",](#page-135-0) which provides a more complete example starting configuration.

Each node has its own section in the config.ini file. For example, this cluster has two data nodes, so the preceding configuration file contains two [ndbd] sections defining these nodes.

![](_page_134_Picture_12.jpeg)

#### **Note**

Do not place comments on the same line as a section heading in the config.ini file; this causes the management server not to start because it cannot parse the configuration file in such cases.

### <span id="page-134-0"></span>**Sections of the config.ini File**

There are six different sections that you can use in the config.ini configuration file, as described in the following list:

- [computer]: Defines cluster hosts. This is not required to configure a viable NDB Cluster, but be may used as a convenience when setting up a large cluster. See [Section 25.4.3.4, "Defining](#page-139-1) [Computers in an NDB Cluster"](#page-139-1), for more information.
- [ndbd]: Defines a cluster data node (ndbd process). See [Section 25.4.3.6, "Defining NDB Cluster](#page-149-0) [Data Nodes"](#page-149-0), for details.
- [mysqld]: Defines the cluster's MySQL server nodes (also called SQL or API nodes). For a discussion of SQL node configuration, see Section 25.4.3.7, "Defining SQL and Other API Nodes in an NDB Cluster".
- [mgm] or [ndb\_mgmd]: Defines a cluster management server (MGM) node. For information concerning the configuration of management nodes, see [Section 25.4.3.5, "Defining an NDB Cluster](#page-140-0) [Management Server".](#page-140-0)
- [tcp]: Defines a TCP/IP connection between cluster nodes, with TCP/IP being the default transport protocol. Normally, [tcp] or [tcp default] sections are not required to set up an NDB Cluster, as the cluster handles this automatically; however, it may be necessary in some situations to override the defaults provided by the cluster. See Section 25.4.3.10, "NDB Cluster TCP/IP Connections", for information about available TCP/IP configuration parameters and how to use them. (You may also find Section 25.4.3.11, "NDB Cluster TCP/IP Connections Using Direct Connections" to be of interest in some cases.)
- [shm]: Defines shared-memory connections between nodes. In MySQL 8.4, it is enabled by default, but should still be considered experimental. For a discussion of SHM interconnects, see Section 25.4.3.12, "NDB Cluster Shared-Memory Connections".
- [sci]: Defines Scalable Coherent Interface connections between cluster data nodes. Not supported in NDB 8.4.

You can define default values for each section. If used, a default section should come before any other sections of that type. For example, an [ndbd default] section should appear in the configuration file before any [ndbd] sections.

NDB Cluster parameter names are case-insensitive, unless specified in MySQL Server my.cnf or my.ini files.

# <span id="page-135-0"></span>**25.4.3.2 Recommended Starting Configuration for NDB Cluster**

Achieving the best performance from an NDB Cluster depends on a number of factors including the following:

- NDB Cluster software version
- Numbers of data nodes and SQL nodes
- Hardware
- Operating system
- Amount of data to be stored
- Size and type of load under which the cluster is to operate

Therefore, obtaining an optimum configuration is likely to be an iterative process, the outcome of which can vary widely with the specifics of each NDB Cluster deployment. Changes in configuration are also likely to be indicated when changes are made in the platform on which the cluster is run, or in applications that use the NDB Cluster 's data. For these reasons, it is not possible to offer a single configuration that is ideal for all usage scenarios. However, in this section, we provide a recommended base configuration.

**Starting config.ini file.** The following config.ini file is a recommended starting point for configuring a cluster running NDB Cluster 8.4:

```
# TCP PARAMETERS
[tcp default]
SendBufferMemory=2M
ReceiveBufferMemory=2M
# Increasing the sizes of these 2 buffers beyond the default values
# helps prevent bottlenecks due to slow disk I/O.
# MANAGEMENT NODE PARAMETERS
[ndb_mgmd default]
DataDir=path/to/management/server/data/directory
# It is possible to use a different data directory for each management
# server, but for ease of administration it is preferable to be
# consistent.
[ndb_mgmd]
HostName=management-server-A-hostname
# NodeId=management-server-A-nodeid
[ndb_mgmd]
HostName=management-server-B-hostname
# NodeId=management-server-B-nodeid
# Using 2 management servers helps guarantee that there is always an
# arbitrator in the event of network partitioning, and so is
# recommended for high availability. Each management server must be
# identified by a HostName. You may for the sake of convenience specify
# a NodeId for any management server, although one is allocated
# for it automatically; if you do so, it must be in the range 1-255
# inclusive and must be unique among all IDs specified for cluster
# nodes.
# DATA NODE PARAMETERS
[ndbd default]
NoOfReplicas=2
# Using two fragment replicas is recommended to guarantee availability of data;
# using only one fragment replica does not provide any redundancy, which means
# that the failure of a single data node causes the entire cluster to shut down. 
# It is also possible (but not required) to use more than two fragment replicas, 
# although two fragment replicas are sufficient to provide high availability. 
LockPagesInMainMemory=1
# On Linux and Solaris systems, setting this parameter locks data node
# processes into memory. Doing so prevents them from swapping to disk,
# which can severely degrade cluster performance.
DataMemory=3456M
# The value provided for DataMemory assumes 4 GB RAM
# per data node. However, for best results, you should first calculate
# the memory that would be used based on the data you actually plan to
# store (you may find the ndb_size.pl utility helpful in estimating
# this), then allow an extra 20% over the calculated values. Naturally,
# you should ensure that each data node host has at least as much
# physical memory as the sum of these two values.
# ODirect=1
# Enabling this parameter causes NDBCLUSTER to try using O_DIRECT
# writes for local checkpoints and redo logs; this can reduce load on
# CPUs. We recommend doing so when using NDB Cluster on systems running
# Linux kernel 2.6 or later.
```

```
NoOfFragmentLogFiles=300
DataDir=path/to/data/node/data/directory
MaxNoOfConcurrentOperations=100000
SchedulerSpinTimer=400
SchedulerExecutionTimer=100
RealTimeScheduler=1
# Setting these parameters allows you to take advantage of real-time scheduling
# of NDB threads to achieve increased throughput when using ndbd. They
# are not needed when using ndbmtd; in particular, you should not set
# RealTimeScheduler for ndbmtd data nodes.
TimeBetweenGlobalCheckpoints=1000
TimeBetweenEpochs=200
RedoBuffer=32M
# CompressedLCP=1
# CompressedBackup=1
# Enabling CompressedLCP and CompressedBackup causes, respectively, local
checkpoint files and backup files to be compressed, which can result in a space
savings of up to 50% over noncompressed LCPs and backups.
# MaxNoOfLocalScans=64
MaxNoOfTables=1024
MaxNoOfOrderedIndexes=256
[ndbd]
HostName=data-node-A-hostname
# NodeId=data-node-A-nodeid
LockExecuteThreadToCPU=1
LockMaintThreadsToCPU=0
# On systems with multiple CPUs, these parameters can be used to lock NDBCLUSTER
# threads to specific CPUs
[ndbd]
HostName=data-node-B-hostname
# NodeId=data-node-B-nodeid
LockExecuteThreadToCPU=1
LockMaintThreadsToCPU=0
# You must have an [ndbd] section for every data node in the cluster;
# each of these sections must include a HostName. Each section may
# optionally include a NodeId for convenience, but in most cases, it is
# sufficient to allow the cluster to allocate node IDs dynamically. If
# you do specify the node ID for a data node, it must be in the range 1
# to 144 inclusive and must be unique among all IDs specified for
# cluster nodes.
# SQL NODE / API NODE PARAMETERS
[mysqld]
# HostName=sql-node-A-hostname
# NodeId=sql-node-A-nodeid
[mysqld]
[mysqld]
# Each API or SQL node that connects to the cluster requires a [mysqld]
# or [api] section of its own. Each such section defines a connection
# "slot"; you should have at least as many of these sections in the
# config.ini file as the total number of API nodes and SQL nodes that
# you wish to have connected to the cluster at any given time. There is
# no performance or other penalty for having extra slots available in
# case you find later that you want or need more API or SQL nodes to
# connect to the cluster at the same time.
# If no HostName is specified for a given [mysqld] or [api] section,
# then any API or SQL node may use that slot to connect to the
# cluster. You may wish to use an explicit HostName for one connection slot
# to guarantee that an API or SQL node from that host can always
```

```
# connect to the cluster. If you wish to prevent API or SQL nodes from
# connecting from other than a desired host or hosts, then use a
# HostName for every [mysqld] or [api] section in the config.ini file.
# You can if you wish define a node ID (NodeId parameter) for any API or
# SQL node, but this is not necessary; if you do so, it must be in the
# range 1 to 255 inclusive and must be unique among all IDs specified
# for cluster nodes.
```

**Required my.cnf options for SQL nodes.** MySQL servers acting as NDB Cluster SQL nodes must always be started with the --ndbcluster and --ndb-connectstring options, either on the command line or in my.cnf.

# <span id="page-138-0"></span>**25.4.3.3 NDB Cluster Connection Strings**

With the exception of the NDB Cluster management server (ndb\_mgmd), each node that is part of an NDB Cluster requires a connection string that points to the management server's location. This connection string is used in establishing a connection to the management server as well as in performing other tasks depending on the node's role in the cluster. The syntax for a connection string is as follows:

```
[nodeid=node_id, ]host-definition[, host-definition[, ...]]
host-definition:
 host_name[:port_number]
```

node\_id is an integer greater than or equal to 1 which identifies a node in config.ini. host\_name is a string representing a valid Internet host name or IP address. port\_number is an integer referring to a TCP/IP port number.

```
example 1 (long): "nodeid=2,myhost1:1100,myhost2:1100,198.51.100.3:1200"
example 2 (short): "myhost1"
```

localhost:1186 is used as the default connection string value if none is provided. If port\_num is omitted from the connection string, the default port is 1186. This port should always be available on the network because it has been assigned by IANA for this purpose (see [http://www.iana.org/assignments/](http://www.iana.org/assignments/port-numbers) [port-numbers](http://www.iana.org/assignments/port-numbers) for details).

By listing multiple host definitions, it is possible to designate several redundant management servers. An NDB Cluster data or API node attempts to contact successive management servers on each host in the order specified, until a successful connection has been established.

It is also possible to specify in a connection string one or more bind addresses to be used by nodes having multiple network interfaces for connecting to management servers. A bind address consists of a hostname or network address and an optional port number. This enhanced syntax for connection strings is shown here:

```
[nodeid=node_id, ]
 [bind-address=host-definition, ]
 host-definition[; bind-address=host-definition]
 host-definition[; bind-address=host-definition]
 [, ...]]
host-definition:
 host_name[:port_number]
```

If a single bind address is used in the connection string prior to specifying any management hosts, then this address is used as the default for connecting to any of them (unless overridden for a given management server; see later in this section for an example). For example, the following connection string causes the node to use 198.51.100.242 regardless of the management server to which it connects:

```
bind-address=198.51.100.242, poseidon:1186, perch:1186
```

If a bind address is specified following a management host definition, then it is used only for connecting to that management node. Consider the following connection string:

poseidon:1186;bind-address=localhost, perch:1186;bind-address=198.51.100.242

In this case, the node uses localhost to connect to the management server running on the host named poseidon and 198.51.100.242 to connect to the management server running on the host named perch.

You can specify a default bind address and then override this default for one or more specific management hosts. In the following example, localhost is used for connecting to the management server running on host poseidon; since 198.51.100.242 is specified first (before any management server definitions), it is the default bind address and so is used for connecting to the management servers on hosts perch and orca:

bind-address=198.51.100.242,poseidon:1186;bind-address=localhost,perch:1186,orca:2200

There are a number of different ways to specify the connection string:

- Each executable has its own command-line option which enables specifying the management server at startup. (See the documentation for the respective executable.)
- It is also possible to set the connection string for all nodes in the cluster at once by placing it in a [mysql\_cluster] section in the management server's my.cnf file.
- For backward compatibility, two other options are available, using the same syntax:
  - 1. Set the NDB\_CONNECTSTRING environment variable to contain the connection string.

This should be considered deprecated, and not used in new installations.

2. Write the connection string for each executable into a text file named Ndb.cfg and place this file in the executable's startup directory.

Use of this file is deprecated in NDB 8.4.3; you should expect it to be removed in a future release of MySQL Cluster.

The recommended method for specifying the connection string is to set it on the command line or in the my.cnf file for each executable.

# <span id="page-139-1"></span>**25.4.3.4 Defining Computers in an NDB Cluster**

The [computer] section has no real significance other than serving as a way to avoid the need of defining host names for each node in the system. All parameters mentioned here are required.

<span id="page-139-0"></span>• Id

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | string                                                                                                                                                                             |
| Default               | []                                                                                                                                                                                 |
| Range                 |                                                                                                                                                                                    |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting |

the cluster. (NDB 8.4.0)

This is a unique identifier, used to refer to the host computer elsewhere in the configuration file.

![](_page_140_Picture_3.jpeg)

#### **Important**

The computer ID is not the same as the node ID used for a management, API, or data node. Unlike the case with node IDs, you cannot use NodeId in place of Id in the [computer] section of the config.ini file.

#### <span id="page-140-1"></span>• HostName

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This is the computer's hostname or IP address.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 25.7 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 25.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |

# <span id="page-140-0"></span>**25.4.3.5 Defining an NDB Cluster Management Server**

The [ndb\_mgmd] section is used to configure the behavior of the management server. If multiple management servers are employed, you can specify parameters common to all of them in an [ndb\_mgmd default] section. [mgm] and [mgm default] are older aliases for these, supported for backward compatibility.

All parameters in the following list are optional and assume their default values if omitted.

![](_page_140_Picture_15.jpeg)

### **Note**

If neither the ExecuteOnComputer nor the HostName parameter is present, the default value localhost is assumed for both.

# <span id="page-141-0"></span>• Id

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                                                                                          |
| Default               | []                                                                                                                                                                                                                |
| Range                 | 1 - 255                                                                                                                                                                                                           |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

Each node in the cluster has a unique identity. For a management node, this is represented by an integer value in the range 1 to 255, inclusive. This ID is used by all internal cluster messages for addressing the node, and so must be unique for each NDB Cluster node, regardless of the type of node.

![](_page_141_Picture_4.jpeg)

#### **Note**

Data node IDs must be less than 145. If you plan to deploy a large number of data nodes, it is a good idea to limit the node IDs for management nodes (and API nodes) to values greater than 144.

The use of the Id parameter for identifying management nodes is deprecated in favor of [NodeId](#page-141-1). Although Id continues to be supported for backward compatibility, it now generates a warning and is subject to removal in a future version of NDB Cluster.

# <span id="page-141-1"></span>• NodeId

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                                                           |
| Default               | []                                                                                                                                                                                 |
| Range                 | 1 - 255                                                                                                                                                                            |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting |

the cluster. (NDB 8.4.0)

Each node in the cluster has a unique identity. For a management node, this is represented by an integer value in the range 1 to 255 inclusive. This ID is used by all internal cluster messages for addressing the node, and so must be unique for each NDB Cluster node, regardless of the type of node.

![](_page_142_Picture_3.jpeg)

#### **Note**

Data node IDs must be less than 145. If you plan to deploy a large number of data nodes, it is a good idea to limit the node IDs for management nodes (and API nodes) to values greater than 144.

NodeId is the preferred parameter name to use when identifying management nodes. Although the older [Id](#page-141-0) continues to be supported for backward compatibility, it is now deprecated and generates a warning when used; it is also subject to removal in a future NDB Cluster release.

#### <span id="page-142-0"></span>• ExecuteOnComputer

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | name                                                                                                      |
| Default               | []                                                                                                        |
| Range                 |                                                                                                           |
| Deprecated            | Yes (in NDB<br>7.5)                                                                                       |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

This refers to the Id set for one of the computers defined in a [computer] section of the config.ini file.

![](_page_142_Picture_10.jpeg)

# **Important**

This parameter is deprecated, and is subject to removal in a future release. Use the [HostName](#page-143-0) parameter instead.

#### <span id="page-142-1"></span>• PortNumber

| Version (or<br>later) | NDB 8.4.0                                                    |
|-----------------------|--------------------------------------------------------------|
| Type or units         | unsigned                                                     |
| Default               | 1186                                                         |
| Range                 | 0 - 64K                                                      |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and |

| restart of the |
|----------------|
| cluster. (NDB  |
| 8.4.0)         |

This is the port number on which the management server listens for configuration requests and management commands.

•

The node ID for this node can be given out only to connections that explicitly request it. A management server that requests "any" node ID cannot use this one. This parameter can be used when running multiple management servers on the same host, and [HostName](#page-143-0) is not sufficient for distinguishing among processes.

#### <span id="page-143-0"></span>• HostName

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Specifying this parameter defines the hostname of the computer on which the management node is to reside. Use HostName to specify a host name other than localhost.

# <span id="page-143-1"></span>• [LocationDomainId](#page-143-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | integer                                                                                                   |
| Default               | 0                                                                                                         |
| Range                 | 0 - 16                                                                                                    |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Assigns a management node to a specific [availability domain](https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/regions.md) (also known as an availability zone) within a cloud. By informing NDB which nodes are in which availability domains, performance can be improved in a cloud environment in the following ways:

- If requested data is not found on the same node, reads can be directed to another node in the same availability domain.
- Communication between nodes in different availability domains are guaranteed to use NDB transporters' WAN support without any further manual intervention.

- The transporter's group number can be based on which availability domain is used, such that also SQL and other API nodes communicate with local data nodes in the same availability domain whenever possible.
- The arbitrator can be selected from an availability domain in which no data nodes are present, or, if no such availability domain can be found, from a third availability domain.

LocationDomainId takes an integer value between 0 and 16 inclusive, with 0 being the default; using 0 is the same as leaving the parameter unset.

<span id="page-144-0"></span>• [LogDestination](#page-144-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |  |
|-----------------------|----------------------------------------------------------------------------------|--|
| Type or units         | {CONSOLE <br>SYSLOG FILE}                                                        |  |
| Default               | FILE:<br>filename=ndb_nodeid_cluster.log,<br>maxsize=1000000,<br>maxfiles=6      |  |
| Range                 |                                                                                  |  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |  |

This parameter specifies where to send cluster logging information. There are three options in this regard—CONSOLE, SYSLOG, and FILE—with FILE being the default:

• CONSOLE outputs the log to stdout:

CONSOLE

• SYSLOG sends the log to a syslog facility, possible values being one of auth, authpriv, cron, daemon, ftp, kern, lpr, mail, news, syslog, user, uucp, local0, local1, local2, local3, local4, local5, local6, or local7.

![](_page_144_Picture_10.jpeg)

#### **Note**

Not every facility is necessarily supported by every operating system.

SYSLOG:facility=syslog

- FILE pipes the cluster log output to a regular file on the same machine. The following values can be specified:
  - filename: The name of the log file.

The default log file name used in such cases is ndb\_nodeid\_cluster.log.

- maxsize: The maximum size (in bytes) to which the file can grow before logging rolls over to a new file. When this occurs, the old log file is renamed by appending .N to the file name, where N is the next number not yet used with this name.
- maxfiles: The maximum number of log files.

```
FILE:filename=cluster.log,maxsize=1000000,maxfiles=6
```

The default value for the FILE parameter is

FILE:filename=ndb\_node\_id\_cluster.log,maxsize=1000000,maxfiles=6, where node\_id is the ID of the node.

It is possible to specify multiple log destinations separated by semicolons as shown here:

CONSOLE;SYSLOG:facility=local0;FILE:filename=/var/log/mgmd

<span id="page-145-0"></span>• ArbitrationRank

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | 0-2                                                                              |
| Default               | 1                                                                                |
| Range                 | 0 - 2                                                                            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is used to define which nodes can act as arbitrators. Only management nodes and SQL nodes can be arbitrators. ArbitrationRank can take one of the following values:

- 0: The node is never used as an arbitrator.
- 1: The node has high priority; that is, it is preferred as an arbitrator over low-priority nodes.
- 2: Indicates a low-priority node which is used as an arbitrator only if a node with a higher priority is not available for that purpose.

Normally, the management server should be configured as an arbitrator by setting its ArbitrationRank to 1 (the default for management nodes) and those for all SQL nodes to 0 (the default for SQL nodes).

You can disable arbitration completely either by setting ArbitrationRank to 0 on all management and SQL nodes, or by setting the Arbitration parameter in the [ndbd default] section of the config.ini global configuration file. Setting Arbitration causes any settings for ArbitrationRank to be disregarded.

# <span id="page-146-0"></span>• ArbitrationDelay

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

An integer value which causes the management server's responses to arbitration requests to be delayed by that number of milliseconds. By default, this value is 0; it is normally not necessary to change it.

#### <span id="page-146-1"></span>• DataDir

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | path                                                                             |
| Default               |                                                                                  |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This specifies the directory where output files from the management server are placed. These files include cluster log files, process output files, and the daemon's process ID (PID) file. (For log files, this location can be overridden by setting the FILE parameter for [LogDestination](#page-144-0), as discussed previously in this section.)

The default value for this parameter is the directory in which ndb\_mgmd is located.

# <span id="page-146-2"></span>• PortNumberStats

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | []                                                                               |
| Range                 | 0 - 64K                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the port number used to obtain statistical information from an NDB Cluster management server. It has no default value.

# <span id="page-147-2"></span>• [Wan](#page-147-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Use WAN TCP setting as default.

<span id="page-147-1"></span>• HeartbeatThreadPriority

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | string                                                                           |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Set the scheduling policy and priority of heartbeat threads for management and API nodes.

The syntax for setting this parameter is shown here:

```
HeartbeatThreadPriority = policy[, priority]
policy:
 {FIFO | RR}
```

When setting this parameter, you must specify a policy. This is one of FIFO (first in, first out) or RR (round robin). The policy value is followed optionally by the priority (an integer).

<span id="page-147-0"></span>• ExtraSendBufferMemory

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 0 - 32G                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the amount of transporter send buffer memory to allocate in addition to any that has been set using [TotalSendBufferMemory](#page-148-2), SendBufferMemory, or both. <sup>3918</sup>

# <span id="page-148-0"></span>• RequireTls

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

If this parameter is set to true, a client, once connected to this management node, must be authenticated using TLS before the connection can be used for anything else.

#### <span id="page-148-2"></span>• TotalSendBufferMemory

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 256K -<br>4294967039<br>(0xFFFFFEFF)                                             |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is used to determine the total amount of memory to allocate on this node for shared send buffer memory among all configured transporters.

If this parameter is set, its minimum permitted value is 256KB; 0 indicates that the parameter has not been set. For more detailed information, see Section 25.4.3.14, "Configuring NDB Cluster Send Buffer Parameters".

### <span id="page-148-1"></span>• HeartbeatIntervalMgmdMgmd

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | milliseconds                                   |
| Default               | 1500                                           |
| Range                 | 100 -<br>4294967039<br>(0xFFFFFEFF)            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 8.4.0)

Specify the interval between heartbeat messages used to determine whether another management node is on contact with this one. The management node waits after 3 of these intervals to declare the connection dead; thus, the default setting of 1500 milliseconds causes the management node to wait for approximately 1600 ms before timing out.

![](_page_149_Picture_3.jpeg)

#### **Note**

After making changes in a management node's configuration, it is necessary to perform a rolling restart of the cluster for the new configuration to take effect.

To add new management servers to a running NDB Cluster, it is also necessary to perform a rolling restart of all cluster nodes after modifying any existing config.ini files. For more information about issues arising when using multiple management nodes, see [Section 25.2.7.10, "Limitations Relating to](#page-80-0) [Multiple NDB Cluster Nodes"](#page-80-0).

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 25.8 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 25.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |

# <span id="page-149-0"></span>**25.4.3.6 Defining NDB Cluster Data Nodes**

The [ndbd] and [ndbd default] sections are used to configure the behavior of the cluster's data nodes.

[ndbd] and [ndbd default] are always used as the section names whether you are using ndbd or ndbmtd binaries for the data node processes.

There are many parameters which control buffer sizes, pool sizes, timeouts, and so forth. The only mandatory parameter is ExecuteOnComputer; this must be defined in the local [ndbd] section.

The parameter [NoOfReplicas](#page-153-0) should be defined in the [ndbd default] section, as it is common to all Cluster data nodes. It is not strictly necessary to set [NoOfReplicas](#page-153-0), but it is good practice to set it explicitly.

Most data node parameters are set in the [ndbd default] section. Only those parameters explicitly stated as being able to set local values are permitted to be changed in the [ndbd] section. Where present, HostName and NodeId must be defined in the local [ndbd] section, and not in any other section of config.ini. In other words, settings for these parameters are specific to one data node.

For those parameters affecting memory usage or buffer sizes, it is possible to use K, M, or G as a suffix to indicate units of 1024, 1024×1024, or 1024×1024×1024. (For example, 100K means 100 × 1024 = 102400.)

Parameter names and values are case-insensitive, unless used in a MySQL Server my.cnf or my.ini file, in which case they are case-sensitive.

Information about configuration parameters specific to NDB Cluster Disk Data tables can be found later in this section (see Disk Data Configuration Parameters).

All of these parameters also apply to ndbmtd (the multithreaded version of ndbd). Three additional data node configuration parameters—MaxNoOfExecutionThreads, ThreadConfig, and NoOfFragmentLogParts—apply to ndbmtd only; these have no effect when used with ndbd. For more information, see Multi-Threading Configuration Parameters (ndbmtd). See also Section 25.5.3, "ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)".

**Identifying data nodes.** The NodeId or Id value (that is, the data node identifier) can be allocated on the command line when the node is started or in the configuration file.

# <span id="page-150-1"></span>• NodeId

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                                                                                          |
| Default               | []                                                                                                                                                                                                                |
| Range                 | 1 - 144                                                                                                                                                                                                           |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

A unique node ID is used as the node's address for all cluster internal messages. For data nodes, this is an integer in the range 1 to 144 inclusive. Each node in the cluster must have a unique identifier.

NodeId is the only supported parameter name to use when identifying data nodes.

#### <span id="page-150-0"></span>• ExecuteOnComputer

| Version (or<br>later) | NDB 8.4.0                                                    |
|-----------------------|--------------------------------------------------------------|
| Type or units         | name                                                         |
| Default               | []                                                           |
| Range                 |                                                              |
| Deprecated            | Yes (in NDB<br>7.5)                                          |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and |

| restart of the |
|----------------|
| cluster. (NDB  |
| 8.4.0)         |

This refers to the Id set for one of the computers defined in a [computer] section.

![](_page_151_Picture_3.jpeg)

•

# **Important**

This parameter is deprecated, and is subject to removal in a future release. Use the [HostName](#page-151-0) parameter instead.

The node ID for this node can be given out only to connections that explicitly request it. A management server that requests "any" node ID cannot use this one. This parameter can be used when running multiple management servers on the same host, and [HostName](#page-151-0) is not sufficient for distinguishing among processes.

#### <span id="page-151-0"></span>• HostName

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | name or IP<br>address                                                            |
| Default               | localhost                                                                        |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Specifying this parameter defines the hostname of the computer on which the data node is to reside. Use HostName to specify a host name other than localhost.

# <span id="page-151-1"></span>• [ServerPort](#page-151-1)

| Version (or<br>later) | NDB 8.4.0 |
|-----------------------|-----------|
| Type or units         | unsigned  |
| Default               | []        |
| Range                 | 1 - 64K   |
| Restart Type          | System    |

cluster. (NDB 8.4.0)

Each node in the cluster uses a port to connect to other nodes. By default, this port is allocated dynamically in such a way as to ensure that no two nodes on the same host computer receive the same port number, so it should normally not be necessary to specify a value for this parameter.

However, if you need to be able to open specific ports in a firewall to permit communication between data nodes and API nodes (including SQL nodes), you can set this parameter to the number of the desired port in an [ndbd] section or (if you need to do this for multiple data nodes) the [ndbd default] section of the config.ini file, and then open the port having that number for incoming connections from SQL nodes, API nodes, or both.

![](_page_152_Picture_4.jpeg)

#### **Note**

Connections from data nodes to management nodes is done using the ndb\_mgmd management port (the management server's [PortNumber](#page-142-1)) so outgoing connections to that port from any data nodes should always be permitted.

<span id="page-152-1"></span>• TcpBind\_INADDR\_ANY

Setting this parameter to TRUE or 1 binds IP\_ADDR\_ANY so that connections can be made from anywhere (for autogenerated connections). The default is FALSE (0).

#### <span id="page-152-0"></span>• [NodeGroup](#page-152-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                                                                                          |
| Default               | []                                                                                                                                                                                                                |
| Range                 | 0 - 65536                                                                                                                                                                                                         |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

This parameter can be used to assign a data node to a specific node group. It is read only when the cluster is started for the first time, and cannot be used to reassign a data node to a different node group online. It is generally not desirable to use this parameter in the [ndbd default] section of the config.ini file, and care must be taken not to assign nodes to node groups in such a way that an invalid numbers of nodes are assigned to any node groups.

The [NodeGroup](#page-152-0) parameter is chiefly intended for use in adding a new node group to a running NDB Cluster without having to perform a rolling restart. For this purpose, you should set it to 65536 (the maximum value). You are not required to set a [NodeGroup](#page-152-0) value for all cluster data nodes, only for those nodes which are to be started and added to the cluster as a new node group at a later time. For more information, see Section 25.6.7.3, "Adding NDB Cluster Data Nodes Online: Detailed Example".

# <span id="page-153-1"></span>• [LocationDomainId](#page-153-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | integer                                                                                                   |
| Default               | 0                                                                                                         |
| Range                 | 0 - 16                                                                                                    |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Assigns a data node to a specific [availability domain](https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/regions.md) (also known as an availability zone) within a cloud. By informing NDB which nodes are in which availability domains, performance can be improved in a cloud environment in the following ways:

- If requested data is not found on the same node, reads can be directed to another node in the same availability domain.
- Communication between nodes in different availability domains are guaranteed to use NDB transporters' WAN support without any further manual intervention.
- The transporter's group number can be based on which availability domain is used, such that also SQL and other API nodes communicate with local data nodes in the same availability domain whenever possible.
- The arbitrator can be selected from an availability domain in which no data nodes are present, or, if no such availability domain can be found, from a third availability domain.

LocationDomainId takes an integer value between 0 and 16 inclusive, with 0 being the default; using 0 is the same as leaving the parameter unset.

#### <span id="page-153-0"></span>• [NoOfReplicas](#page-153-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | integer                                                                                                                                                                                                           |
| Default               | 2                                                                                                                                                                                                                 |
| Range                 | 1 - 4                                                                                                                                                                                                             |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

This global parameter can be set only in the [ndbd default] section, and defines the number of fragment replicas for each table stored in the cluster. This parameter also specifies the size of node groups. A node group is a set of nodes all storing the same information.

Node groups are formed implicitly. The first node group is formed by the set of data nodes with the lowest node IDs, the next node group by the set of the next lowest node identities, and so on. By way of example, assume that we have 4 data nodes and that NoOfReplicas is set to 2. The four data nodes have node IDs 2, 3, 4 and 5. Then the first node group is formed from nodes 2 and 3, and the second node group by nodes 4 and 5. It is important to configure the cluster in such a manner that nodes in the same node groups are not placed on the same computer because a single hardware failure would cause the entire cluster to fail.

If no node IDs are provided, the order of the data nodes is the determining factor for the node group. Whether or not explicit assignments are made, they can be viewed in the output of the management client's SHOW command.

The default value for NoOfReplicas is 2. This is the recommended value for most production environments. Setting this parameter's value to 3 or 4 is also supported.

![](_page_154_Picture_5.jpeg)

#### **Warning**

Setting NoOfReplicas to 1 means that there is only a single copy of all Cluster data; in this case, the loss of a single data node causes the cluster to fail because there are no additional copies of the data stored by that node.

The number of data nodes in the cluster must be evenly divisible by the value of this parameter. For example, if there are two data nodes, then [NoOfReplicas](#page-153-0) must be equal to either 1 or 2, since 2/3 and 2/4 both yield fractional values; if there are four data nodes, then NoOfReplicas must be equal to 1, 2, or 4.

# <span id="page-154-0"></span>• DataDir

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | path                                                                                                                                                   |
| Default               |                                                                                                                                                        |
| Range                 |                                                                                                                                                        |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

This parameter specifies the directory where trace files, log files, pid files and error logs are placed.

The default is the data node process working directory.

### <span id="page-154-1"></span>• [FileSystemPath](#page-154-1)

| Version (or<br>later) | NDB 8.4.0 |
|-----------------------|-----------|
| Type or units         | path      |

| Default      | DataDir                                                                                                                                                |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Range        |                                                                                                                                                        |
| Restart Type | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

This parameter specifies the directory where all files created for metadata, REDO logs, UNDO logs (for Disk Data tables), and data files are placed. The default is the directory specified by DataDir.

![](_page_155_Picture_3.jpeg)

#### **Note**

This directory must exist before the ndbd process is initiated.

The recommended directory hierarchy for NDB Cluster includes /var/lib/mysql-cluster, under which a directory for the node's file system is created. The name of this subdirectory contains the node ID. For example, if the node ID is 2, this subdirectory is named ndb\_2\_fs.

#### <span id="page-155-0"></span>• [BackupDataDir](#page-155-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | path                                                                                                                                                   |
| Default               | FileSystemPath                                                                                                                                         |
| Range                 |                                                                                                                                                        |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

This parameter specifies the directory in which backups are placed.

![](_page_155_Picture_10.jpeg)

#### **Important**

The string '/BACKUP' is always appended to this value. For example, if you set the value of [BackupDataDir](#page-155-0) to /var/lib/cluster-data, then all backups are stored under /var/lib/cluster-data/BACKUP. This also means that the effective default backup location is the directory named BACKUP under the location specified by the [FileSystemPath](#page-154-1) parameter.

# **Data Memory, Index Memory, and String Memory**

[DataMemory](#page-156-0) and [IndexMemory](#page-157-0) are [ndbd] parameters specifying the size of memory segments used to store the actual records and their indexes. In setting values for these, it is important to

understand how [DataMemory](#page-156-0) is used, as it usually needs to be updated to reflect actual usage by the cluster.

![](_page_156_Picture_2.jpeg)

#### **Note**

IndexMemory is deprecated, and subject to removal in a future version of NDB Cluster. See the descriptions that follow for further information.

#### <span id="page-156-0"></span>• [DataMemory](#page-156-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 98M                                                                              |
| Range                 | 1M - 16T                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter defines the amount of space (in bytes) available for storing database records. The entire amount specified by this value is allocated in memory, so it is extremely important that the machine has sufficient physical memory to accommodate it.

The memory allocated by [DataMemory](#page-156-0) is used to store both the actual records and indexes. There is a 16-byte overhead on each record; an additional amount for each record is incurred because it is stored in a 32KB page with 128 byte page overhead (see below). There is also a small amount wasted per page due to the fact that each record is stored in only one page.

For variable-size table attributes, the data is stored on separate data pages, allocated from [DataMemory](#page-156-0). Variable-length records use a fixed-size part with an extra overhead of 4 bytes to reference the variable-size part. The variable-size part has 2 bytes overhead plus 2 bytes per attribute.

The maximum record size is 30000 bytes.

Resources assigned to DataMemory are used for storing all data and indexes. (Any memory configured as IndexMemory is automatically added to that used by DataMemory to form a common resource pool.)

The memory space allocated by [DataMemory](#page-156-0) consists of 32KB pages, which are allocated to table fragments. Each table is normally partitioned into the same number of fragments as there are data nodes in the cluster. Thus, for each node, there are the same number of fragments as are set in [NoOfReplicas](#page-153-0).

Once a page has been allocated, it is currently not possible to return it to the pool of free pages, except by deleting the table. (This also means that [DataMemory](#page-156-0) pages, once allocated to a given table, cannot be used by other tables.) Performing a data node recovery also compresses the partition because all records are inserted into empty partitions from other live nodes.

The [DataMemory](#page-156-0) memory space also contains UNDO information: For each update, a copy of the unaltered record is allocated in the [DataMemory](#page-156-0). There is also a reference to each copy in the ordered table indexes. Unique hash indexes are updated only when the unique index columns are updated, in which case a new entry in the index table is inserted and the old entry is deleted upon commit. For this reason, it is also necessary to allocate enough memory to handle the largest transactions performed by applications using the cluster. In any case, performing a few large transactions holds no advantage over using many smaller ones, for the following reasons:

- Large transactions are not any faster than smaller ones
- Large transactions increase the number of operations that are lost and must be repeated in event of transaction failure
- Large transactions use more memory

The default value for [DataMemory](#page-156-0) is 98MB. The minimum value is 1MB. There is no maximum size, but in reality the maximum size has to be adapted so that the process does not start swapping when the limit is reached. This limit is determined by the amount of physical RAM available on the machine and by the amount of memory that the operating system may commit to any one process. 32-bit operating systems are generally limited to 2−4GB per process; 64-bit operating systems can use more. For large databases, it may be preferable to use a 64-bit operating system for this reason.

#### <span id="page-157-0"></span>• [IndexMemory](#page-157-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 1M - 1T                                                                          |
| Deprecated            | Yes (in NDB<br>7.6)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The IndexMemory parameter is deprecated (and subject to future removal); any memory assigned to IndexMemory is allocated instead to the same pool as [DataMemory](#page-156-0), which is solely responsible for all resources needed for storing data and indexes in memory. In NDB 8.4, the use of IndexMemory in the cluster configuration file triggers a warning from the management server.

You can estimate the size of a hash index using this formula:

```
 size = ( (fragments * 32K) + (rows * 18) )
 * fragment_replicas
```

fragments is the number of fragments, fragment\_replicas is the number of fragment replicas (normally 2), and rows is the number of rows. If a table has one million rows, eight fragments, and two fragment replicas, the expected index memory usage is calculated as shown here:

```
 ((8 * 32K) + (1000000 * 18)) * 2 = ((8 * 32768) + (1000000 * 18)) * 2
 = (262144 + 18000000) * 2
 = 18262144 * 2 = 36524288 bytes = ~35MB
```

Index statistics for ordered indexes (when these are enabled) are stored in the mysql.ndb\_index\_stat\_sample table. Since this table has a hash index, this adds to index memory usage. An upper bound to the number of rows for a given ordered index can be calculated as follows:

```
 sample_size= key_size + ((key_attributes + 1) * 4)
 sample_rows = IndexStatSaveSize
 * ((0.01 * IndexStatSaveScale * log2(rows * sample_size)) + 1)
```

```
 / sample_size
```

In the preceding formula, key\_size is the size of the ordered index key in bytes, key\_attributes is the number of attributes in the ordered index key, and rows is the number of rows in the base table.

Assume that table t1 has 1 million rows and an ordered index named ix1 on two four-byte integers. Assume in addition that IndexStatSaveSize and IndexStatSaveScale are set to their default values (32K and 100, respectively). Using the previous 2 formulas, we can calculate as follows:

```
 sample_size = 8 + ((1 + 2) * 4) = 20 bytes
 sample_rows = 32K
 * ((0.01 * 100 * log2(1000000*20)) + 1)
 / 20
 = 32768 * ( (1 * ~16.811) +1) / 20
 = 32768 * ~17.811 / 20
 = ~29182 rows
```

The expected index memory usage is thus 2 \* 18 \* 29182 = ~1050550 bytes.

The minimum and default value for this parameter is 0 (zero).

#### <span id="page-158-0"></span>• [StringMemory](#page-158-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | % or bytes                                                                                                |
| Default               | 25                                                                                                        |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                                            |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

This parameter determines how much memory is allocated for strings such as table names, and is specified in an [ndbd] or [ndbd default] section of the config.ini file. A value between 0 and 100 inclusive is interpreted as a percent of the maximum default value, which is calculated based on a number of factors including the number of tables, maximum table name size, maximum size of .FRM files, [MaxNoOfTriggers](#page-182-1), maximum column name size, and maximum default column value.

A value greater than 100 is interpreted as a number of bytes.

The default value is 25—that is, 25 percent of the default maximum.

Under most circumstances, the default value should be sufficient, but when you have a great many NDB tables (1000 or more), it is possible to get Error 773 Out of string memory, please modify StringMemory config parameter: Permanent error: Schema error, in which case you should increase this value. 25 (25 percent) is not excessive, and should prevent this error from recurring in all but the most extreme conditions.

The following example illustrates how memory is used for a table. Consider this table definition:

```
CREATE TABLE example (
 a INT NOT NULL,
```

```
 b INT NOT NULL,
 c INT NOT NULL,
 PRIMARY KEY(a),
 UNIQUE(b)
) ENGINE=NDBCLUSTER;
```

For each record, there are 12 bytes of data plus 12 bytes overhead. Having no nullable columns saves 4 bytes of overhead. In addition, we have two ordered indexes on columns a and b consuming roughly 10 bytes each per record. There is a primary key hash index on the base table using roughly 29 bytes per record. The unique constraint is implemented by a separate table with b as primary key and a as a column. This other table consumes an additional 29 bytes of index memory per record in the example table as well 8 bytes of record data plus 12 bytes of overhead.

Thus, for one million records, we need 58MB for index memory to handle the hash indexes for the primary key and the unique constraint. We also need 64MB for the records of the base table and the unique index table, plus the two ordered index tables.

You can see that hash indexes takes up a fair amount of memory space; however, they provide very fast access to the data in return. They are also used in NDB Cluster to handle uniqueness constraints.

Currently, the only partitioning algorithm is hashing and ordered indexes are local to each node. Thus, ordered indexes cannot be used to handle uniqueness constraints in the general case.

An important point for both [IndexMemory](#page-157-0) and [DataMemory](#page-156-0) is that the total database size is the sum of all data memory and all index memory for each node group. Each node group is used to store replicated information, so if there are four nodes with two fragment replicas, there are two node groups. Thus, the total data memory available is 2 × [DataMemory](#page-156-0) for each data node.

It is highly recommended that [DataMemory](#page-156-0) and [IndexMemory](#page-157-0) be set to the same values for all nodes. Data distribution is even over all nodes in the cluster, so the maximum amount of space available for any node can be no greater than that of the smallest node in the cluster.

[DataMemory](#page-156-0) can be changed, but decreasing it can be risky; doing so can easily lead to a node or even an entire NDB Cluster that is unable to restart due to there being insufficient memory space. Increasing these values should be acceptable, but it is recommended that such upgrades are performed in the same manner as a software upgrade, beginning with an update of the configuration file, and then restarting the management server followed by restarting each data node in turn.

<span id="page-159-0"></span>**MinFreePct.** A proportion (5% by default) of data node resources including [DataMemory](#page-156-0) is kept in reserve to insure that the data node does not exhaust its memory when performing a restart. This can be adjusted using the [MinFreePct](#page-159-0) data node configuration parameter (default 5).

| Version (or later) NDB 8.4.0 |                                                                                  |
|------------------------------|----------------------------------------------------------------------------------|
| Type or units                | unsigned                                                                         |
| Default                      | 5                                                                                |
| Range                        | 0 - 100                                                                          |
| Restart Type                 | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Updates do not increase the amount of index memory used. Inserts take effect immediately; however, rows are not actually deleted until the transaction is committed.

<span id="page-159-1"></span>**Transaction parameters.** The next few [ndbd] parameters that we discuss are important because they affect the number of parallel transactions and the sizes of transactions that can be handled by the

system. [MaxNoOfConcurrentTransactions](#page-160-0) sets the number of parallel transactions possible in a node. [MaxNoOfConcurrentOperations](#page-161-0) sets the number of records that can be in update phase or locked simultaneously.

Both of these parameters (especially [MaxNoOfConcurrentOperations](#page-161-0)) are likely targets for users setting specific values and not using the default value. The default value is set for systems using small transactions, to ensure that these do not use excessive memory.

[MaxDMLOperationsPerTransaction](#page-163-0) sets the maximum number of DML operations that can be performed in a given transaction.

<span id="page-160-0"></span>• [MaxNoOfConcurrentTransactions](#page-160-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 4096                                                                             |
| Range                 | 32 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Each cluster data node requires a transaction record for each active transaction in the cluster. The task of coordinating transactions is distributed among all of the data nodes. The total number of transaction records in the cluster is the number of transactions in any given node times the number of nodes in the cluster.

Transaction records are allocated to individual MySQL servers. Each connection to a MySQL server requires at least one transaction record, plus an additional transaction object per table accessed by that connection. This means that a reasonable minimum for the total number of transactions in the cluster can be expressed as

```
TotalNoOfConcurrentTransactions =
 (maximum number of tables accessed in any single transaction + 1)
 * number of SQL nodes
```

Suppose that there are 10 SQL nodes using the cluster. A single join involving 10 tables requires 11 transaction records; if there are 10 such joins in a transaction, then 10 \* 11 = 110 transaction records are required for this transaction, per MySQL server, or 110 \* 10 = 1100 transaction records total. Each data node can be expected to handle TotalNoOfConcurrentTransactions / number of data nodes. For an NDB Cluster having 4 data nodes, this would mean setting MaxNoOfConcurrentTransactions on each data node to 1100 / 4 = 275. In addition, you should provide for failure recovery by ensuring that a single node group can accommodate all concurrent transactions; in other words, that each data node's MaxNoOfConcurrentTransactions is sufficient to cover a number of transactions equal to TotalNoOfConcurrentTransactions / number of node groups. If this cluster has a single node group, then MaxNoOfConcurrentTransactions should be set to 1100 (the same as the total number of concurrent transactions for the entire cluster).

In addition, each transaction involves at least one operation; for this reason, the value set for MaxNoOfConcurrentTransactions should always be no more than the value of [MaxNoOfConcurrentOperations](#page-161-0).

This parameter must be set to the same value for all cluster data nodes. This is due to the fact that, when a data node fails, the oldest surviving node re-creates the transaction state of all transactions that were ongoing in the failed node.

It is possible to change this value using a rolling restart, but the amount of traffic on the cluster must be such that no more transactions occur than the lower of the old and new levels while this is taking place.

The default value is 4096.

<span id="page-161-0"></span>• [MaxNoOfConcurrentOperations](#page-161-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 32K                                                                              |
| Range                 | 32 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

It is a good idea to adjust the value of this parameter according to the size and number of transactions. When performing transactions which involve only a few operations and records, the default value for this parameter is usually sufficient. Performing large transactions involving many records usually requires that you increase its value.

Records are kept for each transaction updating cluster data, both in the transaction coordinator and in the nodes where the actual updates are performed. These records contain state information needed to find UNDO records for rollback, lock queues, and other purposes.

This parameter should be set at a minimum to the number of records to be updated simultaneously in transactions, divided by the number of cluster data nodes. For example, in a cluster which has four data nodes and which is expected to handle one million concurrent updates using transactions, you should set this value to 1000000 / 4 = 250000. To help provide resiliency against failures, it is suggested that you set this parameter to a value that is high enough to permit an individual data node to handle the load for its node group. In other words, you should set the value equal to total number of concurrent operations / number of node groups. (In the case where there is a single node group, this is the same as the total number of concurrent operations for the entire cluster.)

Because each transaction always involves at least one operation, the value of MaxNoOfConcurrentOperations should always be greater than or equal to the value of [MaxNoOfConcurrentTransactions](#page-160-0).

Read queries which set locks also cause operation records to be created. Some extra space is allocated within individual nodes to accommodate cases where the distribution is not perfect over the nodes.

When queries make use of the unique hash index, there are actually two operation records used per record in the transaction. The first record represents the read in the index table and the second handles the operation on the base table.

The default value is 32768.

This parameter actually handles two values that can be configured separately. The first of these specifies how many operation records are to be placed with the transaction coordinator. The second part specifies how many operation records are to be local to the database.

A very large transaction performed on an eight-node cluster requires as many operation records in the transaction coordinator as there are reads, updates, and deletes involved in the transaction. However, the operation records of the are spread over all eight nodes. Thus, if it is necessary to configure the system for one very large transaction, it is a good idea to configure the two parts separately. [MaxNoOfConcurrentOperations](#page-161-0) is always used to calculate the number of operation records in the transaction coordinator portion of the node.

It is also important to have an idea of the memory requirements for operation records. These consume about 1KB per record.

#### <span id="page-162-0"></span>• [MaxNoOfLocalOperations](#page-162-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | UNDEFINED                                                                        |
| Range                 | 32 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

By default, this parameter is calculated as 1.1 × [MaxNoOfConcurrentOperations](#page-161-0). This fits systems with many simultaneous transactions, none of them being very large. If there is a need to handle one very large transaction at a time and there are many nodes, it is a good idea to override the default value by explicitly specifying this parameter.

This parameter is deprecated and subject to removal in a future NDB Cluster release. In addition, this parameter is incompatible with the [TransactionMemory](#page-167-1) parameter; if you try to set values for both parameters in the cluster configuration file (config.ini), the management server refuses to start.

<span id="page-163-0"></span>• [MaxDMLOperationsPerTransaction](#page-163-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | operations<br>(DML)                                                              |
| Default               | 4294967295                                                                       |
| Range                 | 32 -<br>4294967295                                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter limits the size of a transaction. The transaction is aborted if it requires more than this many DML operations.

The value of this parameter cannot exceed that set for [MaxNoOfConcurrentOperations](#page-161-0).

<span id="page-163-2"></span>**Transaction temporary storage.** The next set of [ndbd] parameters is used to determine temporary storage when executing a statement that is part of a Cluster transaction. All records are released when the statement is completed and the cluster is waiting for the commit or rollback.

The default values for these parameters are adequate for most situations. However, users with a need to support transactions involving large numbers of rows or operations may need to increase these values to enable better parallelism in the system, whereas users whose applications require relatively small transactions can decrease the values to save memory.

<span id="page-163-1"></span>• [MaxNoOfConcurrentIndexOperations](#page-163-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 8K                                                                               |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

For queries using a unique hash index, another temporary set of operation records is used during a query's execution phase. This parameter sets the size of that pool of records. Thus, this record is allocated only while executing a part of a query. As soon as this part has been executed, the record is released. The state needed to handle aborts and commits is handled by the normal operation records, where the pool size is set by the parameter [MaxNoOfConcurrentOperations](#page-161-0).

The default value of this parameter is 8192. Only in rare cases of extremely high parallelism using unique hash indexes should it be necessary to increase this value. Using a smaller value is possible and can save memory if the DBA is certain that a high degree of parallelism is not required for the cluster.

This parameter is deprecated and subject to removal in a future NDB Cluster release. In addition, this parameter is incompatible with the [TransactionMemory](#page-167-1) parameter; if you try to set values for both parameters in the cluster configuration file (config.ini), the management server refuses to start.

#### <span id="page-164-0"></span>• [MaxNoOfFiredTriggers](#page-164-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 4000                                                                             |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The default value of [MaxNoOfFiredTriggers](#page-164-0) is 4000, which is sufficient for most situations. In some cases it can even be decreased if the DBA feels certain the need for parallelism in the cluster is not high.

A record is created when an operation is performed that affects a unique hash index. Inserting or deleting a record in a table with unique hash indexes or updating a column that is part of a unique hash index fires an insert or a delete in the index table. The resulting record is used to represent this index table operation while waiting for the original operation that fired it to complete. This operation is short-lived but can still require a large number of records in its pool for situations with many parallel write operations on a base table containing a set of unique hash indexes.

This parameter is deprecated and subject to removal in a future NDB Cluster release. In addition, this parameter is incompatible with the [TransactionMemory](#page-167-1) parameter; if you try to set values for both parameters in the cluster configuration file (config.ini), the management server refuses to start.

#### <span id="page-164-1"></span>• [TransactionBufferMemory](#page-164-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 1M                                                                               |
| Range                 | 1K -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The memory affected by this parameter is used for tracking operations fired when updating index tables and reading unique indexes. This memory is used to store the key and column information for these operations. It is only very rarely that the value for this parameter needs to be altered from the default.

The default value for [TransactionBufferMemory](#page-164-1) is 1MB.

Normal read and write operations use a similar buffer, whose usage is even more short-lived. The compile-time parameter ZATTRBUF\_FILESIZE (found in ndb/src/kernel/blocks/ Dbtc/Dbtc.hpp) set to 4000 × 128 bytes (500KB). A similar buffer for key information, ZDATABUF\_FILESIZE (also in Dbtc.hpp) contains 4000 × 16 = 62.5KB of buffer space. Dbtc is the module that handles transaction coordination.

**Transaction resource allocation parameters.** The parameters in the following list are used to allocate transaction resources in the transaction coordinator ([DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md)). Leaving any one of these set to the default (0) dedicates transaction memory for 25% of estimated total data node usage for the corresponding resource. The actual maximum possible values for these parameters are typically limited by the amount of memory available to the data node; setting them has no impact on the total amount of memory allocated to the data node. In addition, you should keep in mind that they control numbers of reserved internal records for the data node independent of any settings for [MaxDMLOperationsPerTransaction](#page-163-0), [MaxNoOfConcurrentIndexOperations](#page-163-1), [MaxNoOfConcurrentOperations](#page-161-0), [MaxNoOfConcurrentScans](#page-169-1), [MaxNoOfConcurrentTransactions](#page-160-0), [MaxNoOfFiredTriggers](#page-164-0), [MaxNoOfLocalScans](#page-170-0), or [TransactionBufferMemory](#page-164-1) (see [Transaction parameters](#page-159-1) and [Transaction temporary storage](#page-163-2)).

<span id="page-165-0"></span>• [ReservedConcurrentIndexOperations](#page-165-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Number of simultaneous index operations having dedicated resources on one data node.

<span id="page-165-1"></span>• [ReservedConcurrentOperations](#page-165-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Number of simultaneous operations having dedicated resources in transaction coordinators on one data node.

<span id="page-166-0"></span>• [ReservedConcurrentScans](#page-166-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Number of simultaneous scans having dedicated resources on one data node.

<span id="page-166-1"></span>• [ReservedConcurrentTransactions](#page-166-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Number of simultaneous transactions having dedicated resources on one data node.

<span id="page-166-2"></span>• [ReservedFiredTriggers](#page-166-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Number of triggers that have dedicated resources on one ndbd(DB) node.

<span id="page-166-3"></span>• [ReservedLocalScans](#page-166-3)

| Default      | 0                                                                                |
|--------------|----------------------------------------------------------------------------------|
| Range        | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Number of simultaneous fragment scans having dedicated resources on one data node.

<span id="page-167-0"></span>• [ReservedTransactionBufferMemory](#page-167-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Dynamic buffer space (in bytes) for key and attribute data allocated to each data node.

<span id="page-167-1"></span>• [TransactionMemory](#page-167-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 0 - 16384G                                                                       |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

![](_page_167_Picture_8.jpeg)

# **Important**

A number of configuration parameters are incompatible with TransactionMemory; it is not possible to set any of these parameters concurrently with TransactionMemory, and if you attempt to do so, the management server is unable to start (see [Parameters incompatible with](#page-168-2) [TransactionMemory\)](#page-168-2).

This parameter determines the memory (in bytes) allocated for transactions on each data node. Setting of transaction memory is handled as follows:

• If TransactionMemory is set, this value is used for determining transaction memory.

• Otherwise, transaction memory is calculated as it was previous to NDB 8.0.

<span id="page-168-2"></span>**Parameters incompatible with TransactionMemory.** The following parameters cannot be used concurrently with TransactionMemory and are therefore deprecated:

- [MaxNoOfConcurrentIndexOperations](#page-163-1)
- [MaxNoOfFiredTriggers](#page-164-0)
- [MaxNoOfLocalOperations](#page-162-0)
- [MaxNoOfLocalScans](#page-170-0)

Explicitly setting any of the parameters just listed when TransactionMemory has also been set in the cluster configuration file (config.ini) keeps the management node from starting.

For more information regarding resource allocation in NDB Cluster data nodes, see Section 25.4.3.13, "Data Node Memory Management".

**Scans and buffering.** There are additional [ndbd] parameters in the Dblqh module (in ndb/src/kernel/blocks/Dblqh/Dblqh.hpp) that affect reads and updates. These include ZATTRINBUF\_FILESIZE, set by default to 10000 × 128 bytes (1250KB) and ZDATABUF\_FILE\_SIZE, set by default to 10000\*16 bytes (roughly 156KB) of buffer space. To date, there have been neither any reports from users nor any results from our own extensive tests suggesting that either of these compiletime limits should be increased.

<span id="page-168-0"></span>• [BatchSizePerLocalScan](#page-168-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 256                                                                              |
| Range                 | 1 - 992                                                                          |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is used to calculate the number of lock records used to handle concurrent scan operations.

Deprecated.

BatchSizePerLocalScan has a strong connection to the BatchSize defined in the SQL nodes.

<span id="page-168-1"></span>• [LongMessageBuffer](#page-168-1)

| Version (or<br>later) | NDB 8.4.0 |
|-----------------------|-----------|
| Type or units         | bytes     |
| Default               | 64M       |

| Range        | 512K -<br>4294967039<br>(0xFFFFFEFF)                                             |
|--------------|----------------------------------------------------------------------------------|
| Restart Type | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This is an internal buffer used for passing messages within individual nodes and between nodes. The default is 64MB.

This parameter seldom needs to be changed from the default.

#### <span id="page-169-0"></span>• [MaxFKBuildBatchSize](#page-169-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 64                                                                               |
| Range                 | 16 - 512                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Maximum scan batch size used for building foreign keys. Increasing the value set for this parameter may speed up building of foreign key builds at the expense of greater impact to ongoing traffic.

#### <span id="page-169-1"></span>• [MaxNoOfConcurrentScans](#page-169-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 256                                                                              |
| Range                 | 2 - 500                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is used to control the number of parallel scans that can be performed in the cluster. Each transaction coordinator can handle the number of parallel scans defined for this parameter. Each scan query is performed by scanning all partitions in parallel. Each partition scan uses a scan record in the node where the partition is located, the number of records being the value of this parameter times the number of nodes. The cluster should be able to sustain [MaxNoOfConcurrentScans](#page-169-1) scans concurrently from all nodes in the cluster.

Scans are actually performed in two cases. The first of these cases occurs when no hash or ordered indexes exists to handle the query, in which case the query is executed by performing a full table scan. The second case is encountered when there is no hash index to support the query but there is an ordered index. Using the ordered index means executing a parallel range scan. The order is kept on the local partitions only, so it is necessary to perform the index scan on all partitions.

The default value of [MaxNoOfConcurrentScans](#page-169-1) is 256. The maximum value is 500.

#### <span id="page-170-0"></span>• [MaxNoOfLocalScans](#page-170-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |  |
|-----------------------|----------------------------------------------------------------------------------|--|
| Type or units         | integer                                                                          |  |
| Default               | 4 *<br>MaxNoOfConcurrentScans<br>* [# of data<br>nodes] + 2                      |  |
| Range                 | 32 -<br>4294967039<br>(0xFFFFFEFF)                                               |  |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |  |

Specifies the number of local scan records if many scans are not fully parallelized. When the number of local scan records is not provided, it is calculated as shown here:

```
4 * MaxNoOfConcurrentScans * [# data nodes] + 2
```

This parameter is deprecated and subject to removal in a future NDB Cluster release. In addition, this parameter is incompatible with the [TransactionMemory](#page-167-1) parameter; if you try to set values for both parameters in the cluster configuration file (config.ini), the management server refuses to start.

# <span id="page-170-1"></span>• [MaxParallelCopyInstances](#page-170-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 64                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets the parallelization used in the copy phase of a node restart or system restart, when a node that is currently just starting is synchronised with a node that already has current data by copying over any changed records from the node that is up to date. Because full parallelism in such cases can lead to overload situations, MaxParallelCopyInstances provides a means to decrease it. This parameter's default value 0. This value means that the effective parallelism is equal to the number of LDM instances in the node just starting as well as the node updating it.

<span id="page-170-2"></span>• [MaxParallelScansPerFragment](#page-170-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 256                                                                              |
| Range                 | 1 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

It is possible to configure the maximum number of parallel scans ([TUP](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtup.md) scans and [TUX](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtux.md) scans) allowed before they begin queuing for serial handling. You can increase this to take advantage of any unused CPU when performing large number of scans in parallel and improve their performance.

# <span id="page-171-1"></span>• [MaxReorgBuildBatchSize](#page-171-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 64                                                                               |
| Range                 | 16 - 512                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Maximum scan batch size used for reorganization of table partitions. Increasing the value set for this parameter may speed up reorganization at the expense of greater impact to ongoing traffic.

# <span id="page-171-2"></span>• [MaxUIBuildBatchSize](#page-171-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 64                                                                               |
| Range                 | 16 - 512                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Maximum scan batch size used for building unique keys. Increasing the value set for this parameter may speed up such builds at the expense of greater impact to ongoing traffic.

### <span id="page-171-0"></span>**Memory Allocation**

[MaxAllocate](#page-171-0)

| Version (or later) NDB 8.4.0 |  |
|------------------------------|--|
|------------------------------|--|

| Type or units | unsigned                                                                         |
|---------------|----------------------------------------------------------------------------------|
| Default       | 32M                                                                              |
| Range         | 1M - 1G                                                                          |
| Deprecated    | Yes (in NDB 8.0)                                                                 |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter was used in older versions of NDB Cluster, but has no effect in NDB 8.4. It is deprecated and subject to removal in a future release.

# **Multiple Transporters**

NDB allocates multiple transporters for communication between pairs of data nodes. The number of transporters so allocated can be influenced by setting an appropriate value for the NodeGroupTransporters parameter introduced in that release.

#### <span id="page-172-1"></span>[NodeGroupTransporters](#page-172-1)

| Version (or later) NDB 8.4.0 |                                                                                  |
|------------------------------|----------------------------------------------------------------------------------|
| Type or units                | integer                                                                          |
| Default                      | 0                                                                                |
| Range                        | 0 - 32                                                                           |
| Restart Type                 | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter determines the number of transporters used between nodes in the same node group. The default value (0) means that the number of transporters used is the same as the number of LDMs in the node. This should be sufficient for most use cases; thus it should seldom be necessary to change this value from its default.

Setting NodeGroupTransporters to a number greater than the number of LDM threads or the number of TC threads, whichever is higher, causes NDB to use the maximum of these two numbers of threads. This means that a value greater than this is effectively ignored.

### <span id="page-172-0"></span>**Hash Map Size**

# [DefaultHashMapSize](#page-172-0)

| Version (or later) NDB 8.4.0 |                                                                                  |
|------------------------------|----------------------------------------------------------------------------------|
| Type or units                | LDM threads                                                                      |
| Default                      | 240                                                                              |
| Range                        | 0 - 3840                                                                         |
| Restart Type                 | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The original intended use for this parameter was to facilitate upgrades and especially downgrades to and from very old releases with differing default hash map sizes. This is not an issue when upgrading from NDB Cluster 7.3 (or later) to later versions.

Decreasing this parameter online after any tables have been created or modified with DefaultHashMapSize equal to 3840 is not currently supported.

**Logging and checkpointing.** The following [ndbd] parameters control log and checkpoint behavior.

<span id="page-173-0"></span>• [FragmentLogFileSize](#page-173-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | bytes                                                                                                                                                  |
| Default               | 16M                                                                                                                                                    |
| Range                 | 4M - 1G                                                                                                                                                |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

Setting this parameter enables you to control directly the size of redo log files. This can be useful in situations when NDB Cluster is operating under a high load and it is unable to close fragment log files quickly enough before attempting to open new ones (only 2 fragment log files can be open at one time); increasing the size of the fragment log files gives the cluster more time before having to open each new fragment log file. The default value for this parameter is 16M.

For more information about fragment log files, see the description for [NoOfFragmentLogFiles](#page-176-1).

<span id="page-173-2"></span>• [InitialNoOfOpenFiles](#page-173-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | files                                                                            |
| Default               | 27                                                                               |
| Range                 | 20 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets the initial number of internal threads to allocate for open files.

The default value is 27.

<span id="page-173-1"></span>• [InitFragmentLogFiles](#page-173-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | [see values]                                                                                                                                           |
| Default               | SPARSE                                                                                                                                                 |
| Range                 | SPARSE, FULL                                                                                                                                           |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

By default, fragment log files are created sparsely when performing an initial start of a data node—that is, depending on the operating system and file system in use, not all bytes are necessarily written to disk. However, it is possible to override this behavior and force all bytes to be written, regardless of the platform and file system type being used, by means of this parameter. [InitFragmentLogFiles](#page-173-1) takes either of two values:

- SPARSE. Fragment log files are created sparsely. This is the default value.
- FULL. Force all bytes of the fragment log file to be written to disk.

Depending on your operating system and file system, setting InitFragmentLogFiles=FULL may help eliminate I/O errors on writes to the redo log.

<span id="page-174-0"></span>• [EnablePartialLcp](#page-174-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | true                                                                             |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When true, enable partial local checkpoints: This means that each LCP records only part of the full database, plus any records containing rows changed since the last LCP; if no rows have changed, the LCP updates only the LCP control file and does not update any data files.

If EnablePartialLcp is disabled (false), each LCP uses only a single file and writes a full checkpoint; this requires the least amount of disk space for LCPs, but increases the write load for each LCP. The default value is enabled (true). The proportion of space used by partial LCPS can be modified by the setting for the [RecoveryWork](#page-177-0) configuration parameter.

For more information about files and directories used for full and partial LCPs, see [NDB Cluster Data](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md) [Node File System Directory.](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.md)

Setting this parameter to false also disables the calculation of disk write speed used by the adaptive LCP control mechanism.

#### <span id="page-175-0"></span>• [LcpScanProgressTimeout](#page-175-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | second                                                                           |
| Default               | 180                                                                              |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

A local checkpoint fragment scan watchdog checks periodically for no progress in each fragment scan performed as part of a local checkpoint, and shuts down the node if there is no progress after a given amount of time has elapsed. This interval can be set using the [LcpScanProgressTimeout](#page-175-0) data node configuration parameter, which sets the maximum time for which the local checkpoint can be stalled before the LCP fragment scan watchdog shuts down the node.

The default value is 60 seconds (providing compatibility with previous releases). Setting this parameter to 0 disables the LCP fragment scan watchdog altogether.

# <span id="page-175-1"></span>• [MaxNoOfOpenFiles](#page-175-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 20 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets a ceiling on how many internal threads to allocate for open files. Any situation requiring a change in this parameter should be reported as a bug.

The default value is 0. However, the minimum value to which this parameter can be set is 20.

<span id="page-175-2"></span>• [MaxNoOfSavedMessages](#page-175-2)

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | integer                                                                          |
|---------------|----------------------------------------------------------------------------------|
| Default       | 25                                                                               |
| Range         | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets the maximum number of errors written in the error log as well as the maximum number of trace files that are kept before overwriting the existing ones. Trace files are generated when, for whatever reason, the node crashes.

The default is 25, which sets these maximums to 25 error messages and 25 trace files.

# <span id="page-176-0"></span>• [MaxLCPStartDelay](#page-176-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | seconds                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 600                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

In parallel data node recovery, only table data is actually copied and synchronized in parallel; synchronization of metadata such as dictionary and checkpoint information is done in a serial fashion. In addition, recovery of dictionary and checkpoint information cannot be executed in parallel with performing of local checkpoints. This means that, when starting or restarting many data nodes concurrently, data nodes may be forced to wait while a local checkpoint is performed, which can result in longer node recovery times.

It is possible to force a delay in the local checkpoint to permit more (and possibly all) data nodes to complete metadata synchronization; once each data node's metadata synchronization is complete, all of the data nodes can recover table data in parallel, even while the local checkpoint is being executed. To force such a delay, set [MaxLCPStartDelay](#page-176-0), which determines the number of seconds the cluster can wait to begin a local checkpoint while data nodes continue to synchronize metadata. This parameter should be set in the [ndbd default] section of the config.ini file, so that it is the same for all data nodes. The maximum value is 600; the default is 0.

### <span id="page-176-1"></span>• [NoOfFragmentLogFiles](#page-176-1)

| Version (or<br>later) | NDB 8.4.0                      |
|-----------------------|--------------------------------|
| Type or units         | integer                        |
| Default               | 16                             |
| Range                 | 3 - 4294967039<br>(0xFFFFFEFF) |
| Restart Type          | Initial Node<br>Restart:       |

Requires a rolling restart of the cluster; each data node must be restarted with --initial. (NDB 8.4.0)

This parameter sets the number of REDO log files for the node, and thus the amount of space allocated to REDO logging. Because the REDO log files are organized in a ring, it is extremely important that the first and last log files in the set (sometimes referred to as the "head" and "tail" log files, respectively) do not meet. When these approach one another too closely, the node begins aborting all transactions encompassing updates due to a lack of room for new log records.

A REDO log record is not removed until both required local checkpoints have been completed since that log record was inserted. Checkpointing frequency is determined by its own set of configuration parameters discussed elsewhere in this chapter.

The default parameter value is 16, which by default means 16 sets of 4 16MB files for a total of 1024MB. The size of the individual log files is configurable using the [FragmentLogFileSize](#page-173-0) parameter. In scenarios requiring a great many updates, the value for [NoOfFragmentLogFiles](#page-176-1) may need to be set as high as 300 or even higher to provide sufficient space for REDO logs.

If the checkpointing is slow and there are so many writes to the database that the log files are full and the log tail cannot be cut without jeopardizing recovery, all updating transactions are aborted with internal error code 410 (Out of log file space temporarily). This condition prevails until a checkpoint has completed and the log tail can be moved forward.

![](_page_177_Picture_6.jpeg)

#### **Important**

This parameter cannot be changed "on the fly"; you must restart the node using --initial. If you wish to change this value for all data nodes in a running cluster, you can do so using a rolling node restart (using --initial when starting each data node).

<span id="page-177-0"></span>• [RecoveryWork](#page-177-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 60                                                                               |
| Range                 | 25 - 100                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Percentage of storage overhead for LCP files. This parameter has an effect only when [EnablePartialLcp](#page-174-0) is true, that is, only when partial local checkpoints are enabled. A higher value means:

• Fewer records are written for each LCP, LCPs use more space

• More work is needed during restarts

A lower value for RecoveryWork means:

- More records are written during each LCP, but LCPs require less space on disk.
- Less work during restart and thus faster restarts, at the expense of more work during normal operations

For example, setting RecoveryWork to 60 means that the total size of an LCP is roughly 1 + 0.6 = 1.6 times the size of the data to be checkpointed. This means that 60% more work is required during the restore phase of a restart compared to the work done during a restart that uses full checkpoints. (This is more than compensated for during other phases of the restart such that the restart as a whole is still faster when using partial LCPs than when using full LCPs.) In order not to fill up the redo log, it is necessary to write at 1 + (1 / RecoveryWork) times the rate of data changes during checkpoints—thus, when RecoveryWork = 60, it is necessary to write at approximately 1 + (1 / 0.6 ) = 2.67 times the change rate. In other words, if changes are being written at 10 MByte per second, the checkpoint needs to be written at roughly 26.7 MByte per second.

Setting RecoveryWork = 40 means that only 1.4 times the total LCP size is needed (and thus the restore phase takes 10 to 15 percent less time. In this case, the checkpoint write rate is 3.5 times the rate of change.

The NDB source distribution includes a test program for simulating LCPs. lcp\_simulator.cc can be found in storage/ndb/src/kernel/blocks/backup/. To compile and run it on Unix platforms, execute the commands shown here:

```
$> gcc lcp_simulator.cc
$> ./a.out
```

This program has no dependencies other than stdio.h, and does not require a connection to an NDB cluster or a MySQL server. By default, it simulates 300 LCPs (three sets of 100 LCPs, each consisting of inserts, updates, and deletes, in turn), reporting the size of the LCP after each one. You can alter the simulation by changing the values of recovery\_work, insert\_work, and delete\_work in the source and recompiling. For more information, see the source of the program.

<span id="page-178-0"></span>• [InsertRecoveryWork](#page-178-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 40                                                                               |
| Range                 | 0 - 70                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Percentage of [RecoveryWork](#page-177-0) used for inserted rows. A higher value increases the number of writes during a local checkpoint, and decreases the total size of the LCP. A lower value decreases the number of writes during an LCP, but results in more space being used for the LCP, which means that recovery takes longer. This parameter has an effect only when [EnablePartialLcp](#page-174-0) is true, that is, only when partial local checkpoints are enabled.

# <span id="page-179-0"></span>• [EnableRedoControl](#page-179-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | true                                                                             |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enable adaptive checkpointing speed for controlling redo log usage.

When enabled (the default), EnableRedoControl allows the data nodes greater flexibility with regard to the rate at which they write LCPs to disk. More specifically, enabling this parameter means that higher write rates can be employed, so that LCPs can complete and redo logs be trimmed more quickly, thereby reducing recovery time and disk space requirements. This functionality allows data nodes to make better use of the higher rate of I/O and greater bandwidth available from modern solid-state storage devices and protocols, such as solid-state drives (SSDs) using Non-Volatile Memory Express (NVMe).

When NDB is deployed on systems whose I/O or bandwidth is constrained relative to those employing solid-state technology, such as those using conventional hard disks (HDDs), the EnableRedoControl mechanism can easily cause the I/O subsystem to become saturated, increasing wait times for data node input and output. In particular, this can cause issues with NDB Disk Data tables which have tablespaces or log file groups sharing a constrained I/O subsystem with data node LCP and redo log files; such problems potentially include node or cluster failure due to GCP stop errors. Set EnableRedoControl to false to disable it in such situations. Setting [EnablePartialLcp](#page-174-0) to false also disables the adaptive calculation.

**Metadata objects.** The next set of [ndbd] parameters defines pool sizes for metadata objects, used to define the maximum number of attributes, tables, indexes, and trigger objects used by indexes, events, and replication between clusters.

![](_page_179_Picture_7.jpeg)

#### **Note**

These act merely as "suggestions" to the cluster, and any that are not specified revert to the default values shown.

#### <span id="page-179-1"></span>• [MaxNoOfAttributes](#page-179-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 1000                                                                             |
| Range                 | 32 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets a suggested maximum number of attributes that can be defined in the cluster; like [MaxNoOfTables](#page-180-0), it is not intended to function as a hard upper limit.

(In older NDB Cluster releases, this parameter was sometimes treated as a hard limit for certain operations. This caused problems with NDB Cluster Replication, when it was possible to create more tables than could be replicated, and sometimes led to confusion when it was possible [or not possible, depending on the circumstances] to create more than MaxNoOfAttributes attributes.)

The default value is 1000, with the minimum possible value being 32. The maximum is 4294967039. Each attribute consumes around 200 bytes of storage per node due to the fact that all metadata is fully replicated on the servers.

When setting [MaxNoOfAttributes](#page-179-1), it is important to prepare in advance for any ALTER TABLE statements that you might want to perform in the future. This is due to the fact, during the execution of ALTER TABLE on a Cluster table, 3 times the number of attributes as in the original table are used, and a good practice is to permit double this amount. For example, if the NDB Cluster table having the greatest number of attributes (greatest\_number\_of\_attributes) has 100 attributes, a good starting point for the value of [MaxNoOfAttributes](#page-179-1) would be 6 \* greatest\_number\_of\_attributes = 600.

You should also estimate the average number of attributes per table and multiply this by [MaxNoOfTables](#page-180-0). If this value is larger than the value obtained in the previous paragraph, you should use the larger value instead.

Assuming that you can create all desired tables without any problems, you should also verify that this number is sufficient by trying an actual ALTER TABLE after configuring the parameter. If this is not successful, increase [MaxNoOfAttributes](#page-179-1) by another multiple of [MaxNoOfTables](#page-180-0) and test it again.

#### <span id="page-180-0"></span>• [MaxNoOfTables](#page-180-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 128                                                                              |
| Range                 | 8 - 20320                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

A table object is allocated for each table and for each unique hash index in the cluster. This parameter sets a suggested maximum number of table objects for the cluster as a whole; like [MaxNoOfAttributes](#page-179-1), it is not intended to function as a hard upper limit.

(In older NDB Cluster releases, this parameter was sometimes treated as a hard limit for certain operations. This caused problems with NDB Cluster Replication, when it was possible to create

more tables than could be replicated, and sometimes led to confusion when it was possible [or not possible, depending on the circumstances] to create more than MaxNoOfTables tables.)

For each attribute that has a BLOB data type an extra table is used to store most of the BLOB data. These tables also must be taken into account when defining the total number of tables.

The default value of this parameter is 128. The minimum is 8 and the maximum is 20320. Each table object consumes approximately 20KB per node.

![](_page_181_Picture_4.jpeg)

#### **Note**

The sum of [MaxNoOfTables](#page-180-0), [MaxNoOfOrderedIndexes](#page-181-0), and [MaxNoOfUniqueHashIndexes](#page-181-1) must not exceed 2 <sup>32</sup> − 2 (4294967294).

# <span id="page-181-0"></span>• [MaxNoOfOrderedIndexes](#page-181-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 128                                                                              |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

For each ordered index in the cluster, an object is allocated describing what is being indexed and its storage segments. By default, each index so defined also defines an ordered index. Each unique index and primary key has both an ordered index and a hash index. [MaxNoOfOrderedIndexes](#page-181-0) sets the total number of ordered indexes that can be in use in the system at any one time.

The default value of this parameter is 128. Each index object consumes approximately 10KB of data per node.

![](_page_181_Picture_11.jpeg)

#### **Note**

The sum of [MaxNoOfTables](#page-180-0), [MaxNoOfOrderedIndexes](#page-181-0), and [MaxNoOfUniqueHashIndexes](#page-181-1) must not exceed 2 <sup>32</sup> − 2 (4294967294).

# <span id="page-181-1"></span>• [MaxNoOfUniqueHashIndexes](#page-181-1)

| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |
|-----------------------|------------------------------------------------|
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                 |
| Default               | 64                                             |
| Type or units         | integer                                        |
| Version (or<br>later) | NDB 8.4.0                                      |

of the cluster. (NDB 8.4.0)

For each unique index that is not a primary key, a special table is allocated that maps the unique key to the primary key of the indexed table. By default, an ordered index is also defined for each unique index. To prevent this, you must specify the USING HASH option when defining the unique index.

The default value is 64. Each index consumes approximately 15KB per node.

![](_page_182_Picture_4.jpeg)

#### **Note**

The sum of [MaxNoOfTables](#page-180-0), [MaxNoOfOrderedIndexes](#page-181-0), and [MaxNoOfUniqueHashIndexes](#page-181-1) must not exceed 2 <sup>32</sup> − 2 (4294967294).

<span id="page-182-1"></span>• [MaxNoOfTriggers](#page-182-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 768                                                                              |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Internal update, insert, and delete triggers are allocated for each unique hash index. (This means that three triggers are created for each unique hash index.) However, an ordered index requires only a single trigger object. Backups also use three trigger objects for each normal table in the cluster.

Replication between clusters also makes use of internal triggers.

This parameter sets the maximum number of trigger objects in the cluster.

The default value is 768.

<span id="page-182-0"></span>• [MaxNoOfSubscriptions](#page-182-0)

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | unsigned                                       |
| Default               | 0                                              |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                 |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 8.4.0)

Each [NDB](#page-50-0) table in an NDB Cluster requires a subscription in the NDB kernel. For some NDB API applications, it may be necessary or desirable to change this parameter. However, for normal usage with MySQL servers acting as SQL nodes, there is not any need to do so.

The default value for [MaxNoOfSubscriptions](#page-182-0) is 0, which is treated as equal to [MaxNoOfTables](#page-180-0). Each subscription consumes 108 bytes.

#### <span id="page-183-1"></span>• [MaxNoOfSubscribers](#page-183-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is of interest only when using NDB Cluster Replication. The default value is 0. It is treated as 2 \* MaxNoOfTables + 2 \* [number of API nodes]. There is one subscription per [NDB](#page-50-0) table for each of two MySQL servers (one acting as the replication source and the other as the replica). Each subscriber uses 16 bytes of memory.

When using circular replication, multi-source replication, and other replication setups involving more than 2 MySQL servers, you should increase this parameter to the number of mysqld processes included in replication (this is often, but not always, the same as the number of clusters). For example, if you have a circular replication setup using three NDB Clusters, with one mysqld attached to each cluster, and each of these mysqld processes acts as a source and as a replica, you should set [MaxNoOfSubscribers](#page-183-1) equal to 3 \* MaxNoOfTables.

For more information, see Section 25.7, "NDB Cluster Replication".

#### <span id="page-183-0"></span>• [MaxNoOfConcurrentSubOperations](#page-183-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 256                                                                              |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets a ceiling on the number of operations that can be performed by all API nodes in the cluster at one time. The default value (256) is sufficient for normal operations, and might need to be adjusted only in scenarios where there are a great many API nodes each performing a high volume of operations concurrently.

**Boolean parameters.** The behavior of data nodes is also affected by a set of [ndbd] parameters taking on boolean values. These parameters can each be specified as TRUE by setting them equal to 1 or Y, and as FALSE by setting them equal to 0 or N.

#### <span id="page-184-0"></span>• [CompressedLCP](#page-184-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Setting this parameter to 1 causes local checkpoint files to be compressed. The compression used is equivalent to gzip --fast, and can save 50% or more of the space required on the data node to store uncompressed checkpoint files. Compressed LCPs can be enabled for individual data nodes, or for all data nodes (by setting this parameter in the [ndbd default] section of the config.ini file).

![](_page_184_Picture_5.jpeg)

#### **Important**

You cannot restore a compressed local checkpoint to a cluster running a MySQL version that does not support this feature.

The default value is 0 (disabled).

#### <span id="page-184-1"></span>• [CrashOnCorruptedTuple](#page-184-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | true                                                                             |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When this parameter is enabled (the default), it forces a data node to shut down whenever it encounters a corrupted tuple.

# <span id="page-184-2"></span>• [Diskless](#page-184-2)

| Version (or<br>later) | NDB 8.4.0                  |
|-----------------------|----------------------------|
| Type or units         | true false (1 0)           |
| Default               | false                      |
| Range                 | true, false                |
| Restart Type          | Initial System<br>Restart: |

Requires a complete shutdown of the cluster, wiping and restoring the cluster file system from a backup, and then restarting the cluster. (NDB 8.4.0)

It is possible to specify NDB Cluster tables as diskless, meaning that tables are not checkpointed to disk and that no logging occurs. Such tables exist only in main memory. A consequence of using diskless tables is that neither the tables nor the records in those tables survive a crash. However, when operating in diskless mode, it is possible to run ndbd on a diskless computer.

![](_page_185_Picture_3.jpeg)

# **Important**

This feature causes the entire cluster to operate in diskless mode.

When this feature is enabled, NDB Cluster online backup is disabled. In addition, a partial start of the cluster is not possible.

[Diskless](#page-184-2) is disabled by default.

<span id="page-185-0"></span>• [EncryptedFileSystem](#page-185-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                               |
| Default               | 0                                                                                                                                                      |
| Range                 | 0 - 1                                                                                                                                                  |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

Encrypt LCP and tablespace files, including undo logs and redo logs. Disabled by default (0); set to 1 to enable.

![](_page_185_Picture_11.jpeg)

#### **Important**

When file system encryption is enabled, you must supply a password to each data node when starting it, using one of the options --filesystempassword or --filesystem-password-from-stdin. Otherwise, the data node cannot start.

For more information, see Section 25.6.19.4, "File System Encryption for NDB Cluster".

# <span id="page-186-0"></span>• [LateAlloc](#page-186-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 1                                                                                |
| Range                 | 0 - 1                                                                            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Allocate memory for this data node after a connection to the management server has been established. Enabled by default.

<span id="page-186-1"></span>• [LockPagesInMainMemory](#page-186-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 2                                                                            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

For a number of operating systems, including Solaris and Linux, it is possible to lock a process into memory and so avoid any swapping to disk. This can be used to help guarantee the cluster's realtime characteristics.

This parameter takes one of the integer values 0, 1, or 2, which act as shown in the following list:

- 0: Disables locking. This is the default value.
- 1: Performs the lock after allocating memory for the process.
- 2: Performs the lock before memory for the process is allocated.

If the operating system is not configured to permit unprivileged users to lock pages, then the data node process making use of this parameter may have to be run as system root. ([LockPagesInMainMemory](#page-186-1) uses the mlockall function. From Linux kernel 2.6.9, unprivileged users can lock memory as limited by max locked memory. For more information, see ulimit -l and<http://linux.die.net/man/2/mlock>).

![](_page_186_Picture_12.jpeg)

#### **Note**

In older NDB Cluster releases, this parameter was a Boolean. 0 or false was the default setting, and disabled locking. 1 or true enabled locking of the process after its memory was allocated. NDB Cluster 8.4 treats true or false for the value of this parameter as an error.

![](_page_187_Picture_2.jpeg)

#### **Important**

Beginning with glibc 2.10, glibc uses per-thread arenas to reduce lock contention on a shared pool, which consumes real memory. In general, a data node process does not need per-thread arenas, since it does not perform any memory allocation after startup. (This difference in allocators does not appear to affect performance significantly.)

The glibc behavior is intended to be configurable via the MALLOC\_ARENA\_MAX environment variable, but a bug in this mechanism prior to glibc 2.16 meant that this variable could not be set to less than 8, so that the wasted memory could not be reclaimed. (Bug #15907219; see also [http://sourceware.org/bugzilla/show\\_bug.cgi?id=13137](http://sourceware.org/bugzilla/show_bug.cgi?id=13137) for more information concerning this issue.)

One possible workaround for this problem is to use the LD\_PRELOAD environment variable to preload a jemalloc memory allocation library to take the place of that supplied with glibc.

#### <span id="page-187-0"></span>• [ODirect](#page-187-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enabling this parameter causes [NDB](#page-50-0) to attempt using O\_DIRECT writes for LCP, backups, and redo logs, often lowering kswapd and CPU usage. When using NDB Cluster on Linux, enable [ODirect](#page-187-0) if you are using a 2.6 or later kernel.

[ODirect](#page-187-0) is disabled by default.

### <span id="page-187-1"></span>• [ODirectSyncFlag](#page-187-1)

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | boolean                                        |
| Default               | false                                          |
| Range                 | true, false                                    |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 8.4.0)

When this parameter is enabled, redo log writes are performed such that each completed file system write is handled as a call to fsync. The setting for this parameter is ignored if at least one of the following conditions is true:

- [ODirect](#page-187-0) is not enabled.
- [InitFragmentLogFiles](#page-173-1) is set to SPARSE.

#### Disabled by default.

<span id="page-188-1"></span>• RequireCertificate

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

If this parameter is set to true, the data node looks for a key and a valid and current certificate in the TLS search path, and cannot start if it does not find them.

<span id="page-188-0"></span>• RequireTls

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

If this parameter is set to true, connections to this data node must be authenticated using TLS.

<span id="page-188-2"></span>• [RestartOnErrorInsert](#page-188-2)

| Version (or<br>later) | NDB 8.4.0                   |
|-----------------------|-----------------------------|
| Type or units         | error code                  |
| Default               | 2                           |
| Range                 | 0 - 4                       |
| Restart Type          | Node Restart:<br>Requires a |
|                       | rolling restart             |

| of the cluster. |
|-----------------|
| (NDB 8.4.0)     |

This feature is accessible only when building the debug version where it is possible to insert errors in the execution of individual blocks of code as part of testing.

This feature is disabled by default.

#### <span id="page-189-0"></span>• [StopOnError](#page-189-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | 1                                                                                |
| Range                 | 0, 1                                                                             |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies whether a data node process should exit or perform an automatic restart when an error condition is encountered.

This parameter's default value is 1; this means that, by default, an error causes the data node process to halt.

When an error is encountered and StopOnError is 0, the data node process is restarted.

Users of MySQL Cluster Manager should note that, when StopOnError equals 1, this prevents the MySQL Cluster Manager agent from restarting any data nodes after it has performed its own restart and recovery. See [Starting and Stopping the Agent on Linux](https://dev.mysql.com/doc/mysql-cluster-manager/8.4/en/mcm-using-start-stop-agent-linux.md), for more information.

# <span id="page-189-2"></span>• [UseShm](#page-189-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enable a shared memory connection between this data node and the API node also running on this host. Set to 1 to enable.

# **Controlling Timeouts, Intervals, and Disk Paging**

<span id="page-189-1"></span>There are a number of [ndbd] parameters specifying timeouts and intervals between various actions in Cluster data nodes. Most of the timeout values are specified in milliseconds. Any exceptions to this are mentioned where applicable.

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 6000                                                                             |
| Range                 | 70 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

To prevent the main thread from getting stuck in an endless loop at some point, a "watchdog" thread checks the main thread. This parameter specifies the number of milliseconds between checks. If the process remains in the same state after three checks, the watchdog thread terminates it.

This parameter can easily be changed for purposes of experimentation or to adapt to local conditions. It can be specified on a per-node basis although there seems to be little reason for doing so.

The default timeout is 6000 milliseconds (6 seconds).

<span id="page-190-1"></span>• [TimeBetweenWatchDogCheckInitial](#page-190-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 6000                                                                             |
| Range                 | 70 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This is similar to the [TimeBetweenWatchDogCheck](#page-189-1) parameter, except that [TimeBetweenWatchDogCheckInitial](#page-190-1) controls the amount of time that passes between execution checks inside a storage node in the early start phases during which memory is allocated.

The default timeout is 6000 milliseconds (6 seconds).

<span id="page-190-0"></span>• [StartPartialTimeout](#page-190-0)

| Version (or<br>later) | NDB 8.4.0                      |
|-----------------------|--------------------------------|
| Type or units         | milliseconds                   |
| Default               | 30000                          |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF) |

| Node Restart:   |
|-----------------|
| Requires a      |
| rolling restart |
| of the cluster. |
| (NDB 8.4.0)     |
|                 |

This parameter specifies how long the Cluster waits for all data nodes to come up before the cluster initialization routine is invoked. This timeout is used to avoid a partial Cluster startup whenever possible.

This parameter is overridden when performing an initial start or initial restart of the cluster.

The default value is 30000 milliseconds (30 seconds). 0 disables the timeout, in which case the cluster may start only if all nodes are available.

# <span id="page-191-1"></span>• [StartPartitionedTimeout](#page-191-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

If the cluster is ready to start after waiting for [StartPartialTimeout](#page-190-0) milliseconds but is still possibly in a partitioned state, the cluster waits until this timeout has also passed. If [StartPartitionedTimeout](#page-191-1) is set to 0, the cluster waits indefinitely (2<sup>32</sup> −1 ms, or approximately 49.71 days).

This parameter is overridden when performing an initial start or initial restart of the cluster.

# <span id="page-191-0"></span>• [StartFailureTimeout](#page-191-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

If a data node has not completed its startup sequence within the time specified by this parameter, the node startup fails. Setting this parameter to 0 (the default value) means that no data node timeout is applied.

For nonzero values, this parameter is measured in milliseconds. For data nodes containing extremely large amounts of data, this parameter should be increased. For example, in the case of a data node containing several gigabytes of data, a period as long as 10−15 minutes (that is, 600000 to 1000000 milliseconds) might be required to perform a node restart.

<span id="page-192-1"></span>• [StartNoNodeGroupTimeout](#page-192-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 15000                                                                            |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When a data node is configured with [Nodegroup = 65536](#page-152-0), is regarded as not being assigned to any node group. When that is done, the cluster waits StartNoNodegroupTimeout milliseconds, then treats such nodes as though they had been added to the list passed to the --nowait-nodes option, and starts. The default value is 15000 (that is, the management server waits 15 seconds). Setting this parameter equal to 0 means that the cluster waits indefinitely.

StartNoNodegroupTimeout must be the same for all data nodes in the cluster; for this reason, you should always set it in the [ndbd default] section of the config.ini file, rather than for individual data nodes.

See Section 25.6.7, "Adding NDB Cluster Data Nodes Online", for more information.

<span id="page-192-0"></span>• [HeartbeatIntervalDbDb](#page-192-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 5000                                                                             |
| Range                 | 10 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

One of the primary methods of discovering failed nodes is by the use of heartbeats. This parameter states how often heartbeat signals are sent and how often to expect to receive them. Heartbeats cannot be disabled.

After missing four heartbeat intervals in a row, the node is declared dead. Thus, the maximum time for discovering a failure through the heartbeat mechanism is five times the heartbeat interval.

The default heartbeat interval is 5000 milliseconds (5 seconds). This parameter must not be changed drastically and should not vary widely between nodes. If one node uses 5000 milliseconds and the

node watching it uses 1000 milliseconds, obviously the node is declared dead very quickly. This parameter can be changed during an online software upgrade, but only in small increments.

See also [Network communication and latency](#page-62-1), as well as the description of the [ConnectCheckIntervalDelay](#page-195-0) configuration parameter.

#### <span id="page-193-0"></span>• [HeartbeatIntervalDbApi](#page-193-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 1500                                                                             |
| Range                 | 100 -<br>4294967039<br>(0xFFFFFEFF)                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Each data node sends heartbeat signals to each MySQL server (SQL node) to ensure that it remains in contact. If a MySQL server fails to send a heartbeat in time it is declared "dead," in which case all ongoing transactions are completed and all resources released. The SQL node cannot reconnect until all activities initiated by the previous MySQL instance have been completed. The threeheartbeat criteria for this determination are the same as described for [HeartbeatIntervalDbDb](#page-192-0).

The default interval is 1500 milliseconds (1.5 seconds). This interval can vary between individual data nodes because each data node watches the MySQL servers connected to it, independently of all other data nodes.

For more information, see [Network communication and latency.](#page-62-1)

# <span id="page-193-1"></span>• [HeartbeatOrder](#page-193-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | numeric                                                                                                   |
| Default               | 0                                                                                                         |
| Range                 | 0 - 65535                                                                                                 |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Data nodes send heartbeats to one another in a circular fashion whereby each data node monitors the previous one. If a heartbeat is not detected by a given data node, this node declares the previous data node in the circle "dead" (that is, no longer accessible by the cluster). The determination that a

data node is dead is done globally; in other words; once a data node is declared dead, it is regarded as such by all nodes in the cluster.

It is possible for heartbeats between data nodes residing on different hosts to be too slow compared to heartbeats between other pairs of nodes (for example, due to a very low heartbeat interval or temporary connection problem), such that a data node is declared dead, even though the node can still function as part of the cluster. .

In this type of situation, it may be that the order in which heartbeats are transmitted between data nodes makes a difference as to whether or not a particular data node is declared dead. If this declaration occurs unnecessarily, this can in turn lead to the unnecessary loss of a node group and as thus to a failure of the cluster.

Consider a setup where there are 4 data nodes A, B, C, and D running on 2 host computers host1 and host2, and that these data nodes make up 2 node groups, as shown in the following table:

**Table 25.9 Four data nodes A, B, C, D running on two host computers host1, host2; each data node belongs to one of two node groups.**

| Node Group    | Nodes Running on host1 | Nodes Running on host2 |
|---------------|------------------------|------------------------|
| Node Group 0: | Node A                 | Node B                 |
| Node Group 1: | Node C                 | Node D                 |

Suppose the heartbeats are transmitted in the order A->B->C->D->A. In this case, the loss of the heartbeat between the hosts causes node B to declare node A dead and node C to declare node B dead. This results in loss of Node Group 0, and so the cluster fails. On the other hand, if the order of transmission is A->B->D->C->A (and all other conditions remain as previously stated), the loss of the heartbeat causes nodes A and D to be declared dead; in this case, each node group has one surviving node, and the cluster survives.

The [HeartbeatOrder](#page-193-1) configuration parameter makes the order of heartbeat transmission userconfigurable. The default value for [HeartbeatOrder](#page-193-1) is zero; allowing the default value to be used on all data nodes causes the order of heartbeat transmission to be determined by NDB. If this parameter is used, it must be set to a nonzero value (maximum 65535) for every data node in the cluster, and this value must be unique for each data node; this causes the heartbeat transmission to proceed from data node to data node in the order of their [HeartbeatOrder](#page-193-1) values from lowest to highest (and then directly from the data node having the highest [HeartbeatOrder](#page-193-1) to the data node having the lowest value, to complete the circle). The values need not be consecutive. For example, to force the heartbeat transmission order A->B->D->C->A in the scenario outlined previously, you could set the [HeartbeatOrder](#page-193-1) values as shown here:

**Table 25.10 HeartbeatOrder values to force a heartbeat transition order of A->B->D->C->A.**

| Node | HeartbeatOrder Value |
|------|----------------------|
| A    | 10                   |
| B    | 20                   |
| C    | 30                   |
| D    | 25                   |

To use this parameter to change the heartbeat transmission order in a running NDB Cluster, you must first set [HeartbeatOrder](#page-193-1) for each data node in the cluster in the global configuration (config.ini) file (or files). To cause the change to take effect, you must perform either of the following:

• A complete shutdown and restart of the entire cluster.

• 2 rolling restarts of the cluster in succession. All nodes must be restarted in the same order in both rolling restarts.

You can use [DUMP 908](https://dev.mysql.com/doc/ndb-internals/en/dump-command-908.md) to observe the effect of this parameter in the data node logs.

<span id="page-195-0"></span>• [ConnectCheckIntervalDelay](#page-195-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter enables connection checking between data nodes after one of them has failed heartbeat checks for 5 intervals of up to [HeartbeatIntervalDbDb](#page-192-0) milliseconds.

Such a data node that further fails to respond within an interval of ConnectCheckIntervalDelay milliseconds is considered suspect, and is considered dead after two such intervals. This can be useful in setups with known latency issues.

The default value for this parameter is 0 (disabled).

<span id="page-195-1"></span>• [TimeBetweenLocalCheckpoints](#page-195-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | number of 4-<br>byte words,<br>as base-2<br>logarithm                            |
| Default               | 20                                                                               |
| Range                 | 0 - 31                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is an exception in that it does not specify a time to wait before starting a new local checkpoint; rather, it is used to ensure that local checkpoints are not performed in a cluster where relatively few updates are taking place. In most clusters with high update rates, it is likely that a new local checkpoint is started immediately after the previous one has been completed.

The size of all write operations executed since the start of the previous local checkpoints is added. This parameter is also exceptional in that it is specified as the base-2 logarithm of the number of 4byte words, so that the default value 20 means 4MB (4 × 220) of write operations, 21 would mean 8MB, and so on up to a maximum value of 31, which equates to 8GB of write operations.

All the write operations in the cluster are added together. Setting [TimeBetweenLocalCheckpoints](#page-195-1) to 6 or less means that local checkpoints are executed continuously without pause, independent of the cluster's workload.

<span id="page-196-0"></span>• [TimeBetweenGlobalCheckpoints](#page-196-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 2000                                                                             |
| Range                 | 20 - 32000                                                                       |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When a transaction is committed, it is committed in main memory in all nodes on which the data is mirrored. However, transaction log records are not flushed to disk as part of the commit. The reasoning behind this behavior is that having the transaction safely committed on at least two autonomous host machines should meet reasonable standards for durability.

It is also important to ensure that even the worst of cases—a complete crash of the cluster—is handled properly. To guarantee that this happens, all transactions taking place within a given interval are put into a global checkpoint, which can be thought of as a set of committed transactions that has been flushed to disk. In other words, as part of the commit process, a transaction is placed in a global checkpoint group. Later, this group's log records are flushed to disk, and then the entire group of transactions is safely committed to disk on all computers in the cluster.

We recommended when you are using solid-state disks (especially those employing NVMe) with Disk Data tables that you reduce this value. In such cases, you should also ensure that MaxDiskDataLatency is set to a proper level.

This parameter defines the interval between global checkpoints. The default is 2000 milliseconds.

<span id="page-196-1"></span>• [TimeBetweenGlobalCheckpointsTimeout](#page-196-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 120000                                                                           |
| Range                 | 10 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter defines the minimum timeout between global checkpoints. The default is 120000 milliseconds.

# <span id="page-197-1"></span>• [TimeBetweenEpochs](#page-197-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 100                                                                              |
| Range                 | 0 - 32000                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter defines the interval between synchronization epochs for NDB Cluster Replication. The default value is 100 milliseconds.

[TimeBetweenEpochs](#page-197-1) is part of the implementation of "micro-GCPs", which can be used to improve the performance of NDB Cluster Replication.

#### <span id="page-197-2"></span>• [TimeBetweenEpochsTimeout](#page-197-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 0                                                                                |
| Range                 | 0 - 256000                                                                       |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter defines a timeout for synchronization epochs for NDB Cluster Replication. If a node fails to participate in a global checkpoint within the time determined by this parameter, the node is shut down. The default value is 0; in other words, the timeout is disabled.

[TimeBetweenEpochsTimeout](#page-197-2) is part of the implementation of "micro-GCPs", which can be used to improve the performance of NDB Cluster Replication.

The current value of this parameter and a warning are written to the cluster log whenever a GCP save takes longer than 1 minute or a GCP commit takes longer than 10 seconds.

Setting this parameter to zero has the effect of disabling GCP stops caused by save timeouts, commit timeouts, or both. The maximum possible value for this parameter is 256000 milliseconds.

#### • [MaxBufferedEpochs](#page-197-0)

<span id="page-197-0"></span>

|      | Version (or<br>later) | NDB 8.4.0     |
|------|-----------------------|---------------|
|      | Type or units         | epochs        |
|      | Default               | 100           |
|      | Range                 | 0 - 100000    |
|      | Restart Type          | Node Restart: |
| 3968 |                       | Requires a    |

rolling restart of the cluster. (NDB 8.4.0)

The number of unprocessed epochs by which a subscribing node can lag behind. Exceeding this number causes a lagging subscriber to be disconnected.

The default value of 100 is sufficient for most normal operations. If a subscribing node does lag enough to cause disconnections, it is usually due to network or scheduling issues with regard to processes or threads. (In rare circumstances, the problem may be due to a bug in the [NDB](#page-50-0) client.) It may be desirable to set the value lower than the default when epochs are longer.

Disconnection prevents client issues from affecting the data node service, running out of memory to buffer data, and eventually shutting down. Instead, only the client is affected as a result of the disconnect (by, for example gap events in the binary log), forcing the client to reconnect or restart the process.

<span id="page-198-0"></span>• [MaxBufferedEpochBytes](#page-198-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 26214400                                                                         |
| Range                 | 26214400<br>(0x01900000)<br>- 4294967039<br>(0xFFFFFEFF)                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The total number of bytes allocated for buffering epochs by this node.

<span id="page-198-1"></span>• [TimeBetweenInactiveTransactionAbortCheck](#page-198-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 1000                                                                             |
| Range                 | 1000 -<br>4294967039<br>(0xFFFFFEFF)                                             |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Timeout handling is performed by checking a timer on each transaction once for every interval specified by this parameter. Thus, if this parameter is set to 1000 milliseconds, every transaction is checked for timing out once per second.

The default value is 1000 milliseconds (1 second).

# <span id="page-199-1"></span>• [TransactionInactiveTimeout](#page-199-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 4294967039<br>(0xFFFFFEFF)                                                       |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter states the maximum time that is permitted to lapse between operations in the same transaction before the transaction is aborted.

The default for this parameter is 4G (also the maximum). For a real-time database that needs to ensure that no transaction keeps locks for too long, this parameter should be set to a relatively small value. Setting it to 0 means that the application never times out. The unit is milliseconds.

# <span id="page-199-0"></span>• [TransactionDeadlockDetectionTimeout](#page-199-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 1200                                                                             |
| Range                 | 50 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When a node executes a query involving a transaction, the node waits for the other nodes in the cluster to respond before continuing. This parameter sets the amount of time that the transaction can spend executing within a data node, that is, the time that the transaction coordinator waits for each data node participating in the transaction to execute a request.

A failure to respond can occur for any of the following reasons:

- The node is "dead"
- The operation has entered a lock queue

• The node requested to perform the action could be heavily overloaded.

This timeout parameter states how long the transaction coordinator waits for query execution by another node before aborting the transaction, and is important for both node failure handling and deadlock detection.

The default timeout value is 1200 milliseconds (1.2 seconds).

The minimum for this parameter is 50 milliseconds.

<span id="page-0-0"></span>• [DiskSyncSize](#page-0-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 4M                                                                               |
| Range                 | 32K -<br>4294967039<br>(0xFFFFFEFF)                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This is the maximum number of bytes to store before flushing data to a local checkpoint file. This is done to prevent write buffering, which can impede performance significantly. This parameter is not intended to take the place of TimeBetweenLocalCheckpoints.

![](_page_0_Picture_8.jpeg)

#### **Note**

When ODirect is enabled, it is not necessary to set [DiskSyncSize](#page-0-0); in fact, in such cases its value is simply ignored.

The default value is 4M (4 megabytes).

<span id="page-0-1"></span>• [MaxDiskWriteSpeed](#page-0-1)

| Version (or<br>later) | NDB 8.4.0                                                                      |
|-----------------------|--------------------------------------------------------------------------------|
| Type or units         | numeric                                                                        |
| Default               | 20M                                                                            |
| Range                 | 1M - 1024G                                                                     |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the |

| cluster. (NDB |
|---------------|
| 8.4.0)        |

Set the maximum rate for writing to disk, in bytes per second, by local checkpoints and backup operations when no restarts (by this data node or any other data node) are taking place in this NDB Cluster.

For setting the maximum rate of disk writes allowed while this data node is restarting, use [MaxDiskWriteSpeedOwnRestart](#page-1-0). For setting the maximum rate of disk writes allowed while other data nodes are restarting, use [MaxDiskWriteSpeedOtherNodeRestart](#page-1-1). The minimum speed for disk writes by all LCPs and backup operations can be adjusted by setting [MinDiskWriteSpeed](#page-2-0).

<span id="page-1-1"></span>• [MaxDiskWriteSpeedOtherNodeRestart](#page-1-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | numeric                                                                                                   |
| Default               | 50M                                                                                                       |
| Range                 | 1M - 1024G                                                                                                |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Set the maximum rate for writing to disk, in bytes per second, by local checkpoints and backup operations when one or more data nodes in this NDB Cluster are restarting, other than this node.

For setting the maximum rate of disk writes allowed while this data node is restarting, use [MaxDiskWriteSpeedOwnRestart](#page-1-0). For setting the maximum rate of disk writes allowed when no data nodes are restarting anywhere in the cluster, use [MaxDiskWriteSpeed](#page-0-1). The minimum speed for disk writes by all LCPs and backup operations can be adjusted by setting [MinDiskWriteSpeed](#page-2-0).

<span id="page-1-0"></span>• [MaxDiskWriteSpeedOwnRestart](#page-1-0)

| Version (or<br>later) | NDB 8.4.0  |
|-----------------------|------------|
| Type or units         | numeric    |
| Default               | 200M       |
| Range                 | 1M - 1024G |
| Restart Type          | System     |

| cluster. (NDB |
|---------------|
| 8.4.0)        |

Set the maximum rate for writing to disk, in bytes per second, by local checkpoints and backup operations while this data node is restarting.

For setting the maximum rate of disk writes allowed while other data nodes are restarting, use [MaxDiskWriteSpeedOtherNodeRestart](#page-1-1). For setting the maximum rate of disk writes allowed when no data nodes are restarting anywhere in the cluster, use [MaxDiskWriteSpeed](#page-0-1). The minimum speed for disk writes by all LCPs and backup operations can be adjusted by setting [MinDiskWriteSpeed](#page-2-0).

#### <span id="page-2-0"></span>• [MinDiskWriteSpeed](#page-2-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | numeric                                                                                                   |
| Default               | 10M                                                                                                       |
| Range                 | 1M - 1024G                                                                                                |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Set the minimum rate for writing to disk, in bytes per second, by local checkpoints and backup operations.

The maximum rates of disk writes allowed for LCPs and backups under various conditions are adjustable using the parameters [MaxDiskWriteSpeed](#page-0-1), [MaxDiskWriteSpeedOwnRestart](#page-1-0), and [MaxDiskWriteSpeedOtherNodeRestart](#page-1-1). See the descriptions of these parameters for more information.

#### <span id="page-2-1"></span>• [ApiFailureHandlingTimeout](#page-2-1)

| Version (or<br>later) | NDB 8.4.5                      |
|-----------------------|--------------------------------|
| Type or units         | seconds                        |
| Default               | 600                            |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF) |
| Added                 | NDB 8.4.5                      |
| Restart Type          |                                |

Specifies the maximum time (in seconds) that the data node waits for API node failure handling to complete before escalating it to data node failure handling.

Added in NDB 8.4.5.

#### <span id="page-3-0"></span>• [ArbitrationTimeout](#page-3-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 7500                                                                             |
| Range                 | 10 -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies how long data nodes wait for a response from the arbitrator to an arbitration message. If this is exceeded, the network is assumed to have split.

The default value is 7500 milliseconds (7.5 seconds).

#### <span id="page-3-1"></span>• [Arbitration](#page-3-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | enumeration                                                                      |
| Default               | Default                                                                          |
| Range                 | Default,<br>Disabled,<br>WaitExternal                                            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The [Arbitration](#page-3-1) parameter enables a choice of arbitration schemes, corresponding to one of 3 possible values for this parameter:

- **Default.** This enables arbitration to proceed normally, as determined by the ArbitrationRank settings for the management and API nodes. This is the default value.
- **Disabled.** Setting Arbitration = Disabled in the [ndbd default] section of the config.ini file to accomplishes the same task as setting ArbitrationRank to 0 on all management and API nodes. When Arbitration is set in this way, any ArbitrationRank settings are ignored.
- **WaitExternal.** The [Arbitration](#page-3-1) parameter also makes it possible to configure arbitration in such a way that the cluster waits until after the time determined by [ArbitrationTimeout](#page-3-0) has passed for an external cluster manager application to perform arbitration instead of handling arbitration internally. This can be done by setting Arbitration = WaitExternal in the [ndbd default] section of the config.ini file. For best results with the WaitExternal setting, it

is recommended that [ArbitrationTimeout](#page-3-0) be 2 times as long as the interval required by the external cluster manager to perform arbitration.

![](_page_4_Picture_2.jpeg)

#### **Important**

This parameter should be used only in the [ndbd default] section of the cluster configuration file. The behavior of the cluster is unspecified when [Arbitration](#page-3-1) is set to different values for individual data nodes.

<span id="page-4-0"></span>• [RestartSubscriberConnectTimeout](#page-4-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | ms                                                                               |
| Default               | 12000                                                                            |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter determines the time that a data node waits for subscribing API nodes to connect. Once this timeout expires, any "missing" API nodes are disconnected from the cluster. To disable this timeout, set RestartSubscriberConnectTimeout to 0.

While this parameter is specified in milliseconds, the timeout itself is resolved to the next-greatest whole second.

<span id="page-4-1"></span>• [KeepAliveSendInterval](#page-4-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 60000                                                                            |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

You can enable and control the interval between keep-alive signals sent between data nodes by setting this parameter. The default for KeepAliveSendInterval is 60000 milliseconds (one minute); setting it to 0 disables keep-alive signals. Values between 1 and 10 inclusive are treated as 10.

This parameter may prove useful in environments which monitor and disconnect idle TCP connections, possibly causing unnecessary data node failures when the cluster is idle.

The heartbeat interval between management nodes and data nodes is always 100 milliseconds, and is not configurable.

**Buffering and logging.** Several [ndbd] configuration parameters enable the advanced user to have more control over the resources used by node processes and to adjust various buffer sizes at need.

These buffers are used as front ends to the file system when writing log records to disk. If the node is running in diskless mode, these parameters can be set to their minimum values without penalty due to the fact that disk writes are "faked" by the NDB storage engine's file system abstraction layer.

#### <span id="page-5-0"></span>• [UndoIndexBuffer](#page-5-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 2M                                                                               |
| Range                 | 1M -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter formerly set the size of the undo index buffer, but has no effect in current versions of NDB Cluster.

Use of this parameter in the cluster configuration file raises a deprecation warning; you should expect it to be removed in a future NDB Cluster release.

#### <span id="page-5-1"></span>• [UndoDataBuffer](#page-5-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 16M                                                                              |
| Range                 | 1M -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Deprecated            | Yes (in NDB<br>8.0)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter formerly set the size of the undo data buffer, but has no effect in current versions of NDB Cluster.

<span id="page-5-2"></span>Use of this parameter in the cluster configuration file raises a deprecation warning; you should expect it to be removed in a future NDB Cluster release.

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 32M                                                                              |
| Range                 | 1M -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

All update activities also need to be logged. The REDO log makes it possible to replay these updates whenever the system is restarted. The NDB recovery algorithm uses a "fuzzy" checkpoint of the data together with the UNDO log, and then applies the REDO log to play back all changes up to the restoration point.

RedoBuffer sets the size of the buffer in which the REDO log is written. The default value is 32MB; the minimum value is 1MB.

If this buffer is too small, the NDB storage engine issues error code 1221 (REDO log buffers overloaded). For this reason, you should exercise care if you attempt to decrease the value of RedoBuffer as part of an online change in the cluster's configuration.

[ndbmtd](#page-148-0) allocates a separate buffer for each LDM thread (see [ThreadConfig](#page-27-0)). For example, with 4 LDM threads, an [ndbmtd](#page-148-0) data node actually has 4 buffers and allocates RedoBuffer bytes to each one, for a total of 4 \* RedoBuffer bytes.

## <span id="page-6-0"></span>• [EventLogBufferSize](#page-6-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | bytes                                                                                                     |
| Default               | 8192                                                                                                      |
| Range                 | 0 - 64K                                                                                                   |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Controls the size of the circular buffer used for NDB log events within data nodes.

**Controlling log messages.** In managing the cluster, it is very important to be able to control the number of log messages sent for various event types to stdout. For each event category, there are 16 possible event levels (numbered 0 through 15). Setting event reporting for a given event category to level 15 means all event reports in that category are sent to stdout; setting it to 0 means that no event reports in that category are made.

By default, only the startup message is sent to stdout, with the remaining event reporting level defaults being set to 0. The reason for this is that these messages are also sent to the management server's cluster log.

An analogous set of levels can be set for the management client to determine which event levels to record in the cluster log.

#### <span id="page-7-0"></span>• [LogLevelStartup](#page-7-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 1                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for events generated during startup of the process.

The default level is 1.

#### <span id="page-7-1"></span>• [LogLevelShutdown](#page-7-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for events generated as part of graceful shutdown of a node.

The default level is 0.

#### <span id="page-7-2"></span>• [LogLevelStatistic](#page-7-2)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for statistical events such as number of primary key reads, number of updates, number of inserts, information relating to buffer usage, and so on.

The default level is 0.

<span id="page-8-0"></span>• [LogLevelCheckpoint](#page-8-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | log level                                                                        |
| Default               | 0                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for events generated by local and global checkpoints.

The default level is 0.

<span id="page-8-1"></span>• [LogLevelNodeRestart](#page-8-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for events generated during node restart.

The default level is 0.

<span id="page-8-2"></span>• [LogLevelConnection](#page-8-2)

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | integer                                        |
| Default               | 0                                              |
| Range                 | 0 - 15                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

| of the cluster. |
|-----------------|
| (NDB 8.4.0)     |

The reporting level for events generated by connections between cluster nodes.

The default level is 0.

#### <span id="page-9-0"></span>• [LogLevelError](#page-9-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for events generated by errors and warnings by the cluster as a whole. These errors do not cause any node failure but are still considered worth reporting.

The default level is 0.

#### <span id="page-9-1"></span>• [LogLevelCongestion](#page-9-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | level                                                                            |
| Default               | 0                                                                                |
| Range                 | 0 - 15                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The reporting level for events generated by congestion. These errors do not cause node failure but are still considered worth reporting.

The default level is 0.

#### <span id="page-9-2"></span>• [LogLevelInfo](#page-9-2)

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | integer                                        |
| Default               | 0                                              |
| Range                 | 0 - 15                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

| of the cluster. |
|-----------------|
| (NDB 8.4.0)     |

The reporting level for events generated for information about the general state of the cluster.

The default level is 0.

<span id="page-10-0"></span>• [MemReportFrequency](#page-10-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter controls how often data node memory usage reports are recorded in the cluster log; it is an integer value representing the number of seconds between reports.

Each data node's data memory and index memory usage is logged as both a percentage and a number of 32 KB pages of DataMemory, as set in the config.ini file. For example, if DataMemory is equal to 100 MB, and a given data node is using 50 MB for data memory storage, the corresponding line in the cluster log might look like this:

```
2006-12-24 01:18:16 [MgmSrvr] INFO -- Node 2: Data usage is 50%(1280 32K pages of total 2560)
```

[MemReportFrequency](#page-10-0) is not a required parameter. If used, it can be set for all cluster data nodes in the [ndbd default] section of config.ini, and can also be set or overridden for individual data nodes in the corresponding [ndbd] sections of the configuration file. The minimum value which is also the default value—is 0, in which case memory reports are logged only when memory usage reaches certain percentages (80%, 90%, and 100%), as mentioned in the discussion of statistics events in Section 25.6.3.2, "NDB Cluster Log Events".

<span id="page-10-1"></span>• [StartupStatusReportFrequency](#page-10-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | seconds                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When a data node is started with the [--initial](#page-137-0), it initializes the redo log file during Start Phase 4 (see Section 25.6.4, "Summary of NDB Cluster Start Phases"). When very large values are set for NoOfFragmentLogFiles, FragmentLogFileSize, or both, this initialization can take a long time. You can force reports on the progress of this process to be logged periodically, by means of3981 the [StartupStatusReportFrequency](#page-10-1) configuration parameter. In this case, progress is reported in the cluster log, in terms of both the number of files and the amount of space that have been initialized, as shown here:

```
2009-06-20 16:39:23 [MgmSrvr] INFO -- Node 1: Local redo log file initialization status:
#Total files: 80, Completed: 60
#Total MBytes: 20480, Completed: 15557
2009-06-20 16:39:23 [MgmSrvr] INFO -- Node 2: Local redo log file initialization status:
#Total files: 80, Completed: 60
#Total MBytes: 20480, Completed: 15570
```

These reports are logged each [StartupStatusReportFrequency](#page-10-1) seconds during Start Phase 4. If [StartupStatusReportFrequency](#page-10-1) is 0 (the default), then reports are written to the cluster log only when at the beginning and at the completion of the redo log file initialization process.

#### **Data Node Debugging Parameters**

The following parameters are intended for use during testing or debugging of data nodes, and not for use in production.

#### <span id="page-11-0"></span>• [DictTrace](#page-11-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | undefined                                                                        |
| Range                 | 0 - 100                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

It is possible to cause logging of traces for events generated by creating and dropping tables using DictTrace. This parameter is useful only in debugging NDB kernel code. DictTrace takes an integer value. 0 is the default, and means no logging is performed; 1 enables trace logging, and 2 enables logging of additional [DBDICT](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbdict.md) debugging output.

#### <span id="page-11-1"></span>• [WatchDogImmediateKill](#page-11-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

You can cause threads to be killed immediately whenever watchdog issues occur by enabling the WatchDogImmediateKill data node configuration parameter. This parameter should be used only when debugging or troubleshooting, to obtain trace files reporting exactly what was occurring the instant that execution ceased.

**Backup parameters.** The [ndbd] parameters discussed in this section define memory buffers set aside for execution of online backups.

## <span id="page-12-0"></span>• [BackupDataBufferSize](#page-12-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 16M                                                                              |
| Range                 | 512K -<br>4294967039<br>(0xFFFFFEFF)                                             |
| Deprecated            | Yes (in NDB<br>7.6)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

In creating a backup, there are two buffers used for sending data to the disk. The backup data buffer is used to fill in data recorded by scanning a node's tables. Once this buffer has been filled to the level specified as [BackupWriteSize](#page-14-0), the pages are sent to disk. While flushing data to disk, the backup process can continue filling this buffer until it runs out of space. When this happens, the backup process pauses the scan and waits until some disk writes have completed freeing up memory so that scanning may continue.

The default value for this parameter is 16MB. The minimum is 512K.

## <span id="page-12-1"></span>• [BackupDiskWriteSpeedPct](#page-12-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | percent                                                                          |
| Default               | 50                                                                               |
| Range                 | 0 - 90                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

BackupDiskWriteSpeedPct applies only when a backup is single-threaded; since NDB 8.4 supports multi-threaded backups, it is usually not necessary to adjust this parameter, which has no effect in the multi-threaded case. The discussion that follows is specific to single-threaded backups.

During normal operation, data nodes attempt to maximize the disk write speed used for local checkpoints and backups while remaining within the bounds set by [MinDiskWriteSpeed](#page-2-0) and [MaxDiskWriteSpeed](#page-0-1). Disk write throttling gives each LDM thread an equal share of the total budget. This allows parallel LCPs to take place without exceeding the disk I/O budget. Because a backup is executed by only one LDM thread, this effectively caused a budget cut, resulting in longer backup completion times, and—if the rate of change is sufficiently high—in failure to complete the backup when the backup log buffer fill rate is higher than the achievable write rate.

This problem can be addressed by using the BackupDiskWriteSpeedPct configuration parameter, which takes a value in the range 0-90 (inclusive) which is interpreted as the percentage of the node's maximum write rate budget that is reserved prior to sharing out the remainder of the

budget among LDM threads for LCPs. The LDM thread running the backup receives the whole write rate budget for the backup, plus its (reduced) share of the write rate budget for local checkpoints.

The default value for this parameter is 50 (interpreted as 50%).

#### <span id="page-13-0"></span>• [BackupLogBufferSize](#page-13-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 16M                                                                              |
| Range                 | 2M -<br>4294967039<br>(0xFFFFFEFF)                                               |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The backup log buffer fulfills a role similar to that played by the backup data buffer, except that it is used for generating a log of all table writes made during execution of the backup. The same principles apply for writing these pages as with the backup data buffer, except that when there is no more space in the backup log buffer, the backup fails. For that reason, the size of the backup log buffer must be large enough to handle the load caused by write activities while the backup is being made. See Section 25.6.8.3, "Configuration for NDB Cluster Backups".

The default value for this parameter should be sufficient for most applications. In fact, it is more likely for a backup failure to be caused by insufficient disk write speed than it is for the backup log buffer to become full. If the disk subsystem is not configured for the write load caused by applications, the cluster is unlikely to be able to perform the desired operations.

It is preferable to configure cluster nodes in such a manner that the processor becomes the bottleneck rather than the disks or the network connections.

The default value for this parameter is 16MB.

#### <span id="page-13-1"></span>• [BackupMemory](#page-13-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 32M                                                                              |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Deprecated            | Yes (in NDB<br>7.4)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is deprecated, and subject to removal in a future version of NDB Cluster. Any setting made for it is ignored.

#### <span id="page-14-1"></span>• [BackupReportFrequency](#page-14-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | seconds                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter controls how often backup status reports are issued in the management client during a backup, as well as how often such reports are written to the cluster log (provided cluster event logging is configured to permit it—see Logging and checkpointing). [BackupReportFrequency](#page-14-1) represents the time in seconds between backup status reports.

The default value is 0.

#### <span id="page-14-0"></span>• [BackupWriteSize](#page-14-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 256K                                                                             |
| Range                 | 32K -<br>4294967039<br>(0xFFFFFEFF)                                              |
| Deprecated            | Yes (in NDB<br>7.6)                                                              |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the default size of messages written to disk by the backup log and backup data buffers.

The default value for this parameter is 256KB.

#### <span id="page-14-2"></span>• [BackupMaxWriteSize](#page-14-2)

| Version (or<br>later) | NDB 8.4.0                            |
|-----------------------|--------------------------------------|
| Type or units         | bytes                                |
| Default               | 1M                                   |
| Range                 | 256K -<br>4294967039<br>(0xFFFFFEFF) |

| Deprecated   | Yes (in NDB<br>7.6)                                                              |
|--------------|----------------------------------------------------------------------------------|
| Restart Type | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the maximum size of messages written to disk by the backup log and backup data buffers.

The default value for this parameter is 1MB.

<span id="page-15-0"></span>• [CompressedBackup](#page-15-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enabling this parameter causes backup files to be compressed. The compression used is equivalent to gzip --fast, and can save 50% or more of the space required on the data node to store uncompressed backup files. Compressed backups can be enabled for individual data nodes, or for all data nodes (by setting this parameter in the [ndbd default] section of the config.ini file).

![](_page_15_Picture_7.jpeg)

## **Important**

You cannot restore a compressed backup to a cluster running a MySQL version that does not support this feature.

The default value is 0 (disabled).

<span id="page-15-1"></span>• [RequireEncryptedBackup](#page-15-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 1                                                                            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

If set to 1, backups must be encrypted. While it is possible to set this parameter for each data node individually, it is recommended that you set it in the [ndbd default] section of the config.ini global configuration file. For more information about performing encrypted backups, see Section 25.6.8.2, "Using The NDB Cluster Management Client to Create a Backup".

![](_page_16_Picture_1.jpeg)

#### **Note**

The location of the backup files is determined by the BackupDataDir data node configuration parameter.

**Additional requirements.** When specifying these parameters, the following relationships must hold true. Otherwise, the data node cannot start.

- BackupDataBufferSize >= BackupWriteSize + 188KB
- BackupLogBufferSize >= BackupWriteSize + 16KB
- BackupMaxWriteSize >= BackupWriteSize

#### **NDB Cluster Realtime Performance Parameters**

The [ndbd] parameters discussed in this section are used in scheduling and locking of threads to specific CPUs on multiprocessor data node hosts.

![](_page_16_Picture_10.jpeg)

#### **Note**

To make use of these parameters, the data node process must be run as system root.

<span id="page-16-0"></span>• [BuildIndexThreads](#page-16-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 128                                                                              |
| Range                 | 0 - 128                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter determines the number of threads to create when rebuilding ordered indexes during a system or node start, as well as when running ndb\_restore --rebuild-indexes. It is supported only when there is more than one fragment for the table per data node (for example, when COMMENT="NDB\_TABLE=PARTITION\_BALANCE=FOR\_RA\_BY\_LDM\_X\_2" is used with CREATE TABLE).

Setting this parameter to 0 (the default) disables multithreaded building of ordered indexes.

This parameter is supported when using [ndbd](#page-134-0) or [ndbmtd](#page-148-0).

You can enable multithreaded builds during data node initial restarts by setting the [TwoPassInitialNodeRestartCopy](#page-20-0) data node configuration parameter to TRUE.

<span id="page-16-1"></span>• [LockExecuteThreadToCPU](#page-16-1)

| Version (or<br>later) | NDB 8.4.0      |
|-----------------------|----------------|
| Type or units         | set of CPU IDs |
| Default               | 0              |
| Range                 |                |

| Node Restart:   |
|-----------------|
| Requires a      |
| rolling restart |
| of the cluster. |
| (NDB 8.4.0)     |
|                 |

When used with [ndbd](#page-134-0), this parameter (now a string) specifies the ID of the CPU assigned to handle the NDBCLUSTER execution thread. When used with [ndbmtd](#page-148-0), the value of this parameter is a comma-separated list of CPU IDs assigned to handle execution threads. Each CPU ID in the list should be an integer in the range 0 to 65535 (inclusive).

The number of IDs specified should match the number of execution threads determined by [MaxNoOfExecutionThreads](#page-22-0). However, there is no guarantee that threads are assigned to CPUs in any given order when using this parameter. You can obtain more finely-grained control of this type using [ThreadConfig](#page-27-0).

[LockExecuteThreadToCPU](#page-16-1) has no default value.

#### <span id="page-17-0"></span>• [LockMaintThreadsToCPU](#page-17-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | CPU ID                                                                           |
| Default               | 0                                                                                |
| Range                 | 0 - 64K                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the ID of the CPU assigned to handle NDBCLUSTER maintenance threads.

The value of this parameter is an integer in the range 0 to 65535 (inclusive). There is no default value.

#### <span id="page-17-1"></span>• [Numa](#page-17-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 1                                                                                |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter determines whether Non-Uniform Memory Access (NUMA) is controlled by the operating system or by the data node process, whether the data node uses [ndbd](#page-134-0) or [ndbmtd](#page-148-0). By default, NDB attempts to use an interleaved NUMA memory allocation policy on any data node where the host operating system provides NUMA support.

Setting Numa = 0 means that the datanode process does not itself attempt to set a policy for memory allocation, and permits this behavior to be determined by the operating system, which may be further guided by the separate numactl tool. That is, Numa = 0 yields the system default behavior, which can be customised by numactl. For many Linux systems, the system default behavior is to allocate socket-local memory to any given process at allocation time. This can be problematic when using [ndbmtd](#page-148-0); this is because nbdmtd allocates all memory at startup, leading to an imbalance, giving different access speeds for different sockets, especially when locking pages in main memory.

Setting Numa = 1 means that the data node process uses libnuma to request interleaved memory allocation. (This can also be accomplished manually, on the operating system level, using numactl.) Using interleaved allocation in effect tells the data node process to ignore non-uniform memory access but does not attempt to take any advantage of fast local memory; instead, the data node process tries to avoid imbalances due to slow remote memory. If interleaved allocation is not desired, set Numa to 0 so that the desired behavior can be determined on the operating system level.

The Numa configuration parameter is supported only on Linux systems where libnuma.so is available.

#### <span id="page-18-0"></span>• [RealtimeScheduler](#page-18-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Setting this parameter to 1 enables real-time scheduling of data node threads.

The default is 0 (scheduling disabled).

## <span id="page-18-1"></span>• [SchedulerExecutionTimer](#page-18-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | µs                                                                               |
| Default               | 50                                                                               |
| Range                 | 0 - 11000                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the time in microseconds for threads to be executed in the scheduler before being sent. Setting it to 0 minimizes the response time; to achieve higher throughput, you can increase the value at the expense of longer response times.

The default is 50 μsec, which our testing shows to increase throughput slightly in high-load cases without materially delaying requests.

## <span id="page-19-0"></span>• [SchedulerResponsiveness](#page-19-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 5                                                                                |
| Range                 | 0 - 10                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Set the balance in the NDB scheduler between speed and throughput. This parameter takes an integer whose value is in the range 0-10 inclusive, with 5 as the default. Higher values provide better response times relative to throughput. Lower values provide increased throughput at the expense of longer response times.

#### <span id="page-19-1"></span>• [SchedulerSpinTimer](#page-19-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | µs                                                                               |
| Default               | 0                                                                                |
| Range                 | 0 - 500                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the time in microseconds for threads to be executed in the scheduler before sleeping.

![](_page_19_Picture_7.jpeg)

## **Note**

If [SpinMethod](#page-19-2) is set, any setting for this parameter is ignored.

#### <span id="page-19-2"></span>• [SpinMethod](#page-19-2)

| Version (or<br>later) | NDB 8.4.0                                                                                     |  |
|-----------------------|-----------------------------------------------------------------------------------------------|--|
| Type or units         | enumeration                                                                                   |  |
| Default               | StaticSpinning                                                                                |  |
| Range                 | CostBasedSpinning,<br>LatencyOptimisedSpinning,<br>DatabaseMachineSpinning,<br>StaticSpinning |  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart                                                |  |

| of the cluster. |
|-----------------|
| (NDB 8.4.0)     |

This parameter provides a simple interface to control adaptive spinning on data nodes, with four possible values furnishing presets for spin parameter values, as shown in the following list:

- 1. StaticSpinning (default): Sets EnableAdaptiveSpinning to false and [SchedulerSpinTimer](#page-19-1) to 0. (SetAllowedSpinOverhead is not relevant in this case.)
- 2. CostBasedSpinning: Sets EnableAdaptiveSpinning to true, [SchedulerSpinTimer](#page-19-1) to 100, and SetAllowedSpinOverhead to 200.
- 3. LatencyOptimisedSpinning: Sets EnableAdaptiveSpinning to true, [SchedulerSpinTimer](#page-19-1) to 200, and SetAllowedSpinOverhead to 1000.
- 4. DatabaseMachineSpinning: Sets EnableAdaptiveSpinning to true, [SchedulerSpinTimer](#page-19-1) to 500, and SetAllowedSpinOverhead to 10000. This is intended for use in cases where threads own their own CPUs.

The spin parameters modified by [SpinMethod](#page-19-2) are described in the following list:

- [SchedulerSpinTimer](#page-19-1): This is the same as the data node configuration parameter of that name. The setting applied to this parameter by SpinMethod overrides any value set in the config.ini file.
- EnableAdaptiveSpinning: Enables or disables adaptive spinning. Disabling it causes spinning to be performed without making any checks for CPU resources. This parameter cannot be set directly in the cluster configuration file, and under most circumstances should not need to be, but can be enabled directly using [DUMP 104004 1](https://dev.mysql.com/doc/ndb-internals/en/dump-command-104004.md) or disabled with [DUMP 104004 0](https://dev.mysql.com/doc/ndb-internals/en/dump-command-104004.md) in the [ndb\\_mgm](#page-159-0) management client.
- SetAllowedSpinOverhead: Sets the amount of CPU time to allow for gaining latency. This parameter cannot be set directly in the config.ini file. In most cases, the setting applied by SpinMethod should be satisfactory, but if it is necessary to change it directly, you can use [DUMP](https://dev.mysql.com/doc/ndb-internals/en/dump-command-104002.md) 104002 [overhead](https://dev.mysql.com/doc/ndb-internals/en/dump-command-104002.md) to do so, where overhead is a value ranging from 0 to 10000, inclusive; see the description of the indicated DUMP command for details.

On platforms lacking usable spin instructions, such as PowerPC and some SPARC platforms, spin time is set to 0 in all situations, and values for SpinMethod other than StaticSpinning are ignored.

<span id="page-20-0"></span>• [TwoPassInitialNodeRestartCopy](#page-20-0)

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | boolean                                        |
| Default               | true                                           |
| Range                 | true, false                                    |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

of the cluster. (NDB 8.4.0)

Multithreaded building of ordered indexes can be enabled for initial restarts of data nodes by setting this configuration parameter to true (the default value), which enables two-pass copying of data during initial node restarts.

You must also set [BuildIndexThreads](#page-16-0) to a nonzero value.

<span id="page-21-2"></span>**Multi-Threading Configuration Parameters (ndbmtd).** [ndbmtd](#page-148-0) runs by default as a singlethreaded process and must be configured to use multiple threads, using either of two methods, both of which require setting configuration parameters in the config.ini file. The first method is simply to set an appropriate value for the [MaxNoOfExecutionThreads](#page-22-0) configuration parameter. A second method makes it possible to set up more complex rules for [ndbmtd](#page-148-0) multithreading using [ThreadConfig](#page-27-0). The next few paragraphs provide information about these parameters and their use with multithreaded data nodes.

![](_page_21_Picture_5.jpeg)

#### **Note**

A backup using parallelism on the data nodes requires that multiple LDMs are in use on all data nodes in the cluster prior to taking the backup. For more information, see Section 25.6.8.5, "Taking an NDB Backup with Parallel Data Nodes", as well as [Restoring from a backup taken in parallel](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-parallel-data-node-backup.md).

#### <span id="page-21-0"></span>• [AutomaticThreadConfig](#page-21-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | boolean                                                                                                                                                                                                           |
| Default               | false                                                                                                                                                                                                             |
| Range                 | true, false                                                                                                                                                                                                       |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

When set to 1, enables automatic thread configuration employing the number of CPUs available to a data node taking into account any limits set by taskset, numactl, virtual machines, Docker, and other such means of controlling which CPUs are available to a given application (on Windows platforms, automatic thread configuration uses all CPUs which are online); alternatively, you can set [NumCPUs](#page-26-0) to the desired number of CPUs (up to 1024, the maximum number of CPUs that can be handled by automatic thread configuration). Any settings for [ThreadConfig](#page-27-0) and [MaxNoOfExecutionThreads](#page-22-0) are ignored. In addition, enabling this parameter automatically disables [ClassicFragmentation](#page-21-1).

#### <span id="page-21-1"></span>• [ClassicFragmentation](#page-21-1)

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | boolean                                                                          |
|---------------|----------------------------------------------------------------------------------|
| Default       | true                                                                             |
| Range         | true, false                                                                      |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When enabled (set to true), NDB distributes fragments among LDMs such that the default number of partitions per node is equal to the minimum number of local data manager (LDM) threads per data node.

For new clusters, setting ClassicFragmentation to false when first setting up the cluster is preferable; doing so causes the number of partitions per node to be equal to the value of [PartitionsPerNode](#page-27-1), ensuring that all partitions are spread out evenly between all LDMs.

This parameter and [AutomaticThreadConfig](#page-21-0) are mutually exclusive; enabling AutomaticThreadConfig automatically disables ClassicFragmentation.

#### • EnableMultithreadedBackup

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 1                                                                                |
| Range                 | 0 - 1                                                                            |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enables multi-threaded backup. If each data node has at least 2 LDMs, all LDM threads participate in the backup, which is created using one subdirectory per LDM thread, and each subdirectory containing .ctl, .Data, and .log backup files.

This parameter is normally enabled (set to 1) for [ndbmtd](#page-148-0). To force a single-threaded backup that can be restored easily using older versions of ndb\_restore, disable multi-threaded backup by setting this parameter to 0. This must be done for each data node in the cluster.

See Section 25.6.8.5, "Taking an NDB Backup with Parallel Data Nodes", and [Restoring from a](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-parallel-data-node-backup.md) [backup taken in parallel](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-parallel-data-node-backup.md), for more information.

#### <span id="page-22-0"></span>• MaxNoOfExecutionThreads

| Version (or<br>later) | NDB 8.4.0                                    |
|-----------------------|----------------------------------------------|
| Type or units         | integer                                      |
| Default               | 2                                            |
| Range                 | 2 - 72                                       |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete |

| shutdown and   |
|----------------|
| restart of the |
| cluster. (NDB  |
| 8.4.0)         |

This parameter directly controls the number of execution threads used by [ndbmtd](#page-148-0), up to a maximum of 72. Although this parameter is set in [ndbd] or [ndbd default] sections of the config.ini file, it is exclusive to [ndbmtd](#page-148-0) and does not apply to [ndbd](#page-134-0).

Enabling [AutomaticThreadConfig](#page-21-0) causes any setting for this parameter to be ignored.

Setting MaxNoOfExecutionThreads sets the number of threads for each type as determined by a matrix in the file storage/ndb/src/common/mt\_thr\_config.cpp. This table shows these numbers of threads for possible values of MaxNoOfExecutionThreads.

**Table 25.11 MaxNoOfExecutionThreads values and the corresponding number of threads by thread type (LQH, TC, Send, Receive).**

| MaxNoOfExecutionThreads<br>Value | LDM Threads | TC Threads | Send Threads | Receive Threads |
|----------------------------------|-------------|------------|--------------|-----------------|
| 0 3                              | 1           | 0          | 0            | 1               |
| 4 6                              | 2           | 0          | 0            | 1               |
| 7 8                              | 4           | 0          | 0            | 1               |
| 9                                | 4           | 2          | 0            | 1               |
| 10                               | 4           | 2          | 1            | 1               |
| 11                               | 4           | 3          | 1            | 1               |
| 12                               | 6           | 2          | 1            | 1               |
| 13                               | 6           | 3          | 1            | 1               |
| 14                               | 6           | 3          | 1            | 2               |
| 15                               | 6           | 3          | 2            | 2               |
| 16                               | 8           | 3          | 1            | 2               |
| 17                               | 8           | 4          | 1            | 2               |
| 18                               | 8           | 4          | 2            | 2               |
| 19                               | 8           | 5          | 2            | 2               |
| 20                               | 10          | 4          | 2            | 2               |
| 21                               | 10          | 5          | 2            | 2               |
| 22                               | 10          | 5          | 2            | 3               |
| 23                               | 10          | 6          | 2            | 3               |
| 24                               | 12          | 5          | 2            | 3               |
| 25                               | 12          | 6          | 2            | 3               |
| 26                               | 12          | 6          | 3            | 3               |
| 27                               | 12          | 7          | 3            | 3               |
| 28                               | 12          | 7          | 3            | 4               |
| 29                               | 12          | 8          | 3            | 4               |
| 30                               | 12          | 8          | 4            | 4               |
| 31                               | 12          | 9          | 4            | 4               |
| 32                               | 16          | 8          | 3            | 3               |
| 33                               | 16          | 8          | 3            | 4               |

|       | LDM Threads<br>MaxNoOfExecutionThreads | TC Threads | Send Threads | Receive Threads |
|-------|----------------------------------------|------------|--------------|-----------------|
| Value |                                        |            |              |                 |
| 34    | 16                                     | 8          | 4            | 4               |
| 35    | 16                                     | 9          | 4            | 4               |
| 36    | 16                                     | 10         | 4            | 4               |
| 37    | 16                                     | 10         | 4            | 5               |
| 38    | 16                                     | 11         | 4            | 5               |
| 39    | 16                                     | 11         | 5            | 5               |
| 40    | 20                                     | 10         | 4            | 4               |
| 41    | 20                                     | 10         | 4            | 5               |
| 42    | 20                                     | 11         | 4            | 5               |
| 43    | 20                                     | 11         | 5            | 5               |
| 44    | 20                                     | 12         | 5            | 5               |
| 45    | 20                                     | 12         | 5            | 6               |
| 46    | 20                                     | 13         | 5            | 6               |
| 47    | 20                                     | 13         | 6            | 6               |
| 48    | 24                                     | 12         | 5            | 5               |
| 49    | 24                                     | 12         | 5            | 6               |
| 50    | 24                                     | 13         | 5            | 6               |
| 51    | 24                                     | 13         | 6            | 6               |
| 52    | 24                                     | 14         | 6            | 6               |
| 53    | 24                                     | 14         | 6            | 7               |
| 54    | 24                                     | 15         | 6            | 7               |
| 55    | 24                                     | 15         | 7            | 7               |
| 56    | 24                                     | 16         | 7            | 7               |
| 57    | 24                                     | 16         | 7            | 8               |
| 58    | 24                                     | 17         | 7            | 8               |
| 59    | 24                                     | 17         | 8            | 8               |
| 60    | 24                                     | 18         | 8            | 8               |
| 61    | 24                                     | 18         | 8            | 9               |
| 62    | 24                                     | 19         | 8            | 9               |
| 63    | 24                                     | 19         | 9            | 9               |
| 64    | 32                                     | 16         | 7            | 7               |
| 65    | 32                                     | 16         | 7            | 8               |
| 66    | 32                                     | 17         | 7            | 8               |
| 67    | 32                                     | 17         | 8            | 8               |
| 68    | 32                                     | 18         | 8            | 8               |
| 69    | 32                                     | 18         | 8            | 9               |
| 70    | 32                                     | 19         | 8            | 9               |
| 71    | 32                                     | 20         | 8            | 9               |

| MaxNoOfExecutionThreads<br>Value | LDM Threads | TC Threads | Send Threads | Receive Threads |
|----------------------------------|-------------|------------|--------------|-----------------|
| 72                               | 32          | 20         | 8            | 10              |

There is always one SUMA (replication) thread.

[NoOfFragmentLogParts](#page-26-1) should be set equal to the number of LDM threads used by [ndbmtd](#page-148-0), as determined by the setting for this parameter. This ratio should not be any greater than 4:1; a configuration in which this is the case is specifically disallowed.

The number of LDM threads also determines the number of partitions used by an NDB table that is not explicitly partitioned; this is the number of LDM threads times the number of data nodes in the cluster. (If [ndbd](#page-134-0) is used on the data nodes rather than [ndbmtd](#page-148-0), then there is always a single LDM thread; in this case, the number of partitions created automatically is simply equal to the number of data nodes. See Section 25.2.2, "NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions", for more information.

Adding large tablespaces for Disk Data tables when using more than the default number of LDM threads may cause issues with resource and CPU usage if the disk page buffer is insufficiently large; see the description of the [DiskPageBufferMemory](#page-35-0) configuration parameter, for more information.

The thread types are described later in this section (see [ThreadConfig](#page-27-0)).

Setting this parameter outside the permitted range of values causes the management server to abort on startup with the error Error line number: Illegal value value for parameter MaxNoOfExecutionThreads.

For MaxNoOfExecutionThreads, a value of 0 or 1 is rounded up internally by NDB to 2, so that 2 is considered this parameter's default and minimum value.

MaxNoOfExecutionThreads is generally intended to be set equal to the number of CPU threads available, and to allocate a number of threads of each type suitable to typical workloads. It does not assign particular threads to specified CPUs. For cases where it is desirable to vary from the settings provided, or to bind threads to CPUs, you should use [ThreadConfig](#page-27-0) instead, which allows you to allocate each thread directly to a desired type, CPU, or both.

The multithreaded data node process always spawns, at a minimum, the threads listed here:

- 1 local query handler (LDM) thread
- 1 receive thread
- 1 subscription manager (SUMA or replication) thread

For a MaxNoOfExecutionThreads value of 8 or less, no TC threads are created, and TC handling is instead performed by the main thread.

Changing the number of LDM threads normally requires a system restart, whether it is changed using this parameter or [ThreadConfig](#page-27-0), but it is possible to effect the change using a node initial restart (NI) provided the following two conditions are met:

- Each LDM thread handles a maximum of 8 fragments, and
- The total number of table fragments is an integer multiple of the number of LDM threads.
- MaxSendDelay

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | microseconds                                                                     |
|---------------|----------------------------------------------------------------------------------|
| Default       | 0                                                                                |
| Range         | 0 - 11000                                                                        |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter can be used to cause data nodes to wait momentarily before sending data to API nodes; in some circumstances, described in the following paragraphs, this can result in more efficient sending of larger volumes of data and higher overall throughput.

MaxSendDelay can be useful when there are a great many API nodes at saturation point or close to it, which can result in waves of increasing and decreasing performance. This occurs when the data nodes are able to send results back to the API nodes relatively quickly, with many small packets to process, which can take longer to process per byte compared to large packets, thus slowing down the API nodes; later, the data nodes start sending larger packets again.

To handle this type of scenario, you can set MaxSendDelay to a nonzero value, which helps to ensure that responses are not sent back to the API nodes so quickly. When this is done, responses are sent immediately when there is no other competing traffic, but when there is, setting MaxSendDelay causes the data nodes to wait long enough to ensure that they send larger packets. In effect, this introduces an artificial bottleneck into the send process, which can actually improve throughput significantly.

#### <span id="page-26-1"></span>• NoOfFragmentLogParts

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | numeric                                                                                                                                                |
| Default               | 4                                                                                                                                                      |
| Range                 | 4, 6, 8, 10, 12,<br>16, 20, 24, 32                                                                                                                     |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

Set the number of log file groups for redo logs belonging to this [ndbmtd](#page-148-0). The value of this parameter should be set equal to the number of LDM threads used by [ndbmtd](#page-148-0) as determined by the setting for [MaxNoOfExecutionThreads](#page-22-0). A configuration using more than 4 redo log parts per LDM is disallowed.

See the description of [MaxNoOfExecutionThreads](#page-22-0) for more information.

#### <span id="page-26-0"></span>• [NumCPUs](#page-26-0)

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | integer                                                                                                                                                                                                           |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Default       | 0                                                                                                                                                                                                                 |
| Range         | 0 - 1024                                                                                                                                                                                                          |
| Restart Type  | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

Cause automatic thread configuration to use only this many CPUs. Has no effect if [AutomaticThreadConfig](#page-21-0) is not enabled.

#### <span id="page-27-1"></span>• [PartitionsPerNode](#page-27-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 2                                                                                |
| Range                 | 1 - 32                                                                           |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Sets the number of partitions used on each node when creating a new NDB table. This makes it possible to avoid splitting up tables into an excessive number of partitions when the number of local data managers (LDMs) grows high.

While it is possible to set this parameter to different values on different data nodes and there are no known issues with doing so, this is also not likely to be of any advantage; for this reason, it is recommended simply to set it once, for all data nodes, in the [ndbd default] section of the global config.ini file.

If [ClassicFragmentation](#page-21-1) is enabled, any setting for this parameter is ignored. (Remember that enabling [AutomaticThreadConfig](#page-21-0) disables ClassicFragmentation.)

#### <span id="page-27-0"></span>• ThreadConfig

| Version (or<br>later) | NDB 8.4.0          |
|-----------------------|--------------------|
| Type or units         | string             |
| Default               | ''                 |
| Range                 |                    |
| Restart Type          | System<br>Restart: |

Requires a complete shutdown and restart of the cluster. (NDB 8.4.0)

This parameter is used with [ndbmtd](#page-148-0) to assign threads of different types to different CPUs. Its value is a string whose format has the following syntax:

```
ThreadConfig := entry[,entry[,...]]
entry := type={param[,param[,...]]}
type := ldm | query | recover | main | recv | send | rep | io | tc | watchdog | idxbld
param := count=number
 | cpubind=cpu_list
 | cpuset=cpu_list
 | spintime=number
 | realtime={0|1}
 | nosend={0|1}
 | thread_prio={0..10}
 | cpubind_exclusive=cpu_list
 | cpuset_exclusive=cpu_list
```

The curly braces ({...}) surrounding the list of parameters are required, even if there is only one parameter in the list.

A param (parameter) specifies any or all of the following information:

- The number of threads of the given type (count).
- The set of CPUs to which the threads of the given type are to be nonexclusively bound. This is determined by either one of cpubind or cpuset). cpubind causes each thread to be bound (nonexclusively) to a CPU in the set; cpuset means that each thread is bound (nonexclusively) to the set of CPUs specified.

On Solaris, you can instead specify a set of CPUs to which the threads of the given type are to be bound exclusively. cpubind\_exclusive causes each thread to be bound exclusively to a CPU in the set; cpuset\_exclsuive means that each thread is bound exclusively to the set of CPUs specified.

Only one of cpubind, cpuset, cpubind\_exclusive, or cpuset\_exclusive can be provided in a single configuration.

• spintime determines the wait time in microseconds the thread spins before going to sleep.

The default value for spintime is the value of the [SchedulerSpinTimer](#page-19-1) data node configuration parameter.

spintime does not apply to I/O threads, watchdog, or offline index build threads, and so cannot be set for these thread types.

• realtime can be set to 0 or 1. If it is set to 1, the threads run with real-time priority. This also means that thread\_prio cannot be set.

The realtime parameter is set by default to the value of the [RealtimeScheduler](#page-18-0) data node configuration parameter.

realtime cannot be set for offline index build threads.

- By setting nosend to 1, you can prevent a main, ldm, rep, or tc thread from assisting the send threads. This parameter is 0 by default, and cannot be used with other types of threads.
- thread\_prio is a thread priority level that can be set from 0 to 10, with 10 representing the greatest priority. The default is 5. The precise effects of this parameter are platform-specific, and are described later in this section.

The thread priority level cannot be set for offline index build threads.

**thread\_prio settings and effects by platform.** The implementation of thread\_prio differs between Linux/FreeBSD, Solaris, and Windows. In the following list, we discuss its effects on each of these platforms in turn:

• Linux and FreeBSD: We map thread\_prio to a value to be supplied to the nice system call. Since a lower niceness value for a process indicates a higher process priority, increasing thread\_prio has the effect of lowering the nice value.

**Table 25.12 Mapping of thread\_prio to nice values on Linux and FreeBSD**

| thread_prio value | nice value |
|-------------------|------------|
| 0                 | 19         |
| 1                 | 16         |
| 2                 | 12         |
| 3                 | 8          |
| 4                 | 4          |
| 5                 | 0          |
| 6                 | -4         |
| 7                 | -8         |
| 8                 | -12        |
| 9                 | -16        |
| 10                | -20        |

Some operating systems may provide for a maximum process niceness level of 20, but this is not supported by all targeted versions; for this reason, we choose 19 as the maximum nice value that can be set.

• Solaris: Setting thread\_prio on Solaris sets the Solaris FX priority, with mappings as shown in the following table:

**Table 25.13 Mapping of thread\_prio to FX priority on Solaris**

| thread_prio value | Solaris FX priority |
|-------------------|---------------------|
| 0                 | 15                  |
| 1                 | 20                  |
| 2                 | 25                  |
| 3                 | 30                  |
| 4                 | 35                  |
| 5                 | 40                  |
| 6                 | 45                  |
| 7                 | 50                  |
| 8                 | 55                  |

| thread_prio value | Solaris FX priority |
|-------------------|---------------------|
| 9                 | 59                  |
| 10                | 60                  |

A thread\_prio setting of 9 is mapped on Solaris to the special FX priority value 59, which means that the operating system also attempts to force the thread to run alone on its own CPU core.

• Windows: We map thread\_prio to a Windows thread priority value passed to the Windows API SetThreadPriority() function. This mapping is shown in the following table:

**Table 25.14 Mapping of thread\_prio to Windows thread priority**

| thread_prio value | Windows thread priority      |
|-------------------|------------------------------|
| 0 - 1             | THREAD_PRIORITY_LOWEST       |
| 2 - 3             | THREAD_PRIORITY_BELOW_NORMAL |
| 4 - 5             | THREAD_PRIORITY_NORMAL       |
| 6 - 7             | THREAD_PRIORITY_ABOVE_NORMAL |
| 8 - 10            | THREAD_PRIORITY_HIGHEST      |

The type attribute represents an NDB thread type. The thread types supported, and the range of permitted count values for each, are provided in the following list:

• ldm: Local query handler ([DBLQH](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dblqh.md) kernel block) that handles data. The more LDM threads that are used, the more highly partitioned the data becomes.

When [ClassicFragmentation](#page-21-1) is set to 0, the number of partitions is independent of the number of LDM threads, and depends on the value of [PartitionsPerNode](#page-27-1) instead.) Each LDM thread maintains its own sets of data and index partitions, as well as its own redo log. ldm can be set to any value in the range 0 to 332 inclusive. When setting it to 0, main, rep, and tc must also be 0, and recv must also be set to 1; doing this causes [ndbmtd](#page-148-0) to emulate [ndbd](#page-134-0).

Each LDM thread is normally grouped with 1 query thread to form an LDM group. A set of 4 to 8 LDM groups is grouped into a round robin groups. Each LDM thread can be assisted in execution by any query or threads in the same round robin group. NDB attempts to form round robin groups such that all threads in each round robin group are locked to CPUs that are attached to the same L3 cache, within the limits of the range stated for a round robin group's size.

Changing the number of LDM threads normally requires a system restart to be effective and safe for cluster operations; this requirement is relaxed in certain cases, as explained later in this section. This is also true when this is done using [MaxNoOfExecutionThreads](#page-22-0).

Adding large tablespaces (hundreds of gigabytes or more) for Disk Data tables when using more than the default number of LDMs may cause issues with resource and CPU usage if [DiskPageBufferMemory](#page-35-0) is not sufficiently large.

If ldm is not included in the ThreadConfig value string, one ldm thread is created.

• query: A query thread is tied to an LDM and together with it forms an LDM group; acts only on READ COMMITTED queries. The number of query threads must be set to 0, 1, 2, or 3 times the number of LDM threads. Query threads are not used, unless this is overridden by setting query to a nonzero value, or by enabling the [AutomaticThreadConfig](#page-21-0) parameter.

A query thread also acts as a recovery thread (see next item), although the reverse is not true.

Changing the number of query threads requires a node restart.

• recover: A recovery thread restores data from a fragment as part of an LCP.

Changing the number of recovery threads requires a node restart.

• tc: Transaction coordinator thread ([DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) kernel block) containing the state of an ongoing transaction. The maximum number of TC threads is 128.

Optimally, every new transaction can be assigned to a new TC thread. In most cases 1 TC thread per 2 LDM threads is sufficient to guarantee that this can happen. In cases where the number of writes is relatively small when compared to the number of reads, it is possible that only 1 TC thread per 4 LQH threads is required to maintain transaction states. Conversely, in applications that perform a great many updates, it may be necessary for the ratio of TC threads to LDM threads to approach 1 (for example, 3 TC threads to 4 LDM threads).

Setting tc to 0 causes TC handling to be done by the main thread. In most cases, this is effectively the same as setting it to 1.

Range: 0-64

• main: Data dictionary and transaction coordinator ([DBDIH](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbdih.md) and [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) kernel blocks), providing schema management. It is also possible to specify zero or two main threads.

Range: 0-2.

Setting main to 0 and rep to 1 causes the main blocks to be placed into the rep thread; the combined thread is shown in the ndbinfo.threads table as main\_rep. This is effectively the same as setting rep equal to 1 and main equal to 0.

It is also possible to set both main and rep to 0, in which case both threads are placed in the first recv thread; the resulting combined thread is named main\_rep\_recv in the threads table.

If main is omitted from the ThreadConfig value stringthis, one main thread is created.

• recv: Receive thread ([CMVMI](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-cmvmi.md) kernel block). Each receive thread handles one or more sockets for communicating with other nodes in an NDB Cluster, with one socket per node. NDB Cluster supports multiple receive threads; the maximum is 16 such threads.

Range: 1 - 64.

If recv is omitted from the ThreadConfig value string, one recv thread is created.

• send: Send thread ([CMVMI](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-cmvmi.md) kernel block). To increase throughput, it is possible to perform sends from one or more separate, dedicated threads (maximum 8).

Using an excessive number of send threads can have an adverse effect on scalability.

Previously, all threads handled their own sending directly; this can still be made to happen by setting the number of send threads to 0 (this also happens when [MaxNoOfExecutionThreads](#page-22-0) is set less than 10). While doing so can have an adverse impact on throughput, it can also in some cases provide decreased latency.

#### Range:

• 0 - 64

• rep: Replication thread ([SUMA](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-suma.md) kernel block). This thread can also be combined with the main thread (see range information).

Range: 0-1.

Setting rep to 0 and main to 1 causes the rep blocks to be placed into the main thread; the combined thread is shown in the ndbinfo.threads table as main\_rep. This is effectively the same as setting main equal to 1 and rep equal to 0.

It is also possible to set both main and rep to 0, in which case both threads are placed in the first recv thread; the resulting combined thread is named main\_rep\_recv in the threads table.

If rep is omitted from the ThreadConfig value string, one rep thread is created.

• io: File system and other miscellaneous operations. These are not demanding tasks, and are always handled as a group by a single, dedicated I/O thread.

Range: 1 only.

• watchdog: Parameters settings associated with this type are actually applied to several threads, each having a specific use. These threads include the SocketServer thread, which receives connection setups from other nodes; the SocketClient thread, which attempts to set up connections to other nodes; and the thread watchdog thread that checks that threads are progressing.

Range: 1 only.

• idxbld: Offline index build threads. Unlike the other thread types listed previously, which are permanent, these are temporary threads which are created and used only during node or system restarts, or when running ndb\_restore --rebuild-indexes. They may be bound to CPU sets which overlap with CPU sets bound to permanent thread types.

thread\_prio, realtime, and spintime values cannot be set for offline index build threads. In addition, count is ignored for this type of thread.

If idxbld is not specified, the default behavior is as follows:

- Offline index build threads are not bound if the I/O thread is also not bound, and these threads use any available cores.
- If the I/O thread is bound, then the offline index build threads are bound to the entire set of bound threads, due to the fact that there should be no other tasks for these threads to perform.

Range: 0 - 1.

Changing ThreadCOnfig normally requires a system initial restart, but this requirement can be relaxed under certain circumstances:

• If, following the change, the number of LDM threads remains the same as before, nothing more than a simple node restart (rolling restart, or N) is required to implement the change.

- Otherwise (that is, if the number of LDM threads changes), it is still possible to effect the change using a node initial restart (NI) provided the following two conditions are met:
  - a. Each LDM thread handles a maximum of 8 fragments, and
  - b. The total number of table fragments is an integer multiple of the number of LDM threads.

In any other case, a system initial restart is needed to change this parameter.

NDB can distinguish between thread types by both of the following criteria:

- Whether the thread is an execution thread. Threads of type main, ldm, query, recv, rep, tc, and send are execution threads; io, recover, watchdog, and idxbld threads are not considered execution threads.
- Whether the allocation of threads to a given task is permanent or temporary. Currently all thread types except idxbld are considered permanent; idxbld threads are regarded as temporary threads.

#### Simple examples:

```
# Example 1.
ThreadConfig=ldm={count=2,cpubind=1,2},main={cpubind=12},rep={cpubind=11}
# Example 2.
Threadconfig=main={cpubind=0},ldm={count=4,cpubind=1,2,5,6},io={cpubind=3}
```

It is usually desirable when configuring thread usage for a data node host to reserve one or more number of CPUs for operating system and other tasks. Thus, for a host machine with 24 CPUs, you might want to use 20 CPU threads (leaving 4 for other uses), with 8 LDM threads, 4 TC threads (half the number of LDM threads), 3 send threads, 3 receive threads, and 1 thread each for schema management, asynchronous replication, and I/O operations. (This is almost the same distribution of threads used when [MaxNoOfExecutionThreads](#page-22-0) is set equal to 20.) The following ThreadConfig setting performs these assignments, additionally binding all of these threads to specific CPUs:

```
ThreadConfig=ldm{count=8,cpubind=1,2,3,4,5,6,7,8},main={cpubind=9},io={cpubind=9}, \
rep={cpubind=10},tc{count=4,cpubind=11,12,13,14},recv={count=3,cpubind=15,16,17}, \
send{count=3,cpubind=18,19,20}
```

It should be possible in most cases to bind the main (schema management) thread and the I/O thread to the same CPU, as we have done in the example just shown.

The following example incorporates groups of CPUs defined using both cpuset and cpubind, as well as use of thread prioritization.

```
ThreadConfig=ldm={count=4,cpuset=0-3,thread_prio=8,spintime=200}, \
ldm={count=4,cpubind=4-7,thread_prio=8,spintime=200}, \
tc={count=4,cpuset=8-9,thread_prio=6},send={count=2,thread_prio=10,cpubind=10-11}, \
main={count=1,cpubind=10},rep={count=1,cpubind=11}
```

In this case we create two LDM groups; the first uses cpubind and the second uses cpuset. thread\_prio and spintime are set to the same values for each group. This means there are eight LDM threads in total. (You should ensure that [NoOfFragmentLogParts](#page-26-1) is also set to 8.) The four TC threads use only two CPUs; it is possible when using cpuset to specify fewer CPUs than threads in the group. (This is not true for cpubind.) The send threads use two threads using cpubind to bind these threads to CPUs 10 and 11. The main and rep threads can reuse these CPUs.

This example shows how ThreadConfig and NoOfFragmentLogParts might be set up for a 24-CPU host with hyperthreading, leaving CPUs 10, 11, 22, and 23 available for operating system functions and interrupts:

```
NoOfFragmentLogParts=10
ThreadConfig=ldm={count=10,cpubind=0-4,12-16,thread_prio=9,spintime=200}, \
tc={count=4,cpuset=6-7,18-19,thread_prio=8},send={count=1,cpuset=8}, \
recv={count=1,cpuset=20},main={count=1,cpuset=9,21},rep={count=1,cpuset=9,21}, \
io={count=1,cpuset=9,21,thread_prio=8},watchdog={count=1,cpuset=9,21,thread_prio=9}
```

The next few examples include settings for idxbld. The first two of these demonstrate how a CPU set defined for idxbld can overlap those specified for other (permanent) thread types, the first using cpuset and the second using cpubind:

```
ThreadConfig=main,ldm={count=4,cpuset=1-4},tc={count=4,cpuset=5,6,7}, \
io={cpubind=8},idxbld={cpuset=1-8}
ThreadConfig=main,ldm={count=1,cpubind=1},idxbld={count=1,cpubind=1}
```

The next example specifies a CPU for the I/O thread, but not for the index build threads:

```
ThreadConfig=main,ldm={count=4,cpuset=1-4},tc={count=4,cpuset=5,6,7}, \
io={cpubind=8}
```

Since the ThreadConfig setting just shown locks threads to eight cores numbered 1 through 8, it is equivalent to the setting shown here:

```
ThreadConfig=main,ldm={count=4,cpuset=1-4},tc={count=4,cpuset=5,6,7}, \
io={cpubind=8},idxbld={cpuset=1,2,3,4,5,6,7,8}
```

In order to take advantage of the enhanced stability that the use of ThreadConfig offers, it is necessary to insure that CPUs are isolated, and that they not subject to interrupts, or to being scheduled for other tasks by the operating system. On many Linux systems, you can do this by setting IRQBALANCE\_BANNED\_CPUS in /etc/sysconfig/irqbalance to 0xFFFFF0, and by using the isolcpus boot option in grub.conf. For specific information, see your operating system or platform documentation.

**Disk Data Configuration Parameters.** Configuration parameters affecting Disk Data behavior include the following:

<span id="page-34-0"></span>• [DiskPageBufferEntries](#page-34-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 64MB                                                                             |
| Range                 | 4MB - 16TB                                                                       |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This is the number of page entries (page references) to allocate. It is specified as a number of 32K pages in [DiskPageBufferMemory](#page-35-0). The default is sufficient for most cases but you may need to increase the value of this parameter if you encounter problems with very large transactions on Disk Data tables. Each page entry requires approximately 100 bytes.

## <span id="page-35-0"></span>• [DiskPageBufferMemory](#page-35-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 64M                                                                              |
| Range                 | 4M - 16T                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This determines the amount of space, in bytes, used for caching pages on disk, and is set in the [ndbd] or [ndbd default] section of the config.ini file.

If the value for DiskPageBufferMemory is set too low in conjunction with using more than the default number of LDM threads in [ThreadConfig](#page-27-0) (for example {ldm=6...}), problems can arise when trying to add a large (for example 500G) data file to a disk-based NDB table, wherein the process takes indefinitely long while occupying one of the CPU cores.

This is due to the fact that, as part of adding a data file to a tablespace, extent pages are locked into memory in an extra PGMAN worker thread, for quick metadata access. When adding a large file, this worker has insufficient memory for all of the data file metadata. In such cases, you should either increase DiskPageBufferMemory, or add smaller tablespace files. You may also need to adjust [DiskPageBufferEntries](#page-34-0).

You can query the ndbinfo.diskpagebuffer table to help determine whether the value for this parameter should be increased to minimize unnecessary disk seeks. See Section 25.6.15.31, "The ndbinfo diskpagebuffer Table", for more information.

#### <span id="page-35-1"></span>• [SharedGlobalMemory](#page-35-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 128M                                                                             |
| Range                 | 0 - 64T                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter determines the amount of memory that is used for log buffers, disk operations (such as page requests and wait queues), and metadata for tablespaces, log file groups, UNDO files, and data files. The shared global memory pool also provides memory used for satisfying the memory requirements of the UNDO\_BUFFER\_SIZE option used with CREATE LOGFILE GROUP and ALTER LOGFILE GROUP statements, including any default value implied for this options by the setting of the [InitialLogFileGroup](#page-38-0) data node configuration parameter. SharedGlobalMemory can be set in the [ndbd] or [ndbd default] section of the config.ini configuration file, and is measured in bytes.

The default value is 128M.

<span id="page-36-0"></span>• [DiskIOThreadPool](#page-36-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | threads                                                                          |
| Default               | 2                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter determines the number of unbound threads used for Disk Data file access. Before [DiskIOThreadPool](#page-36-0) was introduced, exactly one thread was spawned for each Disk Data file, which could lead to performance issues, particularly when using very large data files. With [DiskIOThreadPool](#page-36-0), you can—for example—access a single large data file using several threads working in parallel.

This parameter applies to Disk Data I/O threads only.

The optimum value for this parameter depends on your hardware and configuration, and includes these factors:

• **Physical distribution of Disk Data files.** You can obtain better performance by placing data files, undo log files, and the data node file system on separate physical disks. If you do this with some or all of these sets of files, then you can (and should) set [DiskIOThreadPool](#page-36-0) higher to enable separate threads to handle the files on each disk.

You should also disable [DiskDataUsingSameDisk](#page-41-0) when using a separate disk or disks for Disk Data files; this increases the rate at which checkpoints of Disk Data tablespaces can be performed.

• **Disk performance and types.** The number of threads that can be accommodated for Disk Data file handling is also dependent on the speed and throughput of the disks. Faster disks and higher throughput allow for more disk I/O threads. Our test results indicate that solid-state disk drives can handle many more disk I/O threads than conventional disks, and thus higher values for [DiskIOThreadPool](#page-36-0).

Decreasing TimeBetweenGlobalCheckpoints is also recommended when using solid-state disk drives, in particular those using NVMe. See also [Disk Data latency parameters](#page-40-0).

The default value for this parameter is 2.

- <span id="page-36-1"></span>• **Disk Data file system parameters.** The parameters in the following list make it possible to place NDB Cluster Disk Data files in specific directories without the need for using symbolic links.
  - [FileSystemPathDD](#page-36-1)

| Version (or<br>later) | NDB 8.4.0      |
|-----------------------|----------------|
| Type or units         | filename       |
| Default               | FileSystemPath |
| Range                 |                |

| Restart Type | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial. |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
|              | (NDB 8.4.0)                                                                                                                             |

If this parameter is specified, then NDB Cluster Disk Data data files and undo log files are placed in the indicated directory. This can be overridden for data files, undo log files, or both, by specifying values for [FileSystemPathDataFiles](#page-37-0), [FileSystemPathUndoFiles](#page-38-1), or both, as explained for these parameters. It can also be overridden for data files by specifying a path in the ADD DATAFILE clause of a CREATE TABLESPACE or ALTER TABLESPACE statement, and for undo log files by specifying a path in the ADD UNDOFILE clause of a CREATE LOGFILE GROUP or ALTER LOGFILE GROUP statement. If [FileSystemPathDD](#page-36-1) is not specified, then FileSystemPath is used.

If a [FileSystemPathDD](#page-36-1) directory is specified for a given data node (including the case where the parameter is specified in the [ndbd default] section of the config.ini file), then starting that data node with --initial causes all files in the directory to be deleted.

#### <span id="page-37-0"></span>• [FileSystemPathDataFiles](#page-37-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |  |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| Type or units         | filename                                                                                                                                               |  |
| Default               | FileSystemPathDD                                                                                                                                       |  |
| Range                 |                                                                                                                                                        |  |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |  |

If this parameter is specified, then NDB Cluster Disk Data data files are placed in the indicated directory. This overrides any value set for [FileSystemPathDD](#page-36-1). This parameter can be overridden for a given data file by specifying a path in the ADD DATAFILE clause of a CREATE TABLESPACE or ALTER TABLESPACE statement used to create that data file. If [FileSystemPathDataFiles](#page-37-0) is not specified, then [FileSystemPathDD](#page-36-1) is used (or FileSystemPath, if [FileSystemPathDD](#page-36-1) has also not been set).

If a [FileSystemPathDataFiles](#page-37-0) directory is specified for a given data node (including the case where the parameter is specified in the [ndbd default] section of the config.ini file), then starting that data node with --initial causes all files in the directory to be deleted.

<span id="page-38-1"></span>• [FileSystemPathUndoFiles](#page-38-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |  |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| Type or units         | filename                                                                                                                                               |  |
| Default               | FileSystemPathDD                                                                                                                                       |  |
| Range                 |                                                                                                                                                        |  |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |  |

If this parameter is specified, then NDB Cluster Disk Data undo log files are placed in the indicated directory. This overrides any value set for [FileSystemPathDD](#page-36-1). This parameter can be overridden for a given data file by specifying a path in the ADD UNDO clause of a CREATE LOGFILE GROUP or ALTER LOGFILE GROUP statement used to create that data file. If [FileSystemPathUndoFiles](#page-38-1) is not specified, then [FileSystemPathDD](#page-36-1) is used (or FileSystemPath, if [FileSystemPathDD](#page-36-1) has also not been set).

If a [FileSystemPathUndoFiles](#page-38-1) directory is specified for a given data node (including the case where the parameter is specified in the [ndbd default] section of the config.ini file), then starting that data node with --initial causes all files in the directory to be deleted.

For more information, see Section 25.6.11.1, "NDB Cluster Disk Data Objects".

- <span id="page-38-0"></span>• **Disk Data object creation parameters.** The next two parameters enable you—when starting the cluster for the first time—to cause a Disk Data log file group, tablespace, or both, to be created without the use of SQL statements.
  - [InitialLogFileGroup](#page-38-0)

| Version (or<br>later) | NDB 8.4.0                                                                      |
|-----------------------|--------------------------------------------------------------------------------|
| Type or units         | string                                                                         |
| Default               | [see<br>documentation]                                                         |
| Range                 |                                                                                |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the |

```
cluster. (NDB
8.4.0)
```

This parameter can be used to specify a log file group that is created when performing an initial start of the cluster. [InitialLogFileGroup](#page-38-0) is specified as shown here:

```
InitialLogFileGroup = [name=name;] [undo_buffer_size=size;] file-specification-list
file-specification-list:
 file-specification[; file-specification[; ...]]
file-specification:
 filename:size
```

The name of the log file group is optional and defaults to DEFAULT-LG. The undo\_buffer\_size is also optional; if omitted, it defaults to 64M. Each file-specification corresponds to an undo log file, and at least one must be specified in the file-specification-list. Undo log files are placed according to any values that have been set for FileSystemPath, [FileSystemPathDD](#page-36-1), and [FileSystemPathUndoFiles](#page-38-1), just as if they had been created as the result of a CREATE LOGFILE GROUP or ALTER LOGFILE GROUP statement.

#### Consider the following:

```
InitialLogFileGroup = name=LG1; undo_buffer_size=128M; undo1.log:250M; undo2.log:150M
```

This is equivalent to the following SQL statements:

```
CREATE LOGFILE GROUP LG1
 ADD UNDOFILE 'undo1.log'
 INITIAL_SIZE 250M
 UNDO_BUFFER_SIZE 128M
 ENGINE NDBCLUSTER;
ALTER LOGFILE GROUP LG1
 ADD UNDOFILE 'undo2.log'
 INITIAL_SIZE 150M
 ENGINE NDBCLUSTER;
```

This logfile group is created when the data nodes are started with --initial.

Resources for the initial log file group are added to the global memory pool along with those indicated by the value of [SharedGlobalMemory](#page-35-1).

This parameter, if used, should always be set in the [ndbd default] section of the config.ini file. The behavior of an NDB Cluster when different values are set on different data nodes is not defined.

<span id="page-39-0"></span>• [InitialTablespace](#page-39-0)

| Version (or<br>later) | NDB 8.4.0                                                                      |
|-----------------------|--------------------------------------------------------------------------------|
| Type or units         | string                                                                         |
| Default               | [see<br>documentation]                                                         |
| Range                 |                                                                                |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the |

```
cluster. (NDB
8.4.0)
```

This parameter can be used to specify an NDB Cluster Disk Data tablespace that is created when performing an initial start of the cluster. [InitialTablespace](#page-39-0) is specified as shown here:

```
InitialTablespace = [name=name;] [extent_size=size;] file-specification-list
```

The name of the tablespace is optional and defaults to DEFAULT-TS. The extent\_size is also optional; it defaults to 1M. The file-specification-list uses the same syntax as shown with the [InitialLogfileGroup](#page-38-0) parameter, the only difference being that each file-specification used with [InitialTablespace](#page-39-0) corresponds to a data file. At least one must be specified in the file-specification-list. Data files are placed according to any values that have been set for FileSystemPath, [FileSystemPathDD](#page-36-1), and [FileSystemPathDataFiles](#page-37-0), just as if they had been created as the result of a CREATE TABLESPACE or ALTER TABLESPACE statement.

For example, consider the following line specifying [InitialTablespace](#page-39-0) in the [ndbd default] section of the config.ini file (as with [InitialLogfileGroup](#page-38-0), this parameter should always be set in the [ndbd default] section, as the behavior of an NDB Cluster when different values are set on different data nodes is not defined):

```
InitialTablespace = name=TS1; extent_size=8M; data1.dat:2G; data2.dat:4G
```

This is equivalent to the following SQL statements:

```
CREATE TABLESPACE TS1
 ADD DATAFILE 'data1.dat'
 EXTENT_SIZE 8M
 INITIAL_SIZE 2G
 ENGINE NDBCLUSTER;
ALTER TABLESPACE TS1
 ADD DATAFILE 'data2.dat'
 INITIAL_SIZE 4G
 ENGINE NDBCLUSTER;
```

This tablespace is created when the data nodes are started with --initial, and can be used whenever creating NDB Cluster Disk Data tables thereafter.

- <span id="page-40-1"></span><span id="page-40-0"></span>• **Disk Data latency parameters.** The two parameters listed here can be used to improve handling of latency issues with NDB Cluster Disk Data tables.
  - [MaxDiskDataLatency](#page-40-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | ms                                                                               |
| Default               | 0                                                                                |
| Range                 | 0 - 8000                                                                         |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter controls the maximum allowed mean latency for disk access (maximum 8000 milliseconds). When this limit is reached, NDB begins to abort transactions in order to decrease pressure on the Disk Data I/O subsystem. Use 0 to disable the latency check.

#### <span id="page-41-0"></span>• [DiskDataUsingSameDisk](#page-41-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | true                                                                             |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Set this parameter to false if your Disk Data tablespaces use one or more separate disks. Doing so allows checkpoints to tablespaces to be executed at a higher rate than normally used for when disks are shared.

When DiskDataUsingSameDisk is true, NDB decreases the rate of Disk Data checkpointing whenever an in-memory checkpoint is in progress to help ensure that disk load remains constant.

**Disk Data and GCP Stop errors.** Errors encountered when using Disk Data tables such as Node nodeid killed this node because GCP stop was detected (error 2303) are often referred to as "GCP stop errors". Such errors occur when the redo log is not flushed to disk quickly enough; this is usually due to slow disks and insufficient disk throughput.

You can help prevent these errors from occurring by using faster disks, and by placing Disk Data files on a separate disk from the data node file system. Reducing the value of TimeBetweenGlobalCheckpoints tends to decrease the amount of data to be written for each global checkpoint, and so may provide some protection against redo log buffer overflows when trying to write a global checkpoint; however, reducing this value also permits less time in which to write the GCP, so this must be done with caution.

In addition to the considerations given for [DiskPageBufferMemory](#page-35-0) as explained previously, it is also very important that the [DiskIOThreadPool](#page-36-0) configuration parameter be set correctly; having [DiskIOThreadPool](#page-36-0) set too high is very likely to cause GCP stop errors (Bug #37227).

GCP stops can be caused by save or commit timeouts; the TimeBetweenEpochsTimeout data node configuration parameter determines the timeout for commits. However, it is possible to disable both types of timeouts by setting this parameter to 0.

**Parameters for configuring send buffer memory allocation.** Send buffer memory is allocated dynamically from a memory pool shared between all transporters, which means that the size of the send buffer can be adjusted as necessary. (Previously, the NDB kernel used a fixed-size send buffer for every node in the cluster, which was allocated when the node started and could not be changed while the node was running.) The [TotalSendBufferMemory](#page-41-1) and [OverLoadLimit](#page-117-0) data node configuration parameters permit the setting of limits on this memory allocation. For more information about the use of these parameters (as well as [SendBufferMemory](#page-119-0)), see [Section 25.4.3.14,](#page-133-0) ["Configuring NDB Cluster Send Buffer Parameters"](#page-133-0).

#### <span id="page-41-2"></span>• [ExtraSendBufferMemory](#page-41-2)

This parameter specifies the amount of transporter send buffer memory to allocate in addition to any set using [TotalSendBufferMemory](#page-41-1), [SendBufferMemory](#page-119-0), or both.

#### <span id="page-41-1"></span>• [TotalSendBufferMemory](#page-41-1)

This parameter is used to determine the total amount of memory to allocate on this node for shared send buffer memory among all configured transporters.

If this parameter is set, its minimum permitted value is 256KB; 0 indicates that the parameter has not been set. For more detailed information, see [Section 25.4.3.14, "Configuring NDB Cluster Send](#page-133-0) [Buffer Parameters"](#page-133-0).

See also Section 25.6.7, "Adding NDB Cluster Data Nodes Online".

**Redo log over-commit handling.** It is possible to control a data node's handling of operations when too much time is taken flushing redo logs to disk. This occurs when a given redo log flush takes longer than [RedoOverCommitLimit](#page-42-0) seconds, more than [RedoOverCommitCounter](#page-42-1) times, causing any pending transactions to be aborted. When this happens, the API node that sent the transaction can handle the operations that should have been committed either by queuing the operations and re-trying them, or by aborting them, as determined by [DefaultOperationRedoProblemAction](#page-54-0). The data node configuration parameters for setting the timeout and number of times it may be exceeded before the API node takes this action are described in the following list:

## <span id="page-42-1"></span>• [RedoOverCommitCounter](#page-42-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | numeric                                                                          |
| Default               | 3                                                                                |
| Range                 | 1 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

When [RedoOverCommitLimit](#page-42-0) is exceeded when trying to write a given redo log to disk this many times or more, any transactions that were not committed as a result are aborted, and an API node where any of these transactions originated handles the operations making up those transactions according to its value for [DefaultOperationRedoProblemAction](#page-54-0) (by either queuing the operations to be re-tried, or aborting them).

#### <span id="page-42-0"></span>• [RedoOverCommitLimit](#page-42-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | seconds                                                                          |
| Default               | 20                                                                               |
| Range                 | 1 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter sets an upper limit in seconds for trying to write a given redo log to disk before timing out. The number of times the data node tries to flush this redo log, but takes longer than RedoOverCommitLimit, is kept and compared with [RedoOverCommitCounter](#page-42-1), and when flushing takes too long more times than the value of that parameter, any transactions that were not committed as a result of the flush timeout are aborted. When this occurs, the API node where any of these transactions originated handles the operations making up those transactions according to its

[DefaultOperationRedoProblemAction](#page-54-0) setting (it either queues the operations to be re-tried, or aborts them).

**Controlling restart attempts.** It is possible to exercise finely-grained control over restart attempts by data nodes when they fail to start using the [MaxStartFailRetries](#page-43-0) and [StartFailRetryDelay](#page-43-1) data node configuration parameters.

[MaxStartFailRetries](#page-43-0) limits the total number of retries made before giving up on starting the data node, [StartFailRetryDelay](#page-43-1) sets the number of seconds between retry attempts. These parameters are listed here:

#### <span id="page-43-1"></span>• [StartFailRetryDelay](#page-43-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Use this parameter to set the number of seconds between restart attempts by the data node in the event on failure on startup. The default is 0 (no delay).

Both this parameter and [MaxStartFailRetries](#page-43-0) are ignored unless StopOnError is equal to 0.

#### <span id="page-43-0"></span>• [MaxStartFailRetries](#page-43-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                         |
| Default               | 3                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Use this parameter to limit the number restart attempts made by the data node in the event that it fails on startup. The default is 3 attempts.

Both this parameter and [StartFailRetryDelay](#page-43-1) are ignored unless StopOnError is equal to 0.

**NDB index statistics parameters.** The parameters in the following list relate to NDB index statistics generation.

## <span id="page-43-2"></span>• [IndexStatAutoCreate](#page-43-2)

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | integer                                                                          |
|---------------|----------------------------------------------------------------------------------|
| Default       | 1                                                                                |
| Range         | 0, 1                                                                             |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enable (set equal to 1) or disable (set equal to 0) automatic statistics collection when indexes are created.

#### <span id="page-44-0"></span>• [IndexStatAutoUpdate](#page-44-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 1                                                                                |
| Range                 | 0, 1                                                                             |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Enable (set equal to 1) or disable (set equal to 0) monitoring of indexes for changes, and trigger automatic statistics updates when these are detected. The degree of change needed to trigger the updates are determined by the settings for the [IndexStatTriggerPct](#page-45-0) and [IndexStatTriggerScale](#page-46-0) options.

## <span id="page-44-1"></span>• [IndexStatSaveSize](#page-44-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Type or units         | bytes                                                                                                                       |
| Default               | 32768                                                                                                                       |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                                                              |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with |

[--initial](#page-137-0). (NDB 8.4.0)

Maximum space in bytes allowed for the saved statistics of any given index in the NDB system tables and in the mysqld memory cache.

At least one sample is always produced, regardless of any size limit. This size is scaled by [IndexStatSaveScale](#page-45-1).

The size specified by [IndexStatSaveSize](#page-44-1) is scaled by the value of IndexStatTriggerPct for a large index, times 0.01. This is further multiplied by the logarithm to the base 2 of the index size. Setting IndexStatTriggerPct equal to 0 disables the scaling effect.

#### <span id="page-45-1"></span>• [IndexStatSaveScale](#page-45-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | percentage                                                                                                                                             |
| Default               | 100                                                                                                                                                    |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                                                                                         |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

The size specified by [IndexStatSaveSize](#page-44-1) is scaled by the value of IndexStatTriggerPct for a large index, times 0.01. This is further multiplied by the logarithm to the base 2 of the index size. Setting IndexStatTriggerPct equal to 0 disables the scaling effect.

#### <span id="page-45-0"></span>• [IndexStatTriggerPct](#page-45-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Type or units         | percentage                                                                                                                  |
| Default               | 100                                                                                                                         |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                                                              |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with |

[--initial](#page-137-0). (NDB 8.4.0)

Percentage change in updates that triggers an index statistics update. The value is scaled by [IndexStatTriggerScale](#page-46-0). You can disable this trigger altogether by setting IndexStatTriggerPct to 0.

<span id="page-46-0"></span>• [IndexStatTriggerScale](#page-46-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | percentage                                                                                                                                             |
| Default               | 100                                                                                                                                                    |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                                                                                         |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

Scale [IndexStatTriggerPct](#page-45-0) by this amount times 0.01 for a large index. A value of 0 disables scaling.

<span id="page-46-1"></span>• [IndexStatUpdateDelay](#page-46-1)

| Version (or<br>later) | NDB 8.4.0                                                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | seconds                                                                                                                                                |
| Default               | 60                                                                                                                                                     |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                                                                                         |
| Restart Type          | Initial Node<br>Restart:<br>Requires a<br>rolling restart<br>of the cluster;<br>each data<br>node must be<br>restarted with<br>initial.<br>(NDB 8.4.0) |

Minimum delay in seconds between automatic index statistics updates for a given index. Setting this variable to 0 disables any delay. The default is 60 seconds.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 25.15 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 25.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |

## <span id="page-47-0"></span>**25.4.3.7 Defining SQL and Other API Nodes in an NDB Cluster**

The [mysqld] and [api] sections in the config.ini file define the behavior of the MySQL servers (SQL nodes) and other applications (API nodes) used to access cluster data. None of the parameters shown is required. If no computer or host name is provided, any host can use this SQL or API node.

Generally speaking, a [mysqld] section is used to indicate a MySQL server providing an SQL interface to the cluster, and an [api] section is used for applications other than mysqld processes accessing cluster data, but the two designations are actually synonymous; you can, for instance, list parameters for a MySQL server acting as an SQL node in an [api] section.

![](_page_47_Picture_6.jpeg)

#### **Note**

For a discussion of MySQL server options for NDB Cluster, see [MySQL Server](#page-59-0) [Options for NDB Cluster](#page-59-0). For information about MySQL server system variables relating to NDB Cluster, see [NDB Cluster System Variables](#page-72-0).

#### • Id

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                                                                                          |
| Default               | []                                                                                                                                                                                                                |
| Range                 | 1 - 255                                                                                                                                                                                                           |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting<br>the cluster.<br>(NDB 8.4.0) |

The Id is an integer value used to identify the node in all cluster internal messages. The permitted range of values is 1 to 255 inclusive. This value must be unique for each node in the cluster, regardless of the type of node.

![](_page_48_Picture_1.jpeg)

#### **Note**

Data node IDs must be less than 145. If you plan to deploy a large number of data nodes, it is a good idea to limit the node IDs for API nodes (and management nodes) to values greater than 144.

[NodeId](#page-48-0) is the preferred parameter name to use when identifying API nodes. (Id continues to be supported for backward compatibility, but is now deprecated and generates a warning when used. It is also subject to future removal.)

#### • ConnectionMap

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | string                                                                           |
| Default               | []                                                                               |
| Range                 |                                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Specifies which data nodes to connect.

#### <span id="page-48-0"></span>• NodeId

| Version (or<br>later) | NDB 8.4.0                                                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Type or units         | unsigned                                                                                                                                                                           |
| Default               | []                                                                                                                                                                                 |
| Range                 | 1 - 255                                                                                                                                                                            |
| Restart Type          | Initial System<br>Restart:<br>Requires a<br>complete<br>shutdown of the<br>cluster, wiping<br>and restoring<br>the cluster file<br>system from a<br>backup, and<br>then restarting |

the cluster. (NDB 8.4.0)

The NodeId is an integer value used to identify the node in all cluster internal messages. The permitted range of values is 1 to 255 inclusive. This value must be unique for each node in the cluster, regardless of the type of node.

![](_page_49_Picture_3.jpeg)

#### **Note**

Data node IDs must be less than 145. If you plan to deploy a large number of data nodes, it is a good idea to limit the node IDs for API nodes (and management nodes) to values greater than 144.

[NodeId](#page-48-0) is the preferred parameter name to use when identifying management nodes. An alias, Id, was used for this purpose in very old versions of NDB Cluster, and continues to be supported for backward compatibility; it is now deprecated and generates a warning when used, and is subject to removal in a future release of NDB Cluster.

#### • ExecuteOnComputer

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | name                                                                                                      |
| Default               | []                                                                                                        |
| Range                 |                                                                                                           |
| Deprecated            | Yes (in NDB<br>7.5)                                                                                       |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

This refers to the Id set for one of the computers (hosts) defined in a [computer] section of the configuration file.

![](_page_49_Picture_10.jpeg)

•

#### **Important**

This parameter is deprecated, and is subject to removal in a future release. Use the [HostName](#page-49-0) parameter instead.

The node ID for this node can be given out only to connections that explicitly request it. A management server that requests "any" node ID cannot use this one. This parameter can be used when running multiple management servers on the same host, and [HostName](#page-49-0) is not sufficient for distinguishing among processes.

#### • HostName

<span id="page-49-0"></span>

|      | Version (or<br>later) | NDB 8.4.0  |
|------|-----------------------|------------|
|      | Type or units         | name or IP |
| 4020 |                       | address    |

| Default      | []                                                                               |
|--------------|----------------------------------------------------------------------------------|
| Range        |                                                                                  |
| Restart Type | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Specifying this parameter defines the hostname of the computer on which the SQL node (API node) is to reside. Use HostName to specify a host name other than localhost.

If no HostName is specified in a given [mysql] or [api] section of the config.ini file, then an SQL or API node may connect using the corresponding "slot" from any host which can establish a network connection to the management server host machine. This differs from the default behavior for data nodes, where localhost is assumed for HostName unless otherwise specified.

#### <span id="page-50-0"></span>• [LocationDomainId](#page-50-0)

| Version (or<br>later) | NDB 8.4.0                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| Type or units         | integer                                                                                                   |
| Default               | 0                                                                                                         |
| Range                 | 0 - 16                                                                                                    |
| Restart Type          | System<br>Restart:<br>Requires a<br>complete<br>shutdown and<br>restart of the<br>cluster. (NDB<br>8.4.0) |

Assigns an SQL or other API node to a specific [availability domain](https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/regions.md) (also known as an availability zone) within a cloud. By informing NDB which nodes are in which availability domains, performance can be improved in a cloud environment in the following ways:

- If requested data is not found on the same node, reads can be directed to another node in the same availability domain.
- Communication between nodes in different availability domains are guaranteed to use NDB transporters' WAN support without any further manual intervention.
- The transporter's group number can be based on which availability domain is used, such that also SQL and other API nodes communicate with local data nodes in the same availability domain whenever possible.
- The arbitrator can be selected from an availability domain in which no data nodes are present, or, if no such availability domain can be found, from a third availability domain.

LocationDomainId takes an integer value between 0 and 16 inclusive, with 0 being the default; using 0 is the same as leaving the parameter unset.

• ArbitrationRank

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | 0-2                                                                              |
|---------------|----------------------------------------------------------------------------------|
| Default       | 0                                                                                |
| Range         | 0 - 2                                                                            |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter defines which nodes can act as arbitrators. Both management nodes and SQL nodes can be arbitrators. A value of 0 means that the given node is never used as an arbitrator, a value of 1 gives the node high priority as an arbitrator, and a value of 2 gives it low priority. A normal configuration uses the management server as arbitrator, setting its ArbitrationRank to 1 (the default for management nodes) and those for all SQL nodes to 0 (the default for SQL nodes).

By setting ArbitrationRank to 0 on all management and SQL nodes, you can disable arbitration completely. You can also control arbitration by overriding this parameter; to do so, set the [Arbitration](#page-3-1) parameter in the [ndbd default] section of the config.ini global configuration file.

#### • ArbitrationDelay

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | milliseconds                                                                     |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Setting this parameter to any other value than 0 (the default) means that responses by the arbitrator to arbitration requests are delayed by the stated number of milliseconds. It is usually not necessary to change this value.

#### <span id="page-51-0"></span>• [BatchByteSize](#page-51-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 16K                                                                              |
| Range                 | 1K - 1M                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

For queries that are translated into full table scans or range scans on indexes, it is important for best performance to fetch records in properly sized batches. It is possible to set the proper size both in

terms of number of records ([BatchSize](#page-52-0)) and in terms of bytes (BatchByteSize). The actual batch size is limited by both parameters.

The speed at which queries are performed can vary by more than 40% depending upon how this parameter is set.

This parameter is measured in bytes. The default value is 16K.

#### <span id="page-52-0"></span>• [BatchSize](#page-52-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | records                                                                          |
| Default               | 256                                                                              |
| Range                 | 1 - 992                                                                          |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is measured in number of records and is by default set to 256. The maximum size is 992.

#### <span id="page-52-1"></span>• [ExtraSendBufferMemory](#page-52-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter specifies the amount of transporter send buffer memory to allocate in addition to any that has been set using [TotalSendBufferMemory](#page-53-0), [SendBufferMemory](#page-119-0), or both.

#### <span id="page-52-2"></span>• [HeartbeatThreadPriority](#page-52-2)

| Version (or<br>later) | NDB 8.4.0                                      |
|-----------------------|------------------------------------------------|
| Type or units         | string                                         |
| Default               | []                                             |
| Range                 |                                                |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart |

```
of the cluster.
(NDB 8.4.0)
```

Use this parameter to set the scheduling policy and priority of heartbeat threads for management and API nodes. The syntax for setting this parameter is shown here:

```
HeartbeatThreadPriority = policy[, priority]
policy:
 {FIFO | RR}
```

When setting this parameter, you must specify a policy. This is one of FIFO (first in, first in) or RR (round robin). This followed optionally by the priority (an integer).

<span id="page-53-1"></span>• [MaxScanBatchSize](#page-53-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 256K                                                                             |
| Range                 | 32K - 16M                                                                        |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The batch size is the size of each batch sent from each data node. Most scans are performed in parallel to protect the MySQL Server from receiving too much data from many nodes in parallel; this parameter sets a limit to the total batch size over all nodes.

The default value of this parameter is set to 256KB. Its maximum size is 16MB.

<span id="page-53-0"></span>• TotalSendBufferMemory

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | bytes                                                                            |
| Default               | 0                                                                                |
| Range                 | 256K -<br>4294967039<br>(0xFFFFFEFF)                                             |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is used to determine the total amount of memory to allocate on this node for shared send buffer memory among all configured transporters.

If this parameter is set, its minimum permitted value is 256KB; 0 indicates that the parameter has not been set. For more detailed information, see [Section 25.4.3.14, "Configuring NDB Cluster Send](#page-133-0) [Buffer Parameters"](#page-133-0).

#### <span id="page-54-1"></span>• [AutoReconnect](#page-54-1)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter is false by default. This forces disconnected API nodes (including MySQL Servers acting as SQL nodes) to use a new connection to the cluster rather than attempting to re-use an existing one, as re-use of connections can cause problems when using dynamically-allocated node IDs. (Bug #45921)

![](_page_54_Picture_4.jpeg)

#### **Note**

This parameter can be overridden using the NDB API. For more information, see [Ndb\\_cluster\\_connection::set\\_auto\\_reconnect\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md#ndb-ndb-cluster-connection-set-auto-reconnect), and [Ndb\\_cluster\\_connection::get\\_auto\\_reconnect\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md#ndb-ndb-cluster-connection-get-auto-reconnect).

<span id="page-54-0"></span>• [DefaultOperationRedoProblemAction](#page-54-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | enumeration                                                                      |
| Default               | QUEUE                                                                            |
| Range                 | ABORT,<br>QUEUE                                                                  |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

This parameter (along with [RedoOverCommitLimit](#page-42-0) and [RedoOverCommitCounter](#page-42-1)) controls the data node's handling of operations when too much time is taken flushing redo logs to disk. This occurs when a given redo log flush takes longer than [RedoOverCommitLimit](#page-42-0) seconds, more than [RedoOverCommitCounter](#page-42-1) times, causing any pending transactions to be aborted.

When this happens, the node can respond in either of two ways, according to the value of DefaultOperationRedoProblemAction, listed here:

- ABORT: Any pending operations from aborted transactions are also aborted.
- QUEUE: Pending operations from transactions that were aborted are queued up to be re-tried. This the default. Pending operations are still aborted when the redo log runs out of space—that is, when **P\_TAIL\_PROBLEM** errors occur.
- <span id="page-54-2"></span>• [DefaultHashMapSize](#page-54-2)

| Version (or | NDB 8.4.0 |
|-------------|-----------|
| later)      |           |

| Type or units | buckets                                                                          |
|---------------|----------------------------------------------------------------------------------|
| Default       | 3840                                                                             |
| Range         | 0 - 3840                                                                         |
| Restart Type  | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

The size of the table hash maps used by NDB is configurable using this parameter. DefaultHashMapSize can take any of three possible values (0, 240, 3840). These values and their effects are described in the following table.

**Table 25.16 DefaultHashMapSize parameter values**

| Value | Description / Effect                                                                                                                                                              |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0     | Use the lowest value set, if any, for this<br>parameter among all data nodes and API nodes<br>in the cluster; if it is not set on any data or API<br>node, use the default value. |
| 240   | Old default hash map size                                                                                                                                                         |
| 3840  | Hash map size used by default in NDB 8.4                                                                                                                                          |

The original intended use for this parameter was to facilitate upgrades and downgrades to and from older NDB Cluster versions, in which the hash map size differed, due to the fact that this change was not otherwise backward compatible.

## <span id="page-55-0"></span>• [Wan](#page-55-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | boolean                                                                          |
| Default               | false                                                                            |
| Range                 | true, false                                                                      |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

Use WAN TCP setting as default.

#### • [ConnectBackoffMaxTime](#page-55-1)

<span id="page-55-1"></span>

|      | Version (or<br>later) | NDB 8.4.0                      |
|------|-----------------------|--------------------------------|
|      | Type or units         | integer                        |
|      | Default               | 0                              |
|      | Range                 | 0 - 4294967039<br>(0xFFFFFEFF) |
|      | Restart Type          | Node Restart:<br>Requires a    |
| 4026 |                       | rolling restart                |

of the cluster. (NDB 8.4.0)

In an NDB Cluster with many unstarted data nodes, the value of this parameter can be raised to circumvent connection attempts to data nodes which have not yet begun to function in the cluster, as well as moderate high traffic to management nodes. As long as the API node is not connected to any new data nodes, the value of the [StartConnectBackoffMaxTime](#page-56-0) parameter is applied; otherwise, ConnectBackoffMaxTime is used to determine the length of time in milliseconds to wait between connection attempts.

Time elapsed during node connection attempts is not taken into account when calculating elapsed time for this parameter. The timeout is applied with approximately 100 ms resolution, starting with a 100 ms delay; for each subsequent attempt, the length of this period is doubled until it reaches ConnectBackoffMaxTime milliseconds, up to a maximum of 100000 ms (100s).

Once the API node is connected to a data node and that node reports (in a heartbeat message) that it has connected to other data nodes, connection attempts to those data nodes are no longer affected by this parameter, and are made every 100 ms thereafter until connected. Once a data node has started, it can take up HeartbeatIntervalDbApi for the API node to be notified that this has occurred.

#### <span id="page-56-0"></span>• [StartConnectBackoffMaxTime](#page-56-0)

| Version (or<br>later) | NDB 8.4.0                                                                        |
|-----------------------|----------------------------------------------------------------------------------|
| Type or units         | integer                                                                          |
| Default               | 0                                                                                |
| Range                 | 0 - 4294967039<br>(0xFFFFFEFF)                                                   |
| Restart Type          | Node Restart:<br>Requires a<br>rolling restart<br>of the cluster.<br>(NDB 8.4.0) |

In an NDB Cluster with many unstarted data nodes, the value of this parameter can be raised to circumvent connection attempts to data nodes which have not yet begun to function in the cluster, as well as moderate high traffic to management nodes. As long as the API node is not connected to any new data nodes, the value of the StartConnectBackoffMaxTime parameter is applied; otherwise, [ConnectBackoffMaxTime](#page-55-1) is used to determine the length of time in milliseconds to wait between connection attempts.

Time elapsed during node connection attempts is not taken into account when calculating elapsed time for this parameter. The timeout is applied with approximately 100 ms resolution, starting with a 100 ms delay; for each subsequent attempt, the length of this period is doubled until it reaches StartConnectBackoffMaxTime milliseconds, up to a maximum of 100000 ms (100s).

Once the API node is connected to a data node and that node reports (in a heartbeat message) that it has connected to other data nodes, connection attempts to those data nodes are no longer affected by this parameter, and are made every 100 ms thereafter until connected. Once a data node has started, it can take up HeartbeatIntervalDbApi for the API node to be notified that this has occurred.

**API Node Debugging Parameters.** You can use the ApiVerbose configuration parameter to enable debugging output from a given API node. This parameter takes an integer value. 0 is the default, and disables such debugging; 1 enables debugging output to the cluster log; 2 adds [DBDICT](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbdict.md) debugging output as well. (Bug #20638450) See also [DUMP 1229](https://dev.mysql.com/doc/ndb-internals/en/dump-command-1229.md).

You can also obtain information from a MySQL server running as an NDB Cluster SQL node using SHOW STATUS in the mysql client, as shown here:

```
mysql> SHOW STATUS LIKE 'ndb%';
+-----------------------------+----------------+
| Variable_name | Value |
+-----------------------------+----------------+
| Ndb_cluster_node_id | 5 |
| Ndb_config_from_host | 198.51.100.112 |
| Ndb_config_from_port | 1186 |
| Ndb_number_of_storage_nodes | 4 |
+-----------------------------+----------------+
4 rows in set (0.02 sec)
```

For information about the status variables appearing in the output from this statement, see [NDB Cluster](#page-97-0) [Status Variables.](#page-97-0)

![](_page_57_Picture_4.jpeg)

### **Note**

To add new SQL or API nodes to the configuration of a running NDB Cluster, it is necessary to perform a rolling restart of all cluster nodes after adding new [mysqld] or [api] sections to the config.ini file (or files, if you are using more than one management server). This must be done before the new SQL or API nodes can connect to the cluster.

It is not necessary to perform any restart of the cluster if new SQL or API nodes can employ previously unused API slots in the cluster configuration to connect to the cluster.

**Restart types.** Information about the restart types used by the parameter descriptions in this section is shown in the following table:

**Table 25.17 NDB Cluster restart types**

| Symbol | Restart Type | Description                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| N      | Node         | The parameter can be updated<br>using a rolling restart (see<br>Section 25.6.5, "Performing<br>a Rolling Restart of an NDB<br>Cluster") |
| S      | System       | All cluster nodes must be<br>shut down completely, then<br>restarted, to effect a change in<br>this parameter                           |
| I      | Initial      | Data nodes must be restarted<br>using theinitial option                                                                                 |