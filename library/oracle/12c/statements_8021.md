# Oracle 12c - statements_8021
Source: https://docs.oracle.com/database/121/SQLRF/statements_8021.htm

[Go to main content](#BEGIN)

476/555 

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