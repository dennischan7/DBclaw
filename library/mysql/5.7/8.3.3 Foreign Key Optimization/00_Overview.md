---
source: MySQL 5.7 Reference
title: 00_Overview
---

If a table has many columns, and you query many different combinations of columns, it might be efficient to split the less-frequently used data into separate tables with a few columns each, and relate them back to the main table by duplicating the numeric ID column from the main table. That way, each small table can have a primary key for fast lookups of its data, and you can query just the set of columns that you need using a join operation. Depending on how the data is distributed, the queries might perform less I/O and take up less cache memory because the relevant columns are packed together on disk. (To maximize performance, queries try to read as few data blocks as possible from disk; tables with only a few columns can fit more rows in each data block.)

## <span id="page-32-1"></span>**8.3.4 Column Indexes**

The most common type of index involves a single column, storing copies of the values from that column in a data structure, allowing fast lookups for the rows with the corresponding column values. The B-tree data structure lets the index quickly find a specific value, a set of values, or a range of values, corresponding to operators such as =, >, ≤, BETWEEN, IN, and so on, in a WHERE clause.

The maximum number of indexes per table and the maximum index length is defined per storage engine. See Chapter 14, The InnoDB Storage Engine, and Chapter 15, Alternative Storage Engines. All storage engines support at least 16 indexes per table and a total index length of at least 256 bytes. Most storage engines have higher limits.

For additional information about column indexes, see Section 13.1.14, "CREATE INDEX Statement".

