---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view domain\_constraints contains all constraints belonging to domains defined in the current database. Only those domains are shown that the current user has access to (by way of being the owner or having some privilege).

#### **Table 37.19. domain\_constraints Columns**

#### **Column Type**

**Description**

constraint\_catalog sql\_identifier

Name of the database that contains the constraint (always the current database)

constraint\_schema sql\_identifier

Name of the schema that contains the constraint

constraint\_name sql\_identifier

Name of the constraint

domain\_catalog sql\_identifier

Name of the database that contains the domain (always the current database)

domain\_schema sql\_identifier

Name of the schema that contains the domain

domain\_name sql\_identifier

Name of the domain

is\_deferrable yes\_or\_no

YES if the constraint is deferrable, NO if not

initially\_deferred yes\_or\_no

YES if the constraint is deferrable and initially deferred, NO if not