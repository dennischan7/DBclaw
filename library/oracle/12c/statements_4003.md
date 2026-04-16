# Oracle 12c - statements_4003
Source: https://docs.oracle.com/database/121/SQLRF/statements_4003.htm

Semantics

The keywords, parameters, and clauses described in this section are unique to `ALTER` `USER` or have different semantics than they have in `CREATE` `USER`. Keywords, parameters, and clauses that do not appear here have the same meaning as in the `CREATE` `USER` statement.

Note:

Oracle recommends that user names and passwords be encoded in ASCII or EBCDIC characters only, depending on your platform.

See Also:

[CREATE USER](statements_8003.md#i2065278)

for information on the keywords and parameters and

[CREATE PROFILE](statements_6012.md#i2065930)

for information on assigning limits on database resources to a user

IDENTIFIED Clause

BY password  Specify `BY` `password` to specify a new password for the user. Passwords are case sensitive. Any subsequent `CONNECT` string used to connect this user to the database must specify the password using the same case (upper, lower, or mixed) that is used in this `ALTER` `USER` statement. Passwords can contain single-byte, or multibyte characters, or both from your database character set.

Note:

Oracle Database expects a different timestamp for each resetting of a particular password. If you reset one password multiple times within one second (for example, by cycling through a set of passwords using a script), then the database may return an error message that the password cannot be reused. For this reason, Oracle recommends that you avoid using scripts to reset passwords.

You can omit the `REPLACE` clause if you are setting your own password or you have the `ALTER` `USER` system privilege and you are changing another user's password. However, unless you have the `ALTER` `USER` system privilege, you must always specify the `REPLACE` clause if a password complexity verification function has been enabled, either by running the `UTLPWDMG.SQL` script or by specifying such a function in the `PASSWORD_VERIFY_FUNCTION` parameter of a profile that has been assigned to the user.

In an Oracle ASM cluster, you can use this clause to change the password of a user in the password file that is local to an Oracle ASM instance of the current node. You must be authenticated `AS` `SYSASM` to specify `IDENTIFIED` `BY` `password` without the `REPLACE` `old_password` clause. If you are not authenticated `AS` `SYSASM`, then you can only change your own password by specifying `REPLACE` `old_password`.

Oracle Database does not check the old password, even if you provide it in the `REPLACE` clause, unless you are changing your own existing password.

GLOBALLY Refer to [CREATE USER](statements_8003.md#i2065278) for more information on this clause.

You can change a user's access verification method from `IDENTIFIED` `GLOBALLY` to either `IDENTIFIED` `BY` `password` or `IDENTIFIED` `EXTERNALLY`. You can change a user's access verification method to `IDENTIFIED` `GLOBALLY` from one of the other methods only if all external roles granted explicitly to the user are revoked.

EXTERNALLY Refer to [CREATE USER](statements_8003.md#i2065278) for more information on this clause.

DEFAULT TABLESPACE Clause

Use this clause to assign or reassign a tablespace for the user's permanent segments. This clause overrides any default tablespace that has been specified for the database.

Restriction on Default Tablespaces You cannot specify a locally managed temporary tablespace, including an undo tablespace, or a dictionary-managed temporary tablespace, as a user's default tablespace.

TEMPORARY TABLESPACE Clause

Use this clause to assign or reassign a tablespace or tablespace group for the user's temporary segments.

* Specify `tablespace` to indicate the user's temporary tablespace. If you are connected to a CDB, then you can specify `CDB$DEFAULT` to use the CDB-wide default temporary tablespace.
* Specify `tablespace_group_name` to indicate that the user can save temporary segments in any tablespace in the tablespace group specified by `tablespace_group_name`.

Restriction on User Temporary Tablespace Any individual tablespace you assign or reassign as the user's temporary tablespace must be a temporary tablespace and must have a standard block size.

DEFAULT ROLE Clause

Specify the roles granted by default to the user at logon. This clause can contain only roles that have been granted directly to the user with a `GRANT` statement, or roles created by the user with the `CREATE` `ROLE` privilege. You cannot use the `DEFAULT` `ROLE` clause to specify:

* Roles not granted to the user
* Roles granted through other roles
* Roles managed by an external service (such as the operating system), or by the Oracle Internet Directory
* Roles that are enabled by the `SET` `ROLE` statement, such as password-authenticated roles and secure application roles

Assigning Default Roles to Common Users in a CDB You can modify the default role assigned to a common user both in the current container and across all containers in a CDB.

While assigning a default role to a common user across all containers, `role` must be a common role that was commonly granted to the common user.

While assigning a default role to a common user in the current container, `role` must be one of the following:

* A local role that was granted to the common user in the current container
* A common role that was granted to the common user, either commonly or locally in the current container

ENABLE EDITIONS

This clause is not reversible. Specify `ENABLE` `EDITIONS` to allow the user to create multiple versions of editionable objects in this schema using editions. Editionable objects in non-editions-enabled schemas cannot be editioned.

Use the `FOR` clause to specify one or more object types for which the user can create editionable objects. For a list of valid values for `object_type`, query the `V$EDITIONABLE_TYPES` dynamic performance view. If you omit the `FOR` clause, then the user can create editionable objects for all editionable object types.

If the schema to be editions-enabled contains any objects that are not editionable and that depend on editionable type objects in the schema, then you must specify `FORCE` to enable editions for this schema. In this case, all the objects that are not editionable and that depend on the editionable type objects in the schema being editions-enabled become invalid.

CONTAINER Clause

If the current container is a PDB, then you can specify `CONTAINER` `=` `CURRENT` to change the attributes of a local user, or the container-specific attributes (such as the default tablespace) of a common user, in the current container. If the current container is the root, then you can specify `CONTAINER` `=` `ALL` to change the attributes of a common user across the entire CDB. If you omit this clause and the current container is a PDB, then `CONTAINER` `=` `CURRENT` is the default. If you omit this clause and the current container is the root, then `CONTAINER` `=` `ALL` is the default.

Restriction on Modifying Common Users in a CDB Certain attributes of a common user must be modified for all the containers in a CDB and not for only some containers. Therefore, when you use any of the following clauses to modify a common user, ensure that you modify all of the containers by connecting to the root and specifying `CONTAINER=ALL`:

* `IDENTIFIED` clause
* `PASSWORD` clause

container\_data\_clause

The `container_data_clause` allows you the set and modify `CONTAINER_DATA` attributes for a common user. Use the `FOR` clause to indicate whether to set or modify the default `CONTAINER_DATA` attribute or an object-specific `CONTAINER_DATA` attribute. These attributes determine the set of containers (which can never exclude the root) whose data will be visible via `CONTAINER_DATA` objects to the specified common user when the current session is the root.

To specify the `container_data_clause`, the current session must be the root and you must specify `CONTAINER` `=` `CURRENT`.

SET CONTAINER\_DATA Use this clause to set the default `CONTAINER_DATA` attribute or an object-specific `CONTAINER_DATA` attribute for a common user. When you specify this clause, you replace the existing value, if any, of the `CONTAINER_DATA` attribute.

Use `container_name` to specify one or more containers that will be accessible to the user.

Use `ALL` to specify that all current and future containers in the CDB will be accessible to the user.

Use `DEFAULT` to specify the default behavior, which is as follows:

* For a default `CONTAINER_DATA` attribute, the current container, that is, the root, and the CDB as a whole will be accessible to the user.
* For an object-specific `CONTAINER_DATA` attribute, the database will use the user's default `CONTAINER_DATA` attribute.

Note:

`CONTAINER_DATA`

attributes that are set to

`DEFAULT`

are not visible in the

`DBA_CONTAINER_DATA`

view.

ADD CONTAINER\_DATA Use this clause to add containers to the default `CONTAINER_DATA` attribute or an object-specific `CONTAINER_DATA` attribute for a common user. Use `container_name` to specify one or more containers to add.

You cannot use this clause if the default `CONTAINER_DATA` attribute is set to `ALL`. If you use this clause when the default `CONTAINER_DATA` attribute is set to `DEFAULT`, then `CDB$ROOT` will automatically be added to the set of containers, unless the set already contains `CDB$ROOT`.

You cannot use this clause if the object-specific `CONTAINER_DATA` attribute is set to `ALL` or `DEFAULT`.

REMOVE CONTAINER\_DATA Use this clause to remove containers from the default `CONTAINER_DATA` attribute or an object-specific `CONTAINER_DATA` attribute for a common user. Use `container_name` to specify one or more containers to remove.

You cannot use this clause if the default `CONTAINER_DATA` attribute or object-specific `CONTAINER_DATA` attribute is set to `ALL` or `DEFAULT`.

FOR container\_data\_object If you specify the `FOR` clause, then you can set and modify the object-specific `CONTAINER_DATA` attribute for `container_data_object` for a common user. `container_data_object` must be a `CONTAINER_DATA` table or view. If you omit `schema`, then Oracle Database assumes that `container_data_object` is in your own schema.

If you omit the `FOR` clause, then you can set and modify the default `CONTAINER_DATA` attribute for a common user.

proxy\_clause

The `proxy_clause` lets you control the ability of an enterprise user (a user outside the database) or a database proxy (another database user) to connect as the database user being altered.

GRANT CONNECT THROUGH

Specify `GRANT` `CONNECT` `THROUGH` to allow the connection.

REVOKE CONNECT THROUGH

Specify `REVOKE` `CONNECT` `THROUGH` to prohibit the connection.

ENTERPRISE USER

This clause lets you expose `user` to proxy use by enterprise users. The administrator working in Oracle Internet Directory must then grant privileges for appropriate enterprise users to act on behalf of `user`.

db\_user\_proxy

This clause lets you expose `user` to proxy use by database user `db_user_proxy` (the proxy).

* The proxy will have all privileges that were directly granted to `user`.
* The proxy will have all roles associated with `user`, unless you specify the `WITH` clauses of `db_user_proxy_clauses` to limit the proxy to some or none of the roles of `user`. For each role associated with the proxy, if the role is enabled by default for `user` at login, then that role will also be enabled by default for the proxy at login.

db\_user\_proxy\_clauses

Specify the `WITH` clauses to limit the proxy to some or none of the roles associated with `user`, and the `AUTHENTICATION` `REQUIRED` clause to specify whether authentication is required.

WITH ROLE `WITH` `ROLE` `role_name` permits the proxy to connect as the specified user and to activate only the roles that are specified by `role_name.` This clause can contain only roles that are associated with `user`.

WITH ROLE ALL EXCEPT `WITH` `ROLE` `ALL` `EXCEPT` `role_name` permits the proxy to connect as the specified user and to activate all roles associated with that user except those specified for `role_name`. This clause can contain only roles that are associated with `user`.

WITH NO ROLES `WITH` `NO` `ROLES` permits the proxy to connect as the specified user, but prohibits the proxy from activating any of that user's roles after connecting.

AUTHENTICATION REQUIRED  Oracle Database does not expect the proxy to authenticate the user unless you specify the `AUTHENTICATION` `REQUIRED` clause. This clause ensures that authentication credentials for the user must be presented when the user is authenticated through the specified proxy. The credential is a password.

AUTHENTICATED USING  The `AUTHENTICATED` `USING` clauses, which appeared in the syntax of earlier releases, have been deprecated and are no longer needed. If you specify the `AUTHENTICATED` `USING` `PASSWORD` clause, then Oracle Database converts it to the `AUTHENTICATION` `REQUIRED` clause. Specifying the `AUTHENTICATED` `USING` `CERTIFICATE` clause or the `AUTHENTICATED` `USING` `DISTINGUISHED` `NAME` clause is equivalent to omitting the `AUTHENTICATION` `REQUIRED` clause.

Examples

Changing User Identification: Example The following statement changes the password of the user `sidney` (created in ["Creating a Database User: Example"](statements_8003.md#i2103003)) `second_2nd_pwd` and default tablespace to the tablespace `example`:

```
ALTER USER sidney 
    IDENTIFIED BY second_2nd_pwd
    DEFAULT TABLESPACE example;
```

The following statement assigns the `new_profile` profile (created in ["Creating a Profile: Example"](statements_6012.md#i2092094)) to the sample user `sh`:

```
ALTER USER sh 
    PROFILE new_profile;
```

In subsequent sessions, `sh` is restricted by limits in the `new_profile` profile.

The following statement makes all roles granted directly to `sh` default roles, except the `dw_manager` role:

```
ALTER USER sh 
    DEFAULT ROLE ALL EXCEPT dw_manager;
```

At the beginning of `sh`'s next session, Oracle Database enables all roles granted directly to `sh` except the `dw_manager` role.

Changing User Authentication: Examples The following statement changes the authentication mechanism of user `app_user1` (created in ["Creating a Database User: Example"](statements_8003.md#i2103003)`)`:

```
ALTER USER app_user1 IDENTIFIED GLOBALLY AS 'CN=tom,O=oracle,C=US';
```

The following statement causes user `sidney`'s password to expire:

```
ALTER USER sidney PASSWORD EXPIRE;
```

If you cause a database user's password to expire with `PASSWORD` `EXPIRE`, then the user (or the DBA) must change the password before attempting to log in to the database following the expiration. However, tools such as SQL\*Plus allow the user to change the password on the first attempted login following the expiration.

Assigning a Tablespace Group: Example The following statement assigns `tbs_grp_01` (created in ["Adding a Temporary Tablespace to a Tablespace Group: Example"](statements_7003.md#i2204334)) as the tablespace group for user `sh`:

```
ALTER USER sh
  TEMPORARY TABLESPACE tbs_grp_01;
```

Proxy Users: Examples The following statement alters the user `app_user1`. The example permits the `app_user1` to connect through the proxy user `sh`. The example also allows `app_user1` to enable its `warehouse_user` role (created in ["Creating a Role: Example"](statements_6014.md#i2082342)) when connected through the proxy `sh`:

```
ALTER USER app_user1 
   GRANT CONNECT THROUGH sh
   WITH ROLE warehouse_user;
```

To show basic syntax, this example uses the sample database Sales History user (`sh`) as the proxy. Normally a proxy user would be an application server or middle-tier entity. For information on creating the interface between an application user and a database by way of an application server, refer to [Oracle Call Interface Programmer's Guide.](../LNOCI/toc.md)

The following statement takes away the right of user `app_user1` to connect through the proxy user `sh`:

```
ALTER USER app_user1 REVOKE CONNECT THROUGH sh;
```

The following hypothetical examples shows another method of proxy authentication:

```
ALTER USER sully GRANT CONNECT THROUGH OAS1
   AUTHENTICATED USING PASSWORD;
```

The following example exposes the user `app_user1` to proxy use by enterprise users. The enterprise users cannot act on behalf of `app_user1` until the Oracle Internet Directory administrator has granted them appropriate privileges:

```
ALTER USER app_user1
   GRANT CONNECT THROUGH ENTERPRISE USERS;
```