---
source: MySQL 8.0 Reference
title: 00_Overview
---

The group\_replication\_autorejoin\_tries system variable, which is available from MySQL 8.0.16, makes a member that has been expelled or reached its unreachable majority timeout try to rejoin the group automatically. Up to MySQL 8.0.20, the value of the system variable defaults to 0, so auto-rejoin is not activated by default. From MySQL 8.0.21, the value of the system variable defaults to 3, meaning that the member automatically makes 3 attempts to rejoin the group, with 5 minutes between each.

When auto-rejoin is not activated, a member accepts its expulsion as soon as it resumes communication, and proceeds to the action specified by the group\_replication\_exit\_state\_action system variable. After this, manual intervention is needed to bring the member back into the group. Using the auto-rejoin feature is appropriate if you can tolerate the possibility of stale reads and want to minimize the need for manual intervention, especially where transient network issues fairly often result in the expulsion of members.

With auto-rejoin, when the member's expulsion or unreachable majority timeout is reached, it makes an attempt to rejoin (using the current plugin option values), then continues to make further auto-rejoin attempts up to the specified number of tries. After an unsuccessful auto-rejoin attempt, the member waits 5 minutes before the next try. The auto-rejoin attempts and the time between them are called the auto-rejoin procedure. If the specified number of tries is exhausted without the member rejoining or being stopped, the member proceeds to the action specified by the group\_replication\_exit\_state\_action system variable.

During and between auto-rejoin attempts, a member remains in super read only mode and displays an ERROR state on its view of the replication group. During this time, the member does not accept writes. However, reads can still be made on the member, with an increasing likelihood of stale reads over time. If you do want to intervene to take the member offline during the auto-rejoin procedure, the member can be stopped manually at any time by using a STOP GROUP\_REPLICATION statement or shutting down the server. If you cannot tolerate the possibility of stale reads for any period of time, set the group\_replication\_autorejoin\_tries system variable to 0.

You can monitor the auto-rejoin procedure using the Performance Schema. While an autorejoin procedure is taking place, the Performance Schema table events\_stages\_current shows the event "Undergoing auto-rejoin procedure", with the number of retries that have been attempted so far during this instance of the procedure (in the WORK\_COMPLETED column). The events\_stages\_summary\_global\_by\_event\_name table shows the number of times the server instance has initiated the auto-rejoin procedure (in the COUNT\_STAR column). The events\_stages\_history\_long table shows the time each of these auto-rejoin procedures was completed (in the TIMER\_END column). While a member is rejoining a replication group, its status can be displayed as OFFLINE or ERROR before the group completes the compatibility checks and accepts it as a member. When the member is catching up with the group's transactions, its status is RECOVERING.

# <span id="page-181-0"></span>**20.7.7.4 Exit Action**

The group\_replication\_exit\_state\_action system variable, which is available from MySQL 8.0.12 and MySQL 5.7.24, specifies what Group Replication does when the member leaves the group unintentionally due to an error or problem, and either fails to auto-rejoin or does not try. Note that in the case of an expelled member, the member does not know that it was expelled until it reconnects to the group, so the specified action is only taken if the member manages to reconnect, or if the member raises a suspicion on itself and expels itself.

In order of impact, the exit actions are as follows:

