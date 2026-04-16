---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section provides information about techniques for more effective use of mysql and about mysql operational behavior.

- [Input-Line Editing](#page-24-1)
- [Disabling Interactive History](#page-24-0)
- [Unicode Support on Windows](#page-25-0)
- [Displaying Query Results Vertically](#page-25-1)
- [Using Safe-Updates Mode \(--safe-updates\)](#page-26-0)
- [Disabling mysql Auto-Reconnect](#page-27-0)
- [mysql Client Parser Versus Server Parser](#page-27-1)

## <span id="page-24-1"></span>**Input-Line Editing**

mysql supports input-line editing, which enables you to modify the current input line in place or recall previous input lines. For example, the **left-arrow** and **right-arrow** keys move horizontally within the current input line, and the **up-arrow** and **down-arrow** keys move up and down through the set of previously entered lines. **Backspace** deletes the character before the cursor and typing new characters enters them at the cursor position. To enter the line, press **Enter**.

On Windows, the editing key sequences are the same as supported for command editing in console windows. On Unix, the key sequences depend on the input library used to build mysql (for example, the libedit or readline library).

Documentation for the libedit and readline libraries is available online. To change the set of key sequences permitted by a given input library, define key bindings in the library startup file. This is a file in your home directory: .editrc for libedit and .inputrc for readline.

For example, in libedit, **Control+W** deletes everything before the current cursor position and **Control+U** deletes the entire line. In readline, **Control+W** deletes the word before the cursor and **Control+U** deletes everything before the current cursor position. If mysql was built using libedit, a user who prefers the readline behavior for these two keys can put the following lines in the .editrc file (creating the file if necessary):

```
bind "^W" ed-delete-prev-word
bind "^U" vi-kill-line-prev
```

To see the current set of key bindings, temporarily put a line that says only bind at the end of .editrc. mysql shows the bindings when it starts.

## <span id="page-24-0"></span>**Disabling Interactive History**

The **up-arrow** key enables you to recall input lines from current and previous sessions. In cases where a console is shared, this behavior may be unsuitable. mysql supports disabling the interactive history partially or fully, depending on the host platform.

On Windows, the history is stored in memory. **Alt+F7** deletes all input lines stored in memory for the current history buffer. It also deletes the list of sequential numbers in front of the input lines displayed with **F7** and recalled (by number) with **F9**. New input lines entered after you press **Alt+F7** repopulate the current history buffer. Clearing the buffer does not prevent logging to the Windows Event Viewer, if the [--syslog](#page-10-1) option was used to start mysql. Closing the console window also clears the current history buffer.

To disable interactive history on Unix, first delete the .mysql\_history file, if it exists (previous entries are recalled otherwise). Then start mysql with the --histignore="\*" option to ignore all new input lines. To re-enable the recall (and logging) behavior, restart mysql without the option.

If you prevent the .mysql\_history file from being created (see [Controlling the History File](#page-21-0)) and use --histignore="\*" to start the mysql client, the interactive history recall facility is disabled fully. Alternatively, if you omit the --histignore option, you can recall the input lines entered during the current session.

# <span id="page-25-0"></span>**Unicode Support on Windows**

Windows provides APIs based on UTF-16LE for reading from and writing to the console; the mysql client for Windows is able to use these APIs. The Windows installer creates an item in the MySQL menu named MySQL command line client - Unicode. This item invokes the mysql client with properties set to communicate through the console to the MySQL server using Unicode.

To take advantage of this support manually, run mysql within a console that uses a compatible Unicode font and set the default character set to a Unicode character set that is supported for communication with the server:

- 1. Open a console window.
- 2. Go to the console window properties, select the font tab, and choose Lucida Console or some other compatible Unicode font. This is necessary because console windows start by default using a DOS raster font that is inadequate for Unicode.
- 3. Execute mysql.exe with the --default-character-set=utf8mb4 (or utf8mb3) option. This option is necessary because utf16le is one of the character sets that cannot be used as the client character set. See Impermissible Client Character Sets.

With those changes, mysql uses the Windows APIs to communicate with the console using UTF-16LE, and communicate with the server using UTF-8. (The menu item mentioned previously sets the font and character set as just described.)

To avoid those steps each time you run mysql, you can create a shortcut that invokes mysql.exe. The shortcut should set the console font to Lucida Console or some other compatible Unicode font, and pass the --default-character-set=utf8mb4 (or utf8mb3) option to mysql.exe.

Alternatively, create a shortcut that only sets the console font, and set the character set in the [mysql] group of your my.ini file:

```
[mysql]
default-character-set=utf8mb4 # or utf8mb3
```

## <span id="page-25-1"></span>**Displaying Query Results Vertically**

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
```

```
Yes, please do that.
Regards,
Jones
 file: inbox-jani-1
 hash: 190402944
1 row in set (0.09 sec)
```

## <span id="page-26-0"></span>**Using Safe-Updates Mode (--safe-updates)**

For beginners, a useful startup option is [--safe-updates](#page-6-0) (or [--i-am-a-dummy](#page-6-0), which has the same effect). Safe-updates mode is helpful for cases when you might have issued an UPDATE or DELETE statement but forgotten the WHERE clause indicating which rows to modify. Normally, such statements update or delete all rows in the table. With [--safe-updates](#page-6-0), you can modify rows only by specifying the key values that identify them, or a LIMIT clause, or both. This helps prevent accidents. Safe-updates mode also restricts SELECT statements that produce (or are estimated to produce) very large result sets.

The [--safe-updates](#page-6-0) option causes mysql to execute the following statement when it connects to the MySQL server, to set the session values of the sql\_safe\_updates, sql\_select\_limit, and max\_join\_size system variables:

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

To specify result set limits different from 1,000 and 1,000,000, you can override the defaults by using the [--select-limit](#page-7-0) and --max-join-size options when you invoke mysql:

```
mysql --safe-updates --select-limit=500 --max-join-size=10000
```

It is possible for UPDATE and DELETE statements to produce an error in safe-updates mode even with a key specified in the WHERE clause, if the optimizer decides not to use the index on the key column:

- Range access on the index cannot be used if memory usage exceeds that permitted by the range\_optimizer\_max\_mem\_size system variable. The optimizer then falls back to a table scan. See Limiting Memory Use for Range Optimization.
- If key comparisons require type conversion, the index may not be used (see Section 10.3.1, "How MySQL Uses Indexes"). Suppose that an indexed string column c1 is compared to a numeric value using WHERE c1 = 2222. For such comparisons, the string value is converted to a number and the operands are compared numerically (see Section 14.3, "Type Conversion in Expression Evaluation"), preventing use of the index. If safe-updates mode is enabled, an error occurs.

These behaviors are included in safe-updates mode:

• EXPLAIN with UPDATE and DELETE statements does not produce safe-updates errors. This enables use of EXPLAIN plus SHOW WARNINGS to see why an index is not used, which can be helpful in cases such as when a range\_optimizer\_max\_mem\_size violation or type conversion occurs and the optimizer does not use an index even though a key column was specified in the WHERE clause.

- When a safe-updates error occurs, the error message includes the first diagnostic that was produced, to provide information about the reason for failure. For example, the message may indicate that the range\_optimizer\_max\_mem\_size value was exceeded or type conversion occurred, either of which can preclude use of an index.
- For multiple-table deletes and updates, an error is produced with safe updates enabled only if any target table uses a table scan.

# <span id="page-27-0"></span>**Disabling mysql Auto-Reconnect**

If the mysql client loses its connection to the server while sending a statement, it immediately and automatically tries to reconnect once to the server and send the statement again. However, even if mysql succeeds in reconnecting, your first connection has ended and all your previous session objects and settings are lost: temporary tables, the autocommit mode, and user-defined and session variables. Also, any current transaction rolls back. This behavior may be dangerous for you, as in the following example where the server was shut down and restarted between the first and second statements without you knowing it:

```
mysql> SET @a=1;
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

The @a user variable has been lost with the connection, and after the reconnection it is undefined. If it is important to have mysql terminate with an error if the connection has been lost, you can start the mysql client with the [--skip-reconnect](#page-5-1) option.

For more information about auto-reconnect and its effect on state information when a reconnection occurs, see [Automatic Reconnection Control](https://dev.mysql.com/doc/c-api/8.4/en/c-api-auto-reconnect.md).

## <span id="page-27-1"></span>**mysql Client Parser Versus Server Parser**

The mysql client uses a parser on the client side that is not a duplicate of the complete parser used by the mysqld server on the server side. This can lead to differences in treatment of certain constructs. Examples:

• The server parser treats strings delimited by " characters as identifiers rather than as plain strings if the ANSI\_QUOTES SQL mode is enabled.

The mysql client parser does not take the ANSI\_QUOTES SQL mode into account. It treats strings delimited by ", ', and ` characters the same, regardless of whether ANSI\_QUOTES is enabled.

• Within /\*! ... \*/ and /\*+ ... \*/ comments, the mysql client parser interprets short-form mysql commands. The server parser does not interpret them because these commands have no meaning on the server side.

If it is desirable for mysql not to interpret short-form commands within comments, a partial workaround is to use the --binary-mode option, which causes all mysql commands to be disabled except \C and \d in noninteractive mode (for input piped to mysql or loaded using the source command).

# <span id="page-28-0"></span>**6.5.2 mysqladmin — A MySQL Server Administration Program**

[mysqladmin](#page-28-0) is a client for performing administrative operations. You can use it to check the server's configuration and current status, to create and drop databases, and more.

Invoke [mysqladmin](#page-28-0) like this:

```
mysqladmin [options] command [command-arg] [command [command-arg]] ...
```

[mysqladmin](#page-28-0) supports the following commands. Some of the commands take an argument following the command name.

• create db\_name

Create a new database named db\_name.

• debug

Tells the server to write debug information to the error log. The connected user must have the SUPER privilege. Format and content of this information is subject to change.

This includes information about the Event Scheduler. See Section 27.4.5, "Event Scheduler Status".

• drop db\_name

Delete the database named db\_name and all its tables.

• extended-status

Display the server status variables and their values.

• flush-hosts

Flush all information in the host cache. See Section 7.1.12.3, "DNS Lookups and the Host Cache".

• flush-logs [log\_type ...]

Flush all logs.

The [mysqladmin flush-logs](#page-28-0) command permits optional log types to be given, to specify which logs to flush. Following the flush-logs command, you can provide a space-separated list of one or more of the following log types: binary, engine, error, general, relay, slow. These correspond to the log types that can be specified for the FLUSH LOGS SQL statement.

• flush-privileges

Reload the grant tables (same as reload).

• flush-status

Clear status variables.

• flush-tables

Flush all tables.

• kill id,id,...

Kill server threads. If multiple thread ID values are given, there must be no spaces in the list.

To kill threads belonging to other users, the connected user must have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

• password new\_password

Set a new password. This changes the password to new\_password for the account that you use with [mysqladmin](#page-28-0) for connecting to the server. Thus, the next time you invoke [mysqladmin](#page-28-0) (or any other client program) using the same account, you must specify the new password.

![](_page_29_Picture_2.jpeg)

#### **Warning**

Setting a password using [mysqladmin](#page-28-0) should be considered insecure. On some systems, your password becomes visible to system status programs such as ps that may be invoked by other users to display command lines. MySQL clients typically overwrite the command-line password argument with zeros during their initialization sequence. However, there is still a brief interval during which the value is visible. Also, on some systems this overwriting strategy is ineffective and the password remains visible to ps. (SystemV Unix systems and perhaps others are subject to this problem.)

If the new\_password value contains spaces or other characters that are special to your command interpreter, you need to enclose it within quotation marks. On Windows, be sure to use double quotation marks rather than single quotation marks; single quotation marks are not stripped from the password, but rather are interpreted as part of the password. For example:

mysqladmin password "my new password"

The new password can be omitted following the password command. In this case, [mysqladmin](#page-28-0) prompts for the password value, which enables you to avoid specifying the password on the command line. Omitting the password value should be done only if password is the final command on the [mysqladmin](#page-28-0) command line. Otherwise, the next argument is taken as the password.

![](_page_29_Picture_8.jpeg)

#### **Caution**

Do not use this command used if the server was started with the --skipgrant-tables option. No password change is applied. This is true even if you precede the password command with flush-privileges on the same command line to re-enable the grant tables because the flush operation occurs after you connect. However, you can use [mysqladmin](#page-28-0) [flush-privileges](#page-28-0) to re-enable the grant tables and then use a separate [mysqladmin password](#page-28-0) command to change the password.

• ping

Check whether the server is available. The return status from [mysqladmin](#page-28-0) is 0 if the server is running, 1 if it is not. This is 0 even in case of an error such as Access denied, because this means that the server is running but refused the connection, which is different from the server not running.

• processlist

Show a list of active server threads. This is like the output of the SHOW PROCESSLIST statement. If the [--verbose](#page-42-0) option is given, the output is like that of SHOW FULL PROCESSLIST. (See Section 15.7.7.31, "SHOW PROCESSLIST Statement".)

• reload

Reload the grant tables.

• refresh

Flush all tables and close and open log files.

• shutdown

Stop the server.

• start-replica

Start replication on a replica server.

• start-slave

This is a deprecated alias for start-replica.

• status

Display a short server status message.

• stop-replica

Stop replication on a replica server.

• stop-slave

This is a deprecated alias for stop-replica.

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

The [mysqladmin status](#page-28-0) command result displays the following values:

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

## • Open tables

The number of tables that currently are open.

If you execute [mysqladmin shutdown](#page-28-0) when connecting to a local server using a Unix socket file, [mysqladmin](#page-28-0) waits until the server's process ID file has been removed, to ensure that the server has stopped properly.

[mysqladmin](#page-28-0) supports the following options, which can be specified on the command line or in the [mysqladmin] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.11 mysqladmin Options**

| Option Name             | Description                                                                    |
|-------------------------|--------------------------------------------------------------------------------|
| bind-address            | Use specified network interface to connect to<br>MySQL Server                  |
| character-sets-dir      | Directory where character sets can be found                                    |
| compress                | Compress all information sent between client and<br>server                     |
| compression-algorithms  | Permitted compression algorithms for connections<br>to server                  |
| connect-timeout         | Number of seconds before connection timeout                                    |
| count                   | Number of iterations to make for repeated<br>command execution                 |
| debug                   | Write debugging log                                                            |
| debug-check             | Print debugging information when program exits                                 |
| debug-info              | Print debugging information, memory, and CPU<br>statistics when program exits  |
| default-auth            | Authentication plugin to use                                                   |
| default-character-set   | Specify default character set                                                  |
| defaults-extra-file     | Read named option file in addition to usual option<br>files                    |
| defaults-file           | Read only named option file                                                    |
| defaults-group-suffix   | Option group suffix value                                                      |
| enable-cleartext-plugin | Enable cleartext authentication plugin                                         |
| force                   | Continue even if an SQL error occurs                                           |
| get-server-public-key   | Request RSA public key from server                                             |
| help                    | Display help message and exit                                                  |
| host                    | Host on which MySQL server is located                                          |
| login-path              | Read login path options from .mylogin.cnf                                      |
| no-beep                 | Do not beep when errors occur                                                  |
| no-defaults             | Read no option files                                                           |
| no-login-paths          | Do not read login paths from the login path file                               |
| password                | Password to use when connecting to server                                      |
| password1               | First multifactor authentication password to use<br>when connecting to server  |
| password2               | Second multifactor authentication password to use<br>when connecting to server |

| Option Name                               | Description                                                                                   |
|-------------------------------------------|-----------------------------------------------------------------------------------------------|
| password3                                 | Third multifactor authentication password to use<br>when connecting to server                 |
| pipe                                      | Connect to server using named pipe (Windows<br>only)                                          |
| plugin-dir                                | Directory where plugins are installed                                                         |
| port                                      | TCP/IP port number for connection                                                             |
| print-defaults                            | Print default options                                                                         |
| protocol                                  | Transport protocol to use                                                                     |
| relative                                  | Show the difference between the current and<br>previous values when used with thesleep option |
| server-public-key-path                    | Path name to file containing RSA public key                                                   |
| shared-memory-base-name                   | Shared-memory name for shared-memory<br>connections (Windows only)                            |
| show-warnings                             | Show warnings after statement execution                                                       |
| shutdown-timeout                          | The maximum number of seconds to wait for<br>server shutdown                                  |
| silent                                    | Silent mode                                                                                   |
| sleep                                     | Execute commands repeatedly, sleeping for delay<br>seconds in between                         |
| socket                                    | Unix socket file or Windows named pipe to use                                                 |
| ssl-ca                                    | File that contains list of trusted SSL Certificate<br>Authorities                             |
| ssl-capath                                | Directory that contains trusted SSL Certificate<br>Authority certificate files                |
| ssl-cert                                  | File that contains X.509 certificate                                                          |
| ssl-cipher                                | Permissible ciphers for connection encryption                                                 |
| ssl-crl                                   | File that contains certificate revocation lists                                               |
| ssl-crlpath                               | Directory that contains certificate revocation-list<br>files                                  |
| ssl-fips-mode                             | Whether to enable FIPS mode on client side                                                    |
| ssl-key                                   | File that contains X.509 key                                                                  |
| ssl-mode                                  | Desired security state of connection to server                                                |
| ssl-session-data                          | File that contains SSL session data                                                           |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails                                    |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections                                 |
| tls-sni-servername                        | Server name supplied by the client                                                            |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                                        |
| user                                      | MySQL user name to use when connecting to<br>server                                           |
| verbose                                   | Verbose mode                                                                                  |
| version                                   | Display version information and exit                                                          |

| Option Name            | Description                                                                    |
|------------------------|--------------------------------------------------------------------------------|
| vertical               | Print query output rows vertically (one line per<br>column value)              |
| wait                   | If the connection cannot be established, wait and<br>retry instead of aborting |
| zstd-compression-level | Compression level for connections to server that<br>use zstd compression       |

## <span id="page-33-4"></span>• [--help](#page-33-4), -?

| Command-Line Format | help |
|---------------------|------|

## Display a help message and exit.

<span id="page-33-0"></span>• [--bind-address=](#page-33-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-33-1"></span>• [--character-sets-dir=](#page-33-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-33-2"></span>• [--compress](#page-33-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-33-3"></span>• [--compression-algorithms=](#page-33-3)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-34-0"></span>• [--connect-timeout=](#page-34-0)value

| Command-Line Format | connect-timeout=value |
|---------------------|-----------------------|
| Type                | Numeric               |
| Default Value       | 43200                 |

The maximum number of seconds before connection timeout. The default value is 43200 (12 hours).

<span id="page-34-1"></span>• [--count=](#page-34-1)N, -c N

| Command-Line Format | count=# |
|---------------------|---------|
|---------------------|---------|

The number of iterations to make for repeated command execution if the [--sleep](#page-40-4) option is given.

<span id="page-34-2"></span>• --debug[=[debug\\_options](#page-34-2)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]       |
|---------------------|-----------------------------|
| Type                | String                      |
| Default Value       | d:t:o,/tmp/mysqladmin.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysqladmin.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-34-3"></span>• [--debug-check](#page-34-3)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-34-4"></span>• [--debug-info](#page-34-4)

| Command-Line Format | debug-info |     |
|---------------------|------------|-----|
| Type                | Boolean    | 405 |

| Default Value | FALSE |
|---------------|-------|
|---------------|-------|

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-35-0"></span>• [--default-auth=](#page-35-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-35-1"></span>• [--default-character-set=](#page-35-1)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

<span id="page-35-2"></span>• [--defaults-extra-file=](#page-35-2)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-35-3"></span>• [--defaults-file=](#page-35-3)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-35-4"></span>406

• [--defaults-group-suffix=](#page-35-4)str

| Command-Line Format<br>defaults-group-suffix=str |
|--------------------------------------------------|
|--------------------------------------------------|

| Type | String |
|------|--------|
|------|--------|

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqladmin](#page-28-0) normally reads the [client] and [mysqladmin] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-35-4), [mysqladmin](#page-28-0) also reads the [client\_other] and [mysqladmin\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-36-0"></span>• [--enable-cleartext-plugin](#page-36-0)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-36-1"></span>• [--force](#page-36-1), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Do not ask for confirmation for the drop db\_name command. With multiple commands, continue even if an error occurs.

<span id="page-36-2"></span>• [--get-server-public-key](#page-36-2)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-39-4)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-36-2).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-36-3"></span>• --host=[host\\_name](#page-36-3), -h host\_name

| Command-Line Format | host=host_name   |
|---------------------|------------------|
| Type                | String           |
| Default Value       | 407<br>localhost |

## <span id="page-37-0"></span>• [--login-path=](#page-37-0)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-37-3"></span>• [--no-login-paths](#page-37-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|                     |                |

Skips reading options from the login path file.

See [--login-path](#page-37-0) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-37-1"></span>• [--no-beep](#page-37-1), -b

| Command-Line Format | no-beep |
|---------------------|---------|
|---------------------|---------|

Suppress the warning beep that is emitted by default for errors such as a failure to connect to the server.

## <span id="page-37-2"></span>• [--no-defaults](#page-37-2)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-37-2) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-37-2) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-37-4"></span>• [--password\[=](#page-37-4)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqladmin](#page-28-0) prompts for one. If given, there must be no space between [-](#page-37-4) [password=](#page-37-4) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqladmin](#page-28-0) should not prompt for one, use the [--skip-password](#page-37-4) option.

<span id="page-38-0"></span>• [--password1\[=](#page-38-0)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, mysql prompts for one. If given, there must be no space between [--password1=](#page-38-0) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqladmin](#page-28-0) should not prompt for one, use the [--skip-password1](#page-38-0) option.

[--password1](#page-38-0) and [--password](#page-37-4) are synonymous, as are [--skip-password1](#page-2-0) and [--skip](#page-1-2)[password](#page-1-2).

<span id="page-38-1"></span>• [--password2\[=](#page-38-1)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-38-0); see the description of that option for details.

<span id="page-38-2"></span>• [--password3\[=](#page-38-2)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-38-0); see the description of that option for details.

<span id="page-38-3"></span>• [--pipe](#page-38-3), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-38-4"></span>• [--plugin-dir=](#page-38-4)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-35-0) option is used to specify an authentication plugin but [mysqladmin](#page-28-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-39-0"></span>• --port=[port\\_num](#page-39-0), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-39-1"></span>• [--print-defaults](#page-39-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-39-2"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-39-2)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-39-3"></span>• [--relative](#page-39-3), -r

| Command-Line Format | relative |
|---------------------|----------|
|---------------------|----------|

Show the difference between the current and previous values when used with the [--sleep](#page-40-4) option. This option works only with the extended-status command.

<span id="page-39-4"></span>• [--server-public-key-path=](#page-39-4)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-39-4)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-36-2).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-40-0"></span>• [--shared-memory-base-name=](#page-40-0)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-40-1"></span>• [--show-warnings](#page-40-1)

| Command-Line Format | show-warnings |
|---------------------|---------------|
|---------------------|---------------|

Show warnings resulting from execution of statements sent to the server.

<span id="page-40-2"></span>• [--shutdown-timeout=](#page-40-2)value

| Command-Line Format | shutdown-timeout=seconds |
|---------------------|--------------------------|
| Type                | Numeric                  |
| Default Value       | 3600                     |

The maximum number of seconds to wait for server shutdown. The default value is 3600 (1 hour).

<span id="page-40-3"></span>• [--silent](#page-40-3), -s

| Command-Line Format | silent |
|---------------------|--------|

Exit silently if a connection to the server cannot be established.

<span id="page-40-4"></span>• [--sleep=](#page-40-4)delay, -i delay

<span id="page-40-5"></span>

| Command-Line Format | sleep=delay |
|---------------------|-------------|

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-41-0"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-41-1"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-41-1)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-41-1) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-41-1) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_41_Picture_13.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-41-1) is OFF. In this case, setting [--ssl-fips-mode](#page-41-1) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-41-2"></span>• [--tls-ciphersuites=](#page-41-2)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-42-1"></span>• [--tls-sni-servername=](#page-42-1)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-42-2"></span>• [--tls-version=](#page-42-2)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-42-3"></span>• --user=[user\\_name](#page-42-3), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin, grant this user the SKIP\_QUERY\_REWRITE privilege.

<span id="page-42-0"></span>• [--verbose](#page-42-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print more information about what the program does.

<span id="page-42-4"></span>• [--version](#page-42-4), -V

| Command-Line Format | version | 413 |
|---------------------|---------|-----|
|---------------------|---------|-----|

<span id="page-43-0"></span>• [--vertical](#page-43-0), -E

| Command-Line Format | vertical |
|---------------------|----------|
|---------------------|----------|

Print output vertically. This is similar to [--relative](#page-39-3), but prints output vertically.

<span id="page-43-1"></span>• [--wait\[=](#page-43-1)count], -w[count]

| Command-Line Format | wait |
|---------------------|------|
|---------------------|------|

If the connection cannot be established, wait and retry instead of aborting. If a count value is given, it indicates the number of times to retry. The default is one time.

<span id="page-43-2"></span>• [--zstd-compression-level=](#page-43-2)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

# <span id="page-43-3"></span>**6.5.3 mysqlcheck — A Table Maintenance Program**

The [mysqlcheck](#page-43-3) client performs table maintenance: It checks, repairs, optimizes, or analyzes tables.

Each table is locked and therefore unavailable to other sessions while it is being processed, although for check operations, the table is locked with a READ lock only (see Section 15.3.6, "LOCK TABLES and UNLOCK TABLES Statements", for more information about READ and WRITE locks). Table maintenance operations can be time-consuming, particularly for large tables. If you use the [-](#page-48-0) [databases](#page-48-0) or [--all-databases](#page-46-0) option to process all tables in one or more databases, an invocation of [mysqlcheck](#page-43-3) might take a long time. (This is also true for the MySQL upgrade procedure if it determines that table checking is needed because it processes tables the same way.)

[mysqlcheck](#page-43-3) must be used when the mysqld server is running, which means that you do not have to stop the server to perform table maintenance.

[mysqlcheck](#page-43-3) uses the SQL statements CHECK TABLE, REPAIR TABLE, ANALYZE TABLE, and OPTIMIZE TABLE in a convenient way for the user. It determines which statements to use for the operation you want to perform, and then sends the statements to the server to be executed. For details about which storage engines each statement works with, see the descriptions for those statements in Section 15.7.3, "Table Maintenance Statements".

All storage engines do not necessarily support all four maintenance operations. In such cases, an error message is displayed. For example, if test.t is an MEMORY table, an attempt to check it produces this result:

```
$> mysqlcheck test t
test.t
note : The storage engine for the table doesn't support check
```

If [mysqlcheck](#page-43-3) is unable to repair a table, see Section 3.14, "Rebuilding or Repairing Tables or Indexes" for manual table repair strategies. This is the case, for example, for InnoDB tables, which can be checked with CHECK TABLE, but not repaired with REPAIR TABLE.

![](_page_44_Picture_1.jpeg)

#### **Caution**

It is best to make a backup of a table before performing a table repair operation; under some circumstances the operation might cause data loss. Possible causes include but are not limited to file system errors.

There are three general ways to invoke [mysqlcheck](#page-43-3):

```
mysqlcheck [options] db_name [tbl_name ...]
mysqlcheck [options] --databases db_name ...
mysqlcheck [options] --all-databases
```

If you do not name any tables following db\_name or if you use the [--databases](#page-48-0) or [--all](#page-46-0)[databases](#page-46-0) option, entire databases are checked.

[mysqlcheck](#page-43-3) has a special feature compared to other client programs. The default behavior of checking tables ([--check](#page-47-0)) can be changed by renaming the binary. If you want to have a tool that repairs tables by default, you should just make a copy of [mysqlcheck](#page-43-3) named mysqlrepair, or make a symbolic link to [mysqlcheck](#page-43-3) named mysqlrepair. If you invoke mysqlrepair, it repairs tables.

The names shown in the following table can be used to change [mysqlcheck](#page-43-3) default behavior.

| Command       | Meaning                       |
|---------------|-------------------------------|
| mysqlrepair   | The default option isrepair   |
| mysqlanalyze  | The default option isanalyze  |
| mysqloptimize | The default option isoptimize |

[mysqlcheck](#page-43-3) supports the following options, which can be specified on the command line or in the [mysqlcheck] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

#### **Table 6.12 mysqlcheck Options**

| Option Name            | Description                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------|
| all-databases          | Check all tables in all databases                                                            |
| all-in-1               | Execute a single statement for each database that<br>names all the tables from that database |
| analyze                | Analyze the tables                                                                           |
| auto-repair            | If a checked table is corrupted, automatically fix it                                        |
| bind-address           | Use specified network interface to connect to<br>MySQL Server                                |
| character-sets-dir     | Directory where character sets are installed                                                 |
| check                  | Check the tables for errors                                                                  |
| check-only-changed     | Check only tables that have changed since the<br>last check                                  |
| check-upgrade          | Invoke CHECK TABLE with the FOR UPGRADE<br>option                                            |
| compress               | Compress all information sent between client and<br>server                                   |
| compression-algorithms | Permitted compression algorithms for connections<br>to server                                |
| databases              | Interpret all arguments as database names                                                    |
| debug                  | Write debugging log                                                                          |
| debug-check            | Print debugging information when program exits                                               |

| Option Name             | Description                                                                             |
|-------------------------|-----------------------------------------------------------------------------------------|
| debug-info              | Print debugging information, memory, and CPU<br>statistics when program exits           |
| default-auth            | Authentication plugin to use                                                            |
| default-character-set   | Specify default character set                                                           |
| defaults-extra-file     | Read named option file in addition to usual option<br>files                             |
| defaults-file           | Read only named option file                                                             |
| defaults-group-suffix   | Option group suffix value                                                               |
| enable-cleartext-plugin | Enable cleartext authentication plugin                                                  |
| extended                | Check and repair tables                                                                 |
| fast                    | Check only tables that have not been closed<br>properly                                 |
| force                   | Continue even if an SQL error occurs                                                    |
| get-server-public-key   | Request RSA public key from server                                                      |
| help                    | Display help message and exit                                                           |
| host                    | Host on which MySQL server is located                                                   |
| login-path              | Read login path options from .mylogin.cnf                                               |
| medium-check            | Do a check that is faster than anextended<br>operation                                  |
| no-defaults             | Read no option files                                                                    |
| no-login-paths          | Do not read login paths from the login path file                                        |
| optimize                | Optimize the tables                                                                     |
| password                | Password to use when connecting to server                                               |
| password1               | First multifactor authentication password to use<br>when connecting to server           |
| password2               | Second multifactor authentication password to use<br>when connecting to server          |
| password3               | Third multifactor authentication password to use<br>when connecting to server           |
| pipe                    | Connect to server using named pipe (Windows<br>only)                                    |
| plugin-dir              | Directory where plugins are installed                                                   |
| port                    | TCP/IP port number for connection                                                       |
| print-defaults          | Print default options                                                                   |
| protocol                | Transport protocol to use                                                               |
| quick                   | The fastest method of checking                                                          |
| repair                  | Perform a repair that can fix almost anything<br>except unique keys that are not unique |
| server-public-key-path  | Path name to file containing RSA public key                                             |
| shared-memory-base-name | Shared-memory name for shared-memory<br>connections (Windows only)                      |
| silent                  | Silent mode                                                                             |
| skip-database           | Omit this database from performed operations                                            |
| socket                  | Unix socket file or Windows named pipe to use                                           |
|                         |                                                                                         |

| Option Name                               | Description                                                                                                               |
|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| ssl-ca                                    | File that contains list of trusted SSL Certificate<br>Authorities                                                         |
| ssl-capath                                | Directory that contains trusted SSL Certificate<br>Authority certificate files                                            |
| ssl-cert                                  | File that contains X.509 certificate                                                                                      |
| ssl-cipher                                | Permissible ciphers for connection encryption                                                                             |
| ssl-crl                                   | File that contains certificate revocation lists                                                                           |
| ssl-crlpath                               | Directory that contains certificate revocation-list<br>files                                                              |
| ssl-fips-mode                             | Whether to enable FIPS mode on client side                                                                                |
| ssl-key                                   | File that contains X.509 key                                                                                              |
| ssl-mode                                  | Desired security state of connection to server                                                                            |
| ssl-session-data                          | File that contains SSL session data                                                                                       |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails                                                                |
| tables                                    | Overrides thedatabases or -B option                                                                                       |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections                                                             |
| tls-sni-servername                        | Server name supplied by the client                                                                                        |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                                                                    |
| use-frm                                   | For repair operations on MyISAM tables                                                                                    |
| user                                      | MySQL user name to use when connecting to<br>server                                                                       |
| verbose                                   | Verbose mode                                                                                                              |
| version                                   | Display version information and exit                                                                                      |
| write-binlog                              | Log ANALYZE, OPTIMIZE, REPAIR statements<br>to binary logskip-write-binlog adds<br>NO_WRITE_TO_BINLOG to these statements |
| zstd-compression-level                    | Compression level for connections to server that<br>use zstd compression                                                  |

## <span id="page-46-2"></span>• [--help](#page-46-2), -?

| Command-Line Format | help |
|---------------------|------|

Display a help message and exit.

<span id="page-46-0"></span>• [--all-databases](#page-46-0), -A

| Command-Line Format | all-databases |
|---------------------|---------------|
|---------------------|---------------|

Check all tables in all databases. This is the same as using the [--databases](#page-48-0) option and naming all the databases on the command line, except that the INFORMATION\_SCHEMA and performance\_schema databases are not checked. They can be checked by explicitly naming them with the [--databases](#page-48-0) option.

<span id="page-46-1"></span>• [--all-in-1](#page-46-1), -1

| Command-Line Format | all-in-1 |
|---------------------|----------|

Instead of issuing a statement for each table, execute a single statement for each database that names all the tables from that database to be processed.

<span id="page-47-1"></span>• [--analyze](#page-47-1), -a

| Command-Line Format | analyze |
|---------------------|---------|
|---------------------|---------|

Analyze the tables.

<span id="page-47-2"></span>• [--auto-repair](#page-47-2)

| Command-Line Format | auto-repair |
|---------------------|-------------|

If a checked table is corrupted, automatically fix it. Any necessary repairs are done after all tables have been checked.

<span id="page-47-3"></span>• [--bind-address=](#page-47-3)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-47-4"></span>• [--character-sets-dir=](#page-47-4)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-47-0"></span>• [--check](#page-47-0), -c

| Command-Line Format | check |
|---------------------|-------|

Check the tables for errors. This is the default operation.

<span id="page-47-5"></span>• [--check-only-changed](#page-47-5), -C

| Command-Line Format | check-only-changed |
|---------------------|--------------------|
|---------------------|--------------------|

Check only tables that have changed since the last check or that have not been closed properly.

<span id="page-47-6"></span>• [--check-upgrade](#page-47-6), -g

| Command-Line Format | check-upgrade |
|---------------------|---------------|

Invoke CHECK TABLE with the FOR UPGRADE option to check tables for incompatibilities with the current version of the server.

<span id="page-47-7"></span>• [--compress](#page-47-7)

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-48-1"></span>• [--compression-algorithms=](#page-48-1)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-48-0"></span>• [--databases](#page-48-0), -B

| Command-Line Format | databases |
|---------------------|-----------|

Process all tables in the named databases. Normally, [mysqlcheck](#page-43-3) treats the first name argument on the command line as a database name and any following names as table names. With this option, it treats all name arguments as database names.

<span id="page-48-2"></span>• --debug[=[debug\\_options](#page-48-2)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-48-3"></span>• [--debug-check](#page-48-3)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |

| Default Value | FALSE |
|---------------|-------|
|---------------|-------|

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-49-0"></span>• [--debug-info](#page-49-0)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-49-1"></span>• [--default-character-set=](#page-49-1)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

<span id="page-49-2"></span>• [--defaults-extra-file=](#page-49-2)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-49-3"></span>• [--defaults-file=](#page-49-3)file\_name

<span id="page-49-4"></span>• [--defaults-group-suffix=](#page-49-4)str

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlcheck](#page-43-3) normally reads the [client] and [mysqlcheck] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-49-4), [mysqlcheck](#page-43-3) also reads the [client\_other] and [mysqlcheck\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-50-2"></span>• [--extended](#page-50-2), -e

| Command-Line Format | extended |
|---------------------|----------|
|---------------------|----------|

If you are using this option to check tables, it ensures that they are 100% consistent but takes a long time.

If you are using this option to repair tables, it runs an extended repair that may not only take a long time to execute, but may produce a lot of garbage rows also!

<span id="page-50-0"></span>• [--default-auth=](#page-50-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-50-1"></span>• [--enable-cleartext-plugin](#page-50-1)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-50-3"></span>• [--fast](#page-50-3), -F

| Command-Line Format | fast |
|---------------------|------|
|---------------------|------|

Check only tables that have not been closed properly.

<span id="page-50-4"></span>• [--force](#page-50-4), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Continue even if an SQL error occurs.

<span id="page-50-5"></span>• [--get-server-public-key](#page-50-5)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-54-2)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-50-5).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-51-0"></span>• --host=[host\\_name](#page-51-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-51-1"></span>• [--login-path=](#page-51-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-51-3"></span>• [--no-login-paths](#page-51-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-51-2"></span>• [--medium-check](#page-51-2), -m

| Command-Line Format | medium-check |
|---------------------|--------------|
|---------------------|--------------|

<span id="page-52-1"></span>• [--no-defaults](#page-52-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-52-1) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-52-1) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-52-0"></span>• [--optimize](#page-52-0), -o

| Command-Line Format | optimize |
|---------------------|----------|

## Optimize the tables.

<span id="page-52-2"></span>• [--password\[=](#page-52-2)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlcheck](#page-43-3) prompts for one. If given, there must be no space between [-](#page-52-2) [password=](#page-52-2) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlcheck](#page-43-3) should not prompt for one, use the [--skip-password](#page-52-2) option.

<span id="page-52-3"></span>• [--password1\[=](#page-52-3)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlcheck](#page-43-3) prompts for one. If given, there must be no space between [--password1=](#page-52-3) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlcheck](#page-43-3) should not prompt for one, use the [--skip-password1](#page-52-3) option.

<span id="page-53-0"></span>• [--password2\[=](#page-53-0)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-52-3); see the description of that option for details.

<span id="page-53-1"></span>• [--password3\[=](#page-53-1)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-52-3); see the description of that option for details.

<span id="page-53-2"></span>• [--pipe](#page-53-2), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-53-3"></span>• [--plugin-dir=](#page-53-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-50-0) option is used to specify an authentication plugin but [mysqlcheck](#page-43-3) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-53-4"></span>• --port=[port\\_num](#page-53-4), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-53-5"></span>• [--print-defaults](#page-53-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-53-6"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-53-6)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |

| SOCKET |
|--------|
| PIPE   |
| MEMORY |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-54-1"></span>• [--quick](#page-54-1), -q

| Command-Line Format | quick |
|---------------------|-------|
|---------------------|-------|

If you are using this option to check tables, it prevents the check from scanning the rows to check for incorrect links. This is the fastest check method.

If you are using this option to repair tables, it tries to repair only the index tree. This is the fastest repair method.

<span id="page-54-0"></span>• [--repair](#page-54-0), -r

| Command-Line Format | repair |
|---------------------|--------|
|---------------------|--------|

Perform a repair that can fix almost anything except unique keys that are not unique.

<span id="page-54-2"></span>• [--server-public-key-path=](#page-54-2)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-54-2)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-50-5).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-54-3"></span>• [--shared-memory-base-name=](#page-54-3)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-55-0"></span>• [--silent](#page-55-0), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Silent mode. Print only error messages.

<span id="page-55-1"></span>• [--skip-database=](#page-55-1)db\_name

| Command-Line Format | skip-database=db_name |
|---------------------|-----------------------|
|---------------------|-----------------------|

Do not include the named database (case-sensitive) in the operations performed by [mysqlcheck](#page-43-3).

<span id="page-55-2"></span>• [--socket=](#page-55-2)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-55-3"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-55-4"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-55-4)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-55-4) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-55-4) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.

• STRICT: Enable "strict" FIPS mode.

![](_page_56_Picture_2.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-55-4) is OFF. In this case, setting [--ssl-fips-mode](#page-55-4) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-56-0"></span>• [--tables](#page-56-0)

| Command-Line Format | tables |
|---------------------|--------|
|---------------------|--------|

Override the [--databases](#page-48-0) or -B option. All name arguments following the option are regarded as table names.

<span id="page-56-1"></span>• [--tls-ciphersuites=](#page-56-1)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-56-2"></span>• [--tls-sni-servername=](#page-56-2)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-56-3"></span>• [--tls-version=](#page-56-3)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-57-1"></span>• [--use-frm](#page-57-1)

For repair operations on MyISAM tables, get the table structure from the data dictionary so that the table can be repaired even if the .MYI header is corrupted.

<span id="page-57-2"></span>• --user=[user\\_name](#page-57-2), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

<span id="page-57-3"></span>• [--verbose](#page-57-3), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print information about the various stages of program operation.

<span id="page-57-4"></span>• [--version](#page-57-4), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-57-5"></span>• [--write-binlog](#page-57-5)

| Command-Line Format | write-binlog |
|---------------------|--------------|

This option is enabled by default, so that ANALYZE TABLE, OPTIMIZE TABLE, and REPAIR TABLE statements generated by [mysqlcheck](#page-43-3) are written to the binary log. Use [--skip-write-binlog](#page-57-5) to cause NO\_WRITE\_TO\_BINLOG to be added to the statements so that they are not logged. Use the [--skip-write-binlog](#page-57-5) when these statements should not be sent to replicas or run when using the binary logs for recovery from backup.

<span id="page-57-6"></span>• [--zstd-compression-level=](#page-57-6)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

<span id="page-57-0"></span>The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

The [mysqldump](#page-57-0) client utility performs logical backups, producing a set of SQL statements that can be executed to reproduce the original database object definitions and table data. It dumps one or more MySQL databases for backup or transfer to another SQL server. The [mysqldump](#page-57-0) command can also generate output in CSV, other delimited text, or XML format.

![](_page_58_Picture_2.jpeg)

#### **Tip**

Consider using the [MySQL Shell dump utilities,](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md) which provide parallel dumping with multiple threads, file compression, and progress information display, as well as cloud features such as Oracle Cloud Infrastructure Object Storage streaming, and MySQL HeatWave compatibility checks and modifications. Dumps can be easily imported into a MySQL Server instance or a MySQL HeatWave DB System using the [MySQL Shell load dump utilities.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-load-dump.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md)

- [Performance and Scalability Considerations](#page-59-0)
- [Invocation Syntax](#page-59-1)
- [Option Syntax Alphabetical Summary](#page-60-0)
- [Connection Options](#page-64-0)
- [Option-File Options](#page-71-0)
- [DDL Options](#page-72-0)
- [Debug Options](#page-74-0)
- [Help Options](#page-76-0)
- [Internationalization Options](#page-76-1)
- [Replication Options](#page-77-0)
- [Format Options](#page-82-0)
- [Filtering Options](#page-86-0)
- [Performance Options](#page-89-0)
- [Transactional Options](#page-91-0)
- [Option Groups](#page-93-0)
- [Examples](#page-93-1)
- [Restrictions](#page-94-0)

[mysqldump](#page-57-0) requires at least the SELECT privilege for dumped tables, SHOW VIEW for dumped views, TRIGGER for dumped triggers, LOCK TABLES if the [--single-transaction](#page-93-2) option is not used, PROCESS if the [--no-tablespaces](#page-74-1) option is not used, and the RELOAD or FLUSH\_TABLES privilege with [--single-transaction](#page-93-2) if both gtid\_mode=ON and gtid\_purged=ON|AUTO. Certain options might require other privileges as noted in the option descriptions.

To reload a dump file, you must have the privileges required to execute the statements that it contains, such as the appropriate CREATE privileges for objects created by those statements.

[mysqldump](#page-57-0) output can include ALTER DATABASE statements that change the database collation. These may be used when dumping stored programs to preserve their character encodings. To reload a dump file containing such statements, the ALTER privilege for the affected database is required.

![](_page_59_Picture_1.jpeg)

#### **Note**

A dump made using PowerShell on Windows with output redirection creates a file that has UTF-16 encoding:

```
mysqldump [options] > dump.sql
```

However, UTF-16 is not permitted as a connection character set (see Impermissible Client Character Sets), so the dump file cannot be loaded correctly. To work around this issue, use the --result-file option, which creates the output in ASCII format:

```
mysqldump [options] --result-file=dump.sql
```

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid\_mode=ON), if your dump file includes system tables. [mysqldump](#page-57-0) issues DML instructions for the system tables which use the non-transactional MyISAM storage engine, and this combination is not permitted when GTIDs are enabled.

# <span id="page-59-0"></span>**Performance and Scalability Considerations**

mysqldump advantages include the convenience and flexibility of viewing or even editing the output before restoring. You can clone databases for development and DBA work, or produce slight variations of an existing database for testing. It is not intended as a fast or scalable solution for backing up substantial amounts of data. With large data sizes, even if the backup step takes a reasonable time, restoring the data can be very slow because replaying the SQL statements involves disk I/O for insertion, index creation, and so on.

For large-scale backup and restore, a physical backup is more appropriate, to copy the data files in their original format so that they can be restored quickly.

If your tables are primarily InnoDB tables, or if you have a mix of InnoDB and MyISAM tables, consider using mysqlbackup, which is available as part of MySQL Enterprise. This tool provides high performance for InnoDB backups with minimal disruption; it can also back up tables from MyISAM and other storage engines; it also provides a number of convenient options to accommodate different backup scenarios. See Section 32.1, "MySQL Enterprise Backup Overview".

[mysqldump](#page-57-0) can retrieve and dump table contents row by row, or it can retrieve the entire content from a table and buffer it in memory before dumping it. Buffering in memory can be a problem if you are dumping large tables. To dump tables row by row, use the [--quick](#page-91-1) option (or [--opt](#page-90-0), which enables [--quick](#page-91-1)). The [--opt](#page-90-0) option (and hence [--quick](#page-91-1)) is enabled by default, so to enable memory buffering, use [--skip-quick](#page-91-1).

If you are using a recent version of [mysqldump](#page-57-0) to generate a dump to be reloaded into a very old MySQL server, use the [--skip-opt](#page-91-2) option instead of the [--opt](#page-90-0) or [--extended-insert](#page-89-1) option.

For additional information about [mysqldump](#page-57-0), see Section 9.4, "Using mysqldump for Backups".

# <span id="page-59-1"></span>**Invocation Syntax**

There are in general three ways to use [mysqldump](#page-57-0)—in order to dump a set of one or more tables, a set of one or more complete databases, or an entire MySQL server—as shown here:

```
mysqldump [options] db_name [tbl_name ...]
mysqldump [options] --databases db_name ...
mysqldump [options] --all-databases
```

To dump entire databases, do not name any tables following db\_name, or use the [--databases](#page-86-1) or [--all-databases](#page-86-2) option.

To see a list of the options your version of [mysqldump](#page-57-0) supports, issue the command [mysqldump](#page-57-0) [-](#page-76-2) [help](#page-76-2).

# <span id="page-60-0"></span>**Option Syntax - Alphabetical Summary**

[mysqldump](#page-57-0) supports the following options, which can be specified on the command line or in the [mysqldump] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.13 mysqldump Options**

| Option Name              | Description                                                                                                   |
|--------------------------|---------------------------------------------------------------------------------------------------------------|
| add-drop-database        | Add DROP DATABASE statement before each<br>CREATE DATABASE statement                                          |
| add-drop-table           | Add DROP TABLE statement before each<br>CREATE TABLE statement                                                |
| add-drop-trigger         | Add DROP TRIGGER statement before each<br>CREATE TRIGGER statement                                            |
| add-locks                | Surround each table dump with LOCK TABLES<br>and UNLOCK TABLES statements                                     |
| all-databases            | Dump all tables in all databases                                                                              |
| allow-keywords           | Allow creation of column names that are keywords                                                              |
| apply-replica-statements | Include STOP REPLICA prior to CHANGE<br>REPLICATION SOURCE TO statement and<br>START REPLICA at end of output |
| apply-slave-statements   | Include STOP SLAVE prior to CHANGE MASTER<br>statement and START SLAVE at end of output                       |
| bind-address             | Use specified network interface to connect to<br>MySQL Server                                                 |
| character-sets-dir       | Directory where character sets are installed                                                                  |
| column-statistics        | Write ANALYZE TABLE statements to generate<br>statistics histograms                                           |
| comments                 | Add comments to dump file                                                                                     |
| compact                  | Produce more compact output                                                                                   |
| compatible               | Produce output that is more compatible with other<br>database systems or with older MySQL servers             |
| complete-insert          | Use complete INSERT statements that include<br>column names                                                   |
| compress                 | Compress all information sent between client and<br>server                                                    |
| compression-algorithms   | Permitted compression algorithms for connections<br>to server                                                 |
| create-options           | Include all MySQL-specific table options in<br>CREATE TABLE statements                                        |
| databases                | Interpret all name arguments as database names                                                                |
| debug                    | Write debugging log                                                                                           |
| debug-check              | Print debugging information when program exits                                                                |
| debug-info               | Print debugging information, memory, and CPU<br>statistics when program exits                                 |
| default-auth             | Authentication plugin to use                                                                                  |
| default-character-set    | Specify default character set                                                                                 |
|                          |                                                                                                               |

| Option Name                   | Description                                                                                                     |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------|
| defaults-extra-file           | Read named option file in addition to usual option<br>files                                                     |
| defaults-file                 | Read only named option file                                                                                     |
| defaults-group-suffix         | Option group suffix value                                                                                       |
| delete-master-logs            | On a replication source server, delete the binary<br>logs after performing the dump operation                   |
| delete-source-logs            | On a replication source server, delete the binary<br>logs after performing the dump operation                   |
| disable-keys                  | For each table, surround INSERT statements with<br>statements to disable and enable keys                        |
| dump-date                     | Include dump date as "Dump completed on"<br>comment ifcomments is given                                         |
| dump-replica                  | Include CHANGE REPLICATION SOURCE TO<br>statement that lists binary log coordinates of<br>replica's source      |
| dump-slave                    | Include CHANGE MASTER statement that lists<br>binary log coordinates of replica's source                        |
| enable-cleartext-plugin       | Enable cleartext authentication plugin                                                                          |
| events                        | Dump events from dumped databases                                                                               |
| extended-insert               | Use multiple-row INSERT syntax                                                                                  |
| fields-enclosed-by            | This option is used with thetab option and has<br>the same meaning as the corresponding clause<br>for LOAD DATA |
| fields-escaped-by             | This option is used with thetab option and has<br>the same meaning as the corresponding clause<br>for LOAD DATA |
| fields-optionally-enclosed-by | This option is used with thetab option and has<br>the same meaning as the corresponding clause<br>for LOAD DATA |
| fields-terminated-by          | This option is used with thetab option and has<br>the same meaning as the corresponding clause<br>for LOAD DATA |
| flush-logs                    | Flush MySQL server log files before starting dump                                                               |
| flush-privileges              | Emit a FLUSH PRIVILEGES statement after<br>dumping mysql database                                               |
| force                         | Continue even if an SQL error occurs during a<br>table dump                                                     |
| get-server-public-key         | Request RSA public key from server                                                                              |
| help                          | Display help message and exit                                                                                   |
| hex-blob                      | Dump binary columns using hexadecimal notation                                                                  |
| host                          | Host on which MySQL server is located                                                                           |
| ignore-error                  | Ignore specified errors                                                                                         |
| ignore-table                  | Do not dump given table                                                                                         |
| ignore-views                  | Skip dumping table views                                                                                        |

| Option Name              | Description                                                                                                               |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------|
| include-master-host-port | Include MASTER_HOST/MASTER_PORT options<br>in CHANGE MASTER statement produced with<br>dump-slave                         |
| include-source-host-port | Include SOURCE_HOST and SOURCE_PORT<br>options in CHANGE REPLICATION SOURCE TO<br>statement produced withdump-replica     |
| init-command             | Single SQL statement to execute after connecting<br>or re-connecting to MySQL server; resets existing<br>defined commands |
| init-command-add         | Add an additional SQL statement to execute after<br>connecting or re-connecting to MySQL server                           |
| insert-ignore            | Write INSERT IGNORE rather than INSERT<br>statements                                                                      |
| lines-terminated-by      | This option is used with thetab option and has<br>the same meaning as the corresponding clause<br>for LOAD DATA           |
| lock-all-tables          | Lock all tables across all databases                                                                                      |
| lock-tables              | Lock all tables before dumping them                                                                                       |
| log-error                | Append warnings and errors to named file                                                                                  |
| login-path               | Read login path options from .mylogin.cnf                                                                                 |
| master-data              | Write the binary log file name and position to the<br>output                                                              |
| max-allowed-packet       | Maximum packet length to send to or receive from<br>server                                                                |
| mysqld-long-query-time   | Session value for slow query threshold                                                                                    |
| net-buffer-length        | Buffer size for TCP/IP and socket communication                                                                           |
| network-timeout          | Increase network timeouts to permit larger table<br>dumps                                                                 |
| no-autocommit            | Enclose the INSERT statements for each dumped<br>table within SET autocommit = 0 and COMMIT<br>statements                 |
| no-create-db             | Do not write CREATE DATABASE statements                                                                                   |
| no-create-info           | Do not write CREATE TABLE statements that re<br>create each dumped table                                                  |
| no-data                  | Do not dump table contents                                                                                                |
| no-defaults              | Read no option files                                                                                                      |
| no-login-paths           | Do not read login paths from the login path file                                                                          |
| no-set-names             | Same asskip-set-charset                                                                                                   |
| no-tablespaces           | Do not write any CREATE LOGFILE GROUP or<br>CREATE TABLESPACE statements in output                                        |
| opt                      | Shorthand foradd-drop-tableadd-locks<br>create-optionsdisable-keysextended-insert<br>lock-tablesquickset-charset          |
| order-by-primary         | Dump each table's rows sorted by its primary key,<br>or by its first unique index                                         |
| output-as-version        | Determines replica and event terminology used in<br>dumps; for compatibility with older versions                          |

| Option Name                                | Description                                                                           |
|--------------------------------------------|---------------------------------------------------------------------------------------|
| password                                   | Password to use when connecting to server                                             |
| password1                                  | First multifactor authentication password to use<br>when connecting to server         |
| password2                                  | Second multifactor authentication password to use<br>when connecting to server        |
| password3                                  | Third multifactor authentication password to use<br>when connecting to server         |
| pipe                                       | Connect to server using named pipe (Windows<br>only)                                  |
| plugin-authentication-kerberos-client-mode | Permit GSSAPI pluggable authentication through<br>the MIT Kerberos library on Windows |
| plugin-dir                                 | Directory where plugins are installed                                                 |
| port                                       | TCP/IP port number for connection                                                     |
| print-defaults                             | Print default options                                                                 |
| protocol                                   | Transport protocol to use                                                             |
| quick                                      | Retrieve rows for a table from the server a row at<br>a time                          |
| quote-names                                | Quote identifiers within backtick characters                                          |
| replace                                    | Write REPLACE statements rather than INSERT<br>statements                             |
| result-file                                | Direct output to a given file                                                         |
| routines                                   | Dump stored routines (procedures and functions)<br>from dumped databases              |
| server-public-key-path                     | Path name to file containing RSA public key                                           |
| set-charset                                | Add SET NAMES default_character_set to output                                         |
| set-gtid-purged                            | Whether to add SET<br>@@GLOBAL.GTID_PURGED to output                                  |
| shared-memory-base-name                    | Shared-memory name for shared-memory<br>connections (Windows only)                    |
| show-create-skip-secondary-engine          | Exclude SECONDARY ENGINE clause from<br>CREATE TABLE statements                       |
| single-transaction                         | Issue a BEGIN SQL statement before dumping<br>data from server                        |
| skip-add-drop-table                        | Do not add a DROP TABLE statement before<br>each CREATE TABLE statement               |
| skip-add-locks                             | Do not add locks                                                                      |
| skip-comments                              | Do not add comments to dump file                                                      |
| skip-compact                               | Do not produce more compact output                                                    |
| skip-disable-keys                          | Do not disable keys                                                                   |
| skip-extended-insert                       | Turn off extended-insert                                                              |
| skip-generated-invisible-primary-key       | Do not include generated invisible primary keys in<br>dump file                       |
| skip-opt                                   | Turn off options set byopt                                                            |
| skip-quick                                 | Do not retrieve rows for a table from the server a<br>row at a time                   |

| Option Name                               | Description                                                                    |
|-------------------------------------------|--------------------------------------------------------------------------------|
| skip-quote-names                          | Do not quote identifiers                                                       |
| skip-set-charset                          | Do not write SET NAMES statement                                               |
| skip-triggers                             | Do not dump triggers                                                           |
| skip-tz-utc                               | Turn off tz-utc                                                                |
| socket                                    | Unix socket file or Windows named pipe to use                                  |
| source-data                               | Write the binary log file name and position to the<br>output                   |
| ssl-ca                                    | File that contains list of trusted SSL Certificate<br>Authorities              |
| ssl-capath                                | Directory that contains trusted SSL Certificate<br>Authority certificate files |
| ssl-cert                                  | File that contains X.509 certificate                                           |
| ssl-cipher                                | Permissible ciphers for connection encryption                                  |
| ssl-crl                                   | File that contains certificate revocation lists                                |
| ssl-crlpath                               | Directory that contains certificate revocation-list<br>files                   |
| ssl-fips-mode                             | Whether to enable FIPS mode on client side                                     |
| ssl-key                                   | File that contains X.509 key                                                   |
| ssl-mode                                  | Desired security state of connection to server                                 |
| ssl-session-data                          | File that contains SSL session data                                            |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails                     |
| tab                                       | Produce tab-separated data files                                               |
| tables                                    | Overridedatabases or -B option                                                 |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections                  |
| tls-sni-servername                        | Server name supplied by the client                                             |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                         |
| triggers                                  | Dump triggers for each dumped table                                            |
| tz-utc                                    | Add SET TIME_ZONE='+00:00' to dump file                                        |
| user                                      | MySQL user name to use when connecting to<br>server                            |
| verbose                                   | Verbose mode                                                                   |
| version                                   | Display version information and exit                                           |
| where                                     | Dump only rows selected by given WHERE<br>condition                            |
| xml                                       | Produce XML output                                                             |
| zstd-compression-level                    | Compression level for connections to server that<br>use zstd compression       |

# <span id="page-64-0"></span>**Connection Options**

The [mysqldump](#page-57-0) command logs into a MySQL server to extract information. The following options specify how to connect to the MySQL server, either on the same machine or a remote system.

<span id="page-65-0"></span>• [--bind-address=](#page-65-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-65-1"></span>• [--compress](#page-65-1), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-65-2"></span>• [--compression-algorithms=](#page-65-2)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-65-3"></span>• [--default-auth=](#page-65-3)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-65-4"></span>• [--enable-cleartext-plugin](#page-65-4)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |

| Default Value | FALSE |  |
|---------------|-------|--|
|---------------|-------|--|

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-66-0"></span>• [--get-server-public-key](#page-66-0)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-69-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-66-0).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-66-1"></span>• --host=[host\\_name](#page-66-1), -h host\_name

| Command-Line Format<br>host |  |
|-----------------------------|--|
|-----------------------------|--|

Dump data from the MySQL server on the given host. The default host is localhost.

<span id="page-66-2"></span>• [--login-path=](#page-66-2)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-66-3"></span>• [--no-login-paths](#page-66-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|

Skips reading options from the login path file.

See [--login-path](#page-66-2) for related information.

Line Options that Affect Option-File Handling".

437

<span id="page-67-0"></span>• [--password\[=](#page-67-0)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqldump](#page-57-0) prompts for one. If given, there must be no space between [-](#page-67-0) [password=](#page-67-0) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqldump](#page-57-0) should not prompt for one, use the [--skip-password](#page-67-0) option.

<span id="page-67-1"></span>• [--password1\[=](#page-67-1)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqldump](#page-57-0) prompts for one. If given, there must be no space between [--password1=](#page-67-1) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqldump](#page-57-0) should not prompt for one, use the [--skip-password1](#page-67-1) option.

[--password1](#page-67-1) and [--password](#page-67-0) are synonymous, as are [--skip-password1](#page-67-1) and [--skip](#page-67-0)[password](#page-67-0).

<span id="page-67-2"></span>• [--password2\[=](#page-67-2)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-67-1); see the description of that option for details.

<span id="page-67-3"></span>• [--password3\[=](#page-67-3)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-67-1); see the description of that option for details.

<span id="page-67-4"></span>• [--pipe](#page-67-4), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the <span id="page-68-0"></span>• [--plugin-authentication-kerberos-client-mode=](#page-68-0)value

| Command-Line Format | plugin-authentication-kerberos<br>client-mode |
|---------------------|-----------------------------------------------|
| Type                | String                                        |
| Default Value       | SSPI                                          |
| Valid Values        | GSSAPI                                        |

On Windows, the authentication\_kerberos\_client authentication plugin supports this plugin option. It provides two possible values that the client user can set at runtime: SSPI and GSSAPI.

The default value for the client-side plugin option uses Security Support Provider Interface (SSPI), which is capable of acquiring credentials from the Windows in-memory cache. Alternatively, the client user can select a mode that supports Generic Security Service Application Program Interface (GSSAPI) through the MIT Kerberos library on Windows. GSSAPI is capable of acquiring cached credentials previously generated by using the kinit command.

For more information, see Commands for Windows Clients in GSSAPI Mode.

<span id="page-68-1"></span>• [--plugin-dir=](#page-68-1)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-65-3) option is used to specify an authentication plugin but [mysqldump](#page-57-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-68-2"></span>• --port=[port\\_num](#page-68-2), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-68-3"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-68-3)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

<span id="page-69-0"></span>• [--server-public-key-path=](#page-69-0)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-69-0)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-66-0).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-69-1"></span>• [--socket=](#page-69-1)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-69-2"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-69-3"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-69-3)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |

STRICT

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-69-3) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-69-3) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_70_Picture_7.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-69-3) is OFF. In this case, setting [--ssl-fips-mode](#page-69-3) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-70-0"></span>• [--tls-ciphersuites=](#page-70-0)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-70-1"></span>• [--tls-sni-servername=](#page-70-1)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-70-2"></span>• [--tls-version=](#page-70-2)protocol\_list

| Command-Line Format | tls-version=protocol_list                                         |
|---------------------|-------------------------------------------------------------------|
| Type                | String                                                            |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>441<br>(OpenSSL 1.1.1 or higher) |

```
TLSv1,TLSv1.1,TLSv1.2 (otherwise)
```

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-71-3"></span>• --user=[user\\_name](#page-71-3), -u user\_name

| Command-Line Format | user=user_name |
|---------------------|----------------|
| Type                | String         |

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin, you should grant this user the SKIP\_QUERY\_REWRITE privilege.

<span id="page-71-4"></span>• [--zstd-compression-level=](#page-71-4)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

# <span id="page-71-1"></span><span id="page-71-0"></span>**Option-File Options**

These options are used to control which option files to read.

• [--defaults-extra-file=](#page-71-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-71-2"></span>• [--defaults-file=](#page-71-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

442

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-72-2"></span>• [--defaults-group-suffix=](#page-72-2)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqldump](#page-57-0) normally reads the [client] and [mysqldump] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-72-2), [mysqldump](#page-57-0) also reads the [client\_other] and [mysqldump\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-72-3"></span>• [--no-defaults](#page-72-3)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|                     |             |

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-72-3) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-72-3) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-72-4"></span>• [--print-defaults](#page-72-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

# <span id="page-72-0"></span>**DDL Options**

Usage scenarios for [mysqldump](#page-57-0) include setting up an entire new MySQL instance (including database tables), and replacing data inside an existing instance with existing databases and tables. The following options let you specify which things to tear down and set up when restoring a dump, by encoding various DDL statements within the dump file.

<span id="page-72-1"></span>• [--add-drop-database](#page-72-1)

| Command-Line Format | add-drop-database |
|---------------------|-------------------|
|---------------------|-------------------|

Write a DROP DATABASE statement before each CREATE DATABASE statement. This option is typically used in conjunction with the [--all-databases](#page-86-2) or [--databases](#page-86-1) option because no CREATE DATABASE statements are written unless one of those options is specified.

![](_page_73_Picture_1.jpeg)

#### **Note**

In MySQL 8.4, the mysql schema is considered a system schema that cannot be dropped by end users. If [--add-drop-database](#page-72-1) is used with [--all-databases](#page-86-2) or with [--databases](#page-86-1) where the list of schemas to be dumped includes mysql, the dump file contains a DROP DATABASE `mysql` statement that causes an error when the dump file is reloaded.

Instead, to use [--add-drop-database](#page-72-1), use [--databases](#page-86-1) with a list of schemas to be dumped, where the list does not include mysql.

<span id="page-73-0"></span>• [--add-drop-table](#page-73-0)

| Command-Line Format | add-drop-table |
|---------------------|----------------|
|---------------------|----------------|

Write a DROP TABLE statement before each CREATE TABLE statement.

<span id="page-73-1"></span>• [--add-drop-trigger](#page-73-1)

| Command-Line Format | add-drop-trigger |
|---------------------|------------------|
|---------------------|------------------|

Write a DROP TRIGGER statement before each CREATE TRIGGER statement.

<span id="page-73-4"></span>• [--all-tablespaces](#page-73-4), -Y

| Command-Line Format | all-tablespaces |
|---------------------|-----------------|
|---------------------|-----------------|

Adds to a table dump all SQL statements needed to create any tablespaces used by an NDB table. This information is not otherwise included in the output from [mysqldump](#page-57-0). This option is currently relevant only to NDB Cluster tables.

<span id="page-73-2"></span>• [--no-create-db](#page-73-2), -n

| Command-Line Format<br>no-create-db |  |
|-------------------------------------|--|
|-------------------------------------|--|

Suppress the CREATE DATABASE statements that are otherwise included in the output if the [-](#page-86-1) [databases](#page-86-1) or [--all-databases](#page-86-2) option is given.

<span id="page-73-3"></span>• [--no-create-info](#page-73-3), -t

| Command-Line Format | no-create-info |
|---------------------|----------------|
|---------------------|----------------|

Do not write CREATE TABLE statements that create each dumped table.

![](_page_73_Picture_20.jpeg)

## **Note**

This option does not exclude statements creating log file groups or tablespaces from [mysqldump](#page-57-0) output; however, you can use the [--no](#page-74-1)[tablespaces](#page-74-1) option for this purpose. <sup>444</sup>

<span id="page-74-1"></span>• [--no-tablespaces](#page-74-1), -y

| Command-Line Format | no-tablespaces |
|---------------------|----------------|
|---------------------|----------------|

This option suppresses all CREATE LOGFILE GROUP and CREATE TABLESPACE statements in the output of [mysqldump](#page-57-0).

<span id="page-74-6"></span>• [--replace](#page-74-6)

| Command-Line Format | replace |
|---------------------|---------|
|---------------------|---------|

Write REPLACE statements rather than INSERT statements.

# <span id="page-74-0"></span>**Debug Options**

The following options print debugging information, encode debugging information in the dump file, or let the dump operation proceed regardless of potential problems.

<span id="page-74-2"></span>• [--allow-keywords](#page-74-2)

| Command-Line Format | allow-keywords |
|---------------------|----------------|
|---------------------|----------------|

Permit creation of column names that are keywords. This works by prefixing each column name with the table name.

<span id="page-74-3"></span>• [--comments](#page-74-3), -i

| Command-Line Format | comments |
|---------------------|----------|
|---------------------|----------|

Write additional information in the dump file such as program version, server version, and host. This option is enabled by default. To suppress this additional information, use [--skip-comments](#page-75-4).

<span id="page-74-4"></span>• --debug[=[debug\\_options](#page-74-4)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]      |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | d:t:o,/tmp/mysqldump.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default value is d:t:o,/tmp/mysqldump.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-74-5"></span>• [--debug-check](#page-74-5)

| Command-Line Format | 445<br>debug-check |
|---------------------|--------------------|
| Type                | Boolean            |
| Default Value       | FALSE              |

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-75-0"></span>• [--debug-info](#page-75-0)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-75-1"></span>• [--dump-date](#page-75-1)

| Command-Line Format | dump-date |
|---------------------|-----------|
| Type                | Boolean   |
| Default Value       | TRUE      |

If the [--comments](#page-74-3) option is given, [mysqldump](#page-57-0) produces a comment at the end of the dump of the following form:

```
-- Dump completed on DATE
```

However, the date causes dump files taken at different times to appear to be different, even if the data are otherwise identical. [--dump-date](#page-75-1) and [--skip-dump-date](#page-75-1) control whether the date is added to the comment. The default is [--dump-date](#page-75-1) (include the date in the comment). [--skip](#page-75-1)[dump-date](#page-75-1) suppresses date printing.

## <span id="page-75-2"></span>• [--force](#page-75-2), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Ignore all errors; continue even if an SQL error occurs during a table dump.

One use for this option is to cause [mysqldump](#page-57-0) to continue executing even when it encounters a view that has become invalid because the definition refers to a table that has been dropped. Without --force, [mysqldump](#page-57-0) exits with an error message. With --force, [mysqldump](#page-57-0) prints the error message, but it also writes an SQL comment containing the view definition to the dump output and continues executing.

If the [--ignore-error](#page-87-0) option is also given to ignore specific errors, [--force](#page-75-2) takes precedence.

## <span id="page-75-3"></span>• [--log-error=](#page-75-3)file\_name

| Command-Line Format | log-error=file_name |
|---------------------|---------------------|
| Type                | File name           |

Log warnings and errors by appending them to the named file. The default is to do no logging.

## <span id="page-75-4"></span>• [--skip-comments](#page-75-4)

| Command-Line Format | skip-comments |
|---------------------|---------------|
|                     |               |

See the description for the [--comments](#page-74-3) option.

<span id="page-76-6"></span>• [--verbose](#page-76-6), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print more information about what the program does.

# <span id="page-76-2"></span><span id="page-76-0"></span>**Help Options**

The following options display information about the [mysqldump](#page-57-0) command itself.

• [--help](#page-76-2), -?

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Display a help message and exit.

<span id="page-76-7"></span>• [--version](#page-76-7), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-76-1"></span>**Internationalization Options**

The following options change how the [mysqldump](#page-57-0) command represents character data with national language settings.

<span id="page-76-3"></span>• [--character-sets-dir=](#page-76-3)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-76-4"></span>• [--default-character-set=](#page-76-4)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |
| Default Value       | utf8                               |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration". If no character set is specified, [mysqldump](#page-57-0) uses utf8mb4.

<span id="page-76-5"></span>• [--no-set-names](#page-76-5), -N

| Command-Line Format | no-set-names |
|---------------------|--------------|
| Deprecated          | Yes          |

Turns off the [--set-charset](#page-77-6) setting, the same as specifying --skip-set-charset.

## <span id="page-77-6"></span>• [--set-charset](#page-77-6)

| Command-Line Format | set-charset      |
|---------------------|------------------|
| Disabled by         | skip-set-charset |

Write SET NAMES default\_character\_set to the output. This option is enabled by default. To suppress the SET NAMES statement, use [--skip-set-charset](#page-77-6).

# <span id="page-77-0"></span>**Replication Options**

The [mysqldump](#page-57-0) command is frequently used to create an empty instance, or an instance including data, on a replica server in a replication configuration. The following options apply to dumping and restoring data on replication source servers and replicas.

## <span id="page-77-1"></span>• [--apply-replica-statements](#page-77-1)

| Command-Line Format | apply-replica-statements |
|---------------------|--------------------------|
| Type                | Boolean                  |
| Default Value       | FALSE                    |

For a replica dump produced with the [--dump-replica](#page-77-5) option, this option adds a STOP REPLICA statement before the statement with the binary log coordinates, and a START REPLICA statement at the end of the output.

## <span id="page-77-2"></span>• [--apply-slave-statements](#page-77-2)

| Command-Line Format | apply-slave-statements |
|---------------------|------------------------|
| Deprecated          | Yes                    |
| Type                | Boolean                |
| Default Value       | FALSE                  |

This is a deprecated alias for [--apply-replica-statements](#page-77-1).

## <span id="page-77-4"></span>• [--delete-source-logs](#page-77-4)

| Command-Line Format | delete-source-logs |
|---------------------|--------------------|
|---------------------|--------------------|

On a replication source server, delete the binary logs by sending a PURGE BINARY LOGS statement to the server after performing the dump operation. The options require the RELOAD privilege as well as privileges sufficient to execute that statement. This option automatically enables [--source](#page-80-1)[data](#page-80-1).

## <span id="page-77-3"></span>• [--delete-master-logs](#page-77-3)

| Command-Line Format | delete-master-logs |
|---------------------|--------------------|
| Deprecated          | Yes                |

This is a deprecated alias for [--delete-source-logs](#page-77-4).

## <span id="page-77-5"></span>• [--dump-replica\[=](#page-77-5)value]

| Command-Line Format | dump-replica[=value] |
|---------------------|----------------------|
|---------------------|----------------------|

| Type          | Numeric |
|---------------|---------|
| Default Value | 1       |
| Valid Values  | 1       |
|               | 2       |

This option is similar to [--source-data](#page-80-1), except that it is used to dump a replica server to produce a dump file that can be used to set up another server as a replica that has the same source as the dumped server. The option causes the dump output to include a CHANGE REPLICATION SOURCE TO statement that indicates the binary log coordinates (file name and position) of the dumped replica's source. The CHANGE REPLICATION SOURCE TO statement reads the values of Relay\_Master\_Log\_File and Exec\_Master\_Log\_Pos from the SHOW REPLICA STATUS output and uses them for SOURCE\_LOG\_FILE and SOURCE\_LOG\_POS respectively. These are the replication source server coordinates from which the replica starts replicating.

![](_page_78_Picture_3.jpeg)

#### **Note**

Inconsistencies in the sequence of transactions from the relay log which have been executed can cause the wrong position to be used. See Section 19.5.1.34, "Replication and Transaction Inconsistencies" for more information.

--dump-replica causes the coordinates from the source to be used rather than those of the dumped server, as is done by the [--source-data](#page-80-1) option. In addition, specifying this option overrides the [--source-data](#page-80-1) option.

![](_page_78_Picture_7.jpeg)

#### **Warning**

--dump-replica should not be used if the server where the dump is going to be applied uses gtid\_mode=ON and SOURCE\_AUTO\_POSITION=1.

The option value is handled the same way as for [--source-data](#page-80-1). Setting no value or 1 causes a CHANGE REPLICATION SOURCE TO statement to be written to the dump. Setting 2 causes the statement to be written but encased in SQL comments. It has the same effect as --source-data in terms of enabling or disabling other options and in how locking is handled.

--dump-replica causes [mysqldump](#page-57-0) to stop the replication SQL thread before the dump and restart it again after.

--dump-replica sends a SHOW REPLICA STATUS statement to the server to obtain information, so they require privileges sufficient to execute that statement.

[--apply-replica-statements](#page-77-1) and [--include-source-host-port](#page-79-1) options can be used in conjunction with --dump-replica.

<span id="page-78-0"></span>• [--dump-slave\[=](#page-78-0)value]

| Command-Line Format | dump-slave[=value] |
|---------------------|--------------------|
| Deprecated          | Yes                |
| Type                | Numeric            |
| Default Value       | 1                  |
| Valid Values        | 1                  |
|                     | 2                  |

This is a deprecated alias for [--dump-replica](#page-77-5).

## <span id="page-79-1"></span>• [--include-source-host-port](#page-79-1)

| Command-Line Format | include-source-host-port |
|---------------------|--------------------------|
| Type                | Boolean                  |
| Default Value       | FALSE                    |

Adds the SOURCE\_HOST and SOURCE\_PORT options for the host name and TCP/IP port number of the replica's source, to the CHANGE REPLICATION SOURCE TO statement in a replica dump produced with the [--dump-replica](#page-77-5) option.

## <span id="page-79-0"></span>• [--include-master-host-port](#page-79-0)

| Command-Line Format | include-master-host-port |
|---------------------|--------------------------|
| Deprecated          | Yes                      |
| Type                | Boolean                  |
| Default Value       | FALSE                    |

This is a deprecated alias for [--include-source-host-port](#page-79-1).

## <span id="page-79-2"></span>• [--master-data\[=](#page-79-2)value]

| Command-Line Format | master-data[=value] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Numeric             |
| Default Value       | 1                   |
| Valid Values        | 1                   |
|                     | 2                   |

This is a deprecated alias for [--source-data](#page-80-1).

## <span id="page-79-3"></span>• [--output-as-version=](#page-79-3)value

| Command-Line Format | output-as-version=value |
|---------------------|-------------------------|
| Type                | Enumeration             |
| Default Value       | SERVER                  |
| Valid Values        | BEFORE_8_0_23           |
|                     | BEFORE_8_2_0            |

Determines the level of terminology used for statements relating to replicas and events, making it possible to create dumps compatible with older versions of MySQL that do not accept the newer terminology. This option can take any one of the following values, with effects described as listed here:

<sup>•</sup> SERVER: Reads the server version and uses the latest versions of statements compatible with that 450 version. This is the default value.

• BEFORE\_8\_0\_23: Replication SQL statements using deprecated terms such as "slave" and "master" are written to the output in place of those using "replica" and "source", as in MySQL versions prior to 8.0.23.

This option also duplicates the effects of BEFORE\_8\_2\_0 on the output of SHOW CREATE EVENT.

• BEFORE\_8\_2\_0: This option causes SHOW CREATE EVENT to reflect how the event would have been created in a MySQL server prior to version 8.2.0, displaying DISABLE ON SLAVE rather than DISABLE ON REPLICA.

This option affects the output from [--events](#page-86-3), [--dump-replica](#page-77-5), [--source-data](#page-80-1), [--apply](#page-77-1)[replica-statements](#page-77-1), and [--include-source-host-port](#page-79-1).

<span id="page-80-1"></span>• [--source-data\[=](#page-80-1)value]

| Command-Line Format | source-data[=value] |
|---------------------|---------------------|
| Type                | Numeric             |
| Default Value       | 1                   |
| Valid Values        | 1                   |
|                     | 2                   |

Used to dump a replication source server to produce a dump file that can be used to set up another server as a replica of the source. The options cause the dump output to include a CHANGE REPLICATION SOURCE TO statement that indicates the binary log coordinates (file name and position) of the dumped server. These are the replication source server coordinates from which the replica should start replicating after you load the dump file into the replica.

If the option value is 2, the CHANGE REPLICATION SOURCE TO statement is written as an SQL comment, and thus is informative only; it has no effect when the dump file is reloaded. If the option value is 1, the statement is not written as a comment and takes effect when the dump file is reloaded. If no option value is specified, the default value is 1.

--source-data sends a SHOW BINARY LOG STATUS statement to the server to obtain information, so they require privileges sufficient to execute that statement. This option also requires the RELOAD privilege and the binary log must be enabled.

--source-data automatically turns off [--lock-tables](#page-92-1). They also turn on [--lock-all](#page-92-0)[tables](#page-92-0), unless [--single-transaction](#page-93-2) also is specified, in which case, a global read lock is acquired only for a short time at the beginning of the dump (see the description for [--single](#page-93-2)[transaction](#page-93-2)). In all cases, any action on logs happens at the exact moment of the dump.

It is also possible to set up a replica by dumping an existing replica of the source, using the [--dump](#page-77-5)[replica](#page-77-5) option, which overrides --source-data causing it to be ignored.

<span id="page-80-0"></span>• [--set-gtid-purged=](#page-80-0)value

| Command-Line Format | set-gtid-purged=value |
|---------------------|-----------------------|
| Type                | Enumeration           |
| Default Value       | AUTO                  |
| Valid Values        | OFF                   |
|                     | ON                    |

AUTO

This option is for servers that use GTID-based replication (gtid\_mode=ON). It controls the inclusion of a SET @@GLOBAL.gtid\_purged statement in the dump output, which updates the value of gtid\_purged on a server where the dump file is reloaded, to add the GTID set from the source server's gtid\_executed system variable. gtid\_purged holds the GTIDs of all transactions that have been applied on the server, but do not exist on any binary log file on the server. [mysqldump](#page-57-0) therefore adds the GTIDs for the transactions that were executed on the source server, so that the target server records these transactions as applied, although it does not have them in its binary logs. --set-gtid-purged also controls the inclusion of a SET @@SESSION.sql\_log\_bin=0 statement, which disables binary logging while the dump file is being reloaded. This statement prevents new GTIDs from being generated and assigned to the transactions in the dump file as they are executed, so that the original GTIDs for the transactions are used.

If you do not set the --set-gtid-purged option, the default is that a SET @@GLOBAL.gtid\_purged statement is included in the dump output if GTIDs are enabled on the server you are backing up, and the set of GTIDs in the global value of the gtid\_executed system variable is not empty. A SET @@SESSION.sql\_log\_bin=0 statement is also included if GTIDs are enabled on the server.

You can either replace the value of gtid\_purged with a specified GTID set, or add a plus sign (+) to the statement to append a specified GTID set to the GTID set that is already held by gtid\_purged. The SET @@GLOBAL.gtid\_purged statement recorded by [mysqldump](#page-57-0) includes a plus sign (+) in a version-specific comment, such that MySQL adds the GTID set from the dump file to the existing gtid\_purged value.

It is important to note that the value that is included by [mysqldump](#page-57-0) for the SET @@GLOBAL.gtid\_purged statement includes the GTIDs of all transactions in the gtid\_executed set on the server, even those that changed suppressed parts of the database, or other databases on the server that were not included in a partial dump. This can mean that after the gtid\_purged value has been updated on the server where the dump file is replayed, GTIDs are present that do not relate to any data on the target server. If you do not replay any further dump files on the target server, the extraneous GTIDs do not cause any problems with the future operation of the server, but they make it harder to compare or reconcile GTID sets on different servers in the replication topology. If you do replay a further dump file on the target server that contains the same GTIDs (for example, another partial dump from the same origin server), any SET @@GLOBAL.gtid\_purged statement in the second dump file fails. In this case, either remove the statement manually before replaying the dump file, or output the dump file without the statement.

If the SET @@GLOBAL.gtid\_purged statement would not have the desired result on your target server, you can exclude the statement from the output, or include it but comment it out so that it is not actioned automatically. You can also include the statement but manually edit it in the dump file to achieve the desired result.

The possible values for the --set-gtid-purged option are as follows:

AUTO The default value. If GTIDs are enabled on the server you are backing up and gtid\_executed is not empty, SET @@GLOBAL.gtid\_purged is added to the output, containing the GTID set from gtid\_executed. If GTIDs are enabled, SET @@SESSION.sql\_log\_bin=0 is added to the output. If GTIDs are not enabled on the server, the statements are not added to the output.

OFF SET @@GLOBAL.gtid\_purged is not added to the output, and SET @@SESSION.sql\_log\_bin=0 is not added to the output. For a server where GTIDs are not in use, use this option or

AUTO. Only use this option for a server where GTIDs are in use if you are sure that the required GTID set is already present in gtid\_purged on the target server and should not be changed, or if you plan to identify and add any missing GTIDs manually.

ON If GTIDs are enabled on the server you are backing up, SET @@GLOBAL.gtid\_purged is added to the output (unless gtid\_executed is empty), and SET @@SESSION.sql\_log\_bin=0 is added to the output. An error occurs if you set this option but GTIDs are not enabled on the server. For a server where GTIDs are in use, use this option or AUTO, unless you are sure that the GTIDs in gtid\_executed are not needed on the target server.

COMMENTED If GTIDs are enabled on the server you are backing up, SET @@GLOBAL.gtid\_purged is added to the output (unless gtid\_executed is empty), but it is commented out. This means that the value of gtid\_executed is available in the output, but no action is taken automatically when the dump file is reloaded. SET @@SESSION.sql\_log\_bin=0 is added to the output, and it is not commented out. With COMMENTED, you can control the use of the gtid\_executed set manually or through automation. For example, you might prefer to do this if you are migrating data to another server that already has different active databases.

# <span id="page-82-0"></span>**Format Options**

The following options specify how to represent the entire dump file or certain kinds of data in the dump file. They also control whether certain optional information is written to the dump file.

<span id="page-82-1"></span>• [--compact](#page-82-1)

| Command-Line Format | compact |
|---------------------|---------|

Produce more compact output. This option enables the [--skip-add-drop-table](#page-73-0), [--skip-add](#page-91-3)[locks](#page-91-3), [--skip-comments](#page-75-4), [--skip-disable-keys](#page-89-3), and [--skip-set-charset](#page-77-6) options.

<span id="page-82-2"></span>• [--compatible=](#page-82-2)name

| Command-Line Format | compatible=name[,name,] |  |
|---------------------|-------------------------|--|
| Type                | String                  |  |
| Default Value       | ''                      |  |
| Valid Values        | ansi                    |  |

Produce output that is more compatible with other database systems or with older MySQL servers. The only permitted value for this option is ansi, which has the same meaning as the corresponding option for setting the server SQL mode. See Section 7.1.11, "Server SQL Modes".

<span id="page-82-3"></span>• [--complete-insert](#page-82-3), -c

| Command-Line Format | complete-insert |
|---------------------|-----------------|
|---------------------|-----------------|

453

<span id="page-82-4"></span>Use complete INSERT statements that include column names.

| Command-Line Format | create-options |
|---------------------|----------------|
|                     |                |

Include all MySQL-specific table options in the CREATE TABLE statements.

<span id="page-83-0"></span>• [--fields-terminated-by=...](#page-83-0), [--fields-enclosed-by=...](#page-83-0), [--fields-optionally](#page-83-0)[enclosed-by=...](#page-83-0), [--fields-escaped-by=...](#page-83-0)

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

These options are used with the [--tab](#page-84-3) option and have the same meaning as the corresponding FIELDS clauses for LOAD DATA. See Section 15.2.9, "LOAD DATA Statement".

<span id="page-83-1"></span>• [--hex-blob](#page-83-1)

| Command-Line Format | hex-blob |
|---------------------|----------|
|---------------------|----------|

Dump binary columns using hexadecimal notation (for example, 'abc' becomes 0x616263). The affected data types are BINARY, VARBINARY, BLOB types, BIT, all spatial data types, and other nonbinary data types when used with the binary character set.

The [--hex-blob](#page-83-1) option is ignored when the [--tab](#page-84-3) is used.

<span id="page-83-2"></span>• [--lines-terminated-by=...](#page-83-2)

| Command-Line Format | lines-terminated-by=string |
|---------------------|----------------------------|
| Type                | String                     |

This option is used with the [--tab](#page-84-3) option and has the same meaning as the corresponding LINES clause for LOAD DATA. See Section 15.2.9, "LOAD DATA Statement".

<span id="page-83-3"></span>454

• [--quote-names](#page-83-3), -Q

|  | Command-Line Format |  | quote-names |  |
|--|---------------------|--|-------------|--|
|--|---------------------|--|-------------|--|

enabled by default. It can be disabled with --skip-quote-names, but this option should be given after any option such as [--compatible](#page-82-2) that may enable [--quote-names](#page-83-3).

<span id="page-84-0"></span>• [--result-file=](#page-84-0)file\_name, -r file\_name

| Command-Line Format | result-file=file_name |
|---------------------|-----------------------|
| Type                | File name             |

Direct output to the named file. The result file is created and its previous contents overwritten, even if an error occurs while generating the dump.

This option should be used on Windows to prevent newline \n characters from being converted to \r\n carriage return/newline sequences.

<span id="page-84-1"></span>• [--show-create-skip-secondary-engine=](#page-84-1)value

| Command-Line Format | show-create-skip-secondary-engine |
|---------------------|-----------------------------------|
|---------------------|-----------------------------------|

Excludes the SECONDARY ENGINE clause from CREATE TABLE statements. It does so by enabling the [show\\_create\\_table\\_skip\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_show_create_table_skip_secondary_engine) system variable for the duration of the dump operation. Alternatively, you can enable the [show\\_create\\_table\\_skip\\_secondary\\_engine](https://dev.mysql.com/doc/heatwave/en/heatwave-system-variables.md#sysvar_show_create_table_skip_secondary_engine) system variable prior to using [mysqldump](#page-57-0).

<span id="page-84-3"></span>• --tab=[dir\\_name](#page-84-3), -T dir\_name

| Command-Line Format | tab=dir_name   |
|---------------------|----------------|
| Type                | Directory name |

Produce tab-separated text-format data files. For each dumped table, [mysqldump](#page-57-0) creates a tbl\_name.sql file that contains the CREATE TABLE statement that creates the table, and the server writes a tbl\_name.txt file that contains its data. The option value is the directory in which to write the files.

![](_page_84_Picture_12.jpeg)

## **Note**

This option should be used only when [mysqldump](#page-57-0) is run on the same machine as the mysqld server. Because the server creates \*.txt files in the directory that you specify, the directory must be writable by the server and the MySQL account that you use must have the FILE privilege. Because [mysqldump](#page-57-0) creates \*.sql in the same directory, it must be writable by your system login account.

By default, the .txt data files are formatted using tab characters between column values and a newline at the end of each line. The format can be specified explicitly using the --fields-xxx and [--lines-terminated-by](#page-83-2) options.

Column values are converted to the character set specified by the [--default-character-set](#page-76-4) option.

<span id="page-84-2"></span>• [--tz-utc](#page-84-2)

| Command-Line Format | tz-utc | 455 |
|---------------------|--------|-----|
|---------------------|--------|-----|

| Disabled by | skip-tz-utc |
|-------------|-------------|
|-------------|-------------|

This option enables TIMESTAMP columns to be dumped and reloaded between servers in different time zones. [mysqldump](#page-57-0) sets its connection time zone to UTC and adds SET TIME\_ZONE='+00:00' to the dump file. Without this option, TIMESTAMP columns are dumped and reloaded in the time zones local to the source and destination servers, which can cause the values to change if the servers are in different time zones. --tz-utc also protects against changes due to daylight saving time. --tz-utc is enabled by default. To disable it, use --skip-tz-utc.

<span id="page-85-0"></span>• [--xml](#page-85-0), -X

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

The output from the mysql client when run using the [--xml](#page-12-3) option also follows the preceding rules. (See Section 6.5.1.1, "mysql Client Options".)

XML output from [mysqldump](#page-57-0) includes the XML namespace, as shown here:

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
```

```
<field name="Name">Rafah</field>
<field name="CountryCode">PSE</field>
<field name="District">Rafah</field>
<field name="Population">92020</field>
</row>
</table_data>
</database>
</mysqldump>
```

# <span id="page-86-0"></span>**Filtering Options**

The following options control which kinds of schema objects are written to the dump file: by category, such as triggers or events; by name, for example, choosing which databases and tables to dump; or even filtering rows from the table data using a WHERE clause.

<span id="page-86-2"></span>• [--all-databases](#page-86-2), -A

| Command-Line Format | all-databases |
|---------------------|---------------|
|                     |               |

Dump all tables in all databases. This is the same as using the [--databases](#page-86-1) option and naming all the databases on the command line.

![](_page_86_Picture_7.jpeg)

## **Note**

See the [--add-drop-database](#page-72-1) description for information about an incompatibility of that option with [--all-databases](#page-86-2).

Prior to MySQL 8.4, the [--routines](#page-88-0) and [--events](#page-86-3) options for [mysqldump](#page-57-0) were not required to include stored routines and events when using the [--all-databases](#page-86-2) option: The dump included the mysql system database, and therefore also the mysql.proc and mysql.event tables containing stored routine and event definitions. As of MySQL 8.4, the mysql.event and mysql.proc tables are not used. Definitions for the corresponding objects are stored in data dictionary tables, but those tables are not dumped. To include stored routines and events in a dump made using [--all-databases](#page-86-2), use the [--routines](#page-88-0) and [--events](#page-86-3) options explicitly.

<span id="page-86-1"></span>• [--databases](#page-86-1), -B

| Command-Line Format | databases |
|---------------------|-----------|
|---------------------|-----------|

Dump several databases. Normally, [mysqldump](#page-57-0) treats the first name argument on the command line as a database name and following names as table names. With this option, it treats all name arguments as database names. CREATE DATABASE and USE statements are included in the output before each new database.

This option may be used to dump the performance\_schema database, which normally is not dumped even with the [--all-databases](#page-86-2) option. (Also use the [--skip-lock-tables](#page-92-1) option.)

![](_page_86_Picture_15.jpeg)

# **Note**

See the [--add-drop-database](#page-72-1) description for information about an incompatibility of that option with [--databases](#page-86-1).

<span id="page-86-3"></span>• [--events](#page-86-3), -E

| Command-Line Format | events |
|---------------------|--------|
|---------------------|--------|

457

The output generated by using --events contains CREATE EVENT statements to create the events.

<span id="page-87-0"></span>• --ignore-error=[error\[,error\]...](#page-87-0)

| Command-Line Format | ignore-error=error[,error] |
|---------------------|----------------------------|
| Type                | String                     |

Ignore the specified errors. The option value is a list of comma-separated error numbers specifying the errors to ignore during [mysqldump](#page-57-0) execution. If the [--force](#page-75-2) option is also given to ignore all errors, [--force](#page-75-2) takes precedence.

<span id="page-87-1"></span>• --ignore-table=[db\\_name.tbl\\_name](#page-87-1)

| Command-Line Format | ignore-table=db_name.tbl_name |
|---------------------|-------------------------------|
| Type                | String                        |

Do not dump the given table, which must be specified using both the database and table names. To ignore multiple tables, use this option multiple times. This option also can be used to ignore views.

<span id="page-87-2"></span>• [--ignore-views=](#page-87-2)boolean

| Command-Line Format | ignore-views |
|---------------------|--------------|
| Type                | Boolean      |
| Default Value       | FALSE        |

Skips table views in the dump file.

<span id="page-87-3"></span>• [--init-command=](#page-87-3)str

| Command-Line Format | init-command=str |
|---------------------|------------------|
| Type                | String           |

Single SQL statement to execute after connecting to the MySQL server. The definition resets existing statements defined by it or [init-command-add](#page-87-4).

<span id="page-87-4"></span>• [--init-command-add=](#page-87-4)str

| Command-Line Format | init-command-add=str |
|---------------------|----------------------|
| Type                | String               |

Add an additional SQL statement to execute after connecting or reconnecting to the MySQL server. It's usable without [--init-command](#page-87-3) but has no effect if used before it because [init-command](#page-87-3) resets the list of commands to call.

<span id="page-87-5"></span>• [--no-data](#page-87-5), -d

| Command-Line Format | no-data |
|---------------------|---------|

Do not write any table row information (that is, do not dump table contents). This is useful if you want to dump only the CREATE TABLE statement for the table (for example, to create an empty copy of the table by loading the dump file).

<span id="page-88-0"></span>• [--routines](#page-88-0), -R

| Command-Line Format | routines |
|---------------------|----------|
|---------------------|----------|

Include stored routines (procedures and functions) for the dumped databases in the output. This option requires the global SELECT privilege.

The output generated by using --routines contains CREATE PROCEDURE and CREATE FUNCTION statements to create the routines.

<span id="page-88-1"></span>• [--skip-generated-invisible-primary-key](#page-88-1)

| Command-Line Format | skip-generated-invisible-primary<br>key |
|---------------------|-----------------------------------------|
| Type                | Boolean                                 |
| Default Value       | FALSE                                   |

This option causes generated invisible primary keys to be excluded from the output. For more information, see Section 15.1.20.11, "Generated Invisible Primary Keys".

<span id="page-88-3"></span>• [--tables](#page-88-3)

| Command-Line Format | tables |
|---------------------|--------|
|---------------------|--------|

Override the [--databases](#page-86-1) or -B option. [mysqldump](#page-57-0) regards all name arguments following the option as table names.

<span id="page-88-2"></span>• [--triggers](#page-88-2)

| Command-Line Format | triggers      |
|---------------------|---------------|
| Disabled by         | skip-triggers |

Include triggers for each dumped table in the output. This option is enabled by default; disable it with --skip-triggers.

To be able to dump a table's triggers, you must have the TRIGGER privilege for the table.

Multiple triggers are permitted. [mysqldump](#page-57-0) dumps triggers in activation order so that when the dump file is reloaded, triggers are created in the same activation order. However, if a [mysqldump](#page-57-0) dump file contains multiple triggers for a table that have the same trigger event and action time, an error occurs for attempts to load the dump file into an older server that does not support multiple triggers. (For a workaround, see [Downgrade Notes](https://dev.mysql.com/doc/refman/5.7/en/downgrading-to-previous-series.md); you can convert triggers to be compatible with older servers.)

<span id="page-88-4"></span>• --where='[where\\_condition](#page-88-4)', -w 'where\_condition'

| Command-Line Format | where='where_condition' |
|---------------------|-------------------------|
|---------------------|-------------------------|

Dump only rows selected by the given WHERE condition. Quotes around the condition are mandatory if it contains spaces or other characters that are special to your command interpreter.

## Examples:

```
--where="user='jimf'"
-w"userid>1"
```

-w"userid<1"

# <span id="page-89-0"></span>**Performance Options**

The following options are the most relevant for the performance particularly of the restore operations. For large data sets, restore operation (processing the INSERT statements in the dump file) is the most time-consuming part. When it is urgent to restore data quickly, plan and test the performance of this stage in advance. For restore times measured in hours, you might prefer an alternative backup and restore solution, such as MySQL Enterprise Backup for InnoDB-only and mixed-use databases.

Performance is also affected by the [transactional options](#page-91-0), primarily for the dump operation.

<span id="page-89-2"></span>• [--column-statistics](#page-89-2)

| Command-Line Format | column-statistics |
|---------------------|-------------------|
| Type                | Boolean           |
| Default Value       | OFF               |

Add ANALYZE TABLE statements to the output to generate histogram statistics for dumped tables when the dump file is reloaded. This option is disabled by default because histogram generation for large tables can take a long time.

<span id="page-89-3"></span>• [--disable-keys](#page-89-3), -K

| Command-Line Format | disable-keys |  |
|---------------------|--------------|--|
|---------------------|--------------|--|

For each table, surround the INSERT statements with /\*!40000 ALTER TABLE tbl\_name DISABLE KEYS \*/; and /\*!40000 ALTER TABLE tbl\_name ENABLE KEYS \*/; statements. This makes loading the dump file faster because the indexes are created after all rows are inserted. This option is effective only for nonunique indexes of MyISAM tables.

<span id="page-89-1"></span>• [--extended-insert](#page-89-1), -e

| Command-Line Format | extended-insert      |
|---------------------|----------------------|
| Disabled by         | skip-extended-insert |

Write INSERT statements using multiple-row syntax that includes several VALUES lists. This results in a smaller dump file and speeds up inserts when the file is reloaded.

<span id="page-89-4"></span>• [--insert-ignore](#page-89-4)

| Command-Line Format | insert-ignore |
|---------------------|---------------|
|---------------------|---------------|

Write INSERT IGNORE statements rather than INSERT statements.

<span id="page-89-5"></span>• [--max-allowed-packet=](#page-89-5)value

| Command-Line Format | max-allowed-packet=value |
|---------------------|--------------------------|
| Type                | Numeric                  |
| Default Value       | 25165824                 |

The maximum size of the buffer for client/server communication. The default is 24MB, the maximum 460 is 1GB.

![](_page_90_Picture_1.jpeg)

#### **Note**

The value of this option is specific to [mysqldump](#page-57-0) and should not be confused with the MySQL server's max\_allowed\_packet system variable; the server value cannot be exceeded by a single packet from [mysqldump](#page-57-0), regardless of any setting for the [mysqldump](#page-57-0) option, even if the latter is larger.

<span id="page-90-1"></span>• [--mysqld-long-query-time=](#page-90-1)value

| Command-Line Format | mysqld-long-query-time=value |
|---------------------|------------------------------|
| Type                | Numeric                      |
| Default Value       | Server global setting        |

Set the session value of the long\_query\_time system variable. Use this option if you want to increase the time allowed for queries from [mysqldump](#page-57-0) before they are logged to the slow query log file. [mysqldump](#page-57-0) performs a full table scan, which means its queries can often exceed a global long\_query\_time setting that is useful for regular queries. The default global setting is 10 seconds.

You can use [--mysqld-long-query-time](#page-90-1) to specify a session value from 0 (meaning that every query from [mysqldump](#page-57-0) is logged to the slow query log) to 31536000, which is 365 days in seconds. For [mysqldump](#page-57-0)'s option, you can only specify whole seconds. When you do not specify this option, the server's global setting applies to [mysqldump](#page-57-0)'s queries.

<span id="page-90-2"></span>• [--net-buffer-length=](#page-90-2)value

| Command-Line Format | net-buffer-length=value |
|---------------------|-------------------------|
| Type                | Numeric                 |
| Default Value       | 16384                   |

The initial size of the buffer for client/server communication. When creating multiple-row INSERT statements (as with the [--extended-insert](#page-89-1) or [--opt](#page-90-0) option), [mysqldump](#page-57-0) creates rows up to [--net-buffer-length](#page-90-2) bytes long. If you increase this variable, ensure that the MySQL server net\_buffer\_length system variable has a value at least this large.

<span id="page-90-3"></span>• [--network-timeout](#page-90-3), -M

| Command-Line Format | network-timeout[={0 1}] |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | TRUE                    |

Enable large tables to be dumped by setting [--max-allowed-packet](#page-89-5) to its maximum value and network read and write timeouts to a large value. This option is enabled by default. To disable it, use [--skip-network-timeout](#page-90-3).

<span id="page-90-0"></span>• [--opt](#page-90-0)

| Command-Line Format | opt      |
|---------------------|----------|
| Disabled by         | skip-opt |

461

[--set-charset](#page-77-6). It gives a fast dump operation and produces a dump file that can be reloaded into a MySQL server quickly.

Because the --opt option is enabled by default, you only specify its converse, the [--skip-opt](#page-91-2) to turn off several default settings. See the discussion of mysqldump [option groups](#page-93-0) for information about selectively enabling or disabling a subset of the options affected by --opt.

<span id="page-91-1"></span>• [--quick](#page-91-1), -q

| Command-Line Format | quick      |
|---------------------|------------|
| Disabled by         | skip-quick |

This option is useful for dumping large tables. It forces [mysqldump](#page-57-0) to retrieve rows for a table from the server a row at a time rather than retrieving the entire row set and buffering it in memory before writing it out.

<span id="page-91-2"></span>• [--skip-opt](#page-91-2)

| Command-Line Format | skip-opt |
|---------------------|----------|
|---------------------|----------|

See the description for the [--opt](#page-90-0) option.

# <span id="page-91-0"></span>**Transactional Options**

The following options trade off the performance of the dump operation, against the reliability and consistency of the exported data.

<span id="page-91-3"></span>• [--add-locks](#page-91-3)

| Command-Line Format | add-locks |
|---------------------|-----------|
|---------------------|-----------|

Surround each table dump with LOCK TABLES and UNLOCK TABLES statements. This results in faster inserts when the dump file is reloaded. See Section 10.2.5.1, "Optimizing INSERT Statements".

<span id="page-91-4"></span>• [--flush-logs](#page-91-4), -F

| Command-Line Format | flush-logs |
|---------------------|------------|
|                     |            |

Flush the MySQL server log files before starting the dump. This option requires the RELOAD privilege. If you use this option in combination with the [--all-databases](#page-86-2) option, the logs are flushed for each database dumped. The exception is when using [--lock-all-tables](#page-92-0), [-](#page-80-1) [source-data](#page-80-1), or [--single-transaction](#page-93-2). In these cases, the logs are flushed only once, corresponding to the moment that all tables are locked by FLUSH TABLES WITH READ LOCK. If you want your dump and the log flush to happen at exactly the same moment, you should use --flush-logs together with [--lock-all-tables](#page-92-0), [--source-data](#page-80-1), or [--single](#page-93-2)[transaction](#page-93-2).

<span id="page-91-5"></span>• [--flush-privileges](#page-91-5)

| Command-Line Format | flush-privileges |
|---------------------|------------------|

Add a FLUSH PRIVILEGES statement to the dump output after dumping the mysql database. This option should be used any time the dump contains the mysql database and any other database that depends on the data in the mysql database for proper restoration.

Because the dump file contains a FLUSH PRIVILEGES statement, reloading the file requires privileges sufficient to execute that statement.

<span id="page-92-0"></span>• [--lock-all-tables](#page-92-0), -x

| Command-Line Format | lock-all-tables |
|---------------------|-----------------|
|---------------------|-----------------|

Lock all tables across all databases. This is achieved by acquiring a global read lock for the duration of the whole dump. This option automatically turns off [--single-transaction](#page-93-2) and [--lock](#page-92-1)[tables](#page-92-1).

<span id="page-92-1"></span>• [--lock-tables](#page-92-1), -l

| Command-Line Format | lock-tables |
|---------------------|-------------|
|                     |             |

For each dumped database, lock all tables to be dumped before dumping them. The tables are locked with READ LOCAL to permit concurrent inserts in the case of MyISAM tables. For transactional tables such as InnoDB, [--single-transaction](#page-93-2) is a much better option than --lock-tables because it does not need to lock the tables at all.

Because --lock-tables locks tables for each database separately, this option does not guarantee that the tables in the dump file are logically consistent between databases. Tables in different databases may be dumped in completely different states.

Some options, such as [--opt](#page-90-0), automatically enable --lock-tables. If you want to override this, use --skip-lock-tables at the end of the option list.

<span id="page-92-2"></span>• [--no-autocommit](#page-92-2)

| Command-Line Format | no-autocommit |
|---------------------|---------------|

Enclose the INSERT statements for each dumped table within SET autocommit = 0 and COMMIT statements.

<span id="page-92-3"></span>• [--order-by-primary](#page-92-3)

| Command-Line Format | order-by-primary |
|---------------------|------------------|
|---------------------|------------------|

Dump each table's rows sorted by its primary key, or by its first unique index, if such an index exists. This is useful when dumping a MyISAM table to be loaded into an InnoDB table, but makes the dump operation take considerably longer.

<span id="page-92-4"></span>• [--shared-memory-base-name=](#page-92-4)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive. 463

This option applies only if the server was started with the shared\_memory system variable enabled

<span id="page-93-2"></span>• [--single-transaction](#page-93-2)

| Command-Line Format | single-transaction |
|---------------------|--------------------|
|---------------------|--------------------|

This option sets the transaction isolation mode to REPEATABLE READ and sends a START TRANSACTION SQL statement to the server before dumping data. It is useful only with transactional tables such as InnoDB, because then it dumps the consistent state of the database at the time when START TRANSACTION was issued without blocking any applications.

The RELOAD or FLUSH\_TABLES privilege is required with [--single-transaction](#page-93-2) if both gtid\_mode=ON and gtid\_purged=ON|AUTO.

When using this option, you should keep in mind that only InnoDB tables are dumped in a consistent state. For example, any MyISAM or MEMORY tables dumped while using this option may still change state.

While a [--single-transaction](#page-93-2) dump is in process, to ensure a valid dump file (correct table contents and binary log coordinates), no other connection should use the following statements: ALTER TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE. A consistent read is not isolated from those statements, so use of them on a table to be dumped can cause the SELECT that is performed by [mysqldump](#page-57-0) to retrieve the table contents to obtain incorrect contents or fail.

The --single-transaction option and the [--lock-tables](#page-92-1) option are mutually exclusive because LOCK TABLES causes any pending transactions to be committed implicitly.

To dump large tables, combine the --single-transaction option with the [--quick](#page-91-1) option.

# <span id="page-93-0"></span>**Option Groups**

- The [--opt](#page-90-0) option turns on several settings that work together to perform a fast dump operation. All of these settings are on by default, because --opt is on by default. Thus you rarely if ever specify --opt. Instead, you can turn these settings off as a group by specifying --skip-opt, then optionally re-enable certain settings by specifying the associated options later on the command line.
- The [--compact](#page-82-1) option turns off several settings that control whether optional statements and comments appear in the output. Again, you can follow this option with other options that re-enable certain settings, or turn all the settings on by using the --skip-compact form.

When you selectively enable or disable the effect of a group option, order is important because options are processed first to last. For example, [--disable-keys](#page-89-3) [--lock-tables](#page-92-1) [--skip-opt](#page-91-2) would not have the intended effect; it is the same as [--skip-opt](#page-91-2) by itself.

# <span id="page-93-1"></span>**Examples**

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

[mysqldump](#page-57-0) is also very useful for populating databases by copying data from one MySQL server to another:

```
mysqldump --opt db_name | mysql --host=remote_host -C db_name
```

You can dump several databases with one command:

```
mysqldump --databases db_name1 [db_name2 ...] > my_databases.sql
```

To dump all databases, use the [--all-databases](#page-86-2) option:

```
mysqldump --all-databases > all_databases.sql
```

For InnoDB tables, [mysqldump](#page-57-0) provides a way of making an online backup:

```
mysqldump --all-databases --source-data --single-transaction > all_databases.sql
```

This backup acquires a global read lock on all tables (using FLUSH TABLES WITH READ LOCK) at the beginning of the dump. As soon as this lock has been acquired, the binary log coordinates are read and the lock is released. If long updating statements are running when the FLUSH statement is issued, the MySQL server may get stalled until those statements finish. After that, the dump becomes lock free and does not disturb reads and writes on the tables. If the update statements that the MySQL server receives are short (in terms of execution time), the initial lock period should not be noticeable, even with many updates.

For point-in-time recovery (also known as "roll-forward," when you need to restore an old backup and replay the changes that happened since that backup), it is often useful to rotate the binary log (see Section 7.4.4, "The Binary Log") or at least know the binary log coordinates to which the dump corresponds:

```
mysqldump --all-databases --source-data=2 > all_databases.sql
```

Or:

```
mysqldump --all-databases --flush-logs --source-data=2 > all_databases.sql
```

The [--source-data](#page-80-1) option can be used simultaneously with the [--single-transaction](#page-93-2) option, which provides a convenient way to make an online backup suitable for use prior to point-in-time recovery if tables are stored using the InnoDB storage engine.

For more information on making backups, see Section 9.2, "Database Backup Methods", and Section 9.3, "Example Backup and Recovery Strategy".

- To select the effect of [--opt](#page-90-0) except for some features, use the --skip option for each feature. To disable extended inserts and memory buffering, use [--opt](#page-90-0) [--skip-extended-insert](#page-89-1) [--skip](#page-91-1)[quick](#page-91-1). (Actually, [--skip-extended-insert](#page-89-1) [--skip-quick](#page-91-1) is sufficient because [--opt](#page-90-0) is on by default.)
- To reverse [--opt](#page-90-0) for all features except disabling of indexes and table locking, use [--skip-opt](#page-91-2) [-](#page-89-3) [disable-keys](#page-89-3) [--lock-tables](#page-92-1).

# <span id="page-94-0"></span>**Restrictions**

[mysqldump](#page-57-0) does not dump the performance\_schema or sys schema by default. To dump any of these, name them explicitly on the command line. You can also name them with the [--databases](#page-86-1) option. For performance\_schema, also use the [--skip-lock-tables](#page-92-1) option.

[mysqldump](#page-57-0) does not dump the INFORMATION\_SCHEMA schema.

[mysqldump](#page-57-0) does not dump InnoDB CREATE TABLESPACE statements.

[mysqldump](#page-57-0) does not dump the NDB Cluster ndbinfo information database.

[mysqldump](#page-57-0) includes statements to recreate the general\_log and slow\_query\_log tables for dumps of the mysql database. Log table contents are not dumped.

If you encounter problems backing up views due to insufficient privileges, see Section 27.9, "Restrictions on Views" for a workaround.

# <span id="page-94-1"></span>**6.5.5 mysqlimport — A Data Import Program**

The [mysqlimport](#page-94-1) client provides a command-line interface to the LOAD DATA SQL statement. Most options to [mysqlimport](#page-94-1) correspond directly to clauses of LOAD DATA syntax. See Section 15.2.9, "LOAD DATA Statement".

Invoke [mysqlimport](#page-94-1) like this:

```
mysqlimport [options] db_name textfile1 [textfile2 ...]
```

For each text file named on the command line, [mysqlimport](#page-94-1) strips any extension from the file name and uses the result to determine the name of the table into which to import the file's contents. For example, files named patient.txt, patient.text, and patient all would be imported into a table named patient.

[mysqlimport](#page-94-1) supports the following options, which can be specified on the command line or in the [mysqlimport] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.14 mysqlimport Options**

| Option Name                   | Description                                                                   |
|-------------------------------|-------------------------------------------------------------------------------|
| bind-address                  | Use specified network interface to connect to<br>MySQL Server                 |
| character-sets-dir            | Directory where character sets can be found                                   |
| columns                       | This option takes a comma-separated list of<br>column names as its value      |
| compress                      | Compress all information sent between client and<br>server                    |
| compression-algorithms        | Permitted compression algorithms for connections<br>to server                 |
| debug                         | Write debugging log                                                           |
| debug-check                   | Print debugging information when program exits                                |
| debug-info                    | Print debugging information, memory, and CPU<br>statistics when program exits |
| default-auth                  | Authentication plugin to use                                                  |
| default-character-set         | Specify default character set                                                 |
| defaults-extra-file           | Read named option file in addition to usual option<br>files                   |
| defaults-file                 | Read only named option file                                                   |
| defaults-group-suffix         | Option group suffix value                                                     |
| delete                        | Empty the table before importing the text file                                |
| enable-cleartext-plugin       | Enable cleartext authentication plugin                                        |
| fields-enclosed-by            | This option has the same meaning as the<br>corresponding clause for LOAD DATA |
| fields-escaped-by             | This option has the same meaning as the<br>corresponding clause for LOAD DATA |
| fields-optionally-enclosed-by | This option has the same meaning as the<br>corresponding clause for LOAD DATA |
| fields-terminated-by          | This option has the same meaning as the<br>corresponding clause for LOAD DATA |
| force                         | Continue even if an SQL error occurs                                          |
| get-server-public-key         | Request RSA public key from server                                            |
| help                          | Display help message and exit                                                 |

| Option Name             | Description                                                                                                         |
|-------------------------|---------------------------------------------------------------------------------------------------------------------|
| host                    | Host on which MySQL server is located                                                                               |
| ignore                  | See the description for thereplace option                                                                           |
| ignore-lines            | Ignore the first N lines of the data file                                                                           |
| lines-terminated-by     | This option has the same meaning as the<br>corresponding clause for LOAD DATA                                       |
| local                   | Read input files locally from the client host                                                                       |
| lock-tables             | Lock all tables for writing before processing any<br>text files                                                     |
| login-path              | Read login path options from .mylogin.cnf                                                                           |
| low-priority            | Use LOW_PRIORITY when loading the table                                                                             |
| no-defaults             | Read no option files                                                                                                |
| no-login-paths          | Do not read login paths from the login path file                                                                    |
| password                | Password to use when connecting to server                                                                           |
| password1               | First multifactor authentication password to use<br>when connecting to server                                       |
| password2               | Second multifactor authentication password to use<br>when connecting to server                                      |
| password3               | Third multifactor authentication password to use<br>when connecting to server                                       |
| pipe                    | Connect to server using named pipe (Windows<br>only)                                                                |
| plugin-dir              | Directory where plugins are installed                                                                               |
| port                    | TCP/IP port number for connection                                                                                   |
| print-defaults          | Print default options                                                                                               |
| protocol                | Transport protocol to use                                                                                           |
| replace                 | Thereplace andignore options control<br>handling of input rows that duplicate existing rows<br>on unique key values |
| server-public-key-path  | Path name to file containing RSA public key                                                                         |
| shared-memory-base-name | Shared-memory name for shared-memory<br>connections (Windows only)                                                  |
| silent                  | Produce output only when errors occur                                                                               |
| socket                  | Unix socket file or Windows named pipe to use                                                                       |
| ssl-ca                  | File that contains list of trusted SSL Certificate<br>Authorities                                                   |
| ssl-capath              | Directory that contains trusted SSL Certificate<br>Authority certificate files                                      |
| ssl-cert                | File that contains X.509 certificate                                                                                |
| ssl-cipher              | Permissible ciphers for connection encryption                                                                       |
| ssl-crl                 | File that contains certificate revocation lists                                                                     |
| ssl-crlpath             | Directory that contains certificate revocation-list<br>files                                                        |
| ssl-fips-mode           | Whether to enable FIPS mode on client side                                                                          |
| ssl-key                 | File that contains X.509 key                                                                                        |

| Option Name                               | Description                                                              |
|-------------------------------------------|--------------------------------------------------------------------------|
| ssl-mode                                  | Desired security state of connection to server                           |
| ssl-session-data                          | File that contains SSL session data                                      |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails               |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections            |
| tls-sni-servername                        | Server name supplied by the client                                       |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                   |
| use-threads                               | Number of threads for parallel file-loading                              |
| user                                      | MySQL user name to use when connecting to<br>server                      |
| verbose                                   | Verbose mode                                                             |
| version                                   | Display version information and exit                                     |
| zstd-compression-level                    | Compression level for connections to server that<br>use zstd compression |

## <span id="page-97-4"></span>• [--help](#page-97-4), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

#### Display a help message and exit.

<span id="page-97-0"></span>• [--bind-address=](#page-97-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|                     |                         |

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-97-1"></span>• [--character-sets-dir=](#page-97-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-97-2"></span>• --columns=[column\\_list](#page-97-2), -c column\_list

| Command-Line Format | columns=column_list |
|---------------------|---------------------|
|---------------------|---------------------|

This option takes a list of comma-separated column names as its value. The order of the column names indicates how to match data file columns with table columns.

<span id="page-97-3"></span>• [--compress](#page-97-3), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |

| Type          | Boolean |
|---------------|---------|
| Default Value | OFF     |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-98-0"></span>• [--compression-algorithms=](#page-98-0)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-98-1"></span>• --debug[=[debug\\_options](#page-98-1)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-98-2"></span>• [--debug-check](#page-98-2)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-98-3"></span>• [--debug-info](#page-98-3)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |

| Default Value | FALSE |
|---------------|-------|
|---------------|-------|

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-99-1"></span>• [--default-character-set=](#page-99-1)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

<span id="page-99-0"></span>• [--default-auth=](#page-99-0)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-99-2"></span>• [--defaults-extra-file=](#page-99-2)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-99-3"></span>• [--defaults-file=](#page-99-3)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-99-4"></span>470

• [--defaults-group-suffix=](#page-99-4)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
|---------------------|---------------------------|

| Type | String |
|------|--------|
|------|--------|

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlimport](#page-94-1) normally reads the [client] and [mysqlimport] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-99-4), [mysqlimport](#page-94-1) also reads the [client\_other] and [mysqlimport\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-100-0"></span>• [--delete](#page-100-0), -D

| Command-Line Format | delete |
|---------------------|--------|
|                     |        |

Empty the table before importing the text file.

<span id="page-100-1"></span>• [--enable-cleartext-plugin](#page-100-1)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-100-2"></span>• [--fields-terminated-by=...](#page-100-2), [--fields-enclosed-by=...](#page-100-2), [--fields-optionally](#page-100-2)[enclosed-by=...](#page-100-2), [--fields-escaped-by=...](#page-100-2)

| Command-Line Format | fields-terminated-by=string |
|---------------------|-----------------------------|
| Type                | String                      |

| Command-Line Format | fields-enclosed-by=string |
|---------------------|---------------------------|
| Type                | String                    |

| Command-Line Format | fields-optionally-enclosed |
|---------------------|----------------------------|
|                     | by=string                  |
| Type                | String                     |

| Command-Line Format | fields-escaped-by |
|---------------------|-------------------|
| Type                | String            |

<span id="page-101-0"></span>• [--force](#page-101-0), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Ignore errors. For example, if a table for a text file does not exist, continue processing any remaining files. Without [--force](#page-101-0), [mysqlimport](#page-94-1) exits if a table does not exist.

<span id="page-101-1"></span>• [--get-server-public-key](#page-101-1)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-105-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-101-1).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-101-2"></span>• --host=[host\\_name](#page-101-2), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Import data to the MySQL server on the given host. The default host is localhost.

<span id="page-101-3"></span>• [--ignore](#page-101-3), -i

| Command-Line Format | ignore |
|---------------------|--------|
|---------------------|--------|

See the description for the [--replace](#page-105-0) option.

<span id="page-101-4"></span>• [--ignore-lines=](#page-101-4)N

| Command-Line Format | ignore-lines=# |
|---------------------|----------------|
| Type                | Numeric        |

Ignore the first N lines of the data file.

<span id="page-101-5"></span>• [--lines-terminated-by=...](#page-101-5)

| Command-Line Format | lines-terminated-by=string |
|---------------------|----------------------------|
| Type                | String                     |

This option has the same meaning as the corresponding clause for LOAD DATA. For example, to import Windows files that have lines terminated with carriage return/linefeed pairs, use [--lines-](#page-101-5) [terminated-by="\r\n"](#page-101-5). (You might have to double the backslashes, depending on the escaping conventions of your command interpreter.) See Section 15.2.9, "LOAD DATA Statement".

<span id="page-102-0"></span>• [--local](#page-102-0), -L

| Command-Line Format | local   |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

By default, files are read by the server on the server host. With this option, [mysqlimport](#page-94-1) reads input files locally on the client host.

Successful use of LOCAL load operations within [mysqlimport](#page-94-1) also requires that the server permits local loading; see Section 8.1.6, "Security Considerations for LOAD DATA LOCAL"

<span id="page-102-1"></span>• [--lock-tables](#page-92-1), -l

| Command-Line Format | lock-tables |
|---------------------|-------------|
|---------------------|-------------|

Lock all tables for writing before processing any text files. This ensures that all tables are synchronized on the server.

<span id="page-102-2"></span>• [--login-path=](#page-102-2)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-102-4"></span>• [--no-login-paths](#page-102-4)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

See [--login-path](#page-102-2) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-102-3"></span>• [--low-priority](#page-102-3)

| Command-Line Format | low-priority | 473 |  |
|---------------------|--------------|-----|--|

Use LOW\_PRIORITY when loading the table. This affects only storage engines that use only table-

<span id="page-103-0"></span>• [--no-defaults](#page-103-0)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-103-0) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-103-0) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-103-1"></span>• [--password\[=](#page-103-1)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlimport](#page-94-1) prompts for one. If given, there must be no space between [-](#page-103-1) [password=](#page-103-1) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlimport](#page-94-1) should not prompt for one, use the [--skip-password](#page-103-1) option.

<span id="page-103-2"></span>• [--password1\[=](#page-103-2)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlimport](#page-94-1) prompts for one. If given, there must be no space between [--password1=](#page-103-2) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlimport](#page-94-1) should not prompt for one, use the [--skip-password1](#page-103-2) option.

[--password1](#page-103-2) and [--password](#page-103-1) are synonymous, as are [--skip-password1](#page-103-2) and [--skip](#page-103-1)[password](#page-103-1).

<span id="page-103-3"></span>• [--password2\[=](#page-103-3)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-103-2); see the description of that option for details.

## <span id="page-104-0"></span>• [--password3\[=](#page-104-0)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-103-2); see the description of that option for details.

## <span id="page-104-1"></span>• [--pipe](#page-104-1), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

## <span id="page-104-2"></span>• [--plugin-dir=](#page-104-2)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-99-0) option is used to specify an authentication plugin but [mysqlimport](#page-94-1) does not find it. See Section 8.2.17, "Pluggable Authentication".

## <span id="page-104-3"></span>• --port=[port\\_num](#page-104-3), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

## <span id="page-104-4"></span>• [--print-defaults](#page-104-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-104-5"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-104-5)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-105-0"></span>• [--replace](#page-105-0), -r

| Command-Line Format | replace |
|---------------------|---------|
|---------------------|---------|

The [--replace](#page-105-0) and [--ignore](#page-101-3) options control handling of input rows that duplicate existing rows on unique key values. If you specify [--replace](#page-105-0), new rows replace existing rows that have the same unique key value. If you specify [--ignore](#page-101-3), input rows that duplicate an existing row on a unique key value are skipped. If you do not specify either option, an error occurs when a duplicate key value is found, and the rest of the text file is ignored.

<span id="page-105-1"></span>• [--server-public-key-path=](#page-105-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-105-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-101-1).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-105-2"></span>• [--shared-memory-base-name=](#page-105-2)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-105-3"></span>• [--silent](#page-105-3), -s

| Command-Line Format | silent |
|---------------------|--------|
|                     |        |

<span id="page-106-0"></span>• [--socket=](#page-106-0)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-106-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-106-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-106-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-106-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-106-2) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_106_Picture_14.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-106-2) is OFF. In this case, setting [--ssl-fips-mode](#page-106-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-106-3"></span>• [--tls-ciphersuites=](#page-106-3)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list477 |
|---------------------|--------------------------------------|

| Type<br>String |
|----------------|
|----------------|

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-107-0"></span>• [--tls-sni-servername=](#page-107-0)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-107-1"></span>• [--tls-version=](#page-107-1)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-107-3"></span>• --user=[user\\_name](#page-107-3), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

The user name of the MySQL account to use for connecting to the server.

<span id="page-107-2"></span>• [--use-threads=](#page-107-2)N

| Command-Line Format | use-threads=# |
|---------------------|---------------|
| Type                | Numeric       |

Load files in parallel using N threads.

<span id="page-107-4"></span>• [--verbose](#page-107-4), -v

| Command-Line Format | verbose |
|---------------------|---------|
|                     |         |

Verbose mode. Print more information about what the program does.

<span id="page-108-0"></span>• [--version](#page-108-0), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-108-1"></span>• [--zstd-compression-level=](#page-108-1)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

Here is a sample session that demonstrates use of [mysqlimport](#page-94-1):

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

# <span id="page-108-2"></span>**6.5.6 mysqlshow — Display Database, Table, and Column Information**

The [mysqlshow](#page-108-2) client can be used to quickly see which databases exist, their tables, or a table's columns or indexes.

[mysqlshow](#page-108-2) provides a command-line interface to several SQL SHOW statements. See Section 15.7.7, "SHOW Statements". The same information can be obtained by using those statements directly. For example, you can issue them from the mysql client program.

Invoke [mysqlshow](#page-108-2) like this:

```
mysqlshow [options] [db_name [tbl_name [col_name]]]
```

- If no database is given, a list of database names is shown.
- If no table is given, all matching tables in the database are shown.
- If no column is given, all matching columns and column types in the table are shown.

The output displays only the names of those databases, tables, or columns for which you have some privileges.

If the last argument contains shell or SQL wildcard characters (\*, ?, %, or \_), only those names that are matched by the wildcard are shown. If a database name contains any underscores, those should be escaped with a backslash (some Unix shells require two) to get a list of the proper tables or columns. \* and ? characters are converted into SQL % and \_ wildcard characters. This might cause some confusion when you try to display the columns for a table with a \_ in the name, because in this case, [mysqlshow](#page-108-2) shows you only the table names that match the pattern. This is easily fixed by adding an extra % last on the command line as a separate argument.

[mysqlshow](#page-108-2) supports the following options, which can be specified on the command line or in the [mysqlshow] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.15 mysqlshow Options**

| Option Name             | Description                                                                    |
|-------------------------|--------------------------------------------------------------------------------|
| bind-address            | Use specified network interface to connect to<br>MySQL Server                  |
| character-sets-dir      | Directory where character sets can be found                                    |
| compress                | Compress all information sent between client and<br>server                     |
| compression-algorithms  | Permitted compression algorithms for connections<br>to server                  |
| count                   | Show the number of rows per table                                              |
| debug                   | Write debugging log                                                            |
| debug-check             | Print debugging information when program exits                                 |
| debug-info              | Print debugging information, memory, and CPU<br>statistics when program exits  |
| default-auth            | Authentication plugin to use                                                   |
| default-character-set   | Specify default character set                                                  |
| defaults-extra-file     | Read named option file in addition to usual option<br>files                    |
| defaults-file           | Read only named option file                                                    |
| defaults-group-suffix   | Option group suffix value                                                      |
| enable-cleartext-plugin | Enable cleartext authentication plugin                                         |
| get-server-public-key   | Request RSA public key from server                                             |
| help                    | Display help message and exit                                                  |
| host                    | Host on which MySQL server is located                                          |
| keys                    | Show table indexes                                                             |
| login-path              | Read login path options from .mylogin.cnf                                      |
| no-defaults             | Read no option files                                                           |
| no-login-paths          | Do not read login paths from the login path file                               |
| password                | Password to use when connecting to server                                      |
| password1               | First multifactor authentication password to use<br>when connecting to server  |
| password2               | Second multifactor authentication password to use<br>when connecting to server |

| Option Name                               | Description                                                                    |
|-------------------------------------------|--------------------------------------------------------------------------------|
| password3                                 | Third multifactor authentication password to use<br>when connecting to server  |
| pipe                                      | Connect to server using named pipe (Windows<br>only)                           |
| plugin-dir                                | Directory where plugins are installed                                          |
| port                                      | TCP/IP port number for connection                                              |
| print-defaults                            | Print default options                                                          |
| protocol                                  | Transport protocol to use                                                      |
| server-public-key-path                    | Path name to file containing RSA public key                                    |
| shared-memory-base-name                   | Shared-memory name for shared-memory<br>connections (Windows only)             |
| show-table-type                           | Show a column indicating the table type                                        |
| socket                                    | Unix socket file or Windows named pipe to use                                  |
| ssl-ca                                    | File that contains list of trusted SSL Certificate<br>Authorities              |
| ssl-capath                                | Directory that contains trusted SSL Certificate<br>Authority certificate files |
| ssl-cert                                  | File that contains X.509 certificate                                           |
| ssl-cipher                                | Permissible ciphers for connection encryption                                  |
| ssl-crl                                   | File that contains certificate revocation lists                                |
| ssl-crlpath                               | Directory that contains certificate revocation-list<br>files                   |
| ssl-fips-mode                             | Whether to enable FIPS mode on client side                                     |
| ssl-key                                   | File that contains X.509 key                                                   |
| ssl-mode                                  | Desired security state of connection to server                                 |
| ssl-session-data                          | File that contains SSL session data                                            |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails                     |
| status                                    | Display extra information about each table                                     |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections                  |
| tls-sni-servername                        | Server name supplied by the client                                             |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                         |
| user                                      | MySQL user name to use when connecting to<br>server                            |
| verbose                                   | Verbose mode                                                                   |
| version                                   | Display version information and exit                                           |
| zstd-compression-level                    | Compression level for connections to server that<br>use zstd compression       |

## <span id="page-111-4"></span>• [--help](#page-111-4), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

#### Display a help message and exit.

<span id="page-111-0"></span>• [--bind-address=](#page-111-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-111-1"></span>• [--character-sets-dir=](#page-111-1)dir\_name

| Command-Line Format | character-sets-dir=path |
|---------------------|-------------------------|
| Type                | String                  |
| Default Value       | [none]                  |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-111-2"></span>• [--compress](#page-111-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-111-3"></span>• [--compression-algorithms=](#page-111-3)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

## <span id="page-112-0"></span>• [--count](#page-112-0)

| Command-Line Format | count |
|---------------------|-------|
|---------------------|-------|

Show the number of rows per table. This can be slow for non-MyISAM tables.

<span id="page-112-1"></span>• --debug[=[debug\\_options](#page-112-1)], -# [debug\_options]

| Command-Line Format | debug[=debug_options] |
|---------------------|-----------------------|
| Type                | String                |
| Default Value       | d:t:o                 |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-112-2"></span>• [--debug-check](#page-112-2)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

## <span id="page-112-3"></span>• [--debug-info](#page-112-3)

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-112-5"></span>• [--default-character-set=](#page-112-5)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

<span id="page-112-4"></span>Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration". 483

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-113-0"></span>• [--defaults-extra-file=](#page-113-0)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-113-1"></span>• [--defaults-file=](#page-113-1)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-113-2"></span>• [--defaults-group-suffix=](#page-113-2)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlshow](#page-108-2) normally reads the [client] and [mysqlshow] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-113-2), [mysqlshow](#page-108-2) also reads the [client\_other] and [mysqlshow\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-113-3"></span>• [--enable-cleartext-plugin](#page-113-3)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

<span id="page-114-0"></span>• [--get-server-public-key](#page-114-0)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the RSA public key that it uses for key pair-based password exchange. This option applies to clients that connect to the server using an account that authenticates with the caching\_sha2\_password authentication plugin. For connections by such accounts, the server does not send the public key to the client unless requested. The option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not needed, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-117-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-114-0).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-114-1"></span>• --host=[host\\_name](#page-114-1), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-114-2"></span>• [--keys](#page-114-2), -k

| Command-Line Format | keys |
|---------------------|------|
|---------------------|------|

## Show table indexes.

<span id="page-114-3"></span>• [--login-path=](#page-114-3)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-115-1"></span>• [--no-login-paths](#page-115-1)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

See [--login-path](#page-114-3) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-115-0"></span>• [--no-defaults](#page-115-0)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|                     |             |

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-115-0) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-115-0) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-115-2"></span>• [--password\[=](#page-115-2)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlshow](#page-108-2) prompts for one. If given, there must be no space between [-](#page-115-2) [password=](#page-115-2) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlshow](#page-108-2) should not prompt for one, use the [--skip-password](#page-115-2) option.

<span id="page-115-3"></span>• [--password1\[=](#page-115-3)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlshow](#page-108-2) prompts for one. If given, there must be no space between [--password1=](#page-115-3) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlshow](#page-108-2) should not prompt for one, use the [--skip-password1](#page-115-3) option.

[--password1](#page-115-3) and [--password](#page-115-2) are synonymous, as are [--skip-password1](#page-115-3) and [--skip](#page-115-2)[password](#page-115-2).

<span id="page-116-0"></span>• [--password2\[=](#page-116-0)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-115-3); see the description of that option for details.

<span id="page-116-1"></span>• [--password3\[=](#page-116-1)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-115-3); see the description of that option for details.

<span id="page-116-2"></span>• [--pipe](#page-116-2), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-116-3"></span>• [--plugin-dir=](#page-116-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-112-4) option is used to specify an authentication plugin but [mysqlshow](#page-108-2) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-116-4"></span>• --port=[port\\_num](#page-116-4), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-116-5"></span>• [--print-defaults](#page-116-5)

| Command-Line Format | print-defaults |
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-117-0"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-117-0)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-117-1"></span>• [--server-public-key-path=](#page-117-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-117-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-114-0).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-117-2"></span>• [--shared-memory-base-name=](#page-117-2)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-117-3"></span>• [--show-table-type](#page-117-3), -t

| Command-Line Format | show-table-type |
|---------------------|-----------------|
|                     |                 |

Show a column indicating the table type, as in SHOW FULL TABLES. The type is BASE TABLE or VIEW.

<span id="page-118-0"></span>• [--socket=](#page-118-0)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-118-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

<span id="page-118-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-118-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-118-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-118-2) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_118_Picture_16.jpeg)

## **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-118-2) is OFF. In this case, setting [--ssl-fips-mode](#page-118-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-119-0"></span>• [--status](#page-119-0), -i

| Command-Line Format | status |
|---------------------|--------|
|---------------------|--------|

Display extra information about each table.

<span id="page-119-1"></span>• [--tls-ciphersuites=](#page-119-1)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-119-2"></span>• [--tls-sni-servername=](#page-119-2)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

<span id="page-119-3"></span>• [--tls-version=](#page-119-3)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-119-4"></span>• --user=[user\\_name](#page-119-4), -u user\_name

| Command-Line Format | user=user_name, |
|---------------------|-----------------|
| Type                | String          |

<span id="page-120-0"></span>• [--verbose](#page-120-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Print more information about what the program does. This option can be used multiple times to increase the amount of information.

<span id="page-120-1"></span>• [--version](#page-120-1), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-120-2"></span>• [--zstd-compression-level=](#page-120-2)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".

# <span id="page-120-3"></span>**6.5.7 mysqlslap — A Load Emulation Client**

[mysqlslap](#page-120-3) is a diagnostic program designed to emulate client load for a MySQL server and to report the timing of each stage. It works as if multiple clients are accessing the server.

Invoke [mysqlslap](#page-120-3) like this:

```
mysqlslap [options]
```

Some options such as [--create](#page-126-0) or [--query](#page-134-0) enable you to specify a string containing an SQL statement or a file containing statements. If you specify a file, by default it must contain one statement per line. (That is, the implicit statement delimiter is the newline character.) Use the [--delimiter](#page-128-0) option to specify a different delimiter, which enables you to specify statements that span multiple lines or place multiple statements on a single line. You cannot include comments in a file; [mysqlslap](#page-120-3) does not understand them.

[mysqlslap](#page-120-3) runs in three stages:

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

Let [mysqlslap](#page-120-3) build the query SQL statement with a table of two INT columns and three VARCHAR columns. Use five clients querying 20 times each. Do not create the table or insert the data (that is, use the previous test's schema and data):

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

[mysqlslap](#page-120-3) supports the following options, which can be specified on the command line or in the [mysqlslap] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

#### **Table 6.16 mysqlslap Options**

| auto-generate-sql<br>Generate SQL statements automatically when<br>options<br>auto-generate-sql-add-autoincrement<br>generated tables<br>auto-generate-sql-execute-number<br>Specify how many queries to generate<br>automatically<br>auto-generate-sql-guid-primary<br>generated tables<br>auto-generate-sql-load-type<br>Specify the test load type<br>auto-generate-sql-secondary-indexes<br>automatically generated tables<br>auto-generate-sql-unique-query-number<br>How many different queries to generate for<br>automatic tests<br>auto-generate-sql-unique-write-number | they are not supplied in files or using command<br>Add AUTO_INCREMENT column to automatically |  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|--|
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                               |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                               |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                               |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Add a GUID-based primary key to automatically                                                 |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                               |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Specify how many secondary indexes to add to                                                  |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                               |  |
| generate-sql-write-number                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | How many different queries to generate forauto                                                |  |
| auto-generate-sql-write-number                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | How many row inserts to perform on each thread                                                |  |
| commit<br>How many statements to execute before<br>committing                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                               |  |
| compress<br>server                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Compress all information sent between client and                                              |  |
| compression-algorithms<br>to server                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Permitted compression algorithms for connections                                              |  |
| concurrency<br>SELECT statement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Number of clients to simulate when issuing the                                                |  |
| create<br>creating the table                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | File or string containing the statement to use for                                            |  |
| create-schema                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Schema in which to run the tests                                                              |  |
| csv<br>Generate output in comma-separated values<br>format                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                               |  |
| debug<br>Write debugging log                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                               |  |

| Option Name             | Description                                                                          |
|-------------------------|--------------------------------------------------------------------------------------|
| debug-check             | Print debugging information when program exits                                       |
| debug-info              | Print debugging information, memory, and CPU<br>statistics when program exits        |
| default-auth            | Authentication plugin to use                                                         |
| defaults-extra-file     | Read named option file in addition to usual option<br>files                          |
| defaults-file           | Read only named option file                                                          |
| defaults-group-suffix   | Option group suffix value                                                            |
| delimiter               | Delimiter to use in SQL statements                                                   |
| detach                  | Detach (close and reopen) each connection after<br>each N statements                 |
| enable-cleartext-plugin | Enable cleartext authentication plugin                                               |
| engine                  | Storage engine to use for creating the table                                         |
| get-server-public-key   | Request RSA public key from server                                                   |
| help                    | Display help message and exit                                                        |
| host                    | Host on which MySQL server is located                                                |
| iterations              | Number of times to run the tests                                                     |
| login-path              | Read login path options from .mylogin.cnf                                            |
| no-defaults             | Read no option files                                                                 |
| no-drop                 | Do not drop any schema created during the test<br>run                                |
| no-login-paths          | Do not read login paths from the login path file                                     |
| number-char-cols        | Number of VARCHAR columns to use ifauto<br>generate-sql is specified                 |
| number-int-cols         | Number of INT columns to use ifauto-generate<br>sql is specified                     |
| number-of-queries       | Limit each client to approximately this number of<br>queries                         |
| only-print              | Do not connect to databases. mysqlslap only<br>prints what it would have done        |
| password                | Password to use when connecting to server                                            |
| password1               | First multifactor authentication password to use<br>when connecting to server        |
| password2               | Second multifactor authentication password to use<br>when connecting to server       |
| password3               | Third multifactor authentication password to use<br>when connecting to server        |
| pipe                    | Connect to server using named pipe (Windows<br>only)                                 |
| plugin-dir              | Directory where plugins are installed                                                |
| port                    | TCP/IP port number for connection                                                    |
| post-query              | File or string containing the statement to execute<br>after the tests have completed |
| post-system             | String to execute using system() after the tests<br>have completed                   |

| Option Name                               | Description                                                                    |
|-------------------------------------------|--------------------------------------------------------------------------------|
| pre-query                                 | File or string containing the statement to execute<br>before running the tests |
| pre-system                                | String to execute using system() before running<br>the tests                   |
| print-defaults                            | Print default options                                                          |
| protocol                                  | Transport protocol to use                                                      |
| query                                     | File or string containing the SELECT statement to<br>use for retrieving data   |
| server-public-key-path                    | Path name to file containing RSA public key                                    |
| shared-memory-base-name                   | Shared-memory name for shared-memory<br>connections (Windows only)             |
| silent                                    | Silent mode                                                                    |
| socket                                    | Unix socket file or Windows named pipe to use                                  |
| sql-mode                                  | Set SQL mode for client session                                                |
| ssl-ca                                    | File that contains list of trusted SSL Certificate<br>Authorities              |
| ssl-capath                                | Directory that contains trusted SSL Certificate<br>Authority certificate files |
| ssl-cert                                  | File that contains X.509 certificate                                           |
| ssl-cipher                                | Permissible ciphers for connection encryption                                  |
| ssl-crl                                   | File that contains certificate revocation lists                                |
| ssl-crlpath                               | Directory that contains certificate revocation-list<br>files                   |
| ssl-fips-mode                             | Whether to enable FIPS mode on client side                                     |
| ssl-key                                   | File that contains X.509 key                                                   |
| ssl-mode                                  | Desired security state of connection to server                                 |
| ssl-session-data                          | File that contains SSL session data                                            |
| ssl-session-data-continue-on-failed-reuse | Whether to establish connections if session reuse<br>fails                     |
| tls-ciphersuites                          | Permissible TLSv1.3 ciphersuites for encrypted<br>connections                  |
| tls-sni-servername                        | Server name supplied by the client                                             |
| tls-version                               | Permissible TLS protocols for encrypted<br>connections                         |
| user                                      | MySQL user name to use when connecting to<br>server                            |
| verbose                                   | Verbose mode                                                                   |
| version                                   | Display version information and exit                                           |
| zstd-compression-level                    | Compression level for connections to server that<br>use zstd compression       |

## <span id="page-124-5"></span>• [--help](#page-124-5), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

#### Display a help message and exit.

<span id="page-124-0"></span>• [--auto-generate-sql](#page-124-0), -a

| Command-Line Format | auto-generate-sql |
|---------------------|-------------------|
| Type                | Boolean           |
| Default Value       | FALSE             |

## Generate SQL statements automatically when they are not supplied in files or using command options.

<span id="page-124-1"></span>• [--auto-generate-sql-add-autoincrement](#page-124-1)

| Command-Line Format | auto-generate-sql-add<br>autoincrement |
|---------------------|----------------------------------------|
| Type                | Boolean                                |
| Default Value       | FALSE                                  |

# Add an AUTO\_INCREMENT column to automatically generated tables.

<span id="page-124-2"></span>• [--auto-generate-sql-execute-number=](#page-124-2)N

| Command-Line Format | auto-generate-sql-execute-number=# |
|---------------------|------------------------------------|
| Type                | Numeric                            |

#### Specify how many queries to generate automatically.

<span id="page-124-3"></span>• [--auto-generate-sql-guid-primary](#page-124-3)

| Command-Line Format | auto-generate-sql-guid-primary |  |
|---------------------|--------------------------------|--|
| Type                | Boolean                        |  |
| Default Value       | FALSE                          |  |

#### Add a GUID-based primary key to automatically generated tables.

<span id="page-124-4"></span>• [--auto-generate-sql-load-type=](#page-124-4)type

| Command-Line Format | auto-generate-sql-load-type=type |     |
|---------------------|----------------------------------|-----|
| Type                | Enumeration                      |     |
| Default Value       | mixed                            | 495 |
| Valid Values        | read                             |     |
|                     | write                            |     |

|  | mixed |
|--|-------|
|--|-------|

Specify the test load type. The permissible values are read (scan tables), write (insert into tables), key (read primary keys), update (update primary keys), or mixed (half inserts, half scanning selects). The default is mixed.

<span id="page-125-0"></span>• [--auto-generate-sql-secondary-indexes=](#page-125-0)N

| Command-Line Format | auto-generate-sql-secondary<br>indexes=# |
|---------------------|------------------------------------------|
| Type                | Numeric                                  |
| Default Value       | 0                                        |

Specify how many secondary indexes to add to automatically generated tables. By default, none are added.

<span id="page-125-1"></span>• [--auto-generate-sql-unique-query-number=](#page-125-1)N

| Command-Line Format | auto-generate-sql-unique-query<br>number=# |
|---------------------|--------------------------------------------|
| Type                | Numeric                                    |
| Default Value       | 10                                         |

How many different queries to generate for automatic tests. For example, if you run a key test that performs 1000 selects, you can use this option with a value of 1000 to run 1000 unique queries, or with a value of 50 to perform 50 different selects. The default is 10.

<span id="page-125-2"></span>• [--auto-generate-sql-unique-write-number=](#page-125-2)N

| Command-Line Format | auto-generate-sql-unique-write<br>number=# |
|---------------------|--------------------------------------------|
| Type                | Numeric                                    |
| Default Value       | 10                                         |

How many different queries to generate for [--auto-generate-sql-write-number](#page-125-3). The default is 10.

<span id="page-125-3"></span>• [--auto-generate-sql-write-number=](#page-125-3)N

| Command-Line Format | auto-generate-sql-write-number=# |
|---------------------|----------------------------------|
| Type                | Numeric                          |
| Default Value       | 100                              |

How many row inserts to perform. The default is 100.

<span id="page-125-4"></span>• [--commit=](#page-125-4)N

| Command-Line Format | commit=# |
|---------------------|----------|
| Type                | Numeric  |
| Default Value       | 0        |

How many statements to execute before committing. The default is 0 (no commits are done).

<span id="page-126-1"></span>• [--compress](#page-126-1), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See Section 6.2.8, "Connection Compression Control".

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-126-2"></span>• [--compression-algorithms=](#page-126-2)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |
|                     | zstd                         |
|                     | uncompressed                 |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-126-3"></span>• [--concurrency=](#page-126-3)N, -c N

| Command-Line Format | concurrency=# |
|---------------------|---------------|
| Type                | Numeric       |

The number of parallel clients to simulate.

<span id="page-126-0"></span>• [--create=](#page-126-0)value

| Command-Line Format | create=value |
|---------------------|--------------|
| Type                | String       |

The file or string containing the statement to use for creating the table.

<span id="page-126-4"></span>• [--create-schema=](#page-126-4)value

| Command-Line Format | create-schema=value |
|---------------------|---------------------|
|---------------------|---------------------|

|  | Type<br>String |  |
|--|----------------|--|
|--|----------------|--|

The schema in which to run the tests.

![](_page_127_Picture_3.jpeg)

#### **Note**

If the [--auto-generate-sql](#page-124-0) option is also given, [mysqlslap](#page-120-3) drops the schema at the end of the test run. To avoid this, use the [--no-drop](#page-130-2) option as well.

<span id="page-127-0"></span>• --csv[=[file\\_name](#page-127-0)]

| Command-Line Format | csv=[file] |
|---------------------|------------|
| Type                | File name  |

Generate output in comma-separated values format. The output goes to the named file, or to the standard output if no file is given.

<span id="page-127-1"></span>• --debug[=[debug\\_options](#page-127-1)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]      |
|---------------------|----------------------------|
| Type                | String                     |
| Default Value       | d:t:o,/tmp/mysqlslap.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysqlslap.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-127-2"></span>• [--debug-check](#page-127-2)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-127-3"></span>• [--debug-info](#page-127-3), -T

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

<span id="page-127-4"></span>• [--default-auth=](#page-127-4)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-128-1"></span>• [--defaults-extra-file=](#page-128-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-128-2"></span>• [--defaults-file=](#page-128-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-128-3"></span>• [--defaults-group-suffix=](#page-128-3)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysqlslap](#page-120-3) normally reads the [client] and [mysqlslap] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-128-3), [mysqlslap](#page-120-3) also reads the [client\_other] and [mysqlslap\_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-128-0"></span>• [--delimiter=](#page-128-0)str, -F str

| Command-Line Format | delimiter=str |
|---------------------|---------------|
| Type                | String        |
|                     | 499           |

## <span id="page-129-0"></span>• [--detach=](#page-129-0)N

| Command-Line Format | detach=# |
|---------------------|----------|
| Type                | Numeric  |
| Default Value       | 0        |

Detach (close and reopen) each connection after each N statements. The default is 0 (connections are not detached).

## <span id="page-129-1"></span>• [--enable-cleartext-plugin](#page-129-1)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-129-2"></span>• --engine=[engine\\_name](#page-129-2), -e engine\_name

| Command-Line Format | engine=engine_name |
|---------------------|--------------------|
| Type                | String             |

The storage engine to use for creating tables.

<span id="page-129-3"></span>• [--get-server-public-key](#page-129-3)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the RSA public key that it uses for key pair-based password exchange. This option applies to clients that connect to the server using an account that authenticates with the caching\_sha2\_password authentication plugin. For connections by such accounts, the server does not send the public key to the client unless requested. The option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not needed, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-134-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-129-3).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-129-4"></span>• --host=[host\\_name](#page-129-4), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

<span id="page-129-5"></span>• [--iterations=](#page-129-5)N, -i N

| Command-Line Format | iterations=# |
|---------------------|--------------|
| Type                | Numeric      |

The number of times to run the tests.

<span id="page-130-0"></span>• [--login-path=](#page-130-0)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7, "mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-130-3"></span>• [--no-login-paths](#page-130-3)

| Command-Line Format | no-login-paths |
|---------------------|----------------|
|---------------------|----------------|

Skips reading options from the login path file.

See [--login-path](#page-130-0) for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-130-2"></span>• [--no-drop](#page-130-2)

| Command-Line Format | no-drop |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | FALSE   |

Prevent [mysqlslap](#page-120-3) from dropping any schema it creates during the test run.

<span id="page-130-1"></span>• [--no-defaults](#page-130-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|                     |             |

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-130-1) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-130-1) is used. To create .mylogin.cnf, use the [mysql\\_config\\_editor](#page-176-0) utility. See [Section 6.6.7,](#page-176-0) ["mysql\\_config\\_editor — MySQL Configuration Utility".](#page-176-0)

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

<span id="page-130-4"></span>• [--number-char-cols=](#page-130-4)N, -x N

| Command-Line Format | number-char-cols=# |
|---------------------|--------------------|
| Type                | Numeric            |

The number of VARCHAR columns to use if [--auto-generate-sql](#page-124-0) is specified.

<span id="page-131-0"></span>• [--number-int-cols=](#page-131-0)N, -y N

| Command-Line Format | number-int-cols=# |
|---------------------|-------------------|
| Type                | Numeric           |

The number of INT columns to use if [--auto-generate-sql](#page-124-0) is specified.

<span id="page-131-1"></span>• [--number-of-queries=](#page-131-1)N

| Command-Line Format | number-of-queries=# |
|---------------------|---------------------|
| Type                | Numeric             |

Limit each client to approximately this many queries. Query counting takes into account the statement delimiter. For example, if you invoke [mysqlslap](#page-120-3) as follows, the ; delimiter is recognized so that each instance of the query string counts as two queries. As a result, 5 rows (not 10) are inserted.

```
mysqlslap --delimiter=";" --number-of-queries=10
 --query="use test;insert into t values(null)"
```

<span id="page-131-2"></span>• [--only-print](#page-131-2)

| Command-Line Format | only-print |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Do not connect to databases. [mysqlslap](#page-120-3) only prints what it would have done.

<span id="page-131-3"></span>• [--password\[=](#page-131-3)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlslap](#page-120-3) prompts for one. If given, there must be no space between [-](#page-131-3) [password=](#page-131-3) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

## <span id="page-132-0"></span>• [--password1\[=](#page-132-0)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysqlslap](#page-120-3) prompts for one. If given, there must be no space between [--password1=](#page-132-0) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysqlslap](#page-120-3) should not prompt for one, use the [--skip-password1](#page-132-0) option.

[--password1](#page-132-0) and [--password](#page-131-3) are synonymous, as are [--skip-password1](#page-132-0) and [--skip](#page-131-3)[password](#page-131-3).

<span id="page-132-1"></span>• [--password2\[=](#page-132-1)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-132-0); see the description of that option for details.

<span id="page-132-2"></span>• [--password3\[=](#page-132-2)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-132-0); see the description of that option for details.

<span id="page-132-3"></span>• [--pipe](#page-132-3), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-132-4"></span>• [--plugin-dir=](#page-132-4)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-127-4) option is used to specify an authentication plugin but [mysqlslap](#page-120-3) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-132-5"></span>• --port=[port\\_num](#page-132-5), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-132-6"></span>• [--post-query=](#page-132-6)value

| Command-Line Format | post-query=value |
|---------------------|------------------|
| Type                | String           |

The file or string containing the statement to execute after the tests have completed. This execution is not counted for timing purposes.

## <span id="page-133-0"></span>• [--post-system=](#page-133-0)str

| Command-Line Format | post-system=str |
|---------------------|-----------------|
| Type                | String          |

The string to execute using system() after the tests have completed. This execution is not counted for timing purposes.

## <span id="page-133-1"></span>• [--pre-query=](#page-133-1)value

| Command-Line Format | pre-query=value |
|---------------------|-----------------|
| Type                | String          |

The file or string containing the statement to execute before running the tests. This execution is not counted for timing purposes.

## <span id="page-133-2"></span>• [--pre-system=](#page-133-2)str

| Command-Line Format | pre-system=str |
|---------------------|----------------|
| Type                | String         |

The string to execute using system() before running the tests. This execution is not counted for timing purposes.

## <span id="page-133-3"></span>• [--print-defaults](#page-133-3)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, "Command-Line Options that Affect Option-File Handling".

## <span id="page-133-4"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-133-4)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see Section 6.2.7, "Connection Transport Protocols".

<span id="page-134-0"></span>• [--query=](#page-134-0)value, -q value

| Command-Line Format | query=value |
|---------------------|-------------|
| Type                | String      |

The file or string containing the SELECT statement to use for retrieving data.

<span id="page-134-1"></span>• [--server-public-key-path=](#page-134-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-134-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-129-3).

For sha256\_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-134-2"></span>• [--shared-memory-base-name=](#page-134-2)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-134-3"></span>• [--silent](#page-134-3), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Silent mode. No output.

<span id="page-134-4"></span>• [--socket=](#page-134-4)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-135-0"></span>• [--sql-mode=](#page-135-0)mode

| Command-Line Format | sql-mode=mode |
|---------------------|---------------|
| Type                | String        |

Set the SQL mode for the client session.

<span id="page-135-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See Command Options for Encrypted Connections.

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

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-135-2) is OFF. In this case, setting [--ssl-fips-mode](#page-135-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-135-3"></span>• [--tls-ciphersuites=](#page-135-3)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
|                     |                                   |

| Type | String |
|------|--------|
|------|--------|

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-136-0"></span>• [--tls-sni-servername=](#page-136-0)server\_name

| Command-Line Format | tls-sni-servername=server_name |
|---------------------|--------------------------------|
| Type                | String                         |

When specified, the name is passed to the libmysqlclient C API library using the MYSQL\_OPT\_TLS\_SNI\_SERVERNAME option of [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). The server name is not casesensitive. To show which server name the client specified for the current session, if any, check the Tls\_sni\_server\_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this option to function). The MySQL implementation of SNI represents the clientside only.

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

<span id="page-136-3"></span>• [--verbose](#page-136-3), -v

| Command-Line Format | verbose |
|---------------------|---------|

Verbose mode. Print more information about what the program does. This option can be used multiple times to increase the amount of information. <sup>507</sup> <span id="page-137-0"></span>• [--version](#page-137-0), -V

| Command-Line Format | version |
|---------------------|---------|

Display version information and exit.

<span id="page-137-1"></span>• [--zstd-compression-level=](#page-137-1)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see Section 6.2.8, "Connection Compression Control".