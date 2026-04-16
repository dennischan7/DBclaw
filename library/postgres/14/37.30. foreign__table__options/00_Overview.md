---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view foreign\_table\_options contains all the options defined for foreign tables in the current database. Only those foreign tables are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.28. foreign\_table\_options Columns**

#### **Column Type Description**

foreign\_table\_catalog sql\_identifier

Name of the database that contains the foreign table (always the current database)

foreign\_table\_schema sql\_identifier

Name of the schema that contains the foreign table

foreign\_table\_name sql\_identifier

Name of the foreign table

option\_name sql\_identifier

Name of an option

option\_value character\_data

Value of the option