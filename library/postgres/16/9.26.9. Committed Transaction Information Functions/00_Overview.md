---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The functions shown in [Table 9.83](#page-28-1) provide information about when past transactions were committed. They only provide useful data when the track\_commit\_timestamp configuration option is enabled, and only for transactions that were committed after it was enabled. Commit timestamp information is routinely removed during vacuum.

<span id="page-28-1"></span>**Table 9.83. Committed Transaction Information Functions**

## **Function Description** pg\_xact\_commit\_timestamp ( xid ) → timestamp with time zone Returns the commit timestamp of a transaction. pg\_xact\_commit\_timestamp\_origin ( xid ) → record ( timestamp timestamp with time zone, roident oid) Returns the commit timestamp and replication origin of a transaction. pg\_last\_committed\_xact () → record ( xid xid, timestamp timestamp with time zone, roident oid ) Returns the transaction ID, commit timestamp and replication origin of the latest committed transaction.