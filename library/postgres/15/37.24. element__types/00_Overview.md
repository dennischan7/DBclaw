---
source: PostgreSQL 15 Reference
title: 00_Overview
---

The view element\_types contains the data type descriptors of the elements of arrays. When a table column, composite-type attribute, domain, function parameter, or function return value is defined to be of an array type, the respective information schema view only contains ARRAY in the column data\_type. To obtain information on the element type of the array, you can join the respective view with this view. For example, to show the columns of a table with data types and array element types, if applicable, you could do:

```
SELECT c.column_name, c.data_type, e.data_type AS element_type
FROM information_schema.columns c LEFT JOIN
 information_schema.element_types e
 ON ((c.table_catalog, c.table_schema, c.table_name, 'TABLE',
 c.dtd_identifier)
 = (e.object_catalog, e.object_schema, e.object_name,
 e.object_type, e.collection_type_identifier))
WHERE c.table_schema = '...' AND c.table_name = '...'
ORDER BY c.ordinal_position;
```

This view only includes objects that the current user has access to, by way of being the owner or having some privilege.

### **Table 37.22. element\_types Columns**

#### **Column Type Description**

object\_catalog sql\_identifier

Name of the database that contains the object that uses the array being described (always the current database)

object\_schema sql\_identifier

Name of the schema that contains the object that uses the array being described

object\_name sql\_identifier

Name of the object that uses the array being described

```
object_type character_data
```

The type of the object that uses the array being described: one of TABLE (the array is used by a column of that table), USER-DEFINED TYPE (the array is used by an attribute of that composite type), DOMAIN (the array is used by that domain), ROUTINE (the array is used by a parameter or the return data type of that function).

```
collection_type_identifier sql_identifier
```

The identifier of the data type descriptor of the array being described. Use this to join with the dtd\_identifier columns of other information schema views.

```
data_type character_data
```

```
Column Type
```

#### **Description**

Data type of the array elements, if it is a built-in type, else USER-DEFINED (in that case, the type is identified in udt\_name and associated columns).

character\_maximum\_length cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

character\_octet\_length cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

character\_set\_catalog sql\_identifier

Applies to a feature not available in PostgreSQL

character\_set\_schema sql\_identifier

Applies to a feature not available in PostgreSQL

character\_set\_name sql\_identifier

Applies to a feature not available in PostgreSQL

collation\_catalog sql\_identifier

Name of the database containing the collation of the element type (always the current database), null if default or the data type of the element is not collatable

collation\_schema sql\_identifier

Name of the schema containing the collation of the element type, null if default or the data type of the element is not collatable

collation\_name sql\_identifier

Name of the collation of the element type, null if default or the data type of the element is not collatable

numeric\_precision cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

numeric\_precision\_radix cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

numeric\_scale cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

datetime\_precision cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

interval\_type character\_data

Always null, since this information is not applied to array element data types in PostgreSQL

interval\_precision cardinal\_number

Always null, since this information is not applied to array element data types in PostgreSQL

domain\_default character\_data

Not yet implemented

udt\_catalog sql\_identifier

Name of the database that the data type of the elements is defined in (always the current database)

udt\_schema sql\_identifier

Name of the schema that the data type of the elements is defined in

udt\_name sql\_identifier

## **Column Type Description** Name of the data type of the elements scope\_catalog sql\_identifier Applies to a feature not available in PostgreSQL scope\_schema sql\_identifier Applies to a feature not available in PostgreSQL scope\_name sql\_identifier Applies to a feature not available in PostgreSQL maximum\_cardinality cardinal\_number Always null, because arrays always have unlimited maximum cardinality in PostgreSQL dtd\_identifier sql\_identifier An identifier of the data type descriptor of the element. This is currently not useful.