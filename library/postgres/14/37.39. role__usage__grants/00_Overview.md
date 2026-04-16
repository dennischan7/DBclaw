---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view role\_usage\_grants identifies USAGE privileges granted on various kinds of objects where the grantor or grantee is a currently enabled role. Further information can be found under usage\_privileges. The only effective difference between this view and usage\_privileges is that this view omits objects that have been made accessible to the current user by way of a grant to PUBLIC.

### **Table 37.37. role\_usage\_grants Columns**

#### **Column Type**

#### **Description**

grantor sql\_identifier

The name of the role that granted the privilege

grantee sql\_identifier

The name of the role that the privilege was granted to

object\_catalog sql\_identifier

Name of the database containing the object (always the current database)

object\_schema sql\_identifier

### **Column Type Description** Name of the schema containing the object, if applicable, else an empty string object\_name sql\_identifier Name of the object object\_type character\_data COLLATION or DOMAIN or FOREIGN DATA WRAPPER or FOREIGN SERVER or SEQUENCE privilege\_type character\_data Always USAGE is\_grantable yes\_or\_no YES if the privilege is grantable, NO if not