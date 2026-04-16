---
source: MySQL 8.4 Reference
title: 00_Overview
---

To connect with a client program to a MySQL server that is listening to different network interfaces from those compiled into your client, you can use one of the following methods:

- Start the client with --host=host\_name --port=port\_number to connect using TCP/IP to a remote server, with --host=127.0.0.1 --port=port\_number to connect using TCP/IP to a local server, or with --host=localhost --socket=file\_name to connect to a local server using a Unix socket file or a Windows named pipe.
- Start the client with --protocol=TCP to connect using TCP/IP, --protocol=SOCKET to connect using a Unix socket file, --protocol=PIPE to connect using a named pipe, or - protocol=MEMORY to connect using shared memory. For TCP/IP connections, you may also need to specify --host and --port options. For the other types of connections, you may need to specify a --socket option to specify a Unix socket file or Windows named-pipe name, or a --sharedmemory-base-name option to specify the shared-memory name. Shared-memory connections are supported only on Windows.
- On Unix, set the MYSQL\_UNIX\_PORT and MYSQL\_TCP\_PORT environment variables to point to the Unix socket file and TCP/IP port number before you start your clients. If you normally use a specific socket file or port number, you can place commands to set these environment variables in your .login file so that they apply each time you log in. See Section 6.9, "Environment Variables".
- Specify the default Unix socket file and TCP/IP port number in the [client] group of an option file. For example, you can use C:\my.cnf on Windows, or the .my.cnf file in your home directory on Unix. See Section 6.2.2.2, "Using Option Files".
- In a C program, you can specify the socket file or port number arguments in the [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-connect.md) call. You can also have the program read option files by calling [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md). See [C API Basic Function Descriptions](https://dev.mysql.com/doc/c-api/8.4/en/c-api-function-descriptions.md).
- If you are using the Perl DBD::mysql module, you can read options from MySQL option files. For example:

```
$dsn = "DBI:mysql:test;mysql_read_default_group=client;"
 . "mysql_read_default_file=/usr/local/mysql/data/my.cnf";
$dbh = DBI->connect($dsn, $user, $password);
```

See Section 31.9, "MySQL Perl API".

Other programming interfaces may provide similar capabilities for reading option files.

# <span id="page-139-0"></span>**7.9 Debugging MySQL**

This section describes debugging techniques that assist efforts to track down problems in MySQL.