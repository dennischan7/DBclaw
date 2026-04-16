---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_inherits records information about table and index inheritance hierarchies. There is one entry for each direct parent-child table or index relationship in the database. (Indirect inheritance can be determined by following chains of entries.)

### **Table 52.27. pg\_inherits Columns**

#### **Column Type Description**

inhrelid oid (references [pg\\_class](#page-8-0).oid)

The OID of the child table or index

inhparent oid (references [pg\\_class](#page-8-0).oid)

The OID of the parent table or index

inhseqno int4

#### **Description**

If there is more than one direct parent for a child table (multiple inheritance), this number tells the order in which the inherited columns are to be arranged. The count starts at 1. Indexes cannot have multiple inheritance, since they can only inherit when using declarative partitioning.

inhdetachpending bool

true for a partition that is in the process of being detached; false otherwise.