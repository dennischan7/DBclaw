---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view routine\_sequence\_usage identifies all sequences that are used by a function or procedure, either in the SQL body or in parameter default expressions. (This only works for unquoted SQL bodies, not quoted bodies or functions in other languages.) A sequence is only included if that sequence is owned by a currently enabled role.

### **Table 37.41. routine\_sequence\_usage Columns**

## **Column Type**

#### **Description**

specific\_catalog sql\_identifier

Name of the database containing the function (always the current database)

specific\_schema sql\_identifier

Name of the schema containing the function

specific\_name sql\_identifier

The "specific name" of the function. See [Section 37.45](#page-149-0) for more information.

routine\_catalog sql\_identifier

Name of the database containing the function (always the current database)

routine\_schema sql\_identifier

Name of the schema containing the function

routine\_name sql\_identifier

Name of the function (might be duplicated in case of overloading)

schema\_catalog sql\_identifier

Name of the database that contains the sequence that is used by the function (always the current database)

sequence\_schema sql\_identifier

Name of the schema that contains the sequence that is used by the function

sequence\_name sql\_identifier

Name of the sequence that is used by the function