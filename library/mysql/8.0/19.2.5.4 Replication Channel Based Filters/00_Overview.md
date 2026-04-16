---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section explains how to work with replication filters when multiple replication channels exist, for example in a multi-source replication topology. Before MySQL 8.0, all replication filters were global, so filters were applied to all replication channels. From MySQL 8.0, replication filters can be global or channel specific, enabling you to configure multi-source replicas with replication filters on specific replication channels. Channel specific replication filters are particularly useful in a multi-source replication topology when the same database or table is present on multiple sources, and the replica is only required to replicate it from one source.

For instructions to set up replication channels, see Section 19.1.5, "MySQL Multi-Source Replication", and for more information on how they work, see Section 19.2.2, "Replication Channels".

![](_page_6_Picture_10.jpeg)

#### **Important**

Each channel on a multi-source replica must replicate from a different source. You cannot set up multiple replication channels from a single replica to a single source, even if you use replication filters to select different data to replicate on each channel. This is because the server IDs of replicas must be unique in a replication topology. The source distinguishes replicas only by their server IDs, not by the names of the replication channels, so it cannot recognize different replication channels from the same replica.

![](_page_6_Picture_13.jpeg)

#### **Important**

On a MySQL server instance that is configured for Group Replication, channel specific replication filters can be used on replication channels that are not directly involved with Group Replication, such as where a group member also acts as a replica to a source that is outside the group. They cannot be used on the group\_replication\_applier or group\_replication\_recovery channels. Filtering on these channels would make the group unable to reach agreement on a consistent state.

![](_page_7_Picture_2.jpeg)

#### **Important**

For a multi-source replica in a diamond topology (where the replica replicates from two or more sources, which in turn replicate from a common source), when GTID-based replication is in use, ensure that any replication filters or other channel configuration are identical on all channels on the multi-source replica. With GTID-based replication, filters are applied only to the transaction data, and GTIDs are not filtered out. This happens so that a replica's GTID set stays consistent with the source's, meaning GTID auto-positioning can be used without re-acquiring filtered out transactions each time. In the case where the downstream replica is multi-source and receives the same transaction from multiple sources in a diamond topology, the downstream replica now has multiple versions of the transaction, and the result depends on which channel applies the transaction first. The second channel to attempt it skips the transaction using GTID auto-skip, because the transaction's GTID was added to the gtid\_executed set by the first channel. With identical filtering on the channels, there is no problem because all versions of the transaction contain the same data, so the results are the same. However, with different filtering on the channels, the database can become inconsistent and replication can hang.

### <span id="page-7-0"></span>**Overview of Replication Filters and Channels**

When multiple replication channels exist, for example in a multi-source replication topology, replication filters are applied as follows:

- Any global replication filter specified is added to the global replication filters of the filter type (do\_db, do\_ignore\_table, and so on).
- Any channel specific replication filter adds the filter to the specified channel's replication filters for the specified filter type.
- Each replication channel copies global replication filters to its channel specific replication filters if no channel specific replication filter of this type is configured.
- Each channel uses its channel specific replication filters to filter the replication stream.

The syntax to create channel specific replication filters extends the existing SQL statements and command options. When a replication channel is not specified the global replication filter is configured to ensure backwards compatibility. The CHANGE REPLICATION FILTER statement supports the FOR CHANNEL clause to configure channel specific filters online. The --replicate- \* command options to configure filters can specify a replication channel using the form - replicate-filter\_type=channel\_name:filter\_details. Suppose channels channel\_1 and channel\_2 exist before the server starts; in this case, starting the replica with the command line options --replicate-do-db=db1 --replicate-do-db=channel\_1:db2 --replicatedo-db=db3 --replicate-ignore-db=db4 --replicate-ignore-db=channel\_2:db5 - replicate-wild-do-table=channel\_1:db6.t1% would result in:

