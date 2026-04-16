---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes sample queries using the instruments and events for monitoring Group Replication memory usage. The queries retrieve data from the memory\_summary\_global\_by\_event\_name table.

The memory data can be queried for individual events, for example:

```
SELECT * FROM performance_schema.memory_summary_global_by_event_name
WHERE EVENT_NAME = 'memory/group_rpl/write_set_encoded'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/write_set_encoded
 COUNT_ALLOC: 1
 COUNT_FREE: 0
 SUM_NUMBER_OF_BYTES_ALLOC: 45
 SUM_NUMBER_OF_BYTES_FREE: 0
 LOW_COUNT_USED: 0
 CURRENT_COUNT_USED: 1
 HIGH_COUNT_USED: 1
 LOW_NUMBER_OF_BYTES_USED: 0
CURRENT_NUMBER_OF_BYTES_USED: 45
 HIGH_NUMBER_OF_BYTES_USED: 45
```

See Section 29.12.20.10, "Memory Summary Tables" for more information on the columns.

You can also define queries which sum various events to provide overviews of specific areas of memory usage.

The following examples are described:

- [Memory Used to Capture Transactions](#page-111-0)
- [Memory Used to Broadcast Transactions](#page-112-0)
- [Total Memory Used in Group Replication](#page-113-0)
- [Memory Used in Certification](#page-113-1)
- [Memory Used in Certification](#page-113-1)
- [Memory Used in Replication Pipeline](#page-114-0)
- [Memory Used in Consistency](#page-114-1)
- [Memory Used in Delivery Message Service](#page-115-0)
- [Memory Used to Broadcast and Receive Transactions](#page-116-0)

### <span id="page-111-0"></span>**Memory Used to Capture Transactions**

The memory allocated to capture user transactions is a sum of the write\_set\_encoded, write\_set\_extraction, and Log\_event event's values. For example:

```
SELECT * FROM (SELECT
 (CASE
 WHEN EVENT_NAME LIKE 'memory/group_rpl/write_set_encoded'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/sql/write_set_extraction'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/sql/Log_event'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME,
```

```
 SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME LIKE 'memory/group_rpl/write_set_encoded'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/sql/write_set_extraction'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/sql/Log_event'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/memory_gr
 SUM(COUNT_ALLOC): 127
 SUM(COUNT_FREE): 117
 SUM(SUM_NUMBER_OF_BYTES_ALLOC): 54808
 SUM(SUM_NUMBER_OF_BYTES_FREE): 52051
 SUM(LOW_COUNT_USED): 0
 SUM(CURRENT_COUNT_USED): 10
 SUM(HIGH_COUNT_USED): 35
 SUM(LOW_NUMBER_OF_BYTES_USED): 0
SUM(CURRENT_NUMBER_OF_BYTES_USED): 2757
 SUM(HIGH_NUMBER_OF_BYTES_USED): 15630
```

### <span id="page-112-0"></span>**Memory Used to Broadcast Transactions**

The memory allocated to broadcast transactions is a sum of the Gcs\_message\_data::m\_buffer, transaction\_data, and GCS\_XCom::xcom\_cache event values. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/Gcs_message_data::m_buffer'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/group_rpl/GCS_XCom::xcom_cache'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/group_rpl/transaction_data'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, 
 SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/Gcs_message_data::m_buffer'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/group_rpl/GCS_XCom::xcom_cache'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/group_rpl/transaction_data'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/memory_gr
 SUM(COUNT_ALLOC): 84
 SUM(COUNT_FREE): 31
 SUM(SUM_NUMBER_OF_BYTES_ALLOC): 1072324
```

```
 SUM(SUM_NUMBER_OF_BYTES_FREE): 7149
 SUM(LOW_COUNT_USED): 0
 SUM(CURRENT_COUNT_USED): 53
 SUM(HIGH_COUNT_USED): 59
 SUM(LOW_NUMBER_OF_BYTES_USED): 0
SUM(CURRENT_NUMBER_OF_BYTES_USED): 1065175
 SUM(HIGH_NUMBER_OF_BYTES_USED): 1065809
```

### <span id="page-113-0"></span>**Total Memory Used in Group Replication**

The memory allocation to sending and receiving transactions, certification, and all other major processes. It is calculated by querying all the events of the memory/group\_rpl/ group. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME LIKE 'memory/group_rpl/%'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, 
 SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME LIKE 'memory/group_rpl/%'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/memory_gr
 SUM(COUNT_ALLOC): 190
 SUM(COUNT_FREE): 127
 SUM(SUM_NUMBER_OF_BYTES_ALLOC): 1096370
 SUM(SUM_NUMBER_OF_BYTES_FREE): 28675
 SUM(LOW_COUNT_USED): 0
 SUM(CURRENT_COUNT_USED): 63
 SUM(HIGH_COUNT_USED): 77
 SUM(LOW_NUMBER_OF_BYTES_USED): 0
SUM(CURRENT_NUMBER_OF_BYTES_USED): 1067695
 SUM(HIGH_NUMBER_OF_BYTES_USED): 1069255
```

### <span id="page-113-1"></span>**Memory Used in Certification**

The memory allocation in the certification process is a sum of the certification\_data, certification\_data\_gc, and certification\_info event values. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/certification_data'
 THEN 'memory/group_rpl/certification'
 WHEN EVENT_NAME = 'memory/group_rpl/certification_data_gc'
 THEN 'memory/group_rpl/certification'
 WHEN EVENT_NAME = 'memory/group_rpl/certification_info'
 THEN 'memory/group_rpl/certification'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
```

```
 WHEN EVENT_NAME = 'memory/group_rpl/certification_data'
 THEN 'memory/group_rpl/certification'
 WHEN EVENT_NAME = 'memory/group_rpl/certification_data_gc'
 THEN 'memory/group_rpl/certification'
 WHEN EVENT_NAME = 'memory/group_rpl/certification_info'
 THEN 'memory/group_rpl/certification'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/certification
 SUM(COUNT_ALLOC): 80
 SUM(COUNT_FREE): 80
 SUM(SUM_NUMBER_OF_BYTES_ALLOC): 9442
 SUM(SUM_NUMBER_OF_BYTES_FREE): 9442
 SUM(LOW_COUNT_USED): 0
 SUM(CURRENT_COUNT_USED): 0
 SUM(HIGH_COUNT_USED): 66
 SUM(LOW_NUMBER_OF_BYTES_USED): 0
SUM(CURRENT_NUMBER_OF_BYTES_USED): 0
 SUM(HIGH_NUMBER_OF_BYTES_USED): 6561
```

### <span id="page-114-0"></span>**Memory Used in Replication Pipeline**

The memory allocation of the replication pipeline is the sum of the certification\_data and transaction\_data event values. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME LIKE 'memory/group_rpl/certification_data'
 THEN 'memory/group_rpl/pipeline'
 WHEN EVENT_NAME LIKE 'memory/group_rpl/transaction_data'
 THEN 'memory/group_rpl/pipeline'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME LIKE 'memory/group_rpl/certification_data'
 THEN 'memory/group_rpl/pipeline'
 WHEN EVENT_NAME LIKE 'memory/group_rpl/transaction_data'
 THEN 'memory/group_rpl/pipeline'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/pipeline
 COUNT_ALLOC: 17
 COUNT_FREE: 13
 SUM_NUMBER_OF_BYTES_ALLOC: 2483
 SUM_NUMBER_OF_BYTES_FREE: 1668
 LOW_COUNT_USED: 0
 CURRENT_COUNT_USED: 4
 HIGH_COUNT_USED: 4
 LOW_NUMBER_OF_BYTES_USED: 0
CURRENT_NUMBER_OF_BYTES_USED: 815
 HIGH_NUMBER_OF_BYTES_USED: 815
```

### <span id="page-114-1"></span>**Memory Used in Consistency**

The memory allocation for transaction consistency guarantees is the sum of the consistent\_members\_that\_must\_prepare\_transaction, consistent\_transactions, consistent\_transactions\_prepared, consistent\_transactions\_waiting, and consistent\_transactions\_delayed\_view\_change event values. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_members_that_must_prepare_transaction'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions_prepared'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions_waiting'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions_delayed_view_change'
 THEN 'memory/group_rpl/consistency'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_members_that_must_prepare_transaction'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions_prepared'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions_waiting'
 THEN 'memory/group_rpl/consistency'
 WHEN EVENT_NAME = 'memory/group_rpl/consistent_transactions_delayed_view_change'
 THEN 'memory/group_rpl/consistency'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/consistency
 COUNT_ALLOC: 16
 COUNT_FREE: 6
 SUM_NUMBER_OF_BYTES_ALLOC: 1464
 SUM_NUMBER_OF_BYTES_FREE: 528
 LOW_COUNT_USED: 0
 CURRENT_COUNT_USED: 10
 HIGH_COUNT_USED: 11
 LOW_NUMBER_OF_BYTES_USED: 0
CURRENT_NUMBER_OF_BYTES_USED: 936
 HIGH_NUMBER_OF_BYTES_USED: 1024
```

### <span id="page-115-0"></span>**Memory Used in Delivery Message Service**

![](_page_115_Picture_4.jpeg)

### **Note**

This instrumentation applies only to data received, not data sent.

The memory allocation for the Group Replication delivery message service is the sum of the message\_service\_received\_message and message\_service\_queue event values. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/message_service_received_message'
 THEN 'memory/group_rpl/message_service'
 WHEN EVENT_NAME = 'memory/group_rpl/message_service_queue'
 THEN 'memory/group_rpl/message_service'
```

```
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, 
 SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/message_service_received_message'
 THEN 'memory/group_rpl/message_service'
 WHEN EVENT_NAME = 'memory/group_rpl/message_service_queue'
 THEN 'memory/group_rpl/message_service'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/message_service
 COUNT_ALLOC: 2
 COUNT_FREE: 0
 SUM_NUMBER_OF_BYTES_ALLOC: 1048664
 SUM_NUMBER_OF_BYTES_FREE: 0
 LOW_COUNT_USED: 0
 CURRENT_COUNT_USED: 2
 HIGH_COUNT_USED: 2
 LOW_NUMBER_OF_BYTES_USED: 0
CURRENT_NUMBER_OF_BYTES_USED: 1048664
 HIGH_NUMBER_OF_BYTES_USED: 1048664
```

### <span id="page-116-0"></span>**Memory Used to Broadcast and Receive Transactions**

The memory allocation for the broadcasting and receiving transactions to and from the network is the sum of the wGcs\_message\_data::m\_buffer and GCS\_XCom::xcom\_cache event values. For example:

```
SELECT * FROM (
 SELECT
 (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/Gcs_message_data::m_buffer'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/group_rpl/GCS_XCom::xcom_cache'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END) AS EVENT_NAME, 
 SUM(COUNT_ALLOC), SUM(COUNT_FREE),
 SUM(SUM_NUMBER_OF_BYTES_ALLOC),
 SUM(SUM_NUMBER_OF_BYTES_FREE), SUM(LOW_COUNT_USED),
 SUM(CURRENT_COUNT_USED), SUM(HIGH_COUNT_USED),
 SUM(LOW_NUMBER_OF_BYTES_USED), SUM(CURRENT_NUMBER_OF_BYTES_USED),
 SUM(HIGH_NUMBER_OF_BYTES_USED)
 FROM performance_schema.memory_summary_global_by_event_name
 GROUP BY (CASE
 WHEN EVENT_NAME = 'memory/group_rpl/Gcs_message_data::m_buffer'
 THEN 'memory/group_rpl/memory_gr'
 WHEN EVENT_NAME = 'memory/group_rpl/GCS_XCom::xcom_cache'
 THEN 'memory/group_rpl/memory_gr'
 ELSE 'memory_gr_rest'
 END)
 ) f
WHERE f.EVENT_NAME != 'memory_gr_rest'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/group_rpl/memory_gr
 SUM(COUNT_ALLOC): 73
 SUM(COUNT_FREE): 20
 SUM(SUM_NUMBER_OF_BYTES_ALLOC): 1070845
 SUM(SUM_NUMBER_OF_BYTES_FREE): 5670
 SUM(LOW_COUNT_USED): 0
```

```
 SUM(CURRENT_COUNT_USED): 53
 SUM(HIGH_COUNT_USED): 56
 SUM(LOW_NUMBER_OF_BYTES_USED): 0
SUM(CURRENT_NUMBER_OF_BYTES_USED): 1065175
 SUM(HIGH_NUMBER_OF_BYTES_USED): 1065175
```

# <span id="page-117-0"></span>**20.8 Upgrading Group Replication**

This section explains how to upgrade a Group Replication setup. The basic process of upgrading members of a group is the same as upgrading stand-alone instances, see Chapter 3, Upgrading MySQL for the actual process of doing upgrade and types available. Choosing between an in-place or logical upgrade depends on the amount of data stored in the group. Usually an in-place upgrade is faster, and therefore is recommended. You should also consult [Section 19.5.3, "Upgrading or](#page-4-0) [Downgrading a Replication Topology".](#page-4-0)

![](_page_117_Picture_4.jpeg)

#### **Note**

Before MySQL 8.4, a server would not join a group if it was running a lower MySQL Server version than the lowest group member's version. For example, for a group with S1 (8.0.30), S2 (8.0.31), and S3 (8.0.32), the joining member needs to be 8.0.30 or higher. MySQL 8.4 allows all versions within the 8.4 series to join. For example, an 8.4.0 server could join a group consisting of S1 (8.4.1) and S2 (8.4.2).

While you are in the process of upgrading an online group, in order to maximize availability, you might need to have members with different MySQL Server versions running at the same time. Group Replication includes compatibility policies that enable you to safely combine members running different versions of MySQL in the same group during the upgrade procedure. Depending on your group, the effects of these policies might affect the order in which you should upgrade group members. For details, see [Section 20.8.1, "Combining Different Member Versions in a Group"](#page-117-1).

If your group can be taken fully offline see [Section 20.8.2, "Group Replication Offline Upgrade".](#page-119-0) If your group needs to remain online, as is common with production deployments, see [Section 20.8.3, "Group](#page-119-1) [Replication Online Upgrade"](#page-119-1) for the different approaches available for upgrading a group with minimal downtime.

# <span id="page-117-1"></span>**20.8.1 Combining Different Member Versions in a Group**

Group Replication is versioned according to the MySQL Server version that the Group Replication plugin was bundled with. For example, if a member is running MySQL 8.4.8 then that is the version of the Group Replication plugin. To check the version of MySQL Server on a group member issue:

```
SELECT MEMBER_HOST,MEMBER_PORT,MEMBER_VERSION FROM performance_schema.replication_group_members;
+-------------+-------------+----------------+
| member_host | member_port | member_version |
+-------------+-------------+----------------+
| example.com | 3306 | 8.4.8 |
+-------------+-------------+----------------+
```

For guidance on understanding the MySQL Server version and selecting a version, see Section 2.1.2, "Which MySQL Version and Distribution to Install".

For optimal compatibility and performance, all members of a group should run the same version of MySQL Server and therefore of Group Replication. However, while you are in the process of upgrading an online group, in order to maximize availability, you might need to have members with different MySQL Server versions running at the same time. Depending on the changes made between the versions of MySQL, you could encounter incompatibilities in this situation. For example, if a feature has been deprecated between major versions, then combining the versions in a group might cause members that rely on the deprecated feature to fail. Conversely, writing to a member running a newer MySQL version while there are read/write members in the group running an older MySQL version might cause issues on members that lack functions introduced in the newer release.

To prevent such issues, Group Replication includes compatibility policies that enable you to combine members running different versions of MySQL in the same group safely. A member applies these policies to decide whether to join the group normally, or join in read-only mode, or not join the group, depending on which choice results in the safe operation of the joining member and of the existing members of the group. In an upgrade scenario, each server must leave the group, be upgraded, and rejoin the group with its new server version. At this point the member applies the policies for its new server version, which might have changed from the policies it applied when it originally joined the group.

As the administrator, you can instruct any server to attempt to join any group by configuring the server appropriately and issuing a START GROUP\_REPLICATION statement. A decision to join or not join the group, or to join the group in read-only mode, is made and implemented by the joining member itself after you attempt to add it to the group. The joining member receives information on the MySQL Server versions of the current group members, assesses its own compatibility with those members, and applies the policies used in its own MySQL Server version (not the policies used by the existing members) to decide whether it is compatible.

The compatibility policies that a joining member applies when attempting to join a group are as follows:

- A member joins a group normally if it is running the same MySQL Server version as the lowest version that the existing group members are running.
- A member joins a group but remains in read-only mode if it is running a higher MySQL Server version than the lowest version that the existing group members are running. This behavior only makes a difference when the group is running in multi-primary mode, because in a group that is running in single-primary mode, newly added members default to being read-only in any case.

Members take into account the entire major.minor.release version of the software when checking compatibility.

In a multi-primary mode group with members that use different MySQL Server versions, Group Replication automatically manages members' read/write and read-only status. If a member leaves the group, the members running the version that is now the lowest are automatically set to read/write mode. When you change a group that was running in single-primary mode to run in multi-primary mode using group\_replication\_switch\_to\_multi\_primary\_mode(), Group Replication automatically sets each member to the correct mode. Members are automatically placed in read-only mode if they are running a higher MySQL server version than the lowest version present in the group, and members running the lowest version are placed in read/write mode.