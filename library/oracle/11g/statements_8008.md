# Oracle 11g - statements_8008
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8008.htm

[Go to main content](#BEGIN)

436/522 

# DROP CONTEXT

Purpose

Use the `DROP` `CONTEXT` statement to remove a context namespace from the database.

Removing a context namespace does not invalidate any context under that namespace that has been set for a user session. However, the context will be invalid when the user next attempts to set that context.

Prerequisites

You must have the `DROP` `ANY` `CONTEXT` system privilege.

Semantics

namespace

Specify the name of the context namespace to drop. You cannot drop the built-in namespace `USERENV`.

See Also:

[SYS\_CONTEXT](functions184.md#i1038176)

for information on the

`USERENV`

namespace

Examples

Dropping an Application Context: Example The following statement drops the context created in [CREATE CONTEXT](statements_5002.md#i2060927):

```
DROP CONTEXT hr_context;
```

Scripting on this page enhances content navigation, but does not change the content in any way.