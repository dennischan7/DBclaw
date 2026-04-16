---
source: PostgreSQL 14 Reference
title: 00_Overview
---

A user able to modify the schema of subscriber-side tables can execute arbitrary code as a superuser. Limit ownership and TRIGGER privilege on such tables to roles that superusers trust. Moreover, if untrusted users can create tables, use only publications that list tables explicitly. That is to say, create a subscription FOR ALL TABLES only when superusers trust every user permitted to create a nontemp table on the publisher or the subscriber.

The role used for the replication connection must have the REPLICATION attribute (or be a superuser). If the role lacks SUPERUSER and BYPASSRLS, publisher row security policies can execute. If the role does not trust all table owners, include options=-crow\_security=off in the connection string; if a table owner then adds a row security policy, that setting will cause replication to halt rather than execute the policy. Access for the role must be configured in pg\_hba.conf and it must have the LOGIN attribute.

In order to be able to copy the initial table data, the role used for the replication connection must have the SELECT privilege on a published table (or be a superuser).

To create a publication, the user must have the CREATE privilege in the database.

To add tables to a publication, the user must have ownership rights on the table. To create a publication that publishes all tables automatically, the user must be a superuser.

To create a subscription, the user must be a superuser.

The subscription apply process will run in the local database with the privileges of a superuser.

Privileges are only checked once at the start of a replication connection. They are not re-checked as each change record is read from the publisher, nor are they re-checked for each change when applied.