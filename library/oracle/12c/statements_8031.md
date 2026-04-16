# Oracle 12c - statements_8031
Source: https://docs.oracle.com/database/121/SQLRF/statements_8031.htm

[Go to main content](#BEGIN)

486/555 

# DROP RESTORE POINT

Purpose

Use the `DROP` `RESTORE` `POINT` statement to remove a normal restore point or a guaranteed restore point from the database.

* You need not drop normal restore points. The database automatically drops the oldest restore points when necessary, as described in the semantics for [restore\_point](statements_6013.md#BABEBBJC). However, you can drop a normal restore point if you want to reuse the name.
* Guaranteed restore points are not dropped automatically. Therefore, if you want to remove a guaranteed restore point from the database, then you must do so explicitly using this statement.

Prerequisites

To drop a normal restore point, you must have the `SELECT` `ANY` `DICTIONARY`, `FLASHBACK` `ANY` `TABLE`, `SYSBACKUP`, or `SYSDG` system privilege. To drop a guaranteed restore point, you must have the `SYSDBA`, `SYSBACKUP`, or `SYSDG` system privilege.

Semantics

restore\_point Specify the name of the restore point you want to drop.

Scripting on this page enhances content navigation, but does not change the content in any way.