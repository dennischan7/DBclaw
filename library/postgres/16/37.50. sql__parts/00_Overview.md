---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The table sql\_parts contains information about which of the several parts of the SQL standard are supported by PostgreSQL.

#### **Table 37.48. sql\_parts Columns**

#### **Column Type**

#### **Description**

feature\_id character\_data

An identifier string containing the number of the part

feature\_name character\_data

#### **Column Type**

#### **Description**

Descriptive name of the part

is\_supported yes\_or\_no

YES if the part is fully supported by the current version of PostgreSQL, NO if not

is\_verified\_by character\_data

Always null, since the PostgreSQL development group does not perform formal testing of feature conformance

comments character\_data

Possibly a comment about the supported status of the part