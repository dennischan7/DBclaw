---
source: PostgreSQL 14 Reference
title: 00_Overview
---

PostgreSQL's VACUUM command has to process each table on a regular basis for several reasons:

- 1. To recover or reuse disk space occupied by updated or deleted rows.
- 2. To update data statistics used by the PostgreSQL query planner.
- 3. To update the visibility map, which speeds up index-only scans.
- 4. To protect against loss of very old data due to *transaction ID wraparound* or *multixact ID wraparound*.

Each of these reasons dictates performing VACUUM operations of varying frequency and scope, as explained in the following subsections.

<sup>1</sup> [https://bucardo.org/check\\_postgres/](https://bucardo.org/check_postgres/)

There are two variants of VACUUM: standard VACUUM and VACUUM FULL. VACUUM FULL can reclaim more disk space but runs much more slowly. Also, the standard form of VACUUM can run in parallel with production database operations. (Commands such as SELECT, INSERT, UPDATE, and DELETE will continue to function normally, though you will not be able to modify the definition of a table with commands such as ALTER TABLE while it is being vacuumed.) VACUUM FULL requires an ACCESS EXCLUSIVE lock on the table it is working on, and therefore cannot be done in parallel with other use of the table. Generally, therefore, administrators should strive to use standard VACUUM and avoid VACUUM FULL.

VACUUM creates a substantial amount of I/O traffic, which can cause poor performance for other active sessions. There are configuration parameters that can be adjusted to reduce the performance impact of background vacuuming — see [Section 20.4.4.](#page-32-1)