- 1. If READ\_ONLY is the exit action, the instance switches MySQL to super read only mode by setting the system variable super\_read\_only to ON. When the member is in super read only mode, clients cannot make any updates, even if they have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). However, clients can still read data, and because updates are no longer being made, there is a probability of stale reads which increases over time. With this setting, you therefore need to pro-actively monitor the servers for failures. This exit action is the default from MySQL 8.0.15. After this exit action is taken, the member's status is displayed as ERROR in the view of the group.
- 2. If OFFLINE\_MODE is the exit action, the instance switches MySQL to offline mode by setting the system variable offline\_mode to ON. When the member is in offline mode, connected client users are disconnected on their next request and connections are no longer accepted, with the exception of client users that have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). Group Replication also sets the system variable super\_read\_only to ON, so clients cannot make any updates, even if they have connected with the CONNECTION\_ADMIN or SUPER privilege. This exit action prevents both updates and stale reads (with the exception of reads by client users with the stated privileges), and enables proxy tools such as MySQL Router to recognize that the server is unavailable and redirect client connections. It also leaves the instance running so that an administrator can attempt to resolve the issue without shutting down MySQL. This exit action is available from MySQL 8.0.18. After this exit action is taken, the member's status is displayed as ERROR in the view of the group (not OFFLINE, which means a member has Group Replication functionality available but does not currently belong to a group).
- 3. If ABORT\_SERVER is the exit action, the instance shuts down MySQL. Instructing the member to shut itself down prevents all stale reads and client updates, but it means that the MySQL Server instance is unavailable and must be restarted, even if the issue could have been resolved without that step. This exit action was the default from MySQL 8.0.12, when the system variable was added, to MySQL 8.0.15 inclusive. After this exit action is taken, the member is removed from the listing of servers in the view of the group.

Bear in mind that operator intervention is required whatever exit action is set, as an ex-member that has exhausted its auto-rejoin attempts (or never had any) and has been expelled from the group is not allowed to rejoin without a restart of Group Replication. The exit action only influences whether or not clients can still read data on the server that was unable to rejoin the group, and whether or not the server stays running.

![](_page_181_Picture_9.jpeg)

#### **Important**

If a failure occurs before the member has successfully joined the group, the exit action specified by group\_replication\_exit\_state\_action is

not taken. This is the case if there is a failure during the local configuration check, or a mismatch between the configuration of the joining member and the configuration of the group. In these situations, the super\_read\_only system variable is left with its original value, and the server does not shut down MySQL. To ensure that the server cannot accept updates when Group Replication did not start, we therefore recommend that super\_read\_only=ON is set in the server's configuration file at startup, which Group Replication changes to OFF on primary members after it has been started successfully. This safeguard is particularly important when the server is configured to start Group Replication on server boot (group\_replication\_start\_on\_boot=ON), but it is also useful when Group Replication is started manually using a START GROUP\_REPLICATION statement.

If a failure occurs after the member has successfully joined the group, the specified exit action is taken. This is the case in the following situations:

