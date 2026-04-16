---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view column\_domain\_usage identifies all columns (of a table or a view) that make use of some domain defined in the current database and owned by a currently enabled role.

**Table 37.11. column\_domain\_usage Columns**

```
Column Type
       Description
domain_catalog sql_identifier
       Name of the database containing the domain (always the current database)
domain_schema sql_identifier
       Name of the schema containing the domain
domain_name sql_identifier
       Name of the domain
table_catalog sql_identifier
       Name of the database containing the table (always the current database)
table_schema sql_identifier
       Name of the schema containing the table
table_name sql_identifier
       Name of the table
column_name sql_identifier
       Name of the column
```