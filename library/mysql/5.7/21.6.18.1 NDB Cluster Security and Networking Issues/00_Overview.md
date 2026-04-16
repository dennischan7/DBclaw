---
source: MySQL 5.7 Reference
title: 00_Overview
---

In this section, we discuss basic network security issues as they relate to NDB Cluster. It is extremely important to remember that NDB Cluster "out of the box" is not secure; you or your network administrator must take the proper steps to ensure that your cluster cannot be compromised over the network.

Cluster communication protocols are inherently insecure, and no encryption or similar security measures are used in communications between nodes in the cluster. Because network speed and latency have a direct impact on the cluster's efficiency, it is also not advisable to employ SSL or other encryption to network connections between nodes, as such schemes effectively slow communications.

It is also true that no authentication is used for controlling API node access to an NDB Cluster. As with encryption, the overhead of imposing authentication requirements would have an adverse impact on Cluster performance.

In addition, there is no checking of the source IP address for either of the following when accessing the cluster:

• SQL or API nodes using "free slots" created by empty [mysqld] or [api] sections in the config.ini file

This means that, if there are any empty [mysqld] or [api] sections in the config.ini file, then any API nodes (including SQL nodes) that know the management server's host name (or IP address) and port can connect to the cluster and access its data without restriction. (See [Section 21.6.18.2,](#page-102-0) ["NDB Cluster and MySQL Privileges",](#page-102-0) for more information about this and related issues.)

![](_page_99_Picture_18.jpeg)

### **Note**

 You can exercise some control over SQL and API node access to the cluster by specifying a HostName parameter for all [mysqld] and [api] sections in the config.ini file. However, this also means that, should you wish to connect an API node to the cluster from a previously unused host, you need to add an [api] section containing its host name to the config.ini file.

More information is available elsewhere in this chapter about the HostName parameter. Also see Section 21.4.1, "Quick Test Setup of NDB Cluster", for configuration examples using HostName with API nodes.

• Any ndb\_mgm client

This means that any cluster management client that is given the management server's host name (or IP address) and port (if not the standard port) can connect to the cluster and execute any management client command. This includes commands such as ALL STOP and SHUTDOWN.

 For these reasons, it is necessary to protect the cluster on the network level. The safest network configuration for Cluster is one which isolates connections between Cluster nodes from any other network communications. This can be accomplished by any of the following methods:

1. Keeping Cluster nodes on a network that is physically separate from any public networks. This option is the most dependable; however, it is the most expensive to implement.

We show an example of an NDB Cluster setup using such a physically segregated network here:

**Figure 21.9 NDB Cluster with Hardware Firewall**

![](_page_100_Figure_7.jpeg)

This setup has two networks, one private (solid box) for the Cluster management servers and data nodes, and one public (dotted box) where the SQL nodes reside. (We show the management and data nodes connected using a gigabit switch since this provides the best performance.) Both networks are protected from the outside by a hardware firewall, sometimes also known as a network-based firewall.

This network setup is safest because no packets can reach the cluster's management or data nodes from outside the network—and none of the cluster's internal communications can reach the outside—without going through the SQL nodes, as long as the SQL nodes do not permit any packets to be forwarded. This means, of course, that all SQL nodes must be secured against hacking attempts.

![](_page_100_Picture_10.jpeg)

### **Important**

With regard to potential security vulnerabilities, an SQL node is no different from any other MySQL server. See Section 6.1.3, "Making MySQL Secure Against Attackers", for a description of techniques you can use to secure MySQL servers.

2. Using one or more software firewalls (also known as host-based firewalls) to control which packets pass through to the cluster from portions of the network that do not require access to it. In this type of setup, a software firewall must be installed on every host in the cluster which might otherwise be accessible from outside the local network.

The host-based option is the least expensive to implement, but relies purely on software to provide protection and so is the most difficult to keep secure.

This type of network setup for NDB Cluster is illustrated here:

**Figure 21.10 NDB Cluster with Software Firewalls**

![](_page_101_Figure_3.jpeg)

