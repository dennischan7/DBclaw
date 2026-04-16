---
source: MySQL 8.4 Reference
title: 00_Overview
---

# <span id="page-176-0"></span>**19.5.1 Replication Features and Issues**

The following sections provide information about what is supported and what is not in MySQL replication, and about specific issues and situations that may occur when replicating certain statements.

Statement-based replication depends on compatibility at the SQL level between the source and replica. In other words, successful statement-based replication requires that any SQL features used be supported by both the source and the replica servers. If you use a feature on the source server that is available only in the current version of MySQL, you cannot replicate to a replica that uses an earlier version of MySQL. Such incompatibilities can also occur within a release series as well as between versions.

If you are planning to use statement-based replication between MySQL 8.4 and a previous MySQL release series, it is a good idea to consult the edition of the MySQL Reference Manual corresponding to the earlier release series for information regarding the replication characteristics of that series.

With MySQL's statement-based replication, there may be issues with replicating stored routines or triggers. You can avoid these issues by using MySQL's row-based replication instead. For a detailed list of issues, see Section 27.7, "Stored Program Binary Logging". For more information about row-based logging and row-based replication, see Section 7.4.4.1, "Binary Logging Formats", and [Section 19.2.1, "Replication Formats"](#page-110-0).

For additional information specific to replication and InnoDB, see Section 17.19, "InnoDB and MySQL Replication". For information relating to replication with NDB Cluster, see Section 25.7, "NDB Cluster Replication".

## <span id="page-177-0"></span>**19.5.1.1 Replication and AUTO\_INCREMENT**

Statement-based replication of AUTO\_INCREMENT, LAST\_INSERT\_ID(), and TIMESTAMP values is carried out subject to the following exceptions:

- A statement invoking a trigger or function that causes an update to an AUTO\_INCREMENT column is not replicated correctly using statement-based replication. These statements are marked as unsafe. (Bug #45677)
- An INSERT into a table that has a composite primary key that includes an AUTO\_INCREMENT column that is not the first column of this composite key is not safe for statement-based logging or replication. These statements are marked as unsafe. (Bug #11754117, Bug #45670)

This issue does not affect tables using the InnoDB storage engine, since an InnoDB table with an AUTO\_INCREMENT column requires at least one key where the auto-increment column is the only or leftmost column.

• Adding an AUTO\_INCREMENT column to a table with ALTER TABLE might not produce the same ordering of the rows on the replica and the source. This occurs because the order in which the rows are numbered depends on the specific storage engine used for the table and the order in which the rows were inserted. If it is important to have the same order on the source and replica, the rows must be ordered before assigning an AUTO\_INCREMENT number. Assuming that you want to add an AUTO\_INCREMENT column to a table t1 that has columns col1 and col2, the following statements produce a new table t2 identical to t1 but with an AUTO\_INCREMENT column:

```
CREATE TABLE t2 LIKE t1;
ALTER TABLE t2 ADD id INT AUTO_INCREMENT PRIMARY KEY;
INSERT INTO t2 SELECT * FROM t1 ORDER BY col1, col2;
```

![](_page_177_Picture_13.jpeg)

#### **Important**

To guarantee the same ordering on both source and replica, the ORDER BY clause must name all columns of t1.

The instructions just given are subject to the limitations of CREATE TABLE ... LIKE: Foreign key definitions are ignored, as are the DATA DIRECTORY and INDEX DIRECTORY table options. If a

table definition includes any of those characteristics, create t2 using a CREATE TABLE statement that is identical to the one used to create t1, but with the addition of the AUTO\_INCREMENT column.

Regardless of the method used to create and populate the copy having the AUTO\_INCREMENT column, the final step is to drop the original table and then rename the copy:

```
DROP t1;
ALTER TABLE t2 RENAME t1;
```

See also Section B.3.6.1, "Problems with ALTER TABLE".