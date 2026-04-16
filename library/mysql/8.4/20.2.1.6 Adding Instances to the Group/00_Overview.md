---
source: MySQL 8.4 Reference
title: 00_Overview
---

At this point, the group has one member in it, server s1, which has some data in it. It is now time to expand the group by adding the other two servers configured previously.

### **Adding a Second Instance**

In order to add a second instance, server s2, first create the configuration file for it. The configuration is similar to the one used for server s1, except for things such as the server\_id.

```
[mysqld]
#
# Disable other storage engines
#
disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"
#
# Replication configuration parameters
#
server_id=2
gtid_mode=ON
enforce_gtid_consistency=ON
#
# Group Replication configuration
#
plugin_load_add='group_replication.so'
group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
group_replication_start_on_boot=off
group_replication_local_address= "s2:33061"
group_replication_group_seeds= "s1:33061,s2:33061,s3:33061"
group_replication_bootstrap_group= off
```

Similar to the procedure for server s1, with the option file in place you launch the server. Then configure the distributed recovery credentials as follows. The operations are the same as used when setting up server s1 as the user is shared within the group. This member needs to have the same replication user configured in [Section 20.2.1.3, "User Credentials For Distributed Recovery".](#page-27-0) If you are relying on distributed recovery to configure the user on all members, when s2 connects to the seed s1 the replication user is replicated or cloned to s1. If you did not have binary logging enabled when you configured the user credentials on s1, and a remote cloning operation is not used for state transfer, you must create the replication user on s2. In this case, connect to s2 and issue:

```
SET SQL_LOG_BIN=0;
CREATE USER rpl_user@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';
GRANT CONNECTION_ADMIN ON *.* TO rpl_user@'%';
GRANT BACKUP_ADMIN ON *.* TO rpl_user@'%';
GRANT GROUP_REPLICATION_STREAM ON *.* TO rpl_user@'%';
FLUSH PRIVILEGES;
SET SQL_LOG_BIN=1;
```

If you are providing user credentials using a CHANGE REPLICATION SOURCE TO, issue the following statement after that:

```
CHANGE REPLICATION SOURCE TO SOURCE_USER='rpl_user', SOURCE_PASSWORD='password' \
 FOR CHANNEL 'group_replication_recovery';
```

![](_page_31_Picture_5.jpeg)

#### **Tip**

If you are using the caching SHA-2 authentication plugin (the default), see [Replication User With The Caching SHA-2 Authentication Plugin.](#page-85-1)

If necessary, install the Group Replication plugin, see [Section 20.2.1.4, "Launching Group Replication".](#page-28-0)

Start Group Replication and s2 starts the process of joining the group.

```
mysql> START GROUP_REPLICATION;
```

If you are providing user credentials for distributed recovery as part of START GROUP\_REPLICATION, you can do so like this:

```
mysql> START GROUP_REPLICATION USER='rpl_user', PASSWORD='password';
```

Unlike the previous steps that were the same as those executed on s1, here there is a difference in that you do not need to bootstrap the group because the group already exists. In other words on s2 [group\\_replication\\_bootstrap\\_group](#page-131-0) is set to OFF, and you do not issue SET GLOBAL group\_replication\_bootstrap\_group=ON; before starting Group Replication, because the group has already been created and bootstrapped by server s1. At this point server s2 only needs to be added to the already existing group.

![](_page_31_Picture_14.jpeg)

#### **Tip**

When Group Replication starts successfully and the server joins the group it checks the super\_read\_only variable. By setting super\_read\_only to ON in the member's configuration file, you can ensure that servers which fail when starting Group Replication for any reason do not accept transactions. If the server should join the group as a read/write instance, for example as the primary in a single-primary group or as a member of a multi-primary group, when super\_read\_only is set to ON then it is set to OFF upon joining the group.

Checking the performance\_schema.replication\_group\_members table again shows that there are now two ONLINE servers in the group.

```
mysql> SELECT * FROM performance_schema.replication_group_members;
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
| CHANNEL_NAME | MEMBER_ID | MEMBER_HOST | MEMBER_PORT | MEMBER_STATE | MEMBER_ROLE | MEMBER_VERSION | MEMBER_COMMUNICATION_STACK |
```

```
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
| group_replication_applier | 395409e1-6dfa-11e6-970b-00212844f856 | s1 | 3306 | ONLINE | PRIMARY | 8.4.8 | XCom |
| group_replication_applier | ac39f1e6-6dfa-11e6-a69d-00212844f856 | s2 | 3306 | ONLINE | SECONDARY | 8.4.8 | XCom |
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
```

When s2 attempted to join the group, [Section 20.5.4, "Distributed Recovery"](#page-58-0) ensured that s2 applied the same transactions which s1 had applied. Once this process completed, s2 could join the group as a member, and at this point it is marked as ONLINE. In other words it must have already caught up with server s1 automatically. Once s2 is ONLINE, it then begins to process transactions with the group. Verify that s2 has indeed synchronized with server s1 as follows.

```
mysql> SHOW DATABASES LIKE 'test';
+-----------------+
| Database (test) |
+-----------------+
| test |
+-----------------+
mysql> SELECT * FROM test.t1;
+----+------+
| c1 | c2 |
+----+------+
| 1 | Luis |
+----+------+
mysql> SHOW BINLOG EVENTS;
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name | Pos | Event_type | Server_id | End_log_pos | Info |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| binlog.000001 | 4 | Format_desc | 2 | 123 | Server ver: 8.4.8-log, Binlog ver: 4 |
| binlog.000001 | 123 | Previous_gtids | 2 | 150 | |
| binlog.000001 | 150 | Gtid | 1 | 211 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:1' |
| binlog.000001 | 211 | Query | 1 | 270 | BEGIN |
| binlog.000001 | 270 | View_change | 1 | 369 | view_id=14724832985483517:1 |
| binlog.000001 | 369 | Query | 1 | 434 | COMMIT |
| binlog.000001 | 434 | Gtid | 1 | 495 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:2' |
| binlog.000001 | 495 | Query | 1 | 585 | CREATE DATABASE test |
| binlog.000001 | 585 | Gtid | 1 | 646 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:3' |
| binlog.000001 | 646 | Query | 1 | 770 | use `test`; CREATE TABLE t1 (c1 INT PRIMARY KEY, c2 TEXT NOT NULL) |
| binlog.000001 | 770 | Gtid | 1 | 831 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:4' |
| binlog.000001 | 831 | Query | 1 | 890 | BEGIN |
| binlog.000001 | 890 | Table_map | 1 | 933 | table_id: 108 (test.t1) |
| binlog.000001 | 933 | Write_rows | 1 | 975 | table_id: 108 flags: STMT_END_F |
| binlog.000001 | 975 | Xid | 1 | 1002 | COMMIT /* xid=30 */ |
| binlog.000001 | 1002 | Gtid | 1 | 1063 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:5' |
| binlog.000001 | 1063 | Query | 1 | 1122 | BEGIN |
| binlog.000001 | 1122 | View_change | 1 | 1261 | view_id=14724832985483517:2 |
| binlog.000001 | 1261 | Query | 1 | 1326 | COMMIT |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
```

As seen above, the second server has been added to the group and it has replicated the changes from server s1 automatically. In other words, the transactions applied on s1 up to the point in time that s2 joined the group have been replicated to s2.

### **Adding Additional Instances**

Adding additional instances to the group is essentially the same sequence of steps as adding the second server, except that the configuration has to be changed as it had to be for server s2. To summarise the required operations:

1. Create the configuration file.

```
[mysqld]
#
# Disable other storage engines
#
disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"
```

```
#
# Replication configuration parameters
#
server_id=3
gtid_mode=ON
enforce_gtid_consistency=ON
#
# Group Replication configuration
#
plugin_load_add='group_replication.so'
group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
group_replication_start_on_boot=off
group_replication_local_address= "s3:33061"
group_replication_group_seeds= "s1:33061,s2:33061,s3:33061"
group_replication_bootstrap_group= off
```

2. Start the server and connect to it. Create the replication user for distributed recovery.

```
SET SQL_LOG_BIN=0;
CREATE USER rpl_user@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';
GRANT CONNECTION_ADMIN ON *.* TO rpl_user@'%';
GRANT BACKUP_ADMIN ON *.* TO rpl_user@'%';
GRANT GROUP_REPLICATION_STREAM ON *.* TO rpl_user@'%';
FLUSH PRIVILEGES;
SET SQL_LOG_BIN=1;
```

If you are providing user credentials using a CHANGE REPLICATION SOURCE TO statement, issue the following statement after that:

```
mysql> CHANGE REPLICATION SOURCE TO SOURCE_USER='rpl_user',
 -> SOURCE_PASSWORD='password'
 -> FOR CHANNEL 'group_replication_recovery';
```

3. Install the Group Replication plugin if necessary, like this:

```
mysql> INSTALL PLUGIN group_replication SONAME 'group_replication.so';
```

4. Start Group Replication:

```
mysql> START GROUP_REPLICATION;
```

If you are providing user credentials for distributed recovery in the START GROUP\_REPLICATION statement, you can do so like this:

```
mysql> START GROUP_REPLICATION USER='rpl_user', PASSWORD='password';
```

At this point server s3 is booted and running, has joined the group and caught up with the other servers in the group. Consulting the performance\_schema.replication\_group\_members table again confirms this is the case.

```
mysql> SELECT * FROM performance_schema.replication_group_members;
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
| CHANNEL_NAME | MEMBER_ID | MEMBER_HOST | MEMBER_PORT | MEMBER_STATE | MEMBER_ROLE | MEMBER_VERSION | MEMBER_COMMUNICATION_STACK |
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
| group_replication_applier | 395409e1-6dfa-11e6-970b-00212844f856 | s1 | 3306 | ONLINE | PRIMARY | 8.4.8 | XCom |
| group_replication_applier | 7eb217ff-6df3-11e6-966c-00212844f856 | s3 | 3306 | ONLINE | SECONDARY | 8.4.8 | XCom |
| group_replication_applier | ac39f1e6-6dfa-11e6-a69d-00212844f856 | s2 | 3306 | ONLINE | SECONDARY | 8.4.8 | XCom |
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
```

Issuing this same query on server s2 or server s1 yields the same result. Also, you can verify that server s3 has caught up:

```
mysql> SHOW DATABASES LIKE 'test';
+-----------------+
| Database (test) |
+-----------------+
| test |
```

```
+-----------------+
mysql> SELECT * FROM test.t1;
+----+------+
| c1 | c2 |
+----+------+
| 1 | Luis |
+----+------+
mysql> SHOW BINLOG EVENTS;
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name | Pos | Event_type | Server_id | End_log_pos | Info |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| binlog.000001 | 4 | Format_desc | 3 | 123 | Server ver: 8.4.8-log, Binlog ver: 4 |
| binlog.000001 | 123 | Previous_gtids | 3 | 150 | |
| binlog.000001 | 150 | Gtid | 1 | 211 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:1' |
| binlog.000001 | 211 | Query | 1 | 270 | BEGIN |
| binlog.000001 | 270 | View_change | 1 | 369 | view_id=14724832985483517:1 |
| binlog.000001 | 369 | Query | 1 | 434 | COMMIT |
| binlog.000001 | 434 | Gtid | 1 | 495 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:2' |
| binlog.000001 | 495 | Query | 1 | 585 | CREATE DATABASE test |
| binlog.000001 | 585 | Gtid | 1 | 646 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:3' |
| binlog.000001 | 646 | Query | 1 | 770 | use `test`; CREATE TABLE t1 (c1 INT PRIMARY KEY, c2 TEXT NOT NULL) |
| binlog.000001 | 770 | Gtid | 1 | 831 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:4' |
| binlog.000001 | 831 | Query | 1 | 890 | BEGIN |
| binlog.000001 | 890 | Table_map | 1 | 933 | table_id: 108 (test.t1) |
| binlog.000001 | 933 | Write_rows | 1 | 975 | table_id: 108 flags: STMT_END_F |
| binlog.000001 | 975 | Xid | 1 | 1002 | COMMIT /* xid=29 */ |
| binlog.000001 | 1002 | Gtid | 1 | 1063 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:5' |
| binlog.000001 | 1063 | Query | 1 | 1122 | BEGIN |
| binlog.000001 | 1122 | View_change | 1 | 1261 | view_id=14724832985483517:2 |
| binlog.000001 | 1261 | Query | 1 | 1326 | COMMIT |
| binlog.000001 | 1326 | Gtid | 1 | 1387 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:6' |
| binlog.000001 | 1387 | Query | 1 | 1446 | BEGIN |
| binlog.000001 | 1446 | View_change | 1 | 1585 | view_id=14724832985483517:3 |
| binlog.000001 | 1585 | Query | 1 | 1650 | COMMIT |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
```

# <span id="page-34-0"></span>**20.2.2 Deploying Group Replication Locally**

The most common way to deploy Group Replication is using multiple server instances, to provide high availability. It is also possible to deploy Group Replication locally, for example for testing purposes. This section explains how you can deploy Group Replication locally.

![](_page_34_Picture_4.jpeg)

#### **Important**

Group Replication is usually deployed on multiple hosts because this ensures that high-availability is provided. The instructions in this section are not suitable for production deployments because all MySQL server instances are running on the same single host. In the event of failure of this host, the whole group fails. Therefore this information should be used for testing purposes and it should not be used in a production environments.

This section explains how to create a replication group with three MySQL Server instances on one physical machine. This means that three data directories are needed, one per server instance, and that you need to configure each instance independently. This - procedure assumes that MySQL Server was downloaded and unpacked - into the directory named mysql-8.4. Each MySQL server instance requires a specific data directory. Create a directory named data, then in that directory create a subdirectory for each server instance, for example s1, s2 and s3, and initialize each one.

```
mysql-8.4/bin/mysqld --initialize-insecure --basedir=$PWD/mysql-8.4 --datadir=$PWD/data/s1
mysql-8.4/bin/mysqld --initialize-insecure --basedir=$PWD/mysql-8.4 --datadir=$PWD/data/s2
mysql-8.4/bin/mysqld --initialize-insecure --basedir=$PWD/mysql-8.4 --datadir=$PWD/data/s3
```

Inside data/s1, data/s2, data/s3 is an initialized data directory, containing the mysql system database and related tables and much more. To learn more about the initialization procedure, see Section 2.9.1, "Initializing the Data Directory".

![](_page_35_Picture_1.jpeg)

#### **Warning**

Do not use -initialize-insecure in production environments, it is only used here to simplify the tutorial. For more information on security settings, see [Section 20.6, "Group Replication Security".](#page-79-0)

# **Configuration of Local Group Replication Members**

When you are following [Section 20.2.1.2, "Configuring an Instance for Group Replication"](#page-23-1), you need to add configuration for the data directories added in the previous section. For example:

```
[mysqld]
# server configuration
datadir=<full_path_to_data>/data/s1
basedir=<full_path_to_bin>/mysql-8.4/
port=24801
socket=<full_path_to_sock_dir>/s1.sock
```

These settings configure MySQL server to use the data directory created earlier and which port the server should open and start listening for incoming connections.

![](_page_35_Picture_8.jpeg)

#### **Note**

The non-default port of 24801 is used because in this tutorial the three server instances use the same hostname. In a setup with three different machines this would not be required.

Group Replication requires a network connection between the members, which means that each member must be able to resolve the network address of all of the other members. For example in this tutorial all three instances run on one machine, so to ensure that the members can contact each other you could add a line to the option file such as report\_host=127.0.0.1.

Then each member needs to be able to connect to the other members on their [group\\_replication\\_local\\_address](#page-148-0). For example in the option file of member s1 add:

```
group_replication_local_address= "127.0.0.1:24901"
group_replication_group_seeds= "127.0.0.1:24901,127.0.0.1:24902,127.0.0.1:24903"
```

This configures s1 to use port 24901 for internal group communication with seed members. For each server instance you want to add to the group, make these changes in the option file of the member. For each member you must ensure a unique address is specified, so use a unique port per instance for [group\\_replication\\_local\\_address](#page-148-0). Usually you want all members to be able to serve as seeds for members that are joining the group and have not got the transactions processed by the group. In this case, add all of the ports to [group\\_replication\\_group\\_seeds](#page-145-1) as shown above.

The remaining steps of [Section 20.2.1, "Deploying Group Replication in Single-Primary Mode"](#page-22-1) apply equally to a group which you have deployed locally in this way.

# <span id="page-35-0"></span>**20.3 Requirements and Limitations**

This section lists and explains the requirements and limitations of Group Replication.

# <span id="page-35-1"></span>**20.3.1 Group Replication Requirements**

- [Infrastructure](#page-36-0)
- [Server Instance Configuration](#page-36-1)

Server instances that you want to use for Group Replication must satisfy the following requirements.

# <span id="page-36-0"></span>**Infrastructure**

• **InnoDB Storage Engine.** Data must be stored in the InnoDB transactional storage engine. Transactions are executed optimistically and then, at commit time, are checked for conflicts. If there are conflicts, in order to maintain consistency across the group, some transactions are rolled back. This means that a transactional storage engine is required. Moreover, InnoDB provides some additional functionality that enables better management and handling of conflicts when operating together with Group Replication. The use of other storage engines, including the temporary MEMORY storage engine, might cause errors in Group Replication. Convert any tables in other storage engines to use InnoDB before using the instance with Group Replication. You can prevent the use of other storage engines by setting the disabled\_storage\_engines system variable on group members, for example:

disabled\_storage\_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"

- **Primary Keys.** Every table that is to be replicated by the group must have a defined primary key, or primary key equivalent where the equivalent is a non-null unique key. Such keys are required as a unique identifier for every row within a table, enabling the system to determine which transactions conflict by identifying exactly which rows each transaction has modified. Group Replication has its own built-in set of checks for primary keys or primary key equivalents, and does not use the checks carried out by the sql\_require\_primary\_key system variable. You may set sql\_require\_primary\_key=ON for a server instance where Group Replication is running, and you may set the REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option of the CHANGE REPLICATION SOURCE TO statement to ON for a Group Replication channel. However, be aware that you might find some transactions that are permitted under Group Replication's built-in checks are not permitted under the checks carried out when you set sql\_require\_primary\_key=ON or REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK=ON.
- **Network Performance.** MySQL Group Replication is designed to be deployed in a cluster environment where server instances are very close to each other. The performance and stability of a group can be impacted by both network latency and network bandwidth. Bi-directional communication must be maintained at all times between all group members. If either inbound or outbound communication is blocked for a server instance (for example, by a firewall, or by connectivity issues), the member cannot function in the group, and the group members (including the member with issues) might not be able to report the correct member status for the affected server instance.

You can use a network infrastructure based on IPv4, IPv6, or a mix of the two, for TCP communication between remote Group Replication servers. There is also nothing preventing Group Replication from operating over a virtual private network (VPN).

Where Group Replication server instances are co-located and share a local group communication engine (XCom) instance, a dedicated input channel with lower overhead is used for communication where possible instead of the TCP socket. For certain Group Replication tasks that require communication between remote XCom instances, such as joining a group, the TCP network is still used, so network performance influences the group's performance.

## <span id="page-36-1"></span>**Server Instance Configuration**

The following options must be configured as shown on server instances that are members of a group.

- **Unique Server Identifier.** Use the server\_id system variable to configure the server with a unique server ID, as required for all servers in replication topologies. The server ID must be a positive integer between 1 and (232)−1, and it must be different from every other server ID in use by any other server in the replication topology.
- **Binary Log Active.** In MySQL 8.4, binary logging is enabled by default. You can optionally specify the names of the binary log files using --log-bin[=log\_file\_name]. Group Replication

replicates the binary log's contents, therefore the binary log needs to be on for it to operate. See Section 7.4.4, "The Binary Log".

- **Replica Updates Logged.** Set log\_replica\_updates=ON if it is not already enabled. (In MySQL 8.4, this is the default.) Group members need to log transactions that are received from their donors at joining time and applied through the replication applier, and to log all transactions that they receive and apply from the group. This enables Group Replication to carry out distributed recovery by state transfer from an existing group member's binary log.
- **Binary Log Row Format.** Set binlog\_format=ROW if necessary; in MySQL 8.4, this is the default. Group Replication relies on the row-based replication format to propagate changes consistently among the servers in the group, and extract the necessary information to detect conflicts among transactions that execute concurrently in different servers in the group. The setting for REQUIRE\_ROW\_FORMAT is automatically added to Group Replication's channels to enforce the use of row-based replication when the transactions are applied. See Section 19.2.1, "Replication Formats" and Section 19.3.3, "Replication Privilege Checks".
- **Global Transaction Identifiers On.** Set gtid\_mode=ON and enforce\_gtid\_consistency=ON. These settings are not the defaults. GTID-based replication is required for Group Replication, which uses global transaction identifiers to track the transactions that have been committed on every server instance in the group. See Section 19.1.3, "Replication with Global Transaction Identifiers".

In addition, if you need to set the value of gtid\_purged, you must do so while Group Replication is not running.

• **Default Table Encryption.** Set default\_table\_encryption to the same value on all group members. Default schema and tablespace encryption can be either enabled (ON) or disabled (OFF, the default) as long as the setting is the same on all members.

The value of default\_table\_encryption cannot be changed while Group Replication is running.

- **Lower Case Table Names.** Set lower\_case\_table\_names to the same value on all group members. A setting of 1 is correct for the use of the InnoDB storage engine, which is required for Group Replication. Note that this setting is not the default on all platforms.
- **Multithreaded Appliers.** Group Replication members can be configured as multithreaded replicas, enabling transactions to be applied in parallel. All replicas are configured as multithreaded by default. A nonzero value for replica\_parallel\_workers enables the multithreaded applier on the member. The default is 4 parallel applier threads; up to 1024 parallel applier threads can be specified. For a multithreaded replica, the following is also required:

replica\_preserve\_commit\_order=ON This setting is required to ensure that the final commit of parallel transactions is in the same order as the original transactions. Group Replication relies on consistency mechanisms built around the guarantee that all participating members receive and apply committed transactions in the same order.

Setting replica\_parallel\_workers=0 disables parallel execution and gives the replica a single applier thread and no coordinator thread. With that setting, the replica\_parallel\_type and replica\_preserve\_commit\_order options have no effect and are ignored. If parallel execution is disabled when GTIDs are in use on a replica, the replica actually uses one parallel worker, to take advantage of the method for retrying transactions without accessing the file positions. However, this behavior does not change anything for the user.

• **Detached XA transactions.** MySQL 8.4 and later supports detached XA transactions. A detached transaction is one which, once prepared, is no longer connected to the current session. This happens automatically as part of executing XA PREPARE. The prepared XA transaction can be committed or rolled back by another connection, and the current session can then initiate another XA transaction or local transaction without waiting for the transaction that was just prepared to complete. When detached XA transaction support is enabled (xa\_detach\_on\_prepare = ON) it is possible for any connection to this server to list (using XA RECOVER), roll back, or commit any prepared XA transaction. In addition, you cannot use temporary tables within detached XA transactions.

You can disable support for detached XA transactions by setting xa\_detach\_on\_prepare to OFF, but this is not recommended. In particular, if this server is being set up as an instance in MySQL group replication, you should leave this variable set to its default value (ON).

See Section 15.3.8.2, "XA Transaction States", for more information.

# <span id="page-38-0"></span>**20.3.2 Group Replication Limitations**

- [Limit on Group Size](#page-39-0)
- [Limits on Transaction Size](#page-40-1)

The following known limitations exist for Group Replication. Note that the limitations and issues described for multi-primary mode groups can also apply in single-primary mode clusters during a failover event, while the newly elected primary flushes out its applier queue from the old primary.

![](_page_38_Picture_8.jpeg)

#### **Tip**

Group Replication is built on GTID based replication, therefore you should also be aware of Section 19.1.3.7, "Restrictions on Replication with GTIDs".

- **--upgrade=MINIMAL option.** Group Replication cannot be started following a MySQL Server upgrade that uses the MINIMAL option (--upgrade=MINIMAL), which does not upgrade system tables on which the replication internals depend.
- **Gap Locks.** Group Replication's certification process for concurrent transactions does not take into account gap locks, as information about gap locks is not available outside of InnoDB. See Gap Locks for more information.

![](_page_38_Picture_13.jpeg)

### **Note**

For a group in multi-primary mode, unless you rely on REPEATABLE READ semantics in your applications, we recommend using the READ COMMITTED isolation level with Group Replication. InnoDB does not use gap locks in READ COMMITTED, which aligns the local conflict detection within InnoDB with the distributed conflict detection performed by Group Replication. For a group in single-primary mode, only the primary accepts writes, so the READ COMMITTED isolation level is not important to Group Replication.

- **Table Locks and Named Locks.** The certification process does not take into account table locks (see Section 15.3.6, "LOCK TABLES and UNLOCK TABLES Statements") or named locks (see GET\_LOCK()).
- **Binary Log Checksums.** Group Replication in MySQL 8.4 supports checksums, so group members may use the default setting binlog\_checksum=CRC32. The setting for binlog\_checksum does not have to be the same for all members of a group.

When checksums are available, Group Replication does not use them to verify incoming events on the group\_replication\_applier channel, because events are written to that relay log from multiple sources and before they are actually written to the originating server's binary log, which is when a checksum is generated. Checksums are used to verify the integrity of events on the group\_replication\_recovery channel and on any other replication channels on group members.

- **SERIALIZABLE Isolation Level.** SERIALIZABLE isolation level is not supported in multiprimary groups by default. Setting a transaction isolation level to SERIALIZABLE configures Group Replication to refuse to commit the transaction.
- **Concurrent DDL versus DML Operations.** Concurrent data definition statements and data manipulation statements executing against the same object but on different servers is not supported when using multi-primary mode. During execution of Data Definition Language (DDL) statements on an object, executing concurrent Data Manipulation Language (DML) on the same object but on a different server instance has the risk of conflicting DDL executing on different instances not being detected.
- **Foreign Keys with Cascading Constraints.** Multi-primary mode groups (members all configured with [group\\_replication\\_single\\_primary\\_mode=OFF](#page-162-0)) do not support tables with multi-level foreign key dependencies, specifically tables that have defined CASCADING foreign key constraints. This is because foreign key constraints that result in cascading operations executed by a multi-primary mode group can result in undetected conflicts and lead to inconsistent data across the members of the group. Therefore we recommend setting [group\\_replication\\_enforce\\_update\\_everywhere\\_checks=ON](#page-137-0) on server instances used in multi-primary mode groups to avoid undetected conflicts.

In single-primary mode this is not a problem as it does not allow concurrent writes to multiple members of the group and thus there is no risk of undetected conflicts.

- **Multi-primary Mode Deadlock.** When a group is operating in multi-primary mode, SELECT .. FOR UPDATE statements can result in a deadlock. This is because the lock is not shared across the members of the group, therefore the expectation for such a statement might not be reached.
- **Replication Filters.** Global replication filters cannot be used on a MySQL server instance that is configured for Group Replication, because filtering transactions on some servers would make the group unable to reach agreement on a consistent state. Channel specific replication filters can be used on replication channels that are not directly involved with Group Replication, such as where a group member also acts as a replica to a source that is outside the group. They cannot be used on the group\_replication\_applier or group\_replication\_recovery channels.
- **Encrypted Connections.** Support for the TLSv1.3 protocol is available in MySQL, provided that it was compiled using OpenSSL 1.1.1 or higher. Group Replication supports TLSv1.3, where it can be used for group communication connections and distributed recovery connections.

```
group_replication_recovery_tls_version and
group_replication_recovery_tls_ciphersuites can be used to configure client support
for any selection of ciphersuites, including only non-default ciphersuites if desired. See Section 8.3.2,
"Encrypted Connection TLS Protocols and Ciphers".
```

• **Cloning Operations.** Group Replication initiates and manages cloning operations for distributed recovery, but group members that have been set up to support cloning may also participate in cloning operations that a user initiates manually. You can initiate a cloning operation manually if the operation involves a group member on which Group Replication is running, provided that the cloning operation does not remove and replace the data on the recipient. The statement to initiate the cloning operation must therefore include the DATA DIRECTORY clause if Group Replication is running. See [Cloning for Other Purposes.](#page-64-0)

## <span id="page-39-0"></span>**Limit on Group Size**

The maximum number of MySQL servers that can be members of a single replication group is 9. If further members attempt to join the group, their request is refused. This limit has been identified from testing and benchmarking as a safe boundary where the group performs reliably on a stable local area network.

# <span id="page-40-1"></span>**Limits on Transaction Size**

If an individual transaction results in message contents which are large enough that the message cannot be copied between group members over the network within a 5-second window, members can be suspected of having failed, and then expelled, just because they are busy processing the transaction. Large transactions can also cause the system to slow due to problems with memory allocation. To avoid these issues use the following mitigations:

- If unnecessary expulsions occur due to large messages, use the system variable [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) to allow additional time before a member under suspicion of having failed is expelled. You can allow up to an hour after the initial 5-second detection period before a suspect member is expelled from the group. An additional 5 seconds is allowed by default.
- Where possible, try and limit the size of your transactions before they are handled by Group Replication. For example, split up files used with LOAD DATA into smaller chunks.
- Use the system variable [group\\_replication\\_transaction\\_size\\_limit](#page-165-0) to specify a maximum transaction size that the group accepts. The default maximum transaction size is 150000000 bytes (approximately 143 MB); transactions above this size are rolled back and are not sent to Group Replication's Group Communication System (GCS) for distribution to the group. Adjust the value of this variable depending on the maximum message size that you need the group to tolerate, bearing in mind that the time taken to process a transaction is proportional to its size.
- Use the system variable [group\\_replication\\_compression\\_threshold](#page-135-0) to specify a message size above which compression is applied. This system variable defaults to 1000000 bytes (1 MB), so large messages are automatically compressed. Compression is carried out by Group Replication's Group Communication System (GCS) when it receives a message that was permitted by the [group\\_replication\\_transaction\\_size\\_limit](#page-165-0) setting but exceeds the [group\\_replication\\_compression\\_threshold](#page-135-0) setting. For more information, see [Section 20.7.4, "Message Compression"](#page-94-0).
- Use the system variable [group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0) to specify a message size above which messages are fragmented. This system variable defaults to 10485760 bytes (10 MiB), so large messages are automatically fragmented. GCS carries out fragmentation after compression if the compressed message still exceeds the [group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0) limit. For more information, see [Section 20.7.5, "Message Fragmentation".](#page-96-0)

The maximum transaction size, message compression, and message fragmentation can all be deactivated by specifying a zero value for the relevant system variable. If you have deactivated all these safeguards, the upper size limit for a message that can be handled by the applier thread on a member of a replication group is the value of the member's replica\_max\_allowed\_packet system variable, which has a default and maximum value of 1073741824 bytes (1 GB). A message that exceeds this limit fails when the receiving member attempts to handle it. The upper size limit for a message that a group member can originate and attempt to transmit to the group is 4294967295 bytes (approximately 4 GB). This is a hard limit on the packet size that is accepted by the group communication engine for Group Replication (XCom, a Paxos variant), which receives messages after GCS has handled them. A message that exceeds this limit fails when the originating member attempts to broadcast it.

# <span id="page-40-0"></span>**20.4 Monitoring Group Replication**

You can use the MySQL Performance Schema to monitor Group Replication. These Performance Schema tables display information specific to Group Replication:

- replication\_group\_member\_stats: See [Section 20.4.4, "The replication\\_group\\_member\\_stats](#page-44-0) [Table"](#page-44-0).
- replication\_group\_members: See [Section 20.4.3, "The replication\\_group\\_members Table"](#page-43-0).

• replication\_group\_communication\_information: See Section 29.12.11.10, "The replication\_group\_communication\_information Table".

These Performance Schema replication tables also show information relating to Group Replication:

- replication\_connection\_status shows information regarding Group Replication, such as transactions received from the group and queued in the applier queue (relay log).
- replication\_applier\_status shows the states of channels and threads relating to Group Replication. These can also be used to monitor what individual worker threads are doing.

Replication channels created by the Group Replication plugin are listed here:

- group\_replication\_recovery: Used for replication changes related to distributed recovery.
- group\_replication\_applier: Used for the incoming changes from the group, to apply transactions coming directly from the group.

For information about system variables affecting Group Replication, see [Section 20.9.1, "Group](#page-125-0) [Replication System Variables"](#page-125-0). See [Section 20.9.2, "Group Replication Status Variables"](#page-167-0), for status variables providing information about Group Replication.

Messages relating to Group Replication lifecycle events other than errors are classified as system messages; these are always written to the replication group member' error log. You can use this information to review the history of a given server's membership in a replication group.

Some lifecycle events that affect the whole group are logged on every group member, such as a new member entering ONLINE status in the group or a primary election. Other events are logged only on the member where they take place, such as super read only mode being enabled or disabled on the member, or the member leaving the group. A number of lifecycle events that can indicate an issue if they occur frequently are logged as warning messages, including a member becoming unreachable and then reachable again, and a member starting distributed recovery by state transfer from the binary log or by a remote cloning operation.

![](_page_41_Picture_11.jpeg)

### **Note**

If you are monitoring one or more secondary instances using mysqladmin, you should be aware that a FLUSH STATUS statement executed by this utility creates a GTID event on the local instance which may impact future group operations.

# <span id="page-41-0"></span>**20.4.1 GTIDs and Group Replication**

Group Replication uses GTIDs (global transaction identifiers) to track exactly which transactions have been committed on every server instance. The settings gtid\_mode=ON and enforce\_gtid\_consistency=ON are required on all group members. Incoming transactions from clients are assigned a GTID by the group member that receives them. Any replicated transactions that are received by group members on asynchronous replication channels from source servers outside the group retain the GTIDs that they have when they arrive on the group member.

The GTIDs that are assigned to incoming transactions from clients use the group name specified by the [group\\_replication\\_group\\_name](#page-145-0) system variable as the UUID part of the identifier, rather than the server UUID of the individual group member that received the transaction. All the transactions received directly by the group can therefore be identified and are grouped together in GTID sets, and it does not matter which member originally received them. Each group member has a block of consecutive GTIDs reserved for its use, and when these are consumed it reserves more. The [group\\_replication\\_gtid\\_assignment\\_block\\_size](#page-146-0) system variable sets the size of the blocks, with a default of 1 million GTIDs in each block.

View change events (View\_change\_log\_event), which are generated by the group itself when a new member joins, are given GTIDs when they are recorded in the binary log. By default, the GTIDs for these events also use the group name specified by the [group\\_replication\\_group\\_name](#page-145-0) system variable as the UUID part of the identifier. You can set the Group Replication system variable [group\\_replication\\_view\\_change\\_uuid](#page-166-0) to use an alternative UUID in the GTIDs for view change events, so that they are easy to distinguish from transactions received by the group from clients. This can be useful if your setup allows for failover between groups, and you need to identify and discard transactions that were specific to the backup group. The alternative UUID must be different from the server UUIDs of the members. It must also be different from any UUIDs in the GTIDs applied to anonymous transactions using the ASSIGN\_GTIDS\_TO\_ANONYMOUS\_TRANSACTIONS option of the CHANGE REPLICATION SOURCE TO statement.

GTID\_ONLY=1, REQUIRE\_ROW\_FORMAT = 1, and SOURCE\_AUTO\_POSITION = 1 are applied for the Group Replication channels group\_replication\_applier and group\_replication\_recovery. The settings are made automatically on the Group Replication channels when they are created, or when a member server in a replication group is upgraded. These options are normally set using a CHANGE REPLICATION SOURCE TO statement, but note that you cannot disable them for a Group Replication channel. With these options set, the group member does not persist file names and file positions in the replication metadata repositories for these channels. GTID auto-positioning and GTID auto-skip are used to locate the correct receiver and applier positions when necessary.

## <span id="page-42-1"></span>**Extra Transactions**

If a joining member has transactions in its GTID set that are not present on the existing members of the group, it is not allowed to complete the distributed recovery process, and cannot join the group. If a remote cloning operation was carried out, these transactions would be deleted and lost, because the data directory on the joining member is erased. If state transfer from a donor's binary log was carried out, these transactions could conflict with the group's transactions.

Extra transactions might be present on a member if an administrative transaction is carried out on the instance while Group Replication is stopped. To avoid introducing new transactions in that way, always set the value of the sql\_log\_bin system variable to OFF before issuing administrative statements, and back to ON afterwards:

```
SET SQL_LOG_BIN=0;
<administrator action>
SET SQL_LOG_BIN=1;
```

Setting this system variable to OFF means that the transactions that occur from that point until you set it back to ON are not written to the binary log and do not have GTIDs assigned to them.

If an extra transaction is present on a joining member, check the binary log for the affected server to see what the extra transaction actually contains. The safest method to reconcile the joining member's data and GTID set with the members currently in the group is to use MySQL's cloning functionality to transfer the content from a server in the group to the affected server. For instructions to do this, see Section 7.6.7.3, "Cloning Remote Data". If the transaction is required, rerun it after the member has successfully rejoined.

# <span id="page-42-0"></span>**20.4.2 Group Replication Server States**

The state of a Group Replication group member shows its current role in the group. The Performance Schema table replication\_group\_members shows the state for each member in a group. If the group is fully functional and all members are communicating properly, all members report the same state for all other members. However, a member that has left the group or is part of a network partition cannot report accurate information on the other servers. In this situation, the member does not attempt to guess the status of the other servers, and instead reports them as unreachable.

A group member can be in the following states:

ONLINE The server is an active member of a group and in a fully functioning state. Other group members can connect to it, as can clients if applicable. A member is only fully synchronized with the group, and participating in it, when it is in the ONLINE state.

RECOVERING The server has joined a group and is in the process of becoming an active member. Distributed recovery is currently taking place, where the member is receiving state transfer from a donor using a remote cloning operation or the donor's binary log. This state is

For more information, see [Section 20.5.4, "Distributed Recovery"](#page-58-0).

OFFLINE The Group Replication plugin is loaded but the member does not belong to any group. This status may briefly occur while a member is joining or rejoining a group.

ERROR The member is in an error state and is not functioning correctly as a group member. A member can enter error state either while applying transactions or during the recovery phase. A member in this state does not participate in the group's transactions. For more information on possible reasons for error states, see [Section 20.7.7,](#page-98-0) ["Responses to Failure Detection and Network Partitioning".](#page-98-0)

#### Depending on the exit action set by

[group\\_replication\\_exit\\_state\\_action](#page-138-0), the member is in read-only mode (super\_read\_only=ON) and could also be in offline mode (offline\_mode=ON). Note that a server in offline mode following the OFFLINE\_MODE exit action is displayed with ERROR status, not OFFLINE. A server with the exit action ABORT\_SERVER shuts down and is removed from the view of the group. For more information, see [Section 20.7.7.4, "Exit Action"](#page-101-0).

While a member is joining or rejoining a replication group, its status can be displayed as ERROR before the group completes the compatibility checks and accepts it as a member.

UNREACHABLE The local failure detector suspects that the member cannot be contacted, because the group's messages are timing out. This can happen if a member is disconnected involuntarily, for example. If you see this status for other servers, it can also mean that the member where you query this table is part of a partition, where a subset of the group's servers can contact each other but cannot contact the other servers in the group. For more information, see [Section 20.7.8, "Handling a Network Partition and Loss of Quorum"](#page-103-0).

See [Section 20.4.3, "The replication\\_group\\_members Table"](#page-43-0) for an example of the Performance Schema table contents.

# <span id="page-43-0"></span>**20.4.3 The replication\_group\_members Table**

The performance\_schema.replication\_group\_members table is used for monitoring the status of the different server instances that are members of the group. The information in the table is updated whenever there is a view change, for example when the configuration of the group is dynamically changed when a new member joins. At that point, servers exchange some of their metadata to synchronize themselves and continue to cooperate together. The information is shared between all the server instances that are members of the replication group, so information on all the group members can be queried from any member. This table can be used to get a high level view of the state of a replication group, for example by issuing:

|              | SELECT * FROM performance_schema.replication_group_members;<br>+++++++++                                                                                                                                                                                     |  |                                                                                                      |                                                 |  |  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|------------------------------------------------------------------------------------------------------|-------------------------------------------------|--|--|
| CHANNEL_NAME | MEMBER_ID                                                                                                                                                                                                                                                    |  | MEMBER_HOST   MEMBER_PORT   MEMBER_STATE   MEMBER_ROLE   MEMBER_VERSION   MEMBER_COMMUNICATION_STACK |                                                 |  |  |
|              | +++++++++<br>  group_replication_applier   d391e9ee-2691-11ec-bf61-00059a3c7a00   example1<br>  group_replication_applier   e059ce5c-2691-11ec-8632-00059a3c7a00   example2<br>  group_replication_applier   ecd9ad06-2691-11ec-91c7-00059a3c7a00   example3 |  | <br> <br>                                                                                            | 4410   ONLINE<br>4420   ONLINE<br>4430   ONLINE |  |  |

+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+ 3 rows in set (0.0007 sec)

Based on this result we can see that the group consists of three members. Shown in the table is each member's server\_uuid, as well as the member's host name and port number, which clients use to connect to it. The MEMBER\_STATE column shows one of the [Section 20.4.2, "Group Replication](#page-42-0) [Server States",](#page-42-0) in this case it shows that all three members in this group are ONLINE, and the MEMBER\_ROLE column shows that there are two secondaries, and a single primary. Therefore this group must be running in single-primary mode. The MEMBER\_VERSION column can be useful when you are upgrading a group and are combining members running different MySQL versions. The MEMBER\_COMMUNICATION\_STACK column shows the communication stack used for the group.

For more information about the MEMBER\_HOST value and its impact on the distributed recovery process, see [Section 20.2.1.3, "User Credentials For Distributed Recovery".](#page-27-0)

# <span id="page-44-0"></span>**20.4.4 The replication\_group\_member\_stats Table**

Each member in a replication group certifies and applies transactions received by the group. Statistics regarding the certifier and applier procedures are useful to understand how the applier queue is growing, how many conflicts have been found, how many transactions were checked, which transactions are committed everywhere, and so on.

The performance\_schema.replication\_group\_member\_stats table provides group-level information related to the certification process, and also statistics for the transactions received and originated by each individual member of the replication group. The information is shared between all the server instances that are members of the replication group, so information on all the group members can be queried from any member. Note that refreshing of statistics for remote members is controlled by the message period specified in the [group\\_replication\\_flow\\_control\\_period](#page-143-0) option, so these can differ slightly from the locally collected statistics for the member where the query is made. To use this table to monitor a Group Replication member, issue the following statement:

mysql> **SELECT \* FROM performance\_schema.replication\_group\_member\_stats\G**

You can also use the following statement:

mysql> **TABLE performance\_schema.replication\_group\_member\_stats\G**

These columns are important for monitoring the performance of the members connected in the group. Suppose that one of the group's members always reports a large number of transactions in its queue compared to other members. This means that the member is delayed and is not able to keep up to date with the other members of the group. Based on this information, you could decide to either remove the member from the group, or delay the processing of transactions on the other members of the group in order to reduce the number of queued transactions. This information can also help you to decide how to adjust the flow control of the Group Replication plugin, see [Section 20.7.2, "Flow Control".](#page-91-2)

# <span id="page-44-1"></span>**20.5 Group Replication Operations**

This section explains common operations for managing groups.

# <span id="page-44-2"></span>**20.5.1 Configuring an Online Group**

You can configure an online group while Group Replication is running by using a set of functions, which rely on a group action coordinator. These functions are installed by the Group Replication plugin. This section describes how changes are made to a running group, and the available functions.

![](_page_44_Picture_15.jpeg)

#### **Important**

For the coordinator to be able to configure group wide actions on a running group, all members must have the functions installed.

To use the functions, connect to a member of the running group and invoke the function with the SELECT statement. The Group Replication plugin processes the action and its parameters and the coordinator sends it to all members which are visible to the member where you invoked the function. If the action is accepted, all members execute the action and send a termination message when completed. Once all members declare the action as finished, the invoking member returns the result to the client.

When configuring a whole group, the distributed nature of the operations means that they interact with many processes of the Group Replication plugin, and therefore you should observe the following:

**You can issue configuration operations everywhere.** If you want to make member A the new primary you do not need to invoke the operation on member A. All operations are sent and executed in a coordinated way on all group members. Also, this distributed execution of an operation has a different ramification: if the invoking member dies, any already running configuration process continues to run on other members. In the unlikely event that the invoking member dies, you can still use the monitoring features to ensure other members complete the operation successfully.

**All members must be online.** To simplify the migration or election processes and guarantee they are as fast as possible, the group must not contain any member currently in the distributed recovery process, otherwise the configuration action is rejected by the member where you issue the statement.

**No members can join a group during a configuration change.** Any member that attempts to join the group during a coordinated configuration change leaves the group and cancels its join process.

**Only one configuration at once.** A group which is executing a configuration change cannot accept any other group configuration change, because concurrent configuration operations could lead to member divergence.