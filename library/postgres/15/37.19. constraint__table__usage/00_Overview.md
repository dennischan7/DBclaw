---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view constraint\_table\_usage identifies all tables in the current database that are used by some constraint and are owned by a currently enabled role. (This is different from the view table\_constraints, which identifies all table constraints along with the table they are defined on.) For a foreign key constraint, this view identifies the table that the foreign key references. For a unique or primary key constraint, this view simply identifies the table the constraint belongs to. Check constraints and not-null constraints are not included in this view.

### **Table 37.17. constraint\_table\_usage Columns**

## **Column Type**

## **Description**

table\_catalog sql\_identifier

Name of the database that contains the table that is used by some constraint (always the current database)

table\_schema sql\_identifier

Name of the schema that contains the table that is used by some constraint

table\_name sql\_identifier

Name of the table that is used by some constraint

constraint\_catalog sql\_identifier

Name of the database that contains the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema that contains the constraint

constraint\_name sql\_identifier

Name of the constraint