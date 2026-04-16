# Oracle 12c - statements_8013
Source: https://docs.oracle.com/database/121/SQLRF/statements_8013.htm

[Go to main content](#BEGIN)

468/555 

# DROP DIRECTORY

Purpose

Use the `DROP` `DIRECTORY` statement to remove a directory object from the database.

Prerequisites

To drop a directory, you must have the `DROP` `ANY` `DIRECTORY` system privilege.

Caution:

Do not drop a directory when files in the associated file system are being accessed by PL/SQL or OCI programs.

Semantics

directory\_name

Specify the name of the directory database object to be dropped.

Oracle Database removes the directory object but does not delete the associated operating system directory on the server file system.

Examples

Dropping a Directory: Example The following statement drops the directory object `bfile_dir`:

```
DROP DIRECTORY bfile_dir;
```

Scripting on this page enhances content navigation, but does not change the content in any way.