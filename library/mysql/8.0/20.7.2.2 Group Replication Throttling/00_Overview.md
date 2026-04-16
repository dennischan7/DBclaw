---
source: MySQL 8.0 Reference
title: 00_Overview
---

Based on the metrics gathered across all servers in the group, a throttling mechanism kicks in and decides whether to limit the rate a member is able to execute/commit new transactions.

Therefore, metrics acquired from all members are the basis for calculating the capacity of each member: if a member has a large queue (for certification or the applier thread), then the capacity to execute new transactions should be close to ones certified or applied in the last period.

The lowest capacity of all the members in the group determines the real capacity of the group, while the number of local transactions determines how many members are writing to it, and, consequently, how many members should that available capacity be shared with.

This means that every member has an established write quota based on the available capacity, in other words a number of transactions it can safely issue for the next period. The writer-quota is enforced by the throttling mechanism if the queue size of the certifier or the binary log applier exceeds a userdefined threshold.

The quota is reduced by the number of transactions that were delayed in the last period, and then also further reduced by 10% to allow the queue that triggered the problem to reduce its size. In order to avoid large jumps in throughput once the queue size goes beyond the threshold, the throughput is only allowed to grow by the same 10% per period after that.

The current throttling mechanism does not penalize transactions below quota, but delays finishing those transactions that exceed it until the end of the monitoring period. As a consequence, if the quota is very small for the write requests issued some transactions may have latencies close to the monitoring period.

# <span id="page-171-0"></span>**20.7.3 Single Consensus Leader**

By default, the group communication engine for Group Replication (XCom, a Paxos variant) operates using every member of the replication group as a leader. From MySQL 8.0.27, the group communication engine can use a single leader to drive consensus when the group is in single-primary mode. Operating with a single consensus leader improves performance and resilience in single-primary mode, particularly when some of the group's secondary members are currently unreachable.

To use a single consensus leader, the group must be configured as follows:

