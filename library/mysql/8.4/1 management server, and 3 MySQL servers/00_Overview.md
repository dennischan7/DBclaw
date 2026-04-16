---
source: MySQL 8.4 Reference
title: 00_Overview
---

# The empty default sections are not required, and are shown only for
# the sake of completeness.
# Data nodes must provide a hostname but MySQL Servers are not required
# to do so.
# If you do not know the hostname for your machine, use localhost.
# The DataDir parameter also has a default value, but it is recommended to
# set it explicitly.
# [api] and [mgm] are aliases for [mysqld] and [ndb_mgmd], respectively.
[ndbd default]
NoOfReplicas= 1
[mysqld default]
[ndb_mgmd default]
[tcp default]
[ndb_mgmd]
HostName= myhost.example.com
[ndbd]
HostName= myhost.example.com
DataDir= /var/lib/mysql-cluster
[mysqld]
[mysqld]
[mysqld]
```

You can now start the ndb\_mgmd management server. By default, it attempts to read the config.ini file in its current working directory, so change location into the directory where the file is located and then invoke ndb\_mgmd:

```
$> cd /var/lib/mysql-cluster
$> ndb_mgmd
```

Then start a single data node by running ndbd:

```
$> ndbd
```

By default, ndbd looks for the management server at localhost on port 1186.

![](_page_108_Picture_7.jpeg)

# **Note**

If you have installed MySQL from a binary tarball, you must to specify the path of the ndb\_mgmd and ndbd servers explicitly. (Normally, these can be found in /usr/local/mysql/bin.)

Finally, change location to the MySQL data directory (usually /var/lib/mysql or /usr/local/ mysql/data), and make sure that the my.cnf file contains the option necessary to enable the NDB storage engine:

```
[mysqld]
ndbcluster
```

You can now start the MySQL server as usual:

```
$> mysqld_safe --user=mysql &
```

Wait a moment to make sure the MySQL server is running properly. If you see the notice mysql ended, check the server's .err file to find out what went wrong.

If all has gone well so far, you now can start using the cluster. Connect to the server and verify that the [NDBCLUSTER](#page-50-0) storage engine is enabled:

```
$> mysql
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 1 to server version: 8.4.8
```

```
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql> SHOW ENGINES\G
...

********************************
```

The row numbers shown in the preceding example output may be different from those shown on your system, depending upon how your server is configured.

Try to create an NDBCLUSTER table:

```
$> mysql
mysql> USE test;
Database changed

mysql> CREATE TABLE ctest (i INT) ENGINE=NDBCLUSTER;
Query OK, 0 rows affected (0.09 sec)

mysql> SHOW CREATE TABLE ctest \G
**********************************
    Table: ctest
Create Table: CREATE TABLE `ctest` (
    `i` int(11) default NULL
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

To check that your nodes were set up properly, start the management client:

```
$> ndb_mgm
```

Use the SHOW command from within the management client to obtain a report on the cluster's status:

```
ndb_mgm> SHOW

Cluster Configuration
-------

[ndbd(NDB)] 1 node(s)
\nid=2 @127.0.0.1 (Version: 8.4.7-ndb-8.4.7, Nodegroup: 0, *)

[ndb_mgmd(MGM)] 1 node(s)
\nid=1 @127.0.0.1 (Version: 8.4.7-ndb-8.4.7)

[mysqld(API)] 3 node(s)
\nid=3 @127.0.0.1 (Version: 8.4.7-ndb-8.4.7)
\nid=4 (not connected, accepting connect from any host)
\nid=5 (not connected, accepting connect from any host)
```

At this point, you have successfully set up a working NDB Cluster. You can now store data in the cluster by using any table created with <code>ENGINE=NDBCLUSTER</code> or its alias <code>ENGINE=NDB</code>.

# <span id="page-109-0"></span>25.4.2 Overview of NDB Cluster Configuration Parameters, Options, and Variables

The next several sections provide summary tables of NDB Cluster node configuration parameters used in the <code>config.ini</code> file to govern various aspects of node behavior, as well as of options and variables read by <code>mysqld</code> from a <code>my.cnf</code> file or from the command line when run as an NDB Cluster process. Each of the node parameter tables lists the parameters for a given type (<code>ndbd</code>, <code>ndb\_mgmd</code>, <code>mysqld</code>, <code>computer</code>, <code>tcp</code>, or <code>shm</code>). All tables include the data type for the parameter, option, or variable, as well as its default, minimum, and maximum values as applicable.

**Considerations when restarting nodes.** For node parameters, these tables also indicate what type of restart is required (node restart or system restart)—and whether the restart must be done with --initial—to change the value of a given configuration parameter. When performing a node restart or an initial node restart, all of the cluster's data nodes must be restarted in turn (also referred to as a rolling restart). It is possible to update cluster configuration parameters marked as node online—that is, without shutting down the cluster—in this fashion. An initial node restart requires restarting each ndbd process with the --initial option.

A system restart requires a complete shutdown and restart of the entire cluster. An initial system restart requires taking a backup of the cluster, wiping the cluster file system after shutdown, and then restoring from the backup following the restart.

In any cluster restart, all of the cluster's management servers must be restarted for them to read the updated configuration parameter values.

![](_page_110_Picture_4.jpeg)

# **Important**

Values for numeric cluster parameters can generally be increased without any problems, although it is advisable to do so progressively, making such adjustments in relatively small increments. Many of these can be increased online, using a rolling restart.

However, decreasing the values of such parameters—whether this is done using a node restart, node initial restart, or even a complete system restart of the cluster—is not to be undertaken lightly; it is recommended that you do so only after careful planning and testing. This is especially true with regard to those parameters that relate to memory usage and disk space, such as [MaxNoOfTables](#page-180-0), [MaxNoOfOrderedIndexes](#page-181-0), and [MaxNoOfUniqueHashIndexes](#page-181-1). In addition, it is the generally the case that configuration parameters relating to memory and disk usage can be raised using a simple node restart, but they require an initial node restart to be lowered.

Because some of these parameters can be used for configuring more than one type of cluster node, they may appear in more than one of the tables.

![](_page_110_Picture_9.jpeg)

# **Note**

4294967039 often appears as a maximum value in these tables. This value is defined in the [NDBCLUSTER](#page-50-0) sources as MAX\_INT\_RNIL and is equal to 0xFFFFFEFF, or 2 <sup>32</sup> − 2<sup>8</sup> − 1.