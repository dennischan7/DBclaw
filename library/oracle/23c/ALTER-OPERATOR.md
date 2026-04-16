# Oracle 23c - ALTER-OPERATOR
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-OPERATOR.html

Purpose

Use the `ALTER` `OPERATOR` statement to add bindings to, drop bindings from, or compile an existing operator.

Prerequisites

The operator must already have been created by a previous `CREATE` `OPERATOR` statement. The operator must be in your own schema or you must have the `ALTER` `ANY` `OPERATOR` system privilege. You must have the `EXECUTE` object privilege on the operators and functions referenced in the `ALTER` `OPERATOR` statement.

IF EXISTS

Specify `IF EXISTS` to alter an existing table.

Specifying `IF NOT EXISTS` with `ALTER VIEW` results in `ORA-11544: Incorrect IF EXISTS clause for ALTER/DROP statement`.

schema

Specify the schema containing the operator. If you omit this clause, then Oracle Database assumes the operator is in your own schema.

operator

Specify the name of the operator to be altered.

add\_binding\_clause

Use this clause to add an operator binding and specify its parameter data types and return type. The signature must be different from the signature of any existing binding for this operator.

If a binding of an operator is associated with an indextype and you add another binding to the operator, then Oracle Database does not automatically associate the new binding with the indextype. If you want to make such an association, then you must issue an explicit `ALTER` `INDEXTYPE` ... `ADD` `OPERATOR` statement.

implementation\_clause

This clause has the same semantics in `CREATE` `OPERATOR` and `ALTER` `OPERATOR` statements. For full information, refer to [implementation\_clause](CREATE-OPERATOR.md#GUID-62676C58-6F57-4572-8C09-7984A8E3EE9F__I2160229) in the documentation on `CREATE` `OPERATOR`.

context\_clause

This clause has the same semantics in `CREATE` `OPERATOR` and `ALTER` `OPERATOR` statements. For full information, refer to [context\_clause](CREATE-OPERATOR.md#GUID-62676C58-6F57-4572-8C09-7984A8E3EE9F__I2152088) in the documentation on `CREATE` `OPERATOR`.

using\_function\_clause

This clause has the same semantics in `CREATE` `OPERATOR` and `ALTER` `OPERATOR` statements. For full information, refer to [using\_function\_clause](CREATE-OPERATOR.md#GUID-62676C58-6F57-4572-8C09-7984A8E3EE9F__I2152100) in the documentation on `CREATE` `OPERATOR`.

drop\_binding\_clause

Use this clause to specify the list of parameter data types of the binding you want to drop from the operator. You must specify `FORCE` if the binding has any dependent objects, such as an indextype or an ancillary operator binding. If you specify `FORCE`, then Oracle Database marks `INVALID` all objects that are dependent on the binding. The dependent objects are revalidated the next time they are referenced in a DDL or DML statement or a query.

You cannot use this clause to drop the only binding associated with this operator. Instead you must use the `DROP` `OPERATOR` statement. Refer to [DROP OPERATOR](DROP-OPERATOR.md#GUID-48E60BB4-9490-4B8B-B08E-D17EAEBDDD7E) for more information.

COMPILE

Specify `COMPILE` to cause Oracle Database to recompile the operator.