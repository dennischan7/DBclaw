---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL has native support for using SSL connections to encrypt client/server communications using TLS protocols for increased security. See Section 19.9 for details about the server-side SSL functionality.

libpq reads the system-wide OpenSSL configuration file. By default, this file is named openssl.cnf and is located in the directory reported by openssl version -d. This default can be overridden by setting environment variable OPENSSL\_CONF to the name of the desired configuration file.