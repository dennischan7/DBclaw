# Oracle 11g - statements_1008
Source: https://docs.oracle.com/cd/E11882_01/server.112/e41084/statements_1008.htm

Prerequisites

You must have the `FLASHBACK` `ARCHIVE` `ADMINISTER` system privilege to alter a flashback data archive in any way. You must also have appropriate privileges on the affected tablespaces to add, modify, or remove a flashback data archive tablespace.

Semantics

flashback\_archive

Specify the name of an existing flashback data archive.

SET DEFAULT

You must be logged in as `SYSDBA` to specify this clause. Use this clause to designate this flashback data archive as the default flashback data archive for the system. When a `CREATE` `TABLE` or `ALTER` `TABLE` statement specifies the `flashback_archive_clause` without specifying a flashback data archive name, the database uses the default flashback data archive to store data from that table.

This statement overrides any previous designation of a different flashback data archive as the default.

ADD TABLESPACE

Use this clause to add a tablespace to the flashback data archive. You can use the `flashback_archive_quota` clause to specify the amount of space that can be used by the flashback data archive in the new tablespace. If you omit that clause, then the flashback data archive has unlimited space in the newly added tablespace.

MODIFY TABLESPACE

Use this clause to change the tablespace quota of a tablespace already used by the flashback data archive.

REMOVE TABLESPACE

Use this clause to remove a tablespace from use by the flashback data archive. You cannot remove the last remaining tablespace used by the flashback data archive.

If the tablespace to be removed contains any data within the retention period of the flashback archive, then that data will be dropped as well. Therefore, you should move your data to another tablespace before removing the tablespace with this clause.

MODIFY RETENTION

Use this clause to change the retention period of the flashback data archive.

PURGE

Use this clause to purge data from the flashback data archive.

* Specify `PURGE` `ALL` to remove all data from the flashback data archive. This historical information can be retrieved using a flashback query only if the SCN or timestamp specified in the flashback query is within the undo retention duration.
* Specify `PURGE` `BEFORE` `SCN` to remove all data from the flashback data archive before the specified system change number.
* Specify `PURGE` `BEFORE` `TIMESTAMP` to remove all data from the flashback data archive before the specified timestamp.

[NO] OPTIMIZE DATA

This clause has the same semantics as the [[NO] OPTIMIZE DATA](statements_5010.md#BGEBGFCA) clause of `CREATE` `FLASHBACK` `ARCHIVE`.

See Also:

[CREATE FLASHBACK ARCHIVE](statements_5010.md#BABIAECC)

for information on creating flashback data archives and for some simple examples of using flashback data archives