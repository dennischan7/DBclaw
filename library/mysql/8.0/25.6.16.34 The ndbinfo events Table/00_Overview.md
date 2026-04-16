---
source: MySQL 8.0 Reference
title: 00_Overview
---

This table provides information about event subscriptions in NDB. The columns of the events table are listed here, with short descriptions of each:

• event\_id

The event ID

• name

The name of the event

• table\_id

The ID of the table on which the event occurred

• reporting

One of updated, all, subscribe, or DDL

• columns

A comma-separated list of columns affected by the event

• table\_event

One or more of INSERT, DELETE, UPDATE, SCAN, DROP, ALTER, CREATE, GCP\_COMPLETE, CLUSTER\_FAILURE, STOP, NODE\_FAILURE, SUBSCRIBE, UNSUBSCRIBE, and ALL (defined by [Event::TableEvent](https://dev.mysql.com/doc/ndbapi/en/ndb-event.md#ndb-event-tableevent) in the NDB API)

The events table was added in NDB 8.0.29.