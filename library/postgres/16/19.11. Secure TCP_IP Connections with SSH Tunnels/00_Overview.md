---
source: PostgreSQL 16 Reference
title: 00_Overview
---

It is possible to use SSH to encrypt the network connection between clients and a PostgreSQL server. Done properly, this provides an adequately secure network connection, even for non-SSL-capable clients.

First make sure that an SSH server is running properly on the same machine as the PostgreSQL server and that you can log in using ssh as some user; you then can establish a secure tunnel to the remote server. A secure tunnel listens on a local port and forwards all traffic to a port on the remote machine. Traffic sent to the remote port can arrive on its localhost address, or different bind address if desired; it does not appear as coming from your local machine. This command creates a secure tunnel from the client machine to the remote machine foo.com:

```
ssh -L 63333:localhost:5432 joe@foo.com
```

The first number in the -L argument, 63333, is the local port number of the tunnel; it can be any unused port. (IANA reserves ports 49152 through 65535 for private use.) The name or IP address after this is the remote bind address you are connecting to, i.e., localhost, which is the default. The second number, 5432, is the remote end of the tunnel, e.g., the port number your database server is using. In order to connect to the database server using this tunnel, you connect to port 63333 on the local machine:

```
psql -h localhost -p 63333 postgres
```

To the database server it will then look as though you are user joe on host foo.com connecting to the localhost bind address, and it will use whatever authentication procedure was configured for connections by that user to that bind address. Note that the server will not think the connection is SSLencrypted, since in fact it is not encrypted between the SSH server and the PostgreSQL server. This should not pose any extra security risk because they are on the same machine.

In order for the tunnel setup to succeed you must be allowed to connect via ssh as joe@foo.com, just as if you had attempted to use ssh to create a terminal session.

You could also have set up port forwarding as

```
ssh -L 63333:foo.com:5432 joe@foo.com
```

but then the database server will see the connection as coming in on its foo.com bind address, which is not opened by the default setting listen\_addresses = 'localhost'. This is usually not what you want.

If you have to "hop" to the database server via some login host, one possible setup could look like this:

```
ssh -L 63333:db.foo.com:5432 joe@shell.foo.com
```

Note that this way the connection from shell.foo.com to db.foo.com will not be encrypted by the SSH tunnel. SSH offers quite a few configuration possibilities when the network is restricted in various ways. Please refer to the SSH documentation for details.

### **Tip**

Several other applications exist that can provide secure tunnels using a procedure similar in concept to the one just described.

# <span id="page-37-0"></span>**19.12. Registering Event Log on Windows**

To register a Windows event log library with the operating system, issue this command:

```
regsvr32 pgsql_library_directory/pgevent.dll
```

This creates registry entries used by the event viewer, under the default event source named PostgreSQL.

To specify a different event source name (see [event\\_source](#page-87-0)), use the /n and /i options:

**regsvr32 /n /i:event\_source\_name pgsql\_library\_directory/ pgevent.dll**

To unregister the event log library from the operating system, issue this command:

**regsvr32 /u [/i:event\_source\_name] pgsql\_library\_directory/ pgevent.dll**

### **Note**

To enable event logging in the database server, modify [log\\_destination](#page-84-0) to include eventlog in postgresql.conf.

# <span id="page-39-0"></span>**Chapter 20. Server Configuration**

There are many configuration parameters that affect the behavior of the database system. In the first section of this chapter we describe how to interact with configuration parameters. The subsequent sections discuss each parameter in detail.