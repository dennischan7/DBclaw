# Oracle 12c - statements_2009
Source: https://docs.oracle.com/database/121/SQLRF/statements_2009.htm

[Go to main content](#BEGIN)

391/555 

# ALTER PROCEDURE

Purpose

Packages are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../LNPLS/alter_procedure.md#LNPLS99997) for details of syntax and semantics.

Use the `ALTER` `PROCEDURE` statement to explicitly recompile a standalone stored procedure. Explicit recompilation eliminates the need for implicit run-time recompilation and prevents associated run-time compilation errors and performance overhead.

To recompile a procedure that is part of a package, recompile the entire package using the `ALTER` `PACKAGE` statement (see [ALTER PACKAGE](statements_2007.md#i2227346)).

Note:

This statement does not change the declaration or definition of an existing procedure. To redeclare or redefine a procedure, use the

`CREATE` `PROCEDURE`

statement with the

`OR` `REPLACE`

clause (see

[CREATE PROCEDURE](statements_6011.md#i2072424)

).

The `ALTER` `PROCEDURE` statement is quite similar to the `ALTER` `FUNCTION` statement. Refer to [ALTER FUNCTION](statements_1011.md#i2166972) for more information.

Prerequisites

The procedure must be in your own schema or you must have `ALTER` `ANY` `PROCEDURE` system privilege.

Semantics

schema

Specify the schema containing the procedure. If you omit `schema`, then Oracle Database assumes the procedure is in your own schema.

procedure\_name

Specify the name of the procedure to be recompiled.

procedure\_compile\_clause

See [Oracle Database PL/SQL Language Reference](../LNPLS/alter_procedure.md#LNPLS1891) for the syntax and semantics of this clause and for complete information on creating and compiling procedures.

EDITIONABLE | NONEDITIONABLE

Use these clauses to specify whether the procedure becomes an editioned or noneditioned object if editioning is later enabled for the schema object type `PROCEDURE` in `schema`. The default is `EDITIONABLE`. For information about altering editioned and noneditioned objects, see [Oracle Database Development Guide](../ADFNS/adfns_editions.md#ADFNS1287).

Scripting on this page enhances content navigation, but does not change the content in any way.