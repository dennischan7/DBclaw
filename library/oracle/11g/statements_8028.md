# Oracle 11g - statements_8028
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_8028.htm

[Go to main content](#BEGIN)

456/522 

# DROP RESTORE POINT

Purpose

Use the `DROP` `RESTORE` `POINT` statement to remove a normal restore point or a guaranteed restore point from the database.

* You need not drop normal restore points. The database automatically drops the oldest restore points when necessary, as described in the semantics for [restore\_point](statements_6011.md#BABEBBJC). However, you can drop a normal restore point if you want to reuse the name.
* Guaranteed restore points are not dropped automatically. Therefore, if you want to remove a guaranteed restore point from the database, then you must do so explicitly using this statement.

Prerequisites

To drop a normal restore point, you must have either the `SELECT` `ANY` `DICTIONARY` or the `FLASHBACK` `ANY` `TABLE` system privilege. To drop a guaranteed restore point, you must have the `SYSDBA` system privilege.

Semantics

restore\_point Specify the name of the restore point you want to drop.

Scripting on this page enhances content navigation, but does not change the content in any way.