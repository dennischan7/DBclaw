# Oracle 11g - statements_8020
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8020.htm

[Go to main content](#BEGIN)

448/522 

# DROP LIBRARY

Purpose

Use the `DROP` `LIBRARY` statement to remove an external procedure library from the database.

Prerequisites

You must have the `DROP` `ANY` `LIBRARY` system privilege.

Semantics

library\_name

Specify the name of the external procedure library being dropped.

Examples

Dropping a Library: Example The following statement drops the `ext_lib` library:

```
DROP LIBRARY ext_lib;
```

Scripting on this page enhances content navigation, but does not change the content in any way.