---
source: MySQL 8.0 Reference
title: 00_Overview
---

When binary log encryption is enabled, you can rotate the binary log master key at any time while the server is running by issuing ALTER INSTANCE ROTATE BINLOG MASTER KEY. When the binary log master key is rotated manually using this statement, the passwords for the new and subsequent files are encrypted using the new binary log master key, and also the file passwords for existing encrypted binary log files and relay log files are re-encrypted using the new binary log master key, so the encryption is renewed completely. You can rotate the binary log master key on a regular basis to comply with your organization's security policy, and also if you suspect that the current or any of the previous binary log master keys might have been compromised.

When you rotate the binary log master key manually, MySQL Server takes the following actions in sequence:

- 1. A new binary log encryption key is generated with the next available sequence number, stored on the keyring, and used as the new binary log master key.
- 2. The binary log and relay log files are rotated on all channels.
- 3. The new binary log master key is used to encrypt the file passwords for the new binary log and relay log files, and subsequent files until the key is changed again.
- 4. The file passwords for existing encrypted binary log files and relay log files on the server are reencrypted in turn using the new binary log master key, starting with the most recent files. Any unencrypted files are skipped.
- 5. Binary log encryption keys that are no longer in use for any files after the re-encryption process are removed from the keyring.

The BINLOG\_ENCRYPTION\_ADMIN privilege is required to issue ALTER INSTANCE ROTATE BINLOG MASTER KEY, and the statement cannot be used if the binlog\_encryption system variable is set to OFF.

As the final step of the binary log master key rotation process, all binary log encryption keys that no longer apply to any retained binary log files or relay log files are cleaned up from the keyring. If a retained binary log file or relay log file cannot be initialized for re-encryption, the relevant binary log encryption keys are not deleted in case the files can be recovered in the future. For example, this

might be the case if a file listed in a binary log index file is currently unreadable, or if a channel fails to initialize. If the server UUID changes, for example because a backup created using MySQL Enterprise Backup is used to set up a new replica, issuing ALTER INSTANCE ROTATE BINLOG MASTER KEY on the new server does not delete any earlier binary log encryption keys that include the original server UUID.

If any of the first four steps of the binary log master key rotation process cannot be completed correctly, an error message is issued explaining the situation and the consequences for the encryption status of the binary log files and relay log files. Files that were previously encrypted are always left in an encrypted state, but their file passwords might still be encrypted using an old binary log master key. If you see these errors, first retry the process by issuing ALTER INSTANCE ROTATE BINLOG MASTER KEY again. Then investigate the status of individual files to see what is blocking the process, especially if you suspect that the current or any of the previous binary log master keys might have been compromised.

If the final step of the binary log master key rotation process cannot be completed correctly, a warning message is issued explaining the situation. The warning message identifies whether the process could not clean up the auxiliary keys in the keyring for rotating the binary log master key, or could not clean up unused binary log encryption keys. You can choose to ignore the message as the keys are auxiliary keys or no longer in use, or you can issue ALTER INSTANCE ROTATE BINLOG MASTER KEY again to retry the process.

If the server stops and is restarted with binary log encryption still set to ON during the binary log master key rotation process, new binary log files and relay log files after the restart are encrypted using the new binary log master key. However, the re-encryption of existing files is not continued, so files that did not get re-encrypted before the server stopped are left encrypted using the previous binary log master key. To complete re-encryption and clean up unused binary log encryption keys, issue ALTER INSTANCE ROTATE BINLOG MASTER KEY again after the restart.

ALTER INSTANCE ROTATE BINLOG MASTER KEY actions are not written to the binary log and are not executed on replicas. Binary log master key rotation can therefore be carried out in replication environments including a mix of MySQL versions. To schedule regular rotation of the binary log master key on all applicable source and replica servers, you can enable the MySQL Event Scheduler on each server and issue the ALTER INSTANCE ROTATE BINLOG MASTER KEY statement using a CREATE EVENT statement. If you rotate the binary log master key because you suspect that the current or any of the previous binary log master keys might have been compromised, issue the statement on every applicable source and replica server. Issuing the statement on individual servers ensures that you can verify immediate compliance, even in the case of replicas that are lagging, belong to multiple replication topologies, or are not currently active in the replication topology but have binary log and relay log files.