- 1. Applier error There is an error in the replication applier. This issue is not recoverable.
- 2. Distributed recovery not possible There is an issue that means Group Replication's distributed recovery process (which uses remote cloning operations and state transfer from the binary log) cannot be completed. Group Replication retries distributed recovery automatically where this makes sense, but stops if there are no more options to complete the process. For details, see [Section 20.5.4.4, "Fault Tolerance for Distributed Recovery".](#page-143-0)
- 3. Group configuration change error An error occurred during a group-wide configuration change carried out using a function, as described in [Section 20.5.1, "Configuring an Online Group"](#page-120-2).
- 4. Primary election error An error occurred during election of a new primary member for a group in single-primary mode, as described in [Section 20.1.3.1, "Single-Primary Mode"](#page-88-1).
- 5. Unreachable majority timeout The member has lost contact with a majority of the group members so is in a minority, and a timeout that was set by the group\_replication\_unreachable\_majority\_timeout system variable has expired.
- 6. Member expelled from group A suspicion has been raised on the member, and any timeout set by the group\_replication\_member\_expel\_timeout system variable has expired, and the member has resumed communication with the group and found that it has been expelled.
- 7. Out of auto-rejoin attempts The group\_replication\_autorejoin\_tries system variable was set to specify a number of auto-rejoin attempts after a loss of majority or expulsion, and the member completed this number of attempts without success.

The following table summarizes the failure scenarios and actions in each case:

**Table 20.3 Exit actions in Group Replication failure situations**

| Failure situation                                          | Group Replication started with<br>START GROUP_REPLICATION                          | Group Replication started with<br>group_replication_start_on_boot<br>=ON                          |  |
|------------------------------------------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|--|
| Member fails local configuration<br>check                  | super_read_only and<br>offline_mode unchanged                                      | super_read_only and<br>offline_mode unchanged                                                     |  |
| Mismatch between joining<br>member and group configuration | MySQL continues running<br>Set super_read_only=ON at<br>startup to prevent updates | MySQL continues running<br>Set super_read_only=ON<br>at startup to prevent updates<br>(Important) |  |
| Applier error on member                                    | super_read_only set to ON                                                          | super_read_only set to ON                                                                         |  |
| Distributed recovery not possible                          | OR                                                                                 | OR                                                                                                |  |

| Failure situation                | Group Replication started with<br>START GROUP_REPLICATION | Group Replication started with<br>group_replication_start_on_boot<br>=ON |
|----------------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------|
| Group configuration change error | offline_mode and                                          | offline_mode and                                                         |
| Primary election error           | super_read_only set to ON                                 | super_read_only set to ON                                                |
| Unreachable majority timeout     | OR                                                        | OR                                                                       |
| Member expelled from group       | MySQL shuts down                                          | MySQL shuts down                                                         |
| Out of auto-rejoin attempts      |                                                           |                                                                          |

# <span id="page-183-0"></span>**20.7.8 Handling a Network Partition and Loss of Quorum**

The group needs to achieve consensus whenever a change that needs to be replicated happens. This is the case for regular transactions but is also required for group membership changes and some internal messaging that keeps the group consistent. Consensus requires a majority of group members to agree on a given decision. When a majority of group members is lost, the group is unable to progress and blocks because it cannot secure majority or quorum.

Quorum may be lost when there are multiple involuntary failures, causing a majority of servers to be removed abruptly from the group. For example, in a group of 5 servers, if 3 of them become silent at once, the majority is compromised and thus no quorum can be achieved. In fact, the remaining two are not able to tell if the other 3 servers have crashed or whether a network partition has isolated these 2 alone and therefore the group cannot be reconfigured automatically.

On the other hand, if servers exit the group voluntarily, they instruct the group that it should reconfigure itself. In practice, this means that a server that is leaving tells others that it is going away. This means that other members can reconfigure the group properly, the consistency of the membership is maintained and the majority is recalculated. For example, in the above scenario of 5 servers where 3 leave at once, if the 3 leaving servers warn the group that they are leaving, one by one, then the membership is able to adjust itself from 5 to 2, and at the same time, securing quorum while that happens.

![](_page_183_Picture_6.jpeg)

# **Note**

Loss of quorum is by itself a side-effect of bad planning. Plan the group size for the number of expected failures (regardless whether they are consecutive, happen all at once or are sporadic).

For a group in single-primary mode, the primary might have transactions that are not yet present on other members at the time of the network partition. If you are considering excluding the primary from the new group, be aware that such transactions might be lost. A member with extra transactions cannot rejoin the group, and the attempt results in an error with the message This member has more executed transactions than those present in the group. Set the group\_replication\_unreachable\_majority\_timeout system variable for the group members to avoid this situation.

The following sections explain what to do if the system partitions in such a way that no quorum is automatically achieved by the servers in the group.

# **Detecting Partitions**

The replication\_group\_members performance schema table presents the status of each server in the current view from the perspective of this server. The majority of the time the system does not run into partitioning, and therefore the table shows information that is consistent across all servers in the group. In other words, the status of each server on this table is agreed by all in the current

view. However, if there is network partitioning, and quorum is lost, then the table shows the status UNREACHABLE for those servers that it cannot contact. This information is exported by the local failure detector built into Group Replication.

**Figure 20.14 Losing Quorum**

![](_page_184_Picture_3.jpeg)

To understand this type of network partition the following section describes a scenario where there are initially 5 servers working together correctly, and the changes that then happen to the group once only 2 servers are online. The scenario is depicted in the figure.

As such, lets assume that there is a group with these 5 servers in it:

- Server s1 with member identifier 199b2df7-4aaf-11e6-bb16-28b2bd168d07
- Server s2 with member identifier 199bb88e-4aaf-11e6-babe-28b2bd168d07
- Server s3 with member identifier 1999b9fb-4aaf-11e6-bb54-28b2bd168d07
- Server s4 with member identifier 19ab72fc-4aaf-11e6-bb51-28b2bd168d07

• Server s5 with member identifier 19b33846-4aaf-11e6-ba81-28b2bd168d07

Initially the group is running fine and the servers are happily communicating with each other. You can verify this by logging into s1 and looking at its replication\_group\_members performance schema table. For example:

```
mysql> SELECT MEMBER_ID,MEMBER_STATE, MEMBER_ROLE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+-------------+
| MEMBER_ID | MEMBER_STATE | MEMBER_ROLE |
+--------------------------------------+--------------+-------------+
| 1999b9fb-4aaf-11e6-bb54-28b2bd168d07 | ONLINE | SECONDARY |
| 199b2df7-4aaf-11e6-bb16-28b2bd168d07 | ONLINE | PRIMARY |
| 199bb88e-4aaf-11e6-babe-28b2bd168d07 | ONLINE | SECONDARY |
| 19ab72fc-4aaf-11e6-bb51-28b2bd168d07 | ONLINE | SECONDARY |
| 19b33846-4aaf-11e6-ba81-28b2bd168d07 | ONLINE | SECONDARY |
+--------------------------------------+--------------+-------------+
```

However, moments later there is a catastrophic failure and servers s3, s4 and s5 stop unexpectedly. A few seconds after this, looking again at the replication\_group\_members table on s1 shows that it is still online, but several others members are not. In fact, as seen below they are marked as UNREACHABLE. Moreover, the system could not reconfigure itself to change the membership, because the majority has been lost.

```
mysql> SELECT MEMBER_ID,MEMBER_STATE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID | MEMBER_STATE |
+--------------------------------------+--------------+
| 1999b9fb-4aaf-11e6-bb54-28b2bd168d07 | UNREACHABLE |
| 199b2df7-4aaf-11e6-bb16-28b2bd168d07 | ONLINE |
| 199bb88e-4aaf-11e6-babe-28b2bd168d07 | ONLINE |
| 19ab72fc-4aaf-11e6-bb51-28b2bd168d07 | UNREACHABLE |
| 19b33846-4aaf-11e6-ba81-28b2bd168d07 | UNREACHABLE |
+--------------------------------------+--------------+
```

The table shows that s1 is now in a group that has no means of progressing without external intervention, because a majority of the servers are unreachable. In this particular case, the group membership list needs to be reset to allow the system to proceed, which is explained in this section. Alternatively, you could also choose to stop Group Replication on s1 and s2 (or stop completely s1 and s2), figure out what happened with s3, s4 and s5 and then restart Group Replication (or the servers).

# **Unblocking a Partition**

Group replication enables you to reset the group membership list by forcing a specific configuration. For instance in the case above, where s1 and s2 are the only servers online, you could choose to force a membership configuration consisting of only s1 and s2. This requires checking some information about s1 and s2 and then using the group\_replication\_force\_members variable.

**Figure 20.15 Forcing a New Membership**

![](_page_186_Picture_2.jpeg)

Suppose that you are back in the situation where s1 and s2 are the only servers left in the group. Servers s3, s4 and s5 have left the group unexpectedly. To make servers s1 and s2 continue, you want to force a membership configuration that contains only s1 and s2.

![](_page_186_Picture_4.jpeg)

#### **Warning**

This procedure uses group\_replication\_force\_members and should be considered a last resort remedy. It must be used with extreme care and only for overriding loss of quorum. If misused, it could create an artificial split-brain scenario or block the entire system altogether.

When forcing a new membership configuration, make sure that any servers are going to be forced out of the group are indeed stopped. In the scenario depicted above, if s3, s4 and s5 are not really unreachable but instead are online, they may have formed their own functional partition (they are 3 out of 5, hence they have the majority). In that case, forcing a group membership list with s1 and s2 could create an artificial split-brain situation. Therefore it is important before forcing a new membership configuration to ensure that the servers to be excluded are indeed shut down and if they are not, shut them down before proceeding.

![](_page_187_Picture_1.jpeg)

#### **Warning**

For a group in single-primary mode, the primary might have transactions that are not yet present on other members at the time of the network partition. If you are considering excluding the primary from the new group, be aware that such transactions might be lost. A member with extra transactions cannot rejoin the group, and the attempt results in an error with the message This member has more executed transactions than those present in the group. Set the group\_replication\_unreachable\_majority\_timeout system variable for the group members to avoid this situation.

Recall that the system is blocked and the current configuration is the following (as perceived by the local failure detector on s1):

```
mysql> SELECT MEMBER_ID,MEMBER_STATE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID | MEMBER_STATE |
+--------------------------------------+--------------+
| 1999b9fb-4aaf-11e6-bb54-28b2bd168d07 | UNREACHABLE |
| 199b2df7-4aaf-11e6-bb16-28b2bd168d07 | ONLINE |
| 199bb88e-4aaf-11e6-babe-28b2bd168d07 | ONLINE |
| 19ab72fc-4aaf-11e6-bb51-28b2bd168d07 | UNREACHABLE |
| 19b33846-4aaf-11e6-ba81-28b2bd168d07 | UNREACHABLE |
+--------------------------------------+--------------+
```

The first thing to do is to check what is the local address (group communication identifier) for s1 and s2. Log in to s1 and s2 and get that information as follows.

```
mysql> SELECT @@group_replication_local_address;
```

Once you know the group communication addresses of s1 (127.0.0.1:10000) and s2 (127.0.0.1:10001), you can use that on one of the two servers to inject a new membership configuration, thus overriding the existing one that has lost quorum. To do that on s1:

```
mysql> SET GLOBAL group_replication_force_members="127.0.0.1:10000,127.0.0.1:10001";
```

This unblocks the group by forcing a different configuration. Check replication\_group\_members on both s1 and s2 to verify the group membership after this change. First on s1.

```
mysql> SELECT MEMBER_ID,MEMBER_STATE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID | MEMBER_STATE |
+--------------------------------------+--------------+
| b5ffe505-4ab6-11e6-b04b-28b2bd168d07 | ONLINE |
| b60907e7-4ab6-11e6-afb7-28b2bd168d07 | ONLINE |
+--------------------------------------+--------------+
```

And then on s2.

```
mysql> SELECT * FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID | MEMBER_STATE |
+--------------------------------------+--------------+
| b5ffe505-4ab6-11e6-b04b-28b2bd168d07 | ONLINE |
| b60907e7-4ab6-11e6-afb7-28b2bd168d07 | ONLINE |
+--------------------------------------+--------------+
```

After you have used the group\_replication\_force\_members system variable to successfully force a new group membership and unblock the group, ensure that you clear the system variable. group\_replication\_force\_members must be empty in order to issue a START GROUP\_REPLICATION statement.

# <span id="page-187-0"></span>**20.7.9 Monitoring Group Replication Memory Usage with Performance Schema Memory Instrumentation**

From MySQL 8.0.30, Performance Schema provides instrumentation for performance monitoring of Group Replication memory usage. To view the available Group Replication instrumentation, issue the following query:

```
mysql> SELECT NAME,ENABLED FROM performance_schema.setup_instruments
 WHERE NAME LIKE 'memory/group_rpl/%';
+-------------------------------------------------------------------+---------+
| NAME | ENABLED |
+-------------------------------------------------------------------+---------+
| memory/group_rpl/write_set_encoded | YES |
| memory/group_rpl/certification_data | YES |
| memory/group_rpl/certification_data_gc | YES |
| memory/group_rpl/certification_info | YES |
| memory/group_rpl/transaction_data | YES |
| memory/group_rpl/sql_service_command_data | YES |
| memory/group_rpl/mysql_thread_queued_task | YES |
| memory/group_rpl/message_service_queue | YES |
| memory/group_rpl/message_service_received_message | YES |
| memory/group_rpl/group_member_info | YES |
| memory/group_rpl/consistent_members_that_must_prepare_transaction | YES |
| memory/group_rpl/consistent_transactions | YES |
| memory/group_rpl/consistent_transactions_prepared | YES |
| memory/group_rpl/consistent_transactions_waiting | YES |
| memory/group_rpl/consistent_transactions_delayed_view_change | YES |
| memory/group_rpl/GCS_XCom::xcom_cache | YES |
| memory/group_rpl/Gcs_message_data::m_buffer | YES |
+-------------------------------------------------------------------+---------+
```

For more information on Performance Schema's memory instrumentation and events, see Section 29.12.20.10, "Memory Summary Tables".

# **Performance Schema Group Replication instruments memory allocation for Group Replication.**

The memory/group\_rpl/ Performance Schema instrumentation was updated in 8.0.30 to extend monitoring of Group Replication memory usage. memory/group\_rpl/ contains the following instruments:

- write\_set\_encoded: Memory allocated to encode the write set before it is broadcast to the group members.
- Gcs\_message\_data::m\_buffer: Memory allocated for the transaction data payload sent to the network.
- certification\_data: Memory allocated for certification of incoming transactions.
- certification\_data\_gc: Memory allocated for the GTID\_EXECUTED sent by each member for garbage collection.
- certification\_info: Memory allocated for storage of certification information allocated to resolve conflicts between concurrent transactions.
- transaction\_data: Memory allocated for incoming transactions queued for the plugin pipeline.
- message\_service\_received\_message: Memory allocated to receiving messages from Group Replication delivery message service.
- sql\_service\_command\_data: Memory allocated for processing the queue of internal SQL service commands.
- mysql\_thread\_queued\_task: Memory allocated when a MySQL-thread dependent task is added to the processing queue.
- message\_service\_queue: Memory allocated for queued messages of the Group Replication delivery message service.

- GCS\_XCom::xcom\_cache: Memory allocated to XCOM ache for messaging and metadata exchanged between group members as part of the consensus protocol.
- consistent\_members\_that\_must\_prepare\_transaction: Memory allocated to hold list of members preparing transaction for Group Replication transaction consistency guarantees.
- consistent\_transactions: Memory allocated to hold transaction and list of members that must prepare that transaction for Group Replication transaction consistency guarantees.
- consistent\_transactions\_prepared: Memory allocated to hold list of transaction's info prepared for the Group Replication Transaction Consistency Guarantees.
- consistent\_transactions\_waiting: Memory allocated to hold information on a list of transactions while preceding prepared transactions with consistency of AFTER and BEFORE\_AND\_AFTER are processed.
- consistent\_transactions\_delayed\_view\_change: Memory allocated to hold list of view change events (view\_change\_log\_event) delayed by prepared consistent transactions waiting for prepare acknowledgement.
- group\_member\_info: Memory allocated to hold the group member properties. Properties such as hostname, port, member weight and role, and so on.

The following instruments in the memory/sql/ grouping are also used to monitor Group Replication memory:

- Log\_event: Memory allocated for encoding transaction data into the binary log format; this is the same format in which Group Replication transmits data.
- write\_set\_extraction: Memory allocated to the transaction's generated write set before it is committed.
- Gtid\_set::to\_string: Memory allocated to stored the string representation of a GTID set.
- Gtid\_set::Interval\_chunk: Memory allocated to store the GTID object.