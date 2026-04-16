---
source: MySQL 5.7 Reference
title: 00_Overview
---

Storage engines collect statistics about tables for use by the optimizer. Table statistics are based on value groups, where a value group is a set of rows with the same key prefix value. For optimizer purposes, an important statistic is the average value group size.

MySQL uses the average value group size in the following ways:

- To estimate how many rows must be read for each [ref](#page-74-3) access
- To estimate how many rows a partial join produces; that is, the number of rows that an operation of this form produces:

```
(...) JOIN tbl_name ON tbl_name.key = expr
```

As the average value group size for an index increases, the index is less useful for those two purposes because the average number of rows per lookup increases: For the index to be good for optimization purposes, it is best that each index value target a small number of rows in the table. When a given index value yields a large number of rows, the index is less useful and MySQL is less likely to use it.

The average value group size is related to table cardinality, which is the number of value groups. The SHOW INDEX statement displays a cardinality value based on N/S, where N is the number of rows in the table and S is the average value group size. That ratio yields an approximate number of value groups in the table.

For a join based on the <=> comparison operator, NULL is not treated differently from any other value: NULL <=> NULL, just as N <=> N for any other N.

However, for a join based on the = operator, NULL is different from non-NULL values: expr1 = expr2 is not true when expr1 or expr2 (or both) are NULL. This affects [ref](#page-74-3) accesses for comparisons of the form tbl\_name.key = expr: MySQL does not access the table if the current value of expr is NULL, because the comparison cannot be true.

For = comparisons, it does not matter how many NULL values are in the table. For optimization purposes, the relevant value is the average size of the non-NULL value groups. However, MySQL does not currently enable that average size to be collected or used.

For InnoDB and MyISAM tables, you have some control over collection of table statistics by means of the innodb\_stats\_method and myisam\_stats\_method system variables, respectively. These variables have three possible values, which differ as follows:

• When the variable is set to nulls\_equal, all NULL values are treated as identical (that is, they all form a single value group).

If the NULL value group size is much higher than the average non-NULL value group size, this method skews the average value group size upward. This makes index appear to the optimizer to be less useful than it really is for joins that look for non-NULL values. Consequently, the nulls\_equal method may cause the optimizer not to use the index for [ref](#page-74-3) accesses when it should.

• When the variable is set to nulls\_unequal, NULL values are not considered the same. Instead, each NULL value forms a separate value group of size 1.

If you have many NULL values, this method skews the average value group size downward. If the average non-NULL value group size is large, counting NULL values each as a group of size 1 causes the optimizer to overestimate the value of the index for joins that look for non-NULL values. Consequently, the nulls\_unequal method may cause the optimizer to use this index for [ref](#page-74-3) lookups when other methods may be better.

• When the variable is set to nulls\_ignored, NULL values are ignored.

If you tend to use many joins that use <=> rather than =, NULL values are not special in comparisons and one NULL is equal to another. In this case, nulls\_equal is the appropriate statistics method.

The innodb\_stats\_method system variable has a global value; the myisam\_stats\_method system variable has both global and session values. Setting the global value affects statistics collection for tables from the corresponding storage engine. Setting the session value affects statistics collection only for the current client connection. This means that you can force a table's statistics to be regenerated with a given method without affecting other clients by setting the session value of myisam\_stats\_method.

To regenerate MyISAM table statistics, you can use any of the following methods:

- Execute myisamchk --stats\_method=method\_name --analyze
- Change the table to cause its statistics to go out of date (for example, insert a row and then delete it), and then set myisam\_stats\_method and issue an ANALYZE TABLE statement

Some caveats regarding the use of innodb\_stats\_method and myisam\_stats\_method:

- You can force table statistics to be collected explicitly, as just described. However, MySQL may also collect statistics automatically. For example, if during the course of executing statements for a table, some of those statements modify the table, MySQL may collect statistics. (This may occur for bulk inserts or deletes, or some ALTER TABLE statements, for example.) If this happens, the statistics are collected using whatever value innodb\_stats\_method or myisam\_stats\_method has at the time. Thus, if you collect statistics using one method, but the system variable is set to the other method when a table's statistics are collected automatically later, the other method is used.
- There is no way to tell which method was used to generate statistics for a given table.
- These variables apply only to InnoDB and MyISAM tables. Other storage engines have only one method for collecting table statistics. Usually it is closer to the nulls\_equal method.

# <span id="page-36-0"></span>**8.3.8 Comparison of B-Tree and Hash Indexes**

Understanding the B-tree and hash data structures can help predict how different queries perform on different storage engines that use these data structures in their indexes, particularly for the MEMORY storage engine that lets you choose B-tree or hash indexes.

- [B-Tree Index Characteristics](#page-36-1)
- [Hash Index Characteristics](#page-37-0)

### <span id="page-36-1"></span>**B-Tree Index Characteristics**

A B-tree index can be used for column comparisons in expressions that use the =, >, >=, <, <=, or BETWEEN operators. The index also can be used for LIKE comparisons if the argument to LIKE is a constant string that does not start with a wildcard character. For example, the following SELECT statements use indexes:

```
SELECT * FROM tbl_name WHERE key_col LIKE 'Patrick%';
SELECT * FROM tbl_name WHERE key_col LIKE 'Pat%_ck%';
```

In the first statement, only rows with 'Patrick' <= key\_col < 'Patricl' are considered. In the second statement, only rows with 'Pat' <= key\_col < 'Pau' are considered.

The following SELECT statements do not use indexes:

```
SELECT * FROM tbl_name WHERE key_col LIKE '%Patrick%';
SELECT * FROM tbl_name WHERE key_col LIKE other_col;
```

In the first statement, the LIKE value begins with a wildcard character. In the second statement, the LIKE value is not a constant.

If you use ... LIKE '%string%' and string is longer than three characters, MySQL uses the Turbo Boyer-Moore algorithm to initialize the pattern for the string and then uses this pattern to perform the search more quickly.

A search using col\_name IS NULL employs indexes if col\_name is indexed.

Any index that does not span all AND levels in the WHERE clause is not used to optimize the query. In other words, to be able to use an index, a prefix of the index must be used in every AND group.

The following WHERE clauses use indexes:

```
... WHERE index_part1=1 AND index_part2=2 AND other_column=3
 /* index = 1 OR index = 2 */
... WHERE index=1 OR A=10 AND index=2
 /* optimized like "index_part1='hello'" */
... WHERE index_part1='hello' AND index_part3=5
 /* Can use index on index1 but not on index2 or index3 */
... WHERE index1=1 AND index2=2 OR index1=3 AND index3=3;
```

These WHERE clauses do not use indexes:

```
 /* index_part1 is not used */
... WHERE index_part2=1 AND index_part3=2
 /* Index is not used in both parts of the WHERE clause */
... WHERE index=1 OR A=10
 /* No index spans all rows */
... WHERE index_part1=1 OR index_part2=10
```

Sometimes MySQL does not use an index, even if one is available. One circumstance under which this occurs is when the optimizer estimates that using the index would require MySQL to access a very large percentage of the rows in the table. (In this case, a table scan is likely to be much faster because it requires fewer seeks.) However, if such a query uses LIMIT to retrieve only some of the rows, MySQL uses an index anyway, because it can much more quickly find the few rows to return in the result.

## <span id="page-37-0"></span>**Hash Index Characteristics**

Hash indexes have somewhat different characteristics from those just discussed:

- They are used only for equality comparisons that use the = or <=> operators (but are very fast). They are not used for comparison operators such as < that find a range of values. Systems that rely on this type of single-value lookup are known as "key-value stores"; to use MySQL for such applications, use hash indexes wherever possible.
- The optimizer cannot use a hash index to speed up ORDER BY operations. (This type of index cannot be used to search for the next entry in order.)
- MySQL cannot determine approximately how many rows there are between two values (this is used by the range optimizer to decide which index to use). This may affect some queries if you change a MyISAM or InnoDB table to a hash-indexed MEMORY table.
- Only whole keys can be used to search for a row. (With a B-tree index, any leftmost prefix of the key can be used to find rows.)

## <span id="page-38-0"></span>**8.3.9 Use of Index Extensions**

InnoDB automatically extends each secondary index by appending the primary key columns to it. Consider this table definition:

```
CREATE TABLE t1 (
 i1 INT NOT NULL DEFAULT 0,
 i2 INT NOT NULL DEFAULT 0,
 d DATE DEFAULT NULL,
 PRIMARY KEY (i1, i2),
 INDEX k_d (d)
) ENGINE = InnoDB;
```

This table defines the primary key on columns (i1, i2). It also defines a secondary index k\_d on column (d), but internally InnoDB extends this index and treats it as columns (d, i1, i2).

The optimizer takes into account the primary key columns of the extended secondary index when determining how and whether to use that index. This can result in more efficient query execution plans and better performance.

The optimizer can use extended secondary indexes for ref, range, and [index\\_merge](#page-88-4) index access, for Loose Index Scan access, for join and sorting optimization, and for MIN()/MAX() optimization.

The following example shows how execution plans are affected by whether the optimizer uses extended secondary indexes. Suppose that t1 is populated with these rows:

```
INSERT INTO t1 VALUES
(1, 1, '1998-01-01'), (1, 2, '1999-01-01'),
(1, 3, '2000-01-01'), (1, 4, '2001-01-01'),
(1, 5, '2002-01-01'), (2, 1, '1998-01-01'),
(2, 2, '1999-01-01'), (2, 3, '2000-01-01'),
(2, 4, '2001-01-01'), (2, 5, '2002-01-01'),
(3, 1, '1998-01-01'), (3, 2, '1999-01-01'),
(3, 3, '2000-01-01'), (3, 4, '2001-01-01'),
(3, 5, '2002-01-01'), (4, 1, '1998-01-01'),
(4, 2, '1999-01-01'), (4, 3, '2000-01-01'),
(4, 4, '2001-01-01'), (4, 5, '2002-01-01'),
(5, 1, '1998-01-01'), (5, 2, '1999-01-01'),
(5, 3, '2000-01-01'), (5, 4, '2001-01-01'),
(5, 5, '2002-01-01');
```

Now consider this query:

```
EXPLAIN SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01'
```

The execution plan depends on whether the extended index is used.

When the optimizer does not consider index extensions, it treats the index k\_d as only (d). EXPLAIN for the query produces this result:

```
mysql> EXPLAIN SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01'\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: t1
 type: ref
possible_keys: PRIMARY,k_d
 key: k_d
 key_len: 4
 ref: const
 rows: 5
 Extra: Using where; Using index
```

When the optimizer takes index extensions into account, it treats k\_d as (d, i1, i2). In this case, it can use the leftmost index prefix (d, i1) to produce a better execution plan:

```
mysql> EXPLAIN SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01'\G
```

```
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: t1
 type: ref
possible_keys: PRIMARY,k_d
 key: k_d
 key_len: 8
 ref: const,const
 rows: 1
 Extra: Using index
```

In both cases, key indicates that the optimizer uses secondary index k\_d but the EXPLAIN output shows these improvements from using the extended index:

- key\_len goes from 4 bytes to 8 bytes, indicating that key lookups use columns d and i1, not just d.
- The ref value changes from const to const,const because the key lookup uses two key parts, not one.
- The rows count decreases from 5 to 1, indicating that InnoDB should need to examine fewer rows to produce the result.
- The Extra value changes from Using where; Using index to Using index. This means that rows can be read using only the index, without consulting columns in the data row.

Differences in optimizer behavior for use of extended indexes can also be seen with SHOW STATUS:

```
FLUSH TABLE t1;
FLUSH STATUS;
SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01';
SHOW STATUS LIKE 'handler_read%'
```

The preceding statements include FLUSH TABLES and FLUSH STATUS to flush the table cache and clear the status counters.

Without index extensions, SHOW STATUS produces this result:

```
+-----------------------+-------+
| Variable_name | Value |
+-----------------------+-------+
| Handler_read_first | 0 |
| Handler_read_key | 1 |
| Handler_read_last | 0 |
| Handler_read_next | 5 |
| Handler_read_prev | 0 |
| Handler_read_rnd | 0 |
| Handler_read_rnd_next | 0 |
+-----------------------+-------+
```

With index extensions, SHOW STATUS produces this result. The Handler\_read\_next value decreases from 5 to 1, indicating more efficient use of the index:

```
+-----------------------+-------+
| Variable_name | Value |
+-----------------------+-------+
| Handler_read_first | 0 |
| Handler_read_key | 1 |
| Handler_read_last | 0 |
| Handler_read_next | 1 |
| Handler_read_prev | 0 |
| Handler_read_rnd | 0 |
| Handler_read_rnd_next | 0 |
+-----------------------+-------+
```

The [use\\_index\\_extensions](#page-87-1) flag of the optimizer\_switch system variable permits control over whether the optimizer takes the primary key columns into account when determining how to use an InnoDB table's secondary indexes. By default, [use\\_index\\_extensions](#page-87-1) is enabled. To check whether disabling use of index extensions improves performance, use this statement:

```
SET optimizer_switch = 'use_index_extensions=off';
```

Use of index extensions by the optimizer is subject to the usual limits on the number of key parts in an index (16) and the maximum key length (3072 bytes).