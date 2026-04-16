---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The function

```
int lo_read(PGconn *conn, int fd, char *buf, size_t len);
```

reads up to len bytes from large object descriptor fd into buf (which must be of size len). The fd argument must have been returned by a previous lo\_open. The number of bytes actually read is returned; this will be less than len if the end of the large object is reached first. In the event of an error, the return value is -1.

Although the len parameter is declared as size\_t, this function will reject length values larger than INT\_MAX. In practice, it's best to transfer data in chunks of at most a few megabytes anyway.