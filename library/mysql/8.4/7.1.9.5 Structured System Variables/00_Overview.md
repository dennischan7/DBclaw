---
source: MySQL 8.4 Reference
title: 00_Overview
---

A structured variable differs from a regular system variable in two respects:

- Its value is a structure with components that specify server parameters considered to be closely related.
- There might be several instances of a given type of structured variable. Each one has a different name and refers to a different resource maintained by the server.

MySQL supports one structured variable type, which specifies parameters governing the operation of key caches. A key cache structured variable has these components:

```
• key_buffer_size
```

- [key\\_cache\\_block\\_size](#page-8-0)
- [key\\_cache\\_division\\_limit](#page-8-2)
- [key\\_cache\\_age\\_threshold](#page-8-1)

This section describes the syntax for referring to structured variables. Key cache variables are used for syntax examples, but specific details about how key caches operate are found elsewhere, in Section 10.10.2, "The MyISAM Key Cache".

To refer to a component of a structured variable instance, you can use a compound name in instance\_name.component\_name format. Examples:

```
hot_cache.key_buffer_size
hot_cache.key_cache_block_size
cold_cache.key_cache_block_size
```

For each structured system variable, an instance with the name of default is always predefined. If you refer to a component of a structured variable without any instance name, the default instance is used. Thus, default.key\_buffer\_size and [key\\_buffer\\_size](#page-6-1) both refer to the same system variable.

Structured variable instances and components follow these naming rules:

- For a given type of structured variable, each instance must have a name that is unique within variables of that type. However, instance names need not be unique across structured variable types. For example, each structured variable has an instance named default, so default is not unique across variable types.
- The names of the components of each structured variable type must be unique across all system variable names. If this were not true (that is, if two different types of structured variables could share component member names), it would not be clear which default structured variable to use for references to member names that are not qualified by an instance name.
- If a structured variable instance name is not legal as an unquoted identifier, refer to it as a quoted identifier using backticks. For example, hot-cache is not legal, but `hot-cache` is.
- global, session, and local are not legal instance names. This avoids a conflict with notation such as @@GLOBAL.var\_name for referring to nonstructured system variables.

Currently, the first two rules have no possibility of being violated because the only structured variable type is the one for key caches. These rules may assume greater significance if some other type of structured variable is created in the future.

With one exception, you can refer to structured variable components using compound names in any context where simple variable names can occur. For example, you can assign a value to a structured variable using a command-line option:

```
$> mysqld --hot_cache.key_buffer_size=64K
```

In an option file, use this syntax:

```
[mysqld]
hot_cache.key_buffer_size=64K
```

If you start the server with this option, it creates a key cache named hot\_cache with a size of 64KB in addition to the default key cache that has a default size of 8MB.

Suppose that you start the server as follows:

```
$> mysqld --key_buffer_size=256K \
 --extra_cache.key_buffer_size=128K \
 --extra_cache.key_cache_block_size=2048
```

In this case, the server sets the size of the default key cache to 256KB. (You could also have written --default.key\_buffer\_size=256K.) In addition, the server creates a second key cache named extra\_cache that has a size of 128KB, with the size of block buffers for caching table index blocks set to 2048 bytes.

The following example starts the server with three different key caches having sizes in a 3:1:1 ratio:

```
$> mysqld --key_buffer_size=6M \
```

```
 --hot_cache.key_buffer_size=2M \
 --cold_cache.key_buffer_size=2M
```

Structured variable values may be set and retrieved at runtime as well. For example, to set a key cache named hot\_cache to a size of 10MB, use either of these statements:

```
mysql> SET GLOBAL hot_cache.key_buffer_size = 10*1024*1024;
mysql> SET @@GLOBAL.hot_cache.key_buffer_size = 10*1024*1024;
```

To retrieve the cache size, do this:

```
mysql> SELECT @@GLOBAL.hot_cache.key_buffer_size;
```

However, the following statement does not work. The variable is not interpreted as a compound name, but as a simple string for a LIKE pattern-matching operation:

```
mysql> SHOW GLOBAL VARIABLES LIKE 'hot_cache.key_buffer_size';
```

This is the exception to being able to use structured variable names anywhere a simple variable name may occur.

# <span id="page-138-0"></span>**7.1.10 Server Status Variables**

The MySQL server maintains many status variables that provide information about its operation. You can view these variables and their values by using the SHOW [GLOBAL | SESSION] STATUS statement (see Section 15.7.7.37, "SHOW STATUS Statement"). The optional GLOBAL keyword aggregates the values over all connections, and SESSION shows the values for the current connection.

| mysql> SHOW GLOBAL STATUS;                                                         |                                                     |
|------------------------------------------------------------------------------------|-----------------------------------------------------|
| +++<br>  Variable_name                                                             | Value<br>                                           |
| +++<br>  Aborted_clients<br>  Aborted_connects<br>  Bytes_received<br>  Bytes_sent | 0<br> <br>  0<br> <br>  155372598  <br>  1176560426 |
| <br>  Connections                                                                  | 30023<br>                                           |
| Created_tmp_disk_tables<br>  Created_tmp_files<br>  Created_tmp_tables             | 0<br> <br>  3<br> <br>  2<br>                       |
| <br>  Threads_created<br>  Threads_running<br>  Uptime                             | 217<br> <br>  88<br> <br>  1389872<br>              |
| +++                                                                                |                                                     |

Many status variables are reset to 0 by the FLUSH STATUS statement.

This section provides a description of each status variable. For a status variable summary, see Section 7.1.6, "Server Status Variable Reference". For information about status variables specific to NDB Cluster, see NDB Cluster Status Variables.

The status variables have the following meanings.

<span id="page-138-1"></span>• [Aborted\\_clients](#page-138-1)

The number of connections that were aborted because the client died without closing the connection properly. See Section B.3.2.9, "Communication Errors and Aborted Connections".

<span id="page-138-2"></span>• [Aborted\\_connects](#page-138-2)

The number of failed attempts to connect to the MySQL server. See Section B.3.2.9, "Communication Errors and Aborted Connections".

For additional connection-related information, check the [Connection\\_errors\\_](#page-140-0)xxx status variables and the host\_cache table.

<span id="page-139-0"></span>• [Authentication\\_ldap\\_sasl\\_supported\\_methods](#page-139-0)

The authentication\_ldap\_sasl plugin that implements SASL LDAP authentication supports multiple authentication methods, but depending on host system configuration, they might not all be available. The [Authentication\\_ldap\\_sasl\\_supported\\_methods](#page-139-0) variable provides discoverability for the supported methods. Its value is a string consisting of supported method names separated by spaces. Example: "SCRAM-SHA 1 SCRAM-SHA-256 GSSAPI"

<span id="page-139-1"></span>• [Binlog\\_cache\\_disk\\_use](#page-139-1)

The number of transactions that used the temporary binary log cache but that exceeded the value of binlog\_cache\_size and used a temporary file to store statements from the transaction.

The number of nontransactional statements that caused the binary log transaction cache to be written to disk is tracked separately in the [Binlog\\_stmt\\_cache\\_disk\\_use](#page-139-2) status variable.

<span id="page-139-3"></span>• [Acl\\_cache\\_items\\_count](#page-139-3)

The number of cached privilege objects. Each object is the privilege combination of a user and its active roles.

<span id="page-139-4"></span>• [Binlog\\_cache\\_use](#page-139-4)

The number of transactions that used the binary log cache.

<span id="page-139-2"></span>• [Binlog\\_stmt\\_cache\\_disk\\_use](#page-139-2)

The number of nontransaction statements that used the binary log statement cache but that exceeded the value of binlog\_stmt\_cache\_size and used a temporary file to store those statements.

<span id="page-139-5"></span>• [Binlog\\_stmt\\_cache\\_use](#page-139-5)

The number of nontransactional statements that used the binary log statement cache.

<span id="page-139-6"></span>• [Bytes\\_received](#page-139-6)

The number of bytes received from all clients.

<span id="page-139-7"></span>• [Bytes\\_sent](#page-139-7)

The number of bytes sent to all clients.

<span id="page-139-8"></span>• [Caching\\_sha2\\_password\\_rsa\\_public\\_key](#page-139-8)

The public key used by the caching\_sha2\_password authentication plugin for RSA key pairbased password exchange. The value is nonempty only if the server successfully initializes the private and public keys in the files named by the caching\_sha2\_password\_private\_key\_path and caching\_sha2\_password\_public\_key\_path system variables. The value of [Caching\\_sha2\\_password\\_rsa\\_public\\_key](#page-139-8) comes from the latter file.

<span id="page-139-9"></span>• Com\_xxx

The Com\_xxx statement counter variables indicate the number of times each xxx statement has been executed. There is one status variable for each type of statement. For example, Com\_delete and Com\_update count DELETE and UPDATE statements, respectively. Com\_delete\_multi and Com\_update\_multi are similar but apply to DELETE and UPDATE statements that use multipletable syntax.

All Com\_stmt\_xxx variables are increased even if a prepared statement argument is unknown or an error occurred during execution. In other words, their values correspond to the number of requests issued, not to the number of requests successfully completed. For example, because status variables are initialized for each server startup and do not persist across restarts, the Com\_restart

and Com\_shutdown variables that track RESTART and SHUTDOWN statements normally have a value of zero, but can be nonzero if RESTART or SHUTDOWN statements were executed but failed.

The Com\_stmt\_xxx status variables are as follows:

- Com\_stmt\_prepare
- Com\_stmt\_execute
- Com\_stmt\_fetch
- Com\_stmt\_send\_long\_data
- Com\_stmt\_reset
- Com\_stmt\_close

Those variables stand for prepared statement commands. Their names refer to the COM\_xxx command set used in the network layer. In other words, their values increase whenever prepared statement API calls such as mysql\_stmt\_prepare(), mysql\_stmt\_execute(), and so forth are executed. However, Com\_stmt\_prepare, Com\_stmt\_execute and Com\_stmt\_close also increase for PREPARE, EXECUTE, or DEALLOCATE PREPARE, respectively. Additionally, the values of the older statement counter variables Com\_prepare\_sql, Com\_execute\_sql, and Com\_dealloc\_sql increase for the PREPARE, EXECUTE, and DEALLOCATE PREPARE statements. Com\_stmt\_fetch stands for the total number of network round-trips issued when fetching from cursors.

Com\_stmt\_reprepare indicates the number of times statements were automatically reprepared by the server, for example, after metadata changes to tables or views referred to by the statement. A reprepare operation increments Com\_stmt\_reprepare, and also Com\_stmt\_prepare.

Com\_explain\_other indicates the number of EXPLAIN FOR CONNECTION statements executed. See Section 10.8.4, "Obtaining Execution Plan Information for a Named Connection".

Com\_change\_repl\_filter indicates the number of CHANGE REPLICATION FILTER statements executed.

<span id="page-140-1"></span>• [Compression](#page-140-1)

Whether the client connection uses compression in the client/server protocol.

This status variable is deprecated; expect it to be removed in a future version of MySQL. See Configuring Legacy Connection Compression.

<span id="page-140-2"></span>• [Compression\\_algorithm](#page-140-2)

The name of the compression algorithm in use for the current connection to the server. The value can be any algorithm permitted in the value of the [protocol\\_compression\\_algorithms](#page-47-3) system variable. For example, the value is uncompressed if the connection does not use compression, or zlib if the connection uses the zlib algorithm.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-140-3"></span>• [Compression\\_level](#page-140-3)

The compression level in use for the current connection to the server. The value is 6 for zlib connections (the default zlib algorithm compression level), 1 to 22 for zstd connections, and 0 for uncompressed connections.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-140-0"></span>• [Connection\\_errors\\_](#page-140-0)xxx

These variables provide information about errors that occur during the client connection process. They are global only and represent error counts aggregated across connections from all hosts. These variables track errors not accounted for by the host cache (see [Section 7.1.12.3, "DNS](#page-178-0) [Lookups and the Host Cache"](#page-178-0)), such as errors that are not associated with TCP connections, occur very early in the connection process (even before an IP address is known), or are not specific to any particular IP address (such as out-of-memory conditions).

<span id="page-141-2"></span>• [Connection\\_errors\\_accept](#page-141-2)

The number of errors that occurred during calls to accept() on the listening port.

<span id="page-141-3"></span>• [Connection\\_errors\\_internal](#page-141-3)

The number of connections refused due to internal errors in the server, such as failure to start a new thread or an out-of-memory condition.

<span id="page-141-4"></span>• [Connection\\_errors\\_max\\_connections](#page-141-4)

The number of connections refused because the server [max\\_connections](#page-21-0) limit was reached.

<span id="page-141-5"></span>• [Connection\\_errors\\_peer\\_address](#page-141-5)

The number of errors that occurred while searching for connecting client IP addresses.

<span id="page-141-6"></span>• [Connection\\_errors\\_select](#page-141-6)

The number of errors that occurred during calls to select() or poll() on the listening port. (Failure of this operation does not necessarily means a client connection was rejected.)

<span id="page-141-7"></span>• [Connection\\_errors\\_tcpwrap](#page-141-7)

The number of connections refused by the libwrap library.

<span id="page-141-0"></span>• [Connections](#page-141-0)

The number of connection attempts (successful or not) to the MySQL server.

<span id="page-141-1"></span>• [Created\\_tmp\\_disk\\_tables](#page-141-1)

The number of internal on-disk temporary tables created by the server while executing statements.

You can compare the number of internal on-disk temporary tables created to the total number of internal temporary tables created by comparing [Created\\_tmp\\_disk\\_tables](#page-141-1) and [Created\\_tmp\\_tables](#page-142-0) values.

![](_page_141_Picture_19.jpeg)

# **Note**

Due to a known limitation, [Created\\_tmp\\_disk\\_tables](#page-141-1) does not count on-disk temporary tables created in memory-mapped files. By default, the TempTable storage engine overflow mechanism creates internal temporary tables in memory-mapped files. This behavior is controlled by the [temptable\\_use\\_mmap](#page-89-0) variable.

See also Section 10.4.4, "Internal Temporary Table Use in MySQL".

<span id="page-141-8"></span>• [Created\\_tmp\\_files](#page-141-8)

How many temporary files mysqld has created.

### <span id="page-142-0"></span>• [Created\\_tmp\\_tables](#page-142-0)

The number of internal temporary tables created by the server while executing statements.

You can compare the number of internal on-disk temporary tables created to the total number of internal temporary tables created by comparing [Created\\_tmp\\_disk\\_tables](#page-141-1) and [Created\\_tmp\\_tables](#page-142-0) values.

See also Section 10.4.4, "Internal Temporary Table Use in MySQL".

Each invocation of the SHOW STATUS statement uses an internal temporary table and increments the global [Created\\_tmp\\_tables](#page-142-0) value.

<span id="page-142-1"></span>• [Current\\_tls\\_ca](#page-142-1)

The active [ssl\\_ca](#page-76-2) value in the SSL context that the server uses for new connections. This context value may differ from the current [ssl\\_ca](#page-76-2) system variable value if the system variable has been changed but ALTER INSTANCE RELOAD TLS has not subsequently been executed to reconfigure the SSL context from the context-related system variable values and update the corresponding status variables. (This potential difference in values applies to each corresponding pair of contextrelated system and status variables. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections.)

The Current\_tls\_xxx status variable values are also available through the Performance Schema tls\_channel\_status table. See Section 29.12.22.9, "The tls\_channel\_status Table".

<span id="page-142-2"></span>• [Current\\_tls\\_capath](#page-142-2)

The active [ssl\\_capath](#page-77-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-142-3"></span>• [Current\\_tls\\_cert](#page-142-3)

The active [ssl\\_cert](#page-77-1) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-142-4"></span>• [Current\\_tls\\_cipher](#page-142-4)

The active [ssl\\_cipher](#page-78-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-142-5"></span>• [Current\\_tls\\_ciphersuites](#page-142-5)

The active [tls\\_ciphersuites](#page-98-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-142-6"></span>• [Current\\_tls\\_crl](#page-142-6)

The active [ssl\\_crl](#page-79-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

![](_page_142_Picture_19.jpeg)

### **Note**

When you reload the TLS context, OpenSSL reloads the file containing the CRL (certificate revocation list) as part of the process. If the CRL file is large, the server allocates a large chunk of memory (ten times the file size), which is doubled while the new instance is being loaded and the old one has not

yet been released. The process resident memory is not immediately reduced after a large allocation is freed, so if you issue the ALTER INSTANCE RELOAD TLS statement repeatedly with a large CRL file, the process resident memory usage may grow as a result of this.

<span id="page-143-0"></span>• [Current\\_tls\\_crlpath](#page-143-0)

The active [ssl\\_crlpath](#page-79-1) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-143-1"></span>• [Current\\_tls\\_key](#page-143-1)

The active [ssl\\_key](#page-80-0) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-143-2"></span>• [Current\\_tls\\_version](#page-143-2)

The active [tls\\_version](#page-98-1) value in the TLS context that the server uses for new connections. For notes about the relationship between this status variable and its corresponding system variable, see the description of [Current\\_tls\\_ca](#page-142-1).

<span id="page-143-3"></span>• [Delayed\\_errors](#page-143-3)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-143-4"></span>• [Delayed\\_insert\\_threads](#page-143-4)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-143-5"></span>• [Delayed\\_writes](#page-143-5)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-143-6"></span>• [Deprecated\\_use\\_i\\_s\\_processlist\\_count](#page-143-6)

How many times the information\_schema.processlist table has been accessed since the last restart.

<span id="page-143-7"></span>• [Deprecated\\_use\\_i\\_s\\_processlist\\_last\\_timestamp](#page-143-7)

A timestamp indicating the last time the information\_schema.processlist table has been accessed since the last restart. Shows microseconds since the Unix Epoch.

<span id="page-143-8"></span>• [dragnet.Status](#page-143-8)

The result of the most recent assignment to the dragnet.log\_error\_filter\_rules system variable, empty if no such assignment has occurred.

<span id="page-143-9"></span>• [Error\\_log\\_buffered\\_bytes](#page-143-9)

The number of bytes currently used in the Performance Schema error\_log table. It is possible for the value to decrease, for example, if a new event cannot fit until discarding an old event, but the new event is smaller than the old one.

<span id="page-143-10"></span>• [Error\\_log\\_buffered\\_events](#page-143-10)

The number of events currently present in the Performance Schema error\_log table. As with [Error\\_log\\_buffered\\_bytes](#page-143-9), it is possible for the value to decrease.

<span id="page-144-0"></span>• [Error\\_log\\_expired\\_events](#page-144-0)

The number of events discarded from the Performance Schema error\_log table to make room for new events.

<span id="page-144-1"></span>• [Error\\_log\\_latest\\_write](#page-144-1)

The time of the last write to the Performance Schema error\_log table.

<span id="page-144-2"></span>• [Flush\\_commands](#page-144-2)

The number of times the server flushes tables, whether because a user executed a FLUSH TABLES statement or due to internal server operation. It is also incremented by receipt of a COM\_REFRESH packet. This is in contrast to [Com\\_flush](#page-139-9), which indicates how many FLUSH statements have been executed, whether FLUSH TABLES, FLUSH LOGS, and so forth.

<span id="page-144-3"></span>• [Global\\_connection\\_memory](#page-144-3)

The memory used by all user connections to the server. Memory used by system threads or by the MySQL root account is included in the total, but such threads or users are not subject to disconnection due to memory usage. This memory is not calculated unless global\_connection\_memory\_tracking is enabled (disabled by default). The Performance Schema must also be enabled.

You can control (indirectly) the frequency with which this variable is updated by setting connection\_memory\_chunk\_size.

<span id="page-144-4"></span>• [Handler\\_commit](#page-144-4)

The number of internal COMMIT statements.

<span id="page-144-5"></span>• [Handler\\_delete](#page-144-5)

The number of times that rows have been deleted from tables.

<span id="page-144-6"></span>• [Handler\\_external\\_lock](#page-144-6)

The server increments this variable for each call to its external\_lock() function, which generally occurs at the beginning and end of access to a table instance. There might be differences among storage engines. This variable can be used, for example, to discover for a statement that accesses a partitioned table how many partitions were pruned before locking occurred: Check how much the counter increased for the statement, subtract 2 (2 calls for the table itself), then divide by 2 to get the number of partitions locked.

<span id="page-144-7"></span>• [Handler\\_mrr\\_init](#page-144-7)

The number of times the server uses a storage engine's own Multi-Range Read implementation for table access.

<span id="page-144-8"></span>• [Handler\\_prepare](#page-144-8)

A counter for the prepare phase of two-phase commit operations.

<span id="page-144-9"></span>• [Handler\\_read\\_first](#page-144-9)

The number of times the first entry in an index was read. If this value is high, it suggests that the server is doing a lot of full index scans (for example, SELECT col1 FROM foo, assuming that col1 is indexed).

<span id="page-144-10"></span>• [Handler\\_read\\_key](#page-144-10)

The number of requests to read a row based on a key. If this value is high, it is a good indication that your tables are properly indexed for your queries.

<span id="page-145-0"></span>• [Handler\\_read\\_last](#page-145-0)

The number of requests to read the last key in an index. With ORDER BY, the server issues a firstkey request followed by several next-key requests, whereas with ORDER BY DESC, the server issues a last-key request followed by several previous-key requests.

<span id="page-145-1"></span>• [Handler\\_read\\_next](#page-145-1)

The number of requests to read the next row in key order. This value is incremented if you are querying an index column with a range constraint or if you are doing an index scan.

<span id="page-145-2"></span>• [Handler\\_read\\_prev](#page-145-2)

The number of requests to read the previous row in key order. This read method is mainly used to optimize ORDER BY ... DESC.

<span id="page-145-3"></span>• [Handler\\_read\\_rnd](#page-145-3)

The number of requests to read a row based on a fixed position. This value is high if you are doing a lot of queries that require sorting of the result. You probably have a lot of queries that require MySQL to scan entire tables or you have joins that do not use keys properly.

<span id="page-145-4"></span>• [Handler\\_read\\_rnd\\_next](#page-145-4)

The number of requests to read the next row in the data file. This value is high if you are doing a lot of table scans. Generally this suggests that your tables are not properly indexed or that your queries are not written to take advantage of the indexes you have.

<span id="page-145-5"></span>• [Handler\\_rollback](#page-145-5)

The number of requests for a storage engine to perform a rollback operation.

<span id="page-145-6"></span>• [Handler\\_savepoint](#page-145-6)

The number of requests for a storage engine to place a savepoint.

<span id="page-145-7"></span>• [Handler\\_savepoint\\_rollback](#page-145-7)

The number of requests for a storage engine to roll back to a savepoint.

<span id="page-145-8"></span>• [Handler\\_update](#page-145-8)

The number of requests to update a row in a table.

<span id="page-145-9"></span>• [Handler\\_write](#page-145-9)

The number of requests to insert a row in a table.

<span id="page-145-10"></span>• [Innodb\\_buffer\\_pool\\_dump\\_status](#page-145-10)

The progress of an operation to record the pages held in the InnoDB buffer pool, triggered by the setting of innodb\_buffer\_pool\_dump\_at\_shutdown or innodb\_buffer\_pool\_dump\_now.

For related information and examples, see Section 17.8.3.6, "Saving and Restoring the Buffer Pool State".

<span id="page-145-11"></span>• [Innodb\\_buffer\\_pool\\_load\\_status](#page-145-11)

The progress of an operation to warm up the InnoDB buffer pool by reading in a set of pages corresponding to an earlier point in time, triggered by the setting of innodb\_buffer\_pool\_load\_at\_startup or innodb\_buffer\_pool\_load\_now. If the operation introduces too much overhead, you can cancel it by setting innodb\_buffer\_pool\_load\_abort.

For related information and examples, see Section 17.8.3.6, "Saving and Restoring the Buffer Pool State".

<span id="page-146-0"></span>• [Innodb\\_buffer\\_pool\\_bytes\\_data](#page-146-0)

The total number of bytes in the InnoDB buffer pool containing data. The number includes both dirty and clean pages. For more accurate memory usage calculations than with [Innodb\\_buffer\\_pool\\_pages\\_data](#page-146-1), when compressed tables cause the buffer pool to hold pages of different sizes.

<span id="page-146-1"></span>• [Innodb\\_buffer\\_pool\\_pages\\_data](#page-146-1)

The number of pages in the InnoDB buffer pool containing data. The number includes both dirty and clean pages. When using compressed tables, the reported [Innodb\\_buffer\\_pool\\_pages\\_data](#page-146-1) value may be larger than [Innodb\\_buffer\\_pool\\_pages\\_total](#page-146-2) (Bug #59550).

<span id="page-146-3"></span>• [Innodb\\_buffer\\_pool\\_bytes\\_dirty](#page-146-3)

The total current number of bytes held in dirty pages in the InnoDB buffer pool. For more accurate memory usage calculations than with [Innodb\\_buffer\\_pool\\_pages\\_dirty](#page-146-4), when compressed tables cause the buffer pool to hold pages of different sizes.

<span id="page-146-4"></span>• [Innodb\\_buffer\\_pool\\_pages\\_dirty](#page-146-4)

The current number of dirty pages in the InnoDB buffer pool.

<span id="page-146-5"></span>• [Innodb\\_buffer\\_pool\\_pages\\_flushed](#page-146-5)

The number of requests to flush pages from the InnoDB buffer pool.

<span id="page-146-6"></span>• [Innodb\\_buffer\\_pool\\_pages\\_free](#page-146-6)

The number of free pages in the InnoDB buffer pool.

<span id="page-146-7"></span>• [Innodb\\_buffer\\_pool\\_pages\\_latched](#page-146-7)

The number of latched pages in the InnoDB buffer pool. These are pages currently being read or written, or that cannot be flushed or removed for some other reason. Calculation of this variable is expensive, so it is available only when the UNIV\_DEBUG system is defined at server build time.

<span id="page-146-8"></span>• [Innodb\\_buffer\\_pool\\_pages\\_misc](#page-146-8)

The number of pages in the InnoDB buffer pool that are busy because they have been allocated for administrative overhead, such as row locks or the adaptive hash index. This value can also be calculated as [Innodb\\_buffer\\_pool\\_pages\\_total](#page-146-2) − [Innodb\\_buffer\\_pool\\_pages\\_free](#page-146-6) − [Innodb\\_buffer\\_pool\\_pages\\_data](#page-146-1). When using compressed tables, [Innodb\\_buffer\\_pool\\_pages\\_misc](#page-146-8) may report an out-of-bounds value (Bug #59550).

<span id="page-146-2"></span>• [Innodb\\_buffer\\_pool\\_pages\\_total](#page-146-2)

The total size of the InnoDB buffer pool, in pages. When using compressed tables, the reported [Innodb\\_buffer\\_pool\\_pages\\_data](#page-146-1) value may be larger than [Innodb\\_buffer\\_pool\\_pages\\_total](#page-146-2) (Bug #59550)

<span id="page-146-9"></span>• [Innodb\\_buffer\\_pool\\_read\\_ahead](#page-146-9)

The number of pages read into the InnoDB buffer pool by the read-ahead background thread.

<span id="page-147-0"></span>• [Innodb\\_buffer\\_pool\\_read\\_ahead\\_evicted](#page-147-0)

The number of pages read into the InnoDB buffer pool by the read-ahead background thread that were subsequently evicted without having been accessed by queries.

<span id="page-147-1"></span>• [Innodb\\_buffer\\_pool\\_read\\_ahead\\_rnd](#page-147-1)

The number of "random" read-aheads initiated by InnoDB. This happens when a query scans a large portion of a table but in random order.

<span id="page-147-2"></span>• [Innodb\\_buffer\\_pool\\_read\\_requests](#page-147-2)

The number of logical read requests.

<span id="page-147-3"></span>• [Innodb\\_buffer\\_pool\\_reads](#page-147-3)

The number of logical reads that InnoDB could not satisfy from the buffer pool, and had to read directly from disk.

<span id="page-147-4"></span>• [Innodb\\_buffer\\_pool\\_resize\\_status](#page-147-4)

The status of an operation to resize the InnoDB buffer pool dynamically, triggered by setting the innodb\_buffer\_pool\_size parameter dynamically. The innodb\_buffer\_pool\_size parameter is dynamic, which allows you to resize the buffer pool without restarting the server. See Configuring InnoDB Buffer Pool Size Online for related information.

<span id="page-147-5"></span>• [Innodb\\_buffer\\_pool\\_resize\\_status\\_code](#page-147-5)

Reports status codes for tracking online buffer pool resizing operations. Each status code represents a stage in a resizing operation. Status codes include:

- 0: No Resize operation in progress
- 1: Starting Resize
- 2: Disabling AHI (Adaptive Hash Index)
- 3: Withdrawing Blocks
- 4: Acquiring Global Lock
- 5: Resizing Pool
- 6: Resizing Hash
- 7: Resizing Failed

You can use this status variable in conjunction with

[Innodb\\_buffer\\_pool\\_resize\\_status\\_progress](#page-147-6) to track the progress of each stage of a resizing operation. The [Innodb\\_buffer\\_pool\\_resize\\_status\\_progress](#page-147-6) variable reports a percentage value indicating the progress of the current stage.

For more information, see Monitoring Online Buffer Pool Resizing Progress.

<span id="page-147-6"></span>• [Innodb\\_buffer\\_pool\\_resize\\_status\\_progress](#page-147-6)

Reports a percentage value indicating the progress of the current stage of an online buffer pool resizing operation. This variable is used in conjunction with

[Innodb\\_buffer\\_pool\\_resize\\_status\\_code](#page-147-5), which reports a status code indicating the current stage of an online buffer pool resizing operation.

The percentage value is updated after each buffer pool instance is processed. As the status code (reported by [Innodb\\_buffer\\_pool\\_resize\\_status\\_code](#page-147-5)) changes from one status to another, the percentage value is reset to 0.

For related information, see Monitoring Online Buffer Pool Resizing Progress.

<span id="page-148-0"></span>• [Innodb\\_buffer\\_pool\\_wait\\_free](#page-148-0)

Normally, writes to the InnoDB buffer pool happen in the background. When InnoDB needs to read or create a page and no clean pages are available, InnoDB flushes some dirty pages first and waits for that operation to finish. This counter counts instances of these waits. If innodb\_buffer\_pool\_size has been set properly, this value should be small.

<span id="page-148-1"></span>• [Innodb\\_buffer\\_pool\\_write\\_requests](#page-148-1)

The number of writes done to the InnoDB buffer pool.

<span id="page-148-2"></span>• [Innodb\\_data\\_fsyncs](#page-148-2)

The number of fsync() operations so far. The frequency of fsync() calls is influenced by the setting of the innodb\_flush\_method configuration option.

Counts the number of fdatasync() operations if innodb\_use\_fdatasync is enabled.

<span id="page-148-3"></span>• [Innodb\\_data\\_pending\\_fsyncs](#page-148-3)

The current number of pending fsync() operations. The frequency of fsync() calls is influenced by the setting of the innodb\_flush\_method configuration option.

<span id="page-148-4"></span>• [Innodb\\_data\\_pending\\_reads](#page-148-4)

The current number of pending reads.

<span id="page-148-5"></span>• [Innodb\\_data\\_pending\\_writes](#page-148-5)

The current number of pending writes.

<span id="page-148-6"></span>• [Innodb\\_data\\_read](#page-148-6)

The amount of data read since the server was started (in bytes).

<span id="page-148-7"></span>• [Innodb\\_data\\_reads](#page-148-7)

The total number of data reads (OS file reads).

<span id="page-148-8"></span>• [Innodb\\_data\\_writes](#page-148-8)

The total number of data writes.

<span id="page-148-9"></span>• [Innodb\\_data\\_written](#page-148-9)

The amount of data written so far, in bytes.

<span id="page-148-10"></span>• [Innodb\\_dblwr\\_pages\\_written](#page-148-10)

The number of pages that have been written to the doublewrite buffer. See Section 17.11.1, "InnoDB Disk I/O".

<span id="page-149-0"></span>• [Innodb\\_dblwr\\_writes](#page-149-0)

The number of doublewrite operations that have been performed. See Section 17.11.1, "InnoDB Disk I/O".

<span id="page-149-1"></span>• [Innodb\\_have\\_atomic\\_builtins](#page-149-1)

Indicates whether the server was built with atomic instructions.

<span id="page-149-2"></span>• [Innodb\\_log\\_waits](#page-149-2)

The number of times that the log buffer was too small and a wait was required for it to be flushed before continuing.

<span id="page-149-3"></span>• [Innodb\\_log\\_write\\_requests](#page-149-3)

The number of write requests for the InnoDB redo log.

<span id="page-149-4"></span>• [Innodb\\_log\\_writes](#page-149-4)

The number of physical writes to the InnoDB redo log file.

<span id="page-149-5"></span>• [Innodb\\_num\\_open\\_files](#page-149-5)

The number of files InnoDB currently holds open.

<span id="page-149-6"></span>• [Innodb\\_os\\_log\\_fsyncs](#page-149-6)

The number of fsync() writes done to the InnoDB redo log files.

<span id="page-149-7"></span>• [Innodb\\_os\\_log\\_pending\\_fsyncs](#page-149-7)

The number of pending fsync() operations for the InnoDB redo log files.

<span id="page-149-8"></span>• [Innodb\\_os\\_log\\_pending\\_writes](#page-149-8)

The number of pending writes to the InnoDB redo log files.

<span id="page-149-9"></span>• [Innodb\\_os\\_log\\_written](#page-149-9)

The number of bytes written to the InnoDB redo log files.

<span id="page-149-10"></span>• [Innodb\\_page\\_size](#page-149-10)

InnoDB page size (default 16KB). Many values are counted in pages; the page size enables them to be easily converted to bytes.

<span id="page-149-11"></span>• [Innodb\\_pages\\_created](#page-149-11)

The number of pages created by operations on InnoDB tables.

<span id="page-149-12"></span>• [Innodb\\_pages\\_read](#page-149-12)

The number of pages read from the InnoDB buffer pool by operations on InnoDB tables.

<span id="page-149-13"></span>• [Innodb\\_pages\\_written](#page-149-13)

The number of pages written by operations on InnoDB tables.

<span id="page-149-14"></span>• [Innodb\\_redo\\_log\\_enabled](#page-149-14)

Whether redo logging is enabled or disabled. See Disabling Redo Logging.

<span id="page-149-15"></span>• [Innodb\\_redo\\_log\\_capacity\\_resized](#page-149-15)

The total redo log capacity for all redo log files, in bytes, after the last completed capacity resize operation. The value includes ordinary and spare redo log files.

If there is no pending resize down operation, [Innodb\\_redo\\_log\\_capacity\\_resized](#page-149-15) should be equal to the innodb\_redo\_log\_capacity setting if it's used, or it's ((innodb\_log\_files\_in\_group \* innodb\_log\_file\_size)) if those are used instead. See the innodb\_redo\_log\_capacity documentation for further clarification. Resize up operations are instantaneous.

For related information, see Section 17.6.5, "Redo Log".

<span id="page-150-0"></span>• [Innodb\\_redo\\_log\\_checkpoint\\_lsn](#page-150-0)

The redo log checkpoint LSN. For related information, see Section 17.6.5, "Redo Log".

<span id="page-150-1"></span>• [Innodb\\_redo\\_log\\_current\\_lsn](#page-150-1)

The current LSN represents the last written position in the redo log buffer. InnoDB writes data to the redo log buffer inside the MySQL process before requesting that the operating system write the data to the current redo log file. For related information, see Section 17.6.5, "Redo Log".

<span id="page-150-2"></span>• [Innodb\\_redo\\_log\\_flushed\\_to\\_disk\\_lsn](#page-150-2)

The flushed-to-disk LSN. InnoDB first writes data to the redo log and then requests that the operating system flush the data to disk. The flushed-to-disk LSN represents the last position in the redo log that InnoDB knows has been flushed to disk. For related information, see Section 17.6.5, "Redo Log".

<span id="page-150-3"></span>• [Innodb\\_redo\\_log\\_logical\\_size](#page-150-3)

A data size value, in bytes, representing the LSN range containing in-use redo log data, spanning from the oldest block required by redo log consumers to the latest written block. For related information, see Section 17.6.5, "Redo Log".

<span id="page-150-4"></span>• [Innodb\\_redo\\_log\\_physical\\_size](#page-150-4)

The amount of disk space in bytes currently consumed by all redo log files on disk, excluding spare redo log files. For related information, see Section 17.6.5, "Redo Log".

<span id="page-150-5"></span>• [Innodb\\_redo\\_log\\_read\\_only](#page-150-5)

Whether the redo log is read-only.

<span id="page-150-6"></span>• [Innodb\\_redo\\_log\\_resize\\_status](#page-150-6)

The redo log resize status indicating the current state of the redo log capacity resize mechanism. Possible values include:

- OK: There are no issues and no pending redo log capacity resize operations.
- Resizing down: A resize down operation is in progress.

A resize up operation is instantaneous and therefore has no pending status.

<span id="page-150-7"></span>• [Innodb\\_redo\\_log\\_uuid](#page-150-7)

The redo log UUID.

<span id="page-150-8"></span>• [Innodb\\_row\\_lock\\_current\\_waits](#page-150-8)

The number of row locks currently waited for by operations on InnoDB tables.

<span id="page-150-9"></span>• [Innodb\\_row\\_lock\\_time](#page-150-9)

The total time spent in acquiring row locks for InnoDB tables, in milliseconds.

<span id="page-151-0"></span>• [Innodb\\_row\\_lock\\_time\\_avg](#page-151-0)

The average time to acquire a row lock for InnoDB tables, in milliseconds.

<span id="page-151-1"></span>• [Innodb\\_row\\_lock\\_time\\_max](#page-151-1)

The maximum time to acquire a row lock for InnoDB tables, in milliseconds.

<span id="page-151-2"></span>• [Innodb\\_row\\_lock\\_waits](#page-151-2)

The number of times operations on InnoDB tables had to wait for a row lock.

<span id="page-151-3"></span>• [Innodb\\_rows\\_deleted](#page-151-3)

The number of rows deleted from InnoDB tables.

<span id="page-151-4"></span>• [Innodb\\_rows\\_inserted](#page-151-4)

The number of rows inserted into InnoDB tables.

<span id="page-151-5"></span>• [Innodb\\_rows\\_read](#page-151-5)

The number of rows read from InnoDB tables.

<span id="page-151-6"></span>• [Innodb\\_rows\\_updated](#page-151-6)

The estimated number of rows updated in InnoDB tables.

![](_page_151_Picture_16.jpeg)

#### **Note**

This value is not meant to be 100% accurate. For an accurate (but more expensive) result, use ROW\_COUNT().

<span id="page-151-7"></span>• [Innodb\\_system\\_rows\\_deleted](#page-151-7)

The number of rows deleted from InnoDB tables belonging to system-created schemas.

<span id="page-151-8"></span>• [Innodb\\_system\\_rows\\_inserted](#page-151-8)

The number of rows inserted into InnoDB tables belonging to system-created schemas.

<span id="page-151-9"></span>• [Innodb\\_system\\_rows\\_updated](#page-151-9)

The number of rows updated in InnoDB tables belonging to system-created schemas.

<span id="page-151-10"></span>• [Innodb\\_system\\_rows\\_read](#page-151-10)

The number of rows read from InnoDB tables belonging to system-created schemas.

<span id="page-151-11"></span>• [Innodb\\_truncated\\_status\\_writes](#page-151-11)

The number of times output from the SHOW ENGINE INNODB STATUS statement has been truncated.

<span id="page-151-12"></span>• [Innodb\\_undo\\_tablespaces\\_active](#page-151-12)

The number of active undo tablespaces. Includes both implicit (InnoDB-created) and explicit (usercreated) undo tablespaces. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-151-13"></span>• [Innodb\\_undo\\_tablespaces\\_explicit](#page-151-13)

The number of user-created undo tablespaces. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-152-5"></span>• [Innodb\\_undo\\_tablespaces\\_implicit](#page-152-5)

The number of undo tablespaces created by InnoDB. Two default undo tablespaces are created by InnoDB when the MySQL instance is initialized. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-152-6"></span>• [Innodb\\_undo\\_tablespaces\\_total](#page-152-6)

The total number of undo tablespaces. Includes both implicit (InnoDB-created) and explicit (usercreated) undo tablespaces, active and inactive. For information about undo tablespaces, see Section 17.6.3.4, "Undo Tablespaces".

<span id="page-152-7"></span>• [Key\\_blocks\\_not\\_flushed](#page-152-7)

The number of key blocks in the MyISAM key cache that have changed but have not yet been flushed to disk.

<span id="page-152-4"></span>• [Key\\_blocks\\_unused](#page-152-4)

The number of unused blocks in the MyISAM key cache. You can use this value to determine how much of the key cache is in use; see the discussion of [key\\_buffer\\_size](#page-6-1) in Section 7.1.8, "Server System Variables".

<span id="page-152-8"></span>• [Key\\_blocks\\_used](#page-152-8)

The number of used blocks in the MyISAM key cache. This value is a high-water mark that indicates the maximum number of blocks that have ever been in use at one time.

<span id="page-152-0"></span>• [Key\\_read\\_requests](#page-152-0)

The number of requests to read a key block from the MyISAM key cache.

<span id="page-152-1"></span>• [Key\\_reads](#page-152-1)

The number of physical reads of a key block from disk into the MyISAM key cache. If [Key\\_reads](#page-152-1) is large, then your [key\\_buffer\\_size](#page-6-1) value is probably too small. The cache miss rate can be calculated as [Key\\_reads](#page-152-1)/[Key\\_read\\_requests](#page-152-0).

<span id="page-152-2"></span>• [Key\\_write\\_requests](#page-152-2)

The number of requests to write a key block to the MyISAM key cache.

<span id="page-152-3"></span>• [Key\\_writes](#page-152-3)

The number of physical writes of a key block from the MyISAM key cache to disk.

<span id="page-152-9"></span>• [Last\\_query\\_cost](#page-152-9)

The total cost of the last compiled query as computed by the query optimizer. This is useful for comparing the cost of different query plans for the same query. The default value of 0 means that no query has been compiled yet. The default value is 0. [Last\\_query\\_cost](#page-152-9) has session scope.

This variable shows the cost of queries that have multiple query blocks, summing the cost estimates of each query block, estimating how many times non-cacheable subqueries are executed, and multiplying the cost of those query blocks by the number of subquery executions.

<span id="page-153-0"></span>• [Last\\_query\\_partial\\_plans](#page-153-0)

The number of iterations the query optimizer made in execution plan construction for the previous query.

Last\_query\_partial\_plans has session scope.

<span id="page-153-1"></span>• [Locked\\_connects](#page-153-1)

The number of attempts to connect to locked user accounts. For information about account locking and unlocking, see Section 8.2.20, "Account Locking".

<span id="page-153-2"></span>• [Max\\_execution\\_time\\_exceeded](#page-153-2)

The number of SELECT statements for which the execution timeout was exceeded.

<span id="page-153-3"></span>• [Max\\_execution\\_time\\_set](#page-153-3)

The number of SELECT statements for which a nonzero execution timeout was set. This includes statements that include a nonzero MAX\_EXECUTION\_TIME optimizer hint, and statements that include no such hint but execute while the timeout indicated by the [max\\_execution\\_time](#page-23-0) system variable is nonzero.

<span id="page-153-4"></span>• [Max\\_execution\\_time\\_set\\_failed](#page-153-4)

The number of SELECT statements for which the attempt to set an execution timeout failed.

<span id="page-153-5"></span>• [Max\\_used\\_connections](#page-153-5)

The maximum number of connections that have been in use simultaneously since the server started.

<span id="page-153-6"></span>• [Max\\_used\\_connections\\_time](#page-153-6)

The time at which [Max\\_used\\_connections](#page-153-5) reached its current value.

<span id="page-153-7"></span>• [Not\\_flushed\\_delayed\\_rows](#page-153-7)

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed in a future release.

<span id="page-153-8"></span>• [mecab\\_charset](#page-153-8)

The character set currently used by the MeCab full-text parser plugin. For related information, see Section 14.9.9, "MeCab Full-Text Parser Plugin".

<span id="page-153-9"></span>• [Ongoing\\_anonymous\\_transaction\\_count](#page-153-9)

Shows the number of ongoing transactions which have been marked as anonymous. This can be used to ensure that no further transactions are waiting to be processed.

<span id="page-153-10"></span>• [Ongoing\\_anonymous\\_gtid\\_violating\\_transaction\\_count](#page-153-10)

This status variable is only available in debug builds. Shows the number of ongoing transactions which use gtid\_next=ANONYMOUS and that violate GTID consistency.

<span id="page-153-11"></span>• [Ongoing\\_automatic\\_gtid\\_violating\\_transaction\\_count](#page-153-11)

This status variable is only available in debug builds. Shows the number of ongoing transactions which use gtid\_next=AUTOMATIC and that violate GTID consistency.

<span id="page-154-1"></span>• [Open\\_files](#page-154-1)

The number of files that are open. This count includes regular files opened by the server. It does not include other types of files such as sockets or pipes. Also, the count does not include files that storage engines open using their own internal functions rather than asking the server level to do so.

<span id="page-154-2"></span>• [Open\\_streams](#page-154-2)

The number of streams that are open (used mainly for logging).

<span id="page-154-3"></span>• [Open\\_table\\_definitions](#page-154-3)

The number of cached table definitions.

<span id="page-154-4"></span>• [Open\\_tables](#page-154-4)

The number of tables that are open.

<span id="page-154-5"></span>• [Opened\\_files](#page-154-5)

The number of files that have been opened with my\_open() (a mysys library function). Parts of the server that open files without using this function do not increment the count.

<span id="page-154-6"></span>• [Opened\\_table\\_definitions](#page-154-6)

The number of table definitions that have been cached.

<span id="page-154-0"></span>• [Opened\\_tables](#page-154-0)

The number of tables that have been opened. If [Opened\\_tables](#page-154-0) is big, your [table\\_open\\_cache](#page-86-0) value is probably too small.

• Performance\_schema\_xxx

Performance Schema status variables are listed in Section 29.16, "Performance Schema Status Variables". These variables provide information about instrumentation that could not be loaded or created due to memory constraints.

<span id="page-154-7"></span>• [Prepared\\_stmt\\_count](#page-154-7)

The current number of prepared statements. (The maximum number of statements is given by the [max\\_prepared\\_stmt\\_count](#page-25-2) system variable.)

<span id="page-154-8"></span>• [Queries](#page-154-8)

The number of statements executed by the server. This variable includes statements executed within stored programs, unlike the [Questions](#page-154-9) variable. It does not count COM\_PING or COM\_STATISTICS commands.

The discussion at the beginning of this section indicates how to relate this statement-counting status variable to other such variables.

<span id="page-154-9"></span>• [Questions](#page-154-9)

The number of statements executed by the server. This includes only statements sent to the server by clients and not statements executed within stored programs, unlike the [Queries](#page-154-8) variable. This variable does not count COM\_PING, COM\_STATISTICS, COM\_STMT\_PREPARE, COM\_STMT\_CLOSE, or COM\_STMT\_RESET commands.

The discussion at the beginning of this section indicates how to relate this statement-counting status variable to other such variables.

<span id="page-154-10"></span>• [Replica\\_open\\_temp\\_tables](#page-154-10)

[Replica\\_open\\_temp\\_tables](#page-154-10) shows the number of temporary tables that the replication SQL thread currently has open. If the value is greater than zero, it is not safe to shut down the replica; see Section 19.5.1.31, "Replication and Temporary Tables". This variable reports the total count of open temporary tables for all replication channels.

<span id="page-155-0"></span>• [Resource\\_group\\_supported](#page-155-0)

Indicates whether the resource group feature is supported.

On some platforms or MySQL server configurations, resource groups are unavailable or have limitations. In particular, Linux systems might require a manual step for some installation methods. For details, see [Resource Group Restrictions.](#page-199-0)

<span id="page-155-1"></span>• [Rpl\\_semi\\_sync\\_master\\_clients](#page-155-1)

The number of semisynchronous replicas.

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_clients](#page-156-0).

<span id="page-155-2"></span>• [Rpl\\_semi\\_sync\\_master\\_net\\_avg\\_wait\\_time](#page-155-2)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_net\\_avg\\_wait\\_time](#page-156-1).

<span id="page-155-3"></span>• [Rpl\\_semi\\_sync\\_master\\_net\\_wait\\_time](#page-155-3)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_net\\_wait\\_time](#page-156-2).

<span id="page-155-4"></span>• [Rpl\\_semi\\_sync\\_master\\_net\\_waits](#page-155-4)

The total number of times the source waited for replica replies.

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_net\\_waits](#page-156-3).

<span id="page-155-5"></span>• [Rpl\\_semi\\_sync\\_master\\_no\\_times](#page-155-5)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_no\\_times](#page-156-4).

<span id="page-155-6"></span>• [Rpl\\_semi\\_sync\\_master\\_no\\_tx](#page-155-6)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_no\\_tx](#page-156-5).

<span id="page-155-7"></span>• [Rpl\\_semi\\_sync\\_master\\_status](#page-155-7)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_status](#page-156-6).

<span id="page-155-8"></span>• [Rpl\\_semi\\_sync\\_master\\_timefunc\\_failures](#page-155-8)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_timefunc\\_failures](#page-156-7).

<span id="page-155-9"></span>• [Rpl\\_semi\\_sync\\_master\\_tx\\_avg\\_wait\\_time](#page-155-9)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_tx\\_avg\\_wait\\_time](#page-157-0).

<span id="page-155-10"></span>• [Rpl\\_semi\\_sync\\_master\\_tx\\_wait\\_time](#page-155-10)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_tx\\_wait\\_time](#page-157-1).

<span id="page-155-11"></span>• [Rpl\\_semi\\_sync\\_master\\_tx\\_waits](#page-155-11)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_tx\\_waits](#page-157-2).

<span id="page-155-12"></span>• [Rpl\\_semi\\_sync\\_master\\_wait\\_pos\\_backtraverse](#page-155-12)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_wait\\_pos\\_backtraverse](#page-157-3).

<span id="page-156-8"></span>• [Rpl\\_semi\\_sync\\_master\\_wait\\_sessions](#page-156-8)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_wait\\_sessions](#page-157-4).

<span id="page-156-9"></span>• [Rpl\\_semi\\_sync\\_master\\_yes\\_tx](#page-156-9)

Deprecated synonym for [Rpl\\_semi\\_sync\\_source\\_yes\\_tx](#page-157-5).

<span id="page-156-0"></span>• [Rpl\\_semi\\_sync\\_source\\_clients](#page-156-0)

The number of semisynchronous replicas.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-1"></span>• [Rpl\\_semi\\_sync\\_source\\_net\\_avg\\_wait\\_time](#page-156-1)

The average time in microseconds the source waited for a replica reply. This variable is always 0, and is deprecated; expect it to be removed in a future version.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-2"></span>• [Rpl\\_semi\\_sync\\_source\\_net\\_wait\\_time](#page-156-2)

The total time in microseconds the source waited for replica replies. This variable is always 0, and is deprecated; expect it to be removed in a future version.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-3"></span>• [Rpl\\_semi\\_sync\\_source\\_net\\_waits](#page-156-3)

The total number of times the source waited for replica replies.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-4"></span>• [Rpl\\_semi\\_sync\\_source\\_no\\_times](#page-156-4)

The number of times the source turned off semisynchronous replication.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-5"></span>• [Rpl\\_semi\\_sync\\_source\\_no\\_tx](#page-156-5)

The number of commits that were not acknowledged successfully by a replica.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-6"></span>• [Rpl\\_semi\\_sync\\_source\\_status](#page-156-6)

Whether semisynchronous replication currently is operational on the source. The value is ON if the plugin has been enabled and a commit acknowledgment has occurred. It is OFF if the plugin is not enabled or the source has fallen back to asynchronous replication due to commit acknowledgment timeout.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-156-7"></span>• [Rpl\\_semi\\_sync\\_source\\_timefunc\\_failures](#page-156-7)

The number of times the source failed when calling time functions such as gettimeofday().

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-0"></span>• [Rpl\\_semi\\_sync\\_source\\_tx\\_avg\\_wait\\_time](#page-157-0)

The average time in microseconds the source waited for each transaction.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-1"></span>• [Rpl\\_semi\\_sync\\_source\\_tx\\_wait\\_time](#page-157-1)

The total time in microseconds the source waited for transactions.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-2"></span>• [Rpl\\_semi\\_sync\\_source\\_tx\\_waits](#page-157-2)

The total number of times the source waited for transactions.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-3"></span>• [Rpl\\_semi\\_sync\\_source\\_wait\\_pos\\_backtraverse](#page-157-3)

The total number of times the source waited for an event with binary coordinates lower than events waited for previously. This can occur when the order in which transactions start waiting for a reply is different from the order in which their binary log events are written.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-4"></span>• [Rpl\\_semi\\_sync\\_source\\_wait\\_sessions](#page-157-4)

The number of sessions currently waiting for replica replies.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-5"></span>• [Rpl\\_semi\\_sync\\_source\\_yes\\_tx](#page-157-5)

The number of commits that were acknowledged successfully by a replica.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-6"></span>• [Rpl\\_semi\\_sync\\_replica\\_status](#page-157-6)

Shows whether semisynchronous replication is currently operational on the replica. This is ON if the plugin has been enabled and the replication I/O (receiver) thread is running, OFF otherwise.

Available when the rpl\_semi\_sync\_source plugin (semisync\_source.so library) is installed on the source.

<span id="page-157-7"></span>• [Rpl\\_semi\\_sync\\_slave\\_status](#page-157-7)

Deprecated synonym for [Rpl\\_semi\\_sync\\_replica\\_status](#page-157-6).

<span id="page-157-8"></span>• [Rsa\\_public\\_key](#page-157-8)

The value of this variable is the public key used by the sha256\_password (deprecated) authentication plugin for RSA key pair-based password exchange. The value is nonempty only if the server successfully initializes the private and public keys in the files named by the [sha256\\_password\\_private\\_key\\_path](#page-65-0) and [sha256\\_password\\_public\\_key\\_path](#page-65-2) system variables. The value of [Rsa\\_public\\_key](#page-157-8) comes from the latter file.

For information about sha256\_password, see Section 8.4.1.3, "SHA-256 Pluggable Authentication".

• [Secondary\\_engine\\_execution\\_count](https://dev.mysql.com/doc/heatwave/en/heatwave-status-variables.md#statvar_Secondary_engine_execution_count)

For use with MySQL HeatWave only. See [Status Variables](https://dev.mysql.com/doc/heatwave/en/heatwave-status-variables.md), for more information.

<span id="page-158-3"></span>• [Select\\_full\\_join](#page-158-3)

The number of joins that perform table scans because they do not use indexes. If this value is not 0, you should carefully check the indexes of your tables.

<span id="page-158-4"></span>• [Select\\_full\\_range\\_join](#page-158-4)

The number of joins that used a range search on a reference table.

<span id="page-158-5"></span>• [Select\\_range](#page-158-5)

The number of joins that used ranges on the first table. This is normally not a critical issue even if the value is quite large.

<span id="page-158-6"></span>• [Select\\_range\\_check](#page-158-6)

The number of joins without keys that check for key usage after each row. If this is not 0, you should carefully check the indexes of your tables.

<span id="page-158-7"></span>• [Select\\_scan](#page-158-7)

The number of joins that did a full scan of the first table.

<span id="page-158-8"></span>• [Slave\\_open\\_temp\\_tables](#page-158-8)

Deprecated alias for [Replica\\_open\\_temp\\_tables](#page-154-10).

<span id="page-158-9"></span>• [Slave\\_rows\\_last\\_search\\_algorithm\\_used](#page-158-9)

Deprecated alias for [Replica\\_rows\\_last\\_search\\_algorithm\\_used](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.md#statvar_Replica_rows_last_search_algorithm_used).

<span id="page-158-1"></span>• [Slow\\_launch\\_threads](#page-158-1)

The number of threads that have taken more than [slow\\_launch\\_time](#page-69-2) seconds to create.

<span id="page-158-0"></span>• [Slow\\_queries](#page-158-0)

The number of queries that have taken more than [long\\_query\\_time](#page-16-2) seconds. This counter increments regardless of whether the slow query log is enabled. For information about that log, see Section 7.4.5, "The Slow Query Log".

<span id="page-158-2"></span>• [Sort\\_merge\\_passes](#page-158-2)

The number of merge passes that the sort algorithm has had to do. If this value is large, you should consider increasing the value of the [sort\\_buffer\\_size](#page-70-0) system variable.

<span id="page-158-10"></span>• [Sort\\_range](#page-158-10)

The number of sorts that were done using ranges.

<span id="page-159-0"></span>• [Sort\\_rows](#page-159-0)

The number of sorted rows.

<span id="page-159-1"></span>• [Sort\\_scan](#page-159-1)

The number of sorts that were done by scanning the table.

<span id="page-159-2"></span>• [Ssl\\_accept\\_renegotiates](#page-159-2)

The number of negotiates needed to establish the connection.

<span id="page-159-3"></span>• [Ssl\\_accepts](#page-159-3)

The number of accepted SSL connections.

<span id="page-159-4"></span>• [Ssl\\_callback\\_cache\\_hits](#page-159-4)

The number of callback cache hits.

<span id="page-159-5"></span>• [Ssl\\_cipher](#page-159-5)

The current encryption cipher (empty for unencrypted connections).

<span id="page-159-6"></span>• [Ssl\\_cipher\\_list](#page-159-6)

The list of possible SSL ciphers (empty for non-SSL connections). If MySQL supports TLSv1.3, the value includes the possible TLSv1.3 ciphersuites. See Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers".

<span id="page-159-7"></span>• [Ssl\\_client\\_connects](#page-159-7)

The number of SSL connection attempts to an SSL-enabled replication source server.

<span id="page-159-8"></span>• [Ssl\\_connect\\_renegotiates](#page-159-8)

The number of negotiates needed to establish the connection to an SSL-enabled replication source server.

<span id="page-159-9"></span>• [Ssl\\_ctx\\_verify\\_depth](#page-159-9)

The SSL context verification depth (how many certificates in the chain are tested).

<span id="page-159-10"></span>• [Ssl\\_ctx\\_verify\\_mode](#page-159-10)

The SSL context verification mode.

<span id="page-159-11"></span>• [Ssl\\_default\\_timeout](#page-159-11)

The default SSL timeout.

<span id="page-159-12"></span>• [Ssl\\_finished\\_accepts](#page-159-12)

The number of successful SSL connections to the server.

<span id="page-159-13"></span>• [Ssl\\_finished\\_connects](#page-159-13)

The number of successful replica connections to an SSL-enabled replication source server.

<span id="page-159-14"></span>• [Ssl\\_server\\_not\\_after](#page-159-14)

The last date for which the SSL certificate is valid. To check SSL certificate expiration information, use this statement:

```
mysql> SHOW STATUS LIKE 'Ssl_server_not%';
+-----------------------+--------------------------+
| Variable_name | Value |
+-----------------------+--------------------------+
| Ssl_server_not_after | Apr 28 14:16:39 2025 GMT |
| Ssl_server_not_before | May 1 14:16:39 2015 GMT |
+-----------------------+--------------------------+
```

<span id="page-160-2"></span>• [Ssl\\_server\\_not\\_before](#page-160-2)

The first date for which the SSL certificate is valid.

<span id="page-160-3"></span>• [Ssl\\_session\\_cache\\_hits](#page-160-3)

The number of SSL session cache hits.

<span id="page-160-4"></span>• [Ssl\\_session\\_cache\\_misses](#page-160-4)

The number of SSL session cache misses.

<span id="page-160-0"></span>• [Ssl\\_session\\_cache\\_mode](#page-160-0)

The SSL session cache mode. When the value of the [ssl\\_session\\_cache\\_mode](#page-80-1) server variable is ON, the value of the [Ssl\\_session\\_cache\\_mode](#page-160-0) status variable is SERVER.

<span id="page-160-5"></span>• [Ssl\\_session\\_cache\\_overflows](#page-160-5)

The number of SSL session cache overflows.

<span id="page-160-6"></span>• [Ssl\\_session\\_cache\\_size](#page-160-6)

The SSL session cache size.

<span id="page-160-1"></span>• [Ssl\\_session\\_cache\\_timeout](#page-160-1)

The timeout value in seconds of SSL sessions in the cache.

<span id="page-160-7"></span>• [Ssl\\_session\\_cache\\_timeouts](#page-160-7)

The number of SSL session cache timeouts.

<span id="page-160-8"></span>• [Ssl\\_sessions\\_reused](#page-160-8)

This is equal to 0 if TLS was not used in the current MySQL session, or if a TLS session has not been reused; otherwise it is equal to 1.

Ssl\_sessions\_reused has session scope.

<span id="page-160-9"></span>• [Ssl\\_used\\_session\\_cache\\_entries](#page-160-9)

How many SSL session cache entries were used.

<span id="page-160-10"></span>• [Ssl\\_verify\\_depth](#page-160-10)

The verification depth for replication SSL connections.

<span id="page-160-11"></span>• [Ssl\\_verify\\_mode](#page-160-11)

The verification mode used by the server for a connection that uses SSL. The value is a bitmask; bits are defined in the openssl/ssl.h header file:

```
# define SSL_VERIFY_NONE 0x00
# define SSL_VERIFY_PEER 0x01
# define SSL_VERIFY_FAIL_IF_NO_PEER_CERT 0x02
# define SSL_VERIFY_CLIENT_ONCE 0x04
```

SSL\_VERIFY\_PEER indicates that the server asks for a client certificate. If the client supplies one, the server performs verification and proceeds only if verification is successful. SSL\_VERIFY\_CLIENT\_ONCE indicates that a request for the client certificate is performed only in the initial handshake.

<span id="page-161-0"></span>• [Ssl\\_version](#page-161-0)

The SSL protocol version of the connection (for example, TLSv1.2). If the connection is not encrypted, the value is empty.

<span id="page-161-1"></span>• [Table\\_locks\\_immediate](#page-161-1)

The number of times that a request for a table lock could be granted immediately.

<span id="page-161-2"></span>• [Table\\_locks\\_waited](#page-161-2)

The number of times that a request for a table lock could not be granted immediately and a wait was needed. If this is high and you have performance problems, you should first optimize your queries, and then either split your table or tables or use replication.

<span id="page-161-3"></span>• [Table\\_open\\_cache\\_hits](#page-161-3)

The number of hits for open tables cache lookups.

<span id="page-161-4"></span>• [Table\\_open\\_cache\\_misses](#page-161-4)

The number of misses for open tables cache lookups.

<span id="page-161-5"></span>• [Table\\_open\\_cache\\_overflows](#page-161-5)

The number of overflows for the open tables cache. This is the number of times, after a table is opened or closed, a cache instance has an unused entry and the size of the instance is larger than [table\\_open\\_cache](#page-86-0) / [table\\_open\\_cache\\_instances](#page-87-0).

<span id="page-161-6"></span>• [Tc\\_log\\_max\\_pages\\_used](#page-161-6)

For the memory-mapped implementation of the log that is used by mysqld when it acts as the transaction coordinator for recovery of internal XA transactions, this variable indicates the largest number of pages used for the log since the server started. If the product of [Tc\\_log\\_max\\_pages\\_used](#page-161-6) and [Tc\\_log\\_page\\_size](#page-161-7) is always significantly less than the log size, the size is larger than necessary and can be reduced. (The size is set by the --log-tcsize option. This variable is unused: It is unneeded for binary log-based recovery, and the memorymapped recovery log method is not used unless the number of storage engines that are capable of two-phase commit and that support XA transactions is greater than one. (InnoDB is the only applicable engine.)

<span id="page-161-7"></span>• [Tc\\_log\\_page\\_size](#page-161-7)

The page size used for the memory-mapped implementation of the XA recovery log. The default value is determined using getpagesize(). This variable is unused for the same reasons as described for [Tc\\_log\\_max\\_pages\\_used](#page-161-6).

<span id="page-161-8"></span>• [Tc\\_log\\_page\\_waits](#page-161-8)

For the memory-mapped implementation of the recovery log, this variable increments each time the server was not able to commit a transaction and had to wait for a free page in the log. If this value is large, you might want to increase the log size (with the --log-tc-size option). For binary log-based recovery, this variable increments each time the binary log cannot be closed because there are two-phase commits in progress. (The close operation waits until all such transactions are finished.)

<span id="page-161-9"></span>• [Telemetry\\_metrics\\_supported](#page-161-9)

Whether server telemetry metrics is supported.

For more information, see the Server telemetry metrics service section in the MySQL Source Code documentation.

<span id="page-162-2"></span>• [telemetry.live\\_sessions](#page-162-2)

Displays the current number of sessions instrumented with telemetry. This can be useful when unloading the Telemetry component, to monitor how many sessions are blocking the unload operation.

For more information, see the Server telemetry traces service section in the MySQL Source Code documentation and Chapter 35, Telemetry.

<span id="page-162-3"></span>• [Telemetry\\_traces\\_supported](#page-162-3)

Whether server telemetry traces is supported.

For more information, see the Server telemetry traces service section in the MySQL Source Code documentation.

<span id="page-162-4"></span>• [Threads\\_cached](#page-162-4)

The number of threads in the thread cache.

<span id="page-162-5"></span>• [Threads\\_connected](#page-162-5)

The number of currently open connections.

<span id="page-162-1"></span>• [Threads\\_created](#page-162-1)

The number of threads created to handle connections. If [Threads\\_created](#page-162-1) is big, you may want to increase the [thread\\_cache\\_size](#page-89-1) value. The cache miss rate can be calculated as [Threads\\_created](#page-162-1)/[Connections](#page-141-0).

<span id="page-162-6"></span>• [Threads\\_running](#page-162-6)

The number of threads that are not sleeping.

<span id="page-162-7"></span>• [Tls\\_library\\_version](#page-162-7)

The runtime version of the OpenSSL library that is in use for this MySQL instance.

<span id="page-162-8"></span>• [Tls\\_sni\\_server\\_name](#page-162-8)

The Server Name Indication (SNI) that is in use for this session, if specified by the client; otherwise, empty. SNI is an extension to the TLS protocol (OpenSSL must be compiled using TLS extensions for this status variable to function). The MySQL implementation of SNI represents the client-side only.

<span id="page-162-9"></span>• [Uptime](#page-162-9)

The number of seconds that the server has been up.

• [Uptime\\_since\\_flush\\_status](#page-162-10)

The number of seconds since the most recent FLUSH STATUS statement.

# <span id="page-162-10"></span><span id="page-162-0"></span>**7.1.11 Server SQL Modes**

The MySQL server can operate in different SQL modes, and can apply these modes differently for different clients, depending on the value of the [sql\\_mode](#page-73-0) system variable. DBAs can set the global SQL mode to match site server operating requirements, and each application can set its session SQL mode to its own requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it easier to use MySQL in different environments and to use MySQL together with other database servers.

- [Setting the SQL Mode](#page-163-0)
- [The Most Important SQL Modes](#page-164-0)
- [Full List of SQL Modes](#page-164-1)
- [Combination SQL Modes](#page-169-0)
- [Strict SQL Mode](#page-170-0)
- [Comparison of the IGNORE Keyword and Strict SQL Mode](#page-171-0)

For answers to questions often asked about server SQL modes in MySQL, see Section A.3, "MySQL 8.4 FAQ: Server SQL Mode".

When working with InnoDB tables, consider also the innodb\_strict\_mode system variable. It enables additional error checks for InnoDB tables.

# <span id="page-163-0"></span>**Setting the SQL Mode**

The default SQL mode in MySQL 8.4 includes these modes: [ONLY\\_FULL\\_GROUP\\_BY](#page-168-0), [STRICT\\_TRANS\\_TABLES](#page-169-1), [NO\\_ZERO\\_IN\\_DATE](#page-167-0), [NO\\_ZERO\\_DATE](#page-167-1), [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0), and [NO\\_ENGINE\\_SUBSTITUTION](#page-166-0).

To set the SQL mode at server startup, use the --sql-mode="modes" option on the command line, or sql-mode="modes" in an option file such as my.cnf (Unix operating systems) or my.ini (Windows). modes is a list of different modes separated by commas. To clear the SQL mode explicitly, set it to an empty string using --sql-mode="" on the command line, or sql-mode="" in an option file.

![](_page_163_Picture_14.jpeg)

# **Note**

MySQL installation programs may configure the SQL mode during the installation process.

If the SQL mode differs from the default or from what you expect, check for a setting in an option file that the server reads at startup.

To change the SQL mode at runtime, set the global or session [sql\\_mode](#page-73-0) system variable using a SET statement:

```
SET GLOBAL sql_mode = 'modes';
SET SESSION sql_mode = 'modes';
```

Setting the GLOBAL variable requires the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege) and affects the operation of all clients that connect from that time on. Setting the SESSION variable affects only the current client. Each client can change its session [sql\\_mode](#page-73-0) value at any time.

To determine the current global or session [sql\\_mode](#page-73-0) setting, select its value:

```
SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;
```

![](_page_163_Picture_23.jpeg)

#### **Important**

**SQL mode and user-defined partitioning.** Changing the server SQL mode after creating and inserting data into partitioned tables can cause major changes in the behavior of such tables, and could lead to loss or corruption of data. It is strongly recommended that you never change the SQL mode once you have created tables employing user-defined partitioning.

When replicating partitioned tables, differing SQL modes on the source and replica can also lead to problems. For best results, you should always use the same server SQL mode on the source and replica.

For more information, see Section 26.6, "Restrictions and Limitations on Partitioning".

## <span id="page-164-0"></span>**The Most Important SQL Modes**

The most important [sql\\_mode](#page-73-0) values are probably these:

• [ANSI](#page-169-2)

This mode changes syntax and behavior to conform more closely to standard SQL. It is one of the special [combination modes](#page-169-0) listed at the end of this section.

• [STRICT\\_TRANS\\_TABLES](#page-169-1)

If a value could not be inserted as given into a transactional table, abort the statement. For a nontransactional table, abort the statement if the value occurs in a single-row statement or the first row of a multiple-row statement. More details are given later in this section.

• [TRADITIONAL](#page-170-1)

Make MySQL behave like a "traditional" SQL database system. A simple description of this mode is "give an error instead of a warning" when inserting an incorrect value into a column. It is one of the special [combination modes](#page-169-0) listed at the end of this section.

![](_page_164_Picture_12.jpeg)

#### **Note**

With [TRADITIONAL](#page-170-1) mode enabled, an INSERT or UPDATE aborts as soon as an error occurs. If you are using a nontransactional storage engine, this may not be what you want because data changes made prior to the error may not be rolled back, resulting in a "partially done" update.

When this manual refers to "strict mode," it means a mode with either or both [STRICT\\_TRANS\\_TABLES](#page-169-1) or [STRICT\\_ALL\\_TABLES](#page-169-3) enabled.

# <span id="page-164-2"></span><span id="page-164-1"></span>**Full List of SQL Modes**

The following list describes all supported SQL modes:

• [ALLOW\\_INVALID\\_DATES](#page-164-2)

Do not perform full checking of dates. Check only that the month is in the range from 1 to 12 and the day is in the range from 1 to 31. This may be useful for Web applications that obtain year, month, and day in three different fields and store exactly what the user inserted, without date validation. This mode applies to DATE and DATETIME columns. It does not apply to TIMESTAMP columns, which always require a valid date.

With [ALLOW\\_INVALID\\_DATES](#page-164-2) disabled, the server requires that month and day values be legal, and not merely in the range 1 to 12 and 1 to 31, respectively. With strict mode disabled, invalid dates such as '2004-04-31' are converted to '0000-00-00' and a warning is generated. With strict mode enabled, invalid dates generate an error. To permit such dates, enable [ALLOW\\_INVALID\\_DATES](#page-164-2).

<span id="page-164-3"></span>• [ANSI\\_QUOTES](#page-164-3)

Treat " as an identifier quote character (like the ` quote character) and not as a string quote character. You can still use ` to quote identifiers with this mode enabled. With [ANSI\\_QUOTES](#page-164-3) enabled, you cannot use double quotation marks to quote literal strings because they are interpreted as identifiers.

<span id="page-165-0"></span>• [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0)

The [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0) mode affects handling of division by zero, which includes MOD(N,0). For data-change operations (INSERT, UPDATE), its effect also depends on whether strict SQL mode is enabled.

- If this mode is not enabled, division by zero inserts NULL and produces no warning.
- If this mode is enabled, division by zero inserts NULL and produces a warning.
- If this mode and strict mode are enabled, division by zero produces an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, division by zero inserts NULL and produces a warning.

For SELECT, division by zero returns NULL. Enabling [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0) causes a warning to be produced as well, regardless of whether strict mode is enabled.

[ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0) is deprecated. [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0) is not part of strict mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs if [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0) is enabled without also enabling strict mode or vice versa.

Because [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0) is deprecated, you should expect it to be removed in a future MySQL release as a separate mode name and its effect included in the effects of strict SQL mode.

<span id="page-165-1"></span>• [HIGH\\_NOT\\_PRECEDENCE](#page-165-1)

The precedence of the NOT operator is such that expressions such as NOT a BETWEEN b AND c are parsed as NOT (a BETWEEN b AND c). In some older versions of MySQL, the expression was parsed as (NOT a) BETWEEN b AND c. The old higher-precedence behavior can be obtained by enabling the [HIGH\\_NOT\\_PRECEDENCE](#page-165-1) SQL mode.

```
mysql> SET sql_mode = '';
mysql> SELECT NOT 1 BETWEEN -5 AND 5;
 -> 0
mysql> SET sql_mode = 'HIGH_NOT_PRECEDENCE';
mysql> SELECT NOT 1 BETWEEN -5 AND 5;
 -> 1
```

<span id="page-165-2"></span>• [IGNORE\\_SPACE](#page-165-2)

Permit spaces between a function name and the ( character. This causes built-in function names to be treated as reserved words. As a result, identifiers that are the same as function names must be quoted as described in Section 11.2, "Schema Object Names". For example, because there is a COUNT() function, the use of count as a table name in the following statement causes an error:

```
mysql> CREATE TABLE count (i INT);
ERROR 1064 (42000): You have an error in your SQL syntax
```

The table name should be quoted:

```
mysql> CREATE TABLE `count` (i INT);
```

```
Query OK, 0 rows affected (0.00 sec)
```

The [IGNORE\\_SPACE](#page-165-2) SQL mode applies to built-in functions, not to loadable functions or stored functions. It is always permissible to have spaces after a loadable function or stored function name, regardless of whether [IGNORE\\_SPACE](#page-165-2) is enabled.

For further discussion of [IGNORE\\_SPACE](#page-165-2), see Section 11.2.5, "Function Name Parsing and Resolution".

<span id="page-166-1"></span>• [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-166-1)

[NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-166-1) affects handling of AUTO\_INCREMENT columns. Normally, you generate the next sequence number for the column by inserting either NULL or 0 into it. [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-166-1) suppresses this behavior for 0 so that only NULL generates the next sequence number.

This mode can be useful if 0 has been stored in a table's AUTO\_INCREMENT column. (Storing 0 is not a recommended practice, by the way.) For example, if you dump the table with mysqldump and then reload it, MySQL normally generates new sequence numbers when it encounters the 0 values, resulting in a table with contents different from the one that was dumped. Enabling [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-166-1) before reloading the dump file solves this problem. For this reason, mysqldump automatically includes in its output a statement that enables [NO\\_AUTO\\_VALUE\\_ON\\_ZERO](#page-166-1).

<span id="page-166-2"></span>• [NO\\_BACKSLASH\\_ESCAPES](#page-166-2)

Enabling this mode disables the use of the backslash character (\) as an escape character within strings and identifiers. With this mode enabled, backslash becomes an ordinary character like any other, and the default escape sequence for LIKE expressions is changed so that no escape character is used.

<span id="page-166-3"></span>• [NO\\_DIR\\_IN\\_CREATE](#page-166-3)

When creating a table, ignore all INDEX DIRECTORY and DATA DIRECTORY directives. This option is useful on replica servers.

<span id="page-166-0"></span>• [NO\\_ENGINE\\_SUBSTITUTION](#page-166-0)

Control automatic substitution of the default storage engine when a statement such as CREATE TABLE or ALTER TABLE specifies a storage engine that is disabled or not compiled in.

By default, [NO\\_ENGINE\\_SUBSTITUTION](#page-166-0) is enabled.

Because storage engines can be pluggable at runtime, unavailable engines are treated the same way:

With [NO\\_ENGINE\\_SUBSTITUTION](#page-166-0) disabled, for CREATE TABLE the default engine is used and a warning occurs if the desired engine is unavailable. For ALTER TABLE, a warning occurs and the table is not altered.

With [NO\\_ENGINE\\_SUBSTITUTION](#page-166-0) enabled, an error occurs and the table is not created or altered if the desired engine is unavailable.

<span id="page-166-4"></span>• [NO\\_UNSIGNED\\_SUBTRACTION](#page-166-4)

Subtraction between integer values, where one is of type UNSIGNED, produces an unsigned result by default. If the result would otherwise have been negative, an error results:

```
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
ERROR 1690 (22003): BIGINT UNSIGNED value is out of range in '(cast(0 as unsigned) - 1)'
```

If the [NO\\_UNSIGNED\\_SUBTRACTION](#page-166-4) SQL mode is enabled, the result is negative:

```
mysql> SET sql_mode = 'NO_UNSIGNED_SUBTRACTION';
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
+-------------------------+
| CAST(0 AS UNSIGNED) - 1 |
+-------------------------+
| -1 |
+-------------------------+
```

If the result of such an operation is used to update an UNSIGNED integer column, the result is clipped to the maximum value for the column type, or clipped to 0 if [NO\\_UNSIGNED\\_SUBTRACTION](#page-166-4) is enabled. With strict SQL mode enabled, an error occurs and the column remains unchanged.

When [NO\\_UNSIGNED\\_SUBTRACTION](#page-166-4) is enabled, the subtraction result is signed, even if any operand is unsigned. For example, compare the type of column c2 in table t1 with that of column c2 in table t2:

```
mysql> SET sql_mode='';
mysql> CREATE TABLE test (c1 BIGINT UNSIGNED NOT NULL);
mysql> CREATE TABLE t1 SELECT c1 - 1 AS c2 FROM test;
mysql> DESCRIBE t1;
+-------+---------------------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+---------------------+------+-----+---------+-------+
| c2 | bigint(21) unsigned | NO | | 0 | |
+-------+---------------------+------+-----+---------+-------+
mysql> SET sql_mode='NO_UNSIGNED_SUBTRACTION';
mysql> CREATE TABLE t2 SELECT c1 - 1 AS c2 FROM test;
mysql> DESCRIBE t2;
+-------+------------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| c2 | bigint(21) | NO | | 0 | |
+-------+------------+------+-----+---------+-------+
```

This means that BIGINT UNSIGNED is not 100% usable in all contexts. See Section 14.10, "Cast Functions and Operators".

<span id="page-167-1"></span>• [NO\\_ZERO\\_DATE](#page-167-1)

The [NO\\_ZERO\\_DATE](#page-167-1) mode affects whether the server permits '0000-00-00' as a valid date. Its effect also depends on whether strict SQL mode is enabled.

- If this mode is not enabled, '0000-00-00' is permitted and inserts produce no warning.
- If this mode is enabled, '0000-00-00' is permitted and inserts produce a warning.
- If this mode and strict mode are enabled, '0000-00-00' is not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, '0000-00-00' is permitted and inserts produce a warning.

[NO\\_ZERO\\_DATE](#page-167-1) is deprecated. [NO\\_ZERO\\_DATE](#page-167-1) is not part of strict mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs if [NO\\_ZERO\\_DATE](#page-167-1) is enabled without also enabling strict mode or vice versa.

Because [NO\\_ZERO\\_DATE](#page-167-1) is deprecated, you should expect it to be removed in a future MySQL release as a separate mode name and its effect included in the effects of strict SQL mode.

<span id="page-167-0"></span>• [NO\\_ZERO\\_IN\\_DATE](#page-167-0)

The [NO\\_ZERO\\_IN\\_DATE](#page-167-0) mode affects whether the server permits dates in which the year part is nonzero but the month or day part is 0. (This mode affects dates such as '2010-00-01' or

'2010-01-00', but not '0000-00-00'. To control whether the server permits '0000-00-00', use the [NO\\_ZERO\\_DATE](#page-167-1) mode.) The effect of [NO\\_ZERO\\_IN\\_DATE](#page-167-0) also depends on whether strict SQL mode is enabled.

- If this mode is not enabled, dates with zero parts are permitted and inserts produce no warning.
- If this mode is enabled, dates with zero parts are inserted as '0000-00-00' and produce a warning.
- If this mode and strict mode are enabled, dates with zero parts are not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, dates with zero parts are inserted as '0000-00-00' and produce a warning.

[NO\\_ZERO\\_IN\\_DATE](#page-167-0) is deprecated. [NO\\_ZERO\\_IN\\_DATE](#page-167-0) is not part of strict mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs if [NO\\_ZERO\\_IN\\_DATE](#page-167-0) is enabled without also enabling strict mode or vice versa.

Because [NO\\_ZERO\\_IN\\_DATE](#page-167-0) is deprecated, you should expect it to be removed in a future MySQL release as a separate mode name and its effect included in the effects of strict SQL mode.

<span id="page-168-0"></span>• [ONLY\\_FULL\\_GROUP\\_BY](#page-168-0)

Reject queries for which the select list, HAVING condition, or ORDER BY list refer to nonaggregated columns that are neither named in the GROUP BY clause nor are functionally dependent on (uniquely determined by) GROUP BY columns.

A MySQL extension to standard SQL permits references in the HAVING clause to aliased expressions in the select list. The HAVING clause can refer to aliases regardless of whether [ONLY\\_FULL\\_GROUP\\_BY](#page-168-0) is enabled.

For additional discussion and examples, see Section 14.19.3, "MySQL Handling of GROUP BY".

<span id="page-168-1"></span>• [PAD\\_CHAR\\_TO\\_FULL\\_LENGTH](#page-168-1)

By default, trailing spaces are trimmed from CHAR column values on retrieval. If [PAD\\_CHAR\\_TO\\_FULL\\_LENGTH](#page-168-1) is enabled, trimming does not occur and retrieved CHAR values are padded to their full length. This mode does not apply to VARCHAR columns, for which trailing spaces are retained on retrieval.

![](_page_168_Picture_13.jpeg)

# **Note**

[PAD\\_CHAR\\_TO\\_FULL\\_LENGTH](#page-168-1) is deprecated. Expect it to be removed in a future version of MySQL.

```
mysql> CREATE TABLE t1 (c1 CHAR(10));
Query OK, 0 rows affected (0.37 sec)
mysql> INSERT INTO t1 (c1) VALUES('xy');
Query OK, 1 row affected (0.01 sec)
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT c1, CHAR_LENGTH(c1) FROM t1;
+------+-----------------+
| c1 | CHAR_LENGTH(c1) |
+------+-----------------+
| xy | 2 |
+------+-----------------+
1 row in set (0.00 sec)
mysql> SET sql_mode = 'PAD_CHAR_TO_FULL_LENGTH';
Query OK, 0 rows affected (0.00 sec)
```

```
mysql> SELECT c1, CHAR_LENGTH(c1) FROM t1;
+------------+-----------------+
| c1 | CHAR_LENGTH(c1) |
+------------+-----------------+
| xy | 10 |
+------------+-----------------+
1 row in set (0.00 sec)
```

<span id="page-169-4"></span>• [PIPES\\_AS\\_CONCAT](#page-169-4)

Treat || as a string concatenation operator (same as CONCAT()) rather than as a synonym for OR.

<span id="page-169-5"></span>• [REAL\\_AS\\_FLOAT](#page-169-5)

Treat REAL as a synonym for FLOAT. By default, MySQL treats REAL as a synonym for DOUBLE.

<span id="page-169-3"></span>• [STRICT\\_ALL\\_TABLES](#page-169-3)

Enable strict SQL mode for all storage engines. Invalid data values are rejected. For details, see [Strict SQL Mode](#page-170-0).

<span id="page-169-1"></span>• [STRICT\\_TRANS\\_TABLES](#page-169-1)

Enable strict SQL mode for transactional storage engines, and when possible for nontransactional storage engines. For details, see [Strict SQL Mode](#page-170-0).

<span id="page-169-6"></span>• [TIME\\_TRUNCATE\\_FRACTIONAL](#page-169-6)

Control whether rounding or truncation occurs when inserting a TIME, DATE, or TIMESTAMP value with a fractional seconds part into a column having the same type but fewer fractional digits. The default behavior is to use rounding. If this mode is enabled, truncation occurs instead. The following sequence of statements illustrates the difference:

```
CREATE TABLE t (id INT, tval TIME(1));
SET sql_mode='';
INSERT INTO t (id, tval) VALUES(1, 1.55);
SET sql_mode='TIME_TRUNCATE_FRACTIONAL';
INSERT INTO t (id, tval) VALUES(2, 1.55);
```

The resulting table contents look like this, where the first value has been subject to rounding and the second to truncation:

```
mysql> SELECT id, tval FROM t ORDER BY id;
+------+------------+
| id | tval |
+------+------------+
| 1 | 00:00:01.6 |
| 2 | 00:00:01.5 |
+------+------------+
```

See also Section 13.2.6, "Fractional Seconds in Time Values".

## <span id="page-169-0"></span>**Combination SQL Modes**

The following special modes are provided as shorthand for combinations of mode values from the preceding list.

<span id="page-169-2"></span>• [ANSI](#page-169-2)

```
Equivalent to REAL_AS_FLOAT, PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, and
ONLY_FULL_GROUP_BY.
```

[ANSI](#page-169-2) mode also causes the server to return an error for queries where a set function S with an outer reference S(outer\_ref) cannot be aggregated in the outer query against which the outer reference has been resolved. This is such a query:

```
SELECT * FROM t1 WHERE t1.a IN (SELECT MAX(t1.b) FROM t2 WHERE ...);
```

Here, MAX(t1.b) cannot aggregated in the outer query because it appears in the WHERE clause of that query. Standard SQL requires an error in this situation. If [ANSI](#page-169-2) mode is not enabled, the server treats S(outer\_ref) in such queries the same way that it would interpret S(const).

See Section 1.7, "MySQL Standards Compliance".

<span id="page-170-1"></span>• [TRADITIONAL](#page-170-1)

[TRADITIONAL](#page-170-1) is equivalent to [STRICT\\_TRANS\\_TABLES](#page-169-1), [STRICT\\_ALL\\_TABLES](#page-169-3), [NO\\_ZERO\\_IN\\_DATE](#page-167-0), [NO\\_ZERO\\_DATE](#page-167-1), [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0), and [NO\\_ENGINE\\_SUBSTITUTION](#page-166-0).

## <span id="page-170-0"></span>**Strict SQL Mode**

Strict mode controls how MySQL handles invalid or missing values in data-change statements such as INSERT or UPDATE. A value can be invalid for several reasons. For example, it might have the wrong data type for the column, or it might be out of range. A value is missing when a new row to be inserted does not contain a value for a non-NULL column that has no explicit DEFAULT clause in its definition. (For a NULL column, NULL is inserted if the value is missing.) Strict mode also affects DDL statements such as CREATE TABLE.

If strict mode is not in effect, MySQL inserts adjusted values for invalid or missing values and produces warnings (see Section 15.7.7.42, "SHOW WARNINGS Statement"). In strict mode, you can produce this behavior by using INSERT IGNORE or UPDATE IGNORE.

For statements such as SELECT that do not change data, invalid values generate a warning in strict mode, not an error.

Strict mode produces an error for attempts to create a key that exceeds the maximum key length. When strict mode is not enabled, this results in a warning and truncation of the key to the maximum key length.

Strict mode does not affect whether foreign key constraints are checked. foreign\_key\_checks can be used for that. (See Section 7.1.8, "Server System Variables".)

Strict SQL mode is in effect if either [STRICT\\_ALL\\_TABLES](#page-169-3) or [STRICT\\_TRANS\\_TABLES](#page-169-1) is enabled, although the effects of these modes differ somewhat:

- For transactional tables, an error occurs for invalid or missing values in a data-change statement when either [STRICT\\_ALL\\_TABLES](#page-169-3) or [STRICT\\_TRANS\\_TABLES](#page-169-1) is enabled. The statement is aborted and rolled back.
- For nontransactional tables, the behavior is the same for either mode if the bad value occurs in the first row to be inserted or updated: The statement is aborted and the table remains unchanged. If the statement inserts or modifies multiple rows and the bad value occurs in the second or later row, the result depends on which strict mode is enabled:
  - For [STRICT\\_ALL\\_TABLES](#page-169-3), MySQL returns an error and ignores the rest of the rows. However, because the earlier rows have been inserted or updated, the result is a partial update. To avoid this, use single-row statements, which can be aborted without changing the table.
  - For [STRICT\\_TRANS\\_TABLES](#page-169-1), MySQL converts an invalid value to the closest valid value for the column and inserts the adjusted value. If a value is missing, MySQL inserts the implicit default value for the column data type. In either case, MySQL generates a warning rather than an error and continues processing the statement. Implicit defaults are described in Section 13.6, "Data Type Default Values".

Strict mode affects handling of division by zero, zero dates, and zeros in dates as follows:

• Strict mode affects handling of division by zero, which includes MOD(N,0):

For data-change operations (INSERT, UPDATE):

- If strict mode is not enabled, division by zero inserts NULL and produces no warning.
- If strict mode is enabled, division by zero produces an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, division by zero inserts NULL and produces a warning.

For SELECT, division by zero returns NULL. Enabling strict mode causes a warning to be produced as well.

- Strict mode affects whether the server permits '0000-00-00' as a valid date:
  - If strict mode is not enabled, '0000-00-00' is permitted and inserts produce no warning.
  - If strict mode is enabled, '0000-00-00' is not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, '0000-00-00' is permitted and inserts produce a warning.
- Strict mode affects whether the server permits dates in which the year part is nonzero but the month or day part is 0 (dates such as '2010-00-01' or '2010-01-00'):
  - If strict mode is not enabled, dates with zero parts are permitted and inserts produce no warning.
  - If strict mode is enabled, dates with zero parts are not permitted and inserts produce an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, dates with zero parts are inserted as '0000-00-00' (which is considered valid with IGNORE) and produce a warning.

For more information about strict mode with respect to IGNORE, see [Comparison of the IGNORE](#page-171-0) [Keyword and Strict SQL Mode](#page-171-0).

Strict mode affects handling of division by zero, zero dates, and zeros in dates in conjunction with the [ERROR\\_FOR\\_DIVISION\\_BY\\_ZERO](#page-165-0), [NO\\_ZERO\\_DATE](#page-167-1), and [NO\\_ZERO\\_IN\\_DATE](#page-167-0) modes.

## <span id="page-171-0"></span>**Comparison of the IGNORE Keyword and Strict SQL Mode**

This section compares the effect on statement execution of the IGNORE keyword (which downgrades errors to warnings) and strict SQL mode (which upgrades warnings to errors). It describes which statements they affect, and which errors they apply to.

The following table presents a summary comparison of statement behavior when the default is to produce an error versus a warning. An example of when the default is to produce an error is inserting a NULL into a NOT NULL column. An example of when the default is to produce a warning is inserting a value of the wrong data type into a column (such as inserting the string 'abc' into an integer column).

| Operational Mode                     | When Statement Default is<br>Error                   | When Statement Default is<br>Warning                   |
|--------------------------------------|------------------------------------------------------|--------------------------------------------------------|
| Without IGNORE or strict SQL<br>mode | Error                                                | Warning                                                |
| With IGNORE                          | Warning                                              | Warning (same as without<br>IGNORE or strict SQL mode) |
| With strict SQL mode                 | Error (same as without IGNORE<br>or strict SQL mode) | Error                                                  |
| With IGNORE and strict SQL<br>mode   | Warning                                              | Warning                                                |

One conclusion to draw from the table is that when the IGNORE keyword and strict SQL mode are both in effect, IGNORE takes precedence. This means that, although IGNORE and strict SQL mode can be considered to have opposite effects on error handling, they do not cancel when used together.

- [The Effect of IGNORE on Statement Execution](#page-172-0)
- [The Effect of Strict SQL Mode on Statement Execution](#page-173-0)

### <span id="page-172-0"></span>**The Effect of IGNORE on Statement Execution**

Several statements in MySQL support an optional IGNORE keyword. This keyword causes the server to downgrade certain types of errors and generate warnings instead. For a multiple-row statement, downgrading an error to a warning may enable a row to be processed. Otherwise, IGNORE causes the statement to skip to the next row instead of aborting. (For nonignorable errors, an error occurs regardless of the IGNORE keyword.)

Example: If the table t has a primary key column i containing unique values, attempting to insert the same value of i into multiple rows normally produces a duplicate-key error:

```
mysql> CREATE TABLE t (i INT NOT NULL PRIMARY KEY);
mysql> INSERT INTO t (i) VALUES(1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 't.PRIMARY'
```

With IGNORE, the row containing the duplicate key still is not inserted, but a warning occurs instead of an error:

```
mysql> INSERT IGNORE INTO t (i) VALUES(1),(1);
Query OK, 1 row affected, 1 warning (0.01 sec)
Records: 2 Duplicates: 1 Warnings: 1
mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------+
| Level | Code | Message |
+---------+------+-----------------------------------------+
| Warning | 1062 | Duplicate entry '1' for key 't.PRIMARY' |
+---------+------+-----------------------------------------+
1 row in set (0.00 sec)
```

Example: If the table t2 has a NOT NULL column id, attempting to insert NULL produces an error in strict SQL mode:

```
mysql> CREATE TABLE t2 (id INT NOT NULL);
mysql> INSERT INTO t2 (id) VALUES(1),(NULL),(3);
ERROR 1048 (23000): Column 'id' cannot be null
mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

If the SQL mode is not strict, IGNORE causes the NULL to be inserted as the column implicit default (0 in this case), which enables the row to be handled without skipping it:

```
mysql> INSERT INTO t2 (id) VALUES(1),(NULL),(3);
mysql> SELECT * FROM t2;
+----+
| id |
+----+
| 1 |
| 0 |
| 3 |
+----+
```

These statements support the IGNORE keyword:

- CREATE TABLE ... SELECT: IGNORE does not apply to the CREATE TABLE or SELECT parts of the statement but to inserts into the table of rows produced by the SELECT. Rows that duplicate an existing row on a unique key value are discarded.
- DELETE: IGNORE causes MySQL to ignore errors during the process of deleting rows.
- INSERT: With IGNORE, rows that duplicate an existing row on a unique key value are discarded. Rows set to values that would cause data conversion errors are set to the closest valid values instead.

 For partitioned tables where no partition matching a given value is found, IGNORE causes the insert operation to fail silently for rows containing the unmatched value.

- LOAD DATA, LOAD XML: With IGNORE, rows that duplicate an existing row on a unique key value are discarded.
- UPDATE: With IGNORE, rows for which duplicate-key conflicts occur on a unique key value are not updated. Rows updated to values that would cause data conversion errors are updated to the closest valid values instead.

The IGNORE keyword applies to the following ignorable errors:

```
• ER_BAD_NULL_ERROR
• ER_DUP_ENTRY
• ER_DUP_ENTRY_WITH_KEY_NAME
• ER_DUP_KEY
• ER_NO_PARTITION_FOR_GIVEN_VALUE
• ER_NO_PARTITION_FOR_GIVEN_VALUE_SILENT
• ER_NO_REFERENCED_ROW_2
• ER_ROW_DOES_NOT_MATCH_GIVEN_PARTITION_SET
• ER_ROW_IS_REFERENCED_2
• ER_SUBQUERY_NO_1_ROW
```

### <span id="page-173-0"></span>**The Effect of Strict SQL Mode on Statement Execution**

• [ER\\_VIEW\\_CHECK\\_FAILED](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_view_check_failed)

The MySQL server can operate in different SQL modes, and can apply these modes differently for different clients, depending on the value of the [sql\\_mode](#page-73-0) system variable. In "strict" SQL mode, the server upgrades certain warnings to errors.

For example, in non-strict SQL mode, inserting the string 'abc' into an integer column results in conversion of the value to 0 and a warning:

```
mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO t (i) VALUES('abc');
Query OK, 1 row affected, 1 warning (0.01 sec)
mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------+
| Level | Code | Message |
+---------+------+--------------------------------------------------------+
| Warning | 1366 | Incorrect integer value: 'abc' for column 'i' at row 1 |
+---------+------+--------------------------------------------------------+
1 row in set (0.00 sec)
```

In strict SQL mode, the invalid value is rejected with an error:

```
mysql> SET sql_mode = 'STRICT_ALL_TABLES';
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO t (i) VALUES('abc');
ERROR 1366 (HY000): Incorrect integer value: 'abc' for column 'i' at row 1
```

For more information about possible settings of the [sql\\_mode](#page-73-0) system variable, see [Section 7.1.11,](#page-162-0) ["Server SQL Modes".](#page-162-0)

Strict SQL mode applies to the following statements under conditions for which some value might be out of range or an invalid row is inserted into or deleted from a table:

- ALTER TABLE
- CREATE TABLE
- CREATE TABLE ... SELECT
- DELETE (both single table and multiple table)
- INSERT
- LOAD DATA
- LOAD XML
- SELECT SLEEP()
- UPDATE (both single table and multiple table)

Within stored programs, individual statements of the types just listed execute in strict SQL mode if the program was defined while strict mode was in effect.

Strict SQL mode applies to the following errors, which represent a class of errors in which an input value is either invalid or missing. A value is invalid if it has the wrong data type for the column or might be out of range. A value is missing if a new row to be inserted does not contain a value for a NOT NULL column that has no explicit DEFAULT clause in its definition.

```
ER_BAD_NULL_ERROR
ER_CUT_VALUE_GROUP_CONCAT
ER_DATA_TOO_LONG
ER_DATETIME_FUNCTION_OVERFLOW
ER_DIVISION_BY_ZERO
ER_INVALID_ARGUMENT_FOR_LOGARITHM
ER_NO_DEFAULT_FOR_FIELD
ER_NO_DEFAULT_FOR_VIEW_FIELD
ER_TOO_LONG_KEY
ER_TRUNCATED_WRONG_VALUE
ER_TRUNCATED_WRONG_VALUE_FOR_FIELD
ER_WARN_DATA_OUT_OF_RANGE
ER_WARN_NULL_TO_NOTNULL
ER_WARN_TOO_FEW_RECORDS
ER_WRONG_ARGUMENTS
ER_WRONG_VALUE_FOR_TYPE
WARN_DATA_TRUNCATED
```

![](_page_174_Picture_15.jpeg)

#### **Note**

Because continued MySQL development defines new errors, there may be errors not in the preceding list to which strict SQL mode applies.