---
source: PostgreSQL 14 Reference
title: 00_Overview
---

Logical replication starts by copying a snapshot of the data on the publisher database. Once that is done, changes on the publisher are sent to the subscriber as they occur in real time. The subscriber applies data in the order in which commits were made on the publisher so that transactional consistency is guaranteed for the publications within any single subscription.

Logical replication is built with an architecture similar to physical streaming replication (see Section 27.2.5). It is implemented by "walsender" and "apply" processes. The walsender process starts logical decoding (described in Chapter 49) of the WAL and loads the standard logical decoding output plugin (pgoutput). The plugin transforms the changes read from WAL to the logical replication protocol (see Section 53.5) and filters the data according to the publication specification. The data is then continuously transferred using the streaming replication protocol to the apply worker, which maps the data to local tables and applies the individual changes as they are received, in correct transactional order.

The apply process on the subscriber database always runs with session\_replication\_role set to replica. This means that, by default, triggers and rules will not fire on a subscriber. Users can optionally choose to enable triggers and rules on a table using the ALTER TABLE command and the ENABLE TRIGGER and ENABLE RULE clauses.

The logical replication apply process currently only fires row triggers, not statement triggers. The initial table synchronization, however, is implemented like a COPY command and thus fires both row and statement triggers for INSERT.