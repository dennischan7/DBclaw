---
source: PostgreSQL 15 Reference
title: 00_Overview
---

To open an existing large object for reading or writing, call

```
int lo_open(PGconn *conn, Oid lobjId, int mode);
```

The lobjId argument specifies the OID of the large object to open. The mode bits control whether the object is opened for reading (INV\_READ), writing (INV\_WRITE), or both. (These symbolic constants are defined in the header file libpq/libpq-fs.h.) lo\_open returns a (non-negative) large object descriptor for later use in lo\_read, lo\_write, lo\_lseek, lo\_lseek64, lo\_tell, lo\_tell64, lo\_truncate, lo\_truncate64, and lo\_close. The descriptor is only valid for the duration of the current transaction. On failure, -1 is returned.

The server currently does not distinguish between modes INV\_WRITE and INV\_READ | IN-V\_WRITE: you are allowed to read from the descriptor in either case. However there is a significant difference between these modes and INV\_READ alone: with INV\_READ you cannot write on the descriptor, and the data read from it will reflect the contents of the large object at the time of the transaction snapshot that was active when lo\_open was executed, regardless of later writes by this or other transactions. Reading from a descriptor opened with INV\_WRITE returns data that reflects all writes of other committed transactions as well as writes of the current transaction. This is similar to the behavior of REPEATABLE READ versus READ COMMITTED transaction modes for ordinary SQL SELECT commands.

lo\_open will fail if SELECT privilege is not available for the large object, or if INV\_WRITE is specified and UPDATE privilege is not available. (Prior to PostgreSQL 11, these privilege checks were instead performed at the first actual read or write call using the descriptor.) These privilege checks can be disabled with the lo\_compat\_privileges run-time parameter.

An example:

```
inv_fd = lo_open(conn, inv_oid, INV_READ|INV_WRITE);
```