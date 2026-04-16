---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view key\_column\_usage identifies all columns in the current database that are restricted by some unique, primary key, or foreign key constraint. Check constraints are not included in this view. Only those columns are shown that the current user has access to, by way of being the owner or having some privilege.

### **Table 37.30. key\_column\_usage Columns**

## **Column Type**

**Description**

constraint\_catalog sql\_identifier

Name of the database that contains the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema that contains the constraint

constraint\_name sql\_identifier

Name of the constraint

table\_catalog sql\_identifier

Name of the database that contains the table that contains the column that is restricted by this constraint (always the current database)

table\_schema sql\_identifier

Name of the schema that contains the table that contains the column that is restricted by this constraint

table\_name sql\_identifier

Name of the table that contains the column that is restricted by this constraint

column\_name sql\_identifier

Name of the column that is restricted by this constraint

ordinal\_position cardinal\_number

Ordinal position of the column within the constraint key (count starts at 1)

position\_in\_unique\_constraint cardinal\_number

For a foreign-key constraint, ordinal position of the referenced column within its unique constraint (count starts at 1); otherwise null