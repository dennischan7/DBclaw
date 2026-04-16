# Oracle 12c - statements_6014
Source: https://docs.oracle.com/database/121/SQLRF/statements_6014.htm

Purpose

Use the `CREATE` `ROLE` statement to create a role, which is a set of privileges that can be granted to users or to other roles. You can use roles to administer database privileges. You can add privileges to a role and then grant the role to a user. The user can then enable the role and exercise the privileges granted by the role.

A role contains all privileges granted to the role and all privileges of other roles granted to it. A new role is initially empty. You add privileges to a role with the `GRANT` statement.

If you create a role that is `NOT` `IDENTIFIED` or is `IDENTIFIED` `EXTERNALLY` or `BY` `password`, then Oracle Database grants you the role with `ADMIN` `OPTION`. However, if you create a role `IDENTIFIED` `GLOBALLY`, then the database does not grant you the role. A global role cannot be granted to a user or role directly. Global roles can be granted only through enterprise roles.

Prerequisites

You must have the `CREATE` `ROLE` system privilege.

To specify the `CONTAINER` clause, you must be connected to a multitenant container database (CDB). To specify `CONTAINER` `=` `ALL`, the current container must be the root. To specify `CONTAINER` `=` `CURRENT`, the current container must be a pluggable database (PDB).

Semantics

role

Specify the name of the role to be created. Oracle recommends that the role contain at least one single-byte character regardless of whether the database character set also contains multibyte characters. The maximum length of the role name is 30 bytes. The maximum number of user-defined roles that can be enabled for a single user at one time is 148.

In a non-CDB, a role name cannot begin with `C##` or `c##`.

In a CDB, the requirements for a role name are as follows:

* In Oracle Database 12c Release 1 (12.1.0.1), the name of a common role must begin with `C##` or `c##` and the name of a local role must not begin with `C##` or `c##`.
* Starting with Oracle Database 12c Release 1 (12.1.0.2):

  + The name of a common role must begin with characters that are a case-insensitive match to the prefix specified by the `COMMON_USER_PREFIX` initialization parameter. By default, the prefix is `C##`.
  + The name of a local role must not begin with characters that are a case-insensitive match to the prefix specified by the `COMMON_USER_PREFIX` initialization parameter. Regardless of the value of `COMMON_USER_PREFIX`, the name of a local role can never begin with `C##` or `c##`.

Note:

If the value of

`COMMON_USER_PREFIX`

is an empty string, then there are no requirements for common or local role names with one exception: the name of a local role can never begin with

`C##`

or

`c##`

. Oracle recommends against using an empty string value because it might result in conflicts between the names of local and common roles when a PDB is plugged into a different CDB, or when opening a PDB that was closed when a common user was created.

Some roles are defined by SQL scripts provided on your distribution media.

See Also:

[GRANT](statements_9014.md#i2155015)

for a list of these predefined roles and

[SET ROLE](statements_10004.md#i2135600)

for information on enabling and disabling roles for a user

NOT IDENTIFIED Clause

Specify `NOT` `IDENTIFIED` to indicate that this role is authorized by the database and that no password is required to enable the role.

IDENTIFIED Clause

Use the `IDENTIFIED` clause to indicate that a user must be authorized by the specified method before the role is enabled with the `SET` `ROLE` statement.

BY password The `BY` `password` clause lets you create a local role and indicates that the user must specify the password to the database when enabling the role. The password can contain only single-byte characters from your database character set regardless of whether this character set also contains multibyte characters.

USING package The `USING` `package` clause lets you create a secure application role, which is a role that can be enabled only by applications using an authorized package. If you do not specify `schema`, then the database assumes the package is in your own schema.

EXTERNALLY Specify `EXTERNALLY` to create an external role. An external user must be authorized by an external service, such as an operating system or third-party service, before enabling the role.

Depending on the operating system, the user may have to specify a password to the operating system before the role is enabled.

GLOBALLY Specify `GLOBALLY` to create a global role. A global user must be authorized to use the role by the enterprise directory service before the role is enabled at login.

If you omit both the `NOT` `IDENTIFIED` clause and the `IDENTIFIED` clause, then the role defaults to `NOT` `IDENTIFIED`.

CONTAINER Clause

The `CONTAINER` clause applies when you are connected to a CDB. However, it is not necessary to specify the `CONTAINER` clause because its default values are the only allowed values.

* To create a common role, you must be connected to the root. You can optionally specify `CONTAINER` `=` `ALL`, which is the default when you are connected to the root.
* To create a local role, you must be connected to a PDB. You can optionally specify `CONTAINER` `=` `CURRENT`, which is the default when you are connected to a PDB.

Examples

Creating a Role: Example The following statement creates the role `dw_manager`:

```
CREATE ROLE dw_manager;
```

Users who are subsequently granted the `dw_manager` role will inherit all of the privileges that have been granted to this role.

You can add a layer of security to roles by specifying a password, as in the following example:

```
CREATE ROLE dw_manager
   IDENTIFIED BY warehouse;
```

Users who are subsequently granted the `dw_manager` role must specify the password `warehouse` to enable the role with the `SET` `ROLE` statement.

The following statement creates global role `warehouse_user`:

```
CREATE ROLE warehouse_user IDENTIFIED GLOBALLY;
```

The following statement creates the same role as an external role:

```
CREATE ROLE warehouse_user IDENTIFIED EXTERNALLY;
```

The following statement creates local role `role1` in the current PDB. The current container must be a PDB when you issue this statement:

```
CREATE ROLE role1 CONTAINER = CURRENT;
```

The following statement creates common role `c##role1`. The current container must be the root when you issue this statement:

```
CREATE ROLE c##role1 CONTAINER = ALL;
```