# Oracle 11g - statements_8027
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8027.htm

[Go to main content](#BEGIN)

455/522 

# DROP PROFILE

Purpose

Use the `DROP` `PROFILE` statement to remove a profile from the database. You can drop any profile except the `DEFAULT` profile.

Prerequisites

You must have the `DROP` `PROFILE` system privilege.

Semantics

profile

Specify the name of the profile to be dropped.

CASCADE

Specify `CASCADE` to deassign the profile from any users to whom it is assigned. Oracle Database automatically assigns the `DEFAULT` profile to such users. You must specify this clause to drop a profile that is currently assigned to users.

Examples

Dropping a Profile: Example The following statement drops the profile `app_user`, which was created in ["Creating a Profile: Example"](statements_6010.md#i2092094). Oracle Database drops the profile `app_user` and assigns the `DEFAULT` profile to any users currently assigned the `app_user` profile:

```
DROP PROFILE app_user CASCADE;
```

Scripting on this page enhances content navigation, but does not change the content in any way.