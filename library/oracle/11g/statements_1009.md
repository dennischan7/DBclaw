# Oracle 11g - statements_1009
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_1009.htm

[Go to main content](#BEGIN)

358/522 

# ALTER FUNCTION

Purpose

Functions are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/alter_function.md#LNPLS99999) for complete syntax, semantics, and examples.

Use the `ALTER` `FUNCTION` statement to recompile an invalid standalone stored function. Explicit recompilation eliminates the need for implicit run-time recompilation and prevents associated run-time compilation errors and performance overhead.

This statement does not change the declaration or definition of an existing function. To redeclare or redefine a function, use the `CREATE` `FUNCTION` statement with the `OR` `REPLACE` clause. See [CREATE FUNCTION](statements_5011.md#i2153260).

Prerequisites

The function must be in your own schema or you must have `ALTER` `ANY` `PROCEDURE` system privilege.

Semantics

schema

Specify the schema containing the function. If you omit `schema`, then Oracle Database assumes the function is in your own schema.

function

Specify the name of the function to be recompiled.

function\_compile\_clause

See [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/alter_function.md#LNPLS99999) for the syntax and semantics of this clause and for complete information on creating and compiling functions.

Scripting on this page enhances content navigation, but does not change the content in any way.