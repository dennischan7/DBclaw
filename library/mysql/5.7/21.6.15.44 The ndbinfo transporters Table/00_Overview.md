---
source: MySQL 5.7 Reference
title: 00_Overview
---

This table contains information about NDB transporters.

The transporters table contains the following columns:

• node\_id

This data node's unique node ID in the cluster

• remote\_node\_id

The remote data node's node ID

• status

Status of the connection

• remote\_address

Name or IP address of the remote host

• bytes\_sent

Number of bytes sent using this connection

• bytes\_received

Number of bytes received using this connection

• connect\_count

Number of times connection established on this transporter

• overloaded

1 if this transporter is currently overloaded, otherwise 0

• overload\_count

Number of times this transporter has entered overload state since connecting

• slowdown

1 if this transporter is in slowdown state, otherwise 0

• slowdown\_count

Number of times this transporter has entered slowdown state since connecting

## **Notes**

For each running data node in the cluster, the transporters table displays a row showing the status of each of that node's connections with all nodes in the cluster, including itself. This information is shown in the table's status column, which can have any one of the following values: CONNECTING, CONNECTED, DISCONNECTING, or DISCONNECTED.

Connections to API and management nodes which are configured but not currently connected to the cluster are shown with status DISCONNECTED. Rows where the node\_id is that of a data node which is not currently connected are not shown in this table. (This is similar omission of disconnected nodes in the [ndbinfo.nodes](#page-64-0) table.

The remote\_address is the host name or address for the node whose ID is shown in the remote\_node\_id column. The bytes\_sent from this node and bytes\_received by this node are the numbers, respectively, of bytes sent and received by the node using this connection since it was established. For nodes whose status is CONNECTING or DISCONNECTED, these columns always display 0.

Assume you have a 5-node cluster consisting of 2 data nodes, 2 SQL nodes, and 1 management node, as shown in the output of the SHOW command in the ndb\_mgm client:

```
ndb_mgm> SHOW
Connected to Management Server at: localhost:1186
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @10.100.10.1 (5.7.44-ndb-7.6.36, Nodegroup: 0, *)
id=2 @10.100.10.2 (5.7.44-ndb-7.6.36, Nodegroup: 0)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @10.100.10.10 (5.7.44-ndb-7.6.36)
[mysqld(API)] 2 node(s)
id=20 @10.100.10.20 (5.7.44-ndb-7.6.36)
id=21 @10.100.10.21 (5.7.44-ndb-7.6.36)
```

There are 10 rows in the transporters table—5 for the first data node, and 5 for the second assuming that all data nodes are running, as shown here:

```
mysql> SELECT node_id, remote_node_id, status
 -> FROM ndbinfo.transporters;
+---------+----------------+---------------+
| node_id | remote_node_id | status |
+---------+----------------+---------------+
| 1 | 1 | DISCONNECTED |
| 1 | 2 | CONNECTED |
| 1 | 10 | CONNECTED |
```

```
| 1 | 20 | CONNECTED |
| 1 | 21 | CONNECTED |
| 2 | 1 | CONNECTED |
| 2 | 2 | DISCONNECTED |
| 2 | 10 | CONNECTED |
| 2 | 20 | CONNECTED |
| 2 | 21 | CONNECTED |
+---------+----------------+---------------+
10 rows in set (0.04 sec)
```

If you shut down one of the data nodes in this cluster using the command 2 STOP in the ndb\_mgm client, then repeat the previous query (again using the mysql client), this table now shows only 5 rows —1 row for each connection from the remaining management node to another node, including both itself and the data node that is currently offline—and displays CONNECTING for the status of each remaining connection to the data node that is currently offline, as shown here:

```
mysql> SELECT node_id, remote_node_id, status
 -> FROM ndbinfo.transporters;
+---------+----------------+---------------+
| node_id | remote_node_id | status |
+---------+----------------+---------------+
| 1 | 1 | DISCONNECTED |
| 1 | 2 | CONNECTING |
| 1 | 10 | CONNECTED |
| 1 | 20 | CONNECTED |
| 1 | 21 | CONNECTED |
+---------+----------------+---------------+
5 rows in set (0.02 sec)
```

The connect\_count, overloaded, overload\_count, slowdown, and slowdown\_count counters are reset on connection, and retain their values after the remote node disconnects. The bytes\_sent and bytes\_received counters are also reset on connection, and so retain their values following disconnection (until the next connection resets them).

The overload state referred to by the overloaded and overload\_count columns occurs when this transporter's send buffer contains more than OVerloadLimit bytes (default is 80% of SendBufferMemory, that is, 0.8 \* 2097152 = 1677721 bytes). When a given transporter is in a state of overload, any new transaction that tries to use this transporter fails with Error 1218 (Send Buffers overloaded in NDB kernel). This affects both scans and primary key operations.

The slowdown state referenced by the slowdown and slowdown\_count columns of this table occurs when the transporter's send buffer contains more than 60% of the overload limit (equal to 0.6 \* 2097152 = 1258291 bytes by default). In this state, any new scan using this transporter has its batch size reduced to minimize the load on the transporter.

Common causes of send buffer slowdown or overloading include the following:

- Data size, in particular the quantity of data stored in TEXT columns or BLOB columns (or both types of columns)
- Having a data node (ndbd or ndbmtd) on the same host as an SQL node that is engaged in binary logging
- Large number of rows per transaction or transaction batch
- Configuration issues such as insufficient SendBufferMemory
- Hardware issues such as insufficient RAM or poor network connectivity

See also Section 21.4.3.13, "Configuring NDB Cluster Send Buffer Parameters".

# <span id="page-90-0"></span>**21.6.16 INFORMATION\_SCHEMA Tables for NDB Cluster**

Two INFORMATION\_SCHEMA tables provide information that is of particular use when managing an NDB Cluster . The FILES table provides information about NDB Cluster Disk Data files. The

ndb\_transid\_mysql\_connection\_map table provides a mapping between transactions, transaction coordinators, and API nodes.

Additional statistical and other data about NDB Cluster transactions, operations, threads, blocks, and other aspects of performance can be obtained from the tables in the [ndbinfo](#page-21-0) database. For information about these tables, see [Section 21.6.15, "ndbinfo: The NDB Cluster Information Database"](#page-21-0).