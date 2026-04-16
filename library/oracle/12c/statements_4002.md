# Oracle 12c - statements_4002
Source: https://docs.oracle.com/database/121/SQLRF/statements_4002.htm

Purpose

Object types are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../LNPLS/alter_type.md#LNPLS99995) for details of syntax and semantics.

Use the `ALTER` `TYPE` statement to add or drop member attributes or methods. You can change the existing properties (`FINAL` or `INSTANTIABLE`) of an object type, and you can modify the scalar attributes of the type.

You can also use this statement to recompile the specification or body of the type or to change the specification of an object type by adding new object member subprogram specifications.

Semantics

schema

Specify the schema that contains the type. If you omit `schema`, then Oracle Database assumes the type is in your current schema.

type\_name

Specify the name of an object type, a nested table type, or a varray type.

Restriction on type\_name You cannot evolve an editioned object type. The `ALTER` `TYPE` statement fails with ORA-22348 if either of the following is true:

* The type is an editioned object type and the `ALTER` `TYPE` statement has no `type_compile_clause`. You can use the `ALTER` `TYPE` statement to recompile an editioned object type, but not for any other purpose.
* The type has a dependent that is an editioned object type and the `ALTER` `TYPE` statement has a `CASCADE` clause.

Refer to Oracle Database PL/SQL Language Reference for more information on the [`type_compile_clause`](../LNPLS/alter_type.md#LNPLS1441) and the [`CASCADE`](../LNPLS/alter_type.md#LNPLS1482) clause.

alter\_type\_clause

See [Oracle Database PL/SQL Language Reference](../LNPLS/alter_type.md#LNPLS2186) for the syntax and semantics of this clause and for complete information on creating and compiling object types.

EDITIONABLE | NONEDITIONABLE

Use these clauses to specify whether the type becomes an editioned or noneditioned object if editioning is later enabled for the schema object type `TYPE` in `schema`. The default is `EDITIONABLE`. For information about altering editioned and noneditioned objects, see [Oracle Database Development Guide](../ADFNS/adfns_editions.md#ADFNS1287).