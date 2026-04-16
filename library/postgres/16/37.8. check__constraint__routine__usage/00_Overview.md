---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view check\_constraint\_routine\_usage identifies routines (functions and procedures) that are used by a check constraint. Only those routines are shown that are owned by a currently enabled role.

#### **Table 37.6. check\_constraint\_routine\_usage Columns**

#### **Column Type**

#### **Description**

constraint\_catalog sql\_identifier

Name of the database containing the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema containing the constraint

constraint\_name sql\_identifier

Name of the constraint

specific\_catalog sql\_identifier

Name of the database containing the function (always the current database)

specific\_schema sql\_identifier

Name of the schema containing the function

specific\_name sql\_identifier

The "specific name" of the function. See [Section 37.45](#page-185-0) for more information.