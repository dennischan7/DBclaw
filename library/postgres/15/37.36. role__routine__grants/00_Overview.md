---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view role\_routine\_grants identifies all privileges granted on functions where the grantor or grantee is a currently enabled role. Further information can be found under routine\_privileges. The only effective difference between this view and routine\_privileges is that this view omits functions that have been made accessible to the current user by way of a grant to PUBLIC.

### **Table 37.34. role\_routine\_grants Columns**

#### **Column Type**

#### **Description**

grantor sql\_identifier

## **Column Type Description** Name of the role that granted the privilege grantee sql\_identifier Name of the role that the privilege was granted to specific\_catalog sql\_identifier Name of the database containing the function (always the current database) specific\_schema sql\_identifier Name of the schema containing the function specific\_name sql\_identifier The "specific name" of the function. See [Section 37.45](#page-149-0) for more information. routine\_catalog sql\_identifier Name of the database containing the function (always the current database) routine\_schema sql\_identifier Name of the schema containing the function routine\_name sql\_identifier Name of the function (might be duplicated in case of overloading) privilege\_type character\_data Always EXECUTE (the only privilege type for functions) is\_grantable yes\_or\_no YES if the privilege is grantable, NO if not