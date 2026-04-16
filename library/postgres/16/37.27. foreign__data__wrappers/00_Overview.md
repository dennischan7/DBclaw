---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view foreign\_data\_wrappers contains all foreign-data wrappers defined in the current database. Only those foreign-data wrappers are shown that the current user has access to (by way of being the owner or having some privilege).

#### **Table 37.25. foreign\_data\_wrappers Columns**

### **Column Type Description** foreign\_data\_wrapper\_catalog sql\_identifier Name of the database that contains the foreign-data wrapper (always the current database) foreign\_data\_wrapper\_name sql\_identifier Name of the foreign-data wrapper authorization\_identifier sql\_identifier Name of the owner of the foreign server library\_name character\_data File name of the library that implementing this foreign-data wrapper foreign\_data\_wrapper\_language character\_data Language used to implement this foreign-data wrapper