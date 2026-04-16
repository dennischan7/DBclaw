# Oracle 11g - statements_5013
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_5013.htm

Purpose

Use the `CREATE` `INDEXTYPE` statement to create an indextype, which is an object that specifies the routines that manage a domain (application-specific) index. Indextypes reside in the same namespace as tables, views, and other schema objects. This statement binds the indextype name to an implementation type, which in turn specifies and refers to user-defined index functions and procedures that implement the indextype.

Prerequisites

To create an indextype in your own schema, you must have the `CREATE` `INDEXTYPE` system privilege. To create an indextype in another schema, you must have the `CREATE` `ANY` `INDEXTYPE` system privilege. In either case, you must have the `EXECUTE` object privilege on the implementation type and the supported operators.

An indextype supports one or more operators, so before creating an indextype, you must first design the operator or operators to be supported and provide functional implementation for those operators.

Semantics

schema

Specify the name of the schema in which the indextype resides. If you omit `schema`, then Oracle Database creates the indextype in your own schema.

indextype

Specify the name of the indextype to be created.

FOR Clause

Use the `FOR` clause to specify the list of operators supported by the indextype.

* For `schema`, specify the schema containing the operator. If you omit `schema`, then Oracle assumes the operator is in your own schema.
* For `operator`, specify the name of the operator supported by the indextype.

  All the operators listed in this clause must be valid operators.
* For `parameter_type`, list the types of parameters to the operator.

using\_type\_clause

The `USING` clause lets you specify the type that provides the implementation for the new indextype.

For `implementation_type`, specify the name of the type that implements the appropriate Oracle Data Cartridge Interface (ODCI).

WITH LOCAL PARTITION

Use this clause to indicate that the indextype can be used to create local domain indexes on range- and list-partitioned tables. You use this clause in combination with the storage\_table in several ways (see [storage\_table\_clause](#BABEHBBD)).

* The recommended method is to specify `WITH` `LOCAL` `[RANGE]` `PARTITION` `WITH` `SYSTEM` `MANAGED` `STORAGE` `TABLES`. This combination uses system-managed storage tables, which are the preferred storage management, and lets you create local domain indexes on both range- and list-partitioned tables. In this case the `RANGE` keyword is optional and ignored, because it is no longer needed if you specify `WITH` `LOCAL` `PARTITION` `WITH` `SYSTEM` `MANAGED` `STORAGE` `TABLES`.
* You can specify `WITH` `LOCAL` `RANGE` `PARTITION` (including the `RANGE` keyword) and omit the `storage_table` clause. Local domain indexes on range-partitioned tables are supported with user-managed storage tables for backward compatibility. Oracle does not recommend this combination because it uses the less efficient user-managed storage tables.

If you omit this clause entirely, then you cannot subsequently use this indextype to create a local domain index on a range- or list-partitioned table.

storage\_table\_clause

Use this clause to specify how storage tables and partition maintenance operations for indexes built on this indextype are managed:

* Specify `WITH` `SYSTEM` `MANAGED` `STORAGE` `TABLES` to indicate that the storage of statistics data is to be managed by the system. The type you specify in `statistics_type` should be storing the statistics related information in tables that are maintained by the system. Also, the indextype you specify must already have been created or altered to support the `WITH` `SYSTEM` `MANAGED` `STORAGE` `TABLES` clause.
* Specify `WITH` `USER` `MANAGED` `STORAGE` `TABLES` to indicate that the tables that store the user-defined statistics will be managed by the user. This is the default behavior.

array\_DML\_clause

Use this clause to let the indextype support the array interface for the `ODCIIndexInsert` method.

type and varray\_type If the data type of the column to be indexed is a user-defined object type, then you must specify this clause to identify the varray `varray_type` that Oracle should use to hold column values of `type`. If the indextype supports a list of types, then you can specify a corresponding list of varray types. If you omit `schema` for either `type` or `varray_type`, then Oracle assumes the type is in your own schema.

If the data type of the column to be indexed is a built-in system type, then any varray type specified for the indextype takes precedence over the ODCI types defined by the system.

Examples

Creating an Indextype: Example The following statement creates an indextype named `position_indextype` and specifies the `position_between` operator that is supported by the indextype and the `position_im` type that implements the index interface. Refer to ["Using Extensible Indexing"](ap_examples001.md#i690409) for an extensible indexing scenario that uses this indextype:

```
CREATE INDEXTYPE position_indextype
   FOR position_between(NUMBER, NUMBER, NUMBER)
   USING position_im;
```