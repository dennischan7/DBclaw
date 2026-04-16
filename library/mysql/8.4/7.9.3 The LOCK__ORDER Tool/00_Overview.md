---
source: MySQL 8.4 Reference
title: 00_Overview
---

The MySQL server is a multithreaded application that uses numerous internal locking and lock-related primitives, such as mutexes, rwlocks (including prlocks and sxlocks), conditions, and files. Within the server, the set of lock-related objects changes with implementation of new features and code refactoring for performance improvements. As with any multithreaded application that uses locking primitives, there is always a risk of encountering a deadlock during execution when multiple locks are held at once. For MySQL, the effect of a deadlock is catastrophic, causing a complete loss of service.

To enable detection of lock-acquisition deadlocks and enforcement that runtime execution is free of them, MySQL supports LOCK\_ORDER tooling. This enables a lock-order dependency graph to be defined as part of server design, and server runtime checking to ensure that lock acquisition is acyclic and that execution paths comply with the graph.

This section provides information about using the LOCK\_ORDER tool, but only at a basic level. For complete details, see the Lock Order section of the MySQL Server Doxygen documentation, available at<https://dev.mysql.com/doc/index-other.html>.

The LOCK\_ORDER tool is intended for debugging the server, not for production use.

To use the LOCK\_ORDER tool, follow this procedure:

1. Build MySQL from source, configuring it with the -DWITH\_LOCK\_ORDER=ON CMake option so that the build includes LOCK\_ORDER tooling.

![](_page_145_Picture_9.jpeg)

#### **Note**

With the WITH\_LOCK\_ORDER option enabled, MySQL builds require the flex program.

