---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL incorporates the concept of user account categories, based on the SYSTEM\_USER privilege.

- [System and Regular Accounts](#page-17-0)
- [Operations Affected by the SYSTEM\\_USER Privilege](#page-18-0)
- [System and Regular Sessions](#page-18-1)
- [Protecting System Accounts Against Manipulation by Regular Accounts](#page-19-0)

# <span id="page-17-0"></span>**System and Regular Accounts**

MySQL incorporates the concept of user account categories, with system and regular users distinguished according to whether they have the SYSTEM\_USER privilege:

- A user with the SYSTEM\_USER privilege is a system user.
- A user without the SYSTEM\_USER privilege is a regular user.

The SYSTEM\_USER privilege has an effect on the accounts to which a given user can apply its other privileges, as well as whether the user is protected from other accounts:

- A system user can modify both system and regular accounts. That is, a user who has the appropriate privileges to perform a given operation on regular accounts is enabled by possession of SYSTEM\_USER to also perform the operation on system accounts. A system account can be modified only by system users with appropriate privileges, not by regular users.
- A regular user with appropriate privileges can modify regular accounts, but not system accounts. A regular account can be modified by both system and regular users with appropriate privileges.

If a user has the appropriate privileges to perform a given operation on regular accounts, SYSTEM\_USER enables the user to also perform the operation on system accounts. SYSTEM\_USER does not imply any other privilege, so the ability to perform a given account operation remains

predicated on possession of any other required privileges. For example, if a user can grant the SELECT and UPDATE privileges to regular accounts, then with SYSTEM\_USER the user can also grant SELECT and UPDATE to system accounts.

The distinction between system and regular accounts enables better control over certain account administration issues by protecting accounts that have the SYSTEM\_USER privilege from accounts that do not have the privilege. For example, the CREATE USER privilege enables not only creation of new accounts, but modification and removal of existing accounts. Without the system user concept, a user who has the CREATE USER privilege can modify or drop any existing account, including the root account. The concept of system user enables restricting modifications to the root account (itself a system account) so they can be made only by system users. Regular users with the CREATE USER privilege can still modify or drop existing accounts, but only regular accounts.

# <span id="page-18-0"></span>**Operations Affected by the SYSTEM\_USER Privilege**

The SYSTEM\_USER privilege affects these operations:

• Account manipulation.

Account manipulation includes creating and dropping accounts, granting and revoking privileges, changing account authentication characteristics such as credentials or authentication plugin, and changing other account characteristics such as password expiration policy.

The SYSTEM\_USER privilege is required to manipulate system accounts using account-management statements such as CREATE USER and GRANT. To prevent an account from modifying system accounts this way, make it a regular account by not granting it the SYSTEM\_USER privilege. (However, to fully protect system accounts against regular accounts, you must also withhold modification privileges for the mysql system schema from regular accounts. See [Protecting System](#page-19-0) [Accounts Against Manipulation by Regular Accounts.](#page-19-0))

• Killing current sessions and statements executing within them.

To kill a session or statement that is executing with the SYSTEM\_USER privilege, your own session must have the SYSTEM\_USER privilege, in addition to any other required privilege (CONNECTION\_ADMIN or the deprecated SUPER privilege).

If the user that puts a server in offline mode does not have the SYSTEM\_USER privilege, connected client users who have the SYSTEM\_USER privilege are also not disconnected. However, these users cannot initiate new connections to the server while it is in offline mode, unless they have the CONNECTION\_ADMIN or SUPER privilege as well. It is only their existing connection that is not terminated, because the SYSTEM\_USER privilege is required to do that.

• Setting the DEFINER attribute for stored objects.

To set the DEFINER attribute for a stored object to an account that has the SYSTEM\_USER privilege, you must have the SYSTEM\_USER privilege, in addition to any other required privilege.

• Specifying mandatory roles.

A role that has the SYSTEM\_USER privilege cannot be listed in the value of the mandatory\_roles system variable.

• Overriding "abort" items in MySQL Enterprise Audit's audit log filter.

Accounts with the SYSTEM\_USER privilege are automatically assigned the AUDIT\_ABORT\_EXEMPT privilege, so that queries from the account are always executed even if an "abort" item in the audit log filter would block them. Accounts with the SYSTEM\_USER privilege can therefore be used to regain access to a system following an audit misconfiguration. See Section 8.4.5, "MySQL Enterprise Audit".

# <span id="page-18-1"></span>**System and Regular Sessions**

Sessions executing within the server are distinguished as system or regular sessions, similar to the distinction between system and regular users:

- A session that possesses the SYSTEM\_USER privilege is a system session.
- A session that does not possess the SYSTEM\_USER privilege is a regular session.

A regular session is able to perform only operations permitted to regular users. A system session is additionally able to perform operations permitted only to system users.

The privileges possessed by a session are those granted directly to its underlying account, plus those granted to all roles currently active within the session. Thus, a session may be a system session because its account has been granted the SYSTEM\_USER privilege directly, or because the session has activated a role that has the SYSTEM\_USER privilege. Roles granted to an account that are not active within the session do not affect session privileges.

Because activating and deactivating roles can change the privileges possessed by sessions, a session may change from a regular session to a system session or vice versa. If a session activates or deactivates a role that has the SYSTEM\_USER privilege, the appropriate change between regular and system session takes place immediately, for that session only:

- If a regular session activates a role with the SYSTEM\_USER privilege, the session becomes a system session.
- If a system session deactivates a role with the SYSTEM\_USER privilege, the session becomes a regular session, unless some other role with the SYSTEM\_USER privilege remains active.

These operations have no effect on existing sessions:

- If the SYSTEM\_USER privilege is granted to or revoked from an account, existing sessions for the account do not change between regular and system sessions. The grant or revoke operation affects only sessions for subsequent connections by the account.
- Statements executed by a stored object invoked within a session execute with the system or regular status of the parent session, even if the object DEFINER attribute names a system account.

Because role activation affects only sessions and not accounts, granting a role that has the SYSTEM\_USER privilege to a regular account does not protect that account against regular users. The role protects only sessions for the account in which the role has been activated, and protects the session only against being killed by regular sessions.

# <span id="page-19-0"></span>**Protecting System Accounts Against Manipulation by Regular Accounts**

Account manipulation includes creating and dropping accounts, granting and revoking privileges, changing account authentication characteristics such as credentials or authentication plugin, and changing other account characteristics such as password expiration policy.

Account manipulation can be done two ways:

- By using account-management statements such as CREATE USER and GRANT. This is the preferred method.
- By direct grant-table modification using statements such as INSERT and UPDATE. This method is discouraged but possible for users with the appropriate privileges on the mysql system schema that contains the grant tables.

To fully protect system accounts against modification by a given account, make it a regular account and do not grant it modification privileges for the mysql schema:

• The SYSTEM\_USER privilege is required to manipulate system accounts using account-management statements. To prevent an account from modifying system accounts this way, make it a regular account by not granting SYSTEM\_USER to it. This includes not granting SYSTEM\_USER to any roles granted to the account.

• Privileges for the mysql schema enable manipulation of system accounts through direct modification of the grant tables, even if the modifying account is a regular account. To restrict unauthorized direct modification of system accounts by a regular account, do not grant modification privileges for the mysql schema to the account (or any roles granted to the account). If a regular account must have global privileges that apply to all schemas, mysql schema modifications can be prevented using privilege restrictions imposed using partial revokes. See [Section 8.2.12, "Privilege Restriction Using](#page-20-0) [Partial Revokes"](#page-20-0).

![](_page_20_Picture_2.jpeg)

#### **Note**

Unlike withholding the SYSTEM\_USER privilege, which prevents an account from modifying system accounts but not regular accounts, withholding mysql schema privileges prevents an account from modifying system accounts as well as regular accounts. This should not be an issue because, as mentioned, direct grant-table modification is discouraged.

Suppose that you want to create a user u1 who has all privileges on all schemas, except that u1 should be a regular user without the ability to modify system accounts. Assuming that the partial\_revokes system variable is enabled, configure u1 as follows:

```
CREATE USER u1 IDENTIFIED BY 'password';
GRANT ALL ON *.* TO u1 WITH GRANT OPTION;
-- GRANT ALL includes SYSTEM_USER, so at this point
-- u1 can manipulate system or regular accounts
REVOKE SYSTEM_USER ON *.* FROM u1;
-- Revoking SYSTEM_USER makes u1 a regular user;
-- now u1 can use account-management statements
-- to manipulate only regular accounts
REVOKE ALL ON mysql.* FROM u1;
-- This partial revoke prevents u1 from directly
-- modifying grant tables to manipulate accounts
```

To prevent all mysql system schema access by an account, revoke all its privileges on the mysql schema, as just shown. It is also possible to permit partial mysql schema access, such as read-only access. The following example creates an account that has SELECT, INSERT, UPDATE, and DELETE privileges globally for all schemas, but only SELECT for the mysql schema:

```
CREATE USER u2 IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO u2;
REVOKE INSERT, UPDATE, DELETE ON mysql.* FROM u2;
```

Another possibility is to revoke all mysql schema privileges but grant access to specific mysql tables or columns. This can be done even with a partial revoke on mysql. The following statements enable read-only access to u1 within the mysql schema, but only for the db table and the Host and User columns of the user table:

```
CREATE USER u3 IDENTIFIED BY 'password';
GRANT ALL ON *.* TO u3;
REVOKE ALL ON mysql.* FROM u3;
GRANT SELECT ON mysql.db TO u3;
GRANT SELECT(Host,User) ON mysql.user TO u3;
```

# <span id="page-20-0"></span>**8.2.12 Privilege Restriction Using Partial Revokes**

It is possible to grant privileges that apply globally if the partial\_revokes system variable is enabled. Specifically, for users who have privileges at the global level, partial\_revokes enables privileges for specific schemas to be revoked while leaving the privileges in place for other schemas. Privilege restrictions thus imposed may be useful for administration of accounts that have global privileges but should not be permitted to access certain schemas. For example, it is possible to permit an account to modify any table except those in the mysql system schema.

- [Using Partial Revokes](#page-21-0)
- [Partial Revokes Versus Explicit Schema Grants](#page-25-0)
- [Disabling Partial Revokes](#page-26-0)
- [Partial Revokes and Replication](#page-26-1)

![](_page_21_Picture_5.jpeg)

### **Note**

For brevity, CREATE USER statements shown here do not include passwords. For production use, always assign account passwords.

# <span id="page-21-0"></span>**Using Partial Revokes**

The partial\_revokes system variable controls whether privilege restrictions can be placed on accounts. By default, partial\_revokes is disabled and attempts to partially revoke global privileges produce an error:

```
mysql> CREATE USER u1;
mysql> GRANT SELECT, INSERT ON *.* TO u1;
mysql> REVOKE INSERT ON world.* FROM u1;
ERROR 1141 (42000): There is no such grant defined for user 'u1' on host '%'
```

To permit the REVOKE operation, enable partial\_revokes:

```
SET PERSIST partial_revokes = ON;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it to carry over to subsequent server restarts. To change the value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST. See Section 15.7.6.1, "SET Syntax for Variable Assignment".

With partial\_revokes enabled, the partial revoke succeeds:

```
mysql> REVOKE INSERT ON world.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+------------------------------------------+
| Grants for u1@% |
+------------------------------------------+
| GRANT SELECT, INSERT ON *.* TO `u1`@`%` |
| REVOKE INSERT ON `world`.* FROM `u1`@`%` |
+------------------------------------------+
```

SHOW GRANTS lists partial revokes as REVOKE statements in its output. The result indicates that u1 has global SELECT and INSERT privileges, except that INSERT cannot be exercised for tables in the world schema. That is, access by u1 to world tables is read only.

The server records privilege restrictions implemented through partial revokes in the mysql.user system table. If an account has partial revokes, its User\_attributes column value has a Restrictions attribute:

```
mysql> SELECT User, Host, User_attributes->>'$.Restrictions'
 FROM mysql.user WHERE User_attributes->>'$.Restrictions' <> '';
+------+------+------------------------------------------------------+
| User | Host | User_attributes->>'$.Restrictions' |
+------+------+------------------------------------------------------+
| u1 | % | [{"Database": "world", "Privileges": ["INSERT"]}] |
+------+------+------------------------------------------------------+
```

![](_page_21_Picture_19.jpeg)

#### **Note**

Although partial revokes can be imposed for any schema, privilege restrictions on the mysql system schema in particular are useful as part of a strategy for preventing regular accounts from modifying system accounts. See [Protecting](#page-19-0) [System Accounts Against Manipulation by Regular Accounts](#page-19-0).

Partial revoke operations are subject to these conditions:

- It is possible to use partial revokes to place restrictions on nonexistent schemas, but only if the revoked privilege is granted globally. If a privilege is not granted globally, revoking it for a nonexistent schema produces an error.
- Partial revokes apply at the schema level only. You cannot use partial revokes for privileges that apply only globally (such as FILE or BINLOG\_ADMIN), or for table, column, or routine privileges.
- In privilege assignments, enabling partial\_revokes causes MySQL to interpret occurrences of unescaped \_ and % SQL wildcard characters in schema names as literal characters, just as if they had been escaped as \\_ and \%. Because this changes how MySQL interprets privileges, it may be advisable to avoid unescaped wildcard characters in privilege assignments for installations where partial\_revokes may be enabled.

As mentioned previously, partial revokes of schema-level privileges appear in SHOW GRANTS output as REVOKE statements. This differs from how SHOW GRANTS represents "plain" schema-level privileges:

• When granted, schema-level privileges are represented by their own GRANT statements in the output:

```
mysql> CREATE USER u1;
mysql> GRANT UPDATE ON mysql.* TO u1;
mysql> GRANT DELETE ON world.* TO u1;
mysql> SHOW GRANTS FOR u1;
+---------------------------------------+
| Grants for u1@% |
+---------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`%` |
| GRANT UPDATE ON `mysql`.* TO `u1`@`%` |
| GRANT DELETE ON `world`.* TO `u1`@`%` |
+---------------------------------------+
```

• When revoked, schema-level privileges simply disappear from the output. They do not appear as REVOKE statements:

```
mysql> REVOKE UPDATE ON mysql.* FROM u1;
mysql> REVOKE DELETE ON world.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+--------------------------------+
| Grants for u1@% |
+--------------------------------+
| GRANT USAGE ON *.* TO `u1`@`%` |
+--------------------------------+
```

When a user grants a privilege, any restriction the grantor has on the privilege is inherited by the grantee, unless the grantee already has the privilege without the restriction. Consider the following two users, one of whom has the global SELECT privilege:

```
CREATE USER u1, u2;
GRANT SELECT ON *.* TO u2;
```

Suppose that an administrative user admin has a global but partially revoked SELECT privilege:

```
mysql> CREATE USER admin;
mysql> GRANT SELECT ON *.* TO admin WITH GRANT OPTION;
mysql> REVOKE SELECT ON mysql.* FROM admin;
mysql> SHOW GRANTS FOR admin;
+------------------------------------------------------+
| Grants for admin@% |
+------------------------------------------------------+
| GRANT SELECT ON *.* TO `admin`@`%` WITH GRANT OPTION |
| REVOKE SELECT ON `mysql`.* FROM `admin`@`%` |
+------------------------------------------------------+
```

If admin grants SELECT globally to u1 and u2, the result differs for each user:

• If admin grants SELECT globally to u1, who has no SELECT privilege to begin with, u1 inherits the admin privilege restriction:

```
mysql> GRANT SELECT ON *.* TO u1;
mysql> SHOW GRANTS FOR u1;
+------------------------------------------+
| Grants for u1@% |
+------------------------------------------+
| GRANT SELECT ON *.* TO `u1`@`%` |
| REVOKE SELECT ON `mysql`.* FROM `u1`@`%` |
+------------------------------------------+
```

• On the other hand, u2 already holds a global SELECT privilege without restriction. GRANT can only add to a grantee's existing privileges, not reduce them, so if admin grants SELECT globally to u2, u2 does not inherit the admin restriction:

```
mysql> GRANT SELECT ON *.* TO u2;
mysql> SHOW GRANTS FOR u2;
+---------------------------------+
| Grants for u2@% |
+---------------------------------+
| GRANT SELECT ON *.* TO `u2`@`%` |
+---------------------------------+
```

If a GRANT statement includes an AS user clause, the privilege restrictions applied are those on the user/role combination specified by the clause, rather than those on the user who executes the statement. For information about the AS clause, see Section 15.7.1.6, "GRANT Statement".

Restrictions on new privileges granted to an account are added to any existing restrictions for that account:

```
mysql> CREATE USER u1;
mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO u1;
mysql> REVOKE INSERT ON mysql.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+---------------------------------------------------------+
| Grants for u1@% |
+---------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO `u1`@`%` |
| REVOKE INSERT ON `mysql`.* FROM `u1`@`%` |
+---------------------------------------------------------+
mysql> REVOKE DELETE, UPDATE ON db2.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+---------------------------------------------------------+
| Grants for u1@% |
+---------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO `u1`@`%` |
| REVOKE UPDATE, DELETE ON `db2`.* FROM `u1`@`%` |
| REVOKE INSERT ON `mysql`.* FROM `u1`@`%` |
+---------------------------------------------------------+
```

Aggregation of privilege restrictions applies both when privileges are partially revoked explicitly (as just shown) and when restrictions are inherited implicitly from the user who executes the statement or the user mentioned in an AS user clause.

If an account has a privilege restriction on a schema:

- The account cannot grant to other accounts a privilege on the restricted schema or any object within it.
- Another account that does not have the restriction can grant privileges to the restricted account for the restricted schema or objects within it. Suppose that an unrestricted user executes these statements:

```
CREATE USER u1;
GRANT SELECT, INSERT, UPDATE ON *.* TO u1;
REVOKE SELECT, INSERT, UPDATE ON mysql.* FROM u1;
GRANT SELECT ON mysql.user TO u1; -- grant table privilege
```

```
GRANT SELECT(Host,User) ON mysql.db TO u1; -- grant column privileges
```

The resulting account has these privileges, with the ability to perform limited operations within the restricted schema:

```
mysql> SHOW GRANTS FOR u1;
+-----------------------------------------------------------+
| Grants for u1@% |
+-----------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE ON *.* TO `u1`@`%` |
| REVOKE SELECT, INSERT, UPDATE ON `mysql`.* FROM `u1`@`%` |
| GRANT SELECT (`Host`, `User`) ON `mysql`.`db` TO `u1`@`%` |
| GRANT SELECT ON `mysql`.`user` TO `u1`@`%` |
+-----------------------------------------------------------+
```

If an account has a restriction on a global privilege, the restriction is removed by any of these actions:

- Granting the privilege globally to the account by an account that has no restriction on the privilege.
- Granting the privilege at the schema level.
- Revoking the privilege globally.

Consider a user u1 who holds several privileges globally, but with restrictions on INSERT, UPDATE and DELETE:

```
mysql> CREATE USER u1;
mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO u1;
mysql> REVOKE INSERT, UPDATE, DELETE ON mysql.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+----------------------------------------------------------+
| Grants for u1@% |
+----------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO `u1`@`%` |
| REVOKE INSERT, UPDATE, DELETE ON `mysql`.* FROM `u1`@`%` |
+----------------------------------------------------------+
```

Granting a privilege globally to u1 from an account with no restriction removes the privilege restriction. For example, to remove the INSERT restriction:

```
mysql> GRANT INSERT ON *.* TO u1;
mysql> SHOW GRANTS FOR u1;
+---------------------------------------------------------+
| Grants for u1@% |
+---------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO `u1`@`%` |
| REVOKE UPDATE, DELETE ON `mysql`.* FROM `u1`@`%` |
+---------------------------------------------------------+
```

Granting a privilege at the schema level to u1 removes the privilege restriction. For example, to remove the UPDATE restriction:

```
mysql> GRANT UPDATE ON mysql.* TO u1;
mysql> SHOW GRANTS FOR u1;
+---------------------------------------------------------+
| Grants for u1@% |
+---------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO `u1`@`%` |
| REVOKE DELETE ON `mysql`.* FROM `u1`@`%` |
+---------------------------------------------------------+
```

Revoking a global privilege removes the privilege, including any restrictions on it. For example, to remove the DELETE restriction (at the cost of removing all DELETE access):

```
mysql> REVOKE DELETE ON *.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+-------------------------------------------------+
| Grants for u1@% |
+-------------------------------------------------+
```

```
| GRANT SELECT, INSERT, UPDATE ON *.* TO `u1`@`%` |
+-------------------------------------------------+
```

If an account has a privilege at both the global and schema levels, you must revoke it at the schema level twice to effect a partial revoke. Suppose that u1 has these privileges, where INSERT is held both globally and on the world schema:

```
mysql> CREATE USER u1;
mysql> GRANT SELECT, INSERT ON *.* TO u1;
mysql> GRANT INSERT ON world.* TO u1;
mysql> SHOW GRANTS FOR u1;
+-----------------------------------------+
| Grants for u1@% |
+-----------------------------------------+
| GRANT SELECT, INSERT ON *.* TO `u1`@`%` |
| GRANT INSERT ON `world`.* TO `u1`@`%` |
+-----------------------------------------+
```

Revoking INSERT on world revokes the schema-level privilege (SHOW GRANTS no longer displays the schema-level GRANT statement):

```
mysql> REVOKE INSERT ON world.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+-----------------------------------------+
| Grants for u1@% |
+-----------------------------------------+
| GRANT SELECT, INSERT ON *.* TO `u1`@`%` |
+-----------------------------------------+
```

Revoking INSERT on world again performs a partial revoke of the global privilege (SHOW GRANTS now includes a schema-level REVOKE statement):

```
mysql> REVOKE INSERT ON world.* FROM u1;
mysql> SHOW GRANTS FOR u1;
+------------------------------------------+
| Grants for u1@% |
+------------------------------------------+
| GRANT SELECT, INSERT ON *.* TO `u1`@`%` |
| REVOKE INSERT ON `world`.* FROM `u1`@`%` |
+------------------------------------------+
```

# <span id="page-25-0"></span>**Partial Revokes Versus Explicit Schema Grants**

To provide access to accounts for some schemas but not others, partial revokes provide an alternative to the approach of explicitly granting schema-level access without granting global privileges. The two approaches have different advantages and disadvantages.

Granting schema-level privileges and not global privileges:

- Adding a new schema: The schema is inaccessible to existing accounts by default. For any account to which the schema should be accessible, the DBA must grant schema-level access.
- Adding a new account: The DBA must grant schema-level access for each schema to which the account should have access.

Granting global privileges in conjunction with partial revokes:

- Adding a new schema: The schema is accessible to existing accounts that have global privileges. For any such account to which the schema should be inaccessible, the DBA must add a partial revoke.
- Adding a new account: The DBA must grant the global privileges, plus a partial revoke on each restricted schema.

The approach that uses explicit schema-level grant is more convenient for accounts for which access is limited to a few schemas. The approach that uses partial revokes is more convenient for accounts with broad access to all schemas except a few.

# <span id="page-26-0"></span>**Disabling Partial Revokes**

Once enabled, partial\_revokes cannot be disabled if any account has privilege restrictions. If any such account exists, disabling partial\_revokes fails:

- For attempts to disable partial\_revokes at startup, the server logs an error message and enables partial\_revokes.
- For attempts to disable partial\_revokes at runtime, an error occurs and the partial\_revokes value remains unchanged.

To disable partial\_revokes when restrictions exist, the restrictions first must be removed:

1. Determine which accounts have partial revokes:

```
SELECT User, Host, User_attributes->>'$.Restrictions'
FROM mysql.user WHERE User_attributes->>'$.Restrictions' <> '';
```

2. For each such account, remove its privilege restrictions. Suppose that the previous step shows account u1 to have these restrictions:

```
[{"Database": "world", "Privileges": ["INSERT", "DELETE"]
```

Restriction removal can be done various ways:

• Grant the privileges globally, without restrictions:

```
GRANT INSERT, DELETE ON *.* TO u1;
```

• Grant the privileges at the schema level:

```
GRANT INSERT, DELETE ON world.* TO u1;
```

• Revoke the privileges globally (assuming that they are no longer needed):

```
REVOKE INSERT, DELETE ON *.* FROM u1;
```

• Remove the account itself (assuming that it is no longer needed):

```
DROP USER u1;
```

After all privilege restrictions are removed, it is possible to disable partial revokes:

```
SET PERSIST partial_revokes = OFF;
```

# <span id="page-26-1"></span>**Partial Revokes and Replication**

In replication scenarios, if partial\_revokes is enabled on any host, it must be enabled on all hosts. Otherwise, REVOKE statements to partially revoke a global privilege do not have the same effect for all hosts on which replication occurs, potentially resulting in replication inconsistencies or errors.

When partial\_revokes is enabled, an extended syntax is recorded in the binary log for GRANT statements, including the current user that issued the statement and their currently active roles. If a user or a role recorded in this way does not exist on the replica, the replication applier thread stops at the GRANT statement with an error. Ensure that all user accounts that issue or might issue GRANT statements on the replication source server also exist on the replica, and have the same set of roles as they have on the source.

# <span id="page-26-2"></span>**8.2.13 When Privilege Changes Take Effect**

If the mysqld server is started without the --skip-grant-tables option, it reads all grant table contents into memory during its startup sequence. The in-memory tables become effective for access control at that point.

If you modify the grant tables indirectly using an account-management statement, the server notices these changes and loads the grant tables into memory again immediately. Account-management statements are described in Section 15.7.1, "Account Management Statements". Examples include GRANT, REVOKE, SET PASSWORD, and RENAME USER.

If you modify the grant tables directly using statements such as INSERT, UPDATE, or DELETE (which is not recommended), the changes have no effect on privilege checking until you either tell the server to reload the tables or restart it. Thus, if you change the grant tables directly but forget to reload them, the changes have no effect until you restart the server. This may leave you wondering why your changes seem to make no difference!

To tell the server to reload the grant tables, perform a flush-privileges operation. This can be done by issuing a FLUSH PRIVILEGES statement or by executing a mysqladmin flush-privileges or mysqladmin reload command.

A grant table reload affects privileges for each existing client session as follows:

- Table and column privilege changes take effect with the client's next request.
- Database privilege changes take effect the next time the client executes a USE db\_name statement.

![](_page_27_Picture_7.jpeg)

#### **Note**

Client applications may cache the database name; thus, this effect may not be visible to them without actually changing to a different database.

• Static global privileges and passwords are unaffected for a connected client. These changes take effect only in sessions for subsequent connections. Changes to dynamic global privileges apply immediately. For information about the differences between static and dynamic privileges, see Static Versus Dynamic Privileges.)

Changes to the set of active roles within a session take effect immediately, for that session only. The SET ROLE statement performs session role activation and deactivation (see Section 15.7.1.11, "SET ROLE Statement").

If the server is started with the --skip-grant-tables option, it does not read the grant tables or implement any access control. Any user can connect and perform any operation, which is insecure. To cause a server thus started to read the tables and enable access checking, flush the privileges.

# <span id="page-27-0"></span>**8.2.14 Assigning Account Passwords**

Required credentials for clients that connect to the MySQL server can include a password. This section describes how to assign passwords for MySQL accounts.

MySQL stores credentials in the user table in the mysql system database. Operations that assign or modify passwords are permitted only to users with the CREATE USER privilege, or, alternatively, privileges for the mysql database (INSERT privilege to create new accounts, UPDATE privilege to modify existing accounts). If the read\_only system variable is enabled, use of account-modification statements such as CREATE USER or ALTER USER additionally requires the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege).

The discussion here summarizes syntax only for the most common password-assignment statements. For complete details on other possibilities, see Section 15.7.1.3, "CREATE USER Statement", Section 15.7.1.1, "ALTER USER Statement", and Section 15.7.1.10, "SET PASSWORD Statement".

MySQL uses plugins to perform client authentication; see [Section 8.2.17, "Pluggable Authentication"](#page-41-0). In password-assigning statements, the authentication plugin associated with an account performs any hashing required of a cleartext password specified. This enables MySQL to obfuscate passwords prior to storing them in the mysql.user system table. For the statements described here, MySQL automatically hashes the password specified. There are also syntax for CREATE USER and ALTER USER that permits hashed values to be specified literally. For details, see the descriptions of those statements.

To assign a password when you create a new account, use CREATE USER and include an IDENTIFIED BY clause:

```
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
```

CREATE USER also supports syntax for specifying the account authentication plugin. See Section 15.7.1.3, "CREATE USER Statement".

To assign or change a password for an existing account, use the ALTER USER statement with an IDENTIFIED BY clause:

```
ALTER USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
```

If you are not connected as an anonymous user, you can change your own password without naming your own account literally:

```
ALTER USER USER() IDENTIFIED BY 'password';
```

To change an account password from the command line, use the mysqladmin command:

```
mysqladmin -u user_name -h host_name password "password"
```

The account for which this command sets the password is the one with a row in the mysql.user system table that matches user\_name in the User column and the client host from which you connect in the Host column.

![](_page_28_Picture_11.jpeg)

#### **Warning**

Setting a password using mysqladmin should be considered insecure. On some systems, your password becomes visible to system status programs such as ps that may be invoked by other users to display command lines. MySQL clients typically overwrite the command-line password argument with zeros during their initialization sequence. However, there is still a brief interval during which the value is visible. Also, on some systems this overwriting strategy is ineffective and the password remains visible to ps. (SystemV Unix systems and perhaps others are subject to this problem.)

If you are using MySQL Replication, be aware that a password used by a replica as part of CHANGE REPLICATION SOURCE TO is effectively limited to 32 characters in length; if the password is longer, any excess characters are truncated. This is not due to any limit imposed by MySQL Server generally, but rather is an issue specific to MySQL Replication.

# <span id="page-28-0"></span>**8.2.15 Password Management**

MySQL supports these password-management capabilities:

- Password expiration, to require passwords to be changed periodically.
- Password reuse restrictions, to prevent old passwords from being chosen again.
- Password verification, to require that password changes also specify the current password to be replaced.
- Dual passwords, to enable clients to connect using either a primary or secondary password.
- Password strength assessment, to require strong passwords.
- Random password generation, as an alternative to requiring explicit administrator-specified literal passwords.
- Password failure tracking, to enable temporary account locking after too many consecutive incorrectpassword login failures.

The following sections describe these capabilities, except password strength assessment, which is implemented using the validate\_password component and is described in [Section 8.4.3, "The](#page-192-0) [Password Validation Component"](#page-192-0).

- [Internal Versus External Credentials Storage](#page-29-0)
- [Password Expiration Policy](#page-29-1)
- [Password Reuse Policy](#page-31-0)
- [Password Verification-Required Policy](#page-33-0)
- [Dual Password Support](#page-35-0)
- [Random Password Generation](#page-37-0)
- [Failed-Login Tracking and Temporary Account Locking](#page-38-0)

![](_page_29_Picture_9.jpeg)

#### **Important**

MySQL implements password-management capabilities using tables in the mysql system database. If you upgrade MySQL from an earlier version, your system tables might not be up to date. In that case, the server writes messages similar to these to the error log during the startup process (the exact numbers may vary):

```
[ERROR] Column count of mysql.user is wrong. Expected
49, found 47. The table is probably corrupted
[Warning] ACL table mysql.password_history missing.
Some operations may fail.
```

To correct the issue, perform the MySQL upgrade procedure. See Chapter 3, Upgrading MySQL. Until this is done, password changes are not possible.

# <span id="page-29-0"></span>**Internal Versus External Credentials Storage**

Some authentication plugins store account credentials internally to MySQL, in the mysql.user system table:

- caching\_sha2\_password
- mysql\_native\_password (deprecated)
- sha256\_password (deprecated)

Most discussion in this section applies to such authentication plugins because most passwordmanagement capabilities described here are based on internal credentials storage handled by MySQL itself. Other authentication plugins store account credentials externally to MySQL. For accounts that use plugins that perform authentication against an external credentials system, password management must be handled externally against that system as well.

The exception is that the options for failed-login tracking and temporary account locking apply to all accounts, not just accounts that use internal credentials storage, because MySQL is able to assess the status of login attempts for any account no matter whether it uses internal or external credentials storage.

For information about individual authentication plugins, see [Section 8.4.1, "Authentication Plugins".](#page-93-0)

# <span id="page-29-1"></span>**Password Expiration Policy**

MySQL enables database administrators to expire account passwords manually, and to establish a policy for automatic password expiration. Expiration policy can be established globally, and individual accounts can be set to either defer to the global policy or override the global policy with specific peraccount behavior.

To expire an account password manually, use the ALTER USER statement:

```
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE;
```

This operation marks the password expired in the corresponding row in the mysql.user system table.

Password expiration according to policy is automatic and is based on password age, which for a given account is assessed from the date and time of its most recent password change. The mysql.user system table indicates for each account when its password was last changed, and the server automatically treats the password as expired at client connection time if its age is greater than its permitted lifetime. This works with no explicit manual password expiration.

To establish automatic password-expiration policy globally, use the default\_password\_lifetime system variable. Its default value is 0, which disables automatic password expiration. If the value of default\_password\_lifetime is a positive integer N, it indicates the permitted password lifetime, such that passwords must be changed every N days.

### Examples:

• To establish a global policy that passwords have a lifetime of approximately six months, start the server with these lines in a server my.cnf file:

```
[mysqld]
default_password_lifetime=180
```

• To establish a global policy such that passwords never expire, set default\_password\_lifetime to 0:

```
[mysqld]
default_password_lifetime=0
```

• default\_password\_lifetime can also be set and persisted at runtime:

```
SET PERSIST default_password_lifetime = 180;
SET PERSIST default_password_lifetime = 0;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value to carry over to subsequent server restarts; see Section 15.7.6.1, "SET Syntax for Variable Assignment". To change the value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST.

The global password-expiration policy applies to all accounts that have not been set to override it. To establish policy for individual accounts, use the PASSWORD EXPIRE option of the CREATE USER and ALTER USER statements. See Section 15.7.1.3, "CREATE USER Statement", and Section 15.7.1.1, "ALTER USER Statement".

Example account-specific statements:

• Require the password to be changed every 90 days:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
```

This expiration option overrides the global policy for all accounts named by the statement.

• Disable password expiration:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE NEVER;
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE NEVER;
```

This expiration option overrides the global policy for all accounts named by the statement.

• Defer to the global expiration policy for all accounts named by the statement:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD EXPIRE DEFAULT;
ALTER USER 'jeffrey'@'localhost' PASSWORD EXPIRE DEFAULT;
```

When a client successfully connects, the server determines whether the account password has expired:

- The server checks whether the password has been manually expired.
- Otherwise, the server checks whether the password age is greater than its permitted lifetime according to the automatic password expiration policy. If so, the server considers the password expired.

If the password is expired (whether manually or automatically), the server either disconnects the client or restricts the operations permitted to it (see [Section 8.2.16, "Server Handling of Expired Passwords"\)](#page-39-0). Operations performed by a restricted client result in an error until the user establishes a new account password:

```
mysql> SELECT 1;
ERROR 1820 (HY000): You must reset your password using ALTER USER
statement before executing this statement.
mysql> ALTER USER USER() IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.01 sec)
mysql> SELECT 1;
+---+
| 1 |
+---+
| 1 |
+---+
1 row in set (0.00 sec)
```

After the client resets the password, the server restores normal access for the session, as well as for subsequent connections that use the account. It is also possible for an administrative user to reset the account password, but any existing restricted sessions for that account remain restricted. A client using the account must disconnect and reconnect before statements can be executed successfully.

![](_page_31_Picture_9.jpeg)

### **Note**

Although it is possible to "reset" an expired password by setting it to its current value, it is preferable, as a matter of good policy, to choose a different password. DBAs can enforce non-reuse by establishing an appropriate password-reuse policy. See [Password Reuse Policy.](#page-31-0)

# <span id="page-31-0"></span>**Password Reuse Policy**

MySQL enables restrictions to be placed on reuse of previous passwords. Reuse restrictions can be established based on number of password changes, time elapsed, or both. Reuse policy can be established globally, and individual accounts can be set to either defer to the global policy or override the global policy with specific per-account behavior.

The password history for an account consists of passwords it has been assigned in the past. MySQL can restrict new passwords from being chosen from this history:

- If an account is restricted on the basis of number of password changes, a new password cannot be chosen from a specified number of the most recent passwords. For example, if the minimum number of password changes is set to 3, a new password cannot be the same as any of the most recent 3 passwords.
- If an account is restricted based on time elapsed, a new password cannot be chosen from passwords in the history that are newer than a specified number of days. For example, if the

password reuse interval is set to 60, a new password must not be among those previously chosen within the last 60 days.

![](_page_32_Picture_2.jpeg)

#### **Note**

The empty password does not count in the password history and is subject to reuse at any time.

To establish password-reuse policy globally, use the password\_history and password\_reuse\_interval system variables.

#### Examples:

• To prohibit reusing any of the last 6 passwords or passwords newer than 365 days, put these lines in the server my.cnf file:

```
[mysqld]
password_history=6
password_reuse_interval=365
```

• To set and persist the variables at runtime, use statements like this:

```
SET PERSIST password_history = 6;
SET PERSIST password_reuse_interval = 365;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value to carry over to subsequent server restarts; see Section 15.7.6.1, "SET Syntax for Variable Assignment". To change the value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST.

The global password-reuse policy applies to all accounts that have not been set to override it. To establish policy for individual accounts, use the PASSWORD HISTORY and PASSWORD REUSE INTERVAL options of the CREATE USER and ALTER USER statements. See Section 15.7.1.3, "CREATE USER Statement", and Section 15.7.1.1, "ALTER USER Statement".

Example account-specific statements:

• Require a minimum of 5 password changes before permitting reuse:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD HISTORY 5;
ALTER USER 'jeffrey'@'localhost' PASSWORD HISTORY 5;
```

This history-length option overrides the global policy for all accounts named by the statement.

• Require a minimum of 365 days elapsed before permitting reuse:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'jeffrey'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
```

This time-elapsed option overrides the global policy for all accounts named by the statement.

• To combine both types of reuse restrictions, use PASSWORD HISTORY and PASSWORD REUSE INTERVAL together:

```
CREATE USER 'jeffrey'@'localhost'
 PASSWORD HISTORY 5
 PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'jeffrey'@'localhost'
 PASSWORD HISTORY 5
 PASSWORD REUSE INTERVAL 365 DAY;
```

These options override both global policy reuse restrictions for all accounts named by the statement.

• Defer to the global policy for both types of reuse restrictions:

```
CREATE USER 'jeffrey'@'localhost'
```

```
 PASSWORD HISTORY DEFAULT
 PASSWORD REUSE INTERVAL DEFAULT;
ALTER USER 'jeffrey'@'localhost'
 PASSWORD HISTORY DEFAULT
 PASSWORD REUSE INTERVAL DEFAULT;
```

# <span id="page-33-0"></span>**Password Verification-Required Policy**

It is possible to require that attempts to change an account password be verified by specifying the current password to be replaced. This enables DBAs to prevent users from changing a password without proving that they know the current password. Such changes could otherwise occur, for example, if one user walks away from a terminal session temporarily without logging out, and a malicious user uses the session to change the original user's MySQL password. This can have unfortunate consequences:

- The original user becomes unable to access MySQL until the account password is reset by an administrator.
- Until the password reset occurs, the malicious user can access MySQL with the benign user's changed credentials.

Password-verification policy can be established globally, and individual accounts can be set to either defer to the global policy or override the global policy with specific per-account behavior.

For each account, its mysql.user row indicates whether there is an account-specific setting requiring verification of the current password for password change attempts. The setting is established by the PASSWORD REQUIRE option of the CREATE USER and ALTER USER statements:

- If the account setting is PASSWORD REQUIRE CURRENT, password changes must specify the current password.
- If the account setting is PASSWORD REQUIRE CURRENT OPTIONAL, password changes may but need not specify the current password.
- If the account setting is PASSWORD REQUIRE CURRENT DEFAULT, the password\_require\_current system variable determines the verification-required policy for the account:
  - If password\_require\_current is enabled, password changes must specify the current password.
  - If password\_require\_current is disabled, password changes may but need not specify the current password.

In other words, if the account setting is not PASSWORD REQUIRE CURRENT DEFAULT, the account setting takes precedence over the global policy established by the password\_require\_current system variable. Otherwise, the account defers to the password\_require\_current setting.

By default, password verification is optional: password\_require\_current is disabled and accounts created with no PASSWORD REQUIRE option default to PASSWORD REQUIRE CURRENT DEFAULT.

The following table shows how per-account settings interact with password\_require\_current system variable values to determine account password verification-required policy.

**Table 8.10 Password-Verification Policy**

| Per-Account Setting                  | password_require_current<br>System Variable | Password Changes Require<br>Current Password? |
|--------------------------------------|---------------------------------------------|-----------------------------------------------|
| PASSWORD REQUIRE CURRENT             | OFF                                         | Yes                                           |
| PASSWORD REQUIRE CURRENT             | ON                                          | Yes                                           |
| PASSWORD REQUIRE CURRENT<br>OPTIONAL | OFF                                         | No                                            |

| Per-Account Setting                  | password_require_current<br>System Variable | Password Changes Require<br>Current Password? |
|--------------------------------------|---------------------------------------------|-----------------------------------------------|
| PASSWORD REQUIRE CURRENT<br>OPTIONAL | ON                                          | No                                            |
| PASSWORD REQUIRE CURRENT<br>DEFAULT  | OFF                                         | No                                            |
| PASSWORD REQUIRE CURRENT<br>DEFAULT  | ON                                          | Yes                                           |

![](_page_34_Picture_2.jpeg)

#### **Note**

Privileged users can change any account password without specifying the current password, regardless of the verification-required policy. A privileged user is one who has the global CREATE USER privilege or the UPDATE privilege for the mysql system database.

To establish password-verification policy globally, use the password\_require\_current system variable. Its default value is OFF, so it is not required that account password changes specify the current password.

### Examples:

• To establish a global policy that password changes must specify the current password, start the server with these lines in a server my.cnf file:

```
[mysqld]
password_require_current=ON
```

• To set and persist password\_require\_current at runtime, use a statement such as one of these:

```
SET PERSIST password_require_current = ON;
SET PERSIST password_require_current = OFF;
```

SET PERSIST sets a value for the running MySQL instance. It also saves the value to carry over to subsequent server restarts; see Section 15.7.6.1, "SET Syntax for Variable Assignment". To change the value for the running MySQL instance without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST.

The global password verification-required policy applies to all accounts that have not been set to override it. To establish policy for individual accounts, use the PASSWORD REQUIRE options of the CREATE USER and ALTER USER statements. See Section 15.7.1.3, "CREATE USER Statement", and Section 15.7.1.1, "ALTER USER Statement".

Example account-specific statements:

• Require that password changes specify the current password:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT;
ALTER USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT;
```

This verification option overrides the global policy for all accounts named by the statement.

• Do not require that password changes specify the current password (the current password may but need not be given):

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT OPTIONAL;
ALTER USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT OPTIONAL;
```

This verification option overrides the global policy for all accounts named by the statement.

• Defer to the global password verification-required policy for all accounts named by the statement:

```
CREATE USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT DEFAULT;
ALTER USER 'jeffrey'@'localhost' PASSWORD REQUIRE CURRENT DEFAULT;
```

Verification of the current password comes into play when a user changes a password using the ALTER USER or SET PASSWORD statement. The examples use ALTER USER, which is preferred over SET PASSWORD, but the principles described here are the same for both statements.

In password-change statements, a REPLACE clause specifies the current password to be replaced. Examples:

• Change the current user's password:

```
ALTER USER USER() IDENTIFIED BY 'auth_string' REPLACE 'current_auth_string';
```

• Change a named user's password:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED BY 'auth_string'
 REPLACE 'current_auth_string';
```

• Change a named user's authentication plugin and password:

```
ALTER USER 'jeffrey'@'localhost'
 IDENTIFIED WITH caching_sha2_password BY 'auth_string'
 REPLACE 'current_auth_string';
```

The REPLACE clause works like this:

- REPLACE must be given if password changes for the account are required to specify the current password, as verification that the user attempting to make the change actually knows the current password.
- REPLACE is optional if password changes for the account may but need not specify the current password.
- If REPLACE is specified, it must specify the correct current password, or an error occurs. This is true even if REPLACE is optional.
- REPLACE can be specified only when changing the account password for the current user. (This means that in the examples just shown, the statements that explicitly name the account for jeffrey fail unless the current user is jeffrey.) This is true even if the change is attempted for another user by a privileged user; however, such a user can change any password without specifying REPLACE.
- REPLACE is omitted from the binary log to avoid writing cleartext passwords to it.

# <span id="page-35-0"></span>**Dual Password Support**

User accounts are permitted to have dual passwords, designated as primary and secondary passwords. Dual-password capability makes it possible to seamlessly perform credential changes in scenarios like this:

- A system has a large number of MySQL servers, possibly involving replication.
- Multiple applications connect to different MySQL servers.
- Periodic credential changes must be made to the account or accounts used by the applications to connect to the servers.

Consider how a credential change must be performed in the preceding type of scenario when an account is permitted only a single password. In this case, there must be close cooperation in the timing of when the account password change is made and propagated throughout all servers, and when all applications that use the account are updated to use the new password. This process may involve downtime during which servers or applications are unavailable.

With dual passwords, credential changes can be made more easily, in phases, without requiring close cooperation, and without downtime:

- 1. For each affected account, establish a new primary password on the servers, retaining the current password as the secondary password. This enables servers to recognize either the primary or secondary password for each account, while applications can continue to connect to the servers using the same password as previously (which is now the secondary password).
- 2. After the password change has propagated to all servers, modify applications that use any affected account to connect using the account primary password.
- 3. After all applications have been migrated from the secondary passwords to the primary passwords, the secondary passwords are no longer needed and can be discarded. After this change has propagated to all servers, only the primary password for each account can be used to connect. The credential change is now complete.

MySQL implements dual-password capability with syntax that saves and discards secondary passwords:

- The RETAIN CURRENT PASSWORD clause for the ALTER USER and SET PASSWORD statements saves an account current password as its secondary password when you assign a new primary password.
- The DISCARD OLD PASSWORD clause for ALTER USER discards an account secondary password, leaving only the primary password.

Suppose that, for the previously described credential-change scenario, an account named 'appuser1'@'host1.example.com' is used by applications to connect to servers, and that the account password is to be changed from 'password\_a' to 'password\_b'.

To perform this change of credentials, use ALTER USER as follows:

1. On each server that is not a replica, establish 'password\_b' as the new appuser1 primary password, retaining the current password as the secondary password:

```
ALTER USER 'appuser1'@'host1.example.com'
 IDENTIFIED BY 'password_b'
 RETAIN CURRENT PASSWORD;
```

- 2. Wait for the password change to replicate throughout the system to all replicas.
- 3. Modify each application that uses the appuser1 account so that it connects to the servers using a password of 'password\_b' rather than 'password\_a'.
- 4. At this point, the secondary password is no longer needed. On each server that is not a replica, discard the secondary password:

```
ALTER USER 'appuser1'@'host1.example.com'
 DISCARD OLD PASSWORD;
```

5. After the discard-password change has replicated to all replicas, the credential change is complete.

The RETAIN CURRENT PASSWORD and DISCARD OLD PASSWORD clauses have the following effects:

- RETAIN CURRENT PASSWORD retains an account current password as its secondary password, replacing any existing secondary password. The new password becomes the primary password, but clients can use the account to connect to the server using either the primary or secondary password. (Exception: If the new password specified by the ALTER USER or SET PASSWORD statement is empty, the secondary password becomes empty as well, even if RETAIN CURRENT PASSWORD is given.)
- If you specify RETAIN CURRENT PASSWORD for an account that has an empty primary password, the statement fails.

- If an account has a secondary password and you change its primary password without specifying RETAIN CURRENT PASSWORD, the secondary password remains unchanged.
- For ALTER USER, if you change the authentication plugin assigned to the account, the secondary password is discarded. If you change the authentication plugin and also specify RETAIN CURRENT PASSWORD, the statement fails.
- For ALTER USER, DISCARD OLD PASSWORD discards the secondary password, if one exists. The account retains only its primary password, and clients can use the account to connect to the server only with the primary password.

Statements that modify secondary passwords require these privileges:

- The APPLICATION\_PASSWORD\_ADMIN privilege is required to use the RETAIN CURRENT PASSWORD or DISCARD OLD PASSWORD clause for ALTER USER and SET PASSWORD statements that apply to your own account. The privilege is required to manipulate your own secondary password because most users require only one password.
- If an account is to be permitted to manipulate secondary passwords for all accounts, it should be granted the CREATE USER privilege rather than APPLICATION\_PASSWORD\_ADMIN.

# <span id="page-37-0"></span>**Random Password Generation**

The CREATE USER, ALTER USER, and SET PASSWORD statements have the capability of generating random passwords for user accounts, as an alternative to requiring explicit administrator-specified literal passwords. See the description of each statement for details about the syntax. This section describes the characteristics common to generated random passwords.

By default, generated random passwords have a length of 20 characters. This length is controlled by the generated\_random\_password\_length system variable, which has a range from 5 to 255.

For each account for which a statement generates a random password, the statement stores the password in the mysql.user system table, hashed appropriately for the account authentication plugin. The statement also returns the cleartext password in a row of a result set to make it available to the user or application executing the statement. The result set columns are named user, host, generated password, and auth\_factor indicating the user name and host name values that identify the affected row in the mysql.user system table, the cleartext generated password, and the authentication factor the displayed password value applies to.

```
mysql> CREATE USER
 'u1'@'localhost' IDENTIFIED BY RANDOM PASSWORD,
 'u2'@'%.example.com' IDENTIFIED BY RANDOM PASSWORD,
 'u3'@'%.org' IDENTIFIED BY RANDOM PASSWORD;
+------+---------------+----------------------+-------------+
| user | host | generated password | auth_factor |
+------+---------------+----------------------+-------------+
| u1 | localhost | iOeqf>Mh9:;XD&qn(Hl} | 1 |
| u2 | %.example.com | sXTSAEvw3St-R+_-C3Vb | 1 |
| u3 | %.org | nEVe%Ctw/U/*Md)Exc7& | 1 |
+------+---------------+----------------------+-------------+
mysql> ALTER USER
 'u1'@'localhost' IDENTIFIED BY RANDOM PASSWORD,
 'u2'@'%.example.com' IDENTIFIED BY RANDOM PASSWORD;
+------+---------------+----------------------+-------------+
| user | host | generated password | auth_factor |
+------+---------------+----------------------+-------------+
| u1 | localhost | Seiei:&cw}8]@3OA64vh | 1 |
| u2 | %.example.com | j@&diTX80l8}(NiHXSae | 1 |
+------+---------------+----------------------+-------------+
mysql> SET PASSWORD FOR 'u3'@'%.org' TO RANDOM;
+------+-------+----------------------+-------------+
| user | host | generated password | auth_factor |
+------+-------+----------------------+-------------+
| u3 | %.org | n&cz2xF;P3!U)+]Vw52H | 1 |
+------+-------+----------------------+-------------+
```

A CREATE USER, ALTER USER, or SET PASSWORD statement that generates a random password for an account is written to the binary log as a CREATE USER or ALTER USER statement with an IDENTIFIED WITH auth\_plugin AS 'auth\_string', clause, where auth\_plugin is the account authentication plugin and 'auth\_string' is the account hashed password value.

If the validate\_password component is installed, the policy that it implements has no effect on generated passwords. (The purpose of password validation is to help humans create better passwords.)

# <span id="page-38-0"></span>**Failed-Login Tracking and Temporary Account Locking**

Administrators can configure user accounts such that too many consecutive login failures cause temporary account locking.

"Login failure" in this context means failure of the client to provide a correct password during a connection attempt. It does not include failure to connect for reasons such as unknown user or network issues. For accounts that have dual passwords (see [Dual Password Support\)](#page-35-0), either account password counts as correct.

The required number of login failures and the lock time are configurable per account, using the FAILED\_LOGIN\_ATTEMPTS and PASSWORD\_LOCK\_TIME options of the CREATE USER and ALTER USER statements. Examples:

```
CREATE USER 'u1'@'localhost' IDENTIFIED BY 'password'
 FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 3;
ALTER USER 'u2'@'localhost'
 FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME UNBOUNDED;
```

When too many consecutive login failures occur, the client receives an error that looks like this:

```
ERROR 3957 (HY000): Access denied for user user.
Account is blocked for D day(s) (R day(s) remaining)
due to N consecutive failed logins.
```

Use the options as follows:

• FAILED\_LOGIN\_ATTEMPTS N

This option indicates whether to track account login attempts that specify an incorrect password. The number N specifies how many consecutive incorrect passwords cause temporary account locking.

• PASSWORD\_LOCK\_TIME {N | UNBOUNDED}

This option indicates how long to lock the account after too many consecutive login attempts provide an incorrect password. The value is a number N to specify the number of days the account remains locked, or UNBOUNDED to specify that when an account enters the temporarily locked state, the duration of that state is unbounded and does not end until the account is unlocked. The conditions under which unlocking occurs are described later.

Permitted values of N for each option are in the range from 0 to 32767. A value of 0 disables the option.

Failed-login tracking and temporary account locking have these characteristics:

- For failed-login tracking and temporary locking to occur for an account, its FAILED\_LOGIN\_ATTEMPTS and PASSWORD\_LOCK\_TIME options both must be nonzero.
- For CREATE USER, if FAILED\_LOGIN\_ATTEMPTS or PASSWORD\_LOCK\_TIME is not specified, its implicit default value is 0 for all accounts named by the statement. This means that failed-login tracking and temporary account locking are disabled.
- For ALTER USER, if FAILED\_LOGIN\_ATTEMPTS or PASSWORD\_LOCK\_TIME is not specified, its value remains unchanged for all accounts named by the statement.

- For temporary account locking to occur, password failures must be consecutive. Any successful login that occurs prior to reaching the FAILED\_LOGIN\_ATTEMPTS value for failed logins causes failure counting to reset. For example, if FAILED\_LOGIN\_ATTEMPTS is 4 and three consecutive password failures have occurred, one more failure is necessary for locking to begin. But if the next login succeeds, failed-login counting for the account is reset so that four consecutive failures are again required for locking.
- Once temporary locking begins, successful login cannot occur even with the correct password until either the lock duration has passed or the account is unlocked by one of the account-reset methods listed in the following discussion.

When the server reads the grant tables, it initializes state information for each account regarding whether failed-login tracking is enabled, whether the account is currently temporarily locked and when locking began if so, and the number of failures before temporary locking occurs if the account is not locked.

An account's state information can be reset, which means that failed-login counting is reset, and the account is unlocked if currently temporarily locked. Account resets can be global for all accounts or per account:

- A global reset of all accounts occurs for any of these conditions:
  - A server restart.
  - Execution of FLUSH PRIVILEGES. (Starting the server with --skip-grant-tables causes the grant tables not to be read, which disables failed-login tracking. In this case, the first execution of FLUSH PRIVILEGES causes the server to read the grant tables and enable failed-login tracking, in addition to resetting all accounts.)
- A per-account reset occurs for any of these conditions:
  - Successful login for the account.
  - The lock duration passes. In this case, failed-login counting resets at the time of the next login attempt.
  - Execution of an ALTER USER statement for the account that sets either FAILED\_LOGIN\_ATTEMPTS or PASSWORD\_LOCK\_TIME (or both) to any value (including the current option value), or execution of an ALTER USER ... UNLOCK statement for the account.

Other ALTER USER statements for the account have no effect on its current failed-login count or its locking state.

Failed-login tracking is tied to the login account that is used to check credentials. If user proxying is in use, tracking occurs for the proxy user, not the proxied user. That is, tracking is tied to the account indicated by USER(), not the account indicated by CURRENT\_USER(). For information about the distinction between proxy and proxied users, see [Section 8.2.19, "Proxy Users".](#page-50-0)

# <span id="page-39-0"></span>**8.2.16 Server Handling of Expired Passwords**

MySQL provides password-expiration capability, which enables database administrators to require that users reset their password. Passwords can be expired manually, and on the basis of a policy for automatic expiration (see [Section 8.2.15, "Password Management"\)](#page-28-0).

The ALTER USER statement enables account password expiration. For example:

```
ALTER USER 'myuser'@'localhost' PASSWORD EXPIRE;
```

For each connection that uses an account with an expired password, the server either disconnects the client or restricts the client to "sandbox mode," in which the server permits the client to perform only those operations necessary to reset the expired password. Which action is taken by the server depends on both client and server settings, as discussed later.

If the server disconnects the client, it returns an [ER\\_MUST\\_CHANGE\\_PASSWORD\\_LOGIN](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_must_change_password_login) error:

```
$> mysql -u myuser -p
Password: ******
ERROR 1862 (HY000): Your password has expired. To log in you must
change it using a client that supports expired passwords.
```

If the server restricts the client to sandbox mode, these operations are permitted within the client session:

• The client can reset the account password with ALTER USER or SET PASSWORD. After that has been done, the server restores normal access for the session, as well as for subsequent connections that use the account.

![](_page_40_Picture_5.jpeg)

#### **Note**

Although it is possible to "reset" an expired password by setting it to its current value, it is preferable, as a matter of good policy, to choose a different password. DBAs can enforce non-reuse by establishing an appropriate password-reuse policy. See [Password Reuse Policy.](#page-31-0)

For any operation not permitted within the session, the server returns an [ER\\_MUST\\_CHANGE\\_PASSWORD](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_must_change_password) error:

```
mysql> USE performance_schema;
ERROR 1820 (HY000): You must reset your password using ALTER USER
statement before executing this statement.
mysql> SELECT 1;
ERROR 1820 (HY000): You must reset your password using ALTER USER
statement before executing this statement.
```

That is what normally happens for interactive invocations of the mysql client because by default such invocations are put in sandbox mode. To resume normal functioning, select a new password.

For noninteractive invocations of the mysql client (for example, in batch mode), the server normally disconnects the client if the password is expired. To permit noninteractive mysql invocations to stay connected so that the password can be changed (using the statements permitted in sandbox mode), add the --connect-expired-password option to the mysql command.

As mentioned previously, whether the server disconnects an expired-password client or restricts it to sandbox mode depends on a combination of client and server settings. The following discussion describes the relevant settings and how they interact.

![](_page_40_Picture_13.jpeg)

# **Note**

This discussion applies only for accounts with expired passwords. If a client connects using a nonexpired password, the server handles the client normally.

On the client side, a given client indicates whether it can handle sandbox mode for expired passwords. For clients that use the C client library, there are two ways to do this:

• Pass the MYSQL\_OPT\_CAN\_HANDLE\_EXPIRED\_PASSWORDS flag to [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md) prior to connecting:

```
bool arg = 1;
mysql_options(mysql,
 MYSQL_OPT_CAN_HANDLE_EXPIRED_PASSWORDS,
 &arg);
```

This is the technique used within the mysql client, which enables MYSQL\_OPT\_CAN\_HANDLE\_EXPIRED\_PASSWORDS if invoked interactively or with the --connectexpired-password option.

• Pass the CLIENT\_CAN\_HANDLE\_EXPIRED\_PASSWORDS flag to [mysql\\_real\\_connect\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-real-connect.md) at connect time:

```
MYSQL mysql;
mysql_init(&mysql);
if (!mysql_real_connect(&mysql,
 host, user, password, db,
 port, unix_socket,
 CLIENT_CAN_HANDLE_EXPIRED_PASSWORDS))
{
 ... handle error ...
}
```

Other MySQL Connectors have their own conventions for indicating readiness to handle sandbox mode. See the documentation for the Connector in which you are interested.

On the server side, if a client indicates that it can handle expired passwords, the server puts it in sandbox mode.

If a client does not indicate that it can handle expired passwords (or uses an older version of the client library that cannot so indicate), the server action depends on the value of the disconnect\_on\_expired\_password system variable:

- If disconnect\_on\_expired\_password is enabled (the default), the server disconnects the client with an [ER\\_MUST\\_CHANGE\\_PASSWORD\\_LOGIN](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_must_change_password_login) error.
- If disconnect\_on\_expired\_password is disabled, the server puts the client in sandbox mode.

# <span id="page-41-0"></span>**8.2.17 Pluggable Authentication**

When a client connects to the MySQL server, the server uses the user name provided by the client and the client host to select the appropriate account row from the mysql.user system table. The server then authenticates the client, determining from the account row which authentication plugin applies to the client:

- If the server cannot find the plugin, an error occurs and the connection attempt is rejected.
- Otherwise, the server invokes that plugin to authenticate the user, and the plugin returns a status to the server indicating whether the user provided the correct password and is permitted to connect.

Pluggable authentication enables these important capabilities:

- **Choice of authentication methods.** Pluggable authentication makes it easy for DBAs to choose and change the authentication method used for individual MySQL accounts.
- **External authentication.** Pluggable authentication makes it possible for clients to connect to the MySQL server with credentials appropriate for authentication methods that store credentials elsewhere than in the mysql.user system table. For example, plugins can be created to use external authentication methods such as PAM, Windows login IDs, LDAP, or Kerberos.
- **Proxy users:** If a user is permitted to connect, an authentication plugin can return to the server a user name different from the name of the connecting user, to indicate that the connecting user is a proxy for another user (the proxied user). While the connection lasts, the proxy user is treated, for purposes of access control, as having the privileges of the proxied user. In effect, one user impersonates another. For more information, see [Section 8.2.19, "Proxy Users"](#page-50-0).

![](_page_41_Picture_16.jpeg)

### **Note**

If you start the server with the --skip-grant-tables option, authentication plugins are not used even if loaded because the server performs no client authentication and permits any client to connect. Because this is insecure, if the server is started with the --skip-grant-tables option, it also disables remote connections by enabling skip\_networking.

- [Available Authentication Plugins](#page-42-0)
- [The Default Authentication Plugin](#page-43-0)
- [Authentication Plugin Usage](#page-43-1)
- [Authentication Plugin Client/Server Compatibility](#page-44-0)
- [Authentication Plugin Connector-Writing Considerations](#page-44-1)
- [Restrictions on Pluggable Authentication](#page-45-0)

# <span id="page-42-0"></span>**Available Authentication Plugins**

MySQL 8.4 provides these authentication plugins:

• A plugin that performs native authentication; that is, authentication based on the password hashing method in use from before the introduction of pluggable authentication in MySQL. The mysql\_native\_password plugin implements authentication based on this native password hashing method. See [Section 8.4.1.1, "Native Pluggable Authentication".](#page-93-1)

![](_page_42_Picture_10.jpeg)

#### **Note**

The mysql\_native\_password authentication plugin is deprecated and subject to removal in a future version of MySQL.

- Plugins that perform authentication using SHA-256 password hashing. This is stronger encryption than that available with native authentication. See [Section 8.4.1.2, "Caching SHA-2 Pluggable](#page-94-0) [Authentication",](#page-94-0) and [Section 8.4.1.3, "SHA-256 Pluggable Authentication".](#page-99-0)
- A client-side plugin that sends the password to the server without hashing or encryption. This plugin is used in conjunction with server-side plugins that require access to the password exactly as provided by the client user. See [Section 8.4.1.4, "Client-Side Cleartext Pluggable Authentication".](#page-103-0)
- A plugin that performs external authentication using PAM (Pluggable Authentication Modules), enabling MySQL Server to use PAM to authenticate MySQL users. This plugin supports proxy users as well. See [Section 8.4.1.5, "PAM Pluggable Authentication".](#page-104-0)
- A plugin that performs external authentication on Windows, enabling MySQL Server to use native Windows services to authenticate client connections. Users who have logged in to Windows can connect from MySQL client programs to the server based on the information in their environment without specifying an additional password. This plugin supports proxy users as well. See [Section 8.4.1.6, "Windows Pluggable Authentication".](#page-114-0)
- Plugins that perform authentication using LDAP (Lightweight Directory Access Protocol) to authenticate MySQL users by accessing directory services such as X.500. These plugins support proxy users as well. See [Section 8.4.1.7, "LDAP Pluggable Authentication".](#page-119-0)
- A plugin that performs authentication using Kerberos to authenticate MySQL users that correspond to Kerberos principals. See [Section 8.4.1.8, "Kerberos Pluggable Authentication".](#page-140-0)
- A plugin that prevents all client connections to any account that uses it. Use cases for this plugin include proxied accounts that should never permit direct login but are accessed only through proxy accounts and accounts that must be able to execute stored programs and views with elevated privileges without exposing those privileges to ordinary users. See [Section 8.4.1.9, "No-Login](#page-151-0) [Pluggable Authentication".](#page-151-0)
- A plugin that authenticates clients that connect from the local host through the Unix socket file. See [Section 8.4.1.10, "Socket Peer-Credential Pluggable Authentication"](#page-154-0).
- A plugin that authenticates users to MySQL Server using WebAuthn format with a FIDO/FIDO2 device. See [Section 8.4.1.11, "WebAuthn Pluggable Authentication".](#page-156-0)

• A test plugin that checks account credentials and logs success or failure to the server error log. This plugin is intended for testing and development purposes, and as an example of how to write an authentication plugin. See [Section 8.4.1.12, "Test Pluggable Authentication"](#page-163-0).

![](_page_43_Picture_2.jpeg)

#### **Note**

For information about current restrictions on the use of pluggable authentication, including which connectors support which plugins, see [Restrictions on](#page-45-0) [Pluggable Authentication.](#page-45-0)

Third-party connector developers should read that section to determine the extent to which a connector can take advantage of pluggable authentication capabilities and what steps to take to become more compliant.

If you are interested in writing your own authentication plugins, see [Writing Authentication Plugins.](https://dev.mysql.com/doc/extending-mysql/8.4/en/writing-authentication-plugins.md)

# <span id="page-43-0"></span>**The Default Authentication Plugin**

The CREATE USER and ALTER USER statements have syntax for specifying how an account authenticates. Some forms of this syntax do not explicitly name an authentication plugin (there is no IDENTIFIED WITH clause). For example:

```
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
```

In such cases, the server assigns the default authentication plugin to the account. MySQL 8.4 supports multifactor authentication and up to three clauses that specify how an account authenticates. The rules that determine the default authentication plugin for authentication methods that name no plugin are factor-specific:

• Factor 1: If authentication\_policy element 1 names an authentication plugin, that plugin is the default. If authentication\_policy element 1 is \*, caching\_sha2\_password is the default.

Given the rules above, the following statement creates a two-factor authentication account, with the first factor authentication method determined by authentication\_policy, as shown here:

```
CREATE USER 'wei'@'localhost' IDENTIFIED BY 'password'
 AND IDENTIFIED WITH authentication_ldap_simple;
```

In the same way, this example creates a three-factor authentication account:

```
CREATE USER 'mateo'@'localhost' IDENTIFIED BY 'password'
 AND IDENTIFIED WITH authentication_ldap_simple
 AND IDENTIFIED WITH authentication_fido;
```

You can use SHOW CREATE USER to view the applied authentication methods.

• Factor 2 or 3: If the corresponding authentication\_policy element names an authentication plugin, that plugin is the default. If the authentication\_policy element is \* or empty, there is no default; attempting to define an account authentication method for the factor without naming a plugin is an error, as in the following examples:

```
mysql> CREATE USER 'sofia'@'localhost' IDENTIFIED WITH authentication_ldap_simple
 AND IDENTIFIED BY 'abc';
ERROR 1524 (HY000): Plugin '' is not loaded
mysql> CREATE USER 'sofia'@'localhost' IDENTIFIED WITH authentication_ldap_simple
 AND IDENTIFIED BY 'abc';
ERROR 1524 (HY000): Plugin '*' is not loaded
```

# <span id="page-43-1"></span>**Authentication Plugin Usage**

This section provides general instructions for installing and using authentication plugins. For instructions specific to a given plugin, see the section that describes that plugin under [Section 8.4.1,](#page-93-0) ["Authentication Plugins".](#page-93-0)

In general, pluggable authentication uses a pair of corresponding plugins on the server and client sides, so you use a given authentication method like this:

- If necessary, install the plugin library or libraries containing the appropriate plugins. On the server host, install the library containing the server-side plugin, so that the server can use it to authenticate client connections. Similarly, on each client host, install the library containing the client-side plugin for use by client programs. Authentication plugins that are built in need not be installed.
- For each MySQL account that you create, specify the appropriate server-side plugin to use for authentication. If the account is to use the default authentication plugin, the account-creation statement need not specify the plugin explicitly. The server assigns the default authentication plugin, determined as described in [The Default Authentication Plugin](#page-43-0).
- When a client connects, the server-side plugin tells the client program which client-side plugin to use for authentication.

In the case that an account uses an authentication method that is the default for both the server and the client program, the server need not communicate to the client which client-side plugin to use, and a round trip in client/server negotiation can be avoided.

For standard MySQL clients such as mysql and mysqladmin, the --default-auth=plugin\_name option can be specified on the command line as a hint about which client-side plugin the program can expect to use, although the server overrides this if the server-side plugin associated with the user account requires a different client-side plugin.

If the client program does not find the client-side plugin library file, specify a --plugindir=dir\_name option to indicate the plugin library directory location.

# <span id="page-44-0"></span>**Authentication Plugin Client/Server Compatibility**

Pluggable authentication enables flexibility in the choice of authentication methods for MySQL accounts, but in some cases client connections cannot be established due to authentication plugin incompatibility between the client and server.

The general compatibility principle for a successful client connection to a given account on a given server is that the client and server both must support the authentication method required by the account. Because authentication methods are implemented by authentication plugins, the client and server both must support the authentication plugin required by the account.

Authentication plugin incompatibilities can arise in various ways. Examples:

- Connect using a MySQL 5.7 client from 5.7.22 or lower to a MySQL 8.4 server account that authenticates with caching\_sha2\_password. This fails because the 5.7 client does not recognize the plugin. (This issue is addressed in MySQL 5.7 as of 5.7.23, when caching\_sha2\_password client-side support was added to the MySQL client library and client programs.)
- Connect using a MySQL 5.7 client to a pre-5.7 server account that authenticates with mysql\_old\_password. This fails for multiple reasons. First, such a connection requires - secure-auth=0, which is no longer a supported option. Even were it supported, the 5.7 client does not recognize the plugin because it was removed in MySQL 5.7.
- Connect using a MySQL 5.7 client from a Community distribution to a MySQL 5.7 Enterprise server account that authenticates using one of the Enterprise-only LDAP authentication plugins. This fails because the Community client does not have access to the Enterprise plugin.

In general, these compatibility issues do not arise when connections are made between a client and server from the same MySQL distribution. When connections are made between a client and server from different MySQL series, issues can arise. These issues are inherent in the development process when MySQL introduces new authentication plugins or removes old ones. To minimize the potential for incompatibilities, regularly upgrade the server, clients, and connectors on a timely basis.

# <span id="page-44-1"></span>**Authentication Plugin Connector-Writing Considerations**

Various implementations of the MySQL client/server protocol exist. The libmysqlclient C API client library is one implementation. Some MySQL connectors (typically those not written in C) provide their own implementation. However, not all protocol implementations handle plugin authentication the same way. This section describes an authentication issue that protocol implementors should take into account.

In the client/server protocol, the server tells connecting clients which authentication plugin it considers the default. If the protocol implementation used by the client tries to load the default plugin and that plugin does not exist on the client side, the load operation fails. This is an unnecessary failure if the default plugin is not the plugin actually required by the account to which the client is trying to connect.

If a client/server protocol implementation does not have its own notion of default authentication plugin and always tries to load the default plugin specified by the server, it fails with an error if that plugin is not available.

To avoid this problem, the protocol implementation used by the client should have its own default plugin and should use it as its first choice (or, alternatively, fall back to this default in case of failure to load the default plugin specified by the server). Example:

- In MySQL 5.7, libmysqlclient uses as its default choice either mysql\_native\_password or the plugin specified through the MYSQL\_DEFAULT\_AUTH option for [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options.md).
- When a 5.7 client tries to connect to an 8.4 server, the server specifies caching\_sha2\_password as its default authentication plugin, but the client still sends credential details per either mysql\_native\_password or whatever is specified through MYSQL\_DEFAULT\_AUTH.
- The only time the client loads the plugin specified by the server is for a change-plugin request, but in that case it can be any plugin depending on the user account. In this case, the client must try to load the plugin, and if that plugin is not available, an error is not optional.

# <span id="page-45-0"></span>**Restrictions on Pluggable Authentication**

The first part of this section describes general restrictions on the applicability of the pluggable authentication framework described at [Section 8.2.17, "Pluggable Authentication".](#page-41-0) The second part describes how third-party connector developers can determine the extent to which a connector can take advantage of pluggable authentication capabilities and what steps to take to become more compliant.

The term "native authentication" used here refers to authentication against passwords stored in the mysql.user system table. This is the same authentication method provided by older MySQL servers, before pluggable authentication was implemented. "Windows native authentication" refers to authentication using the credentials of a user who has already logged in to Windows, as implemented by the Windows Native Authentication plugin ("Windows plugin" for short).

- [General Pluggable Authentication Restrictions](#page-45-1)
- [Pluggable Authentication and Third-Party Connectors](#page-46-0)

### <span id="page-45-1"></span>**General Pluggable Authentication Restrictions**

• **Connector/C++:** Clients that use this connector can connect to the server only through accounts that use native authentication.

Exception: A connector supports pluggable authentication if it was built to link to libmysqlclient dynamically (rather than statically) and it loads the current version of libmysqlclient if that version is installed, or if the connector is recompiled from source to link against the current libmysqlclient.

For information about writing connectors to handle information from the server about the default server-side authentication plugin, see [Authentication Plugin Connector-Writing Considerations](#page-44-1).

- **Connector/NET:** Clients that use Connector/NET can connect to the server through accounts that use native authentication or Windows native authentication.
- **Connector/PHP:** Clients that use this connector can connect to the server only through accounts that use native authentication, when compiled using the MySQL native driver for PHP (mysqlnd).
- **Windows native authentication:** Connecting through an account that uses the Windows plugin requires Windows Domain setup. Without it, NTLM authentication is used and then only local connections are possible; that is, the client and server must run on the same computer.
- **Proxy users:** Proxy user support is available to the extent that clients can connect through accounts authenticated with plugins that implement proxy user capability (that is, plugins that can return a user name different from that of the connecting user). For example, the PAM and Windows plugins support proxy users. The mysql\_native\_password (deprecated) and sha256\_password (deprecated) authentication plugins do not support proxy users by default, but can be configured to do so; see [Server Support for Proxy User Mapping.](#page-56-0)
- **Replication**: Replicas can not only employ replication user accounts using native authentication, but can also connect through replication user accounts that use nonnative authentication if the required client-side plugin is available. If the plugin is built into libmysqlclient, it is available by default. Otherwise, the plugin must be installed on the replica side in the directory named by the replica's plugin\_dir system variable.
- **FEDERATED tables:** A FEDERATED table can access the remote table only through accounts on the remote server that use native authentication.

# <span id="page-46-0"></span>**Pluggable Authentication and Third-Party Connectors**

Third-party connector developers can use the following guidelines to determine readiness of a connector to take advantage of pluggable authentication capabilities and what steps to take to become more compliant:

• An existing connector to which no changes have been made uses native authentication and clients that use the connector can connect to the server only through accounts that use native authentication. However, you should test the connector against a recent version of the server to verify that such connections still work without problem.

Exception: A connector might work with pluggable authentication without any changes if it links to libmysqlclient dynamically (rather than statically) and it loads the current version of libmysqlclient if that version is installed.

• To take advantage of pluggable authentication capabilities, a connector that is libmysqlclientbased should be relinked against the current version of libmysqlclient. This enables the connector to support connections though accounts that require client-side plugins now built into libmysqlclient (such as the cleartext plugin needed for PAM authentication and the Windows plugin needed for Windows native authentication). Linking with a current libmysqlclient also enables the connector to access client-side plugins installed in the default MySQL plugin directory (typically the directory named by the default value of the local server's plugin\_dir system variable).

If a connector links to libmysqlclient dynamically, it must be ensured that the newer version of libmysqlclient is installed on the client host and that the connector loads it at runtime.

- Another way for a connector to support a given authentication method is to implement it directly in the client/server protocol. Connector/NET uses this approach to provide support for Windows native authentication.
- If a connector should be able to load client-side plugins from a directory different from the default plugin directory, it must implement some means for client users to specify the directory. Possibilities for this include a command-line option or environment variable from which the connector can obtain

the directory name. Standard MySQL client programs such as mysql and mysqladmin implement a --plugin-dir option. See also [C API Client Plugin Interface.](https://dev.mysql.com/doc/c-api/8.4/en/c-api-plugin-interface.md)

• Proxy user support by a connector depends, as described earlier in this section, on whether the authentication methods that it supports permit proxy users.

# <span id="page-47-1"></span>**8.2.18 Multifactor Authentication**

Authentication involves one party establishing its identity to the satisfaction of a second party. Multifactor authentication (MFA) is the use of multiple authentication values (or "factors") during the authentication process. MFA provides greater security than one-factor/single-factor authentication (1FA/SFA), which uses only one authentication method such as a password. MFA enables additional authentication methods, such as authentication using multiple passwords, or authentication using devices like smart cards, security keys, and biometric readers.

MySQL includes support for multifactor authentication. This capability includes forms of MFA that require up to three authentication values. That is, MySQL account management supports accounts that use 2FA or 3FA, in addition to the existing 1FA support.

When a client attempts a connection to the MySQL server using a single-factor account, the server invokes the authentication plugin indicated by the account definition and accepts or rejects the connection depending on whether the plugin reports success or failure.

For an account that has multiple authentication factors, the process is similar. The server invokes authentication plugins in the order listed in the account definition. If a plugin reports success, the server either accepts the connection if the plugin is the last one, or proceeds to invoke the next plugin if any remain. If any plugin reports failure, the server rejects the connection.

The following sections cover multifactor authentication in MySQL in more detail.

- [Elements of Multifactor Authentication Support](#page-47-0)
- [Configuring the Multifactor Authentication Policy](#page-48-0)
- [Getting Started with Multifactor Authentication](#page-49-0)

# <span id="page-47-0"></span>**Elements of Multifactor Authentication Support**

Authentication factors commonly include these types of information:

- Something you know, such as a secret password or passphrase.
- Something you have, such as a security key or smart card.
- Something you are; that is, a biometric characteristic such as a fingerprint or facial scan.

The "something you know" factor type relies on information that is kept secret on both sides of the authentication process. Unfortunately, secrets may be subject to compromise: Someone might see you enter your password or fool you with a phishing attack, a password stored on the server side might be exposed by a security breach, and so forth. Security can be improved by using multiple passwords, but each may still be subject to compromise. Use of the other factor types enables improved security with less risk of compromise.

Implementation of multifactor authentication in MySQL comprises these elements:

- The authentication\_policy system variable controls how many authentication factors can be used and the types of authentication permitted for each factor. That is, it places constraints on CREATE USER and ALTER USER statements with respect to multifactor authentication.
- CREATE USER and ALTER USER have syntax enabling multiple authentication methods to be specified for new accounts, and for adding, modifying, or dropping authentication methods for existing accounts. If an account uses 2FA or 3FA, the mysql.user system table stores information about the additional authentication factors in the User\_attributes column.

- To enable authentication to the MySQL server using accounts that require multiple passwords, client programs have --password1, --password2, and --password3 options that permit up to three passwords to be specified. For applications that use the C API, the MYSQL\_OPT\_USER\_PASSWORD option for the [mysql\\_options4\(\)](https://dev.mysql.com/doc/c-api/8.4/en/mysql-options4.md) C API function enables the same capability.
- The server-side authentication\_webauthn plugin enables authentication using devices. This server-side, device-based authentication plugin is included only in MySQL Enterprise Edition distributions. It is not included in MySQL community distributions. However, the clientside authentication\_webauthn\_client plugin is included in all distributions, including community distributions. This enables clients from any distribution to connect to accounts that use authentication\_webauthn to authenticate on a server that has that plugin loaded. See [Section 8.4.1.11, "WebAuthn Pluggable Authentication".](#page-156-0)
- authentication\_webauthn also enables passwordless authentication, if it is the only authentication plugin used by an account. See [WebAuthn Passwordless Authentication.](#page-161-0)
- Multifactor authentication can use non-WebAuthn MySQL authentication methods, the WebAuthn authentication method, or a combination of both.
- These privileges enable users to perform certain restricted multifactor authentication-related operations:
  - A user who has the AUTHENTICATION\_POLICY\_ADMIN privilege is not subject to the constraints imposed by the authentication\_policy system variable. (A warning does occur for statements that otherwise would not be permitted.)
  - The PASSWORDLESS\_USER\_ADMIN privilege enables creation of passwordless-authentication accounts and replication of operations on them.

# <span id="page-48-0"></span>**Configuring the Multifactor Authentication Policy**

The authentication\_policy system variable defines the multifactor authentication policy. Specifically, it defines how many authentication factors accounts may have (or are required to have) and the authentication methods that can be used for each factor.

The value of authentication\_policy is a list of 1, 2, or 3 comma-separated elements. Each element in the list corresponds to an authentication factor and can be an authentication plugin name, an asterisk (\*), empty, or missing. (Exception: Element 1 cannot be empty or missing.) The entire list is enclosed in single quotes. For example, the following authentication\_policy value includes an asterisk, an authentication plugin name, and an empty element:

```
authentication_policy = '*,authentication_webauthn,'
```

An asterisk (\*) indicates that an authentication method is required but any method is permitted. An empty element indicates that an authentication method is optional and any method is permitted. A missing element (no asterisk, empty element, or authentication plugin name) indicates that an authentication method is not permitted. When a plugin name is specified, that authentication method is required for the respective factor when creating or modifying an account.

The default authentication\_policy value is '\*,,' (an asterisk and two empty elements), which requires a first factor, and optionally permits second and third factors. The default authentication\_policy value is thus backward compatible with existing 1FA accounts, but also permits creation or modification of accounts to use 2FA or 3FA.

A user who has the AUTHENTICATION\_POLICY\_ADMIN privilege is not subject to the constraints imposed by the authentication\_policy setting. (A warning occurs for statements that otherwise would not be permitted.)

authentication\_policy values can be defined in an option file or specified using a SET GLOBAL statement:

```
SET GLOBAL authentication_policy='*,*,';
```

There are several rules that govern how the authentication\_policy value can be defined. Refer to the authentication\_policy system variable description for a compete account of those rules. The following table provides several authentication\_policy example values and the policy established by each.

**Table 8.11 Example authentication\_policy Values**

| authentication_policy Value           | Effective Policy                                                                                                                                                         |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| '*'                                   | Permit only creating or altering accounts with one<br>factor.                                                                                                            |
| '*,*'                                 | Permit only creating or altering accounts with two<br>factors.                                                                                                           |
| '*,*,*'                               | Permit only creating or altering accounts with<br>three factors.                                                                                                         |
| '*,'                                  | Permit creating or altering accounts with one or<br>two factors.                                                                                                         |
| '*,,'                                 | Permit creating or altering accounts with one, two,<br>or three factors.                                                                                                 |
| '*,*,'                                | Permit creating or altering accounts with two or<br>three factors.                                                                                                       |
| '*,auth_plugin'                       | Permit creating or altering accounts with two<br>factors, where the first factor can be any<br>authentication method, and the second factor<br>must be the named plugin. |
| 'auth_plugin,*,'                      | Permit creating or altering accounts with two or<br>three factors, where the first factor must be the<br>named plugin.                                                   |
| 'auth_plugin,'                        | Permit creating or altering accounts with one or<br>two factors, where the first factor must be the<br>named plugin.                                                     |
| 'auth_plugin,auth_plugin,auth_plugin' | Permits creating or altering accounts with three<br>factors, where the factors must use the named<br>plugins.                                                            |

# <span id="page-49-0"></span>**Getting Started with Multifactor Authentication**

By default, MySQL uses a multifactor authentication policy that permits any authentication plugin for the first factor, and optionally permits second and third authentication factors. This policy is configurable; for details, see [Configuring the Multifactor Authentication Policy](#page-48-0).

![](_page_49_Picture_6.jpeg)

### **Note**

It is not permitted to use any internal credential storage plugins (caching\_sha2\_password or mysql\_native\_password) for factor 2 or 3.

Suppose that you want an account to authenticate first using the caching\_sha2\_password plugin, then using the authentication\_ldap\_sasl SASL LDAP plugin. (This assumes that LDAP authentication is already set up as described in [Section 8.4.1.7, "LDAP Pluggable Authentication"](#page-119-0), and that the user has an entry in the LDAP directory corresponding to the authentication string shown in the example.) Create the account using a statement like this:

```
CREATE USER 'alice'@'localhost'
 IDENTIFIED WITH caching_sha2_password
 BY 'sha2_password'
 AND IDENTIFIED WITH authentication_ldap_sasl
 AS 'uid=u1_ldap,ou=People,dc=example,dc=com';
```

To connect, the user must supply two passwords. To enable authentication to the MySQL server using accounts that require multiple passwords, client programs have --password1, --password2, and --password3 options that permit up to three passwords to be specified. These options are similar to the --password option in that they can take a password value following the option on the command line (which is insecure) or if given without a password value cause the user to be prompted for one. For the account just created, factors 1 and 2 take passwords, so invoke the mysql client with the - password1 and --password2 options. mysql prompts for each password in turn:

```
$> mysql --user=alice --password1 --password2
Enter password: (enter factor 1 password)
Enter password: (enter factor 2 password)
```

Suppose you want to add a third authentication factor. This can be achieved by dropping and recreating the user with a third factor or by using ALTER USER user ADD factor syntax. Both methods are shown below:

```
DROP USER 'alice'@'localhost';
CREATE USER 'alice'@'localhost'
 IDENTIFIED WITH caching_sha2_password
 BY 'sha2_password'
 AND IDENTIFIED WITH authentication_ldap_sasl
 AS 'uid=u1_ldap,ou=People,dc=example,dc=com'
 AND IDENTIFIED WITH authentication_webauthn;
```

ADD factor syntax includes the factor number and FACTOR keyword:

```
ALTER USER 'alice'@'localhost' ADD 3 FACTOR IDENTIFIED WITH authentication_webauthn;
```

ALTER USER user DROP factor syntax permits dropping a factor. The following example drops the third factor (authentication\_webauthn) that was added in the previous example:

```
ALTER USER 'alice'@'localhost' DROP 3 FACTOR;
```

ALTER USER user MODIFY factor syntax permits changing the plugin or authentication string for a particular factor, provided that the factor exists. The following example modifies the second factor, changing the authentication method from authentication\_ldap\_sasl to authetication\_webauthn:

```
ALTER USER 'alice'@'localhost' MODIFY 2 FACTOR IDENTIFIED WITH authentication_webauthn;
```

Use SHOW CREATE USER to view the authentication methods defined for an account:

```
SHOW CREATE USER 'u1'@'localhost'\G
*************************** 1. row ***************************
CREATE USER for u1@localhost: CREATE USER `u1`@`localhost` 
IDENTIFIED WITH 'caching_sha2_password' AS 'sha2_password' 
AND IDENTIFIED WITH 'authentication_authn' REQUIRE NONE 
PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK PASSWORD HISTORY 
DEFAULT PASSWORD REUSE INTERVAL DEFAULT PASSWORD REQUIRE 
CURRENT DEFAULT
```

# <span id="page-50-0"></span>**8.2.19 Proxy Users**

The MySQL server authenticates client connections using authentication plugins. The plugin that authenticates a given connection may request that the connecting (external) user be treated as a different user for privilege-checking purposes. This enables the external user to be a proxy for the second user; that is, to assume the privileges of the second user:

- The external user is a "proxy user" (a user who can impersonate or become known as another user).
- The second user is a "proxied user" (a user whose identity and privileges can be assumed by a proxy user).

This section describes how the proxy user capability works. For general information about authentication plugins, see [Section 8.2.17, "Pluggable Authentication".](#page-41-0) For information about specific plugins, see [Section 8.4.1, "Authentication Plugins".](#page-93-0) For information about writing authentication plugins that support proxy users, see [Implementing Proxy User Support in Authentication Plugins.](https://dev.mysql.com/doc/extending-mysql/8.4/en/writing-authentication-plugins-proxy-users.md)

- [Requirements for Proxy User Support](#page-51-0)
- [Simple Proxy User Example](#page-52-0)
- [Preventing Direct Login to Proxied Accounts](#page-53-0)
- [Granting and Revoking the PROXY Privilege](#page-53-1)
- [Default Proxy Users](#page-54-0)
- [Default Proxy User and Anonymous User Conflicts](#page-55-0)
- [Server Support for Proxy User Mapping](#page-56-0)
- [Proxy User System Variables](#page-57-0)

![](_page_51_Picture_10.jpeg)

#### **Note**

One administrative benefit to be gained by proxying is that the DBA can set up a single account with a set of privileges and then enable multiple proxy users to have those privileges without having to assign the privileges individually to each of those users. As an alternative to proxy users, DBAs may find that roles provide a suitable way to map users onto specific sets of named privileges. Each user can be granted a given single role to, in effect, be granted the appropriate set of privileges. See [Section 8.2.10, "Using Roles"](#page-10-0).

# <span id="page-51-0"></span>**Requirements for Proxy User Support**

For proxying to occur for a given authentication plugin, these conditions must be satisfied:

- Proxying must be supported, either by the plugin itself, or by the MySQL server on behalf of the plugin. In the latter case, server support may need to be enabled explicitly; see [Server Support for](#page-56-0) [Proxy User Mapping.](#page-56-0)
- The account for the external proxy user must be set up to be authenticated by the plugin. Use the CREATE USER statement to associate an account with an authentication plugin, or ALTER USER to change its plugin.
- The account for the proxied user must exist and be granted the privileges to be assumed by the proxy user. Use the CREATE USER and GRANT statements for this.
- Normally, the proxied user is configured so that it can be used only in proxying scenarios and not for direct logins.
- The proxy user account must have the PROXY privilege for the proxied account. Use the GRANT statement for this.
- For a client connecting to the proxy account to be treated as a proxy user, the authentication plugin must return a user name different from the client user name, to indicate the user name of the proxied account that defines the privileges to be assumed by the proxy user.

Alternatively, for plugins that are provided proxy mapping by the server, the proxied user is determined from the PROXY privilege held by the proxy user.

The proxy mechanism permits mapping only the external client user name to the proxied user name. There is no provision for mapping host names:

• When a client connects to the server, the server determines the proper account based on the user name passed by the client program and the host from which the client connects.

• If that account is a proxy account, the server attempts to determine the appropriate proxied account by finding a match for a proxied account using the user name returned by the authentication plugin and the host name of the proxy account. The host name in the proxied account is ignored.

# <span id="page-52-0"></span>**Simple Proxy User Example**

Consider the following account definitions:

```
-- create proxy account
CREATE USER 'employee_ext'@'localhost'
 IDENTIFIED WITH my_auth_plugin
 AS 'my_auth_string';
-- create proxied account and grant its privileges;
-- use mysql_no_login plugin to prevent direct login
CREATE USER 'employee'@'localhost'
 IDENTIFIED WITH mysql_no_login;
GRANT ALL
 ON employees.*
 TO 'employee'@'localhost';
-- grant to proxy account the
-- PROXY privilege for proxied account
GRANT PROXY
 ON 'employee'@'localhost'
 TO 'employee_ext'@'localhost';
```

When a client connects as employee\_ext from the local host, MySQL uses the plugin named my\_auth\_plugin to perform authentication. Suppose that my\_auth\_plugin returns a user name of employee to the server, based on the content of 'my\_auth\_string' and perhaps by consulting some external authentication system. The name employee differs from employee\_ext, so returning employee serves as a request to the server to treat the employee\_ext external user, for purposes of privilege checking, as the employee local user.

In this case, employee\_ext is the proxy user and employee is the proxied user.

The server verifies that proxy authentication for employee is possible for the employee\_ext user by checking whether employee\_ext (the proxy user) has the PROXY privilege for employee (the proxied user). If this privilege has not been granted, an error occurs. Otherwise, employee\_ext assumes the privileges of employee. The server checks statements executed during the client session by employee\_ext against the privileges granted to employee. In this case, employee\_ext can access tables in the employees database.

The proxied account, employee, uses the mysql\_no\_login authentication plugin to prevent clients from using the account to log in directly. (This assumes that the plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication".](#page-151-0)) For alternative methods of protecting proxied accounts against direct use, see [Preventing Direct Login to Proxied Accounts](#page-53-0).

When proxying occurs, the USER() and CURRENT\_USER() functions can be used to see the difference between the connecting user (the proxy user) and the account whose privileges apply during the current session (the proxied user). For the example just described, those functions return these values:

```
mysql> SELECT USER(), CURRENT_USER();
+------------------------+--------------------+
| USER() | CURRENT_USER() |
+------------------------+--------------------+
| employee_ext@localhost | employee@localhost |
+------------------------+--------------------+
```

In the CREATE USER statement that creates the proxy user account, the IDENTIFIED WITH clause that names the proxy-supporting authentication plugin is optionally followed by an AS 'auth\_string' clause specifying a string that the server passes to the plugin when the user connects. If present, the string provides information that helps the plugin determine how to map the proxy (external) client user name to a proxied user name. It is up to each plugin whether it requires the AS clause. If so, the format of the authentication string depends on how the plugin intends to use it.

Consult the documentation for a given plugin for information about the authentication string values it accepts.

# <span id="page-53-0"></span>**Preventing Direct Login to Proxied Accounts**

Proxied accounts generally are intended to be used only by means of proxy accounts. That is, clients connect using a proxy account, then are mapped onto and assume the privileges of the appropriate proxied user.

There are multiple ways to ensure that a proxied account cannot be used directly:

- Associate the account with the mysql\_no\_login authentication plugin. In this case, the account cannot be used for direct logins under any circumstances. This assumes that the plugin is installed. For instructions, see [Section 8.4.1.9, "No-Login Pluggable Authentication".](#page-151-0)
- Include the ACCOUNT LOCK option when you create the account. See Section 15.7.1.3, "CREATE USER Statement". With this method, also include a password so that if the account is unlocked later, it cannot be accessed with no password. (If the validate\_password component is enabled, creating an account without a password is not permitted, even if the account is locked. See [Section 8.4.3, "The Password Validation Component".](#page-192-0))
- Create the account with a password but do not tell anyone else the password. If you do not let anyone know the password for the account, clients cannot use it to connect directly to the MySQL server.

# <span id="page-53-1"></span>**Granting and Revoking the PROXY Privilege**

The PROXY privilege is needed to enable an external user to connect as and have the privileges of another user. To grant this privilege, use the GRANT statement. For example:

```
GRANT PROXY ON 'proxied_user' TO 'proxy_user';
```

The statement creates a row in the mysql.proxies\_priv grant table.

At connect time, proxy\_user must represent a valid externally authenticated MySQL user, and proxied\_user must represent a valid locally authenticated user. Otherwise, the connection attempt fails.

The corresponding REVOKE syntax is:

```
REVOKE PROXY ON 'proxied_user' FROM 'proxy_user';
```

MySQL GRANT and REVOKE syntax extensions work as usual. Examples:

```
-- grant PROXY to multiple accounts
GRANT PROXY ON 'a' TO 'b', 'c', 'd';
-- revoke PROXY from multiple accounts
REVOKE PROXY ON 'a' FROM 'b', 'c', 'd';
-- grant PROXY to an account and enable the account to grant
-- PROXY to the proxied account
GRANT PROXY ON 'a' TO 'd' WITH GRANT OPTION;
-- grant PROXY to default proxy account
GRANT PROXY ON 'a' TO ''@'';
```

The PROXY privilege can be granted in these cases:

- By a user that has GRANT PROXY ... WITH GRANT OPTION for proxied\_user.
- By proxied\_user for itself: The value of USER() must exactly match CURRENT\_USER() and proxied\_user, for both the user name and host name parts of the account name.

The initial root account created during MySQL installation has the PROXY ... WITH GRANT OPTION privilege for ''@'', that is, for all users and all hosts. This enables root to set up proxy users, as well as to delegate to other accounts the authority to set up proxy users. For example, root can do this:

```
CREATE USER 'admin'@'localhost'
 IDENTIFIED BY 'admin_password';
GRANT PROXY
 ON ''@''
 TO 'admin'@'localhost'
 WITH GRANT OPTION;
```

Those statements create an admin user that can manage all GRANT PROXY mappings. For example, admin can do this:

```
GRANT PROXY ON sally TO joe;
```

# <span id="page-54-0"></span>**Default Proxy Users**

To specify that some or all users should connect using a given authentication plugin, create a "blank" MySQL account with an empty user name and host name (''@''), associate it with that plugin, and let the plugin return the real authenticated user name (if different from the blank user). Suppose that there exists a plugin named ldap\_auth that implements LDAP authentication and maps connecting users onto either a developer or manager account. To set up proxying of users onto these accounts, use the following statements:

```
-- create default proxy account
CREATE USER ''@''
 IDENTIFIED WITH ldap_auth
 AS 'O=Oracle, OU=MySQL';
-- create proxied accounts; use
-- mysql_no_login plugin to prevent direct login
CREATE USER 'developer'@'localhost'
 IDENTIFIED WITH mysql_no_login;
CREATE USER 'manager'@'localhost'
 IDENTIFIED WITH mysql_no_login;
-- grant to default proxy account the
-- PROXY privilege for proxied accounts
GRANT PROXY
 ON 'manager'@'localhost'
 TO ''@'';
GRANT PROXY
 ON 'developer'@'localhost'
 TO ''@'';
```

Now assume that a client connects as follows:

```
$> mysql --user=myuser --password ...
Enter password: myuser_password
```

The server does not find myuser defined as a MySQL user, but because there is a blank user account (''@'') that matches the client user name and host name, the server authenticates the client against that account. The server invokes the ldap\_auth authentication plugin and passes myuser and myuser\_password to it as the user name and password.

If the ldap\_auth plugin finds in the LDAP directory that myuser\_password is not the correct password for myuser, authentication fails and the server rejects the connection.

If the password is correct and ldap\_auth finds that myuser is a developer, it returns the user name developer to the MySQL server, rather than myuser. Returning a user name different from the client user name of myuser signals to the server that it should treat myuser as a proxy. The server verifies that ''@'' can authenticate as developer (because ''@'' has the PROXY privilege to do so) and accepts the connection. The session proceeds with myuser having the privileges of the developer

proxied user. (These privileges should be set up by the DBA using GRANT statements, not shown.) The USER() and CURRENT\_USER() functions return these values:

```
mysql> SELECT USER(), CURRENT_USER();
+------------------+---------------------+
| USER() | CURRENT_USER() |
+------------------+---------------------+
| myuser@localhost | developer@localhost |
+------------------+---------------------+
```

If the plugin instead finds in the LDAP directory that myuser is a manager, it returns manager as the user name and the session proceeds with myuser having the privileges of the manager proxied user.

```
mysql> SELECT USER(), CURRENT_USER();
+------------------+-------------------+
| USER() | CURRENT_USER() |
+------------------+-------------------+
| myuser@localhost | manager@localhost |
+------------------+-------------------+
```

For simplicity, external authentication cannot be multilevel: Neither the credentials for developer nor those for manager are taken into account in the preceding example. However, they are still used if a client tries to connect and authenticate directly as the developer or manager account, which is why those proxied accounts should be protected against direct login (see [Preventing Direct Login to Proxied](#page-53-0) [Accounts](#page-53-0)).

# <span id="page-55-0"></span>**Default Proxy User and Anonymous User Conflicts**

If you intend to create a default proxy user, check for other existing "match any user" accounts that take precedence over the default proxy user because they can prevent that user from working as intended.

In the preceding discussion, the default proxy user account has '' in the host part, which matches any host. If you set up a default proxy user, take care to also check whether nonproxy accounts exist with the same user part and '%' in the host part, because '%' also matches any host, but has precedence over '' by the rules that the server uses to sort account rows internally (see [Section 8.2.6, "Access](#page-2-0) [Control, Stage 1: Connection Verification"\)](#page-2-0).

Suppose that a MySQL installation includes these two accounts:

```
-- create default proxy account
CREATE USER ''@''
 IDENTIFIED WITH some_plugin
 AS 'some_auth_string';
-- create anonymous account
CREATE USER ''@'%'
 IDENTIFIED BY 'anon_user_password';
```

The first account (''@'') is intended as the default proxy user, used to authenticate connections for users who do not otherwise match a more-specific account. The second account (''@'%') is an anonymous-user account, which might have been created, for example, to enable users without their own account to connect anonymously.

Both accounts have the same user part (''), which matches any user. And each account has a host part that matches any host. Nevertheless, there is a priority in account matching for connection attempts because the matching rules sort a host of '%' ahead of ''. For accounts that do not match any more-specific account, the server attempts to authenticate them against ''@'%' (the anonymous user) rather than ''@'' (the default proxy user). As a result, the default proxy account is never used.

To avoid this problem, use one of the following strategies:

- Remove the anonymous account so that it does not conflict with the default proxy user.
- Use a more-specific default proxy user that matches ahead of the anonymous user. For example, to permit only localhost proxy connections, use ''@'localhost':

```
CREATE USER ''@'localhost'
 IDENTIFIED WITH some_plugin
 AS 'some_auth_string';
```

In addition, modify any GRANT PROXY statements to name ''@'localhost' rather than ''@'' as the proxy user.

Be aware that this strategy prevents anonymous-user connections from localhost.

- Use a named default account rather than an anonymous default account. For an example of this technique, consult the instructions for using the authentication\_windows plugin. See [Section 8.4.1.6, "Windows Pluggable Authentication".](#page-114-0)
- Create multiple proxy users, one for local connections and one for "everything else" (remote connections). This can be useful particularly when local users should have different privileges from remote users.

#### Create the proxy users:

```
-- create proxy user for local connections
CREATE USER ''@'localhost'
 IDENTIFIED WITH some_plugin
 AS 'some_auth_string';
-- create proxy user for remote connections
CREATE USER ''@'%'
 IDENTIFIED WITH some_plugin
 AS 'some_auth_string';
```

#### Create the proxied users:

```
-- create proxied user for local connections
CREATE USER 'developer'@'localhost'
 IDENTIFIED WITH mysql_no_login;
-- create proxied user for remote connections
CREATE USER 'developer'@'%'
 IDENTIFIED WITH mysql_no_login;
```

Grant to each proxy account the PROXY privilege for the corresponding proxied account:

```
GRANT PROXY
 ON 'developer'@'localhost'
 TO ''@'localhost';
GRANT PROXY
 ON 'developer'@'%'
 TO ''@'%';
```

Finally, grant appropriate privileges to the local and remote proxied users (not shown).

Assume that the some\_plugin/'some\_auth\_string' combination causes some\_plugin to map the client user name to developer. Local connections match the ''@'localhost' proxy user, which maps to the 'developer'@'localhost' proxied user. Remote connections match the ''@'%' proxy user, which maps to the 'developer'@'%' proxied user.

# <span id="page-56-0"></span>**Server Support for Proxy User Mapping**

Some authentication plugins implement proxy user mapping for themselves (for example, the PAM and Windows authentication plugins). Other authentication plugins do not support proxy users by default. Of these, some can request that the MySQL server itself map proxy users according to granted proxy privileges: mysql\_native\_password (deprecated), sha256\_password (deprecated). If the check\_proxy\_users system variable is enabled, the server performs proxy user mapping for any authentication plugins that make such a request:

• By default, check\_proxy\_users is disabled, so the server performs no proxy user mapping even for authentication plugins that request server support for proxy users.

- If check\_proxy\_users is enabled, it may also be necessary to enable a plugin-specific system variable to take advantage of server proxy user mapping support:
  - For the deprecated mysql\_native\_password plugin, enable mysql\_native\_password\_proxy\_users.
  - For the deprecated sha256\_password plugin, enable sha256\_password\_proxy\_users.

For example, to enable all the preceding capabilities, start the server with these lines in the my.cnf file:

```
[mysqld]
check_proxy_users=ON
mysql_native_password_proxy_users=ON
sha256_password_proxy_users=ON
```

Assuming that the relevant system variables have been enabled, create the proxy user as usual using CREATE USER, then grant it the PROXY privilege to a single other account to be treated as the proxied user. When the server receives a successful connection request for the proxy user, it finds that the user has the PROXY privilege and uses it to determine the proper proxied user.

```
-- create proxy account
CREATE USER 'proxy_user'@'localhost'
 IDENTIFIED WITH mysql_native_password
 BY 'password';
-- create proxied account and grant its privileges;
-- use mysql_no_login plugin to prevent direct login
CREATE USER 'proxied_user'@'localhost'
 IDENTIFIED WITH mysql_no_login;
-- grant privileges to proxied account
GRANT ...
 ON ...
 TO 'proxied_user'@'localhost';
-- grant to proxy account the
-- PROXY privilege for proxied account
GRANT PROXY
 ON 'proxied_user'@'localhost'
 TO 'proxy_user'@'localhost';
```

To use the proxy account, connect to the server using its name and password:

```
$> mysql -u proxy_user -p
Enter password: (enter proxy_user password here)
```

Authentication succeeds, the server finds that proxy\_user has the PROXY privilege for proxied\_user, and the session proceeds with proxy\_user having the privileges of proxied\_user.

Proxy user mapping performed by the server is subject to these restrictions:

- The server does not proxy to or from an anonymous user, even if the associated PROXY privilege is granted.
- When a single account has been granted proxy privileges for more than one proxied account, server proxy user mapping is nondeterministic. Therefore, granting to a single account proxy privileges for multiple proxied accounts is discouraged.

# <span id="page-57-0"></span>**Proxy User System Variables**

Two system variables help trace the proxy login process:

• proxy\_user: This value is NULL if proxying is not used. Otherwise, it indicates the proxy user account. For example, if a client authenticates through the ''@'' proxy account, this variable is set as follows:

```
mysql> SELECT @@proxy_user;
+--------------+
| @@proxy_user |
+--------------+
| ''@'' |
+--------------+
```

• external\_user: Sometimes the authentication plugin may use an external user to authenticate to the MySQL server. For example, when using Windows native authentication, a plugin that authenticates using the windows API does not need the login ID passed to it. However, it still uses a Windows user ID to authenticate. The plugin may return this external user ID (or the first 512 UTF-8 bytes of it) to the server using the external\_user read-only session variable. If the plugin does not set this variable, its value is NULL.