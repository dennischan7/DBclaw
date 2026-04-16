# Oracle 11g - statements_5011
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_5011.htm

[Go to main content](#BEGIN)

402/522 

# CREATE FUNCTION

Purpose

Functions are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/create_function.md#LNPLS01370) for details of syntax and semantics.

Use the `CREATE` `FUNCTION` statement to create a standalone stored function or a call specification.

* A stored function (also called a user function or user-defined function) is a set of PL/SQL statements you can call by name. Stored functions are very similar to procedures, except that a function returns a value to the environment in which it is called. User functions can be used as part of a SQL expression.
* A call specification declares a Java method or a third-generation language (3GL) routine so that it can be called from PL/SQL. You can also use the `CALL` SQL statement to call such a method or routine. The call specification tells Oracle Database which Java method, or which named function in which shared library, to invoke when a call is made. It also tells the database what type conversions to make for the arguments and return value.

Note:

You can also create a function as part of a package using the

`CREATE` `PACKAGE`

statement.

Prerequisites

To create or replace a function in your own schema, you must have the `CREATE` `PROCEDURE` system privilege. To create or replace a function in another user's schema, you must have the `CREATE` `ANY` `PROCEDURE` system privilege.

Semantics

OR REPLACE

Specify `OR` `REPLACE` to re-create the function if it already exists. Use this clause to change the definition of an existing function without dropping, re-creating, and regranting object privileges previously granted on the function. If you redefine a function, then Oracle Database recompiles it.

Users who had previously been granted privileges on a redefined function can still access the function without being regranted the privileges.

If any function-based indexes depend on the function, then Oracle Database marks the indexes `DISABLED`.

See Also:

[`ALTER` `FUNCTION`](../../server.112/e41084/statements_1009.md#SQLRF00804)

for information on recompiling functions using SQL

plsql\_source

See [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/create_function.md#LNPLS01370) for the syntax and semantics of the `plsql_source`, including examples.

Scripting on this page enhances content navigation, but does not change the content in any way.