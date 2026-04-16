---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view view\_table\_usage identifies all tables that are used in the query expression of a view (the SELECT statement that defines the view). A table is only included if that table is owned by a currently enabled role.

### **Note**

System tables are not included. This should be fixed sometime.

### **Table 37.63. view\_table\_usage Columns**

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
       Name of the database that contains the table that is used by the view (always the current
       database)
table_schema sql_identifier
       Name of the schema that contains the table that is used by the view
table_name sql_identifier
       Name of the table that is used by the view
```