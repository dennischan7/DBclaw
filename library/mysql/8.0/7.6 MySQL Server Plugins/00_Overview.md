---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL supports an plugin API that enables creation of server plugins. Plugins can be loaded at server startup, or loaded and unloaded at runtime without restarting the server. The plugins supported by this interface include, but are not limited to, storage engines, INFORMATION\_SCHEMA tables, full-text parser plugins, and server extensions.

MySQL distributions include several plugins that implement server extensions:

- Plugins for authenticating attempts by clients to connect to MySQL Server. Plugins are available for several authentication protocols. See [Section 8.2.17, "Pluggable Authentication".](#page-182-0)
- A connection control plugin that enables administrators to introduce an increasing delay after a certain number of consecutive failed client connection attempts. See Section 8.4.2, "Connection Control Plugins".
- A password-validation plugin implements password strength policies and assesses the strength of potential passwords. See Section 8.4.3, "The Password Validation Component".
- Semisynchronous replication plugins implement an interface to replication capabilities that permit the source to proceed as long as at least one replica has responded to each transaction. See Section 19.4.10, "Semisynchronous Replication".
- Group Replication enables you to create a highly available distributed MySQL service across a group of MySQL server instances, with data consistency, conflict detection and resolution, and group membership services all built-in. See Chapter 20, Group Replication.
- MySQL Enterprise Edition includes a thread pool plugin that manages connection threads to increase server performance by efficiently managing statement execution threads for large numbers of client connections. See [Section 7.6.3, "MySQL Enterprise Thread Pool"](#page-6-0).
- MySQL Enterprise Edition includes an audit plugin for monitoring and logging of connection and query activity. See Section 8.4.5, "MySQL Enterprise Audit".
- MySQL Enterprise Edition includes a firewall plugin that implements an application-level firewall to enable database administrators to permit or deny SQL statement execution based on matching against allowlists of accepted statement patterns. See Section 8.4.7, "MySQL Enterprise Firewall".
- Query rewrite plugins examine statements received by MySQL Server and possibly rewrite them before the server executes them. See [Section 7.6.4, "The Rewriter Query Rewrite Plugin",](#page-14-0) and [Section 7.6.5, "The ddl\\_rewriter Plugin"](#page-23-0).
- Version Tokens enables creation of and synchronization around server tokens that applications can use to prevent accessing incorrect or out-of-date data. Version Tokens is based on a plugin library

that implements a version\_tokens plugin and a set of loadable functions. See [Section 7.6.6,](#page-25-0) ["Version Tokens"](#page-25-0).

• Keyring plugins provide secure storage for sensitive information. See Section 8.4.4, "The MySQL Keyring".

In MySQL 8.0.24, MySQL Keyring began transitioning from plugins to use the component infrastructure, facilitated using the plugin named daemon\_keyring\_proxy\_plugin that acts as a bridge between the plugin and component service APIs. See [Section 7.6.8, "The Keyring Proxy](#page-62-0) [Bridge Plugin".](#page-62-0)

- X Plugin extends MySQL Server to be able to function as a document store. Running X Plugin enables MySQL Server to communicate with clients using the X Protocol, which is designed to expose the ACID compliant storage abilities of MySQL as a document store. See Section 22.5, "X Plugin".
- Clone permits cloning InnoDB data from a local or remote MySQL server instance. See [Section 7.6.7, "The Clone Plugin"](#page-37-0).
- Test framework plugins test server services. For information about these plugins, see the Plugins for Testing Plugin Services section of the MySQL Server Doxygen documentation, available at [https://](https://dev.mysql.com/doc/index-other.md) [dev.mysql.com/doc/index-other.html](https://dev.mysql.com/doc/index-other.md).

The following sections describe how to install and uninstall plugins, and how to determine at runtime which plugins are installed and obtain information about them. For information about writing plugins, see [The MySQL Plugin API.](https://dev.mysql.com/doc/extending-mysql/8.0/en/plugin-api.md)

## <span id="page-1-2"></span>**7.6.1 Installing and Uninstalling Plugins**

Server plugins must be loaded into the server before they can be used. MySQL supports plugin loading at server startup and runtime. It is also possible to control the activation state of loaded plugins at startup, and to unload them at runtime.

While a plugin is loaded, information about it is available as described in [Section 7.6.2, "Obtaining](#page-5-0) [Server Plugin Information"](#page-5-0).

- [Installing Plugins](#page-1-0)
- [Controlling Plugin Activation State](#page-3-0)
- [Uninstalling Plugins](#page-4-0)
- [Plugins and Loadable Functions](#page-5-1)

## <span id="page-1-0"></span>**Installing Plugins**

Before a server plugin can be used, it must be installed using one of the following methods. In the descriptions, plugin\_name stands for a plugin name such as innodb, csv, or validate\_password.

- [Built-in Plugins](#page-1-1)
- [Plugins Registered in the mysql.plugin System Table](#page-2-0)
- [Plugins Named with Command-Line Options](#page-2-1)
- [Plugins Installed with the INSTALL PLUGIN Statement](#page-3-1)

### <span id="page-1-1"></span>**Built-in Plugins**

A built-in plugin is known by the server automatically. By default, the server enables the plugin at startup. Some built-in plugins permit this to be changed with the --plugin\_name[=activation\_state] option.

### <span id="page-2-0"></span>**Plugins Registered in the mysql.plugin System Table**

The mysql.plugin system table serves as a registry of plugins (other than built-in plugins, which need not be registered). During the normal startup sequence, the server loads plugins registered in the table. By default, for a plugin loaded from the mysql.plugin table, the server also enables the plugin. This can be changed with the --plugin\_name[=activation\_state] option.

If the server is started with the --skip-grant-tables option, plugins registered in the mysql.plugin table are not loaded and are unavailable.

### <span id="page-2-1"></span>**Plugins Named with Command-Line Options**

A plugin located in a plugin library file can be loaded at server startup with the --pluginload, --plugin-load-add, or --early-plugin-load option. Normally, for a plugin loaded at startup, the server also enables the plugin. This can be changed with the --plugin\_name[=activation\_state] option.

The --plugin-load and --plugin-load-add options load plugins after built-in plugins and storage engines have initialized during the server startup sequence. The --early-plugin-load option is used to load plugins that must be available prior to initialization of built-in plugins and storage engines.

The value of each plugin-loading option is a semicolon-separated list of plugin\_library and name=plugin\_library values. Each plugin\_library is the name of a library file that contains plugin code, and each name is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads only the named plugin from the library. The server looks for plugin library files in the directory named by the plugin\_dir system variable.

Plugin-loading options do not register any plugin in the mysql.plugin table. For subsequent restarts, the server loads the plugin again only if --plugin-load, --plugin-load-add, or --earlyplugin-load is given again. That is, the option produces a one-time plugin-installation operation that persists for a single server invocation.

--plugin-load, --plugin-load-add, and --early-plugin-load enable plugins to be loaded even when --skip-grant-tables is given (which causes the server to ignore the mysql.plugin table). --plugin-load, --plugin-load-add, and --early-plugin-load also enable plugins to be loaded at startup that cannot be loaded at runtime.

The --plugin-load-add option complements the --plugin-load option:

- Each instance of --plugin-load resets the set of plugins to load at startup, whereas --pluginload-add adds a plugin or plugins to the set of plugins to be loaded without resetting the current set. Consequently, if multiple instances of --plugin-load are specified, only the last one applies. With multiple instances of --plugin-load-add, all of them apply.
- The argument format is the same as for --plugin-load, but multiple instances of --pluginload-add can be used to avoid specifying a large set of plugins as a single long unwieldy - plugin-load argument.
- --plugin-load-add can be given in the absence of --plugin-load, but any instance of plugin-load-add that appears before --plugin-load has no effect because --plugin-load resets the set of plugins to load.

For example, these options:

```
--plugin-load=x --plugin-load-add=y
```

are equivalent to these options:

```
--plugin-load-add=x --plugin-load-add=y
```

and are also equivalent to this option:

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

### <span id="page-3-1"></span>**Plugins Installed with the INSTALL PLUGIN Statement**

A plugin located in a plugin library file can be loaded at runtime with the INSTALL PLUGIN statement. The statement also registers the plugin in the mysql.plugin table to cause the server to load it on subsequent restarts. For this reason, INSTALL PLUGIN requires the [INSERT](#page-115-0) privilege for the mysql.plugin table.

The plugin library file base name depends on your platform. Common suffixes are .so for Unix and Unix-like systems, .dll for Windows.

Example: The --plugin-load-add option installs a plugin at server startup. To install a plugin named myplugin from a plugin library file named somepluglib.so, use these lines in a my.cnf file:

```
[mysqld]
plugin-load-add=myplugin=somepluglib.so
```

In this case, the plugin is not registered in mysql.plugin. Restarting the server without the - plugin-load-add option causes the plugin not to be loaded at startup.

Alternatively, the INSTALL PLUGIN statement causes the server to load the plugin code from the library file at runtime:

```
INSTALL PLUGIN myplugin SONAME 'somepluglib.so';
```

INSTALL PLUGIN also causes "permanent" plugin registration: The plugin is listed in the mysql.plugin table to ensure that the server loads it on subsequent restarts.

Many plugins can be loaded either at server startup or at runtime. However, if a plugin is designed such that it must be loaded and initialized during server startup, attempts to load it at runtime using INSTALL PLUGIN produce an error:

```
mysql> INSTALL PLUGIN myplugin SONAME 'somepluglib.so';
ERROR 1721 (HY000): Plugin 'myplugin' is marked as not dynamically
installable. You have to stop the server to install it.
```

In this case, you must use --plugin-load, --plugin-load-add, or --early-plugin-load.

If a plugin is named both using a --plugin-load, --plugin-load-add, or --early-pluginload option and (as a result of an earlier INSTALL PLUGIN statement) in the mysql.plugin table, the server starts but writes these messages to the error log:

```
[ERROR] Function 'plugin_name' already exists
[Warning] Couldn't load plugin named 'plugin_name'
with soname 'plugin_object_file'.
```

## <span id="page-3-0"></span>**Controlling Plugin Activation State**

If the server knows about a plugin when it starts (for example, because the plugin is named using a --plugin-load-add option or is registered in the mysql.plugin table), the server loads and enables the plugin by default. It is possible to control activation state for such a plugin using a --plugin\_name[=activation\_state] startup option, where plugin\_name is the name of the plugin to affect, such as innodb, csv, or validate\_password. As with other options, dashes and underscores are interchangeable in option names. Also, activation state values are not case-sensitive. For example, --my\_plugin=ON and --my-plugin=on are equivalent.

• --plugin\_name=OFF

Tells the server to disable the plugin. This may not be possible for certain built-in plugins, such as mysql\_native\_password.

• --plugin\_name[=ON]

Tells the server to enable the plugin. (Specifying the option as --plugin\_name without a value has the same effect.) If the plugin fails to initialize, the server runs with the plugin disabled.

• --plugin\_name=FORCE

Tells the server to enable the plugin, but if plugin initialization fails, the server does not start. In other words, this option forces the server to run with the plugin enabled or not at all.

• --plugin\_name=FORCE\_PLUS\_PERMANENT

Like FORCE, but in addition prevents the plugin from being unloaded at runtime. If a user attempts to do so with UNINSTALL PLUGIN, an error occurs.

Plugin activation states are visible in the LOAD\_OPTION column of the Information Schema PLUGINS table.

Suppose that CSV, BLACKHOLE, and ARCHIVE are built-in pluggable storage engines and that you want the server to load them at startup, subject to these conditions: The server is permitted to run if CSV initialization fails, must require that BLACKHOLE initialization succeeds, and should disable ARCHIVE. To accomplish that, use these lines in an option file:

```
[mysqld]
csv=ON
blackhole=FORCE
archive=OFF
```

The --enable-plugin\_name option format is a synonym for --plugin\_name=ON. The --disable-plugin\_name and --skip-plugin\_name option formats are synonyms for --plugin\_name=OFF.

If a plugin is disabled, either explicitly with OFF or implicitly because it was enabled with ON but fails to initialize, aspects of server operation requiring the plugin change. For example, if the plugin implements a storage engine, existing tables for the storage engine become inaccessible, and attempts to create new tables for the storage engine result in tables that use the default storage engine unless the NO\_ENGINE\_SUBSTITUTION SQL mode is enabled to cause an error to occur instead.

Disabling a plugin may require adjustment to other options. For example, if you start the server using --skip-innodb to disable InnoDB, other innodb\_xxx options likely also need to be omitted at startup. In addition, because InnoDB is the default storage engine, it cannot start unless you specify another available storage engine with --default\_storage\_engine. You must also set - default\_tmp\_storage\_engine.

## <span id="page-4-0"></span>**Uninstalling Plugins**

At runtime, the UNINSTALL PLUGIN statement disables and uninstalls a plugin known to the server. The statement unloads the plugin and removes it from the mysql.plugin system table, if it is registered there. For this reason, UNINSTALL PLUGIN statement requires the [DELETE](#page-115-1) privilege for the mysql.plugin table. With the plugin no longer registered in the table, the server does not load the plugin during subsequent restarts.

UNINSTALL PLUGIN can unload a plugin regardless of whether it was loaded at runtime with INSTALL PLUGIN or at startup with a plugin-loading option, subject to these conditions:

- It cannot unload plugins that are built in to the server. These can be identified as those that have a library name of NULL in the output from the Information Schema PLUGINS table or SHOW PLUGINS.
- It cannot unload plugins for which the server was started with --plugin\_name=FORCE\_PLUS\_PERMANENT, which prevents plugin unloading at runtime. These can be identified from the LOAD\_OPTION column of the PLUGINS table.

To uninstall a plugin that currently is loaded at server startup with a plugin-loading option, use this procedure.

- 1. Remove from the my.cnf file any options and system variables related to the plugin. If any plugin system variables were persisted to the mysqld-auto.cnf file, remove them using RESET PERSIST var\_name for each one to remove it.
- 2. Restart the server.
- 3. Plugins normally are installed using either a plugin-loading option at startup or with INSTALL PLUGIN at runtime, but not both. However, removing options for a plugin from the my.cnf file may not be sufficient to uninstall it if at some point INSTALL PLUGIN has also been used. If the plugin still appears in the output from PLUGINS or SHOW PLUGINS, use UNINSTALL PLUGIN to remove it from the mysql.plugin table. Then restart the server again.

## <span id="page-5-1"></span>**Plugins and Loadable Functions**

A plugin when installed may also automatically install related loadable functions. If so, the plugin when uninstalled also automatically uninstalls those functions.

## <span id="page-5-0"></span>**7.6.2 Obtaining Server Plugin Information**

There are several ways to determine which plugins are installed in the server:

• The Information Schema PLUGINS table contains a row for each loaded plugin. Any that have a PLUGIN\_LIBRARY value of NULL are built in and cannot be unloaded.

```
mysql> SELECT * FROM INFORMATION_SCHEMA.PLUGINS\G
*************************** 1. row ***************************
 PLUGIN_NAME: binlog
 PLUGIN_VERSION: 1.0
 PLUGIN_STATUS: ACTIVE
 PLUGIN_TYPE: STORAGE ENGINE
 PLUGIN_TYPE_VERSION: 50158.0
 PLUGIN_LIBRARY: NULL
PLUGIN_LIBRARY_VERSION: NULL
 PLUGIN_AUTHOR: Oracle Corporation
 PLUGIN_DESCRIPTION: This is a pseudo storage engine to represent the binlog in a transaction
 PLUGIN_LICENSE: GPL
 LOAD_OPTION: FORCE
...
*************************** 10. row ***************************
 PLUGIN_NAME: InnoDB
 PLUGIN_VERSION: 1.0
 PLUGIN_STATUS: ACTIVE
 PLUGIN_TYPE: STORAGE ENGINE
 PLUGIN_TYPE_VERSION: 50158.0
 PLUGIN_LIBRARY: ha_innodb_plugin.so
PLUGIN_LIBRARY_VERSION: 1.0
 PLUGIN_AUTHOR: Oracle Corporation
 PLUGIN_DESCRIPTION: Supports transactions, row-level locking,
 and foreign keys
 PLUGIN_LICENSE: GPL
 LOAD_OPTION: ON
...
```

• The SHOW PLUGINS statement displays a row for each loaded plugin. Any that have a Library value of NULL are built in and cannot be unloaded.

```
mysql> SHOW PLUGINS\G

***********************************
```

• The mysql.plugin table shows which plugins have been registered with INSTALL PLUGIN. The table contains only plugin names and library file names, so it does not provide as much information as the PLUGINS table or the SHOW PLUGINS statement.

## <span id="page-6-0"></span>7.6.3 MySQL Enterprise Thread Pool

![](_page_6_Picture_4.jpeg)

#### Note

MySQL Enterprise Thread Pool is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, <a href="https://www.mysgl.com/products/">https://www.mysgl.com/products/</a>.

MySQL Enterprise Edition includes MySQL Enterprise Thread Pool, implemented using a server plugin. The default thread-handling model in MySQL Server executes statements using one thread per client connection. As more clients connect to the server and execute statements, overall performance degrades. The thread pool plugin provides an alternative thread-handling model designed to reduce overhead and improve performance. The plugin implements a thread pool that increases server performance by efficiently managing statement execution threads for large numbers of client connections.

The thread pool addresses several problems of the model that uses one thread per connection:

- Too many thread stacks make CPU caches almost useless in highly parallel execution workloads. The thread pool promotes thread stack reuse to minimize the CPU cache footprint.
- With too many threads executing in parallel, context switching overhead is high. This also presents a
  challenge to the operating system scheduler. The thread pool controls the number of active threads
  to keep the parallelism within the MySQL server at a level that it can handle and that is appropriate
  for the server host on which MySQL is executing.
- Too many transactions executing in parallel increases resource contention. In InnoDB, this increases the time spent holding central mutexes. The thread pool controls when transactions start to ensure that not too many execute in parallel.

#### **Additional Resources**

Section A.15, "MySQL 8.0 FAQ: MySQL Enterprise Thread Pool"

#### 7.6.3.1 Thread Pool Elements

MySQL Enterprise Thread Pool comprises these elements:

- A plugin library file implements a plugin for the thread pool code as well as several associated monitoring tables that provide information about thread pool operation:
  - As of MySQL 8.0.14, the monitoring tables are Performance Schema tables; see Section 29.12.16, "Performance Schema Thread Pool Tables".

• Prior to MySQL 8.0.14, the monitoring tables are INFORMATION\_SCHEMA tables; see Section 28.5, "INFORMATION\_SCHEMA Thread Pool Tables".

The INFORMATION\_SCHEMA tables now are deprecated; expect them to be removed in a future version of MySQL. Applications should transition away from the INFORMATION\_SCHEMA tables to the Performance Schema tables. For example, if an application uses this query:

```
SELECT * FROM INFORMATION_SCHEMA.TP_THREAD_STATE;
```

The application should use this query instead:

SELECT \* FROM performance\_schema.tp\_thread\_state;

![](_page_7_Picture_6.jpeg)

#### **Note**

If you do not load all the monitoring tables, some or all MySQL Enterprise Monitor thread pool graphs may be empty.

For a detailed description of how the thread pool works, see [Section 7.6.3.3, "Thread Pool](#page-9-0) [Operation"](#page-9-0).

• Several system variables are related to the thread pool. The thread\_handling system variable has a value of loaded-dynamically when the server successfully loads the thread pool plugin.

The other related system variables are implemented by the thread pool plugin and are not available unless it is enabled. For information about using these variables, see [Section 7.6.3.3, "Thread Pool](#page-9-0) [Operation"](#page-9-0), and [Section 7.6.3.4, "Thread Pool Tuning"](#page-12-0).

• The Performance Schema has instruments that expose information about the thread pool and may be used to investigate operational performance. To identify them, use this query:

```
SELECT * FROM performance_schema.setup_instruments
WHERE NAME LIKE '%thread_pool%';
```

For more information, see Chapter 29, MySQL Performance Schema.