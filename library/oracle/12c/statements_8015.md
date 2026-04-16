# Oracle 12c - statements_8015
Source: https://docs.oracle.com/database/121/SQLRF/statements_8015.htm

[Go to main content](#BEGIN)

470/555 

# DROP EDITION

Purpose

Use the `DROP` `EDITION` statement to drop an edition, along with all actual editionable objects it contains. An actual editionable object is an editionable object that has been created or modified in an edition.

Prerequisites

You must have the `DROP` `ANY` `EDITION` system privilege, granted either directly or through a role.

Semantics

When successful, this statement drops the specified edition, including versions of any objects associated with that edition. Versions of the same objects in other editions are not dropped. Objects that are not editionable, or that are editionable but have not been actualized in the current edition, are not dropped.

You must specify `CASCADE` if the specified edition contains any actual editionable objects.

This statement is subject to the following conditions and restrictions:

* The specified edition cannot have both a parent edition and a child edition.
* The specified edition cannot contain any actual editionable objects that are inherited by a child edition, even if you specify `CASCADE`.
* `DROP` `EDITION` will fail if you attempt to drop the default edition.
* `DROP` `EDITION` will fail if you attempt to drop the root edition and the recycle bin contains at least one object that used to be in that edition before it was dropped. Under these circumstances, even `DROP` `EDITION` `CASCADE` will fail. In this case, you can purge all objects from the recycle bin with the `PURGE` `DBA_RECYCLEBIN` statement and then drop the edition. Refer to [PURGE](statements_9020.md#i2152611) for more information.

  `DROP` `EDITION` will also fail if you attempt to drop the leaf edition and the recycle bin contains at least one object that used to be in that edition before it was dropped. However, under these circumstances, `DROP` `EDITION` `CASCADE` will succeed.

  The only type of editioned object that might be in the recycle bin is a trigger.

Examples

For examples that use this statement, refer to [CREATE EDITION](statements_5010.md#BABGIFFD).

Scripting on this page enhances content navigation, but does not change the content in any way.