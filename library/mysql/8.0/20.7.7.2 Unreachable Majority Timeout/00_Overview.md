---
source: MySQL 8.0 Reference
title: 00_Overview
---

By default, members that find themselves in a minority due to a network partition do not automatically leave the group. You can use the system variable group\_replication\_unreachable\_majority\_timeout to set a number of seconds for a member to wait after losing contact with the majority of group members, and then exit the group. Setting a timeout means you do not need to pro-actively monitor for servers that are in a minority group after a network partition, and you can avoid the possibility of creating a split-brain situation (with two versions of the group membership) due to inappropriate intervention.

When the timeout specified by group\_replication\_unreachable\_majority\_timeout elapses, all pending transactions that have been processed by the member and the others in the minority group are rolled back, and the servers in that group move to the ERROR state. You can use the group\_replication\_autorejoin\_tries system variable, which is available from MySQL 8.0.16,

to make the member automatically try to rejoin the group at this point. From MySQL 8.0.21, this feature is activated by default and the member makes three auto-rejoin attempts. If the auto-rejoin procedure does not succeed or is not attempted, the minority member then follows the exit action specified by group\_replication\_exit\_state\_action.

Consider the following points when deciding whether or not to set an unreachable majority timeout:

- In a symmetric group, for example a group with two or four servers, if both partitions contain an equal number of servers, both groups consider themselves to be in a minority and enter the ERROR state. In this situation, the group has no functional partition.
- While a minority group exists, any transactions processed by the minority group are accepted, but blocked because the minority servers cannot reach quorum, until either STOP GROUP\_REPLICATION is issued on those servers or the unreachable majority timeout is reached.
- If you do not set an unreachable majority timeout, the servers in the minority group never enter the ERROR state automatically, and you must stop them manually.
- Setting an unreachable majority timeout has no effect if it is set on the servers in the minority group after the loss of majority has been detected.

If you do not use the group\_replication\_unreachable\_majority\_timeoutsystem variable, the process for operator invention in the event of a network partition is described in [Section 20.7.8,](#page-183-0) ["Handling a Network Partition and Loss of Quorum".](#page-183-0) The process involves checking which servers are functioning and forcing a new group membership if necessary.