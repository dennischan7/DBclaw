---
source: PostgreSQL 15 Reference
title: 00_Overview
---

While the server is running, it is not possible for a malicious user to take the place of the normal database server. However, when the server is down, it is possible for a local user to spoof the normal server by starting their own server. The spoof server could read passwords and queries sent by clients, but could not return any data because the PGDATA directory would still be secure because of directory permissions. Spoofing is possible because any user can start a database server; a client cannot identify an invalid server unless it is specially configured.

One way to prevent spoofing of local connections is to use a Unix domain socket directory [\(unix\\_socket\\_directories\)](#page-27-1) that has write permission only for a trusted local user. This prevents a malicious user from creating their own socket file in that directory. If you are concerned that some applications might still reference /tmp for the socket file and hence be vulnerable to spoofing, during operating system startup create a symbolic link /tmp/.s.PGSQL.5432 that points to the relocated socket file. You also might need to modify your /tmp cleanup script to prevent removal of the symbolic link.

Another option for local connections is for clients to use requirepeer to specify the required owner of the server process connected to the socket.

To prevent spoofing on TCP connections, either use SSL certificates and make sure that clients check the server's certificate, or use GSSAPI encryption (or both, if they're on separate connections).

To prevent spoofing with SSL, the server must be configured to accept only hostssl connections [\(Section 21.1\)](#page-105-1) and have SSL key and certificate files ([Section 19.9\)](#page-15-0). The TCP client must connect using sslmode=verify-ca or verify-full and have the appropriate root certificate file installed (Section 34.19.1).

To prevent spoofing with GSSAPI, the server must be configured to accept only hostgssenc connections ([Section 21.1\)](#page-105-1) and use gss authentication with them. The TCP client must connect using gssencmode=require.