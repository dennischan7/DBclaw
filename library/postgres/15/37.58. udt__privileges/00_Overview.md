---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view udt\_privileges identifies USAGE privileges granted on user-defined types to a currently enabled role or by a currently enabled role. There is one row for each combination of type, grantor, and grantee. This view shows only composite types (see under [Section 37.60](#page-162-0) for why); see [Section 37.59](#page-161-0) for domain privileges.

### **Table 37.56. udt\_privileges Columns**

```
Column Type
       Description
grantor sql_identifier
       Name of the role that granted the privilege
grantee sql_identifier
       Name of the role that the privilege was granted to
udt_catalog sql_identifier
       Name of the database containing the type (always the current database)
udt_schema sql_identifier
       Name of the schema containing the type
udt_name sql_identifier
       Name of the type
privilege_type character_data
       Always TYPE USAGE
is_grantable yes_or_no
       YES if the privilege is grantable, NO if not
```

# <span id="page-161-0"></span>**37.59. usage\_privileges**

The view usage\_privileges identifies USAGE privileges granted on various kinds of objects to a currently enabled role or by a currently enabled role. In PostgreSQL, this currently applies to collations, domains, foreign-data wrappers, foreign servers, and sequences. There is one row for each combination of object, grantor, and grantee.

Since collations do not have real privileges in PostgreSQL, this view shows implicit non-grantable USAGE privileges granted by the owner to PUBLIC for all collations. The other object types, however, show real privileges.

In PostgreSQL, sequences also support SELECT and UPDATE privileges in addition to the USAGE privilege. These are nonstandard and therefore not visible in the information schema.

### **Table 37.57. usage\_privileges Columns**

```
Column Type
       Description
grantor sql_identifier
       Name of the role that granted the privilege
grantee sql_identifier
       Name of the role that the privilege was granted to
object_catalog sql_identifier
       Name of the database containing the object (always the current database)
object_schema sql_identifier
       Name of the schema containing the object, if applicable, else an empty string
object_name sql_identifier
       Name of the object
object_type character_data
       COLLATION or DOMAIN or FOREIGN DATA WRAPPER or FOREIGN SERVER or
       SEQUENCE
privilege_type character_data
       Always USAGE
is_grantable yes_or_no
       YES if the privilege is grantable, NO if not
```

# <span id="page-162-0"></span>**37.60. user\_defined\_types**

The view user\_defined\_types currently contains all composite types defined in the current database. Only those types are shown that the current user has access to (by way of being the owner or having some privilege).

SQL knows about two kinds of user-defined types: structured types (also known as composite types in PostgreSQL) and distinct types (not implemented in PostgreSQL). To be future-proof, use the column user\_defined\_type\_category to differentiate between these. Other user-defined types such as base types and enums, which are PostgreSQL extensions, are not shown here. For domains, see [Section 37.23](#page-133-0) instead.

### **Table 37.58. user\_defined\_types Columns**

```
Column Type
       Description
user_defined_type_catalog sql_identifier
       Name of the database that contains the type (always the current database)
user_defined_type_schema sql_identifier
       Name of the schema that contains the type
user_defined_type_name sql_identifier
       Name of the type
user_defined_type_category character_data
       Currently always STRUCTURED
is_instantiable yes_or_no
       Applies to a feature not available in PostgreSQL
is_final yes_or_no
       Applies to a feature not available in PostgreSQL
ordering_form character_data
       Applies to a feature not available in PostgreSQL
```

```
Column Type
       Description
ordering_category character_data
       Applies to a feature not available in PostgreSQL
ordering_routine_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
ordering_routine_schema sql_identifier
       Applies to a feature not available in PostgreSQL
ordering_routine_name sql_identifier
       Applies to a feature not available in PostgreSQL
reference_type character_data
       Applies to a feature not available in PostgreSQL
data_type character_data
       Applies to a feature not available in PostgreSQL
character_maximum_length cardinal_number
       Applies to a feature not available in PostgreSQL
character_octet_length cardinal_number
       Applies to a feature not available in PostgreSQL
character_set_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
character_set_schema sql_identifier
       Applies to a feature not available in PostgreSQL
character_set_name sql_identifier
       Applies to a feature not available in PostgreSQL
collation_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
collation_schema sql_identifier
       Applies to a feature not available in PostgreSQL
collation_name sql_identifier
       Applies to a feature not available in PostgreSQL
numeric_precision cardinal_number
       Applies to a feature not available in PostgreSQL
numeric_precision_radix cardinal_number
       Applies to a feature not available in PostgreSQL
numeric_scale cardinal_number
       Applies to a feature not available in PostgreSQL
datetime_precision cardinal_number
       Applies to a feature not available in PostgreSQL
interval_type character_data
       Applies to a feature not available in PostgreSQL
interval_precision cardinal_number
       Applies to a feature not available in PostgreSQL
source_dtd_identifier sql_identifier
       Applies to a feature not available in PostgreSQL
ref_dtd_identifier sql_identifier
       Applies to a feature not available in PostgreSQL
```