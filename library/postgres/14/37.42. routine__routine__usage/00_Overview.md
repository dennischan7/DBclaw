---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view routine\_routine\_usage identifies all functions or procedures that are used by another (or the same) function or procedure, either in the SQL body or in parameter default expressions. (This only works for unquoted SQL bodies, not quoted bodies or functions in other languages.) An entry is included here only if the used function is owned by a currently enabled role. (There is no such restriction on the using function.)

Note that the entries for both functions in the view refer to the "specific" name of the routine, even though the column names are used in a way that is inconsistent with other information schema views about routines. This is per SQL standard, although it is arguably a misdesign. See [Section 37.45](#page-125-0) for more information about specific names.

**Table 37.40. routine\_routine\_usage Columns**

```
Column Type
       Description
specific_catalog sql_identifier
       Name of the database containing the using function (always the current database)
specific_schema sql_identifier
       Name of the schema containing the using function
specific_name sql_identifier
       The "specific name" of the using function.
routine_catalog sql_identifier
       Name of the database that contains the function that is used by the first function (always
       the current database)
routine_schema sql_identifier
```

#### **Column Type**

#### **Description**

Name of the schema that contains the function that is used by the first function

routine\_name sql\_identifier

The "specific name" of the function that is used by the first function.