- The group must be in single-primary mode.
- The group\_replication\_paxos\_single\_leader system variable must be set to ON. With the default setting OFF, the behavior is disabled. You must carry out a full reboot of the replication group (bootstrap) for Group Replication to pick up a change to this setting.
- The Group Replication communication protocol version must be set to 8.0.27 or later. Use the group\_replication\_get\_communication\_protocol() function to view the group's communication protocol version. If a lower version is in use, the group cannot use this behavior. You can use the group\_replication\_set\_communication\_protocol() function to set the group's communication protocol to a higher version if all group members support it. MySQL InnoDB Cluster manages the communication protocol version automatically. For more information, see [Section 20.5.1.4, "Setting a Group's Communication Protocol Version".](#page-123-0)

When this configuration is in place, Group Replication instructs the group communication engine to use the group's primary as the single leader to drive consensus. When a new primary is elected, Group Replication tells the group communication engine to use it instead. If the primary is currently unhealthy, the group communication engine uses an alternative member as the consensus leader. The Performance Schema table replication\_group\_communication\_information shows the current preferred and actual consensus leader, with the preferred leader being Group Replication's choice, and the actual leader being the one selected by the group communication engine.

If the group is in multi-primary mode, has a lower communication protocol version, or the behavior is disabled by the group\_replication\_paxos\_single\_leader setting, all members are used as leaders to drive consensus. In this situation, the Performance Schema table replication\_group\_communication\_information shows all of the members as both the preferred and actual leaders.

The WRITE\_CONSENSUS\_SINGLE\_LEADER\_CAPABLE column of the Performance Schema table replication\_group\_communication\_information table shows whether the group supports the use of a single leader, even if group\_replication\_paxos\_single\_leader is currently set to OFF on the queried member. The column value is 1 if the group was started with group\_replication\_paxos\_single\_leader set to ON, and its communication protocol version is MySQL 8.0.27 or above. This information is only returned for group members in ONLINE or RECOVERING state.

# <span id="page-172-0"></span>**20.7.4 Message Compression**

For messages sent between online group members, Group Replication enables message compression by default. Whether a specific message is compressed depends on the threshold that you configure using the group\_replication\_compression\_threshold system variable. Messages that have a payload larger than the specified number of bytes are compressed.

The default compression threshold is 1000000 bytes. You could use the following statements to increase the compression threshold to 2MB, for example:

```
STOP GROUP_REPLICATION;
SET GLOBAL group_replication_compression_threshold = 2097152;
START GROUP_REPLICATION;
```

If you set group\_replication\_compression\_threshold to zero, message compression is disabled.

Group Replication uses the LZ4 compression algorithm to compress messages sent in the group. Note that the maximum supported input size for the LZ4 compression

algorithm is 2113929216 bytes. This limit is lower than the maximum possible value for the group\_replication\_compression\_threshold system variable, which is matched to the maximum message size accepted by XCom. The LZ4 maximum input size is therefore a practical limit for message compression, and transactions above this size cannot be committed when message compression is enabled. With the LZ4 compression algorithm, do not set a value greater than 2113929216 bytes for group\_replication\_compression\_threshold.

The value of group\_replication\_compression\_threshold is not required by Group Replication to be the same on all group members. However, it is advisable to set the same value on all group members in order to avoid unnecessary rollback of transactions, failure of message delivery, or failure of message recovery.

From MySQL 8.0.18, you can also configure compression for messages sent for distributed recovery by the method of state transfer from a donor's binary log. Compression for these messages, which are sent from a donor already in the group to a joining member, is controlled separately using the group\_replication\_recovery\_compression\_algorithms and group\_replication\_recovery\_zstd\_compression\_level system variables. For more information, see Section 6.2.8, "Connection Compression Control".

Binary log transaction compression (available as of MySQL 8.0.20), which is activated by the binlog\_transaction\_compression system variable, can also be used to save bandwidth. The transaction payloads remain compressed when they are transferred between group members. If you use binary log transaction compression in combination with Group Replication's message compression, message compression has less opportunity to act on the data, but can still compress headers and those events and transaction payloads that are uncompressed. For more information on binary log transaction compression, see Section 7.4.4.5, "Binary Log Transaction Compression".

Compression for messages sent in the group happens at the group communication engine level, before the data is handed over to the group communication thread, so it takes place within the context of the mysql user session thread. If the message payload size exceeds the threshold set by group\_replication\_compression\_threshold, the transaction payload is compressed before being sent out to the group, and decompressed when it is received. Upon receiving a message, the member checks the message envelope to verify whether it is compressed or not. If needed, then the member decompresses the transaction, before delivering it to the upper layer. This process is shown in the following figure.

**Figure 20.13 Compression Support**

![](_page_174_Picture_2.jpeg)

When network bandwidth is a bottleneck, message compression can provide up to 30-40% throughput improvement at the group communication level. This is especially important within the context of large groups of servers under load. The TCP peer-to-peer nature of the interconnections between N participants in the group makes the sender send the same amount of data N times. Furthermore, binary logs are likely to exhibit a high compression ratio. This makes compression a compelling feature for Group Replication workloads that contain large transactions.

# <span id="page-174-0"></span>**20.7.5 Message Fragmentation**

When an abnormally large message is sent between Group Replication group members, it can result in some group members being reported as failed and expelled from the group. This is because the single thread used by Group Replication's group communication engine (XCom, a Paxos variant) is occupied processing the message for too long, so some of the group members might report the receiver as failed. From MySQL 8.0.16, by default, large messages are automatically split into fragments that are sent separately and reassembled by the recipients.

The system variable group\_replication\_communication\_max\_message\_size specifies a maximum message size for Group Replication communications, above which messages are fragmented. The default maximum message size is 10485760 bytes (10 MiB). The greatest permitted value is the same as the maximum value of the replica\_max\_allowed\_packet and slave\_max\_allowed\_packet system variables, which is 1073741824 bytes (1 GB). The setting for group\_replication\_communication\_max\_message\_size must be less than replica\_max\_allowed\_packet (or slave\_max\_allowed\_packet), because the applier thread cannot handle message fragments larger than the maximum permitted packet size. To switch off fragmentation, specify a zero value for group\_replication\_communication\_max\_message\_size.

As with most other Group Replication system variables, you must restart the Group Replication plugin for the change to take effect. For example:

```
STOP GROUP_REPLICATION;
SET GLOBAL group_replication_communication_max_message_size= 5242880;
START GROUP_REPLICATION;
```

Message delivery for a fragmented message is considered complete when all the fragments of the message have been received and reassembled by all the group members. Fragmented messages include information in their headers that enables a member joining during message transmission to recover the earlier fragments that were sent before it joined. If the joining member fails to recover the fragments, it expels itself from the group.

In order for a replication group to use fragmentation, all group members must be at MySQL 8.0.16 or above, and the Group Replication communication protocol version in use by the group must allow fragmentation. You can inspect the communication protocol in use by a group by using the group\_replication\_get\_communication\_protocol() function, which returns the oldest MySQL Server version that the group supports. Versions from MySQL 5.7.14 allow compression of messages, and versions from MySQL 8.0.16 also allow fragmentation of messages. If all group members are at MySQL 8.0.16 or above and there is no requirement to allow members at earlier releases to join, you can use the group\_replication\_set\_communication\_protocol() function to set the communication protocol version to MySQL 8.0.16 or above in order to allow fragmentation. For more information, see [Section 20.5.1.4, "Setting a Group's Communication Protocol](#page-123-0) [Version"](#page-123-0).

If a replication group cannot use fragmentation because some members do not support it, the system variable group\_replication\_transaction\_size\_limit can be used to limit the maximum size of transactions the group accepts. In MySQL 8.0, the default setting is approximately 143 MB. Transactions above this size are rolled back. You can also use the system variable group\_replication\_member\_expel\_timeout to allow additional time (up to an hour) before a member under suspicion of having failed is expelled from the group.

# <span id="page-175-0"></span>**20.7.6 XCom Cache Management**

The group communication engine for Group Replication (XCom, a Paxos variant) includes a cache for messages (and their metadata) exchanged between the group members as a part of the consensus protocol. Among other functions, the message cache is used for recovery of missed messages by members that reconnect with the group after a period where they were unable to communicate with the other group members.

From MySQL 8.0.16, a cache size limit can be set for XCom's message cache using the group\_replication\_message\_cache\_size system variable. If the cache size limit is reached, XCom removes the oldest entries that have been decided and delivered. The same cache size limit should be set on all group members, because an unreachable member that is attempting to reconnect selects any other member at random for recovery of missed messages. The same messages should therefore be available in each member's cache.

Before MySQL 8.0.16, the cache size was 1 GB, and the default setting for the cache size from MySQL 8.0.16 is the same. Ensure that sufficient memory is available on your system for your chosen cache size limit, considering the size of MySQL Server's other caches and object pools. Note that the limit set

using group\_replication\_message\_cache\_size applies only to the data stored in the cache, and the cache structures require an additional 50 MB of memory.

When selecting a group\_replication\_message\_cache\_size setting, do so with reference to the expected volume of messages in the time period before a member is expelled. The length of this time period is controlled by the group\_replication\_member\_expel\_timeout system variable, which determines the waiting period (up to an hour) that is allowed in addition to the initial 5-second detection period for members to return to the group rather than being expelled. Note that before MySQL 8.0.21, this time period defaulted to 5 seconds from the member becoming unavailable, which is just the detection period before a suspicion is created, because the additional expel timeout set by the group\_replication\_member\_expel\_timeout system variable defaulted to zero. From 8.0.21 the expel timeout defaults to 5 seconds, so by default a member is not expelled until it has been absent for at least 10 seconds.