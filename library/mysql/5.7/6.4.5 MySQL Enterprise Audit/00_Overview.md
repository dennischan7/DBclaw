---
source: MySQL 5.7 Reference
title: 00_Overview
---

![](_page_31_Picture_9.jpeg)

#### **Note**

MySQL Enterprise Audit is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see [https://](https://www.mysql.com/products/) [www.mysql.com/products/](https://www.mysql.com/products/).

MySQL Enterprise Edition includes MySQL Enterprise Audit, implemented using a server plugin named audit\_log. MySQL Enterprise Audit uses the open MySQL Audit API to enable standard, policybased monitoring, logging, and blocking of connection and query activity executed on specific MySQL servers. Designed to meet the Oracle audit specification, MySQL Enterprise Audit provides an out of box, easy to use auditing and compliance solution for applications that are governed by both internal and external regulatory guidelines.

When installed, the audit plugin enables MySQL Server to produce a log file containing an audit record of server activity. The log contents include when clients connect and disconnect, and what actions they perform while connected, such as which databases and tables they access.

After you install the audit plugin (see [Section 6.4.5.2, "Installing or Uninstalling MySQL Enterprise](#page-32-0) [Audit"](#page-32-0)), it writes an audit log file. By default, the file is named audit.log in the server data directory. To change the name of the file, set the [audit\\_log\\_file](#page-91-0) system variable at server startup.

By default, audit log file contents are written in new-style XML format, without compression or encryption. To select the file format, set the [audit\\_log\\_format](#page-92-0) system variable at server startup. For details on file format and contents, see [Section 6.4.5.4, "Audit Log File Formats"](#page-35-0).

For more information about controlling how logging occurs, including audit log file naming and format selection, see [Section 6.4.5.5, "Configuring Audit Logging Characteristics".](#page-53-0) To perform filtering of

audited events, see [Section 6.4.5.7, "Audit Log Filtering"](#page-62-0). For descriptions of the parameters used to configure the audit log plugin, see [Audit Log Options and Variables.](#page-87-0)

If the audit log plugin is enabled, the Performance Schema (see Chapter 25, MySQL Performance Schema) has instrumentation for it. To identify the relevant instruments, use this query:

```
SELECT NAME FROM performance_schema.setup_instruments
WHERE NAME LIKE '%/alog/%';
```

## <span id="page-32-1"></span>**6.4.5.1 Elements of MySQL Enterprise Audit**

MySQL Enterprise Audit is based on the audit log plugin and related elements:

- A server-side plugin named audit\_log examines auditable events and determines whether to write them to the audit log.
- A set of functions enables manipulation of filtering definitions that control logging behavior, the encryption password, and log file reading.
- Tables in the mysql system database provide persistent storage of filter and user account data.
- System variables enable audit log configuration and status variables provide runtime operational information.

![](_page_32_Picture_10.jpeg)

### **Note**

Prior to MySQL 5.7.13, MySQL Enterprise Audit consists only of the audit\_log plugin and operates in legacy mode. See [Section 6.4.5.10, "Legacy](#page-79-0) [Mode Audit Log Filtering".](#page-79-0)

## <span id="page-32-0"></span>**6.4.5.2 Installing or Uninstalling MySQL Enterprise Audit**

This section describes how to install or uninstall MySQL Enterprise Audit, which is implemented using the audit log plugin and related elements described in [Section 6.4.5.1, "Elements of MySQL Enterprise](#page-32-1) [Audit"](#page-32-1). For general information about installing plugins, see Section 5.5.1, "Installing and Uninstalling Plugins".

![](_page_32_Picture_15.jpeg)

#### **Important**

Read this entire section before following its instructions. Parts of the procedure differ depending on your environment.

![](_page_32_Picture_18.jpeg)

#### **Note**

If installed, the audit\_log plugin involves some minimal overhead even when disabled. To avoid this overhead, do not install MySQL Enterprise Audit unless you plan to use it.

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

![](_page_32_Picture_22.jpeg)

#### **Note**

The instructions here apply to MySQL 5.7.13 and later.

Also, prior to MySQL 5.7.13, MySQL Enterprise Audit consists only of the audit\_log plugin and includes none of the other elements described in [Section 6.4.5.1, "Elements of MySQL Enterprise Audit".](#page-32-1) As of MySQL 5.7.13, if the audit\_log plugin is already installed from a version of MySQL prior to 5.7.13, uninstall it using the following statement and restart the server before installing the current version:

```
UNINSTALL PLUGIN audit_log;
```

To install MySQL Enterprise Audit, look in the share directory of your MySQL installation and choose the script that is appropriate for your platform. The available scripts differ in the suffix used to refer to the plugin library file:

- audit\_log\_filter\_win\_install.sql: Choose this script for Windows systems that use .dll as the file name suffix.
- audit\_log\_filter\_linux\_install.sql: Choose this script for Linux and similar systems that use .so as the file name suffix.

Run the script as follows. The example here uses the Linux installation script. Make the appropriate substitution for your system.

```
$> mysql -u root -p < audit_log_filter_linux_install.sql
Enter password: (enter root password here)
```

![](_page_33_Picture_8.jpeg)

#### **Note**

Some MySQL versions have introduced changes to the structure of the MySQL Enterprise Audit tables. To ensure that your tables are up to date for upgrades from earlier versions of MySQL 5.7, run mysql\_upgrade --force (which also performs any other needed updates). If you prefer to run the update statements only for the MySQL Enterprise Audit tables, see the following discussion.

As of MySQL 5.7.23, for new MySQL installations, the USER and HOST columns in the audit\_log\_user table used by MySQL Enterprise Audit have definitions that better correspond to the definitions of the User and Host columns in the mysql.user system table. For upgrades to 5.7.23 or higher of an installation for which MySQL Enterprise Audit is already installed, it is recommended that you alter the table definitions as follows:

```
ALTER TABLE mysql.audit_log_user
 DROP FOREIGN KEY audit_log_user_ibfk_1;
ALTER TABLE mysql.audit_log_filter
 ENGINE=InnoDB;
ALTER TABLE mysql.audit_log_filter
 CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;
ALTER TABLE mysql.audit_log_user
 ENGINE=InnoDB;
ALTER TABLE mysql.audit_log_user
 CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;
ALTER TABLE mysql.audit_log_user
 MODIFY COLUMN USER VARCHAR(32);
ALTER TABLE mysql.audit_log_user
 ADD FOREIGN KEY (FILTERNAME) REFERENCES mysql.audit_log_filter(NAME);
```

As of MySQL 5.7.21, for a new installation of MySQL Enterprise Audit, InnoDB is used instead of MyISAM for the audit log tables. For upgrades to 5.7.21 or higher of an installation for which MySQL Enterprise Audit is already installed, it is recommended that you alter the audit log tables to use InnoDB:

```
ALTER TABLE mysql.audit_log_user ENGINE=InnoDB;
ALTER TABLE mysql.audit_log_filter ENGINE=InnoDB;
```

![](_page_33_Picture_15.jpeg)

#### **Note**

To use MySQL Enterprise Audit in the context of source/replica replication, Group Replication, or InnoDB Cluster, you must use MySQL 5.7.21 or higher, and ensure that the audit log tables use InnoDB as just described. Then you must prepare the replica nodes prior to running the installation script on the source node. This is necessary because the INSTALL PLUGIN statement in the script is not replicated.

- 1. On each replica node, extract the INSTALL PLUGIN statement from the installation script and execute it manually.
- 2. On the source node, run the installation script as described previously.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 5.5.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE 'audit%';
+-------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+-------------+---------------+
| audit_log | ACTIVE |
+-------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

After MySQL Enterprise Audit is installed, you can use the [--audit-log](#page-87-1) option for subsequent server startups to control audit\_log plugin activation. For example, to prevent the plugin from being removed at runtime, use this option:

```
[mysqld]
audit-log=FORCE_PLUS_PERMANENT
```

If it is desired to prevent the server from running without the audit plugin, use [--audit-log](#page-87-1) with a value of FORCE or FORCE\_PLUS\_PERMANENT to force server startup to fail if the plugin does not initialize successfully.

![](_page_34_Picture_10.jpeg)

#### **Important**

By default, rule-based audit log filtering logs no auditable events for any users. This differs from legacy audit log behavior (prior to MySQL 5.7.13), which logs all auditable events for all users (see [Section 6.4.5.10, "Legacy Mode Audit Log](#page-79-0) [Filtering"](#page-79-0)). Should you wish to produce log-everything behavior with rule-based filtering, create a simple filter to enable logging and assign it to the default account:

```
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
SELECT audit_log_filter_set_user('%', 'log_all');
```

The filter assigned to % is used for connections from any account that has no explicitly assigned filter (which initially is true for all accounts).

Once installed as just described, MySQL Enterprise Audit remains installed until uninstalled. To remove it, execute the following statements:

```
DROP TABLE IF EXISTS mysql.audit_log_user;
DROP TABLE IF EXISTS mysql.audit_log_filter;
UNINSTALL PLUGIN audit_log;
DROP FUNCTION audit_log_filter_set_filter;
DROP FUNCTION audit_log_filter_remove_filter;
DROP FUNCTION audit_log_filter_set_user;
DROP FUNCTION audit_log_filter_remove_user;
DROP FUNCTION audit_log_filter_flush;
DROP FUNCTION audit_log_encryption_password_get;
DROP FUNCTION audit_log_encryption_password_set;
DROP FUNCTION audit_log_read;
DROP FUNCTION audit_log_read_bookmark;
```