- [Index Prefixes](#page-32-0)
- [FULLTEXT Indexes](#page-33-1)
- [Spatial Indexes](#page-33-2)
- [Indexes in the MEMORY Storage Engine](#page-33-3)

### <span id="page-32-0"></span>**Index Prefixes**

With col\_name(N) syntax in an index specification for a string column, you can create an index that uses only the first N characters of the column. Indexing only a prefix of column values in this way can make the index file much smaller. When you index a BLOB or TEXT column, you must specify a prefix length for the index. For example:

CREATE TABLE test (blob\_col BLOB, INDEX(blob\_col(10)));

Prefixes can be up to 1000 bytes long (767 bytes for InnoDB tables, unless you have innodb\_large\_prefix set).

![](_page_32_Picture_16.jpeg)

#### **Note**

Prefix limits are measured in bytes, whereas the prefix length in CREATE TABLE, ALTER TABLE, and CREATE INDEX statements is interpreted as number of characters for nonbinary string types (CHAR, VARCHAR, TEXT) and number of bytes for binary string types (BINARY, VARBINARY, BLOB). Take this into account when specifying a prefix length for a nonbinary string column that uses a multibyte character set.

If a search term exceeds the index prefix length, the index is used to exclude non-matching rows, and the remaining rows are examined for possible matches.

For additional information about index prefixes, see Section 13.1.14, "CREATE INDEX Statement".

### <span id="page-33-1"></span>**FULLTEXT Indexes**

FULLTEXT indexes are used for full-text searches. Only the InnoDB and MyISAM storage engines support FULLTEXT indexes and only for CHAR, VARCHAR, and TEXT columns. Indexing always takes place over the entire column and column prefix indexing is not supported. For details, see Section 12.9, "Full-Text Search Functions".

Optimizations are applied to certain kinds of FULLTEXT queries against single InnoDB tables. Queries with these characteristics are particularly efficient:

- FULLTEXT queries that only return the document ID, or the document ID and the search rank.
- FULLTEXT queries that sort the matching rows in descending order of score and apply a LIMIT clause to take the top N matching rows. For this optimization to apply, there must be no WHERE clauses and only a single ORDER BY clause in descending order.
- FULLTEXT queries that retrieve only the COUNT(\*) value of rows matching a search term, with no additional WHERE clauses. Code the WHERE clause as WHERE MATCH(text) AGAINST ('other\_text'), without any > 0 comparison operator.

For queries that contain full-text expressions, MySQL evaluates those expressions during the optimization phase of query execution. The optimizer does not just look at full-text expressions and make estimates, it actually evaluates them in the process of developing an execution plan.

An implication of this behavior is that EXPLAIN for full-text queries is typically slower than for non-fulltext queries for which no expression evaluation occurs during the optimization phase.

EXPLAIN for full-text queries may show Select tables optimized away in the Extra column due to matching occurring during optimization; in this case, no table access need occur during later execution.

### <span id="page-33-2"></span>**Spatial Indexes**

You can create indexes on spatial data types. MyISAM and InnoDB support R-tree indexes on spatial types. Other storage engines use B-trees for indexing spatial types (except for ARCHIVE, which does not support spatial type indexing).

### <span id="page-33-3"></span>**Indexes in the MEMORY Storage Engine**

The MEMORY storage engine uses HASH indexes by default, but also supports BTREE indexes.

# <span id="page-33-0"></span>**8.3.5 Multiple-Column Indexes**

MySQL can create composite indexes (that is, indexes on multiple columns). An index may consist of up to 16 columns. For certain data types, you can index a prefix of the column (see [Section 8.3.4,](#page-32-1) ["Column Indexes"\)](#page-32-1).

MySQL can use multiple-column indexes for queries that test all the columns in the index, or queries that test just the first column, the first two columns, the first three columns, and so on. If you specify the columns in the right order in the index definition, a single composite index can speed up several kinds of queries on the same table.

A multiple-column index can be considered a sorted array, the rows of which contain values that are created by concatenating the values of the indexed columns.

![](_page_33_Picture_18.jpeg)

#### **Note**

As an alternative to a composite index, you can introduce a column that is "hashed" based on information from other columns. If this column is short, reasonably unique, and indexed, it might be faster than a "wide" index on many columns. In MySQL, it is very easy to use this extra column:

```
SELECT * FROM tbl_name
 WHERE hash_col=MD5(CONCAT(val1,val2))
 AND col1=val1 AND col2=val2;
```

Suppose that a table has the following specification:

```
CREATE TABLE test (
 id INT NOT NULL,
 last_name CHAR(30) NOT NULL,
 first_name CHAR(30) NOT NULL,
 PRIMARY KEY (id),
 INDEX name (last_name,first_name)
);
```

The name index is an index over the last\_name and first\_name columns. The index can be used for lookups in queries that specify values in a known range for combinations of last\_name and first\_name values. It can also be used for queries that specify just a last\_name value because that column is a leftmost prefix of the index (as described later in this section). Therefore, the name index is used for lookups in the following queries:

```
SELECT * FROM test WHERE last_name='Jones';
SELECT * FROM test
 WHERE last_name='Jones' AND first_name='John';
SELECT * FROM test
 WHERE last_name='Jones'
 AND (first_name='John' OR first_name='Jon');
SELECT * FROM test
 WHERE last_name='Jones'
 AND first_name >='M' AND first_name < 'N';
```

However, the name index is not used for lookups in the following queries:

```
SELECT * FROM test WHERE first_name='John';
SELECT * FROM test
 WHERE last_name='Jones' OR first_name='John';
```

Suppose that you issue the following SELECT statement:

```
SELECT * FROM tbl_name
 WHERE col1=val1 AND col2=val2;
```

If a multiple-column index exists on col1 and col2, the appropriate rows can be fetched directly. If separate single-column indexes exist on col1 and col2, the optimizer attempts to use the Index Merge optimization (see Section 8.2.1.3, "Index Merge Optimization"), or attempts to find the most restrictive index by deciding which index excludes more rows and using that index to fetch the rows.

If the table has a multiple-column index, any leftmost prefix of the index can be used by the optimizer to look up rows. For example, if you have a three-column index on (col1, col2, col3), you have indexed search capabilities on (col1), (col1, col2), and (col1, col2, col3).

MySQL cannot use the index to perform lookups if the columns do not form a leftmost prefix of the index. Suppose that you have the SELECT statements shown here:

```
SELECT * FROM tbl_name WHERE col1=val1;
SELECT * FROM tbl_name WHERE col1=val1 AND col2=val2;
SELECT * FROM tbl_name WHERE col2=val2;
SELECT * FROM tbl_name WHERE col2=val2 AND col3=val3;
```

If an index exists on (col1, col2, col3), only the first two queries use the index. The third and fourth queries do involve indexed columns, but do not use an index to perform lookups because (col2) and (col2, col3) are not leftmost prefixes of (col1, col2, col3).