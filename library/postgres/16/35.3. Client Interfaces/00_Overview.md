---
source: PostgreSQL 16 Reference
title: 00_Overview
---

This section describes the facilities that PostgreSQL's libpq client interface library provides for accessing large objects. The PostgreSQL large object interface is modeled after the Unix file-system interface, with analogues of open, read, write, lseek, etc.

All large object manipulation using these functions *must* take place within an SQL transaction block, since large object file descriptors are only valid for the duration of a transaction. Write operations, including lo\_open with the INV\_WRITE mode, are not allowed in a read-only transaction.

If an error occurs while executing any one of these functions, the function will return an otherwise-impossible value, typically 0 or -1. A message describing the error is stored in the connection object and can be retrieved with PQerrorMessage.

Client applications that use these functions should include the header file libpq/libpq-fs.h and link with the libpq library.

Client applications cannot use these functions while a libpq connection is in pipeline mode.