Using this type of network setup means that there are two zones of NDB Cluster hosts. Each cluster host must be able to communicate with all of the other machines in the cluster, but only those hosting SQL nodes (dotted box) can be permitted to have any contact with the outside, while those in the zone containing the data nodes and management nodes (solid box) must be isolated from any machines that are not part of the cluster. Applications using the cluster and user of those applications must not be permitted to have direct access to the management and data node hosts.

To accomplish this, you must set up software firewalls that limit the traffic to the type or types shown in the following table, according to the type of node that is running on each cluster host computer:

**Table 21.62 Node types in a host-based firewall cluster configuration**

| Node Type                    | Permitted Traffic                                                                                                                |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| SQL or API node              | •<br>It originates from the IP address of a<br>management or data node (using any TCP or<br>UDP port).                           |
|                              | •<br>It originates from within the network in which<br>the cluster resides and is on the port that your<br>application is using. |
| Data node or Management node | •<br>It originates from the IP address of a<br>management or data node (using any TCP or<br>UDP port).                           |
|                              | •<br>It originates from the IP address of an SQL or<br>API node.                                                                 |

Any traffic other than that shown in the table for a given node type should be denied.

The specifics of configuring a firewall vary from firewall application to firewall application, and are beyond the scope of this Manual. iptables is a very common and reliable firewall application, which is often used with APF as a front end to make configuration easier. You can (and should) consult the documentation for the software firewall that you employ, should you choose to

implement an NDB Cluster network setup of this type, or of a "mixed" type as discussed under the next item.

3. It is also possible to employ a combination of the first two methods, using both hardware and software to secure the cluster—that is, using both network-based and host-based firewalls. This is between the first two schemes in terms of both security level and cost. This type of network setup keeps the cluster behind the hardware firewall, but permits incoming packets to travel beyond the router connecting all cluster hosts to reach the SQL nodes.

One possible network deployment of an NDB Cluster using hardware and software firewalls in combination is shown here:

![](_page_102_Picture_4.jpeg)

**Figure 21.11 NDB Cluster with a Combination of Hardware and Software Firewalls**

In this case, you can set the rules in the hardware firewall to deny any external traffic except to SQL nodes and API nodes, and then permit traffic to them only on the ports required by your application.

Whatever network configuration you use, remember that your objective from the viewpoint of keeping the cluster secure remains the same—to prevent any unessential traffic from reaching the cluster while ensuring the most efficient communication between the nodes in the cluster.

 Because NDB Cluster requires large numbers of ports to be open for communications between nodes, the recommended option is to use a segregated network. This represents the simplest way to prevent unwanted traffic from reaching the cluster.

![](_page_102_Picture_9.jpeg)

### **Note**

 If you wish to administer an NDB Cluster remotely (that is, from outside the local network), the recommended way to do this is to use ssh or another secure login shell to access an SQL node host. From this host, you can then run the management client to access the management server safely, from within the cluster's own local network.

Even though it is possible to do so in theory, it is not recommended to use ndb\_mgm to manage a Cluster directly from outside the local network on which the Cluster is running. Since neither authentication nor encryption takes place between the management client and the management server, this represents an extremely insecure means of managing the cluster, and is almost certain to be compromised sooner or later.

# <span id="page-102-0"></span>**21.6.18.2 NDB Cluster and MySQL Privileges**

