---
source: PostgreSQL 16 Reference
title: 00_Overview
---

A small number of objects, like role, database, and tablespace names, are defined at the cluster level and stored in the pg\_global tablespace. Inside the cluster are multiple databases, which are isolated from each other but can access cluster-level objects. Inside each database are multiple schemas, which contain objects like tables and functions. So the full hierarchy is: cluster, database, schema, table (or some other kind of object, such as a function).

When connecting to the database server, a client must specify the database name in its connection request. It is not possible to access more than one database per connection. However, clients can open multiple connections to the same database, or different databases. Database-level security has two components: access control (see [Section 21.1](#page-124-1)), managed at the connection level, and authorization control (see Section 5.7), managed via the grant system. Foreign data wrappers (see postgres\_fdw) allow for objects within one database to act as proxies for objects in other database or clusters. The older dblink module (see dblink) provides a similar capability. By default, all users can connect to all databases using all connection methods.

If one PostgreSQL server cluster is planned to contain unrelated projects or users that should be, for the most part, unaware of each other, it is recommended to put them into separate databases and adjust authorizations and access controls accordingly. If the projects or users are interrelated, and thus should be able to use each other's resources, they should be put in the same database but probably into separate schemas; this provides a modular structure with namespace isolation and authorization control. More information about managing schemas is in Section 5.9.

While multiple databases can be created within a single cluster, it is advised to consider carefully whether the benefits outweigh the risks and limitations. In particular, the impact that having a shared WAL (see Chapter 30) has on backup and recovery options. While individual databases in the cluster are isolated when considered from the user's perspective, they are closely bound from the database administrator's point-of-view.

Databases are created with the CREATE DATABASE command (see [Section 23.2](#page-155-1)) and destroyed with the DROP DATABASE command (see [Section 23.5](#page-158-1)). To determine the set of existing databases, examine the pg\_database system catalog, for example

SELECT datname FROM pg\_database;

The psql program's \l meta-command and -l command-line option are also useful for listing the existing databases.

### **Note**

The SQL standard calls databases "catalogs", but there is no difference in practice.

# <span id="page-155-1"></span>**23.2. Creating a Database**

In order to create a database, the PostgreSQL server must be up and running (see [Section 19.3](#page-15-0)).

Databases are created with the SQL command CREATE DATABASE:

CREATE DATABASE name;

where name follows the usual rules for SQL identifiers. The current role automatically becomes the owner of the new database. It is the privilege of the owner of a database to remove it later (which also removes all the objects in it, even if they have a different owner).

The creation of databases is a restricted operation. See [Section 22.2](#page-148-0) for how to grant permission.

Since you need to be connected to the database server in order to execute the CREATE DATABASE command, the question remains how the *first* database at any given site can be created. The first database is always created by the initdb command when the data storage area is initialized. (See [Section 19.2](#page-13-2).) This database is called postgres. So to create the first "ordinary" database you can connect to postgres.

Two additional databases, template1 and template0, are also created during database cluster initialization. Whenever a new database is created within the cluster, template1 is essentially cloned. This means that any changes you make in template1 are propagated to all subsequently created databases. Because of this, avoid creating objects in template1 unless you want them propagated to every newly created database. template0 is meant as a pristine copy of the original contents of template1. It can be cloned instead of template1 when it is important to make a database without any such site-local additions. More details appear in [Section 23.3.](#page-156-0)

As a convenience, there is a program you can execute from the shell to create new databases, createdb.

createdb dbname

createdb does no magic. It connects to the postgres database and issues the CREATE DATA-BASE command, exactly as described above. The createdb reference page contains the invocation details. Note that createdb without any arguments will create a database with the current user name.

### **Note**

[Chapter 21](#page-124-0) contains information about how to restrict who can connect to a given database.

Sometimes you want to create a database for someone else, and have them become the owner of the new database, so they can configure and manage it themselves. To achieve that, use one of the following commands:

CREATE DATABASE dbname OWNER rolename;

from the SQL environment, or:

createdb -O rolename dbname

from the shell. Only the superuser is allowed to create a database for someone else (that is, for a role you are not a member of).

# <span id="page-156-0"></span>**23.3. Template Databases**

CREATE DATABASE actually works by copying an existing database. By default, it copies the standard system database named template1. Thus that database is the "template" from which new databases are made. If you add objects to template1, these objects will be copied into subsequently created user databases. This behavior allows site-local modifications to the standard set of objects in databases. For example, if you install the procedural language PL/Perl in template1, it will automatically be available in user databases without any extra action being taken when those databases are created.

However, CREATE DATABASE does not copy database-level GRANT permissions attached to the source database. The new database has default database-level permissions.

There is a second standard system database named template0. This database contains the same data as the initial contents of template1, that is, only the standard objects predefined by your version of PostgreSQL. template0 should never be changed after the database cluster has been initialized. By instructing CREATE DATABASE to copy template0 instead of template1, you can create a "pristine" user database (one where no user-defined objects exist and where the system objects have not been altered) that contains none of the site-local additions in template1. This is particularly handy when restoring a pg\_dump dump: the dump script should be restored in a pristine database to ensure that one recreates the correct contents of the dumped database, without conflicting with objects that might have been added to template1 later on.

Another common reason for copying template0 instead of template1 is that new encoding and locale settings can be specified when copying template0, whereas a copy of template1 must use the same settings it does. This is because template1 might contain encoding-specific or locale-specific data, while template0 is known not to.

To create a database by copying template0, use:

CREATE DATABASE dbname TEMPLATE template0;

from the SQL environment, or:

createdb -T template0 dbname

from the shell.

It is possible to create additional template databases, and indeed one can copy any database in a cluster by specifying its name as the template for CREATE DATABASE. It is important to understand, however, that this is not (yet) intended as a general-purpose "COPY DATABASE" facility. The principal limitation is that no other sessions can be connected to the source database while it is being copied. CREATE DATABASE will fail if any other connection exists when it starts; during the copy operation, new connections to the source database are prevented.

Two useful flags exist in pg\_database for each database: the columns datistemplate and datallowconn. datistemplate can be set to indicate that a database is intended as a template for CREATE DATABASE. If this flag is set, the database can be cloned by any user with CREATEDB privileges; if it is not set, only superusers and the owner of the database can clone it. If datallowconn is false, then no new connections to that database will be allowed (but existing sessions are not terminated simply by setting the flag false). The template0 database is normally marked datallowconn = false to prevent its modification. Both template0 and template1 should always be marked with datistemplate = true.

### **Note**

template1 and template0 do not have any special status beyond the fact that the name template1 is the default source database name for CREATE DATABASE. For example, one could drop template1 and recreate it from template0 without any ill effects. This course of action might be advisable if one has carelessly added a bunch of junk in template1. (To delete template1, it must have pg\_database.datistemplate = false.)

The postgres database is also created when a database cluster is initialized. This database is meant as a default database for users and applications to connect to. It is simply a copy of template1 and can be dropped and recreated if necessary.