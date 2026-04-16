---
source: PostgreSQL 16 Reference
title: 00_Overview
---

To run the tests after installation (see Chapter 17), initialize a data directory and start the server as explained in Chapter 19, then type:

make installcheck

or for a parallel test:

make installcheck-parallel

The tests will expect to contact the server at the local host and the default port number, unless directed otherwise by PGHOST and PGPORT environment variables. The tests will be run in a database named regression; any existing database by this name will be dropped.

The tests will also transiently create some cluster-wide objects, such as roles, tablespaces, and subscriptions. These objects will have names beginning with regress\_. Beware of using installcheck mode with an installation that has any actual global objects named that way.