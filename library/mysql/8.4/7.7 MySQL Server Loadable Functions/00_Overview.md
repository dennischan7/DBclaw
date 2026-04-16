---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL supports loadable functions, that is, functions that are not built in but can be loaded at runtime (either during startup or later) to extend server capabilities, or unloaded to remove capabilities. For a table describing the available loadable functions, see Section 14.2, "Loadable Function Reference". Loadable functions contrast with built-in (native) functions, which are implemented as part of the server and are always available; for a table, see Section 14.1, "Built-In Function and Operator Reference".

![](_page_130_Picture_1.jpeg)

#### **Note**

Loadable functions previously were known as user-defined functions (UDFs). That terminology was something of a misnomer because "user-defined" also can apply to other types of functions, such as stored functions (a type of stored object written using SQL) and native functions added by modifying the server source code.

MySQL distributions include loadable functions that implement, in whole or in part, these server capabilities:

- Group Replication enables you to create a highly available distributed MySQL service across a group of MySQL server instances, with data consistency, conflict detection and resolution, and group membership services all built-in. See Chapter 20, Group Replication.
- MySQL Enterprise Edition includes functions that perform encryption operations based on the OpenSSL library. See Section 8.6, "MySQL Enterprise Encryption".
- MySQL Enterprise Edition includes functions that provide an SQL-level API for masking and deidentification operations. See Section 8.5, "MySQL Enterprise Data Masking and De-Identification".
- MySQL Enterprise Edition includes audit logging for monitoring and logging of connection and query activity. See Section 8.4.5, "MySQL Enterprise Audit", and Section 8.4.6, "The Audit Message Component".
- MySQL Enterprise Edition includes a firewall capability that implements an application-level firewall to enable database administrators to permit or deny SQL statement execution based on matching against patterns for accepted statement. See Section 8.4.7, "MySQL Enterprise Firewall".
- A query rewriter examines statements received by MySQL Server and possibly rewrites them before the server executes them. See [Section 7.6.4, "The Rewriter Query Rewrite Plugin"](#page-76-0)
- Version Tokens enables creation of and synchronization around server tokens that applications can use to prevent accessing incorrect or out-of-date data. See [Section 7.6.6, "Version Tokens".](#page-87-0)
- The MySQL Keyring provides secure storage for sensitive information. See Section 8.4.4, "The MySQL Keyring".
- A locking service provides a locking interface for application use. See [Section 7.6.9.1, "The Locking](#page-122-0) [Service".](#page-122-0)
- A function provides access to query attributes. See Section 11.6, "Query Attributes".

The following sections describe how to install and uninstall loadable functions, and how to determine at runtime which loadable functions are installed and obtain information about them.

In some cases, a loadable function is loaded by installing the component that implements the function, rather than by loading the function directly. For details about a particular loadable function, see the installation instructions for the server feature that includes it.

For information about writing loadable functions, see [Adding Functions to MySQL](https://dev.mysql.com/doc/extending-mysql/8.4/en/adding-functions.md).

# <span id="page-130-0"></span>**7.7.1 Installing and Uninstalling Loadable Functions**

Loadable functions, as the name implies, must be loaded into the server before they can be used. MySQL supports automatic function loading during server startup and manual loading thereafter.

While a loadable function is loaded, information about it is available as described in [Section 7.7.2,](#page-132-0) ["Obtaining Information About Loadable Functions"](#page-132-0).

- [Installing Loadable Functions](#page-131-0)
- [Uninstalling Loadable Functions](#page-131-1)

• [Reinstalling or Upgrading Loadable Functions](#page-131-2)

## <span id="page-131-0"></span>**Installing Loadable Functions**

To load a loadable function manually, use the CREATE FUNCTION statement. For example:

```
CREATE FUNCTION metaphon
 RETURNS STRING
 SONAME 'udf_example.so';
```

The file base name depends on your platform. Common suffixes are .so for Unix and Unix-like systems, .dll for Windows.

CREATE FUNCTION has these effects:

- It loads the function into the server to make it available immediately.
- It registers the function in the mysql.func system table to make it persistent across server restarts. For this reason, CREATE FUNCTION requires the [INSERT](#page-175-0) privilege for the mysql system database.
- It adds the function to the Performance Schema user\_defined\_functions table that provides runtime information about installed loadable functions. See [Section 7.7.2, "Obtaining Information](#page-132-0) [About Loadable Functions".](#page-132-0)

Automatic loading of loadable functions occurs during the normal server startup sequence:

- Functions registered in the mysql.func table are installed.
- Components or plugins that are installed at startup may automatically install related functions.
- Automatic function installation adds the functions to the Performance Schema user\_defined\_functions table that provides runtime information about installed functions.

If the server is started with the --skip-grant-tables option, functions registered in the mysql.func table are not loaded and are unavailable. This does not apply to functions installed automatically by a component or plugin.

## <span id="page-131-1"></span>**Uninstalling Loadable Functions**

To remove a loadable function, use the DROP FUNCTION statement. For example:

```
DROP FUNCTION metaphon;
```

DROP FUNCTION has these effects:

- It unloads the function to make it unavailable.
- It removes the function from the mysql.func system table. For this reason, DROP FUNCTION requires the [DELETE](#page-174-0) privilege for the mysql system database. With the function no longer registered in the mysql.func table, the server does not load the function during subsequent restarts.
- It removes the function from the Performance Schema user\_defined\_functions table that provides runtime information about installed loadable functions.

DROP FUNCTION cannot be used to drop a loadable function that is installed automatically by components or plugins rather than by using CREATE FUNCTION. Such a function is also dropped automatically, when the component or plugin that installed it is uninstalled.

## <span id="page-131-2"></span>**Reinstalling or Upgrading Loadable Functions**

To reinstall or upgrade the shared library associated with a loadable function, issue a DROP FUNCTION statement, upgrade the shared library, and then issue a CREATE FUNCTION statement. If you upgrade the shared library first and then use DROP FUNCTION, the server may unexpectedly shut down.

# <span id="page-132-0"></span>**7.7.2 Obtaining Information About Loadable Functions**

The Performance Schema user\_defined\_functions table contains information about the currently installed loadable functions:

```
SELECT * FROM performance_schema.user_defined_functions;
```

The mysql.func system table also lists installed loadable functions, but only those installed using CREATE FUNCTION. The user\_defined\_functions table lists loadable functions installed using CREATE FUNCTION as well as loadable functions installed automatically by components or plugins. This difference makes user\_defined\_functions preferable to mysql.func for checking which loadable functions are installed. See Section 29.12.22.10, "The user\_defined\_functions Table".

# <span id="page-132-1"></span>**7.8 Running Multiple MySQL Instances on One Machine**

In some cases, you might want to run multiple instances of MySQL on a single machine. You might want to test a new MySQL release while leaving an existing production setup undisturbed. Or you might want to give different users access to different mysqld servers that they manage themselves. (For example, you might be an Internet Service Provider that wants to provide independent MySQL installations for different customers.)

It is possible to use a different MySQL server binary per instance, or use the same binary for multiple instances, or any combination of the two approaches. For example, you might run a server from MySQL 8.3 and one from MySQL 8.4, to see how different versions handle a given workload. Or you might run multiple instances of the current production version, each managing a different set of databases.

Whether or not you use distinct server binaries, each instance that you run must be configured with unique values for several operating parameters. This eliminates the potential for conflict between instances. Parameters can be set on the command line, in option files, or by setting environment variables. See Section 6.2.2, "Specifying Program Options". To see the values used by a given instance, connect to it and execute a SHOW VARIABLES statement.

The primary resource managed by a MySQL instance is the data directory. Each instance should use a different data directory, the location of which is specified using the --datadir=dir\_name option. For methods of configuring each instance with its own data directory, and warnings about the dangers of failing to do so, see [Section 7.8.1, "Setting Up Multiple Data Directories".](#page-133-0)

In addition to using different data directories, several other options must have different values for each server instance:

• --port=port\_num

--port controls the port number for TCP/IP connections. Alternatively, if the host has multiple network addresses, you can set the bind\_address system variable to cause each server to listen to a different address.

• --socket={file\_name|pipe\_name}

--socket controls the Unix socket file path on Unix or the named-pipe name on Windows. On Windows, it is necessary to specify distinct pipe names only for those servers configured to permit named-pipe connections.

• --shared-memory-base-name=name

This option is used only on Windows. It designates the shared-memory name used by a Windows server to permit clients to connect using shared memory. It is necessary to specify distinct sharedmemory names only for those servers configured to permit shared-memory connections.

• --pid-file=file\_name

This option indicates the path name of the file in which the server writes its process ID.

If you use the following log file options, their values must differ for each server:

- --general\_log\_file=file\_name
- --log-bin[=file\_name]
- --slow\_query\_log\_file=file\_name
- --log-error[=file\_name]

For further discussion of log file options, see [Section 7.4, "MySQL Server Logs".](#page-11-0)

To achieve better performance, you can specify the following option differently for each server, to spread the load between several physical disks:

• --tmpdir=dir\_name

Having different temporary directories also makes it easier to determine which MySQL server created any given temporary file.

If you have multiple MySQL installations in different locations, you can specify the base directory for each installation with the --basedir=dir\_name option. This causes each instance to automatically use a different data directory, log files, and PID file because the default for each of those parameters is relative to the base directory. In that case, the only other options you need to specify are the - socket and --port options. Suppose that you install different versions of MySQL using tar file binary distributions. These install in different locations, so you can start the server for each installation using the command bin/mysqld\_safe under its corresponding base directory. mysqld\_safe determines the proper --basedir option to pass to mysqld, and you need specify only the - socket and --port options to mysqld\_safe.

As discussed in the following sections, it is possible to start additional servers by specifying appropriate command options or by setting environment variables. However, if you need to run multiple servers on a more permanent basis, it is more convenient to use option files to specify for each server those option values that must be unique to it. The --defaults-file option is useful for this purpose.

# <span id="page-133-0"></span>**7.8.1 Setting Up Multiple Data Directories**

Each MySQL Instance on a machine should have its own data directory. The location is specified using the --datadir=dir\_name option.

There are different methods of setting up a data directory for a new instance:

- Create a new data directory.
- Copy an existing data directory.

The following discussion provides more detail about each method.

![](_page_133_Picture_19.jpeg)

#### **Warning**

Normally, you should never have two servers that update data in the same databases. This may lead to unpleasant surprises if your operating system does not support fault-free system locking. If (despite this warning) you run multiple servers using the same data directory and they have logging enabled, you must use the appropriate options to specify log file names that are unique to each server. Otherwise, the servers try to log to the same files.

Even when the preceding precautions are observed, this kind of setup works only with MyISAM and MERGE tables, and not with any of the other storage engines. Also, this warning against sharing a data directory among servers

always applies in an NFS environment. Permitting multiple MySQL servers to access a common data directory over NFS is a very bad idea. The primary problem is that NFS is the speed bottleneck. It is not meant for such use. Another risk with NFS is that you must devise a way to ensure that two or more servers do not interfere with each other. Usually NFS file locking is handled by the lockd daemon, but at the moment there is no platform that performs locking 100% reliably in every situation.

# **Create a New Data Directory**

With this method, the data directory is in the same state as when you first install MySQL, and has the default set of MySQL accounts and no user data.

On Unix, initialize the data directory. See Section 2.9, "Postinstallation Setup and Testing".

On Windows, the data directory is included in the MySQL distribution:

- MySQL Zip archive distributions for Windows contain an unmodified data directory. You can unpack such a distribution into a temporary location, then copy it data directory to where you are setting up the new instance.
- Windows MSI package installers create and set up the data directory that the installed server uses, but also create a pristine "template" data directory named data under the installation directory. After an installation has been performed using an MSI package, the template data directory can be copied to set up additional MySQL instances.

# **Copy an Existing Data Directory**

With this method, any MySQL accounts or user data present in the data directory are carried over to the new data directory.

- 1. Stop the existing MySQL instance using the data directory. This must be a clean shutdown so that the instance flushes any pending changes to disk.
- 2. Copy the data directory to the location where the new data directory should be.
- 3. Copy the my.cnf or my.ini option file used by the existing instance. This serves as a basis for the new instance.
- 4. Modify the new option file so that any pathnames referring to the original data directory refer to the new data directory. Also, modify any other options that must be unique per instance, such as the TCP/IP port number and the log files. For a list of parameters that must be unique per instance, see [Section 7.8, "Running Multiple MySQL Instances on One Machine".](#page-132-1)
- 5. Start the new instance, telling it to use the new option file.