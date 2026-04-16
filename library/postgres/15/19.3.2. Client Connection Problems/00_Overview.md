---
source: PostgreSQL 15 Reference
title: 00_Overview
---

Although the error conditions possible on the client side are quite varied and application-dependent, a few of them might be directly related to how the server was started. Conditions other than those shown below should be documented with the respective client application.

```
psql: error: connection to server at
 "server.joe.com" (123.123.123.123), port 5432 failed: Connection
 refused
 Is the server running on that host and accepting TCP/IP
 connections?
```

This is the generic "I couldn't find a server to talk to" failure. It looks like the above when TCP/IP communication is attempted. A common mistake is to forget to configure the server to allow TCP/ IP connections.

Alternatively, you might get this when attempting Unix-domain socket communication to a local server:

```
psql: error: connection to server on socket "/tmp/.s.PGSQL.5432"
 failed: No such file or directory
 Is the server running locally and accepting connections on
 that socket?
```

If the server is indeed running, check that the client's idea of the socket path (here /tmp) agrees with the server's [unix\\_socket\\_directories](#page-27-1) setting.

A connection failure message always shows the server address or socket path name, which is useful in verifying that the client is trying to connect to the right place. If there is in fact no server listening there, the kernel error message will typically be either Connection refused or No such file or directory, as illustrated. (It is important to realize that Connection refused in this context does *not* mean that the server got your connection request and rejected it. That case will produce a different message, as shown in [Section 21.15.](#page-125-0)) Other error messages such as Connection timed out might indicate more fundamental problems, like lack of network connectivity, or a firewall blocking the connection.