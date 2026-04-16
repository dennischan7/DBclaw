---
source: MySQL 8.4 Reference
title: 00_Overview
---

Applications can use the following guidelines to perform SQL-based auditing that ties database activity to MySQL accounts.

MySQL accounts correspond to rows in the mysql.user system table. When a client connects successfully, the server authenticates the client to a particular row in this table. The User and Host column values in this row uniquely identify the account and correspond to the 'user\_name'@'host\_name' format in which account names are written in SQL statements.

The account used to authenticate a client determines which privileges the client has. Normally, the CURRENT\_USER() function can be invoked to determine which account this is for the client user. Its value is constructed from the User and Host columns of the user table row for the account.

However, there are circumstances under which the CURRENT\_USER() value corresponds not to the client user but to a different account. This occurs in contexts when privilege checking is not based the client's account:

- Stored routines (procedures and functions) defined with the SQL SECURITY DEFINER characteristic
- Views defined with the SQL SECURITY DEFINER characteristic
- Triggers and events

In those contexts, privilege checking is done against the DEFINER account and CURRENT\_USER() refers to that account, not to the account for the client who invoked the stored routine or view or who caused the trigger to activate. To determine the invoking user, you can call the USER() function, which returns a value indicating the actual user name provided by the client and the host from which the client connected. However, this value does not necessarily correspond directly to an account in the user table, because the USER() value never contains wildcards, whereas account values (as returned by CURRENT\_USER()) may contain user name and host name wildcards.

For example, a blank user name matches any user, so an account of ''@'localhost' enables clients to connect as an anonymous user from the local host with any user name. In this case, if a client connects as user1 from the local host, USER() and CURRENT\_USER() return different values:

```
mysql> SELECT USER(), CURRENT_USER();
+-----------------+----------------+
| USER() | CURRENT_USER() |
+-----------------+----------------+
| user1@localhost | @localhost |
+-----------------+----------------+
```

The host name part of an account can also contain wildcards. If the host name contains a '%' or '\_' pattern character or uses netmask notation, the account can be used for clients connecting from multiple hosts and the CURRENT\_USER() value does not indicate which one. For example, the account 'user2'@'%.example.com' can be used by user2 to connect from any host in the example.com domain. If user2 connects from remote.example.com, USER() and CURRENT\_USER() return different values:

```
mysql> SELECT USER(), CURRENT_USER();
+--------------------------+---------------------+
| USER() | CURRENT_USER() |
+--------------------------+---------------------+
| user2@remote.example.com | user2@%.example.com |
+--------------------------+---------------------+
```

If an application must invoke USER() for user auditing (for example, if it does auditing from within triggers) but must also be able to associate the USER() value with an account in the user table, it is necessary to avoid accounts that contain wildcards in the User or Host column. Specifically, do not permit User to be empty (which creates an anonymous-user account), and do not permit pattern characters or netmask notation in Host values. All accounts must have a nonempty User value and literal Host value.

With respect to the previous examples, the ''@'localhost' and 'user2'@'%.example.com' accounts should be changed not to use wildcards:

```
RENAME USER ''@'localhost' TO 'user1'@'localhost';
RENAME USER 'user2'@'%.example.com' TO 'user2'@'remote.example.com';
```

If user2 must be able to connect from several hosts in the example.com domain, there should be a separate account for each host.

To extract the user name or host name part from a CURRENT\_USER() or USER() value, use the SUBSTRING\_INDEX() function:

```
mysql> SELECT SUBSTRING_INDEX(CURRENT_USER(),'@',1);
+---------------------------------------+
| SUBSTRING_INDEX(CURRENT_USER(),'@',1) |
+---------------------------------------+
```

```
| user1 |
+---------------------------------------+
mysql> SELECT SUBSTRING_INDEX(CURRENT_USER(),'@',-1);
+----------------------------------------+
| SUBSTRING_INDEX(CURRENT_USER(),'@',-1) |
+----------------------------------------+
| localhost |
+----------------------------------------+
```

# <span id="page-66-0"></span>**8.3 Using Encrypted Connections**

With an unencrypted connection between the MySQL client and the server, someone with access to the network could watch all your traffic and inspect the data being sent or received between client and server.

When you must move information over a network in a secure fashion, an unencrypted connection is unacceptable. To make any kind of data unreadable, use encryption. Encryption algorithms must include security elements to resist many kinds of known attacks such as changing the order of encrypted messages or replaying data twice.

