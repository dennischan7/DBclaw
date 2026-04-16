# Oracle 12c - statements_8027
Source: https://docs.oracle.com/database/121/SQLRF/statements_8027.htm

Purpose

Packages are defined using PL/SQL. Refer to [Oracle Database PL/SQL Language Reference](../LNPLS/drop_package.md#LNPLS99992) for complete information on creating, altering, and dropping packages.

Use the `DROP` `PACKAGE` statement to remove a stored package from the database. This statement drops the body and specification of a package.

Note:

Do not use this statement to remove a single object from a package. Instead, re-create the package without the object using the

`CREATE` `PACKAGE`

and

`CREATE` `PACKAGE` `BODY`

statements with the

`OR` `REPLACE`

clause.

Semantics

BODY

Specify `BODY` to drop only the body of the package. If you omit this clause, then Oracle Database drops both the body and specification of the package.

When you drop only the body of a package but not its specification, the database does not invalidate dependent objects. However, you cannot call one of the procedures or stored functions declared in the package specification until you re-create the package body.

schema

Specify the schema containing the package. If you omit `schema`, then the database assumes the package is in your own schema.

package

Specify the name of the package to be dropped.

Oracle Database invalidates any local objects that depend on the package specification. If you subsequently reference one of these objects, then the database tries to recompile the object and returns an error if you have not re-created the dropped package.

If any statistics types are associated with the package, then the database disassociates the statistics types with the `FORCE` clause and drops any user-defined statistics collected with the statistics types.