The binlog\_rotate\_encryption\_master\_key\_at\_startup system variable controls whether the binary log master key is automatically rotated when the server is restarted. If this system variable is set to ON, a new binary log encryption key is generated and used as the new binary log master key whenever the server is restarted. If it is set to OFF, which is the default, the existing binary log master key is used again after the restart. When the binary log master key is rotated at startup, the file passwords for the new binary log and relay log files are encrypted using the new key. The file passwords for the existing encrypted binary log files and relay log files are not re-encrypted, so they remain encrypted using the old key, which remains available on the keyring.

# <span id="page-15-0"></span>**19.3.3 Replication Privilege Checks**

By default, MySQL replication (including Group Replication) does not carry out privilege checks when transactions that were already accepted by another server are applied on a replica or group member. From MySQL 8.0.18, you can create a user account with the appropriate privileges to apply the transactions that are normally replicated on a channel, and specify this as the PRIVILEGE\_CHECKS\_USER account for the replication applier, using a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23). MySQL then checks each transaction against the user account's privileges to verify that you have authorized the operation for that channel. The account can also be safely used by an

administrator to apply or reapply transactions from mysqlbinlog output, for example to recover from a replication error on the channel.

The use of a PRIVILEGE\_CHECKS\_USER account helps secure a replication channel against the unauthorized or accidental use of privileged or unwanted operations. The PRIVILEGE\_CHECKS\_USER account provides an additional layer of security in situations such as these:

- You are replicating between a server instance on your organization's network, and a server instance on another network, such as an instance supplied by a cloud service provider.
- You want to have multiple on-premise or off-site deployments administered as separate units, without giving one administrator account privileges on all the deployments.
- You want to have an administrator account that enables an administrator to perform only operations that are directly relevant to the replication channel and the databases it replicates, rather than having wide privileges on the server instance.

You can increase the security of a replication channel where privilege checks are applied by adding one or both of these options to the CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement when you specify the PRIVILEGE\_CHECKS\_USER account for the channel:

- The REQUIRE\_ROW\_FORMAT option (available from MySQL 8.0.19) makes the replication channel accept only row-based replication events. When REQUIRE\_ROW\_FORMAT is set, you must use row-based binary logging (binlog\_format=ROW) on the source server. In MySQL 8.0.18, REQUIRE\_ROW\_FORMAT is not available, but the use of row-based binary logging for secured replication channels is still strongly recommended. With statement-based binary logging, some administrator-level privileges might be required for the PRIVILEGE\_CHECKS\_USER account to execute transactions successfully.
- The REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option (available from MySQL 8.0.20) makes the replication channel use its own policy for primary key checks. Setting ON means that primary keys are always required, and setting OFF means that primary keys are never required. The default setting, STREAM, sets the session value of the sql\_require\_primary\_key system variable using the value that is replicated from the source for each transaction. When PRIVILEGE\_CHECKS\_USER is set, setting REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK to either ON or OFF means that the user account does not need session administration level privileges to set restricted session variables, which are required to change the value of sql\_require\_primary\_key. It also normalizes the behavior across replication channels for different sources.

You grant the REPLICATION\_APPLIER privilege to enable a user account to appear as the PRIVILEGE\_CHECKS\_USER for a replication applier thread, and to execute the internal-use BINLOG statements used by mysqlbinlog. The user name and host name for the PRIVILEGE\_CHECKS\_USER account must follow the syntax described in Section 8.2.4, "Specifying Account Names", and the user must not be an anonymous user (with a blank user name) or the CURRENT\_USER. To create a new account, use CREATE USER. To grant this account the REPLICATION\_APPLIER privilege, use the GRANT statement. For example, to create a user account priv\_repl, which can be used manually by an administrator from any host in the example.com domain, and requires an encrypted connection, issue the following statements:

