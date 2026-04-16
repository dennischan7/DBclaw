---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view check\_constraints contains all check constraints, either defined on a table or on a domain, that are owned by a currently enabled role. (The owner of the table or domain is the owner of the constraint.)

### **Table 37.7. check\_constraints Columns**

#### **Column Type**

#### **Description**

constraint\_catalog sql\_identifier

### **Column Type Description** Name of the database containing the constraint (always the current database) constraint\_schema sql\_identifier Name of the schema containing the constraint constraint\_name sql\_identifier Name of the constraint check\_clause character\_data The check expression of the check constraint