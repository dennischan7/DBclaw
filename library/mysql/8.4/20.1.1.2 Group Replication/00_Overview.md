---
source: MySQL 8.4 Reference
title: 00_Overview
---

Group Replication is a technique that can be used to implement fault-tolerant systems. A replication group is a set of servers, each of which has a complete copy of the data (a shared-nothing replication scheme), which interact with each other through message passing. The communication layer provides a set of guarantees such as atomic message and total order message delivery. These are very powerful properties that translate into very useful abstractions that one can resort to build more advanced database replication solutions.

MySQL Group Replication builds on top of such properties and abstractions and implements a multisource update everywhere replication protocol. A replication group is formed by multiple servers; each server in the group may execute transactions independently at any time. Read/write transactions commit only after they have been approved by the group. In other words, for any read/write transaction the group needs to decide whether it commits or not, so the commit operation is not a unilateral decision from the originating server. Read-only transactions need no coordination within the group and commit immediately.

When a read/write transaction is ready to commit at the originating server, the server atomically broadcasts the write values (the rows that were changed) and the corresponding write set (the unique identifiers of the rows that were updated). Because the transaction is sent through an atomic broadcast, either all servers in the group receive the transaction or none do. If they receive it, then they all receive it in the same order with respect to other transactions that were sent before. All servers therefore receive the same set of transactions in the same order, and a global total order is established for the transactions.

However, there may be conflicts between transactions that execute concurrently on different servers. Such conflicts are detected by inspecting and comparing the write sets of two different and concurrent transactions, in a process called certification. During certification, conflict detection is carried out at row level: if two concurrent transactions, that executed on different servers, update the same row, then there is a conflict. The conflict resolution procedure states that the transaction that was ordered first commits on all servers, and the transaction ordered second aborts, and is therefore rolled back on the originating server and dropped by the other servers in the group. For example, if t1 and t2 execute concurrently at different sites, both changing the same row, and t2 is ordered before t1, then t2 wins the conflict and t1 is rolled back. This is in fact a distributed first commit wins rule. Note that if two transactions are bound to conflict more often than not, then it is a good practice to start them on the same server, where they have a chance to synchronize on the local lock manager instead of being rolled back as a result of certification.

For applying and externalizing the certified transactions, Group Replication permits servers to deviate from the agreed order of the transactions if this does not break consistency and validity. Group Replication is an eventual consistency system, meaning that as soon as the incoming traffic slows down or stops, all group members have the same data content. While traffic is flowing, transactions can be externalized in a slightly different order, or externalized on some members before the others. For example, in multi-primary mode, a local transaction might be externalized immediately following certification, although a remote transaction that is earlier in the global order has not yet been applied. This is permitted when the certification process has established that there is no conflict between the transactions. In single-primary mode, on the primary server, there is a small chance that concurrent, non-conflicting local transactions might be committed and externalized in a different order from the global order agreed by Group Replication. On the secondaries, which do not accept writes from clients, transactions are always committed and externalized in the agreed order.

The following figure depicts the MySQL Group Replication protocol and by comparing it to MySQL Replication (or even MySQL semisynchronous replication) you can see some differences. Some underlying consensus and Paxos related messages are missing from this picture for the sake of clarity.

**Figure 20.3 MySQL Group Replication Protocol**

# <span id="page-13-0"></span>**20.1.2 Group Replication Use Cases**

Group Replication enables you to create fault-tolerant systems with redundancy by replicating the system state to a set of servers. Even if some of the servers subsequently fail, as long it is not all or a majority, the system is still available. Depending on the number of servers which fail the group might have degraded performance or scalability, but it is still available. Server failures are isolated and independent. They are tracked by a group membership service which relies on a distributed failure detector that is able to signal when any servers leave the group, either voluntarily or due to an unexpected halt. There is a distributed recovery procedure to ensure that when servers join the group they are brought up to date automatically. There is no need for server failover, and the multi-source update everywhere nature ensures that even updates are not blocked in the event of a single server failure. To summarize, MySQL Group Replication guarantees that the database service is continuously available.