```
mysql> SET sql_log_bin = 0;
mysql> CREATE USER 'priv_repl'@'%.example.com' IDENTIFIED BY 'password' REQUIRE SSL;
mysql> GRANT REPLICATION_APPLIER ON *.* TO 'priv_repl'@'%.example.com';
mysql> SET sql_log_bin = 1;
```

The SET sql\_log\_bin statements are used so that the account management statements are not added to the binary log and sent to the replication channels (see Section 15.4.1.3, "SET sql\_log\_bin Statement").

![](_page_16_Picture_12.jpeg)

#### **Important**

The caching\_sha2\_password authentication plugin is the default for new users created from MySQL 8.0 (for details, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication"). To connect to a server using a user account that authenticates with this plugin, you must either set up an encrypted connection as described in [Section 19.3.1, "Setting Up Replication to Use Encrypted](#page-9-0) [Connections"](#page-9-0), or enable the unencrypted connection to support password exchange using an RSA key pair.

After setting up the user account, use the GRANT statement to grant additional privileges to enable the user account to make the database changes that you expect the applier thread to carry out, such as updating specific tables held on the server. These same privileges enable an administrator to use the account if they need to execute any of those transactions manually on the replication channel. If an unexpected operation is attempted for which you did not grant the appropriate privileges, the operation is disallowed and the replication applier thread stops with an error. [Section 19.3.3.1, "Privileges For](#page-18-0) [The Replication PRIVILEGE\\_CHECKS\\_USER Account"](#page-18-0) explains what additional privileges the account needs. For example, to grant the priv\_repl user account the INSERT privilege to add rows to the cust table in db1, issue the following statement:

```
mysql> GRANT INSERT ON db1.cust TO 'priv_repl'@'%.example.com';
```

You assign the PRIVILEGE\_CHECKS\_USER account for a replication channel using a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23). If replication is running, issue STOP REPLICA (or before MySQL 8.0.22, STOP SLAVE) before the CHANGE MASTER TO statement, and START REPLICA after it. The use of rowbased binary logging is strongly recommended when PRIVILEGE\_CHECKS\_USER is set, and from MySQL 8.0.19 you can use the statement to set REQUIRE\_ROW\_FORMAT to enforce this.

When you restart the replication channel, checks on dynamic privileges are applied from that point on. However, static global privileges are not active in the applier's context until you reload the grant tables, because these privileges are not changed for a connected client. To activate static privileges, perform a flush-privileges operation. This can be done by issuing a FLUSH PRIVILEGES statement or by executing a mysqladmin flush-privileges or mysqladmin reload command.

For example, to start privilege checks on the channel channel\_1 on a running replica in MySQL 8.0.23 and later, issue the following statements:

```
mysql> STOP REPLICA FOR CHANNEL 'channel_1';
mysql> CHANGE REPLICATION SOURCE TO
 > PRIVILEGE_CHECKS_USER = 'priv_repl'@'%.example.com',
 > REQUIRE_ROW_FORMAT = 1 FOR CHANNEL 'channel_1';
mysql> FLUSH PRIVILEGES;
mysql> START REPLICA FOR CHANNEL 'channel_1';
```

Prior to MySQL 8.0.23, you can use the statements shown here:

```
mysql> STOP SLAVE FOR CHANNEL 'channel_1';
mysql> CHANGE MASTER TO
 > PRIVILEGE_CHECKS_USER = 'priv_repl'@'%.example.com',
 > REQUIRE_ROW_FORMAT = 1 FOR CHANNEL 'channel_1';
mysql> FLUSH PRIVILEGES;
mysql> START SLAVE FOR CHANNEL 'channel_1';
```

If you do not specify a channel and no other channels exist, the statement is applied to the default channel. The user name and host name for the PRIVILEGE\_CHECKS\_USER account for a channel are shown in the Performance Schema replication\_applier\_configuration table, where they are properly escaped so they can be copied directly into SQL statements to execute individual transactions.

In MySQL 8.0.31 and later, if you are using the Rewriter plugin, you should grant the PRIVILEGE\_CHECKS\_USER user account the SKIP\_QUERY\_REWRITE privilege. This prevents statements issued by this user from being rewritten. See Section 7.6.4, "The Rewriter Query Rewrite Plugin", for more information.

When REQUIRE\_ROW\_FORMAT is set for a replication channel, the replication applier does not create or drop temporary tables, and so does not set the pseudo\_thread\_id session system variable. It does not execute LOAD DATA INFILE instructions, and so does not attempt file operations to access or delete the temporary files associated with data loads (logged as a Format\_description\_log\_event). It does not execute INTVAR, RAND, and USER\_VAR events, which are used to reproduce the client's connection state for statement-based replication. (An exception is USER\_VAR events that are associated with DDL queries, which are executed.) It does not execute any statements that are logged within DML transactions. If the replication applier detects any of these types of event while attempting to queue or apply a transaction, the event is not applied, and replication stops with an error.

You can set REQUIRE\_ROW\_FORMAT for a replication channel whether or not you set a PRIVILEGE\_CHECKS\_USER account. The restrictions implemented when you set this option increase the security of the replication channel even without privilege checks. You can also specify the - require-row-format option when you use mysqlbinlog, to enforce row-based replication events in mysqlbinlog output.

**Security Context.** By default, when a replication applier thread is started with a user account specified as the PRIVILEGE\_CHECKS\_USER, the security context is created using default roles, or with all roles if activate\_all\_roles\_on\_login is set to ON.

You can use roles to supply a general privilege set to accounts that are used as PRIVILEGE\_CHECKS\_USER accounts, as in the following example. Here, instead of granting the INSERT privilege for the db1.cust table directly to a user account as in the earlier example, this privilege is granted to the role priv\_repl\_role along with the REPLICATION\_APPLIER privilege. The role is then used to grant the privilege set to two user accounts, both of which can now be used as PRIVILEGE\_CHECKS\_USER accounts:

```
mysql> SET sql_log_bin = 0;
mysql> CREATE USER 'priv_repa'@'%.example.com'
 IDENTIFIED BY 'password'
                REQUIRE SSL;
mysql> CREATE USER 'priv_repb'@'%.example.com'
 IDENTIFIED BY 'password'
                REQUIRE SSL;
mysql> CREATE ROLE 'priv_repl_role';
mysql> GRANT REPLICATION_APPLIER TO 'priv_repl_role';
mysql> GRANT INSERT ON db1.cust TO 'priv_repl_role';
mysql> GRANT 'priv_repl_role' TO
 'priv_repa'@'%.example.com',
                'priv_repb'@'%.example.com';
mysql> SET DEFAULT ROLE 'priv_repl_role' TO
 'priv_repa'@'%.example.com',
                'priv_repb'@'%.example.com';
mysql> SET sql_log_bin = 1;
```

Be aware that when the replication applier thread creates the security context, it checks the privileges for the PRIVILEGE\_CHECKS\_USER account, but does not carry out password validation, and does not carry out checks relating to account management, such as checking whether the account is locked. The security context that is created remains unchanged for the lifetime of the replication applier thread.

**Limitation.** In MySQL 8.0.18 only, if the replica mysqld is restarted immediately after issuing a RESET REPLICA statement (due to an unexpected server exit or deliberate restart), the PRIVILEGE\_CHECKS\_USER account setting, which is held in the mysql.slave\_relay\_log\_info table, is lost and must be respecified. When you use privilege checks in that release, always verify that they are in place after a restart, and respecify them if required. From MySQL 8.0.19, the PRIVILEGE\_CHECKS\_USER account setting is preserved in this situation, so it is retrieved from the table and reapplied to the channel.

# <span id="page-18-0"></span>**19.3.3.1 Privileges For The Replication PRIVILEGE\_CHECKS\_USER Account**

The user account that is specified using the CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement as the PRIVILEGE\_CHECKS\_USER account for a replication channel must have the REPLICATION\_APPLIER privilege, otherwise the replication applier thread does not start. As

explained in [Section 19.3.3, "Replication Privilege Checks",](#page-15-0) the account requires further privileges that are sufficient to apply all the expected transactions expected on the replication channel. These privileges are checked only when relevant transactions are executed.

The use of row-based binary logging (binlog\_format=ROW) is strongly recommended for replication channels that are secured using a PRIVILEGE\_CHECKS\_USER account. With statement-based binary logging, some administrator-level privileges might be required for the PRIVILEGE\_CHECKS\_USER account to execute transactions successfully. From MySQL 8.0.19, the REQUIRE\_ROW\_FORMAT setting can be applied to secured channels, which restricts the channel from executing events that would require these privileges.

The REPLICATION\_APPLIER privilege explicitly or implicitly allows the PRIVILEGE\_CHECKS\_USER account to carry out the following operations that a replication thread needs to perform:

- Setting the value of the system variables gtid\_next, original\_commit\_timestamp, original\_server\_version, immediate\_server\_version, and pseudo\_replica\_mode or pseudo\_slave\_mode, to apply appropriate metadata and behaviors when executing transactions.
- Executing internal-use BINLOG statements to apply mysqlbinlog output, provided that the account also has permission for the tables and operations in those statements.
- Updating the system tables mysql.gtid\_executed, mysql.slave\_relay\_log\_info, mysql.slave\_worker\_info, and mysql.slave\_master\_info, to update replication metadata. (If events access these tables explicitly for other purposes, you must grant the appropriate privileges on the tables.)
- Applying a binary log Table\_map\_log\_event, which provides table metadata but does not make any database changes.

If the REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option of the CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement is set to the default of STREAM, the PRIVILEGE\_CHECKS\_USER account needs privileges sufficient to set restricted session variables, so that it can change the value of the sql\_require\_primary\_key system variable for the duration of a session to match the setting replicated from the source. The SESSION\_VARIABLES\_ADMIN privilege gives the account this capability. This privilege also allows the account to apply mysqlbinlog output that was created using the --disable-log-bin option. If you set REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK to either ON or OFF, the replica always uses that value for the sql\_require\_primary\_key system variable in replication operations, and so does not need these session administration level privileges.

If table encryption is in use, the table\_encryption\_privilege\_check system variable is set to ON, and the encryption setting for the tablespace involved in any event differs from the applying server's default encryption setting (specified by the default\_table\_encryption system variable), the PRIVILEGE\_CHECKS\_USER account needs the TABLE\_ENCRYPTION\_ADMIN privilege in order to override the default encryption setting. It is strongly recommended that you do not grant this privilege. Instead, ensure that the default encryption setting on a replica matches the encryption status of the tablespaces that it replicates, and that replication group members have the same default encryption setting, so that the privilege is not needed.

In order to execute specific replicated transactions from the relay log, or transactions from mysqlbinlog output as required, the PRIVILEGE\_CHECKS\_USER account must have the following privileges:

- For a row insertion logged in row format (which are logged as a Write\_rows\_log\_event), the INSERT privilege on the relevant table.
- For a row update logged in row format (which are logged as an Update\_rows\_log\_event), the UPDATE privilege on the relevant table.
- For a row deletion logged in row format (which are logged as a Delete\_rows\_log\_event), the DELETE privilege on the relevant table.

If statement-based binary logging is in use (which is not recommended with a PRIVILEGE\_CHECKS\_USER account), for a transaction control statement such as BEGIN or COMMIT or DML logged in statement format (which are logged as a Query\_log\_event), the PRIVILEGE\_CHECKS\_USER account needs privileges to execute the statement contained in the event.

If LOAD DATA operations need to be carried out on the replication channel, use row-based binary logging (binlog\_format=ROW). With this logging format, the FILE privilege is not needed to execute the event, so do not give the PRIVILEGE\_CHECKS\_USER account this privilege. The use of rowbased binary logging is strongly recommended with replication channels that are secured using a PRIVILEGE\_CHECKS\_USER account. If REQUIRE\_ROW\_FORMAT is set for the channel, row-based binary logging is required. The Format\_description\_log\_event, which deletes any temporary files created by LOAD DATA events, is processed without privilege checks. For more information, see [Section 19.5.1.19, "Replication and LOAD DATA"](#page-61-0).

If the init\_replica or init\_slave system variable is set to specify one or more SQL statements to be executed when the replication SQL thread starts, the PRIVILEGE\_CHECKS\_USER account must have the privileges needed to execute these statements.

It is recommended that you never give any ACL privileges to the PRIVILEGE\_CHECKS\_USER account, including CREATE USER, CREATE ROLE, DROP ROLE, and GRANT OPTION, and do not permit the account to update the mysql.user table. With these privileges, the account could be used to create or modify user accounts on the server. To avoid ACL statements issued on the source server being replicated to the secured channel for execution (where they fail in the absence of these privileges), you can issue SET sql\_log\_bin = 0 before all ACL statements and SET sql\_log\_bin = 1 after them, to omit the statements from the source's binary log. Alternatively, you can set a dedicated current database before executing all ACL statements, and use a replication filter (--binlog-ignore-db) to filter out this database on the replica.

# <span id="page-20-0"></span>**19.3.3.2 Privilege Checks For Group Replication Channels**

From MySQL 8.0.19, as well as securing asynchronous and semi-synchronous replication, you may choose to use a PRIVILEGE\_CHECKS\_USER account to secure the two replication applier threads used by Group Replication. The group\_replication\_applier thread on each group member is used for applying the group's transactions, and the group\_replication\_recovery thread on each group member is used for state transfer from the binary log as part of distributed recovery when the member joins or rejoins the group.

To secure one of these threads, stop Group Replication, then issue the CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) with the PRIVILEGE\_CHECKS\_USER option, specifying group\_replication\_applier or group\_replication\_recovery as the channel name. For example:

```
mysql> STOP GROUP_REPLICATION;
mysql> CHANGE MASTER TO PRIVILEGE_CHECKS_USER = 'gr_repl'@'%.example.com' 
 FOR CHANNEL 'group_replication_recovery';
mysql> FLUSH PRIVILEGES;
mysql> START GROUP_REPLICATION;
Or from MySQL 8.0.23:
mysql> STOP GROUP_REPLICATION;
mysql> CHANGE REPLICATION SOURCE TO PRIVILEGE_CHECKS_USER = 'gr_repl'@'%.example.com' 
 FOR CHANNEL 'group_replication_recovery';
mysql> FLUSH PRIVILEGES;
mysql> START GROUP_REPLICATION;
```

For Group Replication channels, the REQUIRE\_ROW\_FORMAT setting is automatically enabled when the channel is created, and cannot be disabled, so you do not need to specify this.

![](_page_20_Picture_10.jpeg)

#### **Important**

In MySQL 8.0.19, ensure that you do not issue the CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement with the PRIVILEGE\_CHECKS\_USER option while Group Replication is running. This action causes the relay log files for the channel to be purged, which might cause the loss of transactions that have been received and queued in the relay log, but not yet applied.

Group Replication requires every table that is to be replicated by the group to have a defined primary key, or primary key equivalent where the equivalent is a non-null unique key. Rather than using the checks carried out by the sql\_require\_primary\_key system variable, Group Replication has its own built-in set of checks for primary keys or primary key equivalents. You may set the REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option of the CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement to ON for a Group Replication channel. However, be aware that you might find some transactions that are permitted under Group Replication's built-in checks are not permitted under the checks carried out when you set sql\_require\_primary\_key = ON or REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK = ON. For this reason, new and upgraded Group Replication channels from MySQL 8.0.20 (when the option was introduced) have REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK set to the default of STREAM, rather than to ON.

If a remote cloning operation is used for distributed recovery in Group Replication (see [Section 20.5.4.2, "Cloning for Distributed Recovery"\)](#page-138-0), from MySQL 8.0.19, the PRIVILEGE\_CHECKS\_USER account and related settings from the donor are cloned to the joining member. If the joining member is set to start Group Replication on boot, it automatically uses the account for privilege checks on the appropriate replication channels.

In MySQL 8.0.18, due to a number of limitations, it is recommended that you do not use a PRIVILEGE\_CHECKS\_USER account with Group Replication channels.