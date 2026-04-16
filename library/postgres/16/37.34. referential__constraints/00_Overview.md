---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view referential\_constraints contains all referential (foreign key) constraints in the current database. Only those constraints are shown for which the current user has write access to the referencing table (by way of being the owner or having some privilege other than SELECT).

#### **Table 37.32. referential\_constraints Columns**

#### **Column Type**

#### **Description**

constraint\_catalog sql\_identifier

Name of the database containing the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema containing the constraint

constraint\_name sql\_identifier

Name of the constraint

unique\_constraint\_catalog sql\_identifier

Name of the database that contains the unique or primary key constraint that the foreign key constraint references (always the current database)

unique\_constraint\_schema sql\_identifier

Name of the schema that contains the unique or primary key constraint that the foreign key constraint references

unique\_constraint\_name sql\_identifier

Name of the unique or primary key constraint that the foreign key constraint references

#### **Column Type**

#### **Description**

match\_option character\_data

Match option of the foreign key constraint: FULL, PARTIAL, or NONE.

update\_rule character\_data

Update rule of the foreign key constraint: CASCADE, SET NULL, SET DEFAULT, RESTRICT, or NO ACTION.

delete\_rule character\_data

Delete rule of the foreign key constraint: CASCADE, SET NULL, SET DEFAULT, RESTRICT, or NO ACTION.