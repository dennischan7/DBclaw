---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view view\_column\_usage identifies all columns that are used in the query expression of a view (the SELECT statement that defines the view). A column is only included if the table that contains the column is owned by a currently enabled role.

### **Note**

Columns of system tables are not included. This should be fixed sometime.

### **Table 37.61. view\_column\_usage Columns**

```
Column Type
       Description
view_catalog sql_identifier
       Name of the database that contains the view (always the current database)
view_schema sql_identifier
       Name of the schema that contains the view
view_name sql_identifier
       Name of the view
table_catalog sql_identifier
       Name of the database that contains the table that contains the column that is used by the
       view (always the current database)
table_schema sql_identifier
       Name of the schema that contains the table that contains the column that is used by the
       view
table_name sql_identifier
       Name of the table that contains the column that is used by the view
column_name sql_identifier
       Name of the column that is used by the view
```