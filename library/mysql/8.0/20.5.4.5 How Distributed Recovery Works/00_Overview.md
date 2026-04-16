---
source: MySQL 8.0 Reference
title: 00_Overview
---

When Group Replication's distributed recovery process is carrying out state transfer from the binary log, to synchronize the joining member with the donor up to a specific point in time, the joining member and donor make use of GTIDs (see Section 19.1.3, "Replication with Global Transaction Identifiers"). However, GTIDs only provide a means to realize which transactions the joining member is missing. They do not help marking a specific point in time to which the server joining the group must catch up, nor do they convey certification information. This is the job of binary log view markers, which mark view changes in the binary log stream, and also contain additional metadata information, supplying the joining member with missing certification-related data.

This topic explains the role of view changes and the view change identifier, and the steps to carry out state transfer from the binary log.

#### **View and View Changes**

A view corresponds to a group of members participating actively in the current configuration, in other words at a specific point in time. They are functioning correctly and online in the group.

A view change occurs when a modification to the group configuration happens, such as a member joining or leaving. Any group membership change results in an independent view change communicated to all members at the same logical point in time.

A view identifier uniquely identifies a view. It is generated whenever a view change happens.

At the group communication layer, view changes with their associated view identifiers mark boundaries between the data exchanged before and after a member joins. This concept is implemented through a binary log event: the "view change log event" (VCLE). The view identifier is recorded to demarcate transactions transmitted before and after changes happen in the group membership.

The view identifier itself is built from two parts: a randomly generated part, and a monotonically increasing integer. The randomly generated part is generated when the group is created, and remains unchanged while there is at least one member in the group. The integer is incremented every time a view change happens. Using these two different parts enables the view identifier to identify incremental group changes caused by members joining or leaving, and also to identify the situation where all members leave the group in a full group shutdown, so no information remains of what view the group was in. Randomly generating part of the identifier when the group is started from the beginning ensures that the data markers in the binary log remain unique, and an identical identifier is not reused after a full group shutdown, as this would cause issues with distributed recovery in the future.

#### **Begin: Stable Group**

All servers are online and processing incoming transactions from the group. Some servers may be a little behind in terms of transactions replicated, but eventually they converge. The group acts as one distributed and replicated database.

**Figure 20.8 Stable Group**

![](_page_145_Figure_5.jpeg)

#### **View Change: a Member Joins**

Whenever a new member joins the group and therefore a view change is performed, every online server queues a view change log event for execution. This is queued because before the view change, several transactions can be queued on the server to be applied and as such, these belong to the old view. Queuing the view change event after them guarantees a correct marking of when this happened.

Meanwhile, the joining member selects a suitable donor from the list of online servers as stated by the membership service through the view abstraction. A member joins on view 4 and the online members write a view change event to the binary log.

**Figure 20.9 A Member Joins**

#### **State Transfer: Catching Up**

