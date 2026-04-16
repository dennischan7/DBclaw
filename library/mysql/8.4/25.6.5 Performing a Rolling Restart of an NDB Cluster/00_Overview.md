---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section discusses how to perform a rolling restart of an NDB Cluster installation, so called because it involves stopping and starting (or restarting) each node in turn, so that the cluster itself remains operational. This is often done as part of a rolling upgrade or rolling downgrade, where high availability of the cluster is mandatory and no downtime of the cluster as a whole is permissible. Where we refer to upgrades, the information provided here also generally applies to downgrades as well.

There are a number of reasons why a rolling restart might be desirable. These are described in the next few paragraphs.

#### **Configuration change.**

To make a change in the cluster's configuration, such as adding an SQL node to the cluster, or setting a configuration parameter to a new value.

**NDB Cluster software upgrade or downgrade.** To upgrade the cluster to a newer version of the NDB Cluster software (or to downgrade it to an older version). This is usually referred to as a "rolling upgrade" (or "rolling downgrade", when reverting to an older version of NDB Cluster).

**Change on node host.** To make changes in the hardware or operating system on which one or more NDB Cluster node processes are running.

#### **System reset (cluster reset).**

To reset the cluster because it has reached an undesirable state. In such cases it is often desirable to reload the data and metadata of one or more data nodes. This can be done in any of three ways:

• Start each data node process (ndbd or possibly ndbmtd) with the --initial option, which forces the data node to clear its file system and to reload all NDB Cluster data and metadata from the other data nodes. This also forces the removal of all Disk Data objects and files associated with those objects.

