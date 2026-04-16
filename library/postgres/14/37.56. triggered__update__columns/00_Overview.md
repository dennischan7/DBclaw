---
source: PostgreSQL 14 Reference
title: 00_Overview
---

For triggers in the current database that specify a column list (like UPDATE OF column1, column2), the view triggered\_update\_columns identifies these columns. Triggers that do not specify a column list are not included in this view. Only those columns are shown that the current user owns or has some privilege other than SELECT on.

### **Table 37.54. triggered\_update\_columns Columns**

### **Column Type**

#### **Description**

trigger\_catalog sql\_identifier

Name of the database that contains the trigger (always the current database)

trigger\_schema sql\_identifier

Name of the schema that contains the trigger

trigger\_name sql\_identifier

Name of the trigger

event\_object\_catalog sql\_identifier

Name of the database that contains the table that the trigger is defined on (always the current database)

event\_object\_schema sql\_identifier

Name of the schema that contains the table that the trigger is defined on

event\_object\_table sql\_identifier

Name of the table that the trigger is defined on

event\_object\_column sql\_identifier

Name of the column that the trigger is defined on