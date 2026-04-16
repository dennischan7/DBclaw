---
source: PostgreSQL 15 Reference
title: 00_Overview
---

To obtain the current read or write location of a large object descriptor, call

```
int lo_tell(PGconn *conn, int fd);
```

If there is an error, the return value is -1.

When dealing with large objects that might exceed 2GB in size, instead use

```
pg_int64 lo_tell64(PGconn *conn, int fd);
```

This function has the same behavior as lo\_tell, but it can deliver a result larger than 2GB. Note that lo\_tell will fail if the current read/write location is greater than 2GB.

lo\_tell64 is new as of PostgreSQL 9.3. If this function is run against an older server version, it will fail and return -1.