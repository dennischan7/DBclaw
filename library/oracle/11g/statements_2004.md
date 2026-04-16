# Oracle 11g - statements_2004
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_2004.htm

Prerequisites

The operator must already have been created by a previous `CREATE` `OPERATOR` statement. The operator must be in your own schema or you must have the `ALTER` `ANY` `OPERATOR` system privilege. You must have the `EXECUTE` object privilege on the operators and functions referenced in the `ALTER` `OPERATOR` statement.

Semantics

schema

Specify the schema containing the operator. If you omit this clause, then Oracle Database assumes the operator is in your own schema.

operator

Specify the name of the operator to be altered.

add\_binding\_clause

Use this clause to add an operator binding and specify its parameter data types and return type. The signature must be different from the signature of any existing binding for this operator.

If a binding of an operator is associated with an indextype and you add another binding to the operator, then Oracle Database does not automatically associate the new binding with the indextype. If you want to make such an association, then you must issue an explicit `ALTER` `INDEXTYPE` ... `ADD` `OPERATOR` statement.

implementation\_clause

This clause has the same semantics in `CREATE` `OPERATOR` and `ALTER` `OPERATOR` statements. For full information, refer to [implementation\_clause](statements_6004.md#i2160229) in the documentation on `CREATE` `OPERATOR`.

context\_clause

This clause has the same semantics in `CREATE` `OPERATOR` and `ALTER` `OPERATOR` statements. For full information, refer to [context\_clause](statements_6004.md#i2152088) in the documentation on `CREATE` `OPERATOR`.

using\_function\_clause

This clause has the same semantics in `CREATE` `OPERATOR` and `ALTER` `OPERATOR` statements. For full information, refer to [using\_function\_clause](statements_6004.md#i2152100) in the documentation on `CREATE` `OPERATOR`.

drop\_binding\_clause

Use this clause to specify the list of parameter data types of the binding you want to drop from the operator. You must specify `FORCE` if the binding has any dependent objects, such as an indextype or an ancillary operator binding. If you specify `FORCE`, then Oracle Database marks `INVALID` all objects that are dependent on the binding. The dependent objects are revalidated the next time they are referenced in a DDL or DML statement or a query.

You cannot use this clause to drop the only binding associated with this operator. Instead you must use the `DROP` `OPERATOR` statement. Refer to [DROP OPERATOR](statements_8023.md#i2067252) for more information.

COMPILE

Specify `COMPILE` to cause Oracle Database to recompile the operator.