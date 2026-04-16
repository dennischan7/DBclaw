# Oracle 12c - statements_6011
Source: https://docs.oracle.com/database/121/SQLRF/statements_6011.htm

# CREATE PROCEDURE

Purpose

Procedures are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../LNPLS/create_procedure.md#LNPLS01373) for details of syntax and semantics.

Use the `CREATE` `PROCEDURE` statement to create a standalone stored procedure or a call specification.

A procedure is a group of PL/SQL statements that you can call by name. A call specification (sometimes called call spec) declares a Java method or a third-generation language (3GL) routine so that it can be called from SQL and PL/SQL. The call spec tells Oracle Database which Java method to invoke when a call is made. It also tells the database what type conversions to make for the arguments and return value.

Stored procedures offer advantages in the areas of development, integrity, security, performance, and memory allocation.

See Also:

* [Oracle Database Development Guide](../ADFNS/adfns_packages.md#ADFNS009) for more information on stored procedures, including how to call stored procedures and for information about registering external procedures.
* [CREATE FUNCTION](statements_5012.md#i2153260) for information specific to functions, which are similar to procedures in many ways.
* [CREATE PACKAGE](statements_6007.md#i2091914) for information on creating packages. The `CREATE` `PROCEDURE` statement creates a procedure as a standalone schema object. You can also create a procedure as part of a package.
* [ALTER PROCEDURE](statements_2009.md#i2227477) and [DROP PROCEDURE](statements_8029.md#i2067495) for information on modifying and dropping a standalone procedure.
* [CREATE LIBRARY](statements_6001.md#CCHJGGJA) for more information about shared libraries.

Prerequisites

To create or replace a procedure in your own schema, you must have the `CREATE` `PROCEDURE` system privilege. To create or replace a procedure in another user's schema, you must have the `CREATE` `ANY` `PROCEDURE` system privilege.

To invoke a call spec, you may need additional privileges, for example, the `EXECUTE` object privilege on the C library for a C call spec.

To embed a `CREATE` `PROCEDURE` statement inside an Oracle precompiler program, you must terminate the statement with the keyword `END-EXEC` followed by the embedded SQL statement terminator for the specific language.

Semantics

OR REPLACE

Specify `OR` `REPLACE` to re-create the procedure if it already exists. Use this clause to change the definition of an existing procedure without dropping, re-creating, and regranting object privileges previously granted on it. If you redefine a procedure, then Oracle Database recompiles it.

Users who had previously been granted privileges on a redefined procedure can still access the procedure without being regranted the privileges.

If any function-based indexes depend on the procedure, then Oracle Database marks the indexes `DISABLED`.

[ EDITIONABLE | NONEDITIONABLE ]

Use these clauses to specify whether the procedure is an editioned or noneditioned object if editioning is enabled for the schema object type `PROCEDURE` in `schema`. The default is `EDITIONABLE`. For information about editioned and noneditioned objects, see [Oracle Database Development Guide](../ADFNS/adfns_editions.md#ADFNS99923).

plsql\_procedure\_source

See [Oracle Database PL/SQL Language Reference](../LNPLS/create_procedure.md#LNPLS1527) for the syntax and semantics of the `plsql_procedure_source`.