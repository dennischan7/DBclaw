---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section describes client programs that connect to the MySQL server.

# <span id="page-77-0"></span>**6.5.1 mysql — The MySQL Command-Line Client**

[mysql](#page-77-0) is a simple SQL shell with input line editing capabilities. It supports interactive and noninteractive use. When used interactively, query results are presented in an ASCII-table format. When used noninteractively (for example, as a filter), the result is presented in tab-separated format. The output format can be changed using command options.

If you have problems due to insufficient memory for large result sets, use the [--quick](#page-99-0) option. This forces [mysql](#page-77-0) to retrieve results from the server a row at a time rather than retrieving the entire result set and buffering it in memory before displaying it. This is done by returning the result set using the [mysql\\_use\\_result\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-use-result.md) C API function in the client/server library rather than [mysql\\_store\\_result\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-store-result.md).

![](_page_77_Picture_17.jpeg)

### **Note**

Alternatively, MySQL Shell offers access to the X DevAPI. For details, see [MySQL Shell 8.0](https://dev.mysql.com/doc/mysql-shell/8.0/en/).

Using [mysql](#page-77-0) is very easy. Invoke it from the prompt of your command interpreter as follows:

mysql db\_name

Or:

```
mysql --user=user_name --password db_name
```

In this case, you'll need to enter your password in response to the prompt that [mysql](#page-77-0) displays:

```
Enter password: your_password
```

Then type an SQL statement, end it with ;, \g, or \G and press Enter.

Typing **Control+C** interrupts the current statement if there is one, or cancels any partial input line otherwise.

You can execute SQL statements in a script file (batch file) like this:

```
mysql db_name < script.sql > output.tab
```

On Unix, the [mysql](#page-77-0) client logs statements executed interactively to a history file. See [Section 6.5.1.3,](#page-113-0) ["mysql Client Logging"](#page-113-0).

# <span id="page-78-0"></span>**6.5.1.1 mysql Client Options**

[mysql](#page-77-0) supports the following options, which can be specified on the command line or in the [mysql] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.12 mysql Client Options**

| Option Name                                 | Description                                                                  | Deprecated |
|---------------------------------------------|------------------------------------------------------------------------------|------------|
| authentication-oci-client-config<br>profile | Name of the OCI profile defined<br>in the OCI config file to use             |            |
| auto-rehash                                 | Enable automatic rehashing                                                   |            |
| auto-vertical-output                        | Enable automatic vertical result<br>set display                              |            |
| batch                                       | Do not use history file                                                      |            |
| binary-as-hex                               | Display binary values in<br>hexadecimal notation                             |            |
| binary-mode                                 | Disable \r\n - to - \n translation<br>and treatment of \0 as end-of<br>query |            |
| bind-address                                | Use specified network interface<br>to connect to MySQL Server                |            |
| character-sets-dir                          | Directory where character sets<br>are installed                              |            |
| column-names                                | Write column names in results                                                |            |
| column-type-info                            | Display result set metadata                                                  |            |
| commands                                    | Enable or disable processing of<br>local mysql client commands               |            |
| comments                                    | Whether to retain or strip<br>comments in statements sent to<br>the server   |            |
| compress                                    | Compress all information sent<br>between client and server                   | Yes        |

| Option Name              | Description                                                                         | Deprecated |
|--------------------------|-------------------------------------------------------------------------------------|------------|
| compression-algorithms   | Permitted compression<br>algorithms for connections to<br>server                    |            |
| connect-expired-password | Indicate to server that client<br>can handle expired-password<br>sandbox mode       |            |
| connect-timeout          | Number of seconds before<br>connection timeout                                      |            |
| database                 | The database to use                                                                 |            |
| debug                    | Write debugging log; supported<br>only if MySQL was built with<br>debugging support |            |
| debug-check              | Print debugging information<br>when program exits                                   |            |
| debug-info               | Print debugging information,<br>memory, and CPU statistics<br>when program exits    |            |
| default-auth             | Authentication plugin to use                                                        |            |
| default-character-set    | Specify default character set                                                       |            |
| defaults-extra-file      | Read named option file in<br>addition to usual option files                         |            |
| defaults-file            | Read only named option file                                                         |            |
| defaults-group-suffix    | Option group suffix value                                                           |            |
| delimiter                | Set the statement delimiter                                                         |            |
| dns-srv-name             | Use DNS SRV lookup for host<br>information                                          |            |
| enable-cleartext-plugin  | Enable cleartext authentication<br>plugin                                           |            |
| execute                  | Execute the statement and quit                                                      |            |
| fido-register-factor     | Multifactor authentication factors<br>for which registration must be<br>done        | Yes        |
| force                    | Continue even if an SQL error<br>occurs                                             |            |
| get-server-public-key    | Request RSA public key from<br>server                                               |            |
| help                     | Display help message and exit                                                       |            |
| histignore               | Patterns specifying which<br>statements to ignore for logging                       |            |
| host                     | Host on which MySQL server is<br>located                                            |            |
| html                     | Produce HTML output                                                                 |            |
| ignore-spaces            | Ignore spaces after function<br>names                                               |            |
| init-command             | SQL statement to execute after<br>connecting                                        |            |
| line-numbers             | Write line numbers for errors                                                       |            |

| Option Name                                   | Description                                                                                     | Deprecated |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------|------------|
| load-data-local-dir                           | Directory for files named in<br>LOAD DATA LOCAL statements                                      |            |
| local-infile                                  | Enable or disable for LOCAL<br>capability for LOAD DATA                                         |            |
| login-path                                    | Read login path options<br>from .mylogin.cnf                                                    |            |
| max-allowed-packet                            | Maximum packet length to send<br>to or receive from server                                      |            |
| max-join-size                                 | The automatic limit for rows in a<br>join when usingsafe-updates                                |            |
| named-commands                                | Enable named mysql commands                                                                     |            |
| net-buffer-length                             | Buffer size for TCP/IP and socket<br>communication                                              |            |
| network-namespace                             | Specify network namespace                                                                       |            |
| no-auto-rehash                                | Disable automatic rehashing                                                                     |            |
| no-beep                                       | Do not beep when errors occur                                                                   |            |
| no-defaults                                   | Read no option files                                                                            |            |
| oci-config-file                               | Defines an alternate location for<br>the Oracle Cloud Infrastructure<br>CLI configuration file. |            |
| one-database                                  | Ignore statements except those<br>for the default database named<br>on the command line         |            |
| pager                                         | Use the given command for<br>paging query output                                                |            |
| password                                      | Password to use when<br>connecting to server                                                    |            |
| password1                                     | First multifactor authentication<br>password to use when<br>connecting to server                |            |
| password2                                     | Second multifactor authentication<br>password to use when<br>connecting to server               |            |
| password3                                     | Third multifactor authentication<br>password to use when<br>connecting to server                |            |
| pipe                                          | Connect to server using named<br>pipe (Windows only)                                            |            |
| plugin-authentication-kerberos<br>client-mode | Permit GSSAPI pluggable<br>authentication through the MIT<br>Kerberos library on Windows        |            |
| plugin-dir                                    | Directory where plugins are<br>installed                                                        |            |
| port                                          | TCP/IP port number for<br>connection                                                            |            |
| print-defaults                                | Print default options                                                                           |            |

| Option Name               | Description                                                                       | Deprecated |
|---------------------------|-----------------------------------------------------------------------------------|------------|
| prompt                    | Set the prompt to the specified<br>format                                         |            |
| protocol                  | Transport protocol to use                                                         |            |
| quick                     | Do not cache each query result                                                    |            |
| raw                       | Write column values without<br>escape conversion                                  |            |
| reconnect                 | If the connection to the server<br>is lost, automatically try to<br>reconnect     |            |
| safe-updates,i-am-a-dummy | Allow only UPDATE and<br>DELETE statements that specify<br>key values             |            |
| select-limit              | The automatic limit for SELECT<br>statements when usingsafe<br>updates            |            |
| server-public-key-path    | Path name to file containing RSA<br>public key                                    |            |
| shared-memory-base-name   | Shared-memory name for<br>shared-memory connections<br>(Windows only)             |            |
| show-warnings             | Show warnings after each<br>statement if there are any                            |            |
| sigint-ignore             | Ignore SIGINT signals (typically<br>the result of typing Control+C)               |            |
| silent                    | Silent mode                                                                       |            |
| skip-auto-rehash          | Disable automatic rehashing                                                       |            |
| skip-column-names         | Do not write column names in<br>results                                           |            |
| skip-line-numbers         | Skip line numbers for errors                                                      |            |
| skip-named-commands       | Disable named mysql commands                                                      |            |
| skip-pager                | Disable paging                                                                    |            |
| skip-reconnect            | Disable reconnecting                                                              |            |
| skip-system-command       | Disable system (\!) command                                                       |            |
| socket                    | Unix socket file or Windows<br>named pipe to use                                  |            |
| ssl-ca                    | File that contains list of trusted<br>SSL Certificate Authorities                 |            |
| ssl-capath                | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files |            |
| ssl-cert                  | File that contains X.509<br>certificate                                           |            |
| ssl-cipher                | Permissible ciphers for<br>connection encryption                                  |            |
| ssl-crl                   | File that contains certificate<br>revocation lists                                |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                      |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                     | Yes        |
| ssl-key                                      | File that contains X.509 key                                                      |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                 |            |
| ssl-session-data                             | File that contains SSL session<br>data                                            |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                        |            |
| syslog                                       | Log interactive statements to<br>syslog                                           |            |
| system-command                               | Enable or disable system (\!)<br>command                                          |            |
| table                                        | Display output in tabular format                                                  |            |
| tee                                          | Append a copy of output to<br>named file                                          |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                     |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                            |            |
| unbuffered                                   | Flush the buffer after each query                                                 |            |
| user                                         | MySQL user name to use when<br>connecting to server                               |            |
| verbose                                      | Verbose mode                                                                      |            |
| version                                      | Display version information and<br>exit                                           |            |
| vertical                                     | Print query output rows vertically<br>(one line per column value)                 |            |
| wait                                         | If the connection cannot be<br>established, wait and retry<br>instead of aborting |            |
| xml                                          | Produce XML output                                                                |            |
| zstd-compression-level                       | Compression level for<br>connections to server that use<br>zstd compression       |            |

<span id="page-82-1"></span>• [--help](#page-82-1), -?

| Command-Line Format |      |  |
|---------------------|------|--|
|                     | help |  |

### Display a help message and exit.

<span id="page-82-0"></span>• [--authentication-oci-client-config-profile](#page-82-0)

| Command-Line Format | authentication-oci-client-config |
|---------------------|----------------------------------|
|                     | profile=profileName              |

Specify the name of the OCI configuration profile to use. If not set, the default profile is used.

<span id="page-83-0"></span>• [--auto-rehash](#page-83-0)

| Command-Line Format | auto-rehash      |
|---------------------|------------------|
| Disabled by         | skip-auto-rehash |

Enable automatic rehashing. This option is on by default, which enables database, table, and column name completion. Use [--disable-auto-rehash](#page-83-0) to disable rehashing. That causes [mysql](#page-77-0) to start faster, but you must issue the rehash command or its \# shortcut if you want to use name completion.

To complete a name, enter the first part and press Tab. If the name is unambiguous, [mysql](#page-77-0) completes it. Otherwise, you can press Tab again to see the possible names that begin with what you have typed so far. Completion does not occur if there is no default database.

![](_page_83_Picture_7.jpeg)

### **Note**

This feature requires a MySQL client that is compiled with the **readline** library. Typically, the **readline** library is not available on Windows.

<span id="page-83-1"></span>• [--auto-vertical-output](#page-83-1)

| Command-Line Format | auto-vertical-output |
|---------------------|----------------------|
|---------------------|----------------------|

Cause result sets to be displayed vertically if they are too wide for the current window, and using normal tabular format otherwise. (This applies to statements terminated by ; or \G.)

<span id="page-83-2"></span>• [--batch](#page-83-2), -B

| Command-Line Format | batch |
|---------------------|-------|
|---------------------|-------|

Print results using tab as the column separator, with each row on a new line. With this option, [mysql](#page-77-0) does not use the history file.

Batch mode results in nontabular output format and escaping of special characters. Escaping may be disabled by using raw mode; see the description for the [--raw](#page-100-0) option.

<span id="page-83-3"></span>• [--binary-as-hex](#page-83-3)

| Command-Line Format | binary-as-hex |
|---------------------|---------------|
| Type                | Boolean       |

Default Value FALSE in noninteractive mode

When this option is given, [mysql](#page-77-0) displays binary data using hexadecimal notation (0xvalue). This occurs whether the overall output display format is tabular, vertical, HTML, or XML.

[--binary-as-hex](#page-83-3) when enabled affects display of all binary strings, including those returned by functions such as CHAR() and UNHEX(). The following example demonstrates this using the ASCII code for A (65 decimal, 41 hexadecimal):

• [--binary-as-hex](#page-83-3) disabled:

```
mysql> SELECT CHAR(0x41), UNHEX('41');
+------------+-------------+
| CHAR(0x41) | UNHEX('41') |
+------------+-------------+
| A | A |
+------------+-------------+
```

• [--binary-as-hex](#page-83-3) enabled:

```
mysql> SELECT CHAR(0x41), UNHEX('41');
+------------------------+--------------------------+
| CHAR(0x41) | UNHEX('41') |
+------------------------+--------------------------+
| 0x41 | 0x41 |
+------------------------+--------------------------+
```

To write a binary string expression so that it displays as a character string regardless of whether [-](#page-83-3) [binary-as-hex](#page-83-3) is enabled, use these techniques:

• The CHAR() function has a USING charset clause:

```
mysql> SELECT CHAR(0x41 USING utf8mb4);
+--------------------------+
| CHAR(0x41 USING utf8mb4) |
+--------------------------+
| A |
+--------------------------+
```

• More generally, use CONVERT() to convert an expression to a given character set:

```
mysql> SELECT CONVERT(UNHEX('41') USING utf8mb4);
+------------------------------------+
| CONVERT(UNHEX('41') USING utf8mb4) |
+------------------------------------+
| A |
+------------------------------------+
```

As of MySQL 8.0.19, when [mysql](#page-77-0) operates in interactive mode, this option is enabled by default. In addition, output from the status (or \s) command includes this line when the option is enabled implicitly or explicitly:

```
Binary data as: Hexadecimal
```

To disable hexadecimal notation, use [--skip-binary-as-hex](#page-83-3)

<span id="page-84-0"></span>• [--binary-mode](#page-84-0)

| Command-Line Format | binary-mode |
|---------------------|-------------|
|---------------------|-------------|

This option helps when processing mysqlbinlog output that may contain BLOB values. By default, [mysql](#page-77-0) translates \r\n in statement strings to \n and interprets \0 as the statement terminator. [--binary-mode](#page-84-0) disables both features. It also disables all [mysql](#page-77-0) commands except charset 455 and delimiter in noninteractive mode (for input piped to [mysql](#page-77-0) or loaded using the source command).

(MySQL 8.0.43 and later:) --binary-mode, when enabled, causes the server to disregard any setting for [--commands](#page-85-4) .

<span id="page-85-1"></span>• [--bind-address=](#page-85-1)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-85-2"></span>• [--character-sets-dir=](#page-85-2)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-85-0"></span>• [--column-names](#page-85-0)

| Command-Line Format | column-names |
|---------------------|--------------|
|---------------------|--------------|

Write column names in results.

<span id="page-85-3"></span>• [--column-type-info](#page-85-3)

| Command-Line Format | column-type-info |
|---------------------|------------------|
|                     |                  |

Display result set metadata. This information corresponds to the contents of C API MYSQL\_FIELD data structures. See [C API Basic Data Structures.](https://dev.mysql.com/doc/c-api/8.0/en/c-api-data-structures.md)

<span id="page-85-4"></span>• [--commands](#page-85-4)

| Command-Line Format | commands |
|---------------------|----------|
| Type                | Boolean  |
| Default Value       | TRUE     |

Whether to enable or disable processing of local [mysql](#page-77-0) client commands. Setting this option to FALSE disables such processing, and has the effects listed here:

- The following [mysql](#page-77-0) client commands are disabled:
  - charset (/C remains enabled)
  - clear
  - connect
  - edit
  - ego
  - exit

- go
- help
- nopager
- notee
- nowarning
- pager
- print
- prompt
- query\_attributes
- quit
- rehash
- resetconnection
- ssl\_session\_data\_print
- source
- status
- system
- tee
- \u (use is passed to the server)
- warnings
- The \C and delimiter commands remain enabled.
- The [--system-command](#page-104-1) option is ignored, and has no effect.

This option has no effect when [--binary-mode](#page-84-0) is enabled.

When --commands is enabled, it is possible to disable (only) the system command using the [-](#page-104-1) [system-command](#page-104-1) option.

This option was added in MySQL 8.0.43.

<span id="page-86-0"></span>• [--comments](#page-86-0), -c

| Command-Line Format | comments |
|---------------------|----------|
| Type                | Boolean  |

| Default Value | FALSE |
|---------------|-------|
|---------------|-------|

Whether to strip or preserve comments in statements sent to the server. The default is [--skip](#page-86-0)[comments](#page-86-0) (strip comments), enable with [--comments](#page-86-0) (preserve comments).

![](_page_87_Picture_3.jpeg)

### **Note**

The [mysql](#page-77-0) client always passes optimizer hints to the server, regardless of whether this option is given.

Comment stripping is deprecated. Expect this feature and the options to control it to be removed in a future MySQL release.

<span id="page-87-0"></span>• [--compress](#page-87-0), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See [Section 6.2.8,](#page-32-0) ["Connection Compression Control".](#page-32-0)

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

<span id="page-87-1"></span>• [--compression-algorithms=](#page-87-1)value

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

<span id="page-87-2"></span>• [--connect-expired-password](#page-87-2)

| Command-Line Format | connect-expired-password |
|---------------------|--------------------------|
|---------------------|--------------------------|

### <span id="page-88-0"></span>• [--connect-timeout=](#page-88-0)value

| Command-Line Format | connect-timeout=value |
|---------------------|-----------------------|
| Type                | Numeric               |
| Default Value       | 0                     |

The number of seconds before connection timeout. (Default value is 0.)

<span id="page-88-1"></span>• [--database=](#page-88-1)db\_name, -D db\_name

| Command-Line Format | database=dbname |
|---------------------|-----------------|
| Type                | String          |

The database to use. This is useful primarily in an option file.

<span id="page-88-2"></span>• --debug[=[debug\\_options](#page-88-2)], -# [debug\_options]

| Command-Line Format | debug[=debug_options]  |
|---------------------|------------------------|
| Type                | String                 |
| Default Value       | d:t:o,/tmp/mysql.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:o,/tmp/mysql.trace.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-88-3"></span>• [--debug-check](#page-88-3)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |
| Default Value       | FALSE       |

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-88-4"></span>• [--debug-info](#page-88-4), -T

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH\_DEBUG. MySQL release binaries provided by Oracle are not built using this option.

### <span id="page-88-5"></span>• [--default-auth=](#page-88-5)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
|---------------------|---------------------|

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-89-0"></span>• [--default-character-set=](#page-89-0)charset\_name

| Command-Line Format | default-character-set=charset_name |
|---------------------|------------------------------------|
| Type                | String                             |

Use charset\_name as the default character set for the client and connection.

This option can be useful if the operating system uses one character set and the [mysql](#page-77-0) client by default uses another. In this case, output may be formatted incorrectly. You can usually fix such issues by using this option to force the client to use the system character set instead.

For more information, see Section 12.4, "Connection Character Sets and Collations", and Section 12.15, "Character Set Configuration".

<span id="page-89-1"></span>• [--defaults-extra-file=](#page-89-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-89-2"></span>• [--defaults-file=](#page-89-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with [--defaults-file](#page-1-0), client programs read .mylogin.cnf.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-89-3"></span>• [--defaults-group-suffix=](#page-89-3)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

given as [--defaults-group-suffix=\\_other](#page-89-3), [mysql](#page-77-0) also reads the [client\_other] and [mysql\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-90-1"></span>• [--delimiter=](#page-90-1)str

| Command-Line Format | delimiter=str |
|---------------------|---------------|
| Type                | String        |
| Default Value       | ;             |

Set the statement delimiter. The default is the semicolon character (;).

<span id="page-90-2"></span>• [--disable-named-commands](#page-90-2)

Disable named commands. Use the \\* form only, or use named commands only at the beginning of a line ending with a semicolon (;). [mysql](#page-77-0) starts with this option enabled by default. However, even with this option, long-format commands still work from the first line. See [Section 6.5.1.2, "mysql](#page-106-0) [Client Commands".](#page-106-0)

<span id="page-90-0"></span>• [--dns-srv-name=](#page-90-0)name

| Command-Line Format | dns-srv-name=name |
|---------------------|-------------------|
| Type                | String            |

Specifies the name of a DNS SRV record that determines the candidate hosts to use for establishing a connection to a MySQL server. For information about DNS SRV support in MySQL, see [Section 6.2.6, "Connecting to the Server Using DNS SRV Records".](#page-29-0)

Suppose that DNS is configured with this SRV information for the example.com domain:

```
Name TTL Class Priority Weight Port Target
_mysql._tcp.example.com. 86400 IN SRV 0 5 3306 host1.example.com
_mysql._tcp.example.com. 86400 IN SRV 0 10 3306 host2.example.com
_mysql._tcp.example.com. 86400 IN SRV 10 5 3306 host3.example.com
_mysql._tcp.example.com. 86400 IN SRV 20 5 3306 host4.example.com
```

To use that DNS SRV record, invoke [mysql](#page-77-0) like this:

```
mysql --dns-srv-name=_mysql._tcp.example.com
```

[mysql](#page-77-0) then attempts a connection to each server in the group until a successful connection is established. A failure to connect occurs only if a connection cannot be established to any of the servers. The priority and weight values in the DNS SRV record determine the order in which servers should be tried.

When invoked with [--dns-srv-name](#page-90-0), [mysql](#page-77-0) attempts to establish TCP connections only.

The [--dns-srv-name](#page-90-0) option takes precedence over the [--host](#page-93-0) option if both are given. [--dns](#page-90-0)[srv-name](#page-90-0) causes connection establishment to use the [mysql\\_real\\_connect\\_dns\\_srv\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect-dns-srv.md) C API function rather than [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md). However, if the connect command is subsequently used at runtime and specifies a host name argument, that host name takes precedence over any [-](#page-90-0) [dns-srv-name](#page-90-0) option given at [mysql](#page-77-0) startup to specify a DNS SRV record.

<span id="page-91-0"></span>• [--enable-cleartext-plugin](#page-91-0)

| Command-Line Format | enable-cleartext-plugin |
|---------------------|-------------------------|
| Type                | Boolean                 |
| Default Value       | FALSE                   |

Enable the mysql\_clear\_password cleartext authentication plugin. (See Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".)

<span id="page-91-1"></span>• [--execute=](#page-91-1)statement, -e statement

| Command-Line Format | execute=statement |
|---------------------|-------------------|
| Type                | String            |

Execute the statement and quit. The default output format is like that produced with [--batch](#page-83-2). See Section 6.2.2.1, "Using Options on the Command Line", for some examples. With this option, [mysql](#page-77-0) does not use the history file.

<span id="page-91-2"></span>• [--fido-register-factor=](#page-91-2)value

| Command-Line Format | fido-register-factor=value |
|---------------------|----------------------------|
| Deprecated          | Yes                        |
| Type                | String                     |

![](_page_91_Picture_9.jpeg)

### **Note**

As of MySQL 8.0.35, this option is deprecated and subject to removal in a future MySQL release.

The factor or factors for which FIDO device registration must be performed. This option value must be a single value, or two values separated by commas. Each value must be 2 or 3, so the permitted option values are '2', '3', '2,3' and '3,2'.

For example, an account that requires registration for a 3rd authentication factor invokes the [mysql](#page-77-0) client as follows:

```
mysql --user=user_name --fido-register-factor=3
```

An account that requires registration for a 2nd and 3rd authentication factor invokes the [mysql](#page-77-0) client as follows:

```
mysql --user=user_name --fido-register-factor=2,3
```

If registration is successful, a connection is established. If there is an authentication factor with a pending registration, a connection is placed into pending registration mode when attempting to

connect to the server. In this case, disconnect and reconnect with the correct [--fido-register](#page-91-2)[factor](#page-91-2) value to complete the registration.

Registration is a two step process comprising initiate registration and finish registration steps. The initiate registration step executes this statement:

```
ALTER USER user factor INITIATE REGISTRATION
```

The statement returns a result set containing a 32 byte challenge, the user name, and the relying party ID (see authentication\_fido\_rp\_id).

The finish registration step executes this statement:

```
ALTER USER user factor FINISH REGISTRATION SET CHALLENGE_RESPONSE AS 'auth_string'
```

The statement completes the registration and sends the following information to the server as part of the auth\_string: authenticator data, an optional attestation certificate in X.509 format, and a signature.

The initiate and registration steps must be performed in a single connection, as the challenge received by the client during the initiate step is saved to the client connection handler. Registration would fail if the registration step was performed by a different connection. The [--fido-register](#page-91-2)[factor](#page-91-2) option executes both the initiate and registration steps, which avoids the failure scenario described above and prevents having to execute the ALTER USER initiate and registration statements manually.

The [--fido-register-factor](#page-91-2) option is only available for the [mysql](#page-77-0) client and MySQL Shell. Other MySQL client programs do not support it.

For related information, see Using FIDO Authentication.

<span id="page-92-0"></span>• [--force](#page-92-0), -f

| Command-Line Format | force |
|---------------------|-------|
|---------------------|-------|

Continue even if an SQL error occurs.

<span id="page-92-1"></span>• [--get-server-public-key](#page-92-1)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-101-2)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-92-1).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-92-2"></span>• [--histignore](#page-92-2)

| Command-Line Format | histignore=pattern_list |
|---------------------|-------------------------|

463

A list of one or more colon-separated patterns specifying statements to ignore for logging purposes. These patterns are added to the default pattern list ("\*IDENTIFIED\*:\*PASSWORD\*"). The value specified for this option affects logging of statements written to the history file, and to syslog if the [--syslog](#page-104-0) option is given. For more information, see [Section 6.5.1.3, "mysql Client Logging"](#page-113-0).

<span id="page-93-0"></span>• --host=[host\\_name](#page-93-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

Connect to the MySQL server on the given host.

The [--dns-srv-name](#page-90-0) option takes precedence over the [--host](#page-93-0) option if both are given. [--dns](#page-90-0)[srv-name](#page-90-0) causes connection establishment to use the [mysql\\_real\\_connect\\_dns\\_srv\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect-dns-srv.md) C API function rather than [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md). However, if the connect command is subsequently used at runtime and specifies a host name argument, that host name takes precedence over any [-](#page-90-0) [dns-srv-name](#page-90-0) option given at [mysql](#page-77-0) startup to specify a DNS SRV record.

<span id="page-93-1"></span>• [--html](#page-93-1), -H

| Command-Line Format | html |
|---------------------|------|
|---------------------|------|

### Produce HTML output.

<span id="page-93-2"></span>• [--ignore-spaces](#page-93-2), -i

| Command-Line Format | ignore-spaces |
|---------------------|---------------|
|---------------------|---------------|

Ignore spaces after function names. The effect of this is described in the discussion for the IGNORE\_SPACE SQL mode (see Section 7.1.11, "Server SQL Modes").

<span id="page-93-3"></span>• [--init-command=str](#page-93-3)

| Command-Line Format | init-command=str |
|---------------------|------------------|

Single SQL statement to execute after connecting to the server. If auto-reconnect is enabled, the statement is executed again after reconnection occurs.

<span id="page-93-4"></span>• [--line-numbers](#page-93-4)

<span id="page-93-5"></span>

| Command-Line Format | line-numbers      |
|---------------------|-------------------|
| Disabled by         | skip-line-numbers |

| Default Value | empty string |
|---------------|--------------|
|---------------|--------------|

This option affects the client-side LOCAL capability for LOAD DATA operations. It specifies the directory in which files named in LOAD DATA LOCAL statements must be located. The effect of [-](#page-93-5) [load-data-local-dir](#page-93-5) depends on whether LOCAL data loading is enabled or disabled:

- If LOCAL data loading is enabled, either by default in the MySQL client library or by specifying [-](#page-94-0) [local-infile\[=1\]](#page-94-0), the [--load-data-local-dir](#page-93-5) option is ignored.
- If LOCAL data loading is disabled, either by default in the MySQL client library or by specifying [-](#page-94-0) [local-infile=0](#page-94-0), the [--load-data-local-dir](#page-93-5) option applies.

When [--load-data-local-dir](#page-93-5) applies, the option value designates the directory in which local data files must be located. Comparison of the directory path name and the path name of files to be loaded is case-sensitive regardless of the case sensitivity of the underlying file system. If the option value is the empty string, it names no directory, with the result that no files are permitted for local data loading.

For example, to explicitly disable local data loading except for files located in the /my/local/data directory, invoke [mysql](#page-77-0) like this:

```
mysql --local-infile=0 --load-data-local-dir=/my/local/data
```

When both [--local-infile](#page-94-0) and [--load-data-local-dir](#page-93-5) are given, the order in which they are given does not matter.

Successful use of LOCAL load operations within [mysql](#page-77-0) also requires that the server permits local loading; see Section 8.1.6, "Security Considerations for LOAD DATA LOCAL"

The [--load-data-local-dir](#page-93-5) option was added in MySQL 8.0.21.

<span id="page-94-0"></span>• [--local-infile\[={0|1}\]](#page-94-0)

| Command-Line Format | local-infile[={0 1}] |
|---------------------|----------------------|
| Type                | Boolean              |
| Default Value       | FALSE                |

By default, LOCAL capability for LOAD DATA is determined by the default compiled into the MySQL client library. To enable or disable LOCAL data loading explicitly, use the [--local-infile](#page-94-0) option. When given with no value, the option enables LOCAL data loading. When given as [--local](#page-94-0)[infile=0](#page-94-0) or [--local-infile=1](#page-94-0), the option disables or enables LOCAL data loading.

If LOCAL capability is disabled, the [--load-data-local-dir](#page-93-5) option can be used to permit restricted local loading of files located in a designated directory.

Successful use of LOCAL load operations within [mysql](#page-77-0) also requires that the server permits local loading; see Section 8.1.6, "Security Considerations for LOAD DATA LOCAL"

<span id="page-94-1"></span>• [--login-path=](#page-94-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-95-0"></span>• [--max-allowed-packet=](#page-95-0)value

| Command-Line Format | max-allowed-packet=value |
|---------------------|--------------------------|
| Type                | Numeric                  |
| Default Value       | 16777216                 |

The maximum size of the buffer for client/server communication. The default is 16MB, the maximum is 1GB.

<span id="page-95-1"></span>• [--max-join-size=](#page-95-1)value

| Command-Line Format | max-join-size=value |
|---------------------|---------------------|
| Type                | Numeric             |
| Default Value       | 1000000             |

The automatic limit for rows in a join when using [--safe-updates](#page-101-0). (Default value is 1,000,000.)

<span id="page-95-2"></span>• [--named-commands](#page-95-2), -G

| Command-Line Format | named-commands      |
|---------------------|---------------------|
| Disabled by         | skip-named-commands |

Enable named [mysql](#page-77-0) commands. Long-format commands are permitted, not just short-format commands. For example, quit and \q both are recognized. Use [--skip-named-commands](#page-95-2) to disable named commands. See [Section 6.5.1.2, "mysql Client Commands"](#page-106-0).

<span id="page-95-3"></span>• [--net-buffer-length=](#page-95-3)value

| Command-Line Format | net-buffer-length=value |
|---------------------|-------------------------|
| Type                | Numeric                 |
| Default Value       | 16384                   |

The buffer size for TCP/IP and socket communication. (Default value is 16KB.)

<span id="page-95-4"></span>• [--network-namespace=](#page-95-4)name

| Command-Line Format | network-namespace=name |
|---------------------|------------------------|
| Type                | String                 |

The network namespace to use for TCP/IP connections. If omitted, the connection uses the default (global) namespace. For information about network namespaces, see Section 7.1.14, "Network Namespace Support".

This option was added in MySQL 8.0.22. It is available only on platforms that implement network namespace support.

<span id="page-95-5"></span>• [--no-auto-rehash](#page-83-0), -A

| Command-Line Format | no-auto-rehash |
|---------------------|----------------|
| Deprecated          | Yes            |

This has the same effect as --skip-auto-rehash. See the description for [--auto-rehash](#page-83-0).

<span id="page-96-0"></span>• [--no-beep](#page-96-0), -b

| Command-Line Format | no-beep |
|---------------------|---------|
|---------------------|---------|

Do not beep when errors occur.

<span id="page-96-1"></span>• [--no-defaults](#page-96-1)

| Command-Line Format | no-defaults |
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-96-1) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-96-1) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-96-2"></span>• [--one-database](#page-96-2), -o

| Command-Line Format | one-database |
|---------------------|--------------|
|---------------------|--------------|

Ignore statements except those that occur while the default database is the one named on the command line. This option is rudimentary and should be used with care. Statement filtering is based only on USE statements.

Initially, [mysql](#page-77-0) executes statements in the input because specifying a database db\_name on the command line is equivalent to inserting USE db\_name at the beginning of the input. Then, for each USE statement encountered, [mysql](#page-77-0) accepts or rejects following statements depending on whether the database named is the one on the command line. The content of the statements is immaterial.

Suppose that [mysql](#page-77-0) is invoked to process this set of statements:

```
DELETE FROM db2.t2;
USE db2;
DROP TABLE db1.t1;
CREATE TABLE db1.t1 (i INT);
USE db1;
INSERT INTO t1 (i) VALUES(1);
CREATE TABLE db2.t1 (j INT);
```

If the command line is [mysql --force --one-database db1](#page-77-0), [mysql](#page-77-0) handles the input as follows:

- The DELETE statement is executed because the default database is db1, even though the statement names a table in a different database.
- The DROP TABLE and CREATE TABLE statements are not executed because the default database is not db1, even though the statements name a table in db1.

- The INSERT and CREATE TABLE statements are executed because the default database is db1, even though the CREATE TABLE statement names a table in a different database.
- <span id="page-97-0"></span>• [--pager\[=](#page-97-0)command]

| Command-Line Format | pager[=command] |
|---------------------|-----------------|
| Disabled by         | skip-pager      |
| Type                | String          |

Use the given command for paging query output. If the command is omitted, the default pager is the value of your PAGER environment variable. Valid pagers are less, more, cat [> filename], and so forth. This option works only on Unix and only in interactive mode. To disable paging, use [-](#page-97-0) [skip-pager](#page-97-0). [Section 6.5.1.2, "mysql Client Commands",](#page-106-0) discusses output paging further.

<span id="page-97-1"></span>• [--password\[=](#page-97-1)password], -p[password]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysql](#page-77-0) prompts for one. If given, there must be no space between [-](#page-97-1) [password=](#page-97-1) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysql](#page-77-0) should not prompt for one, use the [-](#page-97-1) [skip-password](#page-97-1) option.

<span id="page-97-2"></span>• [--password1\[=](#page-97-2)pass\_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysql](#page-77-0) prompts for one. If given, there must be no space between [--password1=](#page-97-2) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysql](#page-77-0) should not prompt for one, use the [-](#page-97-2) [skip-password1](#page-97-2) option.

[--password1](#page-97-2) and [--password](#page-97-1) are synonymous, as are [--skip-password1](#page-97-2) and [--skip](#page-97-1)[password](#page-97-1).

<span id="page-97-3"></span>• [--password2\[=](#page-97-3)pass\_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-97-2); see the description of that option for details.

### <span id="page-98-0"></span>• [--password3\[=](#page-98-0)pass\_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-97-2); see the description of that option for details.

<span id="page-98-1"></span>• [--pipe](#page-98-1), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-98-2"></span>• [--plugin-authentication-kerberos-client-mode=](#page-98-2)value

| Command-Line Format | plugin-authentication-kerberos<br>client-mode |
|---------------------|-----------------------------------------------|
| Type                | String                                        |
| Default Value       | SSPI                                          |
| Valid Values        | GSSAPI                                        |
|                     | SSPI                                          |

On Windows, the authentication\_kerberos\_client authentication plugin supports this plugin option. It provides two possible values that the client user can set at runtime: SSPI and GSSAPI.

The default value for the client-side plugin option uses Security Support Provider Interface (SSPI), which is capable of acquiring credentials from the Windows in-memory cache. Alternatively, the client user can select a mode that supports Generic Security Service Application Program Interface (GSSAPI) through the MIT Kerberos library on Windows. GSSAPI is capable of acquiring cached credentials previously generated by using the kinit command.

For more information, see Commands for Windows Clients in GSSAPI Mode.

<span id="page-98-3"></span>• [--plugin-dir=](#page-98-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-88-5) option is used to specify an authentication plugin but [mysql](#page-77-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-98-4"></span>• --port=[port\\_num](#page-98-4), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 469<br>3306   |

### <span id="page-99-1"></span>• [--print-defaults](#page-99-1)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-99-2"></span>• --prompt=[format\\_str](#page-99-2)

| Command-Line Format | prompt=format_str |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | mysql>            |

Set the prompt to the specified format. The default is mysql>. The special sequences that the prompt can contain are described in [Section 6.5.1.2, "mysql Client Commands"](#page-106-0).

<span id="page-99-3"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-99-3)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see [Section 6.2.7, "Connection Transport Protocols".](#page-31-0)

<span id="page-99-0"></span>• [--quick](#page-99-0), -q

| Command-Line Format | quick |
|---------------------|-------|

Do not cache each query result, print each row as it is received. This may slow down the server if the output is suspended. With this option, [mysql](#page-77-0) does not use the history file.

By default, [mysql](#page-77-0) fetches all result rows before producing any output; while storing these, it calculates a running maximum column length from the actual value of each column in succession. When printing the output, it uses this maximum to format it. When --quick is specified, [mysql](#page-77-0) does not have the rows for which to calculate the length before starting, and so uses the maximum length. In the following example, table t1 has a single column of type BIGINT and containing 4 rows. The default output is 9 characters wide; this width is equal the maximum number of characters in any of the column values in the rows returned (5), plus 2 characters each for the spaces used as padding and the | characters used as column delimiters). The output when using the - quick option is 25 characters wide; this is equal to the number of characters needed to represent -9223372036854775808, which is the longest possible value that can be stored in a (signed)

BIGINT column, or 19 characters, plus the 4 characters used for padding and column delimiters. The difference can be seen here:

```
$> mysql -t test -e "SELECT * FROM t1"
+-------+
| c1 |
+-------+
| 100 |
| 1000 |
| 10000 |
| 10 |
+-------+
$> mysql --quick -t test -e "SELECT * FROM t1"
+----------------------+
| c1 |
+----------------------+
| 100 |
| 1000 |
| 10000 |
| 10 |
+----------------------+
```

<span id="page-100-0"></span>• [--raw](#page-100-0), -r

| Command-Line Format | raw |
|---------------------|-----|

For tabular output, the "boxing" around columns enables one column value to be distinguished from another. For nontabular output (such as is produced in batch mode or when the [--batch](#page-83-2) or [-](#page-102-2) [silent](#page-102-2) option is given), special characters are escaped in the output so they can be identified easily. Newline, tab, NUL, and backslash are written as \n, \t, \0, and \\. The [--raw](#page-100-0) option disables this character escaping.

The following example demonstrates tabular versus nontabular output and the use of raw mode to disable escaping:

```
% mysql
mysql> SELECT CHAR(92);
+----------+
| CHAR(92) |
+----------+
| \ |
+----------+
% mysql -s
mysql> SELECT CHAR(92);
CHAR(92)
% mysql -s -r
mysql> SELECT CHAR(92);
CHAR(92)
\
```

<span id="page-100-1"></span>• [--reconnect](#page-100-1)

| Command-Line Format | reconnect      |
|---------------------|----------------|
| Disabled by         | skip-reconnect |

If the connection to the server is lost, automatically try to reconnect. A single reconnect attempt is made each time the connection is lost. To suppress reconnection behavior, use [--skip](#page-100-1)[reconnect](#page-100-1).

<span id="page-101-0"></span>• [--safe-updates](#page-101-0), [--i-am-a-dummy](#page-101-0), -U

| Command-Line Format | safe-updates |
|---------------------|--------------|
|                     | i-am-a-dummy |
| Type                | Boolean      |
| Default Value       | FALSE        |

If this option is enabled, UPDATE and DELETE statements that do not use a key in the WHERE clause or a LIMIT clause produce an error. In addition, restrictions are placed on SELECT statements that produce (or are estimated to produce) very large result sets. If you have set this option in an option file, you can use [--skip-safe-updates](#page-101-0) on the command line to override it. For more information about this option, see [Using Safe-Updates Mode \(--safe-updates\)](#page-119-0).

<span id="page-101-1"></span>• [--select-limit=](#page-101-1)value

| Command-Line Format | select-limit=value |
|---------------------|--------------------|
| Type                | Numeric            |
| Default Value       | 1000               |

The automatic limit for SELECT statements when using [--safe-updates](#page-101-0). (Default value is 1,000.)

<span id="page-101-2"></span>• [--server-public-key-path=](#page-101-2)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-101-2)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-92-1).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-101-3"></span>• [--shared-memory-base-name=](#page-101-3)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive. 472

<span id="page-102-0"></span>• [--show-warnings](#page-102-0)

| Command-Line Format | show-warnings |
|---------------------|---------------|
|---------------------|---------------|

Cause warnings to be shown after each statement if there are any. This option applies to interactive and batch mode.

<span id="page-102-1"></span>• [--sigint-ignore](#page-102-1)

| Command-Line Format | sigint-ignore |
|---------------------|---------------|
|---------------------|---------------|

Ignore SIGINT signals (typically the result of typing **Control+C**).

Without this option, typing **Control+C** interrupts the current statement if there is one, or cancels any partial input line otherwise.

<span id="page-102-2"></span>• [--silent](#page-102-2), -s

| Command-Line Format | silent |
|---------------------|--------|
|---------------------|--------|

Silent mode. Produce less output. This option can be given multiple times to produce less and less output.

This option results in nontabular output format and escaping of special characters. Escaping may be disabled by using raw mode; see the description for the [--raw](#page-100-0) option.

<span id="page-102-3"></span>• [--skip-column-names](#page-102-3), -N

```
Command-Line Format --skip-column-names
```

Do not write column names in results. Use of this option causes the output to be right-aligned, as shown here:

```
$> echo "SELECT * FROM t1" | mysql -t test
+-------+
| c1 |
+-------+
| a,c,d |
| c |
+-------+
$> echo "SELECT * FROM t1" | ./mysql -uroot -Nt test
+-------+
| a,c,d |
| c |
+-------+
```

<span id="page-102-4"></span>• [--skip-line-numbers](#page-102-4), -L

```
Command-Line Format --skip-line-numbers
```

Do not write line numbers for errors. Useful when you want to compare result files that include error messages. 473 <span id="page-103-1"></span>• [--skip-system-command](#page-103-1)

| Command-Line Format | skip-system-command |
|---------------------|---------------------|
|---------------------|---------------------|

Disables the system (\!) command. Equivalent to [--system-command=OFF](#page-104-1).

<span id="page-103-2"></span>• [--socket=](#page-103-2)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
| Type                | String                       |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-103-0"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See [Command Options for Encrypted Connections](#page-11-1).

<span id="page-103-3"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-103-3)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-103-3) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-103-3) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_103_Picture_17.jpeg)

### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-103-3) is OFF. In this case, setting [--ssl-fips-mode](#page-103-3) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

### <span id="page-104-0"></span>• [--syslog](#page-104-0), -j

| Command-Line Format | syslog |
|---------------------|--------|
|---------------------|--------|

This option causes [mysql](#page-77-0) to send interactive statements to the system logging facility. On Unix, this is syslog; on Windows, it is the Windows Event Log. The destination where logged messages appear is system dependent. On Linux, the destination is often the /var/log/messages file.

Here is a sample of output generated on Linux by using --syslog. This output is formatted for readability; each logged message actually takes a single line.

```
Mar 7 12:39:25 myhost MysqlClient[20824]:
 SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
 DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
Mar 7 12:39:28 myhost MysqlClient[20824]:
 SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
 DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'
```

For more information, see [Section 6.5.1.3, "mysql Client Logging"](#page-113-0).

<span id="page-104-1"></span>• [--system-command\[={ON|OFF}\]](#page-104-1)

| Command-Line Format | system-command[={ON OFF}] |
|---------------------|---------------------------|
| Disabled by         | skip-system-command       |
| Type                | Boolean                   |
| Default Value       | ON                        |

Enable or disable the system (\!) command. When this option is disabled, either by --systemcommand=OFF or by [--skip-system-command](#page-103-1), the system command is rejected with an error.

(MySQL 8.0.43 and later:) [--commands](#page-85-4), when disabled (set to FALSE), causes the server to disregard any setting for this option.

<span id="page-104-2"></span>• [--table](#page-104-2), -t

| Command-Line Format | table |
|---------------------|-------|

Display output in table format. This is the default for interactive use, but can be used to produce table output in batch mode.

<span id="page-104-3"></span>• --tee=[file\\_name](#page-104-3)

| Command-Line Format | tee=file_name |
|---------------------|---------------|
| Type                | File name     |

Append a copy of output to the given file. This option works only in interactive mode. [Section 6.5.1.2,](#page-106-0) ["mysql Client Commands"](#page-106-0), discusses tee files further.

<span id="page-104-4"></span>• [--tls-ciphersuites=](#page-104-4)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option

depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-105-1"></span>• [--tls-version=](#page-105-1)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-105-2"></span>• [--unbuffered](#page-105-2), -n

| Command-Line Format | unbuffered |
|---------------------|------------|
|---------------------|------------|

Flush the buffer after each query.

<span id="page-105-0"></span>• --user=[user\\_name](#page-105-0), -u user\_name

| Command-Line Format | user=user_name |
|---------------------|----------------|
| Type                | String         |

The user name of the MySQL account to use for connecting to the server.

<span id="page-105-3"></span>• [--verbose](#page-105-3), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Produce more output about what the program does. This option can be given multiple times to produce more and more output. (For example, -v -v -v produces table output format even in batch mode.)

<span id="page-105-4"></span>• [--version](#page-105-4), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

<span id="page-105-5"></span>• [--vertical](#page-105-5), -E

| Command-Line Format | vertical |
|---------------------|----------|

Print query output rows vertically (one line per column value). Without this option, you can specify vertical output for individual statements by terminating them with \G.

<span id="page-105-6"></span>• [--wait](#page-105-6), -w

| Command-Line Format | wait |
|---------------------|------|
|                     |      |

If the connection cannot be established, wait and retry instead of aborting.

<span id="page-106-1"></span>• [--xml](#page-106-1), -X

| Command-Line Format | xml |
|---------------------|-----|

### Produce XML output.

```
<field name="column_name">NULL</field>
```

The output when [--xml](#page-106-1) is used with [mysql](#page-77-0) matches that of [mysqldump](#page-152-0) [--xml](#page-180-0). See [Section 6.5.4,](#page-152-0) ["mysqldump — A Database Backup Program",](#page-152-0) for details.

The XML output also uses an XML namespace, as shown here:

```
$> mysql --xml -uroot -e "SHOW VARIABLES LIKE 'version%'"
<?xml version="1.0"?>
<resultset statement="SHOW VARIABLES LIKE 'version%'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<row>
<field name="Variable_name">version</field>
<field name="Value">5.0.40-debug</field>
</row>
<row>
<field name="Variable_name">version_comment</field>
<field name="Value">Source distribution</field>
</row>
<row>
<field name="Variable_name">version_compile_machine</field>
<field name="Value">i686</field>
</row>
<row>
<field name="Variable_name">version_compile_os</field>
<field name="Value">suse-linux-gnu</field>
</row>
</resultset>
```

<span id="page-106-2"></span>• [--zstd-compression-level=](#page-106-2)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.

## <span id="page-106-0"></span>**6.5.1.2 mysql Client Commands**

[mysql](#page-77-0) sends each SQL statement that you issue to the server to be executed. There is also a set of commands that [mysql](#page-77-0) itself interprets. For a list of these commands, type help or \h at the mysql> prompt:

```
mysql> help
List of all MySQL commands:
Note that all text commands must be first on line and end with ';'
? (\?) Synonym for `help'.
clear (\c) Clear the current input statement.
connect (\r) Reconnect to the server. Optional arguments are db and host.
delimiter (\d) Set statement delimiter.
edit (\e) Edit command with $EDITOR.
ego (\G) Send command to mysql server, display result vertically.
exit (\q) Exit mysql. Same as quit.
go (\g) Send command to mysql server.
help (\h) Display this help.
nopager (\n) Disable pager, print to stdout.
notee (\t) Don't write into outfile.
pager (\P) Set PAGER [to_pager]. Print the query results via PAGER.
print (\p) Print current command.
prompt (\R) Change your mysql prompt.
quit (\q) Quit mysql.
rehash (\#) Rebuild completion hash.
source (\.) Execute an SQL script file. Takes a file name as an argument.
status (\s) Get status information from the server.
system (\!) Execute a system shell command.
tee (\T) Set outfile [to_outfile]. Append everything into given
 outfile.
use (\u) Use another database. Takes database name as argument.
charset (\C) Switch to another charset. Might be needed for processing
 binlog with multi-byte charsets.
warnings (\W) Show warnings after every statement.
nowarning (\w) Don't show warnings after every statement.
resetconnection(\x) Clean session context.
query_attributes Sets string parameters (name1 value1 name2 value2 ...)
for the next query to pick up.
ssl_session_data_print Serializes the current SSL session data to stdout 
or file.
For server side help, type 'help contents'
```

If [mysql](#page-77-0) is invoked with the [--binary-mode](#page-84-0) option, all [mysql](#page-77-0) commands are disabled except charset and delimiter in noninteractive mode (for input piped to [mysql](#page-77-0) or loaded using the source command). Beginning with MySQL 8.0.43, the [--commands](#page-85-4) option can be used to enable or disable all commands except /C, delimiter, and use.

Each command has both a long and short form. The long form is not case-sensitive; the short form is. The long form can be followed by an optional semicolon terminator, but the short form should not.

The use of short-form commands within multiple-line /\* ... \*/ comments is not supported. Shortform commands do work within single-line /\*! ... \*/ version comments, as do /\*+ ... \*/ optimizer-hint comments, which are stored in object definitions. If there is a concern that optimizerhint comments may be stored in object definitions so that dump files when reloaded with mysql would result in execution of such commands, either invoke [mysql](#page-77-0) with the [--binary-mode](#page-84-0) option or use a reload client other than [mysql](#page-77-0).

• help [arg], \h [arg], \? [arg], ? [arg]

Display a help message listing the available [mysql](#page-77-0) commands.

If you provide an argument to the help command, [mysql](#page-77-0) uses it as a search string to access server-side help from the contents of the MySQL Reference Manual. For more information, see [Section 6.5.1.4, "mysql Client Server-Side Help"](#page-115-0).

• charset charset\_name, \C charset\_name

Change the default character set and issue a SET NAMES statement. This enables the character set to remain synchronized on the client and server if [mysql](#page-77-0) is run with auto-reconnect enabled (which is not recommended), because the specified character set is used for reconnects.

• clear, \c

Clear the current input. Use this if you change your mind about executing the statement that you are entering.

• connect [db\_name [host\_name]], \r [db\_name [host\_name]]

Reconnect to the server. The optional database name and host name arguments may be given to specify the default database or the host where the server is running. If omitted, the current values are used.

If the connect command specifies a host name argument, that host takes precedence over any [-](#page-90-0) [dns-srv-name](#page-90-0) option given at [mysql](#page-77-0) startup to specify a DNS SRV record.

• delimiter str, \d str

Change the string that [mysql](#page-77-0) interprets as the separator between SQL statements. The default is the semicolon character (;).

The delimiter string can be specified as an unquoted or quoted argument on the delimiter command line. Quoting can be done with either single quote ('), double quote ("), or backtick (`) characters. To include a quote within a quoted string, either quote the string with a different quote character or escape the quote with a backslash (\) character. Backslash should be avoided outside of quoted strings because it is the escape character for MySQL. For an unquoted argument, the delimiter is read up to the first space or end of line. For a quoted argument, the delimiter is read up to the matching quote on the line.

[mysql](#page-77-0) interprets instances of the delimiter string as a statement delimiter anywhere it occurs, except within quoted strings. Be careful about defining a delimiter that might occur within other words. For example, if you define the delimiter as X, it is not possible to use the word INDEX in statements. [mysql](#page-77-0) interprets this as INDE followed by the delimiter X.

When the delimiter recognized by [mysql](#page-77-0) is set to something other than the default of ;, instances of that character are sent to the server without interpretation. However, the server itself still interprets ; as a statement delimiter and processes statements accordingly. This behavior on the server side comes into play for multiple-statement execution (see [Multiple Statement Execution Support](https://dev.mysql.com/doc/c-api/8.0/en/c-api-multiple-queries.md)), and for parsing the body of stored procedures and functions, triggers, and events (see Section 27.1, "Defining Stored Programs").

• edit, \e

Edit the current input statement. [mysql](#page-77-0) checks the values of the EDITOR and VISUAL environment variables to determine which editor to use. The default editor is vi if neither variable is set.

The edit command works only in Unix.

• ego, \G

Send the current statement to the server to be executed and display the result using vertical format.

• exit, \q

Exit [mysql](#page-77-0).

• go, \g

Send the current statement to the server to be executed.

• nopager, \n

Disable output paging. See the description for pager.

The nopager command works only in Unix.

• notee, \t

Disable output copying to the tee file. See the description for tee.

• nowarning, \w

Disable display of warnings after each statement.

• pager [command], \P [command]

Enable output paging. By using the [--pager](#page-97-0) option when you invoke [mysql](#page-77-0), it is possible to browse or search query results in interactive mode with Unix programs such as less, more, or any other similar program. If you specify no value for the option, [mysql](#page-77-0) checks the value of the PAGER environment variable and sets the pager to that. Pager functionality works only in interactive mode.

Output paging can be enabled interactively with the pager command and disabled with nopager. The command takes an optional argument; if given, the paging program is set to that. With no argument, the pager is set to the pager that was set on the command line, or stdout if no pager was specified.

Output paging works only in Unix because it uses the popen() function, which does not exist on Windows. For Windows, the tee option can be used instead to save query output, although it is not as convenient as pager for browsing output in some situations.

• print, \p

Print the current input statement without executing it.

• prompt [str], \R [str]

Reconfigure the [mysql](#page-77-0) prompt to the given string. The special character sequences that can be used in the prompt are described later in this section.

If you specify the prompt command with no argument, [mysql](#page-77-0) resets the prompt to the default of mysql>.

• query\_attributes name value [name value ...]

Define query attributes that apply to the next query sent to the server. For discussion of the purpose and use of query attributes, see Section 11.6, "Query Attributes".

The query\_attributes command follows these rules:

- The format and quoting rules for attribute names and values are the same as for the delimiter command.
- The command permits up to 32 attribute name/value pairs. Names and values may be up to 1024 characters long. If a name is given without a value, an error occurs.
- If multiple query\_attributes commands are issued prior to query execution, only the last command applies. After sending the query, [mysql](#page-77-0) clears the attribute set.
- If multiple attributes are defined with the same name, attempts to retrieve the attribute value have an undefined result.
- An attribute defined with an empty name cannot be retrieved by name.

- If a reconnect occurs while [mysql](#page-77-0) executes the query, [mysql](#page-77-0) restores the attributes after reconnecting so the query can be executed again with the same attributes.
- quit, \q

Exit [mysql](#page-77-0).

• rehash, \#

Rebuild the completion hash that enables database, table, and column name completion while you are entering statements. (See the description for the [--auto-rehash](#page-83-0) option.)

• resetconnection, \x

Reset the connection to clear the session state. This includes clearing any current query attributes defined using the query\_attributes command.

Resetting a connection has effects similar to [mysql\\_change\\_user\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-change-user.md) or an auto-reconnect except that the connection is not closed and reopened, and re-authentication is not done. See [mysql\\_change\\_user\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-change-user.md), and [Automatic Reconnection Control.](https://dev.mysql.com/doc/c-api/8.0/en/c-api-auto-reconnect.md)

This example shows how resetconnection clears a value maintained in the session state:

```
mysql> SELECT LAST_INSERT_ID(3);
+-------------------+
| LAST_INSERT_ID(3) |
+-------------------+
| 3 |
+-------------------+
mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
| 3 |
+------------------+
mysql> resetconnection;
mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
| 0 |
+------------------+
```

• source file\_name, \. file\_name

Read the named file and executes the statements contained therein. On Windows, specify path name separators as / or \\.

Quote characters are taken as part of the file name itself. For best results, the name should not include space characters.

• ssl\_session\_data\_print [file\_name]

Fetches, serializes, and optionally stores the session data of a successful connection. The optional file name and arguments may be given to specify the file to store serialized session data. If omitted, the session data is printed to stdout.

If the MySQL session is configured for reuse, session data from the file is deserialized and supplied to the connect command to reconnect. When the session is reused successfully, the status command contains a row showing SSL session reused: true while the client remains reconnected to the server.

• status, \s

Provide status information about the connection and the server you are using. If you are running with [--safe-updates](#page-101-0) enabled, status also prints the values for the [mysql](#page-77-0) variables that affect your queries.

• system command, \! command

Execute the given command using your default command interpreter.

Prior to MySQL 8.0.19, the system command works only in Unix. As of 8.0.19, it also works on Windows.

In MySQL 8.0.40 and later, this command can be disabled by starting the client with [--system](#page-104-1)[command=OFF](#page-104-1) or [--skip-system-command](#page-103-1).

• tee [file\_name], \T [file\_name]

By using the [--tee](#page-104-3) option when you invoke [mysql](#page-77-0), you can log statements and their output. All the data displayed on the screen is appended into a given file. This can be very useful for debugging purposes also. [mysql](#page-77-0) flushes results to the file after each statement, just before it prints its next prompt. Tee functionality works only in interactive mode.

You can enable this feature interactively with the tee command. Without a parameter, the previous file is used. The tee file can be disabled with the notee command. Executing tee again re-enables logging.

• use db\_name, \u db\_name

Use db\_name as the default database.

• warnings, \W

Enable display of warnings after each statement (if there are any).

Here are a few tips about the pager command:

• You can use it to write to a file and the results go only to the file:

```
mysql> pager cat > /tmp/log.txt
```

You can also pass any options for the program that you want to use as your pager:

```
mysql> pager less -n -i -S
```

• In the preceding example, note the -S option. You may find it very useful for browsing wide query results. Sometimes a very wide result set is difficult to read on the screen. The -S option to less can make the result set much more readable because you can scroll it horizontally using the leftarrow and right-arrow keys. You can also use -S interactively within less to switch the horizontalbrowse mode on and off. For more information, read the less manual page:

```
man less
```

• The -F and -X options may be used with less to cause it to exit if output fits on one screen, which is convenient when no scrolling is necessary:

```
mysql> pager less -n -i -S -F -X
```

• You can specify very complex pager commands for handling query output:

```
mysql> pager cat | tee /dr1/tmp/res.txt \
 | tee /dr2/tmp/res2.txt | less -n -i -S
```

In this example, the command would send query results to two files in two different directories on two different file systems mounted on /dr1 and /dr2, yet still display the results onscreen using less.

You can also combine the tee and pager functions. Have a tee file enabled and pager set to less, and you are able to browse the results using the less program and still have everything appended into a file the same time. The difference between the Unix tee used with the pager command and the [mysql](#page-77-0) built-in tee command is that the built-in tee works even if you do not have the Unix tee available. The built-in tee also logs everything that is printed on the screen, whereas the Unix tee used with pager does not log quite that much. Additionally, tee file logging can be turned on and off interactively from within [mysql](#page-77-0). This is useful when you want to log some queries to a file, but not others.

The prompt command reconfigures the default mysql> prompt. The string for defining the prompt can contain the following special sequences.

| Option | Description                                                                                       |
|--------|---------------------------------------------------------------------------------------------------|
| \C     | The current connection identifier                                                                 |
| \c     | A counter that increments for each statement you<br>issue                                         |
| \D     | The full current date                                                                             |
| \d     | The default database                                                                              |
| \h     | The server host                                                                                   |
| \l     | The current delimiter                                                                             |
| \m     | Minutes of the current time                                                                       |
| \n     | A newline character                                                                               |
| \O     | The current month in three-letter format (Jan, Feb,<br>…)                                         |
| \o     | The current month in numeric format                                                               |
| \P     | am/pm                                                                                             |
| \p     | The current TCP/IP port or socket file                                                            |
| \R     | The current time, in 24-hour military time (0–23)                                                 |
| \r     | The current time, standard 12-hour time (1–12)                                                    |
| \S     | Semicolon                                                                                         |
| \s     | Seconds of the current time                                                                       |
| \T     | Print an asterisk (*) if the current session is inside<br>a transaction block (from MySQL 8.0.28) |
| \t     | A tab character                                                                                   |
| \U     | Your full user_name@host_name account name                                                        |
| \u     | Your user name                                                                                    |
| \v     | The server version                                                                                |
| \w     | The current day of the week in three-letter format<br>(Mon, Tue, …)                               |
| \Y     | The current year, four digits                                                                     |
| \y     | The current year, two digits                                                                      |
| \_     | A space                                                                                           |
| \      | A space (a space follows the backslash)                                                           |
| \'     | Single quote                                                                                      |
|        |                                                                                                   |

| Option | Description                     |
|--------|---------------------------------|
| \"     | Double quote                    |
| \\     | A literal \ backslash character |
| \x     | x, for any "x" not listed above |

You can set the prompt in several ways:

• Use an environment variable. You can set the MYSQL\_PS1 environment variable to a prompt string. For example:

```
export MYSQL_PS1="(\u@\h) [\d]> "
```

• Use a command-line option. You can set the [--prompt](#page-99-2) option on the command line to [mysql](#page-77-0). For example:

```
$> mysql --prompt="(\u@\h) [\d]> "
(user@host) [database]>
```

• Use an option file. You can set the prompt option in the [mysql] group of any MySQL option file, such as /etc/my.cnf or the .my.cnf file in your home directory. For example:

```
[mysql]
prompt=(\\u@\\h) [\\d]>\\_
```

In this example, note that the backslashes are doubled. If you set the prompt using the prompt option in an option file, it is advisable to double the backslashes when using the special prompt options. There is some overlap in the set of permissible prompt options and the set of special escape sequences that are recognized in option files. (The rules for escape sequences in option files are listed in Section 6.2.2.2, "Using Option Files".) The overlap may cause you problems if you use single backslashes. For example, \s is interpreted as a space rather than as the current seconds value. The following example shows how to define a prompt within an option file to include the current time in hh:mm:ss> format:

```
[mysql]
prompt="\\r:\\m:\\s> "
```

• Set the prompt interactively. You can change your prompt interactively by using the prompt (or \R) command. For example:

```
mysql> prompt (\u@\h) [\d]>\_
PROMPT set to '(\u@\h) [\d]>\_'
(user@host) [database]>
(user@host) [database]> prompt
Returning to default PROMPT of mysql>
mysql>
```

# <span id="page-113-0"></span>**6.5.1.3 mysql Client Logging**

The [mysql](#page-77-0) client can do these types of logging for statements executed interactively:

- On Unix, [mysql](#page-77-0) writes the statements to a history file. By default, this file is named .mysql\_history in your home directory. To specify a different file, set the value of the MYSQL\_HISTFILE environment variable.
- On all platforms, if the --syslog option is given, [mysql](#page-77-0) writes the statements to the system logging facility. On Unix, this is syslog; on Windows, it is the Windows Event Log. The destination where logged messages appear is system dependent. On Linux, the destination is often the /var/log/ messages file.

The following discussion describes characteristics that apply to all logging types and provides information specific to each logging type.

• [How Logging Occurs](#page-114-0)

- [Controlling the History File](#page-114-1)
- [syslog Logging Characteristics](#page-115-1)

### <span id="page-114-0"></span>**How Logging Occurs**

For each enabled logging destination, statement logging occurs as follows:

- Statements are logged only when executed interactively. Statements are noninteractive, for example, when read from a file or a pipe. It is also possible to suppress statement logging by using the [-](#page-83-2) [batch](#page-83-2) or [--execute](#page-91-1) option.
- Statements are ignored and not logged if they match any pattern in the "ignore" list. This list is described later.
- [mysql](#page-77-0) logs each nonignored, nonempty statement line individually.
- If a nonignored statement spans multiple lines (not including the terminating delimiter), [mysql](#page-77-0) concatenates the lines to form the complete statement, maps newlines to spaces, and logs the result, plus a delimiter.

Consequently, an input statement that spans multiple lines can be logged twice. Consider this input:

```
mysql> SELECT
 -> 'Today is'
 -> ,
 -> CURDATE()
 -> ;
```

In this case, [mysql](#page-77-0) logs the "SELECT", "'Today is'", ",", "CURDATE()", and ";" lines as it reads them. It also logs the complete statement, after mapping SELECT\n'Today is'\n,\nCURDATE() to SELECT 'Today is' , CURDATE(), plus a delimiter. Thus, these lines appear in logged output:

```
SELECT
'Today is'
,
CURDATE()
;
SELECT 'Today is' , CURDATE();
```

[mysql](#page-77-0) ignores for logging purposes statements that match any pattern in the "ignore" list. By default, the pattern list is "\*IDENTIFIED\*:\*PASSWORD\*", to ignore statements that refer to passwords. Pattern matching is not case-sensitive. Within patterns, two characters are special:

- ? matches any single character.
- \* matches any sequence of zero or more characters.

To specify additional patterns, use the [--histignore](#page-92-2) option or set the MYSQL\_HISTIGNORE environment variable. (If both are specified, the option value takes precedence.) The value should be a list of one or more colon-separated patterns, which are appended to the default pattern list.

Patterns specified on the command line might need to be quoted or escaped to prevent your command interpreter from treating them specially. For example, to suppress logging for UPDATE and DELETE statements in addition to statements that refer to passwords, invoke [mysql](#page-77-0) like this:

```
mysql --histignore="*UPDATE*:*DELETE*"
```

### <span id="page-114-1"></span>**Controlling the History File**

The .mysql\_history file should be protected with a restrictive access mode because sensitive information might be written to it, such as the text of SQL statements that contain passwords. See Section 8.1.2.1, "End-User Guidelines for Password Security". Statements in the file are accessible from the [mysql](#page-77-0) client when the **up-arrow** key is used to recall the history. See [Disabling Interactive](#page-118-0) [History](#page-118-0).

If you do not want to maintain a history file, first remove .mysql\_history if it exists. Then use either of the following techniques to prevent it from being created again:

- Set the MYSQL\_HISTFILE environment variable to /dev/null. To cause this setting to take effect each time you log in, put it in one of your shell's startup files.
- Create .mysql\_history as a symbolic link to /dev/null; this need be done only once:

```
ln -s /dev/null $HOME/.mysql_history
```

### <span id="page-115-1"></span>**syslog Logging Characteristics**

If the --syslog option is given, [mysql](#page-77-0) writes interactive statements to the system logging facility. Message logging has the following characteristics.

Logging occurs at the "information" level. This corresponds to the LOG\_INFO priority for syslog on Unix/Linux syslog capability and to EVENTLOG\_INFORMATION\_TYPE for the Windows Event Log. Consult your system documentation for configuration of your logging capability.

Message size is limited to 1024 bytes.

Messages consist of the identifier MysqlClient followed by these values:

• SYSTEM\_USER

The operating system user name (login name) or -- if the user is unknown.

• MYSQL\_USER

The MySQL user name (specified with the [--user](#page-105-0) option) or -- if the user is unknown.

• CONNECTION\_ID:

The client connection identifier. This is the same as the CONNECTION\_ID() function value within the session.

• DB\_SERVER

The server host or -- if the host is unknown.

• DB

The default database or -- if no database has been selected.

• QUERY

The text of the logged statement.

Here is a sample of output generated on Linux by using --syslog. This output is formatted for readability; each logged message actually takes a single line.

```
Mar 7 12:39:25 myhost MysqlClient[20824]:
 SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
 DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
Mar 7 12:39:28 myhost MysqlClient[20824]:
 SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
 DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'
```

## <span id="page-115-0"></span>**6.5.1.4 mysql Client Server-Side Help**

```
mysql> help search_string
```

If you provide an argument to the help command, [mysql](#page-77-0) uses it as a search string to access serverside help from the contents of the MySQL Reference Manual. The proper operation of this command

requires that the help tables in the mysql database be initialized with help topic information (see Section 7.1.17, "Server-Side Help Support").

If there is no match for the search string, the search fails:

```
mysql> help me
Nothing found
Please try to run 'help contents' for a list of all accessible topics
```

Use help contents to see a list of the help categories:

```
mysql> help contents
You asked for help about help category: "Contents"
For more information, type 'help <item>', where <item> is one of the
following categories:
 Account Management
 Administration
 Data Definition
 Data Manipulation
 Data Types
 Functions
 Functions and Modifiers for Use with GROUP BY
 Geographic Features
 Language Structure
 Plugins
 Storage Engines
 Stored Routines
 Table Maintenance
 Transactions
 Triggers
```

If the search string matches multiple items, [mysql](#page-77-0) shows a list of matching topics:

```
mysql> help logs
Many help items for your request exist.
To make a more specific request, please type 'help <item>',
where <item> is one of the following topics:
 SHOW
 SHOW BINARY LOGS
 SHOW ENGINE
 SHOW LOGS
```

Use a topic as the search string to see the help entry for that topic:

```
mysql> help show binary logs
Name: 'SHOW BINARY LOGS'
Description:
Syntax:
SHOW BINARY LOGS
SHOW MASTER LOGS
Lists the binary log files on the server. This statement is used as
part of the procedure described in [purge-binary-logs], that shows how
to determine which logs can be purged.
```

```
mysql> SHOW BINARY LOGS;
+---------------+-----------+-----------+
| Log_name | File_size | Encrypted |
+---------------+-----------+-----------+
| binlog.000015 | 724935 | Yes |
| binlog.000016 | 733481 | Yes |
+---------------+-----------+-----------+
```

The search string can contain the wildcard characters % and \_. These have the same meaning as for pattern-matching operations performed with the LIKE operator. For example, HELP rep% returns a list of topics that begin with rep:

```
mysql> HELP rep%
Many help items for your request exist.
To make a more specific request, please type 'help <item>',
```

```
where <item> is one of the following
topics:
 REPAIR TABLE
 REPEAT FUNCTION
 REPEAT LOOP
 REPLACE
 REPLACE FUNCTION
```