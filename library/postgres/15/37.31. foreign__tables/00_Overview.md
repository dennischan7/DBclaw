---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view foreign\_tables contains all foreign tables defined in the current database. Only those foreign tables are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.29. foreign\_tables Columns**

#### **Column Type**

#### **Description**

foreign\_table\_catalog sql\_identifier

Name of the database that the foreign table is defined in (always the current database)

foreign\_table\_schema sql\_identifier

Name of the schema that contains the foreign table

foreign\_table\_name sql\_identifier

### **Column Type**

#### **Description**

Name of the foreign table

foreign\_server\_catalog sql\_identifier

Name of the database that the foreign server is defined in (always the current database)

foreign\_server\_name sql\_identifier

Name of the foreign server