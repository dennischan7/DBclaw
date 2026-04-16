---
source: PostgreSQL 16 Reference
title: 00_Overview
---

In addition to the postgresql.conf file already mentioned, PostgreSQL uses two other manually-edited configuration files, which control client authentication (their use is discussed in [Chapter 21](#page-124-0)). By default, all three configuration files are stored in the database cluster's data directory. The parameters described in this section allow the configuration files to be placed elsewhere. (Doing so can ease administration. In particular it is often easier to ensure that the configuration files are properly backed-up when they are kept separate.)

```
data_directory (string)
```

Specifies the directory to use for data storage. This parameter can only be set at server start.

```
config_file (string)
```

Specifies the main server configuration file (customarily called postgresql.conf). This parameter can only be set on the postgres command line.

```
hba_file (string)
```

Specifies the configuration file for host-based authentication (customarily called pg\_hba.conf). This parameter can only be set at server start.

```
ident_file (string)
```

Specifies the configuration file for user name mapping (customarily called pg\_ident.conf). This parameter can only be set at server start. See also [Section 21.2](#page-133-0).

```
external_pid_file (string)
```

Specifies the name of an additional process-ID (PID) file that the server should create for use by server administration programs. This parameter can only be set at server start.

In a default installation, none of the above parameters are set explicitly. Instead, the data directory is specified by the -D command-line option or the PGDATA environment variable, and the configuration files are all found within the data directory.

If you wish to keep the configuration files elsewhere than the data directory, the postgres -D command-line option or PGDATA environment variable must point to the directory containing the configuration files, and the data\_directory parameter must be set in postgresql.conf (or on the command line) to show where the data directory is actually located. Notice that data\_directory overrides -D and PGDATA for the location of the data directory, but not for the location of the configuration files.

If you wish, you can specify the configuration file names and locations individually using the parameters config\_file, hba\_file and/or ident\_file. config\_file can only be specified on the postgres command line, but the others can be set within the main configuration file. If all three parameters plus data\_directory are explicitly set, then it is not necessary to specify -D or PGDATA.

When setting any of these parameters, a relative path will be interpreted with respect to the directory in which postgres is started.

# <span id="page-44-4"></span>**20.3. Connections and Authentication**

## <span id="page-44-3"></span>**20.3.1. Connection Settings**

```
listen_addresses (string)
```

Specifies the TCP/IP address(es) on which the server is to listen for connections from client applications. The value takes the form of a comma-separated list of host names and/or numeric IP addresses. The special entry \* corresponds to all available IP interfaces. The entry 0.0.0.0 allows listening for all IPv4 addresses and :: allows listening for all IPv6 addresses. If the list is empty, the server does not listen on any IP interface at all, in which case only Unix-domain sockets can be used to connect to it. If the list is not empty, the server will start if it can listen on at least one TCP/IP address. A warning will be emitted for any TCP/IP address which cannot be opened. The default value is localhost, which allows only local TCP/IP "loopback" connections to be made.

While client authentication ([Chapter 21\)](#page-124-0) allows fine-grained control over who can access the server, listen\_addresses controls which interfaces accept connection attempts, which can help prevent repeated malicious connection requests on insecure network interfaces. This parameter can only be set at server start.

```
port (integer)
```

The TCP port the server listens on; 5432 by default. Note that the same port number is used for all IP addresses the server listens on. This parameter can only be set at server start.

```
max_connections (integer)
```

Determines the maximum number of concurrent connections to the database server. The default is typically 100 connections, but might be less if your kernel settings will not support it (as determined during initdb). This parameter can only be set at server start.

When running a standby server, you must set this parameter to the same or higher value than on the primary server. Otherwise, queries will not be allowed in the standby server.

```
reserved_connections (integer)
```

Determines the number of connection "slots" that are reserved for connections by roles with privileges of the [pg\\_use\\_reserved\\_connections](#page-152-0) role. Whenever the number of free connection slots is greater than [superuser\\_reserved\\_connections](#page-44-1) but less than or equal to the sum of superuser\_reserved\_connections and reserved\_connections, new connections will be accepted only for superusers and roles with privileges of pg\_use\_reserved\_connections. If superuser\_reserved\_connections or fewer connection slots are available, new connections will be accepted only for superusers.

The default value is zero connections. The value must be less than max\_connections minus superuser\_reserved\_connections. This parameter can only be set at server start.

```
superuser_reserved_connections (integer)
```

Determines the number of connection "slots" that are reserved for connections by PostgreSQL superusers. At most [max\\_connections](#page-44-0) connections can ever be active simultaneously. Whenever the number of active concurrent connections is at least max\_connections minus superuser\_reserved\_connections, new connections will be accepted only for superusers. The connection slots reserved by this parameter are intended as final reserve for emergency use after the slots reserved by [reserved\\_connections](#page-44-2) have been exhausted.

The default value is three connections. The value must be less than max\_connections minus reserved\_connections. This parameter can only be set at server start.

```
unix_socket_directories (string)
```

Specifies the directory of the Unix-domain socket(s) on which the server is to listen for connections from client applications. Multiple sockets can be created by listing multiple directories separated by commas. Whitespace between entries is ignored; surround a directory name with double quotes if you need to include whitespace or commas in the name. An empty value specifies not listening on any Unix-domain sockets, in which case only TCP/IP sockets can be used to connect to the server.

A value that starts with @ specifies that a Unix-domain socket in the abstract namespace should be created (currently supported on Linux only). In that case, this value does not specify a "directory" but a prefix from which the actual socket name is computed in the same manner as for the filesystem namespace. While the abstract socket name prefix can be chosen freely, since it is not a file-system location, the convention is to nonetheless use file-system-like values such as @/tmp.

The default value is normally /tmp, but that can be changed at build time. On Windows, the default is empty, which means no Unix-domain socket is created by default. This parameter can only be set at server start.

In addition to the socket file itself, which is named .s.PGSQL.nnnn where nnnn is the server's port number, an ordinary file named .s.PGSQL.nnnn.lock will be created in each of the unix\_socket\_directories directories. Neither file should ever be removed manually. For sockets in the abstract namespace, no lock file is created.

```
unix_socket_group (string)
```

Sets the owning group of the Unix-domain socket(s). (The owning user of the sockets is always the user that starts the server.) In combination with the parameter unix\_socket\_permissions this can be used as an additional access control mechanism for Unix-domain connections. By default this is the empty string, which uses the default group of the server user. This parameter can only be set at server start.

This parameter is not supported on Windows. Any setting will be ignored. Also, sockets in the abstract namespace have no file owner, so this setting is also ignored in that case.

```
unix_socket_permissions (integer)
```

Sets the access permissions of the Unix-domain socket(s). Unix-domain sockets use the usual Unix file system permission set. The parameter value is expected to be a numeric mode specified in the format accepted by the chmod and umask system calls. (To use the customary octal format the number must start with a 0 (zero).)

The default permissions are 0777, meaning anyone can connect. Reasonable alternatives are 0770 (only user and group, see also unix\_socket\_group) and 0700 (only user). (Note that for a Unix-domain socket, only write permission matters, so there is no point in setting or revoking read or execute permissions.)

This access control mechanism is independent of the one described in [Chapter 21.](#page-124-0)

This parameter can only be set at server start.

This parameter is irrelevant on systems, notably Solaris as of Solaris 10, that ignore socket permissions entirely. There, one can achieve a similar effect by pointing unix\_socket\_directories to a directory having search permission limited to the desired audience.

Sockets in the abstract namespace have no file permissions, so this setting is also ignored in that case.

```
bonjour (boolean)
```

Enables advertising the server's existence via Bonjour. The default is off. This parameter can only be set at server start.

```
bonjour_name (string)
```

Specifies the Bonjour service name. The computer name is used if this parameter is set to the empty string '' (which is the default). This parameter is ignored if the server was not compiled with Bonjour support. This parameter can only be set at server start.

## <span id="page-46-0"></span>**20.3.2. TCP Settings**

```
tcp_keepalives_idle (integer)
```

Specifies the amount of time with no network activity after which the operating system should send a TCP keepalive message to the client. If this value is specified without units, it is taken as seconds. A value of 0 (the default) selects the operating system's default. On Windows, setting a value of 0 will set this parameter to 2 hours, since Windows does not provide a way to read the system default value. This parameter is supported only on systems that support TCP\_KEEPIDLE or an equivalent socket option, and on Windows; on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

```
tcp_keepalives_interval (integer)
```

Specifies the amount of time after which a TCP keepalive message that has not been acknowledged by the client should be retransmitted. If this value is specified without units, it is taken as seconds. A value of 0 (the default) selects the operating system's default. On Windows, setting a value of 0 will set this parameter to 1 second, since Windows does not provide a way to read the system default value. This parameter is supported only on systems that support TCP\_KEEP-INTVL or an equivalent socket option, and on Windows; on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

```
tcp_keepalives_count (integer)
```

Specifies the number of TCP keepalive messages that can be lost before the server's connection to the client is considered dead. A value of 0 (the default) selects the operating system's default. This parameter is supported only on systems that support TCP\_KEEPCNT or an equivalent socket option (which does not include Windows); on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

```
tcp_user_timeout (integer)
```

Specifies the amount of time that transmitted data may remain unacknowledged before the TCP connection is forcibly closed. If this value is specified without units, it is taken as milliseconds. A value of 0 (the default) selects the operating system's default. This parameter is supported only on systems that support TCP\_USER\_TIMEOUT (which does not include Windows); on other systems, it must be zero. In sessions connected via a Unix-domain socket, this parameter is ignored and always reads as zero.

```
client_connection_check_interval (integer)
```

Sets the time interval between optional checks that the client is still connected, while running queries. The check is performed by polling the socket, and allows long running queries to be aborted sooner if the kernel reports that the connection is closed.

This option relies on kernel events exposed by Linux, macOS, illumos and the BSD family of operating systems, and is not currently available on other systems.

If the value is specified without units, it is taken as milliseconds. The default value is 0, which disables connection checks. Without connection checks, the server will detect the loss of the connection only at the next interaction with the socket, when it waits for, receives or sends data.

For the kernel itself to detect lost TCP connections reliably and within a known timeframe in all scenarios including network failure, it may also be necessary to adjust the TCP keepalive settings of the operating system, or the [tcp\\_keepalives\\_idle](#page-46-0), [tcp\\_keepalives\\_interval](#page-46-1) and [tcp\\_keepalives\\_count](#page-46-2) settings of PostgreSQL.