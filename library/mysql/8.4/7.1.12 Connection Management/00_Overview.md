---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes how MySQL Server manages connections. This includes a description of the available connection interfaces, how the server uses connection handler threads, details about the administrative connection interface, and management of DNS lookups.

# <span id="page-174-0"></span>**7.1.12.1 Connection Interfaces**

This section describes aspects of how the MySQL server manages client connections.

- [Network Interfaces and Connection Manager Threads](#page-175-0)
- [Client Connection Thread Management](#page-175-1)
- [Connection Volume Management](#page-176-0)

### <span id="page-175-0"></span>**Network Interfaces and Connection Manager Threads**

The server is capable of listening for client connections on multiple network interfaces. Connection manager threads handle client connection requests on the network interfaces that the server listens to:

- On all platforms, one manager thread handles TCP/IP connection requests.
- On Unix, the same manager thread also handles Unix socket file connection requests.
- On Windows, one manager thread handles shared-memory connection requests, and another handles named-pipe connection requests.
- On all platforms, an additional network interface may be enabled to accept administrative TCP/IP connection requests. This interface can use the manager thread that handles "ordinary" TCP/IP requests, or a separate thread.

The server does not create threads to handle interfaces that it does not listen to. For example, a Windows server that does not have support for named-pipe connections enabled does not create a thread to handle them.

Individual server plugins or components may implement their own connection interface:

• X Plugin enables MySQL Server to communicate with clients using X Protocol. See Section 22.5, "X Plugin".

### <span id="page-175-1"></span>**Client Connection Thread Management**

Connection manager threads associate each client connection with a thread dedicated to it that handles authentication and request processing for that connection. Manager threads create a new thread when necessary but try to avoid doing so by consulting the thread cache first to see whether it contains a thread that can be used for the connection. When a connection ends, its thread is returned to the thread cache if the cache is not full.

In this connection thread model, there are as many threads as there are clients currently connected, which has some disadvantages when server workload must scale to handle large numbers of connections. For example, thread creation and disposal becomes expensive. Also, each thread requires server and kernel resources, such as stack space. To accommodate a large number of simultaneous connections, the stack size per thread must be kept small, leading to a situation where it is either too small or the server consumes large amounts of memory. Exhaustion of other resources can occur as well, and scheduling overhead can become significant.

MySQL Enterprise Edition includes a thread pool plugin that provides an alternative thread-handling model designed to reduce overhead and improve performance. It implements a thread pool that increases server performance by efficiently managing statement execution threads for large numbers of client connections. See Section 7.6.3, "MySQL Enterprise Thread Pool".

To control and monitor how the server manages threads that handle client connections, several system and status variables are relevant. (See Section 7.1.8, "Server System Variables", and [Section 7.1.10,](#page-138-0) ["Server Status Variables".](#page-138-0))

• The [thread\\_cache\\_size](#page-89-1) system variable determines the thread cache size. By default, the server autosizes the value at startup, but it can be set explicitly to override this default. A value of 0 disables caching, which causes a thread to be set up for each new connection and disposed of when the connection terminates. To enable N inactive connection threads to be cached, set [thread\\_cache\\_size](#page-89-1) to N at server startup or at runtime. A connection thread becomes inactive when the client connection with which it was associated terminates.

- To monitor the number of threads in the cache and how many threads have been created because a thread could not be taken from the cache, check the [Threads\\_cached](#page-162-4) and [Threads\\_created](#page-162-1) status variables.
- When the thread stack is too small, this limits the complexity of the SQL statements the server can handle, the recursion depth of stored procedures, and other memory-consuming actions. To set a stack size of N bytes for each thread, start the server with [thread\\_stack](#page-96-1) set to N.

### <span id="page-176-0"></span>**Connection Volume Management**

To control the maximum number of clients the server permits to connect simultaneously, set the [max\\_connections](#page-21-0) system variable at server startup or at runtime. It may be necessary to increase [max\\_connections](#page-21-0) if more clients attempt to connect simultaneously then the server is configured to handle (see Section B.3.2.5, "Too many connections"). If the server refuses a connection because the [max\\_connections](#page-21-0) limit is reached, it increments the [Connection\\_errors\\_max\\_connections](#page-141-4) status variable.

mysqld actually permits [max\\_connections](#page-21-0) + 1 client connections. The extra connection is reserved for use by accounts that have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). By granting the privilege to administrators and not to normal users (who should not need it), an administrator can connect to the server and use SHOW PROCESSLIST to diagnose problems even if the maximum number of unprivileged clients are connected. See Section 15.7.7.31, "SHOW PROCESSLIST Statement".

The server also permits administrative connections on an administrative network interface, which you can set up using a dedicated IP address and port. See [Section 7.1.12.2, "Administrative Connection](#page-177-0) [Management".](#page-177-0)

The Group Replication plugin interacts with MySQL Server using internal sessions to perform SQL API operations. Group Replication's internal sessions are handled separately from client connections, so they do not count towards the [max\\_connections](#page-21-0) limit and are not refused if the server has reached this limit.

The maximum number of client connections MySQL supports (that is, the maximum value to which [max\\_connections](#page-21-0) can be set) depends on several factors:

- The quality of the thread library on a given platform.
- The amount of RAM available.
- The amount of RAM is used for each connection.
- The workload from each connection.
- The desired response time.
- The number of file descriptors available.

Linux or Solaris should be able to support at least 500 to 1000 simultaneous connections routinely and as many as 10,000 connections if you have many gigabytes of RAM available and the workload from each is low or the response time target undemanding.

Increasing the [max\\_connections](#page-21-0) value increases the number of file descriptors that mysqld requires. If the required number of descriptors are not available, the server reduces the value of [max\\_connections](#page-21-0). For comments on file descriptor limits, see Section 10.4.3.1, "How MySQL Opens and Closes Tables".

Increasing the [open\\_files\\_limit](#page-36-0) system variable may be necessary, which may also require raising the operating system limit on how many file descriptors can be used by MySQL. Consult your operating system documentation to determine whether it is possible to increase the limit and how to do so. See also Section B.3.2.16, "File Not Found and Similar Errors".

## <span id="page-177-0"></span>**7.1.12.2 Administrative Connection Management**

As mentioned in [Connection Volume Management,](#page-176-0) to allow for the need to perform administrative operations even when [max\\_connections](#page-21-0) connections are already established on the interfaces used for ordinary connections, the MySQL server permits a single administrative connection to users who have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

The server also permits dedicating a TCP/IP port for administrative connections, as described in the following sections.

- [Administrative Interface Characteristics](#page-177-1)
- [Administrative Interface Support for Encrypted Connections](#page-177-2)

### <span id="page-177-1"></span>**Administrative Interface Characteristics**

The administrative connection interface has these characteristics:

- The server enables the interface only if the admin\_address system variable is set at startup to indicate the IP address for it. If admin\_address is not set, the server maintains no administrative interface.
- The admin\_port system variable specifies the interface TCP/IP port number (default 33062).
- There is no limit on the number of administrative connections, but connections are permitted only for users who have the SERVICE\_CONNECTION\_ADMIN privilege.
- The create\_admin\_listener\_thread system variable enables DBAs to choose at startup whether the administrative interface has its own separate thread. The default is OFF; that is, the manager thread for ordinary connections on the main interface also handles connections for the administrative interface.

These lines in the server my.cnf file enable the administrative interface on the loopback interface and configure it to use port number 33064 (that is, a port different from the default):

```
[mysqld]
admin_address=127.0.0.1
admin_port=33064
```

MySQL client programs connect to either the main or administrative interface by specifying appropriate connection parameters. If the server running on the local host is using the default TCP/IP port numbers of 3306 and 33062 for the main and administrative interfaces, these commands connect to those interfaces:

```
mysql --protocol=TCP --port=3306
mysql --protocol=TCP --port=33062
```

### <span id="page-177-2"></span>**Administrative Interface Support for Encrypted Connections**

The administrative interface has its own configuration parameters for encrypted connections. These correspond to the main interface parameters but enable independent configuration of encrypted connections for the administrative interface:

The admin\_tls\_xxx and admin\_ssl\_xxx system variables are like the tls\_xxx and ssl\_xxx system variables, but they configure the TLS context for the administrative interface rather than the main interface.

For general information about configuring connection-encryption support, see Section 8.3.1, "Configuring MySQL to Use Encrypted Connections", and Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". That discussion is written for the main connection interface, but the parameter names are similar for the administrative connection interface. Use that discussion together with the following remarks, which provide information specific to the administrative interface.

TLS configuration for the administrative interface follows these rules:

- The administrative interface supports encrypted connections. For connections on the interface, the applicable TLS context depends on whether any nondefault administrative TLS parameter is configured:
  - If all administrative TLS parameters have their default values, the administrative interface uses the same TLS context as the main interface.
  - If any administrative TLS parameter has a nondefault value, the administrative interface uses the TLS context defined by its own parameters. (This is the case if any admin\_tls\_xxx or admin\_ssl\_xxx system variable is set to a value different from its default.) If a valid TLS context cannot be created from those parameters, the administrative interface falls back to the main interface TLS context.
- It is possible to disable encrypted connections to the administrative interface by setting the admin\_tls\_version system variable to the empty value to indicate that no TLS versions are supported. For example, these lines in the server my.cnf file disable encrypted connections on the administrative interface:

```
[mysqld]
admin_tls_version=''
```

#### Examples:

• This configuration in the server my.cnf file enables the administrative interface, but does not set any of the TLS parameters specific to that interface:

```
[mysqld]
admin_address=127.0.0.1
```

As a result, the administrative interface supports encrypted connections (because encryption is supported by default when the administrative interface is enabled), and uses the main interface TLS context. When clients connect to the administrative interface, they should use the same certificate and key files as for ordinary connections on the main interface. For example (enter the command on a single line):

```
mysql --protocol=TCP --port=33062
 --ssl-ca=ca.pem
 --ssl-cert=client-cert.pem
 --ssl-key=client-key.pem
```

• This server configuration enables the administrative interface and sets the TLS certificate and key file parameters specific to that interface:

```
[mysqld]
admin_address=127.0.0.1
admin_ssl_ca=admin-ca.pem
admin_ssl_cert=admin-server-cert.pem
admin_ssl_key=admin-server-key.pem
```

As a result, the administrative interface supports encrypted connections using its own TLS context. When clients connect to the administrative interface, they should use certificate and key files specific to that interface. For example (enter the command on a single line):

```
mysql --protocol=TCP --port=33062
 --ssl-ca=admin-ca.pem
 --ssl-cert=admin-client-cert.pem
 --ssl-key=admin-client-key.pem
```

# <span id="page-178-0"></span>**7.1.12.3 DNS Lookups and the Host Cache**

The MySQL server maintains an in-memory host cache that contains information about clients: IP address, host name, and error information. The Performance Schema host\_cache table exposes the contents of the host cache so that it can be examined using SELECT statements. This may help you diagnose the causes of connection problems. See Section 29.12.22.3, "The host\_cache Table".

The following sections discuss how the host cache works, as well as other topics such as how to configure and monitor the cache.

- [Host Cache Operation](#page-179-0)
- [Configuring the Host Cache](#page-180-0)
- [Monitoring the Host Cache](#page-180-1)
- [Flushing the Host Cache](#page-181-0)
- [Dealing with Blocked Hosts](#page-181-1)

### <span id="page-179-0"></span>**Host Cache Operation**

The server uses the host cache only for non-localhost TCP connections. It does not use the cache for TCP connections established using a loopback interface address (for example, 127.0.0.1 or ::1), or for connections established using a Unix socket file, named pipe, or shared memory.

The server uses the host cache for several purposes:

- By caching the results of IP-to-host name lookups, the server avoids doing a Domain Name System (DNS) lookup for each client connection. Instead, for a given host, it needs to perform a lookup only for the first connection from that host.
- The cache contains information about errors that occur during the client connection process. Some errors are considered "blocking." If too many of these occur successively from a given host without a successful connection, the server blocks further connections from that host. The [max\\_connect\\_errors](#page-20-1) system variable determines the permitted number of successive errors before blocking occurs.

For each applicable new client connection, the server uses the client IP address to check whether the client host name is in the host cache. If so, the server refuses or continues to process the connection request depending on whether or not the host is blocked. If the host is not in the cache, the server attempts to resolve the host name. First, it resolves the IP address to a host name and resolves that host name back to an IP address. Then it compares the result to the original IP address to ensure that they are the same. The server stores information about the result of this operation in the host cache. If the cache is full, the least recently used entry is discarded.

The server performs host name resolution using the getaddrinfo() system call.

The server handles entries in the host cache like this:

- 1. When the first TCP client connection reaches the server from a given IP address, a new cache entry is created to record the client IP, host name, and client lookup validation flag. Initially, the host name is set to NULL and the flag is false. This entry is also used for subsequent client TCP connections from the same originating IP.
- 2. If the validation flag for the client IP entry is false, the server attempts an IP-to-host name-to-IP DNS resolution. If that is successful, the host name is updated with the resolved host name and the validation flag is set to true. If resolution is unsuccessful, the action taken depends on whether the error is permanent or transient. For permanent failures, the host name remains NULL and the validation flag is set to true. For transient failures, the host name and validation flag remain unchanged. (In this case, another DNS resolution attempt occurs the next time a client connects from this IP.)
- 3. If an error occurs while processing an incoming client connection from a given IP address, the server updates the corresponding error counters in the entry for that IP. For a description of the errors recorded, see Section 29.12.22.3, "The host\_cache Table".

To unblock blocked hosts, flush the host cache; see [Dealing with Blocked Hosts.](#page-181-1)

It is possible for a blocked host to become unblocked even without flushing the host cache if activity from other hosts occurs:

- If the cache is full when a connection arrives from a client IP not in the cache, the server discards the least recently used cache entry to make room for the new entry.
- If the discarded entry is for a blocked host, that host becomes unblocked.

Some connection errors are not associated with TCP connections, occur very early in the connection process (even before an IP address is known), or are not specific to any particular IP address (such as out-of-memory conditions). For information about these errors, check the [Connection\\_errors\\_](#page-140-0)xxx status variables (see [Section 7.1.10, "Server Status Variables"\)](#page-138-0).

### <span id="page-180-0"></span>**Configuring the Host Cache**

The host cache is enabled by default. The [host\\_cache\\_size](#page-0-2) system variable controls its size, as well as the size of the Performance Schema host\_cache table that exposes the cache contents. The cache size can be set at server startup and changed at runtime. For example, to set the size to 100 at startup, put these lines in the server my.cnf file:

```
[mysqld]
host_cache_size=200
```

To change the size to 300 at runtime, do this:

```
SET GLOBAL host_cache_size=300;
```

Setting host\_cache\_size to 0, either at server startup or at runtime, disables the host cache. With the cache disabled, the server performs a DNS lookup every time a client connects.

Changing the cache size at runtime causes an implicit host cache flushing operation that clears the host cache, truncates the host\_cache table, and unblocks any blocked hosts; see [Flushing the Host](#page-181-0) [Cache.](#page-181-0)

To disable DNS host name lookups, start the server with the [skip\\_name\\_resolve](#page-67-2) system variable enabled. In this case, the server uses only IP addresses and not host names to match connecting hosts to rows in the MySQL grant tables. Only accounts specified in those tables using IP addresses can be used. (A client may not be able to connect if no account exists that specifies the client IP address.)

If you have a very slow DNS and many hosts, you might be able to improve performance either by enabling [skip\\_name\\_resolve](#page-67-2) to disable DNS lookups, or by increasing the value of [host\\_cache\\_size](#page-0-2) to make the host cache larger.

To disallow TCP/IP connections entirely, start the server with the [skip\\_networking](#page-68-0) system variable enabled.

To adjust the permitted number of successive connection errors before host blocking occurs, set the [max\\_connect\\_errors](#page-20-1) system variable. For example, to set the value at startup put these lines in the server my.cnf file:

```
[mysqld]
max_connect_errors=10000
```

To change the value at runtime, do this:

```
SET GLOBAL max_connect_errors=10000;
```

### <span id="page-180-1"></span>**Monitoring the Host Cache**

The Performance Schema host\_cache table exposes the contents of the host cache. This table can be examined using SELECT statements, which may help you diagnose the causes of connection problems. For information about this table, see Section 29.12.22.3, "The host\_cache Table".

### <span id="page-181-0"></span>**Flushing the Host Cache**

Flushing the host cache might be advisable or desirable under these conditions:

- Some of your client hosts change IP address.
- The error message Host 'host\_name' is blocked occurs for connections from legitimate hosts. (See [Dealing with Blocked Hosts.](#page-181-1))

Flushing the host cache has these effects:

- It clears the in-memory host cache.
- It removes all rows from the Performance Schema host\_cache table that exposes the cache contents.
- It unblocks any blocked hosts. This enables further connection attempts from those hosts.

To flush the host cache, use any of these methods:

- Change the value of the [host\\_cache\\_size](#page-0-2) system variable. This requires the SYSTEM\_VARIABLES\_ADMIN privilege (or the deprecated SUPER privilege).
- Execute a TRUNCATE TABLE statement that truncates the Performance Schema host\_cache table. This requires the DROP privilege for the table.
- Execute a mysqladmin flush-hosts command. This requires the DROP privilege for the Performance Schema host\_cache table or the RELOAD privilege.

### <span id="page-181-1"></span>**Dealing with Blocked Hosts**

The server uses the host cache to track errors that occur during the client connection process. If the following error occurs, it means that mysqld has received many connection requests from the given host that were interrupted in the middle:

```
Host 'host_name' is blocked because of many connection errors.
Unblock with 'mysqladmin flush-hosts'
```

The value of the [max\\_connect\\_errors](#page-20-1) system variable determines how many successive interrupted connection requests the server permits before blocking a host. After [max\\_connect\\_errors](#page-20-1) failed requests without a successful connection, the server assumes that something is wrong (for example, that someone is trying to break in), and blocks the host from further connection requests.

To unblock blocked hosts, flush the host cache; see [Flushing the Host Cache](#page-181-0).

Alternatively, to avoid having the error message occur, set [max\\_connect\\_errors](#page-20-1) as described in [Configuring the Host Cache](#page-180-0). The default value of [max\\_connect\\_errors](#page-20-1) is 100. Increasing [max\\_connect\\_errors](#page-20-1) to a large value makes it less likely that a host reaches the threshold and becomes blocked. However, if the Host 'host\_name' is blocked error message occurs, first verify that there is nothing wrong with TCP/IP connections from the blocked hosts. It does no good to increase the value of [max\\_connect\\_errors](#page-20-1) if there are network problems.