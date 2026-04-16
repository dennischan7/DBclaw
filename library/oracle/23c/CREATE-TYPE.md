# Oracle 23c - CREATE-TYPE
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-TYPE.html

Purpose

Object types are defined using PL/SQL. Therefore, this section provides some general information but refers to [Oracle Database PL/SQL Language Reference](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=LNPLS01375) for details of syntax and semantics.

Note:

Starting with Oracle Database 26ai, the SQLJ method of embedding SQL statements in Java code is deprecated. Oracle recommends using the Java Database Connectivity (JDBC) APIs instead of SQLJ.

Use the `CREATE` `TYPE` statement to create the specification of an object type, a SQLJ object type, a named varying array (varray), a nested table type, or an incomplete object type. You create object types with the `CREATE` `TYPE` and the `CREATE` `TYPE` `BODY` statements. The `CREATE` `TYPE` statement specifies the name of the object type, its attributes, methods, and other properties. The `CREATE` `TYPE` `BODY` statement contains the code for the methods that implement the type.

Note:

* If you create an object type for which the type specification declares only attributes but no methods, then you need not specify a type body.
* If you create a SQLJ object type, then you cannot specify a type body. The implementation of the type is specified as a Java class.

An incomplete type is a type created by a forward type definition. It is called "incomplete" because it has a name but no attributes or methods. It can be referenced by other types, and so can be used to define types that refer to each other. However, you must fully specify the type before you can use it to create a table or an object column or a column of a nested table type.

Prerequisites

To create a type in your own schema, you must have the `CREATE` `TYPE` system privilege. To create a type in another user's schema, you must have the `CREATE` `ANY` `TYPE` system privilege. You can acquire these privileges explicitly or be granted them through a role.

To create a subtype, you must have the `UNDER` `ANY` `TYPE` system privilege or the `UNDER` object privilege on the supertype.

The owner of the type must be explicitly granted the `EXECUTE` object privilege in order to access all other types referenced within the definition of the type, or the type owner must be granted the `EXECUTE` `ANY` `TYPE` system privilege. The owner cannot obtain these privileges through roles.

If the type owner intends to grant other users access to the type, then the owner must be granted the `EXECUTE` object privilege on the referenced types with the `GRANT` `OPTION` or the `EXECUTE` `ANY` `TYPE` system privilege with the `ADMIN` `OPTION`. Otherwise, the type owner has insufficient privileges to grant access on the type to other users.

User-Defined Data Types Declared as Non-Persistable Data Types

You can specify a user-defined data type as non-persistable when creating the data type. Instances of non-persistable types cannot persist on disk. Perisistable data types include the following:

* ANSI-supported data types, for example `NUMERIC`, `DECIMAL`, `REAL`.
* Oracle built-in data types, for example `NUMBER`, `VARCHAR2`, `TIMESTAMP`.
* Oracle-supplied data types, for example `ANYDATA`, `XML Type`, `ORDImage`.

Rules For SQL User-Defined Data Types

* A persistable type cannot have attributes or elements of non-persistable types.
* A non-persistable type can have attributes or elements of both persistable and non-persistable types.
* A sub-type must inherit the persistence property from its super type.
* A `REF` type is persistable and can hold references only to objects of persistable types.
* You cannot persist instances of non-persistable types on disk. If you create a table with a type that has been declared as non-persistable, the `CREATE TABLE` statement will fail. The following operations will likewise fail:

  + Create or alter a relational table with columns of non-persistable types.
  + Create an object table with columns of non-persistable types.
  + Store instances of non-persistable types in an `ANYDATA` instance which is persisted on disk.

You can specify unique PL/SQL attributes in the `CREATE TYPE` statement in the PL/SQL context only.

Syntax

Types are defined using PL/SQL. Therefore, the syntax diagram in this book shows only the SQL keywords. Refer to [Oracle Database PL/SQL Language Reference](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=LNPLS01375) for the PL/SQL syntax, semantics, and examples.

OR REPLACE

Specify `OR` `REPLACE` to re-create the type if it already exists. Use this clause to change the definition of an existing type without first dropping it.

Users previously granted privileges on the re-created object type can use and reference the object type without being granted privileges again.

If any function-based indexes depend on the type, then Oracle Database marks the indexes `DISABLED`.

IF NOT EXISTS

Specifying `IF NOT EXISTS` has the following effects:

* If the type does not exist, a new type is created at the end of the statement.
* If the type exists, this is the type you have at the end of the statement. A new one is not created because the older one is detected.

You can have one of `OR REPLACE` or `IF NOT EXISTS` in a statement at a time. Using both `OR REPLACE` with `IF NOT EXISTS` in the very same statement results in the following error: `ORA-11541: REPLACE and IF NOT EXISTS cannot coexist in the same DDL statement`.

Using `IF EXISTS` with `CREATE` results in `ORA-11543: Incorrect IF NOT EXISTS clause for CREATE statement`.

[ EDITIONABLE | NONEDITIONABLE ]

Use these clauses to specify whether the type is an editioned or noneditioned object if editioning is enabled for the schema object type `TYPE` in `schema`.The default is `EDITIONABLE`. For information about editioned and noneditioned objects, see [Oracle Database Development Guide](/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/sqlrf&id=ADFNS99923).