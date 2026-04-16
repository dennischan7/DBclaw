---
source: PostgreSQL 15 Reference
title: 00_Overview
---

A user able to modify the schema of subscriber-side tables can execute arbitrary code as the role which owns any subscription which modifies those tables. Limit ownership and TRIGGER privilege on such tables to trusted roles. Moreover, if untrusted users can create tables, use only publications that list tables explicitly. That is to say, create a subscription FOR ALL TABLES or FOR TABLES IN SCHEMA only when superusers trust every user permitted to create a non-temp table on the publisher or the subscriber.

The role used for the replication connection must have the REPLICATION attribute (or be a superuser). If the role lacks SUPERUSER and BYPASSRLS, publisher row security policies can execute. If the role does not trust all table owners, include options=-crow\_security=off in the connection string; if a table owner then adds a row security policy, that setting will cause replication to halt rather than execute the policy. Access for the role must be configured in pg\_hba.conf and it must have the LOGIN attribute.

In order to be able to copy the initial table data, the role used for the replication connection must have the SELECT privilege on a published table (or be a superuser).

To create a publication, the user must have the CREATE privilege in the database.

To add tables to a publication, the user must have ownership rights on the table. To add all tables in schema to a publication, the user must be a superuser. To create a publication that publishes all tables or all tables in schema automatically, the user must be a superuser.

To create a subscription, the user must be a superuser.

The subscription apply process will run in the local database with the privileges of the subscription owner.

On the publisher, privileges are only checked once at the start of a replication connection and are not re-checked as each change record is read.

On the subscriber, the subscription owner's privileges are re-checked for each transaction when applied. If a worker is in the process of applying a transaction when the ownership of the subscription is changed by a concurrent transaction, the application of the current transaction will continue under the old owner's privileges.