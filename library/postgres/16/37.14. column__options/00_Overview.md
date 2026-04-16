---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view column\_options contains all the options defined for foreign table columns in the current database. Only those foreign table columns are shown that the current user has access to (by way of being the owner or having some privilege).

**Table 37.12. column\_options Columns**

| Column Type<br>Description                                                                                         |
|--------------------------------------------------------------------------------------------------------------------|
| table_catalog sql_identifier<br>Name of the database that contains the foreign table (always the current database) |
| table_schema sql_identifier<br>Name of the schema that contains the foreign table                                  |
| table_name sql_identifier<br>Name of the foreign table                                                             |
| column_name sql_identifier<br>Name of the column                                                                   |
| option_name sql_identifier<br>Name of an option                                                                    |
| option_value character_data<br>Value of the option                                                                 |