If group members and the joining member are set up with the clone plugin (see [Section 20.5.4.2,](#page-138-0) ["Cloning for Distributed Recovery"\)](#page-138-0), and the difference in transactions between the joining member and the group exceeds the threshold set for a remote cloning operation (group\_replication\_clone\_threshold), Group Replication begins distributed recovery with a remote cloning operation. A remote cloning operation is also carried out if required transactions are no longer present in any group member's binary log files. During a remote cloning operation, the existing data on the joining member is removed, and replaced with a copy of the donor's data. When the remote cloning operation is complete and the joining member has restarted, state transfer from a donor's binary log is carried out to get the transactions that the group applied while the remote cloning operation was in progress. If there is not a large transaction gap, or if the clone plugin is not installed, Group Replication proceeds directly to state transfer from a donor's binary log.

For state transfer from a donor's binary log, a connection is established between the joining member and the donor and state transfer begins. This interaction with the donor continues until the server joining the group's applier thread processes the view change log event that corresponds to the view change triggered when the server joining the group came into the group. In other words, the server joining the group replicates from the donor, until it gets to the marker with the view identifier which matches the view marker it is already in.

**Figure 20.10 State Transfer: Catching Up**

![](_page_147_Figure_2.jpeg)

As view identifiers are transmitted to all members in the group at the same logical time, the server joining the group knows at which view identifier it should stop replicating. This avoids complex GTID set calculations because the view identifier clearly marks which data belongs to each group view.

While the server joining the group is replicating from the donor, it is also caching incoming transactions from the group. Eventually, it stops replicating from the donor and switches to applying those that are cached.

**Figure 20.11 Queued Transactions**

#### **Finish: Caught Up**

When the server joining the group recognizes a view change log event with the expected view identifier, the connection to the donor is terminated and it starts applying the cached transactions. Although it acts as a marker in the binary log, delimiting view changes, the view change log event also plays another role. It conveys the certification information as perceived by all servers when the server joining the group entered the group, in other words the last view change. Without it, the server joining the group would not have the necessary information to be able to certify (detect conflicts) subsequent transactions.

The duration of the catch up is not deterministic, because it depends on the workload and the rate of incoming transactions to the group. This process is completely online and the server joining the group does not block any other server in the group while it is catching up. Therefore the number of transactions the server joining the group is behind when it moves to this stage can, for this reason, vary and thus increase or decrease according to the workload.

When the server joining the group reaches zero queued transactions and its stored data is equal to the other members, its public state changes to online.

**Figure 20.12 Instance Online**

![](_page_149_Figure_3.jpeg)

# <span id="page-149-0"></span>**20.5.5 Support For IPv6 And For Mixed IPv6 And IPv4 Groups**

As of MySQL 8.0.14, Group Replication group members can use IPv6 addresses as an alternative to IPv4 addresses for communications within the group. To use IPv6 addresses, the operating system on the server host and the MySQL Server instance must both be configured to support IPv6. For instructions to set up IPv6 support for a server instance, see Section 7.1.13, "IPv6 Support".

IPv6 addresses, or host names that resolve to them, can be specified as the network address that the member provides in the group\_replication\_local\_address option for connections from other members. When specified with a port number, an IPv6 address must be specified in square brackets, for example:

```
group_replication_local_address= "[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061"
```

The network address or host name specified in group\_replication\_local\_address is used by Group Replication as the unique identifier for a group member within the replication group. If a host name specified as the Group Replication local address for a server instance resolves to both an IPv4 and an IPv6 address, the IPv4 address is always used for Group Replication connections. The address or host name specified as the Group Replication local address is not the same as the MySQL server SQL protocol host and port, and is not specified in the bind\_address system variable for the server instance. For the purpose of IP address permissions for Group Replication (see [Section 20.6.4, "Group Replication IP Address Permissions"\)](#page-167-0), the address that you specify for each group member in group\_replication\_local\_address must

be added to the list for the group\_replication\_ip\_allowlist (from MySQL 8.0.22) or group\_replication\_ip\_whitelist system variable on the other servers in the replication group.

A replication group can contain a combination of members that present an IPv6 address as their Group Replication local address, and members that present an IPv4 address. When a server joins such a mixed group, it must make the initial contact with the seed member using the protocol that the seed member advertises in the group\_replication\_group\_seeds option, whether that is IPv4 or IPv6. If any of the seed members for the group are listed in the group\_replication\_group\_seeds option with an IPv6 address when a joining member has an IPv4 Group Replication local address, or the reverse, you must also set up and permit an alternative address for the joining member for the required protocol (or a host name that resolves to an address for that protocol). If a joining member does not have a permitted address for the appropriate protocol, its connection attempt is refused. The alternative address or host name only needs to be added to the group\_replication\_ip\_allowlist (from MySQL 8.0.22) or group\_replication\_ip\_whitelist system variable on the other servers in the replication group, not to the group\_replication\_local\_address value for the joining member (which can only contain a single address).

For example, server A is a seed member for a group, and has the following configuration settings for Group Replication, so that it is advertising an IPv6 address in the group\_replication\_group\_seeds option:

```
group_replication_bootstrap_group=on
group_replication_local_address= "[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061"
group_replication_group_seeds= "[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061"
```

Server B is a joining member for the group, and has the following configuration settings for Group Replication, so that it has an IPv4 Group Replication local address:

```
group_replication_bootstrap_group=off
group_replication_local_address= "203.0.113.21:33061"
group_replication_group_seeds= "[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061"
```

Server B also has an alternative IPv6 address 2001:db8:8b0:40:3d9c:cc43:e006:19e8. For Server B to join the group successfully, both its IPv4 Group Replication local address, and its alternative IPv6 address, must be listed in Server A's allowlist, as in the following example:

```
group_replication_ip_allowlist=
"203.0.113.0/24,2001:db8:85a3:8d3:1319:8a2e:370:7348,
2001:db8:8b0:40:3d9c:cc43:e006:19e8"
```

As a best practice for Group Replication IP address permissions, Server B (and all other group members) should have the same allowlist as Server A, unless security requirements demand otherwise.

If any or all members of a replication group are using an older MySQL Server version that does not support the use of IPv6 addresses for Group Replication, a member cannot participate in the group using an IPv6 address (or a host name that resolves to one) as its Group Replication local address. This applies both in the case where at least one existing member uses an IPv6 address and a new member that does not support this attempts to join, and in the case where a new member attempts to join using an IPv6 address but the group includes at least one member that does not support this. In each situation, the new member cannot join. To make a joining member present an IPv4 address for group communications, you can either change the value of group\_replication\_local\_address to an IPv4 address, or configure your DNS to resolve the joining member's existing host name to an IPv4 address. After you have upgraded every group member to a MySQL Server version that supports IPv6 for Group Replication, you can change the group\_replication\_local\_address value for each member to an IPv6 address, or configure your DNS to present an IPv6 address. Changing the value of group\_replication\_local\_address takes effect only when you stop and restart Group Replication.

IPv6 addresses can also be used as distributed recovery endpoints, which can be specified in MySQL 8.0.21 and later using the group\_replication\_advertise\_recovery\_endpoints system

variable. The same rules apply to addresses used in this list. See [Section 20.5.4.1, "Connections for](#page-135-0) [Distributed Recovery"](#page-135-0).

# <span id="page-151-0"></span>**20.5.6 Using MySQL Enterprise Backup with Group Replication**

MySQL Enterprise Backup is a commercially-licensed backup utility for MySQL Server, available with [MySQL Enterprise Edition](https://www.mysql.com/products/enterprise/). This section explains how to back up and subsequently restore a Group Replication member using MySQL Enterprise Backup. The same technique can be used to quickly add a new member to a group.

# **Backing up a Group Replication Member Using MySQL Enterprise Backup**

Backing up a Group Replication member is similar to backing up a stand-alone MySQL instance. The following instructions assume that you are already familiar with how to use MySQL Enterprise Backup to perform a backup; if that is not the case, please review [Backing Up a Database Server.](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/backing-up.md) Also note the requirements described in [Grant MySQL Privileges to Backup Administrator](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/mysqlbackup.privileges.md) and [Using MySQL](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/meb-group-replication.md) [Enterprise Backup with Group Replication](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/meb-group-replication.md).

Consider the following group with three members, s1, s2, and s3, running on hosts with the same names:

```
mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |
+-------------+-------------+--------------+
| s1 | 3306 | ONLINE |
| s2 | 3306 | ONLINE |
| s3 | 3306 | ONLINE |
+-------------+-------------+--------------+
```

Using MySQL Enterprise Backup, create a backup of s2 by issuing on its host, for example, the following statement:

```
s2> mysqlbackup --defaults-file=/etc/my.cnf --backup-image=/backups/my.mbi_`date +%d%m_%H%M` \
 --backup-dir=/backups/backup_`date +%d%m_%H%M` --user=root -p \
 --host=127.0.0.1 backup-to-image
```

![](_page_151_Picture_10.jpeg)

# **Notes**

• For MySQL Enterprise Backup 8.0.18 and earlier, If the system variable sql\_require\_primary\_key is set to ON for the group, MySQL Enterprise Backup is not able to log the backup progress on the servers. This is because the backup\_progress table on the server is a CSV table, for which primary keys are not supported. In that case, mysqlbackup issues the following warnings during the backup operation:

181011 11:17:06 MAIN WARNING: MySQL query 'CREATE TABLE IF NOT EXISTS mysql.backup\_progress( `backup\_id` BIGINT NOT NULL, `tool\_name` VARCHAR(4096) NOT NULL, `error\_code` INT NOT NULL, `error\_message` VARCHAR(4096) NOT NULL, `current\_time` TIMESTAMP NOT NULL DEFAULT CURRENT\_TIMESTAMP ON UPDATE CURRENT\_TIMESTAMP,`current\_state` VARCHAR(200) NOT NULL ) ENGINE=CSV DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3\_bin': 3750, Unable to create a table without PK, when system variable 'sql\_require\_primary\_key' is set. Add a PK to the table or unset this variable to avoid this message. Note that tables without PK can cause performance problems in row-based replication, so please consult your DBA before changing this setting. 181011 11:17:06 MAIN WARNING: This backup operation's progress info cannot be logged.

This does not prevent mysqlbackup from finishing the backup.

• For MySQL Enterprise Backup 8.0.20 and earlier, when backing up a secondary member, as MySQL Enterprise Backup cannot write backup status and metadata to a read-only server instance, it might issue warnings similar to the following one during the backup operation:

181113 21:31:08 MAIN WARNING: This backup operation cannot write to backup progress. The MySQL server is running with the --super-read-only option.

You can avoid the warning by using the --no-history-logging option with your backup command. This is not an issue for MySQL Enterprise Backup 8.0.21 and higher—see [Using MySQL Enterprise Backup with Group](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/meb-group-replication.md) [Replication](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/meb-group-replication.md) for details.

# <span id="page-152-0"></span>**Restoring a Failed Member**

Assume one of the members (s3 in the following example) is irreconcilably corrupted. The most recent backup of group member s2 can be used to restore s3. Here are the steps for performing the restore:

1. Copy the backup of s2 onto the host for s3. The exact way to copy the backup depends on the operating system and tools available to you. In this example, we assume the hosts are both Linux servers and use SCP to copy the files between them:

```
s2/backups> scp my.mbi_2206_1429 s3:/backups
```

- 2. Restore the backup. Connect to the target host (the host for s3 in this case), and restore the backup using MySQL Enterprise Backup. Here are the steps:
  - a. Stop the corrupted server, if it is still running. For example, on Linux distributions that use systemd:

```
s3> systemctl stop mysqld
```

- b. Preserve the two configuration files in the corrupted server's data directory, auto.cnf and mysqld-auto.cnf (if it exists), by copying them to a safe location outside of the data directory. This is for preserving the server's UUID and Section 7.1.9.3, "Persisted System Variables" (if used), which are needed in the steps below.
- c. Delete all contents in the data directory of s3. For example:

```
s3> rm -rf /var/lib/mysql/*
```

If the system variables innodb\_data\_home\_dir, innodb\_log\_group\_home\_dir, and innodb\_undo\_directory point to any directories other than the data directory, they should also be made empty; otherwise, the restore operation fails.

d. Restore backup of s2 onto the host for s3:

```
s3> mysqlbackup --defaults-file=/etc/my.cnf \
 --datadir=/var/lib/mysql \
 --backup-image=/backups/my.mbi_2206_1429 \
 --backup-dir=/tmp/restore_`date +%d%m_%H%M` copy-back-and-apply-log
```

![](_page_152_Picture_16.jpeg)

### **Note**

The command above assumes that the binary logs and relay logs on s2 and s3 have the same base name and are at the same location on the two servers. If these conditions are not met, you should use the [--log](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/server-repository-options.md#option_meb_log-bin)[bin](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/server-repository-options.md#option_meb_log-bin) and [--relay-log](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/server-repository-options.md#option_meb_relay-log) options to restore the binary log and relay log to their original file paths on s3. For example, if you know that on s3 the binary log's base name is s3-bin and the relay-log's base name is s3 relay-bin, your restore command should look like:

```
mysqlbackup --defaults-file=/etc/my.cnf \
 --datadir=/var/lib/mysql \
 --backup-image=/backups/my.mbi_2206_1429 \
 --log-bin=s3-bin --relay-log=s3-relay-bin \
 --backup-dir=/tmp/restore_`date +%d%m_%H%M` copy-back-and-apply-log
```

Being able to restore the binary log and relay log to the right file paths makes the restore process easier; if that is impossible for some reason, see [Rebuild the Failed Member to Rejoin as a New Member](#page-154-0).

3. Restore the auto.cnf file for s3. To rejoin the replication group, the restored member must have the same server\_uuid it used to join the group before. Supply the old server UUID by copying the auto.cnf file preserved in step 2 above into the data directory of the restored member.

![](_page_153_Picture_3.jpeg)

#### **Note**

If you cannot supply the failed member's original server\_uuid to the restored member by restoring its old auto.cnf file, you must let the restored member join the group as a new member; see instructions in [Rebuild the Failed Member to Rejoin as a New Member](#page-154-0) below on how to do that.

- 4. Restore the mysqld-auto.cnf file for s3 (only required if s3 used persistent system variables). The settings for the Section 7.1.9.3, "Persisted System Variables" that were used to configure the failed member must be provided to the restored member. These settings are to be found in the mysqld-auto.cnf file of the failed server, which you should have preserved in step 2 above. Restore the file to the data directory of the restored server. See [Restoring Persisted System](#page-156-0) [Variables](#page-156-0) on what to do if you do not have a copy of the file.
- 5. Start the restored server. For example, on Linux distributions that use systemd:

systemctl start mysqld

![](_page_153_Picture_9.jpeg)

#### **Note**

+-------------+-------------+--------------+

If the server you are restoring is a primary member, perform the steps described in [Restoring a Primary Member](#page-156-1) before starting the restored server.

6. Restart Group Replication. Connect to the restarted s3 using, for example, a mysql client, and issue the following statement:

```
mysql> START GROUP_REPLICATION;
```

Before the restored instance can become an online member of the group, it needs to apply any transactions that have happened to the group after the backup was taken; this is achieved using Group Replication's [distributed recovery](#page-134-0) mechanism, and the process starts after the START GROUP\_REPLICATION statement has been issued. To check the member status of the restored instance, issue:

mysql> SELECT member\_host, member\_port, member\_state FROM performance\_schema.replication\_group\_members; +-------------+-------------+--------------+ | member\_host | member\_port | member\_state | +-------------+-------------+--------------+ | s1 | 3306 | ONLINE | | s2 | 3306 | ONLINE | | s3 | 3306 | RECOVERING |

This shows that s3 is applying transactions to catch up with the group. Once it has caught up with the rest of the group, its member\_state changes to ONLINE:

mysql> SELECT member\_host, member\_port, member\_state FROM performance\_schema.replication\_group\_members; +-------------+-------------+--------------+ | member\_host | member\_port | member\_state | +-------------+-------------+--------------+ | s1 | 3306 | ONLINE | | s2 | 3306 | ONLINE | | s3 | 3306 | ONLINE |

+-------------+-------------+--------------+

![](_page_154_Picture_2.jpeg)

#### **Note**

If the server you are restoring is a primary member, once it has gained synchrony with the group and become ONLINE, perform the steps described at the end of [Restoring a Primary Member](#page-156-1) to revert the configuration changes you had made to the server before you started it.

The member has now been fully restored from the backup and functions as a regular member of the group.

# <span id="page-154-0"></span>**Rebuild the Failed Member to Rejoin as a New Member**

Sometimes, the steps outlined above in [Restoring a Failed Member](#page-152-0) cannot be carried out because, for example, the binary log or relay log is corrupted, or it is just missing from the backup. In such a situation, use the backup to rebuild the member, and then add it to the group as a new member. In the steps below, we assume the rebuilt member is named s3, like the failed member, and that it runs on the same host as s3:

1. Copy the backup of s2 onto the host for s3 . The exact way to copy the backup depends on the operating system and tools available to you. In this example we assume the hosts are both Linux servers and use SCP to copy the files between them:

```
s2/backups> scp my.mbi_2206_1429 s3:/backups
```

- 2. Restore the backup. Connect to the target host (the host for s3 in this case), and restore the backup using MySQL Enterprise Backup. Here are the steps:
  - a. Stop the corrupted server, if it is still running. For example, on Linux distributions that use systemd:

```
s3> systemctl stop mysqld
```

- b. Preserve the configuration file mysqld-auto.cnf, if it is found in the corrupted server's data directory, by copying it to a safe location outside of the data directory. This is for preserving the server's Section 7.1.9.3, "Persisted System Variables", which are needed later.
- c. Delete all contents in the data directory of s3. For example:

```
s3> rm -rf /var/lib/mysql/*
```

If the system variables innodb\_data\_home\_dir, innodb\_log\_group\_home\_dir, and innodb\_undo\_directory point to any directories other than the data directory, they should also be made empty; otherwise, the restore operation fails.

d. Restore the backup of s2 onto the host of s3. With this approach, we are rebuilding s3 as a new member, for which we do not need or do not want to use the old binary and relay logs in the backup; therefore, if these logs have been included in your backup, exclude them using the [--skip-binlog](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/backup-capacity-options.md#option_meb_skip-binlog) and [--skip-relaylog](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/backup-capacity-options.md#option_meb_skip-relaylog) options:

```
s3> mysqlbackup --defaults-file=/etc/my.cnf \
 --datadir=/var/lib/mysql \
 --backup-image=/backups/my.mbi_2206_1429 \
 --backup-dir=/tmp/restore_`date +%d%m_%H%M` \
 --skip-binlog --skip-relaylog \
 copy-back-and-apply-log
```

![](_page_154_Picture_19.jpeg)

#### **Note**

If you have healthy binary log and relay logs in the backup that you can transfer onto the target host with no issues, you are recommended to

follow the easier procedure as described in [Restoring a Failed Member](#page-152-0) above.

3. Restore the mysqld-auto.cnf file for s3 (only required if s3 used persistent system variables). The settings for the Section 7.1.9.3, "Persisted System Variables" that were used to configure the failed member must be provided to the restored server. These settings are to be found in the mysqld-auto.cnf file of the failed server, which you should have preserved in step 2 above. Restore the file to the data directory of the restored server. See [Restoring Persisted System](#page-156-0) [Variables](#page-156-0) on what to do if you do not have a copy of the file.

![](_page_155_Picture_3.jpeg)

#### **Note**

Do NOT restore the corrupted server's auto.cnf file to the data directory of the new member—when the rebuilt s3 joins the group as a new member, it is going to be assigned a new server UUID.

4. Start the restored server. For example, on Linux distributions that use systemd:

systemctl start mysqld

![](_page_155_Picture_8.jpeg)

#### **Note**

If the server you are restoring is a primary member, perform the steps described in [Restoring a Primary Member](#page-156-1) before starting the restored server.

5. Reconfigure the restored member to join Group Replication. Connect to the restored server with a mysql client and reset the source and replica information with the following statements:

```
mysql> RESET MASTER;
mysql> RESET MASTER;
mysql> RESET SLAVE ALL;
```

In MySQL 8.0.22 and later, use the statements shown here:

```
mysql> RESET MASTER;
mysql> RESET REPLICA ALL;
```

For the restored server to be able to recover automatically using Group Replication's builtin mechanism for [distributed recovery](#page-134-0), configure the server's gtid\_executed variable. To do this, use the backup\_gtid\_executed.sql file included in the backup of s2, which is usually restored under the restored member's data directory. Disable binary logging, use the backup\_gtid\_executed.sql file to configure gtid\_executed, and then re-enable binary logging by issuing the following statements with your mysql client:

```
mysql> SET SQL_LOG_BIN=OFF;
mysql> SOURCE datadir/backup_gtid_executed.sql
mysql> SET SQL_LOG_BIN=ON;
```

Then, configure the [Group Replication user credentials](#page-101-0) on the member using the SQL statements shown here:

```
mysql> CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password'
 -> FOR CHANNEL 'group_replication_recovery';
```

In MySQL 8.0.23 and later, use these statements instead:

```
mysql> CHANGE REPLICATION SOURCE TO SOURCE_USER='rpl_user', SOURCE_PASSWORD='password'
 -> FOR CHANNEL 'group_replication_recovery';
```

6. Restart Group Replication. Issue the following statement to the restored server with your mysql client:

```
mysql>> START GROUP_REPLICATION;
```

Before the restored instance can become an online member of the group, it needs to apply any transactions that have happened to the group after the backup was taken; this is achieved using Group Replication's [distributed recovery](#page-134-0) mechanism, and the process starts after the START GROUP\_REPLICATION statement has been issued. To check the member status of the restored instance, issue:

```
mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |
+-------------+-------------+--------------+
| s3 | 3306 | RECOVERING |
| s2 | 3306 | ONLINE |
| s1 | 3306 | ONLINE |
+-------------+-------------+--------------+
```

This shows that s3 is applying transactions to catch up with the group. Once it has caught up with the rest of the group, its member\_state changes to ONLINE:

```
mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |
+-------------+-------------+--------------+
| s3 | 3306 | ONLINE |
| s2 | 3306 | ONLINE |
| s1 | 3306 | ONLINE |
+-------------+-------------+--------------+
```

![](_page_156_Picture_7.jpeg)

#### **Note**

If the server you are restoring is a primary member, once it has gained synchrony with the group and become ONLINE, perform the steps described at the end of [Restoring a Primary Member](#page-156-1) to revert the configuration changes you had made to the server before you started it.

The member has now been restored to the group as a new member.

<span id="page-156-0"></span>**Restoring Persisted System Variables.** mysqlbackup does not provide support for backing up or preserving Section 7.1.9.3, "Persisted System Variables"—the file mysqld-auto.cnf is not included in a backup. To start the restored member with its persisted variable settings, you need to do one of the following:

- Preserve a copy of the mysqld-auto.cnf file from the corrupted server, and copy it to the restored server's data directory.
- Copy the mysqld-auto.cnf file from another member of the group into the restored server's data directory, if that member has the same persisted system variable settings as the corrupted member.
- After the restored server is started and before you restart Group Replication, set all the system variables manually to their persisted values through a mysql client.

<span id="page-156-1"></span>**Restoring a Primary Member.** If the restored member is a primary in the group, care must be taken to prevent writes to the restored database during the Group Replication distributed recovery process. Depending on how the group is accessed by clients, there is a possibility of DML statements being executed on the restored member once it becomes accessible on the network, prior to the member finishing its catch-up on the activities it has missed while off the group. To avoid this, before starting the restored server, configure the following system variables in the server option file:

```
group_replication_start_on_boot=OFF
super_read_only=ON
```

```
event_scheduler=OFF
```

These settings ensure that the member becomes read-only at startup, and that the event scheduler is turned off while the member catches up with the group during the distributed recovery process. Adequate error handling must also be provided for on the clients, since they are unable to perform DML operations during this period on the member being restored.

Once the restoration process is fully completed and the restored member is synchronized with the rest of the group, you can revert these changes. First, restart the event scheduler using the statement shown here:

```
mysql> SET global event_scheduler=ON;
```

After this, you should set the following system variables in the member's option file, so that they have the necessary values for the next time that the member is started:

```
group_replication_start_on_boot=ON
super_read_only=OFF
event_scheduler=ON
```

# <span id="page-157-0"></span>**20.6 Group Replication Security**

This section explains how to secure a group, securing the connections between members of a group, or by establishing a security perimeter using an IP address allowlist.

# <span id="page-157-1"></span>**20.6.1 Communication Stack for Connection Security Management**

From MySQL 8.0.27, Group Replication can secure group communication connections between members by one of the following methods:

- Using its own implementation of the security protocols, including TLS/SSL and the use of an allowlist for incoming Group Communication System (GCS) connections. This is the only option for MySQL 8.0.26 and earlier.
- Using MySQL Server's own connection security in place of Group Replication's implementation. Using the MySQL protocol means that standard methods of user authentication can be used for granting (or revoking) access to the group in place of the allowlist, and the latest functionality of the server's protocol is always available on release. This option is available from MySQL 8.0.27.

The choice is made by setting the system variable group\_replication\_communication\_stack to XCOM to use Group Replication's own implementation (this is the default choice), or to MYSQL to use MySQL Server's connection security.

The following additional configuration is required for a replication group to use the MySQL communication stack. It is especially important to make sure these requirements are all fulfilled when you switch from using the XCom communication stack to the MySQL communication stack for your group.

### **Group Replication Requirements For The MySQL Communication Stack**

- The network address configured by the group\_replication\_local\_address system variable for each group member must be set to one of the IP addresses and ports that MySQL Server is listening on, as specified by the bind\_address system variable for the server. The combination of IP address and port for each member must be unique in the group. It is recommended that the group\_replication\_group\_seeds system variable for each group member be configured to contain all the local addresses for all the group members.
- The MySQL communication stack supports network namespaces, which the XCom communication stack does not support. If network namespaces are used with the Group Replication local addresses for the group members (group\_replication\_local\_address), these must be configured for each group member using the CHANGE REPLICATION SOURCE TO statement. Also, the

report\_host server system variable for each group member must be set to report the namespace. All group members must use the same namespace to avoid possible issues with address resolution during distributed recovery.

- The group\_replication\_ssl\_mode system variable must be set to the required setting for group communications. This system variable controls whether TLS/SSL is enabled or disabled for group communications. For MySQL 8.0.26 and earlier, the TLS/SSL configuration is always taken from the server's SSL settings; for MySQL 8.0.27 and later, when the MySQL communication stack is used, the TLS/SSL configuration is taken from Group Replication's distributed recovery settings. This setting should be the same on all the group members, to avoid potential conflicts.
- The settings for the --ssl or --skip-ssl server option and for the require\_secure\_transport server system variable should be the same on all the group members, to avoid potential conflicts. If group\_replication\_ssl\_mode is set to REQUIRED, VERIFY\_CA, or VERIFY\_IDENTITY, use --ssl and require\_secure\_transport=ON. If group\_replication\_ssl\_mode is set to DISABLED, use require\_secure\_transport=OFF.
- If TLS/SSL is enabled for group communications, Group Replication's settings for securing distributed recovery must be configured if they are not already in place, or validated if they already are. The MySQL communication stack uses these settings not just for member-tomember distributed recovery connections, but also for TLS/SSL configuration in general group communications. group\_replication\_recovery\_use\_ssl and the other group\_replication\_recovery\_\* system variables are explained in [Section 20.6.3.2, "Secure](#page-165-0) [Socket Layer \(SSL\) Connections for Distributed Recovery"](#page-165-0).
- The Group Replication allowlist is not used when the group is using the MySQL communication stack, so the group\_replication\_ip\_allowlist and group\_replication\_ip\_whitelist system variables are ignored and need not be configured.
- The replication user account that Group Replication uses for distributed recovery, as configured using the CHANGE REPLICATION SOURCE TO statement, is used for authentication by the MySQL communication stack when setting up Group Replication connections. This user account, which is the same on all group members, must be given the following privileges:
  - GROUP\_REPLICATION\_STREAM. This privilege is required for the user account to be able to establish connections for Group Replication using the MySQL communication stack.
  - CONNECTION\_ADMIN. This privilege is required so that Group Replication connections are not terminated if one of the servers involved is placed in offline mode. If the MySQL communication stack is in use without this privilege, a member that is placed in offline mode is expelled from the group.

These are in addition to the privileges REPLICATION SLAVE and BACKUP\_ADMIN that all replication user accounts must have (see [Section 20.2.1.3, "User Credentials For Distributed Recovery"](#page-101-0)). When you add the new privileges, ensure that you skip binary logging on each group member by issuing SET SQL\_LOG\_BIN=0 before you issue the GRANT statements, and SET SQL\_LOG\_BIN=1 after them, so that the local transaction does not interfere with restarting Group Replication.

group\_replication\_communication\_stack is effectively a group-wide configuration setting, and the setting must be the same on all group members. However, this is not policed by Group Replication's own checks for group-wide configuration settings. A member with a different value from the rest of the group cannot communicate with the other members at all, because the communication protocols are incompatible, so it cannot exchange information about its configuration settings.

This means that although the value of the system variable can be changed while Group Replication is running, and takes effect after you restart Group Replication on the group member, the member still cannot rejoin the group until the setting has been changed on all the members. You must therefore stop Group Replication on all of the members and change the value of the system variable on them all before you can restart the group. Because all of the members are stopped, a full reboot of the group (a bootstrap by a server with group\_replication\_bootstrap\_group=ON) is required in order for

the value change to take effect. You can make the other required changes to settings on the group members while they are stopped.

For a running group, follow this procedure to change the value of group\_replication\_communication\_stack and the other required settings to migrate a group from the XCom communication stack to the MySQL communication stack, or from the MySQL communication stack to the XCom communication stack:

- 1. Stop Group Replication on each of the group members, using a STOP GROUP\_REPLICATION statement. Stop the primary member last, so that you do not trigger a new primary election and have to wait for that to complete.
- 2. On each of the group members, set the system variable group\_replication\_communication\_stack to the new communication stack, MYSQL or XCOM as appropriate. You can do this by editing the MySQL Server configuration file (typically named my.cnf on Linux and Unix systems, or my.ini on Windows systems), or by using a SET statement. For example:

```
SET PERSIST group_replication_communication_stack="MYSQL";
```

- 3. If you are migrating the replication group from the XCom communication stack (the default) to the MySQL communication stack, on each of the group members, configure or reconfigure the required system variables to appropriate settings, as described in the listing above. For example, the group\_replication\_local\_address system variable must be set to one of the IP addresses and ports that MySQL Server is listening on. Also configure any network namespaces using a CHANGE REPLICATION SOURCE TO statement.
- 4. If you are migrating the replication group from the XCom communication stack (the default) to the MySQL communication stack, on each of the group members, issue GRANT statements to give the replication user account the GROUP\_REPLICATION\_STREAM and CONNECTION\_ADMIN privileges. You will need to take the group members out of the read-only state that is applied when Group Replication is stopped. Also ensure that you skip binary logging on each group member by issuing SET SQL\_LOG\_BIN=0 before you issue the GRANT statements, and SET SQL\_LOG\_BIN=1 after them, so that the local transaction does not interfere with restarting Group Replication. For example:

```
SET GLOBAL SUPER_READ_ONLY=OFF;
SET SQL_LOG_BIN=0; 
GRANT GROUP_REPLICATION_STREAM ON *.* TO rpl_user@'%';
GRANT CONNECTION_ADMIN ON *.* TO rpl_user@'%';
SET SQL_LOG_BIN=1;
```

5. If you are migrating the replication group from the MySQL communication stack back to the XCom communication stack, on each of the group members, reconfigure the system variables in the requirements listing above to settings suitable for the XCom communication stack. Section 20.9, "Group Replication Variables" lists the system variables with their defaults and requirements for the XCom communication stack.

![](_page_159_Picture_10.jpeg)

#### **Note**

- The XCom communication stack does not support network namespaces, so the Group Replication local address (group\_replication\_local\_address system variable) cannot use these. Unset them by issuing a CHANGE REPLICATION SOURCE TO statement.
- When you move back to the XCom communication stack, the settings specified by group\_replication\_recovery\_use\_ssl and the other group\_replication\_recovery\_\* system variables are not used to secure group communications. Instead, the Group Replication system variable group\_replication\_ssl\_mode is used to activate the use of SSL for group communication connections and specify the security mode

for the connections, and the remainder of the configuration is taken from the server's SSL configuration. For details, see [Section 20.6.2, "Securing](#page-160-0) [Group Communication Connections with Secure Socket Layer \(SSL\)"](#page-160-0).

- 6. To restart the group, follow the process in [Section 20.5.2, "Restarting a Group"](#page-126-0), which explains how to safely bootstrap a group where transactions have been executed and certified. A bootstrap by a server with group\_replication\_bootstrap\_group=ON is necessary to change the communication stack, because all of the members must be shut down.
- 7. Members now connect to each other using the new communication stack. Any server that has group\_replication\_communication\_stack set (or defaulted, in the case of XCom) to the previous communication stack is no longer able to join the group. It is important to note that because Group Replication cannot even see the joining attempt, it does not check and reject the joining member with an error message. Instead, the attempted join fails silently when the previous communication stack gives up trying to contact the new one.

# <span id="page-160-0"></span>**20.6.2 Securing Group Communication Connections with Secure Socket Layer (SSL)**

Secure sockets can be used for group communication connections between members of a group.

The Group Replication system variable group\_replication\_ssl\_mode is used to activate the use of SSL for group communication connections and specify the security mode for the connections. This value should be the same on all group members; if it differs, some members may not be able to join the group. The default setting means that SSL is not used. This variable has the following possible values:

|  | Table 20.1 group_replication_ssl_mode configuration values |  |  |  |
|--|------------------------------------------------------------|--|--|--|
|  |                                                            |  |  |  |

| Value           | Description                                                                                                                             |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| DISABLED        | Establish an unencrypted connection (the default).                                                                                      |
| REQUIRED        | Establish a secure connection if the server<br>supports secure connections.                                                             |
| VERIFY_CA       | Like REQUIRED, but additionally verify the server<br>TLS certificate against the configured Certificate<br>Authority (CA) certificates. |
| VERIFY_IDENTITY | Like VERIFY_CA, but additionally verify that the<br>server certificate matches the host to which the<br>connection is attempted.        |

If SSL is used, the means for configuring the secure connection depends on whether the XCom or the MySQL communication stack is used for group communication (a choice between the two is available since MySQL 8.0.27).

#### **When using the XCom communication stack**

**(group\_replication\_communication\_stack=XCOM):** The remainder of the configuration for Group Replication's group communication connections is taken from the server's SSL configuration. For more information on the options for configuring the server SSL, see Command Options for Encrypted Connections. The server SSL options that are applied to Group Replication's group communication connections are as follows:

**Table 20.2 SSL Options**

| Server Configuration | Description                                            |
|----------------------|--------------------------------------------------------|
| ssl_key              | The path name of the SSL private key file in PEM       |
|                      | format. On the client side, this is the client private |
|                      | key. On the server side, this is the server private    |
|                      | key.                                                   |

| Server Configuration | Description                                                                                                                                                                                                |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ssl_cert             | The path name of the SSL public key certificate<br>file in PEM format. On the client side, this is the<br>client public key certificate. On the server side,<br>this is the server public key certificate. |
| ssl_ca               | The path name of the Certificate Authority (CA)<br>certificate file in PEM format.                                                                                                                         |
| ssl_capath           | The path name of the directory that contains<br>trusted SSL certificate authority (CA) certificate<br>files in PEM format.                                                                                 |
| ssl_crl              | The path name of the file containing certificate<br>revocation lists in PEM format.                                                                                                                        |
| ssl_crlpath          | The path name of the directory that contains<br>certificate revocation list files in PEM format.                                                                                                           |
| ssl_cipher           | A list of permissible ciphers for encrypted<br>connections.                                                                                                                                                |
| tls_version          | A list of the TLS protocols the server permits for<br>encrypted connections.                                                                                                                               |
| tls_ciphersuites     | Which TLSv1.3 ciphersuites the server permits for<br>encrypted connections.                                                                                                                                |

![](_page_161_Picture_2.jpeg)

#### **Important**

- Support for the TLSv1 and TLSv1.1 connection protocols is removed from MySQL Server as of MySQL 8.0.28. The protocols were deprecated from MySQL 8.0.26, though MySQL Server clients, including Group Replication server instances acting as a client, do not return warnings to the user if a deprecated TLS protocol version is used. See Removal of Support for the TLSv1 and TLSv1.1 Protocols for more information.
- Support for the TLSv1.3 protocol is available in MySQL Server as of MySQL 8.0.16, provided that MySQL Server was compiled using OpenSSL 1.1.1. The server checks the version of OpenSSL at startup, and if it is lower than 1.1.1, TLSv1.3 is removed from the default value for the server system variables relating to TLS versions (including the group\_replication\_recovery\_tls\_version system variable).
- Group Replication supports TLSv1.3 from MySQL 8.0.18. In MySQL 8.0.16 and MySQL 8.0.17, if the server supports TLSv1.3, the protocol is not supported in the group communication engine and cannot be used by Group Replication.
- In MySQL 8.0.18, TLSv1.3 can be used in Group Replication for the distributed recovery connection, but the group\_replication\_recovery\_tls\_version and group\_replication\_recovery\_tls\_ciphersuites system variables are not available. The donor servers must therefore permit the use of at least one TLSv1.3 ciphersuite that is enabled by default, as listed in Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". From MySQL 8.0.19, you can use the options to configure client support for any selection of ciphersuites, including only non-default ciphersuites if you want.
- In the list of TLS protocols specified in the tls\_version system variable, ensure the specified versions are contiguous (for example, TLSv1.2,TLSv1.3). If there are any gaps in the list of protocols (for

example, if you specified TLSv1,TLSv1.2, omitting TLS 1.1) Group Replication might be unable to make group communication connections.

In a replication group, OpenSSL negotiates the use of the highest TLS protocol that is supported by all members. A joining member that is configured to use only TLSv1.3 (tls\_version=TLSv1.3) cannot join a replication group where any existing member does not support TLSv1.3, because the group members in that case are using a lower TLS protocol version. To join the member to the group, you must configure the joining member to also permit the use of lower TLS protocol versions supported by the existing group members. Conversely, if a joining member does not support TLSv1.3, but the existing group members all do and are using that version for connections to each other, the member can join if the existing group members already permit the use of a suitable lower TLS protocol version, or if you configure them to do so. In that situation, OpenSSL uses a lower TLS protocol version for the connections from each member to the joining member. Each member's connections to other existing members continue to use the highest available protocol that both members support.

From MySQL 8.0.16, you can change the tls\_version system variable at runtime to alter the list of permitted TLS protocol versions for the server. Note that for Group Replication, the ALTER INSTANCE RELOAD TLS statement, which reconfigures the server's TLS context from the current values of the system variables that define the context, does not change the TLS context for Group Replication's group communication connection while Group Replication is running. To apply the reconfiguration to these connections, you must execute STOP GROUP\_REPLICATION followed by START GROUP\_REPLICATION to restart Group Replication on the member or members where you changed the tls\_version system variable. Similarly, if you want to make all members of a group change to using a higher or lower TLS protocol version, you must carry out a rolling restart of Group Replication on the members after changing the list of permitted TLS protocol versions, so that OpenSSL negotiates the use of the higher TLS protocol version when the rolling restart is completed. For instructions to change the list of permitted TLS protocol versions at runtime, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers" and Server-Side Runtime Configuration and Monitoring for Encrypted Connections.

The following example shows a section from a my.cnf file that configures SSL on a server, and activates SSL for Group Replication group communication connections:

```
[mysqld]
ssl_ca = "cacert.pem"
ssl_capath = "/.../ca_directory"
ssl_cert = "server-cert.pem"
ssl_cipher = "DHE-RSA-AEs256-SHA"
ssl_crl = "crl-server-revoked.crl"
ssl_crlpath = "/.../crl_directory"
ssl_key = "server-key.pem"
group_replication_ssl_mode= REQUIRED
```

![](_page_162_Picture_6.jpeg)

#### **Important**

The ALTER INSTANCE RELOAD TLS statement, which reconfigures the server's TLS context from the current values of the system variables that define the context, does not change the TLS context for Group Replication's group communication connections while Group Replication is running. To apply the reconfiguration to these connections, you must execute STOP GROUP\_REPLICATION followed by START GROUP\_REPLICATION to restart Group Replication.

Connections made between a joining member and an existing member for distributed recovery are not covered by the options described above. These connections use Group Replication's dedicated distributed recovery SSL options, which are described in [Section 20.6.3.2, "Secure Socket Layer \(SSL\)](#page-165-0) [Connections for Distributed Recovery".](#page-165-0)

**When using the MySQL communication stack (group\_replication\_communication\_stack=MYSQL):** The security settings for distributed recovery of the group are applied to the normal communications between group members. See [Section 20.6.3, "Securing Distributed Recovery Connections"](#page-163-0) on how to configure the security settings.

# <span id="page-163-0"></span>**20.6.3 Securing Distributed Recovery Connections**

![](_page_163_Picture_2.jpeg)

#### **Important**

When using the MySQL communication stack (group\_replication\_communication\_stack=MYSQL) AND secure connections between members (group\_replication\_ssl\_mode is not set to DISABLED), the security settings discussed in this section are applied not just to distributed recovery connections, but to group communications between members in general.

When a member joins the group, distributed recovery is carried out using a combination of a remote cloning operation, if available and appropriate, and an asynchronous replication connection. For a full description of distributed recovery, see [Section 20.5.4, "Distributed Recovery".](#page-134-0)

Up to MySQL 8.0.20, group members offer their standard SQL client connection to joining members for distributed recovery, as specified by MySQL Server's hostname and port system variables. From MySQL 8.0.21, group members may advertise an alternative list of distributed recovery endpoints as dedicated client connections for joining members. For more details, see [Section 20.5.4.1,](#page-135-0) ["Connections for Distributed Recovery"](#page-135-0). Notice that such connections offered to a joining member for distributed recovery is not the same connections that are used by Group Replication for communication between online members when the XCom communication stack is used for group communications (group\_replication\_communication\_stack=XCOM).

To secure distributed recovery connections in the group, ensure that user credentials for the replication user are properly secured, and use SSL for distributed recovery connections if possible.

# <span id="page-163-1"></span>**20.6.3.1 Secure User Credentials for Distributed Recovery**

State transfer from the binary log requires a replication user with the correct permissions so that Group Replication can establish direct member-to-member replication channels. The same replication user is used for distributed recovery on all the group members. If group members have been set up to support the use of a remote cloning operation as part of distributed recovery, which is available from MySQL 8.0.17, this replication user is also used as the clone user on the donor, and requires the correct permissions for this role too. For detailed instructions to set up this user, see [Section 20.2.1.3, "User](#page-101-0) [Credentials For Distributed Recovery"](#page-101-0).

To secure the user credentials, you can require SSL for connections with the user account, and (from MySQL 8.0.21) you can provide the user credentials when Group Replication is started, rather than storing them in the replica status tables. Also, if you are using caching SHA-2 authentication, you must set up RSA key-pairs on the group members.

![](_page_163_Picture_11.jpeg)

#### **Important**

When using the MySQL communication stack (group\_replication\_communication\_stack=MYSQL) AND secure connections between members (group\_replication\_ssl\_mode is not set to DISABLED), the recovery users must be properly set up, as they are also the users for group communications. Follow the instructions in [Replication User](#page-164-1) [With SSL](#page-164-1) and [Providing Replication User Credentials Securely.](#page-164-0)

#### <span id="page-163-2"></span>**Replication User With The Caching SHA-2 Authentication Plugin**

By default, users created in MySQL 8 use Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication". If the replication user you configure for distributed recovery uses the caching SHA-2 authentication plugin, and you are not using SSL for distributed recovery connections, RSA key-pairs are used for password exchange. For more information on RSA key-pairs, see Section 8.3.3, "Creating SSL and RSA Certificates and Keys".

In this situation, you can either copy the public key of the rpl\_user to the joining member, or configure the donors to provide the public key when requested. The more secure approach is to copy the public key of the replication user account to the joining member. Then you need to configure the group\_replication\_recovery\_public\_key\_path system variable on the joining member with the path to the public key for the replication user account.

The less secure approach is to set group\_replication\_recovery\_get\_public\_key=ON on donors so that they provide the public key of the replication user account to joining members. There is no way to verify the identity of a server, therefore only set group\_replication\_recovery\_get\_public\_key=ON when you are sure there is no risk of server identity being compromised, for example by a man-in-the-middle attack.

### <span id="page-164-1"></span>**Replication User With SSL**

A replication user that requires an SSL connection must be created before the server joining the group (the joining member) connects to the donor. Typically, this is set up at the time you are provisioning a server to join the group. To create a replication user for distributed recovery that requires an SSL connection, issue these statements on all servers that are going to participate in the group:

```
mysql> SET SQL_LOG_BIN=0;
mysql> CREATE USER 'rec_ssl_user'@'%' IDENTIFIED BY 'password' REQUIRE SSL;
mysql> GRANT REPLICATION SLAVE ON *.* TO 'rec_ssl_user'@'%';
mysql> GRANT CONNECTION_ADMIN ON *.* TO 'rec_ssl_user'@'%';
mysql> GRANT BACKUP_ADMIN ON *.* TO 'rec_ssl_user'@'%';
mysql> GRANT GROUP_REPLICATION_STREAM ON *.* TO rec_ssl_user@'%';
mysql> FLUSH PRIVILEGES;
mysql> SET SQL_LOG_BIN=1;
```

![](_page_164_Picture_6.jpeg)

#### **Note**

The GROUP\_REPLICATION\_STREAM privilege is required when using both the MySQL communication stack (group\_replication\_communication\_stack=MYSQL) and secure connections between members (group\_replication\_ssl\_mode not set to DISABLED). See [Section 20.6.1, "Communication Stack for Connection Security](#page-157-1) [Management".](#page-157-1)

#### <span id="page-164-0"></span>**Providing Replication User Credentials Securely**

To supply the user credentials for the replication user, you can set them permanently as the credentials for the group\_replication\_recovery channel, using a CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement. Alternatively, from MySQL 8.0.21, you can specify them on the START GROUP\_REPLICATION statement each time Group Replication is started. User credentials specified on START GROUP\_REPLICATION take precedence over any user credentials that have been set using a CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement.

User credentials set using CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO are stored in plain text in the replication metadata repositories on the server, but user credentials specified on START GROUP\_REPLICATION are saved in memory only, and are removed by a STOP GROUP\_REPLICATION statement or server shutdown. Using START GROUP\_REPLICATION to specify the user credentials therefore helps to secure the Group Replication servers against unauthorized access. However, this method is not compatible with starting Group Replication automatically, as specified by the group\_replication\_start\_on\_boot system variable.

If you want to set the user credentials permanently using a CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement, issue this statement on the member that is going to join the group:

```
mysql> CHANGE MASTER TO MASTER_USER='rec_ssl_user', MASTER_PASSWORD='password' 
 FOR CHANNEL 'group_replication_recovery';
Or from MySQL 8.0.23:
```

```
mysql> CHANGE REPLICATION SOURCE TO SOURCE_USER='rec_ssl_user', SOURCE_PASSWORD='password' 
 FOR CHANNEL 'group_replication_recovery';
```

To supply the user credentials on START GROUP\_REPLICATION, issue this statement when starting Group Replication for the first time, or after a server restart:

mysql> START GROUP\_REPLICATION USER='rec\_ssl\_user', PASSWORD='password';

![](_page_165_Picture_4.jpeg)

#### **Important**

If you switch to using START GROUP\_REPLICATION to specify user credentials on a server that previously supplied the credentials using CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO, you must complete the following steps to get the security benefits of this change.

- 1. Stop Group Replication on the group member using a STOP GROUP\_REPLICATION statement. Although it is possible to take the following two steps while Group Replication is running, you need to restart Group Replication to implement the changes.
- 2. Set the value of the group\_replication\_start\_on\_boot system variable to OFF (the default is ON).
- 3. Remove the distributed recovery credentials from the replica status tables by issuing this statement:

```
mysql> CHANGE MASTER TO MASTER_USER='', MASTER_PASSWORD='' 
 FOR CHANNEL 'group_replication_recovery';
Or from MySQL 8.0.23:
mysql> CHANGE REPLICATION SOURCE TO SOURCE_USER='', SOURCE_PASSWORD='' 
 FOR CHANNEL 'group_replication_recovery';
```

4. Restart Group Replication on the group member using a START GROUP\_REPLICATION statement that specifies the distributed recovery user credentials.

Without these steps, the credentials remain stored in the replica status tables, and can also be transferred to other group members during remote cloning operations for distributed recovery. The group\_replication\_recovery channel could then be inadvertently started with the stored credentials, on either the original member or members that were cloned from it. An automatic start of Group Replication on server boot (including after a remote cloning operation) would use the stored user credentials, and they would also be used if an operator did not specify the distributed recovery credentials as part of START GROUP\_REPLICATION.

# <span id="page-165-0"></span>**20.6.3.2 Secure Socket Layer (SSL) Connections for Distributed Recovery**

![](_page_165_Picture_14.jpeg)

#### **Important**

When using the MySQL communication stack (group\_replication\_communication\_stack=MYSQL) AND secure connections between members (group\_replication\_ssl\_mode is not set to DISABLED), the security settings discussed in this section are applied not just to distributed recovery connections, but to group communications between members in general. See [Section 20.6.1, "Communication Stack for Connection](#page-157-1) [Security Management".](#page-157-1)

Whether the distributed recovery connection is made using the standard SQL client connection or a distributed recovery endpoint, to configure the connection securely, you can use Group Replication's dedicated distributed recovery SSL options. These options correspond to the server SSL options that are used for group communication connections, but they are only applied for distributed recovery connections. By default, distributed recovery connections do not use SSL, even if you activated SSL for group communication connections, and the server SSL options are not applied for distributed recovery connections. You must configure these connections separately.

If a remote cloning operation is used as part of distributed recovery, Group Replication automatically configures the clone plugin's SSL options to match your settings for the distributed recovery SSL options. (For details of how the clone plugin uses SSL, see Configuring an Encrypted Connection for Cloning.)

The distributed recovery SSL options are as follows:

- group\_replication\_recovery\_use\_ssl: Set to ON to make Group Replication use SSL for distributed recovery connections, including remote cloning operations and state transfer from a donor's binary log. If the server you connect to does not use the default configuration for this (see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections"), use the other distributed recovery SSL options to determine which certificates and cipher suites to use.
- group\_replication\_recovery\_ssl\_ca: The path name of the Certificate Authority (CA) file to use for distributed recovery connections. Group Replication automatically configures the clone SSL option clone\_ssl\_ca to match this.
  - group\_replication\_recovery\_ssl\_capath: The path name of a directory that contains trusted SSL certificate authority (CA) certificate files.
- group\_replication\_recovery\_ssl\_cert: The path name of the SSL public key certificate file to use for distributed recovery connections. Group Replication automatically configures the clone SSL option clone\_ssl\_cert to match this.
- group\_replication\_recovery\_ssl\_key: The path name of the SSL private key file to use for distributed recovery connections. Group Replication automatically configures the clone SSL option clone\_ssl\_cert to match this.
- group\_replication\_recovery\_ssl\_verify\_server\_cert: Makes the distributed recovery connection check the server's Common Name value in the donor sent certificate. Setting this option to ON is the equivalent for distributed recovery connections of setting VERIFY\_IDENTITY for the group\_replication\_ssl\_mode option for group communication connections.
- group\_replication\_recovery\_ssl\_crl: The path name of a file containing certificate revocation lists.
- group\_replication\_recovery\_ssl\_crlpath: The path name of a directory containing certificate revocation lists.
- group\_replication\_recovery\_ssl\_cipher: A list of permissible ciphers for connection encryption for the distributed recovery connection. Specify a list of one or more cipher names, separated by colons. For information about which encryption ciphers MySQL supports, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".
- group\_replication\_recovery\_tls\_version: A comma-separated list of one or more permitted TLS protocols for connection encryption when this server instance is the client in the distributed recovery connection, that is, the joining member. The default for this system variable depends on the TLS protocol versions supported in the MySQL Server release. The group members involved in each distributed recovery connection as the client (joining member) and server (donor) negotiate the highest protocol version that they are both set up to support. This system variable is available from MySQL 8.0.19.
- group\_replication\_recovery\_tls\_ciphersuites: A colon-separated list of one or more permitted ciphersuites when TLSv1.3 is used for connection encryption for the distributed recovery connection, and this server instance is the client in the distributed recovery connection, that is, the joining member. If this system variable is set to NULL when TLSv1.3 is used (which is the default if you do not set the system variable), the ciphersuites that are enabled by default are allowed, as listed in Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". If this system variable is set to the empty string, no cipher suites are allowed, and TLSv1.3 is therefore not used. This system variable is available beginning with MySQL 8.0.19.

# <span id="page-167-0"></span>**20.6.4 Group Replication IP Address Permissions**

When and only when the XCom communication stack is used for establishing group communications (group\_replication\_communication\_stack=XCOM), the Group Replication plugin lets you specify an allowlist of hosts from which an incoming Group Communication System connection can be accepted. If you specify an allowlist on a server s1, then when server s2 is establishing a connection to s1 for the purpose of engaging group communication, s1 first checks the allowlist before accepting the connection from s2. If s2 is in the allowlist, then s1 accepts the connection, otherwise s1 rejects the connection attempt by s2. Beginning with MySQL 8.0.22, the system variable group\_replication\_ip\_allowlist is used to specify the allowlist, and for releases before MySQL 8.0.22, the system variable group\_replication\_ip\_whitelist is used. The new system variable works in the same way as the old system variable, only the terminology has changed.

![](_page_167_Picture_3.jpeg)

#### **Note**

When the MySQL communication stack is used for establishing group communications (group\_replication\_communication\_stack=MYSQL), the settings for group\_replication\_ip\_allowlist and group\_replication\_ip\_whitelist are ignored. See [Section 20.6.1,](#page-157-1) ["Communication Stack for Connection Security Management".](#page-157-1)

If you do not specify an allowlist explicitly, the group communication engine (XCom) automatically scans active interfaces on the host, and identifies those with addresses on private subnetworks, together with the subnet mask that is configured for each interface. These addresses, and the localhost IP address for IPv4 and (from MySQL 8.0.14) IPv6 are used to create an automatic Group Replication allowlist. The automatic allowlist therefore includes any IP addresses that are found for the host in the following ranges after the appropriate subnet mask has been applied:

```
IPv4 (as defined in RFC 1918)
10/8 prefix (10.0.0.0 - 10.255.255.255) - Class A
172.16/12 prefix (172.16.0.0 - 172.31.255.255) - Class B
192.168/16 prefix (192.168.0.0 - 192.168.255.255) - Class C
IPv6 (as defined in RFC 4193 and RFC 5156)
fc00:/7 prefix - unique-local addresses
fe80::/10 prefix - link-local unicast addresses
127.0.0.1 - localhost for IPv4
::1 - localhost for IPv6
```

An entry is added to the error log stating the addresses that have been allowed automatically for the host.

The automatic allowlist of private addresses cannot be used for connections from servers outside the private network, so a server, even if it has interfaces on public IPs, does not by default allow Group Replication connections from external hosts. For Group Replication connections between server instances that are on different machines, you must provide public IP addresses and specify these as an explicit allowlist. If you specify any entries for the allowlist, the private and localhost addresses are not added automatically, so if you use any of these, you must specify them explicitly.

To specify an allowlist manually, use the group\_replication\_ip\_allowlist (MySQL 8.0.22 and later) or group\_replication\_ip\_whitelist system variable. Before MySQL 8.0.24, you cannot change the allowlist on a server while it is an active member of a replication group. If the member is active, you must execute STOP GROUP\_REPLICATION before changing the allowlist, and START GROUP\_REPLICATION afterwards. From MySQL 8.0.24, you can change the allowlist while Group Replication is running.

The allowlist must contain the IP address or host name that is specified in each member's group\_replication\_local\_address system variable. This address is not the same as the MySQL server SQL protocol host and port, and is not specified in the bind\_address system variable for the server instance. If a host name used as the Group Replication local address for a server

instance resolves to both an IPv4 and an IPv6 address, the IPv4 address is preferred for Group Replication connections.

IP addresses specified as distributed recovery endpoints, and the IP address for the member's standard SQL client connection if that is used for distributed recovery (which is the default), do not need to be added to the allowlist. The allowlist is only for the address specified by group\_replication\_local\_address for each member. A joining member must have its initial connection to the group permitted by the allowlist in order to retrieve the address or addresses for distributed recovery.

In the allowlist, you can specify any combination of the following:

- IPv4 addresses (for example, 198.51.100.44)
- IPv4 addresses with CIDR notation (for example, 192.0.2.21/24)
- IPv6 addresses, from MySQL 8.0.14 (for example, 2001:db8:85a3:8d3:1319:8a2e:370:7348)
- IPv6 addresses with CIDR notation, from MySQL 8.0.14 (for example, 2001:db8:85a3:8d3::/64)
- Host names (for example, example.org)
- Host names with CIDR notation (for example, www.example.com/24)

Before MySQL 8.0.14, host names could only resolve to IPv4 addresses. From MySQL 8.0.14, host names can resolve to IPv4 addresses, IPv6 addresses, or both. If a host name resolves to both an IPv4 and an IPv6 address, the IPv4 address is always used for Group Replication connections. You can use CIDR notation in combination with host names or IP addresses to permit a block of IP addresses with a particular network prefix, but do ensure that all the IP addresses in the specified subnet are under your control.

![](_page_168_Picture_11.jpeg)

#### **Note**

When a connection attempt from an IP address is refused because the address is not in the allowlist, the refusal message always prints the IP address in IPv6 format. IPv4 addresses are preceded by ::ffff: in this format (an IPV4 mapped IPv6 address). You do not need to use this format to specify IPv4 addresses in the allowlist; use the standard IPv4 format for them.

A comma must separate each entry in the allowlist. For example:

mysql> SET GLOBAL group\_replication\_ip\_allowlist="192.0.2.21/24,198.51.100.44,203.0.113.0/24,2001:db8:85a3:8d3:1319:8a2e:370:7348,example.org,www.example.com/24";

To join a replication group, a server needs to be permitted on the seed member to which it makes the request to join the group. Typically, this would be the bootstrap member for the replication group, but it can be any of the servers listed by the group\_replication\_group\_seeds option in the configuration for the server joining the group. If any of the seed members for the group are listed in the group\_replication\_group\_seeds option with an IPv6 address when a joining member has an IPv4 group\_replication\_local\_address, or the reverse, you must also set up and permit an alternative address for the joining member for the protocol offered by the seed member (or a host name that resolves to an address for that protocol). This is because when a server joins a replication group, it must make the initial contact with the seed member using the protocol that the seed member advertises in the group\_replication\_group\_seeds option, whether that is IPv4 or IPv6. If a joining member does not have a permitted address for the appropriate protocol, its connection attempt is refused. For more information on managing mixed IPv4 and IPv6 replication groups, see [Section 20.5.5, "Support For IPv6 And For Mixed IPv6 And IPv4 Groups"](#page-149-0).

When a replication group is reconfigured (for example, when a new primary is elected or a member joins or leaves), the group members re-establish connections between themselves. If a group member is only permitted by servers that are no longer part of the replication group after the reconfiguration, it is unable to reconnect to the remaining servers in the replication group that do not permit it. To avoid this scenario entirely, specify the same allowlist for all servers that are members of the replication group.

![](_page_169_Picture_2.jpeg)

#### **Note**

It is possible to configure different allowlists on different group members according to your security requirements, for example, in order to keep different subnets separate. If you need to configure different allowlists to meet your security requirements, ensure that there is sufficient overlap between the allowlists in the replication group to maximize the possibility of servers being able to reconnect in the absence of their original seed member.

For host names, name resolution takes place only when a connection request is made by another server. A host name that cannot be resolved is not considered for allowlist validation, and a warning message is written to the error log. Forward-confirmed reverse DNS (FCrDNS) verification is carried out for resolved host names.

![](_page_169_Picture_6.jpeg)

#### **Warning**

Host names are inherently less secure than IP addresses in an allowlist. FCrDNS verification provides a good level of protection, but can be compromised by certain types of attack. Specify host names in your allowlist only when strictly necessary, and ensure that all components used for name resolution, such as DNS servers, are maintained under your control. You can also implement name resolution locally using the hosts file, to avoid the use of external components.

# <span id="page-169-0"></span>**20.7 Group Replication Performance and Troubleshooting**

Group Replication is designed to create fault-tolerant systems with built-in failure detection and automated recovery. If a member server instance leaves voluntarily or stops communicating with the group, the remaining members agree a reconfiguration of the group between themselves, and choose a new primary if needed. Expelled members automatically attempt to rejoin the group, and are brought up to date by distributed recovery. If a group experiences a level of difficulties such that it cannot contact a majority of its members in order to agree on a decision, it identifies itself as having lost quorum and stops processing transactions. Group Replication also has built-in mechanisms and settings to help the group adapt to and manage variations in workload and message size, and stay within the limitations of the underlying system and networking resources.

The default settings for Group Replication's system variables are designed to maximize a group's performance and autonomy. The information in this section is to help you configure a replication group to optimize the automatic handling of any recurring issues that you experience on your particular systems, such as transient network outages or workloads and transactions that exceed a server instance's resources.

If you find that group members are being expelled and rejoining the group more frequently than you would like, it is possible that Group Replication's default failure detection settings are too sensitive for your system. This might be the case on slower networks or machines, networks with a high rate of unexpected transient outages, or during planned network outages. For advice on dealing with that situation by adjusting the settings, see [Section 20.7.7, "Responses to Failure Detection and Network](#page-177-0) [Partitioning"](#page-177-0).

You should only need to intervene manually in a Group Replication setup if something happens that the group cannot deal with automatically. Some key issues that can require administrator intervention are when a member is in ERROR status and cannot rejoin the group, or when a network partition causes the group to lose quorum.

• If an otherwise correctly functioning and configured member is unable to join or rejoin the group using distributed recovery, and remains in ERROR status, [Section 20.5.4.4, "Fault Tolerance for](#page-143-0)

[Distributed Recovery"](#page-143-0), explains the possible issues. One likely cause is that the joining member has extra transactions that are not present on the existing members of the group. For advice on dealing with that situation, see [Section 20.4.1, "GTIDs and Group Replication"](#page-117-0).

• If a group has lost quorum, this may be due to a network partition that divides the group into two parts, or possibly due to the failure of the majority of the servers. For advice on dealing with that situation, see [Section 20.7.8, "Handling a Network Partition and Loss of Quorum".](#page-183-0)

# <span id="page-170-0"></span>**20.7.1 Fine Tuning the Group Communication Thread**

The group communication thread (GCT) runs in a loop while the Group Replication plugin is loaded. The GCT receives messages from the group and from the plugin, handles quorum and failure detection related tasks, sends out some keep alive messages and also handles the incoming and outgoing transactions from/to the server/group. The GCT waits for incoming messages in a queue. When there are no messages, the GCT waits. By configuring this wait to be a little longer (doing an active wait) before actually going to sleep can prove to be beneficial in some cases. This is because the alternative is for the operating system to switch out the GCT from the processor and do a context switch.

To force the GCT to do an active wait, use the group\_replication\_poll\_spin\_loops option, which makes the GCT loop, doing nothing relevant for the configured number of loops, before actually polling the queue for the next message.

For example:

mysql> SET GLOBAL group\_replication\_poll\_spin\_loops= 10000;

# <span id="page-170-1"></span>**20.7.2 Flow Control**

MySQL Group Replication ensures that a transaction commits only after a majority of the members in a group have received it and agreed on the relative order amongst all transactions sent concurrently. This approach works well if the total number of writes to the group does not exceed the write capacity of any member in the group. If it does, and some members have less write throughput than others particularly less than the writer members—these members may start lagging behind the writers.

When some members lag behind the rest of the group, reads on such members may externalize very old data. Depending on why the member is lagging behind, other members in the group may have to save more or less of the replication context to be able to fulfil potential data transfer requests from the slow member.

The replication protocol provides a mechanism to avoid having too much distance, in terms of transactions applied, between fast and slow members. This is known as the flow control mechanism, which has the following objectives:

- 1. To keep members close, to minimize buffering and desynchronization between them
- 2. To adapt quickly to changing conditions like different workloads or more writers in the group
- 3. To give each member a share of the available write capacity
- 4. Not to reduce throughput more than strictly necessary to avoid wasting resources

Given the design of Group Replication, the decision whether to throttle, or not, may be made taking into account two work queues, the certification queue, and the binary log applier queue. Whenever the size of one of these queues exceeds the user-defined threshold, the throttling mechanism is triggered.

Flow control depends on two basic mechanisms:

1. Monitoring of members to collect statistics on throughput and queue sizes of all group members to make educated guesses concerning the maximum write pressure to which each member should be subjected

2. Throttling of members that are trying to write beyond their alloted shares of the available capacity at each moment in time