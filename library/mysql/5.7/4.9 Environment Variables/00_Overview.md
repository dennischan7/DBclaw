---
source: MySQL 5.7 Reference
title: 00_Overview
---

This section lists environment variables that are used directly or indirectly by MySQL. Most of these can also be found in other places in this manual.

Options on the command line take precedence over values specified in option files and environment variables, and values in option files take precedence over values in environment variables. In many cases, it is preferable to use an option file instead of environment variables to modify the behavior of MySQL. See Section 4.2.2.2, "Using Option Files".

| Variable                            | Description                                                                                                                     |  |  |  |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|--|--|--|
| AUTHENTICATION_LDAP_CLIENT_LOG      | Client-side LDAP authentication logging level.                                                                                  |  |  |  |
| AUTHENTICATION_PAM_LOG              | PAM authentication plugin debug logging settings.                                                                               |  |  |  |
| CC                                  | The name of your C compiler (for running CMake).                                                                                |  |  |  |
| CXX                                 | The name of your C++ compiler (for running<br>CMake).                                                                           |  |  |  |
| CC                                  | The name of your C compiler (for running CMake).                                                                                |  |  |  |
| DBI_USER                            | The default user name for Perl DBI.                                                                                             |  |  |  |
| DBI_TRACE                           | Trace options for Perl DBI.                                                                                                     |  |  |  |
| HOME                                | The default path for the mysql history file is<br>\$HOME/.mysql_history.                                                        |  |  |  |
| LD_RUN_PATH                         | Used to specify the location of<br>libmysqlclient.so.                                                                           |  |  |  |
| LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN    | Enable mysql_clear_password authentication<br>plugin; see Section 6.4.1.6, "Client-Side Cleartext<br>Pluggable Authentication". |  |  |  |
| LIBMYSQL_PLUGIN_DIR                 | Directory in which to look for client plugins.                                                                                  |  |  |  |
| LIBMYSQL_PLUGINS                    | Client plugins to preload.                                                                                                      |  |  |  |
| MYSQL_DEBUG                         | Debug trace options when debugging.                                                                                             |  |  |  |
| MYSQL_GROUP_SUFFIX                  | Option group suffix value (like specifying<br>defaults-group-suffix).                                                           |  |  |  |
| MYSQL_HISTFILE                      | The path to the mysql history file. If this<br>variable is set, its value overrides the default for<br>\$HOME/.mysql_history.   |  |  |  |
| MYSQL_HISTIGNORE                    | Patterns specifying statements that mysql should<br>not log to \$HOME/.mysql_history, or syslog<br>ifsyslog is given.           |  |  |  |
| MYSQL_HOME                          | The path to the directory in which the server<br>specific my.cnf file resides.                                                  |  |  |  |
| MYSQL_HOST                          | The default host name used by the mysql<br>command-line client.                                                                 |  |  |  |
| MYSQL_OPENSSL_UDF_DH_BITS_THRESHOLD | Maximum key length for<br>create_dh_parameters(). See Section 6.6.2,                                                            |  |  |  |

