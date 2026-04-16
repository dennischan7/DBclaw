---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The function

```
Oid lo_create(PGconn *conn, Oid lobjId);
```

creates a new large object. The OID to be assigned can be specified by lobjId; if so, failure occurs if that OID is already in use for some large object. If lobjId is InvalidOid (zero) then lo\_create assigns an unused OID. The return value is the OID that was assigned to the new large object, or InvalidOid (zero) on failure.

An example:

```
inv_oid = lo_create(conn, desired_oid);
 The older function
```

Oid lo\_creat(PGconn \*conn, int mode);

also creates a new large object, always assigning an unused OID. The return value is the OID that was assigned to the new large object, or InvalidOid (zero) on failure.

In PostgreSQL releases 8.1 and later, the mode is ignored, so that lo\_creat is exactly equivalent to lo\_create with a zero second argument. However, there is little reason to use lo\_creat unless you need to work with servers older than 8.1. To work with such an old server, you must use lo\_creat not lo\_create, and you must set mode to one of INV\_READ, INV\_WRITE, or INV\_READ | INV\_WRITE. (These symbolic constants are defined in the header file libpq/libpq-fs.h.)

An example:

```
inv_oid = lo_creat(conn, INV_READ|INV_WRITE);
```