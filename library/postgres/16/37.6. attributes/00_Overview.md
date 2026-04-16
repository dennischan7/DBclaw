---
source: PostgreSQL 16 Reference
title: 00_Overview
---

The view attributes contains information about the attributes of composite data types defined in the database. (Note that the view does not give information about table columns, which are sometimes called attributes in PostgreSQL contexts.) Only those attributes are shown that the current user has access to (by way of being the owner of or having some privilege on the type).

#### **Table 37.4. attributes Columns**

### **Column Type Description** udt\_catalog sql\_identifier Name of the database containing the data type (always the current database) udt\_schema sql\_identifier Name of the schema containing the data type udt\_name sql\_identifier Name of the data type attribute\_name sql\_identifier Name of the attribute ordinal\_position cardinal\_number Ordinal position of the attribute within the data type (count starts at 1) attribute\_default character\_data Default expression of the attribute is\_nullable yes\_or\_no YES if the attribute is possibly nullable, NO if it is known not nullable. data\_type character\_data Data type of the attribute, if it is a built-in type, or ARRAY if it is some array (in that case, see the view element\_types), else USER-DEFINED (in that case, the type is identified in attribute\_udt\_name and associated columns). character\_maximum\_length cardinal\_number If data\_type identifies a character or bit string type, the declared maximum length; null for all other data types or if no maximum length was declared. character\_octet\_length cardinal\_number If data\_type identifies a character type, the maximum possible length in octets (bytes) of a datum; null for all other data types. The maximum octet length depends on the declared character maximum length (see above) and the server encoding. character\_set\_catalog sql\_identifier Applies to a feature not available in PostgreSQL character\_set\_schema sql\_identifier Applies to a feature not available in PostgreSQL character\_set\_name sql\_identifier Applies to a feature not available in PostgreSQL

#### collation\_catalog sql\_identifier

Name of the database containing the collation of the attribute (always the current database), null if default or the data type of the attribute is not collatable

#### collation\_schema sql\_identifier

Name of the schema containing the collation of the attribute, null if default or the data type of the attribute is not collatable

#### collation\_name sql\_identifier

Name of the collation of the attribute, null if default or the data type of the attribute is not collatable

#### numeric\_precision cardinal\_number

If data\_type identifies a numeric type, this column contains the (declared or implicit) precision of the type for this attribute. The precision indicates the number of significant digits. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. For all other data types, this column is null.

#### numeric\_precision\_radix cardinal\_number

If data\_type identifies a numeric type, this column indicates in which base the values in the columns numeric\_precision and numeric\_scale are expressed. The value is either 2 or 10. For all other data types, this column is null.

#### numeric\_scale cardinal\_number

If data\_type identifies an exact numeric type, this column contains the (declared or implicit) scale of the type for this attribute. The scale indicates the number of significant digits to the right of the decimal point. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column numeric\_precision\_radix. For all other data types, this column is null.

#### datetime\_precision cardinal\_number

If data\_type identifies a date, time, timestamp, or interval type, this column contains the (declared or implicit) fractional seconds precision of the type for this attribute, that is, the number of decimal digits maintained following the decimal point in the seconds value. For all other data types, this column is null.

#### interval\_type character\_data

If data\_type identifies an interval type, this column contains the specification which fields the intervals include for this attribute, e.g., YEAR TO MONTH, DAY TO SE-COND, etc. If no field restrictions were specified (that is, the interval accepts all fields), and for all other data types, this field is null.

#### interval\_precision cardinal\_number

Applies to a feature not available in PostgreSQL (see datetime\_precision for the fractional seconds precision of interval type attributes)

#### attribute\_udt\_catalog sql\_identifier

Name of the database that the attribute data type is defined in (always the current database)

#### attribute\_udt\_schema sql\_identifier

Name of the schema that the attribute data type is defined in

attribute\_udt\_name sql\_identifier

Name of the attribute data type

#### scope\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

#### scope\_schema sql\_identifier

Applies to a feature not available in PostgreSQL

scope\_name sql\_identifier

Applies to a feature not available in PostgreSQL

maximum\_cardinality cardinal\_number

Always null, because arrays always have unlimited maximum cardinality in PostgreSQL

dtd\_identifier sql\_identifier

An identifier of the data type descriptor of the attribute, unique among the data type descriptors pertaining to the composite type. This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)

```
is_derived_reference_attribute yes_or_no
       Applies to a feature not available in PostgreSQL
```

See also under [Section 37.17,](#page-163-0) a similarly structured view, for further information on some of the columns.

# <span id="page-158-0"></span>**37.7. character\_sets**

The view character\_sets identifies the character sets available in the current database. Since PostgreSQL does not support multiple character sets within one database, this view only shows one, which is the database encoding.

Take note of how the following terms are used in the SQL standard:

character repertoire

An abstract collection of characters, for example UNICODE, UCS, or LATIN1. Not exposed as an SQL object, but visible in this view.

character encoding form

An encoding of some character repertoire. Most older character repertoires only use one encoding form, and so there are no separate names for them (e.g., LATIN2 is an encoding form applicable to the LATIN2 repertoire). But for example Unicode has the encoding forms UTF8, UTF16, etc. (not all supported by PostgreSQL). Encoding forms are not exposed as an SQL object, but are visible in this view.

character set

A named SQL object that identifies a character repertoire, a character encoding, and a default collation. A predefined character set would typically have the same name as an encoding form, but users could define other names. For example, the character set UTF8 would typically identify the character repertoire UCS, encoding form UTF8, and some default collation.

You can think of an "encoding" in PostgreSQL either as a character set or a character encoding form. They will have the same name, and there can only be one in one database.

#### **Table 37.5. character\_sets Columns**

### **Column Type Description**

character\_set\_catalog sql\_identifier

Character sets are currently not implemented as schema objects, so this column is null.

character\_set\_schema sql\_identifier

Character sets are currently not implemented as schema objects, so this column is null.

character\_set\_name sql\_identifier

#### **Column Type**

#### **Description**

Name of the character set, currently implemented as showing the name of the database encoding

character\_repertoire sql\_identifier

Character repertoire, showing UCS if the encoding is UTF8, else just the encoding name

form\_of\_use sql\_identifier

Character encoding form, same as the database encoding

default\_collate\_catalog sql\_identifier

Name of the database containing the default collation (always the current database, if any collation is identified)

default\_collate\_schema sql\_identifier

Name of the schema containing the default collation

default\_collate\_name sql\_identifier

Name of the default collation. The default collation is identified as the collation that matches the COLLATE and CTYPE settings of the current database. If there is no such collation, then this column and the associated schema and catalog columns are null.