| Variable                             | Description                                                                                                                                        |  |  |  |  |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|--|
|                                      | "MySQL Enterprise Encryption Usage and<br>Examples".                                                                                               |  |  |  |  |
| MYSQL_OPENSSL_UDF_DSA_BITS_THRESHOLD | Maximum DSA key length for<br>create_asymmetric_priv_key(). See<br>Section 6.6.2, "MySQL Enterprise Encryption<br>Usage and Examples".             |  |  |  |  |
| MYSQL_OPENSSL_UDF_RSA_BITS_THRESHOLD | Maximum RSA key length for<br>create_asymmetric_priv_key(). See<br>Section 6.6.2, "MySQL Enterprise Encryption<br>Usage and Examples".             |  |  |  |  |
| MYSQL_PS1                            | The command prompt to use in the mysql<br>command-line client.                                                                                     |  |  |  |  |
| MYSQL_PWD                            | The default password when connecting<br>to mysqld. Using this is insecure. See<br>Section 6.1.2.1, "End-User Guidelines for<br>Password Security". |  |  |  |  |
| MYSQL_TCP_PORT                       | The default TCP/IP port number.                                                                                                                    |  |  |  |  |
| MYSQL_TEST_LOGIN_FILE                | The name of the .mylogin.cnf login path file.                                                                                                      |  |  |  |  |
| MYSQL_TEST_TRACE_CRASH               | Whether the test protocol trace plugin crashes<br>clients. See note following table.                                                               |  |  |  |  |
| MYSQL_TEST_TRACE_DEBUG               | Whether the test protocol trace plugin produces<br>output. See note following table.                                                               |  |  |  |  |
| MYSQL_UNIX_PORT                      | The default Unix socket file name; used for<br>connections to localhost.                                                                           |  |  |  |  |
| MYSQLX_TCP_PORT                      | The X Plugin default TCP/IP port number.                                                                                                           |  |  |  |  |
| MYSQLX_UNIX_PORT                     | The X Plugin default Unix socket file name; used<br>for connections to localhost.                                                                  |  |  |  |  |
| PATH                                 | Used by the shell to find MySQL programs.                                                                                                          |  |  |  |  |
| PKG_CONFIG_PATH                      | Location of mysqlclient.pc pkg-config file.<br>See note following table.                                                                           |  |  |  |  |
| TMPDIR                               | The directory in which temporary files are created.                                                                                                |  |  |  |  |
| TZ                                   | This should be set to your local time zone. See<br>Section B.3.3.7, "Time Zone Problems".                                                          |  |  |  |  |
| UMASK                                | The user-file creation mode when creating files.<br>See note following table.                                                                      |  |  |  |  |
| UMASK_DIR                            | The user-directory creation mode when creating<br>directories. See note following table.                                                           |  |  |  |  |
| USER                                 | The default user name on Windows when<br>connecting to mysqld.                                                                                     |  |  |  |  |

For information about the mysql history file, see Section 4.5.1.3, "mysql Client Logging".

MYSQL\_TEST\_LOGIN\_FILE is the path name of the login path file (the file created by mysql\_config\_editor). If not set, the default value is %APPDATA%\MySQL\.mylogin.cnf directory on Windows and \$HOME/.mylogin.cnf on non-Windows systems. See Section 4.6.6, "mysql\_config\_editor — MySQL Configuration Utility".

The MYSQL\_TEST\_TRACE\_DEBUG and MYSQL\_TEST\_TRACE\_CRASH variables control the test protocol trace client plugin, if MySQL is built with that plugin enabled. For more information, see [Using the Test](https://dev.mysql.com/doc/extending-mysql/5.7/en/test-protocol-trace-plugin.md) [Protocol Trace Plugin.](https://dev.mysql.com/doc/extending-mysql/5.7/en/test-protocol-trace-plugin.md)

The default UMASK and UMASK\_DIR values are 0640 and 0750, respectively. MySQL assumes that the value for UMASK or UMASK\_DIR is in octal if it starts with a zero. For example, setting UMASK=0600 is equivalent to UMASK=384 because 0600 octal is 384 decimal.

The UMASK and UMASK\_DIR variables, despite their names, are used as modes, not masks:

- If UMASK is set, mysqld uses (\$UMASK | 0600) as the mode for file creation, so that newly created files have a mode in the range from 0600 to 0666 (all values octal).
- If UMASK\_DIR is set, mysqld uses (\$UMASK\_DIR | 0700) as the base mode for directory creation, which then is AND-ed with ~(~\$UMASK & 0666), so that newly created directories have a mode in the range from 0700 to 0777 (all values octal). The AND operation may remove read and write permissions from the directory mode, but not execute permissions.

See also Section B.3.3.1, "Problems with File Permissions".

It may be necessary to set PKG\_CONFIG\_PATH if you use pkg-config for building MySQL programs. See [Building C API Client Programs Using pkg-config.](https://dev.mysql.com/doc/c-api/5.7/en/c-api-building-clients-pkg-config.md)