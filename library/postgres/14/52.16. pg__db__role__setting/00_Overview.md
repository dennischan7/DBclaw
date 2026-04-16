---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The catalog pg\_db\_role\_setting records the default values that have been set for run-time configuration variables, for each role and database combination.

Unlike most system catalogs, pg\_db\_role\_setting is shared across all databases of a cluster: there is only one copy of pg\_db\_role\_setting per cluster, not one per database.

### **Table 52.16. pg\_db\_role\_setting Columns**

## **Column Type Description** setdatabase oid (references [pg\\_database](#page-13-0).oid) The OID of the database the setting is applicable to, or zero if not database-specific setrole oid (references [pg\\_authid](#page-5-0).oid) The OID of the role the setting is applicable to, or zero if not role-specific setconfig text[] Defaults for run-time configuration variables