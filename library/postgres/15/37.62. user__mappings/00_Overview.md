---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view user\_mappings contains all user mappings defined in the current database. Only those user mappings are shown where the current user has access to the corresponding foreign server (by way of being the owner or having some privilege).

### **Table 37.60. user\_mappings Columns**

#### **Column Type**

#### **Description**

authorization\_identifier sql\_identifier

Name of the user being mapped, or PUBLIC if the mapping is public

foreign\_server\_catalog sql\_identifier

Name of the database that the foreign server used by this mapping is defined in (always the current database)

foreign\_server\_name sql\_identifier

Name of the foreign server used by this mapping