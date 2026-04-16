---
source: PostgreSQL 14 Reference
title: 00_Overview
---

Logical replication behaves similarly to normal DML operations in that the data will be updated even if it was changed locally on the subscriber node. If incoming data violates any constraints the replication will stop. This is referred to as a *conflict*. When replicating UPDATE or DELETE operations, missing data will not produce a conflict and such operations will simply be skipped.

A conflict will produce an error and will stop the replication; it must be resolved manually by the user. Details about the conflict can be found in the subscriber's server log.

The resolution can be done either by changing data on the subscriber so that it does not conflict with the incoming change or by skipping the transaction that conflicts with the existing data. The transaction can be skipped by calling the pg\_replication\_origin\_advance() function with a node\_name corresponding to the subscription name, and a position. The current position of origins can be seen in the pg\_replication\_origin\_status system view.