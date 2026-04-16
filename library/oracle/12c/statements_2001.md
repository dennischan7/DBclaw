# Oracle 12c - statements_2001
Source: https://docs.oracle.com/database/121/SQLRF/statements_2001.htm

[Go to main content](#BEGIN)

383/555 

# ALTER LIBRARY

Purpose

The `ALTER` `LIBRARY` statement explicitly recompiles a library. Explicit recompilation eliminates the need for implicit run-time recompilation and prevents associated run-time compilation errors and performance overhead.

Note:

This statement does not change the declaration or definition of an existing library. To redeclare or redefine a library, use the

["CREATE LIBRARY"](statements_6001.md#CCHJGGJA)

with the

`OR` `REPLACE`

clause.

Prerequisites

If the library is in the `SYS` schema, you must be connected as `SYSDBA`. Otherwise, the library must be in your own schema or you must have the `ALTER` `ANY` `LIBRARY` system privilege.

Semantics

schema

Specify the schema containing the library. If you omit `schema`, then Oracle Database assumes the procedure is in your own schema.

library\_name

Specify the name of the library to be recompiled.

library\_compile\_clause

See [Oracle Database PL/SQL Language Reference](../LNPLS/alter_library.md#LNPLS1877) for the syntax and semantics of this clause and for complete information on creating and compiling libraries.

EDITIONABLE | NONEDITIONABLE

Use these clauses to specify whether the library becomes an editioned or noneditioned object if editioning is later enabled for the schema object type `LIBRARY` in `schema`. The default is `EDITIONABLE`. For information about altering editioned and noneditioned objects, see [Oracle Database Development Guide](../ADFNS/adfns_editions.md#ADFNS1287).

Scripting on this page enhances content navigation, but does not change the content in any way.