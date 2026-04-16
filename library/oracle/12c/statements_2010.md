# Oracle 12c - statements_2010
Source: https://docs.oracle.com/database/121/SQLRF/statements_2010.htm

Purpose

Use the `ALTER` `PROFILE` statement to add, modify, or remove a resource limit or password management parameter in a profile.

Changes made to a profile with an `ALTER` `PROFILE` statement affect users only in their subsequent sessions, not in their current sessions.

Prerequisites

You must have the `ALTER` `PROFILE` system privilege.

To specify the `CONTAINER` clause, you must be connected to a multitenant container database (CDB). To specify `CONTAINER` `=` `ALL`, the current container must be the root. To specify `CONTAINER` `=` `CURRENT`, the current container must be a pluggable database (PDB).

Semantics

The keywords, parameters, and clauses in the `ALTER` `PROFILE` statement all have the same meaning as in the `CREATE` `PROFILE` statement.

You cannot remove a limit from the `DEFAULT` profile.

Refer to [CREATE PROFILE](statements_6012.md#i2065930) and to the examples in the next section for more information.

Examples

Making a Password Unavailable: Example The following statement makes the password of the `new_profile` profile (created in ["Creating a Profile: Example"](statements_6012.md#i2092094)) unavailable for reuse for 90 days:

```
ALTER PROFILE new_profile 
   LIMIT PASSWORD_REUSE_TIME 90 
   PASSWORD_REUSE_MAX UNLIMITED;
```

Setting Default Password Values: Example The following statement defaults the `PASSWORD_REUSE_TIME` value of the `app_user` profile (created in ["Setting Profile Resource Limits: Example"](statements_6012.md#i2120023)) to its defined value in the `DEFAULT` profile:

```
ALTER PROFILE app_user 
   LIMIT PASSWORD_REUSE_TIME DEFAULT
   PASSWORD_REUSE_MAX UNLIMITED;
```

Limiting Login Attempts and Password Lock Time: Example The following statement alters profile `app_user` with `FAILED_LOGIN_ATTEMPTS` set to 5 and `PASSWORD_LOCK_TIME` set to 1:

```
ALTER PROFILE app_user LIMIT
   FAILED_LOGIN_ATTEMPTS 5
   PASSWORD_LOCK_TIME 1;
```

This statement causes any user account to which the `app_user` profile is assigned to become locked for one day after five consecutive unsuccessful login attempts.

Changing Password Lifetime and Grace Period: Example The following statement modifies the profile `app_user2` `PASSWORD_LIFE_TIME` to 90 days and `PASSWORD_GRACE_TIME` to 5 days:

```
ALTER PROFILE app_user2 LIMIT
   PASSWORD_LIFE_TIME 90
   PASSWORD_GRACE_TIME 5;
```

Limiting Concurrent Sessions: Example This statement defines a new limit of 5 concurrent sessions for the `app_user` profile:

```
ALTER PROFILE app_user LIMIT SESSIONS_PER_USER 5;
```

If the `app_user` profile does not currently define a limit for `SESSIONS_PER_USER`, then the preceding statement adds the limit of 5 to the profile. If the profile already defines a limit, then the preceding statement redefines it to 5. Any user assigned the `app_user` profile is subsequently limited to 5 concurrent sessions.

Removing Profile Limits: Example This statement removes the `IDLE_TIME` limit from the `app_user` profile:

```
ALTER PROFILE app_user LIMIT IDLE_TIME DEFAULT;
```

Any user assigned the `app_user` profile is subject in their subsequent sessions to the `IDLE_TIME` limit defined in the `DEFAULT` profile.

Limiting Profile Idle Time: Example This statement defines a limit of 2 minutes of idle time for the `DEFAULT` profile:

```
ALTER PROFILE default LIMIT IDLE_TIME  2;
```

This `IDLE_TIME` limit applies to these users:

This statement defines unlimited idle time for the `app_user2` profile:

```
ALTER PROFILE app_user2 LIMIT IDLE_TIME UNLIMITED;
```

Any user assigned the `app_user2` profile is subsequently permitted unlimited idle time.