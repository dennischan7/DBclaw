---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes some utilities that you may find useful when developing MySQL programs.

In shell scripts, you can use the [my\\_print\\_defaults](#page-26-0) program to parse option files and see what options would be used by a given program. The following example shows the output that [my\\_print\\_defaults](#page-26-0) might produce when asked to show the options found in the [client] and [mysql] groups:

```
$> my_print_defaults client mysql
--port=3306
--socket=/tmp/mysql.sock
--no-auto-rehash
```

Note for developers: Option file handling is implemented in the C client library simply by processing all options in the appropriate group or groups before any command-line arguments. This works well for programs that use the last instance of an option that is specified multiple times. If you have a C or C++ program that handles multiply specified options this way but that doesn't read option files, you need add only two lines to give it that capability. Check the source code of any of the standard MySQL clients to see how to do this.

Several other language interfaces to MySQL are based on the C client library, and some of them provide a way to access option file contents. These include Perl and Python. For details, see the documentation for your preferred interface.

# <span id="page-25-0"></span>**6.7.1 mysql\_config — Display Options for Compiling Clients**

[mysql\\_config](#page-25-0) provides you with useful information for compiling your MySQL client and connecting it to MySQL. It is a shell script, so it is available only on Unix and Unix-like systems.

![](_page_25_Picture_11.jpeg)

#### **Note**

pkg-config can be used as an alternative to [mysql\\_config](#page-25-0) for obtaining information such as compiler flags or link libraries required to compile MySQL applications. For more information, see [Building C API Client Programs Using](https://dev.mysql.com/doc/c-api/8.4/en/c-api-building-clients-pkg-config.md) [pkg-config](https://dev.mysql.com/doc/c-api/8.4/en/c-api-building-clients-pkg-config.md).

[mysql\\_config](#page-25-0) supports the following options.

<span id="page-25-1"></span>• [--cflags](#page-25-1)

C Compiler flags to find include files and critical compiler flags and defines used when compiling the libmysqlclient library. The options returned are tied to the specific compiler that was used when the library was created and might clash with the settings for your own compiler. Use [--include](#page-25-2) for more portable options that contain only include paths.

<span id="page-25-3"></span>• [--cxxflags](#page-25-3)

Like [--cflags](#page-25-1), but for C++ compiler flags.

<span id="page-25-2"></span>• [--include](#page-25-2)

Compiler options to find MySQL include files.

<span id="page-25-4"></span>• [--libs](#page-25-4)

Libraries and options required to link with the MySQL client library.

<span id="page-26-1"></span>• [--libs\\_r](#page-26-1)

Libraries and options required to link with the thread-safe MySQL client library. In MySQL 8.4, all client libraries are thread-safe, so this option need not be used. The [--libs](#page-25-4) option can be used in all cases.

<span id="page-26-2"></span>• [--plugindir](#page-26-2)

The default plugin directory path name, defined when configuring MySQL.

<span id="page-26-3"></span>• [--port](#page-26-3)

The default TCP/IP port number, defined when configuring MySQL.

<span id="page-26-4"></span>• [--socket](#page-26-4)

The default Unix socket file, defined when configuring MySQL.

<span id="page-26-5"></span>• [--variable=](#page-26-5)var\_name

Display the value of the named configuration variable. Permitted var\_name values are pkgincludedir (the header file directory), pkglibdir (the library directory), and plugindir (the plugin directory).

<span id="page-26-6"></span>• [--version](#page-26-6)

Version number for the MySQL distribution.

If you invoke [mysql\\_config](#page-25-0) with no options, it displays a list of all options that it supports, and their values:

```
$> mysql_config
Usage: ./mysql_config [OPTIONS]
Compiler: GNU 10.4.0
Options:
 --cflags [-I/usr/local/mysql/include/mysql]
 --cxxflags [-I/usr/local/mysql/include/mysql]
 --include [-I/usr/local/mysql/include/mysql]
 --libs [-L/usr/local/mysql/lib/mysql -lmysqlclient -lpthread -ldl 
 -lssl -lcrypto -lresolv -lm -lrt]
 --libs_r [-L/usr/local/mysql/lib/mysql -lmysqlclient -lpthread -ldl 
 -lssl -lcrypto -lresolv -lm -lrt]
 --plugindir [/usr/local/mysql/lib/plugin]
 --socket [/tmp/mysql.sock]
 --port [3306]
 --version [8.4.0]
 --variable=VAR VAR is one of:
 pkgincludedir [/usr/local/mysql/include]
 pkglibdir [/usr/local/mysql/lib]
 plugindir [/usr/local/mysql/lib/plugin]
```

You can use [mysql\\_config](#page-25-0) within a command line using backticks to include the output that it produces for particular options. For example, to compile and link a MySQL client program, use [mysql\\_config](#page-25-0) as follows:

```
gcc -c `mysql_config --cflags` progname.c
gcc -o progname progname.o `mysql_config --libs`
```

# <span id="page-26-0"></span>**6.7.2 my\_print\_defaults — Display Options from Option Files**

[my\\_print\\_defaults](#page-26-0) displays the options that are present in option groups of option files. The output indicates what options are used by programs that read the specified option groups. For example, the mysqlcheck program reads the [mysqlcheck] and [client] option groups. To see what options are present in those groups in the standard option files, invoke [my\\_print\\_defaults](#page-26-0) like this:

```
$> my_print_defaults mysqlcheck client
--user=myusername
--password=password
--host=localhost
```

The output consists of options, one per line, in the form that they would be specified on the command line.

[my\\_print\\_defaults](#page-26-0) supports the following options.

<span id="page-27-0"></span>• [--help](#page-27-0), -?

Display a help message and exit.

<span id="page-27-1"></span>• [--config-file=](#page-27-1)file\_name, [--defaults-file=](#page-27-1)file\_name, -c file\_name

Read only the given option file.

<span id="page-27-2"></span>• --debug=[debug\\_options](#page-27-2), -# debug\_options

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/my\_print\_defaults.trace.

<span id="page-27-3"></span>• [--defaults-extra-file=](#page-27-3)file\_name, [--extra-file=](#page-27-3)file\_name, -e file\_name

Read this option file after the global option file but (on Unix) before the user option file.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-27-4"></span>• [--defaults-group-suffix=](#page-27-4)suffix, -g suffix

In addition to the groups named on the command line, read groups that have the given suffix.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-27-5"></span>• [--login-path=](#page-27-5)name, -l name

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-27-6"></span>• [--no-login-paths](#page-27-6)

Skips reading options from the login path file.

See [--login-path](#page-27-5) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-27-7"></span>• [--no-defaults](#page-27-7), -n

Return an empty string.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-27-8"></span>• [--show](#page-27-8), -s

[my\\_print\\_defaults](#page-26-0) masks passwords by default. Use this option to display passwords as cleartext.

<span id="page-28-0"></span>• [--verbose](#page-28-0), -v

Verbose mode. Print more information about what the program does.

• [--version](#page-28-1), -V

Display version information and exit.

# <span id="page-28-1"></span>**6.8 Miscellaneous Programs**

# <span id="page-28-2"></span>**6.8.1 perror — Display MySQL Error Message Information**

[perror](#page-28-2) displays the error message for MySQL or operating system error codes. Invoke [perror](#page-28-2) like this:

```
perror [options] errorcode ...
```

[perror](#page-28-2) attempts to be flexible in understanding its arguments. For example, for the [ER\\_WRONG\\_VALUE\\_FOR\\_VAR](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_wrong_value_for_var) error, [perror](#page-28-2) understands any of these arguments: 1231, 001231, MY-1231, or MY-001231, or [ER\\_WRONG\\_VALUE\\_FOR\\_VAR](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_wrong_value_for_var).

```
$> perror 1231
MySQL error code MY-001231 (ER_WRONG_VALUE_FOR_VAR): Variable '%-.64s'
can't be set to the value of '%-.200s'
```

If an error number is in the range where MySQL and operating system errors overlap, [perror](#page-28-2) displays both error messages:

```
$> perror 1 13
OS error code 1: Operation not permitted
MySQL error code MY-000001: Can't create/write to file '%s' (OS errno %d - %s)
OS error code 13: Permission denied
MySQL error code MY-000013: Can't get stat of '%s' (OS errno %d - %s)
```

To obtain the error message for a MySQL Cluster error code, use the ndb\_perror utility.

The meaning of system error messages may be dependent on your operating system. A given error code may mean different things on different operating systems.

[perror](#page-28-2) supports the following options.

<span id="page-28-3"></span>• [--help](#page-28-3), [--info](#page-28-3), -I, -?

Display a help message and exit.

<span id="page-28-4"></span>• [--silent](#page-28-4), -s

Silent mode. Print only the error message.

<span id="page-28-5"></span>• [--verbose](#page-28-5), -v

Verbose mode. Print error code and message. This is the default behavior.

• [--version](#page-28-6), -V

Display version information and exit.

# <span id="page-28-6"></span>**6.9 Environment Variables**

This section lists environment variables that are used directly or indirectly by MySQL. Most of these can also be found in other places in this manual.

Options on the command line take precedence over values specified in option files and environment variables, and values in option files take precedence over values in environment variables. In many cases, it is preferable to use an option file instead of environment variables to modify the behavior of MySQL. See Section 6.2.2.2, "Using Option Files".

| Variable                           | Description                                                                                                                     |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| AUTHENTICATION_KERBEROS_CLIENT_LOG | Kerberos authentication logging level.                                                                                          |
| AUTHENTICATION_LDAP_CLIENT_LOG     | Client-side LDAP authentication logging level.                                                                                  |
| AUTHENTICATION_PAM_LOG             | PAM authentication plugin debug logging settings.                                                                               |
| CC                                 | The name of your C compiler (for running CMake).                                                                                |
| CXX                                | The name of your C++ compiler (for running<br>CMake).                                                                           |
| CC                                 | The name of your C compiler (for running CMake).                                                                                |
| DBI_USER                           | The default user name for Perl DBI.                                                                                             |
| DBI_TRACE                          | Trace options for Perl DBI.                                                                                                     |
| HOME                               | The default path for the mysql history file is<br>\$HOME/.mysql_history.                                                        |
| LD_RUN_PATH                        | Used to specify the location of<br>libmysqlclient.so.                                                                           |
| LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN   | Enable mysql_clear_password authentication<br>plugin; see Section 8.4.1.4, "Client-Side Cleartext<br>Pluggable Authentication". |
| LIBMYSQL_PLUGIN_DIR                | Directory in which to look for client plugins.                                                                                  |
| LIBMYSQL_PLUGINS                   | Client plugins to preload.                                                                                                      |
| MYSQL_DEBUG                        | Debug trace options when debugging.                                                                                             |
| MYSQL_GROUP_SUFFIX                 | Option group suffix value (like specifying<br>defaults-group-suffix).                                                           |
| MYSQL_HISTFILE                     | The path to the mysql history file. If this<br>variable is set, its value overrides the default for<br>\$HOME/.mysql_history.   |
| MYSQL_HISTIGNORE                   | Patterns specifying statements that mysql should<br>not log to \$HOME/.mysql_history, or syslog<br>ifsyslog is given.           |
| MYSQL_HOME                         | The path to the directory in which the server<br>specific my.cnf file resides.                                                  |
| MYSQL_HOST                         | The default host name used by the mysql<br>command-line client.                                                                 |
| MYSQL_PS1                          | The command prompt to use in the mysql<br>command-line client.                                                                  |
| MYSQL_PWD                          | The default password when connecting to<br>mysqld. Using this is insecure. See note following<br>table.                         |
| MYSQL_TCP_PORT                     | The default TCP/IP port number.                                                                                                 |
| MYSQL_TEST_LOGIN_FILE              | The name of the .mylogin.cnf login path file.                                                                                   |
| MYSQL_TEST_TRACE_CRASH             | Whether the test protocol trace plugin crashes<br>clients. See note following table.                                            |

| Variable               | Description                                                                               |
|------------------------|-------------------------------------------------------------------------------------------|
| MYSQL_TEST_TRACE_DEBUG | Whether the test protocol trace plugin produces<br>output. See note following table.      |
| MYSQL_UNIX_PORT        | The default Unix socket file name; used for<br>connections to localhost.                  |
| MYSQLX_TCP_PORT        | The X Plugin default TCP/IP port number.                                                  |
| MYSQLX_UNIX_PORT       | The X Plugin default Unix socket file name; used<br>for connections to localhost.         |
| NOTIFY_SOCKET          | Socket used by mysqld to communicate with<br>systemd.                                     |
| PATH                   | Used by the shell to find MySQL programs.                                                 |
| PKG_CONFIG_PATH        | Location of mysqlclient.pc pkg-config file.<br>See note following table.                  |
| TMPDIR                 | The directory in which temporary files are created.                                       |
| TZ                     | This should be set to your local time zone. See<br>Section B.3.3.7, "Time Zone Problems". |
| UMASK                  | The user-file creation mode when creating files.<br>See note following table.             |
| UMASK_DIR              | The user-directory creation mode when creating<br>directories. See note following table.  |
| USER                   | The default user name on Windows when<br>connecting to mysqld.                            |

For information about the mysql history file, see Section 6.5.1.3, "mysql Client Logging".

Use of MYSQL\_PWD to specify a MySQL password must be considered extremely insecure and should not be used. Some versions of ps include an option to display the environment of running processes. On some systems, if you set MYSQL\_PWD, your password is exposed to any other user who runs ps. Even on systems without such a version of ps, it is unwise to assume that there are no other methods by which users can examine process environments.

MYSQL\_PWD is deprecated as of MySQL 8.4; expect it to be removed in a future version of MySQL.

MYSQL\_TEST\_LOGIN\_FILE is the path name of the login path file (the file created by mysql\_config\_editor). If not set, the default value is %APPDATA%\MySQL\.mylogin.cnf directory on Windows and \$HOME/.mylogin.cnf on non-Windows systems. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

The MYSQL\_TEST\_TRACE\_DEBUG and MYSQL\_TEST\_TRACE\_CRASH variables control the test protocol trace client plugin, if MySQL is built with that plugin enabled. For more information, see [Using the Test](https://dev.mysql.com/doc/extending-mysql/8.4/en/test-protocol-trace-plugin.md) [Protocol Trace Plugin.](https://dev.mysql.com/doc/extending-mysql/8.4/en/test-protocol-trace-plugin.md)

The default UMASK and UMASK\_DIR values are 0640 and 0750, respectively. MySQL assumes that the value for UMASK or UMASK\_DIR is in octal if it starts with a zero. For example, setting UMASK=0600 is equivalent to UMASK=384 because 0600 octal is 384 decimal.

The UMASK and UMASK\_DIR variables, despite their names, are used as modes, not masks:

- If UMASK is set, mysqld uses (\$UMASK | 0600) as the mode for file creation, so that newly created files have a mode in the range from 0600 to 0666 (all values octal).
- If UMASK\_DIR is set, mysqld uses (\$UMASK\_DIR | 0700) as the base mode for directory creation, which then is AND-ed with ~(~\$UMASK & 0666), so that newly created directories have a mode in the range from 0700 to 0777 (all values octal). The AND operation may remove read and write permissions from the directory mode, but not execute permissions.

See also Section B.3.3.1, "Problems with File Permissions".

It may be necessary to set PKG\_CONFIG\_PATH if you use pkg-config for building MySQL programs. See [Building C API Client Programs Using pkg-config.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-building-clients-pkg-config.md)