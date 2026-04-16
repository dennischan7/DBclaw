---
source: MySQL 8.0 Reference
title: 00_Overview
---

If you have followed the instructions but your replication setup is not working, the first thing to do is check the error log for messages. Many users have lost time by not doing this soon enough after encountering problems.

If you cannot tell from the error log what the problem was, try the following techniques:

- Verify that the source has binary logging enabled by issuing a SHOW MASTER STATUS statement. Binary logging is enabled by default. If binary logging is enabled, Position is nonzero. If binary logging is not enabled, verify that you are not running the source with any settings that disable binary logging, such as the --skip-log-bin option.
- Verify that the server\_id system variable was set at startup on both the source and replica and that the ID value is unique on each server.
- Verify that the replica is running. Use SHOW REPLICA STATUS to check whether the Replica\_IO\_Running and Replica\_SQL\_Running values are both Yes. If not, verify the options that were used when starting the replica server. For example, the --skip-slave-start command line option, or from MySQL 8.0.24, the skip\_slave\_start system variable, prevents the replication threads from starting until you issue a START REPLICA statement.
- If the replica is running, check whether it established a connection to the source. Use SHOW PROCESSLIST, find the I/O (receiver) and SQL (applier) threads and check their State column to see what they display. See Section 19.2.3, "Replication Threads". If the receiver thread state says Connecting to master, check the following:
  - Verify the privileges for the replication user on the source.
  - Check that the host name of the source is correct and that you are using the correct port to connect to the source. The port used for replication is the same as used for client network communication (the default is 3306). For the host name, ensure that the name resolves to the correct IP address.
  - Check the configuration file to see whether the skip\_networking system variable has been enabled on the source or replica to disable networking. If so, comment the setting or remove it.
  - If the source has a firewall or IP filtering configuration, ensure that the network port being used for MySQL is not being filtered.
  - Check that you can reach the source by using ping or traceroute/tracert to reach the host.
