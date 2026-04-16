# Oracle 11g - statements_8010
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8010.htm

[Go to main content](#BEGIN)

438/522 

# DROP DATABASE LINK

Purpose

Use the `DROP` `DATABASE` `LINK` statement to remove a database link from the database.

Prerequisites

A private database link must be in your own schema. To drop a `PUBLIC` database link, you must have the `DROP` `PUBLIC` `DATABASE` `LINK` system privilege.

Semantics

PUBLIC

You must specify `PUBLIC` to drop a `PUBLIC` database link.

dblink

Specify the name of the database link to be dropped.

Restriction on Dropping Database Links You cannot drop a database link in another user's schema, and you cannot qualify `dblink` with the name of a schema, because periods are permitted in names of database links. Therefore, Oracle Database interprets the entire name, such as `ralph.linktosales`, as the name of a database link in your schema rather than as a database link named `linktosales` in the schema `ralph`.

Examples

Dropping a Database Link: Example The following statement drops the public database link named `remote`, which was created in ["Defining a Public Database Link: Example"](statements_5005.md#i2133775):

```
DROP PUBLIC DATABASE LINK remote;
```

Scripting on this page enhances content navigation, but does not change the content in any way.