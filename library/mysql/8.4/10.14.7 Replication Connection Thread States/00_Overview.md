---
source: MySQL 8.4 Reference
title: 00_Overview
---

These thread states occur on a replica server but are associated with connection threads, not with the I/O or SQL threads.

• Changing master

Changing replication source

The thread is processing a CHANGE REPLICATION SOURCE TO statement.

• Killing slave

The thread is processing a STOP REPLICA statement.

• Opening master dump table

This state occurs after Creating table from master dump.

• Reading master dump table data

This state occurs after Opening master dump table.

• Rebuilding the index on master dump table

This state occurs after Reading master dump table data.

### **10.14.8 NDB Cluster Thread States**

- Committing events to binlog
- Opening mysql.ndb\_apply\_status
- Processing events

The thread is processing events for binary logging.

• Processing events from schema table

The thread is doing the work of schema replication.

- Shutting down
- Syncing ndb table schema operation and binlog

This is used to have a correct binary log of schema operations for NDB.

• Waiting for allowed to take ndbcluster global schema lock

The thread is waiting for permission to take a global schema lock.

• Waiting for event from ndbcluster

The server is acting as an SQL node in an NDB Cluster, and is connected to a cluster management node.

• Waiting for first event from ndbcluster

- Waiting for ndbcluster binlog update to reach current position
- Waiting for ndbcluster global schema lock

The thread is waiting for a global schema lock held by another thread to be released.

- Waiting for ndbcluster to start
- Waiting for schema epoch

The thread is waiting for a schema epoch (that is, a global checkpoint).

### **10.14.9 Event Scheduler Thread States**

These states occur for the Event Scheduler thread, threads that are created to execute scheduled events, or threads that terminate the scheduler.

• Clearing

The scheduler thread or a thread that was executing an event is terminating and is about to end.

• Initialized

The scheduler thread or a thread that executes an event has been initialized.

• Waiting for next activation

The scheduler has a nonempty event queue but the next activation is in the future.

• Waiting for scheduler to stop

The thread issued SET GLOBAL event\_scheduler=OFF and is waiting for the scheduler to stop.

• Waiting on empty queue

The scheduler's event queue is empty and it is sleeping.