---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_subscription\_rel contains the state for each replicated relation in each subscription. This is a many-to-many mapping.

This catalog only contains tables known to the subscription after running either CREATE SUBSCRIPTION or ALTER SUBSCRIPTION ... REFRESH PUBLICATION.

### **Table 52.53. pg\_subscription\_rel Columns**

#### **Column Type**

#### **Description**

srsubid oid (references [pg\\_subscription](#page-39-1).oid)

Reference to subscription

srrelid oid (references [pg\\_class](#page-8-0).oid)

Reference to relation

srsubstate char

#### **Description**

State code: i = initialize, d = data is being copied, f = finished table copy, s = synchronized, r = ready (normal replication)

srsublsn pg\_lsn

Remote LSN of the state change used for synchronization coordination when in s or r states, otherwise null

# <span id="page-41-0"></span>**52.54. pg\_tablespace**

The catalog pg\_tablespace stores information about the available tablespaces. Tables can be placed in particular tablespaces to aid administration of disk layout.

Unlike most system catalogs, pg\_tablespace is shared across all databases of a cluster: there is only one copy of pg\_tablespace per cluster, not one per database.

### **Table 52.54. pg\_tablespace Columns**

### **Column Type**

#### **Description**

oid oid

Row identifier

spcname name

Tablespace name

spcowner oid (references [pg\\_authid](#page-5-0).oid)

Owner of the tablespace, usually the user who created it

spcacl aclitem[]

Access privileges; see Section 5.7 for details

spcoptions text[]

Tablespace-level options, as "keyword=value" strings