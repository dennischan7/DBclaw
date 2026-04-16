# Oracle 12c - statements_9006
Source: https://docs.oracle.com/database/121/SQLRF/statements_9006.htm

Semantics

schema

Specify the schema containing the type. If you omit `schema`, then Oracle Database assumes the type is in your own schema.

type\_name

Specify the name of the object, varray, or nested table type to be dropped. You can drop only types with no type or table dependencies.

If `type_name` is a supertype, then this statement will fail unless you also specify `FORCE`. If you specify `FORCE`, then the database invalidates all subtypes depending on this supertype.

If `type_name` is a statistics type, then this statement will fail unless you also specify `FORCE`. If you specify `FORCE`, then the database first disassociates all objects that are associated with `type_name` and then drops `type_name`.

If `type_name` is an object type that has been associated with a statistics type, then the database first attempts to disassociate `type_name` from the statistics type and then drops `type_name`. However, if statistics have been collected using the statistics type, then the database will be unable to disassociate `type_name` from the statistics type, and this statement will fail.

If `type_name` is an implementation type for an indextype, then the indextype will be marked `INVALID`.

If `type_name` has a public synonym defined on it, then the database will also drop the synonym.

Unless you specify `FORCE`, you can drop only object types, nested tables, or varray types that are standalone schema objects with no dependencies. This is the default behavior.

FORCE

Specify `FORCE` to drop the type even if it has dependent database objects. Oracle Database marks `UNUSED` all columns dependent on the type to be dropped, and those columns become inaccessible.

Caution:

Oracle does not recommend that you specify

`FORCE`

to drop object types with dependencies. This operation is not recoverable and could cause the data in the dependent tables or columns to become inaccessible.

VALIDATE

If you specify `VALIDATE` when dropping a type, then Oracle Database checks for stored instances of this type within substitutable columns of any of its supertypes. If no such instances are found, then the database completes the drop operation.

This clause is meaningful only for subtypes. Oracle recommends the use of this option to safely drop subtypes that do not have any explicit type or table dependencies.