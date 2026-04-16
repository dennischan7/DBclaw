---
source: MySQL 8.0 Reference
title: 00_Overview
---

There is a lot of automation built into the Group Replication plugin. Nonetheless, you might sometimes need to understand what is happening behind the scenes. This is where the instrumentation of Group Replication and Performance Schema becomes important. The entire state of the system (including the view, conflict statistics and service states) can be queried through Performance Schema tables. The distributed nature of the replication protocol and the fact that server instances agree and thus synchronize on transactions and metadata makes it simpler to inspect the state of the group. For example, you can connect to a single server in the group and obtain both local and global information by issuing select statements on the Group Replication related Performance Schema tables. For more information, see [Section 20.4, "Monitoring Group Replication"](#page-116-0).

# <span id="page-95-0"></span>**20.1.5 Group Replication Plugin Architecture**

MySQL Group Replication is a MySQL plugin and it builds on the existing MySQL replication infrastructure, taking advantage of features such as the binary log, row-based logging, and global transaction identifiers. It integrates with current MySQL frameworks, such as the performance schema or plugin and service infrastructures. The following figure presents a block diagram depicting the overall architecture of MySQL Group Replication.

**Figure 20.6 Group Replication Plugin Block Diagram**

![](_page_95_Figure_5.jpeg)

The MySQL Group Replication plugin includes a set of APIs for capture, apply, and lifecycle, which control how the plugin interacts with MySQL Server. There are interfaces to make information flow from the server to the plugin and vice versa. These interfaces isolate the MySQL Server core from the Group Replication plugin, and are mostly hooks placed in the transaction execution pipeline. In one direction, from server to the plugin, there are notifications for events such as the server starting, the server recovering, the server being ready to accept connections, and the server being about to commit a transaction. In the other direction, the plugin instructs the server to perform actions such as committing or aborting ongoing transactions, or queuing transactions in the relay log.

The next layer of the Group Replication plugin architecture is a set of components that react when a notification is routed to them. The capture component is responsible for keeping track of context related to transactions that are executing. The applier component is responsible for executing remote transactions on the database. The recovery component manages distributed recovery, and is responsible for getting a server that is joining the group up to date by selecting the donor, managing the catch up procedure and reacting to donor failures.

Continuing down the stack, the replication protocol module contains the specific logic of the replication protocol. It handles conflict detection, and receives and propagates transactions to the group.

The final two layers of the Group Replication plugin architecture are the Group Communication System (GCS) API, and an implementation of a Paxos-based group communication engine (XCom). The GCS API is a high level API that abstracts the properties required to build a replicated state machine (see [Section 20.1, "Group Replication Background"](#page-83-0)). It therefore decouples the implementation of the messaging layer from the remaining upper layers of the plugin. The group communication engine handles communications with the members of the replication group.

# <span id="page-96-0"></span>**20.2 Getting Started**

MySQL Group Replication is provided as a plugin for the MySQL server; each server in a group requires configuration and installation of the plugin. This section provides a detailed tutorial with the steps required to create a replication group with at least three members.

![](_page_96_Picture_7.jpeg)

#### **Tip**

To deploy multiple instances of MySQL, you can use [InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster.md) which enables you to easily administer a group of MySQL server instances in [MySQL](https://dev.mysql.com/doc/mysql-shell/8.0/en/) [Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/). InnoDB Cluster wraps MySQL Group Replication in a programmatic environment that enables you easily deploy a cluster of MySQL instances to achieve high availability. In addition, InnoDB Cluster interfaces seamlessly with [MySQL Router,](https://dev.mysql.com/doc/mysql-router/8.0/en/) which enables your applications to connect to the cluster without writing your own failover process. For similar use cases that do not require high availability, however, you can use [InnoDB ReplicaSet.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-replicaset.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

# <span id="page-96-1"></span>**20.2.1 Deploying Group Replication in Single-Primary Mode**

Each of the MySQL server instances in a group can run on an independent physical host machine, which is the recommended way to deploy Group Replication. This section explains how to create a replication group with three MySQL Server instances, each running on a different host machine. See [Section 20.2.2, "Deploying Group Replication Locally"](#page-109-0) for information about deploying multiple MySQL server instances running Group Replication on the same host machine, for example for testing purposes.

**Figure 20.7 Group Architecture**

![](_page_97_Picture_2.jpeg)

This tutorial explains how to get and deploy MySQL Server with the Group Replication plugin, how to configure each server instance before creating a group, and how to use Performance Schema monitoring to verify that everything is working correctly.

# <span id="page-97-0"></span>**20.2.1.1 Deploying Instances for Group Replication**

The first step is to deploy at least three instances of MySQL Server, this procedure demonstrates using multiple hosts for the instances, named s1, s2, and s3. It is assumed that MySQL Server is installed on each host (see Chapter 2, Installing MySQL). The Group Replication plugin is provided with MySQL Server 8.0; no additional software is required, although the plugin must be installed in the running MySQL server. See [Section 20.2.1.1, "Deploying Instances for Group Replication";](#page-97-0) for additional information, see Section 7.6, "MySQL Server Plugins".

In this example, three instances are used for the group, which is the minimum number of instances to create a group. Adding more instances increases the fault tolerance of the group. For example if the group consists of three members, in event of failure of one instance the group can continue. But in the event of another failure the group can no longer continue processing write transactions. By adding more instances, the number of servers which can fail while the group continues to process transactions also increases. The maximum number of instances which can be used in a group is nine. For more information see [Section 20.1.4.2, "Failure Detection"](#page-93-0).

# <span id="page-97-1"></span>**20.2.1.2 Configuring an Instance for Group Replication**

This section explains the configuration settings required for MySQL Server instances that you want to use for Group Replication. For background information, see [Section 20.3, "Requirements and](#page-110-0) [Limitations"](#page-110-0).

- [Storage Engines](#page-98-0)
- [Replication Framework](#page-98-1)
- [Group Replication Settings](#page-98-2)

#### <span id="page-98-0"></span>**Storage Engines**

For Group Replication, data must be stored in the InnoDB transactional storage engine (for details of why, see [Section 20.3.1, "Group Replication Requirements"\)](#page-110-1). The use of other storage engines, including the temporary MEMORY storage engine, might cause errors in Group Replication. Set the disabled\_storage\_engines system variable as follows to prevent their use:

```
disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"
```

Note that with the MyISAM storage engine disabled, when you are upgrading a MySQL instance to a release where mysql\_upgrade is still used (before MySQL 8.0.16), mysql\_upgrade might fail with an error. To handle this, you can re-enable that storage engine while you run mysql\_upgrade, then disable it again when you restart the server. For more information, see Section 6.4.5, "mysql\_upgrade — Check and Upgrade MySQL Tables".

# <span id="page-98-1"></span>**Replication Framework**

The following settings configure replication according to the MySQL Group Replication requirements.

```
server_id=1
gtid_mode=ON
enforce_gtid_consistency=ON
```

These settings configure the server to use the unique identifier number 1, to enable Section 19.1.3, "Replication with Global Transaction Identifiers", and to allow execution of only statements that can be safely logged using a GTID.

Up to and including MySQL 8.0.20, the following setting is also required:

```
binlog_checksum=NONE
```

This setting disables checksums for events written to the binary log, which default to being enabled. In MySQL 8.0.21 and later, Group Replication supports the presence of checksums in the binary log and can use them to verify the integrity of events on some channels, so you can use the default setting. For more details, see [Section 20.3.2, "Group Replication Limitations".](#page-113-0)

If you are using a version of MySQL earlier than 8.0.3, where the defaults were improved for replication, you also need to add these lines to the member's option file. If you have any of these system variables in the option file in later versions, ensure that they are set as shown. For more details see [Section 20.3.1, "Group Replication Requirements"](#page-110-1).

```
log_bin=binlog
log_slave_updates=ON
binlog_format=ROW
master_info_repository=TABLE
relay_log_info_repository=TABLE
transaction_write_set_extraction=XXHASH64
```

#### <span id="page-98-2"></span>**Group Replication Settings**

At this point the option file ensures that the server is configured and is instructed to instantiate the replication infrastructure under a given configuration. The following section configures the Group Replication settings for the server.

```
plugin_load_add='group_replication.so'
group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
group_replication_start_on_boot=off
group_replication_local_address= "s1:33061"
group_replication_group_seeds= "s1:33061,s2:33061,s3:33061"
group_replication_bootstrap_group=off
```

- plugin-load-add adds the Group Replication plugin to the list of plugins which the server loads at startup. This is preferable in a production deployment to installing the plugin manually.
- Configuring group\_replication\_group\_name tells the plugin that the group that it is joining, or creating, is named "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa".

The value of group\_replication\_group\_name must be a valid UUID. You can use SELECT UUID() to generate one. This UUID forms part of the GTIDs that are used when transactions received by group members from clients, and view change events that are generated internally by the group members, are written to the binary log.

- Configuring the group\_replication\_start\_on\_boot variable to off instructs the plugin to not start operations automatically when the server starts. This is important when setting up Group Replication as it ensures you can configure the server before manually starting the plugin. Once the member is configured you can set group\_replication\_start\_on\_boot to on so that Group Replication starts automatically upon server boot.
- Configuring group\_replication\_local\_address sets the network address and port which the member uses for internal communication with other members in the group. Group Replication uses this address for internal member-to-member connections involving remote instances of the group communication engine (XCom, a Paxos variant).

![](_page_99_Picture_7.jpeg)

#### **Important**

The group replication local address must be different to the host name and port used for SQL client connections, which are defined by MySQL Server's hostname and port system variables. It must not be used for client applications. It must be only be used for internal communication between the members of the group while running Group Replication.

The network address configured by group\_replication\_local\_address must be resolvable by all group members. For example, if each server instance is on a different machine with a fixed network address, you could use the IP address of the machine, such as 10.0.0.1. If you use a host name, you must use a fully qualified name, and ensure it is resolvable through DNS, correctly configured /etc/hosts files, or other name resolution processes. In MySQL 8.0.14 and later, IPv6 addresses (or host names that resolve to them) can be used as well as IPv4 addresses. A group can contain a mix of members using IPv6 and members using IPv4. For more information on Group Replication support for IPv6 networks and on mixed IPv4 and IPv6 groups, see [Section 20.5.5,](#page-149-0) ["Support For IPv6 And For Mixed IPv6 And IPv4 Groups".](#page-149-0)

The recommended port for group\_replication\_local\_address is 33061. This is used by Group Replication as the unique identifier for a group member within the replication group. You can use the same port for all members of a replication group as long as the host names or IP addresses are all different, as demonstrated in this tutorial. Alternatively you can use the same host name or IP address for all members as long as the ports are all different, for example as shown in [Section 20.2.2, "Deploying Group Replication Locally"](#page-109-0).

The connection that an existing member offers to a joining member for Group Replication's distributed recovery process is not the network address configured by group\_replication\_local\_address. In MySQL 8.0.20 and earlier, group members offer their standard SQL client connection to joining members for distributed recovery, as specified by MySQL Server's hostname and port system variables. In MySQL 8.0.21 and later, group members may advertise an alternative list of distributed recovery endpoints as dedicated client connections for joining members. For more details, see [Section 20.5.4.1, "Connections for Distributed Recovery".](#page-135-0)

![](_page_100_Picture_1.jpeg)

#### **Important**

Distributed recovery can fail if a joining member cannot correctly identify the other members using the host name as defined by MySQL Server's hostname system variable. It is recommended that operating systems running MySQL have a properly configured unique host name, either using DNS or local settings. The host name that the server is using for SQL client connections can be verified in the Member\_host column of the Performance Schema table replication\_group\_members. If multiple group members externalize a default host name set by the operating system, there is a chance of the joining member not resolving it to the correct member address and not being able to connect for distributed recovery. In this situation you can use MySQL Server's report\_host system variable to configure a unique host name to be externalized by each of the servers.

• Configuring group\_replication\_group\_seeds sets the hostname and port of the group members which are used by the new member to establish its connection to the group. These members are called the seed members. Once the connection is established, the group membership information is listed in the Performance Schema table replication\_group\_members. Usually the group\_replication\_group\_seeds list contains the hostname:port of each of the group member's group\_replication\_local\_address, but this is not obligatory and a subset of the group members can be chosen as seeds.

![](_page_100_Picture_5.jpeg)

### **Important**

The hostname:port listed in group\_replication\_group\_seeds is the seed member's internal network address, configured by group\_replication\_local\_address and not the hostname:port used for SQL client connections, which is shown for example in the Performance Schema table replication\_group\_members.

The server that starts the group does not make use of this option, since it is the initial server and as such, it is in charge of bootstrapping the group. In other words, any existing data which is on the server bootstrapping the group is what is used as the data for the next joining member. The second server joining asks the one and only member in the group to join, any missing data on the second server is replicated from the donor data on the bootstrapping member, and then the group expands. The third server joining can ask any of these two to join, data is synchronized to the new member, and then the group expands again. Subsequent servers repeat this procedure when joining.

![](_page_100_Picture_9.jpeg)

#### **Warning**

When joining multiple servers at the same time, make sure that they point to seed members that are already in the group. Do not use members that are also joining the group as seeds, because they might not yet be in the group when contacted.

It is good practice to start the bootstrap member first, and let it create the group. Then make it the seed member for the rest of the members that are joining. This ensures that there is a group formed when joining the rest of the members.

Creating a group and joining multiple members at the same time is not supported. It might work, but chances are that the operations race and then the act of joining the group ends up in an error or a time out.

A joining member must communicate with a seed member using the same protocol (IPv4 or IPv6) that the seed member advertises in the group\_replication\_group\_seeds option. For the purpose of IP address permissions for Group Replication, the allowlist on the seed member must include an IP address for the joining member for the protocol offered by the seed member, or a

host name that resolves to an address for that protocol. This address or host name must be set up and permitted in addition to the joining member's group\_replication\_local\_address if the protocol for that address does not match the seed member's advertised protocol. If a joining member does not have a permitted address for the appropriate protocol, its connection attempt is refused. For more information, see [Section 20.6.4, "Group Replication IP Address Permissions".](#page-167-0)

• Configuring group\_replication\_bootstrap\_group instructs the plugin whether to bootstrap the group or not. In this case, even though s1 is the first member of the group we set this variable to off in the option file. Instead we configure group\_replication\_bootstrap\_group when the instance is running, to ensure that only one member actually bootstraps the group.

![](_page_101_Picture_3.jpeg)

#### **Important**

The group\_replication\_bootstrap\_group variable must only be enabled on one server instance belonging to a group at any time, usually the first time you bootstrap the group (or in case the entire group is brought down and back up again). If you bootstrap the group multiple times, for example when multiple server instances have this option set, then they could create an artificial split brain scenario, in which two distinct groups with the same name exist. Always set group\_replication\_bootstrap\_group=off after the first server instance comes online.

The system variables described in this tutorial are the required configuration settings to start a new member, but further system variables are also available to configure group members. These are listed in Section 20.9, "Group Replication Variables".

![](_page_101_Picture_7.jpeg)

#### **Important**

A number of system variables, some specific to Group Replication and others not, are group-wide configuration settings that must have the same value on all group members. If the group members have a value set for one of these system variables, and a joining member has a different value set for it, the joining member cannot join the group and an error message is returned. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group. These system variables are all identified in Section 20.9, "Group Replication Variables".

# <span id="page-101-0"></span>**20.2.1.3 User Credentials For Distributed Recovery**

Group Replication uses a distributed recovery process to synchronize group members when joining them to the group. Distributed recovery involves transferring transactions from a donor's binary log to a joining member using a replication channel named group\_replication\_recovery. You must therefore set up a replication user with the correct permissions so that Group Replication can establish direct member-to-member replication channels. If group members have been set up to support the use of a remote cloning operation as part of distributed recovery, which is available in MySQL 8.0.17 and later, this replication user is also used as the clone user on the donor, and requires the correct permissions for this role too. For a complete description of distributed recovery, see [Section 20.5.4,](#page-134-0) ["Distributed Recovery"](#page-134-0).

The same replication user must be used for distributed recovery on every group member. The process of creating the replication user for distributed recovery can be captured in the binary log, and then you can rely on distributed recovery to replicate the statements used to create the user. Alternatively, you can disable binary logging before creating the replication user, and then create the user manually on each member, for example if you want to avoid the changes being propagated to other server instances. If you do this, ensure you re-enable binary logging once you have configured the user.

![](_page_101_Picture_13.jpeg)

#### **Important**

If distributed recovery connections for your group use SSL, the replication user must be created on each server before the joining member connects to the donor. For instructions to set up SSL for distributed recovery connections and create a replication user that requires SSL, see [Section 20.6.3, "Securing](#page-163-0) [Distributed Recovery Connections"](#page-163-0)

![](_page_102_Picture_2.jpeg)

#### **Important**

By default, users created in MySQL 8 use Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication". If the replication user for distributed recovery uses the caching SHA-2 authentication plugin, and you are not using SSL for distributed recovery connections, RSA key-pairs are used for password exchange. You can either copy the public key of the replication user to the joining member, or configure the donors to provide the public key when requested. For instructions to do this, see [Section 20.6.3.1, "Secure User](#page-163-1) [Credentials for Distributed Recovery"](#page-163-1).

To create the replication user for distributed recovery, follow these steps:

- 1. Start the MySQL server instance, then connect a client to it.
- 2. If you want to disable binary logging in order to create the replication user separately on each instance, do so by issuing the following statement:

```
mysql> SET SQL_LOG_BIN=0;
```

- 3. Create a MySQL user with the following privileges:
  - REPLICATION SLAVE, which is required for making a distributed recovery connection to a donor to retrieve data.
  - CONNECTION\_ADMIN, which ensures that Group Replication connections are not terminated if one of the servers involved is placed in offline mode.
  - BACKUP\_ADMIN, if the servers in the replication group are set up to support cloning (see [Section 20.5.4.2, "Cloning for Distributed Recovery"](#page-138-0)). This privilege is required for a member to act as the donor in a cloning operation for distributed recovery.
  - GROUP\_REPLICATION\_STREAM, if the MySQL communication stack is in use for the replication group (see [Section 20.6.1, "Communication Stack for Connection Security Management"\)](#page-157-1). This privilege is required for the user account to be able to establish and maintain connections for Group Replication using the MySQL communication stack.

In this example the user rpl\_user with the password password is shown. When configuring your servers use a suitable user name and password:

```
mysql> CREATE USER rpl_user@'%' IDENTIFIED BY 'password';
mysql> GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';
mysql> GRANT CONNECTION_ADMIN ON *.* TO rpl_user@'%';
mysql> GRANT BACKUP_ADMIN ON *.* TO rpl_user@'%';
mysql> GRANT GROUP_REPLICATION_STREAM ON *.* TO rpl_user@'%';
mysql> FLUSH PRIVILEGES;
```

4. If you disabled binary logging, enable it again as soon as you have created the user, by issuing the following statement:

```
mysql> SET SQL_LOG_BIN=1;
```

5. When you have created the replication user, you must supply the user credentials to the server for use with distributed recovery. You can do this by setting the user credentials as the credentials for the group\_replication\_recovery channel, using a CHANGE REPLICATION SOURCE TO statement (MySQL 8.0.23 or later) or CHANGE MASTER TO statement (prior to MySQL 8.0.23). Alternatively, in MySQL 8.0.21 and later, you can specify the user credentials for distributed recovery on the START GROUP\_REPLICATION statement.

- User credentials set using CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO are stored in plain text in the replication metadata repositories on the server. They are applied whenever Group Replication is started, including automatic starts if the group\_replication\_start\_on\_boot system variable is set to ON.
- User credentials specified on START GROUP\_REPLICATION are saved in memory only, and are removed by a STOP GROUP\_REPLICATION statement or server shutdown. You must issue a START GROUP\_REPLICATION statement to provide the credentials again, so you cannot start Group Replication automatically with these credentials. This method of specifying the user credentials helps to secure the Group Replication servers against unauthorized access.

For more information on the security implications of each method of providing the user credentials, see [Providing Replication User Credentials Securely.](#page-164-0) If you choose to provide the user credentials using a CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement, issue the following statement on the server instance now, replacing rpl\_user and password with the values used when creating the user:

```
mysql> CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password' \\
 FOR CHANNEL 'group_replication_recovery';
```

Or in MySQL 8.0.23 or later:

```
mysql> CHANGE REPLICATION SOURCE TO SOURCE_USER='rpl_user', SOURCE_PASSWORD='password' \\
 FOR CHANNEL 'group_replication_recovery';
```

# <span id="page-103-0"></span>**20.2.1.4 Launching Group Replication**

It is first necessary to ensure that the Group Replication plugin is installed on server s1. If you used plugin\_load\_add='group\_replication.so' in the option file then the Group Replication plugin is already installed, and you can proceed to the next step. Otherwise, you must install the plugin manually; to do this, connect to the server using the mysql client, and issue the SQL statement shown here:

mysql> **INSTALL PLUGIN group\_replication SONAME 'group\_replication.so';**

![](_page_103_Picture_10.jpeg)

#### **Important**

The mysql.session user must exist before you can load Group Replication. mysql.session was added in MySQL version 8.0.2. If your data dictionary was initialized using an earlier version you must perform the MySQL upgrade procedure (see Chapter 3, Upgrading MySQL). If the upgrade is not run, Group Replication fails to start with the error message There was an error when trying to access the server with user: mysql.session@localhost. Make sure the user is present in the server and that mysql\_upgrade was ran after a server update.

To check that the plugin was installed successfully, issue SHOW PLUGINS; and check the output. It should show something like this:

```
mysql> SHOW PLUGINS;
+----------------------------+----------+--------------------+----------------------+-------------+
| Name | Status | Type | Library | License |
+----------------------------+----------+--------------------+----------------------+-------------+
| binlog | ACTIVE | STORAGE ENGINE | NULL | PROPRIETARY |
(...)
| group_replication | ACTIVE | GROUP REPLICATION | group_replication.so | PROPRIETARY |
+----------------------------+----------+--------------------+----------------------+-------------+
```