---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view foreign\_servers contains all foreign servers defined in the current database. Only those foreign servers are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.27. foreign\_servers Columns**

```
Column Type
       Description
foreign_server_catalog sql_identifier
       Name of the database that the foreign server is defined in (always the current database)
```

foreign\_server\_name sql\_identifier

Name of the foreign server

foreign\_data\_wrapper\_catalog sql\_identifier

Name of the database that contains the foreign-data wrapper used by the foreign server (always the current database)

foreign\_data\_wrapper\_name sql\_identifier

Name of the foreign-data wrapper used by the foreign server

foreign\_server\_type character\_data

Foreign server type information, if specified upon creation

foreign\_server\_version character\_data

Foreign server version information, if specified upon creation

authorization\_identifier sql\_identifier

Name of the owner of the foreign server