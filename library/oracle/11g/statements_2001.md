# Oracle 11g - statements_2001
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_2001.htm

[Go to main content](#BEGIN)

363/522 

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

See [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/alter_library.md#LNPLS99946) for the syntax and semantics of this clause and for complete information on creating and compiling libraries.

Scripting on this page enhances content navigation, but does not change the content in any way.