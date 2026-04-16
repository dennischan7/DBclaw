---
source: MySQL 8.0 Reference
title: 00_Overview
---

Third-party tools that need to determine the MySQL version from the MySQL source can read the MYSQL\_VERSION file in the top-level source directory. The file lists the pieces of the version separately. For example, if the version is MySQL 8.0.36, the file looks like this:

```
MYSQL_VERSION_MAJOR=8
MYSQL_VERSION_MINOR=0
MYSQL_VERSION_PATCH=36
MYSQL_VERSION_EXTRA=
MYSQL_VERSION_STABILITY="LTS"
```

![](_page_93_Picture_3.jpeg)

#### **Note**

In MySQL 5.7 and earlier, this file was named VERSION.

To construct a five-digit number from the version components, use this formula:

MYSQL\_VERSION\_MAJOR\*10000 + MYSQL\_VERSION\_MINOR\*100 + MYSQL\_VERSION\_PATCH

## <span id="page-93-0"></span>**2.8.10 Generating MySQL Doxygen Documentation Content**

The MySQL source code contains internal documentation written using Doxygen. The generated Doxygen content is available at<https://dev.mysql.com/doc/index-other.html>. It is also possible to generate this content locally from a MySQL source distribution using the following procedure:

1. Install doxygen 1.9.2 or later. Distributions are available here at <http://www.doxygen.nl/>.

After installing doxygen, verify the version number:

```
$> doxygen --version
1.9.2
```

