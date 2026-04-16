---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view column\_udt\_usage identifies all columns that use data types owned by a currently enabled role. Note that in PostgreSQL, built-in data types behave like user-defined types, so they are included here as well. See also [Section 37.17](#page-163-0) for details.

#### **Table 37.14. column\_udt\_usage Columns**

```
Column Type
       Description
udt_catalog sql_identifier
       Name of the database that the column data type (the underlying type of the domain, if ap-
       plicable) is defined in (always the current database)
udt_schema sql_identifier
       Name of the schema that the column data type (the underlying type of the domain, if ap-
       plicable) is defined in
udt_name sql_identifier
       Name of the column data type (the underlying type of the domain, if applicable)
table_catalog sql_identifier
       Name of the database containing the table (always the current database)
table_schema sql_identifier
       Name of the schema containing the table
table_name sql_identifier
       Name of the table
column_name sql_identifier
       Name of the column
```

# <span id="page-163-0"></span>**37.17. columns**

The view columns contains information about all table columns (or view columns) in the database. System columns (ctid, etc.) are not included. Only those columns are shown that the current user has access to (by way of being the owner or having some privilege).

#### **Table 37.15. columns Columns**

```
Column Type
       Description
table_catalog sql_identifier
       Name of the database containing the table (always the current database)
table_schema sql_identifier
       Name of the schema containing the table
table_name sql_identifier
       Name of the table
column_name sql_identifier
       Name of the column
ordinal_position cardinal_number
       Ordinal position of the column within the table (count starts at 1)
column_default character_data
       Default expression of the column
is_nullable yes_or_no
       YES if the column is possibly nullable, NO if it is known not nullable. A not-null con-
       straint is one way a column can be known not nullable, but there can be others.
```

#### data\_type character\_data

Data type of the column, if it is a built-in type, or ARRAY if it is some array (in that case, see the view element\_types), else USER-DEFINED (in that case, the type is identified in udt\_name and associated columns). If the column is based on a domain, this column refers to the type underlying the domain (and the domain is identified in domain\_name and associated columns).

#### character\_maximum\_length cardinal\_number

If data\_type identifies a character or bit string type, the declared maximum length; null for all other data types or if no maximum length was declared.

#### character\_octet\_length cardinal\_number

If data\_type identifies a character type, the maximum possible length in octets (bytes) of a datum; null for all other data types. The maximum octet length depends on the declared character maximum length (see above) and the server encoding.

#### numeric\_precision cardinal\_number

If data\_type identifies a numeric type, this column contains the (declared or implicit) precision of the type for this column. The precision indicates the number of significant digits. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. For all other data types, this column is null.

#### numeric\_precision\_radix cardinal\_number

If data\_type identifies a numeric type, this column indicates in which base the values in the columns numeric\_precision and numeric\_scale are expressed. The value is either 2 or 10. For all other data types, this column is null.

#### numeric\_scale cardinal\_number

If data\_type identifies an exact numeric type, this column contains the (declared or implicit) scale of the type for this column. The scale indicates the number of significant digits to the right of the decimal point. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. For all other data types, this column is null.

#### datetime\_precision cardinal\_number

If data\_type identifies a date, time, timestamp, or interval type, this column contains the (declared or implicit) fractional seconds precision of the type for this column, that is, the number of decimal digits maintained following the decimal point in the seconds value. For all other data types, this column is null.

#### interval\_type character\_data

If data\_type identifies an interval type, this column contains the specification which fields the intervals include for this column, e.g., YEAR TO MONTH, DAY TO SECOND, etc. If no field restrictions were specified (that is, the interval accepts all fields), and for all other data types, this field is null.

#### interval\_precision cardinal\_number

Applies to a feature not available in PostgreSQL (see datetime\_precision for the fractional seconds precision of interval type columns)

#### character\_set\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

#### character\_set\_schema sql\_identifier

Applies to a feature not available in PostgreSQL

#### character\_set\_name sql\_identifier

Applies to a feature not available in PostgreSQL

collation\_catalog sql\_identifier

#### **Column Type**

#### **Description**

Name of the database containing the collation of the column (always the current database), null if default or the data type of the column is not collatable

collation\_schema sql\_identifier

Name of the schema containing the collation of the column, null if default or the data type of the column is not collatable

collation\_name sql\_identifier

Name of the collation of the column, null if default or the data type of the column is not collatable

domain\_catalog sql\_identifier

If the column has a domain type, the name of the database that the domain is defined in (always the current database), else null.

domain\_schema sql\_identifier

If the column has a domain type, the name of the schema that the domain is defined in, else null.

domain\_name sql\_identifier

If the column has a domain type, the name of the domain, else null.

udt\_catalog sql\_identifier

Name of the database that the column data type (the underlying type of the domain, if applicable) is defined in (always the current database)

udt\_schema sql\_identifier

Name of the schema that the column data type (the underlying type of the domain, if applicable) is defined in

udt\_name sql\_identifier

Name of the column data type (the underlying type of the domain, if applicable)

scope\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

scope\_schema sql\_identifier

Applies to a feature not available in PostgreSQL

scope\_name sql\_identifier

Applies to a feature not available in PostgreSQL

maximum\_cardinality cardinal\_number

Always null, because arrays always have unlimited maximum cardinality in PostgreSQL

dtd\_identifier sql\_identifier

An identifier of the data type descriptor of the column, unique among the data type descriptors pertaining to the table. This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)

is\_self\_referencing yes\_or\_no

Applies to a feature not available in PostgreSQL

is\_identity yes\_or\_no

If the column is an identity column, then YES, else NO.

identity\_generation character\_data

If the column is an identity column, then ALWAYS or BY DEFAULT, reflecting the definition of the column.

identity\_start character\_data

If the column is an identity column, then the start value of the internal sequence, else null.

identity\_increment character\_data

If the column is an identity column, then the increment of the internal sequence, else null.

identity\_maximum character\_data

If the column is an identity column, then the maximum value of the internal sequence, else null.

identity\_minimum character\_data

If the column is an identity column, then the minimum value of the internal sequence, else null.

identity\_cycle yes\_or\_no

If the column is an identity column, then YES if the internal sequence cycles or NO if it does not; otherwise null.

is\_generated character\_data

If the column is a generated column, then ALWAYS, else NEVER.

generation\_expression character\_data

If the column is a generated column, then the generation expression, else null.

is\_updatable yes\_or\_no

YES if the column is updatable, NO if not (Columns in base tables are always updatable, columns in views not necessarily)

Since data types can be defined in a variety of ways in SQL, and PostgreSQL contains additional ways to define data types, their representation in the information schema can be somewhat difficult. The column data\_type is supposed to identify the underlying built-in type of the column. In PostgreSQL, this means that the type is defined in the system catalog schema pg\_catalog. This column might be useful if the application can handle the well-known built-in types specially (for example, format the numeric types differently or use the data in the precision columns). The columns udt\_name, udt\_schema, and udt\_catalog always identify the underlying data type of the column, even if the column is based on a domain. (Since PostgreSQL treats built-in types like user-defined types, builtin types appear here as well. This is an extension of the SQL standard.) These columns should be used if an application wants to process data differently according to the type, because in that case it wouldn't matter if the column is really based on a domain. If the column is based on a domain, the identity of the domain is stored in the columns domain\_name, domain\_schema, and domain\_catalog. If you want to pair up columns with their associated data types and treat domains as separate types, you could write coalesce(domain\_name, udt\_name), etc.