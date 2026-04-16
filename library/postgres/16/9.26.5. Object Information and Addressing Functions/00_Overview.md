---
source: PostgreSQL 16 Reference
title: 00_Overview
---

[Table 9.77](#page-24-0) lists functions related to database object identification and addressing.

### <span id="page-24-0"></span>**Table 9.77. Object Information and Addressing Functions**

### **Function**

#### **Description**

pg\_describe\_object ( classid oid, objid oid, objsubid integer ) → text Returns a textual description of a database object identified by catalog OID, object OID, and sub-object ID (such as a column number within a table; the sub-object ID is zero when referring to a whole object). This description is intended to be human-readable, and might be translated, depending on server configuration. This is especially useful to determine the identity of an object referenced in the pg\_depend catalog. This function returns NULL values for undefined objects.

pg\_identify\_object ( classid oid, objid oid, objsubid integer ) → record ( type text, schema text, name text, identity text )

Returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. This information is intended to be machine-readable, and is never translated. type identifies the type of database object; schema is the schema name that the object belongs in, or NULL for object types that do not belong to schemas; name is the name of the object, quoted if necessary, if the name (along with schema name, if pertinent) is sufficient to uniquely identify the object, otherwise NULL; identity is the complete object identity, with the precise format depending on object type, and each name within the format being schema-qualified and quoted as necessary. Undefined objects are identified with NULL values.

pg\_identify\_object\_as\_address ( classid oid, objid oid, objsubid integer ) → record ( type text, object\_names text[], object\_args text[] )

Returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. The returned information is independent of the current server, that is, it could be used to identify an identically named object in another server. type identifies the type of database object; object\_names and object\_args are text arrays that together form a reference to the object. These three values can be passed to pg\_get\_object\_address to obtain the internal address of the object.

pg\_get\_object\_address ( type text, object\_names text[], object\_args text[] ) → record ( classid oid, objid oid, objsubid integer ) Returns a row containing enough information to uniquely identify the database object specified by a type code and object name and argument arrays. The returned values are the ones that would be used in system catalogs such as pg\_depend; they can be passed to other system functions such as pg\_describe\_object or pg\_identify\_object. classid is the OID of the system catalog containing the object; objid is the OID of the object itself, and objsubid is the sub-object ID, or zero if none. This function is the inverse of pg\_identify\_object\_as\_address. Undefined objects are identified with NULL values.