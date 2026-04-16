---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view column\_privileges identifies all privileges granted on columns to a currently enabled role or by a currently enabled role. There is one row for each combination of column, grantor, and grantee.

If a privilege has been granted on an entire table, it will show up in this view as a grant for each column, but only for the privilege types where column granularity is possible: SELECT, INSERT, UPDATE, REFERENCES.

#### **Table 37.13. column\_privileges Columns**

| Column Type<br>Description                                                                                                             |
|----------------------------------------------------------------------------------------------------------------------------------------|
| grantor sql_identifier<br>Name of the role that granted the privilege                                                                  |
| grantee sql_identifier<br>Name of the role that the privilege was granted to                                                           |
| table_catalog sql_identifier<br>Name of the database that contains the table that contains the column (always the current<br>database) |
| table_schema sql_identifier<br>Name of the schema that contains the table that contains the column                                     |
| table_name sql_identifier<br>Name of the table that contains the column                                                                |
| column_name sql_identifier<br>Name of the column                                                                                       |
| privilege_type character_data<br>Type of the privilege: SELECT, INSERT, UPDATE, or REFERENCES                                          |
| is_grantable yes_or_no<br>YES if the privilege is grantable, NO if not                                                                 |