- Global replication filters: do\_db=db1,db3; ignore\_db=db4
- Channel specific filters on channel\_1: do\_db=db2; ignore\_db=db4; wild-do-table=db6.t1%
- Channel specific filters on channel\_2: do\_db=db1,db3; ignore\_db=db5

These same rules could be applied at startup when included in the replica's my.cnf file, like this:

```
replicate-do-db=db1
replicate-do-db=channel_1:db2
replicate-ignore-db=db4
```

```
replicate-ignore-db=channel_2:db5
replicate-wild-do-table=channel_1:db6.t1%
```

To monitor the replication filters in such a setup use the replication\_applier\_global\_filters and replication\_applier\_filters tables.

### **Configuring Channel Specific Replication Filters at Startup**

The replication filter related command options can take an optional channel followed by a colon, followed by the filter specification. The first colon is interpreted as a separator, subsequent colons are interpreted as literal colons. The following command options support channel specific replication filters using this format:

- --replicate-do-db=channel:database\_id
- --replicate-ignore-db=channel:database\_id
- --replicate-do-table=channel:table\_id
- --replicate-ignore-table=channel:table\_id
- --replicate-rewrite-db=channel:db1-db2
- --replicate-wild-do-table=channel:table pattern
- --replicate-wild-ignore-table=channel:table pattern

All of the options just listed can be used in the replica's my.cnf file, as with most other MySQL server startup options, by omitting the two leading dashes. See [Overview of Replication Filters and Channels](#page-7-0), for a brief example, as well as Section 6.2.2.2, "Using Option Files".

If you use a colon but do not specify a channel for the filter option, for example --replicate-dodb=:database\_id, the option configures the replication filter for the default replication channel. The default replication channel is the replication channel which always exists once replication has been started, and differs from multi-source replication channels which you create manually. When neither the colon nor a channel is specified the option configures the global replication filters, for example - replicate-do-db=database\_id configures the global --replicate-do-db filter.

If you configure multiple rewrite-db=from\_name->to\_name options with the same from\_name database, all filters are added together (put into the rewrite\_do list) and the first one takes effect.

The pattern used for the --replicate-wild-\*-table options can include any characters allowed in identifiers as well as the wildcards % and \_. These work the same way as when used with the LIKE operator; for example, tbl% matches any table name beginning with tbl, and tbl\_ matches any table name matching tbl plus one additional character.

#### **Changing Channel Specific Replication Filters Online**

In addition to the --replicate-\* options, replication filters can be configured using the CHANGE REPLICATION FILTER statement. This removes the need to restart the server, but the replication SQL thread must be stopped while making the change. To make this statement apply the filter to a specific channel, use the FOR CHANNEL channel clause. For example:

```
CHANGE REPLICATION FILTER REPLICATE_DO_DB=(db1) FOR CHANNEL channel_1;
```

When a FOR CHANNEL clause is provided, the statement acts on the specified channel's replication filters. If multiple types of filters (do\_db, do\_ignore\_table, wild\_do\_table, and so on) are specified, only the specified filter types are replaced by the statement. In a replication topology with multiple channels, for example on a multi-source replica, when no FOR CHANNEL clause is provided, the statement acts on the global replication filters and all channels' replication filters, using a similar logic as the FOR CHANNEL case. For more information see Section 15.4.2.2, "CHANGE REPLICATION FILTER Statement".

#### **Removing Channel Specific Replication Filters**

When channel specific replication filters have been configured, you can remove the filter by issuing an empty filter type statement. For example to remove all REPLICATE\_REWRITE\_DB filters from a replication channel named channel\_1 issue:

```
CHANGE REPLICATION FILTER REPLICATE_REWRITE_DB=() FOR CHANNEL channel_1;
```

Any REPLICATE\_REWRITE\_DB filters previously configured, using either command options or CHANGE REPLICATION FILTER, are removed.

The RESET REPLICA ALL statement removes channel specific replication filters that were set on channels deleted by the statement. When the deleted channel or channels are recreated, any global replication filters specified for the replica are copied to them, and no channel specific replication filters are applied.

