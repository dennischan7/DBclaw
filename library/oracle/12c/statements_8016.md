# Oracle 12c - statements_8016
Source: https://docs.oracle.com/database/121/SQLRF/statements_8016.htm

[Go to main content](#BEGIN)

471/555 

# DROP FLASHBACK ARCHIVE

Purpose

Use the `DROP` `FLASHBACK` `ARCHIVE` clause to remove a flashback data archive from the system. This statement removes the flashback data archive and all the historical data in it, but does not drop the tablespaces that were used by the flashback data archive.

Prerequisites

You must have the `FLASHBACK` `ARCHIVE` `ADMINISTER` system privilege to drop a flashback data archive.

Semantics

flashback\_archive

Specify the name of the flashback data archive you want to drop.

See Also:

[CREATE FLASHBACK ARCHIVE](statements_5011.md#BABIAECC)

for information on creating flashback data archives and for some simple examples of using flashback data archives

Scripting on this page enhances content navigation, but does not change the content in any way.