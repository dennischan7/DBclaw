# Oracle 12c - statements_1011
Source: https://docs.oracle.com/database/121/SQLRF/statements_1011.htm

[Go to main content](#BEGIN)

378/555 

# ALTER FUNCTION

Purpose

Functions are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../LNPLS/alter_function.md#LNPLS99999) for details of syntax and semantics.

Use the `ALTER` `FUNCTION` statement to recompile an invalid standalone stored function. Explicit recompilation eliminates the need for implicit run-time recompilation and prevents associated run-time compilation errors and performance overhead.

This statement does not change the declaration or definition of an existing function. To redeclare or redefine a function, use the `CREATE` `FUNCTION` statement with the `OR` `REPLACE` clause. See [CREATE FUNCTION](statements_5012.md#i2153260).

Prerequisites

The function must be in your own schema or you must have `ALTER` `ANY` `PROCEDURE` system privilege.

Semantics

schema

Specify the schema containing the function. If you omit `schema`, then Oracle Database assumes the function is in your own schema.

function\_name

Specify the name of the function to be recompiled.

function\_compile\_clause

See [Oracle Database PL/SQL Language Reference](../LNPLS/alter_function.md#LNPLS1872) for the syntax and semantics of this clause and for complete information on creating and compiling functions.

EDITIONABLE | NONEDITIONABLE

Use these clauses to specify whether the function becomes an editioned or noneditioned object if editioning is later enabled for the schema object type `FUNCTION` in `schema`. The default is `EDITIONABLE`. For information about altering editioned and noneditioned objects, see [Oracle Database Development Guide](../ADFNS/adfns_editions.md#ADFNS1287).

Scripting on this page enhances content navigation, but does not change the content in any way.