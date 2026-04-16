---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL includes several components and plugins that implement security features:

- Plugins for authenticating attempts by clients to connect to MySQL Server. Plugins are available for several authentication protocols. For general discussion of the authentication process, see [Section 8.2.17, "Pluggable Authentication".](#page-41-0) For characteristics of specific authentication plugins, see [Section 8.4.1, "Authentication Plugins".](#page-93-0)
- A password-validation component for implementing password strength policies and assessing the strength of potential passwords. See [Section 8.4.3, "The Password Validation Component"](#page-192-0).
- Keyring plugins that provide secure storage for sensitive information. See Section 8.4.4, "The MySQL Keyring".
- (MySQL Enterprise Edition only) MySQL Enterprise Audit, implemented using a server plugin, uses the open MySQL Audit API to enable standard, policy-based monitoring and logging of connection and query activity executed on specific MySQL servers. Designed to meet the Oracle audit specification, MySQL Enterprise Audit provides an out of box, easy to use auditing and compliance

solution for applications that are governed by both internal and external regulatory guidelines. See Section 8.4.5, "MySQL Enterprise Audit".

- A function enables applications to add their own message events to the audit log. See Section 8.4.6, "The Audit Message Component".
- (MySQL Enterprise Edition only) MySQL Enterprise Firewall, an application-level firewall that enables database administrators to permit or deny SQL statement execution based on matching against lists of accepted statement patterns. This helps harden MySQL Server against attacks such as SQL injection or attempts to exploit applications by using them outside of their legitimate query workload characteristics. See Section 8.4.7, "MySQL Enterprise Firewall".
- (MySQL Enterprise Edition only) MySQL Enterprise Data Masking and De-Identification, implemented as a plugin library containing a plugin and a set of functions. Data masking hides sensitive information by replacing real values with substitutes. MySQL Enterprise Data Masking and De-Identification functions enable masking existing data using several methods such as obfuscation (removing identifying characteristics), generation of formatted random data, and data replacement or substitution. See Section 8.5, "MySQL Enterprise Data Masking and De-Identification".

# <span id="page-93-0"></span>**8.4.1 Authentication Plugins**

![](_page_93_Picture_6.jpeg)

#### **Note**

If you are looking for information about the authentication\_oci plugin, it is MySQL HeatWave Service only. See [authentication\\_oci plugin](https://docs.oracle.com/en-us/iaas/mysql-database/doc/connecting-db-system.md#MYAAS-GUID-232CA959-1FDD-4AA8-A77D-0A551C881C09), in the MySQL HeatWave Service manual.

The following sections describe pluggable authentication methods available in MySQL and the plugins that implement these methods. For general discussion of the authentication process, see [Section 8.2.17, "Pluggable Authentication".](#page-41-0)

The default authentication plugin is determined as described in [The Default Authentication Plugin.](#page-43-0)

# <span id="page-93-1"></span>**8.4.1.1 Native Pluggable Authentication**

MySQL includes a mysql\_native\_password plugin that implements native authentication; that is, authentication based on the password hashing method in use from before the introduction of pluggable authentication.

![](_page_93_Picture_13.jpeg)

#### **Note**

The mysql\_native\_password authentication plugin is deprecated as of MySQL 8.0.34, disabled by default in MySQL 8.4, and removed as of MySQL 9.0.0.

The following table shows the plugin names on the server and client sides.

**Table 8.14 Plugin and Library Names for Native Password Authentication**

| Plugin or File     | Plugin or File Name         |
|--------------------|-----------------------------|
| Server-side plugin | mysql_native_password       |
| Client-side plugin | mysql_native_password       |
| Library file       | None (plugins are built in) |

The following sections provide installation and usage information specific to native pluggable authentication:

- [Installing Native Pluggable Authentication](#page-94-1)
- [Using Native Pluggable Authentication](#page-94-2)
- [Disabling Native Pluggable Authentication](#page-94-3)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-94-1"></span>**Installing Native Pluggable Authentication**

The mysql\_native\_password plugin exists in server and client forms:

- The server-side plugin is built into the server, but is disabled by default. To enable it, start the MySQL Server with --mysql-native-password=ON or by including mysql\_native\_password=ON in the [mysqld] section of your MySQL configuration file.
- The client-side plugin is built into the libmysqlclient client library and is available to any program linked against libmysqlclient.

### <span id="page-94-2"></span>**Using Native Pluggable Authentication**

MySQL client programs in MySQL 8.4 (and later) use caching\_sha2\_password for authentication by default. Use the --default-auth option to set mysql\_native\_password as the default client-side authentication plugin, if that is what is desired, like this:

```
$> mysql --default-auth=mysql_native_password ...
```

# <span id="page-94-3"></span>**Disabling Native Pluggable Authentication**

In MySQL 8.4, the mysql\_native\_password server-side plugin is disabled by default. To keep it disabled, be sure the server is started without specifying the --mysql-native-password option. Using --mysql-native-password=OFF also works for this purpose, but is not required. In addition, do not enable mysql\_native\_password in your MySQL configuration file to keep it disabled.

When the plugin is disabled, all of the operations that depend on the plugin are inaccessible. Specifically:

• Defined user accounts that authenticate with mysql\_native\_password encounter an error when they attempt to connect.

```
$> MYSQL -u userx -p
ERROR 1045 (28000): Access denied for user 'userx'@'localhost' (using password: NO)
```

The server writes these errors to the server log.

• Attempts to create a new user account or to alter an existing user account identified with mysql\_native\_password also fail and emit an error.

```
mysql> CREATE USER userxx@localhost IDENTIFIED WITH 'mysql_native_password';
ERROR 1524 (HY000): Plugin 'mysql_native_password' is not loaded
mysql> ALTER USER userxy@localhost IDENTIFIED WITH 'mysql_native_password';
ERROR 1524 (HY000): Plugin 'mysql_native_password' is not loaded
```

For instructions on enabling the plugin, see [Installing Native Pluggable Authentication](#page-94-1).

# <span id="page-94-0"></span>**8.4.1.2 Caching SHA-2 Pluggable Authentication**

MySQL provides two authentication plugins that implement SHA-256 hashing for user account passwords:

- caching\_sha2\_password: Implements SHA-256 authentication (like sha256\_password), but uses caching on the server side for better performance and has additional features for wider applicability.
- sha256\_password (deprecated): Implements basic SHA-256 authentication. This is deprecated and subject to removal, do not use this authentication plugin.

This section describes the caching SHA-2 authentication plugin. For information about the original basic (noncaching) deprecated plugin, see [Section 8.4.1.3, "SHA-256 Pluggable Authentication".](#page-99-0)

![](_page_95_Picture_1.jpeg)

#### **Important**

In MySQL 8.4, caching\_sha2\_password is the default authentication plugin rather than mysql\_native\_password (deprecated). For information about the implications of this change for server operation and compatibility of the server with clients and connectors, see [caching\\_sha2\\_password as the Preferred](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-caching-sha2-password) [Authentication Plugin](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-caching-sha2-password).

![](_page_95_Picture_4.jpeg)

#### **Important**

To connect to the server using an account that authenticates with the caching\_sha2\_password plugin, you must use either a secure connection or an unencrypted connection that supports password exchange using an RSA key pair, as described later in this section. Either way, the caching\_sha2\_password plugin uses MySQL's encryption capabilities. See [Section 8.3, "Using Encrypted Connections"](#page-66-0).

![](_page_95_Picture_7.jpeg)

#### **Note**

In the name sha256\_password, "sha256" refers to the 256-bit digest length the plugin uses for encryption. In the name caching\_sha2\_password, "sha2" refers more generally to the SHA-2 class of encryption algorithms, of which 256 bit encryption is one instance. The latter name choice leaves room for future expansion of possible digest lengths without changing the plugin name.

The caching\_sha2\_password plugin has these advantages, compared to the deprecated sha256\_password plugin:

- On the server side, an in-memory cache enables faster reauthentication of users who have connected previously when they connect again.
- RSA-based password exchange is available regardless of the SSL library against which MySQL is linked.
- Support is provided for client connections that use the Unix socket-file and shared-memory protocols.

The following table shows the plugin names on the server and client sides.

**Table 8.15 Plugin and Library Names for SHA-2 Authentication**

| Plugin or File     | Plugin or File Name         |
|--------------------|-----------------------------|
| Server-side plugin | caching_sha2_password       |
| Client-side plugin | caching_sha2_password       |
| Library file       | None (plugins are built in) |

The following sections provide installation and usage information specific to caching SHA-2 pluggable authentication:

- [Installing SHA-2 Pluggable Authentication](#page-95-0)
- [Using SHA-2 Pluggable Authentication](#page-96-0)
- [Cache Operation for SHA-2 Pluggable Authentication](#page-99-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-95-0"></span>**Installing SHA-2 Pluggable Authentication**

The caching\_sha2\_password plugin exists in server and client forms:

• The server-side plugin is built into the server, need not be loaded explicitly, and cannot be disabled by unloading it.

• The client-side plugin is built into the libmysqlclient client library and is available to any program linked against libmysqlclient.

The server-side plugin uses the sha2\_cache\_cleaner audit plugin as a helper to perform password cache management. sha2\_cache\_cleaner, like caching\_sha2\_password, is built in and need not be installed.

### <span id="page-96-0"></span>**Using SHA-2 Pluggable Authentication**

To set up an account that uses the caching\_sha2\_password plugin for SHA-256 password hashing, use the following statement, where password is the desired account password:

```
CREATE USER 'sha2user'@'localhost'
IDENTIFIED WITH caching_sha2_password BY 'password';
```

The server assigns the caching\_sha2\_password plugin to the account and uses it to encrypt the password using SHA-256, storing those values in the plugin and authentication\_string columns of the mysql.user system table.

The preceding instructions do not assume that caching\_sha2\_password is the default authentication plugin. If caching\_sha2\_password is the default authentication plugin, a simpler CREATE USER syntax can be used:

```
CREATE USER 'sha2user'@'localhost' IDENTIFIED BY 'password';
```

The default plugin is determined by the value of the authentication\_policy system variable; the default is to use caching\_sha2\_password.

To use a different plugin, you must specify it using IDENTIFIED WITH. For example, to specify the deprecated mysql\_native\_password plugin, use this statement:

```
CREATE USER 'nativeuser'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'password';
```

caching\_sha2\_password supports connections over secure transport. If you follow the RSA configuration procedure given later in this section, it also supports encrypted password exchange using RSA over unencrypted connections. RSA support has these characteristics:

- On the server side, two system variables name the RSA private and public key-pair files: caching\_sha2\_password\_private\_key\_path and caching\_sha2\_password\_public\_key\_path. The database administrator must set these variables at server startup if the key files to use have names that differ from the system variable default values.
- The server uses the caching\_sha2\_password\_auto\_generate\_rsa\_keys system variable to determine whether to automatically generate the RSA key-pair files. See [Section 8.3.3, "Creating](#page-81-0) [SSL and RSA Certificates and Keys"](#page-81-0).
- The Caching\_sha2\_password\_rsa\_public\_key status variable displays the RSA public key value used by the caching\_sha2\_password authentication plugin.
- Clients that are in possession of the RSA public key can perform RSA key pair-based password exchange with the server during the connection process, as described later.
- For connections by accounts that authenticate with caching\_sha2\_password and RSA key pairbased password exchange, the server does not send the RSA public key to clients by default. Clients can use a client-side copy of the required public key, or request the public key from the server.

Use of a trusted local copy of the public key enables the client to avoid a round trip in the client/ server protocol, and is more secure than requesting the public key from the server. On the other hand, requesting the public key from the server is more convenient (it requires no management of a client-side file) and may be acceptable in secure network environments.

- For command-line clients, use the --server-public-key-path option to specify the RSA public key file. Use the --get-server-public-key option to request the public key from the server. The following programs support the two options: mysql, mysqlsh, mysqladmin, mysqlbinlog, mysqlcheck, mysqldump, mysqlimport, mysqlshow, mysqlslap, mysqltest.
- For programs that use the C API, call [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) to specify the RSA public key file by passing the MYSQL\_SERVER\_PUBLIC\_KEY option and the name of the file, or request the public key from the server by passing the MYSQL\_OPT\_GET\_SERVER\_PUBLIC\_KEY option.
- For replicas, use the CHANGE REPLICATION SOURCE TO statement with the SOURCE\_PUBLIC\_KEY\_PATH option to specify the RSA public key file, or the GET\_SOURCE\_PUBLIC\_KEY option to request the public key from the source. For Group Replication, the group\_replication\_recovery\_public\_key\_path and group\_replication\_recovery\_get\_public\_key system variables serve the same purpose.

In all cases, if the option is given to specify a valid public key file, it takes precedence over the option to request the public key from the server.

For clients that use the caching\_sha2\_password plugin, passwords are never exposed as cleartext when connecting to the server. How password transmission occurs depends on whether a secure connection or RSA encryption is used:

- If the connection is secure, an RSA key pair is unnecessary and is not used. This applies to TCP connections encrypted using TLS, as well as Unix socket-file and shared-memory connections. The password is sent as cleartext but cannot be snooped because the connection is secure.
- If the connection is not secure, an RSA key pair is used. This applies to TCP connections not encrypted using TLS and named-pipe connections. RSA is used only for password exchange between client and server, to prevent password snooping. When the server receives the encrypted password, it decrypts it. A scramble is used in the encryption to prevent repeat attacks.

To enable use of an RSA key pair for password exchange during the client connection process, use the following procedure:

- 1. Create the RSA private and public key-pair files using the instructions in [Section 8.3.3, "Creating](#page-81-0) [SSL and RSA Certificates and Keys"](#page-81-0).
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

4. Restart the server, then connect to it and check the

Caching\_sha2\_password\_rsa\_public\_key status variable value. The value actually displayed differs from that shown here, but should be nonempty:

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

### <span id="page-99-1"></span>**Cache Operation for SHA-2 Pluggable Authentication**

On the server side, the caching\_sha2\_password plugin uses an in-memory cache for faster authentication of clients who have connected previously. Entries consist of account-name/passwordhash pairs. The cache works like this:

- 1. When a client connects, caching\_sha2\_password checks whether the client and password match some cache entry. If so, authentication succeeds.
- 2. If there is no matching cache entry, the plugin attempts to verify the client against the credentials in the mysql.user system table. If this succeeds, caching\_sha2\_password adds an entry for the client to the hash. Otherwise, authentication fails and the connection is rejected.

In this way, when a client first connects, authentication against the mysql.user system table occurs. When the client connects subsequently, faster authentication against the cache occurs.

Password cache operations other than adding entries are handled by the sha2\_cache\_cleaner audit plugin, which performs these actions on behalf of caching\_sha2\_password:

- It clears the cache entry for any account that is renamed or dropped, or any account for which the credentials or authentication plugin are changed.
- It empties the cache when the FLUSH PRIVILEGES statement is executed.
- It empties the cache at server shutdown. (This means the cache is not persistent across server restarts.)

Cache clearing operations affect the authentication requirements for subsequent client connections. For each user account, the first client connection for the user after any of the following operations must use a secure connection (made using TCP using TLS credentials, a Unix socket file, or shared memory) or RSA key pair-based password exchange:

- After account creation.
- After a password change for the account.
- After RENAME USER for the account.
- After FLUSH PRIVILEGES.

FLUSH PRIVILEGES clears the entire cache and affects all accounts that use the caching\_sha2\_password plugin. The other operations clear specific cache entries and affect only accounts that are part of the operation.

Once the user authenticates successfully, the account is entered into the cache and subsequent connections do not require a secure connection or the RSA key pair, until another cache clearing event occurs that affects the account. (When the cache can be used, the server uses a challengeresponse mechanism that does not use cleartext password transmission and does not require a secure connection.)

# <span id="page-99-0"></span>**8.4.1.3 SHA-256 Pluggable Authentication**

MySQL provides two authentication plugins that implement SHA-256 hashing for user account passwords:

• caching\_sha2\_password: Implements SHA-256 authentication (like sha256\_password), but uses caching on the server side for better performance and has additional features for wider applicability.

• sha256\_password (deprecated): Implements basic SHA-256 authentication.

This section describes the original noncaching SHA-2 authentication plugin. For information about the caching plugin, see [Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication".](#page-94-0)

![](_page_100_Picture_3.jpeg)

#### **Important**

In MySQL 8.4, caching\_sha2\_password is the default authentication plugin rather than mysql\_native\_password (deprecated). For information about the implications of this change for server operation and compatibility of the server with clients and connectors, see [caching\\_sha2\\_password as the Preferred](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-caching-sha2-password) [Authentication Plugin](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.md#upgrade-caching-sha2-password).

Because caching\_sha2\_password is the default authentication plugin in MySQL 8.4 and provides a superset of the capabilities of the sha256\_password authentication plugin, sha256\_password is deprecated; expect it to be removed in a future version of MySQL. MySQL accounts that authenticate using sha256\_password should be migrated to use caching\_sha2\_password instead.

![](_page_100_Picture_7.jpeg)

#### **Important**

To connect to the server using an account that authenticates with the sha256\_password plugin, you must use either a TLS connection or an unencrypted connection that supports password exchange using an RSA key pair, as described later in this section. Either way, the sha256\_password plugin uses MySQL's encryption capabilities. See [Section 8.3, "Using Encrypted](#page-66-0) [Connections"](#page-66-0).

![](_page_100_Picture_10.jpeg)

#### **Note**

In the name sha256\_password, "sha256" refers to the 256-bit digest length the plugin uses for encryption. In the name caching\_sha2\_password, "sha2" refers more generally to the SHA-2 class of encryption algorithms, of which 256 bit encryption is one instance. The latter name choice leaves room for future expansion of possible digest lengths without changing the plugin name.

The following table shows the plugin names on the server and client sides.

**Table 8.16 Plugin and Library Names for SHA-256 Authentication**

| Plugin or File     | Plugin or File Name         |
|--------------------|-----------------------------|
| Server-side plugin | sha256_password             |
| Client-side plugin | sha256_password             |
| Library file       | None (plugins are built in) |

The following sections provide installation and usage information specific to SHA-256 pluggable authentication:

- [Installing SHA-256 Pluggable Authentication](#page-100-0)
- [Using SHA-256 Pluggable Authentication](#page-101-0)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-100-0"></span>**Installing SHA-256 Pluggable Authentication**

The sha256\_password (deprecated) plugin exists in server and client forms:

• The server-side plugin is built into the server, need not be loaded explicitly, and cannot be disabled by unloading it.

• The client-side plugin is built into the libmysqlclient client library and is available to any program linked against libmysqlclient.

### <span id="page-101-0"></span>**Using SHA-256 Pluggable Authentication**

To set up an account that uses the deprecated sha256\_password plugin for SHA-256 password hashing, use the following statement, where password is the desired account password:

```
CREATE USER 'sha256user'@'localhost'
IDENTIFIED WITH sha256_password BY 'password';
```

The server assigns the sha256\_password plugin to the account and uses it to encrypt the password using SHA-256, storing those values in the plugin and authentication\_string columns of the mysql.user system table.

(The IDENTIFIED WITH clause is not needed if sha256\_password is the default plugin; this can be specified using authentication\_policy.)

sha256\_password supports connections over secure transport. sha256\_password also supports encrypted password exchange using RSA over unencrypted connections if MySQL is compiled using OpenSSL, and the MySQL server to which you wish to connect is configured to support RSA (using the RSA configuration procedure given later in this section).

RSA support has these characteristics:

- On the server side, two system variables name the RSA private and public key-pair files: sha256\_password\_private\_key\_path and sha256\_password\_public\_key\_path. The database administrator must set these variables at server startup if the key files to use have names that differ from the system variable default values.
- The server uses the sha256\_password\_auto\_generate\_rsa\_keys system variable to determine whether to automatically generate the RSA key-pair files. See [Section 8.3.3, "Creating](#page-81-0) [SSL and RSA Certificates and Keys"](#page-81-0).
- The Rsa\_public\_key status variable displays the RSA public key value used by the sha256\_password authentication plugin.
- Clients that are in possession of the RSA public key can perform RSA key pair-based password exchange with the server during the connection process, as described later.
- For connections by accounts that authenticate with sha256\_password and RSA public key pairbased password exchange, the server sends the RSA public key to the client as needed. However, if a copy of the public key is available on the client host, the client can use it to save a round trip in the client/server protocol:
  - For these command-line clients, use the --server-public-key-path option to specify the RSA public key file: mysql, mysqladmin, mysqlbinlog, mysqlcheck, mysqldump, mysqlimport, mysqlshow, mysqlslap, mysqltest.
  - For programs that use the C API, call [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) to specify the RSA public key file by passing the MYSQL\_SERVER\_PUBLIC\_KEY option and the name of the file.
  - For replicas, use the CHANGE REPLICATION SOURCE TO statement with the SOURCE\_PUBLIC\_KEY\_PATH option to specify the RSA public key file. For Group Replication, the group\_replication\_recovery\_get\_public\_key system variable serves the same purpose.

For clients that use the sha256\_password plugin, passwords are never exposed as cleartext when connecting to the server. How password transmission occurs depends on whether a secure connection or RSA encryption is used:

• If the connection is secure, an RSA key pair is unnecessary and is not used. This applies to connections encrypted using TLS. The password is sent as cleartext but cannot be snooped because the connection is secure.

![](_page_102_Picture_1.jpeg)

#### **Note**

Unlike caching\_sha2\_password, the deprecated sha256\_password plugin does not treat shared-memory connections as secure, even though share-memory transport is secure by default.

- If the connection is not secure, and an RSA key pair is available, the connection remains unencrypted. This applies to connections not encrypted using TLS. RSA is used only for password exchange between client and server, to prevent password snooping. When the server receives the encrypted password, it decrypts it. A scramble is used in the encryption to prevent repeat attacks.
- If a secure connection is not used and RSA encryption is not available, the connection attempt fails because the password cannot be sent without being exposed as cleartext.

![](_page_102_Picture_6.jpeg)

#### **Note**

To use RSA password encryption with the deprecated sha256\_password plugin, the client and server both must be compiled using OpenSSL, not just one of them.

Assuming that MySQL has been compiled using OpenSSL, use the following procedure to enable use of an RSA key pair for password exchange during the client connection process:

- 1. Create the RSA private and public key-pair files using the instructions in [Section 8.3.3, "Creating](#page-81-0) [SSL and RSA Certificates and Keys"](#page-81-0).
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

After the server has been configured with the RSA key files, accounts that authenticate with the deprecated sha256\_password plugin have the option of using those key files to connect to the server. As mentioned previously, such accounts can use either a secure connection (in which case RSA is not used) or an unencrypted connection that performs password exchange using RSA. Suppose that an unencrypted connection is used. For example:

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

The public key value in the file named by the --server-public-key-path option should be the same as the key value in the server-side file named by the sha256\_password\_public\_key\_path system variable. If the key file contains a valid public key value but the value is incorrect, an accessdenied error occurs. If the key file does not contain a valid public key, the client program cannot use it. In this case, the deprecated sha256\_password plugin sends the public key to the client as if no - server-public-key-path option had been specified.

Client users can obtain the RSA public key two ways:

- The database administrator can provide a copy of the public key file.
- A client user who can connect to the server some other way can use a SHOW STATUS LIKE 'Rsa\_public\_key' statement and save the returned key value in a file.

# <span id="page-103-0"></span>**8.4.1.4 Client-Side Cleartext Pluggable Authentication**

A client-side authentication plugin is available that enables clients to send passwords to the server as cleartext, without hashing or encryption. This plugin is built into the MySQL client library.

The following table shows the plugin name.

**Table 8.17 Plugin and Library Names for Cleartext Authentication**

| Plugin or File     | Plugin or File Name       |
|--------------------|---------------------------|
| Server-side plugin | None, see discussion      |
| Client-side plugin | mysql_clear_password      |
| Library file       | None (plugin is built in) |

Many client-side authentication plugins perform hashing or encryption of a password before the client sends it to the server. This enables clients to avoid sending passwords as cleartext.

Hashing or encryption cannot be done for authentication schemes that require the server to receive the password as entered on the client side. In such cases, the client-side mysql\_clear\_password plugin is used, which enables the client to send the password to the server as cleartext. There is no corresponding server-side plugin. Rather, mysql\_clear\_password can be used on the client side in concert with any server-side plugin that needs a cleartext password. (Examples are the PAM

and simple LDAP authentication plugins; see [Section 8.4.1.5, "PAM Pluggable Authentication"](#page-104-0), and [Section 8.4.1.7, "LDAP Pluggable Authentication"](#page-119-0).)

The following discussion provides usage information specific to cleartext pluggable authentication. For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

![](_page_104_Picture_3.jpeg)

#### **Note**

Sending passwords as cleartext may be a security problem in some configurations. To avoid problems if there is any possibility that the password would be intercepted, clients should connect to MySQL Server using a method that protects the password. Possibilities include SSL (see [Section 8.3, "Using](#page-66-0) [Encrypted Connections"\)](#page-66-0), IPsec, or a private network.

To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it. This can be done in several ways:

- Set the LIBMYSQL\_ENABLE\_CLEARTEXT\_PLUGIN environment variable to a value that begins with 1, Y, or y. This enables the plugin for all client connections.
- The mysql, mysqladmin, mysqlcheck, mysqldump, mysqlshow, and mysqlslap client programs support an --enable-cleartext-plugin option that enables the plugin on a perinvocation basis.
- The [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) C API function supports a MYSQL\_ENABLE\_CLEARTEXT\_PLUGIN option that enables the plugin on a per-connection basis. Also, any program that uses libmysqlclient and reads option files can enable the plugin by including an enable-cleartext-plugin option in an option group read by the client library.

# <span id="page-104-0"></span>**8.4.1.5 PAM Pluggable Authentication**

![](_page_104_Picture_11.jpeg)

### **Note**

PAM pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

MySQL Enterprise Edition supports an authentication method that enables MySQL Server to use PAM (Pluggable Authentication Modules) to authenticate MySQL users. PAM enables a system to use a standard interface to access various kinds of authentication methods, such as traditional Unix passwords or an LDAP directory.

PAM pluggable authentication provides these capabilities:

- External authentication: PAM authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables and that authenticate using methods supported by PAM.
- Proxy user support: PAM authentication can return to MySQL a user name different from the external user name passed by the client program, based on the PAM groups the external user is a member of and the authentication string provided. This means that the plugin can return the MySQL user that defines the privileges the external PAM-authenticated user should have. For example, an operating system user named joe can connect and have the privileges of a MySQL user named developer.

PAM pluggable authentication has been tested on Linux and macOS; note that Windows does not support PAM.

The following table shows the plugin and library file names. The file name suffix might differ on your system. The file must be located in the directory named by the plugin\_dir system variable. For installation information, see [Installing PAM Pluggable Authentication](#page-106-0).

**Table 8.18 Plugin and Library Names for PAM Authentication**

| Plugin or File     | Plugin or File Name   |
|--------------------|-----------------------|
| Server-side plugin | authentication_pam    |
| Client-side plugin | mysql_clear_password  |
| Library file       | authentication_pam.so |

The client-side mysql\_clear\_password cleartext plugin that communicates with the server-side PAM plugin is built into the libmysqlclient client library and is included in all distributions, including community distributions. Inclusion of the client-side cleartext plugin in all MySQL distributions enables clients from any distribution to connect to a server that has the server-side PAM plugin loaded.

The following sections provide installation and usage information specific to PAM pluggable authentication:

- [How PAM Authentication of MySQL Users Works](#page-105-0)
- [Installing PAM Pluggable Authentication](#page-106-0)
- [Uninstalling PAM Pluggable Authentication](#page-107-0)
- [Using PAM Pluggable Authentication](#page-107-1)
- [PAM Unix Password Authentication without Proxy Users](#page-109-0)
- [PAM LDAP Authentication without Proxy Users](#page-110-0)
- [PAM Unix Password Authentication with Proxy Users and Group Mapping](#page-111-0)
- [PAM Authentication Access to Unix Password Store](#page-113-0)
- [PAM Authentication Debugging](#page-114-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0) For information about the mysql\_clear\_password plugin, see [Section 8.4.1.4,](#page-103-0) ["Client-Side Cleartext Pluggable Authentication".](#page-103-0) For proxy user information, see [Section 8.2.19, "Proxy](#page-50-0) [Users"](#page-50-0).

# <span id="page-105-0"></span>**How PAM Authentication of MySQL Users Works**

This section provides an overview of how MySQL and PAM work together to authenticate MySQL users. For examples showing how to set up MySQL accounts to use specific PAM services, see [Using](#page-107-1) [PAM Pluggable Authentication](#page-107-1).

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

### <span id="page-106-0"></span>**Installing PAM Pluggable Authentication**

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
```

```
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%pam%';
+--------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------------+---------------+
| authentication_pam | ACTIVE |
+--------------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the PAM plugin, see [Using PAM Pluggable Authentication.](#page-107-1)

### <span id="page-107-0"></span>**Uninstalling PAM Pluggable Authentication**

The method used to uninstall the PAM authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN authentication_pam;
```

### <span id="page-107-1"></span>**Using PAM Pluggable Authentication**

This section describes in general terms how to use the PAM authentication plugin to connect from MySQL client programs to the server. The following sections provide instructions for using PAM authentication in specific ways. It is assumed that the server is running with the server-side PAM plugin enabled, as described in [Installing PAM Pluggable Authentication](#page-106-0).

To refer to the PAM authentication plugin in the IDENTIFIED WITH clause of a CREATE USER statement, use the name authentication\_pam. For example:

```
CREATE USER user
 IDENTIFIED WITH authentication_pam
 AS 'auth_string';
```

The authentication string specifies the following types of information:

- The PAM service name (see [How PAM Authentication of MySQL Users Works\)](#page-105-0). Examples in the following discussion use a service name of mysql-unix for authentication using traditional Unix passwords, and mysql-ldap for authentication using LDAP.
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
- The PAM service name corresponds to the authentication method (mysql-unix or mysql-ldap in this discussion). To use a given PAM service, you must set up a PAM file with the same name in the PAM configuration directory (creating the file if it does not exist). In addition, you must name the PAM service in the authentication string of the CREATE USER statement for any account that authenticates using that PAM service.

The PAM authentication plugin checks at initialization time whether the AUTHENTICATION\_PAM\_LOG environment value is set in the server's startup environment. If so, the plugin enables logging of diagnostic messages to the standard output. Depending on how your server is started, the message might appear on the console or in the error log. These messages can be helpful for debugging PAMrelated issues that occur when the plugin performs authentication. For more information, see [PAM](#page-114-1) [Authentication Debugging.](#page-114-1)

### <span id="page-109-0"></span>**PAM Unix Password Authentication without Proxy Users**

This authentication scenario uses PAM to check external users defined in terms of operating system user names and Unix passwords, without proxying. Every such external user permitted to connect to MySQL Server should have a matching MySQL account that is defined to use PAM authentication through traditional Unix password store.

![](_page_109_Picture_8.jpeg)

#### **Note**

Traditional Unix passwords are checked using the /etc/shadow file. For information regarding possible issues related to this file, see [PAM](#page-113-0) [Authentication Access to Unix Password Store.](#page-113-0)

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

![](_page_110_Picture_7.jpeg)

### **Note**

The client-side mysql\_clear\_password authentication plugin leaves the password untouched, so client programs send it to the MySQL server as cleartext. This enables the password to be passed as is to PAM. A cleartext password is necessary to use the server-side PAM library, but may be a security problem in some configurations. These measures minimize the risk:

- To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it (for example, with the --enablecleartext-plugin option). See [Section 8.4.1.4, "Client-Side Cleartext](#page-103-0) [Pluggable Authentication"](#page-103-0).
- To avoid password exposure with the mysql\_clear\_password plugin enabled, MySQL clients should connect to the MySQL server using an encrypted connection. See [Section 8.3.1, "Configuring MySQL to Use](#page-67-0) [Encrypted Connections".](#page-67-0)

### <span id="page-110-0"></span>**PAM LDAP Authentication without Proxy Users**

This authentication scenario uses PAM to check external users defined in terms of operating system user names and LDAP passwords, without proxying. Every such external user permitted to connect to MySQL Server should have a matching MySQL account that is defined to use PAM authentication through LDAP.

To use PAM LDAP pluggable authentication for MySQL, these prerequisites must be satisfied:

- An LDAP server must be available for the PAM LDAP service to communicate with.
- Each LDAP user to be authenticated by MySQL must be present in the directory managed by the LDAP server.

![](_page_110_Picture_17.jpeg)

#### **Note**

Another way to use LDAP for MySQL user authentication is to use the LDAP-specific authentication plugins. See [Section 8.4.1.7, "LDAP Pluggable](#page-119-0) [Authentication".](#page-119-0)

Configure MySQL for PAM LDAP authentication as follows:

1. Verify that Unix authentication permits logins to the operating system with the user name antonio and password antonio\_password.

2. Set up PAM to authenticate MySQL connections using LDAP by creating a mysql-ldap PAM service file named /etc/pam.d/mysql-ldap. The file contents are system dependent, so check existing login-related files in the /etc/pam.d directory to see what they look like. On Linux, the mysql-ldap file might look like this:

```
#%PAM-1.0
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

4. Connecting to the server is the same as described in [PAM Unix Password Authentication without](#page-109-0) [Proxy Users](#page-109-0).

### <span id="page-111-0"></span>**PAM Unix Password Authentication with Proxy Users and Group Mapping**

The authentication scheme described here uses proxying and PAM group mapping to map connecting MySQL users who authenticate using PAM onto other MySQL accounts that define different sets of privileges. Users do not connect directly through the accounts that define the privileges. Instead, they connect through a default proxy account authenticated using PAM, such that all the external users are mapped to the MySQL accounts that hold the privileges. Any user who connects using the proxy account is mapped to one of those MySQL accounts, the privileges for which determine the database operations permitted to the external user.

The procedure shown here uses Unix password authentication. To use LDAP instead, see the early steps of [PAM LDAP Authentication without Proxy Users](#page-110-0).

![](_page_111_Picture_12.jpeg)

#### **Note**

Traditional Unix passwords are checked using the /etc/shadow file. For information regarding possible issues related to this file, see [PAM](#page-113-0) [Authentication Access to Unix Password Store.](#page-113-0)

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

![](_page_112_Picture_7.jpeg)

#### **Note**

If your MySQL installation has anonymous users, they might conflict with the default proxy user. For more information about this issue, and ways of dealing with it, see [Default Proxy User and Anonymous User Conflicts](#page-55-0).

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

The proxied accounts use the mysql\_no\_login authentication plugin to prevent clients from using the accounts to log in directly to the MySQL server. Instead, users who authenticate using PAM are expected to use the developer or data\_entry account by proxy based on their PAM group. (This assumes that the plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login](#page-151-0) [Pluggable Authentication".](#page-151-0)) For alternative methods of protecting proxied accounts against direct use, see [Preventing Direct Login to Proxied Accounts](#page-53-0).

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
+-------------------+---------------------+--------------+
```

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

![](_page_113_Picture_7.jpeg)

#### **Note**

The client-side mysql\_clear\_password authentication plugin leaves the password untouched, so client programs send it to the MySQL server as cleartext. This enables the password to be passed as is to PAM. A cleartext password is necessary to use the server-side PAM library, but may be a security problem in some configurations. These measures minimize the risk:

- To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it (for example, with the --enablecleartext-plugin option). See [Section 8.4.1.4, "Client-Side Cleartext](#page-103-0) [Pluggable Authentication"](#page-103-0).
- To avoid password exposure with the mysql\_clear\_password plugin enabled, MySQL clients should connect to the MySQL server using an encrypted connection. See [Section 8.3.1, "Configuring MySQL to Use](#page-67-0) [Encrypted Connections".](#page-67-0)

### <span id="page-113-0"></span>**PAM Authentication Access to Unix Password Store**

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

### <span id="page-114-1"></span>**PAM Authentication Debugging**

The PAM authentication plugin checks at initialization time whether the AUTHENTICATION\_PAM\_LOG environment value is set. If so, the plugin enables logging of diagnostic messages to the standard output. These messages may be helpful for debugging PAM-related issues that occur when the plugin performs authentication.

Setting AUTHENTICATION\_PAM\_LOG=1 (or some other arbitrary value) does not include any passwords. If you wish to include passwords in these messages, set AUTHENTICATION\_PAM\_LOG=PAM\_LOG\_WITH\_SECRET\_INFO.

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

# <span id="page-114-0"></span>**8.4.1.6 Windows Pluggable Authentication**

![](_page_114_Picture_18.jpeg)

### **Note**

Windows pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

MySQL Enterprise Edition for Windows supports an authentication method that performs external authentication on Windows, enabling MySQL Server to use native Windows services to authenticate client connections. Users who have logged in to Windows can connect from MySQL client programs to the server based on the information in their environment without specifying an additional password.

The client and server exchange data packets in the authentication handshake. As a result of this exchange, the server creates a security context object that represents the identity of the client in the Windows OS. This identity includes the name of the client account. Windows pluggable authentication uses the identity of the client to check whether it is a given account or a member of a group. By default, negotiation uses Kerberos to authenticate, then NTLM if Kerberos is unavailable.

Windows pluggable authentication provides these capabilities:

- External authentication: Windows authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables who have logged in to Windows.
- Proxy user support: Windows authentication can return to MySQL a user name different from the external user name passed by the client program. This means that the plugin can return the MySQL user that defines the privileges the external Windows-authenticated user should have. For example, a Windows user named joe can connect and have the privileges of a MySQL user named developer.

The following table shows the plugin and library file names. The file must be located in the directory named by the plugin\_dir system variable.

**Table 8.19 Plugin and Library Names for Windows Authentication**

| Plugin or File     | Plugin or File Name           |
|--------------------|-------------------------------|
| Server-side plugin | authentication_windows        |
| Client-side plugin | authentication_windows_client |
| Library file       | authentication_windows.dll    |

The library file includes only the server-side plugin. The client-side plugin is built into the libmysqlclient client library.

The server-side Windows authentication plugin is included only in MySQL Enterprise Edition. It is not included in MySQL community distributions. The client-side plugin is included in all distributions, including community distributions. This enables clients from any distribution to connect to a server that has the server-side plugin loaded.

The following sections provide installation and usage information specific to Windows pluggable authentication:

- [Installing Windows Pluggable Authentication](#page-115-0)
- [Uninstalling Windows Pluggable Authentication](#page-116-0)
- [Using Windows Pluggable Authentication](#page-116-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0) For proxy user information, see [Section 8.2.19, "Proxy Users"](#page-50-0).

### <span id="page-115-0"></span>**Installing Windows Pluggable Authentication**

This section describes how to install the server-side Windows authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file:

```
[mysqld]
plugin-load-add=authentication_windows.dll
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement:

```
INSTALL PLUGIN authentication_windows SONAME 'authentication_windows.dll';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%windows%';
+------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+------------------------+---------------+
| authentication_windows | ACTIVE |
+------------------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the Windows authentication plugin, see [Using Windows Pluggable Authentication](#page-116-1). Additional plugin control is provided by the authentication\_windows\_use\_principal\_name and authentication\_windows\_log\_level system variables. See Section 7.1.8, "Server System Variables".

### <span id="page-116-0"></span>**Uninstalling Windows Pluggable Authentication**

The method used to uninstall the Windows authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN authentication_windows;
```

In addition, remove any startup options that set Windows plugin-related system variables.

### <span id="page-116-1"></span>**Using Windows Pluggable Authentication**

The Windows authentication plugin supports the use of MySQL accounts such that users who have logged in to Windows can connect to the MySQL server without having to specify an additional password. It is assumed that the server is running with the server-side plugin enabled, as described in [Installing Windows Pluggable Authentication](#page-115-0). Once the DBA has enabled the server-side plugin and set up accounts to use it, clients can connect using those accounts with no other setup required on their part.

To refer to the Windows authentication plugin in the IDENTIFIED WITH clause of a CREATE USER statement, use the name authentication\_windows. Suppose that the Windows users Rafal and Tasha should be permitted to connect to MySQL, as well as any users in the Administrators or Power Users group. To set this up, create a MySQL account named sql\_admin that uses the Windows plugin for authentication:

```
CREATE USER sql_admin
 IDENTIFIED WITH authentication_windows
```

```
 AS 'Rafal, Tasha, Administrators, "Power Users"';
```

The plugin name is authentication\_windows. The string following the AS keyword is the authentication string. It specifies that the Windows users named Rafal or Tasha are permitted to authenticate to the server as the MySQL user sql\_admin, as are any Windows users in the Administrators or Power Users group. The latter group name contains a space, so it must be quoted with double quote characters.

After you create the sql\_admin account, a user who has logged in to Windows can attempt to connect to the server using that account:

```
C:\> mysql --user=sql_admin
```

No password is required here. The authentication\_windows plugin uses the Windows security API to check which Windows user is connecting. If that user is named Rafal or Tasha, or is a member of the Administrators or Power Users group, the server grants access and the client is authenticated as sql\_admin and has whatever privileges are granted to the sql\_admin account. Otherwise, the server denies access.

Authentication string syntax for the Windows authentication plugin follows these rules:

- The string consists of one or more user mappings separated by commas.
- Each user mapping associates a Windows user or group name with a MySQL user name:

```
win_user_or_group_name=mysql_user_name
win_user_or_group_name
```

For the latter syntax, with no mysql\_user\_name value given, the implicit value is the MySQL user created by the CREATE USER statement. Thus, these statements are equivalent:

```
CREATE USER sql_admin
 IDENTIFIED WITH authentication_windows
 AS 'Rafal, Tasha, Administrators, "Power Users"';
CREATE USER sql_admin
 IDENTIFIED WITH authentication_windows
 AS 'Rafal=sql_admin, Tasha=sql_admin, Administrators=sql_admin,
 "Power Users"=sql_admin';
```

- Each backslash character (\) in a value must be doubled because backslash is the escape character in MySQL strings.
- Leading and trailing spaces not inside double quotation marks are ignored.
- Unquoted win\_user\_or\_group\_name and mysql\_user\_name values can contain anything except equal sign, comma, or space.
- If a win\_user\_or\_group\_name and or mysql\_user\_name value is quoted with double quotation marks, everything between the quotation marks is part of the value. This is necessary, for example, if the name contains space characters. All characters within double quotes are legal except double quotation mark and backslash. To include either character, escape it with a backslash.
- win\_user\_or\_group\_name values use conventional syntax for Windows principals, either local or in a domain. Examples (note the doubling of backslashes):

```
domain\\user
.\\user
domain\\group
.\\group
BUILTIN\\WellKnownGroup
```

When invoked by the server to authenticate a client, the plugin scans the authentication string left to right for a user or group match to the Windows user. If there is a match, the plugin returns the corresponding mysql\_user\_name to the MySQL server. If there is no match, authentication fails. A user name match takes preference over a group name match. Suppose that the Windows user named win\_user is a member of win\_group and the authentication string looks like this:

```
'win_group = sql_user1, win_user = sql_user2'
```

When win\_user connects to the MySQL server, there is a match both to win\_group and to win\_user. The plugin authenticates the user as sql\_user2 because the more-specific user match takes precedence over the group match, even though the group is listed first in the authentication string.

Windows authentication always works for connections from the same computer on which the server is running. For cross-computer connections, both computers must be registered with Microsoft Active Directory. If they are in the same Windows domain, it is unnecessary to specify a domain name. It is also possible to permit connections from a different domain, as in this example:

```
CREATE USER sql_accounting
 IDENTIFIED WITH authentication_windows
 AS 'SomeDomain\\Accounting';
```

Here SomeDomain is the name of the other domain. The backslash character is doubled because it is the MySQL escape character within strings.

MySQL supports the concept of proxy users whereby a client can connect and authenticate to the MySQL server using one account but while connected has the privileges of another account (see [Section 8.2.19, "Proxy Users"\)](#page-50-0). Suppose that you want Windows users to connect using a single user name but be mapped based on their Windows user and group names onto specific MySQL accounts as follows:

- The local\_user and MyDomain\domain\_user local and domain Windows users should map to the local\_wlad MySQL account.
- Users in the MyDomain\Developers domain group should map to the local\_dev MySQL account.
- Local machine administrators should map to the local\_admin MySQL account.

To set this up, create a proxy account for Windows users to connect to, and configure this account so that users and groups map to the appropriate MySQL accounts (local\_wlad, local\_dev, local\_admin). In addition, grant the MySQL accounts the privileges appropriate to the operations they need to perform. The following instructions use win\_proxy as the proxy account, and local\_wlad, local\_dev, and local\_admin as the proxied accounts.

1. Create the proxy MySQL account:

```
CREATE USER win_proxy
 IDENTIFIED WITH authentication_windows
 AS 'local_user = local_wlad,
 MyDomain\\domain_user = local_wlad,
 MyDomain\\Developers = local_dev,
 BUILTIN\\Administrators = local_admin';
```

2. For proxying to work, the proxied accounts must exist, so create them:

```
CREATE USER local_wlad
 IDENTIFIED WITH mysql_no_login;
CREATE USER local_dev
 IDENTIFIED WITH mysql_no_login;
CREATE USER local_admin
 IDENTIFIED WITH mysql_no_login;
```

The proxied accounts use the mysql\_no\_login authentication plugin to prevent clients from using the accounts to log in directly to the MySQL server. Instead, users who authenticate using Windows are expected to use the win\_proxy proxy account. (This assumes that the plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication".](#page-151-0)) For alternative methods of protecting proxied accounts against direct use, see [Preventing Direct Login to Proxied Accounts.](#page-53-0)

You should also execute GRANT statements (not shown) that grant each proxied account the privileges required for MySQL access.

3. Grant to the proxy account the PROXY privilege for each proxied account:

```
GRANT PROXY ON local_wlad TO win_proxy;
GRANT PROXY ON local_dev TO win_proxy;
GRANT PROXY ON local_admin TO win_proxy;
```

Now the Windows users local\_user and MyDomain\domain\_user can connect to the MySQL server as win\_proxy and when authenticated have the privileges of the account given in the authentication string (in this case, local\_wlad). A user in the MyDomain\Developers group who connects as win\_proxy has the privileges of the local\_dev account. A user in the BUILTIN \Administrators group has the privileges of the local\_admin account.

To configure authentication so that all Windows users who do not have their own MySQL account go through a proxy account, substitute the default proxy account (''@'') for win\_proxy in the preceding instructions. For information about default proxy accounts, see [Section 8.2.19, "Proxy Users"](#page-50-0).

![](_page_119_Picture_6.jpeg)

### **Note**

If your MySQL installation has anonymous users, they might conflict with the default proxy user. For more information about this issue, and ways of dealing with it, see [Default Proxy User and Anonymous User Conflicts](#page-55-0).

To use the Windows authentication plugin with Connector/NET connection strings in Connector/NET 8.4 and higher, see [Connector/NET Authentication](https://dev.mysql.com/doc/connector-net/en/connector-net-authentication.md).

# <span id="page-119-0"></span>**8.4.1.7 LDAP Pluggable Authentication**

![](_page_119_Picture_11.jpeg)

### **Note**

LDAP pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see <https://www.mysql.com/products/>.

MySQL Enterprise Edition supports an authentication method that enables MySQL Server to use LDAP (Lightweight Directory Access Protocol) to authenticate MySQL users by accessing directory services such as X.500. MySQL uses LDAP to fetch user, credential, and group information.

LDAP pluggable authentication provides these capabilities:

- External authentication: LDAP authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables in LDAP directories.
- Proxy user support: LDAP authentication can return to MySQL a user name different from the external user name passed by the client program, based on the LDAP groups the external user is a member of. This means that an LDAP plugin can return the MySQL user that defines the privileges the external LDAP-authenticated user should have. For example, an LDAP user named joe can connect and have the privileges of a MySQL user named developer, if the LDAP group for joe is developer.
- Security: Using TLS, connections to the LDAP server can be secure.

Server and client plugins are available for simple and SASL-based LDAP authentication. On Microsoft Windows, the server plugin for SASL-based LDAP authentication is not supported, but the client plugin is.

The following tables show the plugin and library file names for simple and SASL-based LDAP authentication. The file name suffix might differ on your system. The files must be located in the directory named by the plugin\_dir system variable.

**Table 8.20 Plugin and Library Names for Simple LDAP Authentication**

| Plugin or File          | Plugin or File Name           |
|-------------------------|-------------------------------|
| Server-side plugin name | authentication_ldap_simple    |
| Client-side plugin name | mysql_clear_password          |
| Library file name       | authentication_ldap_simple.so |

**Table 8.21 Plugin and Library Names for SASL-Based LDAP Authentication**

| Plugin or File          | Plugin or File Name                                                |
|-------------------------|--------------------------------------------------------------------|
| Server-side plugin name | authentication_ldap_sasl                                           |
| Client-side plugin name | authentication_ldap_sasl_client                                    |
| Library file names      | authentication_ldap_sasl.so,<br>authentication_ldap_sasl_client.so |

The library files include only the authentication\_ldap\_XXX authentication plugins. The client-side mysql\_clear\_password plugin is built into the libmysqlclient client library.

Each server-side LDAP plugin works with a specific client-side plugin:

- The server-side authentication\_ldap\_simple plugin performs simple LDAP authentication. For connections by accounts that use this plugin, client programs use the client-side mysql\_clear\_password plugin, which sends the password to the server as cleartext. No password hashing or encryption is used, so a secure connection between the MySQL client and server is recommended to prevent password exposure.
- The server-side authentication\_ldap\_sasl plugin performs SASL-based LDAP authentication. For connections by accounts that use this plugin, client programs use the clientside authentication\_ldap\_sasl\_client plugin. The client-side and server-side SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

On Microsoft Windows platforms, both the server plugin and the client plugin are supported for SASL-based LDAP authentication.

The server-side LDAP authentication plugins are included only in MySQL Enterprise Edition. They are not included in MySQL community distributions. The client-side SASL LDAP plugin is included in all distributions, including community distributions, and, as mentioned previously, the client-side mysql\_clear\_password plugin is built into the libmysqlclient client library, which also is included in all distributions. This enables clients from any distribution to connect to a server that has the appropriate server-side plugin loaded.

The following sections provide installation and usage information specific to LDAP pluggable authentication:

- [Prerequisites for LDAP Pluggable Authentication](#page-121-0)
- [How LDAP Authentication of MySQL Users Works](#page-121-1)
- [Installing LDAP Pluggable Authentication](#page-122-0)
- [Uninstalling LDAP Pluggable Authentication](#page-124-0)
- [LDAP Pluggable Authentication and ldap.conf](#page-125-0)
- [Setting Timeouts for LDAP Pluggable Authentication](#page-125-1)
- [Using LDAP Pluggable Authentication](#page-126-0)

- [Simple LDAP Authentication \(Without Proxying\)](#page-127-0)
- [SASL-Based LDAP Authentication \(Without Proxying\)](#page-128-0)
- [LDAP Authentication with Proxying](#page-129-0)
- [LDAP Authentication Group Preference and Mapping Specification](#page-131-0)
- [LDAP Authentication User DN Suffixes](#page-132-0)
- [LDAP Authentication Methods](#page-133-0)
- [The GSSAPI/Kerberos Authentication Method](#page-133-1)
- [LDAP Search Referral](#page-139-0)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0) For information about the mysql\_clear\_password plugin, see [Section 8.4.1.4,](#page-103-0) ["Client-Side Cleartext Pluggable Authentication".](#page-103-0) For proxy user information, see [Section 8.2.19, "Proxy](#page-50-0) [Users"](#page-50-0).

![](_page_121_Picture_10.jpeg)

#### **Note**

If your system supports PAM and permits LDAP as a PAM authentication method, another way to use LDAP for MySQL user authentication is to use the server-side authentication\_pam plugin. See [Section 8.4.1.5, "PAM](#page-104-0) [Pluggable Authentication"](#page-104-0).

### <span id="page-121-0"></span>**Prerequisites for LDAP Pluggable Authentication**

To use LDAP pluggable authentication for MySQL, these prerequisites must be satisfied:

- An LDAP server must be available for the LDAP authentication plugins to communicate with.
- LDAP users to be authenticated by MySQL must be present in the directory managed by the LDAP server.
- An LDAP client library must be available on systems where the server-side authentication\_ldap\_sasl or authentication\_ldap\_simple plugin is used. Currently, supported libraries are the Windows native LDAP library, or the OpenLDAP library on non-Windows systems.
- To use SASL-based LDAP authentication:
  - The LDAP server must be configured to communicate with a SASL server.
  - A SASL client library must be available on systems where the client-side authentication\_ldap\_sasl\_client plugin is used. Currently, the only supported library is the Cyrus SASL library.
  - To use a particular SASL authentication method, any other services required by that method must be available. For example, to use GSSAPI/Kerberos, a GSSAPI library and Kerberos services must be available.

### <span id="page-121-1"></span>**How LDAP Authentication of MySQL Users Works**

This section provides an overview of how MySQL and LDAP work together to authenticate MySQL users. For examples showing how to set up MySQL accounts to use specific LDAP authentication plugins, see [Using LDAP Pluggable Authentication](#page-126-0). For information about authentication methods available to the LDAP plugins, see [LDAP Authentication Methods](#page-133-0).

The client connects to the MySQL server, providing the MySQL client user name and a password:

- For simple LDAP authentication, the client-side and server-side plugins communicate the password as cleartext. A secure connection between the MySQL client and server is recommended to prevent password exposure.
- For SASL-based LDAP authentication, the client-side and server-side plugins avoid sending the cleartext password between the MySQL client and server. For example, the plugins might use SASL messages for secure transmission of credentials within the LDAP protocol. For the GSSAPI authentication method, the client-side and server-side plugins communicate securely using Kerberos without using LDAP messages directly.

If the client user name and host name match no MySQL account, the connection is rejected.

If there is a matching MySQL account, authentication against LDAP occurs. The LDAP server looks for an entry matching the user and authenticates the entry against the LDAP password:

- If the MySQL account names an LDAP user distinguished name (DN), LDAP authentication uses that value and the LDAP password provided by the client. (To associate an LDAP user DN with a MySQL account, include a BY clause that specifies an authentication string in the CREATE USER statement that creates the account.)
- If the MySQL account names no LDAP user DN, LDAP authentication uses the user name and LDAP password provided by the client. In this case, the authentication plugin first binds to the LDAP server using the root DN and password as credentials to find the user DN based on the client user name, then authenticates that user DN against the LDAP password. This bind using the root credentials fails if the root DN and password are set to incorrect values, or are empty (not set) and the LDAP server does not permit anonymous connections.

If the LDAP server finds no match or multiple matches, authentication fails and the client connection is rejected.

If the LDAP server finds a single match, LDAP authentication succeeds (assuming that the password is correct), the LDAP server returns the LDAP entry, and the authentication plugin determines the name of the authenticated user based on that entry:

- If the LDAP entry has a group attribute (by default, the cn attribute), the plugin returns its value as the authenticated user name.
- If the LDAP entry has no group attribute, the authentication plugin returns the client user name as the authenticated user name.

The MySQL server compares the client user name with the authenticated user name to determine whether proxying occurs for the client session:

- If the names are the same, no proxying occurs: The MySQL account matching the client user name is used for privilege checking.
- If the names differ, proxying occurs: MySQL looks for an account matching the authenticated user name. That account becomes the proxied user, which is used for privilege checking. The MySQL account that matched the client user name is treated as the external proxy user.

### <span id="page-122-0"></span>**Installing LDAP Pluggable Authentication**

This section describes how to install the server-side LDAP authentication plugins. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library files must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The server-side plugin library file base names are authentication\_ldap\_simple and authentication\_ldap\_sasl. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

![](_page_123_Picture_1.jpeg)

#### **Note**

On Microsoft Windows, the server plugin for SASL-based LDAP authentication is not supported, but the client plugin is supported. On other platforms, both the server and client plugins are supported.

To load the plugins at server startup, use --plugin-load-add options to name the library files that contain them. With this plugin-loading method, the options must be given each time the server starts. Also, specify values for any plugin-provided system variables you wish to configure.

Each server-side LDAP plugin exposes a set of system variables that enable its operation to be configured. Setting most of these is optional, but you must set the variables that specify the LDAP server host (so the plugin knows where to connect) and base distinguished name for LDAP bind operations (to limit the scope of searches and obtain faster searches). For details about all LDAP system variables, see [Section 8.4.1.13, "Pluggable Authentication System Variables".](#page-165-0)

To load the plugins and set the LDAP server host and base distinguished name for LDAP bind operations, put lines such as these in your my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
plugin-load-add=authentication_ldap_simple.so
authentication_ldap_simple_server_host=127.0.0.1
authentication_ldap_simple_bind_base_dn="dc=example,dc=com"
plugin-load-add=authentication_ldap_sasl.so
authentication_ldap_sasl_server_host=127.0.0.1
authentication_ldap_sasl_bind_base_dn="dc=example,dc=com"
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugins at runtime, use these statements, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN authentication_ldap_simple
 SONAME 'authentication_ldap_simple.so';
INSTALL PLUGIN authentication_ldap_sasl
 SONAME 'authentication_ldap_sasl.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

After installing the plugins at runtime, the system variables that they expose become available and you can add settings for them to your my.cnf file to configure the plugins for subsequent restarts. For example:

```
[mysqld]
authentication_ldap_simple_server_host=127.0.0.1
authentication_ldap_simple_bind_base_dn="dc=example,dc=com"
authentication_ldap_sasl_server_host=127.0.0.1
authentication_ldap_sasl_bind_base_dn="dc=example,dc=com"
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

To set and persist each value at runtime rather than at startup, use these statements:

```
SET PERSIST authentication_ldap_simple_server_host='127.0.0.1';
SET PERSIST authentication_ldap_simple_bind_base_dn='dc=example,dc=com';
SET PERSIST authentication_ldap_sasl_server_host='127.0.0.1';
SET PERSIST authentication_ldap_sasl_bind_base_dn='dc=example,dc=com';
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change a value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%ldap%';
+----------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+----------------------------+---------------+
| authentication_ldap_sasl | ACTIVE |
| authentication_ldap_simple | ACTIVE |
+----------------------------+---------------+
```

If a plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with an LDAP plugin, see [Using LDAP Pluggable Authentication.](#page-126-0)

![](_page_124_Picture_5.jpeg)

#### **Additional Notes for SELinux**

On systems running EL6 or EL that have SELinux enabled, changes to the SELinux policy are required to enable the MySQL LDAP plugins to communicate with the LDAP service:

1. Create a file mysqlldap.te with these contents:

```
module mysqlldap 1.0;
require {
 type ldap_port_t;
 type mysqld_t;
 class tcp_socket name_connect;
}
#============= mysqld_t ==============
allow mysqld_t ldap_port_t:tcp_socket name_connect;
```

2. Compile the security policy module into a binary representation:

```
checkmodule -M -m mysqlldap.te -o mysqlldap.mod
```

3. Create an SELinux policy module package:

```
semodule_package -m mysqlldap.mod -o mysqlldap.pp
```

4. Install the module package:

```
semodule -i mysqlldap.pp
```

5. When the SELinux policy changes have been made, restart the MySQL server:

```
service mysqld restart
```

### <span id="page-124-0"></span>**Uninstalling LDAP Pluggable Authentication**

The method used to uninstall the LDAP authentication plugins depends on how you installed them:

- If you installed the plugins at server startup using --plugin-load-add options, restart the server without those options.
- If you installed the plugins at runtime using INSTALL PLUGIN, they remain installed across server restarts. To uninstall them, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN authentication_ldap_simple;
UNINSTALL PLUGIN authentication_ldap_sasl;
```

In addition, remove from your my.cnf file any startup options that set LDAP plugin-related system variables. If you used SET PERSIST to persist LDAP system variables, use RESET PERSIST to remove the settings.

### <span id="page-125-0"></span>**LDAP Pluggable Authentication and ldap.conf**

For installations that use OpenLDAP, the ldap.conf file provides global defaults for LDAP clients. Options can be set in this file to affect LDAP clients, including the LDAP authentication plugins. OpenLDAP uses configuration options in this order of precedence:

- Configuration specified by the LDAP client.
- Configuration specified in the ldap.conf file. To disable use of this file, set the LDAPNOINIT environment variable.
- OpenLDAP library built-in defaults.

If the library defaults or ldap.conf values do not yield appropriate option values, an LDAP authentication plugin may be able to set related variables to affect the LDAP configuration directly. For example, LDAP plugins can override ldap.conf for parameters such as these:

- TLS configuration: System variables are available to enable TLS and control CA configuration, such as [authentication\\_ldap\\_simple\\_tls](#page-185-0) and [authentication\\_ldap\\_simple\\_ca\\_path](#page-178-0) for simple LDAP authentication, and [authentication\\_ldap\\_sasl\\_tls](#page-175-0) and [authentication\\_ldap\\_sasl\\_ca\\_path](#page-170-0) for SASL LDAP authentication.
- LDAP referral. See [LDAP Search Referral.](#page-139-0)

For more information about ldap.conf consult the ldap.conf(5) man page.

### <span id="page-125-1"></span>**Setting Timeouts for LDAP Pluggable Authentication**

For MySQL accounts to connect to a MySQL server using LDAP pluggable authentication, the LDAP server must be available and operational. The interaction between the MySQL and LDAP servers involves two steps. First, the MySQL server establishes a connection to the LDAP server over TCP. Second, the MySQL server sends an LDAP binding request over the connection to the LDAP server and waits for a reply before authenticating the account. If either step fails, the MySQL account cannot connect to the MySQL server.

Short-duration timeouts that supersede a host system's timeout values are applied to both the connection and response steps by default. In all cases, the account user receives notification that their attempt to connect to MySQL is denied if the timeout expires. Client-side and server-side logging can provide additional information. On the client side, set the following environmental variable to elevate the detail level and then restart MySQL client:

```
AUTHENTICATION_LDAP_CLIENT_LOG=5
export AUTHENTICATION_LDAP_CLIENT_LOG
```

The following system variables support default timeouts for SASL-based and simple LDAP authentication on Linux platforms only.

**Table 8.22 System variables for SASL-based and simple LDAP Authentication**

| System Variable Name                                   | Default Timeout Value |
|--------------------------------------------------------|-----------------------|
| authentication_ldap_sasl_connect_timeout30 seconds     |                       |
| authentication_ldap_sasl_response_timeout 30 seconds   |                       |
| authentication_ldap_simple_connect_timeout 30 seconds  |                       |
| authentication_ldap_simple_response_timeout 30 seconds |                       |

Timeout values for LDAP authentication are adjustable at server startup and at runtime. If you set a timeout to zero using one of these variables, you effectively disengage it and MySQL server reverts to using the host system's default timeout.

![](_page_126_Picture_1.jpeg)

#### **Note**

Under the following combination of conditions, the actual wait time of the [authentication\\_ldap\\_sasl\\_connect\\_timeout](#page-170-1) setting doubles because (internally) the server must invoke the TCP connection twice:

- The LDAP server is offline.
- [authentication\\_ldap\\_sasl\\_connect\\_timeout](#page-170-1) has a value greater than zero.
- Connection pooling is in use (specifically, the [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-173-0) system variable has a value greater than zero, which enables pooling).

### <span id="page-126-0"></span>**Using LDAP Pluggable Authentication**

This section describes how to enable MySQL accounts to connect to the MySQL server using LDAP pluggable authentication. It is assumed that the server is running with the appropriate server-side plugins enabled, as described in [Installing LDAP Pluggable Authentication](#page-122-0), and that the appropriate client-side plugins are available on the client host.

This section does not describe LDAP configuration or administration. You are assumed to be familiar with those topics.

The two server-side LDAP plugins each work with a specific client-side plugin:

- The server-side authentication\_ldap\_simple plugin performs simple LDAP authentication. For connections by accounts that use this plugin, client programs use the client-side mysql\_clear\_password plugin, which sends the password to the server as cleartext. No password hashing or encryption is used, so a secure connection between the MySQL client and server is recommended to prevent password exposure.
- The server-side authentication\_ldap\_sasl plugin performs SASL-based LDAP authentication. For connections by accounts that use this plugin, client programs use the clientside authentication\_ldap\_sasl\_client plugin. The client-side and server-side SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

Overall requirements for LDAP authentication of MySQL users:

- There must be an LDAP directory entry for each user to be authenticated.
- There must be a MySQL user account that specifies a server-side LDAP authentication plugin and optionally names the associated LDAP user distinguished name (DN). (To associate an LDAP user DN with a MySQL account, include a BY clause in the CREATE USER statement that creates the account.) If an account names no LDAP string, LDAP authentication uses the user name specified by the client to find the LDAP entry.
- Client programs connect using the connection method appropriate for the server-side authentication plugin the MySQL account uses. For LDAP authentication, connections require the MySQL user name and LDAP password. In addition, for accounts that use the server-side authentication\_ldap\_simple plugin, invoke client programs with the --enable-cleartextplugin option to enable the client-side mysql\_clear\_password plugin.

The instructions here assume the following scenario:

• MySQL users betsy and boris authenticate to the LDAP entries for betsy\_ldap and boris\_ldap, respectively. (It is not necessary that the MySQL and LDAP user names differ. The use of different names in this discussion helps clarify whether an operation context is MySQL or LDAP.)

- LDAP entries use the uid attribute to specify user names. This may vary depending on LDAP server. Some LDAP servers use the cn attribute for user names rather than uid. To change the attribute, modify the [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-185-1) or [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-176-0) system variable appropriately.
- These LDAP entries are available in the directory managed by the LDAP server, to provide distinguished name values that uniquely identify each user:

```
uid=betsy_ldap,ou=People,dc=example,dc=com
uid=boris_ldap,ou=People,dc=example,dc=com
```

• CREATE USER statements that create MySQL accounts name an LDAP user in the BY clause, to indicate which LDAP entry the MySQL account authenticates against.

The instructions for setting up an account that uses LDAP authentication depend on which server-side LDAP plugin is used. The following sections describe several usage scenarios.

### <span id="page-127-0"></span>**Simple LDAP Authentication (Without Proxying)**

The procedure outlined in this section requires that

[authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-179-1) be set to an empty string, like this:

```
SET GLOBAL.authentication_ldap_simple_group_search_attr='';
```

Otherwise, proxying is used by default.

To set up a MySQL account for simple LDAP authentication, use a CREATE USER statement to specify the authentication\_ldap\_simple plugin, optionally including the LDAP user distinguished name (DN), as shown here:

```
CREATE USER user
 IDENTIFIED WITH authentication_ldap_simple
 [BY 'LDAP user DN'];
```

Suppose that MySQL user betsy has this entry in the LDAP directory:

```
uid=betsy_ldap,ou=People,dc=example,dc=com
```

Then the statement to create the MySQL account for betsy looks like this:

```
CREATE USER 'betsy'@'localhost'
 IDENTIFIED WITH authentication_ldap_simple
 AS 'uid=betsy_ldap,ou=People,dc=example,dc=com';
```

The authentication string specified in the BY clause does not include the LDAP password. That must be provided by the client user at connect time.

Clients connect to the MySQL server by providing the MySQL user name and LDAP password, and by enabling the client-side mysql\_clear\_password plugin:

```
$> mysql --user=betsy --password --enable-cleartext-plugin
Enter password: betsy_ldap_password
```

![](_page_127_Picture_20.jpeg)

#### **Note**

The client-side mysql\_clear\_password authentication plugin leaves the password untouched, so client programs send it to the MySQL server as cleartext. This enables the password to be passed as is to the LDAP server. A cleartext password is necessary to use the server-side LDAP library without SASL, but may be a security problem in some configurations. These measures minimize the risk:

• To make inadvertent use of the mysql\_clear\_password plugin less likely, MySQL clients must explicitly enable it (for example, with the --enablecleartext-plugin option). See [Section 8.4.1.4, "Client-Side Cleartext](#page-103-0) [Pluggable Authentication"](#page-103-0).

• To avoid password exposure with the mysql\_clear\_password plugin enabled, MySQL clients should connect to the MySQL server using an encrypted connection. See [Section 8.3.1, "Configuring MySQL to Use](#page-67-0) [Encrypted Connections".](#page-67-0)

The authentication process occurs as follows:

- 1. The client-side plugin sends betsy and betsy\_password as the client user name and LDAP password to the MySQL server.
- 2. The connection attempt matches the 'betsy'@'localhost' account. The server-side LDAP plugin finds that this account has an authentication string of 'uid=betsy\_ldap,ou=People,dc=example,dc=com' to name the LDAP user DN. The plugin sends this string and the LDAP password to the LDAP server.
- 3. The LDAP server finds the LDAP entry for betsy\_ldap and the password matches, so LDAP authentication succeeds.
- 4. The LDAP entry has no group attribute, so the server-side plugin returns the client user name (betsy) as the authenticated user. This is the same user name supplied by the client, so no proxying occurs and the client session uses the 'betsy'@'localhost' account for privilege checking.

Had the CREATE USER statement contained no BY clause to specify the betsy\_ldap LDAP distinguished name, authentication attempts would use the user name provided by the client (in this case, betsy). In the absence of an LDAP entry for betsy, authentication would fail.

# <span id="page-128-0"></span>**SASL-Based LDAP Authentication (Without Proxying)**

The procedure outlined in this section requires that [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-171-0) be set to an empty string, like this:

```
SET GLOBAL.authentication_ldap_sasl_group_search_attr='';
```

Otherwise, proxying is used by default.

To set up a MySQL account for SALS LDAP authentication, use a CREATE USER statement to specify the authentication\_ldap\_sasl plugin, optionally including the LDAP user distinguished name (DN), as shown here:

```
CREATE USER user
 IDENTIFIED WITH authentication_ldap_sasl
 [BY 'LDAP user DN'];
```

Suppose that MySQL user boris has this entry in the LDAP directory:

```
uid=boris_ldap,ou=People,dc=example,dc=com
```

Then the statement to create the MySQL account for boris looks like this:

```
CREATE USER 'boris'@'localhost'
 IDENTIFIED WITH authentication_ldap_sasl
 AS 'uid=boris_ldap,ou=People,dc=example,dc=com';
```

The authentication string specified in the BY clause does not include the LDAP password. That must be provided by the client user at connect time.

Clients connect to the MySQL server by providing the MySQL user name and LDAP password:

```
$> mysql --user=boris --password
```

```
Enter password: boris_ldap_password
```

For the server-side authentication\_ldap\_sasl plugin, clients use the client-side authentication\_ldap\_sasl\_client plugin. If a client program does not find the client-side plugin, specify a --plugin-dir option that names the directory where the plugin library file is installed.

The authentication process for boris is similar to that previously described for betsy with simple LDAP authentication, except that the client-side and server-side SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

# <span id="page-129-0"></span>**LDAP Authentication with Proxying**

LDAP authentication plugins support proxying, enabling a user to connect to the MySQL server as one user but assume the privileges of a different user. This section describes basic LDAP plugin proxy support. The LDAP plugins also support specification of group preference and proxy user mapping; see [LDAP Authentication Group Preference and Mapping Specification.](#page-131-0)

The proxying implementation described here is based on use of LDAP group attribute values to map connecting MySQL users who authenticate using LDAP onto other MySQL accounts that define different sets of privileges. Users do not connect directly through the accounts that define the privileges. Instead, they connect through a default proxy account authenticated with LDAP, such that all external logins are mapped to the proxied MySQL accounts that hold the privileges. Any user who connects using the proxy account is mapped to one of those proxied MySQL accounts, the privileges for which determine the database operations permitted to the external user.

The instructions here assume the following scenario:

- LDAP entries use the uid and cn attributes to specify user name and group values, respectively. To use different user and group attribute names, set the appropriate plugin-specific system variables:
  - For the authentication\_ldap\_simple plugin: Set [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-185-1) and [authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-179-1).
  - For the authentication\_ldap\_sasl plugin: Set [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-176-0) and [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-171-0).
- These LDAP entries are available in the directory managed by the LDAP server, to provide distinguished name values that uniquely identify each user:

```
uid=basha,ou=People,dc=example,dc=com,cn=accounting
uid=basil,ou=People,dc=example,dc=com,cn=front_office
```

At connect time, the group attribute values become the authenticated user names, so they name the accounting and front\_office proxied accounts.

• The examples assume use of SASL LDAP authentication. Make the appropriate adjustments for simple LDAP authentication.

Create the default proxy MySQL account:

```
CREATE USER ''@'%'
 IDENTIFIED WITH authentication_ldap_sasl;
```

The proxy account definition has no AS 'auth\_string' clause to name an LDAP user DN. Thus:

- When a client connects, the client user name becomes the LDAP user name to search for.
- The matching LDAP entry is expected to include a group attribute naming the proxied MySQL account that defines the privileges the client should have.

![](_page_130_Picture_1.jpeg)

#### **Note**

If your MySQL installation has anonymous users, they might conflict with the default proxy user. For more information about this issue, and ways of dealing with it, see [Default Proxy User and Anonymous User Conflicts](#page-55-0).

Create the proxied accounts and grant to each one the privileges it should have:

```
CREATE USER 'accounting'@'localhost'
 IDENTIFIED WITH mysql_no_login;
CREATE USER 'front_office'@'localhost'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL PRIVILEGES
 ON accountingdb.*
 TO 'accounting'@'localhost';
GRANT ALL PRIVILEGES
 ON frontdb.*
 TO 'front_office'@'localhost';
```

The proxied accounts use the mysql\_no\_login authentication plugin to prevent clients from using the accounts to log in directly to the MySQL server. Instead, users who authenticate using LDAP are expected to use the default ''@'%' proxy account. (This assumes that the mysql\_no\_login plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication".](#page-151-0)) For alternative methods of protecting proxied accounts against direct use, see [Preventing Direct Login to Proxied](#page-53-0) [Accounts](#page-53-0).

Grant to the proxy account the PROXY privilege for each proxied account:

```
GRANT PROXY
 ON 'accounting'@'localhost'
 TO ''@'%';
GRANT PROXY
 ON 'front_office'@'localhost'
 TO ''@'%';
```

Use the mysql command-line client to connect to the MySQL server as basha.

```
$> mysql --user=basha --password
Enter password: basha_password (basha LDAP password)
```

Authentication occurs as follows:

- 1. The server authenticates the connection using the default ''@'%' proxy account, for client user basha.
- 2. The matching LDAP entry is:

```
uid=basha,ou=People,dc=example,dc=com,cn=accounting
```

- 3. The matching LDAP entry has group attribute cn=accounting, so accounting becomes the authenticated proxied user.
- 4. The authenticated user differs from the client user name basha, with the result that basha is treated as a proxy for accounting, and basha assumes the privileges of the proxied accounting account. The following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-----------------+----------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-----------------+----------------------+--------------+
| basha@localhost | accounting@localhost | ''@'%' |
+-----------------+----------------------+--------------+
```

This demonstrates that basha uses the privileges granted to the proxied accounting MySQL account, and that proxying occurs through the default proxy user account.

Now connect as basil instead:

```
$> mysql --user=basil --password
Enter password: basil_password (basil LDAP password)
```

The authentication process for basil is similar to that previously described for basha:

- 1. The server authenticates the connection using the default ''@'%' proxy account, for client user basil.
- 2. The matching LDAP entry is:

```
uid=basil,ou=People,dc=example,dc=com,cn=front_office
```

- 3. The matching LDAP entry has group attribute cn=front\_office, so front\_office becomes the authenticated proxied user.
- 4. The authenticated user differs from the client user name basil, with the result that basil is treated as a proxy for front\_office, and basil assumes the privileges of the proxied front\_office account. The following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+-----------------+------------------------+--------------+
| USER() | CURRENT_USER() | @@proxy_user |
+-----------------+------------------------+--------------+
| basil@localhost | front_office@localhost | ''@'%' |
+-----------------+------------------------+--------------+
```

This demonstrates that basil uses the privileges granted to the proxied front\_office MySQL account, and that proxying occurs through the default proxy user account.

### <span id="page-131-0"></span>**LDAP Authentication Group Preference and Mapping Specification**

As described in [LDAP Authentication with Proxying,](#page-129-0) basic LDAP authentication proxying works by the principle that the plugin uses the first group name returned by the LDAP server as the MySQL proxied user account name. This simple capability does not enable specifying any preference about which group name to use if the LDAP server returns multiple group names, or specifying any name other than the group name as the proxied user name.

For MySQL accounts that use LDAP authentication, the authentication string can specify the following information to enable greater proxying flexibility:

- A list of groups in preference order, such that the plugin uses the first group name in the list that matches a group returned by the LDAP server.
- A mapping from group names to proxied user names, such that a group name when matched can provide a specified name to use as the proxied user. This provides an alternative to using the group name as the proxied user.

Consider the following MySQL proxy account definition:

```
CREATE USER ''@'%'
 IDENTIFIED WITH authentication_ldap_sasl
 AS '+ou=People,dc=example,dc=com#grp1=usera,grp2,grp3=userc';
```

The authentication string has a user DN suffix ou=People,dc=example,dc=com prefixed by the + character. Thus, as described in [LDAP Authentication User DN Suffixes,](#page-132-0) the full user DN is constructed from the user DN suffix as specified, plus the client user name as the uid attribute.

The remaining part of the authentication string begins with #, which signifies the beginning of group preference and mapping information. This part of the authentication string lists group names in the order grp1, grp2, grp3. The LDAP plugin compares that list with the set of group names returned by the LDAP server, looking in list order for a match against the returned names. The plugin uses the first match, or if there is no match, authentication fails.

Suppose that the LDAP server returns groups grp3, grp2, and grp7. The LDAP plugin uses grp2 because it is the first group in the authentication string that matches, even though it is not the first group returned by the LDAP server. If the LDAP server returns grp4, grp2, and grp1, the plugin uses grp1 even though grp2 also matches. grp1 has a precedence higher than grp2 because it is listed earlier in the authentication string.

Assuming that the plugin finds a group name match, it performs mapping from that group name to the MySQL proxied user name, if there is one. For the example proxy account, mapping occurs as follows:

- If the matching group name is grp1 or grp3, those are associated in the authentication string with user names usera and userc, respectively. The plugin uses the corresponding associated user name as the proxied user name.
- If the matching group name is grp2, there is no associated user name in the authentication string. The plugin uses grp2 as the proxied user name.

If the LDAP server returns a group in DN format, the LDAP plugin parses the group DN to extract the group name from it.

To specify LDAP group preference and mapping information, these principles apply:

- Begin the group preference and mapping part of the authentication string with a # prefix character.
- The group preference and mapping specification is a list of one or more items, separated by commas. Each item has the form group\_name=user\_name or group\_name. Items should be listed in group name preference order. For a group name selected by the plugin as a match from set of group names returned by the LDAP server, the two syntaxes differ in effect as follows:
  - For an item specified as group\_name=user\_name (with a user name), the group name maps to the user name, which is used as the MySQL proxied user name.
  - For an item specified as group\_name (with no user name), the group name is used as the MySQL proxied user name.
- To quote a group or user name that contains special characters such as space, surround it by double quote (") characters. For example, if an item has group and user names of my group name and my user name, it must be written in a group mapping using quotes:

```
"my group name"="my user name"
```

If an item has group and user names of my\_group\_name and my\_user\_name (which contain no special characters), it may but need not be written using quotes. Any of the following are valid:

```
my_group_name=my_user_name
my_group_name="my_user_name"
"my_group_name"=my_user_name
"my_group_name"="my_user_name"
```

- To escape a character, precede it by a backslash (\). This is useful particularly to include a literal double quote or backslash, which are otherwise not included literally.
- A user DN need not be present in the authentication string, but if present, it must precede the group preference and mapping part. A user DN can be given as a full user DN, or as a user DN suffix with a + prefix character. (See [LDAP Authentication User DN Suffixes.](#page-132-0))

### <span id="page-132-0"></span>**LDAP Authentication User DN Suffixes**

LDAP authentication plugins permit the authentication string that provides user DN information to begin with a + prefix character:

- In the absence of a + character, the authentication string value is treated as is without modification.
- If the authentication string begins with +, the plugin constructs the full user DN value from the user name sent by the client, together with the DN specified in the authentication string (with

the + removed). In the constructed DN, the client user name becomes the value of the attribute that specifies LDAP user names. This is uid by default; to change the attribute, modify the appropriate system variable ([authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-185-1) or [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-176-0)). The authentication string is stored as given in the mysql.user system table, with the full user DN constructed on the fly before authentication.

This account authentication string does not have + at the beginning, so it is taken as the full user DN:

```
CREATE USER 'baldwin'
 IDENTIFIED WITH authentication_ldap_simple
 AS 'uid=admin,ou=People,dc=example,dc=com';
```

The client connects with the user name specified in the account (baldwin). In this case, that name is not used because the authentication string has no prefix and thus fully specifies the user DN.

This account authentication string does have + at the beginning, so it is taken as just part of the user DN:

```
CREATE USER 'accounting'
 IDENTIFIED WITH authentication_ldap_simple
 AS '+ou=People,dc=example,dc=com';
```

The client connects with the user name specified in the account (accounting), which in this case is used as the uid attribute together with the authentication string to construct the user DN: uid=accounting,ou=People,dc=example,dc=com

The accounts in the preceding examples have a nonempty user name, so the client always connects to the MySQL server using the same name as specified in the account definition. If an account has an empty user name, such as the default anonymous ''@'%' proxy account described in [LDAP](#page-129-0) [Authentication with Proxying,](#page-129-0) clients might connect to the MySQL server with varying user names. But the principle is the same: If the authentication string begins with +, the plugin uses the user name sent by the client together with the authentication string to construct the user DN.

### <span id="page-133-0"></span>**LDAP Authentication Methods**

The LDAP authentication plugins use a configurable authentication method. The appropriate system variable and available method choices are plugin-specific:

- For the authentication\_ldap\_simple plugin: Set the [authentication\\_ldap\\_simple\\_auth\\_method\\_name](#page-176-1) system variable to configure the method. The permitted choices are SIMPLE and AD-FOREST.
- For the authentication\_ldap\_sasl plugin: Set the [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-168-0) system variable to configure the method. The permitted choices are SCRAM-SHA-1, SCRAM-SHA-256, and GSSAPI. (To determine which SASL LDAP methods are actually available on the host system, check the value of the Authentication\_ldap\_sasl\_supported\_methods status variable.)

See the system variable descriptions for information about each permitted method. Also, depending on the method, additional configuration may be needed, as described in the following sections.

### <span id="page-133-1"></span>**The GSSAPI/Kerberos Authentication Method**

Generic Security Service Application Program Interface (GSSAPI) is a security abstraction interface. Kerberos is an instance of a specific security protocol that can be used through that abstract interface. Using GSSAPI, applications authenticate to Kerberos to obtain service credentials, then use those credentials in turn to enable secure access to other services.

One such service is LDAP, which is used by the client-side and server-side SASL LDAP authentication plugins. When the [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-168-0) system variable is set to GSSAPI, these plugins use the GSSAPI/Kerberos authentication method. In this case, the plugins communicate securely using Kerberos without using LDAP messages directly. The server-side plugin

then communicates with the LDAP server to interpret LDAP authentication messages and retrieve LDAP groups.

GSSAPI/Kerberos is supported as an LDAP authentication method for MySQL servers and clients on Linux. It is useful in Linux environments where applications have access to LDAP through Microsoft Active Directory, which has Kerberos enabled by default.

The following discussion provides information about the configuration requirements for using the GSSAPI method. Familiarity is assumed with Kerberos concepts and operation. The following list briefly defines several common Kerberos terms. You may also find the Glossary section of [RFC 4120](https://tools.ietf.org/html/rfc4120) helpful.

- Principal: A named entity, such as a user or server.
- KDC: The key distribution center, comprising the AS and TGS:
  - AS: The authentication server; provides the initial ticket-granting ticket needed to obtain additional tickets.
  - TGS: The ticket-granting server; provides additional tickets to Kerberos clients that possess a valid TGT.
- TGT: The ticket-granting ticket; presented to the TGS to obtain service tickets for service access.

LDAP authentication using Kerberos requires both a KDC server and an LDAP server. This requirement can be satisfied in different ways:

- Active Directory includes both servers, with Kerberos authentication enabled by default in the Active Directory LDAP server.
- OpenLDAP provides an LDAP server, but a separate KDC server may be needed, with additional Kerberos setup required.

Kerberos must also be available on the client host. A client contacts the AS using a password to obtain a TGT. The client then uses the TGT to obtain access from the TGS to other services, such as LDAP.

The following sections discuss the configuration steps to use GSSAPI/Kerberos for SASL LDAP authentication in MySQL:

- [Verify Kerberos and LDAP Availability](#page-134-0)
- [Configure the Server-Side SASL LDAP Authentication Plugin for GSSAPI/Kerberos](#page-135-0)
- [Create a MySQL Account That Uses GSSAPI/Kerberos for LDAP Authentication](#page-136-0)
- [Use the MySQL Account to Connect to the MySQL Server](#page-137-0)
- [Client Configuration Parameters for LDAP Authentication](#page-139-1)

#### <span id="page-134-0"></span>**Verify Kerberos and LDAP Availability**

The following example shows how to test availability of Kerberos in Active Directory. The example makes these assumptions:

- Active Directory is running on the host named ldap\_auth.example.com with IP address 198.51.100.10.
- MySQL-related Kerberos authentication and LDAP lookups use the MYSQL.LOCAL domain.
- A principal named bredon@MYSQL.LOCAL is registered with the KDC. (In later discussion, this principal name is also associated with the MySQL account that authenticates to the MySQL server using GSSAPI/Kerberos.)

With those assumptions satisfied, follow this procedure:

1. Verify that the Kerberos library is installed and configured correctly in the operating system. For example, to configure a MYSQL.LOCAL domain for use during MySQL authentication, the /etc/ krb5.conf Kerberos configuration file should contain something like this:

```
[realms]
 MYSQL.LOCAL = {
 kdc = ldap_auth.example.com
 admin_server = ldap_auth.example.com
 default_domain = MYSQL.LOCAL
 }
```

2. You may need to add an entry to /etc/hosts for the server host:

```
198.51.100.10 ldap_auth ldap_auth.example.com
```

- 3. Check whether Kerberos authentication works correctly:
  - a. Use kinit to authenticate to Kerberos:

```
$> kinit bredon@MYSQL.LOCAL
Password for bredon@MYSQL.LOCAL: (enter password here)
```

The command authenticates for the Kerberos principal named bredon@MYSQL.LOCAL. Enter the principal's password when the command prompts for it. The KDC returns a TGT that is cached on the client side for use by other Kerberos-aware applications.

b. Use klist to check whether the TGT was obtained correctly. The output should be similar to this:

```
$> klist
Ticket cache: FILE:/tmp/krb5cc_244306
Default principal: bredon@MYSQL.LOCAL
Valid starting Expires Service principal
03/23/2021 08:18:33 03/23/2021 18:18:33 krbtgt/MYSQL.LOCAL@MYSQL.LOCAL
```

4. Check whether ldapsearch works with the Kerberos TGT using this command, which searches for users in the MYSQL.LOCAL domain:

```
ldapsearch -h 198.51.100.10 -Y GSSAPI -b "dc=MYSQL,dc=LOCAL"
```

#### <span id="page-135-0"></span>**Configure the Server-Side SASL LDAP Authentication Plugin for GSSAPI/Kerberos**

Assuming that the LDAP server is accessible through Kerberos as just described, configure the serverside SASL LDAP authentication plugin to use the GSSAPI/Kerberos authentication method. (For general LDAP plugin installation information, see [Installing LDAP Pluggable Authentication](#page-122-0).) Here is an example of plugin-related settings the server my.cnf file might contain:

```
[mysqld]
plugin-load-add=authentication_ldap_sasl.so
authentication_ldap_sasl_auth_method_name="GSSAPI"
authentication_ldap_sasl_server_host=198.51.100.10
authentication_ldap_sasl_server_port=389
authentication_ldap_sasl_bind_root_dn="cn=admin,cn=users,dc=MYSQL,dc=LOCAL"
authentication_ldap_sasl_bind_root_pwd="password"
authentication_ldap_sasl_bind_base_dn="cn=users,dc=MYSQL,dc=LOCAL"
authentication_ldap_sasl_user_search_attr="sAMAccountName"
```

Those option file settings configure the SASL LDAP plugin as follows:

- The --plugin-load-add option loads the plugin (adjust the .so suffix for your platform as necessary). If you loaded the plugin previously using an INSTALL PLUGIN statement, this option is unnecessary.
- [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-168-0) must be set to GSSAPI to use GSSAPI/ Kerberos as the SASL LDAP authentication method.

- [authentication\\_ldap\\_sasl\\_server\\_host](#page-175-1) and [authentication\\_ldap\\_sasl\\_server\\_port](#page-175-2) indicate the IP address and port number of the Active Directory server host for authentication.
- [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-169-0) and [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-170-2) configure the root DN and password for group search capability. This capability is required, but users may not have privileges to search. In such cases, it is necessary to provide root DN information:
  - In the DN option value, admin should be the name of an administrative LDAP account that has privileges to perform user searches.
  - In the password option value, password should be the admin account password.
- [authentication\\_ldap\\_sasl\\_bind\\_base\\_dn](#page-169-1) indicates the user DN base path, so that searches look for users in the MYSQL.LOCAL domain.
- [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-176-0) specifies a standard Active Directory search attribute, sAMAccountName. This attribute is used in searches to match logon names; attribute values are not the same as the user DN values.

#### <span id="page-136-0"></span>**Create a MySQL Account That Uses GSSAPI/Kerberos for LDAP Authentication**

MySQL authentication using the SASL LDAP authentication plugin with the GSSAPI/Kerberos method is based on a user that is a Kerberos principal. The following discussion uses a principal named bredon@MYSQL.LOCAL as this user, which must be registered in several places:

- The Kerberos administrator should register the user name as a Kerberos principal. This name should include a domain name. Clients use the principal name and password to authenticate with Kerberos and obtain a TGT.
- The LDAP administrator should register the user name in an LDAP entry. For example:

uid=bredon,dc=MYSQL,dc=LOCAL

![](_page_136_Picture_12.jpeg)

#### **Note**

In Active Directory (which uses Kerberos as the default authentication method), creating a user creates both the Kerberos principal and the LDAP entry.

• The MySQL DBA should create an account that has the Kerberos principal name as the user name and that authenticates using the SASL LDAP plugin.

Assume that the Kerberos principal and LDAP entry have been registered by the appropriate service administrators, and that, as previously described in [Installing LDAP Pluggable Authentication,](#page-122-0) and [Configure the Server-Side SASL LDAP Authentication Plugin for GSSAPI/Kerberos](#page-135-0), the MySQL server has been started with appropriate configuration settings for the server-side SASL LDAP plugin. The MySQL DBA then creates a MySQL account that corresponds to the Kerberos principal name, including the domain name.

![](_page_136_Picture_17.jpeg)

#### **Note**

The SASL LDAP plugin uses a constant user DN for Kerberos authentication and ignores any user DN configured from MySQL. This has certain implications:

- For any MySQL account that uses GSSAPI/Kerberos authentication, the authentication string in CREATE USER or ALTER USER statements should contain no user DN because it has no effect.
- Because the authentication string contains no user DN, it should contain group mapping information, to enable the user to be handled as a proxy user

that is mapped onto the desired proxied user. For information about proxying with the LDAP authentication plugin, see [LDAP Authentication with Proxying](#page-129-0).

The following statements create a proxy user named bredon@MYSQL.LOCAL that assumes the privileges of the proxied user named proxied\_krb\_usr. Other GSSAPI/Kerberos users that should have the same privileges can similarly be created as proxy users for the same proxied user.

```
-- create proxy account
CREATE USER 'bredon@MYSQL.LOCAL'
 IDENTIFIED WITH authentication_ldap_sasl
 BY '#krb_grp=proxied_krb_user';
-- create proxied account and grant its privileges;
-- use mysql_no_login plugin to prevent direct login
CREATE USER 'proxied_krb_user'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL
 ON krb_user_db.*
 TO 'proxied_krb_user';
-- grant to proxy account the
-- PROXY privilege for proxied account
GRANT PROXY
 ON 'proxied_krb_user'
 TO 'bredon@MYSQL.LOCAL';
```

Observe closely the quoting for the proxy account name in the first CREATE USER statement and the GRANT PROXY statement:

- For most MySQL accounts, the user and host are separate parts of the account name, and thus are quoted separately as 'user\_name'@'host\_name'.
- For LDAP Kerberos authentication, the user part of the account name includes the principal domain, so 'bredon@MYSQL.LOCAL' is quoted as a single value. Because no host part is given, the full MySQL account name uses the default of '%' as the host part: 'bredon@MYSQL.LOCAL'@'%'

![](_page_137_Picture_7.jpeg)

#### **Note**

When creating an account that authenticates using the authentication\_ldap\_sasl SASL LDAP authentication plugin with the GSSAPI/Kerberos authentication method, the CREATE USER statement includes the realm as part of the user name. This differs from creating accounts that use the authentication\_kerberos Kerberos plugin. For such accounts, the CREATE USER statement does not include the realm as part of the user name. Instead, specify the realm as the authentication string in the BY clause. See [Create a MySQL Account That Uses Kerberos Authentication](#page-145-0).

The proxied account uses the mysql\_no\_login authentication plugin to prevent clients from using the account to log in directly to the MySQL server. Instead, it is expected that users who authenticate using LDAP use the bredon@MYSQL.LOCAL proxy account. (This assumes that the mysql\_no\_login plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication"](#page-151-0).) For alternative methods of protecting proxied accounts against direct use, see [Preventing Direct Login to](#page-53-0) [Proxied Accounts.](#page-53-0)

#### <span id="page-137-0"></span>**Use the MySQL Account to Connect to the MySQL Server**

After a MySQL account that authenticates using GSSAPI/Kerberos has been set up, clients can use it to connect to the MySQL server. Kerberos authentication can take place either prior to or at the time of MySQL client program invocation:

• Prior to invoking the MySQL client program, the client user can obtain a TGT from the KDC independently of MySQL. For example, the client user can use kinit to authenticate to Kerberos by providing a Kerberos principal name and the principal password:

```
$> kinit bredon@MYSQL.LOCAL
Password for bredon@MYSQL.LOCAL: (enter password here)
```

The resulting TGT is cached and becomes available for use by other Kerberos-aware applications, such as programs that use the client-side SASL LDAP authentication plugin. In this case, the MySQL client program authenticates to the MySQL server using the TGT, so invoke the client without specifying a user name or password:

```
mysql --default-auth=authentication_ldap_sasl_client
```

As just described, when the TGT is cached, user-name and password options are not needed in the client command. If the command includes them anyway, they are handled as follows:

- If the command includes a user name, authentication fails if that name does not match the principal name in the TGT.
- If the command includes a password, the client-side plugin ignores it. Because authentication is based on the TGT, it can succeed even if the user-provided password is incorrect. For this reason, the plugin produces a warning if a valid TGT is found that causes a password to be ignored.
- If the Kerberos cache contains no TGT, the client-side SASL LDAP authentication plugin itself can obtain the TGT from the KDC. Invoke the client with options for the name and password of the Kerberos principal associated with the MySQL account (enter the command on a single line, then enter the principal password when prompted):

```
mysql --default-auth=authentication_ldap_sasl_client
 --user=bredon@MYSQL.LOCAL
 --password
```

• If the Kerberos cache contains no TGT and the client command specifies no principal name as the user name, authentication fails.

If you are uncertain whether a TGT exists, you can use klist to check.

Authentication occurs as follows:

- 1. The client uses the TGT to authenticate using Kerberos.
- 2. The server finds the LDAP entry for the principal and uses it to authenticate the connection for the bredon@MYSQL.LOCAL MySQL proxy account.
- 3. The group mapping information in the proxy account authentication string ('#krb\_grp=proxied\_krb\_user') indicates that the authenticated proxied user should be proxied\_krb\_user.
- 4. bredon@MYSQL.LOCAL is treated as a proxy for proxied\_krb\_user, and the following query returns output as shown:

```
mysql> SELECT USER(), CURRENT_USER(), @@proxy_user;
+------------------------------+--------------------+--------------------------+
| USER() | CURRENT_USER() | @@proxy_user |
+------------------------------+--------------------+--------------------------+
| bredon@MYSQL.LOCAL@localhost | proxied_krb_user@% | 'bredon@MYSQL.LOCAL'@'%' |
+------------------------------+--------------------+--------------------------+
```

The USER() value indicates the user name used for the client command (bredon@MYSQL.LOCAL) and the host from which the client connected (localhost).

The CURRENT\_USER() value is the full name of the proxied user account, which consists of the proxied\_krb\_user user part and the % host part.

The @@proxy\_user value indicates the full name of the account used to make the connection to the MySQL server, which consists of the bredon@MYSQL.LOCAL user part and the % host part.

This demonstrates that proxying occurs through the bredon@MYSQL.LOCAL proxy user account, and that bredon@MYSQL.LOCAL assumes the privileges granted to the proxied\_krb\_user proxied user account.

A TGT once obtained is cached on the client side and can be used until it expires without specifying the password again. However the TGT is obtained, the client-side plugin uses it to acquire service tickets and communicate with the server-side plugin.

![](_page_139_Picture_3.jpeg)

#### **Note**

When the client-side authentication plugin itself obtains the TGT, the client user may not want the TGT to be reused. As described in [Client Configuration](#page-139-1) [Parameters for LDAP Authentication](#page-139-1), the local /etc/krb5.conf file can be used to cause the client-side plugin to destroy the TGT when done with it.

The server-side plugin has no access to the TGT itself or the Kerberos password used to obtain it.

The LDAP authentication plugins have no control over the caching mechanism (storage in a local file, in memory, and so forth), but Kerberos utilities such as kswitch may be available for this purpose.

#### <span id="page-139-1"></span>**Client Configuration Parameters for LDAP Authentication**

The authentication\_ldap\_sasl\_client client-side SASL LDAP plugin reads the local / etc/krb5.conf file. If this file is missing or inaccessible, an error occurs. Assuming that the file is accessible, it can include an optional [appdefaults] section to provide information used by the plugin. Place the information within the mysql part of the section. For example:

```
[appdefaults]
 mysql = {
 ldap_server_host = "ldap_host.example.com"
 ldap_destroy_tgt = true
 }
```

The client-side plugin recognizes these parameters in the mysql section:

- The ldap\_server\_host value specifies the LDAP server host and can be useful when that host differs from the KDC server host specified in the [realms] section. By default, the plugin uses the KDC server host as the LDAP server host.
- The ldap\_destroy\_tgt value indicates whether the client-side plugin destroys the TGT after obtaining and using it. By default, ldap\_destroy\_tgt is false, but can be set to true to avoid TGT reuse. (This setting applies only to TGTs created by the client-side plugin, not TGTs created by other plugins or externally to MySQL.)

### <span id="page-139-0"></span>**LDAP Search Referral**

An LDAP server can be configured to delegate LDAP searches to another LDAP server, a functionality known as LDAP referral. Suppose that the server a.example.com holds a "dc=example,dc=com" root DN and wishes to delegate searches to another server b.example.com. To enable this, a.example.com would be configured with a named referral object having these attributes:

```
dn: dc=subtree,dc=example,dc=com
objectClass: referral
objectClass: extensibleObject
dc: subtree
ref: ldap://b.example.com/dc=subtree,dc=example,dc=com
```

An issue with enabling LDAP referral is that searches can fail with LDAP operation errors when the search base DN is the root DN, and referral objects are not set. A MySQL DBA might wish to avoid such referral errors for the LDAP authentication plugins, even though LDAP referral might be set globally in the ldap.conf configuration file. To configure on a plugin-specific basis whether the LDAP server should use LDAP referral when communicating with each plugin, set the [authentication\\_ldap\\_simple\\_referral](#page-182-1) and [authentication\\_ldap\\_sasl\\_referral](#page-174-1)

system variables. Setting either variable to ON or OFF causes the corresponding LDAP authentication plugin to tell the LDAP server whether to use referral during MySQL authentication. Each variable has a plugin-specific effect and does not affect other applications that communicate with the LDAP server. Both variables are OFF by default.

# <span id="page-140-0"></span>**8.4.1.8 Kerberos Pluggable Authentication**

![](_page_140_Picture_3.jpeg)

#### **Note**

Kerberos pluggable authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see<https://www.mysql.com/products/>.

MySQL Enterprise Edition supports an authentication method that enables users to authenticate to MySQL Server using Kerberos, provided that appropriate Kerberos tickets are available or can be obtained.

This authentication method is available in MySQL 8.4 for MySQL servers and clients on Linux. It is useful in Linux environments where applications have access to Microsoft Active Directory, which has Kerberos enabled by default. The client-side plugin is supported on Windows as well. The server-side plugin is still supported only on Linux.

![](_page_140_Picture_8.jpeg)

#### **Note**

Neither MySQL Shell nor MySQL Router currently support creating internally managed MySQL accounts for use with Kerberos. However, MySQL Shell supports using Kerberos to connect to MySQL Server. MySQL Router supports the use of an existing Kerberos-authenticated MySQL account for bootstrap and metadata access. MySQL Router also supports application connections that use Kerberos to authenticate to MySQL Server.

Kerberos pluggable authentication provides these capabilities:

- External authentication: Kerberos authentication enables MySQL Server to accept connections from users defined outside the MySQL grant tables who have obtained the proper Kerberos tickets.
- Security: Kerberos uses tickets together with symmetric-key cryptography, enabling authentication without sending passwords over the network. Kerberos authentication supports userless and passwordless scenarios.

The following table shows the plugin and library file names. The file name suffix might differ on your system. The file must be located in the directory named by the plugin\_dir system variable. For installation information, see [Installing Kerberos Pluggable Authentication](#page-142-0).

**Table 8.23 Plugin and Library Names for Kerberos Authentication**

| Plugin or File     | Plugin or File Name                                              |
|--------------------|------------------------------------------------------------------|
| Server-side plugin | authentication_kerberos                                          |
| Client-side plugin | authentication_kerberos_client                                   |
| Library file       | authentication_kerberos.so,<br>authentication_kerberos_client.so |

The server-side Kerberos authentication plugin is included only in MySQL Enterprise Edition. It is not included in MySQL community distributions. The client-side plugin is included in all distributions, including community distributions. This enables clients from any distribution to connect to a server that has the server-side plugin loaded.

The following sections provide installation and usage information specific to Kerberos pluggable authentication:

• [Prerequisites for Kerberos Pluggable Authentication](#page-141-0)

- [How Kerberos Authentication of MySQL Users Works](#page-141-1)
- [Installing Kerberos Pluggable Authentication](#page-142-0)
- [Using Kerberos Pluggable Authentication](#page-144-0)
- [Kerberos Authentication Debugging](#page-151-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-141-0"></span>**Prerequisites for Kerberos Pluggable Authentication**

To use Kerberos pluggable authentication for MySQL, these prerequisites must be satisfied:

- A Kerberos service must be available for the Kerberos authentication plugins to communicate with.
- Each Kerberos user (principal) to be authenticated by MySQL must be present in the database managed by the KDC server.
- A Kerberos client library must be available on systems where either the server-side or client-side Kerberos authentication plugin is used. In addition, GSSAPI is used as the interface for accessing Kerberos authentication, so a GSSAPI library must be available.

### <span id="page-141-1"></span>**How Kerberos Authentication of MySQL Users Works**

This section provides an overview of how MySQL and Kerberos work together to authenticate MySQL users. For examples showing how to set up MySQL accounts to use the Kerberos authentication plugins, see [Using Kerberos Pluggable Authentication](#page-144-0).

Familiarity is assumed here with Kerberos concepts and operation. The following list briefly defines several common Kerberos terms. You may also find the Glossary section of [RFC 4120](https://tools.ietf.org/html/rfc4120) helpful.

- Principal: A named entity, such as a user or server. In this discussion, certain principal-related terms occur frequently:
  - SPN: Service principal name; the name of a principal that represents a service.
  - UPN: User principal name; the name of a principal that represents a user.
- KDC: The key distribution center, comprising the AS and TGS:
  - AS: The authentication server; provides the initial ticket-granting ticket needed to obtain additional tickets.
  - TGS: The ticket-granting server; provides additional tickets to Kerberos clients that possess a valid TGT.
- TGT: The ticket-granting ticket; presented to the TGS to obtain service tickets for service access.
- ST: A service ticket; provides access to a service such as that offered by a MySQL server.

Authentication using Kerberos requires a KDC server, for example, as provided by Microsoft Active Directory.

Kerberos authentication in MySQL uses Generic Security Service Application Program Interface (GSSAPI), which is a security abstraction interface. Kerberos is an instance of a specific security protocol that can be used through that abstract interface. Using GSSAPI, applications authenticate to Kerberos to obtain service credentials, then use those credentials in turn to enable secure access to other services.

On Windows, the authentication\_kerberos\_client authentication plugin supports two modes, which the client user can set at runtime or specify in an option file:

- SSPI mode: Security Support Provider Interface (SSPI) implements GSSAPI (see Commands for Windows Clients in SSPI Mode). SSPI, while being compatible with GSSAPI at the wire level, only supports the Windows single sign-on scenario and specifically refers to the logged-on user. SSPI is the default mode on most Windows clients.
- GSSAPI mode: Supports GSSAPI through the MIT Kerberos library on Windows (see Commands for Windows Clients in GSSAPI Mode).

With the Kerberos authentication plugins, applications and MySQL servers are able to use the Kerberos authentication protocol to mutually authenticate users and MySQL services. This way both the user and the server are able to verify each other's identity. No passwords are sent over the network and Kerberos protocol messages are protected against eavesdropping and replay attacks.

Kerberos authentication follows these steps, where the server-side and client-side parts are performed using the authentication\_kerberos and authentication\_kerberos\_client authentication plugins, respectively:

- 1. The MySQL server sends to the client application its service principal name. This SPN must be registered in the Kerberos system, and is configured on the server side using the [authentication\\_kerberos\\_service\\_principal](#page-167-0) system variable.
- 2. Using GSSAPI, the client application creates a Kerberos client-side authentication session and exchanges Kerberos messages with the Kerberos KDC:
  - The client obtains a ticket-granting ticket from the authentication server.
  - Using the TGT, the client obtains a service ticket for MySQL from the ticket-granting service.

This step can be skipped or partially skipped if the TGT, ST, or both are already cached locally. The client optionally may use a client keytab file to obtain a TGT and ST without supplying a password.

- 3. Using GSSAPI, the client application presents the MySQL ST to the MySQL server.
- 4. Using GSSAPI, the MySQL server creates a Kerberos server-side authentication session. The server validates the user identity and the validity of the user request. It authenticates the ST using the service key configured in its service keytab file to determine whether authentication succeeds or fails, and returns the authentication result to the client.

Applications are able to authenticate using a provided user name and password, or using a locally cached TGT or ST (for example, created using kinit or similar). This design therefore covers use cases ranging from completely userless and passwordless connections, where Kerberos service tickets are obtained from a locally stored Kerberos cache, to connections where both user name and password are provided and used to obtain a valid Kerberos service ticket from a KDC, to send to the MySQL server.

As indicated in the preceding description, MySQL Kerberos authentication uses two kinds of keytab files:

- On the client host, a client keytab file may be used to obtain a TGT and ST without supplying a password. See [Client Configuration Parameters for Kerberos Authentication](#page-150-0).
- On the MySQL server host, a server-side service keytab file is used to verify service tickets received by the MySQL server from clients. The keytab file name is configured using the [authentication\\_kerberos\\_service\\_key\\_tab](#page-167-1) system variable.

For information about keytab files, see [https://web.mit.edu/kerberos/krb5-latest/doc/basic/](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md) [keytab\\_def.html.](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md)

### <span id="page-142-0"></span>**Installing Kerberos Pluggable Authentication**

This section describes how to install the server-side Kerberos authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

![](_page_143_Picture_1.jpeg)

#### **Note**

The server-side plugin is supported only on Linux systems. On Windows systems, only the client-side plugin is supported, which can be used on a Windows system to connect to a Linux server that uses Kerberos authentication.

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The server-side plugin library file base name is authentication\_kerberos. The file name suffix for Unix and Unix-like systems is .so.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. Also, specify values for any plugin-provided system variables you wish to configure. The plugin exposes these system variables, enabling its operation to be configured:

- [authentication\\_kerberos\\_service\\_principal](#page-167-0): The MySQL service principal name (SPN). This name is sent to clients that attempt to authenticate using Kerberos. The SPN must be present in the database managed by the KDC server. The default is mysql/host\_name@realm\_name.
- [authentication\\_kerberos\\_service\\_key\\_tab](#page-167-1): The keytab file for authenticating tickets received from clients. This file must exist and contain a valid key for the SPN or authentication of clients will fail. The default is mysql.keytab in the data directory.

For details about all Kerberos authentication system variables, see [Section 8.4.1.13, "Pluggable](#page-165-0) [Authentication System Variables"](#page-165-0).

To load the plugin and configure it, put lines such as these in your my.cnf file, using values for the system variables that are appropriate for your installation:

```
[mysqld]
plugin-load-add=authentication_kerberos.so
authentication_kerberos_service_principal=mysql/krbauth.example.com@MYSQL.LOCAL
authentication_kerberos_service_key_tab=/var/mysql/data/mysql.keytab
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement:

```
INSTALL PLUGIN authentication_kerberos
 SONAME 'authentication_kerberos.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

When you install the plugin at runtime without configuring its system variables in the my.cnf file, the system variable [authentication\\_kerberos\\_service\\_key\\_tab](#page-167-1) is set to the default value of mysql.keytab in the data directory. The value of this system variable cannot be changed at runtime, so if you need to specify a different file, you need to add the setting to your my.cnf file then restart the MySQL server. For example:

```
[mysqld]
authentication_kerberos_service_key_tab=/var/mysql/data/mysql.keytab
```

If the keytab file is not in the correct place or does not contain a valid SPN key, the MySQL server does not validate this, but clients return authentication errors until you fix the issue.

The [authentication\\_kerberos\\_service\\_principal](#page-167-0) system variable can be set and persisted at runtime without restarting the server, by using a SET PERSIST statement:

```
SET PERSIST authentication_kerberos_service_principal='mysql/krbauth.example.com@MYSQL.LOCAL';
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change a value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME = 'authentication_kerberos';
+-------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+-------------------------+---------------+
| authentication_kerberos | ACTIVE |
+-------------------------+---------------+
```

If a plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the Kerberos plugin, see [Using Kerberos Pluggable Authentication](#page-144-0).

### <span id="page-144-0"></span>**Using Kerberos Pluggable Authentication**

This section describes how to enable MySQL accounts to connect to the MySQL server using Kerberos pluggable authentication. It is assumed that the server is running with the server-side plugin enabled, as described in [Installing Kerberos Pluggable Authentication](#page-142-0), and that the client-side plugin is available on the client host.

- [Verify Kerberos Availability](#page-144-1)
- [Create a MySQL Account That Uses Kerberos Authentication](#page-145-0)
- [Use the MySQL Account to Connect to the MySQL Server](#page-146-0)
- [Client Configuration Parameters for Kerberos Authentication](#page-150-0)

#### <span id="page-144-1"></span>**Verify Kerberos Availability**

The following example shows how to test availability of Kerberos in Active Directory. The example makes these assumptions:

- Active Directory is running on the host named krbauth.example.com with IP address 198.51.100.11.
- MySQL-related Kerberos authentication uses the MYSQL.LOCAL domain, and also uses MYSQL.LOCAL as the realm name.
- A principal named karl@MYSQL.LOCAL is registered with the KDC. (In later discussion, this principal name is associated with the MySQL account that authenticates to the MySQL server using Kerberos.)

With those assumptions satisfied, follow this procedure:

1. Verify that the Kerberos library is installed and configured correctly in the operating system. For example, to configure a MYSQL.LOCAL domain and realm for use during MySQL authentication, the /etc/krb5.conf Kerberos configuration file should contain something like this:

```
[realms]
 MYSQL.LOCAL = {
 kdc = krbauth.example.com
 admin_server = krbauth.example.com
 default_domain = MYSQL.LOCAL
 }
```

2. You may need to add an entry to /etc/hosts for the server host:

```
198.51.100.11 krbauth krbauth.example.com
```

- 3. Check whether Kerberos authentication works correctly:
  - a. Use kinit to authenticate to Kerberos:

```
$> kinit karl@MYSQL.LOCAL
Password for karl@MYSQL.LOCAL: (enter password here)
```

The command authenticates for the Kerberos principal named karl@MYSQL.LOCAL. Enter the principal's password when the command prompts for it. The KDC returns a TGT that is cached on the client side for use by other Kerberos-aware applications.

b. Use klist to check whether the TGT was obtained correctly. The output should be similar to this:

```
$> klist
Ticket cache: FILE:/tmp/krb5cc_244306
Default principal: karl@MYSQL.LOCAL
Valid starting Expires Service principal
03/23/2021 08:18:33 03/23/2021 18:18:33 krbtgt/MYSQL.LOCAL@MYSQL.LOCAL
```

### <span id="page-145-0"></span>**Create a MySQL Account That Uses Kerberos Authentication**

MySQL authentication using the authentication\_kerberos authentication plugin is based on a Kerberos user principal name (UPN). The instructions here assume that a MySQL user named karl authenticates to MySQL using Kerberos, that the Kerberos realm is named MYSQL.LOCAL, and that the user principal name is karl@MYSQL.LOCAL. This UPN must be registered in several places:

- The Kerberos administrator should register the user name as a Kerberos principal. This name includes a realm name. Clients use the principal name and password to authenticate with Kerberos and obtain a ticket-granting ticket (TGT).
- The MySQL DBA should create an account that corresponds to the Kerberos principal name and that authenticates using the Kerberos plugin.

Assume that the Kerberos user principal name has been registered by the appropriate service administrator, and that, as previously described in [Installing Kerberos Pluggable Authentication](#page-142-0), the MySQL server has been started with appropriate configuration settings for the server-side Kerberos plugin. To create a MySQL account that corresponds to a Kerberos UPN of user@realm\_name, the MySQL DBA uses a statement like this:

```
CREATE USER user
 IDENTIFIED WITH authentication_kerberos
 BY 'realm_name';
```

The account named by user can include or omit the host name part. If the host name is omitted, it defaults to % as usual. The realm\_name is stored as the authentication\_string value for the account in the mysql.user system table.

To create a MySQL account that corresponds to the UPN karl@MYSQL.LOCAL, use this statement:

```
CREATE USER 'karl'
 IDENTIFIED WITH authentication_kerberos
 BY 'MYSQL.LOCAL';
```

If MySQL must construct the UPN for this account, for example, to obtain or validate tickets (TGTs or STs), it does so by combining the account name (ignoring any host name part) and the realm name. For example, the full account name resulting from the preceding CREATE USER statement is 'karl'@'%'. MySQL constructs the UPN from the user name part karl (ignoring the host name part) and the realm name MYSQL.LOCAL to produce karl@MYSQL.LOCAL.

![](_page_146_Picture_1.jpeg)

#### **Note**

Observe that when creating an account that authenticates using authentication\_kerberos, the CREATE USER statement does not include the UPN realm as part of the user name. Instead, specify the realm (MYSQL.LOCAL in this case) as the authentication string in the BY clause. This differs from creating accounts that use the authentication\_ldap\_sasl SASL LDAP authentication plugin with the GSSAPI/Kerberos authentication method. For such accounts, the CREATE USER statement does include the UPN realm as part of the user name. See [Create a MySQL Account That Uses](#page-136-0) [GSSAPI/Kerberos for LDAP Authentication](#page-136-0).

With the account set up, clients can use it to connect to the MySQL server. The procedure depends on whether the client host runs Linux or Windows, as indicated in the following discussion.

Use of authentication\_kerberos is subject to the restriction that UPNs with the same user part but a different realm part are not supported. For example, you cannot create MySQL accounts that correspond to both these UPNs:

```
kate@MYSQL.LOCAL
kate@EXAMPLE.COM
```

Both UPNs have a user part of kate but differ in the realm part (MYSQL.LOCAL versus EXAMPLE.COM). This is disallowed.

#### <span id="page-146-0"></span>**Use the MySQL Account to Connect to the MySQL Server**

After a MySQL account that authenticates using Kerberos has been set up, clients can use it to connect to the MySQL server as follows:

- 1. Authenticate to Kerberos with the user principal name (UPN) and its password to obtain a ticketgranting ticket (TGT).
- 2. Use the TGT to obtain a service ticket (ST) for MySQL.
- 3. Authenticate to the MySQL server by presenting the MySQL ST.

The first step (authenticating to Kerberos) can be performed various ways:

- Prior to connecting to MySQL:
  - On Linux or on Windows in GSSAPI mode, invoke kinit to obtain the TGT and save it in the Kerberos credentials cache.
  - On Windows in SSPI mode, authentication may already have been done at login time, which saves the TGT for the logged-in user in the Windows in-memory cache. kinit is not used and there is no Kerberos cache.
- When connecting to MySQL, the client program itself can obtain the TGT, if it can determine the required Kerberos UPN and password:
  - That information can come from sources such as command options or the operating system.
  - On Linux, clients also can use a keytab file or the /etc/krb5.conf configuration file. Windows clients in GSSAPI mode use a configuration file. Windows clients in SSPI mode use neither.

Details of the client commands for connecting to the MySQL server differ for Linux and Windows, so each host type is discussed separately, but these command properties apply regardless of host type:

• Each command shown includes the following options, but each one may be omitted under certain conditions:

- The --default-auth option specifies the name of the client-side authentication plugin (authentication\_kerberos\_client). This option may be omitted when the --user option is specified because in that case MySQL can determine the plugin from the user account information sent by MySQL server.
- The --plugin-dir option indicates to the client program the location of the authentication\_kerberos\_client plugin. This option may be omitted if the plugin is installed in the default (compiled-in) location.
- Commands should also include any other options such as --host or --port that are required to specify which MySQL server to connect to.
- Enter each command on a single line. If the command includes a --password option to solicit a password, enter the password of the Kerberos UPN associated with the MySQL user when prompted.

#### **Connection Commands for Linux Clients**

On Linux, the appropriate client command for connecting to the MySQL server varies depending on whether the command authenticates using a TGT from the Kerberos cache, or based on command options for the MySQL user name and the UPN password:

• Prior to invoking the MySQL client program, the client user can obtain a TGT from the KDC independently of MySQL. For example, the client user can use kinit to authenticate to Kerberos by providing a Kerberos user principal name and the principal password:

```
$> kinit karl@MYSQL.LOCAL
Password for karl@MYSQL.LOCAL: (enter password here)
```

The resulting TGT for the UPN is cached and becomes available for use by other Kerberos-aware applications, such as programs that use the client-side Kerberos authentication plugin. In this case, invoke the client without specifying a user-name or password option:

```
mysql
 --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
```

The client-side plugin finds the TGT in the cache, uses it to obtain a MySQL ST, and uses the ST to authenticate to the MySQL server.

As just described, when the TGT for the UPN is cached, user-name and password options are not needed in the client command. If the command includes them anyway, they are handled as follows:

• This command includes a user-name option:

```
mysql
 --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --user=karl
```

In this case, authentication fails if the user name specified by the option does not match the user name part of the UPN in the TGT.

• This command includes a password option, which you enter when prompted:

```
mysql
 --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --password
```

In this case, the client-side plugin ignores the password. Because authentication is based on the TGT, it can succeed even if the user-provided password is incorrect. For this reason, the plugin produces a warning if a valid TGT is found that causes a password to be ignored.

• If the Kerberos cache contains no TGT, the client-side Kerberos authentication plugin itself can obtain the TGT from the KDC. Invoke the client with options for the MySQL user name and the password, then enter the UPN password when prompted:

```
mysql --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --user=karl
 --password
```

The client-side Kerberos authentication plugin combines the user name (karl) and the realm specified in the user account (MYSQL.LOCAL) to construct the UPN (karl@MYSQL.LOCAL). The client-side plugin uses the UPN and password to obtain a TGT, uses the TGT to obtain a MySQL ST, and uses the ST to authenticate to the MySQL server.

Or, suppose that the Kerberos cache contains no TGT and the command specifies a password option but no user-name option:

```
mysql --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --password
```

The client-side Kerberos authentication plugin uses the operating system login name as the MySQL user name. It combines that user name and the realm in the user' MySQL account to construct the UPN. The client-side plugin uses the UPN and the password to obtain a TGT, uses the TGT to obtain a MySQL ST, and uses the ST to authenticate to the MySQL server.

If you are uncertain whether a TGT exists, you can use klist to check.

![](_page_148_Picture_8.jpeg)

#### **Note**

When the client-side Kerberos authentication plugin itself obtains the TGT, the client user may not want the TGT to be reused. As described in [Client](#page-150-0) [Configuration Parameters for Kerberos Authentication](#page-150-0), the local /etc/ krb5.conf file can be used to cause the client-side plugin to destroy the TGT when done with it.

### **Connection Commands for Windows Clients in SSPI Mode**

On Windows, using the default client-side plugin option (SSPI), the appropriate client command for connecting to the MySQL server varies depending on whether the command authenticates based on command options for the MySQL user name and the UPN password, or instead uses a TGT from the Windows in-memory cache. For details about GSSAPI mode on Windows, see Commands for Windows Clients in GSSAPI Mode.

A command can explicitly specify options for the MySQL user name and the UPN password, or the command can omit those options:

• This command includes options for the MySQL user name and UPN password:

```
mysql --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --user=karl
 --password
```

The client-side Kerberos authentication plugin combines the user name (karl) and the realm specified in the user account (MYSQL.LOCAL) to construct the UPN (karl@MYSQL.LOCAL). The client-side plugin uses the UPN and password to obtain a TGT, uses the TGT to obtain a MySQL ST, and uses the ST to authenticate to the MySQL server.

Any information in the Windows in-memory cache is ignored; the user-name and password option values take precedence.

• This command includes an option for the UPN password but not for the MySQL user name:

```
mysql
 --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --password
```

The client-side Kerberos authentication plugin uses the logged-in user name as the MySQL user name and combines that user name and the realm in the user's MySQL account to construct the UPN. The client-side plugin uses the UPN and the password to obtain a TGT, uses the TGT to obtain a MySQL ST, and uses the ST to authenticate to the MySQL server.

• This command includes no options for the MySQL user name or UPN password:

```
mysql
 --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
```

The client-side plugin obtains the TGT from the Windows in-memory cache, uses the TGT to obtain a MySQL ST, and uses the ST to authenticate to the MySQL server.

This approach requires the client host to be part of the Windows Server Active Directory (AD) domain. If that is not the case, help the MySQL client discover the IP address for the AD domain by manually entering the AD server and realm as the DNS server and prefix:

- 1. Start console.exe and select **Network and Sharing Center**.
- 2. From the sidebar of the Network and Sharing Center window, select **Change adapter settings**.
- 3. In the Network Connections window, right-click the network or VPN connection to configure and select **Properties**.
- 4. From the **Network** tab, locate and click **Internet Protocol Version 4 (TCP/IPv4)**, and then click **Properties**.
- 5. Click **Advanced** in the Internet Protocol Version 4 (TCP/IPv4) Properties dialog. The Advanced TCP/IP Settings dialog opens.
- 6. From the **DNS** tab, add the Active Directory server and realm as a DNS server and prefix.
- This command includes an option for the MySQL user name but not for the UPN password:

```
mysql
 --default-auth=authentication_kerberos_client
 --plugin-dir=path/to/plugin/directory
 --user=karl
```

The client-side Kerberos authentication plugin compares the name specified by the user-name option against the logged-in user name. If the names are the same, the plugin uses the logged-in user TGT for authentication. If the names differ, authentication fails.

#### **Connection Commands for Windows Clients in GSSAPI Mode**

On Windows, the client user must specify GSSAPI mode explicitly using the plugin\_authentication\_kerberos\_client\_mode plugin option to enable support through the MIT Kerberos library. The default mode is SSPI (see Commands for Windows Clients in SSPI Mode).

It is possible to specify GSSAPI mode:

• Prior to invoking the MySQL client program in an option file. The plugin variable name is valid using either underscores or dashes:

```
[mysql]
plugin_authentication_kerberos_client_mode=GSSAPI
```

Or:

```
[mysql]
plugin-authentication-kerberos-client-mode=GSSAPI
```

• At runtime from the command line using the mysql or mysqldump client programs. For example, the following commands (with underscores or dashes) causes mysql to connect to the server through the MIT Kerberos library on Windows.

mysql [connection-options] --plugin\_authentication\_kerberos\_client\_mode=GSSAPI

Or:

mysql [connection-options] --plugin-authentication-kerberos-client-mode=GSSAPI

- Client users can select GSSAPI mode from MySQL Workbench and some MySQL connectors. On client hosts running Windows, you can override the default location of:
  - The Kerberos configuration file by setting the KRB5\_CONFIG environment variable.
  - The default credential cache name with the KRB5CCNAME environment variable (for example, KRB5CCNAME=DIR:/mydir/).

For specific client-side plugin information, see the documentation at [https://dev.mysql.com/doc/.](https://dev.mysql.com/doc/)

The appropriate client command for connecting to the MySQL server varies depending on whether the command authenticates using a TGT from the MIT Kerberos cache, or based on command options for the MySQL user name and the UPN password. GSSAPI support through the MIT library on Windows is similar to GSSAPI on Linux (see Commands for Linux Clients), with the following exceptions:

- Tickets are always retrieved from or placed into the MIT Kerberos cache on hosts running Windows.
- kinit runs with Functional Accounts on Windows that have narrow permissions and specific roles. The client user does not know the kinit password. For an overview, see [https://docs.oracle.com/](https://docs.oracle.com/en/java/javase/11/tools/kinit.md) [en/java/javase/11/tools/kinit.html.](https://docs.oracle.com/en/java/javase/11/tools/kinit.md)
- If the client user supplies a password, the MIT Kerberos library on Windows decides whether to use it or rely on the existing ticket.
- The destroy\_tickets parameter, described in [Client Configuration Parameters for Kerberos](#page-150-0) [Authentication](#page-150-0), is not supported because the MIT Kerberos library on Windows does not support the required API member (get\_profile\_boolean) to read its value from configuration file.

### <span id="page-150-0"></span>**Client Configuration Parameters for Kerberos Authentication**

This section applies only for client hosts running Linux, not client hosts running Windows.

![](_page_150_Picture_17.jpeg)

#### **Note**

A client host running Windows with the authentication\_kerberos\_client client-side Kerberos plugin set to GSSAPI mode does support client configuration parameters, in general, but the MIT Kerberos library on Windows does not support the destroy\_tickets parameter described in this section.

If no valid ticket-granting ticket (TGT) exists at the time of MySQL client application invocation, the application itself may obtain and cache the TGT. If during the Kerberos authentication process the client application causes a TGT to be cached, any such TGT that was added can be destroyed after it is no longer needed, by setting the appropriate configuration parameter.

The authentication\_kerberos\_client client-side Kerberos plugin reads the local /etc/ krb5.conf file. If this file is missing or inaccessible, an error occurs. Assuming that the file is accessible, it can include an optional [appdefaults] section to provide information used by the plugin. Place the information within the mysql part of the section. For example:

[appdefaults]

```
 mysql = {
 destroy_tickets = true
 }
```

The client-side plugin recognizes these parameters in the mysql section:

• The destroy\_tickets value indicates whether the client-side plugin destroys the TGT after obtaining and using it. By default, destroy\_tickets is false, but can be set to true to avoid TGT reuse. (This setting applies only to TGTs created by the client-side plugin, not TGTs created by other plugins or externally to MySQL.)

On the client host, a client keytab file may be used to obtain a TGT and TS without supplying a password. For information about keytab files, see [https://web.mit.edu/kerberos/krb5-latest/doc/basic/](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md) [keytab\\_def.html.](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md)

# <span id="page-151-1"></span>**Kerberos Authentication Debugging**

The AUTHENTICATION\_KERBEROS\_CLIENT\_LOG environment variable enables or disables debug output for Kerberos authentication.

![](_page_151_Picture_7.jpeg)

#### **Note**

Despite CLIENT in the name AUTHENTICATION\_KERBEROS\_CLIENT\_LOG, the same environment variable applies to the server-side plugin as well as the client-side plugin.

On the server side, the permitted values are 0 (off) and 1 (on). Log messages are written to the server error log, subject to the server error-logging verbosity level. For example, if you are using prioritybased log filtering, the log\_error\_verbosity system variable controls verbosity, as described in Section 7.4.2.5, "Priority-Based Error Log Filtering (log\_filter\_internal)".

On the client side, the permitted values are from 1 to 5 and are written to the standard error output. The following table shows the meaning of each log-level value.

| Log Level    | Meaning                                         |
|--------------|-------------------------------------------------|
| 1 or not set | No logging                                      |
| 2            | Error messages                                  |
| 3            | Error and warning messages                      |
| 4            | Error, warning, and information messages        |
| 5            | Error, warning, information, and debug messages |

# <span id="page-151-0"></span>**8.4.1.9 No-Login Pluggable Authentication**

The mysql\_no\_login server-side authentication plugin prevents all client connections to any account that uses it. Use cases for this plugin include:

- Accounts that must be able to execute stored programs and views with elevated privileges without exposing those privileges to ordinary users.
- Proxied accounts that should never permit direct login but are intended to be accessed only through proxy accounts.

The following table shows the plugin and library file names. The file name suffix might differ on your system. The file must be located in the directory named by the plugin\_dir system variable.

**Table 8.24 Plugin and Library Names for No-Login Authentication**

| Plugin or File     | Plugin or File Name |
|--------------------|---------------------|
| Server-side plugin | mysql_no_login      |

| Plugin or File     | Plugin or File Name |  |
|--------------------|---------------------|--|
| Client-side plugin | None                |  |
| Library file       | mysql_no_login.so   |  |

The following sections provide installation and usage information specific to no-login pluggable authentication:

- [Installing No-Login Pluggable Authentication](#page-152-0)
- [Uninstalling No-Login Pluggable Authentication](#page-153-0)
- [Using No-Login Pluggable Authentication](#page-153-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0) For proxy user information, see [Section 8.2.19, "Proxy Users"](#page-50-0).

### <span id="page-152-0"></span>**Installing No-Login Pluggable Authentication**

This section describes how to install the no-login authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The plugin library file base name is mysql\_no\_login. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
plugin-load-add=mysql_no_login.so
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN mysql_no_login SONAME 'mysql_no_login.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%login%';
+----------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+----------------+---------------+
| mysql_no_login | ACTIVE |
+----------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the no-login plugin, see [Using No-Login Pluggable Authentication](#page-153-1).

### <span id="page-153-0"></span>**Uninstalling No-Login Pluggable Authentication**

The method used to uninstall the no-login authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN mysql_no_login;
```

### <span id="page-153-1"></span>**Using No-Login Pluggable Authentication**

This section describes how to use the no-login authentication plugin to prevent accounts from being used for connecting from MySQL client programs to the server. It is assumed that the server is running with the no-login plugin enabled, as described in [Installing No-Login Pluggable Authentication](#page-152-0).

To refer to the no-login authentication plugin in the IDENTIFIED WITH clause of a CREATE USER statement, use the name mysql\_no\_login.

An account that authenticates using mysql\_no\_login may be used as the DEFINER for stored program and view objects. If such an object definition also includes SQL SECURITY DEFINER, it executes with that account's privileges. DBAs can use this behavior to provide access to confidential or sensitive data that is exposed only through well-controlled interfaces.

The following example illustrates these principles. It defines an account that does not permit client connections, and associates with it a view that exposes only certain columns of the mysql.user system table:

```
CREATE DATABASE nologindb;
CREATE USER 'nologin'@'localhost'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL ON nologindb.*
 TO 'nologin'@'localhost';
GRANT SELECT ON mysql.user
 TO 'nologin'@'localhost';
CREATE DEFINER = 'nologin'@'localhost'
 SQL SECURITY DEFINER
 VIEW nologindb.myview
 AS SELECT User, Host FROM mysql.user;
```

To provide protected access to the view to an ordinary user, do this:

```
GRANT SELECT ON nologindb.myview
 TO 'ordinaryuser'@'localhost';
```

Now the ordinary user can use the view to access the limited information it presents:

```
SELECT * FROM nologindb.myview;
```

Attempts by the user to access columns other than those exposed by the view result in an error, as do attempts to select from the view by users not granted access to it.

![](_page_153_Picture_17.jpeg)

#### **Note**

Because the nologin account cannot be used directly, the operations required to set up objects that it uses must be performed by root or similar account that has the privileges required to create the objects and set DEFINER values.

The mysql\_no\_login plugin is also useful in proxying scenarios. (For a discussion of concepts involved in proxying, see [Section 8.2.19, "Proxy Users".](#page-50-0)) An account that authenticates using mysql\_no\_login may be used as a proxied user for proxy accounts:

```
-- create proxied account
CREATE USER 'proxied_user'@'localhost'
 IDENTIFIED WITH mysql_no_login;
-- grant privileges to proxied account
GRANT ...
 ON ...
 TO 'proxied_user'@'localhost';
-- permit proxy_user to be a proxy account for proxied account
GRANT PROXY
 ON 'proxied_user'@'localhost'
 TO 'proxy_user'@'localhost';
```

This enables clients to access MySQL through the proxy account (proxy\_user) but not to bypass the proxy mechanism by connecting directly as the proxied user (proxied\_user). A client who connects using the proxy\_user account has the privileges of the proxied\_user account, but proxied\_user itself cannot be used to connect.

For alternative methods of protecting proxied accounts against direct use, see [Preventing Direct Login](#page-53-0) [to Proxied Accounts.](#page-53-0)

# <span id="page-154-0"></span>**8.4.1.10 Socket Peer-Credential Pluggable Authentication**

The server-side auth\_socket authentication plugin authenticates clients that connect from the local host through the Unix socket file. The plugin uses the SO\_PEERCRED socket option to obtain information about the user running the client program. Thus, the plugin can be used only on systems that support the SO\_PEERCRED option, such as Linux.

The source code for this plugin can be examined as a relatively simple example demonstrating how to write a loadable authentication plugin.

The following table shows the plugin and library file names. The file must be located in the directory named by the plugin\_dir system variable.

**Table 8.25 Plugin and Library Names for Socket Peer-Credential Authentication**

| Plugin or File     | Plugin or File Name  |  |
|--------------------|----------------------|--|
| Server-side plugin | auth_socket          |  |
| Client-side plugin | None, see discussion |  |
| Library file       | auth_socket.so       |  |

The following sections provide installation and usage information specific to socket pluggable authentication:

- [Installing Socket Pluggable Authentication](#page-154-1)
- [Uninstalling Socket Pluggable Authentication](#page-155-0)
- [Using Socket Pluggable Authentication](#page-155-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-154-1"></span>**Installing Socket Pluggable Authentication**

This section describes how to install the socket authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file:

```
[mysqld]
plugin-load-add=auth_socket.so
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement:

```
INSTALL PLUGIN auth_socket SONAME 'auth_socket.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%socket%';
+-------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+-------------+---------------+
| auth_socket | ACTIVE |
+-------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the socket plugin, see [Using Socket Pluggable Authentication.](#page-155-1)

# <span id="page-155-0"></span>**Uninstalling Socket Pluggable Authentication**

The method used to uninstall the socket authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN auth_socket;
```

### <span id="page-155-1"></span>**Using Socket Pluggable Authentication**

The socket plugin checks whether the socket user name (the operating system user name) matches the MySQL user name specified by the client program to the server. If the names do not match, the plugin checks whether the socket user name matches the name specified in the authentication\_string column of the mysql.user system table row. If a match is found, the plugin permits the connection. The authentication\_string value can be specified using an IDENTIFIED ...AS clause with CREATE USER or ALTER USER.

Suppose that a MySQL account is created for an operating system user named valerie who is to be authenticated by the auth\_socket plugin for connections from the local host through the socket file:

```
CREATE USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket;
```

If a user on the local host with a login name of stefanie invokes mysql with the option - user=valerie to connect through the socket file, the server uses auth\_socket to authenticate the client. The plugin determines that the --user option value (valerie) differs from the client user's name (stephanie) and refuses the connection. If a user named valerie tries the same thing,

the plugin finds that the user name and the MySQL user name are both valerie and permits the connection. However, the plugin refuses the connection even for valerie if the connection is made using a different protocol, such as TCP/IP.

To permit both the valerie and stephanie operating system users to access MySQL through socket file connections that use the account, this can be done two ways:

• Name both users at account-creation time, one following CREATE USER, and the other in the authentication string:

```
CREATE USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket AS 'stephanie';
```

• If you have already used CREATE USER to create the account for a single user, use ALTER USER to add the second user:

```
CREATE USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket;
ALTER USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket AS 'stephanie';
```

To access the account, both valerie and stephanie specify --user=valerie at connect time.

# <span id="page-156-0"></span>**8.4.1.11 WebAuthn Pluggable Authentication**

![](_page_156_Picture_9.jpeg)

#### **Note**

WebAuthn authentication is an extension included in MySQL Enterprise Edition, a commercial product. To learn more about commercial products, see [https://](https://www.mysql.com/products/) [www.mysql.com/products/](https://www.mysql.com/products/).

MySQL Enterprise Edition supports an authentication method that enables users to authenticate to MySQL Server using WebAuthn authentication.

WebAuthn stands for Web Authentication, which is a web standard published by the World Wide Web Consortium (W3C) and web application APIs that add FIDO-based authentication to supported browsers and platforms.

WebAuthn pluggable authentication replaces FIDO pluggable authentication, which is deprecated. WebAuthn pluggable authentication supports both FIDO and FIDO2 devices.

WebAuthn pluggable authentication provides these capabilities:

- WebAuthn enables authentication to MySQL Server using devices such as smart cards, security keys, and biometric readers.
- Because authentication can occur other than by providing a password, WebAuthn enables passwordless authentication.
- On the other hand, device authentication is often used in conjunction with password authentication, so WebAuthn authentication can be used to good effect for MySQL accounts that use multifactor authentication; see [Section 8.2.18, "Multifactor Authentication"](#page-47-1).

The following table shows the plugin and library file names. The file name suffix might differ on your system. Common suffixes are .so for Unix and Unix-like systems, and .dll for Windows. The file must be located in the directory named by the plugin\_dir system variable. For installation information, see [Installing WebAuthn Pluggable Authentication](#page-157-0).

**Table 8.26 Plugin and Library Names for WebAuthn Authentication**

| Plugin or File     | Plugin or File Name            |  |
|--------------------|--------------------------------|--|
| Server-side plugin | authentication_webauthn        |  |
| Client-side plugin | authentication_webauthn_client |  |

| Plugin or File | Plugin or File Name               |
|----------------|-----------------------------------|
| Library file   | authentication_webauthn.so,       |
|                | authentication_webauthn_client.so |

![](_page_157_Picture_2.jpeg)

#### **Note**

A libfido2 library must be available on systems where either the server-side or client-side WebAuthn authentication plugin is used.

The server-side WebAuthn authentication plugin is included only in MySQL Enterprise Edition. It is not included in MySQL community distributions. The client-side plugin is included in all distributions, including community distributions, which enables clients from any distribution to connect to a server that has the server-side plugin loaded.

The following sections provide installation and usage information specific to WebAuthn pluggable authentication:

- [Installing WebAuthn Pluggable Authentication](#page-157-0)
- [Using WebAuthn Authentication](#page-158-0)
- [WebAuthn Passwordless Authentication](#page-161-0)
- [Device Unregistration for WebAuthn](#page-162-0)
- [How WebAuthn Authentication of MySQL Users Works](#page-163-1)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-157-0"></span>**Installing WebAuthn Pluggable Authentication**

This section describes how to install the server-side WebAuthn authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

The server-side plugin library file base name is authentication\_webauthn. The file name suffix differs per platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

Before installing the server-side plugin, define a unique name for the relying party ID (used for device registration and authentication), which is the MySQL server. Start the server using the - loose-authentication-webauthn-rp-id=value option. The example here specifies the value mysql.com as the relying party ID. Replace this value with one that satisfies your requirements.

\$> mysqld [options] --loose-authentication-webauthn-rp-id=mysql.com

![](_page_157_Picture_19.jpeg)

# **Note**

For replication, use the same [authentication\\_webauthn\\_rp\\_id](#page-185-2) value on all nodes if a user is expected to connect to multiple servers.

To define the relying party and load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it, adjusting the .so suffix for your platform as necessary. With this plugin-loading method, the option must be given each time the server starts.

```
$> mysqld [options] 
 --loose-authentication-webauthn-rp-id=mysql.com
 --plugin-load-add=authentication_webauthn.so
```

To define the relying party and load the plugin, put lines such as this in your my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
plugin-load-add=authentication_webauthn.so
authentication_webauthn_rp_id=mysql.com
```

After modifying my.cnf, restart the server to cause the new setting to take effect.

Alternatively, to load the plugin at runtime, use this statement, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN authentication_webauthn
 SONAME 'authentication_webauthn.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME = 'authentication_webauthn';
+-------------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+-------------------------+---------------+
| authentication_webauthn | ACTIVE |
+-------------------------+---------------+
```

If a plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the WebAuthn authentication plugin, see [Using WebAuthn](#page-158-0) [Authentication](#page-158-0).

# <span id="page-158-0"></span>**Using WebAuthn Authentication**

WebAuthn authentication typically is used in the context of multifactor authentication (see [Section 8.2.18, "Multifactor Authentication"](#page-47-1)). This section shows how to incorporate WebAuthn devicebased authentication into a multifactor account, using the authentication\_webauthn plugin.

It is assumed in the following discussion that the server is running with the server-side WebAuthn authentication plugin enabled, as described in [Installing WebAuthn Pluggable Authentication](#page-157-0), and that the client-side WebAuthn plugin is available in the plugin directory on the client host.

![](_page_158_Picture_14.jpeg)

### **Note**

On Windows, WebAuthn authentication only functions if the client process runs as a user with administrator privileges. It might also be necessary to add the location of your FIDO/FIDO2 device to the client host' PATH environment variable.

It is also assumed that WebAuthn authentication is used in conjunction with non-WebAuthn authentication (which implies a 2FA or 3FA account). WebAuthn can also be used by itself to create 1FA accounts that authenticate in a passwordless manner. In this case, the setup process differs somewhat. For instructions, see [WebAuthn Passwordless Authentication](#page-161-0).

An account that is configured to use the authentication\_webauthn plugin is associated with a Fast Identity Online (FIDO/FIDO2) device. Because of this, a one-time device registration step is required before WebAuthn authentication can occur. The device registration process has these characteristics:

- Any FIDO/FIDO2 device associated with an account must be registered before the account can be used.
- Registration requires that a FIDO/FIDO2 device be available on the client host, or registration fails.
- The user is expected to perform the appropriate FIDO/FIDO2 device action when prompted during registration (for example, touching the device or performing a biometric scan).
- To perform device registration, the client user must invoke the mysql client program and specify the --register-factor option to specify the factor or factors for which a device is being registered. For example, if the account is set to use WebAuthn as the second authentication factor, the user invokes mysql with the --register-factor=2 option.
- If the user account is configured with the authentication\_webauthn plugin set as the second or third factor, authentication for all preceding factors must succeed before the registration step can proceed.
- The server knows from the information in the user account whether the FIDO/FIDO2 device requires registration or has already been registered. When the client program connects, the server places the client session in sandbox mode if the device must be registered, so that registration must occur before anything else can be done. Sandbox mode used for FIDO/FIDO2 device registration is similar to that used for handling of expired passwords. See [Section 8.2.16, "Server Handling of Expired](#page-39-0) [Passwords"](#page-39-0).
- In sandbox mode, no statements other than ALTER USER are permitted. Registration is performed using forms of this statement. When invoked with the --register-factor option, the mysql client generates the ALTER USER statements required to perform registration. After registration has been accomplished, the server switches the session out of sandbox mode, and the client can proceed normally. For information about the generated ALTER USER statements, refer to the --registerfactor description.
- When device registration has been performed for the account, the server updates the mysql.user system table row for that account to update the device registration status and to store the public key and credential ID. (The server does not retain the credential ID following FIDO2 device registration.)
- The registration step can be performed only by the user named by the account. If one user attempts to perform registration for another user, an error occurs.
- The user should use the same FIDO/FIDO2 device during registration and authentication. If, after registering a FIDO/FIDO2 device on the client host, the device is reset or a different device is inserted, authentication fails. In this case, the device associated with the account must be unregistered and registration must be done again.

Suppose that you want an account to authenticate first using the caching\_sha2\_password plugin, then using the authentication\_webauthn plugin. Create a multifactor account using a statement like this:

```
CREATE USER 'u2'@'localhost'
 IDENTIFIED WITH caching_sha2_password
 BY 'sha2_password'
 AND IDENTIFIED WITH authentication_webauthn;
```

To connect, supply the factor 1 password to satisfy authentication for that factor, and to initiate registration of the FIDO/FIDO2 device, set the --register-factor to factor 2.

```
$> mysql --user=u2 --password1 --register-factor=2
Enter password: (enter factor 1 password)
Please insert FIDO device and follow the instruction. Depending on the device, 
you may have to perform gesture action multiple times.
1. Perform gesture action (Skip this step if you are prompted to enter device PIN).
2. Enter PIN for token device:
3. Perform gesture action for registration to complete.
Welcome to the MySQL monitor. Commands end with ; or \g.
```

```
Your MySQL connection id is 8
```

After the factor 1 password is accepted, the client session enters sandbox mode so that device registration can be performed for factor 2. During registration, you are prompted to perform the appropriate FIDO/FIDO2 device action, such as touching the device or performing a biometric scan.

After registering the device, you can authenticate to connect.

```
$> mysql --user=u2 --password1 --execute "SELECT CURRENT_USER();"
Enter password: (enter factor 1 password)
Please insert FIDO device and perform gesture action for authentication to complete.
+----------------+
| CURRENT_USER() |
+----------------+
| u2@127.0.0.1 |
+----------------+
```

When authenticating, you have the option to invoke the mysql client program and specify the - plugin-authentication-webauthn-client-preserve-privacy option.

The --plugin-authentication-webauthn-client-preserve-privacy option is suitable for the following scenarios:

- You have privacy concerns that are addressed by using this option.
- A user needs to use the same device for multiple logins on a given MySQL server.
- You want to enhance optimization by only sending the information that is necessary.

If the FIDO2 device contains multiple discoverable credentials (resident keys) for a given relying party (RP) ID, this option permits choosing a key to be used for assertion. By default, the option is set to FALSE, indicating that assertions are to be created using all resident keys for a given RP ID. When specified with this option, mysql prompts you for a device PIN and lists all of the available credentials for given RP ID. Select one key and then perform the remaining online instructions to complete the authentication. The example here assumes that mysql.com is a valid RP ID:

```
$> mysql --user=u2 --password1 --plugin-authentication-webauthn-client-preserve-privacy --execute "SELECT CURRENT_USER();"
mysql: [Warning] Using a password on the command line interface can be insecure.
2. Enter PIN for token device: 
Found following credentials for RP ID: mysql.com
[1]`u2`@`127.0.0.1`
[2]`u2`@`%`
Please select one(1...N):
1
Please insert FIDO device and perform gesture action for authentication to complete.
+----------------+
| CURRENT_USER() |
+----------------+
| u2@127.0.0.1 |
+----------------+
```

The --plugin-authentication-webauthn-client-preserve-privacy option has no effect on FIDO devices that do not support the resident-key feature.

When the registration process is complete, the connection to the server is permitted.

![](_page_160_Picture_14.jpeg)

### **Note**

The connection to the server is permitted following registration regardless of additional authentication factors in the account's authentication chain. For example, if the account in the preceding example was defined with a third authentication factor (using non-WebAuthn authentication), the connection would be permitted after a successful registration without authenticating the third factor. However, subsequent connections would require authenticating all three factors.

### <span id="page-161-0"></span>**WebAuthn Passwordless Authentication**

This section describes how WebAuthn can be used by itself to create 1FA accounts that authenticate in a passwordless manner. In this context, "passwordless" means that authentication occurs but uses a method other than a password, such as a security key or biometric scan. It does not refer to an account that uses a password-based authentication plugin for which the password is empty. That kind of "passwordless" is completely insecure and is not recommended.

The following prerequisites apply when using the authentication\_webauthn plugin to achieve passwordless authentication:

- The user that creates a passwordless-authentication account requires the PASSWORDLESS\_USER\_ADMIN privilege in addition to the CREATE USER privilege.
- The first element of the authentication\_policy value must be an asterisk (\*) and not a plugin name. For example, the default authentication\_policy value supports enabling passwordless authentication because the first element is an asterisk:

```
authentication_policy='*,,'
```

For information about configuring the authentication\_policy value, see [Configuring the](#page-48-0) [Multifactor Authentication Policy.](#page-48-0)

To use authentication\_webauthn as a passwordless authentication method, the account must be created with authentication\_webauthn as the first factor authentication method. The INITIAL AUTHENTICATION IDENTIFIED BY clause must also be specified for the first factor (it is not supported with 2nd or 3rd factors). This clause specifies whether a randomly generated or userspecified password will be used for FIDO/FIDO2 device registration. After device registration, the server deletes the password and modifies the account to make authentication\_webauthn the sole authentication method (the 1FA method).

The required CREATE USER syntax is as follows:

```
CREATE USER user
 IDENTIFIED WITH authentication_webauthn
 INITIAL AUTHENTICATION IDENTIFIED BY {RANDOM PASSWORD | 'auth_string'};
```

The following example uses the RANDOM PASSWORD syntax:

```
mysql> CREATE USER 'u1'@'localhost'
 IDENTIFIED WITH authentication_webauthn
 INITIAL AUTHENTICATION IDENTIFIED BY RANDOM PASSWORD;
+------+-----------+----------------------+-------------+
| user | host | generated password | auth_factor |
+------+-----------+----------------------+-------------+
| u1 | localhost | 9XHK]M{l2rnD;VXyHzeF | 1 |
+------+-----------+----------------------+-------------+
```

To perform registration, the user must authenticate to the server with the password associated with the INITIAL AUTHENTICATION IDENTIFIED BY clause, either the randomly generated password, or the 'auth\_string' value. If the account was created as just shown, the user executes this command and pastes in the preceding randomly generated password (9XHK]M{l2rnD;VXyHzeF) at the prompt:

```
$> mysql --user=u1 --password --register-factor=2
Enter password:
Please insert FIDO device and follow the instruction. Depending on the device, 
you may have to perform gesture action multiple times.
1. Perform gesture action (Skip this step if you are prompted to enter device PIN).
2. Enter PIN for token device:
3. Perform gesture action for registration to complete.
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 10
```

The option --register-factor=2 is used because the INITIAL AUTHENTICATION IDENTIFIED BY clause is currently acting as the first factor authentication method. The user must therefore provide

the temporary password by using the second factor. On a successful registration, the server removes the temporary password and revises the account entry in the mysql.user system table to list authentication\_webauthn as the sole (1FA) authentication method.

When creating a passwordless-authentication account, it is important to include the INITIAL AUTHENTICATION IDENTIFIED BY clause in the CREATE USER statement. The server accepts a statement without the clause, but the resulting account is unusable because there is no way to connect to the server to register the device. Suppose that you execute a statement like this:

```
CREATE USER 'u2'@'localhost'
 IDENTIFIED WITH authentication_webauthn;
```

Subsequent attempts to use the account to connect fail like this:

```
$> mysql --user=u2 --skip-password
mysql: [Warning] Using a password on the command line can be insecure.
No FIDO device on client host.
ERROR 1 (HY000): Unknown MySQL error
```

After registering the device, you can authenticate to connect.

```
$> mysql --user=u1 --password --execute "SELECT CURRENT_USER();"
Please insert FIDO device and perform gesture action for authentication to complete.
+----------------+
| CURRENT_USER() |
+----------------+
| u1@127.0.0.1 |
+----------------+
```

Alternatively, use the --plugin-authentication-webauthn-client-preserve-privacy option to select a discoverable credential for authentication.

```
$> mysql --user=u1 --password --plugin-authentication-webauthn-client-preserve-privacy --execute "SELECT CURRENT_USER();"
Enter password:
Enter PIN for token device: 
Found following credentials for RP ID: mysql.com
[1]`u1`@`127.0.0.1`
[2]`u1`@`%`
Please select one(1...N):
1
Please insert FIDO device and perform gesture action for authentication to complete.
+----------------+
| CURRENT_USER() |
+----------------+
| u1@127.0.0.1 |
+----------------+
```

![](_page_162_Picture_10.jpeg)

#### **Note**

Passwordless authentication is achieved using the Universal 2nd Factor (U2F) protocol, which does not support additional security measures such as setting a PIN on the device to be registered. It is therefore the responsibility of the device holder to ensure the device is handled in a secure manner.

### <span id="page-162-0"></span>**Device Unregistration for WebAuthn**

It is possible to unregister FIDO/FIDO2 devices associated with a MySQL account. This might be desirable or necessary under multiple circumstances:

• A FIDO/FIDO2 device is to be replaced with a different device. The previous device must be unregistered and the new device registered.

In this case, the account owner or any user who has the CREATE USER privilege can unregister the device. The account owner can register the new device.

• A FIDO/FIDO2 device is reset or lost. Authentication attempts will fail until the current device is unregistered and a new registration is performed.

In this case, the account owner, being unable to authenticate, cannot unregister the current device and must contact the DBA (or any user who has the CREATE USER privilege) to do so. Then the account owner can reregister the reset device or register a new device.

Unregistering a FIDO/FIDO2 device can be done by the account owner or by any user who has the CREATE USER privilege. Use this syntax:

```
ALTER USER user {2 | 3} FACTOR UNREGISTER;
```

To re-register a device or perform a new registration, refer to the instructions in [Using WebAuthn](#page-158-0) [Authentication](#page-158-0).

### <span id="page-163-1"></span>**How WebAuthn Authentication of MySQL Users Works**

This section provides an overview of how MySQL and WebAuthn work together to authenticate MySQL users. For examples showing how to set up MySQL accounts to use the WebAuthn authentication plugins, see [Using WebAuthn Authentication](#page-158-0).

An account that uses WebAuthn authentication must perform an initial device registration step before it can connect to the server. After the device has been registered, authentication can proceed. WebAuthn device registration process is as follows:

- 1. The server sends a random challenge, user ID, and relying party ID (which uniquely identifies a server) to the client in JSON format. The relying party ID is defined by the [authentication\\_webauthn\\_rp\\_id](#page-185-2) system variable. The default value is mysql.com.
- 2. The client receives that information and sends it to the client-side WebAuthn authentication plugin, which in turn provides it to the FIDO/FIDO2 device. Client also sends 1-byte capability, with RESIDENT\_KEYS bit set to ON (if it is FIDO2 device) or OFF.
- 3. After the user has performed the appropriate device action (for example, touching the device or performing a biometric scan) the FIDO/FIDO2 device generates a public/private key pair, a key handle, an X.509 certificate, and a signature, which is returned to the server.
- 4. The server-side WebAuthn authentication plugin verifies the signature. With successful verification, the server stores the credential ID (for FIDO devices only) and public key in the mysql.user system table.

After registration has been performed successfully, WebAuthn authentication follows this process:

- 1. The server sends a random challenge, user ID, relying party ID and credentials to the client. The challenge is converted to URL-safe Base64 format.
- 2. The client sends the same information to the device. The client queries the device to check if it supports Client-to-Authenticator Protocols (CTAP2) protocol. CTAP2 support indicates that the device is FIDO2-protocol aware.
- 3. The FIDO/FIDO2 device prompts the user to perform the appropriate device action, based on the selection made during registration.
  - If the device is FIDO2-protocol aware, the device signs with all private keys available in the device for a given RP ID. Optionally, it may prompt user to pick one from the list as well. If the device is not FIDO2 capable, it fetches the right private key.
- 4. This action unlocks the private key and the challenge is signed.
- 5. This signed challenge is returned to the server.
- 6. The server-side WebAuthn authentication plugin verifies the signature with the public key and responds to indicate authentication success or failure.

# <span id="page-163-0"></span>**8.4.1.12 Test Pluggable Authentication**

MySQL includes a test plugin that checks account credentials and logs success or failure to the server error log. This is a loadable plugin (not built in) and must be installed prior to use.

The test plugin source code is separate from the server source, unlike the built-in native plugin, so it can be examined as a relatively simple example demonstrating how to write a loadable authentication plugin.

![](_page_164_Picture_3.jpeg)

#### **Note**

This plugin is intended for testing and development purposes, and is not for use in production environments or on servers that are exposed to public networks.

The following table shows the plugin and library file names. The file name suffix might differ on your system. The file must be located in the directory named by the plugin\_dir system variable.

**Table 8.27 Plugin and Library Names for Test Authentication**

| Plugin or File<br>Plugin or File Name |                     |
|---------------------------------------|---------------------|
| Server-side plugin                    | test_plugin_server  |
| Client-side plugin                    | auth_test_plugin    |
| Library file                          | auth_test_plugin.so |

The following sections provide installation and usage information specific to test pluggable authentication:

- [Installing Test Pluggable Authentication](#page-164-0)
- [Uninstalling Test Pluggable Authentication](#page-165-1)
- [Using Test Pluggable Authentication](#page-165-2)

For general information about pluggable authentication in MySQL, see [Section 8.2.17, "Pluggable](#page-41-0) [Authentication".](#page-41-0)

### <span id="page-164-0"></span>**Installing Test Pluggable Authentication**

This section describes how to install the server-side test authentication plugin. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup.

To load the plugin at server startup, use the --plugin-load-add option to name the library file that contains it. With this plugin-loading method, the option must be given each time the server starts. For example, put these lines in the server my.cnf file, adjusting the .so suffix for your platform as necessary:

```
[mysqld]
plugin-load-add=auth_test_plugin.so
```

After modifying my.cnf, restart the server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this statement, adjusting the .so suffix for your platform as necessary:

```
INSTALL PLUGIN test_plugin_server SONAME 'auth_test_plugin.so';
```

INSTALL PLUGIN loads the plugin immediately, and also registers it in the mysql.plugins system table to cause the server to load it for each subsequent normal startup without the need for - plugin-load-add.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%test_plugin%';
+--------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+--------------------+---------------+
| test_plugin_server | ACTIVE |
+--------------------+---------------+
```

If the plugin fails to initialize, check the server error log for diagnostic messages.

To associate MySQL accounts with the test plugin, see [Using Test Pluggable Authentication.](#page-165-2)

### <span id="page-165-1"></span>**Uninstalling Test Pluggable Authentication**

The method used to uninstall the test authentication plugin depends on how you installed it:

- If you installed the plugin at server startup using a --plugin-load-add option, restart the server without the option.
- If you installed the plugin at runtime using an INSTALL PLUGIN statement, it remains installed across server restarts. To uninstall it, use UNINSTALL PLUGIN:

```
UNINSTALL PLUGIN test_plugin_server;
```

### <span id="page-165-2"></span>**Using Test Pluggable Authentication**

To use the test authentication plugin, create an account and name that plugin in the IDENTIFIED WITH clause:

```
CREATE USER 'testuser'@'localhost'
IDENTIFIED WITH test_plugin_server
BY 'testpassword';
```

The test authentication plugin also requires creating a proxy user as follows:

```
CREATE USER testpassword@localhost;
GRANT PROXY ON testpassword@localhost TO testuser@localhost;
```

Then provide the --user and --password options for that account when you connect to the server. For example:

```
$> mysql --user=testuser --password
Enter password: testpassword
```

The plugin fetches the password as received from the client and compares it with the value stored in the authentication\_string column of the account row in the mysql.user system table. If the two values match, the plugin returns the authentication\_string value as the new effective user ID.

You can look in the server error log for a message indicating whether authentication succeeded (notice that the password is reported as the "user"):

```
[Note] Plugin test_plugin_server reported:
'successfully authenticated user testpassword'
```

# <span id="page-165-0"></span>**8.4.1.13 Pluggable Authentication System Variables**

These variables are unavailable unless the appropriate server-side plugin is installed:

• authentication\_ldap\_sasl for system variables with names of the form authentication\_ldap\_sasl\_xxx

• authentication\_ldap\_simple for system variables with names of the form authentication\_ldap\_simple\_xxx

**Table 8.28 Authentication Plugin System Variable Summary**

| Name                      | Cmd-Line                                              | Option File | System Var | Status Var | Var Scope | Dynamic |
|---------------------------|-------------------------------------------------------|-------------|------------|------------|-----------|---------|
|                           | authentication_kerberos_service_key_tab<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                           | authentication_kerberos_service_principal<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_auth_method_name<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_bind_base_dn<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_bind_root_dn<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_bind_root_pwd<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_ca_path<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_connect_timeout<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_group_search_attr<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_group_search_filter<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_init_pool_size<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_log_status<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_max_pool_size<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_referral<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_response_timeout<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_server_host<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_server_port<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_tls<br>Yes                   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_sasl_user_search_attr<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_auth_method_name<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_bind_base_dn<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_bind_root_dn<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_bind_root_pwd<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_ca_path<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_connect_timeout<br>Yes     | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_group_search_attr<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_group_search_filter<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_init_pool_size<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_log_status<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_max_pool_size<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_referral<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_response_timeout<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_server_host<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_server_port<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_tls<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_ldap_simple_user_search_attr<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
| authentication_policy Yes |                                                       | Yes         | Yes        |            | Global    | Yes     |
|                           | authentication_webauthn_rp_id<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |

| Name | Cmd-Line                                | Option File                                      | System Var | Status Var | Var Scope | Dynamic |
|------|-----------------------------------------|--------------------------------------------------|------------|------------|-----------|---------|
|      | authentication_windows_log_level<br>Yes | Yes                                              | Yes        |            | Global    | No      |
|      | Yes                                     | authentication_windows_use_principal_name<br>Yes | Yes        |            | Global    | No      |

<span id="page-167-1"></span>• [authentication\\_kerberos\\_service\\_key\\_tab](#page-167-1)

| Command-Line Format  | authentication-kerberos-service<br>key-tab=file_name |  |
|----------------------|------------------------------------------------------|--|
| System Variable      | authentication_kerberos_service_key_tab              |  |
| Scope                | Global                                               |  |
| Dynamic              | No                                                   |  |
| SET_VAR Hint Applies | No                                                   |  |
| Type                 | File name                                            |  |
| Default Value        | datadir/mysql.keytab                                 |  |

The name of the server-side key-table ("keytab") file containing Kerberos service keys to authenticate MySQL service tickets received from clients. The file name should be given as an absolute path name. If this variable is not set, the default is mysql.keytab in the data directory.

The file must exist and contain a valid key for the service principal name (SPN) or authentication of clients will fail. (The SPN and same key also must be created in the Kerberos server.) The file may contain multiple service principal names and their respective key combinations.

The file must be generated by the Kerberos server administrator and be copied to a location accessible by the MySQL server. The file can be validated to make sure that it is correct and was copied properly using this command:

klist -k file\_name

For information about keytab files, see [https://web.mit.edu/kerberos/krb5-latest/doc/basic/](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md) [keytab\\_def.html.](https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.md)

<span id="page-167-0"></span>• [authentication\\_kerberos\\_service\\_principal](#page-167-0)

| Command-Line Format  | authentication-kerberos-service<br>principal=name |
|----------------------|---------------------------------------------------|
| System Variable      | authentication_kerberos_service_principal         |
| Scope                | Global                                            |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | String                                            |
| Default Value        | mysql/host_name@realm_name                        |

The Kerberos service principal name (SPN) that the MySQL server sends to clients.

The value is composed from the service name (mysql), a host name, and a realm name. The default value is mysql/host\_name@realm\_name. The realm in the service principal name enables retrieving the exact service key.

To use a nondefault value, set the value using the same format. For example, to use a host name of krbauth.example.com and a realm of MYSQL.LOCAL, set [authentication\\_kerberos\\_service\\_principal](#page-167-0) to mysql/ krbauth.example.com@MYSQL.LOCAL.

The service principal name and service key must already be present in the database managed by the KDC server.

There can be service principal names that differ only by realm name.

<span id="page-168-0"></span>• [authentication\\_ldap\\_sasl\\_auth\\_method\\_name](#page-168-0)

| Command-Line Format  | authentication-ldap-sasl-auth<br>method-name=value |
|----------------------|----------------------------------------------------|
| System Variable      | authentication_ldap_sasl_auth_method_name          |
| Scope                | Global                                             |
| Dynamic              | Yes                                                |
| SET_VAR Hint Applies | No                                                 |
| Type                 | String                                             |
| Default Value        | SCRAM-SHA-1                                        |
| Valid Values         | SCRAM-SHA-1                                        |
|                      | SCRAM-SHA-256                                      |
|                      | GSSAPI                                             |

For SASL LDAP authentication, the authentication method name. Communication between the authentication plugin and the LDAP server occurs according to this authentication method to ensure password security.

These authentication method values are permitted:

• SCRAM-SHA-1: Use a SASL challenge-response mechanism.

The client-side authentication\_ldap\_sasl\_client plugin communicates with the SASL server, using the password to create a challenge and obtain a SASL request buffer, then passes this buffer to the server-side authentication\_ldap\_sasl plugin. The client-side and serverside SASL LDAP plugins use SASL messages for secure transmission of credentials within the LDAP protocol, to avoid sending the cleartext password between the MySQL client and server.

• SCRAM-SHA-256: Use a SASL challenge-response mechanism.

This method is similar to SCRAM-SHA-1, but is more secure. It requires an OpenLDAP server built using Cyrus SASL 2.1.27 or higher.

• GSSAPI: Use Kerberos, a passwordless and ticket-based protocol.

GSSAPI/Kerberos is supported as an authentication method for MySQL clients and servers only on Linux. It is useful in Linux environments where applications access LDAP using Microsoft Active Directory, which has Kerberos enabled by default.

The client-side authentication\_ldap\_sasl\_client plugin obtains a service ticket using the ticket-granting ticket (TGT) from Kerberos, but does not use LDAP services directly. The serverside authentication\_ldap\_sasl plugin routes Kerberos messages between the client-side plugin and the LDAP server. Using the credentials thus obtained, the server-side plugin then communicates with the LDAP server to interpret LDAP authentication messages and retrieve LDAP groups.

<span id="page-169-1"></span>• [authentication\\_ldap\\_sasl\\_bind\\_base\\_dn](#page-169-1)

| Command-Line Format  | authentication-ldap-sasl-bind<br>base-dn=value |
|----------------------|------------------------------------------------|
| System Variable      | authentication_ldap_sasl_bind_base_dn          |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | String                                         |
| Default Value        | NULL                                           |

For SASL LDAP authentication, the base distinguished name (DN). This variable can be used to limit the scope of searches by anchoring them at a certain location (the "base") within the search tree.

Suppose that members of one set of LDAP user entries each have this form:

```
uid=user_name,ou=People,dc=example,dc=com
```

And that members of another set of LDAP user entries each have this form:

```
uid=user_name,ou=Admin,dc=example,dc=com
```

Then searches work like this for different base DN values:

- If the base DN is ou=People,dc=example,dc=com: Searches find user entries only in the first set.
- If the base DN is ou=Admin,dc=example,dc=com: Searches find user entries only in the second set.
- If the base DN is ou=dc=example,dc=com: Searches find user entries in the first or second set.

In general, more specific base DN values result in faster searches because they limit the search scope more.

<span id="page-169-0"></span>• [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-169-0)

| Command-Line Format  | authentication-ldap-sasl-bind<br>root-dn=value |
|----------------------|------------------------------------------------|
| System Variable      | authentication_ldap_sasl_bind_root_dn          |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | String                                         |
| Default Value        | NULL                                           |

For SASL LDAP authentication, the root distinguished name (DN). This variable is used in conjunction with [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-170-2) as the credentials for authenticating to the LDAP server for the purpose of performing searches. Authentication uses either one or two LDAP bind operations, depending on whether the MySQL account names an LDAP user DN:

• If the account does not name a user DN: authentication\_ldap\_sasl performs an initial LDAP binding using [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-169-0) and [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-170-2). (These are both empty by default, so if they are not set, the LDAP server must permit anonymous connections.) The resulting bind LDAP handle is used to search for the user DN, based on the client user name. authentication\_ldap\_sasl performs a second bind using the user DN and client-supplied password.

- If the account does name a user DN: The first bind operation is unnecessary in this case. authentication\_ldap\_sasl performs a single bind using the user DN and client-supplied password. This is faster than if the MySQL account does not specify an LDAP user DN.
- <span id="page-170-2"></span>• [authentication\\_ldap\\_sasl\\_bind\\_root\\_pwd](#page-170-2)

| authentication-ldap-sasl-bind<br>root-pwd=value |
|-------------------------------------------------|
| authentication_ldap_sasl_bind_root_pwd          |
| Global                                          |
| Yes                                             |
| No                                              |
| String                                          |
| NULL                                            |
|                                                 |

For SASL LDAP authentication, the password for the root distinguished name. This variable is used in conjunction with [authentication\\_ldap\\_sasl\\_bind\\_root\\_dn](#page-169-0). See the description of that variable.

<span id="page-170-0"></span>• [authentication\\_ldap\\_sasl\\_ca\\_path](#page-170-0)

| Command-Line Format  | authentication-ldap-sasl-ca<br>path=value |
|----------------------|-------------------------------------------|
| System Variable      | authentication_ldap_sasl_ca_path          |
| Scope                | Global                                    |
| Dynamic              | Yes                                       |
| SET_VAR Hint Applies | No                                        |
| Type                 | String                                    |
| Default Value        | NULL                                      |

For SASL LDAP authentication, the absolute path of the certificate authority file. Specify this file if it is desired that the authentication plugin perform verification of the LDAP server certificate.

![](_page_170_Picture_9.jpeg)

### **Note**

In addition to setting the [authentication\\_ldap\\_sasl\\_ca\\_path](#page-170-0) variable to the file name, you must add the appropriate certificate authority certificates to the file and enable the [authentication\\_ldap\\_sasl\\_tls](#page-175-0) system variable. These variables can be set to override the default OpenLDAP TLS configuration; see [LDAP Pluggable Authentication and ldap.conf](#page-125-0)

<span id="page-170-1"></span>• [authentication\\_ldap\\_sasl\\_connect\\_timeout](#page-170-1)

| Command-Line Format | authentication-ldap-sasl-connect<br>timeout=# |
|---------------------|-----------------------------------------------|
| System Variable     | authentication_ldap_sasl_connect_timeout      |
| Scope               | Global                                        |
| Dynamic             | Yes<br>1341                                   |

| SET_VAR Hint Applies | No       |
|----------------------|----------|
| Type                 | Integer  |
| Default Value        | 30       |
| Minimum Value        | 0        |
| Maximum Value        | 31536000 |
| Unit                 | seconds  |

Specifies the time (in seconds) that MySQL server waits to connect to the LDAP server using TCP.

When a MySQL account authenticates using LDAP, MySQL server attempts to establish a TCP connection with the LDAP server, which it uses to send an LDAP bind request over the connection. If the LDAP server does not respond to TCP handshake after a configured amount of time, MySQL abandons the TCP handshake attempt and emits an error message. If the timeout setting is zero, MySQL server ignores this system variable setting. For more information, see [Setting Timeouts for](#page-125-1) [LDAP Pluggable Authentication.](#page-125-1)

![](_page_171_Picture_4.jpeg)

#### **Note**

If you set this variable to a timeout value that is greater than the host system's default value, the shorter system timeout is used.

<span id="page-171-0"></span>• [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-171-0)

| Command-Line Format  | authentication-ldap-sasl-group<br>search-attr=value |  |
|----------------------|-----------------------------------------------------|--|
| System Variable      | authentication_ldap_sasl_group_search_attr          |  |
| Scope                | Global                                              |  |
| Dynamic              | Yes                                                 |  |
| SET_VAR Hint Applies | No                                                  |  |
| Type                 | String                                              |  |
| Default Value        | cn                                                  |  |

For SASL LDAP authentication, the name of the attribute that specifies group names in LDAP directory entries. If [authentication\\_ldap\\_sasl\\_group\\_search\\_attr](#page-171-0) has its default value of cn, searches return the cn value as the group name. For example, if an LDAP entry with a uid value of user1 has a cn attribute of mygroup, searches for user1 return mygroup as the group name.

This variable should be the empty string if you want no group or proxy authentication.

If the group search attribute is isMemberOf, LDAP authentication directly retrieves the user attribute isMemberOf value and assigns it as group information. If the group search attribute is not isMemberOf, LDAP authentication searches for all groups where the user is a member. (The latter is the default behavior.) This behavior is based on how LDAP group information can be stored two ways: 1) A group entry can have an attribute named memberUid or member with a value that is a user name; 2) A user entry can have an attribute named isMemberOf with values that are group names.

<span id="page-171-1"></span>• [authentication\\_ldap\\_sasl\\_group\\_search\\_filter](#page-171-1)

| Command-Line Format | authentication-ldap-sasl-group<br>search-filter=value |  |
|---------------------|-------------------------------------------------------|--|
| System Variable     | authentication_ldap_sasl_group_search_filter          |  |
| Scope               | Global                                                |  |

| Dynamic              | Yes                                                                                   |
|----------------------|---------------------------------------------------------------------------------------|
| SET_VAR Hint Applies | No                                                                                    |
| Type                 | String                                                                                |
| Default Value        | ( (&(objectClass=posixGroup)<br>(memberUid=%s))(&(objectClass=group)<br>(member=%s))) |

For SASL LDAP authentication, the custom group search filter.

The search filter value can contain {UA} and {UD} notation to represent the user name and the full user DN. For example, {UA} is replaced with a user name such as "admin", whereas {UD} is replaced with a use full DN such as "uid=admin,ou=People,dc=example,dc=com". The following value is the default, which supports both OpenLDAP and Active Directory:

```
(|(&(objectClass=posixGroup)(memberUid={UA}))
 (&(objectClass=group)(member={UD})))
```

In some cases for the user scenario, memberOf is a simple user attribute that holds no group information. For additional flexibility, an optional {GA} prefix can be used with the group search attribute. Any group attribute with a {GA} prefix is treated as a user attribute having group names. For example, with a value of {GA}MemberOf, if the group value is the DN, the first attribute value from the group DN is returned as the group name.

<span id="page-172-0"></span>• [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-172-0)

| Command-Line Format  | authentication-ldap-sasl-init<br>pool-size=# |
|----------------------|----------------------------------------------|
| System Variable      | authentication_ldap_sasl_init_pool_size      |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Integer                                      |
| Default Value        | 10                                           |
| Minimum Value        | 0                                            |
| Maximum Value        | 32767                                        |
| Unit                 | connections                                  |

For SASL LDAP authentication, the initial size of the pool of connections to the LDAP server. Choose the value for this variable based on the average number of concurrent authentication requests to the LDAP server.

The plugin uses [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-172-0) and [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-173-0) together for connection-pool management:

- When the authentication plugin initializes, it creates [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-172-0) connections, unless [authentication\\_ldap\\_sasl\\_max\\_pool\\_size=0](#page-173-0) to disable pooling.
- If the plugin receives an authentication request when there are no free connections in the current connection pool, the plugin can create a new connection, up to the maximum connection pool size given by [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-173-0).
- If the plugin receives a request when the pool size is already at its maximum and there are no free connections, authentication fails.

• When the plugin unloads, it closes all pooled connections.

Changes to plugin system variable settings may have no effect on connections already in the pool. For example, modifying the LDAP server host, port, or TLS settings does not affect existing connections. However, if the original variable values were invalid and the connection pool could not be initialized, the plugin attempts to reinitialize the pool for the next LDAP request. In this case, the new system variable values are used for the reinitialization attempt.

If [authentication\\_ldap\\_sasl\\_max\\_pool\\_size=0](#page-173-0) to disable pooling, each LDAP connection opened by the plugin uses the values the system variables have at that time.

<span id="page-173-1"></span>• [authentication\\_ldap\\_sasl\\_log\\_status](#page-173-1)

| Command-Line Format  | authentication-ldap-sasl-log<br>status=# |
|----------------------|------------------------------------------|
| System Variable      | authentication_ldap_sasl_log_status      |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | Integer                                  |
| Default Value        | 1                                        |
| Minimum Value        | 1                                        |
| Maximum Value        | 6                                        |

For SASL LDAP authentication, the logging level for messages written to the error log. The following table shows the permitted level values and their meanings.

**Table 8.29 Log Levels for authentication\_ldap\_sasl\_log\_status**

| Option Value | Types of Messages Logged                                            |
|--------------|---------------------------------------------------------------------|
| 1            | No messages                                                         |
| 2            | Error messages                                                      |
| 3            | Error and warning messages                                          |
| 4            | Error, warning, and information messages                            |
| 5            | Same as previous level plus debugging<br>messages from MySQL        |
| 6            | Same as previous level plus debugging<br>messages from LDAP library |

On the client side, messages can be logged to the standard output by setting the AUTHENTICATION\_LDAP\_CLIENT\_LOG environment variable. The permitted and default values are the same as for [authentication\\_ldap\\_sasl\\_log\\_status](#page-173-1).

The AUTHENTICATION\_LDAP\_CLIENT\_LOG environment variable applies only to SASL LDAP authentication. It has no effect for simple LDAP authentication because the client plugin in that case is mysql\_clear\_password, which knows nothing about LDAP operations.

<span id="page-173-0"></span>• [authentication\\_ldap\\_sasl\\_max\\_pool\\_size](#page-173-0)

| Command-Line Format | authentication-ldap-sasl-max-pool |
|---------------------|-----------------------------------|
|                     | size=#                            |

| System Variable      | authentication_ldap_sasl_max_pool_size |
|----------------------|----------------------------------------|
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Integer                                |
| Default Value        | 1000                                   |
| Minimum Value        | 0                                      |
| Maximum Value        | 32767                                  |
| Unit                 | connections                            |

For SASL LDAP authentication, the maximum size of the pool of connections to the LDAP server. To disable connection pooling, set this variable to 0.

This variable is used in conjunction with [authentication\\_ldap\\_sasl\\_init\\_pool\\_size](#page-172-0). See the description of that variable.

<span id="page-174-1"></span>• [authentication\\_ldap\\_sasl\\_referral](#page-174-1)

| Command-Line Format  | authentication-ldap-sasl<br>referral[={OFF ON}] |
|----------------------|-------------------------------------------------|
| System Variable      | authentication_ldap_sasl_referral               |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Boolean                                         |
| Default Value        | OFF                                             |

For SASL LDAP authentication, whether to enable LDAP search referral. See [LDAP Search Referral.](#page-139-0)

This variable can be set to override the default OpenLDAP referral configuration; see [LDAP](#page-125-0) [Pluggable Authentication and ldap.conf](#page-125-0)

<span id="page-174-0"></span>• [authentication\\_ldap\\_sasl\\_response\\_timeout](#page-174-0)

| Command-Line Format  | authentication-ldap-sasl-response<br>timeout=# |
|----------------------|------------------------------------------------|
| System Variable      | authentication_ldap_sasl_response_timeout      |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | Integer                                        |
| Default Value        | 30                                             |
| Minimum Value        | 0                                              |
| Maximum Value        | 31536000                                       |

| Unit<br>seconds |  |
|-----------------|--|
|-----------------|--|

Specifies the time (in seconds) that MySQL server waits for the LDAP server to response to an LDAP bind request.

When a MySQL account authenticates using LDAP, MySQL server sends an LDAP bind request to the LDAP server. If the LDAP server does not respond to the request after a configured amount of time, MySQL abandons the request and emits an error message. If the timeout setting is zero, MySQL server ignores this system variable setting. For more information, see [Setting Timeouts for](#page-125-1) [LDAP Pluggable Authentication.](#page-125-1)

<span id="page-175-1"></span>• [authentication\\_ldap\\_sasl\\_server\\_host](#page-175-1)

| Command-Line Format  | authentication-ldap-sasl-server<br>host=host_name |
|----------------------|---------------------------------------------------|
| System Variable      | authentication_ldap_sasl_server_host              |
| Scope                | Global                                            |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | String                                            |

The LDAP server host for SASL LDAP authentication; this can be a host name or IP address.

<span id="page-175-2"></span>• [authentication\\_ldap\\_sasl\\_server\\_port](#page-175-2)

| Command-Line Format  | authentication-ldap-sasl-server<br>port=port_num |
|----------------------|--------------------------------------------------|
| System Variable      | authentication_ldap_sasl_server_port             |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | Integer                                          |
| Default Value        | 389                                              |
| Minimum Value        | 1                                                |
| Maximum Value        | 32376                                            |

For SASL LDAP authentication, the LDAP server TCP/IP port number.

If the LDAP port number is configured as 636 or 3269, the plugin uses LDAPS (LDAP over SSL) instead of LDAP. (LDAPS differs from startTLS.)

<span id="page-175-0"></span>• [authentication\\_ldap\\_sasl\\_tls](#page-175-0)

| Command-Line Format  | authentication-ldap-sasl<br>tls[={OFF ON}] |
|----------------------|--------------------------------------------|
| System Variable      | authentication_ldap_sasl_tls               |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Boolean                                    |

| Default Value | OFF |  |
|---------------|-----|--|
|---------------|-----|--|

For SASL LDAP authentication, whether connections by the plugin to the LDAP server are secure. If this variable is enabled, the plugin uses TLS to connect securely to the LDAP server. This variable can be set to override the default OpenLDAP TLS configuration; see [LDAP](#page-125-0) [Pluggable Authentication and ldap.conf](#page-125-0) If you enable this variable, you may also wish to set the [authentication\\_ldap\\_sasl\\_ca\\_path](#page-170-0) variable.

MySQL LDAP plugins support the StartTLS method, which initializes TLS on top of a plain LDAP connection.

LDAPS can be used by setting the [authentication\\_ldap\\_sasl\\_server\\_port](#page-175-2) system variable.

<span id="page-176-0"></span>• [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-176-0)

| Command-Line Format  | authentication-ldap-sasl-user<br>search-attr=value |
|----------------------|----------------------------------------------------|
| System Variable      | authentication_ldap_sasl_user_search_attr          |
| Scope                | Global                                             |
| Dynamic              | Yes                                                |
| SET_VAR Hint Applies | No                                                 |
| Type                 | String                                             |
| Default Value        | uid                                                |

For SASL LDAP authentication, the name of the attribute that specifies user names in LDAP directory entries. If a user distinguished name is not provided, the authentication plugin searches for the name using this attribute. For example, if the [authentication\\_ldap\\_sasl\\_user\\_search\\_attr](#page-176-0) value is uid, a search for the user name user1 finds entries with a uid value of user1.

<span id="page-176-1"></span>• [authentication\\_ldap\\_simple\\_auth\\_method\\_name](#page-176-1)

| Command-Line Format  | authentication-ldap-simple-auth<br>method-name=value |
|----------------------|------------------------------------------------------|
| System Variable      | authentication_ldap_simple_auth_method_name          |
| Scope                | Global                                               |
| Dynamic              | Yes                                                  |
| SET_VAR Hint Applies | No                                                   |
| Type                 | String                                               |
| Default Value        | SIMPLE                                               |
| Valid Values         | SIMPLE                                               |

AD-FOREST

For simple LDAP authentication, the authentication method name. Communication between the authentication plugin and the LDAP server occurs according to this authentication method.

![](_page_177_Picture_3.jpeg)

#### **Note**

For all simple LDAP authentication methods, it is recommended to also set TLS parameters to require that communication with the LDAP server take place over secure connections.

These authentication method values are permitted:

- SIMPLE: Use simple LDAP authentication. This method uses either one or two LDAP bind operations, depending on whether the MySQL account names an LDAP user distinguished name. See the description of [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-178-1).
- AD-FOREST: A variation on SIMPLE, such that authentication searches all domains in the Active Directory forest, performing an LDAP bind to each Active Directory domain until the user is found in some domain.
- <span id="page-177-0"></span>• [authentication\\_ldap\\_simple\\_bind\\_base\\_dn](#page-177-0)

| Command-Line Format  | authentication-ldap-simple-bind<br>base-dn=value |
|----------------------|--------------------------------------------------|
| System Variable      | authentication_ldap_simple_bind_base_dn          |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | String                                           |
| Default Value        | NULL                                             |

For simple LDAP authentication, the base distinguished name (DN). This variable can be used to limit the scope of searches by anchoring them at a certain location (the "base") within the search tree.

Suppose that members of one set of LDAP user entries each have this form:

uid=user\_name,ou=People,dc=example,dc=com

And that members of another set of LDAP user entries each have this form:

uid=user\_name,ou=Admin,dc=example,dc=com

Then searches work like this for different base DN values:

- If the base DN is ou=People,dc=example,dc=com: Searches find user entries only in the first set.
- If the base DN is ou=Admin,dc=example,dc=com: Searches find user entries only in the second set.
- If the base DN is ou=dc=example,dc=com: Searches find user entries in the first or second set.

In general, more specific base DN values result in faster searches because they limit the search scope more.

<span id="page-178-1"></span>• [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-178-1)

| Command-Line Format  | authentication-ldap-simple-bind<br>root-dn=value |
|----------------------|--------------------------------------------------|
| System Variable      | authentication_ldap_simple_bind_root_dn          |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | String                                           |
| Default Value        | NULL                                             |

For simple LDAP authentication, the root distinguished name (DN). This variable is used in conjunction with [authentication\\_ldap\\_simple\\_bind\\_root\\_pwd](#page-178-2) as the credentials for authenticating to the LDAP server for the purpose of performing searches. Authentication uses either one or two LDAP bind operations, depending on whether the MySQL account names an LDAP user DN:

- If the account does not name a user DN: authentication\_ldap\_simple performs an initial LDAP binding using [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-178-1) and [authentication\\_ldap\\_simple\\_bind\\_root\\_pwd](#page-178-2). (These are both empty by default, so if they are not set, the LDAP server must permit anonymous connections.) The resulting bind LDAP handle is used to search for the user DN, based on the client user name. authentication\_ldap\_simple performs a second bind using the user DN and client-supplied password.
- If the account does name a user DN: The first bind operation is unnecessary in this case. authentication\_ldap\_simple performs a single bind using the user DN and client-supplied password. This is faster than if the MySQL account does not specify an LDAP user DN.
- <span id="page-178-2"></span>• [authentication\\_ldap\\_simple\\_bind\\_root\\_pwd](#page-178-2)

| Command-Line Format  | authentication-ldap-simple-bind<br>root-pwd=value |  |
|----------------------|---------------------------------------------------|--|
| System Variable      | authentication_ldap_simple_bind_root_pwd          |  |
| Scope                | Global                                            |  |
| Dynamic              | Yes                                               |  |
| SET_VAR Hint Applies | No                                                |  |
| Type                 | String                                            |  |
| Default Value        | NULL                                              |  |

For simple LDAP authentication, the password for the root distinguished name. This variable is used in conjunction with [authentication\\_ldap\\_simple\\_bind\\_root\\_dn](#page-178-1). See the description of that variable.

<span id="page-178-0"></span>• [authentication\\_ldap\\_simple\\_ca\\_path](#page-178-0)

| Command-Line Format  | authentication-ldap-simple-ca<br>path=value |
|----------------------|---------------------------------------------|
| System Variable      | authentication_ldap_simple_ca_path          |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |

| Type          | String |
|---------------|--------|
| Default Value | NULL   |

For simple LDAP authentication, the absolute path of the certificate authority file. Specify this file if it is desired that the authentication plugin perform verification of the LDAP server certificate.

![](_page_179_Picture_3.jpeg)

### **Note**

In addition to setting the [authentication\\_ldap\\_simple\\_ca\\_path](#page-178-0) variable to the file name, you must add the appropriate certificate authority certificates to the file and enable the [authentication\\_ldap\\_simple\\_tls](#page-185-0) system variable. These variables can be set to override the default OpenLDAP TLS configuration; see [LDAP Pluggable Authentication and](#page-125-0) [ldap.conf](#page-125-0)

<span id="page-179-0"></span>• [authentication\\_ldap\\_simple\\_connect\\_timeout](#page-179-0)

| Command-Line Format  | authentication-ldap-simple<br>connect-timeout=# |
|----------------------|-------------------------------------------------|
| System Variable      | authentication_ldap_simple_connect_timeout      |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Integer                                         |
| Default Value        | 30                                              |
| Minimum Value        | 0                                               |
| Maximum Value        | 31536000                                        |
| Unit                 | seconds                                         |

Specifies the time (in seconds) that MySQL server waits to connect to the LDAP server using TCP.

When a MySQL account authenticates using LDAP, MySQL server attempts to establish a TCP connection with the LDAP server, which it uses to send an LDAP bind request over the connection. If the LDAP server does not respond to TCP handshake after a configured amount of time, MySQL abandons the TCP handshake attempt and emits an error message. If the timeout setting is zero, MySQL server ignores this system variable setting. For more information, see [Setting Timeouts for](#page-125-1) [LDAP Pluggable Authentication.](#page-125-1)

![](_page_179_Picture_10.jpeg)

#### **Note**

If you set this variable to a timeout value that is greater than the host system's default value, the shorter system timeout is used.

<span id="page-179-1"></span>• [authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-179-1)

| Command-Line Format  | authentication-ldap-simple-group<br>search-attr=value |  |
|----------------------|-------------------------------------------------------|--|
| System Variable      | authentication_ldap_simple_group_search_attr          |  |
| Scope                | Global                                                |  |
| Dynamic              | Yes                                                   |  |
| SET_VAR Hint Applies | No                                                    |  |
| Type                 | String                                                |  |
| Default Value        | cn                                                    |  |

For simple LDAP authentication, the name of the attribute that specifies group names in LDAP directory entries. If [authentication\\_ldap\\_simple\\_group\\_search\\_attr](#page-179-1) has its default value of cn, searches return the cn value as the group name. For example, if an LDAP entry with a uid value of user1 has a cn attribute of mygroup, searches for user1 return mygroup as the group name.

If the group search attribute is isMemberOf, LDAP authentication directly retrieves the user attribute isMemberOf value and assigns it as group information. If the group search attribute is not isMemberOf, LDAP authentication searches for all groups where the user is a member. (The latter is the default behavior.) This behavior is based on how LDAP group information can be stored two ways: 1) A group entry can have an attribute named memberUid or member with a value that is a user name; 2) A user entry can have an attribute named isMemberOf with values that are group names.

<span id="page-180-0"></span>• [authentication\\_ldap\\_simple\\_group\\_search\\_filter](#page-180-0)

| Command-Line Format  | authentication-ldap-simple-group<br>search-filter=value                               |
|----------------------|---------------------------------------------------------------------------------------|
| System Variable      | authentication_ldap_simple_group_search_filter                                        |
| Scope                | Global                                                                                |
| Dynamic              | Yes                                                                                   |
| SET_VAR Hint Applies | No                                                                                    |
| Type                 | String                                                                                |
| Default Value        | ( (&(objectClass=posixGroup)<br>(memberUid=%s))(&(objectClass=group)<br>(member=%s))) |

For simple LDAP authentication, the custom group search filter.

The search filter value can contain {UA} and {UD} notation to represent the user name and the full user DN. For example, {UA} is replaced with a user name such as "admin", whereas {UD} is replaced with a use full DN such as "uid=admin,ou=People,dc=example,dc=com". The following value is the default, which supports both OpenLDAP and Active Directory:

```
(|(&(objectClass=posixGroup)(memberUid={UA}))
 (&(objectClass=group)(member={UD})))
```

In some cases for the user scenario, memberOf is a simple user attribute that holds no group information. For additional flexibility, an optional {GA} prefix can be used with the group search attribute. Any group attribute with a {GA} prefix is treated as a user attribute having group names. For example, with a value of {GA}MemberOf, if the group value is the DN, the first attribute value from the group DN is returned as the group name.

<span id="page-180-1"></span>• [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-180-1)

| Command-Line Format  | authentication-ldap-simple-init<br>pool-size=# |  |
|----------------------|------------------------------------------------|--|
| System Variable      | authentication_ldap_simple_init_pool_size      |  |
| Scope                | Global                                         |  |
| Dynamic              | Yes                                            |  |
| SET_VAR Hint Applies | No                                             |  |
| Type                 | Integer                                        |  |
| Default Value        | 10                                             |  |

| Maximum Value | 32767       |
|---------------|-------------|
| Unit          | connections |

For simple LDAP authentication, the initial size of the pool of connections to the LDAP server. Choose the value for this variable based on the average number of concurrent authentication requests to the LDAP server.

The plugin uses [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-180-1) and [authentication\\_ldap\\_simple\\_max\\_pool\\_size](#page-182-2) together for connection-pool management:

- When the authentication plugin initializes, it creates [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-180-1) connections, unless [authentication\\_ldap\\_simple\\_max\\_pool\\_size=0](#page-182-2) to disable pooling.
- If the plugin receives an authentication request when there are no free connections in the current connection pool, the plugin can create a new connection, up to the maximum connection pool size given by [authentication\\_ldap\\_simple\\_max\\_pool\\_size](#page-182-2).
- If the plugin receives a request when the pool size is already at its maximum and there are no free connections, authentication fails.
- When the plugin unloads, it closes all pooled connections.

Changes to plugin system variable settings may have no effect on connections already in the pool. For example, modifying the LDAP server host, port, or TLS settings does not affect existing connections. However, if the original variable values were invalid and the connection pool could not be initialized, the plugin attempts to reinitialize the pool for the next LDAP request. In this case, the new system variable values are used for the reinitialization attempt.

If [authentication\\_ldap\\_simple\\_max\\_pool\\_size=0](#page-182-2) to disable pooling, each LDAP connection opened by the plugin uses the values the system variables have at that time.

<span id="page-181-0"></span>• [authentication\\_ldap\\_simple\\_log\\_status](#page-181-0)

| Command-Line Format  | authentication-ldap-simple-log<br>status=# |
|----------------------|--------------------------------------------|
| System Variable      | authentication_ldap_simple_log_status      |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 1                                          |
| Minimum Value        | 1                                          |
| Maximum Value        | 6                                          |

For simple LDAP authentication, the logging level for messages written to the error log. The following table shows the permitted level values and their meanings.

**Table 8.30 Log Levels for authentication\_ldap\_simple\_log\_status**

|      | Option Value | Types of Messages Logged |
|------|--------------|--------------------------|
|      | 1            | No messages              |
| 1352 | 2            | Error messages           |

| Option Value | Types of Messages Logged                                            |
|--------------|---------------------------------------------------------------------|
| 3            | Error and warning messages                                          |
| 4            | Error, warning, and information messages                            |
| 5            | Same as previous level plus debugging<br>messages from MySQL        |
| 6            | Same as previous level plus debugging<br>messages from LDAP library |

#### <span id="page-182-2"></span>• [authentication\\_ldap\\_simple\\_max\\_pool\\_size](#page-182-2)

| Command-Line Format  | authentication-ldap-simple-max<br>pool-size=# |
|----------------------|-----------------------------------------------|
| System Variable      | authentication_ldap_simple_max_pool_size      |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Integer                                       |
| Default Value        | 1000                                          |
| Minimum Value        | 0                                             |
| Maximum Value        | 32767                                         |
| Unit                 | connections                                   |

For simple LDAP authentication, the maximum size of the pool of connections to the LDAP server. To disable connection pooling, set this variable to 0.

This variable is used in conjunction with [authentication\\_ldap\\_simple\\_init\\_pool\\_size](#page-180-1). See the description of that variable.

# <span id="page-182-1"></span>• [authentication\\_ldap\\_simple\\_referral](#page-182-1)

| Command-Line Format  | authentication-ldap-simple<br>referral[={OFF ON}] |
|----------------------|---------------------------------------------------|
| System Variable      | authentication_ldap_simple_referral               |
| Scope                | Global                                            |
| Dynamic              | Yes                                               |
| SET_VAR Hint Applies | No                                                |
| Type                 | Boolean                                           |
| Default Value        | OFF                                               |

For simple LDAP authentication, whether to enable LDAP search referral. See [LDAP Search](#page-139-0) [Referral.](#page-139-0)

#### <span id="page-182-0"></span>• [authentication\\_ldap\\_simple\\_response\\_timeout](#page-182-0)

| Command-Line Format  | authentication-ldap-simple<br>response-timeout=# |
|----------------------|--------------------------------------------------|
| System Variable      | authentication_ldap_simple_response_timeout      |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |

| Type          | Integer  |
|---------------|----------|
| Default Value | 30       |
| Minimum Value | 0        |
| Maximum Value | 31536000 |
| Unit          | seconds  |

Specifies the time (in seconds) that MySQL server waits for the LDAP server to response to an LDAP bind request.

When a MySQL account authenticates using LDAP, MySQL server sends an LDAP bind request to the LDAP server. If the LDAP server does not respond to the request after a configured amount of time, MySQL abandons the request and emits an error message. If the timeout setting is zero, MySQL server ignores this system variable setting. For more information, see [Setting Timeouts for](#page-125-1) [LDAP Pluggable Authentication.](#page-125-1)

<span id="page-183-0"></span>• [authentication\\_ldap\\_simple\\_server\\_host](#page-183-0)

| Command-Line Format  | authentication-ldap-simple-server<br>host=host_name |
|----------------------|-----------------------------------------------------|
| System Variable      | authentication_ldap_simple_server_host              |
| Scope                | Global                                              |
| Dynamic              | Yes                                                 |
| SET_VAR Hint Applies | No                                                  |
| Type                 | String                                              |

For simple LDAP authentication, the LDAP server host. The permitted values for this variable depend on the authentication method:

- For [authentication\\_ldap\\_simple\\_auth\\_method\\_name=SIMPLE](#page-176-1): The LDAP server host can be a host name or IP address.
- For [authentication\\_ldap\\_simple\\_auth\\_method\\_name=AD-FOREST](#page-176-1). The LDAP server host can be an Active Directory domain name. For example, for an LDAP server URL of ldap:// example.mem.local:389, the domain name can be mem.local.

An Active Directory forest setup can have multiple domains (LDAP server IPs), which can be discovered using DNS. On Unix and Unix-like systems, some additional setup may be required to configure your DNS server with SRV records that specify the LDAP servers for the Active Directory domain. For information about DNS SRV, see [RFC 2782.](https://tools.ietf.org/html/rfc2782)

Suppose that your configuration has these properties:

- The name server that provides information about Active Directory domains has IP address 10.172.166.100.
- The LDAP servers have names ldap1.mem.local through ldap3.mem.local and IP addresses 10.172.166.101 through 10.172.166.103.

You want the LDAP servers to be discoverable using SRV searches. For example, at the command line, a command like this should list the LDAP servers:

```
host -t SRV _ldap._tcp.mem.local
```

Perform the DNS configuration as follows:

1. Add a line to /etc/resolv.conf to specify the name server that provides information about Active Directory domains:

```
nameserver 10.172.166.100
```

2. Configure the appropriate zone file for the name server with SRV records for the LDAP servers:

```
_ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap1.mem.local.
_ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap2.mem.local.
_ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap3.mem.local.
```

3. It may also be necessary to specify the IP address for the LDAP servers in /etc/hosts if the server host cannot be resolved. For example, add lines like this to the file:

```
10.172.166.101 ldap1.mem.local
10.172.166.102 ldap2.mem.local
10.172.166.103 ldap3.mem.local
```

With the DNS configured as just described, the server-side LDAP plugin can discover the LDAP servers and tries to authenticate in all domains until authentication succeeds or there are no more servers.

Windows needs no such settings as just described. Given the LDAP server host in the [authentication\\_ldap\\_simple\\_server\\_host](#page-183-0) value, the Windows LDAP library searches all domains and attempts to authenticate.

<span id="page-184-0"></span>• [authentication\\_ldap\\_simple\\_server\\_port](#page-184-0)

| Command-Line Format  | authentication-ldap-simple-server<br>port=port_num |
|----------------------|----------------------------------------------------|
| System Variable      | authentication_ldap_simple_server_port             |
| Scope                | Global                                             |
| Dynamic              | Yes                                                |
| SET_VAR Hint Applies | No                                                 |
| Type                 | Integer                                            |
| Default Value        | 389                                                |
| Minimum Value        | 1                                                  |

| Maximum Value | 32376 |
|---------------|-------|
|---------------|-------|

For simple LDAP authentication, the LDAP server TCP/IP port number.

If the LDAP port number is configured as 636 or 3269, the plugin uses LDAPS (LDAP over SSL) instead of LDAP. (LDAPS differs from startTLS.)

<span id="page-185-0"></span>• [authentication\\_ldap\\_simple\\_tls](#page-185-0)

| Command-Line Format  | authentication-ldap-simple<br>tls[={OFF ON}] |
|----------------------|----------------------------------------------|
| System Variable      | authentication_ldap_simple_tls               |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Boolean                                      |
| Default Value        | OFF                                          |

For simple LDAP authentication, whether connections by the plugin to the LDAP server are secure. If this variable is enabled, the plugin uses TLS to connect securely to the LDAP server. This variable can be set to override the default OpenLDAP TLS configuration; see [LDAP](#page-125-0) [Pluggable Authentication and ldap.conf](#page-125-0) If you enable this variable, you may also wish to set the [authentication\\_ldap\\_simple\\_ca\\_path](#page-178-0) variable.

MySQL LDAP plugins support the StartTLS method, which initializes TLS on top of a plain LDAP connection.

LDAPS can be used by setting the [authentication\\_ldap\\_simple\\_server\\_port](#page-184-0) system variable.

<span id="page-185-1"></span>• [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-185-1)

| Command-Line Format  | authentication-ldap-simple-user<br>search-attr=value |
|----------------------|------------------------------------------------------|
| System Variable      | authentication_ldap_simple_user_search_attr          |
| Scope                | Global                                               |
| Dynamic              | Yes                                                  |
| SET_VAR Hint Applies | No                                                   |
| Type                 | String                                               |
| Default Value        | uid                                                  |

For simple LDAP authentication, the name of the attribute that specifies user names in LDAP directory entries. If a user distinguished name is not provided, the authentication plugin searches for the name using this attribute. For example, if the [authentication\\_ldap\\_simple\\_user\\_search\\_attr](#page-185-1) value is uid, a search for the user name user1 finds entries with a uid value of user1.

• [authentication\\_webauthn\\_rp\\_id](#page-185-2)

<span id="page-185-2"></span>

|      | Command-Line Format | authentication-webauthn-rp<br>id=value |
|------|---------------------|----------------------------------------|
|      | System Variable     | authentication_webauthn_rp_id          |
| 1356 | Scope               | Global                                 |

| Dynamic              | Yes    |
|----------------------|--------|
| SET_VAR Hint Applies | No     |
| Type                 | String |

This variable specifies the relying party ID used for server-side plugin installation, device registration, and WebAuthn authentication. If WebAuthn authentication is attempted and this value is not the one expected by the device, the device assumes that it is not talking to the correct server and an error occurs. The maximum value length is 255 characters.