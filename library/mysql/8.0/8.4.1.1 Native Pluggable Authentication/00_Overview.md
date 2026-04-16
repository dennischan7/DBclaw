---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL includes a mysql\_native\_password plugin that implements native authentication; that is, authentication based on the password hashing method in use from before the introduction of pluggable authentication.

![](_page_37_Picture_10.jpeg)

#### **Note**

The mysql\_native\_password authentication plugin is deprecated as of MySQL 8.0.34, disabled by default in MySQL 8.4, and removed as of MySQL 9.0.0.

The following table shows the plugin names on the server and client sides.

**Table 8.16 Plugin and Library Names for Native Password Authentication**

| Plugin or File     | Plugin or File Name         |
|--------------------|-----------------------------|
| Server-side plugin | mysql_native_password       |
| Client-side plugin | mysql_native_password       |
| Library file       | None (plugins are built in) |

The following sections provide installation and usage information specific to native pluggable authentication:

- [Installing Native Pluggable Authentication](#page-37-1)
- [Using Native Pluggable Authentication](#page-38-1)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication".

## <span id="page-37-1"></span>**Installing Native Pluggable Authentication**

The mysql\_native\_password plugin exists in server and client forms:

- The server-side plugin is built into the server, need not be loaded explicitly, and cannot be disabled by unloading it.
- The client-side plugin is built into the libmysqlclient client library and is available to any program linked against libmysqlclient.

## <span id="page-38-1"></span>**Using Native Pluggable Authentication**

MySQL client programs use mysql\_native\_password by default. The --default-auth option can be used as a hint about which client-side plugin the program can expect to use:

\$> **mysql --default-auth=mysql\_native\_password ...**

# <span id="page-38-0"></span>**8.4.1.2 Caching SHA-2 Pluggable Authentication**

MySQL provides two authentication plugins that implement SHA-256 hashing for user account passwords:

- caching\_sha2\_password: Implements SHA-256 authentication (like the deprecated sha256\_password), but uses caching on the server side for better performance and has additional features for wider applicability.
- sha256\_password: Implements basic SHA-256 authentication. This is deprecated as of MySQL 8.0.16 and subject to removal in the future.

This section describes the caching SHA-2 authentication plugin. For information about the original basic (noncaching) plugin, see [Section 8.4.1.3, "SHA-256 Pluggable Authentication".](#page-43-0)

![](_page_38_Picture_9.jpeg)

## **Important**

In MySQL 8.0, caching\_sha2\_password is the default authentication plugin rather than mysql\_native\_password. For information about the implications of this change for server operation and compatibility of the server with clients and connectors, see caching\_sha2\_password as the Preferred Authentication Plugin.

![](_page_38_Picture_12.jpeg)

#### **Important**

To connect to the server using an account that authenticates with the caching\_sha2\_password plugin, you must use either a secure connection or an unencrypted connection that supports password exchange using an RSA key pair, as described later in this section. Either way, the caching\_sha2\_password plugin uses MySQL's encryption capabilities. See [Section 8.3, "Using Encrypted Connections"](#page-7-0).

![](_page_38_Picture_15.jpeg)

#### **Note**

In the name sha256\_password, "sha256" refers to the 256-bit digest length the plugin uses for encryption. In the name caching\_sha2\_password, "sha2" refers more generally to the SHA-2 class of encryption algorithms, of which 256 bit encryption is one instance. The latter name choice leaves room for future expansion of possible digest lengths without changing the plugin name.

The caching\_sha2\_password plugin has these advantages, compared to sha256\_password:

- On the server side, an in-memory cache enables faster reauthentication of users who have connected previously when they connect again.
- RSA-based password exchange is available regardless of the SSL library against which MySQL is linked.
- Support is provided for client connections that use the Unix socket-file and shared-memory protocols.

The following table shows the plugin names on the server and client sides.

**Table 8.17 Plugin and Library Names for SHA-2 Authentication**

| Plugin or File     | Plugin or File Name   |
|--------------------|-----------------------|
| Server-side plugin | caching_sha2_password |

| Plugin or File     | Plugin or File Name         |
|--------------------|-----------------------------|
| Client-side plugin | caching_sha2_password       |
| Library file       | None (plugins are built in) |

The following sections provide installation and usage information specific to caching SHA-2 pluggable authentication:

- [Installing SHA-2 Pluggable Authentication](#page-39-0)
- [Using SHA-2 Pluggable Authentication](#page-39-1)
- [Cache Operation for SHA-2 Pluggable Authentication](#page-42-0)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication".

## <span id="page-39-0"></span>**Installing SHA-2 Pluggable Authentication**

The caching\_sha2\_password plugin exists in server and client forms:

- The server-side plugin is built into the server, need not be loaded explicitly, and cannot be disabled by unloading it.
- The client-side plugin is built into the libmysqlclient client library and is available to any program linked against libmysqlclient.

The server-side plugin uses the sha2\_cache\_cleaner audit plugin as a helper to perform password cache management. sha2\_cache\_cleaner, like caching\_sha2\_password, is built in and need not be installed.

## <span id="page-39-1"></span>**Using SHA-2 Pluggable Authentication**

To set up an account that uses the caching\_sha2\_password plugin for SHA-256 password hashing, use the following statement, where password is the desired account password:

```
CREATE USER 'sha2user'@'localhost'
IDENTIFIED WITH caching_sha2_password BY 'password';
```

The server assigns the caching\_sha2\_password plugin to the account and uses it to encrypt the password using SHA-256, storing those values in the plugin and authentication\_string columns of the mysql.user system table.

The preceding instructions do not assume that caching\_sha2\_password is the default authentication plugin. If caching\_sha2\_password is the default authentication plugin, a simpler CREATE USER syntax can be used.

To start the server with the default authentication plugin set to caching\_sha2\_password, put these lines in the server option file:

```
[mysqld]
default_authentication_plugin=caching_sha2_password
```

That causes the caching\_sha2\_password plugin to be used by default for new accounts. As a result, it is possible to create the account and set its password without naming the plugin explicitly:

```
CREATE USER 'sha2user'@'localhost' IDENTIFIED BY 'password';
```

Another consequence of setting default\_authentication\_plugin to caching\_sha2\_password is that, to use some other plugin for account creation, you must specify that plugin explicitly. For example, to use the deprecated mysql\_native\_password plugin, use this statement:

```
CREATE USER 'nativeuser'@'localhost'
```

IDENTIFIED WITH mysql\_native\_password BY 'password';

caching\_sha2\_password supports connections over secure transport. If you follow the RSA configuration procedure given later in this section, it also supports encrypted password exchange using RSA over unencrypted connections. RSA support has these characteristics:

- On the server side, two system variables name the RSA private and public key-pair files: caching\_sha2\_password\_private\_key\_path and caching\_sha2\_password\_public\_key\_path. The database administrator must set these variables at server startup if the key files to use have names that differ from the system variable default values.
- The server uses the caching\_sha2\_password\_auto\_generate\_rsa\_keys system variable to determine whether to automatically generate the RSA key-pair files. See [Section 8.3.3, "Creating](#page-24-0) [SSL and RSA Certificates and Keys"](#page-24-0).
- The Caching\_sha2\_password\_rsa\_public\_key status variable displays the RSA public key value used by the caching\_sha2\_password authentication plugin.
- Clients that are in possession of the RSA public key can perform RSA key pair-based password exchange with the server during the connection process, as described later.
- For connections by accounts that authenticate with caching\_sha2\_password and RSA key pairbased password exchange, the server does not send the RSA public key to clients by default. Clients can use a client-side copy of the required public key, or request the public key from the server.

Use of a trusted local copy of the public key enables the client to avoid a round trip in the client/ server protocol, and is more secure than requesting the public key from the server. On the other hand, requesting the public key from the server is more convenient (it requires no management of a client-side file) and may be acceptable in secure network environments.

- For command-line clients, use the --server-public-key-path option to specify the RSA public key file. Use the --get-server-public-key option to request the public key from the server. The following programs support the two options: mysql, mysqlsh, mysqladmin, mysqlbinlog, mysqlcheck, mysqldump, mysqlimport, mysqlpump, mysqlshow, mysqlslap, mysqltest, mysql\_upgrade.
- For programs that use the C API, call [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-options.md) to specify the RSA public key file by passing the MYSQL\_SERVER\_PUBLIC\_KEY option and the name of the file, or request the public key from the server by passing the MYSQL\_OPT\_GET\_SERVER\_PUBLIC\_KEY option.
- For replicas, use the CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) with the SOURCE\_PUBLIC\_KEY\_PATH | MASTER\_PUBLIC\_KEY\_PATH option to specify the RSA public key file, or the GET\_SOURCE\_PUBLIC\_KEY | GET\_MASTER\_PUBLIC\_KEY option to request the public key from the source. For Group Replication, the group\_replication\_recovery\_public\_key\_path and group\_replication\_recovery\_get\_public\_key system variables serve the same purpose.

In all cases, if the option is given to specify a valid public key file, it takes precedence over the option to request the public key from the server.

For clients that use the caching\_sha2\_password plugin, passwords are never exposed as cleartext when connecting to the server. How password transmission occurs depends on whether a secure connection or RSA encryption is used:

- If the connection is secure, an RSA key pair is unnecessary and is not used. This applies to TCP connections encrypted using TLS, as well as Unix socket-file and shared-memory connections. The password is sent as cleartext but cannot be snooped because the connection is secure.
- If the connection is not secure, an RSA key pair is used. This applies to TCP connections not encrypted using TLS and named-pipe connections. RSA is used only for password exchange

between client and server, to prevent password snooping. When the server receives the encrypted password, it decrypts it. A scramble is used in the encryption to prevent repeat attacks.

To enable use of an RSA key pair for password exchange during the client connection process, use the following procedure:

- 1. Create the RSA private and public key-pair files using the instructions in [Section 8.3.3, "Creating](#page-24-0) [SSL and RSA Certificates and Keys"](#page-24-0).
- 2. If the private and public key files are located in the data directory and are named private\_key.pem and public\_key.pem (the default values of the caching\_sha2\_password\_private\_key\_path and caching\_sha2\_password\_public\_key\_path system variables), the server uses them automatically at startup.

Otherwise, to name the key files explicitly, set the system variables to the key file names in the server option file. If the files are located in the server data directory, you need not specify their full path names:

```
[mysqld]
caching_sha2_password_private_key_path=myprivkey.pem
caching_sha2_password_public_key_path=mypubkey.pem
```

If the key files are not located in the data directory, or to make their locations explicit in the system variable values, use full path names:

```
[mysqld]
caching_sha2_password_private_key_path=/usr/local/mysql/myprivkey.pem
caching_sha2_password_public_key_path=/usr/local/mysql/mypubkey.pem
```

3. If you want to change the number of hash rounds used by caching\_sha2\_password during password generation, set the caching\_sha2\_password\_digest\_rounds system variable. For example:

```
[mysqld]
caching_sha2_password_digest_rounds=10000
```

4. Restart the server, then connect to it and check the Caching\_sha2\_password\_rsa\_public\_key status variable value. The value actually displayed differs from that shown here, but should be nonempty:

```
mysql> SHOW STATUS LIKE 'Caching_sha2_password_rsa_public_key'\G
*************************** 1. row ***************************
Variable_name: Caching_sha2_password_rsa_public_key
 Value: -----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDO9nRUDd+KvSZgY7cNBZMNpwX6
MvE1PbJFXO7u18nJ9lwc99Du/E7lw6CVXw7VKrXPeHbVQUzGyUNkf45Nz/ckaaJa
aLgJOBCIDmNVnyU54OT/1lcs2xiyfaDMe8fCJ64ZwTnKbY2gkt1IMjUAB5Ogd5kJ
g8aV7EtKwyhHb0c30QIDAQAB
-----END PUBLIC KEY-----
```

If the value is empty, the server found some problem with the key files. Check the error log for diagnostic information.

After the server has been configured with the RSA key files, accounts that authenticate with the caching\_sha2\_password plugin have the option of using those key files to connect to the server. As mentioned previously, such accounts can use either a secure connection (in which case RSA is not used) or an unencrypted connection that performs password exchange using RSA. Suppose that an unencrypted connection is used. For example:

```
$> mysql --ssl-mode=DISABLED -u sha2user -p
Enter password: password
```

For this connection attempt by sha2user, the server determines that caching\_sha2\_password is the appropriate authentication plugin and invokes it (because that was the plugin specified at CREATE USER time). The plugin finds that the connection is not encrypted and thus requires the password to be transmitted using RSA encryption. However, the server does not send the public key to the client, and the client provided no public key, so it cannot encrypt the password and the connection fails:

```
ERROR 2061 (HY000): Authentication plugin 'caching_sha2_password'
reported error: Authentication requires secure connection.
```

To request the RSA public key from the server, specify the --get-server-public-key option:

```
$> mysql --ssl-mode=DISABLED -u sha2user -p --get-server-public-key
Enter password: password
```

In this case, the server sends the RSA public key to the client, which uses it to encrypt the password and returns the result to the server. The plugin uses the RSA private key on the server side to decrypt the password and accepts or rejects the connection based on whether the password is correct.

Alternatively, if the client has a file containing a local copy of the RSA public key required by the server, it can specify the file using the --server-public-key-path option:

```
$> mysql --ssl-mode=DISABLED -u sha2user -p --server-public-key-path=file_name
Enter password: password
```

In this case, the client uses the public key to encrypt the password and returns the result to the server. The plugin uses the RSA private key on the server side to decrypt the password and accepts or rejects the connection based on whether the password is correct.

The public key value in the file named by the --server-public-key-path option should be the same as the key value in the server-side file named by the caching\_sha2\_password\_public\_key\_path system variable. If the key file contains a valid public key value but the value is incorrect, an access-denied error occurs. If the key file does not contain a valid public key, the client program cannot use it.

Client users can obtain the RSA public key two ways:

- The database administrator can provide a copy of the public key file.
- A client user who can connect to the server some other way can use a SHOW STATUS LIKE 'Caching\_sha2\_password\_rsa\_public\_key' statement and save the returned key value in a file.

## <span id="page-42-0"></span>**Cache Operation for SHA-2 Pluggable Authentication**

On the server side, the caching\_sha2\_password plugin uses an in-memory cache for faster authentication of clients who have connected previously. Entries consist of account-name/passwordhash pairs. The cache works like this:

- 1. When a client connects, caching\_sha2\_password checks whether the client and password match some cache entry. If so, authentication succeeds.
- 2. If there is no matching cache entry, the plugin attempts to verify the client against the credentials in the mysql.user system table. If this succeeds, caching\_sha2\_password adds an entry for the client to the hash. Otherwise, authentication fails and the connection is rejected.

In this way, when a client first connects, authentication against the mysql.user system table occurs. When the client connects subsequently, faster authentication against the cache occurs.

Password cache operations other than adding entries are handled by the sha2\_cache\_cleaner audit plugin, which performs these actions on behalf of caching\_sha2\_password:

- It clears the cache entry for any account that is renamed or dropped, or any account for which the credentials or authentication plugin are changed.
- It empties the cache when the FLUSH PRIVILEGES statement is executed.

• It empties the cache at server shutdown. (This means the cache is not persistent across server restarts.)

Cache clearing operations affect the authentication requirements for subsequent client connections. For each user account, the first client connection for the user after any of the following operations must use a secure connection (made using TCP using TLS credentials, a Unix socket file, or shared memory) or RSA key pair-based password exchange:

- After account creation.
- After a password change for the account.
- After RENAME USER for the account.
- After FLUSH PRIVILEGES.

FLUSH PRIVILEGES clears the entire cache and affects all accounts that use the caching\_sha2\_password plugin. The other operations clear specific cache entries and affect only accounts that are part of the operation.

Once the user authenticates successfully, the account is entered into the cache and subsequent connections do not require a secure connection or the RSA key pair, until another cache clearing event occurs that affects the account. (When the cache can be used, the server uses a challengeresponse mechanism that does not use cleartext password transmission and does not require a secure connection.)

# <span id="page-43-0"></span>**8.4.1.3 SHA-256 Pluggable Authentication**

MySQL provides two authentication plugins that implement SHA-256 hashing for user account passwords:

- caching\_sha2\_password: Implements SHA-256 authentication (like the deprecated sha256\_password), but uses caching on the server side for better performance and has additional features for wider applicability.
- sha256\_password: Implements basic SHA-256 authentication. This is deprecated as of MySQL 8.0.16 and subject to removal in the future.

This section describes the original noncaching SHA-2 authentication plugin. For information about the caching plugin, see [Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".](#page-38-0)

![](_page_43_Picture_14.jpeg)

### **Important**

In MySQL 8.0, caching\_sha2\_password is the default authentication plugin rather than mysql\_native\_password. For information about the implications of this change for server operation and compatibility of the server with clients and connectors, see caching\_sha2\_password as the Preferred Authentication Plugin.

Because caching\_sha2\_password is the default authentication plugin in MySQL 8.0 and provides a superset of the capabilities of the sha256\_password authentication plugin, sha256\_password is deprecated; expect it to be removed in a future version of MySQL. MySQL accounts that authenticate using sha256\_password should be migrated to use caching\_sha2\_password instead.

![](_page_43_Picture_18.jpeg)

#### **Important**

To connect to the server using an account that authenticates with the sha256\_password plugin, you must use either a TLS connection or an unencrypted connection that supports password exchange using an RSA key pair, as described later in this section. Either way, the sha256\_password plugin uses MySQL's encryption capabilities. See [Section 8.3, "Using Encrypted](#page-7-0) [Connections"](#page-7-0).

![](_page_44_Picture_2.jpeg)

#### **Note**

In the name sha256\_password, "sha256" refers to the 256-bit digest length the plugin uses for encryption. In the name caching\_sha2\_password, "sha2" refers more generally to the SHA-2 class of encryption algorithms, of which 256 bit encryption is one instance. The latter name choice leaves room for future expansion of possible digest lengths without changing the plugin name.

The following table shows the plugin names on the server and client sides.

#### **Table 8.18 Plugin and Library Names for SHA-256 Authentication**

| Plugin or File     | Plugin or File Name         |
|--------------------|-----------------------------|
| Server-side plugin | sha256_password             |
| Client-side plugin | sha256_password             |
| Library file       | None (plugins are built in) |

The following sections provide installation and usage information specific to SHA-256 pluggable authentication:

- [Installing SHA-256 Pluggable Authentication](#page-44-0)
- [Using SHA-256 Pluggable Authentication](#page-44-1)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication".

## <span id="page-44-0"></span>**Installing SHA-256 Pluggable Authentication**

The sha256\_password plugin exists in server and client forms:

- The server-side plugin is built into the server, need not be loaded explicitly, and cannot be disabled by unloading it.
- The client-side plugin is built into the libmysqlclient client library and is available to any program linked against libmysqlclient.

## <span id="page-44-1"></span>**Using SHA-256 Pluggable Authentication**

To set up an account that uses the deprecated sha256\_password plugin for SHA-256 password hashing, use the following statement, where password is the desired account password:

```
CREATE USER 'sha256user'@'localhost'
IDENTIFIED WITH sha256_password BY 'password';
```

The server assigns the sha256\_password plugin to the account and uses it to encrypt the password using SHA-256, storing those values in the plugin and authentication\_string columns of the mysql.user system table.

The preceding instructions do not assume that sha256\_password is the default authentication plugin. If sha256\_password is the default authentication plugin, a simpler CREATE USER syntax can be used.

To start the server with the default authentication plugin set to sha256\_password, put these lines in the server option file:

```
[mysqld]
default_authentication_plugin=sha256_password
```

That causes the sha256\_password plugin to be used by default for new accounts. As a result, it is possible to create the account and set its password without naming the plugin explicitly:

```
CREATE USER 'sha256user'@'localhost' IDENTIFIED BY 'password';
```

Another consequence of setting default\_authentication\_plugin to sha256\_password is that, to use some other plugin for account creation, you must specify that plugin explicitly. For example, to use the mysql\_native\_password plugin, use this statement:

```
CREATE USER 'nativeuser'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'password';
```

sha256\_password supports connections over secure transport. sha256\_password also supports encrypted password exchange using RSA over unencrypted connections if MySQL is compiled using OpenSSL, and the MySQL server to which you wish to connect is configured to support RSA (using the RSA configuration procedure given later in this section).

RSA support has these characteristics:

- On the server side, two system variables name the RSA private and public key-pair files: sha256\_password\_private\_key\_path and sha256\_password\_public\_key\_path. The database administrator must set these variables at server startup if the key files to use have names that differ from the system variable default values.
- The server uses the sha256\_password\_auto\_generate\_rsa\_keys system variable to determine whether to automatically generate the RSA key-pair files. See [Section 8.3.3, "Creating](#page-24-0) [SSL and RSA Certificates and Keys"](#page-24-0).
- The Rsa\_public\_key status variable displays the RSA public key value used by the sha256\_password authentication plugin.
- Clients that are in possession of the RSA public key can perform RSA key pair-based password exchange with the server during the connection process, as described later.
- For connections by accounts that authenticate with sha256\_password and RSA public key pairbased password exchange, the server sends the RSA public key to the client as needed. However, if a copy of the public key is available on the client host, the client can use it to save a round trip in the client/server protocol:
  - For these command-line clients, use the --server-public-key-path option to specify the RSA public key file: mysql, mysqladmin, mysqlbinlog, mysqlcheck, mysqldump, mysqlimport, mysqlpump, mysqlshow, mysqlslap, mysqltest, mysql\_upgrade.
  - For programs that use the C API, call [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-options.md) to specify the RSA public key file by passing the MYSQL\_SERVER\_PUBLIC\_KEY option and the name of the file.
  - For replicas, use the CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) with the SOURCE\_PUBLIC\_KEY\_PATH | MASTER\_PUBLIC\_KEY\_PATH option to specify the RSA public key file. For Group Replication, the group\_replication\_recovery\_get\_public\_key system variable serves the same purpose.

For clients that use the sha256\_password plugin, passwords are never exposed as cleartext when connecting to the server. How password transmission occurs depends on whether a secure connection or RSA encryption is used:

• If the connection is secure, an RSA key pair is unnecessary and is not used. This applies to connections encrypted using TLS. The password is sent as cleartext but cannot be snooped because the connection is secure.

![](_page_46_Picture_1.jpeg)

## **Note**

Unlike caching\_sha2\_password, the sha256\_password plugin does not treat shared-memory connections as secure, even though share-memory transport is secure by default.

- If the connection is not secure, and an RSA key pair is available, the connection remains unencrypted. This applies to connections not encrypted using TLS. RSA is used only for password exchange between client and server, to prevent password snooping. When the server receives the encrypted password, it decrypts it. A scramble is used in the encryption to prevent repeat attacks.
- If a secure connection is not used and RSA encryption is not available, the connection attempt fails because the password cannot be sent without being exposed as cleartext.

![](_page_46_Picture_6.jpeg)

#### **Note**

To use RSA password encryption with sha256\_password, the client and server both must be compiled using OpenSSL, not just one of them.

Assuming that MySQL has been compiled using OpenSSL, use the following procedure to enable use of an RSA key pair for password exchange during the client connection process:

- 1. Create the RSA private and public key-pair files using the instructions in [Section 8.3.3, "Creating](#page-24-0) [SSL and RSA Certificates and Keys"](#page-24-0).
- 2. If the private and public key files are located in the data directory and are named private\_key.pem and public\_key.pem (the default values of the sha256\_password\_private\_key\_path and sha256\_password\_public\_key\_path system variables), the server uses them automatically at startup.

Otherwise, to name the key files explicitly, set the system variables to the key file names in the server option file. If the files are located in the server data directory, you need not specify their full path names:

```
[mysqld]
sha256_password_private_key_path=myprivkey.pem
sha256_password_public_key_path=mypubkey.pem
```

If the key files are not located in the data directory, or to make their locations explicit in the system variable values, use full path names:

```
[mysqld]
sha256_password_private_key_path=/usr/local/mysql/myprivkey.pem
sha256_password_public_key_path=/usr/local/mysql/mypubkey.pem
```

3. Restart the server, then connect to it and check the Rsa\_public\_key status variable value. The value actually displayed differs from that shown here, but should be nonempty:

```
mysql> SHOW STATUS LIKE 'Rsa_public_key'\G
*************************** 1. row ***************************
Variable_name: Rsa_public_key
 Value: -----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDO9nRUDd+KvSZgY7cNBZMNpwX6
MvE1PbJFXO7u18nJ9lwc99Du/E7lw6CVXw7VKrXPeHbVQUzGyUNkf45Nz/ckaaJa
aLgJOBCIDmNVnyU54OT/1lcs2xiyfaDMe8fCJ64ZwTnKbY2gkt1IMjUAB5Ogd5kJ
g8aV7EtKwyhHb0c30QIDAQAB
-----END PUBLIC KEY-----
```

If the value is empty, the server found some problem with the key files. Check the error log for diagnostic information.

After the server has been configured with the RSA key files, accounts that authenticate with the sha256\_password plugin have the option of using those key files to connect to the server. As mentioned previously, such accounts can use either a secure connection (in which case RSA is not used) or an unencrypted connection that performs password exchange using RSA. Suppose that an unencrypted connection is used. For example:

```
$> mysql --ssl-mode=DISABLED -u sha256user -p
Enter password: password
```

For this connection attempt by sha256user, the server determines that sha256\_password is the appropriate authentication plugin and invokes it (because that was the plugin specified at CREATE USER time). The plugin finds that the connection is not encrypted and thus requires the password to be transmitted using RSA encryption. In this case, the plugin sends the RSA public key to the client, which uses it to encrypt the password and returns the result to the server. The plugin uses the RSA private key on the server side to decrypt the password and accepts or rejects the connection based on whether the password is correct.

The server sends the RSA public key to the client as needed. However, if the client has a file containing a local copy of the RSA public key required by the server, it can specify the file using the - server-public-key-path option:

```
$> mysql --ssl-mode=DISABLED -u sha256user -p --server-public-key-path=file_name
Enter password: password
```

The public key value in the file named by the --server-public-key-path option should be the same as the key value in the server-side file named by the sha256\_password\_public\_key\_path system variable. If the key file contains a valid public key value but the value is incorrect, an accessdenied error occurs. If the key file does not contain a valid public key, the client program cannot use it. In this case, the sha256\_password plugin sends the public key to the client as if no --serverpublic-key-path option had been specified.

Client users can obtain the RSA public key two ways:

- The database administrator can provide a copy of the public key file.
- A client user who can connect to the server some other way can use a SHOW STATUS LIKE 'Rsa\_public\_key' statement and save the returned key value in a file.

# <span id="page-47-0"></span>**8.4.1.4 Client-Side Cleartext Pluggable Authentication**

A client-side authentication plugin is available that enables clients to send passwords to the server as cleartext, without hashing or encryption. This plugin is built into the MySQL client library.

The following table shows the plugin name.

**Table 8.19 Plugin and Library Names for Cleartext Authentication**

| Plugin or File     | Plugin or File Name       |
|--------------------|---------------------------|
| Server-side plugin | None, see discussion      |
| Client-side plugin | mysql_clear_password      |
| Library file       | None (plugin is built in) |

Many client-side authentication plugins perform hashing or encryption of a password before the client sends it to the server. This enables clients to avoid sending passwords as cleartext.

Hashing or encryption cannot be done for authentication schemes that require the server to receive the password as entered on the client side. In such cases, the client-side mysql\_clear\_password plugin is used, which enables the client to send the password to the server as cleartext. There is no corresponding server-side plugin. Rather, mysql\_clear\_password can be used on the client side in concert with any server-side plugin that needs a cleartext password. (Examples are the PAM and simple LDAP authentication plugins; see [Section 8.4.1.5, "PAM Pluggable Authentication"](#page-48-0), and [Section 8.4.1.7, "LDAP Pluggable Authentication"](#page-63-0).)

The following discussion provides usage information specific to cleartext pluggable authentication. For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication".

![](_page_48_Picture_1.jpeg)

## **Note**

Sending passwords as cleartext may be a security problem in some configurations. To avoid problems if there is any possibility that the password would be intercepted, clients should connect to MySQL Server using a method that protects the password. Possibilities include SSL (see [Section 8.3, "Using](#page-7-0) [Encrypted Connections"\)](#page-7-0), IPsec, or a private network.

To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it. This can be done in several ways:

- Set the LIBMYSQL\_ENABLE\_CLEARTEXT\_PLUGIN environment variable to a value that begins with 1, Y, or y. This enables the plugin for all client connections.
- The mysql, mysqladmin, mysqlcheck, mysqldump, mysqlshow, and mysqlslap client programs support an --enable-cleartext-plugin option that enables the plugin on a perinvocation basis.
- The [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.0/en/mysql-options.md) C API function supports a MYSQL\_ENABLE\_CLEARTEXT\_PLUGIN option that enables the plugin on a per-connection basis. Also, any program that uses libmysqlclient and reads option files can enable the plugin by including an enable-cleartext-plugin option in an option group read by the client library.

# <span id="page-48-0"></span>**8.4.1.5 PAM Pluggable Authentication**

![](_page_48_Picture_9.jpeg)

#### **Note**

PAM pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

MySQL Enterprise Edition supports an authentication method that enables MySQL Server to use PAM (Pluggable Authentication Modules) to authenticate MySQL users. PAM enables a system to use a standard interface to access various kinds of authentication methods, such as traditional Unix passwords or an LDAP directory.

PAM pluggable authentication provides these capabilities:

- External authentication: PAM authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables and that authenticate using methods supported by PAM.
- Proxy user support: PAM authentication can return to MySQL a user name different from the external user name passed by the client program, based on the PAM groups the external user is a member of and the authentication string provided. This means that the plugin can return the MySQL user that defines the privileges the external PAM-authenticated user should have. For example, an operating system user named joe can connect and have the privileges of a MySQL user named developer.

PAM pluggable authentication has been tested on Linux and macOS; note that Windows does not support PAM.

The following table shows the plugin and library file names. The file name suffix might differ on your system. The file must be located in the directory named by the plugin\_dir system variable. For installation information, see [Installing PAM Pluggable Authentication](#page-50-0).

**Table 8.20 Plugin and Library Names for PAM Authentication**

| Plugin or File     | Plugin or File Name   |
|--------------------|-----------------------|
| Server-side plugin | authentication_pam    |
| Client-side plugin | mysql_clear_password  |
| Library file       | authentication_pam.so |

The client-side mysql\_clear\_password cleartext plugin that communicates with the server-side PAM plugin is built into the libmysqlclient client library and is included in all distributions, including community distributions. Inclusion of the client-side cleartext plugin in all MySQL distributions enables clients from any distribution to connect to a server that has the server-side PAM plugin loaded.

The following sections provide installation and usage information specific to PAM pluggable authentication:

- [How PAM Authentication of MySQL Users Works](#page-49-0)
- [Installing PAM Pluggable Authentication](#page-50-0)
- [Uninstalling PAM Pluggable Authentication](#page-51-0)
- [Using PAM Pluggable Authentication](#page-51-1)
- [PAM Unix Password Authentication without Proxy Users](#page-53-0)
- [PAM LDAP Authentication without Proxy Users](#page-54-0)
- [PAM Unix Password Authentication with Proxy Users and Group Mapping](#page-55-0)
- [PAM Authentication Access to Unix Password Store](#page-57-0)
- [PAM Authentication Debugging](#page-58-0)

For general information about pluggable authentication in MySQL, see Section 8.2.17, "Pluggable Authentication". For information about the mysql\_clear\_password plugin, see [Section 8.4.1.4,](#page-47-0) ["Client-Side Cleartext Pluggable Authentication".](#page-47-0) For proxy user information, see Section 8.2.19, "Proxy Users".

# <span id="page-49-0"></span>**How PAM Authentication of MySQL Users Works**

This section provides an overview of how MySQL and PAM work together to authenticate MySQL users. For examples showing how to set up MySQL accounts to use specific PAM services, see [Using](#page-51-1) [PAM Pluggable Authentication](#page-51-1).

- 1. The client program and the server communicate, with the client sending to the server the client user name (the operating system user name by default) and password:
  - The client user name is the external user name.
  - For accounts that use the PAM server-side authentication plugin, the corresponding client-side plugin is mysql\_clear\_password. This client-side plugin performs no password hashing, with the result that the client sends the password to the server as cleartext.
- 2. The server finds a matching MySQL account based on the external user name and the host from which the client connects. The PAM plugin uses the information passed to it by MySQL Server (such as user name, host name, password, and authentication string). When you define a MySQL account that authenticates using PAM, the authentication string contains:
  - A PAM service name, which is a name that the system administrator can use to refer to an authentication method for a particular application. There can be multiple applications associated with a single database server instance, so the choice of service name is left to the SQL application developer.
  - Optionally, if proxying is to be used, a mapping from PAM groups to MySQL user names.
- 3. The plugin uses the PAM service named in the authentication string to check the user credentials and returns 'Authentication succeeded, Username is user\_name' or 'Authentication failed'. The password must be appropriate for the password store used by the PAM service. Examples:

- For traditional Unix passwords, the service looks up passwords stored in the /etc/shadow file.
- For LDAP, the service looks up passwords stored in an LDAP directory.

If the credentials check fails, the server refuses the connection.

- 4. Otherwise, the authentication string indicates whether proxying occurs. If the string contains no PAM group mapping, proxying does not occur. In this case, the MySQL user name is the same as the external user name.
- 5. Otherwise, proxying is indicated based on the PAM group mapping, with the MySQL user name determined based on the first matching group in the mapping list. The meaning of "PAM group" depends on the PAM service. Examples:
  - For traditional Unix passwords, groups are Unix groups defined in the /etc/group file, possibly supplemented with additional PAM information in a file such as /etc/security/group.conf.
  - For LDAP, groups are LDAP groups defined in an LDAP directory.

If the proxy user (the external user) has the PROXY privilege for the proxied MySQL user name, proxying occurs, with the proxy user assuming the privileges of the proxied user.

## <span id="page-50-0"></span>**Installing PAM Pluggable Authentication**

This section describes how to install the server-side PAM authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The plugin library file base name is authentication\_pam, and is typically compiled with the .so suffix.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file:

```
[mysqld]
plugin-load-add=authentication_pam.so
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement, adjusting the .so suffix as necessary:

```
INSTALL PLUGIN authentication_pam SONAME 'authentication_pam.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%pam%';
+--------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------------+---------------+
| authentication_pam | ACTIVE |
+--------------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the PAM plugin, see [Using PAM Pluggable Authentication.](#page-51-1)

## <span id="page-51-0"></span>**Uninstalling PAM Pluggable Authentication**

The method used to uninstall the PAM authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN authentication_pam;
```

# <span id="page-51-1"></span>**Using PAM Pluggable Authentication**

This section describes in general terms how to use the PAM authentication plugin to connect from MySQL client programs to the server. The following sections provide instructions for using PAM authentication in specific ways. It is assumed that the server is running with the server-side PAM plugin enabled, as described in [Installing PAM Pluggable Authentication](#page-50-0).

To refer to the PAM authentication plugin in the IDENTIFIED WITH clause of a CREATE USER statement, use the name authentication\_pam. For example:

```
CREATE USER user
 IDENTIFIED WITH authentication_pam
 AS 'auth_string';
```

The authentication string specifies the following types of information:

- The PAM service name (see [How PAM Authentication of MySQL Users Works\)](#page-49-0). Examples in the following discussion use a service name of mysql-unix for authentication using traditional Unix passwords, and mysql-ldap for authentication using LDAP.
- For proxy support, PAM provides a way for a PAM module to return to the server a MySQL user name other than the external user name passed by the client program when it connects to the server. Use the authentication string to control the mapping from external user names to MySQL user names. If you want to take advantage of proxy user capabilities, the authentication string must include this kind of mapping.

For example, if an account uses the mysql-unix PAM service name and should map operating system users in the root and users PAM groups to the developer and data\_entry MySQL users, respectively, use a statement like this:

```
CREATE USER user
 IDENTIFIED WITH authentication_pam
 AS 'mysql-unix, root=developer, users=data_entry';
```

Authentication string syntax for the PAM authentication plugin follows these rules:

• The string consists of a PAM service name, optionally followed by a PAM group mapping list consisting of one or more keyword/value pairs each specifying a PAM group name and a MySQL user name:

```
pam_service_name[,pam_group_name=mysql_user_name]...
```

The plugin parses the authentication string for each connection attempt that uses the account. To minimize overhead, keep the string as short as possible.

- Each pam\_group\_name=mysql\_user\_name pair must be preceded by a comma.
- Leading and trailing spaces not inside double quotation marks are ignored.

- Unquoted pam\_service\_name, pam\_group\_name, and mysql\_user\_name values can contain anything except equal sign, comma, or space.
- If a pam\_service\_name, pam\_group\_name, or mysql\_user\_name value is quoted with double quotation marks, everything between the quotation marks is part of the value. This is necessary, for example, if the value contains space characters. All characters are legal except double quotation mark and backslash (\). To include either character, escape it with a backslash.

If the plugin successfully authenticates the external user name (the name passed by the client), it looks for a PAM group mapping list in the authentication string and, if present, uses it to return a different MySQL user name to the MySQL server based on which PAM groups the external user is a member of:

- If the authentication string contains no PAM group mapping list, the plugin returns the external name.
- If the authentication string does contain a PAM group mapping list, the plugin examines each pam\_group\_name=mysql\_user\_name pair in the list from left to right and tries to find a match for the pam\_group\_name value in a non-MySQL directory of the groups assigned to the authenticated user and returns mysql\_user\_name for the first match it finds. If the plugin finds no match for any PAM group, it returns the external name. If the plugin is not capable of looking up a group in a directory, it ignores the PAM group mapping list and returns the external name.

The following sections describe how to set up several authentication scenarios that use the PAM authentication plugin:

• No proxy users. This uses PAM only to check login names and passwords. Every external user permitted to connect to MySQL Server should have a matching MySQL account that is defined to use PAM authentication. (For a MySQL account of 'user\_name'@'host\_name' to match the external user, user\_name must be the external user name and host\_name must match the host from which the client connects.) Authentication can be performed by various PAM-supported methods. Later discussion shows how to authenticate client credentials using traditional Unix passwords, and passwords in LDAP.

PAM authentication, when not done through proxy users or PAM groups, requires the MySQL user name to be same as the operating system user name. MySQL user names are limited to 32 characters (see Section 8.2.3, "Grant Tables"), which limits PAM nonproxy authentication to Unix accounts with names of at most 32 characters.

• Proxy users only, with PAM group mapping. For this scenario, create one or more MySQL accounts that define different sets of privileges. (Ideally, nobody should connect using those accounts directly.) Then define a default user authenticating through PAM that uses some mapping scheme (usually based on the external PAM groups the users are members of) to map all the external user names to the few MySQL accounts holding the privilege sets. Any client who connects and specifies an external user name as the client user name is mapped to one of the MySQL accounts and uses its privileges. The discussion shows how to set this up using traditional Unix passwords, but other PAM methods such as LDAP could be used instead.

Variations on these scenarios are possible:

- You can permit some users to log in directly (without proxying) but require others to connect through proxy accounts.
- You can use one PAM authentication method for some users, and another method for other users, by using differing PAM service names among your PAM-authenticated accounts. For example, you can use the mysql-unix PAM service for some users, and mysql-ldap for others.

The examples make the following assumptions. You might need to make some adjustments if your system is set up differently.

- The login name and password are antonio and antonio\_password, respectively. Change these to correspond to the user you want to authenticate.
- The PAM configuration directory is /etc/pam.d.

• The PAM service name corresponds to the authentication method (mysql-unix or mysql-ldap in this discussion). To use a given PAM service, you must set up a PAM file with the same name in the PAM configuration directory (creating the file if it does not exist). In addition, you must name the PAM service in the authentication string of the CREATE USER statement for any account that authenticates using that PAM service.

The PAM authentication plugin checks at initialization time whether the AUTHENTICATION\_PAM\_LOG environment value is set in the server's startup environment. If so, the plugin enables logging of diagnostic messages to the standard output. Depending on how your server is started, the message might appear on the console or in the error log. These messages can be helpful for debugging PAMrelated issues that occur when the plugin performs authentication. For more information, see [PAM](#page-58-0) [Authentication Debugging.](#page-58-0)

## <span id="page-53-0"></span>**PAM Unix Password Authentication without Proxy Users**

This authentication scenario uses PAM to check external users defined in terms of operating system user names and Unix passwords, without proxying. Every such external user permitted to connect to MySQL Server should have a matching MySQL account that is defined to use PAM authentication through traditional Unix password store.

![](_page_53_Picture_5.jpeg)

#### **Note**

Traditional Unix passwords are checked using the /etc/shadow file. For information regarding possible issues related to this file, see [PAM](#page-57-0) [Authentication Access to Unix Password Store.](#page-57-0)

- 1. Verify that Unix authentication permits logins to the operating system with the user name antonio and password antonio\_password.
- 2. Set up PAM to authenticate MySQL connections using traditional Unix passwords by creating a mysql-unix PAM service file named /etc/pam.d/mysql-unix. The file contents are system dependent, so check existing login-related files in the /etc/pam.d directory to see what they look like. On Linux, the mysql-unix file might look like this:

```
#%PAM-1.0
auth include password-auth
account include password-auth
```

For macOS, use login rather than password-auth.

The PAM file format might differ on some systems. For example, on Ubuntu and other Debianbased systems, use these file contents instead:

```
@include common-auth
@include common-account
@include common-session-noninteractive
```

3. Create a MySQL account with the same user name as the operating system user name and define it to authenticate using the PAM plugin and the mysql-unix PAM service:

```
CREATE USER 'antonio'@'localhost'
 IDENTIFIED WITH authentication_pam
 AS 'mysql-unix';
GRANT ALL PRIVILEGES
 ON mydb.*
 TO 'antonio'@'localhost';
```

Here, the authentication string contains only the PAM service name, mysql-unix, which authenticates Unix passwords.

4. Use the mysql command-line client to connect to the MySQL server as antonio. For example:

```
$> mysql --user=antonio --password --enable-cleartext-plugin
Enter password: antonio_password
```

The server should permit the connection and the following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-------------------+-------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-------------------+-------------------+--------------+
| antonio@localhost | antonio@localhost | NULL |
+-------------------+-------------------+--------------+
```

This demonstrates that the antonio operating system user is authenticated to have the privileges granted to the antonio MySQL user, and that no proxying has occurred.

![](_page_54_Picture_4.jpeg)

#### **Note**

The client-side mysql\_clear\_password authentication plugin leaves the password untouched, so client programs send it to the MySQL server as cleartext. This enables the password to be passed as is to PAM. A cleartext password is necessary to use the server-side PAM library, but may be a security problem in some configurations. These measures minimize the risk:

- To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it (for example, with the --enablecleartext-plugin option). See [Section 8.4.1.4, "Client-Side Cleartext](#page-47-0) [Pluggable Authentication"](#page-47-0).
- To avoid password exposure with the mysql\_clear\_password plugin enabled, MySQL clients should connect to the MySQL server using an encrypted connection. See [Section 8.3.1, "Configuring MySQL to Use](#page-8-0) [Encrypted Connections".](#page-8-0)

## <span id="page-54-0"></span>**PAM LDAP Authentication without Proxy Users**

This authentication scenario uses PAM to check external users defined in terms of operating system user names and LDAP passwords, without proxying. Every such external user permitted to connect to MySQL Server should have a matching MySQL account that is defined to use PAM authentication through LDAP.

To use PAM LDAP pluggable authentication for MySQL, these prerequisites must be satisfied:

- An LDAP server must be available for the PAM LDAP service to communicate with.
- Each LDAP user to be authenticated by MySQL must be present in the directory managed by the LDAP server.

![](_page_54_Picture_14.jpeg)

## **Note**

Another way to use LDAP for MySQL user authentication is to use the LDAP-specific authentication plugins. See [Section 8.4.1.7, "LDAP Pluggable](#page-63-0) [Authentication".](#page-63-0)

Configure MySQL for PAM LDAP authentication as follows:

- 1. Verify that Unix authentication permits logins to the operating system with the user name antonio and password antonio\_password.
- 2. Set up PAM to authenticate MySQL connections using LDAP by creating a mysql-ldap PAM service file named /etc/pam.d/mysql-ldap. The file contents are system dependent, so check existing login-related files in the /etc/pam.d directory to see what they look like. On Linux, the mysql-ldap file might look like this:

#%PAM-1.0

```
auth required pam_ldap.so
account required pam_ldap.so
```

If PAM object files have a suffix different from .so on your system, substitute the correct suffix.

The PAM file format might differ on some systems.

3. Create a MySQL account with the same user name as the operating system user name and define it to authenticate using the PAM plugin and the mysql-ldap PAM service:

```
CREATE USER 'antonio'@'localhost'
 IDENTIFIED WITH authentication_pam
 AS 'mysql-ldap';
GRANT ALL PRIVILEGES
 ON mydb.*
 TO 'antonio'@'localhost';
```

Here, the authentication string contains only the PAM service name, mysql-ldap, which authenticates using LDAP.

4. Connecting to the server is the same as described in [PAM Unix Password Authentication without](#page-53-0) [Proxy Users](#page-53-0).

## <span id="page-55-0"></span>**PAM Unix Password Authentication with Proxy Users and Group Mapping**

The authentication scheme described here uses proxying and PAM group mapping to map connecting MySQL users who authenticate using PAM onto other MySQL accounts that define different sets of privileges. Users do not connect directly through the accounts that define the privileges. Instead, they connect through a default proxy account authenticated using PAM, such that all the external users are mapped to the MySQL accounts that hold the privileges. Any user who connects using the proxy account is mapped to one of those MySQL accounts, the privileges for which determine the database operations permitted to the external user.

The procedure shown here uses Unix password authentication. To use LDAP instead, see the early steps of [PAM LDAP Authentication without Proxy Users](#page-54-0).

![](_page_55_Picture_11.jpeg)

# **Note**

Traditional Unix passwords are checked using the /etc/shadow file. For information regarding possible issues related to this file, see [PAM](#page-57-0) [Authentication Access to Unix Password Store.](#page-57-0)

- 1. Verify that Unix authentication permits logins to the operating system with the user name antonio and password antonio\_password.
- 2. Verify that antonio is a member of the root or users PAM group.
- 3. Set up PAM to authenticate the mysql-unix PAM service through operating system users by creating a file named /etc/pam.d/mysql-unix. The file contents are system dependent, so check existing login-related files in the /etc/pam.d directory to see what they look like. On Linux, the mysql-unix file might look like this:

```
#%PAM-1.0
auth include password-auth
account include password-auth
```

For macOS, use login rather than password-auth.

The PAM file format might differ on some systems. For example, on Ubuntu and other Debianbased systems, use these file contents instead:

```
@include common-auth
@include common-account
@include common-session-noninteractive
```

4. Create a default proxy user (''@'') that maps external PAM users to the proxied accounts:

```
CREATE USER ''@''
 IDENTIFIED WITH authentication_pam
 AS 'mysql-unix, root=developer, users=data_entry';
```

Here, the authentication string contains the PAM service name, mysql-unix, which authenticates Unix passwords. The authentication string also maps external users in the root and users PAM groups to the developer and data\_entry MySQL user names, respectively.

The PAM group mapping list following the PAM service name is required when you set up proxy users. Otherwise, the plugin cannot tell how to perform mapping from external user names to the proper proxied MySQL user names.

![](_page_56_Picture_5.jpeg)

#### **Note**

If your MySQL installation has anonymous users, they might conflict with the default proxy user. For more information about this issue, and ways of dealing with it, see Default Proxy User and Anonymous User Conflicts.

5. Create the proxied accounts and grant to each one the privileges it should have:

```
CREATE USER 'developer'@'localhost'
 IDENTIFIED WITH mysql_no_login;
CREATE USER 'data_entry'@'localhost'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL PRIVILEGES
 ON mydevdb.*
 TO 'developer'@'localhost';
GRANT ALL PRIVILEGES
 ON mydb.*
 TO 'data_entry'@'localhost';
```

The proxied accounts use the mysql\_no\_login authentication plugin to prevent clients from using the accounts to log in directly to the MySQL server. Instead, users who authenticate using PAM are expected to use the developer or data\_entry account by proxy based on their PAM group. (This assumes that the plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login](#page-94-0) [Pluggable Authentication".](#page-94-0)) For alternative methods of protecting proxied accounts against direct use, see Preventing Direct Login to Proxied Accounts.

6. Grant to the proxy account the PROXY privilege for each proxied account:

```
GRANT PROXY
 ON 'developer'@'localhost'
 TO ''@'';
GRANT PROXY
 ON 'data_entry'@'localhost'
 TO ''@'';
```

7. Use the mysql command-line client to connect to the MySQL server as antonio.

```
$> mysql --user=antonio --password --enable-cleartext-plugin
Enter password: antonio_password
```

The server authenticates the connection using the default ''@'' proxy account. The resulting privileges for antonio depend on which PAM groups antonio is a member of. If antonio is a member of the root PAM group, the PAM plugin maps root to the developer MySQL user name and returns that name to the server. The server verifies that ''@'' has the PROXY privilege for developer and permits the connection. The following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-------------------+---------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-------------------+---------------------+--------------+
| antonio@localhost | developer@localhost | ''@'' |
```

+-------------------+---------------------+--------------+

This demonstrates that the antonio operating system user is authenticated to have the privileges granted to the developer MySQL user, and that proxying occurs through the default proxy account.

If antonio is not a member of the root PAM group but is a member of the users PAM group, a similar process occurs, but the plugin maps user PAM group membership to the data\_entry MySQL user name and returns that name to the server:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-------------------+----------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-------------------+----------------------+--------------+
| antonio@localhost | data_entry@localhost | ''@'' |
+-------------------+----------------------+--------------+
```

This demonstrates that the antonio operating system user is authenticated to have the privileges of the data\_entry MySQL user, and that proxying occurs through the default proxy account.

![](_page_57_Picture_6.jpeg)

#### **Note**

The client-side mysql\_clear\_password authentication plugin leaves the password untouched, so client programs send it to the MySQL server as cleartext. This enables the password to be passed as is to PAM. A cleartext password is necessary to use the server-side PAM library, but may be a security problem in some configurations. These measures minimize the risk:

- To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it (for example, with the --enablecleartext-plugin option). See [Section 8.4.1.4, "Client-Side Cleartext](#page-47-0) [Pluggable Authentication"](#page-47-0).
- To avoid password exposure with the mysql\_clear\_password plugin enabled, MySQL clients should connect to the MySQL server using an encrypted connection. See [Section 8.3.1, "Configuring MySQL to Use](#page-8-0) [Encrypted Connections".](#page-8-0)

# <span id="page-57-0"></span>**PAM Authentication Access to Unix Password Store**

On some systems, Unix authentication uses a password store such as /etc/shadow, a file that typically has restricted access permissions. This can cause MySQL PAM-based authentication to fail. Unfortunately, the PAM implementation does not permit distinguishing "password could not be checked" (due, for example, to inability to read /etc/shadow) from "password does not match." If you are using Unix password store for PAM authentication, you may be able to enable access to it from MySQL using one of the following methods:

- Assuming that the MySQL server is run from the mysql operating system account, put that account in the shadow group that has /etc/shadow access:
  - 1. Create a shadow group in /etc/group.
  - 2. Add the mysql operating system user to the shadow group in /etc/group.
  - 3. Assign /etc/group to the shadow group and enable the group read permission:

```
chgrp shadow /etc/shadow
chmod g+r /etc/shadow
```

- 4. Restart the MySQL server.
- If you are using the pam\_unix module and the unix\_chkpwd utility, enable password store access as follows:

```
chmod u-s /usr/sbin/unix_chkpwd
setcap cap_dac_read_search+ep /usr/sbin/unix_chkpwd
```

Adjust the path to unix\_chkpwd as necessary for your platform.

## <span id="page-58-0"></span>**PAM Authentication Debugging**

The PAM authentication plugin checks at initialization time whether the AUTHENTICATION\_PAM\_LOG environment value is set. In MySQL 8.0.35 and earlier, the value does not matter. If so, the plugin enables logging of diagnostic messages to the standard output. These messages may be helpful for debugging PAM-related issues that occur when the plugin performs authentication. You should be aware that, in these versions, passwords are included in these messages.

Beginning with MySQL 8.0.36, setting AUTHENTICATION\_PAM\_LOG=1 (or some other arbitrary value) produces the same diagnostic messages, but does not include any passwords. If you wish to include passwords in these messages, set AUTHENTICATION\_PAM\_LOG=PAM\_LOG\_WITH\_SECRET\_INFO.

Some messages include reference to PAM plugin source files and line numbers, which enables plugin actions to be tied more closely to the location in the code where they occur.

Another technique for debugging connection failures and determining what is happening during connection attempts is to configure PAM authentication to permit all connections, then check the system log files. This technique should be used only on a temporary basis, and not on a production server.

Configure a PAM service file named /etc/pam.d/mysql-any-password with these contents (the format may differ on some systems):

```
#%PAM-1.0
auth required pam_permit.so
account required pam_permit.so
```

Create an account that uses the PAM plugin and names the mysql-any-password PAM service:

```
CREATE USER 'testuser'@'localhost'
 IDENTIFIED WITH authentication_pam
 AS 'mysql-any-password';
```

The mysql-any-password service file causes any authentication attempt to return true, even for incorrect passwords. If an authentication attempt fails, that tells you the configuration problem is on the MySQL side. Otherwise, the problem is on the operating system/PAM side. To see what might be happening, check system log files such as /var/log/secure, /var/log/audit.log, /var/log/ syslog, or /var/log/messages.

After determining what the problem is, remove the mysql-any-password PAM service file to disable any-password access.