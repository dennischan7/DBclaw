---
source: MySQL 5.7 Reference
title: 00_Overview
---

In this section, we discuss MySQL standard security procedures as they apply to running NDB Cluster.

In general, any standard procedure for running MySQL securely also applies to running a MySQL Server as part of an NDB Cluster. First and foremost, you should always run a MySQL Server as the mysql operating system user; this is no different from running MySQL in a standard (non-Cluster) environment. The mysql system account should be uniquely and clearly defined. Fortunately, this is the default behavior for a new MySQL installation. You can verify that the mysqld process is running as the mysql operating system user by using the system command such as the one shown here:

```
$> ps aux | grep mysql
root 10467 0.0 0.1 3616 1380 pts/3 S 11:53 0:00 \
 /bin/sh ./mysqld_safe --ndbcluster --ndb-connectstring=localhost:1186
mysql 10512 0.2 2.5 58528 26636 pts/3 Sl 11:53 0:00 \
```

```
 /usr/local/mysql/libexec/mysqld --basedir=/usr/local/mysql \
 --datadir=/usr/local/mysql/var --user=mysql --ndbcluster \
 --ndb-connectstring=localhost:1186 --pid-file=/usr/local/mysql/var/mothra.pid \
 --log-error=/usr/local/mysql/var/mothra.err
jon 10579 0.0 0.0 2736 688 pts/0 S+ 11:54 0:00 grep mysql
```

If the mysqld process is running as any other user than mysql, you should immediately shut it down and restart it as the mysql user. If this user does not exist on the system, the mysql user account should be created, and this user should be part of the mysql user group; in this case, you should also make sure that the MySQL data directory on this system (as set using the --datadir option for mysqld) is owned by the mysql user, and that the SQL node's my.cnf file includes user=mysql in the [mysqld] section. Alternatively, you can start the MySQL server process with --user=mysql on the command line, but it is preferable to use the my.cnf option, since you might forget to use the command-line option and so have mysqld running as another user unintentionally. The mysqld\_safe startup script forces MySQL to run as the mysql user.

![](_page_105_Picture_3.jpeg)

### **Important**

Never run mysqld as the system root user. Doing so means that potentially any file on the system can be read by MySQL, and thus—should MySQL be compromised—by an attacker.

 As mentioned in the previous section (see [Section 21.6.18.2, "NDB Cluster and MySQL Privileges"\)](#page-102-0), you should always set a root password for the MySQL Server as soon as you have it running. You should also delete the anonymous user account that is installed by default. You can accomplish these tasks using the following statements:

```
$> mysql -u root
mysql> UPDATE mysql.user
 -> SET Password=PASSWORD('secure_password')
 -> WHERE User='root';
mysql> DELETE FROM mysql.user
 -> WHERE User='';
mysql> FLUSH PRIVILEGES;
```

Be very careful when executing the DELETE statement not to omit the WHERE clause, or you risk deleting all MySQL users. Be sure to run the FLUSH PRIVILEGES statement as soon as you have modified the mysql.user table, so that the changes take immediate effect. Without FLUSH PRIVILEGES, the changes do not take effect until the next time that the server is restarted.

![](_page_105_Picture_9.jpeg)

### **Note**

 Many of the NDB Cluster utilities such as ndb\_show\_tables, ndb\_desc, and ndb\_select\_all also work without authentication and can reveal table names, schemas, and data. By default these are installed on Unix-style systems with the permissions wxr-xr-x (755), which means they can be executed by any user that can access the mysql/bin directory.

See Section 21.5, "NDB Cluster Programs", for more information about these utilities.

# <span id="page-105-0"></span>**21.7 NDB Cluster Replication**

NDB Cluster supports asynchronous replication, more usually referred to simply as "replication". This section explains how to set up and manage a configuration in which one group of computers operating as an NDB Cluster replicates to a second computer or group of computers. We assume some familiarity on the part of the reader with standard MySQL replication as discussed elsewhere in this Manual. (See Chapter 16, Replication).

![](_page_106_Picture_1.jpeg)

### **Note**

NDB Cluster does not support replication using GTIDs; semisynchronous replication and group replication are also not supported by the NDB storage engine.

Normal (non-clustered) replication involves a source server (formerly called a "master") and a replica server (formerly referred to as a "slave"), the source being so named because operations and data to be replicated originate with it, and the replica being the recipient of these. In NDB Cluster, replication is conceptually very similar but can be more complex in practice, as it may be extended to cover a number of different configurations including replicating between two complete clusters. Although an NDB Cluster itself depends on the NDB storage engine for clustering functionality, it is not necessary to use NDB as the storage engine for the replica's copies of the replicated tables (see [Replication from](#page-113-0) [NDB to other storage engines\)](#page-113-0). However, for maximum availability, it is possible (and preferable) to replicate from one NDB Cluster to another, and it is this scenario that we discuss, as shown in the following figure:

**Figure 21.12 NDB Cluster-to-Cluster Replication Layout**

In this scenario, the replication process is one in which successive states of a source cluster are logged and saved to a replica cluster. This process is accomplished by a special thread known as the NDB binary log injector thread, which runs on each MySQL server and produces a binary log (binlog). This thread ensures that all changes in the cluster producing the binary log—and not just those changes that are effected through the MySQL Server—are inserted into the binary log with the correct serialization order. We refer to the MySQL source and replica servers as replication servers or replication nodes, and the data flow or line of communication between them as a replication channel.

For information about performing point-in-time recovery with NDB Cluster and NDB Cluster Replication, see [Section 21.7.9.2, "Point-In-Time Recovery Using NDB Cluster Replication"](#page-133-0).

**NDB API replica status variables.** NDB API counters can provide enhanced monitoring capabilities on replica clusters. These counters are implemented as NDB statistics \_slave status variables, as seen in the output of SHOW STATUS, or in the results of queries against the SESSION\_STATUS or GLOBAL\_STATUS table in a mysql client session connected to a MySQL Server that is acting as a replica in NDB Cluster Replication. By comparing the values of these status variables before and after the execution of statements affecting replicated NDB tables, you can observe the corresponding actions taken on the NDB API level by the replica, which can be useful when monitoring or troubleshooting NDB Cluster Replication. [Section 21.6.14, "NDB API Statistics Counters and Variables"](#page-10-0), provides additional information.

**Replication from NDB to non-NDB tables.** It is possible to replicate NDB tables from an NDB Cluster acting as the replication source to tables using other MySQL storage engines such as InnoDB or MyISAM on a replica mysqld. This is subject to a number of conditions; see [Replication from NDB](#page-113-0) [to other storage engines,](#page-113-0) and [Replication from NDB to a nontransactional storage engine,](#page-113-1) for more information.