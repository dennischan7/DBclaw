---
source: PostgreSQL 15 Reference
title: 00_Overview
---

At this writing, there are several limitations of the continuous archiving technique. These will probably be fixed in future releases:

- If a CREATE DATABASE command is executed while a base backup is being taken, and then the template database that the CREATE DATABASE copied is modified while the base backup is still in progress, it is possible that recovery will cause those modifications to be propagated into the created database as well. This is of course undesirable. To avoid this risk, it is best not to modify any template databases while taking a base backup.
- CREATE TABLESPACE commands are WAL-logged with the literal absolute path, and will therefore be replayed as tablespace creations with the same absolute path. This might be undesirable if the log is being replayed on a different machine. It can be dangerous even if the log is being replayed on the same machine, but into a new data directory: the replay will still overwrite the contents of the original tablespace. To avoid potential gotchas of this sort, the best practice is to take a new base backup after creating or dropping tablespaces.

It should also be noted that the default WAL format is fairly bulky since it includes many disk page snapshots. These page snapshots are designed to support crash recovery, since we might need to fix partially-written disk pages. Depending on your system hardware and software, the risk of partial writes might be small enough to ignore, in which case you can significantly reduce the total volume of archived logs by turning off page snapshots using the [full\\_page\\_writes](#page-45-0) parameter. (Read the notes and warnings in Chapter 30 before you do so.) Turning off page snapshots does not prevent use of the logs for PITR operations. An area for future development is to compress archived WAL data by removing unnecessary page copies even when full\_page\_writes is on. In the meantime, administrators

|  | interval parameters as much as feasible. |  |  |
|--|------------------------------------------|--|--|
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |
|  |                                          |  |  |