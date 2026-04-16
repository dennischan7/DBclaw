# Oracle 11g - statements_4001
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_4001.htm

Purpose

Triggers are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/alter_trigger.md#LNPLS99996) for details of syntax and semantics.

Use the `ALTER` `TRIGGER` statement to enable, disable, or compile a database trigger.

Note:

This statement does not change the declaration or definition of an existing trigger. To redeclare or redefine a trigger, use the

`CREATE` `TRIGGER`

statement with the

`OR` `REPLACE`

keywords.

Prerequisites

The trigger must be in your own schema or you must have `ALTER` `ANY` `TRIGGER` system privilege.

In addition, to alter a trigger on `DATABASE`, you must have the `ADMINISTER` `DATABASE` `TRIGGER` privilege.

See Also:

[CREATE TRIGGER](statements_7004.md#i2235611)

for more information on triggers based on

`DATABASE`

triggers

Semantics

schema

Specify the schema containing the trigger. If you omit `schema`, then Oracle Database assumes the trigger is in your own schema.

trigger

Specify the name of the trigger to be altered.

ENABLE | DISABLE

Specify `ENABLE` to enable the trigger. You can also use the `ENABLE` `ALL` `TRIGGERS` clause of `ALTER` `TABLE` to enable all triggers associated with a table. See [ALTER TABLE](statements_3001.md#CJAHHIBI).

Specify `DISABLE` to disable the trigger. You can also use the `DISABLE` `ALL` `TRIGGERS` clause of `ALTER` `TABLE` to disable all triggers associated with a table.

RENAME Clause

Specify `RENAME` `TO` `new_name` to rename the trigger. Oracle Database renames the trigger and leaves it in the same state it was in before being renamed.

When you rename a trigger, the database rebuilds the remembered source of the trigger in the `USER_SOURCE`, `ALL_SOURCE`, and `DBA_SOURCE` data dictionary views. As a result, comments and formatting may change in the `TEXT` column of those views even though the trigger source did not change.

trigger\_compile\_clause

See [Oracle Database PL/SQL Language Reference](../../appdev.112/e25519/alter_trigger.md#LNPLS99996) for the syntax and semantics of this clause and for complete information on creating and compiling triggers.