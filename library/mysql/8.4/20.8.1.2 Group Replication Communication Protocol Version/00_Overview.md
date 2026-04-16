---
source: MySQL 8.4 Reference
title: 00_Overview
---

A replication group uses a Group Replication communication protocol version that differs from the MySQL Server version of the members. To check the group's communication protocol version, issue the following statement on any member:

```
SELECT @@version, group_replication_get_communication_protocol();
+------------------------------------------------------------+
| @@version | group_replication_get_communication_protocol() |
+------------------------------------------------------------+
| 8.4.0 | 8.0.27 |
+------------------------------------------------------------+
```

As demonstrated, the MySQL 8.4 LTS series uses the 8.0.27 communication protocol.

For more information, see [Section 20.5.1.4, "Setting a Group's Communication Protocol Version"](#page-47-0).

# <span id="page-119-0"></span>**20.8.2 Group Replication Offline Upgrade**

To perform an offline upgrade of a Group Replication group, you remove each member from the group, perform an upgrade of the member and then restart the group as usual. In a multi-primary group you can shutdown the members in any order. In a single-primary group, shutdown each secondary first and then finally the primary. See [Section 20.8.3.2, "Upgrading a Group Replication Member"](#page-120-0) for how to remove members from a group and shutdown MySQL.

Once the group is offline, upgrade all of the members. See Chapter 3, Upgrading MySQL for how to perform an upgrade. When all members have been upgraded, restart the members.

If you upgrade all the members of a replication group when they are offline and then restart the group, the members join using the new release's Group Replication communication protocol version, so that becomes the group's communication protocol version. If you have a requirement to allow members at earlier releases to join, you can use the group\_replication\_set\_communication\_protocol() function to downgrade the communication protocol version, specifying the MySQL Server version of the prospective group member that has the oldest installed server version.

# <span id="page-119-1"></span>**20.8.3 Group Replication Online Upgrade**

When you have a group running which you want to upgrade but you need to keep the group online to serve your application, you need to consider your approach to the upgrade. This section describes the different elements involved in an online upgrade, and various methods of how to upgrade your group.