It is important to understand that although the database service is available, in the event of an unexpected server exit, those clients connected to it must be redirected, or failed over, to a different server. This is not something Group Replication attempts to resolve. A connector, load balancer, router, or some form of middleware are more suitable to deal with this issue. For example see [MySQL Router](https://dev.mysql.com/doc/mysql-router/8.4/en/) [8.4.](https://dev.mysql.com/doc/mysql-router/8.4/en/)

To summarize, MySQL Group Replication provides a highly available, highly elastic, dependable MySQL service.

![](_page_13_Picture_7.jpeg)

#### **Tip**

To deploy multiple instances of MySQL, you can use [InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-cluster.md) which enables you to easily administer a group of MySQL server instances in [MySQL](https://dev.mysql.com/doc/mysql-shell/8.4/en/) [Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/). InnoDB Cluster wraps MySQL Group Replication in a programmatic environment that enables you easily deploy a cluster of MySQL instances to achieve high availability. In addition, InnoDB Cluster interfaces seamlessly with [MySQL Router,](https://dev.mysql.com/doc/mysql-router/8.4/en/) which enables your applications to connect to the cluster without writing your own failover process. For similar use cases that do not require high availability, however, you can use [InnoDB ReplicaSet.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-replicaset.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md)

## **Example Use Cases**

The following examples are typical use cases for Group Replication.

- Elastic Replication Environments that require a very fluid replication infrastructure, where the number of servers has to grow or shrink dynamically and with as few side-effects as possible. For instance, database services for the cloud.
- Highly Available Shards Sharding is a popular approach to achieve write scale-out. Use MySQL Group Replication to implement highly available shards, where each shard maps to a replication group.
- Alternative to asynchronous Source-Replica replication In certain situations, using a single source server makes it a single point of contention. Writing to an entire group may prove more scalable under certain circumstances.
- Autonomic Systems Additionally, you can deploy MySQL Group Replication purely for the automation that is built into the replication protocol (described already in this and previous chapters).

# <span id="page-14-0"></span>**20.1.3 Multi-Primary and Single-Primary Modes**

Group Replication operates either in single-primary mode or in multi-primary mode. The group's mode is a group-wide configuration setting, specified by the [group\\_replication\\_single\\_primary\\_mode](#page-162-0) system variable, which must be the same on all members. ON means single-primary mode, which is the default mode, and OFF means multi-primary mode. It is not possible to have members of the group deployed in different modes, for example one member configured in multi-primary mode while another member is in single-primary mode.

You cannot change the value of [group\\_replication\\_single\\_primary\\_mode](#page-162-0) manually while Group Replication is running. You can use the group\_replication\_switch\_to\_single\_primary\_mode() and group\_replication\_switch\_to\_multi\_primary\_mode() functions to move a group from one mode to another while Group Replication is still running. These functions manage the process of changing the group's mode and ensure the safety and consistency of your data. In earlier releases, to change the group's mode you must stop Group Replication and change the value of [group\\_replication\\_single\\_primary\\_mode](#page-162-0) on all members. Then carry out a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) to implement the change to the new operating configuration. You do not need to restart the servers.

Regardless of the deployed mode, Group Replication does not handle client-side failover. That must be handled by a middleware framework such as [MySQL Router 8.4](https://dev.mysql.com/doc/mysql-router/8.4/en/), a proxy, a connector, or the application itself.

## <span id="page-14-1"></span>**20.1.3.1 Single-Primary Mode**

In single-primary mode ([group\\_replication\\_single\\_primary\\_mode=ON](#page-162-0)) the group has a single primary server that is set to read/write mode. All the other members in the group are set to read-only mode (with super\_read\_only=ON). The primary typically bootstraps the entire group. All other servers that join the group learn about the primary server and are automatically set to read-only mode.

In single-primary mode, Group Replication enforces that only a single server writes to the group, so compared to multi-primary mode, consistency checking can be less strict and DDL statements do not need to be handled with any extra care. The option [group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-137-0) enables or disables strict consistency checks for a group. When deploying in single-primary mode, or changing the group to single-primary mode, this system variable must be set to OFF.

The member that is designated as the primary server can change in the following ways:

- If the existing primary leaves the group, whether voluntarily or unexpectedly, a new primary is elected automatically.
- You can appoint a specific member as the new primary using the group\_replication\_set\_as\_primary() function.

• If you use the group\_replication\_switch\_to\_single\_primary\_mode() function to change a group that was running in multi-primary mode to run in single-primary mode, a new primary is elected automatically, or you can appoint the new primary by specifying it with the function.

When a new primary server is elected (automatically or manually), it is automatically set to read/write, and the other group members remain as secondaries, and as such, read-only. The following diagram shows this process:

**Figure 20.4 New Primary Election**

![](_page_15_Figure_4.jpeg)

When a new primary is chosen, it might have a backlog of changes that had been applied on the old primary but have not yet been applied on the new one. In this case, until the new primary catches up with the old one, read/write transactions might result in conflicts and be rolled back, and read-only transactions might result in stale reads. The Group Replication flow control mechanism minimizes the difference between fast and slow members, and so reduces the chances of this happening if it is activated and properly tuned. For more information, see [Section 20.7.2, "Flow Control"](#page-91-2). You can also use the [group\\_replication\\_consistency](#page-136-0) system variable to set the group's level of transaction consistency to prevent this issue. Setting this variable to BEFORE\_ON\_PRIMARY\_FAILOVER (the default) or any higher consistency level holds new transactions on a newly elected primary until the backlog has been applied.

For more information on transaction consistency, see [Section 20.5.3, "Transaction Consistency](#page-51-0) [Guarantees".](#page-51-0) If flow control and transaction consistency guarantees are not used for a group, it is a good practice to wait for the new primary to apply its replication-related relay log before re-routing client applications to it.

### **Primary Election Algorithm**

The automatic primary member election process involves each member looking at the new view of the group, ordering the potential new primary members, and choosing the member that qualifies as the most suitable. Each member makes its own decision locally, following the primary election algorithm in its MySQL Server release. Because all members must reach the same decision, members adapt their primary election algorithm if other group members are running lower MySQL Server versions, so that they have the same behavior as the member with the lowest MySQL Server version in the group.

The factors considered by members when electing a primary, in order, are as follows:

- 1. The first factor considered is which member or members are running the lowest MySQL Server version. All group members are first ordered by the patch version of their release.
- 2. If more than one member is running the lowest MySQL Server version, the second factor considered is the member weight of each of those members, as specified by the [group\\_replication\\_member\\_weight](#page-150-0) system variable on the member.

The [group\\_replication\\_member\\_weight](#page-150-0) system variable specifies a number in the range 0-100. All members default to a weight of 50, so set a weight below this to lower their ordering, and a weight above it to increase their ordering. You can use this weighting function to prioritize the use of better hardware or to ensure failover to a specific member during scheduled maintenance of the primary.

3. If more than one member is running the lowest MySQL Server version, and more than one of those members has the highest member weight (or member weighting is being ignored), the third factor considered is the lexicographical order of the generated server UUIDs of each member, as specified by the server\_uuid system variable. The member with the lowest server UUID is chosen as the primary. This factor acts as a guaranteed and predictable tie-breaker so that all group members reach the same decision if it cannot be determined by any important factors.

### <span id="page-16-1"></span>**Finding the Primary**

To find out which server is currently the primary when deployed in single-primary mode, use the MEMBER\_ROLE column in the performance\_schema.replication\_group\_members table. For example:

```
mysql> SELECT MEMBER_HOST, MEMBER_ROLE FROM performance_schema.replication_group_members;
+-------------------------+-------------+
| MEMBER_HOST | MEMBER_ROLE |
+-------------------------+-------------+
| remote1.example.com | PRIMARY |
| remote2.example.com | SECONDARY |
| remote3.example.com | SECONDARY |
+-------------------------+-------------+
```