• Create a backup using the ndb\_mgm client [START BACKUP](#page-151-1) command prior to performing the restart. Following the upgrade, restore the node or nodes using [ndb\\_restore](#page-35-7).

See [Section 25.6.8, "Online Backup of NDB Cluster"](#page-150-0), and [Section 25.5.23, "ndb\\_restore — Restore](#page-35-7) [an NDB Cluster Backup",](#page-35-7) for more information.

• Use mysqldump to create a backup prior to the upgrade; afterward, restore the dump using LOAD DATA.

#### **Resource Recovery.**

To free memory previously allocated to a table by successive INSERT and DELETE operations, for reuse by other NDB Cluster tables.

The process for performing a rolling restart may be generalized as follows:

- 1. Stop all cluster management nodes (ndb\_mgmd processes), reconfigure them, then restart them. (See [Rolling restarts with multiple management servers](#page-139-1).)
- 2. Stop, reconfigure, then restart each cluster data node (ndbd process) in turn.

Some node configuration parameters can be updated by issuing [RESTART](#page-102-1) for each of the data nodes in the ndb\_mgm client following the previous step. Other parameters require that the data node be stopped completely using the management client [STOP](#page-104-1) command, then started again from a system shell by invoking the ndbd or ndbmtd executable as appropriate. (A shell command such as kill can also be used on most Unix systems to stop a data node process, but the STOP command is preferred and usually simpler.)

![](_page_138_Picture_10.jpeg)

#### **Note**

On Windows, you can also use SC STOP and SC START commands, NET STOP and NET START commands, or the Windows Service Manager to stop and start nodes which have been installed as Windows services (see Section 25.3.2.4, "Installing NDB Cluster Processes as Windows Services").

The type of restart required is indicated in the documentation for each node configuration parameter. See Section 25.4.3, "NDB Cluster Configuration Files".

3. Stop, reconfigure, then restart each cluster SQL node (mysqld process) in turn.

NDB Cluster supports a somewhat flexible order for upgrading nodes. When upgrading an NDB Cluster, you may upgrade API nodes (including SQL nodes) before upgrading the management nodes, data nodes, or both. In other words, you are permitted to upgrade the API and SQL nodes in any order. This is subject to the following provisions:

- This functionality is intended for use as part of an online upgrade only. A mix of node binaries from different NDB Cluster releases is neither intended nor supported for continuous, long-term use in a production setting.
- You must upgrade all nodes of the same type (management, data, or API node) before upgrading any nodes of a different type. This remains true regardless of the order in which the nodes are upgraded.
- You must upgrade all management nodes before upgrading any data nodes. This remains true regardless of the order in which you upgrade the cluster's API and SQL nodes.
- Features specific to the "new" version must not be used until all management nodes and data nodes have been upgraded.

This also applies to any MySQL Server version change that may apply, in addition to the NDB engine version change, so do not forget to take this into account when planning the upgrade. (This is true for online upgrades of NDB Cluster in general.)

It is not possible for any API node to perform schema operations (such as data definition statements) during a node restart. Due in part to this limitation, schema operations are also not supported during an online upgrade or downgrade. In addition, it is not possible to perform native backups while an upgrade or downgrade is ongoing.

<span id="page-139-1"></span>**Rolling restarts with multiple management servers.** When performing a rolling restart of an NDB Cluster with multiple management nodes, you should keep in mind that ndb\_mgmd checks to see if any other management node is running, and, if so, tries to use that node's configuration data. To keep this from occurring, and to force ndb\_mgmd to re-read its configuration file, perform the following steps:

- 1. Stop all NDB Cluster ndb\_mgmd processes.
- 2. Update all config.ini files.
- 3. Start a single ndb\_mgmd with --reload, --initial, or both options as desired.
- 4. If you started the first ndb\_mgmd with the --initial option, you must also start any remaining ndb\_mgmd processes using --initial.

Regardless of any other options used when starting the first ndb\_mgmd, you should not start any remaining ndb\_mgmd processes after the first one using --reload.

5. Complete the rolling restarts of the data nodes and API nodes as normal.

When performing a rolling restart to update the cluster's configuration, you can use the config\_generation column of the ndbinfo.nodes table to keep track of which data nodes have been successfully restarted with the new configuration. See Section 25.6.15.48, "The ndbinfo nodes Table".

## <span id="page-139-0"></span>**25.6.6 NDB Cluster Single User Mode**

Single user mode enables the database administrator to restrict access to the database system to a single API node, such as a MySQL server (SQL node) or an instance of [ndb\\_restore](#page-35-7). When entering single user mode, connections to all other API nodes are closed gracefully and all running transactions are aborted. No new transactions are permitted to start.

Once the cluster has entered single user mode, only the designated API node is granted access to the database.

You can use the ALL STATUS command in the ndb\_mgm client to see when the cluster has entered single user mode. You can also check the status column of the ndbinfo.nodes table (see Section 25.6.15.48, "The ndbinfo nodes Table", for more information).

#### Example:

ndb\_mgm> **ENTER SINGLE USER MODE 5**

After this command has executed and the cluster has entered single user mode, the API node whose node ID is 5 becomes the cluster's only permitted user.

The node specified in the preceding command must be an API node; attempting to specify any other type of node is rejected.

![](_page_139_Picture_18.jpeg)

### **Note**

When the preceding command is invoked, all transactions running on the designated node are aborted, the connection is closed, and the server must be restarted.

The command EXIT SINGLE USER MODE changes the state of the cluster's data nodes from single user mode to normal mode. API nodes—such as MySQL Servers—waiting for a connection (that is,

waiting for the cluster to become ready and available), are again permitted to connect. The API node denoted as the single-user node continues to run (if still connected) during and after the state change.

#### Example:

ndb\_mgm> **EXIT SINGLE USER MODE**

There are two recommended ways to handle a node failure when running in single user mode:

- Method 1:
  - 1. Finish all single user mode transactions
  - 2. Issue the EXIT SINGLE USER MODE command
  - 3. Restart the cluster's data nodes
- Method 2:

Restart storage nodes prior to entering single user mode.

## <span id="page-140-0"></span>**25.6.7 Adding NDB Cluster Data Nodes Online**

This section describes how to add NDB Cluster data nodes "online"—that is, without needing to shut down the cluster completely and restart it as part of the process.

![](_page_140_Picture_13.jpeg)

#### **Important**

Currently, you must add new data nodes to an NDB Cluster as part of a new node group. In addition, it is not possible to change the number of fragment replicas (or the number of nodes per node group) online.

### **25.6.7.1 Adding NDB Cluster Data Nodes Online: General Issues**

This section provides general information about the behavior of and current limitations in adding NDB Cluster nodes online.

**Redistribution of Data.** The ability to add new nodes online includes a means to reorganize NDBCLUSTER table data and indexes so that they are distributed across all data nodes, including the new ones, by means of the ALTER TABLE ... REORGANIZE PARTITION statement. Table reorganization of both in-memory and Disk Data tables is supported. This redistribution does not currently include unique indexes (only ordered indexes are redistributed).

The redistribution for NDBCLUSTER tables already existing before the new data nodes were added is not automatic, but can be accomplished using simple SQL statements in mysql or another MySQL client application. However, all data and indexes added to tables created after a new node group has been added are distributed automatically among all cluster data nodes, including those added as part of the new node group.

**Partial starts.** It is possible to add a new node group without all of the new data nodes being started. It is also possible to add a new node group to a degraded cluster—that is, a cluster that is only partially started, or where one or more data nodes are not running. In the latter case, the cluster must have enough nodes running to be viable before the new node group can be added.

**Effects on ongoing operations.** Normal DML operations using NDB Cluster data are not prevented by the creation or addition of a new node group, or by table reorganization. However, it is not possible to perform DDL concurrently with table reorganization—that is, no other DDL statements can be issued while an ALTER TABLE ... REORGANIZE PARTITION statement is executing. In addition, during the execution of ALTER TABLE ... REORGANIZE PARTITION (or the execution of any other DDL statement), it is not possible to restart cluster data nodes.

**Failure handling.** Failures of data nodes during node group creation and table reorganization are handled as shown in the following table:

**Table 25.38 Data node failure handling during node group creation and table reorganization**

| Failure during       | Failure in "Old" data<br>node                                                                                                                                                                                                                                                                                                                                                                        | Failure in "New" data<br>node                                                                                                                                                                                                                                                                                                                                                                        | System Failure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Node group creation  | •<br>If a node other than<br>the master fails:<br>The creation of the<br>node group is always<br>rolled forward.<br>•<br>If the master fails:<br>•<br>If the internal<br>commit point has<br>been reached:<br>The creation of the<br>node group is rolled<br>forward.<br>•<br>If the internal<br>commit point<br>has not yet been<br>reached.<br>The<br>creation of the node<br>group is rolled back | •<br>If a node other than<br>the master fails:<br>The creation of the<br>node group is always<br>rolled forward.<br>•<br>If the master fails:<br>•<br>If the internal<br>commit point has<br>been reached:<br>The creation of the<br>node group is rolled<br>forward.<br>•<br>If the internal<br>commit point<br>has not yet been<br>reached.<br>The<br>creation of the node<br>group is rolled back | •<br>If the execution<br>of CREATE<br>NODEGROUP has<br>reached the internal<br>commit point:<br>When restarted, the<br>cluster includes the<br>new node group.<br>Otherwise it without.<br>•<br>If the execution<br>of CREATE<br>NODEGROUP has<br>not yet reached the<br>internal commit<br>point:<br>When<br>restarted, the cluster<br>does not include the<br>new node group.                                                                                                                                                                                 |
| Table reorganization | •<br>If a node other<br>than the master<br>fails:<br>The table<br>reorganization is<br>always rolled forward.<br>•<br>If the master fails:<br>•<br>If the internal<br>commit point<br>has been<br>reached:<br>The<br>table reorganization<br>is rolled forward.<br>•<br>If the internal<br>commit point<br>has not yet been<br>reached.<br>The<br>table reorganization<br>is rolled back.            | •<br>If a node other<br>than the master<br>fails:<br>The table<br>reorganization is<br>always rolled forward.<br>•<br>If the master fails:<br>•<br>If the internal<br>commit point<br>has been<br>reached:<br>The<br>table reorganization<br>is rolled forward.<br>•<br>If the internal<br>commit point<br>has not yet been<br>reached.<br>The<br>table reorganization<br>is rolled back.            | •<br>If the execution of<br>an ALTER TABLE<br>REORGANIZE<br>PARTITION<br>statement has<br>reached the internal<br>commit point:<br>When the cluster<br>is restarted, the<br>data and indexes<br>belonging to table<br>are distributed using<br>the "new" data nodes.<br>•<br>If the execution of<br>an ALTER TABLE<br>REORGANIZE<br>PARTITION<br>statement has not<br>yet reached the<br>internal commit<br>point:<br>When the<br>cluster is restarted,<br>the data and indexes<br>belonging to table<br>are distributed using<br>only the "old" data<br>nodes. |

**Dropping node groups.** The ndb\_mgm client supports a [DROP NODEGROUP](#page-100-1) command, but it is possible to drop a node group only when no data nodes in the node group contain any data. Since

there is currently no way to "empty" a specific data node or node group, this command works only the following two cases:

- 1. After issuing [CREATE NODEGROUP](#page-100-0) in the ndb\_mgm client, but before issuing any ALTER TABLE ... REORGANIZE PARTITION statements in the mysql client.
- 2. After dropping all NDBCLUSTER tables using DROP TABLE.

TRUNCATE TABLE does not work for this purpose because the data nodes continue to store the table definitions.

### **25.6.7.2 Adding NDB Cluster Data Nodes Online: Basic procedure**

In this section, we list the basic steps required to add new data nodes to an NDB Cluster. This procedure applies whether you are using ndbd or ndbmtd binaries for the data node processes. For a more detailed example, see [Section 25.6.7.3, "Adding NDB Cluster Data Nodes Online: Detailed](#page-143-0) [Example"](#page-143-0).

Assuming that you already have a running NDB Cluster, adding data nodes online requires the following steps:

1. Edit the cluster configuration config.ini file, adding new [ndbd] sections corresponding to the nodes to be added. In the case where the cluster uses multiple management servers, these changes need to be made to all config.ini files used by the management servers.

You must be careful that node IDs for any new data nodes added in the config.ini file do not overlap node IDs used by existing nodes. In the event that you have API nodes using dynamically allocated node IDs and these IDs match node IDs that you want to use for new data nodes, it is possible to force any such API nodes to "migrate", as described later in this procedure.

2. Perform a rolling restart of all NDB Cluster management servers.

![](_page_142_Picture_11.jpeg)

#### **Important**

All management servers must be restarted with the --reload or - initial option to force the reading of the new configuration.

3. Perform a rolling restart of all existing NDB Cluster data nodes. It is not necessary (or usually even desirable) to use --initial when restarting the existing data nodes.

If you are using API nodes with dynamically allocated IDs matching any node IDs that you wish to assign to new data nodes, you must restart all API nodes (including SQL nodes) before restarting any of the data nodes processes in this step. This causes any API nodes with node IDs that were previously not explicitly assigned to relinquish those node IDs and acquire new ones.

- 4. Perform a rolling restart of any SQL or API nodes connected to the NDB Cluster.
- 5. Start the new data nodes.

The new data nodes may be started in any order. They can also be started concurrently, as long as they are started after the rolling restarts of all existing data nodes have been completed, and before proceeding to the next step.

- 6. Execute one or more [CREATE NODEGROUP](#page-100-0) commands in the NDB Cluster management client to create the new node group or node groups to which the new data nodes belong.
- 7. Redistribute the cluster's data among all data nodes, including the new ones. Normally this is done by issuing an ALTER TABLE ... ALGORITHM=INPLACE, REORGANIZE PARTITION statement in the mysql client for each NDBCLUSTER table.

Exception: For tables created using the MAX\_ROWS option, this statement does not work; instead, use ALTER TABLE ... ALGORITHM=INPLACE MAX\_ROWS=... to reorganize such tables. You should also bear in mind that using MAX\_ROWS to set the number of partitions in this fashion is

deprecated, and you should use PARTITION\_BALANCE instead; see Section 15.1.20.12, "Setting NDB Comment Options", for more information.

![](_page_143_Picture_2.jpeg)

#### **Note**

This needs to be done only for tables already existing at the time the new node group is added. Data in tables created after the new node group is added is distributed automatically; however, data added to any given table tbl that existed before the new nodes were added is not distributed using the new nodes until that table has been reorganized.

8. ALTER TABLE ... REORGANIZE PARTITION ALGORITHM=INPLACE reorganizes partitions but does not reclaim the space freed on the "old" nodes. You can do this by issuing, for each NDBCLUSTER table, an OPTIMIZE TABLE statement in the mysql client.

This works for space used by variable-width columns of in-memory NDB tables. OPTIMIZE TABLE is not supported for fixed-width columns of in-memory tables; it is also not supported for Disk Data tables.

You can add all the nodes desired, then issue several [CREATE NODEGROUP](#page-100-0) commands in succession to add the new node groups to the cluster.

### <span id="page-143-0"></span>**25.6.7.3 Adding NDB Cluster Data Nodes Online: Detailed Example**

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
HostName = 198.51.100.21
```

![](_page_143_Picture_12.jpeg)

#### **Note**

We have left a gap in the sequence between data node IDs and other nodes. This make it easier later to assign node IDs that are not already in use to data nodes which are newly added.

We also assume that you have already started the cluster using the appropriate command line or my.cnf options, and that running [SHOW](#page-102-0) in the management client produces output similar to what is shown here:

```
-- NDB Cluster -- Management Client --
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186 (using cleartext)
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.4.7-ndb-8.4.7, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.4.7-ndb-8.4.7, Nodegroup: 0)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.4.7-ndb-8.4.7)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.4.7-ndb-8.4.7)
id=21 @198.51.100.21 (8.4.7-ndb-8.4.7)
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

![](_page_144_Picture_5.jpeg)

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
```

```
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

1. Stop the management server using the management client [STOP](#page-104-1) command, as shown here:

```
ndb_mgm> 10 STOP
Node 10 has shut down.
Disconnecting to allow Management Server to shutdown
$>
```

2. Because shutting down the management server causes the management client to terminate, you must start the management server from the system shell. For simplicity, we assume that config.ini is in the same directory as the management server binary, but in practice, you must supply the correct path to the configuration file. You must also supply the --reload or --initial option so that the management server reads the new configuration from the file rather than its configuration cache. If your shell's current directory is also the same as the directory where the management server binary is located, then you can invoke the management server as shown here:

```
$> ndb_mgmd -f config.ini --reload
2008-12-08 17:29:23 [MgmSrvr] INFO -- NDB Cluster Management Server. 8.4.7-ndb-8.4.7
2008-12-08 17:29:23 [MgmSrvr] INFO -- Reading cluster configuration from 'config.ini'
```

If you check the output of [SHOW](#page-102-0) in the management client after restarting the ndb\_mgm process, you should now see something like this:

```
-- NDB Cluster -- Management Client --
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186 (using cleartext)
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.4.7-ndb-8.4.7, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.4.7-ndb-8.4.7, Nodegroup: 0)
id=3 (not connected, accepting connect from 198.51.100.3)
id=4 (not connected, accepting connect from 198.51.100.4)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.4.7-ndb-8.4.7)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.4.7-ndb-8.4.7)
id=21 @198.51.100.21 (8.4.7-ndb-8.4.7)
```

**Step 3: Perform a rolling restart of the existing data nodes.** This step can be accomplished entirely within the cluster management client using the [RESTART](#page-102-1) command, as shown here:

```
ndb_mgm> 1 RESTART
Node 1: Node shutdown initiated
Node 1: Node shutdown completed, restarting, no start.
Node 1 is being restarted
ndb_mgm> Node 1: Start initiated (version 8.4.7)
Node 1: Started (version 8.4.7)
ndb_mgm> 2 RESTART
Node 2: Node shutdown initiated
```

```
Node 2: Node shutdown completed, restarting, no start.
Node 2 is being restarted
ndb_mgm> Node 2: Start initiated (version 8.4.7)
ndb_mgm> Node 2: Started (version 8.4.7)
```

![](_page_146_Picture_2.jpeg)

#### **Important**

After issuing each X RESTART command, wait until the management client reports Node X: Started (version ...) before proceeding any further.

You can verify that all existing data nodes were restarted using the updated configuration by checking the ndbinfo.nodes table in the mysql client.

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

![](_page_146_Picture_11.jpeg)

#### **Note**

Unlike the case with restarting the existing data nodes, you can start the new data nodes concurrently; you do not need to wait for one to finish starting before starting the other.

Wait until both of the new data nodes have started before proceeding with the next step. Once the new data nodes have started, you can see in the output of the management client [SHOW](#page-102-0) command that they do not yet belong to any node group (as indicated with bold type here):

```
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186 (using cleartext)
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.4.7-ndb-8.4.7, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.4.7-ndb-8.4.7, Nodegroup: 0)
id=3 @198.51.100.3 (8.4.7-ndb-8.4.7, no nodegroup)
id=4 @198.51.100.4 (8.4.7-ndb-8.4.7, no nodegroup)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.4.7-ndb-8.4.7)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.4.7-ndb-8.4.7)
id=21 @198.51.100.21 (8.4.7-ndb-8.4.7)
```

**Step 6: Create a new node group.** You can do this by issuing a [CREATE NODEGROUP](#page-100-0) command in the cluster management client. This command takes as its argument a comma-separated list of the node IDs of the data nodes to be included in the new node group, as shown here:

```
ndb_mgm> CREATE NODEGROUP 3,4
Nodegroup 1 created
```

By issuing [SHOW](#page-102-0) again, you can verify that data nodes 3 and 4 have joined the new node group (again indicated in bold type):

```
ndb_mgm> SHOW
Connected to Management Server at: 198.51.100.10:1186 (using cleartext)
Cluster Configuration
---------------------
[ndbd(NDB)] 2 node(s)
id=1 @198.51.100.1 (8.4.7-ndb-8.4.7, Nodegroup: 0, *)
id=2 @198.51.100.2 (8.4.7-ndb-8.4.7, Nodegroup: 0)
id=3 @198.51.100.3 (8.4.7-ndb-8.4.7, Nodegroup: 1)
id=4 @198.51.100.4 (8.4.7-ndb-8.4.7, Nodegroup: 1)
[ndb_mgmd(MGM)] 1 node(s)
id=10 @198.51.100.10 (8.4.7-ndb-8.4.7)
[mysqld(API)] 2 node(s)
id=20 @198.51.100.20 (8.4.7-ndb-8.4.7)
id=21 @198.51.100.21 (8.4.7-ndb-8.4.7)
```

**Step 7: Redistribute cluster data.** When a node group is created, existing data and indexes are not automatically distributed to the new node group's data nodes, as you can see by issuing the appropriate [REPORT](#page-102-2) command in the management client:

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
```

```
-- Per partition info --
Partition Row count Commit count Frag fixed memory Frag varsized memory
0 26086 26086 1572864 557056
1 26329 26329 1605632 557056
```

You can cause the data to be redistributed among all of the data nodes by performing, for each NDB table, an ALTER TABLE ... ALGORITHM=INPLACE, REORGANIZE PARTITION statement in the mysql client.

![](_page_148_Picture_3.jpeg)

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
1 13236 52515 1605632 557056
2 13105 13105 819200 294912
3 13093 13093 819200 294912
```

![](_page_148_Picture_9.jpeg)

#### **Note**

Normally, ALTER TABLE table\_name [ALGORITHM=INPLACE,] REORGANIZE PARTITION is used with a list of partition identifiers and a set of partition definitions to create a new partitioning scheme for a table that has already been explicitly partitioned. Its use here to redistribute data onto a new NDB Cluster node group is an exception in this regard; when used in this way, no other keywords or identifiers follow REORGANIZE PARTITION.

For more information, see Section 15.1.9, "ALTER TABLE Statement".

In addition, for each table, the ALTER TABLE statement should be followed by an OPTIMIZE TABLE to reclaim wasted space. You can obtain a list of all NDBCLUSTER tables using the following query against the Information Schema TABLES table:

```
SELECT TABLE_SCHEMA, TABLE_NAME
 FROM INFORMATION_SCHEMA.TABLES
 WHERE ENGINE = 'NDBCLUSTER';
```

![](_page_149_Picture_5.jpeg)

#### **Note**

The INFORMATION\_SCHEMA.TABLES.ENGINE value for an NDB Cluster table is always NDBCLUSTER, regardless of whether the CREATE TABLE statement used to create the table (or ALTER TABLE statement used to convert an existing table from a different storage engine) used NDB or NDBCLUSTER in its ENGINE option.

You can see after performing these statements in the output of [ALL REPORT MEMORY](#page-102-2) that the data and indexes are now redistributed between all cluster data nodes, as shown here:

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

![](_page_149_Picture_10.jpeg)

### **Note**

Since only one DDL operation on NDBCLUSTER tables can be executed at a time, you must wait for each ALTER TABLE ... REORGANIZE PARTITION statement to finish before issuing the next one.

It is not necessary to issue ALTER TABLE ... REORGANIZE PARTITION statements for NDBCLUSTER tables created after the new data nodes have been added; data added to such tables is distributed among all data nodes automatically. However, in NDBCLUSTER tables that existed prior to the addition of the new nodes, neither existing nor new data is distributed using the new nodes until these tables have been reorganized using ALTER TABLE ... REORGANIZE PARTITION.

**Alternative procedure, without rolling restart.** It is possible to avoid the need for a rolling restart by configuring the extra data nodes, but not starting them, when first starting the cluster. We assume, as before, that you wish to start with two data nodes—nodes 1 and 2—in one node group and later to expand the cluster to four data nodes, by adding a second node group consisting of nodes 3 and 4:

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
```

```
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

![](_page_150_Picture_5.jpeg)

#### **Note**

StartNoNodegroupTimeout must be the same for all data nodes in the cluster; for this reason, you should always set it in the [ndbd default] section of the config.ini file, rather than for individual data nodes.

When you are ready to add the second node group, you need only perform the following additional steps:

1. Start data nodes 3 and 4, invoking the data node process once for each new node:

```
$> ndbd -c 198.51.100.10 --initial
```

2. Issue the appropriate [CREATE NODEGROUP](#page-100-0) command in the management client:

```
ndb_mgm> CREATE NODEGROUP 3,4
```

3. In the mysql client, issue ALTER TABLE ... REORGANIZE PARTITION and OPTIMIZE TABLE statements for each existing NDBCLUSTER table. (As noted elsewhere in this section, existing NDB Cluster tables cannot use the new nodes for data distribution until this has been done.)

# <span id="page-150-0"></span>**25.6.8 Online Backup of NDB Cluster**

The next few sections describe how to prepare for and then to create an NDB Cluster backup using the functionality for this purpose found in the ndb\_mgm management client. To distinguish this type of backup from a backup made using mysqldump, we sometimes refer to it as a "native" NDB Cluster backup. (For information about the creation of backups with mysqldump, see Section 6.5.4, "mysqldump — A Database Backup Program".) Restoration of NDB Cluster backups is done using the [ndb\\_restore](#page-35-7) utility provided with the NDB Cluster distribution; for information about [ndb\\_restore](#page-35-7) and its use in restoring NDB Cluster backups, see [Section 25.5.23, "ndb\\_restore — Restore an NDB](#page-35-7) [Cluster Backup"](#page-35-7).

It is also possible to create backups using multiple LDMs to achieve parallelism on the data nodes. See [Section 25.6.8.5, "Taking an NDB Backup with Parallel Data Nodes".](#page-156-0)

### <span id="page-151-0"></span>**25.6.8.1 NDB Cluster Backup Concepts**

A backup is a snapshot of the database at a given time. The backup consists of three main parts:

- **Metadata.** The names and definitions of all database tables
- **Table records.** The data actually stored in the database tables at the time that the backup was made
- **Transaction log.** A sequential record telling how and when data was stored in the database

Each of these parts is saved on all nodes participating in the backup. During backup, each node saves these three parts into three files on disk:

• BACKUP-backup\_id.node\_id.ctl

A control file containing control information and metadata. Each node saves the same table definitions (for all tables in the cluster) to its own version of this file.

• BACKUP-backup\_id-0.node\_id.data

A data file containing the table records, which are saved on a per-fragment basis. That is, different nodes save different fragments during the backup. The file saved by each node starts with a header that states the tables to which the records belong. Following the list of records there is a footer containing a checksum for all records.

• BACKUP-backup\_id.node\_id.log

A log file containing records of committed transactions. Only transactions on tables stored in the backup are stored in the log. Nodes involved in the backup save different records because different nodes host different database fragments.

In the listing just shown, backup\_id stands for the backup identifier and node\_id is the unique identifier for the node creating the file.

The location of the backup files is determined by the BackupDataDir parameter.

### <span id="page-151-1"></span>**25.6.8.2 Using The NDB Cluster Management Client to Create a Backup**

Before starting a backup, make sure that the cluster is properly configured for performing one. (See [Section 25.6.8.3, "Configuration for NDB Cluster Backups".](#page-155-0))

The START BACKUP command is used to create a backup, and has the syntax shown here:

```
START BACKUP [backup_id]
 [encryption_option]
 [wait_option]
 [snapshot_option]
encryption_option:
ENCRYPT [PASSWORD=password]
password:
{'password_string' | "password_string"}
wait_option:
WAIT {STARTED | COMPLETED} | NOWAIT
snapshot_option:
SNAPSHOTSTART | SNAPSHOTEND
```

Successive backups are automatically identified sequentially, so the backup\_id, an integer greater than or equal to 1, is optional; if it is omitted, the next available value is used. If an existing backup\_id value is used, the backup fails with the error Backup failed: file already exists. If used, the backup\_id must follow immediately after the START BACKUP keywords, before any other options are used.

START BACKUP supports the creation of encrypted backups using ENCRYPT PASSWORD=password. The password must meet all of the following requirements:

- Uses any of the printable ASCII characters except !, ', ", \$, %, \, and ^
- Is no more than 256 characters in length
- Is enclosed by single or double quotation marks

When ENCRYPT PASSWORD='password' is used, the backup data record and log files written by each data node are encrypted with a key derived from the user-provided password and a randomlygenerated salt using a key derivation function (KDF) that employs the PBKDF2-SHA256 algorithm to generate a symmetric encryption key for that file. This function has the form shown here:

```
key = KDF(random_salt, password)
```

The key so generated is then used to encrypt the backup data using AES 256 CBC inline, and symmetric encryption is employed for encrypting the backup fileset (with the generated key).

![](_page_152_Picture_8.jpeg)

#### **Note**

NDB Cluster never saves the user-furnished password or generated encryption key.

The PASSWORD option can be omitted from encryption\_option. In this case, the management client prompts the user for a password.

It is possible using PASSWORD to set an empty password ('' or ""), but this is not recommended.

An encrypted backup can be decrypted using any of the following commands:

- [ndb\\_restore](#page-35-7) [--decrypt](#page-39-0) [--backup-password=](#page-38-0)password
- [ndbxfrm](#page-93-0) [--decrypt-password=](#page-94-0)password input\_file output\_file
- [ndb\\_print\\_backup\\_file](#page-27-4) [-P](#page-28-0) password file\_name
- [ndb\\_restore](#page-35-7) [--decrypt](#page-39-0) [--backup-password-from-stdin](#page-38-1)
- [ndbxfrm](#page-93-0) [--decrypt-password-from-stdin](#page-94-2) input\_file output\_file
- [ndb\\_print\\_backup\\_file](#page-27-4) [--backup-password=](#page-28-0)password file\_name
- [ndb\\_print\\_backup\\_file](#page-27-4) [--backup-password-from-stdin](#page-28-1) file\_name
- ndb\_mgm --backup-password-from-stdin --execute "START BACKUP ..."

See the descriptions of these programs for more information, such as additional options that may be required.

The wait\_option can be used to determine when control is returned to the management client after a START BACKUP command is issued, as shown in the following list:

• If NOWAIT is specified, the management client displays a prompt immediately, as seen here:

```
ndb_mgm> START BACKUP NOWAIT
ndb_mgm>
```

In this case, the management client can be used even while it prints progress information from the backup process.

• With WAIT STARTED the management client waits until the backup has started before returning control to the user, as shown here:

```
ndb_mgm> START BACKUP WAIT STARTED
```

```
Waiting for started, this may take several minutes
Node 2: Backup 3 started from node 1
ndb_mgm>
```

• **WAIT COMPLETED** causes the management client to wait until the backup process is complete before returning control to the user.

WAIT COMPLETED is the default.

 A snapshot\_option can be used to determine whether the backup matches the state of the cluster when START BACKUP was issued, or when it was completed. SNAPSHOTSTART causes the backup to match the state of the cluster when the backup began; SNAPSHOTEND causes the backup to reflect the state of the cluster when the backup was finished. SNAPSHOTEND is the default, and matches the behavior found in previous NDB Cluster releases.

![](_page_153_Picture_5.jpeg)

#### **Note**

If you use the SNAPSHOTSTART option with START BACKUP, and the CompressedBackup parameter is enabled, only the data and control files are compressed—the log file is not compressed.

If both a wait\_option and a snapshot\_option are used, they may be specified in either order. For example, all of the following commands are valid, assuming that there is no existing backup having 4 as its ID:

```
START BACKUP WAIT STARTED SNAPSHOTSTART
START BACKUP SNAPSHOTSTART WAIT STARTED
START BACKUP 4 WAIT COMPLETED SNAPSHOTSTART
START BACKUP SNAPSHOTEND WAIT COMPLETED
START BACKUP 4 NOWAIT SNAPSHOTSTART
```

The procedure for creating a backup consists of the following steps:

- 1. Start the management client (ndb\_mgm), if it not running already.
- 2. Execute the **START BACKUP** command. This produces several lines of output indicating the progress of the backup, as shown here:

```
ndb_mgm> START BACKUP
Waiting for completed, this may take several minutes
Node 2: Backup 1 started from node 1
Node 2: Backup 1 started from node 1 completed
 StartGCP: 177 StopGCP: 180
 #Records: 7362 #LogRecords: 0
 Data: 453648 bytes Log: 0 bytes
ndb_mgm>
```

3. When the backup has started the management client displays this message:

```
Backup backup_id started from node node_id
```

backup\_id is the unique identifier for this particular backup. This identifier is saved in the cluster log, if it has not been configured otherwise. node\_id is the identifier of the management server that is coordinating the backup with the data nodes. At this point in the backup process the cluster has received and processed the backup request. It does not mean that the backup has finished. An example of this statement is shown here:

```
Node 2: Backup 1 started from node 1
```

4. The management client indicates with a message like this one that the backup has started:

```
Backup backup_id started from node node_id completed
```

As is the case for the notification that the backup has started, backup\_id is the unique identifier for this particular backup, and node\_id is the node ID of the management server that is coordinating the backup with the data nodes. This output is accompanied by additional information including relevant global checkpoints, the number of records backed up, and the size of the data, as shown here:

```
Node 2: Backup 1 started from node 1 completed
 StartGCP: 177 StopGCP: 180
 #Records: 7362 #LogRecords: 0
 Data: 453648 bytes Log: 0 bytes
```

It is also possible to perform a backup from the system shell by invoking ndb\_mgm with the -e or - execute option, as shown in this example:

```
$> ndb_mgm -e "START BACKUP 6 WAIT COMPLETED SNAPSHOTSTART"
```

When using START BACKUP in this way, you must specify the backup ID.

Cluster backups are created by default in the BACKUP subdirectory of the DataDir on each data node. This can be overridden for one or more data nodes individually, or for all cluster data nodes in the config.ini file using the BackupDataDir configuration parameter. The backup files created for a backup with a given backup\_id are stored in a subdirectory named BACKUP-backup\_id in the backup directory.

<span id="page-154-0"></span>**Cancelling backups.** To cancel or abort a backup that is already in progress, perform the following steps:

- 1. Start the management client.
- 2. Execute this command:

```
ndb_mgm> ABORT BACKUP backup_id
```

The number backup\_id is the identifier of the backup that was included in the response of the management client when the backup was started (in the message Backup backup\_id started from node management\_node\_id).

3. The management client acknowledges the abort request with Abort of backup backup\_id ordered.

![](_page_154_Picture_13.jpeg)

#### **Note**

At this point, the management client has not yet received a response from the cluster data nodes to this request, and the backup has not yet actually been aborted.

4. After the backup has been aborted, the management client reports this fact in a manner similar to what is shown here:

```
Node 1: Backup 3 started from 5 has been aborted.
 Error: 1321 - Backup aborted by user request: Permanent error: User defined error
Node 3: Backup 3 started from 5 has been aborted.
 Error: 1323 - 1323: Permanent error: Internal error
Node 2: Backup 3 started from 5 has been aborted.
 Error: 1323 - 1323: Permanent error: Internal error
Node 4: Backup 3 started from 5 has been aborted.
 Error: 1323 - 1323: Permanent error: Internal error
```

In this example, we have shown sample output for a cluster with 4 data nodes, where the sequence number of the backup to be aborted is 3, and the management node to which the cluster management client is connected has the node ID 5. The first node to complete its part in aborting the backup reports that the reason for the abort was due to a request by the user. (The remaining nodes report that the backup was aborted due to an unspecified internal error.)

![](_page_154_Picture_19.jpeg)

### **Note**

There is no guarantee that the cluster nodes respond to an ABORT BACKUP command in any particular order.

The Backup backup\_id started from node management\_node\_id has been aborted messages mean that the backup has been terminated and that all files relating to this backup have been removed from the cluster file system.

It is also possible to abort a backup in progress from a system shell using this command:

\$> **ndb\_mgm -e "ABORT BACKUP backup\_id"**

![](_page_155_Picture_4.jpeg)

#### **Note**

If there is no backup having the ID backup\_id running when an ABORT BACKUP is issued, the management client makes no response, nor is it indicated in the cluster log that an invalid abort command was sent.

### <span id="page-155-0"></span>**25.6.8.3 Configuration for NDB Cluster Backups**

Five configuration parameters are essential for backup:

• BackupDataBufferSize

The amount of memory used to buffer data before it is written to disk.

• BackupLogBufferSize

The amount of memory used to buffer log records before these are written to disk.

• BackupMemory

The total memory allocated in a data node for backups. This should be the sum of the memory allocated for the backup data buffer and the backup log buffer.

• BackupWriteSize

The default size of blocks written to disk. This applies for both the backup data buffer and the backup log buffer.

• BackupMaxWriteSize

The maximum size of blocks written to disk. This applies for both the backup data buffer and the backup log buffer.

In addition, CompressedBackup causes NDB to use compression when creating and writing to backup files.

More detailed information about these parameters can be found in Backup Parameters.

You can also set a location for the backup files using the BackupDataDir configuration parameter. The default is FileSystemPath/BACKUP/BACKUP-backup\_id.

You can enforce encryption of backup files by setting RequireEncryptedBackup to 1; this prevents the creation of backups without specifying ENCRYPT PASSWORD=password as part of a START BACKUP command.

### **25.6.8.4 NDB Cluster Backup Troubleshooting**

If an error code is returned when issuing a backup request, the most likely cause is insufficient memory or disk space. You should check that there is enough memory allocated for the backup.

![](_page_155_Picture_25.jpeg)

### **Important**

If you have set BackupDataBufferSize and BackupLogBufferSize and their sum is greater than 4MB, then you must also set BackupMemory as well. You should also make sure that there is sufficient space on the hard drive partition of the backup target.

NDB does not support repeatable reads, which can cause problems with the restoration process. Although the backup process is "hot", restoring an NDB Cluster from backup is not a 100% "hot" process. This is due to the fact that, for the duration of the restore process, running transactions get nonrepeatable reads from the restored data. This means that the state of the data is inconsistent while the restore is in progress.

### <span id="page-156-0"></span>**25.6.8.5 Taking an NDB Backup with Parallel Data Nodes**

It is possible to take a backup with multiple local data managers (LDMs) acting in parallel on the data nodes. For this to work, all data nodes in the cluster must use multiple LDMs, and each data node must use the same number of LDMs. This means that all data nodes must run ndbmtd (ndbd is single-threaded and thus always has only one LDM) and they must be configured to use multiple LDMs before taking the backup; ndbmtd by default runs in single-threaded mode. You can cause them to use multiple LDMs by choosing an appropriate setting for one of the multi-threaded data node configuration parameters MaxNoOfExecutionThreads or ThreadConfig. Keep in mind that changing these parameters requires a restart of the cluster; this can be a rolling restart. In addition, the EnableMultithreadedBackup parameter must be set to 1 for each data node (this is the default).

Depending on the number of LDMs and other factors, you may also need to increase NoOfFragmentLogParts. If you are using large Disk Data tables, you may also need to increase DiskPageBufferMemory. As with single-threaded backups, you may also want or need to make adjustments to settings for BackupDataBufferSize, BackupMemory, and other configuration parameters relating to backups (see Backup parameters).

Once all data nodes are using multiple LDMs, you can take the parallel backup using the [START](#page-151-1) [BACKUP](#page-151-1) command in the NDB management client just as you would if the data nodes were running ndbd (or ndbmtd in single-threaded mode); no additional or special syntax is required, and you can specify a backup ID, wait option, or snapshot option in any combination as needed or desired.

Backups using multiple LDMs create subdirectories, one per LDM, under the directory BACKUP/ BACKUP-backup\_id/ (which in turn resides under the BackupDataDir) on each data node; these subdirectories are named BACKUP-backup\_id-PART-1-OF-N/, BACKUP-backup\_id-PART-2-OF-N/, and so on, up to BACKUP-backup\_id-PART-N-OF-N/, where backup\_id is the backup ID used for this backup and N is the number of LDMs per data node. Each of these subdirectories contains the usual backup files BACKUP-backup\_id-0.node\_id.Data, BACKUP-backup\_id.node\_id.ctl, and BACKUP-backup\_id.node\_id.log, where node\_id is the node ID of this data node.

[ndb\\_restore](#page-35-7) automatically checks for the presence of the subdirectories just described; if it finds them, it attempts to restore the backup in parallel. For information about restoring backups taken with multiple LDMs, see [Restoring from a backup taken in parallel.](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-parallel-data-node-backup.md)

To force creation of a single-threaded backup, set EnableMultithreadedBackup = 0 for all data nodes (you can do this by setting the parameter in the [ndbd default] section of the config.ini global configuration file). It is also possible to restore a parallel backup to a cluster running an older version of NDB. See [Restoring an NDB backup to a previous version of NDB Cluster](https://dev.mysql.com/doc/refman/8.0/en/ndb-restore-to-different-version.md#ndb-restore-to-previous-version), for more information.