2. Install [PlantUML.](http://plantuml.com/download.md)

When you install PlantUML on Windows (tested on Windows 10), you must run it at least once as administrator so it creates the registry keys. Open an administrator console and run this command:

```
$> java -jar path-to-plantuml.jar
```

The command should open a GUI window and return no errors on the console.

3. Set the PLANTUML\_JAR\_PATH environment to the location where you installed PlantUML. For example:

```
$> export PLANTUML_JAR_PATH=path-to-plantuml.jar
```

4. Install the [Graphviz](http://www.graphviz.org/) dot command.

After installing Graphviz, verify dot availability. For example:

```
$> which dot
/usr/bin/dot
$> dot -V
dot - graphviz version 2.40.1 (20161225.0304)
```

5. Change location to the top-level directory of your MySQL source distribution and do the following:

First, execute cmake:

```
$> cd mysql-source-directory
$> mkdir build
$> cd build
$> cmake ..
```

Next, generate the doxygen documentation:

```
$> make doxygen
```

Inspect the error log, which is available in the doxyerror.log file in the top-level directory. Assuming that the build executed successfully, view the generated output using a browser. For example:

\$> **firefox doxygen/html/index.html**

# <span id="page-94-1"></span>**2.9 Postinstallation Setup and Testing**

This section discusses tasks that you should perform after installing MySQL:

- If necessary, initialize the data directory and create the MySQL grant tables. For some MySQL installation methods, data directory initialization may be done for you automatically:
  - Windows installation operations performed by MySQL Installer.
  - Installation on Linux using a server RPM or Debian distribution from Oracle.
  - Installation using the native packaging system on many platforms, including Debian Linux, Ubuntu Linux, Gentoo Linux, and others.
  - Installation on macOS using a DMG distribution.

For other platforms and installation types, you must initialize the data directory manually. These include installation from generic binary and source distributions on Unix and Unix-like system, and installation from a ZIP Archive package on Windows. For instructions, see [Section 2.9.1, "Initializing](#page-94-0) [the Data Directory".](#page-94-0)

- Start the server and make sure that it can be accessed. For instructions, see [Section 2.9.2, "Starting](#page-100-0) [the Server"](#page-100-0), and [Section 2.9.3, "Testing the Server".](#page-102-0)
- Assign passwords to the initial root account in the grant tables, if that was not already done during data directory initialization. Passwords prevent unauthorized access to the MySQL server. For instructions, see [Section 2.9.4, "Securing the Initial MySQL Account".](#page-104-0)
- Optionally, arrange for the server to start and stop automatically when your system starts and stops. For instructions, see [Section 2.9.5, "Starting and Stopping MySQL Automatically".](#page-106-0)
- Optionally, populate time zone tables to enable recognition of named time zones. For instructions, see Section 7.1.15, "MySQL Server Time Zone Support".

When you are ready to create additional user accounts, you can find information on the MySQL access control system and account management in Section 8.2, "Access Control and Account Management".

# <span id="page-94-0"></span>**2.9.1 Initializing the Data Directory**

After MySQL is installed, the data directory must be initialized, including the tables in the mysql system schema:

- For some MySQL installation methods, data directory initialization is automatic, as described in [Section 2.9, "Postinstallation Setup and Testing"](#page-94-1).
- For other installation methods, you must initialize the data directory manually. These include installation from generic binary and source distributions on Unix and Unix-like systems, and installation from a ZIP Archive package on Windows.

This section describes how to initialize the data directory manually for MySQL installation methods for which data directory initialization is not automatic. For some suggested commands that enable testing whether the server is accessible and working properly, see [Section 2.9.3, "Testing the Server".](#page-102-0)

![](_page_95_Picture_1.jpeg)

### **Note**

In MySQL 8.0, the default authentication plugin has changed from mysql\_native\_password to caching\_sha2\_password, and the 'root'@'localhost' administrative account uses caching\_sha2\_password by default. If you prefer that the root account use the previous default authentication plugin (mysql\_native\_password), see [caching\\_sha2\\_password and the root Administrative Account.](#page-121-0)

The mysql\_native\_password plugin is deprecated as of MySQL 8.0.34, disabled by default as of MySQL 8.4.0, and removed as of MySQL 9.0.0.

- [Data Directory Initialization Overview](#page-95-0)
- [Data Directory Initialization Procedure](#page-96-0)
- [Server Actions During Data Directory Initialization](#page-97-0)
- [Post-Initialization root Password Assignment](#page-99-0)

## <span id="page-95-0"></span>**Data Directory Initialization Overview**

In the examples shown here, the server is intended to run under the user ID of the mysql login account. Either create the account if it does not exist (see Create a mysql User and Group), or substitute the name of a different existing login account that you plan to use for running the server.

1. Change location to the top-level directory of your MySQL installation, which is typically /usr/ local/mysql (adjust the path name for your system as necessary):

```
cd /usr/local/mysql
```

Within this directory you can find several files and subdirectories, including the bin subdirectory that contains the server, as well as client and utility programs.

2. The secure\_file\_priv system variable limits import and export operations to a specific directory. Create a directory whose location can be specified as the value of that variable:

```
mkdir mysql-files
```

Grant directory user and group ownership to the mysql user and mysql group, and set the directory permissions appropriately:

```
chown mysql:mysql mysql-files
chmod 750 mysql-files
```

3. Use the server to initialize the data directory, including the mysql schema containing the initial MySQL grant tables that determine how users are permitted to connect to the server. For example:

```
bin/mysqld --initialize --user=mysql
```

For important information about the command, especially regarding command options you might use, see [Data Directory Initialization Procedure](#page-96-0). For details about how the server performs initialization, see [Server Actions During Data Directory Initialization](#page-97-0).

Typically, data directory initialization need be done only after you first install MySQL. (For upgrades to an existing installation, perform the upgrade procedure instead; see [Chapter 3,](#page-110-0) Upgrading [MySQL](#page-110-0).) However, the command that initializes the data directory does not overwrite any existing mysql schema tables, so it is safe to run in any circumstances.

4. If you want to deploy the server with automatic support for secure connections, use the mysql\_ssl\_rsa\_setup utility to create default SSL and RSA files:

```
bin/mysql_ssl_rsa_setup
```

For more information, see Section 6.4.3, "mysql\_ssl\_rsa\_setup — Create SSL/RSA Files".

![](_page_96_Picture_2.jpeg)

#### **Note**

The mysql\_ssl\_rsa\_setup utility is deprecated as of MySQL 8.0.34.

- 5. In the absence of any option files, the server starts with its default settings. (See Section 7.1.2, "Server Configuration Defaults".) To explicitly specify options that the MySQL server should use at startup, put them in an option file such as /etc/my.cnf or /etc/mysql/my.cnf. (See [Section 6.2.2.2, "Using Option Files".](#page-196-0)) For example, you can use an option file to set the secure\_file\_priv system variable.
- 6. To arrange for MySQL to start without manual intervention at system boot time, see [Section 2.9.5,](#page-106-0) ["Starting and Stopping MySQL Automatically"](#page-106-0).
- 7. Data directory initialization creates time zone tables in the mysql schema but does not populate them. To do so, use the instructions in Section 7.1.15, "MySQL Server Time Zone Support".

## <span id="page-96-0"></span>**Data Directory Initialization Procedure**

Change location to the top-level directory of your MySQL installation, which is typically /usr/local/ mysql (adjust the path name for your system as necessary):

```
cd /usr/local/mysql
```

To initialize the data directory, invoke mysqld with the --initialize or --initialize-insecure option, depending on whether you want the server to generate a random initial password for the 'root'@'localhost' account, or to create that account with no password:

- Use --initialize for "secure by default" installation (that is, including generation of a random initial root password). In this case, the password is marked as expired and you must choose a new one.
- With --initialize-insecure, no root password is generated. This is insecure; it is assumed that you intend to assign a password to the account in a timely fashion before putting the server into production use.

For instructions on assigning a new 'root'@'localhost' password, see [Post-Initialization root](#page-99-0) [Password Assignment.](#page-99-0)

![](_page_96_Picture_15.jpeg)

### **Note**

The server writes any messages (including any initial password) to its standard error output. This may be redirected to the error log, so look there if you do not see the messages on your screen. For information about the error log, including where it is located, see Section 7.4.2, "The Error Log".

On Windows, use the --console option to direct messages to the console.

On Unix and Unix-like systems, it is important for the database directories and files to be owned by the mysql login account so that the server has read and write access to them when you run it later. To ensure this, start mysqld from the system root account and include the --user option as shown here:

```
bin/mysqld --initialize --user=mysql
bin/mysqld --initialize-insecure --user=mysql
```

Alternatively, execute mysqld while logged in as mysql, in which case you can omit the --user option from the command.

On Windows, use one of these commands:

bin\mysqld --initialize --console bin\mysqld --initialize-insecure --console

![](_page_97_Picture_2.jpeg)

#### **Note**

Data directory initialization might fail if required system libraries are missing. For example, you might see an error like this:

```
bin/mysqld: error while loading shared libraries:
libnuma.so.1: cannot open shared object file:
No such file or directory
```

If this happens, you must install the missing libraries manually or with your system's package manager. Then retry the data directory initialization command.

It might be necessary to specify other options such as --basedir or --datadir if mysqld cannot identify the correct locations for the installation directory or data directory. For example (enter the command on a single line):

```
bin/mysqld --initialize --user=mysql
 --basedir=/opt/mysql/mysql
 --datadir=/opt/mysql/mysql/data
```

Alternatively, put the relevant option settings in an option file and pass the name of that file to mysqld. For Unix and Unix-like systems, suppose that the option file name is /opt/mysql/mysql/etc/ my.cnf. Put these lines in the file:

```
[mysqld]
basedir=/opt/mysql/mysql
datadir=/opt/mysql/mysql/data
```

Then invoke mysqld as follows (enter the command on a single line, with the --defaults-file option first):

```
bin/mysqld --defaults-file=/opt/mysql/mysql/etc/my.cnf
 --initialize --user=mysql
```

On Windows, suppose that C:\my.ini contains these lines:

```
[mysqld]
basedir=C:\\Program Files\\MySQL\\MySQL Server 8.0
datadir=D:\\MySQLdata
```

Then invoke mysqld as follows (again, you should enter the command on a single line, with the - defaults-file option first):

```
bin\mysqld --defaults-file=C:\my.ini
 --initialize --console
```

![](_page_97_Picture_17.jpeg)

### **Important**

When initializing the data directory, you should not specify any options other than those used for setting directory locations such as --basedir or - datadir, and the --user option if needed. Options to be employed by the MySQL server during normal use can be set when restarting it following initialization. See the description of the --initialize option for further information.

## <span id="page-97-0"></span>**Server Actions During Data Directory Initialization**

![](_page_97_Picture_21.jpeg)

### **Note**

The data directory initialization sequence performed by the server does not substitute for the actions performed by mysql\_secure\_installation and mysql\_ssl\_rsa\_setup. See Section 6.4.2, "mysql\_secure\_installation — Improve MySQL Installation Security", and Section 6.4.3, "mysql\_ssl\_rsa\_setup — Create SSL/RSA Files".

When invoked with the --initialize or --initialize-insecure option, mysqld performs the following actions during the data directory initialization sequence:

- 1. The server checks for the existence of the data directory as follows:
  - If no data directory exists, the server creates it.
  - If the data directory exists but is not empty (that is, it contains files or subdirectories), the server exits after producing an error message:

```
[ERROR] --initialize specified but the data directory exists. Aborting.
```

In this case, remove or rename the data directory and try again.

An existing data directory is permitted to be nonempty if every entry has a name that begins with a period (.).

- 2. Within the data directory, the server creates the mysql system schema and its tables, including the data dictionary tables, grant tables, time zone tables, and server-side help tables. See Section 7.3, "The mysql System Schema".
- 3. The server initializes the system tablespace and related data structures needed to manage InnoDB tables.

![](_page_98_Picture_11.jpeg)

#### **Note**

After mysqld sets up the InnoDB system tablespace, certain changes to tablespace characteristics require setting up a whole new instance. Qualifying changes include the file name of the first file in the system tablespace and the number of undo logs. If you do not want to use the default values, make sure that the settings for the innodb\_data\_file\_path and innodb\_log\_file\_size configuration parameters are in place in the MySQL configuration file before running mysqld. Also make sure to specify as necessary other parameters that affect the creation and location of InnoDB files, such as innodb\_data\_home\_dir and innodb\_log\_group\_home\_dir.

If those options are in your configuration file but that file is not in a location that MySQL reads by default, specify the file location using the - defaults-extra-file option when you run mysqld.

4. The server creates a 'root'@'localhost' superuser account and other reserved accounts (see Section 8.2.9, "Reserved Accounts"). Some reserved accounts are locked and cannot be used by clients, but 'root'@'localhost' is intended for administrative use and you should assign it a password.

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

For instructions on assigning a new 'root'@'localhost' password, see [Post-Initialization root](#page-99-0) [Password Assignment.](#page-99-0)

- 5. The server populates the server-side help tables used for the HELP statement (see Section 15.8.3, "HELP Statement"). The server does not populate the time zone tables. To do so manually, see Section 7.1.15, "MySQL Server Time Zone Support".
- 6. If the init\_file system variable was given to name a file of SQL statements, the server executes the statements in the file. This option enables you to perform custom bootstrapping sequences.

When the server operates in bootstrap mode, some functionality is unavailable that limits the statements permitted in the file. These include statements that relate to account management (such as CREATE USER or GRANT), replication, and global transaction identifiers.

7. The server exits.

## <span id="page-99-0"></span>**Post-Initialization root Password Assignment**

After you initialize the data directory by starting the server with --initialize or --initializeinsecure, start the server normally (that is, without either of those options) and assign the 'root'@'localhost' account a new password:

- 1. Start the server. For instructions, see [Section 2.9.2, "Starting the Server".](#page-100-0)
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

```
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';
```

See also [Section 2.9.4, "Securing the Initial MySQL Account".](#page-104-0)

![](_page_99_Picture_21.jpeg)

#### **Note**

Attempts to connect to the host 127.0.0.1 normally resolve to the localhost account. However, this fails if the server is run with skip\_name\_resolve enabled. If you plan to do that, make sure that an account exists that can accept a connection. For example, to be able to connect as root using - host=127.0.0.1 or --host=::1, create these accounts:

```
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';
```

It is possible to put those statements in a file to be executed using the init\_file system variable, as discussed in [Server Actions During Data](#page-97-0) [Directory Initialization](#page-97-0).

## <span id="page-100-0"></span>**2.9.2 Starting the Server**

This section describes how start the server on Unix and Unix-like systems. (For Windows, see Section 2.3.4.5, "Starting the Server for the First Time".) For some suggested commands that you can use to test whether the server is accessible and working properly, see [Section 2.9.3, "Testing the](#page-102-0) [Server".](#page-102-0)

Start the MySQL server like this if your installation includes mysqld\_safe:

\$> **bin/mysqld\_safe --user=mysql &**

![](_page_100_Picture_6.jpeg)

### **Note**

For Linux systems on which MySQL is installed using RPM packages, server startup and shutdown is managed using systemd rather than mysqld\_safe, and mysqld\_safe is not installed. See [Section 2.5.9, "Managing MySQL](#page-47-0) [Server with systemd".](#page-47-0)

Start the server like this if your installation includes systemd support:

\$> **systemctl start mysqld**

Substitute the appropriate service name if it differs from mysqld (for example, mysql on SLES systems).

It is important that the MySQL server be run using an unprivileged (non-root) login account. To ensure this, run mysqld\_safe as root and include the --user option as shown. Otherwise, you should execute the program while logged in as mysql, in which case you can omit the --user option from the command.

For further instructions for running MySQL as an unprivileged user, see Section 8.1.5, "How to Run MySQL as a Normal User".

If the command fails immediately and prints mysqld ended, look for information in the error log (which by default is the host\_name.err file in the data directory).

If the server is unable to access the data directory it starts or read the grant tables in the mysql schema, it writes a message to its error log. Such problems can occur if you neglected to create the grant tables by initializing the data directory before proceeding to this step, or if you ran the command that initializes the data directory without the --user option. Remove the data directory and run the command with the --user option.

If you have other problems starting the server, see [Section 2.9.2.1, "Troubleshooting Problems Starting](#page-100-1) [the MySQL Server".](#page-100-1) For more information about mysqld\_safe, see Section 6.3.2, "mysqld\_safe — MySQL Server Startup Script". For more information about systemd support, see [Section 2.5.9,](#page-47-0) ["Managing MySQL Server with systemd"](#page-47-0).

### <span id="page-100-1"></span>**2.9.2.1 Troubleshooting Problems Starting the MySQL Server**

This section provides troubleshooting suggestions for problems starting the server. For additional suggestions for Windows systems, see [Section 2.3.5, "Troubleshooting a Microsoft Windows MySQL](#page-0-0) [Server Installation"](#page-0-0).

If you have problems starting the server, here are some things to try:

• Check the error log to see why the server does not start. Log files are located in the data directory (typically C:\Program Files\MySQL\MySQL Server 8.0\data on Windows, /usr/local/ mysql/data for a Unix/Linux binary distribution, and /usr/local/var for a Unix/Linux source

distribution). Look in the data directory for files with names of the form host\_name.err and host\_name.log, where host\_name is the name of your server host. Then examine the last few lines of these files. Use tail to display them:

```
$> tail host_name.err
$> tail host_name.log
```

• Specify any special options needed by the storage engines you are using. You can create a my.cnf file and specify startup options for the engines that you plan to use. If you are going to use storage engines that support transactional tables (InnoDB, NDB), be sure that you have them configured the way you want before starting the server. If you are using InnoDB tables, see Section 17.8, "InnoDB Configuration" for guidelines and Section 17.14, "InnoDB Startup Options and System Variables" for option syntax.

Although storage engines use default values for options that you omit, Oracle recommends that you review the available options and specify explicit values for any options whose defaults are not appropriate for your installation.

• Make sure that the server knows where to find the data directory. The mysqld server uses this directory as its current directory. This is where it expects to find databases and where it expects to write log files. The server also writes the pid (process ID) file in the data directory.

The default data directory location is hardcoded when the server is compiled. To determine what the default path settings are, invoke mysqld with the --verbose and --help options. If the data directory is located somewhere else on your system, specify that location with the --datadir option to mysqld or mysqld\_safe, on the command line or in an option file. Otherwise, the server does not work properly. As an alternative to the --datadir option, you can specify mysqld the location of the base directory under which MySQL is installed with the --basedir, and mysqld looks for the data directory there.

To check the effect of specifying path options, invoke mysqld with those options followed by the - verbose and --help options. For example, if you change location to the directory where mysqld is installed and then run the following command, it shows the effect of starting the server with a base directory of /usr/local:

```
$> ./mysqld --basedir=/usr/local --verbose --help
```

You can specify other options such as --datadir as well, but --verbose and --help must be the last options.

Once you determine the path settings you want, start the server without --verbose and --help.

If mysqld is currently running, you can find out what path settings it is using by executing this command:

```
$> mysqladmin variables
```

Or:

```
$> mysqladmin -h host_name variables
```

host\_name is the name of the MySQL server host.

• Make sure that the server can access the data directory. The ownership and permissions of the data directory and its contents must allow the server to read and modify them.

If you get Errcode 13 (which means Permission denied) when starting mysqld, this means that the privileges of the data directory or its contents do not permit server access. In this case, you change the permissions for the involved files and directories so that the server has the right to use them. You can also start the server as root, but this raises security issues and should be avoided.

Change location to the data directory and check the ownership of the data directory and its contents to make sure the server has access. For example, if the data directory is /usr/local/mysql/var, use this command:

```
$> ls -la /usr/local/mysql/var
```

If the data directory or its files or subdirectories are not owned by the login account that you use for running the server, change their ownership to that account. If the account is named mysql, use these commands:

```
$> chown -R mysql /usr/local/mysql/var
$> chgrp -R mysql /usr/local/mysql/var
```

Even with correct ownership, MySQL might fail to start up if there is other security software running on your system that manages application access to various parts of the file system. In this case, reconfigure that software to enable mysqld to access the directories it uses during normal operation.

• Verify that the network interfaces the server wants to use are available.

If either of the following errors occur, it means that some other program (perhaps another mysqld server) is using the TCP/IP port or Unix socket file that mysqld is trying to use:

```
Can't start server: Bind on TCP/IP port: Address already in use
Can't start server: Bind on unix socket...
```

Use ps to determine whether you have another mysqld server running. If so, shut down the server before starting mysqld again. (If another server is running, and you really want to run multiple servers, you can find information about how to do so in Section 7.8, "Running Multiple MySQL Instances on One Machine".)

If no other server is running, execute the command telnet your\_host\_name tcp\_ip\_port\_number. (The default MySQL port number is 3306.) Then press Enter a couple of times. If you do not get an error message like telnet: Unable to connect to remote host: Connection refused, some other program is using the TCP/IP port that mysqld is trying to use. Track down what program this is and disable it, or tell mysqld to listen to a different port with the --port option. In this case, specify the same non-default port number for client programs when connecting to the server using TCP/IP.

Another reason the port might be inaccessible is that you have a firewall running that blocks connections to it. If so, modify the firewall settings to permit access to the port.

If the server starts but you cannot connect to it, make sure that you have an entry in /etc/hosts that looks like this:

```
127.0.0.1 localhost
```

• If you cannot get mysqld to start, try to make a trace file to find the problem by using the --debug option. See Section 7.9.4, "The DBUG Package".

# <span id="page-102-0"></span>**2.9.3 Testing the Server**

After the data directory is initialized and you have started the server, perform some simple tests to make sure that it works satisfactorily. This section assumes that your current location is the MySQL installation directory and that it has a bin subdirectory containing the MySQL programs used here. If that is not true, adjust the command path names accordingly.

Alternatively, add the bin directory to your PATH environment variable setting. That enables your shell (command interpreter) to find MySQL programs properly, so that you can run a program by typing only its name, not its path name. See Section 6.2.9, "Setting Environment Variables".

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
mysqladmin Ver 14.12 Distrib 8.0.45, for pc-linux-gnu on i686
...
Server version 8.0.45
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

Verify that you can start the server again. Do this by using mysqld\_safe or by invoking mysqld directly. For example:

```
$> bin/mysqld_safe --user=mysql &
```

If mysqld\_safe fails, see [Section 2.9.2.1, "Troubleshooting Problems Starting the MySQL Server"](#page-100-1).

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
| sys |
+--------------------+
```

The list of installed databases may vary, but always includes at least mysql and information\_schema.

If you specify a database name, mysqlshow displays a list of the tables within the database:

```
$> bin/mysqlshow mysql
Database: mysql
+---------------------------+
```

```
| Tables |
+---------------------------+
| columns_priv |
| component |
| db |
| default_roles |
| engine_cost |
| func |
| general_log |
| global_grants |
| gtid_executed |
| help_category |
| help_keyword |
| help_relation |
| help_topic |
| innodb_index_stats |
| innodb_table_stats |
| ndb_binlog_index |
| password_history |
| plugin |
| procs_priv |
| proxies_priv |
| role_edges |
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

Use the mysql program to select information from a table in the mysql schema:

```
$> bin/mysql -e "SELECT User, Host, plugin FROM mysql.user" mysql
+------+-----------+-----------------------+
| User | Host | plugin |
+------+-----------+-----------------------+
| root | localhost | caching_sha2_password |
+------+-----------+-----------------------+
```

At this point, your server is running and you can access it. To tighten security if you have not yet assigned a password to the initial account, follow the instructions in [Section 2.9.4, "Securing the Initial](#page-104-0) [MySQL Account".](#page-104-0)

For more information about mysql, mysqladmin, and mysqlshow, see Section 6.5.1, "mysql — The MySQL Command-Line Client", Section 6.5.2, "mysqladmin — A MySQL Server Administration Program", and Section 6.5.7, "mysqlshow — Display Database, Table, and Column Information".

# <span id="page-104-0"></span>**2.9.4 Securing the Initial MySQL Account**

The MySQL installation process involves initializing the data directory, including the grant tables in the mysql system schema that define MySQL accounts. For details, see [Section 2.9.1, "Initializing the](#page-94-0) [Data Directory"](#page-94-0).

This section describes how to assign a password to the initial root account created during the MySQL installation procedure, if you have not already done so.

![](_page_104_Picture_9.jpeg)

### **Note**

Alternative means for performing the process described in this section:

- On Windows, you can perform the process during installation with MySQL Installer (see Section 2.3.3, "MySQL Installer for Windows").
- On all platforms, the MySQL distribution includes mysql\_secure\_installation, a command-line utility that automates much of the process of securing a MySQL installation.
- On all platforms, MySQL Workbench is available and offers the ability to manage user accounts (see Chapter 33, MySQL Workbench ).

A password may already be assigned to the initial account under these circumstances:

- On Windows, installations performed using MySQL Installer give you the option of assigning a password.
- Installation using the macOS installer generates an initial random password, which the installer displays to the user in a dialog box.
- Installation using RPM packages generates an initial random password, which is written to the server error log.
- Installations using Debian packages give you the option of assigning a password.
- For data directory initialization performed manually using mysqld --initialize, mysqld generates an initial random password, marks it expired, and writes it to the server error log. See [Section 2.9.1, "Initializing the Data Directory".](#page-94-0)

The mysql.user grant table defines the initial MySQL user account and its access privileges. Installation of MySQL creates only a 'root'@'localhost' superuser account that has all privileges and can do anything. If the root account has an empty password, your MySQL installation is unprotected: Anyone can connect to the MySQL server as root without a password and be granted all privileges.

The 'root'@'localhost' account also has a row in the mysql.proxies\_priv table that enables granting the PROXY privilege for ''@'', that is, for all users and all hosts. This enables root to set up proxy users, as well as to delegate to other accounts the authority to set up proxy users. See Section 8.2.19, "Proxy Users".

To assign a password for the initial MySQL root account, use the following procedure. Replace root-password in the examples with the password that you want to use.

Start the server if it is not running. For instructions, see [Section 2.9.2, "Starting the Server"](#page-100-0).

The initial root account may or may not have a password. Choose whichever of the following procedures applies:

- If the root account exists with an initial random password that has been expired, connect to the server as root using that password, then choose a new password. This is the case if the data directory was initialized using mysqld --initialize, either manually or using an installer that does not give you the option of specifying a password during the install operation. Because the password exists, you must use it to connect to the server. But because the password is expired, you cannot use the account for any purpose other than to choose a new password, until you do choose one.
  - 1. If you do not know the initial random password, look in the server error log.
  - 2. Connect to the server as root using the password:

```
$> mysql -u root -p
Enter password: (enter the random root password here)
```

3. Choose a new password to replace the random password:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';
```

- If the root account exists but has no password, connect to the server as root using no password, then assign a password. This is the case if you initialized the data directory using mysqld - initialize-insecure.
  - 1. Connect to the server as root using no password:

```
$> mysql -u root --skip-password
```

2. Assign a password:

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';
```

After assigning the root account a password, you must supply that password whenever you connect to the server using the account. For example, to connect to the server using the mysql client, use this command:

```
$> mysql -u root -p
Enter password: (enter root password here)
```

To shut down the server with mysqladmin, use this command:

```
$> mysqladmin -u root -p shutdown
Enter password: (enter root password here)
```

![](_page_106_Picture_12.jpeg)

#### **Note**

For additional information about setting passwords, see Section 8.2.14, "Assigning Account Passwords". If you forget your root password after setting it, see Section B.3.3.2, "How to Reset the Root Password".

To set up additional accounts, see Section 8.2.8, "Adding Accounts, Assigning Privileges, and Dropping Accounts".

# <span id="page-106-0"></span>**2.9.5 Starting and Stopping MySQL Automatically**

This section discusses methods for starting and stopping the MySQL server.

Generally, you start the mysqld server in one of these ways:

- Invoke mysqld directly. This works on any platform.
- On Windows, you can set up a MySQL service that runs automatically when Windows starts. See Section 2.3.4.8, "Starting MySQL as a Windows Service".
- On Unix and Unix-like systems, you can invoke mysqld\_safe, which tries to determine the proper options for mysqld and then runs it with those options. See Section 6.3.2, "mysqld\_safe — MySQL Server Startup Script".
- On Linux systems that support systemd, you can use it to control the server. See [Section 2.5.9,](#page-47-0) ["Managing MySQL Server with systemd"](#page-47-0).
- On systems that use System V-style run directories (that is, /etc/init.d and run-level specific directories), invoke mysql.server. This script is used primarily at system startup and shutdown. It usually is installed under the name mysql. The mysql.server script starts the server by invoking mysqld\_safe. See Section 6.3.3, "mysql.server — MySQL Server Startup Script".
- On macOS, install a launchd daemon to enable automatic MySQL startup at system startup. The daemon starts the server by invoking mysqld\_safe. For details, see [Section 2.4.3, "Installing and](#page-11-0)

[Using the MySQL Launch Daemon".](#page-11-0) A MySQL Preference Pane also provides control for starting and stopping MySQL through the System Preferences. See [Section 2.4.4, "Installing and Using the](#page-15-0) [MySQL Preference Pane"](#page-15-0).

• On Solaris, use the service management framework (SMF) system to initiate and control MySQL startup.

systemd, the mysqld\_safe and mysql.server scripts, Solaris SMF, and the macOS Startup Item (or MySQL Preference Pane) can be used to start the server manually, or automatically at system startup time. systemd, mysql.server, and the Startup Item also can be used to stop the server.

The following table shows which option groups the server and startup scripts read from option files.

**Table 2.15 MySQL Startup Scripts and Supported Server Option Groups**

| Script       | Option Groups                                 |
|--------------|-----------------------------------------------|
| mysqld       | [mysqld], [server],<br>[mysqld-major_version] |
| mysqld_safe  | [mysqld], [server], [mysqld_safe]             |
| mysql.server | [mysqld], [mysql.server], [server]            |

[mysqld-major\_version] means that groups with names like [mysqld-5.7] and [mysqld-8.0] are read by servers having versions 5.7.x, 8.0.x, and so forth. This feature can be used to specify options that can be read only by servers within a given release series.

For backward compatibility, mysql.server also reads the [mysql\_server] group and mysqld\_safe also reads the [safe\_mysqld] group. To be current, you should update your option files to use the [mysql.server] and [mysqld\_safe] groups instead.

For more information on MySQL configuration files and their structure and contents, see [Section 6.2.2.2, "Using Option Files".](#page-196-0)