---
source: PostgreSQL 15 Reference
title: 00_Overview
---

To close a connection, use the following statement:

```
EXEC SQL DISCONNECT [connection];
```

The connection can be specified in the following ways:

- connection-name
- CURRENT
- ALL

If no connection name is specified, the current connection is closed.

It is good style that an application always explicitly disconnect from every connection it opened.

# <span id="page-14-0"></span>**36.3. Running SQL Commands**

Any SQL command can be run from within an embedded SQL application. Below are some examples of how to do that.