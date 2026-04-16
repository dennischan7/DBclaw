---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view table\_constraints contains all constraints belonging to tables that the current user owns or has some privilege other than SELECT on.

### **Table 37.50. table\_constraints Columns**

#### **Column Type**

#### **Description**

constraint\_catalog sql\_identifier

Name of the database that contains the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema that contains the constraint

constraint\_name sql\_identifier

Name of the constraint

table\_catalog sql\_identifier

Name of the database that contains the table (always the current database)

table\_schema sql\_identifier

Name of the schema that contains the table

### **Column Type Description** table\_name sql\_identifier Name of the table constraint\_type character\_data Type of the constraint: CHECK, FOREIGN KEY, PRIMARY KEY, or UNIQUE is\_deferrable yes\_or\_no YES if the constraint is deferrable, NO if not initially\_deferred yes\_or\_no YES if the constraint is deferrable and initially deferred, NO if not enforced yes\_or\_no Applies to a feature not available in PostgreSQL (currently always YES) nulls\_distinct yes\_or\_no If the constraint is a unique constraint, then YES if the constraint treats nulls as distinct or NO if it treats nulls as not distinct, otherwise null for other types of constraints.