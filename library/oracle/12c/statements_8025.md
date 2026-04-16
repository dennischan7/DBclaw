# Oracle 12c - statements_8025
Source: https://docs.oracle.com/database/121/SQLRF/statements_8025.htm

[Go to main content](#BEGIN)

480/555 

# DROP OPERATOR

Purpose

Use the `DROP` `OPERATOR` statement to drop a user-defined operator.

Prerequisites

The operator must be in your schema or you must have the `DROP` `ANY` `OPERATOR` system privilege.

Semantics

schema

Specify the schema containing the operator. If you omit `schema`, then Oracle Database assumes the operator is in your own schema.

operator

Specify the name of the operator to be dropped.

FORCE

Specify `FORCE` to drop the operator even if it is currently being referenced by one or more schema objects, such as indextypes, packages, functions, procedures, and so on. The database marks any such dependent objects `INVALID`. Without `FORCE`, you cannot drop an operator if any schema objects reference it.

Examples

Dropping a User-Defined Operator: Example The following statement drops the operator `eq_op`:

```
DROP OPERATOR eq_op;
```

Because the `FORCE` clause is not specified, this operation will fail if any of the bindings of this operator are referenced by an indextype.

Scripting on this page enhances content navigation, but does not change the content in any way.