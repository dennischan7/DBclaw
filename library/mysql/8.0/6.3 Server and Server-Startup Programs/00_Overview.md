---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes [mysqld](#page-37-0), the MySQL server, and several programs that are used to start the server.

# <span id="page-37-0"></span>**6.3.1 mysqld — The MySQL Server**

[mysqld](#page-37-0), also known as MySQL Server, is a single multithreaded program that does most of the work in a MySQL installation. It does not spawn additional processes. MySQL Server manages access to the MySQL data directory that contains databases and tables. The data directory is also the default location for other information such as log files and status files.

![](_page_37_Picture_13.jpeg)

# **Note**

Some installation packages contain a debugging version of the server named [mysqld-debug](#page-37-0). Invoke this version instead of [mysqld](#page-37-0) for debugging support, memory allocation checking, and trace file support (see Section 7.9.1.2, "Creating Trace Files").

When MySQL server starts, it listens for network connections from client programs and manages access to databases on behalf of those clients.

The [mysqld](#page-37-0) program has many options that can be specified at startup. For a complete list of options, run this command:

```
mysqld --verbose --help
```

MySQL Server also has a set of system variables that affect its operation as it runs. System variables can be set at server startup, and many of them can be changed at runtime to effect dynamic server reconfiguration. MySQL Server also has a set of status variables that provide information about its operation. You can monitor these status variables to access runtime performance characteristics.

For a full description of MySQL Server command options, system variables, and status variables, see Section 7.1, "The MySQL Server". For information about installing MySQL and setting up the initial configuration, see Chapter 2, Installing MySQL.

# <span id="page-37-1"></span>**6.3.2 mysqld\_safe — MySQL Server Startup Script**

[mysqld\\_safe](#page-37-1) is the recommended way to start a [mysqld](#page-37-0) server on Unix. [mysqld\\_safe](#page-37-1) adds some safety features such as restarting the server when an error occurs and logging runtime information to an error log. A description of error logging is given later in this section.

![](_page_38_Picture_1.jpeg)

### **Note**

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysqld\\_safe](#page-37-1) is not installed because it is unnecessary. For more information, see Section 2.5.9, "Managing MySQL Server with systemd".

One implication of the non-use of [mysqld\\_safe](#page-37-1) on platforms that use systemd for server management is that use of [mysqld\_safe] or [safe\_mysqld] sections in option files is not supported and might lead to unexpected behavior.

[mysqld\\_safe](#page-37-1) tries to start an executable named [mysqld](#page-37-0). To override the default behavior and specify explicitly the name of the server you want to run, specify a [--mysqld](#page-42-0) or [--mysqld-version](#page-42-1) option to [mysqld\\_safe](#page-37-1). You can also use [--ledir](#page-40-1) to indicate the directory where [mysqld\\_safe](#page-37-1) should look for the server.

Many of the options to [mysqld\\_safe](#page-37-1) are the same as the options to [mysqld](#page-37-0). See Section 7.1.7, "Server Command Options".

Options unknown to [mysqld\\_safe](#page-37-1) are passed to [mysqld](#page-37-0) if they are specified on the command line, but ignored if they are specified in the [mysqld\_safe] group of an option file. See Section 6.2.2.2, "Using Option Files".

[mysqld\\_safe](#page-37-1) reads all options from the [mysqld], [server], and [mysqld\_safe] sections in option files. For example, if you specify a [mysqld] section like this, [mysqld\\_safe](#page-37-1) finds and uses the [--log-error](#page-40-0) option:

```
[mysqld]
log-error=error.log
```

For backward compatibility, [mysqld\\_safe](#page-37-1) also reads [safe\_mysqld] sections, but to be current you should rename such sections to [mysqld\_safe].

[mysqld\\_safe](#page-37-1) accepts options on the command line and in option files, as described in the following table. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.7 mysqld\_safe Options**

| Option Name                | Description                                                 |
|----------------------------|-------------------------------------------------------------|
| basedir                    | Path to MySQL installation directory                        |
| core-file-size             | Size of core file that mysqld should be able to<br>create   |
| datadir                    | Path to data directory                                      |
| defaults-extra-file        | Read named option file in addition to usual option<br>files |
| defaults-file              | Read only named option file                                 |
| help                       | Display help message and exit                               |
| ledir                      | Path to directory where server is located                   |
| log-error                  | Write error log to named file                               |
| malloc-lib                 | Alternative malloc library to use for mysqld                |
| mysqld                     | Name of server program to start (in ledir directory)        |
| mysqld-safe-log-timestamps | Timestamp format for logging                                |
| mysqld-version             | Suffix for server program name                              |
| nice                       | Use nice program to set server scheduling priority          |

| Option Name      | Description                                                            |
|------------------|------------------------------------------------------------------------|
| no-defaults      | Read no option files                                                   |
| open-files-limit | Number of files that mysqld should be able to<br>open                  |
| pid-file         | Path name of server process ID file                                    |
| plugin-dir       | Directory where plugins are installed                                  |
| port             | Port number on which to listen for TCP/IP<br>connections               |
| skip-kill-mysqld | Do not try to kill stray mysqld processes                              |
| skip-syslog      | Do not write error messages to syslog; use error<br>log file           |
| socket           | Socket file on which to listen for Unix socket<br>connections          |
| syslog           | Write error messages to syslog                                         |
| syslog-tag       | Tag suffix for messages written to syslog                              |
| timezone         | Set TZ time zone environment variable to named<br>value                |
| user             | Run mysqld as user having name user_name or<br>numeric user ID user_id |

### <span id="page-39-3"></span>• [--help](#page-39-3)

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-39-0"></span>• [--basedir=](#page-39-0)dir\_name

| Command-Line Format | basedir=dir_name |
|---------------------|------------------|
| Type                | Directory name   |

The path to the MySQL installation directory.

<span id="page-39-1"></span>• [--core-file-size=](#page-39-1)size

| Command-Line Format | core-file-size=size |
|---------------------|---------------------|
| Type                | String              |

The size of the core file that [mysqld](#page-37-0) should be able to create. The option value is passed to ulimit -c.

![](_page_39_Picture_11.jpeg)

# **Note**

The innodb\_buffer\_pool\_in\_core\_file variable can be used to reduce the size of core files on operating systems that support it. For more information, see Section 17.8.3.7, "Excluding Buffer Pool Pages from Core Files".

<span id="page-39-2"></span>• [--datadir=](#page-39-2)dir\_name

| Command-Line Format | datadir=dir_name |
|---------------------|------------------|
|                     |                  |

| Type | Directory name |
|------|----------------|
|------|----------------|

The path to the data directory.

<span id="page-40-2"></span>• [--defaults-extra-file=](#page-40-2)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file in addition to the usual option files. If the file does not exist or is otherwise inaccessible, the server exits with an error. If file\_name is not an absolute path name, it is interpreted relative to the current directory. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-40-3"></span>• [--defaults-file=](#page-40-3)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, the server exits with an error. If file\_name is not an absolute path name, it is interpreted relative to the current directory. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-40-1"></span>• [--ledir=](#page-40-1)dir\_name

| Command-Line Format | ledir=dir_name |
|---------------------|----------------|
| Type                | Directory name |

If [mysqld\\_safe](#page-37-1) cannot find the server, use this option to indicate the path name to the directory where the server is located.

This option is accepted only on the command line, not in option files. On platforms that use systemd, the value can be specified in the value of MYSQLD\_OPTS. See Section 2.5.9, "Managing MySQL Server with systemd".

<span id="page-40-0"></span>• [--log-error=](#page-40-0)file\_name

| Command-Line Format | log-error=file_name |
|---------------------|---------------------|
| Type                | File name           |

Write the error log to the given file. See Section 7.4.2, "The Error Log".

<span id="page-40-4"></span>• [--mysqld-safe-log-timestamps](#page-40-4)

| Command-Line Format | mysqld-safe-log-timestamps=type |
|---------------------|---------------------------------|
| Type                | Enumeration                     |
| Default Value       | utc                             |

| Valid Values | system |
|--------------|--------|
|              | hyphen |
|              | legacy |

This option controls the format for timestamps in log output produced by [mysqld\\_safe](#page-37-1). The following list describes the permitted values. For any other value, [mysqld\\_safe](#page-37-1) logs a warning and uses UTC format.

• UTC, utc

ISO 8601 UTC format (same as --log\_timestamps=UTC for the server). This is the default.

• SYSTEM, system

ISO 8601 local time format (same as --log\_timestamps=SYSTEM for the server).

• HYPHEN, hyphen

YY-MM-DD h:mm:ss format, as in [mysqld\\_safe](#page-37-1) for MySQL 5.6.

• LEGACY, legacy

YYMMDD hh:mm:ss format, as in [mysqld\\_safe](#page-37-1) prior to MySQL 5.6.

<span id="page-41-0"></span>• [--malloc-lib=\[](#page-41-0)lib\_name]

| Command-Line Format | malloc-lib=[lib-name] |
|---------------------|-----------------------|
| Type                | String                |

The name of the library to use for memory allocation instead of the system malloc() library. The option value must be one of the directories /usr/lib, /usr/lib64, /usr/lib/i386-linuxgnu, or /usr/lib/x86\_64-linux-gnu.

The [--malloc-lib](#page-41-0) option works by modifying the LD\_PRELOAD environment value to affect dynamic linking to enable the loader to find the memory-allocation library when [mysqld](#page-37-0) runs:

- If the option is not given, or is given without a value ([--malloc-lib=](#page-41-0)), LD\_PRELOAD is not modified and no attempt is made to use tcmalloc.
- Prior to MySQL 8.0.21, if the option is given as [--malloc-lib=tcmalloc](#page-41-0), [mysqld\\_safe](#page-37-1) looks for a tcmalloc library in /usr/lib. If tmalloc is found, its path name is added to the beginning

of the LD\_PRELOAD value for [mysqld](#page-37-0). If tcmalloc is not found, [mysqld\\_safe](#page-37-1) aborts with an error.

As of MySQL 8.0.21, tcmalloc is not a permitted value for the [--malloc-lib](#page-41-0) option.

- If the option is given as --malloc-lib=[/path/to/some/library](#page-41-0), that full path is added to the beginning of the LD\_PRELOAD value. If the full path points to a nonexistent or unreadable file, [mysqld\\_safe](#page-37-1) aborts with an error.
- For cases where [mysqld\\_safe](#page-37-1) adds a path name to LD\_PRELOAD, it adds the path to the beginning of any existing value the variable already has.

![](_page_42_Picture_5.jpeg)

### **Note**

On systems that manage the server using systemd, [mysqld\\_safe](#page-37-1) is not available. Instead, specify the allocation library by setting LD\_PRELOAD in / etc/sysconfig/mysql.

Linux users can use the libtcmalloc\_minimal.so library on any platform for which a tcmalloc package is installed in /usr/lib by adding these lines to the my.cnf file:

```
[mysqld_safe]
malloc-lib=tcmalloc
```

To use a specific tcmalloc library, specify its full path name. Example:

```
[mysqld_safe]
malloc-lib=/opt/lib/libtcmalloc_minimal.so
```

<span id="page-42-0"></span>• [--mysqld=](#page-42-0)prog\_name

| Command-Line Format | mysqld=file_name |
|---------------------|------------------|
| Type                | File name        |

The name of the server program (in the ledir directory) that you want to start. This option is needed if you use the MySQL binary distribution but have the data directory outside of the binary distribution. If [mysqld\\_safe](#page-37-1) cannot find the server, use the [--ledir](#page-40-1) option to indicate the path name to the directory where the server is located.

This option is accepted only on the command line, not in option files. On platforms that use systemd, the value can be specified in the value of MYSQLD\_OPTS. See Section 2.5.9, "Managing MySQL Server with systemd".

<span id="page-42-1"></span>• [--mysqld-version=](#page-42-1)suffix

| Command-Line Format | mysqld-version=suffix |
|---------------------|-----------------------|
| Type                | String                |

This option is similar to the [--mysqld](#page-42-0) option, but you specify only the suffix for the server program name. The base name is assumed to be [mysqld](#page-37-0). For example, if you use [--mysqld](#page-42-1)[version=debug](#page-42-1), [mysqld\\_safe](#page-37-1) starts the [mysqld-debug](#page-37-0) program in the ledir directory. If the argument to [--mysqld-version](#page-42-1) is empty, [mysqld\\_safe](#page-37-1) uses [mysqld](#page-37-0) in the ledir directory.

This option is accepted only on the command line, not in option files. On platforms that use systemd, the value can be specified in the value of MYSQLD\_OPTS. See Section 2.5.9, "Managing MySQL Server with systemd". 413

### <span id="page-43-0"></span>• --nice=[priority](#page-43-0)

| Command-Line Format | nice=priority |
|---------------------|---------------|
| Type                | Numeric       |

Use the nice program to set the server's scheduling priority to the given value.

### <span id="page-43-1"></span>• [--no-defaults](#page-43-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
| Type                | String      |

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-43-1) can be used to prevent them from being read. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

### <span id="page-43-2"></span>• [--open-files-limit=](#page-43-2)count

| Command-Line Format | open-files-limit=count |
|---------------------|------------------------|
| Type                | String                 |

The number of files that [mysqld](#page-37-0) should be able to open. The option value is passed to ulimit -n.

![](_page_43_Picture_11.jpeg)

# **Note**

You must start [mysqld\\_safe](#page-37-1) as root for this to function properly.

<span id="page-43-3"></span>• [--pid-file=](#page-43-3)file\_name

| Command-Line Format | pid-file=file_name |
|---------------------|--------------------|
| Type                | File name          |

The path name that [mysqld](#page-37-0) should use for its process ID file.

<span id="page-43-4"></span>• [--plugin-dir=](#page-43-4)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The path name of the plugin directory.

<span id="page-43-5"></span>• --port=[port\\_num](#page-43-5)

| Command-Line Format | port=number |
|---------------------|-------------|
| Type                | Numeric     |

### <span id="page-44-0"></span>• [--skip-kill-mysqld](#page-44-0)

| Command-Line Format | skip-kill-mysqld |
|---------------------|------------------|
|---------------------|------------------|

Do not try to kill stray [mysqld](#page-37-0) processes at startup. This option works only on Linux.

### <span id="page-44-2"></span>• [--socket=](#page-44-2)path

| Command-Line Format | socket=file_name |
|---------------------|------------------|
| Type                | File name        |

The Unix socket file that the server should use when listening for local connections.

### <span id="page-44-1"></span>• [--syslog](#page-44-1), [--skip-syslog](#page-44-1)

| Command-Line Format | syslog |
|---------------------|--------|
| Deprecated          | Yes    |

| Command-Line Format | skip-syslog |
|---------------------|-------------|
| Deprecated          | Yes         |

[--syslog](#page-44-1) causes error messages to be sent to syslog on systems that support the logger program. --skip-syslog suppresses the use of syslog; messages are written to an error log file.

When syslog is used for error logging, the daemon.err facility/severity is used for all log messages.

Using these options to control [mysqld](#page-37-0) logging is deprecated. To write error log output to the system log, use the instructions at Section 7.4.2.8, "Error Logging to the System Log". To control the facility, use the server log\_syslog\_facility system variable.

### <span id="page-44-3"></span>• [--syslog-tag=](#page-44-3)tag

| Command-Line Format | syslog-tag=tag |
|---------------------|----------------|
| Deprecated          | Yes            |

For logging to syslog, messages from [mysqld\\_safe](#page-37-1) and [mysqld](#page-37-0) are written with identifiers of mysqld\_safe and mysqld, respectively. To specify a suffix for the identifiers, use [--syslog](#page-44-3)[tag=](#page-44-3)tag, which modifies the identifiers to be mysqld\_safe-tag and mysqld-tag.

Using this option to control [mysqld](#page-37-0) logging is deprecated. Use the server log\_syslog\_tag system variable instead. See Section 7.4.2.8, "Error Logging to the System Log".

### <span id="page-44-4"></span>• [--timezone=](#page-44-4)timezone

| Command-Line Format | timezone=timezone | 415 |
|---------------------|-------------------|-----|
| Type                | String            |     |

<span id="page-45-0"></span>• --user={[user\\_name](#page-45-0)|user\_id}

| Command-Line Format | user={user_name user_id} |
|---------------------|--------------------------|
| Type                | String                   |
| Type                | Numeric                  |

Run the [mysqld](#page-37-0) server as the user having the name user\_name or the numeric user ID user\_id. ("User" in this context refers to a system login account, not a MySQL user listed in the grant tables.)

If you execute [mysqld\\_safe](#page-37-1) with the [--defaults-file](#page-40-3) or [--defaults-extra-file](#page-40-2) option to name an option file, the option must be the first one given on the command line or the option file is not used. For example, this command does not use the named option file:

```
mysql> mysqld_safe --port=port_num --defaults-file=file_name
```

Instead, use the following command:

```
mysql> mysqld_safe --defaults-file=file_name --port=port_num
```

The [mysqld\\_safe](#page-37-1) script is written so that it normally can start a server that was installed from either a source or a binary distribution of MySQL, even though these types of distributions typically install the server in slightly different locations. (See Section 2.1.5, "Installation Layouts".) [mysqld\\_safe](#page-37-1) expects one of the following conditions to be true:

- The server and databases can be found relative to the working directory (the directory from which [mysqld\\_safe](#page-37-1) is invoked). For binary distributions, [mysqld\\_safe](#page-37-1) looks under its working directory for bin and data directories. For source distributions, it looks for libexec and var directories. This condition should be met if you execute [mysqld\\_safe](#page-37-1) from your MySQL installation directory (for example, /usr/local/mysql for a binary distribution).
- If the server and databases cannot be found relative to the working directory, [mysqld\\_safe](#page-37-1) attempts to locate them by absolute path names. Typical locations are /usr/local/libexec and /usr/local/var. The actual locations are determined from the values configured into the distribution at the time it was built. They should be correct if MySQL is installed in the location specified at configuration time.

Because [mysqld\\_safe](#page-37-1) tries to find the server and databases relative to its own working directory, you can install a binary distribution of MySQL anywhere, as long as you run [mysqld\\_safe](#page-37-1) from the MySQL installation directory:

```
cd mysql_installation_directory
bin/mysqld_safe &
```

If [mysqld\\_safe](#page-37-1) fails, even when invoked from the MySQL installation directory, specify the [--ledir](#page-40-1) and [--datadir](#page-39-2) options to indicate the directories in which the server and databases are located on your system.

[mysqld\\_safe](#page-37-1) tries to use the sleep and date system utilities to determine how many times per second it has attempted to start. If these utilities are present and the attempted starts per second is greater than 5, [mysqld\\_safe](#page-37-1) waits 1 full second before starting again. This is intended to prevent excessive CPU usage in the event of repeated failures. (Bug #11761530, Bug #54035)

When you use [mysqld\\_safe](#page-37-1) to start [mysqld](#page-37-0), [mysqld\\_safe](#page-37-1) arranges for error (and notice) messages from itself and from [mysqld](#page-37-0) to go to the same destination.

There are several [mysqld\\_safe](#page-37-1) options for controlling the destination of these messages:

- [--log-error=](#page-40-0)file\_name: Write error messages to the named error file.
- [--syslog](#page-44-1): Write error messages to syslog on systems that support the logger program.

• [--skip-syslog](#page-44-1): Do not write error messages to syslog. Messages are written to the default error log file (host\_name.err in the data directory), or to a named file if the [--log-error](#page-40-0) option is given.

If none of these options is given, the default is [--skip-syslog](#page-44-1).

When [mysqld\\_safe](#page-37-1) writes a message, notices go to the logging destination (syslog or the error log file) and stdout. Errors go to the logging destination and stderr.

![](_page_46_Picture_4.jpeg)

### **Note**

Controlling [mysqld](#page-37-0) logging from [mysqld\\_safe](#page-37-1) is deprecated. Use the server's native syslog support instead. For more information, see Section 7.4.2.8, "Error Logging to the System Log".

# <span id="page-46-0"></span>**6.3.3 mysql.server — MySQL Server Startup Script**

MySQL distributions on Unix and Unix-like system include a script named [mysql.server](#page-46-0), which starts the MySQL server using [mysqld\\_safe](#page-37-1). It can be used on systems such as Linux and Solaris that use System V-style run directories to start and stop system services. It is also used by the macOS Startup Item for MySQL.

[mysql.server](#page-46-0) is the script name as used within the MySQL source tree. The installed name might be different (for example, [mysqld](#page-37-0) or [mysql](#page-77-0)). In the following discussion, adjust the name [mysql.server](#page-46-0) as appropriate for your system.

![](_page_46_Picture_10.jpeg)

### **Note**

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysql.server](#page-46-0) and [mysqld\\_safe](#page-37-1) are not installed because they are unnecessary. For more information, see Section 2.5.9, "Managing MySQL Server with systemd".

To start or stop the server manually using the [mysql.server](#page-46-0) script, invoke it from the command line with start or stop arguments:

```
mysql.server start
mysql.server stop
```

[mysql.server](#page-46-0) changes location to the MySQL installation directory, then invokes [mysqld\\_safe](#page-37-1). To run the server as some specific user, add an appropriate user option to the [mysqld] group of the global /etc/my.cnf option file, as shown later in this section. (It is possible that you must edit [mysql.server](#page-46-0) if you've installed a binary distribution of MySQL in a nonstandard location. Modify it to change location into the proper directory before it runs [mysqld\\_safe](#page-37-1). If you do this, your modified version of [mysql.server](#page-46-0) may be overwritten if you upgrade MySQL in the future; make a copy of your edited version that you can reinstall.)

[mysql.server stop](#page-46-0) stops the server by sending a signal to it. You can also stop the server manually by executing [mysqladmin shutdown](#page-121-0).

To start and stop MySQL automatically on your server, you must add start and stop commands to the appropriate places in your /etc/rc\* files:

- If you use the Linux server RPM package (MySQL-server-VERSION.rpm), or a native Linux package installation, the [mysql.server](#page-46-0) script may be installed in the /etc/init.d directory with the name mysqld or mysql. See Section 2.5.4, "Installing MySQL on Linux Using RPM Packages from Oracle", for more information on the Linux RPM packages.
- If you install MySQL from a source distribution or using a binary distribution format that does not install [mysql.server](#page-46-0) automatically, you can install the script manually. It can be found in the support-files directory under the MySQL installation directory or in a MySQL source tree. Copy the script to the /etc/init.d directory with the name [mysql](#page-77-0) and make it executable:

```
cp mysql.server /etc/init.d/mysql
chmod +x /etc/init.d/mysql
```

After installing the script, the commands needed to activate it to run at system startup depend on your operating system. On Linux, you can use chkconfig:

```
chkconfig --add mysql
```

On some Linux systems, the following command also seems to be necessary to fully enable the [mysql](#page-77-0) script:

```
chkconfig --level 345 mysql on
```

- On FreeBSD, startup scripts generally should go in /usr/local/etc/rc.d/. Install the mysql.server script as /usr/local/etc/rc.d/mysql.server.sh to enable automatic startup. The rc(8) manual page states that scripts in this directory are executed only if their base name matches the \*.sh shell file name pattern. Any other files or directories present within the directory are silently ignored.
- As an alternative to the preceding setup, some operating systems also use /etc/rc.local or / etc/init.d/boot.local to start additional services on startup. To start up MySQL using this method, append a command like the one following to the appropriate startup file:

```
/bin/sh -c 'cd /usr/local/mysql; ./bin/mysqld_safe --user=mysql &'
```

• For other systems, consult your operating system documentation to see how to install startup scripts.

[mysql.server](#page-46-0) reads options from the [mysql.server] and [mysqld] sections of option files. For backward compatibility, it also reads [mysql\_server] sections, but to be current you should rename such sections to [mysql.server].

You can add options for [mysql.server](#page-46-0) in a global /etc/my.cnf file. A typical my.cnf file might look like this:

```
[mysqld]
datadir=/usr/local/mysql/var
socket=/var/tmp/mysql.sock
port=3306
user=mysql
[mysql.server]
basedir=/usr/local/mysql
```

The [mysql.server](#page-46-0) script supports the options shown in the following table. If specified, they must be placed in an option file, not on the command line. [mysql.server](#page-46-0) supports only start and stop as command-line arguments.

**Table 6.8 mysql.server Option-File Options**

| Option Name             | Description                                         | Type           |
|-------------------------|-----------------------------------------------------|----------------|
| basedir                 | Path to MySQL installation<br>directory             | Directory name |
| datadir                 | Path to MySQL data directory                        | Directory name |
| pid-file                | File in which server should write<br>its process ID | File name      |
| service-startup-timeout | How long to wait for server<br>startup              | Integer        |

<span id="page-47-0"></span>• [basedir=](#page-47-0)dir\_name

The path to the MySQL installation directory.

<span id="page-48-0"></span>• [datadir=](#page-48-0)dir\_name

The path to the MySQL data directory.

<span id="page-48-1"></span>• [pid-file=](#page-48-1)file\_name

The path name of the file in which the server should write its process ID. The server creates the file in the data directory unless an absolute path name is given to specify a different directory.

If this option is not given, [mysql.server](#page-46-0) uses a default value of host\_name.pid. The PID file value passed to [mysqld\\_safe](#page-37-1) overrides any value specified in the [mysqld\_safe] option file group. Because [mysql.server](#page-46-0) reads the [mysqld] option file group but not the [mysqld\_safe] group, you can ensure that [mysqld\\_safe](#page-37-1) gets the same value when invoked from [mysql.server](#page-46-0) as when invoked manually by putting the same pid-file setting in both the [mysqld\_safe] and [mysqld] groups.

<span id="page-48-2"></span>• [service-startup-timeout=](#page-48-2)seconds

How long in seconds to wait for confirmation of server startup. If the server does not start within this time, [mysql.server](#page-46-0) exits with an error. The default value is 900. A value of 0 means not to wait at all for startup. Negative values mean to wait forever (no timeout).

# <span id="page-48-3"></span>**6.3.4 mysqld\_multi — Manage Multiple MySQL Servers**

[mysqld\\_multi](#page-48-3) is designed to manage several [mysqld](#page-37-0) processes that listen for connections on different Unix socket files and TCP/IP ports. It can start or stop servers, or report their current status.

![](_page_48_Picture_10.jpeg)

### **Note**

For some Linux platforms, MySQL installation from RPM or Debian packages includes systemd support for managing MySQL server startup and shutdown. On these platforms, [mysqld\\_multi](#page-48-3) is not installed because it is unnecessary. For information about using systemd to handle multiple MySQL instances, see Section 2.5.9, "Managing MySQL Server with systemd".

[mysqld\\_multi](#page-48-3) searches for groups named [mysqldN] in my.cnf (or in the file named by the [-](#page-49-0) [defaults-file](#page-49-0) option). N can be any positive integer. This number is referred to in the following discussion as the option group number, or GNR. Group numbers distinguish option groups from one another and are used as arguments to [mysqld\\_multi](#page-48-3) to specify which servers you want to start, stop, or obtain a status report for. Options listed in these groups are the same that you would use in the [mysqld] group used for starting [mysqld](#page-37-0). (See, for example, Section 2.9.5, "Starting and Stopping MySQL Automatically".) However, when using multiple servers, it is necessary that each one use its own value for options such as the Unix socket file and TCP/IP port number. For more information on which options must be unique per server in a multiple-server environment, see Section 7.8, "Running Multiple MySQL Instances on One Machine".

To invoke [mysqld\\_multi](#page-48-3), use the following syntax:

```
mysqld_multi [options] {start|stop|reload|report} [GNR[,GNR] ...]
```

start, stop, reload (stop and restart), and report indicate which operation to perform. You can perform the designated operation for a single server or multiple servers, depending on the GNR list that follows the option name. If there is no list, [mysqld\\_multi](#page-48-3) performs the operation for all servers in the option file.

Each GNR value represents an option group number or range of group numbers. The value should be the number at the end of the group name in the option file. For example, the GNR for a group named [mysqld17] is 17. To specify a range of numbers, separate the first and last numbers by a dash. The GNR value 10-13 represents groups [mysqld10] through [mysqld13]. Multiple groups or group ranges can be specified on the command line, separated by commas. There must be no whitespace characters (spaces or tabs) in the GNR list; anything after a whitespace character is ignored.

This command starts a single server using option group [mysqld17]:

```
mysqld_multi start 17
```

This command stops several servers, using option groups [mysqld8] and [mysqld10] through [mysqld13]:

```
mysqld_multi stop 8,10-13
```

For an example of how you might set up an option file, use this command:

```
mysqld_multi --example
```

[mysqld\\_multi](#page-48-3) searches for option files as follows:

<span id="page-49-1"></span>• With [--no-defaults](#page-49-1), no option files are read.

| Command-Line Format | no-defaults |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | false       |

<span id="page-49-0"></span>• With [--defaults-file=](#page-49-0)file\_name, only the named file is read.

| Command-Line Format | defaults-file=filename |  |
|---------------------|------------------------|--|
| Type                | File name              |  |
| Default Value       | [none]                 |  |

<span id="page-49-2"></span>• Otherwise, option files in the standard list of locations are read, including any file named by the [-](#page-49-2) [defaults-extra-file=](#page-49-2)file\_name option, if one is given. (If the option is given multiple times, the last value is used.)

| Command-Line Format | defaults-extra-file=filename |
|---------------------|------------------------------|
| Type                | File name                    |
| Default Value       | [none]                       |

For additional information about these and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

Option files read are searched for [mysqld\_multi] and [mysqldN] option groups. The [mysqld\_multi] group can be used for options to [mysqld\\_multi](#page-48-3) itself. [mysqldN] groups can be used for options passed to specific [mysqld](#page-37-0) instances.

The [mysqld] or [mysqld\_safe] groups can be used for common options read by all instances of [mysqld](#page-37-0) or [mysqld\\_safe](#page-37-1). You can specify a --defaults-file=file\_name option to use a different configuration file for that instance, in which case the [mysqld] or [mysqld\_safe] groups from that file are used for that instance.

[mysqld\\_multi](#page-48-3) supports the following options.

<span id="page-49-3"></span>• [--help](#page-49-3)

| Command-Line Format | help    |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Display a help message and exit.

### <span id="page-50-0"></span>• [--example](#page-50-0)

| Command-Line Format | example |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Display a sample option file.

### <span id="page-50-1"></span>• --log=[file\\_name](#page-50-1)

| Command-Line Format | log=path                  |
|---------------------|---------------------------|
| Type                | File name                 |
| Default Value       | /var/log/mysqld_multi.log |

Specify the name of the log file. If the file exists, log output is appended to it.

### <span id="page-50-2"></span>• [--mysqladmin=](#page-50-2)prog\_name

| Command-Line Format | mysqladmin=file |
|---------------------|-----------------|
| Type                | File name       |
| Default Value       | [none]          |

The [mysqladmin](#page-121-0) binary to be used to stop servers.

### <span id="page-50-3"></span>• [--mysqld=](#page-50-3)prog\_name

| Command-Line Format | mysqld=file |
|---------------------|-------------|
| Type                | File name   |
| Default Value       | [none]      |

The [mysqld](#page-37-0) binary to be used. Note that you can specify [mysqld\\_safe](#page-37-1) as the value for this option also. If you use [mysqld\\_safe](#page-37-1) to start the server, you can include the mysqld or ledir options in the corresponding [mysqldN] option group. These options indicate the name of the server that [mysqld\\_safe](#page-37-1) should start and the path name of the directory where the server is located. (See the descriptions for these options in [Section 6.3.2, "mysqld\\_safe — MySQL Server Startup Script"](#page-37-1).) Example:

```
[mysqld38]
mysqld = mysqld-debug
ledir = /opt/local/mysql/libexec
```

### <span id="page-50-4"></span>• [--no-log](#page-50-4)

| Command-Line Format | no-log  |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Print log information to stdout rather than to the log file. By default, output goes to the log file.

### <span id="page-50-5"></span>• [--password=](#page-50-5)password

| Command-Line Format | password=string |
|---------------------|-----------------|

| Type          | String |
|---------------|--------|
| Default Value | [none] |

The password of the MySQL account to use when invoking [mysqladmin](#page-121-0). Note that the password value is not optional for this option, unlike for other MySQL programs.

### <span id="page-51-0"></span>• [--silent](#page-51-0)

| Command-Line Format | silent  |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Silent mode; disable warnings.

### <span id="page-51-1"></span>• [--tcp-ip](#page-51-1)

| Command-Line Format | tcp-ip  |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Connect to each MySQL server through the TCP/IP port instead of the Unix socket file. (If a socket file is missing, the server might still be running, but accessible only through the TCP/IP port.) By default, connections are made using the Unix socket file. This option affects stop and report operations.

### <span id="page-51-2"></span>• --user=[user\\_name](#page-51-2)

| Command-Line Format | user=name |
|---------------------|-----------|
| Type                | String    |
| Default Value       | root      |

The user name of the MySQL account to use when invoking [mysqladmin](#page-121-0).

### <span id="page-51-3"></span>• [--verbose](#page-51-3)

| Command-Line Format | verbose |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

# Be more verbose.

### <span id="page-51-4"></span>• [--version](#page-51-4)

| Command-Line Format | version |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Display version information and exit.

Some notes about [mysqld\\_multi](#page-48-3):

• **Most important**: Before using [mysqld\\_multi](#page-48-3) be sure that you understand the meanings of the options that are passed to the [mysqld](#page-37-0) servers and why you would want to have separate [mysqld](#page-37-0) processes. Beware of the dangers of using multiple [mysqld](#page-37-0) servers with the same data directory. Use separate data directories, unless you know what you are doing. Starting multiple servers with the same data directory does not give you extra performance in a threaded system. See Section 7.8, "Running Multiple MySQL Instances on One Machine".

![](_page_52_Picture_2.jpeg)

### **Important**

Make sure that the data directory for each server is fully accessible to the Unix account that the specific [mysqld](#page-37-0) process is started as. Do not use the Unix root account for this, unless you know what you are doing. See Section 8.1.5, "How to Run MySQL as a Normal User".

• Make sure that the MySQL account used for stopping the [mysqld](#page-37-0) servers (with the [mysqladmin](#page-121-0) program) has the same user name and password for each server. Also, make sure that the account has the SHUTDOWN privilege. If the servers that you want to manage have different user names or passwords for the administrative accounts, you might want to create an account on each server that has the same user name and password. For example, you might set up a common multi\_admin account by executing the following commands for each server:

```
$> mysql -u root -S /tmp/mysql.sock -p
Enter password:
mysql> CREATE USER 'multi_admin'@'localhost' IDENTIFIED BY 'multipass';
mysql> GRANT SHUTDOWN ON *.* TO 'multi_admin'@'localhost';
```

See Section 8.2, "Access Control and Account Management". You have to do this for each [mysqld](#page-37-0) server. Change the connection parameters appropriately when connecting to each one. Note that the host name part of the account name must permit you to connect as multi\_admin from the host where you want to run [mysqld\\_multi](#page-48-3).

- The Unix socket file and the TCP/IP port number must be different for every [mysqld](#page-37-0). (Alternatively, if the host has multiple network addresses, you can set the bind\_address system variable to cause different servers to listen to different interfaces.)
- The [--pid-file](#page-43-3) option is very important if you are using [mysqld\\_safe](#page-37-1) to start [mysqld](#page-37-0) (for example, [--mysqld=mysqld\\_safe](#page-42-0)) Every [mysqld](#page-37-0) should have its own process ID file. The advantage of using [mysqld\\_safe](#page-37-1) instead of [mysqld](#page-37-0) is that [mysqld\\_safe](#page-37-1) monitors its [mysqld](#page-37-0) process and restarts it if the process terminates due to a signal sent using kill -9 or for other reasons, such as a segmentation fault.
- You might want to use the --user option for [mysqld](#page-37-0), but to do this you need to run the [mysqld\\_multi](#page-48-3) script as the Unix superuser (root). Having the option in the option file doesn't matter; you just get a warning if you are not the superuser and the [mysqld](#page-37-0) processes are started under your own Unix account.

The following example shows how you might set up an option file for use with [mysqld\\_multi](#page-48-3). The order in which the [mysqld](#page-37-0) programs are started or stopped depends on the order in which they appear in the option file. Group numbers need not form an unbroken sequence. The first and fifth [mysqldN] groups were intentionally omitted from the example to illustrate that you can have "gaps" in the option file. This gives you more flexibility.

```
# This is an example of a my.cnf file for mysqld_multi.
# Usually this file is located in home dir ~/.my.cnf or /etc/my.cnf
[mysqld_multi]
mysqld = /usr/local/mysql/bin/mysqld_safe
mysqladmin = /usr/local/mysql/bin/mysqladmin
user = multi_admin
password = my_password
[mysqld2]
socket = /tmp/mysql.sock2
```

```
port = 3307
pid-file = /usr/local/mysql/data2/hostname.pid2
datadir = /usr/local/mysql/data2
language = /usr/local/mysql/share/mysql/english
user = unix_user1
[mysqld3]
mysqld = /path/to/mysqld_safe
ledir = /path/to/mysqld-binary/
mysqladmin = /path/to/mysqladmin
socket = /tmp/mysql.sock3
port = 3308
pid-file = /usr/local/mysql/data3/hostname.pid3
datadir = /usr/local/mysql/data3
language = /usr/local/mysql/share/mysql/swedish
user = unix_user2
[mysqld4]
socket = /tmp/mysql.sock4
port = 3309
pid-file = /usr/local/mysql/data4/hostname.pid4
datadir = /usr/local/mysql/data4
language = /usr/local/mysql/share/mysql/estonia
user = unix_user3
[mysqld6]
socket = /tmp/mysql.sock6
port = 3311
pid-file = /usr/local/mysql/data6/hostname.pid6
datadir = /usr/local/mysql/data6
language = /usr/local/mysql/share/mysql/japanese
user = unix_user4
```

See Section 6.2.2.2, "Using Option Files".