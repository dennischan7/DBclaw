---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view domain\_udt\_usage identifies all domains that are based on data types owned by a currently enabled role. Note that in PostgreSQL, built-in data types behave like user-defined types, so they are included here as well.

### **Table 37.20. domain\_udt\_usage Columns**

### **Column Type Description** udt\_catalog sql\_identifier Name of the database that the domain data type is defined in (always the current database) udt\_schema sql\_identifier Name of the schema that the domain data type is defined in udt\_name sql\_identifier Name of the domain data type domain\_catalog sql\_identifier Name of the database that contains the domain (always the current database) domain\_schema sql\_identifier Name of the schema that contains the domain domain\_name sql\_identifier Name of the domain

# <span id="page-133-0"></span>**37.23. domains**

The view domains contains all *domains* defined in the current database. Only those domains are shown that the current user has access to (by way of being the owner or having some privilege).

### **Table 37.21. domains Columns**

```
Column Type
       Description
domain_catalog sql_identifier
       Name of the database that contains the domain (always the current database)
domain_schema sql_identifier
       Name of the schema that contains the domain
domain_name sql_identifier
       Name of the domain
data_type character_data
       Data type of the domain, if it is a built-in type, or ARRAY if it is some array (in that case,
       see the view element_types), else USER-DEFINED (in that case, the type is identi-
       fied in udt_name and associated columns).
character_maximum_length cardinal_number
       If the domain has a character or bit string type, the declared maximum length; null for all
       other data types or if no maximum length was declared.
character_octet_length cardinal_number
       If the domain has a character type, the maximum possible length in octets (bytes) of a
       datum; null for all other data types. The maximum octet length depends on the declared
       character maximum length (see above) and the server encoding.
character_set_catalog sql_identifier
       Applies to a feature not available in PostgreSQL
character_set_schema sql_identifier
       Applies to a feature not available in PostgreSQL
character_set_name sql_identifier
       Applies to a feature not available in PostgreSQL
collation_catalog sql_identifier
```

Name of the database containing the collation of the domain (always the current database), null if default or the data type of the domain is not collatable

collation\_schema sql\_identifier

Name of the schema containing the collation of the domain, null if default or the data type of the domain is not collatable

collation\_name sql\_identifier

Name of the collation of the domain, null if default or the data type of the domain is not collatable

numeric\_precision cardinal\_number

If the domain has a numeric type, this column contains the (declared or implicit) precision of the type for this domain. The precision indicates the number of significant digits. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. For all other data types, this column is null.

numeric\_precision\_radix cardinal\_number

If the domain has a numeric type, this column indicates in which base the values in the columns numeric\_precision and numeric\_scale are expressed. The value is either 2 or 10. For all other data types, this column is null.

numeric\_scale cardinal\_number

If the domain has an exact numeric type, this column contains the (declared or implicit) scale of the type for this domain. The scale indicates the number of significant digits to the right of the decimal point. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. For all other data types, this column is null.

datetime\_precision cardinal\_number

If data\_type identifies a date, time, timestamp, or interval type, this column contains the (declared or implicit) fractional seconds precision of the type for this domain, that is, the number of decimal digits maintained following the decimal point in the seconds value. For all other data types, this column is null.

interval\_type character\_data

If data\_type identifies an interval type, this column contains the specification which fields the intervals include for this domain, e.g., YEAR TO MONTH, DAY TO SECOND, etc. If no field restrictions were specified (that is, the interval accepts all fields), and for all other data types, this field is null.

interval\_precision cardinal\_number

Applies to a feature not available in PostgreSQL (see datetime\_precision for the fractional seconds precision of interval type domains)

domain\_default character\_data

Default expression of the domain

udt\_catalog sql\_identifier

Name of the database that the domain data type is defined in (always the current database)

udt\_schema sql\_identifier

Name of the schema that the domain data type is defined in

udt\_name sql\_identifier

Name of the domain data type

scope\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

scope\_schema sql\_identifier

Applies to a feature not available in PostgreSQL

scope\_name sql\_identifier

Applies to a feature not available in PostgreSQL

maximum\_cardinality cardinal\_number

Always null, because arrays always have unlimited maximum cardinality in PostgreSQL

```
dtd_identifier sql_identifier
```

An identifier of the data type descriptor of the domain, unique among the data type descriptors pertaining to the domain (which is trivial, because a domain only contains one data type descriptor). This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)