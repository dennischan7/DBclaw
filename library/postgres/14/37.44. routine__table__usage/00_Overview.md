---
source: PostgreSQL 14 Reference
title: 00_Overview
---

The view routine\_table\_usage is meant to identify all tables that are used by a function or procedure. This information is currently not tracked by PostgreSQL.

### **Table 37.42. routine\_table\_usage Columns**

#### **Column Type**

#### **Description**

specific\_catalog sql\_identifier

Name of the database containing the function (always the current database)

specific\_schema sql\_identifier

Name of the schema containing the function

specific\_name sql\_identifier

The "specific name" of the function. See [Section 37.45](#page-125-0) for more information.

routine\_catalog sql\_identifier

Name of the database containing the function (always the current database)

routine\_schema sql\_identifier

Name of the schema containing the function

routine\_name sql\_identifier

Name of the function (might be duplicated in case of overloading)

table\_catalog sql\_identifier

Name of the database that contains the table that is used by the function (always the current database)

table\_schema sql\_identifier

Name of the schema that contains the table that is used by the function

table\_name sql\_identifier

Name of the table that is used by the function

# <span id="page-125-0"></span>**37.45. routines**

The view routines contains all functions and procedures in the current database. Only those functions and procedures are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.43. routines Columns**

#### **Column Type**

#### **Description**

specific\_catalog sql\_identifier

Name of the database containing the function (always the current database)

specific\_schema sql\_identifier

Name of the schema containing the function

specific\_name sql\_identifier

The "specific name" of the function. This is a name that uniquely identifies the function in the schema, even if the real name of the function is overloaded. The format of the specific name is not defined, it should only be used to compare it to other instances of specific routine names.

routine\_catalog sql\_identifier

Name of the database containing the function (always the current database)

routine\_schema sql\_identifier

Name of the schema containing the function

routine\_name sql\_identifier

Name of the function (might be duplicated in case of overloading)

routine\_type character\_data

FUNCTION for a function, PROCEDURE for a procedure

module\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

module\_schema sql\_identifier

Applies to a feature not available in PostgreSQL

module\_name sql\_identifier

Applies to a feature not available in PostgreSQL

udt\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

```
Column Type
       Description
udt_schema sql_identifier
       Applies to a feature not available in PostgreSQL
udt_name sql_identifier
       Applies to a feature not available in PostgreSQL
data_type character_data
       Return data type of the function, if it is a built-in type, or ARRAY if it is some array (in
       that case, see the view element_types), else USER-DEFINED (in that case, the type
       is identified in type_udt_name and associated columns). Null for a procedure.
character_maximum_length cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
character_octet_length cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
character_set_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
character_set_schema sql_identifier
       Applies to a feature not available in PostgreSQL
character_set_name sql_identifier
       Applies to a feature not available in PostgreSQL
collation_catalog sql_identifier
       Always null, since this information is not applied to return data types in PostgreSQL
collation_schema sql_identifier
       Always null, since this information is not applied to return data types in PostgreSQL
collation_name sql_identifier
       Always null, since this information is not applied to return data types in PostgreSQL
numeric_precision cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
numeric_precision_radix cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
numeric_scale cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
datetime_precision cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
interval_type character_data
       Always null, since this information is not applied to return data types in PostgreSQL
interval_precision cardinal_number
       Always null, since this information is not applied to return data types in PostgreSQL
type_udt_catalog sql_identifier
       Name of the database that the return data type of the function is defined in (always the
       current database). Null for a procedure.
type_udt_schema sql_identifier
       Name of the schema that the return data type of the function is defined in. Null for a pro-
       cedure.
type_udt_name sql_identifier
       Name of the return data type of the function. Null for a procedure.
scope_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
```

scope\_schema sql\_identifier

```
Column Type
```

#### **Description**

Applies to a feature not available in PostgreSQL

scope\_name sql\_identifier

Applies to a feature not available in PostgreSQL

maximum\_cardinality cardinal\_number

Always null, because arrays always have unlimited maximum cardinality in PostgreSQL

dtd\_identifier sql\_identifier

An identifier of the data type descriptor of the return data type of this function, unique among the data type descriptors pertaining to the function. This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)

routine\_body character\_data

If the function is an SQL function, then SQL, else EXTERNAL.

routine\_definition character\_data

The source text of the function (null if the function is not owned by a currently enabled role). (According to the SQL standard, this column is only applicable if routine\_body is SQL, but in PostgreSQL it will contain whatever source text was specified when the function was created.)

