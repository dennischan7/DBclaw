---
source: MySQL 5.7 Reference
title: 00_Overview
---

This section discusses how to perform a rolling restart of an NDB Cluster installation, so called because it involves stopping and starting (or restarting) each node in turn, so that the cluster itself remains operational. This is often done as part of a rolling upgrade or rolling downgrade, where high availability of the cluster is mandatory and no downtime of the cluster as a whole is permissible. Where we refer to upgrades, the information provided here also generally applies to downgrades as well.

There are a number of reasons why a rolling restart might be desirable. These are described in the next few paragraphs.

# **Configuration change.**

To make a change in the cluster's configuration, such as adding an SQL node to the cluster, or setting a configuration parameter to a new value.

**NDB Cluster software upgrade or downgrade.** To upgrade the cluster to a newer version of the NDB Cluster software (or to downgrade it to an older version). This is usually referred to as a "rolling upgrade" (or "rolling downgrade", when reverting to an older version of NDB Cluster).

**Change on node host.** To make changes in the hardware or operating system on which one or more NDB Cluster node processes are running.

#### **System reset (cluster reset).**

To reset the cluster because it has reached an undesirable state. In such cases it is often desirable to reload the data and metadata of one or more data nodes. This can be done in any of three ways:

- Start each data node process (ndbd or possibly ndbmtd) with the --initial option, which forces the data node to clear its file system and to reload all NDB Cluster data and metadata from the other data nodes.
- Create a backup using the ndb\_mgm client [START BACKUP](#page-192-0) command prior to performing the restart. Following the upgrade, restore the node or nodes using [ndb\\_restore](#page-81-3).

See [Section 21.6.8, "Online Backup of NDB Cluster"](#page-191-1), and [Section 21.5.24, "ndb\\_restore — Restore](#page-81-3) [an NDB Cluster Backup",](#page-81-3) for more information.

• Use mysqldump to create a backup prior to the upgrade; afterward, restore the dump using LOAD DATA.

### **Resource Recovery.**

To free memory previously allocated to a table by successive INSERT and DELETE operations, for reuse by other NDB Cluster tables.

The process for performing a rolling restart may be generalized as follows:

- 1. Stop all cluster management nodes (ndb\_mgmd processes), reconfigure them, then restart them. (See [Rolling restarts with multiple management servers](#page-180-1).)
- 2. Stop, reconfigure, then restart each cluster data node (ndbd process) in turn.

Some node configuration parameters can be updated by issuing [RESTART](#page-143-1) for each of the data nodes in the ndb\_mgm client following the previous step. Other parameters require that the data node be stopped completely using the management client [STOP](#page-145-1) command, then started again from a system shell by invoking the ndbd or ndbmtd executable as appropriate. (A shell command such as kill can also be used on most Unix systems to stop a data node process, but the STOP command is preferred and usually simpler.)

![](_page_179_Picture_8.jpeg)

#### **Note**

On Windows, you can also use SC STOP and SC START commands, NET STOP and NET START commands, or the Windows Service Manager to stop and start nodes which have been installed as Windows services (see Section 21.3.2.4, "Installing NDB Cluster Processes as Windows Services").

The type of restart required is indicated in the documentation for each node configuration parameter. See Section 21.4.3, "NDB Cluster Configuration Files".

3. Stop, reconfigure, then restart each cluster SQL node (mysqld process) in turn.

NDB Cluster supports a somewhat flexible order for upgrading nodes. When upgrading an NDB Cluster, you may upgrade API nodes (including SQL nodes) before upgrading the management nodes, data nodes, or both. In other words, you are permitted to upgrade the API and SQL nodes in any order. This is subject to the following provisions:

- This functionality is intended for use as part of an online upgrade only. A mix of node binaries from different NDB Cluster releases is neither intended nor supported for continuous, long-term use in a production setting.
- You must upgrade all nodes of the same type (management, data, or API node) before upgrading any nodes of a different type. This remains true regardless of the order in which the nodes are upgraded.
- You must upgrade all management nodes before upgrading any data nodes. This remains true regardless of the order in which you upgrade the cluster's API and SQL nodes.
- Features specific to the "new" version must not be used until all management nodes and data nodes have been upgraded.

This also applies to any MySQL Server version change that may apply, in addition to the NDB engine version change, so do not forget to take this into account when planning the upgrade. (This is true for online upgrades of NDB Cluster in general.)

It is not possible for any API node to perform schema operations (such as data definition statements) during a node restart. Due in part to this limitation, schema operations are also not supported during an online upgrade or downgrade. In addition, it is not possible to perform native backups while an upgrade or downgrade is ongoing.

<span id="page-180-1"></span>**Rolling restarts with multiple management servers.** When performing a rolling restart of an NDB Cluster with multiple management nodes, you should keep in mind that ndb\_mgmd checks to see if any other management node is running, and, if so, tries to use that node's configuration data. To keep this from occurring, and to force ndb\_mgmd to re-read its configuration file, perform the following steps:

- 1. Stop all NDB Cluster ndb\_mgmd processes.
- 2. Update all config.ini files.
- 3. Start a single ndb\_mgmd with --reload, --initial, or both options as desired.
- 4. If you started the first ndb\_mgmd with the --initial option, you must also start any remaining ndb\_mgmd processes using --initial.

Regardless of any other options used when starting the first ndb\_mgmd, you should not start any remaining ndb\_mgmd processes after the first one using --reload.

5. Complete the rolling restarts of the data nodes and API nodes as normal.

When performing a rolling restart to update the cluster's configuration, you can use the config\_generation column of the ndbinfo.nodes table to keep track of which data nodes have been successfully restarted with the new configuration. See Section 21.6.15.28, "The ndbinfo nodes Table".

# <span id="page-180-0"></span>**21.6.6 NDB Cluster Single User Mode**

Single user mode enables the database administrator to restrict access to the database system to a single API node, such as a MySQL server (SQL node) or an instance of [ndb\\_restore](#page-81-3). When entering single user mode, connections to all other API nodes are closed gracefully and all running transactions are aborted. No new transactions are permitted to start.

Once the cluster has entered single user mode, only the designated API node is granted access to the database.

You can use the ALL STATUS command in the ndb\_mgm client to see when the cluster has entered single user mode. You can also check the status column of the ndbinfo.nodes table (see Section 21.6.15.28, "The ndbinfo nodes Table", for more information).

### Example:

```
ndb_mgm> ENTER SINGLE USER MODE 5
```

After this command has executed and the cluster has entered single user mode, the API node whose node ID is 5 becomes the cluster's only permitted user.

The node specified in the preceding command must be an API node; attempting to specify any other type of node is rejected.

![](_page_180_Picture_17.jpeg)

#### **Note**

When the preceding command is invoked, all transactions running on the designated node are aborted, the connection is closed, and the server must be restarted.

The command EXIT SINGLE USER MODE changes the state of the cluster's data nodes from single user mode to normal mode. API nodes—such as MySQL Servers—waiting for a connection (that is, waiting for the cluster to become ready and available), are again permitted to connect. The API node denoted as the single-user node continues to run (if still connected) during and after the state change.

#### Example:

ndb\_mgm> **EXIT SINGLE USER MODE**

There are two recommended ways to handle a node failure when running in single user mode:

- Method 1:
  - 1. Finish all single user mode transactions
  - 2. Issue the EXIT SINGLE USER MODE command
  - 3. Restart the cluster's data nodes
- Method 2:

Restart storage nodes prior to entering single user mode.

# <span id="page-181-0"></span>**21.6.7 Adding NDB Cluster Data Nodes Online**

This section describes how to add NDB Cluster data nodes "online"—that is, without needing to shut down the cluster completely and restart it as part of the process.

![](_page_181_Picture_11.jpeg)

# **Important**

Currently, you must add new data nodes to an NDB Cluster as part of a new node group. In addition, it is not possible to change the number of fragment replicas (or the number of nodes per node group) online.