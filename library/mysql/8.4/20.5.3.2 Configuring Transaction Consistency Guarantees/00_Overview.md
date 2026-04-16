---
source: MySQL 8.4 Reference
title: 00_Overview
---

Although the [Transaction Synchronization Points](#page-52-0) section explains that conceptually there are two synchronization points from which you can choose: on read or on write, these terms were a simplification and the terms used in Group Replication are: before and after transaction execution. The consistency level can have different effects on read-only and read/write transactions processed by the group as demonstrated in this section.

- [How to Choose a Consistency Level](#page-54-0)
- [Impacts of Consistency Levels](#page-55-0)
- [Impact of Consistency on Primary Election](#page-56-0)
- [Permitted Queries Under Consistency Rules](#page-57-0)

The following list shows the possible consistency levels that you can configure in Group Replication using the [group\\_replication\\_consistency](#page-136-0) variable, in order of increasing transaction consistency guarantee:

• EVENTUAL

Neither read-only nor read/write transactions wait for preceding transactions to be applied before executing. This was the behavior of Group Replication before the [group\\_replication\\_consistency](#page-136-0) variable was added. A read/write transaction does not wait for other members to apply a transaction. This means that a transaction could be externalized on one member before the others. This also means that in the event of a primary failover, the new primary can accept new read-only and read/write transactions before the previous primary transactions are all applied. Read-only transactions could result in outdated values, read/write transactions could result in a rollback due to conflicts.

### • BEFORE\_ON\_PRIMARY\_FAILOVER

New read-only or read/write transactions with a newly elected primary that is applying a backlog from the old primary are not applied until any backlog has been applied. This ensures that when a primary failover happens, intentionally or not, clients always see the latest value on the primary. This guarantees consistency, but means that clients must be able to handle the delay in the event that a backlog is being applied. Usually this delay should be minimal, but it does depend on the size of the backlog.

#### • BEFORE

A read/write transaction waits for all preceding transactions to complete before being applied. A read-only transaction waits for all preceding transactions to complete before being executed. This ensures that this transaction reads the latest value by only affecting the latency of the transaction. This reduces the overhead of synchronization on every read/write transaction, by ensuring synchronization is used only on read-only transactions. This consistency level also includes the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

#### • AFTER

A read/write transaction waits until its changes have been applied to all of the other members. This value has no effect on read-only transactions. This mode ensures that when a transaction is committed on the local member, any subsequent transaction reads the written value or a more recent value on any group member. Use this mode with a group that is used for predominantly readonly operations to ensure that applied read/write transactions are applied everywhere once they commit. This could be used by your application to ensure that subsequent reads fetch the latest data which includes the latest writes. This reduces the overhead of synchronization on every read-only transaction, by ensuring synchronization is used only on read/write transactions. This consistency level also includes the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

#### • BEFORE\_AND\_AFTER

A read/write transaction waits for 1) all preceding transactions to complete before being applied and 2) until its changes have been applied on other members. A read-only transaction waits for all preceding transactions to complete before execution takes place. This consistency level also includes the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

The BEFORE and BEFORE\_AND\_AFTER consistency levels can be used on both read-only and read/ write transactions. The AFTER consistency level has no impact on read-only transactions, because they do not generate changes.

### <span id="page-54-0"></span>**How to Choose a Consistency Level**

The different consistency levels provide flexibility to both DBAs, who can use them to set up their infrastructure; and to developers who can use the consistency level that best suits their application's requirements. The following scenarios show how to choose a consistency guarantee level based on how you use your group:

• Scenario 1: You want to balance reads without being concerned about stale reads, and group write operations are considerably fewer than group read operations. In this case, you should choose AFTER.

- Scenario 2: For a data set that applies many writes, you want to perform occasional reads without concerns about reading stale data. In this case, you should choose BEFORE.
- Scenario 3: You want specific transactions to read only up-to-date data from the group, so that whenever sensitive data such as credentials for a file is updated, reads always use the most recent value. In this case, you should choose BEFORE.
- Scenario 4: For a group that has predominantly read-only data, you want read/write transactions to be applied everywhere once they commit, so that subsequent reads are done on data that includes your latest writes and you do not incur the cost of synchronization for every read-only transaction, but only for read/write transactions. In this case, you should choose AFTER.
- Scenario 5: For a group that works predominantly with read-only data, you want read/write transactions to read up-to-date data from the group and to be applied everywhere once they commit, so that subsequent reads are performed on data that includes the latest write and you do not incur the cost of synchronization for every read-only transaction, but only for read/write transactions. In this case, you should choose BEFORE\_AND\_AFTER.

You can choose the scope for which the consistency level is enforced by setting [group\\_replication\\_consistency](#page-136-0) with session or global scope. This is important because consistency levels can have a negative impact on group performance they apply globally.

To enforce the consistency level for the current session, use session scope, like this:

```
> SET @@SESSION.group_replication_consistency= 'BEFORE';
```

To enforce the consistency level for all sessions, use global scope, as shown here:

```
> SET @@GLOBAL.group_replication_consistency= 'BEFORE';
```

The possibility of setting the consistency level on specific sessions enables you to take advantage of scenarios such as those listed here:

- Scenario 6: A given system handles several instructions that do not require a strong consistency level, but one kind of instruction does require strong consistency: managing access permissions to documents;. In this scenario, the system changes access permissions and it wants to be sure that all clients see the correct permission. You only need to SET @@SESSION.group\_replication\_consistency= 'AFTER', on those instructions and leave the other instructions to run with EVENTUAL set at the global scope.
- Scenario 7: On the same system as described in Scenario 6, a command that performs analytics needs to be executed daily, using the most up-to-date data. To achieve this, you need only run the SQL statement SET @@SESSION.group\_replication\_consistency= 'BEFORE' prior to executing the command.

In sum, you do not need to run all transactions with the same specific consistency level, especially if only some transactions actually require it.

You should be aware that all read/write transactions are always ordered in Group Replication, so even when you set the consistency level to AFTER for the current session, this transaction waits until its changes are applied on all members, which means waiting for this and all preceding transactions that could be in the secondaries' queues. In other words, the consistency level AFTER waits for everything up to and including this transaction.

### <span id="page-55-0"></span>**Impacts of Consistency Levels**

Another way to classify the consistency levels is in terms of impact on the group, that is, the repercussions that the consistency levels have on the other members.

The BEFORE consistency level, apart from being ordered on the transaction stream, only impacts on the local member. That is, it does not require coordination with the other members and does not have repercussions on their transactions. In other words, BEFORE only impacts the transactions on which it is used.

The AFTER and BEFORE\_AND\_AFTER consistency levels do have side-effects on concurrent transactions executed on other members. These consistency levels make the other members transactions wait if transactions with the EVENTUAL consistency level start while a transaction with AFTER or BEFORE\_AND\_AFTER is executing. The other members wait until the AFTER transaction is committed on that member, even if the other member's transactions have the EVENTUAL consistency level. In other words, AFTER and BEFORE\_AND\_AFTER impact all ONLINE group members.

To illustrate this further, imagine a group with 3 members, M1, M2 and M3. On member M1 a client issues:

```
> SET @@SESSION.group_replication_consistency= AFTER;
> BEGIN;
> INSERT INTO t1 VALUES (1);
> COMMIT;
```

Then, while the above transaction is being applied, on member M2 a client issues:

```
> SET SESSION group_replication_consistency= EVENTUAL;
```

In this situation, even though the second transaction's consistency level is EVENTUAL, because it starts executing while the first transaction is already in the commit phase on M2, the second transaction has to wait for the first transaction to finish the commit and only then can it execute.

You can only use the consistency levels BEFORE, AFTER and BEFORE\_AND\_AFTER on ONLINE members, attempting to use them on members in other states causes a session error.

Transactions whose consistency level is not EVENTUAL hold execution until a timeout, configured by wait\_timeout value is reached, which defaults to 8 hours. If the timeout is reached an [ER\\_GR\\_HOLD\\_WAIT\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_gr_hold_wait_timeout) error is thrown.

### <span id="page-56-0"></span>**Impact of Consistency on Primary Election**

This section describes how a group's consistency level impacts on a single-primary group that has elected a new primary. Such a group automatically detects failures and adjusts the view of the members that are active, in other words the membership configuration. Furthermore, if a group is deployed in single-primary mode, whenever the group's membership changes there is a check performed to detect if there is still a primary member in the group. If there is none, a new one is selected from the list of secondary members. Typically, this is known as the secondary promotion.

Given the fact that the system detects failures and reconfigures itself automatically, the user may also expect that once the promotion takes place, the new primary is in the exact state, data-wise, as that of the old one. In other words, the user may expect that there is no backlog of replicated transactions to be applied on the new primary once he is able to read from and write to it. In practical terms, the user may expect that once his application fails-over to the new primary, there would be no chance, even if temporarily, to read old data or write into old data records.

When flow control is activated and properly tuned on a group, there is only a small chance of transiently reading stale data from a newly elected primary immediately after the promotion, as there should not be a backlog, or if there is one it should be small. Moreover, you might have a proxy or middleware layers that govern application accesses to the primary after a promotion and enforce the consistency criteria at that level. You can specify the behavior of the new primary once it is promoted using the [group\\_replication\\_consistency](#page-136-0) variable, which controls whether a newly elected primary blocks both reads and writes until after the backlog is fully applied. If the [group\\_replication\\_consistency](#page-136-0) variable was set to BEFORE\_ON\_PRIMARY\_FAILOVER on a newly elected primary which has backlog to apply, and transactions are issued against the new primary while it is still applying the backlog, incoming transactions are blocked until the backlog is fully applied. This prevents the following anomalies:

- No stale reads for read-only and read/write transactions. This prevents stale reads from being externalized to the application by the new primary.
- No spurious rollbacks for read/write transactions, due to write-write conflicts with replicated read/ write transactions still in the backlog waiting to be applied.
- No read skew on read/write transactions, such as this one:

```
> BEGIN;
> SELECT x FROM t1; -- x=1 because x=2 is in the backlog;
> INSERT x INTO t2;
> COMMIT;
```

This query should not cause a conflict but writes outdated values.

To summarize, when [group\\_replication\\_consistency](#page-136-0) is set to BEFORE\_ON\_PRIMARY\_FAILOVER you are choosing to prioritize consistency over availability, because reads and writes are held whenever a new primary is elected. This is the trade-off you have to consider when configuring your group. It should also be remembered that if flow control is working correctly, backlog should be minimal. Note that the higher consistency levels BEFORE, AFTER, and BEFORE\_AND\_AFTER also include the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

To guarantee that the group provides the same consistency level regardless of which member is promoted to primary, all members of the group should have BEFORE\_ON\_PRIMARY\_FAILOVER (or a higher consistency level) persisted to their configuration. For example, on each member issue:

```
> SET PERSIST group_replication_consistency='BEFORE_ON_PRIMARY_FAILOVER';
```

This ensures that the members all behave in the same way, and that the configuration is persisted after a restart of the member.

A transaction cannot be on-hold forever, and if the time held exceeds wait\_timeout it returns an ER\_GR\_HOLD\_WAIT\_TIMEOUT error.

### <span id="page-57-0"></span>**Permitted Queries Under Consistency Rules**

Although all writes are held when using BEFORE\_ON\_PRIMARY\_FAILOVER consistency level, not all reads are blocked to ensure that you can still inspect the server while it is applying backlog after a promotion took place. This is useful for debugging, monitoring, observability and troubleshooting. Some queries that do not modify data are allowed, such as the following:

• SHOW statements: These are restricted to those that do not depend on data, only on status and configuration.

The SHOW statements that are allowed are SHOW VARIABLES, SHOW PROCESSLIST, SHOW STATUS, SHOW ENGINE INNODB LOGS, SHOW ENGINE INNODB STATUS, SHOW ENGINE INNODB MUTEX, SHOW BINARY LOG STATUS, SHOW REPLICA STATUS, SHOW CHARACTER SET, SHOW COLLATION, SHOW BINARY LOGS, SHOW OPEN TABLES, SHOW REPLICAS, SHOW BINLOG EVENTS, SHOW WARNINGS, SHOW ERRORS, SHOW ENGINES, SHOW PRIVILEGES, SHOW PROCEDURE STATUS, SHOW FUNCTION STATUS, SHOW PLUGINS, SHOW EVENTS, SHOW PROFILE, SHOW PROFILES, and SHOW RELAYLOG EVENTS.

- SET statements
- DO statements that do not use tables or loadable functions
- EMPTY statements
- USE statements
- Using SELECT statements against the performance\_schema and sys databases
- Using SELECT statements against the PROCESSLIST table from the infoschema database

- SELECT statements that do not use tables or loadable functions
- STOP GROUP\_REPLICATION statements
- SHUTDOWN statements
- RESET PERSIST statements

# <span id="page-58-0"></span>**20.5.4 Distributed Recovery**

Whenever a member joins or rejoins a replication group, it must catch up with the transactions that were applied by the group members before it joined, or while it was away. This process is called distributed recovery.

The joining member begins by checking the relay log for its group\_replication\_applier channel for any transactions that it already received from the group but did not yet apply. If the joining member was in the group previously, it might find unapplied transactions from before it left, in which case it applies these as a first step. A member that is new to the group does not have anything to apply.

After this, the joining member connects to an online existing member to carry out state transfer. The joining member transfers all the transactions that took place in the group before it joined or while it was away, which are provided by the existing member (called the donor). Next, the joining member applies the transactions that took place in the group while this state transfer was in progress. When this process is complete, the joining member has caught up with the remaining servers in the group, and it begins to participate normally in the group.

Group Replication uses a combination of these methods for state transfer during distributed recovery:

- A remote cloning operation using the clone plugin's function. To enable this method of state transfer, you must install the clone plugin on the group members and the joining member. Group Replication automatically configures the required clone plugin settings and manages the remote cloning operation.
- Replicating from a donor's binary log and applying the transactions on the joining member. This method uses a standard asynchronous replication channel named group\_replication\_recovery that is established between the donor and the joining member.

Group Replication automatically selects the best combination of these methods for state transfer after you issue START GROUP\_REPLICATION on the joining member. To do this, Group Replication checks which existing members are suitable as donors, how many transactions the joining member needs from a donor, and whether any required transactions are no longer present in the binary log files on any group member. If the transaction gap between the joining member and a suitable donor is large, or if some required transactions are not in any donor's binary log files, Group Replication begins distributed recovery with a remote cloning operation. If there is not a large transaction gap, or if the clone plugin is not installed, Group Replication proceeds directly to state transfer from a donor's binary log.

- During a remote cloning operation, the existing data on the joining member is removed, and replaced with a copy of the donor's data. When the remote cloning operation is complete and the joining member has restarted, state transfer from a donor's binary log is carried out to get the transactions that the group applied while the remote cloning operation was in progress.
- During state transfer from a donor's binary log, the joining member replicates and applies the required transactions from the donor's binary log, applying the transactions as they are received, up to the point where the binary log records that the joining member joined the group (a view change event). While this is in progress, the joining member buffers the new transactions that the group applies. When state transfer from the binary log is complete, the joining member applies the buffered transactions.

When the joining member is up to date with all the group's transactions, it is declared online and can participate in the group as a normal member, and distributed recovery is complete.

![](_page_59_Picture_1.jpeg)

#### **Tip**

State transfer from the binary log is Group Replication's base mechanism for distributed recovery, and if the donors and joining members in your replication group are not set up to support cloning, this is the only available option. As state transfer from the binary log is based on classic asynchronous replication, it might take a very long time if the server joining the group does not have the group's data at all, or has data taken from a very old backup image. In this situation, it is therefore recommended that before adding a server to the group, you should set it up with the group's data by transferring a fairly recent snapshot of a server already in the group. This minimizes the time taken for distributed recovery, and reduces the impact on donor servers, since they have to retain and transfer fewer binary log files.

# <span id="page-59-0"></span>**20.5.4.1 Connections for Distributed Recovery**

When a joining member connects to an online existing member for state transfer during distributed recovery, the joining member acts as a client on the connection and the existing member acts as a server. When state transfer from the donor's binary log is in progress over this connection (using the asynchronous replication channel group\_replication\_recovery), the joining member acts as the replica and the existing member acts as the source. When a remote cloning operation is in progress over this connection, the joining member acts as a recipient and the existing member acts as a donor. Configuration settings that apply to those roles outside the Group Replication context can apply for Group Replication also, unless they are overridden by a Group Replication-specific configuration setting or behavior.

The connection that an existing member offers to a joining member for distributed recovery is not the same connection that is used by Group Replication for communication between online members of the group.

- The connection used by the group communication engine for Group Replication (XCom, a Paxos variant) for TCP communication between remote XCom instances is specified by the [group\\_replication\\_local\\_address](#page-148-0) system variable. This connection is used for TCP/IP messages between online members. Communication with the local instance is over an input channel using shared memory.
- For distributed recovery, by default, group members offer their standard SQL client connection to joining members, as specified by hostname and port. If an alternative port number is specified by report\_port, that one is used instead.
- Group members may instead advertise an alternative list of distributed recovery endpoints as dedicated client connections for joining members, allowing you to control distributed recovery traffic separately from connections by regular client users of the member. A member transmits the list of distributed recovery endpoints specified by [group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0) to the group when it joins. By default, the member continues to offer the standard SQL client connection as in earlier releases.

![](_page_59_Picture_10.jpeg)

#### **Important**

Distributed recovery can fail if a joining member cannot correctly identify the other members using the host name as defined by MySQL Server's hostname system variable. It is recommended that operating systems running MySQL have a properly configured unique host name, either using DNS or local settings. The host name that the server is using for SQL client connections can be verified in the Member\_host column of the Performance Schema table replication\_group\_members. If multiple group members externalize a default host name set by the operating system, there is a chance of the joining member not resolving it to the correct member address and not being able to connect for distributed recovery. In this situation you can use MySQL

Server's report\_host system variable to configure a unique host name to be externalized by each of the servers.

The steps for a joining member to establish a connection for distributed recovery are as follows:

- 1. When the member joins the group, it connects with one of the seed members included in the list in its [group\\_replication\\_group\\_seeds](#page-145-1) system variable, initially using the [group\\_replication\\_local\\_address](#page-148-0) connection as specified in that list. The seed members might be a subset of the group.
- 2. Over this connection, the seed member uses Group Replication's membership service to provide the joining member with a list of all the members that are online in the group, in the form of a view. The membership information includes the details of the distributed recovery endpoints or standard SQL client connection offered by each member for distributed recovery.
- 3. The joining member selects a suitable group member from this list to be its donor for distributed recovery, following the behaviors described in [Section 20.5.4.4, "Fault Tolerance for Distributed](#page-66-0) [Recovery".](#page-66-0)
- 4. The joining member then attempts to connect to the donor using the donor's advertised distributed recovery endpoints, trying each in turn in the order they are specified in the list. If the donor provides no endpoints, the joining member attempts to connect using the donor's standard SQL client connection. The SSL requirements for the connection are as specified by the group\_replication\_recovery\_ssl\_\* options described in [SSL and Authentication for](#page-61-0) [Distributed Recovery.](#page-61-0)
- 5. If the joining member is not able to connect to the selected donor, it retries with other suitable donors, following the behaviors described in [Section 20.5.4.4, "Fault Tolerance for Distributed](#page-66-0) [Recovery".](#page-66-0) Note that if the joining member exhausts the list of advertised endpoints without making a connection, it does not fall back to the donor's standard SQL client connection, but switches to another donor.
- 6. When the joining member establishes a distributed recovery connection with a donor, it uses that connection for state transfer as described in [Section 20.5.4, "Distributed Recovery".](#page-58-0) The host and port for the connection that is used are shown in the joining member's log. Note that if a remote cloning operation is used, when the joining member has restarted at the end of the operation, it establishes a connection with a new donor for state transfer from the binary log. This might be a connection to a different member from the original donor used for the remote cloning operation, or it might be a different connection to the original donor. In any case, the distributed recovery process continues in the same way as it would have with the original donor.

### <span id="page-60-0"></span>**Selecting addresses for distributed recovery endpoints**

IP addresses supplied by the [group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0) system variable as distributed recovery endpoints do not have to be configured for MySQL Server (that is, they do not have to be specified by the admin\_address system variable or in the list for the bind\_address system variable). They do have to be assigned to the server. Any host names used must resolve to a local IP address. IPv4 and IPv6 addresses can be used.

The ports supplied for the distributed recovery endpoints do have to be configured for MySQL Server, so they must be specified by the port, report\_port, or admin\_port system variable. The server must listen for TCP/IP connections on these ports. If you specify the admin\_port, the replication user for distributed recovery needs the SERVICE\_CONNECTION\_ADMIN privilege to connect. Selecting the admin\_port keeps distributed recovery connections separate from regular MySQL client connections.

Joining members try each of the endpoints in turn in the order they are specified on the list. If [group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0) is set to DEFAULT rather than a list of endpoints, the standard SQL client connection is offered. Note that the standard SQL client connection is not automatically included on a list of distributed recovery endpoints, and is not offered as a fallback if the donor's list of endpoints is exhausted without a connection. If you want to offer the standard SQL

client connection as one of a number of distributed recovery endpoints, you must include it explicitly in the list specified by [group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0). You can put it in the last place so that it acts as a last resort for connection.

A group member's distributed recovery endpoints (or standard SQL client connection if endpoints are not provided) do not need to be added to the Group Replication allowlist specified by the [group\\_replication\\_ip\\_allowlist](#page-146-1) system variable. The allowlist is only for the address specified by [group\\_replication\\_local\\_address](#page-148-0) for each member. A joining member must have its initial connection to the group permitted by the allowlist in order to retrieve the address or addresses for distributed recovery.

The distributed recovery endpoints that you list are validated when the system variable is set and when a START GROUP\_REPLICATION statement has been issued. If the list cannot be parsed correctly, or if any of the endpoints cannot be accessed on the host because the server is not listening on them, Group Replication logs an error and does not start.

### **Compression for Distributed Recovery**

You can optionally configure compression for distributed recovery by the method of state transfer from a donor's binary log. Compression can benefit distributed recovery where network bandwidth is limited and the donor has to transfer many transactions to the joining member. The [group\\_replication\\_recovery\\_compression\\_algorithms](#page-154-0) and [group\\_replication\\_recovery\\_zstd\\_compression\\_level](#page-162-1) system variables determine permitted compression algorithms, and the zstd compression level used when carrying out state transfer from a donor's binary log. For more information, see Section 6.2.8, "Connection Compression Control".

These compression settings do not apply to remote cloning operations. When a remote cloning operation is used for distributed recovery, the clone plugin's setting for clone\_enable\_compression applies.

### **Replication User for Distributed Recovery**

Distributed recovery requires a replication user that has the correct permissions so that Group Replication can establish direct member-to-member replication channels. The replication user must also have the correct permissions to act as the clone user on the donor for a remote cloning operation. The same replication user must be used for distributed recovery on every group member. For instructions to set up this replication user, see [Section 20.2.1.3, "User Credentials For Distributed](#page-27-0) [Recovery".](#page-27-0) For instructions to secure the replication user credentials, see [Section 20.6.3.1, "Secure](#page-85-0) [User Credentials for Distributed Recovery".](#page-85-0)

# <span id="page-61-0"></span>**SSL and Authentication for Distributed Recovery**

SSL for distributed recovery is configured separately from SSL for normal group communications, which is determined by the server's SSL settings and the [group\\_replication\\_ssl\\_mode](#page-163-0) system variable. For distributed recovery connections, dedicated Group Replication distributed recovery SSL system variables are available to configure the use of certificates and ciphers specifically for distributed recovery.

By default, SSL is not used for distributed recovery connections. To activate it, set [group\\_replication\\_recovery\\_use\\_ssl=ON](#page-161-0), and configure the Group Replication distributed recovery SSL system variables as described in [Section 20.6.3, "Securing Distributed Recovery](#page-84-0) [Connections".](#page-84-0) You need a replication user that is set up to use SSL.

When distributed recovery is configured to use SSL, Group Replication applies this setting for remote cloning operations, as well as for state transfer from a donor's binary log. Group Replication automatically configures the settings for the clone SSL options (clone\_ssl\_ca, clone\_ssl\_cert, and clone\_ssl\_key) to match your settings for the corresponding

Group Replication distributed recovery options ([group\\_replication\\_recovery\\_ssl\\_ca](#page-156-0), [group\\_replication\\_recovery\\_ssl\\_cert](#page-157-0), and [group\\_replication\\_recovery\\_ssl\\_key](#page-159-0)).

If you are not using SSL for distributed recovery (so [group\\_replication\\_recovery\\_use\\_ssl](#page-161-0) is set to OFF), and the replication user account for Group Replication authenticates with the caching\_sha2\_password plugin (the default) or the sha256\_password plugin (deprecated), RSA key pairs are used for password exchange. In this case, either use the [group\\_replication\\_recovery\\_public\\_key\\_path](#page-155-0) system variable to specify the RSA public key file, or use the [group\\_replication\\_recovery\\_get\\_public\\_key](#page-155-1) system variable to request the public key from the source, as described in [Replication User With The Caching SHA-2 Authentication](#page-85-1) [Plugin.](#page-85-1)

# <span id="page-62-0"></span>**20.5.4.2 Cloning for Distributed Recovery**

If you want to use remote cloning operations for distributed recovery in a group, you must set up existing members and joining members beforehand to support this function. If you do not want to use this function in a group, do not set it up, in which case Group Replication only uses state transfer from the binary log.

To use cloning, at least one existing group member and the joining member must be set up beforehand to support remote cloning operations. As a minimum, you must install the clone plugin on the donor and joining member, grant the BACKUP\_ADMIN permission to the replication user for distributed recovery, and set the [group\\_replication\\_clone\\_threshold](#page-131-1) system variable to an appropriate level. To ensure the maximum availability of donors, it is advisable to set up all current and future group members to support remote cloning operations.

Be aware that a remote cloning operation removes user-created tablespaces and data from the joining member before transferring the data from the donor. If the operation is stopped while in progress, the joining member might be left with partial data or no data. This can be repaired by retrying the remote cloning operation, which Group Replication does automatically.

### **Prerequisites for Cloning**

For full instructions to set up and configure the clone plugin, see Section 7.6.7, "The Clone Plugin" . Detailed prerequisites for a remote cloning operation are covered in Section 7.6.7.3, "Cloning Remote Data" . For Group Replication, note the following key points and differences:

- The donor (an existing group member) and the recipient (the joining member) must have the clone plugin installed and active. For instructions to do this, see Section 7.6.7.1, "Installing the Clone Plugin" .
- The donor and the recipient must run on the same operating system, and must use the same MySQL Server release series. Cloning is therefore not suitable for groups where members run different minor MySQL Server versions, such as MySQL 8.0 and 8.4.
- The donor and the recipient must have the Group Replication plugin installed and active, and any other plugins that are active on the donor (such as a keyring plugin) must also be active on the recipient.
- If distributed recovery is configured to use SSL ([group\\_replication\\_recovery\\_use\\_ssl=ON](#page-161-0)), Group Replication applies this setting for remote cloning operations. Group Replication automatically configures the settings for the clone SSL options (clone\_ssl\_ca, clone\_ssl\_cert, and clone\_ssl\_key) to match your settings for the corresponding Group Replication distributed recovery options ([group\\_replication\\_recovery\\_ssl\\_ca](#page-156-0), [group\\_replication\\_recovery\\_ssl\\_cert](#page-157-0), and [group\\_replication\\_recovery\\_ssl\\_key](#page-159-0)).
- You do not need to set up a list of valid donors in the clone\_valid\_donor\_list system variable for the purpose of joining a replication group. Group Replication configures this setting automatically for you after it selects a donor from the existing group members. Note that remote cloning operations use the server's SQL protocol hostname and port.

- The clone plugin has a number of system variables to manage the network load and performance impact of the remote cloning operation. Group Replication does not configure these settings, so you can review them and set them if you want to, or allow them to default. Note that when a remote cloning operation is used for distributed recovery, the clone plugin's clone\_enable\_compression setting applies to the operation, rather than the Group Replication compression setting.
- To invoke the remote cloning operation on the recipient, Group Replication uses the internal mysql.session user, which already has the CLONE\_ADMIN privilege, so you do not need to set this up.
- As the clone user on the donor for the remote cloning operation, Group Replication uses the replication user that you set up for distributed recovery (which is covered in [Section 20.2.1.3, "User](#page-27-0) [Credentials For Distributed Recovery"](#page-27-0)). You must therefore give the BACKUP\_ADMIN privilege to this replication user on all group members that support cloning. Also give the privilege to the replication user on joining members when you are configuring them for Group Replication, because they can act as donors after they join the group. The same replication user is used for distributed recovery on every group member. To give this privilege to the replication user on existing members, you can issue this statement on each group member individually with binary logging disabled, or on one group member with binary logging enabled:

GRANT BACKUP\_ADMIN ON \*.\* TO rpl\_user@'%';

• If you use START GROUP\_REPLICATION to specify the replication user credentials on a server that previously supplied the user credentials using CHANGE REPLICATION SOURCE TO, ensure that you remove the user credentials from the replication metadata repositories before any remote cloning operations take place. Also ensure that [group\\_replication\\_start\\_on\\_boot=OFF](#page-164-0) is set on the joining member. For instructions, see [Section 20.6.3, "Securing Distributed Recovery Connections"](#page-84-0). If you do not unset the user credentials, they are transferred to the joining member during remote cloning operations. The group\_replication\_recovery channel could then be inadvertently started with the stored credentials, on either the original member or members that were cloned from it. An automatic start of Group Replication on server boot (including after a remote cloning operation) would use the stored user credentials, and they would also be used if an operator did not specify the distributed recovery credentials on a START GROUP\_REPLICATION statement.

### **Threshold for Cloning**

When group members have been set up to support cloning, the [group\\_replication\\_clone\\_threshold](#page-131-1) system variable specifies a threshold, expressed as a number of transactions, for the use of a remote cloning operation in distributed recovery. If the gap between the transactions on the donor and the transactions on the joining member is larger than this number, a remote cloning operation is used for state transfer to the joining member when this is technically possible. Group Replication calculates whether the threshold has been exceeded based on the gtid\_executed sets of the existing group members. Using a remote cloning operation in the event of a large transaction gap lets you add new members to the group without transferring the group's data to the server manually beforehand, and also enables a member that is very out of date to catch up more efficiently.

The default setting for the [group\\_replication\\_clone\\_threshold](#page-131-1) Group Replication system variable is extremely high (the maximum permitted sequence number for a transaction in a GTID), so it effectively deactivates cloning wherever state transfer from the binary log is possible. To enable Group Replication to select a remote cloning operation for state transfer where this is more appropriate, set the system variable to specify a number of transactions as the transaction gap above which you want cloning to take place.

![](_page_63_Picture_9.jpeg)

#### **Warning**

Do not use a low setting for [group\\_replication\\_clone\\_threshold](#page-131-1) in an active group. If a number of transactions above the threshold takes place in the group while the remote cloning operation is in progress, the joining member triggers a remote cloning operation again after restarting, and could continue

this indefinitely. To avoid this situation, ensure that you set the threshold to a number higher than the number of transactions that you would expect to occur in the group during the time taken for the remote cloning operation.

Group Replication attempts to execute a remote cloning operation regardless of your threshold when state transfer from a donor's binary log is impossible, for example because the transactions needed by the joining member are not available in the binary log on any existing group member. Group Replication identifies this based on the gtid\_purged sets of the existing group members. You cannot use the [group\\_replication\\_clone\\_threshold](#page-131-1) system variable to deactivate cloning when the required transactions are not available in any member's binary log files, because in that situation cloning is the only alternative to transferring data to the joining member manually.

# **Cloning Operations**

When group members and joining members are set up for cloning, Group Replication manages remote cloning operations for you. A remote cloning operation might take some time to complete, depending on the size of the data. See Section 7.6.7.10, "Monitoring Cloning Operations" for information on monitoring the process.

![](_page_64_Picture_5.jpeg)

#### **Note**

When state transfer is complete, Group Replication restarts the joining member to complete the process. If [group\\_replication\\_start\\_on\\_boot=OFF](#page-164-0) is set on the joining member, for example because you specify the replication user credentials on the START GROUP\_REPLICATION statement, you must issue START GROUP\_REPLICATION manually again following this restart. If [group\\_replication\\_start\\_on\\_boot=ON](#page-164-0) and other settings required to start Group Replication were set in a configuration file or using a SET PERSIST statement, you do not need to intervene and the process continues automatically to bring the joining member online.

A remote cloning operation clones settings that are persisted in tables from the donor to the recipient, as well as the data. Group Replication manages the settings that relate specifically to Group Replication channels. Group Replication member settings that are persisted in configuration files, such as the group replication local address, are not cloned and are not changed on the joining member. Group Replication also preserves the channel settings that relate to the use of SSL, so these are unique to the individual member.

If the replication user credentials used by the donor for the group\_replication\_recovery replication channel have been stored in the replication metadata repositories using a CHANGE REPLICATION SOURCE TO statement, they are transferred to and used by the joining member after cloning, and they must be valid there. With stored credentials, all group members that received state transfer by a remote cloning operation therefore automatically receive the replication user and password for distributed recovery. If you specify the replication user credentials on the START GROUP\_REPLICATION statement, these are used to start the remote cloning operation, but they are not transferred to and used by the joining member after cloning. If you do not want the credentials transferred to new joiners and recorded there, ensure that you unset them before remote cloning operations take place, as described in [Section 20.6.3, "Securing Distributed Recovery Connections"](#page-84-0), and use START GROUP\_REPLICATION to supply them instead.

If a PRIVILEGE\_CHECKS\_USER account has been used to help secure the replication appliers (see Section 19.3.3.2, "Privilege Checks For Group Replication Channels"), the PRIVILEGE\_CHECKS\_USER account and related settings from the donor are cloned to the joining member. If the joining member is set to start Group Replication on boot, it automatically uses the account for privilege checks on the appropriate replication channels.

### <span id="page-64-0"></span>**Cloning for Other Purposes**

Group Replication initiates and manages cloning operations for distributed recovery. Group members that have been set up to support cloning may also participate in cloning operations that a user initiates manually. For example, you might want to create a new server instance by cloning from a group member as the donor, but you do not want the new server instance to join the group immediately, or maybe not ever.

In all releases that support cloning, you can initiate a cloning operation manually involving a group member on which Group Replication is stopped. Note that because cloning requires that the active plugins on a donor and recipient must match, the Group Replication plugin must be installed and active on the other server instance, even if you do not intend that server instance to join a group. You can install the plugin by issuing this statement:

```
INSTALL PLUGIN group_replication SONAME 'group_replication.so';
```

You can initiate a cloning operation manually if the operation involves a group member on which Group Replication is running, provided that the cloning operation does not remove and replace the data on the recipient. The statement to initiate the cloning operation must therefore include the DATA DIRECTORY clause if Group Replication is running.

# <span id="page-65-0"></span>**20.5.4.3 Configuring Distributed Recovery**

Several aspects of Group Replication's distributed recovery process can be configured to suit your system.

### **Number of Connection Attempts**

For state transfer from the binary log, Group Replication limits the number of attempts a joining member makes when trying to connect to a donor from the pool of donors. If the connection retry limit is reached without a successful connection, the distributed recovery procedure terminates with an error. Note that this limit specifies the total number of attempts that the joining member makes to connect to a donor. For example, if 2 group members are suitable donors, and the connection retry limit is set to 4, the joining member makes 2 attempts to connect to each of the donors before reaching the limit.

The default connection retry limit is 10. You can configure this setting using the [group\\_replication\\_recovery\\_retry\\_count](#page-156-1) system variable. The following statement sets the maximum number of attempts to connect to a donor to 5:

```
mysql> SET GLOBAL group_replication_recovery_retry_count= 5;
```

For remote cloning operations, this limit does not apply. Group Replication makes only one connection attempt to each suitable donor for cloning, before starting to attempt state transfer from the binary log.

### **Sleep Interval for Connection Attempts**

For state transfer from the binary log, the [group\\_replication\\_recovery\\_reconnect\\_interval](#page-156-2) system variable defines how much time the distributed recovery process should sleep between donor connection attempts. Note that distributed recovery does not sleep after every donor connection attempt. As the joining member is connecting to different servers and not to the same one repeatedly, it can assume that the problem that affects server A does not affect server B. Distributed recovery therefore suspends only when it has gone through all the possible donors. Once the server joining the group has made one attempt to connect to each of the suitable donors in the group, the distributed recovery process sleeps for the number of seconds configured by the [group\\_replication\\_recovery\\_reconnect\\_interval](#page-156-2) system variable. For example, if 2 group members are suitable donors, and the connection retry limit is set to 4, the joining member makes one attempt to connect to each of the donors, then sleeps for the connection retry interval, then makes one further attempt to connect to each of the donors before reaching the limit.

The default connection retry interval is 60 seconds, and you can change this value dynamically. The following statement sets the distributed recovery donor connection retry interval to 120 seconds:

```
mysql> SET GLOBAL group_replication_recovery_reconnect_interval= 120;
```

For remote cloning operations, this interval does not apply. Group Replication makes only one connection attempt to each suitable donor for cloning, before starting to attempt state transfer from the binary log.

### **Marking the Joining Member Online**

When distributed recovery has successfully completed state transfer from the donor to the joining member, the joining member can be marked as online in the group and ready to participate. This is done after the new member has received and applied all the transactions that it missed prior to joining the group.

# <span id="page-66-0"></span>**20.5.4.4 Fault Tolerance for Distributed Recovery**

Group Replication's distributed recovery process has a number of built-in measures to ensure fault tolerance in the event of any problems during the process.

The donor for distributed recovery is selected randomly from the existing list of suitable online group members in the current view. Selecting a random donor means that there is a good chance that the same server is not selected more than once when multiple members enter the group. For state transfer from the binary log, the joiner selects a donor that is running a lower or equal patch version of MySQL Server compared to itself. For earlier releases, all of the online members are allowed to be a donor. For a remote cloning operation, the joiner selects a donor that is running the same patch version as itself. When the member joining has restarted at the end of the operation, it establishes a connection with a new donor for state transfer from the binary log, which might be a different member from the original donor used for the remote cloning operation.

In the following situations, Group Replication detects an error in distributed recovery, automatically switches over to a new donor, and retries the state transfer:

- Connection error There is an authentication issue or another problem with making the connection to a candidate donor.
- Replication errors One of the replication threads (the receiver or applier threads) being used for state transfer from the binary log fails. Because this method of state transfer uses the existing MySQL replication framework, it is possible that some transient errors could cause errors in the receiver or applier threads.
- Remote cloning operation errors A remote cloning operation fails or is stopped before it completes.
- Donor leaves the group The donor leaves the group, or Group Replication is stopped on the donor, while state transfer is in progress.

The Performance Schema table replication\_applier\_status\_by\_worker displays the error that caused the last retry. In these situations, the new connection following the error is attempted with a new candidate donor. Selecting a different donor in the event of an error means that there is a chance the new candidate donor does not have the same error. If the clone plugin is installed, Group Replication attempts a remote cloning operation with each of the suitable online clone-supporting donors first. If all those attempts fail, Group Replication attempts state transfer from the binary log with all the suitable donors in turn, if that is possible.

![](_page_66_Picture_13.jpeg)

#### **Warning**

For a remote cloning operation, user-created tablespaces and data on the recipient (the joining member) are dropped before the remote cloning operation begins to transfer the data from the donor. If the remote cloning operation starts but does not complete, the joining member might be left with a partial set of its original data files, or with no user data. Data transferred by the donor is removed from the recipient if the cloning operation is stopped before the data is fully cloned. This situation can be repaired by retrying the cloning operation, which Group Replication does automatically.

In the following situations, the distributed recovery process cannot be completed, and the joining member leaves the group:

- Purged transactions Transactions that are required by the joining member are not present in any online group member's binary log files, and the data cannot be obtained by a remote cloning operation (because the clone plugin is not installed, or because cloning was attempted with all possible donors but failed). The joining member is therefore unable to catch up with the group.
- Extra transactions The joining member already contains some transactions that are not present in the group. If a remote cloning operation was carried out, these transactions would be deleted and lost, because the data directory on the joining member is erased. If state transfer from a donor's binary log was carried out, these transactions could conflict with the group's transactions. For advice on dealing with this situation, see [Extra Transactions.](#page-42-1)
- Connection retry limit reached The joining member has made all the connection attempts allowed by the connection retry limit. You can configure this using the [group\\_replication\\_recovery\\_retry\\_count](#page-156-1) system variable (see [Section 20.5.4.3,](#page-65-0) ["Configuring Distributed Recovery"](#page-65-0)).
- No more donors The joining member has unsuccessfully attempted a remote cloning operation with each of the online clone-supporting donors in turn (if the clone plugin is installed), then has unsuccessfully attempted state transfer from the binary log with each of the suitable online donors in turn, if possible.
- Joining member leaves the group The joining member leaves the group or Group Replication is stopped on the joining member while state transfer is in progress.

If the joining member left the group unintentionally, so in any situation listed above except the last, it proceeds to take the action specified by the [group\\_replication\\_exit\\_state\\_action](#page-138-0) system variable.