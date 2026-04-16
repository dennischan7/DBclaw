---
source: MySQL 5.7 Reference
title: 00_Overview
---

On Unix and Unix-like systems, a process can be the recipient of signals sent to it by the root system account or the system account that owns the process. Signals can be sent using the kill command. Some command interpreters associate certain key sequences with signals, such as **Control+C** to send a SIGINT signal. This section describes how the MySQL server and client programs respond to signals.

- [Server Response to Signals](#page-28-0)
- [Client Response to Signals](#page-30-0)

# <span id="page-28-0"></span>**Server Response to Signals**

mysqld responds to signals as follows:

- SIGTERM causes the server to shut down. This is like executing a SHUTDOWN statement without having to connect to the server (which for shutdown requires an account that has the SHUTDOWN privilege).
- SIGHUP causes the server to reload the grant tables and to flush tables, logs, the thread cache, and the host cache. These actions are like various forms of the FLUSH statement. Sending the signal enables the flush operations to be performed without having to connect to the server, which requires a MySQL account that has privileges sufficient for those operations. The server also writes a status report to the error log that has this format:

```
Status information:
Current dir: /var/mysql/data/
Running threads: 4 Stack size: 262144
Current locks:
lock: 0x7f742c02c0e0:
lock: 0x2cee2a20:
:
lock: 0x207a080:
Key caches:
default
Buffer_size: 8388608
Block_size: 1024
Division_limit: 100
Age_limit: 300
blocks used: 4
not flushed: 0
w_requests: 0
```

```
writes: 0
r_requests: 8
reads: 4
handler status:
read_key: 13
read_next: 4
read_rnd 0
read_first: 13
write: 1
delete 0
update: 0
Table status:
Opened tables: 121
Open tables: 114
Open files: 18
Open streams: 0
Memory status:
<malloc version="1">
<heap nr="0">
<sizes>
 <size from="17" to="32" total="32" count="1"/>
 <size from="33" to="48" total="96" count="2"/>
 <size from="33" to="33" total="33" count="1"/>
 <size from="97" to="97" total="6014" count="62"/>
 <size from="113" to="113" total="904" count="8"/>
 <size from="193" to="193" total="193" count="1"/>
 <size from="241" to="241" total="241" count="1"/>
 <size from="609" to="609" total="609" count="1"/>
 <size from="16369" to="16369" total="49107" count="3"/>
 <size from="24529" to="24529" total="98116" count="4"/>
 <size from="32689" to="32689" total="32689" count="1"/>
 <unsorted from="241" to="7505" total="7746" count="2"/>
</sizes>
<total type="fast" count="3" size="128"/>
<total type="rest" count="84" size="195652"/>
<system type="current" size="690774016"/>
<system type="max" size="690774016"/>
<aspace type="total" size="690774016"/>
<aspace type="mprotect" size="690774016"/>
</heap>
:
<total type="fast" count="85" size="5520"/>
<total type="rest" count="116" size="316820"/>
<total type="mmap" count="82" size="939954176"/>
<system type="current" size="695717888"/>
<system type="max" size="695717888"/>
<aspace type="total" size="695717888"/>
<aspace type="mprotect" size="695717888"/>
</malloc>
Events status:
LLA = Last Locked At LUA = Last Unlocked At
WOC = Waiting On Condition DL = Data Locked
Event scheduler status:
State : INITIALIZED
Thread id : 0
LLA : n/a:0
LUA : n/a:0
WOC : NO
Workers : 0
Executed : 0
Data locked: NO
Event queue status:
Element count : 0
Data locked : NO
Attempting lock : NO
LLA : init_queue:95
```

```
LUA : init_queue:103
WOC : NO
Next activation : never
```

• SIGINT normally is ignored by the server. Starting the server with the [--gdb](#page-115-0) option installs an interrupt handler for SIGINT for debugging purposes. See Section 5.8.1.4, "Debugging mysqld under gdb".

# <span id="page-30-0"></span>**Client Response to Signals**

MySQL client programs respond to signals as follows:

- The mysql client interprets SIGINT (typically the result of typing **Control+C**) as instruction to interrupt the current statement if there is one, or to cancel any partial input line otherwise. This behavior can be disabled using the --sigint-ignore option to ignore SIGINT signals.
- Client programs that use the MySQL client library block SIGPIPE signals by default. These variations are possible:
  - Client can install their own SIGPIPE handler to override the default behavior. See [Writing C API](https://dev.mysql.com/doc/c-api/5.7/en/c-api-threaded-clients.md) [Threaded Client Programs](https://dev.mysql.com/doc/c-api/5.7/en/c-api-threaded-clients.md).
  - Clients can prevent installation of SIGPIPE handlers by specifying the CLIENT\_IGNORE\_SIGPIPE option to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.md) at connect time. See [mysql\\_real\\_connect\(\).](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.md)

# Chapter 5 MySQL Server Administration

# **Table of Contents**

| 5.1 | The MySQL Server                                                         |     |
|-----|--------------------------------------------------------------------------|-----|
|     | 5.1.1 Configuring the Server                                             | 606 |
|     | 5.1.2 Server Configuration Defaults                                      | 608 |
|     | 5.1.3 Server Option, System Variable, and Status Variable Reference      | 608 |
|     | 5.1.4 Server System Variable Reference                                   | 647 |
|     | 5.1.5 Server Status Variable Reference                                   | 666 |
|     | 5.1.6 Server Command Options                                             | 680 |
|     | 5.1.7 Server System Variables                                            | 706 |
|     | 5.1.8 Using System Variables                                             | 823 |
|     | 5.1.9 Server Status Variables                                            | 840 |
|     | 5.1.10 Server SQL Modes                                                  | 861 |
|     | 5.1.11 Connection Management                                             | 876 |
|     | 5.1.12 IPv6 Support                                                      |     |
|     | 5.1.13 MySQL Server Time Zone Support                                    |     |
|     | 5.1.14 Server-Side Help Support                                          |     |
|     | 5.1.15 Server Tracking of Client Session State                           |     |
|     | 5.1.16 The Server Shutdown Process                                       |     |
| 5.2 | The MySQL Data Directory                                                 |     |
|     | The mysql System Database                                                |     |
|     | MySQL Server Logs                                                        |     |
|     | 5.4.1 Selecting General Query Log and Slow Query Log Output Destinations |     |
|     | 5.4.2 The Error Log                                                      |     |
|     | 5.4.3 The General Query Log                                              |     |
|     | 5.4.4 The Binary Log                                                     |     |
|     | 5.4.5 The Slow Query Log                                                 |     |
|     | 5.4.6 The DDL Log                                                        |     |
|     | 5.4.7 Server Log Maintenance                                             |     |
| 5.5 | MySQL Server Plugins                                                     |     |
| 0.0 | 5.5.1 Installing and Uninstalling Plugins                                |     |
|     | 5.5.2 Obtaining Server Plugin Information                                |     |
|     | 5.5.3 MySQL Enterprise Thread Pool                                       |     |
|     | 5.5.4 The Rewriter Query Rewrite Plugin                                  |     |
|     | 5.5.5 Version Tokens                                                     |     |
|     | 5.5.6 MySQL Plugin Services                                              |     |
| 5.6 | MySQL Server Loadable Functions                                          |     |
|     | 5.6.1 Installing and Uninstalling Loadable Functions                     |     |
|     | 5.6.2 Obtaining Information About Loadable Functions                     |     |
| 5.7 | Running Multiple MySQL Instances on One Machine                          |     |
|     | 5.7.1 Setting Up Multiple Data Directories                               |     |
|     | 5.7.2 Running Multiple MySQL Instances on Windows                        |     |
|     | 5.7.3 Running Multiple MySQL Instances on Unix                           |     |
|     | 5.7.4 Using Client Programs in a Multiple-Server Environment             |     |
| 5.8 | Debugging MySQL                                                          |     |
| 5.5 | 5.8.1 Debugging a MySQL Server                                           |     |
|     | 5.8.2 Debugging a MySQL Client                                           |     |
|     | 5.8.3 The DBUG Package                                                   |     |
|     | 5.8.4 Tracing mysald Using DTrace                                        |     |
|     |                                                                          |     |

MySQL Server (mysqld) is the main program that does most of the work in a MySQL installation. This chapter provides an overview of MySQL Server and covers general server administration:

· Server configuration

- The data directory, particularly the mysql system database
- The server log files
- Management of multiple servers on a single machine

For additional information on administrative topics, see also:

- Chapter 6, Security
- Chapter 7, Backup and Recovery
- Chapter 16, Replication

# <span id="page-33-0"></span>**5.1 The MySQL Server**

mysqld is the MySQL server. The following discussion covers these MySQL server configuration topics:

- Startup options that the server supports. You can specify these options on the command line, through configuration files, or both.
- Server system variables. These variables reflect the current state and values of the startup options, some of which can be modified while the server is running.
- Server status variables. These variables contain counters and statistics about runtime operation.
- How to set the server SQL mode. This setting modifies certain aspects of SQL syntax and semantics, for example for compatibility with code from other database systems, or to control the error handling for particular situations.
- How the server manages client connections.
- Configuring and using IPv6 support.
- Configuring and using time zone support.
- Server-side help capabilities.
- The server shutdown process. There are performance and reliability considerations depending on the type of table (transactional or nontransactional) and whether you use replication.

For listings of MySQL server variables and options that have been added, deprecated, or removed in MySQL 5.7, see Section 1.4, "Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 5.7".

![](_page_33_Picture_20.jpeg)

#### **Note**

Not all storage engines are supported by all MySQL server binaries and configurations. To find out how to determine which storage engines your MySQL server installation supports, see Section 13.7.5.16, "SHOW ENGINES Statement".

# <span id="page-33-1"></span>**5.1.1 Configuring the Server**

The MySQL server, mysqld, has many command options and system variables that can be set at startup to configure its operation. To determine the default command option and system variable values used by the server, execute this command:

```
$> mysqld --verbose --help
```

The command produces a list of all mysqld options and configurable system variables. Its output includes the default option and variable values and looks something like this:

```
abort-slave-event-count 0
allow-suspicious-udfs FALSE
archive ON
auto-increment-increment 1
auto-increment-offset 1
autocommit TRUE
automatic-sp-privileges TRUE
avoid-temporal-upgrade FALSE
back-log 80
basedir /home/jon/bin/mysql-5.7/
...
tmpdir /tmp
transaction-alloc-block-size 8192
transaction-isolation REPEATABLE-READ
transaction-prealloc-size 4096
transaction-read-only FALSE
transaction-write-set-extraction OFF
updatable-views-with-limit YES
validate-user-plugins TRUE
verbose TRUE
wait-timeout 28800
```

To see the current system variable values actually used by the server as it runs, connect to it and execute this statement:

```
mysql> SHOW VARIABLES;
```

To see some statistical and status indicators for a running server, execute this statement:

```
mysql> SHOW STATUS;
```

System variable and status information also is available using the mysqladmin command:

```
$> mysqladmin variables
$> mysqladmin extended-status
```

For a full description of all command options, system variables, and status variables, see these sections:

- [Section 5.1.6, "Server Command Options"](#page-107-0)
- [Section 5.1.7, "Server System Variables"](#page-133-0)
- Section 5.1.9, "Server Status Variables"

More detailed monitoring information is available from the Performance Schema; see Chapter 25, MySQL Performance Schema. In addition, the MySQL sys schema is a set of objects that provides convenient access to data collected by the Performance Schema; see Chapter 26, MySQL sys Schema.

MySQL uses algorithms that are very scalable, so you can usually run with very little memory. However, normally better performance results from giving MySQL more memory.

When tuning a MySQL server, the two most important variables to configure are [key\\_buffer\\_size](#page-167-0) and table\_open\_cache. You should first feel confident that you have these set appropriately before trying to change any other variables.

The following examples indicate some typical variable values for different runtime configurations.

• If you have at least 1-2GB of memory and many tables and want maximum performance with a moderate number of clients, use something like this:

```
$> mysqld_safe --key_buffer_size=384M --table_open_cache=4000 \
 --sort_buffer_size=4M --read_buffer_size=1M &
```

• If you have only 256MB of memory and only a few tables, but you still do a lot of sorting, you can use something like this:

```
$> mysqld_safe --key_buffer_size=64M --sort_buffer_size=1M
```

If there are very many simultaneous connections, swapping problems may occur unless mysqld has been configured to use very little memory for each connection. mysqld performs better if you have enough memory for all connections.

• With little memory and lots of connections, use something like this:

```
$> mysqld_safe --key_buffer_size=512K --sort_buffer_size=100K \
 --read_buffer_size=100K &
```

Or even this:

```
$> mysqld_safe --key_buffer_size=512K --sort_buffer_size=16K \
 --table_open_cache=32 --read_buffer_size=8K \
 --net_buffer_length=1K &
```

If you are performing GROUP BY or ORDER BY operations on tables that are much larger than your available memory, increase the value of read\_rnd\_buffer\_size to speed up the reading of rows following sorting operations.

If you specify an option on the command line for mysqld or mysqld\_safe, it remains in effect only for that invocation of the server. To use the option every time the server runs, put it in an option file. See Section 4.2.2.2, "Using Option Files".

# <span id="page-35-0"></span>**5.1.2 Server Configuration Defaults**

The MySQL server has many operating parameters, which you can change at server startup using command-line options or configuration files (option files). It is also possible to change many parameters at runtime. For general instructions on setting parameters at startup or runtime, see [Section 5.1.6,](#page-107-0) ["Server Command Options"](#page-107-0), and [Section 5.1.7, "Server System Variables".](#page-133-0)

On Windows, MySQL Installer interacts with the user and creates a file named my.ini in the base installation directory as the default option file. If you install on Windows from a Zip archive, you can copy the my-default.ini template file in the base installation directory to my.ini and use the latter as the default option file.

![](_page_35_Picture_12.jpeg)

## **Note**

As of MySQL 5.7.18, my-default.ini is no longer included in or installed by distribution packages.

![](_page_35_Picture_15.jpeg)

#### **Note**

On Windows, the .ini or .cnf option file extension might not be displayed.

After completing the installation process, you can edit the default option file at any time to modify the parameters used by the server. For example, to use a parameter setting in the file that is commented with a # character at the beginning of the line, remove the #, and modify the parameter value if necessary. To disable a setting, either add a # to the beginning of the line or remove it.

For non-Windows platforms, no default option file is created during either the server installation or the data directory initialization process. Create your option file by following the instructions given in Section 4.2.2.2, "Using Option Files". Without an option file, the server just starts with its default settings—see [Section 5.1.2, "Server Configuration Defaults"](#page-35-0) on how to check those settings.

For additional information about option file format and syntax, see Section 4.2.2.2, "Using Option Files".

# <span id="page-35-1"></span>**5.1.3 Server Option, System Variable, and Status Variable Reference**

The following table lists all command-line options, system variables, and status variables applicable within mysqld.

The table lists command-line options (Cmd-line), options valid in configuration files (Option file), server system variables (System Var), and status variables (Status var) in one unified list, with an indication of where each option or variable is valid. If a server option set on the command line or in an option file differs from the name of the corresponding system variable, the variable name is noted immediately below the corresponding option. For system and status variables, the scope of the variable (Var Scope) is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the options and variables. Where appropriate, direct links to further information about the items are provided.

For a version of this table that is specific to NDB Cluster, see Section 21.4.2.5, "NDB Cluster mysqld Option and Variable Reference".

**Table 5.1 Command-Line Option, System Variable, and Status Variable Summary**

| Name                        | Cmd-Line                               | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|----------------------------------------|-------------|------------|------------|-----------|---------|
| abort-slave<br>event-count  | Yes                                    | Yes         |            |            |           |         |
| Aborted_clients             |                                        |             |            | Yes        | Global    | No      |
| Aborted_connects            |                                        |             |            | Yes        | Global    | No      |
| allow<br>suspicious<br>udfs | Yes                                    | Yes         |            |            |           |         |
| ansi                        | Yes                                    | Yes         |            |            |           |         |
| audit-log                   | Yes                                    | Yes         |            |            |           |         |
| audit_log_buffer_size Ye    |                                        | Yes         | Yes        |            | Global    | No      |
| audit_log_compression Yes   |                                        | Yes         | Yes        |            | Global    | No      |
|                             | audit_log_connection_policy<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| audit_log_current_session   |                                        |             | Yes        |            | Both      | No      |
| Audit_log_current_size      |                                        |             |            | Yes        | Global    | No      |
| audit_log_disableYs         |                                        | Yes         | Yes        |            | Global    | Yes     |
| audit_log_encryption Yes    |                                        | Yes         | Yes        |            | Global    | No      |
|                             | Audit_log_event_max_drop_size          |             |            | Yes        | Global    | No      |
| Audit_log_events            |                                        |             |            | Yes        | Global    | No      |
| Audit_log_events_filtered   |                                        |             |            | Yes        | Global    | No      |
| Audit_log_events_lost       |                                        |             |            | Yes        | Global    | No      |
| Audit_log_events_written    |                                        |             |            | Yes        | Global    | No      |
|                             | audit_log_exclude_accounts<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
| audit_log_file              | Yes                                    | Yes         | Yes        |            | Global    | No      |
| audit_log_filter_id         |                                        |             | Yes        |            | Both      | No      |
| audit_log_flush             |                                        |             | Yes        |            | Global    | Yes     |
| audit_log_format Yes        |                                        | Yes         | Yes        |            | Global    | No      |
|                             | audit_log_format_unix_timestamp<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                             | audit_log_include_accounts<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
| audit_log_policyYes         |                                        | Yes         | Yes        |            | Global    | No      |
| audit_log_read_buffer_size  | Yes                                    | Yes         | Yes        |            | Varies    | Varies  |
| audit_log_rotate_on_size    | Yes                                    | Yes         | Yes        |            | Global    | Yes     |
| audit_log_statement_policy  | Yes                                    | Yes         | Yes        |            | Global    | Yes     |
| audit_log_strategy Yes      |                                        | Yes         | Yes        |            | Global    | No      |

| Name                         | Cmd-Line                                         | Option File                                           | System Var | Status Var | Var Scope | Dynamic |
|------------------------------|--------------------------------------------------|-------------------------------------------------------|------------|------------|-----------|---------|
| Audit_log_total_size         |                                                  |                                                       |            | Yes        | Global    | No      |
| Audit_log_write_waits        |                                                  |                                                       |            | Yes        | Global    | No      |
|                              | Yes                                              | authentication_ldap_sasl_auth_method_name<br>Yes      | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_bind_base_dn<br>Yes     | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_bind_root_dn<br>Yes     | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_bind_root_pwd<br>Yes    | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_ca_path<br>Yes          | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | Yes                                              | authentication_ldap_sasl_group_search_attr<br>Yes     | Yes        |            | Global    | Yes     |
|                              | Yes                                              | authentication_ldap_sasl_group_search_filter<br>Yes   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_init_pool_size<br>Yes   | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_log_status<br>Yes       | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_max_pool_size<br>Yes    | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_server_host<br>Yes      | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_server_port<br>Yes      | Yes                                                   | Yes        |            | Global    | Yes     |
| authentication_ldap_sasl_tls | Yes                                              | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_sasl_user_search_attr<br>Yes | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | Yes                                              | authentication_ldap_simple_auth_method_name<br>Yes    | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_bind_base_dn<br>Yes   | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_bind_root_dn<br>Yes   | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_bind_root_pwd<br>Yes  | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_ca_path<br>Yes        | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | Yes                                              | authentication_ldap_simple_group_search_attr<br>Yes   | Yes        |            | Global    | Yes     |
|                              | Yes                                              | authentication_ldap_simple_group_search_filter<br>Yes | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_init_pool_size<br>Yes | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_log_status<br>Yes     | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_max_pool_size<br>Yes  | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_server_host<br>Yes    | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_server_port<br>Yes    | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | authentication_ldap_simple_tls<br>Yes            | Yes                                                   | Yes        |            | Global    | Yes     |
|                              | Yes                                              | authentication_ldap_simple_user_search_attr<br>Yes    | Yes        |            | Global    | Yes     |
|                              | authentication_windows_log_level<br>Yes          | Yes                                                   | Yes        |            | Global    | No      |
|                              | Yes                                              | authentication_windows_use_principal_name<br>Yes      | Yes        |            | Global    | No      |
| auto_generate_certs Yes      |                                                  | Yes                                                   | Yes        |            | Global    | No      |
| auto_increment_increment     | Yes                                              | Yes                                                   | Yes        |            | Both      | Yes     |
| auto_increment_offset Yes    |                                                  | Yes                                                   | Yes        |            | Both      | Yes     |
| autocommit                   | Yes                                              | Yes                                                   | Yes        |            | Both      | Yes     |
| automatic_sp_privileges Yes  |                                                  | Yes                                                   | Yes        |            | Global    | Yes     |
| avoid_temporal_upgrade       | Yes                                              | Yes                                                   | Yes        |            | Global    | Yes     |
| back_log                     | Yes                                              | Yes                                                   | Yes        |            | Global    | No      |
| basedir                      | Yes                                              | Yes                                                   | Yes        |            | Global    | No      |
| big_tables                   | Yes                                              | Yes                                                   | Yes        |            | Both      | Yes     |

| Name                                 | Cmd-Line                                       | Option File                                       | System Var | Status Var | Var Scope | Dynamic |
|--------------------------------------|------------------------------------------------|---------------------------------------------------|------------|------------|-----------|---------|
| bind_address Yes                     |                                                | Yes                                               | Yes        |            | Global    | No      |
| Binlog_cache_disk_use                |                                                |                                                   |            | Yes        | Global    | No      |
| binlog_cache_size Yes                |                                                | Yes                                               | Yes        |            | Global    | Yes     |
| Binlog_cache_use                     |                                                |                                                   |            | Yes        | Global    | No      |
| binlog<br>checksum                   | Yes                                            | Yes                                               |            |            |           |         |
| binlog_checksumYes                   |                                                | Yes                                               | Yes        |            | Global    | Yes     |
|                                      | binlog_direct_non_transactional_updates<br>Yes | Yes                                               | Yes        |            | Both      | Yes     |
| binlog-do-db                         | Yes                                            | Yes                                               |            |            |           |         |
| binlog_error_action Yes              |                                                | Yes                                               | Yes        |            | Global    | Yes     |
| binlog_format Yes                    |                                                | Yes                                               | Yes        |            | Both      | Yes     |
|                                      | binlog_group_commit_sync_delay<br>Yes          | Yes                                               | Yes        |            | Global    | Yes     |
|                                      | Yes                                            | binlog_group_commit_sync_no_delay_count<br>Yes    | Yes        |            | Global    | Yes     |
|                                      | binlog_gtid_simple_recovery<br>Yes             | Yes                                               | Yes        |            | Global    | No      |
| binlog<br>ignore-db                  | Yes                                            | Yes                                               |            |            |           |         |
|                                      | binlog_max_flush_queue_time<br>Yes             | Yes                                               | Yes        |            | Global    | Yes     |
| binlog_order_commits Yes             |                                                | Yes                                               | Yes        |            | Global    | Yes     |
| binlog-row<br>event-max<br>size      | Yes                                            | Yes                                               |            |            |           |         |
| binlog_row_image Yes                 |                                                | Yes                                               | Yes        |            | Both      | Yes     |
|                                      | binlog_rows_query_log_events<br>Yes            | Yes                                               | Yes        |            | Both      | Yes     |
|                                      | Binlog_stmt_cache_disk_use                     |                                                   |            | Yes        | Global    | No      |
| binlog_stmt_cache_size Yes           |                                                | Yes                                               | Yes        |            | Global    | Yes     |
| Binlog_stmt_cache_use                |                                                |                                                   |            | Yes        | Global    | No      |
|                                      | Yes                                            | binlog_transaction_dependency_history_size<br>Yes | Yes        |            | Global    | Yes     |
|                                      | binlog_transaction_dependency_tracking<br>Yes  | Yes                                               | Yes        |            | Global    | Yes     |
| block_encryption_mode Yes            |                                                | Yes                                               | Yes        |            | Both      | Yes     |
| bootstrap                            | Yes                                            | Yes                                               |            |            |           |         |
| bulk_insert_buffer_size Yes          |                                                | Yes                                               | Yes        |            | Both      | Yes     |
| Bytes_received                       |                                                |                                                   |            | Yes        | Both      | No      |
| Bytes_sent                           |                                                |                                                   |            | Yes        | Both      | No      |
| character_set_client                 |                                                |                                                   | Yes        |            | Both      | Yes     |
| character<br>set-client<br>handshake | Yes                                            | Yes                                               |            |            |           |         |
| character_set_connection             |                                                |                                                   | Yes        |            | Both      | Yes     |
| character_set_database<br>(note 1)   |                                                |                                                   | Yes        |            | Both      | Yes     |
| character_set_filesystem             | Yes                                            | Yes                                               | Yes        |            | Both      | Yes     |
| character_set_results                |                                                |                                                   | Yes        |            | Both      | Yes     |
| character_set_server Yes             |                                                | Yes                                               | Yes        |            | Both      | Yes     |

| Name                           | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------------|----------|-------------|------------|------------|-----------|---------|
| character_set_system           |          |             | Yes        |            | Global    | No      |
| character_sets_dir Yes         |          | Yes         | Yes        |            | Global    | No      |
| check_proxy_users Ys           |          | Yes         | Yes        |            | Global    | Yes     |
| chroot                         | Yes      | Yes         |            |            |           |         |
| collation_connection           |          |             | Yes        |            | Both      | Yes     |
| collation_database<br>(note 1) |          |             | Yes        |            | Both      | Yes     |
| collation_serverYes            |          | Yes         | Yes        |            | Both      | Yes     |
| Com_admin_commands             |          |             |            | Yes        | Both      | No      |
| Com_alter_db                   |          |             |            | Yes        | Both      | No      |
| Com_alter_db_upgrade           |          |             |            | Yes        | Both      | No      |
| Com_alter_event                |          |             |            | Yes        | Both      | No      |
| Com_alter_function             |          |             |            | Yes        | Both      | No      |
| Com_alter_procedure            |          |             |            | Yes        | Both      | No      |
| Com_alter_server               |          |             |            | Yes        | Both      | No      |
| Com_alter_table                |          |             |            | Yes        | Both      | No      |
| Com_alter_tablespace           |          |             |            | Yes        | Both      | No      |
| Com_alter_user                 |          |             |            | Yes        | Both      | No      |
| Com_analyze                    |          |             |            | Yes        | Both      | No      |
| Com_assign_to_keycache         |          |             |            | Yes        | Both      | No      |
| Com_begin                      |          |             |            | Yes        | Both      | No      |
| Com_binlog                     |          |             |            | Yes        | Both      | No      |
| Com_call_procedure             |          |             |            | Yes        | Both      | No      |
| Com_change_db                  |          |             |            | Yes        | Both      | No      |
| Com_change_master              |          |             |            | Yes        | Both      | No      |
| Com_change_repl_filter         |          |             |            | Yes        | Both      | No      |
| Com_check                      |          |             |            | Yes        | Both      | No      |
| Com_checksum                   |          |             |            | Yes        | Both      | No      |
| Com_commit                     |          |             |            | Yes        | Both      | No      |
| Com_create_db                  |          |             |            | Yes        | Both      | No      |
| Com_create_event               |          |             |            | Yes        | Both      | No      |
| Com_create_function            |          |             |            | Yes        | Both      | No      |
| Com_create_index               |          |             |            | Yes        | Both      | No      |
| Com_create_procedure           |          |             |            | Yes        | Both      | No      |
| Com_create_server              |          |             |            | Yes        | Both      | No      |
| Com_create_table               |          |             |            | Yes        | Both      | No      |
| Com_create_trigger             |          |             |            | Yes        | Both      | No      |
| Com_create_udf                 |          |             |            | Yes        | Both      | No      |
| Com_create_user                |          |             |            | Yes        | Both      | No      |
| Com_create_view                |          |             |            | Yes        | Both      | No      |
| Com_dealloc_sql                |          |             |            | Yes        | Both      | No      |

| Name                  | Cmd-Line                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------|-----------------------------|-------------|------------|------------|-----------|---------|
| Com_delete            |                             |             |            | Yes        | Both      | No      |
| Com_delete_multi      |                             |             |            | Yes        | Both      | No      |
| Com_do                |                             |             |            | Yes        | Both      | No      |
| Com_drop_db           |                             |             |            | Yes        | Both      | No      |
| Com_drop_event        |                             |             |            | Yes        | Both      | No      |
| Com_drop_function     |                             |             |            | Yes        | Both      | No      |
| Com_drop_index        |                             |             |            | Yes        | Both      | No      |
| Com_drop_procedure    |                             |             |            | Yes        | Both      | No      |
| Com_drop_server       |                             |             |            | Yes        | Both      | No      |
| Com_drop_table        |                             |             |            | Yes        | Both      | No      |
| Com_drop_trigger      |                             |             |            | Yes        | Both      | No      |
| Com_drop_user         |                             |             |            | Yes        | Both      | No      |
| Com_drop_view         |                             |             |            | Yes        | Both      | No      |
| Com_empty_query       |                             |             |            | Yes        | Both      | No      |
| Com_execute_sql       |                             |             |            | Yes        | Both      | No      |
| Com_explain_other     |                             |             |            | Yes        | Both      | No      |
| Com_flush             |                             |             |            | Yes        | Both      | No      |
| Com_get_diagnostics   |                             |             |            | Yes        | Both      | No      |
| Com_grant             |                             |             |            | Yes        | Both      | No      |
|                       | Com_group_replication_start |             |            | Yes        | Global    | No      |
|                       | Com_group_replication_stop  |             |            | Yes        | Global    | No      |
| Com_ha_close          |                             |             |            | Yes        | Both      | No      |
| Com_ha_open           |                             |             |            | Yes        | Both      | No      |
| Com_ha_read           |                             |             |            | Yes        | Both      | No      |
| Com_help              |                             |             |            | Yes        | Both      | No      |
| Com_insert            |                             |             |            | Yes        | Both      | No      |
| Com_insert_select     |                             |             |            | Yes        | Both      | No      |
| Com_install_plugin    |                             |             |            | Yes        | Both      | No      |
| Com_kill              |                             |             |            | Yes        | Both      | No      |
| Com_load              |                             |             |            | Yes        | Both      | No      |
| Com_lock_tables       |                             |             |            | Yes        | Both      | No      |
| Com_optimize          |                             |             |            | Yes        | Both      | No      |
| Com_preload_keys      |                             |             |            | Yes        | Both      | No      |
| Com_prepare_sql       |                             |             |            | Yes        | Both      | No      |
| Com_purge             |                             |             |            | Yes        | Both      | No      |
| Com_purge_before_date |                             |             |            | Yes        | Both      | No      |
| Com_release_savepoint |                             |             |            | Yes        | Both      | No      |
| Com_rename_table      |                             |             |            | Yes        | Both      | No      |
| Com_rename_user       |                             |             |            | Yes        | Both      | No      |
| Com_repair            |                             |             |            | Yes        | Both      | No      |
| Com_replace           |                             |             |            | Yes        | Both      | No      |

| Name                     | Cmd-Line                  | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------|---------------------------|-------------|------------|------------|-----------|---------|
| Com_replace_select       |                           |             |            | Yes        | Both      | No      |
| Com_reset                |                           |             |            | Yes        | Both      | No      |
| Com_resignal             |                           |             |            | Yes        | Both      | No      |
| Com_revoke               |                           |             |            | Yes        | Both      | No      |
| Com_revoke_all           |                           |             |            | Yes        | Both      | No      |
| Com_rollback             |                           |             |            | Yes        | Both      | No      |
|                          | Com_rollback_to_savepoint |             |            | Yes        | Both      | No      |
| Com_savepoint            |                           |             |            | Yes        | Both      | No      |
| Com_select               |                           |             |            | Yes        | Both      | No      |
| Com_set_option           |                           |             |            | Yes        | Both      | No      |
| Com_show_authors         |                           |             |            | Yes        | Both      | No      |
| Com_show_binlog_events   |                           |             |            | Yes        | Both      | No      |
| Com_show_binlogs         |                           |             |            | Yes        | Both      | No      |
| Com_show_charsets        |                           |             |            | Yes        | Both      | No      |
| Com_show_collations      |                           |             |            | Yes        | Both      | No      |
| Com_show_contributors    |                           |             |            | Yes        | Both      | No      |
| Com_show_create_db       |                           |             |            | Yes        | Both      | No      |
| Com_show_create_event    |                           |             |            | Yes        | Both      | No      |
| Com_show_create_func     |                           |             |            | Yes        | Both      | No      |
| Com_show_create_proc     |                           |             |            | Yes        | Both      | No      |
| Com_show_create_table    |                           |             |            | Yes        | Both      | No      |
| Com_show_create_trigger  |                           |             |            | Yes        | Both      | No      |
| Com_show_create_user     |                           |             |            | Yes        | Both      | No      |
| Com_show_databases       |                           |             |            | Yes        | Both      | No      |
| Com_show_engine_logs     |                           |             |            | Yes        | Both      | No      |
| Com_show_engine_mutex    |                           |             |            | Yes        | Both      | No      |
| Com_show_engine_status   |                           |             |            | Yes        | Both      | No      |
| Com_show_errors          |                           |             |            | Yes        | Both      | No      |
| Com_show_events          |                           |             |            | Yes        | Both      | No      |
| Com_show_fields          |                           |             |            | Yes        | Both      | No      |
| Com_show_function_code   |                           |             |            | Yes        | Both      | No      |
| Com_show_function_status |                           |             |            | Yes        | Both      | No      |
| Com_show_grants          |                           |             |            | Yes        | Both      | No      |
| Com_show_keys            |                           |             |            | Yes        | Both      | No      |
| Com_show_master_status   |                           |             |            | Yes        | Both      | No      |
| Com_show_ndb_status      |                           |             |            | Yes        | Both      | No      |
| Com_show_open_tables     |                           |             |            | Yes        | Both      | No      |
| Com_show_plugins         |                           |             |            | Yes        | Both      | No      |
| Com_show_privileges      |                           |             |            | Yes        | Both      | No      |
|                          | Com_show_procedure_code   |             |            | Yes        | Both      | No      |
|                          | Com_show_procedure_status |             |            | Yes        | Both      | No      |

| Name                    | Cmd-Line                                               | Option File | System Var | Status Var | Var Scope | Dynamic |
|-------------------------|--------------------------------------------------------|-------------|------------|------------|-----------|---------|
| Com_show_processlist    |                                                        |             |            | Yes        | Both      | No      |
| Com_show_profile        |                                                        |             |            | Yes        | Both      | No      |
| Com_show_profiles       |                                                        |             |            | Yes        | Both      | No      |
|                         | Com_show_relaylog_events                               |             |            | Yes        | Both      | No      |
| Com_show_slave_hosts    |                                                        |             |            | Yes        | Both      | No      |
| Com_show_slave_status   |                                                        |             |            | Yes        | Both      | No      |
| Com_show_status         |                                                        |             |            | Yes        | Both      | No      |
|                         | Com_show_storage_engines                               |             |            | Yes        | Both      | No      |
| Com_show_table_status   |                                                        |             |            | Yes        | Both      | No      |
| Com_show_tables         |                                                        |             |            | Yes        | Both      | No      |
| Com_show_triggers       |                                                        |             |            | Yes        | Both      | No      |
| Com_show_variables      |                                                        |             |            | Yes        | Both      | No      |
| Com_show_warnings       |                                                        |             |            | Yes        | Both      | No      |
| Com_shutdown            |                                                        |             |            | Yes        | Both      | No      |
| Com_signal              |                                                        |             |            | Yes        | Both      | No      |
| Com_slave_start         |                                                        |             |            | Yes        | Both      | No      |
| Com_slave_stop          |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_close          |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_execute        |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_fetch          |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_prepare        |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_reprepare      |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_reset          |                                                        |             |            | Yes        | Both      | No      |
| Com_stmt_send_long_data |                                                        |             |            | Yes        | Both      | No      |
| Com_truncate            |                                                        |             |            | Yes        | Both      | No      |
| Com_uninstall_plugin    |                                                        |             |            | Yes        | Both      | No      |
| Com_unlock_tables       |                                                        |             |            | Yes        | Both      | No      |
| Com_update              |                                                        |             |            | Yes        | Both      | No      |
| Com_update_multi        |                                                        |             |            | Yes        | Both      | No      |
| Com_xa_commit           |                                                        |             |            | Yes        | Both      | No      |
| Com_xa_end              |                                                        |             |            | Yes        | Both      | No      |
| Com_xa_prepare          |                                                        |             |            | Yes        | Both      | No      |
| Com_xa_recover          |                                                        |             |            | Yes        | Both      | No      |
| Com_xa_rollback         |                                                        |             |            | Yes        | Both      | No      |
| Com_xa_start            |                                                        |             |            | Yes        | Both      | No      |
| completion_typeYes      |                                                        | Yes         | Yes        |            | Both      | Yes     |
| Compression             |                                                        |             |            | Yes        | Session   | No      |
| concurrent_insert Yes   |                                                        | Yes         | Yes        |            | Global    | Yes     |
| connect_timeout Yes     |                                                        | Yes         | Yes        |            | Global    | Yes     |
|                         | Connection_control_delay_generated                     |             |            | Yes        | Global    | No      |
|                         | connection_control_failed_connections_threshold<br>Yes | Yes         | Yes        |            | Global    | Yes     |

| Name                       | Cmd-Line                                       | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|------------------------------------------------|-------------|------------|------------|-----------|---------|
|                            | connection_control_max_connection_delay<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                            | connection_control_min_connection_delay<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| Connection_errors_accept   |                                                |             |            | Yes        | Global    | No      |
| Connection_errors_internal |                                                |             |            | Yes        | Global    | No      |
|                            | Connection_errors_max_connections              |             |            | Yes        | Global    | No      |
|                            | Connection_errors_peer_address                 |             |            | Yes        | Global    | No      |
| Connection_errors_select   |                                                |             |            | Yes        | Global    | No      |
| Connection_errors_tcpwrap  |                                                |             |            | Yes        | Global    | No      |
| Connections                |                                                |             |            | Yes        | Global    | No      |
| console                    | Yes                                            | Yes         |            |            |           |         |
| core-file                  | Yes                                            | Yes         |            |            |           |         |
| core_file                  |                                                |             | Yes        |            | Global    | No      |
| Created_tmp_disk_tables    |                                                |             |            | Yes        | Both      | No      |
| Created_tmp_files          |                                                |             |            | Yes        | Global    | No      |
| Created_tmp_tables         |                                                |             |            | Yes        | Both      | No      |
|                            | daemon_memcached_enable_binlog<br>Yes          | Yes         | Yes        |            | Global    | No      |
|                            | daemon_memcached_engine_lib_name<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                            | daemon_memcached_engine_lib_path<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                            | daemon_memcached_option<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|                            | daemon_memcached_r_batch_size<br>Yes           | Yes         | Yes        |            | Global    | No      |
|                            | daemon_memcached_w_batch_size<br>Yes           | Yes         | Yes        |            | Global    | No      |
| daemonize                  | Yes                                            | Yes         |            |            |           |         |
| datadir                    | Yes                                            | Yes         | Yes        |            | Global    | No      |
| date_format                |                                                |             | Yes        |            | Global    | No      |
| datetime_format            |                                                |             | Yes        |            | Global    | No      |
| debug                      | Yes                                            | Yes         | Yes        |            | Both      | Yes     |
| debug_sync                 |                                                |             | Yes        |            | Session   | Yes     |
| debug-sync<br>timeout      | Yes                                            | Yes         |            |            |           |         |
|                            | default_authentication_plugin<br>Yes           | Yes         | Yes        |            | Global    | No      |
| default_password_lifetime  | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| default_storage_engine Yes |                                                | Yes         | Yes        |            | Both      | Yes     |
| default-time<br>zone       | Yes                                            | Yes         |            |            |           |         |
|                            | default_tmp_storage_engine<br>Yes              | Yes         | Yes        |            | Both      | Yes     |
| default_week_format Yes    |                                                | Yes         | Yes        |            | Both      | Yes     |
| defaults<br>extra-file     | Yes                                            |             |            |            |           |         |
| defaults-file              | Yes                                            |             |            |            |           |         |
| defaults<br>group-suffix   | Yes                                            |             |            |            |           |         |
| delay_key_writeYes         |                                                | Yes         | Yes        |            | Global    | Yes     |

| Name                                 | Cmd-Line                               | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------------------|----------------------------------------|-------------|------------|------------|-----------|---------|
| Delayed_errors                       |                                        |             |            | Yes        | Global    | No      |
| delayed_insert_limit Yes             |                                        | Yes         | Yes        |            | Global    | Yes     |
| Delayed_insert_threads               |                                        |             |            | Yes        | Global    | No      |
| delayed_insert_timeout Yes           |                                        | Yes         | Yes        |            | Global    | Yes     |
| delayed_queue_size Yes               |                                        | Yes         | Yes        |            | Global    | Yes     |
| Delayed_writes                       |                                        |             |            | Yes        | Global    | No      |
| des-key-file                         | Yes                                    | Yes         |            |            |           |         |
| disable<br>partition<br>engine-check | Yes                                    | Yes         |            |            |           |         |
| disabled_storage_engines             | Yes                                    | Yes         | Yes        |            | Global    | No      |
|                                      | disconnect_on_expired_password<br>Yes  | Yes         | Yes        |            | Global    | No      |
| disconnect<br>slave-event<br>count   | Yes                                    | Yes         |            |            |           |         |
| div_precision_increment              | Yes                                    | Yes         | Yes        |            | Both      | Yes     |
| early-plugin<br>load                 | Yes                                    | Yes         |            |            |           |         |
| end_markers_in_json Yes              |                                        | Yes         | Yes        |            | Both      | Yes     |
| enforce_gtid_consistency             | Yes                                    | Yes         | Yes        |            | Global    | Varies  |
| eq_range_index_dive_limit            | Yes                                    | Yes         | Yes        |            | Both      | Yes     |
| error_count                          |                                        |             | Yes        |            | Session   | No      |
| event_schedulerYes                   |                                        | Yes         | Yes        |            | Global    | Yes     |
| exit-info                            | Yes                                    | Yes         |            |            |           |         |
| expire_logs_days Yes                 |                                        | Yes         | Yes        |            | Global    | Yes     |
|                                      | explicit_defaults_for_timestamp<br>Yes | Yes         | Yes        |            | Both      | Yes     |
| external<br>locking                  | Yes                                    | Yes         |            |            |           |         |
| - Variable:<br>skip_external_locking |                                        |             |            |            |           |         |
| external_user                        |                                        |             | Yes        |            | Session   | No      |
| federated                            | Yes                                    | Yes         |            |            |           |         |
| Firewall_access_denied               |                                        |             |            | Yes        | Global    | No      |
| Firewall_access_granted              |                                        |             |            | Yes        | Global    | No      |
|                                      | Firewall_access_suspicious             |             |            | Yes        | Global    | No      |
| Firewall_cached_entries              |                                        |             |            | Yes        | Global    | No      |
| flush                                | Yes                                    | Yes         | Yes        |            | Global    | Yes     |
| Flush_commands                       |                                        |             |            | Yes        | Global    | No      |
| flush_time                           | Yes                                    | Yes         | Yes        |            | Global    | Yes     |
| foreign_key_checks                   |                                        |             | Yes        |            | Both      | Yes     |
| ft_boolean_syntax Yes                |                                        | Yes         | Yes        |            | Global    | Yes     |
| ft_max_word_lenYes                   |                                        | Yes         | Yes        |            | Global    | No      |
| ft_min_word_lenYes                   |                                        | Yes         | Yes        |            | Global    | No      |

| Name                     | Cmd-Line                                                  | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------|-----------------------------------------------------------|-------------|------------|------------|-----------|---------|
| ft_query_expansion_limit | Yes                                                       | Yes         | Yes        |            | Global    | No      |
| ft_stopword_fileYes      |                                                           | Yes         | Yes        |            | Global    | No      |
| gdb                      | Yes                                                       | Yes         |            |            |           |         |
| general_log              | Yes                                                       | Yes         | Yes        |            | Global    | Yes     |
| general_log_fileYes      |                                                           | Yes         | Yes        |            | Global    | Yes     |
| group_concat_max_len Yes |                                                           | Yes         | Yes        |            | Both      | Yes     |
|                          | group_replication_allow_local_disjoint_gtids_join<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_allow_local_lower_version_join<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_auto_increment_increment<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_bootstrap_group<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_components_stop_timeout<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_compression_threshold<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_enforce_update_everywhere_checks<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_exit_state_action<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_flow_control_applier_threshold<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_flow_control_certifier_threshold<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_flow_control_mode<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_force_members<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_group_name<br>Yes                       | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_group_seeds<br>Yes                      | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_gtid_assignment_block_size<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_ip_whitelist<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_local_address<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_member_weight<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_poll_spin_loops<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_primary_member                          |             |            | Yes        | Global    | No      |
|                          | group_replication_recovery_complete_at<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_reconnect_interval<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_retry_count<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_ca<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_capath<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_cert<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_cipher<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_crl<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_crlpath<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_key<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_ssl_verify_server_cert<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_recovery_use_ssl<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_single_primary_mode<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_ssl_mode<br>Yes                         | Yes         | Yes        |            | Global    | Yes     |
|                          | group_replication_start_on_boot<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |

| Name                                           | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|------------------------------------------------|----------|-------------|------------|------------|-----------|---------|
| group_replication_transaction_size_limit       | Yes      | Yes         | Yes        |            | Global    | Yes     |
| group_replication_unreachable_majority_timeout | Yes      | Yes         | Yes        |            | Global    | Yes     |
| gtid_executed                                  |          |             | Yes        |            | Varies    | No      |
| gtid_executed_compression_period               | Yes      | Yes         | Yes        |            | Global    | Yes     |
| gtid_mode                                      | Yes      | Yes         | Yes        |            | Global    | Varies  |
| gtid_next                                      |          |             | Yes        |            | Session   | Yes     |
| gtid_owned                                     |          |             | Yes        |            | Both      | No      |
| gtid_purged                                    |          |             | Yes        |            | Global    | Yes     |
| Handler_commit                                 |          |             |            | Yes        | Both      | No      |
| Handler_delete                                 |          |             |            | Yes        | Both      | No      |
| Handler_discover                               |          |             |            | Yes        | Both      | No      |
| Handler_external_lock                          |          |             |            | Yes        | Both      | No      |
| Handler_mrr_init                               |          |             |            | Yes        | Both      | No      |
| Handler_prepare                                |          |             |            | Yes        | Both      | No      |
| Handler_read_first                             |          |             |            | Yes        | Both      | No      |
| Handler_read_key                               |          |             |            | Yes        | Both      | No      |
| Handler_read_last                              |          |             |            | Yes        | Both      | No      |
| Handler_read_next                              |          |             |            | Yes        | Both      | No      |
| Handler_read_prev                              |          |             |            | Yes        | Both      | No      |
| Handler_read_rnd                               |          |             |            | Yes        | Both      | No      |
| Handler_read_rnd_next                          |          |             |            | Yes        | Both      | No      |
| Handler_rollback                               |          |             |            | Yes        | Both      | No      |
| Handler_savepoint                              |          |             |            | Yes        | Both      | No      |
| Handler_savepoint_rollback                     |          |             |            | Yes        | Both      | No      |
| Handler_update                                 |          |             |            | Yes        | Both      | No      |
| Handler_write                                  |          |             |            | Yes        | Both      | No      |
| have_compress                                  |          |             | Yes        |            | Global    | No      |
| have_crypt                                     |          |             | Yes        |            | Global    | No      |
| have_dynamic_loading                           |          |             | Yes        |            | Global    | No      |
| have_geometry                                  |          |             | Yes        |            | Global    | No      |
| have_openssl                                   |          |             | Yes        |            | Global    | No      |
| have_profiling                                 |          |             | Yes        |            | Global    | No      |
| have_query_cache                               |          |             | Yes        |            | Global    | No      |
| have_rtree_keys                                |          |             | Yes        |            | Global    | No      |
| have_ssl                                       |          |             | Yes        |            | Global    | No      |
| have_statement_timeout                         |          |             | Yes        |            | Global    | No      |
| have_symlink                                   |          |             | Yes        |            | Global    | No      |
| help                                           | Yes      | Yes         |            |            |           |         |
| host_cache_sizeYes                             |          | Yes         | Yes        |            | Global    | Yes     |
| hostname                                       |          |             | Yes        |            | Global    | No      |
| identity                                       |          |             | Yes        |            | Session   | Yes     |

| Name                      | Cmd-Line                                   | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|--------------------------------------------|-------------|------------|------------|-----------|---------|
| ignore_builtin_innodb Yes |                                            | Yes         | Yes        |            | Global    | No      |
| ignore-db-dir             | Yes                                        | Yes         |            |            |           |         |
| ignore_db_dirs            |                                            |             | Yes        |            | Global    | No      |
| init_connect              | Yes                                        | Yes         | Yes        |            | Global    | Yes     |
| init_file                 | Yes                                        | Yes         | Yes        |            | Global    | No      |
| init_slave                | Yes                                        | Yes         | Yes        |            | Global    | Yes     |
| initialize                | Yes                                        | Yes         |            |            |           |         |
| initialize<br>insecure    | Yes                                        | Yes         |            |            |           |         |
| innodb                    | Yes                                        | Yes         |            |            |           |         |
| innodb_adaptive_flushing  | Yes                                        | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_adaptive_flushing_lwm<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_adaptive_hash_index<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_adaptive_hash_index_parts<br>Yes    | Yes         | Yes        |            | Global    | No      |
|                           | innodb_adaptive_max_sleep_delay<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_api_bk_commit_interval<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_api_disable_rowlock<br>Yes          | Yes         | Yes        |            | Global    | No      |
| innodb_api_enable_binlog  | Yes                                        | Yes         | Yes        |            | Global    | No      |
| innodb_api_enable_mdl Yes |                                            | Yes         | Yes        |            | Global    | No      |
| innodb_api_trx_level Yes  |                                            | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_autoextend_increment<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
| innodb_autoinc_lock_mode  | Yes                                        | Yes         | Yes        |            | Global    | No      |
|                           | Innodb_available_undo_logs                 |             |            | Yes        | Global    | No      |
|                           | innodb_background_drop_list_empty<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                           | Innodb_buffer_pool_bytes_data              |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_bytes_dirty             |             |            | Yes        | Global    | No      |
|                           | innodb_buffer_pool_chunk_size<br>Yes       | Yes         | Yes        |            | Global    | No      |
|                           | innodb_buffer_pool_dump_at_shutdown<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_dump_now<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_dump_pct<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | Innodb_buffer_pool_dump_status             |             |            | Yes        | Global    | No      |
|                           | innodb_buffer_pool_filename<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_instances<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                           | innodb_buffer_pool_load_abort<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | innodb_buffer_pool_load_at_startup<br>Yes  | Yes         | Yes        |            | Global    | No      |
|                           | innodb_buffer_pool_load_now<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | Innodb_buffer_pool_load_status             |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_pages_data              |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_pages_dirty             |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_pages_flushed           |             |            | Yes        | Global    | No      |
|                           | Innodb_buffer_pool_pages_free              |             |            | Yes        | Global    | No      |

| Name                       | Cmd-Line                                        | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|-------------------------------------------------|-------------|------------|------------|-----------|---------|
|                            | Innodb_buffer_pool_pages_latched                |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_pages_misc                   |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_pages_total                  |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_ahead                   |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_ahead_evicted           |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_ahead_rnd               |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_read_requests                |             |            | Yes        | Global    | No      |
| Innodb_buffer_pool_reads   |                                                 |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_resize_status                |             |            | Yes        | Global    | No      |
| innodb_buffer_pool_size    | Yes                                             | Yes         | Yes        |            | Global    | Varies  |
|                            | Innodb_buffer_pool_wait_free                    |             |            | Yes        | Global    | No      |
|                            | Innodb_buffer_pool_write_requests               |             |            | Yes        | Global    | No      |
|                            | innodb_change_buffer_max_size<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
| innodb_change_buffering    | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_change_buffering_debug<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_checksum_algorithm<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
| innodb_checksums Yes       |                                                 | Yes         | Yes        |            | Global    | No      |
|                            | innodb_cmp_per_index_enabled<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_commit_concurrency<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
| innodb_compress_debug      | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_compression_failure_threshold_pct<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_compression_level   | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_compression_pad_pct_max<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| innodb_concurrency_tickets | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_data_file_path Yes  |                                                 | Yes         | Yes        |            | Global    | No      |
| Innodb_data_fsyncs         |                                                 |             |            | Yes        | Global    | No      |
| innodb_data_home_dir Yes   |                                                 | Yes         | Yes        |            | Global    | No      |
|                            | Innodb_data_pending_fsyncs                      |             |            | Yes        | Global    | No      |
|                            | Innodb_data_pending_reads                       |             |            | Yes        | Global    | No      |
|                            | Innodb_data_pending_writes                      |             |            | Yes        | Global    | No      |
| Innodb_data_read           |                                                 |             |            | Yes        | Global    | No      |
| Innodb_data_reads          |                                                 |             |            | Yes        | Global    | No      |
| Innodb_data_writes         |                                                 |             |            | Yes        | Global    | No      |
| Innodb_data_written        |                                                 |             |            | Yes        | Global    | No      |
|                            | Innodb_dblwr_pages_written                      |             |            | Yes        | Global    | No      |
| Innodb_dblwr_writes        |                                                 |             |            | Yes        | Global    | No      |
| innodb_deadlock_detect     | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_default_row_format  | Yes                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_disable_resize_buffer_pool_debug<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_disable_sort_file_cache<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| innodb_doublewrite Yes     |                                                 | Yes         | Yes        |            | Global    | No      |

| Name                       | Cmd-Line                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|---------------------------------------------|-------------|------------|------------|-----------|---------|
| innodb_fast_shutdown Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_fil_make_page_dirty_debug<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| innodb_file_format Yes     |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_file_format_check   | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_file_format_max Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_file_per_table Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_fill_factor Yes     |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_flush_log_at_timeout<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_flush_log_at_trx_commit<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
| innodb_flush_method Yes    |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_flush_neighbors Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_flush_sync Yes      |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_flushing_avg_loops  | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_force_load_corrupted<br>Yes          | Yes         | Yes        |            | Global    | No      |
| innodb_force_recovery Yes  |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_ft_aux_table        |                                             |             | Yes        |            | Global    | Yes     |
| innodb_ft_cache_size Yes   |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_ft_enable_diag_print<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_ft_enable_stopword  | Yes                                         | Yes         | Yes        |            | Both      | Yes     |
| innodb_ft_max_token_size   | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_ft_min_token_size   | Yes                                         | Yes         | Yes        |            | Global    | No      |
|                            | innodb_ft_num_word_optimize<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_ft_result_cache_limit<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_ft_server_stopword_table<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
| innodb_ft_sort_pll_degree  | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_ft_total_cache_size | Yes                                         | Yes         | Yes        |            | Global    | No      |
|                            | innodb_ft_user_stopword_table<br>Yes        | Yes         | Yes        |            | Both      | Yes     |
|                            | Innodb_have_atomic_builtins                 |             |            | Yes        | Global    | No      |
| innodb_io_capacity Yes     |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_io_capacity_max     | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
| innodb_large_prefix Ys     |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_limit_optimistic_insert_debug<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_lock_wait_timeout   | Yes                                         | Yes         | Yes        |            | Both      | Yes     |
|                            | innodb_locks_unsafe_for_binlog<br>Yes       | Yes         | Yes        |            | Global    | No      |
| innodb_log_buffer_size Yes |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_log_checkpoint_now<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
| innodb_log_checksums Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_log_compressed_pages<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_log_file_size Yes   |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_log_files_in_group  | Yes                                         | Yes         | Yes        |            | Global    | No      |
|                            | innodb_log_group_home_dir<br>Yes            | Yes         | Yes        |            | Global    | No      |

| Name                       | Cmd-Line                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|---------------------------------------------|-------------|------------|------------|-----------|---------|
| Innodb_log_waits           |                                             |             |            | Yes        | Global    | No      |
|                            | innodb_log_write_ahead_size<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| Innodb_log_write_requests  |                                             |             |            | Yes        | Global    | No      |
| Innodb_log_writes          |                                             |             |            | Yes        | Global    | No      |
| innodb_lru_scan_depth Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_dirty_pages_pct<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_dirty_pages_pct_lwm<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
| innodb_max_purge_lag Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_purge_lag_delay<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_max_undo_log_size<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_merge_threshold_set_all_debug<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_disable Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_enable Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_reset Yes   |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_monitor_reset_all   | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
| Innodb_num_open_files      |                                             |             |            | Yes        | Global    | No      |
| innodb_numa_interleave     | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_old_blocks_pct Yes  |                                             | Yes         | Yes        |            | Global    | Yes     |
| innodb_old_blocks_time Yes |                                             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_online_alter_log_max_size<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| innodb_open_files Yes      |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_optimize_fulltext_only<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
| Innodb_os_log_fsyncs       |                                             |             |            | Yes        | Global    | No      |
|                            | Innodb_os_log_pending_fsyncs                |             |            | Yes        | Global    | No      |
|                            | Innodb_os_log_pending_writes                |             |            | Yes        | Global    | No      |
| Innodb_os_log_written      |                                             |             |            | Yes        | Global    | No      |
| innodb_page_cleaners Yes   |                                             | Yes         | Yes        |            | Global    | No      |
| Innodb_page_size           |                                             |             |            | Yes        | Global    | No      |
| innodb_page_size Yes       |                                             | Yes         | Yes        |            | Global    | No      |
| Innodb_pages_created       |                                             |             |            | Yes        | Global    | No      |
| Innodb_pages_read          |                                             |             |            | Yes        | Global    | No      |
| Innodb_pages_written       |                                             |             |            | Yes        | Global    | No      |
|                            | innodb_print_all_deadlocks<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| innodb_purge_batch_size    | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_purge_rseg_truncate_frequency<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| innodb_purge_threads Yes   |                                             | Yes         | Yes        |            | Global    | No      |
|                            | innodb_random_read_ahead<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                            | innodb_read_ahead_threshold<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_read_io_threads     | Yes                                         | Yes         | Yes        |            | Global    | No      |
| innodb_read_only Yes       |                                             | Yes         | Yes        |            | Global    | No      |
| innodb_replication_delay   | Yes                                         | Yes         | Yes        |            | Global    | Yes     |

| Name                        | Cmd-Line                                       | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|------------------------------------------------|-------------|------------|------------|-----------|---------|
|                             | innodb_rollback_on_timeout<br>Yes              | Yes         | Yes        |            | Global    | No      |
| innodb_rollback_segments    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
|                             | Innodb_row_lock_current_waits                  |             |            | Yes        | Global    | No      |
| Innodb_row_lock_time        |                                                |             |            | Yes        | Global    | No      |
| Innodb_row_lock_time_avg    |                                                |             |            | Yes        | Global    | No      |
|                             | Innodb_row_lock_time_max                       |             |            | Yes        | Global    | No      |
| Innodb_row_lock_waits       |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_deleted         |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_inserted        |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_read            |                                                |             |            | Yes        | Global    | No      |
| Innodb_rows_updated         |                                                |             |            | Yes        | Global    | No      |
|                             | innodb_saved_page_number_debug<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| innodb_sort_buffer_size Yes |                                                | Yes         | Yes        |            | Global    | No      |
| innodb_spin_wait_delay Yes  |                                                | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_auto_recalc    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_include_delete_marked<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_method Yes     |                                                | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_on_metadata    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| innodb_stats_persistent Yes |                                                | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_persistent_sample_pages<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_sample_pages<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_stats_transient_sample_pages<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| innodb<br>status-file       | Yes                                            | Yes         |            |            |           |         |
| innodb_status_output Yes    |                                                | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_status_output_locks<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
| innodb_strict_mode Yes      |                                                | Yes         | Yes        |            | Both      | Yes     |
| innodb_support_xa Yes       |                                                | Yes         | Yes        |            | Both      | Yes     |
| innodb_sync_array_size      | Yes                                            | Yes         | Yes        |            | Global    | No      |
| innodb_sync_debug Yes       |                                                | Yes         | Yes        |            | Global    | No      |
| innodb_sync_spin_loops      | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| innodb_table_locks Yes      |                                                | Yes         | Yes        |            | Both      | Yes     |
|                             | innodb_temp_data_file_path<br>Yes              | Yes         | Yes        |            | Global    | No      |
|                             | innodb_thread_concurrency<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
| innodb_thread_sleep_delay   | Yes                                            | Yes         | Yes        |            | Global    | Yes     |
| innodb_tmpdir Yes           |                                                | Yes         | Yes        |            | Both      | Yes     |
|                             | Innodb_truncated_status_writes                 |             |            | Yes        | Global    | No      |
|                             | innodb_trx_purge_view_update_only_debug<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                             | innodb_trx_rseg_n_slots_debug<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
| innodb_undo_directory Yes   |                                                | Yes         | Yes        |            | Global    | No      |
| innodb_undo_log_truncate    | Yes                                            | Yes         | Yes        |            | Global    | Yes     |

| Name                                | Cmd-Line                                | Option File | System Var | Status Var | Var Scope | Dynamic |
|-------------------------------------|-----------------------------------------|-------------|------------|------------|-----------|---------|
| innodb_undo_logs Yes                |                                         | Yes         | Yes        |            | Global    | Yes     |
| innodb_undo_tablespaces             | Yes                                     | Yes         | Yes        |            | Global    | No      |
| innodb_use_native_aio Yes           |                                         | Yes         | Yes        |            | Global    | No      |
| innodb_version                      |                                         |             | Yes        |            | Global    | No      |
| innodb_write_io_threads             | Yes                                     | Yes         | Yes        |            | Global    | No      |
| insert_id                           |                                         |             | Yes        |            | Session   | Yes     |
| install                             | Yes                                     |             |            |            |           |         |
| install<br>manual                   | Yes                                     |             |            |            |           |         |
| interactive_timeout Yes             |                                         | Yes         | Yes        |            | Both      | Yes     |
|                                     | internal_tmp_disk_storage_engine<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| join_buffer_sizeYes                 |                                         | Yes         | Yes        |            | Both      | Yes     |
| keep_files_on_create Yes            |                                         | Yes         | Yes        |            | Both      | Yes     |
| Key_blocks_not_flushed              |                                         |             |            | Yes        | Global    | No      |
| Key_blocks_unused                   |                                         |             |            | Yes        | Global    | No      |
| Key_blocks_used                     |                                         |             |            | Yes        | Global    | No      |
| key_buffer_sizeYes                  |                                         | Yes         | Yes        |            | Global    | Yes     |
| key_cache_age_threshold             | Yes                                     | Yes         | Yes        |            | Global    | Yes     |
| key_cache_block_size Yes            |                                         | Yes         | Yes        |            | Global    | Yes     |
| key_cache_division_limit            | Yes                                     | Yes         | Yes        |            | Global    | Yes     |
| Key_read_requests                   |                                         |             |            | Yes        | Global    | No      |
| Key_reads                           |                                         |             |            | Yes        | Global    | No      |
| Key_write_requests                  |                                         |             |            | Yes        | Global    | No      |
| Key_writes                          |                                         |             |            | Yes        | Global    | No      |
| keyring_aws_cmk_id Yes              |                                         | Yes         | Yes        |            | Global    | Yes     |
| keyring_aws_conf_file Yes           |                                         | Yes         | Yes        |            | Global    | No      |
| keyring_aws_data_file Yes           |                                         | Yes         | Yes        |            | Global    | No      |
| keyring_aws_region Yes              |                                         | Yes         | Yes        |            | Global    | Yes     |
| keyring_encrypted_file_data         | Yes                                     | Yes         | Yes        |            | Global    | Yes     |
|                                     | keyring_encrypted_file_password<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
| keyring_file_dataYes                |                                         | Yes         | Yes        |            | Global    | Yes     |
| keyring<br>migration<br>destination | Yes                                     | Yes         |            |            |           |         |
| keyring<br>migration<br>host        | Yes                                     | Yes         |            |            |           |         |
| keyring<br>migration<br>password    | Yes                                     | Yes         |            |            |           |         |
| keyring<br>migration<br>port        | Yes                                     | Yes         |            |            |           |         |

| Name                           | Cmd-Line                                     | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------------|----------------------------------------------|-------------|------------|------------|-----------|---------|
| keyring<br>migration<br>socket | Yes                                          | Yes         |            |            |           |         |
| keyring<br>migration<br>source | Yes                                          | Yes         |            |            |           |         |
| keyring<br>migration<br>user   | Yes                                          | Yes         |            |            |           |         |
| keyring_okv_conf_dir Yes       |                                              | Yes         | Yes        |            | Global    | Yes     |
| keyring_operations             |                                              |             | Yes        |            | Global    | Yes     |
| language                       | Yes                                          | Yes         | Yes        |            | Global    | No      |
| large_files_support            |                                              |             | Yes        |            | Global    | No      |
| large_page_size                |                                              |             | Yes        |            | Global    | No      |
| large_pages                    | Yes                                          | Yes         | Yes        |            | Global    | No      |
| last_insert_id                 |                                              |             | Yes        |            | Session   | Yes     |
| Last_query_cost                |                                              |             |            | Yes        | Session   | No      |
| Last_query_partial_plans       |                                              |             |            | Yes        | Session   | No      |
| lc_messages                    | Yes                                          | Yes         | Yes        |            | Both      | Yes     |
| lc_messages_dir Yes            |                                              | Yes         | Yes        |            | Global    | No      |
| lc_time_namesYes               |                                              | Yes         | Yes        |            | Both      | Yes     |
| license                        |                                              |             | Yes        |            | Global    | No      |
| local_infile                   | Yes                                          | Yes         | Yes        |            | Global    | Yes     |
| local-service                  | Yes                                          |             |            |            |           |         |
| lock_wait_timeout Yes          |                                              | Yes         | Yes        |            | Both      | Yes     |
| Locked_connects                |                                              |             |            | Yes        | Global    | No      |
| locked_in_memory               |                                              |             | Yes        |            | Global    | No      |
| log-bin                        | Yes                                          | Yes         |            |            |           |         |
| log_bin                        |                                              |             | Yes        |            | Global    | No      |
| log_bin_basename               |                                              |             | Yes        |            | Global    | No      |
| log_bin_index Yes              |                                              | Yes         | Yes        |            | Global    | No      |
|                                | log_bin_trust_function_creators<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                                | log_bin_use_v1_row_events<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                                | log_builtin_as_identified_by_password<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| log_error                      | Yes                                          | Yes         | Yes        |            | Global    | No      |
| log_error_verbosity Yes        |                                              | Yes         | Yes        |            | Global    | Yes     |
| log-isam                       | Yes                                          | Yes         |            |            |           |         |
| log_output                     | Yes                                          | Yes         | Yes        |            | Global    | Yes     |
|                                | log_queries_not_using_indexes<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
| log-raw                        | Yes                                          | Yes         |            |            |           |         |
| log-short<br>format            | Yes                                          | Yes         |            |            |           |         |
| log_slave_updates Yes          |                                              | Yes         | Yes        |            | Global    | No      |

| Name                       | Cmd-Line                                      | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|-----------------------------------------------|-------------|------------|------------|-----------|---------|
| log_slow_admin_statements  | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
| log_slow_slave_statements  | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
|                            | log_statements_unsafe_for_binlog<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
| log_syslog                 | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
| log_syslog_facility Yes    |                                               | Yes         | Yes        |            | Global    | Yes     |
| log_syslog_include_pid Yes |                                               | Yes         | Yes        |            | Global    | Yes     |
| log_syslog_tagYes          |                                               | Yes         | Yes        |            | Global    | Yes     |
| log-tc                     | Yes                                           | Yes         |            |            |           |         |
| log-tc-size                | Yes                                           | Yes         |            |            |           |         |
|                            | log_throttle_queries_not_using_indexes<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| log_timestampsYes          |                                               | Yes         | Yes        |            | Global    | Yes     |
| log_warnings               | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
| long_query_timeYes         |                                               | Yes         | Yes        |            | Both      | Yes     |
| low_priority_updates Yes   |                                               | Yes         | Yes        |            | Both      | Yes     |
| lower_case_file_system     |                                               |             | Yes        |            | Global    | No      |
| lower_case_table_names     | Yes                                           | Yes         | Yes        |            | Global    | No      |
| master-info<br>file        | Yes                                           | Yes         |            |            |           |         |
| master_info_repository Yes |                                               | Yes         | Yes        |            | Global    | Yes     |
| master-retry<br>count      | Yes                                           | Yes         |            |            |           |         |
| master_verify_checksum     | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
| max_allowed_packet Yes     |                                               | Yes         | Yes        |            | Both      | Yes     |
| max_binlog_cache_size Yes  |                                               | Yes         | Yes        |            | Global    | Yes     |
| max-binlog<br>dump-events  | Yes                                           | Yes         |            |            |           |         |
| max_binlog_sizeYes         |                                               | Yes         | Yes        |            | Global    | Yes     |
|                            | max_binlog_stmt_cache_size<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
| max_connect_errors Yes     |                                               | Yes         | Yes        |            | Global    | Yes     |
| max_connections Yes        |                                               | Yes         | Yes        |            | Global    | Yes     |
| max_delayed_threads Yes    |                                               | Yes         | Yes        |            | Both      | Yes     |
| max_digest_length Yes      |                                               | Yes         | Yes        |            | Global    | No      |
| max_error_count Yes        |                                               | Yes         | Yes        |            | Both      | Yes     |
| max_execution_time Yes     |                                               | Yes         | Yes        |            | Both      | Yes     |
|                            | Max_execution_time_exceeded                   |             |            | Yes        | Both      | No      |
| Max_execution_time_set     |                                               |             |            | Yes        | Both      | No      |
|                            | Max_execution_time_set_failed                 |             |            | Yes        | Both      | No      |
| max_heap_table_size Yes    |                                               | Yes         | Yes        |            | Both      | Yes     |
|                            | max_insert_delayed_threads                    |             | Yes        |            | Both      | Yes     |
| max_join_size Yes          |                                               | Yes         | Yes        |            | Both      | Yes     |
| max_length_for_sort_data   | Yes                                           | Yes         | Yes        |            | Both      | Yes     |
| max_points_in_geometry     | Yes                                           | Yes         | Yes        |            | Both      | Yes     |

| Name                      | Cmd-Line                                 | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|------------------------------------------|-------------|------------|------------|-----------|---------|
| max_prepared_stmt_count   | Yes                                      | Yes         | Yes        |            | Global    | Yes     |
| max_relay_log_size Yes    |                                          | Yes         | Yes        |            | Global    | Yes     |
| max_seeks_for_key Yes     |                                          | Yes         | Yes        |            | Both      | Yes     |
| max_sort_lengthYes        |                                          | Yes         | Yes        |            | Both      | Yes     |
| max_sp_recursion_depth    | Yes                                      | Yes         | Yes        |            | Both      | Yes     |
| max_tmp_tables            |                                          |             | Yes        |            | Both      | Yes     |
| Max_used_connections      |                                          |             |            | Yes        | Global    | No      |
|                           | Max_used_connections_time                |             |            | Yes        | Global    | No      |
| max_user_connections Yes  |                                          | Yes         | Yes        |            | Both      | Yes     |
| max_write_lock_count Yes  |                                          | Yes         | Yes        |            | Global    | Yes     |
| mecab_charset             |                                          |             |            | Yes        | Global    | No      |
| mecab_rc_file Yes         |                                          | Yes         | Yes        |            | Global    | No      |
| memlock                   | Yes                                      | Yes         |            |            |           |         |
| - Variable:               |                                          |             |            |            |           |         |
| locked_in_memory          |                                          |             |            |            |           |         |
| metadata_locks_cache_size | Yes                                      | Yes         | Yes        |            | Global    | No      |
|                           | metadata_locks_hash_instances<br>Yes     | Yes         | Yes        |            | Global    | No      |
| min_examined_row_limit    | Yes                                      | Yes         | Yes        |            | Both      | Yes     |
| multi_range_count Yes     |                                          | Yes         | Yes        |            | Both      | Yes     |
| myisam<br>block-size      | Yes                                      | Yes         |            |            |           |         |
| myisam_data_pointer_size  | Yes                                      | Yes         | Yes        |            | Global    | Yes     |
| myisam_max_sort_file_size | Yes                                      | Yes         | Yes        |            | Global    | Yes     |
| myisam_mmap_size Yes      |                                          | Yes         | Yes        |            | Global    | No      |
| myisam_recover_options    | Yes                                      | Yes         | Yes        |            | Global    | No      |
| myisam_sort_buffer_size   | Yes                                      | Yes         | Yes        |            | Both      | Yes     |
| myisam_stats_method Yes   |                                          | Yes         | Yes        |            | Both      | Yes     |
| myisam_use_mmap Yes       |                                          | Yes         | Yes        |            | Global    | Yes     |
| mysql_firewall_mode Yes   |                                          | Yes         | Yes        |            | Global    | Yes     |
| mysql_firewall_trace Yes  |                                          | Yes         | Yes        |            | Global    | Yes     |
|                           | mysql_native_password_proxy_users<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| mysqlx                    | Yes                                      | Yes         |            |            |           |         |
| Mysqlx_address            |                                          |             |            | Yes        | Global    | No      |
| mysqlx_bind_address Yes   |                                          | Yes         | Yes        |            | Global    | No      |
| Mysqlx_bytes_received     |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_bytes_sent         |                                          |             |            | Yes        | Both      | No      |
| mysqlx_connect_timeout    | Yes                                      | Yes         | Yes        |            | Global    | Yes     |
|                           | Mysqlx_connection_accept_errors          |             |            | Yes        | Both      | No      |
| Mysqlx_connection_errors  |                                          |             |            | Yes        | Both      | No      |
|                           | Mysqlx_connections_accepted              |             |            | Yes        | Global    | No      |
| Mysqlx_connections_closed |                                          |             |            | Yes        | Global    | No      |

| Name                     | Cmd-Line                                 | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------|------------------------------------------|-------------|------------|------------|-----------|---------|
|                          | Mysqlx_connections_rejected              |             |            | Yes        | Global    | No      |
| Mysqlx_crud_create_view  |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_crud_delete       |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_crud_drop_view    |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_crud_find         |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_crud_insert       |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_crud_modify_view  |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_crud_update       |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_errors_sent       |                                          |             |            | Yes        | Both      | No      |
|                          | Mysqlx_errors_unknown_message_type       |             |            | Yes        | Both      | No      |
| Mysqlx_expect_close      |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_expect_open       |                                          |             |            | Yes        | Both      | No      |
|                          | mysqlx_idle_worker_thread_timeout<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_init_error        |                                          |             |            | Yes        | Both      | No      |
|                          | mysqlx_max_allowed_packet<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
| mysqlx_max_connections   | Yes                                      | Yes         | Yes        |            | Global    | Yes     |
|                          | mysqlx_min_worker_threads<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
| Mysqlx_notice_other_sent |                                          |             |            | Yes        | Both      | No      |
|                          | Mysqlx_notice_warning_sent               |             |            | Yes        | Both      | No      |
| Mysqlx_port              |                                          |             |            | Yes        | Global    | No      |
| mysqlx_port              | Yes                                      | Yes         | Yes        |            | Global    | No      |
| mysqlx_port_open_timeout | Yes                                      | Yes         | Yes        |            | Global    | No      |
| Mysqlx_rows_sent         |                                          |             |            | Yes        | Both      | No      |
| Mysqlx_sessions          |                                          |             |            | Yes        | Global    | No      |
|                          | Mysqlx_sessions_accepted                 |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_closed   |                                          |             |            | Yes        | Global    | No      |
|                          | Mysqlx_sessions_fatal_error              |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_killed   |                                          |             |            | Yes        | Global    | No      |
| Mysqlx_sessions_rejected |                                          |             |            | Yes        | Global    | No      |
| Mysqlx_socket            |                                          |             |            | Yes        | Global    | No      |
| mysqlx_socketYes         |                                          | Yes         | Yes        |            | Global    | No      |
|                          | Mysqlx_ssl_accept_renegotiates           |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_accepts       |                                          |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_active        |                                          |             |            | Yes        | Both      | No      |
| mysqlx_ssl_caYes         |                                          | Yes         | Yes        |            | Global    | No      |
| mysqlx_ssl_capath Yes    |                                          | Yes         | Yes        |            | Global    | No      |
| mysqlx_ssl_certYes       |                                          | Yes         | Yes        |            | Global    | No      |
| Mysqlx_ssl_cipher        |                                          |             |            | Yes        | Both      | No      |
| mysqlx_ssl_cipher Yes    |                                          | Yes         | Yes        |            | Global    | No      |
| Mysqlx_ssl_cipher_list   |                                          |             |            | Yes        | Both      | No      |
| mysqlx_ssl_crlYes        |                                          | Yes         | Yes        |            | Global    | No      |

| Name                        | Cmd-Line                                     | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|----------------------------------------------|-------------|------------|------------|-----------|---------|
| mysqlx_ssl_crlpath Yes      |                                              | Yes         | Yes        |            | Global    | No      |
| Mysqlx_ssl_ctx_verify_depth |                                              |             |            | Yes        | Both      | No      |
| Mysqlx_ssl_ctx_verify_mode  |                                              |             |            | Yes        | Both      | No      |
|                             | Mysqlx_ssl_finished_accepts                  |             |            | Yes        | Global    | No      |
| mysqlx_ssl_keyYes           |                                              | Yes         | Yes        |            | Global    | No      |
| Mysqlx_ssl_server_not_after |                                              |             |            | Yes        | Global    | No      |
|                             | Mysqlx_ssl_server_not_before                 |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_verify_depth     |                                              |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_verify_mode      |                                              |             |            | Yes        | Global    | No      |
| Mysqlx_ssl_version          |                                              |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_create_collection                |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_create_collection_index          |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_disable_notices                  |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_drop_collection                  |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_drop_collection_index            |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_enable_notices                   |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_ensure_collection                |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_execute_mysqlx                   |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_execute_sql     |                                              |             |            | Yes        | Both      | No      |
|                             | Mysqlx_stmt_execute_xplugin                  |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_kill_client     |                                              |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_list_clients    |                                              |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_list_notices    |                                              |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_list_objects    |                                              |             |            | Yes        | Both      | No      |
| Mysqlx_stmt_ping            |                                              |             |            | Yes        | Both      | No      |
| Mysqlx_worker_threads       |                                              |             |            | Yes        | Global    | No      |
|                             | Mysqlx_worker_threads_active                 |             |            | Yes        | Global    | No      |
| named_pipe                  | Yes                                          | Yes         | Yes        |            | Global    | No      |
|                             | named_pipe_full_access_group<br>Yes          | Yes         | Yes        |            | Global    | No      |
|                             | ndb_allow_copying_alter_table<br>Yes         | Yes         | Yes        |            | Both      | Yes     |
|                             | Ndb_api_adaptive_send_deferred_count         |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_deferred_count_session |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_deferred_count_slave   |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_forced_count           |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_forced_count_session   |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_forced_count_slave     |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_unforced_count         |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_unforced_count_session |             |            | Yes        | Global    | No      |
|                             | Ndb_api_adaptive_send_unforced_count_slave   |             |            | Yes        | Global    | No      |
|                             | Ndb_api_bytes_received_count                 |             |            | Yes        | Global    | No      |
|                             | Ndb_api_bytes_received_count_session         |             |            | Yes        | Session   | No      |

| Name                      | Cmd-Line                             | Option File                                | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|--------------------------------------|--------------------------------------------|------------|------------|-----------|---------|
|                           | Ndb_api_bytes_received_count_slave   |                                            |            | Yes        | Global    | No      |
| Ndb_api_bytes_sent_count  |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_bytes_sent_count_session     |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_bytes_sent_count_slave       |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_event_bytes_count            |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_event_bytes_count_injector   |                                            |            | Yes        | Global    | No      |
| Ndb_api_event_data_count  |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_event_data_count_injector    |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_event_nondata_count          |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_event_nondata_count_injector |                                            |            | Yes        | Global    | No      |
| Ndb_api_pk_op_count       |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_pk_op_count_session          |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_pk_op_count_slave            |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_pruned_scan_count            |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_pruned_scan_count_session    |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_pruned_scan_count_slave      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_range_scan_count             |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_range_scan_count_session     |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_range_scan_count_slave       |                                            |            | Yes        | Global    | No      |
| Ndb_api_read_row_count    |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_read_row_count_session       |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_read_row_count_slave         |                                            |            | Yes        | Global    | No      |
| Ndb_api_scan_batch_count  |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_scan_batch_count_session     |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_scan_batch_count_slave       |                                            |            | Yes        | Global    | No      |
| Ndb_api_table_scan_count  |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_table_scan_count_session     |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_table_scan_count_slave       |                                            |            | Yes        | Global    | No      |
| Ndb_api_trans_abort_count |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_trans_abort_count_session    |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_trans_abort_count_slave      |                                            |            | Yes        | Global    | No      |
| Ndb_api_trans_close_count |                                      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_trans_close_count_session    |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_trans_close_count_slave      |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_trans_commit_count           |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_trans_commit_count_session   |                                            |            | Yes        | Session   | No      |
|                           | Ndb_api_trans_commit_count_slave     |                                            |            | Yes        | Global    | No      |
|                           | Ndb_api_trans_local_read_row_count   |                                            |            | Yes        | Global    | No      |
|                           |                                      | Ndb_api_trans_local_read_row_count_session |            | Yes        | Session   | No      |
|                           |                                      | Ndb_api_trans_local_read_row_count_slave   |            | Yes        | Global    | No      |
| Ndb_api_trans_start_count |                                      |                                            |            | Yes        | Global    | No      |

| Name                       | Cmd-Line                                   | Option File                              | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|--------------------------------------------|------------------------------------------|------------|------------|-----------|---------|
|                            | Ndb_api_trans_start_count_session          |                                          |            | Yes        | Session   | No      |
|                            | Ndb_api_trans_start_count_slave            |                                          |            | Yes        | Global    | No      |
| Ndb_api_uk_op_count        |                                            |                                          |            | Yes        | Global    | No      |
|                            | Ndb_api_uk_op_count_session                |                                          |            | Yes        | Session   | No      |
|                            | Ndb_api_uk_op_count_slave                  |                                          |            | Yes        | Global    | No      |
|                            | Ndb_api_wait_exec_complete_count           |                                          |            | Yes        | Global    | No      |
|                            |                                            | Ndb_api_wait_exec_complete_count_session |            | Yes        | Session   | No      |
|                            | Ndb_api_wait_exec_complete_count_slave     |                                          |            | Yes        | Global    | No      |
|                            | Ndb_api_wait_meta_request_count            |                                          |            | Yes        | Global    | No      |
|                            |                                            | Ndb_api_wait_meta_request_count_session  |            | Yes        | Session   | No      |
|                            | Ndb_api_wait_meta_request_count_slave      |                                          |            | Yes        | Global    | No      |
| Ndb_api_wait_nanos_count   |                                            |                                          |            | Yes        | Global    | No      |
|                            | Ndb_api_wait_nanos_count_session           |                                          |            | Yes        | Session   | No      |
|                            | Ndb_api_wait_nanos_count_slave             |                                          |            | Yes        | Global    | No      |
|                            | Ndb_api_wait_scan_result_count             |                                          |            | Yes        | Global    | No      |
|                            | Ndb_api_wait_scan_result_count_session     |                                          |            | Yes        | Session   | No      |
|                            | Ndb_api_wait_scan_result_count_slave       |                                          |            | Yes        | Global    | No      |
|                            | ndb_autoincrement_prefetch_sz<br>Yes       | Yes                                      | Yes        |            | Both      | Yes     |
| ndb_batch_sizeYes          |                                            | Yes                                      | Yes        |            | Both      | Yes     |
|                            | ndb_blob_read_batch_bytes<br>Yes           | Yes                                      | Yes        |            | Both      | Yes     |
|                            | ndb_blob_write_batch_bytes<br>Yes          | Yes                                      | Yes        |            | Both      | Yes     |
| ndb_cache_check_time Yes   |                                            | Yes                                      | Yes        |            | Global    | Yes     |
| ndb_clear_apply_status Yes |                                            |                                          | Yes        |            | Global    | Yes     |
|                            | ndb_cluster_connection_pool<br>Yes         | Yes                                      | Yes        |            | Global    | No      |
|                            | ndb_cluster_connection_pool_nodeids<br>Yes | Yes                                      | Yes        |            | Global    | No      |
| Ndb_cluster_node_id        |                                            |                                          |            | Yes        | Global    | No      |
| Ndb_config_from_host       |                                            |                                          |            | Yes        | Both      | No      |
| Ndb_config_from_port       |                                            |                                          |            | Yes        | Both      | No      |
| Ndb_conflict_fn_epoch      |                                            |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_fn_epoch_trans                |                                          |            | Yes        | Global    | No      |
| Ndb_conflict_fn_epoch2     |                                            |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_fn_epoch2_trans               |                                          |            | Yes        | Global    | No      |
| Ndb_conflict_fn_max        |                                            |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_fn_max_del_win                |                                          |            | Yes        | Global    | No      |
| Ndb_conflict_fn_old        |                                            |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_last_conflict_epoch           |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_last_stable_epoch             |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_reflected_op_discard_count    |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_reflected_op_prepare_count    |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_refresh_op_count              |                                          |            | Yes        | Global    | No      |
|                            | Ndb_conflict_trans_conflict_commit_count   |                                          |            | Yes        | Global    | No      |

| Ndb_conflict_trans_detect_iter_count<br>Yes<br>Global<br>No<br>Ndb_conflict_trans_reject_count<br>Yes<br>Global<br>No<br>Ndb_conflict_trans_row_conflict_count<br>Yes<br>Global<br>No<br>Ndb_conflict_trans_row_reject_count<br>Yes<br>Global<br>No<br>ndb<br>Yes<br>Yes<br>connectstring<br>ndb_data_node_neighbour<br>Yes<br>Yes<br>Yes<br>Global<br>Yes<br>ndb_default_column_format<br>Yes<br>Yes<br>Yes<br>Global<br>Yes<br>ndb_default_column_format<br>Yes<br>Yes<br>Yes<br>Global<br>Yes<br>ndb_deferred_constraints<br>Yes<br>Yes<br>Yes<br>Both<br>Yes<br>ndb_deferred_constraints<br>Yes<br>Yes<br>Yes<br>Both<br>Yes<br>ndb_distributionYes<br>Yes<br>Yes<br>Global<br>Yes<br>ndb_distributionYes<br>Yes<br>Yes<br>Global<br>Yes<br>Ndb_epoch_delete_delete_count<br>Yes<br>Global<br>No<br>ndb_eventbuffer_free_percent<br>Yes<br>Yes<br>Yes<br>Global<br>Yes<br>ndb_eventbuffer_max_alloc<br>Yes<br>Yes<br>Yes<br>Global<br>Yes<br>Ndb_execute_count<br>Yes<br>Global<br>No<br>ndb_extra_logging Yes<br>Yes<br>Yes<br>Global<br>Yes<br>ndb_force_sendYes<br>Yes<br>Yes<br>Both<br>Yes<br>ndb_fully_replicated Yes<br>Yes<br>Yes<br>Both<br>Yes<br>ndb_index_stat_enable Yes<br>Yes<br>Yes<br>Both<br>Yes<br>ndb_index_stat_option Yes<br>Yes<br>Yes<br>Both<br>Yes<br>ndb_join_pushdown<br>Yes<br>Both<br>Yes<br>Ndb_last_commit_epoch_server<br>Yes<br>Global<br>No<br>Ndb_last_commit_epoch_session<br>Yes<br>Session<br>No<br>ndb_log_apply_status Yes<br>Yes<br>Yes<br>Global<br>No<br>ndb_log_apply_status Yes<br>Yes<br>Yes<br>Global<br>No<br>ndb_log_bin<br>Yes<br>Yes<br>Both<br>No<br>ndb_log_binlog_index Yes<br>Yes<br>Global<br>Yes<br>ndb_log_empty_epochs Yes<br>Yes<br>Yes<br>Global<br>Yes | Dynamic |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
| ndb_log_empty_epochs Yes<br>Yes<br>Yes<br>Global<br>Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |         |
| ndb_log_empty_update Yes<br>Yes<br>Yes<br>Global<br>Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |         |
| ndb_log_empty_update Yes<br>Yes<br>Yes<br>Global<br>Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |         |
| ndb_log_exclusive_reads<br>Yes<br>Yes<br>Yes<br>Both<br>Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |         |
| ndb_log_exclusive_reads<br>Yes<br>Yes<br>Yes<br>Both<br>Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |         |
| ndb_log_fail_terminate Yes<br>Yes<br>Yes<br>Global<br>No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |
| ndb_log_orig<br>Yes<br>Yes<br>Yes<br>Global<br>No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |         |
| ndb_log_orig<br>Yes<br>Yes<br>Yes<br>Global<br>No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |         |
| ndb_log_transaction_id Yes<br>Yes<br>Yes<br>Global<br>No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |
| ndb_log_transaction_id<br>Yes<br>Global<br>No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |         |
| ndb_log_update_as_write<br>Yes<br>Yes<br>Yes<br>Global<br>Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |         |

| Name                                      | Cmd-Line                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|-------------------------------------------|---------------------------------------------|-------------|------------|------------|-----------|---------|
| ndb_log_update_minimal                    | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
| ndb_log_updated_only Yes                  |                                             | Yes         | Yes        |            | Global    | Yes     |
| ndb-mgmd<br>host                          | Yes                                         | Yes         |            |            |           |         |
| ndb_nodeid                                | Yes                                         | Yes         |            | Yes        | Global    | No      |
|                                           | Ndb_number_of_data_nodes                    |             |            | Yes        | Global    | No      |
| ndb_optimization_delay Yes                |                                             | Yes         | Yes        |            | Global    | Yes     |
|                                           | ndb_optimized_node_selection<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                                           | ndb_optimized_node_selection<br>Yes         | Yes         | Yes        |            | Global    | No      |
| Ndb_pruned_scan_count                     |                                             |             |            | Yes        | Global    | No      |
|                                           | Ndb_pushed_queries_defined                  |             |            | Yes        | Global    | No      |
|                                           | Ndb_pushed_queries_dropped                  |             |            | Yes        | Global    | No      |
|                                           | Ndb_pushed_queries_executed                 |             |            | Yes        | Global    | No      |
| Ndb_pushed_reads                          |                                             |             |            | Yes        | Global    | No      |
| ndb_read_backup Yes                       |                                             | Yes         | Yes        |            | Global    | Yes     |
|                                           | ndb_recv_thread_activation_threshold<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                                           | ndb_recv_thread_cpu_mask<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                                           | ndb_report_thresh_binlog_epoch_slip<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|                                           | ndb_report_thresh_binlog_mem_usage<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
| ndb_row_checksum                          |                                             |             | Yes        |            | Both      | Yes     |
| Ndb_scan_count                            |                                             |             |            | Yes        | Global    | No      |
|                                           | ndb_show_foreign_key_mock_tables<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
| ndb_slave_conflict_role Yes               |                                             | Yes         | Yes        |            | Global    | Yes     |
|                                           | Ndb_slave_max_replicated_epoch              |             |            | Yes        | Global    | No      |
| Ndb_system_name                           |                                             |             | Yes        |            | Global    | No      |
| ndb_table_no_logging                      |                                             |             | Yes        |            | Session   | Yes     |
| ndb_table_temporary                       |                                             |             | Yes        |            | Session   | Yes     |
| ndb-transid<br>mysql<br>connection<br>map | Yes                                         |             |            |            |           |         |
|                                           | ndb_use_copying_alter_table                 |             | Yes        |            | Both      | No      |
| ndb_use_exact_count                       |                                             |             | Yes        |            | Both      | Yes     |
| ndb_use_transactions Yes                  |                                             | Yes         | Yes        |            | Both      | Yes     |
| ndb_version                               |                                             |             | Yes        |            | Global    | No      |
| ndb_version_string                        |                                             |             | Yes        |            | Global    | No      |
| ndb_wait_connected Yes                    |                                             | Yes         | Yes        |            | Global    | No      |
| ndb_wait_setupYes                         |                                             | Yes         | Yes        |            | Global    | No      |
| ndbcluster                                | Yes                                         | Yes         |            |            |           |         |
| ndbinfo_database                          |                                             |             | Yes        |            | Global    | No      |
| ndbinfo_max_bytes Yes                     |                                             |             | Yes        |            | Both      | Yes     |
| ndbinfo_max_rows Yes                      |                                             |             | Yes        |            | Both      | Yes     |

| Name                       | Cmd-Line                                           | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|----------------------------------------------------|-------------|------------|------------|-----------|---------|
| ndbinfo_offline            |                                                    |             | Yes        |            | Global    | Yes     |
| ndbinfo_show_hidden Yes    |                                                    |             | Yes        |            | Both      | Yes     |
| ndbinfo_table_prefix       |                                                    |             | Yes        |            | Global    | No      |
| ndbinfo_version            |                                                    |             | Yes        |            | Global    | No      |
| net_buffer_lengthYes       |                                                    | Yes         | Yes        |            | Both      | Yes     |
| net_read_timeout Yes       |                                                    | Yes         | Yes        |            | Both      | Yes     |
| net_retry_countYes         |                                                    | Yes         | Yes        |            | Both      | Yes     |
| net_write_timeout Yes      |                                                    | Yes         | Yes        |            | Both      | Yes     |
| new                        | Yes                                                | Yes         | Yes        |            | Both      | Yes     |
| ngram_token_size Yes       |                                                    | Yes         | Yes        |            | Global    | No      |
| no-defaults                | Yes                                                |             |            |            |           |         |
|                            | Not_flushed_delayed_rows                           |             |            | Yes        | Global    | No      |
| offline_mode               | Yes                                                | Yes         | Yes        |            | Global    | Yes     |
| old                        | Yes                                                | Yes         | Yes        |            | Global    | No      |
| old_alter_tableYes         |                                                    | Yes         | Yes        |            | Both      | Yes     |
| old_passwordsYes           |                                                    | Yes         | Yes        |            | Both      | Yes     |
| old-style<br>user-limits   | Yes                                                | Yes         |            |            |           |         |
|                            | Ongoing_anonymous_gtid_violating_transaction_count |             |            | Yes        | Global    | No      |
|                            | Ongoing_anonymous_transaction_count                |             |            | Yes        | Global    | No      |
|                            | Ongoing_automatic_gtid_violating_transaction_count |             |            | Yes        | Global    | No      |
| Open_files                 |                                                    |             |            | Yes        | Global    | No      |
| open_files_limitYes        |                                                    | Yes         | Yes        |            | Global    | No      |
| Open_streams               |                                                    |             |            | Yes        | Global    | No      |
| Open_table_definitions     |                                                    |             |            | Yes        | Global    | No      |
| Open_tables                |                                                    |             |            | Yes        | Both      | No      |
| Opened_files               |                                                    |             |            | Yes        | Global    | No      |
| Opened_table_definitions   |                                                    |             |            | Yes        | Both      | No      |
| Opened_tables              |                                                    |             |            | Yes        | Both      | No      |
| optimizer_prune_level Yes  |                                                    | Yes         | Yes        |            | Both      | Yes     |
| optimizer_search_depth Yes |                                                    | Yes         | Yes        |            | Both      | Yes     |
| optimizer_switchYes        |                                                    | Yes         | Yes        |            | Both      | Yes     |
| optimizer_traceYes         |                                                    | Yes         | Yes        |            | Both      | Yes     |
| optimizer_trace_features   | Yes                                                | Yes         | Yes        |            | Both      | Yes     |
| optimizer_trace_limit Yes  |                                                    | Yes         | Yes        |            | Both      | Yes     |
|                            | optimizer_trace_max_mem_size<br>Yes                | Yes         | Yes        |            | Both      | Yes     |
| optimizer_trace_offset Yes |                                                    | Yes         | Yes        |            | Both      | Yes     |
| parser_max_mem_size Yes    |                                                    | Yes         | Yes        |            | Both      | Yes     |
| partition                  | Yes                                                | Yes         |            |            |           |         |
| performance_schema Yes     |                                                    | Yes         | Yes        |            | Global    | No      |
|                            | Performance_schema_accounts_lost                   |             |            | Yes        | Global    | No      |

| Name                                                                      | Cmd-Line                                | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------------------------------------------------------|-----------------------------------------|-------------|------------|------------|-----------|---------|
|                                                                           | performance_schema_accounts_size<br>Yes | Yes         | Yes        |            | Global    | No      |
|                                                                           | Performance_schema_cond_classes_lost    |             |            | Yes        | Global    | No      |
|                                                                           | Performance_schema_cond_instances_lost  |             |            | Yes        | Global    | No      |
| performance<br>schema<br>consumer<br>events<br>stages<br>current          | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>stages<br>history          | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>stages<br>history-long     | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>current      | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>history      | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>history-long | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>transactions<br>current    | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>transactions<br>history    | Yes                                     | Yes         |            |            |           |         |

| Name                                                                        | Cmd-Line                                                   | Option File | System Var                                                      | Status Var | Var Scope | Dynamic |
|-----------------------------------------------------------------------------|------------------------------------------------------------|-------------|-----------------------------------------------------------------|------------|-----------|---------|
| performance<br>schema<br>consumer<br>events<br>transactions<br>history-long | Yes                                                        | Yes         |                                                                 |            |           |         |
| performance<br>schema<br>consumer<br>events-waits<br>current                | Yes                                                        | Yes         |                                                                 |            |           |         |
| performance<br>schema<br>consumer<br>events-waits<br>history                | Yes                                                        | Yes         |                                                                 |            |           |         |
| performance<br>schema<br>consumer<br>events-waits<br>history-long           | Yes                                                        | Yes         |                                                                 |            |           |         |
| performance<br>schema<br>consumer<br>global<br>instrumentation              | Yes                                                        | Yes         |                                                                 |            |           |         |
| performance<br>schema<br>consumer<br>statements<br>digest                   | Yes                                                        | Yes         |                                                                 |            |           |         |
| performance<br>schema<br>consumer<br>thread<br>instrumentation              | Yes                                                        | Yes         |                                                                 |            |           |         |
|                                                                             | Performance_schema_digest_lost                             |             |                                                                 | Yes        | Global    | No      |
|                                                                             | performance_schema_digests_size<br>Yes                     | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | performance_schema_events_stages_history_long_size<br>Yes  | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | performance_schema_events_stages_history_size<br>Yes       | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | Yes                                                        | Yes         | performance_schema_events_statements_history_long_size<br>Yes   |            | Global    | No      |
|                                                                             | performance_schema_events_statements_history_size<br>Yes   | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | Yes                                                        | Yes         | performance_schema_events_transactions_history_long_size<br>Yes |            | Global    | No      |
|                                                                             | performance_schema_events_transactions_history_size<br>Yes | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | performance_schema_events_waits_history_long_size<br>Yes   | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | performance_schema_events_waits_history_size<br>Yes        | Yes         | Yes                                                             |            | Global    | No      |
|                                                                             | Performance_schema_file_classes_lost                       |             |                                                                 | Yes        | Global    | No      |
|                                                                             | Performance_schema_file_handles_lost                       |             |                                                                 | Yes        | Global    | No      |
|                                                                             | Performance_schema_file_instances_lost                     |             |                                                                 | Yes        | Global    | No      |

| Name                                | Cmd-Line                                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|-------------------------------------|-------------------------------------------------------------|-------------|------------|------------|-----------|---------|
|                                     | Performance_schema_hosts_lost                               |             |            | Yes        | Global    | No      |
|                                     | performance_schema_hosts_size<br>Yes                        | Yes         | Yes        |            | Global    | No      |
|                                     | Performance_schema_index_stat_lost                          |             |            | Yes        | Global    | No      |
| performance<br>schema<br>instrument | Yes                                                         | Yes         |            |            |           |         |
|                                     | Performance_schema_locker_lost                              |             |            | Yes        | Global    | No      |
|                                     | performance_schema_max_cond_classes<br>Yes                  | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_cond_instances<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_digest_length<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_file_classes<br>Yes                  | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_file_handles<br>Yes                  | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_file_instances<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_index_stat<br>Yes                    | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_memory_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_metadata_locks<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_mutex_classes<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_mutex_instances<br>Yes               | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_prepared_statements_instances<br>Yes | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_program_instances<br>Yes             | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_rwlock_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_rwlock_instances<br>Yes              | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_socket_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_socket_instances<br>Yes              | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_sql_text_length<br>Yes               | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_stage_classes<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_statement_classes<br>Yes             | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_statement_stack<br>Yes               | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_table_handles<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_table_instances<br>Yes               | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_table_lock_stat<br>Yes               | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_thread_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|                                     | performance_schema_max_thread_instances<br>Yes              | Yes         | Yes        |            | Global    | No      |
|                                     | Performance_schema_memory_classes_lost                      |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_metadata_lock_lost                       |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_mutex_classes_lost                       |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_mutex_instances_lost                     |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_nested_statement_lost                    |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_prepared_statements_lost                 |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_program_lost                             |             |            | Yes        | Global    | No      |
|                                     | Performance_schema_rwlock_classes_lost                      |             |            | Yes        | Global    | No      |

| Name                       | Cmd-Line                                             | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|------------------------------------------------------|-------------|------------|------------|-----------|---------|
|                            | Performance_schema_rwlock_instances_lost             |             |            | Yes        | Global    | No      |
|                            | Performance_schema_session_connect_attrs_lost        |             |            | Yes        | Global    | No      |
|                            | performance_schema_session_connect_attrs_size<br>Yes | Yes         | Yes        |            | Global    | No      |
|                            | performance_schema_setup_actors_size<br>Yes          | Yes         | Yes        |            | Global    | No      |
|                            | performance_schema_setup_objects_size<br>Yes         | Yes         | Yes        |            | Global    | No      |
|                            | performance_schema_show_processlist<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                            | Performance_schema_socket_classes_lost               |             |            | Yes        | Global    | No      |
|                            | Performance_schema_socket_instances_lost             |             |            | Yes        | Global    | No      |
|                            | Performance_schema_stage_classes_lost                |             |            | Yes        | Global    | No      |
|                            | Performance_schema_statement_classes_lost            |             |            | Yes        | Global    | No      |
|                            | Performance_schema_table_handles_lost                |             |            | Yes        | Global    | No      |
|                            | Performance_schema_table_instances_lost              |             |            | Yes        | Global    | No      |
|                            | Performance_schema_table_lock_stat_lost              |             |            | Yes        | Global    | No      |
|                            | Performance_schema_thread_classes_lost               |             |            | Yes        | Global    | No      |
|                            | Performance_schema_thread_instances_lost             |             |            | Yes        | Global    | No      |
|                            | Performance_schema_users_lost                        |             |            | Yes        | Global    | No      |
|                            | performance_schema_users_size<br>Yes                 | Yes         | Yes        |            | Global    | No      |
| pid_file                   | Yes                                                  | Yes         | Yes        |            | Global    | No      |
| plugin_dir                 | Yes                                                  | Yes         | Yes        |            | Global    | No      |
| plugin-load                | Yes                                                  | Yes         |            |            |           |         |
| plugin-load<br>add         | Yes                                                  | Yes         |            |            |           |         |
| plugin-xxx                 | Yes                                                  | Yes         |            |            |           |         |
| port                       | Yes                                                  | Yes         | Yes        |            | Global    | No      |
| port-open<br>timeout       | Yes                                                  | Yes         |            |            |           |         |
| preload_buffer_size Yes    |                                                      | Yes         | Yes        |            | Both      | Yes     |
| Prepared_stmt_count        |                                                      |             |            | Yes        | Global    | No      |
| print-defaults             | Yes                                                  |             |            |            |           |         |
| profiling                  |                                                      |             | Yes        |            | Both      | Yes     |
| profiling_history_size Yes |                                                      | Yes         | Yes        |            | Both      | Yes     |
| protocol_version           |                                                      |             | Yes        |            | Global    | No      |
| proxy_user                 |                                                      |             | Yes        |            | Session   | No      |
| pseudo_slave_mode          |                                                      |             | Yes        |            | Session   | Yes     |
| pseudo_thread_id           |                                                      |             | Yes        |            | Session   | Yes     |
| Qcache_free_blocks         |                                                      |             |            | Yes        | Global    | No      |
| Qcache_free_memory         |                                                      |             |            | Yes        | Global    | No      |
| Qcache_hits                |                                                      |             |            | Yes        | Global    | No      |
| Qcache_inserts             |                                                      |             |            | Yes        | Global    | No      |
| Qcache_lowmem_prunes       |                                                      |             |            | Yes        | Global    | No      |
| Qcache_not_cached          |                                                      |             |            | Yes        | Global    | No      |

| Name                           | Cmd-Line                            | Option File | System Var | Status Var | Var Scope | Dynamic |
|--------------------------------|-------------------------------------|-------------|------------|------------|-----------|---------|
| Qcache_queries_in_cache        |                                     |             |            | Yes        | Global    | No      |
| Qcache_total_blocks            |                                     |             |            | Yes        | Global    | No      |
| Queries                        |                                     |             |            | Yes        | Both      | No      |
| query_alloc_block_size Yes     |                                     | Yes         | Yes        |            | Both      | Yes     |
| query_cache_limit Yes          |                                     | Yes         | Yes        |            | Global    | Yes     |
| query_cache_min_res_unit       | Yes                                 | Yes         | Yes        |            | Global    | Yes     |
| query_cache_size Yes           |                                     | Yes         | Yes        |            | Global    | Yes     |
| query_cache_type Yes           |                                     | Yes         | Yes        |            | Both      | Yes     |
|                                | query_cache_wlock_invalidate<br>Yes | Yes         | Yes        |            | Both      | Yes     |
| query_prealloc_size Yes        |                                     | Yes         | Yes        |            | Both      | Yes     |
| Questions                      |                                     |             |            | Yes        | Both      | No      |
| rand_seed1                     |                                     |             | Yes        |            | Session   | Yes     |
| rand_seed2                     |                                     |             | Yes        |            | Session   | Yes     |
| range_alloc_block_size Yes     |                                     | Yes         | Yes        |            | Both      | Yes     |
|                                | range_optimizer_max_mem_size<br>Yes | Yes         | Yes        |            | Both      | Yes     |
| rbr_exec_mode                  |                                     |             | Yes        |            | Session   | Yes     |
| read_buffer_sizeYes            |                                     | Yes         | Yes        |            | Both      | Yes     |
| read_only                      | Yes                                 | Yes         | Yes        |            | Global    | Yes     |
| read_rnd_buffer_size Yes       |                                     | Yes         | Yes        |            | Both      | Yes     |
| relay_log                      | Yes                                 | Yes         | Yes        |            | Global    | No      |
| relay_log_basename             |                                     |             | Yes        |            | Global    | No      |
| relay_log_indexYes             |                                     | Yes         | Yes        |            | Global    | No      |
| relay_log_info_file Yes        |                                     | Yes         | Yes        |            | Global    | No      |
| relay_log_info_repository      | Yes                                 | Yes         | Yes        |            | Global    | Yes     |
| relay_log_purgeYes             |                                     | Yes         | Yes        |            | Global    | Yes     |
| relay_log_recovery Yes         |                                     | Yes         | Yes        |            | Global    | No      |
| relay_log_space_limit Yes      |                                     | Yes         | Yes        |            | Global    | No      |
| remove                         | Yes                                 |             |            |            |           |         |
| replicate-do<br>db             | Yes                                 | Yes         |            |            |           |         |
| replicate-do<br>table          | Yes                                 | Yes         |            |            |           |         |
| replicate<br>ignore-db         | Yes                                 | Yes         |            |            |           |         |
| replicate<br>ignore-table      | Yes                                 | Yes         |            |            |           |         |
| replicate<br>rewrite-db        | Yes                                 | Yes         |            |            |           |         |
| replicate<br>same-server<br>id | Yes                                 | Yes         |            |            |           |         |
| replicate<br>wild-do-table     | Yes                                 | Yes         |            |            |           |         |

| Name                              | Cmd-Line                                      | Option File                                          | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------------|-----------------------------------------------|------------------------------------------------------|------------|------------|-----------|---------|
| replicate<br>wild-ignore<br>table | Yes                                           | Yes                                                  |            |            |           |         |
|                                   | Yes                                           | replication_optimize_for_static_plugin_config<br>Yes | Yes        |            | Global    | Yes     |
|                                   | replication_sender_observe_commit_only<br>Yes | Yes                                                  | Yes        |            | Global    | Yes     |
| report_host                       | Yes                                           | Yes                                                  | Yes        |            | Global    | No      |
| report_passwordYes                |                                               | Yes                                                  | Yes        |            | Global    | No      |
| report_port                       | Yes                                           | Yes                                                  | Yes        |            | Global    | No      |
| report_user                       | Yes                                           | Yes                                                  | Yes        |            | Global    | No      |
| require_secure_transport          | Yes                                           | Yes                                                  | Yes        |            | Global    | Yes     |
| rewriter_enabled                  |                                               |                                                      | Yes        |            | Global    | Yes     |
|                                   | Rewriter_number_loaded_rules                  |                                                      |            | Yes        | Global    | No      |
| Rewriter_number_reloads           |                                               |                                                      |            | Yes        | Global    | No      |
|                                   | Rewriter_number_rewritten_queries             |                                                      |            | Yes        | Global    | No      |
| Rewriter_reload_error             |                                               |                                                      |            | Yes        | Global    | No      |
| rewriter_verbose                  |                                               |                                                      | Yes        |            | Global    | Yes     |
|                                   | Rpl_semi_sync_master_clients                  |                                                      |            | Yes        | Global    | No      |
|                                   | rpl_semi_sync_master_enabled<br>Yes           | Yes                                                  | Yes        |            | Global    | Yes     |
|                                   |                                               | Rpl_semi_sync_master_net_avg_wait_time               |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_net_wait_time            |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_net_waits                |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_no_times                 |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_no_tx                    |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_status                   |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_timefunc_failures        |                                                      |            | Yes        | Global    | No      |
|                                   | rpl_semi_sync_master_timeout<br>Yes           | Yes                                                  | Yes        |            | Global    | Yes     |
|                                   | rpl_semi_sync_master_trace_level<br>Yes       | Yes                                                  | Yes        |            | Global    | Yes     |
|                                   | Rpl_semi_sync_master_tx_avg_wait_time         |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_tx_wait_time             |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_tx_waits                 |                                                      |            | Yes        | Global    | No      |
|                                   | Yes                                           | rpl_semi_sync_master_wait_for_slave_count<br>Yes     | Yes        |            | Global    | Yes     |
|                                   | rpl_semi_sync_master_wait_no_slave<br>Yes     | Yes                                                  | Yes        |            | Global    | Yes     |
|                                   | rpl_semi_sync_master_wait_point<br>Yes        | Yes                                                  | Yes        |            | Global    | Yes     |
|                                   |                                               | Rpl_semi_sync_master_wait_pos_backtraverse           |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_wait_sessions            |                                                      |            | Yes        | Global    | No      |
|                                   | Rpl_semi_sync_master_yes_tx                   |                                                      |            | Yes        | Global    | No      |
|                                   | rpl_semi_sync_slave_enabled<br>Yes            | Yes                                                  | Yes        |            | Global    | Yes     |
|                                   | Rpl_semi_sync_slave_status                    |                                                      |            | Yes        | Global    | No      |
|                                   | rpl_semi_sync_slave_trace_level<br>Yes        | Yes                                                  | Yes        |            | Global    | Yes     |
| rpl_stop_slave_timeout Yes        |                                               | Yes                                                  | Yes        |            | Global    | Yes     |
| Rsa_public_key                    |                                               |                                                      |            | Yes        | Global    | No      |

| Name                                         | Cmd-Line                                      | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------------------------|-----------------------------------------------|-------------|------------|------------|-----------|---------|
| safe-user<br>create                          | Yes                                           | Yes         |            |            |           |         |
| secure_auth                                  | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
| secure_file_privYes                          |                                               | Yes         | Yes        |            | Global    | No      |
| Select_full_join                             |                                               |             |            | Yes        | Both      | No      |
| Select_full_range_join                       |                                               |             |            | Yes        | Both      | No      |
| Select_range                                 |                                               |             |            | Yes        | Both      | No      |
| Select_range_check                           |                                               |             |            | Yes        | Both      | No      |
| Select_scan                                  |                                               |             |            | Yes        | Both      | No      |
| server_id                                    | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
| server_id_bits Yes                           |                                               | Yes         | Yes        |            | Global    | No      |
| server_uuid                                  |                                               |             | Yes        |            | Global    | No      |
| session_track_gtids Yes                      |                                               | Yes         | Yes        |            | Both      | Yes     |
| session_track_schema Yes                     |                                               | Yes         | Yes        |            | Both      | Yes     |
|                                              | session_track_state_change<br>Yes             | Yes         | Yes        |            | Both      | Yes     |
|                                              | session_track_system_variables<br>Yes         | Yes         | Yes        |            | Both      | Yes     |
|                                              | session_track_transaction_info<br>Yes         | Yes         | Yes        |            | Both      | Yes     |
|                                              | sha256_password_auto_generate_rsa_keys<br>Yes | Yes         | Yes        |            | Global    | No      |
|                                              | sha256_password_private_key_path<br>Yes       | Yes         | Yes        |            | Global    | No      |
|                                              | sha256_password_proxy_users<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                                              | sha256_password_public_key_path<br>Yes        | Yes         | Yes        |            | Global    | No      |
| shared_memoryYes                             |                                               | Yes         | Yes        |            | Global    | No      |
|                                              | shared_memory_base_name<br>Yes                | Yes         | Yes        |            | Global    | No      |
| show_compatibility_56 Yes                    |                                               | Yes         | Yes        |            | Global    | Yes     |
|                                              | show_create_table_verbosity<br>Yes            | Yes         | Yes        |            | Both      | Yes     |
| show_old_temporals Yes                       |                                               | Yes         | Yes        |            | Both      | Yes     |
| show-slave<br>auth-info                      | Yes                                           | Yes         |            |            |           |         |
| skip<br>character<br>set-client<br>handshake | Yes                                           | Yes         |            |            |           |         |
| skip_external_locking Yes                    |                                               | Yes         | Yes        |            | Global    | No      |
| skip-grant<br>tables                         | Yes                                           | Yes         |            |            |           |         |
| skip-host<br>cache                           | Yes                                           | Yes         |            |            |           |         |
| skip_name_resolve Yes                        |                                               | Yes         | Yes        |            | Global    | No      |
| skip<br>ndbcluster                           | Yes                                           | Yes         |            |            |           |         |
| skip_networkingYes                           |                                               | Yes         | Yes        |            | Global    | No      |
| skip-new                                     | Yes                                           | Yes         |            |            |           |         |
| skip-partition                               | Yes                                           | Yes         |            |            |           |         |

| Name                            | Cmd-Line                              | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------------|---------------------------------------|-------------|------------|------------|-----------|---------|
| skip_show_database Yes          |                                       | Yes         | Yes        |            | Global    | No      |
| skip_slave_startYes             |                                       | Yes         | Yes        |            | Global    | No      |
| skip-ssl                        | Yes                                   | Yes         |            |            |           |         |
| skip-stack<br>trace             | Yes                                   | Yes         |            |            |           |         |
| slave_allow_batching Yes        |                                       | Yes         | Yes        |            | Global    | Yes     |
| slave_checkpoint_group          | Yes                                   | Yes         | Yes        |            | Global    | Yes     |
| slave_checkpoint_period         | Yes                                   | Yes         | Yes        |            | Global    | Yes     |
| slave_compressed_protocol       | Yes                                   | Yes         | Yes        |            | Global    | Yes     |
| slave_exec_mode Yes             |                                       | Yes         | Yes        |            | Global    | Yes     |
| Slave_heartbeat_period          |                                       |             |            | Yes        | Global    | No      |
| Slave_last_heartbeat            |                                       |             |            | Yes        | Global    | No      |
| slave_load_tmpdir Yes           |                                       | Yes         | Yes        |            | Global    | No      |
| slave_max_allowed_packet        | Yes                                   | Yes         | Yes        |            | Global    | Yes     |
| slave_net_timeout Yes           |                                       | Yes         | Yes        |            | Global    | Yes     |
| Slave_open_temp_tables          |                                       |             |            | Yes        | Global    | No      |
| slave_parallel_type Yes         |                                       | Yes         | Yes        |            | Global    | Yes     |
| slave_parallel_workers Yes      |                                       | Yes         | Yes        |            | Global    | Yes     |
|                                 | slave_pending_jobs_size_max<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                                 | slave_preserve_commit_order<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
| Slave_received_heartbeats       |                                       |             |            | Yes        | Global    | No      |
| Slave_retried_transactions      |                                       |             |            | Yes        | Global    | No      |
|                                 | Slave_rows_last_search_algorithm_used |             |            | Yes        | Global    | No      |
|                                 | slave_rows_search_algorithms<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
| Slave_running                   |                                       |             |            | Yes        | Global    | No      |
| slave_skip_errors Yes           |                                       | Yes         | Yes        |            | Global    | No      |
| slave-sql<br>verify<br>checksum | Yes                                   | Yes         |            |            |           |         |
| slave_sql_verify_checksum       | Yes                                   | Yes         | Yes        |            | Global    | Yes     |
| slave_transaction_retries       | Yes                                   | Yes         | Yes        |            | Global    | Yes     |
| slave_type_conversions Yes      |                                       | Yes         | Yes        |            | Global    | Yes     |
| Slow_launch_threads             |                                       |             |            | Yes        | Both      | No      |
| slow_launch_time Yes            |                                       | Yes         | Yes        |            | Global    | Yes     |
| Slow_queries                    |                                       |             |            | Yes        | Both      | No      |
| slow_query_logYes               |                                       | Yes         | Yes        |            | Global    | Yes     |
| slow_query_log_file Yes         |                                       | Yes         | Yes        |            | Global    | Yes     |
| slow-start<br>timeout           | Yes                                   | Yes         |            |            |           |         |
| socket                          | Yes                                   | Yes         | Yes        |            | Global    | No      |
| sort_buffer_sizeYes             |                                       | Yes         | Yes        |            | Both      | Yes     |
| Sort_merge_passes               |                                       |             |            | Yes        | Both      | No      |

| Name                            | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------------|----------|-------------|------------|------------|-----------|---------|
| Sort_range                      |          |             |            | Yes        | Both      | No      |
| Sort_rows                       |          |             |            | Yes        | Both      | No      |
| Sort_scan                       |          |             |            | Yes        | Both      | No      |
| sporadic<br>binlog-dump<br>fail | Yes      | Yes         |            |            |           |         |
| sql_auto_is_null                |          |             | Yes        |            | Both      | Yes     |
| sql_big_selects                 |          |             | Yes        |            | Both      | Yes     |
| sql_buffer_result               |          |             | Yes        |            | Both      | Yes     |
| sql_log_bin                     |          |             | Yes        |            | Session   | Yes     |
| sql_log_off                     |          |             | Yes        |            | Both      | Yes     |
| sql_mode                        | Yes      | Yes         | Yes        |            | Both      | Yes     |
| sql_notes                       |          |             | Yes        |            | Both      | Yes     |
| sql_quote_show_create           |          |             | Yes        |            | Both      | Yes     |
| sql_safe_updates                |          |             | Yes        |            | Both      | Yes     |
| sql_select_limit                |          |             | Yes        |            | Both      | Yes     |
| sql_slave_skip_counter          |          |             | Yes        |            | Global    | Yes     |
| sql_warnings                    |          |             | Yes        |            | Both      | Yes     |
| ssl                             | Yes      | Yes         |            |            |           |         |
| Ssl_accept_renegotiates         |          |             |            | Yes        | Global    | No      |
| Ssl_accepts                     |          |             |            | Yes        | Global    | No      |
| ssl_ca                          | Yes      | Yes         | Yes        |            | Global    | No      |
| Ssl_callback_cache_hits         |          |             |            | Yes        | Global    | No      |
| ssl_capath                      | Yes      | Yes         | Yes        |            | Global    | No      |
| ssl_cert                        | Yes      | Yes         | Yes        |            | Global    | No      |
| Ssl_cipher                      |          |             |            | Yes        | Both      | No      |
| ssl_cipher                      | Yes      | Yes         | Yes        |            | Global    | No      |
| Ssl_cipher_list                 |          |             |            | Yes        | Both      | No      |
| Ssl_client_connects             |          |             |            | Yes        | Global    | No      |
| Ssl_connect_renegotiates        |          |             |            | Yes        | Global    | No      |
| ssl_crl                         | Yes      | Yes         | Yes        |            | Global    | No      |
| ssl_crlpath                     | Yes      | Yes         | Yes        |            | Global    | No      |
| Ssl_ctx_verify_depth            |          |             |            | Yes        | Global    | No      |
| Ssl_ctx_verify_mode             |          |             |            | Yes        | Global    | No      |
| Ssl_default_timeout             |          |             |            | Yes        | Both      | No      |
| Ssl_finished_accepts            |          |             |            | Yes        | Global    | No      |
| Ssl_finished_connects           |          |             |            | Yes        | Global    | No      |
| ssl_key                         | Yes      | Yes         | Yes        |            | Global    | No      |
| Ssl_server_not_after            |          |             |            | Yes        | Both      | No      |
| Ssl_server_not_before           |          |             |            | Yes        | Both      | No      |
| Ssl_session_cache_hits          |          |             |            | Yes        | Global    | No      |

| Name                       | Cmd-Line                          | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|-----------------------------------|-------------|------------|------------|-----------|---------|
| Ssl_session_cache_misses   |                                   |             |            | Yes        | Global    | No      |
| Ssl_session_cache_mode     |                                   |             |            | Yes        | Global    | No      |
|                            | Ssl_session_cache_overflows       |             |            | Yes        | Global    | No      |
| Ssl_session_cache_size     |                                   |             |            | Yes        | Global    | No      |
|                            | Ssl_session_cache_timeouts        |             |            | Yes        | Global    | No      |
| Ssl_sessions_reused        |                                   |             |            | Yes        | Session   | No      |
|                            | Ssl_used_session_cache_entries    |             |            | Yes        | Global    | No      |
| Ssl_verify_depth           |                                   |             |            | Yes        | Both      | No      |
| Ssl_verify_mode            |                                   |             |            | Yes        | Both      | No      |
| Ssl_version                |                                   |             |            | Yes        | Both      | No      |
| standalone                 | Yes                               | Yes         |            |            |           |         |
| stored_program_cache Yes   |                                   | Yes         | Yes        |            | Global    | Yes     |
| super-large<br>pages       | Yes                               | Yes         |            |            |           |         |
| super_read_onlyYes         |                                   | Yes         | Yes        |            | Global    | Yes     |
| symbolic<br>links          | Yes                               | Yes         |            |            |           |         |
| sync_binlog                | Yes                               | Yes         | Yes        |            | Global    | Yes     |
| sync_frm                   | Yes                               | Yes         | Yes        |            | Global    | Yes     |
| sync_master_info Yes       |                                   | Yes         | Yes        |            | Global    | Yes     |
| sync_relay_logYes          |                                   | Yes         | Yes        |            | Global    | Yes     |
| sync_relay_log_info Yes    |                                   | Yes         | Yes        |            | Global    | Yes     |
| sysdate-is<br>now          | Yes                               | Yes         |            |            |           |         |
| system_time_zone           |                                   |             | Yes        |            | Global    | No      |
| table_definition_cache Yes |                                   | Yes         | Yes        |            | Global    | Yes     |
| Table_locks_immediate      |                                   |             |            | Yes        | Global    | No      |
| Table_locks_waited         |                                   |             |            | Yes        | Global    | No      |
| table_open_cache Yes       |                                   | Yes         | Yes        |            | Global    | Yes     |
| Table_open_cache_hits      |                                   |             |            | Yes        | Both      | No      |
|                            | table_open_cache_instances<br>Yes | Yes         | Yes        |            | Global    | No      |
| Table_open_cache_misses    |                                   |             |            | Yes        | Both      | No      |
|                            | Table_open_cache_overflows        |             |            | Yes        | Both      | No      |
| tc-heuristic<br>recover    | Yes                               | Yes         |            |            |           |         |
| Tc_log_max_pages_used      |                                   |             |            | Yes        | Global    | No      |
| Tc_log_page_size           |                                   |             |            | Yes        | Global    | No      |
| Tc_log_page_waits          |                                   |             |            | Yes        | Global    | No      |
| temp-pool                  | Yes                               | Yes         |            |            |           |         |
| thread_cache_size Yes      |                                   | Yes         | Yes        |            | Global    | Yes     |
| thread_handlingYes         |                                   | Yes         | Yes        |            | Global    | No      |
| thread_pool_algorithm Yes  |                                   | Yes         | Yes        |            | Global    | No      |

| Name                        | Cmd-Line                                      | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------|-----------------------------------------------|-------------|------------|------------|-----------|---------|
|                             | thread_pool_high_priority_connection<br>Yes   | Yes         | Yes        |            | Both      | Yes     |
|                             | thread_pool_max_unused_threads<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                             | thread_pool_prio_kickup_timer<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
| thread_pool_sizeYes         |                                               | Yes         | Yes        |            | Global    | No      |
| thread_pool_stall_limit Yes |                                               | Yes         | Yes        |            | Global    | Yes     |
| thread_stack                | Yes                                           | Yes         | Yes        |            | Global    | No      |
| Threads_cached              |                                               |             |            | Yes        | Global    | No      |
| Threads_connected           |                                               |             |            | Yes        | Global    | No      |
| Threads_created             |                                               |             |            | Yes        | Global    | No      |
| Threads_running             |                                               |             |            | Yes        | Global    | No      |
| time_format                 |                                               |             | Yes        |            | Global    | No      |
| time_zone                   |                                               |             | Yes        |            | Both      | Yes     |
| timestamp                   |                                               |             | Yes        |            | Session   | Yes     |
| tls_version                 | Yes                                           | Yes         | Yes        |            | Global    | No      |
| tmp_table_sizeYes           |                                               | Yes         | Yes        |            | Both      | Yes     |
| tmpdir                      | Yes                                           | Yes         | Yes        |            | Global    | No      |
|                             | transaction_alloc_block_size<br>Yes           | Yes         | Yes        |            | Both      | Yes     |
| transaction_allow_batching  |                                               |             | Yes        |            | Session   | Yes     |
| transaction_isolation Yes   |                                               | Yes         |            |            | Both      | Yes     |
| - Variable:<br>tx_isolation |                                               |             | Yes        |            | Both      | Yes     |
| transaction_prealloc_size   | Yes                                           | Yes         | Yes        |            | Both      | Yes     |
| transaction_read_only Yes   |                                               | Yes         |            |            | Both      | Yes     |
| - Variable:<br>tx_read_only |                                               |             | Yes        |            | Both      | Yes     |
|                             | transaction_write_set_extraction<br>Yes       | Yes         | Yes        |            | Both      | Yes     |
| tx_isolation                |                                               |             | Yes        |            | Both      | Yes     |
| tx_read_only                |                                               |             | Yes        |            | Both      | Yes     |
| unique_checks               |                                               |             | Yes        |            | Both      | Yes     |
| updatable_views_with_limit  | Yes                                           | Yes         | Yes        |            | Both      | Yes     |
| Uptime                      |                                               |             |            | Yes        | Global    | No      |
| Uptime_since_flush_status   |                                               |             |            | Yes        | Global    | No      |
| user                        | Yes                                           | Yes         |            |            |           |         |
| validate<br>password        | Yes                                           | Yes         |            |            |           |         |
|                             | validate_password_check_user_name<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                             | validate_password_dictionary_file<br>Yes      | Yes         | Yes        |            | Global    | Varies  |
|                             | validate_password_dictionary_file_last_parsed |             |            | Yes        | Global    | No      |
|                             | validate_password_dictionary_file_words_count |             |            | Yes        | Global    | No      |
| validate_password_length    | Yes                                           | Yes         | Yes        |            | Global    | Yes     |
|                             | validate_password_mixed_case_count<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                             | validate_password_number_count<br>Yes         | Yes         | Yes        |            | Global    | Yes     |

| Name                       | Cmd-Line                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|----------------------------|---------------------------------------------|-------------|------------|------------|-----------|---------|
| validate_password_policy   | Yes                                         | Yes         | Yes        |            | Global    | Yes     |
|                            | validate_password_special_char_count<br>Yes | Yes         | Yes        |            | Global    | Yes     |
| validate-user<br>plugins   | Yes                                         | Yes         |            |            |           |         |
| verbose                    | Yes                                         | Yes         |            |            |           |         |
| version                    |                                             |             | Yes        |            | Global    | No      |
| version_comment            |                                             |             | Yes        |            | Global    | No      |
| version_compile_machine    |                                             |             | Yes        |            | Global    | No      |
| version_compile_os         |                                             |             | Yes        |            | Global    | No      |
| version_tokens_session Yes |                                             | Yes         | Yes        |            | Both      | Yes     |
|                            | version_tokens_session_number<br>Yes        | Yes         | Yes        |            | Both      | No      |
| wait_timeout               | Yes                                         | Yes         | Yes        |            | Both      | Yes     |
| warning_count              |                                             |             | Yes        |            | Session   | No      |

#### **Notes:**

1. This option is dynamic, but should be set only by server. You should not set this variable manually.

# <span id="page-74-0"></span>**5.1.4 Server System Variable Reference**

The following table lists all system variables applicable within mysqld.

The table lists command-line options (Cmd-line), options valid in configuration files (Option file), server system variables (System Var), and status variables (Status var) in one unified list, with an indication of where each option or variable is valid. If a server option set on the command line or in an option file differs from the name of the corresponding system variable, the variable name is noted immediately below the corresponding option. The scope of the variable (Var Scope) is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the variables. Where appropriate, direct links to further information about the items are provided.

**Table 5.2 System Variable Summary**

| Name                        | Cmd-Line                               | Option File | System Var | Var Scope | Dynamic |
|-----------------------------|----------------------------------------|-------------|------------|-----------|---------|
| audit_log_buffer_size Yes   |                                        | Yes         | Yes        | Global    | No      |
| audit_log_compression Yes   |                                        | Yes         | Yes        | Global    | No      |
| audit_log_connection_policy | Yes                                    | Yes         | Yes        | Global    | Yes     |
| audit_log_current_session   |                                        |             | Yes        | Both      | No      |
| audit_log_disableYes        |                                        | Yes         | Yes        | Global    | Yes     |
| audit_log_encryption Yes    |                                        | Yes         | Yes        | Global    | No      |
| audit_log_exclude_accounts  | Yes                                    | Yes         | Yes        | Global    | Yes     |
| audit_log_file              | Yes                                    | Yes         | Yes        | Global    | No      |
| audit_log_filter_id         |                                        |             | Yes        | Both      | No      |
| audit_log_flush             |                                        |             | Yes        | Global    | Yes     |
| audit_log_format Yes        |                                        | Yes         | Yes        | Global    | No      |
|                             | audit_log_format_unix_timestamp<br>Yes | Yes         | Yes        | Global    | Yes     |
| audit_log_include_accounts  | Yes                                    | Yes         | Yes        | Global    | Yes     |
| audit_log_policy Yes        |                                        | Yes         | Yes        | Global    | No      |
| audit_log_read_buffer_size  | Yes                                    | Yes         | Yes        | Varies    | Varies  |

| Name                           | Cmd-Line                                              | Option File | System Var | Var Scope | Dynamic |
|--------------------------------|-------------------------------------------------------|-------------|------------|-----------|---------|
| audit_log_rotate_on_size Yes   |                                                       | Yes         | Yes        | Global    | Yes     |
| audit_log_statement_policy     | Yes                                                   | Yes         | Yes        | Global    | Yes     |
| audit_log_strategyYes          |                                                       | Yes         | Yes        | Global    | No      |
|                                | authentication_ldap_sasl_auth_method_name<br>Yes      | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_bind_base_dn<br>Yes          | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_bind_root_dn<br>Yes          | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_bind_root_pwd<br>Yes         | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_ca_path<br>Yes               | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_group_search_attr<br>Yes     | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_group_search_filter<br>Yes   | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_init_pool_size<br>Yes        | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_log_status<br>Yes            | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_max_pool_size<br>Yes         | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_server_host<br>Yes           | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_server_port<br>Yes           | Yes         | Yes        | Global    | Yes     |
| authentication_ldap_sasl_tls   | Yes                                                   | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_sasl_user_search_attr<br>Yes      | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_auth_method_name<br>Yes    | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_bind_base_dn<br>Yes        | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_bind_root_dn<br>Yes        | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_bind_root_pwd<br>Yes       | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_ca_path<br>Yes             | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_group_search_attr<br>Yes   | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_group_search_filter<br>Yes | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_init_pool_size<br>Yes      | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_log_status<br>Yes          | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_max_pool_size<br>Yes       | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_server_host<br>Yes         | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_server_port<br>Yes         | Yes         | Yes        | Global    | Yes     |
| authentication_ldap_simple_tls | Yes                                                   | Yes         | Yes        | Global    | Yes     |
|                                | authentication_ldap_simple_user_search_attr<br>Yes    | Yes         | Yes        | Global    | Yes     |
|                                | authentication_windows_log_level<br>Yes               | Yes         | Yes        | Global    | No      |
|                                | authentication_windows_use_principal_name<br>Yes      | Yes         | Yes        | Global    | No      |
| auto_generate_certs Yes        |                                                       | Yes         | Yes        | Global    | No      |
| auto_increment_increment       | Yes                                                   | Yes         | Yes        | Both      | Yes     |
| auto_increment_offset Yes      |                                                       | Yes         | Yes        | Both      | Yes     |
| autocommit                     | Yes                                                   | Yes         | Yes        | Both      | Yes     |
| automatic_sp_privileges Yes    |                                                       | Yes         | Yes        | Global    | Yes     |
| avoid_temporal_upgrade Yes     |                                                       | Yes         | Yes        | Global    | Yes     |
| back_log                       | Yes                                                   | Yes         | Yes        | Global    | No      |
| basedir                        | Yes                                                   | Yes         | Yes        | Global    | No      |

| Name                               | Cmd-Line                                               | Option File | System Var | Var Scope | Dynamic |
|------------------------------------|--------------------------------------------------------|-------------|------------|-----------|---------|
| big_tables                         | Yes                                                    | Yes         | Yes        | Both      | Yes     |
| bind_address                       | Yes                                                    | Yes         | Yes        | Global    | No      |
| binlog_cache_sizeYes               |                                                        | Yes         | Yes        | Global    | Yes     |
| binlog_checksumYes                 |                                                        | Yes         | Yes        | Global    | Yes     |
|                                    | binlog_direct_non_transactional_updates<br>Yes         | Yes         | Yes        | Both      | Yes     |
| binlog_error_actionYes             |                                                        | Yes         | Yes        | Global    | Yes     |
| binlog_format                      | Yes                                                    | Yes         | Yes        | Both      | Yes     |
|                                    | binlog_group_commit_sync_delay<br>Yes                  | Yes         | Yes        | Global    | Yes     |
|                                    | binlog_group_commit_sync_no_delay_count<br>Yes         | Yes         | Yes        | Global    | Yes     |
| binlog_gtid_simple_recovery        | Yes                                                    | Yes         | Yes        | Global    | No      |
| binlog_max_flush_queue_time        | Yes                                                    | Yes         | Yes        | Global    | Yes     |
| binlog_order_commits Yes           |                                                        | Yes         | Yes        | Global    | Yes     |
| binlog_row_imageYes                |                                                        | Yes         | Yes        | Both      | Yes     |
| binlog_rows_query_log_events       | Yes                                                    | Yes         | Yes        | Both      | Yes     |
| binlog_stmt_cache_size Ye          |                                                        | Yes         | Yes        | Global    | Yes     |
|                                    | binlog_transaction_dependency_history_size<br>Yes      | Yes         | Yes        | Global    | Yes     |
|                                    | binlog_transaction_dependency_tracking<br>Yes          | Yes         | Yes        | Global    | Yes     |
| block_encryption_mode Yes          |                                                        | Yes         | Yes        | Both      | Yes     |
| bulk_insert_buffer_size Yes        |                                                        | Yes         | Yes        | Both      | Yes     |
| character_set_client               |                                                        |             | Yes        | Both      | Yes     |
| character_set_connection           |                                                        |             | Yes        | Both      | Yes     |
| character_set_database<br>(note 1) |                                                        |             | Yes        | Both      | Yes     |
| character_set_filesystem Ye        |                                                        | Yes         | Yes        | Both      | Yes     |
| character_set_results              |                                                        |             | Yes        | Both      | Yes     |
| character_set_server Yes           |                                                        | Yes         | Yes        | Both      | Yes     |
| character_set_system               |                                                        |             | Yes        | Global    | No      |
| character_sets_dirYes              |                                                        | Yes         | Yes        | Global    | No      |
| check_proxy_usersYes               |                                                        | Yes         | Yes        | Global    | Yes     |
| collation_connection               |                                                        |             | Yes        | Both      | Yes     |
| collation_database<br>(note 1)     |                                                        |             | Yes        | Both      | Yes     |
| collation_server                   | Yes                                                    | Yes         | Yes        | Both      | Yes     |
| completion_type Yes                |                                                        | Yes         | Yes        | Both      | Yes     |
| concurrent_insertYes               |                                                        | Yes         | Yes        | Global    | Yes     |
| connect_timeout Yes                |                                                        | Yes         | Yes        | Global    | Yes     |
|                                    | connection_control_failed_connections_threshold<br>Yes | Yes         | Yes        | Global    | Yes     |
|                                    | connection_control_max_connection_delay<br>Yes         | Yes         | Yes        | Global    | Yes     |
|                                    | connection_control_min_connection_delay<br>Yes         | Yes         | Yes        | Global    | Yes     |
| core_file                          |                                                        |             | Yes        | Global    | No      |
|                                    | daemon_memcached_enable_binlog<br>Yes                  | Yes         | Yes        | Global    | No      |

| Name                            | Cmd-Line                                | Option File | System Var | Var Scope | Dynamic |
|---------------------------------|-----------------------------------------|-------------|------------|-----------|---------|
|                                 | daemon_memcached_engine_lib_name<br>Yes | Yes         | Yes        | Global    | No      |
|                                 | daemon_memcached_engine_lib_path<br>Yes | Yes         | Yes        | Global    | No      |
| daemon_memcached_option         | Yes                                     | Yes         | Yes        | Global    | No      |
|                                 | daemon_memcached_r_batch_size<br>Yes    | Yes         | Yes        | Global    | No      |
|                                 | daemon_memcached_w_batch_size<br>Yes    | Yes         | Yes        | Global    | No      |
| datadir                         | Yes                                     | Yes         | Yes        | Global    | No      |
| date_format                     |                                         |             | Yes        | Global    | No      |
| datetime_format                 |                                         |             | Yes        | Global    | No      |
| debug                           | Yes                                     | Yes         | Yes        | Both      | Yes     |
| debug_sync                      |                                         |             | Yes        | Session   | Yes     |
| default_authentication_plugin   | Yes                                     | Yes         | Yes        | Global    | No      |
| default_password_lifetime Yes   |                                         | Yes         | Yes        | Global    | Yes     |
| default_storage_engine Yes      |                                         | Yes         | Yes        | Both      | Yes     |
| default_tmp_storage_engine      | Yes                                     | Yes         | Yes        | Both      | Yes     |
| default_week_format Yes         |                                         | Yes         | Yes        | Both      | Yes     |
| delay_key_write Yes             |                                         | Yes         | Yes        | Global    | Yes     |
| delayed_insert_limit Yes        |                                         | Yes         | Yes        | Global    | Yes     |
| delayed_insert_timeout Yes      |                                         | Yes         | Yes        | Global    | Yes     |
| delayed_queue_size Yes          |                                         | Yes         | Yes        | Global    | Yes     |
| disabled_storage_engines Yes    |                                         | Yes         | Yes        | Global    | No      |
|                                 | disconnect_on_expired_password<br>Yes   | Yes         | Yes        | Global    | No      |
| div_precision_increment Yes     |                                         | Yes         | Yes        | Both      | Yes     |
| end_markers_in_json Yes         |                                         | Yes         | Yes        | Both      | Yes     |
| enforce_gtid_consistency Yes    |                                         | Yes         | Yes        | Global    | Varies  |
| eq_range_index_dive_limit       | Yes                                     | Yes         | Yes        | Both      | Yes     |
| error_count                     |                                         |             | Yes        | Session   | No      |
| event_scheduler Yes             |                                         | Yes         | Yes        | Global    | Yes     |
| expire_logs_daysYes             |                                         | Yes         | Yes        | Global    | Yes     |
| explicit_defaults_for_timestamp | Yes                                     | Yes         | Yes        | Both      | Yes     |
| external_user                   |                                         |             | Yes        | Session   | No      |
| flush                           | Yes                                     | Yes         | Yes        | Global    | Yes     |
| flush_time                      | Yes                                     | Yes         | Yes        | Global    | Yes     |
| foreign_key_checks              |                                         |             | Yes        | Both      | Yes     |
| ft_boolean_syntaxYes            |                                         | Yes         | Yes        | Global    | Yes     |
| ft_max_word_lenYes              |                                         | Yes         | Yes        | Global    | No      |
| ft_min_word_len Yes             |                                         | Yes         | Yes        | Global    | No      |
| ft_query_expansion_limit Yes    |                                         | Yes         | Yes        | Global    | No      |
| ft_stopword_file                | Yes                                     | Yes         | Yes        | Global    | No      |
| general_log                     | Yes                                     | Yes         | Yes        | Global    | Yes     |
| general_log_file Yes            |                                         | Yes         | Yes        | Global    | Yes     |
| group_concat_max_len Yes        |                                         | Yes         | Yes        | Both      | Yes     |

| Name                            | Cmd-Line                                                  | Option File                                               | System Var | Var Scope | Dynamic |
|---------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|------------|-----------|---------|
|                                 | group_replication_allow_local_disjoint_gtids_join<br>Yes  | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_allow_local_lower_version_join<br>Yes   | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_auto_increment_increment<br>Yes         | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_bootstrap_group<br>Yes                  | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_components_stop_timeout<br>Yes          | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_compression_threshold<br>Yes            | Yes                                                       | Yes        | Global    | Yes     |
|                                 | Yes                                                       | group_replication_enforce_update_everywhere_checks<br>Yes | Yes        | Global    | Yes     |
|                                 | group_replication_exit_state_action<br>Yes                | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_flow_control_applier_threshold<br>Yes   | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_flow_control_certifier_threshold<br>Yes | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_flow_control_mode<br>Yes                | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_force_members<br>Yes                    | Yes                                                       | Yes        | Global    | Yes     |
| group_replication_group_name    | Yes                                                       | Yes                                                       | Yes        | Global    | Yes     |
| group_replication_group_seeds   | Yes                                                       | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_gtid_assignment_block_size<br>Yes       | Yes                                                       | Yes        | Global    | Yes     |
| group_replication_ip_whitelist  | Yes                                                       | Yes                                                       | Yes        | Global    | Yes     |
| group_replication_local_address | Yes                                                       | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_member_weight<br>Yes                    | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_poll_spin_loops<br>Yes                  | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_complete_at<br>Yes             | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_reconnect_interval<br>Yes      | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_retry_count<br>Yes             | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_ca<br>Yes                  | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_capath<br>Yes              | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_cert<br>Yes                | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_cipher<br>Yes              | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_crl<br>Yes                 | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_crlpath<br>Yes             | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_key<br>Yes                 | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_ssl_verify_server_cert<br>Yes  | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_recovery_use_ssl<br>Yes                 | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_single_primary_mode<br>Yes              | Yes                                                       | Yes        | Global    | Yes     |
| group_replication_ssl_mode      | Yes                                                       | Yes                                                       | Yes        | Global    | Yes     |
| group_replication_start_on_boot | Yes                                                       | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_transaction_size_limit<br>Yes           | Yes                                                       | Yes        | Global    | Yes     |
|                                 | group_replication_unreachable_majority_timeout<br>Yes     | Yes                                                       | Yes        | Global    | Yes     |
| gtid_executed                   |                                                           |                                                           | Yes        | Varies    | No      |
|                                 | gtid_executed_compression_period<br>Yes                   | Yes                                                       | Yes        | Global    | Yes     |
| gtid_mode                       | Yes                                                       | Yes                                                       | Yes        | Global    | Varies  |
| gtid_next                       |                                                           |                                                           | Yes        | Session   | Yes     |
| gtid_owned                      |                                                           |                                                           | Yes        | Both      | No      |

| Name                          | Cmd-Line                                   | Option File | System Var | Var Scope | Dynamic |
|-------------------------------|--------------------------------------------|-------------|------------|-----------|---------|
| gtid_purged                   |                                            |             | Yes        | Global    | Yes     |
| have_compress                 |                                            |             | Yes        | Global    | No      |
| have_crypt                    |                                            |             | Yes        | Global    | No      |
| have_dynamic_loading          |                                            |             | Yes        | Global    | No      |
| have_geometry                 |                                            |             | Yes        | Global    | No      |
| have_openssl                  |                                            |             | Yes        | Global    | No      |
| have_profiling                |                                            |             | Yes        | Global    | No      |
| have_query_cache              |                                            |             | Yes        | Global    | No      |
| have_rtree_keys               |                                            |             | Yes        | Global    | No      |
| have_ssl                      |                                            |             | Yes        | Global    | No      |
| have_statement_timeout        |                                            |             | Yes        | Global    | No      |
| have_symlink                  |                                            |             | Yes        | Global    | No      |
| host_cache_size Yes           |                                            | Yes         | Yes        | Global    | Yes     |
| hostname                      |                                            |             | Yes        | Global    | No      |
| identity                      |                                            |             | Yes        | Session   | Yes     |
| ignore_builtin_innodb Yes     |                                            | Yes         | Yes        | Global    | No      |
| ignore_db_dirs                |                                            |             | Yes        | Global    | No      |
| init_connect                  | Yes                                        | Yes         | Yes        | Global    | Yes     |
| init_file                     | Yes                                        | Yes         | Yes        | Global    | No      |
| init_slave                    | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_adaptive_flushing Yes  |                                            | Yes         | Yes        | Global    | Yes     |
| innodb_adaptive_flushing_lwm  | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_adaptive_hash_index    | Yes                                        | Yes         | Yes        | Global    | Yes     |
|                               | innodb_adaptive_hash_index_parts<br>Yes    | Yes         | Yes        | Global    | No      |
|                               | innodb_adaptive_max_sleep_delay<br>Yes     | Yes         | Yes        | Global    | Yes     |
| innodb_api_bk_commit_interval | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_api_disable_rowlock    | Yes                                        | Yes         | Yes        | Global    | No      |
| innodb_api_enable_binlog Yes  |                                            | Yes         | Yes        | Global    | No      |
| innodb_api_enable_mdl Yes     |                                            | Yes         | Yes        | Global    | No      |
| innodb_api_trx_level Yes      |                                            | Yes         | Yes        | Global    | Yes     |
| innodb_autoextend_increment   | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_autoinc_lock_mode      | Yes                                        | Yes         | Yes        | Global    | No      |
|                               | innodb_background_drop_list_empty<br>Yes   | Yes         | Yes        | Global    | Yes     |
| innodb_buffer_pool_chunk_size | Yes                                        | Yes         | Yes        | Global    | No      |
|                               | innodb_buffer_pool_dump_at_shutdown<br>Yes | Yes         | Yes        | Global    | Yes     |
| innodb_buffer_pool_dump_now   | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_buffer_pool_dump_pct   | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_buffer_pool_filename   | Yes                                        | Yes         | Yes        | Global    | Yes     |
| innodb_buffer_pool_instances  | Yes                                        | Yes         | Yes        | Global    | No      |
| innodb_buffer_pool_load_abort | Yes                                        | Yes         | Yes        | Global    | Yes     |
|                               | innodb_buffer_pool_load_at_startup<br>Yes  | Yes         | Yes        | Global    | No      |

| Name                           | Cmd-Line                                        | Option File | System Var | Var Scope | Dynamic |
|--------------------------------|-------------------------------------------------|-------------|------------|-----------|---------|
| innodb_buffer_pool_load_now    | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_buffer_pool_size Yes    |                                                 | Yes         | Yes        | Global    | Varies  |
|                                | innodb_change_buffer_max_size<br>Yes            | Yes         | Yes        | Global    | Yes     |
| innodb_change_buffering Yes    |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_change_buffering_debug  | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_checksum_algorithm      | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_checksumsYes            |                                                 | Yes         | Yes        | Global    | No      |
| innodb_cmp_per_index_enabled   | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_commit_concurrency      | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_compress_debug Yes      |                                                 | Yes         | Yes        | Global    | Yes     |
|                                | innodb_compression_failure_threshold_pct<br>Yes | Yes         | Yes        | Global    | Yes     |
| innodb_compression_level       | Yes                                             | Yes         | Yes        | Global    | Yes     |
|                                | innodb_compression_pad_pct_max<br>Yes           | Yes         | Yes        | Global    | Yes     |
| innodb_concurrency_tickets     | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_data_file_path Yes      |                                                 | Yes         | Yes        | Global    | No      |
| innodb_data_home_dir Yes       |                                                 | Yes         | Yes        | Global    | No      |
| innodb_deadlock_detect Yes     |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_default_row_format      | Yes                                             | Yes         | Yes        | Global    | Yes     |
|                                | innodb_disable_resize_buffer_pool_debug<br>Yes  | Yes         | Yes        | Global    | Yes     |
| innodb_disable_sort_file_cache | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_doublewriteYes          |                                                 | Yes         | Yes        | Global    | No      |
| innodb_fast_shutdown Yes       |                                                 | Yes         | Yes        | Global    | Yes     |
|                                | innodb_fil_make_page_dirty_debug<br>Yes         | Yes         | Yes        | Global    | Yes     |
| innodb_file_formatYes          |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_file_format_check Yes   |                                                 | Yes         | Yes        | Global    | No      |
| innodb_file_format_max Yes     |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_file_per_table Yes      |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_fill_factorYes          |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_flush_log_at_timeout    | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_flush_log_at_trx_commit | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_flush_method Yes        |                                                 | Yes         | Yes        | Global    | No      |
| innodb_flush_neighbors Yes     |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_flush_syncYes           |                                                 | Yes         | Yes        | Global    | Yes     |
| innodb_flushing_avg_loops      | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_force_load_corrupted    | Yes                                             | Yes         | Yes        | Global    | No      |
| innodb_force_recovery Yes      |                                                 | Yes         | Yes        | Global    | No      |
| innodb_ft_aux_table            |                                                 |             | Yes        | Global    | Yes     |
| innodb_ft_cache_size Yes       |                                                 | Yes         | Yes        | Global    | No      |
| innodb_ft_enable_diag_print    | Yes                                             | Yes         | Yes        | Global    | Yes     |
| innodb_ft_enable_stopword      | Yes                                             | Yes         | Yes        | Both      | Yes     |
| innodb_ft_max_token_size       | Yes                                             | Yes         | Yes        | Global    | No      |

| Name                           | Cmd-Line                                    | Option File | System Var | Var Scope | Dynamic |
|--------------------------------|---------------------------------------------|-------------|------------|-----------|---------|
| innodb_ft_min_token_size Yes   |                                             | Yes         | Yes        | Global    | No      |
| innodb_ft_num_word_optimize    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| innodb_ft_result_cache_limit   | Yes                                         | Yes         | Yes        | Global    | Yes     |
|                                | innodb_ft_server_stopword_table<br>Yes      | Yes         | Yes        | Global    | Yes     |
| innodb_ft_sort_pll_degree Yes  |                                             | Yes         | Yes        | Global    | No      |
| innodb_ft_total_cache_size     | Yes                                         | Yes         | Yes        | Global    | No      |
| innodb_ft_user_stopword_table  | Yes                                         | Yes         | Yes        | Both      | Yes     |
| innodb_io_capacityYes          |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_io_capacity_max Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_large_prefixYes         |                                             | Yes         | Yes        | Global    | Yes     |
|                                | innodb_limit_optimistic_insert_debug<br>Yes | Yes         | Yes        | Global    | Yes     |
| innodb_lock_wait_timeout Yes   |                                             | Yes         | Yes        | Both      | Yes     |
| innodb_locks_unsafe_for_binlog | Yes                                         | Yes         | Yes        | Global    | No      |
| innodb_log_buffer_size Yes     |                                             | Yes         | Yes        | Global    | No      |
| innodb_log_checkpoint_now      | Yes                                         | Yes         | Yes        | Global    | Yes     |
| innodb_log_checksums Yes       |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_log_compressed_pages    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| innodb_log_file_size Yes       |                                             | Yes         | Yes        | Global    | No      |
| innodb_log_files_in_group Yes  |                                             | Yes         | Yes        | Global    | No      |
| innodb_log_group_home_dir      | Yes                                         | Yes         | Yes        | Global    | No      |
| innodb_log_write_ahead_size    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| innodb_lru_scan_depth Yes      |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_max_dirty_pages_pct     | Yes                                         | Yes         | Yes        | Global    | Yes     |
|                                | innodb_max_dirty_pages_pct_lwm<br>Yes       | Yes         | Yes        | Global    | Yes     |
| innodb_max_purge_lag Yes       |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_max_purge_lag_delay     | Yes                                         | Yes         | Yes        | Global    | Yes     |
| innodb_max_undo_log_size       | Yes                                         | Yes         | Yes        | Global    | Yes     |
|                                | innodb_merge_threshold_set_all_debug<br>Yes | Yes         | Yes        | Global    | Yes     |
| innodb_monitor_disable Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_monitor_enable Yes      |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_monitor_reset Yes       |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_monitor_reset_all Yes   |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_numa_interleave Yes     |                                             | Yes         | Yes        | Global    | No      |
| innodb_old_blocks_pct Yes      |                                             | Yes         | Yes        | Global    | Yes     |
| innodb_old_blocks_time Yes     |                                             | Yes         | Yes        | Global    | Yes     |
|                                | innodb_online_alter_log_max_size<br>Yes     | Yes         | Yes        | Global    | Yes     |
| innodb_open_filesYes           |                                             | Yes         | Yes        | Global    | No      |
| innodb_optimize_fulltext_only  | Yes                                         | Yes         | Yes        | Global    | Yes     |
| innodb_page_cleaners Yes       |                                             | Yes         | Yes        | Global    | No      |
| innodb_page_sizeYes            |                                             | Yes         | Yes        | Global    | No      |
| innodb_print_all_deadlocks     | Yes                                         | Yes         | Yes        | Global    | Yes     |

| Name                          | Cmd-Line                                       | Option File | System Var | Var Scope | Dynamic |
|-------------------------------|------------------------------------------------|-------------|------------|-----------|---------|
| innodb_purge_batch_size Yes   |                                                | Yes         | Yes        | Global    | Yes     |
|                               | innodb_purge_rseg_truncate_frequency<br>Yes    | Yes         | Yes        | Global    | Yes     |
| innodb_purge_threads Yes      |                                                | Yes         | Yes        | Global    | No      |
| innodb_random_read_ahead      | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_read_ahead_threshold   | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_read_io_threads Yes    |                                                | Yes         | Yes        | Global    | No      |
| innodb_read_onlyYes           |                                                | Yes         | Yes        | Global    | No      |
| innodb_replication_delay Yes  |                                                | Yes         | Yes        | Global    | Yes     |
| innodb_rollback_on_timeout    | Yes                                            | Yes         | Yes        | Global    | No      |
| innodb_rollback_segments      | Yes                                            | Yes         | Yes        | Global    | Yes     |
|                               | innodb_saved_page_number_debug<br>Yes          | Yes         | Yes        | Global    | Yes     |
| innodb_sort_buffer_size Ye    |                                                | Yes         | Yes        | Global    | No      |
| innodb_spin_wait_delay Yes    |                                                | Yes         | Yes        | Global    | Yes     |
| innodb_stats_auto_recalc Yes  |                                                | Yes         | Yes        | Global    | Yes     |
|                               | innodb_stats_include_delete_marked<br>Yes      | Yes         | Yes        | Global    | Yes     |
| innodb_stats_method Yes       |                                                | Yes         | Yes        | Global    | Yes     |
| innodb_stats_on_metadata      | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_stats_persistent Yes   |                                                | Yes         | Yes        | Global    | Yes     |
|                               | innodb_stats_persistent_sample_pages<br>Yes    | Yes         | Yes        | Global    | Yes     |
| innodb_stats_sample_pages     | Yes                                            | Yes         | Yes        | Global    | Yes     |
|                               | innodb_stats_transient_sample_pages<br>Yes     | Yes         | Yes        | Global    | Yes     |
| innodb_status_output Yes      |                                                | Yes         | Yes        | Global    | Yes     |
| innodb_status_output_locks    | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_strict_modeYes         |                                                | Yes         | Yes        | Both      | Yes     |
| innodb_support_xaYes          |                                                | Yes         | Yes        | Both      | Yes     |
| innodb_sync_array_size Yes    |                                                | Yes         | Yes        | Global    | No      |
| innodb_sync_debug Yes         |                                                | Yes         | Yes        | Global    | No      |
| innodb_sync_spin_loops Yes    |                                                | Yes         | Yes        | Global    | Yes     |
| innodb_table_locksYes         |                                                | Yes         | Yes        | Both      | Yes     |
| innodb_temp_data_file_path    | Yes                                            | Yes         | Yes        | Global    | No      |
| innodb_thread_concurrency     | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_thread_sleep_delay     | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_tmpdir                 | Yes                                            | Yes         | Yes        | Both      | Yes     |
|                               | innodb_trx_purge_view_update_only_debug<br>Yes | Yes         | Yes        | Global    | Yes     |
| innodb_trx_rseg_n_slots_debug | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_undo_directory Yes     |                                                | Yes         | Yes        | Global    | No      |
| innodb_undo_log_truncate      | Yes                                            | Yes         | Yes        | Global    | Yes     |
| innodb_undo_logsYes           |                                                | Yes         | Yes        | Global    | Yes     |
| innodb_undo_tablespaces Yes   |                                                | Yes         | Yes        | Global    | No      |
| innodb_use_native_aio Yes     |                                                | Yes         | Yes        | Global    | No      |
| innodb_version                |                                                |             | Yes        | Global    | No      |

| Name                            | Cmd-Line                                     | Option File | System Var | Var Scope | Dynamic |
|---------------------------------|----------------------------------------------|-------------|------------|-----------|---------|
| innodb_write_io_threads Yes     |                                              | Yes         | Yes        | Global    | No      |
| insert_id                       |                                              |             | Yes        | Session   | Yes     |
| interactive_timeout Yes         |                                              | Yes         | Yes        | Both      | Yes     |
|                                 | internal_tmp_disk_storage_engine<br>Yes      | Yes         | Yes        | Global    | Yes     |
| join_buffer_size                | Yes                                          | Yes         | Yes        | Both      | Yes     |
| keep_files_on_create Yes        |                                              | Yes         | Yes        | Both      | Yes     |
| key_buffer_size                 | Yes                                          | Yes         | Yes        | Global    | Yes     |
| key_cache_age_threshold Yes     |                                              | Yes         | Yes        | Global    | Yes     |
| key_cache_block_size Yes        |                                              | Yes         | Yes        | Global    | Yes     |
| key_cache_division_limit Yes    |                                              | Yes         | Yes        | Global    | Yes     |
| keyring_aws_cmk_id Yes          |                                              | Yes         | Yes        | Global    | Yes     |
| keyring_aws_conf_file Yes       |                                              | Yes         | Yes        | Global    | No      |
| keyring_aws_data_file Yes       |                                              | Yes         | Yes        | Global    | No      |
| keyring_aws_regionYes           |                                              | Yes         | Yes        | Global    | Yes     |
| keyring_encrypted_file_data     | Yes                                          | Yes         | Yes        | Global    | Yes     |
|                                 | keyring_encrypted_file_password<br>Yes       | Yes         | Yes        | Global    | Yes     |
| keyring_file_dataYes            |                                              | Yes         | Yes        | Global    | Yes     |
| keyring_okv_conf_dir Yes        |                                              | Yes         | Yes        | Global    | Yes     |
| keyring_operations              |                                              |             | Yes        | Global    | Yes     |
| language                        | Yes                                          | Yes         | Yes        | Global    | No      |
| large_files_support             |                                              |             | Yes        | Global    | No      |
| large_page_size                 |                                              |             | Yes        | Global    | No      |
| large_pages                     | Yes                                          | Yes         | Yes        | Global    | No      |
| last_insert_id                  |                                              |             | Yes        | Session   | Yes     |
| lc_messages                     | Yes                                          | Yes         | Yes        | Both      | Yes     |
| lc_messages_dirYes              |                                              | Yes         | Yes        | Global    | No      |
| lc_time_names                   | Yes                                          | Yes         | Yes        | Both      | Yes     |
| license                         |                                              |             | Yes        | Global    | No      |
| local_infile                    | Yes                                          | Yes         | Yes        | Global    | Yes     |
| lock_wait_timeoutYes            |                                              | Yes         | Yes        | Both      | Yes     |
| locked_in_memory                |                                              |             | Yes        | Global    | No      |
| log_bin                         |                                              |             | Yes        | Global    | No      |
| log_bin_basename                |                                              |             | Yes        | Global    | No      |
| log_bin_index                   | Yes                                          | Yes         | Yes        | Global    | No      |
| log_bin_trust_function_creators | Yes                                          | Yes         | Yes        | Global    | Yes     |
| log_bin_use_v1_row_events       | Yes                                          | Yes         | Yes        | Global    | Yes     |
|                                 | log_builtin_as_identified_by_password<br>Yes | Yes         | Yes        | Global    | Yes     |
| log_error                       | Yes                                          | Yes         | Yes        | Global    | No      |
| log_error_verbosityYes          |                                              | Yes         | Yes        | Global    | Yes     |
| log_output                      | Yes                                          | Yes         | Yes        | Global    | Yes     |
| log_queries_not_using_indexes   | Yes                                          | Yes         | Yes        | Global    | Yes     |

| Name                         | Cmd-Line                                      | Option File | System Var | Var Scope | Dynamic |
|------------------------------|-----------------------------------------------|-------------|------------|-----------|---------|
| log_slave_updatesYes         |                                               | Yes         | Yes        | Global    | No      |
| log_slow_admin_statements    | Yes                                           | Yes         | Yes        | Global    | Yes     |
| log_slow_slave_statements    | Yes                                           | Yes         | Yes        | Global    | Yes     |
|                              | log_statements_unsafe_for_binlog<br>Yes       | Yes         | Yes        | Global    | Yes     |
| log_syslog                   | Yes                                           | Yes         | Yes        | Global    | Yes     |
| log_syslog_facilityYes       |                                               | Yes         | Yes        | Global    | Yes     |
| log_syslog_include_pid Yes   |                                               | Yes         | Yes        | Global    | Yes     |
| log_syslog_tag               | Yes                                           | Yes         | Yes        | Global    | Yes     |
|                              | log_throttle_queries_not_using_indexes<br>Yes | Yes         | Yes        | Global    | Yes     |
| log_timestamps               | Yes                                           | Yes         | Yes        | Global    | Yes     |
| log_warnings                 | Yes                                           | Yes         | Yes        | Global    | Yes     |
| long_query_time Yes          |                                               | Yes         | Yes        | Both      | Yes     |
| low_priority_updates Yes     |                                               | Yes         | Yes        | Both      | Yes     |
| lower_case_file_system       |                                               |             | Yes        | Global    | No      |
| lower_case_table_names Yes   |                                               | Yes         | Yes        | Global    | No      |
| master_info_repository Yes   |                                               | Yes         | Yes        | Global    | Yes     |
| master_verify_checksum Yes   |                                               | Yes         | Yes        | Global    | Yes     |
| max_allowed_packet Yes       |                                               | Yes         | Yes        | Both      | Yes     |
| max_binlog_cache_size Ye     |                                               | Yes         | Yes        | Global    | Yes     |
| max_binlog_size Yes          |                                               | Yes         | Yes        | Global    | Yes     |
| max_binlog_stmt_cache_size   | Yes                                           | Yes         | Yes        | Global    | Yes     |
| max_connect_errors Yes       |                                               | Yes         | Yes        | Global    | Yes     |
| max_connectionsYes           |                                               | Yes         | Yes        | Global    | Yes     |
| max_delayed_threads Yes      |                                               | Yes         | Yes        | Both      | Yes     |
| max_digest_lengthYes         |                                               | Yes         | Yes        | Global    | No      |
| max_error_countYes           |                                               | Yes         | Yes        | Both      | Yes     |
| max_execution_time Yes       |                                               | Yes         | Yes        | Both      | Yes     |
| max_heap_table_size Yes      |                                               | Yes         | Yes        | Both      | Yes     |
| max_insert_delayed_threads   |                                               |             | Yes        | Both      | Yes     |
| max_join_size                | Yes                                           | Yes         | Yes        | Both      | Yes     |
| max_length_for_sort_data Yes |                                               | Yes         | Yes        | Both      | Yes     |
| max_points_in_geometry Yes   |                                               | Yes         | Yes        | Both      | Yes     |
| max_prepared_stmt_count      | Yes                                           | Yes         | Yes        | Global    | Yes     |
| max_relay_log_sizeYs         |                                               | Yes         | Yes        | Global    | Yes     |
| max_seeks_for_key Yes        |                                               | Yes         | Yes        | Both      | Yes     |
| max_sort_length Yes          |                                               | Yes         | Yes        | Both      | Yes     |
| max_sp_recursion_depth Yes   |                                               | Yes         | Yes        | Both      | Yes     |
| max_tmp_tables               |                                               |             | Yes        | Both      | Yes     |
| max_user_connections Yes     |                                               | Yes         | Yes        | Both      | Yes     |
| max_write_lock_count Yes     |                                               | Yes         | Yes        | Global    | Yes     |
| mecab_rc_file                | Yes                                           | Yes         | Yes        | Global    | No      |

| Name                          | Cmd-Line                                   | Option File | System Var | Var Scope | Dynamic |
|-------------------------------|--------------------------------------------|-------------|------------|-----------|---------|
| metadata_locks_cache_size     | Yes                                        | Yes         | Yes        | Global    | No      |
| metadata_locks_hash_instances | Yes                                        | Yes         | Yes        | Global    | No      |
| min_examined_row_limit Yes    |                                            | Yes         | Yes        | Both      | Yes     |
| multi_range_countYes          |                                            | Yes         | Yes        | Both      | Yes     |
| myisam_data_pointer_size      | Yes                                        | Yes         | Yes        | Global    | Yes     |
| myisam_max_sort_file_size     | Yes                                        | Yes         | Yes        | Global    | Yes     |
| myisam_mmap_size Yes          |                                            | Yes         | Yes        | Global    | No      |
| myisam_recover_options Yes    |                                            | Yes         | Yes        | Global    | No      |
| myisam_sort_buffer_size Yes   |                                            | Yes         | Yes        | Both      | Yes     |
| myisam_stats_method Yes       |                                            | Yes         | Yes        | Both      | Yes     |
| myisam_use_mmap Yes           |                                            | Yes         | Yes        | Global    | Yes     |
| mysql_firewall_mode Yes       |                                            | Yes         | Yes        | Global    | Yes     |
| mysql_firewall_trace Yes      |                                            | Yes         | Yes        | Global    | Yes     |
|                               | mysql_native_password_proxy_users<br>Yes   | Yes         | Yes        | Global    | Yes     |
| mysqlx_bind_address Yes       |                                            | Yes         | Yes        | Global    | No      |
| mysqlx_connect_timeout Yes    |                                            | Yes         | Yes        | Global    | Yes     |
|                               | mysqlx_idle_worker_thread_timeout<br>Yes   | Yes         | Yes        | Global    | Yes     |
| mysqlx_max_allowed_packet     | Yes                                        | Yes         | Yes        | Global    | Yes     |
| mysqlx_max_connections Yes    |                                            | Yes         | Yes        | Global    | Yes     |
| mysqlx_min_worker_threads     | Yes                                        | Yes         | Yes        | Global    | Yes     |
| mysqlx_port                   | Yes                                        | Yes         | Yes        | Global    | No      |
| mysqlx_port_open_timeout      | Yes                                        | Yes         | Yes        | Global    | No      |
| mysqlx_socket                 | Yes                                        | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_ca                 | Yes                                        | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_capathYes          |                                            | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_cert Yes           |                                            | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_cipherYes          |                                            | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_crl                | Yes                                        | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_crlpathYes         |                                            | Yes         | Yes        | Global    | No      |
| mysqlx_ssl_key                | Yes                                        | Yes         | Yes        | Global    | No      |
| named_pipe                    | Yes                                        | Yes         | Yes        | Global    | No      |
| named_pipe_full_access_group  | Yes                                        | Yes         | Yes        | Global    | No      |
| ndb_allow_copying_alter_table | Yes                                        | Yes         | Yes        | Both      | Yes     |
| ndb_autoincrement_prefetch_sz | Yes                                        | Yes         | Yes        | Both      | Yes     |
| ndb_batch_size                | Yes                                        | Yes         | Yes        | Both      | Yes     |
| ndb_blob_read_batch_bytes     | Yes                                        | Yes         | Yes        | Both      | Yes     |
| ndb_blob_write_batch_bytes    | Yes                                        | Yes         | Yes        | Both      | Yes     |
| ndb_cache_check_time Yes      |                                            | Yes         | Yes        | Global    | Yes     |
| ndb_clear_apply_status Yes    |                                            |             | Yes        | Global    | Yes     |
| ndb_cluster_connection_pool   | Yes                                        | Yes         | Yes        | Global    | No      |
|                               | ndb_cluster_connection_pool_nodeids<br>Yes | Yes         | Yes        | Global    | No      |

| Name                         | Cmd-Line                                    | Option File | System Var | Var Scope | Dynamic |
|------------------------------|---------------------------------------------|-------------|------------|-----------|---------|
| ndb_data_node_neighbour      | Yes                                         | Yes         | Yes        | Global    | Yes     |
| ndb_default_column_format    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| ndb_default_column_format    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| ndb_deferred_constraints Yes |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_deferred_constraints Yes |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_distribution Yes         |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_distribution Yes         |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_eventbuffer_free_percent | Yes                                         | Yes         | Yes        | Global    | Yes     |
| ndb_eventbuffer_max_alloc    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| ndb_extra_loggingYes         |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_force_send Yes           |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_fully_replicatedYes      |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_index_stat_enable Yes    |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_index_stat_option Yes    |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_join_pushdown            |                                             |             | Yes        | Both      | Yes     |
| ndb_log_apply_status Yes     |                                             | Yes         | Yes        | Global    | No      |
| ndb_log_apply_status Yes     |                                             | Yes         | Yes        | Global    | No      |
| ndb_log_bin                  | Yes                                         |             | Yes        | Both      | No      |
| ndb_log_binlog_index Yes     |                                             |             | Yes        | Global    | Yes     |
| ndb_log_empty_epochs Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_log_empty_epochs Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_log_empty_update Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_log_empty_update Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_log_exclusive_reads Yes  |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_log_exclusive_reads Yes  |                                             | Yes         | Yes        | Both      | Yes     |
| ndb_log_fail_terminate Yes   |                                             | Yes         | Yes        | Global    | No      |
| ndb_log_orig                 | Yes                                         | Yes         | Yes        | Global    | No      |
| ndb_log_orig                 | Yes                                         | Yes         | Yes        | Global    | No      |
| ndb_log_transaction_id Yes   |                                             | Yes         | Yes        | Global    | No      |
| ndb_log_transaction_id       |                                             |             | Yes        | Global    | No      |
| ndb_log_update_as_write Yes  |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_log_update_minimal Yes   |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_log_updated_only Yes     |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_optimization_delay Yes   |                                             | Yes         | Yes        | Global    | Yes     |
| ndb_optimized_node_selection | Yes                                         | Yes         | Yes        | Global    | Yes     |
| ndb_optimized_node_selection | Yes                                         | Yes         | Yes        | Global    | No      |
| ndb_read_backupYes           |                                             | Yes         | Yes        | Global    | Yes     |
|                              | ndb_recv_thread_activation_threshold<br>Yes | Yes         | Yes        | Global    | Yes     |
| ndb_recv_thread_cpu_mask     | Yes                                         | Yes         | Yes        | Global    | Yes     |
|                              | ndb_report_thresh_binlog_epoch_slip<br>Yes  | Yes         | Yes        | Global    | Yes     |
|                              | ndb_report_thresh_binlog_mem_usage<br>Yes   | Yes         | Yes        | Global    | Yes     |

| Name                         | Cmd-Line                                | Option File | System Var | Var Scope | Dynamic |
|------------------------------|-----------------------------------------|-------------|------------|-----------|---------|
| ndb_row_checksum             |                                         |             | Yes        | Both      | Yes     |
|                              | ndb_show_foreign_key_mock_tables<br>Yes | Yes         | Yes        | Global    | Yes     |
| ndb_slave_conflict_role Yes  |                                         | Yes         | Yes        | Global    | Yes     |
| Ndb_system_name              |                                         |             | Yes        | Global    | No      |
| ndb_table_no_logging         |                                         |             | Yes        | Session   | Yes     |
| ndb_table_temporary          |                                         |             | Yes        | Session   | Yes     |
| ndb_use_copying_alter_table  |                                         |             | Yes        | Both      | No      |
| ndb_use_exact_count          |                                         |             | Yes        | Both      | Yes     |
| ndb_use_transactions Yes     |                                         | Yes         | Yes        | Both      | Yes     |
| ndb_version                  |                                         |             | Yes        | Global    | No      |
| ndb_version_string           |                                         |             | Yes        | Global    | No      |
| ndb_wait_connected Yes       |                                         | Yes         | Yes        | Global    | No      |
| ndb_wait_setup               | Yes                                     | Yes         | Yes        | Global    | No      |
| ndbinfo_database             |                                         |             | Yes        | Global    | No      |
| ndbinfo_max_bytesYes         |                                         |             | Yes        | Both      | Yes     |
| ndbinfo_max_rowsYes          |                                         |             | Yes        | Both      | Yes     |
| ndbinfo_offline              |                                         |             | Yes        | Global    | Yes     |
| ndbinfo_show_hidden Yes      |                                         |             | Yes        | Both      | Yes     |
| ndbinfo_table_prefix         |                                         |             | Yes        | Global    | No      |
| ndbinfo_version              |                                         |             | Yes        | Global    | No      |
| net_buffer_lengthYes         |                                         | Yes         | Yes        | Both      | Yes     |
| net_read_timeoutYes          |                                         | Yes         | Yes        | Both      | Yes     |
| net_retry_count              | Yes                                     | Yes         | Yes        | Both      | Yes     |
| net_write_timeoutYes         |                                         | Yes         | Yes        | Both      | Yes     |
| new                          | Yes                                     | Yes         | Yes        | Both      | Yes     |
| ngram_token_sizeYes          |                                         | Yes         | Yes        | Global    | No      |
| offline_mode                 | Yes                                     | Yes         | Yes        | Global    | Yes     |
| old                          | Yes                                     | Yes         | Yes        | Global    | No      |
| old_alter_table              | Yes                                     | Yes         | Yes        | Both      | Yes     |
| old_passwords                | Yes                                     | Yes         | Yes        | Both      | Yes     |
| open_files_limit             | Yes                                     | Yes         | Yes        | Global    | No      |
| optimizer_prune_level Yes    |                                         | Yes         | Yes        | Both      | Yes     |
| optimizer_search_depth Yes   |                                         | Yes         | Yes        | Both      | Yes     |
| optimizer_switch Yes         |                                         | Yes         | Yes        | Both      | Yes     |
| optimizer_trace              | Yes                                     | Yes         | Yes        | Both      | Yes     |
| optimizer_trace_features Yes |                                         | Yes         | Yes        | Both      | Yes     |
| optimizer_trace_limit Yes    |                                         | Yes         | Yes        | Both      | Yes     |
| optimizer_trace_max_mem_size | Yes                                     | Yes         | Yes        | Both      | Yes     |
| optimizer_trace_offset Yes   |                                         | Yes         | Yes        | Both      | Yes     |
| parser_max_mem_size Yes      |                                         | Yes         | Yes        | Both      | Yes     |
| performance_schema Yes       |                                         | Yes         | Yes        | Global    | No      |

| Name | Cmd-Line                                             | Option File                                                     | System Var | Var Scope | Dynamic |
|------|------------------------------------------------------|-----------------------------------------------------------------|------------|-----------|---------|
|      | performance_schema_accounts_size<br>Yes              | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_digests_size<br>Yes               | Yes                                                             | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_events_stages_history_long_size<br>Yes       | Yes        | Global    | No      |
|      | performance_schema_events_stages_history_size<br>Yes | Yes                                                             | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_events_statements_history_long_size<br>Yes   | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_events_statements_history_size<br>Yes        | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_events_transactions_history_long_size<br>Yes | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_events_transactions_history_size<br>Yes      | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_events_waits_history_long_size<br>Yes        | Yes        | Global    | No      |
|      | performance_schema_events_waits_history_size<br>Yes  | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_hosts_size<br>Yes                 | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_cond_classes<br>Yes           | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_cond_instances<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_digest_length<br>Yes          | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_file_classes<br>Yes           | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_file_handles<br>Yes           | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_file_instances<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_index_stat<br>Yes             | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_memory_classes<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_metadata_locks<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_mutex_classes<br>Yes          | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_mutex_instances<br>Yes        | Yes                                                             | Yes        | Global    | No      |
|      | Yes                                                  | performance_schema_max_prepared_statements_instances<br>Yes     | Yes        | Global    | No      |
|      | performance_schema_max_program_instances<br>Yes      | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_rwlock_classes<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_rwlock_instances<br>Yes       | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_socket_classes<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_socket_instances<br>Yes       | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_sql_text_length<br>Yes        | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_stage_classes<br>Yes          | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_statement_classes<br>Yes      | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_statement_stack<br>Yes        | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_table_handles<br>Yes          | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_table_instances<br>Yes        | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_table_lock_stat<br>Yes        | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_thread_classes<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_max_thread_instances<br>Yes       | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_session_connect_attrs_size<br>Yes | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_setup_actors_size<br>Yes          | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_setup_objects_size<br>Yes         | Yes                                                             | Yes        | Global    | No      |
|      | performance_schema_show_processlist<br>Yes           | Yes                                                             | Yes        | Global    | Yes     |

| Name                          | Cmd-Line                                             | Option File | System Var | Var Scope | Dynamic |
|-------------------------------|------------------------------------------------------|-------------|------------|-----------|---------|
|                               | performance_schema_users_size<br>Yes                 | Yes         | Yes        | Global    | No      |
| pid_file                      | Yes                                                  | Yes         | Yes        | Global    | No      |
| plugin_dir                    | Yes                                                  | Yes         | Yes        | Global    | No      |
| port                          | Yes                                                  | Yes         | Yes        | Global    | No      |
| preload_buffer_sizeYs         |                                                      | Yes         | Yes        | Both      | Yes     |
| profiling                     |                                                      |             | Yes        | Both      | Yes     |
| profiling_history_size Yes    |                                                      | Yes         | Yes        | Both      | Yes     |
| protocol_version              |                                                      |             | Yes        | Global    | No      |
| proxy_user                    |                                                      |             | Yes        | Session   | No      |
| pseudo_slave_mode             |                                                      |             | Yes        | Session   | Yes     |
| pseudo_thread_id              |                                                      |             | Yes        | Session   | Yes     |
| query_alloc_block_size Yes    |                                                      | Yes         | Yes        | Both      | Yes     |
| query_cache_limitYes          |                                                      | Yes         | Yes        | Global    | Yes     |
| query_cache_min_res_unit      | Yes                                                  | Yes         | Yes        | Global    | Yes     |
| query_cache_sizeYes           |                                                      | Yes         | Yes        | Global    | Yes     |
| query_cache_typeYes           |                                                      | Yes         | Yes        | Both      | Yes     |
| query_cache_wlock_invalidate  | Yes                                                  | Yes         | Yes        | Both      | Yes     |
| query_prealloc_sizeYs         |                                                      | Yes         | Yes        | Both      | Yes     |
| rand_seed1                    |                                                      |             | Yes        | Session   | Yes     |
| rand_seed2                    |                                                      |             | Yes        | Session   | Yes     |
| range_alloc_block_size Yes    |                                                      | Yes         | Yes        | Both      | Yes     |
|                               | range_optimizer_max_mem_size<br>Yes                  | Yes         | Yes        | Both      | Yes     |
| rbr_exec_mode                 |                                                      |             | Yes        | Session   | Yes     |
| read_buffer_size Yes          |                                                      | Yes         | Yes        | Both      | Yes     |
| read_only                     | Yes                                                  | Yes         | Yes        | Global    | Yes     |
| read_rnd_buffer_size Yes      |                                                      | Yes         | Yes        | Both      | Yes     |
| relay_log                     | Yes                                                  | Yes         | Yes        | Global    | No      |
| relay_log_basename            |                                                      |             | Yes        | Global    | No      |
| relay_log_index               | Yes                                                  | Yes         | Yes        | Global    | No      |
| relay_log_info_fileYes        |                                                      | Yes         | Yes        | Global    | No      |
| relay_log_info_repository Yes |                                                      | Yes         | Yes        | Global    | Yes     |
| relay_log_purge Yes           |                                                      | Yes         | Yes        | Global    | Yes     |
| relay_log_recoveryYes         |                                                      | Yes         | Yes        | Global    | No      |
| relay_log_space_limit Yes     |                                                      | Yes         | Yes        | Global    | No      |
|                               | replication_optimize_for_static_plugin_config<br>Yes | Yes         | Yes        | Global    | Yes     |
|                               | replication_sender_observe_commit_only<br>Yes        | Yes         | Yes        | Global    | Yes     |
| report_host                   | Yes                                                  | Yes         | Yes        | Global    | No      |
| report_password Yes           |                                                      | Yes         | Yes        | Global    | No      |
| report_port                   | Yes                                                  | Yes         | Yes        | Global    | No      |
| report_user                   | Yes                                                  | Yes         | Yes        | Global    | No      |
| require_secure_transport Yes  |                                                      | Yes         | Yes        | Global    | Yes     |

| Name                           | Cmd-Line                                         | Option File | System Var | Var Scope | Dynamic |
|--------------------------------|--------------------------------------------------|-------------|------------|-----------|---------|
| rewriter_enabled               |                                                  |             | Yes        | Global    | Yes     |
| rewriter_verbose               |                                                  |             | Yes        | Global    | Yes     |
| rpl_semi_sync_master_enabled   | Yes                                              | Yes         | Yes        | Global    | Yes     |
| rpl_semi_sync_master_timeout   | Yes                                              | Yes         | Yes        | Global    | Yes     |
|                                | rpl_semi_sync_master_trace_level<br>Yes          | Yes         | Yes        | Global    | Yes     |
|                                | rpl_semi_sync_master_wait_for_slave_count<br>Yes | Yes         | Yes        | Global    | Yes     |
|                                | rpl_semi_sync_master_wait_no_slave<br>Yes        | Yes         | Yes        | Global    | Yes     |
|                                | rpl_semi_sync_master_wait_point<br>Yes           | Yes         | Yes        | Global    | Yes     |
| rpl_semi_sync_slave_enabled    | Yes                                              | Yes         | Yes        | Global    | Yes     |
|                                | rpl_semi_sync_slave_trace_level<br>Yes           | Yes         | Yes        | Global    | Yes     |
| rpl_stop_slave_timeout Ys      |                                                  | Yes         | Yes        | Global    | Yes     |
| secure_auth                    | Yes                                              | Yes         | Yes        | Global    | Yes     |
| secure_file_priv               | Yes                                              | Yes         | Yes        | Global    | No      |
| server_id                      | Yes                                              | Yes         | Yes        | Global    | Yes     |
| server_id_bits                 | Yes                                              | Yes         | Yes        | Global    | No      |
| server_uuid                    |                                                  |             | Yes        | Global    | No      |
| session_track_gtidsYes         |                                                  | Yes         | Yes        | Both      | Yes     |
| session_track_schema Ys        |                                                  | Yes         | Yes        | Both      | Yes     |
| session_track_state_change     | Yes                                              | Yes         | Yes        | Both      | Yes     |
| session_track_system_variables | Yes                                              | Yes         | Yes        | Both      | Yes     |
| session_track_transaction_info | Yes                                              | Yes         | Yes        | Both      | Yes     |
|                                | sha256_password_auto_generate_rsa_keys<br>Yes    | Yes         | Yes        | Global    | No      |
|                                | sha256_password_private_key_path<br>Yes          | Yes         | Yes        | Global    | No      |
| sha256_password_proxy_users    | Yes                                              | Yes         | Yes        | Global    | Yes     |
|                                | sha256_password_public_key_path<br>Yes           | Yes         | Yes        | Global    | No      |
| shared_memory Yes              |                                                  | Yes         | Yes        | Global    | No      |
| shared_memory_base_name        | Yes                                              | Yes         | Yes        | Global    | No      |
| show_compatibility_56 Yes      |                                                  | Yes         | Yes        | Global    | Yes     |
| show_create_table_verbosity    | Yes                                              | Yes         | Yes        | Both      | Yes     |
| show_old_temporals Yes         |                                                  | Yes         | Yes        | Both      | Yes     |
| skip_external_locking Yes      |                                                  | Yes         | Yes        | Global    | No      |
| skip_name_resolveYes           |                                                  | Yes         | Yes        | Global    | No      |
| skip_networking Yes            |                                                  | Yes         | Yes        | Global    | No      |
| skip_show_database Yes         |                                                  | Yes         | Yes        | Global    | No      |
| skip_slave_start Yes           |                                                  | Yes         | Yes        | Global    | No      |
| slave_allow_batching Yes       |                                                  | Yes         | Yes        | Global    | Yes     |
| slave_checkpoint_group Yes     |                                                  | Yes         | Yes        | Global    | Yes     |
| slave_checkpoint_period Yes    |                                                  | Yes         | Yes        | Global    | Yes     |
| slave_compressed_protocol      | Yes                                              | Yes         | Yes        | Global    | Yes     |
| slave_exec_modeYes             |                                                  | Yes         | Yes        | Global    | Yes     |
| slave_load_tmpdirYes           |                                                  | Yes         | Yes        | Global    | No      |

| Name                          | Cmd-Line | Option File | System Var | Var Scope | Dynamic |
|-------------------------------|----------|-------------|------------|-----------|---------|
| slave_max_allowed_packet      | Yes      | Yes         | Yes        | Global    | Yes     |
| slave_net_timeoutYes          |          | Yes         | Yes        | Global    | Yes     |
| slave_parallel_typeYes        |          | Yes         | Yes        | Global    | Yes     |
| slave_parallel_workers Yes    |          | Yes         | Yes        | Global    | Yes     |
| slave_pending_jobs_size_max   | Yes      | Yes         | Yes        | Global    | Yes     |
| slave_preserve_commit_order   | Yes      | Yes         | Yes        | Global    | Yes     |
| slave_rows_search_algorithms  | Yes      | Yes         | Yes        | Global    | Yes     |
| slave_skip_errorsYes          |          | Yes         | Yes        | Global    | No      |
| slave_sql_verify_checksum     | Yes      | Yes         | Yes        | Global    | Yes     |
| slave_transaction_retries Yes |          | Yes         | Yes        | Global    | Yes     |
| slave_type_conversions Yes    |          | Yes         | Yes        | Global    | Yes     |
| slow_launch_timeYes           |          | Yes         | Yes        | Global    | Yes     |
| slow_query_log                | Yes      | Yes         | Yes        | Global    | Yes     |
| slow_query_log_fileYs         |          | Yes         | Yes        | Global    | Yes     |
| socket                        | Yes      | Yes         | Yes        | Global    | No      |
| sort_buffer_size Yes          |          | Yes         | Yes        | Both      | Yes     |
| sql_auto_is_null              |          |             | Yes        | Both      | Yes     |
| sql_big_selects               |          |             | Yes        | Both      | Yes     |
| sql_buffer_result             |          |             | Yes        | Both      | Yes     |
| sql_log_bin                   |          |             | Yes        | Session   | Yes     |
| sql_log_off                   |          |             | Yes        | Both      | Yes     |
| sql_mode                      | Yes      | Yes         | Yes        | Both      | Yes     |
| sql_notes                     |          |             | Yes        | Both      | Yes     |
| sql_quote_show_create         |          |             | Yes        | Both      | Yes     |
| sql_safe_updates              |          |             | Yes        | Both      | Yes     |
| sql_select_limit              |          |             | Yes        | Both      | Yes     |
| sql_slave_skip_counter        |          |             | Yes        | Global    | Yes     |
| sql_warnings                  |          |             | Yes        | Both      | Yes     |
| ssl_ca                        | Yes      | Yes         | Yes        | Global    | No      |
| ssl_capath                    | Yes      | Yes         | Yes        | Global    | No      |
| ssl_cert                      | Yes      | Yes         | Yes        | Global    | No      |
| ssl_cipher                    | Yes      | Yes         | Yes        | Global    | No      |
| ssl_crl                       | Yes      | Yes         | Yes        | Global    | No      |
| ssl_crlpath                   | Yes      | Yes         | Yes        | Global    | No      |
| ssl_key                       | Yes      | Yes         | Yes        | Global    | No      |
| stored_program_cache Yes      |          | Yes         | Yes        | Global    | Yes     |
| super_read_only Yes           |          | Yes         | Yes        | Global    | Yes     |
| sync_binlog                   | Yes      | Yes         | Yes        | Global    | Yes     |
| sync_frm                      | Yes      | Yes         | Yes        | Global    | Yes     |
| sync_master_infoYes           |          | Yes         | Yes        | Global    | Yes     |
| sync_relay_log                | Yes      | Yes         | Yes        | Global    | Yes     |

| Name                                 | Cmd-Line                                    | Option File | System Var | Var Scope | Dynamic |
|--------------------------------------|---------------------------------------------|-------------|------------|-----------|---------|
| sync_relay_log_infoYes               |                                             | Yes         | Yes        | Global    | Yes     |
| system_time_zone                     |                                             |             | Yes        | Global    | No      |
| table_definition_cache Yes           |                                             | Yes         | Yes        | Global    | Yes     |
| table_open_cacheYes                  |                                             | Yes         | Yes        | Global    | Yes     |
| table_open_cache_instances           | Yes                                         | Yes         | Yes        | Global    | No      |
| thread_cache_sizeYes                 |                                             | Yes         | Yes        | Global    | Yes     |
| thread_handling Yes                  |                                             | Yes         | Yes        | Global    | No      |
| thread_pool_algorithm Yes            |                                             | Yes         | Yes        | Global    | No      |
| thread_pool_high_priority_connection | Yes                                         | Yes         | Yes        | Both      | Yes     |
| thread_pool_max_unused_threads       | Yes                                         | Yes         | Yes        | Global    | Yes     |
| thread_pool_prio_kickup_timer        | Yes                                         | Yes         | Yes        | Global    | Yes     |
| thread_pool_sizeYes                  |                                             | Yes         | Yes        | Global    | No      |
| thread_pool_stall_limit Yes          |                                             | Yes         | Yes        | Global    | Yes     |
| thread_stack                         | Yes                                         | Yes         | Yes        | Global    | No      |
| time_format                          |                                             |             | Yes        | Global    | No      |
| time_zone                            |                                             |             | Yes        | Both      | Yes     |
| timestamp                            |                                             |             | Yes        | Session   | Yes     |
| tls_version                          | Yes                                         | Yes         | Yes        | Global    | No      |
| tmp_table_size                       | Yes                                         | Yes         | Yes        | Both      | Yes     |
| tmpdir                               | Yes                                         | Yes         | Yes        | Global    | No      |
| transaction_alloc_block_size         | Yes                                         | Yes         | Yes        | Both      | Yes     |
| transaction_allow_batching           |                                             |             | Yes        | Session   | Yes     |
| transaction_isolation Yes            |                                             | Yes         |            |           | Yes     |
| - Variable:<br>tx_isolation          |                                             |             | Yes        | Both      | Yes     |
| transaction_prealloc_size Yes        |                                             | Yes         | Yes        | Both      | Yes     |
| transaction_read_only Yes            |                                             | Yes         |            |           | Yes     |
| - Variable:<br>tx_read_only          |                                             |             | Yes        | Both      | Yes     |
| transaction_write_set_extraction     | Yes                                         | Yes         | Yes        | Both      | Yes     |
| tx_isolation                         |                                             |             | Yes        | Both      | Yes     |
| tx_read_only                         |                                             |             | Yes        | Both      | Yes     |
| unique_checks                        |                                             |             | Yes        | Both      | Yes     |
| updatable_views_with_limit           | Yes                                         | Yes         | Yes        | Both      | Yes     |
| validate_password_check_user_name    | Yes                                         | Yes         | Yes        | Global    | Yes     |
| validate_password_dictionary_file    | Yes                                         | Yes         | Yes        | Global    | Varies  |
| validate_password_length Yes         |                                             | Yes         | Yes        | Global    | Yes     |
| validate_password_mixed_case_count   | Yes                                         | Yes         | Yes        | Global    | Yes     |
| validate_password_number_count       | Yes                                         | Yes         | Yes        | Global    | Yes     |
| validate_password_policy Yes         |                                             | Yes         | Yes        | Global    | Yes     |
|                                      | validate_password_special_char_count<br>Yes | Yes         | Yes        | Global    | Yes     |

| Name                          | Cmd-Line | Option File | System Var | Var Scope | Dynamic |
|-------------------------------|----------|-------------|------------|-----------|---------|
| version                       |          |             | Yes        | Global    | No      |
| version_comment               |          |             | Yes        | Global    | No      |
| version_compile_machine       |          |             | Yes        | Global    | No      |
| version_compile_os            |          |             | Yes        | Global    | No      |
| version_tokens_session Ye     |          | Yes         | Yes        | Both      | Yes     |
| version_tokens_session_number | Yes      | Yes         | Yes        | Both      | No      |
| wait_timeout                  | Yes      | Yes         | Yes        | Both      | Yes     |
| warning_count                 |          |             | Yes        | Session   | No      |

#### **Notes:**

1. This option is dynamic, but should be set only by server. You should not set this variable manually.

# <span id="page-93-0"></span>**5.1.5 Server Status Variable Reference**

The following table lists all status variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the variables. Where appropriate, direct links to further information about the items are provided.

**Table 5.3 Status Variable Summary**

| Variable Name                 | Variable Type | Variable Scope |
|-------------------------------|---------------|----------------|
| Aborted_clients               | Integer       | Global         |
| Aborted_connects              | Integer       | Global         |
| Audit_log_current_size        | Integer       | Global         |
| Audit_log_event_max_drop_size | Integer       | Global         |
| Audit_log_events              | Integer       | Global         |
| Audit_log_events_filtered     | Integer       | Global         |
| Audit_log_events_lost         | Integer       | Global         |
| Audit_log_events_written      | Integer       | Global         |
| Audit_log_total_size          | Integer       | Global         |
| Audit_log_write_waits         | Integer       | Global         |
| Binlog_cache_disk_use         | Integer       | Global         |
| Binlog_cache_use              | Integer       | Global         |
| Binlog_stmt_cache_disk_use    | Integer       | Global         |
| Binlog_stmt_cache_use         | Integer       | Global         |
| Bytes_received                | Integer       | Both           |
| Bytes_sent                    | Integer       | Both           |
| Com_admin_commands            | Integer       | Both           |
| Com_alter_db                  | Integer       | Both           |
| Com_alter_db_upgrade          | Integer       | Both           |
| Com_alter_event               | Integer       | Both           |
| Com_alter_function            | Integer       | Both           |
| Com_alter_procedure           | Integer       | Both           |

| Variable Name          | Variable Type | Variable Scope |
|------------------------|---------------|----------------|
| Com_alter_server       | Integer       | Both           |
| Com_alter_table        | Integer       | Both           |
| Com_alter_tablespace   | Integer       | Both           |
| Com_alter_user         | Integer       | Both           |
| Com_analyze            | Integer       | Both           |
| Com_assign_to_keycache | Integer       | Both           |
| Com_begin              | Integer       | Both           |
| Com_binlog             | Integer       | Both           |
| Com_call_procedure     | Integer       | Both           |
| Com_change_db          | Integer       | Both           |
| Com_change_master      | Integer       | Both           |
| Com_change_repl_filter | Integer       | Both           |
| Com_check              | Integer       | Both           |
| Com_checksum           | Integer       | Both           |
| Com_commit             | Integer       | Both           |
| Com_create_db          | Integer       | Both           |
| Com_create_event       | Integer       | Both           |
| Com_create_function    | Integer       | Both           |
| Com_create_index       | Integer       | Both           |
| Com_create_procedure   | Integer       | Both           |
| Com_create_server      | Integer       | Both           |
| Com_create_table       | Integer       | Both           |
| Com_create_trigger     | Integer       | Both           |
| Com_create_udf         | Integer       | Both           |
| Com_create_user        | Integer       | Both           |
| Com_create_view        | Integer       | Both           |
| Com_dealloc_sql        | Integer       | Both           |
| Com_delete             | Integer       | Both           |
| Com_delete_multi       | Integer       | Both           |
| Com_do                 | Integer       | Both           |
| Com_drop_db            | Integer       | Both           |
| Com_drop_event         | Integer       | Both           |
| Com_drop_function      | Integer       | Both           |
| Com_drop_index         | Integer       | Both           |
| Com_drop_procedure     | Integer       | Both           |
| Com_drop_server        | Integer       | Both           |
| Com_drop_table         | Integer       | Both           |
| Com_drop_trigger       | Integer       | Both           |
| Com_drop_user          | Integer       | Both           |
| Com_drop_view          | Integer       | Both           |
| Com_empty_query        | Integer       | Both           |

| Variable Name               | Variable Type | Variable Scope |
|-----------------------------|---------------|----------------|
| Com_execute_sql             | Integer       | Both           |
| Com_explain_other           | Integer       | Both           |
| Com_flush                   | Integer       | Both           |
| Com_get_diagnostics         | Integer       | Both           |
| Com_grant                   | Integer       | Both           |
| Com_group_replication_start | Integer       | Global         |
| Com_group_replication_stop  | Integer       | Global         |
| Com_ha_close                | Integer       | Both           |
| Com_ha_open                 | Integer       | Both           |
| Com_ha_read                 | Integer       | Both           |
| Com_help                    | Integer       | Both           |
| Com_insert                  | Integer       | Both           |
| Com_insert_select           | Integer       | Both           |
| Com_install_plugin          | Integer       | Both           |
| Com_kill                    | Integer       | Both           |
| Com_load                    | Integer       | Both           |
| Com_lock_tables             | Integer       | Both           |
| Com_optimize                | Integer       | Both           |
| Com_preload_keys            | Integer       | Both           |
| Com_prepare_sql             | Integer       | Both           |
| Com_purge                   | Integer       | Both           |
| Com_purge_before_date       | Integer       | Both           |
| Com_release_savepoint       | Integer       | Both           |
| Com_rename_table            | Integer       | Both           |
| Com_rename_user             | Integer       | Both           |
| Com_repair                  | Integer       | Both           |
| Com_replace                 | Integer       | Both           |
| Com_replace_select          | Integer       | Both           |
| Com_reset                   | Integer       | Both           |
| Com_resignal                | Integer       | Both           |
| Com_revoke                  | Integer       | Both           |
| Com_revoke_all              | Integer       | Both           |
| Com_rollback                | Integer       | Both           |
| Com_rollback_to_savepoint   | Integer       | Both           |
| Com_savepoint               | Integer       | Both           |
| Com_select                  | Integer       | Both           |
| Com_set_option              | Integer       | Both           |
| Com_show_authors            | Integer       | Both           |
| Com_show_binlog_events      | Integer       | Both           |
| Com_show_binlogs            | Integer       | Both           |
| Com_show_charsets           | Integer       | Both           |

| Variable Name             | Variable Type | Variable Scope |
|---------------------------|---------------|----------------|
| Com_show_collations       | Integer       | Both           |
| Com_show_contributors     | Integer       | Both           |
| Com_show_create_db        | Integer       | Both           |
| Com_show_create_event     | Integer       | Both           |
| Com_show_create_func      | Integer       | Both           |
| Com_show_create_proc      | Integer       | Both           |
| Com_show_create_table     | Integer       | Both           |
| Com_show_create_trigger   | Integer       | Both           |
| Com_show_create_user      | Integer       | Both           |
| Com_show_databases        | Integer       | Both           |
| Com_show_engine_logs      | Integer       | Both           |
| Com_show_engine_mutex     | Integer       | Both           |
| Com_show_engine_status    | Integer       | Both           |
| Com_show_errors           | Integer       | Both           |
| Com_show_events           | Integer       | Both           |
| Com_show_fields           | Integer       | Both           |
| Com_show_function_code    | Integer       | Both           |
| Com_show_function_status  | Integer       | Both           |
| Com_show_grants           | Integer       | Both           |
| Com_show_keys             | Integer       | Both           |
| Com_show_master_status    | Integer       | Both           |
| Com_show_ndb_status       | Integer       | Both           |
| Com_show_open_tables      | Integer       | Both           |
| Com_show_plugins          | Integer       | Both           |
| Com_show_privileges       | Integer       | Both           |
| Com_show_procedure_code   | Integer       | Both           |
| Com_show_procedure_status | Integer       | Both           |
| Com_show_processlist      | Integer       | Both           |
| Com_show_profile          | Integer       | Both           |
| Com_show_profiles         | Integer       | Both           |
| Com_show_relaylog_events  | Integer       | Both           |
| Com_show_slave_hosts      | Integer       | Both           |
| Com_show_slave_status     | Integer       | Both           |
| Com_show_status           | Integer       | Both           |
| Com_show_storage_engines  | Integer       | Both           |
| Com_show_table_status     | Integer       | Both           |
| Com_show_tables           | Integer       | Both           |
| Com_show_triggers         | Integer       | Both           |
| Com_show_variables        | Integer       | Both           |
| Com_show_warnings         | Integer       | Both           |
| Com_shutdown              | Integer       | Both           |

| Variable Name                              | Variable Type | Variable Scope |
|--------------------------------------------|---------------|----------------|
| Com_signal                                 | Integer       | Both           |
| Com_slave_start                            | Integer       | Both           |
| Com_slave_stop                             | Integer       | Both           |
| Com_stmt_close                             | Integer       | Both           |
| Com_stmt_execute                           | Integer       | Both           |
| Com_stmt_fetch                             | Integer       | Both           |
| Com_stmt_prepare                           | Integer       | Both           |
| Com_stmt_reprepare                         | Integer       | Both           |
| Com_stmt_reset                             | Integer       | Both           |
| Com_stmt_send_long_data                    | Integer       | Both           |
| Com_truncate                               | Integer       | Both           |
| Com_uninstall_plugin                       | Integer       | Both           |
| Com_unlock_tables                          | Integer       | Both           |
| Com_update                                 | Integer       | Both           |
| Com_update_multi                           | Integer       | Both           |
| Com_xa_commit                              | Integer       | Both           |
| Com_xa_end                                 | Integer       | Both           |
| Com_xa_prepare                             | Integer       | Both           |
| Com_xa_recover                             | Integer       | Both           |
| Com_xa_rollback                            | Integer       | Both           |
| Com_xa_start                               | Integer       | Both           |
| Compression                                | Integer       | Session        |
| Connection_control_delay_generated Integer |               | Global         |
| Connection_errors_accept                   | Integer       | Global         |
| Connection_errors_internal                 | Integer       | Global         |
| Connection_errors_max_connections Iteger   |               | Global         |
| Connection_errors_peer_address Integer     |               | Global         |
| Connection_errors_select                   | Integer       | Global         |
| Connection_errors_tcpwrap                  | Integer       | Global         |
| Connections                                | Integer       | Global         |
| Created_tmp_disk_tables                    | Integer       | Both           |
| Created_tmp_files                          | Integer       | Global         |
| Created_tmp_tables                         | Integer       | Both           |
| Delayed_errors                             | Integer       | Global         |
| Delayed_insert_threads                     | Integer       | Global         |
| Delayed_writes                             | Integer       | Global         |
| Firewall_access_denied                     | Integer       | Global         |
| Firewall_access_granted                    | Integer       | Global         |
| Firewall_access_suspicious                 | Integer       | Global         |
| Firewall_cached_entries                    | Integer       | Global         |
| Flush_commands                             | Integer       | Global         |

| Variable Name                                 | Variable Type | Variable Scope |
|-----------------------------------------------|---------------|----------------|
| group_replication_primary_memberString        |               | Global         |
| Handler_commit                                | Integer       | Both           |
| Handler_delete                                | Integer       | Both           |
| Handler_discover                              | Integer       | Both           |
| Handler_external_lock                         | Integer       | Both           |
| Handler_mrr_init                              | Integer       | Both           |
| Handler_prepare                               | Integer       | Both           |
| Handler_read_first                            | Integer       | Both           |
| Handler_read_key                              | Integer       | Both           |
| Handler_read_last                             | Integer       | Both           |
| Handler_read_next                             | Integer       | Both           |
| Handler_read_prev                             | Integer       | Both           |
| Handler_read_rnd                              | Integer       | Both           |
| Handler_read_rnd_next                         | Integer       | Both           |
| Handler_rollback                              | Integer       | Both           |
| Handler_savepoint                             | Integer       | Both           |
| Handler_savepoint_rollback                    | Integer       | Both           |
| Handler_update                                | Integer       | Both           |
| Handler_write                                 | Integer       | Both           |
| Innodb_available_undo_logs                    | Integer       | Global         |
| Innodb_buffer_pool_bytes_data                 | Integer       | Global         |
| Innodb_buffer_pool_bytes_dirty                | Integer       | Global         |
| Innodb_buffer_pool_dump_status String         |               | Global         |
| Innodb_buffer_pool_load_status                | String        | Global         |
| Innodb_buffer_pool_pages_data                 | Integer       | Global         |
| Innodb_buffer_pool_pages_dirty                | Integer       | Global         |
| Innodb_buffer_pool_pages_flushedInteger       |               | Global         |
| Innodb_buffer_pool_pages_free                 | Integer       | Global         |
| Innodb_buffer_pool_pages_latchedInteger       |               | Global         |
| Innodb_buffer_pool_pages_misc                 | Integer       | Global         |
| Innodb_buffer_pool_pages_total                | Integer       | Global         |
| Innodb_buffer_pool_read_ahead                 | Integer       | Global         |
| Innodb_buffer_pool_read_ahead_evicted Integer |               | Global         |
| Innodb_buffer_pool_read_ahead_rndInteger      |               | Global         |
| Innodb_buffer_pool_read_requestsInteger       |               | Global         |
| Innodb_buffer_pool_reads                      | Integer       | Global         |
| Innodb_buffer_pool_resize_status String       |               | Global         |
| Innodb_buffer_pool_wait_free                  | Integer       | Global         |
| Innodb_buffer_pool_write_requestsInteger      |               | Global         |
| Innodb_data_fsyncs                            | Integer       | Global         |
| Innodb_data_pending_fsyncs                    | Integer       | Global         |

| Variable Name                  | Variable Type | Variable Scope |
|--------------------------------|---------------|----------------|
| Innodb_data_pending_reads      | Integer       | Global         |
| Innodb_data_pending_writes     | Integer       | Global         |
| Innodb_data_read               | Integer       | Global         |
| Innodb_data_reads              | Integer       | Global         |
| Innodb_data_writes             | Integer       | Global         |
| Innodb_data_written            | Integer       | Global         |
| Innodb_dblwr_pages_written     | Integer       | Global         |
| Innodb_dblwr_writes            | Integer       | Global         |
| Innodb_have_atomic_builtins    | Integer       | Global         |
| Innodb_log_waits               | Integer       | Global         |
| Innodb_log_write_requests      | Integer       | Global         |
| Innodb_log_writes              | Integer       | Global         |
| Innodb_num_open_files          | Integer       | Global         |
| Innodb_os_log_fsyncs           | Integer       | Global         |
| Innodb_os_log_pending_fsyncs   | Integer       | Global         |
| Innodb_os_log_pending_writes   | Integer       | Global         |
| Innodb_os_log_written          | Integer       | Global         |
| Innodb_page_size               | Integer       | Global         |
| Innodb_pages_created           | Integer       | Global         |
| Innodb_pages_read              | Integer       | Global         |
| Innodb_pages_written           | Integer       | Global         |
| Innodb_row_lock_current_waits  | Integer       | Global         |
| Innodb_row_lock_time           | Integer       | Global         |
| Innodb_row_lock_time_avg       | Integer       | Global         |
| Innodb_row_lock_time_max       | Integer       | Global         |
| Innodb_row_lock_waits          | Integer       | Global         |
| Innodb_rows_deleted            | Integer       | Global         |
| Innodb_rows_inserted           | Integer       | Global         |
| Innodb_rows_read               | Integer       | Global         |
| Innodb_rows_updated            | Integer       | Global         |
| Innodb_truncated_status_writes | Integer       | Global         |
| Key_blocks_not_flushed         | Integer       | Global         |
| Key_blocks_unused              | Integer       | Global         |
| Key_blocks_used                | Integer       | Global         |
| Key_read_requests              | Integer       | Global         |
| Key_reads                      | Integer       | Global         |
| Key_write_requests             | Integer       | Global         |
| Key_writes                     | Integer       | Global         |
| Last_query_cost                | Numeric       | Session        |
| Last_query_partial_plans       | Integer       | Session        |
| Locked_connects                | Integer       | Global         |

| Variable Name                              | Variable Type | Variable Scope |
|--------------------------------------------|---------------|----------------|
| Max_execution_time_exceeded                | Integer       | Both           |
| Max_execution_time_set                     | Integer       | Both           |
| Max_execution_time_set_failed              | Integer       | Both           |
| Max_used_connections                       | Integer       | Global         |
| Max_used_connections_time                  | Datetime      | Global         |
| mecab_charset                              | String        | Global         |
| Mysqlx_address                             | String        | Global         |
| Mysqlx_bytes_received                      | Integer       | Both           |
| Mysqlx_bytes_sent                          | Integer       | Both           |
| Mysqlx_connection_accept_errorsInteger     |               | Both           |
| Mysqlx_connection_errors                   | Integer       | Both           |
| Mysqlx_connections_accepted                | Integer       | Global         |
| Mysqlx_connections_closed                  | Integer       | Global         |
| Mysqlx_connections_rejected                | Integer       | Global         |
| Mysqlx_crud_create_view                    | Integer       | Both           |
| Mysqlx_crud_delete                         | Integer       | Both           |
| Mysqlx_crud_drop_view                      | Integer       | Both           |
| Mysqlx_crud_find                           | Integer       | Both           |
| Mysqlx_crud_insert                         | Integer       | Both           |
| Mysqlx_crud_modify_view                    | Integer       | Both           |
| Mysqlx_crud_update                         | Integer       | Both           |
| Mysqlx_errors_sent                         | Integer       | Both           |
| Mysqlx_errors_unknown_message_type Integer |               | Both           |
| Mysqlx_expect_close                        | Integer       | Both           |
| Mysqlx_expect_open                         | Integer       | Both           |
| Mysqlx_init_error                          | Integer       | Both           |
| Mysqlx_notice_other_sent                   | Integer       | Both           |
| Mysqlx_notice_warning_sent                 | Integer       | Both           |
| Mysqlx_port                                | String        | Global         |
| Mysqlx_rows_sent                           | Integer       | Both           |
| Mysqlx_sessions                            | Integer       | Global         |
| Mysqlx_sessions_accepted                   | Integer       | Global         |
| Mysqlx_sessions_closed                     | Integer       | Global         |
| Mysqlx_sessions_fatal_error                | Integer       | Global         |
| Mysqlx_sessions_killed                     | Integer       | Global         |
| Mysqlx_sessions_rejected                   | Integer       | Global         |
| Mysqlx_socket                              | String        | Global         |
| Mysqlx_ssl_accept_renegotiates             | Integer       | Global         |
| Mysqlx_ssl_accepts                         | Integer       | Global         |
| Mysqlx_ssl_active                          | Integer       | Both           |
| Mysqlx_ssl_cipher                          | Integer       | Both           |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| Mysqlx_ssl_cipher_list                       | Integer       | Both           |
| Mysqlx_ssl_ctx_verify_depth                  | Integer       | Both           |
| Mysqlx_ssl_ctx_verify_mode                   | Integer       | Both           |
| Mysqlx_ssl_finished_accepts                  | Integer       | Global         |
| Mysqlx_ssl_server_not_after                  | Integer       | Global         |
| Mysqlx_ssl_server_not_before                 | Integer       | Global         |
| Mysqlx_ssl_verify_depth                      | Integer       | Global         |
| Mysqlx_ssl_verify_mode                       | Integer       | Global         |
| Mysqlx_ssl_version                           | Integer       | Both           |
| Mysqlx_stmt_create_collection                | Integer       | Both           |
| Mysqlx_stmt_create_collection_index Integer  |               | Both           |
| Mysqlx_stmt_disable_notices                  | Integer       | Both           |
| Mysqlx_stmt_drop_collection                  | Integer       | Both           |
| Mysqlx_stmt_drop_collection_indexInteger     |               | Both           |
| Mysqlx_stmt_enable_notices                   | Integer       | Both           |
| Mysqlx_stmt_ensure_collection                | String        | Both           |
| Mysqlx_stmt_execute_mysqlx                   | Integer       | Both           |
| Mysqlx_stmt_execute_sql                      | Integer       | Both           |
| Mysqlx_stmt_execute_xplugin                  | Integer       | Both           |
| Mysqlx_stmt_kill_client                      | Integer       | Both           |
| Mysqlx_stmt_list_clients                     | Integer       | Both           |
| Mysqlx_stmt_list_notices                     | Integer       | Both           |
| Mysqlx_stmt_list_objects                     | Integer       | Both           |
| Mysqlx_stmt_ping                             | Integer       | Both           |
| Mysqlx_worker_threads                        | Integer       | Global         |
| Mysqlx_worker_threads_active                 | Integer       | Global         |
| Ndb_api_adaptive_send_deferred_count Integer |               | Global         |
| Ndb_api_adaptive_send_deferred_count_session | Integer       | Global         |
| Ndb_api_adaptive_send_deferred_count_slave   | Integer       | Global         |
| Ndb_api_adaptive_send_forced_count Integer   |               | Global         |
| Ndb_api_adaptive_send_forced_count_session   | Integer       | Global         |
| Ndb_api_adaptive_send_forced_count_slave     | Integer       | Global         |
| Ndb_api_adaptive_send_unforced_count Integer |               | Global         |
| Ndb_api_adaptive_send_unforced_count_session | Integer       | Global         |
| Ndb_api_adaptive_send_unforced_count_slave   | Integer       | Global         |
| Ndb_api_bytes_received_count                 | Integer       | Global         |
| Ndb_api_bytes_received_count_session Integer |               | Session        |
| Ndb_api_bytes_received_count_slave Intger    |               | Global         |
| Ndb_api_bytes_sent_count                     | Integer       | Global         |
| Ndb_api_bytes_sent_count_sessionIteger       |               | Session        |
| Ndb_api_bytes_sent_count_slave Integer       |               | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| Ndb_api_event_bytes_count                    | Integer       | Global         |
| Ndb_api_event_bytes_count_injector Integer   |               | Global         |
| Ndb_api_event_data_count                     | Integer       | Global         |
| Ndb_api_event_data_count_injectorInteger     |               | Global         |
| Ndb_api_event_nondata_count                  | Integer       | Global         |
| Ndb_api_event_nondata_count_injector Integer |               | Global         |
| Ndb_api_pk_op_count                          | Integer       | Global         |
| Ndb_api_pk_op_count_session                  | Integer       | Session        |
| Ndb_api_pk_op_count_slave                    | Integer       | Global         |
| Ndb_api_pruned_scan_count                    | Integer       | Global         |
| Ndb_api_pruned_scan_count_session Integer    |               | Session        |
| Ndb_api_pruned_scan_count_slaveInteger       |               | Global         |
| Ndb_api_range_scan_count                     | Integer       | Global         |
| Ndb_api_range_scan_count_sessionInteger      |               | Session        |
| Ndb_api_range_scan_count_slaveInteger        |               | Global         |
| Ndb_api_read_row_count                       | Integer       | Global         |
| Ndb_api_read_row_count_sessionInteger        |               | Session        |
| Ndb_api_read_row_count_slave                 | Integer       | Global         |
| Ndb_api_scan_batch_count                     | Integer       | Global         |
| Ndb_api_scan_batch_count_sessionInteger      |               | Session        |
| Ndb_api_scan_batch_count_slaveInteger        |               | Global         |
| Ndb_api_table_scan_count                     | Integer       | Global         |
| Ndb_api_table_scan_count_sessionIteger       |               | Session        |
| Ndb_api_table_scan_count_slave Integer       |               | Global         |
| Ndb_api_trans_abort_count                    | Integer       | Global         |
| Ndb_api_trans_abort_count_sessionInteger     |               | Session        |
| Ndb_api_trans_abort_count_slaveInteger       |               | Global         |
| Ndb_api_trans_close_count                    | Integer       | Global         |
| Ndb_api_trans_close_count_sessionInteger     |               | Session        |
| Ndb_api_trans_close_count_slaveInteger       |               | Global         |
| Ndb_api_trans_commit_count                   | Integer       | Global         |
| Ndb_api_trans_commit_count_session Integer   |               | Session        |
| Ndb_api_trans_commit_count_slaveInteger      |               | Global         |
| Ndb_api_trans_local_read_row_count Integer   |               | Global         |
| Ndb_api_trans_local_read_row_count_session   | Integer       | Session        |
| Ndb_api_trans_local_read_row_count_slave     | Integer       | Global         |
| Ndb_api_trans_start_count                    | Integer       | Global         |
| Ndb_api_trans_start_count_sessionInteger     |               | Session        |
| Ndb_api_trans_start_count_slave Integer      |               | Global         |
| Ndb_api_uk_op_count                          | Integer       | Global         |
| Ndb_api_uk_op_count_session                  | Integer       | Session        |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| Ndb_api_uk_op_count_slave                        | Integer       | Global         |
| Ndb_api_wait_exec_complete_count Ieger           |               | Global         |
| Ndb_api_wait_exec_complete_count_session         | Integer       | Session        |
| Ndb_api_wait_exec_complete_count_slave Integer   |               | Global         |
| Ndb_api_wait_meta_request_countInteger           |               | Global         |
| Ndb_api_wait_meta_request_count_session          | Integer       | Session        |
| Ndb_api_wait_meta_request_count_slave Integer    |               | Global         |
| Ndb_api_wait_nanos_count                         | Integer       | Global         |
| Ndb_api_wait_nanos_count_sessionInteger          |               | Session        |
| Ndb_api_wait_nanos_count_slaveInteger            |               | Global         |
| Ndb_api_wait_scan_result_count Integer           |               | Global         |
| Ndb_api_wait_scan_result_count_session Integer   |               | Session        |
| Ndb_api_wait_scan_result_count_slave Integer     |               | Global         |
| Ndb_cluster_node_id                              | Integer       | Global         |
| Ndb_config_from_host                             | Integer       | Both           |
| Ndb_config_from_port                             | Integer       | Both           |
| Ndb_conflict_fn_epoch                            | Integer       | Global         |
| Ndb_conflict_fn_epoch_trans                      | Integer       | Global         |
| Ndb_conflict_fn_epoch2                           | Integer       | Global         |
| Ndb_conflict_fn_epoch2_trans                     | Integer       | Global         |
| Ndb_conflict_fn_max                              | Integer       | Global         |
| Ndb_conflict_fn_max_del_win                      | Integer       | Global         |
| Ndb_conflict_fn_old                              | Integer       | Global         |
| Ndb_conflict_last_conflict_epoch                 | Integer       | Global         |
| Ndb_conflict_last_stable_epoch                   | Integer       | Global         |
| Ndb_conflict_reflected_op_discard_count Integer  |               | Global         |
| Ndb_conflict_reflected_op_prepare_count Integer  |               | Global         |
| Ndb_conflict_refresh_op_count                    | Integer       | Global         |
| Ndb_conflict_trans_conflict_commit_count Integer |               | Global         |
| Ndb_conflict_trans_detect_iter_count Integer     |               | Global         |
| Ndb_conflict_trans_reject_count                  | Integer       | Global         |
| Ndb_conflict_trans_row_conflict_count Integer    |               | Global         |
| Ndb_conflict_trans_row_reject_count Integer      |               | Global         |
| Ndb_epoch_delete_delete_count Integer            |               | Global         |
| Ndb_execute_count                                | Integer       | Global         |
| Ndb_last_commit_epoch_server                     | Integer       | Global         |
| Ndb_last_commit_epoch_session Integer            |               | Session        |
| Ndb_cluster_node_id                              | Integer       | Global         |
| Ndb_number_of_data_nodes                         | Integer       | Global         |
| Ndb_pruned_scan_count                            | Integer       | Global         |
| Ndb_pushed_queries_defined                       | Integer       | Global         |

| Variable Name                                      | Variable Type | Variable Scope |
|----------------------------------------------------|---------------|----------------|
| Ndb_pushed_queries_dropped                         | Integer       | Global         |
| Ndb_pushed_queries_executed                        | Integer       | Global         |
| Ndb_pushed_reads                                   | Integer       | Global         |
| Ndb_scan_count                                     | Integer       | Global         |
| Ndb_slave_max_replicated_epochInteger              |               | Global         |
| Not_flushed_delayed_rows                           | Integer       | Global         |
| Ongoing_anonymous_gtid_violating_transaction_count | Integer       | Global         |
| Ongoing_anonymous_transaction_count Integer        |               | Global         |
| Ongoing_automatic_gtid_violating_transaction_count | Integer       | Global         |
| Open_files                                         | Integer       | Global         |
| Open_streams                                       | Integer       | Global         |
| Open_table_definitions                             | Integer       | Global         |
| Open_tables                                        | Integer       | Both           |
| Opened_files                                       | Integer       | Global         |
| Opened_table_definitions                           | Integer       | Both           |
| Opened_tables                                      | Integer       | Both           |
| Performance_schema_accounts_lost Integer           |               | Global         |
| Performance_schema_cond_classes_lost Integer       |               | Global         |
| Performance_schema_cond_instances_lost Integer     |               | Global         |
| Performance_schema_digest_lostInteger              |               | Global         |
| Performance_schema_file_classes_lost Integer       |               | Global         |
| Performance_schema_file_handles_lost Integer       |               | Global         |
| Performance_schema_file_instances_lost Integer     |               | Global         |
| Performance_schema_hosts_lost Integer              |               | Global         |
| Performance_schema_index_stat_lost Integer         |               | Global         |
| Performance_schema_locker_lostInteger              |               | Global         |
| Performance_schema_memory_classes_lost             | Integer       | Global         |
| Performance_schema_metadata_lock_lost Integer      |               | Global         |
| Performance_schema_mutex_classes_lost Integer      |               | Global         |
| Performance_schema_mutex_instances_lost            | Integer       | Global         |
| Performance_schema_nested_statement_lost           | Integer       | Global         |
| Performance_schema_prepared_statements_lost        | Integer       | Global         |
| Performance_schema_program_lost Integer            |               | Global         |
| Performance_schema_rwlock_classes_lost Integer     |               | Global         |
| Performance_schema_rwlock_instances_lost           | Integer       | Global         |
| Performance_schema_session_connect_attrs_lost      | Integer       | Global         |
| Performance_schema_socket_classes_lost Integer     |               | Global         |
| Performance_schema_socket_instances_lost           | Integer       | Global         |
| Performance_schema_stage_classes_lost Integer      |               | Global         |
| Performance_schema_statement_classes_lost          | Integer       | Global         |
| Performance_schema_table_handles_lost Integer      |               | Global         |

| Variable Name                                   | Variable Type | Variable Scope |
|-------------------------------------------------|---------------|----------------|
| Performance_schema_table_instances_lost Integer |               | Global         |
| Performance_schema_table_lock_stat_lost Integer |               | Global         |
| Performance_schema_thread_classes_lost Integer  |               | Global         |
| Performance_schema_thread_instances_lost        | Integer       | Global         |
| Performance_schema_users_lost Integer           |               | Global         |
| Prepared_stmt_count                             | Integer       | Global         |
| Qcache_free_blocks                              | Integer       | Global         |
| Qcache_free_memory                              | Integer       | Global         |
| Qcache_hits                                     | Integer       | Global         |
| Qcache_inserts                                  | Integer       | Global         |
| Qcache_lowmem_prunes                            | Integer       | Global         |
| Qcache_not_cached                               | Integer       | Global         |
| Qcache_queries_in_cache                         | Integer       | Global         |
| Qcache_total_blocks                             | Integer       | Global         |
| Queries                                         | Integer       | Both           |
| Questions                                       | Integer       | Both           |
| Rewriter_number_loaded_rules                    | Integer       | Global         |
| Rewriter_number_reloads                         | Integer       | Global         |
| Rewriter_number_rewritten_queriesInteger        |               | Global         |
| Rewriter_reload_error                           | Boolean       | Global         |
| Rpl_semi_sync_master_clients                    | Integer       | Global         |
| Rpl_semi_sync_master_net_avg_wait_time Integer  |               | Global         |
| Rpl_semi_sync_master_net_wait_time Integer      |               | Global         |
| Rpl_semi_sync_master_net_waitsInteger           |               | Global         |
| Rpl_semi_sync_master_no_times Integer           |               | Global         |
| Rpl_semi_sync_master_no_tx                      | Integer       | Global         |
| Rpl_semi_sync_master_status                     | Boolean       | Global         |
| Rpl_semi_sync_master_timefunc_failures Integer  |               | Global         |
| Rpl_semi_sync_master_tx_avg_wait_time Integer   |               | Global         |
| Rpl_semi_sync_master_tx_wait_timeInteger        |               | Global         |
| Rpl_semi_sync_master_tx_waits                   | Integer       | Global         |
| Rpl_semi_sync_master_wait_pos_backtraverse      | Integer       | Global         |
| Rpl_semi_sync_master_wait_sessions Integer      |               | Global         |
| Rpl_semi_sync_master_yes_tx                     | Integer       | Global         |
| Rpl_semi_sync_slave_status                      | Boolean       | Global         |
| Rsa_public_key                                  | String        | Global         |
| Select_full_join                                | Integer       | Both           |
| Select_full_range_join                          | Integer       | Both           |
| Select_range                                    | Integer       | Both           |
| Select_range_check                              | Integer       | Both           |
| Select_scan                                     | Integer       | Both           |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| Slave_heartbeat_period                       | Numeric       | Global         |
| Slave_last_heartbeat                         | Datetime      | Global         |
| Slave_open_temp_tables                       | Integer       | Global         |
| Slave_received_heartbeats                    | Integer       | Global         |
| Slave_retried_transactions                   | Integer       | Global         |
| Slave_rows_last_search_algorithm_used String |               | Global         |
| Slave_running                                | String        | Global         |
| Slow_launch_threads                          | Integer       | Both           |
| Slow_queries                                 | Integer       | Both           |
| Sort_merge_passes                            | Integer       | Both           |
| Sort_range                                   | Integer       | Both           |
| Sort_rows                                    | Integer       | Both           |
| Sort_scan                                    | Integer       | Both           |
| Ssl_accept_renegotiates                      | Integer       | Global         |
| Ssl_accepts                                  | Integer       | Global         |
| Ssl_callback_cache_hits                      | Integer       | Global         |
| Ssl_cipher                                   | String        | Both           |
| Ssl_cipher_list                              | String        | Both           |
| Ssl_client_connects                          | Integer       | Global         |
| Ssl_connect_renegotiates                     | Integer       | Global         |
| Ssl_ctx_verify_depth                         | Integer       | Global         |
| Ssl_ctx_verify_mode                          | Integer       | Global         |
| Ssl_default_timeout                          | Integer       | Both           |
| Ssl_finished_accepts                         | Integer       | Global         |
| Ssl_finished_connects                        | Integer       | Global         |
| Ssl_server_not_after                         | Integer       | Both           |
| Ssl_server_not_before                        | Integer       | Both           |
| Ssl_session_cache_hits                       | Integer       | Global         |
| Ssl_session_cache_misses                     | Integer       | Global         |
| Ssl_session_cache_mode                       | String        | Global         |
| Ssl_session_cache_overflows                  | Integer       | Global         |
| Ssl_session_cache_size                       | Integer       | Global         |
| Ssl_session_cache_timeouts                   | Integer       | Global         |
| Ssl_sessions_reused                          | Integer       | Session        |
| Ssl_used_session_cache_entries Integer       |               | Global         |
| Ssl_verify_depth                             | Integer       | Both           |
| Ssl_verify_mode                              | Integer       | Both           |
| Ssl_version                                  | String        | Both           |
| Table_locks_immediate                        | Integer       | Global         |
| Table_locks_waited                           | Integer       | Global         |
| Table_open_cache_hits                        | Integer       | Both           |

| Variable Name                                 | Variable Type | Variable Scope |
|-----------------------------------------------|---------------|----------------|
| Table_open_cache_misses                       | Integer       | Both           |
| Table_open_cache_overflows                    | Integer       | Both           |
| Tc_log_max_pages_used                         | Integer       | Global         |
| Tc_log_page_size                              | Integer       | Global         |
| Tc_log_page_waits                             | Integer       | Global         |
| Threads_cached                                | Integer       | Global         |
| Threads_connected                             | Integer       | Global         |
| Threads_created                               | Integer       | Global         |
| Threads_running                               | Integer       | Global         |
| Uptime                                        | Integer       | Global         |
| Uptime_since_flush_status                     | Integer       | Global         |
| validate_password_dictionary_file_last_parsed | Datetime      | Global         |
| validate_password_dictionary_file_words_count | Integer       | Global         |

# <span id="page-107-0"></span>**5.1.6 Server Command Options**

When you start the mysqld server, you can specify program options using any of the methods described in Section 4.2.2, "Specifying Program Options". The most common methods are to provide options in an option file or on the command line. However, in most cases it is desirable to make sure that the server uses the same options each time it runs. The best way to ensure this is to list them in an option file. See Section 4.2.2.2, "Using Option Files". That section also describes option file format and syntax.

mysqld reads options from the [mysqld] and [server] groups. mysqld\_safe reads options from the [mysqld], [server], [mysqld\_safe], and [safe\_mysqld] groups. mysql.server reads options from the [mysqld] and [mysql.server] groups.

An embedded MySQL server usually reads options from the [server], [embedded], and [xxxxx\_SERVER] groups, where xxxxx is the name of the application into which the server is embedded.

mysqld accepts many command options. For a brief summary, execute this command:

mysqld --help

To see the full list, use this command:

mysqld --verbose --help

Some of the items in the list are actually system variables that can be set at server startup. These can be displayed at runtime using the SHOW VARIABLES statement. Some items displayed by the preceding mysqld command do not appear in SHOW VARIABLES output; this is because they are options only and not system variables.

The following list shows some of the most common server options. Additional options are described in other sections:

- Options that affect security: See Section 6.1.4, "Security-Related mysqld Options and Variables".
- SSL-related options: See Command Options for Encrypted Connections.
- Binary log control options: See Section 5.4.4, "The Binary Log".
- Replication-related options: See Section 16.1.6, "Replication and Binary Logging Options and Variables".

- Options for loading plugins such as pluggable storage engines: See Section 5.5.1, "Installing and Uninstalling Plugins".
- Options specific to particular storage engines: See Section 14.15, "InnoDB Startup Options and System Variables" and Section 15.2.1, "MyISAM Startup Options".

Some options control the size of buffers or caches. For a given buffer, the server might need to allocate internal data structures. These structures typically are allocated from the total memory allocated to the buffer, and the amount of space required might be platform dependent. This means that when you assign a value to an option that controls a buffer size, the amount of space actually available might differ from the value assigned. In some cases, the amount might be less than the value assigned. It is also possible that the server adjusts a value upward. For example, if you assign a value of 0 to an option for which the minimal value is 1024, the server sets the value to 1024.

Values for buffer sizes, lengths, and stack sizes are given in bytes unless otherwise specified.

Some options take file name values. Unless otherwise specified, the default file location is the data directory if the value is a relative path name. To specify the location explicitly, use an absolute path name. Suppose that the data directory is /var/mysql/data. If a file-valued option is given as a relative path name, it is located under /var/mysql/data. If the value is an absolute path name, its location is as given by the path name.

You can also set the values of server system variables at server startup by using variable names as options. To assign a value to a server system variable, use an option of the form --var\_name=value. For example, --sort\_buffer\_size=384M sets the sort\_buffer\_size variable to a value of 384MB.

When you assign a value to a variable, MySQL might automatically correct the value to stay within a given range, or adjust the value to the closest permissible value if only certain values are permitted.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement, specify this maximum by using an option of the form --maximum-var\_name=value at server startup.

You can change the values of most system variables at runtime with the SET statement. See Section 13.7.4.1, "SET Syntax for Variable Assignment".

[Section 5.1.7, "Server System Variables",](#page-133-0) provides a full description for all variables, and additional information for setting them at server startup and runtime. For information on changing system variables, see [Section 5.1.1, "Configuring the Server"](#page-33-1).

<span id="page-108-2"></span>• [--help](#page-108-2), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a short help message and exit. Use both the [--verbose](#page-132-2) and [--help](#page-108-2) options to see the full message.

<span id="page-108-0"></span>• [--allow-suspicious-udfs](#page-108-0)

| Command-Line Format | allow-suspicious-udfs[={OFF ON}] |
|---------------------|----------------------------------|
| Type                | Boolean                          |
| Default Value       | OFF                              |

This option controls whether loadable functions that have only an xxx symbol for the main function can be loaded. By default, the option is off and only loadable functions that have at least one auxiliary symbol can be loaded; this prevents attempts at loading functions from shared object files other than those containing legitimate functions. See [Loadable Function Security Precautions.](https://dev.mysql.com/doc/extending-mysql/5.7/en/adding-loadable-function.md#loadable-function-security)

<span id="page-108-1"></span>• [--ansi](#page-108-1)

| Command-Line Format | ansi |
|---------------------|------|
|                     |      |

Use standard (ANSI) SQL syntax instead of MySQL syntax. For more precise control over the server SQL mode, use the [--sql-mode](#page-128-0) option instead. See Section 1.6, "MySQL Standards Compliance", and Section 5.1.10, "Server SQL Modes".

• [--basedir=](#page-137-1)dir\_name, -b [dir\\_name](#page-137-1)

| Command-Line Format | basedir=dir_name                |
|---------------------|---------------------------------|
| System Variable     | basedir                         |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | Directory name                  |
| Default Value       | configuration-dependent default |

The path to the MySQL installation directory. This option sets the [basedir](#page-137-1) system variable.

<span id="page-109-0"></span>• [--bootstrap](#page-109-0)

| Command-Line Format | bootstrap |
|---------------------|-----------|
| Deprecated          | Yes       |

This option is used by the mysql\_install\_db program to create the MySQL privilege tables without having to start a full MySQL server.

![](_page_109_Picture_9.jpeg)

# **Note**

mysql\_install\_db is deprecated because its functionality has been integrated into mysqld, the MySQL server. Consequently, the [-](#page-109-0) [bootstrap](#page-109-0) server option that mysql\_install\_db passes to mysqld is also deprecated. To initialize a MySQL installation, invoke mysqld with the [--initialize](#page-116-0) or [--initialize-insecure](#page-116-1) option. For more information, see Section 2.9.1, "Initializing the Data Directory". Expect mysql\_install\_db and the [--bootstrap](#page-109-0) server option to be removed in a future release of MySQL.

[--bootstrap](#page-109-0) is mutually exclusive with [--daemonize](#page-110-3), [--initialize](#page-116-0), and [--initialize](#page-116-1)[insecure](#page-116-1).

Global transaction identifiers (GTIDs) are not disabled when [--bootstrap](#page-109-0) is used. [--bootstrap](#page-109-0) was used (Bug #20980271). See Section 16.1.3, "Replication with Global Transaction Identifiers".

When the server operates in bootstap mode, some functionality is unavailable that limits the statements permitted in any file named by the [init\\_file](#page-164-3) system variable. For more information, see the description of that variable. In addition, the [disabled\\_storage\\_engines](#page-152-1) system variable has no effect.

<span id="page-109-1"></span>• [--character-set-client-handshake](#page-109-1)

| Command-Line Format | character-set-client<br>handshake[={OFF ON}] |
|---------------------|----------------------------------------------|
| Type                | Boolean                                      |

| Default Value | ON |
|---------------|----|
|---------------|----|

Do not ignore character set information sent by the client. To ignore client information and use the default server character set, use [--skip-character-set-client-handshake](#page-109-1); this makes MySQL behave like MySQL 4.0.

<span id="page-110-0"></span>• [--chroot=](#page-110-0)dir\_name, -r dir\_name

| Command-Line Format | chroot=dir_name |
|---------------------|-----------------|
| Type                | Directory name  |

Put the mysqld server in a closed environment during startup by using the chroot() system call. This is a recommended security measure. Use of this option somewhat limits LOAD DATA and SELECT ... INTO OUTFILE.

<span id="page-110-1"></span>• [--console](#page-110-1)

| Command-Line Format | console |
|---------------------|---------|
| Platform Specific   | Windows |

(Windows only.) Write the error log to stderr and stdout (the console). mysqld does not close the console window if this option is used.

[--console](#page-110-1) takes precedence over [--log-error](#page-119-0) if both are given. (In MySQL 5.5 and 5.6, this is reversed: [--log-error](#page-119-0) takes precedence over [--console](#page-110-1) if both are given.)

<span id="page-110-2"></span>• [--core-file](#page-110-2)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

When this option is used, write a core file if mysqld dies; no arguments are needed (or accepted). The name and location of the core file is system dependent. On Linux, a core file named core.pid is written to the current working directory of the process, which for mysqld is the data directory. pid represents the process ID of the server process. On macOS, a core file named core.pid is written to the /cores directory. On Solaris, use the coreadm command to specify where to write the core file and how to name it.

For some systems, to get a core file you must also specify the --core-file-size option to mysqld\_safe. See Section 4.3.2, "mysqld\_safe — MySQL Server Startup Script". On some systems, such as Solaris, you do not get a core file if you are also using the [--user](#page-132-0) option. There might be additional restrictions or limitations. For example, it might be necessary to execute ulimit -c unlimited before starting the server. Consult your system documentation.

<span id="page-110-3"></span>• [--daemonize](#page-110-3)

| Command-Line Format | daemonize[={OFF ON}] |
|---------------------|----------------------|
| Type                | Boolean              |
| Default Value       | OFF                  |

This option causes the server to run as a traditional, forking daemon, permitting it to work with operating systems that use systemd for process control. For more information, see Section 2.5.10, "Managing MySQL Server with systemd".

[--daemonize](#page-110-3) is mutually exclusive with [--bootstrap](#page-109-0), [--initialize](#page-116-0), and [--initialize](#page-116-1)[insecure](#page-116-1).

• [--datadir=](#page-145-2)dir\_name, -h dir\_name

| Command-Line Format | datadir=dir_name |
|---------------------|------------------|
| System Variable     | datadir          |
| Scope               | Global           |
| Dynamic             | No               |
| Type                | Directory name   |

The path to the MySQL server data directory. This option sets the [datadir](#page-145-2) system variable. See the description of that variable.

<span id="page-111-0"></span>• --debug[=[debug\\_options](#page-111-0)], -# [debug\_options]

| Command-Line Format     | debug[=debug_options]     |
|-------------------------|---------------------------|
| System Variable         | debug                     |
| Scope                   | Global, Session           |
| Dynamic                 | Yes                       |
| Type                    | String                    |
| Default Value (Unix)    | d:t:i:o,/tmp/mysqld.trace |
| Default Value (Windows) | d:t:i:O,\mysqld.trace     |

If MySQL is configured with the -DWITH\_DEBUG=1 CMake option, you can use this option to get a trace file of what mysqld is doing. A typical debug\_options string is d:t:o,file\_name. The default is d:t:i:o,/tmp/mysqld.trace on Unix and d:t:i:O,\mysqld.trace on Windows.

Using -DWITH\_DEBUG=1 to configure MySQL with debugging support enables you to use the [-](#page-111-0) [debug="d,parser\\_debug"](#page-111-0) option when you start the server. This causes the Bison parser that is used to process SQL statements to dump a parser trace to the server's standard error output. Typically, this output is written to the error log.

This option may be given multiple times. Values that begin with + or - are added to or subtracted from the previous value. For example, [--debug=T](#page-111-0) [--debug=+P](#page-111-0) sets the value to P:T.

For more information, see Section 5.8.3, "The DBUG Package".

<span id="page-111-1"></span>• [--debug-sync-timeout\[=](#page-111-1)N]

| Command-Line Format | debug-sync-timeout[=#] |
|---------------------|------------------------|
| Type                | Integer                |

Controls whether the Debug Sync facility for testing and debugging is enabled. Use of Debug Sync requires that MySQL be configured with the -DWITH\_DEBUG=ON CMake option (see Section 2.8.7, "MySQL Source-Configuration Options"). If Debug Sync is not compiled in, this option is not available. The option value is a timeout in seconds. The default value is 0, which disables Debug Sync. To enable it, specify a value greater than 0; this value also becomes the default timeout for individual synchronization points. If the option is given without a value, the timeout is set to 300 seconds.

For a description of the Debug Sync facility and how to use synchronization points, see [MySQL](https://dev.mysql.com/doc/internals/en/test-synchronization.md) [Internals: Test Synchronization](https://dev.mysql.com/doc/internals/en/test-synchronization.md).

<span id="page-111-2"></span>• [--default-time-zone=](#page-111-2)timezone

| Type | String |
|------|--------|
|------|--------|

Set the default server time zone. This option sets the global time\_zone system variable. If this option is not given, the default time zone is the same as the system time zone (given by the value of the system\_time\_zone system variable.

The system\_time\_zone variable differs from time\_zone. Although they might have the same value, the latter variable is used to initialize the time zone for each client that connects. See Section 5.1.13, "MySQL Server Time Zone Support".

<span id="page-112-0"></span>• [--defaults-extra-file=](#page-112-0)file\_name

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-112-1"></span>• [--defaults-file=](#page-112-1)file\_name

Read only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

![](_page_112_Picture_9.jpeg)

#### **Note**

This must be the first option on the command line if it is used, except that if the server is started with the [--defaults-file](#page-112-1) and [--install](#page-117-0) (or [-](#page-117-1) [install-manual](#page-117-1)) options, [--install](#page-117-0) (or [--install-manual](#page-117-1)) must be first.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-112-2"></span>• [--defaults-group-suffix=](#page-112-2)str

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, mysqld normally reads the [mysqld] group. If this option is given as [--defaults](#page-112-2)[group-suffix=\\_other](#page-112-2), mysqld also reads the [mysqld\_other] group.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-112-3"></span>• [--des-key-file=](#page-112-3)file\_name

| Command-Line Format | des-key-file=file_name |
|---------------------|------------------------|
| Deprecated          | Yes                    |

Read the default DES keys from this file. These keys are used by the DES\_ENCRYPT() and DES\_DECRYPT() functions.

![](_page_112_Picture_19.jpeg)

#### **Note**

The DES\_ENCRYPT() and DES\_DECRYPT() functions are deprecated in MySQL 5.7, are removed in MySQL 8.0, and should no longer be used. Consequently, [--des-key-file](#page-112-3) also is deprecated and is removed in MySQL 8.0.

<span id="page-113-0"></span>• [--disable-partition-engine-check](#page-113-0)

| Command-Line Format | disable-partition-engine<br>check[={OFF ON}] |
|---------------------|----------------------------------------------|
| Deprecated          | Yes                                          |
| Type                | Boolean                                      |
| Default Value       | ON                                           |

Whether to disable the startup check for tables with nonnative partitioning.

As of MySQL 5.7.17, the generic partitioning handler in the MySQL server is deprecated, and is removed in MySQL 8.0, when the storage engine used for a given table is expected to provide its own ("native") partitioning handler. Currently, only the InnoDB and NDB storage engines do this.

Use of tables with nonnative partitioning results in an [ER\\_WARN\\_DEPRECATED\\_SYNTAX](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_warn_deprecated_syntax) warning. In MySQL 5.7.17 through 5.7.20, the server automatically performs a check at startup to identify tables that use nonnative partitioning; for any that are found, the server writes a message to its error log. To disable this check, use the [--disable-partition-engine-check](#page-113-0) option. In MySQL 5.7.21 and later, this check is not performed; in these versions, you must start the server with [--disable](#page-113-0)[partition-engine-check=false](#page-113-0), if you wish for the server to check for tables using the generic partitioning handler (Bug #85830, Bug #25846957).

Use of tables with nonnative partitioning results in an [ER\\_WARN\\_DEPRECATED\\_SYNTAX](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_warn_deprecated_syntax) warning. Also, the server performs a check at startup to identify tables that use nonnative partitioning; for any found, the server writes a message to its error log. To disable this check, use the [--disable](#page-113-0)[partition-engine-check](#page-113-0) option.

To prepare for migration to MySQL 8.0, any table with nonnative partitioning should be changed to use an engine that provides native partitioning, or be made nonpartitioned. For example, to change a table to InnoDB, execute this statement:

ALTER TABLE table\_name ENGINE = INNODB;

<span id="page-113-1"></span>• [--early-plugin-load=](#page-113-1)plugin\_list

| Command-Line Format | early-plugin-load=plugin_list |
|---------------------|-------------------------------|
| Type                | String                        |
| Default Value       | empty string                  |

This option tells the server which plugins to load before loading mandatory built-in plugins and before storage engine initialization. Early loading is supported only for plugins compiled with PLUGIN\_OPT\_ALLOW\_EARLY. If multiple [--early-plugin-load](#page-113-1) options are given, only the last one applies.

The option value is a semicolon-separated list of plugin\_library and name=plugin\_library values. Each plugin\_library is the name of a library file that contains plugin code, and each name is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads only the

named plugin from the libary. The server looks for plugin library files in the directory named by the plugin\_dir system variable.

For example, if plugins named myplug1 and myplug2 are contained in the plugin library files myplug1.so and myplug2.so, use this option to perform an early plugin load:

```
mysqld --early-plugin-load="myplug1=myplug1.so;myplug2=myplug2.so"
```

Quotes surround the argument value because otherwise some command interpreters interpret semicolon (;) as a special character. (For example, Unix shells treat it as a command terminator.)

Each named plugin is loaded early for a single invocation of mysqld only. After a restart, the plugin is not loaded early unless [--early-plugin-load](#page-113-1) is used again.

If the server is started using [--initialize](#page-116-0) or [--initialize-insecure](#page-116-1), plugins specified by [-](#page-113-1) [early-plugin-load](#page-113-1) are not loaded.

If the server is run with [--help](#page-108-2), plugins specified by [--early-plugin-load](#page-113-1) are loaded but not initialized. This behavior ensures that plugin options are displayed in the help message.

InnoDB tablespace encryption relies on the MySQL Keyring for encryption key management, and the keyring plugin to be used must be loaded prior to storage engine initialization to facilitate InnoDB recovery for encrypted tables. For example, administrators who want the keyring\_file plugin loaded at startup should use [--early-plugin-load](#page-113-1) with the appropriate option value (such as keyring\_file.so on Unix and Unix-like systems or keyring\_file.dll on Windows).

![](_page_114_Picture_9.jpeg)

#### **Important**

In MySQL 5.7.11, the default [--early-plugin-load](#page-113-1) value is the name of the keyring\_file plugin library file, causing that plugin to be loaded by default. In MySQL 5.7.12 and higher, the default [--early-plugin-load](#page-113-1) value is empty; to load the keyring\_file plugin, you must explicitly specify the option with a value naming the keyring\_file plugin library file.

This change of default [--early-plugin-load](#page-113-1) value introduces an incompatibility for InnoDB tablespace encryption for upgrades from 5.7.11 to 5.7.12 or higher. Administrators who have encrypted InnoDB tablespaces must take explicit action to ensure continued loading of the keyring plugin: Start the server with an [--early-plugin-load](#page-113-1) option that names the plugin library file. For additional information, see Section 6.4.4.1, "Keyring Plugin Installation".

For information about InnoDB tablespace encryption, see Section 14.14, "InnoDB Data-at-Rest Encryption". For general information about plugin loading, see Section 5.5.1, "Installing and Uninstalling Plugins".

<span id="page-114-0"></span>• [--exit-info\[=](#page-114-0)flags], -T [flags]

| Command-Line Format | exit-info[=flags] |
|---------------------|-------------------|
| Type                | Integer           |

This is a bitmask of different flags that you can use for debugging the mysqld server. Do not use this option unless you know exactly what it does!

<span id="page-114-1"></span>• [--external-locking](#page-114-1)

| Command-Line Format | external-locking[={OFF ON}] |
|---------------------|-----------------------------|
| Type                | Boolean                     |

| Default Value | OFF |  |
|---------------|-----|--|
|---------------|-----|--|

Enable external locking (system locking), which is disabled by default. If you use this option on a system on which lockd does not fully work (such as Linux), it is easy for mysqld to deadlock.

To disable external locking explicitly, use --skip-external-locking.

External locking affects only MyISAM table access. For more information, including conditions under which it can and cannot be used, see Section 8.11.5, "External Locking".

#### <span id="page-115-2"></span>• [--flush](#page-115-2)

| Command-Line Format | flush[={OFF ON}] |
|---------------------|------------------|
| System Variable     | flush            |
| Scope               | Global           |
| Dynamic             | Yes              |
| Type                | Boolean          |
| Default Value       | OFF              |

Flush (synchronize) all changes to disk after each SQL statement. Normally, MySQL does a write of all changes to disk only after each SQL statement and lets the operating system handle the synchronizing to disk. See Section B.3.3.3, "What to Do If MySQL Keeps Crashing".

![](_page_115_Picture_8.jpeg)

#### **Note**

If [--flush](#page-115-2) is specified, the value of [flush\\_time](#page-157-2) does not matter and changes to [flush\\_time](#page-157-2) have no effect on flush behavior.

## <span id="page-115-0"></span>• [--gdb](#page-115-0)

| Command-Line Format | gdb[={OFF ON}] |
|---------------------|----------------|
| Type                | Boolean        |
| Default Value       | OFF            |

Install an interrupt handler for SIGINT (needed to stop mysqld with ^C to set breakpoints) and disable stack tracing and core file handling. See Section 5.8.1.4, "Debugging mysqld under gdb".

#### <span id="page-115-1"></span>• [--ignore-db-dir=](#page-115-1)dir\_name

| Command-Line Format | ignore-db-dir=dir_name |
|---------------------|------------------------|
| Deprecated          | Yes                    |
| Type                | Directory name         |

This option tells the server to ignore the given directory name for purposes of the SHOW DATABASES statement or INFORMATION\_SCHEMA tables. For example, if a MySQL configuration locates the data directory at the root of a file system on Unix, the system might create a lost+found directory there

that the server should ignore. Starting the server with [--ignore-db-dir=lost+found](#page-115-1) causes that name not to be listed as a database.

To specify more than one name, use this option multiple times, once for each name. Specifying the option with an empty value (that is, as [--ignore-db-dir=](#page-115-1)) resets the directory list to the empty list.

Instances of this option given at server startup are used to set the [ignore\\_db\\_dirs](#page-164-1) system variable.

This option is deprecated in MySQL 5.7. With the introduction of the data dictionary in MySQL 8.0, it became superfluous and was removed in that version.

#### <span id="page-116-0"></span>• [--initialize](#page-116-0)

| Command-Line Format | initialize[={OFF ON}] |
|---------------------|-----------------------|
| Type                | Boolean               |
| Default Value       | OFF                   |

This option is used to initialize a MySQL installation by creating the data directory and populating the tables in the mysql system database. For more information, see Section 2.9.1, "Initializing the Data Directory".

This option limits the effects of, or is not compatible with, a number of other startup options for the MySQL server. Some of the most common issues of this sort are noted here:

- We strongly recommend, when initializing the data directory with --initialize, that you specify no additional options other than [--datadir](#page-145-2), other options used for setting directory locations such as [--basedir](#page-137-1), and possibly [--user](#page-132-0), if required. Options for the running MySQL server can be specified when starting it once initialization has been completed and mysqld has shut down. This also applies when using [--initialize-insecure](#page-116-1) instead of --initialize.
- When the server is started with --initialize, some functionality is unavailable that limits the statements permitted in any file named by the [init\\_file](#page-164-3) system variable. For more information, see the description of that variable. In addition, the [disabled\\_storage\\_engines](#page-152-1) system variable has no effect.
- The --ndbcluster option is ignored when used together with --initialize.
- --initialize is mutually exclusive with [--bootstrap](#page-109-0) and [--daemonize](#page-110-3).

The items in the preceding list also apply when initializing the server using the [--initialize](#page-116-1)[insecure](#page-116-1) option.

# <span id="page-116-1"></span>• [--initialize-insecure](#page-116-1)

| Command-Line Format | initialize-insecure[={OFF ON}] |
|---------------------|--------------------------------|
| Type                | Boolean                        |
| Default Value       | OFF                            |

This option is used to initialize a MySQL installation by creating the data directory and populating the tables in the mysql system database. This option implies [--initialize](#page-116-0), and the same restrictions and limitations apply; for more information, see the description of that option, and Section 2.9.1, "Initializing the Data Directory".

![](_page_116_Picture_17.jpeg)

#### **Warning**

This option creates a MySQL root user with an empty password, which is insecure. For this reason, do not use it in production without setting this password manually. See Post-Initialization root Password Assignment, for information about how to do this.

• --innodb-xxx

Set an option for the InnoDB storage engine. The InnoDB options are listed in Section 14.15, "InnoDB Startup Options and System Variables".

<span id="page-117-0"></span>• --install [[service\\_name](#page-117-0)]

| Command-Line Format | install [service_name] |
|---------------------|------------------------|
| Platform Specific   | Windows                |

(Windows only) Install the server as a Windows service that starts automatically during Windows startup. The default service name is MySQL if no service\_name value is given. For more information, see Section 2.3.4.8, "Starting MySQL as a Windows Service".

![](_page_117_Picture_7.jpeg)

#### **Note**

If the server is started with the [--defaults-file](#page-112-1) and [--install](#page-117-0) options, [--install](#page-117-0) must be first.

<span id="page-117-1"></span>• [--install-manual \[](#page-117-1)service\_name]

| Command-Line Format | install-manual [service_name] |
|---------------------|-------------------------------|
| Platform Specific   | Windows                       |

(Windows only) Install the server as a Windows service that must be started manually. It does not start automatically during Windows startup. The default service name is MySQL if no service\_name value is given. For more information, see Section 2.3.4.8, "Starting MySQL as a Windows Service".

![](_page_117_Picture_13.jpeg)

#### **Note**

If the server is started with the --defaults-file and [--install-manual](#page-117-1) options, [--install-manual](#page-117-1) must be first.

<span id="page-117-2"></span>• [--language=](#page-117-2)lang\_name, -L lang\_name

| Command-Line Format | language=name                             |
|---------------------|-------------------------------------------|
| Deprecated          | Yes; use lc-messages-dir instead          |
| System Variable     | language                                  |
| Scope               | Global                                    |
| Dynamic             | No                                        |
| Type                | Directory name                            |
| Default Value       | /usr/local/mysql/share/mysql/<br>english/ |

The language to use for error messages. lang\_name can be given as the language name or as the full path name to the directory where the language files are installed. See Section 10.12, "Setting the Error Message Language".

[--lc-messages-dir](#page-118-2) and [--lc-messages](#page-118-1) should be used rather than [--language](#page-117-2), which is deprecated (and handled as a synonym for [--lc-messages-dir](#page-118-2)). You should expect the [-](#page-117-2) [language](#page-117-2) option to be removed in a future release of MySQL.

## <span id="page-118-0"></span>• [--large-pages](#page-118-0)

| Command-Line Format | large-pages[={OFF ON}] |
|---------------------|------------------------|
| System Variable     | large_pages            |
| Scope               | Global                 |
| Dynamic             | No                     |
| Platform Specific   | Linux                  |
| Type                | Boolean                |
| Default Value       | OFF                    |

Some hardware/operating system architectures support memory pages greater than the default (usually 4KB). The actual implementation of this support depends on the underlying hardware and operating system. Applications that perform a lot of memory accesses may obtain performance improvements by using large pages due to reduced Translation Lookaside Buffer (TLB) misses.

MySQL supports the Linux implementation of large page support (which is called HugeTLB in Linux). See Section 8.12.4.3, "Enabling Large Page Support". For Solaris support of large pages, see the description of the [--super-large-pages](#page-129-2) option.

- [--large-pages](#page-118-0) is disabled by default.
- <span id="page-118-1"></span>• [--lc-messages=](#page-118-1)locale\_name

| Command-Line Format | lc-messages=name |
|---------------------|------------------|
| System Variable     | lc_messages      |
| Scope               | Global, Session  |
| Dynamic             | Yes              |
| Type                | String           |
| Default Value       | en_US            |

The locale to use for error messages. The default is en\_US. The server converts the argument to a language name and combines it with the value of [--lc-messages-dir](#page-118-2) to produce the location for the error message file. See Section 10.12, "Setting the Error Message Language".

<span id="page-118-2"></span>• [--lc-messages-dir=](#page-118-2)dir\_name

| Command-Line Format | lc-messages-dir=dir_name |
|---------------------|--------------------------|
| System Variable     | lc_messages_dir          |
| Scope               | Global                   |
| Dynamic             | No                       |
| Type                | Directory name           |

The directory where error messages are located. The server uses the value together with the value of [--lc-messages](#page-118-1) to produce the location for the error message file. See Section 10.12, "Setting the Error Message Language".

<span id="page-118-3"></span>• [--local-service](#page-118-3)

| Command-Line Format | local-service |
|---------------------|---------------|
|---------------------|---------------|

defaults-file and --local-service are given following the service name, they can be in any order. See Section 2.3.4.8, "Starting MySQL as a Windows Service".

<span id="page-119-0"></span>• [--log-error\[=](#page-119-0)file\_name]

| Command-Line Format | log-error[=file_name] |
|---------------------|-----------------------|
| System Variable     | log_error             |
| Scope               | Global                |
| Dynamic             | No                    |
| Type                | File name             |

Write the error log and startup messages to this file. See Section 5.4.2, "The Error Log".

If the option names no file, the error log file name on Unix and Unix-like systems is host\_name.err in the data directory. The file name on Windows is the same, unless the --pid-file option is specified. In that case, the file name is the PID file base name with a suffix of .err in the data directory.

If the option names a file, the error log file has that name (with an .err suffix added if the name has no suffix), located under the data directory unless an absolute path name is given to specify a different location.

On Windows, [--console](#page-110-1) takes precedence over [--log-error](#page-119-0) if both are given. In this case, the server writes the error log to the console rather than to a file. (In MySQL 5.5 and 5.6, this is reversed: [--log-error](#page-119-0) takes precedence over [--console](#page-110-1) if both are given.)

<span id="page-119-1"></span>• [--log-isam\[=](#page-119-1)file\_name]

| Command-Line Format | log-isam[=file_name] |
|---------------------|----------------------|
| Type                | File name            |

Log all MyISAM changes to this file (used only when debugging MyISAM).

<span id="page-119-2"></span>• [--log-raw](#page-119-2)

| Command-Line Format | log-raw[={OFF ON}] |  |
|---------------------|--------------------|--|
| Type                | Boolean            |  |
| Default Value       | OFF                |  |

Passwords in certain statements written to the general query log, slow query log, and binary log are rewritten by the server not to occur literally in plain text. Password rewriting can be suppressed for the general query log by starting the server with the [--log-raw](#page-119-2) option. This option may be useful for diagnostic purposes, to see the exact text of statements as received by the server, but for security reasons is not recommended for production use.

If a query rewrite plugin is installed, the [--log-raw](#page-119-2) option affects statement logging as follows:

- Without [--log-raw](#page-119-2), the server logs the statement returned by the query rewrite plugin. This may differ from the statement as received.
- With [--log-raw](#page-119-2), the server logs the original statement as received.

For more information, see Section 6.1.2.3, "Passwords and Logging".

• [--log-short-format](#page-119-3)

<span id="page-119-3"></span>

| 109 | DITOLC | TOTMAC |
|-----|--------|--------|
|     |        |        |
|     |        |        |

| Type          | Boolean |
|---------------|---------|
| Default Value | OFF     |

Log less information to the slow query log, if it has been activated.

<span id="page-120-0"></span>• [--log-tc=](#page-120-0)file\_name

| Command-Line Format | log-tc=file_name |
|---------------------|------------------|
| Type                | File name        |
| Default Value       | tc.log           |

The name of the memory-mapped transaction coordinator log file (for XA transactions that affect multiple storage engines when the binary log is disabled). The default name is tc.log. The file is created under the data directory if not given as a full path name. This option is unused.

<span id="page-120-1"></span>• [--log-tc-size=](#page-120-1)size

| Command-Line Format              | log-tc-size=#        |
|----------------------------------|----------------------|
| Type                             | Integer              |
| Default Value                    | 6 * page size        |
| Minimum Value                    | 6 * page size        |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

The size in bytes of the memory-mapped transaction coordinator log. The default and minimum values are 6 times the page size, and the value must be a multiple of the page size. (Before MySQL 5.7.21, the default size is 24KB.)

<span id="page-120-2"></span>• [--log-warnings\[=](#page-120-2)level], -W [level]

| Command-Line Format              | log-warnings[=#]     |
|----------------------------------|----------------------|
| Deprecated                       | Yes                  |
| System Variable                  | log_warnings         |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 2                    |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

![](_page_120_Picture_11.jpeg)

#### **Note**

The [log\\_error\\_verbosity](#page-172-1) system variable is preferred over, and should be used instead of, the [--log-warnings](#page-120-2) option or [log\\_warnings](#page-176-1) system variable. For more information, see the descriptions of [log\\_error\\_verbosity](#page-172-1) and [log\\_warnings](#page-176-1). The [--log-warnings](#page-120-2) command-line option and [log\\_warnings](#page-176-1) system variable are deprecated; expect them to be removed in a future release of MySQL.

the current value by 1. The server logs messages about statements that are unsafe for statementbased logging if the value is greater than 0. Aborted connections and access-denied errors for new connection attempts are logged if the value is greater than 1. See Section B.3.2.9, "Communication Errors and Aborted Connections".

#### <span id="page-121-0"></span>• [--memlock](#page-121-0)

| Command-Line Format | memlock[={OFF ON}] |
|---------------------|--------------------|
| Type                | Boolean            |
| Default Value       | OFF                |

Lock the mysqld process in memory. This option might help if you have a problem where the operating system is causing mysqld to swap to disk.

[--memlock](#page-121-0) works on systems that support the mlockall() system call; this includes Solaris, most Linux distributions that use a 2.4 or higher kernel, and perhaps other Unix systems. On Linux systems, you can tell whether or not mlockall() (and thus this option) is supported by checking to see whether or not it is defined in the system mman.h file, like this:

```
$> grep mlockall /usr/include/sys/mman.h
```

If mlockall() is supported, you should see in the output of the previous command something like the following:

extern int mlockall (int \_\_flags) \_\_THROW;

![](_page_121_Picture_9.jpeg)

#### **Important**

Use of this option may require you to run the server as root, which, for reasons of security, is normally not a good idea. See Section 6.1.5, "How to Run MySQL as a Normal User".

On Linux and perhaps other systems, you can avoid the need to run the server as root by changing the limits.conf file. See the notes regarding the memlock limit in Section 8.12.4.3, "Enabling Large Page Support".

You must not use this option on a system that does not support the mlockall() system call; if you do so, mysqld is very likely to exit as soon as you try to start it.

#### <span id="page-121-1"></span>• [--myisam-block-size=](#page-121-1)N

| Command-Line Format | myisam-block-size=# |
|---------------------|---------------------|
| Type                | Integer             |
| Default Value       | 1024                |
| Minimum Value       | 1024                |
| Maximum Value       | 16384               |

The block size to be used for MyISAM index pages.

## <span id="page-121-2"></span>• [--no-defaults](#page-121-2)

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-121-2) can be used to prevent them from being read. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-694 Line Options that Affect Option-File Handling".

<span id="page-122-0"></span>• [--old-style-user-limits](#page-122-0)

| Command-Line Format | old-style-user-limits[={OFF ON}] |
|---------------------|----------------------------------|
| Type                | Boolean                          |
| Default Value       | OFF                              |

Enable old-style user limits. (Before MySQL 5.0.3, account resource limits were counted separately for each host from which a user connected rather than per account row in the user table.) See Section 6.2.16, "Setting Account Resource Limits".

<span id="page-122-1"></span>• [--partition\[=](#page-122-1)value]

| Command-Line Format | partition[={OFF ON}] |
|---------------------|----------------------|
| Deprecated          | Yes                  |
| Disabled by         | skip-partition       |
| Type                | Boolean              |
| Default Value       | ON                   |

Enables or disables user-defined partitioning support in the MySQL Server.

This option is deprecated in MySQL 5.7.16, and is removed from MySQL 8.0 because in MySQL 8.0, the partitioning engine is replaced by native partitioning, which cannot be disabled.

• --performance-schema-xxx

Configure a Performance Schema option. For details, see Section 25.14, "Performance Schema Command Options".

<span id="page-122-2"></span>• [--plugin-load=](#page-122-2)plugin\_list

| Command-Line Format | plugin-load=plugin_list |
|---------------------|-------------------------|
| Type                | String                  |

This option tells the server to load the named plugins at startup. If multiple [--plugin-load](#page-122-2) options are given, only the last one applies. Additional plugins to load may be specified using [--plugin](#page-123-0)[load-add](#page-123-0) options.

The option value is a semicolon-separated list of plugin\_library and name=plugin\_library values. Each plugin\_library is the name of a library file that contains plugin code, and each name is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads only the named plugin from the libary. The server looks for plugin library files in the directory named by the plugin\_dir system variable.

For example, if plugins named myplug1 and myplug2 are contained in the plugin library files myplug1.so and myplug2.so, use this option to perform an early plugin load:

```
mysqld --plugin-load="myplug1=myplug1.so;myplug2=myplug2.so"
```

Quotes surround the argument value because otherwise some command interpreters interpret semicolon (;) as a special character. (For example, Unix shells treat it as a command terminator.)

Each named plugin is loaded for a single invocation of mysqld only. After a restart, the plugin is not loaded unless [--plugin-load](#page-122-2) is used again. This is in contrast to INSTALL PLUGIN, which adds an entry to the mysql.plugins table to cause the plugin to be loaded for every normal server startup.

During the normal startup sequence, the server determines which plugins to load by reading the mysql.plugins system table. If the server is started with the [--skip-grant-tables](#page-125-1) option, plugins registered in the mysql.plugins table are not loaded and are unavailable. [--plugin](#page-122-2)[load](#page-122-2) enables plugins to be loaded even when [--skip-grant-tables](#page-125-1) is given. [--plugin-load](#page-122-2) also enables plugins to be loaded at startup that cannot be loaded at runtime.

This option does not set a corresponding system variable. The output of SHOW PLUGINS provides information about loaded plugins. More detailed information can be found in the Information Schema PLUGINS table. See Section 5.5.2, "Obtaining Server Plugin Information".

For additional information about plugin loading, see Section 5.5.1, "Installing and Uninstalling Plugins".

<span id="page-123-0"></span>• [--plugin-load-add=](#page-123-0)plugin\_list

| Command-Line Format | plugin-load-add=plugin_list |
|---------------------|-----------------------------|
| Type                | String                      |

This option complements the [--plugin-load](#page-122-2) option. [--plugin-load-add](#page-123-0) adds a plugin or plugins to the set of plugins to be loaded at startup. The argument format is the same as for [-](#page-122-2) [plugin-load](#page-122-2). [--plugin-load-add](#page-123-0) can be used to avoid specifying a large set of plugins as a single long unwieldy [--plugin-load](#page-122-2) argument.

[--plugin-load-add](#page-123-0) can be given in the absence of [--plugin-load](#page-122-2), but any instance of [-](#page-123-0) [plugin-load-add](#page-123-0) that appears before [--plugin-load](#page-122-2) has no effect because [--plugin-load](#page-122-2) resets the set of plugins to load. In other words, these options:

```
--plugin-load=x --plugin-load-add=y
```

are equivalent to this option:

```
--plugin-load="x;y"
```

But these options:

```
--plugin-load-add=y --plugin-load=x
```

are equivalent to this option:

```
--plugin-load=x
```

This option does not set a corresponding system variable. The output of SHOW PLUGINS provides information about loaded plugins. More detailed information can be found in the Information Schema PLUGINS table. See Section 5.5.2, "Obtaining Server Plugin Information".

For additional information about plugin loading, see Section 5.5.1, "Installing and Uninstalling Plugins".

<span id="page-123-1"></span>• [--plugin-](#page-123-1)xxx

Specifies an option that pertains to a server plugin. For example, many storage engines can be built as plugins, and for such engines, options for them can be specified with a --plugin prefix. Thus,

the --innodb-file-per-table option for InnoDB can be specified as --plugin-innodbfile-per-table.

For boolean options that can be enabled or disabled, the --skip prefix and other alternative formats are supported as well (see Section 4.2.2.4, "Program Option Modifiers"). For example, --skipplugin-innodb-file-per-table disables innodb-file-per-table.

The rationale for the --plugin prefix is that it enables plugin options to be specified unambiguously if there is a name conflict with a built-in server option. For example, were a plugin writer to name a plugin "sql" and implement a "mode" option, the option name might be [--sql-mode](#page-128-0), which would conflict with the built-in option of the same name. In such cases, references to the conflicting name are resolved in favor of the built-in option. To avoid the ambiguity, users can specify the plugin option as --plugin-sql-mode. Use of the --plugin prefix for plugin options is recommended to avoid any question of ambiguity.

<span id="page-124-0"></span>• --port=[port\\_num](#page-124-0), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| System Variable     | port          |
| Scope               | Global        |
| Dynamic             | No            |
| Type                | Integer       |
| Default Value       | 3306          |
| Minimum Value       | 0             |
| Maximum Value       | 65535         |

The port number to use when listening for TCP/IP connections. On Unix and Unix-like systems, the port number must be 1024 or higher unless the server is started by the root operating system user. Setting this option to 0 causes the default value to be used.

<span id="page-124-1"></span>• [--port-open-timeout=](#page-124-1)num

| Command-Line Format | port-open-timeout=# |
|---------------------|---------------------|
| Type                | Integer             |
| Default Value       | 0                   |

On some systems, when the server is stopped, the TCP/IP port might not become available immediately. If the server is restarted quickly afterward, its attempt to reopen the port can fail. This option indicates how many seconds the server should wait for the TCP/IP port to become free if it cannot be opened. The default is not to wait.

<span id="page-124-2"></span>• [--print-defaults](#page-124-2)

Print the program name and all options that it gets from option files. Password values are masked. This must be the first option on the command line if it is used, except that it may be used immediately after [--defaults-file](#page-112-1) or [--defaults-extra-file](#page-112-0).

For additional information about this and other option-file options, see Section 4.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-124-3"></span>• --remove [[service\\_name](#page-124-3)]

| Command-Line Format | remove [service_name] |
|---------------------|-----------------------|
|---------------------|-----------------------|

| Platform Specific | Windows |
|-------------------|---------|
|-------------------|---------|

(Windows only) Remove a MySQL Windows service. The default service name is MySQL if no service\_name value is given. For more information, see Section 2.3.4.8, "Starting MySQL as a Windows Service".

#### <span id="page-125-0"></span>• [--safe-user-create](#page-125-0)

| Command-Line Format | safe-user-create[={OFF ON}] |
|---------------------|-----------------------------|
| Type                | Boolean                     |
| Default Value       | OFF                         |

If this option is enabled, a user cannot create new MySQL users by using the GRANT statement unless the user has the INSERT privilege for the mysql.user system table or any column in the table. If you want a user to have the ability to create new users that have those privileges that the user has the right to grant, you should grant the user the following privilege:

```
GRANT INSERT(user) ON mysql.user TO 'user_name'@'host_name';
```

This ensures that the user cannot change any privilege columns directly, but has to use the GRANT statement to give privileges to other users.

### <span id="page-125-1"></span>• [--skip-grant-tables](#page-125-1)

| Command-Line Format | skip-grant-tables[={OFF ON}] |
|---------------------|------------------------------|
| Type                | Boolean                      |
| Default Value       | OFF                          |

This option affects the server startup sequence:

• [--skip-grant-tables](#page-125-1) causes the server not to read the grant tables in the mysql system database, and thus to start without using the privilege system at all. This gives anyone with access to the server unrestricted access to all databases.

To cause a server started with [--skip-grant-tables](#page-125-1) to load the grant tables at runtime, perform a privilege-flushing operation, which can be done in these ways:

- Issue a MySQL FLUSH PRIVILEGES statement after connecting to the server.
- Execute a mysqladmin flush-privileges or mysqladmin reload command from the command line.

Privilege flushing might also occur implicitly as a result of other actions performed after startup, thus causing the server to start using the grant tables. For example, mysql\_upgrade flushes the privileges during the upgrade procedure.

- [--skip-grant-tables](#page-125-1) causes the server not to load certain other objects registered in the mysql system database:
  - Plugins installed using INSTALL PLUGIN and registered in the mysql.plugin system table.

To cause plugins to be loaded even when using [--skip-grant-tables](#page-125-1), use the [--plugin](#page-122-2)[load](#page-122-2) or [--plugin-load-add](#page-123-0) option.

- Scheduled events installed using CREATE EVENT and registered in the mysql.event system table.
- Loadable functions installed using CREATE FUNCTION and registered in the mysql.func system table.

- [--skip-grant-tables](#page-125-1) causes the [disabled\\_storage\\_engines](#page-152-1) system variable to have no effect.
- <span id="page-126-0"></span>• [--skip-host-cache](#page-126-0)

| Command-Line Format | skip-host-cache |
|---------------------|-----------------|
|---------------------|-----------------|

Disable use of the internal host cache for faster name-to-IP resolution. With the cache disabled, the server performs a DNS lookup every time a client connects.

Use of [--skip-host-cache](#page-126-0) is similar to setting the [host\\_cache\\_size](#page-163-1) system variable to 0, but [host\\_cache\\_size](#page-163-1) is more flexible because it can also be used to resize, enable, or disable the host cache at runtime, not just at server startup.

Starting the server with [--skip-host-cache](#page-126-0) does not prevent runtime changes to the value of [host\\_cache\\_size](#page-163-1), but such changes have no effect and the cache is not re-enabled even if [host\\_cache\\_size](#page-163-1) is set larger than 0.

For more information about how the host cache works, see Section 5.1.11.2, "DNS Lookups and the Host Cache".

• --skip-innodb

Disable the InnoDB storage engine. In this case, because the default storage engine is InnoDB, the server cannot start unless you also use [--default-storage-engine](#page-149-0) and [--default-tmp](#page-149-1)[storage-engine](#page-149-1) to set the default to some other engine for both permanent and TEMPORARY tables.

The InnoDB storage engine cannot be disabled, and the --skip-innodb option is deprecated and has no effect. Its use results in a warning. Expect this option to be removed in a future release of MySQL.

<span id="page-126-1"></span>• [--skip-new](#page-126-1)

| Command-Line Format | skip-new |
|---------------------|----------|
|---------------------|----------|

This option disables (what used to be considered) new, possibly unsafe behaviors. It results in these settings: [delay\\_key\\_write=OFF](#page-150-1), [concurrent\\_insert=NEVER](#page-144-0), [automatic\\_sp\\_privileges=OFF](#page-136-1). It also causes OPTIMIZE TABLE to be mapped to ALTER TABLE for storage engines for which OPTIMIZE TABLE is not supported.

<span id="page-126-2"></span>• [--skip-partition](#page-126-2)

| Command-Line Format | skip-partition    |
|---------------------|-------------------|
|                     | disable-partition |
| Deprecated          | Yes               |

Disables user-defined partitioning. Partitioned tables can be seen using SHOW TABLES or by querying the Information Schema TABLES table, but cannot be created or modified, nor can data in such tables be accessed. All partition-specific columns in the Information Schema PARTITIONS table display NULL.

Since DROP TABLE removes table definition (.frm) files, this statement works on partitioned tables even when partitioning is disabled using the option. The statement, however, does not remove partition definitions associated with partitioned tables in such cases. For this reason, you should

avoid dropping partitioned tables with partitioning disabled, or take action to remove orphaned .par files manually (if present).

![](_page_127_Picture_2.jpeg)

#### **Note**

In MySQL 5.7, partition definition (.par) files are no longer created for partitioned InnoDB tables. Instead, partition definitions are stored in the InnoDB internal data dictionary. Partition definition (.par) files continue to be used for partitioned MyISAM tables.

This option is deprecated in MySQL 5.7.16, and is removed from MySQL 8.0 because in MySQL 8.0, the partitioning engine is replaced by native partitioning, which cannot be disabled.

<span id="page-127-0"></span>• [--skip-show-database](#page-127-0)

| Command-Line Format | skip-show-database |
|---------------------|--------------------|
| System Variable     | skip_show_database |
| Scope               | Global             |
| Dynamic             | No                 |
| Type                | Boolean            |
| Default Value       | OFF                |

This option sets the skip\_show\_database system variable that controls who is permitted to use the SHOW DATABASES statement. See [Section 5.1.7, "Server System Variables"](#page-133-0).

<span id="page-127-1"></span>• [--skip-stack-trace](#page-127-1)

| Command-Line Format | skip-stack-trace |
|---------------------|------------------|
|---------------------|------------------|

Do not write stack traces. This option is useful when you are running mysqld under a debugger. On some systems, you also must use this option to get a core file. See Section 5.8, "Debugging MySQL".

<span id="page-127-2"></span>• [--slow-start-timeout=](#page-127-2)timeout

| Command-Line Format | slow-start-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 15000                |

This option controls the Windows service control manager's service start timeout. The value is the maximum number of milliseconds that the service control manager waits before trying to kill the windows service during startup. The default value is 15000 (15 seconds). If the MySQL service takes too long to start, you may need to increase this value. A value of 0 means there is no timeout.

<span id="page-127-3"></span>• [--socket=](#page-127-3)path

| Command-Line Format     | socket={file_name pipe_name} |
|-------------------------|------------------------------|
| System Variable         | socket                       |
| Scope                   | Global                       |
| Dynamic                 | No                           |
| Type                    | String                       |
| Default Value (Windows) | MySQL                        |

| Default Value (Other) | /tmp/mysql.sock |
|-----------------------|-----------------|
|-----------------------|-----------------|

On Unix, this option specifies the Unix socket file to use when listening for local connections. The default value is /tmp/mysql.sock. If this option is given, the server creates the file in the data directory unless an absolute path name is given to specify a different directory. On Windows, the option specifies the pipe name to use when listening for local connections that use a named pipe. The default value is MySQL (not case-sensitive).

<span id="page-128-0"></span>• [--sql-mode=](#page-128-0)value[,value[,value...]]

| Command-Line Format | sql-mode=name                                                                                                                                            |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| System Variable     | sql_mode                                                                                                                                                 |
| Scope               | Global, Session                                                                                                                                          |
| Dynamic             | Yes                                                                                                                                                      |
| Type                | Set                                                                                                                                                      |
| Default Value       | ONLY_FULL_GROUP_BY<br>STRICT_TRANS_TABLES<br>NO_ZERO_IN_DATE NO_ZERO_DATE<br>ERROR_FOR_DIVISION_BY_ZERO<br>NO_AUTO_CREATE_USER<br>NO_ENGINE_SUBSTITUTION |
| Valid Values        | ALLOW_INVALID_DATES                                                                                                                                      |
|                     | ANSI_QUOTES                                                                                                                                              |
|                     | ERROR_FOR_DIVISION_BY_ZERO                                                                                                                               |
|                     | HIGH_NOT_PRECEDENCE                                                                                                                                      |
|                     | IGNORE_SPACE                                                                                                                                             |
|                     | NO_AUTO_CREATE_USER                                                                                                                                      |
|                     | NO_AUTO_VALUE_ON_ZERO                                                                                                                                    |
|                     | NO_BACKSLASH_ESCAPES                                                                                                                                     |
|                     | NO_DIR_IN_CREATE                                                                                                                                         |
|                     | NO_ENGINE_SUBSTITUTION                                                                                                                                   |
|                     | NO_FIELD_OPTIONS                                                                                                                                         |
|                     | NO_KEY_OPTIONS                                                                                                                                           |
|                     | NO_TABLE_OPTIONS                                                                                                                                         |
|                     | NO_UNSIGNED_SUBTRACTION                                                                                                                                  |
|                     | NO_ZERO_DATE                                                                                                                                             |
|                     | NO_ZERO_IN_DATE                                                                                                                                          |
|                     | ONLY_FULL_GROUP_BY                                                                                                                                       |
|                     | PAD_CHAR_TO_FULL_LENGTH                                                                                                                                  |
|                     | PIPES_AS_CONCAT                                                                                                                                          |

```
REAL_AS_FLOAT
STRICT_ALL_TABLES
STRICT_TRANS_TABLES
```

Set the SQL mode. See Section 5.1.10, "Server SQL Modes".

![](_page_129_Picture_3.jpeg)

#### **Note**

MySQL installation programs may configure the SQL mode during the installation process. If the SQL mode differs from the default or from what you expect, check for a setting in an option file that the server reads at startup.

<span id="page-129-0"></span>• [--ssl](#page-129-0), [--skip-ssl](#page-129-0)

| Command-Line Format | ssl[={OFF ON}] |
|---------------------|----------------|
| Disabled by         | skip-ssl       |
| Type                | Boolean        |
| Default Value       | ON             |

The [--ssl](#page-129-0) option specifies that the server permits but does not require encrypted connections. This option is enabled by default.

[--ssl](#page-129-0) can be specified in negated form as [--skip-ssl](#page-129-0) or a synonym ([--ssl=OFF](#page-129-0), [--disable](#page-129-0)[ssl](#page-129-0)). In this case, the option specifies that the server does not permit encrypted connections, regardless of the settings of the tls\_xxx and ssl\_xxx system variables.

For more information about configuring whether the server permits clients to connect using SSL and indicating where to find SSL keys and certificates, see Section 6.3.1, "Configuring MySQL to Use Encrypted Connections", which also describes server capabilities for certificate and key file autogeneration and autodiscovery. Consider setting at least the ssl\_cert and ssl\_key system variables on the server side and the --ssl-ca (or --ssl-capath) option on the client side.

<span id="page-129-1"></span>• [--standalone](#page-129-1)

| Command-Line Format | standalone |
|---------------------|------------|
| Platform Specific   | Windows    |

Available on Windows only; instructs the MySQL server not to run as a service.

<span id="page-129-2"></span>• [--super-large-pages](#page-129-2)

| Command-Line Format | super-large-pages[={OFF ON}] |
|---------------------|------------------------------|
| Platform Specific   | Solaris                      |
| Type                | Boolean                      |
| Default Value       | OFF                          |

Standard use of large pages in MySQL attempts to use the largest size supported, up to 4MB. Under Solaris, a "super large pages" feature enables uses of pages up to 256MB. This feature is available for recent SPARC platforms. It can be enabled or disabled by using the [--super-large-pages](#page-129-2) or [--skip-super-large-pages](#page-129-2) option.

<span id="page-129-3"></span>• [--symbolic-links](#page-129-3), [--skip-symbolic-links](#page-129-3)

| Type          | Boolean |
|---------------|---------|
| Default Value | ON      |

Enable or disable symbolic link support. On Unix, enabling symbolic links means that you can link a MyISAM index file or data file to another directory with the INDEX DIRECTORY or DATA DIRECTORY option of the CREATE TABLE statement. If you delete or rename the table, the files that its symbolic links point to also are deleted or renamed. See Section 8.12.3.2, "Using Symbolic Links for MyISAM Tables on Unix".

This option has no meaning on Windows.

<span id="page-130-0"></span>• [--sysdate-is-now](#page-130-0)

| Command-Line Format | sysdate-is-now[={OFF ON}] |
|---------------------|---------------------------|
| Type                | Boolean                   |
| Default Value       | OFF                       |

SYSDATE() by default returns the time at which it executes, not the time at which the statement in which it occurs begins executing. This differs from the behavior of NOW(). This option causes SYSDATE() to be a synonym for NOW(). For information about the implications for binary logging and replication, see the description for SYSDATE() in Section 12.7, "Date and Time Functions" and for SET TIMESTAMP in [Section 5.1.7, "Server System Variables"](#page-133-0).

<span id="page-130-1"></span>• [--tc-heuristic-recover={COMMIT|ROLLBACK}](#page-130-1)

| Command-Line Format | tc-heuristic-recover=name |
|---------------------|---------------------------|
| Type                | Enumeration               |
| Default Value       | OFF                       |
| Valid Values        | OFF                       |
|                     | COMMIT                    |
|                     | ROLLBACK                  |

The decision to use in a manual heuristic recovery.

If a --tc-heuristic-recover option is specified, the server exits regardless of whether manual heuristic recovery is successful.

On systems with more than one storage engine capable of two-phase commit, the ROLLBACK option is not safe and causes recovery to halt with the following error:

```
[ERROR] --tc-heuristic-recover rollback
strategy is not safe on systems with more than one 2-phase-commit-capable
storage engine. Aborting crash recovery.
```

<span id="page-130-2"></span>• [--temp-pool](#page-130-2)

| Command-Line Format   | temp-pool[={OFF ON}] |
|-----------------------|----------------------|
| Deprecated            | Yes                  |
| Type                  | Boolean              |
| Default Value (Linux) | ON                   |
| Default Value (Other) | OFF                  |

This option is ignored except on Linux. On Linux, it causes most temporary files created by the server to use a small set of names, rather than a unique name for each new file. This works around703 a problem in the Linux kernel dealing with creating many new files with different names. With the old behavior, Linux seems to "leak" memory, because it is being allocated to the directory entry cache rather than to the disk cache.

As of MySQL 5.7.18, this option is deprecated and is removed in MySQL 8.0.

<span id="page-131-1"></span>• [--transaction-isolation=](#page-131-1)level

| Command-Line Format | transaction-isolation=name |
|---------------------|----------------------------|
| System Variable     | transaction_isolation      |
| Scope               | Global, Session            |
| Dynamic             | Yes                        |
| Type                | Enumeration                |
| Default Value       | REPEATABLE-READ            |
| Valid Values        | READ-UNCOMMITTED           |
|                     | READ-COMMITTED             |
|                     | REPEATABLE-READ            |
|                     | SERIALIZABLE               |

Sets the default transaction isolation level. The level value can be READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ, or SERIALIZABLE. See Section 13.3.6, "SET TRANSACTION Statement".

The default transaction isolation level can also be set at runtime using the SET TRANSACTION statement or by setting the tx\_isolation (or, as of MySQL 5.7.20, transaction\_isolation) system variable.

<span id="page-131-2"></span>• [--transaction-read-only](#page-131-2)

| Command-Line Format | transaction-read-only[={OFF ON}] |
|---------------------|----------------------------------|
| System Variable     | transaction_read_only            |
| Scope               | Global, Session                  |
| Dynamic             | Yes                              |
| Type                | Boolean                          |
| Default Value       | OFF                              |

Sets the default transaction access mode. By default, read-only mode is disabled, so the mode is read/write.

To set the default transaction access mode at runtime, use the SET TRANSACTION statement or set the tx\_read\_only (or, as of MySQL 5.7.20, transaction\_read\_only) system variable. See Section 13.3.6, "SET TRANSACTION Statement".

<span id="page-131-0"></span>• [--tmpdir=](#page-131-0)dir\_name, -t dir\_name

| Command-Line Format | tmpdir=dir_name |
|---------------------|-----------------|
| System Variable     | tmpdir          |
| Scope               | Global          |
| Dynamic             | No              |

| Type<br>Directory name |
|------------------------|
|------------------------|

The path of the directory to use for creating temporary files. It might be useful if your default /tmp directory resides on a partition that is too small to hold temporary tables. This option accepts several paths that are used in round-robin fashion. Paths should be separated by colon characters (:) on Unix and semicolon characters (;) on Windows.

[--tmpdir](#page-131-0) can be a non-permanent location, such as a directory on a memory-based file system or a directory that is cleared when the server host restarts. If the MySQL server is acting as a replica, and you are using a non-permanent location for [--tmpdir](#page-131-0), consider setting a different temporary directory for the replica using the slave\_load\_tmpdir system variable. For a replication replica, the temporary files used to replicate LOAD DATA statements are stored in this directory, so with a permanent location they can survive machine restarts, although replication can now continue after a restart if the temporary files have been removed.

For more information about the storage location of temporary files, see Section B.3.3.5, "Where MySQL Stores Temporary Files".

<span id="page-132-0"></span>• --user={[user\\_name](#page-132-0)|user\_id}, -u {user\_name|user\_id}

| Command-Line Format | user=name |
|---------------------|-----------|
| Type                | String    |

Run the mysqld server as the user having the name user\_name or the numeric user ID user\_id. ("User" in this context refers to a system login account, not a MySQL user listed in the grant tables.)

This option is mandatory when starting mysqld as root. The server changes its user ID during its startup sequence, causing it to run as that particular user rather than as root. See Section 6.1.1, "Security Guidelines".

To avoid a possible security hole where a user adds a [--user=root](#page-132-0) option to a my.cnf file (thus causing the server to run as root), mysqld uses only the first [--user](#page-132-0) option specified and produces a warning if there are multiple [--user](#page-132-0) options. Options in /etc/my.cnf and \$MYSQL\_HOME/my.cnf are processed before command-line options, so it is recommended that you put a [--user](#page-132-0) option in /etc/my.cnf and specify a value other than root. The option in /etc/ my.cnf is found before any other [--user](#page-132-0) options, which ensures that the server runs as a user other than root, and that a warning results if any other [--user](#page-132-0) option is found.

<span id="page-132-1"></span>• [--validate-user-plugins\[={OFF|ON}\]](#page-132-1)

| Command-Line Format | validate-user-plugins[={OFF ON}] |
|---------------------|----------------------------------|
| Type                | Boolean                          |
| Default Value       | ON                               |

If this option is enabled (the default), the server checks each user account and produces a warning if conditions are found that would make the account unusable:

- The account requires an authentication plugin that is not loaded.
- The account requires the sha256\_password authentication plugin but the server was started with neither SSL nor RSA enabled as required by this plugin.

Enabling [--validate-user-plugins](#page-132-1) slows down server initialization and FLUSH PRIVILEGES. If you do not require the additional checking, you can disable this option at startup to avoid the performance decrement.

<span id="page-132-2"></span>• [--verbose](#page-132-2), [-v](#page-132-2)

Use this option with the [--help](#page-108-2) option for detailed help.

• [--version](#page-133-1), -V

Display version information and exit.

# <span id="page-133-1"></span><span id="page-133-0"></span>**5.1.7 Server System Variables**

The MySQL server maintains many system variables that affect its operation. Most system variables can be set at server startup using options on the command line or in an option file. Most of them can be changed dynamically at runtime using the SET statement, which enables you to modify operation of the server without having to stop and restart it. Some variables are read-only, and their values are determined by the system environment, by how MySQL is installed on the system, or possibly by the options used to compile MySQL. Most system variables have a default value, but there are exceptions, including read-only variables. You can also use system variable values in expressions.

At runtime, setting a global system variable value requires the SUPER privilege. Setting a session system variable value normally requires no special privileges and can be done by any user, although there are exceptions. For more information, see Section 5.1.8.1, "System Variable Privileges"

There are several ways to see the names and values of system variables:

• To see the values that a server uses based on its compiled-in defaults and any option files that it reads, use this command:

```
mysqld --verbose --help
```

• To see the values that a server uses based on only its compiled-in defaults, ignoring the settings in any option files, use this command:

```
mysqld --no-defaults --verbose --help
```

• To see the current values used by a running server, use the SHOW VARIABLES statement or the Performance Schema system variable tables. See Section 25.12.13, "Performance Schema System Variable Tables".

This section provides a description of each system variable. For a system variable summary table, see [Section 5.1.4, "Server System Variable Reference".](#page-74-0) For more information about manipulation of system variables, see Section 5.1.8, "Using System Variables".

For additional system variable information, see these sections:

- Section 5.1.8, "Using System Variables", discusses the syntax for setting and displaying system variable values.
- Section 5.1.8.2, "Dynamic System Variables", lists the variables that can be set at runtime.
- Information on tuning system variables can be found in [Section 5.1.1, "Configuring the Server".](#page-33-1)
- Section 14.15, "InnoDB Startup Options and System Variables", lists InnoDB system variables.
- NDB Cluster System Variables, lists system variables which are specific to NDB Cluster.
- For information on server system variables specific to replication, see Section 16.1.6, "Replication and Binary Logging Options and Variables".

![](_page_133_Picture_20.jpeg)

## **Note**

Some of the following variable descriptions refer to "enabling" or "disabling" a variable. These variables can be enabled with the SET statement by setting them to ON or 1, or disabled by setting them to OFF or 0. Boolean variables can be set at startup to the values ON, TRUE, OFF, and FALSE (not case-sensitive), as well as 1 and 0. See Section 4.2.2.4, "Program Option Modifiers".

Some system variables control the size of buffers or caches. For a given buffer, the server might need to allocate internal data structures. These structures typically are allocated from the total memory allocated to the buffer, and the amount of space required might be platform dependent. This means that when you assign a value to a system variable that controls a buffer size, the amount of space actually available might differ from the value assigned. In some cases, the amount might be less than the value assigned. It is also possible for the server to adjust a value upward. For example, if you assign a value of 0 to a variable for which the minimal value is 1024, the server sets the value to 1024.

<span id="page-134-1"></span>Values for buffer sizes, lengths, and stack sizes are given in bytes unless otherwise specified.

![](_page_134_Picture_3.jpeg)

#### **Note**

Some system variable descriptions include a block size, in which case a value that is not an integer multiple of the stated block size is rounded down to the next lower multiple of the block size before being stored by the server, that is to FLOOR(value) \* block\_size.

Example: Suppose that the block size for a given variable is given as 4096, and you set the value of the variable to 100000 (we assume that the variable's maximum value is greater than this number). Since 100000 / 4096 = 24.4140625, the server automatically lowers the value to 98304 (24 \* 4096) before storing it.

In some cases, the stated maximum for a variable is the maximum allowed by the MySQL parser, but is not an exact multiple of the block size. In such cases, the effective maximum is the next lower multiple of the block size.

Example: A system variable's maxmum value is shown as 4294967295 (232-1), and its block size is 1024. 4294967295 / 1024 = 4194303.9990234375, so if you set this variable to its stated maximum, the value actually stored is 4194303 \* 1024 = 4294966272.

Some system variables take file name values. Unless otherwise specified, the default file location is the data directory if the value is a relative path name. To specify the location explicitly, use an absolute path name. Suppose that the data directory is /var/mysql/data. If a file-valued variable is given as a relative path name, it is located under /var/mysql/data. If the value is an absolute path name, its location is as given by the path name.

<span id="page-134-0"></span>• [authentication\\_windows\\_log\\_level](#page-134-0)

| Command-Line Format | authentication-windows-log-level=# |
|---------------------|------------------------------------|
| System Variable     | authentication_windows_log_level   |
| Scope               | Global                             |
| Dynamic             | No                                 |
| Type                | Integer                            |
| Default Value       | 2                                  |
| Minimum Value       | 0                                  |
| Maximum Value       | 4                                  |

This variable is available only if the authentication\_windows Windows authentication plugin is enabled and debugging code is enabled. See Section 6.4.1.8, "Windows Pluggable Authentication".

This variable sets the logging level for the Windows authentication plugin. The following table shows the permitted values.

| Value | Description |
|-------|-------------|
| 0     | No logging  |

| Value | Description                                |
|-------|--------------------------------------------|
| 1     | Log only error messages                    |
| 2     | Log level 1 messages and warning messages  |
| 3     | Log level 2 messages and information notes |
| 4     | Log level 3 messages and debug messages    |

# <span id="page-135-0"></span>• [authentication\\_windows\\_use\\_principal\\_name](#page-135-0)

| Command-Line Format | authentication-windows-use<br>principal-name[={OFF ON}] |  |
|---------------------|---------------------------------------------------------|--|
| System Variable     | authentication_windows_use_principal_name               |  |
| Scope               | Global                                                  |  |
| Dynamic             | No                                                      |  |
| Type                | Boolean                                                 |  |
| Default Value       | ON                                                      |  |

This variable is available only if the authentication\_windows Windows authentication plugin is enabled. See Section 6.4.1.8, "Windows Pluggable Authentication".

A client that authenticates using the InitSecurityContext() function should provide a string identifying the service to which it connects (targetName). MySQL uses the principal name (UPN) of the account under which the server is running. The UPN has the form user\_id@computer\_name and need not be registered anywhere to be used. This UPN is sent by the server at the beginning of authentication handshake.

This variable controls whether the server sends the UPN in the initial challenge. By default, the variable is enabled. For security reasons, it can be disabled to avoid sending the server's account name to a client as cleartext. If the variable is disabled, the server always sends a 0x00 byte in the first challenge, the client does not specify targetName, and as a result, NTLM authentication is used.

If the server fails to obtain its UPN (which happens primarily in environments that do not support Kerberos authentication), the UPN is not sent by the server and NTLM authentication is used.

#### <span id="page-135-1"></span>• [autocommit](#page-135-1)

| Command-Line Format | autocommit[={OFF ON}] |
|---------------------|-----------------------|
| System Variable     | autocommit            |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | Boolean               |
| Default Value       | ON                    |

The autocommit mode. If set to 1, all changes to a table take effect immediately. If set to 0, you must use COMMIT to accept a transaction or ROLLBACK to cancel it. If [autocommit](#page-135-1) is 0 and you change it to 1, MySQL performs an automatic COMMIT of any open transaction. Another way to begin a transaction is to use a START TRANSACTION or BEGIN statement. See Section 13.3.1, "START TRANSACTION, COMMIT, and ROLLBACK Statements".

By default, client connections begin with [autocommit](#page-135-1) set to 1. To cause clients to begin with a default of 0, set the global [autocommit](#page-135-1) value by starting the server with the [--autocommit=0](#page-135-1) option. To set the variable using an option file, include these lines:

[mysqld]

autocommit=0

## <span id="page-136-1"></span>• [automatic\\_sp\\_privileges](#page-136-1)

| Command-Line Format | automatic-sp-privileges[={OFF ON}] |
|---------------------|------------------------------------|
| System Variable     | automatic_sp_privileges            |
| Scope               | Global                             |
| Dynamic             | Yes                                |
| Type                | Boolean                            |
| Default Value       | ON                                 |

When this variable has a value of 1 (the default), the server automatically grants the EXECUTE and ALTER ROUTINE privileges to the creator of a stored routine, if the user cannot already execute and alter or drop the routine. (The ALTER ROUTINE privilege is required to drop the routine.) The server also automatically drops those privileges from the creator when the routine is dropped. If [automatic\\_sp\\_privileges](#page-136-1) is 0, the server does not automatically add or drop these privileges.

The creator of a routine is the account used to execute the CREATE statement for it. This might not be the same as the account named as the DEFINER in the routine definition.

If you start mysqld with [--skip-new](#page-126-1), [automatic\\_sp\\_privileges](#page-136-1) is set to OFF.

See also Section 23.2.2, "Stored Routines and MySQL Privileges".

#### <span id="page-136-0"></span>• [auto\\_generate\\_certs](#page-136-0)

| Command-Line Format | auto-generate-certs[={OFF ON}] |
|---------------------|--------------------------------|
| System Variable     | auto_generate_certs            |
| Scope               | Global                         |
| Dynamic             | No                             |
| Type                | Boolean                        |
| Default Value       | ON                             |

This variable is available if the server was compiled using OpenSSL (see Section 6.3.4, "SSL Library-Dependent Capabilities"). It controls whether the server autogenerates SSL key and certificate files in the data directory, if they do not already exist.

At startup, the server automatically generates server-side and client-side SSL certificate and key files in the data directory if the [auto\\_generate\\_certs](#page-136-0) system variable is enabled, no SSL options other than [--ssl](#page-129-0) are specified, and the server-side SSL files are missing from the data directory. These files enable secure client connections using SSL; see Section 6.3.1, "Configuring MySQL to Use Encrypted Connections".

For more information about SSL file autogeneration, including file names and characteristics, see Section 6.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"

The sha256\_password\_auto\_generate\_rsa\_keys system variable is related but controls autogeneration of RSA key-pair files needed for secure password exchange using RSA over unencypted connections.

#### <span id="page-136-2"></span>• [avoid\\_temporal\\_upgrade](#page-136-2)

| Command-Line Format | avoid-temporal-upgrade[={OFF ON}] |
|---------------------|-----------------------------------|
| Deprecated          | Yes                               |
| System Variable     | avoid_temporal_upgrade            |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | Yes     |
| Type          | Boolean |
| Default Value | OFF     |

This variable controls whether ALTER TABLE implicitly upgrades temporal columns found to be in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision). Upgrading such columns requires a table rebuild, which prevents any use of fast alterations that might otherwise apply to the operation to be performed.

This variable is disabled by default. Enabling it causes ALTER TABLE not to rebuild temporal columns and thereby be able to take advantage of possible fast alterations.

This variable is deprecated; expect it to be removed in a future release of MySQL.

#### <span id="page-137-0"></span>• [back\\_log](#page-137-0)

| Command-Line Format | back-log=#                                                     |
|---------------------|----------------------------------------------------------------|
| System Variable     | back_log                                                       |
| Scope               | Global                                                         |
| Dynamic             | No                                                             |
| Type                | Integer                                                        |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value       | 1                                                              |
| Maximum Value       | 65535                                                          |

The number of outstanding connection requests MySQL can have. This comes into play when the main MySQL thread gets very many connection requests in a very short time. It then takes some time (although very little) for the main thread to check the connection and start a new thread. The [back\\_log](#page-137-0) value indicates how many requests can be stacked during this short time before MySQL momentarily stops answering new requests. You need to increase this only if you expect a large number of connections in a short period of time.

In other words, this value is the size of the listen queue for incoming TCP/IP connections. Your operating system has its own limit on the size of this queue. The manual page for the Unix listen() system call should have more details. Check your OS documentation for the maximum value for this variable. [back\\_log](#page-137-0) cannot be set higher than your operating system limit.

The default value is based on the following formula, capped to a limit of 900:

50 + (max\_connections / 5)

#### <span id="page-137-1"></span>• [basedir](#page-137-1)

| Command-Line Format | basedir=dir_name                |
|---------------------|---------------------------------|
| System Variable     | basedir                         |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | Directory name                  |
| Default Value       | configuration-dependent default |

The path to the MySQL installation base directory.

# <span id="page-138-0"></span>• [big\\_tables](#page-138-0)

| Command-Line Format | big-tables[={OFF ON}] |
|---------------------|-----------------------|
| System Variable     | big_tables            |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | Boolean               |
| Default Value       | OFF                   |

If enabled, the server stores all temporary tables on disk rather than in memory. This prevents most The table tbl\_name is full errors for SELECT operations that require a large temporary table, but also slows down queries for which in-memory tables would suffice.

The default value for new connections is OFF (use in-memory temporary tables). Normally, it should never be necessary to enable this variable because the server is able to handle large result sets automatically by using memory for small temporary tables and switching to disk-based tables as required.

# <span id="page-138-1"></span>• [bind\\_address](#page-138-1)

| Command-Line Format | bind-address=addr |
|---------------------|-------------------|
| System Variable     | bind_address      |
| Scope               | Global            |
| Dynamic             | No                |
| Type                | String            |
| Default Value       | *                 |

The MySQL server listens on a single network socket for TCP/IP connections. This socket is bound to a single address, but it is possible for an address to map onto multiple network interfaces. To specify an address, set [bind\\_address=](#page-138-1)addr at server startup, where addr is an IPv4 or IPv6 address or a host name. If addr is a host name, the server resolves the name to an IP address and binds to that address. If a host name resolves to multiple IP addresses, the server uses the first IPv4 address if there are any, or the first IPv6 address otherwise.

The server treats different types of addresses as follows:

- If the address is \*, the server accepts TCP/IP connections on all server host IPv4 interfaces, and, if the server host supports IPv6, on all IPv6 interfaces. Use this address to permit both IPv4 and IPv6 connections on all server interfaces. This value is the default.
- If the address is 0.0.0.0, the server accepts TCP/IP connections on all server host IPv4 interfaces.
- If the address is ::, the server accepts TCP/IP connections on all server host IPv4 and IPv6 interfaces.
- If the address is an IPv4-mapped address, the server accepts TCP/IP connections for that address, in either IPv4 or IPv6 format. For example, if the server is bound to ::ffff:127.0.0.1, clients can connect using --host=127.0.0.1 or --host=::ffff:127.0.0.1.

• If the address is a "regular" IPv4 or IPv6 address (such as 127.0.0.1 or ::1), the server accepts TCP/IP connections only for that IPv4 or IPv6 address.

If binding to the address fails, the server produces an error and does not start.

If you intend to bind the server to a specific address, be sure that the mysql.user system table contains an account with administrative privileges that you can use to connect to that address. Otherwise, you cannot shut down the server. For example, if you bind the server to \*, you can connect to it using all existing accounts. But if you bind the server to ::1, it accepts connections only on that address. In that case, first make sure that the 'root'@'::1' account is present in the mysql.user table so you can still connect to the server to shut it down.

This variable has no effect for the embedded server (libmysqld) and is not visible within the embedded server.

<span id="page-139-0"></span>• [block\\_encryption\\_mode](#page-139-0)

| Command-Line Format | block-encryption-mode=# |
|---------------------|-------------------------|
| System Variable     | block_encryption_mode   |
| Scope               | Global, Session         |
| Dynamic             | Yes                     |
| Type                | String                  |
| Default Value       | aes-128-ecb             |

This variable controls the block encryption mode for block-based algorithms such as AES. It affects encryption for AES\_ENCRYPT() and AES\_DECRYPT().

[block\\_encryption\\_mode](#page-139-0) takes a value in aes-keylen-mode format, where keylen is the key length in bits and mode is the encryption mode. The value is not case-sensitive. Permitted keylen values are 128, 192, and 256. Permitted encryption modes depend on whether MySQL was compiled using OpenSSL or yaSSL:

- For OpenSSL, permitted mode values are: ECB, CBC, CFB1, CFB8, CFB128, OFB
- For yaSSL, permitted mode values are: ECB, CBC

For example, this statement causes the AES encryption functions to use a key length of 256 bits and the CBC mode:

```
SET block_encryption_mode = 'aes-256-cbc';
```

An error occurs for attempts to set [block\\_encryption\\_mode](#page-139-0) to a value containing an unsupported key length or a mode that the SSL library does not support.

<span id="page-139-1"></span>• [bulk\\_insert\\_buffer\\_size](#page-139-1)

| Command-Line Format              | bulk-insert-buffer-size=# |
|----------------------------------|---------------------------|
| System Variable                  | bulk_insert_buffer_size   |
| Scope                            | Global, Session           |
| Dynamic                          | Yes                       |
| Type                             | Integer                   |
| Default Value                    | 8388608                   |
| Minimum Value                    | 0                         |
| Maximum Value (64-bit platforms) | 18446744073709551615      |

|      | Maximum Value (32-bit platforms) | 4294967295   |
|------|----------------------------------|--------------|
| Unit |                                  | bytes/thread |

MyISAM uses a special tree-like cache to make bulk inserts faster for INSERT ... SELECT, INSERT ... VALUES (...), (...), ..., and LOAD DATA when adding data to nonempty tables. This variable limits the size of the cache tree in bytes per thread. Setting it to 0 disables this optimization. The default value is 8MB.

#### <span id="page-140-0"></span>• [character\\_set\\_client](#page-140-0)

| System Variable | character_set_client |
|-----------------|----------------------|
| Scope           | Global, Session      |
| Dynamic         | Yes                  |
| Type            | String               |
| Default Value   | utf8                 |

The character set for statements that arrive from the client. The session value of this variable is set using the character set requested by the client when the client connects to the server. (Many clients support a --default-character-set option to enable this character set to be specified explicitly. See also Section 10.4, "Connection Character Sets and Collations".) The global value of the variable is used to set the session value in cases when the client-requested value is unknown or not available, or the server is configured to ignore client requests:

- The client requests a character set not known to the server. For example, a Japanese-enabled client requests sjis when connecting to a server not configured with sjis support.
- The client is from a version of MySQL older than MySQL 4.1, and thus does not request a character set.
- mysqld was started with the [--skip-character-set-client-handshake](#page-109-1) option, which causes it to ignore client character set configuration. This reproduces MySQL 4.0 behavior and is useful should you wish to upgrade the server without upgrading all the clients.

Some character sets cannot be used as the client character set. Attempting to use them as the [character\\_set\\_client](#page-140-0) value produces an error. See Impermissible Client Character Sets.

## <span id="page-140-1"></span>• [character\\_set\\_connection](#page-140-1)

| System Variable | character_set_connection |
|-----------------|--------------------------|
| Scope           | Global, Session          |
| Dynamic         | Yes                      |
| Type            | String                   |
| Default Value   | utf8                     |

The character set used for literals specified without a character set introducer and for number-tostring conversion. For information about introducers, see Section 10.3.8, "Character Set Introducers".

#### <span id="page-140-2"></span>• [character\\_set\\_database](#page-140-2)

| System Variable | character_set_database |
|-----------------|------------------------|
| Scope           | Global, Session        |
| Dynamic         | Yes                    |
| Type            | String                 |
| Default Value   | latin1                 |

| Footnote | This option is dynamic, but should be set only by  |
|----------|----------------------------------------------------|
|          | server. You should not set this variable manually. |

The character set used by the default database. The server sets this variable whenever the default database changes. If there is no default database, the variable has the same value as [character\\_set\\_server](#page-141-2).

The global [character\\_set\\_database](#page-140-2) and [collation\\_database](#page-143-0) system variables are deprecated in MySQL 5.7; expect them to be removed in a future version of MySQL.

Assigning a value to the session [character\\_set\\_database](#page-140-2) and [collation\\_database](#page-143-0) system variables is deprecated in MySQL 5.7 and assignments produce a warning. You should expect the session variables to become read only in a future version of MySQL and assignments to produce an error, while remaining possible to access the session variables to determine the database character set and collation for the default database.

<span id="page-141-0"></span>• [character\\_set\\_filesystem](#page-141-0)

| Command-Line Format | character-set-filesystem=name |
|---------------------|-------------------------------|
| System Variable     | character_set_filesystem      |
| Scope               | Global, Session               |
| Dynamic             | Yes                           |
| Type                | String                        |
| Default Value       | binary                        |

The file system character set. This variable is used to interpret string literals that refer to file names, such as in the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD\_FILE() function. Such file names are converted from [character\\_set\\_client](#page-140-0) to [character\\_set\\_filesystem](#page-141-0) before the file opening attempt occurs. The default value is binary, which means that no conversion occurs. For systems on which multibyte file names are permitted, a different value may be more appropriate. For example, if the system represents file names using UTF-8, set [character\\_set\\_filesystem](#page-141-0) to 'utf8mb4'.

<span id="page-141-1"></span>• [character\\_set\\_results](#page-141-1)

| System Variable | character_set_results |
|-----------------|-----------------------|
| Scope           | Global, Session       |
| Dynamic         | Yes                   |
| Type            | String                |
| Default Value   | utf8                  |

The character set used for returning query results to the client. This includes result data such as column values, result metadata such as column names, and error messages.

<span id="page-141-2"></span>• [character\\_set\\_server](#page-141-2)

| Command-Line Format | character-set-server=name |
|---------------------|---------------------------|
| System Variable     | character_set_server      |
| Scope               | Global, Session           |
| Dynamic             | Yes                       |
| Type                | String                    |

| Default Value | latin1 |
|---------------|--------|
|---------------|--------|

The servers default character set. See Section 10.15, "Character Set Configuration". If you set this variable, you should also set [collation\\_server](#page-143-1) to specify the collation for the character set.

<span id="page-142-0"></span>• [character\\_set\\_system](#page-142-0)

| System Variable | character_set_system |
|-----------------|----------------------|
| Scope           | Global               |
| Dynamic         | No                   |
| Type            | String               |
| Default Value   | utf8                 |

The character set used by the server for storing identifiers. The value is always utf8.

<span id="page-142-1"></span>• [character\\_sets\\_dir](#page-142-1)

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| System Variable     | character_sets_dir          |
| Scope               | Global                      |
| Dynamic             | No                          |
| Type                | Directory name              |

The directory where character sets are installed. See Section 10.15, "Character Set Configuration".

<span id="page-142-2"></span>• [check\\_proxy\\_users](#page-142-2)

| Command-Line Format | check-proxy-users[={OFF ON}] |
|---------------------|------------------------------|
| System Variable     | check_proxy_users            |
| Scope               | Global                       |
| Dynamic             | Yes                          |
| Type                | Boolean                      |
| Default Value       | OFF                          |

Some authentication plugins implement proxy user mapping for themselves (for example, the PAM and Windows authentication plugins). Other authentication plugins do not support proxy users by default. Of these, some can request that the MySQL server itself map proxy users according to granted proxy privileges: mysql\_native\_password, sha256\_password.

If the [check\\_proxy\\_users](#page-142-2) system variable is enabled, the server performs proxy user mapping for any authentication plugins that make such a request. However, it may also be necessary to enable plugin-specific system variables to take advantage of server proxy user mapping support:

- For the mysql\_native\_password plugin, enable [mysql\\_native\\_password\\_proxy\\_users](#page-192-3).
- For the sha256\_password plugin, enable sha256\_password\_proxy\_users.

For information about user proxying, see Section 6.2.14, "Proxy Users".

<span id="page-142-3"></span>• [collation\\_connection](#page-142-3)

| System Variable | collation_connection   |
|-----------------|------------------------|
| Scope           | 715<br>Global, Session |

| Dynamic | Yes    |
|---------|--------|
| Type    | String |

The collation of the connection character set. [collation\\_connection](#page-142-3) is important for comparisons of literal strings. For comparisons of strings with column values, [collation\\_connection](#page-142-3) does not matter because columns have their own collation, which has a higher collation precedence (see Section 10.8.4, "Collation Coercibility in Expressions").

#### <span id="page-143-0"></span>• [collation\\_database](#page-143-0)

| System Variable | collation_database                                                                                      |
|-----------------|---------------------------------------------------------------------------------------------------------|
| Scope           | Global, Session                                                                                         |
| Dynamic         | Yes                                                                                                     |
| Type            | String                                                                                                  |
| Default Value   | latin1_swedish_ci                                                                                       |
| Footnote        | This option is dynamic, but should be set only by<br>server. You should not set this variable manually. |

The collation used by the default database. The server sets this variable whenever the default database changes. If there is no default database, the variable has the same value as [collation\\_server](#page-143-1).

The global [character\\_set\\_database](#page-140-2) and [collation\\_database](#page-143-0) system variables are deprecated in MySQL 5.7; expect them to be removed in a future version of MySQL.

Assigning a value to the session [character\\_set\\_database](#page-140-2) and [collation\\_database](#page-143-0) system variables is deprecated in MySQL 5.7 and assignments produce a warning. Expect the session variables to become read only in a future version of MySQL and assignments to produce an error, while remaining possible to access the session variables to determine the database character set and collation for the default database.

#### <span id="page-143-1"></span>• [collation\\_server](#page-143-1)

| Command-Line Format | collation-server=name |
|---------------------|-----------------------|
| System Variable     | collation_server      |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | String                |
| Default Value       | latin1_swedish_ci     |

The server's default collation. See Section 10.15, "Character Set Configuration".

#### <span id="page-143-2"></span>• [completion\\_type](#page-143-2)

| Command-Line Format | completion-type=# |
|---------------------|-------------------|
| System Variable     | completion_type   |
| Scope               | Global, Session   |
| Dynamic             | Yes               |
| Type                | Enumeration       |
| Default Value       | NO_CHAIN          |
| Valid Values        | NO_CHAIN          |

| CHAIN   |
|---------|
| RELEASE |
| 0       |
| 1       |
| 2       |

The transaction completion type. This variable can take the values shown in the following table. The variable can be assigned using either the name values or corresponding integer values.

| Value           | Description                                                                                                                                                                                                       |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NO_CHAIN (or 0) | COMMIT and ROLLBACK are unaffected. This is<br>the default value.                                                                                                                                                 |
| CHAIN (or 1)    | COMMIT and ROLLBACK are equivalent to<br>COMMIT AND CHAIN and ROLLBACK AND<br>CHAIN, respectively. (A new transaction starts<br>immediately with the same isolation level as the<br>just-terminated transaction.) |
| RELEASE (or 2)  | COMMIT and ROLLBACK are equivalent to<br>COMMIT RELEASE and ROLLBACK RELEASE,<br>respectively. (The server disconnects after<br>terminating the transaction.)                                                     |

[completion\\_type](#page-143-2) affects transactions that begin with START TRANSACTION or BEGIN and end with COMMIT or ROLLBACK. It does not apply to implicit commits resulting from execution of the statements listed in Section 13.3.3, "Statements That Cause an Implicit Commit". It also does not apply for XA COMMIT, XA ROLLBACK, or when [autocommit=1](#page-135-1).

<span id="page-144-0"></span>• [concurrent\\_insert](#page-144-0)

| Command-Line Format | concurrent-insert[=value] |
|---------------------|---------------------------|
| System Variable     | concurrent_insert         |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Enumeration               |
| Default Value       | AUTO                      |
| Valid Values        | NEVER                     |
|                     | AUTO                      |
|                     | ALWAYS                    |
|                     | 0                         |
|                     | 1                         |

2

If AUTO (the default), MySQL permits INSERT and SELECT statements to run concurrently for MyISAM tables that have no free blocks in the middle of the data file.

This variable can take the values shown in the following table. The variable can be assigned using either the name values or corresponding integer values.

| Value         | Description                                                                                                                                                                                                                                                                             |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NEVER (or 0)  | Disables concurrent inserts                                                                                                                                                                                                                                                             |
| AUTO (or 1)   | (Default) Enables concurrent insert for MyISAM<br>tables that do not have holes                                                                                                                                                                                                         |
| ALWAYS (or 2) | Enables concurrent inserts for all MyISAM tables,<br>even those that have holes. For a table with a<br>hole, new rows are inserted at the end of the<br>table if it is in use by another thread. Otherwise,<br>MySQL acquires a normal write lock and inserts<br>the row into the hole. |

If you start mysqld with [--skip-new](#page-126-1), [concurrent\\_insert](#page-144-0) is set to NEVER.

See also Section 8.11.3, "Concurrent Inserts".

<span id="page-145-0"></span>• [connect\\_timeout](#page-145-0)

| Command-Line Format | connect-timeout=# |
|---------------------|-------------------|
| System Variable     | connect_timeout   |
| Scope               | Global            |
| Dynamic             | Yes               |
| Type                | Integer           |
| Default Value       | 10                |
| Minimum Value       | 2                 |
| Maximum Value       | 31536000          |
| Unit                | seconds           |

The number of seconds that the mysqld server waits for a connect packet before responding with Bad handshake. The default value is 10 seconds.

Increasing the [connect\\_timeout](#page-145-0) value might help if clients frequently encounter errors of the form Lost connection to MySQL server at 'XXX', system error: errno.

<span id="page-145-1"></span>• [core\\_file](#page-145-1)

| System Variable | core_file |
|-----------------|-----------|
| Scope           | Global    |
| Dynamic         | No        |
| Type            | Boolean   |
| Default Value   | OFF       |

Whether to write a core file if the server unexpectedly exits. This variable is set by the [--core-file](#page-110-2) option.

<span id="page-145-2"></span>• [datadir](#page-145-2)

| Command-Line Format | datadir=dir_name |
|---------------------|------------------|
| System Variable     | datadir          |
| Scope               | Global           |
| Dynamic             | No               |
| Type                | Directory name   |

The path to the MySQL server data directory. Relative paths are resolved with respect to the current directory. If you expect the server to be started automatically (that is, in contexts for which you cannot assume what the current directory is), it is best to specify the [datadir](#page-145-2) value as an absolute path.

<span id="page-146-0"></span>• [date\\_format](#page-146-0)

This variable is unused. It is deprecated and is removed in MySQL 8.0.

<span id="page-146-1"></span>• [datetime\\_format](#page-146-1)

This variable is unused. It is deprecated and is removed in MySQL 8.0.

<span id="page-146-2"></span>• [debug](#page-146-2)

| Command-Line Format     | debug[=debug_options]     |
|-------------------------|---------------------------|
| System Variable         | debug                     |
| Scope                   | Global, Session           |
| Dynamic                 | Yes                       |
| Type                    | String                    |
| Default Value (Unix)    | d:t:i:o,/tmp/mysqld.trace |
| Default Value (Windows) | d:t:i:O,\mysqld.trace     |

This variable indicates the current debugging settings. It is available only for servers built with debugging support. The initial value comes from the value of instances of the [--debug](#page-111-0) option given at server startup. The global and session values may be set at runtime.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 5.1.8.1, "System Variable Privileges".

Assigning a value that begins with + or - cause the value to added to or subtracted from the current value:

```
mysql> SET debug = 'T';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| T |
+---------+
mysql> SET debug = '+P';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| P:T |
+---------+
mysql> SET debug = '-P';
mysql> SELECT @@debug;
+---------+
```

```
| @@debug |
+---------+
| T |
+---------+
```

For more information, see Section 5.8.3, "The DBUG Package".

<span id="page-147-0"></span>• [debug\\_sync](#page-147-0)

| System Variable | debug_sync |
|-----------------|------------|
| Scope           | Session    |
| Dynamic         | Yes        |
| Type            | String     |

This variable is the user interface to the Debug Sync facility. Use of Debug Sync requires that MySQL be configured with the -DWITH\_DEBUG=ON CMake option (see Section 2.8.7, "MySQL Source-Configuration Options"); otherwise, this system variable is not available.

The global variable value is read only and indicates whether the facility is enabled. By default, Debug Sync is disabled and the value of [debug\\_sync](#page-147-0) is OFF. If the server is started with [--debug-sync](#page-111-1)[timeout=](#page-111-1)N, where N is a timeout value greater than 0, Debug Sync is enabled and the value of [debug\\_sync](#page-147-0) is ON - current signal followed by the signal name. Also, N becomes the default timeout for individual synchronization points.

The session value can be read by any user and has the same value as the global variable. The session value can be set to control synchronization points.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 5.1.8.1, "System Variable Privileges".

For a description of the Debug Sync facility and how to use synchronization points, see [MySQL](https://dev.mysql.com/doc/index-other.md) [Server Doxygen Documentation.](https://dev.mysql.com/doc/index-other.md)

<span id="page-147-1"></span>• [default\\_authentication\\_plugin](#page-147-1)

| Command-Line Format | default-authentication<br>plugin=plugin_name |
|---------------------|----------------------------------------------|
| System Variable     | default_authentication_plugin                |
| Scope               | Global                                       |
| Dynamic             | No                                           |
| Type                | Enumeration                                  |
| Default Value       | mysql_native_password                        |
| Valid Values        | mysql_native_password                        |
|                     | sha256_password                              |

The default authentication plugin. These values are permitted:

• mysql\_native\_password: Use MySQL native passwords; see Section 6.4.1.1, "Native Pluggable Authentication".

• sha256\_password: Use SHA-256 passwords; see Section 6.4.1.5, "SHA-256 Pluggable Authentication".

![](_page_148_Picture_2.jpeg)

#### **Note**

If this variable has a value other than mysql\_native\_password, clients older than MySQL 5.5.7 cannot connect because, of the permitted default authentication plugins, they understand only the mysql\_native\_password authentication protocol.

The [default\\_authentication\\_plugin](#page-147-1) value affects these aspects of server operation:

- It determines which authentication plugin the server assigns to new accounts created by CREATE USER and GRANT statements that do not explicitly specify an authentication plugin.
- The [old\\_passwords](#page-196-2) system variable affects password hashing for accounts that use the mysql\_native\_password or sha256\_password authentication plugin. If the default authentication plugin is one of those plugins, the server sets [old\\_passwords](#page-196-2) at startup to the value required by the plugin password hashing method.
- For an account created with either of the following statements, the server associates the account with the default authentication plugin and assigns the account the given password, hashed as required by that plugin:

```
CREATE USER ... IDENTIFIED BY 'cleartext password';
GRANT ... IDENTIFIED BY 'cleartext password';
```

• For an account created with either of the following statements, the server associates the account with the default authentication plugin and assigns the account the given password hash, if the password hash has the format required by the plugin:

```
CREATE USER ... IDENTIFIED BY PASSWORD 'encrypted password';
GRANT ... IDENTIFIED BY PASSWORD 'encrypted password';
```

If the password hash is not in the format required by the default authentication plugin, the statement fails.

<span id="page-148-0"></span>• [default\\_password\\_lifetime](#page-148-0)

| Command-Line Format | default-password-lifetime=# |
|---------------------|-----------------------------|
| System Variable     | default_password_lifetime   |
| Scope               | Global                      |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 0                           |
| Minimum Value       | 0                           |
| Maximum Value       | 65535                       |
| Unit                | days                        |

This variable defines the global automatic password expiration policy. The default [default\\_password\\_lifetime](#page-148-0) value is 0, which disables automatic password expiration. If the value of [default\\_password\\_lifetime](#page-148-0) is a positive integer N, it indicates the permitted password lifetime; passwords must be changed every N days.

The global password expiration policy can be overridden as desired for individual accounts using the password expiration options of the ALTER USER statement. See Section 6.2.11, "Password Management".

![](_page_149_Picture_3.jpeg)

#### **Note**

Prior to MySQL 5.7.11, the default [default\\_password\\_lifetime](#page-148-0) value is 360 (passwords must be changed approximately once per year). For those versions, be aware that, if you make no changes to the [default\\_password\\_lifetime](#page-148-0) variable or to individual user accounts, all user passwords expire after 360 days, and all user accounts start running in restricted mode when this happens. Clients (which are effectively users) connecting to the server then get an error indicating that the password must be changed: ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.

However, this is easy to miss for clients that automatically connect to the server, such as connections made from scripts. To avoid having such clients suddenly stop working due to a password expiring, make sure to change the password expiration settings for those clients, like this:

```
ALTER USER 'script'@'localhost' PASSWORD EXPIRE NEVER;
```

Alternatively, set the [default\\_password\\_lifetime](#page-148-0) variable to 0, thus disabling automatic password expiration for all users.

<span id="page-149-0"></span>• [default\\_storage\\_engine](#page-149-0)

| Command-Line Format | default-storage-engine=name |
|---------------------|-----------------------------|
| System Variable     | default_storage_engine      |
| Scope               | Global, Session             |
| Dynamic             | Yes                         |
| Type                | Enumeration                 |
| Default Value       | InnoDB                      |

The default storage engine for tables. See Chapter 15, Alternative Storage Engines. This variable sets the storage engine for permanent tables only. To set the storage engine for TEMPORARY tables, set the [default\\_tmp\\_storage\\_engine](#page-149-1) system variable.

To see which storage engines are available and enabled, use the SHOW ENGINES statement or query the INFORMATION\_SCHEMA ENGINES table.

If you disable the default storage engine at server startup, you must set the default engine for both permanent and TEMPORARY tables to a different engine or the server cannot start.

• [default\\_tmp\\_storage\\_engine](#page-149-1)

<span id="page-149-1"></span>

|     | Command-Line Format | default-tmp-storage-engine=name |
|-----|---------------------|---------------------------------|
|     | System Variable     | default_tmp_storage_engine      |
|     | Scope               | Global, Session                 |
|     | Dynamic             | Yes                             |
| 722 | Type                | Enumeration                     |

| Default Value | InnoDB |
|---------------|--------|
|---------------|--------|

The default storage engine for TEMPORARY tables (created with CREATE TEMPORARY TABLE). To set the storage engine for permanent tables, set the [default\\_storage\\_engine](#page-149-0) system variable. Also see the discussion of that variable regarding possible values.

If you disable the default storage engine at server startup, you must set the default engine for both permanent and TEMPORARY tables to a different engine or the server cannot start.

<span id="page-150-0"></span>• [default\\_week\\_format](#page-150-0)

| Command-Line Format | default-week-format=# |
|---------------------|-----------------------|
| System Variable     | default_week_format   |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | Integer               |
| Default Value       | 0                     |
| Minimum Value       | 0                     |
| Maximum Value       | 7                     |

The default mode value to use for the WEEK() function. See Section 12.7, "Date and Time Functions".

<span id="page-150-1"></span>• [delay\\_key\\_write](#page-150-1)

| Command-Line Format | delay-key-write[={OFF ON ALL}] |
|---------------------|--------------------------------|
| System Variable     | delay_key_write                |
| Scope               | Global                         |
| Dynamic             | Yes                            |
| Type                | Enumeration                    |
| Default Value       | ON                             |
| Valid Values        | OFF                            |
|                     | ON                             |
|                     | ALL                            |

This variable specifies how to use delayed key writes. It applies only to MyISAM tables. Delayed key writing causes key buffers not to be flushed between writes. See also Section 15.2.1, "MyISAM Startup Options".

This variable can have one of the following values to affect handling of the DELAY\_KEY\_WRITE table option that can be used in CREATE TABLE statements.

| Option | Description                                                                                                    |
|--------|----------------------------------------------------------------------------------------------------------------|
| OFF    | DELAY_KEY_WRITE is ignored.                                                                                    |
| ON     | MySQL honors any DELAY_KEY_WRITE option<br>specified in CREATE TABLE statements. This is<br>the default value. |

| Option | Description                                                                                              |
|--------|----------------------------------------------------------------------------------------------------------|
| ALL    | All new opened tables are treated as if they were<br>created with the DELAY_KEY_WRITE option<br>enabled. |

![](_page_151_Picture_2.jpeg)

#### **Note**

If you set this variable to ALL, you should not use MyISAM tables from within another program (such as another MySQL server or myisamchk) when the tables are in use. Doing so leads to index corruption.

If DELAY\_KEY\_WRITE is enabled for a table, the key buffer is not flushed for the table on every index update, but only when the table is closed. This speeds up writes on keys a lot, but if you use this feature, you should add automatic checking of all MyISAM tables by starting the server with the [myisam\\_recover\\_options](#page-190-0) system variable set (for example, myisam\_recover\_options='BACKUP,FORCE'). See [Section 5.1.7, "Server System Variables"](#page-133-0), and Section 15.2.1, "MyISAM Startup Options".

If you start mysqld with [--skip-new](#page-126-1), [delay\\_key\\_write](#page-150-1) is set to OFF.

![](_page_151_Picture_7.jpeg)

#### **Warning**

If you enable external locking with [--external-locking](#page-114-1), there is no protection against index corruption for tables that use delayed key writes.

<span id="page-151-0"></span>• [delayed\\_insert\\_limit](#page-151-0)

| Command-Line Format              | delayed-insert-limit=# |
|----------------------------------|------------------------|
| Deprecated                       | Yes                    |
| System Variable                  | delayed_insert_limit   |
| Scope                            | Global                 |
| Dynamic                          | Yes                    |
| Type                             | Integer                |
| Default Value                    | 100                    |
| Minimum Value                    | 1                      |
| Maximum Value (64-bit platforms) | 18446744073709551615   |
| Maximum Value (32-bit platforms) | 4294967295             |

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

• [delayed\\_insert\\_timeout](#page-151-1)

<span id="page-151-1"></span>

|     | Command-Line Format | delayed-insert-timeout=# |
|-----|---------------------|--------------------------|
|     | Deprecated          | Yes                      |
|     | System Variable     | delayed_insert_timeout   |
|     | Scope               | Global                   |
|     | Dynamic             | Yes                      |
|     | Type                | Integer                  |
|     | Default Value       | 300                      |
|     | Minimum Value       | 1                        |
| 724 | Maximum Value       | 31536000                 |

| Unit<br>seconds |  |
|-----------------|--|
|-----------------|--|

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-152-0"></span>• [delayed\\_queue\\_size](#page-152-0)

| Command-Line Format              | delayed-queue-size=# |
|----------------------------------|----------------------|
| Deprecated                       | Yes                  |
| System Variable                  | delayed_queue_size   |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 1000                 |
| Minimum Value                    | 1                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-152-1"></span>• [disabled\\_storage\\_engines](#page-152-1)

| Command-Line Format | disabled-storage<br>engines=engine[,engine] |
|---------------------|---------------------------------------------|
| System Variable     | disabled_storage_engines                    |
| Scope               | Global                                      |
| Dynamic             | No                                          |
| Type                | String                                      |
| Default Value       | empty string                                |

This variable indicates which storage engines cannot be used to create tables or tablespaces. For example, to prevent new MyISAM or FEDERATED tables from being created, start the server with these lines in the server option file:

```
[mysqld]
disabled_storage_engines="MyISAM,FEDERATED"
```

By default, [disabled\\_storage\\_engines](#page-152-1) is empty (no engines disabled), but it can be set to a comma-separated list of one or more engines (not case-sensitive). Any engine named in the value cannot be used to create tables or tablespaces with CREATE TABLE or CREATE TABLESPACE, and cannot be used with ALTER TABLE ... ENGINE or ALTER TABLESPACE ... ENGINE to change the storage engine of existing tables or tablespaces. Attempts to do so result in an [ER\\_DISABLED\\_STORAGE\\_ENGINE](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_disabled_storage_engine) error.

[disabled\\_storage\\_engines](#page-152-1) does not restrict other DDL statements for existing tables, such as CREATE INDEX, TRUNCATE TABLE, ANALYZE TABLE, DROP TABLE, or DROP TABLESPACE. This permits a smooth transition so that existing tables or tablespaces that use a disabled engine can be migrated to a permitted engine by means such as ALTER TABLE ... ENGINE permitted\_engine.

It is permitted to set the [default\\_storage\\_engine](#page-149-0) or [default\\_tmp\\_storage\\_engine](#page-149-1) system variable to a storage engine that is disabled. This could cause applications to behave erratically

or fail, although that might be a useful technique in a development environment for identifying applications that use disabled engines, so that they can be modified.

[disabled\\_storage\\_engines](#page-152-1) is disabled and has no effect if the server is started with any of these options: [--bootstrap](#page-109-0), [--initialize](#page-116-0), [--initialize-insecure](#page-116-1), [--skip-grant](#page-125-1)[tables](#page-125-1).

![](_page_153_Picture_3.jpeg)

#### **Note**

Setting [disabled\\_storage\\_engines](#page-152-1) might cause an issue with mysql\_upgrade. For details, see Section 4.4.7, "mysql\_upgrade — Check and Upgrade MySQL Tables".

<span id="page-153-0"></span>• [disconnect\\_on\\_expired\\_password](#page-153-0)

| Command-Line Format | disconnect-on-expired<br>password[={OFF ON}] |
|---------------------|----------------------------------------------|
| System Variable     | disconnect_on_expired_password               |
| Scope               | Global                                       |
| Dynamic             | No                                           |
| Type                | Boolean                                      |
| Default Value       | ON                                           |

This variable controls how the server handles clients with expired passwords:

- If the client indicates that it can handle expired passwords, the value of [disconnect\\_on\\_expired\\_password](#page-153-0) is irrelevant. The server permits the client to connect but puts it in sandbox mode.
- If the client does not indicate that it can handle expired passwords, the server handles the client according to the value of [disconnect\\_on\\_expired\\_password](#page-153-0):
  - If [disconnect\\_on\\_expired\\_password](#page-153-0): is enabled, the server disconnects the client.
  - If [disconnect\\_on\\_expired\\_password](#page-153-0): is disabled, the server permits the client to connect but puts it in sandbox mode.

For more information about the interaction of client and server settings relating to expired-password handling, see Section 6.2.12, "Server Handling of Expired Passwords".

<span id="page-153-1"></span>• [div\\_precision\\_increment](#page-153-1)

| Command-Line Format | div-precision-increment=# |
|---------------------|---------------------------|
| System Variable     | div_precision_increment   |
| Scope               | Global, Session           |
| Dynamic             | Yes                       |
| Type                | Integer                   |
| Default Value       | 4                         |
| Minimum Value       | 0                         |
| Maximum Value       | 30                        |

This variable indicates the number of digits by which to increase the scale of the result of division operations performed with the / operator. The default value is 4. The minimum and maximum values are 0 and 30, respectively. The following example illustrates the effect of increasing the default value.

mysql> **SELECT 1/7;**

```
+--------+
| 1/7 |
+--------+
| 0.1429 |
+--------+
mysql> SET div_precision_increment = 12;
mysql> SELECT 1/7;
+----------------+
| 1/7 |
+----------------+
| 0.142857142857 |
+----------------+
```

<span id="page-154-0"></span>• [end\\_markers\\_in\\_json](#page-154-0)

| Command-Line Format | end-markers-in-json[={OFF ON}] |
|---------------------|--------------------------------|
| System Variable     | end_markers_in_json            |
| Scope               | Global, Session                |
| Dynamic             | Yes                            |
| Type                | Boolean                        |
| Default Value       | OFF                            |

Whether optimizer JSON output should add end markers. See Section 8.15.9, "The end\_markers\_in\_json System Variable".

<span id="page-154-1"></span>• [eq\\_range\\_index\\_dive\\_limit](#page-154-1)

| Command-Line Format | eq-range-index-dive-limit=# |
|---------------------|-----------------------------|
| System Variable     | eq_range_index_dive_limit   |
| Scope               | Global, Session             |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 200                         |
| Minimum Value       | 0                           |
| Maximum Value       | 4294967295                  |

This variable indicates the number of equality ranges in an equality comparison condition when the optimizer should switch from using index dives to index statistics in estimating the number of qualifying rows. It applies to evaluation of expressions that have either of these equivalent forms, where the optimizer uses a nonunique index to look up col\_name values:

```
col_name IN(val1, ..., valN)
col_name = val1 OR ... OR col_name = valN
```

In both cases, the expression contains N equality ranges. The optimizer can make row estimates using index dives or index statistics. If [eq\\_range\\_index\\_dive\\_limit](#page-154-1) is greater than 0, the optimizer uses existing index statistics instead of index dives if there are [eq\\_range\\_index\\_dive\\_limit](#page-154-1) or more equality ranges. Thus, to permit use of index dives for up to N equality ranges, set [eq\\_range\\_index\\_dive\\_limit](#page-154-1) to N + 1. To disable use of index statistics and always use index dives regardless of N, set [eq\\_range\\_index\\_dive\\_limit](#page-154-1) to 0.

For more information, see Equality Range Optimization of Many-Valued Comparisons.

To update table index statistics for best estimates, use ANALYZE TABLE.

<span id="page-155-0"></span>• [error\\_count](#page-155-0)

The number of errors that resulted from the last statement that generated messages. This variable is read only. See Section 13.7.5.17, "SHOW ERRORS Statement".

<span id="page-155-1"></span>• [event\\_scheduler](#page-155-1)

| Command-Line Format | event-scheduler[=value] |
|---------------------|-------------------------|
| System Variable     | event_scheduler         |
| Scope               | Global                  |
| Dynamic             | Yes                     |
| Type                | Enumeration             |
| Default Value       | OFF                     |
| Valid Values        | OFF                     |
|                     | ON                      |
|                     | DISABLED                |

This variable enables or disables, and starts or stops, the Event Scheduler. The possible status values are ON, OFF, and DISABLED. Turning the Event Scheduler OFF is not the same as disabling the Event Scheduler, which requires setting the status to DISABLED. This variable and its effects on the Event Scheduler's operation are discussed in greater detail in Section 23.4.2, "Event Scheduler Configuration"

<span id="page-155-2"></span>• [explicit\\_defaults\\_for\\_timestamp](#page-155-2)

| Command-Line Format | explicit-defaults-for<br>timestamp[={OFF ON}] |
|---------------------|-----------------------------------------------|
| Deprecated          | Yes                                           |
| System Variable     | explicit_defaults_for_timestamp               |
| Scope               | Global, Session                               |
| Dynamic             | Yes                                           |
| Type                | Boolean                                       |
| Default Value       | OFF                                           |

This system variable determines whether the server enables certain nonstandard behaviors for default values and NULL-value handling in TIMESTAMP columns. By default, [explicit\\_defaults\\_for\\_timestamp](#page-155-2) is disabled, which enables the nonstandard behaviors.

If [explicit\\_defaults\\_for\\_timestamp](#page-155-2) is disabled, the server enables the nonstandard behaviors and handles TIMESTAMP columns as follows:

- TIMESTAMP columns not explicitly declared with the NULL attribute are automatically declared with the NOT NULL attribute. Assigning such a column a value of NULL is permitted and sets the column to the current timestamp.
- The first TIMESTAMP column in a table, if not explicitly declared with the NULL attribute or an explicit DEFAULT or ON UPDATE attribute, is automatically declared with the DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP attributes.
- TIMESTAMP columns following the first one, if not explicitly declared with the NULL attribute or an explicit DEFAULT attribute, are automatically declared as DEFAULT '0000-00-00 00:00:00'

(the "zero" timestamp). For inserted rows that specify no explicit value for such a column, the column is assigned '0000-00-00 00:00:00' and no warning occurs.

Depending on whether strict SQL mode or the NO\_ZERO\_DATE SQL mode is enabled, a default value of '0000-00-00 00:00:00' may be invalid. Be aware that the TRADITIONAL SQL mode includes strict mode and NO\_ZERO\_DATE. See Section 5.1.10, "Server SQL Modes".

The nonstandard behaviors just described are deprecated; expect them to be removed in a future release of MySQL.

If [explicit\\_defaults\\_for\\_timestamp](#page-155-2) is enabled, the server disables the nonstandard behaviors and handles TIMESTAMP columns as follows:

- It is not possible to assign a TIMESTAMP column a value of NULL to set it to the current timestamp. To assign the current timestamp, set the column to CURRENT\_TIMESTAMP or a synonym such as NOW().
- TIMESTAMP columns not explicitly declared with the NOT NULL attribute are automatically declared with the NULL attribute and permit NULL values. Assigning such a column a value of NULL sets it to NULL, not the current timestamp.
- TIMESTAMP columns declared with the NOT NULL attribute do not permit NULL values. For inserts that specify NULL for such a column, the result is either an error for a single-row insert if strict SQL mode is enabled, or '0000-00-00 00:00:00' is inserted for multiple-row inserts with strict SQL mode disabled. In no case does assigning the column a value of NULL set it to the current timestamp.
- TIMESTAMP columns explicitly declared with the NOT NULL attribute and without an explicit DEFAULT attribute are treated as having no default value. For inserted rows that specify no explicit value for such a column, the result depends on the SQL mode. If strict SQL mode is enabled, an error occurs. If strict SQL mode is not enabled, the column is declared with the implicit default of '0000-00-00 00:00:00' and a warning occurs. This is similar to how MySQL treats other temporal types such as DATETIME.
- No TIMESTAMP column is automatically declared with the DEFAULT CURRENT\_TIMESTAMP or ON UPDATE CURRENT\_TIMESTAMP attributes. Those attributes must be explicitly specified.
- The first TIMESTAMP column in a table is not handled differently from TIMESTAMP columns following the first one.

If [explicit\\_defaults\\_for\\_timestamp](#page-155-2) is disabled at server startup, this warning appears in the error log:

```
[Warning] TIMESTAMP with implicit DEFAULT value is deprecated.
Please use --explicit_defaults_for_timestamp server option (see
documentation for more details).
```

As indicated by the warning, to disable the deprecated nonstandard behaviors, enable the [explicit\\_defaults\\_for\\_timestamp](#page-155-2) system variable at server startup.

![](_page_156_Picture_14.jpeg)

#### **Note**

[explicit\\_defaults\\_for\\_timestamp](#page-155-2) is itself deprecated because its only purpose is to permit control over deprecated TIMESTAMP behaviors that are to be removed in a future release of MySQL. When removal of those behaviors occurs, [explicit\\_defaults\\_for\\_timestamp](#page-155-2) no longer has any purpose, and you can expect it to be removed as well.

For additional information, see Section 11.2.6, "Automatic Initialization and Updating for TIMESTAMP and DATETIME".

## <span id="page-157-0"></span>• [external\\_user](#page-157-0)

| System Variable | external_user |
|-----------------|---------------|
| Scope           | Session       |
| Dynamic         | No            |
| Type            | String        |

The external user name used during the authentication process, as set by the plugin used to authenticate the client. With native (built-in) MySQL authentication, or if the plugin does not set the value, this variable is NULL. See Section 6.2.14, "Proxy Users".

## <span id="page-157-1"></span>• [flush](#page-157-1)

| Command-Line Format | flush[={OFF ON}] |
|---------------------|------------------|
| System Variable     | flush            |
| Scope               | Global           |
| Dynamic             | Yes              |
| Type                | Boolean          |
| Default Value       | OFF              |

If ON, the server flushes (synchronizes) all changes to disk after each SQL statement. Normally, MySQL does a write of all changes to disk only after each SQL statement and lets the operating system handle the synchronizing to disk. See Section B.3.3.3, "What to Do If MySQL Keeps Crashing". This variable is set to ON if you start mysqld with the [--flush](#page-115-2) option.

![](_page_157_Picture_7.jpeg)

# **Note**

If [flush](#page-157-1) is enabled, the value of [flush\\_time](#page-157-2) does not matter and changes to [flush\\_time](#page-157-2) have no effect on flush behavior.

# <span id="page-157-2"></span>• [flush\\_time](#page-157-2)

| Command-Line Format | flush-time=# |
|---------------------|--------------|
| System Variable     | flush_time   |
| Scope               | Global       |
| Dynamic             | Yes          |
| Type                | Integer      |
| Default Value       | 0            |
| Minimum Value       | 0            |
| Maximum Value       | 31536000     |
| Unit                | seconds      |

If this is set to a nonzero value, all tables are closed every [flush\\_time](#page-157-2) seconds to free up resources and synchronize unflushed data to disk. This option is best used only on systems with minimal resources.

![](_page_157_Picture_13.jpeg)

## **Note**

If [flush](#page-157-1) is enabled, the value of [flush\\_time](#page-157-2) does not matter and changes to [flush\\_time](#page-157-2) have no effect on flush behavior.

# <span id="page-158-0"></span>• [foreign\\_key\\_checks](#page-158-0)

| System Variable | foreign_key_checks |
|-----------------|--------------------|
| Scope           | Global, Session    |
| Dynamic         | Yes                |
| Type            | Boolean            |
| Default Value   | ON                 |

If set to 1 (the default), foreign key constraints are checked. If set to 0, foreign key constraints are ignored, with a couple of exceptions. When re-creating a table that was dropped, an error is returned if the table definition does not conform to the foreign key constraints referencing the table. Likewise, an ALTER TABLE operation returns an error if a foreign key definition is incorrectly formed. For more information, see Section 13.1.18.5, "FOREIGN KEY Constraints".

Setting this variable has the same effect on NDB tables as it does for InnoDB tables. Typically you leave this setting enabled during normal operation, to enforce referential integrity. Disabling foreign key checking can be useful for reloading InnoDB tables in an order different from that required by their parent/child relationships. See Section 13.1.18.5, "FOREIGN KEY Constraints".

Setting foreign\_key\_checks to 0 also affects data definition statements: DROP SCHEMA drops a schema even if it contains tables that have foreign keys that are referred to by tables outside the schema, and DROP TABLE drops tables that have foreign keys that are referred to by other tables.

![](_page_158_Picture_6.jpeg)

#### **Note**

Setting foreign\_key\_checks to 1 does not trigger a scan of the existing table data. Therefore, rows added to the table while [foreign\\_key\\_checks=0](#page-158-0) are not verified for consistency.

Dropping an index required by a foreign key constraint is not permitted, even with foreign\_key\_checks=0. The foreign key constraint must be removed before dropping the index (Bug #70260).

#### <span id="page-158-1"></span>• [ft\\_boolean\\_syntax](#page-158-1)

| Command-Line Format | ft-boolean-syntax=name |
|---------------------|------------------------|
| System Variable     | ft_boolean_syntax      |
| Scope               | Global                 |
| Dynamic             | Yes                    |
| Type                | String                 |

The list of operators supported by boolean full-text searches performed using IN BOOLEAN MODE. See Section 12.9.2, "Boolean Full-Text Searches".

The default variable value is '+ -><()~\*:""&|'. The rules for changing the value are as follows:

- Operator function is determined by position within the string.
- The replacement value must be 14 characters.
- Each character must be an ASCII nonalphanumeric character.
- Either the first or second character must be a space.
- No duplicates are permitted except the phrase quoting operators in positions 11 and 12. These two characters are not required to be the same, but they are the only two that may be.
- Positions 10, 13, and 14 (which by default are set to :, &, and |) are reserved for future extensions.
- <span id="page-159-0"></span>• [ft\\_max\\_word\\_len](#page-159-0)

| Command-Line Format | ft-max-word-len=# |
|---------------------|-------------------|
| System Variable     | ft_max_word_len   |
| Scope               | Global            |
| Dynamic             | No                |
| Type                | Integer           |
| Default Value       | 84                |
| Minimum Value       | 10                |
| Maximum Value       | 84                |

The maximum length of the word to be included in a MyISAM FULLTEXT index.

![](_page_159_Picture_13.jpeg)

#### **Note**

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable. Use REPAIR TABLE tbl\_name QUICK.

<span id="page-159-1"></span>• [ft\\_min\\_word\\_len](#page-159-1)

| Command-Line Format | ft-min-word-len=# |
|---------------------|-------------------|
| System Variable     | ft_min_word_len   |
| Scope               | Global            |
| Dynamic             | No                |
| Type                | Integer           |
| Default Value       | 4                 |
| Minimum Value       | 1                 |

| Maximum Value | 82 |
|---------------|----|
|---------------|----|

The minimum length of the word to be included in a MyISAM FULLTEXT index.

![](_page_160_Picture_3.jpeg)

#### **Note**

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable. Use REPAIR TABLE tbl\_name QUICK.

<span id="page-160-0"></span>• [ft\\_query\\_expansion\\_limit](#page-160-0)

| Command-Line Format | ft-query-expansion-limit=# |
|---------------------|----------------------------|
| System Variable     | ft_query_expansion_limit   |
| Scope               | Global                     |
| Dynamic             | No                         |
| Type                | Integer                    |
| Default Value       | 20                         |
| Minimum Value       | 0                          |
| Maximum Value       | 1000                       |

The number of top matches to use for full-text searches performed using WITH QUERY EXPANSION.

<span id="page-160-1"></span>• [ft\\_stopword\\_file](#page-160-1)

| Command-Line Format | ft-stopword-file=file_name |
|---------------------|----------------------------|
| System Variable     | ft_stopword_file           |
| Scope               | Global                     |
| Dynamic             | No                         |
| Type                | File name                  |

The file from which to read the list of stopwords for full-text searches on MyISAM tables. The server looks for the file in the data directory unless an absolute path name is given to specify a different directory. All the words from the file are used; comments are not honored. By default, a built-in list of stopwords is used (as defined in the storage/myisam/ft\_static.c file). Setting this variable to the empty string ('') disables stopword filtering. See also Section 12.9.4, "Full-Text Stopwords".

![](_page_160_Picture_12.jpeg)

# **Note**

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable or the contents of the stopword file. Use REPAIR TABLE tbl\_name QUICK.

<span id="page-160-2"></span>• [general\\_log](#page-160-2)

| Command-Line Format | general-log[={OFF ON}] |
|---------------------|------------------------|
| System Variable     | general_log            |
| Scope               | Global                 |
| Dynamic             | Yes                    |
| Type                | Boolean                |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

Whether the general query log is enabled. The value can be 0 (or OFF) to disable the log or 1 (or ON) to enable the log. The destination for log output is controlled by the [log\\_output](#page-173-0) system variable; if that value is NONE, no log entries are written even if the log is enabled.

#### <span id="page-161-0"></span>• [general\\_log\\_file](#page-161-0)

| Command-Line Format | general-log-file=file_name |
|---------------------|----------------------------|
| System Variable     | general_log_file           |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | File name                  |
| Default Value       | host_name.log              |

The name of the general query log file. The default value is host\_name.log, but the initial value can be changed with the [--general\\_log\\_file](#page-161-0) option.

## <span id="page-161-1"></span>• [group\\_concat\\_max\\_len](#page-161-1)

| Command-Line Format              | group-concat-max-len=# |
|----------------------------------|------------------------|
| System Variable                  | group_concat_max_len   |
| Scope                            | Global, Session        |
| Dynamic                          | Yes                    |
| Type                             | Integer                |
| Default Value                    | 1024                   |
| Minimum Value                    | 4                      |
| Maximum Value (64-bit platforms) | 18446744073709551615   |
| Maximum Value (32-bit platforms) | 4294967295             |

The maximum permitted result length in bytes for the GROUP\_CONCAT() function. The default is 1024.

#### <span id="page-161-2"></span>• [have\\_compress](#page-161-2)

YES if the zlib compression library is available to the server, NO if not. If not, the COMPRESS() and UNCOMPRESS() functions cannot be used.

#### <span id="page-161-3"></span>• [have\\_crypt](#page-161-3)

YES if the crypt() system call is available to the server, NO if not. If not, the ENCRYPT() function cannot be used.

![](_page_161_Picture_13.jpeg)

#### **Note**

The ENCRYPT() function is deprecated in MySQL 5.7, will be removed in a future release of MySQL, and should no longer be used. (For one-way hashing, consider using SHA2() instead.) Consequently, [have\\_crypt](#page-161-3) also is deprecated; expect it to be removed in a future release.

#### <span id="page-161-4"></span>• [have\\_dynamic\\_loading](#page-161-4)

YES if mysqld supports dynamic loading of plugins, NO if not. If the value is NO, you cannot use options such as --plugin-load to load plugins at server startup, or the INSTALL PLUGIN statement to load plugins at runtime.

<span id="page-162-0"></span>• [have\\_geometry](#page-162-0)

YES if the server supports spatial data types, NO if not.

<span id="page-162-1"></span>• [have\\_openssl](#page-162-1)

This variable is a synonym for [have\\_ssl](#page-162-5).

<span id="page-162-2"></span>• [have\\_profiling](#page-162-2)

YES if statement profiling capability is present, NO if not. If present, the profiling system variable controls whether this capability is enabled or disabled. See Section 13.7.5.31, "SHOW PROFILES Statement".

This variable is deprecated; expect it to be removed in a future release of MySQL.

<span id="page-162-3"></span>• [have\\_query\\_cache](#page-162-3)

YES if mysqld supports the query cache, NO if not.

![](_page_162_Picture_10.jpeg)

#### **Note**

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation includes [have\\_query\\_cache](#page-162-3).

<span id="page-162-4"></span>• [have\\_rtree\\_keys](#page-162-4)

YES if RTREE indexes are available, NO if not. (These are used for spatial indexes in MyISAM tables.)

<span id="page-162-5"></span>• [have\\_ssl](#page-162-5)

| System Variable | have_ssl                                                                                                              |
|-----------------|-----------------------------------------------------------------------------------------------------------------------|
| Scope           | Global                                                                                                                |
| Dynamic         | No                                                                                                                    |
| Type            | String                                                                                                                |
| Valid Values    | YES (SSL support available)                                                                                           |
|                 | DISABLED (SSL support was compiled into<br>server, but server was not started with necessary<br>options to enable it) |

YES if mysqld supports SSL connections, DISABLED if the server was compiled with SSL support, but was not started with the appropriate connection-encryption options. For more information, see Section 2.8.6, "Configuring SSL Library Support".

<span id="page-162-6"></span>• [have\\_statement\\_timeout](#page-162-6)

| System Variable | have_statement_timeout |
|-----------------|------------------------|
| Scope           | Global                 |
| Dynamic         | No                     |
| Type            | Boolean                |

Whether the statement execution timeout feature is available (see Statement Execution Time Optimizer Hints). The value can be NO if the background thread used by this feature could not be initialized.

## <span id="page-163-0"></span>• [have\\_symlink](#page-163-0)

YES if symbolic link support is enabled, NO if not. This is required on Unix for support of the DATA DIRECTORY and INDEX DIRECTORY table options. If the server is started with the [--skip](#page-129-3)[symbolic-links](#page-129-3) option, the value is DISABLED.

This variable has no meaning on Windows.

<span id="page-163-1"></span>• [host\\_cache\\_size](#page-163-1)

| Command-Line Format | host-cache-size=#                                              |
|---------------------|----------------------------------------------------------------|
| System Variable     | host_cache_size                                                |
| Scope               | Global                                                         |
| Dynamic             | Yes                                                            |
| Type                | Integer                                                        |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value       | 0                                                              |
| Maximum Value       | 65536                                                          |

The MySQL server maintains an in-memory host cache that contains client host name and IP address information and is used to avoid Domain Name System (DNS) lookups; see Section 5.1.11.2, "DNS Lookups and the Host Cache".

The [host\\_cache\\_size](#page-163-1) variable controls the size of the host cache, as well as the size of the Performance Schema host\_cache table that exposes the cache contents. Setting [host\\_cache\\_size](#page-163-1) has these effects:

- Setting the size to 0 disables the host cache. With the cache disabled, the server performs a DNS lookup every time a client connects.
- Changing the size at runtime causes an implicit host cache flushing operation that clears the host cache, truncates the host\_cache table, and unblocks any blocked hosts.

The default value is autosized to 128, plus 1 for a value of [max\\_connections](#page-180-1) up to 500, plus 1 for every increment of 20 over 500 in the [max\\_connections](#page-180-1) value, capped to a limit of 2000.

Using the [--skip-host-cache](#page-126-0) option is similar to setting the host\_cache\_size system variable to 0, but host\_cache\_size is more flexible because it can also be used to resize, enable, and disable the host cache at runtime, not just at server startup.

Starting the server with [--skip-host-cache](#page-126-0) does not prevent runtime changes to the value of host\_cache\_size, but such changes have no effect and the cache is not re-enabled even if host\_cache\_size is set larger than 0.

Setting the host\_cache\_size system variable rather than the [--skip-host-cache](#page-126-0) option is preferred for the reasons given in the previous paragraph. In addition, the --skip-host-cache option is deprecated in MySQL 8.0, and its removal is expected in a future version of MySQL.

<span id="page-163-2"></span>• [hostname](#page-163-2)

| System Variable | hostname |
|-----------------|----------|
| Scope           | Global   |
| Dynamic         | No       |

| Type | String |
|------|--------|
|------|--------|

The server sets this variable to the server host name at startup.

#### <span id="page-164-0"></span>• [identity](#page-164-0)

This variable is a synonym for the [last\\_insert\\_id](#page-170-1) variable. It exists for compatibility with other database systems. You can read its value with SELECT @@identity, and set it using SET identity.

<span id="page-164-1"></span>• [ignore\\_db\\_dirs](#page-164-1)

| Deprecated      | Yes            |
|-----------------|----------------|
| System Variable | ignore_db_dirs |
| Scope           | Global         |
| Dynamic         | No             |
| Type            | String         |

A comma-separated list of names that are not considered as database directories in the data directory. The value is set from any instances of [--ignore-db-dir](#page-115-1) given at server startup.

As of MySQL 5.7.11, [--ignore-db-dir](#page-115-1) can be used at data directory initialization time with mysqld --initialize to specify directories that the server should ignore for purposes of assessing whether an existing data directory is considered empty. See Section 2.9.1, "Initializing the Data Directory".

This system variable is deprecated in MySQL 5.7. With the introduction of the data dictionary in MySQL 8.0, it became superfluous and was removed in that version.

<span id="page-164-2"></span>• [init\\_connect](#page-164-2)

| Command-Line Format | init-connect=name |
|---------------------|-------------------|
| System Variable     | init_connect      |
| Scope               | Global            |
| Dynamic             | Yes               |
| Type                | String            |

A string to be executed by the server for each client that connects. The string consists of one or more SQL statements, separated by semicolon characters.

For users that have the SUPER privilege, the content of [init\\_connect](#page-164-2) is not executed. This is done so that an erroneous value for [init\\_connect](#page-164-2) does not prevent all clients from connecting. For example, the value might contain a statement that has a syntax error, thus causing client connections to fail. Not executing [init\\_connect](#page-164-2) for users that have the SUPER privilege enables them to open a connection and fix the [init\\_connect](#page-164-2) value.

As of MySQL 5.7.22, [init\\_connect](#page-164-2) execution is skipped for any client user with an expired password. This is done because such a user cannot execute arbitrary statements, and thus [init\\_connect](#page-164-2) execution fails, leaving the client unable to connect. Skipping [init\\_connect](#page-164-2) execution enables the user to connect and change password.

The server discards any result sets produced by statements in the value of [init\\_connect](#page-164-2).

<span id="page-164-3"></span>• [init\\_file](#page-164-3)

| Command-Line Format | init-file=file_name | 737 |
|---------------------|---------------------|-----|

| System Variable | init_file |
|-----------------|-----------|
| Scope           | Global    |
| Dynamic         | No        |
| Type            | File name |

If specified, this variable names a file containing SQL statements to be read and executed during the startup process. Each statement must be on a single line and should not include comments.

If the server is started with any of the [--bootstrap](#page-109-0), [--initialize](#page-116-0), or [--initialize](#page-116-1)[insecure](#page-116-1) options, it operates in bootstap mode and some functionality is unavailable that limits the statements permitted in the file. These include statements that relate to account management (such as CREATE USER or GRANT), replication, and global transaction identifiers. See Section 16.1.3, "Replication with Global Transaction Identifiers".

• innodb\_xxx

InnoDB system variables are listed in Section 14.15, "InnoDB Startup Options and System Variables". These variables control many aspects of storage, memory use, and I/O patterns for InnoDB tables, and are especially important now that InnoDB is the default storage engine.

<span id="page-165-0"></span>• [insert\\_id](#page-165-0)

The value to be used by the following INSERT or ALTER TABLE statement when inserting an AUTO\_INCREMENT value. This is mainly used with the binary log.

<span id="page-165-1"></span>• [interactive\\_timeout](#page-165-1)

| Command-Line Format | interactive-timeout=# |
|---------------------|-----------------------|
| System Variable     | interactive_timeout   |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | Integer               |
| Default Value       | 28800                 |
| Minimum Value       | 1                     |
| Maximum Value       | 31536000              |
| Unit                | seconds               |

The number of seconds the server waits for activity on an interactive connection before closing it. An interactive client is defined as a client that uses the CLIENT\_INTERACTIVE option to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.md). See also wait\_timeout.

<span id="page-165-2"></span>• [internal\\_tmp\\_disk\\_storage\\_engine](#page-165-2)

| Command-Line Format | internal-tmp-disk-storage-engine=# |
|---------------------|------------------------------------|
| System Variable     | internal_tmp_disk_storage_engine   |
| Scope               | Global                             |
| Dynamic             | Yes                                |
| Type                | Enumeration                        |
| Default Value       | INNODB                             |
| Valid Values        | MYISAM                             |

INNODB

The storage engine for on-disk internal temporary tables (see Section 8.4.4, "Internal Temporary Table Use in MySQL"). Permitted values are MYISAM and INNODB (the default).

The optimizer uses the storage engine defined by <code>internal\_tmp\_disk\_storage\_engine</code> for ondisk internal temporary tables.

When using <code>internal\_tmp\_disk\_storage\_engine=INNODB</code> (the default), queries that generate on-disk internal temporary tables that exceed <code>InnoDB</code> row or column limits return <code>Row size too large</code> or <code>Too many columns</code> errors. The workaround is to set <code>internal tmp disk storage engine</code> to <code>MYISAM</code>.

<span id="page-166-0"></span>• join buffer size

| Command-Line Format                     | join-buffer-size=#   |
|-----------------------------------------|----------------------|
| System Variable                         | join_buffer_size     |
| Scope                                   | Global, Session      |
| Dynamic                                 | Yes                  |
| Туре                                    | Integer              |
| Default Value                           | 262144               |
| Minimum Value                           | 128                  |
| Maximum Value (Windows)                 | 4294967168           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551488 |
| Maximum Value (Other, 32-bit platforms) | 4294967168           |
| Unit                                    | bytes                |
| Block Size                              | 128                  |

The minimum size of the buffer that is used for plain index scans, range index scans, and joins that do not use indexes and thus perform full table scans. Normally, the best way to get fast joins is to add indexes. Increase the value of <code>join\_buffer\_size</code> to get a faster full join when adding indexes is not possible. One join buffer is allocated for each full join between two tables. For a complex join between several tables for which indexes are not used, multiple join buffers might be necessary.

The default is 256KB. The maximum permissible setting for <code>join\_buffer\_size</code> is 4GB-1. Larger values are permitted for 64-bit platforms (except 64-bit Windows, for which large values are truncated to 4GB-1 with a warning). The block size is 128, and a value that is not an exact multiple of the block size is rounded down to the next lower multiple of the block size by MySQL Server before storing the value for the system variable. The parser allows values up to the maximum unsigned integer value for the platform (4294967295 or 2<sup>32</sup>-1 for a 32-bit system, 18446744073709551615 or 2<sup>64</sup>-1 for a 64-bit system) but the actual maximum is a block size lower.

Unless a Block Nested-Loop or Batched Key Access algorithm is used, there is no gain from setting the buffer larger than required to hold each matching row, and all joins allocate at least the minimum size, so use caution in setting this variable to a large value globally. It is better to keep the global setting small and change the session setting to a larger value only in sessions that are doing large

joins. Memory allocation time can cause substantial performance drops if the global size is larger than needed by most queries that use it.

When Block Nested-Loop is used, a larger join buffer can be beneficial up to the point where all required columns from all rows in the first table are stored in the join buffer. This depends on the query; the optimal size may be smaller than holding all rows from the first tables.

When Batched Key Access is used, the value of [join\\_buffer\\_size](#page-166-0) defines how large the batch of keys is in each request to the storage engine. The larger the buffer, the more sequential access is made to the right hand table of a join operation, which can significantly improve performance.

For additional information about join buffering, see Section 8.2.1.6, "Nested-Loop Join Algorithms". For information about Batched Key Access, see Section 8.2.1.11, "Block Nested-Loop and Batched Key Access Joins".

<span id="page-167-1"></span>• [keep\\_files\\_on\\_create](#page-167-1)

| Command-Line Format | keep-files-on-create[={OFF ON}] |
|---------------------|---------------------------------|
| System Variable     | keep_files_on_create            |
| Scope               | Global, Session                 |
| Dynamic             | Yes                             |
| Type                | Boolean                         |
| Default Value       | OFF                             |

If a MyISAM table is created with no DATA DIRECTORY option, the .MYD file is created in the database directory. By default, if MyISAM finds an existing .MYD file in this case, it overwrites it. The same applies to .MYI files for tables created with no INDEX DIRECTORY option. To suppress this behavior, set the [keep\\_files\\_on\\_create](#page-167-1) variable to ON (1), in which case MyISAM does not overwrite existing files and returns an error instead. The default value is OFF (0).

If a MyISAM table is created with a DATA DIRECTORY or INDEX DIRECTORY option and an existing .MYD or .MYI file is found, MyISAM always returns an error. It does not overwrite a file in the specified directory.

<span id="page-167-0"></span>• [key\\_buffer\\_size](#page-167-0)

| Command-Line Format              | key-buffer-size=#    |
|----------------------------------|----------------------|
| System Variable                  | key_buffer_size      |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 8388608              |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | OS_PER_PROCESS_LIMIT |
| Maximum Value (32-bit platforms) | 4294967295           |
| Unit                             | bytes                |

Index blocks for MyISAM tables are buffered and are shared by all threads. [key\\_buffer\\_size](#page-167-0) is the size of the buffer used for index blocks. The key buffer is also known as the key cache.

The minimum permissible setting is 0, but you cannot set [key\\_buffer\\_size](#page-167-0) to 0 dynamically. A setting of 0 drops the key cache, which is not permitted at runtime. Setting [key\\_buffer\\_size](#page-167-0) to 0 is permitted only at startup, in which case the key cache is not initialized. Changing the

[key\\_buffer\\_size](#page-167-0) setting at runtime from a value of 0 to a permitted non-zero value initializes the key cache.

[key\\_buffer\\_size](#page-167-0) can be increased or decreased only in increments or multiples of 4096 bytes. Increasing or decreasing the setting by a nonconforming value produces a warning and truncates the setting to a conforming value.

The maximum permissible setting for [key\\_buffer\\_size](#page-167-0) is 4GB−1 on 32-bit platforms. Larger values are permitted for 64-bit platforms. The effective maximum size might be less, depending on your available physical RAM and per-process RAM limits imposed by your operating system or hardware platform. The value of this variable indicates the amount of memory requested. Internally, the server allocates as much memory as possible up to this amount, but the actual allocation might be less.

You can increase the value to get better index handling for all reads and multiple writes; on a system whose primary function is to run MySQL using the MyISAM storage engine, 25% of the machine's total memory is an acceptable value for this variable. However, you should be aware that, if you make the value too large (for example, more than 50% of the machine's total memory), your system might start to page and become extremely slow. This is because MySQL relies on the operating system to perform file system caching for data reads, so you must leave some room for the file system cache. You should also consider the memory requirements of any other storage engines that you may be using in addition to MyISAM.

For even more speed when writing many rows at the same time, use LOCK TABLES. See Section 8.2.4.1, "Optimizing INSERT Statements".

You can check the performance of the key buffer by issuing a SHOW STATUS statement and examining the Key\_read\_requests, Key\_reads, Key\_write\_requests, and Key\_writes status variables. (See Section 13.7.5, "SHOW Statements".) The Key\_reads/ Key\_read\_requests ratio should normally be less than 0.01. The Key\_writes/ Key\_write\_requests ratio is usually near 1 if you are using mostly updates and deletes, but might be much smaller if you tend to do updates that affect many rows at the same time or if you are using the DELAY\_KEY\_WRITE table option.

The fraction of the key buffer in use can be determined using [key\\_buffer\\_size](#page-167-0) in conjunction with the Key\_blocks\_unused status variable and the buffer block size, which is available from the [key\\_cache\\_block\\_size](#page-169-0) system variable:

```
1 - ((Key_blocks_unused * key_cache_block_size) / key_buffer_size)
```

This value is an approximation because some space in the key buffer is allocated internally for administrative structures. Factors that influence the amount of overhead for these structures include block size and pointer size. As block size increases, the percentage of the key buffer lost to overhead tends to decrease. Larger blocks results in a smaller number of read operations (because more keys are obtained per read), but conversely an increase in reads of keys that are not examined (if not all keys in a block are relevant to a query).

It is possible to create multiple MyISAM key caches. The size limit of 4GB applies to each cache individually, not as a group. See Section 8.10.2, "The MyISAM Key Cache".

<span id="page-168-0"></span>• [key\\_cache\\_age\\_threshold](#page-168-0)

| Command-Line Format | key-cache-age-threshold=# |
|---------------------|---------------------------|
| System Variable     | key_cache_age_threshold   |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Integer                   |
| Default Value       | 300                       |

| Minimum Value                    | 100                  |
|----------------------------------|----------------------|
| Maximum Value (64-bit platforms) | 18446744073709551516 |
| Maximum Value (32-bit platforms) | 4294967196           |
| Block Size                       | 100                  |

This value controls the demotion of buffers from the hot sublist of a key cache to the warm sublist. Lower values cause demotion to happen more quickly. The minimum value is 100. The default value is 300. See Section 8.10.2, "The MyISAM Key Cache".

<span id="page-169-0"></span>• [key\\_cache\\_block\\_size](#page-169-0)

| Command-Line Format | key-cache-block-size=# |
|---------------------|------------------------|
| System Variable     | key_cache_block_size   |
| Scope               | Global                 |
| Dynamic             | Yes                    |
| Type                | Integer                |
| Default Value       | 1024                   |
| Minimum Value       | 512                    |
| Maximum Value       | 16384                  |
| Unit                | bytes                  |
| Block Size          | 512                    |

The size in bytes of blocks in the key cache. The default value is 1024. See Section 8.10.2, "The MyISAM Key Cache".

<span id="page-169-1"></span>• [key\\_cache\\_division\\_limit](#page-169-1)

| Command-Line Format | key-cache-division-limit=# |
|---------------------|----------------------------|
| System Variable     | key_cache_division_limit   |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 100                        |
| Minimum Value       | 1                          |
| Maximum Value       | 100                        |

The division point between the hot and warm sublists of the key cache buffer list. The value is the percentage of the buffer list to use for the warm sublist. Permissible values range from 1 to 100. The default value is 100. See Section 8.10.2, "The MyISAM Key Cache".

<span id="page-169-2"></span>• [large\\_files\\_support](#page-169-2)

| System Variable | large_files_support |
|-----------------|---------------------|
| Scope           | Global              |
| Dynamic         | No                  |
| Type            | Boolean             |

Whether mysqld was compiled with options for large file support.

## <span id="page-170-2"></span>• [large\\_pages](#page-170-2)

| Command-Line Format | large-pages[={OFF ON}] |
|---------------------|------------------------|
| System Variable     | large_pages            |
| Scope               | Global                 |
| Dynamic             | No                     |
| Platform Specific   | Linux                  |
| Type                | Boolean                |
| Default Value       | OFF                    |

Whether large page support is enabled (via the [--large-pages](#page-118-0) option). See Section 8.12.4.3, "Enabling Large Page Support".

#### <span id="page-170-0"></span>• [large\\_page\\_size](#page-170-0)

| System Variable | large_page_size |
|-----------------|-----------------|
| Scope           | Global          |
| Dynamic         | No              |
| Type            | Integer         |
| Default Value   | 0               |
| Minimum Value   | 0               |
| Maximum Value   | 65535           |
| Unit            | bytes           |

If large page support is enabled, this shows the size of memory pages. Large memory pages are supported only on Linux; on other platforms, the value of this variable is always 0. See Section 8.12.4.3, "Enabling Large Page Support".

#### <span id="page-170-1"></span>• [last\\_insert\\_id](#page-170-1)

The value to be returned from LAST\_INSERT\_ID(). This is stored in the binary log when you use LAST\_INSERT\_ID() in a statement that updates a table. Setting this variable does not update the value returned by the [mysql\\_insert\\_id\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-insert-id.md) C API function.

#### <span id="page-170-3"></span>• [lc\\_messages](#page-170-3)

| Command-Line Format | lc-messages=name |
|---------------------|------------------|
| System Variable     | lc_messages      |
| Scope               | Global, Session  |
| Dynamic             | Yes              |
| Type                | String           |
| Default Value       | en_US            |

The locale to use for error messages. The default is en\_US. The server converts the argument to a language name and combines it with the value of [lc\\_messages\\_dir](#page-170-4) to produce the location for the error message file. See Section 10.12, "Setting the Error Message Language".

#### <span id="page-170-4"></span>• [lc\\_messages\\_dir](#page-170-4)

| Command-Line Format | lc-messages-dir=dir_name |
|---------------------|--------------------------|
| System Variable     | 743<br>lc_messages_dir   |

| Scope   | Global         |
|---------|----------------|
| Dynamic | No             |
| Type    | Directory name |

The directory where error messages are located. The server uses the value together with the value of [lc\\_messages](#page-170-3) to produce the location for the error message file. See Section 10.12, "Setting the Error Message Language".

#### <span id="page-171-0"></span>• [lc\\_time\\_names](#page-171-0)

| Command-Line Format | lc-time-names=value |
|---------------------|---------------------|
| System Variable     | lc_time_names       |
| Scope               | Global, Session     |
| Dynamic             | Yes                 |
| Type                | String              |

This variable specifies the locale that controls the language used to display day and month names and abbreviations. This variable affects the output from the DATE\_FORMAT(), DAYNAME() and MONTHNAME() functions. Locale names are POSIX-style values such as 'ja\_JP' or 'pt\_BR'. The default value is 'en\_US' regardless of your system's locale setting. For further information, see Section 10.16, "MySQL Server Locale Support".

# <span id="page-171-1"></span>• [license](#page-171-1)

| System Variable | license |
|-----------------|---------|
| Scope           | Global  |
| Dynamic         | No      |
| Type            | String  |
| Default Value   | GPL     |

The type of license the server has.

# <span id="page-171-2"></span>• [local\\_infile](#page-171-2)

| Command-Line Format | local-infile[={OFF ON}] |
|---------------------|-------------------------|
| System Variable     | local_infile            |
| Scope               | Global                  |
| Dynamic             | Yes                     |
| Type                | Boolean                 |
| Default Value       | ON                      |

This variable controls server-side LOCAL capability for LOAD DATA statements. Depending on the [local\\_infile](#page-171-2) setting, the server refuses or permits local data loading by clients that have LOCAL enabled on the client side.

To explicitly cause the server to refuse or permit LOAD DATA LOCAL statements (regardless of how client programs and libraries are configured at build time or runtime), start mysqld with [local\\_infile](#page-171-2) disabled or enabled, respectively. [local\\_infile](#page-171-2) can also be set at runtime. For more information, see Section 6.1.6, "Security Considerations for LOAD DATA LOCAL".

#### <span id="page-171-3"></span>• [lock\\_wait\\_timeout](#page-171-3)

| Command-Line Format | lock-wait-timeout=# |
|---------------------|---------------------|
|---------------------|---------------------|

| System Variable | lock_wait_timeout |
|-----------------|-------------------|
| Scope           | Global, Session   |
| Dynamic         | Yes               |
| Type            | Integer           |
| Default Value   | 31536000          |
| Minimum Value   | 1                 |
| Maximum Value   | 31536000          |
| Unit            | seconds           |

This variable specifies the timeout in seconds for attempts to acquire metadata locks. The permissible values range from 1 to 31536000 (1 year). The default is 31536000.

This timeout applies to all statements that use metadata locks. These include DML and DDL operations on tables, views, stored procedures, and stored functions, as well as LOCK TABLES, FLUSH TABLES WITH READ LOCK, and HANDLER statements.

This timeout does not apply to implicit accesses to system tables in the mysql database, such as grant tables modified by GRANT or REVOKE statements or table logging statements. The timeout does apply to system tables accessed directly, such as with SELECT or UPDATE.

The timeout value applies separately for each metadata lock attempt. A given statement can require more than one lock, so it is possible for the statement to block for longer than the [lock\\_wait\\_timeout](#page-171-3) value before reporting a timeout error. When lock timeout occurs, [ER\\_LOCK\\_WAIT\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_lock_wait_timeout) is reported.

[lock\\_wait\\_timeout](#page-171-3) does not apply to delayed inserts, which always execute with a timeout of 1 year. This is done to avoid unnecessary timeouts because a session that issues a delayed insert receives no notification of delayed insert timeouts.

<span id="page-172-0"></span>• [locked\\_in\\_memory](#page-172-0)

| System Variable | locked_in_memory |
|-----------------|------------------|
| Scope           | Global           |
| Dynamic         | No               |
| Type            | Boolean          |
| Default Value   | OFF              |

Whether mysqld was locked in memory with [--memlock](#page-121-0).

<span id="page-172-2"></span>• [log\\_error](#page-172-2)

| Command-Line Format | log-error[=file_name] |
|---------------------|-----------------------|
| System Variable     | log_error             |
| Scope               | Global                |
| Dynamic             | No                    |
| Type                | File name             |

The error log output destination. If the destination is the console, the value is stderr. Otherwise, the destination is a file and the [log\\_error](#page-172-2) value is the file name. See Section 5.4.2, "The Error Log".

<span id="page-172-1"></span>• [log\\_error\\_verbosity](#page-172-1)

| Command-Line Format | log-error-verbosity=# | 745 |
|---------------------|-----------------------|-----|

| System Variable | log_error_verbosity |
|-----------------|---------------------|
| Scope           | Global              |
| Dynamic         | Yes                 |
| Type            | Integer             |
| Default Value   | 3                   |
| Minimum Value   | 1                   |
| Maximum Value   | 3                   |

The verbosity of the server in writing error, warning, and note messages to the error log. The following table shows the permitted values. The default is 3.

| log_error_verbosity Value | Permitted Messages                       |
|---------------------------|------------------------------------------|
| 1                         | Error messages                           |
| 2                         | Error and warning messages               |
| 3                         | Error, warning, and information messages |

[log\\_error\\_verbosity](#page-172-1) was added in MySQL 5.7.2. It is preferred over, and should be used instead of, the older [log\\_warnings](#page-176-1) system variable. See the description of [log\\_warnings](#page-176-1) for information about how that variable relates to [log\\_error\\_verbosity](#page-172-1). In particular, assigning a value to [log\\_warnings](#page-176-1) assigns a value to [log\\_error\\_verbosity](#page-172-1) and vice versa.

#### <span id="page-173-0"></span>• [log\\_output](#page-173-0)

| Command-Line Format | log-output=name |
|---------------------|-----------------|
| System Variable     | log_output      |
| Scope               | Global          |
| Dynamic             | Yes             |
| Type                | Set             |
| Default Value       | FILE            |
| Valid Values        | TABLE           |
|                     | FILE            |
|                     | NONE            |

The destination or destinations for general query log and slow query log output. The value is a list one or more comma-separated words chosen from TABLE, FILE, and NONE. TABLE selects logging to the [general\\_log](#page-160-2) and slow\_log tables in the mysql system database. FILE selects logging to log files. NONE disables logging. If NONE is present in the value, it takes precedence over any other words that are present. TABLE and FILE can both be given to select both log output destinations.

This variable selects log output destinations, but does not enable log output. To do that, enable the [general\\_log](#page-160-2) and slow\_query\_log system variables. For FILE logging, the [general\\_log\\_file](#page-161-0) and slow\_query\_log\_file system variables determine the log file locations. For more information, see Section 5.4.1, "Selecting General Query Log and Slow Query Log Output Destinations".

#### • [log\\_queries\\_not\\_using\\_indexes](#page-173-1)

<span id="page-173-1"></span>

|     | Command-Line Format | log-queries-not-using<br>indexes[={OFF ON}] |
|-----|---------------------|---------------------------------------------|
| 746 | System Variable     | log_queries_not_using_indexes               |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | Yes     |
| Type          | Boolean |
| Default Value | OFF     |

If you enable this variable with the slow query log enabled, queries that are expected to retrieve all rows are logged. See Section 5.4.5, "The Slow Query Log". This option does not necessarily mean that no index is used. For example, a query that uses a full index scan uses an index but would be logged because the index would not limit the number of rows.

#### <span id="page-174-0"></span>• [log\\_slow\\_admin\\_statements](#page-174-0)

| Command-Line Format | log-slow-admin-statements[={OFF <br>ON}] |
|---------------------|------------------------------------------|
| System Variable     | log_slow_admin_statements                |
| Scope               | Global                                   |
| Dynamic             | Yes                                      |
| Type                | Boolean                                  |
| Default Value       | OFF                                      |

Include slow administrative statements in the statements written to the slow query log. Administrative statements include ALTER TABLE, ANALYZE TABLE, CHECK TABLE, CREATE INDEX, DROP INDEX, OPTIMIZE TABLE, and REPAIR TABLE.

#### <span id="page-174-1"></span>• [log\\_syslog](#page-174-1)

| Command-Line Format     | log-syslog[={OFF ON}] |
|-------------------------|-----------------------|
| System Variable         | log_syslog            |
| Scope                   | Global                |
| Dynamic                 | Yes                   |
| Type                    | Boolean               |
| Default Value (Unix)    | OFF                   |
| Default Value (Windows) | ON                    |

Whether to write error log output to the system log. This is the Event Log on Windows, and syslog on Unix and Unix-like systems. The default value is platform specific:

- On Windows, Event Log output is enabled by default.
- On Unix and Unix-like systems, syslog output is disabled by default.

Regardless of the default, [log\\_syslog](#page-174-1) can be set explicitly to control output on any supported platform.

System log output control is distinct from sending error output to a file or the console. Error output can be directed to a file or the console in addition to or instead of the system log as desired. See Section 5.4.2, "The Error Log".

# <span id="page-174-2"></span>• [log\\_syslog\\_facility](#page-174-2)

| Command-Line Format | log-syslog-facility=value |
|---------------------|---------------------------|
| System Variable     | log_syslog_facility       |
| Scope               | Global                    |

| Dynamic       | Yes    |
|---------------|--------|
| Type          | String |
| Default Value | daemon |

The facility for error log output written to syslog (what type of program is sending the message). This variable has no effect unless the [log\\_syslog](#page-174-1) system variable is enabled. See Section 5.4.2.3, "Error Logging to the System Log".

The permitted values can vary per operating system; consult your system syslog documentation.

This variable does not exist on Windows.

<span id="page-175-0"></span>• [log\\_syslog\\_include\\_pid](#page-175-0)

| Command-Line Format | log-syslog-include-pid[={OFF ON}] |
|---------------------|-----------------------------------|
| System Variable     | log_syslog_include_pid            |
| Scope               | Global                            |
| Dynamic             | Yes                               |
| Type                | Boolean                           |
| Default Value       | ON                                |

Whether to include the server process ID in each line of error log output written to syslog. This variable has no effect unless the [log\\_syslog](#page-174-1) system variable is enabled. See Section 5.4.2.3, "Error Logging to the System Log".

This variable does not exist on Windows.

<span id="page-175-1"></span>• [log\\_syslog\\_tag](#page-175-1)

| Command-Line Format | log-syslog-tag=tag |
|---------------------|--------------------|
| System Variable     | log_syslog_tag     |
| Scope               | Global             |
| Dynamic             | Yes                |
| Type                | String             |
| Default Value       | empty string       |

The tag to be added to the server identifier in error log output written to syslog. This variable has no effect unless the [log\\_syslog](#page-174-1) system variable is enabled. See Section 5.4.2.3, "Error Logging to the System Log".

By default, the server identifier is mysqld with no tag. If a tag value of tag is specified, it is appended to the server identifier with a leading hyphen, resulting in an identifier of mysqld-tag.

On Windows, to use a tag that does not already exist, the server must be run from an account with Administrator privileges, to permit creation of a registry entry for the tag. Elevated privileges are not required if the tag already exists.

• [log\\_timestamps](#page-175-2)

<span id="page-175-2"></span>

|     | Command-Line Format | log-timestamps=# |
|-----|---------------------|------------------|
|     | System Variable     | log_timestamps   |
|     | Scope               | Global           |
| 748 | Dynamic             | Yes              |

| Type          | Enumeration |
|---------------|-------------|
| Default Value | UTC         |
| Valid Values  | UTC         |
|               | SYSTEM      |

This variable controls the time zone of timestamps in messages written to the error log, and in general query log and slow query log messages written to files. It does not affect the time zone of general query log and slow query log messages written to tables (mysql.general\_log, mysql.slow\_log). Rows retrieved from those tables can be converted from the local system time zone to any desired time zone with CONVERT\_TZ() or by setting the session time\_zone system variable.

Permitted [log\\_timestamps](#page-175-2) values are UTC (the default) and SYSTEM (local system time zone).

Timestamps are written using ISO 8601 / RFC 3339 format: YYYY-MM-DDThh:mm:ss.uuuuuu plus a tail value of Z signifying Zulu time (UTC) or ±hh:mm (an offset from UTC).

<span id="page-176-0"></span>• [log\\_throttle\\_queries\\_not\\_using\\_indexes](#page-176-0)

| Command-Line Format | log-throttle-queries-not-using<br>indexes=# |
|---------------------|---------------------------------------------|
| System Variable     | log_throttle_queries_not_using_indexes      |
| Scope               | Global                                      |
| Dynamic             | Yes                                         |
| Type                | Integer                                     |
| Default Value       | 0                                           |
| Minimum Value       | 0                                           |
| Maximum Value       | 4294967295                                  |

If [log\\_queries\\_not\\_using\\_indexes](#page-173-1) is enabled, the [log\\_throttle\\_queries\\_not\\_using\\_indexes](#page-176-0) variable limits the number of such queries per minute that can be written to the slow query log. A value of 0 (the default) means "no limit". For more information, see Section 5.4.5, "The Slow Query Log".

<span id="page-176-1"></span>• [log\\_warnings](#page-176-1)

| Command-Line Format              | log-warnings[=#]     |
|----------------------------------|----------------------|
| Deprecated                       | Yes                  |
| System Variable                  | log_warnings         |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 2                    |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

Whether to produce additional warning messages to the error log. As of MySQL 5.7.2, information items previously governed by [log\\_warnings](#page-176-1) are governed by [log\\_error\\_verbosity](#page-172-1), which is preferred over, and should be used instead of, the older [log\\_warnings](#page-176-1) system variable. (The

[log\\_warnings](#page-176-1) system variable and [--log-warnings](#page-120-2) command-line option are deprecated; expect them to be removed in a future release of MySQL.)

[log\\_warnings](#page-176-1) is enabled by default (the default is 1 before MySQL 5.7.2, 2 as of 5.7.2). To disable it, set it to 0. If the value is greater than 0, the server logs messages about statements that are unsafe for statement-based logging. If the value is greater than 1, the server logs aborted connections and access-denied errors for new connection attempts. See Section B.3.2.9, "Communication Errors and Aborted Connections".

If you use replication, enabling this variable by setting it greater than 0 is recommended, to get more information about what is happening, such as messages about network failures and reconnections.

If a replica server is started with [log\\_warnings](#page-176-1) enabled, the replica prints messages to the error log to provide information about its status, such as the binary log and relay log coordinates where it starts its job, when it is switching to another relay log, when it reconnects after a disconnect, and so forth.

Assigning a value to [log\\_warnings](#page-176-1) assigns a value to [log\\_error\\_verbosity](#page-172-1) and vice versa. The variables are related as follows:

- Suppression of all [log\\_warnings](#page-176-1) items, achieved with [log\\_warnings=0](#page-176-1), is achieved with [log\\_error\\_verbosity=1](#page-172-1) (errors only).
- Items printed for [log\\_warnings=1](#page-176-1) or higher count as warnings and are printed for [log\\_error\\_verbosity=2](#page-172-1) or higher.
- Items printed for [log\\_warnings=2](#page-176-1) count as notes and are printed for [log\\_error\\_verbosity=3](#page-172-1).

As of MySQL 5.7.2, the default log level is controlled by [log\\_error\\_verbosity](#page-172-1), which has a default of 3. In addition, the default for [log\\_warnings](#page-176-1) changes from 1 to 2, which corresponds to [log\\_error\\_verbosity=3](#page-172-1). To achieve a logging level similar to the previous default, set [log\\_error\\_verbosity=2](#page-172-1).

In MySQL 5.7.2 and higher, use of [log\\_warnings](#page-176-1) is still permitted but maps onto use of [log\\_error\\_verbosity](#page-172-1) as follows:

- Setting [log\\_warnings=0](#page-176-1) is equivalent to [log\\_error\\_verbosity=1](#page-172-1) (errors only).
- Setting [log\\_warnings=1](#page-176-1) is equivalent to [log\\_error\\_verbosity=2](#page-172-1) (errors, warnings).
- Setting [log\\_warnings=2](#page-176-1) (or higher) is equivalent to [log\\_error\\_verbosity=3](#page-172-1) (errors, warnings, notes), and the server sets [log\\_warnings](#page-176-1) to 2 if a larger value is specified.
- <span id="page-177-0"></span>• [long\\_query\\_time](#page-177-0)

| Command-Line Format | long-query-time=# |
|---------------------|-------------------|
| System Variable     | long_query_time   |
| Scope               | Global, Session   |
| Dynamic             | Yes               |
| Type                | Numeric           |
| Default Value       | 10                |
| Minimum Value       | 0                 |
| Maximum Value       | 31536000          |

| Unit | seconds |
|------|---------|
|------|---------|

If a query takes longer than this many seconds, the server increments the Slow\_queries status variable. If the slow query log is enabled, the query is logged to the slow query log file. This value is measured in real time, not CPU time, so a query that is under the threshold on a lightly loaded system might be above the threshold on a heavily loaded one. The minimum and default values of [long\\_query\\_time](#page-177-0) are 0 and 10, respectively. The maximum is 31536000, which is 365 days in seconds. The value can be specified to a resolution of microseconds. See Section 5.4.5, "The Slow Query Log".

Smaller values of this variable result in more statements being considered long-running, with the result that more space is required for the slow query log. For very small values (less than one second), the log may grow quite large in a small time. Increasing the number of statements considered long-running may also result in false positives for the "excessive Number of Long Running Processes" alert in MySQL Enterprise Monitor, especially if Group Replication is enabled. For these reasons, very small values should be used in test environments only, or, in production environments, only for a short period.

#### <span id="page-178-0"></span>• [low\\_priority\\_updates](#page-178-0)

| Command-Line Format | low-priority-updates[={OFF ON}] |
|---------------------|---------------------------------|
| System Variable     | low_priority_updates            |
| Scope               | Global, Session                 |
| Dynamic             | Yes                             |
| Type                | Boolean                         |
| Default Value       | OFF                             |

If set to 1, all INSERT, UPDATE, DELETE, and LOCK TABLE WRITE statements wait until there is no pending SELECT or LOCK TABLE READ on the affected table. The same effect can be obtained using {INSERT | REPLACE | DELETE | UPDATE} LOW\_PRIORITY ... to lower the priority of only one query. This variable affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE). See Section 8.11.2, "Table Locking Issues".

#### <span id="page-178-1"></span>• [lower\\_case\\_file\\_system](#page-178-1)

| System Variable | lower_case_file_system |
|-----------------|------------------------|
| Scope           | Global                 |
| Dynamic         | No                     |
| Type            | Boolean                |

This variable describes the case sensitivity of file names on the file system where the data directory is located. OFF means file names are case-sensitive, ON means they are not case-sensitive. This variable is read only because it reflects a file system attribute and setting it would have no effect on the file system.

#### <span id="page-178-2"></span>• [lower\\_case\\_table\\_names](#page-178-2)

| Command-Line Format   | lower-case-table-names[=#] |
|-----------------------|----------------------------|
| System Variable       | lower_case_table_names     |
| Scope                 | Global                     |
| Dynamic               | No                         |
| Type                  | Integer                    |
| Default Value (macOS) | 2<br>751                   |

| Default Value (Unix)    | 0 |
|-------------------------|---|
| Default Value (Windows) | 1 |
| Minimum Value           | 0 |
| Maximum Value           | 2 |

If set to 0, table names are stored as specified and comparisons are case-sensitive. If set to 1, table names are stored in lowercase on disk and comparisons are not case-sensitive. If set to 2, table names are stored as given but compared in lowercase. This option also applies to database names and table aliases. For additional details, see Section 9.2.3, "Identifier Case Sensitivity".

The default value of this variable is platform-dependent (see [lower\\_case\\_file\\_system](#page-178-1)). On Linux and other Unix-like systems, the default is 0. On Windows the default value is 1. On macOS, the default value is 2. On Linux (and other Unix-like systems), setting the value to 2 is not supported; the server forces the value to 0 instead.

You should not set [lower\\_case\\_table\\_names](#page-178-2) to 0 if you are running MySQL on a system where the data directory resides on a case-insensitive file system (such as on Windows or macOS). It is an unsupported combination that could result in a hang condition when running an INSERT INTO ... SELECT ... FROM tbl\_name operation with the wrong tbl\_name lettercase. With MyISAM, accessing table names using different lettercases could cause index corruption.

An error message is printed and the server exits if you attempt to start the server with [-](#page-178-2) [lower\\_case\\_table\\_names=0](#page-178-2) on a case-insensitive file system.

The setting of this variable affects the behavior of replication filtering options with regard to case sensitivity. For more information, see Section 16.2.5, "How Servers Evaluate Replication Filtering Rules".

<span id="page-179-0"></span>• [max\\_allowed\\_packet](#page-179-0)

| Command-Line Format | max-allowed-packet=# |
|---------------------|----------------------|
| System Variable     | max_allowed_packet   |
| Scope               | Global, Session      |
| Dynamic             | Yes                  |
| Type                | Integer              |
| Default Value       | 4194304              |
| Minimum Value       | 1024                 |
| Maximum Value       | 1073741824           |
| Unit                | bytes                |
| Block Size          | 1024                 |

The maximum size of one packet or any generated/intermediate string, or any parameter sent by the [mysql\\_stmt\\_send\\_long\\_data\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-stmt-send-long-data.md) C API function. The default is 4MB.

The packet message buffer is initialized to [net\\_buffer\\_length](#page-193-0) bytes, but can grow up to [max\\_allowed\\_packet](#page-179-0) bytes when needed. This value by default is small, to catch large (possibly incorrect) packets.

You must increase this value if you are using large BLOB columns or long strings. It should be as big as the largest BLOB you want to use. The protocol limit for [max\\_allowed\\_packet](#page-179-0) is 1GB. The value should be a multiple of 1024; nonmultiples are rounded down to the nearest multiple.

When you change the message buffer size by changing the value of the [max\\_allowed\\_packet](#page-179-0) variable, you should also change the buffer size on the client side if your client program permits

it. The default [max\\_allowed\\_packet](#page-179-0) value built in to the client library is 1GB, but individual client programs might override this. For example, mysql and mysqldump have defaults of 16MB and 24MB, respectively. They also enable you to change the client-side value by setting [max\\_allowed\\_packet](#page-179-0) on the command line or in an option file.

The session value of this variable is read only. The client can receive up to as many bytes as the session value. However, the server cannot send to the client more bytes than the current global [max\\_allowed\\_packet](#page-179-0) value. (The global value could be less than the session value if the global value is changed after the client connects.)

#### <span id="page-180-0"></span>• [max\\_connect\\_errors](#page-180-0)

| Command-Line Format              | max-connect-errors=# |
|----------------------------------|----------------------|
| System Variable                  | max_connect_errors   |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 100                  |
| Minimum Value                    | 1                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

After [max\\_connect\\_errors](#page-180-0) successive connection requests from a host are interrupted without a successful connection, the server blocks that host from further connections. If a connection from a host is established successfully within fewer than [max\\_connect\\_errors](#page-180-0) attempts after a previous connection was interrupted, the error count for the host is cleared to zero. To unblock blocked hosts, flush the host cache; see Flushing the Host Cache.

#### <span id="page-180-1"></span>• [max\\_connections](#page-180-1)

| Command-Line Format | max-connections=# |
|---------------------|-------------------|
| System Variable     | max_connections   |
| Scope               | Global            |
| Dynamic             | Yes               |
| Type                | Integer           |
| Default Value       | 151               |
| Minimum Value       | 1                 |
| Maximum Value       | 100000            |

The maximum permitted number of simultaneous client connections. The maximum effective value is the lesser of the effective value of [open\\_files\\_limit](#page-197-0) - 810, and the value actually set for max\_connections.

For more information, see Section 5.1.11.1, "Connection Interfaces".

# <span id="page-180-2"></span>• [max\\_delayed\\_threads](#page-180-2)

| Command-Line Format | max-delayed-threads=# |
|---------------------|-----------------------|
| Deprecated          | Yes                   |
| System Variable     | max_delayed_threads   |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |

| Type          | Integer |
|---------------|---------|
| Default Value | 20      |
| Minimum Value | 0       |
| Maximum Value | 16384   |

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-181-0"></span>• [max\\_digest\\_length](#page-181-0)

| Command-Line Format | max-digest-length=# |
|---------------------|---------------------|
| System Variable     | max_digest_length   |
| Scope               | Global              |
| Dynamic             | No                  |
| Type                | Integer             |
| Default Value       | 1024                |
| Minimum Value       | 0                   |
| Maximum Value       | 1048576             |
| Unit                | bytes               |

The maximum number of bytes of memory reserved per session for computation of normalized statement digests. Once that amount of space is used during digest computation, truncation occurs: no further tokens from a parsed statement are collected or figure into its digest value. Statements that differ only after that many bytes of parsed tokens produce the same normalized statement digest and are considered identical if compared or if aggregated for digest statistics.

The length used for calculating a normalized statement digest is the sum of the length of the normalized statement digest and the length of the statement digest. Since the length of the statement digest is always 64, when the value of max\_digest\_length is 1024 (the default), the maximum length for a normalized SQL statement before truncation occurs is 1024 - 64 = 960 bytes.

![](_page_181_Picture_7.jpeg)

#### **Warning**

Setting [max\\_digest\\_length](#page-181-0) to zero disables digest production, which also disables server functionality that requires digests, such as MySQL Enterprise Firewall.

Decreasing the [max\\_digest\\_length](#page-181-0) value reduces memory use but causes the digest value of more statements to become indistinguishable if they differ only at the end. Increasing the value permits longer statements to be distinguished but increases memory use, particularly for workloads that involve large numbers of simultaneous sessions (the server allocates [max\\_digest\\_length](#page-181-0) bytes per session).

The parser uses this system variable as a limit on the maximum length of normalized statement digests that it computes. The Performance Schema, if it tracks statement digests, makes a copy of the digest value, using the performance\_schema\_max\_digest\_length. system variable as a limit on the maximum length of digests that it stores. Consequently, if performance\_schema\_max\_digest\_length is less than [max\\_digest\\_length](#page-181-0), digest values stored in the Performance Schema are truncated relative to the original digest values.

For more information about statement digesting, see Section 25.10, "Performance Schema Statement Digests".

## <span id="page-182-0"></span>• [max\\_error\\_count](#page-182-0)

| Command-Line Format | max-error-count=# |
|---------------------|-------------------|
| System Variable     | max_error_count   |
| Scope               | Global, Session   |
| Dynamic             | Yes               |
| Type                | Integer           |
| Default Value       | 64                |
| Minimum Value       | 0                 |
| Maximum Value       | 65535             |

The maximum number of error, warning, and information messages to be stored for display by the SHOW ERRORS and SHOW WARNINGS statements. This is the same as the number of condition areas in the diagnostics area, and thus the number of conditions that can be inspected by GET DIAGNOSTICS.

#### <span id="page-182-1"></span>• [max\\_execution\\_time](#page-182-1)

| Command-Line Format | max-execution-time=# |
|---------------------|----------------------|
| System Variable     | max_execution_time   |
| Scope               | Global, Session      |
| Dynamic             | Yes                  |
| Type                | Integer              |
| Default Value       | 0                    |
| Minimum Value       | 0                    |
| Maximum Value       | 4294967295           |
| Unit                | milliseconds         |

The execution timeout for SELECT statements, in milliseconds. If the value is 0, timeouts are not enabled.

[max\\_execution\\_time](#page-182-1) applies as follows:

- The global [max\\_execution\\_time](#page-182-1) value provides the default for the session value for new connections. The session value applies to SELECT executions executed within the session that include no MAX\_EXECUTION\_TIME(N) optimizer hint or for which N is 0.
- [max\\_execution\\_time](#page-182-1) applies to read-only SELECT statements. Statements that are not read only are those that invoke a stored function that modifies data as a side effect.
- [max\\_execution\\_time](#page-182-1) is ignored for SELECT statements in stored programs.
- <span id="page-182-2"></span>• [max\\_heap\\_table\\_size](#page-182-2)

| Command-Line Format | max-heap-table-size=# |
|---------------------|-----------------------|
| System Variable     | max_heap_table_size   |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | Integer               |
| Default Value       | 16777216              |
| Minimum Value       | 16384                 |

| Maximum Value (64-bit platforms) | 18446744073709550592 |
|----------------------------------|----------------------|
| Maximum Value (32-bit platforms) | 4294966272           |
| Unit                             | bytes                |
|                                  |                      |

This variable sets the maximum size to which user-created MEMORY tables are permitted to grow. The value of the variable is used to calculate MEMORY table MAX\_ROWS values.

Setting this variable has no effect on any existing MEMORY table, unless the table is re-created with a statement such as CREATE TABLE or altered with ALTER TABLE or TRUNCATE TABLE. A server restart also sets the maximum size of existing MEMORY tables to the global [max\\_heap\\_table\\_size](#page-182-2) value.

This variable is also used in conjunction with tmp\_table\_size to limit the size of internal inmemory tables. See Section 8.4.4, "Internal Temporary Table Use in MySQL".

max\_heap\_table\_size is not replicated. See Section 16.4.1.20, "Replication and MEMORY Tables", and Section 16.4.1.37, "Replication and Variables", for more information.

<span id="page-183-0"></span>• [max\\_insert\\_delayed\\_threads](#page-183-0)

| Deprecated      | Yes                        |
|-----------------|----------------------------|
| System Variable | max_insert_delayed_threads |
| Scope           | Global, Session            |
| Dynamic         | Yes                        |
| Type            | Integer                    |
| Default Value   | 0                          |
| Minimum Value   | 20                         |
| Maximum Value   | 16384                      |

This variable is a synonym for [max\\_delayed\\_threads](#page-180-2).

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-183-1"></span>• [max\\_join\\_size](#page-183-1)

| Command-Line Format | max-join-size=#      |
|---------------------|----------------------|
| System Variable     | max_join_size        |
| Scope               | Global, Session      |
| Dynamic             | Yes                  |
| Type                | Integer              |
| Default Value       | 18446744073709551615 |
| Minimum Value       | 1                    |
| Maximum Value       | 18446744073709551615 |

Do not permit statements that probably need to examine more than [max\\_join\\_size](#page-183-1) rows (for single-table statements) or row combinations (for multiple-table statements) or that are likely to do more than [max\\_join\\_size](#page-183-1) disk seeks. By setting this value, you can catch statements where keys are not used properly and that would probably take a long time. Set it if your users tend to

perform joins that lack a WHERE clause, that take a long time, or that return millions of rows. For more information, see Using Safe-Updates Mode (--safe-updates).

Setting this variable to a value other than DEFAULT resets the value of sql\_big\_selects to 0. If you set the sql\_big\_selects value again, the [max\\_join\\_size](#page-183-1) variable is ignored.

If a query result is in the query cache, no result size check is performed, because the result has previously been computed and it does not burden the server to send it to the client.

<span id="page-184-0"></span>• [max\\_length\\_for\\_sort\\_data](#page-184-0)

| Command-Line Format | max-length-for-sort-data=# |
|---------------------|----------------------------|
| System Variable     | max_length_for_sort_data   |
| Scope               | Global, Session            |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 1024                       |
| Minimum Value       | 4                          |
| Maximum Value       | 8388608                    |
| Unit                | bytes                      |

The cutoff on the size of index values that determines which filesort algorithm to use. See Section 8.2.1.14, "ORDER BY Optimization".

<span id="page-184-1"></span>• [max\\_points\\_in\\_geometry](#page-184-1)

| Command-Line Format | max-points-in-geometry=# |
|---------------------|--------------------------|
| System Variable     | max_points_in_geometry   |
| Scope               | Global, Session          |
| Dynamic             | Yes                      |
| Type                | Integer                  |
| Default Value       | 65536                    |
| Minimum Value       | 3                        |
| Maximum Value       | 1048576                  |

The maximum value of the points\_per\_circle argument to the ST\_Buffer\_Strategy() function.

<span id="page-184-2"></span>• [max\\_prepared\\_stmt\\_count](#page-184-2)

| Command-Line Format | max-prepared-stmt-count=# |
|---------------------|---------------------------|
| System Variable     | max_prepared_stmt_count   |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Integer                   |
| Default Value       | 16382                     |
| Minimum Value       | 0                         |
| Maximum Value       | 1048576                   |

This variable limits the total number of prepared statements in the server. It can be used in environments where there is the potential for denial-of-service attacks based on running the server out of memory by preparing huge numbers of statements. If the value is set lower than the current number of prepared statements, existing statements are not affected and can be used, but no new statements can be prepared until the current number drops below the limit. Setting the value to 0 disables prepared statements.

#### <span id="page-185-0"></span>• [max\\_seeks\\_for\\_key](#page-185-0)

| Command-Line Format                     | max-seeks-for-key=#  |
|-----------------------------------------|----------------------|
| System Variable                         | max_seeks_for_key    |
| Scope                                   | Global, Session      |
| Dynamic                                 | Yes                  |
| Type                                    | Integer              |
| Default Value (Windows)                 | 4294967295           |
| Default Value (Other, 64-bit platforms) | 18446744073709551615 |
| Default Value (Other, 32-bit platforms) | 4294967295           |
| Minimum Value                           | 1                    |
| Maximum Value (Windows)                 | 4294967295           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551615 |
| Maximum Value (Other, 32-bit platforms) | 4294967295           |

Limit the assumed maximum number of seeks when looking up rows based on a key. The MySQL optimizer assumes that no more than this number of key seeks are required when searching for matching rows in a table by scanning an index, regardless of the actual cardinality of the index (see Section 13.7.5.22, "SHOW INDEX Statement"). By setting this to a low value (say, 100), you can force MySQL to prefer indexes instead of table scans.

#### <span id="page-185-1"></span>• [max\\_sort\\_length](#page-185-1)

| Command-Line Format | max-sort-length=# |
|---------------------|-------------------|
| System Variable     | max_sort_length   |
| Scope               | Global, Session   |
| Dynamic             | Yes               |
| Type                | Integer           |
| Default Value       | 1024              |
| Minimum Value       | 4                 |
| Maximum Value       | 8388608           |
| Unit                | bytes             |

The number of bytes to use when sorting data values. The server uses only the first [max\\_sort\\_length](#page-185-1) bytes of each value and ignores the rest. Consequently, values that differ only after the first [max\\_sort\\_length](#page-185-1) bytes compare as equal for GROUP BY, ORDER BY, and DISTINCT operations.

Increasing the value of [max\\_sort\\_length](#page-185-1) may require increasing the value of sort\_buffer\_size as well. For details, see Section 8.2.1.14, "ORDER BY Optimization"

#### <span id="page-185-2"></span>• [max\\_sp\\_recursion\\_depth](#page-185-2)

| Command-Line Format | max-sp-recursion-depth[=#] |
|---------------------|----------------------------|
| System Variable     | max_sp_recursion_depth     |
| Scope               | Global, Session            |

| Dynamic       | Yes     |
|---------------|---------|
| Type          | Integer |
| Default Value | 0       |
| Minimum Value | 0       |
| Maximum Value | 255     |

The number of times that any given stored procedure may be called recursively. The default value for this option is 0, which completely disables recursion in stored procedures. The maximum value is 255.

Stored procedure recursion increases the demand on thread stack space. If you increase the value of [max\\_sp\\_recursion\\_depth](#page-185-2), it may be necessary to increase thread stack size by increasing the value of thread\_stack at server startup.

<span id="page-186-0"></span>• [max\\_tmp\\_tables](#page-186-0)

This variable is unused. It is deprecated and is removed in MySQL 8.0.

<span id="page-186-1"></span>• [max\\_user\\_connections](#page-186-1)

| Command-Line Format | max-user-connections=# |
|---------------------|------------------------|
| System Variable     | max_user_connections   |
| Scope               | Global, Session        |
| Dynamic             | Yes                    |
| Type                | Integer                |
| Default Value       | 0                      |
| Minimum Value       | 0                      |
| Maximum Value       | 4294967295             |

The maximum number of simultaneous connections permitted to any given MySQL user account. A value of 0 (the default) means "no limit."

This variable has a global value that can be set at server startup or runtime. It also has a read-only session value that indicates the effective simultaneous-connection limit that applies to the account associated with the current session. The session value is initialized as follows:

- If the user account has a nonzero MAX\_USER\_CONNECTIONS resource limit, the session [max\\_user\\_connections](#page-186-1) value is set to that limit.
- Otherwise, the session [max\\_user\\_connections](#page-186-1) value is set to the global value.

Account resource limits are specified using the CREATE USER or ALTER USER statement. See Section 6.2.16, "Setting Account Resource Limits".

<span id="page-186-2"></span>• [max\\_write\\_lock\\_count](#page-186-2)

| Command-Line Format                     | max-write-lock-count=# |
|-----------------------------------------|------------------------|
| System Variable                         | max_write_lock_count   |
| Scope                                   | Global                 |
| Dynamic                                 | Yes                    |
| Type                                    | Integer                |
| Default Value (Windows)                 | 4294967295             |
| Default Value (Other, 64-bit platforms) | 18446744073709551615   |

| Default Value (Other, 32-bit platforms) | 4294967295           |
|-----------------------------------------|----------------------|
| Minimum Value                           | 1                    |
| Maximum Value (Windows)                 | 4294967295           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551615 |
| Maximum Value (Other, 32-bit platforms) | 4294967295           |

After this many write locks, permit some pending read lock requests to be processed in between. Write lock requests have higher priority than read lock requests. However, if [max\\_write\\_lock\\_count](#page-186-2) is set to some low value (say, 10), read lock requests may be preferred over pending write lock requests if the read lock requests have already been passed over in favor of 10 write lock requests. Normally this behavior does not occur because [max\\_write\\_lock\\_count](#page-186-2) by default has a very large value.

#### <span id="page-187-0"></span>• mecab\_rc\_file

| Command-Line Format | mecab-rc-file=file_name |
|---------------------|-------------------------|
| System Variable     | mecab_rc_file           |
| Scope               | Global                  |
| Dynamic             | No                      |
| Type                | File name               |

The mecab\_rc\_file option is used when setting up the MeCab full-text parser.

The mecab\_rc\_file option defines the path to the mecabrc configuration file, which is the configuration file for MeCab. The option is read-only and can only be set at startup. The mecabrc configuration file is required to initialize MeCab.

For information about the MeCab full-text parser, see Section 12.9.9, "MeCab Full-Text Parser Plugin".

For information about options that can be specified in the MeCab mecabrc configuration file, refer to the [MeCab Documentation](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.md) on the [Google Developers](https://code.google.com/) site.

#### <span id="page-187-1"></span>• [metadata\\_locks\\_cache\\_size](#page-187-1)

| Command-Line Format | metadata-locks-cache-size=# |
|---------------------|-----------------------------|
| Deprecated          | Yes                         |
| System Variable     | metadata_locks_cache_size   |
| Scope               | Global                      |
| Dynamic             | No                          |
| Type                | Integer                     |
| Default Value       | 1024                        |
| Minimum Value       | 1                           |
| Maximum Value       | 1048576                     |
| Unit                | bytes                       |

The size of the metadata locks cache. The server uses this cache to avoid creation and destruction of synchronization objects. This is particularly helpful on systems where such operations are expensive, such as Windows XP.

In MySQL 5.7.4, metadata locking implementation changes make this variable unnecessary, and so it is deprecated; expect it to be removed in a future release of MySQL.

<span id="page-188-0"></span>• [metadata\\_locks\\_hash\\_instances](#page-188-0)

| Command-Line Format | metadata-locks-hash-instances=# |
|---------------------|---------------------------------|
| Deprecated          | Yes                             |
| System Variable     | metadata_locks_hash_instances   |
| Scope               | Global                          |
| Dynamic             | No                              |
| Type                | Integer                         |
| Default Value       | 8                               |
| Minimum Value       | 1                               |
| Maximum Value       | 1024                            |

The set of metadata locks can be partitioned into separate hashes to permit connections accessing different objects to use different locking hashes and reduce contention. The [metadata\\_locks\\_hash\\_instances](#page-188-0) system variable specifies the number of hashes (default 8).

In MySQL 5.7.4, metadata locking implementation changes make this variable unnecessary, and so it is deprecated; expect it to be removed in a future release of MySQL.

<span id="page-188-1"></span>• [min\\_examined\\_row\\_limit](#page-188-1)

| Command-Line Format              | min-examined-row-limit=# |
|----------------------------------|--------------------------|
| System Variable                  | min_examined_row_limit   |
| Scope                            | Global, Session          |
| Dynamic                          | Yes                      |
| Type                             | Integer                  |
| Default Value                    | 0                        |
| Minimum Value                    | 0                        |
| Maximum Value (64-bit platforms) | 18446744073709551615     |
| Maximum Value (32-bit platforms) | 4294967295               |

Queries that examine fewer than this number of rows are not logged to the slow query log.

<span id="page-188-2"></span>• [multi\\_range\\_count](#page-188-2)

| Command-Line Format | multi-range-count=# |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| System Variable     | multi_range_count   |
| Scope               | Global, Session     |
| Dynamic             | Yes                 |
| Type                | Integer             |
| Default Value       | 256                 |
| Minimum Value       | 1                   |
| Maximum Value       | 4294967295          |

This variable has no effect. It is deprecated and is removed in MySQL 8.0.

<span id="page-189-0"></span>• [myisam\\_data\\_pointer\\_size](#page-189-0)

| Command-Line Format | myisam-data-pointer-size=# |
|---------------------|----------------------------|
| System Variable     | myisam_data_pointer_size   |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Integer                    |
| Default Value       | 6                          |
| Minimum Value       | 2                          |
| Maximum Value       | 7                          |
| Unit                | bytes                      |

The default pointer size in bytes, to be used by CREATE TABLE for MyISAM tables when no MAX\_ROWS option is specified. This variable cannot be less than 2 or larger than 7. The default value is 6. See Section B.3.2.10, "The table is full".

<span id="page-189-1"></span>• [myisam\\_max\\_sort\\_file\\_size](#page-189-1)

| Command-Line Format                     | myisam-max-sort-file-size=# |
|-----------------------------------------|-----------------------------|
| System Variable                         | myisam_max_sort_file_size   |
| Scope                                   | Global                      |
| Dynamic                                 | Yes                         |
| Type                                    | Integer                     |
| Default Value (Windows)                 | 2146435072                  |
| Default Value (Other, 64-bit platforms) | 9223372036853727232         |
| Default Value (Other, 32-bit platforms) | 2147483648                  |
| Minimum Value                           | 0                           |
| Maximum Value (Windows)                 | 2146435072                  |
| Maximum Value (Other, 64-bit platforms) | 9223372036853727232         |
| Maximum Value (Other, 32-bit platforms) | 2147483648                  |
| Unit                                    | bytes                       |

The maximum size of the temporary file that MySQL is permitted to use while re-creating a MyISAM index (during REPAIR TABLE, ALTER TABLE, or LOAD DATA). If the file size would be larger than this value, the index is created using the key cache instead, which is slower. The value is given in bytes.

If MyISAM index files exceed this size and disk space is available, increasing the value may help performance. The space must be available in the file system containing the directory where the original index file is located.

<span id="page-189-2"></span>• [myisam\\_mmap\\_size](#page-189-2)

| Command-Line Format              | myisam-mmap-size=#   |
|----------------------------------|----------------------|
| System Variable                  | myisam_mmap_size     |
| Scope                            | Global               |
| Dynamic                          | No                   |
| Type                             | Integer              |
| Default Value (64-bit platforms) | 18446744073709551615 |

| Default Value (32-bit platforms) | 4294967295           |
|----------------------------------|----------------------|
| Minimum Value                    | 7                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |
| Unit                             | bytes                |

The maximum amount of memory to use for memory mapping compressed MyISAM files. If many compressed MyISAM tables are used, the value can be decreased to reduce the likelihood of memory-swapping problems.

<span id="page-190-0"></span>• [myisam\\_recover\\_options](#page-190-0)

| Command-Line Format | myisam-recover-options[=list] |
|---------------------|-------------------------------|
| System Variable     | myisam_recover_options        |
| Scope               | Global                        |
| Dynamic             | No                            |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | DEFAULT                       |
|                     | BACKUP                        |
|                     | FORCE                         |
|                     | QUICK                         |

Set the MyISAM storage engine recovery mode. The variable value is any combination of the values of OFF, DEFAULT, BACKUP, FORCE, or QUICK. If you specify multiple values, separate them by commas. Specifying the variable with no value at server startup is the same as specifying DEFAULT, and specifying with an explicit value of "" disables recovery (same as a value of OFF). If recovery is enabled, each time mysqld opens a MyISAM table, it checks whether the table is marked as crashed or was not closed properly. (The last option works only if you are running with external locking disabled.) If this is the case, mysqld runs a check on the table. If the table was corrupted, mysqld attempts to repair it.

The following options affect how the repair works.

| Option  | Description                                                                                                          |
|---------|----------------------------------------------------------------------------------------------------------------------|
| OFF     | No recovery.                                                                                                         |
| DEFAULT | Recovery without backup, forcing, or quick<br>checking.                                                              |
| BACKUP  | If the data file was changed during recovery,<br>save a backup of the tbl_name.MYD file as<br>tbl_name-datetime.BAK. |
| FORCE   | Run recovery even if we would lose more than<br>one row from the .MYD file.                                          |
| QUICK   | Do not check the rows in the table if there are not<br>any delete blocks.                                            |

Before the server automatically repairs a table, it writes a note about the repair to the error log. If you want to be able to recover from most problems without user intervention, you should use the options

BACKUP,FORCE. This forces a repair of a table even if some rows would be deleted, but it keeps the old data file as a backup so that you can later examine what happened.

See Section 15.2.1, "MyISAM Startup Options".

<span id="page-191-2"></span>• [myisam\\_repair\\_threads](#page-191-2)

![](_page_191_Picture_4.jpeg)

#### **Note**

This system variable is deprecated in MySQL 5.7; expect it to be removed in a future release of MySQL.

From MySQL 5.7.38, values other than 1 produce a warning.

If this value is greater than 1, MyISAM table indexes are created in parallel (each index in its own thread) during the Repair by sorting process. The default value is 1.

![](_page_191_Picture_9.jpeg)

#### **Note**

Multithreaded repair is beta-quality code.

<span id="page-191-0"></span>• [myisam\\_sort\\_buffer\\_size](#page-191-0)

| Command-Line Format              | myisam-sort-buffer-size=# |
|----------------------------------|---------------------------|
| System Variable                  | myisam_sort_buffer_size   |
| Scope                            | Global, Session           |
| Dynamic                          | Yes                       |
| Type                             | Integer                   |
| Default Value                    | 8388608                   |
| Minimum Value                    | 4096                      |
| Maximum Value (64-bit platforms) | 18446744073709551615      |
| Maximum Value (32-bit platforms) | 4294967295                |
| Unit                             | bytes                     |

The size of the buffer that is allocated when sorting MyISAM indexes during a REPAIR TABLE or when creating indexes with CREATE INDEX or ALTER TABLE.

<span id="page-191-1"></span>• [myisam\\_stats\\_method](#page-191-1)

| Command-Line Format | myisam-stats-method=name |
|---------------------|--------------------------|
| System Variable     | myisam_stats_method      |
| Scope               | Global, Session          |
| Dynamic             | Yes                      |
| Type                | Enumeration              |
| Default Value       | nulls_unequal            |
| Valid Values        | nulls_unequal            |
|                     | nulls_equal              |
|                     | nulls_ignored            |

How the server treats NULL values when collecting statistics about the distribution of index values for MyISAM tables. This variable has three possible values, nulls\_equal, nulls\_unequal, and nulls\_ignored. For nulls\_equal, all NULL index values are considered equal and form a single value group that has a size equal to the number of NULL values. For nulls\_unequal, NULL values are considered unequal, and each NULL forms a distinct value group of size 1. For nulls\_ignored, NULL values are ignored.

The method that is used for generating table statistics influences how the optimizer chooses indexes for query execution, as described in Section 8.3.7, "InnoDB and MyISAM Index Statistics Collection".

<span id="page-192-2"></span>• [myisam\\_use\\_mmap](#page-192-2)

| Command-Line Format | myisam-use-mmap[={OFF ON}] |
|---------------------|----------------------------|
| System Variable     | myisam_use_mmap            |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Boolean                    |
| Default Value       | OFF                        |

Use memory mapping for reading and writing MyISAM tables.

<span id="page-192-3"></span>• [mysql\\_native\\_password\\_proxy\\_users](#page-192-3)

| Command-Line Format | mysql-native-password-proxy<br>users[={OFF ON}] |
|---------------------|-------------------------------------------------|
| System Variable     | mysql_native_password_proxy_users               |
| Scope               | Global                                          |
| Dynamic             | Yes                                             |
| Type                | Boolean                                         |
| Default Value       | OFF                                             |

This variable controls whether the mysql\_native\_password built-in authentication plugin supports proxy users. It has no effect unless the [check\\_proxy\\_users](#page-142-2) system variable is enabled. For information about user proxying, see Section 6.2.14, "Proxy Users".

<span id="page-192-0"></span>• [named\\_pipe](#page-192-0)

| Command-Line Format | named-pipe[={OFF ON}] |
|---------------------|-----------------------|
| System Variable     | named_pipe            |
| Scope               | Global                |
| Dynamic             | No                    |
| Platform Specific   | Windows               |
| Type                | Boolean               |
| Default Value       | OFF                   |

(Windows only.) Indicates whether the server supports connections over named pipes.

<span id="page-192-1"></span>• [named\\_pipe\\_full\\_access\\_group](#page-192-1)

| Command-Line Format | named-pipe-full-access-group=value |
|---------------------|------------------------------------|
| System Variable     | named_pipe_full_access_group       |
| Scope               | Global                             |
| Dynamic             | No                                 |
| Platform Specific   | 765<br>Windows                     |

| Type          | String                         |
|---------------|--------------------------------|
| Default Value | empty string                   |
| Valid Values  | empty string                   |
|               | valid Windows local group name |
|               | *everyone*                     |

(Windows only.) The access control granted to clients on the named pipe created by the MySQL server is set to the minimum necessary for successful communication when the [named\\_pipe](#page-192-0) system variable is enabled to support named-pipe connections. Some MySQL client software can open named pipe connections without any additional configuration; however, other client software may still require full access to open a named pipe connection.

This variable sets the name of a Windows local group whose members are granted sufficient access by the MySQL server to use named-pipe clients. As of MySQL 5.7.34, the default value is set to an empty string, which means that no Windows user is granted full access to the named pipe.

A new Windows local group name (for example, mysql\_access\_client\_users) can be created in Windows and then used to replace the default value when access is absolutely necessary. In this case, limit the membership of the group to as few users as possible, removing users from the group when their client software is upgraded. A non-member of the group who attempts to open a connection to MySQL with the affected named-pipe client is denied access until a Windows administrator adds the user to the group. Newly added users must log out and log in again to join the group (required by Windows).

Setting the value to '\*everyone\*' provides a language-independent way of referring to the Everyone group on Windows. The Everyone group is not secure by default.

<span id="page-193-0"></span>• [net\\_buffer\\_length](#page-193-0)

| Command-Line Format | net-buffer-length=# |
|---------------------|---------------------|
| System Variable     | net_buffer_length   |
| Scope               | Global, Session     |
| Dynamic             | Yes                 |
| Type                | Integer             |
| Default Value       | 16384               |
| Minimum Value       | 1024                |
| Maximum Value       | 1048576             |
| Unit                | bytes               |
| Block Size          | 1024                |

Each client thread is associated with a connection buffer and result buffer. Both begin with a size given by [net\\_buffer\\_length](#page-193-0) but are dynamically enlarged up to [max\\_allowed\\_packet](#page-179-0) bytes as needed. The result buffer shrinks to [net\\_buffer\\_length](#page-193-0) after each SQL statement.

This variable should not normally be changed, but if you have very little memory, you can set it to the expected length of statements sent by clients. If statements exceed this length, the connection buffer is automatically enlarged. The maximum value to which [net\\_buffer\\_length](#page-193-0) can be set is 1MB.

The session value of this variable is read only.

• [net\\_read\\_timeout](#page-193-1)

<span id="page-193-1"></span>

| 766 | Command-Line Format | net-read-timeout=# |
|-----|---------------------|--------------------|

| System Variable | net_read_timeout |
|-----------------|------------------|
| Scope           | Global, Session  |
| Dynamic         | Yes              |
| Type            | Integer          |
| Default Value   | 30               |
| Minimum Value   | 1                |
| Maximum Value   | 31536000         |
| Unit            | seconds          |

The number of seconds to wait for more data from a connection before aborting the read. When the server is reading from the client, [net\\_read\\_timeout](#page-193-1) is the timeout value controlling when to abort. When the server is writing to the client, [net\\_write\\_timeout](#page-194-1) is the timeout value controlling when to abort. See also slave\_net\_timeout.

#### <span id="page-194-0"></span>• [net\\_retry\\_count](#page-194-0)

| Command-Line Format              | net-retry-count=#    |
|----------------------------------|----------------------|
| System Variable                  | net_retry_count      |
| Scope                            | Global, Session      |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 10                   |
| Minimum Value                    | 1                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

If a read or write on a communication port is interrupted, retry this many times before giving up. This value should be set quite high on FreeBSD because internal interrupts are sent to all threads.

#### <span id="page-194-1"></span>• [net\\_write\\_timeout](#page-194-1)

| Command-Line Format | net-write-timeout=# |
|---------------------|---------------------|
| System Variable     | net_write_timeout   |
| Scope               | Global, Session     |
| Dynamic             | Yes                 |
| Type                | Integer             |
| Default Value       | 60                  |
| Minimum Value       | 1                   |
| Maximum Value       | 31536000            |
| Unit                | seconds             |

The number of seconds to wait for a block to be written to a connection before aborting the write. See also [net\\_read\\_timeout](#page-193-1).

#### <span id="page-194-2"></span>• [new](#page-194-2)

| Command-Line Format | new[={OFF ON}]  |
|---------------------|-----------------|
| System Variable     | new             |
| Scope               | Global, Session |

| Dynamic       | Yes      |
|---------------|----------|
| Disabled by   | skip-new |
| Type          | Boolean  |
| Default Value | OFF      |

This variable was used in MySQL 4.0 to turn on some 4.1 behaviors, and is retained for backward compatibility. Its value is always OFF.

In NDB Cluster, setting this variable to ON makes it possible to employ partitioning types other than KEY or LINEAR KEY with NDB tables. This experimental feature is not supported in production, and is now deprecated and thus subject to removal in a future release. For additional information, see User-defined partitioning and the NDB storage engine (NDB Cluster).

<span id="page-195-0"></span>• ngram\_token\_size

| Command-Line Format | ngram-token-size=# |
|---------------------|--------------------|
| System Variable     | ngram_token_size   |
| Scope               | Global             |
| Dynamic             | No                 |
| Type                | Integer            |
| Default Value       | 2                  |
| Minimum Value       | 1                  |
| Maximum Value       | 10                 |

Defines the n-gram token size for the n-gram full-text parser. The ngram\_token\_size option is read-only and can only be modified at startup. The default value is 2 (bigram). The maximum value is 10.

For more information about how to configure this variable, see Section 12.9.8, "ngram Full-Text Parser".

<span id="page-195-1"></span>• [offline\\_mode](#page-195-1)

| Command-Line Format | offline-mode[={OFF ON}] |  |
|---------------------|-------------------------|--|
| System Variable     | offline_mode            |  |
| Scope               | Global                  |  |
| Dynamic             | Yes                     |  |
| Type                | Boolean                 |  |
| Default Value       | OFF                     |  |

Whether the server is in "offline mode", which has these characteristics:

- Connected client users who do not have the SUPER privilege are disconnected on the next request, with an appropriate error. Disconnection includes terminating running statements and releasing locks. Such clients also cannot initiate new connections, and receive an appropriate error.
- Connected client users who have the SUPER privilege are not disconnected, and can initiate new connections to manage the server.

• Replica threads are permitted to keep applying data to the server.

Only users who have the SUPER privilege can control offline mode. To put a server in offline mode, change the value of the [offline\\_mode](#page-195-1) system variable from OFF to ON. To resume normal operations, change [offline\\_mode](#page-195-1) from ON to OFF. In offline mode, clients that are refused access receive an [ER\\_SERVER\\_OFFLINE\\_MODE](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_server_offline_mode) error.

#### <span id="page-196-0"></span>• [old](#page-196-0)

| Command-Line Format | old[={OFF ON}] |
|---------------------|----------------|
| System Variable     | old            |
| Scope               | Global         |
| Dynamic             | No             |
| Type                | Boolean        |
| Default Value       | OFF            |

[old](#page-196-0) is a compatibility variable. It is disabled by default, but can be enabled at startup to revert the server to behaviors present in older versions.

When [old](#page-196-0) is enabled, it changes the default scope of index hints to that used prior to MySQL 5.1.17. That is, index hints with no FOR clause apply only to how indexes are used for row retrieval and not to resolution of ORDER BY or GROUP BY clauses. (See Section 8.9.4, "Index Hints".) Take care about enabling this in a replication setup. With statement-based binary logging, having different modes for the source and replicas might lead to replication errors.

#### <span id="page-196-1"></span>• [old\\_alter\\_table](#page-196-1)

| Command-Line Format | old-alter-table[={OFF ON}] |  |
|---------------------|----------------------------|--|
| System Variable     | old_alter_table            |  |
| Scope               | Global, Session            |  |
| Dynamic             | Yes                        |  |
| Type                | Boolean                    |  |
| Default Value       | OFF                        |  |

When this variable is enabled, the server does not use the optimized method of processing an ALTER TABLE operation. It reverts to using a temporary table, copying over the data, and then renaming the temporary table to the original, as used by MySQL 5.0 and earlier. For more information on the operation of ALTER TABLE, see Section 13.1.8, "ALTER TABLE Statement".

## <span id="page-196-2"></span>• [old\\_passwords](#page-196-2)

| Command-Line Format | old-passwords=value |  |
|---------------------|---------------------|--|
| Deprecated          | Yes                 |  |
| System Variable     | old_passwords       |  |
| Scope               | Global, Session     |  |
| Dynamic             | Yes                 |  |
| Type                | Enumeration         |  |
| Default Value       | 0                   |  |
| Valid Values        | 0                   |  |

2

![](_page_197_Picture_2.jpeg)

#### **Note**

This system variable is deprecated in MySQL 5.7; expect it to be removed in a future release of MySQL.

This variable controls the password hashing method used by the PASSWORD() function. It also influences password hashing performed by CREATE USER and GRANT statements that specify a password using an IDENTIFIED BY clause.

The following table shows, for each password hashing method, the permitted value of old\_passwords and which authentication plugins use the hashing method.

| Password Hashing Method  | old_passwords Value | Associated Authentication<br>Plugin |
|--------------------------|---------------------|-------------------------------------|
| MySQL 4.1 native hashing | 0                   | mysql_native_password               |
| SHA-256 hashing          | 2                   | sha256_password                     |

If you set [old\\_passwords=2](#page-196-2), follow the instructions for using the sha256\_password plugin at Section 6.4.1.5, "SHA-256 Pluggable Authentication".

The server sets the global [old\\_passwords](#page-196-2) value during startup to be consistent with the password hashing method required by the authentication plugin indicated by the [default\\_authentication\\_plugin](#page-147-1) system variable.

When a client successfully connects to the server, the server sets the session [old\\_passwords](#page-196-2) value appropriately for the account authentication method. For example, if the account uses the sha256\_password authentication plugin, the server sets old\_passwords=2.

For additional information about authentication plugins and hashing formats, see Section 6.2.13, "Pluggable Authentication", and Section 6.1.2.4, "Password Hashing in MySQL".

<span id="page-197-0"></span>• [open\\_files\\_limit](#page-197-0)

| Command-Line Format | open-files-limit=#             |  |
|---------------------|--------------------------------|--|
| System Variable     | open_files_limit               |  |
| Scope               | Global                         |  |
| Dynamic             | No                             |  |
| Type                | Integer                        |  |
| Default Value       | 5000, with possible adjustment |  |
| Minimum Value       | 0                              |  |
| Maximum Value       | platform dependent             |  |

The number of file descriptors available to mysqld from the operating system:

- At startup, mysqld reserves descriptors with setrlimit(), using the value requested at by setting this variable directly or by using the --open-files-limit option to mysqld\_safe. If mysqld produces the error Too many open files, try increasing the [open\\_files\\_limit](#page-197-0) value. Internally, the maximum value for this variable is the maximum unsigned integer value, but the actual maximum is platform dependent.
- At runtime, the value of [open\\_files\\_limit](#page-197-0) indicates the number of file descriptors actually permitted to mysqld by the operating system, which might differ from the value requested at

startup. If the number of file descriptors requested during startup cannot be allocated, mysqld writes a warning to the error log.

The effective [open\\_files\\_limit](#page-197-0) value is based on the value specified at system startup (if any) and the values of [max\\_connections](#page-180-1) and table\_open\_cache, using these formulas:

- 10 + max\_connections + (table\_open\_cache \* 2)
- max\_connections \* 5
- The operating system limit if that limit is positive but not Infinity.
- If the operating system limit is Infinity: open\_files\_limit value if specified at startup, 5000 if not.

The server attempts to obtain the number of file descriptors using the maximum of those values. If that many descriptors cannot be obtained, the server attempts to obtain as many as the system permits.

The effective value is 0 on systems where MySQL cannot change the number of open files.

On Unix, the value cannot be set greater than the value displayed by the ulimit -n command. On Linux systems using systemd, the value cannot be set greater than LimitNOFile (this is DefaultLimitNOFILE, if LimitNOFile is not set); otherwise, on Linux, the value of open\_files\_limit cannot exceed ulimit -n.

<span id="page-198-0"></span>• [optimizer\\_prune\\_level](#page-198-0)

| Command-Line Format | optimizer-prune-level=# |
|---------------------|-------------------------|
| System Variable     | optimizer_prune_level   |
| Scope               | Global, Session         |
| Dynamic             | Yes                     |
| Type                | Integer                 |
| Default Value       | 1                       |
| Minimum Value       | 0                       |
| Maximum Value       | 1                       |

Controls the heuristics applied during query optimization to prune less-promising partial plans from the optimizer search space. A value of 0 disables heuristics so that the optimizer performs an exhaustive search. A value of 1 causes the optimizer to prune plans based on the number of rows retrieved by intermediate plans.

<span id="page-198-1"></span>• [optimizer\\_search\\_depth](#page-198-1)

| Command-Line Format | optimizer-search-depth=# |  |
|---------------------|--------------------------|--|
| System Variable     | optimizer_search_depth   |  |
| Scope               | Global, Session          |  |
| Dynamic             | Yes                      |  |
| Type                | Integer                  |  |
| Default Value       | 62                       |  |
| Minimum Value       | 0                        |  |

| Maximum Value | 62 |  |
|---------------|----|--|
|---------------|----|--|

The maximum depth of search performed by the query optimizer. Values larger than the number of relations in a query result in better query plans, but take longer to generate an execution plan for a query. Values smaller than the number of relations in a query return an execution plan quicker, but the resulting plan may be far from being optimal. If set to 0, the system automatically picks a reasonable value.

<span id="page-199-0"></span>• [optimizer\\_switch](#page-199-0)

| Command-Line Format | optimizer-switch=value                           |
|---------------------|--------------------------------------------------|
| System Variable     | optimizer_switch                                 |
| Scope               | Global, Session                                  |
| Dynamic             | Yes                                              |
| Type                | Set                                              |
| Valid Values        | batched_key_access={on off}                      |
|                     | block_nested_loop={on off}                       |
|                     | condition_fanout_filter={on off}                 |
|                     | derived_merge={on off}                           |
|                     | duplicateweedout={on off}                        |
|                     | engine_condition_pushdown={on off}               |
|                     | firstmatch={on off}                              |
|                     | index_condition_pushdown={on off}                |
|                     | index_merge={on off}                             |
|                     | index_merge_intersection={on off}                |
|                     | index_merge_sort_union={on off}                  |
|                     | index_merge_union={on off}                       |
|                     | loosescan={on off}                               |
|                     | materialization={on off}                         |
|                     | mrr={on off}                                     |
|                     | mrr_cost_based={on off}                          |
|                     | prefer_ordering_index={on off}                   |
|                     | semijoin={on off}                                |
|                     | subquery_materialization_cost_based={on <br>off} |
|                     | use_index_extensions={on off}                    |

The [optimizer\\_switch](#page-199-0) system variable enables control over optimizer behavior. The value of this variable is a set of flags, each of which has a value of on or off to indicate whether the

corresponding optimizer behavior is enabled or disabled. This variable has global and session values and can be changed at runtime. The global default can be set at server startup.

To see the current set of optimizer flags, select the variable value:

```
mysql> SELECT @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,
 index_merge_sort_union=on,
 index_merge_intersection=on,
 engine_condition_pushdown=on,
 index_condition_pushdown=on,
 mrr=on,mrr_cost_based=on,
 block_nested_loop=on,batched_key_access=off,
 materialization=on,semijoin=on,loosescan=on,
 firstmatch=on,duplicateweedout=on,
 subquery_materialization_cost_based=on,
 use_index_extensions=on,
 condition_fanout_filter=on,derived_merge=on,
 prefer_ordering_index=on
```

For more information about the syntax of this variable and the optimizer behaviors that it controls, see Section 8.9.2, "Switchable Optimizations".

<span id="page-0-0"></span>• [optimizer\\_trace](#page-0-0)

| Command-Line Format | optimizer-trace=value |
|---------------------|-----------------------|
| System Variable     | optimizer_trace       |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | String                |

This variable controls optimizer tracing. For details, see Section 8.15, "Tracing the Optimizer".

<span id="page-0-1"></span>• [optimizer\\_trace\\_features](#page-0-1)

| Command-Line Format | optimizer-trace-features=value |
|---------------------|--------------------------------|
| System Variable     | optimizer_trace_features       |
| Scope               | Global, Session                |
| Dynamic             | Yes                            |
| Type                | String                         |

This variable enables or disables selected optimizer tracing features. For details, see Section 8.15, "Tracing the Optimizer".

<span id="page-0-2"></span>• [optimizer\\_trace\\_limit](#page-0-2)

| Command-Line Format | optimizer-trace-limit=# |
|---------------------|-------------------------|
| System Variable     | optimizer_trace_limit   |
| Scope               | Global, Session         |
| Dynamic             | Yes                     |
| Type                | Integer                 |
| Default Value       | 1                       |
| Minimum Value       | 0                       |

| Maximum Value | 2147483647 |
|---------------|------------|
|---------------|------------|

The maximum number of optimizer traces to display. For details, see Section 8.15, "Tracing the Optimizer".

<span id="page-1-0"></span>• [optimizer\\_trace\\_max\\_mem\\_size](#page-1-0)

| Command-Line Format | optimizer-trace-max-mem-size=# |
|---------------------|--------------------------------|
| System Variable     | optimizer_trace_max_mem_size   |
| Scope               | Global, Session                |
| Dynamic             | Yes                            |
| Type                | Integer                        |
| Default Value       | 16384                          |
| Minimum Value       | 0                              |
| Maximum Value       | 4294967295                     |
| Unit                | bytes                          |

The maximum cumulative size of stored optimizer traces. For details, see Section 8.15, "Tracing the Optimizer".

<span id="page-1-1"></span>• [optimizer\\_trace\\_offset](#page-1-1)

| Command-Line Format | optimizer-trace-offset=# |
|---------------------|--------------------------|
| System Variable     | optimizer_trace_offset   |
| Scope               | Global, Session          |
| Dynamic             | Yes                      |
| Type                | Integer                  |
| Default Value       | -1                       |
| Minimum Value       | -2147483647              |
| Maximum Value       | 2147483647               |

The offset of optimizer traces to display. For details, see Section 8.15, "Tracing the Optimizer".

• performance\_schema\_xxx

Performance Schema system variables are listed in Section 25.15, "Performance Schema System Variables". These variables may be used to configure Performance Schema operation.

<span id="page-1-2"></span>• [parser\\_max\\_mem\\_size](#page-1-2)

| Command-Line Format              | parser-max-mem-size=# |
|----------------------------------|-----------------------|
| System Variable                  | parser_max_mem_size   |
| Scope                            | Global, Session       |
| Dynamic                          | Yes                   |
| Type                             | Integer               |
| Default Value (64-bit platforms) | 18446744073709551615  |
| Default Value (32-bit platforms) | 4294967295            |
| Minimum Value                    | 10000000              |
| Maximum Value (64-bit platforms) | 18446744073709551615  |
| Maximum Value (32-bit platforms) | 4294967295            |

| Unit | bytes |
|------|-------|
|------|-------|

The maximum amount of memory available to the parser. The default value places no limit on memory available. The value can be reduced to protect against out-of-memory situations caused by parsing long or complex SQL statements.

## <span id="page-2-0"></span>• [pid\\_file](#page-2-0)

| Command-Line Format | pid-file=file_name |
|---------------------|--------------------|
| System Variable     | pid_file           |
| Scope               | Global             |
| Dynamic             | No                 |
| Type                | File name          |

The path name of the file in which the server writes its process ID. The server creates the file in the data directory unless an absolute path name is given to specify a different directory. If you specify this variable, you must specify a value. If you do not specify this variable, MySQL uses a default value of host\_name.pid, where host\_name is the name of the host machine.

The process ID file is used by other programs such as mysqld\_safe to determine the server's process ID. On Windows, this variable also affects the default error log file name. See [Section 5.4.2,](#page-128-0) ["The Error Log"](#page-128-0).

### <span id="page-2-1"></span>• [plugin\\_dir](#page-2-1)

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| System Variable     | plugin_dir          |
| Scope               | Global              |
| Dynamic             | No                  |
| Type                | Directory name      |
| Default Value       | BASEDIR/lib/plugin  |

The path name of the plugin directory.

If the plugin directory is writable by the server, it may be possible for a user to write executable code to a file in the directory using SELECT ... INTO DUMPFILE. This can be prevented by making [plugin\\_dir](#page-2-1) read only to the server or by setting [secure\\_file\\_priv](#page-13-0) to a directory where SELECT writes can be made safely.

### <span id="page-2-2"></span>• [port](#page-2-2)

| Command-Line Format | port=port_num |
|---------------------|---------------|
| System Variable     | port          |
| Scope               | Global        |
| Dynamic             | No            |
| Type                | Integer       |
| Default Value       | 3306          |
| Minimum Value       | 0             |
| Maximum Value       | 65535         |

The number of the port on which the server listens for TCP/IP connections. This variable can be set with the --port option. 775

## <span id="page-3-0"></span>• [preload\\_buffer\\_size](#page-3-0)

| Command-Line Format | preload-buffer-size=# |
|---------------------|-----------------------|
| System Variable     | preload_buffer_size   |
| Scope               | Global, Session       |
| Dynamic             | Yes                   |
| Type                | Integer               |
| Default Value       | 32768                 |
| Minimum Value       | 1024                  |
| Maximum Value       | 1073741824            |
| Unit                | bytes                 |

The size of the buffer that is allocated when preloading indexes.

### <span id="page-3-1"></span>• [profiling](#page-3-1)

If set to 0 or OFF (the default), statement profiling is disabled. If set to 1 or ON, statement profiling is enabled and the SHOW PROFILE and SHOW PROFILES statements provide access to profiling information. See Section 13.7.5.31, "SHOW PROFILES Statement".

This variable is deprecated; expect it to be removed in a future release of MySQL.

### <span id="page-3-2"></span>• [profiling\\_history\\_size](#page-3-2)

The number of statements for which to maintain profiling information if [profiling](#page-3-1) is enabled. The default value is 15. The maximum value is 100. Setting the value to 0 effectively disables profiling. See Section 13.7.5.31, "SHOW PROFILES Statement".

This variable is deprecated; expect it to be removed in a future release of MySQL.

<span id="page-3-3"></span>• [protocol\\_version](#page-3-3)

| System Variable | protocol_version |
|-----------------|------------------|
| Scope           | Global           |
| Dynamic         | No               |
| Type            | Integer          |
| Default Value   | 10               |
| Minimum Value   | 0                |
| Maximum Value   | 4294967295       |

The version of the client/server protocol used by the MySQL server.

### <span id="page-3-4"></span>• [proxy\\_user](#page-3-4)

| System Variable | proxy_user |
|-----------------|------------|
| Scope           | Session    |
| Dynamic         | No         |
| Type            | String     |

If the current client is a proxy for another user, this variable is the proxy user account name. Otherwise, this variable is NULL. See Section 6.2.14, "Proxy Users".

<span id="page-4-0"></span>• [pseudo\\_slave\\_mode](#page-4-0)

| System Variable | pseudo_slave_mode |
|-----------------|-------------------|
| Scope           | Session           |
| Dynamic         | Yes               |
| Type            | Boolean           |

This system variable is for internal server use. [pseudo\\_slave\\_mode](#page-4-0) assists with the correct handling of transactions that originated on older or newer servers than the server currently processing them. mysqlbinlog sets the value of [pseudo\\_slave\\_mode](#page-4-0) to true before executing any SQL statements.

[pseudo\\_slave\\_mode](#page-4-0) has the following effects on the handling of prepared XA transactions, which can be attached to or detached from the handling session (by default, the session that issues XA START):

- If true, and the handling session has executed an internal-use BINLOG statement, XA transactions are automatically detached from the session as soon as the first part of the transaction up to XA PREPARE finishes, so they can be committed or rolled back by any session that has the [XA\\_RECOVER\\_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.md#priv_xa-recover-admin) privilege.
- If false, XA transactions remain attached to the handling session as long as that session is alive, during which time no other session can commit the transaction. The prepared transaction is only detached if the session disconnects or the server restarts.
- <span id="page-4-1"></span>• [pseudo\\_thread\\_id](#page-4-1)

| System Variable | pseudo_thread_id |
|-----------------|------------------|
| Scope           | Session          |
| Dynamic         | Yes              |
| Type            | Integer          |
| Default Value   | 2147483647       |
| Minimum Value   | 0                |
| Maximum Value   | 2147483647       |

This variable is for internal server use.

![](_page_4_Picture_10.jpeg)

### **Warning**

Changing the session value of the [pseudo\\_thread\\_id](#page-4-1) system variable changes the value returned by the CONNECTION\_ID() function.

<span id="page-4-2"></span>• [query\\_alloc\\_block\\_size](#page-4-2)

| Command-Line Format | query-alloc-block-size=# |
|---------------------|--------------------------|
| System Variable     | query_alloc_block_size   |
| Scope               | Global, Session          |
| Dynamic             | Yes                      |
| Type                | Integer                  |
| Default Value       | 8192                     |
| Minimum Value       | 1024                     |
| Maximum Value       | 4294966272               |

| Unit       | bytes |
|------------|-------|
| Block Size | 1024  |

The allocation size in bytes of memory blocks that are allocated for objects created during statement parsing and execution. If you have problems with memory fragmentation, it might help to increase this parameter.

The block size for the byte number is 1024. A value that is not an exact multiple of the block size is rounded down to the next lower multiple of the block size by MySQL Server before storing the value for the system variable. The parser allows values up to the maximum unsigned integer value for the platform (4294967295 or  $2^{32}$ –1 for a 32-bit system, 18446744073709551615 or  $2^{64}$ –1 for a 64-bit system) but the actual maximum is a block size lower.

<span id="page-5-0"></span>• query\_cache\_limit

| Command-Line Format              | query-cache-limit=#  |
|----------------------------------|----------------------|
| Deprecated                       | Yes                  |
| System Variable                  | query_cache_limit    |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Туре                             | Integer              |
| Default Value                    | 1048576              |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |
| Unit                             | bytes                |

Do not cache results that are larger than this number of bytes. The default value is 1MB.

![](_page_5_Picture_7.jpeg)

### Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation includes  $query\_cache\_limit$ .

<span id="page-5-1"></span>• query\_cache\_min\_res\_unit

| Command-Line Format              | query-cache-min-res-unit=# |
|----------------------------------|----------------------------|
| Deprecated                       | Yes                        |
| System Variable                  | query_cache_min_res_unit   |
| Scope                            | Global                     |
| Dynamic                          | Yes                        |
| Туре                             | Integer                    |
| Default Value                    | 4096                       |
| Minimum Value                    | 512                        |
| Maximum Value (64-bit platforms) | 18446744073709551615       |
| Maximum Value (32-bit platforms) | 4294967295                 |

| Unit | bytes |
|------|-------|
|------|-------|

The minimum size (in bytes) for blocks allocated by the query cache. The default value is 4096 (4KB). Tuning information for this variable is given in Section 8.10.3.3, "Query Cache Configuration".

![](_page_6_Picture_3.jpeg)

### **Note**

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation includes [query\\_cache\\_min\\_res\\_unit](#page-5-1).

<span id="page-6-0"></span>• [query\\_cache\\_size](#page-6-0)

| Command-Line Format              | query-cache-size=#   |
|----------------------------------|----------------------|
| Deprecated                       | Yes                  |
| System Variable                  | query_cache_size     |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 1048576              |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |
| Unit                             | bytes                |

The amount of memory allocated for caching query results. By default, the query cache is disabled. This is achieved using a default value of 1M, with a default for [query\\_cache\\_type](#page-6-1) of 0. (To reduce overhead significantly if you set the size to 0, you should also start the server with [query\\_cache\\_type=0](#page-6-1).

The permissible values are multiples of 1024; other values are rounded down to the nearest multiple. For nonzero values of [query\\_cache\\_size](#page-6-0), that many bytes of memory are allocated even if [query\\_cache\\_type=0](#page-6-1). See Section 8.10.3.3, "Query Cache Configuration", for more information.

The query cache needs a minimum size of about 40KB to allocate its structures. (The exact size depends on system architecture.) If you set the value of [query\\_cache\\_size](#page-6-0) too small, a warning occurs, as described in Section 8.10.3.3, "Query Cache Configuration".

![](_page_6_Picture_11.jpeg)

## **Note**

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation includes [query\\_cache\\_size](#page-6-0).

<span id="page-6-1"></span>• [query\\_cache\\_type](#page-6-1)

| Command-Line Format | query-cache-type=# |
|---------------------|--------------------|
| Deprecated          | Yes                |
| System Variable     | query_cache_type   |
| Scope               | Global, Session    |
| Dynamic             | Yes                |
| Type                | Enumeration        |
| Default Value       | 0                  |
| Valid Values        | 0                  |

|  | 1 |  |
|--|---|--|
|  | 2 |  |

Set the query cache type. Setting the GLOBAL value sets the type for all clients that connect thereafter. Individual clients can set the SESSION value to affect their own use of the query cache. Possible values are shown in the following table.

| Option      | Description                                                                                                                                                                             |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0 or OFF    | Do not cache results in or retrieve results<br>from the query cache. Note that this does not<br>deallocate the query cache buffer. To do that,<br>you should set query_cache_size to 0. |
| 1 or ON     | Cache all cacheable query results except for<br>those that begin with SELECT SQL_NO_CACHE.                                                                                              |
| 2 or DEMAND | Cache results only for cacheable queries that<br>begin with SELECT SQL_CACHE.                                                                                                           |

This variable defaults to OFF.

If the server is started with query\_cache\_type set to 0, it does not acquire the query cache mutex at all, which means that the query cache cannot be enabled at runtime and there is reduced overhead in query execution.

![](_page_7_Picture_6.jpeg)

### **Note**

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation includes [query\\_cache\\_type](#page-6-1).

<span id="page-7-0"></span>• [query\\_cache\\_wlock\\_invalidate](#page-7-0)

| Command-Line Format | query-cache-wlock<br>invalidate[={OFF ON}] |
|---------------------|--------------------------------------------|
| Deprecated          | Yes                                        |
| System Variable     | query_cache_wlock_invalidate               |
| Scope               | Global, Session                            |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | OFF                                        |

Normally, when one client acquires a WRITE lock on a table, other clients are not blocked from issuing statements that read from the table if the query results are present in the query cache. Setting this variable to 1 causes acquisition of a WRITE lock for a table to invalidate any queries in the query cache that refer to the table. This forces other clients that attempt to access the table to wait while the lock is in effect.

![](_page_7_Picture_12.jpeg)

## **Note**

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation includes [query\\_cache\\_wlock\\_invalidate](#page-7-0).

<span id="page-7-1"></span>• [query\\_prealloc\\_size](#page-7-1)

| Command-Line Format | query-prealloc-size=# |
|---------------------|-----------------------|
|                     |                       |

| System Variable                  | query_prealloc_size  |
|----------------------------------|----------------------|
| Scope                            | Global, Session      |
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 8192                 |
| Minimum Value                    | 8192                 |
| Maximum Value (64-bit platforms) | 18446744073709550592 |
| Maximum Value (32-bit platforms) | 4294966272           |
| Unit                             | bytes                |
| Block Size                       | 1024                 |

The size in bytes of the persistent buffer used for statement parsing and execution. This buffer is not freed between statements. If you are running complex queries, a larger [query\\_prealloc\\_size](#page-7-1) value might be helpful in improving performance, because it can reduce the need for the server to perform memory allocation during query execution operations. You should be aware that doing this does not necessarily eliminate allocation completely; the server may still allocate memory in some situations, such as for operations relating to transactions, or to stored programs.

### <span id="page-8-0"></span>• [rand\\_seed1](#page-8-0)

| System Variable | rand_seed1 |
|-----------------|------------|
| Scope           | Session    |
| Dynamic         | Yes        |
| Type            | Integer    |
| Default Value   | N/A        |
| Minimum Value   | 0          |
| Maximum Value   | 4294967295 |

The [rand\\_seed1](#page-8-0) and [rand\\_seed2](#page-8-1) variables exist as session variables only, and can be set but not read. The variables—but not their values—are shown in the output of SHOW VARIABLES.

The purpose of these variables is to support replication of the RAND() function. For statements that invoke RAND(), the source passes two values to the replica, where they are used to seed the random number generator. The replica uses these values to set the session variables [rand\\_seed1](#page-8-0) and [rand\\_seed2](#page-8-1) so that RAND() on the replica generates the same value as on the source.

<span id="page-8-1"></span>• [rand\\_seed2](#page-8-1)

See the description for [rand\\_seed1](#page-8-0).

<span id="page-8-2"></span>• [range\\_alloc\\_block\\_size](#page-8-2)

| Command-Line Format              | range-alloc-block-size=# |
|----------------------------------|--------------------------|
| System Variable                  | range_alloc_block_size   |
| Scope                            | Global, Session          |
| Dynamic                          | Yes                      |
| Type                             | Integer                  |
| Default Value                    | 4096                     |
| Minimum Value                    | 4096                     |
| Maximum Value (64-bit platforms) | 18446744073709550592     |

| Maximum Value | 4294966272 |
|---------------|------------|
| Unit          | bytes      |
| Block Size    | 1024       |

The size in bytes of blocks that are allocated when doing range optimization.

The block size for the byte number is 1024. A value that is not an exact multiple of the block size is rounded down to the next lower multiple of the block size by MySQL Server before storing the value for the system variable. The parser allows values up to the maximum unsigned integer value for the platform (4294967295 or 2<sup>32</sup>-1 for a 32-bit system, 18446744073709551615 or 2<sup>64</sup>-1 for a 64-bit system) but the actual maximum is a block size lower.

#### <span id="page-9-0"></span>• range optimizer max mem size

| Command-Line Format | range-optimizer-max-mem-size=# |
|---------------------|--------------------------------|
| System Variable     | range_optimizer_max_mem_size   |
| Scope               | Global, Session                |
| Dynamic             | Yes                            |
| Туре                | Integer                        |
| Default Value       | 8388608                        |
| Minimum Value       | 0                              |
| Maximum Value       | 18446744073709551615           |
| Unit                | bytes                          |

The limit on memory consumption for the range optimizer. A value of 0 means "no limit." If an execution plan considered by the optimizer uses the range access method but the optimizer estimates that the amount of memory needed for this method would exceed the limit, it abandons the plan and considers other plans. For more information, see Limiting Memory Use for Range Optimization.

### <span id="page-9-1"></span>• rbr exec mode

| System Variable | rbr_exec_mode |
|-----------------|---------------|
| Scope           | Session       |
| Dynamic         | Yes           |
| Туре            | Enumeration   |
| Default Value   | STRICT        |
| Valid Values    | STRICT        |
|                 | IDEMPOTENT    |

For internal use by <code>mysqlbinlog</code>. This variable switches the server between <code>IDEMPOTENT</code> mode and <code>STRICT</code> mode. <code>IDEMPOTENT</code> mode causes suppression of duplicate-key and no-key-found errors in <code>BINLOG</code> statements generated by <code>mysqlbinlog</code>. This mode is useful when replaying a row-based binary log on a server that causes conflicts with existing data. <code>mysqlbinlog</code> sets this mode when you specify the <code>--idempotent</code> option by writing the following to the output:

SET SESSION RBR\_EXEC\_MODE=IDEMPOTENT;

### <span id="page-9-2"></span>• read buffer size

| Command-Line Format | read-buffer-size=# |
|---------------------|--------------------|
| System Variable     | read_buffer_size   |

| Scope         | Global, Session |
|---------------|-----------------|
| Dynamic       | Yes             |
| Type          | Integer         |
| Default Value | 131072          |
| Minimum Value | 8192            |
| Maximum Value | 2147479552      |
| Unit          | bytes           |
| Block Size    | 4096            |

Each thread that does a sequential scan for a MyISAM table allocates a buffer of this size (in bytes) for each table it scans. If you do many sequential scans, you might want to increase this value, which defaults to 131072. The value of this variable should be a multiple of 4KB. If it is set to a value that is not a multiple of 4KB, its value is rounded down to the nearest multiple of 4KB.

This option is also used in the following context for all storage engines:

- For caching the indexes in a temporary file (not a temporary table), when sorting rows for ORDER BY.
- For bulk insert into partitions.
- For caching results of nested queries.

[read\\_buffer\\_size](#page-9-2) is also used in one other storage engine-specific way: to determine the memory block size for MEMORY tables.

For more information about memory use during different operations, see Section 8.12.4.1, "How MySQL Uses Memory".

<span id="page-10-0"></span>• [read\\_only](#page-10-0)

| Command-Line Format | read-only[={OFF ON}] |
|---------------------|----------------------|
| System Variable     | read_only            |
| Scope               | Global               |
| Dynamic             | Yes                  |
| Type                | Boolean              |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

If the [read\\_only](#page-10-0) system variable is enabled, the server permits no client updates except from users who have the SUPER privilege. This variable is disabled by default.

The server also supports a [super\\_read\\_only](#page-34-0) system variable (disabled by default), which has these effects:

- If [super\\_read\\_only](#page-34-0) is enabled, the server prohibits client updates, even from users who have the SUPER privilege.
- Setting [super\\_read\\_only](#page-34-0) to ON implicitly forces [read\\_only](#page-10-0) to ON.
- Setting [read\\_only](#page-10-0) to OFF implicitly forces [super\\_read\\_only](#page-34-0) to OFF.

Even with [read\\_only](#page-10-0) enabled, the server permits these operations:

- Updates performed by replication threads, if the server is a replica. In replication setups, it can be useful to enable [read\\_only](#page-10-0) on replica servers to ensure that replicas accept updates only from the source server and not from clients.
- Use of ANALYZE TABLE or OPTIMIZE TABLE statements. The purpose of read-only mode is to prevent changes to table structure or contents. Analysis and optimization do not qualify as such changes. This means, for example, that consistency checks on read-only replicas can be performed with mysqlcheck --all-databases --analyze.
- Use of FLUSH STATUS statements, which are always written to the binary log.
- Operations on TEMPORARY tables.
- Inserts into the log tables (mysql.general\_log and mysql.slow\_log); see [Section 5.4.1,](#page-126-0) ["Selecting General Query Log and Slow Query Log Output Destinations".](#page-126-0)
- As of MySQL 5.7.16, updates to Performance Schema tables, such as UPDATE or TRUNCATE TABLE operations.

Changes to [read\\_only](#page-10-0) on a replication source server are not replicated to replica servers. The value can be set on a replica independent of the setting on the source.

The following conditions apply to attempts to enable [read\\_only](#page-10-0) (including implicit attempts resulting from enabling [super\\_read\\_only](#page-34-0)):

- The attempt fails and an error occurs if you have any explicit locks (acquired with LOCK TABLES) or have a pending transaction.
- The attempt blocks while other clients have any ongoing statement, active LOCK TABLES WRITE, or ongoing commit, until the locks are released and the statements and transactions end. While the attempt to enable [read\\_only](#page-10-0) is pending, requests by other clients for table locks or to begin transactions also block until [read\\_only](#page-10-0) has been set.
- The attempt blocks if there are active transactions that hold metadata locks, until those transactions end.
- [read\\_only](#page-10-0) can be enabled while you hold a global read lock (acquired with FLUSH TABLES WITH READ LOCK) because that does not involve table locks.
- <span id="page-11-0"></span>• [read\\_rnd\\_buffer\\_size](#page-11-0)

| Command-Line Format | read-rnd-buffer-size=# |
|---------------------|------------------------|
| System Variable     | read_rnd_buffer_size   |

| Scope         | Global, Session |
|---------------|-----------------|
| Dynamic       | Yes             |
| Type          | Integer         |
| Default Value | 262144          |
| Minimum Value | 1               |
| Maximum Value | 2147483647      |
| Unit          | bytes           |

This variable is used for reads from MyISAM tables, and, for any storage engine, for Multi-Range Read optimization.

When reading rows from a MyISAM table in sorted order following a key-sorting operation, the rows are read through this buffer to avoid disk seeks. See Section 8.2.1.14, "ORDER BY Optimization". Setting the variable to a large value can improve ORDER BY performance by a lot. However, this is a buffer allocated for each client, so you should not set the global variable to a large value. Instead, change the session variable only from within those clients that need to run large queries.

For more information about memory use during different operations, see Section 8.12.4.1, "How MySQL Uses Memory". For information about Multi-Range Read optimization, see Section 8.2.1.10, "Multi-Range Read Optimization".

### <span id="page-12-0"></span>• [require\\_secure\\_transport](#page-12-0)

| Command-Line Format | require-secure-transport[={OFF <br>ON}] |
|---------------------|-----------------------------------------|
| System Variable     | require_secure_transport                |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | Boolean                                 |
| Default Value       | OFF                                     |

Whether client connections to the server are required to use some form of secure transport. When this variable is enabled, the server permits only TCP/IP connections encrypted using TLS/SSL, or connections that use a socket file (on Unix) or shared memory (on Windows). The server rejects nonsecure connection attempts, which fail with an [ER\\_SECURE\\_TRANSPORT\\_REQUIRED](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_secure_transport_required) error.

This capability supplements per-account SSL requirements, which take precedence. For example, if an account is defined with REQUIRE SSL, enabling [require\\_secure\\_transport](#page-12-0) does not make it possible to use the account to connect using a Unix socket file.

It is possible for a server to have no secure transports available. For example, a server on Windows supports no secure transports if started without specifying any SSL certificate or key files and with the [shared\\_memory](#page-19-0) system variable disabled. Under these conditions, attempts to enable [require\\_secure\\_transport](#page-12-0) at startup cause the server to write a message to the error log and exit. Attempts to enable the variable at runtime fail with an [ER\\_NO\\_SECURE\\_TRANSPORTS\\_CONFIGURED](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_no_secure_transports_configured) error.

See also Configuring Encrypted Connections as Mandatory.

### <span id="page-12-1"></span>• [secure\\_auth](#page-12-1)

| Command-Line Format | secure-auth[={OFF ON}] |
|---------------------|------------------------|
| Deprecated          | Yes                    |
| System Variable     | secure_auth            |

| Scope         | Global  |
|---------------|---------|
| Dynamic       | Yes     |
| Type          | Boolean |
| Default Value | ON      |
| Valid Values  | ON      |

If this variable is enabled, the server blocks connections by clients that attempt to use accounts that have passwords stored in the old (pre-4.1) format. Enable this variable to prevent all use of passwords employing the old format (and hence insecure communication over the network).

This variable is deprecated; expect it to be removed in a future release of MySQL. It is always enabled and attempting to disable it produces an error.

Server startup fails with an error if this variable is enabled and the privilege tables are in pre-4.1 format. See Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".

![](_page_13_Picture_5.jpeg)

### **Note**

Passwords that use the pre-4.1 hashing method are less secure than passwords that use the native password hashing method and should be avoided. Pre-4.1 passwords are deprecated and support for them is removed in MySQL 5.7.5. For account upgrade instructions, see Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".

<span id="page-13-0"></span>• [secure\\_file\\_priv](#page-13-0)

| Command-Line Format | secure-file-priv=dir_name |
|---------------------|---------------------------|
| System Variable     | secure_file_priv          |
| Scope               | Global                    |
| Dynamic             | No                        |
| Type                | String                    |
| Default Value       | platform specific         |
| Valid Values        | empty string              |
|                     | dirname                   |
|                     | NULL                      |

This variable is used to limit the effect of data import and export operations, such as those performed by the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD\_FILE() function. These operations are permitted only to users who have the FILE privilege.

[secure\\_file\\_priv](#page-13-0) may be set as follows:

- If empty, the variable has no effect. This is not a secure setting.
- If set to the name of a directory, the server limits import and export operations to work only with files in that directory. The directory must exist; the server does not create it.

• If set to NULL, the server disables import and export operations.

The default value is platform specific and depends on the value of the INSTALL\_LAYOUT CMake option, as shown in the following table. To specify the default [secure\\_file\\_priv](#page-13-0) value explicitly if you are building from source, use the INSTALL\_SECURE\_FILE\_PRIVDIR CMake option.

| INSTALL_LAYOUT Value | Default secure_file_priv Value                      |
|----------------------|-----------------------------------------------------|
| STANDALONE, WIN      | NULL (>= MySQL 5.7.16), empty (< MySQL<br>5.7.16)   |
| DEB, RPM, SLES, SVR4 | /var/lib/mysql-files                                |
| Otherwise            | mysql-files under the<br>CMAKE_INSTALL_PREFIX value |

To set the default [secure\\_file\\_priv](#page-13-0) value for the libmysqld embedded server, use the INSTALL\_SECURE\_FILE\_PRIV\_EMBEDDEDDIR CMake option. The default value for this option is NULL.

The server checks the value of [secure\\_file\\_priv](#page-13-0) at startup and writes a warning to the error log if the value is insecure. A non-NULL value is considered insecure if it is empty, or the value is the data directory or a subdirectory of it, or a directory that is accessible by all users. If [secure\\_file\\_priv](#page-13-0) is set to a nonexistent path, the server writes an error message to the error log and exits.

<span id="page-14-0"></span>• [session\\_track\\_gtids](#page-14-0)

| Command-Line Format | session-track-gtids=value |
|---------------------|---------------------------|
| System Variable     | session_track_gtids       |
| Scope               | Global, Session           |
| Dynamic             | Yes                       |
| Type                | Enumeration               |
| Default Value       | OFF                       |
| Valid Values        | OFF                       |
|                     | OWN_GTID                  |
|                     | ALL_GTIDS                 |

Controls whether the server returns GTIDs to the client, enabling the client to use them to track the server state. Depending on the variable value, at the end of executing each transaction, the server's GTIDs are captured and returned to the client as part of the acknowledgement. The possible values for [session\\_track\\_gtids](#page-14-0) are as follows:

- OFF: The server does not return GTIDs to the client. This is the default.
- OWN\_GTID: The server returns the GTIDs for all transactions that were successfully committed by this client in its current session since the last acknowledgement. Typically, this is the single GTID for the last transaction committed, but if a single client request resulted in multiple transactions, the server returns a GTID set containing all the relevant GTIDs.
- ALL\_GTIDS: The server returns the global value of its gtid\_executed system variable, which it reads at a point after the transaction is successfully committed. As well as the GTID for the transaction just committed, this GTID set includes all transactions committed on the server by any

client, and can include transactions committed after the point when the transaction currently being acknowledged was committed.

[session\\_track\\_gtids](#page-14-0) cannot be set within transactional context.

For more information about session state tracking, see [Section 5.1.15, "Server Tracking of Client](#page-117-0) [Session State"](#page-117-0).

<span id="page-15-0"></span>• [session\\_track\\_schema](#page-15-0)

| Command-Line Format | session-track-schema[={OFF ON}] |
|---------------------|---------------------------------|
| System Variable     | session_track_schema            |
| Scope               | Global, Session                 |
| Dynamic             | Yes                             |
| Type                | Boolean                         |
| Default Value       | ON                              |

Controls whether the server tracks when the default schema (database) is set within the current session and notifies the client to make the schema name available.

If the schema name tracker is enabled, name notification occurs each time the default schema is set, even if the new schema name is the same as the old.

For more information about session state tracking, see [Section 5.1.15, "Server Tracking of Client](#page-117-0) [Session State"](#page-117-0).

<span id="page-15-1"></span>• [session\\_track\\_state\\_change](#page-15-1)

| Command-Line Format | session-track-state-change[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | session_track_state_change                |
| Scope               | Global, Session                           |
| Dynamic             | Yes                                       |
| Type                | Boolean                                   |
| Default Value       | OFF                                       |

Controls whether the server tracks changes to the state of the current session and notifies the client when state changes occur. Changes can be reported for these attributes of client session state:

- The default schema (database).
- Session-specific values for system variables.
- User-defined variables.
- Temporary tables.
- Prepared statements.

If the session state tracker is enabled, notification occurs for each change that involves tracked session attributes, even if the new attribute values are the same as the old. For example, setting a user-defined variable to its current value results in a notification.

The [session\\_track\\_state\\_change](#page-15-1) variable controls only notification of when changes occur, not what the changes are. For example, state-change notifications occur when the default schema is set or tracked session system variables are assigned, but the notification does not include the <sup>788</sup>

schema name or variable values. To receive notification of the schema name or session system variable values, use the [session\\_track\\_schema](#page-15-0) or [session\\_track\\_system\\_variables](#page-16-0) system variable, respectively.

![](_page_16_Picture_2.jpeg)

### **Note**

Assigning a value to [session\\_track\\_state\\_change](#page-15-1) itself is not considered a state change and is not reported as such. However, if its name listed in the value of [session\\_track\\_system\\_variables](#page-16-0), any assignments to it do result in notification of the new value.

For more information about session state tracking, see [Section 5.1.15, "Server Tracking of Client](#page-117-0) [Session State"](#page-117-0).

<span id="page-16-0"></span>• [session\\_track\\_system\\_variables](#page-16-0)

| Command-Line Format | session-track-system-variables=#                                                                      |
|---------------------|-------------------------------------------------------------------------------------------------------|
| System Variable     | session_track_system_variables                                                                        |
| Scope               | Global, Session                                                                                       |
| Dynamic             | Yes                                                                                                   |
| Type                | String                                                                                                |
| Default Value       | time_zone, autocommit,<br>character_set_client,<br>character_set_results,<br>character_set_connection |

Controls whether the server tracks assignments to session system variables and notifies the client of the name and value of each assigned variable. The variable value is a commaseparated list of variables for which to track assignments. By default, notification is enabled for [time\\_zone](#page-41-0), autocommit, character\_set\_client, character\_set\_results, and character\_set\_connection. (The latter three variables are those affected by SET NAMES.)

The special value \* causes the server to track assignments to all session variables. If given, this value must be specified by itself without specific system variable names.

To disable notification of session variable assignments, set [session\\_track\\_system\\_variables](#page-16-0) to the empty string.

If session system variable tracking is enabled, notification occurs for all assignments to tracked session variables, even if the new values are the same as the old.

For more information about session state tracking, see [Section 5.1.15, "Server Tracking of Client](#page-117-0) [Session State"](#page-117-0).

<span id="page-16-1"></span>• [session\\_track\\_transaction\\_info](#page-16-1)

| Command-Line Format | session-track-transaction<br>info=value |
|---------------------|-----------------------------------------|
| System Variable     | session_track_transaction_info          |
| Scope               | Global, Session                         |
| Dynamic             | Yes                                     |
| Type                | Enumeration                             |
| Default Value       | OFF                                     |
| Valid Values        | OFF                                     |

![](_page_17_Figure_1.jpeg)

Controls whether the server tracks the state and characteristics of transactions within the current session and notifies the client to make this information available. These [session\\_track\\_transaction\\_info](#page-16-1) values are permitted:

- OFF: Disable transaction state tracking. This is the default.
- STATE: Enable transaction state tracking without characteristics tracking. State tracking enables the client to determine whether a transaction is in progress and whether it could be moved to a different session without being rolled back.
- CHARACTERISTICS: Enable transaction state tracking, including characteristics tracking. Characteristics tracking enables the client to determine how to restart a transaction in another session so that it has the same characteristics as in the original session. The following characteristics are relevant for this purpose:

```
ISOLATION LEVEL
READ ONLY
READ WRITE
WITH CONSISTENT SNAPSHOT
```

For a client to safely relocate a transaction to another session, it must track not only transaction state but also transaction characteristics. In addition, the client must track the [transaction\\_isolation](#page-43-0) and [transaction\\_read\\_only](#page-46-0) system variables to correctly determine the session defaults. (To track these variables, list them in the value of the [session\\_track\\_system\\_variables](#page-16-0) system variable.)

For more information about session state tracking, see [Section 5.1.15, "Server Tracking of Client](#page-117-0) [Session State"](#page-117-0).

<span id="page-17-0"></span>• [sha256\\_password\\_auto\\_generate\\_rsa\\_keys](#page-17-0)

| Command-Line Format | sha256-password-auto-generate-rsa<br>keys[={OFF ON}] |
|---------------------|------------------------------------------------------|
| System Variable     | sha256_password_auto_generate_rsa_keys               |
| Scope               | Global                                               |
| Dynamic             | No                                                   |
| Type                | Boolean                                              |
| Default Value       | ON                                                   |

This variable is available if the server was compiled using OpenSSL (see Section 6.3.4, "SSL Library-Dependent Capabilities"). It controls whether the server autogenerates RSA private/public key-pair files in the data directory, if they do not already exist.

At startup, the server automatically generates RSA private/public key-pair files in the data directory if the [sha256\\_password\\_auto\\_generate\\_rsa\\_keys](#page-17-0) system variable is enabled, no RSA options are specified, and the RSA files are missing from the data directory. These files enable secure password exchange using RSA over unencrypted connections for accounts authenticated by the sha256\_password plugin; see Section 6.4.1.5, "SHA-256 Pluggable Authentication".

For more information about RSA file autogeneration, including file names and characteristics, see Section 6.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"

The auto\_generate\_certs system variable is related but controls autogeneration of SSL certificate and key files needed for secure connections using SSL.

<span id="page-18-0"></span>• [sha256\\_password\\_private\\_key\\_path](#page-18-0)

| Command-Line Format | sha256-password-private-key<br>path=file_name |
|---------------------|-----------------------------------------------|
| System Variable     | sha256_password_private_key_path              |
| Scope               | Global                                        |
| Dynamic             | No                                            |
| Type                | File name                                     |
| Default Value       | private_key.pem                               |

This variable is available if MySQL was compiled using OpenSSL (see Section 6.3.4, "SSL Library-Dependent Capabilities"). Its value is the path name of the RSA private key file for the sha256\_password authentication plugin. If the file is named as a relative path, it is interpreted relative to the server data directory. The file must be in PEM format.

![](_page_18_Picture_4.jpeg)

### **Important**

Because this file stores a private key, its access mode should be restricted so that only the MySQL server can read it.

For information about sha256\_password, see Section 6.4.1.5, "SHA-256 Pluggable Authentication".

<span id="page-18-1"></span>• [sha256\\_password\\_proxy\\_users](#page-18-1)

| Command-Line Format | sha256-password-proxy-users[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | sha256_password_proxy_users                |
| Scope               | Global                                     |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | OFF                                        |

This variable controls whether the sha256\_password built-in authentication plugin supports proxy users. It has no effect unless the check\_proxy\_users system variable is enabled. For information about user proxying, see Section 6.2.14, "Proxy Users".

<span id="page-18-2"></span>• [sha256\\_password\\_public\\_key\\_path](#page-18-2)

| Command-Line Format | sha256-password-public-key<br>path=file_name |
|---------------------|----------------------------------------------|
| System Variable     | sha256_password_public_key_path              |
| Scope               | Global                                       |
| Dynamic             | No                                           |
| Type                | File name                                    |
| Default Value       | public_key.pem                               |

This variable is available if MySQL was compiled using OpenSSL (see Section 6.3.4, "SSL Library-Dependent Capabilities"). Its value is the path name of the RSA public key file for the sha256\_password authentication plugin. If the file is named as a relative path, it is interpreted relative to the server data directory. The file must be in PEM format. Because this file stores a public key, copies can be freely distributed to client users. (Clients that explicitly specify a public key when 791 connecting to the server using RSA password encryption must use the same public key as that used by the server.)

For information about sha256\_password, including information about how clients specify the RSA public key, see Section 6.4.1.5, "SHA-256 Pluggable Authentication".

<span id="page-19-0"></span>• [shared\\_memory](#page-19-0)

| Command-Line Format | shared-memory[={OFF ON}] |
|---------------------|--------------------------|
| System Variable     | shared_memory            |
| Scope               | Global                   |
| Dynamic             | No                       |
| Platform Specific   | Windows                  |
| Type                | Boolean                  |
| Default Value       | OFF                      |

(Windows only.) Whether the server permits shared-memory connections.

<span id="page-19-1"></span>• [shared\\_memory\\_base\\_name](#page-19-1)

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| System Variable     | shared_memory_base_name      |
| Scope               | Global                       |
| Dynamic             | No                           |
| Platform Specific   | Windows                      |
| Type                | String                       |
| Default Value       | MYSQL                        |

(Windows only.) The name of shared memory to use for shared-memory connections. This is useful when running multiple MySQL instances on a single physical machine. The default name is MYSQL. The name is case-sensitive.

This variable applies only if the server is started with the [shared\\_memory](#page-19-0) system variable enabled to support shared-memory connections.

<span id="page-19-2"></span>• [show\\_compatibility\\_56](#page-19-2)

| Command-Line Format | show-compatibility-56[={OFF ON}] |
|---------------------|----------------------------------|
| Deprecated          | Yes                              |
| System Variable     | show_compatibility_56            |
| Scope               | Global                           |
| Dynamic             | Yes                              |
| Type                | Boolean                          |
| Default Value       | OFF                              |

The INFORMATION\_SCHEMA has tables that contain system and status variable information (see Section 24.3.11, "The INFORMATION\_SCHEMA GLOBAL\_VARIABLES and SESSION\_VARIABLES Tables", and Section 24.3.10, "The INFORMATION\_SCHEMA GLOBAL\_STATUS and SESSION\_STATUS Tables"). As of MySQL 5.7.6, the Performance Schema also contains system and status variable tables (see Section 25.12.13, "Performance Schema System Variable Tables", and Section 25.12.14, "Performance Schema Status Variable Tables").

The Performance Schema tables are intended to replace the INFORMATION\_SCHEMA tables, which are deprecated as of MySQL 5.7.6 and are removed in MySQL 8.0.

For advice on migrating away from the INFORMATION\_SCHEMA tables to the Performance Schema tables, see Section 25.20, "Migrating to Performance Schema System and Status Variable Tables". To assist in the migration, you can use the [show\\_compatibility\\_56](#page-19-2) system variable, which affects whether MySQL 5.6 compatibility is enabled with respect to how system and status variable information is provided by the INFORMATION\_SCHEMA and Performance Schema tables, and also by the SHOW VARIABLES and SHOW STATUS statements.

![](_page_20_Picture_3.jpeg)

### **Note**

[show\\_compatibility\\_56](#page-19-2) is deprecated because its only purpose is to permit control over deprecated system and status variable information sources which you can expect to be removed in a future release of MySQL. When those sources are removed, [show\\_compatibility\\_56](#page-19-2) no longer has any purpose, and you can expect it be removed as well.

The following discussion describes the effects of [show\\_compatibility\\_56](#page-19-2):

- [Overview of show\\_compatibility\\_56 Effects](#page-20-0)
- [Effect of show\\_compatibility\\_56 on SHOW Statements](#page-21-0)
- [Effect of show\\_compatibility\\_56 on INFORMATION\\_SCHEMA Tables](#page-22-0)
- [Effect of show\\_compatibility\\_56 on Performance Schema Tables](#page-22-1)
- [Effect of show\\_compatibility\\_56 on Slave Status Variables](#page-23-0)
- [Effect of show\\_compatibility\\_56 on FLUSH STATUS](#page-23-1)

For better understanding, it is strongly recommended that you also read these sections:

- Section 25.12.13, "Performance Schema System Variable Tables"
- Section 25.12.14, "Performance Schema Status Variable Tables"
- Section 25.12.15.10, "Status Variable Summary Tables"

## <span id="page-20-0"></span>**Overview of show\_compatibility\_56 Effects**

The [show\\_compatibility\\_56](#page-19-2) system variable affects these aspects of server operation regarding system and status variables:

- Information available from the SHOW VARIABLES and SHOW STATUS statements
- Information available from the INFORMATION\_SCHEMA tables that provide system and status variable information
- Information available from the Performance Schema tables that provide system and status variable information
- The effect of the FLUSH STATUS statement on status variables

This list summarizes the effects of [show\\_compatibility\\_56](#page-19-2), with additional details given later:

• When [show\\_compatibility\\_56](#page-19-2) is ON, compatibility with MySQL 5.6 is enabled. Older variable information sources (SHOW statements, INFORMATION\_SCHEMA tables) produce the same output as in MySQL 5.6.

• When [show\\_compatibility\\_56](#page-19-2) is OFF, compatibility with MySQL 5.6 is disabled. Selecting from the INFORMATION\_SCHEMA tables produces an error because the Performance Schema tables are intended to replace them. The INFORMATION\_SCHEMA tables are deprecated as of MySQL 5.7.6 and are removed in MySQL 8.0.

To obtain system and status variable information When [show\\_compatibility\\_56=OFF](#page-19-2), use the Performance Schema tables or the SHOW statements.

![](_page_21_Picture_3.jpeg)

### **Note**

When [show\\_compatibility\\_56=OFF](#page-19-2), the SHOW VARIABLES and SHOW STATUS statements display rows from the Performance Schema global\_variables, session\_variables, global\_status, and session\_status tables.

As of MySQL 5.7.9, those tables are world readable and accessible without the SELECT privilege, which means that SELECT is not needed to use the SHOW statements, either. Before MySQL 5.7.9, the SELECT privilege is required to access those Performance Schema tables, either directly, or indirectly through the SHOW statements.

- Several Slave\_xxx status variables are available from SHOW STATUS when [show\\_compatibility\\_56](#page-19-2) is ON. When [show\\_compatibility\\_56](#page-19-2) is OFF, some of those variables are not exposed to SHOW STATUS. The information they provide is available in replication-related Performance Schema tables, as described later.
- [show\\_compatibility\\_56](#page-19-2) has no effect on system variable access using @@ notation: @@GLOBAL.var\_name, @@SESSION.var\_name, @@var\_name.
- [show\\_compatibility\\_56](#page-19-2) has no effect for the embedded server, which produces 5.6 compatible output in all cases.

The following descriptions detail the effect of setting [show\\_compatibility\\_56](#page-19-2) to ON or OFF in the contexts in which this variable applies.

## <span id="page-21-0"></span>**Effect of show\_compatibility\_56 on SHOW Statements**

SHOW GLOBAL VARIABLES statement:

- ON: MySQL 5.6 output.
- OFF: Output displays rows from the Performance Schema global\_variables table.

SHOW [SESSION | LOCAL] VARIABLES statement:

- ON: MySQL 5.6 output.
- OFF: Output displays rows from the Performance Schema session\_variables table. (In MySQL 5.7.6 and 5.7.7, OFF output does not fully reflect all system variable values in effect for the current session; it includes no rows for global variables that have no session counterpart. This is corrected in MySQL 5.7.8.)

SHOW GLOBAL STATUS statement:

• ON: MySQL 5.6 output.

• OFF: Output displays rows from the Performance Schema global\_status table, plus the Com\_xxx statement execution counters.

OFF output includes no rows for session variables that have no global counterpart, unlike ON output.

SHOW [SESSION | LOCAL] STATUS statement:

- ON: MySQL 5.6 output.
- OFF: Output displays rows from the Performance Schema session\_status table, plus the Com\_xxx statement execution counters. (In MySQL 5.7.6 and 5.7.7, OFF output does not fully reflect all status variable values in effect for the current session; it includes no rows for global variables that have no session counterpart. This is corrected in MySQL 5.7.8.)

In MySQL 5.7.6 and 5.7.7, for each of the SHOW statements just described, use of a WHERE clause produces a warning when show\_compatibility\_56=ON and an error when show\_compatibility\_56=OFF. (This applies to WHERE clauses that are not optimized away. For example, WHERE 1 is trivially true, is optimized away, and thus produces no warning or error.) This behavior does not occur as of MySQL 5.7.8; WHERE is supported as before 5.7.6.

## <span id="page-22-0"></span>**Effect of show\_compatibility\_56 on INFORMATION\_SCHEMA Tables**

INFORMATION\_SCHEMA tables (GLOBAL\_VARIABLES, SESSION\_VARIABLES, GLOBAL\_STATUS, and SESSION\_STATUS):

- ON: MySQL 5.6 output, with a deprecation warning.
- OFF: Selecting from these tables produces an error. (Before 5.7.9, selecting from these tables produces no output, with a deprecation warning.)

## <span id="page-22-1"></span>**Effect of show\_compatibility\_56 on Performance Schema Tables**

Performance Schema system variable tables:

- OFF:
  - global\_variables: Global system variables only.
  - session\_variables: System variables in effect for the current session: A row for each session variable, and a row for each global variable that has no session counterpart.
  - variables\_by\_thread: Session system variables only, for each active session.

• ON: Same output as for OFF. (Before 5.7.8, these tables produce no output.)

Performance Schema status variable tables:

- OFF:
  - global\_status: Global status variables only.
  - session\_status: Status variables in effect the current session: A row for each session variable, and a row for each global variable that has no session counterpart.
  - status\_by\_account Session status variables only, aggregated per account.
  - status\_by\_host: Session status variables only, aggregated per host name.
  - status\_by\_thread: Session status variables only, for each active session.
  - status\_by\_user: Session status variables only, aggregated per user name.

The Performance Schema does not collect statistics for Com\_xxx status variables in the status variable tables. To obtain global and per-session statement execution counts, use the events\_statements\_summary\_global\_by\_event\_name and events\_statements\_summary\_by\_thread\_by\_event\_name tables, respectively.

• ON: Same output as for OFF. (Before 5.7.9, these tables produce no output.)

## <span id="page-23-0"></span>**Effect of show\_compatibility\_56 on Slave Status Variables**

Replica status variables:

- ON: Several Slave\_xxx status variables are available from SHOW STATUS.
- OFF: Some of those replica variables are not exposed to SHOW STATUS or the Performance Schema status variable tables. The information they provide is available in replication-related Performance Schema tables. The following table shows which Slave\_xxx status variables become unavailable in SHOW STATUS and their locations in Performance Schema replication tables.

| Status Variable            | Performance Schema Location                                                                     |
|----------------------------|-------------------------------------------------------------------------------------------------|
| Slave_heartbeat_period     | replication_connection_configuration<br>table, HEARTBEAT_INTERVAL column                        |
| Slave_last_heartbeat       | replication_connection_status table,<br>LAST_HEARTBEAT_TIMESTAMP column                         |
| Slave_received_heartbeats  | replication_connection_status table,<br>COUNT_RECEIVED_HEARTBEATS column                        |
| Slave_retried_transactions | replication_applier_status table,<br>COUNT_TRANSACTIONS_RETRIES column                          |
| Slave_running              | replication_connection_status and<br>replication_applier_status tables,<br>SERVICE_STATE column |

## <span id="page-23-1"></span>**Effect of show\_compatibility\_56 on FLUSH STATUS**

FLUSH STATUS statement:

• ON: This statement produces MySQL 5.6 behavior. It adds the current thread's session status variable values to the global values and resets the session values to zero. Some global variables may be reset to zero as well. It also resets the counters for key caches (default and named) to zero and sets [Max\\_used\\_connections](#page-78-0) to the current number of open connections.

- OFF: This statement adds the session status from all active sessions to the global status variables, resets the status of all active sessions, and resets account, host, and user status values aggregated from disconnected sessions.
- <span id="page-24-0"></span>• [show\\_create\\_table\\_verbosity](#page-24-0)

| Command-Line Format | show-create-table-verbosity[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | show_create_table_verbosity                |
| Scope               | Global, Session                            |
| Dynamic             | Yes                                        |
| Type                | Boolean                                    |
| Default Value       | OFF                                        |

SHOW CREATE TABLE normally does not show the ROW\_FORMAT table option if the row format is the default format. Enabling this variable causes SHOW CREATE TABLE to display ROW\_FORMAT regardless of whether it is the default format.

<span id="page-24-1"></span>• [show\\_old\\_temporals](#page-24-1)

| Command-Line Format | show-old-temporals[={OFF ON}] |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| System Variable     | show_old_temporals            |
| Scope               | Global, Session               |
| Dynamic             | Yes                           |
| Type                | Boolean                       |
| Default Value       | OFF                           |

Whether SHOW CREATE TABLE output includes comments to flag temporal columns found to be in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision). This variable is disabled by default. If enabled, SHOW CREATE TABLE output looks like this:

```
CREATE TABLE `mytbl` (
 `ts` timestamp /* 5.5 binary format */ NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `dt` datetime /* 5.5 binary format */ DEFAULT NULL,
 `t` time /* 5.5 binary format */ DEFAULT NULL
) DEFAULT CHARSET=latin1
```

Output for the COLUMN\_TYPE column of the Information Schema COLUMNS table is affected similarly.

This variable is deprecated; expect it to be removed in a future release of MySQL.

<span id="page-24-2"></span>• [skip\\_external\\_locking](#page-24-2)

| Command-Line Format | skip-external-locking[={OFF ON}] |
|---------------------|----------------------------------|
| System Variable     | skip_external_locking            |
| Scope               | Global                           |
| Dynamic             | No                               |
| Type                | Boolean                          |

| Default Value | ON |  |
|---------------|----|--|
|---------------|----|--|

This is OFF if mysqld uses external locking (system locking), ON if external locking is disabled. This affects only MyISAM table access.

This variable is set by the --external-locking or --skip-external-locking option. External locking is disabled by default.

External locking affects only MyISAM table access. For more information, including conditions under which it can and cannot be used, see Section 8.11.5, "External Locking".

<span id="page-25-0"></span>• [skip\\_name\\_resolve](#page-25-0)

| Command-Line Format | skip-name-resolve[={OFF ON}] |
|---------------------|------------------------------|
| System Variable     | skip_name_resolve            |
| Scope               | Global                       |
| Dynamic             | No                           |
| Type                | Boolean                      |
| Default Value       | OFF                          |

Whether to resolve host names when checking client connections. If this variable is OFF, mysqld resolves host names when checking client connections. If it is ON, mysqld uses only IP numbers; in this case, all Host column values in the grant tables must be IP addresses. See [Section 5.1.11.2,](#page-105-0) ["DNS Lookups and the Host Cache".](#page-105-0)

Depending on the network configuration of your system and the Host values for your accounts, clients may need to connect using an explicit --host option, such as --host=127.0.0.1 or - host=::1.

An attempt to connect to the host 127.0.0.1 normally resolves to the localhost account. However, this fails if the server is run with [skip\\_name\\_resolve](#page-25-0) enabled. If you plan to do that, make sure an account exists that can accept a connection. For example, to be able to connect as root using --host=127.0.0.1 or --host=::1, create these accounts:

```
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';
```

<span id="page-25-1"></span>• [skip\\_networking](#page-25-1)

| Command-Line Format | skip-networking[={OFF ON}] |
|---------------------|----------------------------|
| System Variable     | skip_networking            |
| Scope               | Global                     |
| Dynamic             | No                         |
| Type                | Boolean                    |
| Default Value       | OFF                        |

This variable controls whether the server permits TCP/IP connections. By default, it is disabled (permit TCP connections). If enabled, the server permits only local (non-TCP/IP) connections and all interaction with mysqld must be made using named pipes or shared memory (on Windows) or Unix socket files (on Unix). This option is highly recommended for systems where only local clients are permitted. See [Section 5.1.11.2, "DNS Lookups and the Host Cache"](#page-105-0).

• [skip\\_show\\_database](#page-25-2)

<span id="page-25-2"></span>

| 798 | Command-Line Format | skip-show-database |
|-----|---------------------|--------------------|
|-----|---------------------|--------------------|

| System Variable | skip_show_database |
|-----------------|--------------------|
| Scope           | Global             |
| Dynamic         | No                 |
| Type            | Boolean            |
| Default Value   | OFF                |

This prevents people from using the SHOW DATABASES statement if they do not have the SHOW DATABASES privilege. This can improve security if you have concerns about users being able to see databases belonging to other users. Its effect depends on the SHOW DATABASES privilege: If the variable value is ON, the SHOW DATABASES statement is permitted only to users who have the SHOW DATABASES privilege, and the statement displays all database names. If the value is OFF, SHOW DATABASES is permitted to all users, but displays the names of only those databases for which the user has the SHOW DATABASES or other privilege.

![](_page_26_Picture_3.jpeg)

### **Caution**

Because a global privilege is considered a privilege for all databases, any global privilege enables a user to see all database names with SHOW DATABASES or by examining the INFORMATION\_SCHEMA SCHEMATA table.

<span id="page-26-0"></span>• [slow\\_launch\\_time](#page-26-0)

| Command-Line Format | slow-launch-time=# |
|---------------------|--------------------|
| System Variable     | slow_launch_time   |
| Scope               | Global             |
| Dynamic             | Yes                |
| Type                | Integer            |
| Default Value       | 2                  |
| Minimum Value       | 0                  |
| Maximum Value       | 31536000           |
| Unit                | seconds            |

If creating a thread takes longer than this many seconds, the server increments the [Slow\\_launch\\_threads](#page-84-0) status variable.

<span id="page-26-1"></span>• [slow\\_query\\_log](#page-26-1)

| Command-Line Format | slow-query-log[={OFF ON}] |
|---------------------|---------------------------|
| System Variable     | slow_query_log            |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Boolean                   |
| Default Value       | OFF                       |

Whether the slow query log is enabled. The value can be 0 (or OFF) to disable the log or 1 (or ON) to enable the log. The destination for log output is controlled by the log\_output system variable; if that value is NONE, no log entries are written even if the log is enabled.

"Slow" is determined by the value of the long\_query\_time variable. See [Section 5.4.5, "The Slow](#page-145-0) [Query Log"](#page-145-0).

## <span id="page-27-0"></span>• [slow\\_query\\_log\\_file](#page-27-0)

| Command-Line Format | slow-query-log-file=file_name |
|---------------------|-------------------------------|
| System Variable     | slow_query_log_file           |
| Scope               | Global                        |
| Dynamic             | Yes                           |
| Type                | File name                     |
| Default Value       | host_name-slow.log            |

The name of the slow query log file. The default value is host\_name-slow.log, but the initial value can be changed with the --slow\_query\_log\_file option.

### <span id="page-27-1"></span>• [socket](#page-27-1)

| Command-Line Format     | socket={file_name pipe_name} |
|-------------------------|------------------------------|
| System Variable         | socket                       |
| Scope                   | Global                       |
| Dynamic                 | No                           |
| Type                    | String                       |
| Default Value (Windows) | MySQL                        |
| Default Value (Other)   | /tmp/mysql.sock              |

On Unix platforms, this variable is the name of the socket file that is used for local client connections. The default is /tmp/mysql.sock. (For some distribution formats, the directory might be different, such as /var/lib/mysql for RPMs.)

On Windows, this variable is the name of the named pipe that is used for local client connections. The default value is MySQL (not case-sensitive).

### <span id="page-27-2"></span>• [sort\\_buffer\\_size](#page-27-2)

| Command-Line Format                     | sort-buffer-size=#   |
|-----------------------------------------|----------------------|
| System Variable                         | sort_buffer_size     |
| Scope                                   | Global, Session      |
| Dynamic                                 | Yes                  |
| Type                                    | Integer              |
| Default Value                           | 262144               |
| Minimum Value                           | 32768                |
| Maximum Value (Windows)                 | 4294967295           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551615 |
| Maximum Value (Other, 32-bit platforms) | 4294967295           |
| Unit                                    | bytes                |

Each session that must perform a sort allocates a buffer of this size. [sort\\_buffer\\_size](#page-27-2) is not specific to any storage engine and applies in a general manner for optimization. At minimum the [sort\\_buffer\\_size](#page-27-2) value must be large enough to accommodate fifteen tuples in the sort

buffer. Also, increasing the value of max\_sort\_length may require increasing the value of [sort\\_buffer\\_size](#page-27-2). For more information, see Section 8.2.1.14, "ORDER BY Optimization"

If you see many [Sort\\_merge\\_passes](#page-85-0) per second in SHOW GLOBAL STATUS output, you can consider increasing the [sort\\_buffer\\_size](#page-27-2) value to speed up ORDER BY or GROUP BY operations that cannot be improved with query optimization or improved indexing.

The optimizer tries to work out how much space is needed but can allocate more, up to the limit. Setting it larger than required globally slows down most queries that sort. It is best to increase it as a session setting, and only for the sessions that need a larger size. On Linux, there are thresholds of 256KB and 2MB where larger values may significantly slow down memory allocation, so you should consider staying below one of those values. Experiment to find the best value for your workload. See Section B.3.3.5, "Where MySQL Stores Temporary Files".

The maximum permissible setting for [sort\\_buffer\\_size](#page-27-2) is 4GB−1. Larger values are permitted for 64-bit platforms (except 64-bit Windows, for which large values are truncated to 4GB−1 with a warning).

### <span id="page-28-0"></span>• [sql\\_auto\\_is\\_null](#page-28-0)

| System Variable | sql_auto_is_null |
|-----------------|------------------|
| Scope           | Global, Session  |
| Dynamic         | Yes              |
| Type            | Boolean          |
| Default Value   | OFF              |

If this variable is enabled, then after a statement that successfully inserts an automatically generated AUTO\_INCREMENT value, you can find that value by issuing a statement of the following form:

```
SELECT * FROM tbl_name WHERE auto_col IS NULL
```

If the statement returns a row, the value returned is the same as if you invoked the LAST\_INSERT\_ID() function. For details, including the return value after a multiple-row insert, see Section 12.15, "Information Functions". If no AUTO\_INCREMENT value was successfully inserted, the SELECT statement returns no row.

The behavior of retrieving an AUTO\_INCREMENT value by using an IS NULL comparison is used by some ODBC programs, such as Access. See [Obtaining Auto-Increment Values.](https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-usagenotes-functionality-last-insert-id.md) This behavior can be disabled by setting [sql\\_auto\\_is\\_null](#page-28-0) to OFF.

The default value of [sql\\_auto\\_is\\_null](#page-28-0) is OFF.

### <span id="page-28-1"></span>• [sql\\_big\\_selects](#page-28-1)

| System Variable | sql_big_selects |
|-----------------|-----------------|
| Scope           | Global, Session |
| Dynamic         | Yes             |
| Type            | Boolean         |
| Default Value   | ON              |

If set to OFF, MySQL aborts SELECT statements that are likely to take a very long time to execute (that is, statements for which the optimizer estimates that the number of examined rows exceeds the value of max\_join\_size). This is useful when an inadvisable WHERE statement has been issued. The default value for a new connection is ON, which permits all SELECT statements.

If you set the max\_join\_size system variable to a value other than DEFAULT, [sql\\_big\\_selects](#page-28-1) is set to OFF.

## <span id="page-29-0"></span>• [sql\\_buffer\\_result](#page-29-0)

| System Variable | sql_buffer_result |
|-----------------|-------------------|
| Scope           | Global, Session   |
| Dynamic         | Yes               |
| Type            | Boolean           |
| Default Value   | OFF               |

If enabled, [sql\\_buffer\\_result](#page-29-0) forces results from SELECT statements to be put into temporary tables. This helps MySQL free the table locks early and can be beneficial in cases where it takes a long time to send results to the client. The default value is OFF.

### <span id="page-29-1"></span>• [sql\\_log\\_off](#page-29-1)

| System Variable | sql_log_off          |
|-----------------|----------------------|
| Scope           | Global, Session      |
| Dynamic         | Yes                  |
| Type            | Boolean              |
| Default Value   | OFF                  |
| Valid Values    | OFF (enable logging) |
|                 | ON (disable logging) |

This variable controls whether logging to the general query log is disabled for the current session (assuming that the general query log itself is enabled). The default value is OFF (that is, enable logging). To disable or enable general query logging for the current session, set the session [sql\\_log\\_off](#page-29-1) variable to ON or OFF.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See [Section 5.1.8.1, "System Variable](#page-52-0) [Privileges".](#page-52-0)

### <span id="page-29-2"></span>• [sql\\_mode](#page-29-2)

| Command-Line Format | sql-mode=name                                                                                                                                            |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| System Variable     | sql_mode                                                                                                                                                 |
| Scope               | Global, Session                                                                                                                                          |
| Dynamic             | Yes                                                                                                                                                      |
| Type                | Set                                                                                                                                                      |
| Default Value       | ONLY_FULL_GROUP_BY<br>STRICT_TRANS_TABLES<br>NO_ZERO_IN_DATE NO_ZERO_DATE<br>ERROR_FOR_DIVISION_BY_ZERO<br>NO_AUTO_CREATE_USER<br>NO_ENGINE_SUBSTITUTION |
| Valid Values        | ALLOW_INVALID_DATES<br>ANSI_QUOTES<br>ERROR_FOR_DIVISION_BY_ZERO<br>HIGH_NOT_PRECEDENCE<br>IGNORE_SPACE                                                  |

```
NO_AUTO_CREATE_USER
NO_AUTO_VALUE_ON_ZERO
NO_BACKSLASH_ESCAPES
NO_DIR_IN_CREATE
NO_ENGINE_SUBSTITUTION
NO_FIELD_OPTIONS
NO_KEY_OPTIONS
NO_TABLE_OPTIONS
NO_UNSIGNED_SUBTRACTION
NO_ZERO_DATE
NO_ZERO_IN_DATE
ONLY_FULL_GROUP_BY
PAD_CHAR_TO_FULL_LENGTH
PIPES_AS_CONCAT
REAL_AS_FLOAT
STRICT_ALL_TABLES
STRICT_TRANS_TABLES
```

The current server SQL mode, which can be set dynamically. For details, see [Section 5.1.10, "Server](#page-88-0) [SQL Modes"](#page-88-0).

![](_page_30_Picture_3.jpeg)

## **Note**

MySQL installation programs may configure the SQL mode during the installation process. If the SQL mode differs from the default or from what you expect, check for a setting in an option file that the server reads at startup.

### <span id="page-30-0"></span>• [sql\\_notes](#page-30-0)

| System Variable | sql_notes       |
|-----------------|-----------------|
| Scope           | Global, Session |
| Dynamic         | Yes             |
| Type            | Boolean         |
| Default Value   | ON              |

If enabled (the default), diagnostics of Note level increment warning\_count and the server records them. If disabled, Note diagnostics do not increment [warning\\_count](#page-50-0) and the server does not record them. mysqldump includes output to disable this variable so that reloading the dump file does not produce warnings for events that do not affect the integrity of the reload operation.

<span id="page-30-1"></span>• [sql\\_quote\\_show\\_create](#page-30-1)

| System Variable | sql_quote_show_create |
|-----------------|-----------------------|

| Scope         | Global, Session |
|---------------|-----------------|
| Dynamic       | Yes             |
| Type          | Boolean         |
| Default Value | ON              |

If enabled (the default), the server quotes identifiers for SHOW CREATE TABLE and SHOW CREATE DATABASE statements. If disabled, quoting is disabled. This option is enabled by default so that replication works for identifiers that require quoting. See Section 13.7.5.10, "SHOW CREATE TABLE Statement", and Section 13.7.5.6, "SHOW CREATE DATABASE Statement".

### <span id="page-31-0"></span>• [sql\\_safe\\_updates](#page-31-0)

| System Variable | sql_safe_updates |
|-----------------|------------------|
| Scope           | Global, Session  |
| Dynamic         | Yes              |
| Type            | Boolean          |
| Default Value   | OFF              |

If this variable is enabled, UPDATE and DELETE statements that do not use a key in the WHERE clause or a LIMIT clause produce an error. This makes it possible to catch UPDATE and DELETE statements where keys are not used properly and that would probably change or delete a large number of rows. The default value is OFF.

For the mysql client, [sql\\_safe\\_updates](#page-31-0) can be enabled by using the --safe-updates option. For more information, see Using Safe-Updates Mode (--safe-updates).

### <span id="page-31-1"></span>• [sql\\_select\\_limit](#page-31-1)

| System Variable | sql_select_limit     |
|-----------------|----------------------|
| Scope           | Global, Session      |
| Dynamic         | Yes                  |
| Type            | Integer              |
| Default Value   | 18446744073709551615 |
| Minimum Value   | 0                    |
| Maximum Value   | 18446744073709551615 |

The maximum number of rows to return from SELECT statements. For more information, see Using Safe-Updates Mode (--safe-updates).

The default value for a new connection is the maximum number of rows that the server permits per table. Typical default values are (232)−1 or (264)−1. If you have changed the limit, the default value can be restored by assigning a value of DEFAULT.

If a SELECT has a LIMIT clause, the LIMIT takes precedence over the value of [sql\\_select\\_limit](#page-31-1).

## • [sql\\_warnings](#page-31-2)

<span id="page-31-2"></span>

|     | System Variable | sql_warnings    |
|-----|-----------------|-----------------|
|     | Scope           | Global, Session |
|     | Dynamic         | Yes             |
| 804 | Type            | Boolean         |

This variable controls whether single-row INSERT statements produce an information string if warnings occur. The default is OFF. Set the value to ON to produce an information string.

### <span id="page-32-0"></span>• [ssl\\_ca](#page-32-0)

| Command-Line Format | ssl-ca=file_name |
|---------------------|------------------|
| System Variable     | ssl_ca           |
| Scope               | Global           |
| Dynamic             | No               |
| Type                | File name        |
| Default Value       | NULL             |

The path name of the Certificate Authority (CA) certificate file in PEM format. The file contains a list of trusted SSL Certificate Authorities.

## <span id="page-32-1"></span>• [ssl\\_capath](#page-32-1)

| Command-Line Format | ssl-capath=dir_name |
|---------------------|---------------------|
| System Variable     | ssl_capath          |
| Scope               | Global              |
| Dynamic             | No                  |
| Type                | Directory name      |
| Default Value       | NULL                |

The path name of the directory that contains trusted SSL Certificate Authority (CA) certificate files in PEM format. You must run OpenSSL rehash on the directory specified by this option prior to using it. On Linux systems, you can invoke rehash like this:

### \$> **openssl rehash path/to/directory**

On Windows platforms, you can use the c\_rehash script in a command prompt, like this:

### \> **c\_rehash path/to/directory**

See [openssl-rehash](https://docs.openssl.org/3.1/man1/openssl-rehash/) for complete syntax and other information.

Support for this capability depends on the SSL library used to compile MySQL; see Section 6.3.4, "SSL Library-Dependent Capabilities".

### <span id="page-32-2"></span>• [ssl\\_cert](#page-32-2)

| Command-Line Format | ssl-cert=file_name |
|---------------------|--------------------|
| System Variable     | ssl_cert           |
| Scope               | Global             |
| Dynamic             | No                 |
| Type                | File name          |

| Default Value | NULL |
|---------------|------|
|---------------|------|

The path name of the server SSL public key certificate file in PEM format.

If the server is started with [ssl\\_cert](#page-32-2) set to a certificate that uses any restricted cipher or cipher category, the server starts with support for encrypted connections disabled. For information about cipher restrictions, see Connection Cipher Configuration.

<span id="page-33-0"></span>• [ssl\\_cipher](#page-33-0)

| Command-Line Format | ssl-cipher=name |
|---------------------|-----------------|
| System Variable     | ssl_cipher      |
| Scope               | Global          |
| Dynamic             | No              |
| Type                | String          |
| Default Value       | NULL            |

The list of permissible ciphers for connection encryption. If no cipher in the list is supported, encrypted connections do not work.

For greatest portability, the cipher list should be a list of one or more cipher names, separated by colons. This format is understood both by OpenSSL and yaSSL. The following example shows two cipher names separated by a colon:

```
[mysqld]
ssl_cipher="DHE-RSA-AES128-GCM-SHA256:AES128-SHA"
```

OpenSSL supports a more flexible syntax for specifying ciphers, as described in the OpenSSL documentation at [https://www.openssl.org/docs/manmaster/man1/openssl-ciphers.html.](https://www.openssl.org/docs/manmaster/man1/openssl-ciphers.md) yaSSL does not, so attempts to use that extended syntax fail for a MySQL distribution compiled using yaSSL.

For information about which encryption ciphers MySQL supports, see Section 6.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-33-1"></span>• [ssl\\_crl](#page-33-1)

| Command-Line Format | ssl-crl=file_name |
|---------------------|-------------------|
| System Variable     | ssl_crl           |
| Scope               | Global            |
| Dynamic             | No                |
| Type                | File name         |
| Default Value       | NULL              |

The path name of the file containing certificate revocation lists in PEM format. Support for revocationlist capability depends on the SSL library used to compile MySQL. See Section 6.3.4, "SSL Library-Dependent Capabilities".

• [ssl\\_crlpath](#page-33-2)

<span id="page-33-2"></span>

|     | Command-Line Format | ssl-crlpath=dir_name |
|-----|---------------------|----------------------|
|     | System Variable     | ssl_crlpath          |
|     | Scope               | Global               |
|     | Dynamic             | No                   |
| 806 | Type                | Directory name       |

| Default Value | NULL |
|---------------|------|
|---------------|------|

The path of the directory that contains certificate revocation-list files in PEM format. Support for revocation-list capability depends on the SSL library used to compile MySQL. See Section 6.3.4, "SSL Library-Dependent Capabilities".

## <span id="page-34-1"></span>• [ssl\\_key](#page-34-1)

| Command-Line Format | ssl-key=file_name |
|---------------------|-------------------|
| System Variable     | ssl_key           |
| Scope               | Global            |
| Dynamic             | No                |
| Type                | File name         |
| Default Value       | NULL              |

The path name of the server SSL private key file in PEM format. For better security, use a certificate with an RSA key size of at least 2048 bits.

If the key file is protected by a passphrase, the server prompts the user for the passphrase. The password must be given interactively; it cannot be stored in a file. If the passphrase is incorrect, the program continues as if it could not read the key.

### <span id="page-34-2"></span>• [stored\\_program\\_cache](#page-34-2)

| Command-Line Format | stored-program-cache=# |
|---------------------|------------------------|
| System Variable     | stored_program_cache   |
| Scope               | Global                 |
| Dynamic             | Yes                    |
| Type                | Integer                |
| Default Value       | 256                    |
| Minimum Value       | 16                     |
| Maximum Value       | 524288                 |

Sets a soft upper limit for the number of cached stored routines per connection. The value of this variable is specified in terms of the number of stored routines held in each of the two caches maintained by the MySQL Server for, respectively, stored procedures and stored functions.

Whenever a stored routine is executed this cache size is checked before the first or top-level statement in the routine is parsed; if the number of routines of the same type (stored procedures or stored functions according to which is being executed) exceeds the limit specified by this variable, the corresponding cache is flushed and memory previously allocated for cached objects is freed. This allows the cache to be flushed safely, even when there are dependencies between stored routines.

### <span id="page-34-0"></span>• [super\\_read\\_only](#page-34-0)

| Command-Line Format | super-read-only[={OFF ON}] |
|---------------------|----------------------------|
| System Variable     | super_read_only            |
| Scope               | Global                     |
| Dynamic             | Yes                        |
| Type                | Boolean                    |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

If the [read\\_only](#page-10-0) system variable is enabled, the server permits no client updates except from users who have the SUPER privilege. If the [super\\_read\\_only](#page-34-0) system variable is also enabled, the server prohibits client updates even from users who have SUPER. See the description of the [read\\_only](#page-10-0) system variable for a description of read-only mode and information about how [read\\_only](#page-10-0) and [super\\_read\\_only](#page-34-0) interact.

Client updates prevented when [super\\_read\\_only](#page-34-0) is enabled include operations that do not necessarily appear to be updates, such as CREATE FUNCTION (to install a loadable function) and INSTALL PLUGIN. These operations are prohibited because they involve changes to tables in the mysql system database.

Changes to [super\\_read\\_only](#page-34-0) on a replication source server are not replicated to replica servers. The value can be set on a replica independent of the setting on the source.

<span id="page-35-0"></span>• [sync\\_frm](#page-35-0)

| Command-Line Format | sync-frm[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| System Variable     | sync_frm            |
| Scope               | Global              |
| Dynamic             | Yes                 |
| Type                | Boolean             |
| Default Value       | ON                  |

If this variable is set to 1, when any nontemporary table is created its .frm file is synchronized to disk (using fdatasync()). This is slower but safer in case of a crash. The default is 1.

This variable is deprecated in MySQL 5.7 and is removed in MySQL 8.0 (when .frm files become obsolete).

<span id="page-35-1"></span>• [system\\_time\\_zone](#page-35-1)

| System Variable | system_time_zone |
|-----------------|------------------|
| Scope           | Global           |
| Dynamic         | No               |
| Type            | String           |

The server system time zone. When the server begins executing, it inherits a time zone setting from the machine defaults, possibly modified by the environment of the account used for running the server or the startup script. The value is used to set [system\\_time\\_zone](#page-35-1). To explicitly specify the system time zone, set the TZ environment variable or use the --timezone option of the mysqld\_safe script.

The [system\\_time\\_zone](#page-35-1) variable differs from the [time\\_zone](#page-41-0) variable. Although they might have the same value, the latter variable is used to initialize the time zone for each client that connects. See [Section 5.1.13, "MySQL Server Time Zone Support".](#page-111-0)

• [table\\_definition\\_cache](#page-35-2)

<span id="page-35-2"></span>

|     | Command-Line Format | table-definition-cache=# |
|-----|---------------------|--------------------------|
|     | System Variable     | table_definition_cache   |
| 808 | Scope               | Global                   |

| Dynamic       | Yes                                                            |
|---------------|----------------------------------------------------------------|
| Type          | Integer                                                        |
| Default Value | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value | 400                                                            |
| Maximum Value | 524288                                                         |

The number of table definitions (from .frm files) that can be stored in the table definition cache. If you use a large number of tables, you can create a large table definition cache to speed up opening of tables. The table definition cache takes less space and does not use file descriptors, unlike the normal table cache. The minimum value is 400. The default value is based on the following formula, capped to a limit of 2000:

```
400 + (table_open_cache / 2)
```

For InnoDB, the [table\\_definition\\_cache](#page-35-2) setting acts as a soft limit for the number of table instances in the InnoDB data dictionary cache and the number file-per-table tablespaces that can be open at one time.

If the number of table instances in the InnoDB data dictionary cache exceeds the [table\\_definition\\_cache](#page-35-2) limit, an LRU mechanism begins marking table instances for eviction and eventually removes them from the InnoDB data dictionary cache. The number of open tables with cached metadata can be higher than the [table\\_definition\\_cache](#page-35-2) limit due to table instances with foreign key relationships, which are not placed on the LRU list.

The number of file-per-table tablespaces that can be open at one time is limited by both the [table\\_definition\\_cache](#page-35-2) and innodb\_open\_files settings. If both variables are set, the highest setting is used. If neither variable is set, the [table\\_definition\\_cache](#page-35-2) setting, which has a higher default value, is used. If the number of open tablespaces exceeds the limit defined by [table\\_definition\\_cache](#page-35-2) or innodb\_open\_files, an LRU mechanism searches the LRU list for tablespace files that are fully flushed and not currently being extended. This process is performed each time a new tablespace is opened. Only inactive tablespaces are closed.

## <span id="page-36-0"></span>• [table\\_open\\_cache](#page-36-0)

| Command-Line Format | table-open-cache=# |
|---------------------|--------------------|
| System Variable     | table_open_cache   |
| Scope               | Global             |
| Dynamic             | Yes                |
| Type                | Integer            |
| Default Value       | 2000               |
| Minimum Value       | 1                  |
| Maximum Value       | 524288             |

The number of open tables for all threads. Increasing this value increases the number of file descriptors that mysqld requires. The effective value of this variable is the greater of the effective value of open\_files\_limit - 10 - the effective value of max\_connections / 2, and 400; that is

```
MAX(
 (open_files_limit - 10 - max_connections) / 2,
 400
 )
```

You can check whether you need to increase the table cache by checking the [Opened\\_tables](#page-79-0) status variable. If the value of [Opened\\_tables](#page-79-0) is large and you do not use FLUSH TABLES often (which just forces all tables to be closed and reopened), then you should increase the value of the [table\\_open\\_cache](#page-36-0) variable. For more information about the table cache, see Section 8.4.3.1, "How MySQL Opens and Closes Tables".

## <span id="page-37-0"></span>• [table\\_open\\_cache\\_instances](#page-37-0)

| Command-Line Format | table-open-cache-instances=# |
|---------------------|------------------------------|
| System Variable     | table_open_cache_instances   |
| Scope               | Global                       |
| Dynamic             | No                           |
| Type                | Integer                      |
| Default Value       | 16                           |
| Minimum Value       | 1                            |
| Maximum Value       | 64                           |

The number of open tables cache instances. To improve scalability by reducing contention among sessions, the open tables cache can be partitioned into several smaller cache instances of size [table\\_open\\_cache](#page-36-0) / [table\\_open\\_cache\\_instances](#page-37-0) . A session needs to lock only one instance to access it for DML statements. This segments cache access among instances, permitting higher performance for operations that use the cache when there are many sessions accessing tables. (DDL statements still require a lock on the entire cache, but such statements are much less frequent than DML statements.)

A value of 8 or 16 is recommended on systems that routinely use 16 or more cores. However, if you have many large triggers on your tables that cause a high memory load, the default setting for [table\\_open\\_cache\\_instances](#page-37-0) might lead to excessive memory usage. In that situation, it can be helpful to set [table\\_open\\_cache\\_instances](#page-37-0) to 1 in order to restrict memory usage.

### <span id="page-37-1"></span>• [thread\\_cache\\_size](#page-37-1)

| Command-Line Format | thread-cache-size=#                                            |
|---------------------|----------------------------------------------------------------|
| System Variable     | thread_cache_size                                              |
| Scope               | Global                                                         |
| Dynamic             | Yes                                                            |
| Type                | Integer                                                        |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value       | 0                                                              |
| Maximum Value       | 16384                                                          |

How many threads the server should cache for reuse. When a client disconnects, the client's threads are put in the cache if there are fewer than [thread\\_cache\\_size](#page-37-1) threads there. Requests for threads are satisfied by reusing threads taken from the cache if possible, and only when the cache is empty is a new thread created. This variable can be increased to improve performance if you have a lot of new connections. Normally, this does not provide a notable performance improvement if you have a good thread implementation. However, if your server sees hundreds of connections per second you should normally set [thread\\_cache\\_size](#page-37-1) high enough so that most new connections use cached threads. By examining the difference between the [Connections](#page-70-0) and [Threads\\_created](#page-88-1) status variables, you can see how efficient the thread cache is. For details, see [Section 5.1.9, "Server Status Variables".](#page-67-0)

The default value is based on the following formula, capped to a limit of 100:

8 + (max\_connections / 100)

This variable has no effect for the embedded server (libmysqld) and as of MySQL 5.7.2 is no longer visible within the embedded server.

## <span id="page-38-0"></span>• [thread\\_handling](#page-38-0)

| Command-Line Format | thread-handling=name      |
|---------------------|---------------------------|
| System Variable     | thread_handling           |
| Scope               | Global                    |
| Dynamic             | No                        |
| Type                | Enumeration               |
| Default Value       | one-thread-per-connection |
| Valid Values        | no-threads                |
|                     | one-thread-per-connection |
|                     | loaded-dynamically        |

The thread-handling model used by the server for connection threads. The permissible values are no-threads (the server uses a single thread to handle one connection), one-threadper-connection (the server uses one thread to handle each client connection), and loadeddynamically (set by the thread pool plugin when it initializes). no-threads is useful for debugging under Linux; see [Section 5.8, "Debugging MySQL".](#page-196-0)

This variable has no effect for the embedded server (libmysqld) and as of MySQL 5.7.2 is no longer visible within the embedded server.

### <span id="page-38-1"></span>• [thread\\_pool\\_algorithm](#page-38-1)

| Command-Line Format | thread-pool-algorithm=# |
|---------------------|-------------------------|
| System Variable     | thread_pool_algorithm   |
| Scope               | Global                  |
| Dynamic             | No                      |

This variable controls which algorithm the thread pool plugin uses:

- A value of 0 (the default) uses a conservative low-concurrency algorithm which is most well tested and is known to produce very good results.
- A value of 1 increases the concurrency and uses a more aggressive algorithm which at times has been known to perform 5–10% better on optimal thread counts, but has degrading performance as the number of connections increases. Its use should be considered as experimental and not supported.

This variable is available only if the thread pool plugin is enabled. See [Section 5.5.3, "MySQL](#page-155-0) [Enterprise Thread Pool"](#page-155-0).

### <span id="page-38-2"></span>• [thread\\_pool\\_high\\_priority\\_connection](#page-38-2)

| Command-Line Format | thread-pool-high-priority<br>connection=# |
|---------------------|-------------------------------------------|
| System Variable     | thread_pool_high_priority_connection      |
| Scope               | Global, Session                           |
| Dynamic             | Yes                                       |
| Type                | Integer                                   |

| Default Value | 0 |
|---------------|---|
| Minimum Value | 0 |
| Maximum Value | 1 |

This variable affects queuing of new statements prior to execution. If the value is 0 (false, the default), statement queuing uses both the low-priority and high-priority queues. If the value is 1 (true), queued statements always go to the high-priority queue.

This variable is available only if the thread pool plugin is enabled. See [Section 5.5.3, "MySQL](#page-155-0) [Enterprise Thread Pool"](#page-155-0).

### <span id="page-39-0"></span>• [thread\\_pool\\_max\\_unused\\_threads](#page-39-0)

| Command-Line Format | thread-pool-max-unused-threads=# |
|---------------------|----------------------------------|
| System Variable     | thread_pool_max_unused_threads   |
| Scope               | Global                           |
| Dynamic             | Yes                              |

The maximum permitted number of unused threads in the thread pool. This variable makes it possible to limit the amount of memory used by sleeping threads.

A value of 0 (the default) means no limit on the number of sleeping threads. A value of N where N is greater than 0 means 1 consumer thread and N−1 reserve threads. In this case, if a thread is ready to sleep but the number of sleeping threads is already at the maximum, the thread exits rather than going to sleep.

A sleeping thread is either sleeping as a consumer thread or a reserve thread. The thread pool permits one thread to be the consumer thread when sleeping. If a thread goes to sleep and there is no existing consumer thread, it sleeps as a consumer thread. When a thread must be woken up, a consumer thread is selected if there is one. A reserve thread is selected only when there is no consumer thread to wake up.

This variable is available only if the thread pool plugin is enabled. See [Section 5.5.3, "MySQL](#page-155-0) [Enterprise Thread Pool"](#page-155-0).

## <span id="page-39-1"></span>• [thread\\_pool\\_prio\\_kickup\\_timer](#page-39-1)

| Command-Line Format | thread-pool-prio-kickup-timer=# |
|---------------------|---------------------------------|
| System Variable     | thread_pool_prio_kickup_timer   |
| Scope               | Global                          |
| Dynamic             | Yes                             |

This variable affects statements waiting for execution in the low-priority queue. The value is the number of milliseconds before a waiting statement is moved to the high-priority queue. The default is 1000 (1 second).

This variable is available only if the thread pool plugin is enabled. See [Section 5.5.3, "MySQL](#page-155-0) [Enterprise Thread Pool"](#page-155-0).

### <span id="page-39-2"></span>• [thread\\_pool\\_size](#page-39-2)

| Command-Line Format | thread-pool-size=# |
|---------------------|--------------------|
| System Variable     | thread_pool_size   |
| Scope               | Global             |
| Dynamic             | No                 |

| Type          | Integer |
|---------------|---------|
| Default Value | 16      |
| Minimum Value | 1       |
| Maximum Value | 64      |

The number of thread groups in the thread pool. This is the most important parameter controlling thread pool performance. It affects how many statements can execute simultaneously. If a value outside the range of permissible values is specified, the thread pool plugin does not load and the server writes a message to the error log.

This variable is available only if the thread pool plugin is enabled. See [Section 5.5.3, "MySQL](#page-155-0) [Enterprise Thread Pool"](#page-155-0).

## <span id="page-40-0"></span>• [thread\\_pool\\_stall\\_limit](#page-40-0)

| Command-Line Format | thread-pool-stall-limit=# |
|---------------------|---------------------------|
| System Variable     | thread_pool_stall_limit   |
| Scope               | Global                    |
| Dynamic             | Yes                       |
| Type                | Integer                   |
| Default Value       | 6                         |
| Minimum Value       | 4                         |
| Maximum Value       | 600                       |
| Unit                | milliseconds * 10         |

This variable affects executing statements. The value is the amount of time a statement has to finish after starting to execute before it becomes defined as stalled, at which point the thread pool permits the thread group to begin executing another statement. The value is measured in 10 millisecond units, so the default of 6 means 60ms. Short wait values permit threads to start more quickly. Short values are also better for avoiding deadlock situations. Long wait values are useful for workloads that include long-running statements, to avoid starting too many new statements while the current ones execute.

This variable is available only if the thread pool plugin is enabled. See [Section 5.5.3, "MySQL](#page-155-0) [Enterprise Thread Pool"](#page-155-0).

### <span id="page-40-1"></span>• [thread\\_stack](#page-40-1)

| Command-Line Format              | thread-stack=#       |
|----------------------------------|----------------------|
| System Variable                  | thread_stack         |
| Scope                            | Global               |
| Dynamic                          | No                   |
| Type                             | Integer              |
| Default Value (64-bit platforms) | 262144               |
| Default Value (32-bit platforms) | 196608               |
| Minimum Value                    | 131072               |
| Maximum Value (64-bit platforms) | 18446744073709550592 |
| Maximum Value (32-bit platforms) | 4294966272           |
| Unit                             | bytes                |

| Block Size | 1024 |
|------------|------|
|------------|------|

The stack size for each thread. The default is large enough for normal operation. If the thread stack size is too small, it limits the complexity of the SQL statements that the server can handle, the recursion depth of stored procedures, and other memory-consuming actions.

<span id="page-41-1"></span>• [time\\_format](#page-41-1)

This variable is unused. It is deprecated and is removed in MySQL 8.0.

<span id="page-41-0"></span>• [time\\_zone](#page-41-0)

| System Variable | time_zone       |
|-----------------|-----------------|
| Scope           | Global, Session |
| Dynamic         | Yes             |
| Type            | String          |
| Default Value   | SYSTEM          |
| Minimum Value   | -12:59          |
| Maximum Value   | +13:00          |

The current time zone. This variable is used to initialize the time zone for each client that connects. By default, the initial value of this is 'SYSTEM' (which means, "use the value of [system\\_time\\_zone](#page-35-1)"). The value can be specified explicitly at server startup with the --defaulttime-zone option. See [Section 5.1.13, "MySQL Server Time Zone Support"](#page-111-0).

![](_page_41_Picture_8.jpeg)

### **Note**

If set to SYSTEM, every MySQL function call that requires a time zone calculation makes a system library call to determine the current system time zone. This call may be protected by a global mutex, resulting in contention.

<span id="page-41-2"></span>• [timestamp](#page-41-2)

| System Variable | timestamp        |
|-----------------|------------------|
| Scope           | Session          |
| Dynamic         | Yes              |
| Type            | Numeric          |
| Default Value   | UNIX_TIMESTAMP() |
| Minimum Value   | 1                |
| Maximum Value   | 2147483647       |

Set the time for this client. This is used to get the original timestamp if you use the binary log to restore rows. timestamp\_value should be a Unix epoch timestamp (a value like that returned by UNIX\_TIMESTAMP(), not a value in 'YYYY-MM-DD hh:mm:ss' format) or DEFAULT.

Setting [timestamp](#page-41-2) to a constant value causes it to retain that value until it is changed again. Setting [timestamp](#page-41-2) to DEFAULT causes its value to be the current date and time as of the time it is accessed. The maximum value corresponds to '2038-01-19 03:14:07' UTC, the same as for the TIMESTAMP data type.

[timestamp](#page-41-2) is a DOUBLE rather than BIGINT because its value includes a microseconds part.

SET timestamp affects the value returned by NOW() but not by SYSDATE(). This means that timestamp settings in the binary log have no effect on invocations of SYSDATE(). The server can be started with the --sysdate-is-now option to cause SYSDATE() to be a synonym for NOW(), in which case SET timestamp affects both functions.

<span id="page-42-0"></span>• [tls\\_version](#page-42-0)

| Command-Line Format | tls-version=protocol_list |
|---------------------|---------------------------|
| System Variable     | tls_version               |
| Scope               | Global                    |
| Dynamic             | No                        |
| Type                | String                    |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2     |

Which protocols the server permits for encrypted connections. The value is a comma-separated list containing one or more protocol versions. The protocols that can be named for this variable depend on the SSL library used to compile MySQL. Permitted protocols should be chosen such as not to leave "holes" in the list. For details, see Section 6.3.2, "Encrypted Connection TLS Protocols and Ciphers".

![](_page_42_Picture_5.jpeg)

### **Note**

As of MySQL 5.7.35, the TLSv1 and TLSv1.1 connection protocols are deprecated and support for them is subject to removal in a future version of MySQL. See Deprecated TLS Protocols.

Setting this variable to an empty string disables encrypted connections.

<span id="page-42-1"></span>• [tmp\\_table\\_size](#page-42-1)

| Command-Line Format | tmp-table-size=#     |
|---------------------|----------------------|
| System Variable     | tmp_table_size       |
| Scope               | Global, Session      |
| Dynamic             | Yes                  |
| Type                | Integer              |
| Default Value       | 16777216             |
| Minimum Value       | 1024                 |
| Maximum Value       | 18446744073709551615 |
| Unit                | bytes                |

The maximum size of internal in-memory temporary tables. This variable does not apply to usercreated MEMORY tables.

The actual limit is the smaller of [tmp\\_table\\_size](#page-42-1) and max\_heap\_table\_size. When an inmemory temporary table exceeds the limit, MySQL automatically converts it to an on-disk temporary table. The internal\_tmp\_disk\_storage\_engine option defines the storage engine used for ondisk temporary tables.

Increase the value of [tmp\\_table\\_size](#page-42-1) (and max\_heap\_table\_size if necessary) if you do many advanced GROUP BY queries and you have lots of memory.

You can compare the number of internal on-disk temporary tables created to the total number of internal temporary tables created by comparing [Created\\_tmp\\_disk\\_tables](#page-70-1) and [Created\\_tmp\\_tables](#page-70-2) values.

## <span id="page-43-1"></span>• [tmpdir](#page-43-1)

| Command-Line Format | tmpdir=dir_name |
|---------------------|-----------------|
| System Variable     | tmpdir          |
| Scope               | Global          |
| Dynamic             | No              |
| Type                | Directory name  |

The path of the directory to use for creating temporary files. It might be useful if your default /tmp directory resides on a partition that is too small to hold temporary tables. This variable can be set to a list of several paths that are used in round-robin fashion. Paths should be separated by colon characters (:) on Unix and semicolon characters (;) on Windows.

[tmpdir](#page-43-1) can be a non-permanent location, such as a directory on a memory-based file system or a directory that is cleared when the server host restarts. If the MySQL server is acting as a replica, and you are using a non-permanent location for [tmpdir](#page-43-1), consider setting a different temporary directory for the replica using the slave\_load\_tmpdir variable. For a replica, the temporary files used to replicate LOAD DATA statements are stored in this directory, so with a permanent location they can survive machine restarts, although replication can now continue after a restart if the temporary files have been removed.

For more information about the storage location of temporary files, see Section B.3.3.5, "Where MySQL Stores Temporary Files".

<span id="page-43-2"></span>• [transaction\\_alloc\\_block\\_size](#page-43-2)

| Command-Line Format | transaction-alloc-block-size=# |
|---------------------|--------------------------------|
| System Variable     | transaction_alloc_block_size   |
| Scope               | Global, Session                |
| Dynamic             | Yes                            |
| Type                | Integer                        |
| Default Value       | 8192                           |
| Minimum Value       | 1024                           |
| Maximum Value       | 131072                         |
| Unit                | bytes                          |
| Block Size          | 1024                           |

The amount in bytes by which to increase a per-transaction memory pool which needs memory. See the description of [transaction\\_prealloc\\_size](#page-45-0).

• [transaction\\_isolation](#page-43-0)

<span id="page-43-0"></span>

|     | Command-Line Format | transaction-isolation=name |
|-----|---------------------|----------------------------|
|     | System Variable     | transaction_isolation      |
|     | Scope               | Global, Session            |
|     | Dynamic             | Yes                        |
|     | Type                | Enumeration                |
|     | Default Value       | REPEATABLE-READ            |
|     | Valid Values        | READ-UNCOMMITTED           |
|     |                     | READ-COMMITTED             |
| 816 |                     |                            |

```
REPEATABLE-READ
SERIALIZABLE
```

The transaction isolation level. The default is REPEATABLE-READ.

The transaction isolation level has three scopes: global, session, and next transaction. This three-scope implementation leads to some nonstandard isolation-level assignment semantics, as described later.

To set the global transaction isolation level at startup, use the --transaction-isolation server option.

At runtime, the isolation level can be set directly using the SET statement to assign a value to the [transaction\\_isolation](#page-43-0) system variable, or indirectly using the SET TRANSACTION statement. If you set [transaction\\_isolation](#page-43-0) directly to an isolation level name that contains a space, the name should be enclosed within quotation marks, with the space replaced by a dash. For example, use this SET statement to set the global value:

```
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
```

Setting the global [transaction\\_isolation](#page-43-0) value sets the isolation level for all subsequent sessions. Existing sessions are unaffected.

To set the session or next-level [transaction\\_isolation](#page-43-0) value, use the SET statement. For most session system variables, these statements are equivalent ways to set the value:

```
SET @@SESSION.var_name = value;
SET SESSION var_name = value;
SET var_name = value;
SET @@var_name = value;
```

As mentioned previously, the transaction isolation level has a next-transaction scope, in addition to the global and session scopes. To enable the next-transaction scope to be set, SET syntax for assigning session system variable values has nonstandard semantics for [transaction\\_isolation](#page-43-0):

• To set the session isolation level, use any of these syntaxes:

```
SET @@SESSION.transaction_isolation = value;
SET SESSION transaction_isolation = value;
```

SET transaction\_isolation = value;

For each of those syntaxes, these semantics apply:

- Sets the isolation level for all subsequent transactions performed within the session.
- Permitted within transactions, but does not affect the current ongoing transaction.
- If executed between transactions, overrides any preceding statement that sets the nexttransaction isolation level.
- Corresponds to SET SESSION TRANSACTION ISOLATION LEVEL (with the SESSION keyword).
- To set the next-transaction isolation level, use this syntax:

```
SET @@transaction_isolation = value;
```

For that syntax, these semantics apply:

- Sets the isolation level only for the next single transaction performed within the session.
- Subsequent transactions revert to the session isolation level.
- Not permitted within transactions.
- Corresponds to SET TRANSACTION ISOLATION LEVEL (without the SESSION keyword).

For more information about SET TRANSACTION and its relationship to the [transaction\\_isolation](#page-43-0) system variable, see Section 13.3.6, "SET TRANSACTION Statement".

![](_page_45_Picture_15.jpeg)

### **Note**

[transaction\\_isolation](#page-43-0) was added in MySQL 5.7.20 as a synonym for [tx\\_isolation](#page-47-0), which is now deprecated and is removed in MySQL 8.0. Applications should be adjusted to use [transaction\\_isolation](#page-43-0) in preference to [tx\\_isolation](#page-47-0).

<span id="page-45-0"></span>• [transaction\\_prealloc\\_size](#page-45-0)

| Command-Line Format | transaction-prealloc-size=# |
|---------------------|-----------------------------|
| System Variable     | transaction_prealloc_size   |
| Scope               | Global, Session             |
| Dynamic             | Yes                         |
| Type                | Integer                     |
| Default Value       | 4096                        |
| Minimum Value       | 1024                        |
| Maximum Value       | 131072                      |
| Unit                | bytes                       |
| Block Size          | 1024                        |

There is a per-transaction memory pool from which various transaction-related allocations take memory. The initial size of the pool in bytes is [transaction\\_prealloc\\_size](#page-45-0). For every allocation that cannot be satisfied from the pool because it has insufficient memory available, the pool is increased by [transaction\\_alloc\\_block\\_size](#page-43-2) bytes. When the transaction ends, the pool is truncated to [transaction\\_prealloc\\_size](#page-45-0) bytes.

By making [transaction\\_prealloc\\_size](#page-45-0) sufficiently large to contain all statements within a single transaction, you can avoid many malloc() calls.

<span id="page-46-0"></span>• [transaction\\_read\\_only](#page-46-0)

| Command-Line Format | transaction-read-only[={OFF ON}] |
|---------------------|----------------------------------|
| System Variable     | transaction_read_only            |
| Scope               | Global, Session                  |
| Dynamic             | Yes                              |
| Type                | Boolean                          |
| Default Value       | OFF                              |

The transaction access mode. The value can be OFF (read/write; the default) or ON (read only).

The transaction access mode has three scopes: global, session, and next transaction. This threescope implementation leads to some nonstandard access-mode assignment semantics, as described later.

To set the global transaction access mode at startup, use the --transaction-read-only server option.

At runtime, the access mode can be set directly using the SET statement to assign a value to the [transaction\\_read\\_only](#page-46-0) system variable, or indirectly using the SET TRANSACTION statement. For example, use this SET statement to set the global value:

```
SET GLOBAL transaction_read_only = ON;
```

Setting the global [transaction\\_read\\_only](#page-46-0) value sets the access mode for all subsequent sessions. Existing sessions are unaffected.

To set the session or next-level [transaction\\_read\\_only](#page-46-0) value, use the SET statement. For most session system variables, these statements are equivalent ways to set the value:

```
SET @@SESSION.var_name = value;
SET SESSION var_name = value;
SET var_name = value;
SET @@var_name = value;
```

As mentioned previously, the transaction access mode has a next-transaction scope, in addition to the global and session scopes. To enable the next-transaction scope to be set, SET syntax for assigning session system variable values has nonstandard semantics for [transaction\\_read\\_only](#page-46-0),

• To set the session access mode, use any of these syntaxes:

```
SET @@SESSION.transaction_read_only = value;
SET SESSION transaction_read_only = value;
```

```
SET transaction_read_only = value;
```

For each of those syntaxes, these semantics apply:

- Sets the access mode for all subsequent transactions performed within the session.
- Permitted within transactions, but does not affect the current ongoing transaction.
- If executed between transactions, overrides any preceding statement that sets the nexttransaction access mode.
- Corresponds to SET SESSION TRANSACTION {READ WRITE | READ ONLY} (with the SESSION keyword).
- To set the next-transaction access mode, use this syntax:

```
SET @@transaction_read_only = value;
```

For that syntax, these semantics apply:

- Sets the access mode only for the next single transaction performed within the session.
- Subsequent transactions revert to the session access mode.
- Not permitted within transactions.
- Corresponds to SET TRANSACTION {READ WRITE | READ ONLY} (without the SESSION keyword).

For more information about SET TRANSACTION and its relationship to the [transaction\\_read\\_only](#page-46-0) system variable, see Section 13.3.6, "SET TRANSACTION Statement".

![](_page_47_Picture_15.jpeg)

## **Note**

[transaction\\_read\\_only](#page-46-0) was added in MySQL 5.7.20 as a synonym for [tx\\_read\\_only](#page-48-0), which is now deprecated and is removed in MySQL 8.0. Applications should be adjusted to use [transaction\\_read\\_only](#page-46-0) in preference to [tx\\_read\\_only](#page-48-0).

<span id="page-47-0"></span>• [tx\\_isolation](#page-47-0)

| Deprecated      | Yes              |
|-----------------|------------------|
| System Variable | tx_isolation     |
| Scope           | Global, Session  |
| Dynamic         | Yes              |
| Type            | Enumeration      |
| Default Value   | REPEATABLE-READ  |
| Valid Values    | READ-UNCOMMITTED |
|                 | READ-COMMITTED   |
|                 | REPEATABLE-READ  |

SERIALIZABLE

The default transaction isolation level. Defaults to REPEATABLE-READ.

![](_page_48_Picture_3.jpeg)

### **Note**

[transaction\\_isolation](#page-43-0) was added in MySQL 5.7.20 as a synonym for [tx\\_isolation](#page-47-0), which is now deprecated and is removed in MySQL 8.0. Applications should be adjusted to use [transaction\\_isolation](#page-43-0) in preference to [tx\\_isolation](#page-47-0). See the description of [transaction\\_isolation](#page-43-0) for details.

<span id="page-48-0"></span>• [tx\\_read\\_only](#page-48-0)

| Deprecated      | Yes             |
|-----------------|-----------------|
| System Variable | tx_read_only    |
| Scope           | Global, Session |
| Dynamic         | Yes             |
| Type            | Boolean         |
| Default Value   | OFF             |

The default transaction access mode. The value can be OFF (read/write, the default) or ON (read only).

![](_page_48_Picture_9.jpeg)

### **Note**

[transaction\\_read\\_only](#page-46-0) was added in MySQL 5.7.20 as a synonym for [tx\\_read\\_only](#page-48-0), which is now deprecated and is removed in MySQL 8.0. Applications should be adjusted to use [transaction\\_read\\_only](#page-46-0) in preference to [tx\\_read\\_only](#page-48-0). See the description of [transaction\\_read\\_only](#page-46-0) for details.

<span id="page-48-1"></span>• [unique\\_checks](#page-48-1)

| System Variable | unique_checks   |
|-----------------|-----------------|
| Scope           | Global, Session |
| Dynamic         | Yes             |
| Type            | Boolean         |
| Default Value   | ON              |

If set to 1 (the default), uniqueness checks for secondary indexes in InnoDB tables are performed. If set to 0, storage engines are permitted to assume that duplicate keys are not present in input data. If you know for certain that your data does not contain uniqueness violations, you can set this to 0 to speed up large table imports to InnoDB.

Setting this variable to 0 does not require storage engines to ignore duplicate keys. An engine is still permitted to check for them and issue duplicate-key errors if it detects them.

<span id="page-48-2"></span>• [updatable\\_views\\_with\\_limit](#page-48-2)

| Command-Line Format | updatable-views-with-limit[={OFF <br>ON}] |
|---------------------|-------------------------------------------|
| System Variable     | updatable_views_with_limit                |
| Scope               | Global, Session<br>821                    |

| Dynamic       | Yes     |
|---------------|---------|
| Type          | Boolean |
| Default Value | 1       |

This variable controls whether updates to a view can be made when the view does not contain all columns of the primary key defined in the underlying table, if the update statement contains a LIMIT clause. (Such updates often are generated by GUI tools.) An update is an UPDATE or DELETE statement. Primary key here means a PRIMARY KEY, or a UNIQUE index in which no column can contain NULL.

The variable can have two values:

- 1 or YES: Issue a warning only (not an error message). This is the default value.
- 0 or NO: Prohibit the update.
- validate\_password\_xxx

The validate\_password plugin implements a set of system variables having names of the form validate\_password\_xxx. These variables affect password testing by that plugin; see Section 6.4.3.2, "Password Validation Plugin Options and Variables".

<span id="page-49-0"></span>• [version](#page-49-0)

The version number for the server. The value might also include a suffix indicating server build or configuration information. -log indicates that one or more of the general log, slow query log, or binary log are enabled. -debug indicates that the server was built with debugging support enabled.

<span id="page-49-1"></span>• [version\\_comment](#page-49-1)

| System Variable | version_comment |
|-----------------|-----------------|
| Scope           | Global          |
| Dynamic         | No              |
| Type            | String          |

The CMake configuration program has a COMPILATION\_COMMENT option that permits a comment to be specified when building MySQL. This variable contains the value of that comment. See Section 2.8.7, "MySQL Source-Configuration Options".

<span id="page-49-2"></span>• [version\\_compile\\_machine](#page-49-2)

| System Variable | version_compile_machine |  |
|-----------------|-------------------------|--|
| Scope           | Global                  |  |
| Dynamic         | No                      |  |
| Type            | String                  |  |

The type of the server binary.

<span id="page-49-3"></span>• [version\\_compile\\_os](#page-49-3)

| System Variable | version_compile_os |  |
|-----------------|--------------------|--|
| Scope           | Global             |  |
| Dynamic         | No                 |  |
| Type            | String             |  |

The type of operating system on which MySQL was built.

<span id="page-50-1"></span>• [wait\\_timeout](#page-50-1)

| Command-Line Format     | wait-timeout=#  |
|-------------------------|-----------------|
| System Variable         | wait_timeout    |
| Scope                   | Global, Session |
| Dynamic                 | Yes             |
| Type                    | Integer         |
| Default Value           | 28800           |
| Minimum Value           | 1               |
| Maximum Value (Windows) | 2147483         |
| Maximum Value (Other)   | 31536000        |
| Unit                    | seconds         |

The number of seconds the server waits for activity on a noninteractive connection before closing it.

On thread startup, the session [wait\\_timeout](#page-50-1) value is initialized from the global [wait\\_timeout](#page-50-1) value or from the global interactive\_timeout value, depending on the type of client (as defined by the CLIENT\_INTERACTIVE connect option to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.md)). See also interactive\_timeout.

<span id="page-50-0"></span>• [warning\\_count](#page-50-0)

The number of errors, warnings, and notes that resulted from the last statement that generated messages. This variable is read only. See Section 13.7.5.40, "SHOW WARNINGS Statement".

## <span id="page-50-2"></span>**5.1.8 Using System Variables**

The MySQL server maintains many system variables that configure its operation. Section 5.1.7, "Server System Variables", describes the meaning of these variables. Each system variable has a default value. System variables can be set at server startup using options on the command line or in an option file. Most of them can be changed dynamically while the server is running by means of the SET statement, which enables you to modify operation of the server without having to stop and restart it. You can also use system variable values in expressions.

Many system variables are built in. System variables implemented by a server plugin are exposed when the plugin is installed and have names that begin with the plugin name. For example, the audit\_log plugin implements a system variable named audit\_log\_policy.

There are two scopes in which system variables exist. Global variables affect the overall operation of the server. Session variables affect its operation for individual client connections. A given system variable can have both a global and a session value. Global and session system variables are related as follows:

- When the server starts, it initializes each global variable to its default value. These defaults can be changed by options specified on the command line or in an option file. (See Section 4.2.2, "Specifying Program Options".)
- The server also maintains a set of session variables for each client that connects. The client's session variables are initialized at connect time using the current values of the corresponding global variables. For example, a client's SQL mode is controlled by the session [sql\\_mode](#page-29-2) value, which is initialized when the client connects to the value of the global [sql\\_mode](#page-29-2) value.

For some system variables, the session value is not initialized from the corresponding global value; if so, that is indicated in the variable description.

System variable values can be set globally at server startup by using options on the command line or in an option file. At startup, the syntax for system variables is the same as for command options, so within variable names, dashes and underscores may be used interchangeably. For example, -- general log=ON and --general-log=ON are equivalent.

When you use a startup option to set a variable that takes a numeric value, the value can be given with a suffix of K, M, or G (either uppercase or lowercase) to indicate a multiplier of 1024, 1024<sup>2</sup> or 1024<sup>3</sup>; that is, units of kilobytes, megabytes, or gigabytes, respectively. Thus, the following command starts the server with an InnobB log file size of 16 megabytes and a maximum packet size of one gigabyte:

```
mysqld --innodb-log-file-size=16M --max-allowed-packet=1G
```

Within an option file, those variables are set like this:

```
[mysqld]\ninnodb_log_file_size=16M
max_allowed_packet=1G
```

The lettercase of suffix letters does not matter; 16M and 16m are equivalent, as are 1G and 1g.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement, specify this maximum by using an option of the form  $--maximum-var\_name=value$  at server startup. For example, to prevent the value of  $innodb\_log\_file\_size$  from being increased to more than 32MB at runtime, use the option --maximum-innodb-log-file-size=32M.

Many system variables are dynamic and can be changed at runtime by using the SET statement. For a list, see Section 5.1.8.2, "Dynamic System Variables". To change a system variable with SET, refer to it by name, optionally preceded by a modifier. At runtime, system variable names must be written using underscores, not dashes. The following examples briefly illustrate this syntax:

· Set a global system variable:

```
SET GLOBAL max_connections = 1000;
SET @@GLOBAL.max connections = 1000;
```

Set a session system variable:

```
SET SESSION sql_mode = 'TRADITIONAL';
SET @@SESSION.sql_mode = 'TRADITIONAL';
SET @@sql_mode = 'TRADITIONAL';
```

For complete details about SET syntax, see Section 13.7.4.1, "SET Syntax for Variable Assignment". For a description of the privilege requirements for setting system variables, see Section 5.1.8.1, "System Variable Privileges"

Suffixes for specifying a value multiplier can be used when setting a variable at server startup, but not to set the value with SET at runtime. On the other hand, with SET you can assign a variable's value using an expression, which is not true when you set a variable at server startup. For example, the first of the following lines is legal at server startup, but the second is not:

```
$> mysql --max_allowed_packet=16M
$> mysql --max_allowed_packet=16*1024*1024
```

Conversely, the second of the following lines is legal at runtime, but the first is not:

```
mysql> SET GLOBAL max_allowed_packet=16M;
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;
```

To display system variable names and values, use the SHOW VARIABLES statement:

```
      mysql> SHOW VARIABLES;

      +------------------------------------
```

```
| bulk_insert_buffer_size | 8388608 |
| character_set_client | utf8 |
| character_set_connection | utf8 |
| character_set_database | latin1 |
| character_set_filesystem | binary |
| character_set_results | utf8 |
| character_set_server | latin1 |
| character_set_system | utf8 |
| character_sets_dir | /home/mysql/share/mysql/charsets/ |
| collation_connection | utf8_general_ci |
| collation_database | latin1_swedish_ci |
| collation_server | latin1_swedish_ci |
...
| innodb_autoextend_increment | 8 |
| innodb_buffer_pool_size | 8388608 |
| innodb_checksums | ON |
| innodb_commit_concurrency | 0 |
| innodb_concurrency_tickets | 500 |
| innodb_data_file_path | ibdata1:10M:autoextend |
| innodb_data_home_dir | |
...
| version | 5.7.18-log |
| version_comment | Source distribution |
| version_compile_machine | i686 |
| version_compile_os | suse-linux |
| wait_timeout | 28800 |
+---------------------------------+-----------------------------------+
```

With a LIKE clause, the statement displays only those variables that match the pattern. To obtain a specific variable name, use a LIKE clause as shown:

```
SHOW VARIABLES LIKE 'max_join_size';
SHOW SESSION VARIABLES LIKE 'max_join_size';
```

To get a list of variables whose name match a pattern, use the % wildcard character in a LIKE clause:

```
SHOW VARIABLES LIKE '%size%';
SHOW GLOBAL VARIABLES LIKE '%size%';
```

Wildcard characters can be used in any position within the pattern to be matched. Strictly speaking, because \_ is a wildcard that matches any single character, you should escape it as \\_ to match it literally. In practice, this is rarely necessary.

For SHOW VARIABLES, if you specify neither GLOBAL nor SESSION, MySQL returns SESSION values.

The reason for requiring the GLOBAL keyword when setting GLOBAL-only variables but not when retrieving them is to prevent problems in the future:

- Were a SESSION variable to be removed that has the same name as a GLOBAL variable, a client with privileges sufficient to modify global variables might accidentally change the GLOBAL variable rather than just the SESSION variable for its own session.
- Were a SESSION variable to be added with the same name as a GLOBAL variable, a client that intends to change the GLOBAL variable might find only its own SESSION variable changed.

## <span id="page-52-0"></span>**5.1.8.1 System Variable Privileges**

A system variable can have a global value that affects server operation as a whole, a session value that affects only the current session, or both. To modify system variable runtime values, use the SET statement. See Section 13.7.4.1, "SET Syntax for Variable Assignment". This section describes the privileges required to assign values to system variables at runtime.

Setting a global system variable runtime value requires the SUPER privilege.

To set a session system variable runtime value, use the SET SESSION statement. In contrast to setting global runtime values, setting session runtime values normally requires no special privileges and can be done by any user to affect the current session. For some system variables, setting the session value may have effects outside the current session and thus is a restricted operation that

can be done only by users who have the SUPER privilege. If a session system variable is restricted in this way, the variable description indicates that restriction. Examples include binlog\_format and sql\_log\_bin. Setting the session value of these variables affects binary logging for the current session, but may also have wider implications for the integrity of server replication and backups.

## <span id="page-53-0"></span>**5.1.8.2 Dynamic System Variables**

Many server system variables are dynamic and can be set at runtime. See Section 13.7.4.1, "SET Syntax for Variable Assignment". For a description of the privilege requirements for setting system variables, see [Section 5.1.8.1, "System Variable Privileges"](#page-52-0)

The following table lists all dynamic system variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the variables. Where appropriate, direct links to further information about the items are provided.

Variables that have a type of "string" take a string value. Variables that have a type of "numeric" take a numeric value. Variables that have a type of "boolean" can be set to 0, 1, ON or OFF. Variables that are marked as "enumeration" normally should be set to one of the available values for the variable, but can also be set to the number that corresponds to the desired enumeration value. For enumerated system variables, the first enumeration value corresponds to 0. This differs from the ENUM data type used for table columns, for which the first enumeration value corresponds to 1.

**Table 5.4 Dynamic System Variable Summary**

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| audit_log_connection_policy                      | Enumeration   | Global         |
| audit_log_disable                                | Boolean       | Global         |
| audit_log_exclude_accounts                       | String        | Global         |
| audit_log_flush                                  | Boolean       | Global         |
| audit_log_format_unix_timestamp Boolean          |               | Global         |
| audit_log_include_accounts                       | String        | Global         |
| audit_log_read_buffer_size                       | Integer       | Varies         |
| audit_log_rotate_on_size                         | Integer       | Global         |
| audit_log_statement_policy                       | Enumeration   | Global         |
| authentication_ldap_sasl_auth_method_name        | String        | Global         |
| authentication_ldap_sasl_bind_base_dn String     |               | Global         |
| authentication_ldap_sasl_bind_root_dn String     |               | Global         |
| authentication_ldap_sasl_bind_root_pwd String    |               | Global         |
| authentication_ldap_sasl_ca_pathString           |               | Global         |
| authentication_ldap_sasl_group_search_attr       | String        | Global         |
| authentication_ldap_sasl_group_search_filter     | String        | Global         |
| authentication_ldap_sasl_init_pool_size Integer  |               | Global         |
| authentication_ldap_sasl_log_statusInteger       |               | Global         |
| authentication_ldap_sasl_max_pool_size Integer   |               | Global         |
| authentication_ldap_sasl_server_host String      |               | Global         |
| authentication_ldap_sasl_server_port Integer     |               | Global         |
| authentication_ldap_sasl_tls                     | Boolean       | Global         |
| authentication_ldap_sasl_user_search_attr String |               | Global         |

| Variable Name                                      | Variable Type | Variable Scope |
|----------------------------------------------------|---------------|----------------|
| authentication_ldap_simple_auth_method_name        | String        | Global         |
| authentication_ldap_simple_bind_base_dn String     |               | Global         |
| authentication_ldap_simple_bind_root_dn String     |               | Global         |
| authentication_ldap_simple_bind_root_pwd String    |               | Global         |
| authentication_ldap_simple_ca_pathString           |               | Global         |
| authentication_ldap_simple_group_search_attr       | String        | Global         |
| authentication_ldap_simple_group_search_filter     | String        | Global         |
| authentication_ldap_simple_init_pool_size Integer  |               | Global         |
| authentication_ldap_simple_log_status Integer      |               | Global         |
| authentication_ldap_simple_max_pool_size Integer   |               | Global         |
| authentication_ldap_simple_server_host String      |               | Global         |
| authentication_ldap_simple_server_port Integer     |               | Global         |
| authentication_ldap_simple_tls                     | Boolean       | Global         |
| authentication_ldap_simple_user_search_attr        | String        | Global         |
| auto_increment_increment                           | Integer       | Both           |
| auto_increment_offset                              | Integer       | Both           |
| autocommit                                         | Boolean       | Both           |
| automatic_sp_privileges                            | Boolean       | Global         |
| avoid_temporal_upgrade                             | Boolean       | Global         |
| big_tables                                         | Boolean       | Both           |
| binlog_cache_size                                  | Integer       | Global         |
| binlog_checksum                                    | String        | Global         |
| binlog_direct_non_transactional_updates Boolan     |               | Both           |
| binlog_error_action                                | Enumeration   | Global         |
| binlog_format                                      | Enumeration   | Both           |
| binlog_group_commit_sync_delay Integer             |               | Global         |
| binlog_group_commit_sync_no_delay_count            | Integer       | Global         |
| binlog_max_flush_queue_time                        | Integer       | Global         |
| binlog_order_commits                               | Boolean       | Global         |
| binlog_row_image                                   | Enumeration   | Both           |
| binlog_rows_query_log_events                       | Boolean       | Both           |
| binlog_stmt_cache_size                             | Integer       | Global         |
| binlog_transaction_dependency_history_size         | Integer       | Global         |
| binlog_transaction_dependency_tracking Enumeration |               | Global         |
| block_encryption_mode                              | String        | Both           |
| bulk_insert_buffer_size                            | Integer       | Both           |
| character_set_client                               | String        | Both           |
| character_set_connection                           | String        | Both           |
| character_set_database                             | String        | Both           |
| character_set_filesystem                           | String        | Both           |
| character_set_results                              | String        | Both           |

| Variable Name                                     | Variable Type | Variable Scope |
|---------------------------------------------------|---------------|----------------|
| character_set_server                              | String        | Both           |
| check_proxy_users                                 | Boolean       | Global         |
| collation_connection                              | String        | Both           |
| collation_database                                | String        | Both           |
| collation_server                                  | String        | Both           |
| completion_type                                   | Enumeration   | Both           |
| concurrent_insert                                 | Enumeration   | Global         |
| connect_timeout                                   | Integer       | Global         |
| connection_control_failed_connections_threshold   | Integer       | Global         |
| connection_control_max_connection_delay Integer   |               | Global         |
| connection_control_min_connection_delay Integer   |               | Global         |
| debug                                             | String        | Both           |
| debug_sync                                        | String        | Session        |
| default_password_lifetime                         | Integer       | Global         |
| default_storage_engine                            | Enumeration   | Both           |
| default_tmp_storage_engine                        | Enumeration   | Both           |
| default_week_format                               | Integer       | Both           |
| delay_key_write                                   | Enumeration   | Global         |
| delayed_insert_limit                              | Integer       | Global         |
| delayed_insert_timeout                            | Integer       | Global         |
| delayed_queue_size                                | Integer       | Global         |
| div_precision_increment                           | Integer       | Both           |
| end_markers_in_json                               | Boolean       | Both           |
| enforce_gtid_consistency                          | Enumeration   | Global         |
| eq_range_index_dive_limit                         | Integer       | Both           |
| event_scheduler                                   | Enumeration   | Global         |
| expire_logs_days                                  | Integer       | Global         |
| explicit_defaults_for_timestamp                   | Boolean       | Both           |
| flush                                             | Boolean       | Global         |
| flush_time                                        | Integer       | Global         |
| foreign_key_checks                                | Boolean       | Both           |
| ft_boolean_syntax                                 | String        | Global         |
| general_log                                       | Boolean       | Global         |
| general_log_file                                  | File name     | Global         |
| group_concat_max_len                              | Integer       | Both           |
| group_replication_allow_local_disjoint_gtids_join | Boolean       | Global         |
| group_replication_allow_local_lower_version_join  | Boolean       | Global         |
| group_replication_auto_increment_increment        | Integer       | Global         |
| group_replication_bootstrap_groupBoolean          |               | Global         |
| group_replication_components_stop_timeout         | Integer       | Global         |
| group_replication_compression_threshold Integer   |               | Global         |

| Variable Name                                         | Variable Type | Variable Scope |
|-------------------------------------------------------|---------------|----------------|
| group_replication_enforce_update_everywhere_checks    | Boolean       | Global         |
| group_replication_exit_state_actionEnumeration        |               | Global         |
| group_replication_flow_control_applier_threshold      | Integer       | Global         |
| group_replication_flow_control_certifier_threshold    | Integer       | Global         |
| group_replication_flow_control_mode Enumeration       |               | Global         |
| group_replication_force_membersString                 |               | Global         |
| group_replication_group_name                          | String        | Global         |
| group_replication_group_seeds                         | String        | Global         |
| group_replication_gtid_assignment_block_size          | Integer       | Global         |
| group_replication_ip_whitelist                        | String        | Global         |
| group_replication_local_address                       | String        | Global         |
| group_replication_member_weightInteger                |               | Global         |
| group_replication_poll_spin_loopsInteger              |               | Global         |
| group_replication_recovery_complete_at Enumeration    |               | Global         |
| group_replication_recovery_reconnect_interval         | Integer       | Global         |
| group_replication_recovery_retry_count Integer        |               | Global         |
| group_replication_recovery_ssl_caString               |               | Global         |
| group_replication_recovery_ssl_capath String          |               | Global         |
| group_replication_recovery_ssl_cert String            |               | Global         |
| group_replication_recovery_ssl_cipher String          |               | Global         |
| group_replication_recovery_ssl_crlFile name           |               | Global         |
| group_replication_recovery_ssl_crlpath Directory name |               | Global         |
| group_replication_recovery_ssl_keyString              |               | Global         |
| group_replication_recovery_ssl_verify_server_cert     | Boolean       | Global         |
| group_replication_recovery_use_ssl Boolean            |               | Global         |
| group_replication_single_primary_mode Boolan          |               | Global         |
| group_replication_ssl_mode                            | Enumeration   | Global         |
| group_replication_start_on_boot                       | Boolean       | Global         |
| group_replication_transaction_size_limit Integer      |               | Global         |
| group_replication_unreachable_majority_timeout        | Integer       | Global         |
| gtid_executed_compression_periodInteger               |               | Global         |
| gtid_mode                                             | Enumeration   | Global         |
| gtid_next                                             | Enumeration   | Session        |
| gtid_purged                                           | String        | Global         |
| host_cache_size                                       | Integer       | Global         |
| identity                                              | Integer       | Session        |
| init_connect                                          | String        | Global         |
| init_slave                                            | String        | Global         |
| innodb_adaptive_flushing                              | Boolean       | Global         |
| innodb_adaptive_flushing_lwm                          | Integer       | Global         |
| innodb_adaptive_hash_index                            | Boolean       | Global         |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| innodb_adaptive_max_sleep_delayInteger           |               | Global         |
| innodb_api_bk_commit_interval                    | Integer       | Global         |
| innodb_api_trx_level                             | Integer       | Global         |
| innodb_autoextend_increment                      | Integer       | Global         |
| innodb_background_drop_list_emptyBoolean         |               | Global         |
| innodb_buffer_pool_dump_at_shutdown Boolean      |               | Global         |
| innodb_buffer_pool_dump_now                      | Boolean       | Global         |
| innodb_buffer_pool_dump_pct                      | Integer       | Global         |
| innodb_buffer_pool_filename                      | File name     | Global         |
| innodb_buffer_pool_load_abort                    | Boolean       | Global         |
| innodb_buffer_pool_load_now                      | Boolean       | Global         |
| innodb_buffer_pool_size                          | Integer       | Global         |
| innodb_change_buffer_max_size Integer            |               | Global         |
| innodb_change_buffering                          | Enumeration   | Global         |
| innodb_change_buffering_debug                    | Integer       | Global         |
| innodb_checksum_algorithm                        | Enumeration   | Global         |
| innodb_cmp_per_index_enabled                     | Boolean       | Global         |
| innodb_commit_concurrency                        | Integer       | Global         |
| innodb_compress_debug                            | Enumeration   | Global         |
| innodb_compression_failure_threshold_pct Integer |               | Global         |
| innodb_compression_level                         | Integer       | Global         |
| innodb_compression_pad_pct_maxInteger            |               | Global         |
| innodb_concurrency_tickets                       | Integer       | Global         |
| innodb_deadlock_detect                           | Boolean       | Global         |
| innodb_default_row_format                        | Enumeration   | Global         |
| innodb_disable_resize_buffer_pool_debug Boolean  |               | Global         |
| innodb_disable_sort_file_cache                   | Boolean       | Global         |
| innodb_fast_shutdown                             | Integer       | Global         |
| innodb_fil_make_page_dirty_debugInteger          |               | Global         |
| innodb_file_format                               | String        | Global         |
| innodb_file_format_max                           | String        | Global         |
| innodb_file_per_table                            | Boolean       | Global         |
| innodb_fill_factor                               | Integer       | Global         |
| innodb_flush_log_at_timeout                      | Integer       | Global         |
| innodb_flush_log_at_trx_commit                   | Enumeration   | Global         |
| innodb_flush_neighbors                           | Enumeration   | Global         |
| innodb_flush_sync                                | Boolean       | Global         |
| innodb_flushing_avg_loops                        | Integer       | Global         |
| innodb_ft_aux_table                              | String        | Global         |
| innodb_ft_enable_diag_print                      | Boolean       | Global         |
| innodb_ft_enable_stopword                        | Boolean       | Both           |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| innodb_ft_num_word_optimize                  | Integer       | Global         |
| innodb_ft_result_cache_limit                 | Integer       | Global         |
| innodb_ft_server_stopword_table String       |               | Global         |
| innodb_ft_user_stopword_table                | String        | Both           |
| innodb_io_capacity                           | Integer       | Global         |
| innodb_io_capacity_max                       | Integer       | Global         |
| innodb_large_prefix                          | Boolean       | Global         |
| innodb_limit_optimistic_insert_debugInteger  |               | Global         |
| innodb_lock_wait_timeout                     | Integer       | Both           |
| innodb_log_checkpoint_now                    | Boolean       | Global         |
| innodb_log_checksums                         | Boolean       | Global         |
| innodb_log_compressed_pages                  | Boolean       | Global         |
| innodb_log_write_ahead_size                  | Integer       | Global         |
| innodb_lru_scan_depth                        | Integer       | Global         |
| innodb_max_dirty_pages_pct                   | Numeric       | Global         |
| innodb_max_dirty_pages_pct_lwmNumeric        |               | Global         |
| innodb_max_purge_lag                         | Integer       | Global         |
| innodb_max_purge_lag_delay                   | Integer       | Global         |
| innodb_max_undo_log_size                     | Integer       | Global         |
| innodb_merge_threshold_set_all_debug Integer |               | Global         |
| innodb_monitor_disable                       | String        | Global         |
| innodb_monitor_enable                        | String        | Global         |
| innodb_monitor_reset                         | Enumeration   | Global         |
| innodb_monitor_reset_all                     | Enumeration   | Global         |
| innodb_old_blocks_pct                        | Integer       | Global         |
| innodb_old_blocks_time                       | Integer       | Global         |
| innodb_online_alter_log_max_sizeInteger      |               | Global         |
| innodb_optimize_fulltext_only                | Boolean       | Global         |
| innodb_print_all_deadlocks                   | Boolean       | Global         |
| innodb_purge_batch_size                      | Integer       | Global         |
| innodb_purge_rseg_truncate_frequency Integer |               | Global         |
| innodb_random_read_ahead                     | Boolean       | Global         |
| innodb_read_ahead_threshold                  | Integer       | Global         |
| innodb_replication_delay                     | Integer       | Global         |
| innodb_rollback_segments                     | Integer       | Global         |
| innodb_saved_page_number_debugInteger        |               | Global         |
| innodb_spin_wait_delay                       | Integer       | Global         |
| innodb_stats_auto_recalc                     | Boolean       | Global         |
| innodb_stats_include_delete_marked Boolean   |               | Global         |
| innodb_stats_method                          | Enumeration   | Global         |
| innodb_stats_on_metadata                     | Boolean       | Global         |

| Variable Name                                 | Variable Type  | Variable Scope |
|-----------------------------------------------|----------------|----------------|
| innodb_stats_persistent                       | Boolean        | Global         |
| innodb_stats_persistent_sample_pages Integer  |                | Global         |
| innodb_stats_sample_pages                     | Integer        | Global         |
| innodb_stats_transient_sample_pages Integer   |                | Global         |
| innodb_status_output                          | Boolean        | Global         |
| innodb_status_output_locks                    | Boolean        | Global         |
| innodb_strict_mode                            | Boolean        | Both           |
| innodb_support_xa                             | Boolean        | Both           |
| innodb_sync_spin_loops                        | Integer        | Global         |
| innodb_table_locks                            | Boolean        | Both           |
| innodb_thread_concurrency                     | Integer        | Global         |
| innodb_thread_sleep_delay                     | Integer        | Global         |
| innodb_tmpdir                                 | Directory name | Both           |
| innodb_trx_purge_view_update_only_debug       | Boolean        | Global         |
| innodb_trx_rseg_n_slots_debug                 | Integer        | Global         |
| innodb_undo_log_truncate                      | Boolean        | Global         |
| innodb_undo_logs                              | Integer        | Global         |
| insert_id                                     | Integer        | Session        |
| interactive_timeout                           | Integer        | Both           |
| internal_tmp_disk_storage_engineEnumeration   |                | Global         |
| join_buffer_size                              | Integer        | Both           |
| keep_files_on_create                          | Boolean        | Both           |
| key_buffer_size                               | Integer        | Global         |
| key_cache_age_threshold                       | Integer        | Global         |
| key_cache_block_size                          | Integer        | Global         |
| key_cache_division_limit                      | Integer        | Global         |
| keyring_aws_cmk_id                            | String         | Global         |
| keyring_aws_region                            | Enumeration    | Global         |
| keyring_encrypted_file_data                   | File name      | Global         |
| keyring_encrypted_file_password String        |                | Global         |
| keyring_file_data                             | File name      | Global         |
| keyring_okv_conf_dir                          | Directory name | Global         |
| keyring_operations                            | Boolean        | Global         |
| last_insert_id                                | Integer        | Session        |
| lc_messages                                   | String         | Both           |
| lc_time_names                                 | String         | Both           |
| local_infile                                  | Boolean        | Global         |
| lock_wait_timeout                             | Integer        | Both           |
| log_bin_trust_function_creators               | Boolean        | Global         |
| log_bin_use_v1_row_events                     | Boolean        | Global         |
| log_builtin_as_identified_by_password Boolean |                | Global         |

| Variable Name                                  | Variable Type | Variable Scope |
|------------------------------------------------|---------------|----------------|
| log_error_verbosity                            | Integer       | Global         |
| log_output                                     | Set           | Global         |
| log_queries_not_using_indexes                  | Boolean       | Global         |
| log_slow_admin_statements                      | Boolean       | Global         |
| log_slow_slave_statements                      | Boolean       | Global         |
| log_statements_unsafe_for_binlogBoolean        |               | Global         |
| log_syslog                                     | Boolean       | Global         |
| log_syslog_facility                            | String        | Global         |
| log_syslog_include_pid                         | Boolean       | Global         |
| log_syslog_tag                                 | String        | Global         |
| log_throttle_queries_not_using_indexes Integer |               | Global         |
| log_timestamps                                 | Enumeration   | Global         |
| log_warnings                                   | Integer       | Global         |
| long_query_time                                | Numeric       | Both           |
| low_priority_updates                           | Boolean       | Both           |
| master_info_repository                         | String        | Global         |
| master_verify_checksum                         | Boolean       | Global         |
| max_allowed_packet                             | Integer       | Both           |
| max_binlog_cache_size                          | Integer       | Global         |
| max_binlog_size                                | Integer       | Global         |
| max_binlog_stmt_cache_size                     | Integer       | Global         |
| max_connect_errors                             | Integer       | Global         |
| max_connections                                | Integer       | Global         |
| max_delayed_threads                            | Integer       | Both           |
| max_error_count                                | Integer       | Both           |
| max_execution_time                             | Integer       | Both           |
| max_heap_table_size                            | Integer       | Both           |
| max_insert_delayed_threads                     | Integer       | Both           |
| max_join_size                                  | Integer       | Both           |
| max_length_for_sort_data                       | Integer       | Both           |
| max_points_in_geometry                         | Integer       | Both           |
| max_prepared_stmt_count                        | Integer       | Global         |
| max_relay_log_size                             | Integer       | Global         |
| max_seeks_for_key                              | Integer       | Both           |
| max_sort_length                                | Integer       | Both           |
| max_sp_recursion_depth                         | Integer       | Both           |
| max_tmp_tables                                 | Integer       | Both           |
| max_user_connections                           | Integer       | Both           |
| max_write_lock_count                           | Integer       | Global         |
| min_examined_row_limit                         | Integer       | Both           |
| multi_range_count                              | Integer       | Both           |

| Variable Name                             | Variable Type | Variable Scope |
|-------------------------------------------|---------------|----------------|
| myisam_data_pointer_size                  | Integer       | Global         |
| myisam_max_sort_file_size                 | Integer       | Global         |
| myisam_sort_buffer_size                   | Integer       | Both           |
| myisam_stats_method                       | Enumeration   | Both           |
| myisam_use_mmap                           | Boolean       | Global         |
| mysql_firewall_mode                       | Boolean       | Global         |
| mysql_firewall_trace                      | Boolean       | Global         |
| mysql_native_password_proxy_users Boolean |               | Global         |
| mysqlx_connect_timeout                    | Integer       | Global         |
| mysqlx_idle_worker_thread_timeoutInteger  |               | Global         |
| mysqlx_max_allowed_packet                 | Integer       | Global         |
| mysqlx_max_connections                    | Integer       | Global         |
| mysqlx_min_worker_threads                 | Integer       | Global         |
| ndb_allow_copying_alter_table             | Boolean       | Both           |
| ndb_autoincrement_prefetch_sz             | Integer       | Both           |
| ndb_batch_size                            | Integer       | Both           |
| ndb_blob_read_batch_bytes                 | Integer       | Both           |
| ndb_blob_write_batch_bytes                | Integer       | Both           |
| ndb_cache_check_time                      | Integer       | Global         |
| ndb_clear_apply_status                    | Boolean       | Global         |
| ndb_data_node_neighbour                   | Integer       | Global         |
| ndb_default_column_format                 | Enumeration   | Global         |
| ndb_default_column_format                 | Enumeration   | Global         |
| ndb_deferred_constraints                  | Integer       | Both           |
| ndb_deferred_constraints                  | Integer       | Both           |
| ndb_distribution                          | Enumeration   | Global         |
| ndb_distribution                          | Enumeration   | Global         |
| ndb_eventbuffer_free_percent              | Integer       | Global         |
| ndb_eventbuffer_max_alloc                 | Integer       | Global         |
| ndb_extra_logging                         | Integer       | Global         |
| ndb_force_send                            | Boolean       | Both           |
| ndb_fully_replicated                      | Boolean       | Both           |
| ndb_index_stat_enable                     | Boolean       | Both           |
| ndb_index_stat_option                     | String        | Both           |
| ndb_join_pushdown                         | Boolean       | Both           |
| ndb_log_binlog_index                      | Boolean       | Global         |
| ndb_log_empty_epochs                      | Boolean       | Global         |
| ndb_log_empty_epochs                      | Boolean       | Global         |
| ndb_log_empty_update                      | Boolean       | Global         |
| ndb_log_empty_update                      | Boolean       | Global         |
| ndb_log_exclusive_reads                   | Boolean       | Both           |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| ndb_log_exclusive_reads                      | Boolean       | Both           |
| ndb_log_update_as_write                      | Boolean       | Global         |
| ndb_log_update_minimal                       | Boolean       | Global         |
| ndb_log_updated_only                         | Boolean       | Global         |
| ndb_optimization_delay                       | Integer       | Global         |
| ndb_optimized_node_selection                 | Integer       | Global         |
| ndb_read_backup                              | Boolean       | Global         |
| ndb_recv_thread_activation_threshold Integer |               | Global         |
| ndb_recv_thread_cpu_mask                     | Bitmap        | Global         |
| ndb_report_thresh_binlog_epoch_slip Integer  |               | Global         |
| ndb_report_thresh_binlog_mem_usage Integer   |               | Global         |
| ndb_row_checksum                             | Integer       | Both           |
| ndb_show_foreign_key_mock_tables Boolean     |               | Global         |
| ndb_slave_conflict_role                      | Enumeration   | Global         |
| ndb_table_no_logging                         | Boolean       | Session        |
| ndb_table_temporary                          | Boolean       | Session        |
| ndb_use_exact_count                          | Boolean       | Both           |
| ndb_use_transactions                         | Boolean       | Both           |
| ndbinfo_max_bytes                            | Integer       | Both           |
| ndbinfo_max_rows                             | Integer       | Both           |
| ndbinfo_offline                              | Boolean       | Global         |
| ndbinfo_show_hidden                          | Boolean       | Both           |
| net_buffer_length                            | Integer       | Both           |
| net_read_timeout                             | Integer       | Both           |
| net_retry_count                              | Integer       | Both           |
| net_write_timeout                            | Integer       | Both           |
| new                                          | Boolean       | Both           |
| offline_mode                                 | Boolean       | Global         |
| old_alter_table                              | Boolean       | Both           |
| old_passwords                                | Enumeration   | Both           |
| optimizer_prune_level                        | Integer       | Both           |
| optimizer_search_depth                       | Integer       | Both           |
| optimizer_switch                             | Set           | Both           |
| optimizer_trace                              | String        | Both           |
| optimizer_trace_features                     | String        | Both           |
| optimizer_trace_limit                        | Integer       | Both           |
| optimizer_trace_max_mem_size                 | Integer       | Both           |
| optimizer_trace_offset                       | Integer       | Both           |
| parser_max_mem_size                          | Integer       | Both           |
| performance_schema_show_processlist Boolean  |               | Global         |
| preload_buffer_size                          | Integer       | Both           |

| Variable Name                                  | Variable Type | Variable Scope |
|------------------------------------------------|---------------|----------------|
| profiling                                      | Boolean       | Both           |
| profiling_history_size                         | Integer       | Both           |
| pseudo_slave_mode                              | Boolean       | Session        |
| pseudo_thread_id                               | Integer       | Session        |
| query_alloc_block_size                         | Integer       | Both           |
| query_cache_limit                              | Integer       | Global         |
| query_cache_min_res_unit                       | Integer       | Global         |
| query_cache_size                               | Integer       | Global         |
| query_cache_type                               | Enumeration   | Both           |
| query_cache_wlock_invalidate                   | Boolean       | Both           |
| query_prealloc_size                            | Integer       | Both           |
| rand_seed1                                     | Integer       | Session        |
| rand_seed2                                     | Integer       | Session        |
| range_alloc_block_size                         | Integer       | Both           |
| range_optimizer_max_mem_size Integer           |               | Both           |
| rbr_exec_mode                                  | Enumeration   | Session        |
| read_buffer_size                               | Integer       | Both           |
| read_only                                      | Boolean       | Global         |
| read_rnd_buffer_size                           | Integer       | Both           |
| relay_log_info_repository                      | String        | Global         |
| relay_log_purge                                | Boolean       | Global         |
| replication_optimize_for_static_plugin_config  | Boolean       | Global         |
| replication_sender_observe_commit_only Boolean |               | Global         |
| require_secure_transport                       | Boolean       | Global         |
| rewriter_enabled                               | Boolean       | Global         |
| rewriter_verbose                               | Integer       | Global         |
| rpl_semi_sync_master_enabled                   | Boolean       | Global         |
| rpl_semi_sync_master_timeout                   | Integer       | Global         |
| rpl_semi_sync_master_trace_levelInteger        |               | Global         |
| rpl_semi_sync_master_wait_for_slave_count      | Integer       | Global         |
| rpl_semi_sync_master_wait_no_slave Boolean     |               | Global         |
| rpl_semi_sync_master_wait_point Enumeration    |               | Global         |
| rpl_semi_sync_slave_enabled                    | Boolean       | Global         |
| rpl_semi_sync_slave_trace_level Integer        |               | Global         |
| rpl_stop_slave_timeout                         | Integer       | Global         |
| secure_auth                                    | Boolean       | Global         |
| server_id                                      | Integer       | Global         |
| session_track_gtids                            | Enumeration   | Both           |
| session_track_schema                           | Boolean       | Both           |
| session_track_state_change                     | Boolean       | Both           |
| session_track_system_variables                 | String        | Both           |

| Variable Name                  | Variable Type | Variable Scope |
|--------------------------------|---------------|----------------|
| session_track_transaction_info | Enumeration   | Both           |
| sha256_password_proxy_users    | Boolean       | Global         |
| show_compatibility_56          | Boolean       | Global         |
| show_create_table_verbosity    | Boolean       | Both           |
| show_old_temporals             | Boolean       | Both           |
| slave_allow_batching           | Boolean       | Global         |
| slave_checkpoint_group         | Integer       | Global         |
| slave_checkpoint_period        | Integer       | Global         |
| slave_compressed_protocol      | Boolean       | Global         |
| slave_exec_mode                | Enumeration   | Global         |
| slave_max_allowed_packet       | Integer       | Global         |
| slave_net_timeout              | Integer       | Global         |
| slave_parallel_type            | Enumeration   | Global         |
| slave_parallel_workers         | Integer       | Global         |
| slave_pending_jobs_size_max    | Integer       | Global         |
| slave_preserve_commit_order    | Boolean       | Global         |
| slave_rows_search_algorithms   | Set           | Global         |
| slave_sql_verify_checksum      | Boolean       | Global         |
| slave_transaction_retries      | Integer       | Global         |
| slave_type_conversions         | Set           | Global         |
| slow_launch_time               | Integer       | Global         |
| slow_query_log                 | Boolean       | Global         |
| slow_query_log_file            | File name     | Global         |
| sort_buffer_size               | Integer       | Both           |
| sql_auto_is_null               | Boolean       | Both           |
| sql_big_selects                | Boolean       | Both           |
| sql_buffer_result              | Boolean       | Both           |
| sql_log_bin                    | Boolean       | Session        |
| sql_log_off                    | Boolean       | Both           |
| sql_mode                       | Set           | Both           |
| sql_notes                      | Boolean       | Both           |
| sql_quote_show_create          | Boolean       | Both           |
| sql_safe_updates               | Boolean       | Both           |
| sql_select_limit               | Integer       | Both           |
| sql_slave_skip_counter         | Integer       | Global         |
| sql_warnings                   | Boolean       | Both           |
| stored_program_cache           | Integer       | Global         |
| super_read_only                | Boolean       | Global         |
| sync_binlog                    | Integer       | Global         |
| sync_frm                       | Boolean       | Global         |
| sync_master_info               | Integer       | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| sync_relay_log                               | Integer       | Global         |
| sync_relay_log_info                          | Integer       | Global         |
| table_definition_cache                       | Integer       | Global         |
| table_open_cache                             | Integer       | Global         |
| thread_cache_size                            | Integer       | Global         |
| thread_pool_high_priority_connection Integer |               | Both           |
| thread_pool_max_unused_threads               |               | Global         |
| thread_pool_prio_kickup_timer                |               | Global         |
| thread_pool_stall_limit                      | Integer       | Global         |
| time_zone                                    | String        | Both           |
| timestamp                                    | Numeric       | Session        |
| tmp_table_size                               | Integer       | Both           |
| transaction_alloc_block_size                 | Integer       | Both           |
| transaction_allow_batching                   | Boolean       | Session        |
| transaction_isolation                        | Enumeration   | Both           |
| transaction_prealloc_size                    | Integer       | Both           |
| transaction_read_only                        | Boolean       | Both           |
| transaction_write_set_extraction             | Enumeration   | Both           |
| tx_isolation                                 | Enumeration   | Both           |
| tx_read_only                                 | Boolean       | Both           |
| unique_checks                                | Boolean       | Both           |
| updatable_views_with_limit                   | Boolean       | Both           |
| validate_password_check_user_name Boolean    |               | Global         |
| validate_password_dictionary_file File name  |               | Global         |
| validate_password_length                     | Integer       | Global         |
| validate_password_mixed_case_count Integer   |               | Global         |
| validate_password_number_countInteger        |               | Global         |
| validate_password_policy                     | Enumeration   | Global         |
| validate_password_special_char_count Integer |               | Global         |
| version_tokens_session                       | String        | Both           |
| wait_timeout                                 | Integer       | Both           |