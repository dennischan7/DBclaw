# Oracle 12c - statements_8003
Source: https://docs.oracle.com/database/121/SQLRF/statements_8003.htm

Semantics

user

Specify the name of the user to be created. This name can contain only characters from your database character set and must follow the rules described in the section ["Database Object Naming Rules"](sql_elements008.md#i27570). Oracle recommends that the user name contain at least one single-byte character regardless of whether the database character set also contains multibyte characters.

In a non-CDB, a user name cannot begin with `C##` or `c##`.

In a CDB, the requirements for a user name are as follows:

* In Oracle Database 12c Release 1 (12.1.0.1), the name of a common user must begin with `C##` or `c##` and the name of a local user must not begin with `C##` or `c##`.
* Starting with Oracle Database 12c Release 1 (12.1.0.2):

  + The name of a common user must begin with characters that are a case-insensitive match to the prefix specified by the `COMMON_USER_PREFIX` initialization parameter. By default, the prefix is `C##`.
  + The name of a local user must not begin with characters that are a case-insensitive match to the prefix specified by the `COMMON_USER_PREFIX` initialization parameter. Regardless of the value of `COMMON_USER_PREFIX`, the name of a local user can never begin with `C##` or `c##`.

Note:

If the value of

`COMMON_USER_PREFIX`

is an empty string, then there are no requirements for common or local user names with one exception: the name of a local user can never begin with

`C##`

or

`c##`

. Oracle recommends against using an empty string value because it might result in conflicts between the names of local and common users when a PDB is plugged into a different CDB, or when opening a PDB that was closed when a common user was created.

Note:

Oracle recommends that user names and passwords be encoded in ASCII or EBCDIC characters only, depending on your platform.

IDENTIFIED Clause

The `IDENTIFIED` clause lets you indicate how Oracle Database authenticates the user.

BY password

The `BY` `password` clause lets you creates a local user and indicates that the user must specify `password` to log on to the database. Passwords are case sensitive. Any subsequent `CONNECT` string used to connect this user to the database must specify the password using the same case (upper, lower, or mixed) that is used in this `CREATE` `USER` statement or a subsequent `ALTER` `USER` statement. Passwords can contain any single-byte, multibyte, or special characters, or any combination of these, from your database character set, with the exception of the double quotation mark (") and the return character. If a password starts with a non-alphabetic character, or contains a character other than an alphanumeric character, the underscore (\_), dollar sign ($), or pound sign (#), then it must be enclosed in double quotation marks. Otherwise, enclosing a password in double quotation marks is optional.

Passwords must follow the rules described in the section ["Database Object Naming Rules"](sql_elements008.md#i27570), unless you are using one of the three Oracle Database password complexity verification routines. These routines requires a more complex combination of characters than the normal naming rules permit. You implement these routines with the `UTLPWDMG.SQL` script, which is further described in [Oracle Database Security Guide](../DBSEG/authentication.md#DBSEG845).

Note:

Oracle recommends that user names and passwords be encoded in ASCII or EBCDIC characters only, depending on your platform.

EXTERNALLY Clause

Specify `EXTERNALLY` to create an external user. Such a user must be authenticated by an external service, such as an operating system or a third-party service. In this case, Oracle Database relies on authentication by the operating system or third-party service to ensure that a specific external user has access to a specific database user.

AS 'certificate\_DN' This clause is required for and used for SSL-authenticated external users only. The `certificate_DN` is the distinguished name in the user's PKI certificate in the user's wallet. The maximum length of `certificate_DN` is 1024 characters.

AS 'kerberos\_principal\_name' This clause is required for and used for Kerberos-authenticated external users only. The maximum length of `kerberos_principal_name` is 1024 characters.

Caution:

Oracle strongly recommends that you do not use

`IDENTIFIED` `EXTERNALLY`

with operating systems that have inherently weak login security.

Restrictions on Creating External Users The following restrictions apply to creating external users:

GLOBALLY Clause

The `GLOBALLY` clause lets you create a global user. Such a user must be authorized by the enterprise directory service (Oracle Internet Directory).

The `directory_DN` string can take one of two forms:

* The X.509 name at the enterprise directory service that identifies this user. It should be of the form `CN=``username,other_attributes`, where `other_attributes` is the rest of the user's distinguished name (DN) in the directory. This form creates a private global schema.
* A null string (' ') indicating that the enterprise directory service will map authenticated global users to this database schema with the appropriate roles. This form is the same as specifying the `GLOBALLY` keyword alone and creates a shared global schema.

The maximum length of `directory_DN` is 1024 characters.

You can control the ability of an application server to connect as the specified user and to activate that user's roles using the `ALTER` `USER` statement.

Restriction on Creating Global Users Oracle ASM does not support the creation of global users.

DEFAULT TABLESPACE Clause

Specify the default tablespace for objects that are created in the user's schema. If you omit this clause, then the user's objects are stored in the database default tablespace. If no default tablespace has been specified for the database, then the user's objects are stored in the `SYSTEM` tablespace.

Restriction on Default Tablespaces You cannot specify a locally managed temporary tablespace, including an undo tablespace, or a dictionary-managed temporary tablespace, as a user's default tablespace.

TEMPORARY TABLESPACE Clause

Specify the tablespace or tablespace group for the user's temporary segments. If you omit this clause, then the user's temporary segments are stored in the database default temporary tablespace or, if none has been specified, in the `SYSTEM` tablespace.

* Specify `tablespace` to indicate the user's temporary tablespace. If you are connected to a CDB, then you can specify `CDB$DEFAULT` to use the CDB-wide default temporary tablespace.
* Specify `tablespace_group_name` to indicate that the user can save temporary segments in any tablespace in the tablespace group specified by `tablespace_group_name`.

Restrictions on Temporary Tablespace This clause is subject to the following restrictions:

QUOTA Clause

Use the `QUOTA` clause to specify the maximum amount of space the user can allocate in the tablespace.

A `CREATE` `USER` statement can have multiple `QUOTA` clauses for multiple tablespaces.

`UNLIMITED` lets the user allocate space in the tablespace without bound.

The maximum amount of space that you can specify is 2 terabytes (TB). If you need more space, then specify `UNLIMITED`.

Restriction on the QUOTA Clause You cannot specify this clause for a temporary tablespace.

PROFILE Clause

Specify the profile you want to assign to the user. The profile limits the amount of database resources the user can use. If you omit this clause, then Oracle Database assigns the `DEFAULT` profile to the user.

Note:

Oracle recommends that you use the Database Resource Manager rather SQL profiles to establish database resource limits. The Database Resource Manager offers a more flexible means of managing and tracking resource use. For more information on the Database Resource Manager, refer to

[Oracle Database Administrator's Guide.](../ADMIN/dbrm.md#ADMIN027)

PASSWORD EXPIRE Clause

Specify `PASSWORD` `EXPIRE` if you want the user's password to expire. This setting forces the user or the DBA to change the password before the user can log in to the database.

ACCOUNT Clause

Specify `ACCOUNT` `LOCK` to lock the user's account and disable access. Specify `ACCOUNT` `UNLOCK` to unlock the user's account and enable access to the account. The default is `ACCOUNT` `UNLOCK`.

ENABLE EDITIONS

This clause is not reversible. Specify `ENABLE` `EDITIONS` to allow the user to create multiple versions of editionable objects in this schema using editions. Editionable objects in schemas that are not editions-enabled cannot be editioned.

Restriction on Enabling Editions You cannot enable editions for any schemas supplied by Oracle except for the sample schemas in the seed database.

CONTAINER Clause

The `CONTAINER` clause applies when you are connected to a CDB. However, it is not necessary to specify the `CONTAINER` clause because its default values are the only allowed values.

* To create a common user, you must be connected to the root. You can optionally specify `CONTAINER` `=` `ALL`, which is the default when you are connected to the root.
* To create a local user, you must be connected to a PDB. You can optionally specify `CONTAINER` `=` `CURRENT`, which is the default when you are connected to a PDB.

While creating a common user, any default tablespace, temporary tablespace, or profile specified using the following clauses must exist in all the containers belonging to the CDB:

* `DEFAULT` `TABLESPACE`
* `TEMPORARY` `TABLESPACE`
* `QUOTA`
* `PROFILE`

If these objects do not exist in all the containers, the `CREATE` `USER` statement fails.

Examples

All of the following examples use the `example` tablespace, which exists in the seed database and is accessible to the sample schemas.

Creating a Database User: Example If you create a new user with `PASSWORD` `EXPIRE`, then the user's password must be changed before the user attempts to log in to the database. You can create the user `sidney` by issuing the following statement:

```
CREATE USER sidney 
    IDENTIFIED BY out_standing1 
    DEFAULT TABLESPACE example 
    QUOTA 10M ON example 
    TEMPORARY TABLESPACE temp
    QUOTA 5M ON system 
    PROFILE app_user 
    PASSWORD EXPIRE;
```

The user `sidney` has the following characteristics:

* The password `out_standing1`
* Default tablespace `example`, with a quota of 10 megabytes
* Temporary tablespace `temp`
* Access to the tablespace `SYSTEM`, with a quota of 5 megabytes
* Limits on database resources defined by the profile `app_user` (which was created in ["Creating a Profile: Example"](statements_6012.md#i2092094))
* An expired password, which must be changed before `sidney` can log in to the database

Creating External Database Users: Examples The following example creates an external user, who must be identified by an external source before accessing the database:

```
CREATE USER app_user1
   IDENTIFIED EXTERNALLY
   DEFAULT TABLESPACE example
   QUOTA 5M ON example
   PROFILE app_user;
```

The user `app_user1` has the following additional characteristics:

* Default tablespace `example`
* Default temporary tablespace `example`
* 5M of space on the tablespace `example` and unlimited quota on the temporary tablespace of the database
* Limits on database resources defined by the `app_user` profile

To create another user accessible only by an operating system account, prefix the user name with the value of the initialization parameter `OS_AUTHENT_PREFIX`. For example, if this value is "`ops$`", then you can create the externally identified user `external_user` with the following statement:

```
CREATE USER ops$external_user
   IDENTIFIED EXTERNALLY
   DEFAULT TABLESPACE example
   QUOTA 5M ON example
   PROFILE app_user;
```

Creating a Global Database User: Example The following example creates a global user. When you create a global user, you can specify the X.509 name that identifies this user at the enterprise directory server:

```
CREATE USER global_user
   IDENTIFIED GLOBALLY AS 'CN=analyst, OU=division1, O=oracle, C=US'
   DEFAULT TABLESPACE example
   QUOTA 5M ON example;
```

Creating a Common User in a CDB The following example creates a common user called c##`comm_user` in a CDB. Before you run this `CREATE USER` statement, ensure that the tablespaces `example` and `temp_tbs` exist in all of the containers in the CDB.

```
CREATE USER c##comm_user
   IDENTIFIED BY comm_pwd
   DEFAULT TABLESPACE example
   QUOTA 20M ON example
   TEMPORARY TABLESPACE temp_tbs;
```

The user `comm_user` has the following additional characteristics: