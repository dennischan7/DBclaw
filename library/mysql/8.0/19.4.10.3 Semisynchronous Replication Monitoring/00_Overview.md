---
source: MySQL 8.0 Reference
title: 00_Overview
---

The plugins for semisynchronous replication expose a number of status variables that enable you to monitor their operation. To check the current values of the status variables, use SHOW STATUS:

```
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
```

Beginning with MySQL 8.0.26, new versions of the source and replica plugins are supplied, which replace the terms "master" and "slave" with "source" and "replica" in system variables and status variables. If you install the new rpl\_semi\_sync\_source and rpl\_semi\_sync\_replica plugins, the new system variables and status variables are available but the old ones are not. If you install the old rpl\_semi\_sync\_master and rpl\_semi\_sync\_slave plugins, the old system variables and status variables are available but the new ones are not. You cannot have both the new and the old version of the relevant plugin installed on an instance.

All Rpl\_semi\_sync\_xxx status variables are described at Section 7.1.10, "Server Status Variables". Some examples are:

• Rpl\_semi\_sync\_source\_clients or Rpl\_semi\_sync\_master\_clients

The number of semisynchronous replicas that are connected to the source server.

• Rpl\_semi\_sync\_source\_status or Rpl\_semi\_sync\_master\_status

Whether semisynchronous replication currently is operational on the source server. The value is 1 if the plugin has been enabled and a commit acknowledgment has not occurred. It is 0 if the plugin is not enabled or the source has fallen back to asynchronous replication due to commit acknowledgment timeout.

• Rpl\_semi\_sync\_source\_no\_tx or Rpl\_semi\_sync\_master\_no\_tx

The number of commits that were not acknowledged successfully by a replica.

• Rpl\_semi\_sync\_source\_yes\_tx or Rpl\_semi\_sync\_master\_yes\_tx

The number of commits that were acknowledged successfully by a replica.

• Rpl\_semi\_sync\_replica\_status or Rpl\_semi\_sync\_slave\_status

Whether semisynchronous replication currently is operational on the replica. This is 1 if the plugin has been enabled and the replication I/O (receiver) thread is running, 0 otherwise.

When the source switches between asynchronous or semisynchronous replication due to commitblocking timeout or a replica catching up, it sets the value of the Rpl\_semi\_sync\_source\_status or Rpl\_semi\_sync\_master\_status status variable appropriately. Automatic fallback from semisynchronous to asynchronous replication on the source means that it is possible for the rpl\_semi\_sync\_source\_enabled or rpl\_semi\_sync\_master\_enabled system variable to have a value of 1 on the source side even when semisynchronous replication is in fact not operational at the moment. You can monitor the Rpl\_semi\_sync\_source\_status or Rpl\_semi\_sync\_master\_status status variable to determine whether the source currently is using asynchronous or semisynchronous replication.