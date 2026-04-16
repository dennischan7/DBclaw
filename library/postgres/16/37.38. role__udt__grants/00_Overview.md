---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view role\_udt\_grants is intended to identify USAGE privileges granted on user-defined types where the grantor or grantee is a currently enabled role. Further information can be found under udt\_privileges. The only effective difference between this view and udt\_privileges is that this view omits objects that have been made accessible to the current user by way of a grant to PUBLIC. Since data types do not have real privileges in PostgreSQL, but only an implicit grant to PUBLIC, this view is empty.

#### **Table 37.36. role\_udt\_grants Columns**

### **Column Type Description** grantor sql\_identifier The name of the role that granted the privilege grantee sql\_identifier The name of the role that the privilege was granted to udt\_catalog sql\_identifier Name of the database containing the type (always the current database) udt\_schema sql\_identifier Name of the schema containing the type udt\_name sql\_identifier Name of the type privilege\_type character\_data Always TYPE USAGE is\_grantable yes\_or\_no