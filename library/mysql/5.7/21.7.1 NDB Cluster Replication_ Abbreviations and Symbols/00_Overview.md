---
source: MySQL 5.7 Reference
title: 00_Overview
---

Throughout this section, we use the following abbreviations or symbols for referring to the source and replica clusters, and to processes and commands run on the clusters or cluster nodes:

**Table 21.63 Abbreviations used throughout this section referring to source and replica clusters, and to processes and commands run on cluster nodes**

| Symbol or Abbreviation | Description (Refers to)                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------------------|
| S                      | The cluster serving as the (primary) replication<br>source                                               |
| R                      | The cluster acting as the (primary) replica                                                              |
| shellS>                | Shell command to be issued on the source cluster                                                         |
| mysqlS>                | MySQL client command issued on a single<br>MySQL server running as an SQL node on the<br>source cluster  |
| mysqlS*>               | MySQL client command to be issued on all SQL<br>nodes participating in the replication source<br>cluster |
| shellR>                | Shell command to be issued on the replica cluster                                                        |
| mysqlR>                | MySQL client command issued on a single<br>MySQL server running as an SQL node on the<br>replica cluster |
| mysqlR*>               | MySQL client command to be issued on all SQL<br>nodes participating in the replica cluster               |
| C                      | Primary replication channel                                                                              |
| C'                     | Secondary replication channel                                                                            |
| S'                     | Secondary replication source                                                                             |
| R'                     | Secondary replica                                                                                        |

# <span id="page-107-0"></span>**21.7.2 General Requirements for NDB Cluster Replication**

A replication channel requires two MySQL servers acting as replication servers (one each for the source and replica). For example, this means that in the case of a replication setup with two replication channels (to provide an extra channel for redundancy), there should be a total of four replication nodes, two per cluster.

Replication of an NDB Cluster as described in this section and those following is dependent on rowbased replication. This means that the replication source MySQL server must be running with - binlog-format=ROW or --binlog-format=MIXED, as described in [Section 21.7.6, "Starting NDB](#page-124-0) [Cluster Replication \(Single Replication Channel\)".](#page-124-0) For general information about row-based replication, see Section 16.2.1, "Replication Formats".

![](_page_108_Picture_2.jpeg)

### **Important**

If you attempt to use NDB Cluster Replication with --binlogformat=STATEMENT, replication fails to work properly because the ndb\_binlog\_index table on the source cluster and the epoch column of the ndb\_apply\_status table on the replica cluster are not updated (see [Section 21.7.4, "NDB Cluster Replication Schema and Tables"\)](#page-115-0). Instead, only updates on the MySQL server acting as the replication source propagate to the replica, and no updates from any other SQL nodes in the source cluster are replicated.

The default value for the --binlog-format option is MIXED.

Each MySQL server used for replication in either cluster must be uniquely identified among all the MySQL replication servers participating in either cluster (you cannot have replication servers on both the source and replica clusters sharing the same ID). This can be done by starting each SQL node using the --server-id=id option, where id is a unique integer. Although it is not strictly necessary, we assume for purposes of this discussion that all NDB Cluster binaries are of the same release version.

It is generally true in MySQL Replication that both MySQL servers (mysqld processes) involved must be compatible with one another with respect to both the version of the replication protocol used and the SQL feature sets which they support (see Section 16.4.2, "Replication Compatibility Between MySQL Versions"). It is due to such differences between the binaries in the NDB Cluster and MySQL Server 5.7 distributions that NDB Cluster Replication has the additional requirement that both mysqld binaries come from an NDB Cluster distribution. The simplest and easiest way to assure that the mysqld servers are compatible is to use the same NDB Cluster distribution for all source and replica mysqld binaries.

We assume that the replica server or cluster is dedicated to replication of the source cluster, and that no other data is being stored on it.

All NDB tables being replicated must be created using a MySQL server and client. Tables and other database objects created using the NDB API (with, for example, [Dictionary::createTable\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-dictionary.md#ndb-dictionary-createtable)) are not visible to a MySQL server and so are not replicated. Updates by NDB API applications to existing tables that were created using a MySQL server can be replicated.

![](_page_108_Picture_10.jpeg)

### **Note**

It is possible to replicate an NDB Cluster using statement-based replication. However, in this case, the following restrictions apply:

- All updates to data rows on the cluster acting as the source must be directed to a single MySQL server.
- It is not possible to replicate a cluster using multiple simultaneous MySQL replication processes.
- Only changes made at the SQL level are replicated.

These are in addition to the other limitations of statement-based replication as opposed to row-based replication; see Section 16.2.1.1, "Advantages and Disadvantages of Statement-Based and Row-Based Replication", for more specific information concerning the differences between the two replication formats.