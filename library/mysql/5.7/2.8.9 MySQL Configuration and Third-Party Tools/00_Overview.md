---
source: MySQL 5.7 Reference
title: 00_Overview
---

Third-party tools that need to determine the MySQL version from the MySQL source can read the VERSION file in the top-level source directory. The file lists the pieces of the version separately. For example, if the version is MySQL 5.7.4-m14, the file looks like this:

```
MYSQL_VERSION_MAJOR=5
MYSQL_VERSION_MINOR=7
```

```
MYSQL_VERSION_PATCH=4
MYSQL_VERSION_EXTRA=-m14
```

If the source is not for a MySQL Server General Availablility (GA) release, the MYSQL\_VERSION\_EXTRA value is nonempty. In the preceding example, the value corresponds to Milestone 14.

MYSQL\_VERSION\_EXTRA is also nonempty for NDB Cluster releases (including GA releases of NDB Cluster), as shown here:

```
MYSQL_VERSION_MAJOR=5
MYSQL_VERSION_MINOR=7
MYSQL_VERSION_PATCH=32
MYSQL_VERSION_EXTRA=-ndb-7.5.21
```

To construct a five-digit number from the version components, use this formula:

```
MYSQL_VERSION_MAJOR*10000 + MYSQL_VERSION_MINOR*100 + MYSQL_VERSION_PATCH
```

# <span id="page-32-0"></span>**2.9 Postinstallation Setup and Testing**

This section discusses tasks that you should perform after installing MySQL:

- If necessary, initialize the data directory and create the MySQL grant tables. For some MySQL installation methods, data directory initialization may be done for you automatically:
  - Windows installation operations performed by MySQL Installer.
  - Installation on Linux using a server RPM or Debian distribution from Oracle.
  - Installation using the native packaging system on many platforms, including Debian Linux, Ubuntu Linux, Gentoo Linux, and others.
  - Installation on macOS using a DMG distribution.

