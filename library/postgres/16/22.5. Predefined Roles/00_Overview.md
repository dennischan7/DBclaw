---
source: PostgreSQL 16 Reference
title: 00_Overview
---

PostgreSQL provides a set of predefined roles that provide access to certain, commonly needed, privileged capabilities and information. Administrators (including roles that have the CREATEROLE privilege) can GRANT these roles to users and/or other roles in their environment, providing those users with access to the specified capabilities and information.

The predefined roles are described in [Table 22.1](#page-152-0). Note that the specific permissions for each of the roles may change in the future as additional capabilities are added. Administrators should monitor the release notes for changes.

<span id="page-152-0"></span>

| Role              | Allowed Access                                                                                                                                                                                                                                                                                                                                |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pg_read_all_data  | Read all data (tables, views, sequences), as if having SELECT<br>rights on those objects, and USAGE rights on all schemas, even<br>without having it explicitly. This role does not have the role<br>attribute BYPASSRLS set. If RLS is being used, an adminis<br>trator may wish to set BYPASSRLS on roles which this role is<br>GRANTed to. |
| pg_write_all_data | Write all data (tables, views, sequences), as if having INSERT,<br>UPDATE, and DELETE rights on those objects, and USAGE<br>rights on all schemas, even without having it explicitly. This role                                                                                                                                               |

| Role                        | Allowed Access                                                                                                                                                     |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                             | does not have the role attribute BYPASSRLS set. If RLS is be<br>ing used, an administrator may wish to set BYPASSRLS on roles<br>which this role is GRANTed to.    |
| pg_read_all_settings        | Read all configuration variables, even those normally visible only<br>to superusers.                                                                               |
| pg_read_all_stats           | Read all pg_stat_* views and use various statistics related exten<br>sions, even those normally visible only to superusers.                                        |
| pg_stat_scan_tables         | Execute monitoring functions that may take ACCESS SHARE<br>locks on tables, potentially for a long time.                                                           |
| pg_monitor                  | Read/execute various monitoring views and functions. This role<br>is a member of pg_read_all_settings, pg_read_al<br>l_stats and pg_stat_scan_tables.              |
| pg_database_owner           | None. Membership consists, implicitly, of the current database<br>owner.                                                                                           |
| pg_signal_backend           | Signal another backend to cancel a query or terminate its session.                                                                                                 |
| pg_read_server_files        | Allow reading files from any location the database can access on<br>the server with COPY and other file-access functions.                                          |
| pg_write_server_files       | Allow writing to files in any location the database can access on<br>the server with COPY and other file-access functions.                                         |
| pg_execute_server_program   | Allow executing programs on the database server as the user the<br>database runs as with COPY and other functions which allow ex<br>ecuting a server-side program. |
| pg_checkpoint               | Allow executing the CHECKPOINT command.                                                                                                                            |
| pg_use_reserved_connections | Allow use of connection slots reserved via reserved_connections.                                                                                                   |
| pg_create_subscription      | Allow users with CREATE permission on the database to issue<br>CREATE SUBSCRIPTION.                                                                                |

The pg\_monitor, pg\_read\_all\_settings, pg\_read\_all\_stats and pg\_stat\_scan\_tables roles are intended to allow administrators to easily configure a role for the purpose of monitoring the database server. They grant a set of common privileges allowing the role to read various useful configuration settings, statistics and other system information normally restricted to superusers.

The pg\_database\_owner role has one implicit, situation-dependent member, namely the owner of the current database. Like any role, it can own objects or receive grants of access privileges. Consequently, once pg\_database\_owner has rights within a template database, each owner of a database instantiated from that template will exercise those rights. pg\_database\_owner cannot be a member of any role, and it cannot have non-implicit members. Initially, this role owns the public schema, so each database owner governs local use of the schema.

The pg\_signal\_backend role is intended to allow administrators to enable trusted, but non-superuser, roles to send signals to other backends. Currently this role enables sending of signals for canceling a query on another backend or terminating its session. A user granted this role cannot however send signals to a backend owned by a superuser. See Section 9.27.2.

The pg\_read\_server\_files, pg\_write\_server\_files and pg\_execute\_server\_program roles are intended to allow administrators to have trusted, but non-superuser, roles which are able to access files and run programs on the database server as the user the database runs as. As these roles are able to access any file on the server file system, they bypass all database-level permission checks when accessing files directly and they could be used to gain superuser-level access, therefore great care should be taken when granting these roles to users.

Care should be taken when granting these roles to ensure they are only used where needed and with the understanding that these roles grant access to privileged information.

Administrators can grant access to these roles to users using the GRANT command, for example:

GRANT pg\_signal\_backend TO admin\_user;