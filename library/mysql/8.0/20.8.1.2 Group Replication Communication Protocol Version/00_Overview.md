---
source: MySQL 8.0 Reference
title: 00_Overview
---

A replication group uses a Group Replication communication protocol version that can differ from the MySQL Server version of the members. To check the group's communication protocol version, issue the following statement on any member:

**SELECT group\_replication\_get\_communication\_protocol();**

The return value shows the oldest MySQL Server version that can join this group and use the group's communication protocol. Versions from MySQL 5.7.14 allow compression of messages, and versions from MySQL 8.0.16 also allow fragmentation of messages. Note that the group\_replication\_get\_communication\_protocol() function returns the minimum MySQL version that the group supports, which might differ from the version number that was passed to the group\_replication\_set\_communication\_protocol() function, and from the MySQL Server version that is installed on the member where you use the function.

When you upgrade all the members of a replication group to a new MySQL Server release, the Group Replication communication protocol version is not automatically upgraded, in case there is still a requirement to allow members at earlier releases to join. If you do not need to support older members and want to allow the upgraded members to use any added communication capabilities, after the upgrade use the group\_replication\_set\_communication\_protocol() function to upgrade the communication protocol, specifying the new MySQL Server version to which you have upgraded the members. For more information, see [Section 20.5.1.4, "Setting a Group's Communication Protocol](#page-123-0) [Version"](#page-123-0).

# <span id="page-198-0"></span>**20.8.2 Group Replication Offline Upgrade**

To perform an offline upgrade of a Group Replication group, you remove each member from the group, perform an upgrade of the member and then restart the group as usual. In a multi-primary group you can shutdown the members in any order. In a single-primary group, shutdown each secondary first and then finally the primary. See [Section 20.8.3.2, "Upgrading a Group Replication Member"](#page-199-1) for how to remove members from a group and shutdown MySQL.

Once the group is offline, upgrade all of the members. See Chapter 3, Upgrading MySQL for how to perform an upgrade. When all members have been upgraded, restart the members.

If you upgrade all the members of a replication group when they are offline and then restart the group, the members join using the new release's Group Replication communication protocol version, so that becomes the group's communication protocol version. If you have a requirement to allow members at earlier releases to join, you can use the group\_replication\_set\_communication\_protocol() function to downgrade the communication protocol version, specifying the MySQL Server version of the prospective group member that has the oldest installed server version.

# <span id="page-199-0"></span>**20.8.3 Group Replication Online Upgrade**

When you have a group running which you want to upgrade but you need to keep the group online to serve your application, you need to consider your approach to the upgrade. This section describes the different elements involved in an online upgrade, and various methods of how to upgrade your group.