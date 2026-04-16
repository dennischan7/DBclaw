---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view transforms contains information about the transforms defined in the current database. More precisely, it contains a row for each function contained in a transform (the "from SQL" or "to SQL" function).

### **Table 37.53. transforms Columns**

```
Column Type
       Description
udt_catalog sql_identifier
       Name of the database that contains the type the transform is for (always the current data-
       base)
udt_schema sql_identifier
       Name of the schema that contains the type the transform is for
udt_name sql_identifier
       Name of the type the transform is for
specific_catalog sql_identifier
```

### **Column Type**

#### **Description**

Name of the database containing the function (always the current database)

specific\_schema sql\_identifier

Name of the schema containing the function

specific\_name sql\_identifier

The "specific name" of the function. See [Section 37.45](#page-149-0) for more information.

group\_name sql\_identifier

The SQL standard allows defining transforms in "groups", and selecting a group at run time. PostgreSQL does not support this. Instead, transforms are specific to a language. As a compromise, this field contains the language the transform is for.

transform\_type character\_data FROM SQL or TO SQL