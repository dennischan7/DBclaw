---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section provides information about techniques for more effective use of [mysql](#page-77-0) and about [mysql](#page-77-0) operational behavior.

- [Input-Line Editing](#page-118-1)
- [Disabling Interactive History](#page-118-0)
- [Unicode Support on Windows](#page-118-2)
- [Displaying Query Results Vertically](#page-119-1)
- [Using Safe-Updates Mode \(--safe-updates\)](#page-119-0)
- [Disabling mysql Auto-Reconnect](#page-120-0)
- [mysql Client Parser Versus Server Parser](#page-121-1)

### <span id="page-118-1"></span>**Input-Line Editing**

[mysql](#page-77-0) supports input-line editing, which enables you to modify the current input line in place or recall previous input lines. For example, the **left-arrow** and **right-arrow** keys move horizontally within the current input line, and the **up-arrow** and **down-arrow** keys move up and down through the set of previously entered lines. **Backspace** deletes the character before the cursor and typing new characters enters them at the cursor position. To enter the line, press **Enter**.

On Windows, the editing key sequences are the same as supported for command editing in console windows. On Unix, the key sequences depend on the input library used to build [mysql](#page-77-0) (for example, the libedit or readline library).

Documentation for the libedit and readline libraries is available online. To change the set of key sequences permitted by a given input library, define key bindings in the library startup file. This is a file in your home directory: .editrc for libedit and .inputrc for readline.

For example, in libedit, **Control+W** deletes everything before the current cursor position and **Control+U** deletes the entire line. In readline, **Control+W** deletes the word before the cursor and **Control+U** deletes everything before the current cursor position. If [mysql](#page-77-0) was built using libedit, a user who prefers the readline behavior for these two keys can put the following lines in the .editrc file (creating the file if necessary):

```
bind "^W" ed-delete-prev-word
bind "^U" vi-kill-line-prev
```

To see the current set of key bindings, temporarily put a line that says only bind at the end of .editrc. [mysql](#page-77-0) shows the bindings when it starts.

### <span id="page-118-0"></span>**Disabling Interactive History**

The **up-arrow** key enables you to recall input lines from current and previous sessions. In cases where a console is shared, this behavior may be unsuitable. [mysql](#page-77-0) supports disabling the interactive history partially or fully, depending on the host platform.

On Windows, the history is stored in memory. **Alt+F7** deletes all input lines stored in memory for the current history buffer. It also deletes the list of sequential numbers in front of the input lines displayed with **F7** and recalled (by number) with **F9**. New input lines entered after you press **Alt+F7** repopulate the current history buffer. Clearing the buffer does not prevent logging to the Windows Event Viewer, if the [--syslog](#page-104-0) option was used to start [mysql](#page-77-0). Closing the console window also clears the current history buffer.

To disable interactive history on Unix, first delete the .mysql\_history file, if it exists (previous entries are recalled otherwise). Then start [mysql](#page-77-0) with the --histignore="\*" option to ignore all new input lines. To re-enable the recall (and logging) behavior, restart [mysql](#page-77-0) without the option.

If you prevent the .mysql\_history file from being created (see [Controlling the History File](#page-114-1)) and use --histignore="\*" to start the [mysql](#page-77-0) client, the interactive history recall facility is disabled fully. Alternatively, if you omit the [--histignore](#page-92-2) option, you can recall the input lines entered during the current session.

### <span id="page-118-2"></span>**Unicode Support on Windows**

Windows provides APIs based on UTF-16LE for reading from and writing to the console; the [mysql](#page-77-0) client for Windows is able to use these APIs. The Windows installer creates an item in the MySQL menu named MySQL command line client - Unicode. This item invokes the [mysql](#page-77-0) client with properties set to communicate through the console to the MySQL server using Unicode.

To take advantage of this support manually, run [mysql](#page-77-0) within a console that uses a compatible Unicode font and set the default character set to a Unicode character set that is supported for communication with the server:

1. Open a console window.

- 2. Go to the console window properties, select the font tab, and choose Lucida Console or some other compatible Unicode font. This is necessary because console windows start by default using a DOS raster font that is inadequate for Unicode.
- 3. Execute [mysql.exe](#page-77-0) with the [--default-character-set=utf8mb4](#page-89-0) (or utf8mb3) option. This option is necessary because utf16le is one of the character sets that cannot be used as the client character set. See Impermissible Client Character Sets.

With those changes, [mysql](#page-77-0) uses the Windows APIs to communicate with the console using UTF-16LE, and communicate with the server using UTF-8. (The menu item mentioned previously sets the font and character set as just described.)

To avoid those steps each time you run [mysql](#page-77-0), you can create a shortcut that invokes [mysql.exe](#page-77-0). The shortcut should set the console font to Lucida Console or some other compatible Unicode font, and pass the [--default-character-set=utf8mb4](#page-89-0) (or utf8mb3) option to [mysql.exe](#page-77-0).

Alternatively, create a shortcut that only sets the console font, and set the character set in the [mysql] group of your my.ini file:

```
[mysql]
default-character-set=utf8mb4 # or utf8mb3
```

### <span id="page-119-1"></span>**Displaying Query Results Vertically**

Some query results are much more readable when displayed vertically, instead of in the usual horizontal table format. Queries can be displayed vertically by terminating the query with \G instead of a semicolon. For example, longer text values that include newlines often are much easier to read with vertical output:

```
mysql> SELECT * FROM mails WHERE LENGTH(txt) < 300 LIMIT 300,1\G
*************************** 1. row ***************************
 msg_nro: 3068
 date: 2000-03-01 23:29:50
time_zone: +0200
mail_from: Jones
 reply: jones@example.com
 mail_to: "John Smith" <smith@example.com>
 sbj: UTF-8
 txt: >>>>> "John" == John Smith writes:
John> Hi. I think this is a good idea. Is anyone familiar
John> with UTF-8 or Unicode? Otherwise, I'll put this on my
John> TODO list and see what happens.
Yes, please do that.
Regards,
Jones
 file: inbox-jani-1
 hash: 190402944
1 row in set (0.09 sec)
```

### <span id="page-119-0"></span>**Using Safe-Updates Mode (--safe-updates)**

For beginners, a useful startup option is [--safe-updates](#page-101-0) (or [--i-am-a-dummy](#page-101-0), which has the same effect). Safe-updates mode is helpful for cases when you might have issued an UPDATE or DELETE statement but forgotten the WHERE clause indicating which rows to modify. Normally, such statements update or delete all rows in the table. With [--safe-updates](#page-101-0), you can modify rows only by specifying the key values that identify them, or a LIMIT clause, or both. This helps prevent accidents. Safe-updates mode also restricts SELECT statements that produce (or are estimated to produce) very large result sets.

The [--safe-updates](#page-101-0) option causes [mysql](#page-77-0) to execute the following statement when it connects to the MySQL server, to set the session values of the sql\_safe\_updates, sql\_select\_limit, and max\_join\_size system variables:

```
SET sql_safe_updates=1, sql_select_limit=1000, max_join_size=1000000;
```

The SET statement affects statement processing as follows:

• Enabling sql\_safe\_updates causes UPDATE and DELETE statements to produce an error if they do not specify a key constraint in the WHERE clause, or provide a LIMIT clause, or both. For example:

```
UPDATE tbl_name SET not_key_column=val WHERE key_column=val;
UPDATE tbl_name SET not_key_column=val LIMIT 1;
```

- Setting sql\_select\_limit to 1,000 causes the server to limit all SELECT result sets to 1,000 rows unless the statement includes a LIMIT clause.
- Setting max\_join\_size to 1,000,000 causes multiple-table SELECT statements to produce an error if the server estimates it must examine more than 1,000,000 row combinations.

To specify result set limits different from 1,000 and 1,000,000, you can override the defaults by using the [--select-limit](#page-101-1) and [--max-join-size](#page-95-1) options when you invoke [mysql](#page-77-0):

```
mysql --safe-updates --select-limit=500 --max-join-size=10000
```

It is possible for UPDATE and DELETE statements to produce an error in safe-updates mode even with a key specified in the WHERE clause, if the optimizer decides not to use the index on the key column:

- Range access on the index cannot be used if memory usage exceeds that permitted by the range\_optimizer\_max\_mem\_size system variable. The optimizer then falls back to a table scan. See Limiting Memory Use for Range Optimization.
- If key comparisons require type conversion, the index may not be used (see Section 10.3.1, "How MySQL Uses Indexes"). Suppose that an indexed string column c1 is compared to a numeric value using WHERE c1 = 2222. For such comparisons, the string value is converted to a number and the operands are compared numerically (see Section 14.3, "Type Conversion in Expression Evaluation"), preventing use of the index. If safe-updates mode is enabled, an error occurs.

As of MySQL 8.0.13, safe-updates mode also includes these behaviors:

- EXPLAIN with UPDATE and DELETE statements does not produce safe-updates errors. This enables use of EXPLAIN plus SHOW WARNINGS to see why an index is not used, which can be helpful in cases such as when a range\_optimizer\_max\_mem\_size violation or type conversion occurs and the optimizer does not use an index even though a key column was specified in the WHERE clause.
- When a safe-updates error occurs, the error message includes the first diagnostic that was produced, to provide information about the reason for failure. For example, the message may indicate that the range\_optimizer\_max\_mem\_size value was exceeded or type conversion occurred, either of which can preclude use of an index.
- For multiple-table deletes and updates, an error is produced with safe updates enabled only if any target table uses a table scan.

### <span id="page-120-0"></span>**Disabling mysql Auto-Reconnect**

If the [mysql](#page-77-0) client loses its connection to the server while sending a statement, it immediately and automatically tries to reconnect once to the server and send the statement again. However, even if [mysql](#page-77-0) succeeds in reconnecting, your first connection has ended and all your previous session objects and settings are lost: temporary tables, the autocommit mode, and user-defined and session variables. Also, any current transaction rolls back. This behavior may be dangerous for you, as in the following example where the server was shut down and restarted between the first and second statements without you knowing it:

```
mysql> SET @a=1;
```

```
Query OK, 0 rows affected (0.05 sec)
mysql> INSERT INTO t VALUES(@a);
ERROR 2006: MySQL server has gone away
No connection. Trying to reconnect...
Connection id: 1
Current database: test
Query OK, 1 row affected (1.30 sec)
mysql> SELECT * FROM t;
+------+
| a |
+------+
| NULL |
+------+
1 row in set (0.05 sec)
```

The @a user variable has been lost with the connection, and after the reconnection it is undefined. If it is important to have [mysql](#page-77-0) terminate with an error if the connection has been lost, you can start the [mysql](#page-77-0) client with the [--skip-reconnect](#page-100-1) option.

For more information about auto-reconnect and its effect on state information when a reconnection occurs, see [Automatic Reconnection Control](https://dev.mysql.com/doc/c-api/8.0/en/c-api-auto-reconnect.md).

### <span id="page-121-1"></span>**mysql Client Parser Versus Server Parser**

The [mysql](#page-77-0) client uses a parser on the client side that is not a duplicate of the complete parser used by the [mysqld](#page-37-0) server on the server side. This can lead to differences in treatment of certain constructs. Examples:

• The server parser treats strings delimited by " characters as identifiers rather than as plain strings if the ANSI\_QUOTES SQL mode is enabled.

The [mysql](#page-77-0) client parser does not take the ANSI\_QUOTES SQL mode into account. It treats strings delimited by ", ', and ` characters the same, regardless of whether ANSI\_QUOTES is enabled.

• Within /\*! ... \*/ and /\*+ ... \*/ comments, the [mysql](#page-77-0) client parser interprets short-form [mysql](#page-77-0) commands. The server parser does not interpret them because these commands have no meaning on the server side.

If it is desirable for [mysql](#page-77-0) not to interpret short-form commands within comments, a partial workaround is to use the [--binary-mode](#page-84-0) option, which causes all [mysql](#page-77-0) commands to be disabled except \C and \d in noninteractive mode (for input piped to [mysql](#page-77-0) or loaded using the source command).

# <span id="page-121-0"></span>**6.5.2 mysqladmin — A MySQL Server Administration Program**

[mysqladmin](#page-121-0) is a client for performing administrative operations. You can use it to check the server's configuration and current status, to create and drop databases, and more.

Invoke [mysqladmin](#page-121-0) like this:

```
mysqladmin [options] command [command-arg] [command [command-arg]] ...
```

[mysqladmin](#page-121-0) supports the following commands. Some of the commands take an argument following the command name.

• create db\_name

Create a new database named db\_name.

• debug

Prior to MySQL 8.0.20, tell the server to write debug information to the error log. The connected user must have the SUPER privilege. Format and content of this information is subject to change.

This includes information about the Event Scheduler. See Section 27.4.5, "Event Scheduler Status".

• drop db\_name

Delete the database named db\_name and all its tables.

• extended-status

Display the server status variables and their values.

• flush-hosts

Flush all information in the host cache. See Section 7.1.12.3, "DNS Lookups and the Host Cache".

• flush-logs [log\_type ...]

Flush all logs.

The [mysqladmin flush-logs](#page-121-0) command permits optional log types to be given, to specify which logs to flush. Following the flush-logs command, you can provide a space-separated list of one or more of the following log types: binary, engine, error, general, relay, slow. These correspond to the log types that can be specified for the FLUSH LOGS SQL statement.

• flush-privileges

Reload the grant tables (same as reload).

• flush-status

Clear status variables.

• flush-tables

Flush all tables.

• flush-threads

Flush the thread cache.

• kill id,id,...

Kill server threads. If multiple thread ID values are given, there must be no spaces in the list.

To kill threads belonging to other users, the connected user must have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

• password new\_password

Set a new password. This changes the password to new\_password for the account that you use with [mysqladmin](#page-121-0) for connecting to the server. Thus, the next time you invoke [mysqladmin](#page-121-0) (or any other client program) using the same account, you must specify the new password.

![](_page_122_Picture_25.jpeg)

### **Warning**

Setting a password using [mysqladmin](#page-121-0) should be considered insecure. On some systems, your password becomes visible to system status programs such as ps that may be invoked by other users to display command lines. MySQL clients typically overwrite the command-line password argument with zeros during their initialization sequence. However, there is still a brief interval during which the value is visible. Also, on some systems this overwriting strategy is ineffective and the password remains visible to ps. (SystemV Unix systems and perhaps others are subject to this problem.)

If the new\_password value contains spaces or other characters that are special to your command interpreter, you need to enclose it within quotation marks. On Windows, be sure to use double quotation marks rather than single quotation marks; single quotation marks are not stripped from the password, but rather are interpreted as part of the password. For example:

mysqladmin password "my new password"

The new password can be omitted following the password command. In this case, [mysqladmin](#page-121-0) prompts for the password value, which enables you to avoid specifying the password on the command line. Omitting the password value should be done only if password is the final command on the [mysqladmin](#page-121-0) command line. Otherwise, the next argument is taken as the password.

![](_page_123_Picture_5.jpeg)

### **Caution**

Do not use this command used if the server was started with the --skipgrant-tables option. No password change is applied. This is true even if you precede the password command with flush-privileges on the same command line to re-enable the grant tables because the flush operation occurs after you connect. However, you can use [mysqladmin](#page-121-0) [flush-privileges](#page-121-0) to re-enable the grant tables and then use a separate [mysqladmin password](#page-121-0) command to change the password.

• ping

Check whether the server is available. The return status from [mysqladmin](#page-121-0) is 0 if the server is running, 1 if it is not. This is 0 even in case of an error such as Access denied, because this means that the server is running but refused the connection, which is different from the server not running.

• processlist

Show a list of active server threads. This is like the output of the SHOW PROCESSLIST statement. If the [--verbose](#page-136-0) option is given, the output is like that of SHOW FULL PROCESSLIST. (See Section 15.7.7.29, "SHOW PROCESSLIST Statement".)

• reload

Reload the grant tables.

• refresh

Flush all tables and close and open log files.

• shutdown

Stop the server.

• start-replica

Start replication on a replica server. Use this command from MySQL 8.0.26.

• start-slave

Start replication on a replica server. Use this command before MySQL 8.0.26.

• status

Display a short server status message.

• stop-replica

Stop replication on a replica server. Use this command from MySQL 8.0.26.

• stop-slave

Stop replication on a replica server. Use this command before MySQL 8.0.26.

• variables

Display the server system variables and their values.

• version

Display version information from the server.

All commands can be shortened to any unique prefix. For example:

```
$> mysqladmin proc stat
+----+-------+-----------+----+---------+------+-------+------------------+
| Id | User | Host | db | Command | Time | State | Info |
+----+-------+-----------+----+---------+------+-------+------------------+
| 51 | jones | localhost | | Query | 0 | | show processlist |
+----+-------+-----------+----+---------+------+-------+------------------+
Uptime: 1473624 Threads: 1 Questions: 39487
Slow queries: 0 Opens: 541 Flush tables: 1
Open tables: 19 Queries per second avg: 0.0268
```

The [mysqladmin status](#page-121-0) command result displays the following values:

• Uptime

The number of seconds the MySQL server has been running.

• Threads

The number of active threads (clients).

• Questions

The number of questions (queries) from clients since the server was started.

• Slow queries

The number of queries that have taken more than long\_query\_time seconds. See Section 7.4.5, "The Slow Query Log".

• Opens

The number of tables the server has opened.

• Flush tables

The number of flush-\*, refresh, and reload commands the server has executed.

• Open tables

The number of tables that currently are open.

If you execute [mysqladmin shutdown](#page-121-0) when connecting to a local server using a Unix socket file, [mysqladmin](#page-121-0) waits until the server's process ID file has been removed, to ensure that the server has stopped properly.

[mysqladmin](#page-121-0) supports the following options, which can be specified on the command line or in the [mysqladmin] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.13 mysqladmin Options**

| Option Name             | Description                                                                       | Deprecated |
|-------------------------|-----------------------------------------------------------------------------------|------------|
| bind-address            | Use specified network interface<br>to connect to MySQL Server                     |            |
| character-sets-dir      | Directory where character sets<br>can be found                                    |            |
| compress                | Compress all information sent<br>between client and server                        | Yes        |
| compression-algorithms  | Permitted compression<br>algorithms for connections to<br>server                  |            |
| connect-timeout         | Number of seconds before<br>connection timeout                                    |            |
| count                   | Number of iterations to make for<br>repeated command execution                    |            |
| debug                   | Write debugging log                                                               |            |
| debug-check             | Print debugging information<br>when program exits                                 |            |
| debug-info              | Print debugging information,<br>memory, and CPU statistics<br>when program exits  |            |
| default-auth            | Authentication plugin to use                                                      |            |
| default-character-set   | Specify default character set                                                     |            |
| defaults-extra-file     | Read named option file in<br>addition to usual option files                       |            |
| defaults-file           | Read only named option file                                                       |            |
| defaults-group-suffix   | Option group suffix value                                                         |            |
| enable-cleartext-plugin | Enable cleartext authentication<br>plugin                                         |            |
| force                   | Continue even if an SQL error<br>occurs                                           |            |
| get-server-public-key   | Request RSA public key from<br>server                                             |            |
| help                    | Display help message and exit                                                     |            |
| host                    | Host on which MySQL server is<br>located                                          |            |
| login-path              | Read login path options<br>from .mylogin.cnf                                      |            |
| no-beep                 | Do not beep when errors occur                                                     |            |
| no-defaults             | Read no option files                                                              |            |
| password                | Password to use when<br>connecting to server                                      |            |
| password1               | First multifactor authentication<br>password to use when<br>connecting to server  |            |
| password2               | Second multifactor authentication<br>password to use when<br>connecting to server |            |

| Option Name             | Description                                                                                         | Deprecated |
|-------------------------|-----------------------------------------------------------------------------------------------------|------------|
| password3               | Third multifactor authentication<br>password to use when<br>connecting to server                    |            |
| pipe                    | Connect to server using named<br>pipe (Windows only)                                                |            |
| plugin-dir              | Directory where plugins are<br>installed                                                            |            |
| port                    | TCP/IP port number for<br>connection                                                                |            |
| print-defaults          | Print default options                                                                               |            |
| protocol                | Transport protocol to use                                                                           |            |
| relative                | Show the difference between<br>the current and previous values<br>when used with thesleep<br>option |            |
| server-public-key-path  | Path name to file containing RSA<br>public key                                                      |            |
| shared-memory-base-name | Shared-memory name for<br>shared-memory connections<br>(Windows only)                               |            |
| show-warnings           | Show warnings after statement<br>execution                                                          |            |
| shutdown-timeout        | The maximum number of<br>seconds to wait for server<br>shutdown                                     |            |
| silent                  | Silent mode                                                                                         |            |
| sleep                   | Execute commands repeatedly,<br>sleeping for delay seconds in<br>between                            |            |
| socket                  | Unix socket file or Windows<br>named pipe to use                                                    |            |
| ssl-ca                  | File that contains list of trusted<br>SSL Certificate Authorities                                   |            |
| ssl-capath              | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files                   |            |
| ssl-cert                | File that contains X.509<br>certificate                                                             |            |
| ssl-cipher              | Permissible ciphers for<br>connection encryption                                                    |            |
| ssl-crl                 | File that contains certificate<br>revocation lists                                                  |            |
| ssl-crlpath             | Directory that contains certificate<br>revocation-list files                                        |            |
| ssl-fips-mode           | Whether to enable FIPS mode<br>on client side                                                       | Yes        |
| ssl-key                 | File that contains X.509 key                                                                        |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| ssl-mode                                     | Desired security state of<br>connection to server                                 |            |
| ssl-session-data                             | File that contains SSL session<br>data                                            |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                        |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                     |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                            |            |
| user                                         | MySQL user name to use when<br>connecting to server                               |            |
| verbose                                      | Verbose mode                                                                      |            |
| version                                      | Display version information and<br>exit                                           |            |
| vertical                                     | Print query output rows vertically<br>(one line per column value)                 |            |
| wait                                         | If the connection cannot be<br>established, wait and retry<br>instead of aborting |            |
| zstd-compression-level                       | Compression level for<br>connections to server that use<br>zstd compression       |            |

<span id="page-127-3"></span>• [--help](#page-127-3), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-127-0"></span>• [--bind-address=](#page-127-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-127-1"></span>• [--character-sets-dir=](#page-127-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-127-2"></span>• [--compress](#page-127-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |

| Type          | Boolean |
|---------------|---------|
| Default Value | OFF     |

Compress all information sent between the client and the server if possible. See [Section 6.2.8,](#page-32-0) ["Connection Compression Control".](#page-32-0)

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

<span id="page-128-0"></span>• [--compression-algorithms=](#page-128-0)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

<span id="page-128-1"></span>• [--connect-timeout=](#page-128-1)value

| Command-Line Format | connect-timeout=value |
|---------------------|-----------------------|
| Type                | Numeric               |
| Default Value       | 43200                 |

The maximum number of seconds before connection timeout. The default value is 43200 (12 hours).

<span id="page-128-2"></span>• [--count=](#page-128-2)N, -c N

| Command-Line Format | count=# |
|---------------------|---------|
|---------------------|---------|

The number of iterations to make for repeated command execution if the [--sleep](#page-134-4) option is given.

<span id="page-128-3"></span>• --debug[=[debug\\_options](#page-128-3)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |

| Default Value | d:t:o,/tmp/mysqladmin.trace |
|---------------|-----------------------------|
|---------------|-----------------------------|

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysqladmin.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-129-0"></span>• [--debug-check](#page-129-0)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-129-1"></span>• [--debug-info](#page-129-1)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-129-2"></span>• [--default-auth=](#page-129-2)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

### <span id="page-129-3"></span>• [--default-character-set=](#page-129-3)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

<span id="page-129-4"></span>• [--defaults-extra-file=](#page-129-4)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|

| Type | File name |
|------|-----------|
|------|-----------|

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-130-0"></span>• [--defaults-file=](#page-130-0)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with [--defaults-file](#page-1-0), client programs read .mylogin.cnf.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-130-1"></span>• [--defaults-group-suffix=](#page-130-1)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqladmin](#page-121-0) normally reads the [client] and [mysqladmin] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-130-1), [mysqladmin](#page-121-0) also reads the [client\_other] and [mysqladmin\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-130-2"></span>• [--enable-cleartext-plugin](#page-130-2)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-130-3"></span>• [--force](#page-130-3), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Do not ask for confirmation for the drop db\_name command. With multiple commands, continue even if an error occurs.

<span id="page-130-4"></span>• [--get-server-public-key](#page-130-4)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|

| Type | Boolean |
|------|---------|
|------|---------|

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-133-5)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-130-4).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-131-0"></span>• --host=[host\\_name](#page-131-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-131-1"></span>• [--login-path=](#page-131-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-131-2"></span>• [--no-beep](#page-131-2), -b

| Command-Line Format | no-beep |
|---------------------|---------|
|---------------------|---------|

Suppress the warning beep that is emitted by default for errors such as a failure to connect to the server.

<span id="page-131-3"></span>• [--no-defaults](#page-131-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-131-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-131-3) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-132-0"></span>• [--password\[=](#page-132-0)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqladmin](#page-121-0) prompts for one. If given, there must be no space between [-](#page-132-0) [password=](#page-132-0) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqladmin](#page-121-0) should not prompt for one, use the [--skip-password](#page-132-0) option.

<span id="page-132-1"></span>• [--password1\[=](#page-132-1)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysql](#page-77-0) prompts for one. If given, there must be no space between [--password1=](#page-132-1) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqladmin](#page-121-0) should not prompt for one, use the [--skip-password1](#page-132-1) option.

[--password1](#page-132-1) and [--password](#page-132-0) are synonymous, as are [--skip-password1](#page-97-2) and [--skip](#page-97-1)[password](#page-97-1).

<span id="page-132-2"></span>• [--password2\[=](#page-132-2)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-132-1); see the description of that option for details.

<span id="page-132-3"></span>• [--password3\[=](#page-132-3)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-132-1); see the description of that option for details.

<span id="page-132-4"></span>• [--pipe](#page-132-4), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-133-0"></span>• [--plugin-dir=](#page-133-0)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-129-2) option is used to specify an authentication plugin but [mysqladmin](#page-121-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-133-1"></span>• --port=[port\\_num](#page-133-1), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-133-2"></span>• [--print-defaults](#page-133-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-133-3"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-133-3)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see [Section 6.2.7, "Connection Transport Protocols".](#page-31-0)

<span id="page-133-4"></span>• [--relative](#page-133-4), -r

| Command-Line Format | relative |
|---------------------|----------|

Show the difference between the current and previous values when used with the [--sleep](#page-134-4) option. This option works only with the extended-status command.

<span id="page-133-5"></span>• [--server-public-key-path=](#page-133-5)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-133-5)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-130-4).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-134-0"></span>• [--shared-memory-base-name=](#page-134-0)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-134-1"></span>• [--show-warnings](#page-134-1)

| Command-Line Format | show-warnings |
|---------------------|---------------|
|---------------------|---------------|

Show warnings resulting from execution of statements sent to the server.

<span id="page-134-2"></span>• [--shutdown-timeout=](#page-134-2)value

| Command-Line Format | shutdown-timeout=seconds |
|---------------------|--------------------------|
| Type                | Numeric                  |
| Default Value       | 3600                     |

The maximum number of seconds to wait for server shutdown. The default value is 3600 (1 hour).

<span id="page-134-3"></span>• [--silent](#page-134-3), -s

| Command-Line Format | silent |
|---------------------|--------|

Exit silently if a connection to the server cannot be established.

<span id="page-134-4"></span>• [--sleep=](#page-134-4)delay, -i delay

| Command-Line Format | sleep=delay |
|---------------------|-------------|
|---------------------|-------------|

Execute commands repeatedly, sleeping for delay seconds in between. The [--count](#page-128-2) option determines the number of iterations. If [--count](#page-128-2) is not given, [mysqladmin](#page-121-0) executes commands indefinitely until interrupted.

<span id="page-135-0"></span>• [--socket=](#page-135-0)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-135-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See [Command Options for Encrypted Connections](#page-11-1).

<span id="page-135-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-135-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-135-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-135-2) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_135_Picture_15.jpeg)

### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-135-2) is OFF. In this case, setting [--ssl-fips-mode](#page-135-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-135-3"></span>• [--tls-ciphersuites=](#page-135-3)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-136-1"></span>• [--tls-version=](#page-136-1)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-136-2"></span>• --user=[user\\_name](#page-136-2), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin with MySQL 8.0.31 or later, you should grant this user the SKIP\_QUERY\_REWRITE privilege.

<span id="page-136-0"></span>• [--verbose](#page-136-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|                     |         |

Verbose mode. Print more information about what the program does.

<span id="page-136-3"></span>• [--version](#page-136-3), -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

<span id="page-136-4"></span>• [--vertical](#page-136-4), -E

| Command-Line Format | vertical |
|---------------------|----------|

507

<span id="page-137-1"></span>• [--wait\[=](#page-137-1)count], -w[count]

| Command-Line Format | wait |
|---------------------|------|

If the connection cannot be established, wait and retry instead of aborting. If a count value is given, it indicates the number of times to retry. The default is one time.

<span id="page-137-2"></span>• [--zstd-compression-level=](#page-137-2)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

# <span id="page-137-0"></span>**6.5.3 mysqlcheck — A Table Maintenance Program**

The [mysqlcheck](#page-137-0) client performs table maintenance: It checks, repairs, optimizes, or analyzes tables.

Each table is locked and therefore unavailable to other sessions while it is being processed, although for check operations, the table is locked with a READ lock only (see Section 15.3.6, "LOCK TABLES and UNLOCK TABLES Statements", for more information about READ and WRITE locks). Table maintenance operations can be time-consuming, particularly for large tables. If you use the [-](#page-143-0) [databases](#page-143-0) or [--all-databases](#page-141-0) option to process all tables in one or more databases, an invocation of [mysqlcheck](#page-137-0) might take a long time. (This is also true for the MySQL upgrade procedure if it determines that table checking is needed because it processes tables the same way.)

[mysqlcheck](#page-137-0) must be used when the [mysqld](#page-37-0) server is running, which means that you do not have to stop the server to perform table maintenance.

[mysqlcheck](#page-137-0) uses the SQL statements CHECK TABLE, REPAIR TABLE, ANALYZE TABLE, and OPTIMIZE TABLE in a convenient way for the user. It determines which statements to use for the operation you want to perform, and then sends the statements to the server to be executed. For details about which storage engines each statement works with, see the descriptions for those statements in Section 15.7.3, "Table Maintenance Statements".

All storage engines do not necessarily support all four maintenance operations. In such cases, an error message is displayed. For example, if test.t is an MEMORY table, an attempt to check it produces this result:

```
$> mysqlcheck test t
test.t
note : The storage engine for the table doesn't support check
```

If [mysqlcheck](#page-137-0) is unable to repair a table, see Section 3.14, "Rebuilding or Repairing Tables or Indexes" for manual table repair strategies. This is the case, for example, for InnoDB tables, which can be checked with CHECK TABLE, but not repaired with REPAIR TABLE.

![](_page_137_Picture_17.jpeg)

# **Caution**

It is best to make a backup of a table before performing a table repair operation; under some circumstances the operation might cause data loss. Possible causes include but are not limited to file system errors.

There are three general ways to invoke [mysqlcheck](#page-137-0):

```
mysqlcheck [options] db_name [tbl_name ...]
mysqlcheck [options] --databases db_name ...
mysqlcheck [options] --all-databases
```

If you do not name any tables following db\_name or if you use the [--databases](#page-143-0) or [--all](#page-141-0)[databases](#page-141-0) option, entire databases are checked.

[mysqlcheck](#page-137-0) has a special feature compared to other client programs. The default behavior of checking tables ([--check](#page-142-0)) can be changed by renaming the binary. If you want to have a tool that repairs tables by default, you should just make a copy of [mysqlcheck](#page-137-0) named mysqlrepair, or make a symbolic link to [mysqlcheck](#page-137-0) named mysqlrepair. If you invoke mysqlrepair, it repairs tables.

The names shown in the following table can be used to change [mysqlcheck](#page-137-0) default behavior.

| Command       | Meaning                       |
|---------------|-------------------------------|
| mysqlrepair   | The default option isrepair   |
| mysqlanalyze  | The default option isanalyze  |
| mysqloptimize | The default option isoptimize |

[mysqlcheck](#page-137-0) supports the following options, which can be specified on the command line or in the [mysqlcheck] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.14 mysqlcheck Options**

| Option Name            | Description                                                                                     | Deprecated |
|------------------------|-------------------------------------------------------------------------------------------------|------------|
| all-databases          | Check all tables in all databases                                                               |            |
| all-in-1               | Execute a single statement for<br>each database that names all the<br>tables from that database |            |
| analyze                | Analyze the tables                                                                              |            |
| auto-repair            | If a checked table is corrupted,<br>automatically fix it                                        |            |
| bind-address           | Use specified network interface<br>to connect to MySQL Server                                   |            |
| character-sets-dir     | Directory where character sets<br>are installed                                                 |            |
| check                  | Check the tables for errors                                                                     |            |
| check-only-changed     | Check only tables that have<br>changed since the last check                                     |            |
| check-upgrade          | Invoke CHECK TABLE with the<br>FOR UPGRADE option                                               |            |
| compress               | Compress all information sent<br>between client and server                                      | Yes        |
| compression-algorithms | Permitted compression<br>algorithms for connections to<br>server                                |            |
| databases              | Interpret all arguments as<br>database names                                                    |            |
| debug                  | Write debugging log                                                                             |            |
| debug-check            | Print debugging information<br>when program exits                                               |            |

| Option Name             | Description                                                                       | Deprecated |
|-------------------------|-----------------------------------------------------------------------------------|------------|
| debug-info              | Print debugging information,<br>memory, and CPU statistics<br>when program exits  |            |
| default-auth            | Authentication plugin to use                                                      |            |
| default-character-set   | Specify default character set                                                     |            |
| defaults-extra-file     | Read named option file in<br>addition to usual option files                       |            |
| defaults-file           | Read only named option file                                                       |            |
| defaults-group-suffix   | Option group suffix value                                                         |            |
| enable-cleartext-plugin | Enable cleartext authentication<br>plugin                                         |            |
| extended                | Check and repair tables                                                           |            |
| fast                    | Check only tables that have not<br>been closed properly                           |            |
| force                   | Continue even if an SQL error<br>occurs                                           |            |
| get-server-public-key   | Request RSA public key from<br>server                                             |            |
| help                    | Display help message and exit                                                     |            |
| host                    | Host on which MySQL server is<br>located                                          |            |
| login-path              | Read login path options<br>from .mylogin.cnf                                      |            |
| medium-check            | Do a check that is faster than an<br>extended operation                           |            |
| no-defaults             | Read no option files                                                              |            |
| optimize                | Optimize the tables                                                               |            |
| password                | Password to use when<br>connecting to server                                      |            |
| password1               | First multifactor authentication<br>password to use when<br>connecting to server  |            |
| password2               | Second multifactor authentication<br>password to use when<br>connecting to server |            |
| password3               | Third multifactor authentication<br>password to use when<br>connecting to server  |            |
| pipe                    | Connect to server using named<br>pipe (Windows only)                              |            |
| plugin-dir              | Directory where plugins are<br>installed                                          |            |
| port                    | TCP/IP port number for<br>connection                                              |            |
| print-defaults          | Print default options                                                             |            |
| protocol                | Transport protocol to use                                                         |            |

| Option Name                                  | Description                                                                                | Deprecated |
|----------------------------------------------|--------------------------------------------------------------------------------------------|------------|
| quick                                        | The fastest method of checking                                                             |            |
| repair                                       | Perform a repair that can fix<br>almost anything except unique<br>keys that are not unique |            |
| server-public-key-path                       | Path name to file containing RSA<br>public key                                             |            |
| shared-memory-base-name                      | Shared-memory name for<br>shared-memory connections<br>(Windows only)                      |            |
| silent                                       | Silent mode                                                                                |            |
| skip-database                                | Omit this database from<br>performed operations                                            |            |
| socket                                       | Unix socket file or Windows<br>named pipe to use                                           |            |
| ssl-ca                                       | File that contains list of trusted<br>SSL Certificate Authorities                          |            |
| ssl-capath                                   | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files          |            |
| ssl-cert                                     | File that contains X.509<br>certificate                                                    |            |
| ssl-cipher                                   | Permissible ciphers for<br>connection encryption                                           |            |
| ssl-crl                                      | File that contains certificate<br>revocation lists                                         |            |
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                               |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                              | Yes        |
| ssl-key                                      | File that contains X.509 key                                                               |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                          |            |
| ssl-session-data                             | File that contains SSL session<br>data                                                     |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                                 |            |
| tables                                       | Overrides thedatabases or -B<br>option                                                     |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                              |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                                     |            |
| use-frm                                      | For repair operations on MyISAM<br>tables                                                  |            |
| user                                         | MySQL user name to use when<br>connecting to server                                        |            |
| verbose                                      | Verbose mode                                                                               |            |

| Option Name            | Description                                                                                                                     | Deprecated |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------|
| version                | Display version information and<br>exit                                                                                         |            |
| write-binlog           | Log ANALYZE, OPTIMIZE,<br>REPAIR statements to binary<br>logskip-write-binlog adds<br>NO_WRITE_TO_BINLOG to<br>these statements |            |
| zstd-compression-level | Compression level for<br>connections to server that use<br>zstd compression                                                     |            |

<span id="page-141-5"></span>• [--help](#page-141-5), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-141-0"></span>• [--all-databases](#page-141-0), -A

| Command-Line Format | all-databases |
|---------------------|---------------|
|---------------------|---------------|

Check all tables in all databases. This is the same as using the [--databases](#page-143-0) option and naming all the databases on the command line, except that the INFORMATION\_SCHEMA and performance\_schema databases are not checked. They can be checked by explicitly naming them with the [--databases](#page-143-0) option.

<span id="page-141-2"></span>• [--all-in-1](#page-141-2), -1

| Command-Line Format | all-in-1 |
|---------------------|----------|
|---------------------|----------|

Instead of issuing a statement for each table, execute a single statement for each database that names all the tables from that database to be processed.

<span id="page-141-1"></span>• [--analyze](#page-141-1), -a

| Command-Line Format | analyze |
|---------------------|---------|
|---------------------|---------|

Analyze the tables.

<span id="page-141-3"></span>• [--auto-repair](#page-141-3)

| Command-Line Format | auto-repair |
|---------------------|-------------|
|---------------------|-------------|

If a checked table is corrupted, automatically fix it. Any necessary repairs are done after all tables have been checked.

<span id="page-141-4"></span>• [--bind-address=](#page-141-4)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-142-1"></span>• [--character-sets-dir=](#page-142-1)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-142-0"></span>• [--check](#page-142-0), -c

| Command-Line Format | check |
|---------------------|-------|
|---------------------|-------|

Check the tables for errors. This is the default operation.

<span id="page-142-2"></span>• [--check-only-changed](#page-142-2), -C

| Command-Line Format | check-only-changed |
|---------------------|--------------------|
|---------------------|--------------------|

Check only tables that have changed since the last check or that have not been closed properly.

<span id="page-142-3"></span>• [--check-upgrade](#page-142-3), -g

| Command-Line Format | check-upgrade |
|---------------------|---------------|
|---------------------|---------------|

Invoke CHECK TABLE with the FOR UPGRADE option to check tables for incompatibilities with the current version of the server.

<span id="page-142-4"></span>• [--compress](#page-142-4)

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See [Section 6.2.8,](#page-32-0) ["Connection Compression Control".](#page-32-0)

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

<span id="page-142-5"></span>• [--compression-algorithms=](#page-142-5)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | 513<br>zlib                  |
|                     | zstd                         |

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

<span id="page-143-0"></span>• [--databases](#page-143-0), -B

| Command-Line Format | databases |
|---------------------|-----------|
|                     |           |

Process all tables in the named databases. Normally, [mysqlcheck](#page-137-0) treats the first name argument on the command line as a database name and any following names as table names. With this option, it treats all name arguments as database names.

<span id="page-143-1"></span>• --debug[=[debug\\_options](#page-143-1)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-143-2"></span>• [--debug-check](#page-143-2)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-143-3"></span>• [--debug-info](#page-143-3)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-143-4"></span>• [--default-character-set=](#page-143-4)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

<span id="page-144-0"></span>• [--defaults-extra-file=](#page-144-0)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-144-1"></span>• [--defaults-file=](#page-144-1)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with [--defaults-file](#page-1-0), client programs read .mylogin.cnf.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-144-2"></span>• [--defaults-group-suffix=](#page-144-2)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlcheck](#page-137-0) normally reads the [client] and [mysqlcheck] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-144-2), [mysqlcheck](#page-137-0) also reads the [client\_other] and [mysqlcheck\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-144-3"></span>• [--extended](#page-144-3), -e

| Command-Line Format | extended |
|---------------------|----------|
|---------------------|----------|

If you are using this option to check tables, it ensures that they are 100% consistent but takes a long time. 515

If you are using this option to repair tables, it runs an extended repair that may not only take a long

### <span id="page-145-0"></span>• [--default-auth=](#page-145-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

### <span id="page-145-1"></span>• [--enable-cleartext-plugin](#page-145-1)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

### <span id="page-145-2"></span>• [--fast](#page-145-2), -F

| Command-Line Format | fast |
|---------------------|------|
|---------------------|------|

Check only tables that have not been closed properly.

### <span id="page-145-3"></span>• [--force](#page-145-3), -f

| Command-Line Format | force |
|---------------------|-------|
|                     |       |

Continue even if an SQL error occurs.

# <span id="page-145-4"></span>• [--get-server-public-key](#page-145-4)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-148-5)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-145-4).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

### <span id="page-145-5"></span>• --host=[host\\_name](#page-145-5), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-146-1"></span>• [--login-path=](#page-146-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-146-2"></span>• [--medium-check](#page-146-2), -m

| Command-Line Format | medium-check |
|---------------------|--------------|
|---------------------|--------------|

Do a check that is faster than an [--extended](#page-144-3) operation. This finds only 99.99% of all errors, which should be good enough in most cases.

<span id="page-146-3"></span>• [--no-defaults](#page-146-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-146-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-146-3) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-146-0"></span>• [--optimize](#page-146-0), -o

| Command-Line Format | optimize |
|---------------------|----------|
|---------------------|----------|

Optimize the tables.

<span id="page-146-4"></span>• [--password\[=](#page-146-4)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

[password=](#page-146-4) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlcheck](#page-137-0) should not prompt for one, use the [--skip-password](#page-146-4) option.

<span id="page-147-0"></span>• [--password1\[=](#page-147-0)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlcheck](#page-137-0) prompts for one. If given, there must be no space between [--password1=](#page-147-0) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlcheck](#page-137-0) should not prompt for one, use the [--skip-password1](#page-147-0) option.

[--password1](#page-147-0) and [--password](#page-146-4) are synonymous, as are [--skip-password1](#page-147-0) and [--skip](#page-146-4)[password](#page-146-4).

<span id="page-147-1"></span>• [--password2\[=](#page-147-1)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-147-0); see the description of that option for details.

<span id="page-147-2"></span>• [--password3\[=](#page-147-2)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-147-0); see the description of that option for details.

<span id="page-147-3"></span>• [--pipe](#page-147-3), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-147-4"></span>• [--plugin-dir=](#page-147-4)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-145-0) option is used to specify an authentication plugin but [mysqlcheck](#page-137-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

### <span id="page-148-1"></span>• --port=[port\\_num](#page-148-1), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-148-2"></span>• [--print-defaults](#page-148-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-148-3"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-148-3)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see [Section 6.2.7, "Connection Transport Protocols".](#page-31-0)

<span id="page-148-4"></span>• [--quick](#page-148-4), -q

| Command-Line Format | quick |
|---------------------|-------|
|---------------------|-------|

If you are using this option to check tables, it prevents the check from scanning the rows to check for incorrect links. This is the fastest check method.

If you are using this option to repair tables, it tries to repair only the index tree. This is the fastest repair method.

<span id="page-148-0"></span>• [--repair](#page-148-0), -r

<span id="page-148-5"></span>

| Command-Line Format | repair |
|---------------------|--------|
|---------------------|--------|

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-148-5)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-145-4).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-149-0"></span>• [--shared-memory-base-name=](#page-149-0)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-149-1"></span>• [--silent](#page-149-1), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Silent mode. Print only error messages.

<span id="page-149-2"></span>• [--skip-database=](#page-149-2)db\_name

| Command-Line Format | skip-database=db_name |
|---------------------|-----------------------|
|                     |                       |

Do not include the named database (case-sensitive) in the operations performed by [mysqlcheck](#page-137-0).

<span id="page-149-3"></span>• [--socket=](#page-149-3)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-149-4"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See [Command Options for Encrypted Connections](#page-11-1).

<span id="page-150-0"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-150-0)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-150-0) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-150-0) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_150_Picture_9.jpeg)

## **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-150-0) is OFF. In this case, setting [--ssl-fips-mode](#page-150-0) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-150-1"></span>• [--tables](#page-150-1)

| Command-Line Format | tables |
|---------------------|--------|

Override the [--databases](#page-143-0) or -B option. All name arguments following the option are regarded as table names.

<span id="page-150-2"></span>• [--tls-ciphersuites=](#page-150-2)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-151-0"></span>• [--tls-version=](#page-151-0)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-151-1"></span>• [--use-frm](#page-151-1)

| Command-Line Format | use-frm |
|---------------------|---------|
|---------------------|---------|

For repair operations on MyISAM tables, get the table structure from the data dictionary so that the table can be repaired even if the .MYI header is corrupted.

<span id="page-151-2"></span>• --user=[user\\_name](#page-151-2), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

<span id="page-151-3"></span>• [--verbose](#page-151-3), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Print information about the various stages of program operation.

<span id="page-151-4"></span>• [--version](#page-151-4), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-151-5"></span>• [--write-binlog](#page-151-5)

| Command-Line Format | write-binlog |
|---------------------|--------------|
|---------------------|--------------|

This option is enabled by default, so that ANALYZE TABLE, OPTIMIZE TABLE, and REPAIR TABLE statements generated by [mysqlcheck](#page-137-0) are written to the binary log. Use [--skip-write-binlog](#page-151-5) to cause NO\_WRITE\_TO\_BINLOG to be added to the statements so that they are not logged. Use the [--skip-write-binlog](#page-151-5) when these statements should not be sent to replicas or run when using the binary logs for recovery from backup.

<span id="page-151-6"></span>• [--zstd-compression-level=](#page-151-6)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
|                     |                          |

Type Integer

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

# <span id="page-152-0"></span>**6.5.4 mysqldump — A Database Backup Program**

The [mysqldump](#page-152-0) client utility performs logical backups, producing a set of SQL statements that can be executed to reproduce the original database object definitions and table data. It dumps one or more MySQL databases for backup or transfer to another SQL server. The [mysqldump](#page-152-0) command can also generate output in CSV, other delimited text, or XML format.

![](_page_152_Picture_7.jpeg)

### **Tip**

Consider using the [MySQL Shell dump utilities,](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-dump-instance-schema.md) which provide parallel dumping with multiple threads, file compression, and progress information display, as well as cloud features such as Oracle Cloud Infrastructure Object Storage streaming, and MySQL HeatWave compatibility checks and modifications. Dumps can be easily imported into a MySQL Server instance or a MySQL HeatWave DB System using the [MySQL Shell load dump utilities.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-load-dump.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

- [Performance and Scalability Considerations](#page-153-0)
- [Invocation Syntax](#page-154-0)
- [Option Syntax Alphabetical Summary](#page-154-1)
- [Connection Options](#page-160-0)
- [Option-File Options](#page-166-0)
- [DDL Options](#page-167-0)
- [Debug Options](#page-169-0)
- [Help Options](#page-171-0)
- [Internationalization Options](#page-171-1)
- [Replication Options](#page-172-0)
- [Format Options](#page-177-0)
- [Filtering Options](#page-181-0)
- [Performance Options](#page-183-0)
- [Transactional Options](#page-185-0)
- [Option Groups](#page-188-0)
- [Examples](#page-188-1)
- [Restrictions](#page-189-1)

[mysqldump](#page-152-0) requires at least the SELECT privilege for dumped tables, SHOW VIEW for dumped views, TRIGGER for dumped triggers, LOCK TABLES if the [--single-transaction](#page-187-0) option is not used, PROCESS (as of MySQL 8.0.21) if the --no-tablespaces option is not used, and (as of MySQL 8.0.32) the RELOAD or FLUSH\_TABLES privilege with [--single-transaction](#page-187-0) if both gtid\_mode=ON and gtid\_purged=ON|AUTO. Certain options might require other privileges as noted in the option descriptions.

To reload a dump file, you must have the privileges required to execute the statements that it contains, such as the appropriate CREATE privileges for objects created by those statements.

[mysqldump](#page-152-0) output can include ALTER DATABASE statements that change the database collation. These may be used when dumping stored programs to preserve their character encodings. To reload a dump file containing such statements, the ALTER privilege for the affected database is required.

![](_page_153_Picture_4.jpeg)

### **Note**

A dump made using PowerShell on Windows with output redirection creates a file that has UTF-16 encoding:

```
mysqldump [options] > dump.sql
```

However, UTF-16 is not permitted as a connection character set (see Impermissible Client Character Sets), so the dump file cannot be loaded correctly. To work around this issue, use the --result-file option, which creates the output in ASCII format:

```
mysqldump [options] --result-file=dump.sql
```

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid\_mode=ON), if your dump file includes system tables. [mysqldump](#page-152-0) issues DML instructions for the system tables which use the non-transactional MyISAM storage engine, and this combination is not permitted when GTIDs are enabled.

## <span id="page-153-0"></span>**Performance and Scalability Considerations**

mysqldump advantages include the convenience and flexibility of viewing or even editing the output before restoring. You can clone databases for development and DBA work, or produce slight variations of an existing database for testing. It is not intended as a fast or scalable solution for backing up substantial amounts of data. With large data sizes, even if the backup step takes a reasonable time, restoring the data can be very slow because replaying the SQL statements involves disk I/O for insertion, index creation, and so on.

For large-scale backup and restore, a physical backup is more appropriate, to copy the data files in their original format so that they can be restored quickly.

If your tables are primarily InnoDB tables, or if you have a mix of InnoDB and MyISAM tables, consider using mysqlbackup, which is available as part of MySQL Enterprise. This tool provides high performance for InnoDB backups with minimal disruption; it can also back up tables from MyISAM and other storage engines; it also provides a number of convenient options to accommodate different backup scenarios. See Section 32.1, "MySQL Enterprise Backup Overview".

[mysqldump](#page-152-0) can retrieve and dump table contents row by row, or it can retrieve the entire content from a table and buffer it in memory before dumping it. Buffering in memory can be a problem if you are dumping large tables. To dump tables row by row, use the [--quick](#page-185-1) option (or [--opt](#page-185-2), which enables [--quick](#page-185-1)). The [--opt](#page-185-2) option (and hence [--quick](#page-185-1)) is enabled by default, so to enable memory buffering, use [--skip-quick](#page-185-1).

If you are using a recent version of [mysqldump](#page-152-0) to generate a dump to be reloaded into a very old MySQL server, use the [--skip-opt](#page-185-3) option instead of the [--opt](#page-185-2) or [--extended-insert](#page-183-1) option.

For additional information about [mysqldump](#page-152-0), see Section 9.4, "Using mysqldump for Backups".

# <span id="page-154-0"></span>**Invocation Syntax**

There are in general three ways to use [mysqldump](#page-152-0)—in order to dump a set of one or more tables, a set of one or more complete databases, or an entire MySQL server—as shown here:

```
mysqldump [options] db_name [tbl_name ...]
mysqldump [options] --databases db_name ...
mysqldump [options] --all-databases
```

To dump entire databases, do not name any tables following db\_name, or use the [--databases](#page-181-1) or [--all-databases](#page-181-2) option.

To see a list of the options your version of [mysqldump](#page-152-0) supports, issue the command [mysqldump](#page-152-0) [-](#page-171-2) [help](#page-171-2).

# <span id="page-154-1"></span>**Option Syntax - Alphabetical Summary**

[mysqldump](#page-152-0) supports the following options, which can be specified on the command line or in the [mysqldump] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

### **Table 6.15 mysqldump Options**

| Option Name              | Description                                                                                                         | Deprecated |
|--------------------------|---------------------------------------------------------------------------------------------------------------------|------------|
| add-drop-database        | Add DROP DATABASE<br>statement before each CREATE<br>DATABASE statement                                             |            |
| add-drop-table           | Add DROP TABLE statement<br>before each CREATE TABLE<br>statement                                                   |            |
| add-drop-trigger         | Add DROP TRIGGER statement<br>before each CREATE TRIGGER<br>statement                                               |            |
| add-locks                | Surround each table dump with<br>LOCK TABLES and UNLOCK<br>TABLES statements                                        |            |
| all-databases            | Dump all tables in all databases                                                                                    |            |
| allow-keywords           | Allow creation of column names<br>that are keywords                                                                 |            |
| apply-replica-statements | Include STOP REPLICA prior<br>to CHANGE REPLICATION<br>SOURCE TO statement and<br>START REPLICA at end of<br>output |            |
| apply-slave-statements   | Include STOP SLAVE prior to<br>CHANGE MASTER statement<br>and START SLAVE at end of<br>output                       | Yes        |
| bind-address             | Use specified network interface<br>to connect to MySQL Server                                                       |            |
| character-sets-dir       | Directory where character sets<br>are installed                                                                     |            |
| column-statistics        | Write ANALYZE TABLE<br>statements to generate statistics<br>histograms                                              |            |
| comments                 | Add comments to dump file                                                                                           |            |

| Option Name            | Description                                                                                                   | Deprecated |
|------------------------|---------------------------------------------------------------------------------------------------------------|------------|
| compact                | Produce more compact output                                                                                   |            |
| compatible             | Produce output that is more<br>compatible with other database<br>systems or with older MySQL<br>servers       |            |
| complete-insert        | Use complete INSERT<br>statements that include column<br>names                                                |            |
| compress               | Compress all information sent<br>between client and server                                                    | Yes        |
| compression-algorithms | Permitted compression<br>algorithms for connections to<br>server                                              |            |
| create-options         | Include all MySQL-specific table<br>options in CREATE TABLE<br>statements                                     |            |
| databases              | Interpret all name arguments as<br>database names                                                             |            |
| debug                  | Write debugging log                                                                                           |            |
| debug-check            | Print debugging information<br>when program exits                                                             |            |
| debug-info             | Print debugging information,<br>memory, and CPU statistics<br>when program exits                              |            |
| default-auth           | Authentication plugin to use                                                                                  |            |
| default-character-set  | Specify default character set                                                                                 |            |
| defaults-extra-file    | Read named option file in<br>addition to usual option files                                                   |            |
| defaults-file          | Read only named option file                                                                                   |            |
| defaults-group-suffix  | Option group suffix value                                                                                     |            |
| delete-master-logs     | On a replication source server,<br>delete the binary logs after<br>performing the dump operation              | Yes        |
| delete-source-logs     | On a replication source server,<br>delete the binary logs after<br>performing the dump operation              |            |
| disable-keys           | For each table, surround<br>INSERT statements with<br>statements to disable and enable<br>keys                |            |
| dump-date              | Include dump date as "Dump<br>completed on" comment if<br>comments is given                                   |            |
| dump-replica           | Include CHANGE REPLICATION<br>SOURCE TO statement that<br>lists binary log coordinates of<br>replica's source |            |

| Option Name                   | Description                                                                                                                 | Deprecated |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------|------------|
| dump-slave                    | Include CHANGE MASTER<br>statement that lists binary log<br>coordinates of replica's source                                 | Yes        |
| enable-cleartext-plugin       | Enable cleartext authentication<br>plugin                                                                                   |            |
| events                        | Dump events from dumped<br>databases                                                                                        |            |
| extended-insert               | Use multiple-row INSERT syntax                                                                                              |            |
| fields-enclosed-by            | This option is used with the<br>tab option and has the same<br>meaning as the corresponding<br>clause for LOAD DATA         |            |
| fields-escaped-by             | This option is used with the<br>tab option and has the same<br>meaning as the corresponding<br>clause for LOAD DATA         |            |
| fields-optionally-enclosed-by | This option is used with the<br>tab option and has the same<br>meaning as the corresponding<br>clause for LOAD DATA         |            |
| fields-terminated-by          | This option is used with the<br>tab option and has the same<br>meaning as the corresponding<br>clause for LOAD DATA         |            |
| flush-logs                    | Flush MySQL server log files<br>before starting dump                                                                        |            |
| flush-privileges              | Emit a FLUSH PRIVILEGES<br>statement after dumping mysql<br>database                                                        |            |
| force                         | Continue even if an SQL error<br>occurs during a table dump                                                                 |            |
| get-server-public-key         | Request RSA public key from<br>server                                                                                       |            |
| help                          | Display help message and exit                                                                                               |            |
| hex-blob                      | Dump binary columns using<br>hexadecimal notation                                                                           |            |
| host                          | Host on which MySQL server is<br>located                                                                                    |            |
| ignore-error                  | Ignore specified errors                                                                                                     |            |
| ignore-table                  | Do not dump given table                                                                                                     |            |
| include-master-host-port      | Include MASTER_HOST/<br>MASTER_PORT options in<br>CHANGE MASTER statement<br>produced withdump-slave                        | Yes        |
| include-source-host-port      | Include SOURCE_HOST and<br>SOURCE_PORT options in<br>CHANGE REPLICATION<br>SOURCE TO statement<br>produced withdump-replica |            |

| Option Name            | Description                                                                                                          | Deprecated |
|------------------------|----------------------------------------------------------------------------------------------------------------------|------------|
| insert-ignore          | Write INSERT IGNORE rather<br>than INSERT statements                                                                 |            |
| lines-terminated-by    | This option is used with the<br>tab option and has the same<br>meaning as the corresponding<br>clause for LOAD DATA  |            |
| lock-all-tables        | Lock all tables across all<br>databases                                                                              |            |
| lock-tables            | Lock all tables before dumping<br>them                                                                               |            |
| log-error              | Append warnings and errors to<br>named file                                                                          |            |
| login-path             | Read login path options<br>from .mylogin.cnf                                                                         |            |
| master-data            | Write the binary log file name<br>and position to the output                                                         | Yes        |
| max-allowed-packet     | Maximum packet length to send<br>to or receive from server                                                           |            |
| mysqld-long-query-time | Session value for slow query<br>threshold                                                                            |            |
| net-buffer-length      | Buffer size for TCP/IP and socket<br>communication                                                                   |            |
| network-timeout        | Increase network timeouts to<br>permit larger table dumps                                                            |            |
| no-autocommit          | Enclose the INSERT statements<br>for each dumped table within<br>SET autocommit = 0 and<br>COMMIT statements         |            |
| no-create-db           | Do not write CREATE<br>DATABASE statements                                                                           |            |
| no-create-info         | Do not write CREATE TABLE<br>statements that re-create each<br>dumped table                                          |            |
| no-data                | Do not dump table contents                                                                                           |            |
| no-defaults            | Read no option files                                                                                                 |            |
| no-set-names           | Same asskip-set-charset                                                                                              |            |
| no-tablespaces         | Do not write any CREATE<br>LOGFILE GROUP or CREATE<br>TABLESPACE statements in<br>output                             |            |
| opt                    | Shorthand foradd-drop-table<br>add-lockscreate-options<br>disable-keysextended-insert<br>lock-tablesquickset-charset |            |
| order-by-primary       | Dump each table's rows sorted<br>by its primary key, or by its first<br>unique index                                 |            |

| Option Name                                   | Description                                                                              | Deprecated |
|-----------------------------------------------|------------------------------------------------------------------------------------------|------------|
| password                                      | Password to use when<br>connecting to server                                             |            |
| password1                                     | First multifactor authentication<br>password to use when<br>connecting to server         |            |
| password2                                     | Second multifactor authentication<br>password to use when<br>connecting to server        |            |
| password3                                     | Third multifactor authentication<br>password to use when<br>connecting to server         |            |
| pipe                                          | Connect to server using named<br>pipe (Windows only)                                     |            |
| plugin-authentication-kerberos<br>client-mode | Permit GSSAPI pluggable<br>authentication through the MIT<br>Kerberos library on Windows |            |
| plugin-dir                                    | Directory where plugins are<br>installed                                                 |            |
| port                                          | TCP/IP port number for<br>connection                                                     |            |
| print-defaults                                | Print default options                                                                    |            |
| protocol                                      | Transport protocol to use                                                                |            |
| quick                                         | Retrieve rows for a table from the<br>server a row at a time                             |            |
| quote-names                                   | Quote identifiers within backtick<br>characters                                          |            |
| replace                                       | Write REPLACE statements<br>rather than INSERT statements                                |            |
| result-file                                   | Direct output to a given file                                                            |            |
| routines                                      | Dump stored routines<br>(procedures and functions) from<br>dumped databases              |            |
| server-public-key-path                        | Path name to file containing RSA<br>public key                                           |            |
| set-charset                                   | Add SET NAMES<br>default_character_set to output                                         |            |
| set-gtid-purged                               | Whether to add SET<br>@@GLOBAL.GTID_PURGED to<br>output                                  |            |
| shared-memory-base-name                       | Shared-memory name for<br>shared-memory connections<br>(Windows only)                    |            |
| show-create-skip-secondary<br>engine          | Exclude SECONDARY ENGINE<br>clause from CREATE TABLE<br>statements                       |            |
| single-transaction                            | Issue a BEGIN SQL statement<br>before dumping data from server                           |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| skip-add-drop-table                          | Do not add a DROP TABLE<br>statement before each CREATE<br>TABLE statement        |            |
| skip-add-locks                               | Do not add locks                                                                  |            |
| skip-comments                                | Do not add comments to dump<br>file                                               |            |
| skip-compact                                 | Do not produce more compact<br>output                                             |            |
| skip-disable-keys                            | Do not disable keys                                                               |            |
| skip-extended-insert                         | Turn off extended-insert                                                          |            |
| skip-generated-invisible<br>primary-key      | Do not include generated<br>invisible primary keys in dump<br>file                |            |
| skip-opt                                     | Turn off options set byopt                                                        |            |
| skip-quick                                   | Do not retrieve rows for a table<br>from the server a row at a time               |            |
| skip-quote-names                             | Do not quote identifiers                                                          |            |
| skip-set-charset                             | Do not write SET NAMES<br>statement                                               |            |
| skip-triggers                                | Do not dump triggers                                                              |            |
| skip-tz-utc                                  | Turn off tz-utc                                                                   |            |
| socket                                       | Unix socket file or Windows<br>named pipe to use                                  |            |
| source-data                                  | Write the binary log file name<br>and position to the output                      |            |
| ssl-ca                                       | File that contains list of trusted<br>SSL Certificate Authorities                 |            |
| ssl-capath                                   | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files |            |
| ssl-cert                                     | File that contains X.509<br>certificate                                           |            |
| ssl-cipher                                   | Permissible ciphers for<br>connection encryption                                  |            |
| ssl-crl                                      | File that contains certificate<br>revocation lists                                |            |
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                      |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                     | Yes        |
| ssl-key                                      | File that contains X.509 key                                                      |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                 |            |
| ssl-session-data                             | File that contains SSL session<br>data                                            |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                        |            |

| Option Name            | Description                                                                 | Deprecated |
|------------------------|-----------------------------------------------------------------------------|------------|
| tab                    | Produce tab-separated data files                                            |            |
| tables                 | Overridedatabases or -B<br>option                                           |            |
| tls-ciphersuites       | Permissible TLSv1.3 ciphersuites<br>for encrypted connections               |            |
| tls-version            | Permissible TLS protocols for<br>encrypted connections                      |            |
| triggers               | Dump triggers for each dumped<br>table                                      |            |
| tz-utc                 | Add SET TIME_ZONE='+00:00'<br>to dump file                                  |            |
| user                   | MySQL user name to use when<br>connecting to server                         |            |
| verbose                | Verbose mode                                                                |            |
| version                | Display version information and<br>exit                                     |            |
| where                  | Dump only rows selected by<br>given WHERE condition                         |            |
| xml                    | Produce XML output                                                          |            |
| zstd-compression-level | Compression level for<br>connections to server that use<br>zstd compression |            |

# <span id="page-160-0"></span>**Connection Options**

The [mysqldump](#page-152-0) command logs into a MySQL server to extract information. The following options specify how to connect to the MySQL server, either on the same machine or a remote system.

<span id="page-160-1"></span>• [--bind-address=](#page-160-1)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-160-2"></span>• [--compress](#page-160-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See [Section 6.2.8,](#page-32-0) ["Connection Compression Control".](#page-32-0)

<span id="page-160-3"></span>As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

<span id="page-161-0"></span>• [--default-auth=](#page-161-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-161-1"></span>• [--enable-cleartext-plugin](#page-161-1)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-161-2"></span>• [--get-server-public-key](#page-161-2)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-164-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-161-2).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-161-3"></span>• --host=[host\\_name](#page-161-3), -h host\_name

| Command-Line Format | host |
|---------------------|------|
|                     |      |

Dump data from the MySQL server on the given host. The default host is localhost.

<span id="page-162-0"></span>• [--login-path=](#page-162-0)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-162-1"></span>• [--password\[=](#page-162-1)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqldump](#page-152-0) prompts for one. If given, there must be no space between [-](#page-162-1) [password=](#page-162-1) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqldump](#page-152-0) should not prompt for one, use the [--skip-password](#page-162-1) option.

<span id="page-162-2"></span>• [--password1\[=](#page-162-2)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqldump](#page-152-0) prompts for one. If given, there must be no space between [--password1=](#page-162-2) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqldump](#page-152-0) should not prompt for one, use the [--skip-password1](#page-162-2) option.

[--password1](#page-162-2) and [--password](#page-162-1) are synonymous, as are [--skip-password1](#page-162-2) and [--skip](#page-162-1)[password](#page-162-1).

<span id="page-162-3"></span>• [--password2\[=](#page-162-3)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-162-2); see the description of that option for details.

<span id="page-163-0"></span>• [--password3\[=](#page-163-0)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-162-2); see the description of that option for details.

<span id="page-163-1"></span>• [--pipe](#page-163-1), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-163-2"></span>• [--plugin-authentication-kerberos-client-mode=](#page-163-2)value

| Command-Line Format | plugin-authentication-kerberos<br>client-mode |
|---------------------|-----------------------------------------------|
| Type                | String                                        |
| Default Value       | SSPI                                          |
| Valid Values        | GSSAPI                                        |

On Windows, the authentication\_kerberos\_client authentication plugin supports this plugin option. It provides two possible values that the client user can set at runtime: SSPI and GSSAPI.

The default value for the client-side plugin option uses Security Support Provider Interface (SSPI), which is capable of acquiring credentials from the Windows in-memory cache. Alternatively, the client user can select a mode that supports Generic Security Service Application Program Interface (GSSAPI) through the MIT Kerberos library on Windows. GSSAPI is capable of acquiring cached credentials previously generated by using the kinit command.

For more information, see Commands for Windows Clients in GSSAPI Mode.

<span id="page-163-3"></span>• [--plugin-dir=](#page-163-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-161-0) option is used to specify an authentication plugin but [mysqldump](#page-152-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-163-4"></span>• --port=[port\\_num](#page-163-4), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

<span id="page-164-0"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-164-0)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see [Section 6.2.7, "Connection Transport Protocols".](#page-31-0)

<span id="page-164-1"></span>• [--server-public-key-path=](#page-164-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-164-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-161-2).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-164-2"></span>• [--socket=](#page-164-2)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-164-3"></span>• --ssl\* 535

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See [Command Options for Encrypted Connections](#page-11-1).

<span id="page-165-0"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-165-0)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-165-0) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-165-0) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_165_Picture_8.jpeg)

### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-165-0) is OFF. In this case, setting [--ssl-fips-mode](#page-165-0) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-165-1"></span>• [--tls-ciphersuites=](#page-165-1)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-165-2"></span>• [--tls-version=](#page-165-2)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |

```
TLSv1,TLSv1.1,TLSv1.2 (otherwise)
```

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-166-3"></span>• --user=[user\\_name](#page-166-3), -u user\_name

| Command-Line Format | user=user_name |
|---------------------|----------------|
| Type                | String         |

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin with MySQL 8.0.31 or later, you should grant this user the SKIP\_QUERY\_REWRITE privilege.

<span id="page-166-4"></span>• [--zstd-compression-level=](#page-166-4)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

## <span id="page-166-1"></span><span id="page-166-0"></span>**Option-File Options**

These options are used to control which option files to read.

• [--defaults-extra-file=](#page-166-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-166-2"></span>• [--defaults-file=](#page-166-2)file\_name

| Command-Line Format | defaults-file=file_name | 537 |
|---------------------|-------------------------|-----|
| Type                | File name               |     |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with [--defaults-file](#page-1-0), client programs read .mylogin.cnf.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-167-2"></span>• [--defaults-group-suffix=](#page-167-2)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqldump](#page-152-0) normally reads the [client] and [mysqldump] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-167-2), [mysqldump](#page-152-0) also reads the [client\_other] and [mysqldump\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-167-3"></span>• [--no-defaults](#page-167-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-167-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-167-3) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-167-4"></span>• [--print-defaults](#page-167-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

## <span id="page-167-0"></span>**DDL Options**

Usage scenarios for [mysqldump](#page-152-0) include setting up an entire new MySQL instance (including database tables), and replacing data inside an existing instance with existing databases and tables. The following options let you specify which things to tear down and set up when restoring a dump, by encoding various DDL statements within the dump file.

<span id="page-167-1"></span>• [--add-drop-database](#page-167-1)

| Command-Line Format | add-drop-database |
|---------------------|-------------------|
|---------------------|-------------------|

Write a DROP DATABASE statement before each CREATE DATABASE statement. This option is typically used in conjunction with the [--all-databases](#page-181-2) or [--databases](#page-181-1) option because no CREATE DATABASE statements are written unless one of those options is specified.

![](_page_168_Picture_2.jpeg)

### **Note**

In MySQL 8.0, the mysql schema is considered a system schema that cannot be dropped by end users. If [--add-drop-database](#page-167-1) is used with [--all-databases](#page-181-2) or with [--databases](#page-181-1) where the list of schemas to be dumped includes mysql, the dump file contains a DROP DATABASE `mysql` statement that causes an error when the dump file is reloaded.

Instead, to use [--add-drop-database](#page-167-1), use [--databases](#page-181-1) with a list of schemas to be dumped, where the list does not include mysql.

<span id="page-168-0"></span>• [--add-drop-table](#page-168-0)

| Command-Line Format<br>add-drop-table |
|---------------------------------------|
|---------------------------------------|

Write a DROP TABLE statement before each CREATE TABLE statement.

<span id="page-168-1"></span>• [--add-drop-trigger](#page-168-1)

| Command-Line Format | add-drop-trigger |
|---------------------|------------------|
|---------------------|------------------|

Write a DROP TRIGGER statement before each CREATE TRIGGER statement.

<span id="page-168-5"></span>• [--all-tablespaces](#page-168-5), -Y

| Command-Line Format | all-tablespaces |
|---------------------|-----------------|
|                     |                 |

Adds to a table dump all SQL statements needed to create any tablespaces used by an NDB table. This information is not otherwise included in the output from [mysqldump](#page-152-0). This option is currently relevant only to NDB Cluster tables.

<span id="page-168-2"></span>• [--no-create-db](#page-168-2), -n

| Command-Line Format | no-create-db |
|---------------------|--------------|
|---------------------|--------------|

Suppress the CREATE DATABASE statements that are otherwise included in the output if the [-](#page-181-1) [databases](#page-181-1) or [--all-databases](#page-181-2) option is given.

<span id="page-168-3"></span>• [--no-create-info](#page-168-3), -t

| Command-Line Format | no-create-info |
|---------------------|----------------|

Do not write CREATE TABLE statements that create each dumped table.

![](_page_168_Picture_21.jpeg)

### **Note**

This option does not exclude statements creating log file groups or tablespaces from [mysqldump](#page-152-0) output; however, you can use the [--no](#page-168-4)[tablespaces](#page-168-4) option for this purpose.

<span id="page-168-4"></span>• [--no-tablespaces](#page-168-4), -y

| Command-Line Format | no-tablespaces |
|---------------------|----------------|
|                     |                |

This option suppresses all CREATE LOGFILE GROUP and CREATE TABLESPACE statements in the output of [mysqldump](#page-152-0).

<span id="page-169-5"></span>• [--replace](#page-169-5)

| Command-Line Format | replace |
|---------------------|---------|
|---------------------|---------|

Write REPLACE statements rather than INSERT statements.

# <span id="page-169-0"></span>**Debug Options**

The following options print debugging information, encode debugging information in the dump file, or let the dump operation proceed regardless of potential problems.

<span id="page-169-1"></span>• [--allow-keywords](#page-169-1)

| Command-Line Format | allow-keywords |
|---------------------|----------------|
|---------------------|----------------|

Permit creation of column names that are keywords. This works by prefixing each column name with the table name.

<span id="page-169-2"></span>• [--comments](#page-169-2), -i

| Command-Line Format | comments |
|---------------------|----------|
|---------------------|----------|

Write additional information in the dump file such as program version, server version, and host. This option is enabled by default. To suppress this additional information, use [--skip-comments](#page-170-4).

<span id="page-169-3"></span>• --debug[=[debug\\_options](#page-169-3)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]      |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | d:t:o,/tmp/mysqldump.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default value is d:t:o,/tmp/mysqldump.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-169-4"></span>• [--debug-check](#page-169-4)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-170-0"></span>• [--debug-info](#page-170-0)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-170-1"></span>• [--dump-date](#page-170-1)

| Command-Line Format | dump-date |
|---------------------|-----------|
| Type                | Boolean   |
| Default Value       | TRUE      |

If the [--comments](#page-169-2) option is given, [mysqldump](#page-152-0) produces a comment at the end of the dump of the following form:

```
-- Dump completed on DATE
```

However, the date causes dump files taken at different times to appear to be different, even if the data are otherwise identical. [--dump-date](#page-170-1) and [--skip-dump-date](#page-170-1) control whether the date is added to the comment. The default is [--dump-date](#page-170-1) (include the date in the comment). [--skip](#page-170-1)[dump-date](#page-170-1) suppresses date printing.

<span id="page-170-2"></span>• [--force](#page-170-2), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Ignore all errors; continue even if an SQL error occurs during a table dump.

One use for this option is to cause [mysqldump](#page-152-0) to continue executing even when it encounters a view that has become invalid because the definition refers to a table that has been dropped. Without --force, [mysqldump](#page-152-0) exits with an error message. With --force, [mysqldump](#page-152-0) prints the error message, but it also writes an SQL comment containing the view definition to the dump output and continues executing.

If the [--ignore-error](#page-181-4) option is also given to ignore specific errors, [--force](#page-170-2) takes precedence.

<span id="page-170-3"></span>• [--log-error=](#page-170-3)file\_name

<span id="page-170-4"></span>• [--skip-comments](#page-170-4)

| Command-Line Format | log-error=file_name |
|---------------------|---------------------|
| Type                | File name           |

Log warnings and errors by appending them to the named file. The default is to do no logging.

| Command-Line Format | skip-comments |
|---------------------|---------------|

541

<span id="page-171-7"></span>• [--verbose](#page-171-7), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Print more information about what the program does.

# <span id="page-171-2"></span><span id="page-171-0"></span>**Help Options**

The following options display information about the [mysqldump](#page-152-0) command itself.

• [--help](#page-171-2), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-171-8"></span>• [--version](#page-171-8), -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

# <span id="page-171-1"></span>**Internationalization Options**

The following options change how the [mysqldump](#page-152-0) command represents character data with national language settings.

<span id="page-171-3"></span>• [--character-sets-dir=](#page-171-3)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-171-4"></span>• [--default-character-set=](#page-171-4)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |
| Default Value       | utf8                               |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration". If no character set is specified, [mysqldump](#page-152-0) uses utf8mb4.

<span id="page-171-5"></span>• [--no-set-names](#page-171-5), -N

| Command-Line Format | no-set-names |
|---------------------|--------------|
| Deprecated          | Yes          |

Turns off the [--set-charset](#page-171-6) setting, the same as specifying --skip-set-charset.

<span id="page-171-6"></span>• [--set-charset](#page-171-6)

| Command-Line Format | set-charset |
|---------------------|-------------|

| Disabled by | skip-set-charset |  |
|-------------|------------------|--|
|-------------|------------------|--|

Write SET NAMES default\_character\_set to the output. This option is enabled by default. To suppress the SET NAMES statement, use [--skip-set-charset](#page-171-6).

# <span id="page-172-0"></span>**Replication Options**

The [mysqldump](#page-152-0) command is frequently used to create an empty instance, or an instance including data, on a replica server in a replication configuration. The following options apply to dumping and restoring data on replication source servers and replicas.

<span id="page-172-1"></span>• [--apply-replica-statements](#page-172-1)

| Command-Line Format | apply-replica-statements |
|---------------------|--------------------------|
| Type                | Boolean                  |
| Default Value       | FALSE                    |

From MySQL 8.0.26, use --apply-replica-statements, and before MySQL 8.0.26, use [-](#page-172-2) [apply-slave-statements](#page-172-2). Both options have the same effect. For a replica dump produced with the [--dump-replica](#page-172-5) or [--dump-slave](#page-173-0) option, the options add a STOP REPLICA (or before MySQL 8.0.22, STOP SLAVE) statement before the statement with the binary log coordinates, and a START REPLICA statement at the end of the output.

<span id="page-172-2"></span>• [--apply-slave-statements](#page-172-2)

| Command-Line Format | apply-slave-statements |
|---------------------|------------------------|
| Deprecated          | Yes                    |
| Type                | Boolean                |
| Default Value       | FALSE                  |

Use this option before MySQL 8.0.26 rather than [--apply-replica-statements](#page-172-1). Both options have the same effect.

<span id="page-172-4"></span>• [--delete-source-logs](#page-172-4)

| Command-Line Format | delete-source-logs |
|---------------------|--------------------|
|                     |                    |

From MySQL 8.0.26, use --delete-source-logs, and before MySQL 8.0.26, use [--delete](#page-172-3)[master-logs](#page-172-3). Both options have the same effect. On a replication source server, the options delete the binary logs by sending a PURGE BINARY LOGS statement to the server after performing the dump operation. The options require the RELOAD privilege as well as privileges sufficient to execute that statement. The options automatically enable [--source-data](#page-174-2) or [--master-data](#page-175-0).

<span id="page-172-3"></span>• [--delete-master-logs](#page-172-3)

<span id="page-172-5"></span>

| Command-Line Format | delete-master-logs |
|---------------------|--------------------|
| Deprecated          | Yes                |

| Command-Line Format | dump-replica[=value] |
|---------------------|----------------------|
| Type                | Numeric              |
| Default Value       | 1                    |
| Valid Values        | 1                    |
|                     | 2                    |

From MySQL 8.0.26, use --dump-replica, and before MySQL 8.0.26, use [--dump-slave](#page-173-0). Both options have the same effect. The options are similar to [--source-data](#page-174-2), except that they are used to dump a replica server to produce a dump file that can be used to set up another server as a replica that has the same source as the dumped server. The options cause the dump output to include a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) that indicates the binary log coordinates (file name and position) of the dumped replica's source. The CHANGE REPLICATION SOURCE TO statement reads the values of Relay\_Master\_Log\_File and Exec\_Master\_Log\_Pos from the SHOW REPLICA STATUS output and uses them for SOURCE\_LOG\_FILE and SOURCE\_LOG\_POS respectively. These are the replication source server coordinates from which the replica starts replicating.

![](_page_173_Picture_3.jpeg)

### **Note**

Inconsistencies in the sequence of transactions from the relay log which have been executed can cause the wrong position to be used. See Section 19.5.1.34, "Replication and Transaction Inconsistencies" for more information.

--dump-replica or --dump-slave causes the coordinates from the source to be used rather than those of the dumped server, as is done by the [--source-data](#page-174-2) or [--master-data](#page-175-0) option. In addition, specifying this option causes the [--source-data](#page-174-2) or --master-data option to be overridden, if used, and effectively ignored.

![](_page_173_Picture_7.jpeg)

### **Warning**

--dump-replica or --dump-slave should not be used if the server where the dump is going to be applied uses gtid\_mode=ON and SOURCE\_AUTO\_POSITION=1 or MASTER\_AUTO\_POSITION=1.

The option value is handled the same way as for [--source-data](#page-174-2). Setting no value or 1 causes a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) to be written to the dump. Setting 2 causes the statement to be written but encased in SQL comments. It has the same effect as --source-data in terms of enabling or disabling other options and in how locking is handled.

--dump-replica or --dump-slave causes [mysqldump](#page-152-0) to stop the replication SQL thread before the dump and restart it again after.

--dump-replica or --dump-slave sends a SHOW REPLICA STATUS statement to the server to obtain information, so they require privileges sufficient to execute that statement.

[--apply-replica-statements](#page-172-1) and [--include-source-host-port](#page-174-1) options can be used in conjunction with --dump-replica or --dump-slave.

<span id="page-173-0"></span>• [--dump-slave\[=](#page-173-0)value]

| Command-Line Format | dump-slave[=value] |
|---------------------|--------------------|
| Deprecated          | Yes                |
| Type                | Numeric            |

| Default Value | 1 |
|---------------|---|
| Valid Values  | 1 |
|               | 2 |

Use this option before MySQL 8.0.26 rather than [--dump-replica](#page-172-5). Both options have the same effect.

### <span id="page-174-1"></span>• [--include-source-host-port](#page-174-1)

| Command-Line Format | include-source-host-port |
|---------------------|--------------------------|
| Type                | Boolean                  |
| Default Value       | FALSE                    |

From MySQL 8.0.26, use --include-source-host-port, and before MySQL 8.0.26, use [--include-master-host-port](#page-174-0). Both options have the same effect. The options add the SOURCE\_HOST | MASTER\_HOST and SOURCE\_PORT | MASTER\_PORT options for the host name and TCP/IP port number of the replica's source, to the CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) in a replica dump produced with the [--dump-replica](#page-172-5) or [--dump-slave](#page-173-0) option.

### <span id="page-174-0"></span>• [--include-master-host-port](#page-174-0)

| Command-Line Format | include-master-host-port |
|---------------------|--------------------------|
| Deprecated          | Yes                      |
| Type                | Boolean                  |
| Default Value       | FALSE                    |

Use this option before MySQL 8.0.26 rather than [--include-source-host-port](#page-174-1). Both options have the same effect.

### <span id="page-174-2"></span>• [--source-data\[=](#page-174-2)value]

| Command-Line Format | source-data[=value] |
|---------------------|---------------------|
| Type                | Numeric             |
| Default Value       | 1                   |
| Valid Values        | 1                   |
|                     | 2                   |

From MySQL 8.0.26, use --source-data, and before MySQL 8.0.26, use [--master-data](#page-175-0). Both options have the same effect. The options are used to dump a replication source server to produce a dump file that can be used to set up another server as a replica of the source. The options cause the dump output to include a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) that indicates the binary log coordinates (file name and position) of the dumped server. These are the replication source server coordinates from which the replica should start replicating after you load the dump file into the replica.

reloaded. If the option value is 1, the statement is not written as a comment and takes effect when the dump file is reloaded. If no option value is specified, the default value is 1.

--source-data and --master-data send a SHOW MASTER STATUS statement to the server to obtain information, so they require privileges sufficient to execute that statement. This option also requires the RELOAD privilege and the binary log must be enabled.

--source-data and --master-data automatically turn off [--lock-tables](#page-186-3). They also turn on [--lock-all-tables](#page-186-2), unless [--single-transaction](#page-187-0) also is specified, in which case, a global read lock is acquired only for a short time at the beginning of the dump (see the description for [-](#page-187-0) [single-transaction](#page-187-0)). In all cases, any action on logs happens at the exact moment of the dump.

It is also possible to set up a replica by dumping an existing replica of the source, using the [--dump](#page-172-5)[replica](#page-172-5) or [--dump-slave](#page-173-0) option, which overrides --source-data and --master-data and causes them to be ignored.

<span id="page-175-0"></span>• [--master-data\[=](#page-175-0)value]

| Command-Line Format | master-data[=value] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Numeric             |
| Default Value       | 1                   |
| Valid Values        | 1                   |
|                     | 2                   |

Use this option before MySQL 8.0.26 rather than [--source-data](#page-174-2). Both options have the same effect.

<span id="page-175-1"></span>• [--set-gtid-purged=](#page-175-1)value

| Command-Line Format | set-gtid-purged=value |
|---------------------|-----------------------|
| Type                | Enumeration           |
| Default Value       | AUTO                  |
| Valid Values        | OFF                   |
|                     | ON                    |
|                     | AUTO                  |

This option is for servers that use GTID-based replication (gtid\_mode=ON). It controls the inclusion of a SET @@GLOBAL.gtid\_purged statement in the dump output, which updates the value of gtid\_purged on a server where the dump file is reloaded, to add the GTID set from the source server's gtid\_executed system variable. gtid\_purged holds the GTIDs of all transactions that have been applied on the server, but do not exist on any binary log file on the server. [mysqldump](#page-152-0) therefore adds the GTIDs for the transactions that were executed on the source server, so that the target server records these transactions as applied, although it does not have them in its binary logs. --set-gtid-purged also controls the inclusion of a SET @@SESSION.sql\_log\_bin=0 statement, which disables binary logging while the dump file is being reloaded. This statement prevents new GTIDs from being generated and assigned to the transactions in the dump file as they are executed, so that the original GTIDs for the transactions are used.

If you do not set the --set-gtid-purged option, the default is that a SET @@GLOBAL.gtid\_purged statement is included in the dump output if GTIDs are enabled on the server you are backing up, and the set of GTIDs in the global value of the gtid\_executed system variable is not empty. A SET @@SESSION.sql\_log\_bin=0 statement is also included if GTIDs are enabled on the server.

You can either replace the value of gtid\_purged with a specified GTID set, or add a plus sign (+) to the statement to append a specified GTID set to the GTID set that is already held by gtid\_purged. The SET @@GLOBAL.gtid\_purged statement recorded by [mysqldump](#page-152-0) includes a plus sign (+) in a version-specific comment, such that MySQL adds the GTID set from the dump file to the existing gtid\_purged value.

It is important to note that the value that is included by [mysqldump](#page-152-0) for the SET @@GLOBAL.gtid\_purged statement includes the GTIDs of all transactions in the gtid\_executed set on the server, even those that changed suppressed parts of the database, or other databases on the server that were not included in a partial dump. This can mean that after the gtid\_purged value has been updated on the server where the dump file is replayed, GTIDs are present that do not relate to any data on the target server. If you do not replay any further dump files on the target server, the extraneous GTIDs do not cause any problems with the future operation of the server, but they make it harder to compare or reconcile GTID sets on different servers in the replication topology. If you do replay a further dump file on the target server that contains the same GTIDs (for example, another partial dump from the same origin server), any SET @@GLOBAL.gtid\_purged statement in the second dump file fails. In this case, either remove the statement manually before replaying the dump file, or output the dump file without the statement.

Before MySQL 8.0.32: Using this option with the [--single-transaction](#page-187-0) option could lead to inconsistencies in the output. If --set-gtid-purged=ON is required, it can be used with [--lock](#page-186-2)[all-tables](#page-186-2), but this can prevent parallel queries while [mysqldump](#page-152-0) is being run.

If the SET @@GLOBAL.gtid\_purged statement would not have the desired result on your target server, you can exclude the statement from the output, or (from MySQL 8.0.17) include it but comment it out so that it is not actioned automatically. You can also include the statement but manually edit it in the dump file to achieve the desired result.

The possible values for the --set-gtid-purged option are as follows:

AUTO The default value. If GTIDs are enabled on the server you are backing up and gtid\_executed is not empty, SET @@GLOBAL.gtid\_purged is added to the output, containing the GTID set from gtid\_executed. If GTIDs are enabled, SET @@SESSION.sql\_log\_bin=0 is added to the output. If GTIDs are not enabled on the server, the statements are not added to the output.

OFF SET @@GLOBAL.gtid\_purged is not added to the output, and SET @@SESSION.sql\_log\_bin=0 is not added to the output. For a server where GTIDs are not in use, use this option or AUTO. Only use this option for a server where GTIDs are in use if you are sure that the required GTID set is already present in gtid\_purged on the target server and should not be changed, or if you plan to identify and add any missing GTIDs manually.

ON If GTIDs are enabled on the server you are backing up, SET @@GLOBAL.gtid\_purged is added to the output (unless gtid\_executed is empty), and SET @@SESSION.sql\_log\_bin=0 is added to the output. An error occurs if you set this option but GTIDs are not enabled on the server. For a server where GTIDs are in use, use this option or AUTO, unless you are sure that the GTIDs in gtid\_executed are not needed on the target server.

COMMENTED Available from MySQL 8.0.17. If GTIDs are enabled on the server you are backing up, SET @@GLOBAL.gtid\_purged is added to the output (unless gtid\_executed is empty), but it is commented out. This means that the value of gtid\_executed is available in the output, but no action is taken automatically when the dump file is reloaded. SET @@SESSION.sql\_log\_bin=0 is added to the output, and it is not commented out. With COMMENTED, you can control the use of the gtid\_executed set manually or through automation. For example, you might prefer to do this if you are migrating data to another server that already has different active databases.

## <span id="page-177-0"></span>**Format Options**

The following options specify how to represent the entire dump file or certain kinds of data in the dump file. They also control whether certain optional information is written to the dump file.

<span id="page-177-1"></span>• [--compact](#page-177-1)

| Command-Line Format | compact |
|---------------------|---------|
|---------------------|---------|

Produce more compact output. This option enables the [--skip-add-drop-table](#page-168-0), [--skip-add](#page-185-4)[locks](#page-185-4), [--skip-comments](#page-170-4), [--skip-disable-keys](#page-183-3), and [--skip-set-charset](#page-171-6) options.

<span id="page-177-2"></span>• [--compatible=](#page-177-2)name

| Command-Line Format | compatible=name[,name,] |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | ''                      |
| Valid Values        | ansi                    |

Produce output that is more compatible with other database systems or with older MySQL servers. The only permitted value for this option is ansi, which has the same meaning as the corresponding option for setting the server SQL mode. See Section 7.1.11, "Server SQL Modes".

<span id="page-177-3"></span>• [--complete-insert](#page-177-3), -c

| Command-Line Format | complete-insert |
|---------------------|-----------------|
|---------------------|-----------------|

Use complete INSERT statements that include column names.

<span id="page-177-4"></span>• [--create-options](#page-177-4)

| Command-Line Format | create-options |
|---------------------|----------------|

Include all MySQL-specific table options in the CREATE TABLE statements.

<span id="page-177-5"></span>• [--fields-terminated-by=...](#page-177-5), [--fields-enclosed-by=...](#page-177-5), [--fields-optionally](#page-177-5)[enclosed-by=...](#page-177-5), [--fields-escaped-by=...](#page-177-5)

| Command-Line Format | fields-terminated-by=string |
|---------------------|-----------------------------|
| Type                | String                      |

| Command-Line Format | fields-enclosed-by=string |
|---------------------|---------------------------|
| Type                | String                    |

| Command-Line Format | fields-optionally-enclosed<br>by=string |
|---------------------|-----------------------------------------|
| Type                | String                                  |

| Command-Line Format | fields-escaped-by |
|---------------------|-------------------|
| Type                | String            |

These options are used with the [--tab](#page-179-2) option and have the same meaning as the corresponding FIELDS clauses for LOAD DATA. See Section 15.2.9, "LOAD DATA Statement".

### <span id="page-178-0"></span>• [--hex-blob](#page-178-0)

| Command-Line Format | hex-blob |
|---------------------|----------|
|---------------------|----------|

Dump binary columns using hexadecimal notation (for example, 'abc' becomes 0x616263). The affected data types are BINARY, VARBINARY, BLOB types, BIT, all spatial data types, and other nonbinary data types when used with the binary character set.

The [--hex-blob](#page-178-0) option is ignored when the [--tab](#page-179-2) is used.

<span id="page-178-1"></span>• [--lines-terminated-by=...](#page-178-1)

| Command-Line Format | lines-terminated-by=string |
|---------------------|----------------------------|
| Type                | String                     |

This option is used with the [--tab](#page-179-2) option and has the same meaning as the corresponding LINES clause for LOAD DATA. See Section 15.2.9, "LOAD DATA Statement".

### <span id="page-178-2"></span>• [--quote-names](#page-178-2), -Q

| Command-Line Format | quote-names      |
|---------------------|------------------|
| Disabled by         | skip-quote-names |

Quote identifiers (such as database, table, and column names) within ` characters. If the ANSI\_QUOTES SQL mode is enabled, identifiers are quoted within " characters. This option is enabled by default. It can be disabled with --skip-quote-names, but this option should be given after any option such as [--compatible](#page-177-2) that may enable [--quote-names](#page-178-2).

<span id="page-178-3"></span>• [--result-file=](#page-178-3)file\_name, -r file\_name

|                     | 549                   |  |
|---------------------|-----------------------|--|
| Command-Line Format | result-file=file_name |  |
|                     |                       |  |

Direct output to the named file. The result file is created and its previous contents overwritten, even if an error occurs while generating the dump.

This option should be used on Windows to prevent newline \n characters from being converted to \r\n carriage return/newline sequences.

<span id="page-179-0"></span>• [--show-create-skip-secondary-engine=](#page-179-0)value

| Command-Line Format | show-create-skip-secondary-engine |
|---------------------|-----------------------------------|
|---------------------|-----------------------------------|

Excludes the SECONDARY ENGINE clause from CREATE TABLE statements. It does so by enabling the [show\\_create\\_table\\_skip\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_show_create_table_skip_secondary_engine) system variable for the duration of the dump operation. Alternatively, you can enable the [show\\_create\\_table\\_skip\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_show_create_table_skip_secondary_engine) system variable prior to using [mysqldump](#page-152-0).

This option was added in MySQL 8.0.18. Attempting a [mysqldump](#page-152-0) operation with the [--show](#page-179-0)[create-skip-secondary-engine](#page-179-0) option on a release prior to MySQL 8.0.18 that does not support the [show\\_create\\_table\\_skip\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_show_create_table_skip_secondary_engine) variable causes an error.

<span id="page-179-2"></span>• --tab=[dir\\_name](#page-179-2), -T dir\_name

| Command-Line Format | tab=dir_name   |
|---------------------|----------------|
| Type                | Directory name |

Produce tab-separated text-format data files. For each dumped table, [mysqldump](#page-152-0) creates a tbl\_name.sql file that contains the CREATE TABLE statement that creates the table, and the server writes a tbl\_name.txt file that contains its data. The option value is the directory in which to write the files.

![](_page_179_Picture_11.jpeg)

# **Note**

This option should be used only when [mysqldump](#page-152-0) is run on the same machine as the [mysqld](#page-37-0) server. Because the server creates \*.txt files in the directory that you specify, the directory must be writable by the server and the MySQL account that you use must have the FILE privilege. Because [mysqldump](#page-152-0) creates \*.sql in the same directory, it must be writable by your system login account.

By default, the .txt data files are formatted using tab characters between column values and a newline at the end of each line. The format can be specified explicitly using the --fields-xxx and [--lines-terminated-by](#page-178-1) options.

Column values are converted to the character set specified by the [--default-character-set](#page-171-4) option.

<span id="page-179-1"></span>• [--tz-utc](#page-179-1)

| Command-Line Format | tz-utc      |
|---------------------|-------------|
| Disabled by         | skip-tz-utc |

reloaded in the time zones local to the source and destination servers, which can cause the values to change if the servers are in different time zones. --tz-utc also protects against changes due to daylight saving time. --tz-utc is enabled by default. To disable it, use --skip-tz-utc.

<span id="page-180-0"></span>• [--xml](#page-180-0), -X

| Command-Line Format | xml |
|---------------------|-----|
|---------------------|-----|

Write dump output as well-formed XML.

**NULL, 'NULL', and Empty Values**: For a column named column\_name, the NULL value, an empty string, and the string value 'NULL' are distinguished from one another in the output generated by this option as follows.

| Value:                | XML Representation:                                           |
|-----------------------|---------------------------------------------------------------|
| NULL (unknown value)  | <field <br="" name="column_name">xsi:nil="true" /&gt;</field> |
| '' (empty string)     | <field name="column_name"></field>                            |
| 'NULL' (string value) | <field name="column_name">NULL<!--<br-->field&gt;</field>     |

The output from the [mysql](#page-77-0) client when run using the [--xml](#page-106-1) option also follows the preceding rules. (See [Section 6.5.1.1, "mysql Client Options".](#page-78-0))

XML output from [mysqldump](#page-152-0) includes the XML namespace, as shown here:

```
$> mysqldump --xml -u root world City
<?xml version="1.0"?>
<mysqldump xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<database name="world">
<table_structure name="City">
<field Field="ID" Type="int(11)" Null="NO" Key="PRI" Extra="auto_increment" />
<field Field="Name" Type="char(35)" Null="NO" Key="" Default="" Extra="" />
<field Field="CountryCode" Type="char(3)" Null="NO" Key="" Default="" Extra="" />
<field Field="District" Type="char(20)" Null="NO" Key="" Default="" Extra="" />
<field Field="Population" Type="int(11)" Null="NO" Key="" Default="0" Extra="" />
<key Table="City" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="ID"
Collation="A" Cardinality="4079" Null="" Index_type="BTREE" Comment="" />
<options Name="City" Engine="MyISAM" Version="10" Row_format="Fixed" Rows="4079"
Avg_row_length="67" Data_length="273293" Max_data_length="18858823439613951"
Index_length="43008" Data_free="0" Auto_increment="4080"
Create_time="2007-03-31 01:47:01" Update_time="2007-03-31 01:47:02"
Collation="latin1_swedish_ci" Create_options="" Comment="" />
</table_structure>
<table_data name="City">
<row>
<field name="ID">1</field>
<field name="Name">Kabul</field>
<field name="CountryCode">AFG</field>
<field name="District">Kabol</field>
<field name="Population">1780000</field>
</row>
...
<row>
<field name="ID">4079</field>
<field name="Name">Rafah</field>
<field name="CountryCode">PSE</field>
<field name="District">Rafah</field>
<field name="Population">92020</field>
</row>
</table_data>
</database> 551
```

</mysqldump>

## <span id="page-181-0"></span>**Filtering Options**

The following options control which kinds of schema objects are written to the dump file: by category, such as triggers or events; by name, for example, choosing which databases and tables to dump; or even filtering rows from the table data using a WHERE clause.

<span id="page-181-2"></span>• [--all-databases](#page-181-2), -A

| Command-Line Format | all-databases |
|---------------------|---------------|
|---------------------|---------------|

Dump all tables in all databases. This is the same as using the [--databases](#page-181-1) option and naming all the databases on the command line.

![](_page_181_Picture_7.jpeg)

### **Note**

See the [--add-drop-database](#page-167-1) description for information about an incompatibility of that option with [--all-databases](#page-181-2).

Prior to MySQL 8.0, the [--routines](#page-182-2) and [--events](#page-181-3) options for [mysqldump](#page-152-0) and mysqlpump were not required to include stored routines and events when using the [--all-databases](#page-181-2) option: The dump included the mysql system database, and therefore also the mysql.proc and mysql.event tables containing stored routine and event definitions. As of MySQL 8.0, the mysql.event and mysql.proc tables are not used. Definitions for the corresponding objects are stored in data dictionary tables, but those tables are not dumped. To include stored routines and events in a dump made using [--all-databases](#page-181-2), use the [--routines](#page-182-2) and [--events](#page-181-3) options explicitly.

<span id="page-181-1"></span>• [--databases](#page-181-1), -B

| Command-Line Format | databases |
|---------------------|-----------|
|---------------------|-----------|

Dump several databases. Normally, [mysqldump](#page-152-0) treats the first name argument on the command line as a database name and following names as table names. With this option, it treats all name arguments as database names. CREATE DATABASE and USE statements are included in the output before each new database.

This option may be used to dump the performance\_schema database, which normally is not dumped even with the [--all-databases](#page-181-2) option. (Also use the [--skip-lock-tables](#page-186-3) option.)

![](_page_181_Picture_15.jpeg)

### **Note**

See the [--add-drop-database](#page-167-1) description for information about an incompatibility of that option with [--databases](#page-181-1).

<span id="page-181-3"></span>• [--events](#page-181-3), -E

| Command-Line Format | events |
|---------------------|--------|
|---------------------|--------|

Include Event Scheduler events for the dumped databases in the output. This option requires the EVENT privileges for those databases.

The output generated by using --events contains CREATE EVENT statements to create the events.

<span id="page-181-4"></span>• --ignore-error=[error\[,error\]...](#page-181-4)

| Command-Line Format | ignore-error=error[,error] |
|---------------------|----------------------------|
| Type                | String                     |

Ignore the specified errors. The option value is a list of comma-separated error numbers specifying the errors to ignore during [mysqldump](#page-152-0) execution. If the [--force](#page-170-2) option is also given to ignore all errors, [--force](#page-170-2) takes precedence.

<span id="page-182-0"></span>• --ignore-table=[db\\_name.tbl\\_name](#page-182-0)

| Command-Line Format | ignore-table=db_name.tbl_name |
|---------------------|-------------------------------|
| Type                | String                        |

Do not dump the given table, which must be specified using both the database and table names. To ignore multiple tables, use this option multiple times. This option also can be used to ignore views.

<span id="page-182-1"></span>• [--no-data](#page-182-1), -d

| Command-Line Format | no-data |
|---------------------|---------|
|---------------------|---------|

Do not write any table row information (that is, do not dump table contents). This is useful if you want to dump only the CREATE TABLE statement for the table (for example, to create an empty copy of the table by loading the dump file).

<span id="page-182-2"></span>• [--routines](#page-182-2), -R

| Command-Line Format | routines |
|---------------------|----------|
|---------------------|----------|

Include stored routines (procedures and functions) for the dumped databases in the output. This option requires the global SELECT privilege.

The output generated by using --routines contains CREATE PROCEDURE and CREATE FUNCTION statements to create the routines.

<span id="page-182-3"></span>• [--skip-generated-invisible-primary-key](#page-182-3)

| Command-Line Format | skip-generated-invisible-primary<br>key |
|---------------------|-----------------------------------------|
| Type                | Boolean                                 |
| Default Value       | FALSE                                   |

This option is available beginning with MySQL 8.0.30, and causes generated invisible primary keys to be excluded from the output. For more information, see Section 15.1.20.11, "Generated Invisible Primary Keys".

<span id="page-182-5"></span>• [--tables](#page-182-5)

| Command-Line Format | tables |
|---------------------|--------|
|---------------------|--------|

Override the [--databases](#page-181-1) or -B option. [mysqldump](#page-152-0) regards all name arguments following the option as table names.

<span id="page-182-4"></span>• [--triggers](#page-182-4)

| Command-Line Format | triggers      |
|---------------------|---------------|
| Disabled by         | skip-triggers |

Include triggers for each dumped table in the output. This option is enabled by default; disable it with --skip-triggers.

To be able to dump a table's triggers, you must have the TRIGGER privilege for the table.

Multiple triggers are permitted. [mysqldump](#page-152-0) dumps triggers in activation order so that when the dump file is reloaded, triggers are created in the same activation order. However, if a [mysqldump](#page-152-0) dump file contains multiple triggers for a table that have the same trigger event and action time, an error occurs for attempts to load the dump file into an older server that does not support multiple triggers. (For a workaround, see [Downgrade Notes](https://dev.mysql.com/doc/refman/5.7/en/downgrading-to-previous-series.md); you can convert triggers to be compatible with older servers.)

<span id="page-183-4"></span>• --where='[where\\_condition](#page-183-4)', -w 'where\_condition'

| Command-Line Format | where='where_condition' |
|---------------------|-------------------------|
|                     |                         |

Dump only rows selected by the given WHERE condition. Quotes around the condition are mandatory if it contains spaces or other characters that are special to your command interpreter.

### Examples:

```
--where="user='jimf'"
-w"userid>1"
-w"userid<1"
```

# <span id="page-183-0"></span>**Performance Options**

The following options are the most relevant for the performance particularly of the restore operations. For large data sets, restore operation (processing the INSERT statements in the dump file) is the most time-consuming part. When it is urgent to restore data quickly, plan and test the performance of this stage in advance. For restore times measured in hours, you might prefer an alternative backup and restore solution, such as MySQL Enterprise Backup for InnoDB-only and mixed-use databases.

Performance is also affected by the [transactional options](#page-185-0), primarily for the dump operation.

<span id="page-183-2"></span>• [--column-statistics](#page-183-2)

| Command-Line Format | column-statistics |
|---------------------|-------------------|
| Type                | Boolean           |
| Default Value       | OFF               |

Add ANALYZE TABLE statements to the output to generate histogram statistics for dumped tables when the dump file is reloaded. This option is disabled by default because histogram generation for large tables can take a long time.

<span id="page-183-3"></span>• [--disable-keys](#page-183-3), -K

| Command-Line Format | disable-keys |
|---------------------|--------------|

<span id="page-183-1"></span>For each table, surround the INSERT statements with /\*!40000 ALTER TABLE tbl\_name DISABLE KEYS \*/; and /\*!40000 ALTER TABLE tbl\_name ENABLE KEYS \*/; statements. This makes loading the dump file faster because the indexes are created after all rows are inserted. This option is effective only for nonunique indexes of MyISAM tables.

| Command-Line Format | extended-insert      |
|---------------------|----------------------|
| Disabled by         | skip-extended-insert |

Write INSERT statements using multiple-row syntax that includes several VALUES lists. This results in a smaller dump file and speeds up inserts when the file is reloaded.

<span id="page-184-0"></span>• [--insert-ignore](#page-184-0)

| Command-Line Format |               |
|---------------------|---------------|
|                     | insert-ignore |

Write INSERT IGNORE statements rather than INSERT statements.

<span id="page-184-1"></span>• [--max-allowed-packet=](#page-184-1)value

| Command-Line Format | max-allowed-packet=value |
|---------------------|--------------------------|
| Type                | Numeric                  |
| Default Value       | 25165824                 |

The maximum size of the buffer for client/server communication. The default is 24MB, the maximum is 1GB.

![](_page_184_Picture_9.jpeg)

### **Note**

The value of this option is specific to [mysqldump](#page-152-0) and should not be confused with the MySQL server's max\_allowed\_packet system variable; the server value cannot be exceeded by a single packet from [mysqldump](#page-152-0), regardless of any setting for the [mysqldump](#page-152-0) option, even if the latter is larger.

<span id="page-184-2"></span>• [--mysqld-long-query-time=](#page-184-2)value

| Command-Line Format | mysqld-long-query-time=value |
|---------------------|------------------------------|
| Type                | Numeric                      |
| Default Value       | Server global setting        |

Set the session value of the long\_query\_time system variable. Use this option, which is available from MySQL 8.0.30, if you want to increase the time allowed for queries from [mysqldump](#page-152-0) before they are logged to the slow query log file. [mysqldump](#page-152-0) performs a full table scan, which means its queries can often exceed a global long\_query\_time setting that is useful for regular queries. The default global setting is 10 seconds.

You can use [--mysqld-long-query-time](#page-184-2) to specify a session value from 0 (meaning that every query from [mysqldump](#page-152-0) is logged to the slow query log) to 31536000, which is 365 days in seconds. For [mysqldump](#page-152-0)'s option, you can only specify whole seconds. When you do not specify this option, the server's global setting applies to [mysqldump](#page-152-0)'s queries.

<span id="page-184-3"></span>• [--net-buffer-length=](#page-184-3)value

| Command-Line Format | net-buffer-length=value |  |
|---------------------|-------------------------|--|
| Type                | 555<br>Numeric          |  |

| Default Value | 16384 |
|---------------|-------|
|---------------|-------|

The initial size of the buffer for client/server communication. When creating multiple-row INSERT statements (as with the [--extended-insert](#page-183-1) or [--opt](#page-185-2) option), [mysqldump](#page-152-0) creates rows up to [--net-buffer-length](#page-184-3) bytes long. If you increase this variable, ensure that the MySQL server net\_buffer\_length system variable has a value at least this large.

<span id="page-185-5"></span>• [--network-timeout](#page-185-5), -M

| Command-Line Format | network-timeout[={0 1}] |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | TRUE                    |

Enable large tables to be dumped by setting [--max-allowed-packet](#page-184-1) to its maximum value and network read and write timeouts to a large value. This option is enabled by default. To disable it, use [--skip-network-timeout](#page-185-5).

<span id="page-185-2"></span>• [--opt](#page-185-2)

| Command-Line Format | opt      |
|---------------------|----------|
| Disabled by         | skip-opt |

This option, enabled by default, is shorthand for the combination of [--add-drop-table](#page-168-0) [--add](#page-185-4)[locks](#page-185-4) [--create-options](#page-177-4) [--disable-keys](#page-183-3) [--extended-insert](#page-183-1) [--lock-tables](#page-186-3) [--quick](#page-185-1) [--set-charset](#page-171-6). It gives a fast dump operation and produces a dump file that can be reloaded into a MySQL server quickly.

Because the --opt option is enabled by default, you only specify its converse, the [--skip-opt](#page-185-3) to turn off several default settings. See the discussion of mysqldump [option groups](#page-188-0) for information about selectively enabling or disabling a subset of the options affected by --opt.

<span id="page-185-1"></span>• [--quick](#page-185-1), -q

| Command-Line Format | quick      |
|---------------------|------------|
| Disabled by         | skip-quick |

This option is useful for dumping large tables. It forces [mysqldump](#page-152-0) to retrieve rows for a table from the server a row at a time rather than retrieving the entire row set and buffering it in memory before writing it out.

<span id="page-185-3"></span>• [--skip-opt](#page-185-3)

| Command-Line Format | skip-opt |
|---------------------|----------|
|---------------------|----------|

See the description for the [--opt](#page-185-2) option.

# <span id="page-185-0"></span>**Transactional Options**

The following options trade off the performance of the dump operation, against the reliability and consistency of the exported data.

<span id="page-185-4"></span>• [--add-locks](#page-185-4)

| Command-Line Format | add-locks |
|---------------------|-----------|
|---------------------|-----------|

Surround each table dump with LOCK TABLES and UNLOCK TABLES statements. This results in faster inserts when the dump file is reloaded. See Section 10.2.5.1, "Optimizing INSERT Statements".

<span id="page-186-0"></span>• [--flush-logs](#page-186-0), -F

| Command-Line Format | flush-logs |
|---------------------|------------|
|---------------------|------------|

Flush the MySQL server log files before starting the dump. This option requires the RELOAD privilege. If you use this option in combination with the [--all-databases](#page-181-2) option, the logs are flushed for each database dumped. The exception is when using [--lock-all-tables](#page-186-2), [-](#page-174-2) [source-data](#page-174-2) or [--master-data](#page-175-0), or [--single-transaction](#page-187-0). In these cases, the logs are flushed only once, corresponding to the moment that all tables are locked by FLUSH TABLES WITH READ LOCK. If you want your dump and the log flush to happen at exactly the same moment, you should use --flush-logs together with [--lock-all-tables](#page-186-2), [--source-data](#page-174-2) or [--master](#page-175-0)[data](#page-175-0), or [--single-transaction](#page-187-0).

<span id="page-186-1"></span>• [--flush-privileges](#page-186-1)

| Command-Line Format | flush-privileges |
|---------------------|------------------|
|---------------------|------------------|

Add a FLUSH PRIVILEGES statement to the dump output after dumping the mysql database. This option should be used any time the dump contains the mysql database and any other database that depends on the data in the mysql database for proper restoration.

Because the dump file contains a FLUSH PRIVILEGES statement, reloading the file requires privileges sufficient to execute that statement.

![](_page_186_Picture_9.jpeg)

### **Note**

For upgrades to MySQL 5.7 or higher from older versions, do not use - flush-privileges. For upgrade instructions in this case, see Section 3.5, "Changes in MySQL 8.0".

<span id="page-186-2"></span>• [--lock-all-tables](#page-186-2), -x

| Command-Line Format | lock-all-tables |
|---------------------|-----------------|
|---------------------|-----------------|

Lock all tables across all databases. This is achieved by acquiring a global read lock for the duration of the whole dump. This option automatically turns off [--single-transaction](#page-187-0) and [--lock](#page-186-3)[tables](#page-186-3).

<span id="page-186-3"></span>• [--lock-tables](#page-186-3), -l

| Command-Line Format | lock-tables |
|---------------------|-------------|
|---------------------|-------------|

For each dumped database, lock all tables to be dumped before dumping them. The tables are locked with READ LOCAL to permit concurrent inserts in the case of MyISAM tables. For transactional tables such as InnoDB, [--single-transaction](#page-187-0) is a much better option than --lock-tables because it does not need to lock the tables at all.

Because --lock-tables locks tables for each database separately, this option does not guarantee that the tables in the dump file are logically consistent between databases. Tables in different databases may be dumped in completely different states.

Some options, such as [--opt](#page-185-2), automatically enable --lock-tables. If you want to override this, use --skip-lock-tables at the end of the option list.

<span id="page-187-1"></span>• [--no-autocommit](#page-187-1)

| Command-Line Format | no-autocommit |
|---------------------|---------------|
|---------------------|---------------|

Enclose the INSERT statements for each dumped table within SET autocommit = 0 and COMMIT statements.

<span id="page-187-2"></span>• [--order-by-primary](#page-187-2)

| Command-Line Format | order-by-primary |
|---------------------|------------------|
|---------------------|------------------|

Dump each table's rows sorted by its primary key, or by its first unique index, if such an index exists. This is useful when dumping a MyISAM table to be loaded into an InnoDB table, but makes the dump operation take considerably longer.

<span id="page-187-3"></span>• [--shared-memory-base-name=](#page-187-3)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-187-0"></span>• [--single-transaction](#page-187-0)

| Command-Line Format | single-transaction |
|---------------------|--------------------|

This option sets the transaction isolation mode to REPEATABLE READ and sends a START TRANSACTION SQL statement to the server before dumping data. It is useful only with transactional tables such as InnoDB, because then it dumps the consistent state of the database at the time when START TRANSACTION was issued without blocking any applications.

The RELOAD or FLUSH\_TABLES privilege is required with [--single-transaction](#page-187-0) if both gtid\_mode=ON and gtid\_purged=ON|AUTO. This requirement was added in MySQL 8.0.32.

When using this option, you should keep in mind that only InnoDB tables are dumped in a consistent state. For example, any MyISAM or MEMORY tables dumped while using this option may still change state.

While a [--single-transaction](#page-187-0) dump is in process, to ensure a valid dump file (correct table contents and binary log coordinates), no other connection should use the following statements: ALTER TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE. A consistent read is not isolated from those statements, so use of them on a table to be dumped can cause the

SELECT that is performed by [mysqldump](#page-152-0) to retrieve the table contents to obtain incorrect contents or fail.

The --single-transaction option and the [--lock-tables](#page-186-3) option are mutually exclusive because LOCK TABLES causes any pending transactions to be committed implicitly.

Before 8.0.32: Using --single-transaction together with the [--set-gtid-purged](#page-175-1) option was not recommended; doing so could lead to inconsistencies in the output of [mysqldump](#page-152-0).

To dump large tables, combine the --single-transaction option with the [--quick](#page-185-1) option.

## <span id="page-188-0"></span>**Option Groups**

- The [--opt](#page-185-2) option turns on several settings that work together to perform a fast dump operation. All of these settings are on by default, because --opt is on by default. Thus you rarely if ever specify --opt. Instead, you can turn these settings off as a group by specifying --skip-opt, then optionally re-enable certain settings by specifying the associated options later on the command line.
- The [--compact](#page-177-1) option turns off several settings that control whether optional statements and comments appear in the output. Again, you can follow this option with other options that re-enable certain settings, or turn all the settings on by using the --skip-compact form.

When you selectively enable or disable the effect of a group option, order is important because options are processed first to last. For example, [--disable-keys](#page-183-3) [--lock-tables](#page-186-3) [--skip-opt](#page-185-3) would not have the intended effect; it is the same as [--skip-opt](#page-185-3) by itself.

## <span id="page-188-1"></span>**Examples**

To make a backup of an entire database:

```
mysqldump db_name > backup-file.sql
```

To load the dump file back into the server:

```
mysql db_name < backup-file.sql
```

Another way to reload the dump file:

```
mysql -e "source /path-to-backup/backup-file.sql" db_name
```

[mysqldump](#page-152-0) is also very useful for populating databases by copying data from one MySQL server to another:

```
mysqldump --opt db_name | mysql --host=remote_host -C db_name
```

You can dump several databases with one command:

```
mysqldump --databases db_name1 [db_name2 ...] > my_databases.sql
```

To dump all databases, use the [--all-databases](#page-181-2) option:

```
mysqldump --all-databases > all_databases.sql
```

For InnoDB tables, [mysqldump](#page-152-0) provides a way of making an online backup:

```
mysqldump --all-databases --master-data --single-transaction > all_databases.sql
```

Or, in MySQL 8.0.26 and later:

```
mysqldump --all-databases --source-data --single-transaction > all_databases.sql
```

This backup acquires a global read lock on all tables (using FLUSH TABLES WITH READ LOCK) at the beginning of the dump. As soon as this lock has been acquired, the binary log coordinates are read and the lock is released. If long updating statements are running when the FLUSH statement is issued, the MySQL server may get stalled until those statements finish. After that, the dump becomes lock free and does not disturb reads and writes on the tables. If the update statements that the MySQL server receives are short (in terms of execution time), the initial lock period should not be noticeable, even with many updates.

For point-in-time recovery (also known as "roll-forward," when you need to restore an old backup and replay the changes that happened since that backup), it is often useful to rotate the binary log (see Section 7.4.4, "The Binary Log") or at least know the binary log coordinates to which the dump corresponds:

```
mysqldump --all-databases --master-data=2 > all_databases.sql
```

Or, in MySQL 8.0.26 and later:

```
mysqldump --all-databases --source-data=2 > all_databases.sql
```

Or:

```
mysqldump --all-databases --flush-logs --master-data=2 > all_databases.sql
```

Or, in MySQL 8.0.26 and later:

```
mysqldump --all-databases --flush-logs --source-data=2 > all_databases.sql
```

The [--source-data](#page-174-2) or [--master-data](#page-175-0) option can be used simultaneously with the [--single](#page-187-0)[transaction](#page-187-0) option, which provides a convenient way to make an online backup suitable for use prior to point-in-time recovery if tables are stored using the InnoDB storage engine.

For more information on making backups, see Section 9.2, "Database Backup Methods", and Section 9.3, "Example Backup and Recovery Strategy".

- To select the effect of [--opt](#page-185-2) except for some features, use the --skip option for each feature. To disable extended inserts and memory buffering, use [--opt](#page-185-2) [--skip-extended-insert](#page-183-1) [--skip](#page-185-1)[quick](#page-185-1). (Actually, [--skip-extended-insert](#page-183-1) [--skip-quick](#page-185-1) is sufficient because [--opt](#page-185-2) is on by default.)
- To reverse [--opt](#page-185-2) for all features except disabling of indexes and table locking, use [--skip-opt](#page-185-3) [-](#page-183-3) [disable-keys](#page-183-3) [--lock-tables](#page-186-3).

## <span id="page-189-1"></span>**Restrictions**

[mysqldump](#page-152-0) does not dump the performance\_schema or sys schema by default. To dump any of these, name them explicitly on the command line. You can also name them with the [--databases](#page-181-1) option. For performance\_schema, also use the [--skip-lock-tables](#page-186-3) option.

```
mysqldump does not dump the INFORMATION_SCHEMA schema.
```

[mysqldump](#page-152-0) does not dump InnoDB CREATE TABLESPACE statements.

[mysqldump](#page-152-0) does not dump the NDB Cluster ndbinfo information database.

[mysqldump](#page-152-0) includes statements to recreate the general\_log and slow\_query\_log tables for dumps of the mysql database. Log table contents are not dumped.

If you encounter problems backing up views due to insufficient privileges, see Section 27.9, "Restrictions on Views" for a workaround.

# <span id="page-189-0"></span>**6.5.5 mysqlimport — A Data Import Program**

The [mysqlimport](#page-189-0) client provides a command-line interface to the LOAD DATA SQL statement. Most options to [mysqlimport](#page-189-0) correspond directly to clauses of LOAD DATA syntax. See Section 15.2.9, "LOAD DATA Statement".

Invoke [mysqlimport](#page-189-0) like this:

```
mysqlimport [options] db_name textfile1 [textfile2 ...]
```

For each text file named on the command line, [mysqlimport](#page-189-0) strips any extension from the file name and uses the result to determine the name of the table into which to import the file's contents. For example, files named patient.txt, patient.text, and patient all would be imported into a table named patient.

[mysqlimport](#page-189-0) supports the following options, which can be specified on the command line or in the [mysqlimport] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.16 mysqlimport Options**

| Option Name                   | Description                                                                      | Deprecated |
|-------------------------------|----------------------------------------------------------------------------------|------------|
| bind-address                  | Use specified network interface<br>to connect to MySQL Server                    |            |
| character-sets-dir            | Directory where character sets<br>can be found                                   |            |
| columns                       | This option takes a comma<br>separated list of column names<br>as its value      |            |
| compress                      | Compress all information sent<br>between client and server                       | Yes        |
| compression-algorithms        | Permitted compression<br>algorithms for connections to<br>server                 |            |
| debug                         | Write debugging log                                                              |            |
| debug-check                   | Print debugging information<br>when program exits                                |            |
| debug-info                    | Print debugging information,<br>memory, and CPU statistics<br>when program exits |            |
| default-auth                  | Authentication plugin to use                                                     |            |
| default-character-set         | Specify default character set                                                    |            |
| defaults-extra-file           | Read named option file in<br>addition to usual option files                      |            |
| defaults-file                 | Read only named option file                                                      |            |
| defaults-group-suffix         | Option group suffix value                                                        |            |
| delete                        | Empty the table before importing<br>the text file                                |            |
| enable-cleartext-plugin       | Enable cleartext authentication<br>plugin                                        |            |
| fields-enclosed-by            | This option has the same<br>meaning as the corresponding<br>clause for LOAD DATA |            |
| fields-escaped-by             | This option has the same<br>meaning as the corresponding<br>clause for LOAD DATA |            |
| fields-optionally-enclosed-by | This option has the same<br>meaning as the corresponding<br>clause for LOAD DATA |            |
| fields-terminated-by          | This option has the same<br>meaning as the corresponding<br>clause for LOAD DATA |            |

| Option Name            | Description                                                                                                            | Deprecated |
|------------------------|------------------------------------------------------------------------------------------------------------------------|------------|
| force                  | Continue even if an SQL error<br>occurs                                                                                |            |
| get-server-public-key  | Request RSA public key from<br>server                                                                                  |            |
| help                   | Display help message and exit                                                                                          |            |
| host                   | Host on which MySQL server is<br>located                                                                               |            |
| ignore                 | See the description for the<br>replace option                                                                          |            |
| ignore-lines           | Ignore the first N lines of the data<br>file                                                                           |            |
| lines-terminated-by    | This option has the same<br>meaning as the corresponding<br>clause for LOAD DATA                                       |            |
| local                  | Read input files locally from the<br>client host                                                                       |            |
| lock-tables            | Lock all tables for writing before<br>processing any text files                                                        |            |
| login-path             | Read login path options<br>from .mylogin.cnf                                                                           |            |
| low-priority           | Use LOW_PRIORITY when<br>loading the table                                                                             |            |
| no-defaults            | Read no option files                                                                                                   |            |
| password               | Password to use when<br>connecting to server                                                                           |            |
| password1              | First multifactor authentication<br>password to use when<br>connecting to server                                       |            |
| password2              | Second multifactor authentication<br>password to use when<br>connecting to server                                      |            |
| password3              | Third multifactor authentication<br>password to use when<br>connecting to server                                       |            |
| pipe                   | Connect to server using named<br>pipe (Windows only)                                                                   |            |
| plugin-dir             | Directory where plugins are<br>installed                                                                               |            |
| port                   | TCP/IP port number for<br>connection                                                                                   |            |
| print-defaults         | Print default options                                                                                                  |            |
| protocol               | Transport protocol to use                                                                                              |            |
| replace                | Thereplace andignore<br>options control handling of input<br>rows that duplicate existing rows<br>on unique key values |            |
| server-public-key-path | Path name to file containing RSA<br>public key                                                                         |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| shared-memory-base-name                      | Shared-memory name for<br>shared-memory connections<br>(Windows only)             |            |
| silent                                       | Produce output only when errors<br>occur                                          |            |
| socket                                       | Unix socket file or Windows<br>named pipe to use                                  |            |
| ssl-ca                                       | File that contains list of trusted<br>SSL Certificate Authorities                 |            |
| ssl-capath                                   | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files |            |
| ssl-cert                                     | File that contains X.509<br>certificate                                           |            |
| ssl-cipher                                   | Permissible ciphers for<br>connection encryption                                  |            |
| ssl-crl                                      | File that contains certificate<br>revocation lists                                |            |
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                      |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                     | Yes        |
| ssl-key                                      | File that contains X.509 key                                                      |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                 |            |
| ssl-session-data                             | File that contains SSL session<br>data                                            |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                        |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                     |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                            |            |
| use-threads                                  | Number of threads for parallel<br>file-loading                                    |            |
| user                                         | MySQL user name to use when<br>connecting to server                               |            |
| verbose                                      | Verbose mode                                                                      |            |
| version                                      | Display version information and<br>exit                                           |            |
| zstd-compression-level                       | Compression level for<br>connections to server that use<br>zstd compression       |            |

<span id="page-193-5"></span>• [--help](#page-193-5), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-193-0"></span>• [--bind-address=](#page-193-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-193-1"></span>• [--character-sets-dir=](#page-193-1)dir\_name

| Command-Line Format | character-sets-dir=path |  |
|---------------------|-------------------------|--|
| Type                | String                  |  |
| Default Value       | [none]                  |  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-193-2"></span>• --columns=[column\\_list](#page-193-2), -c column\_list

| Command-Line Format | columns=column_list |
|---------------------|---------------------|
|---------------------|---------------------|

This option takes a list of comma-separated column names as its value. The order of the column names indicates how to match data file columns with table columns.

<span id="page-193-3"></span>• [--compress](#page-193-3), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See [Section 6.2.8,](#page-32-0) ["Connection Compression Control".](#page-32-0)

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

<span id="page-193-4"></span>• [--compression-algorithms=](#page-193-4)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

<span id="page-194-0"></span>• --debug[=[debug\\_options](#page-194-0)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-194-1"></span>• [--debug-check](#page-194-1)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-194-2"></span>• [--debug-info](#page-194-2)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-194-3"></span>• [--default-character-set=](#page-194-3)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String<br>565                      |

### <span id="page-195-0"></span>• [--default-auth=](#page-195-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-195-1"></span>• [--defaults-extra-file=](#page-195-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-195-2"></span>• [--defaults-file=](#page-195-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with [--defaults-file](#page-1-0), client programs read .mylogin.cnf.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-195-3"></span>• [--defaults-group-suffix=](#page-195-3)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlimport](#page-189-0) normally reads the [client] and [mysqlimport] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-195-3), [mysqlimport](#page-189-0) also reads the [client\_other] and [mysqlimport\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

• [--delete](#page-195-4), -D

<span id="page-195-4"></span>

| Command-Line Format | delete |
|---------------------|--------|

### <span id="page-196-0"></span>• [--enable-cleartext-plugin](#page-196-0)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-196-1"></span>• [--fields-terminated-by=...](#page-196-1), [--fields-enclosed-by=...](#page-196-1), [--fields-optionally](#page-196-1)[enclosed-by=...](#page-196-1), [--fields-escaped-by=...](#page-196-1)

| Command-Line Format | fields-terminated-by=string |
|---------------------|-----------------------------|
| Type                | String                      |

| Command-Line Format | fields-enclosed-by=string |
|---------------------|---------------------------|
| Type                | String                    |

| Command-Line Format | fields-optionally-enclosed<br>by=string |
|---------------------|-----------------------------------------|
| Type                | String                                  |

| Command-Line Format | fields-escaped-by |
|---------------------|-------------------|
| Type                | String            |

These options have the same meaning as the corresponding clauses for LOAD DATA. See Section 15.2.9, "LOAD DATA Statement".

### <span id="page-196-2"></span>• [--force](#page-196-2), -f

| Command-Line Format<br>force |  |
|------------------------------|--|
|                              |  |

Ignore errors. For example, if a table for a text file does not exist, continue processing any remaining files. Without [--force](#page-196-2), [mysqlimport](#page-189-0) exits if a table does not exist.

<span id="page-196-3"></span>• [--get-server-public-key](#page-196-3)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

password exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-196-3).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-197-0"></span>• --host=[host\\_name](#page-197-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Import data to the MySQL server on the given host. The default host is localhost.

<span id="page-197-1"></span>• [--ignore](#page-197-1), -i

| Command-Line Format | ignore |
|---------------------|--------|
|---------------------|--------|

See the description for the --replace option.

<span id="page-197-2"></span>• [--ignore-lines=](#page-197-2)N

| Command-Line Format | ignore-lines=# |
|---------------------|----------------|
| Type                | Numeric        |

Ignore the first N lines of the data file.

<span id="page-197-3"></span>• [--lines-terminated-by=...](#page-197-3)

| Command-Line Format | lines-terminated-by=string |
|---------------------|----------------------------|
| Type                | String                     |

This option has the same meaning as the corresponding clause for LOAD DATA. For example, to import Windows files that have lines terminated with carriage return/linefeed pairs, use [--lines](#page-197-3)[terminated-by="\r\n"](#page-197-3). (You might have to double the backslashes, depending on the escaping conventions of your command interpreter.) See Section 15.2.9, "LOAD DATA Statement".

<span id="page-197-4"></span>• [--local](#page-197-4), -L

| Command-Line Format | local   |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

568

By default, files are read by the server on the server host. With this option, [mysqlimport](#page-189-0) reads input files locally on the client host.

Successful use of LOCAL load operations within [mysqlimport](#page-189-0) also requires that the server permits

<span id="page-198-0"></span>• [--lock-tables](#page-186-3), -l

| Command-Line Format | lock-tables |
|---------------------|-------------|
|---------------------|-------------|

Lock all tables for writing before processing any text files. This ensures that all tables are synchronized on the server.

<span id="page-198-1"></span>• [--login-path=](#page-198-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-198-2"></span>• [--low-priority](#page-198-2)

| Command-Line Format | low-priority |
|---------------------|--------------|
|---------------------|--------------|

Use LOW\_PRIORITY when loading the table. This affects only storage engines that use only tablelevel locking (such as MyISAM, MEMORY, and MERGE).

<span id="page-198-3"></span>• [--no-defaults](#page-198-3)

| Command-Line Format<br>no-defaults |  |
|------------------------------------|--|
|------------------------------------|--|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-198-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-198-3) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-198-4"></span>• [--password\[=](#page-198-4)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlimport](#page-189-0) prompts for one. If given, there must be no space between [-](#page-198-4) [password=](#page-198-4) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlimport](#page-189-0) should not prompt for one, use the [--skip-password](#page-198-4) option.

<span id="page-199-0"></span>• [--password1\[=](#page-199-0)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlimport](#page-189-0) prompts for one. If given, there must be no space between [--password1=](#page-199-0) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlimport](#page-189-0) should not prompt for one, use the [--skip-password1](#page-199-0) option.

[--password1](#page-199-0) and [--password](#page-198-4) are synonymous, as are [--skip-password1](#page-199-0) and [--skip](#page-198-4)[password](#page-198-4).

<span id="page-199-1"></span>• [--password2\[=](#page-199-1)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-199-0); see the description of that option for details.

<span id="page-199-2"></span>• [--password3\[=](#page-199-2)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-199-0); see the description of that option for details.

<span id="page-199-3"></span>• [--pipe](#page-199-3), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-199-4"></span>• [--plugin-dir=](#page-199-4)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-195-0) option is used to specify an authentication plugin but [mysqlimport](#page-189-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-199-5"></span>• --port=[port\\_num](#page-199-5), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-0-0"></span>• [--print-defaults](#page-0-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-0-1"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-0-1)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-0-2"></span>• [--replace](#page-0-2), -r

| Command-Line Format | replace |
|---------------------|---------|
|                     |         |

The [--replace](#page-0-2) and --ignore options control handling of input rows that duplicate existing rows on unique key values. If you specify [--replace](#page-0-2), new rows replace existing rows that have the same unique key value. If you specify --ignore, input rows that duplicate an existing row on a unique key value are skipped. If you do not specify either option, an error occurs when a duplicate key value is found, and the rest of the text file is ignored.

<span id="page-0-3"></span>• [--server-public-key-path=](#page-0-3)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-0-3)file\_name is given and specifies a valid public key file, it takes precedence over --get-server-public-key.

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

### <span id="page-1-0"></span>• [--shared-memory-base-name=](#page-1-0)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

### <span id="page-1-1"></span>• [--silent](#page-1-1), -s

| Command-Line Format | silent |
|---------------------|--------|

Silent mode. Produce output only when errors occur.

### <span id="page-1-2"></span>• [--socket=](#page-1-2)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

### • --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

### <span id="page-1-3"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-1-3)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-1-3) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-1-3) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_2_Picture_5.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-1-3) is OFF. In this case, setting [--ssl-fips-mode](#page-1-3) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-2-0"></span>• [--tls-ciphersuites=](#page-2-0)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-2-1"></span>• [--tls-version=](#page-2-1)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-2-2"></span>• --user=[user\\_name](#page-2-2), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

<span id="page-2-3"></span>• [--use-threads=](#page-2-3)N

| Command-Line Format | use-threads=# |
|---------------------|---------------|
| Type                | Numeric       |

Load files in parallel using N threads.

<span id="page-3-0"></span>• [--verbose](#page-3-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|                     |         |

Verbose mode. Print more information about what the program does.

<span id="page-3-1"></span>• [--version](#page-3-1), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-3-2"></span>• [--zstd-compression-level=](#page-3-2)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

This option was added in MySQL 8.0.18.

Here is a sample session that demonstrates use of mysqlimport:

```
$> mysql -e 'CREATE TABLE imptest(id INT, n VARCHAR(30))' test
$> ed
a
100 Max Sydow
101 Count Dracula
.
w imptest.txt
32
q
$> od -c imptest.txt
0000000 1 0 0 \t M a x S y d o w \n 1 0
0000020 1 \t C o u n t D r a c u l a \n
0000040
$> mysqlimport --local test imptest.txt
test.imptest: Records: 2 Deleted: 0 Skipped: 0 Warnings: 0
$> mysql -e 'SELECT * FROM imptest' test
+------+---------------+
| id | n |
+------+---------------+
| 100 | Max Sydow |
| 101 | Count Dracula |
+------+---------------+
```

## <span id="page-3-3"></span>**6.5.6 mysqlpump — A Database Backup Program**

- [mysqlpump Invocation Syntax](#page-5-0)
- [mysqlpump Option Summary](#page-5-1)
- [mysqlpump Option Descriptions](#page-9-0)

- [mysqlpump Object Selection](#page-27-0)
- [mysqlpump Parallel Processing](#page-28-0)
- [mysqlpump Restrictions](#page-29-0)

The [mysqlpump](#page-3-3) client utility performs logical backups, producing a set of SQL statements that can be executed to reproduce the original database object definitions and table data. It dumps one or more MySQL databases for backup or transfer to another SQL server.

![](_page_4_Picture_5.jpeg)

### **Note**

[mysqlpump](#page-3-3) is deprecated as of MySQL 8.0.34; expect it to be removed in a future version of MySQL. You can use such MySQL programs as mysqldump and MySQL Shell to perform logical backups, dump databases, and similar tasks instead.

![](_page_4_Picture_8.jpeg)

#### **Tip**

Consider using the [MySQL Shell dump utilities,](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-dump-instance-schema.md) which provide parallel dumping with multiple threads, file compression, and progress information display, as well as cloud features such as Oracle Cloud Infrastructure Object Storage streaming, and MySQL HeatWave compatibility checks and modifications. Dumps can be easily imported into a MySQL Server instance or a MySQL HeatWave DB System using the [MySQL Shell load dump utilities.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-load-dump.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

[mysqlpump](#page-3-3) features include:

- Parallel processing of databases, and of objects within databases, to speed up the dump process
- Better control over which databases and database objects (tables, stored programs, user accounts) to dump
- Dumping of user accounts as account-management statements (CREATE USER, GRANT) rather than as inserts into the mysql system database
- Capability of creating compressed output
- Progress indicator (the values are estimates)
- For dump file reloading, faster secondary index creation for InnoDB tables by adding indexes after rows are inserted

![](_page_4_Picture_18.jpeg)

#### **Note**

[mysqlpump](#page-3-3) uses MySQL features introduced in MySQL 5.7, and thus assumes use with MySQL 5.7 or higher.

[mysqlpump](#page-3-3) requires at least the SELECT privilege for dumped tables, SHOW VIEW for dumped views, TRIGGER for dumped triggers, and LOCK TABLES if the [--single-transaction](#page-23-0) option is not used. The SELECT privilege on the mysql system database is required to dump user definitions. Certain options might require other privileges as noted in the option descriptions.

To reload a dump file, you must have the privileges required to execute the statements that it contains, such as the appropriate CREATE privileges for objects created by those statements.

![](_page_4_Picture_23.jpeg)

## **Note**

A dump made using PowerShell on Windows with output redirection creates a file that has UTF-16 encoding:

mysqlpump [options] > dump.sql

However, UTF-16 is not permitted as a connection character set (see Section 12.4, "Connection Character Sets and Collations"), so the dump file cannot be loaded correctly. To work around this issue, use the --resultfile option, which creates the output in ASCII format:

```
mysqlpump [options] --result-file=dump.sql
```

## <span id="page-5-0"></span>**mysqlpump Invocation Syntax**

By default, [mysqlpump](#page-3-3) dumps all databases (with certain exceptions noted in [mysqlpump](#page-29-0) [Restrictions](#page-29-0)). To specify this behavior explicitly, use the [--all-databases](#page-10-0) option:

```
mysqlpump --all-databases
```

To dump a single database, or certain tables within that database, name the database on the command line, optionally followed by table names:

```
mysqlpump db_name
mysqlpump db_name tbl_name1 tbl_name2 ...
```

To treat all name arguments as database names, use the [--databases](#page-12-0) option:

```
mysqlpump --databases db_name1 db_name2 ...
```

By default, [mysqlpump](#page-3-3) does not dump user account definitions, even if you dump the mysql system database that contains the grant tables. To dump grant table contents as logical definitions in the form of CREATE USER and GRANT statements, use the [--users](#page-26-0) option and suppress all database dumping:

```
mysqlpump --exclude-databases=% --users
```

In the preceding command, % is a wildcard that matches all database names for the [--exclude](#page-15-0)[databases](#page-15-0) option.

[mysqlpump](#page-3-3) supports several options for including or excluding databases, tables, stored programs, and user definitions. See [mysqlpump Object Selection.](#page-27-0)

To reload a dump file, execute the statements that it contains. For example, use the mysql client:

```
mysqlpump [options] > dump.sql
mysql < dump.sql
```

The following discussion provides additional [mysqlpump](#page-3-3) usage examples.

To see a list of the options [mysqlpump](#page-3-3) supports, issue the command [mysqlpump --help](#page-3-3).

## <span id="page-5-1"></span>**mysqlpump Option Summary**

[mysqlpump](#page-3-3) supports the following options, which can be specified on the command line or in the [mysqlpump] and [client] groups of an option file. (Prior to MySQL 8.0.20, [mysqlpump](#page-3-3) read the [mysql\_dump] group rather than [mysqlpump]. As of 8.0.20, [mysql\_dump] is still accepted but is deprecated.) For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.17 mysqlpump Options**

| Option Name       | Description                                                             | Deprecated |
|-------------------|-------------------------------------------------------------------------|------------|
| add-drop-database | Add DROP DATABASE<br>statement before each CREATE<br>DATABASE statement |            |
| add-drop-table    | Add DROP TABLE statement<br>before each CREATE TABLE<br>statement       |            |

| Option Name            | Description                                                                      | Deprecated |
|------------------------|----------------------------------------------------------------------------------|------------|
| add-drop-user          | Add DROP USER statement<br>before each CREATE USER<br>statement                  |            |
| add-locks              | Surround each table dump with<br>LOCK TABLES and UNLOCK<br>TABLES statements     |            |
| all-databases          | Dump all databases                                                               |            |
| bind-address           | Use specified network interface<br>to connect to MySQL Server                    |            |
| character-sets-dir     | Directory where character sets<br>are installed                                  |            |
| column-statistics      | Write ANALYZE TABLE<br>statements to generate statistics<br>histograms           |            |
| complete-insert        | Use complete INSERT<br>statements that include column<br>names                   |            |
| compress               | Compress all information sent<br>between client and server                       | Yes        |
| compress-output        | Output compression algorithm                                                     |            |
| compression-algorithms | Permitted compression<br>algorithms for connections to<br>server                 |            |
| databases              | Interpret all name arguments as<br>database names                                |            |
| debug                  | Write debugging log                                                              |            |
| debug-check            | Print debugging information<br>when program exits                                |            |
| debug-info             | Print debugging information,<br>memory, and CPU statistics<br>when program exits |            |
| default-auth           | Authentication plugin to use                                                     |            |
| default-character-set  | Specify default character set                                                    |            |
| default-parallelism    | Default number of threads for<br>parallel processing                             |            |
| defaults-extra-file    | Read named option file in<br>addition to usual option files                      |            |
| defaults-file          | Read only named option file                                                      |            |
| defaults-group-suffix  | Option group suffix value                                                        |            |
| defer-table-indexes    | For reloading, defer index<br>creation until after loading table<br>rows         |            |
| events                 | Dump events from dumped<br>databases                                             |            |
| exclude-databases      | Databases to exclude from dump                                                   |            |
|                        |                                                                                  |            |
| exclude-events         | Events to exclude from dump                                                      |            |

| Option Name           | Description                                                                       | Deprecated |
|-----------------------|-----------------------------------------------------------------------------------|------------|
| exclude-tables        | Tables to exclude from dump                                                       |            |
| exclude-triggers      | Triggers to exclude from dump                                                     |            |
| exclude-users         | Users to exclude from dump                                                        |            |
| extended-insert       | Use multiple-row INSERT syntax                                                    |            |
| get-server-public-key | Request RSA public key from<br>server                                             |            |
| help                  | Display help message and exit                                                     |            |
| hex-blob              | Dump binary columns using<br>hexadecimal notation                                 |            |
| host                  | Host on which MySQL server is<br>located                                          |            |
| include-databases     | Databases to include in dump                                                      |            |
| include-events        | Events to include in dump                                                         |            |
| include-routines      | Routines to include in dump                                                       |            |
| include-tables        | Tables to include in dump                                                         |            |
| include-triggers      | Triggers to include in dump                                                       |            |
| include-users         | Users to include in dump                                                          |            |
| insert-ignore         | Write INSERT IGNORE rather<br>than INSERT statements                              |            |
| log-error-file        | Append warnings and errors to<br>named file                                       |            |
| login-path            | Read login path options<br>from .mylogin.cnf                                      |            |
| max-allowed-packet    | Maximum packet length to send<br>to or receive from server                        |            |
| net-buffer-length     | Buffer size for TCP/IP and socket<br>communication                                |            |
| no-create-db          | Do not write CREATE<br>DATABASE statements                                        |            |
| no-create-info        | Do not write CREATE TABLE<br>statements that re-create each<br>dumped table       |            |
| no-defaults           | Read no option files                                                              |            |
| parallel-schemas      | Specify schema-processing<br>parallelism                                          |            |
| password              | Password to use when<br>connecting to server                                      |            |
| password1             | First multifactor authentication<br>password to use when<br>connecting to server  |            |
| password2             | Second multifactor authentication<br>password to use when<br>connecting to server |            |
| password3             | Third multifactor authentication<br>password to use when<br>connecting to server  |            |

| Option Name                             | Description                                                                                   | Deprecated |
|-----------------------------------------|-----------------------------------------------------------------------------------------------|------------|
| plugin-dir                              | Directory where plugins are<br>installed                                                      |            |
| port                                    | TCP/IP port number for<br>connection                                                          |            |
| print-defaults                          | Print default options                                                                         |            |
| protocol                                | Transport protocol to use                                                                     |            |
| replace                                 | Write REPLACE statements<br>rather than INSERT statements                                     |            |
| result-file                             | Direct output to a given file                                                                 |            |
| routines                                | Dump stored routines<br>(procedures and functions) from<br>dumped databases                   |            |
| server-public-key-path                  | Path name to file containing RSA<br>public key                                                |            |
| set-charset                             | Add SET NAMES<br>default_character_set to output                                              |            |
| set-gtid-purged                         | Whether to add SET<br>@@GLOBAL.GTID_PURGED to<br>output                                       |            |
| single-transaction                      | Dump tables within single<br>transaction                                                      |            |
| skip-definer                            | Omit DEFINER and SQL<br>SECURITY clauses from view<br>and stored program CREATE<br>statements |            |
| skip-dump-rows                          | Do not dump table rows                                                                        |            |
| skip-generated-invisible<br>primary-key | Do not dump information about<br>generated invisible primary keys                             |            |
| socket                                  | Unix socket file or Windows<br>named pipe to use                                              |            |
| ssl-ca                                  | File that contains list of trusted<br>SSL Certificate Authorities                             |            |
| ssl-capath                              | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files             |            |
| ssl-cert                                | File that contains X.509<br>certificate                                                       |            |
| ssl-cipher                              | Permissible ciphers for<br>connection encryption                                              |            |
| ssl-crl                                 | File that contains certificate<br>revocation lists                                            |            |
| ssl-crlpath                             | Directory that contains certificate<br>revocation-list files                                  |            |
| ssl-fips-mode                           | Whether to enable FIPS mode<br>on client side                                                 | Yes        |
| ssl-key                                 | File that contains X.509 key                                                                  |            |
|                                         |                                                                                               |            |

| Option Name                                  | Description                                                                 | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------|------------|
| ssl-mode                                     | Desired security state of<br>connection to server                           |            |
| ssl-session-data                             | File that contains SSL session<br>data                                      |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                  |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections               |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                      |            |
| triggers                                     | Dump triggers for each dumped<br>table                                      |            |
| tz-utc                                       | Add SET TIME_ZONE='+00:00'<br>to dump file                                  |            |
| user                                         | MySQL user name to use when<br>connecting to server                         |            |
| users                                        | Dump user accounts                                                          |            |
| version                                      | Display version information and<br>exit                                     |            |
| watch-progress                               | Display progress indicator                                                  |            |
| zstd-compression-level                       | Compression level for<br>connections to server that use<br>zstd compression |            |

## <span id="page-9-3"></span><span id="page-9-0"></span>**mysqlpump Option Descriptions**

• [--help](#page-9-3), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-9-1"></span>• [--add-drop-database](#page-9-1)

| Command-Line Format | add-drop-database |
|---------------------|-------------------|
|---------------------|-------------------|

Write a DROP DATABASE statement before each CREATE DATABASE statement.

<span id="page-9-2"></span>![](_page_9_Picture_9.jpeg)

#### **Note**

In MySQL 8.0, the mysql schema is considered a system schema that cannot be dropped by end users. If [--add-drop-database](#page-9-1) is used with [--all-databases](#page-10-0) or with [--databases](#page-12-0) where the list of schemas to be dumped includes mysql, the dump file contains a DROP DATABASE `mysql` statement that causes an error when the dump file is reloaded.

Instead, to use [--add-drop-database](#page-9-1), use [--databases](#page-12-0) with a list of schemas to be dumped, where the list does not include mysql.

| Command-Line Format | add-drop-table |
|---------------------|----------------|

Write a DROP TABLE statement before each CREATE TABLE statement.

<span id="page-10-1"></span>• [--add-drop-user](#page-10-1)

| Command-Line Format | add-drop-user |
|---------------------|---------------|
|                     |               |

Write a DROP USER statement before each CREATE USER statement.

<span id="page-10-2"></span>• [--add-locks](#page-10-2)

| Command-Line Format | add-locks |
|---------------------|-----------|
|---------------------|-----------|

Surround each table dump with LOCK TABLES and UNLOCK TABLES statements. This results in faster inserts when the dump file is reloaded. See Section 10.2.5.1, "Optimizing INSERT Statements".

This option does not work with parallelism because INSERT statements from different tables can be interleaved and UNLOCK TABLES following the end of the inserts for one table could release locks on tables for which inserts remain.

[--add-locks](#page-10-2) and [--single-transaction](#page-23-0) are mutually exclusive.

<span id="page-10-0"></span>• [--all-databases](#page-10-0), -A

| Command-Line Format | all-databases |
|---------------------|---------------|
|---------------------|---------------|

Dump all databases (with certain exceptions noted in [mysqlpump Restrictions\)](#page-29-0). This is the default behavior if no other is specified explicitly.

[--all-databases](#page-10-0) and [--databases](#page-12-0) are mutually exclusive.

![](_page_10_Picture_15.jpeg)

#### **Note**

See the [--add-drop-database](#page-9-1) description for information about an incompatibility of that option with [--all-databases](#page-10-0).

Prior to MySQL 8.0, the --routines and --events options for mysqldump and [mysqlpump](#page-3-3) were not required to include stored routines and events when using the --all-databases option: The dump included the mysql system database, and therefore also the mysql.proc and mysql.event tables containing stored routine and event definitions. As of MySQL 8.0, the mysql.event and mysql.proc tables are not used. Definitions for the corresponding objects are stored in data dictionary tables, but those tables are not dumped. To include stored routines and events in a dump made using --all-databases, use the --routines and --events options explicitly.

<span id="page-10-3"></span>• [--bind-address=](#page-10-3)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

581

<span id="page-11-0"></span>• [--character-sets-dir=](#page-11-0)path

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-11-1"></span>• [--column-statistics](#page-11-1)

| Command-Line Format | column-statistics |
|---------------------|-------------------|
| Type                | Boolean           |
| Default Value       | OFF               |

Add ANALYZE TABLE statements to the output to generate histogram statistics for dumped tables when the dump file is reloaded. This option is disabled by default because histogram generation for large tables can take a long time.

<span id="page-11-2"></span>• [--complete-insert](#page-11-2)

| Command-Line Format | complete-insert |
|---------------------|-----------------|
|---------------------|-----------------|

Write complete INSERT statements that include column names.

<span id="page-11-3"></span>• [--compress](#page-11-3), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-11-4"></span>• [--compress-output=](#page-11-4)algorithm

| Command-Line Format | compress-output=algorithm |
|---------------------|---------------------------|
| Type                | Enumeration               |
| Valid Values        | LZ4                       |
|                     | ZLIB                      |

By default, [mysqlpump](#page-3-3) does not compress output. This option specifies output compression using the specified algorithm. Permitted algorithms are LZ4 and ZLIB.

To uncompress compressed output, you must have an appropriate utility. If the system commands lz4 and openssl zlib are not available, MySQL distributions include [lz4\\_decompress](#page-149-0) and [zlib\\_decompress](#page-151-0) utilities that can be used to decompress [mysqlpump](#page-3-3) output that was compressed using the [--compress-output=LZ4](#page-11-4) and [--compress-output=ZLIB](#page-11-4) options. For more information, see [Section 6.8.1, "lz4\\_decompress — Decompress mysqlpump LZ4-Compressed](#page-149-0) [Output"](#page-149-0), and [Section 6.8.3, "zlib\\_decompress — Decompress mysqlpump ZLIB-Compressed](#page-151-0) [Output"](#page-151-0).

<span id="page-12-1"></span>• [--compression-algorithms=](#page-12-1)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

This option was added in MySQL 8.0.18.

<span id="page-12-0"></span>• [--databases](#page-12-0), -B

Normally, [mysqlpump](#page-3-3) treats the first name argument on the command line as a database name and any following names as table names. With this option, it treats all name arguments as database names. CREATE DATABASE statements are included in the output before each new database.

[--all-databases](#page-10-0) and [--databases](#page-12-0) are mutually exclusive.

![](_page_12_Picture_11.jpeg)

## **Note**

See the [--add-drop-database](#page-9-1) description for information about an incompatibility of that option with [--databases](#page-12-0).

<span id="page-12-2"></span>• --debug[=[debug\\_options](#page-12-2)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]      |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | d:t:O,/tmp/mysqlpump.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:O,/tmp/mysqlpump.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-12-3"></span>• [--debug-check](#page-12-3)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-13-0"></span>• [--debug-info](#page-13-0), -T

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-13-1"></span>• [--default-auth=](#page-13-1)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-13-2"></span>• [--default-character-set=](#page-13-2)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |
| Default Value       | utf8                               |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration". If no character set is specified, [mysqlpump](#page-3-3) uses utf8mb4.

<span id="page-13-3"></span>• [--default-parallelism=](#page-13-3)N

| Command-Line Format | default-parallelism=N |
|---------------------|-----------------------|
| Type                | Integer               |
| Default Value       | 2                     |

The default number of threads for each parallel processing queue. The default is 2.

The [--parallel-schemas](#page-19-3) option also affects parallelism and can be used to override the default number of threads. For more information, see [mysqlpump Parallel Processing](#page-28-0).

With [--default-parallelism=0](#page-13-3) and no [--parallel-schemas](#page-19-3) options, [mysqlpump](#page-3-3) runs as a single-threaded process and creates no queues.

With parallelism enabled, it is possible for output from different databases to be interleaved.

<span id="page-13-4"></span>• [--defaults-extra-file=](#page-13-4)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-14-0"></span>• [--defaults-file=](#page-14-0)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-14-1"></span>• [--defaults-group-suffix=](#page-14-1)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlpump](#page-3-3) normally reads the [client] and [mysqlpump] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-14-1), [mysqlpump](#page-3-3) also reads the [client\_other] and [mysqlpump\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-14-2"></span>• [--defer-table-indexes](#page-14-2)

| Command-Line Format | defer-table-indexes |
|---------------------|---------------------|
| Type                | Boolean             |
| Default Value       | TRUE                |

In the dump output, defer index creation for each table until after its rows have been loaded. This works for all storage engines, but for InnoDB applies only for secondary indexes.

This option is enabled by default; use [--skip-defer-table-indexes](#page-14-2) to disable it.

<span id="page-14-3"></span>• [--events](#page-14-3)

| Command-Line Format | events  |
|---------------------|---------|
| Type                | Boolean |

| Default Value | TRUE |
|---------------|------|
|---------------|------|

Include Event Scheduler events for the dumped databases in the output. Event dumping requires the EVENT privileges for those databases.

The output generated by using [--events](#page-14-3) contains CREATE EVENT statements to create the events.

This option is enabled by default; use [--skip-events](#page-14-3) to disable it.

<span id="page-15-0"></span>• [--exclude-databases=](#page-15-0)db\_list

| Command-Line Format | exclude-databases=db_list |
|---------------------|---------------------------|
| Type                | String                    |

Do not dump the databases in db\_list, which is a list of one or more comma-separated database names. Multiple instances of this option are additive. For more information, see [mysqlpump Object](#page-27-0) [Selection](#page-27-0).

<span id="page-15-1"></span>• [--exclude-events=](#page-15-1)event\_list

| Command-Line Format | exclude-events=event_list |
|---------------------|---------------------------|
| Type                | String                    |

Do not dump the databases in event\_list, which is a list of one or more comma-separated event names. Multiple instances of this option are additive. For more information, see [mysqlpump Object](#page-27-0) [Selection](#page-27-0).

<span id="page-15-2"></span>• [--exclude-routines=](#page-15-2)routine\_list

| Command-Line Format | exclude-routines=routine_list |
|---------------------|-------------------------------|
| Type                | String                        |

Do not dump the events in routine\_list, which is a list of one or more comma-separated routine (stored procedure or function) names. Multiple instances of this option are additive. For more information, see [mysqlpump Object Selection.](#page-27-0)

<span id="page-15-3"></span>• [--exclude-tables=](#page-15-3)table\_list

| Command-Line Format | exclude-tables=table_list |
|---------------------|---------------------------|
| Type                | String                    |

Do not dump the tables in table\_list, which is a list of one or more comma-separated table names. Multiple instances of this option are additive. For more information, see [mysqlpump Object](#page-27-0) [Selection](#page-27-0).

<span id="page-15-4"></span>• [--exclude-triggers=](#page-15-4)trigger\_list

| Command-Line Format | exclude-triggers=trigger_list |
|---------------------|-------------------------------|

| Type | String |
|------|--------|
|------|--------|

Do not dump the triggers in trigger\_list, which is a list of one or more comma-separated trigger names. Multiple instances of this option are additive. For more information, see [mysqlpump Object](#page-27-0) [Selection](#page-27-0).

<span id="page-16-0"></span>• [--exclude-users=](#page-16-0)user\_list

| Command-Line Format | exclude-users=user_list |
|---------------------|-------------------------|
| Type                | String                  |

Do not dump the user accounts in user\_list, which is a list of one or more comma-separated account names. Multiple instances of this option are additive. For more information, see [mysqlpump](#page-27-0) [Object Selection.](#page-27-0)

<span id="page-16-1"></span>• [--extended-insert=](#page-16-1)N

| Command-Line Format | extended-insert=N |
|---------------------|-------------------|
|---------------------|-------------------|

Write INSERT statements using multiple-row syntax that includes several VALUES lists. This results in a smaller dump file and speeds up inserts when the file is reloaded.

The option value indicates the number of rows to include in each INSERT statement. The default is 250. A value of 1 produces one INSERT statement per table row.

<span id="page-16-2"></span>• [--get-server-public-key](#page-16-2)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-22-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-16-2).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-16-3"></span>• [--hex-blob](#page-16-3)

| Command-Line Format | hex-blob |
|---------------------|----------|

Dump binary columns using hexadecimal notation (for example, 'abc' becomes 0x616263). The affected data types are BINARY, VARBINARY, BLOB types, BIT, all spatial data types, and other nonbinary data types when used with the binary character set.

<span id="page-16-4"></span>• --host=[host\\_name](#page-16-4), -h host\_name

| Command-Line Format | host |
|---------------------|------|
|---------------------|------|

Dump data from the MySQL server on the given host.

<span id="page-17-0"></span>• [--include-databases=](#page-17-0)db\_list

| Command-Line Format | include-databases=db_list |
|---------------------|---------------------------|
| Type                | String                    |

Dump the databases in db\_list, which is a list of one or more comma-separated database names. The dump includes all objects in the named databases. Multiple instances of this option are additive. For more information, see [mysqlpump Object Selection.](#page-27-0)

<span id="page-17-1"></span>• [--include-events=](#page-17-1)event\_list

| Command-Line Format | include-events=event_list |
|---------------------|---------------------------|
| Type                | String                    |

Dump the events in event\_list, which is a list of one or more comma-separated event names. Multiple instances of this option are additive. For more information, see [mysqlpump Object Selection.](#page-27-0)

<span id="page-17-2"></span>• [--include-routines=](#page-17-2)routine\_list

| Command-Line Format | include-routines=routine_list |
|---------------------|-------------------------------|
| Type                | String                        |

Dump the routines in routine\_list, which is a list of one or more comma-separated routine (stored procedure or function) names. Multiple instances of this option are additive. For more information, see [mysqlpump Object Selection.](#page-27-0)

<span id="page-17-3"></span>• [--include-tables=](#page-17-3)table\_list

| Command-Line Format | include-tables=table_list |
|---------------------|---------------------------|
| Type                | String                    |

Dump the tables in table\_list, which is a list of one or more comma-separated table names. Multiple instances of this option are additive. For more information, see [mysqlpump Object Selection.](#page-27-0)

<span id="page-17-4"></span>• [--include-triggers=](#page-17-4)trigger\_list

| Command-Line Format | include-triggers=trigger_list |
|---------------------|-------------------------------|
| Type                | String                        |

Dump the triggers in trigger\_list, which is a list of one or more comma-separated trigger names. Multiple instances of this option are additive. For more information, see [mysqlpump Object Selection.](#page-27-0)

<span id="page-17-5"></span>• [--include-users=](#page-17-5)user\_list

| Command-Line Format | include-users=user_list |
|---------------------|-------------------------|

Dump the user accounts in user\_list, which is a list of one or more comma-separated user names. Multiple instances of this option are additive. For more information, see [mysqlpump Object](#page-27-0) [Selection](#page-27-0).

### <span id="page-18-0"></span>• [--insert-ignore](#page-18-0)

| Command-Line Format | insert-ignore |
|---------------------|---------------|
|---------------------|---------------|

Write INSERT IGNORE statements rather than INSERT statements.

### <span id="page-18-1"></span>• [--log-error-file=](#page-18-1)file\_name

| Command-Line Format | log-error-file=file_name |
|---------------------|--------------------------|
| Type                | File name                |

Log warnings and errors by appending them to the named file. If this option is not given, [mysqlpump](#page-3-3) writes warnings and errors to the standard error output.

## <span id="page-18-2"></span>• [--login-path=](#page-18-2)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-97-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-97-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

### <span id="page-18-3"></span>• [--max-allowed-packet=](#page-18-3)N

| Command-Line Format | max-allowed-packet=N |
|---------------------|----------------------|
| Type                | Numeric              |
| Default Value       | 25165824             |

The maximum size of the buffer for client/server communication. The default is 24MB, the maximum is 1GB.

### <span id="page-18-4"></span>• [--net-buffer-length=](#page-18-4)N

| Command-Line Format | net-buffer-length=N |
|---------------------|---------------------|
| Type                | Numeric             |
| Default Value       | 1047552             |

The initial size of the buffer for client/server communication. When creating multiple-row INSERT statements (as with the [--extended-insert](#page-16-1) option), [mysqlpump](#page-3-3) creates rows up to N bytes long. If you use this option to increase the value, ensure that the MySQL server net\_buffer\_length system variable has a value at least this large.

<span id="page-19-0"></span>• [--no-create-db](#page-19-0)

| Command-Line Format | no-create-db |
|---------------------|--------------|
|---------------------|--------------|

Suppress any CREATE DATABASE statements that might otherwise be included in the output.

<span id="page-19-1"></span>• [--no-create-info](#page-19-1), -t

| Command-Line Format | no-create-info |
|---------------------|----------------|
|---------------------|----------------|

Do not write CREATE TABLE statements that create each dumped table.

<span id="page-19-2"></span>• [--no-defaults](#page-19-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-19-2) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-19-2) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-97-0) utility. See [Section 6.6.7,](#page-97-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-97-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-19-3"></span>• [--parallel-schemas=\[](#page-19-3)N:]db\_list

| Command-Line Format | parallel-schemas=[N:]schema_list |
|---------------------|----------------------------------|
| Type                | String                           |

Create a queue for processing the databases in db\_list, which is a list of one or more commaseparated database names. If N is given, the queue uses N threads. If N is not given, the [-](#page-13-3) [default-parallelism](#page-13-3) option determines the number of queue threads.

Multiple instances of this option create multiple queues. [mysqlpump](#page-3-3) also creates a default queue to use for databases not named in any [--parallel-schemas](#page-19-3) option, and for dumping user definitions if command options select them. For more information, see [mysqlpump Parallel](#page-28-0) [Processing](#page-28-0).

<span id="page-19-4"></span>• [--password\[=](#page-19-4)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

[password=](#page-19-4) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlpump](#page-3-3) should not prompt for one, use the [--skip-password](#page-19-4) option.

<span id="page-20-0"></span>• [--password1\[=](#page-20-0)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlpump](#page-3-3) prompts for one. If given, there must be no space between [--password1=](#page-20-0) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlpump](#page-3-3) should not prompt for one, use the [--skip-password1](#page-20-0) option.

[--password1](#page-20-0) and [--password](#page-19-4) are synonymous, as are [--skip-password1](#page-20-0) and [--skip](#page-19-4)[password](#page-19-4).

<span id="page-20-1"></span>• [--password2\[=](#page-20-1)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-20-0); see the description of that option for details.

<span id="page-20-2"></span>• [--password3\[=](#page-20-2)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-20-0); see the description of that option for details.

<span id="page-20-3"></span>• [--plugin-dir=](#page-20-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-13-1) option is used to specify an authentication plugin but [mysqlpump](#page-3-3) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-20-4"></span>• --port=[port\\_num](#page-20-4), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

## <span id="page-21-0"></span>• [--print-defaults](#page-21-0)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-21-1"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-21-1)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

## <span id="page-21-2"></span>• [--replace](#page-21-2)

| Command-Line Format | replace |
|---------------------|---------|
|---------------------|---------|

Write REPLACE statements rather than INSERT statements.

<span id="page-21-3"></span>• [--result-file=](#page-21-3)file\_name

| Command-Line Format | result-file=file_name |
|---------------------|-----------------------|
| Type                | File name             |

Direct output to the named file. The result file is created and its previous contents overwritten, even if an error occurs while generating the dump.

This option should be used on Windows to prevent newline \n characters from being converted to \r\n carriage return/newline sequences.

<span id="page-21-4"></span>• [--routines](#page-21-4)

| Command-Line Format | routines |
|---------------------|----------|
| Type                | Boolean  |

| Default Value | TRUE |
|---------------|------|
|---------------|------|

Include stored routines (procedures and functions) for the dumped databases in the output. This option requires the global SELECT privilege.

The output generated by using [--routines](#page-21-4) contains CREATE PROCEDURE and CREATE FUNCTION statements to create the routines.

This option is enabled by default; use [--skip-routines](#page-21-4) to disable it.

<span id="page-22-0"></span>• [--server-public-key-path=](#page-22-0)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-22-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-16-2).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-22-1"></span>• [--set-charset](#page-22-1)

| Command-Line Format | set-charset |
|---------------------|-------------|
|---------------------|-------------|

Write SET NAMES default\_character\_set to the output.

This option is enabled by default. To disable it and suppress the SET NAMES statement, use [-](#page-22-1) [skip-set-charset](#page-22-1).

<span id="page-22-2"></span>• --set-gtid-purged=value

| Command-Line Format | set-gtid-purged=value |
|---------------------|-----------------------|
| Type                | Enumeration           |
| Default Value       | AUTO                  |
| Valid Values        | OFF                   |
|                     | ON                    |
|                     | AUTO                  |

This option enables control over global transaction ID (GTID) information written to the dump file, by indicating whether to add a SET @@GLOBAL.gtid\_purged statement to the output. This option may also cause a statement to be written to the output that disables binary logging while the dump file is being reloaded.

The following table shows the permitted option values. The default value is AUTO.

| Value | Meaning                                                                                       |
|-------|-----------------------------------------------------------------------------------------------|
| OFF   | Add no SET statement to the output.                                                           |
| ON    | Add a SET statement to the output. An error<br>occurs if GTIDs are not enabled on the server. |
| AUTO  | Add a SET statement to the output if GTIDs are<br>enabled on the server.                      |

The --set-gtid-purged option has the following effect on binary logging when the dump file is reloaded:

- --set-gtid-purged=OFF: SET @@SESSION.SQL\_LOG\_BIN=0; is not added to the output.
- --set-gtid-purged=ON: SET @@SESSION.SQL\_LOG\_BIN=0; is added to the output.
- --set-gtid-purged=AUTO: SET @@SESSION.SQL\_LOG\_BIN=0; is added to the output if GTIDs are enabled on the server you are backing up (that is, if AUTO evaluates to ON).
- <span id="page-23-0"></span>• [--single-transaction](#page-23-0)

| Command-Line Format | single-transaction |
|---------------------|--------------------|
|---------------------|--------------------|

This option sets the transaction isolation mode to REPEATABLE READ and sends a START TRANSACTION SQL statement to the server before dumping data. It is useful only with transactional tables such as InnoDB, because then it dumps the consistent state of the database at the time when START TRANSACTION was issued without blocking any applications.

When using this option, you should keep in mind that only InnoDB tables are dumped in a consistent state. For example, any MyISAM or MEMORY tables dumped while using this option may still change state.

While a [--single-transaction](#page-23-0) dump is in process, to ensure a valid dump file (correct table contents and binary log coordinates), no other connection should use the following statements: ALTER TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE. A consistent read is not isolated from those statements, so use of them on a table to be dumped can cause the SELECT that is performed by [mysqlpump](#page-3-3) to retrieve the table contents to obtain incorrect contents or fail.

[--add-locks](#page-10-2) and [--single-transaction](#page-23-0) are mutually exclusive.

<span id="page-23-1"></span>• [--skip-definer](#page-23-1)

| Command-Line Format | skip-definer |
|---------------------|--------------|
| Type                | Boolean      |
| Default Value       | FALSE        |

Omit DEFINER and SQL SECURITY clauses from the CREATE statements for views and stored programs. The dump file, when reloaded, creates objects that use the default DEFINER and SQL SECURITY values. See Section 27.6, "Stored Object Access Control".

<span id="page-23-2"></span>• [--skip-dump-rows](#page-23-2), -d

| Command-Line Format | skip-dump-rows |
|---------------------|----------------|
| Type                | Boolean        |

| Default Value | FALSE |
|---------------|-------|
|---------------|-------|

Do not dump table rows.

<span id="page-24-0"></span>• [--skip-generated-invisible-primary-key](#page-24-0)

| Command-Line Format | skip-generated-invisible-primary<br>key |
|---------------------|-----------------------------------------|
| Type                | Boolean                                 |
| Default Value       | FALSE                                   |

This option is available beginning with MySQL 8.0.30, and causes generated invisible primary keys (GIPKs) to be excluded from the dump. See Section 15.1.20.11, "Generated Invisible Primary Keys", for more information about GIPKs and GIPK mode.

<span id="page-24-1"></span>• [--socket=](#page-24-1)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-24-2"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-24-3"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-24-3)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-24-3) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-24-3) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.

• STRICT: Enable "strict" FIPS mode.

![](_page_25_Picture_2.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-24-3) is OFF. In this case, setting [--ssl-fips-mode](#page-24-3) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-25-0"></span>• [--tls-ciphersuites=](#page-25-0)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-25-1"></span>• [--tls-version=](#page-25-1)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-25-2"></span>• [--triggers](#page-25-2)

| Command-Line Format | triggers |
|---------------------|----------|
| Type                | Boolean  |
| Default Value       | TRUE     |

Include triggers for each dumped table in the output.

This option is enabled by default; use [--skip-triggers](#page-25-2) to disable it.

<span id="page-25-3"></span>• [--tz-utc](#page-25-3)

| Command-Line Format | tz-utc |
|---------------------|--------|

This option enables TIMESTAMP columns to be dumped and reloaded between servers in different time zones. [mysqlpump](#page-3-3) sets its connection time zone to UTC and adds SET TIME\_ZONE='+00:00' to the dump file. Without this option, TIMESTAMP columns are dumped and reloaded in the time zones local to the source and destination servers, which can cause the values to change if the servers are in different time zones. [--tz-utc](#page-25-3) also protects against changes due to daylight saving time.

This option is enabled by default; use [--skip-tz-utc](#page-25-3) to disable it.

<span id="page-26-1"></span>• --user=[user\\_name](#page-26-1), -u user\_name

| Command-Line Format | user=user_name |
|---------------------|----------------|
| Type                | String         |

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin with MySQL 8.0.31 or later, you should grant this user the SKIP\_QUERY\_REWRITE privilege.

### <span id="page-26-0"></span>• [--users](#page-26-0)

| Command-Line Format | users   |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

Dump user accounts as logical definitions in the form of CREATE USER and GRANT statements.

User definitions are stored in the grant tables in the mysql system database. By default, [mysqlpump](#page-3-3) does not include the grant tables in mysql database dumps. To dump the contents of the grant tables as logical definitions, use the [--users](#page-26-0) option and suppress all database dumping:

mysqlpump --exclude-databases=% --users

<span id="page-26-2"></span>• [--version](#page-26-2), -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

### <span id="page-26-3"></span>• [--watch-progress](#page-26-3)

| Command-Line Format | watch-progress |
|---------------------|----------------|
| Type                | Boolean        |
| Default Value       | TRUE           |

Periodically display a progress indicator that provides information about the completed and total number of tables, rows, and other objects.

This option is enabled by default; use [--skip-watch-progress](#page-26-3) to disable it.

<span id="page-26-4"></span>• [--zstd-compression-level=](#page-26-4)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.

The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

This option was added in MySQL 8.0.18.

## <span id="page-27-0"></span>**mysqlpump Object Selection**

[mysqlpump](#page-3-3) has a set of inclusion and exclusion options that enable filtering of several object types and provide flexible control over which objects to dump:

- [--include-databases](#page-17-0) and [--exclude-databases](#page-15-0) apply to databases and all objects within them.
- [--include-tables](#page-17-3) and [--exclude-tables](#page-15-3) apply to tables. These options also affect triggers associated with tables unless the trigger-specific options are given.
- [--include-triggers](#page-17-4) and [--exclude-triggers](#page-15-4) apply to triggers.
- [--include-routines](#page-17-2) and [--exclude-routines](#page-15-2) apply to stored procedures and functions. If a routine option matches a stored procedure name, it also matches a stored function of the same name.
- [--include-events](#page-17-1) and [--exclude-events](#page-15-1) apply to Event Scheduler events.
- [--include-users](#page-17-5) and [--exclude-users](#page-16-0) apply to user accounts.

Any inclusion or exclusion option may be given multiple times. The effect is additive. Order of these options does not matter.

The value of each inclusion and exclusion option is a list of comma-separated names of the appropriate object type. For example:

```
--exclude-databases=test,world
--include-tables=customer,invoice
```

Wildcard characters are permitted in the object names:

- % matches any sequence of zero or more characters.
- \_ matches any single character.

For example, [--include-tables=t%,\\_\\_tmp](#page-17-3) matches all table names that begin with t and all fivecharacter table names that end with tmp.

For users, a name specified without a host part is interpreted with an implied host of %. For example, u1 and u1@% are equivalent. This is the same equivalence that applies in MySQL generally (see Section 8.2.4, "Specifying Account Names").

Inclusion and exclusion options interact as follows:

- By default, with no inclusion or exclusion options, [mysqlpump](#page-3-3) dumps all databases (with certain exceptions noted in [mysqlpump Restrictions](#page-29-0)).
- If inclusion options are given in the absence of exclusion options, only the objects named as included are dumped.
- If exclusion options are given in the absence of inclusion options, all objects are dumped except those named as excluded.
- If inclusion and exclusion options are given, all objects named as excluded and not named as included are not dumped. All other objects are dumped.

If multiple databases are being dumped, it is possible to name tables, triggers, and routines in a specific database by qualifying the object names with the database name. The following command dumps databases db1 and db2, but excludes tables db1.t1 and db2.t2:

```
mysqlpump --include-databases=db1,db2 --exclude-tables=db1.t1,db2.t2
```

The following options provide alternative ways to specify which databases to dump:

- The [--all-databases](#page-10-0) option dumps all databases (with certain exceptions noted in [mysqlpump](#page-29-0) [Restrictions](#page-29-0)). It is equivalent to specifying no object options at all (the default [mysqlpump](#page-3-3) action is to dump everything).
  - [--include-databases=%](#page-17-0) is similar to [--all-databases](#page-10-0), but selects all databases for dumping, even those that are exceptions for [--all-databases](#page-10-0).
- The [--databases](#page-12-0) option causes [mysqlpump](#page-3-3) to treat all name arguments as names of databases to dump. It is equivalent to an [--include-databases](#page-17-0) option that names the same databases.

## <span id="page-28-0"></span>**mysqlpump Parallel Processing**

[mysqlpump](#page-3-3) can use parallelism to achieve concurrent processing. You can select concurrency between databases (to dump multiple databases simultaneously) and within databases (to dump multiple objects from a given database simultaneously).

By default, [mysqlpump](#page-3-3) sets up one queue with two threads. You can create additional queues and control the number of threads assigned to each one, including the default queue:

• [--default-parallelism=](#page-13-3)N specifies the default number of threads used for each queue. In the absence of this option, N is 2.

The default queue always uses the default number of threads. Additional queues use the default number of threads unless you specify otherwise.

• [--parallel-schemas=\[](#page-19-3)N:]db\_list sets up a processing queue for dumping the databases named in db\_list and optionally specifies how many threads the queue uses. db\_list is a list of comma-separated database names. If the option argument begins with N:, the queue uses N threads. Otherwise, the [--default-parallelism](#page-13-3) option determines the number of queue threads.

Multiple instances of the [--parallel-schemas](#page-19-3) option create multiple queues.

Names in the database list are permitted to contain the same % and \_ wildcard characters supported for filtering options (see [mysqlpump Object Selection](#page-27-0)).

[mysqlpump](#page-3-3) uses the default queue for processing any databases not named explicitly with a [-](#page-19-3) [parallel-schemas](#page-19-3) option, and for dumping user definitions if command options select them.

In general, with multiple queues, [mysqlpump](#page-3-3) uses parallelism between the sets of databases processed by the queues, to dump multiple databases simultaneously. For a queue that uses multiple threads, [mysqlpump](#page-3-3) uses parallelism within databases, to dump multiple objects from a given database simultaneously. Exceptions can occur; for example, [mysqlpump](#page-3-3) may block queues while it obtains from the server lists of objects in databases.

With parallelism enabled, it is possible for output from different databases to be interleaved. For example, INSERT statements from multiple tables dumped in parallel can be interleaved; the statements are not written in any particular order. This does not affect reloading because output statements qualify object names with database names or are preceded by USE statements as required.

The granularity for parallelism is a single database object. For example, a single table cannot be dumped in parallel using multiple threads.

Examples:

```
mysqlpump --parallel-schemas=db1,db2 --parallel-schemas=db3
```

[mysqlpump](#page-3-3) sets up a queue to process db1 and db2, another queue to process db3, and a default queue to process all other databases. All queues use two threads.

```
mysqlpump --parallel-schemas=db1,db2 --parallel-schemas=db3
 --default-parallelism=4
```

This is the same as the previous example except that all queues use four threads.

```
mysqlpump --parallel-schemas=5:db1,db2 --parallel-schemas=3:db3
```

The queue for db1 and db2 uses five threads, the queue for db3 uses three threads, and the default queue uses the default of two threads.

As a special case, with [--default-parallelism=0](#page-13-3) and no [--parallel-schemas](#page-19-3) options, [mysqlpump](#page-3-3) runs as a single-threaded process and creates no queues.

## <span id="page-29-0"></span>**mysqlpump Restrictions**

[mysqlpump](#page-3-3) does not dump the performance\_schema, ndbinfo, or sys schema by default. To dump any of these, name them explicitly on the command line. You can also name them with the [-](#page-12-0) [databases](#page-12-0) or [--include-databases](#page-17-0) option.

[mysqlpump](#page-3-3) does not dump the INFORMATION\_SCHEMA schema.

[mysqlpump](#page-3-3) does not dump InnoDB CREATE TABLESPACE statements.

[mysqlpump](#page-3-3) dumps user accounts in logical form using CREATE USER and GRANT statements (for example, when you use the [--include-users](#page-17-5) or [--users](#page-26-0) option). For this reason, dumps of the mysql system database do not by default include the grant tables that contain user definitions: user, db, tables\_priv, columns\_priv, procs\_priv, or proxies\_priv. To dump any of the grant tables, name the mysql database followed by the table names:

mysqlpump mysql user db ...

## <span id="page-29-1"></span>**6.5.7 mysqlshow — Display Database, Table, and Column Information**

The [mysqlshow](#page-29-1) client can be used to quickly see which databases exist, their tables, or a table's columns or indexes.

[mysqlshow](#page-29-1) provides a command-line interface to several SQL SHOW statements. See Section 15.7.7, "SHOW Statements". The same information can be obtained by using those statements directly. For example, you can issue them from the mysql client program.

Invoke [mysqlshow](#page-29-1) like this:

```
mysqlshow [options] [db_name [tbl_name [col_name]]]
```

- If no database is given, a list of database names is shown.
- If no table is given, all matching tables in the database are shown.
- If no column is given, all matching columns and column types in the table are shown.

The output displays only the names of those databases, tables, or columns for which you have some privileges.

If the last argument contains shell or SQL wildcard characters (\*, ?, %, or \_), only those names that are matched by the wildcard are shown. If a database name contains any underscores, those should be escaped with a backslash (some Unix shells require two) to get a list of the proper tables or columns. \* and ? characters are converted into SQL % and \_ wildcard characters. This might cause some confusion when you try to display the columns for a table with a \_ in the name, because in this case, [mysqlshow](#page-29-1) shows you only the table names that match the pattern. This is easily fixed by adding an extra % last on the command line as a separate argument.

[mysqlshow](#page-29-1) supports the following options, which can be specified on the command line or in the [mysqlshow] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.18 mysqlshow Options**

| Option Name             | Description                                                                       | Deprecated |
|-------------------------|-----------------------------------------------------------------------------------|------------|
| bind-address            | Use specified network interface<br>to connect to MySQL Server                     |            |
| character-sets-dir      | Directory where character sets<br>can be found                                    |            |
| compress                | Compress all information sent<br>between client and server                        | Yes        |
| compression-algorithms  | Permitted compression<br>algorithms for connections to<br>server                  |            |
| count                   | Show the number of rows per<br>table                                              |            |
| debug                   | Write debugging log                                                               |            |
| debug-check             | Print debugging information<br>when program exits                                 |            |
| debug-info              | Print debugging information,<br>memory, and CPU statistics<br>when program exits  |            |
| default-auth            | Authentication plugin to use                                                      |            |
| default-character-set   | Specify default character set                                                     |            |
| defaults-extra-file     | Read named option file in<br>addition to usual option files                       |            |
| defaults-file           | Read only named option file                                                       |            |
| defaults-group-suffix   | Option group suffix value                                                         |            |
| enable-cleartext-plugin | Enable cleartext authentication<br>plugin                                         |            |
| get-server-public-key   | Request RSA public key from<br>server                                             |            |
| help                    | Display help message and exit                                                     |            |
| host                    | Host on which MySQL server is<br>located                                          |            |
| keys                    | Show table indexes                                                                |            |
| login-path              | Read login path options<br>from .mylogin.cnf                                      |            |
| no-defaults             | Read no option files                                                              |            |
| password                | Password to use when<br>connecting to server                                      |            |
| password1               | First multifactor authentication<br>password to use when<br>connecting to server  |            |
| password2               | Second multifactor authentication<br>password to use when<br>connecting to server |            |
|                         |                                                                                   |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| password3                                    | Third multifactor authentication<br>password to use when<br>connecting to server  |            |
| pipe                                         | Connect to server using named<br>pipe (Windows only)                              |            |
| plugin-dir                                   | Directory where plugins are<br>installed                                          |            |
| port                                         | TCP/IP port number for<br>connection                                              |            |
| print-defaults                               | Print default options                                                             |            |
| protocol                                     | Transport protocol to use                                                         |            |
| server-public-key-path                       | Path name to file containing RSA<br>public key                                    |            |
| shared-memory-base-name                      | Shared-memory name for<br>shared-memory connections<br>(Windows only)             |            |
| show-table-type                              | Show a column indicating the<br>table type                                        |            |
| socket                                       | Unix socket file or Windows<br>named pipe to use                                  |            |
| ssl-ca                                       | File that contains list of trusted<br>SSL Certificate Authorities                 |            |
| ssl-capath                                   | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files |            |
| ssl-cert                                     | File that contains X.509<br>certificate                                           |            |
| ssl-cipher                                   | Permissible ciphers for<br>connection encryption                                  |            |
| ssl-crl                                      | File that contains certificate<br>revocation lists                                |            |
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                      |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                     | Yes        |
| ssl-key                                      | File that contains X.509 key                                                      |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                 |            |
| ssl-session-data                             | File that contains SSL session<br>data                                            |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                        |            |
| status                                       | Display extra information about<br>each table                                     |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                     |            |

| Option Name            | Description                                                                 | Deprecated |
|------------------------|-----------------------------------------------------------------------------|------------|
| tls-version            | Permissible TLS protocols for<br>encrypted connections                      |            |
| user                   | MySQL user name to use when<br>connecting to server                         |            |
| verbose                | Verbose mode                                                                |            |
| version                | Display version information and<br>exit                                     |            |
| zstd-compression-level | Compression level for<br>connections to server that use<br>zstd compression |            |

### <span id="page-32-4"></span>• [--help](#page-32-4), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

## Display a help message and exit.

<span id="page-32-0"></span>• [--bind-address=](#page-32-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-32-1"></span>• [--character-sets-dir=](#page-32-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-32-2"></span>• [--compress](#page-32-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-32-3"></span>• [--compression-algorithms=](#page-32-3)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |

| Valid Values | zlib         |
|--------------|--------------|
|              | zstd         |
|              | uncompressed |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

This option was added in MySQL 8.0.18.

<span id="page-33-0"></span>• [--count](#page-33-0)

| Command-Line Format | count |
|---------------------|-------|
|---------------------|-------|

Show the number of rows per table. This can be slow for non-MyISAM tables.

<span id="page-33-1"></span>• --debug[=[debug\\_options](#page-33-1)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-33-2"></span>• [--debug-check](#page-33-2)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-33-3"></span>• [--debug-info](#page-33-3)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

## <span id="page-34-1"></span>• [--default-character-set=](#page-34-1)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

### <span id="page-34-0"></span>• [--default-auth=](#page-34-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

## <span id="page-34-2"></span>• [--defaults-extra-file=](#page-34-2)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-34-3"></span>• [--defaults-file=](#page-34-3)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

### <span id="page-34-4"></span>• [--defaults-group-suffix=](#page-34-4)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlshow](#page-29-1) normally reads the [client] and [mysqlshow] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-34-4), [mysqlshow](#page-29-1) also reads the [client\_other] and [mysqlshow\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-34-5"></span>• [--enable-cleartext-plugin](#page-34-5)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-35-0"></span>• [--get-server-public-key](#page-35-0)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the RSA public key that it uses for key pair-based password exchange. This option applies to clients that connect to the server using an account that authenticates with the caching\_sha2\_password authentication plugin. For connections by such accounts, the server does not send the public key to the client unless requested. The option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not needed, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-38-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-35-0).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-35-1"></span>• --host=[host\\_name](#page-35-1), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-35-2"></span>• [--keys](#page-35-2), -k

| Command-Line Format | keys |
|---------------------|------|
|---------------------|------|

Show table indexes.

<span id="page-35-3"></span>• [--login-path=](#page-35-3)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-97-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-97-0)

<span id="page-36-0"></span>• [--no-defaults](#page-36-0)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-36-0) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-36-0) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-97-0) utility. See [Section 6.6.7,](#page-97-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-97-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-36-1"></span>• [--password\[=](#page-36-1)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlshow](#page-29-1) prompts for one. If given, there must be no space between [-](#page-36-1) [password=](#page-36-1) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlshow](#page-29-1) should not prompt for one, use the [--skip-password](#page-36-1) option.

<span id="page-36-2"></span>• [--password1\[=](#page-36-2)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlshow](#page-29-1) prompts for one. If given, there must be no space between [--password1=](#page-36-2) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlshow](#page-29-1) should not prompt for one, use the [--skip-password1](#page-36-2) option.

[--password1](#page-36-2) and [--password](#page-36-1) are synonymous, as are [--skip-password1](#page-36-2) and [--skip](#page-36-1)[password](#page-36-1).

<span id="page-36-3"></span>• [--password2\[=](#page-36-3)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-36-2); see the description of that option for details.

## <span id="page-37-0"></span>• [--password3\[=](#page-37-0)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-36-2); see the description of that option for details.

### <span id="page-37-1"></span>• [--pipe](#page-37-1), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

### <span id="page-37-2"></span>• [--plugin-dir=](#page-37-2)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-34-0) option is used to specify an authentication plugin but [mysqlshow](#page-29-1) does not find it. See Section 8.2.17, "Pluggable Authentication".

### <span id="page-37-3"></span>• --port=[port\\_num](#page-37-3), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

## <span id="page-37-4"></span>• [--print-defaults](#page-37-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-37-5"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-37-5)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-38-0"></span>• [--server-public-key-path=](#page-38-0)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-38-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-35-0).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-38-1"></span>• [--shared-memory-base-name=](#page-38-1)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-38-2"></span>• [--show-table-type](#page-38-2), -t

| Command-Line Format | show-table-type |
|---------------------|-----------------|
|---------------------|-----------------|

Show a column indicating the table type, as in SHOW FULL TABLES. The type is BASE TABLE or VIEW.

<span id="page-38-3"></span>• [--socket=](#page-38-3)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use. 609

On Windows, this option applies only if the server was started with the named\_pipe system variable

a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-39-0"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-39-1"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-39-1)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-39-1) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-39-1) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_39_Picture_11.jpeg)

## **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-39-1) is OFF. In this case, setting [--ssl-fips-mode](#page-39-1) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-39-2"></span>• [--status](#page-39-2), -i

| Command-Line Format | status |
|---------------------|--------|
|---------------------|--------|

Display extra information about each table.

<span id="page-39-3"></span>• [--tls-ciphersuites=](#page-39-3)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-40-0"></span>• [--tls-version=](#page-40-0)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-40-1"></span>• --user=[user\\_name](#page-40-1), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

<span id="page-40-2"></span>• [--verbose](#page-40-2), -v

| Command-Line Format | verbose |
|---------------------|---------|
|                     |         |

Verbose mode. Print more information about what the program does. This option can be used multiple times to increase the amount of information.

<span id="page-40-3"></span>• [--version](#page-40-3), -V

| Command-Line Format<br>version |
|--------------------------------|
|--------------------------------|

Display version information and exit.

<span id="page-40-4"></span>• [--zstd-compression-level=](#page-40-4)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

<span id="page-40-5"></span>For more information, see Section 6.2.8, "Connection Compression Control".

[mysqlslap](#page-40-5) is a diagnostic program designed to emulate client load for a MySQL server and to report the timing of each stage. It works as if multiple clients are accessing the server.

Invoke [mysqlslap](#page-40-5) like this:

```
mysqlslap [options]
```

Some options such as [--create](#page-47-0) or [--query](#page-55-0) enable you to specify a string containing an SQL statement or a file containing statements. If you specify a file, by default it must contain one statement per line. (That is, the implicit statement delimiter is the newline character.) Use the [--delimiter](#page-50-0) option to specify a different delimiter, which enables you to specify statements that span multiple lines or place multiple statements on a single line. You cannot include comments in a file; [mysqlslap](#page-40-5) does not understand them.

[mysqlslap](#page-40-5) runs in three stages:

- 1. Create schema, table, and optionally any stored programs or data to use for the test. This stage uses a single client connection.
- 2. Run the load test. This stage can use many client connections.
- 3. Clean up (disconnect, drop table if specified). This stage uses a single client connection.

#### Examples:

Supply your own create and query SQL statements, with 50 clients querying and 200 selects for each (enter the command on a single line):

```
mysqlslap --delimiter=";"
 --create="CREATE TABLE a (b int);INSERT INTO a VALUES (23)"
 --query="SELECT * FROM a" --concurrency=50 --iterations=200
```

Let [mysqlslap](#page-40-5) build the query SQL statement with a table of two INT columns and three VARCHAR columns. Use five clients querying 20 times each. Do not create the table or insert the data (that is, use the previous test's schema and data):

```
mysqlslap --concurrency=5 --iterations=20
 --number-int-cols=2 --number-char-cols=3
 --auto-generate-sql
```

Tell the program to load the create, insert, and query SQL statements from the specified files, where the create.sql file has multiple table creation statements delimited by ';' and multiple insert statements delimited by ';'. The --query file should contain multiple queries delimited by ';'. Run all the load statements, then run all the queries in the query file with five clients (five times each):

```
mysqlslap --concurrency=5
 --iterations=5 --query=query.sql --create=create.sql
 --delimiter=";"
```

[mysqlslap](#page-40-5) supports the following options, which can be specified on the command line or in the [mysqlslap] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.19 mysqlslap Options**

| Option Name                            | Description                                                                                                 | Deprecated |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------|------------|
| auto-generate-sql                      | Generate SQL statements<br>automatically when they are<br>not supplied in files or using<br>command options |            |
| auto-generate-sql-add<br>autoincrement | Add AUTO_INCREMENT<br>column to automatically<br>generated tables                                           |            |

| Option Name                                                    | Description                                                                       | Deprecated |
|----------------------------------------------------------------|-----------------------------------------------------------------------------------|------------|
| auto-generate-sql-execute<br>number                            | Specify how many queries to<br>generate automatically                             |            |
| auto-generate-sql-guid-primary                                 | Add a GUID-based primary key<br>to automatically generated tables                 |            |
| auto-generate-sql-load-type                                    | Specify the test load type                                                        |            |
| auto-generate-sql-secondary<br>indexes                         | Specify how many secondary<br>indexes to add to automatically<br>generated tables |            |
| auto-generate-sql-unique<br>query-number                       | How many different queries to<br>generate for automatic tests                     |            |
| auto-generate-sql-unique-write<br>number                       | How many different queries to<br>generate forauto-generate-sql<br>write-number    |            |
| auto-generate-sql-write-number How many row inserts to perform | on each thread                                                                    |            |
| commit                                                         | How many statements to execute<br>before committing                               |            |
| compress                                                       | Compress all information sent<br>between client and server                        | Yes        |
| compression-algorithms                                         | Permitted compression<br>algorithms for connections to<br>server                  |            |
| concurrency                                                    | Number of clients to simulate<br>when issuing the SELECT<br>statement             |            |
| create                                                         | File or string containing the<br>statement to use for creating the<br>table       |            |
| create-schema                                                  | Schema in which to run the tests                                                  |            |
| csv                                                            | Generate output in comma<br>separated values format                               |            |
| debug                                                          | Write debugging log                                                               |            |
| debug-check                                                    | Print debugging information<br>when program exits                                 |            |
| debug-info                                                     | Print debugging information,<br>memory, and CPU statistics<br>when program exits  |            |
| default-auth                                                   | Authentication plugin to use                                                      |            |
| defaults-extra-file                                            | Read named option file in<br>addition to usual option files                       |            |
| defaults-file                                                  | Read only named option file                                                       |            |
| defaults-group-suffix                                          | Option group suffix value                                                         |            |
| delimiter                                                      | Delimiter to use in SQL<br>statements                                             |            |
| detach                                                         | Detach (close and reopen)<br>each connection after each N<br>statements           |            |

| Option Name             | Description                                                                             | Deprecated |
|-------------------------|-----------------------------------------------------------------------------------------|------------|
| enable-cleartext-plugin | Enable cleartext authentication<br>plugin                                               |            |
| engine                  | Storage engine to use for<br>creating the table                                         |            |
| get-server-public-key   | Request RSA public key from<br>server                                                   |            |
| help                    | Display help message and exit                                                           |            |
| host                    | Host on which MySQL server is<br>located                                                |            |
| iterations              | Number of times to run the tests                                                        |            |
| login-path              | Read login path options<br>from .mylogin.cnf                                            |            |
| no-defaults             | Read no option files                                                                    |            |
| no-drop                 | Do not drop any schema created<br>during the test run                                   |            |
| number-char-cols        | Number of VARCHAR columns<br>to use ifauto-generate-sql is<br>specified                 |            |
| number-int-cols         | Number of INT columns to use if<br>auto-generate-sql is specified                       |            |
| number-of-queries       | Limit each client to approximately<br>this number of queries                            |            |
| only-print              | Do not connect to databases.<br>mysqlslap only prints what it<br>would have done        |            |
| password                | Password to use when<br>connecting to server                                            |            |
| password1               | First multifactor authentication<br>password to use when<br>connecting to server        |            |
| password2               | Second multifactor authentication<br>password to use when<br>connecting to server       |            |
| password3               | Third multifactor authentication<br>password to use when<br>connecting to server        |            |
| pipe                    | Connect to server using named<br>pipe (Windows only)                                    |            |
| plugin-dir              | Directory where plugins are<br>installed                                                |            |
| port                    | TCP/IP port number for<br>connection                                                    |            |
| post-query              | File or string containing the<br>statement to execute after the<br>tests have completed |            |
| post-system             | String to execute using system()<br>after the tests have completed                      |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| pre-query                                    | File or string containing the<br>statement to execute before<br>running the tests |            |
| pre-system                                   | String to execute using system()<br>before running the tests                      |            |
| print-defaults                               | Print default options                                                             |            |
| protocol                                     | Transport protocol to use                                                         |            |
| query                                        | File or string containing the<br>SELECT statement to use for<br>retrieving data   |            |
| server-public-key-path                       | Path name to file containing RSA<br>public key                                    |            |
| shared-memory-base-name                      | Shared-memory name for<br>shared-memory connections<br>(Windows only)             |            |
| silent                                       | Silent mode                                                                       |            |
| socket                                       | Unix socket file or Windows<br>named pipe to use                                  |            |
| sql-mode                                     | Set SQL mode for client session                                                   |            |
| ssl-ca                                       | File that contains list of trusted<br>SSL Certificate Authorities                 |            |
| ssl-capath                                   | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files |            |
| ssl-cert                                     | File that contains X.509<br>certificate                                           |            |
| ssl-cipher                                   | Permissible ciphers for<br>connection encryption                                  |            |
| ssl-crl                                      | File that contains certificate<br>revocation lists                                |            |
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                      |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                     | Yes        |
| ssl-key                                      | File that contains X.509 key                                                      |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                 |            |
| ssl-session-data                             | File that contains SSL session<br>data                                            |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                        |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                     |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                            |            |
| user                                         | MySQL user name to use when<br>connecting to server                               |            |

| Option Name            | Description                                                                 | Deprecated |
|------------------------|-----------------------------------------------------------------------------|------------|
| verbose                | Verbose mode                                                                |            |
| version                | Display version information and<br>exit                                     |            |
| zstd-compression-level | Compression level for<br>connections to server that use<br>zstd compression |            |

## <span id="page-45-5"></span>• [--help](#page-45-5), -?

| Command-Line Format | help |
|---------------------|------|

#### Display a help message and exit.

<span id="page-45-0"></span>• [--auto-generate-sql](#page-45-0), -a

| Command-Line Format | auto-generate-sql |
|---------------------|-------------------|
| Type                | Boolean           |
| Default Value       | FALSE             |

## Generate SQL statements automatically when they are not supplied in files or using command options.

<span id="page-45-1"></span>• [--auto-generate-sql-add-autoincrement](#page-45-1)

| Command-Line Format | auto-generate-sql-add<br>autoincrement |
|---------------------|----------------------------------------|
| Type                | Boolean                                |
| Default Value       | FALSE                                  |

### Add an AUTO\_INCREMENT column to automatically generated tables.

<span id="page-45-2"></span>• [--auto-generate-sql-execute-number=](#page-45-2)N

| Command-Line Format | auto-generate-sql-execute-number=# |
|---------------------|------------------------------------|
| Type                | Numeric                            |

## Specify how many queries to generate automatically.

<span id="page-45-3"></span>• [--auto-generate-sql-guid-primary](#page-45-3)

| Command-Line Format | auto-generate-sql-guid-primary |
|---------------------|--------------------------------|
| Type                | Boolean                        |
| Default Value       | FALSE                          |

#### Add a GUID-based primary key to automatically generated tables.

<span id="page-45-4"></span>• [--auto-generate-sql-load-type=](#page-45-4)type

| Command-Line Format | auto-generate-sql-load-type=type |
|---------------------|----------------------------------|
| Type                | Enumeration                      |

#### mysqlslap — A Load Emulation Client

| Default Value | mixed  |
|---------------|--------|
| Valid Values  | read   |
|               | write  |
|               | key    |
|               | update |
|               | mixed  |

Specify the test load type. The permissible values are read (scan tables), write (insert into tables), key (read primary keys), update (update primary keys), or mixed (half inserts, half scanning selects). The default is mixed.

<span id="page-46-0"></span>• [--auto-generate-sql-secondary-indexes=](#page-46-0)N

| Command-Line Format | auto-generate-sql-secondary<br>indexes=# |
|---------------------|------------------------------------------|
| Type                | Numeric                                  |
| Default Value       | 0                                        |

Specify how many secondary indexes to add to automatically generated tables. By default, none are added.

<span id="page-46-1"></span>• [--auto-generate-sql-unique-query-number=](#page-46-1)N

| Command-Line Format | auto-generate-sql-unique-query<br>number=# |
|---------------------|--------------------------------------------|
| Type                | Numeric                                    |
| Default Value       | 10                                         |

How many different queries to generate for automatic tests. For example, if you run a key test that performs 1000 selects, you can use this option with a value of 1000 to run 1000 unique queries, or with a value of 50 to perform 50 different selects. The default is 10.

<span id="page-46-2"></span>• [--auto-generate-sql-unique-write-number=](#page-46-2)N

| Command-Line Format | auto-generate-sql-unique-write<br>number=# |
|---------------------|--------------------------------------------|
| Type                | Numeric                                    |
| Default Value       | 10                                         |

How many different queries to generate for [--auto-generate-sql-write-number](#page-46-3). The default is 10.

<span id="page-46-3"></span>• [--auto-generate-sql-write-number=](#page-46-3)N

| Command-Line Format | 617<br>auto-generate-sql-write-number=# |
|---------------------|-----------------------------------------|
| Type                | Numeric                                 |

| Default Value | 100 |
|---------------|-----|
|---------------|-----|

How many row inserts to perform. The default is 100.

<span id="page-47-1"></span>• [--commit=](#page-47-1)N

| Command-Line Format | commit=# |
|---------------------|----------|
| Type                | Numeric  |
| Default Value       | 0        |

How many statements to execute before committing. The default is 0 (no commits are done).

<span id="page-47-2"></span>• [--compress](#page-47-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-47-3"></span>• [--compression-algorithms=](#page-47-3)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

This option was added in MySQL 8.0.18.

<span id="page-47-4"></span>• [--concurrency=](#page-47-4)N, -c N

| Command-Line Format | concurrency=# |
|---------------------|---------------|
| Type                | Numeric       |

The number of parallel clients to simulate.

<span id="page-47-0"></span>• [--create=](#page-47-0)value

| Command-Line Format | create=value |
|---------------------|--------------|
| Type                | String       |

The file or string containing the statement to use for creating the table.

<span id="page-48-0"></span>• [--create-schema=](#page-48-0)value

| Command-Line Format | create-schema=value |
|---------------------|---------------------|
| Type                | String              |

The schema in which to run the tests.

![](_page_48_Picture_6.jpeg)

#### **Note**

If the [--auto-generate-sql](#page-45-0) option is also given, [mysqlslap](#page-40-5) drops the schema at the end of the test run. To avoid this, use the [--no-drop](#page-51-4) option as well.

<span id="page-48-1"></span>• --csv[=[file\\_name](#page-48-1)]

| Command-Line Format | csv=[file] |
|---------------------|------------|
| Type                | File name  |

Generate output in comma-separated values format. The output goes to the named file, or to the standard output if no file is given.

<span id="page-48-2"></span>• --debug[=[debug\\_options](#page-48-2)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]      |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | d:t:o,/tmp/mysqlslap.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysqlslap.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-48-3"></span>• [--debug-check](#page-48-3)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-48-4"></span>• [--debug-info](#page-48-4), -T

| Command-Line Format | debug-info |
|---------------------|------------|

| Type          | Boolean |
|---------------|---------|
| Default Value | FALSE   |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-49-0"></span>• [--default-auth=](#page-49-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-49-1"></span>• [--defaults-extra-file=](#page-49-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-49-2"></span>• [--defaults-file=](#page-49-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-49-3"></span>• [--defaults-group-suffix=](#page-49-3)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlslap](#page-40-5) normally reads the [client] and [mysqlslap] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-49-3), [mysqlslap](#page-40-5) also reads the [client\_other] and [mysqlslap\_other] groups.

## <span id="page-50-0"></span>• [--delimiter=](#page-50-0)str, -F str

| Command-Line Format | delimiter=str |
|---------------------|---------------|
| Type                | String        |

The delimiter to use in SQL statements supplied in files or using command options.

### <span id="page-50-1"></span>• [--detach=](#page-50-1)N

| Command-Line Format | detach=# |
|---------------------|----------|
| Type                | Numeric  |
| Default Value       | 0        |

Detach (close and reopen) each connection after each N statements. The default is 0 (connections are not detached).

### <span id="page-50-2"></span>• [--enable-cleartext-plugin](#page-50-2)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-50-3"></span>• --engine=[engine\\_name](#page-50-3), -e engine\_name

| Command-Line Format | engine=engine_name |
|---------------------|--------------------|
| Type                | String             |

The storage engine to use for creating tables.

<span id="page-50-4"></span>• [--get-server-public-key](#page-50-4)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the RSA public key that it uses for key pair-based password exchange. This option applies to clients that connect to the server using an account that authenticates with the caching\_sha2\_password authentication plugin. For connections by such accounts, the server does not send the public key to the client unless requested. The option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not needed, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-55-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-50-4). 621 <span id="page-51-0"></span>• --host=[host\\_name](#page-51-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-51-1"></span>• [--iterations=](#page-51-1)N, -i N

| Command-Line Format | iterations=# |
|---------------------|--------------|
| Type                | Numeric      |

The number of times to run the tests.

<span id="page-51-2"></span>• [--login-path=](#page-51-2)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-97-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-97-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-51-4"></span>• [--no-drop](#page-51-4)

| Command-Line Format | no-drop |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

Prevent [mysqlslap](#page-40-5) from dropping any schema it creates during the test run.

<span id="page-51-3"></span>• [--no-defaults](#page-51-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-51-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-51-3) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-97-0) utility. See [Section 6.6.7,](#page-97-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-97-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-

<span id="page-52-0"></span>• [--number-char-cols=](#page-52-0)N, -x N

| Command-Line Format | number-char-cols=# |
|---------------------|--------------------|
| Type                | Numeric            |

The number of VARCHAR columns to use if [--auto-generate-sql](#page-45-0) is specified.

<span id="page-52-1"></span>• [--number-int-cols=](#page-52-1)N, -y N

| Command-Line Format | number-int-cols=# |
|---------------------|-------------------|
| Type                | Numeric           |

The number of INT columns to use if [--auto-generate-sql](#page-45-0) is specified.

<span id="page-52-2"></span>• [--number-of-queries=](#page-52-2)N

| Command-Line Format | number-of-queries=# |
|---------------------|---------------------|
| Type                | Numeric             |

Limit each client to approximately this many queries. Query counting takes into account the statement delimiter. For example, if you invoke [mysqlslap](#page-40-5) as follows, the ; delimiter is recognized so that each instance of the query string counts as two queries. As a result, 5 rows (not 10) are inserted.

```
mysqlslap --delimiter=";" --number-of-queries=10
 --query="use test;insert into t values(null)"
```

<span id="page-52-3"></span>• [--only-print](#page-52-3)

| Command-Line Format | only-print |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Do not connect to databases. [mysqlslap](#page-40-5) only prints what it would have done.

<span id="page-52-4"></span>• [--password\[=](#page-52-4)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlslap](#page-40-5) prompts for one. If given, there must be no space between [-](#page-52-4) [password=](#page-52-4) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security". 623

To explicitly specify that there is no password and that [mysqlslap](#page-40-5) should not prompt for one, use

## <span id="page-53-0"></span>• [--password1\[=](#page-53-0)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlslap](#page-40-5) prompts for one. If given, there must be no space between [--password1=](#page-53-0) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlslap](#page-40-5) should not prompt for one, use the [--skip-password1](#page-53-0) option.

[--password1](#page-53-0) and [--password](#page-52-4) are synonymous, as are [--skip-password1](#page-53-0) and [--skip](#page-52-4)[password](#page-52-4).

<span id="page-53-1"></span>• [--password2\[=](#page-53-1)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-53-0); see the description of that option for details.

<span id="page-53-2"></span>• [--password3\[=](#page-53-2)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-53-0); see the description of that option for details.

<span id="page-53-3"></span>• [--pipe](#page-53-3), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-53-4"></span>• [--plugin-dir=](#page-53-4)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-49-0) option is used to specify an authentication plugin but [mysqlslap](#page-40-5) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-53-5"></span>• --port=[port\\_num](#page-53-5), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-53-6"></span>• [--post-query=](#page-53-6)value

| Command-Line Format | post-query=value |
|---------------------|------------------|
| Type                | String           |

The file or string containing the statement to execute after the tests have completed. This execution is not counted for timing purposes.

### <span id="page-54-0"></span>• [--post-system=](#page-54-0)str

| Command-Line Format | post-system=str |
|---------------------|-----------------|
| Type                | String          |

The string to execute using system() after the tests have completed. This execution is not counted for timing purposes.

### <span id="page-54-1"></span>• [--pre-query=](#page-54-1)value

| Command-Line Format | pre-query=value |
|---------------------|-----------------|
| Type                | String          |

The file or string containing the statement to execute before running the tests. This execution is not counted for timing purposes.

### <span id="page-54-2"></span>• [--pre-system=](#page-54-2)str

| Command-Line Format | pre-system=str |
|---------------------|----------------|
| Type                | String         |

The string to execute using system() before running the tests. This execution is not counted for timing purposes.

## <span id="page-54-3"></span>• [--print-defaults](#page-54-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

### <span id="page-54-4"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-54-4)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-55-0"></span>• [--query=](#page-55-0)value, -q value

| Command-Line Format | query=value |
|---------------------|-------------|
| Type                | String      |

The file or string containing the SELECT statement to use for retrieving data.

<span id="page-55-1"></span>• [--server-public-key-path=](#page-55-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-55-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-50-4).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-55-2"></span>• [--shared-memory-base-name=](#page-55-2)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-55-3"></span>• [--silent](#page-55-3), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Silent mode. No output.

<span id="page-55-4"></span>• [--socket=](#page-55-4)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-56-0"></span>• [--sql-mode=](#page-56-0)mode

| Command-Line Format | sql-mode=mode |
|---------------------|---------------|
| Type                | String        |

Set the SQL mode for the client session.

<span id="page-56-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-56-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-56-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-56-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-56-2) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_56_Picture_15.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-56-2) is OFF. In this case, setting [--ssl-fips-mode](#page-56-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-56-3"></span>• [--tls-ciphersuites=](#page-56-3)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
|                     |                                   |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-57-0"></span>• [--tls-version=](#page-57-0)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-57-1"></span>• --user=[user\\_name](#page-57-1), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

<span id="page-57-2"></span>• [--verbose](#page-57-2), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print more information about what the program does. This option can be used multiple times to increase the amount of information.

<span id="page-57-3"></span>• [--version](#page-57-3), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-57-4"></span>• [--zstd-compression-level=](#page-57-4)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

This option was added in MySQL 8.0.18.