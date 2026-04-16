---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view foreign\_data\_wrapper\_options contains all the options defined for foreign-data wrappers in the current database. Only those foreign-data wrappers are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.24. foreign\_data\_wrapper\_options Columns**

```
Column Type
       Description
foreign_data_wrapper_catalog sql_identifier
       Name of the database that the foreign-data wrapper is defined in (always the current
       database)
foreign_data_wrapper_name sql_identifier
       Name of the foreign-data wrapper
option_name sql_identifier
       Name of an option
option_value character_data
       Value of the option
```