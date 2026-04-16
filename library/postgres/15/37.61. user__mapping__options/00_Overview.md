---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view user\_mapping\_options contains all the options defined for user mappings in the current database. Only those user mappings are shown where the current user has access to the corresponding foreign server (by way of being the owner or having some privilege).

### **Table 37.59. user\_mapping\_options Columns**

### **Column Type**

#### **Description**

authorization\_identifier sql\_identifier

Name of the user being mapped, or PUBLIC if the mapping is public

foreign\_server\_catalog sql\_identifier

Name of the database that the foreign server used by this mapping is defined in (always the current database)

foreign\_server\_name sql\_identifier

Name of the foreign server used by this mapping

option\_name sql\_identifier

Name of an option

option\_value character\_data

Value of the option. This column will show as null unless the current user is the user being mapped, or the mapping is for PUBLIC and the current user is the server owner, or the current user is a superuser. The intent is to protect password information stored as user mapping option.