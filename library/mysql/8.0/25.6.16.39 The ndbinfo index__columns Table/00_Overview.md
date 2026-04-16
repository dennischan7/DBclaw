---
source: MySQL 8.0 Reference
title: 00_Overview
---

This table provides information about indexes on NDB tables. The columns of the index\_columns table are listed here, along with brief descriptions:

• table\_id

Unique ID of the NDB table for which the index is defined

• Name of the database containing this table

varchar(64)

• table\_name

Name of the table

• index\_object\_id

Object ID of this index

• index\_name

Name of the index; if the index is not named, the name of the first column in the index is used

• index\_type

Type of index; normally this is 3 (unique hash index) or 6 (ordered index); the values are the same as those in the type\_id column of the [dict\\_obj\\_types](#page-157-0) table

• status

One of new, changed, retrieved, invalid, or altered

• columns

A comma-delimited list of columns making up the index

The index\_columns table was added in NDB 8.0.29.