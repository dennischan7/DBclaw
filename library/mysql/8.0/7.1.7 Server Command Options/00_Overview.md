---
source: MySQL 8.0 Reference
title: 00_Overview
---

When you start the mysqld server, you can specify program options using any of the methods described in Section 6.2.2, "Specifying Program Options". The most common methods are to provide options in an option file or on the command line. However, in most cases it is desirable to make sure that the server uses the same options each time it runs. The best way to ensure this is to list them in an option file. See Section 6.2.2.2, "Using Option Files". That section also describes option file format and syntax.

mysqld reads options from the [mysqld] and [server] groups. mysqld\_safe reads options from the [mysqld], [server], [mysqld\_safe], and [safe\_mysqld] groups. mysql.server reads options from the [mysqld] and [mysql.server] groups.

mysqld accepts many command options. For a brief summary, execute this command:

```
mysqld --help
```

To see the full list, use this command:

```
mysqld --verbose --help
```

Some of the items in the list are actually system variables that can be set at server startup. These can be displayed at runtime using the SHOW VARIABLES statement. Some items displayed by the preceding mysqld command do not appear in SHOW VARIABLES output; this is because they are options only and not system variables.

The following list shows some of the most common server options. Additional options are described in other sections:

- Options that affect security: See Section 8.1.4, "Security-Related mysqld Options and Variables".
- SSL-related options: See Command Options for Encrypted Connections.
- Binary log control options: See Section 7.4.4, "The Binary Log".
- Replication-related options: See Section 19.1.6, "Replication and Binary Logging Options and Variables".
- Options for loading plugins such as pluggable storage engines: See Section 7.6.1, "Installing and Uninstalling Plugins".
- Options specific to particular storage engines: See Section 17.14, "InnoDB Startup Options and System Variables" and Section 18.2.1, "MyISAM Startup Options".

Some options control the size of buffers or caches. For a given buffer, the server might need to allocate internal data structures. These structures typically are allocated from the total memory allocated to the buffer, and the amount of space required might be platform dependent. This means that when you assign a value to an option that controls a buffer size, the amount of space actually available might differ from the value assigned. In some cases, the amount might be less than the value assigned. It is also possible that the server adjusts a value upward. For example, if you assign a value of 0 to an option for which the minimal value is 1024, the server sets the value to 1024.

Values for buffer sizes, lengths, and stack sizes are given in bytes unless otherwise specified.

Some options take file name values. Unless otherwise specified, the default file location is the data directory if the value is a relative path name. To specify the location explicitly, use an absolute path name. Suppose that the data directory is /var/mysql/data. If a file-valued option is given as a relative path name, it is located under /var/mysql/data. If the value is an absolute path name, its location is as given by the path name.

You can also set the values of server system variables at server startup by using variable names as options. To assign a value to a server system variable, use an option of the form --var\_name=value. For example, --sort\_buffer\_size=384M sets the sort\_buffer\_size variable to a value of 384MB.

When you assign a value to a variable, MySQL might automatically correct the value to stay within a given range, or adjust the value to the closest permissible value if only certain values are permitted.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement, specify this maximum by using an option of the form --maximum-var\_name=value at server startup.

You can change the values of most system variables at runtime with the SET statement. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

[Section 7.1.8, "Server System Variables",](#page-81-1) provides a full description for all variables, and additional information for setting them at server startup and runtime. For information on changing system variables, see Section 7.1.1, "Configuring the Server".

<span id="page-53-0"></span>• [--help](#page-53-0), -?

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Display a short help message and exit. Use both the [--verbose](#page-81-0) and [--help](#page-53-0) options to see the full message.

<span id="page-53-1"></span>• [--admin-ssl](#page-53-1), [--skip-admin-ssl](#page-53-1)

| Command-Line Format | admin-ssl[={OFF ON}] |
|---------------------|----------------------|
| Deprecated          | Yes                  |
| Type                | Boolean              |
| Default Value       | ON                   |

The [--admin-ssl](#page-53-1) option is like the [--ssl](#page-74-0) option, except that it applies to the administrative connection interface rather than the main connection interface. For information about these interfaces, see Section 7.1.12.1, "Connection Interfaces".

The [--admin-ssl](#page-53-1) option specifies that the server permits but does not require encrypted connections on the administrative interface. This option is enabled by default.

[--admin-ssl](#page-53-1) can be specified in negated form as [--skip-admin-ssl](#page-53-1) or a synonym ([-](#page-53-1) [admin-ssl=OFF](#page-53-1), [--disable-admin-ssl](#page-53-1)). In this case, the option specifies that the server does not permit encrypted connections, regardless of the settings of the admin\_tsl\_xxx and admin\_ssl\_xxx system variables.

The [--admin-ssl](#page-53-1) option has an effect only at server startup on whether the administrative interface supports encrypted connections. It is ignored and has no effect on the operation of ALTER INSTANCE RELOAD TLS at runtime. For example, you can use [--admin-ssl=OFF](#page-53-1) to start the administrative interface with encrypted connections disabled, then reconfigure TLS and execute ALTER INSTANCE RELOAD TLS FOR CHANNEL mysql\_admin to enable encrypted connections at runtime.

For general information about configuring connection-encryption support, see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections". That discussion is written for the main connection interface, but the parameter names are similar for the administrative connection interface. Consider setting at least the [admin\\_ssl\\_cert](#page-85-1) and [admin\\_ssl\\_key](#page-86-2) system variables on the server side and the --ssl-ca (or --ssl-capath) option on the client side. For additional information specifically about the administrative interface, see Administrative Interface Support for Encrypted Connections.

Because support for encrypted connections is enabled by default, it is normally unnecessary to specify [--admin-ssl](#page-53-1). As of MySQL 8.0.26, [--admin-ssl](#page-53-1) is deprecated and subject to removal in a future MySQL version. If it is desired to disable encrypted connections, that can be done without specifying [--admin-ssl](#page-53-1) in negated form. Set the [admin\\_tls\\_version](#page-87-1) system variable to the empty value to indicate that no TLS versions are supported. For example, these lines in the server my.cnf file disable encrypted connections:

```
[mysqld]
admin_tls_version=''
```

## <span id="page-54-1"></span>• [--allow-suspicious-udfs](#page-54-1)

| Command-Line Format | allow-suspicious-udfs[={OFF ON}] |
|---------------------|----------------------------------|
| Type                | Boolean                          |
| Default Value       | OFF                              |

This option controls whether loadable functions that have only an xxx symbol for the main function can be loaded. By default, the option is off and only loadable functions that have at least one auxiliary symbol can be loaded; this prevents attempts at loading functions from shared object files other than those containing legitimate functions. See [Loadable Function Security Precautions.](https://dev.mysql.com/doc/extending-mysql/8.0/en/adding-loadable-function.md#loadable-function-security)

## <span id="page-54-2"></span>• [--ansi](#page-54-2)

| Command-Line Format | ansi |
|---------------------|------|
|---------------------|------|

Use standard (ANSI) SQL syntax instead of MySQL syntax. For more precise control over the server SQL mode, use the [--sql-mode](#page-73-3) option instead. See Section 1.6, "MySQL Standards Compliance", and Section 7.1.11, "Server SQL Modes".

## • [--basedir=](#page-93-1)dir\_name, -b [dir\\_name](#page-93-1)

| Command-Line Format  | basedir=dir_name                           |
|----------------------|--------------------------------------------|
| System Variable      | basedir                                    |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Directory name                             |
| Default Value        | parent of mysqld installation<br>directory |

The path to the MySQL installation directory. This option sets the [basedir](#page-93-1) system variable.

The server executable determines its own full path name at startup and uses the parent of the directory in which it is located as the default [basedir](#page-93-1) value. This in turn enables the server to use that [basedir](#page-93-1) when searching for server-related information such as the share directory containing error messages.

## <span id="page-54-0"></span>• [--character-set-client-handshake](#page-54-0)

| Command-Line Format | character-set-client<br>handshake[={OFF ON}] |
|---------------------|----------------------------------------------|
| Deprecated          | Yes                                          |
| Type                | Boolean                                      |
| Default Value       | ON                                           |

Do not ignore character set information sent by the client. To ignore client information and use the default server character set, use [--skip-character-set-client-handshake](#page-54-0).

This option is deprecated in MySQL 8.0.35 and later MySQL 8.0 releases, where a warning is issued whenever it is used, and is to be removed in a future version of MySQL. Applications which depen on this option should begin migration away from it as soon as possible.

<span id="page-55-0"></span>• [--check-table-functions=](#page-55-0)value

| Command-Line Format | check-table-functions=value |
|---------------------|-----------------------------|
| Type                | Enumeration                 |
| Default Value       | ABORT                       |
| Valid Values        | WARN                        |
|                     | ABORT                       |

When performing an upgade of the server, we scan the data dictionary for functions used in table constraints and other expressions, including DEFAULT expressions, partitioning expressions, and virtual columns. It is possible that a change in the behavior of the function causes it to raise an error in the new version of the server, where no such error occurred before in which case the table cannot be opened. This option provides a choice in how to handle such problems, according to which of the two values shown here is used:

- WARN: Log a warning for each table that cannot be opened.
- ABORT: Also logs a warning; in addition, the upgrade is stopped. This is the default. For a sufficiently high value of [--log-error-verbosity](#page-144-1), it also logs a note with a streamlined table definition listing only those expressions that potentially contain SQL functions.

The default behaviour is to abort the upgrade, so that the user can fix the issue using the older version of the server, before upgrading to the newer one. Use WARN to continue the upgrade in interactive mode while reporting any issues.

The --check-table-functions option was introduced in MySQL 8.0.42.

<span id="page-55-1"></span>• [--chroot=](#page-55-1)dir\_name, -r dir\_name

| Command-Line Format | chroot=dir_name |
|---------------------|-----------------|
| Type                | Directory name  |

Put the mysqld server in a closed environment during startup by using the chroot() system call. This is a recommended security measure. Use of this option somewhat limits LOAD DATA and SELECT ... INTO OUTFILE.

<span id="page-55-2"></span>• [--console](#page-55-2)

| Platform Specific | Windows |
|-------------------|---------|
|-------------------|---------|

(Windows only.) Cause the default error log destination to be the console. This affects log sinks that base their own output destination on the default destination. See Section 7.4.2, "The Error Log". mysqld does not close the console window if this option is used.

[--console](#page-55-2) takes precedence over [--log-error](#page-63-1) if both are given.

<span id="page-56-0"></span>• [--core-file](#page-56-0)

| Command-Line Format | core-file |
|---------------------|-----------|
|---------------------|-----------|

When this option is used, write a core file if mysqld dies; no arguments are needed (or accepted). The name and location of the core file is system dependent. On Linux, a core file named core.pid is written to the current working directory of the process, which for mysqld is the data directory. pid represents the process ID of the server process. On macOS, a core file named core.pid is written to the /cores directory. On Solaris, use the coreadm command to specify where to write the core file and how to name it.

For some systems, to get a core file you must also specify the --core-file-size option to mysqld\_safe. See Section 6.3.2, "mysqld\_safe — MySQL Server Startup Script". On some systems, such as Solaris, you do not get a core file if you are also using the [--user](#page-80-0) option. There might be additional restrictions or limitations. For example, it might be necessary to execute ulimit -c unlimited before starting the server. Consult your system documentation.

The innodb\_buffer\_pool\_in\_core\_file variable can be used to reduce the size of core files on operating systems that support it. For more information, see Section 17.8.3.7, "Excluding Buffer Pool Pages from Core Files".

<span id="page-56-1"></span>• [--daemonize](#page-56-1), -D

| Command-Line Format | daemonize[={OFF ON}] |
|---------------------|----------------------|
| Type                | Boolean              |
| Default Value       | OFF                  |

This option causes the server to run as a traditional, forking daemon, permitting it to work with operating systems that use systemd for process control. For more information, see Section 2.5.9, "Managing MySQL Server with systemd".

[--daemonize](#page-56-1) is mutually exclusive with [--initialize](#page-60-0) and [--initialize-insecure](#page-61-0).

If the server is started using the --daemonize option and is not connected to a tty device, a default error logging option of --log-error="" is used in the absence of an explicit logging option, to direct error output to the default log file.

-D is a synonym for [--daemonize](#page-56-1).

• [--datadir=](#page-108-0)dir\_name, -h dir\_name

| Command-Line Format  | datadir=dir_name |
|----------------------|------------------|
| System Variable      | datadir          |
| Scope                | Global           |
| Dynamic              | No               |
| SET_VAR Hint Applies | No               |

|  | Type | Directory name |  |
|--|------|----------------|--|
|--|------|----------------|--|

The path to the MySQL server data directory. This option sets the [datadir](#page-108-0) system variable. See the description of that variable.

<span id="page-57-0"></span>• --debug[=[debug\\_options](#page-57-0)], -# [debug\_options]

| Command-Line Format     | debug[=debug_options]     |
|-------------------------|---------------------------|
| System Variable         | debug                     |
| Scope                   | Global, Session           |
| Dynamic                 | Yes                       |
| SET_VAR Hint Applies    | No                        |
| Type                    | String                    |
| Default Value (Unix)    | d:t:i:o,/tmp/mysqld.trace |
| Default Value (Windows) | d:t:i:O,\mysqld.trace     |

If MySQL is configured with the -DWITH\_DEBUG=1 CMake option, you can use this option to get a trace file of what mysqld is doing. A typical debug\_options string is d:t:o,file\_name. The default is d:t:i:o,/tmp/mysqld.trace on Unix and d:t:i:O,\mysqld.trace on Windows.

Using -DWITH\_DEBUG=1 to configure MySQL with debugging support enables you to use the [-](#page-57-0) [debug="d,parser\\_debug"](#page-57-0) option when you start the server. This causes the Bison parser that is used to process SQL statements to dump a parser trace to the server's standard error output. Typically, this output is written to the error log.

This option may be given multiple times. Values that begin with + or - are added to or subtracted from the previous value. For example, [--debug=T](#page-57-0) [--debug=+P](#page-57-0) sets the value to P:T.

For more information, see Section 7.9.4, "The DBUG Package".

<span id="page-57-1"></span>• [--debug-sync-timeout\[=](#page-57-1)N]

| Command-Line Format | debug-sync-timeout[=#] |
|---------------------|------------------------|
| Type                | Integer                |

Controls whether the Debug Sync facility for testing and debugging is enabled. Use of Debug Sync requires that MySQL be configured with the -DWITH\_DEBUG=ON CMake option (see Section 2.8.7, "MySQL Source-Configuration Options"); otherwise, this option is not available. The option value is a timeout in seconds. The default value is 0, which disables Debug Sync. To enable it, specify a value greater than 0; this value also becomes the default timeout for individual synchronization points. If the option is given without a value, the timeout is set to 300 seconds.

For a description of the Debug Sync facility and how to use synchronization points, see [MySQL](https://dev.mysql.com/doc/internals/en/test-synchronization.md) [Internals: Test Synchronization](https://dev.mysql.com/doc/internals/en/test-synchronization.md).

<span id="page-57-2"></span>• [--default-time-zone=](#page-57-2)timezone

| Command-Line Format | default-time-zone=name |
|---------------------|------------------------|
|---------------------|------------------------|

| Type | String |
|------|--------|
|      |        |

Set the default server time zone. This option sets the global time\_zone system variable. If this option is not given, the default time zone is the same as the system time zone (given by the value of the system\_time\_zone system variable.

The system\_time\_zone variable differs from time\_zone. Although they might have the same value, the latter variable is used to initialize the time zone for each client that connects. See Section 7.1.15, "MySQL Server Time Zone Support".

<span id="page-58-0"></span>• [--defaults-extra-file=](#page-58-0)file\_name

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-58-1"></span>• [--defaults-file=](#page-58-1)file\_name

Read only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with [--defaults-file](#page-58-1), mysqld reads mysqld-auto.cnf.

![](_page_58_Picture_10.jpeg)

#### **Note**

This must be the first option on the command line if it is used, except that if the server is started with the [--defaults-file](#page-58-1) and [--install](#page-61-1) (or [-](#page-61-2) [install-manual](#page-61-2)) options, [--install](#page-61-1) (or [--install-manual](#page-61-2)) must be first.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-58-2"></span>• [--defaults-group-suffix=](#page-58-2)str

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, mysqld normally reads the [mysqld] group. If this option is given as [--defaults](#page-58-2)[group-suffix=\\_other](#page-58-2), mysqld also reads the [mysqld\_other] group.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-58-3"></span>• [--early-plugin-load=](#page-58-3)plugin\_list

| Command-Line Format | early-plugin-load=plugin_list |
|---------------------|-------------------------------|
| Type                | String                        |
| Default Value       | empty string                  |

This option tells the server which plugins to load before loading mandatory built-in plugins and before storage engine initialization. Early loading is supported only for plugins compiled with PLUGIN\_OPT\_ALLOW\_EARLY. If multiple [--early-plugin-load](#page-58-3) options are given, only the last one applies.

The option value is a semicolon-separated list of plugin\_library and name=plugin\_library values. Each plugin\_library is the name of a library file that contains plugin code, and each name is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads only the named plugin from the library. The server looks for plugin library files in the directory named by the [plugin\\_dir](#page-178-1) system variable.

For example, if plugins named myplug1 and myplug2 are contained in the plugin library files myplug1.so and myplug2.so, use this option to perform an early plugin load:

```
mysqld --early-plugin-load="myplug1=myplug1.so;myplug2=myplug2.so"
```

Quotes surround the argument value because otherwise some command interpreters interpret semicolon (;) as a special character. (For example, Unix shells treat it as a command terminator.)

Each named plugin is loaded early for a single invocation of mysqld only. After a restart, the plugin is not loaded early unless [--early-plugin-load](#page-58-3) is used again.

If the server is started using [--initialize](#page-60-0) or [--initialize-insecure](#page-61-0), plugins specified by [-](#page-58-3) [early-plugin-load](#page-58-3) are not loaded.

If the server is run with [--help](#page-53-0), plugins specified by [--early-plugin-load](#page-58-3) are loaded but not initialized. This behavior ensures that plugin options are displayed in the help message.

InnoDB tablespace encryption relies on the MySQL Keyring for encryption key management, and the keyring plugin to be used must be loaded prior to storage engine initialization to facilitate InnoDB recovery for encrypted tables. For example, administrators who want the keyring\_file plugin loaded at startup should use [--early-plugin-load](#page-58-3) with the appropriate option value (such as keyring\_file.so on Unix and Unix-like systems or keyring\_file.dll on Windows).

For information about InnoDB tablespace encryption, see Section 17.13, "InnoDB Data-at-Rest Encryption". For general information about plugin loading, see Section 7.6.1, "Installing and Uninstalling Plugins".

![](_page_59_Picture_10.jpeg)

## **Note**

For MySQL Keyring, this option is used only when the keystore is managed with a keyring plugin. If keystore management uses a keyring component rather than a plugin, specify component loading using a manifest file; see Section 8.4.4.2, "Keyring Component Installation".

<span id="page-59-0"></span>• [--exit-info\[=](#page-59-0)flags], -T [flags]

| Command-Line Format | exit-info[=flags] |
|---------------------|-------------------|
| Type                | Integer           |

This is a bitmask of different flags that you can use for debugging the mysqld server. Do not use this option unless you know exactly what it does!

<span id="page-59-1"></span>• [--external-locking](#page-59-1)

| Command-Line Format | external-locking[={OFF ON}] |  |
|---------------------|-----------------------------|--|
| Type                | Boolean                     |  |
| Default Value       | OFF                         |  |

Enable external locking (system locking), which is disabled by default. If you use this option on a system on which lockd does not fully work (such as Linux), it is easy for mysqld to deadlock.

To disable external locking explicitly, use --skip-external-locking.

External locking affects only MyISAM table access. For more information, including conditions under which it can and cannot be used, see Section 10.11.5, "External Locking".

## <span id="page-60-1"></span>• [--flush](#page-60-1)

| Command-Line Format  | flush[={OFF ON}] |
|----------------------|------------------|
| System Variable      | flush            |
| Scope                | Global           |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Type                 | Boolean          |
| Default Value        | OFF              |

Flush (synchronize) all changes to disk after each SQL statement. Normally, MySQL does a write of all changes to disk only after each SQL statement and lets the operating system handle the synchronizing to disk. See Section B.3.3.3, "What to Do If MySQL Keeps Crashing".

![](_page_60_Picture_4.jpeg)

#### **Note**

If [--flush](#page-60-1) is specified, the value of [flush\\_time](#page-124-0) does not matter and changes to [flush\\_time](#page-124-0) have no effect on flush behavior.

## <span id="page-60-2"></span>• [--gdb](#page-60-2)

| Command-Line Format | gdb[={OFF ON}] |  |
|---------------------|----------------|--|
| Type                | Boolean        |  |
| Default Value       | OFF            |  |

Install an interrupt handler for SIGINT (needed to stop mysqld with ^C to set breakpoints) and disable stack tracing and core file handling. See Section 7.9.1.4, "Debugging mysqld under gdb".

On Windows, this option also suppresses the forking that is used to implement the RESTART statement: Forking enables one process to act as a monitor to the other, which acts as the server. However, forking makes determining the server process to attach to for debugging more difficult, so starting the server with [--gdb](#page-60-2) suppresses forking. For a server started with this option, RESTART simply exits and does not restart.

In non-debug settings, [--no-monitor](#page-66-0) may be used to suppress forking the monitor process.

## <span id="page-60-0"></span>• [--initialize](#page-60-0), -I

| Command-Line Format | initialize[={OFF ON}] |  |
|---------------------|-----------------------|--|
| Type                | Boolean               |  |
| Default Value       | OFF                   |  |

This option is used to initialize a MySQL installation by creating the data directory and populating the tables in the mysql system schema. For more information, see Section 2.9.1, "Initializing the Data Directory".

This option limits the effects of, or is not compatible with, a number of other startup options for the MySQL server. Some of the most common issues of this sort are noted here:

• We strongly recommend, when initializing the data directory with --initialize, that you specify no additional options other than [--datadir](#page-108-0), other options used for setting directory locations such as [--basedir](#page-93-1), and possibly [--user](#page-80-0), if required. Options for the running MySQL server can be specified when starting it once initialization has been completed and mysqld has shut down. This also applies when using [--initialize-insecure](#page-61-0) instead of --initialize.

- When the server is started with --initialize, some functionality is unavailable that limits the statements permitted in any file named by the [init\\_file](#page-134-0) system variable. For more information, see the description of that variable. In addition, the [disabled\\_storage\\_engines](#page-115-2) system variable has no effect.
- The --ndbcluster option is ignored when used together with --initialize.
- --initialize is mutually exclusive with [--bootstrap](https://dev.mysql.com/doc/refman/5.7/en/server-options.md#option_mysqld_bootstrap) and [--daemonize](#page-56-1).

The items in the preceding list also apply when initializing the server using the [--initialize](#page-61-0)[insecure](#page-61-0) option.

<span id="page-61-0"></span>• [--initialize-insecure](#page-61-0)

| Command-Line Format | initialize-insecure[={OFF ON}] |  |
|---------------------|--------------------------------|--|
| Type                | Boolean                        |  |
| Default Value       | OFF                            |  |

This option is used to initialize a MySQL installation by creating the data directory and populating the tables in the mysql system schema. This option implies [--initialize](#page-60-0), and the same restrictions and limitations apply; for more information, see the description of that option, and Section 2.9.1, "Initializing the Data Directory".

![](_page_61_Picture_9.jpeg)

#### **Warning**

This option creates a MySQL root user with an empty password, which is insecure. For this reason, do not use it in production without setting this password manually. See Post-Initialization root Password Assignment, for information about how to do this.

• --innodb-xxx

Set an option for the InnoDB storage engine. The InnoDB options are listed in Section 17.14, "InnoDB Startup Options and System Variables".

<span id="page-61-1"></span>• --install [[service\\_name](#page-61-1)]

| Command-Line Format | install [service_name] |
|---------------------|------------------------|
| Platform Specific   | Windows                |

(Windows only) Install the server as a Windows service that starts automatically during Windows startup. The default service name is MySQL if no service\_name value is given. For more information, see Section 2.3.4.8, "Starting MySQL as a Windows Service".

![](_page_61_Picture_17.jpeg)

#### **Note**

If the server is started with the [--defaults-file](#page-58-1) and [--install](#page-61-1) options, [--install](#page-61-1) must be first.

<span id="page-61-2"></span>• [--install-manual \[](#page-61-2)service\_name]

| Command-Line Format | install-manual [service_name] |  |  |
|---------------------|-------------------------------|--|--|
|---------------------|-------------------------------|--|--|

| Platform Specific | Windows |
|-------------------|---------|
|-------------------|---------|

(Windows only) Install the server as a Windows service that must be started manually. It does not start automatically during Windows startup. The default service name is MySQL if no service\_name value is given. For more information, see Section 2.3.4.8, "Starting MySQL as a Windows Service".

![](_page_62_Picture_3.jpeg)

#### **Note**

If the server is started with the --defaults-file and [--install-manual](#page-61-2) options, [--install-manual](#page-61-2) must be first.

<span id="page-62-2"></span>• [--language=](#page-62-2)lang\_name, -L lang\_name

| Command-Line Format  | language=name                             |  |
|----------------------|-------------------------------------------|--|
| Deprecated           | Yes; use lc-messages-dir instead          |  |
| System Variable      | language                                  |  |
| Scope                | Global                                    |  |
| Dynamic              | No                                        |  |
| SET_VAR Hint Applies | No                                        |  |
| Type                 | Directory name                            |  |
| Default Value        | /usr/local/mysql/share/mysql/<br>english/ |  |

The language to use for error messages. lang\_name can be given as the language name or as the full path name to the directory where the language files are installed. See Section 12.12, "Setting the Error Message Language".

[--lc-messages-dir](#page-63-0) and [--lc-messages](#page-62-1) should be used rather than [--language](#page-62-2), which is deprecated (and handled as a synonym for [--lc-messages-dir](#page-63-0)). You should expect the [-](#page-62-2) [language](#page-62-2) option to be removed in a future MySQL release.

<span id="page-62-0"></span>• [--large-pages](#page-62-0)

| Command-Line Format  | large-pages[={OFF ON}] |
|----------------------|------------------------|
| System Variable      | large_pages            |
| Scope                | Global                 |
| Dynamic              | No                     |
| SET_VAR Hint Applies | No                     |
| Platform Specific    | Linux                  |
| Type                 | Boolean                |
| Default Value        | OFF                    |

Some hardware/operating system architectures support memory pages greater than the default (usually 4KB). The actual implementation of this support depends on the underlying hardware and operating system. Applications that perform a lot of memory accesses may obtain performance improvements by using large pages due to reduced Translation Lookaside Buffer (TLB) misses.

MySQL supports the Linux implementation of large page support (which is called HugeTLB in Linux). See Section 10.12.3.3, "Enabling Large Page Support". For Solaris support of large pages, see the description of the [--super-large-pages](#page-75-1) option.

- [--large-pages](#page-62-0) is disabled by default.
- <span id="page-62-1"></span>• [--lc-messages=](#page-62-1)locale\_name

| Command-Line Format  | lc-messages=name |
|----------------------|------------------|
| System Variable      | lc_messages      |
| Scope                | Global, Session  |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Type                 | String           |
| Default Value        | en_US            |

The locale to use for error messages. The default is en\_US. The server converts the argument to a language name and combines it with the value of [--lc-messages-dir](#page-63-0) to produce the location for the error message file. See Section 12.12, "Setting the Error Message Language".

<span id="page-63-0"></span>• [--lc-messages-dir=](#page-63-0)dir\_name

| Command-Line Format  | lc-messages-dir=dir_name |
|----------------------|--------------------------|
| System Variable      | lc_messages_dir          |
| Scope                | Global                   |
| Dynamic              | No                       |
| SET_VAR Hint Applies | No                       |
| Type                 | Directory name           |

The directory where error messages are located. The server uses the value together with the value of [--lc-messages](#page-62-1) to produce the location for the error message file. See Section 12.12, "Setting the Error Message Language".

<span id="page-63-2"></span>• [--local-service](#page-63-2)

| Command-Line Format | local-service |
|---------------------|---------------|
|---------------------|---------------|

(Windows only) A --local-service option following the service name causes the server to run using the LocalService Windows account that has limited system privileges. If both - defaults-file and --local-service are given following the service name, they can be in any order. See Section 2.3.4.8, "Starting MySQL as a Windows Service".

<span id="page-63-1"></span>• [--log-error\[=](#page-63-1)file\_name]

| Command-Line Format  | log-error[=file_name] |
|----------------------|-----------------------|
| System Variable      | log_error             |
| Scope                | Global                |
| Dynamic              | No                    |
| SET_VAR Hint Applies | No                    |
| Type                 | File name             |

Set the default error log destination to the named file. This affects log sinks that base their own output destination on the default destination. See Section 7.4.2, "The Error Log".

If the option names no file, the default error log destination on Unix and Unix-like systems is a file named host\_name.err in the data directory. The default destination on Windows is the same,

unless the [--pid-file](#page-178-0) option is specified. In that case, the file name is the PID file base name with a suffix of .err in the data directory.

If the option names a file, the default destination is that file (with an .err suffix added if the name has no suffix), located under the data directory unless an absolute path name is given to specify a different location.

If error log output cannot be redirected to the error log file, an error occurs and startup fails.

On Windows, [--console](#page-55-2) takes precedence over [--log-error](#page-63-1) if both are given. In this case, the default error log destination is the console rather than a file.

<span id="page-64-1"></span>• [--log-isam\[=](#page-64-1)file\_name]

| Command-Line Format | log-isam[=file_name] |
|---------------------|----------------------|
| Type                | File name            |

Log all MyISAM changes to this file (used only when debugging MyISAM).

<span id="page-64-0"></span>• [--log-raw](#page-64-0)

| Command-Line Format  | log-raw[={OFF ON}] |
|----------------------|--------------------|
| System Variable      | log_raw            |
| Scope                | Global             |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Boolean            |
| Default Value        | OFF                |

Passwords in certain statements written to the general query log, slow query log, and binary log are rewritten by the server not to occur literally in plain text. Password rewriting can be suppressed for the general query log by starting the server with the [--log-raw](#page-64-0) option. This option may be useful for diagnostic purposes, to see the exact text of statements as received by the server, but for security reasons is not recommended for production use.

If a query rewrite plugin is installed, the [--log-raw](#page-64-0) option affects statement logging as follows:

- Without [--log-raw](#page-64-0), the server logs the statement returned by the query rewrite plugin. This may differ from the statement as received.
- With [--log-raw](#page-64-0), the server logs the original statement as received.

For more information, see Section 8.1.2.3, "Passwords and Logging".

<span id="page-64-2"></span>• [--log-short-format](#page-64-2)

| Command-Line Format | log-short-format[={OFF ON}] |
|---------------------|-----------------------------|
| Type                | Boolean                     |
| Default Value       | OFF                         |

Log less information to the slow query log, if it has been activated.

<span id="page-64-3"></span>• [--log-tc=](#page-64-3)file\_name

| Command-Line Format | log-tc=file_name |
|---------------------|------------------|
| Type                | File name        |

| Default Value | tc.log |
|---------------|--------|
|---------------|--------|

The name of the memory-mapped transaction coordinator log file (for XA transactions that affect multiple storage engines when the binary log is disabled). The default name is tc.log. The file is created under the data directory if not given as a full path name. This option is unused.

## <span id="page-65-0"></span>• [--log-tc-size=](#page-65-0)size

| Command-Line Format              | log-tc-size=#        |
|----------------------------------|----------------------|
| Type                             | Integer              |
| Default Value                    | 6 * page size        |
| Minimum Value                    | 6 * page size        |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

The size in bytes of the memory-mapped transaction coordinator log. The default and minimum values are 6 times the page size, and the value must be a multiple of the page size.

## <span id="page-65-1"></span>• [--memlock](#page-65-1)

| Command-Line Format | memlock[={OFF ON}] |
|---------------------|--------------------|
| Type                | Boolean            |
| Default Value       | OFF                |

Lock the mysqld process in memory. This option might help if you have a problem where the operating system is causing mysqld to swap to disk.

[--memlock](#page-65-1) works on systems that support the mlockall() system call; this includes Solaris, most Linux distributions that use a 2.4 or higher kernel, and perhaps other Unix systems. On Linux systems, you can tell whether or not mlockall() (and thus this option) is supported by checking to see whether or not it is defined in the system mman.h file, like this:

\$> **grep mlockall /usr/include/sys/mman.h**

If mlockall() is supported, you should see in the output of the previous command something like the following:

extern int mlockall (int \_\_flags) \_\_THROW;

![](_page_65_Picture_13.jpeg)

#### **Important**

Use of this option may require you to run the server as root, which, for reasons of security, is normally not a good idea. See Section 8.1.5, "How to Run MySQL as a Normal User".

On Linux and perhaps other systems, you can avoid the need to run the server as root by changing the limits.conf file. See the notes regarding the memlock limit in Section 10.12.3.3, "Enabling Large Page Support".

You must not use this option on a system that does not support the mlockall() system call; if you do so, mysqld is very likely to exit as soon as you try to start it.

## <span id="page-65-2"></span>• [--myisam-block-size=](#page-65-2)N

| Command-Line Format | myisam-block-size=# |
|---------------------|---------------------|
| Type                | Integer             |

| Default Value | 1024  |
|---------------|-------|
| Minimum Value | 1024  |
| Maximum Value | 16384 |

The block size to be used for MyISAM index pages.

<span id="page-66-1"></span>• [--no-defaults](#page-66-1)

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-66-1) can be used to prevent them from being read. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-66-2"></span>• [--no-dd-upgrade](#page-66-2)

| Command-Line Format | no-dd-upgrade[={OFF ON}] |
|---------------------|--------------------------|
| Deprecated          | Yes                      |
| Type                | Boolean                  |
| Default Value       | OFF                      |

![](_page_66_Picture_8.jpeg)

#### **Note**

This option is deprecated as of MySQL 8.0.16. It is superseded by the [-](#page-78-0) [upgrade](#page-78-0) option, which provides finer control over data dictionary and server upgrade behavior.

Prevent automatic upgrade of the data dictionary tables during the MySQL server startup process. This option is typically used when starting the MySQL server following an in-place upgrade of an existing installation to a newer MySQL version, which may include changes to data dictionary table definitions.

When [--no-dd-upgrade](#page-66-2) is specified, and the server finds that its expected version of the data dictionary differs from the version stored in the data dictionary itself, startup fails with an error stating that data dictionary upgrade is prohibited;

```
[ERROR] [MY-011091] [Server] Data dictionary upgrade prohibited by the
command line option '--no_dd_upgrade'.
[ERROR] [MY-010020] [Server] Data Dictionary initialization failed.
```

During a normal startup, the data dictionary version of the server is compared to the version stored in the data dictionary to determine whether data dictionary table definitions should be upgraded. If an upgrade is necessary and supported, the server creates data dictionary tables with updated definitions, copies persisted metadata to the new tables, atomically replaces the old tables with the new ones, and reinitializes the data dictionary. If an upgrade is not necessary, startup continues without updating data dictionary tables.

<span id="page-66-0"></span>• [--no-monitor](#page-66-0)

| Command-Line Format | no-monitor[={OFF ON}] |
|---------------------|-----------------------|
| Platform Specific   | Windows               |
| Type                | Boolean               |

| Default Value | OFF |  |
|---------------|-----|--|
|---------------|-----|--|

(Windows only). This option suppresses the forking that is used to implement the RESTART statement: Forking enables one process to act as a monitor to the other, which acts as the server. For a server started with this option, RESTART simply exits and does not restart.

[--no-monitor](#page-66-0) is not available prior to MySQL 8.0.12. The [--gdb](#page-60-2) option can be used as a workaround.

<span id="page-67-1"></span>• [--old-style-user-limits](#page-67-1)

| Command-Line Format | old-style-user-limits[={OFF ON}] |
|---------------------|----------------------------------|
| Deprecated          | Yes                              |
| Type                | Boolean                          |
| Default Value       | OFF                              |

Enable old-style user limits. (Before MySQL 5.0.3, account resource limits were counted separately for each host from which a user connected rather than per account row in the user table.) See Section 8.2.21, "Setting Account Resource Limits".

This option is deprecated, and, as of MySQL 8.0.30, using it on the command line or in an option file causes MySQL to raise a warning. Expect this option to be removed in a future release; you should check your applications now for use of --old-style-user-limits and remove any dependencies they might have on it, before this happens.

• --performance-schema-xxx

Configure a Performance Schema option. For details, see Section 29.14, "Performance Schema Command Options".

<span id="page-67-0"></span>• [--plugin-load=](#page-67-0)plugin\_list

| Command-Line Format | plugin-load=plugin_list |
|---------------------|-------------------------|
| Type                | String                  |

This option tells the server to load the named plugins at startup. If multiple [--plugin-load](#page-67-0) options are given, only the last one applies. Additional plugins to load may be specified using [--plugin](#page-68-0)[load-add](#page-68-0) options.

The option value is a semicolon-separated list of plugin\_library and name=plugin\_library values. Each plugin\_library is the name of a library file that contains plugin code, and each name is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads only the named plugin from the library. The server looks for plugin library files in the directory named by the [plugin\\_dir](#page-178-1) system variable.

For example, if plugins named myplug1 and myplug2 are contained in the plugin library files myplug1.so and myplug2.so, use this option to perform an early plugin load:

```
mysqld --plugin-load="myplug1=myplug1.so;myplug2=myplug2.so"
```

Quotes surround the argument value because otherwise some command interpreters interpret semicolon (;) as a special character. (For example, Unix shells treat it as a command terminator.)

Each named plugin is loaded for a single invocation of mysqld only. After a restart, the plugin is not loaded unless [--plugin-load](#page-67-0) is used again. This is in contrast to INSTALL PLUGIN, which adds an entry to the mysql.plugins table to cause the plugin to be loaded for every normal server startup.

During the normal startup sequence, the server determines which plugins to load by reading the mysql.plugins system table. If the server is started with the [--skip-grant-tables](#page-70-1) option, plugins registered in the mysql.plugins table are not loaded and are unavailable. [--plugin](#page-67-0)[load](#page-67-0) enables plugins to be loaded even when [--skip-grant-tables](#page-70-1) is given. [--plugin-load](#page-67-0) also enables plugins to be loaded at startup that cannot be loaded at runtime.

This option does not set a corresponding system variable. The output of SHOW PLUGINS provides information about loaded plugins. More detailed information can be found in the Information Schema PLUGINS table. See Section 7.6.2, "Obtaining Server Plugin Information".

For additional information about plugin loading, see Section 7.6.1, "Installing and Uninstalling Plugins".

<span id="page-68-0"></span>• [--plugin-load-add=](#page-68-0)plugin\_list

| Command-Line Format | plugin-load-add=plugin_list |
|---------------------|-----------------------------|
| Type                | String                      |

This option complements the [--plugin-load](#page-67-0) option. [--plugin-load-add](#page-68-0) adds a plugin or plugins to the set of plugins to be loaded at startup. The argument format is the same as for [-](#page-67-0) [plugin-load](#page-67-0). [--plugin-load-add](#page-68-0) can be used to avoid specifying a large set of plugins as a single long unwieldy [--plugin-load](#page-67-0) argument.

[--plugin-load-add](#page-68-0) can be given in the absence of [--plugin-load](#page-67-0), but any instance of [-](#page-68-0) [plugin-load-add](#page-68-0) that appears before [--plugin-load](#page-67-0) has no effect because [--plugin-load](#page-67-0) resets the set of plugins to load. In other words, these options:

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

This option does not set a corresponding system variable. The output of SHOW PLUGINS provides information about loaded plugins. More detailed information can be found in the Information Schema PLUGINS table. See Section 7.6.2, "Obtaining Server Plugin Information".

For additional information about plugin loading, see Section 7.6.1, "Installing and Uninstalling Plugins".

<span id="page-68-1"></span>• [--plugin-](#page-68-1)xxx

Specifies an option that pertains to a server plugin. For example, many storage engines can be built as plugins, and for such engines, options for them can be specified with a --plugin prefix. Thus,

the --innodb-file-per-table option for InnoDB can be specified as --plugin-innodbfile-per-table.

For boolean options that can be enabled or disabled, the --skip prefix and other alternative formats are supported as well (see Section 6.2.2.4, "Program Option Modifiers"). For example, --skipplugin-innodb-file-per-table disables innodb-file-per-table.

The rationale for the --plugin prefix is that it enables plugin options to be specified unambiguously if there is a name conflict with a built-in server option. For example, were a plugin writer to name a plugin "sql" and implement a "mode" option, the option name might be [--sql-mode](#page-73-3), which would conflict with the built-in option of the same name. In such cases, references to the conflicting name are resolved in favor of the built-in option. To avoid the ambiguity, users can specify the plugin option as --plugin-sql-mode. Use of the --plugin prefix for plugin options is recommended to avoid any question of ambiguity.

<span id="page-69-0"></span>• --port=[port\\_num](#page-69-0), -P port\_num

| Command-Line Format  | port=port_num |
|----------------------|---------------|
| System Variable      | port          |
| Scope                | Global        |
| Dynamic              | No            |
| SET_VAR Hint Applies | No            |
| Type                 | Integer       |
| Default Value        | 3306          |
| Minimum Value        | 0             |
| Maximum Value        | 65535         |

The port number to use when listening for TCP/IP connections. On Unix and Unix-like systems, the port number must be 1024 or higher unless the server is started by the root operating system user. Setting this option to 0 causes the default value to be used.

<span id="page-69-1"></span>• [--port-open-timeout=](#page-69-1)num

| Command-Line Format | port-open-timeout=# |
|---------------------|---------------------|
| Type                | Integer             |
| Default Value       | 0                   |

On some systems, when the server is stopped, the TCP/IP port might not become available immediately. If the server is restarted quickly afterward, its attempt to reopen the port can fail. This option indicates how many seconds the server should wait for the TCP/IP port to become free if it cannot be opened. The default is not to wait.

<span id="page-69-2"></span>• [--print-defaults](#page-69-2)

Print the program name and all options that it gets from option files. Password values are masked. This must be the first option on the command line if it is used, except that it may be used immediately after [--defaults-file](#page-58-1) or [--defaults-extra-file](#page-58-0).

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-69-3"></span>• --remove [[service\\_name](#page-69-3)]

| Command-Line Format | remove [service_name] |
|---------------------|-----------------------|
|                     |                       |

| Platform Specific | Windows |
|-------------------|---------|
|-------------------|---------|

(Windows only) Remove a MySQL Windows service. The default service name is MySQL if no service\_name value is given. For more information, see Section 2.3.4.8, "Starting MySQL as a Windows Service".

<span id="page-70-0"></span>• [--safe-user-create](#page-70-0)

| Command-Line Format | safe-user-create[={OFF ON}] |
|---------------------|-----------------------------|
| Deprecated          | Yes                         |
| Type                | Boolean                     |
| Default Value       | OFF                         |

This option is deprecated, and ignored as of MySQL 8.0.11. For related information, see Server Changes.

If this option is enabled, a user cannot create new MySQL users by using the GRANT statement unless the user has the INSERT privilege for the mysql.user system table or any column in the table. If you want a user to have the ability to create new users that have those privileges that the user has the right to grant, you should grant the user the following privilege:

```
GRANT INSERT(user) ON mysql.user TO 'user_name'@'host_name';
```

This ensures that the user cannot change any privilege columns directly, but has to use the GRANT statement to give privileges to other users.

<span id="page-70-1"></span>• [--skip-grant-tables](#page-70-1)

| Command-Line Format | skip-grant-tables[={OFF ON}] |
|---------------------|------------------------------|
| Type                | Boolean                      |

| Default Value | OFF |  |
|---------------|-----|--|
|---------------|-----|--|

This option affects the server startup sequence:

• [--skip-grant-tables](#page-70-1) causes the server not to read the grant tables in the mysql system schema, and thus to start without using the privilege system at all. This gives anyone with access to the server unrestricted access to all databases.

Because starting the server with [--skip-grant-tables](#page-70-1) disables authentication checks, the server also disables remote connections in that case by enabling skip\_networking.

To cause a server started with [--skip-grant-tables](#page-70-1) to load the grant tables at runtime, perform a privilege-flushing operation, which can be done in these ways:

- Issue a MySQL FLUSH PRIVILEGES statement after connecting to the server.
- Execute a mysqladmin flush-privileges or mysqladmin reload command from the command line.

Privilege flushing might also occur implicitly as a result of other actions performed after startup, thus causing the server to start using the grant tables. For example, the server flushes the privileges if it performs an upgrade during the startup sequence.

- [--skip-grant-tables](#page-70-1) disables failed-login tracking and temporary account locking because those capabilities depend on the grant tables. See Section 8.2.15, "Password Management".
- [--skip-grant-tables](#page-70-1) causes the server not to load certain other objects registered in the data dictionary or the mysql system schema:
  - Scheduled events installed using CREATE EVENT and registered in the events data dictionary table.
  - Plugins installed using INSTALL PLUGIN and registered in the mysql.plugin system table.

To cause plugins to be loaded even when using [--skip-grant-tables](#page-70-1), use the [--plugin](#page-67-0)[load](#page-67-0) or [--plugin-load-add](#page-68-0) option.

- Loadable functions installed using CREATE FUNCTION and registered in the mysql.func system table.
- [--skip-grant-tables](#page-70-1) does not suppress loading during startup of components.
- [--skip-grant-tables](#page-70-1) causes the [disabled\\_storage\\_engines](#page-115-2) system variable to have no effect.
- <span id="page-71-0"></span>• [--skip-host-cache](#page-71-0)

| Command-Line Format<br>skip-host-cache |
|----------------------------------------|
|----------------------------------------|

| Deprecated | Yes |
|------------|-----|
|------------|-----|

Disable use of the internal host cache for faster name-to-IP resolution. With the cache disabled, the server performs a DNS lookup every time a client connects.

Use of [--skip-host-cache](#page-71-0) is similar to setting the [host\\_cache\\_size](#page-131-1) system variable to 0, but [host\\_cache\\_size](#page-131-1) is more flexible because it can also be used to resize, enable, or disable the host cache at runtime, not just at server startup.

Beginning with MySQL 8.0.30, this option is deprecated; you should use SET GLOBAL host\_cache\_size = 0 instead.

Starting the server with [--skip-host-cache](#page-71-0) does not prevent runtime changes to the value of [host\\_cache\\_size](#page-131-1), but such changes have no effect and the cache is not re-enabled even if [host\\_cache\\_size](#page-131-1) is set larger than 0.

For more information about how the host cache works, see Section 7.1.12.3, "DNS Lookups and the Host Cache".

## • --skip-innodb

Disable the InnoDB storage engine. In this case, because the default storage engine is InnoDB, the server does not start unless you also use [--default-storage-engine](#page-112-0) and [--default](#page-113-0)[tmp-storage-engine](#page-113-0) to set the default to some other engine for both permanent and TEMPORARY tables.

The InnoDB storage engine cannot be disabled, and the --skip-innodb option is deprecated and has no effect. Its use results in a warning. Expect this option to be removed in a future MySQL release.

## <span id="page-72-0"></span>• [--skip-new](#page-72-0)

| Command-Line Format | skip-new |
|---------------------|----------|
| Deprecated          | Yes      |

This option disables (what used to be considered) new, possibly unsafe behaviors. It results in these settings: [delay\\_key\\_write=OFF](#page-113-2), [concurrent\\_insert=NEVER](#page-105-0), [automatic\\_sp\\_privileges=OFF](#page-91-1). It also causes OPTIMIZE TABLE to be mapped to ALTER TABLE for storage engines for which OPTIMIZE TABLE is not supported.

This option is deprecated as of MySQL 8.0.35, and is subject to removal in a future release.

## <span id="page-72-1"></span>• [--skip-show-database](#page-72-1)

| Command-Line Format  | skip-show-database |
|----------------------|--------------------|
| System Variable      | skip_show_database |
| Scope                | Global             |
| Dynamic              | No                 |
| SET_VAR Hint Applies | No                 |
| Type                 | Boolean            |
| Default Value        | OFF                |

This option sets the skip\_show\_database system variable that controls who is permitted to use the SHOW DATABASES statement. See [Section 7.1.8, "Server System Variables"](#page-81-1).

## <span id="page-73-0"></span>• [--skip-stack-trace](#page-73-0)

| Command-Line Format | skip-stack-trace |
|---------------------|------------------|
|---------------------|------------------|

Do not write stack traces. This option is useful when you are running mysqld under a debugger. On some systems, you also must use this option to get a core file. See Section 7.9, "Debugging MySQL".

## <span id="page-73-1"></span>• [--slow-start-timeout=](#page-73-1)timeout

| Command-Line Format | slow-start-timeout=# |
|---------------------|----------------------|
| Type                | Integer              |
| Default Value       | 15000                |

This option controls the Windows service control manager's service start timeout. The value is the maximum number of milliseconds that the service control manager waits before trying to kill the windows service during startup. The default value is 15000 (15 seconds). If the MySQL service takes too long to start, you may need to increase this value. A value of 0 means there is no timeout.

## <span id="page-73-2"></span>• [--socket=](#page-73-2)path

| Command-Line Format     | socket={file_name pipe_name} |
|-------------------------|------------------------------|
| System Variable         | socket                       |
| Scope                   | Global                       |
| Dynamic                 | No                           |
| SET_VAR Hint Applies    | No                           |
| Type                    | String                       |
| Default Value (Windows) | MySQL                        |
| Default Value (Other)   | /tmp/mysql.sock              |

On Unix, this option specifies the Unix socket file to use when listening for local connections. The default value is /tmp/mysql.sock. If this option is given, the server creates the file in the data directory unless an absolute path name is given to specify a different directory. On Windows, the option specifies the pipe name to use when listening for local connections that use a named pipe. The default value is MySQL (not case-sensitive).

## • [--sql-mode=](#page-73-3)value[,value[,value...]]

<span id="page-73-3"></span>

|     | Command-Line Format  | sql-mode=name                                                                                                                     |
|-----|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
|     | System Variable      | sql_mode                                                                                                                          |
|     | Scope                | Global, Session                                                                                                                   |
|     | Dynamic              | Yes                                                                                                                               |
|     | SET_VAR Hint Applies | Yes                                                                                                                               |
|     | Type                 | Set                                                                                                                               |
|     | Default Value        | ONLY_FULL_GROUP_BY<br>STRICT_TRANS_TABLES<br>NO_ZERO_IN_DATE NO_ZERO_DATE<br>ERROR_FOR_DIVISION_BY_ZERO<br>NO_ENGINE_SUBSTITUTION |
|     | Valid Values         | ALLOW_INVALID_DATES                                                                                                               |
| 844 |                      | ANSI_QUOTES                                                                                                                       |

ERROR\_FOR\_DIVISION\_BY\_ZERO HIGH\_NOT\_PRECEDENCE IGNORE\_SPACE NO\_AUTO\_VALUE\_ON\_ZERO NO\_BACKSLASH\_ESCAPES NO\_DIR\_IN\_CREATE NO\_ENGINE\_SUBSTITUTION NO\_UNSIGNED\_SUBTRACTION NO\_ZERO\_DATE NO\_ZERO\_IN\_DATE ONLY\_FULL\_GROUP\_BY PAD\_CHAR\_TO\_FULL\_LENGTH PIPES\_AS\_CONCAT REAL\_AS\_FLOAT STRICT\_ALL\_TABLES STRICT\_TRANS\_TABLES TIME\_TRUNCATE\_FRACTIONAL

Set the SQL mode. See Section 7.1.11, "Server SQL Modes".

![](_page_74_Picture_3.jpeg)

## **Note**

MySQL installation programs may configure the SQL mode during the installation process.

If the SQL mode differs from the default or from what you expect, check for a setting in an option file that the server reads at startup.

<span id="page-74-0"></span>• [--ssl](#page-74-0), [--skip-ssl](#page-74-0)

| Command-Line Format | ssl[={OFF ON}] |
|---------------------|----------------|
| Deprecated          | Yes            |
| Disabled by         | skip-ssl       |
| Type                | Boolean        |

| Default Value | ON |
|---------------|----|
|---------------|----|

The [--ssl](#page-74-0) option specifies that the server permits but does not require encrypted connections on the main connection interface. This option is enabled by default.

A similar option, [--admin-ssl](#page-53-1), is like the [--ssl](#page-74-0), except that it applies to the administrative connection interface rather than the main connection interface. For information about these interfaces, see Section 7.1.12.1, "Connection Interfaces".

[--ssl](#page-74-0) can be specified in negated form as [--skip-ssl](#page-74-0) or a synonym ([--ssl=OFF](#page-74-0), [--disable](#page-74-0)[ssl](#page-74-0)). In this case, the option specifies that the server does not permit encrypted connections, regardless of the settings of the tls\_xxx and ssl\_xxx system variables.

The [--ssl](#page-74-0) option has an effect only at server startup on whether the server supports encrypted connections. It is ignored and has no effect on the operation of ALTER INSTANCE RELOAD TLS at runtime. For example, you can use [--ssl=OFF](#page-74-0) to start the server with encrypted connections disabled, then reconfigure TLS and execute ALTER INSTANCE RELOAD TLS to enable encrypted connections at runtime.

For more information about configuring whether the server permits clients to connect using SSL and indicating where to find SSL keys and certificates, see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections", which also describes server capabilities for certificate and key file autogeneration and autodiscovery. Consider setting at least the ssl\_cert and ssl\_key system variables on the server side and the --ssl-ca (or --ssl-capath) option on the client side.

Because support for encrypted connections is enabled by default, it is normally unnecessary to specify [--ssl](#page-74-0). As of MySQL 8.0.26, [--ssl](#page-74-0) is deprecated and subject to removal in a future MySQL version. If it is desired to disable encrypted connections, that can be done without specifying [-](#page-74-0) [ssl](#page-74-0) in negated form. Set the tls\_version system variable to the empty value to indicate that no TLS versions are supported. For example, these lines in the server my.cnf file disable encrypted connections:

```
[mysqld]
tls_version=''
```

## <span id="page-75-0"></span>• [--standalone](#page-75-0)

| Command-Line Format | standalone |
|---------------------|------------|
| Platform Specific   | Windows    |

Available on Windows only; instructs the MySQL server not to run as a service.

## <span id="page-75-1"></span>• [--super-large-pages](#page-75-1)

| Command-Line Format | super-large-pages[={OFF ON}] |
|---------------------|------------------------------|
| Platform Specific   | Solaris                      |
| Type                | Boolean                      |
| Default Value       | OFF                          |

Standard use of large pages in MySQL attempts to use the largest size supported, up to 4MB. Under Solaris, a "super large pages" feature enables uses of pages up to 256MB. This feature is available for recent SPARC platforms. It can be enabled or disabled by using the [--super-large-pages](#page-75-1) or [--skip-super-large-pages](#page-75-1) option.

## <span id="page-75-2"></span>• [--symbolic-links](#page-75-2), [--skip-symbolic-links](#page-75-2)

| Command-Line Format | symbolic-links[={OFF ON}] |
|---------------------|---------------------------|
| Deprecated          | Yes                       |

| Type          | Boolean |
|---------------|---------|
| Default Value | OFF     |

Enable or disable symbolic link support. On Unix, enabling symbolic links means that you can link a MyISAM index file or data file to another directory with the INDEX DIRECTORY or DATA DIRECTORY option of the CREATE TABLE statement. If you delete or rename the table, the files that its symbolic links point to also are deleted or renamed. See Section 10.12.2.2, "Using Symbolic Links for MyISAM Tables on Unix".

![](_page_76_Picture_3.jpeg)

#### **Note**

Symbolic link support, along with the [--symbolic-links](#page-75-2) option that controls it, is deprecated; you should expect it to be removed in a future version of MySQL. In addition, the option is disabled by default. The related [have\\_symlink](#page-130-4) system variable also is deprecated; expect it to be removed in a future version of MySQL.

This option has no meaning on Windows.

<span id="page-76-0"></span>• [--sysdate-is-now](#page-76-0)

| Command-Line Format | sysdate-is-now[={OFF ON}] |
|---------------------|---------------------------|
| Type                | Boolean                   |
| Default Value       | OFF                       |

SYSDATE() by default returns the time at which it executes, not the time at which the statement in which it occurs begins executing. This differs from the behavior of NOW(). This option causes SYSDATE() to be a synonym for NOW(). For information about the implications for binary logging and replication, see the description for SYSDATE() in Section 14.7, "Date and Time Functions" and for SET TIMESTAMP in [Section 7.1.8, "Server System Variables"](#page-81-1).

<span id="page-76-1"></span>• [--tc-heuristic-recover={COMMIT|ROLLBACK}](#page-76-1)

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

<span id="page-76-2"></span>• [--transaction-isolation=](#page-76-2)level

| Command-Line Format<br>transaction-isolation=name<br>847 |
|----------------------------------------------------------|
|----------------------------------------------------------|

| System Variable      | transaction_isolation |
|----------------------|-----------------------|
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Enumeration           |
| Default Value        | REPEATABLE-READ       |
| Valid Values         | READ-UNCOMMITTED      |
|                      | READ-COMMITTED        |
|                      | REPEATABLE-READ       |
|                      | SERIALIZABLE          |

Sets the default transaction isolation level. The level value can be READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ, or SERIALIZABLE. See Section 15.3.7, "SET TRANSACTION Statement".

The default transaction isolation level can also be set at runtime using the SET TRANSACTION statement or by setting the transaction\_isolation system variable.

## <span id="page-77-1"></span>• [--transaction-read-only](#page-77-1)

| Command-Line Format  | transaction-read-only[={OFF ON}] |
|----------------------|----------------------------------|
| System Variable      | transaction_read_only            |
| Scope                | Global, Session                  |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Boolean                          |
| Default Value        | OFF                              |

Sets the default transaction access mode. By default, read-only mode is disabled, so the mode is read/write.

To set the default transaction access mode at runtime, use the SET TRANSACTION statement or set the transaction\_read\_only system variable. See Section 15.3.7, "SET TRANSACTION Statement".

## <span id="page-77-0"></span>• [--tmpdir=](#page-77-0)dir\_name, -t dir\_name

| Command-Line Format  | tmpdir=dir_name |
|----------------------|-----------------|
| System Variable      | tmpdir          |
| Scope                | Global          |
| Dynamic              | No              |
| SET_VAR Hint Applies | No              |
| Type                 | Directory name  |

The path of the directory to use for creating temporary files. It might be useful if your default /tmp directory resides on a partition that is too small to hold temporary tables. This option accepts several paths that are used in round-robin fashion. Paths should be separated by colon characters (:) on Unix and semicolon characters (;) on Windows.

[--tmpdir](#page-77-0) can be a non-permanent location, such as a directory on a memory-based file system or a directory that is cleared when the server host restarts. If the MySQL server is acting as a replica, and you are using a non-permanent location for [--tmpdir](#page-77-0), consider setting a different temporary directory for the replica using the replica\_load\_tmpdir or slave\_load\_tmpdir system variable. For a replica, the temporary files used to replicate LOAD DATA statements are stored in this directory, so with a permanent location they can survive machine restarts, although replication can now continue after a restart if the temporary files have been removed.

For more information about the storage location of temporary files, see Section B.3.3.5, "Where MySQL Stores Temporary Files".

## <span id="page-78-0"></span>• [--upgrade=](#page-78-0)value

| Command-Line Format | upgrade=value |
|---------------------|---------------|
| Type                | Enumeration   |
| Default Value       | AUTO          |
| Valid Values        | AUTO          |
|                     | NONE          |
|                     | MINIMAL       |

FORCE

This option controls whether and how the server performs an automatic upgrade at startup. Automatic upgrade involves two steps:

• Step 1: Data dictionary upgrade.

This step upgrades:

- The data dictionary tables in the mysql schema. If the actual data dictionary version is lower than the current expected version, the server upgrades the data dictionary. If it cannot, or is prevented from doing so, the server cannot run.
- The Performance Schema and INFORMATION\_SCHEMA.
- Step 2: Server upgrade.

This step comprises all other upgrade tasks. If the existing installation data has a lower MySQL version than the server expects, it must be upgraded:

- The system tables in the mysql schema (the remaining non-data dictionary tables).
- The sys schema.
- User schemas.

For details about upgrade steps 1 and 2, see Section 3.4, "What the MySQL Upgrade Process Upgrades".

These [--upgrade](#page-78-0) option values are permitted:

• AUTO

The server performs an automatic upgrade of anything it finds to be out of date (steps 1 and 2). This is the default action if [--upgrade](#page-78-0) is not specified explicitly.

• NONE

The server performs no automatic upgrade steps during the startup process (skips steps 1 and 2). Because this option value prevents a data dictionary upgrade, the server exits with an error if the data dictionary is found to be out of date:

```
[ERROR] [MY-013381] [Server] Server shutting down because upgrade is
required, yet prohibited by the command line option '--upgrade=NONE'.
[ERROR] [MY-010334] [Server] Failed to initialize DD Storage Engine
[ERROR] [MY-010020] [Server] Data Dictionary initialization failed.
```

• MINIMAL

The server upgrades the data dictionary, the Performance Schema, and the INFORMATION\_SCHEMA, if necessary (step 1). Note that following an upgrade with this option, Group Replication cannot be started, because system tables on which the replication internals depend are not updated, and reduced functionality might also be apparent in other areas.

• FORCE

The server upgrades the data dictionary, the Performance Schema, and the INFORMATION\_SCHEMA, if necessary (step 1). In addition, the server forces an upgrade of everything else (step 2). Expect server startup to take longer with this option because the server checks all objects in all schemas.

FORCE is useful to force step 2 actions to be performed if the server thinks they are not necessary. For example, you may believe that a system table is missing or has become damaged and want to force a repair.

The following table summarizes the actions taken by the server for each option value.

| Option Value | Server Performs Step 1? | Server Performs Step 2? |
|--------------|-------------------------|-------------------------|
| AUTO         | If necessary            | If necessary            |
| NONE         | No                      | No                      |
| MINIMAL      | If necessary            | No                      |
| FORCE        | If necessary            | Yes                     |

<span id="page-80-0"></span>• --user={[user\\_name](#page-80-0)|user\_id}, -u {user\_name|user\_id}

| Command-Line Format | user=name |
|---------------------|-----------|
| Type                | String    |

Run the mysqld server as the user having the name user\_name or the numeric user ID user\_id. ("User" in this context refers to a system login account, not a MySQL user listed in the grant tables.)

This option is mandatory when starting mysqld as root. The server changes its user ID during its startup sequence, causing it to run as that particular user rather than as root. See Section 8.1.1, "Security Guidelines".

To avoid a possible security hole where a user adds a [--user=root](#page-80-0) option to a my.cnf file (thus causing the server to run as root), mysqld uses only the first [--user](#page-80-0) option specified and produces a warning if there are multiple [--user](#page-80-0) options. Options in /etc/my.cnf and \$MYSQL\_HOME/my.cnf are processed before command-line options, so it is recommended that you put a [--user](#page-80-0) option in /etc/my.cnf and specify a value other than root. The option in /etc/ my.cnf is found before any other [--user](#page-80-0) options, which ensures that the server runs as a user other than root, and that a warning results if any other [--user](#page-80-0) option is found.

<span id="page-80-1"></span>• [--validate-config](#page-80-1)

| Command-Line Format | validate-config[={OFF ON}] |
|---------------------|----------------------------|
| Type                | Boolean                    |
| Default Value       | OFF                        |

Validate the server startup configuration. If no errors are found, the server terminates with an exit code of 0. If an error is found, the server displays a diagnostic message and terminates with an exit code of 1. Warning and information messages may also be displayed, depending on the [log\\_error\\_verbosity](#page-144-1) value, but do not produce immediate validation termination or an exit code of 1. For more information, see Section 7.1.3, "Server Configuration Validation".

<span id="page-80-2"></span>• [--validate-user-plugins\[={OFF|ON}\]](#page-80-2)

| Command-Line Format | validate-user-plugins[={OFF ON}] |
|---------------------|----------------------------------|
| Type                | Boolean                          |

Default Value ON

If this option is enabled (the default), the server checks each user account and produces a warning if conditions are found that would make the account unusable:

- The account requires an authentication plugin that is not loaded.
- The account requires the sha256\_password or caching\_sha2\_password authentication plugin but the server was started with neither SSL nor RSA enabled as required by the plugin.

Enabling [--validate-user-plugins](#page-80-2) slows down server initialization and FLUSH PRIVILEGES. If you do not require the additional checking, you can disable this option at startup to avoid the performance decrement.

<span id="page-81-0"></span>• [--verbose](#page-81-0), [-v](#page-81-0)

Use this option with the [--help](#page-53-0) option for detailed help.

• [--version](#page-81-2), -V

Display version information and exit.

# <span id="page-81-2"></span><span id="page-81-1"></span>**7.1.8 Server System Variables**

The MySQL server maintains many system variables that affect its operation. Most system variables can be set at server startup using options on the command line or in an option file. Most of them can be changed dynamically at runtime using the SET statement, which enables you to modify operation of the server without having to stop and restart it. Some variables are read-only, and their values are determined by the system environment, by how MySQL is installed on the system, or possibly by the options used to compile MySQL. Most system variables have a default value, but there are exceptions, including read-only variables. You can also use system variable values in expressions.

Setting a global system variable runtime value normally requires the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege). Setting a session system runtime variable value normally requires no special privileges and can be done by any user, although there are exceptions. For more information, see Section 7.1.9.1, "System Variable Privileges"

There are several ways to see the names and values of system variables:

• To see the values that a server uses based on its compiled-in defaults and any option files that it reads, use this command:

```
mysqld --verbose --help
```

• To see the values that a server uses based only on its compiled-in defaults, ignoring the settings in any option files, use this command:

```
mysqld --no-defaults --verbose --help
```

• To see the current values used by a running server, use the SHOW VARIABLES statement or the Performance Schema system variable tables. See Section 29.12.14, "Performance Schema System Variable Tables".

This section provides a description of each system variable. For a system variable summary table, see [Section 7.1.5, "Server System Variable Reference".](#page-10-0) For more information about manipulation of system variables, see Section 7.1.9, "Using System Variables".

For additional system variable information, see these sections:

- Section 7.1.9, "Using System Variables", discusses the syntax for setting and displaying system variable values.
- Section 7.1.9.2, "Dynamic System Variables", lists the variables that can be set at runtime.

- Information on tuning system variables can be found in Section 7.1.1, "Configuring the Server".
- Section 17.14, "InnoDB Startup Options and System Variables", lists InnoDB system variables.
- NDB Cluster System Variables, lists system variables which are specific to NDB Cluster.
- For information on server system variables specific to replication, see Section 19.1.6, "Replication and Binary Logging Options and Variables".

![](_page_82_Picture_5.jpeg)

## **Note**

Some of the following variable descriptions refer to "enabling" or "disabling" a variable. These variables can be enabled with the SET statement by setting them to ON or 1, or disabled by setting them to OFF or 0. Boolean variables can be set at startup to the values ON, TRUE, OFF, and FALSE (not case-sensitive), as well as 1 and 0. See Section 6.2.2.4, "Program Option Modifiers".

Some system variables control the size of buffers or caches. For a given buffer, the server might need to allocate internal data structures. These structures typically are allocated from the total memory allocated to the buffer, and the amount of space required might be platform dependent. This means that when you assign a value to a system variable that controls a buffer size, the amount of space actually available might differ from the value assigned. In some cases, the amount might be less than the value assigned. It is also possible that the server adjusts a value upward. For example, if you assign a value of 0 to a variable for which the minimal value is 1024, the server sets the value to 1024.

<span id="page-82-1"></span>Values for buffer sizes, lengths, and stack sizes are given in bytes unless otherwise specified.

![](_page_82_Picture_10.jpeg)

#### **Note**

Some system variable descriptions include a block size, in which case a value that is not an integer multiple of the stated block size is rounded down to the next lower multiple of the block size before being stored by the server, that is to FLOOR(value) \* block\_size.

Example: Suppose that the block size for a given variable is given as 4096, and you set the value of the variable to 100000 (we assume that the variable's maximum value is greater than this number). Since 100000 / 4096 = 24.4140625, the server automatically lowers the value to 98304 (24 \* 4096) before storing it.

In some cases, the stated maximum for a variable is the maximum allowed by the MySQL parser, but is not an exact multiple of the block size. In such cases, the effective maximum is the next lower multiple of the block size.

Example: A system variable's maxmum value is shown as 4294967295 (232-1), and its block size is 1024. 4294967295 / 1024 = 4194303.9990234375, so if you set this variable to its stated maximum, the value actually stored is 4194303 \* 1024 = 4294966272.

Some system variables take file name values. Unless otherwise specified, the default file location is the data directory if the value is a relative path name. To specify the location explicitly, use an absolute path name. Suppose that the data directory is /var/mysql/data. If a file-valued variable is given as a relative path name, it is located under /var/mysql/data. If the value is an absolute path name, its location is as given by the path name.

<span id="page-82-0"></span>• [activate\\_all\\_roles\\_on\\_login](#page-82-0)

| Command-Line Format | activate-all-roles-on-login[={OFF <br>ON}] |
|---------------------|--------------------------------------------|
| System Variable     | activate_all_roles_on_login                |
| Scope               | Global                                     |

| Dynamic              | Yes     |
|----------------------|---------|
| SET_VAR Hint Applies | No      |
| Type                 | Boolean |
| Default Value        | OFF     |

Whether to enable automatic activation of all granted roles when users log in to the server:

- If [activate\\_all\\_roles\\_on\\_login](#page-82-0) is enabled, the server activates all roles granted to each account at login time. This takes precedence over default roles specified with SET DEFAULT ROLE.
- If [activate\\_all\\_roles\\_on\\_login](#page-82-0) is disabled, the server activates the default roles specified with SET DEFAULT ROLE, if any, at login time.

Granted roles include those granted explicitly to the user and those named in the [mandatory\\_roles](#page-150-0) system variable value.

[activate\\_all\\_roles\\_on\\_login](#page-82-0) applies only at login time, and at the beginning of execution for stored programs and views that execute in definer context. To change the active roles within a session, use SET ROLE. To change the active roles for a stored program, the program body should execute SET ROLE.

<span id="page-83-0"></span>• [admin\\_address](#page-83-0)

| Command-Line Format  | admin-address=addr |
|----------------------|--------------------|
| System Variable      | admin_address      |
| Scope                | Global             |
| Dynamic              | No                 |
| SET_VAR Hint Applies | No                 |
| Type                 | String             |

The IP address on which to listen for TCP/IP connections on the administrative network interface (see Section 7.1.12.1, "Connection Interfaces"). There is no default [admin\\_address](#page-83-0) value. If this variable is not specified at startup, the server maintains no administrative interface. The server also has a [bind\\_address](#page-94-0) system variable for configuring regular (nonadministrative) client TCP/IP connections. See Section 7.1.12.1, "Connection Interfaces".

If [admin\\_address](#page-83-0) is specified, its value must satisfy these requirements:

- The value must be a single IPv4 address, IPv6 address, or host name.
- The value cannot specify a wildcard address format (\*, 0.0.0.0, or ::).
- As of MySQL 8.0.22, the value may include a network namespace specifier.

An IP address can be specified as an IPv4 or IPv6 address. If the value is a host name, the server resolves the name to an IP address and binds to that address. If a host name resolves to multiple IP addresses, the server uses the first IPv4 address if there are any, or the first IPv6 address otherwise.

The server treats different types of addresses as follows:

• If the address is an IPv4-mapped address, the server accepts TCP/IP connections for that address, in either IPv4 or IPv6 format. For example, if the server is bound to ::ffff:127.0.0.1, clients can connect using --host=127.0.0.1 or --host=::ffff:127.0.0.1.

• If the address is a "regular" IPv4 or IPv6 address (such as 127.0.0.1 or ::1), the server accepts TCP/IP connections only for that IPv4 or IPv6 address.

These rules apply to specifying a network namespace for an address:

- A network namespace can be specified for an IP address or a host name.
- A network namespace cannot be specified for a wildcard IP address.
- For a given address, the network namespace is optional. If given, it must be specified as a /ns suffix immediately following the address.
- An address with no /ns suffix uses the host system global namespace. The global namespace is therefore the default.
- An address with a /ns suffix uses the namespace named ns.
- The host system must support network namespaces and each named namespace must previously have been set up. Naming a nonexistent namespace produces an error.

For additional information about network namespaces, see Section 7.1.14, "Network Namespace Support".

If binding to the address fails, the server produces an error and does not start.

The [admin\\_address](#page-83-0) system variable is similar to the [bind\\_address](#page-94-0) system variable that binds the server to an address for ordinary client connections, but with these differences:

- [bind\\_address](#page-94-0) permits multiple addresses. [admin\\_address](#page-83-0) permits a single address.
- [bind\\_address](#page-94-0) permits wildcard addresses. [admin\\_address](#page-83-0) does not.
- <span id="page-84-0"></span>• [admin\\_port](#page-84-0)

| Command-Line Format  | admin-port=port_num |
|----------------------|---------------------|
| System Variable      | admin_port          |
| Scope                | Global              |
| Dynamic              | No                  |
| SET_VAR Hint Applies | No                  |
| Type                 | Integer             |
| Default Value        | 33062               |
| Minimum Value        | 0                   |
| Maximum Value        | 65535               |

The TCP/IP port number to use for connections on the administrative network interface (see Section 7.1.12.1, "Connection Interfaces"). Setting this variable to 0 causes the default value to be used.

Setting [admin\\_port](#page-84-0) has no effect if [admin\\_address](#page-83-0) is not specified because in that case the server maintains no administrative network interface.

<span id="page-84-1"></span>• [admin\\_ssl\\_ca](#page-84-1)

| Command-Line Format | admin-ssl-ca=file_name |
|---------------------|------------------------|
| System Variable     | admin_ssl_ca           |
| Scope               | Global                 |

| Dynamic              | Yes       |
|----------------------|-----------|
| SET_VAR Hint Applies | No        |
| Type                 | File name |
| Default Value        | NULL      |

The [admin\\_ssl\\_ca](#page-84-1) system variable is like ssl\_ca, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-85-0"></span>• [admin\\_ssl\\_capath](#page-85-0)

| Command-Line Format  | admin-ssl-capath=dir_name |
|----------------------|---------------------------|
| System Variable      | admin_ssl_capath          |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Directory name            |
| Default Value        | NULL                      |

The [admin\\_ssl\\_capath](#page-85-0) system variable is like ssl\_capath, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-85-1"></span>• [admin\\_ssl\\_cert](#page-85-1)

| Command-Line Format  | admin-ssl-cert=file_name |
|----------------------|--------------------------|
| System Variable      | admin_ssl_cert           |
| Scope                | Global                   |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | No                       |
| Type                 | File name                |
| Default Value        | NULL                     |

The [admin\\_ssl\\_cert](#page-85-1) system variable is like ssl\_cert, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-85-2"></span>• [admin\\_ssl\\_cipher](#page-85-2)

| Command-Line Format  | admin-ssl-cipher=name |
|----------------------|-----------------------|
| System Variable      | admin_ssl_cipher      |
| Scope                | Global                |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | String                |

| Default Value | NULL |
|---------------|------|
|---------------|------|

The [admin\\_ssl\\_cipher](#page-85-2) system variable is like ssl\_cipher, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-86-0"></span>• [admin\\_ssl\\_crl](#page-86-0)

| Command-Line Format  | admin-ssl-crl=file_name |
|----------------------|-------------------------|
| System Variable      | admin_ssl_crl           |
| Scope                | Global                  |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | File name               |
| Default Value        | NULL                    |

The [admin\\_ssl\\_crl](#page-86-0) system variable is like ssl\_crl, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-86-1"></span>• [admin\\_ssl\\_crlpath](#page-86-1)

| Command-Line Format  | admin-ssl-crlpath=dir_name |
|----------------------|----------------------------|
| System Variable      | admin_ssl_crlpath          |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Directory name             |
| Default Value        | NULL                       |

The [admin\\_ssl\\_crlpath](#page-86-1) system variable is like ssl\_crlpath, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-86-2"></span>• [admin\\_ssl\\_key](#page-86-2)

| Command-Line Format  | admin-ssl-key=file_name |
|----------------------|-------------------------|
| System Variable      | admin_ssl_key           |
| Scope                | Global                  |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | File name               |
| Default Value        | NULL                    |

The [admin\\_ssl\\_key](#page-86-2) system variable is like ssl\_key, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-87-0"></span>• [admin\\_tls\\_ciphersuites](#page-87-0)

| Command-Line Format  | admin-tls<br>ciphersuites=ciphersuite_list |
|----------------------|--------------------------------------------|
| System Variable      | admin_tls_ciphersuites                     |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | String                                     |
| Default Value        | NULL                                       |

The [admin\\_tls\\_ciphersuites](#page-87-0) system variable is like tls\_ciphersuites, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

<span id="page-87-1"></span>• [admin\\_tls\\_version](#page-87-1)

| Command-Line Format  | admin-tls-version=protocol_list |
|----------------------|---------------------------------|
| System Variable      | admin_tls_version               |
| Scope                | Global                          |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | String                          |
| Default Value        | TLSv1.2,TLSv1.3                 |

The [admin\\_tls\\_version](#page-87-1) system variable is like tls\_version, except that it applies to the administrative connection interface rather than the main connection interface. For information about configuring encryption support for the administrative interface, see Administrative Interface Support for Encrypted Connections.

![](_page_87_Picture_7.jpeg)

## **Important**

- Support for the TLSv1 and TLSv1.1 connection protocols is removed from MySQL Server as of MySQL 8.0.28. The protocols were deprecated from MySQL 8.0.26. See Removal of Support for the TLSv1 and TLSv1.1 Protocols for more information.
- Support for the TLSv1.3 protocol is available in MySQL Server as of MySQL 8.0.16, provided that MySQL Server was compiled using OpenSSL 1.1.1 or higher. The server checks the version of OpenSSL at startup, and if it is lower than 1.1.1, TLSv1.3 is removed from the default value for the system variable. In that case, the defaults are "TLSv1,TLSv1.1,TLSv1.2" up to and including MySQL 8.0.27, and "TLSv1.2" from MySQL 8.0.28.
- <span id="page-87-2"></span>• [authentication\\_policy](#page-87-2)

| Command-Line Format  | authentication-policy=value |
|----------------------|-----------------------------|
| System Variable      | authentication_policy       |
| Scope                | Global                      |
| Dynamic              | Yes                         |
| SET_VAR Hint Applies | No                          |

| Type          | String |
|---------------|--------|
| Default Value | *,,    |

This variable is used to administer multifactor authentication (MFA) capabilities. It applies to the authentication factor-related clauses of CREATE USER and ALTER USER statements used to manage MySQL account definitions, where "factor" corresponds to an authentication method or plugin associated with an account:

- [authentication\\_policy](#page-87-2) controls the number of authentication factors that accounts may have. That is, it controls which factors are required or permitted.
- [authentication\\_policy](#page-87-2) also controls, for each factor, which plugins (or methods) are permitted.
- [authentication\\_policy](#page-87-2), in conjunction with [default\\_authentication\\_plugin](#page-109-1), determines the default authentication plugin for authentication specifications that do not name a plugin explicitly.

Because [authentication\\_policy](#page-87-2) applies only when accounts are created or altered, changes to its value have no effect on existing user accounts.

![](_page_88_Picture_7.jpeg)

### **Note**

Although the [authentication\\_policy](#page-87-2) system variable places certain constraints on the authentication-related clauses of CREATE USER and ALTER USER statements, a user who has the AUTHENTICATION\_POLICY\_ADMIN privilege is not subject to the constraints. (A warning does occur for statements that otherwise would not be permitted.)

The value of [authentication\\_policy](#page-87-2) is a list of 1, 2, or 3 comma-separated elements. Each element present can be an authentication plugin name, an asterisk (\*), empty, or missing. (Exception: Element 1 cannot be empty or missing.) In all cases, an element may be surrounded by whitespace characters and the entire list is enclosed in single quotes.

The type of value specified for element N in the list has implications for whether factor N must be present in account definitions, and which authentication plugins can be used:

• If element N is an authentication plugin name, an authentication method for factor N is required and must use the named plugin.

In addition, the plugin becomes the default plugin for factor N authentication methods that do not name a plugin explicitly. For details, see The Default Authentication Plugin.

Authentication plugins that use internal credentials storage can be specified for the first element only, and cannot repeat. For example, the following settings are not permitted:

- authentication\_policy = 'caching\_sha2\_password, sha256\_password'
- authentication\_policy = 'caching\_sha2\_password, authentication\_fido, sha256\_password'
- If element N is an asterisk (\*), an authentication method for factor N is required. It may use any authentication plugin that is valid for element N (as described later).
- If element N is empty, an authentication method for factor N is optional. If given, it may use any authentication plugin that is valid for element N (as described later).
- If element N is missing from the list (that is, there are fewer than N−1 commas in the value), an authentication method for factor N is forbidden. For example, a value of '\*' permits only a single factor and thus enforces single-factor authentication (1FA) for new accounts created with CREATE

USER or changes to existing accounts made with ALTER USER. In this case, such statements cannot specify authentication for factors 2 or 3.

When an [authentication\\_policy](#page-87-2) element names an authentication plugin, the permitted plugin names for the element are subject to these conditions:

- Element 1 must name a plugin that does not require a registration step. For example, authentication\_fido cannot be named.
- Elements 2 and 3 must name a plugin that does not use internal credentials storage.

For information about which authentication plugins use internal credentials storage, see Section 8.2.15, "Password Management".

When [authentication\\_policy](#page-87-2) element N is \*, the permitted plugin names for factor N in account definitions are subject to these conditions:

- For factor 1, account definitions can use any plugin. Default authentication plugin rules apply for authentication specifications that do not name a plugin. See The Default Authentication Plugin.
- For factors 2 and 3, account definitions cannot name a plugin that uses internal credentials storage. For example, with '\*,\*', '\*,\*,\*', '\*,', '\*,,' [authentication\\_policy](#page-87-2) settings, plugins that use internal credentials storage are only permitted for the first factor and cannot repeat.

When [authentication\\_policy](#page-87-2) element N is empty, the permitted plugin names for factor N in account definitions are subject to these conditions:

- For factor 1, this does not apply because element 1 cannot be empty.
- For factors 2 and 3, account definitions cannot name a plugin that uses internal credentials storage.

Empty elements must occur at the end of the list, following a nonempty element. In other words, the first element cannot be empty, and either no element is empty or the last element is empty or the last two elements are empty. For example, a value of ',,' is not permitted because it would signify that all factors are optional. That cannot be; accounts must have at least one authentication factor.

The default value of [authentication\\_policy](#page-87-2) is '\*,,'. This means that factor 1 is required in account definitions and can use any authentication plugin, and that factors 2 and 3 are optional and each can use any authentication plugin that does not use internal credentials storage.

The following table shows some [authentication\\_policy](#page-87-2) values and the policy that each establishes for creating or altering accounts.

**Table 7.4 Example authentication\_policy Values**

| authentication_policy Value | Effective Policy                                                         |
|-----------------------------|--------------------------------------------------------------------------|
| '*'                         | Permit only creating or altering accounts with one<br>factor.            |
| '*,*'                       | Permit only creating or altering accounts with two<br>factors.           |
| '*,*,*'                     | Permit only creating or altering accounts with<br>three factors.         |
| '*,'                        | Permit creating or altering accounts with one or<br>two factors.         |
| '*,,'                       | Permit creating or altering accounts with one,<br>two, or three factors. |

| authentication_policy Value                                                           | Effective Policy                                                                                                                                                         |
|---------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| '*,*,'                                                                                | Permit creating or altering accounts with two or<br>three factors.                                                                                                       |
| '*,auth_plugin'                                                                       | Permit creating or altering accounts with two<br>factors, where the first factor can be any<br>authentication method, and the second factor<br>must be the named plugin. |
| 'auth_plugin,*,'                                                                      | Permit creating or altering accounts with two or<br>three factors, where the first factor must be the<br>named plugin.                                                   |
| 'auth_plugin,'                                                                        | Permit creating or altering accounts with one or<br>two factors, where the first factor must be the<br>named plugin.                                                     |
| 'auth_plugin,auth_plugin,auth_plugin'Permits creating or altering accounts with three | factors, where the factors must use the named<br>plugins.                                                                                                                |

## <span id="page-90-0"></span>• [authentication\\_windows\\_log\\_level](#page-90-0)

| Command-Line Format  | authentication-windows-log-level=# |
|----------------------|------------------------------------|
| System Variable      | authentication_windows_log_level   |
| Scope                | Global                             |
| Dynamic              | No                                 |
| SET_VAR Hint Applies | No                                 |
| Type                 | Integer                            |
| Default Value        | 2                                  |
| Minimum Value        | 0                                  |
| Maximum Value        | 4                                  |

This variable is available only if the authentication\_windows Windows authentication plugin is enabled and debugging code is enabled. See Section 8.4.1.6, "Windows Pluggable Authentication".

This variable sets the logging level for the Windows authentication plugin. The following table shows the permitted values.

| Value | Description                                |
|-------|--------------------------------------------|
| 0     | No logging                                 |
| 1     | Log only error messages                    |
| 2     | Log level 1 messages and warning messages  |
| 3     | Log level 2 messages and information notes |
| 4     | Log level 3 messages and debug messages    |

## <span id="page-90-1"></span>• [authentication\\_windows\\_use\\_principal\\_name](#page-90-1)

| Command-Line Format | authentication-windows-use<br>principal-name[={OFF ON}] |  |
|---------------------|---------------------------------------------------------|--|
| System Variable     | authentication_windows_use_principal_name               |  |
| Scope               | Global                                                  |  |
| Dynamic             | No                                                      |  |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | Boolean |
| Default Value        | ON      |

This variable is available only if the authentication\_windows Windows authentication plugin is enabled. See Section 8.4.1.6, "Windows Pluggable Authentication".

A client that authenticates using the InitSecurityContext() function should provide a string identifying the service to which it connects (targetName). MySQL uses the principal name (UPN) of the account under which the server is running. The UPN has the form user\_id@computer\_name and need not be registered anywhere to be used. This UPN is sent by the server at the beginning of authentication handshake.

This variable controls whether the server sends the UPN in the initial challenge. By default, the variable is enabled. For security reasons, it can be disabled to avoid sending the server's account name to a client as cleartext. If the variable is disabled, the server always sends a 0x00 byte in the first challenge, the client does not specify targetName, and as a result, NTLM authentication is used.

If the server fails to obtain its UPN (which happens primarily in environments that do not support Kerberos authentication), the UPN is not sent by the server and NTLM authentication is used.

## <span id="page-91-0"></span>• [autocommit](#page-91-0)

| Command-Line Format  | autocommit[={OFF ON}] |
|----------------------|-----------------------|
| System Variable      | autocommit            |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Boolean               |
| Default Value        | ON                    |

The autocommit mode. If set to 1, all changes to a table take effect immediately. If set to 0, you must use COMMIT to accept a transaction or ROLLBACK to cancel it. If [autocommit](#page-91-0) is 0 and you change it to 1, MySQL performs an automatic COMMIT of any open transaction. Another way to begin a transaction is to use a START TRANSACTION or BEGIN statement. See Section 15.3.1, "START TRANSACTION, COMMIT, and ROLLBACK Statements".

By default, client connections begin with [autocommit](#page-91-0) set to 1. To cause clients to begin with a default of 0, set the global [autocommit](#page-91-0) value by starting the server with the [--autocommit=0](#page-91-0) option. To set the variable using an option file, include these lines:

[mysqld] autocommit=0

## <span id="page-91-1"></span>• [automatic\\_sp\\_privileges](#page-91-1)

| Command-Line Format  | automatic-sp-privileges[={OFF ON}] |
|----------------------|------------------------------------|
| System Variable      | automatic_sp_privileges            |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Boolean                            |

| Default Value<br>ON |
|---------------------|
|---------------------|

When this variable has a value of 1 (the default), the server automatically grants the EXECUTE and ALTER ROUTINE privileges to the creator of a stored routine, if the user cannot already execute and alter or drop the routine. (The ALTER ROUTINE privilege is required to drop the routine.) The server also automatically drops those privileges from the creator when the routine is dropped. If [automatic\\_sp\\_privileges](#page-91-1) is 0, the server does not automatically add or drop these privileges.

The creator of a routine is the account used to execute the CREATE statement for it. This might not be the same as the account named as the DEFINER in the routine definition.

If you start mysqld with [--skip-new](#page-72-0), [automatic\\_sp\\_privileges](#page-91-1) is set to OFF.

See also Section 27.2.2, "Stored Routines and MySQL Privileges".

<span id="page-92-0"></span>• [auto\\_generate\\_certs](#page-92-0)

| Command-Line Format  | auto-generate-certs[={OFF ON}] |
|----------------------|--------------------------------|
| System Variable      | auto_generate_certs            |
| Scope                | Global                         |
| Dynamic              | No                             |
| SET_VAR Hint Applies | No                             |
| Type                 | Boolean                        |
| Default Value        | ON                             |

This variable controls whether the server autogenerates SSL key and certificate files in the data directory, if they do not already exist.

At startup, the server automatically generates server-side and client-side SSL certificate and key files in the data directory if the [auto\\_generate\\_certs](#page-92-0) system variable is enabled, no SSL options other than [--ssl](#page-74-0) are specified, and the server-side SSL files are missing from the data directory. These files enable secure client connections using SSL; see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".

For more information about SSL file autogeneration, including file names and characteristics, see Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"

The [sha256\\_password\\_auto\\_generate\\_rsa\\_keys](#page-196-0) and [caching\\_sha2\\_password\\_auto\\_generate\\_rsa\\_keys](#page-98-0) system variables are related but control autogeneration of RSA key-pair files needed for secure password exchange using RSA over unencrypted connections.

<span id="page-92-1"></span>• [avoid\\_temporal\\_upgrade](#page-92-1)

| Command-Line Format  | avoid-temporal-upgrade[={OFF ON}] |
|----------------------|-----------------------------------|
| Deprecated           | Yes                               |
| System Variable      | avoid_temporal_upgrade            |
| Scope                | Global                            |
| Dynamic              | Yes                               |
| SET_VAR Hint Applies | No                                |
| Type                 | Boolean                           |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

This variable controls whether ALTER TABLE implicitly upgrades temporal columns found to be in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision). Upgrading such columns requires a table rebuild, which prevents any use of fast alterations that might otherwise apply to the operation to be performed.

This variable is disabled by default. Enabling it causes ALTER TABLE not to rebuild temporal columns and thereby be able to take advantage of possible fast alterations.

This variable is deprecated; expect it to be removed in a future MySQL release.

## <span id="page-93-0"></span>• [back\\_log](#page-93-0)

| Command-Line Format  | back-log=#                                                     |
|----------------------|----------------------------------------------------------------|
| System Variable      | back_log                                                       |
| Scope                | Global                                                         |
| Dynamic              | No                                                             |
| SET_VAR Hint Applies | No                                                             |
| Type                 | Integer                                                        |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value        | 1                                                              |
| Maximum Value        | 65535                                                          |

The number of outstanding connection requests MySQL can have. This comes into play when the main MySQL thread gets very many connection requests in a very short time. It then takes some time (although very little) for the main thread to check the connection and start a new thread. The [back\\_log](#page-93-0) value indicates how many requests can be stacked during this short time before MySQL momentarily stops answering new requests. You need to increase this only if you expect a large number of connections in a short period of time.

In other words, this value is the size of the listen queue for incoming TCP/IP connections. Your operating system has its own limit on the size of this queue. The manual page for the Unix listen() system call should have more details. Check your OS documentation for the maximum value for this variable. [back\\_log](#page-93-0) cannot be set higher than your operating system limit.

The default value is the value of [max\\_connections](#page-152-1), which enables the permitted backlog to adjust to the maximum permitted number of connections.

## <span id="page-93-1"></span>• [basedir](#page-93-1)

| Command-Line Format  | basedir=dir_name                           |
|----------------------|--------------------------------------------|
| System Variable      | basedir                                    |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Directory name                             |
| Default Value        | parent of mysqld installation<br>directory |

The path to the MySQL installation base directory.

<span id="page-93-2"></span>• [big\\_tables](#page-93-2)

| Command-Line Format  | big-tables[={OFF ON}] |
|----------------------|-----------------------|
| System Variable      | big_tables            |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Boolean               |
| Default Value        | OFF                   |

If enabled, the server stores all temporary tables on disk rather than in memory. This prevents most The table tbl\_name is full errors for SELECT operations that require a large temporary table, but also slows down queries for which in-memory tables would suffice.

The default value for new connections is OFF (use in-memory temporary tables). Normally, it should never be necessary to enable this variable. When in-memory internal temporary tables are managed by the TempTable storage engine (the default), and the maximum amount of memory that can be occupied by the TempTable storage engine is exceeded, the TempTable storage engine starts storing data to temporary files on disk. When in-memory temporary tables are managed by the MEMORY storage engine, in-memory tables are automatically converted to disk-based tables as required. For more information, see Section 10.4.4, "Internal Temporary Table Use in MySQL".

## <span id="page-94-0"></span>• [bind\\_address](#page-94-0)

| Command-Line Format  | bind-address=addr |
|----------------------|-------------------|
| System Variable      | bind_address      |
| Scope                | Global            |
| Dynamic              | No                |
| SET_VAR Hint Applies | No                |
| Type                 | String            |
| Default Value        | *                 |

The MySQL server listens on one or more network sockets for TCP/IP connections. Each socket is bound to one address, but it is possible for an address to map onto multiple network interfaces. To specify how the server should listen for TCP/IP connections, set the [bind\\_address](#page-94-0) system variable at server startup. The server also has an [admin\\_address](#page-83-0) system variable that enables administrative connections on a dedicated interface. See Section 7.1.12.1, "Connection Interfaces".

If [bind\\_address](#page-94-0) is specified, its value must satisfy these requirements:

- Prior to MySQL 8.0.13, [bind\\_address](#page-94-0) accepts a single address value, which may specify a single non-wildcard IP address or host name, or one of the wildcard address formats that permit listening on multiple network interfaces (\*, 0.0.0.0, or ::).
- As of MySQL 8.0.13, [bind\\_address](#page-94-0) accepts either a single value as just described, or a list of comma-separated values. When the variable names a list of multiple values, each value must specify a single non-wildcard IP address (either IPv4 or IPv6) or a host name. Wildcard address formats (\*, 0.0.0.0, or ::) are not allowed in a list of values.
- As of MySQL 8.0.22, addresses may include a network namespace specifier.

IP addresses can be specified as IPv4 or IPv6 addresses. For any value that is a host name, the server resolves the name to an IP address and binds to that address. If a host name resolves to multiple IP addresses, the server uses the first IPv4 address if there are any, or the first IPv6 address otherwise.

The server treats different types of addresses as follows:

- If the address is \*, the server accepts TCP/IP connections on all server host IPv4 interfaces, and, if the server host supports IPv6, on all IPv6 interfaces. Use this address to permit both IPv4 and IPv6 connections on all server interfaces. This value is the default. If the variable specifies a list of multiple values, this value is not permitted.
- If the address is 0.0.0.0, the server accepts TCP/IP connections on all server host IPv4 interfaces. If the variable specifies a list of multiple values, this value is not permitted.
- If the address is ::, the server accepts TCP/IP connections on all server host IPv4 and IPv6 interfaces. If the variable specifies a list of multiple values, this value is not permitted.
- If the address is an IPv4-mapped address, the server accepts TCP/IP connections for that address, in either IPv4 or IPv6 format. For example, if the server is bound to ::ffff:127.0.0.1, clients can connect using --host=127.0.0.1 or --host=::ffff:127.0.0.1.
- If the address is a "regular" IPv4 or IPv6 address (such as 127.0.0.1 or ::1), the server accepts TCP/IP connections only for that IPv4 or IPv6 address.

These rules apply to specifying a network namespace for an address:

- A network namespace can be specified for an IP address or a host name.
- A network namespace cannot be specified for a wildcard IP address.
- For a given address, the network namespace is optional. If given, it must be specified as a /ns suffix immediately following the address.
- An address with no /ns suffix uses the host system global namespace. The global namespace is therefore the default.
- An address with a /ns suffix uses the namespace named ns.
- The host system must support network namespaces and each named namespace must previously have been set up. Naming a nonexistent namespace produces an error.
- If the variable value specifies multiple addresses, it can include addresses in the global namespace, in named namespaces, or a mix.

For additional information about network namespaces, see Section 7.1.14, "Network Namespace Support".

If binding to any address fails, the server produces an error and does not start.

## Examples:

• bind\_address=\*

The server listens on all IPv4 or IPv6 addresses, as specified by the \* wildcard.

• bind\_address=198.51.100.20

The server listens only on the 198.51.100.20 IPv4 address.

• bind\_address=198.51.100.20,2001:db8:0:f101::1

The server listens on the 198.51.100.20 IPv4 address and the 2001:db8:0:f101::1 IPv6 address.

• bind\_address=198.51.100.20,\*

This produces an error because wildcard addresses are not permitted when [bind\\_address](#page-94-0) names a list of multiple values.

• bind\_address=198.51.100.20/red,2001:db8:0:f101::1/blue,192.0.2.50

The server listens on the 198.51.100.20 IPv4 address in the red namespace, the 2001:db8:0:f101::1 IPv6 address in the blue namespace, and the 192.0.2.50 IPv4 address in the global namespace.

When [bind\\_address](#page-94-0) names a single value (wildcard or non-wildcard), the server listens on a single socket, which for a wildcard address may be bound to multiple network interfaces. When [bind\\_address](#page-94-0) names a list of multiple values, the server listens on one socket per value, with each socket bound to a single network interface. The number of sockets is linear with the number of values specified. Depending on operating system connection-acceptance efficiency, long value lists might incur a performance penalty for accepting TCP/IP connections.

 Because file descriptors are allocated for listening sockets and network namespace files, it may be necessary to increase the [open\\_files\\_limit](#page-169-1) system variable.

If you intend to bind the server to a specific address, be sure that the mysql.user system table contains an account with administrative privileges that you can use to connect to that address. Otherwise, you cannot shut down the server. For example, if you bind the server to \*, you can connect to it using all existing accounts. But if you bind the server to ::1, it accepts connections only on that address. In that case, first make sure that the 'root'@'::1' account is present in the mysql.user table so you can still connect to the server to shut it down.

<span id="page-96-0"></span>• [block\\_encryption\\_mode](#page-96-0)

| Command-Line Format  | block-encryption-mode=# |
|----------------------|-------------------------|
| System Variable      | block_encryption_mode   |
| Scope                | Global, Session         |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | String                  |
| Default Value        | aes-128-ecb             |

This variable controls the block encryption mode for block-based algorithms such as AES. It affects encryption for AES\_ENCRYPT() and AES\_DECRYPT().

[block\\_encryption\\_mode](#page-96-0) takes a value in aes-keylen-mode format, where keylen is the key length in bits and mode is the encryption mode. The value is not case-sensitive. Permitted keylen values are 128, 192, and 256. Permitted mode values are ECB, CBC, CFB1, CFB8, CFB128, and OFB.

For example, this statement causes the AES encryption functions to use a key length of 256 bits and the CBC mode:

```
SET block_encryption_mode = 'aes-256-cbc';
```

An error occurs for attempts to set [block\\_encryption\\_mode](#page-96-0) to a value containing an unsupported key length or a mode that the SSL library does not support.

<span id="page-96-1"></span>• [build\\_id](#page-96-1)

| System Variable | build_id |
|-----------------|----------|
|-----------------|----------|

| Scope                | Global |
|----------------------|--------|
| Dynamic              | No     |
| SET_VAR Hint Applies | No     |
| Platform Specific    | Linux  |

This is a 160-bit SHA1 signature which is generated by the linker when compiling the server on Linux systems with -DWITH\_BUILD\_ID=ON (enabled by default), and converted to a hexadecimal string. This read-only value serves as a unique build ID, and is written into the server log at startup.

build\_id is not supported on platforms other than Linux.

<span id="page-97-0"></span>• [bulk\\_insert\\_buffer\\_size](#page-97-0)

| Command-Line Format              | bulk-insert-buffer-size=# |
|----------------------------------|---------------------------|
| System Variable                  | bulk_insert_buffer_size   |
| Scope                            | Global, Session           |
| Dynamic                          | Yes                       |
| SET_VAR Hint Applies             | Yes                       |
| Type                             | Integer                   |
| Default Value                    | 8388608                   |
| Minimum Value                    | 0                         |
| Maximum Value (64-bit platforms) | 18446744073709551615      |
| Maximum Value (32-bit platforms) | 4294967295                |
| Unit                             | bytes/thread              |

MyISAM uses a special tree-like cache to make bulk inserts faster for INSERT ... SELECT, INSERT ... VALUES (...), (...), ..., and LOAD DATA when adding data to nonempty tables. This variable limits the size of the cache tree in bytes per thread. Setting it to 0 disables this optimization. The default value is 8MB.

As of MySQL 8.0.14, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-97-1"></span>• [caching\\_sha2\\_password\\_digest\\_rounds](#page-97-1)

| Command-Line Format  | caching-sha2-password-digest<br>rounds=# |
|----------------------|------------------------------------------|
| System Variable      | caching_sha2_password_digest_rounds      |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | Integer                                  |
| Default Value        | 5000                                     |
| Minimum Value        | 5000                                     |

| Maximum Value | 4095000 |  |
|---------------|---------|--|
|---------------|---------|--|

The number of hash rounds used by the caching\_sha2\_password authentication plugin for password storage.

Increasing the number of hashing rounds above the default value incurs a performance penalty that correlates with the amount of increase:

- Creating an account that uses the caching\_sha2\_password plugin has no impact on the client session within which the account is created, but the server must perform the hashing rounds to complete the operation.
- For client connections that use the account, the server must perform the hashing rounds and save the result in the cache. The result is longer login time for the first client connection, but not for subsequent connections. This behavior occurs after each server restart.
- <span id="page-98-0"></span>• [caching\\_sha2\\_password\\_auto\\_generate\\_rsa\\_keys](#page-98-0)

| Command-Line Format  | caching-sha2-password-auto<br>generate-rsa-keys[={OFF ON}] |  |
|----------------------|------------------------------------------------------------|--|
| System Variable      | caching_sha2_password_auto_generate_rsa_keys               |  |
| Scope                | Global                                                     |  |
| Dynamic              | No                                                         |  |
| SET_VAR Hint Applies | No                                                         |  |
| Type                 | Boolean                                                    |  |
| Default Value        | ON                                                         |  |

The server uses this variable to determine whether to autogenerate RSA private/public key-pair files in the data directory if they do not already exist.

At startup, the server automatically generates RSA private/public key-pair files in the data directory if all of these conditions are true: The [sha256\\_password\\_auto\\_generate\\_rsa\\_keys](#page-196-0) or [caching\\_sha2\\_password\\_auto\\_generate\\_rsa\\_keys](#page-98-0) system variable is enabled; no RSA options are specified; the RSA files are missing from the data directory. These key-pair files enable secure password exchange using RSA over unencrypted connections for accounts authenticated by the sha256\_password or caching\_sha2\_password plugin; see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

For more information about RSA file autogeneration, including file names and characteristics, see Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"

The [auto\\_generate\\_certs](#page-92-0) system variable is related but controls autogeneration of SSL certificate and key files needed for secure connections using SSL.

<span id="page-98-1"></span>• [caching\\_sha2\\_password\\_private\\_key\\_path](#page-98-1)

| Command-Line Format  | caching-sha2-password-private-key<br>path=file_name |
|----------------------|-----------------------------------------------------|
| System Variable      | caching_sha2_password_private_key_path              |
| Scope                | Global                                              |
| Dynamic              | No                                                  |
| SET_VAR Hint Applies | No                                                  |
| Type                 | File name                                           |

This variable specifies the path name of the RSA private key file for the caching\_sha2\_password authentication plugin. If the file is named as a relative path, it is interpreted relative to the server data directory. The file must be in PEM format.

![](_page_99_Picture_3.jpeg)

#### **Important**

Because this file stores a private key, its access mode should be restricted so that only the MySQL server can read it.

For information about caching\_sha2\_password, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-99-0"></span>• [caching\\_sha2\\_password\\_public\\_key\\_path](#page-99-0)

| Command-Line Format  | caching-sha2-password-public-key<br>path=file_name |
|----------------------|----------------------------------------------------|
| System Variable      | caching_sha2_password_public_key_path              |
| Scope                | Global                                             |
| Dynamic              | No                                                 |
| SET_VAR Hint Applies | No                                                 |
| Type                 | File name                                          |
| Default Value        | public_key.pem                                     |

This variable specifies the path name of the RSA public key file for the caching\_sha2\_password authentication plugin. If the file is named as a relative path, it is interpreted relative to the server data directory. The file must be in PEM format.

For information about caching\_sha2\_password, including information about how clients request the RSA public key, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-99-1"></span>• [character\\_set\\_client](#page-99-1)

| System Variable      | character_set_client |
|----------------------|----------------------|
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | String               |
| Default Value        | utf8mb4              |

The character set for statements that arrive from the client. The session value of this variable is set using the character set requested by the client when the client connects to the server. (Many clients support a --default-character-set option to enable this character set to be specified explicitly. See also Section 12.4, "Connection Character Sets and Collations".) The global value of the variable is used to set the session value in cases when the client-requested value is unknown or not available, or the server is configured to ignore client requests:

- The client requests a character set not known to the server. For example, a Japanese-enabled client requests sjis when connecting to a server not configured with sjis support.
- The client is from a version of MySQL older than MySQL 4.1, and thus does not request a character set.

• mysqld was started with the [--skip-character-set-client-handshake](#page-54-0) option, which causes it to ignore client character set configuration.

Some character sets cannot be used as the client character set. Attempting to use them as the [character\\_set\\_client](#page-99-1) value produces an error. See Impermissible Client Character Sets.

<span id="page-100-0"></span>• [character\\_set\\_connection](#page-100-0)

| System Variable      | character_set_connection |
|----------------------|--------------------------|
| Scope                | Global, Session          |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | No                       |
| Type                 | String                   |
| Default Value        | utf8mb4                  |

The character set used for literals specified without a character set introducer and for number-tostring conversion. For information about introducers, see Section 12.3.8, "Character Set Introducers".

<span id="page-100-1"></span>• [character\\_set\\_database](#page-100-1)

| System Variable      | character_set_database                                                                                  |
|----------------------|---------------------------------------------------------------------------------------------------------|
| Scope                | Global, Session                                                                                         |
| Dynamic              | Yes                                                                                                     |
| SET_VAR Hint Applies | No                                                                                                      |
| Type                 | String                                                                                                  |
| Default Value        | utf8mb4                                                                                                 |
| Footnote             | This option is dynamic, but should be set only by<br>server. You should not set this variable manually. |

The character set used by the default database. The server sets this variable whenever the default database changes. If there is no default database, the variable has the same value as [character\\_set\\_server](#page-101-1).

As of MySQL 8.0.14, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

The global [character\\_set\\_database](#page-100-1) and [collation\\_database](#page-103-0) system variables are deprecated; expect them to be removed in a future version of MySQL.

Assigning a value to the session [character\\_set\\_database](#page-100-1) and [collation\\_database](#page-103-0) system variables is deprecated and assignments produce a warning. Expect the session variables to become read-only (and assignments to them to produce an error) in a future version of MySQL in which it remains possible to access the session variables to determine the database character set and collation for the default database.

<span id="page-100-2"></span>• [character\\_set\\_filesystem](#page-100-2)

| Command-Line Format  | character-set-filesystem=name |
|----------------------|-------------------------------|
| System Variable      | character_set_filesystem      |
| Scope                | Global, Session               |
| Dynamic              | Yes                           |
| SET_VAR Hint Applies | No                            |

| Type          | String |
|---------------|--------|
| Default Value | binary |

The file system character set. This variable is used to interpret string literals that refer to file names, such as in the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD\_FILE() function. Such file names are converted from [character\\_set\\_client](#page-99-1) to [character\\_set\\_filesystem](#page-100-2) before the file opening attempt occurs. The default value is binary, which means that no conversion occurs. For systems on which multibyte file names are permitted, a different value may be more appropriate. For example, if the system represents file names using UTF-8, set [character\\_set\\_filesystem](#page-100-2) to 'utf8mb4'.

As of MySQL 8.0.14, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-101-0"></span>• [character\\_set\\_results](#page-101-0)

| System Variable      | character_set_results |
|----------------------|-----------------------|
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | String                |
| Default Value        | utf8mb4               |

The character set used for returning query results to the client. This includes result data such as column values, result metadata such as column names, and error messages.

<span id="page-101-1"></span>• [character\\_set\\_server](#page-101-1)

| Command-Line Format  | character-set-server=name |
|----------------------|---------------------------|
| System Variable      | character_set_server      |
| Scope                | Global, Session           |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | String                    |
| Default Value        | utf8mb4                   |

The servers default character set. See Section 12.15, "Character Set Configuration". If you set this variable, you should also set [collation\\_server](#page-103-1) to specify the collation for the character set.

<span id="page-101-2"></span>• [character\\_set\\_system](#page-101-2)

| System Variable      | character_set_system |
|----------------------|----------------------|
| Scope                | Global               |
| Dynamic              | No                   |
| SET_VAR Hint Applies | No                   |
| Type                 | String               |
| Default Value        | utf8mb3              |

The character set used by the server for storing identifiers. The value is always utf8mb3.

<span id="page-102-0"></span>• [character\\_sets\\_dir](#page-102-0)

| Command-Line Format  | character-sets-dir=dir_name |
|----------------------|-----------------------------|
| System Variable      | character_sets_dir          |
| Scope                | Global                      |
| Dynamic              | No                          |
| SET_VAR Hint Applies | No                          |
| Type                 | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-102-1"></span>• [check\\_proxy\\_users](#page-102-1)

| Command-Line Format  | check-proxy-users[={OFF ON}] |
|----------------------|------------------------------|
| System Variable      | check_proxy_users            |
| Scope                | Global                       |
| Dynamic              | Yes                          |
| SET_VAR Hint Applies | No                           |
| Type                 | Boolean                      |
| Default Value        | OFF                          |

Some authentication plugins implement proxy user mapping for themselves (for example, the PAM and Windows authentication plugins). Other authentication plugins do not support proxy users by default. Of these, some can request that the MySQL server itself map proxy users according to granted proxy privileges: mysql\_native\_password, sha256\_password.

If the [check\\_proxy\\_users](#page-102-1) system variable is enabled, the server performs proxy user mapping for any authentication plugins that make such a request. However, it may also be necessary to enable plugin-specific system variables to take advantage of server proxy user mapping support:

- For the mysql\_native\_password plugin, enable [mysql\\_native\\_password\\_proxy\\_users](#page-164-1).
- For the sha256\_password plugin, enable [sha256\\_password\\_proxy\\_users](#page-197-1).

For information about user proxying, see Section 8.2.19, "Proxy Users".

<span id="page-102-2"></span>• [collation\\_connection](#page-102-2)

| System Variable      | collation_connection |
|----------------------|----------------------|
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | String               |

The collation of the connection character set. [collation\\_connection](#page-102-2) is important for comparisons of literal strings. For comparisons of strings with column values, [collation\\_connection](#page-102-2) does not matter because columns have their own collation, which has a higher collation precedence (see Section 12.8.4, "Collation Coercibility in Expressions").

In MySQL 8.0.33 and later, using the name of a user-defined collation for this variable raises a warning.

## <span id="page-103-0"></span>• [collation\\_database](#page-103-0)

| System Variable      | collation_database                                                                                      |
|----------------------|---------------------------------------------------------------------------------------------------------|
| Scope                | Global, Session                                                                                         |
| Dynamic              | Yes                                                                                                     |
| SET_VAR Hint Applies | No                                                                                                      |
| Type                 | String                                                                                                  |
| Default Value        | utf8mb4_0900_ai_ci                                                                                      |
| Footnote             | This option is dynamic, but should be set only by<br>server. You should not set this variable manually. |

The collation used by the default database. The server sets this variable whenever the default database changes. If there is no default database, the variable has the same value as [collation\\_server](#page-103-1).

As of MySQL 8.0.18, setting the session value of this system variable is no longer a restricted operation.

The global [character\\_set\\_database](#page-100-1) and [collation\\_database](#page-103-0) system variables are deprecated; expect them to be removed in a future version of MySQL.

Assigning a value to the session [character\\_set\\_database](#page-100-1) and [collation\\_database](#page-103-0) system variables is deprecated and assignments produce a warning. Expect the session variables to become read-only (and assignments to produce an error) in a future version of MySQL in which it remains possible to access the session variables to determine the database character set and collation for the default database.

In MySQL 8.0.33 and later, using the name of a user-defined collation for [collation\\_database](#page-103-0) raises a warning.

## <span id="page-103-1"></span>• [collation\\_server](#page-103-1)

| Command-Line Format  | collation-server=name |
|----------------------|-----------------------|
| System Variable      | collation_server      |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | String                |
| Default Value        | utf8mb4_0900_ai_ci    |

The server's default collation. See Section 12.15, "Character Set Configuration".

Beginning with MySQL 8.0.33, setting this to the name of a user-defined collation raises a warning.

## • [completion\\_type](#page-103-2)

<span id="page-103-2"></span>

|     | Command-Line Format  | completion-type=# |
|-----|----------------------|-------------------|
|     | System Variable      | completion_type   |
|     | Scope                | Global, Session   |
|     | Dynamic              | Yes               |
|     | SET_VAR Hint Applies | No                |
| 874 | Type                 | Enumeration       |

| Default Value | NO_CHAIN |
|---------------|----------|
| Valid Values  | NO_CHAIN |
|               | CHAIN    |
|               | RELEASE  |
|               | 0        |
|               | 1        |
|               | 2        |

The transaction completion type. This variable can take the values shown in the following table. The variable can be assigned using either the name values or corresponding integer values.

| Value           | Description                                                                                                                                                                                                       |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NO_CHAIN (or 0) | COMMIT and ROLLBACK are unaffected. This is<br>the default value.                                                                                                                                                 |
| CHAIN (or 1)    | COMMIT and ROLLBACK are equivalent to<br>COMMIT AND CHAIN and ROLLBACK AND<br>CHAIN, respectively. (A new transaction starts<br>immediately with the same isolation level as the<br>just-terminated transaction.) |
| RELEASE (or 2)  | COMMIT and ROLLBACK are equivalent to<br>COMMIT RELEASE and ROLLBACK RELEASE,<br>respectively. (The server disconnects after<br>terminating the transaction.)                                                     |

[completion\\_type](#page-103-2) affects transactions that begin with START TRANSACTION or BEGIN and end with COMMIT or ROLLBACK. It does not apply to implicit commits resulting from execution of the statements listed in Section 15.3.3, "Statements That Cause an Implicit Commit". It also does not apply for XA COMMIT, XA ROLLBACK, or when [autocommit=1](#page-91-0).

<span id="page-104-0"></span>• [component\\_scheduler.enabled](#page-104-0)

| Command-Line Format  | component<br>scheduler.enabled[=value] |
|----------------------|----------------------------------------|
| System Variable      | component_scheduler.enabled            |
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Boolean                                |
| Default Value        | ON                                     |

When set to OFF at startup, the background thread does not start. Tasks can still be scheduled, but they do not run until component\_scheduler is enabled. When set to ON at startup, the component is fully operational.

It is also possible to set the value dynamically to get the following effects:

- ON starts the background thread that begins servicing the queue immediately.
- OFF signals a termination of the background thread, which waits for it to end. The background thread checks the termination flag before accessing the queue to check for tasks to execute.

## <span id="page-105-0"></span>• [concurrent\\_insert](#page-105-0)

| Command-Line Format  | concurrent-insert[=value] |
|----------------------|---------------------------|
| System Variable      | concurrent_insert         |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Enumeration               |
| Default Value        | AUTO                      |
| Valid Values         | NEVER                     |
|                      | AUTO                      |
|                      | ALWAYS                    |
|                      | 0                         |
|                      | 1                         |
|                      | 2                         |

If AUTO (the default), MySQL permits INSERT and SELECT statements to run concurrently for MyISAM tables that have no free blocks in the middle of the data file.

This variable can take the values shown in the following table. The variable can be assigned using either the name values or corresponding integer values.

| Value         | Description                                                                                                                                                                                                                                                                             |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NEVER (or 0)  | Disables concurrent inserts                                                                                                                                                                                                                                                             |
| AUTO (or 1)   | (Default) Enables concurrent insert for MyISAM<br>tables that do not have holes                                                                                                                                                                                                         |
| ALWAYS (or 2) | Enables concurrent inserts for all MyISAM tables,<br>even those that have holes. For a table with a<br>hole, new rows are inserted at the end of the<br>table if it is in use by another thread. Otherwise,<br>MySQL acquires a normal write lock and inserts<br>the row into the hole. |

If you start mysqld with [--skip-new](#page-72-0), [concurrent\\_insert](#page-105-0) is set to NEVER.

See also Section 10.11.3, "Concurrent Inserts".

## <span id="page-105-1"></span>• [connect\\_timeout](#page-105-1)

| Command-Line Format  | connect-timeout=# |
|----------------------|-------------------|
| System Variable      | connect_timeout   |
| Scope                | Global            |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | Integer           |
| Default Value        | 10                |
| Minimum Value        | 2                 |

| Maximum Value | 31536000 |
|---------------|----------|
| Unit          | seconds  |

The number of seconds that the mysqld server waits for a connect packet before responding with Bad handshake. The default value is 10 seconds.

Increasing the [connect\\_timeout](#page-105-1) value might help if clients frequently encounter errors of the form Lost connection to MySQL server at 'XXX', system error: errno.

<span id="page-106-0"></span>• [connection\\_memory\\_chunk\\_size](#page-106-0)

| Command-Line Format  | connection-memory-chunk-size=# |
|----------------------|--------------------------------|
| System Variable      | connection_memory_chunk_size   |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |
| Type                 | Integer                        |
| Default Value        | 8192                           |
| Minimum Value        | 0                              |
| Maximum Value        | 536870912                      |
| Unit                 | bytes                          |

Set the chunking size for updates to the global memory usage counter Global\_connection\_memory. The status variable is updated only when total memory consumption by all user connections changes by more than this amount. Disable updates by setting connection\_memory\_chunk\_size = 0.

The memory calculation is exclusive of any memory used by system users such as the MySQL root user. Memory used by the InnoDB buffer pool is also not included.

You must have the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege to set this variable.

<span id="page-106-1"></span>• [connection\\_memory\\_limit](#page-106-1)

| Command-Line Format  | connection-memory-limit=# |
|----------------------|---------------------------|
| System Variable      | connection_memory_limit   |
| Scope                | Global, Session           |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |
| Default Value        | 18446744073709551615      |
| Minimum Value        | 2097152                   |
| Maximum Value        | 18446744073709551615      |

| Unit | bytes |
|------|-------|
|------|-------|

Set the maximum amount of memory that can be used by a single user connection. If any user connection uses more than this amount, all queries from this connection are rejected with [ER\\_CONN\\_LIMIT](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_conn_limit), including any queries currently running.

The limit set by this variable does not apply to system users, or to the MySQL root account. Memory used by the InnoDB buffer pool is also not included.

You must have the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege to set this variable.

## <span id="page-107-0"></span>• [core\\_file](#page-107-0)

| System Variable      | core_file |
|----------------------|-----------|
| Scope                | Global    |
| Dynamic              | No        |
| SET_VAR Hint Applies | No        |
| Type                 | Boolean   |
| Default Value        | OFF       |

Whether to write a core file if the server unexpectedly exits. This variable is set by the [--core-file](#page-56-0) option.

## <span id="page-107-1"></span>• [create\\_admin\\_listener\\_thread](#page-107-1)

| Command-Line Format  | create-admin-listener<br>thread[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | create_admin_listener_thread               |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

Whether to use a dedicated listening thread for client connections on the administrative network interface (see Section 7.1.12.1, "Connection Interfaces"). The default is OFF; that is, the manager thread for ordinary connections on the main interface also handles connections for the administrative interface.

Depending on factors such as platform type and workload, you may find one setting for this variable yields better performance than the other setting.

Setting [create\\_admin\\_listener\\_thread](#page-107-1) has no effect if [admin\\_address](#page-83-0) is not specified because in that case the server maintains no administrative network interface.

## <span id="page-107-2"></span>• [cte\\_max\\_recursion\\_depth](#page-107-2)

| Command-Line Format  | cte-max-recursion-depth=# |
|----------------------|---------------------------|
| System Variable      | cte_max_recursion_depth   |
| Scope                | Global, Session           |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |

| Default Value | 1000       |
|---------------|------------|
| Minimum Value | 0          |
| Maximum Value | 4294967295 |

The common table expression (CTE) maximum recursion depth. The server terminates execution of any CTE that recurses more levels than the value of this variable. For more information, see Limiting Common Table Expression Recursion.

## <span id="page-108-0"></span>• [datadir](#page-108-0)

| Command-Line Format  | datadir=dir_name |
|----------------------|------------------|
| System Variable      | datadir          |
| Scope                | Global           |
| Dynamic              | No               |
| SET_VAR Hint Applies | No               |
| Type                 | Directory name   |

The path to the MySQL server data directory. Relative paths are resolved with respect to the current directory. If you expect the server to be started automatically (that is, in contexts for which you cannot know the current directory in advance), it is best to specify the [datadir](#page-108-0) value as an absolute path.

## <span id="page-108-1"></span>• [debug](#page-108-1)

| Command-Line Format     | debug[=debug_options]     |
|-------------------------|---------------------------|
| System Variable         | debug                     |
| Scope                   | Global, Session           |
| Dynamic                 | Yes                       |
| SET_VAR Hint Applies    | No                        |
| Type                    | String                    |
| Default Value (Unix)    | d:t:i:o,/tmp/mysqld.trace |
| Default Value (Windows) | d:t:i:O,\mysqld.trace     |

This variable indicates the current debugging settings. It is available only for servers built with debugging support. The initial value comes from the value of instances of the [--debug](#page-57-0) option given at server startup. The global and session values may be set at runtime.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

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
```

```
+---------+
| P:T |
+---------+
mysql> SET debug = '-P';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| T |
+---------+
```

For more information, see Section 7.9.4, "The DBUG Package".

<span id="page-109-0"></span>• [debug\\_sync](#page-109-0)

| System Variable      | debug_sync |
|----------------------|------------|
| Scope                | Session    |
| Dynamic              | Yes        |
| SET_VAR Hint Applies | No         |
| Type                 | String     |

This variable is the user interface to the Debug Sync facility. Use of Debug Sync requires that MySQL be configured with the -DWITH\_DEBUG=ON CMake option (see Section 2.8.7, "MySQL Source-Configuration Options"); otherwise, this system variable is not available.

The global variable value is read only and indicates whether the facility is enabled. By default, Debug Sync is disabled and the value of [debug\\_sync](#page-109-0) is OFF. If the server is started with [--debug-sync](#page-57-1)[timeout=](#page-57-1)N, where N is a timeout value greater than 0, Debug Sync is enabled and the value of [debug\\_sync](#page-109-0) is ON - current signal followed by the signal name. Also, N becomes the default timeout for individual synchronization points.

The session value can be read by any user and has the same value as the global variable. The session value can be set to control synchronization points.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

For a description of the Debug Sync facility and how to use synchronization points, see [MySQL](https://dev.mysql.com/doc/index-other.md) [Server Doxygen Documentation.](https://dev.mysql.com/doc/index-other.md)

<span id="page-109-1"></span>• [default\\_authentication\\_plugin](#page-109-1)

| Command-Line Format  | default-authentication<br>plugin=plugin_name |
|----------------------|----------------------------------------------|
| Deprecated           | Yes                                          |
| System Variable      | default_authentication_plugin                |
| Scope                | Global                                       |
| Dynamic              | No                                           |
| SET_VAR Hint Applies | No                                           |
| Type                 | Enumeration                                  |
| Default Value        | caching_sha2_password                        |
| Valid Values         | mysql_native_password                        |
|                      | sha256_password                              |

```
caching_sha2_password
```

The default authentication plugin. This must be a plugin that uses internal credentials storage, so these values are permitted:

- mysql\_native\_password: Use MySQL native passwords; see Section 8.4.1.1, "Native Pluggable Authentication".
- sha256\_password: Use SHA-256 passwords; see Section 8.4.1.3, "SHA-256 Pluggable Authentication".
- caching\_sha2\_password: Use SHA-256 passwords; see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

For information about which authentication plugins use internal credentials storage, see Section 8.2.15, "Password Management".

![](_page_110_Picture_7.jpeg)

#### **Note**

In MySQL 8.0, caching\_sha2\_password is the default authentication plugin rather than mysql\_native\_password. For information about the implications of this change for server operation and compatibility of the server with clients and connectors, see caching\_sha2\_password as the Preferred Authentication Plugin.

Prior to MySQL 8.0.27, the [default\\_authentication\\_plugin](#page-109-1) value affects these aspects of server operation:

- It determines which authentication plugin the server assigns to new accounts created by CREATE USER statements that do not explicitly specify an authentication plugin.
- For an account created with a statement of the following form, the server associates the account with the default authentication plugin and assigns the account the given password, hashed as required by that plugin:

```
CREATE USER ... IDENTIFIED BY 'cleartext password';
```

As of MySQL 8.0.27, which introduces multifactor authentication, [default\\_authentication\\_plugin](#page-109-1) is still used, but in conjunction with and at a lower precedence than the [authentication\\_policy](#page-87-2) system variable. For details, see The Default Authentication Plugin. Because of this diminished role, [default\\_authentication\\_plugin](#page-109-1) is deprecated as of MySQL 8.0.27 and subject to removal in a future MySQL version.

<span id="page-110-0"></span>• [default\\_collation\\_for\\_utf8mb4](#page-110-0)

| System Variable      | default_collation_for_utf8mb4 |
|----------------------|-------------------------------|
| Scope                | Global, Session               |
| Dynamic              | Yes                           |
| SET_VAR Hint Applies | No                            |
| Type                 | Enumeration                   |
| Default Value        | utf8mb4_0900_ai_ci            |
| Valid Values         | utf8mb4_0900_ai_ci            |

utf8mb4\_general\_ci

![](_page_111_Picture_2.jpeg)

### **Important**

The default\_collation\_for\_utf8mb4 system variable is for internal use by MySQL Replication only.

This variable is set by the server to the default collation for the utf8mb4 character set. The value of the variable is replicated from a source to a replica so that the replica can correctly process data originating from a source with a different default collation for utf8mb4. This variable is primarily intended to support replication from a MySQL 5.7 or older replication source server to a MySQL 8.0 replica server, or group replication with a MySQL 5.7 primary node and one or more MySQL 8.0 secondaries. The default collation for utf8mb4 in MySQL 5.7 is utf8mb4\_general\_ci, but utf8mb4\_0900\_ai\_ci in MySQL 8.0. The variable is not present in releases earlier than MySQL 8.0, so if the replica does not receive a value for the variable, it assumes the source is from an earlier release and sets the value to the previous default collation utf8mb4\_general\_ci.

As of MySQL 8.0.18, setting the session value of this system variable is no longer a restricted operation.

The default utf8mb4 collation is used in the following statements:

- SHOW COLLATION and SHOW CHARACTER SET.
- CREATE TABLE and ALTER TABLE having a CHARACTER SET utf8mb4 clause without a COLLATION clause, either for the table character set or for a column character set.
- CREATE DATABASE and ALTER DATABASE having a CHARACTER SET utf8mb4 clause without a COLLATION clause.
- Any statement containing a string literal of the form \_utf8mb4'some text' without a COLLATE clause.

See also Section 12.9, "Unicode Support".

<span id="page-111-0"></span>• [default\\_password\\_lifetime](#page-111-0)

| Command-Line Format  | default-password-lifetime=# |
|----------------------|-----------------------------|
| System Variable      | default_password_lifetime   |
| Scope                | Global                      |
| Dynamic              | Yes                         |
| SET_VAR Hint Applies | No                          |
| Type                 | Integer                     |
| Default Value        | 0                           |
| Minimum Value        | 0                           |
| Maximum Value        | 65535                       |
| Unit                 | days                        |

This variable defines the global automatic password expiration policy. The default [default\\_password\\_lifetime](#page-111-0) value is 0, which disables automatic password expiration. If the value of [default\\_password\\_lifetime](#page-111-0) is a positive integer N, it indicates the permitted password lifetime; passwords must be changed every N days.

The global password expiration policy can be overridden as desired for individual accounts using the password expiration option of the CREATE USER and ALTER USER statements. See Section 8.2.15, "Password Management".

<span id="page-112-0"></span>• [default\\_storage\\_engine](#page-112-0)

| Command-Line Format  | default-storage-engine=name |
|----------------------|-----------------------------|
| System Variable      | default_storage_engine      |
| Scope                | Global, Session             |
| Dynamic              | Yes                         |
| SET_VAR Hint Applies | No                          |
| Type                 | Enumeration                 |
| Default Value        | InnoDB                      |

The default storage engine for tables. See Chapter 18, Alternative Storage Engines. This variable sets the storage engine for permanent tables only. To set the storage engine for TEMPORARY tables, set the [default\\_tmp\\_storage\\_engine](#page-113-0) system variable.

To see which storage engines are available and enabled, use the SHOW ENGINES statement or query the INFORMATION\_SCHEMA ENGINES table.

If you disable the default storage engine at server startup, you must set the default engine for both permanent and TEMPORARY tables to a different engine, or else the server does not start.

<span id="page-112-1"></span>• [default\\_table\\_encryption](#page-112-1)

| Command-Line Format  | default-table-encryption[={OFF <br>ON}] |
|----------------------|-----------------------------------------|
| System Variable      | default_table_encryption                |
| Scope                | Global, Session                         |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | Yes                                     |
| Type                 | Boolean                                 |
| Default Value        | OFF                                     |

Defines the default encryption setting applied to schemas and general tablespaces when they are created without specifying an ENCRYPTION clause.

The [default\\_table\\_encryption](#page-112-1) variable is only applicable to user-created schemas and general tablespaces. It does not govern encryption of the mysql system tablespace.

Setting the runtime value of [default\\_table\\_encryption](#page-112-1) requires the SYSTEM\_VARIABLES\_ADMIN and TABLE\_ENCRYPTION\_ADMIN privileges, or the deprecated SUPER privilege.

The value of [default\\_table\\_encryption](#page-112-1) cannot be changed while Group Replication is running.

[default\\_table\\_encryption](#page-112-1) supports SET PERSIST and SET PERSIST\_ONLY syntax. See Section 7.1.9.3, "Persisted System Variables".

For more information, see Defining an Encryption Default for Schemas and General Tablespaces.

<span id="page-113-0"></span>• [default\\_tmp\\_storage\\_engine](#page-113-0)

| Command-Line Format  | default-tmp-storage-engine=name |
|----------------------|---------------------------------|
| System Variable      | default_tmp_storage_engine      |
| Scope                | Global, Session                 |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | Yes                             |
| Type                 | Enumeration                     |
| Default Value        | InnoDB                          |

The default storage engine for TEMPORARY tables (created with CREATE TEMPORARY TABLE). To set the storage engine for permanent tables, set the [default\\_storage\\_engine](#page-112-0) system variable. Also see the discussion of that variable regarding possible values.

If you disable the default storage engine at server startup, you must set the default engine for both permanent and TEMPORARY tables to a different engine, or else the server does not start.

<span id="page-113-1"></span>• [default\\_week\\_format](#page-113-1)

| Command-Line Format  | default-week-format=# |
|----------------------|-----------------------|
| System Variable      | default_week_format   |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Integer               |
| Default Value        | 0                     |
| Minimum Value        | 0                     |
| Maximum Value        | 7                     |

The default mode value to use for the WEEK() function. See Section 14.7, "Date and Time Functions".

<span id="page-113-2"></span>• [delay\\_key\\_write](#page-113-2)

| Command-Line Format  | delay-key-write[={OFF ON ALL}] |
|----------------------|--------------------------------|
| System Variable      | delay_key_write                |
| Scope                | Global                         |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |
| Type                 | Enumeration                    |
| Default Value        | ON                             |
| Valid Values         | OFF                            |
|                      | ON                             |

ALL

This variable specifies how to use delayed key writes. It applies only to MyISAM tables. Delayed key writing causes key buffers not to be flushed between writes. See also Section 18.2.1, "MyISAM Startup Options".

This variable can have one of the following values to affect handling of the DELAY\_KEY\_WRITE table option that can be used in CREATE TABLE statements.

| Option | Description                                                                                                    |
|--------|----------------------------------------------------------------------------------------------------------------|
| OFF    | DELAY_KEY_WRITE is ignored.                                                                                    |
| ON     | MySQL honors any DELAY_KEY_WRITE option<br>specified in CREATE TABLE statements. This is<br>the default value. |
| ALL    | All new opened tables are treated as if they were<br>created with the DELAY_KEY_WRITE option<br>enabled.       |

![](_page_114_Picture_5.jpeg)

#### **Note**

If you set this variable to ALL, you should not use MyISAM tables from within another program (such as another MySQL server or myisamchk) when the tables are in use. Doing so leads to index corruption.

If DELAY\_KEY\_WRITE is enabled for a table, the key buffer is not flushed for the table on every index update, but only when the table is closed. This speeds up writes on keys a lot, but if you use this feature, you should add automatic checking of all MyISAM tables by starting the server with the [myisam\\_recover\\_options](#page-162-1) system variable set (for example, myisam\_recover\_options='BACKUP,FORCE'). See [Section 7.1.8, "Server System Variables"](#page-81-1), and Section 18.2.1, "MyISAM Startup Options".

If you start mysqld with [--skip-new](#page-72-0), [delay\\_key\\_write](#page-113-2) is set to OFF.

![](_page_114_Picture_10.jpeg)

## **Warning**

If you enable external locking with [--external-locking](#page-59-1), there is no protection against index corruption for tables that use delayed key writes.

<span id="page-114-0"></span>• [delayed\\_insert\\_limit](#page-114-0)

| Command-Line Format              | delayed-insert-limit=# |
|----------------------------------|------------------------|
| Deprecated                       | Yes                    |
| System Variable                  | delayed_insert_limit   |
| Scope                            | Global                 |
| Dynamic                          | Yes                    |
| SET_VAR Hint Applies             | No                     |
| Type                             | Integer                |
| Default Value                    | 100                    |
| Minimum Value                    | 1                      |
| Maximum Value (64-bit platforms) | 18446744073709551615   |

| Maximum Value (32-bit platforms) | 4294967295 |
|----------------------------------|------------|
|----------------------------------|------------|

This system variable is deprecated (because DELAYED inserts are not supported), and you should expect it to be removed in a future release.

<span id="page-115-0"></span>• [delayed\\_insert\\_timeout](#page-115-0)

| Command-Line Format  | delayed-insert-timeout=# |
|----------------------|--------------------------|
| Deprecated           | Yes                      |
| System Variable      | delayed_insert_timeout   |
| Scope                | Global                   |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | No                       |
| Type                 | Integer                  |
| Default Value        | 300                      |
| Minimum Value        | 1                        |
| Maximum Value        | 31536000                 |
| Unit                 | seconds                  |

This system variable is deprecated (because DELAYED inserts are not supported), and you should expect it to be removed in a future release.

<span id="page-115-1"></span>• [delayed\\_queue\\_size](#page-115-1)

| Command-Line Format              | delayed-queue-size=# |
|----------------------------------|----------------------|
| Deprecated                       | Yes                  |
| System Variable                  | delayed_queue_size   |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value                    | 1000                 |
| Minimum Value                    | 1                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

This system variable is deprecated (because DELAYED inserts are not supported), and you should expect it to be removed in a future release.

<span id="page-115-2"></span>• [disabled\\_storage\\_engines](#page-115-2)

| Command-Line Format  | disabled-storage<br>engines=engine[,engine] |
|----------------------|---------------------------------------------|
| System Variable      | disabled_storage_engines                    |
| Scope                | Global                                      |
| Dynamic              | No                                          |
| SET_VAR Hint Applies | No                                          |
| Type                 | String                                      |

| Default Value | empty string |
|---------------|--------------|
|---------------|--------------|

This variable indicates which storage engines cannot be used to create tables or tablespaces. For example, to prevent new MyISAM or FEDERATED tables from being created, start the server with these lines in the server option file:

```
[mysqld]
disabled_storage_engines="MyISAM,FEDERATED"
```

By default, [disabled\\_storage\\_engines](#page-115-2) is empty (no engines disabled), but it can be set to a comma-separated list of one or more engines (not case-sensitive). Any engine named in the value cannot be used to create tables or tablespaces with CREATE TABLE or CREATE TABLESPACE, and cannot be used with ALTER TABLE ... ENGINE or ALTER TABLESPACE ... ENGINE to change the storage engine of existing tables or tablespaces. Attempts to do so result in an [ER\\_DISABLED\\_STORAGE\\_ENGINE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_disabled_storage_engine) error.

[disabled\\_storage\\_engines](#page-115-2) does not restrict other DDL statements for existing tables, such as CREATE INDEX, TRUNCATE TABLE, ANALYZE TABLE, DROP TABLE, or DROP TABLESPACE. This permits a smooth transition so that existing tables or tablespaces that use a disabled engine can be migrated to a permitted engine by means such as ALTER TABLE ... ENGINE permitted\_engine.

It is permitted to set the [default\\_storage\\_engine](#page-112-0) or [default\\_tmp\\_storage\\_engine](#page-113-0) system variable to a storage engine that is disabled. This could cause applications to behave erratically or fail, although that might be a useful technique in a development environment for identifying applications that use disabled engines, so that they can be modified.

[disabled\\_storage\\_engines](#page-115-2) is disabled and has no effect if the server is started with any of these options: [--initialize](#page-60-0), [--initialize-insecure](#page-61-0), [--skip-grant-tables](#page-70-1).

![](_page_116_Picture_8.jpeg)

## **Note**

Setting [disabled\\_storage\\_engines](#page-115-2) might cause an issue with mysql\_upgrade. For details, see Section 6.4.5, "mysql\_upgrade — Check and Upgrade MySQL Tables".

<span id="page-116-0"></span>• [disconnect\\_on\\_expired\\_password](#page-116-0)

| Command-Line Format  | disconnect-on-expired<br>password[={OFF ON}] |
|----------------------|----------------------------------------------|
| System Variable      | disconnect_on_expired_password               |
| Scope                | Global                                       |
| Dynamic              | No                                           |
| SET_VAR Hint Applies | No                                           |
| Type                 | Boolean                                      |
| Default Value        | ON                                           |

This variable controls how the server handles clients with expired passwords:

• If the client indicates that it can handle expired passwords, the value of [disconnect\\_on\\_expired\\_password](#page-116-0) is irrelevant. The server permits the client to connect but puts it in sandbox mode.

- If the client does not indicate that it can handle expired passwords, the server handles the client according to the value of [disconnect\\_on\\_expired\\_password](#page-116-0):
  - If [disconnect\\_on\\_expired\\_password](#page-116-0): is enabled, the server disconnects the client.
  - If [disconnect\\_on\\_expired\\_password](#page-116-0): is disabled, the server permits the client to connect but puts it in sandbox mode.

For more information about the interaction of client and server settings relating to expired-password handling, see Section 8.2.16, "Server Handling of Expired Passwords".

<span id="page-117-0"></span>• [div\\_precision\\_increment](#page-117-0)

| Command-Line Format  | div-precision-increment=# |
|----------------------|---------------------------|
| System Variable      | div_precision_increment   |
| Scope                | Global, Session           |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | Yes                       |
| Type                 | Integer                   |
| Default Value        | 4                         |
| Minimum Value        | 0                         |
| Maximum Value        | 30                        |

This variable indicates the number of digits by which to increase the scale of the result of division operations performed with the / operator. The default value is 4. The minimum and maximum values are 0 and 30, respectively. The following example illustrates the effect of increasing the default value.

```
mysql> SELECT 1/7;
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

<span id="page-117-1"></span>• [dragnet.log\\_error\\_filter\\_rules](#page-117-1)

| Command-Line Format  | dragnet.log-error-filter<br>rules=value |
|----------------------|-----------------------------------------|
| System Variable      | dragnet.log_error_filter_rules          |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | String                                  |

| Default Value | IF prio>=INFORMATION THEN drop.  |
|---------------|----------------------------------|
|               | IF EXISTS source_line THEN unset |
|               | source_line.                     |

The filter rules that control operation of the log\_filter\_dragnet error log filter component. If log\_filter\_dragnet is not installed, [dragnet.log\\_error\\_filter\\_rules](#page-117-1) is unavailable. If log\_filter\_dragnet is installed but not enabled, changes to [dragnet.log\\_error\\_filter\\_rules](#page-117-1) have no effect.

The effect of the default value is similar to the filtering performed by the log\_sink\_internal filter with a setting of [log\\_error\\_verbosity=2](#page-144-1).

As of MySQL 8.0.12, the dragnet.Status status variable can be consulted to determine the result of the most recent assignment to [dragnet.log\\_error\\_filter\\_rules](#page-117-1).

Prior to MySQL 8.0.12, successful assignments to [dragnet.log\\_error\\_filter\\_rules](#page-117-1) at runtime produce a note confirming the new value:

```
mysql> SET GLOBAL dragnet.log_error_filter_rules = 'IF prio <> 0 THEN unset prio.';
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
 Level: Note
 Code: 4569
Message: filter configuration accepted:
 SET @@GLOBAL.dragnet.log_error_filter_rules=
 'IF prio!=ERROR THEN unset prio.';
```

The value displayed by SHOW WARNINGS indicates the "decompiled" canonical representation after the rule set has been successfully parsed and compiled into internal form. Semantically, this canonical form is identical to the value assigned to [dragnet.log\\_error\\_filter\\_rules](#page-117-1), but there may be some differences between the assigned and canonical values, as illustrated by the preceding example:

- The <> operator is changed to !=.
- The numeric priority of 0 is changed to the corresponding priority symbol ERROR.
- Optional spaces are removed.

For additional information, see Section 7.4.2.4, "Types of Error Log Filtering", and Section 7.5.3, "Error Log Components".

<span id="page-118-0"></span>• [enterprise\\_encryption.maximum\\_rsa\\_key\\_size](#page-118-0)

| Command-Line Format  | enterprise-encryption.maximum-rsa<br>key-size=# |  |
|----------------------|-------------------------------------------------|--|
| System Variable      | enterprise_encryption.maximum_rsa_key_size      |  |
| Scope                | Global                                          |  |
| Dynamic              | Yes                                             |  |
| SET_VAR Hint Applies | No                                              |  |
| Type                 | Integer                                         |  |
| Default Value        | 4096                                            |  |
| Minimum Value        | 2048                                            |  |

| Maximum Value | 16384 |  |
|---------------|-------|--|
|---------------|-------|--|

This variable limits the maximum size of RSA keys generated by MySQL Enterprise Encryption. The variable is available only if the MySQL Enterprise Encryption component component\_enterprise\_encryption is installed, which is available from MySQL 8.0.30. The variable is not available if the openssl\_udf shared library is used to provide MySQL Enterprise Encryption functions.

The lowest setting is 2048 bits, which is the minimum RSA key length that is acceptable by current best practice. The default setting is 4096 bits. The highest setting is 16384 bits. Generating longer keys can consume significant CPU resources, so you can use this setting to limit keys to a length that provides adequate security for your requirements while balancing this with resource usage. Note that the functions provided by the openssl\_udf shared library allow key lengths starting at 1024 bits, and following an upgrade to the component, the minimum key length is greater than this. See Section 8.6.2, "Configuring MySQL Enterprise Encryption" for more information.

<span id="page-119-1"></span>• [enterprise\\_encryption.rsa\\_support\\_legacy\\_padding](#page-119-1)

| Command-Line Format  | enterprise<br>encryption.rsa_support_legacy_padding[={OFF <br>ON}] |  |
|----------------------|--------------------------------------------------------------------|--|
| System Variable      | enterprise_encryption.rsa_support_legacy_padding                   |  |
| Scope                | Global                                                             |  |
| Dynamic              | Yes                                                                |  |
| SET_VAR Hint Applies | No                                                                 |  |
| Type                 | Boolean                                                            |  |
| Default Value        | OFF                                                                |  |

This variable controls whether encrypted data and signatures that MySQL Enterprise Encryption produced with the openssl\_udf shared library functions used before MySQL 8.0.30, can be decrypted or verified by the functions of the MySQL Enterprise Encryption component component\_enterprise\_encryption, which is available from MySQL 8.0.30. The variable is available only if the MySQL Enterprise Encryption component is installed, and it is not available if the openssl\_udf shared library is used to provide MySQL Enterprise Encryption functions.

For the component functions to support decryption and verification for content produced by the legacy openssl\_udf shared library functions, you must set the system variable padding to ON. When ON is set, if the component functions cannot decrypt or verify content when assuming it has the RSAES-OAEP or RSASSA-PSS scheme (as used by the component), they make another attempt assuming it has the RSAES-PKCS1-v1\_5 or RSASSA-PKCS1-v1\_5 scheme (as used by the openssl\_udf shared library functions). When OFF is set, if the component functions cannot decrypt or verify content using their normal schemes, they return null output. See Section 8.6.2, "Configuring MySQL Enterprise Encryption" for more information.

<span id="page-119-0"></span>• [end\\_markers\\_in\\_json](#page-119-0)

| Command-Line Format  | end-markers-in-json[={OFF ON}] |
|----------------------|--------------------------------|
| System Variable      | end_markers_in_json            |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | Yes                            |
| Type                 | Boolean                        |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

Whether optimizer JSON output should add end markers. See Section 10.15.9, "The end\_markers\_in\_json System Variable".

<span id="page-120-0"></span>• [eq\\_range\\_index\\_dive\\_limit](#page-120-0)

| Command-Line Format  | eq-range-index-dive-limit=# |
|----------------------|-----------------------------|
| System Variable      | eq_range_index_dive_limit   |
| Scope                | Global, Session             |
| Dynamic              | Yes                         |
| SET_VAR Hint Applies | Yes                         |
| Type                 | Integer                     |
| Default Value        | 200                         |
| Minimum Value        | 0                           |
| Maximum Value        | 4294967295                  |

This variable indicates the number of equality ranges in an equality comparison condition when the optimizer should switch from using index dives to index statistics in estimating the number of qualifying rows. It applies to evaluation of expressions that have either of these equivalent forms, where the optimizer uses a nonunique index to look up col\_name values:

```
col_name IN(val1, ..., valN)
col_name = val1 OR ... OR col_name = valN
```

In both cases, the expression contains N equality ranges. The optimizer can make row estimates using index dives or index statistics. If [eq\\_range\\_index\\_dive\\_limit](#page-120-0) is greater than 0, the optimizer uses existing index statistics instead of index dives if there are [eq\\_range\\_index\\_dive\\_limit](#page-120-0) or more equality ranges. Thus, to permit use of index dives for up to N equality ranges, set [eq\\_range\\_index\\_dive\\_limit](#page-120-0) to N + 1. To disable use of index statistics and always use index dives regardless of N, set [eq\\_range\\_index\\_dive\\_limit](#page-120-0) to 0.

For more information, see Equality Range Optimization of Many-Valued Comparisons.

To update table index statistics for best estimates, use ANALYZE TABLE.

<span id="page-120-1"></span>• [error\\_count](#page-120-1)

The number of errors that resulted from the last statement that generated messages. This variable is read only. See Section 15.7.7.17, "SHOW ERRORS Statement".

<span id="page-120-2"></span>• [event\\_scheduler](#page-120-2)

| Command-Line Format  | event-scheduler[=value] |
|----------------------|-------------------------|
| System Variable      | event_scheduler         |
| Scope                | Global                  |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | Enumeration             |
| Default Value        | ON                      |
| Valid Values         | ON                      |
|                      | OFF                     |

DISABLED

This variable enables or disables, and starts or stops, the Event Scheduler. The possible status values are ON, OFF, and DISABLED. Turning the Event Scheduler OFF is not the same as disabling the Event Scheduler, which requires setting the status to DISABLED. This variable and its effects on the Event Scheduler's operation are discussed in greater detail in Section 27.4.2, "Event Scheduler Configuration"

<span id="page-121-0"></span>• [explain\\_format](#page-121-0)

| Command-Line Format  | explain-format=format |
|----------------------|-----------------------|
| System Variable      | explain_format        |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Enumeration           |
| Default Value        | TRADITIONAL           |
| Valid Values         | TRADITIONAL           |
|                      | JSON                  |
|                      | TREE                  |

This variable determines the default output format used by EXPLAIN in the absence of a FORMAT option when displaying a query execution plan. Possible values and their effects are listed here:

• TRADITIONAL: Use MySQL's traditional table-based output, as if FORMAT=TRADITIONAL had been specified as part of the EXPLAIN statement. This is the variable's default value. DEFAULT is also supported as a synonym for TRADITIONAL, and has exactly the same effect.

![](_page_121_Picture_7.jpeg)

## **Note**

DEFAULT cannot be used as part of an EXPLAIN statement's FORMAT option.

- JSON: Use the JSON output format, as if FORMAT=JSON had been specified.
- TREE: Use the tree-based output format, as if FORMAT=TREE had been specified.

The setting for this variable also affects EXPLAIN ANALYZE. For this purpose, DEFAULT and TRADITIONAL are interpeted as TREE. If the value of explain\_format is JSON and an EXPLAIN ANALYZE statement having no FORMAT option is issued, the statement raises an error ([ER\\_NOT\\_SUPPORTED\\_YET](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_not_supported_yet)).

Using a format specifier with EXPLAIN or EXPLAIN ANALYZE overrides any setting for explain\_format.

The explain\_format system variable has no effect on EXPLAIN output when this statement is used to display information about table columns.

Setting the session value of explain\_format requires no special privileges; setting it on the global level requires SYSTEM\_VARIABLES\_ADMIN (or the deprecated SUPER privilege). See Section 7.1.9.1, "System Variable Privileges".

For more information and examples, see Obtaining Execution Plan Information.

<span id="page-121-1"></span>• [explicit\\_defaults\\_for\\_timestamp](#page-121-1)

| Command-Line Format  | explicit-defaults-for<br>timestamp[={OFF ON}] |
|----------------------|-----------------------------------------------|
| Deprecated           | Yes                                           |
| System Variable      | explicit_defaults_for_timestamp               |
| Scope                | Global, Session                               |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Boolean                                       |
| Default Value        | ON                                            |

This system variable determines whether the server enables certain nonstandard behaviors for default values and NULL-value handling in TIMESTAMP columns. By default, [explicit\\_defaults\\_for\\_timestamp](#page-121-1) is enabled, which disables the nonstandard behaviors. Disabling [explicit\\_defaults\\_for\\_timestamp](#page-121-1) results in a warning.

As of MySQL 8.0.18, setting the session value of this system variable is no longer a restricted operation.

If [explicit\\_defaults\\_for\\_timestamp](#page-121-1) is disabled, the server enables the nonstandard behaviors and handles TIMESTAMP columns as follows:

- TIMESTAMP columns not explicitly declared with the NULL attribute are automatically declared with the NOT NULL attribute. Assigning such a column a value of NULL is permitted and sets the column to the current timestamp. Exception: As of MySQL 8.0.22, attempting to insert NULL into a generated column declared as TIMESTAMP NOT NULL is rejected with an error.
- The first TIMESTAMP column in a table, if not explicitly declared with the NULL attribute or an explicit DEFAULT or ON UPDATE attribute, is automatically declared with the DEFAULT CURRENT\_TIMESTAMP and ON UPDATE CURRENT\_TIMESTAMP attributes.
- TIMESTAMP columns following the first one, if not explicitly declared with the NULL attribute or an explicit DEFAULT attribute, are automatically declared as DEFAULT '0000-00-00 00:00:00' (the "zero" timestamp). For inserted rows that specify no explicit value for such a column, the column is assigned '0000-00-00 00:00:00' and no warning occurs.

Depending on whether strict SQL mode or the NO\_ZERO\_DATE SQL mode is enabled, a default value of '0000-00-00 00:00:00' may be invalid. Be aware that the TRADITIONAL SQL mode includes strict mode and NO\_ZERO\_DATE. See Section 7.1.11, "Server SQL Modes".

The nonstandard behaviors just described are deprecated; expect them to be removed in a future MySQL release.

If [explicit\\_defaults\\_for\\_timestamp](#page-121-1) is enabled, the server disables the nonstandard behaviors and handles TIMESTAMP columns as follows:

- It is not possible to assign a TIMESTAMP column a value of NULL to set it to the current timestamp. To assign the current timestamp, set the column to CURRENT\_TIMESTAMP or a synonym such as NOW().
- TIMESTAMP columns not explicitly declared with the NOT NULL attribute are automatically declared with the NULL attribute and permit NULL values. Assigning such a column a value of NULL sets it to NULL, not the current timestamp.
- TIMESTAMP columns declared with the NOT NULL attribute do not permit NULL values. For inserts that specify NULL for such a column, the result is either an error for a single-row insert if strict SQL mode is enabled, or '0000-00-00 00:00:00' is inserted for multiple-row inserts with strict

SQL mode disabled. In no case does assigning the column a value of NULL set it to the current timestamp.

- TIMESTAMP columns explicitly declared with the NOT NULL attribute and without an explicit DEFAULT attribute are treated as having no default value. For inserted rows that specify no explicit value for such a column, the result depends on the SQL mode. If strict SQL mode is enabled, an error occurs. If strict SQL mode is not enabled, the column is declared with the implicit default of '0000-00-00 00:00:00' and a warning occurs. This is similar to how MySQL treats other temporal types such as DATETIME.
- No TIMESTAMP column is automatically declared with the DEFAULT CURRENT\_TIMESTAMP or ON UPDATE CURRENT\_TIMESTAMP attributes. Those attributes must be explicitly specified.
- The first TIMESTAMP column in a table is not handled differently from TIMESTAMP columns following the first one.

If [explicit\\_defaults\\_for\\_timestamp](#page-121-1) is disabled at server startup, this warning appears in the error log:

```
[Warning] TIMESTAMP with implicit DEFAULT value is deprecated.
Please use --explicit_defaults_for_timestamp server option (see
documentation for more details).
```

As indicated by the warning, to disable the deprecated nonstandard behaviors, enable the [explicit\\_defaults\\_for\\_timestamp](#page-121-1) system variable at server startup.

![](_page_123_Picture_8.jpeg)

### **Note**

[explicit\\_defaults\\_for\\_timestamp](#page-121-1) is itself deprecated because its only purpose is to permit control over deprecated TIMESTAMP behaviors that are to be removed in a future MySQL release. When removal of those behaviors occurs, expect [explicit\\_defaults\\_for\\_timestamp](#page-121-1) to be removed as well.

For additional information, see Section 13.2.5, "Automatic Initialization and Updating for TIMESTAMP and DATETIME".

<span id="page-123-0"></span>• [external\\_user](#page-123-0)

| System Variable      | external_user |
|----------------------|---------------|
| Scope                | Session       |
| Dynamic              | No            |
| SET_VAR Hint Applies | No            |
| Type                 | String        |

The external user name used during the authentication process, as set by the plugin used to authenticate the client. With native (built-in) MySQL authentication, or if the plugin does not set the value, this variable is NULL. See Section 8.2.19, "Proxy Users".

<span id="page-123-1"></span>• [flush](#page-123-1)

| Command-Line Format  | flush[={OFF ON}] |
|----------------------|------------------|
| System Variable      | flush            |
| Scope                | Global           |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Type                 | Boolean          |

| Default Value | OFF |  |
|---------------|-----|--|
|---------------|-----|--|

Applies to MyISAM, only.

If ON, the server flushes (synchronizes) all changes to disk after each SQL statement. Normally, MySQL does a write of all changes to disk only after each SQL statement and lets the operating system handle the synchronizing to disk. See Section B.3.3.3, "What to Do If MySQL Keeps Crashing". This variable is set to ON if you start mysqld with the [--flush](#page-60-1) option.

![](_page_124_Picture_4.jpeg)

## **Note**

If [flush](#page-123-1) is enabled, the value of [flush\\_time](#page-124-0) does not matter and changes to [flush\\_time](#page-124-0) have no effect on flush behavior.

<span id="page-124-0"></span>• [flush\\_time](#page-124-0)

| Command-Line Format  | flush-time=# |
|----------------------|--------------|
| System Variable      | flush_time   |
| Scope                | Global       |
| Dynamic              | Yes          |
| SET_VAR Hint Applies | No           |
| Type                 | Integer      |
| Default Value        | 0            |
| Minimum Value        | 0            |
| Maximum Value        | 31536000     |
| Unit                 | seconds      |

If this is set to a nonzero value, all tables are closed every [flush\\_time](#page-124-0) seconds to free up resources and synchronize unflushed data to disk. This option is best used only on systems with minimal resources.

![](_page_124_Picture_10.jpeg)

## **Note**

If [flush](#page-123-1) is enabled, the value of [flush\\_time](#page-124-0) does not matter and changes to [flush\\_time](#page-124-0) have no effect on flush behavior.

<span id="page-124-1"></span>• [foreign\\_key\\_checks](#page-124-1)

| System Variable      | foreign_key_checks |
|----------------------|--------------------|
| Scope                | Global, Session    |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | Yes                |
| Type                 | Boolean            |
| Default Value        | ON                 |

If set to 1 (the default), foreign key constraints are checked. If set to 0, foreign key constraints are ignored, with a couple of exceptions. When re-creating a table that was dropped, an error is returned if the table definition does not conform to the foreign key constraints referencing the table. Likewise, an ALTER TABLE operation returns an error if a foreign key definition is incorrectly formed. For more information, see Section 15.1.20.5, "FOREIGN KEY Constraints".

Setting this variable has the same effect on NDB tables as it does for InnoDB tables. Typically you leave this setting enabled during normal operation, to enforce referential integrity. Disabling foreign key checking can be useful for reloading InnoDB tables in an order different from that required by their parent/child relationships. See Section 15.1.20.5, "FOREIGN KEY Constraints".

Setting foreign\_key\_checks to 0 also affects data definition statements: DROP SCHEMA drops a schema even if it contains tables that have foreign keys that are referred to by tables outside the schema, and DROP TABLE drops tables that have foreign keys that are referred to by other tables.

![](_page_125_Picture_3.jpeg)

#### **Note**

Setting foreign\_key\_checks to 1 does not trigger a scan of the existing table data. Therefore, rows added to the table while [foreign\\_key\\_checks](#page-124-1) [= 0](#page-124-1) are not verified for consistency.

Dropping an index required by a foreign key constraint is not permitted, even with [foreign\\_key\\_checks=0](#page-124-1). The foreign key constraint must be removed before dropping the index.

<span id="page-125-0"></span>• [ft\\_boolean\\_syntax](#page-125-0)

| Command-Line Format  | ft-boolean-syntax=name |
|----------------------|------------------------|
| System Variable      | ft_boolean_syntax      |
| Scope                | Global                 |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | String                 |
| Default Value        | + -><()~*:""&          |

The list of operators supported by boolean full-text searches performed using IN BOOLEAN MODE. See Section 14.9.2, "Boolean Full-Text Searches".

The default variable value is '+ -><()~\*:""&|'. The rules for changing the value are as follows:

- Operator function is determined by position within the string.
- The replacement value must be 14 characters.
- Each character must be an ASCII nonalphanumeric character.
- Either the first or second character must be a space.
- No duplicates are permitted except the phrase quoting operators in positions 11 and 12. These two characters are not required to be the same, but they are the only two that may be.
- Positions 10, 13, and 14 (which by default are set to :, &, and |) are reserved for future extensions.
- <span id="page-125-1"></span>• [ft\\_max\\_word\\_len](#page-125-1)

| Command-Line Format  | ft-max-word-len=# |
|----------------------|-------------------|
| System Variable      | ft_max_word_len   |
| Scope                | Global            |
| Dynamic              | No                |
| SET_VAR Hint Applies | No                |
| Type                 | Integer           |
| Default Value        | 84                |

| Minimum Value | 10 |
|---------------|----|
| Maximum Value | 84 |

The maximum length of the word to be included in a MyISAM FULLTEXT index.

![](_page_126_Picture_3.jpeg)

#### **Note**

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable. Use REPAIR TABLE tbl\_name QUICK.

## <span id="page-126-0"></span>• [ft\\_min\\_word\\_len](#page-126-0)

| Command-Line Format  | ft-min-word-len=# |
|----------------------|-------------------|
| System Variable      | ft_min_word_len   |
| Scope                | Global            |
| Dynamic              | No                |
| SET_VAR Hint Applies | No                |
| Type                 | Integer           |
| Default Value        | 4                 |
| Minimum Value        | 1                 |
| Maximum Value        | 82                |

The minimum length of the word to be included in a MyISAM FULLTEXT index.

![](_page_126_Picture_9.jpeg)

#### **Note**

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable. Use REPAIR TABLE tbl\_name QUICK.

## <span id="page-126-1"></span>• [ft\\_query\\_expansion\\_limit](#page-126-1)

| Command-Line Format  | ft-query-expansion-limit=# |
|----------------------|----------------------------|
| System Variable      | ft_query_expansion_limit   |
| Scope                | Global                     |
| Dynamic              | No                         |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 20                         |
| Minimum Value        | 0                          |
| Maximum Value        | 1000                       |

The number of top matches to use for full-text searches performed using WITH QUERY EXPANSION.

## <span id="page-126-2"></span>• [ft\\_stopword\\_file](#page-126-2)

| Command-Line Format  | ft-stopword-file=file_name |
|----------------------|----------------------------|
| System Variable      | ft_stopword_file           |
| Scope                | Global                     |
| Dynamic              | No                         |
| SET_VAR Hint Applies | No                         |
| Type                 | File name                  |

The file from which to read the list of stopwords for full-text searches on MyISAM tables. The server looks for the file in the data directory unless an absolute path name is given to specify a different directory. All the words from the file are used; comments are not honored. By default, a built-in list of stopwords is used (as defined in the storage/myisam/ft\_static.c file). Setting this variable to the empty string ('') disables stopword filtering. See also Section 14.9.4, "Full-Text Stopwords".

![](_page_127_Picture_2.jpeg)

#### **Note**

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable or the contents of the stopword file. Use REPAIR TABLE tbl\_name QUICK.

<span id="page-127-0"></span>• [general\\_log](#page-127-0)

| Command-Line Format  | general-log[={OFF ON}] |
|----------------------|------------------------|
| System Variable      | general_log            |
| Scope                | Global                 |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | Boolean                |
| Default Value        | OFF                    |

Whether the general query log is enabled. The value can be 0 (or OFF) to disable the log or 1 (or ON) to enable the log. The destination for log output is controlled by the [log\\_output](#page-145-0) system variable; if that value is NONE, no log entries are written even if the log is enabled.

<span id="page-127-1"></span>• [general\\_log\\_file](#page-127-1)

| Command-Line Format  | general-log-file=file_name |
|----------------------|----------------------------|
| System Variable      | general_log_file           |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | File name                  |
| Default Value        | host_name.log              |

The name of the general query log file. The default value is host\_name.log, but the initial value can be changed with the [--general\\_log\\_file](#page-127-1) option.

<span id="page-127-2"></span>• [generated\\_random\\_password\\_length](#page-127-2)

| Command-Line Format  | generated-random-password-length=# |
|----------------------|------------------------------------|
| System Variable      | generated_random_password_length   |
| Scope                | Global, Session                    |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Integer                            |
| Default Value        | 20                                 |
| Minimum Value        | 5                                  |

| Maximum Value<br>255 |  |
|----------------------|--|
|----------------------|--|

The maximum number of characters permitted in random passwords generated for CREATE USER, ALTER USER, and SET PASSWORD statements. For more information, see Random Password Generation.

<span id="page-128-0"></span>• [global\\_connection\\_memory\\_limit](#page-128-0)

| Command-Line Format  | global-connection-memory-limit=# |
|----------------------|----------------------------------|
| System Variable      | global_connection_memory_limit   |
| Scope                | Global                           |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Integer                          |
| Default Value        | 18446744073709551615             |
| Minimum Value        | 16777216                         |
| Maximum Value        | 18446744073709551615             |
| Unit                 | bytes                            |

Set the total amount of memory that can be used by all user connections; that is, Global\_connection\_memory should not exceed this amount. Any time that it does, all queries (including any currently running) from regular users are rejected with [ER\\_GLOBAL\\_CONN\\_LIMIT](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_global_conn_limit).

Memory used by the system users such as the MySQL root user is included in this total, but is not counted towards the disconnection limit; such users are never disconnected due to memory usage.

Memory used by the InnoDB buffer pool is excluded from the total.

You must have the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege to set this variable.

<span id="page-128-1"></span>• [global\\_connection\\_memory\\_tracking](#page-128-1)

| Command-Line Format  | global-connection-memory<br>tracking={TRUE FALSE} |
|----------------------|---------------------------------------------------|
| System Variable      | global_connection_memory_tracking                 |
| Scope                | Global, Session                                   |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | Boolean                                           |
| Default Value        | FALSE                                             |

Determines whether the server calculates Global\_connection\_memory. This variable must be enabled explicitly; otherwise, the memory calculation is not performed, and Global\_connection\_memory is not set.

You must have the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege to set this variable.

<span id="page-128-2"></span>• [group\\_concat\\_max\\_len](#page-128-2)

| Command-Line Format | group-concat-max-len=# |
|---------------------|------------------------|
| System Variable     | group_concat_max_len   |
| Scope               | 899<br>Global, Session |

| Dynamic                          | Yes                  |
|----------------------------------|----------------------|
| SET_VAR Hint Applies             | Yes                  |
| Type                             | Integer              |
| Default Value                    | 1024                 |
| Minimum Value                    | 4                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

The maximum permitted result length in bytes for the GROUP\_CONCAT() function. The default is 1024.

![](_page_129_Picture_3.jpeg)

#### **Important**

When setting the value for [group\\_concat\\_max\\_len](#page-128-2), consider the following:

- Estimate the maximum length required for GROUP\_CONCAT() output and set the value accordingly.
- Setting the value excessively high can negatively affect performance and lead to out-of-memory (OOM) errors.
- In MySQL HeatWave, the maximum column length is 4 MB, so setting a value higher than this causes the output to be truncated. To avoid this, set a value under 4 MB.
- <span id="page-129-0"></span>• [have\\_compress](#page-129-0)

YES if the zlib compression library is available to the server, NO if not. If not, the COMPRESS() and UNCOMPRESS() functions cannot be used.

<span id="page-129-1"></span>• [have\\_dynamic\\_loading](#page-129-1)

YES if mysqld supports dynamic loading of plugins, NO if not. If the value is NO, you cannot use options such as --plugin-load to load plugins at server startup, or the INSTALL PLUGIN statement to load plugins at runtime.

<span id="page-129-2"></span>• [have\\_geometry](#page-129-2)

YES if the server supports spatial data types, NO if not.

<span id="page-129-3"></span>• [have\\_openssl](#page-129-3)

This variable is a synonym for [have\\_ssl](#page-130-2).

As of MySQL 8.0.26, [have\\_openssl](#page-129-3) is deprecated and subject to removal in a future MySQL version. For information about TLS properties of MySQL connection interfaces, use the tls\_channel\_status table.

<span id="page-129-4"></span>• [have\\_profiling](#page-129-4)

YES if statement profiling capability is present, NO if not. If present, the profiling system variable controls whether this capability is enabled or disabled. See Section 15.7.7.31, "SHOW PROFILES Statement".

This variable is deprecated and you should expect it to be removed in a future MySQL release.

<span id="page-130-0"></span>• [have\\_query\\_cache](#page-130-0)

The query cache was removed in MySQL 8.0.3. [have\\_query\\_cache](#page-130-0) is deprecated, always has a value of NO, and you should expect it to be removed in a future MySQL release.

<span id="page-130-1"></span>• [have\\_rtree\\_keys](#page-130-1)

YES if RTREE indexes are available, NO if not. (These are used for spatial indexes in MyISAM tables.)

<span id="page-130-2"></span>• [have\\_ssl](#page-130-2)

| Deprecated           | Yes                                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------------------------|
| System Variable      | have_ssl                                                                                                              |
| Scope                | Global                                                                                                                |
| Dynamic              | No                                                                                                                    |
| SET_VAR Hint Applies | No                                                                                                                    |
| Type                 | String                                                                                                                |
| Valid Values         | YES (SSL support available)                                                                                           |
|                      | DISABLED (SSL support was compiled into<br>server, but server was not started with necessary<br>options to enable it) |

YES if mysqld supports SSL connections, DISABLED if the server was compiled with SSL support, but was not started with the appropriate connection-encryption options. For more information, see Section 2.8.6, "Configuring SSL Library Support".

As of MySQL 8.0.26, [have\\_ssl](#page-130-2) is deprecated and subject to removal in a future MySQL version. For information about TLS properties of MySQL connection interfaces, use the tls\_channel\_status table.

<span id="page-130-3"></span>• [have\\_statement\\_timeout](#page-130-3)

| System Variable      | have_statement_timeout |
|----------------------|------------------------|
| Scope                | Global                 |
| Dynamic              | No                     |
| SET_VAR Hint Applies | No                     |
| Type                 | Boolean                |

Whether the statement execution timeout feature is available (see Statement Execution Time Optimizer Hints). The value can be NO if the background thread used by this feature could not be initialized.

<span id="page-130-4"></span>• [have\\_symlink](#page-130-4)

YES if symbolic link support is enabled, NO if not. This is required on Unix for support of the DATA DIRECTORY and INDEX DIRECTORY table options. If the server is started with the [--skip](#page-75-2)[symbolic-links](#page-75-2) option, the value is DISABLED.

This variable has no meaning on Windows.

![](_page_130_Picture_15.jpeg)

#### **Note**

Symbolic link support, along with the [--symbolic-links](#page-75-2) option that controls it, is deprecated; expect these to be removed in a future version of MySQL. In addition, the option is disabled by default. The related 901 [have\\_symlink](#page-130-4) system variable also is deprecated and you should expect it to be removed in a future version of MySQL.

<span id="page-131-0"></span>• [histogram\\_generation\\_max\\_mem\\_size](#page-131-0)

| Command-Line Format              | histogram-generation-max-mem<br>size=# |
|----------------------------------|----------------------------------------|
| System Variable                  | histogram_generation_max_mem_size      |
| Scope                            | Global, Session                        |
| Dynamic                          | Yes                                    |
| SET_VAR Hint Applies             | No                                     |
| Type                             | Integer                                |
| Default Value                    | 20000000                               |
| Minimum Value                    | 1000000                                |
| Maximum Value (64-bit platforms) | 18446744073709551615                   |
| Maximum Value (32-bit platforms) | 4294967295                             |
| Unit                             | bytes                                  |

The maximum amount of memory available for generating histogram statistics. See Section 10.9.6, "Optimizer Statistics", and Section 15.7.3.1, "ANALYZE TABLE Statement".

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-131-1"></span>• [host\\_cache\\_size](#page-131-1)

| Command-Line Format  | host-cache-size=#                                              |
|----------------------|----------------------------------------------------------------|
| System Variable      | host_cache_size                                                |
| Scope                | Global                                                         |
| Dynamic              | Yes                                                            |
| SET_VAR Hint Applies | No                                                             |
| Type                 | Integer                                                        |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value        | 0                                                              |
| Maximum Value        | 65536                                                          |

The MySQL server maintains an in-memory host cache that contains client host name and IP address information and is used to avoid Domain Name System (DNS) lookups; see Section 7.1.12.3, "DNS Lookups and the Host Cache".

The [host\\_cache\\_size](#page-131-1) variable controls the size of the host cache, as well as the size of the Performance Schema host\_cache table that exposes the cache contents. Setting [host\\_cache\\_size](#page-131-1) has these effects:

• Setting the size to 0 disables the host cache. With the cache disabled, the server performs a DNS lookup every time a client connects.

• Changing the size at runtime causes an implicit host cache flushing operation that clears the host cache, truncates the host\_cache table, and unblocks any blocked hosts.

The default value is autosized to 128, plus 1 for a value of [max\\_connections](#page-152-1) up to 500, plus 1 for every increment of 20 over 500 in the [max\\_connections](#page-152-1) value, capped to a limit of 2000.

Using the [--skip-host-cache](#page-71-0) option is similar to setting the host\_cache\_size system variable to 0, but host\_cache\_size is more flexible because it can also be used to resize, enable, and disable the host cache at runtime, not just at server startup.

Starting the server with [--skip-host-cache](#page-71-0) does not prevent runtime changes to the value of host\_cache\_size, but such changes have no effect and the cache is not re-enabled even if host\_cache\_size is set larger than 0.

Setting the host\_cache\_size system variable rather than the [--skip-host-cache](#page-71-0) option is preferred for the reasons given in the previous paragraph. In addition, the --skip-host-cache option is deprecated and its removal is expected in a future version of MySQL; in MySQL 8.0.29 and later, using the option raises a warning.

## <span id="page-132-0"></span>• [hostname](#page-132-0)

| System Variable      | hostname |
|----------------------|----------|
| Scope                | Global   |
| Dynamic              | No       |
| SET_VAR Hint Applies | No       |
| Type                 | String   |

The server sets this variable to the server host name at startup. The maximum length is 255 characters as of MySQL 8.0.17, per RFC 1034, and 60 characters before that.

## <span id="page-132-1"></span>• [identity](#page-132-1)

This variable is a synonym for the [last\\_insert\\_id](#page-141-0) variable. It exists for compatibility with other database systems. You can read its value with SELECT @@identity, and set it using SET identity.

## <span id="page-132-2"></span>• [init\\_connect](#page-132-2)

| Command-Line Format  | init-connect=name |
|----------------------|-------------------|
| System Variable      | init_connect      |
| Scope                | Global            |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | String            |

A string to be executed by the server for each client that connects. The string consists of one or more SQL statements, separated by semicolon characters.

For users that have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege), the content of [init\\_connect](#page-132-2) is not executed. This is done so that an erroneous value for [init\\_connect](#page-132-2) does not prevent all clients from connecting. For example, the value might contain a statement that has a syntax error, thus causing client connections to fail. Not executing [init\\_connect](#page-132-2) for users that have the CONNECTION\_ADMIN or SUPER privilege enables them to open a connection and fix the [init\\_connect](#page-132-2) value.

[init\\_connect](#page-132-2) execution is skipped for any client user with an expired password. This is done because such a user cannot execute arbitrary statements, and thus [init\\_connect](#page-132-2) execution fails, leaving the client unable to connect. Skipping [init\\_connect](#page-132-2) execution enables the user to connect and change password.

The server discards any result sets produced by statements in the value of [init\\_connect](#page-132-2).

<span id="page-133-0"></span>• [information\\_schema\\_stats\\_expiry](#page-133-0)

| Command-Line Format  | information-schema-stats-expiry=# |
|----------------------|-----------------------------------|
| System Variable      | information_schema_stats_expiry   |
| Scope                | Global, Session                   |
| Dynamic              | Yes                               |
| SET_VAR Hint Applies | No                                |
| Type                 | Integer                           |
| Default Value        | 86400                             |
| Minimum Value        | 0                                 |
| Maximum Value        | 31536000                          |
| Unit                 | seconds                           |

Some INFORMATION\_SCHEMA tables contain columns that provide table statistics:

```
STATISTICS.CARDINALITY
TABLES.AUTO_INCREMENT
TABLES.AVG_ROW_LENGTH
TABLES.CHECKSUM
TABLES.CHECK_TIME
TABLES.CREATE_TIME
TABLES.DATA_FREE
TABLES.DATA_LENGTH
TABLES.INDEX_LENGTH
TABLES.MAX_DATA_LENGTH
TABLES.TABLE_ROWS
TABLES.UPDATE_TIME
```

Those columns represent dynamic table metadata; that is, information that changes as table contents change.

By default, MySQL retrieves cached values for those columns from the mysql.index\_stats and mysql.table\_stats dictionary tables when the columns are queried, which is more efficient than retrieving statistics directly from the storage engine. If cached statistics are not available or have expired, MySQL retrieves the latest statistics from the storage engine and caches them in the mysql.index\_stats and mysql.table\_stats dictionary tables. Subsequent queries retrieve the cached statistics until the cached statistics expire. A server restart or the first opening

of the mysql.index\_stats and mysql.table\_stats tables do not update cached statistics automatically.

The [information\\_schema\\_stats\\_expiry](#page-133-0) session variable defines the period of time before cached statistics expire. The default is 86400 seconds (24 hours), but the time period can be extended to as much as one year.

To update cached values at any time for a given table, use ANALYZE TABLE.

To always retrieve the latest statistics directly from the storage engine and bypass cached values, set [information\\_schema\\_stats\\_expiry](#page-133-0) to 0.

Querying statistics columns does not store or update statistics in the mysql.index\_stats and mysql.table\_stats dictionary tables under these circumstances:

- When cached statistics have not expired.
- When [information\\_schema\\_stats\\_expiry](#page-133-0) is set to 0.
- When the server is in [read\\_only](#page-186-1), super\_read\_only, transaction\_read\_only, or innodb\_read\_only mode.
- When the query also fetches Performance Schema data.

The statistics cache may be updated during a multiple-statement transaction before it is known whether the transaction commits. As a result, the cache may contain information that does not correspond to a known committed state. This can occur with [autocommit=0](#page-91-0) or after START TRANSACTION.

[information\\_schema\\_stats\\_expiry](#page-133-0) is a session variable, and each client session can define its own expiration value. Statistics that are retrieved from the storage engine and cached by one session are available to other sessions.

For related information, see Section 10.2.3, "Optimizing INFORMATION\_SCHEMA Queries".

<span id="page-134-0"></span>• [init\\_file](#page-134-0)

| Command-Line Format  | init-file=file_name |
|----------------------|---------------------|
| System Variable      | init_file           |
| Scope                | Global              |
| Dynamic              | No                  |
| SET_VAR Hint Applies | No                  |
| Type                 | File name           |

If specified, this variable names a file containing SQL statements to be read and executed during the startup process. Prior to MySQL 8.0.18, each statement must be on a single line and should not include comments. As of MySQL 8.0.18, the acceptable format for statements in the file is expanded to support these constructs:

- delimiter ;, to set the statement delimiter to the ; character.
- delimiter \$\$, to set the statement delimiter to the \$\$ character sequence.
- Multiple statements on the same line, delimited by the current delimiter.
- Multiple-line statements.
- Comments from a # character to the end of the line.

- Comments from a -- sequence to the end of the line.
- C-style comments from a /\* sequence to the following \*/ sequence, including over multiple lines.
- Multiple-line string literals enclosed within either single quote (') or double quote (") characters.

If the server is started with the [--initialize](#page-60-0) or [--initialize-insecure](#page-61-0) option, it operates in bootstrap mode and some functionality is unavailable that limits the statements permitted in the file. These include statements that relate to account management (such as CREATE USER or GRANT), replication, and global transaction identifiers. See Section 19.1.3, "Replication with Global Transaction Identifiers".

As of MySQL 8.0.17, threads created during server startup are used for tasks such as creating the data dictionary, running upgrade procedures, and creating system tables. To ensure a stable and predictable environment, these threads are executed with the server built-in defaults for some system variables, such as sql\_mode, [character\\_set\\_server](#page-101-1), [collation\\_server](#page-103-1), [completion\\_type](#page-103-2), [explicit\\_defaults\\_for\\_timestamp](#page-121-1), and [default\\_table\\_encryption](#page-112-1).

These threads are also used to execute the statements in any file specified with [init\\_file](#page-134-0) when starting the server, so such statements execute with the server's built-in default values for those system variables.

• innodb\_xxx

InnoDB system variables are listed in Section 17.14, "InnoDB Startup Options and System Variables". These variables control many aspects of storage, memory use, and I/O patterns for InnoDB tables, and are especially important now that InnoDB is the default storage engine.

<span id="page-135-0"></span>• [insert\\_id](#page-135-0)

The value to be used by the following INSERT or ALTER TABLE statement when inserting an AUTO\_INCREMENT value. This is mainly used with the binary log.

<span id="page-135-1"></span>• [interactive\\_timeout](#page-135-1)

| Command-Line Format  | interactive-timeout=# |
|----------------------|-----------------------|
| System Variable      | interactive_timeout   |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Integer               |
| Default Value        | 28800                 |
| Minimum Value        | 1                     |
| Maximum Value        | 31536000              |
| Unit                 | seconds               |

The number of seconds the server waits for activity on an interactive connection before closing it. An interactive client is defined as a client that uses the CLIENT\_INTERACTIVE option to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md). See also wait\_timeout.

<span id="page-136-2"></span>• [internal\\_tmp\\_disk\\_storage\\_engine](#page-136-2)

![](_page_136_Picture_2.jpeg)

#### **Important**

In MySQL 8.0.16 and later, on-disk internal temporary tables always use the InnoDB storage engine; as of MySQL 8.0.16, this variable has been removed and is thus no longer supported.

Prior to MySQL 8.0.16, this variable determines the storage engine used for on-disk internal temporary tables (see Storage Engine for On-Disk Internal Temporary Tables). Permitted values are MYISAM and INNODB (the default).

<span id="page-136-0"></span>• [internal\\_tmp\\_mem\\_storage\\_engine](#page-136-0)

| Command-Line Format  | internal-tmp-mem-storage-engine=# |
|----------------------|-----------------------------------|
| System Variable      | internal_tmp_mem_storage_engine   |
| Scope                | Global, Session                   |
| Dynamic              | Yes                               |
| SET_VAR Hint Applies | Yes                               |
| Type                 | Enumeration                       |
| Default Value        | TempTable                         |
| Valid Values         | MEMORY                            |
|                      | TempTable                         |

The storage engine for in-memory internal temporary tables (see Section 10.4.4, "Internal Temporary Table Use in MySQL"). Permitted values are TempTable (the default) and MEMORY.

The optimizer uses the storage engine defined by [internal\\_tmp\\_mem\\_storage\\_engine](#page-136-0) for inmemory internal temporary tables.

From MySQL 8.0.27, configuring a session setting for [internal\\_tmp\\_mem\\_storage\\_engine](#page-136-0) requires the SESSION\_VARIABLES\_ADMIN or SYSTEM\_VARIABLES\_ADMIN privilege.

<span id="page-136-1"></span>• [join\\_buffer\\_size](#page-136-1)

| Command-Line Format                     | join-buffer-size=#   |
|-----------------------------------------|----------------------|
| System Variable                         | join_buffer_size     |
| Scope                                   | Global, Session      |
| Dynamic                                 | Yes                  |
| SET_VAR Hint Applies                    | Yes                  |
| Type                                    | Integer              |
| Default Value                           | 262144               |
| Minimum Value                           | 128                  |
| Maximum Value (Windows)                 | 4294967168           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551488 |
| Maximum Value (Other, 32-bit platforms) | 4294967168           |
| Unit                                    | bytes                |
| Block Size                              | 128                  |

The minimum size of the buffer that is used for plain index scans, range index scans, and joins that do not use indexes and thus perform full table scans. In MySQL 8.0.18 and later, this variable also907 controls the amount of memory used for hash joins. Normally, the best way to get fast joins is to add indexes. Increase the value of join\_buffer\_size to get a faster full join when adding indexes is not possible. One join buffer is allocated for each full join between two tables. For a complex join between several tables for which indexes are not used, multiple join buffers might be necessary.

The default is 256KB. The maximum permissible setting for <code>join\_buffer\_size</code> is 4GB-1. Larger values are permitted for 64-bit platforms (except 64-bit Windows, for which large values are truncated to 4GB-1 with a warning). The block size is 128, and a value that is not an exact multiple of the block size is rounded down to the next lower multiple of the block size by MySQL Server before storing the value for the system variable. The parser allows values up to the maximum unsigned integer value for the platform (4294967295 or 2<sup>32</sup>-1 for a 32-bit system, 18446744073709551615 or 2<sup>64</sup>-1 for a 64-bit system) but the actual maximum is a block size lower.

Unless a Block Nested-Loop or Batched Key Access algorithm is used, there is no gain from setting the buffer larger than required to hold each matching row, and all joins allocate at least the minimum size, so use caution in setting this variable to a large value globally. It is better to keep the global setting small and change the session setting to a larger value only in sessions that are doing large joins, or change the setting on a per-query basis by using a SET\_VAR optimizer hint (see Section 10.9.3, "Optimizer Hints"). Memory allocation time can cause substantial performance drops if the global size is larger than needed by most queries that use it.

When Block Nested-Loop is used, a larger join buffer can be beneficial up to the point where all required columns from all rows in the first table are stored in the join buffer. This depends on the query; the optimal size may be smaller than holding all rows from the first tables.

When Batched Key Access is used, the value of <code>join\_buffer\_size</code> defines how large the batch of keys is in each request to the storage engine. The larger the buffer, the more sequential access is made to the right hand table of a join operation, which can significantly improve performance.

For additional information about join buffering, see Section 10.2.1.7, "Nested-Loop Join Algorithms". For information about Batched Key Access, see Section 10.2.1.12, "Block Nested-Loop and Batched Key Access Joins". For information about hash joins, see Section 10.2.1.4, "Hash Join Optimization".

<span id="page-137-0"></span>keep\_files\_on\_create

| Command-Line Format  | keep-files-on-create[={OFF ON}] |
|----------------------|---------------------------------|
| System Variable      | keep_files_on_create            |
| Scope                | Global, Session                 |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Туре                 | Boolean                         |
| Default Value        | OFF                             |

If a MyISAM table is created with no DATA DIRECTORY option, the .MYD file is created in the database directory. By default, if MyISAM finds an existing .MYD file in this case, it overwrites it. The same applies to .MYI files for tables created with no INDEX DIRECTORY option. To suppress this behavior, set the keep\_files\_on\_create variable to ON (1), in which case MyISAM does not overwrite existing files and returns an error instead. The default value is OFF (0).

If a MyISAM table is created with a DATA DIRECTORY or INDEX DIRECTORY option and an existing .MYD or .MYI file is found, MyISAM always returns an error. It does not overwrite a file in the specified directory.

<span id="page-137-1"></span>• key buffer size

| Command-Line Format | key-buffer-size=# |
|---------------------|-------------------|
|                     | <u> -</u>         |

| System Variable                  | key_buffer_size      |
|----------------------------------|----------------------|
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value                    | 8388608              |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | OS_PER_PROCESS_LIMIT |
| Maximum Value (32-bit platforms) | 4294967295           |
| Unit                             | bytes                |

Index blocks for MyISAM tables are buffered and are shared by all threads. [key\\_buffer\\_size](#page-137-1) is the size of the buffer used for index blocks. The key buffer is also known as the key cache.

The minimum permissible setting is 0, but you cannot set [key\\_buffer\\_size](#page-137-1) to 0 dynamically. A setting of 0 drops the key cache, which is not permitted at runtime. Setting [key\\_buffer\\_size](#page-137-1) to 0 is permitted only at startup, in which case the key cache is not initialized. Changing the [key\\_buffer\\_size](#page-137-1) setting at runtime from a value of 0 to a permitted non-zero value initializes the key cache.

[key\\_buffer\\_size](#page-137-1) can be increased or decreased only in increments or multiples of 4096 bytes. Increasing or decreasing the setting by a nonconforming value produces a warning and truncates the setting to a conforming value.

The maximum permissible setting for [key\\_buffer\\_size](#page-137-1) is 4GB−1 on 32-bit platforms. Larger values are permitted for 64-bit platforms. The effective maximum size might be less, depending on your available physical RAM and per-process RAM limits imposed by your operating system or hardware platform. The value of this variable indicates the amount of memory requested. Internally, the server allocates as much memory as possible up to this amount, but the actual allocation might be less.

You can increase the value to get better index handling for all reads and multiple writes; on a system whose primary function is to run MySQL using the MyISAM storage engine, 25% of the machine's total memory is an acceptable value for this variable. However, you should be aware that, if you make the value too large (for example, more than 50% of the machine's total memory), your system might start to page and become extremely slow. This is because MySQL relies on the operating system to perform file system caching for data reads, so you must leave some room for the file system cache. You should also consider the memory requirements of any other storage engines that you may be using in addition to MyISAM.

For even more speed when writing many rows at the same time, use LOCK TABLES. See Section 10.2.5.1, "Optimizing INSERT Statements".

You can check the performance of the key buffer by issuing a SHOW STATUS statement and examining the Key\_read\_requests, Key\_reads, Key\_write\_requests, and Key\_writes status variables. (See Section 15.7.7, "SHOW Statements".) The Key\_reads/ Key\_read\_requests ratio should normally be less than 0.01. The Key\_writes/ Key\_write\_requests ratio is usually near 1 if you are using mostly updates and deletes, but might be much smaller if you tend to do updates that affect many rows at the same time or if you are using the DELAY\_KEY\_WRITE table option.

The fraction of the key buffer in use can be determined using [key\\_buffer\\_size](#page-137-1) in conjunction with the Key\_blocks\_unused status variable and the buffer block size, which is available from the [key\\_cache\\_block\\_size](#page-139-1) system variable:

```
1 - ((Key_blocks_unused * key_cache_block_size) / key_buffer_size)
```

This value is an approximation because some space in the key buffer is allocated internally for administrative structures. Factors that influence the amount of overhead for these structures include block size and pointer size. As block size increases, the percentage of the key buffer lost to overhead tends to decrease. Larger blocks results in a smaller number of read operations (because more keys are obtained per read), but conversely an increase in reads of keys that are not examined (if not all keys in a block are relevant to a query).

It is possible to create multiple MyISAM key caches. The size limit of 4GB applies to each cache individually, not as a group. See Section 10.10.2, "The MyISAM Key Cache".

<span id="page-139-0"></span>• [key\\_cache\\_age\\_threshold](#page-139-0)

| Command-Line Format              | key-cache-age-threshold=# |
|----------------------------------|---------------------------|
| System Variable                  | key_cache_age_threshold   |
| Scope                            | Global                    |
| Dynamic                          | Yes                       |
| SET_VAR Hint Applies             | No                        |
| Type                             | Integer                   |
| Default Value                    | 300                       |
| Minimum Value                    | 100                       |
| Maximum Value (64-bit platforms) | 18446744073709551516      |
| Maximum Value (32-bit platforms) | 4294967196                |
| Block Size                       | 100                       |

This value controls the demotion of buffers from the hot sublist of a key cache to the warm sublist. Lower values cause demotion to happen more quickly. The minimum value is 100. The default value is 300. See Section 10.10.2, "The MyISAM Key Cache".

<span id="page-139-1"></span>• [key\\_cache\\_block\\_size](#page-139-1)

| Command-Line Format  | key-cache-block-size=# |
|----------------------|------------------------|
| System Variable      | key_cache_block_size   |
| Scope                | Global                 |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | Integer                |
| Default Value        | 1024                   |
| Minimum Value        | 512                    |
| Maximum Value        | 16384                  |
| Unit                 | bytes                  |

The size in bytes of blocks in the key cache. The default value is 1024. See Section 10.10.2, "The MyISAM Key Cache".

<span id="page-140-0"></span>• [key\\_cache\\_division\\_limit](#page-140-0)

| Command-Line Format  | key-cache-division-limit=# |
|----------------------|----------------------------|
| System Variable      | key_cache_division_limit   |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 100                        |
| Minimum Value        | 1                          |
| Maximum Value        | 100                        |

The division point between the hot and warm sublists of the key cache buffer list. The value is the percentage of the buffer list to use for the warm sublist. Permissible values range from 1 to 100. The default value is 100. See Section 10.10.2, "The MyISAM Key Cache".

<span id="page-140-1"></span>• [large\\_files\\_support](#page-140-1)

| System Variable      | large_files_support |
|----------------------|---------------------|
| Scope                | Global              |
| Dynamic              | No                  |
| SET_VAR Hint Applies | No                  |
| Type                 | Boolean             |

Whether mysqld was compiled with options for large file support.

<span id="page-140-3"></span>• [large\\_pages](#page-140-3)

| Command-Line Format  | large-pages[={OFF ON}] |
|----------------------|------------------------|
| System Variable      | large_pages            |
| Scope                | Global                 |
| Dynamic              | No                     |
| SET_VAR Hint Applies | No                     |
| Platform Specific    | Linux                  |
| Type                 | Boolean                |
| Default Value        | OFF                    |

Whether large page support is enabled (via the [--large-pages](#page-62-0) option). See Section 10.12.3.3, "Enabling Large Page Support".

<span id="page-140-2"></span>• [large\\_page\\_size](#page-140-2)

| System Variable | large_page_size |
|-----------------|-----------------|
| Scope           | Global          |
| Dynamic         | 911<br>No       |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | Integer |
| Default Value        | 0       |
| Minimum Value        | 0       |
| Maximum Value        | 65535   |
| Unit                 | bytes   |

If large page support is enabled, this shows the size of memory pages. Large memory pages are supported only on Linux; on other platforms, the value of this variable is always 0. See Section 10.12.3.3, "Enabling Large Page Support".

## <span id="page-141-0"></span>• [last\\_insert\\_id](#page-141-0)

The value to be returned from LAST\_INSERT\_ID(). This is stored in the binary log when you use LAST\_INSERT\_ID() in a statement that updates a table. Setting this variable does not update the value returned by the [mysql\\_insert\\_id\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-insert-id.md) C API function.

## <span id="page-141-2"></span>• [lc\\_messages](#page-141-2)

| Command-Line Format  | lc-messages=name |
|----------------------|------------------|
| System Variable      | lc_messages      |
| Scope                | Global, Session  |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Type                 | String           |
| Default Value        | en_US            |

The locale to use for error messages. The default is en\_US. The server converts the argument to a language name and combines it with the value of [lc\\_messages\\_dir](#page-141-3) to produce the location for the error message file. See Section 12.12, "Setting the Error Message Language".

## <span id="page-141-3"></span>• [lc\\_messages\\_dir](#page-141-3)

| Command-Line Format  | lc-messages-dir=dir_name |
|----------------------|--------------------------|
| System Variable      | lc_messages_dir          |
| Scope                | Global                   |
| Dynamic              | No                       |
| SET_VAR Hint Applies | No                       |
| Type                 | Directory name           |

The directory where error messages are located. The server uses the value together with the value of [lc\\_messages](#page-141-2) to produce the location for the error message file. See Section 12.12, "Setting the Error Message Language".

## <span id="page-141-1"></span>• [lc\\_time\\_names](#page-141-1)

| Command-Line Format  | lc-time-names=value |
|----------------------|---------------------|
| System Variable      | lc_time_names       |
| Scope                | Global, Session     |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |

| Type | String |
|------|--------|
|------|--------|

This variable specifies the locale that controls the language used to display day and month names and abbreviations. This variable affects the output from the DATE\_FORMAT(), DAYNAME() and MONTHNAME() functions. Locale names are POSIX-style values such as 'ja\_JP' or 'pt\_BR'. The default value is 'en\_US' regardless of your system's locale setting. For further information, see Section 12.16, "MySQL Server Locale Support".

## <span id="page-142-0"></span>• [license](#page-142-0)

| System Variable      | license |
|----------------------|---------|
| Scope                | Global  |
| Dynamic              | No      |
| SET_VAR Hint Applies | No      |
| Type                 | String  |
| Default Value        | GPL     |

The type of license the server has.

## <span id="page-142-1"></span>• [local\\_infile](#page-142-1)

| Command-Line Format  | local-infile[={OFF ON}] |
|----------------------|-------------------------|
| System Variable      | local_infile            |
| Scope                | Global                  |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | Boolean                 |
| Default Value        | OFF                     |

This variable controls server-side LOCAL capability for LOAD DATA statements. Depending on the [local\\_infile](#page-142-1) setting, the server refuses or permits local data loading by clients that have LOCAL enabled on the client side.

To explicitly cause the server to refuse or permit LOAD DATA LOCAL statements (regardless of how client programs and libraries are configured at build time or runtime), start mysqld with [local\\_infile](#page-142-1) disabled or enabled, respectively. [local\\_infile](#page-142-1) can also be set at runtime. For more information, see Section 8.1.6, "Security Considerations for LOAD DATA LOCAL".

## <span id="page-142-2"></span>• [lock\\_wait\\_timeout](#page-142-2)

| Command-Line Format  | lock-wait-timeout=# |
|----------------------|---------------------|
| System Variable      | lock_wait_timeout   |
| Scope                | Global, Session     |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | Yes                 |
| Type                 | Integer             |
| Default Value        | 31536000            |
| Minimum Value        | 1                   |
| Maximum Value        | 31536000            |

| Unit | seconds |
|------|---------|
|------|---------|

This variable specifies the timeout in seconds for attempts to acquire metadata locks. The permissible values range from 1 to 31536000 (1 year). The default is 31536000.

This timeout applies to all statements that use metadata locks. These include DML and DDL operations on tables, views, stored procedures, and stored functions, as well as LOCK TABLES, FLUSH TABLES WITH READ LOCK, and HANDLER statements.

This timeout does not apply to implicit accesses to system tables in the mysql database, such as grant tables modified by GRANT or REVOKE statements or table logging statements. The timeout does apply to system tables accessed directly, such as with SELECT or UPDATE.

The timeout value applies separately for each metadata lock attempt. A given statement can require more than one lock, so it is possible for the statement to block for longer than the [lock\\_wait\\_timeout](#page-142-2) value before reporting a timeout error. When lock timeout occurs, [ER\\_LOCK\\_WAIT\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_lock_wait_timeout) is reported.

[lock\\_wait\\_timeout](#page-142-2) also defines the amount of time that a LOCK INSTANCE FOR BACKUP statement waits for a lock before giving up.

<span id="page-143-0"></span>• [locked\\_in\\_memory](#page-143-0)

| System Variable      | locked_in_memory |
|----------------------|------------------|
| Scope                | Global           |
| Dynamic              | No               |
| SET_VAR Hint Applies | No               |
| Type                 | Boolean          |
| Default Value        | OFF              |

Whether mysqld was locked in memory with [--memlock](#page-65-1).

<span id="page-143-2"></span>• [log\\_error](#page-143-2)

| Command-Line Format  | log-error[=file_name] |
|----------------------|-----------------------|
| System Variable      | log_error             |
| Scope                | Global                |
| Dynamic              | No                    |
| SET_VAR Hint Applies | No                    |
| Type                 | File name             |

The default error log destination. If the destination is the console, the value is stderr. Otherwise, the destination is a file and the [log\\_error](#page-143-2) value is the file name. See Section 7.4.2, "The Error Log".

• [log\\_error\\_services](#page-143-1)

<span id="page-143-1"></span>

|     | Command-Line Format  | log-error-services=value |
|-----|----------------------|--------------------------|
|     | System Variable      | log_error_services       |
|     | Scope                | Global                   |
|     | Dynamic              | Yes                      |
|     | SET_VAR Hint Applies | No                       |
| 914 | Type                 | String                   |

| Default Value | log_filter_internal; |
|---------------|----------------------|
|               | log_sink_internal    |

The components to enable for error logging. The variable may contain a list with 0, 1, or many elements. In the latter case, elements may be delimited by semicolon or (as of MySQL 8.0.12) comma, optionally followed by space. A given setting cannot use both semicolon and comma separators. Component order is significant because the server executes components in the order listed.

From MySQL 8.0.30, any loadable (not built in) component named in the [log\\_error\\_services](#page-143-1) is implicitly loaded if it is not already loaded. Before MySQL 8.0.30, any loadable (not built in) component named in the [log\\_error\\_services](#page-143-1) value must first be installed with INSTALL COMPONENT. For more information, see Section 7.4.2.1, "Error Log Configuration".

<span id="page-144-0"></span>• [log\\_error\\_suppression\\_list](#page-144-0)

| Command-Line Format  | log-error-suppression-list=value |
|----------------------|----------------------------------|
| System Variable      | log_error_suppression_list       |
| Scope                | Global                           |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | String                           |
| Default Value        | empty string                     |

The [log\\_error\\_suppression\\_list](#page-144-0) system variable applies to events intended for the error log and specifies which events to suppress when they occur with a priority of WARNING or INFORMATION. For example, if a particular type of warning is considered undesirable "noise" in the error log because it occurs frequently but is not of interest, it can be suppressed. This variable affects filtering performed by the log\_filter\_internal error log filter component, which is enabled by default (see Section 7.5.3, "Error Log Components"). If log\_filter\_internal is disabled, [log\\_error\\_suppression\\_list](#page-144-0) has no effect.

The [log\\_error\\_suppression\\_list](#page-144-0) value may be the empty string for no suppression, or a list of one or more comma-separated values indicating the error codes to suppress. Error codes may be specified in symbolic or numeric form. A numeric code may be specified with or without the MYprefix. Leading zeros in the numeric part are not significant. Examples of permitted code formats:

```
ER_SERVER_SHUTDOWN_COMPLETE
MY-000031
000031
MY-31
31
```

Symbolic values are preferable to numeric values for readability and portability. For information about the permitted error symbols and numbers, see [MySQL 8.0 Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/8.0/en/)

The effect of [log\\_error\\_suppression\\_list](#page-144-0) combines with that of [log\\_error\\_verbosity](#page-144-1). For additional information, see Section 7.4.2.5, "Priority-Based Error Log Filtering (log\_filter\_internal)".

<span id="page-144-1"></span>• [log\\_error\\_verbosity](#page-144-1)

| log_error_verbosity |
|---------------------|
| Global              |
| Yes                 |
|                     |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | Integer |
| Default Value        | 2       |
| Minimum Value        | 1       |
| Maximum Value        | 3       |

The [log\\_error\\_verbosity](#page-144-1) system variable specifies the verbosity for handling events intended for the error log. This variable affects filtering performed by the log\_filter\_internal error log filter component, which is enabled by default (see Section 7.5.3, "Error Log Components"). If log\_filter\_internal is disabled, [log\\_error\\_verbosity](#page-144-1) has no effect.

Events intended for the error log have a priority of ERROR, WARNING, or INFORMATION. [log\\_error\\_verbosity](#page-144-1) controls verbosity based on which priorities to permit for messages written to the log, as shown in the following table.

| log_error_verbosity Value | Permitted Message Priorities |
|---------------------------|------------------------------|
| 1                         | ERROR                        |
| 2                         | ERROR, WARNING               |
| 3                         | ERROR, WARNING, INFORMATION  |

There is also a priority of SYSTEM. System messages about non-error situations are printed to the error log regardless of the [log\\_error\\_verbosity](#page-144-1) value. These messages include startup and shutdown messages, and some significant changes to settings.

The effect of [log\\_error\\_verbosity](#page-144-1) combines with that of [log\\_error\\_suppression\\_list](#page-144-0). For additional information, see Section 7.4.2.5, "Priority-Based Error Log Filtering (log\_filter\_internal)".

## <span id="page-145-0"></span>• [log\\_output](#page-145-0)

| Command-Line Format  | log-output=name |
|----------------------|-----------------|
| System Variable      | log_output      |
| Scope                | Global          |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | No              |
| Type                 | Set             |
| Default Value        | FILE            |
| Valid Values         | TABLE           |
|                      | FILE            |
|                      | NONE            |

The destination or destinations for general query log and slow query log output. The value is a list one or more comma-separated words chosen from TABLE, FILE, and NONE. TABLE selects logging to the [general\\_log](#page-127-0) and slow\_log tables in the mysql system schema. FILE selects logging to log files. NONE disables logging. If NONE is present in the value, it takes precedence over any other words that are present. TABLE and FILE can both be given to select both log output destinations.

This variable selects log output destinations, but does not enable log output. To do that, enable the [general\\_log](#page-127-0) and slow\_query\_log system variables. For FILE logging, the [general\\_log\\_file](#page-127-1) and slow\_query\_log\_file system variables determine the log file locations. For more information, see Section 7.4.1, "Selecting General Query Log and Slow Query Log Output Destinations".

## <span id="page-146-0"></span>• [log\\_queries\\_not\\_using\\_indexes](#page-146-0)

| Command-Line Format  | log-queries-not-using<br>indexes[={OFF ON}] |
|----------------------|---------------------------------------------|
| System Variable      | log_queries_not_using_indexes               |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | Boolean                                     |
| Default Value        | OFF                                         |

If you enable this variable with the slow query log enabled, queries that are expected to retrieve all rows are logged. See Section 7.4.5, "The Slow Query Log". This option does not necessarily mean that no index is used. For example, a query that uses a full index scan uses an index but would be logged because the index would not limit the number of rows.

## <span id="page-146-3"></span>• [log\\_raw](#page-146-3)

| Command-Line Format  | log-raw[={OFF ON}] |
|----------------------|--------------------|
| System Variable      | log_raw            |
| Scope                | Global             |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Boolean            |
| Default Value        | OFF                |

The [log\\_raw](#page-146-3) system variable is initially set to the value of the [--log-raw](#page-64-0) option. See the description of that option for more information. The system variable may also be set at runtime to change password masking behavior.

## <span id="page-146-1"></span>• [log\\_slow\\_admin\\_statements](#page-146-1)

| Command-Line Format  | log-slow-admin-statements[={OFF <br>ON}] |
|----------------------|------------------------------------------|
| System Variable      | log_slow_admin_statements                |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | Boolean                                  |
| Default Value        | OFF                                      |

Include slow administrative statements in the statements written to the slow query log. Administrative statements include ALTER TABLE, ANALYZE TABLE, CHECK TABLE, CREATE INDEX, DROP INDEX, OPTIMIZE TABLE, and REPAIR TABLE.

## <span id="page-146-2"></span>• [log\\_slow\\_extra](#page-146-2)

| Command-Line Format | log-slow-extra[={OFF ON}] |
|---------------------|---------------------------|
| System Variable     | log_slow_extra            |

| Scope                | Global  |
|----------------------|---------|
| Dynamic              | Yes     |
| SET_VAR Hint Applies | No      |
| Type                 | Boolean |
| Default Value        | OFF     |

If the slow query log is enabled and the output destination includes FILE, the server writes additional fields to log file lines that provide information about slow statements. See Section 7.4.5, "The Slow Query Log". TABLE output is unaffected.

## <span id="page-147-1"></span>• [log\\_syslog](#page-147-1)

Prior to MySQL 8.0, this variable controlled whether to perform error logging to the system log (the Event Log on Windows, and syslog on Unix and Unix-like systems).

In MySQL 8.0, the log\_sink\_syseventlog log component implements error logging to the system log (see Section 7.4.2.8, "Error Logging to the System Log"), so this type of logging can be enabled by adding that component to the [log\\_error\\_services](#page-143-1) system variable. [log\\_syslog](#page-147-1) is removed. (Prior to MySQL 8.0.13, [log\\_syslog](#page-147-1) exists but is deprecated and has no effect.)

## <span id="page-147-2"></span>• [log\\_syslog\\_facility](#page-147-2)

This variable was removed in MySQL 8.0.13 and replaced by syseventlog.facility.

## <span id="page-147-3"></span>• [log\\_syslog\\_include\\_pid](#page-147-3)

This variable was removed in MySQL 8.0.13 and replaced by syseventlog.include\_pid.

## <span id="page-147-4"></span>• [log\\_syslog\\_tag](#page-147-4)

This variable was removed in MySQL 8.0.13 and replaced by syseventlog.tag.

## <span id="page-147-0"></span>• [log\\_timestamps](#page-147-0)

| Command-Line Format  | log-timestamps=# |
|----------------------|------------------|
| System Variable      | log_timestamps   |
| Scope                | Global           |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Type                 | Enumeration      |
| Default Value        | UTC              |
| Valid Values         | UTC              |
|                      | SYSTEM           |

This variable controls the time zone of timestamps in messages written to the error log, and in general query log and slow query log messages written to files. It does not affect the time zone of general query log and slow query log messages written to tables (mysql.general\_log, mysql.slow\_log). Rows retrieved from those tables can be converted from the local system time zone to any desired time zone with CONVERT\_TZ() or by setting the session time\_zone system variable.

Permitted [log\\_timestamps](#page-147-0) values are UTC (the default) and SYSTEM (the local system time zone).

Timestamps are written using ISO 8601 / RFC 3339 format: YYYY-MM-DDThh:mm:ss.uuuuuu plus a tail value of Z signifying Zulu time (UTC) or ±hh:mm (an offset from UTC).

<span id="page-148-0"></span>• [log\\_throttle\\_queries\\_not\\_using\\_indexes](#page-148-0)

| Command-Line Format  | log-throttle-queries-not-using<br>indexes=# |
|----------------------|---------------------------------------------|
| System Variable      | log_throttle_queries_not_using_indexes      |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | Integer                                     |
| Default Value        | 0                                           |
| Minimum Value        | 0                                           |
| Maximum Value        | 4294967295                                  |

If [log\\_queries\\_not\\_using\\_indexes](#page-146-0) is enabled, the [log\\_throttle\\_queries\\_not\\_using\\_indexes](#page-148-0) variable limits the number of such queries per minute that can be written to the slow query log. A value of 0 (the default) means "no limit". For more information, see Section 7.4.5, "The Slow Query Log".

<span id="page-148-1"></span>• [long\\_query\\_time](#page-148-1)

| Command-Line Format  | long-query-time=# |
|----------------------|-------------------|
| System Variable      | long_query_time   |
| Scope                | Global, Session   |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | Numeric           |
| Default Value        | 10                |
| Minimum Value        | 0                 |
| Maximum Value        | 31536000          |
| Unit                 | seconds           |

If a query takes longer than this many seconds, the server increments the Slow\_queries status variable. If the slow query log is enabled, the query is logged to the slow query log file. This value is measured in real time, not CPU time, so a query that is under the threshold on a lightly loaded system might be above the threshold on a heavily loaded one. The minimum and default values of [long\\_query\\_time](#page-148-1) are 0 and 10, respectively. The maximum is 31536000, which is 365 days in seconds. The value can be specified to a resolution of microseconds. See Section 7.4.5, "The Slow Query Log".

Smaller values of this variable result in more statements being considered long-running, with the result that more space is required for the slow query log. For very small values (less than one second), the log may grow quite large in a small time. Increasing the number of statements considered long-running may also result in false positives for the "excessive Number of Long Running Processes" alert in MySQL Enterprise Monitor, especially if Group Replication is enabled. For these reasons, very small values should be used in test environments only, or, in production environments, only for a short period.

mysqldump performs a full table scan, which means its queries can often exceed a [long\\_query\\_time](#page-148-1) setting that is useful for regular queries. From MySQL 8.0.30, if you want to exclude most or all of mysqldump's queries from the slow query log, you can set mysqldump's --mysqld-long-query-time command line option to change the session value of the system variable to a higher value.

## <span id="page-149-0"></span>• [low\\_priority\\_updates](#page-149-0)

| Command-Line Format  | low-priority-updates[={OFF ON}] |
|----------------------|---------------------------------|
| System Variable      | low_priority_updates            |
| Scope                | Global, Session                 |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |
| Default Value        | OFF                             |

If set to 1, all INSERT, UPDATE, DELETE, and LOCK TABLE WRITE statements wait until there is no pending SELECT or LOCK TABLE READ on the affected table. The same effect can be obtained using {INSERT | REPLACE | DELETE | UPDATE} LOW\_PRIORITY ... to lower the priority of only one query. This variable affects only storage engines that use only table-level locking (such as MyISAM, MEMORY, and MERGE). See Section 10.11.2, "Table Locking Issues".

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

## <span id="page-149-1"></span>• [lower\\_case\\_file\\_system](#page-149-1)

| System Variable      | lower_case_file_system |
|----------------------|------------------------|
| Scope                | Global                 |
| Dynamic              | No                     |
| SET_VAR Hint Applies | No                     |
| Type                 | Boolean                |

This variable describes the case sensitivity of file names on the file system where the data directory is located. OFF means file names are case-sensitive, ON means they are not case-sensitive. This variable is read only because it reflects a file system attribute and setting it would have no effect on the file system.

## <span id="page-149-2"></span>• [lower\\_case\\_table\\_names](#page-149-2)

| Command-Line Format     | lower-case-table-names[=#] |
|-------------------------|----------------------------|
| System Variable         | lower_case_table_names     |
| Scope                   | Global                     |
| Dynamic                 | No                         |
| SET_VAR Hint Applies    | No                         |
| Type                    | Integer                    |
| Default Value (macOS)   | 2                          |
| Default Value (Unix)    | 0                          |
| Default Value (Windows) | 1                          |
| Minimum Value           | 0                          |
| Maximum Value           | 2                          |

If set to 0, table names are stored as specified and comparisons are case-sensitive. If set to 1, table names are stored in lowercase on disk and comparisons are not case-sensitive. If set to 2, table

names are stored as given but compared in lowercase. This option also applies to database names and table aliases. For additional details, see Section 11.2.3, "Identifier Case Sensitivity".

The default value of this variable is platform-dependent (see [lower\\_case\\_file\\_system](#page-149-1)). On Linux and other Unix-like systems, the default is 0. On Windows the default value is 1. On macOS, the default value is 2. On Linux (and other Unix-like systems), setting the value to 2 is not supported; the server forces the value to 0 instead.

You should not set [lower\\_case\\_table\\_names](#page-149-2) to 0 if you are running MySQL on a system where the data directory resides on a case-insensitive file system (such as on Windows or macOS). It is an unsupported combination that could result in a hang condition when running an INSERT INTO ... SELECT ... FROM tbl\_name operation with the wrong tbl\_name lettercase. With MyISAM, accessing table names using different lettercases could cause index corruption.

An error message is printed and the server exits if you attempt to start the server with [-](#page-149-2) [lower\\_case\\_table\\_names=0](#page-149-2) on a case-insensitive file system.

The setting of this variable affects the behavior of replication filtering options with regard to case sensitivity. For more information, see Section 19.2.5, "How Servers Evaluate Replication Filtering Rules".

It is prohibited to start the server with a [lower\\_case\\_table\\_names](#page-149-2) setting that is different from the setting used when the server was initialized. The restriction is necessary because collations used by various data dictionary table fields are determined by the setting defined when the server is initialized, and restarting the server with a different setting would introduce inconsistencies with respect to how identifiers are ordered and compared.

It is therefore necessary to configure [lower\\_case\\_table\\_names](#page-149-2) to the desired setting before initializing the server. In most cases, this requires configuring [lower\\_case\\_table\\_names](#page-149-2) in a MySQL option file before starting the MySQL server for the first time. For APT installations on Debian and Ubuntu, however, the server is initialized for you, and there is no opportunity to configure the setting in an option file beforehand. You must therefore use the debconf-set-selection utility prior to installing MySQL using APT to enable [lower\\_case\\_table\\_names](#page-149-2). To do so, run this command before installing MySQL using APT:

\$> **sudo debconf-set-selections <<< "mysql-server mysql-server/lowercase-table-names select Enabled"**

![](_page_150_Picture_9.jpeg)

#### **Note**

The ability to enable [lower\\_case\\_table\\_names](#page-149-2) using debconfset-selections was added in MySQL 8.0.17. Enabling [lower\\_case\\_table\\_names](#page-149-2) sets the value to 1.

<span id="page-150-0"></span>• [mandatory\\_roles](#page-150-0)

| Command-Line Format  | mandatory-roles=value |
|----------------------|-----------------------|
| System Variable      | mandatory_roles       |
| Scope                | Global                |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | String                |
| Default Value        | empty string          |

Roles the server should treat as mandatory. In effect, these roles are automatically granted to every user, although setting [mandatory\\_roles](#page-150-0) does not actually change any user accounts, and the granted roles are not visible in the mysql.role\_edges system table.

The variable value is a comma-separated list of role names. Example:

```
SET PERSIST mandatory_roles = '`role1`@`%`,`role2`,role3,role4@localhost';
```

Setting the runtime value of [mandatory\\_roles](#page-150-0) requires the ROLE\_ADMIN privilege, in addition to the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege) normally required to set a global system variable runtime value.

Role names consist of a user part and host part in user\_name@host\_name format. The host part, if omitted, defaults to %. For additional information, see Section 8.2.5, "Specifying Role Names".

The [mandatory\\_roles](#page-150-0) value is a string, so user names and host names, if quoted, must be written in a fashion permitted for quoting within quoted strings.

Roles named in the value of [mandatory\\_roles](#page-150-0) cannot be revoked with REVOKE or dropped with DROP ROLE or DROP USER.

To prevent sessions from being made system sessions by default, a role that has the SYSTEM\_USER privilege cannot be listed in the value of the [mandatory\\_roles](#page-150-0) system variable:

- If [mandatory\\_roles](#page-150-0) is assigned a role at startup that has the SYSTEM\_USER privilege, the server writes a message to the error log and exits.
- If [mandatory\\_roles](#page-150-0) is assigned a role at runtime that has the SYSTEM\_USER privilege, an error occurs and the [mandatory\\_roles](#page-150-0) value remains unchanged.

Mandatory roles, like explicitly granted roles, do not take effect until activated (see Activating Roles). At login time, role activation occurs for all granted roles if the [activate\\_all\\_roles\\_on\\_login](#page-82-0) system variable is enabled; otherwise, or for roles that are set as default roles otherwise. At runtime, SET ROLE activates roles.

Roles that do not exist when assigned to [mandatory\\_roles](#page-150-0) but are created later may require special treatment to be considered mandatory. For details, see Defining Mandatory Roles.

SHOW GRANTS displays mandatory roles according to the rules described in Section 15.7.7.21, "SHOW GRANTS Statement".

<span id="page-151-0"></span>• [max\\_allowed\\_packet](#page-151-0)

| Command-Line Format  | max-allowed-packet=# |
|----------------------|----------------------|
| System Variable      | max_allowed_packet   |
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | Integer              |
| Default Value        | 67108864             |
| Minimum Value        | 1024                 |
| Maximum Value        | 1073741824           |
| Unit                 | bytes                |

| Block Size |
|------------|
|------------|

The maximum size of one packet or any generated/intermediate string, or any parameter sent by the [mysql\\_stmt\\_send\\_long\\_data\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-stmt-send-long-data.md) C API function. The default is 64MB.

The packet message buffer is initialized to [net\\_buffer\\_length](#page-165-1) bytes, but can grow up to [max\\_allowed\\_packet](#page-151-0) bytes when needed. This value by default is small, to catch large (possibly incorrect) packets.

You must increase this value if you are using large BLOB columns or long strings. It should be as big as the largest BLOB you want to use. The protocol limit for [max\\_allowed\\_packet](#page-151-0) is 1GB. The value should be a multiple of 1024; nonmultiples are rounded down to the nearest multiple.

When you change the message buffer size by changing the value of the [max\\_allowed\\_packet](#page-151-0) variable, you should also change the buffer size on the client side if your client program permits it. The default [max\\_allowed\\_packet](#page-151-0) value built in to the client library is 1GB, but individual client programs might override this. For example, mysql and mysqldump have defaults of 16MB and 24MB, respectively. They also enable you to change the client-side value by setting [max\\_allowed\\_packet](#page-151-0) on the command line or in an option file.

The session value of this variable is read only. The client can receive up to as many bytes as the session value. However, the server does not send to the client more bytes than the current global [max\\_allowed\\_packet](#page-151-0) value. (The global value could be less than the session value if the global value is changed after the client connects.)

<span id="page-152-0"></span>• [max\\_connect\\_errors](#page-152-0)

| Command-Line Format              | max-connect-errors=# |
|----------------------------------|----------------------|
| System Variable                  | max_connect_errors   |
| Scope                            | Global               |
| Dynamic                          | Yes                  |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value                    | 100                  |
| Minimum Value                    | 1                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

After [max\\_connect\\_errors](#page-152-0) successive connection requests from a host are interrupted without a successful connection, the server blocks that host from further connections. If a connection from a host is established successfully within fewer than [max\\_connect\\_errors](#page-152-0) attempts after a previous connection was interrupted, the error count for the host is cleared to zero. To unblock blocked hosts, flush the host cache; see Flushing the Host Cache.

<span id="page-152-1"></span>• [max\\_connections](#page-152-1)

| Command-Line Format  | max-connections=# |
|----------------------|-------------------|
| System Variable      | max_connections   |
| Scope                | Global            |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | Integer           |
| Default Value        | 151<br>923        |

| Minimum Value | 1      |
|---------------|--------|
| Maximum Value | 100000 |

The maximum permitted number of simultaneous client connections. The maximum effective value is the lesser of the effective value of [open\\_files\\_limit](#page-169-1) - 810, and the value actually set for max\_connections.

For more information, see Section 7.1.12.1, "Connection Interfaces".

<span id="page-153-0"></span>• [max\\_delayed\\_threads](#page-153-0)

| Command-Line Format  | max-delayed-threads=# |
|----------------------|-----------------------|
| Deprecated           | Yes                   |
| System Variable      | max_delayed_threads   |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Integer               |
| Default Value        | 20                    |
| Minimum Value        | 0                     |
| Maximum Value        | 16384                 |

This system variable is deprecated (because DELAYED inserts are not supported) and subject to removal in a future MySQL release.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-153-1"></span>• [max\\_digest\\_length](#page-153-1)

| Command-Line Format  | max-digest-length=# |
|----------------------|---------------------|
| System Variable      | max_digest_length   |
| Scope                | Global              |
| Dynamic              | No                  |
| SET_VAR Hint Applies | No                  |
| Type                 | Integer             |
| Default Value        | 1024                |
| Minimum Value        | 0                   |
| Maximum Value        | 1048576             |
| Unit                 | bytes               |

The maximum number of bytes of memory reserved per session for computation of normalized statement digests. Once that amount of space is used during digest computation, truncation occurs: no further tokens from a parsed statement are collected or figure into its digest value. Statements that differ only after that many bytes of parsed tokens produce the same normalized statement digest and are considered identical if compared or if aggregated for digest statistics.

The length used for calculating a normalized statement digest is the sum of the length of the normalized statement digest and the length of the statement digest. Since the length of the statement digest is always 64, this is equivalent to LENGTH (STATEMENT\_DIGEST\_TEXT(statement) ) +

64. This means that, when the value of max\_digest\_length is 1024 (the default), the maximum length for a normalized SQL statement before truncation occurs is in effect 960 bytes.

![](_page_154_Picture_2.jpeg)

### **Warning**

Setting [max\\_digest\\_length](#page-153-1) to zero disables digest production, which also disables server functionality that requires digests, such as MySQL Enterprise Firewall.

Decreasing the [max\\_digest\\_length](#page-153-1) value reduces memory use but causes the digest value of more statements to become indistinguishable if they differ only at the end. Increasing the value permits longer statements to be distinguished but increases memory use, particularly for workloads that involve large numbers of simultaneous sessions (the server allocates [max\\_digest\\_length](#page-153-1) bytes per session).

The parser uses this system variable as a limit on the maximum length of normalized statement digests that it computes. The Performance Schema, if it tracks statement digests, makes a copy of the digest value, using the performance\_schema\_max\_digest\_length. system variable as a limit on the maximum length of digests that it stores. Consequently, if performance\_schema\_max\_digest\_length is less than [max\\_digest\\_length](#page-153-1), digest values stored in the Performance Schema are truncated relative to the original digest values.

For more information about statement digesting, see Section 29.10, "Performance Schema Statement Digests and Sampling".

<span id="page-154-0"></span>• [max\\_error\\_count](#page-154-0)

| Command-Line Format  | max-error-count=# |
|----------------------|-------------------|
| System Variable      | max_error_count   |
| Scope                | Global, Session   |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | Yes               |
| Type                 | Integer           |
| Default Value        | 1024              |
| Minimum Value        | 0                 |
| Maximum Value        | 65535             |

The maximum number of error, warning, and information messages to be stored for display by the SHOW ERRORS and SHOW WARNINGS statements. This is the same as the number of condition areas in the diagnostics area, and thus the number of conditions that can be inspected by GET DIAGNOSTICS.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-154-1"></span>• [max\\_execution\\_time](#page-154-1)

| Command-Line Format  | max-execution-time=# |
|----------------------|----------------------|
| System Variable      | max_execution_time   |
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | Yes                  |
| Type                 | Integer              |

| Default Value | 0            |
|---------------|--------------|
| Minimum Value | 0            |
| Maximum Value | 4294967295   |
| Unit          | milliseconds |

The execution timeout for SELECT statements, in milliseconds. If the value is 0, timeouts are not enabled.

[max\\_execution\\_time](#page-154-1) applies as follows:

- The global [max\\_execution\\_time](#page-154-1) value provides the default for the session value for new connections. The session value applies to SELECT executions executed within the session that include no MAX\_EXECUTION\_TIME(N) optimizer hint or for which N is 0.
- [max\\_execution\\_time](#page-154-1) applies to read-only SELECT statements. Statements that are not read only are those that invoke a stored function that modifies data as a side effect.
- [max\\_execution\\_time](#page-154-1) is ignored for SELECT statements in stored programs.
- <span id="page-155-0"></span>• [max\\_heap\\_table\\_size](#page-155-0)

| Command-Line Format              | max-heap-table-size=# |
|----------------------------------|-----------------------|
| System Variable                  | max_heap_table_size   |
| Scope                            | Global, Session       |
| Dynamic                          | Yes                   |
| SET_VAR Hint Applies             | Yes                   |
| Type                             | Integer               |
| Default Value                    | 16777216              |
| Minimum Value                    | 16384                 |
| Maximum Value (64-bit platforms) | 18446744073709550592  |
| Maximum Value (32-bit platforms) | 4294966272            |
| Unit                             | bytes                 |
| Block Size                       | 1024                  |

This variable sets the maximum size to which user-created MEMORY tables are permitted to grow. The value of the variable is used to calculate MEMORY table MAX\_ROWS values.

Setting this variable has no effect on any existing MEMORY table, unless the table is re-created with a statement such as CREATE TABLE or altered with ALTER TABLE or TRUNCATE TABLE. A server restart also sets the maximum size of existing MEMORY tables to the global [max\\_heap\\_table\\_size](#page-155-0) value.

This variable is also used in conjunction with tmp\_table\_size to limit the size of internal inmemory tables. See Section 10.4.4, "Internal Temporary Table Use in MySQL".

max\_heap\_table\_size is not replicated. See Section 19.5.1.21, "Replication and MEMORY Tables", and Section 19.5.1.39, "Replication and Variables", for more information.

<span id="page-155-1"></span>• [max\\_insert\\_delayed\\_threads](#page-155-1)

| Deprecated      | Yes                        |
|-----------------|----------------------------|
| System Variable | max_insert_delayed_threads |
| Scope           | Global, Session            |

| Dynamic              | Yes     |
|----------------------|---------|
| SET_VAR Hint Applies | No      |
| Type                 | Integer |
| Default Value        | 0       |
| Minimum Value        | 20      |
| Maximum Value        | 16384   |

This variable is a synonym for [max\\_delayed\\_threads](#page-153-0). Like [max\\_delayed\\_threads](#page-153-0), it is deprecated (because DELAYED inserts are not supported) and subject to removal in a future MySQL release.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-156-0"></span>• [max\\_join\\_size](#page-156-0)

| Command-Line Format  | max-join-size=#      |
|----------------------|----------------------|
| System Variable      | max_join_size        |
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | Yes                  |
| Type                 | Integer              |
| Default Value        | 18446744073709551615 |
| Minimum Value        | 1                    |
| Maximum Value        | 18446744073709551615 |

As of MySQL 8.0.31, this represents a limit on the maximum number of row accesses in base tables made by a join. If the server's estimate indicates that a greater number of rows than max\_join\_size must be read from the base tables, the statement is rejected with an error.

MySQL 8.0.30 and earlier: Do not permit statements that probably need to examine more than max\_join\_size rows (for single-table statements) or row combinations (for multiple-table statements) or that are likely to do more than max\_join\_size disk seeks. By setting this value, you can catch statements where keys are not used properly and that would probably take a long time. Set it if your users tend to perform joins that lack a WHERE clause, that take a long time, or that return millions of rows. For more information, see Using Safe-Updates Mode (--safe-updates).

Regardless of MySQL release version, setting this variable to a value other than DEFAULT resets the value of sql\_big\_selects to 0. If you set the sql\_big\_selects value again, the max\_join\_size variable is ignored.

<span id="page-156-1"></span>• [max\\_length\\_for\\_sort\\_data](#page-156-1)

| Command-Line Format  | max-length-for-sort-data=# |
|----------------------|----------------------------|
| Deprecated           | Yes                        |
| System Variable      | max_length_for_sort_data   |
| Scope                | Global, Session            |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | Yes                        |
| Type                 | Integer                    |

| Default Value | 4096    |
|---------------|---------|
| Minimum Value | 4       |
| Maximum Value | 8388608 |
| Unit          | bytes   |

This variable is deprecated as of MySQL 8.0.20 due to optimizer changes that make it obsolete and of no effect. Previously, it acted as the cutoff on the size of index values that determines which filesort algorithm to use. See Section 10.2.1.16, "ORDER BY Optimization".

## <span id="page-157-0"></span>• [max\\_points\\_in\\_geometry](#page-157-0)

| Command-Line Format  | max-points-in-geometry=# |
|----------------------|--------------------------|
| System Variable      | max_points_in_geometry   |
| Scope                | Global, Session          |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | Yes                      |
| Type                 | Integer                  |
| Default Value        | 65536                    |
| Minimum Value        | 3                        |
| Maximum Value        | 1048576                  |

The maximum value of the points\_per\_circle argument to the ST\_Buffer\_Strategy() function.

## <span id="page-157-1"></span>• [max\\_prepared\\_stmt\\_count](#page-157-1)

| Command-Line Format  | max-prepared-stmt-count=# |
|----------------------|---------------------------|
| System Variable      | max_prepared_stmt_count   |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |
| Default Value        | 16382                     |
| Minimum Value        | 0                         |
| Maximum Value        | 4194304                   |

This variable limits the total number of prepared statements in the server. It can be used in environments where there is the potential for denial-of-service attacks based on running the server out of memory by preparing huge numbers of statements. If the value is set lower than the current number of prepared statements, existing statements are not affected and can be used, but no new statements can be prepared until the current number drops below the limit. Setting the value to 0 disables prepared statements.

## <span id="page-157-2"></span>• [max\\_seeks\\_for\\_key](#page-157-2)

| Command-Line Format  | max-seeks-for-key=# |
|----------------------|---------------------|
| System Variable      | max_seeks_for_key   |
| Scope                | Global, Session     |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | Yes                 |

| Type                                    | Integer              |
|-----------------------------------------|----------------------|
| Default Value (Windows)                 | 4294967295           |
| Default Value (Other, 64-bit platforms) | 18446744073709551615 |
| Default Value (Other, 32-bit platforms) | 4294967295           |
| Minimum Value                           | 1                    |
| Maximum Value (Windows)                 | 4294967295           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551615 |
| Maximum Value (Other, 32-bit platforms) | 4294967295           |

Limit the assumed maximum number of seeks when looking up rows based on a key. The MySQL optimizer assumes that no more than this number of key seeks are required when searching for matching rows in a table by scanning an index, regardless of the actual cardinality of the index (see Section 15.7.7.22, "SHOW INDEX Statement"). By setting this to a low value (say, 100), you can force MySQL to prefer indexes instead of table scans.

## <span id="page-158-0"></span>• [max\\_sort\\_length](#page-158-0)

| Command-Line Format  | max-sort-length=# |
|----------------------|-------------------|
| System Variable      | max_sort_length   |
| Scope                | Global, Session   |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | Yes               |
| Type                 | Integer           |
| Default Value        | 1024              |
| Minimum Value        | 4                 |
| Maximum Value        | 8388608           |
| Unit                 | bytes             |

The number of bytes to use when sorting string values which use PAD SPACE collations. The server uses only the first [max\\_sort\\_length](#page-158-0) bytes of any such value and ignores the rest. Consequently, such values that differ only after the first [max\\_sort\\_length](#page-158-0) bytes compare as equal for GROUP BY, ORDER BY, and DISTINCT operations. (This behavior differs from previous versions of MySQL, where this setting was applied to all values used in comparisons.)

Increasing the value of [max\\_sort\\_length](#page-158-0) may require increasing the value of sort\_buffer\_size as well. For details, see Section 10.2.1.16, "ORDER BY Optimization"

## <span id="page-158-1"></span>• [max\\_sp\\_recursion\\_depth](#page-158-1)

| Command-Line Format  | max-sp-recursion-depth[=#] |
|----------------------|----------------------------|
| System Variable      | max_sp_recursion_depth     |
| Scope                | Global, Session            |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 0                          |
| Minimum Value        | 0                          |

| Maximum Value | 255 |
|---------------|-----|
|---------------|-----|

The number of times that any given stored procedure may be called recursively. The default value for this option is 0, which completely disables recursion in stored procedures. The maximum value is 255.

Stored procedure recursion increases the demand on thread stack space. If you increase the value of [max\\_sp\\_recursion\\_depth](#page-158-1), it may be necessary to increase thread stack size by increasing the value of thread\_stack at server startup.

<span id="page-159-0"></span>• [max\\_user\\_connections](#page-159-0)

| Command-Line Format  | max-user-connections=# |
|----------------------|------------------------|
| System Variable      | max_user_connections   |
| Scope                | Global, Session        |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | Integer                |
| Default Value        | 0                      |
| Minimum Value        | 0                      |
| Maximum Value        | 4294967295             |

The maximum number of simultaneous connections permitted to any given MySQL user account. A value of 0 (the default) means "no limit."

This variable has a global value that can be set at server startup or runtime. It also has a read-only session value that indicates the effective simultaneous-connection limit that applies to the account associated with the current session. The session value is initialized as follows:

- If the user account has a nonzero MAX\_USER\_CONNECTIONS resource limit, the session [max\\_user\\_connections](#page-159-0) value is set to that limit.
- Otherwise, the session [max\\_user\\_connections](#page-159-0) value is set to the global value.

Account resource limits are specified using the CREATE USER or ALTER USER statement. See Section 8.2.21, "Setting Account Resource Limits".

<span id="page-159-1"></span>• [max\\_write\\_lock\\_count](#page-159-1)

| Command-Line Format                     | max-write-lock-count=# |
|-----------------------------------------|------------------------|
| System Variable                         | max_write_lock_count   |
| Scope                                   | Global                 |
| Dynamic                                 | Yes                    |
| SET_VAR Hint Applies                    | No                     |
| Type                                    | Integer                |
| Default Value (Windows)                 | 4294967295             |
| Default Value (Other, 64-bit platforms) | 18446744073709551615   |
| Default Value (Other, 32-bit platforms) | 4294967295             |
| Minimum Value                           | 1                      |
| Maximum Value (Windows)                 | 4294967295             |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551615   |

| Maximum Value (Other, 32-bit platforms) | 4294967295 |
|-----------------------------------------|------------|
|-----------------------------------------|------------|

After this many write locks, permit some pending read lock requests to be processed in between. Write lock requests have higher priority than read lock requests. However, if [max\\_write\\_lock\\_count](#page-159-1) is set to some low value (say, 10), read lock requests may be preferred over pending write lock requests if the read lock requests have already been passed over in favor of 10 write lock requests. Normally this behavior does not occur because [max\\_write\\_lock\\_count](#page-159-1) by default has a very large value.

<span id="page-160-0"></span>• [mecab\\_rc\\_file](#page-160-0)

| Command-Line Format  | mecab-rc-file=file_name |
|----------------------|-------------------------|
| System Variable      | mecab_rc_file           |
| Scope                | Global                  |
| Dynamic              | No                      |
| SET_VAR Hint Applies | No                      |
| Type                 | File name               |

The mecab\_rc\_file option is used when setting up the MeCab full-text parser.

The mecab\_rc\_file option defines the path to the mecabrc configuration file, which is the configuration file for MeCab. The option is read-only and can only be set at startup. The mecabrc configuration file is required to initialize MeCab.

For information about the MeCab full-text parser, see Section 14.9.9, "MeCab Full-Text Parser Plugin".

For information about options that can be specified in the MeCab mecabrc configuration file, refer to the [MeCab Documentation](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.md) on the [Google Developers](https://code.google.com/) site.

<span id="page-160-2"></span>• [metadata\\_locks\\_cache\\_size](#page-160-2)

This system variable was removed in MySQL 8.0.13.

<span id="page-160-3"></span>• [metadata\\_locks\\_hash\\_instances](#page-160-3)

This system variable was removed in MySQL 8.0.13.

<span id="page-160-1"></span>• [min\\_examined\\_row\\_limit](#page-160-1)

| Command-Line Format              | min-examined-row-limit=# |
|----------------------------------|--------------------------|
| System Variable                  | min_examined_row_limit   |
| Scope                            | Global, Session          |
| Dynamic                          | Yes                      |
| SET_VAR Hint Applies             | No                       |
| Type                             | Integer                  |
| Default Value                    | 0                        |
| Minimum Value                    | 0                        |
| Maximum Value (64-bit platforms) | 18446744073709551615     |

| Maximum Value (32-bit platforms) | 4294967295 |
|----------------------------------|------------|
|----------------------------------|------------|

Queries that examine fewer than this number of rows are not logged to the slow query log.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-161-0"></span>• [myisam\\_data\\_pointer\\_size](#page-161-0)

| Command-Line Format  | myisam-data-pointer-size=# |
|----------------------|----------------------------|
| System Variable      | myisam_data_pointer_size   |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Integer                    |
| Default Value        | 6                          |
| Minimum Value        | 2                          |
| Maximum Value        | 7                          |
| Unit                 | bytes                      |

The default pointer size in bytes, to be used by CREATE TABLE for MyISAM tables when no MAX\_ROWS option is specified. This variable cannot be less than 2 or larger than 7. The default value is 6. See Section B.3.2.10, "The table is full".

<span id="page-161-1"></span>• [myisam\\_max\\_sort\\_file\\_size](#page-161-1)

| Command-Line Format                     | myisam-max-sort-file-size=# |
|-----------------------------------------|-----------------------------|
| System Variable                         | myisam_max_sort_file_size   |
| Scope                                   | Global                      |
| Dynamic                                 | Yes                         |
| SET_VAR Hint Applies                    | No                          |
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

## <span id="page-162-0"></span>• [myisam\\_mmap\\_size](#page-162-0)

| Command-Line Format              | myisam-mmap-size=#   |
|----------------------------------|----------------------|
| System Variable                  | myisam_mmap_size     |
| Scope                            | Global               |
| Dynamic                          | No                   |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value (64-bit platforms) | 18446744073709551615 |
| Default Value (32-bit platforms) | 4294967295           |
| Minimum Value                    | 7                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |
| Unit                             | bytes                |

The maximum amount of memory to use for memory mapping compressed MyISAM files. If many compressed MyISAM tables are used, the value can be decreased to reduce the likelihood of memory-swapping problems.

## <span id="page-162-1"></span>• [myisam\\_recover\\_options](#page-162-1)

| Command-Line Format  | myisam-recover-options[=list] |
|----------------------|-------------------------------|
| System Variable      | myisam_recover_options        |
| Scope                | Global                        |
| Dynamic              | No                            |
| SET_VAR Hint Applies | No                            |
| Type                 | Enumeration                   |
| Default Value        | OFF                           |
| Valid Values         | OFF                           |
|                      | DEFAULT                       |
|                      | BACKUP                        |
|                      | FORCE                         |
|                      | QUICK                         |

Set the MyISAM storage engine recovery mode. The variable value is any combination of the values of OFF, DEFAULT, BACKUP, FORCE, or QUICK. If you specify multiple values, separate them by commas. Specifying the variable with no value at server startup is the same as specifying DEFAULT, and specifying with an explicit value of "" disables recovery (same as a value of OFF). If recovery is enabled, each time mysqld opens a MyISAM table, it checks whether the table is marked as crashed or was not closed properly. (The last option works only if you are running with external locking disabled.) If this is the case, mysqld runs a check on the table. If the table was corrupted, mysqld attempts to repair it.

The following options affect how the repair works.

| Option | Description  |
|--------|--------------|
| OFF    | No recovery. |
|        |              |

| Option  | Description                                                                                                          |
|---------|----------------------------------------------------------------------------------------------------------------------|
| DEFAULT | Recovery without backup, forcing, or quick<br>checking.                                                              |
| BACKUP  | If the data file was changed during recovery,<br>save a backup of the tbl_name.MYD file as<br>tbl_name-datetime.BAK. |
| FORCE   | Run recovery even if we would lose more than<br>one row from the .MYD file.                                          |
| QUICK   | Do not check the rows in the table if there are not<br>any delete blocks.                                            |

Before the server automatically repairs a table, it writes a note about the repair to the error log. If you want to be able to recover from most problems without user intervention, you should use the options BACKUP,FORCE. This forces a repair of a table even if some rows would be deleted, but it keeps the old data file as a backup so that you can later examine what happened.

See Section 18.2.1, "MyISAM Startup Options".

<span id="page-163-2"></span>• [myisam\\_repair\\_threads](#page-163-2)

![](_page_163_Picture_5.jpeg)

#### **Note**

This system variable is deprecated in MySQL 8.0.29 and removed in MySQL 8.0.30.

From MySQL 8.0.29, values other than 1 produce a warning.

If this value is greater than 1, MyISAM table indexes are created in parallel (each index in its own thread) during the Repair by sorting process. The default value is 1.

![](_page_163_Picture_10.jpeg)

## **Note**

Multithreaded repair is beta-quality code.

<span id="page-163-0"></span>• [myisam\\_sort\\_buffer\\_size](#page-163-0)

| Command-Line Format              | myisam-sort-buffer-size=# |
|----------------------------------|---------------------------|
| System Variable                  | myisam_sort_buffer_size   |
| Scope                            | Global, Session           |
| Dynamic                          | Yes                       |
| SET_VAR Hint Applies             | No                        |
| Type                             | Integer                   |
| Default Value                    | 8388608                   |
| Minimum Value                    | 4096                      |
| Maximum Value (64-bit platforms) | 18446744073709551615      |
| Maximum Value (32-bit platforms) | 4294967295                |
| Unit                             | bytes                     |

The size of the buffer that is allocated when sorting MyISAM indexes during a REPAIR TABLE or when creating indexes with CREATE INDEX or ALTER TABLE.

<span id="page-163-1"></span>• [myisam\\_stats\\_method](#page-163-1)

| Command-Line Format | myisam-stats-method=name |
|---------------------|--------------------------|
|                     |                          |

| System Variable      | myisam_stats_method |
|----------------------|---------------------|
| Scope                | Global, Session     |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |
| Type                 | Enumeration         |
| Default Value        | nulls_unequal       |
| Valid Values         | nulls_unequal       |
|                      | nulls_equal         |
|                      | nulls_ignored       |

How the server treats NULL values when collecting statistics about the distribution of index values for MyISAM tables. This variable has three possible values, nulls\_equal, nulls\_unequal, and nulls\_ignored. For nulls\_equal, all NULL index values are considered equal and form a single value group that has a size equal to the number of NULL values. For nulls\_unequal, NULL values are considered unequal, and each NULL forms a distinct value group of size 1. For nulls\_ignored, NULL values are ignored.

The method that is used for generating table statistics influences how the optimizer chooses indexes for query execution, as described in Section 10.3.8, "InnoDB and MyISAM Index Statistics Collection".

## <span id="page-164-0"></span>• [myisam\\_use\\_mmap](#page-164-0)

| Command-Line Format  | myisam-use-mmap[={OFF ON}] |
|----------------------|----------------------------|
| System Variable      | myisam_use_mmap            |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Boolean                    |
| Default Value        | OFF                        |

Use memory mapping for reading and writing MyISAM tables.

## <span id="page-164-1"></span>• [mysql\\_native\\_password\\_proxy\\_users](#page-164-1)

| Command-Line Format  | mysql-native-password-proxy<br>users[={OFF ON}] |
|----------------------|-------------------------------------------------|
| Deprecated           | Yes                                             |
| System Variable      | mysql_native_password_proxy_users               |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Boolean                                         |
| Default Value        | OFF                                             |

This variable controls whether the mysql\_native\_password built-in authentication plugin supports proxy users. It has no effect unless the [check\\_proxy\\_users](#page-102-1) system variable is enabled. For information about user proxying, see Section 8.2.19, "Proxy Users".

<span id="page-164-2"></span>• [named\\_pipe](#page-164-2)

| Command-Line Format  | named-pipe[={OFF ON}] |
|----------------------|-----------------------|
| System Variable      | named_pipe            |
| Scope                | Global                |
| Dynamic              | No                    |
| SET_VAR Hint Applies | No                    |
| Platform Specific    | Windows               |
| Type                 | Boolean               |
| Default Value        | OFF                   |

(Windows only.) Indicates whether the server supports connections over named pipes.

<span id="page-165-0"></span>• [named\\_pipe\\_full\\_access\\_group](#page-165-0)

| Command-Line Format  | named-pipe-full-access-group=value |
|----------------------|------------------------------------|
| System Variable      | named_pipe_full_access_group       |
| Scope                | Global                             |
| Dynamic              | No                                 |
| SET_VAR Hint Applies | No                                 |
| Platform Specific    | Windows                            |
| Type                 | String                             |
| Default Value        | empty string                       |
| Valid Values         | empty string                       |
|                      | valid Windows local group name     |
|                      | *everyone*                         |

(Windows only.) The access control granted to clients on the named pipe created by the MySQL server is set to the minimum necessary for successful communication when the [named\\_pipe](#page-164-2) system variable is enabled to support named-pipe connections. Some MySQL client software can open named pipe connections without any additional configuration; however, other client software may still require full access to open a named pipe connection.

This variable sets the name of a Windows local group whose members are granted sufficient access by the MySQL server to use named-pipe clients. As of MySQL 8.0.24, the default value is set to an empty string, which means that no Windows user is granted full access to the named pipe.

A new Windows local group name (for example, mysql\_access\_client\_users) can be created in Windows and then used to replace the default value when access is absolutely necessary. In this case, limit the membership of the group to as few users as possible, removing users from the group when their client software is upgraded. A non-member of the group who attempts to open a connection to MySQL with the affected named-pipe client is denied access until a Windows administrator adds the user to the group. Newly added users must log out and log in again to join the group (required by Windows).

Setting the value to '\*everyone\*' provides a language-independent way of referring to the Everyone group on Windows. The Everyone group is not secure by default.

<span id="page-165-1"></span>• [net\\_buffer\\_length](#page-165-1)

| Command-Line Format | net-buffer-length=# |
|---------------------|---------------------|
| System Variable     | net_buffer_length   |

| Scope                | Global, Session |
|----------------------|-----------------|
| Dynamic              | Yes             |
| SET_VAR Hint Applies | No              |
| Type                 | Integer         |
| Default Value        | 16384           |
| Minimum Value        | 1024            |
| Maximum Value        | 1048576         |
| Unit                 | bytes           |
| Block Size           | 1024            |

Each client thread is associated with a connection buffer and result buffer. Both begin with a size given by [net\\_buffer\\_length](#page-165-1) but are dynamically enlarged up to [max\\_allowed\\_packet](#page-151-0) bytes as needed. The result buffer shrinks to [net\\_buffer\\_length](#page-165-1) after each SQL statement.

This variable should not normally be changed, but if you have very little memory, you can set it to the expected length of statements sent by clients. If statements exceed this length, the connection buffer is automatically enlarged. The maximum value to which [net\\_buffer\\_length](#page-165-1) can be set is 1MB.

The session value of this variable is read only.

<span id="page-166-0"></span>• [net\\_read\\_timeout](#page-166-0)

| Command-Line Format  | net-read-timeout=# |
|----------------------|--------------------|
| System Variable      | net_read_timeout   |
| Scope                | Global, Session    |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Integer            |
| Default Value        | 30                 |
| Minimum Value        | 1                  |
| Maximum Value        | 31536000           |
| Unit                 | seconds            |

The number of seconds to wait for more data from a connection before aborting the read. When the server is reading from the client, [net\\_read\\_timeout](#page-166-0) is the timeout value controlling when to abort. When the server is writing to the client, [net\\_write\\_timeout](#page-167-0) is the timeout value controlling when to abort. See also replica\_net\_timeout and slave\_net\_timeout.

<span id="page-166-1"></span>• [net\\_retry\\_count](#page-166-1)

| Command-Line Format              | net-retry-count=#    |
|----------------------------------|----------------------|
| System Variable                  | net_retry_count      |
| Scope                            | Global, Session      |
| Dynamic                          | Yes                  |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value                    | 10                   |
| Minimum Value                    | 1                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |

If a read or write on a communication port is interrupted, retry this many times before giving up. This value should be set quite high on FreeBSD because internal interrupts are sent to all threads.

<span id="page-167-0"></span>• [net\\_write\\_timeout](#page-167-0)

| Command-Line Format  | net-write-timeout=# |
|----------------------|---------------------|
| System Variable      | net_write_timeout   |
| Scope                | Global, Session     |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |
| Type                 | Integer             |
| Default Value        | 60                  |
| Minimum Value        | 1                   |
| Maximum Value        | 31536000            |
| Unit                 | seconds             |

The number of seconds to wait for a block to be written to a connection before aborting the write. See also [net\\_read\\_timeout](#page-166-0).

<span id="page-167-1"></span>• [new](#page-167-1)

| Command-Line Format  | new[={OFF ON}]  |
|----------------------|-----------------|
| Deprecated           | Yes             |
| System Variable      | new             |
| Scope                | Global, Session |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | No              |
| Disabled by          | skip-new        |
| Type                 | Boolean         |
| Default Value        | OFF             |

This variable was used in MySQL 4.0 to turn on some 4.1 behaviors, and is retained for backward compatibility. Its value is always OFF.

This variable is deprecated as of MySQL 8.0.35, and is subject to removal in a future release.

In NDB Cluster, setting this variable to ON makes it possible to employ partitioning types other than KEY or LINEAR KEY with NDB tables. This experimental feature is not supported in production, and is now deprecated and thus subject to removal in a future release. For additional information, see User-defined partitioning and the NDB storage engine (NDB Cluster).

• [ngram\\_token\\_size](#page-167-2)

<span id="page-167-2"></span>

|     | Command-Line Format  | ngram-token-size=# |
|-----|----------------------|--------------------|
|     | System Variable      | ngram_token_size   |
|     | Scope                | Global             |
|     | Dynamic              | No                 |
| 938 | SET_VAR Hint Applies | No                 |

| Type          | Integer |
|---------------|---------|
| Default Value | 2       |
| Minimum Value | 1       |
| Maximum Value | 10      |

Defines the n-gram token size for the n-gram full-text parser. The ngram\_token\_size option is read-only and can only be modified at startup. The default value is 2 (bigram). The maximum value is 10.

For more information about how to configure this variable, see Section 14.9.8, "ngram Full-Text Parser".

<span id="page-168-0"></span>• [offline\\_mode](#page-168-0)

| Command-Line Format  | offline-mode[={OFF ON}] |
|----------------------|-------------------------|
| System Variable      | offline_mode            |
| Scope                | Global                  |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | Boolean                 |
| Default Value        | OFF                     |

In offline mode, the MySQL instance disconnects client users unless they have relevant privileges, and does not allow them to initiate new connections. Clients that are refused access receive an [ER\\_SERVER\\_OFFLINE\\_MODE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_server_offline_mode) error.

To put a server in offline mode, change the value of the [offline\\_mode](#page-168-0) system variable from OFF to ON. To resume normal operations, change [offline\\_mode](#page-168-0) from ON to OFF. To control offline mode, an administrator account must have the SYSTEM\_VARIABLES\_ADMIN privilege and the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege, which covers both these privileges). CONNECTION\_ADMIN is required from MySQL 8.0.31 and recommended in all releases to prevent accidental lockout.

Offline mode has these characteristics:

- Connected client users who do not have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege) are disconnected on the next request, with an appropriate error. Disconnection includes terminating running statements and releasing locks. Such clients also cannot initiate new connections, and receive an appropriate error.
- Connected client users who have the CONNECTION\_ADMIN or SUPER privilege are not disconnected, and can initiate new connections to manage the server.
- From MySQL 8.0.30, if the user that puts a server in offline mode does not have the SYSTEM\_USER privilege, connected client users who have the SYSTEM\_USER privilege are also not disconnected. However, these users cannot initiate new connections to the server while it is in offline mode, unless they have the CONNECTION\_ADMIN or SUPER privilege as well. It is only their existing connection that cannot be terminated, because the SYSTEM\_USER privilege is required to kill a session or statement that is executing with the SYSTEM\_USER privilege.
- Replication threads are permitted to keep applying data to the server.
- <span id="page-168-1"></span>• [old](#page-168-1)

| Command-Line Format | old[={OFF ON}] |
|---------------------|----------------|

| Deprecated           | Yes     |
|----------------------|---------|
| System Variable      | old     |
| Scope                | Global  |
| Dynamic              | No      |
| SET_VAR Hint Applies | No      |
| Type                 | Boolean |
| Default Value        | OFF     |

[old](#page-168-1) is a compatibility variable. It is disabled by default, but can be enabled at startup to revert the server to behaviors present in older versions.

When [old](#page-168-1) is enabled, it changes the default scope of index hints to that used prior to MySQL 5.1.17. That is, index hints with no FOR clause apply only to how indexes are used for row retrieval and not to resolution of ORDER BY or GROUP BY clauses. (See Section 10.9.4, "Index Hints".) Take care about enabling this in a replication setup. With statement-based binary logging, having different modes for the source and replicas might lead to replication errors.

This variable is deprecated as of MySQL 8.0.35, and is subject to removal in a future release.

## <span id="page-169-0"></span>• [old\\_alter\\_table](#page-169-0)

| Command-Line Format  | old-alter-table[={OFF ON}] |
|----------------------|----------------------------|
| System Variable      | old_alter_table            |
| Scope                | Global, Session            |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Boolean                    |
| Default Value        | OFF                        |

When this variable is enabled, the server does not use the optimized method of processing an ALTER TABLE operation. It reverts to using a temporary table, copying over the data, and then renaming the temporary table to the original, as used by MySQL 5.0 and earlier. For more information on the operation of ALTER TABLE, see Section 15.1.9, "ALTER TABLE Statement".

ALTER TABLE ... DROP PARTITION with [old\\_alter\\_table=ON](#page-169-0) rebuilds the partitioned table and attempts to move data from the dropped partition to another partition with a compatible PARTITION ... VALUES definition. Data that cannot be moved to another partition is deleted. In earlier releases, ALTER TABLE ... DROP PARTITION with [old\\_alter\\_table=ON](#page-169-0) deletes data stored in the partition and drops the partition.

## <span id="page-169-1"></span>• [open\\_files\\_limit](#page-169-1)

| Command-Line Format  | open-files-limit=#             |
|----------------------|--------------------------------|
| System Variable      | open_files_limit               |
| Scope                | Global                         |
| Dynamic              | No                             |
| SET_VAR Hint Applies | No                             |
| Type                 | Integer                        |
| Default Value        | 5000, with possible adjustment |
| Minimum Value        | 0                              |

| Maximum Value | platform dependent |
|---------------|--------------------|
|---------------|--------------------|

The number of file descriptors available to mysqld from the operating system:

- At startup, mysqld reserves descriptors with setrlimit(), using the value requested at by setting this variable directly or by using the --open-files-limit option to mysqld\_safe. If mysqld produces the error Too many open files, try increasing the [open\\_files\\_limit](#page-169-1) value. Internally, the maximum value for this variable is the maximum unsigned integer value, but the actual maximum is platform dependent.
- At runtime, the value of [open\\_files\\_limit](#page-169-1) indicates the number of file descriptors actually permitted to mysqld by the operating system, which might differ from the value requested at startup. If the number of file descriptors requested during startup cannot be allocated, mysqld writes a warning to the error log.

The effective [open\\_files\\_limit](#page-169-1) value is based on the value specified at system startup (if any) and the values of [max\\_connections](#page-152-1) and table\_open\_cache, using these formulas:

• 10 + max\_connections + (table\_open\_cache \* 2). Using the defaults for these variables yields 8161.

On Windows only, 2048 (the value of the C Run-Time Library file descriptor maximum) is added to this number. This totals 10209, again using the default values for the indicated system variables.

- max\_connections \* 5
- MySQL 8.0.19 and higher: The operating system limit.
- Prior to MySQL 8.0.19:
  - The operating system limit if that limit is positive but not Infinity.
  - If the operating system limit is Infinity: open\_files\_limit value if specified at startup, 5000 if not.

The server attempts to obtain the number of file descriptors using the maximum of those values, capped to the maximum unsigned integer value. If that many descriptors cannot be obtained, the server attempts to obtain as many as the system permits.

The effective value is 0 on systems where MySQL cannot change the number of open files.

On Unix, the value cannot be set greater than the value displayed by the ulimit -n command. On Linux systems using systemd, the value cannot be set greater than LimitNOFILE (this is DefaultLimitNOFILE, if LimitNOFILE is not set); otherwise, on Linux, the value of open\_files\_limit cannot exceed ulimit -n.

<span id="page-170-0"></span>• [optimizer\\_prune\\_level](#page-170-0)

| Command-Line Format  | optimizer-prune-level=# |
|----------------------|-------------------------|
| System Variable      | optimizer_prune_level   |
| Scope                | Global, Session         |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | Yes                     |
| Type                 | Integer                 |
| Default Value        | 1                       |
| Minimum Value        | 0                       |

| Maximum Value | 1 |
|---------------|---|
|---------------|---|

Controls the heuristics applied during query optimization to prune less-promising partial plans from the optimizer search space. A value of 0 disables heuristics so that the optimizer performs an exhaustive search. A value of 1 causes the optimizer to prune plans based on the number of rows retrieved by intermediate plans.

<span id="page-171-0"></span>• [optimizer\\_search\\_depth](#page-171-0)

| Command-Line Format  | optimizer-search-depth=# |
|----------------------|--------------------------|
| System Variable      | optimizer_search_depth   |
| Scope                | Global, Session          |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | Yes                      |
| Type                 | Integer                  |
| Default Value        | 62                       |
| Minimum Value        | 0                        |
| Maximum Value        | 62                       |

The maximum depth of search performed by the query optimizer. Values larger than the number of relations in a query result in better query plans, but take longer to generate an execution plan for a query. Values smaller than the number of relations in a query return an execution plan quicker, but the resulting plan may be far from being optimal. If set to 0, the system automatically picks a reasonable value.

<span id="page-171-1"></span>• [optimizer\\_switch](#page-171-1)

| Command-Line Format  | optimizer-switch=value              |
|----------------------|-------------------------------------|
| System Variable      | optimizer_switch                    |
| Scope                | Global, Session                     |
| Dynamic              | Yes                                 |
| SET_VAR Hint Applies | Yes                                 |
| Type                 | Set                                 |
| Valid Values         | batched_key_access={on off}         |
|                      | block_nested_loop={on off}          |
|                      | condition_fanout_filter={on off}    |
|                      | derived_condition_pushdown={on off} |
|                      | derived_merge={on off}              |
|                      | duplicateweedout={on off}           |
|                      | engine_condition_pushdown={on off}  |
|                      | firstmatch={on off}                 |
|                      | hash_join={on off}                  |
|                      | index_condition_pushdown={on off}   |
|                      | index_merge={on off}                |

```
index_merge_intersection={on|off}
index_merge_sort_union={on|off}
index_merge_union={on|off}
loosescan={on|off}
materialization={on|off}
mrr={on|off}
mrr_cost_based={on|off}
prefer_ordering_index={on|off}
semijoin={on|off}
skip_scan={on|off}
subquery_materialization_cost_based={on|
off}
subquery_to_derived={on|off}
use_index_extensions={on|off}
use_invisible_indexes={on|off}
```

The [optimizer\\_switch](#page-171-1) system variable enables control over optimizer behavior. The value of this variable is a set of flags, each of which has a value of on or off to indicate whether the corresponding optimizer behavior is enabled or disabled. This variable has global and session values and can be changed at runtime. The global default can be set at server startup.

To see the current set of optimizer flags, select the variable value:

```
mysql> SELECT @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,
 index_merge_sort_union=on,index_merge_intersection=on,
 engine_condition_pushdown=on,index_condition_pushdown=on,
 mrr=on,mrr_cost_based=on,block_nested_loop=on,
 batched_key_access=off,materialization=on,semijoin=on,
 loosescan=on,firstmatch=on,duplicateweedout=on,
 subquery_materialization_cost_based=on,
 use_index_extensions=on,condition_fanout_filter=on,
 derived_merge=on,use_invisible_indexes=off,skip_scan=on,
 hash_join=on,subquery_to_derived=off,
 prefer_ordering_index=on,hypergraph_optimizer=off,
 derived_condition_pushdown=on
```

For more information about the syntax of this variable and the optimizer behaviors that it controls, see Section 10.9.2, "Switchable Optimizations".

<span id="page-172-0"></span>• [optimizer\\_trace](#page-172-0)

| Command-Line Format  | optimizer-trace=value |
|----------------------|-----------------------|
| System Variable      | optimizer_trace       |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |

This variable controls optimizer tracing. For details, see Section 10.15, "Tracing the Optimizer".

<span id="page-173-0"></span>• [optimizer\\_trace\\_features](#page-173-0)

| Command-Line Format  | optimizer-trace-features=value |
|----------------------|--------------------------------|
| System Variable      | optimizer_trace_features       |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |
| Type                 | String                         |

This variable enables or disables selected optimizer tracing features. For details, see Section 10.15, "Tracing the Optimizer".

<span id="page-173-1"></span>• [optimizer\\_trace\\_limit](#page-173-1)

| Command-Line Format  | optimizer-trace-limit=# |
|----------------------|-------------------------|
| System Variable      | optimizer_trace_limit   |
| Scope                | Global, Session         |
| Dynamic              | Yes                     |
| SET_VAR Hint Applies | No                      |
| Type                 | Integer                 |
| Default Value        | 1                       |
| Minimum Value        | 0                       |
| Maximum Value        | 2147483647              |

The maximum number of optimizer traces to display. For details, see Section 10.15, "Tracing the Optimizer".

<span id="page-173-2"></span>• [optimizer\\_trace\\_max\\_mem\\_size](#page-173-2)

| Command-Line Format  | optimizer-trace-max-mem-size=# |
|----------------------|--------------------------------|
| System Variable      | optimizer_trace_max_mem_size   |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | Yes                            |
| Type                 | Integer                        |
| Default Value        | 1048576                        |
| Minimum Value        | 0                              |
| Maximum Value        | 4294967295                     |
| Unit                 | bytes                          |

The maximum cumulative size of stored optimizer traces. For details, see Section 10.15, "Tracing the Optimizer".

• [optimizer\\_trace\\_offset](#page-173-3)

<span id="page-173-3"></span>

|  |  | 944 |
|--|--|-----|
|--|--|-----|

| Command-Line Format | optimizer-trace-offset=# |
|---------------------|--------------------------|

| System Variable      | optimizer_trace_offset |
|----------------------|------------------------|
| Scope                | Global, Session        |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | Integer                |
| Default Value        | -1                     |
| Minimum Value        | -2147483647            |
| Maximum Value        | 2147483647             |

The offset of optimizer traces to display. For details, see Section 10.15, "Tracing the Optimizer".

• performance\_schema\_xxx

Performance Schema system variables are listed in Section 29.15, "Performance Schema System Variables". These variables may be used to configure Performance Schema operation.

<span id="page-174-0"></span>• [parser\\_max\\_mem\\_size](#page-174-0)

| Command-Line Format              | parser-max-mem-size=# |
|----------------------------------|-----------------------|
| System Variable                  | parser_max_mem_size   |
| Scope                            | Global, Session       |
| Dynamic                          | Yes                   |
| SET_VAR Hint Applies             | No                    |
| Type                             | Integer               |
| Default Value (64-bit platforms) | 18446744073709551615  |
| Default Value (32-bit platforms) | 4294967295            |
| Minimum Value                    | 10000000              |
| Maximum Value (64-bit platforms) | 18446744073709551615  |
| Maximum Value (32-bit platforms) | 4294967295            |
| Unit                             | bytes                 |

The maximum amount of memory available to the parser. The default value places no limit on memory available. The value can be reduced to protect against out-of-memory situations caused by parsing long or complex SQL statements.

## <span id="page-174-1"></span>• [partial\\_revokes](#page-174-1)

| Command-Line Format  | partial-revokes[={OFF ON}]            |
|----------------------|---------------------------------------|
| System Variable      | partial_revokes                       |
| Scope                | Global                                |
| Dynamic              | Yes                                   |
| SET_VAR Hint Applies | No                                    |
| Type                 | Boolean                               |
| Default Value        | OFF (if partial revokes do not exist) |
|                      | ON (if partial revokes exist)         |

Enabling this variable makes it possible to revoke privileges partially. Specifically, for users who have privileges at the global level, [partial\\_revokes](#page-174-1) enables privileges for specific schemas to be revoked while leaving the privileges in place for other schemas. For example, a user who has

the global UPDATE privilege can be restricted from exercising this privilege on the mysql system schema. (Or, stated another way, the user is enabled to exercise the UPDATE privilege on all schemas except the mysql schema.) In this sense, the user's global UPDATE privilege is partially revoked.

Once enabled, [partial\\_revokes](#page-174-1) cannot be disabled if any account has privilege restrictions. If any such account exists, disabling [partial\\_revokes](#page-174-1) fails:

- For attempts to disable [partial\\_revokes](#page-174-1) at startup, the server logs an error message and enables [partial\\_revokes](#page-174-1).
- For attempts to disable [partial\\_revokes](#page-174-1) at runtime, an error occurs and the [partial\\_revokes](#page-174-1) value remains unchanged.

To disable [partial\\_revokes](#page-174-1) in this case, first modify each account that has partially revoked privileges, either by re-granting the privileges or by removing the account.

![](_page_175_Picture_6.jpeg)

#### **Note**

In privilege assignments, enabling [partial\\_revokes](#page-174-1) causes MySQL to interpret occurrences of unescaped \_ and % SQL wildcard characters in schema names as literal characters, just as if they had been escaped as \\_ and \%. Because this changes how MySQL interprets privileges, it may be advisable to avoid unescaped wildcard characters in privilege assignments for installations where [partial\\_revokes](#page-174-1) may be enabled.

In addition, use of \_ and % as wildcard characters in grants is deprecated as of MySQL 8.0.35, and you should expect support for them to be removed in a future version of MySQL.

For more information, including instructions for removing partial revokes, see Section 8.2.12, "Privilege Restriction Using Partial Revokes".

<span id="page-175-0"></span>• [password\\_history](#page-175-0)

| Command-Line Format  | password-history=# |
|----------------------|--------------------|
| System Variable      | password_history   |
| Scope                | Global             |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Integer            |
| Default Value        | 0                  |
| Minimum Value        | 0                  |
| Maximum Value        | 4294967295         |

This variable defines the global policy for controlling reuse of previous passwords based on required minimum number of password changes. For an account password used previously, this variable indicates the number of subsequent account password changes that must occur before the password can be reused. If the value is 0 (the default), there is no reuse restriction based on number of password changes.

Changes to this variable apply immediately to all accounts defined with the PASSWORD HISTORY DEFAULT option.

The global number-of-changes password reuse policy can be overridden as desired for individual accounts using the PASSWORD HISTORY option of the CREATE USER and ALTER USER statements. See Section 8.2.15, "Password Management".

<span id="page-176-1"></span>• [password\\_require\\_current](#page-176-1)

| Command-Line Format  | password-require-current[={OFF <br>ON}] |
|----------------------|-----------------------------------------|
| System Variable      | password_require_current                |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Boolean                                 |
| Default Value        | OFF                                     |

This variable defines the global policy for controlling whether attempts to change an account password must specify the current password to be replaced.

Changes to this variable apply immediately to all accounts defined with the PASSWORD REQUIRE CURRENT DEFAULT option.

The global verification-required policy can be overridden as desired for individual accounts using the PASSWORD REQUIRE option of the CREATE USER and ALTER USER statements. See Section 8.2.15, "Password Management".

<span id="page-176-2"></span>• [password\\_reuse\\_interval](#page-176-2)

| Command-Line Format  | password-reuse-interval=# |
|----------------------|---------------------------|
| System Variable      | password_reuse_interval   |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |
| Default Value        | 0                         |
| Minimum Value        | 0                         |
| Maximum Value        | 4294967295                |
| Unit                 | days                      |

This variable defines the global policy for controlling reuse of previous passwords based on time elapsed. For an account password used previously, this variable indicates the number of days that must pass before the password can be reused. If the value is 0 (the default), there is no reuse restriction based on time elapsed.

Changes to this variable apply immediately to all accounts defined with the PASSWORD REUSE INTERVAL DEFAULT option.

The global time-elapsed password reuse policy can be overridden as desired for individual accounts using the PASSWORD REUSE INTERVAL option of the CREATE USER and ALTER USER statements. See Section 8.2.15, "Password Management".

<span id="page-176-0"></span>• [persisted\\_globals\\_load](#page-176-0)

| Command-Line Format | persisted-globals-load[={OFF ON}] |
|---------------------|-----------------------------------|
| System Variable     | persisted_globals_load            |
| Scope               | Global                            |
| Dynamic             | 947<br>No                         |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | Boolean |
| Default Value        | ON      |

Whether to load persisted configuration settings from the mysqld-auto.cnf file in the data directory. The server normally processes this file at startup after all other option files (see Section 6.2.2.2, "Using Option Files"). Disabling [persisted\\_globals\\_load](#page-176-0) causes the server startup sequence to skip mysqld-auto.cnf.

To modify the contents of mysqld-auto.cnf, use the SET PERSIST, SET PERSIST\_ONLY, and RESET PERSIST statements. See Section 7.1.9.3, "Persisted System Variables".

<span id="page-177-0"></span>• [persist\\_only\\_admin\\_x509\\_subject](#page-177-0)

| Command-Line Format  | persist-only-admin-x509-<br>subject=string |
|----------------------|--------------------------------------------|
| System Variable      | persist_only_admin_x509_subject            |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | String                                     |
| Default Value        | empty string                               |

SET PERSIST and SET PERSIST\_ONLY enable system variables to be persisted to the mysqldauto.cnf option file in the data directory (see Section 15.7.6.1, "SET Syntax for Variable Assignment"). Persisting system variables enables runtime configuration changes that affect subsequent server restarts, which is convenient for remote administration not requiring direct access to MySQL server host option files. However, some system variables are nonpersistible or can be persisted only under certain restrictive conditions.

The [persist\\_only\\_admin\\_x509\\_subject](#page-177-0) system variable specifies the SSL certificate X.509 Subject value that users must have to be able to persist system variables that are persist-restricted. The default value is the empty string, which disables the Subject check so that persist-restricted system variables cannot be persisted by any user.

If [persist\\_only\\_admin\\_x509\\_subject](#page-177-0) is nonempty, users who connect to the server using an encrypted connection and supply an SSL certificate with the designated Subject value then can use SET PERSIST\_ONLY to persist persist-restricted system variables. For information about persist-restricted system variables and instructions for configuring MySQL to enable [persist\\_only\\_admin\\_x509\\_subject](#page-177-0), see Section 7.1.9.4, "Nonpersistible and Persist-Restricted System Variables".

<span id="page-177-1"></span>• [persist\\_sensitive\\_variables\\_in\\_plaintext](#page-177-1)

| Command-Line Format  | <br>persist_sensitive_variables_in_plaintext[={OFF <br>ON}] |  |
|----------------------|-------------------------------------------------------------|--|
| System Variable      | persist_sensitive_variables_in_plaintext                    |  |
| Scope                | Global                                                      |  |
| Dynamic              | No                                                          |  |
| SET_VAR Hint Applies | No                                                          |  |
| Type                 | Boolean                                                     |  |

| Default Value | ON |  |
|---------------|----|--|
|---------------|----|--|

persist\_sensitive\_variables\_in\_plaintext controls whether the server is permitted to store the values of sensitive system variables in an unencrypted format, if keyring component support is not available at the time when SET PERSIST is used to set the value of the system variable. It also controls whether or not the server can start if the encrypted values cannot be decrypted. Note that keyring plugins do not support secure storage of sensitive system variables; a keyring component (see Section 8.4.4, "The MySQL Keyring") must be enabled on the MySQL Server instance to support secure storage.

The default setting, ON, encrypts the values if keyring component support is available, and persists them unencrypted (with a warning) if it is not. The next time any persisted system variable is set, if keyring support is available at that time, the server encrypts the values of any unencrypted sensitive system variables. The ON setting also allows the server to start if encrypted system variable values cannot be decrypted, in which case a warning is issued and the default values for the system variables are used. In that situation, their values cannot be changed until they can be decrypted.

The most secure setting, OFF, means sensitive system variable values cannot be persisted if keyring component support is unavailable. The OFF setting also means the server does not start if encrypted system variable values cannot be decrypted.

For more information, see Persisting Sensitive System Variables.

## <span id="page-178-0"></span>• [pid\\_file](#page-178-0)

| Command-Line Format  | pid-file=file_name |
|----------------------|--------------------|
| System Variable      | pid_file           |
| Scope                | Global             |
| Dynamic              | No                 |
| SET_VAR Hint Applies | No                 |
| Type                 | File name          |

The path name of the file in which the server writes its process ID. The server creates the file in the data directory unless an absolute path name is given to specify a different directory. If you specify this variable, you must specify a value. If you do not specify this variable, MySQL uses a default value of host\_name.pid, where host\_name is the name of the host machine.

The process ID file is used by other programs such as mysqld\_safe to determine the server's process ID. On Windows, this variable also affects the default error log file name. See Section 7.4.2, "The Error Log".

## <span id="page-178-1"></span>• [plugin\\_dir](#page-178-1)

| Command-Line Format  | plugin-dir=dir_name |
|----------------------|---------------------|
| System Variable      | plugin_dir          |
| Scope                | Global              |
| Dynamic              | No                  |
| SET_VAR Hint Applies | No                  |
| Type                 | Directory name      |
| Default Value        | BASEDIR/lib/plugin  |

The path name of the plugin directory.

If the plugin directory is writable by the server, it may be possible for a user to write executable code to a file in the directory using SELECT ... INTO DUMPFILE. This can be prevented by

making [plugin\\_dir](#page-178-1) read only to the server or by setting [secure\\_file\\_priv](#page-191-0) to a directory where SELECT writes can be made safely.

## <span id="page-179-2"></span>• [port](#page-179-2)

| Command-Line Format  | port=port_num |
|----------------------|---------------|
| System Variable      | port          |
| Scope                | Global        |
| Dynamic              | No            |
| SET_VAR Hint Applies | No            |
| Type                 | Integer       |
| Default Value        | 3306          |
| Minimum Value        | 0             |
| Maximum Value        | 65535         |

The number of the port on which the server listens for TCP/IP connections. This variable can be set with the [--port](#page-69-0) option.

## <span id="page-179-0"></span>• [preload\\_buffer\\_size](#page-179-0)

| Command-Line Format  | preload-buffer-size=# |
|----------------------|-----------------------|
| System Variable      | preload_buffer_size   |
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Integer               |
| Default Value        | 32768                 |
| Minimum Value        | 1024                  |
| Maximum Value        | 1073741824            |
| Unit                 | bytes                 |

The size of the buffer that is allocated when preloading indexes.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

## <span id="page-179-1"></span>• [print\\_identified\\_with\\_as\\_hex](#page-179-1)

| Command-Line Format  | print-identified-with-as<br>hex[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | print_identified_with_as_hex               |
| Scope                | Global, Session                            |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

environments. Enabling [print\\_identified\\_with\\_as\\_hex](#page-179-1) causes SHOW CREATE USER to display such hash values as hexadecimal strings rather than as regular string literals. Hash values that do not contain unprintable characters still display as regular string literals, even with this variable enabled.

## <span id="page-180-0"></span>• [profiling](#page-180-0)

If set to 0 or OFF (the default), statement profiling is disabled. If set to 1 or ON, statement profiling is enabled and the SHOW PROFILE and SHOW PROFILES statements provide access to profiling information. See Section 15.7.7.31, "SHOW PROFILES Statement".

This variable is deprecated; expect it to be removed in a future MySQL release.

## <span id="page-180-1"></span>• [profiling\\_history\\_size](#page-180-1)

The number of statements for which to maintain profiling information if [profiling](#page-180-0) is enabled. The default value is 15. The maximum value is 100. Setting the value to 0 effectively disables profiling. See Section 15.7.7.31, "SHOW PROFILES Statement".

This variable is deprecated; expect it to be removed in a future MySQL release.

## <span id="page-180-2"></span>• [protocol\\_compression\\_algorithms](#page-180-2)

| Command-Line Format  | protocol-compression<br>algorithms=value |
|----------------------|------------------------------------------|
| System Variable      | protocol_compression_algorithms          |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | Set                                      |
| Default Value        | zlib,zstd,uncompressed                   |
| Valid Values         | zlib                                     |
|                      | zstd                                     |
|                      | uncompressed                             |

The compression algorithms that the server permits for incoming connections. These include connections by client programs and by servers participating in source/replica replication or Group Replication. Compression does not apply to connections for FEDERATED tables.

[protocol\\_compression\\_algorithms](#page-180-2) does not control connection compression for X Protocol. See Section 22.5.5, "Connection Compression with X Plugin" for information on how this operates.

The variable value is a list of one or more comma-separated compression algorithm names, in any order, chosen from the following items (not case-sensitive):

- zlib: Permit connections that use the zlib compression algorithm.
- zstd: Permit connections that use the zstd compression algorithm.
- uncompressed: Permit uncompressed connections. If this algorithm name is not included in the [protocol\\_compression\\_algorithms](#page-180-2) value, the server does not permit uncompressed connections. It permits only compressed connections that use whichever other algorithms are specified in the value, and there is no fallback to uncompressed connections.

The default value of zlib,zstd,uncompressed indicates that the server permits all compression algorithms.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-181-0"></span>• [protocol\\_version](#page-181-0)

| System Variable      | protocol_version |
|----------------------|------------------|
| Scope                | Global           |
| Dynamic              | No               |
| SET_VAR Hint Applies | No               |
| Type                 | Integer          |
| Default Value        | 10               |
| Minimum Value        | 0                |
| Maximum Value        | 4294967295       |

The version of the client/server protocol used by the MySQL server.

<span id="page-181-1"></span>• [proxy\\_user](#page-181-1)

| System Variable      | proxy_user |
|----------------------|------------|
| Scope                | Session    |
| Dynamic              | No         |
| SET_VAR Hint Applies | No         |
| Type                 | String     |

If the current client is a proxy for another user, this variable is the proxy user account name. Otherwise, this variable is NULL. See Section 8.2.19, "Proxy Users".

<span id="page-181-2"></span>• [pseudo\\_replica\\_mode](#page-181-2)

| System Variable      | pseudo_replica_mode |
|----------------------|---------------------|
| Scope                | Session             |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |
| Type                 | Boolean             |

From MySQL 8.0.26, [pseudo\\_replica\\_mode](#page-181-2) is used in place of [pseudo\\_slave\\_mode](#page-182-0), which is deprecated from that release. The operation and effects are the same, only the terminology has changed.

[pseudo\\_replica\\_mode](#page-181-2) is for internal server use. It assists with the correct handling of transactions that originated on older or newer servers than the server currently processing them. mysqlbinlog sets the value of [pseudo\\_replica\\_mode](#page-181-2) to true before executing any SQL statements.

Setting the session value of [pseudo\\_replica\\_mode](#page-181-2) is a restricted operation. The session user must have either the REPLICATION\_APPLIER privilege (see Section 19.3.3, "Replication Privilege Checks"), or privileges sufficient to set restricted session variables (see Section 7.1.9.1, "System

Variable Privileges"). However, note that the variable is not intended for users to set; it is set automatically by the replication infrastructure.

[pseudo\\_replica\\_mode](#page-181-2) has the following effects on the handling of prepared XA transactions, which can be attached to or detached from the handling session (by default, the session that issues XA START):

- If true, and the handling session has executed an internal-use BINLOG statement, XA transactions are automatically detached from the session as soon as the first part of the transaction up to XA PREPARE finishes, so they can be committed or rolled back by any session that has the XA\_RECOVER\_ADMIN privilege.
- If false, XA transactions remain attached to the handling session as long as that session is alive, during which time no other session can commit the transaction. The prepared transaction is only detached if the session disconnects or the server restarts.

[pseudo\\_replica\\_mode](#page-181-2) has the following effects on the original\_commit\_timestamp replication delay timestamp and the original\_server\_version system variable:

- If true, transactions that do not explicitly set original\_commit\_timestamp or original\_server\_version are assumed to originate on another, unknown server, so the value 0, meaning unknown, is assigned to both the timestamp and the system variable.
- If false, transactions that do not explicitly set original\_commit\_timestamp or original\_server\_version are assumed to originate on the current server, so the current timestamp and the current server's version are assigned to the timestamp and the system variable.

In MySQL 8.0.14 and later, [pseudo\\_replica\\_mode](#page-181-2) has the following effects on the handling of a statement that sets one or more unsupported (removed or unknown) SQL modes:

- If true, the server ignores the unsupported mode and raises a warning.
- If false, the server rejects the statement with [ER\\_UNSUPPORTED\\_SQL\\_MODE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_unsupported_sql_mode).
- <span id="page-182-0"></span>• [pseudo\\_slave\\_mode](#page-182-0)

| Deprecated           | Yes               |
|----------------------|-------------------|
| System Variable      | pseudo_slave_mode |
| Scope                | Session           |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | Boolean           |

From MySQL 8.0.26, [pseudo\\_slave\\_mode](#page-182-0) is deprecated and the alias [pseudo\\_replica\\_mode](#page-181-2) is used instead. [pseudo\\_slave\\_mode](#page-182-0) is for internal server use. It assists with the correct handling of transactions that originated on older or newer servers than the server currently processing them. mysqlbinlog sets the value of [pseudo\\_slave\\_mode](#page-182-0) to true before executing any SQL statements.

Setting the session value of this system variable is a restricted operation. The session user must have either the REPLICATION\_APPLIER privilege (see Section 19.3.3, "Replication Privilege Checks"), or privileges sufficient to set restricted session variables (see Section 7.1.9.1, "System Variable Privileges"). However, note that the variable is not intended for users to set; it is set automatically by the replication infrastructure.

See the description of the [pseudo\\_replica\\_mode](#page-181-2) system variable for the effects of [pseudo\\_slave\\_mode](#page-182-0).

<span id="page-183-0"></span>• pseudo thread id

| System Variable      | pseudo_thread_id |
|----------------------|------------------|
| Scope                | Session          |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Туре                 | Integer          |
| Default Value        | 2147483647       |
| Minimum Value        | 0                |
| Maximum Value        | 2147483647       |

This variable is for internal server use.

![](_page_183_Picture_4.jpeg)

## Warning

Changing the session value of the <code>pseudo\_thread\_id</code> system variable changes the value returned by the <code>CONNECTION ID()</code> function.

As of MySQL 8.0.14, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-183-1"></span>• query alloc block size

| Command-Line Format  | query-alloc-block-size=# |
|----------------------|--------------------------|
| System Variable      | query_alloc_block_size   |
| Scope                | Global, Session          |
| Dynamic              | Yes                      |
| SET_VAR Hint Applies | No                       |
| Туре                 | Integer                  |
| Default Value        | 8192                     |
| Minimum Value        | 1024                     |
| Maximum Value        | 4294966272               |
| Unit                 | bytes                    |
| Block Size           | 1024                     |

The allocation size in bytes of memory blocks that are allocated for objects created during statement parsing and execution. If you have problems with memory fragmentation, it might help to increase this parameter.

The block size for the byte number is 1024. A value that is not an exact multiple of the block size is rounded down to the next lower multiple of the block size by MySQL Server before storing the value for the system variable. The parser allows values up to the maximum unsigned integer value for the platform (4294967295 or 2<sup>32</sup>–1 for a 32-bit system, 18446744073709551615 or 2<sup>64</sup>–1 for a 64-bit system) but the actual maximum is a block size lower.

<span id="page-183-2"></span>• query prealloc size

| Command-Line Format | query-prealloc-size=# |
|---------------------|-----------------------|
| Deprecated          | Yes                   |
| System Variable     | query_prealloc_size   |

| Scope                            | Global, Session      |
|----------------------------------|----------------------|
| Dynamic                          | Yes                  |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value                    | 8192                 |
| Minimum Value                    | 8192                 |
| Maximum Value (64-bit platforms) | 18446744073709550592 |
| Maximum Value (32-bit platforms) | 4294966272           |
| Unit                             | bytes                |
| Block Size                       | 1024                 |

MySQL 8.0.28 and earlier: This sets the size in bytes of the persistent buffer used for statement parsing and execution. This buffer is not freed between statements. If you are running complex queries, a larger query\_prealloc\_size value might be helpful in improving performance, because it can reduce the need for the server to perform memory allocation during query execution operations. You should be aware that doing this does not necessarily eliminate allocation completely; the server may still allocate memory in some situations, such as for operations relating to transactions, or to stored programs.

As of MySQL 8.0.29, query\_prealloc\_size is deprecated, and setting it no longer has any effect; you should expect its removal in a future release of MySQL.

## <span id="page-184-0"></span>• [rand\\_seed1](#page-184-0)

| System Variable      | rand_seed1 |
|----------------------|------------|
| Scope                | Session    |
| Dynamic              | Yes        |
| SET_VAR Hint Applies | No         |
| Type                 | Integer    |
| Default Value        | N/A        |
| Minimum Value        | 0          |
| Maximum Value        | 4294967295 |

The [rand\\_seed1](#page-184-0) and [rand\\_seed2](#page-184-1) variables exist as session variables only, and can be set but not read. The variables—but not their values—are shown in the output of SHOW VARIABLES.

The purpose of these variables is to support replication of the RAND() function. For statements that invoke RAND(), the source passes two values to the replica, where they are used to seed the random number generator. The replica uses these values to set the session variables [rand\\_seed1](#page-184-0) and [rand\\_seed2](#page-184-1) so that RAND() on the replica generates the same value as on the source.

<span id="page-184-1"></span>• [rand\\_seed2](#page-184-1)

See the description for [rand\\_seed1](#page-184-0).

<span id="page-184-2"></span>• [range\\_alloc\\_block\\_size](#page-184-2)

| Command-Line Format | range-alloc-block-size=# |
|---------------------|--------------------------|
| System Variable     | range_alloc_block_size   |
| Scope               | Global, Session          |
| Dynamic             | Yes                      |

| SET_VAR Hint Applies             | Yes                  |
|----------------------------------|----------------------|
| Туре                             | Integer              |
| Default Value                    | 4096                 |
| Minimum Value                    | 4096                 |
| Maximum Value (64-bit platforms) | 18446744073709550592 |
| Maximum Value                    | 4294966272           |
| Unit                             | bytes                |
| Block Size                       | 1024                 |

The size in bytes of blocks that are allocated when doing range optimization.

The block size for the byte number is 1024. A value that is not an exact multiple of the block size is rounded down to the next lower multiple of the block size by MySQL Server before storing the value for the system variable. The parser allows values up to the maximum unsigned integer value for the platform (4294967295 or 2<sup>32</sup>-1 for a 32-bit system, 18446744073709551615 or 2<sup>64</sup>-1 for a 64-bit system) but the actual maximum is a block size lower.

<span id="page-185-0"></span>• range optimizer max mem size

| Command-Line Format  | range-optimizer-max-mem-size=# |
|----------------------|--------------------------------|
| System Variable      | range_optimizer_max_mem_size   |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | Yes                            |
| Туре                 | Integer                        |
| Default Value        | 8388608                        |
| Minimum Value        | 0                              |
| Maximum Value        | 18446744073709551615           |
| Unit                 | bytes                          |

The limit on memory consumption for the range optimizer. A value of 0 means "no limit." If an execution plan considered by the optimizer uses the range access method but the optimizer estimates that the amount of memory needed for this method would exceed the limit, it abandons the plan and considers other plans. For more information, see Limiting Memory Use for Range Optimization.

<span id="page-185-1"></span>• rbr exec mode

| System Variable      | rbr_exec_mode |
|----------------------|---------------|
| Scope                | Session       |
| Dynamic              | Yes           |
| SET_VAR Hint Applies | No            |
| Туре                 | Enumeration   |
| Default Value        | STRICT        |
| Valid Values         | STRICT        |
|                      | IDEMPOTENT    |

For internal use by mysqlbinlog. This variable switches the server between IDEMPOTENT mode and STRICT mode. IDEMPOTENT mode causes suppression of duplicate-key and no-key-found

errors in BINLOG statements generated by mysqlbinlog. This mode is useful when replaying a row-based binary log on a server that causes conflicts with existing data. mysqlbinlog sets this mode when you specify the --idempotent option by writing the following to the output:

```
SET SESSION RBR_EXEC_MODE=IDEMPOTENT;
```

As of MySQL 8.0.18, setting the session value of this system variable is no longer a restricted operation.

<span id="page-186-0"></span>• [read\\_buffer\\_size](#page-186-0)

| Command-Line Format  | read-buffer-size=# |
|----------------------|--------------------|
| System Variable      | read_buffer_size   |
| Scope                | Global, Session    |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | Yes                |
| Type                 | Integer            |
| Default Value        | 131072             |
| Minimum Value        | 8192               |
| Maximum Value        | 2147479552         |
| Unit                 | bytes              |
| Block Size           | 4096               |

Each thread that does a sequential scan for a MyISAM table allocates a buffer of this size (in bytes) for each table it scans. If you do many sequential scans, you might want to increase this value, which defaults to 131072. The value of this variable should be a multiple of 4KB. If it is set to a value that is not a multiple of 4KB, its value is rounded down to the nearest multiple of 4KB.

This option is also used in the following context for all other storage engines with the exception of InnoDB:

- For caching the indexes in a temporary file (not a temporary table), when sorting rows for ORDER BY.
- For bulk insert into partitions.
- For caching results of nested queries.

[read\\_buffer\\_size](#page-186-0) is also used in one other storage engine-specific way: to determine the memory block size for MEMORY tables.

Beginning with MySQL 8.0.22, the value of [select\\_into\\_buffer\\_size](#page-192-0) is used in place of the value of read\_buffer\_size for the I/O cache buffer used when executing SELECT INTO DUMPFILE and SELECT INTO OUTFILE statements. (read\_buffer\_size is used for the I/O cache buffer size in all other cases.)

For more information about memory use during different operations, see Section 10.12.3.1, "How MySQL Uses Memory".

<span id="page-186-1"></span>• [read\\_only](#page-186-1)

| Command-Line Format | read-only[={OFF ON}] |
|---------------------|----------------------|
| System Variable     | read_only            |
| Scope               | Global               |
| Dynamic             | Yes<br>957           |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | Boolean |
| Default Value        | OFF     |

If the [read\\_only](#page-186-1) system variable is enabled, the server permits no client updates except from users who have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). This variable is disabled by default.

The server also supports a super\_read\_only system variable (disabled by default), which has these effects:

- If super\_read\_only is enabled, the server prohibits client updates, even from users who have the CONNECTION\_ADMIN or SUPER privilege.
- Setting super\_read\_only to ON implicitly forces [read\\_only](#page-186-1) to ON.
- Setting [read\\_only](#page-186-1) to OFF implicitly forces super\_read\_only to OFF.

When [read\\_only](#page-186-1) is enabled and when super\_read\_only is enabled, the server still permits these operations:

- Updates performed by replication threads, if the server is a replica. In replication setups, it can be useful to enable [read\\_only](#page-186-1) on replica servers to ensure that replicas accept updates only from the source server and not from clients.
- Writes to the system table mysql.gtid\_executed, which stores GTIDs for executed transactions that are not present in the current binary log file.
- Use of ANALYZE TABLE or OPTIMIZE TABLE statements. The purpose of read-only mode is to prevent changes to table structure or contents. Analysis and optimization do not qualify as such changes. This means, for example, that consistency checks on read-only replicas can be performed with mysqlcheck --all-databases --analyze.
- Use of FLUSH STATUS statements, which are always written to the binary log.
- Operations on TEMPORARY tables.
- Inserts into the log tables (mysql.general\_log and mysql.slow\_log); see Section 7.4.1, "Selecting General Query Log and Slow Query Log Output Destinations".
- Updates to Performance Schema tables, such as UPDATE or TRUNCATE TABLE operations.

Changes to [read\\_only](#page-186-1) on a replication source server are not replicated to replica servers. The value can be set on a replica independent of the setting on the source.

The following conditions apply to attempts to enable [read\\_only](#page-186-1) (including implicit attempts resulting from enabling super\_read\_only):

- The attempt fails and an error occurs if you have any explicit locks (acquired with LOCK TABLES) or have a pending transaction.
- The attempt blocks while other clients have any ongoing statement, active LOCK TABLES WRITE, or ongoing commit, until the locks are released and the statements and transactions end. While the attempt to enable [read\\_only](#page-186-1) is pending, requests by other clients for table locks or to begin transactions also block until [read\\_only](#page-186-1) has been set.
- The attempt blocks if there are active transactions that hold metadata locks, until those transactions end.

- [read\\_only](#page-186-1) can be enabled while you hold a global read lock (acquired with FLUSH TABLES WITH READ LOCK) because that does not involve table locks.
- <span id="page-188-0"></span>• [read\\_rnd\\_buffer\\_size](#page-188-0)

| Command-Line Format  | read-rnd-buffer-size=# |
|----------------------|------------------------|
| System Variable      | read_rnd_buffer_size   |
| Scope                | Global, Session        |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | Yes                    |
| Type                 | Integer                |
| Default Value        | 262144                 |
| Minimum Value        | 1                      |
| Maximum Value        | 2147483647             |
| Unit                 | bytes                  |

This variable is used for reads from MyISAM tables, and, for any storage engine, for Multi-Range Read optimization.

When reading rows from a MyISAM table in sorted order following a key-sorting operation, the rows are read through this buffer to avoid disk seeks. See Section 10.2.1.16, "ORDER BY Optimization". Setting the variable to a large value can improve ORDER BY performance by a lot. However, this is a buffer allocated for each client, so you should not set the global variable to a large value. Instead, change the session variable only from within those clients that need to run large queries.

For more information about memory use during different operations, see Section 10.12.3.1, "How MySQL Uses Memory". For information about Multi-Range Read optimization, see Section 10.2.1.11, "Multi-Range Read Optimization".

<span id="page-188-1"></span>• [regexp\\_stack\\_limit](#page-188-1)

| Command-Line Format  | regexp-stack-limit=# |
|----------------------|----------------------|
| System Variable      | regexp_stack_limit   |
| Scope                | Global               |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | Integer              |
| Default Value        | 8000000              |
| Minimum Value        | 0                    |
| Maximum Value        | 2147483647           |
| Unit                 | bytes                |

The maximum available memory in bytes for the internal stack used for regular expression matching operations performed by REGEXP\_LIKE() and similar functions (see Section 14.8.2, "Regular Expressions").

<span id="page-188-2"></span>• [regexp\\_time\\_limit](#page-188-2)

| Command-Line Format | regexp-time-limit=# |
|---------------------|---------------------|
| System Variable     | regexp_time_limit   |

| Scope                | Global     |
|----------------------|------------|
| Dynamic              | Yes        |
| SET_VAR Hint Applies | No         |
| Type                 | Integer    |
| Default Value        | 32         |
| Minimum Value        | 0          |
| Maximum Value        | 2147483647 |

The time limit for regular expression matching operations performed by REGEXP\_LIKE() and similar functions (see Section 14.8.2, "Regular Expressions"). This limit is expressed as the maximum permitted number of steps performed by the match engine, and thus affects execution time only indirectly. Typically, it is on the order of milliseconds.

<span id="page-189-0"></span>• [require\\_row\\_format](#page-189-0)

| System Variable      | require_row_format |
|----------------------|--------------------|
| Scope                | Session            |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Boolean            |
| Default Value        | OFF                |

This variable is for internal server use by replication and mysqlbinlog. It restricts DML events executed in the session to events encoded in row-based binary logging format only, and temporary tables cannot be created. Queries that do not respect the restrictions fail.

Setting the session value of this system variable to ON requires no privileges. Setting the session value of this system variable to OFF is a restricted operation, and the session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-189-1"></span>• [require\\_secure\\_transport](#page-189-1)

| Command-Line Format  | require-secure-transport[={OFF <br>ON}] |
|----------------------|-----------------------------------------|
| System Variable      | require_secure_transport                |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Boolean                                 |
| Default Value        | OFF                                     |

Whether client connections to the server are required to use some form of secure transport. When this variable is enabled, the server permits only TCP/IP connections encrypted using TLS/SSL, or

connections that use a socket file (on Unix) or shared memory (on Windows). The server rejects nonsecure connection attempts, which fail with an [ER\\_SECURE\\_TRANSPORT\\_REQUIRED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_secure_transport_required) error.

This capability supplements per-account SSL requirements, which take precedence. For example, if an account is defined with REQUIRE SSL, enabling [require\\_secure\\_transport](#page-189-1) does not make it possible to use the account to connect using a Unix socket file.

It is possible for a server to have no secure transports available. For example, a server on Windows supports no secure transports if started without specifying any SSL certificate or key files and with the [shared\\_memory](#page-198-1) system variable disabled. Under these conditions, attempts to enable [require\\_secure\\_transport](#page-189-1) at startup cause the server to write a message to the error log and exit. Attempts to enable the variable at runtime fail with an [ER\\_NO\\_SECURE\\_TRANSPORTS\\_CONFIGURED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_no_secure_transports_configured) error.

All replication group members should have the same value for this variable; otherwise, some members may not be able to join.

See also Configuring Encrypted Connections as Mandatory.

<span id="page-190-0"></span>• [resultset\\_metadata](#page-190-0)

| System Variable      | resultset_metadata |
|----------------------|--------------------|
| Scope                | Session            |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Enumeration        |
| Default Value        | FULL               |
| Valid Values         | FULL               |
|                      | NONE               |

For connections for which metadata transfer is optional, the client sets the [resultset\\_metadata](#page-190-0) system variable to control whether the server returns result set metadata. Permitted values are FULL (return all metadata; this is the default) and NONE (return no metadata).

For connections that are not metadata-optional, setting [resultset\\_metadata](#page-190-0) to NONE produces an error.

For details about managing result set metadata transfer, see [Optional Result Set Metadata.](https://dev.mysql.com/doc/c-api/8.0/en/c-api-optional-metadata.md)

• [secondary\\_engine\\_cost\\_threshold](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_secondary_engine_cost_threshold)

For use with MySQL HeatWave only. See [System Variables](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md), for more information.

<span id="page-190-1"></span>• [schema\\_definition\\_cache](#page-190-1)

| Command-Line Format  | schema-definition-cache=# |
|----------------------|---------------------------|
| System Variable      | schema_definition_cache   |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |
| Default Value        | 256                       |
| Minimum Value        | 256                       |
|                      |                           |

| Maximum Value | 524288 |
|---------------|--------|
|---------------|--------|

Defines a limit for the number of schema definition objects, both used and unused, that can be kept in the dictionary object cache.

Unused schema definition objects are only kept in the dictionary object cache when the number in use is less than the capacity defined by schema\_definition\_cache.

A setting of 0 means that schema definition objects are only kept in the dictionary object cache while they are in use.

For more information, see Section 16.4, "Dictionary Object Cache".

<span id="page-191-0"></span>• [secure\\_file\\_priv](#page-191-0)

| Command-Line Format  | secure-file-priv=dir_name |
|----------------------|---------------------------|
| System Variable      | secure_file_priv          |
| Scope                | Global                    |
| Dynamic              | No                        |
| SET_VAR Hint Applies | No                        |
| Type                 | String                    |
| Default Value        | platform specific         |
| Valid Values         | empty string              |
|                      | dirname                   |
|                      | NULL                      |

This variable is used to limit the effect of data import and export operations, such as those performed by the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD\_FILE() function. These operations are permitted only to users who have the FILE privilege.

[secure\\_file\\_priv](#page-191-0) may be set as follows:

- If empty, the variable has no effect. This is not a secure setting.
- If set to the name of a directory, the server limits import and export operations to work only with files in that directory. The directory must exist; the server does not create it.
- If set to NULL, the server disables import and export operations.

The default value is platform specific and depends on the value of the INSTALL\_LAYOUT CMake option, as shown in the following table. To specify the default [secure\\_file\\_priv](#page-191-0) value explicitly if you are building from source, use the INSTALL\_SECURE\_FILE\_PRIVDIR CMake option.

| INSTALL_LAYOUT Value | Default secure_file_priv Value                      |
|----------------------|-----------------------------------------------------|
| STANDALONE           | empty                                               |
| DEB, RPM, SVR4       | /var/lib/mysql-files                                |
| Otherwise            | mysql-files under the<br>CMAKE_INSTALL_PREFIX value |

The server checks the value of [secure\\_file\\_priv](#page-191-0) at startup and writes a warning to the error log if the value is insecure. A non-NULL value is considered insecure if it is empty, or the value is the data directory or a subdirectory of it, or a directory that is accessible by all users. If [secure\\_file\\_priv](#page-191-0) is set to a nonexistent path, the server writes an error message to the error log and exits.

<span id="page-192-0"></span>• [select\\_into\\_buffer\\_size](#page-192-0)

| Command-Line Format  | select-into-buffer-size=# |
|----------------------|---------------------------|
| System Variable      | select_into_buffer_size   |
| Scope                | Global, Session           |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | Yes                       |
| Type                 | Integer                   |
| Default Value        | 131072                    |
| Minimum Value        | 8192                      |
| Maximum Value        | 2147479552                |
| Unit                 | bytes                     |
| Block Size           | 4096                      |

When using SELECT INTO OUTFILE or SELECT INTO DUMPFILE to dump data into one or more files for backup creation, data migration, or other purposes, writes can often be buffered and then trigger a large burst of write I/O activity to the disk or other storage device and stall other queries that are more sensitive to latency. You can use this variable to control the size of the buffer used to write data to the storage device to determine when buffer synchronization should occur, and thus to prevent write stalls of the kind just described from occurring.

select\_into\_buffer\_size overrides any value set for [read\\_buffer\\_size](#page-186-0). (select\_into\_buffer\_size and read\_buffer\_size have the same default, maximum, and minimum values.) You can also use [select\\_into\\_disk\\_sync\\_delay](#page-192-2) to set a timeout to be observed afterwards, each time synchronization takes place.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-192-1"></span>• [select\\_into\\_disk\\_sync](#page-192-1)

| Command-Line Format  | select-into-disk-sync={ON OFF} |
|----------------------|--------------------------------|
| System Variable      | select_into_disk_sync          |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | Yes                            |
| Type                 | Boolean                        |
| Default Value        | OFF                            |
| Valid Values         | OFF                            |
|                      | ON                             |

When set on ON, enables buffer synchronization of writes to an output file by a long-running SELECT INTO OUTFILE or SELECT INTO DUMPFILE statement using [select\\_into\\_buffer\\_size](#page-192-0).

<span id="page-192-2"></span>• [select\\_into\\_disk\\_sync\\_delay](#page-192-2)

| Command-Line Format | select-into-disk-sync-delay=# |
|---------------------|-------------------------------|
| System Variable     | select_into_disk_sync_delay   |
| Scope               | Global, Session<br>963        |

| Dynamic              | Yes          |
|----------------------|--------------|
| SET_VAR Hint Applies | Yes          |
| Type                 | Integer      |
| Default Value        | 0            |
| Minimum Value        | 0            |
| Maximum Value        | 31536000     |
| Unit                 | milliseconds |

When buffer synchronization of writes to an output file by a long-running SELECT INTO OUTFILE or SELECT INTO DUMPFILE statement is enabled by [select\\_into\\_disk\\_sync](#page-192-1), this variable sets an optional delay (in milliseconds) following synchronization. 0 (the default) means no delay.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

<span id="page-193-0"></span>• [session\\_track\\_gtids](#page-193-0)

| Command-Line Format  | session-track-gtids=value |
|----------------------|---------------------------|
| System Variable      | session_track_gtids       |
| Scope                | Global, Session           |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Enumeration               |
| Default Value        | OFF                       |
| Valid Values         | OFF                       |
|                      | OWN_GTID                  |
|                      | ALL_GTIDS                 |

Controls whether the server returns GTIDs to the client, enabling the client to use them to track the server state. Depending on the variable value, at the end of executing each transaction, the server's GTIDs are captured and returned to the client as part of the acknowledgement. The possible values for [session\\_track\\_gtids](#page-193-0) are as follows:

- OFF: The server does not return GTIDs to the client. This is the default.
- OWN\_GTID: The server returns the GTIDs for all transactions that were successfully committed by this client in its current session since the last acknowledgement. Typically, this is the single GTID for the last transaction committed, but if a single client request resulted in multiple transactions, the server returns a GTID set containing all the relevant GTIDs.
- ALL\_GTIDS: The server returns the global value of its gtid\_executed system variable, which it reads at a point after the transaction is successfully committed. As well as the GTID for the transaction just committed, this GTID set includes all transactions committed on the server by any client, and can include transactions committed after the point when the transaction currently being acknowledged was committed.

[session\\_track\\_gtids](#page-193-0) cannot be set within transactional context.

For more information about session state tracking, see Section 7.1.18, "Server Tracking of Client Session State".

<span id="page-193-1"></span>• [session\\_track\\_schema](#page-193-1)

| Command-Line Format  | session-track-schema[={OFF ON}] |
|----------------------|---------------------------------|
| System Variable      | session_track_schema            |
| Scope                | Global, Session                 |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |
| Default Value        | ON                              |

Controls whether the server tracks when the default schema (database) is set within the current session and notifies the client to make the schema name available.

If the schema name tracker is enabled, name notification occurs each time the default schema is set, even if the new schema name is the same as the old.

For more information about session state tracking, see Section 7.1.18, "Server Tracking of Client Session State".

<span id="page-194-0"></span>• [session\\_track\\_state\\_change](#page-194-0)

| Command-Line Format  | session-track-state-change[={OFF <br>ON}] |
|----------------------|-------------------------------------------|
| System Variable      | session_track_state_change                |
| Scope                | Global, Session                           |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | Boolean                                   |
| Default Value        | OFF                                       |

Controls whether the server tracks changes to the state of the current session and notifies the client when state changes occur. Changes can be reported for these attributes of client session state:

- The default schema (database).
- Session-specific values for system variables.
- User-defined variables.
- Temporary tables.
- Prepared statements.

If the session state tracker is enabled, notification occurs for each change that involves tracked session attributes, even if the new attribute values are the same as the old. For example, setting a user-defined variable to its current value results in a notification.

The [session\\_track\\_state\\_change](#page-194-0) variable controls only notification of when changes occur, not what the changes are. For example, state-change notifications occur when the default schema is set or tracked session system variables are assigned, but the notification does not include the schema name or variable values. To receive notification of the schema name or session system

variable values, use the [session\\_track\\_schema](#page-193-1) or [session\\_track\\_system\\_variables](#page-195-0) system variable, respectively.

![](_page_195_Picture_2.jpeg)

#### **Note**

Assigning a value to [session\\_track\\_state\\_change](#page-194-0) itself is not considered a state change and is not reported as such. However, if its name listed in the value of [session\\_track\\_system\\_variables](#page-195-0), any assignments to it do result in notification of the new value.

For more information about session state tracking, see Section 7.1.18, "Server Tracking of Client Session State".

<span id="page-195-0"></span>• [session\\_track\\_system\\_variables](#page-195-0)

| Command-Line Format  | session-track-system-variables=#                                                                      |
|----------------------|-------------------------------------------------------------------------------------------------------|
| System Variable      | session_track_system_variables                                                                        |
| Scope                | Global, Session                                                                                       |
| Dynamic              | Yes                                                                                                   |
| SET_VAR Hint Applies | No                                                                                                    |
| Type                 | String                                                                                                |
| Default Value        | time_zone, autocommit,<br>character_set_client,<br>character_set_results,<br>character_set_connection |

Controls whether the server tracks assignments to session system variables and notifies the client of the name and value of each assigned variable. The variable value is a commaseparated list of variables for which to track assignments. By default, notification is enabled for time\_zone, [autocommit](#page-91-0), [character\\_set\\_client](#page-99-1), [character\\_set\\_results](#page-101-0), and [character\\_set\\_connection](#page-100-0). (The latter three variables are those affected by SET NAMES.)

To enable display of the Statement ID for each statement processed, use the statement\_id variable. For example:

```
mysql> SET @@SESSION.session_track_system_variables='statement_id'
mysql> SELECT 1;
+---+
| 1 |
+---+
| 1 |
+---+
1 row in set (0.0006 sec)
Statement ID: 603835
```

The special value \* causes the server to track assignments to all session variables. If given, this value must be specified by itself without specific system variable names. This value also enables display of the Statement ID for each successful statement processed.

To disable notification of session variable assignments, set [session\\_track\\_system\\_variables](#page-195-0) to the empty string.

If session system variable tracking is enabled, notification occurs for all assignments to tracked session variables, even if the new values are the same as the old.

For more information about session state tracking, see Section 7.1.18, "Server Tracking of Client Session State".

<span id="page-195-1"></span>• [session\\_track\\_transaction\\_info](#page-195-1)

| Command-Line Format  | session-track-transaction<br>info=value |
|----------------------|-----------------------------------------|
| System Variable      | session_track_transaction_info          |
| Scope                | Global, Session                         |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Enumeration                             |
| Default Value        | OFF                                     |
| Valid Values         | OFF                                     |
|                      | STATE                                   |
|                      | CHARACTERISTICS                         |

Controls whether the server tracks the state and characteristics of transactions within the current session and notifies the client to make this information available. These [session\\_track\\_transaction\\_info](#page-195-1) values are permitted:

- OFF: Disable transaction state tracking. This is the default.
- STATE: Enable transaction state tracking without characteristics tracking. State tracking enables the client to determine whether a transaction is in progress and whether it could be moved to a different session without being rolled back.
- CHARACTERISTICS: Enable transaction state tracking, including characteristics tracking. Characteristics tracking enables the client to determine how to restart a transaction in another session so that it has the same characteristics as in the original session. The following characteristics are relevant for this purpose:

```
ISOLATION LEVEL
READ ONLY
READ WRITE
WITH CONSISTENT SNAPSHOT
```

For a client to safely relocate a transaction to another session, it must track not only transaction state but also transaction characteristics. In addition, the client must track the transaction\_isolation and transaction\_read\_only system variables to correctly determine the session defaults. (To track these variables, list them in the value of the [session\\_track\\_system\\_variables](#page-195-0) system variable.)

For more information about session state tracking, see Section 7.1.18, "Server Tracking of Client Session State".

<span id="page-196-0"></span>• [sha256\\_password\\_auto\\_generate\\_rsa\\_keys](#page-196-0)

| Command-Line Format  | sha256-password-auto-generate-rsa<br>keys[={OFF ON}] |
|----------------------|------------------------------------------------------|
| Deprecated           | Yes                                                  |
| System Variable      | sha256_password_auto_generate_rsa_keys               |
| Scope                | Global                                               |
| Dynamic              | No                                                   |
| SET_VAR Hint Applies | No                                                   |
| Type                 | Boolean                                              |
| Default Value        | ON                                                   |

The server uses this variable to determine whether to autogenerate RSA private/public key-pair files in the data directory if they do not already exist.

At startup, the server automatically generates RSA private/public key-pair files in the data directory if all of these conditions are true: The [sha256\\_password\\_auto\\_generate\\_rsa\\_keys](#page-196-0) or [caching\\_sha2\\_password\\_auto\\_generate\\_rsa\\_keys](#page-98-0) system variable is enabled; no RSA options are specified; the RSA files are missing from the data directory. These key-pair files enable secure password exchange using RSA over unencrypted connections for accounts authenticated by the sha256\_password or caching\_sha2\_password plugin; see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

For more information about RSA file autogeneration, including file names and characteristics, see Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"

The [auto\\_generate\\_certs](#page-92-0) system variable is related but controls autogeneration of SSL certificate and key files needed for secure connections using SSL.

<span id="page-197-0"></span>• [sha256\\_password\\_private\\_key\\_path](#page-197-0)

| Command-Line Format  | sha256-password-private-key<br>path=file_name |
|----------------------|-----------------------------------------------|
| Deprecated           | Yes                                           |
| System Variable      | sha256_password_private_key_path              |
| Scope                | Global                                        |
| Dynamic              | No                                            |
| SET_VAR Hint Applies | No                                            |
| Type                 | File name                                     |
| Default Value        | private_key.pem                               |

The value of this variable is the path name of the RSA private key file for the sha256\_password authentication plugin. If the file is named as a relative path, it is interpreted relative to the server data directory. The file must be in PEM format.

![](_page_197_Picture_8.jpeg)

#### **Important**

Because this file stores a private key, its access mode should be restricted so that only the MySQL server can read it.

For information about sha256\_password, see Section 8.4.1.3, "SHA-256 Pluggable Authentication".

<span id="page-197-1"></span>• [sha256\\_password\\_proxy\\_users](#page-197-1)

| Command-Line Format  | sha256-password-proxy-users[={OFF <br>ON}] |
|----------------------|--------------------------------------------|
| Deprecated           | Yes                                        |
| System Variable      | sha256_password_proxy_users                |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

This variable controls whether the sha256\_password built-in authentication plugin supports proxy users. It has no effect unless the [check\\_proxy\\_users](#page-102-1) system variable is enabled. For information about user proxying, see Section 8.2.19, "Proxy Users".

<span id="page-198-0"></span>• [sha256\\_password\\_public\\_key\\_path](#page-198-0)

| Command-Line Format  | sha256-password-public-key<br>path=file_name |
|----------------------|----------------------------------------------|
| Deprecated           | Yes                                          |
| System Variable      | sha256_password_public_key_path              |
| Scope                | Global                                       |
| Dynamic              | No                                           |
| SET_VAR Hint Applies | No                                           |
| Type                 | File name                                    |
| Default Value        | public_key.pem                               |

The value of this variable is the path name of the RSA public key file for the sha256\_password authentication plugin. If the file is named as a relative path, it is interpreted relative to the server data directory. The file must be in PEM format. Because this file stores a public key, copies can be freely distributed to client users. (Clients that explicitly specify a public key when connecting to the server using RSA password encryption must use the same public key as that used by the server.)

For information about sha256\_password, including information about how clients specify the RSA public key, see Section 8.4.1.3, "SHA-256 Pluggable Authentication".

<span id="page-198-1"></span>• [shared\\_memory](#page-198-1)

| Command-Line Format  | shared-memory[={OFF ON}] |
|----------------------|--------------------------|
| System Variable      | shared_memory            |
| Scope                | Global                   |
| Dynamic              | No                       |
| SET_VAR Hint Applies | No                       |
| Platform Specific    | Windows                  |
| Type                 | Boolean                  |
| Default Value        | OFF                      |

(Windows only.) Whether the server permits shared-memory connections.

<span id="page-198-2"></span>• [shared\\_memory\\_base\\_name](#page-198-2)

| Command-Line Format  | shared-memory-base-name=name |
|----------------------|------------------------------|
| System Variable      | shared_memory_base_name      |
| Scope                | Global                       |
| Dynamic              | No                           |
| SET_VAR Hint Applies | No                           |
| Platform Specific    | Windows                      |
| Type                 | String                       |

| Default Value | MYSQL |
|---------------|-------|
|---------------|-------|

(Windows only.) The name of shared memory to use for shared-memory connections. This is useful when running multiple MySQL instances on a single physical machine. The default name is MYSQL. The name is case-sensitive.

This variable applies only if the server is started with the [shared\\_memory](#page-198-1) system variable enabled to support shared-memory connections.

• [show\\_create\\_table\\_skip\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_show_create_table_skip_secondary_engine)

For use with MySQL HeatWave only. See [System Variables](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md), for more information.

<span id="page-199-0"></span>• [show\\_create\\_table\\_verbosity](#page-199-0)

| Command-Line Format  | show-create-table-verbosity[={OFF <br>ON}] |
|----------------------|--------------------------------------------|
| System Variable      | show_create_table_verbosity                |
| Scope                | Global, Session                            |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |
| Default Value        | OFF                                        |

SHOW CREATE TABLE normally does not show the ROW\_FORMAT table option if the row format is the default format. Enabling this variable causes SHOW CREATE TABLE to display ROW\_FORMAT regardless of whether it is the default format.

<span id="page-199-1"></span>• [show\\_gipk\\_in\\_create\\_table\\_and\\_information\\_schema](#page-199-1)

| Command-Line Format  | show-gipk-in-create-table-and<br>information-schema[={OFF ON}] |
|----------------------|----------------------------------------------------------------|
| System Variable      | show_gipk_in_create_table_and_information_schema               |
| Scope                | Global, Session                                                |
| Dynamic              | Yes                                                            |
| SET_VAR Hint Applies | No                                                             |
| Type                 | Boolean                                                        |
| Default Value        | ON                                                             |
|                      |                                                                |

Whether generated invisible primary keys are visible in the output of SHOW statements and in Information Schema tables. When this variable is set to OFF, such keys are not shown.

This variable is not replicated.

For more information, see Section 15.1.20.11, "Generated Invisible Primary Keys".

<span id="page-199-2"></span>• [show\\_old\\_temporals](#page-199-2)

| Command-Line Format | show-old-temporals[={OFF ON}] |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| System Variable     | show_old_temporals            |
| Scope               | Global, Session               |
| Dynamic             | Yes                           |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | Boolean |
| Default Value        | OFF     |

Whether SHOW CREATE TABLE output includes comments to flag temporal columns found to be in pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds precision). This variable is disabled by default. If enabled, SHOW CREATE TABLE output looks like this:

```
CREATE TABLE `mytbl` (
 `ts` timestamp /* 5.5 binary format */ NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `dt` datetime /* 5.5 binary format */ DEFAULT NULL,
 `t` time /* 5.5 binary format */ DEFAULT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

Output for the COLUMN\_TYPE column of the Information Schema COLUMNS table is affected similarly.

This variable is deprecated and subject to removal in a future MySQL release.

As of MySQL 8.0.27, setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See [Section 7.1.9.1,](#page-42-0) ["System Variable Privileges".](#page-42-0)

<span id="page-0-0"></span>• [skip\\_external\\_locking](#page-0-0)

| Command-Line Format  | skip-external-locking[={OFF ON}] |
|----------------------|----------------------------------|
| System Variable      | skip_external_locking            |
| Scope                | Global                           |
| Dynamic              | No                               |
| SET_VAR Hint Applies | No                               |
| Type                 | Boolean                          |
| Default Value        | ON                               |

This is OFF if mysqld uses external locking (system locking), ON if external locking is disabled. This affects only MyISAM table access.

This variable is set by the --external-locking or --skip-external-locking option. External locking is disabled by default.

External locking affects only MyISAM table access. For more information, including conditions under which it can and cannot be used, see Section 10.11.5, "External Locking".

<span id="page-0-1"></span>• [skip\\_name\\_resolve](#page-0-1)

| Command-Line Format  | skip-name-resolve[={OFF ON}] |
|----------------------|------------------------------|
| System Variable      | skip_name_resolve            |
| Scope                | Global                       |
| Dynamic              | No                           |
| SET_VAR Hint Applies | No                           |
| Type                 | Boolean                      |
| Default Value        | OFF                          |

Whether to resolve host names when checking client connections. If this variable is OFF, mysqld resolves host names when checking client connections. If it is ON, mysqld uses only IP numbers; in this case, all Host column values in the grant tables must be IP addresses. See [Section 7.1.12.3,](#page-114-0) ["DNS Lookups and the Host Cache".](#page-114-0)

Depending on the network configuration of your system and the Host values for your accounts, clients may need to connect using an explicit --host option, such as --host=127.0.0.1 or - host=::1.

An attempt to connect to the host 127.0.0.1 normally resolves to the localhost account. However, this fails if the server is run with [skip\\_name\\_resolve](#page-0-1) enabled. If you plan to do that, make sure an account exists that can accept a connection. For example, to be able to connect as root using --host=127.0.0.1 or --host=::1, create these accounts:

```
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';
```

#### <span id="page-1-0"></span>• [skip\\_networking](#page-1-0)

| Command-Line Format  | skip-networking[={OFF ON}] |
|----------------------|----------------------------|
| System Variable      | skip_networking            |
| Scope                | Global                     |
| Dynamic              | No                         |
| SET_VAR Hint Applies | No                         |
| Type                 | Boolean                    |
| Default Value        | OFF                        |

This variable controls whether the server permits TCP/IP connections. By default, it is disabled (permit TCP connections). If enabled, the server permits only local (non-TCP/IP) connections and all interaction with mysqld must be made using named pipes or shared memory (on Windows) or Unix socket files (on Unix). This option is highly recommended for systems where only local clients are permitted. See [Section 7.1.12.3, "DNS Lookups and the Host Cache"](#page-114-0).

Because starting the server with --skip-grant-tables disables authentication checks, the server also disables remote connections in that case by enabling [skip\\_networking](#page-1-0).

#### <span id="page-1-1"></span>• [skip\\_show\\_database](#page-1-1)

| Command-Line Format  | skip-show-database |
|----------------------|--------------------|
| System Variable      | skip_show_database |
| Scope                | Global             |
| Dynamic              | No                 |
| SET_VAR Hint Applies | No                 |
| Type                 | Boolean            |
| Default Value        | OFF                |

This prevents people from using the SHOW DATABASES statement if they do not have the SHOW DATABASES privilege. This can improve security if you have concerns about users being able to see databases belonging to other users. Its effect depends on the SHOW DATABASES privilege: If the variable value is ON, the SHOW DATABASES statement is permitted only to users who have the SHOW DATABASES privilege, and the statement displays all database names. If the value is OFF, SHOW

DATABASES is permitted to all users, but displays the names of only those databases for which the user has the SHOW DATABASES or other privilege.

![](_page_2_Picture_2.jpeg)

#### **Caution**

Because any static global privilege is considered a privilege for all databases, any static global privilege enables a user to see all database names with SHOW DATABASES or by examining the SCHEMATA table of INFORMATION\_SCHEMA, except databases that have been restricted at the database level by partial revokes.

<span id="page-2-0"></span>• [slow\\_launch\\_time](#page-2-0)

| Command-Line Format  | slow-launch-time=# |
|----------------------|--------------------|
| System Variable      | slow_launch_time   |
| Scope                | Global             |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Integer            |
| Default Value        | 2                  |
| Minimum Value        | 0                  |
| Maximum Value        | 31536000           |
| Unit                 | seconds            |

If creating a thread takes longer than this many seconds, the server increments the [Slow\\_launch\\_threads](#page-94-0) status variable.

<span id="page-2-1"></span>• [slow\\_query\\_log](#page-2-1)

| Command-Line Format  | slow-query-log[={OFF ON}] |
|----------------------|---------------------------|
| System Variable      | slow_query_log            |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Boolean                   |
| Default Value        | OFF                       |

Whether the slow query log is enabled. The value can be 0 (or OFF) to disable the log or 1 (or ON) to enable the log. The destination for log output is controlled by the log\_output system variable; if that value is NONE, no log entries are written even if the log is enabled.

"Slow" is determined by the value of the long\_query\_time variable. See [Section 7.4.5, "The Slow](#page-189-0) [Query Log"](#page-189-0).

<span id="page-2-2"></span>• [slow\\_query\\_log\\_file](#page-2-2)

| Command-Line Format  | slow-query-log-file=file_name |
|----------------------|-------------------------------|
| System Variable      | slow_query_log_file           |
| Scope                | Global                        |
| Dynamic              | Yes                           |
| SET_VAR Hint Applies | No<br>973                     |

| Type          | File name          |
|---------------|--------------------|
| Default Value | host_name-slow.log |

The name of the slow query log file. The default value is host\_name-slow.log, but the initial value can be changed with the --slow\_query\_log\_file option.

### <span id="page-3-0"></span>• [socket](#page-3-0)

| Command-Line Format     | socket={file_name pipe_name} |
|-------------------------|------------------------------|
| System Variable         | socket                       |
| Scope                   | Global                       |
| Dynamic                 | No                           |
| SET_VAR Hint Applies    | No                           |
| Type                    | String                       |
| Default Value (Windows) | MySQL                        |
| Default Value (Other)   | /tmp/mysql.sock              |

On Unix platforms, this variable is the name of the socket file that is used for local client connections. The default is /tmp/mysql.sock. (For some distribution formats, the directory might be different, such as /var/lib/mysql for RPMs.)

On Windows, this variable is the name of the named pipe that is used for local client connections. The default value is MySQL (not case-sensitive).

#### <span id="page-3-1"></span>• [sort\\_buffer\\_size](#page-3-1)

| Command-Line Format                     | sort-buffer-size=#   |
|-----------------------------------------|----------------------|
| System Variable                         | sort_buffer_size     |
| Scope                                   | Global, Session      |
| Dynamic                                 | Yes                  |
| SET_VAR Hint Applies                    | Yes                  |
| Type                                    | Integer              |
| Default Value                           | 262144               |
| Minimum Value                           | 32768                |
| Maximum Value (Windows)                 | 4294967295           |
| Maximum Value (Other, 64-bit platforms) | 18446744073709551615 |
| Maximum Value (Other, 32-bit platforms) | 4294967295           |
| Unit                                    | bytes                |

Each session that must perform a sort allocates a buffer of this size. [sort\\_buffer\\_size](#page-3-1) is not specific to any storage engine and applies in a general manner for optimization. At minimum the [sort\\_buffer\\_size](#page-3-1) value must be large enough to accommodate fifteen tuples in the sort buffer. Also, increasing the value of max\_sort\_length may require increasing the value of [sort\\_buffer\\_size](#page-3-1). For more information, see Section 10.2.1.16, "ORDER BY Optimization"

If you see many [Sort\\_merge\\_passes](#page-94-1) per second in SHOW GLOBAL STATUS output, you can consider increasing the [sort\\_buffer\\_size](#page-3-1) value to speed up ORDER BY or GROUP BY operations that cannot be improved with query optimization or improved indexing.

The optimizer tries to work out how much space is needed but can allocate more, up to the limit. Setting it larger than required globally slows down most queries that perform sorts. It is best to

increase it as a session setting, and only for the sessions that need a larger size. On Linux, there are thresholds of 256KB and 2MB where larger values may significantly slow down memory allocation, so you should consider staying below one of those values. Experiment to find the best value for your workload. See Section B.3.3.5, "Where MySQL Stores Temporary Files".

The maximum permissible setting for [sort\\_buffer\\_size](#page-3-1) is 4GB−1. Larger values are permitted for 64-bit platforms (except 64-bit Windows, for which large values are truncated to 4GB−1 with a warning).

<span id="page-4-0"></span>• [sql\\_auto\\_is\\_null](#page-4-0)

| System Variable      | sql_auto_is_null |
|----------------------|------------------|
| Scope                | Global, Session  |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | Yes              |
| Type                 | Boolean          |
| Default Value        | OFF              |

If this variable is enabled, then after a statement that successfully inserts an automatically generated AUTO\_INCREMENT value, you can find that value by issuing a statement of the following form:

```
SELECT * FROM tbl_name WHERE auto_col IS NULL
```

If the statement returns a row, the value returned is the same as if you invoked the LAST\_INSERT\_ID() function. For details, including the return value after a multiple-row insert, see Section 14.15, "Information Functions". If no AUTO\_INCREMENT value was successfully inserted, the SELECT statement returns no row.

The behavior of retrieving an AUTO\_INCREMENT value by using an IS NULL comparison is used by some ODBC programs, such as Access. See [Obtaining Auto-Increment Values.](https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-usagenotes-functionality-last-insert-id.md) This behavior can be disabled by setting [sql\\_auto\\_is\\_null](#page-4-0) to OFF.

Prior to MySQL 8.0.16, the transformation of WHERE auto\_col IS NULL to WHERE auto\_col = LAST\_INSERT\_ID() was performed only when the statement was executed, so that the value of sql\_auto\_is\_null during execution determined whether the query was transformed. In MySQL 8.0.16 and later, the transformation is performed during statement preparation.

The default value of [sql\\_auto\\_is\\_null](#page-4-0) is OFF.

<span id="page-4-1"></span>• [sql\\_big\\_selects](#page-4-1)

| System Variable      | sql_big_selects |
|----------------------|-----------------|
| Scope                | Global, Session |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | Yes             |
| Type                 | Boolean         |
| Default Value        | ON              |

If set to OFF, MySQL aborts SELECT statements that are likely to take a very long time to execute (that is, statements for which the optimizer estimates that the number of examined rows exceeds the value of max\_join\_size). This is useful when an inadvisable WHERE statement has been issued. The default value for a new connection is ON, which permits all SELECT statements.

If you set the max\_join\_size system variable to a value other than DEFAULT, [sql\\_big\\_selects](#page-4-1) is set to OFF.

<span id="page-5-0"></span>• [sql\\_buffer\\_result](#page-5-0)

| System Variable      | sql_buffer_result |
|----------------------|-------------------|
| Scope                | Global, Session   |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | Yes               |
| Type                 | Boolean           |
| Default Value        | OFF               |

If enabled, [sql\\_buffer\\_result](#page-5-0) forces results from SELECT statements to be put into temporary tables. This helps MySQL free the table locks early and can be beneficial in cases where it takes a long time to send results to the client. The default value is OFF.

<span id="page-5-1"></span>• [sql\\_generate\\_invisible\\_primary\\_key](#page-5-1)

| Command-Line Format  | sql-generate-invisible-primary<br>key[={OFF ON}] |
|----------------------|--------------------------------------------------|
| System Variable      | sql_generate_invisible_primary_key               |
| Scope                | Global, Session                                  |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | Boolean                                          |
| Default Value        | OFF                                              |

Whether this server adds a generated invisible primary key to any InnoDB table that is created without one.

This variable is not replicated. In addition, even if set on the replica, it is ignored by replication applier threads; this means that, by default, a replica does not generate a primary key for any replicated table which, on the source, was created without one. In MySQL 8.0.32 and later, you can cause the replica to generate invisible primary keys for such tables by setting REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK = GENERATE as part of a CHANGE REPLICATION SOURCE TO statement, optionally specifying a replication channel.

For more information and examples, see Section 15.1.20.11, "Generated Invisible Primary Keys".

<span id="page-5-2"></span>• [sql\\_log\\_off](#page-5-2)

| System Variable      | sql_log_off          |
|----------------------|----------------------|
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | Boolean              |
| Default Value        | OFF                  |
| Valid Values         | OFF (enable logging) |
|                      | ON (disable logging) |

This variable controls whether logging to the general query log is disabled for the current session (assuming that the general query log itself is enabled). The default value is OFF (that is, enable

logging). To disable or enable general query logging for the current session, set the session [sql\\_log\\_off](#page-5-2) variable to ON or OFF.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See [Section 7.1.9.1, "System Variable](#page-42-0) [Privileges".](#page-42-0)

#### <span id="page-6-0"></span>• [sql\\_mode](#page-6-0)

| Command-Line Format  | sql-mode=name                                                                                                                     |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| System Variable      | sql_mode                                                                                                                          |
| Scope                | Global, Session                                                                                                                   |
| Dynamic              | Yes                                                                                                                               |
| SET_VAR Hint Applies | Yes                                                                                                                               |
| Type                 | Set                                                                                                                               |
| Default Value        | ONLY_FULL_GROUP_BY<br>STRICT_TRANS_TABLES<br>NO_ZERO_IN_DATE NO_ZERO_DATE<br>ERROR_FOR_DIVISION_BY_ZERO<br>NO_ENGINE_SUBSTITUTION |
| Valid Values         | ALLOW_INVALID_DATES                                                                                                               |
|                      | ANSI_QUOTES                                                                                                                       |
|                      | ERROR_FOR_DIVISION_BY_ZERO                                                                                                        |
|                      | HIGH_NOT_PRECEDENCE                                                                                                               |
|                      | IGNORE_SPACE                                                                                                                      |
|                      | NO_AUTO_VALUE_ON_ZERO                                                                                                             |
|                      | NO_BACKSLASH_ESCAPES                                                                                                              |
|                      | NO_DIR_IN_CREATE                                                                                                                  |
|                      | NO_ENGINE_SUBSTITUTION                                                                                                            |
|                      | NO_UNSIGNED_SUBTRACTION                                                                                                           |
|                      | NO_ZERO_DATE                                                                                                                      |
|                      | NO_ZERO_IN_DATE                                                                                                                   |
|                      | ONLY_FULL_GROUP_BY                                                                                                                |
|                      | PAD_CHAR_TO_FULL_LENGTH                                                                                                           |
|                      | PIPES_AS_CONCAT                                                                                                                   |
|                      | REAL_AS_FLOAT                                                                                                                     |
|                      | STRICT_ALL_TABLES                                                                                                                 |
|                      | STRICT_TRANS_TABLES                                                                                                               |

TIME\_TRUNCATE\_FRACTIONAL

The current server SQL mode, which can be set dynamically. For details, see [Section 7.1.11, "Server](#page-98-0) [SQL Modes"](#page-98-0).

![](_page_7_Picture_3.jpeg)

#### **Note**

MySQL installation programs may configure the SQL mode during the installation process.

If the SQL mode differs from the default or from what you expect, check for a setting in an option file that the server reads at startup.

<span id="page-7-0"></span>• [sql\\_notes](#page-7-0)

| System Variable      | sql_notes       |
|----------------------|-----------------|
| Scope                | Global, Session |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | No              |
| Type                 | Boolean         |
| Default Value        | ON              |

If enabled (the default), diagnostics of Note level increment warning\_count and the server records them. If disabled, Note diagnostics do not increment [warning\\_count](#page-38-0) and the server does not record them. mysqldump includes output to disable this variable so that reloading the dump file does not produce warnings for events that do not affect the integrity of the reload operation.

<span id="page-7-1"></span>• [sql\\_quote\\_show\\_create](#page-7-1)

| System Variable      | sql_quote_show_create |
|----------------------|-----------------------|
| Scope                | Global, Session       |
| Dynamic              | Yes                   |
| SET_VAR Hint Applies | No                    |
| Type                 | Boolean               |
| Default Value        | ON                    |

If enabled (the default), the server quotes identifiers for SHOW CREATE TABLE and SHOW CREATE DATABASE statements. If disabled, quoting is disabled. This option is enabled by default so that replication works for identifiers that require quoting. See Section 15.7.7.10, "SHOW CREATE TABLE Statement", and Section 15.7.7.6, "SHOW CREATE DATABASE Statement".

<span id="page-7-2"></span>• [sql\\_require\\_primary\\_key](#page-7-2)

| Command-Line Format  | sql-require-primary-key[={OFF ON}] |
|----------------------|------------------------------------|
| System Variable      | sql_require_primary_key            |
| Scope                | Global, Session                    |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | Yes                                |
| Type                 | Boolean                            |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

Whether statements that create new tables or alter the structure of existing tables enforce the requirement that tables have a primary key.

Setting the session value of this system variable is a restricted operation. The session user must have privileges sufficient to set restricted session variables. See [Section 7.1.9.1, "System Variable](#page-42-0) [Privileges".](#page-42-0)

Enabling this variable helps avoid performance problems in row-based replication that can occur when tables have no primary key. Suppose that a table has no primary key and an update or delete modifies multiple rows. On the replication source server, this operation can be performed using a single table scan but, when replicated using row-based replication, results in a table scan for each row to be modified on the replica. With a primary key, these table scans do not occur.

[sql\\_require\\_primary\\_key](#page-7-2) applies to both base tables and TEMPORARY tables, and changes to its value are replicated to replica servers. As of MySQL 8.0.18, it applies only to storage engines that can participate in replication.

When enabled, [sql\\_require\\_primary\\_key](#page-7-2) has these effects:

- Attempts to create a new table with no primary key fail with an error. This includes CREATE TABLE ... LIKE. It also includes CREATE TABLE ... SELECT, unless the CREATE TABLE part includes a primary key definition.
- Attempts to drop the primary key from an existing table fail with an error, with the exception that dropping the primary key and adding a primary key in the same ALTER TABLE statement is permitted.

Dropping the primary key fails even if the table also contains a UNIQUE NOT NULL index.

• Attempts to import a table with no primary key fail with an error.

The REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option of the CHANGE REPLICATION SOURCE TO statement (MySQL 8.0.23 and later) or CHANGE MASTER TO statement (before MySQL 8.0.23) enables a replica to select its own policy for primary key checks. When the option is set to ON for a replication channel, the replica always uses the value ON for the [sql\\_require\\_primary\\_key](#page-7-2) system variable in replication operations, requiring a primary key. When the option is set to OFF, the replica always uses the value OFF for the [sql\\_require\\_primary\\_key](#page-7-2) system variable in replication operations, so that a primary key is never required, even if the source required one. When the REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option is set to STREAM, which is the default, the replica uses whatever value is replicated from the source for each transaction. With the STREAM setting for the REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK option, if privilege checks are in use for the replication channel, the PRIVILEGE\_CHECKS\_USER account needs privileges sufficient to set restricted session variables, so that it can set the session value for the [sql\\_require\\_primary\\_key](#page-7-2) system variable. With the ON or OFF settings, the account does not need these privileges. For more information, see Section 19.3.3, "Replication Privilege Checks".

<span id="page-8-0"></span>• [sql\\_safe\\_updates](#page-8-0)

| System Variable      | sql_safe_updates |
|----------------------|------------------|
| Scope                | Global, Session  |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | Yes              |
| Type                 | Boolean          |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

If this variable is enabled, UPDATE and DELETE statements that do not use a key in the WHERE clause or a LIMIT clause produce an error. This makes it possible to catch UPDATE and DELETE statements where keys are not used properly and that would probably change or delete a large number of rows. The default value is OFF.

For the mysql client, [sql\\_safe\\_updates](#page-8-0) can be enabled by using the --safe-updates option. For more information, see Using Safe-Updates Mode (--safe-updates).

#### <span id="page-9-0"></span>• [sql\\_select\\_limit](#page-9-0)

| System Variable      | sql_select_limit     |
|----------------------|----------------------|
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | Yes                  |
| Type                 | Integer              |
| Default Value        | 18446744073709551615 |
| Minimum Value        | 0                    |
| Maximum Value        | 18446744073709551615 |

The maximum number of rows to return from SELECT statements. For more information, see Using Safe-Updates Mode (--safe-updates).

The default value for a new connection is the maximum number of rows that the server permits per table. Typical default values are (232)−1 or (264)−1. If you have changed the limit, the default value can be restored by assigning a value of DEFAULT.

If a SELECT has a LIMIT clause, the LIMIT takes precedence over the value of [sql\\_select\\_limit](#page-9-0).

#### <span id="page-9-1"></span>• [sql\\_warnings](#page-9-1)

| System Variable      | sql_warnings    |
|----------------------|-----------------|
| Scope                | Global, Session |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | No              |
| Type                 | Boolean         |
| Default Value        | OFF             |

This variable controls whether single-row INSERT statements produce an information string if warnings occur. The default is OFF. Set the value to ON to produce an information string.

### <span id="page-9-2"></span>• [ssl\\_ca](#page-9-2)

| Command-Line Format  | ssl-ca=file_name |
|----------------------|------------------|
| System Variable      | ssl_ca           |
| Scope                | Global           |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | No               |
| Type                 | File name        |
| Default Value        | NULL             |

The path name of the Certificate Authority (CA) certificate file in PEM format. The file contains a list of trusted SSL Certificate Authorities.

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

### <span id="page-10-0"></span>• [ssl\\_capath](#page-10-0)

| Command-Line Format  | ssl-capath=dir_name |
|----------------------|---------------------|
| System Variable      | ssl_capath          |
| Scope                | Global              |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |
| Type                 | Directory name      |
| Default Value        | NULL                |

The path name of the directory that contains trusted SSL Certificate Authority (CA) certificate files in PEM format. You must run OpenSSL rehash on the directory specified by this option prior to using it. On Linux systems, you can invoke rehash like this:

#### \$> **openssl rehash path/to/directory**

On Windows platforms, you can use the c\_rehash script in a command prompt, like this:

#### \> **c\_rehash path/to/directory**

See [openssl-rehash](https://docs.openssl.org/3.1/man1/openssl-rehash/) for complete syntax and other information.

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

#### <span id="page-10-1"></span>• [ssl\\_cert](#page-10-1)

| Command-Line Format  | ssl-cert=file_name |
|----------------------|--------------------|
| System Variable      | ssl_cert           |
| Scope                | Global             |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | File name          |
| Default Value        | NULL               |

The path name of the server SSL public key certificate file in PEM format.

If the server is started with [ssl\\_cert](#page-10-1) set to a certificate that uses any restricted cipher or cipher category, the server starts with support for encrypted connections disabled. For information about cipher restrictions, see Connection Cipher Configuration.

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

![](_page_11_Picture_2.jpeg)

#### **Note**

Chained SSL certificate support was added in v8.0.30; previously only the first certificate was read.

<span id="page-11-0"></span>• [ssl\\_cipher](#page-11-0)

| Command-Line Format  | ssl-cipher=name |
|----------------------|-----------------|
| System Variable      | ssl_cipher      |
| Scope                | Global          |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | No              |
| Type                 | String          |
| Default Value        | NULL            |

The list of permissible encryption ciphers for connections that use TLS protocols up through TLSv1.2. If no cipher in the list is supported, encrypted connections that use these TLS protocols do not work.

For greatest portability, the cipher list should be a list of one or more cipher names, separated by colons. The following example shows two cipher names separated by a colon:

```
[mysqld]
ssl_cipher="DHE-RSA-AES128-GCM-SHA256:AES128-SHA"
```

OpenSSL supports the syntax for specifying ciphers described in the OpenSSL documentation at <https://www.openssl.org/docs/manmaster/man1/ciphers.html>.

For information about which encryption ciphers MySQL supports, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

<span id="page-11-1"></span>• [ssl\\_crl](#page-11-1)

| Command-Line Format  | ssl-crl=file_name |
|----------------------|-------------------|
| System Variable      | ssl_crl           |
| Scope                | Global            |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | File name         |
| Default Value        | NULL              |

The path name of the file containing certificate revocation lists in PEM format.

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE 982 RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

<span id="page-12-0"></span>• [ssl\\_crlpath](#page-12-0)

| Command-Line Format  | ssl-crlpath=dir_name |
|----------------------|----------------------|
| System Variable      | ssl_crlpath          |
| Scope                | Global               |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | Directory name       |
| Default Value        | NULL                 |

The path of the directory that contains certificate revocation-list files in PEM format.

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

<span id="page-12-1"></span>• [ssl\\_fips\\_mode](#page-12-1)

| Command-Line Format  | ssl-fips-mode={OFF ON STRICT} |
|----------------------|-------------------------------|
| Deprecated           | Yes                           |
| System Variable      | ssl_fips_mode                 |
| Scope                | Global                        |
| Dynamic              | No                            |
| SET_VAR Hint Applies | No                            |
| Type                 | Enumeration                   |
| Default Value        | OFF                           |
| Valid Values         | OFF (or 0)                    |
|                      | ON (or 1)                     |
|                      | STRICT (or 2)                 |

Controls whether to enable FIPS mode on the server side. The [ssl\\_fips\\_mode](#page-12-1) system variable differs from other ssl\_xxx system variables in that it is not used to control whether the server permits encrypted connections, but rather to affect which cryptographic operations are permitted. See Section 8.8, "FIPS Support".

These [ssl\\_fips\\_mode](#page-12-1) values are permitted:

- OFF (or 0): Disable FIPS mode.
- ON (or 1): Enable FIPS mode.

• STRICT (or 2): Enable "strict" FIPS mode.

![](_page_13_Picture_2.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [ssl\\_fips\\_mode](#page-12-1) is OFF. In this case, setting [ssl\\_fips\\_mode](#page-12-1) to ON or STRICT at startup causes the server to produce an error message and exit.

As of MySQL 8.0.34, this option is deprecated and made read-only. Expect it to be removed in a future version of MySQL.

<span id="page-13-0"></span>• [ssl\\_key](#page-13-0)

| Command-Line Format  | ssl-key=file_name |
|----------------------|-------------------|
| System Variable      | ssl_key           |
| Scope                | Global            |
| Dynamic              | Yes               |
| SET_VAR Hint Applies | No                |
| Type                 | File name         |
| Default Value        | NULL              |

The path name of the server SSL private key file in PEM format. For better security, use a certificate with an RSA key size of at least 2048 bits.

If the key file is protected by a passphrase, the server prompts the user for the passphrase. The password must be given interactively; it cannot be stored in a file. If the passphrase is incorrect, the program continues as if it could not read the key.

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections established after the execution of ALTER INSTANCE RELOAD TLS or after a restart if the variable value was persisted. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

<span id="page-13-1"></span>• [ssl\\_session\\_cache\\_mode](#page-13-1)

| Command-Line Format  | ssl_session_cache_mode={ON OFF} |
|----------------------|---------------------------------|
| System Variable      | ssl_session_cache_mode          |
| Scope                | Global                          |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |
| Default Value        | ON                              |
| Valid Values         | ON                              |
|                      | OFF                             |

Controls whether to enable the session cache in memory on the server side and session-ticket generation by the server. The default mode is ON (enable session cache mode). A change to the [ssl\\_session\\_cache\\_mode](#page-13-1) system variable has an effect only after the ALTER INSTANCE RELOAD TLS statement has been executed, or after a restart if the variable value was persisted.

These [ssl\\_session\\_cache\\_mode](#page-13-1) values are permitted:

- ON: Enable session cache mode.
- OFF: Disable session cache mode.

The server does not advertise its support for session resumption if the value of this system variable is OFF. When running on OpenSSL 1.0.x the session tickets are always generated, but the tickets are not usable when [ssl\\_session\\_cache\\_mode](#page-13-1) is enabled.

The current value in effect for [ssl\\_session\\_cache\\_mode](#page-13-1) can be observed with the [Ssl\\_session\\_cache\\_mode](#page-96-0) status variable.

<span id="page-14-0"></span>• [ssl\\_session\\_cache\\_timeout](#page-14-0)

| Command-Line Format  | ssl_session_cache_timeout |
|----------------------|---------------------------|
| System Variable      | ssl_session_cache_timeout |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |
| Default Value        | 300                       |
| Minimum Value        | 0                         |
| Maximum Value        | 84600                     |
| Unit                 | seconds                   |

Sets a period of time during which prior session reuse is permitted when establishing a new encrypted connection to the server, provided the [ssl\\_session\\_cache\\_mode](#page-13-1) system variable is enabled and prior session data is available. If the session timeout expires, a session can no longer be reused.

The default value is 300 seconds and the maximum value is 84600 (or one day in seconds). A change to the [ssl\\_session\\_cache\\_timeout](#page-14-0) system variable has an effect only after the ALTER INSTANCE RELOAD TLS statement has been executed, or after a restart if the variable value was persisted. The current value in effect for [ssl\\_session\\_cache\\_timeout](#page-14-0) can be observed with the [Ssl\\_session\\_cache\\_timeout](#page-96-1) status variable.

<span id="page-14-1"></span>• [statement\\_id](#page-14-1)

| System Variable      | statement_id |
|----------------------|--------------|
| Scope                | Session      |
| Dynamic              | No           |
| SET_VAR Hint Applies | No           |
| Type                 | Integer      |

Each statement executed in the current session is assigned a sequence number. This can be used together with the session\_track\_system\_variables system variable to identify this statement in Performance Schema tables such as the events\_statements\_history table.

### <span id="page-15-0"></span>• [stored\\_program\\_cache](#page-15-0)

| Command-Line Format  | stored-program-cache=# |
|----------------------|------------------------|
| System Variable      | stored_program_cache   |
| Scope                | Global                 |
| Dynamic              | Yes                    |
| SET_VAR Hint Applies | No                     |
| Type                 | Integer                |
| Default Value        | 256                    |
| Minimum Value        | 16                     |
| Maximum Value        | 524288                 |

Sets a soft upper limit for the number of cached stored routines per connection. The value of this variable is specified in terms of the number of stored routines held in each of the two caches maintained by the MySQL Server for, respectively, stored procedures and stored functions.

Whenever a stored routine is executed this cache size is checked before the first or top-level statement in the routine is parsed; if the number of routines of the same type (stored procedures or stored functions according to which is being executed) exceeds the limit specified by this variable, the corresponding cache is flushed and memory previously allocated for cached objects is freed. This allows the cache to be flushed safely, even when there are dependencies between stored routines.

The stored procedure and stored function caches exists in parallel with the stored program definition cache partition of the dictionary object cache. The stored procedure and stored function caches are per connection, while the stored program definition cache is shared. The existence of objects in the stored procedure and stored function caches have no dependence on the existence of objects in the stored program definition cache, and vice versa. For more information, see Section 16.4, "Dictionary Object Cache".

#### <span id="page-15-1"></span>• [stored\\_program\\_definition\\_cache](#page-15-1)

| Command-Line Format  | stored-program-definition-cache=# |
|----------------------|-----------------------------------|
| System Variable      | stored_program_definition_cache   |
| Scope                | Global                            |
| Dynamic              | Yes                               |
| SET_VAR Hint Applies | No                                |
| Type                 | Integer                           |
| Default Value        | 256                               |
| Minimum Value        | 256                               |

| Maximum Value | 524288 |
|---------------|--------|
|---------------|--------|

Defines a limit for the number of stored program definition objects, both used and unused, that can be kept in the dictionary object cache.

Unused stored program definition objects are only kept in the dictionary object cache when the number in use is less than the capacity defined by stored\_program\_definition\_cache.

A setting of 0 means that stored program definition objects are only kept in the dictionary object cache while they are in use.

The stored program definition cache partition exists in parallel with the stored procedure and stored function caches that are configured using the [stored\\_program\\_cache](#page-15-0) option.

The [stored\\_program\\_cache](#page-15-0) option sets a soft upper limit for the number of cached stored procedures or functions per connection, and the limit is checked each time a connection executes a stored procedure or function. The stored program definition cache partition, on the other hand, is a shared cache that stores stored program definition objects for other purposes. The existence of objects in the stored program definition cache partition has no dependence on the existence of objects in the stored procedure cache or stored function cache, and vice versa.

For related information, see Section 16.4, "Dictionary Object Cache".

<span id="page-16-0"></span>• [super\\_read\\_only](#page-16-0)

| Command-Line Format  | super-read-only[={OFF ON}] |
|----------------------|----------------------------|
| System Variable      | super_read_only            |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Boolean                    |
| Default Value        | OFF                        |

If the read\_only system variable is enabled, the server permits no client updates except from users who have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). If the [super\\_read\\_only](#page-16-0) system variable is also enabled, the server prohibits client updates even from users who have CONNECTION\_ADMIN or SUPER. See the description of the read\_only system variable for a description of read-only mode and information about how read\_only and [super\\_read\\_only](#page-16-0) interact.

Client updates prevented when [super\\_read\\_only](#page-16-0) is enabled include operations that do not necessarily appear to be updates, such as CREATE FUNCTION (to install a loadable function), INSTALL PLUGIN, and INSTALL COMPONENT. These operations are prohibited because they involve changes to tables in the mysql system schema.

Similarly, if the Event Scheduler is enabled, enabling the [super\\_read\\_only](#page-16-0) system variable prevents it from updating event "last executed" timestamps in the events data dictionary table. This causes the Event Scheduler to stop the next time it tries to execute a scheduled event, after writing a message to the server error log. (In this situation the event\_scheduler system variable does not change from ON to OFF. An implication is that this variable rejects the DBA intent that the Event Scheduler be enabled or disabled, where its actual status of started or stopped may be distinct.). If [super\\_read\\_only](#page-16-0) is subsequently disabled after being enabled, the server automatically restarts the Event Scheduler as needed, as of MySQL 8.0.26. Prior to MySQL 8.0.26, it is necessary to manually restart the Event Scheduler by enabling it again.

Changes to [super\\_read\\_only](#page-16-0) on a replication source server are not replicated to replica servers. The value can be set on a replica independent of the setting on the source.

### <span id="page-17-0"></span>• [syseventlog.facility](#page-17-0)

| Command-Line Format  | syseventlog.facility=value |
|----------------------|----------------------------|
| System Variable      | syseventlog.facility       |
| Scope                | Global                     |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | String                     |
| Default Value        | daemon                     |

The facility for error log output written to syslog (what type of program is sending the message). This variable is unavailable unless the log\_sink\_syseventlog error log component is installed. See [Section 7.4.2.8, "Error Logging to the System Log"](#page-168-0).

The permitted values can vary per operating system; consult your system syslog documentation.

This variable does not exist on Windows.

#### <span id="page-17-1"></span>• [syseventlog.include\\_pid](#page-17-1)

| Command-Line Format  | syseventlog.include-pid[={OFF ON}] |
|----------------------|------------------------------------|
| System Variable      | syseventlog.include_pid            |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Boolean                            |
| Default Value        | ON                                 |

Whether to include the server process ID in each line of error log output written to syslog. This variable is unavailable unless the log\_sink\_syseventlog error log component is installed. See [Section 7.4.2.8, "Error Logging to the System Log".](#page-168-0)

This variable does not exist on Windows.

### <span id="page-17-2"></span>• [syseventlog.tag](#page-17-2)

| Command-Line Format  | syseventlog.tag=tag |
|----------------------|---------------------|
| System Variable      | syseventlog.tag     |
| Scope                | Global              |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |
| Type                 | String              |

| Default Value | empty string |
|---------------|--------------|
|---------------|--------------|

The tag to be added to the server identifier in error log output written to syslog or the Windows Event Log. This variable is unavailable unless the log\_sink\_syseventlog error log component is installed. See [Section 7.4.2.8, "Error Logging to the System Log".](#page-168-0)

By default, no tag is set, so the server identifier is simply MySQL on Windows, and mysqld on other platforms. If a tag value of tag is specified, it is appended to the server identifier with a leading hyphen, resulting in a syslog identifier of mysqld-tag (or MySQL-tag on Windows).

On Windows, to use a tag that does not already exist, the server must be run from an account with Administrator privileges, to permit creation of a registry entry for the tag. Elevated privileges are not required if the tag already exists.

<span id="page-18-0"></span>• [system\\_time\\_zone](#page-18-0)

| System Variable      | system_time_zone |
|----------------------|------------------|
| Scope                | Global           |
| Dynamic              | No               |
| SET_VAR Hint Applies | No               |
| Type                 | String           |

The server system time zone. When the server begins executing, it inherits a time zone setting from the machine defaults, possibly modified by the environment of the account used for running the server or the startup script. The value is used to set [system\\_time\\_zone](#page-18-0). To explicitly specify the system time zone, set the TZ environment variable or use the --timezone option of the mysqld\_safe script.

As of MySQL 8.0.26, in addition to startup time initialization, if the server host time zone changes (for example, due to daylight saving time), [system\\_time\\_zone](#page-18-0) reflects that change, which has these implications for applications:

- Queries that reference [system\\_time\\_zone](#page-18-0) will get one value before a daylight saving change and a different value after the change.
- For queries that begin executing before a daylight saving change and end after the change, the [system\\_time\\_zone](#page-18-0) remains constant within the query because the value is usually cached at the beginning of execution.

The [system\\_time\\_zone](#page-18-0) variable differs from the [time\\_zone](#page-29-0) variable. Although they might have the same value, the latter variable is used to initialize the time zone for each client that connects. See [Section 7.1.15, "MySQL Server Time Zone Support".](#page-126-0)

<span id="page-18-1"></span>• [table\\_definition\\_cache](#page-18-1)

| Command-Line Format  | table-definition-cache=#                                       |
|----------------------|----------------------------------------------------------------|
| System Variable      | table_definition_cache                                         |
| Scope                | Global                                                         |
| Dynamic              | Yes                                                            |
| SET_VAR Hint Applies | No                                                             |
| Type                 | Integer                                                        |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value        | 400                                                            |

| Maximum Value | 524288 |
|---------------|--------|
|---------------|--------|

The number of table definitions that can be stored in the table definition cache. If you use a large number of tables, you can create a large table definition cache to speed up opening of tables. The table definition cache takes less space and does not use file descriptors, unlike the normal table cache. The minimum value is 400. The default value is based on the following formula, capped to a limit of 2000:

```
MIN(400 + table_open_cache / 2, 2000)
```

For InnoDB, the [table\\_definition\\_cache](#page-18-1) setting acts as a soft limit for the number of table instances in the dictionary object cache and the number file-per-table tablespaces that can be open at one time.

If the number of table instances in the dictionary object cache exceeds the [table\\_definition\\_cache](#page-18-1) limit, an LRU mechanism begins marking table instances for eviction and eventually removes them from the dictionary object cache. The number of open tables with cached metadata can be higher than the [table\\_definition\\_cache](#page-18-1) limit due to table instances with foreign key relationships, which are not placed on the LRU list.

The number of file-per-table tablespaces that can be open at one time is limited by both the [table\\_definition\\_cache](#page-18-1) and innodb\_open\_files settings. If both variables are set, the highest setting is used. If neither variable is set, the [table\\_definition\\_cache](#page-18-1) setting, which has a higher default value, is used. If the number of open tablespaces exceeds the limit defined by [table\\_definition\\_cache](#page-18-1) or innodb\_open\_files, an LRU mechanism searches the LRU list for tablespace files that are fully flushed and not currently being extended. This process is performed each time a new tablespace is opened. Only inactive tablespaces are closed.

The table definition cache exists in parallel with the table definition cache partition of the dictionary object cache. Both caches store table definitions but serve different parts of the MySQL server. Objects in one cache have no dependence on the existence of objects in the other. For more information, see Section 16.4, "Dictionary Object Cache".

<span id="page-19-0"></span>• [table\\_encryption\\_privilege\\_check](#page-19-0)

| Command-Line Format  | table-encryption-privilege<br>check[={OFF ON}] |
|----------------------|------------------------------------------------|
| System Variable      | table_encryption_privilege_check               |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | Boolean                                        |
| Default Value        | OFF                                            |

Controls the TABLE\_ENCRYPTION\_ADMIN privilege check that occurs when creating or altering a schema or general tablespace with encryption that differs from the default\_table\_encryption setting, or when creating or altering a table with an encryption setting that differs from the default schema encryption. The check is disabled by default.

Setting [table\\_encryption\\_privilege\\_check](#page-19-0) at runtime requires the SUPER privilege.

[table\\_encryption\\_privilege\\_check](#page-19-0) supports SET PERSIST and SET PERSIST\_ONLY syntax. See [Section 7.1.9.3, "Persisted System Variables"](#page-61-0).

For more information, see Defining an Encryption Default for Schemas and General Tablespaces.

### <span id="page-20-0"></span>• [table\\_open\\_cache](#page-20-0)

| Command-Line Format  | table-open-cache=# |
|----------------------|--------------------|
| System Variable      | table_open_cache   |
| Scope                | Global             |
| Dynamic              | Yes                |
| SET_VAR Hint Applies | No                 |
| Type                 | Integer            |
| Default Value        | 4000               |
| Minimum Value        | 1                  |
| Maximum Value        | 524288             |

The number of open tables for all threads. Increasing this value increases the number of file descriptors that mysqld requires. The effective value of this variable is the greater of the effective value of open\_files\_limit - 10 - the effective value of max\_connections / 2, and 400; that is

```
MAX(
 (open_files_limit - 10 - max_connections) / 2,
 400
 )
```

You can check whether you need to increase the table cache by checking the [Opened\\_tables](#page-87-0) status variable. If the value of [Opened\\_tables](#page-87-0) is large and you do not use FLUSH TABLES often (which just forces all tables to be closed and reopened), then you should increase the value of the [table\\_open\\_cache](#page-20-0) variable. For more information about the table cache, see Section 10.4.3.1, "How MySQL Opens and Closes Tables".

### <span id="page-20-1"></span>• [table\\_open\\_cache\\_instances](#page-20-1)

| Command-Line Format  | table-open-cache-instances=# |
|----------------------|------------------------------|
| System Variable      | table_open_cache_instances   |
| Scope                | Global                       |
| Dynamic              | No                           |
| SET_VAR Hint Applies | No                           |
| Type                 | Integer                      |
| Default Value        | 16                           |
| Minimum Value        | 1                            |
| Maximum Value        | 64                           |

The number of open tables cache instances. To improve scalability by reducing contention among sessions, the open tables cache can be partitioned into several smaller cache instances of size [table\\_open\\_cache](#page-20-0) / [table\\_open\\_cache\\_instances](#page-20-1) . A session needs to lock only one instance to access it for DML statements. This segments cache access among instances, permitting higher performance for operations that use the cache when there are many sessions accessing tables. (DDL statements still require a lock on the entire cache, but such statements are much less frequent than DML statements.)

A value of 8 or 16 is recommended on systems that routinely use 16 or more cores. However, if you have many large triggers on your tables that cause a high memory load, the default setting for [table\\_open\\_cache\\_instances](#page-20-1) might lead to excessive memory usage. In that situation, it can be helpful to set [table\\_open\\_cache\\_instances](#page-20-1) to 1 in order to restrict memory usage.

<span id="page-20-2"></span>• [tablespace\\_definition\\_cache](#page-20-2)

| Command-Line Format  | tablespace-definition-cache=# |
|----------------------|-------------------------------|
| System Variable      | tablespace_definition_cache   |
| Scope                | Global                        |
| Dynamic              | Yes                           |
| SET_VAR Hint Applies | No                            |
| Type                 | Integer                       |
| Default Value        | 256                           |
| Minimum Value        | 256                           |
| Maximum Value        | 524288                        |

Defines a limit for the number of tablespace definition objects, both used and unused, that can be kept in the dictionary object cache.

Unused tablespace definition objects are only kept in the dictionary object cache when the number in use is less than the capacity defined by tablespace\_definition\_cache.

A setting of 0 means that tablespace definition objects are only kept in the dictionary object cache while they are in use.

For more information, see Section 16.4, "Dictionary Object Cache".

#### <span id="page-21-0"></span>• [temptable\\_max\\_mmap](#page-21-0)

| Command-Line Format  | temptable-max-mmap=# |
|----------------------|----------------------|
| System Variable      | temptable_max_mmap   |
| Scope                | Global               |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | No                   |
| Type                 | Integer              |
| Default Value        | 1073741824           |
| Minimum Value        | 0                    |
| Maximum Value        | 2^64-1               |
| Unit                 | bytes                |

Defines the maximum amount of memory (in bytes) the TempTable storage engine is permitted to allocate from memory-mapped temporary files before it starts storing data to InnoDB internal temporary tables on disk. A setting of 0 disables allocation of memory from memory-mapped temporary files. For more information, see Section 10.4.4, "Internal Temporary Table Use in MySQL".

### <span id="page-21-1"></span>• [temptable\\_max\\_ram](#page-21-1)

| Command-Line Format  | temptable-max-ram=# |
|----------------------|---------------------|
| System Variable      | temptable_max_ram   |
| Scope                | Global              |
| Dynamic              | Yes                 |
| SET_VAR Hint Applies | No                  |
| Type                 | Integer             |
| Default Value        | 1073741824          |
| Minimum Value        | 2097152             |

| Maximum Value | 2^64-1 |
|---------------|--------|
| Unit          | bytes  |

Defines the maximum amount of memory that can be occupied by the TempTable storage engine before it starts storing data on disk. The default value is 1073741824 bytes (1GiB). For more information, see Section 10.4.4, "Internal Temporary Table Use in MySQL".

<span id="page-22-0"></span>• [temptable\\_use\\_mmap](#page-22-0)

| Command-Line Format  | temptable-use-mmap[={OFF ON}] |
|----------------------|-------------------------------|
| Deprecated           | Yes                           |
| System Variable      | temptable_use_mmap            |
| Scope                | Global                        |
| Dynamic              | Yes                           |
| SET_VAR Hint Applies | No                            |
| Type                 | Boolean                       |
| Default Value        | ON                            |

Defines whether the TempTable storage engine allocates space for internal in-memory temporary tables as memory-mapped temporary files when the amount of memory occupied by the TempTable storage engine exceeds the limit defined by the [temptable\\_max\\_ram](#page-21-1) variable. When [temptable\\_use\\_mmap](#page-22-0) is disabled, the TempTable storage engine uses InnoDB on-disk internal temporary tables instead. For more information, see Section 10.4.4, "Internal Temporary Table Use in MySQL".

<span id="page-22-1"></span>• [thread\\_cache\\_size](#page-22-1)

| Command-Line Format  | thread-cache-size=#                                            |
|----------------------|----------------------------------------------------------------|
| System Variable      | thread_cache_size                                              |
| Scope                | Global                                                         |
| Dynamic              | Yes                                                            |
| SET_VAR Hint Applies | No                                                             |
| Type                 | Integer                                                        |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value        | 0                                                              |
| Maximum Value        | 16384                                                          |

How many threads the server should cache for reuse. When a client disconnects, the client's threads are put in the cache if there are fewer than [thread\\_cache\\_size](#page-22-1) threads there. Requests for threads are satisfied by reusing threads taken from the cache if possible, and only when the cache is empty is a new thread created. This variable can be increased to improve performance if you have a lot of new connections. Normally, this does not provide a notable performance improvement if you have a good thread implementation. However, if your server sees hundreds of connections per second you should normally set [thread\\_cache\\_size](#page-22-1) high enough so that most new connections use cached threads. By examining the difference between the [Connections](#page-74-0) and [Threads\\_created](#page-97-0) status variables, you can see how efficient the thread cache is. For details, see [Section 7.1.10, "Server Status Variables"](#page-70-0).

The default value is based on the following formula, capped to a limit of 100:

### <span id="page-23-0"></span>• [thread\\_handling](#page-23-0)

| Command-Line Format  | thread-handling=name      |
|----------------------|---------------------------|
| System Variable      | thread_handling           |
| Scope                | Global                    |
| Dynamic              | No                        |
| SET_VAR Hint Applies | No                        |
| Type                 | Enumeration               |
| Default Value        | one-thread-per-connection |
| Valid Values         | no-threads                |
|                      | one-thread-per-connection |
|                      | loaded-dynamically        |

The thread-handling model used by the server for connection threads. The permissible values are no-threads (the server uses a single thread to handle one connection), one-threadper-connection (the server uses one thread to handle each client connection), and loadeddynamically (set by the thread pool plugin when it initializes). no-threads is useful for debugging under Linux; see Section 7.9, "Debugging MySQL".

### <span id="page-23-1"></span>• [thread\\_pool\\_algorithm](#page-23-1)

| Command-Line Format  | thread-pool-algorithm=# |
|----------------------|-------------------------|
| System Variable      | thread_pool_algorithm   |
| Scope                | Global                  |
| Dynamic              | No                      |
| SET_VAR Hint Applies | No                      |
| Type                 | Integer                 |
| Default Value        | 0                       |
| Minimum Value        | 0                       |
| Maximum Value        | 1                       |

This variable controls which algorithm the thread pool plugin uses:

- 0: Use a conservative low-concurrency algorithm.
- 1: Use an aggressive high-currency algorithm which performs better with optimal thread counts, but performance may be degraded if the number of connections reaches extremely high values.

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-23-2"></span>• [thread\\_pool\\_dedicated\\_listeners](#page-23-2)

| Command-Line Format  | thread-pool-dedicated-listeners |
|----------------------|---------------------------------|
| System Variable      | thread_pool_dedicated_listeners |
| Scope                | Global                          |
| Dynamic              | No                              |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |

| Default Value | OFF |
|---------------|-----|
|---------------|-----|

Dedicates a listener thread in each thread group to listen for incoming statements from connections assigned to the group.

- OFF: (Default) Disables dedicated listener threads.
- ON: Dedicates a listener thread in each thread group to listen for incoming statements from connections assigned to the group. Dedicated listener threads do not execute queries.

Enabling [thread\\_pool\\_dedicated\\_listeners](#page-23-2) is only useful when a transaction limit is defined by thread\_pool\_max\_transactions\_limit. Otherwise, [thread\\_pool\\_dedicated\\_listeners](#page-23-2) should not be enabled.

MySQL HeatWave Service introduced this variable in MySQL 8.0.23. It is available with MySQL Enterprise Edition from MySQL 8.0.31.

<span id="page-24-0"></span>• [thread\\_pool\\_high\\_priority\\_connection](#page-24-0)

| Command-Line Format  | thread-pool-high-priority<br>connection=# |
|----------------------|-------------------------------------------|
| System Variable      | thread_pool_high_priority_connection      |
| Scope                | Global, Session                           |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |
| Default Value        | 0                                         |
| Minimum Value        | 0                                         |
| Maximum Value        | 1                                         |

This variable affects queuing of new statements prior to execution. If the value is 0 (false, the default), statement queuing uses both the low-priority and high-priority queues. If the value is 1 (true), queued statements always go to the high-priority queue.

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-24-1"></span>• [thread\\_pool\\_max\\_active\\_query\\_threads](#page-24-1)

| Command-Line Format  | thread-pool-max-active-query<br>threads |
|----------------------|-----------------------------------------|
| System Variable      | thread_pool_max_active_query_threads    |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Integer                                 |
| Default Value        | 0                                       |
| Minimum Value        | 0                                       |

| Maximum Value | 512 |  |
|---------------|-----|--|
|---------------|-----|--|

The maximum permissible number of active (running) query threads per group. If the value is 0, the thread pool plugin uses up to as many threads as are available.

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-25-0"></span>• [thread\\_pool\\_max\\_transactions\\_limit](#page-25-0)

| Command-Line Format  | thread-pool-max-transactions-limit |
|----------------------|------------------------------------|
| System Variable      | thread_pool_max_transactions_limit |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Integer                            |
| Default Value        | 0                                  |
| Minimum Value        | 0                                  |
| Maximum Value        | 1000000                            |

The maximum number of transactions permitted by the thread pool plugin. Defining a transaction limit binds a thread to a transaction until it commits, which helps stabilize throughput during high concurrency.

The default value of 0 means that there is no transaction limit. The variable is dynamic but cannot be changed from 0 to a higher value at runtime and vice versa. A non-zero value at startup permits dynamic configuration at runtime. The CONNECTION\_ADMIN privilege is required to configure thread\_pool\_max\_transactions\_limit at runtime.

When you define a transaction limit, enabling [thread\\_pool\\_dedicated\\_listeners](#page-23-2) creates a dedicated listener thread in each thread group. The additional dedicated listener thread consumes more resources and affects thread pool performance. [thread\\_pool\\_dedicated\\_listeners](#page-23-2) should therefore be used cautiously.

When the limit defined by [thread\\_pool\\_max\\_transactions\\_limit](#page-25-0) has been reached, new connections appear to hang until one or more existing transactions are completed. The same occurs when attempting to start a new transaction on an existing connection. If existing connections are blocked or long-running, a privileged connection may be required to access the server to increase the limit, remove the limit, or kill running transactions. See Privileged Connections.

MySQL HeatWave Service introduced this variable in MySQL 8.0.23. It is available with MySQL Enterprise Edition in from MySQL 8.0.31.

<span id="page-25-1"></span>• [thread\\_pool\\_max\\_unused\\_threads](#page-25-1)

| Command-Line Format  | thread-pool-max-unused-threads=# |
|----------------------|----------------------------------|
| System Variable      | thread_pool_max_unused_threads   |
| Scope                | Global                           |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Integer                          |
| Default Value        | 0                                |
| Minimum Value        | 0                                |

| Maximum Value | 4096 |
|---------------|------|
|---------------|------|

The maximum permitted number of unused threads in the thread pool. This variable makes it possible to limit the amount of memory used by sleeping threads.

A value of 0 (the default) means no limit on the number of sleeping threads. A value of N where N is greater than 0 means 1 consumer thread and N−1 reserve threads. In this case, if a thread is ready to sleep but the number of sleeping threads is already at the maximum, the thread exits rather than going to sleep.

A sleeping thread is either sleeping as a consumer thread or a reserve thread. The thread pool permits one thread to be the consumer thread when sleeping. If a thread goes to sleep and there is no existing consumer thread, it sleeps as a consumer thread. When a thread must be woken up, a consumer thread is selected if there is one. A reserve thread is selected only when there is no consumer thread to wake up.

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-26-0"></span>• [thread\\_pool\\_prio\\_kickup\\_timer](#page-26-0)

| Command-Line Format  | thread-pool-prio-kickup-timer=# |
|----------------------|---------------------------------|
| System Variable      | thread_pool_prio_kickup_timer   |
| Scope                | Global                          |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | Integer                         |
| Default Value        | 1000                            |
| Minimum Value        | 0                               |
| Maximum Value        | 4294967294                      |
| Unit                 | milliseconds                    |

This variable affects statements waiting for execution in the low-priority queue. The value is the number of milliseconds before a waiting statement is moved to the high-priority queue. The default is 1000 (1 second).

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-26-1"></span>• [thread\\_pool\\_query\\_threads\\_per\\_group](#page-26-1)

| Command-Line Format  | thread-pool-query-threads-per       |
|----------------------|-------------------------------------|
|                      | group                               |
| System Variable      | thread_pool_query_threads_per_group |
| Scope                | Global                              |
| Dynamic              | Yes                                 |
| SET_VAR Hint Applies | No                                  |
| Type                 | Integer                             |
| Default Value        | 1                                   |
| Minimum Value        | 1                                   |

| Maximum Value | 4096 |  |
|---------------|------|--|
|---------------|------|--|

The maximum number of query threads permitted in a thread group. The maximum value is 4096, but if [thread\\_pool\\_max\\_transactions\\_limit](#page-25-0) is set, [thread\\_pool\\_query\\_threads\\_per\\_group](#page-26-1) must not exceed that value.

The default value of 1 means there is one active query thread in each thread group, which works well for many loads. When you are using the high concurrency thread pool algorithm (thread\_pool\_algorithm = 1), consider increasing the value if you experience slower response times due to long-running transactions.

The CONNECTION\_ADMIN privilege is required to configure [thread\\_pool\\_query\\_threads\\_per\\_group](#page-26-1) at runtime.

If you decrease the value of [thread\\_pool\\_query\\_threads\\_per\\_group](#page-26-1) at runtime, threads that are currently running user queries are allowed to complete, then moved to the reserve pool or terminated. if you increment the value at runtime and the thread group needs more threads, these are taken from the reserve pool if possible, otherwise they are created.

This variable is available from MySQL 8.0.31 in MySQL HeatWave Service and MySQL Enterprise Edition.

<span id="page-27-0"></span>• [thread\\_pool\\_size](#page-27-0)

| Command-Line Format  | thread-pool-size=# |
|----------------------|--------------------|
| System Variable      | thread_pool_size   |
| Scope                | Global             |
| Dynamic              | No                 |
| SET_VAR Hint Applies | No                 |
| Type                 | Integer            |
| Default Value        | 16                 |
| Minimum Value        | 1                  |
| Maximum Value        | 512                |

The number of thread groups in the thread pool. This is the most important parameter controlling thread pool performance. It affects how many statements can execute simultaneously. If a value outside the range of permissible values is specified, the thread pool plugin does not load and the server writes a message to the error log.

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-27-1"></span>• [thread\\_pool\\_stall\\_limit](#page-27-1)

| Command-Line Format  | thread-pool-stall-limit=# |
|----------------------|---------------------------|
| System Variable      | thread_pool_stall_limit   |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | Integer                   |
| Default Value        | 6                         |
| Minimum Value        | 4                         |
| Maximum Value        | 600                       |

| Unit<br>milliseconds * 10 |  |
|---------------------------|--|
|---------------------------|--|

This variable affects executing statements. The value is the amount of time a statement has to finish after starting to execute before it becomes defined as stalled, at which point the thread pool permits the thread group to begin executing another statement. The value is measured in 10 millisecond units, so the default of 6 means 60ms. Short wait values permit threads to start more quickly. Short values are also better for avoiding deadlock situations. Long wait values are useful for workloads that include long-running statements, to avoid starting too many new statements while the current ones execute.

This variable is available only if the thread pool plugin is enabled. See Section 7.6.3, "MySQL Enterprise Thread Pool".

<span id="page-28-0"></span>• [thread\\_pool\\_transaction\\_delay](#page-28-0)

| Command-Line Format  | thread-pool-transaction-delay |
|----------------------|-------------------------------|
| System Variable      | thread_pool_transaction_delay |
| Scope                | Global                        |
| Dynamic              | Yes                           |
| SET_VAR Hint Applies | No                            |
| Type                 | Integer                       |
| Default Value        | 0                             |
| Minimum Value        | 0                             |
| Maximum Value        | 300000                        |

The delay period before executing a new transaction, in milliseconds. The maximum value is 300000 (5 minutes).

A transaction delay can be used in cases where parallel transactions affect the performance of other operations due to resource contention. For example, if parallel transactions affect index creation or an online buffer pool resizing operation, you can configure a transaction delay to reduce resource contention while those operations are running.

Worker threads sleep for the number of milliseconds specified by thread\_pool\_transaction\_delay before executing a new transaction.

The thread\_pool\_transaction\_delay setting does not affect queries issued from a privileged connection (a connection assigned to the Admin thread group). These queries are not subject to a configured transaction delay.

<span id="page-28-1"></span>• [thread\\_stack](#page-28-1)

| Command-Line Format              | thread-stack=#       |
|----------------------------------|----------------------|
| System Variable                  | thread_stack         |
| Scope                            | Global               |
| Dynamic                          | No                   |
| SET_VAR Hint Applies             | No                   |
| Type                             | Integer              |
| Default Value                    | 1048576              |
| Minimum Value                    | 131072               |
| Maximum Value (64-bit platforms) | 18446744073709550592 |
| Maximum Value (32-bit platforms) | 4294966272           |

| Unit       | bytes |
|------------|-------|
| Block Size | 1024  |

The stack size for each thread. The default is large enough for normal operation. If the thread stack size is too small, it limits the complexity of the SQL statements that the server can handle, the recursion depth of stored procedures, and other memory-consuming actions.

#### <span id="page-29-0"></span>• [time\\_zone](#page-29-0)

| System Variable      | time_zone       |
|----------------------|-----------------|
| Scope                | Global, Session |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | Yes             |
| Type                 | String          |
| Default Value        | SYSTEM          |
| Minimum Value        | -13:59          |
| Maximum Value        | +14:00          |

The current time zone. This variable is used to initialize the time zone for each client that connects. By default, the initial value of this is 'SYSTEM' (which means, "use the value of [system\\_time\\_zone](#page-18-0)"). The value can be specified explicitly at server startup with the --defaulttime-zone option. See [Section 7.1.15, "MySQL Server Time Zone Support"](#page-126-0).

![](_page_29_Picture_6.jpeg)

#### **Note**

If set to SYSTEM, every MySQL function call that requires a time zone calculation makes a system library call to determine the current system time zone. This call may be protected by a global mutex, resulting in contention.

### <span id="page-29-1"></span>• [timestamp](#page-29-1)

| System Variable      | timestamp        |
|----------------------|------------------|
| Scope                | Session          |
| Dynamic              | Yes              |
| SET_VAR Hint Applies | Yes              |
| Type                 | Numeric          |
| Default Value        | UNIX_TIMESTAMP() |
| Minimum Value        | 1                |

| Maximum Value | 2147483647 |
|---------------|------------|
|---------------|------------|

Set the time for this client. This is used to get the original timestamp if you use the binary log to restore rows. timestamp\_value should be a Unix epoch timestamp (a value like that returned by UNIX\_TIMESTAMP(), not a value in 'YYYY-MM-DD hh:mm:ss' format) or DEFAULT.

Setting [timestamp](#page-29-1) to a constant value causes it to retain that value until it is changed again. Setting [timestamp](#page-29-1) to DEFAULT causes its value to be the current date and time as of the time it is accessed.

[timestamp](#page-29-1) is a DOUBLE rather than BIGINT because its value includes a microseconds part. The maximum value corresponds to '2038-01-19 03:14:07' UTC, the same as for the TIMESTAMP data type.

SET timestamp affects the value returned by NOW() but not by SYSDATE(). This means that timestamp settings in the binary log have no effect on invocations of SYSDATE(). The server can be started with the --sysdate-is-now option to cause SYSDATE() to be a synonym for NOW(), in which case SET timestamp affects both functions.

#### <span id="page-30-0"></span>• [tls\\_ciphersuites](#page-30-0)

| Command-Line Format  | tls-ciphersuites=ciphersuite_list |
|----------------------|-----------------------------------|
| System Variable      | tls_ciphersuites                  |
| Scope                | Global                            |
| Dynamic              | Yes                               |
| SET_VAR Hint Applies | No                                |
| Type                 | String                            |
| Default Value        | NULL                              |

Which ciphersuites the server permits for encrypted connections that use TLSv1.3. The value is a list of zero or more colon-separated ciphersuite names.

The ciphersuites that can be named for this variable depend on the SSL library used to compile MySQL. If this variable is not set, its default value is NULL, which means that the server permits the default set of ciphersuites. If the variable is set to the empty string, no ciphersuites are enabled and encrypted connections cannot be established. For more information, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

### <span id="page-30-1"></span>• [tls\\_version](#page-30-1)

| Command-Line Format  | tls-version=protocol_list |
|----------------------|---------------------------|
| System Variable      | tls_version               |
| Scope                | Global                    |
| Dynamic              | Yes                       |
| SET_VAR Hint Applies | No                        |
| Type                 | String                    |
| Default Value        | TLSv1.2,TLSv1.3           |

Which protocols the server permits for encrypted connections. The value is a list of one or more comma-separated protocol names, which are not case-sensitive. The protocols that can be named for this variable depend on the SSL library used to compile MySQL. Permitted protocols should be

chosen such as not to leave "holes" in the list. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

As of MySQL 8.0.16, this variable is dynamic and can be modified at runtime to affect the TLS context the server uses for new connections. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections. Prior to MySQL 8.0.16, this variable can be set only at server startup.

![](_page_31_Picture_3.jpeg)

#### **Important**

- Support for the TLSv1 and TLSv1.1 connection protocols is removed from MySQL Server as of MySQL 8.0.28. The protocols were deprecated from MySQL 8.0.26. See Removal of Support for the TLSv1 and TLSv1.1 Protocols for more information.
- Support for the TLSv1.3 protocol is available in MySQL Server as of MySQL 8.0.16, provided that MySQL Server was compiled using OpenSSL 1.1.1 or higher. The server checks the version of OpenSSL at startup, and if it is lower than 1.1.1, TLSv1.3 is removed from the default value for the system variable. In that case, the defaults are "TLSv1,TLSv1.1,TLSv1.2" up to and including MySQL 8.0.27, and "TLSv1.2" from MySQL 8.0.28.

Setting this variable to an empty string disables encrypted connections.

<span id="page-31-0"></span>• [tmp\\_table\\_size](#page-31-0)

| Command-Line Format  | tmp-table-size=#     |
|----------------------|----------------------|
| System Variable      | tmp_table_size       |
| Scope                | Global, Session      |
| Dynamic              | Yes                  |
| SET_VAR Hint Applies | Yes                  |
| Type                 | Integer              |
| Default Value        | 16777216             |
| Minimum Value        | 1024                 |
| Maximum Value        | 18446744073709551615 |

| Unit<br>bytes |  |
|---------------|--|
|---------------|--|

Defines the maximum size of internal in-memory temporary tables created by the MEMORY storage engine and, as of MySQL 8.0.28, the TempTable storage engine. If an internal in-memory temporary table exceeds this size, it is automatically converted to an on-disk internal temporary table.

The [tmp\\_table\\_size](#page-31-0) variable does not apply to user-created MEMORY tables. User-created TempTable tables are not supported.

When using the MEMORY storage engine for internal in-memory temporary tables, the actual size limit is the smaller of [tmp\\_table\\_size](#page-31-0) and max\_heap\_table\_size. The max\_heap\_table\_size setting does not apply to TempTable tables.

Increase the value of [tmp\\_table\\_size](#page-31-0) (and max\_heap\_table\_size if necessary when using the MEMORY storage engine for internal in-memory temporary tables) if you do many advanced GROUP BY queries and you have lots of memory.

You can compare the number of internal on-disk temporary tables created to the total number of internal temporary tables created by comparing [Created\\_tmp\\_disk\\_tables](#page-74-1) and [Created\\_tmp\\_tables](#page-74-2) values.

See also Section 10.4.4, "Internal Temporary Table Use in MySQL".

#### <span id="page-32-0"></span>• [tmpdir](#page-32-0)

| Command-Line Format  | tmpdir=dir_name |
|----------------------|-----------------|
| System Variable      | tmpdir          |
| Scope                | Global          |
| Dynamic              | No              |
| SET_VAR Hint Applies | No              |
| Type                 | Directory name  |

The path of the directory to use for creating temporary files. It might be useful if your default /tmp directory resides on a partition that is too small to hold temporary tables. This variable can be set to a list of several paths that are used in round-robin fashion. Paths should be separated by colon characters (:) on Unix and semicolon characters (;) on Windows.

[tmpdir](#page-32-0) can be a non-permanent location, such as a directory on a memory-based file system or a directory that is cleared when the server host restarts. If the MySQL server is acting as a replica, and you are using a non-permanent location for [tmpdir](#page-32-0), consider setting a different temporary directory for the replica using the replica\_load\_tmpdir or slave\_load\_tmpdir variable. For a replica, the temporary files used to replicate LOAD DATA statements are stored in this directory, so with a permanent location they can survive machine restarts, although replication can now continue after a restart if the temporary files have been removed.

For more information about the storage location of temporary files, see Section B.3.3.5, "Where MySQL Stores Temporary Files".

### <span id="page-32-1"></span>• [transaction\\_alloc\\_block\\_size](#page-32-1)

| Command-Line Format  | transaction-alloc-block-size=# |
|----------------------|--------------------------------|
| System Variable      | transaction_alloc_block_size   |
| Scope                | Global, Session                |
| Dynamic              | Yes                            |
| SET_VAR Hint Applies | No                             |

| Type          | Integer |
|---------------|---------|
| Default Value | 8192    |
| Minimum Value | 1024    |
| Maximum Value | 131072  |
| Unit          | bytes   |
| Block Size    | 1024    |

The amount in bytes by which to increase a per-transaction memory pool which needs memory. See the description of [transaction\\_prealloc\\_size](#page-34-0).

<span id="page-33-0"></span>• [transaction\\_isolation](#page-33-0)

| Command-Line Format  | transaction-isolation=name |
|----------------------|----------------------------|
| System Variable      | transaction_isolation      |
| Scope                | Global, Session            |
| Dynamic              | Yes                        |
| SET_VAR Hint Applies | No                         |
| Type                 | Enumeration                |
| Default Value        | REPEATABLE-READ            |
| Valid Values         | READ-UNCOMMITTED           |
|                      | READ-COMMITTED             |
|                      | REPEATABLE-READ            |
|                      | SERIALIZABLE               |

The transaction isolation level. The default is REPEATABLE-READ.

The transaction isolation level has three scopes: global, session, and next transaction. This three-scope implementation leads to some nonstandard isolation-level assignment semantics, as described later.

To set the global transaction isolation level at startup, use the --transaction-isolation server option.

At runtime, the isolation level can be set directly using the SET statement to assign a value to the [transaction\\_isolation](#page-33-0) system variable, or indirectly using the SET TRANSACTION statement. If you set [transaction\\_isolation](#page-33-0) directly to an isolation level name that contains a space, the name should be enclosed within quotation marks, with the space replaced by a dash. For example, use this SET statement to set the global value:

```
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
```

Setting the global [transaction\\_isolation](#page-33-0) value sets the isolation level for all subsequent sessions. Existing sessions are unaffected.

To set the session or next-level [transaction\\_isolation](#page-33-0) value, use the SET statement. For most session system variables, these statements are equivalent ways to set the value:

```
SET @@SESSION.var_name = value;
SET SESSION var_name = value;
SET var_name = value;
```

```
SET @@var_name = value;
```

As mentioned previously, the transaction isolation level has a next-transaction scope, in addition to the global and session scopes. To enable the next-transaction scope to be set, SET syntax for assigning session system variable values has nonstandard semantics for [transaction\\_isolation](#page-33-0):

• To set the session isolation level, use any of these syntaxes:

```
SET @@SESSION.transaction_isolation = value;
SET SESSION transaction_isolation = value;
SET transaction_isolation = value;
```

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

For more information about SET TRANSACTION and its relationship to the [transaction\\_isolation](#page-33-0) system variable, see Section 15.3.7, "SET TRANSACTION Statement".

<span id="page-34-0"></span>• [transaction\\_prealloc\\_size](#page-34-0)

| Command-Line Format  | transaction-prealloc-size=# |
|----------------------|-----------------------------|
| Deprecated           | Yes                         |
| System Variable      | transaction_prealloc_size   |
| Scope                | Global, Session             |
| Dynamic              | Yes                         |
| SET_VAR Hint Applies | No                          |
| Type                 | Integer                     |
| Default Value        | 4096                        |
| Minimum Value        | 1024                        |
| Maximum Value        | 131072                      |
| Unit                 | bytes                       |

| Block Size | 1024 |
|------------|------|
|------------|------|

There is a per-transaction memory pool from which various transaction-related allocations take memory. The initial size of the pool in bytes is transaction\_prealloc\_size. For every allocation that cannot be satisfied from the pool because it has insufficient memory available, the pool is increased by [transaction\\_alloc\\_block\\_size](#page-32-1) bytes. When the transaction ends, the pool is truncated to transaction\_prealloc\_size bytes. By making transaction\_prealloc\_size sufficiently large to contain all statements within a single transaction, you can avoid many malloc() calls.

Beginning with MySQL 8.0.29, transaction\_prealloc\_size is deprecated; the initial size of the transaction memory pool is fixed, and setting this variable no longer has any effect. (The functioning of transaction\_alloc\_block\_size is unaffected by this change.) Expect transaction\_prealloc\_size to be removed in a future release of MySQL.

<span id="page-35-0"></span>• [transaction\\_read\\_only](#page-35-0)

| Command-Line Format  | transaction-read-only[={OFF ON}] |
|----------------------|----------------------------------|
| System Variable      | transaction_read_only            |
| Scope                | Global, Session                  |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Boolean                          |
| Default Value        | OFF                              |

The transaction access mode. The value can be OFF (read/write; the default) or ON (read only).

The transaction access mode has three scopes: global, session, and next transaction. This threescope implementation leads to some nonstandard access-mode assignment semantics, as described later.

To set the global transaction access mode at startup, use the --transaction-read-only server option.

At runtime, the access mode can be set directly using the SET statement to assign a value to the [transaction\\_read\\_only](#page-35-0) system variable, or indirectly using the SET TRANSACTION statement. For example, use this SET statement to set the global value:

```
SET GLOBAL transaction_read_only = ON;
```

Setting the global [transaction\\_read\\_only](#page-35-0) value sets the access mode for all subsequent sessions. Existing sessions are unaffected.

To set the session or next-level [transaction\\_read\\_only](#page-35-0) value, use the SET statement. For most session system variables, these statements are equivalent ways to set the value:

```
SET @@SESSION.var_name = value;
SET SESSION var_name = value;
SET var_name = value;
SET @@var_name = value;
```

As mentioned previously, the transaction access mode has a next-transaction scope, in addition to the global and session scopes. To enable the next-transaction scope to be set, SET syntax for assigning session system variable values has nonstandard semantics for [transaction\\_read\\_only](#page-35-0),

• To set the session access mode, use any of these syntaxes:

```
SET @@SESSION.transaction_read_only = value;
```

```
SET SESSION transaction_read_only = value;
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

For more information about SET TRANSACTION and its relationship to the [transaction\\_read\\_only](#page-35-0) system variable, see Section 15.3.7, "SET TRANSACTION Statement".

<span id="page-36-0"></span>• [unique\\_checks](#page-36-0)

| System Variable      | unique_checks   |
|----------------------|-----------------|
| Scope                | Global, Session |
| Dynamic              | Yes             |
| SET_VAR Hint Applies | Yes             |
| Type                 | Boolean         |
| Default Value        | ON              |

If set to 1 (the default), uniqueness checks for secondary indexes in InnoDB tables are performed. If set to 0, storage engines are permitted to assume that duplicate keys are not present in input data. If you know for certain that your data does not contain uniqueness violations, you can set this to 0 to speed up large table imports to InnoDB.

Setting this variable to 0 does not require storage engines to ignore duplicate keys. An engine is still permitted to check for them and issue duplicate-key errors if it detects them.

<span id="page-36-1"></span>• [updatable\\_views\\_with\\_limit](#page-36-1)

| Command-Line Format  | updatable-views-with-limit[={OFF <br>ON}] |
|----------------------|-------------------------------------------|
| System Variable      | updatable_views_with_limit                |
| Scope                | Global, Session                           |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | Yes                                       |

| Type          | Boolean |
|---------------|---------|
| Default Value | 1       |

This variable controls whether updates to a view can be made when the view does not contain all columns of the primary key defined in the underlying table, if the update statement contains a LIMIT clause. (Such updates often are generated by GUI tools.) An update is an UPDATE or DELETE statement. Primary key here means a PRIMARY KEY, or a UNIQUE index in which no column can contain NULL.

The variable can have two values:

- 1 or YES: Issue a warning only (not an error message). This is the default value.
- 0 or NO: Prohibit the update.
- [use\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_use_secondary_engine)

For use with MySQL HeatWave only. See [System Variables](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md), for more information.

• validate\_password.xxx

The validate\_password component implements a set of system variables having names of the form validate\_password.xxx. These variables affect password testing by that component; see Section 8.4.3.2, "Password Validation Options and Variables".

<span id="page-37-0"></span>• [version](#page-37-0)

The version number for the server. The value might also include a suffix indicating server build or configuration information. -debug indicates that the server was built with debugging support enabled.

<span id="page-37-1"></span>• [version\\_comment](#page-37-1)

| System Variable      | version_comment |
|----------------------|-----------------|
| Scope                | Global          |
| Dynamic              | No              |
| SET_VAR Hint Applies | No              |
| Type                 | String          |

The CMake configuration program has a COMPILATION\_COMMENT\_SERVER option that permits a comment to be specified when building MySQL. This variable contains the value of that comment. (Prior to MySQL 8.0.14, [version\\_comment](#page-37-1) is set by the COMPILATION\_COMMENT option.) See Section 2.8.7, "MySQL Source-Configuration Options".

<span id="page-37-2"></span>• [version\\_compile\\_machine](#page-37-2)

| System Variable      | version_compile_machine |
|----------------------|-------------------------|
| Scope                | Global                  |
| Dynamic              | No                      |
| SET_VAR Hint Applies | No                      |
| Type                 | String                  |

The type of the server binary.

<span id="page-37-3"></span>• [version\\_compile\\_os](#page-37-3)

| System Variable | version_compile_os |
|-----------------|--------------------|
|-----------------|--------------------|

| Scope                | Global |
|----------------------|--------|
| Dynamic              | No     |
| SET_VAR Hint Applies | No     |
| Type                 | String |

The type of operating system on which MySQL was built.

<span id="page-38-1"></span>• [version\\_compile\\_zlib](#page-38-1)

| System Variable      | version_compile_zlib |
|----------------------|----------------------|
| Scope                | Global               |
| Dynamic              | No                   |
| SET_VAR Hint Applies | No                   |
| Type                 | String               |

The version of the compiled-in zlib library.

<span id="page-38-2"></span>• [wait\\_timeout](#page-38-2)

| Command-Line Format     | wait-timeout=#  |
|-------------------------|-----------------|
| System Variable         | wait_timeout    |
| Scope                   | Global, Session |
| Dynamic                 | Yes             |
| SET_VAR Hint Applies    | No              |
| Type                    | Integer         |
| Default Value           | 28800           |
| Minimum Value           | 1               |
| Maximum Value (Windows) | 2147483         |
| Maximum Value (Other)   | 31536000        |
| Unit                    | seconds         |

The number of seconds the server waits for activity on a noninteractive connection before closing it.

On thread startup, the session [wait\\_timeout](#page-38-2) value is initialized from the global [wait\\_timeout](#page-38-2) value or from the global interactive\_timeout value, depending on the type of client (as defined by the CLIENT\_INTERACTIVE connect option to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md)). See also interactive\_timeout.

<span id="page-38-0"></span>• [warning\\_count](#page-38-0)

The number of errors, warnings, and notes that resulted from the last statement that generated messages. This variable is read only. See Section 15.7.7.42, "SHOW WARNINGS Statement".

<span id="page-38-3"></span>• [windowing\\_use\\_high\\_precision](#page-38-3)

| Command-Line Format  | windowing-use-high<br>precision[={OFF ON}] |  |
|----------------------|--------------------------------------------|--|
| System Variable      | windowing_use_high_precision               |  |
| Scope                | Global, Session                            |  |
| Dynamic              | Yes                                        |  |
| SET_VAR Hint Applies | Yes                                        |  |

| Type          | Boolean |
|---------------|---------|
| Default Value | ON      |

Whether to compute window operations without loss of precision. See Section 10.2.1.21, "Window Function Optimization".

<span id="page-39-0"></span>• [xa\\_detach\\_on\\_prepare](#page-39-0)

| Command-Line Format  | xa-detach-on-prepare[={OFF ON}] |
|----------------------|---------------------------------|
| System Variable      | xa_detach_on_prepare            |
| Scope                | Global, Session                 |
| Dynamic              | Yes                             |
| SET_VAR Hint Applies | No                              |
| Type                 | Boolean                         |
| Default Value        | ON                              |

When set to ON (enabled), all XA transactions are detached (disconnected) from the connection (session) as part of XA PREPARE. This means that the XA transaction can be committed or rolled back by another connection, even if the originating connection has not terminated, and this connection can start new transactions.

Temporary tables cannot be used inside detached XA transactions.

When this is OFF (disabled), an XA transaction is strictly associated with the same connection until the session disconnects. It is recommended that you allow it to be enabled (the default behavior) for replication.

For more information, see Section 15.3.8.2, "XA Transaction States".

# <span id="page-39-1"></span>**7.1.9 Using System Variables**

The MySQL server maintains many system variables that configure its operation. Section 7.1.8, "Server System Variables", describes the meaning of these variables. Each system variable has a default value. System variables can be set at server startup using options on the command line or in an option file. Most of them can be changed dynamically while the server is running by means of the SET statement, which enables you to modify operation of the server without having to stop and restart it. You can also use system variable values in expressions.

Many system variables are built in. System variables may also be installed by server plugins or components:

- System variables implemented by a server plugin are exposed when the plugin is installed and have names that begin with the plugin name. For example, the audit\_log plugin implements a system variable named audit\_log\_policy.
- System variables implemented by a component are exposed when the component is installed and have names that begin with a component-specific prefix. For example, the log\_filter\_dragnet error log filter component implements a system variable named log\_error\_filter\_rules, the full name of which is dragnet.log\_error\_filter\_rules. To refer to this variable, use the full name.

There are two scopes in which system variables exist. Global variables affect the overall operation of the server. Session variables affect its operation for individual client connections. A given system variable can have both a global and a session value. Global and session system variables are related as follows:

- When the server starts, it initializes each global variable to its default value. These defaults can be changed by options specified on the command line or in an option file. (See Section 6.2.2, "Specifying Program Options".)
- The server also maintains a set of session variables for each client that connects. The client's session variables are initialized at connect time using the current values of the corresponding global variables. For example, a client's SQL mode is controlled by the session sql\_mode value, which is initialized when the client connects to the value of the global sql\_mode value.

For some system variables, the session value is not initialized from the corresponding global value; if so, that is indicated in the variable description.

System variable values can be set globally at server startup by using options on the command line or in an option file. At startup, the syntax for system variables is the same as for command options, so within variable names, dashes and underscores may be used interchangeably. For example, --general\_log=ON and --general-log=ON are equivalent.

When you use a startup option to set a variable that takes a numeric value, the value can be given with a suffix of  $\mathbb{K}$ ,  $\mathbb{M}$ , or  $\mathbb{G}$  (either uppercase or lowercase) to indicate a multiplier of 1024, 1024<sup>2</sup> or 1024<sup>3</sup>; that is, units of kilobytes, megabytes, or gigabytes, respectively. As of MySQL 8.0.14, a suffix can also be  $\mathbb{T}$ ,  $\mathbb{P}$ , and  $\mathbb{E}$  to indicate a multiplier of 1024<sup>4</sup>, 1024<sup>5</sup> or 1024<sup>6</sup>. Thus, the following command starts the server with a sort buffer size of 256 kilobytes and a maximum packet size of one gigabyte:

```
mysqld --sort-buffer-size=256K --max-allowed-packet=1G
```

Within an option file, those variables are set like this:

```
[mysqld]
sort_buffer_size=256K
max_allowed_packet=1G
```

The lettercase of suffix letters does not matter; 256k and 256k are equivalent, as are 1g and 1g.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement, specify this maximum by using an option of the form  $--maximum-var\_name=value$  at server startup. For example, to prevent the value of  $sort\_buffer\_size$  from being increased to more than 32MB at runtime, use the option --maximum-sort-buffer-size=32M.

Many system variables are dynamic and can be changed at runtime by using the SET statement. For a list, see Section 7.1.9.2, "Dynamic System Variables". To change a system variable with SET, refer to it by name, optionally preceded by a modifier. At runtime, system variable names must be written using underscores, not dashes. The following examples briefly illustrate this syntax:

· Set a global system variable:

```
SET GLOBAL max_connections = 1000;
SET @@GLOBAL.max_connections = 1000;
```

Persist a global system variable to the mysqld-auto.cnf file (and set the runtime value):

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
```

Persist a global system variable to the mysgld-auto.cnf file (without setting the runtime value):

```
SET PERSIST_ONLY back_log = 1000;
SET @@PERSIST_ONLY.back_log = 1000;
```

• Set a session system variable:

```
SET SESSION sql_mode = 'TRADITIONAL';
SET @@SESSION.sql_mode = 'TRADITIONAL';
SET @@sql_mode = 'TRADITIONAL';
```

For complete details about SET syntax, see Section 15.7.6.1, "SET Syntax for Variable Assignment". For a description of the privilege requirements for setting and persisting system variables, see [Section 7.1.9.1, "System Variable Privileges"](#page-42-0)

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
+---------------------------------+-----------------------------------+
| Variable_name | Value |
+---------------------------------+-----------------------------------+
| auto_increment_increment | 1 |
| auto_increment_offset | 1 |
| automatic_sp_privileges | ON |
| back_log | 151 |
| basedir | /home/mysql/ |
| binlog_cache_size | 32768 |
| bulk_insert_buffer_size | 8388608 |
| character_set_client | utf8mb4 |
| character_set_connection | utf8mb4 |
| character_set_database | utf8mb4 |
| character_set_filesystem | binary |
| character_set_results | utf8mb4 |
| character_set_server | utf8mb4 |
| character_set_system | utf8mb3 |
| character_sets_dir | /home/mysql/share/charsets/ |
| check_proxy_users | OFF |
| collation_connection | utf8mb4_0900_ai_ci |
| collation_database | utf8mb4_0900_ai_ci |
| collation_server | utf8mb4_0900_ai_ci |
...
| innodb_autoextend_increment | 8 |
| innodb_buffer_pool_size | 8388608 |
| innodb_commit_concurrency | 0 |
| innodb_concurrency_tickets | 500 |
| innodb_data_file_path | ibdata1:10M:autoextend |
| innodb_data_home_dir | |
...
| version | 8.0.31 |
| version_comment | Source distribution |
| version_compile_machine | x86_64 |
| version_compile_os | Linux |
| version_compile_zlib | 1.2.12 |
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

### <span id="page-42-0"></span>**7.1.9.1 System Variable Privileges**

A system variable can have a global value that affects server operation as a whole, a session value that affects only the current session, or both:

- For dynamic system variables, the SET statement can be used to change their global or session runtime value (or both), to affect operation of the current server instance. (For information about dynamic variables, see [Section 7.1.9.2, "Dynamic System Variables".](#page-43-0))
- For certain global system variables, SET can be used to persist their value to the mysqldauto.cnf file in the data directory, to affect server operation for subsequent startups. (For information about persisting system variables and the mysqld-auto.cnf file, see [Section 7.1.9.3,](#page-61-0) ["Persisted System Variables".](#page-61-0))
- For persisted global system variables, RESET PERSIST can be used to remove their value from mysqld-auto.cnf, to affect server operation for subsequent startups.

This section describes the privileges required for operations that assign values to system variables at runtime. This includes operations that affect runtime values, and operations that persist values.

To set a global system variable, use a SET statement with the appropriate keyword. These privileges apply:

- To set a global system variable runtime value, use the SET GLOBAL statement, which requires the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege).
- To persist a global system variable to the mysqld-auto.cnf file (and set the runtime value), use the SET PERSIST statement, which requires the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege.
- To persist a global system variable to the mysqld-auto.cnf file (without setting the runtime value), use the SET PERSIST\_ONLY statement, which requires the SYSTEM\_VARIABLES\_ADMIN and PERSIST\_RO\_VARIABLES\_ADMIN privileges. SET PERSIST\_ONLY can be used for both dynamic and read-only system variables, but is particularly useful for persisting read-only variables, for which SET PERSIST cannot be used.
- Some global system variables are persist-restricted (see [Section 7.1.9.4, "Nonpersistible and Persist-](#page-65-0)[Restricted System Variables"\)](#page-65-0). To persist these variables, use the SET PERSIST\_ONLY statement, which requires the privileges described previously. In addition, you must connect to the server using an encrypted connection and supply an SSL certificate with the Subject value specified by the persist\_only\_admin\_x509\_subject system variable.

To remove a persisted global system variable from the mysqld-auto.cnf file, use the RESET PERSIST statement. These privileges apply:

• For dynamic system variables, RESET PERSIST requires the SYSTEM\_VARIABLES\_ADMIN or SUPER privilege.

- For read-only system variables, RESET PERSIST requires the SYSTEM\_VARIABLES\_ADMIN and PERSIST\_RO\_VARIABLES\_ADMIN privileges.
- For persist-restricted variables, RESET PERSIST does not require an encrypted connection to the server made using a particular SSL certificate.

If a global system variable has any exceptions to the preceding privilege requirements, the variable description indicates those exceptions. Examples include default\_table\_encryption and mandatory\_roles, which require additional privileges. These additional privileges apply to operations that set the global runtime value, but not operations that persist the value.

To set a session system variable runtime value, use the SET SESSION statement. In contrast to setting global runtime values, setting session runtime values normally requires no special privileges and can be done by any user to affect the current session. For some system variables, setting the session value may have effects outside the current session and thus is a restricted operation that can be done only by users who have a special privilege:

• As of MySQL 8.0.14, the privilege required is SESSION\_VARIABLES\_ADMIN.

![](_page_43_Picture_6.jpeg)

#### **Note**

Any user who has SYSTEM\_VARIABLES\_ADMIN or SUPER effectively has SESSION\_VARIABLES\_ADMIN by implication and need not be granted SESSION\_VARIABLES\_ADMIN explicitly.

• Prior to MySQL 8.0.14, the privilege required is SYSTEM\_VARIABLES\_ADMIN or SUPER.

If a session system variable is restricted, the variable description indicates that restriction. Examples include binlog\_format and sql\_log\_bin. Setting the session value of these variables affects binary logging for the current session, but may also have wider implications for the integrity of server replication and backups.

SESSION\_VARIABLES\_ADMIN enables administrators to minimize the privilege footprint of users who may previously have been granted SYSTEM\_VARIABLES\_ADMIN or SUPER for the purpose of enabling them to modify restricted session system variables. Suppose that an administrator has created the following role to confer the ability to set restricted session system variables:

```
CREATE ROLE set_session_sysvars;
GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO set_session_sysvars;
```

Any user granted the set\_session\_sysvars role (and who has that role active) is able to set restricted session system variables. However, that user is also able to set global system variables, which may be undesirable.

By modifying the role to have SESSION\_VARIABLES\_ADMIN instead of SYSTEM\_VARIABLES\_ADMIN, the role privileges can be reduced to the ability to set restricted session system variables and nothing else. To modify the role, use these statements:

```
GRANT SESSION_VARIABLES_ADMIN ON *.* TO set_session_sysvars;
REVOKE SYSTEM_VARIABLES_ADMIN ON *.* FROM set_session_sysvars;
```

Modifying the role has an immediate effect: Any account granted the set\_session\_sysvars role no longer has SYSTEM\_VARIABLES\_ADMIN and is not able to set global system variables without being granted that ability explicitly. A similar GRANT/REVOKE sequence can be applied to any account that was granted SYSTEM\_VARIABLES\_ADMIN directly rather than by means of a role.

### <span id="page-43-0"></span>**7.1.9.2 Dynamic System Variables**

Many server system variables are dynamic and can be set at runtime. See Section 15.7.6.1, "SET Syntax for Variable Assignment". For a description of the privilege requirements for setting system variables, see [Section 7.1.9.1, "System Variable Privileges"](#page-42-0)

The following table lists all dynamic system variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the variables. Where appropriate, direct links to further information about the items are provided.

Variables that have a type of "string" take a string value. Variables that have a type of "numeric" take a numeric value. Variables that have a type of "boolean" can be set to 0, 1, ON or OFF. Variables that are marked as "enumeration" normally should be set to one of the available values for the variable, but can also be set to the number that corresponds to the desired enumeration value. For enumerated system variables, the first enumeration value corresponds to 0. This differs from the ENUM data type used for table columns, for which the first enumeration value corresponds to 1.

**Table 7.5 Dynamic System Variable Summary**

| Variable Name                                    | Variable Type  | Variable Scope |
|--------------------------------------------------|----------------|----------------|
| activate_all_roles_on_login                      | Boolean        | Global         |
| admin_ssl_ca                                     | File name      | Global         |
| admin_ssl_capath                                 | Directory name | Global         |
| admin_ssl_cert                                   | File name      | Global         |
| admin_ssl_cipher                                 | String         | Global         |
| admin_ssl_crl                                    | File name      | Global         |
| admin_ssl_crlpath                                | Directory name | Global         |
| admin_ssl_key                                    | File name      | Global         |
| admin_tls_ciphersuites                           | String         | Global         |
| admin_tls_version                                | String         | Global         |
| audit_log_connection_policy                      | Enumeration    | Global         |
| audit_log_disable                                | Boolean        | Global         |
| audit_log_exclude_accounts                       | String         | Global         |
| audit_log_flush                                  | Boolean        | Global         |
| audit_log_format_unix_timestamp Boolean          |                | Global         |
| audit_log_include_accounts                       | String         | Global         |
| audit_log_password_history_keep_days Integer     |                | Global         |
| audit_log_prune_seconds                          | Integer        | Global         |
| audit_log_read_buffer_size                       | Integer        | Varies         |
| audit_log_rotate_on_size                         | Integer        | Global         |
| audit_log_statement_policy                       | Enumeration    | Global         |
| authentication_fido_rp_id                        | String         | Global         |
| authentication_kerberos_service_principal String |                | Global         |
| authentication_ldap_sasl_auth_method_name        | String         | Global         |
| authentication_ldap_sasl_bind_base_dn String     |                | Global         |
| authentication_ldap_sasl_bind_root_dn String     |                | Global         |
| authentication_ldap_sasl_bind_root_pwd String    |                | Global         |
| authentication_ldap_sasl_ca_pathString           |                | Global         |
| authentication_ldap_sasl_group_search_attr       | String         | Global         |
| authentication_ldap_sasl_group_search_filter     | String         | Global         |
| authentication_ldap_sasl_init_pool_size Integer  |                | Global         |
| authentication_ldap_sasl_log_statusInteger       |                | Global         |

| Variable Name                                     | Variable Type | Variable Scope |
|---------------------------------------------------|---------------|----------------|
| authentication_ldap_sasl_max_pool_size Integer    |               | Global         |
| authentication_ldap_sasl_referral Boolean         |               | Global         |
| authentication_ldap_sasl_server_host String       |               | Global         |
| authentication_ldap_sasl_server_port Integer      |               | Global         |
| authentication_ldap_sasl_tls                      | Boolean       | Global         |
| authentication_ldap_sasl_user_search_attr String  |               | Global         |
| authentication_ldap_simple_auth_method_name       | String        | Global         |
| authentication_ldap_simple_bind_base_dn String    |               | Global         |
| authentication_ldap_simple_bind_root_dn String    |               | Global         |
| authentication_ldap_simple_bind_root_pwd String   |               | Global         |
| authentication_ldap_simple_ca_pathString          |               | Global         |
| authentication_ldap_simple_group_search_attr      | String        | Global         |
| authentication_ldap_simple_group_search_filter    | String        | Global         |
| authentication_ldap_simple_init_pool_size Integer |               | Global         |
| authentication_ldap_simple_log_status Integer     |               | Global         |
| authentication_ldap_simple_max_pool_size Integer  |               | Global         |
| authentication_ldap_simple_referralBoolean        |               | Global         |
| authentication_ldap_simple_server_host String     |               | Global         |
| authentication_ldap_simple_server_port Integer    |               | Global         |
| authentication_ldap_simple_tls                    | Boolean       | Global         |
| authentication_ldap_simple_user_search_attr       | String        | Global         |
| authentication_policy                             | String        | Global         |
| auto_increment_increment                          | Integer       | Both           |
| auto_increment_offset                             | Integer       | Both           |
| autocommit                                        | Boolean       | Both           |
| automatic_sp_privileges                           | Boolean       | Global         |
| avoid_temporal_upgrade                            | Boolean       | Global         |
| big_tables                                        | Boolean       | Both           |
| binlog_cache_size                                 | Integer       | Global         |
| binlog_checksum                                   | String        | Global         |
| binlog_direct_non_transactional_updates Boolan    |               | Both           |
| binlog_encryption                                 | Boolean       | Global         |
| binlog_error_action                               | Enumeration   | Global         |
| binlog_expire_logs_auto_purge                     | Boolean       | Global         |
| binlog_expire_logs_seconds                        | Integer       | Global         |
| binlog_format                                     | Enumeration   | Both           |
| binlog_group_commit_sync_delay Integer            |               | Global         |
| binlog_group_commit_sync_no_delay_count           | Integer       | Global         |
| binlog_max_flush_queue_time                       | Integer       | Global         |
| binlog_order_commits                              | Boolean       | Global         |
| binlog_row_image                                  | Enumeration   | Both           |

| Variable Name                                      | Variable Type | Variable Scope |
|----------------------------------------------------|---------------|----------------|
| binlog_row_metadata                                | Enumeration   | Global         |
| binlog_row_value_options                           | Set           | Both           |
| binlog_rows_query_log_events                       | Boolean       | Both           |
| binlog_stmt_cache_size                             | Integer       | Global         |
| binlog_transaction_compression                     | Boolean       | Both           |
| binlog_transaction_compression_level_zstd Integer  |               | Both           |
| binlog_transaction_dependency_history_size         | Integer       | Global         |
| binlog_transaction_dependency_tracking Enumeration |               | Global         |
| block_encryption_mode                              | String        | Both           |
| bulk_insert_buffer_size                            | Integer       | Both           |
| caching_sha2_password_digest_rounds Integer        |               | Global         |
| character_set_client                               | String        | Both           |
| character_set_connection                           | String        | Both           |
| character_set_database                             | String        | Both           |
| character_set_filesystem                           | String        | Both           |
| character_set_results                              | String        | Both           |
| character_set_server                               | String        | Both           |
| check_proxy_users                                  | Boolean       | Global         |
| clone_autotune_concurrency                         | Boolean       | Global         |
| clone_block_ddl                                    | Boolean       | Global         |
| clone_buffer_size                                  | Integer       | Global         |
| clone_ddl_timeout                                  | Integer       | Global         |
| clone_delay_after_data_drop                        | Integer       | Global         |
| clone_donor_timeout_after_network_failure Integer  |               | Global         |
| clone_enable_compression                           | Boolean       | Global         |
| clone_max_concurrency                              | Integer       | Global         |
| clone_max_data_bandwidth                           | Integer       | Global         |
| clone_max_network_bandwidth                        | Integer       | Global         |
| clone_ssl_ca                                       | File name     | Global         |
| clone_ssl_cert                                     | File name     | Global         |
| clone_ssl_key                                      | File name     | Global         |
| clone_valid_donor_list                             | String        | Global         |
| collation_connection                               | String        | Both           |
| collation_database                                 | String        | Both           |
| collation_server                                   | String        | Both           |
| completion_type                                    | Enumeration   | Both           |
| component_scheduler.enabled                        | Boolean       | Global         |
| concurrent_insert                                  | Enumeration   | Global         |
| connect_timeout                                    | Integer       | Global         |
| connection_control_failed_connections_threshold    | Integer       | Global         |
| connection_control_max_connection_delay Integer    |               | Global         |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| connection_control_min_connection_delay Integer  |               | Global         |
| connection_memory_chunk_size                     | Integer       | Both           |
| connection_memory_limit                          | Integer       | Both           |
| cte_max_recursion_depth                          | Integer       | Both           |
| debug                                            | String        | Both           |
| debug_sync                                       | String        | Session        |
| default_collation_for_utf8mb4                    | Enumeration   | Both           |
| default_password_lifetime                        | Integer       | Global         |
| default_storage_engine                           | Enumeration   | Both           |
| default_table_encryption                         | Boolean       | Both           |
| default_tmp_storage_engine                       | Enumeration   | Both           |
| default_week_format                              | Integer       | Both           |
| delay_key_write                                  | Enumeration   | Global         |
| delayed_insert_limit                             | Integer       | Global         |
| delayed_insert_timeout                           | Integer       | Global         |
| delayed_queue_size                               | Integer       | Global         |
| div_precision_increment                          | Integer       | Both           |
| dragnet.log_error_filter_rules                   | String        | Global         |
| end_markers_in_json                              | Boolean       | Both           |
| enforce_gtid_consistency                         | Enumeration   | Global         |
| enterprise_encryption.maximum_rsa_key_size       | Integer       | Global         |
| enterprise_encryption.rsa_support_legacy_padding | Boolean       | Global         |
| eq_range_index_dive_limit                        | Integer       | Both           |
| event_scheduler                                  | Enumeration   | Global         |
| expire_logs_days                                 | Integer       | Global         |
| explain_format                                   | Enumeration   | Both           |
| explicit_defaults_for_timestamp                  | Boolean       | Both           |
| flush                                            | Boolean       | Global         |
| flush_time                                       | Integer       | Global         |
| foreign_key_checks                               | Boolean       | Both           |
| ft_boolean_syntax                                | String        | Global         |
| general_log                                      | Boolean       | Global         |
| general_log_file                                 | File name     | Global         |
| generated_random_password_length Integer         |               | Both           |
| global_connection_memory_limit                   | Integer       | Global         |
| global_connection_memory_trackingBoolean         |               | Both           |
| group_concat_max_len                             | Integer       | Both           |
| group_replication_advertise_recovery_endpoints   | String        | Global         |
| group_replication_allow_local_lower_version_join | Boolean       | Global         |
| group_replication_auto_increment_increment       | Integer       | Global         |
| group_replication_autorejoin_tries Integer       |               | Global         |

| Variable Name                                       | Variable Type | Variable Scope |
|-----------------------------------------------------|---------------|----------------|
| group_replication_bootstrap_groupBoolean            |               | Global         |
| group_replication_clone_thresholdInteger            |               | Global         |
| group_replication_communication_debug_options       | String        | Global         |
| group_replication_communication_max_message_size    | Integer       | Global         |
| group_replication_communication_stack String        |               | Global         |
| group_replication_components_stop_timeout           | Integer       | Global         |
| group_replication_compression_threshold Integer     |               | Global         |
| group_replication_consistency                       | Enumeration   | Both           |
| group_replication_enforce_update_everywhere_checks  | Boolean       | Global         |
| group_replication_exit_state_actionEnumeration      |               | Global         |
| group_replication_flow_control_applier_threshold    | Integer       | Global         |
| group_replication_flow_control_certifier_threshold  | Integer       | Global         |
| group_replication_flow_control_hold_percent         | Integer       | Global         |
| group_replication_flow_control_max_quota Integer    |               | Global         |
| group_replication_flow_control_member_quota_percent | Integer       | Global         |
| group_replication_flow_control_min_quota Integer    |               | Global         |
| group_replication_flow_control_min_recovery_quota   | Integer       | Global         |
| group_replication_flow_control_mode Enumeration     |               | Global         |
| group_replication_flow_control_period Integer       |               | Global         |
| group_replication_flow_control_release_percent      | Integer       | Global         |
| group_replication_force_membersString               |               | Global         |
| group_replication_group_name                        | String        | Global         |
| group_replication_group_seeds                       | String        | Global         |
| group_replication_gtid_assignment_block_size        | Integer       | Global         |
| group_replication_ip_allowlist                      | String        | Global         |
| group_replication_ip_whitelist                      | String        | Global         |
| group_replication_local_address                     | String        | Global         |
| group_replication_member_expel_timeout Integer      |               | Global         |
| group_replication_member_weightInteger              |               | Global         |
| group_replication_message_cache_size Integer        |               | Global         |
| group_replication_paxos_single_leader Boolean       |               | Global         |
| group_replication_poll_spin_loopsInteger            |               | Global         |
| group_replication_recovery_complete_at Enumeration  |               | Global         |
| group_replication_recovery_compression_algorithms   | Set           | Global         |
| group_replication_recovery_get_public_key Boolean   |               | Global         |
| group_replication_recovery_public_key_path          | File name     | Global         |
| group_replication_recovery_reconnect_interval       | Integer       | Global         |
| group_replication_recovery_retry_count Integer      |               | Global         |
| group_replication_recovery_ssl_caString             |               | Global         |
| group_replication_recovery_ssl_capath String        |               | Global         |
| group_replication_recovery_ssl_cert String          |               | Global         |

| Variable Name                                         | Variable Type | Variable Scope |
|-------------------------------------------------------|---------------|----------------|
| group_replication_recovery_ssl_cipher String          |               | Global         |
| group_replication_recovery_ssl_crlFile name           |               | Global         |
| group_replication_recovery_ssl_crlpath Directory name |               | Global         |
| group_replication_recovery_ssl_keyString              |               | Global         |
| group_replication_recovery_ssl_verify_server_cert     | Boolean       | Global         |
| group_replication_recovery_tls_ciphersuites           | String        | Global         |
| group_replication_recovery_tls_version String         |               | Global         |
| group_replication_recovery_use_ssl Boolean            |               | Global         |
| group_replication_recovery_zstd_compression_level     | Integer       | Global         |
| group_replication_single_primary_mode Boolan          |               | Global         |
| group_replication_ssl_mode                            | Enumeration   | Global         |
| group_replication_start_on_boot                       | Boolean       | Global         |
| group_replication_tls_source                          | Enumeration   | Global         |
| group_replication_transaction_size_limit Integer      |               | Global         |
| group_replication_unreachable_majority_timeout        | Integer       | Global         |
| group_replication_view_change_uuidString              |               | Global         |
| gtid_executed_compression_periodInteger               |               | Global         |
| gtid_mode                                             | Enumeration   | Global         |
| gtid_next                                             | Enumeration   | Session        |
| gtid_purged                                           | String        | Global         |
| histogram_generation_max_mem_size Integer             |               | Both           |
| host_cache_size                                       | Integer       | Global         |
| identity                                              | Integer       | Session        |
| immediate_server_version                              | Integer       | Session        |
| information_schema_stats_expiry Integer               |               | Both           |
| init_connect                                          | String        | Global         |
| init_replica                                          | String        | Global         |
| init_slave                                            | String        | Global         |
| innodb_adaptive_flushing                              | Boolean       | Global         |
| innodb_adaptive_flushing_lwm                          | Integer       | Global         |
| innodb_adaptive_hash_index                            | Boolean       | Global         |
| innodb_adaptive_max_sleep_delayInteger                |               | Global         |
| innodb_api_bk_commit_interval                         | Integer       | Global         |
| innodb_api_trx_level                                  | Integer       | Global         |
| innodb_autoextend_increment                           | Integer       | Global         |
| innodb_background_drop_list_emptyBoolean              |               | Global         |
| innodb_buffer_pool_dump_at_shutdown Boolean           |               | Global         |
| innodb_buffer_pool_dump_now                           | Boolean       | Global         |
| innodb_buffer_pool_dump_pct                           | Integer       | Global         |
| innodb_buffer_pool_filename                           | File name     | Global         |
| innodb_buffer_pool_in_core_file                       | Boolean       | Global         |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| innodb_buffer_pool_load_abort                    | Boolean       | Global         |
| innodb_buffer_pool_load_now                      | Boolean       | Global         |
| innodb_buffer_pool_size                          | Integer       | Global         |
| innodb_change_buffer_max_size Integer            |               | Global         |
| innodb_change_buffering                          | Enumeration   | Global         |
| innodb_change_buffering_debug                    | Integer       | Global         |
| innodb_checkpoint_disabled                       | Boolean       | Global         |
| innodb_checksum_algorithm                        | Enumeration   | Global         |
| innodb_cmp_per_index_enabled                     | Boolean       | Global         |
| innodb_commit_concurrency                        | Integer       | Global         |
| innodb_compress_debug                            | Enumeration   | Global         |
| innodb_compression_failure_threshold_pct Integer |               | Global         |
| innodb_compression_level                         | Integer       | Global         |
| innodb_compression_pad_pct_maxInteger            |               | Global         |
| innodb_concurrency_tickets                       | Integer       | Global         |
| innodb_ddl_buffer_size                           | Integer       | Session        |
| innodb_ddl_log_crash_reset_debugBoolean          |               | Global         |
| innodb_ddl_threads                               | Integer       | Session        |
| innodb_deadlock_detect                           | Boolean       | Global         |
| innodb_default_row_format                        | Enumeration   | Global         |
| innodb_disable_sort_file_cache                   | Boolean       | Global         |
| innodb_doublewrite                               | Enumeration   | Global         |
| innodb_extend_and_initialize                     | Boolean       | Global         |
| innodb_fast_shutdown                             | Integer       | Global         |
| innodb_fil_make_page_dirty_debugInteger          |               | Global         |
| innodb_file_per_table                            | Boolean       | Global         |
| innodb_fill_factor                               | Integer       | Global         |
| innodb_flush_log_at_timeout                      | Integer       | Global         |
| innodb_flush_log_at_trx_commit                   | Enumeration   | Global         |
| innodb_flush_neighbors                           | Enumeration   | Global         |
| innodb_flush_sync                                | Boolean       | Global         |
| innodb_flushing_avg_loops                        | Integer       | Global         |
| innodb_fsync_threshold                           | Integer       | Global         |
| innodb_ft_aux_table                              | String        | Global         |
| innodb_ft_enable_diag_print                      | Boolean       | Global         |
| innodb_ft_enable_stopword                        | Boolean       | Both           |
| innodb_ft_num_word_optimize                      | Integer       | Global         |
| innodb_ft_result_cache_limit                     | Integer       | Global         |
| innodb_ft_server_stopword_table String           |               | Global         |
| innodb_ft_user_stopword_table                    | String        | Both           |
| innodb_idle_flush_pct                            | Integer       | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| innodb_io_capacity                           | Integer       | Global         |
| innodb_io_capacity_max                       | Integer       | Global         |
| innodb_limit_optimistic_insert_debugInteger  |               | Global         |
| innodb_lock_wait_timeout                     | Integer       | Both           |
| innodb_log_buffer_size                       | Integer       | Global         |
| innodb_log_checkpoint_fuzzy_nowBoolean       |               | Global         |
| innodb_log_checkpoint_now                    | Boolean       | Global         |
| innodb_log_checksums                         | Boolean       | Global         |
| innodb_log_compressed_pages                  | Boolean       | Global         |
| innodb_log_spin_cpu_abs_lwm                  | Integer       | Global         |
| innodb_log_spin_cpu_pct_hwm                  | Integer       | Global         |
| innodb_log_wait_for_flush_spin_hwmInteger    |               | Global         |
| innodb_log_write_ahead_size                  | Integer       | Global         |
| innodb_log_writer_threads                    | Boolean       | Global         |
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
| innodb_open_files                            | Integer       | Global         |
| innodb_optimize_fulltext_only                | Boolean       | Global         |
| innodb_parallel_read_threads                 | Integer       | Session        |
| innodb_print_all_deadlocks                   | Boolean       | Global         |
| innodb_print_ddl_logs                        | Boolean       | Global         |
| innodb_purge_batch_size                      | Integer       | Global         |
| innodb_purge_rseg_truncate_frequency Integer |               | Global         |
| innodb_random_read_ahead                     | Boolean       | Global         |
| innodb_read_ahead_threshold                  | Integer       | Global         |
| innodb_redo_log_archive_dirs                 | String        | Global         |
| innodb_redo_log_capacity                     | Integer       | Global         |
| innodb_redo_log_encrypt                      | Boolean       | Global         |
| innodb_replication_delay                     | Integer       | Global         |

| Variable Name                                | Variable Type  | Variable Scope |
|----------------------------------------------|----------------|----------------|
| innodb_rollback_segments                     | Integer        | Global         |
| innodb_saved_page_number_debugInteger        |                | Global         |
| innodb_segment_reserve_factor                | Numeric        | Global         |
| innodb_spin_wait_delay                       | Integer        | Global         |
| innodb_spin_wait_pause_multiplierInteger     |                | Global         |
| innodb_stats_auto_recalc                     | Boolean        | Global         |
| innodb_stats_include_delete_marked Boolean   |                | Global         |
| innodb_stats_method                          | Enumeration    | Global         |
| innodb_stats_on_metadata                     | Boolean        | Global         |
| innodb_stats_persistent                      | Boolean        | Global         |
| innodb_stats_persistent_sample_pages Integer |                | Global         |
| innodb_stats_transient_sample_pages Integer  |                | Global         |
| innodb_status_output                         | Boolean        | Global         |
| innodb_status_output_locks                   | Boolean        | Global         |
| innodb_strict_mode                           | Boolean        | Both           |
| innodb_sync_spin_loops                       | Integer        | Global         |
| innodb_table_locks                           | Boolean        | Both           |
| innodb_thread_concurrency                    | Integer        | Global         |
| innodb_thread_sleep_delay                    | Integer        | Global         |
| innodb_tmpdir                                | Directory name | Both           |
| innodb_trx_purge_view_update_only_debug      | Boolean        | Global         |
| innodb_trx_rseg_n_slots_debug                | Integer        | Global         |
| innodb_undo_log_encrypt                      | Boolean        | Global         |
| innodb_undo_log_truncate                     | Boolean        | Global         |
| innodb_undo_tablespaces                      | Integer        | Global         |
| innodb_use_fdatasync                         | Boolean        | Global         |
| insert_id                                    | Integer        | Session        |
| interactive_timeout                          | Integer        | Both           |
| internal_tmp_mem_storage_engineEnumeration   |                | Both           |
| join_buffer_size                             | Integer        | Both           |
| keep_files_on_create                         | Boolean        | Both           |
| key_buffer_size                              | Integer        | Global         |
| key_cache_age_threshold                      | Integer        | Global         |
| key_cache_block_size                         | Integer        | Global         |
| key_cache_division_limit                     | Integer        | Global         |
| keyring_aws_cmk_id                           | String         | Global         |
| keyring_aws_region                           | Enumeration    | Global         |
| keyring_encrypted_file_data                  | File name      | Global         |
| keyring_encrypted_file_password String       |                | Global         |
| keyring_file_data                            | File name      | Global         |
| keyring_hashicorp_auth_path                  | String         | Global         |

| Variable Name                                  | Variable Type  | Variable Scope |
|------------------------------------------------|----------------|----------------|
| keyring_hashicorp_ca_path                      | File name      | Global         |
| keyring_hashicorp_caching                      | Boolean        | Global         |
| keyring_hashicorp_role_id                      | String         | Global         |
| keyring_hashicorp_secret_id                    | String         | Global         |
| keyring_hashicorp_server_url                   | String         | Global         |
| keyring_hashicorp_store_path                   | String         | Global         |
| keyring_okv_conf_dir                           | Directory name | Global         |
| keyring_operations                             | Boolean        | Global         |
| last_insert_id                                 | Integer        | Session        |
| lc_messages                                    | String         | Both           |
| lc_time_names                                  | String         | Both           |
| local_infile                                   | Boolean        | Global         |
| lock_wait_timeout                              | Integer        | Both           |
| log_bin_trust_function_creators                | Boolean        | Global         |
| log_bin_use_v1_row_events                      | Boolean        | Global         |
| log_error_services                             | String         | Global         |
| log_error_suppression_list                     | String         | Global         |
| log_error_verbosity                            | Integer        | Global         |
| log_output                                     | Set            | Global         |
| log_queries_not_using_indexes                  | Boolean        | Global         |
| log_raw                                        | Boolean        | Global         |
| log_slow_admin_statements                      | Boolean        | Global         |
| log_slow_extra                                 | Boolean        | Global         |
| log_slow_replica_statements                    | Boolean        | Global         |
| log_slow_slave_statements                      | Boolean        | Global         |
| log_statements_unsafe_for_binlogBoolean        |                | Global         |
| log_throttle_queries_not_using_indexes Integer |                | Global         |
| log_timestamps                                 | Enumeration    | Global         |
| long_query_time                                | Numeric        | Both           |
| low_priority_updates                           | Boolean        | Both           |
| mandatory_roles                                | String         | Global         |
| master_info_repository                         | String         | Global         |
| master_verify_checksum                         | Boolean        | Global         |
| max_allowed_packet                             | Integer        | Both           |
| max_binlog_cache_size                          | Integer        | Global         |
| max_binlog_size                                | Integer        | Global         |
| max_binlog_stmt_cache_size                     | Integer        | Global         |
| max_connect_errors                             | Integer        | Global         |
| max_connections                                | Integer        | Global         |
| max_delayed_threads                            | Integer        | Both           |
| max_error_count                                | Integer        | Both           |

| Variable Name                                    | Variable Type | Variable Scope |
|--------------------------------------------------|---------------|----------------|
| max_execution_time                               | Integer       | Both           |
| max_heap_table_size                              | Integer       | Both           |
| max_insert_delayed_threads                       | Integer       | Both           |
| max_join_size                                    | Integer       | Both           |
| max_length_for_sort_data                         | Integer       | Both           |
| max_points_in_geometry                           | Integer       | Both           |
| max_prepared_stmt_count                          | Integer       | Global         |
| max_relay_log_size                               | Integer       | Global         |
| max_seeks_for_key                                | Integer       | Both           |
| max_sort_length                                  | Integer       | Both           |
| max_sp_recursion_depth                           | Integer       | Both           |
| max_user_connections                             | Integer       | Both           |
| max_write_lock_count                             | Integer       | Global         |
| min_examined_row_limit                           | Integer       | Both           |
| myisam_data_pointer_size                         | Integer       | Global         |
| myisam_max_sort_file_size                        | Integer       | Global         |
| myisam_sort_buffer_size                          | Integer       | Both           |
| myisam_stats_method                              | Enumeration   | Both           |
| myisam_use_mmap                                  | Boolean       | Global         |
| mysql_firewall_mode                              | Boolean       | Global         |
| mysql_firewall_trace                             | Boolean       | Global         |
| mysql_native_password_proxy_users Boolean        |               | Global         |
| mysqlx_compression_algorithms                    | Set           | Global         |
| mysqlx_connect_timeout                           | Integer       | Global         |
| mysqlx_deflate_default_compression_level Integer |               | Global         |
| mysqlx_deflate_max_client_compression_level      | Integer       | Global         |
| mysqlx_document_id_unique_prefixInteger          |               | Global         |
| mysqlx_enable_hello_notice                       | Boolean       | Global         |
| mysqlx_idle_worker_thread_timeoutInteger         |               | Global         |
| mysqlx_interactive_timeout                       | Integer       | Global         |
| mysqlx_lz4_default_compression_level Integer     |               | Global         |
| mysqlx_lz4_max_client_compression_level Integer  |               | Global         |
| mysqlx_max_allowed_packet                        | Integer       | Global         |
| mysqlx_max_connections                           | Integer       | Global         |
| mysqlx_min_worker_threads                        | Integer       | Global         |
| mysqlx_read_timeout                              | Integer       | Session        |
| mysqlx_wait_timeout                              | Integer       | Session        |
| mysqlx_write_timeout                             | Integer       | Session        |
| mysqlx_zstd_default_compression_level Integer    |               | Global         |
| mysqlx_zstd_max_client_compression_level         | Integer       | Global         |
| ndb_allow_copying_alter_table                    | Boolean       | Both           |

| Variable Name                              | Variable Type | Variable Scope |
|--------------------------------------------|---------------|----------------|
| ndb_autoincrement_prefetch_sz              | Integer       | Both           |
| ndb_batch_size                             | Integer       | Both           |
| ndb_blob_read_batch_bytes                  | Integer       | Both           |
| ndb_blob_write_batch_bytes                 | Integer       | Both           |
| ndb_clear_apply_status                     | Boolean       | Global         |
| ndb_conflict_role                          | Enumeration   | Global         |
| ndb_data_node_neighbour                    | Integer       | Global         |
| ndb_dbg_check_shares                       | Integer       | Both           |
| ndb_default_column_format                  | Enumeration   | Global         |
| ndb_default_column_format                  | Enumeration   | Global         |
| ndb_deferred_constraints                   | Integer       | Both           |
| ndb_deferred_constraints                   | Integer       | Both           |
| ndb_distribution                           | Enumeration   | Global         |
| ndb_distribution                           | Enumeration   | Global         |
| ndb_eventbuffer_free_percent               | Integer       | Global         |
| ndb_eventbuffer_max_alloc                  | Integer       | Global         |
| ndb_extra_logging                          | Integer       | Global         |
| ndb_force_send                             | Boolean       | Both           |
| ndb_fully_replicated                       | Boolean       | Both           |
| ndb_index_stat_enable                      | Boolean       | Both           |
| ndb_index_stat_option                      | String        | Both           |
| ndb_join_pushdown                          | Boolean       | Both           |
| ndb_log_binlog_index                       | Boolean       | Global         |
| ndb_log_cache_size                         | Integer       | Global         |
| ndb_log_empty_epochs                       | Boolean       | Global         |
| ndb_log_empty_epochs                       | Boolean       | Global         |
| ndb_log_empty_update                       | Boolean       | Global         |
| ndb_log_empty_update                       | Boolean       | Global         |
| ndb_log_exclusive_reads                    | Boolean       | Both           |
| ndb_log_exclusive_reads                    | Boolean       | Both           |
| ndb_log_transaction_compressionBoolean     |               | Global         |
| ndb_log_transaction_compression_level_zstd | Integer       | Global         |
| ndb_log_update_as_write                    | Boolean       | Global         |
| ndb_log_update_minimal                     | Boolean       | Global         |
| ndb_log_updated_only                       | Boolean       | Global         |
| ndb_metadata_check                         | Boolean       | Global         |
| ndb_metadata_check_interval                | Integer       | Global         |
| ndb_metadata_sync                          | Boolean       | Global         |
| ndb_optimization_delay                     | Integer       | Global         |
| ndb_optimized_node_selection               | Integer       | Global         |
| ndb_read_backup                            | Boolean       | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| ndb_recv_thread_activation_threshold Integer |               | Global         |
| ndb_recv_thread_cpu_mask                     | Bitmap        | Global         |
| ndb_replica_batch_size                       | Integer       | Global         |
| ndb_replica_blob_write_batch_bytesInteger    |               | Global         |
| ndb_report_thresh_binlog_epoch_slip Integer  |               | Global         |
| ndb_report_thresh_binlog_mem_usage Integer   |               | Global         |
| ndb_row_checksum                             | Integer       | Both           |
| ndb_schema_dist_lock_wait_timeout Ineger     |               | Global         |
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
| optimizer_prune_level                        | Integer       | Both           |
| optimizer_search_depth                       | Integer       | Both           |
| optimizer_switch                             | Set           | Both           |
| optimizer_trace                              | String        | Both           |
| optimizer_trace_features                     | String        | Both           |
| optimizer_trace_limit                        | Integer       | Both           |
| optimizer_trace_max_mem_size                 | Integer       | Both           |
| optimizer_trace_offset                       | Integer       | Both           |
| original_commit_timestamp                    | Numeric       | Session        |
| original_server_version                      | Integer       | Session        |
| parser_max_mem_size                          | Integer       | Both           |
| partial_revokes                              | Boolean       | Global         |
| password_history                             | Integer       | Global         |
| password_require_current                     | Boolean       | Global         |
| password_reuse_interval                      | Integer       | Global         |
| performance_schema_max_digest_sample_age     | Integer       | Global         |

| Variable Name                                  | Variable Type | Variable Scope |
|------------------------------------------------|---------------|----------------|
| performance_schema_show_processlist Boolean    |               | Global         |
| preload_buffer_size                            | Integer       | Both           |
| print_identified_with_as_hex                   | Boolean       | Both           |
| profiling                                      | Boolean       | Both           |
| profiling_history_size                         | Integer       | Both           |
| protocol_compression_algorithms Set            |               | Global         |
| pseudo_replica_mode                            | Boolean       | Session        |
| pseudo_slave_mode                              | Boolean       | Session        |
| pseudo_thread_id                               | Integer       | Session        |
| query_alloc_block_size                         | Integer       | Both           |
| query_prealloc_size                            | Integer       | Both           |
| rand_seed1                                     | Integer       | Session        |
| rand_seed2                                     | Integer       | Session        |
| range_alloc_block_size                         | Integer       | Both           |
| range_optimizer_max_mem_size Integer           |               | Both           |
| rbr_exec_mode                                  | Enumeration   | Session        |
| read_buffer_size                               | Integer       | Both           |
| read_only                                      | Boolean       | Global         |
| read_rnd_buffer_size                           | Integer       | Both           |
| regexp_stack_limit                             | Integer       | Global         |
| regexp_time_limit                              | Integer       | Global         |
| relay_log_info_repository                      | String        | Global         |
| relay_log_purge                                | Boolean       | Global         |
| replica_allow_batching                         | Boolean       | Global         |
| replica_checkpoint_group                       | Integer       | Global         |
| replica_checkpoint_period                      | Integer       | Global         |
| replica_compressed_protocol                    | Boolean       | Global         |
| replica_exec_mode                              | Enumeration   | Global         |
| replica_max_allowed_packet                     | Integer       | Global         |
| replica_net_timeout                            | Integer       | Global         |
| replica_parallel_type                          | Enumeration   | Global         |
| replica_parallel_workers                       | Integer       | Global         |
| replica_pending_jobs_size_max                  | Integer       | Global         |
| replica_preserve_commit_order                  | Boolean       | Global         |
| replica_sql_verify_checksum                    | Boolean       | Global         |
| replica_transaction_retries                    | Integer       | Global         |
| replica_type_conversions                       | Set           | Global         |
| replication_optimize_for_static_plugin_config  | Boolean       | Global         |
| replication_sender_observe_commit_only Boolean |               | Global         |
| require_row_format                             | Boolean       | Session        |
| require_secure_transport                       | Boolean       | Global         |

| Variable Name                                         | Variable Type | Variable Scope |
|-------------------------------------------------------|---------------|----------------|
| resultset_metadata                                    | Enumeration   | Session        |
| rewriter_enabled                                      | Boolean       | Global         |
| rewriter_enabled_for_threads_without_privilege_checks | Boolean       | Global         |
| rewriter_verbose                                      | Integer       | Global         |
| rpl_read_size                                         | Integer       | Global         |
| rpl_semi_sync_master_enabled                          | Boolean       | Global         |
| rpl_semi_sync_master_timeout                          | Integer       | Global         |
| rpl_semi_sync_master_trace_levelInteger               |               | Global         |
| rpl_semi_sync_master_wait_for_slave_count             | Integer       | Global         |
| rpl_semi_sync_master_wait_no_slave Boolean            |               | Global         |
| rpl_semi_sync_master_wait_point Enumeration           |               | Global         |
| rpl_semi_sync_replica_enabled                         | Boolean       | Global         |
| rpl_semi_sync_replica_trace_levelInteger              |               | Global         |
| rpl_semi_sync_slave_enabled                           | Boolean       | Global         |
| rpl_semi_sync_slave_trace_level Integer               |               | Global         |
| rpl_semi_sync_source_enabled                          | Boolean       | Global         |
| rpl_semi_sync_source_timeout                          | Integer       | Global         |
| rpl_semi_sync_source_trace_levelInteger               |               | Global         |
| rpl_semi_sync_source_wait_for_replica_count           | Integer       | Global         |
| rpl_semi_sync_source_wait_no_replica Boolean          |               | Global         |
| rpl_semi_sync_source_wait_point Enumeration           |               | Global         |
| rpl_stop_replica_timeout                              | Integer       | Global         |
| rpl_stop_slave_timeout                                | Integer       | Global         |
| schema_definition_cache                               | Integer       | Global         |
| secondary_engine_cost_thresholdNumeric                |               | Session        |
| select_into_buffer_size                               | Integer       | Both           |
| select_into_disk_sync                                 | Boolean       | Both           |
| select_into_disk_sync_delay                           | Integer       | Both           |
| server_id                                             | Integer       | Global         |
| session_track_gtids                                   | Enumeration   | Both           |
| session_track_schema                                  | Boolean       | Both           |
| session_track_state_change                            | Boolean       | Both           |
| session_track_system_variables                        | String        | Both           |
| session_track_transaction_info                        | Enumeration   | Both           |
| sha256_password_proxy_users                           | Boolean       | Global         |
| show_create_table_skip_secondary_engine Boolean       |               | Session        |
| show_create_table_verbosity                           | Boolean       | Both           |
| show_gipk_in_create_table_and_information_schema      | Boolean       | Both           |
| show_old_temporals                                    | Boolean       | Both           |
| slave_allow_batching                                  | Boolean       | Global         |
| slave_checkpoint_group                                | Integer       | Global         |

| Variable Name                             | Variable Type  | Variable Scope |
|-------------------------------------------|----------------|----------------|
| slave_checkpoint_period                   | Integer        | Global         |
| slave_compressed_protocol                 | Boolean        | Global         |
| slave_exec_mode                           | Enumeration    | Global         |
| slave_max_allowed_packet                  | Integer        | Global         |
| slave_net_timeout                         | Integer        | Global         |
| slave_parallel_type                       | Enumeration    | Global         |
| slave_parallel_workers                    | Integer        | Global         |
| slave_pending_jobs_size_max               | Integer        | Global         |
| slave_preserve_commit_order               | Boolean        | Global         |
| slave_rows_search_algorithms              | Set            | Global         |
| slave_sql_verify_checksum                 | Boolean        | Global         |
| slave_transaction_retries                 | Integer        | Global         |
| slave_type_conversions                    | Set            | Global         |
| slow_launch_time                          | Integer        | Global         |
| slow_query_log                            | Boolean        | Global         |
| slow_query_log_file                       | File name      | Global         |
| sort_buffer_size                          | Integer        | Both           |
| source_verify_checksum                    | Boolean        | Global         |
| sql_auto_is_null                          | Boolean        | Both           |
| sql_big_selects                           | Boolean        | Both           |
| sql_buffer_result                         | Boolean        | Both           |
| sql_generate_invisible_primary_keyBoolean |                | Both           |
| sql_log_bin                               | Boolean        | Session        |
| sql_log_off                               | Boolean        | Both           |
| sql_mode                                  | Set            | Both           |
| sql_notes                                 | Boolean        | Both           |
| sql_quote_show_create                     | Boolean        | Both           |
| sql_replica_skip_counter                  | Integer        | Global         |
| sql_require_primary_key                   | Boolean        | Both           |
| sql_safe_updates                          | Boolean        | Both           |
| sql_select_limit                          | Integer        | Both           |
| sql_slave_skip_counter                    | Integer        | Global         |
| sql_warnings                              | Boolean        | Both           |
| ssl_ca                                    | File name      | Global         |
| ssl_capath                                | Directory name | Global         |
| ssl_cert                                  | File name      | Global         |
| ssl_cipher                                | String         | Global         |
| ssl_crl                                   | File name      | Global         |
| ssl_crlpath                               | Directory name | Global         |
| ssl_key                                   | File name      | Global         |
| ssl_session_cache_mode                    | Boolean        | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| ssl_session_cache_timeout                    | Integer       | Global         |
| stored_program_cache                         | Integer       | Global         |
| stored_program_definition_cache Integer      |               | Global         |
| super_read_only                              | Boolean       | Global         |
| sync_binlog                                  | Integer       | Global         |
| sync_master_info                             | Integer       | Global         |
| sync_relay_log                               | Integer       | Global         |
| sync_relay_log_info                          | Integer       | Global         |
| sync_source_info                             | Integer       | Global         |
| syseventlog.facility                         | String        | Global         |
| syseventlog.include_pid                      | Boolean       | Global         |
| syseventlog.tag                              | String        | Global         |
| table_definition_cache                       | Integer       | Global         |
| table_encryption_privilege_check Boolean     |               | Global         |
| table_open_cache                             | Integer       | Global         |
| tablespace_definition_cache                  | Integer       | Global         |
| temptable_max_mmap                           | Integer       | Global         |
| temptable_max_ram                            | Integer       | Global         |
| temptable_use_mmap                           | Boolean       | Global         |
| terminology_use_previous                     | Enumeration   | Both           |
| thread_cache_size                            | Integer       | Global         |
| thread_pool_high_priority_connection Integer |               | Both           |
| thread_pool_max_active_query_threads Integer |               | Global         |
| thread_pool_max_transactions_limitInteger    |               | Global         |
| thread_pool_max_unused_threadsInteger        |               | Global         |
| thread_pool_prio_kickup_timer                | Integer       | Global         |
| thread_pool_query_threads_per_group Integer  |               | Global         |
| thread_pool_stall_limit                      | Integer       | Global         |
| thread_pool_transaction_delay                | Integer       | Global         |
| time_zone                                    | String        | Both           |
| timestamp                                    | Numeric       | Session        |
| tls_ciphersuites                             | String        | Global         |
| tls_version                                  | String        | Global         |
| tmp_table_size                               | Integer       | Both           |
| transaction_alloc_block_size                 | Integer       | Both           |
| transaction_allow_batching                   | Boolean       | Session        |
| transaction_isolation                        | Enumeration   | Both           |
| transaction_prealloc_size                    | Integer       | Both           |
| transaction_read_only                        | Boolean       | Both           |
| transaction_write_set_extraction             | Enumeration   | Both           |
| unique_checks                                | Boolean       | Both           |

| Variable Name                                   | Variable Type | Variable Scope |
|-------------------------------------------------|---------------|----------------|
| updatable_views_with_limit                      | Boolean       | Both           |
| use_secondary_engine                            | Enumeration   | Session        |
| validate_password_check_user_name Boolean       |               | Global         |
| validate_password_dictionary_file File name     |               | Global         |
| validate_password_length                        | Integer       | Global         |
| validate_password_mixed_case_count Integer      |               | Global         |
| validate_password_number_countInteger           |               | Global         |
| validate_password_policy                        | Enumeration   | Global         |
| validate_password_special_char_count Integer    |               | Global         |
| validate_password.changed_characters_percentage | Integer       | Global         |
| validate_password.check_user_name Boolean       |               | Global         |
| validate_password.dictionary_file File name     |               | Global         |
| validate_password.length                        | Integer       | Global         |
| validate_password.mixed_case_count Integer      |               | Global         |
| validate_password.number_count Integer          |               | Global         |
| validate_password.policy                        | Enumeration   | Global         |
| validate_password.special_char_count Integer    |               | Global         |
| version_tokens_session                          | String        | Both           |
| wait_timeout                                    | Integer       | Both           |
| windowing_use_high_precision                    | Boolean       | Both           |
| xa_detach_on_prepare                            | Boolean       | Both           |

## <span id="page-61-0"></span>**7.1.9.3 Persisted System Variables**

The MySQL server maintains system variables that configure its operation. A system variable can have a global value that affects server operation as a whole, a session value that affects the current session, or both. Many system variables are dynamic and can be changed at runtime using the SET statement to affect operation of the current server instance. SET can also be used to persist certain global system variables to the mysqld-auto.cnf file in the data directory, to affect server operation for subsequent startups. RESET PERSIST removes persisted settings from mysqld-auto.cnf.

The following discussion describes aspects of persisting system variables:

- [Overview of Persisted System Variables](#page-61-1)
- [Syntax for Persisting System Variables](#page-62-0)
- [Obtaining Information About Persisted System Variables](#page-63-0)
- [Format and Server Handling of the mysqld-auto.cnf File](#page-63-1)
- [Persisting Sensitive System Variables](#page-65-1)

### <span id="page-61-1"></span>**Overview of Persisted System Variables**

The capability of persisting global system variables at runtime enables server configuration that persists across server startups. Although many system variables can be set at startup from a my.cnf option file, or at runtime using the SET statement, those methods of configuring the server either require login access to the server host, or do not provide the capability of persistently configuring the server at runtime or remotely:

- Modifying an option file requires direct access to that file, which requires login access to the MySQL server host. This is not always convenient.
- Modifying system variables with SET GLOBAL is a runtime capability that can be done from clients run locally or from remote hosts, but the changes affect only the currently running server instance. The settings are not persistent and do not carry over to subsequent server startups.

To augment administrative capabilities for server configuration beyond what is achievable by editing option files or using SET GLOBAL, MySQL provides variants of SET syntax that persist system variable settings to a file named mysqld-auto.cnf file in the data directory. Examples:

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
SET PERSIST_ONLY back_log = 100;
SET @@PERSIST_ONLY.back_log = 100;
```

MySQL also provides a RESET PERSIST statement for removing persisted system variables from mysqld-auto.cnf.

Server configuration performed by persisting system variables has these characteristics:

- Persisted settings are made at runtime.
- Persisted settings are permanent. They apply across server restarts.
- Persisted settings can be made from local clients or clients who connect from a remote host. This provides the convenience of remotely configuring multiple MySQL servers from a central client host.
- To persist system variables, you need not have login access to the MySQL server host or file system access to option files. Ability to persist settings is controlled using the MySQL privilege system. See [Section 7.1.9.1, "System Variable Privileges".](#page-42-0)
- An administrator with sufficient privileges can reconfigure a server by persisting system variables, then cause the server to use the changed settings immediately by executing a RESTART statement.
- Persisted settings provide immediate feedback about errors. An error in a manually entered setting might not be discovered until much later. SET statements that persist system variables avoid the possibility of malformed settings because settings with syntax errors do not succeed and do not change server configuration.

### <span id="page-62-0"></span>**Syntax for Persisting System Variables**

These SET syntax options are available for persisting system variables:

• To persist a global system variable to the mysqld-auto.cnf option file in the data directory, precede the variable name by the PERSIST keyword or the @@PERSIST. qualifier:

```
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
```

Like SET GLOBAL, SET PERSIST sets the global variable runtime value, but also writes the variable setting to the mysqld-auto.cnf file (replacing any existing variable setting if there is one).

• To persist a global system variable to the mysqld-auto.cnf file without setting the global variable runtime value, precede the variable name by the PERSIST\_ONLY keyword or the @@PERSIST\_ONLY. qualifier:

```
SET PERSIST_ONLY back_log = 1000;
SET @@PERSIST_ONLY.back_log = 1000;
```

Like PERSIST, PERSIST\_ONLY writes the variable setting to mysqld-auto.cnf. However, unlike PERSIST, PERSIST\_ONLY does not modify the global variable runtime value. This makes PERSIST\_ONLY suitable for configuring read-only system variables that can be set only at server startup.

For more information about SET, see Section 15.7.6.1, "SET Syntax for Variable Assignment".

These RESET PERSIST syntax options are available for removing persisted system variables:

• To remove all persisted variables from mysqld-auto.cnf, use RESET PERSIST without naming any system variable:

```
RESET PERSIST;
```

• To remove a specific persisted variable from mysqld-auto.cnf, name it in the statement:

```
RESET PERSIST system_var_name;
```

This includes plugin system variables, even if the plugin is not currently installed. If the variable is not present in the file, an error occurs.

• To remove a specific persisted variable from mysqld-auto.cnf, but produce a warning rather than an error if the variable is not present in the file, add an IF EXISTS clause to the previous syntax:

```
RESET PERSIST IF EXISTS system_var_name;
```

For more information about RESET PERSIST, see Section 15.7.8.7, "RESET PERSIST Statement".

Using SET to persist a global system variable to a value of DEFAULT or to its literal default value assigns the variable its default value and adds a setting for the variable to mysqld-auto.cnf. To remove the variable from the file, use RESET PERSIST.

Some system variables cannot be persisted. See [Section 7.1.9.4, "Nonpersistible and Persist-](#page-65-0)[Restricted System Variables".](#page-65-0)

A system variable implemented by a plugin can be persisted if the plugin is installed when the SET statement is executed. Assignment of the persisted plugin variable takes effect for subsequent server restarts if the plugin is still installed. If the plugin is no longer installed, the plugin variable does not exist when the server reads the mysqld-auto.cnf file. In this case, the server writes a warning to the error log and continues:

```
currently unknown variable 'var_name'
was read from the persisted config file
```

### <span id="page-63-0"></span>**Obtaining Information About Persisted System Variables**

The Performance Schema persisted\_variables table provides an SQL interface to the mysqldauto.cnf file, enabling its contents to be inspected at runtime using SELECT statements. See Section 29.12.14.1, "Performance Schema persisted\_variables Table".

The Performance Schema variables\_info table contains information showing when and by which user each system variable was most recently set. See Section 29.12.14.2, "Performance Schema variables\_info Table".

RESET PERSIST affects the contents of the persisted\_variables table because the table contents correspond to the contents of the mysqld-auto.cnf file. On the other hand, because RESET PERSIST does not change variable values, it has no effect on the contents of the variables\_info table until the server is restarted.

### <span id="page-63-1"></span>**Format and Server Handling of the mysqld-auto.cnf File**

The mysqld-auto.cnf file uses a JSON format like this (reformatted slightly for readability):

{

```
 "Version": 1,
 "mysql_server": {
 "max_connections": {
 "Value": "152",
 "Metadata": {
 "Timestamp": 1519921341372531,
 "User": "root",
 "Host": "localhost"
 }
 },
 "transaction_isolation": {
 "Value": "READ-COMMITTED",
 "Metadata": {
 "Timestamp": 1519921553880520,
 "User": "root",
 "Host": "localhost"
 }
 },
 "mysql_server_static_options": {
 "innodb_api_enable_mdl": {
 "Value": "0",
 "Metadata": {
 "Timestamp": 1519922873467872,
 "User": "root",
 "Host": "localhost"
 }
 },
 "log_slave_updates": {
 "Value": "1",
 "Metadata": {
 "Timestamp": 1519925628441588,
 "User": "root",
 "Host": "localhost"
 }
 }
 }
 }
}
```

At startup, the server processes the mysqld-auto.cnf file after all other option files (see Section 6.2.2.2, "Using Option Files"). The server handles the file contents as follows:

- If the persisted\_globals\_load system variable is disabled, the server ignores the mysqldauto.cnf file.
- The "mysql\_server\_static\_options" section contains read-only variables persisted using SET PERSIST\_ONLY. The section may also (despite its name) contain certain dynamic variables that are not read only. All variables present inside this section are appended to the command line and processed with other command-line options.
- All remaining persisted variables are set by executing the equivalent of a SET GLOBAL statement later, just before the server starts listening for client connections. These settings therefore do not take effect until late in the startup process, which might be unsuitable for certain system variables. It may be preferable to set such variables in my.cnf rather than in mysqld-auto.cnf.

Management of the mysqld-auto.cnf file should be left to the server. Manipulation of the file should be performed only using SET and RESET PERSIST statements, not manually:

• Removal of the file results in a loss of all persisted settings at the next server startup. (This is permissible if your intent is to reconfigure the server without these settings.) To remove all settings in the file without removing the file itself, use this statement:

RESET PERSIST;

• Manual changes to the file may result in a parse error at server startup. In this case, the server reports an error and exits. If this issue occurs, start the server with the persisted\_globals\_load system variable disabled or with the --no-defaults option. Alternatively, remove the mysqldauto.cnf file. However, as noted previously, removing this file results in a loss of all persisted settings.

### <span id="page-65-1"></span>**Persisting Sensitive System Variables**

From MySQL 8.0.29, MySQL Server has the capability to securely store persisted system variable values containing sensitive data such as private keys or passwords, and restrict viewing of the values. No MySQL Server system variables are currently marked as sensitive, but the new capability allows system variables containing sensitive data to be persisted securely in the future. After upgrading to MySQL 8.0.29, the format of the mysqld-auto.cnf option file remains the same until the first time a SET PERSIST or SET PERSIST ONLY statement is issued, and at that point it is changed to a new format, even if the system variable involved is not sensitive. In the new format, the option file cannot be read by older releases of MySQL Server.

![](_page_65_Picture_4.jpeg)

#### **Note**

A keyring component must be enabled on the MySQL Server instance to support secure storage for persisted system variable values, rather than a keyring plugin, which do not support the function. See Section 8.4.4, "The MySQL Keyring".

In the mysqld-auto.cnf option file, the names and values of sensitive system variables are stored in an encrypted format, along with a generated file key to decrypt them. The generated file key is in turn encrypted using a master key (persisted\_variables\_key) that is stored in a keyring. When the server starts up, the persisted sensitive system variables are decrypted and used. By default, if encrypted values are present in the option file but cannot be successfully decrypted at startup, their default settings are used. The optional most secure setting makes the server halt startup if the encrypted values cannot be decrypted.

The system variable persist\_sensitive\_variables\_in\_plaintext controls whether the server is permitted to store the values of sensitive system variables in an unencrypted format, if keyring component support is not available at the time when SET PERSIST is used to set the value. It also controls whether or not the server can start if the encrypted values cannot be decrypted.

- The default setting, ON, encrypts the values if keyring component support is available, and persists them unencrypted (with a warning) if it is not. The next time any persisted system variable is set, if keyring support is available at that time, the server encrypts the values of any unencrypted sensitive system variables. The ON setting also allows the server to start if encrypted system variable values cannot be decrypted, in which case a warning is issued and the default values for the system variables are used. In that situation, their values cannot be changed until they can be decrypted.
- The most secure setting, OFF, means sensitive system variable values cannot be persisted if keyring component support is unavailable. The OFF setting also means the server does not start if encrypted system variable values cannot be decrypted.

The privilege SENSITIVE\_VARIABLES\_OBSERVER allows a holder to view the values of sensitive system variables in the Performance Schema tables global\_variables, session\_variables, variables\_by\_thread, and persisted\_variables, to issue SELECT statements to return their values, and to track changes to them in session trackers for connections. Users without this privilege cannot view or track those system variable values.

If a SET statement is issued for a sensitive system variable, the query is rewritten to replace the value with "<redacted>" before it is logged to the general log and audit log. This takes place even if secure storage through a keyring component is not available on the server instance.

### <span id="page-65-0"></span>**7.1.9.4 Nonpersistible and Persist-Restricted System Variables**

SET PERSIST and SET PERSIST\_ONLY enable global system variables to be persisted to the mysqld-auto.cnf option file in the data directory (see Section 15.7.6.1, "SET Syntax for Variable Assignment"). However, not all system variables can be persisted, or can be persisted only under

certain restrictive conditions. Here are some reasons why a system variable might be nonpersistible or persist-restricted:

- Session system variables cannot be persisted. Session variables cannot be set at server startup, so there is no reason to persist them.
- A global system variable might involve sensitive data such that it should be settable only by a user with direct access to the server host.
- A global system variable might be read only (that is, set only by the server). In this case, it cannot be set by users at all, whether at server startup or at runtime.
- A global system variable might be intended only for internal use.

Nonpersistible system variables cannot be persisted under any circumstances. As of MySQL 8.0.14, persist-restricted system variables can be persisted with SET PERSIST\_ONLY, but only by users for which the following conditions are satisfied:

- The persist\_only\_admin\_x509\_subject system variable is set to an SSL certificate X.509 Subject value.
- The user connects to the server using an encrypted connection and supplies an SSL certificate with the designated Subject value.
- The user has sufficient privileges to use SET PERSIST\_ONLY (see [Section 7.1.9.1, "System](#page-42-0) [Variable Privileges"](#page-42-0)).

For example, protocol\_version is read only and set only by the server, so it cannot be persisted under any circumstances. On the other hand, bind\_address is persist-restricted, so it can be set by users who satisfy the preceding conditions.

The following system variables are nonpersistible. This list may change with ongoing development.

```
audit_log_current_session
audit_log_filter_id
caching_sha2_password_digest_rounds
character_set_system
core_file
have_statement_timeout
have_symlink
hostname
innodb_version
keyring_hashicorp_auth_path
keyring_hashicorp_ca_path
keyring_hashicorp_caching
keyring_hashicorp_commit_auth_path
keyring_hashicorp_commit_ca_path
keyring_hashicorp_commit_caching
keyring_hashicorp_commit_role_id
keyring_hashicorp_commit_server_url
keyring_hashicorp_commit_store_path
keyring_hashicorp_role_id
keyring_hashicorp_secret_id
keyring_hashicorp_server_url
keyring_hashicorp_store_path
large_files_support
large_page_size
license
locked_in_memory
log_bin
log_bin_basename
log_bin_index
lower_case_file_system
ndb_version
ndb_version_string
persist_only_admin_x509_subject
persisted_globals_load
```

```
protocol_version
relay_log_basename
relay_log_index
server_uuid
skip_external_locking
system_time_zone
version_comment
version_compile_machine
version_compile_os
version_compile_zlib
```

Persist-restricted system variables are those that are read only and can be set on the command line or in an option file, other than persist\_only\_admin\_x509\_subject and persisted\_globals\_load. This list may change with ongoing development.

```
audit_log_file
audit_log_format
auto_generate_certs
basedir
bind_address
caching_sha2_password_auto_generate_rsa_keys
caching_sha2_password_private_key_path
caching_sha2_password_public_key_path
character_sets_dir
daemon_memcached_engine_lib_name
daemon_memcached_engine_lib_path
daemon_memcached_option
datadir
default_authentication_plugin
ft_stopword_file
init_file
innodb_buffer_pool_load_at_startup
innodb_data_file_path
innodb_data_home_dir
innodb_dedicated_server
innodb_directories
innodb_force_load_corrupted
innodb_log_group_home_dir
innodb_page_size
innodb_read_only
innodb_temp_data_file_path
innodb_temp_tablespaces_dir
innodb_undo_directory
innodb_undo_tablespaces
keyring_encrypted_file_data
keyring_encrypted_file_password
lc_messages_dir
log_error
mecab_rc_file
named_pipe
pid_file
plugin_dir
port
relay_log
relay_log_info_file
replica_load_tmpdir
secure_file_priv
sha256_password_auto_generate_rsa_keys
sha256_password_private_key_path
sha256_password_public_key_path
shared_memory
shared_memory_base_name
skip_networking
slave_load_tmpdir
socket
ssl_ca
ssl_capath
ssl_cert
ssl_crl
ssl_crlpath
ssl_key
tmpdir
```

```
version_tokens_session_number
```

To configure the server to enable persisting persist-restricted system variables, use this procedure:

- 1. Ensure that MySQL is configured to support encrypted connections. See Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".
- 2. Designate an SSL certificate X.509 Subject value that signifies the ability to persist persistrestricted system variables, and generate a certificate that has that Subject. See Section 8.3.3, "Creating SSL and RSA Certificates and Keys".
- 3. Start the server with persist\_only\_admin\_x509\_subject set to the designated Subject value. For example, put these lines in your server my.cnf file:

```
[mysqld]
persist_only_admin_x509_subject="subject-value"
```

The format of the Subject value is the same as used for CREATE USER ... REQUIRE SUBJECT. See Section 15.7.1.3, "CREATE USER Statement".

You must perform this step directly on the MySQL server host because persist\_only\_admin\_x509\_subject itself cannot be persisted at runtime.

- 4. Restart the server.
- 5. Distribute the SSL certificate that has the designated Subject value to users who are to be permitted to persist persist-restricted system variables.

Suppose that myclient-cert.pem is the SSL certificate to be used by clients who can persist persist-restricted system variables. Display the certificate contents using the openssl command:

```
$> openssl x509 -text -in myclient-cert.pem
Certificate:
 Data:
 Version: 3 (0x2)
 Serial Number: 2 (0x2)
 Signature Algorithm: md5WithRSAEncryption
 Issuer: C=US, ST=IL, L=Chicago, O=MyOrg, OU=CA, CN=MyCN
 Validity
 Not Before: Oct 18 17:03:03 2018 GMT
 Not After : Oct 15 17:03:03 2028 GMT
 Subject: C=US, ST=IL, L=Chicago, O=MyOrg, OU=client, CN=MyCN
...
```

The openssl output shows that the certificate Subject value is:

```
C=US, ST=IL, L=Chicago, O=MyOrg, OU=client, CN=MyCN
```

To specify the Subject for MySQL, use this format:

```
/C=US/ST=IL/L=Chicago/O=MyOrg/OU=client/CN=MyCN
```

Configure the server my.cnf file with the Subject value:

```
[mysqld]
persist_only_admin_x509_subject="/C=US/ST=IL/L=Chicago/O=MyOrg/OU=client/CN=MyCN"
```

Restart the server so that the new configuration takes effect.

Distribute the SSL certificate (and any other associated SSL files) to the appropriate users. Such a user then connects to the server with the certificate and any other SSL options required to establish an encrypted connection.

To use X.509, clients must specify the --ssl-key and --ssl-cert options to connect. It is recommended but not required that --ssl-ca also be specified so that the public certificate provided by the server can be verified. For example:

```
$> mysql --ssl-key=myclient-key.pem --ssl-cert=myclient-cert.pem --ssl-ca=mycacert.pem
```

Assuming that the user has sufficient privileges to use SET PERSIST\_ONLY, persist-restricted system variables can be persisted like this:

```
mysql> SET PERSIST_ONLY socket = '/tmp/mysql.sock';
Query OK, 0 rows affected (0.00 sec)
```

If the server is not configured to enable persisting persist-restricted system variables, or the user does not satisfy the required conditions for that capability, an error occurs:

```
mysql> SET PERSIST_ONLY socket = '/tmp/mysql.sock';
ERROR 1238 (HY000): Variable 'socket' is a non persistent read only variable
```

### **7.1.9.5 Structured System Variables**

A structured variable differs from a regular system variable in two respects:

- Its value is a structure with components that specify server parameters considered to be closely related.
- There might be several instances of a given type of structured variable. Each one has a different name and refers to a different resource maintained by the server.

MySQL supports one structured variable type, which specifies parameters governing the operation of key caches. A key cache structured variable has these components:

- key\_buffer\_size
- key\_cache\_block\_size
- key\_cache\_division\_limit
- key\_cache\_age\_threshold

This section describes the syntax for referring to structured variables. Key cache variables are used for syntax examples, but specific details about how key caches operate are found elsewhere, in Section 10.10.2, "The MyISAM Key Cache".

To refer to a component of a structured variable instance, you can use a compound name in instance\_name.component\_name format. Examples:

```
hot_cache.key_buffer_size
hot_cache.key_cache_block_size
cold_cache.key_cache_block_size
```

For each structured system variable, an instance with the name of default is always predefined. If you refer to a component of a structured variable without any instance name, the default instance is used. Thus, default.key\_buffer\_size and key\_buffer\_size both refer to the same system variable.

Structured variable instances and components follow these naming rules:

- For a given type of structured variable, each instance must have a name that is unique within variables of that type. However, instance names need not be unique across structured variable types. For example, each structured variable has an instance named default, so default is not unique across variable types.
- The names of the components of each structured variable type must be unique across all system variable names. If this were not true (that is, if two different types of structured variables could share component member names), it would not be clear which default structured variable to use for references to member names that are not qualified by an instance name.

- If a structured variable instance name is not legal as an unquoted identifier, refer to it as a quoted identifier using backticks. For example, hot-cache is not legal, but `hot-cache` is.
- global, session, and local are not legal instance names. This avoids a conflict with notation such as @@GLOBAL.var\_name for referring to nonstructured system variables.

Currently, the first two rules have no possibility of being violated because the only structured variable type is the one for key caches. These rules may assume greater significance if some other type of structured variable is created in the future.

With one exception, you can refer to structured variable components using compound names in any context where simple variable names can occur. For example, you can assign a value to a structured variable using a command-line option:

```
$> mysqld --hot_cache.key_buffer_size=64K
```

In an option file, use this syntax:

```
[mysqld]
hot_cache.key_buffer_size=64K
```

If you start the server with this option, it creates a key cache named hot\_cache with a size of 64KB in addition to the default key cache that has a default size of 8MB.

Suppose that you start the server as follows:

```
$> mysqld --key_buffer_size=256K \
 --extra_cache.key_buffer_size=128K \
 --extra_cache.key_cache_block_size=2048
```

In this case, the server sets the size of the default key cache to 256KB. (You could also have written --default.key\_buffer\_size=256K.) In addition, the server creates a second key cache named extra\_cache that has a size of 128KB, with the size of block buffers for caching table index blocks set to 2048 bytes.

The following example starts the server with three different key caches having sizes in a 3:1:1 ratio:

```
$> mysqld --key_buffer_size=6M \
 --hot_cache.key_buffer_size=2M \
 --cold_cache.key_buffer_size=2M
```

Structured variable values may be set and retrieved at runtime as well. For example, to set a key cache named hot\_cache to a size of 10MB, use either of these statements:

```
mysql> SET GLOBAL hot_cache.key_buffer_size = 10*1024*1024;
mysql> SET @@GLOBAL.hot_cache.key_buffer_size = 10*1024*1024;
```

To retrieve the cache size, do this:

```
mysql> SELECT @@GLOBAL.hot_cache.key_buffer_size;
```

However, the following statement does not work. The variable is not interpreted as a compound name, but as a simple string for a LIKE pattern-matching operation:

```
mysql> SHOW GLOBAL VARIABLES LIKE 'hot_cache.key_buffer_size';
```

This is the exception to being able to use structured variable names anywhere a simple variable name may occur.

## <span id="page-70-0"></span>**7.1.10 Server Status Variables**

The MySQL server maintains many status variables that provide information about its operation. You can view these variables and their values by using the SHOW [GLOBAL | SESSION] STATUS statement (see Section 15.7.7.37, "SHOW STATUS Statement"). The optional GLOBAL keyword aggregates the values over all connections, and SESSION shows the values for the current connection.

| mysql> SHOW GLOBAL STATUS;           |                  |
|--------------------------------------|------------------|
| +++<br>  Variable_name<br>+++        | Value            |
| Aborted_clients                      | 0                |
| Aborted_connects<br>  Bytes_received | 0<br>  155372598 |
| Bytes_sent<br>                       | 1176560426       |
| Connections                          | 30023            |
| Created_tmp_disk_tables              | 0                |
| Created_tmp_files                    | 3                |
| Created_tmp_tables<br>               | 2                |
| Threads_created                      | 217              |
| Threads_running                      | 88               |
| Uptime                               | 1389872          |
| +++                                  |                  |

Many status variables are reset to 0 by the FLUSH STATUS statement.

This section provides a description of each status variable. For a status variable summary, see Section 7.1.6, "Server Status Variable Reference". For information about status variables specific to NDB Cluster, see NDB Cluster Status Variables.

The status variables have the following meanings.

<span id="page-71-0"></span>• [Aborted\\_clients](#page-71-0)

The number of connections that were aborted because the client died without closing the connection properly. See Section B.3.2.9, "Communication Errors and Aborted Connections".

<span id="page-71-1"></span>• [Aborted\\_connects](#page-71-1)

The number of failed attempts to connect to the MySQL server. See Section B.3.2.9, "Communication Errors and Aborted Connections".

For additional connection-related information, check the [Connection\\_errors\\_](#page-73-0)xxx status variables and the host\_cache table.

<span id="page-71-2"></span>• [Authentication\\_ldap\\_sasl\\_supported\\_methods](#page-71-2)

The authentication\_ldap\_sasl plugin that implements SASL LDAP authentication supports multiple authentication methods, but depending on host system configuration, they might not all be available. The [Authentication\\_ldap\\_sasl\\_supported\\_methods](#page-71-2) variable provides discoverability for the supported methods. Its value is a string consisting of supported method names separated by spaces. Example: "SCRAM-SHA 1 SCRAM-SHA-256 GSSAPI"

This variable was added in MySQL 8.0.21.

<span id="page-71-3"></span>• [Binlog\\_cache\\_disk\\_use](#page-71-3)

The number of transactions that used the temporary binary log cache but that exceeded the value of binlog\_cache\_size and used a temporary file to store statements from the transaction.

The number of nontransactional statements that caused the binary log transaction cache to be written to disk is tracked separately in the [Binlog\\_stmt\\_cache\\_disk\\_use](#page-72-0) status variable.

<span id="page-71-4"></span>• [Acl\\_cache\\_items\\_count](#page-71-4)

The number of cached privilege objects. Each object is the privilege combination of a user and its active roles.

<span id="page-72-1"></span>• [Binlog\\_cache\\_use](#page-72-1)

The number of transactions that used the binary log cache.

<span id="page-72-0"></span>• [Binlog\\_stmt\\_cache\\_disk\\_use](#page-72-0)

The number of nontransaction statements that used the binary log statement cache but that exceeded the value of binlog\_stmt\_cache\_size and used a temporary file to store those statements.

<span id="page-72-2"></span>• [Binlog\\_stmt\\_cache\\_use](#page-72-2)

The number of nontransactional statements that used the binary log statement cache.

<span id="page-72-3"></span>• [Bytes\\_received](#page-72-3)

The number of bytes received from all clients.

<span id="page-72-4"></span>• [Bytes\\_sent](#page-72-4)

The number of bytes sent to all clients.

<span id="page-72-5"></span>• [Caching\\_sha2\\_password\\_rsa\\_public\\_key](#page-72-5)

The public key used by the caching\_sha2\_password authentication plugin for RSA key pairbased password exchange. The value is nonempty only if the server successfully initializes the private and public keys in the files named by the caching\_sha2\_password\_private\_key\_path and caching\_sha2\_password\_public\_key\_path system variables. The value of [Caching\\_sha2\\_password\\_rsa\\_public\\_key](#page-72-5) comes from the latter file.

<span id="page-72-6"></span>• Com\_xxx

The Com\_xxx statement counter variables indicate the number of times each xxx statement has been executed. There is one status variable for each type of statement. For example, Com\_delete and Com\_update count DELETE and UPDATE statements, respectively. Com\_delete\_multi and Com\_update\_multi are similar but apply to DELETE and UPDATE statements that use multipletable syntax.

All Com\_stmt\_xxx variables are increased even if a prepared statement argument is unknown or an error occurred during execution. In other words, their values correspond to the number of requests issued, not to the number of requests successfully completed. For example, because status variables are initialized for each server startup and do not persist across restarts, the Com\_restart and Com\_shutdown variables that track RESTART and SHUTDOWN statements normally have a value of zero, but can be nonzero if RESTART or SHUTDOWN statements were executed but failed.

The Com\_stmt\_xxx status variables are as follows:

- Com\_stmt\_prepare
- Com\_stmt\_execute
- Com\_stmt\_fetch
- Com\_stmt\_send\_long\_data
- Com\_stmt\_reset
- Com\_stmt\_close

Those variables stand for prepared statement commands. Their names refer to the COM\_xxx command set used in the network layer. In other words, their values increase whenever prepared statement API calls such as mysql\_stmt\_prepare(), mysql\_stmt\_execute(), and so forth are executed. However, Com\_stmt\_prepare, Com\_stmt\_execute and Com\_stmt\_close also increase for PREPARE, EXECUTE, or DEALLOCATE PREPARE, respectively. Additionally, the values of the older statement counter variables Com\_prepare\_sql, Com\_execute\_sql, and Com\_dealloc\_sql increase for the PREPARE, EXECUTE, and DEALLOCATE PREPARE statements. Com\_stmt\_fetch stands for the total number of network round-trips issued when fetching from cursors.

Com\_stmt\_reprepare indicates the number of times statements were automatically reprepared by the server, for example, after metadata changes to tables or views referred to by the statement. A reprepare operation increments Com\_stmt\_reprepare, and also Com\_stmt\_prepare.

Com\_explain\_other indicates the number of EXPLAIN FOR CONNECTION statements executed. See Section 10.8.4, "Obtaining Execution Plan Information for a Named Connection".

Com\_change\_repl\_filter indicates the number of CHANGE REPLICATION FILTER statements executed.

#### <span id="page-73-1"></span>• [Compression](#page-73-1)

Whether the client connection uses compression in the client/server protocol.

As of MySQL 8.0.18, this status variable is deprecated; expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

#### <span id="page-73-2"></span>• [Compression\\_algorithm](#page-73-2)

The name of the compression algorithm in use for the current connection to the server. The value can be any algorithm permitted in the value of the protocol\_compression\_algorithms system variable. For example, the value is uncompressed if the connection does not use compression, or zlib if the connection uses the zlib algorithm.

For more information, see Section 6.2.8, "Connection Compression Control".

This variable was added in MySQL 8.0.18.

### <span id="page-73-3"></span>• [Compression\\_level](#page-73-3)

The compression level in use for the current connection to the server. The value is 6 for zlib connections (the default zlib algorithm compression level), 1 to 22 for zstd connections, and 0 for uncompressed connections.

For more information, see Section 6.2.8, "Connection Compression Control".

This variable was added in MySQL 8.0.18.

#### <span id="page-73-0"></span>• [Connection\\_errors\\_](#page-73-0)xxx

These variables provide information about errors that occur during the client connection process. They are global only and represent error counts aggregated across connections from all hosts. These variables track errors not accounted for by the host cache (see [Section 7.1.12.3, "DNS](#page-114-0) [Lookups and the Host Cache"](#page-114-0)), such as errors that are not associated with TCP connections, occur very early in the connection process (even before an IP address is known), or are not specific to any particular IP address (such as out-of-memory conditions).

### <span id="page-73-4"></span>• [Connection\\_errors\\_accept](#page-73-4)

The number of errors that occurred during calls to accept() on the listening port.

#### <span id="page-73-5"></span>• [Connection\\_errors\\_internal](#page-73-5)

The number of connections refused due to internal errors in the server, such as failure to start a new thread or an out-of-memory condition.

<span id="page-74-3"></span>• [Connection\\_errors\\_max\\_connections](#page-74-3)

The number of connections refused because the server max\_connections limit was reached.

<span id="page-74-4"></span>• [Connection\\_errors\\_peer\\_address](#page-74-4)

The number of errors that occurred while searching for connecting client IP addresses.

<span id="page-74-5"></span>• [Connection\\_errors\\_select](#page-74-5)

The number of errors that occurred during calls to select() or poll() on the listening port. (Failure of this operation does not necessarily means a client connection was rejected.)

<span id="page-74-6"></span>• [Connection\\_errors\\_tcpwrap](#page-74-6)

The number of connections refused by the libwrap library.

<span id="page-74-0"></span>• [Connections](#page-74-0)

The number of connection attempts (successful or not) to the MySQL server.

<span id="page-74-1"></span>• [Created\\_tmp\\_disk\\_tables](#page-74-1)

The number of internal on-disk temporary tables created by the server while executing statements.

You can compare the number of internal on-disk temporary tables created to the total number of internal temporary tables created by comparing [Created\\_tmp\\_disk\\_tables](#page-74-1) and [Created\\_tmp\\_tables](#page-74-2) values.

![](_page_74_Picture_14.jpeg)

#### **Note**

Due to a known limitation, [Created\\_tmp\\_disk\\_tables](#page-74-1) does not count on-disk temporary tables created in memory-mapped files. By default, the TempTable storage engine overflow mechanism creates internal temporary tables in memory-mapped files. This behavior is controlled by the [temptable\\_use\\_mmap](#page-22-0) variable, which is enabled by default.

See also Section 10.4.4, "Internal Temporary Table Use in MySQL".

<span id="page-74-7"></span>• [Created\\_tmp\\_files](#page-74-7)

How many temporary files mysqld has created.

<span id="page-74-2"></span>• [Created\\_tmp\\_tables](#page-74-2)

The number of internal temporary tables created by the server while executing statements.

You can compare the number of internal on-disk temporary tables created to the total number of internal temporary tables created by comparing [Created\\_tmp\\_disk\\_tables](#page-74-1) and [Created\\_tmp\\_tables](#page-74-2) values.

See also Section 10.4.4, "Internal Temporary Table Use in MySQL".

Each invocation of the SHOW STATUS statement uses an internal temporary table and increments the global [Created\\_tmp\\_tables](#page-74-2) value.

<span id="page-74-8"></span>• [Current\\_tls\\_ca](#page-74-8)

The active [ssl\\_ca](#page-9-2) value in the SSL context that the server uses for new connections. This context value may differ from the current [ssl\\_ca](#page-9-2) system variable value if the system variable has been changed but ALTER INSTANCE RELOAD TLS has not subsequently been executed to reconfigure the SSL context from the context-related system variable values and update the corresponding

status variables. (This potential difference in values applies to each corresponding pair of contextrelated system and status variables. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections.)

This variable was added in MySQL 8.0.16.

As of MySQL 8.0.21, the Current\_tls\_xxx status variable values are also available through the Performance Schema tls\_channel\_status table. See Section 29.12.21.9, "The tls\_channel\_status Table".

<span id="page-75-0"></span>• [Current\\_tls\\_capath](#page-75-0)

The active [ssl\\_capath](#page-10-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-75-1"></span>• [Current\\_tls\\_cert](#page-75-1)

The active [ssl\\_cert](#page-10-1) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-75-2"></span>• [Current\\_tls\\_cipher](#page-75-2)

The active [ssl\\_cipher](#page-11-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-75-3"></span>• [Current\\_tls\\_ciphersuites](#page-75-3)

The active [tls\\_ciphersuites](#page-30-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-75-4"></span>• [Current\\_tls\\_crl](#page-75-4)

The active [ssl\\_crl](#page-11-1) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

![](_page_75_Picture_19.jpeg)

### **Note**

When you reload the TLS context, OpenSSL reloads the file containing the CRL (certificate revocation list) as part of the process. If the CRL file is large, the server allocates a large chunk of memory (ten times the file size), which is doubled while the new instance is being loaded and the old one has not yet been released. The process resident memory is not immediately reduced after a large allocation is freed, so if you issue the ALTER INSTANCE RELOAD TLS statement repeatedly with a large CRL file, the process resident memory usage may grow as a result of this.

<span id="page-75-5"></span>• [Current\\_tls\\_crlpath](#page-75-5)

The active [ssl\\_crlpath](#page-12-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-76-0"></span>• [Current\\_tls\\_key](#page-76-0)

The active [ssl\\_key](#page-13-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-76-1"></span>• [Current\\_tls\\_version](#page-76-1)

The active [tls\\_version](#page-30-1) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-74-8).

This variable was added in MySQL 8.0.16.

<span id="page-76-2"></span>• [Delayed\\_errors](#page-76-2)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-76-3"></span>• [Delayed\\_insert\\_threads](#page-76-3)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-76-4"></span>• [Delayed\\_writes](#page-76-4)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-76-5"></span>• [dragnet.Status](#page-76-5)

The result of the most recent assignment to the dragnet.log\_error\_filter\_rules system variable, empty if no such assignment has occurred.

This variable was added in MySQL 8.0.12.

<span id="page-76-6"></span>• [Error\\_log\\_buffered\\_bytes](#page-76-6)

The number of bytes currently used in the Performance Schema error\_log table. It is possible for the value to decrease, for example, if a new event cannot fit until discarding an old event, but the new event is smaller than the old one.

This variable was added in MySQL 8.0.22.

<span id="page-76-7"></span>• [Error\\_log\\_buffered\\_events](#page-76-7)

The number of events currently present in the Performance Schema error\_log table. As with [Error\\_log\\_buffered\\_bytes](#page-76-6), it is possible for the value to decrease.

This variable was added in MySQL 8.0.22.

<span id="page-77-0"></span>• [Error\\_log\\_expired\\_events](#page-77-0)

The number of events discarded from the Performance Schema error\_log table to make room for new events.

This variable was added in MySQL 8.0.22.

<span id="page-77-1"></span>• [Error\\_log\\_latest\\_write](#page-77-1)

The time of the last write to the Performance Schema error\_log table.

This variable was added in MySQL 8.0.22.

<span id="page-77-2"></span>• [Flush\\_commands](#page-77-2)

The number of times the server flushes tables, whether because a user executed a FLUSH TABLES statement or due to internal server operation. It is also incremented by receipt of a COM\_REFRESH packet. This is in contrast to [Com\\_flush](#page-72-6), which indicates how many FLUSH statements have been executed, whether FLUSH TABLES, FLUSH LOGS, and so forth.

<span id="page-77-3"></span>• [Global\\_connection\\_memory](#page-77-3)

The memory used by all user connections to the server. Memory used by system threads or by the MySQL root account is included in the total, but such threads or users are not subject to disconnection due to memory usage. This memory is not calculated unless global\_connection\_memory\_tracking is enabled (disabled by default). The Performance Schema must also be enabled.

You can control (indirectly) the frequency with which this variable is updated by setting connection\_memory\_chunk\_size.

The Global\_connection\_memory status variable was introduced in MySQL 8.0.28.

<span id="page-77-4"></span>• [Handler\\_commit](#page-77-4)

The number of internal COMMIT statements.

<span id="page-77-5"></span>• [Handler\\_delete](#page-77-5)

The number of times that rows have been deleted from tables.

<span id="page-77-6"></span>• [Handler\\_external\\_lock](#page-77-6)

The server increments this variable for each call to its external\_lock() function, which generally occurs at the beginning and end of access to a table instance. There might be differences among storage engines. This variable can be used, for example, to discover for a statement that accesses a partitioned table how many partitions were pruned before locking occurred: Check how much the counter increased for the statement, subtract 2 (2 calls for the table itself), then divide by 2 to get the number of partitions locked.

<span id="page-77-7"></span>• [Handler\\_mrr\\_init](#page-77-7)

The number of times the server uses a storage engine's own Multi-Range Read implementation for table access.

<span id="page-77-8"></span>• [Handler\\_prepare](#page-77-8)

A counter for the prepare phase of two-phase commit operations.

<span id="page-78-0"></span>• [Handler\\_read\\_first](#page-78-0)

The number of times the first entry in an index was read. If this value is high, it suggests that the server is doing a lot of full index scans (for example, SELECT col1 FROM foo, assuming that col1 is indexed).

<span id="page-78-1"></span>• [Handler\\_read\\_key](#page-78-1)

The number of requests to read a row based on a key. If this value is high, it is a good indication that your tables are properly indexed for your queries.

<span id="page-78-2"></span>• [Handler\\_read\\_last](#page-78-2)

The number of requests to read the last key in an index. With ORDER BY, the server issues a firstkey request followed by several next-key requests, whereas with ORDER BY DESC, the server issues a last-key request followed by several previous-key requests.

<span id="page-78-3"></span>• [Handler\\_read\\_next](#page-78-3)

The number of requests to read the next row in key order. This value is incremented if you are querying an index column with a range constraint or if you are doing an index scan.

<span id="page-78-4"></span>• [Handler\\_read\\_prev](#page-78-4)

The number of requests to read the previous row in key order. This read method is mainly used to optimize ORDER BY ... DESC.

<span id="page-78-5"></span>• [Handler\\_read\\_rnd](#page-78-5)

The number of requests to read a row based on a fixed position. This value is high if you are doing a lot of queries that require sorting of the result. You probably have a lot of queries that require MySQL to scan entire tables or you have joins that do not use keys properly.

<span id="page-78-6"></span>• [Handler\\_read\\_rnd\\_next](#page-78-6)

The number of requests to read the next row in the data file. This value is high if you are doing a lot of table scans. Generally this suggests that your tables are not properly indexed or that your queries are not written to take advantage of the indexes you have.

<span id="page-78-7"></span>• [Handler\\_rollback](#page-78-7)

The number of requests for a storage engine to perform a rollback operation.

<span id="page-78-8"></span>• [Handler\\_savepoint](#page-78-8)

The number of requests for a storage engine to place a savepoint.

<span id="page-78-9"></span>• [Handler\\_savepoint\\_rollback](#page-78-9)

The number of requests for a storage engine to roll back to a savepoint.

<span id="page-78-10"></span>• [Handler\\_update](#page-78-10)

The number of requests to update a row in a table.

<span id="page-78-11"></span>• [Handler\\_write](#page-78-11)

The number of requests to insert a row in a table.

<span id="page-78-12"></span>• [Innodb\\_buffer\\_pool\\_dump\\_status](#page-78-12)

The progress of an operation to record the pages held in the InnoDB buffer pool, triggered by the setting of innodb\_buffer\_pool\_dump\_at\_shutdown or innodb\_buffer\_pool\_dump\_now. For related information and examples, see Section 17.8.3.6, "Saving and Restoring the Buffer Pool State".

<span id="page-79-0"></span>• [Innodb\\_buffer\\_pool\\_load\\_status](#page-79-0)

The progress of an operation to warm up the InnoDB buffer pool by reading in a set of pages corresponding to an earlier point in time, triggered by the setting of innodb\_buffer\_pool\_load\_at\_startup or innodb\_buffer\_pool\_load\_now. If the operation introduces too much overhead, you can cancel it by setting innodb\_buffer\_pool\_load\_abort.

For related information and examples, see Section 17.8.3.6, "Saving and Restoring the Buffer Pool State".

<span id="page-79-1"></span>• [Innodb\\_buffer\\_pool\\_bytes\\_data](#page-79-1)

The total number of bytes in the InnoDB buffer pool containing data. The number includes both dirty and clean pages. For more accurate memory usage calculations than with [Innodb\\_buffer\\_pool\\_pages\\_data](#page-79-2), when compressed tables cause the buffer pool to hold pages of different sizes.

<span id="page-79-2"></span>• [Innodb\\_buffer\\_pool\\_pages\\_data](#page-79-2)

The number of pages in the InnoDB buffer pool containing data. The number includes both dirty and clean pages. When using compressed tables, the reported [Innodb\\_buffer\\_pool\\_pages\\_data](#page-79-2) value may be larger than [Innodb\\_buffer\\_pool\\_pages\\_total](#page-79-3) (Bug #59550).

<span id="page-79-4"></span>• [Innodb\\_buffer\\_pool\\_bytes\\_dirty](#page-79-4)

The total current number of bytes held in dirty pages in the InnoDB buffer pool. For more accurate memory usage calculations than with [Innodb\\_buffer\\_pool\\_pages\\_dirty](#page-79-5), when compressed tables cause the buffer pool to hold pages of different sizes.

<span id="page-79-5"></span>• [Innodb\\_buffer\\_pool\\_pages\\_dirty](#page-79-5)

The current number of dirty pages in the InnoDB buffer pool.

<span id="page-79-6"></span>• [Innodb\\_buffer\\_pool\\_pages\\_flushed](#page-79-6)

The number of requests to flush pages from the InnoDB buffer pool.

<span id="page-79-7"></span>• [Innodb\\_buffer\\_pool\\_pages\\_free](#page-79-7)

The number of free pages in the InnoDB buffer pool.

<span id="page-79-8"></span>• [Innodb\\_buffer\\_pool\\_pages\\_latched](#page-79-8)

The number of latched pages in the InnoDB buffer pool. These are pages currently being read or written, or that cannot be flushed or removed for some other reason. Calculation of this variable is expensive, so it is available only when the UNIV\_DEBUG system is defined at server build time.

<span id="page-79-9"></span>• [Innodb\\_buffer\\_pool\\_pages\\_misc](#page-79-9)

The number of pages in the InnoDB buffer pool that are busy because they have been allocated for administrative overhead, such as row locks or the adaptive hash index. This value can also be calculated as [Innodb\\_buffer\\_pool\\_pages\\_total](#page-79-3) − [Innodb\\_buffer\\_pool\\_pages\\_free](#page-79-7) − [Innodb\\_buffer\\_pool\\_pages\\_data](#page-79-2). When using compressed tables, [Innodb\\_buffer\\_pool\\_pages\\_misc](#page-79-9) may report an out-of-bounds value (Bug #59550).

<span id="page-79-3"></span>• [Innodb\\_buffer\\_pool\\_pages\\_total](#page-79-3)

The total size of the InnoDB buffer pool, in pages. When using compressed tables, the reported [Innodb\\_buffer\\_pool\\_pages\\_data](#page-79-2) value may be larger than [Innodb\\_buffer\\_pool\\_pages\\_total](#page-79-3) (Bug #59550)

<span id="page-80-0"></span>• [Innodb\\_buffer\\_pool\\_read\\_ahead](#page-80-0)

The number of pages read into the InnoDB buffer pool by the read-ahead background thread.

<span id="page-80-1"></span>• [Innodb\\_buffer\\_pool\\_read\\_ahead\\_evicted](#page-80-1)

The number of pages read into the InnoDB buffer pool by the read-ahead background thread that were subsequently evicted without having been accessed by queries.

<span id="page-80-2"></span>• [Innodb\\_buffer\\_pool\\_read\\_ahead\\_rnd](#page-80-2)

The number of "random" read-aheads initiated by InnoDB. This happens when a query scans a large portion of a table but in random order.

<span id="page-80-3"></span>• [Innodb\\_buffer\\_pool\\_read\\_requests](#page-80-3)

The number of logical read requests.

<span id="page-80-4"></span>• [Innodb\\_buffer\\_pool\\_reads](#page-80-4)

The number of logical reads that InnoDB could not satisfy from the buffer pool, and had to read directly from disk.

<span id="page-80-5"></span>• [Innodb\\_buffer\\_pool\\_resize\\_status](#page-80-5)

The status of an operation to resize the InnoDB buffer pool dynamically, triggered by setting the innodb\_buffer\_pool\_size parameter dynamically. The innodb\_buffer\_pool\_size parameter is dynamic, which allows you to resize the buffer pool without restarting the server. See Configuring InnoDB Buffer Pool Size Online for related information.

<span id="page-80-6"></span>• [Innodb\\_buffer\\_pool\\_resize\\_status\\_code](#page-80-6)

Reports status codes for tracking online buffer pool resizing operations. Each status code represents a stage in a resizing operation. Status codes include:

- 0: No Resize operation in progress
- 1: Starting Resize
- 2: Disabling AHI (Adaptive Hash Index)
- 3: Withdrawing Blocks
- 4: Acquiring Global Lock
- 5: Resizing Pool
- 6: Resizing Hash
- 7: Resizing Failed

You can use this status variable in conjunction with

[Innodb\\_buffer\\_pool\\_resize\\_status\\_progress](#page-81-0) to track the progress of each stage of a resizing operation. The [Innodb\\_buffer\\_pool\\_resize\\_status\\_progress](#page-81-0) variable reports a percentage value indicating the progress of the current stage.

For more information, see Monitoring Online Buffer Pool Resizing Progress.

<span id="page-81-0"></span>• [Innodb\\_buffer\\_pool\\_resize\\_status\\_progress](#page-81-0)

Reports a percentage value indicating the progress of the current stage of an online buffer pool resizing operation. This variable is used in conjunction with [Innodb\\_buffer\\_pool\\_resize\\_status\\_code](#page-80-6), which reports a status code indicating the current stage of an online buffer pool resizing operation.

The percentage value is updated after each buffer pool instance is processed. As the status code (reported by [Innodb\\_buffer\\_pool\\_resize\\_status\\_code](#page-80-6)) changes from one status to another, the percentage value is reset to 0.

For related information, see Monitoring Online Buffer Pool Resizing Progress.

<span id="page-81-1"></span>• [Innodb\\_buffer\\_pool\\_wait\\_free](#page-81-1)

Normally, writes to the InnoDB buffer pool happen in the background. When InnoDB needs to read or create a page and no clean pages are available, InnoDB flushes some dirty pages first and waits for that operation to finish. This counter counts instances of these waits. If innodb\_buffer\_pool\_size has been set properly, this value should be small.

<span id="page-81-2"></span>• [Innodb\\_buffer\\_pool\\_write\\_requests](#page-81-2)

The number of writes done to the InnoDB buffer pool.

<span id="page-81-3"></span>• [Innodb\\_data\\_fsyncs](#page-81-3)

The number of fsync() operations so far. The frequency of fsync() calls is influenced by the setting of the innodb\_flush\_method configuration option.

Counts the number of fdatasync() operations if innodb\_use\_fdatasync is enabled.

<span id="page-81-4"></span>• [Innodb\\_data\\_pending\\_fsyncs](#page-81-4)

The current number of pending fsync() operations. The frequency of fsync() calls is influenced by the setting of the innodb\_flush\_method configuration option.

<span id="page-81-5"></span>• [Innodb\\_data\\_pending\\_reads](#page-81-5)

The current number of pending reads.

<span id="page-81-6"></span>• [Innodb\\_data\\_pending\\_writes](#page-81-6)

The current number of pending writes.

<span id="page-81-7"></span>• [Innodb\\_data\\_read](#page-81-7)

The amount of data read since the server was started (in bytes).

<span id="page-81-8"></span>• [Innodb\\_data\\_reads](#page-81-8)

The total number of data reads (OS file reads).

<span id="page-81-9"></span>• [Innodb\\_data\\_writes](#page-81-9)

The total number of data writes.

<span id="page-81-10"></span>• [Innodb\\_data\\_written](#page-81-10)

The amount of data written so far, in bytes.

<span id="page-81-11"></span>• [Innodb\\_dblwr\\_pages\\_written](#page-81-11)

The number of pages that have been written to the doublewrite buffer. See Section 17.11.1, "InnoDB Disk I/O".

<span id="page-82-0"></span>• [Innodb\\_dblwr\\_writes](#page-82-0)

The number of doublewrite operations that have been performed. See Section 17.11.1, "InnoDB Disk I/O".

<span id="page-82-1"></span>• [Innodb\\_have\\_atomic\\_builtins](#page-82-1)

Indicates whether the server was built with atomic instructions.

<span id="page-82-2"></span>• [Innodb\\_log\\_waits](#page-82-2)

The number of times that the log buffer was too small and a wait was required for it to be flushed before continuing.

<span id="page-82-3"></span>• [Innodb\\_log\\_write\\_requests](#page-82-3)

The number of write requests for the InnoDB redo log.

<span id="page-82-4"></span>• [Innodb\\_log\\_writes](#page-82-4)

The number of physical writes to the InnoDB redo log file.

<span id="page-82-5"></span>• [Innodb\\_num\\_open\\_files](#page-82-5)

The number of files InnoDB currently holds open.

<span id="page-82-6"></span>• [Innodb\\_os\\_log\\_fsyncs](#page-82-6)

The number of fsync() writes done to the InnoDB redo log files.

<span id="page-82-7"></span>• [Innodb\\_os\\_log\\_pending\\_fsyncs](#page-82-7)

The number of pending fsync() operations for the InnoDB redo log files.

<span id="page-82-8"></span>• [Innodb\\_os\\_log\\_pending\\_writes](#page-82-8)

The number of pending writes to the InnoDB redo log files.

<span id="page-82-9"></span>• [Innodb\\_os\\_log\\_written](#page-82-9)

The number of bytes written to the InnoDB redo log files.

<span id="page-82-10"></span>• [Innodb\\_page\\_size](#page-82-10)

InnoDB page size (default 16KB). Many values are counted in pages; the page size enables them to be easily converted to bytes.

<span id="page-82-11"></span>• [Innodb\\_pages\\_created](#page-82-11)

The number of pages created by operations on InnoDB tables.

<span id="page-82-12"></span>• [Innodb\\_pages\\_read](#page-82-12)

The number of pages read from the InnoDB buffer pool by operations on InnoDB tables.

<span id="page-82-13"></span>• [Innodb\\_pages\\_written](#page-82-13)

The number of pages written by operations on InnoDB tables.

<span id="page-82-14"></span>• [Innodb\\_redo\\_log\\_enabled](#page-82-14)

Whether redo logging is enabled or disabled. See Disabling Redo Logging.

This variable was added in MySQL 8.0.21.

<span id="page-83-0"></span>• [Innodb\\_redo\\_log\\_capacity\\_resized](#page-83-0)

The total redo log capacity for all redo log files, in bytes, after the last completed capacity resize operation. The value includes ordinary and spare redo log files.

If there is no pending resize down operation, [Innodb\\_redo\\_log\\_capacity\\_resized](#page-83-0) should be equal to the innodb\_redo\_log\_capacity setting if it's used, or it's ((innodb\_log\_files\_in\_group \* innodb\_log\_file\_size)) if those are used instead. See the innodb\_redo\_log\_capacity documentation for further clarification. Resize up operations are instantaneous.

For related information, see Section 17.6.5, "Redo Log".

This variable was added in MySQL 8.0.30.

<span id="page-83-1"></span>• [Innodb\\_redo\\_log\\_checkpoint\\_lsn](#page-83-1)

The redo log checkpoint LSN. For related information, see Section 17.6.5, "Redo Log".

This variable was added in MySQL 8.0.30.

<span id="page-83-2"></span>• [Innodb\\_redo\\_log\\_current\\_lsn](#page-83-2)

The current LSN represents the last written position in the redo log buffer. InnoDB writes data to the redo log buffer inside the MySQL process before requesting that the operating system write the data to the current redo log file. For related information, see Section 17.6.5, "Redo Log".

This variable was added in MySQL 8.0.30.

<span id="page-83-3"></span>• [Innodb\\_redo\\_log\\_flushed\\_to\\_disk\\_lsn](#page-83-3)

The flushed-to-disk LSN. InnoDB first writes data to the redo log and then requests that the operating system flush the data to disk. The flushed-to-disk LSN represents the last position in the redo log that InnoDB knows has been flushed to disk. For related information, see Section 17.6.5, "Redo Log".

This variable was added in MySQL 8.0.30.

<span id="page-83-4"></span>• [Innodb\\_redo\\_log\\_logical\\_size](#page-83-4)

A data size value, in bytes, representing the LSN range containing in-use redo log data, spanning from the oldest block required by redo log consumers to the latest written block. For related information, see Section 17.6.5, "Redo Log".

This variable was added in MySQL 8.0.30.

<span id="page-83-5"></span>• [Innodb\\_redo\\_log\\_physical\\_size](#page-83-5)

The amount of disk space in bytes currently consumed by all redo log files on disk, excluding spare redo log files. For related information, see Section 17.6.5, "Redo Log".

This variable was added in MySQL 8.0.30.

<span id="page-83-6"></span>• [Innodb\\_redo\\_log\\_read\\_only](#page-83-6)

Whether the redo log is read-only.

This variable was added in MySQL 8.0.30.

<span id="page-84-0"></span>• [Innodb\\_redo\\_log\\_resize\\_status](#page-84-0)

The redo log resize status indicating the current state of the redo log capacity resize mechanism. Possible values include:

- OK: There are no issues and no pending redo log capacity resize operations.
- Resizing down: A resize down operation is in progress.

A resize up operation is instantaneous and therefore has no pending status.

This variable was added in MySQL 8.0.30.

<span id="page-84-1"></span>• [Innodb\\_redo\\_log\\_uuid](#page-84-1)

The redo log UUID.

This variable was added in MySQL 8.0.30.

<span id="page-84-2"></span>• [Innodb\\_row\\_lock\\_current\\_waits](#page-84-2)

The number of row locks currently waited for by operations on InnoDB tables.

<span id="page-84-3"></span>• [Innodb\\_row\\_lock\\_time](#page-84-3)

The total time spent in acquiring row locks for InnoDB tables, in milliseconds.

<span id="page-84-4"></span>• [Innodb\\_row\\_lock\\_time\\_avg](#page-84-4)

The average time to acquire a row lock for InnoDB tables, in milliseconds.

<span id="page-84-5"></span>• [Innodb\\_row\\_lock\\_time\\_max](#page-84-5)

The maximum time to acquire a row lock for InnoDB tables, in milliseconds.

<span id="page-84-6"></span>• [Innodb\\_row\\_lock\\_waits](#page-84-6)

The number of times operations on InnoDB tables had to wait for a row lock.

<span id="page-84-7"></span>• [Innodb\\_rows\\_deleted](#page-84-7)

The number of rows deleted from InnoDB tables.

<span id="page-84-8"></span>• [Innodb\\_rows\\_inserted](#page-84-8)

The number of rows inserted into InnoDB tables.

<span id="page-84-9"></span>• [Innodb\\_rows\\_read](#page-84-9)

The number of rows read from InnoDB tables.

<span id="page-84-10"></span>• [Innodb\\_rows\\_updated](#page-84-10)

The estimated number of rows updated in InnoDB tables.

![](_page_84_Picture_28.jpeg)

#### **Note**

This value is not meant to be 100% accurate. For an accurate (but more expensive) result, use ROW\_COUNT().

<span id="page-84-11"></span>• [Innodb\\_system\\_rows\\_deleted](#page-84-11)

The number of rows deleted from InnoDB tables belonging to system-created schemas.

<span id="page-84-12"></span>• [Innodb\\_system\\_rows\\_inserted](#page-84-12)

The number of rows inserted into InnoDB tables belonging to system-created schemas.

<span id="page-85-0"></span>• [Innodb\\_system\\_rows\\_updated](#page-85-0)

The number of rows updated in InnoDB tables belonging to system-created schemas.

<span id="page-85-1"></span>• [Innodb\\_system\\_rows\\_read](#page-85-1)

The number of rows read from InnoDB tables belonging to system-created schemas.

<span id="page-85-2"></span>• [Innodb\\_truncated\\_status\\_writes](#page-85-2)

The number of times output from the SHOW ENGINE INNODB STATUS statement has been truncated.

<span id="page-85-3"></span>• [Innodb\\_undo\\_tablespaces\\_active](#page-85-3)

The number of active undo tablespaces. Includes both implicit (InnoDB-created) and explicit (usercreated) undo tablespaces. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-85-4"></span>• [Innodb\\_undo\\_tablespaces\\_explicit](#page-85-4)

The number of user-created undo tablespaces. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-85-5"></span>• [Innodb\\_undo\\_tablespaces\\_implicit](#page-85-5)

The number of undo tablespaces created by InnoDB. Two default undo tablespaces are created by InnoDB when the MySQL instance is initialized. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-85-6"></span>• [Innodb\\_undo\\_tablespaces\\_total](#page-85-6)

The total number of undo tablespaces. Includes both implicit (InnoDB-created) and explicit (usercreated) undo tablespaces, active and inactive. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-85-7"></span>• [Key\\_blocks\\_not\\_flushed](#page-85-7)

The number of key blocks in the MyISAM key cache that have changed but have not yet been flushed to disk.

<span id="page-85-8"></span>• [Key\\_blocks\\_unused](#page-85-8)

The number of unused blocks in the MyISAM key cache. You can use this value to determine how much of the key cache is in use; see the discussion of key\_buffer\_size in Section 7.1.8, "Server System Variables".

<span id="page-85-9"></span>• [Key\\_blocks\\_used](#page-85-9)

The number of used blocks in the MyISAM key cache. This value is a high-water mark that indicates the maximum number of blocks that have ever been in use at one time.

<span id="page-85-10"></span>• [Key\\_read\\_requests](#page-85-10)

The number of requests to read a key block from the MyISAM key cache.

<span id="page-85-11"></span>• [Key\\_reads](#page-85-11)

The number of physical reads of a key block from disk into the MyISAM key cache. If [Key\\_reads](#page-85-11) is large, then your key\_buffer\_size value is probably too small. The cache miss rate can be calculated as [Key\\_reads](#page-85-11)/[Key\\_read\\_requests](#page-85-10).

<span id="page-86-0"></span>• [Key\\_write\\_requests](#page-86-0)

The number of requests to write a key block to the MyISAM key cache.

<span id="page-86-1"></span>• [Key\\_writes](#page-86-1)

The number of physical writes of a key block from the MyISAM key cache to disk.

<span id="page-86-2"></span>• [Last\\_query\\_cost](#page-86-2)

The total cost of the last compiled query as computed by the query optimizer. This is useful for comparing the cost of different query plans for the same query. The default value of 0 means that no query has been compiled yet. The default value is 0. [Last\\_query\\_cost](#page-86-2) has session scope.

In MySQL 8.0.16 and later, this variable shows the cost of queries that have multiple query blocks, summing the cost estimates of each query block, estimating how many times non-cacheable subqueries are executed, and multiplying the cost of those query blocks by the number of subquery executions. (Bug #92766, Bug #28786951) Prior to MySQL 8.0.16, Last\_query\_cost was computed accurately only for simple, "flat" queries, but not for complex queries such as those containing subqueries or UNION. (For the latter, the value was set to 0.)

<span id="page-86-3"></span>• [Last\\_query\\_partial\\_plans](#page-86-3)

The number of iterations the query optimizer made in execution plan construction for the previous query.

Last\_query\_partial\_plans has session scope.

<span id="page-86-4"></span>• [Locked\\_connects](#page-86-4)

The number of attempts to connect to locked user accounts. For information about account locking and unlocking, see Section 8.2.20, "Account Locking".

<span id="page-86-5"></span>• [Max\\_execution\\_time\\_exceeded](#page-86-5)

The number of SELECT statements for which the execution timeout was exceeded.

<span id="page-86-6"></span>• [Max\\_execution\\_time\\_set](#page-86-6)

The number of SELECT statements for which a nonzero execution timeout was set. This includes statements that include a nonzero MAX\_EXECUTION\_TIME optimizer hint, and statements that include no such hint but execute while the timeout indicated by the max\_execution\_time system variable is nonzero.

<span id="page-86-7"></span>• [Max\\_execution\\_time\\_set\\_failed](#page-86-7)

The number of SELECT statements for which the attempt to set an execution timeout failed.

<span id="page-86-8"></span>• [Max\\_used\\_connections](#page-86-8)

The maximum number of connections that have been in use simultaneously since the server started.

<span id="page-86-9"></span>• [Max\\_used\\_connections\\_time](#page-86-9)

The time at which [Max\\_used\\_connections](#page-86-8) reached its current value.

<span id="page-86-10"></span>• [Not\\_flushed\\_delayed\\_rows](#page-86-10)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-87-1"></span>• [mecab\\_charset](#page-87-1)

The character set currently used by the MeCab full-text parser plugin. For related information, see Section 14.9.9, "MeCab Full-Text Parser Plugin".

<span id="page-87-2"></span>• [Ongoing\\_anonymous\\_transaction\\_count](#page-87-2)

Shows the number of ongoing transactions which have been marked as anonymous. This can be used to ensure that no further transactions are waiting to be processed.

<span id="page-87-3"></span>• [Ongoing\\_anonymous\\_gtid\\_violating\\_transaction\\_count](#page-87-3)

This status variable is only available in debug builds. Shows the number of ongoing transactions which use gtid\_next=ANONYMOUS and that violate GTID consistency.

<span id="page-87-4"></span>• [Ongoing\\_automatic\\_gtid\\_violating\\_transaction\\_count](#page-87-4)

This status variable is only available in debug builds. Shows the number of ongoing transactions which use gtid\_next=AUTOMATIC and that violate GTID consistency.

<span id="page-87-5"></span>• [Open\\_files](#page-87-5)

The number of files that are open. This count includes regular files opened by the server. It does not include other types of files such as sockets or pipes. Also, the count does not include files that storage engines open using their own internal functions rather than asking the server level to do so.

<span id="page-87-6"></span>• [Open\\_streams](#page-87-6)

The number of streams that are open (used mainly for logging).

<span id="page-87-7"></span>• [Open\\_table\\_definitions](#page-87-7)

The number of cached table definitions.

<span id="page-87-8"></span>• [Open\\_tables](#page-87-8)

The number of tables that are open.

<span id="page-87-9"></span>• [Opened\\_files](#page-87-9)

The number of files that have been opened with my\_open() (a mysys library function). Parts of the server that open files without using this function do not increment the count.

<span id="page-87-10"></span>• [Opened\\_table\\_definitions](#page-87-10)

The number of table definitions that have been cached.

<span id="page-87-0"></span>• [Opened\\_tables](#page-87-0)

The number of tables that have been opened. If [Opened\\_tables](#page-87-0) is big, your [table\\_open\\_cache](#page-20-0) value is probably too small.

• Performance\_schema\_xxx

Performance Schema status variables are listed in Section 29.16, "Performance Schema Status Variables". These variables provide information about instrumentation that could not be loaded or created due to memory constraints.

<span id="page-87-11"></span>• [Prepared\\_stmt\\_count](#page-87-11)

The current number of prepared statements. (The maximum number of statements is given by the max\_prepared\_stmt\_count system variable.)

<span id="page-87-12"></span>• [Queries](#page-87-12)

The number of statements executed by the server. This variable includes statements executed within stored programs, unlike the [Questions](#page-88-0) variable. It does not count COM\_PING or COM\_STATISTICS commands.

The discussion at the beginning of this section indicates how to relate this statement-counting status variable to other such variables.

<span id="page-88-0"></span>• [Questions](#page-88-0)

The number of statements executed by the server. This includes only statements sent to the server by clients and not statements executed within stored programs, unlike the [Queries](#page-87-12) variable. This variable does not count COM\_PING, COM\_STATISTICS, COM\_STMT\_PREPARE, COM\_STMT\_CLOSE, or COM\_STMT\_RESET commands.

The discussion at the beginning of this section indicates how to relate this statement-counting status variable to other such variables.

<span id="page-88-1"></span>• [Replica\\_open\\_temp\\_tables](#page-88-1)

From MySQL 8.0.26, use [Replica\\_open\\_temp\\_tables](#page-88-1) in place of [Slave\\_open\\_temp\\_tables](#page-94-2), which is deprecated from that release. In releases before MySQL 8.0.26, use [Slave\\_open\\_temp\\_tables](#page-94-2).

[Replica\\_open\\_temp\\_tables](#page-88-1) shows the number of temporary tables that the replication SQL thread currently has open. If the value is greater than zero, it is not safe to shut down the replica; see Section 19.5.1.31, "Replication and Temporary Tables". This variable reports the total count of open temporary tables for all replication channels.

<span id="page-88-2"></span>• [Replica\\_rows\\_last\\_search\\_algorithm\\_used](#page-88-2)

From MySQL 8.0.26, use [Replica\\_rows\\_last\\_search\\_algorithm\\_used](#page-88-2) in place of [Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-94-3), which is deprecated from that release. In releases before MySQL 8.0.26, use [Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-94-3).

[Replica\\_rows\\_last\\_search\\_algorithm\\_used](#page-88-2) shows the search algorithm that was most recently used by this replica to locate rows for row-based replication. The result shows whether the replica used indexes, a table scan, or hashing as the search algorithm for the last transaction executed on any channel.

The method used depends on the setting for the slave\_rows\_search\_algorithms system variable (which is now deprecated), and the keys that are available on the relevant table.

This variable is available only for debug builds of MySQL.

<span id="page-88-3"></span>• [Resource\\_group\\_supported](#page-88-3)

Indicates whether the resource group feature is supported.

On some platforms or MySQL server configurations, resource groups are unavailable or have limitations. In particular, Linux systems might require a manual step for some installation methods. For details, see [Resource Group Restrictions.](#page-134-0)

<span id="page-88-4"></span>• [Rpl\\_semi\\_sync\\_master\\_clients](#page-88-4)

The number of semisynchronous replicas.

[Rpl\\_semi\\_sync\\_master\\_clients](#page-88-4) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_clients](#page-91-0) is available instead.

<span id="page-89-0"></span>• [Rpl\\_semi\\_sync\\_master\\_net\\_avg\\_wait\\_time](#page-89-0)

The average time in microseconds the source waited for a replica reply. This variable is always 0, and is deprecated; expect it to be removed in a future version.

[Rpl\\_semi\\_sync\\_master\\_net\\_avg\\_wait\\_time](#page-89-0) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_net\\_avg\\_wait\\_time](#page-91-1) is available instead.

<span id="page-89-1"></span>• [Rpl\\_semi\\_sync\\_master\\_net\\_wait\\_time](#page-89-1)

The total time in microseconds the source waited for replica replies. This variable is always 0, and is deprecated; expect it to be removed in a future version.

[Rpl\\_semi\\_sync\\_master\\_net\\_wait\\_time](#page-89-1) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_net\\_wait\\_time](#page-91-2) is available instead.

<span id="page-89-2"></span>• [Rpl\\_semi\\_sync\\_master\\_net\\_waits](#page-89-2)

The total number of times the source waited for replica replies.

[Rpl\\_semi\\_sync\\_master\\_net\\_waits](#page-89-2) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_net\\_waits](#page-91-3) is available instead.

<span id="page-89-3"></span>• [Rpl\\_semi\\_sync\\_master\\_no\\_times](#page-89-3)

The number of times the source turned off semisynchronous replication.

[Rpl\\_semi\\_sync\\_master\\_no\\_times](#page-89-3) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_no\\_times](#page-91-4) is available instead.

<span id="page-89-4"></span>• [Rpl\\_semi\\_sync\\_master\\_no\\_tx](#page-89-4)

The number of commits that were not acknowledged successfully by a replica.

[Rpl\\_semi\\_sync\\_master\\_no\\_tx](#page-89-4) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_no\\_tx](#page-91-5) is available instead.

<span id="page-89-5"></span>• [Rpl\\_semi\\_sync\\_master\\_status](#page-89-5)

Whether semisynchronous replication currently is operational on the source. The value is ON if the plugin has been enabled and a commit acknowledgment has occurred. It is OFF if the plugin is not enabled or the source has fallen back to asynchronous replication due to commit acknowledgment timeout.

[Rpl\\_semi\\_sync\\_master\\_status](#page-89-5) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_status](#page-91-6) is available instead.

<span id="page-89-6"></span>• [Rpl\\_semi\\_sync\\_master\\_timefunc\\_failures](#page-89-6)

The number of times the source failed when calling time functions such as gettimeofday().

[Rpl\\_semi\\_sync\\_master\\_timefunc\\_failures](#page-89-6) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_timefunc\\_failures](#page-92-0) is available instead.

<span id="page-90-0"></span>• [Rpl\\_semi\\_sync\\_master\\_tx\\_avg\\_wait\\_time](#page-90-0)

The average time in microseconds the source waited for each transaction.

[Rpl\\_semi\\_sync\\_master\\_tx\\_avg\\_wait\\_time](#page-90-0) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_tx\\_avg\\_wait\\_time](#page-92-1) is available instead.

<span id="page-90-1"></span>• [Rpl\\_semi\\_sync\\_master\\_tx\\_wait\\_time](#page-90-1)

The total time in microseconds the source waited for transactions.

[Rpl\\_semi\\_sync\\_master\\_tx\\_wait\\_time](#page-90-1) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_tx\\_wait\\_time](#page-92-2) is available instead.

<span id="page-90-2"></span>• [Rpl\\_semi\\_sync\\_master\\_tx\\_waits](#page-90-2)

The total number of times the source waited for transactions.

[Rpl\\_semi\\_sync\\_master\\_tx\\_waits](#page-90-2) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_tx\\_waits](#page-92-3) is available instead.

<span id="page-90-3"></span>• [Rpl\\_semi\\_sync\\_master\\_wait\\_pos\\_backtraverse](#page-90-3)

The total number of times the source waited for an event with binary coordinates lower than events waited for previously. This can occur when the order in which transactions start waiting for a reply is different from the order in which their binary log events are written.

[Rpl\\_semi\\_sync\\_master\\_wait\\_pos\\_backtraverse](#page-90-3) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_wait\\_pos\\_backtraverse](#page-92-4) is available instead.

<span id="page-90-4"></span>• [Rpl\\_semi\\_sync\\_master\\_wait\\_sessions](#page-90-4)

The number of sessions currently waiting for replica replies.

[Rpl\\_semi\\_sync\\_master\\_wait\\_sessions](#page-90-4) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_wait\\_sessions](#page-92-5) is available instead.

<span id="page-90-5"></span>• [Rpl\\_semi\\_sync\\_master\\_yes\\_tx](#page-90-5)

The number of commits that were acknowledged successfully by a replica.

[Rpl\\_semi\\_sync\\_master\\_yes\\_tx](#page-90-5) is available when the rpl\_semi\_sync\_master (semisync\_master.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_source plugin (semisync\_source.so library) was installed, [Rpl\\_semi\\_sync\\_source\\_yes\\_tx](#page-93-0) is available instead.

<span id="page-91-0"></span>• [Rpl\\_semi\\_sync\\_source\\_clients](#page-91-0)

The number of semisynchronous replicas.

[Rpl\\_semi\\_sync\\_source\\_clients](#page-91-0) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_clients](#page-88-4) is available instead.

<span id="page-91-1"></span>• [Rpl\\_semi\\_sync\\_source\\_net\\_avg\\_wait\\_time](#page-91-1)

The average time in microseconds the source waited for a replica reply. This variable is always 0, and is deprecated; expect it to be removed in a future version.

[Rpl\\_semi\\_sync\\_source\\_net\\_avg\\_wait\\_time](#page-91-1) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_net\\_avg\\_wait\\_time](#page-89-0) is available instead.

<span id="page-91-2"></span>• [Rpl\\_semi\\_sync\\_source\\_net\\_wait\\_time](#page-91-2)

The total time in microseconds the source waited for replica replies. This variable is always 0, and is deprecated; expect it to be removed in a future version.

[Rpl\\_semi\\_sync\\_source\\_net\\_wait\\_time](#page-91-2) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_net\\_wait\\_time](#page-89-1) is available instead.

<span id="page-91-3"></span>• [Rpl\\_semi\\_sync\\_source\\_net\\_waits](#page-91-3)

The total number of times the source waited for replica replies.

[Rpl\\_semi\\_sync\\_source\\_net\\_waits](#page-91-3) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_net\\_waits](#page-89-2) is available instead.

<span id="page-91-4"></span>• [Rpl\\_semi\\_sync\\_source\\_no\\_times](#page-91-4)

The number of times the source turned off semisynchronous replication.

[Rpl\\_semi\\_sync\\_source\\_no\\_times](#page-91-4) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_no\\_times](#page-89-3) is available instead.

<span id="page-91-5"></span>• [Rpl\\_semi\\_sync\\_source\\_no\\_tx](#page-91-5)

The number of commits that were not acknowledged successfully by a replica.

[Rpl\\_semi\\_sync\\_source\\_no\\_tx](#page-91-5) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_no\\_tx](#page-89-4) is available instead.

<span id="page-91-6"></span>• [Rpl\\_semi\\_sync\\_source\\_status](#page-91-6)

Whether semisynchronous replication currently is operational on the source. The value is ON if the plugin has been enabled and a commit acknowledgment has occurred. It is OFF if the plugin is not enabled or the source has fallen back to asynchronous replication due to commit acknowledgment timeout.

[Rpl\\_semi\\_sync\\_source\\_status](#page-91-6) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_status](#page-89-5) is available instead.

<span id="page-92-0"></span>• [Rpl\\_semi\\_sync\\_source\\_timefunc\\_failures](#page-92-0)

The number of times the source failed when calling time functions such as gettimeofday().

[Rpl\\_semi\\_sync\\_source\\_timefunc\\_failures](#page-92-0) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_timefunc\\_failures](#page-89-6) is available instead.

<span id="page-92-1"></span>• [Rpl\\_semi\\_sync\\_source\\_tx\\_avg\\_wait\\_time](#page-92-1)

The average time in microseconds the source waited for each transaction.

[Rpl\\_semi\\_sync\\_source\\_tx\\_avg\\_wait\\_time](#page-92-1) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_tx\\_avg\\_wait\\_time](#page-90-0) is available instead.

<span id="page-92-2"></span>• [Rpl\\_semi\\_sync\\_source\\_tx\\_wait\\_time](#page-92-2)

The total time in microseconds the source waited for transactions.

[Rpl\\_semi\\_sync\\_source\\_tx\\_wait\\_time](#page-92-2) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_tx\\_wait\\_time](#page-90-1) is available instead.

<span id="page-92-3"></span>• [Rpl\\_semi\\_sync\\_source\\_tx\\_waits](#page-92-3)

The total number of times the source waited for transactions.

[Rpl\\_semi\\_sync\\_source\\_tx\\_waits](#page-92-3) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_tx\\_waits](#page-90-2) is available instead.

<span id="page-92-4"></span>• [Rpl\\_semi\\_sync\\_source\\_wait\\_pos\\_backtraverse](#page-92-4)

The total number of times the source waited for an event with binary coordinates lower than events waited for previously. This can occur when the order in which transactions start waiting for a reply is different from the order in which their binary log events are written.

[Rpl\\_semi\\_sync\\_source\\_wait\\_pos\\_backtraverse](#page-92-4) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_wait\\_pos\\_backtraverse](#page-90-3) is available instead.

<span id="page-92-5"></span>• [Rpl\\_semi\\_sync\\_source\\_wait\\_sessions](#page-92-5)

The number of sessions currently waiting for replica replies.

[Rpl\\_semi\\_sync\\_source\\_wait\\_sessions](#page-92-5) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_wait\\_sessions](#page-90-4) is available instead.

<span id="page-93-0"></span>• [Rpl\\_semi\\_sync\\_source\\_yes\\_tx](#page-93-0)

The number of commits that were acknowledged successfully by a replica.

[Rpl\\_semi\\_sync\\_source\\_yes\\_tx](#page-93-0) is available when the rpl\_semi\_sync\_source (semisync\_source.so library) plugin was installed on the source to set up semisynchronous replication. If the rpl\_semi\_sync\_master plugin (semisync\_master.so library) was installed, [Rpl\\_semi\\_sync\\_master\\_yes\\_tx](#page-90-5) is available instead.

<span id="page-93-1"></span>• [Rpl\\_semi\\_sync\\_replica\\_status](#page-93-1)

Shows whether semisynchronous replication is currently operational on the replica. This is ON if the plugin has been enabled and the replication I/O (receiver) thread is running, OFF otherwise.

[Rpl\\_semi\\_sync\\_replica\\_status](#page-93-1) is available when the rpl\_semi\_sync\_replica (semisync\_replica.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_slave plugin (semisync\_slave.so library) was installed, [Rpl\\_semi\\_sync\\_slave\\_status](#page-93-2) is available instead.

<span id="page-93-2"></span>• [Rpl\\_semi\\_sync\\_slave\\_status](#page-93-2)

Shows whether semisynchronous replication is currently operational on the replica. This is ON if the plugin has been enabled and the replication I/O (receiver) thread is running, OFF otherwise.

[Rpl\\_semi\\_sync\\_slave\\_status](#page-93-2) is available when the rpl\_semi\_sync\_slave (semisync\_slave.so library) plugin was installed on the replica to set up semisynchronous replication. If the rpl\_semi\_sync\_replica plugin (semisync\_replica.so library) was installed, [Rpl\\_semi\\_sync\\_replica\\_status](#page-93-1) is available instead.

<span id="page-93-3"></span>• [Rsa\\_public\\_key](#page-93-3)

The value of this variable is the public key used by the sha256\_password authentication plugin for RSA key pair-based password exchange. The value is nonempty only if the server successfully initializes the private and public keys in the files named by the sha256\_password\_private\_key\_path and sha256\_password\_public\_key\_path system variables. The value of [Rsa\\_public\\_key](#page-93-3) comes from the latter file.

For information about sha256\_password, see Section 8.4.1.3, "SHA-256 Pluggable Authentication".

• [Secondary\\_engine\\_execution\\_count](https://dev.mysql.com/doc/heatwave/en/heatwave-status-variables.md#statvar_Secondary_engine_execution_count)

For use with MySQL HeatWave only. See [Status Variables](https://dev.mysql.com/doc/heatwave/en/heatwave-status-variables.md), for more information.

<span id="page-93-4"></span>• [Select\\_full\\_join](#page-93-4)

The number of joins that perform table scans because they do not use indexes. If this value is not 0, you should carefully check the indexes of your tables.

<span id="page-93-5"></span>• [Select\\_full\\_range\\_join](#page-93-5)

The number of joins that used a range search on a reference table.

<span id="page-93-6"></span>• [Select\\_range](#page-93-6)

The number of joins that used ranges on the first table. This is normally not a critical issue even if the value is quite large.

<span id="page-93-7"></span>• [Select\\_range\\_check](#page-93-7)

The number of joins without keys that check for key usage after each row. If this is not 0, you should carefully check the indexes of your tables.

<span id="page-94-4"></span>• [Select\\_scan](#page-94-4)

The number of joins that did a full scan of the first table.

<span id="page-94-2"></span>• [Slave\\_open\\_temp\\_tables](#page-94-2)

From MySQL 8.0.26, [Slave\\_open\\_temp\\_tables](#page-94-2) is deprecated and the alias [Replica\\_open\\_temp\\_tables](#page-88-1) should be used instead. In releases before MySQL 8.0.26, use [Slave\\_open\\_temp\\_tables](#page-94-2).

[Slave\\_open\\_temp\\_tables](#page-94-2) shows the number of temporary tables that the replication SQL thread currently has open. If the value is greater than zero, it is not safe to shut down the replica; see Section 19.5.1.31, "Replication and Temporary Tables". This variable reports the total count of open temporary tables for all replication channels.

<span id="page-94-3"></span>• [Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-94-3)

From MySQL 8.0.26, [Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-94-3) is deprecated and the alias [Replica\\_rows\\_last\\_search\\_algorithm\\_used](#page-88-2) should be used instead. In releases before MySQL 8.0.26, use [Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-94-3).

[Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-94-3) shows the search algorithm that was most recently used by this replica to locate rows for row-based replication. The result shows whether the replica used indexes, a table scan, or hashing as the search algorithm for the last transaction executed on any channel.

The method used depends on the setting for the slave\_rows\_search\_algorithms system variable, and the keys that are available on the relevant table.

This variable is available only for debug builds of MySQL.

<span id="page-94-0"></span>• [Slow\\_launch\\_threads](#page-94-0)

The number of threads that have taken more than [slow\\_launch\\_time](#page-2-0) seconds to create.

<span id="page-94-5"></span>• [Slow\\_queries](#page-94-5)

The number of queries that have taken more than long\_query\_time seconds. This counter increments regardless of whether the slow query log is enabled. For information about that log, see [Section 7.4.5, "The Slow Query Log".](#page-189-0)

<span id="page-94-1"></span>• [Sort\\_merge\\_passes](#page-94-1)

The number of merge passes that the sort algorithm has had to do. If this value is large, you should consider increasing the value of the [sort\\_buffer\\_size](#page-3-1) system variable.

<span id="page-94-6"></span>• [Sort\\_range](#page-94-6)

The number of sorts that were done using ranges.

<span id="page-94-7"></span>• [Sort\\_rows](#page-94-7)

The number of sorted rows.

<span id="page-94-8"></span>• [Sort\\_scan](#page-94-8)

The number of sorts that were done by scanning the table.

<span id="page-94-9"></span>• [Ssl\\_accept\\_renegotiates](#page-94-9)

The number of negotiates needed to establish the connection.

<span id="page-94-10"></span>• [Ssl\\_accepts](#page-94-10)

The number of accepted SSL connections.

<span id="page-95-0"></span>• [Ssl\\_callback\\_cache\\_hits](#page-95-0)

The number of callback cache hits.

<span id="page-95-1"></span>• [Ssl\\_cipher](#page-95-1)

The current encryption cipher (empty for unencrypted connections).

<span id="page-95-2"></span>• [Ssl\\_cipher\\_list](#page-95-2)

The list of possible SSL ciphers (empty for non-SSL connections). If MySQL supports TLSv1.3, the value includes the possible TLSv1.3 ciphersuites. See Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-95-3"></span>• [Ssl\\_client\\_connects](#page-95-3)

The number of SSL connection attempts to an SSL-enabled replication source server.

<span id="page-95-4"></span>• [Ssl\\_connect\\_renegotiates](#page-95-4)

The number of negotiates needed to establish the connection to an SSL-enabled replication source server.

<span id="page-95-5"></span>• [Ssl\\_ctx\\_verify\\_depth](#page-95-5)

The SSL context verification depth (how many certificates in the chain are tested).

<span id="page-95-6"></span>• [Ssl\\_ctx\\_verify\\_mode](#page-95-6)

The SSL context verification mode.

<span id="page-95-7"></span>• [Ssl\\_default\\_timeout](#page-95-7)

The default SSL timeout.

<span id="page-95-8"></span>• [Ssl\\_finished\\_accepts](#page-95-8)

The number of successful SSL connections to the server.

<span id="page-95-9"></span>• [Ssl\\_finished\\_connects](#page-95-9)

The number of successful replica connections to an SSL-enabled replication source server.

<span id="page-95-10"></span>• [Ssl\\_server\\_not\\_after](#page-95-10)

The last date for which the SSL certificate is valid. To check SSL certificate expiration information, use this statement:

```
mysql> SHOW STATUS LIKE 'Ssl_server_not%';
+-----------------------+--------------------------+
| Variable_name | Value |
+-----------------------+--------------------------+
| Ssl_server_not_after | Apr 28 14:16:39 2025 GMT |
| Ssl_server_not_before | May 1 14:16:39 2015 GMT |
+-----------------------+--------------------------+
```

<span id="page-95-11"></span>• [Ssl\\_server\\_not\\_before](#page-95-11)

The first date for which the SSL certificate is valid.

<span id="page-95-12"></span>• [Ssl\\_session\\_cache\\_hits](#page-95-12)

The number of SSL session cache hits.

<span id="page-96-2"></span>• [Ssl\\_session\\_cache\\_misses](#page-96-2)

The number of SSL session cache misses.

<span id="page-96-0"></span>• [Ssl\\_session\\_cache\\_mode](#page-96-0)

The SSL session cache mode. When the value of the [ssl\\_session\\_cache\\_mode](#page-13-1) server variable is ON, the value of the [Ssl\\_session\\_cache\\_mode](#page-96-0) status variable is SERVER.

<span id="page-96-3"></span>• [Ssl\\_session\\_cache\\_overflows](#page-96-3)

The number of SSL session cache overflows.

<span id="page-96-4"></span>• [Ssl\\_session\\_cache\\_size](#page-96-4)

The SSL session cache size.

<span id="page-96-1"></span>• [Ssl\\_session\\_cache\\_timeout](#page-96-1)

The timeout value in seconds of SSL sessions in the cache.

<span id="page-96-5"></span>• [Ssl\\_session\\_cache\\_timeouts](#page-96-5)

The number of SSL session cache timeouts.

<span id="page-96-6"></span>• [Ssl\\_sessions\\_reused](#page-96-6)

This is equal to 0 if TLS was not used in the current MySQL session, or if a TLS session has not been reused; otherwise it is equal to 1.

Ssl\_sessions\_reused has session scope.

<span id="page-96-7"></span>• [Ssl\\_used\\_session\\_cache\\_entries](#page-96-7)

How many SSL session cache entries were used.

<span id="page-96-8"></span>• [Ssl\\_verify\\_depth](#page-96-8)

The verification depth for replication SSL connections.

<span id="page-96-9"></span>• [Ssl\\_verify\\_mode](#page-96-9)

The verification mode used by the server for a connection that uses SSL. The value is a bitmask; bits are defined in the openssl/ssl.h header file:

```
# define SSL_VERIFY_NONE 0x00
# define SSL_VERIFY_PEER 0x01
# define SSL_VERIFY_FAIL_IF_NO_PEER_CERT 0x02
# define SSL_VERIFY_CLIENT_ONCE 0x04
```

SSL\_VERIFY\_PEER indicates that the server asks for a client certificate. If the client supplies one, the server performs verification and proceeds only if verification is successful. SSL\_VERIFY\_CLIENT\_ONCE indicates that a request for the client certificate is performed only in the initial handshake.

<span id="page-96-10"></span>• [Ssl\\_version](#page-96-10)

The SSL protocol version of the connection (for example, TLSv1). If the connection is not encrypted, the value is empty.

<span id="page-96-11"></span>• [Table\\_locks\\_immediate](#page-96-11)

The number of times that a request for a table lock could be granted immediately.

<span id="page-96-12"></span>• [Table\\_locks\\_waited](#page-96-12)

The number of times that a request for a table lock could not be granted immediately and a wait was needed. If this is high and you have performance problems, you should first optimize your queries, and then either split your table or tables or use replication.

<span id="page-97-1"></span>• [Table\\_open\\_cache\\_hits](#page-97-1)

The number of hits for open tables cache lookups.

<span id="page-97-2"></span>• [Table\\_open\\_cache\\_misses](#page-97-2)

The number of misses for open tables cache lookups.

<span id="page-97-3"></span>• [Table\\_open\\_cache\\_overflows](#page-97-3)

The number of overflows for the open tables cache. This is the number of times, after a table is opened or closed, a cache instance has an unused entry and the size of the instance is larger than [table\\_open\\_cache](#page-20-0) / [table\\_open\\_cache\\_instances](#page-20-1).

<span id="page-97-4"></span>• [Tc\\_log\\_max\\_pages\\_used](#page-97-4)

For the memory-mapped implementation of the log that is used by mysqld when it acts as the transaction coordinator for recovery of internal XA transactions, this variable indicates the largest number of pages used for the log since the server started. If the product of [Tc\\_log\\_max\\_pages\\_used](#page-97-4) and [Tc\\_log\\_page\\_size](#page-97-5) is always significantly less than the log size, the size is larger than necessary and can be reduced. (The size is set by the --log-tcsize option. This variable is unused: It is unneeded for binary log-based recovery, and the memorymapped recovery log method is not used unless the number of storage engines that are capable of two-phase commit and that support XA transactions is greater than one. (InnoDB is the only applicable engine.)

<span id="page-97-5"></span>• [Tc\\_log\\_page\\_size](#page-97-5)

The page size used for the memory-mapped implementation of the XA recovery log. The default value is determined using getpagesize(). This variable is unused for the same reasons as described for [Tc\\_log\\_max\\_pages\\_used](#page-97-4).

<span id="page-97-6"></span>• [Tc\\_log\\_page\\_waits](#page-97-6)

For the memory-mapped implementation of the recovery log, this variable increments each time the server was not able to commit a transaction and had to wait for a free page in the log. If this value is large, you might want to increase the log size (with the --log-tc-size option). For binary log-based recovery, this variable increments each time the binary log cannot be closed because there are two-phase commits in progress. (The close operation waits until all such transactions are finished.)

<span id="page-97-7"></span>• [Telemetry\\_traces\\_supported](#page-97-7)

Whether server telemetry traces is supported.

For more information, see the Server telemetry traces service section in the MySQL Source Code documentation.

<span id="page-97-8"></span>• [Threads\\_cached](#page-97-8)

The number of threads in the thread cache.

<span id="page-97-9"></span>• [Threads\\_connected](#page-97-9)

The number of currently open connections.

<span id="page-97-0"></span>• [Threads\\_created](#page-97-0)

The number of threads created to handle connections. If [Threads\\_created](#page-97-0) is big, you may want to increase the [thread\\_cache\\_size](#page-22-1) value. The cache miss rate can be calculated as [Threads\\_created](#page-97-0)/[Connections](#page-74-0).

<span id="page-98-1"></span>• [Threads\\_running](#page-98-1)

The number of threads that are not sleeping.

<span id="page-98-2"></span>• [Tls\\_library\\_version](#page-98-2)

The runtime version of the OpenSSL library that is in use for this MySQL instance.

This variable was added in MySQL 8.0.30.

<span id="page-98-3"></span>• [Uptime](#page-98-3)

The number of seconds that the server has been up.

• [Uptime\\_since\\_flush\\_status](#page-98-4)

The number of seconds since the most recent FLUSH STATUS statement.

## <span id="page-98-4"></span><span id="page-98-0"></span>**7.1.11 Server SQL Modes**

The MySQL server can operate in different SQL modes, and can apply these modes differently for different clients, depending on the value of the [sql\\_mode](#page-6-0) system variable. DBAs can set the global SQL mode to match site server operating requirements, and each application can set its session SQL mode to its own requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it easier to use MySQL in different environments and to use MySQL together with other database servers.

- [Setting the SQL Mode](#page-98-5)
- [The Most Important SQL Modes](#page-99-0)
- [Full List of SQL Modes](#page-100-0)
- [Combination SQL Modes](#page-105-0)
- [Strict SQL Mode](#page-105-1)
- [Comparison of the IGNORE Keyword and Strict SQL Mode](#page-107-0)

For answers to questions often asked about server SQL modes in MySQL, see Section A.3, "MySQL 8.0 FAQ: Server SQL Mode".

When working with InnoDB tables, consider also the innodb\_strict\_mode system variable. It enables additional error checks for InnoDB tables.

### <span id="page-98-5"></span>**Setting the SQL Mode**

The default SQL mode in MySQL 8.0 includes these modes: [ONLY\\_FULL\\_GROUP\\_BY](#page-103-0), [STRICT\\_TRANS\\_TABLES](#page-104-0), [NO\\_ZERO\\_IN\\_DATE](#page-103-1), [NO\\_ZERO\\_DATE](#page-103-2), [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1), and [NO\\_ENGINE\\_SUBSTITUTION](#page-101-0).

To set the SQL mode at server startup, use the --sql-mode="modes" option on the command line, or sql-mode="modes" in an option file such as my.cnf (Unix operating systems) or my.ini (Windows). modes is a list of different modes separated by commas. To clear the SQL mode explicitly, set it to an empty string using --sql-mode="" on the command line, or sql-mode="" in an option file.

![](_page_99_Picture_1.jpeg)

#### **Note**

MySQL installation programs may configure the SQL mode during the installation process.

If the SQL mode differs from the default or from what you expect, check for a setting in an option file that the server reads at startup.

To change the SQL mode at runtime, set the global or session [sql\\_mode](#page-6-0) system variable using a SET statement:

```
SET GLOBAL sql_mode = 'modes';
SET SESSION sql_mode = 'modes';
```

Setting the GLOBAL variable requires the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege) and affects the operation of all clients that connect from that time on. Setting the SESSION variable affects only the current client. Each client can change its session [sql\\_mode](#page-6-0) value at any time.

To determine the current global or session [sql\\_mode](#page-6-0) setting, select its value:

```
SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;
```

![](_page_99_Picture_10.jpeg)

#### **Important**

**SQL mode and user-defined partitioning.** Changing the server SQL mode after creating and inserting data into partitioned tables can cause major changes in the behavior of such tables, and could lead to loss or corruption of data. It is strongly recommended that you never change the SQL mode once you have created tables employing user-defined partitioning.

When replicating partitioned tables, differing SQL modes on the source and replica can also lead to problems. For best results, you should always use the same server SQL mode on the source and replica.

For more information, see Section 26.6, "Restrictions and Limitations on Partitioning".

### <span id="page-99-0"></span>**The Most Important SQL Modes**

The most important [sql\\_mode](#page-6-0) values are probably these:

• [ANSI](#page-105-2)

This mode changes syntax and behavior to conform more closely to standard SQL. It is one of the special [combination modes](#page-105-0) listed at the end of this section.

• [STRICT\\_TRANS\\_TABLES](#page-104-0)

If a value could not be inserted as given into a transactional table, abort the statement. For a nontransactional table, abort the statement if the value occurs in a single-row statement or the first row of a multiple-row statement. More details are given later in this section.

• [TRADITIONAL](#page-105-3)

Make MySQL behave like a "traditional" SQL database system. A simple description of this mode is "give an error instead of a warning" when inserting an incorrect value into a column. It is one of the special [combination modes](#page-105-0) listed at the end of this section.

![](_page_99_Picture_23.jpeg)

#### **Note**

With [TRADITIONAL](#page-105-3) mode enabled, an INSERT or UPDATE aborts as soon as an error occurs. If you are using a nontransactional storage engine, this may

not be what you want because data changes made prior to the error may not be rolled back, resulting in a "partially done" update.

When this manual refers to "strict mode," it means a mode with either or both [STRICT\\_TRANS\\_TABLES](#page-104-0) or [STRICT\\_ALL\\_TABLES](#page-104-1) enabled.

### <span id="page-100-2"></span><span id="page-100-0"></span>**Full List of SQL Modes**

The following list describes all supported SQL modes:

• [ALLOW\\_INVALID\\_DATES](#page-100-2)

Do not perform full checking of dates. Check only that the month is in the range from 1 to 12 and the day is in the range from 1 to 31. This may be useful for Web applications that obtain year, month, and day in three different fields and store exactly what the user inserted, without date validation. This mode applies to DATE and DATETIME columns. It does not apply to TIMESTAMP columns, which always require a valid date.

With [ALLOW\\_INVALID\\_DATES](#page-100-2) disabled, the server requires that month and day values be legal, and not merely in the range 1 to 12 and 1 to 31, respectively. With strict mode disabled, invalid dates such as '2004-04-31' are converted to '0000-00-00' and a warning is generated. With strict mode enabled, invalid dates generate an error. To permit such dates, enable [ALLOW\\_INVALID\\_DATES](#page-100-2).

<span id="page-100-3"></span>• [ANSI\\_QUOTES](#page-100-3)

Treat " as an identifier quote character (like the ` quote character) and not as a string quote character. You can still use ` to quote identifiers with this mode enabled. With [ANSI\\_QUOTES](#page-100-3) enabled, you cannot use double quotation marks to quote literal strings because they are interpreted as identifiers.

<span id="page-100-1"></span>• [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1)

The [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1) mode affects handling of division by zero, which includes MOD(N,0). For data-change operations (INSERT, UPDATE), its effect also depends on whether strict SQL mode is enabled.

- If this mode is not enabled, division by zero inserts NULL and produces no warning.
- If this mode is enabled, division by zero inserts NULL and produces a warning.
- If this mode and strict mode are enabled, division by zero produces an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, division by zero inserts NULL and produces a warning.

For SELECT, division by zero returns NULL. Enabling [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1) causes a warning to be produced as well, regardless of whether strict mode is enabled.

[ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1) is deprecated. [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1) is not part of strict mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs if [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1) is enabled without also enabling strict mode or vice versa.

Because [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1) is deprecated, you should expect it to be removed in a future MySQL release as a separate mode name and its effect included in the effects of strict SQL mode.

<span id="page-100-4"></span>• [HIGH\\_NOT\\_PRECEDENCE](#page-100-4)

The precedence of the NOT operator is such that expressions such as NOT a BETWEEN b AND c are parsed as NOT (a BETWEEN b AND c). In some older versions of MySQL, the expression was parsed as (NOT a) BETWEEN b AND c. The old higher-precedence behavior can be obtained by enabling the [HIGH\\_NOT\\_PRECEDENCE](#page-100-4) SQL mode.

```
mysql> SET sql_mode = '';
mysql> SELECT NOT 1 BETWEEN -5 AND 5;
 -> 0
mysql> SET sql_mode = 'HIGH_NOT_PRECEDENCE';
mysql> SELECT NOT 1 BETWEEN -5 AND 5;
 -> 1
```

<span id="page-101-1"></span>• [IGNORE\\_SPACE](#page-101-1)

Permit spaces between a function name and the ( character. This causes built-in function names to be treated as reserved words. As a result, identifiers that are the same as function names must be quoted as described in Section 11.2, "Schema Object Names". For example, because there is a COUNT() function, the use of count as a table name in the following statement causes an error:

```
mysql> CREATE TABLE count (i INT);
ERROR 1064 (42000): You have an error in your SQL syntax
```

The table name should be quoted:

```
mysql> CREATE TABLE `count` (i INT);
Query OK, 0 rows affected (0.00 sec)
```

The [IGNORE\\_SPACE](#page-101-1) SQL mode applies to built-in functions, not to loadable functions or stored functions. It is always permissible to have spaces after a loadable function or stored function name, regardless of whether [IGNORE\\_SPACE](#page-101-1) is enabled.

For further discussion of [IGNORE\\_SPACE](#page-101-1), see Section 11.2.5, "Function Name Parsing and Resolution".

<span id="page-101-2"></span>• [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-101-2)

[NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-101-2) affects handling of AUTO\_INCREMENT columns. Normally, you generate the next sequence number for the column by inserting either NULL or 0 into it. [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-101-2) suppresses this behavior for 0 so that only NULL generates the next sequence number.

This mode can be useful if 0 has been stored in a table's AUTO\_INCREMENT column. (Storing 0 is not a recommended practice, by the way.) For example, if you dump the table with mysqldump and then reload it, MySQL normally generates new sequence numbers when it encounters the 0 values, resulting in a table with contents different from the one that was dumped. Enabling [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-101-2) before reloading the dump file solves this problem. For this reason, mysqldump automatically includes in its output a statement that enables [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-101-2).

<span id="page-101-3"></span>• [NO\\_BACKSLASH\\_ESCAPES](#page-101-3)

Enabling this mode disables the use of the backslash character (\) as an escape character within strings and identifiers. With this mode enabled, backslash becomes an ordinary character like any other, and the default escape sequence for LIKE expressions is changed so that no escape character is used.

<span id="page-101-4"></span>• [NO\\_DIR\\_IN\\_CREATE](#page-101-4)

When creating a table, ignore all INDEX DIRECTORY and DATA DIRECTORY directives. This option is useful on replica servers.

<span id="page-101-0"></span>• [NO\\_ENGINE\\_SUBSTITUTION](#page-101-0)

Control automatic substitution of the default storage engine when a statement such as CREATE TABLE or ALTER TABLE specifies a storage engine that is disabled or not compiled in.

By default, [NO\\_ENGINE\\_SUBSTITUTION](#page-101-0) is enabled.

Because storage engines can be pluggable at runtime, unavailable engines are treated the same way:

With [NO\\_ENGINE\\_SUBSTITUTION](#page-101-0) disabled, for CREATE TABLE the default engine is used and a warning occurs if the desired engine is unavailable. For ALTER TABLE, a warning occurs and the table is not altered.

With [NO\\_ENGINE\\_SUBSTITUTION](#page-101-0) enabled, an error occurs and the table is not created or altered if the desired engine is unavailable.

<span id="page-102-0"></span>• [NO\\_UNSIGNED\\_SUBTRACTION](#page-102-0)

Subtraction between integer values, where one is of type UNSIGNED, produces an unsigned result by default. If the result would otherwise have been negative, an error results:

```
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
ERROR 1690 (22003): BIGINT UNSIGNED value is out of range in '(cast(0 as unsigned) - 1)'
```

If the [NO\\_UNSIGNED\\_SUBTRACTION](#page-102-0) SQL mode is enabled, the result is negative:

```
mysql> SET sql_mode = 'NO_UNSIGNED_SUBTRACTION';
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
+-------------------------+
| CAST(0 AS UNSIGNED) - 1 |
+-------------------------+
| -1 |
+-------------------------+
```

If the result of such an operation is used to update an UNSIGNED integer column, the result is clipped to the maximum value for the column type, or clipped to 0 if [NO\\_UNSIGNED\\_SUBTRACTION](#page-102-0) is enabled. With strict SQL mode enabled, an error occurs and the column remains unchanged.

When [NO\\_UNSIGNED\\_SUBTRACTION](#page-102-0) is enabled, the subtraction result is signed, even if any operand is unsigned. For example, compare the type of column c2 in table t1 with that of column c2 in table t2:

```
mysql> SET sql_mode='';
mysql> CREATE TABLE test (c1 BIGINT UNSIGNED NOT NULL);
mysql> CREATE TABLE t1 SELECT c1 - 1 AS c2 FROM test;
mysql> DESCRIBE t1;
+-------+---------------------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+---------------------+------+-----+---------+-------+
| c2 | bigint(21) unsigned | NO | | 0 | |
+-------+---------------------+------+-----+---------+-------+
mysql> SET sql_mode='NO_UNSIGNED_SUBTRACTION';
mysql> CREATE TABLE t2 SELECT c1 - 1 AS c2 FROM test;
mysql> DESCRIBE t2;
+-------+------------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| c2 | bigint(21) | NO | | 0 | |
+-------+------------+------+-----+---------+-------+
```

This means that BIGINT UNSIGNED is not 100% usable in all contexts. See Section 14.10, "Cast Functions and Operators".

### <span id="page-103-2"></span>• [NO\\_ZERO\\_DATE](#page-103-2)

The [NO\\_ZERO\\_DATE](#page-103-2) mode affects whether the server permits '0000-00-00' as a valid date. Its effect also depends on whether strict SQL mode is enabled.

- If this mode is not enabled, '0000-00-00' is permitted and inserts produce no warning.
- If this mode is enabled, '0000-00-00' is permitted and inserts produce a warning.
- If this mode and strict mode are enabled, '0000-00-00' is not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, '0000-00-00' is permitted and inserts produce a warning.

[NO\\_ZERO\\_DATE](#page-103-2) is deprecated. [NO\\_ZERO\\_DATE](#page-103-2) is not part of strict mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs if [NO\\_ZERO\\_DATE](#page-103-2) is enabled without also enabling strict mode or vice versa.

Because [NO\\_ZERO\\_DATE](#page-103-2) is deprecated, you should expect it to be removed in a future MySQL release as a separate mode name and its effect included in the effects of strict SQL mode.

<span id="page-103-1"></span>• [NO\\_ZERO\\_IN\\_DATE](#page-103-1)

The [NO\\_ZERO\\_IN\\_DATE](#page-103-1) mode affects whether the server permits dates in which the year part is nonzero but the month or day part is 0. (This mode affects dates such as '2010-00-01' or '2010-01-00', but not '0000-00-00'. To control whether the server permits '0000-00-00', use the [NO\\_ZERO\\_DATE](#page-103-2) mode.) The effect of [NO\\_ZERO\\_IN\\_DATE](#page-103-1) also depends on whether strict SQL mode is enabled.

- If this mode is not enabled, dates with zero parts are permitted and inserts produce no warning.
- If this mode is enabled, dates with zero parts are inserted as '0000-00-00' and produce a warning.
- If this mode and strict mode are enabled, dates with zero parts are not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, dates with zero parts are inserted as '0000-00-00' and produce a warning.

[NO\\_ZERO\\_IN\\_DATE](#page-103-1) is deprecated. [NO\\_ZERO\\_IN\\_DATE](#page-103-1) is not part of strict mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs if [NO\\_ZERO\\_IN\\_DATE](#page-103-1) is enabled without also enabling strict mode or vice versa.

Because [NO\\_ZERO\\_IN\\_DATE](#page-103-1) is deprecated, you should expect it to be removed in a future MySQL release as a separate mode name and its effect included in the effects of strict SQL mode.

<span id="page-103-0"></span>• [ONLY\\_FULL\\_GROUP\\_BY](#page-103-0)

Reject queries for which the select list, HAVING condition, or ORDER BY list refer to nonaggregated columns that are neither named in the GROUP BY clause nor are functionally dependent on (uniquely determined by) GROUP BY columns.

A MySQL extension to standard SQL permits references in the HAVING clause to aliased expressions in the select list. The HAVING clause can refer to aliases regardless of whether [ONLY\\_FULL\\_GROUP\\_BY](#page-103-0) is enabled.

For additional discussion and examples, see Section 14.19.3, "MySQL Handling of GROUP BY".

<span id="page-103-3"></span>• [PAD\\_CHAR\\_TO\\_FULL\\_LENGTH](#page-103-3)

By default, trailing spaces are trimmed from CHAR column values on retrieval. If [PAD\\_CHAR\\_TO\\_FULL\\_LENGTH](#page-103-3) is enabled, trimming does not occur and retrieved CHAR values are padded to their full length. This mode does not apply to VARCHAR columns, for which trailing spaces are retained on retrieval.

![](_page_104_Picture_2.jpeg)

#### **Note**

As of MySQL 8.0.13, [PAD\\_CHAR\\_TO\\_FULL\\_LENGTH](#page-103-3) is deprecated. Expect it to be removed in a future version of MySQL.

```
mysql> CREATE TABLE t1 (c1 CHAR(10));
Query OK, 0 rows affected (0.37 sec)
mysql> INSERT INTO t1 (c1) VALUES('xy');
Query OK, 1 row affected (0.01 sec)
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT c1, CHAR_LENGTH(c1) FROM t1;
+------+-----------------+
| c1 | CHAR_LENGTH(c1) |
+------+-----------------+
| xy | 2 |
+------+-----------------+
1 row in set (0.00 sec)
mysql> SET sql_mode = 'PAD_CHAR_TO_FULL_LENGTH';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT c1, CHAR_LENGTH(c1) FROM t1;
+------------+-----------------+
| c1 | CHAR_LENGTH(c1) |
+------------+-----------------+
| xy | 10 |
+------------+-----------------+
1 row in set (0.00 sec)
```

<span id="page-104-2"></span>• [PIPES\\_AS\\_CONCAT](#page-104-2)

Treat || as a string concatenation operator (same as CONCAT()) rather than as a synonym for OR.

<span id="page-104-3"></span>• [REAL\\_AS\\_FLOAT](#page-104-3)

Treat REAL as a synonym for FLOAT. By default, MySQL treats REAL as a synonym for DOUBLE.

<span id="page-104-1"></span>• [STRICT\\_ALL\\_TABLES](#page-104-1)

Enable strict SQL mode for all storage engines. Invalid data values are rejected. For details, see [Strict SQL Mode](#page-105-1).

<span id="page-104-0"></span>• [STRICT\\_TRANS\\_TABLES](#page-104-0)

Enable strict SQL mode for transactional storage engines, and when possible for nontransactional storage engines. For details, see [Strict SQL Mode](#page-105-1).

<span id="page-104-4"></span>• [TIME\\_TRUNCATE\\_FRACTIONAL](#page-104-4)

Control whether rounding or truncation occurs when inserting a TIME, DATE, or TIMESTAMP value with a fractional seconds part into a column having the same type but fewer fractional digits. The default behavior is to use rounding. If this mode is enabled, truncation occurs instead. The following sequence of statements illustrates the difference:

```
CREATE TABLE t (id INT, tval TIME(1));
SET sql_mode='';
INSERT INTO t (id, tval) VALUES(1, 1.55);
SET sql_mode='TIME_TRUNCATE_FRACTIONAL';
INSERT INTO t (id, tval) VALUES(2, 1.55);
```

The resulting table contents look like this, where the first value has been subject to rounding and the second to truncation:

```
mysql> SELECT id, tval FROM t ORDER BY id;
+------+------------+
| id | tval |
+------+------------+
| 1 | 00:00:01.6 |
| 2 | 00:00:01.5 |
+------+------------+
```

See also Section 13.2.6, "Fractional Seconds in Time Values".

### <span id="page-105-0"></span>**Combination SQL Modes**

The following special modes are provided as shorthand for combinations of mode values from the preceding list.

<span id="page-105-2"></span>• [ANSI](#page-105-2)

```
Equivalent to REAL_AS_FLOAT, PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, and
ONLY_FULL_GROUP_BY.
```

[ANSI](#page-105-2) mode also causes the server to return an error for queries where a set function S with an outer reference S(outer\_ref) cannot be aggregated in the outer query against which the outer reference has been resolved. This is such a query:

```
SELECT * FROM t1 WHERE t1.a IN (SELECT MAX(t1.b) FROM t2 WHERE ...);
```

Here, MAX(t1.b) cannot aggregated in the outer query because it appears in the WHERE clause of that query. Standard SQL requires an error in this situation. If [ANSI](#page-105-2) mode is not enabled, the server treats S(outer\_ref) in such queries the same way that it would interpret S(const).

See Section 1.6, "MySQL Standards Compliance".

<span id="page-105-3"></span>• [TRADITIONAL](#page-105-3)

```
TRADITIONAL is equivalent to STRICT_TRANS_TABLES, STRICT_ALL_TABLES,
NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, and
NO_ENGINE_SUBSTITUTION.
```

### <span id="page-105-1"></span>**Strict SQL Mode**

Strict mode controls how MySQL handles invalid or missing values in data-change statements such as INSERT or UPDATE. A value can be invalid for several reasons. For example, it might have the wrong data type for the column, or it might be out of range. A value is missing when a new row to be inserted does not contain a value for a non-NULL column that has no explicit DEFAULT clause in its definition. (For a NULL column, NULL is inserted if the value is missing.) Strict mode also affects DDL statements such as CREATE TABLE.

If strict mode is not in effect, MySQL inserts adjusted values for invalid or missing values and produces warnings (see Section 15.7.7.42, "SHOW WARNINGS Statement"). In strict mode, you can produce this behavior by using INSERT IGNORE or UPDATE IGNORE.

For statements such as SELECT that do not change data, invalid values generate a warning in strict mode, not an error.

Strict mode produces an error for attempts to create a key that exceeds the maximum key length. When strict mode is not enabled, this results in a warning and truncation of the key to the maximum key length.

Strict mode does not affect whether foreign key constraints are checked. foreign\_key\_checks can be used for that. (See Section 7.1.8, "Server System Variables".)

Strict SQL mode is in effect if either [STRICT\\_ALL\\_TABLES](#page-104-1) or [STRICT\\_TRANS\\_TABLES](#page-104-0) is enabled, although the effects of these modes differ somewhat:

- For transactional tables, an error occurs for invalid or missing values in a data-change statement when either [STRICT\\_ALL\\_TABLES](#page-104-1) or [STRICT\\_TRANS\\_TABLES](#page-104-0) is enabled. The statement is aborted and rolled back.
- For nontransactional tables, the behavior is the same for either mode if the bad value occurs in the first row to be inserted or updated: The statement is aborted and the table remains unchanged. If the statement inserts or modifies multiple rows and the bad value occurs in the second or later row, the result depends on which strict mode is enabled:
  - For [STRICT\\_ALL\\_TABLES](#page-104-1), MySQL returns an error and ignores the rest of the rows. However, because the earlier rows have been inserted or updated, the result is a partial update. To avoid this, use single-row statements, which can be aborted without changing the table.
  - For [STRICT\\_TRANS\\_TABLES](#page-104-0), MySQL converts an invalid value to the closest valid value for the column and inserts the adjusted value. If a value is missing, MySQL inserts the implicit default value for the column data type. In either case, MySQL generates a warning rather than an error and continues processing the statement. Implicit defaults are described in Section 13.6, "Data Type Default Values".

Strict mode affects handling of division by zero, zero dates, and zeros in dates as follows:

• Strict mode affects handling of division by zero, which includes MOD(N,0):

For data-change operations (INSERT, UPDATE):

- If strict mode is not enabled, division by zero inserts NULL and produces no warning.
- If strict mode is enabled, division by zero produces an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, division by zero inserts NULL and produces a warning.

For SELECT, division by zero returns NULL. Enabling strict mode causes a warning to be produced as well.

- Strict mode affects whether the server permits '0000-00-00' as a valid date:
  - If strict mode is not enabled, '0000-00-00' is permitted and inserts produce no warning.
  - If strict mode is enabled, '0000-00-00' is not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, '0000-00-00' is permitted and inserts produce a warning.
- Strict mode affects whether the server permits dates in which the year part is nonzero but the month or day part is 0 (dates such as '2010-00-01' or '2010-01-00'):
  - If strict mode is not enabled, dates with zero parts are permitted and inserts produce no warning.
  - If strict mode is enabled, dates with zero parts are not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, dates with zero parts are inserted as '0000-00-00' (which is considered valid with IGNORE) and produce a warning.

For more information about strict mode with respect to IGNORE, see [Comparison of the IGNORE](#page-107-0) [Keyword and Strict SQL Mode](#page-107-0).

Strict mode affects handling of division by zero, zero dates, and zeros in dates in conjunction with the [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-100-1), [NO\\_ZERO\\_DATE](#page-103-2), and [NO\\_ZERO\\_IN\\_DATE](#page-103-1) modes.

### <span id="page-107-0"></span>**Comparison of the IGNORE Keyword and Strict SQL Mode**

This section compares the effect on statement execution of the IGNORE keyword (which downgrades errors to warnings) and strict SQL mode (which upgrades warnings to errors). It describes which statements they affect, and which errors they apply to.

The following table presents a summary comparison of statement behavior when the default is to produce an error versus a warning. An example of when the default is to produce an error is inserting a NULL into a NOT NULL column. An example of when the default is to produce a warning is inserting a value of the wrong data type into a column (such as inserting the string 'abc' into an integer column).

| Operational Mode                     | When Statement Default is<br>Error                   | When Statement Default is<br>Warning                   |
|--------------------------------------|------------------------------------------------------|--------------------------------------------------------|
| Without IGNORE or strict SQL<br>mode | Error                                                | Warning                                                |
| With IGNORE                          | Warning                                              | Warning (same as without<br>IGNORE or strict SQL mode) |
| With strict SQL mode                 | Error (same as without IGNORE<br>or strict SQL mode) | Error                                                  |
| With IGNORE and strict SQL<br>mode   | Warning                                              | Warning                                                |

One conclusion to draw from the table is that when the IGNORE keyword and strict SQL mode are both in effect, IGNORE takes precedence. This means that, although IGNORE and strict SQL mode can be considered to have opposite effects on error handling, they do not cancel when used together.

- [The Effect of IGNORE on Statement Execution](#page-107-1)
- [The Effect of Strict SQL Mode on Statement Execution](#page-109-0)

### <span id="page-107-1"></span>**The Effect of IGNORE on Statement Execution**

Several statements in MySQL support an optional IGNORE keyword. This keyword causes the server to downgrade certain types of errors and generate warnings instead. For a multiple-row statement, downgrading an error to a warning may enable a row to be processed. Otherwise, IGNORE causes the statement to skip to the next row instead of aborting. (For nonignorable errors, an error occurs regardless of the IGNORE keyword.)

Example: If the table t has a primary key column i containing unique values, attempting to insert the same value of i into multiple rows normally produces a duplicate-key error:

```
mysql> CREATE TABLE t (i INT NOT NULL PRIMARY KEY);
mysql> INSERT INTO t (i) VALUES(1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 't.PRIMARY'
```

With IGNORE, the row containing the duplicate key still is not inserted, but a warning occurs instead of an error:

```
mysql> INSERT IGNORE INTO t (i) VALUES(1),(1);
Query OK, 1 row affected, 1 warning (0.01 sec)
Records: 2 Duplicates: 1 Warnings: 1
mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------+
| Level | Code | Message |
+---------+------+-----------------------------------------+
| Warning | 1062 | Duplicate entry '1' for key 't.PRIMARY' |
+---------+------+-----------------------------------------+
1 row in set (0.00 sec)
```

Example: If the table t2 has a NOT NULL column id, attempting to insert NULL produces an error in strict SQL mode:

```
mysql> CREATE TABLE t2 (id INT NOT NULL);
mysql> INSERT INTO t2 (id) VALUES(1),(NULL),(3);
ERROR 1048 (23000): Column 'id' cannot be null
mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

If the SQL mode is not strict, IGNORE causes the NULL to be inserted as the column implicit default (0 in this case), which enables the row to be handled without skipping it:

```
mysql> INSERT INTO t2 (id) VALUES(1),(NULL),(3);
mysql> SELECT * FROM t2;
+----+
| id |
+----+
| 1 |
| 0 |
| 3 |
+----+
```

These statements support the IGNORE keyword:

- CREATE TABLE ... SELECT: IGNORE does not apply to the CREATE TABLE or SELECT parts of the statement but to inserts into the table of rows produced by the SELECT. Rows that duplicate an existing row on a unique key value are discarded.
- DELETE: IGNORE causes MySQL to ignore errors during the process of deleting rows.
- INSERT: With IGNORE, rows that duplicate an existing row on a unique key value are discarded. Rows set to values that would cause data conversion errors are set to the closest valid values instead.

 For partitioned tables where no partition matching a given value is found, IGNORE causes the insert operation to fail silently for rows containing the unmatched value.

- LOAD DATA, LOAD XML: With IGNORE, rows that duplicate an existing row on a unique key value are discarded.
- UPDATE: With IGNORE, rows for which duplicate-key conflicts occur on a unique key value are not updated. Rows updated to values that would cause data conversion errors are updated to the closest valid values instead.

The IGNORE keyword applies to the following ignorable errors:

```
• ER_BAD_NULL_ERROR
```

- [ER\\_DUP\\_ENTRY](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_dup_entry)
- [ER\\_DUP\\_ENTRY\\_WITH\\_KEY\\_NAME](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_dup_entry_with_key_name)
- [ER\\_DUP\\_KEY](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_dup_key)
- [ER\\_NO\\_PARTITION\\_FOR\\_GIVEN\\_VALUE](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_no_partition_for_given_value)
- [ER\\_NO\\_PARTITION\\_FOR\\_GIVEN\\_VALUE\\_SILENT](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_no_partition_for_given_value_silent)
- [ER\\_NO\\_REFERENCED\\_ROW\\_2](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_no_referenced_row_2)
- [ER\\_ROW\\_DOES\\_NOT\\_MATCH\\_GIVEN\\_PARTITION\\_SET](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_row_does_not_match_given_partition_set)
- [ER\\_ROW\\_IS\\_REFERENCED\\_2](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_row_is_referenced_2)
- [ER\\_SUBQUERY\\_NO\\_1\\_ROW](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_subquery_no_1_row)
- [ER\\_VIEW\\_CHECK\\_FAILED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_view_check_failed)

### <span id="page-109-0"></span>**The Effect of Strict SQL Mode on Statement Execution**

The MySQL server can operate in different SQL modes, and can apply these modes differently for different clients, depending on the value of the [sql\\_mode](#page-6-0) system variable. In "strict" SQL mode, the server upgrades certain warnings to errors.

For example, in non-strict SQL mode, inserting the string 'abc' into an integer column results in conversion of the value to 0 and a warning:

```
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO t (i) VALUES('abc');
Query OK, 1 row affected, 1 warning (0.01 sec)
mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------+
| Level | Code | Message |
+---------+------+--------------------------------------------------------+
| Warning | 1366 | Incorrect integer value: 'abc' for column 'i' at row 1 |
+---------+------+--------------------------------------------------------+
1 row in set (0.00 sec)
```

In strict SQL mode, the invalid value is rejected with an error:

```
mysql> SET sql_mode = 'STRICT_ALL_TABLES';
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO t (i) VALUES('abc');
ERROR 1366 (HY000): Incorrect integer value: 'abc' for column 'i' at row 1
```

For more information about possible settings of the [sql\\_mode](#page-6-0) system variable, see [Section 7.1.11,](#page-98-0) ["Server SQL Modes".](#page-98-0)

Strict SQL mode applies to the following statements under conditions for which some value might be out of range or an invalid row is inserted into or deleted from a table:

- ALTER TABLE
- CREATE TABLE
- CREATE TABLE ... SELECT
- DELETE (both single table and multiple table)
- INSERT
- LOAD DATA
- LOAD XML
- SELECT SLEEP()
- UPDATE (both single table and multiple table)

Within stored programs, individual statements of the types just listed execute in strict SQL mode if the program was defined while strict mode was in effect.

Strict SQL mode applies to the following errors, which represent a class of errors in which an input value is either invalid or missing. A value is invalid if it has the wrong data type for the column or might be out of range. A value is missing if a new row to be inserted does not contain a value for a NOT NULL column that has no explicit DEFAULT clause in its definition.

```
ER_BAD_NULL_ERROR
ER_CUT_VALUE_GROUP_CONCAT
ER_DATA_TOO_LONG
ER_DATETIME_FUNCTION_OVERFLOW
```

```
ER_DIVISION_BY_ZERO
ER_INVALID_ARGUMENT_FOR_LOGARITHM
ER_NO_DEFAULT_FOR_FIELD
ER_NO_DEFAULT_FOR_VIEW_FIELD
ER_TOO_LONG_KEY
ER_TRUNCATED_WRONG_VALUE
ER_TRUNCATED_WRONG_VALUE_FOR_FIELD
ER_WARN_DATA_OUT_OF_RANGE
ER_WARN_NULL_TO_NOTNULL
ER_WARN_TOO_FEW_RECORDS
ER_WRONG_ARGUMENTS
ER_WRONG_VALUE_FOR_TYPE
WARN_DATA_TRUNCATED
```

![](_page_110_Picture_2.jpeg)

#### **Note**

Because continued MySQL development defines new errors, there may be errors not in the preceding list to which strict SQL mode applies.