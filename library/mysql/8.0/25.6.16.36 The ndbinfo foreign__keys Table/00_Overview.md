---
source: MySQL 8.0 Reference
title: 00_Overview
---

The foreign\_keys table provides information about foreign keys on NDB tables. This table has the following columns:

• object\_id

The foreign key's object ID

• name

Name of the foreign key

• parent\_table

The name of the foreign key's parent table

• parent\_columns

A comma-delimited list of parent columns

• child\_table

The name of the child table

• child\_columns

A comma-separated list of child columns

• parent\_index

Name of the parent index

• child\_index

Name of the child index

• on\_update\_action

The ON UPDATE action specified for the foreign key; one of No Action, Restrict, Cascade, Set Null, or Set Default

• on\_delete\_action

The ON DELETE action specified for the foreign key; one of No Action, Restrict, Cascade, Set Null, or Set Default

The foreign\_keys table was added in NDB 8.0.29.