In this section, we discuss how the MySQL privilege system works in relation to NDB Cluster and the implications of this for keeping an NDB Cluster secure.

 Standard MySQL privileges apply to NDB Cluster tables. This includes all MySQL privilege types (SELECT privilege, UPDATE privilege, DELETE privilege, and so on) granted on the database, table, and column level. As with any other MySQL Server, user and privilege information is stored in the mysql system database. The SQL statements used to grant and revoke privileges on NDB tables, databases containing such tables, and columns within such tables are identical in all respects with the GRANT and REVOKE statements used in connection with database objects involving any (other) MySQL storage engine. The same thing is true with respect to the CREATE USER and DROP USER statements.

 It is important to keep in mind that, by default, the MySQL grant tables use the MyISAM storage engine. Because of this, those tables are not normally duplicated or shared among MySQL servers acting as SQL nodes in an NDB Cluster. In other words, changes in users and their privileges do not automatically propagate between SQL nodes by default. If you wish, you can enable automatic distribution of MySQL users and privileges across NDB Cluster SQL nodes; see [Section 21.6.13,](#page-7-0) ["Distributed Privileges Using Shared Grant Tables",](#page-7-0) for details.

 Conversely, because there is no way in MySQL to deny privileges (privileges can either be revoked or not granted in the first place, but not denied as such), there is no special protection for NDB tables on one SQL node from users that have privileges on another SQL node; (This is true even if you are not using automatic distribution of user privileges. The definitive example of this is the MySQL root account, which can perform any action on any database object. In combination with empty [mysqld] or [api] sections of the config.ini file, this account can be especially dangerous. To understand why, consider the following scenario:

- The config.ini file contains at least one empty [mysqld] or [api] section. This means that the NDB Cluster management server performs no checking of the host from which a MySQL Server (or other API node) accesses the NDB Cluster.
- There is no firewall, or the firewall fails to protect against access to the NDB Cluster from hosts external to the network.
- The host name or IP address of the NDB Cluster management server is known or can be determined from outside the network.

If these conditions are true, then anyone, anywhere can start a MySQL Server with --ndbcluster --ndb-connectstring=management\_host and access this NDB Cluster. Using the MySQL root account, this person can then perform the following actions:

- Execute metadata statements such as SHOW DATABASES statement (to obtain a list of all NDB databases on the server) or SHOW TABLES FROM some\_ndb\_database statement to obtain a list of all NDB tables in a given database
- Run any legal MySQL statements on any of the discovered tables, such as:
  - SELECT \* FROM some\_table to read all the data from any table
  - DELETE FROM some\_table to delete all the data from a table
  - DESCRIBE some\_table or SHOW CREATE TABLE some\_table to determine the table schema
  - UPDATE some\_table SET column1 = some\_value to fill a table column with "garbage" data; this could actually cause much greater damage than simply deleting all the data

More insidious variations might include statements like these:

```
UPDATE some_table SET an_int_column = an_int_column + 1
or
UPDATE some_table SET a_varchar_column = REVERSE(a_varchar_column)
```

Such malicious statements are limited only by the imagination of the attacker.

The only tables that would be safe from this sort of mayhem would be those tables that were created using storage engines other than NDB, and so not visible to a "rogue" SQL node.

 A user who can log in as root can also access the INFORMATION\_SCHEMA database and its tables, and so obtain information about databases, tables, stored routines, scheduled events, and any other database objects for which metadata is stored in INFORMATION\_SCHEMA.

It is also a very good idea to use different passwords for the root accounts on different NDB Cluster SQL nodes unless you are using distributed privileges.

In sum, you cannot have a safe NDB Cluster if it is directly accessible from outside your local network.

![](_page_104_Picture_6.jpeg)

### **Important**

Never leave the MySQL root account password empty. This is just as true when running MySQL as an NDB Cluster SQL node as it is when running it as a standalone (non-Cluster) MySQL Server, and should be done as part of the MySQL installation process before configuring the MySQL Server as an SQL node in an NDB Cluster.

If you wish to employ NDB Cluster's distributed privilege capabilities, you should not simply convert the system tables in the mysql database to use the NDB storage engine manually. Use the stored procedure provided for this purpose instead; see [Section 21.6.13, "Distributed Privileges Using Shared](#page-7-0) [Grant Tables"](#page-7-0).

Otherwise, if you need to synchronize mysql system tables between SQL nodes, you can use standard MySQL replication to do so, or employ a script to copy table entries between the MySQL servers.

**Summary.** The most important points to remember regarding the MySQL privilege system with regard to NDB Cluster are listed here:

- 1. Users and privileges established on one SQL node do not automatically exist or take effect on other SQL nodes in the cluster. Conversely, removing a user or privilege on one SQL node in the cluster does not remove the user or privilege from any other SQL nodes.
- 2. You can distribute MySQL users and privileges among SQL nodes using the SQL script, and the stored procedures it contains, that are supplied for this purpose in the NDB Cluster distribution.
- 3. Once a MySQL user is granted privileges on an NDB table from one SQL node in an NDB Cluster, that user can "see" any data in that table regardless of the SQL node from which the data originated, even if you are not using privilege distribution.