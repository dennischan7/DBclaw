---
source: MySQL 8.4 Reference
title: 00_Overview
---

![](_page_149_Picture_11.jpeg)

## **Note**

MySQL Enterprise Firewall is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

MySQL Enterprise Edition includes MySQL Enterprise Firewall, an application-level firewall that enables database administrators to permit or deny SQL statement execution based on matching against lists of accepted statement patterns. This helps harden MySQL Server against attacks such as SQL injection or attempts to exploit applications by using them outside of their legitimate query workload characteristics.

Each MySQL account registered with the firewall has its own statement allowlist, enabling protection to be tailored per account. For a given account, the firewall can operate in recording, protecting, or detecting mode, for training in the accepted statement patterns, active protection against unacceptable statements, or passive detection of unacceptable statements. The diagram illustrates how the firewall processes incoming statements in each mode.

![](_page_150_Figure_1.jpeg)

**Figure 8.1 MySQL Enterprise Firewall Operation**

The following sections describe the elements of MySQL Enterprise Firewall, discuss how to install and use it, and provide reference information for its elements.

## <span id="page-150-0"></span>**8.4.7.1 Elements of MySQL Enterprise Firewall**

MySQL Enterprise Firewall is based on a plugin library that includes these elements:

- A server-side plugin named MYSQL\_FIREWALL examines SQL statements before they execute and, based on the registered firewall profiles, renders a decision whether to execute or reject each statement.
- The MYSQL\_FIREWALL plugin, along with server-side plugins named MYSQL\_FIREWALL\_USERS and MYSQL\_FIREWALL\_WHITELIST implement Performance Schema and INFORMATION\_SCHEMA tables that provide views into the registered profiles.
- Profiles are cached in memory for better performance. Tables in the firewall database provide backing storage of firewall data for persistence of profiles across server restarts. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL Enterprise](#page-151-0) [Firewall](#page-151-0)).

- Stored procedures perform tasks such as registering firewall profiles, establishing their operational mode, and managing transfer of firewall data between the cache and persistent storage.
- Administrative functions provide an API for lower-level tasks such as synchronizing the cache with persistent storage.
- System variables enable firewall configuration and status variables provide runtime operational information.
- The FIREWALL\_ADMIN and FIREWALL\_USER privileges enable users to administer firewall rules for any user, and their own firewall rules, respectively.
- The FIREWALL\_EXEMPT privilege exempts a user from firewall restrictions. This is useful, for example, for any database administrator who configures the firewall, to avoid the possibility of a misconfiguration causing even the administrator to be locked out and unable to execute statements.

## <span id="page-151-1"></span>**8.4.7.2 Installing or Uninstalling MySQL Enterprise Firewall**

MySQL Enterprise Firewall installation is a one-time operation that installs the elements described in [Section 8.4.7.1, "Elements of MySQL Enterprise Firewall".](#page-150-0) Installation can be performed using a graphical interface or manually:

- On Windows, MySQL Configurator includes an option to enable MySQL Enterprise Firewall for you.
- MySQL Workbench 6.3.4 or higher can install MySQL Enterprise Firewall, enable or disable an installed firewall, or uninstall the firewall.
- Manual MySQL Enterprise Firewall installation involves running a script located in the share directory of your MySQL installation.

![](_page_151_Picture_11.jpeg)

## **Important**

Read this entire section before following its instructions. Parts of the procedure differ depending on your environment.

![](_page_151_Picture_14.jpeg)

## **Note**

If installed, MySQL Enterprise Firewall involves some minimal overhead even when disabled. To avoid this overhead, do not install the firewall unless you plan to use it.

For usage instructions, see [Section 8.4.7.3, "Using MySQL Enterprise Firewall"](#page-153-0). For reference information, see [Section 8.4.7.4, "MySQL Enterprise Firewall Reference".](#page-167-0)

- [Installing MySQL Enterprise Firewall](#page-151-0)
- [Uninstalling MySQL Enterprise Firewall](#page-152-0)

## <span id="page-151-0"></span>**Installing MySQL Enterprise Firewall**

If MySQL Enterprise Firewall is already installed from an older version of MySQL, uninstall it using the instructions given later in this section and then restart your server before installing the current version. In this case, it is also necessary to register your configuration again.

On Windows, you can use Section 2.3.2, "Configuration: Using MySQL Configurator" to install MySQL Enterprise Firewall by checking the **Enable MySQL Enterprise Firewall** check box from the Type and Networking tab. (**Open Firewall port for network access** has a different purpose. It refers to Windows Firewall and controls whether Windows blocks the TCP/IP port on which the MySQL server listens for client connections.)

To install MySQL Enterprise Firewall using MySQL Workbench, see [MySQL Enterprise Firewall](https://dev.mysql.com/doc/workbench/en/wb-mysql-firewall.md) [Interface.](https://dev.mysql.com/doc/workbench/en/wb-mysql-firewall.md)

To install MySQL Enterprise Firewall manually, look in the share directory of your MySQL installation and choose the script that is appropriate for your platform. The available scripts differ in the file name used to refer to the script:

- win\_install\_firewall.sql
- linux\_install\_firewall.sql

The installation script creates stored procedures and tables in the firewall database you specify when you run the script. The mysql system database is the traditional storage option, however, it is preferred that you create and use a custom schema for this purpose.

To use the mysql system database, run the script as follows from the command line. The example here uses the Linux installation script. Make the appropriate substitutions for your system.

```
$> mysql -u root -p -D mysql < linux_install_firewall.sql
Enter password: (enter root password here)
```

To create and use a custom schema with the script, do the following:

1. Start the server with the --loose-mysql-firewall-database=database-name option. Insert the name of the custom schema to be used as the firewall database.

By prefixing the option with --loose, the program does not emit an error and exit, but instead issues only a warning.

2. Invoke the MySQL client program and create the custom schema on the server.

```
mysql> CREATE DATABASE IF NOT EXISTS database-name;
```

3. Run the script, naming the custom schema as the database for MySQL Enterprise Firewall.

```
$> mysql -u root -p -D database-name < linux_install_firewall.sql
Enter password: (enter root password here)
```

Installing MySQL Enterprise Firewall either using a graphical interface or manually should enable the firewall. To verify that, connect to the server and execute this statement:

```
mysql> SHOW GLOBAL VARIABLES LIKE 'mysql_firewall_mode';
+---------------------+-------+
| Variable_name | Value |
+---------------------+-------+
| mysql_firewall_mode | ON |
+---------------------+-------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

![](_page_152_Picture_17.jpeg)

## **Note**

To use MySQL Enterprise Firewall in the context of source/replica replication, Group Replication, or InnoDB Cluster, you must prepare the replica nodes prior to running the installation script on the source node. This is necessary because the INSTALL PLUGIN statements in the script are not replicated.

- 1. On each replica node, extract the INSTALL PLUGIN statements from the installation script and execute them manually.
- 2. On the source node, run the installation script as described previously.

## <span id="page-152-0"></span>**Uninstalling MySQL Enterprise Firewall**

MySQL Enterprise Firewall can be uninstalled using MySQL Workbench or manually.

To uninstall MySQL Enterprise Firewall using MySQL Workbench 6.3.4 or higher, see [MySQL](https://dev.mysql.com/doc/workbench/en/wb-mysql-firewall.md) [Enterprise Firewall Interface](https://dev.mysql.com/doc/workbench/en/wb-mysql-firewall.md), in Chapter 33, MySQL Workbench.

To uninstall MySQL Enterprise Firewall at the command line, run the uninstall script located in the share directory of your MySQL installation. The example here specifies the system database, mysql.

```
$> mysql -u root -p -D mysql < uninstall_firewall.sql
Enter password: (enter root password here)
```

If you created a custom schema when you installed MySQL Enterprise Firewall, make the appropriate substitution for your system.

```
$> mysql -u root -p -D database-name < uninstall_firewall.sql
Enter password: (enter root password here)
```

This script removes the plugins, tables, functions, and stored procedures for MySQL Enterprise Firewall.

## <span id="page-153-0"></span>**8.4.7.3 Using MySQL Enterprise Firewall**

Before using MySQL Enterprise Firewall, install it according to the instructions provided in [Section 8.4.7.2, "Installing or Uninstalling MySQL Enterprise Firewall"](#page-151-1).

This section describes how to configure MySQL Enterprise Firewall using SQL statements. Alternatively, MySQL Workbench 6.3.4 or higher provides a graphical interface for firewall control. See [MySQL Enterprise Firewall Interface.](https://dev.mysql.com/doc/workbench/en/wb-mysql-firewall.md)

- [Enabling or Disabling the Firewall](#page-153-1)
- [Scheduling Firewall Cache Reloads](#page-153-2)
- [Assigning Firewall Privileges](#page-154-0)
- [Firewall Concepts](#page-155-0)
- [Registering Firewall Group Profiles](#page-158-0)
- [Registering Firewall Account Profiles](#page-163-0)
- [Monitoring the Firewall](#page-166-0)
- [Migrating Account Profiles to Group Profiles](#page-166-1)

## <span id="page-153-1"></span>**Enabling or Disabling the Firewall**

To enable or disable the firewall, set the [mysql\\_firewall\\_mode](#page-176-0) system variable. By default, this variable is enabled when the firewall is installed. To control the initial firewall state explicitly, you can set the variable at server startup. For example, to enable the firewall in an option file, use these lines:

```
[mysqld]
mysql_firewall_mode=ON
```

After modifying my.cnf, restart the server to cause the new setting to take effect.

Alternatively, to set and persist the firewall setting at runtime:

```
SET PERSIST mysql_firewall_mode = OFF;
SET PERSIST mysql_firewall_mode = ON;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change a value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

## <span id="page-153-2"></span>**Scheduling Firewall Cache Reloads**

Each time the MYSQL\_FIREWALL server-side plugin initializes, it loads data from these tables to its internal cache:

- firewall\_whitelist
- firewall\_group\_allowlist
- firewall\_users
- firewall\_groups
- firewall\_membership

Without restarting the server or reinstalling the server-side plugin, modification of data outside of the plugin is not reflected internally. The [mysql\\_firewall\\_reload\\_interval\\_seconds](#page-177-0) system variable makes it possible to force memory cache reloads from tables at specified intervals. By default, the periodic interval value is set to zero, which disables reloads.

To schedule regular cache reloads, first ensure that the scheduler component is installed and enabled (see Section 7.5.5, "Scheduler Component"). To check the status of the component:

```
SHOW VARIABLES LIKE 'component_scheduler%';
+-----------------------------+-------+
| Variable_name | Value |
+-----------------------------+-------|
| component_scheduler.enabled | On |
+-----------------------------+-------+
```

With the firewall installed, set the [mysql\\_firewall\\_reload\\_interval\\_seconds](#page-177-0) global system variable at server startup to a number between 60 and the INT\_MAX macro value of the platform hosting the server. Values between zero and 60 (1 through 59) reset to 60. For example:

```
$> mysqld [server-options] --mysql-firewall-reload-interval-seconds=40
...
2023-08-31T17:46:35.043468Z 0 [Warning] [MY-015031] [Server] Plugin MYSQL_FIREWALL 
reported: 'Invalid reload interval specified: 40. Valid values are 0 (off) or 
greater than or equal to 60. Adjusting to 60.'
...
```

Alternatively, to set and persist the firewall setting at startup, precede the read-only variable name by the PERSIST\_ONLY keyword or the @@PERSIST\_ONLY. qualifier:

```
SET PERSIST_ONLY mysql_firewall_reload_interval_seconds = 120;
SET @@PERSIST_ONLY.mysql_firewall_reload_interval_seconds = 120;
```

After modifying the variable, restart the server to cause the new setting to take effect.

## <span id="page-154-0"></span>**Assigning Firewall Privileges**

With the firewall installed, grant the appropriate privileges to the MySQL account or accounts to be used for administering it. The privileges depend on which firewall operations an account should be permitted to perform:

- Grant the FIREWALL\_EXEMPT privilege to any account that should be exempt from firewall restrictions. This is useful, for example, for a database administrator who configures the firewall, to avoid the possibility of a misconfiguration causing even the administrator to be locked out and unable to execute statements.
- Grant the FIREWALL\_ADMIN privilege to any account that should have full administrative firewall access. (Some administrative firewall functions can be invoked by accounts that have FIREWALL\_ADMIN or the deprecated SUPER privilege, as indicated in the individual function descriptions.)
- Grant the FIREWALL\_USER privilege to any account that should have administrative access only for its own firewall rules.
- Grant the EXECUTE privilege for the firewall stored procedures in the firewall database. These may invoke administrative functions, so stored procedure access also requires the privileges indicated

earlier that are needed for those functions. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL Enterprise Firewall](#page-151-0)).

![](_page_155_Picture_2.jpeg)

#### **Note**

The FIREWALL\_EXEMPT, FIREWALL\_ADMIN, and FIREWALL\_USER privileges can be granted only while the firewall is installed because the MYSQL\_FIREWALL plugin defines those privileges.

## <span id="page-155-0"></span>**Firewall Concepts**

The MySQL server permits clients to connect and receives from them SQL statements to be executed. If the firewall is enabled, the server passes to it each incoming statement that does not immediately fail with a syntax error. Based on whether the firewall accepts the statement, the server executes it or returns an error to the client. This section describes how the firewall accomplishes the task of accepting or rejecting statements.

- [Firewall Profiles](#page-155-1)
- [Firewall Statement Matching](#page-156-0)
- [Profile Operational Modes](#page-157-0)
- [Firewall Statement Handling When Multiple Profiles Apply](#page-157-1)

#### <span id="page-155-1"></span>**Firewall Profiles**

The firewall uses a registry of profiles that determine whether to permit statement execution. Profiles have these attributes:

- An allowlist. The allowlist is the set of rules that defines which statements are acceptable to the profile.
- A current operational mode. The mode enables the profile to be used in different ways. For example: the profile can be placed in training mode to establish the allowlist; the allowlist can be used for restricting statement execution or intrusion detection; the profile can be disabled entirely.
- A scope of applicability. The scope indicates which client connections the profile applies to:
  - The firewall supports account-based profiles such that each profile matches a particular client account (client user name and host name combination). For example, you can register one account profile for which the allowlist applies to connections originating from admin@localhost and another account profile for which the allowlist applies to connections originating from myapp@apphost.example.com.
  - The firewall supports group profiles that can have multiple accounts as members, with the profile allowlist applying equally to all members. Group profiles enable easier administration and greater flexibility for deployments that require applying a given set of allowlist rules to multiple accounts.

Initially, no profiles exist, so by default, the firewall accepts all statements and has no effect on which statements MySQL accounts can execute. To apply firewall protective capabilities, explicit action is required:

- Register one or more profiles with the firewall.
- Train the firewall by establishing the allowlist for each profile; that is, the types of statements the profile permits clients to execute.
- Place the trained profiles in protecting mode to harden MySQL against unauthorized statement execution:
  - MySQL associates each client session with a specific user name and host name combination. This combination is the session account.

• For each client connection, the firewall uses the session account to determine which profiles apply to handling incoming statements from the client.

The firewall accepts only statements permitted by the applicable profile allowlists.

Most firewall principles apply identically to group profiles and account profiles. The two types of profiles differ in these respects:

- An account profile allowlist applies only to a single account. A group profile allowlist applies when the session account matches any account that is a member of the group.
- To apply an allowlist to multiple accounts using account profiles, it is necessary to register one profile per account and duplicate the allowlist across each profile. This entails training each account profile individually because each one must be trained using the single account to which it applies.

A group profile allowlist applies to multiple accounts, with no need to duplicate it for each account. A group profile can be trained using any or all of the group member accounts, or training can be limited to any single member. Either way, the allowlist applies to all members.

• Account profile names are based on specific user name and host name combinations that depend on which clients connect to the MySQL server. Group profile names are chosen by the firewall administrator with no constraints other than that their length must be from 1 to 288 characters.

![](_page_156_Picture_8.jpeg)

#### **Note**

Due to the advantages of group profiles over account profiles, and because a group profile with a single member account is logically equivalent to an account profile for that account, it is recommended that all new firewall profiles be created as group profiles. Account profiles are deprecated, and subject to removal in a future MySQL version. For assistance converting existing account profiles, see [Migrating Account Profiles to Group Profiles.](#page-166-1)

The profile-based protection afforded by the firewall enables implementation of strategies such as these:

- If an application has unique protection requirements, configure it to use an account not used for any other purpose and set up a group profile or account profile for that account.
- If related applications share protection requirements, associate each application with its own account, then add these application accounts as members of the same group profile. Alternatively, configure all the applications to use the same account and associate them with an account profile for that account.

#### <span id="page-156-0"></span>**Firewall Statement Matching**

Statement matching performed by the firewall does not use SQL statements as received from clients. Instead, the server converts incoming statements to normalized digest form and firewall operation uses these digests. The benefit of statement normalization is that it enables similar statements to be grouped and recognized using a single pattern. For example, these statements are distinct from each other:

```
SELECT first_name, last_name FROM customer WHERE customer_id = 1;
select first_name, last_name from customer where customer_id = 99;
SELECT first_name, last_name FROM customer WHERE customer_id = 143;
```

But all of them have the same normalized digest form:

```
SELECT `first_name` , `last_name` FROM `customer` WHERE `customer_id` = ?
```

By using normalization, firewall allowlists can store digests that each match many different statements received from clients. For more information about normalization and digests, see Section 29.10, "Performance Schema Statement Digests and Sampling".

![](_page_157_Picture_1.jpeg)

### **Warning**

Setting the max\_digest\_length system variable to zero disables digest production, which also disables server functionality that requires digests, such as MySQL Enterprise Firewall.

#### <span id="page-157-0"></span>**Profile Operational Modes**

Each profile registered with the firewall has its own operational mode, chosen from these values:

- OFF: This mode disables the profile. The firewall considers it inactive and ignores it.
- RECORDING: This is the firewall training mode. Incoming statements received from a client that matches the profile are considered acceptable for the profile and become part of its "fingerprint." The firewall records the normalized digest form of each statement to learn the acceptable statement patterns for the profile. Each pattern is a rule, and the union of the rules is the profile allowlist.

A difference between group and account profiles is that statement recording for a group profile can be limited to statements received from a single group member (the training member).

- PROTECTING: In this mode, the profile allows or prevents statement execution. The firewall matches incoming statements against the profile allowlist, accepting only statements that match and rejecting those that do not. After training a profile in RECORDING mode, switch it to PROTECTING mode to harden MySQL against access by statements that deviate from the allowlist. If the [mysql\\_firewall\\_trace](#page-177-1) system variable is enabled, the firewall also writes rejected statements to the error log.
- DETECTING: This mode detects but not does not block intrusions (statements that are suspicious because they match nothing in the profile allowlist). In DETECTING mode, the firewall writes suspicious statements to the error log but accepts them without denying access.

When a profile is assigned any of the preceding mode values, the firewall stores the mode in the profile. Firewall mode-setting operations also permit a mode value of RESET, but this value is not stored: setting a profile to RESET mode causes the firewall to delete all rules for the profile and set its mode to OFF.

![](_page_157_Picture_12.jpeg)

## **Note**

Messages written to the error log in DETECTING mode or because [mysql\\_firewall\\_trace](#page-177-1) is enabled are written as Notes, which are information messages. To ensure that such messages appear in the error log and are not discarded, make sure that error-logging verbosity is sufficient to include information messages. For example, if you are using priority-based log filtering, as described in Section 7.4.2.5, "Priority-Based Error Log Filtering (log\_filter\_internal)", set the log\_error\_verbosity system variable to a value of 3.

#### <span id="page-157-1"></span>**Firewall Statement Handling When Multiple Profiles Apply**

For simplicity, later sections that describe how to set up profiles take the perspective that the firewall matches incoming statements from a client against only a single profile, either a group profile or account profile. But firewall operation can be more complex:

- A group profile can include multiple accounts as members.
- An account can be a member of multiple group profiles.
- Multiple profiles can match a given client.

The following description covers the general case of how the firewall operates, when potentially multiple profiles apply to incoming statements.

As previously mentioned, MySQL associates each client session with a specific user name and host name combination known as the session account. The firewall matches the session account against registered profiles to determine which profiles apply to handling incoming statements from the session:

- The firewall ignores inactive profiles (profiles with a mode of OFF).
- The session account matches every active group profile that includes a member having the same user and host. There can be more than one such group profile.
- The session account matches an active account profile having the same user and host, if there is one. There is at most one such account profile.

In other words, the session account can match 0 or more active group profiles, and 0 or 1 active account profiles. This means that 0, 1, or multiple firewall profiles are applicable to a given session, for which the firewall handles each incoming statement as follows:

- If there is no applicable profile, the firewall imposes no restrictions and accepts the statement.
- If there are applicable profiles, their modes determine statement handling:
  - The firewall records the statement in the allowlist of each applicable profile that is in RECORDING mode.
  - The firewall writes the statement to the error log for each applicable profile in DETECTING mode for which the statement is suspicious (does not match the profile allowlist).
  - The firewall accepts the statement if at least one applicable profile is in RECORDING or DETECTING mode (those modes accept all statements), or if the statement matches the allowlist of at least one applicable profile in PROTECTING mode. Otherwise, the firewall rejects the statement (and writes it to the error log if the [mysql\\_firewall\\_trace](#page-177-1) system variable is enabled).

With that description in mind, the next sections revert to the simplicity of the situations when a single group profile or a single account profile apply, and cover how to set up each type of profile.

## <span id="page-158-0"></span>**Registering Firewall Group Profiles**

MySQL Enterprise Firewall supports registration of group profiles. A group profile can have multiple accounts as its members. To use a firewall group profile to protect MySQL against incoming statements from a given account, follow these steps:

- 1. Register the group profile and put it in RECORDING mode.
- 2. Add a member account to the group profile.
- 3. Connect to the MySQL server using the member account and execute statements to be learned. This trains the group profile and establishes the rules that form the profile allowlist.
- 4. Add to the group profile any other accounts that are to be group members.
- 5. Switch the group profile to PROTECTING mode. When a client connects to the server using any account that is a member of the group profile, the profile allowlist restricts statement execution.
- 6. Should additional training be necessary, switch the group profile to RECORDING mode again, update its allowlist with new statement patterns, then switch it back to PROTECTING mode.

Observe these guidelines for firewall-related account references:

• Take note of the context in which account references occur. To name an account for firewall operations, specify it as a single quoted string ('user\_name@host\_name'). This differs from the usual MySQL convention for statements such as CREATE USER and GRANT, for which you quote the user and host parts of an account name separately ('user\_name'@'host\_name').

The requirement for naming accounts as a single quoted string for firewall operations means that you cannot use accounts that have embedded @ characters in the user name.

- The firewall assesses statements against accounts represented by actual user and host names as authenticated by the server. When registering accounts in profiles, do not use wildcard characters or netmasks:
  - Suppose that an account named me@%.example.org exists and a client uses it to connect to the server from the host abc.example.org.
  - The account name contains a % wildcard character, but the server authenticates the client as having a user name of me and host name of abc.example.com, and that is what the firewall sees.
  - Consequently, the account name to use for firewall operations is me@abc.example.org rather than me@%.example.org.

The following procedure shows how to register a group profile with the firewall, train the firewall to know the acceptable statements for that profile (its allowlist), use the profile to protect MySQL against execution of unacceptable statements, and add and remove group members. The example uses a group profile name of fwgrp. The example profile is presumed for use by clients of an application that accesses tables in the sakila database (available at [https://dev.mysql.com/doc/index-other.html\)](https://dev.mysql.com/doc/index-other.md).

Use an administrative MySQL account to perform the steps in this procedure, except those steps designated for execution by member accounts of the firewall group profile. For statements executed by member accounts, the default database should be sakila. (You can use a different database by adjusting the instructions accordingly.)

1. If necessary, create the accounts that are to be members of the fwgrp group profile and grant them appropriate access privileges. Statements for one member are shown here (choose an appropriate password):

```
CREATE USER 'member1'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON sakila.* TO 'member1'@'localhost';
```

2. Use the sp\_set\_firewall\_group\_mode() stored procedure to register the group profile with the firewall and place the profile in RECORDING (training) mode:

```
CALL mysql.sp_set_firewall_group_mode('fwgrp', 'RECORDING');
```

![](_page_159_Picture_11.jpeg)

#### **Note**

If you have installed MySQL Enterprise Firewall in a custom schema, then make appropriate substitution for your system. For example, if the firewall is installed in the fwdb schema, then execute the stored procedures like this:

```
CALL fwdb.sp_set_firewall_group_mode('fwgrp', 'RECORDING');
```

3. Use the sp\_firewall\_group\_enlist() stored procedure to add an initial member account for use in training the group profile allowlist:

```
CALL mysql.sp_firewall_group_enlist('fwgrp', 'member1@localhost');
```

4. To train the group profile using the initial member account, connect to the server as member1 from the server host so that the firewall sees a session account of member1@localhost. Then execute some statements to be considered legitimate for the profile. For example:

```
SELECT title, release_year FROM film WHERE film_id = 1;
UPDATE actor SET last_update = NOW() WHERE actor_id = 1;
SELECT store_id, COUNT(*) FROM inventory GROUP BY store_id;
```

The firewall receives the statements from the member1@localhost account. Because that account is a member of the fwgrp profile, which is in RECORDING mode, the firewall interprets the statements as applicable to fwgrp and records the normalized digest form of the statements as rules in the fwgrp allowlist. Those rules then apply to all accounts that are members of fwgrp.

![](_page_160_Picture_1.jpeg)

### **Note**

Until the fwgrp group profile receives statements in RECORDING mode, its allowlist is empty, which is equivalent to "deny all." No statement can match an empty allowlist, which has these implications:

- The group profile cannot be switched to PROTECTING mode. It would reject every statement, effectively prohibiting the accounts that are group members from executing any statement.
- The group profile can be switched to DETECTING mode. In this case, the profile accepts every statement but logs it as suspicious.
- 5. At this point, the group profile information is cached, including its name, membership, and allowlist. To see this information, query the Performance Schema firewall tables:

```
mysql> SELECT MODE FROM performance_schema.firewall_groups
 WHERE NAME = 'fwgrp';
+-----------+
| MODE |
+-----------+
| RECORDING |
+-----------+
mysql> SELECT * FROM performance_schema.firewall_membership
 WHERE GROUP_ID = 'fwgrp' ORDER BY MEMBER_ID;
+----------+-------------------+
| GROUP_ID | MEMBER_ID |
+----------+-------------------+
| fwgrp | member1@localhost |
+----------+-------------------+
mysql> SELECT RULE FROM performance_schema.firewall_group_allowlist
 WHERE NAME = 'fwgrp';
+----------------------------------------------------------------------+
| RULE |
+----------------------------------------------------------------------+
| SELECT @@`version_comment` LIMIT ? |
| UPDATE `actor` SET `last_update` = NOW ( ) WHERE `actor_id` = ? |
| SELECT `title` , `release_year` FROM `film` WHERE `film_id` = ? |
| SELECT `store_id` , COUNT ( * ) FROM `inventory` GROUP BY `store_id` |
+----------------------------------------------------------------------+
```

![](_page_160_Picture_8.jpeg)

#### **Note**

The @@version\_comment rule comes from a statement sent automatically by the mysql client when you connect to the server.

![](_page_160_Picture_11.jpeg)

#### **Important**

Train the firewall under conditions matching application use. For example, to determine server characteristics and capabilities, a given MySQL connector might send statements to the server at the beginning of each session. If an application normally is used through that connector, train the firewall using the connector, too. That enables those initial statements to become part of the allowlist for the group profile associated with the application.

6. Invoke sp\_set\_firewall\_group\_mode() again to switch the group profile to PROTECTING mode:

CALL mysql.sp\_set\_firewall\_group\_mode('fwgrp', 'PROTECTING');

![](_page_160_Picture_16.jpeg)

## **Important**

Switching the group profile out of RECORDING mode synchronizes its cached data to the firewall database tables that provide persistent underlying storage. If you do not switch the mode for a profile that is being recorded, the cached data is not written to persistent storage and is lost when the server is restarted. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL Enterprise](#page-151-0) [Firewall\)](#page-151-0).

7. Add to the group profile any other accounts that should be members:

```
CALL mysql.sp_firewall_group_enlist('fwgrp', 'member2@localhost');
CALL mysql.sp_firewall_group_enlist('fwgrp', 'member3@localhost');
CALL mysql.sp_firewall_group_enlist('fwgrp', 'member4@localhost');
```

The profile allowlist trained using the member1@localhost account now also applies to the additional accounts.

8. To verify the updated group membership, query the firewall\_membership table again:

```
mysql> SELECT * FROM performance_schema.firewall_membership
 WHERE GROUP_ID = 'fwgrp' ORDER BY MEMBER_ID;
+----------+-------------------+
| GROUP_ID | MEMBER_ID |
+----------+-------------------+
| fwgrp | member1@localhost |
| fwgrp | member2@localhost |
| fwgrp | member3@localhost |
| fwgrp | member4@localhost |
+----------+-------------------+
```

- 9. Test the group profile against the firewall by using any account in the group to execute some acceptable and unacceptable statements. The firewall matches each statement from the account against the profile allowlist and accepts or rejects it:
  - This statement is not identical to a training statement but produces the same normalized statement as one of them, so the firewall accepts it:

```
mysql> SELECT title, release_year FROM film WHERE film_id = 98;
+-------------------+--------------+
| title | release_year |
+-------------------+--------------+
| BRIGHT ENCOUNTERS | 2006 |
+-------------------+--------------+
```

• These statements match nothing in the allowlist, so the firewall rejects each with an error:

```
mysql> SELECT title, release_year FROM film WHERE film_id = 98 OR TRUE;
ERROR 1045 (28000): Statement was blocked by Firewall
mysql> SHOW TABLES LIKE 'customer%';
ERROR 1045 (28000): Statement was blocked by Firewall
mysql> TRUNCATE TABLE mysql.slow_log;
ERROR 1045 (28000): Statement was blocked by Firewall
```

• If the [mysql\\_firewall\\_trace](#page-177-1) system variable is enabled, the firewall also writes rejected statements to the error log. For example:

```
[Note] Plugin MYSQL_FIREWALL reported:
'ACCESS DENIED for 'member1@localhost'. Reason: No match in allowlist.
Statement: TRUNCATE TABLE `mysql` . `slow_log`'
```

These log messages may be helpful in identifying the source of attacks, should that be necessary.

10. Should members need to be removed from the group profile, use the sp\_firewall\_group\_delist() stored procedure rather than sp\_firewall\_group\_enlist():

```
CALL mysql.sp_firewall_group_delist('fwgrp', 'member3@localhost');
```

The firewall group profile now is trained for member accounts. When clients connect using any account in the group and attempt to execute statements, the profile protects MySQL against statements not matched by the profile allowlist.

The procedure just shown added only one member to the group profile before training its allowlist. Doing so provides better control over the training period by limiting which accounts can add new acceptable statements to the allowlist. Should additional training be necessary, you can switch the profile back to RECORDING mode:

```
CALL mysql.sp_set_firewall_group_mode('fwgrp', 'RECORDING');
```

However, that enables any member of the group to execute statements and add them to the allowlist. To limit the additional training to a single group member, call sp\_set\_firewall\_group\_mode\_and\_user(), which is like sp\_set\_firewall\_group\_mode() but takes one more argument specifying which account is permitted to train the profile in RECORDING mode. For example, to enable training only by member4@localhost, do this:

```
CALL mysql.sp_set_firewall_group_mode_and_user('fwgrp', 'RECORDING', 'member4@localhost');
```

That enables additional training by the specified account without having to remove the other group members. They can execute statements, but the statements are not added to the allowlist. (Remember, however, that in RECORDING mode the other members can execute any statement.)

![](_page_162_Picture_7.jpeg)

#### **Note**

To avoid unexpected behavior when a particular account is specified as the training account for a group profile, always ensure that account is a member of the group.

After the additional training, set the group profile back to PROTECTING mode:

```
CALL mysql.sp_set_firewall_group_mode('fwgrp', 'PROTECTING');
```

The training account established by sp\_set\_firewall\_group\_mode\_and\_user() is saved in the group profile, so the firewall remembers it in case more training is needed later. Thus, if you call sp\_set\_firewall\_group\_mode() (which takes no training account argument), the current profile training account, member4@localhost, remains unchanged.

To clear the training account if it actually is desired to enable all group members to perform training in RECORDING mode, call sp\_set\_firewall\_group\_mode\_and\_user() and pass a NULL value for the account argument:

```
CALL mysql.sp_set_firewall_group_mode_and_user('fwgrp', 'RECORDING', NULL);
```

It is possible to detect intrusions by logging nonmatching statements as suspicious without denying access. First, put the group profile in DETECTING mode:

```
CALL mysql.sp_set_firewall_group_mode('fwgrp', 'DETECTING');
```

Then, using a member account, execute a statement that does not match the group profile allowlist. In DETECTING mode, the firewall permits the nonmatching statement to execute:

```
mysql> SHOW TABLES LIKE 'customer%';
+------------------------------+
| Tables_in_sakila (customer%) |
+------------------------------+
| customer |
| customer_list |
+------------------------------+
```

In addition, the firewall writes a message to the error log:

```
[Note] Plugin MYSQL_FIREWALL reported:
'SUSPICIOUS STATEMENT from 'member1@localhost'. Reason: No match in allowlist.
Statement: SHOW TABLES LIKE ?'
```

To disable a group profile, change its mode to OFF:

```
CALL mysql.sp_set_firewall_group_mode(group, 'OFF');
```

To forget all training for a profile and disable it, reset it:

```
CALL mysql.sp_set_firewall_group_mode(group, 'RESET');
```

The reset operation causes the firewall to delete all rules for the profile and set its mode to OFF.

## <span id="page-163-0"></span>**Registering Firewall Account Profiles**

MySQL Enterprise Firewall enables profiles to be registered that correspond to individual accounts. To use a firewall account profile to protect MySQL against incoming statements from a given account, follow these steps:

- 1. Register the account profile and put it in RECORDING mode.
- 2. Connect to the MySQL server using the account and execute statements to be learned. This trains the account profile and establishes the rules that form the profile allowlist.
- 3. Switch the account profile to PROTECTING mode. When a client connects to the server using the account, the account profile allowlist restricts statement execution.
- 4. Should additional training be necessary, switch the account profile to RECORDING mode again, update its allowlist with new statement patterns, then switch it back to PROTECTING mode.

Observe these guidelines for firewall-related account references:

• Take note of the context in which account references occur. To name an account for firewall operations, specify it as a single quoted string ('user\_name@host\_name'). This differs from the usual MySQL convention for statements such as CREATE USER and GRANT, for which you quote the user and host parts of an account name separately ('user\_name'@'host\_name').

The requirement for naming accounts as a single quoted string for firewall operations means that you cannot use accounts that have embedded @ characters in the user name.

- The firewall assesses statements against accounts represented by actual user and host names as authenticated by the server. When registering accounts in profiles, do not use wildcard characters or netmasks:
  - Suppose that an account named me@%.example.org exists and a client uses it to connect to the server from the host abc.example.org.
  - The account name contains a % wildcard character, but the server authenticates the client as having a user name of me and host name of abc.example.com, and that is what the firewall sees.
  - Consequently, the account name to use for firewall operations is me@abc.example.org rather than me@%.example.org.

The following procedure shows how to register an account profile with the firewall, train the firewall to know the acceptable statements for that profile (its allowlist), and use the profile to protect MySQL against execution of unacceptable statements by the account. The example account, fwuser@localhost, is presumed for use by an application that accesses tables in the sakila database (available at [https://dev.mysql.com/doc/index-other.html\)](https://dev.mysql.com/doc/index-other.md).

Use an administrative MySQL account to perform the steps in this procedure, except those steps designated for execution by the fwuser@localhost account that corresponds to the account profile registered with the firewall. For statements executed using this account, the default database should be sakila. (You can use a different database by adjusting the instructions accordingly.)

1. If necessary, create the account to use for executing statements (choose an appropriate password) and grant it privileges for the sakila database:

```
CREATE USER 'fwuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON sakila.* TO 'fwuser'@'localhost';
```

2. Use the sp\_set\_firewall\_mode() stored procedure to register the account profile with the firewall and place the profile in RECORDING (training) mode:

```
CALL mysql.sp_set_firewall_mode('fwuser@localhost', 'RECORDING');
```

![](_page_164_Picture_4.jpeg)

#### **Note**

If you have installed MySQL Enterprise Firewall in a custom schema, then make appropriate substitution for your system. For example, if the firewall is installed in the fwdb schema, then execute the stored procedures like this:

```
CALL fwdb.sp_set_firewall_mode('fwuser@localhost', 'RECORDING');
```

3. To train the registered account profile, connect to the server as fwuser from the server host so that the firewall sees a session account of fwuser@localhost. Then use the account to execute some statements to be considered legitimate for the profile. For example:

```
SELECT first_name, last_name FROM customer WHERE customer_id = 1;
UPDATE rental SET return_date = NOW() WHERE rental_id = 1;
SELECT get_customer_balance(1, NOW());
```

Because the profile is in RECORDING mode, the firewall records the normalized digest form of the statements as rules in the profile allowlist.

![](_page_164_Picture_11.jpeg)

#### **Note**

Until the fwuser@localhost account profile receives statements in RECORDING mode, its allowlist is empty, which is equivalent to "deny all." No statement can match an empty allowlist, which has these implications:

- The account profile cannot be switched to PROTECTING mode. It would reject every statement, effectively prohibiting the account from executing any statement.
- The account profile can be switched to DETECTING mode. In this case, the profile accepts every statement but logs it as suspicious.
- 4. At this point, the account profile information is cached. To see this information, query the INFORMATION\_SCHEMA firewall tables:

```
mysql> SELECT MODE FROM INFORMATION_SCHEMA.MYSQL_FIREWALL_USERS
 WHERE USERHOST = 'fwuser@localhost';
+-----------+
| MODE |
+-----------+
| RECORDING |
+-----------+
mysql> SELECT RULE FROM INFORMATION_SCHEMA.MYSQL_FIREWALL_WHITELIST
 WHERE USERHOST = 'fwuser@localhost';
+----------------------------------------------------------------------------+
| RULE |
+----------------------------------------------------------------------------+
| SELECT `first_name` , `last_name` FROM `customer` WHERE `customer_id` = ? |
| SELECT `get_customer_balance` ( ? , NOW ( ) ) |
| UPDATE `rental` SET `return_date` = NOW ( ) WHERE `rental_id` = ? |
| SELECT @@`version_comment` LIMIT ? |
+----------------------------------------------------------------------------+
```

![](_page_164_Picture_18.jpeg)

## **Note**

The @@version\_comment rule comes from a statement sent automatically by the mysql client when you connect to the server.

![](_page_165_Picture_1.jpeg)

### **Important**

Train the firewall under conditions matching application use. For example, to determine server characteristics and capabilities, a given MySQL connector might send statements to the server at the beginning of each session. If an application normally is used through that connector, train the firewall using the connector, too. That enables those initial statements to become part of the allowlist for the account profile associated with the application.

5. Invoke sp\_set\_firewall\_mode() again, this time switching the account profile to PROTECTING mode:

CALL mysql.sp\_set\_firewall\_mode('fwuser@localhost', 'PROTECTING');

![](_page_165_Picture_6.jpeg)

## **Important**

Switching the account profile out of RECORDING mode synchronizes its cached data to the firewall database tables that provide persistent underlying storage. If you do not switch the mode for a profile that is being recorded, the cached data is not written to persistent storage and is lost when the server is restarted. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL Enterprise](#page-151-0) [Firewall\)](#page-151-0).

- 6. Test the account profile by using the account to execute some acceptable and unacceptable statements. The firewall matches each statement from the account against the profile allowlist and accepts or rejects it:
  - This statement is not identical to a training statement but produces the same normalized statement as one of them, so the firewall accepts it:

```
mysql> SELECT first_name, last_name FROM customer WHERE customer_id = '48';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| ANN | EVANS |
+------------+-----------+
```

• These statements match nothing in the allowlist, so the firewall rejects each with an error:

```
mysql> SELECT first_name, last_name FROM customer WHERE customer_id = 1 OR TRUE;
ERROR 1045 (28000): Statement was blocked by Firewall
mysql> SHOW TABLES LIKE 'customer%';
ERROR 1045 (28000): Statement was blocked by Firewall
mysql> TRUNCATE TABLE mysql.slow_log;
ERROR 1045 (28000): Statement was blocked by Firewall
```

• If the [mysql\\_firewall\\_trace](#page-177-1) system variable is enabled, the firewall also writes rejected statements to the error log. For example:

```
[Note] Plugin MYSQL_FIREWALL reported:
'ACCESS DENIED for fwuser@localhost. Reason: No match in allowlist.
Statement: TRUNCATE TABLE `mysql` . `slow_log`'
```

These log messages may be helpful in identifying the source of attacks, should that be necessary.

The firewall account profile now is trained for the fwuser@localhost account. When clients connect using that account and attempt to execute statements, the profile protects MySQL against statements not matched by the profile allowlist.

It is possible to detect intrusions by logging nonmatching statements as suspicious without denying access. First, put the account profile in DETECTING mode:

```
CALL mysql.sp_set_firewall_mode('fwuser@localhost', 'DETECTING');
```

Then, using the account, execute a statement that does not match the account profile allowlist. In DETECTING mode, the firewall permits the nonmatching statement to execute:

```
mysql> SHOW TABLES LIKE 'customer%';
+------------------------------+
| Tables_in_sakila (customer%) |
+------------------------------+
| customer |
| customer_list |
+------------------------------+
```

In addition, the firewall writes a message to the error log:

```
[Note] Plugin MYSQL_FIREWALL reported:
'SUSPICIOUS STATEMENT from 'fwuser@localhost'. Reason: No match in allowlist.
Statement: SHOW TABLES LIKE ?'
```

To disable an account profile, change its mode to OFF:

```
CALL mysql.sp_set_firewall_mode(user, 'OFF');
```

To forget all training for a profile and disable it, reset it:

```
CALL mysql.sp_set_firewall_mode(user, 'RESET');
```

The reset operation causes the firewall to delete all rules for the profile and set its mode to OFF.

## <span id="page-166-0"></span>**Monitoring the Firewall**

To assess firewall activity, examine its status variables. For example, after performing the procedure shown earlier to train and protect the fwgrp group profile, the variables look like this:

```
mysql> SHOW GLOBAL STATUS LIKE 'Firewall%';
+----------------------------+-------+
| Variable_name | Value |
+----------------------------+-------+
| Firewall_access_denied | 3 |
| Firewall_access_granted | 4 |
| Firewall_access_suspicious | 1 |
| Firewall_cached_entries | 4 |
+----------------------------+-------+
```

The variables indicate the number of statements rejected, accepted, logged as suspicious, and added to the cache, respectively. The [Firewall\\_access\\_granted](#page-178-0) count is 4 because of the @@version\_comment statement sent by the mysql client each of the three times you connected using the registered account, plus the SHOW TABLES statement that was not blocked in DETECTING mode.

## <span id="page-166-1"></span>**Migrating Account Profiles to Group Profiles**

MySQL Enterprise Firewall supports account profiles that each apply to a single account and also group profiles that each can apply to multiple accounts. A group profile enables easier administration when the same allowlist is to be applied to multiple accounts: instead of creating one account profile per account and duplicating the allowlist across all those profiles, create a single group profile and make the accounts members of it. The group allowlist then applies to all the accounts.

A group profile with a single member account is logically equivalent to an account profile for that account, so it is possible to administer the firewall using group profiles exclusively, rather than a mix of account and group profiles. For new firewall installations, that is accomplished by uniformly creating new profiles as group profiles and avoiding account profiles.

Due to the greater flexibility offered by group profiles, it is recommended that all new firewall profiles be created as group profiles. Account profiles are deprecated, and subject to removal in a future MySQL version. For upgrades from firewall installations that already contain account profiles, MySQL Enterprise Firewall includes a stored procedure named sp\_migrate\_firewall\_user\_to\_group() to help you convert account profiles to group profiles. To use it, perform the following procedure as a user who has the FIREWALL\_ADMIN privilege:

1. Run the firewall\_profile\_migration.sql script to install the sp\_migrate\_firewall\_user\_to\_group() stored procedure. The script is located in the share directory of your MySQL installation.

Specify the same firewall database name on the command line that you previously defined for your firewall installation. The example here specifies the system database, mysql.

```
$> mysql -u root -p -D mysql < firewall_profile_migration.sql
Enter password: (enter root password here)
```

If you installed MySQL Enterprise Firewall in a custom schema, make the appropriate substitution for your system.

2. Identify which account profiles exist by querying the Information Schema MYSQL\_FIREWALL\_USERS table. For example:

```
mysql> SELECT USERHOST FROM INFORMATION_SCHEMA.MYSQL_FIREWALL_USERS;
+-------------------------------+
| USERHOST |
+-------------------------------+
| admin@localhost |
| local_client@localhost |
| remote_client@abc.example.com |
+-------------------------------+
```

3. For each account profile identified by the previous step, convert it to a group profile. Replace the mysql. prefix with the actual firewall database name, if necessary:

```
CALL mysql.sp_migrate_firewall_user_to_group('admin@localhost', 'admins');
CALL mysql.sp_migrate_firewall_user_to_group('local_client@localhost', 'local_clients');
CALL mysql.sp_migrate_firewall_user_to_group('remote_client@localhost', 'remote_clients');
```

In each case, the account profile must exist and must not currently be in RECORDING mode, and the group profile must not already exist. The resulting group profile has the named account as its single enlisted member, which is also set as the group training account. The group profile operational mode is taken from the account profile operational mode.

4. (Optional) Remove sp\_migrate\_firewall\_user\_to\_group():

```
DROP PROCEDURE IF EXISTS mysql.sp_migrate_firewall_user_to_group;
```

If you installed MySQL Enterprise Firewall in a custom schema, make the appropriate substitution for your system.

For additional details about sp\_migrate\_firewall\_user\_to\_group(), see [Firewall](#page-173-0) [Miscellaneous Stored Procedures.](#page-173-0)

## <span id="page-167-0"></span>**8.4.7.4 MySQL Enterprise Firewall Reference**

The following sections provide a reference to MySQL Enterprise Firewall elements:

- [MySQL Enterprise Firewall Tables](#page-168-0)
- [MySQL Enterprise Firewall Stored Procedures](#page-169-0)
- [MySQL Enterprise Firewall Administrative Functions](#page-173-1)
- [MySQL Enterprise Firewall System Variables](#page-176-1)
- [MySQL Enterprise Firewall Status Variables](#page-177-2)

## <span id="page-168-0"></span>**MySQL Enterprise Firewall Tables**

MySQL Enterprise Firewall maintains profile information on a per-group and per-account basis, using tables in the firewall database for persistent storage and Information Schema and Performance Schema tables to provide views into in-memory cached data. When enabled, the firewall bases operational decisions on the cached data. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL Enterprise Firewall\)](#page-151-0).

Tables in the firewall database are covered in this section. For information about MySQL Enterprise Firewall Information Schema and Performance Schema tables, see Section 28.7, "INFORMATION\_SCHEMA MySQL Enterprise Firewall Tables", and Section 29.12.17, "Performance Schema Firewall Tables", respectively.

- [Firewall Group Profile Tables](#page-168-1)
- [Firewall Account Profile Tables](#page-169-1)

#### <span id="page-168-1"></span>**Firewall Group Profile Tables**

MySQL Enterprise Firewall maintains group profile information using tables in the firewall database (mysql or custom) for persistent storage and Performance Schema tables to provide views into inmemory cached data.

Each system and Performance Schema table is accessible only by accounts that have the SELECT privilege for it.

The firewall-database.firewall\_groups table lists names and operational modes of registered firewall group profiles. The table has the following columns (with the corresponding Performance Schema firewall\_groups table having similar but not necessarily identical columns):

• NAME

The group profile name.

• MODE

The current operational mode for the profile. Permitted mode values are OFF, DETECTING, PROTECTING, and RECORDING. For details about their meanings, see [Firewall Concepts](#page-155-0).

• USERHOST

The training account for the group profile, to be used when the profile is in RECORDING mode. The value is NULL, or a non-NULL account that has the format user\_name@host\_name:

- If the value is NULL, the firewall records allowlist rules for statements received from any account that is a member of the group.
- If the value is non-NULL, the firewall records allowlist rules only for statements received from the named account (which should be a member of the group).

The firewall-database.firewall\_group\_allowlist table lists allowlist rules of registered firewall group profiles. The table has the following columns (with the corresponding Performance Schema firewall\_group\_allowlist table having similar but not necessarily identical columns):

• NAME

The group profile name.

• RULE

A normalized statement indicating an acceptable statement pattern for the profile. A profile allowlist is the union of its rules.

• ID

An integer column that is a primary key for the table.

The firewall-database.firewall\_membership table lists the members (accounts) of registered firewall group profiles. The table has the following columns (with the corresponding Performance Schema firewall\_membership table having similar but not necessarily identical columns):

• GROUP\_ID

The group profile name.

• MEMBER\_ID

The name of an account that is a member of the profile.

#### <span id="page-169-1"></span>**Firewall Account Profile Tables**

MySQL Enterprise Firewall maintains account profile information using tables in the firewall database for persistent storage and INFORMATION\_SCHEMA tables to provide views into in-memory cached data. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL](#page-151-0) [Enterprise Firewall\)](#page-151-0).

Each default database table is accessible only by accounts that have the SELECT privilege for it. The INFORMATION\_SCHEMA tables are accessible by anyone.

These tables are deprecated, and subject to removal in a future MySQL version. See [Migrating](#page-166-1) [Account Profiles to Group Profiles](#page-166-1).

The firewall-database.firewall\_users table lists names and operational modes of registered firewall account profiles. The table has the following columns (with the corresponding MYSQL\_FIREWALL\_USERS table having similar but not necessarily identical columns):

• USERHOST

The account profile name. Each account name has the format user\_name@host\_name.

• MODE

The current operational mode for the profile. Permitted mode values are OFF, DETECTING, PROTECTING, RECORDING, and RESET. For details about their meanings, see [Firewall Concepts.](#page-155-0)

The firewall-database.firewall\_whitelist table lists allowlist rules of registered firewall account profiles. The table has the following columns (with the corresponding MYSQL\_FIREWALL\_WHITELIST table having similar but not necessarily identical columns):

• USERHOST

The account profile name. Each account name has the format user\_name@host\_name.

• RULE

A normalized statement indicating an acceptable statement pattern for the profile. A profile allowlist is the union of its rules.

• ID

An integer column that is a primary key for the table.

## <span id="page-169-0"></span>**MySQL Enterprise Firewall Stored Procedures**

MySQL Enterprise Firewall stored procedures perform tasks such as registering profiles with the firewall, establishing their operational mode, and managing transfer of firewall data between the cache and persistent storage. These procedures invoke administrative functions that provide an API for lowerlevel tasks.

Firewall stored procedures are created in the firewall database. The firewall database can be the mysql system database or a custom schema (see [Installing MySQL Enterprise Firewall](#page-151-0)).

To invoke a firewall stored procedure, either do so while the specified firewall database is the default database, or qualify the procedure name with the database name. For example, if mysql is the firewall database:

```
CALL mysql.sp_set_firewall_group_mode(group, mode);
```

In MySQL 8.4, firewall stored procedures are transactional; if an error occurs during execution of a firewall stored procedure, all changes made by it up to that point are rolled back, and an error is reported.

![](_page_170_Picture_5.jpeg)

#### **Note**

If you have installed MySQL Enterprise Firewall in a custom schema, then make appropriate substitution for your system. For example, if the firewall is installed in the fwdb schema, then execute the stored procedures like this:

```
CALL fwdb.sp_set_firewall_group_mode(group, mode);
```

- [Firewall Group Profile Stored Procedures](#page-170-0)
- [Firewall Account Profile Stored Procedures](#page-172-0)
- [Firewall Miscellaneous Stored Procedures](#page-173-0)

#### <span id="page-170-0"></span>**Firewall Group Profile Stored Procedures**

These stored procedures perform management operations on firewall group profiles:

• sp\_firewall\_group\_delist(group, user)

This stored procedure removes an account from a firewall group profile.

If the call succeeds, the change in group membership is made to both the in-memory cache and persistent storage.

#### Arguments:

- group: The name of the affected group profile.
- user: The account to remove, as a string in user\_name@host\_name format.

## Example:

```
CALL mysql.sp_firewall_group_delist('g', 'fwuser@localhost');
```

• sp\_firewall\_group\_enlist(group, user)

This stored procedure adds an account to a firewall group profile. It is not necessary to register the account itself with the firewall before adding the account to the group.

If the call succeeds, the change in group membership is made to both the in-memory cache and persistent storage.

#### Arguments:

- group: The name of the affected group profile.
- user: The account to add, as a string in user\_name@host\_name format.

```
CALL mysql.sp_firewall_group_enlist('g', 'fwuser@localhost');
```

• sp\_reload\_firewall\_group\_rules(group)

This stored procedure provides control over firewall operation for individual group profiles. The procedure uses firewall administrative functions to reload the in-memory rules for a group profile from the rules stored in the firewall-database.firewall\_group\_allowlist table.

#### Arguments:

• group: The name of the affected group profile.

#### Example:

CALL mysql.sp\_reload\_firewall\_group\_rules('myapp');

![](_page_171_Picture_7.jpeg)

#### **Warning**

This procedure clears the group profile in-memory allowlist rules before reloading them from persistent storage, and sets the profile mode to OFF. If the profile mode was not OFF prior to the sp\_reload\_firewall\_group\_rules() call, use sp\_set\_firewall\_group\_mode() to restore its previous mode after reloading the rules. For example, if the profile was in PROTECTING mode, that is no longer true after calling sp\_reload\_firewall\_group\_rules() and you must set it to PROTECTING again explicitly.

• sp\_set\_firewall\_group\_mode(group, mode)

This stored procedure establishes the operational mode for a firewall group profile, after registering the profile with the firewall if it was not already registered. The procedure also invokes firewall administrative functions as necessary to transfer firewall data between the cache and persistent storage. This procedure may be called even if the mysql\_firewall\_mode system variable is OFF, although setting the mode for a profile has no operational effect until the firewall is enabled.

If the profile previously existed, any recording limitation for it remains unchanged. To set or clear the limitation, call sp\_set\_firewall\_group\_mode\_and\_user() instead.

#### Arguments:

- group: The name of the affected group profile.
- mode: The operational mode for the profile, as a string. Permitted mode values are OFF, DETECTING, PROTECTING, and RECORDING. For details about their meanings, see [Firewall](#page-155-0) [Concepts](#page-155-0).

```
CALL mysql.sp_set_firewall_group_mode('myapp', 'PROTECTING');
```

• sp\_set\_firewall\_group\_mode\_and\_user(group, mode, user)

This stored procedure registers a group with the firewall and establishes its operational mode, similar to sp\_set\_firewall\_group\_mode(), but also specifies the training account to be used when the group is in RECORDING mode.

#### Arguments:

- group: The name of the affected group profile.
- mode: The operational mode for the profile, as a string. Permitted mode values are OFF, DETECTING, PROTECTING, and RECORDING. For details about their meanings, see [Firewall](#page-155-0) [Concepts](#page-155-0).
- user: The training account for the group profile, to be used when the profile is in RECORDING mode. The value is NULL, or a non-NULL account that has the format user\_name@host\_name:
  - If the value is NULL, the firewall records allowlist rules for statements received from any account that is a member of the group.
  - If the value is non-NULL, the firewall records allowlist rules only for statements received from the named account (which should be a member of the group).

#### Example:

```
CALL mysql.sp_set_firewall_group_mode_and_user('myapp', 'RECORDING', 'myapp_user1@localhost');
```

## <span id="page-172-0"></span>**Firewall Account Profile Stored Procedures**

These stored procedures perform management operations on firewall account profiles:

• sp\_reload\_firewall\_rules(user)

This stored procedure provides control over firewall operation for individual account profiles. The procedure uses firewall administrative functions to reload the in-memory rules for an account profile from the rules stored in the firewall-database.firewall\_whitelist table.

## Arguments:

• user: The name of the affected account profile, as a string in user\_name@host\_name format.

#### Example:

CALL sp\_reload\_firewall\_rules('fwuser@localhost');

![](_page_172_Picture_19.jpeg)

## **Warning**

This procedure clears the account profile in-memory allowlist rules before reloading them from persistent storage, and sets the profile mode to OFF. If the profile mode was not OFF prior to the sp\_reload\_firewall\_rules() call, use sp\_set\_firewall\_mode() to restore its previous mode after reloading the rules. For example, if the profile was in PROTECTING mode, that is no longer true after calling sp\_reload\_firewall\_rules() and you must set it to PROTECTING again explicitly.

This procedure is deprecated, and subject to removal in a future MySQL version. See [Migrating](#page-166-1) [Account Profiles to Group Profiles](#page-166-1).

• sp\_set\_firewall\_mode(user, mode)

This stored procedure establishes the operational mode for a firewall account profile, after registering the profile with the firewall if it was not already registered. The procedure also invokes firewall

administrative functions as necessary to transfer firewall data between the cache and persistent storage. This procedure may be called even if the mysql\_firewall\_mode system variable is OFF, although setting the mode for a profile has no operational effect until the firewall is enabled.

#### Arguments:

- user: The name of the affected account profile, as a string in user\_name@host\_name format.
- mode: The operational mode for the profile, as a string. Permitted mode values are OFF, DETECTING, PROTECTING, RECORDING, and RESET. For details about their meanings, see [Firewall Concepts](#page-155-0).

Switching an account profile to any mode but RECORDING synchronizes its firewall cache data to the firewall database tables that provide persistent underlying storage (mysql or custom). Switching the mode from OFF to RECORDING reloads the allowlist from the firewalldatabase.firewall\_whitelist table into the cache.

If an account profile has an empty allowlist, its mode cannot be set to PROTECTING because the profile would reject every statement, effectively prohibiting the account from executing statements. In response to such a mode-setting attempt, the firewall produces a diagnostic message that is returned as a result set rather than as an SQL error:

```
mysql> CALL sp_set_firewall_mode('a@b','PROTECTING');
+----------------------------------------------------------------------+
| set_firewall_mode(arg_userhost, arg_mode) |
+----------------------------------------------------------------------+
| ERROR: PROTECTING mode requested for a@b but the allowlist is empty. |
+----------------------------------------------------------------------+
```

This procedure is deprecated, and subject to removal in a future MySQL version. See [Migrating](#page-166-1) [Account Profiles to Group Profiles](#page-166-1).

#### <span id="page-173-0"></span>**Firewall Miscellaneous Stored Procedures**

These stored procedures perform miscellaneous firewall management operations.

• sp\_migrate\_firewall\_user\_to\_group(user, group)

The sp\_migrate\_firewall\_user\_to\_group() stored procedure converts a firewall account profile to a group profile with the account as its single enlisted member. Run the firewall\_profile\_migration.sql script to install it. The conversion procedure is discussed in [Migrating Account Profiles to Group Profiles.](#page-166-1)

This routine requires the FIREWALL\_ADMIN privilege.

#### Arguments:

- user: The name of the account profile to convert to a group profile, as a string in user\_name@host\_name format. The account profile must exist, and must not currently be in RECORDING mode.
- group: The name of the new group profile, which must not already exist. The new group profile has the named account as its single enlisted member, and that member is set as the group training account. The group profile operational mode is taken from the account profile operational mode.

#### Example:

```
CALL sp_migrate_firewall_user_to_group('fwuser@localhost', 'mygroup);
```

## <span id="page-173-1"></span>**MySQL Enterprise Firewall Administrative Functions**

MySQL Enterprise Firewall administrative functions provide an API for lower-level tasks such as synchronizing the firewall cache with the underlying system tables.

Under normal operation, these functions are invoked by the firewall stored procedures, not directly by users. For that reason, these function descriptions do not include details such as information about their arguments and return types.

- [Firewall Group Profile Functions](#page-174-0)
- [Firewall Account Profile Functions](#page-175-0)
- [Firewall Miscellaneous Functions](#page-175-1)

### <span id="page-174-1"></span><span id="page-174-0"></span>**Firewall Group Profile Functions**

These functions perform management operations on firewall group profiles:

• [firewall\\_group\\_delist\(](#page-174-1)group, user)

This function removes an account from a group profile. It requires the FIREWALL\_ADMIN privilege.

#### Example:

```
SELECT firewall_group_delist('g', 'fwuser@localhost');
```

<span id="page-174-2"></span>• [firewall\\_group\\_enlist\(](#page-174-2)group, user)

This function adds an account to a group profile. It requires the FIREWALL\_ADMIN privilege.

It is not necessary to register the account itself with the firewall before adding the account to the group.

#### Example:

```
SELECT firewall_group_enlist('g', 'fwuser@localhost');
```

<span id="page-174-3"></span>• [read\\_firewall\\_group\\_allowlist\(](#page-174-3)group, rule)

This aggregate function updates the recorded-statement cache for the named group profile through a SELECT statement on the firewall-database.firewall\_group\_allowlist table. It requires the FIREWALL\_ADMIN privilege.

## Example:

```
SELECT read_firewall_group_allowlist('my_fw_group', fgw.rule)
FROM mysql.firewall_group_allowlist AS fgw
WHERE NAME = 'my_fw_group';
```

<span id="page-174-4"></span>• [read\\_firewall\\_groups\(](#page-174-4)group, mode, user)

This aggregate function updates the firewall group profile cache through a SELECT statement on the firewall-database.firewall\_groups table. It requires the FIREWALL\_ADMIN privilege.

#### Example:

```
SELECT read_firewall_groups('g', 'RECORDING', 'fwuser@localhost')
FROM mysql.firewall_groups;
```

<span id="page-174-5"></span>• [set\\_firewall\\_group\\_mode\(](#page-174-5)group, mode[, user])

This function manages the group profile cache, establishes the profile operational mode, and optionally specifies the profile training account. It requires the FIREWALL\_ADMIN privilege.

If the optional user argument is not given, any previous user setting for the profile remains unchanged. To change the setting, call the function with a third argument.

If the optional user argument is given, it specifies the training account for the group profile, to be used when the profile is in RECORDING mode. The value is NULL, or a non-NULL account that has the format user\_name@host\_name:

- If the value is NULL, the firewall records allowlist rules for statements received from any account that is a member of the group.
- If the value is non-NULL, the firewall records allowlist rules only for statements received from the named account (which should be a member of the group).

#### Example:

```
SELECT set_firewall_group_mode('g', 'DETECTING');
```

## <span id="page-175-2"></span><span id="page-175-0"></span>**Firewall Account Profile Functions**

These functions perform management operations on firewall account profiles:

```
• read_firewall_users(user, mode)
```

This aggregate function updates the firewall account profile cache through a SELECT statement on the firewall-database.firewall\_users table. It requires the FIREWALL\_ADMIN privilege or the deprecated SUPER privilege.

#### Example:

```
SELECT read_firewall_users('fwuser@localhost', 'RECORDING')
FROM mysql.firewall_users;
```

This function is deprecated, and subject to removal in a future MySQL version. See [Migrating](#page-166-1) [Account Profiles to Group Profiles](#page-166-1).

<span id="page-175-3"></span>• [read\\_firewall\\_whitelist\(](#page-175-3)user, rule)

This aggregate function updates the recorded-statement cache for the named account profile through a SELECT statement on the firewall-database.firewall\_whitelist table. It requires the FIREWALL\_ADMIN privilege or the deprecated SUPER privilege.

### Example:

```
SELECT read_firewall_whitelist('fwuser@localhost', fw.rule)
FROM mysql.firewall_whitelist AS fw
WHERE USERHOST = 'fwuser@localhost';
```

This function is deprecated, and subject to removal in a future MySQL version. See [Migrating](#page-166-1) [Account Profiles to Group Profiles](#page-166-1).

<span id="page-175-4"></span>• [set\\_firewall\\_mode\(](#page-175-4)user, mode)

This function manages the account profile cache and establishes the profile operational mode. It requires the FIREWALL\_ADMIN privilege or the deprecated SUPER privilege.

### Example:

```
SELECT set_firewall_mode('fwuser@localhost', 'RECORDING');
```

This function is deprecated, and subject to removal in a future MySQL version. See [Migrating](#page-166-1) [Account Profiles to Group Profiles](#page-166-1).

#### <span id="page-175-5"></span><span id="page-175-1"></span>**Firewall Miscellaneous Functions**

These functions perform miscellaneous firewall operations:

```
• mysql_firewall_flush_status()
```

This function resets several firewall status variables to 0:

- [Firewall\\_access\\_denied](#page-177-3)
- [Firewall\\_access\\_granted](#page-178-0)
- [Firewall\\_access\\_suspicious](#page-178-1)

This function requires the FIREWALL\_ADMIN privilege or the deprecated SUPER privilege.

#### Example:

```
SELECT mysql_firewall_flush_status();
```

<span id="page-176-2"></span>• [normalize\\_statement\(](#page-176-2)stmt)

This function normalizes an SQL statement into the digest form used for allowlist rules. It requires the FIREWALL\_ADMIN privilege or the deprecated SUPER privilege.

#### Example:

SELECT normalize\_statement('SELECT \* FROM t1 WHERE c1 > 2');

![](_page_176_Picture_12.jpeg)

#### **Note**

The same digest functionality is available outside firewall context using the STATEMENT\_DIGEST\_TEXT() SQL function.

## <span id="page-176-1"></span>**MySQL Enterprise Firewall System Variables**

MySQL Enterprise Firewall supports the following system variables. Use them to configure firewall operation. These variables are unavailable unless the firewall is installed (see [Section 8.4.7.2,](#page-151-1) ["Installing or Uninstalling MySQL Enterprise Firewall"\)](#page-151-1).

<span id="page-176-3"></span>• [mysql\\_firewall\\_database](#page-176-3)

| Command-Line Format  | mysql-firewall-database[=value] |
|----------------------|---------------------------------|
| System Variable      | mysql_firewall_database         |
| Scope                | Global                          |
| Dynamic              | No                              |
| SET_VAR Hint Applies | No                              |
| Type                 | String                          |
| Default Value        | mysql                           |

Specifies the database from which MySQL Enterprise Firewall reads data. Typically, the MYSQL\_FIREWALL server-side plugin stores its internal data (tables, stored procedures, and functions) in the mysql system database, but you can create and use a custom schema instead (see [Installing MySQL Enterprise Firewall](#page-151-0)). This variable permits specifying an alternative database name at startup.

<span id="page-176-0"></span>• [mysql\\_firewall\\_mode](#page-176-0)

| Command-Line Format  | mysql-firewall-mode[={OFF ON}] |
|----------------------|--------------------------------|
| System Variable      | mysql_firewall_mode            |
| Scope                | Global                         |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |

| Type          | Boolean |
|---------------|---------|
| Default Value | ON      |

Whether MySQL Enterprise Firewall is enabled (the default) or disabled.

<span id="page-177-0"></span>• [mysql\\_firewall\\_reload\\_interval\\_seconds](#page-177-0)

| Command-Line Format  | mysql-firewall-reload-interval<br>seconds[=value] |
|----------------------|---------------------------------------------------|
| System Variable      | mysql_firewall_reload_interval_seconds            |
| Scope                | Global                                            |
| Dynamic              | No                                                |
| SET_VAR Hint Applies | No                                                |
| Type                 | Integer                                           |
| Default Value        | 0                                                 |
| Minimum Value        | 60 (unless 0: OFF)                                |
| Maximum Value        | INT_MAX                                           |
| Unit                 | seconds                                           |

Specifies the interval (in seconds) that the server-side plugin uses to reload its internal cache from firewall tables. When [mysql\\_firewall\\_reload\\_interval\\_seconds](#page-177-0) has a value of zero (the default), no periodic reloading of data from tables occurs at runtime. Values between 0 and 60 (1 to 59) are not acknowledged by the plugin. Instead, these values adjust to 60 automatically.

This variable requires that the scheduler component be enabled (ON). For more information, see [Scheduling Firewall Cache Reloads.](#page-153-2)

<span id="page-177-1"></span>• [mysql\\_firewall\\_trace](#page-177-1)

| Command-Line Format  | mysql-firewall-trace[={OFF ON}] |
|----------------------|---------------------------------|
| System Variable      | mysql_firewall_trace            |
| Scope                | Global                          |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |
| Default Value        | OFF                             |

Whether the MySQL Enterprise Firewall trace is enabled or disabled (the default). When [mysql\\_firewall\\_trace](#page-177-1) is enabled, for PROTECTING mode, the firewall writes rejected statements to the error log.

## <span id="page-177-2"></span>**MySQL Enterprise Firewall Status Variables**

MySQL Enterprise Firewall supports the following status variables. Use them to obtain information about firewall operational status. These variables are unavailable unless the firewall is installed (see [Section 8.4.7.2, "Installing or Uninstalling MySQL Enterprise Firewall"](#page-151-1)). Firewall status variables are set to 0 whenever the MYSQL\_FIREWALL plugin is installed or the server is started. Many of them are reset to zero by the [mysql\\_firewall\\_flush\\_status\(\)](#page-175-5) function (see [MySQL Enterprise Firewall](#page-173-1) [Administrative Functions\)](#page-173-1).

<span id="page-177-3"></span>• [Firewall\\_access\\_denied](#page-177-3)

The number of statements rejected by MySQL Enterprise Firewall.

<span id="page-178-0"></span>• [Firewall\\_access\\_granted](#page-178-0)

The number of statements accepted by MySQL Enterprise Firewall.

<span id="page-178-1"></span>• [Firewall\\_access\\_suspicious](#page-178-1)

The number of statements logged by MySQL Enterprise Firewall as suspicious for users who are in DETECTING mode.

• [Firewall\\_cached\\_entries](#page-178-2)

The number of statements recorded by MySQL Enterprise Firewall, including duplicates.

# <span id="page-178-2"></span>**8.5 MySQL Enterprise Data Masking and De-Identification**

![](_page_178_Picture_8.jpeg)

#### **Note**

MySQL Enterprise Data Masking and De-Identification is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, <https://www.mysql.com/products/>.

MySQL Enterprise Edition provides data masking and de-identification capabilities:

- Transformation of existing data to mask it and remove identifying characteristics, such as changing all digits of a credit card number but the last four to 'X' characters.
- Generation of random data, such as email addresses and payment card numbers.
- Substitution of data by data from dictionaries stored in the database. The dictionaries are easily replicated in a standard way. Administration is restricted to authorized users who are granted special privileges so that only they can create and modify the dictionaries.

![](_page_178_Picture_15.jpeg)

### **Note**

MySQL Enterprise Data Masking and De-Identification was implemented originally in MySQL as a plugin library. As of MySQL 8.4, MySQL Enterprise Edition also provides components to access data masking and de-identification capabilities. For information about the similarities and differences, see [Table 8.45, "Comparison Between Data-Masking Components and Plugin](#page-180-0) [Elements"](#page-180-0).

If you are using MySQL Enterprise Data Masking and De-Identification for the first time, consider installing the components for access to the ongoing enhancements only available with component infrastructure.

The way that applications use these capabilities depends on the purpose for which the data is used and who accesses it:

- Applications that use sensitive data may protect it by performing data masking and permitting use of partially masked data for client identification. Example: A call center may ask for clients to provide their last four Social Security Number digits.
- Applications that require properly formatted data, but not necessarily the original data, can synthesize sample data. Example: An application developer who is testing data validators but has no access to original data may synthesize random data with the same format.
- Applications that must substitute a real name with a dictionary term to protect to protect sensitive information, but still provide realistic content to application users. Example: A user in training who is restricted from viewing addresses gets a random term from dictionary city names instead of the real city name. A variant of this scenario may be that the real city name is replaced only if it exists in usa\_city\_names.

## Example 1:

Medical research facilities can hold patient data that comprises a mix of personal and medical data. This may include genetic sequences (long strings), test results stored in JSON format, and other data types. Although the data may be used mostly by automated analysis software, access to genome data or test results of particular patients is still possible. In such cases, data masking should be used to render this information not personally identifiable.

### Example 2:

A credit card processor company provides a set of services using sensitive data, such as:

- Processing a large number of financial transactions per second.
- Storing a large amount of transaction-related data.
- Protecting transaction-related data with strict requirements for personal data.
- Handling client complaints about transactions using reversible or partially masked data.

A typical transaction may include many types of sensitive information, including:

- Credit card number.
- Transaction type and amount.
- Merchant type.
- Transaction cryptogram (to confirm transaction legitimacy).
- Geolocation of GPS-equipped terminal (for fraud detection).

Those types of information may then be joined within a bank or other card-issuing financial institution with client personal data, such as:

- Full client name (either person or company).
- Address.
- Date of birth.
- Social Security number.
- Email address.
- Phone number.

Various employee roles within both the card processing company and the financial institution require access to that data. Some of these roles may require access only to masked data. Other roles may require access to the original data on a case-to-case basis, which is recorded in audit logs.

Masking and de-identification are core to regulatory compliance, so MySQL Enterprise Data Masking and De-Identification can help application developers satisfy privacy requirements:

- PCI DSS: Payment Card Data.
- HIPAA: Privacy of Health Data, Health Information Technology for Economic and Clinical Health Act (HITECH Act).
- EU General Data Protection Directive (GDPR): Protection of Personal Data.
- Data Protection Act (UK): Protection of Personal Data.
- Sarbanes Oxley, GLBA, The USA Patriot Act, Identity Theft and Assumption Deterrence Act of 1998.
- FERPA Student Data, NASD, CA SB1386 and AB 1950, State Data Protection Laws, Basel II.

The following sections describe the elements of MySQL Enterprise Data Masking and De-Identification, discuss how to install and use it, and provide reference information for its elements.