MySQL supports encrypted connections between clients and the server using the TLS (Transport Layer Security) protocol. TLS is sometimes referred to as SSL (Secure Sockets Layer) but MySQL does not actually use the SSL protocol for encrypted connections because its encryption is weak (see [Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers"](#page-75-0)).

TLS uses encryption algorithms to ensure that data received over a public network can be trusted. It has mechanisms to detect data change, loss, or replay. TLS also incorporates algorithms that provide identity verification using the X.509 standard.

X.509 makes it possible to identify someone on the Internet. In basic terms, there should be some entity called a "Certificate Authority" (or CA) that assigns electronic certificates to anyone who needs them. Certificates rely on asymmetric encryption algorithms that have two encryption keys (a public key and a secret key). A certificate owner can present the certificate to another party as proof of identity. A certificate consists of its owner's public key. Any data encrypted using this public key can be decrypted only using the corresponding secret key, which is held by the owner of the certificate.

Support for encrypted connections in MySQL is provided using OpenSSL. For information about the encryption protocols and ciphers that OpenSSL supports, see [Section 8.3.2, "Encrypted Connection](#page-75-0) [TLS Protocols and Ciphers".](#page-75-0)

By default, MySQL instances link to an available installed OpenSSL library at runtime for support of encrypted connections and other encryption-related operations. You may compile MySQL from source and use the WITH\_SSL CMake option to specify the path to a particular installed OpenSSL version or an alternative OpenSSL system package. In that case, MySQL selects that version. For instructions to do this, see Section 2.8.6, "Configuring SSL Library Support".

You can check what version of the OpenSSL library is in use at runtime using the Tls\_library\_version system status variable.

If you compile MySQL with one version of OpenSSL and want to change to a different version without recompiling, you may do this by editing the dynamic library loader path (LD\_LIBRARY\_PATH on Unix systems or PATH on Windows systems). Remove the path to the compiled version of OpenSSL, and add the path to the replacement version, placing it before any other OpenSSL libraries on the path. At startup, when MySQL cannot find the version of OpenSSL specified with WITH\_SSL on the path, it uses the first version specified on the path instead.

By default, MySQL programs attempt to connect using encryption if the server supports encrypted connections, falling back to an unencrypted connection if an encrypted connection cannot be established. For information about options that affect use of encrypted connections, see [Section 8.3.1,](#page-67-0) ["Configuring MySQL to Use Encrypted Connections"](#page-67-0) and Command Options for Encrypted Connections.

MySQL performs encryption on a per-connection basis, and use of encryption for a given user can be optional or mandatory. This enables you to choose an encrypted or unencrypted connection according to the requirements of individual applications. For information on how to require users to use encrypted connections, see the discussion of the REQUIRE clause of the CREATE USER statement in Section 15.7.1.3, "CREATE USER Statement". See also the description of the require\_secure\_transport system variable at Section 7.1.8, "Server System Variables"

Encrypted connections can be used between source and replica servers. See Section 19.3.1, "Setting Up Replication to Use Encrypted Connections".

For information about using encrypted connections from the MySQL C API, see [Support for Encrypted](https://dev.mysql.com/doc/c-api/8.4/en/c-api-encrypted-connections.md) [Connections.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-encrypted-connections.md)

It is also possible to connect using encryption from within an SSH connection to the MySQL server host. For an example, see [Section 8.3.4, "Connecting to MySQL Remotely from Windows with SSH".](#page-89-0)

# <span id="page-67-0"></span>**8.3.1 Configuring MySQL to Use Encrypted Connections**

Several configuration parameters are available to indicate whether to use encrypted connections, and to specify the appropriate certificate and key files. This section provides general guidance about configuring the server and clients for encrypted connections:

- [Server-Side Startup Configuration for Encrypted Connections](#page-67-1)
- [Server-Side Runtime Configuration and Monitoring for Encrypted Connections](#page-68-0)
- [Client-Side Configuration for Encrypted Connections](#page-70-0)
- [Configuring Certificate Validation Enforcement](#page-73-0)
- [Configuring Encrypted Connections as Mandatory](#page-74-0)

Encrypted connections also can be used in other contexts, as discussed in these additional sections:

- Between source and replica replication servers. See Section 19.3.1, "Setting Up Replication to Use Encrypted Connections".
- Among Group Replication servers. See Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer (SSL)".
- By client programs that are based on the MySQL C API. See [Support for Encrypted Connections.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-encrypted-connections.md)

Instructions for creating any required certificate and key files are available in [Section 8.3.3, "Creating](#page-81-0) [SSL and RSA Certificates and Keys"](#page-81-0).

# <span id="page-67-1"></span>**Server-Side Startup Configuration for Encrypted Connections**

To require that clients connect using encrypted connections, enable the require\_secure\_transport system variable. See [Configuring Encrypted Connections as](#page-74-0) [Mandatory](#page-74-0).

These system variables on the server side specify the certificate and key files the server uses when permitting clients to establish encrypted connections:

- ssl\_ca: The path name of the Certificate Authority (CA) certificate file. (ssl\_capath is similar but specifies the path name of a directory of CA certificate files.)
- ssl\_cert: The path name of the server public key certificate file. This certificate can be sent to the client and authenticated against the CA certificate that it has.
- ssl\_key: The path name of the server private key file.

For example, to enable the server for encrypted connections, start it with these lines in the my.cnf file, changing the file names as necessary:

```
[mysqld]
ssl_ca=ca.pem
ssl_cert=server-cert.pem
ssl_key=server-key.pem
```

To specify in addition that clients are required to use encrypted connections, enable the require\_secure\_transport system variable:

```
[mysqld]
ssl_ca=ca.pem
ssl_cert=server-cert.pem
ssl_key=server-key.pem
require_secure_transport=ON
```

Each certificate and key system variable names a file in PEM format. Should you need to create the required certificate and key files, see [Section 8.3.3, "Creating SSL and RSA Certificates and](#page-81-0) [Keys".](#page-81-0) MySQL servers compiled using OpenSSL can generate missing certificate and key files automatically at startup. See [Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using](#page-81-1) [MySQL".](#page-81-1) Alternatively, if you have a MySQL source distribution, you can test your setup using the demonstration certificate and key files in its mysql-test/std\_data directory.

The server performs certificate and key file autodiscovery. If no explicit encrypted-connection options are given to configure encrypted connections, the server attempts to enable encrypted-connection support automatically at startup:

- If the server discovers valid certificate and key files named ca.pem, server-cert.pem, and server-key.pem in the data directory, it enables support for encrypted connections by clients. (The files need not have been generated automatically; what matters is that they have those names and are valid.)
- If the server does not find valid certificate and key files in the data directory, it continues executing but without support for encrypted connections.

If the server automatically enables encrypted connection support, it writes a note to the error log. If the server discovers that the CA certificate is self-signed, it writes a warning to the error log. (The certificate is self-signed if created automatically by the server.)

MySQL also provides these system variables for server-side encrypted-connection control:

- ssl\_cipher: The list of permissible ciphers for connection encryption.
- ssl\_crl: The path name of the file containing certificate revocation lists. (ssl\_crlpath is similar but specifies the path name of a directory of certificate revocation-list files.)
- tls\_version, tls\_ciphersuites: Which encryption protocols and ciphersuites the server permits for encrypted connections; see [Section 8.3.2, "Encrypted Connection TLS Protocols and](#page-75-0) [Ciphers".](#page-75-0) For example, you can configure tls\_version to prevent clients from using less-secure protocols.

If the server cannot create a valid TLS context from the system variables for server-side encryptedconnection control, the server executes without support for encrypted connections.

# <span id="page-68-0"></span>**Server-Side Runtime Configuration and Monitoring for Encrypted Connections**

The tls\_xxx and ssl\_xxx system variables are dynamic and can be set at runtime, not just at startup. If changed with SET GLOBAL, the new values apply only until server restart. If changed with SET PERSIST, the new values also carry over to subsequent server restarts. See Section 15.7.6.1, "SET Syntax for Variable Assignment". However, runtime changes to these variables do not immediately affect the TLS context for new connections, as explained later in this section.

Along with the change that enables runtime changes to the TLS context-related system variables, the server enables runtime updates to the actual TLS context used for new connections. This capability may be useful, for example, to avoid restarting a MySQL server that has been running so long that its SSL certificate has expired.

To create the initial TLS context, the server uses the values that the context-related system variables have at startup. To expose the context values, the server also initializes a set of corresponding status variables. The following table shows the system variables that define the TLS context and the corresponding status variables that expose the currently active context values.

**Table 8.12 System and Status Variables for Server Main Connection Interface TLS Context**

| System Variable Name | Corresponding Status Variable Name |
|----------------------|------------------------------------|
| ssl_ca               | Current_tls_ca                     |
| ssl_capath           | Current_tls_capath                 |
| ssl_cert             | Current_tls_cert                   |
| ssl_cipher           | Current_tls_cipher                 |
| ssl_crl              | Current_tls_crl                    |
| ssl_crlpath          | Current_tls_crlpath                |
| ssl_key              | Current_tls_key                    |
| tls_ciphersuites     | Current_tls_ciphersuites           |
| tls_version          | Current_tls_version                |

Those active TLS context values are also exposed as properties in the Performance Schema tls\_channel\_status table, along with the properties for any other active TLS contexts.

To reconfigure the TLS context at runtime, use this procedure:

- 1. Set each TLS context-related system variable that should be changed to its new value.
- 2. Execute ALTER INSTANCE RELOAD TLS. This statement reconfigures the active TLS context from the current values of the TLS context-related system variables. It also sets the contextrelated status variables to reflect the new active context values. The statement requires the CONNECTION\_ADMIN privilege.
- 3. New connections established after execution of ALTER INSTANCE RELOAD TLS use the new TLS context. Existing connections remain unaffected. If existing connections should be terminated, use the KILL statement.

The members of each pair of system and status variables may have different values temporarily due to the way the reconfiguration procedure works:

- Changes to the system variables prior to ALTER INSTANCE RELOAD TLS do not change the TLS context. At this point, those changes have no effect on new connections, and corresponding context-related system and status variables may have different values. This enables you to make any changes required to individual system variables, then update the active TLS context atomically with ALTER INSTANCE RELOAD TLS after all system variable changes have been made.
- After ALTER INSTANCE RELOAD TLS, corresponding system and status variables have the same values. This remains true until the next change to the system variables.

In some cases, ALTER INSTANCE RELOAD TLS by itself may suffice to reconfigure the TLS context, without changing any system variables. Suppose that the certificate in the file named by ssl\_cert has expired. It is sufficient to replace the existing file contents with a nonexpired certificate and execute ALTER INSTANCE RELOAD TLS to cause the new file contents to be read and used for new connections.

The server implements independent connection-encryption configuration for the administrative connection interface. See Administrative Interface Support for Encrypted Connections. In addition, ALTER INSTANCE RELOAD TLS is extended with a FOR CHANNEL clause that enables specifying the channel (interface) for which to reload the TLS context. See Section 15.1.5, "ALTER INSTANCE Statement". There are no status variables to expose the administrative interface TLS context, but the Performance Schema tls\_channel\_status table exposes TLS properties for both the main and administrative interfaces. See Section 29.12.22.9, "The tls\_channel\_status Table".

Updating the main interface TLS context has these effects:

- The update changes the TLS context used for new connections on the main connection interface.
- The update also changes the TLS context used for new connections on the administrative interface unless some nondefault TLS parameter value is configured for that interface.
- The update does not affect the TLS context used by other enabled server plugins or components such as Group Replication or X Plugin:
  - To apply the main interface reconfiguration to Group Replication's group communication connections, which take their settings from the server's TLS context-related system variables, you must execute STOP GROUP\_REPLICATION followed by START GROUP\_REPLICATION to stop and restart Group Replication.
  - X Plugin initializes its TLS context at plugin initialization as described at Section 22.5.3, "Using Encrypted Connections with X Plugin". This context does not change thereafter.

By default, the RELOAD TLS action rolls back with an error and has no effect if the configuration values do not permit creation of the new TLS context. The previous context values continue to be used for new connections. If the optional NO ROLLBACK ON ERROR clause is given and the new context cannot be created, rollback does not occur. Instead, a warning is generated and encryption is disabled for new connections on the interface to which the statement applies.

Options that enable or disable encrypted connections on a connection interface have an effect only at startup. For example, the --tls-version and --admin-tls-version options affect only at startup whether the main and administrative interfaces support those TLS versions. Such options are ignored and have no effect on the operation of ALTER INSTANCE RELOAD TLS at runtime. For example, you can set tls\_version='' to start the server with encrypted connections disabled on the main interface, then reconfigure TLS and execute ALTER INSTANCE RELOAD TLS to enable encrypted connections at runtime.

# <span id="page-70-0"></span>**Client-Side Configuration for Encrypted Connections**

For a complete list of client options related to establishment of encrypted connections, see Command Options for Encrypted Connections.

By default, MySQL client programs attempt to establish an encrypted connection if the server supports encrypted connections, with further control available through the --ssl-mode option:

- In the absence of an --ssl-mode option, clients attempt to connect using encryption, falling back to an unencrypted connection if an encrypted connection cannot be established. This is also the behavior with an explicit --ssl-mode=PREFERRED option.
- With --ssl-mode=REQUIRED, clients require an encrypted connection and fail if one cannot be established.
- With --ssl-mode=DISABLED, clients use an unencrypted connection.
- With --ssl-mode=VERIFY\_CA or --ssl-mode=VERIFY\_IDENTITY, clients require an encrypted connection, and also perform verification against the server CA certificate and (with VERIFY\_IDENTITY) against the server host name in its certificate.

![](_page_70_Picture_17.jpeg)

#### **Important**

The default setting, --ssl-mode=PREFERRED, produces an encrypted connection if the other default settings are unchanged. However, to help prevent sophisticated man-in-the-middle attacks, it is important for the client to verify the server's identity. The settings --ssl-mode=VERIFY\_CA and --sslmode=VERIFY\_IDENTITY are a better choice than the default setting to help prevent this type of attack. VERIFY\_CA makes the client check that the server's certificate is valid. VERIFY\_IDENTITY makes the client check that the server's certificate is valid, and also makes the client check that the host name the client is using matches the identity in the server's certificate. To implement one of these settings, you must first ensure that the CA certificate for the server is reliably available to all the clients that use it in your environment, otherwise availability issues will result. For this reason, they are not the default setting.

Attempts to establish an unencrypted connection fail if the require\_secure\_transport system variable is enabled on the server side to cause the server to require encrypted connections. See [Configuring Encrypted Connections as Mandatory.](#page-74-0)

The following options on the client side identify the certificate and key files clients use when establishing encrypted connections to the server. They are similar to the ssl\_ca, ssl\_cert, and ssl\_key system variables used on the server side, but --ssl-cert and --ssl-key identify the client public and private key:

- --ssl-ca: The path name of the Certificate Authority (CA) certificate file. This option, if used, must specify the same certificate used by the server. (--ssl-capath is similar but specifies the path name of a directory of CA certificate files.)
- --ssl-cert: The path name of the client public key certificate file.
- --ssl-key: The path name of the client private key file.

For additional security relative to that provided by the default encryption, clients can supply a CA certificate matching the one used by the server and enable host name identity verification. In this way, the server and client place their trust in the same CA certificate and the client verifies that the host to which it connected is the one intended:

- To specify the CA certificate, use --ssl-ca (or --ssl-capath), and specify --sslmode=VERIFY\_CA.
- To enable host name identity verification as well, use --ssl-mode=VERIFY\_IDENTITY rather than --ssl-mode=VERIFY\_CA.

![](_page_71_Picture_10.jpeg)

### **Note**

Host name identity verification with VERIFY\_IDENTITY does not work with self-signed certificates that are created automatically by the server (see [Section 8.3.3.1, "Creating SSL and RSA Certificates and Keys using MySQL"](#page-81-1)). Such self-signed certificates do not contain the server name as the Common Name value.

MySQL also provides these options for client-side encrypted-connection control:

- --ssl-cipher: The list of permissible ciphers for connection encryption.
- --ssl-crl: The path name of the file containing certificate revocation lists. (--ssl-crlpath is similar but specifies the path name of a directory of certificate revocation-list files.)
- --tls-version, --tls-ciphersuites: The permitted encryption protocols and ciphersuites; see [Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers"](#page-75-0).

Depending on the encryption requirements of the MySQL account used by a client, the client may be required to specify certain options to connect using encryption to the MySQL server.

Suppose that you want to connect using an account that has no special encryption requirements or that was created using a CREATE USER statement that included the REQUIRE SSL clause. Assuming that the server supports encrypted connections, a client can connect using encryption with no --ssl-mode option or with an explicit --ssl-mode=PREFERRED option:

mysql

Or:

```
mysql --ssl-mode=PREFERRED
```

For an account created with a REQUIRE SSL clause, the connection attempt fails if an encrypted connection cannot be established. For an account with no special encryption requirements, the attempt falls back to an unencrypted connection if an encrypted connection cannot be established. To prevent fallback and fail if an encrypted connection cannot be obtained, connect like this:

```
mysql --ssl-mode=REQUIRED
```

If the account has more stringent security requirements, other options must be specified to establish an encrypted connection:

• For accounts created with a REQUIRE X509 clause, clients must specify at least --ssl-cert and --ssl-key. In addition, --ssl-ca (or --ssl-capath) is recommended so that the public certificate provided by the server can be verified. For example (enter the command on a single line):

```
mysql --ssl-ca=ca.pem
 --ssl-cert=client-cert.pem
 --ssl-key=client-key.pem
```

• For accounts created with a REQUIRE ISSUER or REQUIRE SUBJECT clause, the encryption requirements are the same as for REQUIRE X509, but the certificate must match the issue or subject, respectively, specified in the account definition.

For additional information about the REQUIRE clause, see Section 15.7.1.3, "CREATE USER Statement".

MySQL servers can generate client certificate and key files that clients can use to connect to MySQL server instances. See [Section 8.3.3, "Creating SSL and RSA Certificates and Keys"](#page-81-0).

![](_page_72_Picture_12.jpeg)

#### **Important**

If a client connecting to a MySQL server instance uses an SSL certificate with the extendedKeyUsage extension (an X.509 v3 extension), the extended key usage must include client authentication (clientAuth). If the SSL certificate is only specified for server authentication (serverAuth) and other non-client certificate purposes, certificate verification fails and the client connection to the MySQL server instance fails. There is no extendedKeyUsage extension in SSL certificates generated by MySQL Server (as described in [Section 8.3.3.1,](#page-81-1) ["Creating SSL and RSA Certificates and Keys using MySQL"](#page-81-1)), and SSL certificates created using the openssl command following the instructions in [Section 8.3.3.2, "Creating SSL Certificates and Keys Using openssl"](#page-83-0). If you use your own client certificate created in another way, ensure any extendedKeyUsage extension includes client authentication.

To prevent use of encryption and override other --ssl-xxx options, invoke the client program with - ssl-mode=DISABLED:

```
mysql --ssl-mode=DISABLED
```

To determine whether the current connection with the server uses encryption, check the session value of the Ssl\_cipher status variable. If the value is empty, the connection is not encrypted. Otherwise, the connection is encrypted and the value indicates the encryption cipher. For example:

```
mysql> SHOW SESSION STATUS LIKE 'Ssl_cipher';
+---------------+---------------------------+
| Variable_name | Value |
+---------------+---------------------------+
| Ssl_cipher | DHE-RSA-AES128-GCM-SHA256 |
+---------------+---------------------------+
```

For the mysql client, an alternative is to use the STATUS or \s command and check the SSL line:

```
mysql> \s
...
SSL: Not in use
...
```

#### Or:

```
mysql> \s
...
SSL: Cipher in use is DHE-RSA-AES128-GCM-SHA256
...
```

# <span id="page-73-0"></span>**Configuring Certificate Validation Enforcement**

The --tls-certificates-enforced-validation option enables validation of the server public key certificate file, Certificate Authority (CA) certificate files, and certificate revocation-list files at server startup:

```
mysqld --tls-certificates-enforced-validation
```

If set to ON, the server stops execution of the startup in case of invalid certificates. The server informs DBAs by providing valid debug messages, error messages, or both depending on the status of the certificates. This capability may be useful, for example, to avoid restarting a MySQL server that has been running so long that its SSL certificate has expired.

Similarly, when you execute the ALTER INSTANCE RELOAD TLS statement to change the TLS context at runtime, the new server and CA certificate files are not used if validation fails. The server continues to use the old certificates in this case. For more information about changing the TLS context dynamically, see [Server-Side Runtime Configuration and Monitoring for Encrypted Connections](#page-68-0).

#### **Validating CA Certificates**

For a connection using the server main interface:

- If --ssl\_ca is specified, then the server validates the respective CA certificate and gives the DBA an appropriate warning message.
- If --ssl\_capath is specified, then the server validates all the CA certificates in the respective folder and gives the DBA an appropriate warning message.
- If SSL parameters are not specified, by default the server validates the CA certificate present in the data directory and gives the DBA an appropriate warning message.

For a connection using the server administrative interface:

- If --admin\_ssl\_ca is specified, then the server validates the respective CA certificate and gives the DBA an appropriate warning message.
- If --admin\_ssl\_capath is specified, then the server validates all of the CA certificates in the respective folder and gives the DBA an appropriate warning message.
- If administrative SSL parameters are not specified, by default the server validates the CA certificate present in the data directory and gives the DBA an appropriate warning message.

#### **Validating the Server Certificate**

For a connection using the server main interface:

- If --ssl\_cert is not specified, then the server validates the server certificate in default data directory.
- If --ssl\_cert is given, then the server validates the server certificate, taking into consideration ssl\_crl, if specified.

• If a DBA sets the command-line option to validate certificates, then the server stops in case of invalid certificates and an appropriate error message is displayed to the DBA. Otherwise, the server emits warning messages to the DBA and the server starts.

For a connection using the server administrative interface:

- If --admin\_ssl\_cert is not specified, then the server validates the server certificate in default data directory.
- If --admin\_ssl\_cert is given, then the server validates the server certificate, taking into consideration --admin\_ssl\_crl, if specified.
- If a DBA sets the command-line option to validate certificates, then the server stops in case of invalid certificates and an appropriate error message is displayed to the DBA. Otherwise, the server emits warning messages to the DBA and the server starts.

# <span id="page-74-0"></span>**Configuring Encrypted Connections as Mandatory**

For some MySQL deployments it may be not only desirable but mandatory to use encrypted connections (for example, to satisfy regulatory requirements). This section discusses configuration settings that enable you to do this. These levels of control are available:

- You can configure the server to require that clients connect using encrypted connections.
- You can invoke individual client programs to require an encrypted connection, even if the server permits but does not require encryption.
- You can configure individual MySQL accounts to be usable only over encrypted connections.

To require that clients connect using encrypted connections, enable the require\_secure\_transport system variable. For example, put these lines in the server my.cnf file:

```
[mysqld]
require_secure_transport=ON
```

Alternatively, to set and persist the value at runtime, use this statement:

```
SET PERSIST require_secure_transport=ON;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to be used for subsequent server restarts. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

With require\_secure\_transport enabled, client connections to the server are required to use some form of secure transport, and the server permits only TCP/IP connections that use SSL, or connections that use a socket file (on Unix) or shared memory (on Windows). The server rejects nonsecure connection attempts, which fail with an [ER\\_SECURE\\_TRANSPORT\\_REQUIRED](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_secure_transport_required) error.

To invoke a client program such that it requires an encrypted connection whether or not the server requires encryption, use an --ssl-mode option value of REQUIRED, VERIFY\_CA, or VERIFY\_IDENTITY. For example:

```
mysql --ssl-mode=REQUIRED
mysqldump --ssl-mode=VERIFY_CA
mysqladmin --ssl-mode=VERIFY_IDENTITY
```

To configure a MySQL account to be usable only over encrypted connections, include a REQUIRE clause in the CREATE USER statement that creates the account, specifying in that clause the encryption characteristics you require. For example, to require an encrypted connection and the use of a valid X.509 certificate, use REQUIRE X509:

```
CREATE USER 'jeffrey'@'localhost' REQUIRE X509;
```

For additional information about the REQUIRE clause, see Section 15.7.1.3, "CREATE USER Statement".

To modify existing accounts that have no encryption requirements, use the ALTER USER statement.

# <span id="page-75-0"></span>**8.3.2 Encrypted Connection TLS Protocols and Ciphers**

MySQL supports multiple TLS protocols and ciphers, and enables configuring which protocols and ciphers to permit for encrypted connections. It is also possible to determine which protocol and cipher the current session uses.

- [Supported TLS Protocols](#page-75-1)
- [Removal of Support for the TLSv1 and TLSv1.1 Protocols](#page-76-0)
- [Connection TLS Protocol Configuration](#page-76-1)
- [Connection Cipher Configuration](#page-77-0)
- [Connection TLS Protocol Negotiation](#page-80-0)
- [Monitoring Current Client Session TLS Protocol and Cipher](#page-81-2)

# <span id="page-75-1"></span>**Supported TLS Protocols**

MySQL 8.4 supports the TLSv1.2 and TLSv1.3 protocols for connections. To use TLSv1.3, both the MySQL server and the client application must be compiled using OpenSSL 1.1.1 or higher. The Group Replication component supports TLSv1.3 from MySQL 8.0.18 (for details, see Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer (SSL)").

MySQL 8.4 does not support the old TLSv1 and TLSv1.1 protocols.

Permitted TLS protocols can be configured on both the server side and client side to include only a subset of the supported TLS protocols. The configuration on both sides must include at least one protocol in common or connection attempts cannot negotiate a protocol to use. For details, see [Connection TLS Protocol Negotiation.](#page-80-0)

The host system may permit only certain TLS protocols, which means that MySQL connections cannot use protocols not allowed by the host even if MySQL itself permits them. Possible workarounds for this issue include the following:

• Change the system-wide host configuration to permit additional TLS protocols. Consult your operating system documentation for instructions. For example, your system may have an /etc/ ssl/openssl.cnf file that contains these lines to restrict TLS protocols to TLSv1.3 or higher:

```
[system_default_sect]
MinProtocol = TLSv1.3
```

Changing the value to a lower protocol version or None makes the system more permissive. This workaround has the disadvantage that permitting lower (less secure) protocols may have adverse security consequences.

• If you cannot or prefer not to change the host system TLS configuration, change MySQL applications to use higher (more secure) TLS protocols that are permitted by the host system. This may not be possible for older versions of MySQL that support only lower protocol versions. For example, TLSv1 is the only supported protocol prior to MySQL 5.6.46, so attempts to connect to a pre-5.6.46 server fail even if the client is from a newer MySQL version that supports higher protocol versions. In such cases, an upgrade to a version of MySQL that supports additional TLS versions may be required.

- System-wide host configuration If the MySQL configuration permits TLSv1.2, and your host system configuration permits only connections that use TLSv1.2 or higher, you can establish MySQL connections using TLSv1.2 only.
  - Suppose the MySQL configuration permits TLSv1.2, but your host system configuration permits only connections that use

TLSv1.3 or higher. If this is the case, you cannot establish MySQL connections at all, because no protocol permitted by MySQL is permitted by the host system.

# <span id="page-76-0"></span>**Removal of Support for the TLSv1 and TLSv1.1 Protocols**

Support for the TLSv1 and TLSv1.1 connection protocols was deprecated and removed in MySQL 8.0. For background information, refer to [RFC 8996](https://tools.ietf.org/html/rfc8996) (Deprecating TLS 1.0 and TLS 1.1). In MySQL 8.4, connections can be made using only the more secure TLSv1.2 and TLSv1.3 protocols. TLSv1.3 requires that both the MySQL server and the client application are compiled with OpenSSL 1.1.1.

For more information, see Does MySQL 8.4 support TLS 1.0 and 1.1?

# <span id="page-76-1"></span>**Connection TLS Protocol Configuration**

On the server side, the value of the tls\_version system variable determines which TLS protocols a MySQL server permits for encrypted connections. The tls\_version value applies to connections from clients, regular source/replica replication connections where this server instance is the source, Group Replication group communication connections, and Group Replication distributed recovery connections where this server instance is the donor. The administrative connection interface is configured similarly, but uses the admin\_tls\_version system variable (see Section 7.1.12.2, "Administrative Connection Management"). This discussion applies to admin\_tls\_version as well.

The tls\_version value is a list of one or more comma-separated TLS protocol versions, which is not case-sensitive. By default, this variable lists all protocols that are supported by the SSL library used to compile MySQL and by the MySQL Server release. The default settings are therefore as shown in [MySQL Server TLS Protocol Default Settings.](https://dev.mysql.com/doc/refman/8.0/en/encrypted-connection-protocols-ciphers.md#tls-support-defaults)

To determine the value of tls\_version at runtime, use this statement:

```
mysql> SHOW GLOBAL VARIABLES LIKE 'tls_version';
+---------------+-----------------------+
| Variable_name | Value |
+---------------+-----------------------+
| tls_version | TLSv1.2,TLSv1.3 |
+---------------+-----------------------+
```

To change the value of tls\_version, set it at server startup. For example, to permit connections that use the TLSv1.2 or TLSv1.3 protocol, but prohibit connections that use any other protocol, use these lines in the server my.cnf file:

```
[mysqld]
tls_version=TLSv1.2,TLSv1.3
```

To be even more restrictive and permit only TLSv1.3 connections, set tls\_version like this:

```
[mysqld]
tls_version=TLSv1.3
```

tls\_version can be changed at runtime. See [Server-Side Runtime Configuration and Monitoring for](#page-68-0) [Encrypted Connections](#page-68-0).

On the client side, the --tls-version option specifies which TLS protocols a client program permits for connections to the server. The format of the option value is the same as for the tls\_version system variable described previously (a list of one or more comma-separated protocol versions).

For source/replica replication connections where this server instance is the replica, the SOURCE\_TLS\_VERSION option for the CHANGE REPLICATION SOURCE TO statement specifies which TLS protocols the replica permits for connections to the source. The format of the option value is the same as for the tls\_version system variable described previously. See Section 19.3.1, "Setting Up Replication to Use Encrypted Connections".

The protocols that can be specified for SOURCE\_TLS\_VERSION depend on the SSL library. This option is independent of and not affected by the server tls\_version value. For example, a server that acts

as a replica can be configured with tls\_version set to TLSv1.3 to permit only incoming connections that use TLSv1.3, but also configured with SOURCE\_TLS\_VERSION set to TLSv1.2 to permit only TLSv1.2 for outgoing replica connections to the source.

For Group Replication distributed recovery connections where this server instance is the joining member that initiates distributed recovery (that is, the client), the group\_replication\_recovery\_tls\_version system variable specifies which protocols are permitted by the client. Again, this option is independent of and not affected by the server tls\_version value, which applies when this server instance is the donor. A Group Replication server generally participates in distributed recovery both as a donor and as a joining member over the course of its group membership, so both these system variables should be set. See Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer (SSL)".

TLS protocol configuration affects which protocol a given connection uses, as described in [Connection](#page-80-0) [TLS Protocol Negotiation](#page-80-0).

Permitted protocols should be chosen such as not to leave "holes" in the list. For example, these server configuration values do not have holes:

```
tls_version=TLSv1.2,TLSv1.3
tls_version=TLSv1.3
```

The prohibition on holes also applies in other configuration contexts, such as for clients or replicas.

Unless you intend to disable encrypted connections, the list of permitted protocols should not be empty. If you set a TLS version parameter to the empty string, encrypted connections cannot be established:

- tls\_version: The server does not permit encrypted incoming connections.
- --tls-version: The client does not permit encrypted outgoing connections to the server.
- SOURCE\_TLS\_VERSION: The replica does not permit encrypted outgoing connections to the source.
- group\_replication\_recovery\_tls\_version: The joining member does not permit encrypted connections to the distributed recovery connection.

# <span id="page-77-0"></span>**Connection Cipher Configuration**

A default set of ciphers applies to encrypted connections, which can be overridden by explicitly configuring the permitted ciphers. During connection establishment, both sides of a connection must permit some cipher in common or the connection fails. Of the permitted ciphers common to both sides, the SSL library chooses the one supported by the provided certificate that has the highest priority.

To specify a cipher or ciphers applicable for encrypted connections that use TLSv1.2:

- Set the ssl\_cipher system variable on the server side, and use the --ssl-cipher option for client programs.
- For regular source/replica replication connections, where this server instance is the source, set the ssl\_cipher system variable. Where this server instance is the replica, use the SOURCE\_SSL\_CIPHER option for the CHANGE REPLICATION SOURCE TO statement. See Section 19.3.1, "Setting Up Replication to Use Encrypted Connections".
- For a Group Replication group member, for Group Replication group communication connections and also for Group Replication distributed recovery connections where this server instance is the donor, set the ssl\_cipher system variable. For Group Replication distributed recovery connections where this server instance is the joining member, use the group\_replication\_recovery\_ssl\_cipher system variable. See Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer (SSL)".

For encrypted connections that use TLSv1.3, OpenSSL 1.1.1 and higher supports the following ciphersuites, all of which are enabled by default for use with server system variables --tlsciphersuites or --admin-tls-ciphersuites:

TLS\_AES\_128\_GCM\_SHA256 TLS\_AES\_256\_GCM\_SHA384 TLS\_CHACHA20\_POLY1305\_SHA256 TLS\_AES\_128\_CCM\_SHA256

![](_page_78_Picture_2.jpeg)

#### **Note**

In MySQL 8.4, use of TLS\_AES\_128\_CCM\_8\_SHA256 with server system variables --tls-ciphersuites or --admin-tls-ciphersuites generates a deprecation warning.

To configure the permitted TLSv1.3 ciphersuites explicitly, set the following parameters. In each case, the configuration value is a list of zero or more colon-separated ciphersuite names.

- On the server side, use the tls\_ciphersuites system variable. If this variable is not set, its default value is NULL, which means that the server permits the default set of ciphersuites. If the variable is set to the empty string, no ciphersuites are enabled and encrypted connections cannot be established.
- On the client side, use the --tls-ciphersuites option. If this option is not set, the client permits the default set of ciphersuites. If the option is set to the empty string, no ciphersuites are enabled and encrypted connections cannot be established.
- For regular source/replica replication connections, where this server instance is the source, use the tls\_ciphersuites system variable. Where this server instance is the replica, use the SOURCE\_TLS\_CIPHERSUITES option for the CHANGE REPLICATION SOURCE TO statement. See Section 19.3.1, "Setting Up Replication to Use Encrypted Connections".
- For a Group Replication group member, for Group Replication group communication connections and also for Group Replication distributed recovery connections where this server instance is the donor, use the tls\_ciphersuites system variable. For Group Replication distributed recovery connections where this server instance is the joining member, use the group\_replication\_recovery\_tls\_ciphersuites system variable. See Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer (SSL)".

Ciphersuite support requires that both the MySQL server and the client application be compiled using OpenSSL 1.1.1 or higher.

A given cipher may work only with particular TLS protocols, which affects the TLS protocol negotiation process. See [Connection TLS Protocol Negotiation.](#page-80-0)

To determine which ciphers a given server supports, check the session value of the Ssl\_cipher\_list status variable:

```
SHOW SESSION STATUS LIKE 'Ssl_cipher_list';
```

The Ssl\_cipher\_list status variable lists the possible SSL ciphers (empty for non-SSL connections). If MySQL supports TLSv1.3, the value includes the possible TLSv1.3 ciphersuites.

![](_page_78_Picture_15.jpeg)

#### **Note**

ECDSA ciphers only work in combination with an SSL certificate that uses ECDSA for the digital signature, and they do not work with certificates that use RSA. MySQL Server's automatic generation process for SSL certificates does not generate ECDSA signed certificates, it generates only RSA signed certificates. Do not select ECDSA ciphers unless you have an ECDSA certificate available to you.

For encrypted connections that use TLS.v1.3, MySQL uses the SSL library default ciphersuite list.

For encrypted connections that use TLSv1.2, MySQL passes the following default cipher list to the SSL library when used with the server system variables --ssl-cipher and --admin-ssl-cipher.

```
ECDHE-ECDSA-AES128-GCM-SHA256
ECDHE-ECDSA-AES256-GCM-SHA384
ECDHE-RSA-AES128-GCM-SHA256
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-ECDSA-CHACHA20-POLY1305
ECDHE-RSA-CHACHA20-POLY1305
ECDHE-ECDSA-AES256-CCM
ECDHE-ECDSA-AES128-CCM
DHE-RSA-AES128-GCM-SHA256
DHE-RSA-AES256-GCM-SHA384
DHE-RSA-AES256-CCM
DHE-RSA-AES128-CCM
DHE-RSA-CHACHA20-POLY1305
```

#### These cipher restrictions are in place:

• The following ciphers are deprecated and produce a warning when used with the server system variables --ssl-cipher and --admin-ssl-cipher:

```
ECDHE-ECDSA-AES128-SHA256
ECDHE-RSA-AES128-SHA256
ECDHE-ECDSA-AES256-SHA384
ECDHE-RSA-AES256-SHA384
DHE-DSS-AES128-GCM-SHA256
DHE-RSA-AES128-SHA256
DHE-DSS-AES128-SHA256
DHE-DSS-AES256-GCM-SHA384
DHE-RSA-AES256-SHA256
DHE-DSS-AES256-SHA256
ECDHE-RSA-AES128-SHA
ECDHE-ECDSA-AES128-SHA
ECDHE-RSA-AES256-SHA
ECDHE-ECDSA-AES256-SHA
DHE-DSS-AES128-SHA
DHE-RSA-AES128-SHA
TLS_DHE_DSS_WITH_AES_256_CBC_SHA
DHE-RSA-AES256-SHA
AES128-GCM-SHA256
DH-DSS-AES128-GCM-SHA256
ECDH-ECDSA-AES128-GCM-SHA256
AES256-GCM-SHA384
DH-DSS-AES256-GCM-SHA384
ECDH-ECDSA-AES256-GCM-SHA384
AES128-SHA256
DH-DSS-AES128-SHA256
ECDH-ECDSA-AES128-SHA256
AES256-SHA256
DH-DSS-AES256-SHA256
ECDH-ECDSA-AES256-SHA384
AES128-SHA
DH-DSS-AES128-SHA
ECDH-ECDSA-AES128-SHA
AES256-SHA
DH-DSS-AES256-SHA
ECDH-ECDSA-AES256-SHA
DH-RSA-AES128-GCM-SHA256
ECDH-RSA-AES128-GCM-SHA256
DH-RSA-AES256-GCM-SHA384
ECDH-RSA-AES256-GCM-SHA384
DH-RSA-AES128-SHA256
ECDH-RSA-AES128-SHA256
DH-RSA-AES256-SHA256
ECDH-RSA-AES256-SHA384
ECDHE-RSA-AES128-SHA
ECDHE-ECDSA-AES128-SHA
ECDHE-RSA-AES256-SHA
ECDHE-ECDSA-AES256-SHA
DHE-DSS-AES128-SHA
DHE-RSA-AES128-SHA
TLS_DHE_DSS_WITH_AES_256_CBC_SHA
DHE-RSA-AES256-SHA
AES128-SHA
```

```
DH-DSS-AES128-SHA
ECDH-ECDSA-AES128-SHA
AES256-SHA
DH-DSS-AES256-SHA
ECDH-ECDSA-AES256-SHA
DH-RSA-AES128-SHA
ECDH-RSA-AES128-SHA
DH-RSA-AES256-SHA
ECDH-RSA-AES256-SHA
DES-CBC3-SHA
```

• The following ciphers are permanently restricted:

```
!DHE-DSS-DES-CBC3-SHA
!DHE-RSA-DES-CBC3-SHA
!ECDH-RSA-DES-CBC3-SHA
!ECDH-ECDSA-DES-CBC3-SHA
!ECDHE-RSA-DES-CBC3-SHA
!ECDHE-ECDSA-DES-CBC3-SHA
```

• The following categories of ciphers are permanently restricted:

```
!aNULL
!eNULL
!EXPORT
!LOW
!MD5
!DES
!RC2
!RC4
!PSK
!SSLv3
```

If the server is started with the ssl\_cert system variable set to a certificate that uses any of the preceding restricted ciphers or cipher categories, the server starts with support for encrypted connections disabled.

# <span id="page-80-0"></span>**Connection TLS Protocol Negotiation**

Connection attempts in MySQL negotiate use of the highest TLS protocol version available on both sides for which a protocol-compatible encryption cipher is available on both sides. The negotiation process depends on factors such as the SSL library used to compile the server and client, the TLS protocol and encryption cipher configuration, and which key size is used:

- For a connection attempt to succeed, the server and client TLS protocol configuration must permit some protocol in common.
- Similarly, the server and client encryption cipher configuration must permit some cipher in common. A given cipher may work only with particular TLS protocols, so a protocol available to the negotiation process is not chosen unless there is also a compatible cipher.
- If TLSv1.3 is available, it is used if possible. (This means that server and client configuration both must permit TLSv1.3, and both must also permit some TLSv1.3-compatible encryption cipher.) Otherwise, MySQL continues through the list of available protocols, using TLSv1.2 if possible, and so forth. Negotiation proceeds from more secure protocols to less secure. Negotiation order is independent of the order in which protocols are configured. For example, negotiation order is the same regardless of whether tls\_version has a value of TLSv1.2,TLSv1.3 or TLSv1.3,TLSv1.2.
- For better security, use a certificate with an RSA key size of at least 2048 bits.

If the server and client do not have a permitted protocol in common, and a protocol-compatible cipher in common, the server terminates the connection request.

MySQL permits specifying a list of protocols to support. This list is passed directly down to the underlying SSL library and is ultimately up to that library what protocols it actually enables from the supplied list. Please refer to the MySQL source code and the OpenSSL [SSL\\_CTX\\_new\(\)](https://www.openssl.org/docs/man1.1.0/ssl/SSL_CTX_new.md) documentation for information about how the SSL library handles this.

# <span id="page-81-2"></span>**Monitoring Current Client Session TLS Protocol and Cipher**

To determine which encryption TLS protocol and cipher the current client session uses, check the session values of the Ssl\_version and Ssl\_cipher status variables:

```
mysql> SELECT * FROM performance_schema.session_status
 WHERE VARIABLE_NAME IN ('Ssl_version','Ssl_cipher');
+---------------+---------------------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+---------------+---------------------------+
| Ssl_cipher | DHE-RSA-AES128-GCM-SHA256 |
| Ssl_version | TLSv1.2 |
+---------------+---------------------------+
```

If the connection is not encrypted, both variables have an empty value.

# <span id="page-81-0"></span>**8.3.3 Creating SSL and RSA Certificates and Keys**

The following discussion describes how to create the files required for SSL and RSA support in MySQL. File creation can be performed using facilities provided by MySQL itself, or by invoking the openssl command directly.

SSL certificate and key files enable MySQL to support encrypted connections using SSL. See [Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".](#page-67-0)

RSA key files enable MySQL to support secure password exchange over unencrypted connections for accounts authenticated by the sha256\_password (deprecated) or caching\_sha2\_password plugin. See [Section 8.4.1.3, "SHA-256 Pluggable Authentication",](#page-99-0) and [Section 8.4.1.2, "Caching SHA-2](#page-94-0) [Pluggable Authentication".](#page-94-0)

# <span id="page-81-1"></span>**8.3.3.1 Creating SSL and RSA Certificates and Keys using MySQL**

MySQL provides these ways to create the SSL certificate and key files and RSA key-pair files required to support encrypted connections using SSL and secure password exchange using RSA over unencrypted connections, if those files are missing:

• The server can autogenerate these files at startup, for MySQL distributions.

![](_page_81_Picture_13.jpeg)

### **Important**

Server autogeneration helps lower the barrier to using SSL by making it easier to generate the required files. However, certificates generated by this method are self-signed, which may not be very secure. After you gain experience using these, consider obtaining certificate and key material from a registered certificate authority.

![](_page_81_Picture_16.jpeg)

### **Important**

If a client connecting to a MySQL server instance uses an SSL certificate with the extendedKeyUsage extension (an X.509 v3 extension), the extended key usage must include client authentication (clientAuth). If the SSL certificate is only specified for server authentication (serverAuth) and other non-client certificate purposes, certificate verification fails and the client connection to the MySQL server instance fails. There is no extendedKeyUsage extension in SSL certificates generated by MySQL Server. If you use your own client certificate created in another way, ensure any extendedKeyUsage extension includes client authentication.

- [Automatic SSL and RSA File Generation](#page-82-0)
- [SSL and RSA File Characteristics](#page-82-1)

### <span id="page-82-0"></span>**Automatic SSL and RSA File Generation**

For MySQL distributions compiled using OpenSSL, the MySQL server has the capability of automatically generating missing SSL and RSA files at startup. The auto\_generate\_certs, sha256\_password\_auto\_generate\_rsa\_keys, and caching\_sha2\_password\_auto\_generate\_rsa\_keys system variables control automatic generation of these files. These variables are enabled by default. They can be enabled at startup and inspected but not set at runtime.

At startup, the server automatically generates server-side and client-side SSL certificate and key files in the data directory if the auto\_generate\_certs system variable is enabled, no SSL options are specified, and the server-side SSL files are missing from the data directory. These files enable encrypted client connections using SSL; see [Section 8.3.1, "Configuring MySQL to Use Encrypted](#page-67-0) [Connections".](#page-67-0)

1. The server checks the data directory for SSL files with the following names:

```
ca.pem
server-cert.pem
server-key.pem
```

2. If any of those files are present, the server creates no SSL files. Otherwise, it creates them, plus some additional files:

```
ca.pem Self-signed CA certificate
ca-key.pem CA private key
server-cert.pem Server certificate
server-key.pem Server private key
client-cert.pem Client certificate
client-key.pem Client private key
```

3. If the server autogenerates SSL files, it uses the names of the ca.pem, server-cert.pem, and server-key.pem files to set the corresponding system variables (ssl\_ca, ssl\_cert, ssl\_key).

At startup, the server automatically generates RSA private/public key-pair files in the data directory if all of these conditions are true: The sha256\_password\_auto\_generate\_rsa\_keys or caching\_sha2\_password\_auto\_generate\_rsa\_keys system variable is enabled; no RSA options are specified; the RSA files are missing from the data directory. These key-pair files enable secure password exchange using RSA over unencrypted connections for accounts authenticated by the sha256\_password (deprecated) or caching\_sha2\_password plugin; see [Section 8.4.1.3,](#page-99-0) ["SHA-256 Pluggable Authentication",](#page-99-0) and [Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".](#page-94-0)

1. The server checks the data directory for RSA files with the following names:

```
private_key.pem Private member of private/public key pair
public_key.pem Public member of private/public key pair
```

- 2. If any of these files are present, the server creates no RSA files. Otherwise, it creates them.
- 3. If the server autogenerates the RSA files, it uses their names to set the corresponding system variables (sha256\_password\_private\_key\_path and sha256\_password\_public\_key\_path; caching\_sha2\_password\_private\_key\_path and caching\_sha2\_password\_public\_key\_path).

### <span id="page-82-1"></span>**SSL and RSA File Characteristics**

SSL and RSA files created automatically by the server have these characteristics:

- SSL and RSA keys have a size of 2048 bits.
- The SSL CA certificate is self signed.
- The SSL server and client certificates are signed with the CA certificate and key, using the sha256WithRSAEncryption signature algorithm.

• SSL certificates use these Common Name (CN) values, with the appropriate certificate type (CA, Server, Client):

```
ca.pem: MySQL_Server_suffix_Auto_Generated_CA_Certificate
server-cert.pm: MySQL_Server_suffix_Auto_Generated_Server_Certificate
client-cert.pm: MySQL_Server_suffix_Auto_Generated_Client_Certificate
```

The suffix value is based on the MySQL version number.

For files generated by the server, if the resulting CN values exceed 64 characters, the \_suffix portion of the name is omitted.

- SSL files have blank values for Country (C), State or Province (ST), Organization (O), Organization Unit Name (OU) and email address.
- SSL files created by the server are valid for ten years from the time of generation.
- RSA files do not expire.
- SSL files have different serial numbers for each certificate/key pair (1 for CA, 2 for Server, 3 for Client).
- Files created automatically by the server are owned by the account that runs the server.
- On Unix and Unix-like systems, the file access mode is 644 for certificate files (that is, world readable) and 600 for key files (that is, accessible only by the account that runs the server).

To see the contents of an SSL certificate (for example, to check the range of dates over which it is valid), invoke openssl directly:

```
openssl x509 -text -in ca.pem
openssl x509 -text -in server-cert.pem
openssl x509 -text -in client-cert.pem
```

It is also possible to check SSL certificate expiration information using this SQL statement:

```
mysql> SHOW STATUS LIKE 'Ssl_server_not%';
+-----------------------+--------------------------+
| Variable_name | Value |
+-----------------------+--------------------------+
| Ssl_server_not_after | Apr 28 14:16:39 2027 GMT |
| Ssl_server_not_before | May 1 14:16:39 2017 GMT |
+-----------------------+--------------------------+
```

# <span id="page-83-0"></span>**8.3.3.2 Creating SSL Certificates and Keys Using openssl**

This section describes how to use the openssl command to set up SSL certificate and key files for use by MySQL servers and clients. The first example shows a simplified procedure such as you might use from the command line. The second shows a script that contains more detail. The first two examples are intended for use on Unix and both use the openssl command that is part of OpenSSL. The third example describes how to set up SSL files on Windows.

![](_page_83_Picture_17.jpeg)

### **Note**

An easier alternative to generating the files required for SSL than the procedure described here is to let the server autogenerate them; see [Section 8.3.3.1,](#page-81-1) ["Creating SSL and RSA Certificates and Keys using MySQL"](#page-81-1).

![](_page_83_Picture_20.jpeg)

### **Important**

Whatever method you use to generate the certificate and key files, the Common Name value used for the server and client certificates/keys must each differ from the Common Name value used for the CA certificate. Otherwise, the certificate and key files do not work for servers compiled using OpenSSL. A typical error in this case is:

ERROR 2026 (HY000): SSL connection error: error:00000001:lib(0):func(0):reason(1)

![](_page_84_Picture_2.jpeg)

#### **Important**

If a client connecting to a MySQL server instance uses an SSL certificate with the extendedKeyUsage extension (an X.509 v3 extension), the extended key usage must include client authentication (clientAuth). If the SSL certificate is only specified for server authentication (serverAuth) and other non-client certificate purposes, certificate verification fails and the client connection to the MySQL server instance fails. There is no extendedKeyUsage extension in SSL certificates created using the openssl command following the instructions in this topic. If you use your own client certificate created in another way, ensure any extendedKeyUsage extension includes client authentication.

- [Example 1: Creating SSL Files from the Command Line on Unix](#page-84-0)
- [Example 2: Creating SSL Files Using a Script on Unix](#page-85-0)
- [Example 3: Creating SSL Files on Windows](#page-88-0)

### <span id="page-84-0"></span>**Example 1: Creating SSL Files from the Command Line on Unix**

The following example shows a set of commands to create MySQL server and client certificate and key files. You must respond to several prompts by the openssl commands. To generate test files, you can press Enter to all prompts. To generate files for production use, you should provide nonempty responses.

```
# Create clean environment
rm -rf newcerts
mkdir newcerts && cd newcerts
# Create CA certificate
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3600 \
 -key ca-key.pem -out ca.pem
# Create server certificate, remove passphrase, and sign it
# server-cert.pem = public key, server-key.pem = private key
openssl req -newkey rsa:2048 -days 3600 \
 -nodes -keyout server-key.pem -out server-req.pem
openssl rsa -in server-key.pem -out server-key.pem
openssl x509 -req -in server-req.pem -days 3600 \
 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
# Create client certificate, remove passphrase, and sign it
# client-cert.pem = public key, client-key.pem = private key
openssl req -newkey rsa:2048 -days 3600 \
 -nodes -keyout client-key.pem -out client-req.pem
openssl rsa -in client-key.pem -out client-key.pem
openssl x509 -req -in client-req.pem -days 3600 \
 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
```

After generating the certificates, verify them:

```
openssl verify -CAfile ca.pem server-cert.pem client-cert.pem
```

You should see a response like this:

```
server-cert.pem: OK
client-cert.pem: OK
```

To see the contents of a certificate (for example, to check the range of dates over which a certificate is valid), invoke openssl like this:

```
openssl x509 -text -in ca.pem
openssl x509 -text -in server-cert.pem
```

```
openssl x509 -text -in client-cert.pem
```

Now you have a set of files that can be used as follows:

- ca.pem: Use this to set the ssl\_ca system variable on the server side and the --ssl-ca option on the client side. (The CA certificate, if used, must be the same on both sides.)
- server-cert.pem, server-key.pem: Use these to set the ssl\_cert and ssl\_key system variables on the server side.
- client-cert.pem, client-key.pem: Use these as the arguments to the --ssl-cert and ssl-key options on the client side.

For additional usage instructions, see [Section 8.3.1, "Configuring MySQL to Use Encrypted](#page-67-0) [Connections".](#page-67-0)

### <span id="page-85-0"></span>**Example 2: Creating SSL Files Using a Script on Unix**

Here is an example script that shows how to set up SSL certificate and key files for MySQL. After executing the script, use the files for SSL connections as described in [Section 8.3.1, "Configuring](#page-67-0) [MySQL to Use Encrypted Connections".](#page-67-0)

```
DIR=`pwd`/openssl
PRIV=$DIR/private
mkdir $DIR $PRIV $DIR/newcerts
cp /usr/share/ssl/openssl.cnf $DIR
replace ./demoCA $DIR -- $DIR/openssl.cnf
# Create necessary files: $database, $serial and $new_certs_dir
# directory (optional)
touch $DIR/index.txt
echo "01" > $DIR/serial
#
# Generation of Certificate Authority(CA)
#
openssl req -new -x509 -keyout $PRIV/cakey.pem -out $DIR/ca.pem \
 -days 3600 -config $DIR/openssl.cnf
# Sample output:
# Using configuration from /home/jones/openssl/openssl.cnf
# Generating a 1024 bit RSA private key
# ................++++++
# .........++++++
# writing new private key to '/home/jones/openssl/private/cakey.pem'
# Enter PEM pass phrase:
# Verifying password - Enter PEM pass phrase:
# -----
# You are about to be asked to enter information to be
# incorporated into your certificate request.
# What you are about to enter is what is called a Distinguished Name
# or a DN.
# There are quite a few fields but you can leave some blank
# For some fields there will be a default value,
# If you enter '.', the field will be left blank.
# -----
# Country Name (2 letter code) [AU]:FI
# State or Province Name (full name) [Some-State]:.
# Locality Name (eg, city) []:
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:MySQL AB
# Organizational Unit Name (eg, section) []:
# Common Name (eg, YOUR name) []:MySQL admin
# Email Address []:
#
# Create server request and key
#
```

```
openssl req -new -keyout $DIR/server-key.pem -out \
 $DIR/server-req.pem -days 3600 -config $DIR/openssl.cnf
# Sample output:
# Using configuration from /home/jones/openssl/openssl.cnf
# Generating a 1024 bit RSA private key
# ..++++++
# ..........++++++
# writing new private key to '/home/jones/openssl/server-key.pem'
# Enter PEM pass phrase:
# Verifying password - Enter PEM pass phrase:
# -----
# You are about to be asked to enter information that will be
# incorporated into your certificate request.
# What you are about to enter is what is called a Distinguished Name
# or a DN.
# There are quite a few fields but you can leave some blank
# For some fields there will be a default value,
# If you enter '.', the field will be left blank.
# -----
# Country Name (2 letter code) [AU]:FI
# State or Province Name (full name) [Some-State]:.
# Locality Name (eg, city) []:
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:MySQL AB
# Organizational Unit Name (eg, section) []:
# Common Name (eg, YOUR name) []:MySQL server
# Email Address []:
#
# Please enter the following 'extra' attributes
# to be sent with your certificate request
# A challenge password []:
# An optional company name []:
#
# Remove the passphrase from the key
#
openssl rsa -in $DIR/server-key.pem -out $DIR/server-key.pem
#
# Sign server cert
#
openssl ca -cert $DIR/ca.pem -policy policy_anything \
 -out $DIR/server-cert.pem -config $DIR/openssl.cnf \
 -infiles $DIR/server-req.pem
# Sample output:
# Using configuration from /home/jones/openssl/openssl.cnf
# Enter PEM pass phrase:
# Check that the request matches the signature
# Signature ok
# The Subjects Distinguished Name is as follows
# countryName :PRINTABLE:'FI'
# organizationName :PRINTABLE:'MySQL AB'
# commonName :PRINTABLE:'MySQL admin'
# Certificate is to be certified until Sep 13 14:22:46 2003 GMT
# (365 days)
# Sign the certificate? [y/n]:y
#
#