For other platforms and installation types, you must initialize the data directory manually. These include installation from generic binary and source distributions on Unix and Unix-like system, and installation from a ZIP Archive package on Windows. For instructions, see [Section 2.9.1, "Initializing](#page-32-1) [the Data Directory".](#page-32-1)

- Start the server and make sure that it can be accessed. For instructions, see [Section 2.9.2, "Starting](#page-38-0) [the Server"](#page-38-0), and [Section 2.9.3, "Testing the Server".](#page-41-0)
- Assign passwords to the initial root account in the grant tables, if that was not already done during data directory initialization. Passwords prevent unauthorized access to the MySQL server. For instructions, see [Section 2.9.4, "Securing the Initial MySQL Account".](#page-42-0)
- Optionally, arrange for the server to start and stop automatically when your system starts and stops. For instructions, see [Section 2.9.5, "Starting and Stopping MySQL Automatically".](#page-44-0)
- Optionally, populate time zone tables to enable recognition of named time zones. For instructions, see Section 5.1.13, "MySQL Server Time Zone Support".

When you are ready to create additional user accounts, you can find information on the MySQL access control system and account management in Section 6.2, "Access Control and Account Management".

# <span id="page-32-1"></span>**2.9.1 Initializing the Data Directory**

After MySQL is installed, the data directory must be initialized, including the tables in the mysql system database:

• For some MySQL installation methods, data directory initialization is automatic, as described in [Section 2.9, "Postinstallation Setup and Testing"](#page-32-0).

• For other installation methods, you must initialize the data directory manually. These include installation from generic binary and source distributions on Unix and Unix-like systems, and installation from a ZIP Archive package on Windows.

This section describes how to initialize the data directory manually for MySQL installation methods for which data directory initialization is not automatic. For some suggested commands that enable testing whether the server is accessible and working properly, see [Section 2.9.3, "Testing the Server".](#page-41-0)

- [Data Directory Initialization Overview](#page-33-0)
- [Data Directory Initialization Procedure](#page-34-0)
- [Server Actions During Data Directory Initialization](#page-36-0)
- [Post-Initialization root Password Assignment](#page-37-0)

## <span id="page-33-0"></span>**Data Directory Initialization Overview**

In the examples shown here, the server is intended to run under the user ID of the mysql login account. Either create the account if it does not exist (see Create a mysql User and Group), or substitute the name of a different existing login account that you plan to use for running the server.

1. Change location to the top-level directory of your MySQL installation, which is typically /usr/ local/mysql (adjust the path name for your system as necessary):

```
cd /usr/local/mysql
```

Within this directory are several files and subdirectories, including the bin subdirectory that contains the server as well as client and utility programs.

2. The secure\_file\_priv system variable limits import and export operations to a specific directory. Create a directory whose location can be specified as the value of that variable:

```
mkdir mysql-files
```

Grant directory user and group ownership to the mysql user and mysql group, and set the directory permissions appropriately:

```
chown mysql:mysql mysql-files
chmod 750 mysql-files
```

3. Use the server to initialize the data directory, including the mysql database containing the initial MySQL grant tables that determine how users are permitted to connect to the server. For example:

```
bin/mysqld --initialize --user=mysql
```

For important information about the command, especially regarding command options you might use, see [Data Directory Initialization Procedure](#page-34-0). For details about how the server performs initialization, see [Server Actions During Data Directory Initialization](#page-36-0).

Typically, data directory initialization need be done only after you first install MySQL. (For upgrades to an existing installation, perform the upgrade procedure instead; see [Section 2.10, "Upgrading](#page-45-0) [MySQL".](#page-45-0)) However, the command that initializes the data directory does not overwrite any existing mysql database tables, so it is safe to run in any circumstances.

![](_page_33_Picture_20.jpeg)

### **Note**

Initialization of the data directory might fail if required system libraries are missing. For example, you might see an error like this:

```
bin/mysqld: error while loading shared libraries:
libnuma.so.1: cannot open shared object file:
No such file or directory
```

If this happens, you must install the missing libraries manually or with your system's package manager. Then retry the data directory initialization command.

4. If you want to deploy the server with automatic support for secure connections, use the [mysql\\_ssl\\_rsa\\_setup](#page-178-0) utility to create default SSL and RSA files:

```
bin/mysql_ssl_rsa_setup
```

For more information, see [Section 4.4.5, "mysql\\_ssl\\_rsa\\_setup — Create SSL/RSA Files".](#page-178-0)

- 5. In the absence of any option files, the server starts with its default settings. (See Section 5.1.2, "Server Configuration Defaults".) To explicitly specify options that the MySQL server should use at startup, put them in an option file such as /etc/my.cnf or /etc/mysql/my.cnf. (See [Section 4.2.2.2, "Using Option Files".](#page-116-0)) For example, you can use an option file to set the secure\_file\_priv system variable.
- 6. To arrange for MySQL to start without manual intervention at system boot time, see [Section 2.9.5,](#page-44-0) ["Starting and Stopping MySQL Automatically"](#page-44-0).
- 7. Data directory initialization creates time zone tables in the mysql database but does not populate them. To do so, use the instructions in Section 5.1.13, "MySQL Server Time Zone Support".

### <span id="page-34-0"></span>**Data Directory Initialization Procedure**

Change location to the top-level directory of your MySQL installation, which is typically /usr/local/ mysql (adjust the path name for your system as necessary):

```
cd /usr/local/mysql
```

To initialize the data directory, invoke [mysqld](#page-144-0) with the --initialize or --initialize-insecure option, depending on whether you want the server to generate a random initial password for the 'root'@'localhost' account, or to create that account with no password:

- Use --initialize for "secure by default" installation (that is, including generation of a random initial root password). In this case, the password is marked as expired and you must choose a new one.
- With --initialize-insecure, no root password is generated. This is insecure; it is assumed that you assign a password to the account in timely fashion before putting the server into production use.

For instructions on assigning a new 'root'@'localhost' password, see [Post-Initialization root](#page-37-0) [Password Assignment.](#page-37-0)

![](_page_34_Picture_15.jpeg)

#### **Note**

The server writes any messages (including any initial password) to its standard error output. This may be redirected to the error log, so look there if you do not see the messages on your screen. For information about the error log, including where it is located, see Section 5.4.2, "The Error Log".

On Windows, use the --console option to direct messages to the console.

On Unix and Unix-like systems, it is important for the database directories and files to be owned by the mysql login account so that the server has read and write access to them when you run it later. To ensure this, start [mysqld](#page-144-0) from the system root account and include the --user option as shown here:

bin/mysqld --initialize --user=mysql

bin/mysqld --initialize-insecure --user=mysql

Alternatively, execute [mysqld](#page-144-0) while logged in as mysql, in which case you can omit the --user option from the command.

On Windows, use one of these commands:

```
bin\mysqld --initialize --console
bin\mysqld --initialize-insecure --console
```

![](_page_35_Picture_5.jpeg)

#### **Note**

Data directory initialization might fail if required system libraries are missing. For example, you might see an error like this:

```
bin/mysqld: error while loading shared libraries:
libnuma.so.1: cannot open shared object file:
No such file or directory
```

If this happens, you must install the missing libraries manually or with your system's package manager. Then retry the data directory initialization command.

It might be necessary to specify other options such as --basedir or --datadir if [mysqld](#page-144-0) cannot identify the correct locations for the installation directory or data directory. For example (enter the command on a single line):

```
bin/mysqld --initialize --user=mysql
 --basedir=/opt/mysql/mysql
 --datadir=/opt/mysql/mysql/data
```

Alternatively, put the relevant option settings in an option file and pass the name of that file to [mysqld](#page-144-0). For Unix and Unix-like systems, suppose that the option file name is /opt/mysql/mysql/etc/ my.cnf. Put these lines in the file:

```
[mysqld]
basedir=/opt/mysql/mysql
datadir=/opt/mysql/mysql/data
```

Then invoke [mysqld](#page-144-0) as follows (enter the command on a single line, with the [--defaults-file](#page-121-0) option first):

```
bin/mysqld --defaults-file=/opt/mysql/mysql/etc/my.cnf
 --initialize --user=mysql
```

On Windows, suppose that C:\my.ini contains these lines:

```
[mysqld]
basedir=C:\\Program Files\\MySQL\\MySQL Server 5.7
datadir=D:\\MySQLdata
```

Then invoke [mysqld](#page-144-0) as follows (again, you should enter the command on a single line, with the [-](#page-121-0) [defaults-file](#page-121-0) option first):

```
bin\mysqld --defaults-file=C:\my.ini
 --initialize --console
```

![](_page_35_Picture_20.jpeg)

#### **Important**

When initializing the data directory, you should not specify any options other than those used for setting directory locations such as --basedir or - datadir, and the --user option if needed. Options to be employed by the MySQL server during normal use can be set when restarting it following

initialization. See the description of the --initialize option for further information.

## <span id="page-36-0"></span>**Server Actions During Data Directory Initialization**

![](_page_36_Picture_3.jpeg)

#### **Note**

The data directory initialization sequence performed by the server does not substitute for the actions performed by [mysql\\_secure\\_installation](#page-173-0) and [mysql\\_ssl\\_rsa\\_setup](#page-178-0). See [Section 4.4.4, "mysql\\_secure\\_installation —](#page-173-0) [Improve MySQL Installation Security"](#page-173-0), and [Section 4.4.5, "mysql\\_ssl\\_rsa\\_setup](#page-178-0) [— Create SSL/RSA Files"](#page-178-0).

When invoked with the --initialize or --initialize-insecure option, [mysqld](#page-144-0) performs the following actions during the data directory initialization sequence:

- 1. The server checks for the existence of the data directory as follows:
  - If no data directory exists, the server creates it.
  - If the data directory exists but is not empty (that is, it contains files or subdirectories), the server exits after producing an error message:

```
[ERROR] --initialize specified but the data directory exists. Aborting.
```

In this case, remove or rename the data directory and try again.

As of MySQL 5.7.11, an existing data directory is permitted to be nonempty if every entry either has a name that begins with a period (.) or is named using an --ignore-db-dir option.

![](_page_36_Picture_13.jpeg)

#### **Note**

Avoid the use of the --ignore-db-dir option, which has been deprecated since MySQL 5.7.16.

- 2. Within the data directory, the server creates the mysql system database and its tables, including the grant tables, time zone tables, and server-side help tables. See Section 5.3, "The mysql System Database".
- 3. The server initializes the system tablespace and related data structures needed to manage InnoDB tables.

![](_page_36_Picture_18.jpeg)

#### **Note**

After [mysqld](#page-144-0) sets up the InnoDB system tablespace, certain changes to tablespace characteristics require setting up a whole new instance. Qualifying changes include the file name of the first file in the system tablespace and the number of undo logs. If you do not want to use the default values, make sure that the settings for the innodb\_data\_file\_path and innodb\_log\_file\_size configuration parameters are in place in the MySQL configuration file before running [mysqld](#page-144-0). Also make sure to specify as necessary other parameters that affect the creation and location of InnoDB files, such as innodb\_data\_home\_dir and innodb\_log\_group\_home\_dir.

If those options are in your configuration file but that file is not in a location that MySQL reads by default, specify the file location using the - defaults-extra-file option when you run [mysqld](#page-144-0).

4. The server creates a 'root'@'localhost' superuser account and other reserved accounts (see Section 6.2.8, "Reserved Accounts"). Some reserved accounts are locked and cannot be used by

clients, but 'root'@'localhost' is intended for administrative use and you should assign it a password.

Server actions with respect to a password for the 'root'@'localhost' account depend on how you invoke it:

• With --initialize but not --initialize-insecure, the server generates a random password, marks it as expired, and writes a message displaying the password:

```
[Warning] A temporary password is generated for root@localhost:
iTag*AfrH5ej
```

• With --initialize-insecure, (either with or without --initialize because - initialize-insecure implies --initialize), the server does not generate a password or mark it expired, and writes a warning message:

```
[Warning] root@localhost is created with an empty password ! Please
consider switching off the --initialize-insecure option.
```

For instructions on assigning a new 'root'@'localhost' password, see [Post-Initialization root](#page-37-0) [Password Assignment.](#page-37-0)

- 5. The server populates the server-side help tables used for the HELP statement (see Section 13.8.3, "HELP Statement"). The server does not populate the time zone tables. To do so manually, see Section 5.1.13, "MySQL Server Time Zone Support".
- 6. If the init\_file system variable was given to name a file of SQL statements, the server executes the statements in the file. This option enables you to perform custom bootstrapping sequences.

When the server operates in bootstrap mode, some functionality is unavailable that limits the statements permitted in the file. These include statements that relate to account management (such as CREATE USER or GRANT), replication, and global transaction identifiers.

7. The server exits.

### <span id="page-37-0"></span>**Post-Initialization root Password Assignment**

After you initialize the data directory by starting the server with --initialize or --initializeinsecure, start the server normally (that is, without either of those options) and assign the 'root'@'localhost' account a new password:

- 1. Start the server. For instructions, see [Section 2.9.2, "Starting the Server".](#page-38-0)
- 2. Connect to the server:
  - If you used --initialize but not --initialize-insecure to initialize the data directory, connect to the server as root:

```
mysql -u root -p
```

Then, at the password prompt, enter the random password that the server generated during the initialization sequence:

```
Enter password: (enter the random root password here)
```

Look in the server error log if you do not know this password.

• If you used --initialize-insecure to initialize the data directory, connect to the server as root without a password:

```
mysql -u root --skip-password
```

3. After connecting, use an ALTER USER statement to assign a new root password:

ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';

See also [Section 2.9.4, "Securing the Initial MySQL Account".](#page-42-0)

![](_page_38_Picture_3.jpeg)

#### **Note**

Attempts to connect to the host 127.0.0.1 normally resolve to the localhost account. However, this fails if the server is run with skip\_name\_resolve enabled. If you plan to do that, make sure that an account exists that can accept a connection. For example, to be able to connect as root using - host=127.0.0.1 or --host=::1, create these accounts:

```
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';
```

It is possible to put those statements in a file to be executed using the init\_file system variable, as discussed in [Server Actions During Data](#page-36-0) [Directory Initialization](#page-36-0).

## <span id="page-38-0"></span>**2.9.2 Starting the Server**

This section describes how start the server on Unix and Unix-like systems. (For Windows, see Section 2.3.4.5, "Starting the Server for the First Time".) For some suggested commands that you can use to test whether the server is accessible and working properly, see [Section 2.9.3, "Testing the](#page-41-0) [Server".](#page-41-0)

Start the MySQL server like this if your installation includes [mysqld\\_safe](#page-144-1):

\$> **bin/mysqld\_safe --user=mysql &**

![](_page_38_Picture_12.jpeg)

#### **Note**

For Linux systems on which MySQL is installed using RPM packages, server startup and shutdown is managed using systemd rather than [mysqld\\_safe](#page-144-1), and [mysqld\\_safe](#page-144-1) is not installed. See Section 2.5.10, "Managing MySQL Server with systemd".

Start the server like this if your installation includes systemd support:

```
$> systemctl start mysqld
```

Substitute the appropriate service name if it differs from mysqld (for example, mysql on SLES systems).

It is important that the MySQL server be run using an unprivileged (non-root) login account. To ensure this, run [mysqld\\_safe](#page-144-1) as root and include the [--user](#page-152-0) option as shown. Otherwise, you should execute the program while logged in as mysql, in which case you can omit the [--user](#page-152-0) option from the command.

For further instructions for running MySQL as an unprivileged user, see Section 6.1.5, "How to Run MySQL as a Normal User".

If the command fails immediately and prints mysqld ended, look for information in the error log (which by default is the host\_name.err file in the data directory).

If the server is unable to access the data directory it starts or read the grant tables in the mysql database, it writes a message to its error log. Such problems can occur if you neglected to create the grant tables by initializing the data directory before proceeding to this step, or if you ran the command that initializes the data directory without the --user option. Remove the data directory and run the command with the --user option.

If you have other problems starting the server, see [Section 2.9.2.1, "Troubleshooting Problems Starting](#page-39-0) [the MySQL Server".](#page-39-0) For more information about [mysqld\\_safe](#page-144-1), see [Section 4.3.2, "mysqld\\_safe](#page-144-1) [— MySQL Server Startup Script"](#page-144-1). For more information about systemd support, see Section 2.5.10, "Managing MySQL Server with systemd".

### <span id="page-39-0"></span>**2.9.2.1 Troubleshooting Problems Starting the MySQL Server**

This section provides troubleshooting suggestions for problems starting the server. For additional suggestions for Windows systems, see Section 2.3.5, "Troubleshooting a Microsoft Windows MySQL Server Installation".

If you have problems starting the server, here are some things to try:

• Check the error log to see why the server does not start. Log files are located in the data directory (typically C:\Program Files\MySQL\MySQL Server 5.7\data on Windows, /usr/local/ mysql/data for a Unix/Linux binary distribution, and /usr/local/var for a Unix/Linux source distribution). Look in the data directory for files with names of the form host\_name.err and host\_name.log, where host\_name is the name of your server host. Then examine the last few lines of these files. Use tail to display them:

```
$> tail host_name.err
$> tail host_name.log
```

• Specify any special options needed by the storage engines you are using. You can create a my.cnf file and specify startup options for the engines that you plan to use. If you are going to use storage engines that support transactional tables (InnoDB, NDB), be sure that you have them configured the way you want before starting the server. If you are using InnoDB tables, see Section 14.8, "InnoDB Configuration" for guidelines and Section 14.15, "InnoDB Startup Options and System Variables" for option syntax.

Although storage engines use default values for options that you omit, Oracle recommends that you review the available options and specify explicit values for any options whose defaults are not appropriate for your installation.

• Make sure that the server knows where to find the data directory. The [mysqld](#page-144-0) server uses this directory as its current directory. This is where it expects to find databases and where it expects to write log files. The server also writes the pid (process ID) file in the data directory.

The default data directory location is hardcoded when the server is compiled. To determine what the default path settings are, invoke [mysqld](#page-144-0) with the --verbose and --help options. If the data directory is located somewhere else on your system, specify that location with the --datadir option to [mysqld](#page-144-0) or [mysqld\\_safe](#page-144-1), on the command line or in an option file. Otherwise, the server does not work properly. As an alternative to the --datadir option, you can specify [mysqld](#page-144-0) the location of the base directory under which MySQL is installed with the --basedir, and [mysqld](#page-144-0) looks for the data directory there.

To check the effect of specifying path options, invoke [mysqld](#page-144-0) with those options followed by the - verbose and --help options. For example, if you change location to the directory where [mysqld](#page-144-0) is installed and then run the following command, it shows the effect of starting the server with a base directory of /usr/local:

```
$> ./mysqld --basedir=/usr/local --verbose --help
```

You can specify other options such as --datadir as well, but --verbose and --help must be the last options.

Once you determine the path settings you want, start the server without --verbose and --help.

If [mysqld](#page-144-0) is currently running, you can find out what path settings it is using by executing this command:

```
$> mysqladmin variables
```

Or:

```
$> mysqladmin -h host_name variables
```

host\_name is the name of the MySQL server host.

• Make sure that the server can access the data directory. The ownership and permissions of the data directory and its contents must allow the server to read and modify them.

If you get Errcode 13 (which means Permission denied) when starting [mysqld](#page-144-0), this means that the privileges of the data directory or its contents do not permit server access. In this case, you change the permissions for the involved files and directories so that the server has the right to use them. You can also start the server as root, but this raises security issues and should be avoided.

Change location to the data directory and check the ownership of the data directory and its contents to make sure the server has access. For example, if the data directory is /usr/local/mysql/var, use this command:

```
$> ls -la /usr/local/mysql/var
```

If the data directory or its files or subdirectories are not owned by the login account that you use for running the server, change their ownership to that account. If the account is named mysql, use these commands:

```
$> chown -R mysql /usr/local/mysql/var
$> chgrp -R mysql /usr/local/mysql/var
```

Even with correct ownership, MySQL might fail to start up if there is other security software running on your system that manages application access to various parts of the file system. In this case, reconfigure that software to enable [mysqld](#page-144-0) to access the directories it uses during normal operation.

• Verify that the network interfaces the server wants to use are available.

If either of the following errors occur, it means that some other program (perhaps another [mysqld](#page-144-0) server) is using the TCP/IP port or Unix socket file that [mysqld](#page-144-0) is trying to use:

```
Can't start server: Bind on TCP/IP port: Address already in use
Can't start server: Bind on unix socket...
```

Use ps to determine whether you have another [mysqld](#page-144-0) server running. If so, shut down the server before starting [mysqld](#page-144-0) again. (If another server is running, and you really want to run multiple servers, you can find information about how to do so in Section 5.7, "Running Multiple MySQL Instances on One Machine".)

If no other server is running, execute the command telnet your\_host\_name tcp\_ip\_port\_number. (The default MySQL port number is 3306.) Then press Enter a couple of times. If you do not get an error message like telnet: Unable to connect to remote host: Connection refused, some other program is using the TCP/IP port that [mysqld](#page-144-0) is trying to use. Track down what program this is and disable it, or tell [mysqld](#page-144-0) to listen to a different port with the --port option. In this case, specify the same non-default port number for client programs when connecting to the server using TCP/IP.

Another reason the port might be inaccessible is that you have a firewall running that blocks connections to it. If so, modify the firewall settings to permit access to the port.

If the server starts but you cannot connect to it, make sure that you have an entry in /etc/hosts that looks like this:

```
127.0.0.1 localhost
```

• If you cannot get [mysqld](#page-144-0) to start, try to make a trace file to find the problem by using the --debug option. See Section 5.8.3, "The DBUG Package".

## <span id="page-41-0"></span>**2.9.3 Testing the Server**

After the data directory is initialized and you have started the server, perform some simple tests to make sure that it works satisfactorily. This section assumes that your current location is the MySQL installation directory and that it has a bin subdirectory containing the MySQL programs used here. If that is not true, adjust the command path names accordingly.

Alternatively, add the bin directory to your PATH environment variable setting. That enables your shell (command interpreter) to find MySQL programs properly, so that you can run a program by typing only its name, not its path name. See [Section 4.2.7, "Setting Environment Variables"](#page-143-0).

Use mysqladmin to verify that the server is running. The following commands provide simple tests to check whether the server is up and responding to connections:

```
$> bin/mysqladmin version
$> bin/mysqladmin variables
```

If you cannot connect to the server, specify a -u root option to connect as root. If you have assigned a password for the root account already, you'll also need to specify -p on the command line and enter the password when prompted. For example:

```
$> bin/mysqladmin -u root -p version
Enter password: (enter root password here)
```

The output from mysqladmin version varies slightly depending on your platform and version of MySQL, but should be similar to that shown here:

```
$> bin/mysqladmin version
mysqladmin Ver 14.12 Distrib 5.7.44, for pc-linux-gnu on i686
...
Server version 5.7.44
Protocol version 10
Connection Localhost via UNIX socket
UNIX socket /var/lib/mysql/mysql.sock
Uptime: 14 days 5 hours 5 min 21 sec
Threads: 1 Questions: 366 Slow queries: 0
Opens: 0 Flush tables: 1 Open tables: 19
Queries per second avg: 0.000
```

To see what else you can do with mysqladmin, invoke it with the --help option.

Verify that you can shut down the server (include a -p option if the root account has a password already):

```
$> bin/mysqladmin -u root shutdown
```

Verify that you can start the server again. Do this by using [mysqld\\_safe](#page-144-1) or by invoking [mysqld](#page-144-0) directly. For example:

```
$> bin/mysqld_safe --user=mysql &
```

If [mysqld\\_safe](#page-144-1) fails, see [Section 2.9.2.1, "Troubleshooting Problems Starting the MySQL Server"](#page-39-0).

Run some simple tests to verify that you can retrieve information from the server. The output should be similar to that shown here.

Use mysqlshow to see what databases exist:

```
$> bin/mysqlshow
+--------------------+
| Databases |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
```

```
| sys |
+--------------------+
```

The list of installed databases may vary, but always includes at least mysql and information\_schema.

If you specify a database name, mysqlshow displays a list of the tables within the database:

```
$> bin/mysqlshow mysql
Database: mysql
+---------------------------+
| Tables |
+---------------------------+
| columns_priv |
| db |
| engine_cost |
| event |
| func |
| general_log |
| gtid_executed |
| help_category |
| help_keyword |
| help_relation |
| help_topic |
| innodb_index_stats |
| innodb_table_stats |
| ndb_binlog_index |
| plugin |
| proc |
| procs_priv |
| proxies_priv |
| server_cost |
| servers |
| slave_master_info |
| slave_relay_log_info |
| slave_worker_info |
| slow_log |
| tables_priv |
| time_zone |
| time_zone_leap_second |
| time_zone_name |
| time_zone_transition |
| time_zone_transition_type |
| user |
+---------------------------+
```

Use the [mysql](#page-191-0) program to select information from a table in the mysql database:

```
$> bin/mysql -e "SELECT User, Host, plugin FROM mysql.user" mysql
+------+-----------+-----------------------+
| User | Host | plugin |
+------+-----------+-----------------------+
| root | localhost | mysql_native_password |
+------+-----------+-----------------------+
```

At this point, your server is running and you can access it. To tighten security if you have not yet assigned a password to the initial account, follow the instructions in [Section 2.9.4, "Securing the Initial](#page-42-0) [MySQL Account".](#page-42-0)

For more information about [mysql](#page-191-0), mysqladmin, and mysqlshow, see [Section 4.5.1, "mysql —](#page-191-0) [The MySQL Command-Line Client"](#page-191-0), Section 4.5.2, "mysqladmin — A MySQL Server Administration Program", and Section 4.5.7, "mysqlshow — Display Database, Table, and Column Information".

# <span id="page-42-0"></span>**2.9.4 Securing the Initial MySQL Account**

The MySQL installation process involves initializing the data directory, including the grant tables in the mysql system database that define MySQL accounts. For details, see [Section 2.9.1, "Initializing the](#page-32-1) [Data Directory"](#page-32-1).

This section describes how to assign a password to the initial root account created during the MySQL installation procedure, if you have not already done so.

![](_page_43_Picture_2.jpeg)

#### **Note**

Alternative means for performing the process described in this section:

- On Windows, you can perform the process during installation with MySQL Installer (see Section 2.3.3, "MySQL Installer for Windows").
- On all platforms, the MySQL distribution includes [mysql\\_secure\\_installation](#page-173-0), a command-line utility that automates much of the process of securing a MySQL installation.
- On all platforms, MySQL Workbench is available and offers the ability to manage user accounts (see Chapter 29, MySQL Workbench ).

A password may already be assigned to the initial account under these circumstances:

- On Windows, installations performed using MySQL Installer give you the option of assigning a password.
- Installation using the macOS installer generates an initial random password, which the installer displays to the user in a dialog box.
- Installation using RPM packages generates an initial random password, which is written to the server error log.
- Installations using Debian packages give you the option of assigning a password.
- For data directory initialization performed manually using [mysqld --initialize](#page-144-0), [mysqld](#page-144-0) generates an initial random password, marks it expired, and writes it to the server error log. See [Section 2.9.1, "Initializing the Data Directory".](#page-32-1)

The mysql.user grant table defines the initial MySQL user account and its access privileges. Installation of MySQL creates only a 'root'@'localhost' superuser account that has all privileges and can do anything. If the root account has an empty password, your MySQL installation is unprotected: Anyone can connect to the MySQL server as root without a password and be granted all privileges.

The 'root'@'localhost' account also has a row in the mysql.proxies\_priv table that enables granting the PROXY privilege for ''@'', that is, for all users and all hosts. This enables root to set up proxy users, as well as to delegate to other accounts the authority to set up proxy users. See Section 6.2.14, "Proxy Users".

To assign a password for the initial MySQL root account, use the following procedure. Replace root-password in the examples with the password that you want to use.

Start the server if it is not running. For instructions, see [Section 2.9.2, "Starting the Server"](#page-38-0).

The initial root account may or may not have a password. Choose whichever of the following procedures applies:

- If the root account exists with an initial random password that has been expired, connect to the server as root using that password, then choose a new password. This is the case if the data directory was initialized using [mysqld --initialize](#page-144-0), either manually or using an installer that does not give you the option of specifying a password during the install operation. Because the password exists, you must use it to connect to the server. But because the password is expired, you cannot use the account for any purpose other than to choose a new password, until you do choose one.
  - 1. If you do not know the initial random password, look in the server error log.

2. Connect to the server as root using the password:

```
$> mysql -u root -p
Enter password: (enter the random root password here)
```

3. Choose a new password to replace the random password:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';
```

- If the root account exists but has no password, connect to the server as root using no password, then assign a password. This is the case if you initialized the data directory using [mysqld -](#page-144-0) [initialize-insecure](#page-144-0).
  - 1. Connect to the server as root using no password:

```
$> mysql -u root --skip-password
```

2. Assign a password:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';
```

After assigning the root account a password, you must supply that password whenever you connect to the server using the account. For example, to connect to the server using the [mysql](#page-191-0) client, use this command:

```
$> mysql -u root -p
Enter password: (enter root password here)
```

To shut down the server with mysqladmin, use this command:

```
$> mysqladmin -u root -p shutdown
Enter password: (enter root password here)
```

![](_page_44_Picture_14.jpeg)

#### **Note**

For additional information about setting passwords, see Section 6.2.10, "Assigning Account Passwords". If you forget your root password after setting it, see Section B.3.3.2, "How to Reset the Root Password".

To set up additional accounts, see Section 6.2.7, "Adding Accounts, Assigning Privileges, and Dropping Accounts".

# <span id="page-44-0"></span>**2.9.5 Starting and Stopping MySQL Automatically**

This section discusses methods for starting and stopping the MySQL server.

Generally, you start the [mysqld](#page-144-0) server in one of these ways:

- Invoke [mysqld](#page-144-0) directly. This works on any platform.
- On Windows, you can set up a MySQL service that runs automatically when Windows starts. See Section 2.3.4.8, "Starting MySQL as a Windows Service".
- On Unix and Unix-like systems, you can invoke [mysqld\\_safe](#page-144-1), which tries to determine the proper options for [mysqld](#page-144-0) and then runs it with those options. See [Section 4.3.2, "mysqld\\_safe — MySQL](#page-144-1) [Server Startup Script"](#page-144-1).
- On Linux systems that support systemd, you can use it to control the server. See Section 2.5.10, "Managing MySQL Server with systemd".
- On systems that use System V-style run directories (that is, /etc/init.d and run-level specific directories), invoke [mysql.server](#page-153-0). This script is used primarily at system startup and shutdown. It usually is installed under the name mysql. The [mysql.server](#page-153-0) script starts the server by invoking [mysqld\\_safe](#page-144-1). See [Section 4.3.3, "mysql.server — MySQL Server Startup Script".](#page-153-0)

- On macOS, install a launchd daemon to enable automatic MySQL startup at system startup. The daemon starts the server by invoking [mysqld\\_safe](#page-144-1). For details, see Section 2.4.3, "Installing a MySQL Launch Daemon". A MySQL Preference Pane also provides control for starting and stopping MySQL through the System Preferences. See Section 2.4.4, "Installing and Using the MySQL Preference Pane".
- On Solaris, use the service management framework (SMF) system to initiate and control MySQL startup.

systemd, the [mysqld\\_safe](#page-144-1) and [mysql.server](#page-153-0) scripts, Solaris SMF, and the macOS Startup Item (or MySQL Preference Pane) can be used to start the server manually, or automatically at system startup time. systemd, [mysql.server](#page-153-0), and the Startup Item also can be used to stop the server.

The following table shows which option groups the server and startup scripts read from option files.

**Table 2.15 MySQL Startup Scripts and Supported Server Option Groups**

| Script       | Option Groups                                 |
|--------------|-----------------------------------------------|
| mysqld       | [mysqld], [server],<br>[mysqld-major_version] |
| mysqld_safe  | [mysqld], [server], [mysqld_safe]             |
| mysql.server | [mysqld], [mysql.server], [server]            |

[mysqld-major\_version] means that groups with names like [mysqld-5.6] and [mysqld-5.7] are read by servers having versions 5.6.x, 5.7.x, and so forth. This feature can be used to specify options that can be read only by servers within a given release series.

For backward compatibility, [mysql.server](#page-153-0) also reads the [mysql\_server] group and [mysqld\\_safe](#page-144-1) also reads the [safe\_mysqld] group. To be current, you should update your option files to use the [mysql.server] and [mysqld\_safe] groups instead.

For more information on MySQL configuration files and their structure and contents, see [Section 4.2.2.2, "Using Option Files".](#page-116-0)

# <span id="page-45-0"></span>**2.10 Upgrading MySQL**

This section describes the steps to upgrade a MySQL installation.

Upgrading is a common procedure, as you pick up bug fixes within the same MySQL release series or significant features between major MySQL releases. You perform this procedure first on some test systems to make sure everything works smoothly, and then on the production systems.

![](_page_45_Picture_13.jpeg)

#### **Note**

In the following discussion, MySQL commands that must be run using a MySQL account with administrative privileges include -u root on the command line to specify the MySQL root user. Commands that require a password for root also include a -p option. Because -p is followed by no option value, such commands prompt for the password. Type the password when prompted and press Enter.

SQL statements can be executed using the [mysql](#page-191-0) command-line client (connect as root to ensure that you have the necessary privileges).

## <span id="page-45-1"></span>**2.10.1 Before You Begin**

Review the information in this section before upgrading. Perform any recommended actions.

• Protect your data by creating a backup. The backup should include the mysql system database, which contains the MySQL system tables. See Section 7.2, "Database Backup Methods".

- Review [Section 2.10.2, "Upgrade Paths"](#page-46-0) to ensure that your intended upgrade path is supported.
- Review [Section 2.10.3, "Changes in MySQL 5.7"](#page-47-0) for changes that you should be aware of before upgrading. Some changes may require action.
- Review Section 1.3, "What Is New in MySQL 5.7" for deprecated and removed features. An upgrade may require changes with respect to those features if you use any of them.
- Review Section 1.4, "Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 5.7". If you use deprecated or removed variables, an upgrade may require configuration changes.
- Review the [Release Notes](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) for information about fixes, changes, and new features.
- If you use replication, review Section 16.4.3, "Upgrading a Replication Topology".
- Upgrade procedures vary by platform and how the initial installation was performed. Use the procedure that applies to your current MySQL installation:
  - For binary and package-based installations on non-Windows platforms, refer to [Section 2.10.4,](#page-56-0) ["Upgrading MySQL Binary or Package-based Installations on Unix/Linux".](#page-56-0)

![](_page_46_Picture_9.jpeg)

#### **Note**

For supported Linux distributions, the preferred method for upgrading package-based installations is to use the MySQL software repositories (MySQL Yum Repository, MySQL APT Repository, and MySQL SLES Repository).

- For installations on an Enterprise Linux platform or Fedora using the MySQL Yum Repository, refer to [Section 2.10.5, "Upgrading MySQL with the MySQL Yum Repository"](#page-59-0).
- For installations on Ubuntu using the MySQL APT repository, refer to [Section 2.10.6, "Upgrading](#page-60-0) [MySQL with the MySQL APT Repository".](#page-60-0)
- For installations on SLES using the MySQL SLES repository, refer to [Section 2.10.7, "Upgrading](#page-60-1) [MySQL with the MySQL SLES Repository".](#page-60-1)
- For installations performed using Docker, refer to [Section 2.10.9, "Upgrading a Docker Installation](#page-62-0) [of MySQL".](#page-62-0)
- For installations on Windows, refer to [Section 2.10.8, "Upgrading MySQL on Windows".](#page-61-0)
- If your MySQL installation contains a large amount of data that might take a long time to convert after an in-place upgrade, it may be useful to create a test instance for assessing the conversions that are required and the work involved to perform them. To create a test instance, make a copy of your MySQL instance that contains the mysql database and other databases without the data. Run the upgrade procedure on the test instance to assess the work involved to perform the actual data conversion.
- Rebuilding and reinstalling MySQL language interfaces is recommended when you install or upgrade to a new release of MySQL. This applies to MySQL interfaces such as PHP mysql extensions and the Perl DBD::mysql module.

# <span id="page-46-0"></span>**2.10.2 Upgrade Paths**

- Upgrade is only supported between General Availability (GA) releases.
- Upgrade from MySQL 5.6 to 5.7 is supported. Upgrading to the latest release is recommended before upgrading to the next version. For example, upgrade to the latest MySQL 5.6 release before upgrading to MySQL 5.7.

- Upgrade that skips versions is not supported. For example, upgrading directly from MySQL 5.5 to 5.7 is not supported.
- Upgrade within a release series is supported. For example, upgrading from MySQL 5.7.x to 5.7.y is supported. Skipping a release is also supported. For example, upgrading from MySQL 5.7.x to 5.7.z is supported.

## <span id="page-47-0"></span>**2.10.3 Changes in MySQL 5.7**

Before upgrading to MySQL 5.7, review the changes described in this section to identify those that apply to your current MySQL installation and applications. Perform any recommended actions.

Changes marked as **Incompatible change** are incompatibilities with earlier versions of MySQL, and may require your attention before upgrading. Our aim is to avoid these changes, but occasionally they are necessary to correct problems that would be worse than an incompatibility between releases. If an upgrade issue applicable to your installation involves an incompatibility, follow the instructions given in the description. Sometimes this involves dumping and reloading tables, or use of a statement such as CHECK TABLE or REPAIR TABLE.

For dump and reload instructions, see [Section 2.10.12, "Rebuilding or Repairing Tables or Indexes"](#page-64-0). Any procedure that involves REPAIR TABLE with the USE\_FRM option must be done before upgrading. Use of this statement with a version of MySQL different from the one used to create the table (that is, using it after upgrading) may damage the table. See Section 13.7.2.5, "REPAIR TABLE Statement".

- [Configuration Changes](#page-47-1)
- [System Table Changes](#page-49-0)
- [Server Changes](#page-49-1)
- [InnoDB Changes](#page-54-0)
- [SQL Changes](#page-55-0)

## <span id="page-47-1"></span>**Configuration Changes**

• **Incompatible change**: In MySQL 5.7.11, the default --early-plugin-load value is the name of the keyring\_file plugin library file, causing that plugin to be loaded by default. In MySQL 5.7.12 and higher, the default --early-plugin-load value is empty; to load the keyring\_file plugin, you must explicitly specify the option with a value naming the keyring\_file plugin library file.

InnoDB tablespace encryption requires that the keyring plugin to be used be loaded prior to InnoDB initialization, so this change of default --early-plugin-load value introduces an incompatibility for upgrades from 5.7.11 to 5.7.12 or higher. Administrators who have encrypted InnoDB tablespaces must take explicit action to ensure continued loading of the keyring plugin: Start the server with an --early-plugin-load option that names the plugin library file. For additional information, see Section 6.4.4.1, "Keyring Plugin Installation".

• **Incompatible change**: The INFORMATION\_SCHEMA has tables that contain system and status variable information (see Section 24.3.11, "The INFORMATION\_SCHEMA GLOBAL\_VARIABLES and SESSION\_VARIABLES Tables", and Section 24.3.10, "The INFORMATION\_SCHEMA GLOBAL\_STATUS and SESSION\_STATUS Tables"). As of MySQL 5.7.6, the Performance Schema also contains system and status variable tables (see Section 25.12.13, "Performance Schema System Variable Tables", and Section 25.12.14, "Performance Schema Status Variable Tables"). The Performance Schema tables are intended to replace the INFORMATION\_SCHEMA tables, which are deprecated as of MySQL 5.7.6 and are removed in MySQL 8.0.

For advice on migrating away from the INFORMATION\_SCHEMA tables to the Performance Schema tables, see Section 25.20, "Migrating to Performance Schema System and Status Variable Tables". To assist in the migration, you can use the show\_compatibility\_56 system variable, which affects how system and status variable information is provided by the INFORMATION\_SCHEMA and Performance Schema tables, and also by the SHOW VARIABLES and SHOW STATUS statements.

show\_compatibility\_56 is enabled by default in 5.7.6 and 5.7.7, and disabled by default in MySQL 5.7.8.

For details about the effects of show\_compatibility\_56, see Section 5.1.7, "Server System Variables" For better understanding, it is strongly recommended that you read also these sections:

- Section 25.12.13, "Performance Schema System Variable Tables"
- Section 25.12.14, "Performance Schema Status Variable Tables"
- Section 25.12.15.10, "Status Variable Summary Tables"
- **Incompatible change**: As of MySQL 5.7.6, data directory initialization creates only a single root account, 'root'@'localhost'. (See [Section 2.9.1, "Initializing the Data Directory".](#page-32-1)) An attempt to connect to the host 127.0.0.1 normally resolves to the localhost account. However, this fails if the server is run with skip\_name\_resolve enabled. If you plan to do that, make sure that an account exists that can accept a connection. For example, to be able to connect as root using - host=127.0.0.1 or --host=::1, create these accounts:

```
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';
```

- **Incompatible change**: As of MySQL 5.7.6, for some Linux platforms, when MySQL is installed using RPM and Debian packages, server startup and shutdown now is managed using systemd rather than [mysqld\\_safe](#page-144-1), and [mysqld\\_safe](#page-144-1) is not installed. This may require some adjustment to the manner in which you specify server options. For details, see Section 2.5.10, "Managing MySQL Server with systemd".
- **Incompatible change**: In MySQL 5.7.5, the executable binary version of [mysql\\_install\\_db](#page-162-0) is located in the bin installation directory, whereas the Perl version was located in the scripts installation directory. For upgrades from an older version of MySQL, you may find a version in both directories. To avoid confusion, remove the version in the scripts directory. For fresh installations of MySQL 5.7.5 or later, [mysql\\_install\\_db](#page-162-0) is only found in the bin directory, and the scripts directory is no longer present. Applications that expect to find [mysql\\_install\\_db](#page-162-0) in the scripts directory should be updated to look in the bin directory instead.

The location of [mysql\\_install\\_db](#page-162-0) becomes less material as of MySQL 5.7.6 because as of that version it is deprecated in favor of [mysqld --initialize](#page-144-0) (or [mysqld --initialize](#page-144-0)[insecure](#page-144-0)). See [Section 2.9.1, "Initializing the Data Directory"](#page-32-1)

- **Incompatible change**: In MySQL 5.7.5, these SQL mode changes were made:
  - Strict SQL mode for transactional storage engines (STRICT\_TRANS\_TABLES) is now enabled by default.
  - Implementation of the ONLY\_FULL\_GROUP\_BY SQL mode has been made more sophisticated, to no longer reject deterministic queries that previously were rejected. In consequence,

ONLY\_FULL\_GROUP\_BY is now enabled by default, to prohibit nondeterministic queries containing expressions not guaranteed to be uniquely determined within a group.

- The changes to the default SQL mode result in a default sql\_mode system variable value with these modes enabled: ONLY\_FULL\_GROUP\_BY, STRICT\_TRANS\_TABLES, NO\_ENGINE\_SUBSTITUTION.
- The ONLY\_FULL\_GROUP\_BY mode is also now included in the modes comprised by the ANSI SQL mode.

If you find that having ONLY\_FULL\_GROUP\_BY enabled causes queries for existing applications to be rejected, either of these actions should restore operation:

- If it is possible to modify an offending query, do so, either so that nondeterministic nonaggregated columns are functionally dependent on GROUP BY columns, or by referring to nonaggregated columns using ANY\_VALUE().
- If it is not possible to modify an offending query (for example, if it is generated by a thirdparty application), set the sql\_mode system variable at server startup to not enable ONLY\_FULL\_GROUP\_BY.

For more information about SQL modes and GROUP BY queries, see Section 5.1.10, "Server SQL Modes", and Section 12.19.3, "MySQL Handling of GROUP BY".

## <span id="page-49-0"></span>**System Table Changes**

• **Incompatible change**: The Password column of the mysql.user system table was removed in MySQL 5.7.6. All credentials are stored in the authentication\_string column, including those formerly stored in the Password column. If performing an in-place upgrade to MySQL 5.7.6 or later, run [mysql\\_upgrade](#page-181-0) as directed by the [in-place upgrade procedure](#page-56-1) to migrate the Password column contents to the authentication\_string column.

If performing a [logical upgrade](#page-57-0) using a mysqldump dump file from a pre-5.7.6 MySQL installation, you must observe these conditions for the mysqldump command used to generate the dump file:

- You must include the --add-drop-table option
- You must not include the --flush-privileges option

As outlined in the [logical upgrade procedure](#page-57-0), load the pre-5.7.6 dump file into the 5.7.6 (or later) server before running [mysql\\_upgrade](#page-181-0).

## <span id="page-49-1"></span>**Server Changes**

- **Incompatible change**: As of MySQL 5.7.5, support for passwords that use the older pre-4.1 password hashing format is removed, which involves the following changes. Applications that use any feature no longer supported must be modified.
  - The mysql\_old\_password authentication plugin that used pre-4.1 password hash values is removed. Accounts that use this plugin are disabled at startup and the server writes an "unknown plugin" message to the error log. For instructions on upgrading accounts that use this plugin, see Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".
  - For the old\_passwords system variable, a value of 1 (produce pre-4.1 hash values) is no longer permitted.
  - The --secure-auth option to the server and client programs is the default, but is now a no-op. It is deprecated;expect it to be removed in a future MySQL release.

- The --skip-secure-auth option to the server and client programs is no longer supported and using it produces an error.
- The secure\_auth system variable permits only a value of 1; a value of 0 is no longer permitted.
- The OLD\_PASSWORD() function is removed.
- **Incompatible change**: In MySQL 5.6.6, the 2-digit YEAR(2) data type was deprecated. In MySQL 5.7.5, support for YEAR(2) is removed. Once you upgrade to MySQL 5.7.5 or higher, any remaining 2-digit YEAR(2) columns must be converted to 4-digit YEAR columns to become usable again. For conversion strategies, see Section 11.2.5, "2-Digit YEAR(2) Limitations and Migrating to 4-Digit YEAR". Running [mysql\\_upgrade](#page-181-0) after upgrading is one of the possible conversion strategies.
- As of MySQL 5.7.7, CHECK TABLE ... FOR UPGRADE reports a table as needing a rebuild if it contains old temporal columns in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision) and the avoid\_temporal\_upgrade system variable is disabled. This helps [mysql\\_upgrade](#page-181-0) to detect and upgrade tables containing old temporal columns. If avoid\_temporal\_upgrade is enabled, FOR UPGRADE ignores the old temporal columns present in the table; consequently, [mysql\\_upgrade](#page-181-0) does not upgrade them.

As of MySQL 5.7.7, REPAIR TABLE upgrades a table if it contains old temporal columns in pre-5.6.4 format and the avoid\_temporal\_upgrade system variable is disabled. If avoid\_temporal\_upgrade is enabled, REPAIR TABLE ignores the old temporal columns present in the table and does not upgrade them.

To check for tables that contain such temporal columns and need a rebuild, disable avoid\_temporal\_upgrade before executing CHECK TABLE ... FOR UPGRADE.

To upgrade tables that contain such temporal columns, disable avoid\_temporal\_upgrade before executing REPAIR TABLE or [mysql\\_upgrade](#page-181-0).

• **Incompatible change**: As of MySQL 5.7.2, the server requires account rows in the mysql.user system table to have a nonempty plugin column value and disables accounts with an empty value. This requires that you upgrade your mysql.user table to fill in all plugin values. As of MySQL 5.7.6, use this procedure:

If you plan to upgrade using the data directory from your existing MySQL installation:

- 1. Stop the old (MySQL 5.6) server
- 2. Upgrade the MySQL binaries in place by replacing the old binaries with the new ones
- 3. Start the MySQL 5.7 server normally (no special options)
- 4. Run [mysql\\_upgrade](#page-181-0) to upgrade the system tables
- 5. Restart the MySQL 5.7 server

If you plan to upgrade by reloading a dump file generated from your existing MySQL installation:

- 1. To generate the dump file, run mysqldump with the --add-drop-table option and without the --flush-privileges option
- 2. Stop the old (MySQL 5.6) server
- 3. Upgrade the MySQL binaries in place (replace the old binaries with the new ones)
- 4. Start the MySQL 5.7 server normally (no special options)
- 5. Reload the dump file (mysql < [dump\\_file](#page-191-0))
- 6. Run [mysql\\_upgrade](#page-181-0) to upgrade the system tables
- 7. Restart the MySQL 5.7 server

Before MySQL 5.7.6, the procedure is more involved:

If you plan to upgrade using the data directory from your existing MySQL installation:

- 1. Stop the old (MySQL 5.6) server
- 2. Upgrade the MySQL binaries in place (replace the old binaries with the new ones)
- 3. Restart the server with the --skip-grant-tables option to disable privilege checking
- 4. Run [mysql\\_upgrade](#page-181-0) to upgrade the system tables
- 5. Restart the server normally (without --skip-grant-tables)

If you plan to upgrade by reloading a dump file generated from your existing MySQL installation:

- 1. To generate the dump file, run mysqldump without the --flush-privileges option
- 2. Stop the old (MySQL 5.6) server
- 3. Upgrade the MySQL binaries in place (replace the old binaries with the new ones)
- 4. Restart the server with the --skip-grant-tables option to disable privilege checking
- 5. Reload the dump file (mysql < [dump\\_file](#page-191-0))
- 6. Run [mysql\\_upgrade](#page-181-0) to upgrade the system tables
- 7. Restart the server normally (without --skip-grant-tables)

[mysql\\_upgrade](#page-181-0) runs by default as the MySQL root user. For the preceding procedures, if the root password is expired when you run [mysql\\_upgrade](#page-181-0), it displays a message informing you that your password is expired and that [mysql\\_upgrade](#page-181-0) failed as a result. To correct this, reset the root password and run [mysql\\_upgrade](#page-181-0) again:

```
$> mysql -u root -p
Enter password: **** <- enter root password here
mysql> ALTER USER USER() IDENTIFIED BY 'root-password'; # MySQL 5.7.6 and up
mysql> SET PASSWORD = PASSWORD('root-password'); # Before MySQL 5.7.6
mysql> quit
$> mysql_upgrade -p
Enter password: **** <- enter root password here
```

The password-resetting statement normally does not work if the server is started with --skipgrant-tables, but the first invocation of [mysql\\_upgrade](#page-181-0) flushes the privileges, so when you run [mysql](#page-191-0), the statement is accepted.

If [mysql\\_upgrade](#page-181-0) itself expires the root password, you must reset the password again in the same manner.

After following the preceding instructions, DBAs are advised also to convert accounts that use the mysql\_old\_password authentication plugin to use mysql\_native\_password instead, because support for mysql\_old\_password has been removed. For account upgrade instructions, see Section 6.4.1.3, "Migrating Away from Pre-4.1 Password Hashing and the mysql\_old\_password Plugin".

• **Incompatible change**: It is possible for a column DEFAULT value to be valid for the sql\_mode value at table-creation time but invalid for the sql\_mode value when rows are inserted or updated. Example:

```
SET sql_mode = '';
CREATE TABLE t (d DATE DEFAULT 0);
SET sql_mode = 'NO_ZERO_DATE,STRICT_ALL_TABLES';
INSERT INTO t (d) VALUES(DEFAULT);
```

In this case, 0 should be accepted for the CREATE TABLE but rejected for the INSERT. However, previously the server did not evaluate DEFAULT values used for inserts or updates against the current sql\_mode. In the example, the INSERT succeeds and inserts '0000-00-00' into the DATE column.

As of MySQL 5.7.2, the server applies the proper sql\_mode checks to generate a warning or error at insert or update time.

A resulting incompatibility for replication if you use statement-based logging (binlog\_format=STATEMENT) is that if a replica is upgraded, a source which has not been upgraded executes the preceding example without error, whereas the INSERT fails on the replica and replication stops.

To deal with this, stop all new statements on the source and wait until the replicas catch up. Then upgrade the replicas followed by the source. Alternatively, if you cannot stop new statements, temporarily change to row-based logging on the source (binlog\_format=ROW) and wait until all replicas have processed all binary logs produced up to the point of this change. Then upgrade the replicas followed by the source and change the source back to statement-based logging.

• **Incompatible change**: Several changes were made to the audit log plugin for better compatibility with Oracle Audit Vault. For upgrading purpose, the main issue is that the default format of the

audit log file has changed: Information within <AUDIT\_RECORD> elements previously written using attributes now is written using subelements.

Example of old <AUDIT\_RECORD> format:

```
<AUDIT_RECORD
 TIMESTAMP="2013-04-15T15:27:27"
 NAME="Query"
 CONNECTION_ID="3"
 STATUS="0"
 SQLTEXT="SELECT 1"
/>
```

#### Example of new format:

```
<AUDIT_RECORD>
 <TIMESTAMP>2013-04-15T15:27:27 UTC</TIMESTAMP>
 <RECORD_ID>3998_2013-04-15T15:27:27</RECORD_ID>
 <NAME>Query</NAME>
 <CONNECTION_ID>3</CONNECTION_ID>
 <STATUS>0</STATUS>
 <STATUS_CODE>0</STATUS_CODE>
 <USER>root[root] @ localhost [127.0.0.1]</USER>
 <OS_LOGIN></OS_LOGIN>
 <HOST>localhost</HOST>
 <IP>127.0.0.1</IP>
 <COMMAND_CLASS>select</COMMAND_CLASS>
 <SQLTEXT>SELECT 1</SQLTEXT>
</AUDIT_RECORD>
```

If you previously used an older version of the audit log plugin, use this procedure to avoid writing new-format log entries to an existing log file that contains old-format entries:

- 1. Stop the server.
- 2. Rename the current audit log file manually. This file contains log entries using only the old format.
- 3. Update the server and restart it. The audit log plugin creates a new log file, which contains log entries using only the new format.

For information about the audit log plugin, see Section 6.4.5, "MySQL Enterprise Audit".

• As of MySQL 5.7.7, the default connection timeout for a replica was changed from 3600 seconds (one hour) to 60 seconds (one minute). The new default is applied when a replica without a setting for the slave\_net\_timeout system variable is upgraded to MySQL 5.7. The default setting for the heartbeat interval, which regulates the heartbeat signal to stop the connection timeout occurring in the absence of data if the connection is still good, is calculated as half the value of slave\_net\_timeout. The heartbeat interval is recorded in the replica's source info log (the mysql.slave\_master\_info table or master.info file), and it is not changed automatically when the value or default setting of slave\_net\_timeout is changed. A MySQL 5.6 replica that used the default connection timeout and heartbeat interval, and was then upgraded to MySQL 5.7, therefore has a heartbeat interval that is much longer than the connection timeout.

If the level of activity on the source is such that updates to the binary log are sent to the replica at least once every 60 seconds, this situation is not an issue. However, if no data is received from the source, because the heartbeat is not being sent, the connection timeout expires. The replica therefore thinks the connection to the source has been lost and makes multiple reconnection attempts (as controlled by the MASTER\_CONNECT\_RETRY and MASTER\_RETRY\_COUNT settings, which can also be seen in the source info log). The reconnection attempts spawn numerous zombie dump threads that the source must kill, causing the error log on the source to contain multiple errors of the form While initializing dump thread for slave with UUID uuid, found a zombie dump thread with the same UUID. Master is killing the zombie dump thread threadid. To avoid this issue, immediately before upgrading a replica to MySQL 5.7, check whether the slave\_net\_timeout system variable is using the default setting. If so, issue

CHANGE MASTER TO with the MASTER\_HEARTBEAT\_PERIOD option, and set the heartbeat interval to 30 seconds, so that it works with the new connection timeout of 60 seconds that applies after the upgrade.

• **Incompatible change**: MySQL 5.6.22 and later recognized the REFERENCES privilege but did not entirely enforce it; a user with at least one of SELECT, INSERT, UPDATE, DELETE, or REFERENCES could create a foreign key constraint on a table. MySQL 5.7 (and later) requires the user to have the REFERENCES privilege to do this. This means that if you migrate users from a MySQL 5.6 server (any version) to one running MySQL 5.7, you must make sure to grant this privilege explicitly to any users which need to be able to create foreign keys. This includes the user account employed to import dumps containing tables with foreign keys.

### <span id="page-54-0"></span>**InnoDB Changes**

• As of MySQL 5.7.24, the [zlib library](http://www.zlib.net/) version bundled with MySQL was raised from version 1.2.3 to version 1.2.11.

The zlib compressBound() function in zlib 1.2.11 returns a slightly higher estimate of the buffer size required to compress a given length of bytes than it did in zlib version 1.2.3. The compressBound() function is called by InnoDB functions that determine the maximum row size permitted when creating compressed InnoDB tables or inserting rows into compressed InnoDB tables. As a result, CREATE TABLE ... ROW\_FORMAT=COMPRESSED or INSERT operations with row sizes very close to the maximum row size that were successful in earlier releases could now fail.

If you have compressed InnoDB tables with large rows, it is recommended that you test compressed table CREATE TABLE statements on a MySQL 5.7 test instance prior to upgrading.

- **Incompatible change**: To simplify InnoDB tablespace discovery during crash recovery, new redo log record types were introduced in MySQL 5.7.5. This enhancement changes the redo log format. Before performing an in-place upgrade, perform a clean shutdown using an innodb\_fast\_shutdown setting of 0 or 1. A slow shutdown using innodb\_fast\_shutdown=0 is a recommended step in [In-Place Upgrade](#page-56-1).
- **Incompatible change**: MySQL 5.7.8 and 5.7.9 undo logs may contain insufficient information about spatial columns, which could result in a upgrade failure (Bug #21508582). Before performing an in-place upgrade from MySQL 5.7.8 or 5.7.9 to 5.7.10 or higher, perform a slow shutdown using innodb\_fast\_shutdown=0 to clear the undo logs. A slow shutdown using innodb\_fast\_shutdown=0 is a recommended step in [In-Place Upgrade.](#page-56-1)
- **Incompatible change**: MySQL 5.7.8 undo logs may contain insufficient information about virtual columns and virtual column indexes, which could result in a upgrade failure (Bug #21869656). Before performing an in-place upgrade from MySQL 5.7.8 to MySQL 5.7.9 or higher, perform a slow shutdown using innodb\_fast\_shutdown=0 to clear the undo logs. A slow shutdown using innodb\_fast\_shutdown=0 is a recommended step in [In-Place Upgrade.](#page-56-1)
- **Incompatible change**: As of MySQL 5.7.9, the redo log header of the first redo log file (ib\_logfile0) includes a format version identifier and a text string that identifies the MySQL version that created the redo log files. This enhancement changes the redo log format, requiring that MySQL be shutdown cleanly using an innodb\_fast\_shutdown setting of 0 or 1 before performing an in-place upgrade to MySQL 5.7.9 or higher. A slow shutdown using innodb\_fast\_shutdown=0 is a recommended step in [In-Place Upgrade](#page-56-1).
- In MySQL 5.7.9, DYNAMIC replaces COMPACT as the implicit default row format for InnoDB tables. A new configuration option, innodb\_default\_row\_format, specifies the default InnoDB row format. Permitted values include DYNAMIC (the default), COMPACT, and REDUNDANT.

After upgrading to 5.7.9, any new tables that you create use the row format defined by innodb\_default\_row\_format unless you explicitly define a row format (ROW\_FORMAT).

For existing tables that do not explicitly define a ROW\_FORMAT option or that use ROW\_FORMAT=DEFAULT, any operation that rebuilds a table also silently changes the row format of the table to the format defined by innodb\_default\_row\_format. Otherwise, existing tables retain their current row format setting. For more information, see Defining the Row Format of a Table.

- Beginning with MySQL 5.7.6, the InnoDB storage engine uses its own built-in ("native") partitioning handler for any new partitioned tables created using InnoDB. Partitioned InnoDB tables created in previous versions of MySQL are not automatically upgraded. You can easily upgrade such tables to use InnoDB native partitioning in MySQL 5.7.9 or later using either of the following methods:
  - To upgrade an individual table from the generic partitioning handler to InnoDB native partitioning, execute the statement ALTER TABLE table\_name UPGRADE PARTITIONING.
  - To upgrade all InnoDB tables that use the generic partitioning handler to use the native partitioning handler instead, run [mysql\\_upgrade](#page-181-0).

## <span id="page-55-0"></span>**SQL Changes**

- **Incompatible change**: The GET\_LOCK() function was reimplemented in MySQL 5.7.5 using the metadata locking (MDL) subsystem and its capabilities have been extended:
  - Previously, GET\_LOCK() permitted acquisition of only one named lock at a time, and a second GET\_LOCK() call released any existing lock. Now GET\_LOCK() permits acquisition of more than one simultaneous named lock and does not release existing locks.

Applications that rely on the behavior of GET\_LOCK() releasing any previous lock must be modified for the new behavior.

- The capability of acquiring multiple locks introduces the possibility of deadlock among clients. The MDL subsystem detects deadlock and returns an [ER\\_USER\\_LOCK\\_DEADLOCK](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_user_lock_deadlock) error when this occurs.
- The MDL subsystem imposes a limit of 64 characters on lock names, so this limit now also applies to named locks. Previously, no length limit was enforced.
- Locks acquired with GET\_LOCK() now appear in the Performance Schema metadata\_locks table. The OBJECT\_TYPE column says USER LEVEL LOCK and the OBJECT\_NAME column indicates the lock name.
- A new function, RELEASE\_ALL\_LOCKS() permits release of all acquired named locks at once.

For more information, see Section 12.14, "Locking Functions".

• The optimizer now handles derived tables and views in the FROM clause in consistent fashion to better avoid unnecessary materialization and to enable use of pushed-down conditions that produce more efficient execution plans.

However in MySQL 5.7 before MySQL 5.7.11, and for statements such as DELETE or UPDATE that modify tables, using the merge strategy for a derived table that previously was materialized can result in an [ER\\_UPDATE\\_TABLE\\_USED](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_update_table_used) error:

```
mysql> DELETE FROM t1
 -> WHERE id IN (SELECT id
 -> FROM (SELECT t1.id
 -> FROM t1 INNER JOIN t2 USING (id)
 -> WHERE t2.status = 0) AS t);
ERROR 1093 (HY000): You can't specify target table 't1'
for update in FROM clause
```

The error occurs when merging a derived table into the outer query block results in a statement that both selects from and modifies a table. (Materialization does not cause the problem because, in effect, it converts the derived table to a separate table.) The workaround to avoid this error was to disable the derived\_merge flag of the optimizer\_switch system variable before executing the statement:

```
SET optimizer_switch = 'derived_merge=off';
```

The derived\_merge flag controls whether the optimizer attempts to merge subqueries and views in the FROM clause into the outer query block, assuming that no other rule prevents merging. By default, the flag is on to enable merging. Setting the flag to off prevents merging and avoids the error just described. For more information, see Section 8.2.2.4, "Optimizing Derived Tables and View References with Merging or Materialization".

- Some keywords may be reserved in MySQL 5.7 that were not reserved in MySQL 5.6. See Section 9.3, "Keywords and Reserved Words". This can cause words previously used as identifiers to become illegal. To fix affected statements, use identifier quoting. See Section 9.2, "Schema Object Names".
- After upgrading, it is recommended that you test optimizer hints specified in application code to ensure that the hints are still required to achieve the desired optimization strategy. Optimizer enhancements can sometimes render certain optimizer hints unnecessary. In some cases, an unnecessary optimizer hint may even be counterproductive.
- In UNION statements, to apply ORDER BY or LIMIT to an individual SELECT, place the clause inside the parentheses that enclose the SELECT:

```
(SELECT a FROM t1 WHERE a=10 AND B=1 ORDER BY a LIMIT 10)
UNION
(SELECT a FROM t2 WHERE a=11 AND B=2 ORDER BY a LIMIT 10);
```

Previous versions of MySQL may permit such statements without parentheses. In MySQL 5.7, the requirement for parentheses is enforced.

## <span id="page-56-0"></span>**2.10.4 Upgrading MySQL Binary or Package-based Installations on Unix/ Linux**

This section describes how to upgrade MySQL binary and package-based installations on Unix/Linux. In-place and logical upgrade methods are described.

- [In-Place Upgrade](#page-56-1)
- [Logical Upgrade](#page-57-0)

### <span id="page-56-1"></span>**In-Place Upgrade**

An in-place upgrade involves shutting down the old MySQL server, replacing the old MySQL binaries or packages with the new ones, restarting MySQL on the existing data directory, and upgrading any remaining parts of the existing installation that require upgrading.

![](_page_56_Picture_14.jpeg)

#### **Note**

Only upgrade a MySQL server instance that was properly shut down. If the instance unexpectedly shutdown, then restart the instance and shut it down with innodb\_fast\_shutdown=0 before upgrade.

![](_page_56_Picture_17.jpeg)

#### **Note**

If you upgrade an installation originally produced by installing multiple RPM packages, upgrade all the packages, not just some. For example, if you previously installed the server and client RPMs, do not upgrade just the server RPM.

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysqld\\_safe](#page-144-1) is not installed. In such cases, use systemd for server startup and shutdown instead of the methods used in the following instructions. See Section 2.5.10, "Managing MySQL Server with systemd".

To perform an in-place upgrade:

- 1. If you use XA transactions with InnoDB, run XA RECOVER before upgrading to check for uncommitted XA transactions. If results are returned, either commit or rollback the XA transactions by issuing an XA COMMIT or XA ROLLBACK statement.
- 2. Configure MySQL to perform a slow shutdown by setting innodb\_fast\_shutdown to 0. For example:

```
mysql -u root -p --execute="SET GLOBAL innodb_fast_shutdown=0"
```

With a slow shutdown, InnoDB performs a full purge and change buffer merge before shutting down, which ensures that data files are fully prepared in case of file format differences between releases.

3. Shut down the old MySQL server. For example:

```
mysqladmin -u root -p shutdown
```

- 4. Upgrade the MySQL binary installation or packages. If upgrading a binary installation, unpack the new MySQL binary distribution package. See Obtain and Unpack the Distribution. For packagebased installations, install the new packages.
- 5. Start the MySQL 5.7 server, using the existing data directory. For example:

```
mysqld_safe --user=mysql --datadir=/path/to/existing-datadir &
```

6. Run [mysql\\_upgrade](#page-181-0). For example:

```
mysql_upgrade -u root -p
```

[mysql\\_upgrade](#page-181-0) examines all tables in all databases for incompatibilities with the current version of MySQL. [mysql\\_upgrade](#page-181-0) also upgrades the mysql system database so that you can take advantage of new privileges or capabilities.

![](_page_57_Picture_15.jpeg)

#### **Note**

[mysql\\_upgrade](#page-181-0) does not upgrade the contents of the time zone tables or help tables. For upgrade instructions, see Section 5.1.13, "MySQL Server Time Zone Support", and Section 5.1.14, "Server-Side Help Support".

7. Shut down and restart the MySQL server to ensure that any changes made to the system tables take effect. For example:

```
mysqladmin -u root -p shutdown
mysqld_safe --user=mysql --datadir=/path/to/existing-datadir &
```

### <span id="page-57-0"></span>**Logical Upgrade**

A logical upgrade involves exporting SQL from the old MySQL instance using a backup or export utility such as mysqldump or mysqlpump, installing the new MySQL server, and applying the SQL to your new MySQL instance.

![](_page_57_Picture_22.jpeg)

#### **Note**

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysqld\\_safe](#page-144-1) is not installed. In such cases, use systemd for server startup and shutdown instead of the methods used in the following instructions. See Section 2.5.10, "Managing MySQL Server with systemd".

To perform a logical upgrade:

- 1. Review the information in [Section 2.10.1, "Before You Begin".](#page-45-1)
- 2. Export your existing data from the previous MySQL installation:

```
mysqldump -u root -p
 --add-drop-table --routines --events
 --all-databases --force > data-for-upgrade.sql
```

![](_page_58_Picture_5.jpeg)

#### **Note**

Use the --routines and --events options with mysqldump (as shown above) if your databases include stored programs. The --all-databases option includes all databases in the dump, including the mysql database that holds the system tables.

![](_page_58_Picture_8.jpeg)

#### **Important**

If you have tables that contain generated columns, use the mysqldump utility provided with MySQL 5.7.9 or higher to create your dump files. The mysqldump utility provided in earlier releases uses incorrect syntax for generated column definitions (Bug #20769542). You can use the Information Schema COLUMNS table to identify tables with generated columns.

3. Shut down the old MySQL server. For example:

```
mysqladmin -u root -p shutdown
```

- 4. Install MySQL 5.7. For installation instructions, see Chapter 2, Installing and Upgrading MySQL.
- 5. Initialize a new data directory, as described at [Section 2.9.1, "Initializing the Data Directory".](#page-32-1) For example:

```
mysqld --initialize --datadir=/path/to/5.7-datadir
```

Copy the temporary 'root'@'localhost' password displayed to your screen or written to your error log for later use.

6. Start the MySQL 5.7 server, using the new data directory. For example:

```
mysqld_safe --user=mysql --datadir=/path/to/5.7-datadir &
```

7. Reset the root password:

```
$> mysql -u root -p
Enter password: **** <- enter temporary root password
mysql> ALTER USER USER() IDENTIFIED BY 'your new password';
```

8. Load the previously created dump file into the new MySQL server. For example:

```
mysql -u root -p --force < data-for-upgrade.sql
```

![](_page_58_Picture_23.jpeg)

#### **Note**

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid\_mode=ON), if your dump file includes system tables. mysqldump issues DML instructions for the system tables which use the non-transactional MyISAM storage engine, and this combination is not permitted when GTIDs are enabled. Also be aware that loading a dump file from a server with GTIDs enabled, into another server with GTIDs enabled, causes different transaction identifiers to be generated.

9. Run [mysql\\_upgrade](#page-181-0). For example:

```
mysql_upgrade -u root -p
```

[mysql\\_upgrade](#page-181-0) examines all tables in all databases for incompatibilities with the current version of MySQL. [mysql\\_upgrade](#page-181-0) also upgrades the mysql system database so that you can take advantage of new privileges or capabilities.

![](_page_59_Picture_3.jpeg)

#### **Note**

[mysql\\_upgrade](#page-181-0) does not upgrade the contents of the time zone tables or help tables. For upgrade instructions, see Section 5.1.13, "MySQL Server Time Zone Support", and Section 5.1.14, "Server-Side Help Support".

10. Shut down and restart the MySQL server to ensure that any changes made to the system tables take effect. For example:

```
mysqladmin -u root -p shutdown
mysqld_safe --user=mysql --datadir=/path/to/5.7-datadir &
```

## <span id="page-59-0"></span>**2.10.5 Upgrading MySQL with the MySQL Yum Repository**

For supported Yum-based platforms (see Section 2.5.1, "Installing MySQL on Linux Using the MySQL Yum Repository", for a list), you can perform an in-place upgrade for MySQL (that is, replacing the old version and then running the new version using the old data files) with the MySQL Yum repository.

![](_page_59_Picture_10.jpeg)

#### **Notes**

- Before performing any update to MySQL, follow carefully the instructions in [Section 2.10, "Upgrading MySQL"](#page-45-0). Among other instructions discussed there, it is especially important to back up your database before the update.
- The following instructions assume you have installed MySQL with the MySQL Yum repository or with an RPM package directly downloaded from [MySQL](https://dev.mysql.com/downloads/) [Developer Zone's MySQL Download page;](https://dev.mysql.com/downloads/) if that is not the case, following the instructions in Section 2.5.2, "Replacing a Third-Party Distribution of MySQL Using the MySQL Yum Repository".

### **Selecting a Target Series** 1.

By default, the MySQL Yum repository updates MySQL to the latest version in the release series you have chosen during installation (see Selecting a Release Series for details), which means, for example, a 5.6.x installation is not updated to a 5.7.x release automatically. To update to another release series, you need first to disable the subrepository for the series that has been selected (by default, or by yourself) and enable the subrepository for your target series. To do that, see the general instructions given in Selecting a Release Series. For upgrading from MySQL 5.6 to 5.7, perform the reverse of the steps illustrated in Selecting a Release Series, disabling the subrepository for the MySQL 5.6 series and enabling that for the MySQL 5.7 series.

As a general rule, to upgrade from one release series to another, go to the next series rather than skipping a series. For example, if you are currently running MySQL 5.5 and wish to upgrade to 5.7, upgrade to MySQL 5.6 first before upgrading to 5.7.

![](_page_59_Picture_17.jpeg)

#### **Important**

For important information about upgrading from MySQL 5.6 to 5.7, see [Upgrading from MySQL 5.6 to 5.7.](#page-47-0)

## **Upgrading MySQL** 2.

Upgrade MySQL and its components by the following command, for platforms that are not dnfenabled:

sudo yum update mysql-server

For platforms that are dnf-enabled:

sudo dnf upgrade mysql-server

Alternatively, you can update MySQL by telling Yum to update everything on your system, which might take considerably more time. For platforms that are not dnf-enabled:

sudo yum update

For platforms that are dnf-enabled:

sudo dnf upgrade

## **Restarting MySQL** 3.

The MySQL server always restarts after an update by Yum. Once the server restarts, run [mysql\\_upgrade](#page-181-0) to check and possibly resolve any incompatibilities between the old data and the upgraded software. [mysql\\_upgrade](#page-181-0) also performs other functions; see [Section 4.4.7,](#page-181-0) ["mysql\\_upgrade — Check and Upgrade MySQL Tables"](#page-181-0) for details.

You can also update only a specific component. Use the following command to list all the installed packages for the MySQL components (for dnf-enabled systems, replace yum in the command with dnf):

```
sudo yum list installed | grep "^mysql"
```

After identifying the package name of the component of your choice, update the package with the following command, replacing package-name with the name of the package. For platforms that are not dnf-enabled:

sudo yum update package-name

For dnf-enabled platforms:

sudo dnf upgrade package-name

### **Upgrading the Shared Client Libraries**

After updating MySQL using the Yum repository, applications compiled with older versions of the shared client libraries should continue to work.

If you recompile applications and dynamically link them with the updated libraries: As typical with new versions of shared libraries where there are differences or additions in symbol versioning between the newer and older libraries (for example, between the newer, standard 5.7 shared client libraries and some older—prior or variant—versions of the shared libraries shipped natively by the Linux distributions' software repositories, or from some other sources), any applications compiled using the updated, newer shared libraries require those updated libraries on systems where the applications are deployed. If those libraries are not in place, the applications requiring the shared libraries fail. For this reason, be sure to deploy the packages for the shared libraries from MySQL on those systems. To do this, add the MySQL Yum repository to the systems (see Adding the MySQL Yum Repository) and install the latest shared libraries using the instructions given in Installing Additional MySQL Products and Components with Yum.

## <span id="page-60-0"></span>**2.10.6 Upgrading MySQL with the MySQL APT Repository**

On Debian and Ubuntu platforms, to perform an in-place upgrade of MySQL and its components, use the MySQL APT repository. See [Upgrading MySQL with the MySQL APT Repository](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/index.md#repo-qg-apt-upgrading) in [A Quick Guide](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/) [to Using the MySQL APT Repository](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/).

# <span id="page-60-1"></span>**2.10.7 Upgrading MySQL with the MySQL SLES Repository**

On the SUSE Linux Enterprise Server (SLES) platform, to perform an in-place upgrade of MySQL and its components, use the MySQL SLES repository. See [Upgrading MySQL with the MySQL SLES](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/index.md#repo-qg-sles-upgrading) [Repository](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/index.md#repo-qg-sles-upgrading) in [A Quick Guide to Using the MySQL SLES Repository.](https://dev.mysql.com/doc/mysql-sles-repo-quick-guide/en/)

## <span id="page-61-0"></span>**2.10.8 Upgrading MySQL on Windows**

There are two approaches for upgrading MySQL on Windows:

- [Using MySQL Installer](#page-61-1)
- [Using the Windows ZIP archive distribution](#page-62-1)

The approach you select depends on how the existing installation was performed. Before proceeding, review [Section 2.10, "Upgrading MySQL"](#page-45-0) for additional information on upgrading MySQL that is not specific to Windows.

![](_page_61_Picture_7.jpeg)

#### **Note**

Whichever approach you choose, always back up your current MySQL installation before performing an upgrade. See Section 7.2, "Database Backup Methods".

Upgrades between milestone releases (or from a milestone release to a GA release) are not supported. Significant development changes take place in milestone releases and you may encounter compatibility issues or problems starting the server. For instructions on how to perform a logical upgrade with a milestone release, see [Logical Upgrade.](#page-57-0)

![](_page_61_Picture_11.jpeg)

#### **Note**

MySQL Installer does not support upgrades between Community releases and Commercial releases. If you require this type of upgrade, perform it using the [ZIP archive](#page-62-1) approach.

## <span id="page-61-1"></span>**Upgrading MySQL with MySQL Installer**

Performing an upgrade with MySQL Installer is the best approach when the current server installation was performed with it and the upgrade is within the current release series. MySQL Installer does not support upgrades between release series, such as from 5.6 to 5.7, and it does not provide an upgrade indicator to prompt you to upgrade. For instructions on upgrading between release series, see [Upgrading MySQL Using the Windows ZIP Distribution.](#page-62-1)

To perform an upgrade using MySQL Installer:

- 1. Start MySQL Installer.
- 2. From the dashboard, click **Catalog** to download the latest changes to the catalog. The installed server can be upgraded only if the dashboard displays an arrow next to the version number of the server.
- 3. Click **Upgrade**. All products that have a newer version now appear in a list.

![](_page_61_Picture_20.jpeg)

#### **Note**

MySQL Installer deselects the server upgrade option for milestone releases (Pre-Release) in the same release series. In addition, it displays a warning to indicate that the upgrade is not supported, identifies the risks of continuing, and provides a summary of the steps to perform a logical upgrade manually. You can reselect server upgrade and proceed at your own risk.

4. Deselect all but the MySQL server product, unless you intend to upgrade other products at this time, and click **Next**.

- 5. Click **Execute** to start the download. When the download finishes, click **Next** to begin the upgrade operation.
- 6. Configure the server.

## <span id="page-62-1"></span>**Upgrading MySQL Using the Windows ZIP Distribution**

To perform an upgrade using the Windows ZIP archive distribution:

- 1. Download the latest Windows ZIP Archive distribution of MySQL from [https://dev.mysql.com/](https://dev.mysql.com/downloads/) [downloads/.](https://dev.mysql.com/downloads/)
- 2. If the server is running, stop it. If the server is installed as a service, stop the service with the following command from the command prompt:

```
C:\> SC STOP mysqld_service_name
```

Alternatively, use NET STOP mysqld\_service\_name.

If you are not running the MySQL server as a service, use mysqladmin to stop it. For example, before upgrading from MySQL 5.6 to 5.7, use mysqladmin from MySQL 5.6 as follows:

C:\> **"C:\Program Files\MySQL\MySQL Server 5.6\bin\mysqladmin" -u root shutdown**

![](_page_62_Picture_11.jpeg)

#### **Note**

If the MySQL root user account has a password, invoke mysqladmin with the -p option and enter the password when prompted.

- 3. Extract the ZIP archive. You may either overwrite your existing MySQL installation (usually located at C:\mysql), or install it into a different directory, such as C:\mysql5. Overwriting the existing installation is recommended.
- 4. Restart the server. For example, use the SC START mysqld\_service\_name or NET START mysqld\_service\_name command if you run MySQL as a service, or invoke [mysqld](#page-144-0) directly otherwise.
- 5. As Administrator, run [mysql\\_upgrade](#page-181-0) to check your tables, attempt to repair them if necessary, and update your grant tables if they have changed so that you can take advantage of any new capabilities. See [Section 4.4.7, "mysql\\_upgrade — Check and Upgrade MySQL Tables".](#page-181-0)
- 6. If you encounter errors, see Section 2.3.5, "Troubleshooting a Microsoft Windows MySQL Server Installation".

# <span id="page-62-0"></span>**2.10.9 Upgrading a Docker Installation of MySQL**

To upgrade a Docker installation of MySQL, refer to Upgrading a MySQL Server Container.