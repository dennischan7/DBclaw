---
source: PostgreSQL 16 Reference
title: 00_Overview
---

In addition to setting global defaults or attaching overrides at the database or role level, you can pass settings to PostgreSQL via shell facilities. Both the server and libpq client library accept parameter values via the shell.

• During server startup, parameter settings can be passed to the postgres command via the -c command-line parameter. For example,

```
postgres -c log_connections=yes -c log_destination='syslog'
```

Settings provided in this way override those set via postgresql.conf or ALTER SYSTEM, so they cannot be changed globally without restarting the server.

• When starting a client session via libpq, parameter settings can be specified using the PGOPTIONS environment variable. Settings established in this way constitute defaults for the life of the session, but do not affect other sessions. For historical reasons, the format of PGOPTIONS is similar to that used when launching the postgres command; specifically, the -c flag must be specified. For example,

```
env PGOPTIONS="-c geqo=off -c statement_timeout=5min" psql
```

Other clients and libraries might provide their own mechanisms, via the shell or otherwise, that allow the user to alter session settings without direct use of SQL commands.