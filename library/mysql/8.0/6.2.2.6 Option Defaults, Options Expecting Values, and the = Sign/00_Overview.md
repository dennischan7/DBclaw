---
source: MySQL 8.0 Reference
title: 00_Overview
---

By convention, long forms of options that assign a value are written with an equals (=) sign, like this:

```
mysql --host=tonfisk --user=jon
```

For options that require a value (that is, not having a default value), the equal sign is not required, and so the following is also valid:

```
mysql --host tonfisk --user jon
```

In both cases, the <code>mysql</code> client attempts to connect to a MySQL server running on the host named "tonfisk" using an account with the user name "jon".

Due to this behavior, problems can occasionally arise when no value is provided for an option that expects one. Consider the following example, where a user connects to a MySQL server running on host tonfisk as user jon:

```
$> mysql --host 85.224.35.45 --user jon
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 8.0.45 Source distribution
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql> SELECT CURRENT_USER();
+----------------+
| CURRENT_USER() |
+----------------+
| jon@% |
+----------------+
1 row in set (0.00 sec)
```

Omitting the required value for one of these option yields an error, such as the one shown here:

```
$> mysql --host 85.224.35.45 --user
mysql: option '--user' requires an argument
```

In this case, [mysql](#page-77-0) was unable to find a value following the [--user](#page-11-0) option because nothing came after it on the command line. However, if you omit the value for an option that is not the last option to be used, you obtain a different error that you may not be expecting:

```
$> mysql --host --user jon
ERROR 2005 (HY000): Unknown MySQL server host '--user' (1)
```

Because [mysql](#page-77-0) assumes that any string following [--host](#page-8-0) on the command line is a host name, [-](#page-8-0) [host](#page-8-0) [--user](#page-11-0) is interpreted as [--host=--user](#page-8-0), and the client attempts to connect to a MySQL server running on a host named "--user".

Options having default values always require an equal sign when assigning a value; failing to do so causes an error. For example, the MySQL server --log-error option has the default value host\_name.err, where host\_name is the name of the host on which MySQL is running. Assume that you are running MySQL on a computer whose host name is "tonfisk", and consider the following invocation of [mysqld\\_safe](#page-37-1):

```
$> mysqld_safe &
[1] 11699
$> 080112 12:53:40 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
080112 12:53:40 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
$>
```

After shutting down the server, restart it as follows:

```
$> mysqld_safe --log-error &
[1] 11699
$> 080112 12:53:40 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
080112 12:53:40 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
$>
```

The result is the same, since [--log-error](#page-40-0) is not followed by anything else on the command line, and it supplies its own default value. (The & character tells the operating system to run MySQL in the background; it is ignored by MySQL itself.) Now suppose that you wish to log errors to a file named my-errors.err. You might try starting the server with --log-error my-errors, but this does not have the intended effect, as shown here:

```
$> mysqld_safe --log-error my-errors &
[1] 31357
$> 080111 22:53:31 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
080111 22:53:32 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
080111 22:53:34 mysqld_safe mysqld from pid file /usr/local/mysql/var/tonfisk.pid ended
[1]+ Done ./mysqld_safe --log-error my-errors
```

The server attempted to start using /usr/local/mysql/var/tonfisk.err as the error log, but then shut down. Examining the last few lines of this file shows the reason:

```
$> tail /usr/local/mysql/var/tonfisk.err
2013-09-24T15:36:22.278034Z 0 [ERROR] Too many arguments (first extra is 'my-errors').
2013-09-24T15:36:22.278059Z 0 [Note] Use --verbose --help to get a list of available options!
2013-09-24T15:36:22.278076Z 0 [ERROR] Aborting
2013-09-24T15:36:22.279704Z 0 [Note] InnoDB: Starting shutdown...
2013-09-24T15:36:23.777471Z 0 [Note] InnoDB: Shutdown completed; log sequence number 2319086
2013-09-24T15:36:23.780134Z 0 [Note] mysqld: Shutdown complete
```

Because the [--log-error](#page-40-0) option supplies a default value, you must use an equal sign to assign a different value to it, as shown here:

```
$> mysqld_safe --log-error=my-errors &
[1] 31437
$> 080111 22:54:15 mysqld_safe Logging to '/usr/local/mysql/var/my-errors.err'.
080111 22:54:15 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
$>
```

Now the server has been started successfully, and is logging errors to the file /usr/local/mysql/ var/my-errors.err.

Similar issues can arise when specifying option values in option files. For example, consider a my.cnf file that contains the following:

```
[mysql]
host
user
```

When the [mysql](#page-77-0) client reads this file, these entries are parsed as [--host](#page-93-0) [--user](#page-105-0) or [--host=-](#page-93-0) [user](#page-93-0), with the result shown here:

```
$> mysql
ERROR 2005 (HY000): Unknown MySQL server host '--user' (1)
```

However, in option files, an equal sign is not assumed. Suppose the my.cnf file is as shown here:

```
[mysql]
user jon
```

Trying to start [mysql](#page-77-0) in this case causes a different error:

```
$> mysql
mysql: unknown option '--user jon'
```

A similar error would occur if you were to write host tonfisk in the option file rather than host=tonfisk. Instead, you must use the equal sign:

```
[mysql]
user=jon
```

Now the login attempt succeeds:

```
$> mysql
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 8.0.45 Source distribution
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql> SELECT USER();
+---------------+
| USER() |
+---------------+
| jon@localhost |
```

```
+---------------+
1 row in set (0.00 sec)
```

This is not the same behavior as with the command line, where the equal sign is not required:

```
$> mysql --user jon --host tonfisk
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 6
Server version: 8.0.45 Source distribution
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql> SELECT USER();
+---------------+
| USER() |
+---------------+
| jon@tonfisk |
+---------------+
1 row in set (0.00 sec)
```

Specifying an option requiring a value without a value in an option file causes the server to abort with an error.

# <span id="page-7-1"></span>**6.2.3 Command Options for Connecting to the Server**

This section describes options supported by most MySQL client programs that control how client programs establish connections to the server, whether connections are encrypted, and whether connections are compressed. These options can be given on the command line or in an option file.

- [Command Options for Connection Establishment](#page-7-0)
- [Command Options for Encrypted Connections](#page-11-1)
- [Command Options for Connection Compression](#page-19-0)

# <span id="page-7-0"></span>**Command Options for Connection Establishment**

This section describes options that control how client programs establish connections to the server. For additional information and examples showing how to use them, see [Section 6.2.4, "Connecting to the](#page-20-0) [MySQL Server Using Command Options"](#page-20-0).

**Table 6.4 Connection-Establishment Option Summary**

| Option Name             | Description                                                                    |
|-------------------------|--------------------------------------------------------------------------------|
| default-auth            | Authentication plugin to use                                                   |
| host                    | Host on which MySQL server is located                                          |
| password                | Password to use when connecting to server                                      |
| password1               | First multifactor authentication password to use<br>when connecting to server  |
| password2               | Second multifactor authentication password to use<br>when connecting to server |
| password3               | Third multifactor authentication password to use<br>when connecting to server  |
| pipe                    | Connect to server using named pipe (Windows<br>only)                           |
| plugin-dir              | Directory where plugins are installed                                          |
| port                    | TCP/IP port number for connection                                              |
| protocol                | Transport protocol to use                                                      |
| shared-memory-base-name | Shared-memory name for shared-memory<br>connections (Windows only)             |

| Option Name | Description                                         |
|-------------|-----------------------------------------------------|
| socket      | Unix socket file or Windows named pipe to use       |
| user        | MySQL user name to use when connecting to<br>server |

### <span id="page-8-1"></span>• [--default-auth=](#page-8-1)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

### <span id="page-8-0"></span>• --host=[host\\_name](#page-8-0), -h host\_name

| Command-Line Format | host=host_name |
|---------------------|----------------|
| Type                | String         |
| Default Value       | localhost      |

The host on which the MySQL server is running. The value can be a host name, IPv4 address, or IPv6 address. The default value is localhost.

### <span id="page-8-2"></span>• [--password\[=](#page-8-2)pass\_val], -p[pass\_val]

| Command-Line Format | password[=password] |
|---------------------|---------------------|
| Type                | String              |
| Default Value       | [none]              |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, the client program prompts for one. If given, there must be no space between [--password=](#page-8-2) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that the client program should not prompt for one, use the [--skip-password](#page-8-2) option.

### <span id="page-8-3"></span>• [--password1\[=](#page-8-3)pass\_val]

| Command-Line Format | password1[=password] |
|---------------------|----------------------|
| Type                | String               |

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the server. The password value is optional. If not given, the client program prompts for one. If given, there must be no space between [--password1=](#page-8-3) and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that the client program should not prompt for one, use the [--skip-password1](#page-8-3) option.

[--password1](#page-8-3) and [--password](#page-8-2) are synonymous, as are [--skip-password1](#page-8-3) and [--skip](#page-8-2)[password](#page-8-2).

<span id="page-9-0"></span>• [--password2\[=](#page-9-0)pass\_val]

| Command-Line Format | password2[=password] |
|---------------------|----------------------|
| Type                | String               |

The password for multifactor authentication factor 2 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-8-3); see the description of that option for details.

<span id="page-9-1"></span>• [--password3\[=](#page-9-1)pass\_val]

| Command-Line Format | password3[=password] |
|---------------------|----------------------|
| Type                | String               |

The password for multifactor authentication factor 3 of the MySQL account used for connecting to the server. The semantics of this option are similar to the semantics for [--password1](#page-8-3); see the description of that option for details.

<span id="page-9-2"></span>• [--pipe](#page-9-2), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-9-3"></span>• [--plugin-dir=](#page-9-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The directory in which to look for plugins. Specify this option if the [--default-auth](#page-8-1) option is used to specify an authentication plugin but the client program does not find it. See Section 8.2.17, "Pluggable Authentication".

<span id="page-9-4"></span>• --port=[port\\_num](#page-9-4), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use. The default port number is 3306.

<span id="page-9-5"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-9-5)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

This option explicitly specifies which transport protocol to use for connecting to the server. It is useful when other connection parameters normally result in use of a protocol other than the one you want. For example, connections on Unix to localhost are made using a Unix socket file by default:

```
mysql --host=localhost
```

To force TCP/IP transport to be used instead, specify a [--protocol](#page-9-5) option:

```
mysql --host=localhost --protocol=TCP
```

The following table shows the permissible [--protocol](#page-9-5) option values and indicates the applicable platforms for each value. The values are not case-sensitive.

| protocol Value | Transport Protocol Used                       | Applicable Platforms       |
|----------------|-----------------------------------------------|----------------------------|
| TCP            | TCP/IP transport to local or<br>remote server | All                        |
| SOCKET         | Unix socket-file transport to local<br>server | Unix and Unix-like systems |
| PIPE           | Named-pipe transport to local<br>server       | Windows                    |
| MEMORY         | Shared-memory transport to<br>local server    | Windows                    |

See also [Section 6.2.7, "Connection Transport Protocols"](#page-31-0)

<span id="page-10-0"></span>• [--shared-memory-base-name=](#page-10-0)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-10-1"></span>• [--socket=](#page-10-1)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
|---------------------|------------------------------|

On Unix, the name of the Unix socket file to use for connections made using a named pipe to a local server. The default Unix socket file name is /tmp/mysql.sock.

On Windows, the name of the named pipe to use for connections to a local server. The default Windows pipe name is MySQL. The pipe name is not case-sensitive.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-11-0"></span>• --user=[user\\_name](#page-11-0), -u user\_name

| Command-Line Format | user=user_name |
|---------------------|----------------|
| Type                | String         |

The user name of the MySQL account to use for connecting to the server. The default user name is ODBC on Windows or your Unix login name on Unix.

## <span id="page-11-1"></span>**Command Options for Encrypted Connections**

This section describes options for client programs that specify whether to use encrypted connections to the server, the names of certificate and key files, and other parameters related to encrypted-connection support. For examples of suggested use and how to check whether a connection is encrypted, see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".

![](_page_11_Picture_10.jpeg)

# **Note**

These options have an effect only for connections that use a transport protocol subject to encryption; that is, TCP/IP and Unix socket-file connections. See [Section 6.2.7, "Connection Transport Protocols"](#page-31-0)

For information about using encrypted connections from the MySQL C API, see [Support for Encrypted](https://dev.mysql.com/doc/c-api/8.0/en/c-api-encrypted-connections.md) [Connections.](https://dev.mysql.com/doc/c-api/8.0/en/c-api-encrypted-connections.md)

**Table 6.5 Connection-Encryption Option Summary**

| Option Name            | Description                                                                       | Deprecated |
|------------------------|-----------------------------------------------------------------------------------|------------|
| get-server-public-key  | Request RSA public key from<br>server                                             |            |
| server-public-key-path | Path name to file containing RSA<br>public key                                    |            |
| ssl-ca                 | File that contains list of trusted<br>SSL Certificate Authorities                 |            |
| ssl-capath             | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files |            |
| ssl-cert               | File that contains X.509<br>certificate                                           |            |
| ssl-cipher             | Permissible ciphers for<br>connection encryption                                  |            |
| ssl-crl                | File that contains certificate<br>revocation lists                                |            |

| Option Name                                  | Description                                                   | Deprecated |
|----------------------------------------------|---------------------------------------------------------------|------------|
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files  |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                 | Yes        |
| ssl-key                                      | File that contains X.509 key                                  |            |
| ssl-mode                                     | Desired security state of<br>connection to server             |            |
| ssl-session-data                             | File that contains SSL session<br>data                        |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails    |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections        |            |

### <span id="page-12-0"></span>• [--get-server-public-key](#page-12-0)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-12-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-12-0).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-12-1"></span>• [--server-public-key-path=](#page-12-1)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-

based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-12-1)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-12-0).

This option is available only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-13-0"></span>• [--ssl-ca=](#page-13-0)file\_name

| Command-Line Format | ssl-ca=file_name |
|---------------------|------------------|
| Type                | File name        |

The path name of the Certificate Authority (CA) certificate file in PEM format. The file contains a list of trusted SSL Certificate Authorities.

To tell the client not to authenticate the server certificate when establishing an encrypted connection to the server, specify neither [--ssl-ca](#page-13-0) nor [--ssl-capath](#page-13-1). The server still verifies the client according to any applicable requirements established for the client account, and it still uses any ssl\_ca or ssl\_capath system variable values specified on the server side.

To specify the CA file for the server, set the ssl\_ca system variable.

<span id="page-13-1"></span>• [--ssl-capath=](#page-13-1)dir\_name

| Command-Line Format | ssl-capath=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

The path name of the directory that contains trusted SSL certificate authority (CA) certificate files in PEM format.

To tell the client not to authenticate the server certificate when establishing an encrypted connection to the server, specify neither [--ssl-ca](#page-13-0) nor [--ssl-capath](#page-13-1). The server still verifies the client according to any applicable requirements established for the client account, and it still uses any ssl\_ca or ssl\_capath system variable values specified on the server side.

To specify the CA directory for the server, set the ssl\_capath system variable.

<span id="page-13-2"></span>• [--ssl-cert=](#page-13-2)file\_name

| Command-Line Format | ssl-cert=file_name |
|---------------------|--------------------|
| Type                | File name          |

The path name of the client SSL public key certificate file in PEM format.

To specify the server SSL public key certificate file, set the ssl\_cert system variable.

![](_page_13_Picture_19.jpeg)

### **Note**

Chained SSL certificate support was added in v8.0.30; previously only the first certificate was read.

<span id="page-13-3"></span>• [--ssl-cipher=](#page-13-3)cipher\_list

| Command-Line Format | ssl-cipher=name |
|---------------------|-----------------|
| Type                | String          |

The list of permissible encryption ciphers for connections that use TLS protocols up through TLSv1.2. If no cipher in the list is supported, encrypted connections that use these TLS protocols do not work.

For greatest portability, cipher\_list should be a list of one or more cipher names, separated by colons. Examples:

```
--ssl-cipher=AES128-SHA
--ssl-cipher=DHE-RSA-AES128-GCM-SHA256:AES128-SHA
```

OpenSSL supports the syntax for specifying ciphers described in the OpenSSL documentation at <https://www.openssl.org/docs/manmaster/man1/ciphers.html>.

For information about which encryption ciphers MySQL supports, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

To specify the encryption ciphers for the server, set the ssl\_cipher system variable.

<span id="page-14-0"></span>• [--ssl-crl=](#page-14-0)file\_name

| Command-Line Format | ssl-crl=file_name |
|---------------------|-------------------|
| Type                | File name         |

The path name of the file containing certificate revocation lists in PEM format.

If neither [--ssl-crl](#page-14-0) nor [--ssl-crlpath](#page-14-1) is given, no CRL checks are performed, even if the CA path contains certificate revocation lists.

To specify the revocation-list file for the server, set the ssl\_crl system variable.

<span id="page-14-1"></span>• [--ssl-crlpath=](#page-14-1)dir\_name

| Command-Line Format | ssl-crlpath=dir_name |
|---------------------|----------------------|
| Type                | Directory name       |

The path name of the directory that contains certificate revocation-list files in PEM format.

If neither [--ssl-crl](#page-14-0) nor [--ssl-crlpath](#page-14-1) is given, no CRL checks are performed, even if the CA path contains certificate revocation lists.

To specify the revocation-list directory for the server, set the ssl\_crlpath system variable.

<span id="page-14-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-14-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF<br>385                    |
| Valid Values        | OFF                           |
|                     | ON                            |

STRICT

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-14-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-14-2) values are permissible:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_15_Picture_7.jpeg)

### **Note**

If the OpenSSL FIPS Object Module is not available, the only permissible value for [--ssl-fips-mode](#page-14-2) is OFF. In this case, setting [--ssl-fips](#page-14-2)[mode](#page-14-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

To specify the FIPS mode for the server, set the ssl\_fips\_mode system variable.

<span id="page-15-0"></span>• [--ssl-key=](#page-15-0)file\_name

| Command-Line Format | ssl-key=file_name |
|---------------------|-------------------|
| Type                | File name         |

The path name of the client SSL private key file in PEM format. For better security, use a certificate with an RSA key size of at least 2048 bits.

If the key file is protected by a passphrase, the client program prompts the user for the passphrase. The password must be given interactively; it cannot be stored in a file. If the passphrase is incorrect, the program continues as if it could not read the key.

To specify the server SSL private key file, set the ssl\_key system variable.

<span id="page-15-1"></span>• [--ssl-mode=](#page-15-1)mode

| Command-Line Format | ssl-mode=mode   |
|---------------------|-----------------|
| Type                | Enumeration     |
| Default Value       | PREFERRED       |
| Valid Values        | DISABLED        |
|                     | PREFERRED       |
|                     | REQUIRED        |
|                     | VERIFY_CA       |
|                     | VERIFY_IDENTITY |

This option specifies the desired security state of the connection to the server. These mode values are permissible, in order of increasing strictness:

• DISABLED: Establish an unencrypted connection.

• PREFERRED: Establish an encrypted connection if the server supports encrypted connections, falling back to an unencrypted connection if an encrypted connection cannot be established. This is the default if [--ssl-mode](#page-15-1) is not specified.

Connections over Unix socket files are not encrypted with a mode of PREFERRED. To enforce encryption for Unix socket-file connections, use a mode of REQUIRED or stricter. (However, socket-file transport is secure by default, so encrypting a socket-file connection makes it no more secure and increases CPU load.)

- REQUIRED: Establish an encrypted connection if the server supports encrypted connections. The connection attempt fails if an encrypted connection cannot be established.
- VERIFY\_CA: Like REQUIRED, but additionally verify the server Certificate Authority (CA) certificate against the configured CA certificates. The connection attempt fails if no valid matching CA certificates are found.
- VERIFY\_IDENTITY: Like VERIFY\_CA, but additionally perform host name identity verification by checking the host name the client uses for connecting to the server against the identity in the certificate that the server sends to the client:
  - As of MySQL 8.0.12, if the client uses OpenSSL 1.0.2 or higher, the client checks whether the host name that it uses for connecting matches either the Subject Alternative Name value or the Common Name value in the server certificate. Host name identity verification also works with certificates that specify the Common Name using wildcards.
  - Otherwise, the client checks whether the host name that it uses for connecting matches the Common Name value in the server certificate.

The connection fails if there is a mismatch. For encrypted connections, this option helps prevent man-in-the-middle attacks.

![](_page_16_Picture_9.jpeg)

### **Note**

Host name identity verification with VERIFY\_IDENTITY does not work with self-signed certificates that are created automatically by the server or manually using [mysql\\_ssl\\_rsa\\_setup](#page-61-0) (see Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"). Such self-signed certificates do not contain the server name as the Common Name value.

![](_page_16_Picture_12.jpeg)

### **Important**

The default setting, [--ssl-mode=PREFERRED](#page-15-1), produces an encrypted connection if the other default settings are unchanged. However, to help prevent sophisticated man-in-the-middle attacks, it is important for the client to verify the server's identity. The settings [--ssl-mode=VERIFY\\_CA](#page-15-1) and [-](#page-15-1) [ssl-mode=VERIFY\\_IDENTITY](#page-15-1) are a better choice than the default setting to help prevent this type of attack. To implement one of these settings, you must first ensure that the CA certificate for the server is reliably available to all the clients that use it in your environment, otherwise availability issues will result. For this reason, they are not the default setting.

The [--ssl-mode](#page-15-1) option interacts with CA certificate options as follows:

- If [--ssl-mode](#page-15-1) is not explicitly set otherwise, use of [--ssl-ca](#page-13-0) or [--ssl-capath](#page-13-1) implies [-](#page-15-1) [ssl-mode=VERIFY\\_CA](#page-15-1).
- For [--ssl-mode](#page-15-1) values of VERIFY\_CA or VERIFY\_IDENTITY, [--ssl-ca](#page-13-0) or [--ssl-capath](#page-13-1) is also required, to supply a CA certificate that matches the one used by the server.

• An explicit [--ssl-mode](#page-15-1) option with a value other than VERIFY\_CA or VERIFY\_IDENTITY, together with an explicit [--ssl-ca](#page-13-0) or [--ssl-capath](#page-13-1) option, produces a warning that no verification of the server certificate is performed, despite a CA certificate option being specified.

To require use of encrypted connections by a MySQL account, use CREATE USER to create the account with a REQUIRE SSL clause, or use ALTER USER for an existing account to add a REQUIRE SSL clause. This causes connection attempts by clients that use the account to be rejected unless MySQL supports encrypted connections and an encrypted connection can be established.

The REQUIRE clause permits other encryption-related options, which can be used to enforce security requirements stricter than REQUIRE SSL. For additional details about which command options may or must be specified by clients that connect using accounts configured using the various REQUIRE options, see CREATE USER SSL/TLS Options.

<span id="page-17-0"></span>• [--ssl-session-data=](#page-17-0)file\_name

| Command-Line Format | ssl-session-data=file_name |
|---------------------|----------------------------|
| Type                | File name                  |

The path name of the client SSL session data file in PEM format for session reuse.

When you invoke a MySQL client program with the [--ssl-session-data](#page-17-0) option, the client attempts to deserialize session data from the file, if provided, and then use it to establish a new connection. If you supply a file, but the session is not reused, then the connection fails unless you also specified the [--ssl-session-data-continue-on-failed-reuse](#page-17-1) option on the command line when you invoked the client program.

The [mysql](#page-77-0) command, ssl\_session\_data\_print, generates the session data file (see [Section 6.5.1.2, "mysql Client Commands"](#page-106-0)).

<span id="page-17-1"></span>• [ssl-session-data-continue-on-failed-reuse](#page-17-1)

| Command-Line Format | ssl-session-data-continue-on<br>failed-reuse |
|---------------------|----------------------------------------------|
| Type                | Boolean                                      |
| Default Value       | OFF                                          |

Controls whether a new connection is started to replace an attempted connection that tried but failed to reuse session data specified with the [--ssl-session-data](#page-17-0) command-line option. By default, the [--ssl-session-data-continue-on-failed-reuse](#page-17-1) command-line option is off, which causes a client program to return a connect failure when session data are supplied and not reused.

To ensure that a new, unrelated connection opens after session reuse fails silently, invoke MySQL client programs with both the [--ssl-session-data](#page-17-0) and [--ssl-session-data-continue-on](#page-17-1)[failed-reuse](#page-17-1) command-line options.

<span id="page-17-2"></span>• [--tls-ciphersuites=](#page-17-2)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

| Default Value | empty string |
|---------------|--------------|
|---------------|--------------|

This option specifies which ciphersuites the client permits for encrypted connections that use TLSv1.3. The value is a list of zero or more colon-separated ciphersuite names. For example:

```
mysql --tls-ciphersuites="suite1:suite2:suite3"
```

The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. If this option is not set, the client permits the default set of ciphersuites. If the option is set to the empty string, no ciphersuites are enabled and encrypted connections cannot be established. For more information, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

To specify which ciphersuites the server permits, set the tls\_ciphersuites system variable.

<span id="page-18-0"></span>• [--tls-version=](#page-18-0)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

This option specifies the TLS protocols the client permits for encrypted connections. The value is a list of one or more comma-separated protocol versions. For example:

```
mysql --tls-version="TLSv1.2,TLSv1.3"
```

The protocols that can be named for this option depend on the SSL library used to compile MySQL, and on the MySQL Server release.

![](_page_18_Picture_12.jpeg)

### **Important**

- Support for the TLSv1 and TLSv1.1 connection protocols is removed from MySQL Server as of MySQL 8.0.28. The protocols were deprecated from MySQL 8.0.26, though MySQL Server clients do not return warnings to the user if a deprecated TLS protocol version is used. From MySQL 8.0.28 onwards, clients, including MySQL Shell, that support the [--tls](#page-18-0)[version](#page-18-0) option cannot make a TLS/SSL connection with the protocol set to TLSv1 or TLSv1.1. If a client attempts to connect using these protocols, for TCP connections, the connection fails, and an error is returned to the client. For socket connections, if [--ssl-mode](#page-15-1) is set to REQUIRED, the connection fails, otherwise the connection is made but with TLS/SSL disabled. See Removal of Support for the TLSv1 and TLSv1.1 Protocols for more information.
- Support for the TLSv1.3 protocol is available in MySQL Server as of MySQL 8.0.16, provided that MySQL Server was compiled using OpenSSL 1.1.1 or higher. The server checks the version of OpenSSL at startup, and if it is lower than 1.1.1, TLSv1.3 is removed from the default value

for the server system variables relating to the TLS version (such as the tls\_version system variable).

Permitted protocols should be chosen such as not to leave "holes" in the list. For example, these values do not have holes:

```
--tls-version="TLSv1,TLSv1.1,TLSv1.2,TLSv1.3"
--tls-version="TLSv1.1,TLSv1.2,TLSv1.3"
--tls-version="TLSv1.2,TLSv1.3"
--tls-version="TLSv1.3"
From MySQL 8.0.28, only the last two values are suitable.
```

These values do have holes and should not be used:

```
--tls-version="TLSv1,TLSv1.2"
--tls-version="TLSv1.1,TLSv1.3"
```

For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

To specify which TLS protocols the server permits, set the tls\_version system variable.

# <span id="page-19-0"></span>**Command Options for Connection Compression**

This section describes options that enable client programs to control use of compression for connections to the server. For additional information and examples showing how to use them, see [Section 6.2.8, "Connection Compression Control".](#page-32-0)

**Table 6.6 Connection-Compression Option Summary**

| Option Name            | Description                                                                 | Deprecated |
|------------------------|-----------------------------------------------------------------------------|------------|
| compress               | Compress all information sent<br>between client and server                  | Yes        |
| compression-algorithms | Permitted compression<br>algorithms for connections to<br>server            |            |
| zstd-compression-level | Compression level for<br>connections to server that use<br>zstd compression |            |

<span id="page-19-1"></span>• [--compress](#page-19-1), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible.

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

<span id="page-19-2"></span>• [--compression-algorithms=](#page-19-2)value

| Command-Line Format | compression-algorithms=value |
|---------------------|------------------------------|
| Type                | Set                          |
| Default Value       | uncompressed                 |
| Valid Values        | zlib                         |

|  | zstd         |
|--|--------------|
|  | uncompressed |

The permitted compression algorithms for connections to the server. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. The default value is uncompressed.

This option was added in MySQL 8.0.18.

<span id="page-20-1"></span>• [--zstd-compression-level=](#page-20-1)level

| Command-Line Format | zstd-compression-level=# |
|---------------------|--------------------------|
| Type                | Integer                  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

This option was added in MySQL 8.0.18.

# <span id="page-20-0"></span>**6.2.4 Connecting to the MySQL Server Using Command Options**

This section describes use of command-line options to specify how to establish connections to the MySQL server, for clients such as [mysql](#page-77-0) or [mysqldump](#page-152-0). For information on establishing connections using URI-like connection strings or key-value pairs, for clients such as MySQL Shell, see [Section 6.2.5, "Connecting to the Server Using URI-Like Strings or Key-Value Pairs"](#page-22-0). For additional information if you are unable to connect, see Section 8.2.22, "Troubleshooting Problems Connecting to MySQL".

For a client program to connect to the MySQL server, it must use the proper connection parameters, such as the name of the host where the server is running and the user name and password of your MySQL account. Each connection parameter has a default value, but you can override default values as necessary using program options specified either on the command line or in an option file.

The examples here use the [mysql](#page-77-0) client program, but the principles apply to other clients such as [mysqldump](#page-152-0), [mysqladmin](#page-121-0), or mysqlshow.

This command invokes [mysql](#page-77-0) without specifying any explicit connection parameters:

mysql

Because there are no parameter options, the default values apply:

- The default host name is localhost. On Unix, this has a special meaning, as described later.
- The default user name is ODBC on Windows or your Unix login name on Unix.
- No password is sent because neither [--password](#page-8-2) nor -p is given.
- For [mysql](#page-77-0), the first nonoption argument is taken as the name of the default database. Because there is no such argument, [mysql](#page-77-0) selects no default database.

To specify the host name and user name explicitly, as well as a password, supply appropriate options on the command line. To select a default database, add a database-name argument. Examples:

```
mysql --host=localhost --user=myname --password=password mydb
mysql -h localhost -u myname -ppassword mydb
```

For password options, the password value is optional:

- If you use a [--password](#page-8-2) or -p option and specify a password value, there must be no space between [--password=](#page-8-2) or -p and the password following it.
- If you use [--password](#page-8-2) or -p but do not specify a password value, the client program prompts you to enter the password. The password is not displayed as you enter it. This is more secure than giving the password on the command line, which might enable other users on your system to see the password line by executing a command such as ps. See Section 8.1.2.1, "End-User Guidelines for Password Security".
- To explicitly specify that there is no password and that the client program should not prompt for one, use the [--skip-password](#page-8-2) option.

As just mentioned, including the password value on the command line is a security risk. To avoid this risk, specify the [--password](#page-8-2) or -p option without any following password value:

```
mysql --host=localhost --user=myname --password mydb
mysql -h localhost -u myname -p mydb
```

When the [--password](#page-8-2) or -p option is given with no password value, the client program prints a prompt and waits for you to enter the password. (In these examples, mydb is not interpreted as a password because it is separated from the preceding password option by a space.)

On some systems, the library routine that MySQL uses to prompt for a password automatically limits the password to eight characters. That limitation is a property of the system library, not MySQL. Internally, MySQL does not have any limit for the length of the password. To work around the limitation on systems affected by it, specify your password in an option file (see Section 6.2.2.2, "Using Option Files"). Another workaround is to change your MySQL password to a value that has eight or fewer characters, but that has the disadvantage that shorter passwords tend to be less secure.

Client programs determine what type of connection to make as follows:

- If the host is not specified or is localhost, a connection to the local host occurs:
  - On Windows, the client connects using shared memory, if the server was started with the shared\_memory system variable enabled to support shared-memory connections.
  - On Unix, MySQL programs treat the host name localhost specially, in a way that is likely different from what you expect compared to other network-based programs: the client connects using a Unix socket file. The [--socket](#page-10-1) option or the MYSQL\_UNIX\_PORT environment variable may be used to specify the socket name.
- On Windows, if host is . (period), or TCP/IP is not enabled and [--socket](#page-10-1) is not specified or the host is empty, the client connects using a named pipe, if the server was started with the named\_pipe system variable enabled to support named-pipe connections. If named-pipe connections are not supported or if the user making the connection is not a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable, an error occurs.
- Otherwise, the connection uses TCP/IP.

The [--protocol](#page-9-5) option enables you to use a particular transport protocol even when other options normally result in use of a different protocol. That is, [--protocol](#page-9-5) specifies the transport protocol explicitly and overrides the preceding rules, even for localhost.

Only connection options that are relevant to the selected transport protocol are used or checked. Other connection options are ignored. For example, with [--host=localhost](#page-8-0) on Unix, the client attempts to connect to the local server using a Unix socket file, even if a [--port](#page-9-4) or -P option is given to specify a TCP/IP port number.

To ensure that the client makes a TCP/IP connection to the local server, use [--host](#page-8-0) or -h to specify a host name value of 127.0.0.1 (instead of localhost), or the IP address or name of the local

server. You can also specify the transport protocol explicitly, even for localhost, by using the [-](#page-9-5) [protocol=TCP](#page-9-5) option. Examples:

```
mysql --host=127.0.0.1
mysql --protocol=TCP
```

If the server is configured to accept IPv6 connections, clients can connect to the local server over IPv6 using [--host=::1](#page-8-0). See Section 7.1.13, "IPv6 Support".

On Windows, to force a MySQL client to use a named-pipe connection, specify the [--pipe](#page-9-2) or [--protocol=PIPE](#page-9-5) option, or specify . (period) as the host name. If the server was not started with the named\_pipe system variable enabled to support named-pipe connections or if the user making the connection is not a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable, an error occurs. Use the [--socket](#page-10-1) option to specify the name of the pipe if you do not want to use the default pipe name.

Connections to remote servers use TCP/IP. This command connects to the server running on remote.example.com using the default port number (3306):

```
mysql --host=remote.example.com
```

To specify a port number explicitly, use the [--port](#page-9-4) or -P option:

```
mysql --host=remote.example.com --port=13306
```

You can specify a port number for connections to a local server, too. However, as indicated previously, connections to localhost on Unix use a socket file by default, so unless you force a TCP/IP connection as previously described, any option that specifies a port number is ignored.

For this command, the program uses a socket file on Unix and the [--port](#page-9-4) option is ignored:

```
mysql --port=13306 --host=localhost
```

To cause the port number to be used, force a TCP/IP connection. For example, invoke the program in either of these ways:

```
mysql --port=13306 --host=127.0.0.1
mysql --port=13306 --protocol=TCP
```

For additional information about options that control how client programs establish connections to the server, see [Section 6.2.3, "Command Options for Connecting to the Server"](#page-7-1).

It is possible to specify connection parameters without entering them on the command line each time you invoke a client program:

• Specify the connection parameters in the [client] section of an option file. The relevant section of the file might look like this:

```
[client]
host=host_name
user=user_name
password=password
```

For more information, see Section 6.2.2.2, "Using Option Files".

- Some connection parameters can be specified using environment variables. Examples:
  - To specify the host for [mysql](#page-77-0), use MYSQL\_HOST.
  - On Windows, to specify the MySQL user name, use USER.

For a list of supported environment variables, see Section 6.9, "Environment Variables".

# <span id="page-22-0"></span>**6.2.5 Connecting to the Server Using URI-Like Strings or Key-Value Pairs**

This section describes use of URI-like connection strings or key-value pairs to specify how to establish connections to the MySQL server, for clients such as MySQL Shell. For information on establishing connections using command-line options, for clients such as [mysql](#page-77-0) or [mysqldump](#page-152-0), see [Section 6.2.4,](#page-20-0) ["Connecting to the MySQL Server Using Command Options".](#page-20-0) For additional information if you are unable to connect, see Section 8.2.22, "Troubleshooting Problems Connecting to MySQL".

![](_page_23_Picture_2.jpeg)

### **Note**

The term "URI-like" signifies connection-string syntax that is similar to but not identical to the URI (uniform resource identifier) syntax defined by [RFC 3986.](https://tools.ietf.org/html/rfc3986)

The following MySQL clients support connecting to a MySQL server using a URI-like connection string or key-value pairs:

- MySQL Shell
- MySQL Connectors which implement X DevAPI

This section documents all valid URI-like string and key-value pair connection parameters, many of which are similar to those specified with command-line options:

- Parameters specified with a URI-like string use a syntax such as myuser@example.com:3306/ main-schema. For the full syntax, see [Connecting Using URI-Like Connection Strings.](#page-27-0)
- Parameters specified with key-value pairs use a syntax such as {user:'myuser', host:'example.com', port:3306, schema:'main-schema'}. For the full syntax, see [Connecting Using Key-Value Pairs](#page-28-0).

Connection parameters are not case-sensitive. Each parameter, if specified, can be given only once. If a parameter is specified more than once, an error occurs.

This section covers the following topics:

- [Base Connection Parameters](#page-23-0)
- [Additional Connection parameters](#page-24-0)
- [Connecting Using URI-Like Connection Strings](#page-27-0)
- [Connecting Using Key-Value Pairs](#page-28-0)

# <span id="page-23-0"></span>**Base Connection Parameters**

The following discussion describes the parameters available when specifying a connection to MySQL. These parameters can be provided using either a string that conforms to the base URI-like syntax (see [Connecting Using URI-Like Connection Strings\)](#page-27-0), or as key-value pairs (see [Connecting Using Key-](#page-28-0)[Value Pairs](#page-28-0)).

- scheme: The transport protocol to use. Use mysqlx for X Protocol connections and mysql for classic MySQL protocol connections. If no protocol is specified, the server attempts to guess the protocol. Connectors that support DNS SRV can use the mysqlx+srv scheme (see [Connections](https://dev.mysql.com/doc/x-devapi-userguide/en/connecting-dns-srv.md) [Using DNS SRV Records\)](https://dev.mysql.com/doc/x-devapi-userguide/en/connecting-dns-srv.md).
- user: The MySQL user account to provide for the authentication process.
- password: The password to use for the authentication process.

![](_page_23_Picture_22.jpeg)

### **Warning**

Specifying an explicit password in the connection specification is insecure and not recommended. Later discussion shows how to cause an interactive prompt for the password to occur.

- host: The host on which the server instance is running. The value can be a host name, IPv4 address, or IPv6 address. If no host is specified, the default is localhost.
- port: The TCP/IP network port on which the target MySQL server is listening for connections. If no port is specified, the default is 33060 for X Protocol connections and 3306 for classic MySQL protocol connections.
- socket: The path to a Unix socket file or the name of a Windows named pipe. Values are local file paths. In URI-like strings, they must be encoded, using either percent encoding or by surrounding the path with parentheses. Parentheses eliminate the need to percent encode characters such as the / directory separator character. For example, to connect as root@localhost using the Unix socket /tmp/mysql.sock, specify the path using percent encoding as root@localhost? socket=%2Ftmp%2Fmysql.sock, or using parentheses as root@localhost?socket=(/tmp/ mysql.sock).
- schema: The default database for the connection. If no database is specified, the connection has no default database.

The handling of localhost on Unix depends on the type of transport protocol. Connections using classic MySQL protocol handle localhost the same way as other MySQL clients, which means that localhost is assumed to be for socket-based connections. For connections using X Protocol, the behavior of localhost differs in that it is assumed to represent the loopback address, for example, IPv4 address 127.0.0.1.

# <span id="page-24-0"></span>**Additional Connection parameters**

You can specify options for the connection, either as attributes in a URI-like string by appending ?attribute=value, or as key-value pairs. The following options are available:

- ssl-mode: The desired security state for the connection. The following modes are permissible:
  - DISABLED
  - PREFERRED
  - REQUIRED
  - VERIFY\_CA
  - VERIFY\_IDENTITY

![](_page_24_Picture_14.jpeg)

### **Important**

VERIFY\_CA and VERIFY\_IDENTITY are better choices than the default PREFERRED, because they help prevent man-in-the-middle attacks.

For information about these modes, see the [--ssl-mode](#page-15-1) option description in [Command Options](#page-11-1) [for Encrypted Connections.](#page-11-1)

- ssl-ca: The path to the X.509 certificate authority file in PEM format.
- ssl-capath: The path to the directory that contains the X.509 certificates authority files in PEM format.
- ssl-cert: The path to the X.509 certificate file in PEM format.
- ssl-cipher: The encryption cipher to use for connections that use TLS protocols up through TLSv1.2.
- ssl-crl: The path to the file that contains certificate revocation lists in PEM format.
- ssl-crlpath: The path to the directory that contains certificate revocation-list files in PEM format.

- ssl-key: The path to the X.509 key file in PEM format.
- tls-version: The TLS protocols permitted for classic MySQL protocol encrypted connections. This option is supported by MySQL Shell only. The value of tls-version (singular) is a comma separated list, for example TLSv1.2,TLSv1.3. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". This option depends on the ssl-mode option not being set to DISABLED.
- tls-versions: The permissible TLS protocols for encrypted X Protocol connections. The value of tls-versions (plural) is an array such as [TLSv1.2,TLSv1.3]. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". This option depends on the ssl-mode option not being set to DISABLED.
- tls-ciphersuites: The permitted TLS cipher suites. The value of tls-ciphersuites is a list of IANA cipher suite names as listed at [TLS Ciphersuites](https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-parameters-4). For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". This option depends on the ssl-mode option not being set to DISABLED.
- auth-method: The authentication method to use for the connection. The default is AUTO, meaning that the server attempts to guess. The following methods are permissible:
  - AUTO
  - MYSQL41
  - SHA256\_MEMORY
  - FROM\_CAPABILITIES
  - FALLBACK
  - PLAIN

For X Protocol connections, any configured auth-method is overridden to this sequence of authentication methods: MYSQL41, SHA256\_MEMORY, PLAIN.

• get-server-public-key: Request from the server the public key required for RSA key pairbased password exchange. Use when connecting to MySQL 8.0 servers over classic MySQL protocol with SSL mode DISABLED. You must specify the protocol in this case. For example:

```
mysql://user@localhost:3306?get-server-public-key=true
```

This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If server-public-key-path=file\_name is given and specifies a valid public key file, it takes precedence over get-server-public-key.

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

• server-public-key-path: The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. Use when connecting to MySQL 8.0 servers over classic MySQL protocol with SSL mode DISABLED.

This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not used, as is the case when the client connects to the server using a secure connection.

If server-public-key-path=file\_name is given and specifies a valid public key file, it takes precedence over get-server-public-key.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

- ssh: The URI for connection to an SSH server to access a MySQL server instance using SSH tunneling. The URI format is [user@]host[:port]. Use the uri option to specify the URI of the target MySQL server instance. For information on SSH tunnel connections from MySQL Shell, see [Using an SSH Tunnel](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-connection-ssh.md).
- uri: The URI for a MySQL server instance that is to be accessed through an SSH tunnel from the server specified by the ssh option. The URI format is [scheme://][user@]host[:port]. Do not use the base connection parameters (scheme, user, host, port) to specify the MySQL server connection for SSH tunneling, just use the uri option.
- ssh-password: The password for the connection to the SSH server.

![](_page_26_Picture_6.jpeg)

### **Warning**

Specifying an explicit password in the connection specification is insecure and not recommended. MySQL Shell prompts for a password interactively when one is required.

- ssh-config-file: The SSH configuration file for the connection to the SSH server. You can use the MySQL Shell configuration option ssh.configFile to set a custom file as the default if this option is not specified. If ssh.configFile has not been set, the default is the standard SSH configuration file ~/.ssh/config.
- ssh-identity-file: The identity file to use for the connection to the SSH server. The default if this option is not specified is any identity file configured in an SSH agent (if used), or in the SSH configuration file, or the standard private key file in the SSH configuration folder (~/.ssh/id\_rsa).
- ssh-identity-pass: The passphrase for the identity file specified by the ssh-identity-file option.

![](_page_26_Picture_12.jpeg)

### **Warning**

Specifying an explicit password in the connection specification is insecure and not recommended. MySQL Shell prompts for a password interactively when one is required.

- connect-timeout: An integer value used to configure the number of seconds that clients, such as MySQL Shell, wait until they stop trying to connect to an unresponsive MySQL server.
- compression: This option requests or disables compression for the connection. Up to MySQL 8.0.19 it operates for classic MySQL protocol connections only, and from MySQL 8.0.20 it also operates for X Protocol connections.
  - Up to MySQL 8.0.19, the values for this option are true (or 1) which enables compression, and the default false (or 0) which disables compression.
  - From MySQL 8.0.20, the values for this option are required, which requests compression and fails if the server does not support it; preferred, which requests compression and falls back to an uncompressed connection; and disabled, which requests an uncompressed connection and fails if the server does not permit those. preferred is the default for X Protocol connections, and disabled is the default for classic MySQL protocol connections. For information on X Plugin connection compression control, see Section 22.5.5, "Connection Compression with X Plugin". Note that different MySQL clients implement their support for connection compression differently. Consult your client's documentation for details.

- compression-algorithms and compression-level: These options are available in MySQL Shell 8.0.20 and later for more control over connection compression. You can specify them to select the compression algorithm used for the connection, and the numeric compression level used with that algorithm. You can also use compression-algorithms in place of compression to request compression for the connection. For information on MySQL Shell's connection compression control, see [Using Compressed Connections](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-compressed-connections.md).
- connection-attributes: Controls the key-value pairs that application programs pass to the server at connect time. For general information about connection attributes, see Section 29.12.9, "Performance Schema Connection Attribute Tables". Clients usually define a default set of attributes, which can be disabled or enabled. For example:

```
mysqlx://user@host?connection-attributes
mysqlx://user@host?connection-attributes=true
mysqlx://user@host?connection-attributes=false
```

The default behavior is to send the default attribute set. Applications can specify attributes to be passed in addition to the default attributes. You specify additional connection attributes as a connection-attributes parameter in a connection string. The connection-attributes parameter value must be empty (the same as specifying true), a Boolean value (true or false to enable or disable the default attribute set), or a list or zero or more key=value specifiers separated by commas (to be sent in addition to the default attribute set). Within a list, a missing key value evaluates as an empty string. Further examples:

```
mysqlx://user@host?connection-attributes=[attr1=val1,attr2,attr3=]
mysqlx://user@host?connection-attributes=[]
```

Application-defined attribute names cannot begin with \_ because such names are reserved for internal attributes.

# <span id="page-27-0"></span>**Connecting Using URI-Like Connection Strings**

You can specify a connection to MySQL Server using a URI-like string. Such strings can be used with the MySQL Shell with the [--uri](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysqlsh.md#option_mysqlsh_uri) command option, the MySQL Shell \connect command, and MySQL Connectors which implement X DevAPI.

![](_page_27_Picture_9.jpeg)

### **Note**

The term "URI-like" signifies connection-string syntax that is similar to but not identical to the URI (uniform resource identifier) syntax defined by [RFC 3986.](https://tools.ietf.org/html/rfc3986)

A URI-like connection string has the following syntax:

[scheme://][user[:[password]]@]host[:port][/schema][?attribute1=value1&attribute2=value2...

![](_page_27_Picture_14.jpeg)

### **Important**

Percent encoding must be used for reserved characters in the elements of the URI-like string. For example, if you specify a string that includes the @ character, the character must be replaced by %40. If you include a zone ID in an IPv6 address, the % character used as the separator must be replaced with %25.

The parameters you can use in a URI-like connection string are described at [Base Connection](#page-23-0) [Parameters.](#page-23-0)

MySQL Shell's shell.parseUri() and shell.unparseUri() methods can be used to deconstruct and assemble a URI-like connection string. Given a URI-like connection string, shell.parseUri() returns a dictionary containing each element found in the string. shell.unparseUri() converts a dictionary of URI components and connection options into a valid URI-like connection string for connecting to MySQL, which can be used in MySQL Shell or by MySQL Connectors which implement X DevAPI.

If no password is specified in the URI-like string, which is recommended, interactive clients prompt for the password. The following examples show how to specify URI-like strings with the user name user\_name. In each case, the password is prompted for.

• An X Protocol connection to a local server instance listening at port 33065.

```
mysqlx://user_name@localhost:33065
```

• A classic MySQL protocol connection to a local server instance listening at port 3333.

```
mysql://user_name@localhost:3333
```

• An X Protocol connection to a remote server instance, using a host name, an IPv4 address, and an IPv6 address.

```
mysqlx://user_name@server.example.com/
mysqlx://user_name@198.51.100.14:123
mysqlx://user_name@[2001:db8:85a3:8d3:1319:8a2e:370:7348]
```

• An X Protocol connection using a socket, with the path provided using either percent encoding or parentheses.

```
mysqlx://user_name@/path%2Fto%2Fsocket.sock
mysqlx://user_name@(/path/to/socket.sock)
```

• An optional path can be specified, which represents a database.

```
# use 'world' as the default database
mysqlx://user_name@198.51.100.1/world
# use 'world_x' as the default database, encoding _ as %5F
mysqlx://user_name@198.51.100.2:33060/world%5Fx
```

• An optional query can be specified, consisting of values each given as a key=value pair or as a single key. To specify multiple values, separate them by , characters. A mix of key=value and key values is permissible. Values can be of type list, with list values ordered by appearance. Strings must be either percent encoded or surrounded by parentheses. The following are equivalent.

```
ssluser@127.0.0.1?ssl-ca=%2Froot%2Fclientcert%2Fca-cert.pem\
&ssl-cert=%2Froot%2Fclientcert%2Fclient-cert.pem\
&ssl-key=%2Froot%2Fclientcert%2Fclient-key
ssluser@127.0.0.1?ssl-ca=(/root/clientcert/ca-cert.pem)\
&ssl-cert=(/root/clientcert/client-cert.pem)\
&ssl-key=(/root/clientcert/client-key)
```

• To specify a TLS version and ciphersuite to use for encrypted connections:

```
mysql://user_name@198.51.100.2:3306/world%5Fx?\
tls-versions=[TLSv1.2,TLSv1.3]&tls-ciphersuites=[TLS_DHE_PSK_WITH_AES_128_\
GCM_SHA256, TLS_CHACHA20_POLY1305_SHA256]
```

The previous examples assume that connections require a password. With interactive clients, the specified user's password is requested at the login prompt. If the user account has no password (which is insecure and not recommended), or if socket peer-credential authentication is in use (for example, with Unix socket connections), you must explicitly specify in the connection string that no password is being provided and the password prompt is not required. To do this, place a : after the user\_name in the string but do not specify a password after it. For example:

```
mysqlx://user_name:@localhost
```

## <span id="page-28-0"></span>**Connecting Using Key-Value Pairs**

In MySQL Shell and some MySQL Connectors which implement X DevAPI, you can specify a connection to MySQL Server using key-value pairs, supplied in language-natural constructs for the implementation. For example, you can supply connection parameters using key-value pairs as a

JSON object in JavaScript, or as a dictionary in Python. Regardless of the way the key-value pairs are supplied, the concept remains the same: the keys as described in this section can be assigned values that are used to specify a connection. You can specify connections using key-value pairs in MySQL Shell's shell.connect() method or InnoDB Cluster's dba.createCluster() method, and with some of the MySQL Connectors which implement X DevAPI.

Generally, key-value pairs are surrounded by { and } characters and the , character is used as a separator between key-value pairs. The : character is used between keys and values, and strings must be delimited (for example, using the ' character). It is not necessary to percent encode strings, unlike URI-like connection strings.

A connection specified as key-value pairs has the following format:

```
{ key: value, key: value, ...}
```

The parameters you can use as keys for a connection are described at [Base Connection Parameters.](#page-23-0)

If no password is specified in the key-value pairs, which is recommended, interactive clients prompt for the password. The following examples show how to specify connections using key-value pairs with the user name 'user\_name'. In each case, the password is prompted for.

• An X Protocol connection to a local server instance listening at port 33065.

```
{user:'user_name', host:'localhost', port:33065}
```

• A classic MySQL protocol connection to a local server instance listening at port 3333.

```
{user:'user_name', host:'localhost', port:3333}
```

• An X Protocol connection to a remote server instance, using a host name, an IPv4 address, and an IPv6 address.

```
{user:'user_name', host:'server.example.com'}
{user:'user_name', host:198.51.100.14:123}
{user:'user_name', host:[2001:db8:85a3:8d3:1319:8a2e:370:7348]}
```

• An X Protocol connection using a socket.

```
{user:'user_name', socket:'/path/to/socket/file'}
```

• An optional schema can be specified, which represents a database.

```
{user:'user_name', host:'localhost', schema:'world'}
```

The previous examples assume that connections require a password. With interactive clients, the specified user's password is requested at the login prompt. If the user account has no password (which is insecure and not recommended), or if socket peer-credential authentication is in use (for example, with Unix socket connections), you must explicitly specify that no password is being provided and the password prompt is not required. To do this, provide an empty string using '' after the password key. For example:

```
{user:'user_name', password:'', host:'localhost'}
```

# <span id="page-29-0"></span>**6.2.6 Connecting to the Server Using DNS SRV Records**

In the Domain Name System (DNS), a SRV record (service location record) is a type of resource record that enables a client to specify a name that indicates a service, protocol, and domain. A DNS lookup on the name returns a reply containing the names of multiple available servers in the domain that provide the required service. For information about DNS SRV, including how a record defines the preference order of the listed servers, see [RFC 2782](https://tools.ietf.org/html/rfc2782).

MySQL supports the use of DNS SRV records for connecting to servers. A client that receives a DNS SRV lookup result attempts to connect to the MySQL server on each of the listed hosts in order of

preference, based on the priority and weighting assigned to each host by the DNS administrator. A failure to connect occurs only if the client cannot connect to any of the servers.

When multiple MySQL instances, such as a cluster of servers, provide the same service for your applications, DNS SRV records can be used to assist with failover, load balancing, and replication services. It is cumbersome for applications to directly manage the set of candidate servers for connection attempts, and DNS SRV records provide an alternative:

- DNS SRV records enable a DNS administrator to map a single DNS domain to multiple servers. DNS SRV records also can be updated centrally by administrators when servers are added or removed from the configuration or when their host names are changed.
- Central management of DNS SRV records eliminates the need for individual clients to identify each possible host in connection requests, or for connections to be handled by an additional software component. An application can use the DNS SRV record to obtain information about candidate MySQL servers, instead of managing the server information itself.
- DNS SRV records can be used in combination with connection pooling, in which case connections to hosts that are no longer in the current list of DNS SRV records are removed from the pool when they become idle.

MySQL supports use of DNS SRV records to connect to servers in these contexts:

- Several MySQL Connectors implement DNS SRV support; connector-specific options enable requesting DNS SRV record lookup both for X Protocol connections and for classic MySQL protocol connections. For general information, see [Connections Using DNS SRV Records.](https://dev.mysql.com/doc/x-devapi-userguide/en/connecting-dns-srv.md) For details, see the documentation for individual MySQL Connectors.
- The C API provides a [mysql\\_real\\_connect\\_dns\\_srv\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect-dns-srv.md) function that is similar to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.md), except that the argument list does not specify the particular host of the MySQL server to connect to. Instead, it names a DNS SRV record that specifies a group of servers. See [mysql\\_real\\_connect\\_dns\\_srv\(\).](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect-dns-srv.md)
- The [mysql](#page-77-0) client has a [--dns-srv-name](#page-90-0) option to indicate a DNS SRV record that specifies a group of servers. See [Section 6.5.1, "mysql — The MySQL Command-Line Client"](#page-77-0).

A DNS SRV name consists of a service, protocol, and domain, with the service and protocol each prefixed by an underscore:

```
_service._protocol.domain
```

The following DNS SRV record identifies multiple candidate servers, such as might be used by clients for establishing X Protocol connections:

```
Name TTL Class Priority Weight Port Target
_mysqlx._tcp.example.com. 86400 IN SRV 0 5 33060 server1.example.com.
_mysqlx._tcp.example.com. 86400 IN SRV 0 10 33060 server2.example.com.
_mysqlx._tcp.example.com. 86400 IN SRV 10 5 33060 server3.example.com.
_mysqlx._tcp.example.com. 86400 IN SRV 20 5 33060 server4.example.com.
```

Here, mysqlx indicates the X Protocol service and tcp indicates the TCP protocol. A client can request this DNS SRV record using the name \_mysqlx.\_tcp.example.com. The particular syntax for specifying the name in the connection request depends on the type of client. For example, a client might support specifying the name within a URI-like connection string or as a key-value pair.

A DNS SRV record for classic protocol connections might look like this:

```
Name TTL Class Priority Weight Port Target
_mysql._tcp.example.com. 86400 IN SRV 0 5 3306 server1.example.com.
_mysql._tcp.example.com. 86400 IN SRV 0 10 3306 server2.example.com.
_mysql._tcp.example.com. 86400 IN SRV 10 5 3306 server3.example.com.
_mysql._tcp.example.com. 86400 IN SRV 20 5 3306 server4.example.com.
```

Here, the name mysql designates the classic MySQL protocol service, and the port is 3306 (the default classic MySQL protocol port) rather than 33060 (the default X Protocol port).

When DNS SRV record lookup is used, clients generally must apply these rules for connection requests (there may be client- or connector-specific exceptions):

- The request must specify the full DNS SRV record name, with the service and protocol names prefixed by underscores.
- The request must not specify multiple host names.
- The request must not specify a port number.
- Only TCP connections are supported. Unix socket files, Windows named pipes, and shared memory cannot be used.

For more information on using DNS SRV based connections in X DevAPI, see [Connections Using DNS](https://dev.mysql.com/doc/x-devapi-userguide/en/connecting-dns-srv.md) [SRV Records.](https://dev.mysql.com/doc/x-devapi-userguide/en/connecting-dns-srv.md)

# <span id="page-31-0"></span>**6.2.7 Connection Transport Protocols**

For programs that use the MySQL client library (for example, [mysql](#page-77-0) and [mysqldump](#page-152-0)), MySQL supports connections to the server based on several transport protocols: TCP/IP, Unix socket file, named pipe, and shared memory. This section describes how to select these protocols, and how they are similar and different.

- [Transport Protocol Selection](#page-31-1)
- [Transport Support for Local and Remote Connections](#page-31-2)
- [Interpretation of localhost](#page-31-3)
- [Encryption and Security Characteristics](#page-32-1)
- [Connection Compression](#page-32-2)

## <span id="page-31-1"></span>**Transport Protocol Selection**

For a given connection, if the transport protocol is not specified explicitly, it is determined implicitly. For example, connections to localhost result in a socket file connection on Unix and Unix-like systems, and a TCP/IP connection to 127.0.0.1 otherwise. For additional information, see [Section 6.2.4,](#page-20-0) ["Connecting to the MySQL Server Using Command Options".](#page-20-0)

To specify the protocol explicitly, use the [--protocol](#page-9-5) command option. The following table shows the permissible values for [--protocol](#page-9-5) and indicates the applicable platforms for each value. The values are not case-sensitive.

| protocol Value | Transport Protocol Used | Applicable Platforms       |
|----------------|-------------------------|----------------------------|
| TCP            | TCP/IP                  | All                        |
| SOCKET         | Unix socket file        | Unix and Unix-like systems |
| PIPE           | Named pipe              | Windows                    |
| MEMORY         | Shared memory           | Windows                    |

# <span id="page-31-2"></span>**Transport Support for Local and Remote Connections**

TCP/IP transport supports connections to local or remote MySQL servers.

Socket-file, named-pipe, and shared-memory transports support connections only to local MySQL servers. (Named-pipe transport does allow for remote connections, but this capability is not implemented in MySQL.)

# <span id="page-31-3"></span>**Interpretation of localhost**

If the transport protocol is not specified explicitly, localhost is interpreted as follows:

- On Unix and Unix-like systems, a connection to localhost results in a socket-file connection.
- Otherwise, a connection to localhost results in a TCP/IP connection to 127.0.0.1.

If the transport protocol is specified explicitly, localhost is interpreted with respect to that protocol. For example, with [--protocol=TCP](#page-9-5), a connection to localhost results in a TCP/IP connection to 127.0.0.1 on all platforms.

# <span id="page-32-1"></span>**Encryption and Security Characteristics**

TCP/IP and socket-file transports are subject to TLS/SSL encryption, using the options described in [Command Options for Encrypted Connections.](#page-11-1) Named-pipe and shared-memory transports are not subject to TLS/SSL encryption.

A connection is secure by default if made over a transport protocol that is secure by default. Otherwise, for protocols that are subject to TLS/SSL encryption, a connection may be made secure using encryption:

- TCP/IP connections are not secure by default, but can be encrypted to make them secure.
- Socket-file connections are secure by default. They can also be encrypted, but encrypting a socketfile connection makes it no more secure and increases CPU load.
- Named-pipe connections are not secure by default, and are not subject to encryption to make them secure. However, the named\_pipe\_full\_access\_group system variable is available to control which MySQL users are permitted to use named-pipe connections.
- Shared-memory connections are secure by default.

If the require\_secure\_transport system variable is enabled, the server permits only connections that use some form of secure transport. Per the preceding remarks, connections that use TCP/ IP encrypted using TLS/SSL, a socket file, or shared memory are secure connections. TCP/IP connections not encrypted using TLS/SSL and named-pipe connections are not secure.

See also Configuring Encrypted Connections as Mandatory.

## <span id="page-32-2"></span>**Connection Compression**

All transport protocols are subject to use of compression on the traffic between the client and server. If both compression and encryption are used for a given connection, compression occurs before encryption. For more information, see [Section 6.2.8, "Connection Compression Control".](#page-32-0)

# <span id="page-32-0"></span>**6.2.8 Connection Compression Control**

Connections to the server can use compression on the traffic between client and server to reduce the number of bytes sent over the connection. By default, connections are uncompressed, but can be compressed if the server and the client agree on a mutually permitted compression algorithm.

Compressed connections originate on the client side but affect CPU load on both the client and server sides because both sides perform compression and decompression operations. Because enabling compression decreases performance, its benefits occur primarily when there is low network bandwidth, network transfer time dominates the cost of compression and decompression operations, and result sets are large.

This section describes the available compression-control configuration parameters and the information sources available for monitoring use of compression. It applies to classic MySQL protocol connections.

Compression control applies to connections to the server by client programs and by servers participating in source/replica replication or Group Replication. Compression control does not apply to connections for FEDERATED tables. In the following discussion, "client connection" is shorthand for a connection to the server originating from any source for which compression is supported, unless context indicates a specific connection type.

![](_page_33_Picture_2.jpeg)

### **Note**

X Protocol connections to a MySQL Server instance support compression from MySQL 8.0.19, but compression for X Protocol connections operates independently from the compression for classic MySQL protocol connections described here, and is controlled separately. See Section 22.5.5, "Connection Compression with X Plugin" for information on X Protocol connection compression.

- [Configuring Connection Compression](#page-33-0)
- [Configuring Legacy Connection Compression](#page-35-0)
- [Monitoring Connection Compression](#page-35-1)

## <span id="page-33-0"></span>**Configuring Connection Compression**

As of MySQL 8.0.18, these configuration parameters are available for controlling connection compression:

- The protocol\_compression\_algorithms system variable configures which compression algorithms the server permits for incoming connections.
- The [--compression-algorithms](#page-19-2) and [--zstd-compression-level](#page-20-1) command-line options configure permitted compression algorithms and zstd compression level for these client programs: [mysql](#page-77-0), [mysqladmin](#page-121-0), mysqlbinlog, [mysqlcheck](#page-137-0), [mysqldump](#page-152-0), [mysqlimport](#page-189-0), mysqlpump, mysqlshow, mysqlslap, and mysqltest, and [mysql\\_upgrade](#page-65-0). MySQL Shell also offers these command-line options from its 8.0.20 release.
- The MYSQL\_OPT\_COMPRESSION\_ALGORITHMS and MYSQL\_OPT\_ZSTD\_COMPRESSION\_LEVEL options for the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-options.md) function configure permitted compression algorithms and zstd compression level for client programs that use the MySQL C API.
- The MASTER\_COMPRESSION\_ALGORITHMS and MASTER\_ZSTD\_COMPRESSION\_LEVEL options for the CHANGE MASTER TO statement configure permitted compression algorithms and zstd compression level for replica servers participating in source/replica replication. From MySQL 8.0.23, use the statement CHANGE REPLICATION SOURCE TO and the options SOURCE\_COMPRESSION\_ALGORITHMS and SOURCE\_ZSTD\_COMPRESSION\_LEVEL instead.
- The group\_replication\_recovery\_compression\_algorithms and group\_replication\_recovery\_zstd\_compression\_level system variables configure permitted compression algorithms and zstd compression level for Group Replication recovery connections when a new member joins a group and connects to a donor.

Configuration parameters that enable specifying compression algorithms are string-valued and take a list of one or more comma-separated compression algorithm names, in any order, chosen from the following items (not case-sensitive):

- zlib: Permit connections that use the zlib compression algorithm.
- zstd: Permit connections that use the zstd compression algorithm.
- uncompressed: Permit uncompressed connections.

![](_page_33_Picture_19.jpeg)

### **Note**

Because uncompressed is an algorithm name that may or may not be configured, it is possible to configure MySQL not to permit uncompressed connections.

### Examples:

• To configure which compression algorithms the server permits for incoming connections, set the protocol\_compression\_algorithms system variable. By default, the server permits all available algorithms. To configure that setting explicitly at startup, use these lines in the server my.cnf file:

```
[mysqld]
protocol_compression_algorithms=zlib,zstd,uncompressed
```

To set and persist the protocol\_compression\_algorithms system variable to that value at runtime, use this statement:

```
SET PERSIST protocol_compression_algorithms='zlib,zstd,uncompressed';
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change the value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

• To permit only incoming connections that use zstd compression, configure the server at startup like this:

```
[mysqld]
protocol_compression_algorithms=zstd
```

Or, to make the change at runtime:

```
SET PERSIST protocol_compression_algorithms='zstd';
```

• To permit the [mysql](#page-77-0) client to initiate zlib or uncompressed connections, invoke it like this:

```
mysql --compression-algorithms=zlib,uncompressed
```

• To configure replicas to connect to the source using zlib or zstd connections, with a compression level of 7 for zstd connections, use a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23):

```
CHANGE REPLICATION SOURCE TO
 SOURCE_COMPRESSION_ALGORITHMS = 'zlib,zstd',
 SOURCE_ZSTD_COMPRESSION_LEVEL = 7;
```

This assumes that the replica\_compressed\_protocol or slave\_compressed\_protocol system variable is disabled, for reasons described in [Configuring Legacy Connection Compression.](#page-35-0)

For successful connection setup, both sides of the connection must agree on a mutually permitted compression algorithm. The algorithm-negotiation process attempts to use zlib, then zstd, then uncompressed. If the two sides can find no common algorithm, the connection attempt fails.

Because both sides must agree on the compression algorithm, and because uncompressed is an algorithm value that is not necessarily permitted, fallback to an uncompressed connection does not necessarily occur. For example, if the server is configured to permit zstd and a client is configured to permit zlib,uncompressed, the client cannot connect at all. In this case, no algorithm is common to both sides, so connection attempts fail.

Configuration parameters that enable specifying the zstd compression level take an integer value from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

A configurable zstd compression level enables choosing between less network traffic and higher CPU load versus more network traffic and lower CPU load. Higher compression levels reduce network congestion but the additional CPU load may reduce server performance.

# <span id="page-35-0"></span>**Configuring Legacy Connection Compression**

Prior to MySQL 8.0.18, these configuration parameters are available for controlling connection compression:

- Client programs support a [--compress](#page-19-1) command-line option to specify use of compression for the connection to the server.
- For programs that use the MySQL C API, enabling the MYSQL\_OPT\_COMPRESS option for the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-options.md) function specifies use of compression for the connection to the server.
- For source/replica replication, enabling the system variable replica\_compressed\_protocol (from MySQL 8.0.26) or slave\_compressed\_protocol (before MySQL 8.0.26) specifies use of compression for replica connections to the source.

In each case, when use of compression is specified, the connection uses the zlib compression algorithm if both sides permit it, with fallback to an uncompressed connection otherwise.

As of MySQL 8.0.18, the compression parameters just described become legacy parameters, due to the additional compression parameters introduced for more control over connection compression that are described in [Configuring Connection Compression](#page-33-0). An exception is MySQL Shell, where the [-](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysqlsh.md#option_mysqlsh_compress) [compress](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysqlsh.md#option_mysqlsh_compress) command-line option remains current, and can be used to request compression without selecting compression algorithms. For information on MySQL Shell's connection compression control, see [Using Compressed Connections](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-compressed-connections.md).

The legacy compression parameters interact with the newer parameters and their semantics change as follows:

- The meaning of the legacy [--compress](#page-19-1) option depends on whether [--compression](#page-19-2)[algorithms](#page-19-2) is specified:
  - When [--compression-algorithms](#page-19-2) is not specified, [--compress](#page-19-1) is equivalent to specifying a client-side algorithm set of zlib,uncompressed.
  - When [--compression-algorithms](#page-19-2) is specified, [--compress](#page-19-1) is equivalent to specifying an algorithm set of zlib and the full client-side algorithm set is the union of zlib plus the algorithms specified by [--compression-algorithms](#page-19-2). For example, with both [-](#page-19-1) [compress](#page-19-1) and [--compression-algorithms=zlib,zstd](#page-19-2), the permitted-algorithm set is zlib plus zlib,zstd; that is, zlib,zstd. With both [--compress](#page-19-1) and [-](#page-19-2) [compression-algorithms=zstd,uncompressed](#page-19-2), the permitted-algorithm set is zlib plus zstd,uncompressed; that is, zlib,zstd,uncompressed.
- The same type of interaction occurs between the legacy MYSQL\_OPT\_COMPRESS option and the MYSQL\_OPT\_COMPRESSION\_ALGORITHMS option for the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-options.md) C API function.
- If the replica\_compressed\_protocol or slave\_compressed\_protocol system variable is enabled, it takes precedence over MASTER\_COMPRESSION\_ALGORITHMS and connections to the source use zlib compression if both source and replica permit that algorithm. If replica\_compressed\_protocol or slave\_compressed\_protocol is disabled, the value of MASTER\_COMPRESSION\_ALGORITHMS applies.

![](_page_35_Picture_14.jpeg)

### **Note**

The legacy compression-control parameters are deprecated as of MySQL 8.0.18; expect it to be removed in a future version of MySQL.

# <span id="page-35-1"></span>**Monitoring Connection Compression**

The Compression status variable is ON or OFF to indicate whether the current connection uses compression.

The [mysql](#page-77-0) client \status command displays a line that says Protocol: Compressed if compression is enabled for the current connection. If that line is not present, the connection is uncompressed.

As of 8.0.14, the MySQL Shell \status command displays a Compression: line that says Disabled or Enabled to indicate whether the connection is compressed.

As of MySQL 8.0.18, these additional sources of information are available for monitoring connection compression:

- To monitor compression in use for client connections, use the Compression\_algorithm and Compression\_level status variables. For the current connection, their values indicate the compression algorithm and compression level, respectively.
- To determine which compression algorithms the server is configured to permit for incoming connections, check the protocol\_compression\_algorithms system variable.
- For source/replica replication connections, the configured compression algorithms and compression level are available from multiple sources:
  - The Performance Schema replication\_connection\_configuration table has COMPRESSION\_ALGORITHMS and ZSTD\_COMPRESSION\_LEVEL columns.
  - The mysql.slave\_master\_info system table has Master\_compression\_algorithms and Master\_zstd\_compression\_level columns. If the master.info file exists, it contains lines for those values as well.