# <span id="page-9-1"></span>**19.3 Replication Security**

To protect against unauthorized access to data that is stored on and transferred between replication source servers and replicas, set up all the servers involved using the security measures that you would choose for any MySQL instance in your installation, as described in Chapter 8, Security. In addition, for servers in a replication topology, consider implementing the following security measures:

- Set up sources and replicas to use encrypted connections to transfer the binary log, which protects this data in motion. Encryption for these connections must be activated using a CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement, in addition to setting up the servers to support encrypted network connections. See [Section 19.3.1, "Setting Up Replication to Use](#page-9-0) [Encrypted Connections".](#page-9-0)
- Encrypt the binary log files and relay log files on sources and replicas, which protects this data at rest, and also any data in use in the binary log cache. Binary log encryption is activated using the binlog\_encryption system variable. See [Section 19.3.2, "Encrypting Binary Log Files and Relay](#page-12-0) [Log Files".](#page-12-0)
- Apply privilege checks to replication appliers, which help to secure replication channels against the unauthorized or accidental use of privileged or unwanted operations. Privilege checks are implemented by setting up a PRIVILEGE\_CHECKS\_USER account, which MySQL uses to verify that you have authorized each specific transaction for that channel. See [Section 19.3.3, "Replication](#page-15-0) [Privilege Checks".](#page-15-0)

For Group Replication, binary log encryption and privilege checks can be used as a security measure on replication group members. You should also consider encrypting the connections between group members, comprising group communication connections and distributed recovery connections, and applying IP address allowlisting to exclude untrusted hosts. For information on these security measures specific to Group Replication, see [Section 20.6, "Group Replication Security"](#page-157-0).

# <span id="page-9-0"></span>**19.3.1 Setting Up Replication to Use Encrypted Connections**

To use an encrypted connection for the transfer of the binary log required during replication, both the source and the replica servers must support encrypted network connections. If either server does not support encrypted connections (because it has not been compiled or configured for them), replication through an encrypted connection is not possible.

Setting up encrypted connections for replication is similar to doing so for client/server connections. You must obtain (or create) a suitable security certificate that you can use on the source, and a similar certificate (from the same certificate authority) on each replica. You must also obtain suitable key files.

For more information on setting up a server and client for encrypted connections, see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections".

To enable encrypted connections on the source, you must create or obtain suitable certificate and key files, and then add the following configuration parameters to the [mysqld] section of the source my.cnf file, changing the file names as necessary:

```
[mysqld]
ssl_ca=cacert.pem
ssl_cert=server-cert.pem
ssl_key=server-key.pem
```

The paths to the files may be relative or absolute; we recommend that you always use complete paths for this purpose.

The configuration parameters are as follows:

- ssl\_ca: The path name of the Certificate Authority (CA) certificate file. (ssl\_capath is similar but specifies the path name of a directory of CA certificate files.)
- ssl\_cert: The path name of the server public key certificate file. This certificate can be sent to the client and authenticated against the CA certificate that it has.
- ssl\_key: The path name of the server private key file.

To enable encrypted connections on the replica, use the CHANGE REPLICATION SOURCE TO statement (MySQL 8.0.23 and later) or CHANGE MASTER TO statement (prior to MySQL 8.0.23).

• To name the replica's certificate and SSL private key files using CHANGE REPLICATION SOURCE TO (CHANGE MASTER TO), add the appropriate SOURCE\_SSL\_xxx (MASTER\_SSL\_xxx) options, like this:

```
 -> SOURCE_SSL_CA = 'ca_file_name',
 -> SOURCE_SSL_CAPATH = 'ca_directory_name',
 -> SOURCE_SSL_CERT = 'cert_file_name',
 -> SOURCE_SSL_KEY = 'key_file_name',
```

These options correspond to the --ssl-xxx options with the same names, as described in Command Options for Encrypted Connections. For these options to take effect, SOURCE\_SSL=1 must also be set. For a replication connection, specifying a value for either of SOURCE\_SSL\_CA or SOURCE\_SSL\_CAPATH corresponds to setting --ssl-mode=VERIFY\_CA. The connection attempt succeeds only if a valid matching Certificate Authority (CA) certificate is found using the specified information.

• To activate host name identity verification, add the SOURCE\_SSL\_VERIFY\_SERVER\_CERT option, like this:

```
 -> SOURCE_SSL_VERIFY_SERVER_CERT=1,
```

This option corresponds to the --ssl-verify-server-cert option, which is deprecated in MySQL 5.7 and removed in MySQL 8.0. For a replication connection, specifying MASTER\_SSL\_VERIFY\_SERVER\_CERT=1 corresponds to setting --sslmode=VERIFY\_IDENTITY, as described in Command Options for Encrypted Connections. For this option to take effect, SOURCE\_SSL=1 must also be set. Host name identity verification does not work with self-signed certificates.

• To activate certificate revocation list (CRL) checks, add the SOURCE\_SSL\_CRL or SOURCE\_SSL\_CRLPATH option, as shown here:

```
 -> SOURCE_SSL_CRL = 'crl_file_name',
 -> SOURCE_SSL_CRLPATH = 'crl_directory_name',
```

These options correspond to the --ssl-xxx options with the same names, as described in Command Options for Encrypted Connections. If they are not specified, no CRL checking takes place.

• To specify lists of ciphers, ciphersuites, and encryption protocols permitted by the replica for the replication connection, use the SOURCE\_SSL\_CIPHER, SOURCE\_TLS\_VERSION, and SOURCE\_TLS\_CIPHERSUITES options, like this:

```
 -> SOURCE_SSL_CIPHER = 'cipher_list',
 -> SOURCE_TLS_VERSION = 'protocol_list',
 -> SOURCE_TLS_CIPHERSUITES = 'ciphersuite_list',
```

- The SOURCE\_SSL\_CIPHER option specifies a colon-separated list of one or more ciphers permitted by the replica for the replication connection.
- The SOURCE\_TLS\_VERSION option specifies a comma-separated list of the TLS encryption protocols permitted by the replica for the replication connection, in a format like that for the tls\_version server system variable. The connection procedure negotiates the use of the highest TLS version that both the source and the replica permit. To be able to connect, the replica must have at least one TLS version in common with the source.
- The SOURCE\_TLS\_CIPHERSUITES option (available beginning with MySQL 8.0.19) specifies a colon-separated list of one or more ciphersuites that are permitted by the replica for the replication connection if TLSv1.3 is used for the connection. If this option is set to NULL when TLSv1.3 is used (which is the default if you do not set the option), the ciphersuites that are enabled by default are allowed. If you set the option to an empty string, no cipher suites are allowed, and TLSv1.3 is therefore not used.

The protocols, ciphers, and ciphersuites that you can specify in these lists depend on the SSL library used to compile MySQL. For information about the formats, the permitted values, and the defaults if you do not specify the options, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

![](_page_11_Picture_7.jpeg)

#### **Note**

In MySQL 8.0.16 through 8.0.18, MySQL supports TLSv1.3, but the SOURCE\_TLS\_CIPHERSUITES option is not available. In these releases, if TLSv1.3 is used for connections between a source and replica, the source must permit the use of at least one TLSv1.3 ciphersuite that is enabled by default. From MySQL 8.0.19, you can use the option to specify any selection of ciphersuites, including only non-default ciphersuites if you want.

• After the source information has been updated, start the replication process on the replica, like this:

```
mysql> START SLAVE;
```

Beginning with MySQL 8.0.22, START REPLICA is preferred, as shown here:

```
mysql> START REPLICA;
```

You can use the SHOW REPLICA STATUS (prior to MySQL 8.0.22, SHOW SLAVE STATUS) statement to confirm that an encrypted connection was established successfully.

• Requiring encrypted connections on the replica does not ensure that the source requires encrypted connections from replicas. If you want to ensure that the source only accepts replicas that connect using encrypted connections, create a replication user account on the source using the REQUIRE SSL option, then grant that user the REPLICATION SLAVE privilege. For example:

```
mysql> CREATE USER 'repl'@'%.example.com' IDENTIFIED BY 'password'
 -> REQUIRE SSL;
mysql> GRANT REPLICATION SLAVE ON *.*
 -> TO 'repl'@'%.example.com';
```

If you have an existing replication user account on the source, you can add REQUIRE SSL to it with this statement:

```
mysql> ALTER USER 'repl'@'%.example.com' REQUIRE SSL;
```

# <span id="page-12-0"></span>**19.3.2 Encrypting Binary Log Files and Relay Log Files**

From MySQL 8.0.14, binary log files and relay log files can be encrypted, helping to protect these files and the potentially sensitive data contained in them from being misused by outside attackers, and also from unauthorized viewing by users of the operating system where they are stored. The encryption algorithm used for the files, the AES (Advanced Encryption Standard) cipher algorithm, is built in to MySQL Server and cannot be configured.

You enable this encryption on a MySQL server by setting the binlog\_encryption system variable to ON. OFF is the default. The system variable sets encryption on for binary log files and relay log files. Binary logging does not need to be enabled on the server to enable encryption, so you can encrypt the relay log files on a replica that has no binary log. To use encryption, a keyring component or plugin must be installed and configured to supply MySQL Server's keyring service. For instructions to do this, see Section 8.4.4, "The MySQL Keyring". Any supported keyring component or plugin can be used to store binary log encryption keys.

When you first start the server with encryption enabled, a new binary log encryption key is generated before the binary log and relay logs are initialized. This key is used to encrypt a file password for each binary log file (if the server has binary logging enabled) and relay log file (if the server has replication channels), and further keys generated from the file passwords are used to encrypt the data in the files. The binary log encryption key that is currently in use on the server is called the binary log master key. The two tier encryption key architecture means that the binary log master key can be rotated (replaced by a new master key) as required, and only the file password for each file needs to be re-encrypted with the new master key, not the whole file. Relay log files are encrypted for all channels, including new channels that are created after encryption is activated. The binary log index file and relay log index file are never encrypted.

If you activate encryption while the server is running, a new binary log encryption key is generated at that time. The exception is if encryption was active previously on the server and was then disabled, in which case the binary log encryption key that was in use before is used again. The binary log file and relay log files are rotated immediately, and file passwords for the new files and all subsequent binary log files and relay log files are encrypted using this binary log encryption key. Existing binary log files and relay log files still present on the server are not encrypted, but you can purge them if they are no longer needed.

If you deactivate encryption by changing the binlog\_encryption system variable to OFF, the binary log file and relay log files are rotated immediately and all subsequent logging is unencrypted. Previously encrypted files are not automatically decrypted, but the server is still able to read them. The BINLOG\_ENCRYPTION\_ADMIN privilege is required to activate or deactivate encryption while the server is running.

Encrypted and unencrypted binary log files can be distinguished using the magic number at the start of the file header for encrypted log files (0xFD62696E), which differs from that used for unencrypted log files (0xFE62696E). The SHOW BINARY LOGS statement shows whether each binary log file is encrypted or unencrypted.

When binary log files have been encrypted, mysqlbinlog cannot read them directly, but can read them from the server using the --read-from-remote-server option. From MySQL 8.0.14, mysqlbinlog returns a suitable error if you attempt to read an encrypted binary log file directly, but older versions of mysqlbinlog do not recognize the file as a binary log file at all. If you back up encrypted binary log files using mysqlbinlog, note that the copies of the files that are generated using mysqlbinlog are stored in an unencrypted format.

Binary log encryption can be combined with binary log transaction compression (available as of MySQL 8.0.20). For more information on binary log transaction compression, see Section 7.4.4.5, "Binary Log Transaction Compression".