---
source: PostgreSQL 16 Reference
title: 00_Overview
---

libpq is reentrant and thread-safe by default. You might need to use special compiler command-line options when you compile your application code. Refer to your system's documentation for information about how to build thread-enabled applications, or look in src/Makefile.global for PTHREAD\_CFLAGS and PTHREAD\_LIBS. This function allows the querying of libpq's thread-safe status:

PQisthreadsafe

Returns the thread safety status of the libpq library.

```
int PQisthreadsafe();
```

Returns 1 if the libpq is thread-safe and 0 if it is not.

One thread restriction is that no two threads attempt to manipulate the same PGconn object at the same time. In particular, you cannot issue concurrent commands from different threads through the same connection object. (If you need to run concurrent commands, use multiple connections.)

PGresult objects are normally read-only after creation, and so can be passed around freely between threads. However, if you use any of the PGresult-modifying functions described in [Section 34.12](#page-1-2) or [Section 34.14,](#page-6-0) it's up to you to avoid concurrent operations on the same PGresult, too.

The deprecated functions PQrequestCancel and PQoidStatus are not thread-safe and should not be used in multithread programs. PQrequestCancel can be replaced by PQcancel. PQoidStatus can be replaced by PQoidValue.

If you are using Kerberos inside your application (in addition to inside libpq), you will need to do locking around Kerberos calls because Kerberos functions are not thread-safe. See function PQregisterThreadLock in the libpq source code for a way to do cooperative locking between libpq and your application.