- 2. To run the server with the LOCK\_ORDER tool enabled, enable the [lock\\_order](#page-146-0) system variable at server startup. Several other system variables for LOCK\_ORDER configuration are available as well.
- 3. For MySQL test suite operation, mysql-test-run.pl has a --lock-order option that controls whether to enable the LOCK\_ORDER tool during test case execution.

The system variables described following configure operation of the LOCK\_ORDER tool, assuming that MySQL has been built to include LOCK\_ORDER tooling. The primary variable is [lock\\_order](#page-146-0), which indicates whether to enable the LOCK\_ORDER tool at runtime:

- If [lock\\_order](#page-146-0) is disabled (the default), no other LOCK\_ORDER system variables have any effect.
- If [lock\\_order](#page-146-0) is enabled, the other system variables configure which LOCK\_ORDER features to enable.

![](_page_145_Picture_17.jpeg)

#### **Note**

In general, it is intended that the LOCK\_ORDER tool be configured by executing mysql-test-run.pl with the --lock-order option, and for mysql-testrun.pl to set LOCK\_ORDER system variables to appropriate values.

All LOCK\_ORDER system variables must be set at server startup. At runtime, their values are visible but cannot be changed.

Some system variables exist in pairs, such as [lock\\_order\\_debug\\_loop](#page-146-1) and [lock\\_order\\_trace\\_loop](#page-149-0). For such pairs, the variables are distinguished as follows when the condition occurs with which they are associated:

- If the \_debug\_ variable is enabled, a debug assertion is raised.
- If the \_trace\_ variable is enabled, an error is printed to the logs.

#### **Table 7.8 LOCK\_ORDER System Variable Summary**

| Variable Name                           | Variable Type  | Variable Scope |
|-----------------------------------------|----------------|----------------|
| lock_order                              | Boolean        | Global         |
| lock_order_debug_loop                   | Boolean        | Global         |
| lock_order_debug_missing_arc            | Boolean        | Global         |
| lock_order_debug_missing_key            | Boolean        | Global         |
| lock_order_debug_missing_unlockBoolean  |                | Global         |
| lock_order_dependencies                 | File name      | Global         |
| lock_order_extra_dependencies           | File name      | Global         |
| lock_order_output_directory             | Directory name | Global         |
| lock_order_print_txt                    | Boolean        | Global         |
| lock_order_trace_loop                   | Boolean        | Global         |
| lock_order_trace_missing_arc            | Boolean        | Global         |
| lock_order_trace_missing_key            | Boolean        | Global         |
| lock_order_trace_missing_unlock Boolean |                | Global         |

#### <span id="page-146-0"></span>• [lock\\_order](#page-146-0)

| Command-Line Format  | lock-order[={OFF ON}] |
|----------------------|-----------------------|
| System Variable      | lock_order            |
| Scope                | Global                |
| Dynamic              | No                    |
| SET_VAR Hint Applies | No                    |
| Type                 | Boolean               |
| Default Value        | OFF                   |

Whether to enable the LOCK\_ORDER tool at runtime. If [lock\\_order](#page-146-0) is disabled (the default), no other LOCK\_ORDER system variables have any effect. If [lock\\_order](#page-146-0) is enabled, the other system variables configure which LOCK\_ORDER features to enable.

If [lock\\_order](#page-146-0) is enabled, an error is raised if the server encounters a lock-acquisition sequence that is not declared in the lock-order graph.

#### <span id="page-146-1"></span>• [lock\\_order\\_debug\\_loop](#page-146-1)

| Command-Line Format  | lock-order-debug-loop[={OFF ON}] |
|----------------------|----------------------------------|
| System Variable      | lock_order_debug_loop            |
| Scope                | Global                           |
| Dynamic              | No                               |
| SET_VAR Hint Applies | No                               |
| Type                 | Boolean                          |
| Default Value        | OFF                              |

Whether the LOCK\_ORDER tool causes a debug assertion failure when it encounters a dependency that is flagged as a loop in the lock-order graph.

<span id="page-147-0"></span>• [lock\\_order\\_debug\\_missing\\_arc](#page-147-0)

| Command-Line Format  | lock-order-debug-missing<br>arc[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | lock_order_debug_missing_arc               |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

Whether the LOCK\_ORDER tool causes a debug assertion failure when it encounters a dependency that is not declared in the lock-order graph.

<span id="page-147-1"></span>• [lock\\_order\\_debug\\_missing\\_key](#page-147-1)

| Command-Line Format  | lock-order-debug-missing<br>key[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | lock_order_debug_missing_key               |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

Whether the LOCK\_ORDER tool causes a debug assertion failure when it encounters an object that is not properly instrumented with the Performance Schema.

<span id="page-147-2"></span>• [lock\\_order\\_debug\\_missing\\_unlock](#page-147-2)

| Command-Line Format  | lock-order-debug-missing<br>unlock[={OFF ON}] |
|----------------------|-----------------------------------------------|
| System Variable      | lock_order_debug_missing_unlock               |
| Scope                | Global                                        |
| Dynamic              | No                                            |
| SET_VAR Hint Applies | No                                            |
| Type                 | Boolean                                       |
| Default Value        | OFF                                           |

Whether the LOCK\_ORDER tool causes a debug assertion failure when it encounters a lock that is destroyed while still held.

<span id="page-147-3"></span>• [lock\\_order\\_dependencies](#page-147-3)

| Command-Line Format  | lock-order-dependencies=file_name |
|----------------------|-----------------------------------|
| System Variable      | lock_order_dependencies           |
| Scope                | Global                            |
| Dynamic              | No                                |
| SET_VAR Hint Applies | No                                |
| Type                 | File name                         |

| Default Value | empty string |
|---------------|--------------|
|---------------|--------------|

The path to the lock\_order\_dependencies.txt file that defines the server lock-order dependency graph.

It is permitted to specify no dependencies. An empty dependency graph is used in this case.

<span id="page-148-0"></span>• [lock\\_order\\_extra\\_dependencies](#page-148-0)

| Command-Line Format  | lock-order-extra<br>dependencies=file_name |
|----------------------|--------------------------------------------|
| System Variable      | lock_order_extra_dependencies              |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | File name                                  |
| Default Value        | empty string                               |

The path to a file containing additional dependencies for the lock-order dependency graph. This is useful to amend the primary server dependency graph, defined in the lock\_order\_dependencies.txt file, with additional dependencies describing the behavior of third party code. (The alternative is to modify lock\_order\_dependencies.txt itself, which is not encouraged.)

If this variable is not set, no secondary file is used.

<span id="page-148-1"></span>• [lock\\_order\\_output\\_directory](#page-148-1)

| Command-Line Format  | lock-order-output<br>directory=dir_name |
|----------------------|-----------------------------------------|
|                      |                                         |
| System Variable      | lock_order_output_directory             |
| Scope                | Global                                  |
| Dynamic              | No                                      |
| SET_VAR Hint Applies | No                                      |
| Type                 | Directory name                          |
| Default Value        | empty string                            |

The directory where the LOCK\_ORDER tool writes its logs. If this variable is not set, the default is the current directory.

<span id="page-148-2"></span>• [lock\\_order\\_print\\_txt](#page-148-2)

| Command-Line Format  | lock-order-print-txt[={OFF ON}] |
|----------------------|---------------------------------|
| System Variable      | lock_order_print_txt            |
| Scope                | Global                          |
| Dynamic              | No                              |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |
| Default Value        | OFF                             |

Whether the LOCK\_ORDER tool performs a lock-order graph analysis and prints a textual report. The report includes any lock-acquisition cycles detected.

<span id="page-149-0"></span>• [lock\\_order\\_trace\\_loop](#page-149-0)

| Command-Line Format  | lock-order-trace-loop[={OFF ON}] |
|----------------------|----------------------------------|
| System Variable      | lock_order_trace_loop            |
| Scope                | Global                           |
| Dynamic              | No                               |
| SET_VAR Hint Applies | No                               |
| Type                 | Boolean                          |
| Default Value        | OFF                              |

Whether the LOCK\_ORDER tool prints a trace in the log file when it encounters a dependency that is flagged as a loop in the lock-order graph.

<span id="page-149-1"></span>• [lock\\_order\\_trace\\_missing\\_arc](#page-149-1)

| Command-Line Format  | lock-order-trace-missing<br>arc[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | lock_order_trace_missing_arc               |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | ON                                         |

Whether the LOCK\_ORDER tool prints a trace in the log file when it encounters a dependency that is not declared in the lock-order graph.

<span id="page-149-2"></span>• [lock\\_order\\_trace\\_missing\\_key](#page-149-2)

| Command-Line Format  | lock-order-trace-missing<br>key[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | lock_order_trace_missing_key               |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

Whether the LOCK\_ORDER tool prints a trace in the log file when it encounters an object that is not properly instrumented with the Performance Schema.

<span id="page-149-3"></span>• [lock\\_order\\_trace\\_missing\\_unlock](#page-149-3)

| Command-Line Format  | lock-order-trace-missing<br>unlock[={OFF ON}] |
|----------------------|-----------------------------------------------|
| System Variable      | lock_order_trace_missing_unlock               |
| Scope                | Global                                        |
| Dynamic              | No                                            |
| SET_VAR Hint Applies | No                                            |
| Type                 | Boolean                                       |

| Default Value | ON |
|---------------|----|
|---------------|----|

Whether the LOCK\_ORDER tool prints a trace in the log file when it encounters a lock that is destroyed while still held.

# <span id="page-150-0"></span>**7.9.4 The DBUG Package**

The MySQL server and most MySQL clients are compiled with the DBUG package originally created by Fred Fish. When you have configured MySQL for debugging, this package makes it possible to get a trace file of what the program is doing. See [Section 7.9.1.2, "Creating Trace Files".](#page-140-0)

This section summarizes the argument values that you can specify in debug options on the command line for MySQL programs that have been built with debugging support.

The DBUG package can be used by invoking a program with the --debug[=debug\_options] or -# [debug\_options] option. If you specify the --debug or -# option without a debug\_options value, most MySQL programs use a default value. The server default is d:t:i:o,/tmp/mysqld.trace on Unix and d:t:i:O,\mysqld.trace on Windows. The effect of this default is:

- d: Enable output for all debug macros
- t: Trace function calls and exits
- i: Add PID to output lines
- o,/tmp/mysqld.trace, O,\mysqld.trace: Set the debug output file.

Most client programs use a default debug\_options value of d:t:o,/tmp/program\_name.trace, regardless of platform.

Here are some example debug control strings as they might be specified on a shell command line:

```
--debug=d:t
--debug=d:f,main,subr1:F:L:t,20
--debug=d,input,output,files:n
--debug=d:t:i:O,\\mysqld.trace
```

For mysqld, it is also possible to change DBUG settings at runtime by setting the debug system variable. This variable has global and session values:

```
mysql> SET GLOBAL debug = 'debug_options';
mysql> SET SESSION debug = 'debug_options';
```

Changing the global debug value requires privileges sufficient to set global system variables. Changing the session debug value requires privileges sufficient to set restricted session system variables. See Section 7.1.9.1, "System Variable Privileges".

The debug\_options value is a sequence of colon-separated fields:

```
field_1:field_2:...:field_N
```

Each field within the value consists of a mandatory flag character, optionally preceded by a + or character, and optionally followed by a comma-separated list of modifiers:

```
[+|-]flag[,modifier,modifier,...,modifier]
```

The following table describes the permitted flag characters. Unrecognized flag characters are silently ignored.

| Flag | Description                                     |
|------|-------------------------------------------------|
| d    | Enable output from DBUG_XXX macros for          |
|      | the current state. May be followed by a list of |
|      | keywords, which enables output only for the     |

| Flag | Description                                                                                                                                                                                                                                                      |
|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      | DBUG macros with that keyword. An empty list of<br>keywords enables output for all macros.                                                                                                                                                                       |
|      | In MySQL, common debug macro keywords to<br>enable are enter, exit, error, warning,<br>info, and loop.                                                                                                                                                           |
| D    | Delay after each debugger output line. The<br>argument is the delay, in tenths of seconds,<br>subject to machine capabilities. For example,<br>D,20 specifies a delay of two seconds.                                                                            |
| f    | Limit debugging, tracing, and profiling to the list<br>of named functions. An empty list enables all<br>functions. The appropriate d or t flags must still<br>be given; this flag only limits their actions if they<br>are enabled.                              |
| F    | Identify the source file name for each line of debug<br>or trace output.                                                                                                                                                                                         |
| i    | Identify the process with the PID or thread ID for<br>each line of debug or trace output.                                                                                                                                                                        |
| L    | Identify the source file line number for each line of<br>debug or trace output.                                                                                                                                                                                  |
| n    | Print the current function nesting depth for each<br>line of debug or trace output.                                                                                                                                                                              |
| N    | Number each line of debug output.                                                                                                                                                                                                                                |
| o    | Redirect the debugger output stream to the<br>specified file. The default output is stderr.                                                                                                                                                                      |
| O    | Like o, but the file is really flushed between<br>each write. When needed, the file is closed and<br>reopened between each write.                                                                                                                                |
| a    | Like o, but opens for append.                                                                                                                                                                                                                                    |
| A    | Like O, but opens for append.                                                                                                                                                                                                                                    |
| p    | Limit debugger actions to specified processes.<br>A process must be identified with the<br>DBUG_PROCESS macro and match one in the list<br>for debugger actions to occur.                                                                                        |
| P    | Print the current process name for each line of<br>debug or trace output.                                                                                                                                                                                        |
| r    | When pushing a new state, do not inherit the<br>previous state's function nesting level. Useful<br>when the output is to start at the left margin.                                                                                                               |
| t    | Enable function call/exit trace lines. May be<br>followed by a list (containing only one modifier)<br>giving a numeric maximum trace level, beyond<br>which no output occurs for either debugging or<br>tracing macros. The default is a compile time<br>option. |
| T    | Print the current timestamp for every line of<br>output.                                                                                                                                                                                                         |

The leading + or - character and trailing list of modifiers are used for flag characters such as d or f that can enable a debug operation for all applicable modifiers or just some of them:

- With no leading + or -, the flag value is set to exactly the modifier list as given.
- With a leading + or -, the modifiers in the list are added to or subtracted from the current modifier list.

The following examples show how this works for the d flag. An empty d list enabled output for all debug macros. A nonempty list enables output only for the macro keywords in the list.

These statements set the d value to the modifier list as given:

```
mysql> SET debug = 'd';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| d |
+---------+
mysql> SET debug = 'd,error,warning';
mysql> SELECT @@debug;
+-----------------+
| @@debug |
+-----------------+
| d,error,warning |
+-----------------+
```

A leading + or - adds to or subtracts from the current d value:

```
mysql> SET debug = '+d,loop';
mysql> SELECT @@debug;
+----------------------+
| @@debug |
+----------------------+
| d,error,warning,loop |
+----------------------+
mysql> SET debug = '-d,error,loop';
mysql> SELECT @@debug;
+-----------+
| @@debug |
+-----------+
| d,warning |
+-----------+
```

Adding to "all macros enabled" results in no change:

```
mysql> SET debug = 'd';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| d |
+---------+
mysql> SET debug = '+d,loop';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| d |
+---------+
```

Disabling all enabled macros disables the d flag entirely:

```
mysql> SET debug = 'd,error,loop';
mysql> SELECT @@debug;
+--------------+
| @@debug |
+--------------+
| d,error,loop |
+--------------+
```

```
mysql> SET debug = '-d,error,loop';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| |
+---------+
```

# Chapter 8 Security

# **Table of Contents**

| 8.1 General Security Issues 1126                                          |      |
|---------------------------------------------------------------------------|------|
| 8.1.1 Security Guidelines 1126                                            |      |
| 8.1.2 Keeping Passwords Secure 1128                                       |      |
| 8.1.3 Making MySQL Secure Against Attackers 1131                          |      |
| 8.1.4 Security-Related mysqld Options and Variables 1132                  |      |
| 8.1.5 How to Run MySQL as a Normal User 1133                              |      |
| 8.1.6 Security Considerations for LOAD DATA LOCAL 1134                    |      |
| 8.1.7 Client Programming Security Guidelines 1137                         |      |
| 8.2 Access Control and Account Management 1139                            |      |
| 8.2.1 Account User Names and Passwords 1140                               |      |
| 8.2.2 Privileges Provided by MySQL 1141                                   |      |
| 8.2.3 Grant Tables 1161                                                   |      |
| 8.2.4 Specifying Account Names                                            | 1170 |
| 8.2.5 Specifying Role Names 1172                                          |      |
| 8.2.6 Access Control, Stage 1: Connection Verification 1173               |      |
| 8.2.7 Access Control, Stage 2: Request Verification 1176                  |      |
| 8.2.8 Adding Accounts, Assigning Privileges, and Dropping Accounts 1178   |      |
| 8.2.9 Reserved Accounts 1181                                              |      |
| 8.2.10 Using Roles 1181                                                   |      |
|                                                                           |      |
| 8.2.11 Account Categories 1188                                            |      |
| 8.2.12 Privilege Restriction Using Partial Revokes 1191                   |      |
| 8.2.13 When Privilege Changes Take Effect 1197                            |      |
| 8.2.14 Assigning Account Passwords 1198                                   |      |
| 8.2.15 Password Management 1199                                           |      |
| 8.2.16 Server Handling of Expired Passwords 1210                          |      |
| 8.2.17 Pluggable Authentication 1212                                      |      |
| 8.2.18 Multifactor Authentication 1218                                    |      |
| 8.2.19 Proxy Users                                                        | 1221 |
| 8.2.20 Account Locking 1229                                               |      |
| 8.2.21 Setting Account Resource Limits 1229                               |      |
| 8.2.22 Troubleshooting Problems Connecting to MySQL 1231                  |      |
| 8.2.23 SQL-Based Account Activity Auditing 1235                           |      |
| 8.3 Using Encrypted Connections 1237                                      |      |
| 8.3.1 Configuring MySQL to Use Encrypted Connections 1238                 |      |
| 8.3.2 Encrypted Connection TLS Protocols and Ciphers 1246                 |      |
| 8.3.3 Creating SSL and RSA Certificates and Keys 1252                     |      |
| 8.3.4 Connecting to MySQL Remotely from Windows with SSH 1260             |      |
| 8.3.5 Reusing SSL Sessions 1261                                           |      |
| 8.4 Security Components and Plugins 1263                                  |      |
| 8.4.1 Authentication Plugins 1264                                         |      |
| 8.4.2 Connection Control Plugins 1357                                     |      |
| 8.4.3 The Password Validation Component 1363                              |      |
| 8.4.4 The MySQL Keyring 1375                                              |      |
| 8.4.5 MySQL Enterprise Audit                                              | 1434 |
| 8.4.6 The Audit Message Component 1517                                    |      |
| 8.4.7 MySQL Enterprise Firewall 1520                                      |      |
| 8.5 MySQL Enterprise Data Masking and De-Identification 1549              |      |
| 8.5.1 Data-Masking Components Versus the Data-Masking Plugin 1551         |      |
| 8.5.2 MySQL Enterprise Data Masking and De-Identification Components 1551 |      |
| 8.5.3 MySQL Enterprise Data Masking and De-Identification Plugin 1577     |      |
| 8.6 MySQL Enterprise Encryption 1593                                      |      |
| 8.6.1 MySQL Enterprise Encryption Installation and Upgrading 1594         |      |
|                                                                           |      |

| 8.6.2 Configuring MySQL Enterprise Encryption                          | 1595 |
|------------------------------------------------------------------------|------|
| 8.6.3 MySQL Enterprise Encryption Usage and Examples 1595              |      |
| 8.6.4 MySQL Enterprise Encryption Function Reference 1597              |      |
| 8.6.5 MySQL Enterprise Encryption Component Function Descriptions 1597 |      |
| 8.7 SELinux 1601                                                       |      |
| 8.7.1 Check if SELinux is Enabled 1602                                 |      |
| 8.7.2 Changing the SELinux Mode 1602                                   |      |
| 8.7.3 MySQL Server SELinux Policies 1602                               |      |
| 8.7.4 SELinux File Context 1603                                        |      |
| 8.7.5 SELinux TCP Port Context 1604                                    |      |
| 8.7.6 Troubleshooting SELinux 1605                                     |      |
| 8.8 FIPS Support 1606                                                  |      |
|                                                                        |      |

When thinking about security within a MySQL installation, you should consider a wide range of possible topics and how they affect the security of your MySQL server and related applications:

- General factors that affect security. These include choosing good passwords, not granting unnecessary privileges to users, ensuring application security by preventing SQL injections and data corruption, and others. See [Section 8.1, "General Security Issues".](#page-155-0)
- Security of the installation itself. The data files, log files, and the all the application files of your installation should be protected to ensure that they are not readable or writable by unauthorized parties. For more information, see Section 2.9, "Postinstallation Setup and Testing".
- Access control and security within the database system itself, including the users and databases granted with access to the databases, views and stored programs in use within the database. For more information, see [Section 8.2, "Access Control and Account Management"](#page-168-0).
- The features offered by security-related plugins. See Section 8.4, "Security Components and Plugins".
- Network security of MySQL and your system. The security is related to the grants for individual users, but you may also wish to restrict MySQL so that it is available only locally on the MySQL server host, or to a limited set of other hosts.
- Ensure that you have adequate and appropriate backups of your database files, configuration and log files. Also be sure that you have a recovery solution in place and test that you are able to successfully recover the information from your backups. See Chapter 9, Backup and Recovery.

![](_page_155_Picture_9.jpeg)

# **Note**

Several topics in this chapter are also addressed in the [Secure Deployment](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/) [Guide,](https://dev.mysql.com/doc/mysql-secure-deployment-guide/en/) which provides procedures for deploying a generic binary distribution of MySQL Enterprise Edition Server with features for managing the security of your MySQL installation.

# <span id="page-155-0"></span>**8.1 General Security Issues**

This section describes general security issues to be aware of and what you can do to make your MySQL installation more secure against attack or misuse. For information specifically about the access control system that MySQL uses for setting up user accounts and checking database access, see Section 2.9, "Postinstallation Setup and Testing".

For answers to some questions that are often asked about MySQL Server security issues, see Section A.9, "MySQL 8.4 FAQ: Security".

# <span id="page-155-1"></span>**8.1.1 Security Guidelines**

Anyone using MySQL on a computer connected to the Internet should read this section to avoid the most common security mistakes.

In discussing security, it is necessary to consider fully protecting the entire server host (not just the MySQL server) against all types of applicable attacks: eavesdropping, altering, playback, and denial of service. We do not cover all aspects of availability and fault tolerance here.

MySQL uses security based on Access Control Lists (ACLs) for all connections, queries, and other operations that users can attempt to perform. There is also support for SSL-encrypted connections between MySQL clients and servers. Many of the concepts discussed here are not specific to MySQL at all; the same general ideas apply to almost all applications.

When running MySQL, follow these guidelines:

- **Do not ever give anyone (except MySQL root accounts) access to the user table in the mysql system database!** This is critical.
- Learn how the MySQL access privilege system works (see [Section 8.2, "Access Control and Account](#page-168-0) [Management"\)](#page-168-0). Use the GRANT and REVOKE statements to control access to MySQL. Do not grant more privileges than necessary. Never grant privileges to all hosts.

### Checklist:

- Try mysql -u root. If you are able to connect successfully to the server without being asked for a password, anyone can connect to your MySQL server as the MySQL root user with full privileges! Review the MySQL installation instructions, paying particular attention to the information about setting a root password. See Section 2.9.4, "Securing the Initial MySQL Account".
- Use the SHOW GRANTS statement to check which accounts have access to what. Then use the REVOKE statement to remove those privileges that are not necessary.
- Do not store cleartext passwords in your database. If your computer becomes compromised, the intruder can take the full list of passwords and use them. Instead, use SHA2() or some other oneway hashing function and store the hash value.

To prevent password recovery using rainbow tables, do not use these functions on a plain password; instead, choose some string to be used as a salt, and use hash(hash(password)+salt) values.

• Assume that all passwords will be subject to automated cracking attempts using lists of known passwords, and also to targeted guessing using publicly available information about you, such as social media posts. Do not choose passwords that consist of easily cracked or guessed items such as a dictionary word, proper name, sports team name, acronym, or commonly known phrase, particularly if they are relevant to you. The use of upper case letters, number substitutions and additions, and special characters does not help if these are used in predictable ways. Also do not choose any password you have seen used as an example anywhere, or a variation on it, even if it was presented as an example of a strong password.

Instead, choose passwords that are as long and as unpredictable as possible. That does not mean the combination needs to be a random string of characters that is difficult to remember and reproduce, although this is a good approach if you have, for example, password manager software that can generate and fill such passwords and store them securely. A passphrase containing multiple words is easy to create, remember, and reproduce, and is much more secure than a typical userselected password consisting of a single modified word or a predictable sequence of characters. To create a secure passphrase, ensure that the words and other items in it are not a known phrase or quotation, do not occur in a predictable order, and preferably have no previous relationship to each other at all.

• Invest in a firewall. This protects you from at least 50% of all types of exploits in any software. Put MySQL behind the firewall or in a demilitarized zone (DMZ).

#### Checklist:

• Try to scan your ports from the Internet using a tool such as nmap. MySQL uses port 3306 by default. This port should not be accessible from untrusted hosts. As a simple way to check whether your MySQL port is open, try the following command from some remote machine, where server\_host is the host name or IP address of the host on which your MySQL server runs:

```
$> telnet server_host 3306
```

If telnet hangs or the connection is refused, the port is blocked, which is how you want it to be. If you get a connection and some garbage characters, the port is open, and should be closed on your firewall or router, unless you really have a good reason to keep it open.

- Applications that access MySQL should not trust any data entered by users, and should be written using proper defensive programming techniques. See [Section 8.1.7, "Client Programming Security](#page-166-0) [Guidelines".](#page-166-0)
- Do not transmit plain (unencrypted) data over the Internet. This information is accessible to everyone who has the time and ability to intercept it and use it for their own purposes. Instead, use an encrypted protocol such as SSL or SSH. MySQL supports internal SSL connections. Another technique is to use SSH port-forwarding to create an encrypted (and compressed) tunnel for the communication.
- Learn to use the tcpdump and strings utilities. In most cases, you can check whether MySQL data streams are unencrypted by issuing a command like the following:

```
$> tcpdump -l -i eth0 -w - src or dst port 3306 | strings
```

This works under Linux and should work with small modifications under other systems.

![](_page_157_Picture_9.jpeg)

#### **Warning**

If you do not see cleartext data, this does not always mean that the information actually is encrypted. If you need high security, consult with a security expert.

# <span id="page-157-0"></span>**8.1.2 Keeping Passwords Secure**

Passwords occur in several contexts within MySQL. The following sections provide guidelines that enable end users and administrators to keep these passwords secure and avoid exposing them. In addition, the validate\_password plugin can be used to enforce a policy on acceptable password. See Section 8.4.3, "The Password Validation Component".

## <span id="page-157-1"></span>**8.1.2.1 End-User Guidelines for Password Security**

MySQL users should use the following guidelines to keep passwords secure.

When you run a client program to connect to the MySQL server, it is inadvisable to specify your password in a way that exposes it to discovery by other users. The methods you can use to specify your password when you run client programs are listed here, along with an assessment of the risks of each method. In short, the safest methods are to have the client program prompt for the password or to specify the password in a properly protected option file.

- Use the mysql\_config\_editor utility, which enables you to store authentication credentials in an encrypted login path file named .mylogin.cnf. The file can be read later by MySQL client programs to obtain authentication credentials for connecting to MySQL Server. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".
- Use a --password=password or -ppassword option on the command line. For example:

\$> **mysql -u francis -pfrank db\_name**

![](_page_157_Picture_20.jpeg)

#### **Warning**

This is convenient but insecure. On some systems, your password becomes visible to system status programs such as ps that may be invoked by

other users to display command lines. MySQL clients typically overwrite the command-line password argument with zeros during their initialization sequence. However, there is still a brief interval during which the value is visible. Also, on some systems this overwriting strategy is ineffective and the password remains visible to ps. (SystemV Unix systems and perhaps others are subject to this problem.)

If your operating environment is set up to display your current command in the title bar of your terminal window, the password remains visible as long as the command is running, even if the command has scrolled out of view in the window content area.

• Use the --password or -p option on the command line with no password value specified. In this case, the client program solicits the password interactively:

```
$> mysql -u francis -p db_name
Enter password: ********
```

The \* characters indicate where you enter your password. The password is not displayed as you enter it.

It is more secure to enter your password this way than to specify it on the command line because it is not visible to other users. However, this method of entering a password is suitable only for programs that you run interactively. If you want to invoke a client from a script that runs noninteractively, there is no opportunity to enter the password from the keyboard. On some systems, you may even find that the first line of your script is read and interpreted (incorrectly) as your password.

• Store your password in an option file. For example, on Unix, you can list your password in the [client] section of the .my.cnf file in your home directory:

```
[client]
password=password
```

To keep the password safe, the file should not be accessible to anyone but yourself. To ensure this, set the file access mode to 400 or 600. For example:

```
$> chmod 600 .my.cnf
```

To name from the command line a specific option file containing the password, use the - defaults-file=file\_name option, where file\_name is the full path name to the file. For example:

```
$> mysql --defaults-file=/home/francis/mysql-opts
```

Section 6.2.2.2, "Using Option Files", discusses option files in more detail.

On Unix, the mysql client writes a record of executed statements to a history file (see Section 6.5.1.3, "mysql Client Logging"). By default, this file is named .mysql\_history and is created in your home directory. Passwords can be written as plain text in SQL statements such as CREATE USER and ALTER USER, so if you use these statements, they are logged in the history file. To keep this file safe, use a restrictive access mode, the same way as described earlier for the .my.cnf file.

If your command interpreter maintains a history, any file in which the commands are saved contains MySQL passwords entered on the command line. For example, bash uses ~/.bash\_history. Any such file should have a restrictive access mode.