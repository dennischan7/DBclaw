---
source: MySQL 5.7 Reference
title: 00_Overview
---

If you have followed the instructions but your replication setup is not working, the first thing to do is check the error log for messages. Many users have lost time by not doing this soon enough after encountering problems.

If you cannot tell from the error log what the problem was, try the following techniques:

- Verify that the source has binary logging enabled by issuing a SHOW MASTER STATUS statement. If logging is enabled, Position is nonzero. If binary logging is not enabled, verify that you are running the source server with the [--log-bin](#page-77-0) option.
- Verify that the [server\\_id](#page-29-0) system variable was set at startup on both the source and replica and that the ID value is unique on each server.
- Verify that the replica is running. Use SHOW SLAVE STATUS to check whether the Slave\_IO\_Running and Slave\_SQL\_Running values are both Yes. If not, verify the options that were used when starting the replica server. For example, [--skip-slave-start](#page-53-0) prevents the replica threads from starting until you issue a START SLAVE statement.
- If the replica is running, check whether it established a connection to the source. Use SHOW PROCESSLIST, find the I/O and SQL threads and check their State column to see what they

display. See [Section 16.2.3, "Replication Threads"](#page-121-0). If the replication I/O thread state says Connecting to master, check the following:

- Verify the privileges for the user being used for replication on the source.
- Check that the host name of the source is correct and that you are using the correct port to connect to the source. The port used for replication is the same as used for client network communication (the default is 3306). For the host name, ensure that the name resolves to the correct IP address.
- Check the configuration file to see whether the skip\_networking system variable has been enabled on the source or replica to disable networking. If so, comment the setting or remove it.
- If the source has a firewall or IP filtering configuration, ensure that the network port being used for MySQL is not being filtered.
- Check that you can reach the source by using ping or traceroute/tracert to reach the host.
- If the replica was running previously but has stopped, the reason usually is that some statement that succeeded on the source failed on the replica. This should never happen if you have taken a proper snapshot of the source, and never modified the data on the replica outside of the replication threads. If the replica stops unexpectedly, it is a bug or you have encountered one of the known replication limitations described in [Section 16.4.1, "Replication Features and Issues"](#page-156-1). If it is a bug, see [Section 16.4.5, "How to Report Replication Bugs or Problems"](#page-184-0), for instructions on how to report it.
- If a statement that succeeded on the source refuses to run on the replica, try the following procedure if it is not feasible to do a full database resynchronization by deleting the replica's databases and copying a new snapshot from the source:
  - 1. Determine whether the affected table on the replica is different from the table on the source. Try to understand how this happened. Then make the replica's table identical to the source's and run START SLAVE.
  - 2. If the preceding step does not work or does not apply, try to understand whether it would be safe to make the update manually (if needed) and then ignore the next statement from the source.
  - 3. If you decide that the replica can skip the next statement from the source, issue the following statements:

```
mysql> SET GLOBAL sql_slave_skip_counter = N;
mysql> START SLAVE;
```

The value of N should be 1 if the next statement from the source does not use AUTO\_INCREMENT or LAST\_INSERT\_ID(). Otherwise, the value should be 2. The reason for using a value of 2 for statements that use AUTO\_INCREMENT or LAST\_INSERT\_ID() is that they take two events in the binary log of the source.

See also Section 13.4.2.4, "SET GLOBAL sql\_slave\_skip\_counter Syntax".

4. If you are sure that the replica started out perfectly synchronized with the source, and that no one has updated the tables involved outside of the replication threads, then presumably the discrepancy is the result of a bug. If you are running the most recent version of MySQL, please report the problem. If you are running an older version, try upgrading to the latest production release to determine whether the problem persists.

# <span id="page-184-0"></span>**16.4.5 How to Report Replication Bugs or Problems**

When you have determined that there is no user error involved, and replication still either does not work at all or is unstable, it is time to send us a bug report. We need to obtain as much information as possible from you to be able to track down the bug. Please spend some time and effort in preparing a good bug report.

If you have a repeatable test case that demonstrates the bug, please enter it into our bugs database using the instructions given in Section 1.5, "How to Report Bugs or Problems". If you have a "phantom" problem (one that you cannot duplicate at will), use the following procedure:

- 1. Verify that no user error is involved. For example, if you update the replica outside of the replication thread, the data goes out of synchrony, and you can have unique key violations on updates. In this case, the replication SQL thread stops and waits for you to clean up the tables manually to bring them into synchrony. This is not a replication problem. It is a problem of outside interference causing replication to fail.
- 2. Run the replica with the [--log-slave-updates](#page-93-0) and [--log-bin](#page-77-0) options. These options cause the replica to log the updates that it receives from the source into its own binary logs.
- 3. Save all evidence before resetting the replication state. If we have no information or only sketchy information, it becomes difficult or impossible for us to track down the problem. The evidence you should collect is:
  - All binary log files from the source
  - All binary log files from the replica
  - The output of SHOW MASTER STATUS from the source at the time you discovered the problem
  - The output of SHOW SLAVE STATUS from the replica at the time you discovered the problem
  - Error logs from the source and the replica
- 4. Use mysqlbinlog to examine the binary logs. The following should be helpful to find the problem statement. log\_file and log\_pos are the Master\_Log\_File and Read\_Master\_Log\_Pos values from SHOW SLAVE STATUS.

```
$> mysqlbinlog --start-position=log_pos log_file | head
```

After you have collected the evidence for the problem, try to isolate it as a separate test case first. Then enter the problem with as much information as possible into our bugs database using the instructions at Section 1.5, "How to Report Bugs or Problems".

# <span id="page-186-0"></span>Chapter 17 Group Replication

# **Table of Contents**

| 17.1 Group Replication Background 2960                            |      |
|-------------------------------------------------------------------|------|
| 17.1.1 Replication Technologies                                   | 2961 |
| 17.1.2 Group Replication Use Cases 2963                           |      |
| 17.1.3 Group Replication Details 2964                             |      |
| 17.2 Getting Started 2966                                         |      |
| 17.2.1 Deploying Group Replication in Single-Primary Mode 2966    |      |
| 17.2.2 Deploying Group Replication Locally 2976                   |      |
| 17.3 Requirements and Limitations 2978                            |      |
| 17.3.1 Group Replication Requirements 2978                        |      |
| 17.3.2 Group Replication Limitations 2980                         |      |
| 17.4 Monitoring Group Replication 2982                            |      |
| 17.4.1 Group Replication Server States                            | 2982 |
| 17.4.2 The replication_group_members Table 2983                   |      |
| 17.4.3 The replication_group_member_stats Table 2984              |      |
| 17.5 Group Replication Operations 2984                            |      |
| 17.5.1 Deploying in Multi-Primary or Single-Primary Mode 2984     |      |
| 17.5.2 Tuning Recovery                                            | 2986 |
| 17.5.3 Network Partitioning 2987                                  |      |
| 17.5.4 Restarting a Group 2992                                    |      |
| 17.5.5 Using MySQL Enterprise Backup with Group Replication 2994  |      |
| 17.6 Group Replication Security 2999                              |      |
| 17.6.1 Group Replication IP Address Allowlisting 2999             |      |
| 17.6.2 Group Replication Secure Socket Layer (SSL) Support 3000   |      |
| 17.6.3 Group Replication and Virtual Private Networks (VPNs) 3002 |      |
| 17.7 Group Replication Variables 3002                             |      |
| 17.7.1 Group Replication System Variables 3003                    |      |
| 17.7.2 Group Replication Status Variables                         | 3022 |
| 17.8 Frequently Asked Questions 3022                              |      |
| 17.9 Group Replication Technical Details 3026                     |      |
| 17.9.1 Group Replication Plugin Architecture 3026                 |      |
| 17.9.2 The Group 3028                                             |      |
| 17.9.3 Data Manipulation Statements 3028                          |      |
| 17.9.4 Data Definition Statements 3028                            |      |
| 17.9.5 Distributed Recovery 3029                                  |      |
| 17.9.6 Observability 3035                                         |      |
| 17.9.7 Group Replication Performance 3036                         |      |

This chapter explains MySQL Group Replication and how to install, configure and monitor groups. MySQL Group Replication is a MySQL Server plugin that enables you to create elastic, highlyavailable, fault-tolerant replication topologies.

Groups can operate in a single-primary mode with automatic primary election, where only one server accepts updates at a time. Alternatively, for more advanced users, groups can be deployed in multiprimary mode, where all servers can accept updates, even if they are issued concurrently.

There is a built-in group membership service that keeps the view of the group consistent and available for all servers at any given point in time. Servers can leave and join the group and the view is updated accordingly. Sometimes servers can leave the group unexpectedly, in which case the failure detection mechanism detects this and notifies the group that the view has changed. This is all automatic.

The chapter is structured as follows:

- [Section 17.1, "Group Replication Background"](#page-187-0) provides an introduction to groups and how Group Replication works.
- [Section 17.2, "Getting Started"](#page-193-0) explains how to configure multiple MySQL Server instances to create a group.
- Section 17.3, "Requirements and Limitations" explains architecture and setup requirements and limitations for Group Replication.
- Section 17.4, "Monitoring Group Replication" explains how to monitor a group.
- Section 17.5, "Group Replication Operations" explains how to work with a group.
- Section 17.6, "Group Replication Security" explains how to secure a group.
- [Upgrading Group Replication](https://dev.mysql.com/doc/refman/8.0/en/group-replication-upgrade.md) explains how to upgrade a group.
- Section 17.7, "Group Replication Variables" is a reference for the system variables specific to Group Replication.
- Section 17.8, "Frequently Asked Questions" provides answers to some technical questions about deploying and operating Group Replication.
- Section 17.9, "Group Replication Technical Details" provides in-depth information about how Group Replication works.

# <span id="page-187-0"></span>**17.1 Group Replication Background**

This section provides background information on MySQL Group Replication.

The most common way to create a fault-tolerant system is to resort to making components redundant, in other words the component can be removed and the system should continue to operate as expected. This creates a set of challenges that raise complexity of such systems to a whole different level. Specifically, replicated databases have to deal with the fact that they require maintenance and administration of several servers instead of just one. Moreover, as servers are cooperating together to create the group several other classic distributed systems problems have to be dealt with, such as network partitioning or split brain scenarios.

Therefore, the ultimate challenge is to fuse the logic of the database and data replication with the logic of having several servers coordinated in a consistent and simple way. In other words, to have multiple servers agreeing on the state of the system and the data on each and every change that the system goes through. This can be summarized as having servers reaching agreement on each database state transition, so that they all progress as one single database or alternatively that they eventually converge to the same state. Meaning that they need to operate as a (distributed) state machine.

MySQL Group Replication provides distributed state machine replication with strong coordination between servers. Servers coordinate themselves automatically when they are part of the same group. The group can operate in a single-primary mode with automatic primary election, where only one server accepts updates at a time. Alternatively, for more advanced users the group can be deployed in multi-primary mode, where all servers can accept updates, even if they are issued concurrently. This power comes at the expense of applications having to work around the limitations imposed by such deployments.

There is a built-in group membership service that keeps the view of the group consistent and available for all servers at any given point in time. Servers can leave and join the group and the view is updated accordingly. Sometimes servers can leave the group unexpectedly, in which case the failure detection mechanism detects this and notifies the group that the view has changed. This is all automatic.

For a transaction to commit, the majority of the group have to agree on the order of a given transaction in the global sequence of transactions. Deciding to commit or abort a transaction is done by each

server individually, but all servers make the same decision. If there is a network partition, resulting in a split where members are unable to reach agreement, then the system does not progress until this issue is resolved. Hence there is also a built-in, automatic, split-brain protection mechanism.

All of this is powered by the provided Group Communication System (GCS) protocols. These provide a failure detection mechanism, a group membership service, and safe and completely ordered message delivery. All these properties are key to creating a system which ensures that data is consistently replicated across the group of servers. At the very core of this technology lies an implementation of the Paxos algorithm. It acts as the group communication engine.

## <span id="page-188-0"></span>**17.1.1 Replication Technologies**

Before getting into the details of MySQL Group Replication, this section introduces some background concepts and an overview of how things work. This provides some context to help understand what is required for Group Replication and what the differences are between classic asynchronous MySQL Replication and Group Replication.