external\_name character\_data

If this function is a C function, then the external name (link symbol) of the function; else null. (This works out to be the same value that is shown in routine\_definition.)

external\_language character\_data

The language the function is written in

parameter\_style character\_data

Always GENERAL (The SQL standard defines other parameter styles, which are not available in PostgreSQL.)

is\_deterministic yes\_or\_no

If the function is declared immutable (called deterministic in the SQL standard), then YES, else NO. (You cannot query the other volatility levels available in PostgreSQL through the information schema.)

sql\_data\_access character\_data

Always MODIFIES, meaning that the function possibly modifies SQL data. This information is not useful for PostgreSQL.

is\_null\_call yes\_or\_no

If the function automatically returns null if any of its arguments are null, then YES, else NO. Null for a procedure.

sql\_path character\_data

Applies to a feature not available in PostgreSQL

schema\_level\_routine yes\_or\_no

Always YES (The opposite would be a method of a user-defined type, which is a feature not available in PostgreSQL.)

max\_dynamic\_result\_sets cardinal\_number

Applies to a feature not available in PostgreSQL

is\_user\_defined\_cast yes\_or\_no

Applies to a feature not available in PostgreSQL

is\_implicitly\_invocable yes\_or\_no

Applies to a feature not available in PostgreSQL

security\_type character\_data

If the function runs with the privileges of the current user, then INVOKER, if the function runs with the privileges of the user who defined it, then DEFINER.

```
Column Type
       Description
to_sql_specific_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
to_sql_specific_schema sql_identifier
       Applies to a feature not available in PostgreSQL
to_sql_specific_name sql_identifier
       Applies to a feature not available in PostgreSQL
as_locator yes_or_no
       Applies to a feature not available in PostgreSQL
created time_stamp
       Applies to a feature not available in PostgreSQL
last_altered time_stamp
       Applies to a feature not available in PostgreSQL
new_savepoint_level yes_or_no
       Applies to a feature not available in PostgreSQL
is_udt_dependent yes_or_no
       Currently always NO. The alternative YES applies to a feature not available in Post-
       greSQL.
result_cast_from_data_type character_data
       Applies to a feature not available in PostgreSQL
result_cast_as_locator yes_or_no
       Applies to a feature not available in PostgreSQL
result_cast_char_max_length cardinal_number
       Applies to a feature not available in PostgreSQL
result_cast_char_octet_length cardinal_number
       Applies to a feature not available in PostgreSQL
result_cast_char_set_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
result_cast_char_set_schema sql_identifier
       Applies to a feature not available in PostgreSQL
result_cast_char_set_name sql_identifier
       Applies to a feature not available in PostgreSQL
result_cast_collation_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
result_cast_collation_schema sql_identifier
       Applies to a feature not available in PostgreSQL
result_cast_collation_name sql_identifier
       Applies to a feature not available in PostgreSQL
result_cast_numeric_precision cardinal_number
       Applies to a feature not available in PostgreSQL
result_cast_numeric_precision_radix cardinal_number
       Applies to a feature not available in PostgreSQL
result_cast_numeric_scale cardinal_number
       Applies to a feature not available in PostgreSQL
result_cast_datetime_precision cardinal_number
       Applies to a feature not available in PostgreSQL
result_cast_interval_type character_data
       Applies to a feature not available in PostgreSQL
```

| Column Type<br>Description                                                                          |
|-----------------------------------------------------------------------------------------------------|
| result_cast_interval_precision cardinal_number<br>Applies to a feature not available in PostgreSQL  |
| result_cast_type_udt_catalog sql_identifier<br>Applies to a feature not available in PostgreSQL     |
| result_cast_type_udt_schema sql_identifier<br>Applies to a feature not available in PostgreSQL      |
| result_cast_type_udt_name sql_identifier<br>Applies to a feature not available in PostgreSQL        |
| result_cast_scope_catalog sql_identifier<br>Applies to a feature not available in PostgreSQL        |
| result_cast_scope_schema sql_identifier<br>Applies to a feature not available in PostgreSQL         |
| result_cast_scope_name sql_identifier<br>Applies to a feature not available in PostgreSQL           |
| result_cast_maximum_cardinality cardinal_number<br>Applies to a feature not available in PostgreSQL |
| result_cast_dtd_identifier sql_identifier<br>Applies to a feature not available in PostgreSQL       |