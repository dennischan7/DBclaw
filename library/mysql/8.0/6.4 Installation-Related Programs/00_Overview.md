---
source: MySQL 8.0 Reference
title: 00_Overview
---

The programs in this section are used when installing or upgrading MySQL.

# <span id="page-53-0"></span>**6.4.1 comp\_err — Compile MySQL Error Message File**

[comp\\_err](#page-53-0) creates the errmsg.sys file that is used by [mysqld](#page-37-0) to determine the error messages to display for different error codes. [comp\\_err](#page-53-0) normally is run automatically when MySQL is built. It compiles the errmsg.sys file from text-format error information in MySQL source distributions:

• As of MySQL 8.0.19, the error information comes from the messages\_to\_error\_log.txt and messages\_to\_clients.txt files in the share directory.

For more information about defining error messages, see the comments within those files, along with the errmsg\_readme.txt file.

• Prior to MySQL 8.0.19, the error information comes from the errmsg-utf8.txt file in the sql/ share directory.

[comp\\_err](#page-53-0) also generates the mysqld\_error.h, mysqld\_ername.h, and mysqld\_errmsg.h header files.

Invoke [comp\\_err](#page-53-0) like this:

```
comp_err [options]
```

[comp\\_err](#page-53-0) supports the following options.

<span id="page-53-1"></span>• [--help](#page-53-1), -?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

| Type          | Boolean |
|---------------|---------|
| Default Value | false   |

### Display a help message and exit.

<span id="page-54-0"></span>• [--charset=](#page-54-0)dir\_name, -C dir\_name

| Command-Line Format | charset         |
|---------------------|-----------------|
| Type                | String          |
| Default Value       | /share/charsets |

The character set directory. The default is ../sql/share/charsets.

<span id="page-54-1"></span>• --debug=[debug\\_options](#page-54-1), -# debug\_options

| Command-Line Format | debug=options             |
|---------------------|---------------------------|
| Type                | String                    |
| Default Value       | d:t:O,/tmp/comp_err.trace |

Write a debugging log. A typical debug\_options string is d:t:O,file\_name. The default is d:t:O,/tmp/comp\_err.trace.

<span id="page-54-2"></span>• [--debug-info](#page-54-2), -T

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | false      |

Print some debugging information when the program exits.

<span id="page-54-3"></span>• [--errmsg-file=](#page-54-3)file\_name, -H file\_name

| Command-Line Format | errmsg-file=name |  |
|---------------------|------------------|--|
| Type                | File name        |  |
| Default Value       | mysqld_errmsg.h  |  |

The name of the error message file. The default is mysqld\_errmsg.h. This option was added in MySQL 8.0.18.

<span id="page-54-4"></span>• [--header-file=](#page-54-4)file\_name, -H file\_name

| Command-Line Format | header-file=name |  |
|---------------------|------------------|--|
| Type                | File name        |  |
| Default Value       | mysqld_error.h   |  |

The name of the error header file. The default is mysqld\_error.h.

<span id="page-54-5"></span>• [--in-file=](#page-54-5)file\_name, -F file\_name

| Command-Line Format | in-file=path |
|---------------------|--------------|

| Type          | File name |
|---------------|-----------|
| Default Value | [none]    |

The name of the input file. The default is ../share/errmsg-utf8.txt.

This option was removed in MySQL 8.0.19 and replaced by the [--in-file-errlog](#page-55-0) and [--in](#page-55-1)[file-toclient](#page-55-1) options.

<span id="page-55-0"></span>• [--in-file-errlog=](#page-55-0)file\_name, -e file\_name

| Command-Line Format | in-file-errlog                   |  |
|---------------------|----------------------------------|--|
| Type                | File name                        |  |
| Default Value       | /share/messages_to_error_log.txt |  |

The name of the input file that defines error messages intended to be written to the error log. The default is ../share/messages\_to\_error\_log.txt.

This option was added in MySQL 8.0.19.

<span id="page-55-1"></span>• [--in-file-toclient=](#page-55-1)file\_name, -c file\_name

| Command-Line Format | in-file-toclient=path          |  |
|---------------------|--------------------------------|--|
| Type                | File name                      |  |
| Default Value       | /share/messages_to_clients.txt |  |

The name of the input file that defines error messages intended to be written to clients. The default is ../share/messages\_to\_clients.txt.

This option was added in MySQL 8.0.19.

<span id="page-55-2"></span>• [--name-file=](#page-55-2)file\_name, -N file\_name

| Command-Line Format | name-file=name  |  |
|---------------------|-----------------|--|
| Type                | File name       |  |
| Default Value       | mysqld_ername.h |  |

The name of the error name file. The default is mysqld\_ername.h.

<span id="page-55-3"></span>• [--out-dir=](#page-55-3)dir\_name, -D dir\_name

| Command-Line Format | out-dir=path |  |
|---------------------|--------------|--|
| Type                | String       |  |
| Default Value       | /share/      |  |

The name of the output base directory. The default is ../sql/share/.

<span id="page-55-4"></span>• [--out-file=](#page-55-4)file\_name, -O file\_name

| Command-Line Format | out-file=name |
|---------------------|---------------|
| Type                | File name     |
| Default Value       | errmsg.sys    |

The name of the output file. The default is errmsg.sys.

<span id="page-56-0"></span>• [--version](#page-56-0), -V

| Command-Line Format | version |
|---------------------|---------|
| Type                | Boolean |
| Default Value       | false   |

Display version information and exit.

# <span id="page-56-1"></span>**6.4.2 mysql\_secure\_installation — Improve MySQL Installation Security**

This program enables you to improve the security of your MySQL installation in the following ways:

- You can set a password for root accounts.
- You can remove root accounts that are accessible from outside the local host.
- You can remove anonymous-user accounts.
- You can remove the test database (which by default can be accessed by all users, even anonymous users), and privileges that permit anyone to access databases with names that start with test\_.

[mysql\\_secure\\_installation](#page-56-1) helps you implement security recommendations similar to those described at Section 2.9.4, "Securing the Initial MySQL Account".

Normal usage is to connect to the local MySQL server; invoke [mysql\\_secure\\_installation](#page-56-1) without arguments:

```
mysql_secure_installation
```

When executed, [mysql\\_secure\\_installation](#page-56-1) prompts you to determine which actions to perform.

The validate\_password component can be used for password strength checking. If the plugin is not installed, [mysql\\_secure\\_installation](#page-56-1) prompts the user whether to install it. Any passwords entered later are checked using the plugin if it is enabled.

Most of the usual MySQL client options such as [--host](#page-58-0) and [--port](#page-59-0) can be used on the command line and in option files. For example, to connect to the local server over IPv6 using port 3307, use this command:

```
mysql_secure_installation --host=::1 --port=3307
```

[mysql\\_secure\\_installation](#page-56-1) supports the following options, which can be specified on the command line or in the [mysql\_secure\_installation] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.9 mysql\_secure\_installation Options**

| Option Name           | Description                                                 | Deprecated |
|-----------------------|-------------------------------------------------------------|------------|
| defaults-extra-file   | Read named option file in<br>addition to usual option files |            |
| defaults-file         | Read only named option file                                 |            |
| defaults-group-suffix | Option group suffix value                                   |            |
| help                  | Display help message and exit                               |            |
| host                  | Host on which MySQL server is<br>located                    |            |

| Option Name                                  | Description                                                                                                                             | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|------------|
| no-defaults                                  | Read no option files                                                                                                                    |            |
| password                                     | Accepted but always<br>ignored. Whenever<br>mysql_secure_installation is<br>invoked, the user is prompted for<br>a password, regardless |            |
| port                                         | TCP/IP port number for<br>connection                                                                                                    |            |
| print-defaults                               | Print default options                                                                                                                   |            |
| protocol                                     | Transport protocol to use                                                                                                               |            |
| socket                                       | Unix socket file or Windows<br>named pipe to use                                                                                        |            |
| ssl-ca                                       | File that contains list of trusted<br>SSL Certificate Authorities                                                                       |            |
| ssl-capath                                   | Directory that contains trusted<br>SSL Certificate Authority<br>certificate files                                                       |            |
| ssl-cert                                     | File that contains X.509<br>certificate                                                                                                 |            |
| ssl-cipher                                   | Permissible ciphers for<br>connection encryption                                                                                        |            |
| ssl-crl                                      | File that contains certificate<br>revocation lists                                                                                      |            |
| ssl-crlpath                                  | Directory that contains certificate<br>revocation-list files                                                                            |            |
| ssl-fips-mode                                | Whether to enable FIPS mode<br>on client side                                                                                           | Yes        |
| ssl-key                                      | File that contains X.509 key                                                                                                            |            |
| ssl-mode                                     | Desired security state of<br>connection to server                                                                                       |            |
| ssl-session-data                             | File that contains SSL session<br>data                                                                                                  |            |
| ssl-session-data-continue-on<br>failed-reuse | Whether to establish connections<br>if session reuse fails                                                                              |            |
| tls-ciphersuites                             | Permissible TLSv1.3 ciphersuites<br>for encrypted connections                                                                           |            |
| tls-version                                  | Permissible TLS protocols for<br>encrypted connections                                                                                  |            |
| use-default                                  | Execute with no user interactivity                                                                                                      |            |
| user                                         | MySQL user name to use when<br>connecting to server                                                                                     |            |

<span id="page-57-0"></span>• [--help](#page-57-0), -?

| Command-Line Format | help |
|---------------------|------|
|                     |      |

Display a help message and exit.

<span id="page-58-1"></span>• [--defaults-extra-file=](#page-58-1)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-58-2"></span>• [--defaults-file=](#page-58-2)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-58-3"></span>• [--defaults-group-suffix=](#page-58-3)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysql\\_secure\\_installation](#page-56-1) normally reads the [client] and [mysql\_secure\_installation] groups. If this option is given as [--defaults-group](#page-58-3)[suffix=\\_other](#page-58-3), [mysql\\_secure\\_installation](#page-56-1) also reads the [client\_other] and [mysql\_secure\_installation\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-58-0"></span>• --host=[host\\_name](#page-58-0), -h host\_name

| Command-Line Format | host |
|---------------------|------|
|---------------------|------|

Connect to the MySQL server on the given host.

<span id="page-58-4"></span>• [--no-defaults](#page-58-4)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-58-4) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-58-4) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-59-1"></span>• [--password=](#page-59-1)password, -p password

| Command-Line Format | password=password |
|---------------------|-------------------|
| Type                | String            |
| Default Value       | [none]            |

This option is accepted but ignored. Whether or not this option is used, [mysql\\_secure\\_installation](#page-56-1) always prompts the user for a password.

<span id="page-59-0"></span>• --port=[port\\_num](#page-59-0), -P port\_num

| Command-Line Format | port=port_num |
|---------------------|---------------|
| Type                | Numeric       |
| Default Value       | 3306          |

For TCP/IP connections, the port number to use.

<span id="page-59-4"></span>• [--print-defaults](#page-59-4)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|                     |                |

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-59-2"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-59-2)

| Command-Line Format | protocol=type |
|---------------------|---------------|
| Type                | String        |
| Default Value       | [see text]    |
| Valid Values        | TCP           |
|                     | SOCKET        |
|                     | PIPE          |
|                     | MEMORY        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see [Section 6.2.7, "Connection Transport Protocols".](#page-31-0)

<span id="page-59-3"></span>• [--socket=](#page-59-3)path, -S path

| Command-Line Format | socket={file_name pipe_name} |
|---------------------|------------------------------|
|---------------------|------------------------------|

| Type | String |
|------|--------|
|------|--------|

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-60-0"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See [Command Options for Encrypted Connections](#page-11-1).

<span id="page-60-1"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-60-1)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-60-1) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-60-1) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_60_Picture_13.jpeg)

# **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-60-1) is OFF. In this case, setting [--ssl-fips-mode](#page-60-1) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-60-2"></span>• [--tls-ciphersuites=](#page-60-2)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-61-1"></span>• [--tls-version=](#page-61-1)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-61-2"></span>• [--use-default](#page-61-2)

| Command-Line Format | use-default |
|---------------------|-------------|
| Type                | Boolean     |

Execute noninteractively. This option can be used for unattended installation operations.

<span id="page-61-3"></span>• --user=[user\\_name](#page-61-3), -u user\_name

| Command-Line Format | user=user_name |
|---------------------|----------------|
| Type                | String         |

The user name of the MySQL account to use for connecting to the server.

# <span id="page-61-0"></span>**6.4.3 mysql\_ssl\_rsa\_setup — Create SSL/RSA Files**

![](_page_61_Picture_12.jpeg)

### **Note**

[mysql\\_ssl\\_rsa\\_setup](#page-61-0) is deprecated as of MySQL 8.0.34. Instead, consider using MySQL server to generate missing SSL and RSA files automatically at startup (see Automatic SSL and RSA File Generation).

This program creates the SSL certificate and key files and RSA key-pair files required to support secure connections using SSL and secure password exchange using RSA over unencrypted connections, if those files are missing. [mysql\\_ssl\\_rsa\\_setup](#page-61-0) can also be used to create new SSL files if the existing ones have expired.

![](_page_61_Picture_16.jpeg)

### **Note**

[mysql\\_ssl\\_rsa\\_setup](#page-61-0) uses the openssl command, so its use is contingent on having OpenSSL installed on your machine.

Another way to generate SSL and RSA files, for MySQL distributions compiled using OpenSSL, is to have the server generate them automatically. See Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL".

![](_page_61_Picture_20.jpeg)

### **Important**

[mysql\\_ssl\\_rsa\\_setup](#page-61-0) helps lower the barrier to using SSL by making it easier to generate the required files. However, certificates generated by [mysql\\_ssl\\_rsa\\_setup](#page-61-0) are self-signed, which is not very secure. After you gain experience using the files created by [mysql\\_ssl\\_rsa\\_setup](#page-61-0), consider obtaining a CA certificate from a registered certificate authority.

Invoke [mysql\\_ssl\\_rsa\\_setup](#page-61-0) like this:

```
mysql_ssl_rsa_setup [options]
```

Typical options are [--datadir](#page-63-0) to specify where to create the files, and [--verbose](#page-64-0) to see the openssl commands that [mysql\\_ssl\\_rsa\\_setup](#page-61-0) executes.

[mysql\\_ssl\\_rsa\\_setup](#page-61-0) attempts to create SSL and RSA files using a default set of file names. It works as follows:

- 1. [mysql\\_ssl\\_rsa\\_setup](#page-61-0) checks for the openssl binary at the locations specified by the PATH environment variable. If openssl is not found, [mysql\\_ssl\\_rsa\\_setup](#page-61-0) does nothing. If openssl is present, [mysql\\_ssl\\_rsa\\_setup](#page-61-0) looks for default SSL and RSA files in the MySQL data directory specified by the [--datadir](#page-63-0) option, or the compiled-in data directory if the [--datadir](#page-63-0) option is not given.
- 2. [mysql\\_ssl\\_rsa\\_setup](#page-61-0) checks the data directory for SSL files with the following names:

```
ca.pem
server-cert.pem
server-key.pem
```

3. If any of those files are present, [mysql\\_ssl\\_rsa\\_setup](#page-61-0) creates no SSL files. Otherwise, it invokes openssl to create them, plus some additional files:

```
ca.pem Self-signed CA certificate
ca-key.pem CA private key
server-cert.pem Server certificate
server-key.pem Server private key
client-cert.pem Client certificate
client-key.pem Client private key
```

These files enable secure client connections using SSL; see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".

4. [mysql\\_ssl\\_rsa\\_setup](#page-61-0) checks the data directory for RSA files with the following names:

```
private_key.pem Private member of private/public key pair
public_key.pem Public member of private/public key pair
```

5. If any of these files are present, [mysql\\_ssl\\_rsa\\_setup](#page-61-0) creates no RSA files. Otherwise, it invokes openssl to create them. These files enable secure password exchange using RSA over unencrypted connections for accounts authenticated by the sha256\_password or caching\_sha2\_password plugin; see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

For information about the characteristics of files created by [mysql\\_ssl\\_rsa\\_setup](#page-61-0), see Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL".

At startup, the MySQL server automatically uses the SSL files created by [mysql\\_ssl\\_rsa\\_setup](#page-61-0) to enable SSL if no explicit SSL options are given other than --ssl (possibly along with ssl\_cipher). If you prefer to designate the files explicitly, invoke clients with the [--ssl-ca](#page-13-0), [--ssl-cert](#page-13-2), and [-](#page-15-0) [ssl-key](#page-15-0) options at startup to name the ca.pem, server-cert.pem, and server-key.pem files, respectively.

The server also automatically uses the RSA files created by [mysql\\_ssl\\_rsa\\_setup](#page-61-0) to enable RSA if no explicit RSA options are given.

If the server is SSL-enabled, clients use SSL by default for the connection. To specify certificate and key files explicitly, use the [--ssl-ca](#page-13-0), [--ssl-cert](#page-13-2), and [--ssl-key](#page-15-0) options to name the ca.pem, client-cert.pem, and client-key.pem files, respectively. However, some additional client setup may be required first because [mysql\\_ssl\\_rsa\\_setup](#page-61-0) by default creates those files in the data directory. The permissions for the data directory normally enable access only to the system account that runs the MySQL server, so client programs cannot use files located there. To make the files available, copy them to a directory that is readable (but not writable) by clients:

• For local clients, the MySQL installation directory can be used. For example, if the data directory is a subdirectory of the installation directory and your current location is the data directory, you can copy the files like this:

```
cp ca.pem client-cert.pem client-key.pem ..
```

• For remote clients, distribute the files using a secure channel to ensure they are not tampered with during transit.

If the SSL files used for a MySQL installation have expired, you can use [mysql\\_ssl\\_rsa\\_setup](#page-61-0) to create new ones:

- 1. Stop the server.
- 2. Rename or remove the existing SSL files. You may wish to make a backup of them first. (The RSA files do not expire, so you need not remove them. [mysql\\_ssl\\_rsa\\_setup](#page-61-0) can see that they exist and does not overwrite them.)
- 3. Run [mysql\\_ssl\\_rsa\\_setup](#page-61-0) with the [--datadir](#page-63-0) option to specify where to create the new files.
- 4. Restart the server.

[mysql\\_ssl\\_rsa\\_setup](#page-61-0) supports the following command-line options, which can be specified on the command line or in the [mysql\_ssl\_rsa\_setup] and [mysqld] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.10 mysql\_ssl\_rsa\_setup Options**

| Option Name | Description                                           |
|-------------|-------------------------------------------------------|
| datadir     | Path to data directory                                |
| help        | Display help message and exit                         |
| suffix      | Suffix for X.509 certificate Common Name<br>attribute |
| uid         | Name of effective user to use for file permissions    |
| verbose     | Verbose mode                                          |
| version     | Display version information and exit                  |

<span id="page-63-1"></span>• [--help](#page-63-1), ?

| Command-Line Format | help |
|---------------------|------|
|---------------------|------|

Display a help message and exit.

<span id="page-63-0"></span>• [--datadir=](#page-63-0)dir\_name

| Command-Line Format | datadir=dir_name |
|---------------------|------------------|
| Type                | Directory name   |

The path to the directory that [mysql\\_ssl\\_rsa\\_setup](#page-61-0) should check for default SSL and RSA files and in which it should create files if they are missing. The default is the compiled-in data directory.

### <span id="page-64-1"></span>• [--suffix=](#page-64-1)str

| Command-Line Format | suffix=str |
|---------------------|------------|
| Type                | String     |

The suffix for the Common Name attribute in X.509 certificates. The suffix value is limited to 17 characters. The default is based on the MySQL version number.

<span id="page-64-2"></span>• [--uid=name](#page-64-2), -v

| Command-Line Format | uid=name |
|---------------------|----------|
|---------------------|----------|

The name of the user who should be the owner of any created files. The value is a user name, not a numeric user ID. In the absence of this option, files created by [mysql\\_ssl\\_rsa\\_setup](#page-61-0) are owned by the user who executes it. This option is valid only if you execute the program as root on a system that supports the chown() system call.

<span id="page-64-0"></span>• [--verbose](#page-64-0), -v

| Command-Line Format | verbose |
|---------------------|---------|
|---------------------|---------|

Verbose mode. Produce more output about what the program does. For example, the program shows the openssl commands it runs, and produces output to indicate whether it skips SSL or RSA file creation because some default file already exists.

<span id="page-64-3"></span>• [--version](#page-64-3), -V

| Command-Line Format | version |
|---------------------|---------|
|---------------------|---------|

Display version information and exit.

# <span id="page-64-4"></span>**6.4.4 mysql\_tzinfo\_to\_sql — Load the Time Zone Tables**

The [mysql\\_tzinfo\\_to\\_sql](#page-64-4) program loads the time zone tables in the mysql database. It is used on systems that have a zoneinfo database (the set of files describing time zones). Examples of such systems are Linux, FreeBSD, Solaris, and macOS. One likely location for these files is the /usr/ share/zoneinfo directory (/usr/share/lib/zoneinfo on Solaris). If your system does not have a zoneinfo database, you can use the downloadable package described in Section 7.1.15, "MySQL Server Time Zone Support".

[mysql\\_tzinfo\\_to\\_sql](#page-64-4) can be invoked several ways:

```
mysql_tzinfo_to_sql tz_dir
mysql_tzinfo_to_sql tz_file tz_name
mysql_tzinfo_to_sql --leap tz_file
```

For the first invocation syntax, pass the zoneinfo directory path name to [mysql\\_tzinfo\\_to\\_sql](#page-64-4) and send the output into the [mysql](#page-77-0) program. For example:

```
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql
```

[mysql\\_tzinfo\\_to\\_sql](#page-64-4) reads your system's time zone files and generates SQL statements from them. [mysql](#page-77-0) processes those statements to load the time zone tables.

The second syntax causes [mysql\\_tzinfo\\_to\\_sql](#page-64-4) to load a single time zone file tz\_file that corresponds to a time zone name tz\_name:

```
mysql_tzinfo_to_sql tz_file tz_name | mysql -u root mysql
```

If your time zone needs to account for leap seconds, invoke [mysql\\_tzinfo\\_to\\_sql](#page-64-4) using the third syntax, which initializes the leap second information. tz\_file is the name of your time zone file:

```
mysql_tzinfo_to_sql --leap tz_file | mysql -u root mysql
```

After running [mysql\\_tzinfo\\_to\\_sql](#page-64-4), it is best to restart the server so that it does not continue to use any previously cached time zone data.

# <span id="page-65-0"></span>**6.4.5 mysql\_upgrade — Check and Upgrade MySQL Tables**

![](_page_65_Picture_5.jpeg)

### **Note**

As of MySQL 8.0.16, the MySQL server performs the upgrade tasks previously handled by [mysql\\_upgrade](#page-65-0) (for details, see Section 3.4, "What the MySQL Upgrade Process Upgrades"). Consequently, [mysql\\_upgrade](#page-65-0) is unneeded and is deprecated as of that version; expect it to be removed in a future version of MySQL. Because [mysql\\_upgrade](#page-65-0) no longer performs upgrade tasks, it exits with status 0 unconditionally.

Each time you upgrade MySQL, you should execute [mysql\\_upgrade](#page-65-0), which looks for incompatibilities with the upgraded MySQL server:

- It upgrades the system tables in the mysql schema so that you can take advantage of new privileges or capabilities that might have been added.
- It upgrades the Performance Schema, INFORMATION\_SCHEMA, and sys schema.
- It examines user schemas.

If [mysql\\_upgrade](#page-65-0) finds that a table has a possible incompatibility, it performs a table check and, if problems are found, attempts a table repair. If the table cannot be repaired, see Section 3.14, "Rebuilding or Repairing Tables or Indexes" for manual table repair strategies.

[mysql\\_upgrade](#page-65-0) communicates directly with the MySQL server, sending it the SQL statements required to perform an upgrade.

![](_page_65_Picture_14.jpeg)

### **Caution**

You should always back up your current MySQL installation before performing an upgrade. See Section 9.2, "Database Backup Methods".

Some upgrade incompatibilities may require special handling before upgrading your MySQL installation and running [mysql\\_upgrade](#page-65-0). See Chapter 3, Upgrading MySQL, for instructions on determining whether any such incompatibilities apply to your installation and how to handle them.

Use [mysql\\_upgrade](#page-65-0) like this:

- 1. Ensure that the server is running.
- 2. Invoke [mysql\\_upgrade](#page-65-0) to upgrade the system tables in the mysql schema and check and repair tables in other schemas:

```
mysql_upgrade [options]
```

3. Stop the server and restart it so that any system table changes take effect.

If you have multiple MySQL server instances to upgrade, invoke [mysql\\_upgrade](#page-65-0) with connection parameters appropriate for connecting to each of the desired servers. For example, with servers running on the local host on parts 3306 through 3308, upgrade each of them by connecting to the appropriate port:

```
mysql_upgrade --protocol=tcp -P 3306 [other_options]
mysql_upgrade --protocol=tcp -P 3307 [other_options]
mysql_upgrade --protocol=tcp -P 3308 [other_options]
```

For local host connections on Unix, the [--protocol=tcp](#page-74-0) option forces a connection using TCP/IP rather than the Unix socket file.

By default, [mysql\\_upgrade](#page-65-0) runs as the MySQL root user. If the root password is expired when you run [mysql\\_upgrade](#page-65-0), it displays a message that your password is expired and that [mysql\\_upgrade](#page-65-0) failed as a result. To correct this, reset the root password to unexpire it and run [mysql\\_upgrade](#page-65-0) again. First, connect to the server as root:

```
$> mysql -u root -p
Enter password: **** <- enter root password here
```

Reset the password using ALTER USER:

```
mysql> ALTER USER USER() IDENTIFIED BY 'root-password';
```

Then exit [mysql](#page-77-0) and run [mysql\\_upgrade](#page-65-0) again:

\$> **mysql\_upgrade [options]**

![](_page_66_Picture_8.jpeg)

### **Note**

If you run the server with the disabled\_storage\_engines system variable set to disable certain storage engines (for example, MyISAM), [mysql\\_upgrade](#page-65-0) might fail with an error like this:

```
mysql_upgrade: [ERROR] 3161: Storage engine MyISAM is disabled
(Table creation is disallowed).
```

To handle this, restart the server with disabled\_storage\_engines disabled. Then you should be able to run [mysql\\_upgrade](#page-65-0) successfully. After that, restart the server with disabled\_storage\_engines set to its original value.

Unless invoked with the [--upgrade-system-tables](#page-76-0) option, [mysql\\_upgrade](#page-65-0) processes all tables in all user schemas as necessary. Table checking might take a long time to complete. Each table is locked and therefore unavailable to other sessions while it is being processed. Check and repair operations can be time-consuming, particularly for large tables. Table checking uses the FOR UPGRADE option of the CHECK TABLE statement. For details about what this option entails, see Section 15.7.3.2, "CHECK TABLE Statement".

[mysql\\_upgrade](#page-65-0) marks all checked and repaired tables with the current MySQL version number. This ensures that the next time you run [mysql\\_upgrade](#page-65-0) with the same version of the server, it can be determined whether there is any need to check or repair a given table again.

[mysql\\_upgrade](#page-65-0) saves the MySQL version number in a file named mysql\_upgrade\_info in the data directory. This is used to quickly check whether all tables have been checked for this release so that table-checking can be skipped. To ignore this file and perform the check regardless, use the [-](#page-71-0) [force](#page-71-0) option.

![](_page_66_Picture_16.jpeg)

# **Note**

The mysql\_upgrade\_info file is deprecated; expect it to be removed in a future version of MySQL.

[mysql\\_upgrade](#page-65-0) checks mysql.user system table rows and, for any row with an empty plugin column, sets that column to 'mysql\_native\_password' if the credentials use a hash format compatible with that plugin. Rows with a pre-4.1 password hash must be upgraded manually.

[mysql\\_upgrade](#page-65-0) does not upgrade the contents of the time zone tables or help tables. For upgrade instructions, see Section 7.1.15, "MySQL Server Time Zone Support", and Section 7.1.17, "Server-Side Help Support".

Unless invoked with the [--skip-sys-schema](#page-74-1) option, [mysql\\_upgrade](#page-65-0) installs the sys schema if it is not installed, and upgrades it to the current version otherwise. An error occurs if a sys schema exists but has no version view, on the assumption that its absence indicates a user-created schema:

A sys schema exists with no sys.version view. If you have a user created sys schema, this must be renamed for the upgrade to succeed.

To upgrade in this case, remove or rename the existing sys schema first.

[mysql\\_upgrade](#page-65-0) supports the following options, which can be specified on the command line or in the [mysql\_upgrade] and [client] groups of an option file. For information about option files used by MySQL programs, see Section 6.2.2.2, "Using Option Files".

**Table 6.11 mysql\_upgrade Options**

| Option Name            | Description                                                                                        | Deprecated |
|------------------------|----------------------------------------------------------------------------------------------------|------------|
| bind-address           | Use specified network interface<br>to connect to MySQL Server                                      |            |
| character-sets-dir     | Directory where character sets<br>are installed                                                    |            |
| compress               | Compress all information sent<br>between client and server                                         | Yes        |
| compression-algorithms | Permitted compression<br>algorithms for connections to<br>server                                   |            |
| debug                  | Write debugging log                                                                                |            |
| debug-check            | Print debugging information<br>when program exits                                                  |            |
| debug-info             | Print debugging information,<br>memory, and CPU statistics<br>when program exits                   |            |
| default-auth           | Authentication plugin to use                                                                       |            |
| default-character-set  | Specify default character set                                                                      |            |
| defaults-extra-file    | Read named option file in<br>addition to usual option files                                        |            |
| defaults-file          | Read only named option file                                                                        |            |
| defaults-group-suffix  | Option group suffix value                                                                          |            |
| force                  | Force execution even if<br>mysql_upgrade has already been<br>executed for current MySQL<br>version |            |
| get-server-public-key  | Request RSA public key from<br>server                                                              |            |
| help                   | Display help message and exit                                                                      |            |
| host                   | Host on which MySQL server is<br>located                                                           |            |
| login-path             | Read login path options<br>from .mylogin.cnf                                                       |            |
| max-allowed-packet     | Maximum packet length to send<br>to or receive from server                                         |            |
| net-buffer-length      | Buffer size for TCP/IP and socket<br>communication                                                 |            |
| no-defaults            | Read no option files                                                                               |            |
| password               | Password to use when<br>connecting to server                                                       |            |

| Option Name                                  | Description                                                                       | Deprecated |
|----------------------------------------------|-----------------------------------------------------------------------------------|------------|
| pipe                                         | Connect to server using named<br>pipe (Windows only)                              |            |
| plugin-dir                                   | Directory where plugins are<br>installed                                          |            |
| port                                         | TCP/IP port number for<br>connection                                              |            |
| print-defaults                               | Print default options                                                             |            |
| protocol                                     | Transport protocol to use                                                         |            |
| server-public-key-path                       | Path name to file containing RSA<br>public key                                    |            |
| shared-memory-base-name                      | Shared-memory name for<br>shared-memory connections<br>(Windows only)             |            |
| skip-sys-schema                              | Do not install or upgrade sys<br>schema                                           |            |
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
| upgrade-system-tables                        | Update only system tables, not<br>user schemas                                    |            |
| user                                         | MySQL user name to use when<br>connecting to server                               |            |

| Option Name            | Description                                                                 | Deprecated |
|------------------------|-----------------------------------------------------------------------------|------------|
| verbose                | Verbose mode                                                                |            |
| version-check          | Check for proper server version                                             |            |
| write-binlog           | Write all statements to binary log                                          |            |
| zstd-compression-level | Compression level for<br>connections to server that use<br>zstd compression |            |

### <span id="page-69-4"></span>• [--help](#page-69-4)

| Command-Line Format | help |
|---------------------|------|

### Display a short help message and exit.

<span id="page-69-0"></span>• [--bind-address=](#page-69-0)ip\_address

| Command-Line Format | bind-address=ip_address |
|---------------------|-------------------------|
|---------------------|-------------------------|

On a computer having multiple network interfaces, use this option to select which interface to use for connecting to the MySQL server.

<span id="page-69-1"></span>• [--character-sets-dir=](#page-69-1)dir\_name

| Command-Line Format | character-sets-dir=dir_name |
|---------------------|-----------------------------|
| Type                | Directory name              |

The directory where character sets are installed. See Section 12.15, "Character Set Configuration".

<span id="page-69-2"></span>• [--compress](#page-69-2), -C

| Command-Line Format | compress[={OFF ON}] |
|---------------------|---------------------|
| Deprecated          | Yes                 |
| Type                | Boolean             |
| Default Value       | OFF                 |

Compress all information sent between the client and the server if possible. See [Section 6.2.8,](#page-32-0) ["Connection Compression Control".](#page-32-0)

As of MySQL 8.0.18, this option is deprecated. Expect it to be removed in a future version of MySQL. See [Configuring Legacy Connection Compression.](#page-35-0)

<span id="page-69-3"></span>• [--compression-algorithms=](#page-69-3)value

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

<span id="page-70-0"></span>• --debug[=[debug\\_options](#page-70-0)], -# [debug\_options]

| Command-Line Format | debug[=#]                      |
|---------------------|--------------------------------|
| Type                | String                         |
| Default Value       | d:t:O,/tmp/mysql_upgrade.trace |

Write a debugging log. A typical debug\_options string is d:t:o,file\_name. The default is d:t:O,/tmp/mysql\_upgrade.trace.

<span id="page-70-1"></span>• [--debug-check](#page-70-1)

| Command-Line Format | debug-check |
|---------------------|-------------|
| Type                | Boolean     |

Print some debugging information when the program exits.

<span id="page-70-2"></span>• [--debug-info](#page-70-2), -T

| Command-Line Format | debug-info |
|---------------------|------------|
| Type                | Boolean    |
| Default Value       | FALSE      |

Print debugging information and memory and CPU usage statistics when the program exits.

<span id="page-70-3"></span>• [--default-auth=](#page-70-3)plugin

| Command-Line Format | default-auth=plugin |
|---------------------|---------------------|
| Type                | String              |

A hint about which client-side authentication plugin to use. See Section 8.2.17, "Pluggable Authentication".

<span id="page-70-4"></span>• [--default-character-set=](#page-70-4)charset\_name

| Command-Line Format | default-character-set=name |
|---------------------|----------------------------|
| Type                | String                     |

Use charset\_name as the default character set. See Section 12.15, "Character Set Configuration".

<span id="page-70-5"></span>• [--defaults-extra-file=](#page-70-5)file\_name

| Command-Line Format | defaults-extra-file=file_name |
|---------------------|-------------------------------|
| Type                | File name                     |

Read this option file after the global option file but (on Unix) before the user option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-71-1"></span>• [--defaults-file=](#page-71-1)file\_name

| Command-Line Format | defaults-file=file_name |
|---------------------|-------------------------|
| Type                | File name               |

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If file\_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-71-2"></span>• [--defaults-group-suffix=](#page-71-2)str

| Command-Line Format | defaults-group-suffix=str |
|---------------------|---------------------------|
| Type                | String                    |

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For example, [mysql\\_upgrade](#page-65-0) normally reads the [client] and [mysql\_upgrade] groups. If this option is given as [--defaults-group-suffix=\\_other](#page-71-2), [mysql\\_upgrade](#page-65-0) also reads the [client\_other] and [mysql\_upgrade\_other] groups.

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-71-0"></span>• [--force](#page-71-0)

| Command-Line Format | force   |
|---------------------|---------|
| Type                | Boolean |

Ignore the mysql\_upgrade\_info file and force execution even if [mysql\\_upgrade](#page-65-0) has already been executed for the current version of MySQL.

<span id="page-71-3"></span>• [--get-server-public-key](#page-71-3)

| Command-Line Format | get-server-public-key |
|---------------------|-----------------------|
| Type                | Boolean               |

Request from the server the public key required for RSA key pair-based password exchange. This option applies to clients that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the server does not send the public key unless requested. This option is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based

password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-74-3)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-71-3).

For information about the caching\_sha2\_password plugin, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-72-0"></span>• --host=[host\\_name](#page-72-0), -h host\_name

| Command-Line Format | host=name |
|---------------------|-----------|
| Type                | String    |

Connect to the MySQL server on the given host.

<span id="page-72-1"></span>• [--login-path=](#page-72-1)name

| Command-Line Format | login-path=name |
|---------------------|-----------------|
| Type                | String          |

Read options from the named login path in the .mylogin.cnf login path file. A "login path" is an option group containing options that specify which MySQL server to connect to and which account to authenticate as. To create or modify a login path file, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-72-2"></span>• [--max-allowed-packet=](#page-72-2)value

| Command-Line Format | max-allowed-packet=value |
|---------------------|--------------------------|
| Type                | Integer                  |
| Default Value       | 25165824                 |
| Minimum Value       | 4096                     |
| Maximum Value       | 2147483648               |

The maximum size of the buffer for client/server communication. The default value is 24MB. The minimum and maximum values are 4KB and 2GB.

<span id="page-72-3"></span>• [--net-buffer-length=](#page-72-3)value

| Command-Line Format | net-buffer-length=value |
|---------------------|-------------------------|
| Type                | Integer                 |
| Default Value       | 1047552                 |
| Minimum Value       | 4096                    |
| Maximum Value       | 16777216                |

### <span id="page-73-0"></span>• [--no-defaults](#page-73-0)

| Command-Line Format | no-defaults |
|---------------------|-------------|
|---------------------|-------------|

Do not read any option files. If program startup fails due to reading unknown options from an option file, [--no-defaults](#page-73-0) can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to be specified in a safer way than on the command line even when [--no-defaults](#page-73-0) is used. To create .mylogin.cnf, use the mysql\_config\_editor utility. See Section 6.6.7, "mysql\_config\_editor — MySQL Configuration Utility".

For additional information about this and other option-file options, see [Section 6.2.2.3, "Command-](#page-1-2)[Line Options that Affect Option-File Handling"](#page-1-2).

<span id="page-73-1"></span>• [--password\[=](#page-73-1)password], -p[password]

| Command-Line Format | password[=name] |
|---------------------|-----------------|
| Type                | String          |

The password of the MySQL account used for connecting to the server. The password value is optional. If not given, [mysql\\_upgrade](#page-65-0) prompts for one. If given, there must be no space between [--password=](#page-73-1) or -p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the password on the command line, use an option file. See Section 8.1.2.1, "End-User Guidelines for Password Security".

To explicitly specify that there is no password and that [mysql\\_upgrade](#page-65-0) should not prompt for one, use the [--skip-password](#page-73-1) option.

<span id="page-73-2"></span>• [--pipe](#page-73-2), -W

| Command-Line Format | pipe   |
|---------------------|--------|
| Type                | String |

On Windows, connect to the server using a named pipe. This option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-73-3"></span>• [--plugin-dir=](#page-73-3)dir\_name

| Command-Line Format | plugin-dir=dir_name |
|---------------------|---------------------|
| Type                | Directory name      |

<span id="page-73-4"></span>The directory in which to look for plugins. Specify this option if the [--default-auth](#page-70-3) option is used to specify an authentication plugin but [mysql\\_upgrade](#page-65-0) does not find it. See Section 8.2.17, "Pluggable Authentication".

| Type | Numeric |
|------|---------|
|------|---------|

For TCP/IP connections, the port number to use.

<span id="page-74-2"></span>• [--print-defaults](#page-74-2)

| Command-Line Format | print-defaults |
|---------------------|----------------|
|---------------------|----------------|

Print the program name and all options that it gets from option files.

<span id="page-74-0"></span>• [--protocol={TCP|SOCKET|PIPE|MEMORY}](#page-74-0)

| Command-Line Format | protocol=name |
|---------------------|---------------|
| Type                | String        |

The transport protocol to use for connecting to the server. It is useful when the other connection parameters normally result in use of a protocol other than the one you want. For details on the permissible values, see [Section 6.2.7, "Connection Transport Protocols".](#page-31-0)

<span id="page-74-3"></span>• [--server-public-key-path=](#page-74-3)file\_name

| Command-Line Format | server-public-key-path=file_name |
|---------------------|----------------------------------|
| Type                | File name                        |

The path name to a file in PEM format containing a client-side copy of the public key required by the server for RSA key pair-based password exchange. This option applies to clients that authenticate with the sha256\_password or caching\_sha2\_password authentication plugin. This option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if RSAbased password exchange is not used, as is the case when the client connects to the server using a secure connection.

If [--server-public-key-path=](#page-74-3)file\_name is given and specifies a valid public key file, it takes precedence over [--get-server-public-key](#page-71-3).

For sha256\_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256\_password and caching\_sha2\_password plugins, see Section 8.4.1.3, "SHA-256 Pluggable Authentication", and Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".

<span id="page-74-4"></span>• [--shared-memory-base-name=](#page-74-4)name

| Command-Line Format | shared-memory-base-name=name |
|---------------------|------------------------------|
| Platform Specific   | Windows                      |

On Windows, the shared-memory name to use for connections made using shared memory to a local server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared\_memory system variable enabled to support shared-memory connections.

<span id="page-74-1"></span>• [--skip-sys-schema](#page-74-1)

| Command-Line Format | skip-sys-schema |
|---------------------|-----------------|
|---------------------|-----------------|

| Type          | Boolean |
|---------------|---------|
| Default Value | FALSE   |

By default, [mysql\\_upgrade](#page-65-0) installs the sys schema if it is not installed, and upgrades it to the current version otherwise. The [--skip-sys-schema](#page-74-1) option suppresses this behavior.

<span id="page-75-0"></span>• [--socket=](#page-75-0)path, -S path

| Command-Line Format | socket={file_name pipe_name} |  |
|---------------------|------------------------------|--|
| Type                | String                       |  |

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe to use.

On Windows, this option applies only if the server was started with the named\_pipe system variable enabled to support named-pipe connections. In addition, the user making the connection must be a member of the Windows group specified by the named\_pipe\_full\_access\_group system variable.

<span id="page-75-1"></span>• --ssl\*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate where to find SSL keys and certificates. See [Command Options for Encrypted Connections](#page-11-1).

<span id="page-75-2"></span>• [--ssl-fips-mode={OFF|ON|STRICT}](#page-75-2)

| Command-Line Format | ssl-fips-mode={OFF ON STRICT} |
|---------------------|-------------------------------|
| Deprecated          | Yes                           |
| Type                | Enumeration                   |
| Default Value       | OFF                           |
| Valid Values        | OFF                           |
|                     | ON                            |
|                     | STRICT                        |

Controls whether to enable FIPS mode on the client side. The [--ssl-fips-mode](#page-75-2) option differs from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to affect which cryptographic operations to permit. See Section 8.8, "FIPS Support".

These [--ssl-fips-mode](#page-75-2) values are permitted:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_75_Picture_16.jpeg)

### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for [--ssl-fips-mode](#page-75-2) is OFF. In this case, setting [--ssl-fips-mode](#page-75-2) to ON or STRICT causes the client to produce a warning at startup and to operate in non-FIPS mode.

As of MySQL 8.0.34, this option is deprecated. Expect it to be removed in a future version of MySQL.

<span id="page-76-1"></span>• [--tls-ciphersuites=](#page-76-1)ciphersuite\_list

| Command-Line Format | tls-ciphersuites=ciphersuite_list |
|---------------------|-----------------------------------|
| Type                | String                            |

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one or more colon-separated ciphersuite names. The ciphersuites that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

This option was added in MySQL 8.0.16.

<span id="page-76-2"></span>• [--tls-version=](#page-76-2)protocol\_list

| Command-Line Format | tls-version=protocol_list                                  |
|---------------------|------------------------------------------------------------|
| Type                | String                                                     |
| Default Value       | TLSv1,TLSv1.1,TLSv1.2,TLSv1.3<br>(OpenSSL 1.1.1 or higher) |
|                     | TLSv1,TLSv1.1,TLSv1.2 (otherwise)                          |

The permissible TLS protocols for encrypted connections. The value is a list of one or more commaseparated protocol names. The protocols that can be named for this option depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-76-0"></span>• [--upgrade-system-tables](#page-76-0), -s

| Command-Line Format | upgrade-system-tables |  |
|---------------------|-----------------------|--|
| Type                | Boolean               |  |

Upgrade only the system tables in the mysql schema, do not upgrade user schemas.

<span id="page-76-3"></span>• --user=[user\\_name](#page-76-3), -u user\_name

| Command-Line Format | user=name |
|---------------------|-----------|
| Type                | String    |

The user name of the MySQL account to use for connecting to the server. The default user name is root.

<span id="page-76-4"></span>• [--verbose](#page-76-4)

| Command-Line Format | verbose |
|---------------------|---------|
| Type                | Boolean |

Verbose mode. Print more information about what the program does.

<span id="page-76-5"></span>• [--version-check](#page-76-5), -k

| Command-Line Format | version-check |  |
|---------------------|---------------|--|
| Type                | Boolean       |  |

Check the version of the server to which [mysql\\_upgrade](#page-65-0) is connecting to verify that it is the same as the version for which [mysql\\_upgrade](#page-65-0) was built. If not, [mysql\\_upgrade](#page-65-0) exits. This option is enabled by default; to disable the check, use --skip-version-check.

### <span id="page-77-1"></span>• [--write-binlog](#page-77-1)

| Command-Line Format | write-binlog |  |
|---------------------|--------------|--|
| Type                | Boolean      |  |
| Default Value       | OFF          |  |

By default, binary logging by [mysql\\_upgrade](#page-65-0) is disabled. Invoke the program with [--write](#page-77-1)[binlog](#page-77-1) if you want its actions to be written to the binary log.

When the server is running with global transaction identifiers (GTIDs) enabled (gtid\_mode=ON), do not enable binary logging by [mysql\\_upgrade](#page-65-0).

### <span id="page-77-2"></span>• [--zstd-compression-level=](#page-77-2)level

| Command-Line Format | zstd-compression-level=# |  |
|---------------------|--------------------------|--|
| Type                | Integer                  |  |

The compression level to use for connections to the server that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. The compression level setting has no effect on connections that do not use zstd compression.

For more information, see [Section 6.2.8, "Connection Compression Control"](#page-32-0).

This option was added in MySQL 8.0.18.