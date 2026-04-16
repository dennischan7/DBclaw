# Oracle 11g - statements_6007
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_6007.htm

# CREATE PACKAGE BODY

Purpose

Package bodies are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/create_package_body.md#LNPLS01372) for details of syntax and semantics.

Use the `CREATE` `PACKAGE` `BODY` statement to create the body of a stored package, which is an encapsulated collection of related procedures, stored functions, and other program objects stored together in the database. The package body defines these objects. The package specification, defined in an earlier `CREATE` `PACKAGE` statement, declares these objects.

Packages are an alternative to creating procedures and functions as standalone schema objects.

Prerequisites

To create or replace a package in your own schema, you must have the `CREATE` `PROCEDURE` system privilege. To create or replace a package in another user's schema, you must have the `CREATE` `ANY` `PROCEDURE` system privilege. In both cases, the package body must be created in the same schema as the package.

To embed a `CREATE` `PACKAGE` `BODY` statement inside an Oracle Database precompiler program, you must terminate the statement with the keyword `END-EXEC` followed by the embedded SQL statement terminator for the specific language.

Semantics

OR REPLACE

Specify `OR` `REPLACE` to re-create the package body if it already exists. Use this clause to change the body of an existing package without dropping, re-creating, and regranting object privileges previously granted on it. If you change a package body, then Oracle Database recompiles it.

Users who had previously been granted privileges on a redefined package can still access the package without being regranted the privileges.

See Also:

[ALTER PACKAGE](statements_2006.md#i2227346)

for information on recompiling package bodies

plsql\_source

See [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/create_package_body.md#LNPLS01372) for the syntax and semantics of the `plsql_source`.