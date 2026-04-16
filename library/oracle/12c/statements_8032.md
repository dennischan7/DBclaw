# Oracle 12c - statements_8032
Source: https://docs.oracle.com/database/121/SQLRF/statements_8032.htm

[Go to main content](#BEGIN)

487/555 

# DROP ROLE

Purpose

Use the `DROP` `ROLE` statement to remove a role from the database. When you drop a role, Oracle Database revokes it from all users and roles to whom it has been granted and removes it from the database. User sessions in which the role is already enabled are not affected. However, no new user session can enable the role after it is dropped.

Prerequisites

You must have been granted the role with the `ADMIN` `OPTION` or you must have the `DROP` `ANY` `ROLE` system privilege.

Semantics

role

Specify the name of the role to be dropped.

Examples

Dropping a Role: Example To drop the role `dw_manager`, which was created in ["Creating a Role: Example"](statements_6014.md#i2082342), issue the following statement:

```
DROP ROLE dw_manager;
```

Scripting on this page enhances content navigation, but does not change the content in any way.