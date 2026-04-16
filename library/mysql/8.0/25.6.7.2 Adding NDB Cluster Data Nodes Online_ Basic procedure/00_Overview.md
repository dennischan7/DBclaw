---
source: MySQL 8.0 Reference
title: 00_Overview
---

In this section, we list the basic steps required to add new data nodes to an NDB Cluster. This procedure applies whether you are using ndbd or ndbmtd binaries for the data node processes. For a more detailed example, see [Section 25.6.7.3, "Adding NDB Cluster Data Nodes Online: Detailed](#page-85-0) [Example"](#page-85-0).

Assuming that you already have a running NDB Cluster, adding data nodes online requires the following steps:

1. Edit the cluster configuration config.ini file, adding new [ndbd] sections corresponding to the nodes to be added. In the case where the cluster uses multiple management servers, these changes need to be made to all config.ini files used by the management servers.

You must be careful that node IDs for any new data nodes added in the config.ini file do not overlap node IDs used by existing nodes. In the event that you have API nodes using dynamically allocated node IDs and these IDs match node IDs that you want to use for new data nodes, it is possible to force any such API nodes to "migrate", as described later in this procedure.

2. Perform a rolling restart of all NDB Cluster management servers.

![](_page_84_Picture_12.jpeg)

### **Important**

All management servers must be restarted with the --reload or - initial option to force the reading of the new configuration.

3. Perform a rolling restart of all existing NDB Cluster data nodes. It is not necessary (or usually even desirable) to use --initial when restarting the existing data nodes.

If you are using API nodes with dynamically allocated IDs matching any node IDs that you wish to assign to new data nodes, you must restart all API nodes (including SQL nodes) before restarting any of the data nodes processes in this step. This causes any API nodes with node IDs that were previously not explicitly assigned to relinquish those node IDs and acquire new ones.

- 4. Perform a rolling restart of any SQL or API nodes connected to the NDB Cluster.
- 5. Start the new data nodes.

The new data nodes may be started in any order. They can also be started concurrently, as long as they are started after the rolling restarts of all existing data nodes have been completed, and before proceeding to the next step.

- 6. Execute one or more [CREATE NODEGROUP](#page-42-1) commands in the NDB Cluster management client to create the new node group or node groups to which the new data nodes belong.
- 7. Redistribute the cluster's data among all data nodes, including the new ones. Normally this is done by issuing an ALTER TABLE ... ALGORITHM=INPLACE, REORGANIZE PARTITION statement in the mysql client for each NDBCLUSTER table.

Exception: For tables created using the MAX\_ROWS option, this statement does not work; instead, use ALTER TABLE ... ALGORITHM=INPLACE MAX\_ROWS=... to reorganize such tables. You should also bear in mind that using MAX\_ROWS to set the number of partitions in this fashion is deprecated, and you should use PARTITION\_BALANCE instead; see Section 15.1.20.12, "Setting NDB Comment Options", for more information.

![](_page_85_Picture_4.jpeg)

### **Note**

This needs to be done only for tables already existing at the time the new node group is added. Data in tables created after the new node group is added is distributed automatically; however, data added to any given table tbl that existed before the new nodes were added is not distributed using the new nodes until that table has been reorganized.

8. ALTER TABLE ... REORGANIZE PARTITION ALGORITHM=INPLACE reorganizes partitions but does not reclaim the space freed on the "old" nodes. You can do this by issuing, for each NDBCLUSTER table, an OPTIMIZE TABLE statement in the mysql client.

This works for space used by variable-width columns of in-memory NDB tables. OPTIMIZE TABLE is not supported for fixed-width columns of in-memory tables; it is also not supported for Disk Data tables.

You can add all the nodes desired, then issue several [CREATE NODEGROUP](#page-42-1) commands in succession to add the new node groups to the cluster.

# <span id="page-85-0"></span>**25.6.7.3 Adding NDB Cluster Data Nodes Online: Detailed Example**

In this section we provide a detailed example illustrating how to add new NDB Cluster data nodes online, starting with an NDB Cluster having 2 data nodes in a single node group and concluding with a cluster having 4 data nodes in 2 node groups.

**Starting configuration.** For purposes of illustration, we assume a minimal configuration, and that the cluster uses a config.ini file containing only the following information:

```
[ndbd default]
DataMemory = 100M
IndexMemory = 100M
NoOfReplicas = 2
DataDir = /usr/local/mysql/var/mysql-cluster
[ndbd]
Id = 1
HostName = 198.51.100.1
[ndbd]
Id = 2
HostName = 198.51.100.2
[mgm]
HostName = 198.51.100.10
Id = 10
[api]
Id=20
HostName = 198.51.100.20
[api]
Id=21
```

HostName = 198.51.100.21

![](_page_86_Picture_2.jpeg)

#### **Note**

We have left a gap in the sequence between data node IDs and other nodes. This make it easier later to assign node IDs that are not already in use to data nodes which are newly added.

We also assume that you have already started the cluster using the appropriate command line or my.cnf options, and that running [SHOW](#page-45-1) in the management client produces output similar to what is shown here:

```
-- NDB Cluster -- Management Client --
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.0.44-ndb-8.0.44, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.0.44-ndb-8.0.44, Nodegroup: 0)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.0.44-ndb-8.0.44)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.0.44-ndb-8.0.44)
id=21 @198.51.100.21 (8.0.44-ndb-8.0.44)
```

Finally, we assume that the cluster contains a single NDBCLUSTER table created as shown here:

```
USE n;
CREATE TABLE ips (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 country_code CHAR(2) NOT NULL,
 type CHAR(4) NOT NULL,
 ip_address VARCHAR(15) NOT NULL,
 addresses BIGINT UNSIGNED DEFAULT NULL,
 date BIGINT UNSIGNED DEFAULT NULL
) ENGINE NDBCLUSTER;
```

The memory usage and related information shown later in this section was generated after inserting approximately 50000 rows into this table.

![](_page_86_Picture_10.jpeg)

#### **Note**

In this example, we show the single-threaded ndbd being used for the data node processes. You can also apply this example, if you are using the multithreaded ndbmtd by substituting ndbmtd for ndbd wherever it appears in the steps that follow.

**Step 1: Update configuration file.** Open the cluster global configuration file in a text editor and add [ndbd] sections corresponding to the 2 new data nodes. (We give these data nodes IDs 3 and 4, and assume that they are to be run on host machines at addresses 198.51.100.3 and 198.51.100.4, respectively.) After you have added the new sections, the contents of the config.ini file should look like what is shown here, where the additions to the file are shown in bold type:

```
[ndbd default]
DataMemory = 100M
IndexMemory = 100M
NoOfReplicas = 2
DataDir = /usr/local/mysql/var/mysql-cluster
[ndbd]
Id = 1
HostName = 198.51.100.1
```

```
[ndbd]
Id = 2
HostName = 198.51.100.2
[ndbd]
Id = 3
HostName = 198.51.100.3
[ndbd]
Id = 4
HostName = 198.51.100.4
[mgm]
HostName = 198.51.100.10
Id = 10
[api]
Id=20
HostName = 198.51.100.20
[api]
Id=21
HostName = 198.51.100.21
```

Once you have made the necessary changes, save the file.

**Step 2: Restart the management server.** Restarting the cluster management server requires that you issue separate commands to stop the management server and then to start it again, as follows:

1. Stop the management server using the management client [STOP](#page-47-0) command, as shown here:

```
ndb_mgm> 10 STOP
Node 10 has shut down.
Disconnecting to allow Management Server to shutdown
$>
```

2. Because shutting down the management server causes the management client to terminate, you must start the management server from the system shell. For simplicity, we assume that config.ini is in the same directory as the management server binary, but in practice, you must supply the correct path to the configuration file. You must also supply the --reload or --initial option so that the management server reads the new configuration from the file rather than its configuration cache. If your shell's current directory is also the same as the directory where the management server binary is located, then you can invoke the management server as shown here:

```
$> ndb_mgmd -f config.ini --reload
2008-12-08 17:29:23 [MgmSrvr] INFO -- NDB Cluster Management Server. 8.0.44-ndb-8.0.44
2008-12-08 17:29:23 [MgmSrvr] INFO -- Reading cluster configuration from 'config.ini'
```

If you check the output of [SHOW](#page-45-1) in the management client after restarting the ndb\_mgm process, you should now see something like this:

```
-- NDB Cluster -- Management Client --
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.0.44-ndb-8.0.44, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.0.44-ndb-8.0.44, Nodegroup: 0)
id=3 (not connected, accepting connect from 198.51.100.3)
id=4 (not connected, accepting connect from 198.51.100.4)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.0.44-ndb-8.0.44)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.0.44-ndb-8.0.44)
id=21 @198.51.100.21 (8.0.44-ndb-8.0.44)
```

**Step 3: Perform a rolling restart of the existing data nodes.** This step can be accomplished entirely within the cluster management client using the [RESTART](#page-45-0) command, as shown here:

```
ndb_mgm> 1 RESTART
Node 1: Node shutdown initiated
Node 1: Node shutdown completed, restarting, no start.
Node 1 is being restarted
ndb_mgm> Node 1: Start initiated (version 8.0.44)
Node 1: Started (version 8.0.44)
ndb_mgm> 2 RESTART
Node 2: Node shutdown initiated
Node 2: Node shutdown completed, restarting, no start.
Node 2 is being restarted
ndb_mgm> Node 2: Start initiated (version 8.0.44)
ndb_mgm> Node 2: Started (version 8.0.44)
```

![](_page_88_Picture_3.jpeg)

#### **Important**

After issuing each X RESTART command, wait until the management client reports Node X: Started (version ...) before proceeding any further.

You can verify that all existing data nodes were restarted using the updated configuration by checking the [ndbinfo.nodes](#page-186-0) table in the mysql client.

**Step 4: Perform a rolling restart of all cluster API nodes.** Shut down and restart each MySQL server acting as an SQL node in the cluster using mysqladmin shutdown followed by mysqld\_safe (or another startup script). This should be similar to what is shown here, where password is the MySQL root password for a given MySQL server instance:

```
$> mysqladmin -uroot -ppassword shutdown
081208 20:19:56 mysqld_safe mysqld from pid file
/usr/local/mysql/var/tonfisk.pid ended
$> mysqld_safe --ndbcluster --ndb-connectstring=198.51.100.10 &
081208 20:20:06 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
081208 20:20:06 mysqld_safe Starting mysqld daemon with databases
from /usr/local/mysql/var
```

Of course, the exact input and output depend on how and where MySQL is installed on the system, as well as which options you choose to start it (and whether or not some or all of these options are specified in a my.cnf file).

**Step 5: Perform an initial start of the new data nodes.** From a system shell on each of the hosts for the new data nodes, start the data nodes as shown here, using the --initial option:

```
$> ndbd -c 198.51.100.10 --initial
```

![](_page_88_Picture_12.jpeg)

### **Note**

Unlike the case with restarting the existing data nodes, you can start the new data nodes concurrently; you do not need to wait for one to finish starting before starting the other.

Wait until both of the new data nodes have started before proceeding with the next step. Once the new data nodes have started, you can see in the output of the management client [SHOW](#page-45-1) command that they do not yet belong to any node group (as indicated with bold type here):

```
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.0.44-ndb-8.0.44, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.0.44-ndb-8.0.44, Nodegroup: 0)
id=3 @198.51.100.3 (8.0.44-ndb-8.0.44, no nodegroup)
```

```
id=4 @198.51.100.4 (8.0.44-ndb-8.0.44, no nodegroup)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.0.44-ndb-8.0.44)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.0.44-ndb-8.0.44)
id=21 @198.51.100.21 (8.0.44-ndb-8.0.44)
```

**Step 6: Create a new node group.** You can do this by issuing a [CREATE NODEGROUP](#page-42-1) command in the cluster management client. This command takes as its argument a comma-separated list of the node IDs of the data nodes to be included in the new node group, as shown here:

```
ndb_mgm> CREATE NODEGROUP 3,4
Nodegroup 1 created
```

By issuing [SHOW](#page-45-1) again, you can verify that data nodes 3 and 4 have joined the new node group (again indicated in bold type):

```
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.0.44-ndb-8.0.44, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.0.44-ndb-8.0.44, Nodegroup: 0)
id=3 @198.51.100.3 (8.0.44-ndb-8.0.44, Nodegroup: 1)
id=4 @198.51.100.4 (8.0.44-ndb-8.0.44, Nodegroup: 1)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.0.44-ndb-8.0.44)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.0.44-ndb-8.0.44)
id=21 @198.51.100.21 (8.0.44-ndb-8.0.44)
```

**Step 7: Redistribute cluster data.** When a node group is created, existing data and indexes are not automatically distributed to the new node group's data nodes, as you can see by issuing the appropriate [REPORT](#page-44-5) command in the management client:

```
ndb_mgm> ALL REPORT MEMORY
Node 1: Data usage is 5%(177 32K pages of total 3200)
Node 1: Index usage is 0%(108 8K pages of total 12832)
Node 2: Data usage is 5%(177 32K pages of total 3200)
Node 2: Index usage is 0%(108 8K pages of total 12832)
Node 3: Data usage is 0%(0 32K pages of total 3200)
Node 3: Index usage is 0%(0 8K pages of total 12832)
Node 4: Data usage is 0%(0 32K pages of total 3200)
Node 4: Index usage is 0%(0 8K pages of total 12832)
```

By using ndb\_desc with the -p option, which causes the output to include partitioning information, you can see that the table still uses only 2 partitions (in the Per partition info section of the output, shown here in bold text):

```
$> ndb_desc -c 198.51.100.10 -d n ips -p
-- ips --
Version: 1
Fragment type: 9
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 6
Number of primary keys: 1
Length of frm data: 340
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
FragmentCount: 2
```

```
TableStatus: Retrieved
-- Attributes --
id Bigint PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY AUTO_INCR
country_code Char(2;latin1_swedish_ci) NOT NULL AT=FIXED ST=MEMORY
type Char(4;latin1_swedish_ci) NOT NULL AT=FIXED ST=MEMORY
ip_address Varchar(15;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY
addresses Bigunsigned NULL AT=FIXED ST=MEMORY
date Bigunsigned NULL AT=FIXED ST=MEMORY
-- Indexes --
PRIMARY KEY(id) - UniqueHashIndex
PRIMARY(id) - OrderedIndex
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory
0 26086 26086 1572864 557056
1 26329 26329 1605632 557056
```

You can cause the data to be redistributed among all of the data nodes by performing, for each NDB table, an ALTER TABLE ... ALGORITHM=INPLACE, REORGANIZE PARTITION statement in the mysql client.

![](_page_90_Picture_3.jpeg)

#### **Important**

ALTER TABLE ... ALGORITHM=INPLACE, REORGANIZE PARTITION does not work on tables that were created with the MAX\_ROWS option. Instead, use ALTER TABLE ... ALGORITHM=INPLACE, MAX\_ROWS=... to reorganize such tables.

Keep in mind that using MAX\_ROWS to set the number of partitions per table is deprecated, and you should use PARTITION\_BALANCE instead; see Section 15.1.20.12, "Setting NDB Comment Options", for more information.

After issuing the statement ALTER TABLE ips ALGORITHM=INPLACE, REORGANIZE PARTITION, you can see using ndb\_desc that the data for this table is now stored using 4 partitions, as shown here (with the relevant portions of the output in bold type):

```
$> ndb_desc -c 198.51.100.10 -d n ips -p
-- ips --
Version: 16777217
Fragment type: 9
K Value: 6
Min load factor: 78
Max load factor: 80
Temporary table: no
Number of attributes: 6
Number of primary keys: 1
Length of frm data: 341
Row Checksum: 1
Row GCI: 1
SingleUserMode: 0
ForceVarPart: 1
FragmentCount: 4
TableStatus: Retrieved
-- Attributes --
id Bigint PRIMARY KEY DISTRIBUTION KEY AT=FIXED ST=MEMORY AUTO_INCR
country_code Char(2;latin1_swedish_ci) NOT NULL AT=FIXED ST=MEMORY
type Char(4;latin1_swedish_ci) NOT NULL AT=FIXED ST=MEMORY
ip_address Varchar(15;latin1_swedish_ci) NOT NULL AT=SHORT_VAR ST=MEMORY
addresses Bigunsigned NULL AT=FIXED ST=MEMORY
date Bigunsigned NULL AT=FIXED ST=MEMORY
-- Indexes --
PRIMARY KEY(id) - UniqueHashIndex
PRIMARY(id) - OrderedIndex
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory
0 12981 52296 1572864 557056
```

| 1 | 13236 | 52515 | 1605632 | 557056 |  |
|---|-------|-------|---------|--------|--|
| 2 | 13105 | 13105 | 819200  | 294912 |  |
| 3 | 13093 | 13093 | 819200  | 294912 |  |

![](_page_91_Picture_2.jpeg)

#### **Note**

Normally, ALTER TABLE table\_name [ALGORITHM=INPLACE,] REORGANIZE PARTITION is used with a list of partition identifiers and a set of partition definitions to create a new partitioning scheme for a table that has already been explicitly partitioned. Its use here to redistribute data onto a new NDB Cluster node group is an exception in this regard; when used in this way, no other keywords or identifiers follow REORGANIZE PARTITION.

For more information, see Section 15.1.9, "ALTER TABLE Statement".

In addition, for each table, the ALTER TABLE statement should be followed by an OPTIMIZE TABLE to reclaim wasted space. You can obtain a list of all NDBCLUSTER tables using the following query against the Information Schema TABLES table:

```
SELECT TABLE_SCHEMA, TABLE_NAME
 FROM INFORMATION_SCHEMA.TABLES
 WHERE ENGINE = 'NDBCLUSTER';
```

![](_page_91_Picture_8.jpeg)

#### **Note**

The INFORMATION\_SCHEMA.TABLES.ENGINE value for an NDB Cluster table is always NDBCLUSTER, regardless of whether the CREATE TABLE statement used to create the table (or ALTER TABLE statement used to convert an existing table from a different storage engine) used NDB or NDBCLUSTER in its ENGINE option.

You can see after performing these statements in the output of [ALL REPORT MEMORY](#page-44-5) that the data and indexes are now redistributed between all cluster data nodes, as shown here:

```
ndb_mgm> ALL REPORT MEMORY
Node 1: Data usage is 5%(176 32K pages of total 3200)
Node 1: Index usage is 0%(76 8K pages of total 12832)
Node 2: Data usage is 5%(176 32K pages of total 3200)
Node 2: Index usage is 0%(76 8K pages of total 12832)
Node 3: Data usage is 2%(80 32K pages of total 3200)
Node 3: Index usage is 0%(51 8K pages of total 12832)
Node 4: Data usage is 2%(80 32K pages of total 3200)
Node 4: Index usage is 0%(50 8K pages of total 12832)
```

![](_page_91_Picture_13.jpeg)

### **Note**

Since only one DDL operation on NDBCLUSTER tables can be executed at a time, you must wait for each ALTER TABLE ... REORGANIZE PARTITION statement to finish before issuing the next one.

It is not necessary to issue ALTER TABLE ... REORGANIZE PARTITION statements for NDBCLUSTER tables created after the new data nodes have been added; data added to such tables is distributed among all data nodes automatically. However, in NDBCLUSTER tables that existed prior to the addition of the new nodes, neither existing nor new data is distributed using the new nodes until these tables have been reorganized using ALTER TABLE ... REORGANIZE PARTITION.

**Alternative procedure, without rolling restart.** It is possible to avoid the need for a rolling restart by configuring the extra data nodes, but not starting them, when first starting the cluster. We assume, as before, that you wish to start with two data nodes—nodes 1 and 2—in one node group and later to expand the cluster to four data nodes, by adding a second node group consisting of nodes 3 and 4:

```
[ndbd default]
DataMemory = 100M
IndexMemory = 100M
```

```
NoOfReplicas = 2
DataDir = /usr/local/mysql/var/mysql-cluster
[ndbd]
Id = 1
HostName = 198.51.100.1
[ndbd]
Id = 2
HostName = 198.51.100.2
[ndbd]
Id = 3
HostName = 198.51.100.3
Nodegroup = 65536
[ndbd]
Id = 4
HostName = 198.51.100.4
Nodegroup = 65536
[mgm]
HostName = 198.51.100.10
Id = 10
[api]
Id=20
HostName = 198.51.100.20
[api]
Id=21
HostName = 198.51.100.21
```

The data nodes to be brought online at a later time (nodes 3 and 4) can be configured with NodeGroup = 65536, in which case nodes 1 and 2 can each be started as shown here:

```
$> ndbd -c 198.51.100.10 --initial
```

The data nodes configured with NodeGroup = 65536 are treated by the management server as though you had started nodes 1 and 2 using --nowait-nodes=3,4 after waiting for a period of time determined by the setting for the StartNoNodeGroupTimeout data node configuration parameter. By default, this is 15 seconds (15000 milliseconds).

![](_page_92_Picture_5.jpeg)

### **Note**

StartNoNodegroupTimeout must be the same for all data nodes in the cluster; for this reason, you should always set it in the [ndbd default] section of the config.ini file, rather than for individual data nodes.

When you are ready to add the second node group, you need only perform the following additional steps:

1. Start data nodes 3 and 4, invoking the data node process once for each new node:

```
$> ndbd -c 198.51.100.10 --initial
```

2. Issue the appropriate [CREATE NODEGROUP](#page-42-1) command in the management client:

```
ndb_mgm> CREATE NODEGROUP 3,4
```

3. In the mysql client, issue ALTER TABLE ... REORGANIZE PARTITION and OPTIMIZE TABLE statements for each existing NDBCLUSTER table. (As noted elsewhere in this section, existing NDB Cluster tables cannot use the new nodes for data distribution until this has been done.)

# <span id="page-92-0"></span>**25.6.8 Online Backup of NDB Cluster**

The next few sections describe how to prepare for and then to create an NDB Cluster backup using the functionality for this purpose found in the ndb\_mgm management client. To distinguish this type

of backup from a backup made using mysqldump, we sometimes refer to it as a "native" NDB Cluster backup. (For information about the creation of backups with mysqldump, see Section 6.5.4, "mysqldump — A Database Backup Program".) Restoration of NDB Cluster backups is done using the ndb\_restore utility provided with the NDB Cluster distribution; for information about ndb\_restore and its use in restoring NDB Cluster backups, see Section 25.5.23, "ndb\_restore — Restore an NDB Cluster Backup".

NDB 8.0 makes it possible to create backups using multiple LDMs to achieve parallelism on the data nodes. See [Section 25.6.8.5, "Taking an NDB Backup with Parallel Data Nodes"](#page-98-0).