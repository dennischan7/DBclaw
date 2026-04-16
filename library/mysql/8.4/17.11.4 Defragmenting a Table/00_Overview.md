---
source: MySQL 8.4 Reference
title: 00_Overview
---

Random insertions into or deletions from a secondary index can cause the index to become fragmented. Fragmentation means that the physical ordering of the index pages on the disk is not close to the index ordering of the records on the pages, or that there are many unused pages in the 64-page blocks that were allocated to the index.

One symptom of fragmentation is that a table takes more space than it "should" take. How much that is exactly, is difficult to determine. All InnoDB data and indexes are stored in B-trees, and their fill factor may vary from 50% to 100%. Another symptom of fragmentation is that a table scan such as this takes more time than it "should" take:

```
SELECT COUNT(*) FROM t WHERE non_indexed_column <> 12345;
```

The preceding query requires MySQL to perform a full table scan, the slowest type of query for a large table.

To speed up index scans, you can periodically perform a "null" ALTER TABLE operation, which causes MySQL to rebuild the table:

ALTER TABLE tbl\_name ENGINE=INNODB

You can also use ALTER TABLE tbl\_name FORCE to perform a "null" alter operation that rebuilds the table.

Both ALTER TABLE tbl\_name ENGINE=INNODB and ALTER TABLE tbl\_name FORCE use [online](#page-151-0) [DDL](#page-151-0). For more information, see [Section 17.12, "InnoDB and Online DDL"](#page-151-0).

Another way to perform a defragmentation operation is to use mysqldump to dump the table to a text file, drop the table, and reload it from the dump file.

If the insertions into an index are always ascending and records are deleted only from the end, the InnoDB filespace management algorithm guarantees that fragmentation in the index does not occur.