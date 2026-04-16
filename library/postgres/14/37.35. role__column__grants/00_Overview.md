---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view role\_column\_grants identifies all privileges granted on columns where the grantor or grantee is a currently enabled role. Further information can be found under column\_privileges. The only effective difference between this view and column\_privileges is that this view omits columns that have been made accessible to the current user by way of a grant to PUBLIC.

### **Table 37.33. role\_column\_grants Columns**

#### **Column Type**

#### **Description**

grantor sql\_identifier

Name of the role that granted the privilege

grantee sql\_identifier

Name of the role that the privilege was granted to

table\_catalog sql\_identifier

Name of the database that contains the table that contains the column (always the current database)

table\_schema sql\_identifier

Name of the schema that contains the table that contains the column

table\_name sql\_identifier

Name of the table that contains the column

column\_name sql\_identifier

Name of the column

privilege\_type character\_data

Type of the privilege: SELECT, INSERT, UPDATE, or REFERENCES

is\_grantable yes\_or\_no

YES if the privilege is grantable, NO if not