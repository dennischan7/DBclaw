---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view constraint\_column\_usage identifies all columns in the current database that are used by some constraint. Only those columns are shown that are contained in a table owned by a currently enabled role. For a check constraint, this view identifies the columns that are used in the check expression. For a foreign key constraint, this view identifies the columns that the foreign key references. For a unique or primary key constraint, this view identifies the constrained columns.

### **Table 37.16. constraint\_column\_usage Columns**

### **Column Type Description** table\_catalog sql\_identifier Name of the database that contains the table that contains the column that is used by some constraint (always the current database) table\_schema sql\_identifier Name of the schema that contains the table that contains the column that is used by some constraint

table\_name sql\_identifier

Name of the table that contains the column that is used by some constraint

column\_name sql\_identifier

Name of the column that is used by some constraint

constraint\_catalog sql\_identifier

Name of the database that contains the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema that contains the constraint

constraint\_name sql\_identifier

Name of the constraint