---
source: PostgreSQL 15 Reference
title: 00_Overview
---

To truncate a large object to a given length, call

```
int lo_truncate(PGconn *conn, int fd, size_t len);
```

This function truncates the large object descriptor fd to length len. The fd argument must have been returned by a previous lo\_open. If len is greater than the large object's current length, the large object is extended to the specified length with null bytes ('\0'). On success, lo\_truncate returns zero. On error, the return value is -1.

The read/write location associated with the descriptor fd is not changed.

Although the len parameter is declared as size\_t, lo\_truncate will reject length values larger than INT\_MAX.

When dealing with large objects that might exceed 2GB in size, instead use

```
int lo_truncate64(PGconn *conn, int fd, pg_int64 len);
```

This function has the same behavior as lo\_truncate, but it can accept a len value exceeding 2GB.

lo\_truncate is new as of PostgreSQL 8.3; if this function is run against an older server version, it will fail and return -1.

lo\_truncate64 is new as of PostgreSQL 9.3; if this function is run against an older server version, it will fail and return -1.