- If the replica was running previously but has stopped, the reason usually is that some statement that succeeded on the source failed on the replica. This should never happen if you have taken a proper snapshot of the source, and never modified the data on the replica outside of the replication threads. If the replica stops unexpectedly, it is a bug or you have encountered one of the known replication limitations described in [Section 19.5.1, "Replication Features and Issues"](#page-49-0). If it is a bug, see [Section 19.5.5, "How to Report Replication Bugs or Problems"](#page-80-0), for instructions on how to report it.

- If a statement that succeeded on the source refuses to run on the replica, try the following procedure if it is not feasible to do a full database resynchronization by deleting the replica's databases and copying a new snapshot from the source:
  - 1. Determine whether the affected table on the replica is different from the source table. Try to understand how this happened. Then make the replica's table identical to the source's and run START REPLICA.
  - 2. If the preceding step does not work or does not apply, try to understand whether it would be safe to make the update manually (if needed) and then ignore the next statement from the source.
  - 3. If you decide that the replica can skip the next statement from the source, issue the following statements:

```
mysql> SET GLOBAL sql_slave_skip_counter = N;
mysql> START SLAVE;
Or from MySQL 8.0.26:
mysql> SET GLOBAL sql_replica_skip_counter = N;
mysql> START REPLICA;
```

The value of N should be 1 if the next statement from the source does not use AUTO\_INCREMENT or LAST\_INSERT\_ID(). Otherwise, the value should be 2. The reason for using a value of 2 for statements that use AUTO\_INCREMENT or LAST\_INSERT\_ID() is that they take two events in the binary log of the source.

See also [SET GLOBAL sql\\_slave\\_skip\\_counter Syntax](https://dev.mysql.com/doc/refman/5.7/en/set-global-sql-slave-skip-counter.md).

4. If you are sure that the replica started out perfectly synchronized with the source, and that no one has updated the tables involved outside of the replication threads, then presumably the discrepancy is the result of a bug. If you are running the most recent version of MySQL, please report the problem. If you are running an older version, try upgrading to the latest production release to determine whether the problem persists.

# <span id="page-80-0"></span>**19.5.5 How to Report Replication Bugs or Problems**

When you have determined that there is no user error involved, and replication still either does not work at all or is unstable, it is time to send us a bug report. We need to obtain as much information as possible from you to be able to track down the bug. Please spend some time and effort in preparing a good bug report.

If you have a repeatable test case that demonstrates the bug, please enter it into our bugs database using the instructions given in Section 1.5, "How to Report Bugs or Problems". If you have a "phantom" problem (one that you cannot duplicate at will), use the following procedure:

- 1. Verify that no user error is involved. For example, if you update the replica outside of the replication threads, the data goes out of synchrony, and you can have unique key violations on updates. In this case, the replication thread stops and waits for you to clean up the tables manually to bring them into synchrony. This is not a replication problem. It is a problem of outside interference causing replication to fail.
- 2. Ensure that the replica is running with binary logging enabled (the log\_bin system variable), and with the --log-slave-updates option enabled, which causes the replica to log the updates that it receives from the source into its own binary logs. These settings are the defaults.
- 3. Save all evidence before resetting the replication state. If we have no information or only sketchy information, it becomes difficult or impossible for us to track down the problem. The evidence you should collect is:
  - All binary log files from the source
  - All binary log files from the replica

- The output of SHOW MASTER STATUS from the source at the time you discovered the problem
- The output of SHOW REPLICA STATUS from the replica at the time you discovered the problem
- Error logs from the source and the replica
- 4. Use mysqlbinlog to examine the binary logs. The following should be helpful to find the problem statement. log\_file and log\_pos are the Master\_Log\_File and Read\_Master\_Log\_Pos values from SHOW REPLICA STATUS.

```
$> mysqlbinlog --start-position=log_pos log_file | head
```

After you have collected the evidence for the problem, try to isolate it as a separate test case first. Then enter the problem with as much information as possible into our bugs database using the instructions at Section 1.5, "How to Report Bugs or Problems".

# <span id="page-82-0"></span>Chapter 20 Group Replication

# **Table of Contents**

| 20.1 Group Replication Background 3854                                              |      |
|-------------------------------------------------------------------------------------|------|
| 20.1.1 Replication Technologies                                                     | 3855 |
| 20.1.2 Group Replication Use Cases 3858                                             |      |
| 20.1.3 Multi-Primary and Single-Primary Modes 3859                                  |      |
| 20.1.4 Group Replication Services 3863                                              |      |
| 20.1.5 Group Replication Plugin Architecture 3866                                   |      |
| 20.2 Getting Started 3867                                                           |      |
| 20.2.1 Deploying Group Replication in Single-Primary Mode 3867                      |      |
| 20.2.2 Deploying Group Replication Locally 3880                                     |      |
| 20.3 Requirements and Limitations 3881                                              |      |
| 20.3.1 Group Replication Requirements 3881                                          |      |
| 20.3.2 Group Replication Limitations 3884                                           |      |
| 20.4 Monitoring Group Replication 3887                                              |      |
| 20.4.1 GTIDs and Group Replication 3888                                             |      |
| 20.4.2 Group Replication Server States                                              | 3889 |
| 20.4.3 The replication_group_members Table 3890                                     |      |
| 20.4.4 The replication_group_member_stats Table 3891                                |      |
| 20.5 Group Replication Operations 3891                                              |      |
| 20.5.1 Configuring an Online Group 3891                                             |      |
| 20.5.2 Restarting a Group 3897                                                      |      |
| 20.5.3 Transaction Consistency Guarantees 3899                                      |      |
| 20.5.4 Distributed Recovery 3905                                                    |      |
| 20.5.5 Support For IPv6 And For Mixed IPv6 And IPv4 Groups 3920                     |      |
| 20.5.6 Using MySQL Enterprise Backup with Group Replication 3922                    |      |
| 20.6 Group Replication Security 3928                                                |      |
| 20.6.1 Communication Stack for Connection Security Management 3928                  |      |
| 20.6.2 Securing Group Communication Connections with Secure Socket Layer (SSL) 3931 |      |
| 20.6.3 Securing Distributed Recovery Connections 3934                               |      |
| 20.6.4 Group Replication IP Address Permissions 3938                                |      |
| 20.7 Group Replication Performance and Troubleshooting 3940                         |      |
| 20.7.1 Fine Tuning the Group Communication Thread 3941                              |      |
| 20.7.2 Flow Control 3941                                                            |      |
| 20.7.3 Single Consensus Leader 3942                                                 |      |
|                                                                                     |      |
| 20.7.4 Message Compression 3943                                                     |      |
| 20.7.5 Message Fragmentation 3945                                                   |      |
| 20.7.6 XCom Cache Management 3946                                                   |      |
| 20.7.7 Responses to Failure Detection and Network Partitioning 3948                 |      |
| 20.7.8 Handling a Network Partition and Loss of Quorum 3954                         |      |
| 20.7.9 Monitoring Group Replication Memory Usage with Performance Schema Memory     |      |
| Instrumentation 3958                                                                |      |
| 20.8 Upgrading Group Replication 3967                                               |      |
| 20.8.1 Combining Different Member Versions in a Group 3967                          |      |
| 20.8.2 Group Replication Offline Upgrade 3969                                       |      |
| 20.8.3 Group Replication Online Upgrade 3970                                        |      |
| 20.9 Group Replication Variables 3973                                               |      |
| 20.9.1 Group Replication System Variables 3975                                      |      |
| 20.9.2 Group Replication Status Variables                                           | 4017 |
| 20.10 Frequently Asked Questions                                                    | 4018 |

This chapter explains MySQL Group Replication and how to install, configure and monitor groups. MySQL Group Replication enables you to create elastic, highly-available, fault-tolerant replication topologies.

Groups can operate in a single-primary mode with automatic primary election, where only one server accepts updates at a time. Alternatively, groups can be deployed in multi-primary mode, where all servers can accept updates, even if they are issued concurrently.

There is a built-in group membership service that keeps the view of the group consistent and available for all servers at any given point in time. Servers can leave and join the group and the view is updated accordingly. Sometimes servers can leave the group unexpectedly, in which case the failure detection mechanism detects this and notifies the group that the view has changed. This is all automatic.

Group Replication guarantees that the database service is continuously available. However, it is important to understand that if one of the group members becomes unavailable, the clients connected to that group member must be redirected, or failed over, to a different server in the group, using a connector, load balancer, router, or some form of middleware. Group Replication does not have an inbuilt method to do this. For example, see [MySQL Router 8.0](https://dev.mysql.com/doc/mysql-router/8.0/en/).

Group Replication is provided as a plugin to MySQL Server. You can follow the instructions in this chapter to configure the plugin on each of the server instances that you want in the group, start up the group, and monitor and administer the group. An alternative way to deploy a group of MySQL server instances is by using InnoDB Cluster.

![](_page_83_Picture_5.jpeg)

### **Tip**

To deploy multiple instances of MySQL, you can use [InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster.md) which enables you to easily administer a group of MySQL server instances in [MySQL](https://dev.mysql.com/doc/mysql-shell/8.0/en/) [Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/). InnoDB Cluster wraps MySQL Group Replication in a programmatic environment that enables you easily deploy a cluster of MySQL instances to achieve high availability. In addition, InnoDB Cluster interfaces seamlessly with [MySQL Router,](https://dev.mysql.com/doc/mysql-router/8.0/en/) which enables your applications to connect to the cluster without writing your own failover process. For similar use cases that do not require high availability, however, you can use [InnoDB ReplicaSet.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-replicaset.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

The chapter is structured as follows:

- [Section 20.1, "Group Replication Background"](#page-83-0) provides an introduction to groups and how Group Replication works.
- [Section 20.2, "Getting Started"](#page-96-0) explains how to configure multiple MySQL Server instances to create a group.
- [Section 20.3, "Requirements and Limitations"](#page-110-0) explains architecture and setup requirements and limitations for Group Replication.
- [Section 20.4, "Monitoring Group Replication"](#page-116-0) explains how to monitor a group.
- [Section 20.5, "Group Replication Operations"](#page-120-1) explains how to work with a group.
- [Section 20.6, "Group Replication Security"](#page-157-0) explains how to secure a group.
- [Section 20.7, "Group Replication Performance and Troubleshooting"](#page-169-0) explains how to fine tune performance for a group.
- [Section 20.8, "Upgrading Group Replication"](#page-196-0) explains how to upgrade a group.
- Section 20.9, "Group Replication Variables" is a reference for the system variables specific to Group Replication.
- Section 20.10, "Frequently Asked Questions" provides answers to some technical questions about deploying and operating Group Replication.

# <span id="page-83-0"></span>**20.1 Group Replication Background**

This section provides background information on MySQL Group Replication.

The most common way to create a fault-tolerant system is to resort to making components redundant, in other words the component can be removed and the system should continue to operate as expected. This creates a set of challenges that raise complexity of such systems to a whole different level. Specifically, replicated databases have to deal with the fact that they require maintenance and administration of several servers instead of just one. Moreover, as servers are cooperating together to create the group several other classic distributed systems problems have to be dealt with, such as network partitioning or split brain scenarios.

Therefore, the ultimate challenge is to fuse the logic of the database and data replication with the logic of having several servers coordinated in a consistent and simple way. In other words, to have multiple servers agreeing on the state of the system and the data on each and every change that the system goes through. This can be summarized as having servers reaching agreement on each database state transition, so that they all progress as one single database or alternatively that they eventually converge to the same state. Meaning that they need to operate as a (distributed) state machine.

MySQL Group Replication provides distributed state machine replication with strong coordination between servers. Servers coordinate themselves automatically when they are part of the same group. The group can operate in a single-primary mode with automatic primary election, where only one server accepts updates at a time. Alternatively, for more advanced users the group can be deployed in multi-primary mode, where all servers can accept updates, even if they are issued concurrently. This power comes at the expense of applications having to work around the limitations imposed by such deployments.

There is a built-in group membership service that keeps the view of the group consistent and available for all servers at any given point in time. Servers can leave and join the group and the view is updated accordingly. Sometimes servers can leave the group unexpectedly, in which case the failure detection mechanism detects this and notifies the group that the view has changed. This is all automatic.

For a transaction to commit, the majority of the group have to agree on the order of a given transaction in the global sequence of transactions. Deciding to commit or abort a transaction is done by each server individually, but all servers make the same decision. If there is a network partition, resulting in a split where members are unable to reach agreement, then the system does not progress until this issue is resolved. Hence there is also a built-in, automatic, split-brain protection mechanism.

All of this is powered by the provided Group Communication System (GCS) protocols. These provide a failure detection mechanism, a group membership service, and safe and completely ordered message delivery. All these properties are key to creating a system which ensures that data is consistently replicated across the group of servers. At the very core of this technology lies an implementation of the Paxos algorithm. It acts as the group communication engine.

# <span id="page-84-0"></span>**20.1.1 Replication Technologies**

Before getting into the details of MySQL Group Replication, this section introduces some background concepts and an overview of how things work. This provides some context to help understand what is required for Group Replication and what the differences are between classic asynchronous MySQL Replication and Group Replication.