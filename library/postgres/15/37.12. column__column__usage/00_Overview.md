---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view column\_column\_usage identifies all generated columns that depend on another base column in the same table. Only tables owned by a currently enabled role are included.

**Table 37.10. column\_column\_usage Columns**

```
Column Type
       Description
table_catalog sql_identifier
       Name of the database containing the table (always the current database)
table_schema sql_identifier
       Name of the schema containing the table
table_name sql_identifier
       Name of the table
column_name sql_identifier
       Name of the base column that a generated column depends on
dependent_column sql_identifier
       Name of the generated column
```