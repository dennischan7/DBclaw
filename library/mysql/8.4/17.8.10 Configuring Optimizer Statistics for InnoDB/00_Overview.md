---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section describes how to configure persistent and non-persistent optimizer statistics for InnoDB tables.

Persistent optimizer statistics are persisted across server restarts, allowing for greater plan stability and more consistent query performance. Persistent optimizer statistics also provide control and flexibility with these additional benefits:

- You can use the innodb\_stats\_auto\_recalc configuration option to control whether statistics are updated automatically after substantial changes to a table.
- You can use the STATS\_PERSISTENT, STATS\_AUTO\_RECALC, and STATS\_SAMPLE\_PAGES clauses with CREATE TABLE and ALTER TABLE statements to configure optimizer statistics for individual tables.
- You can query optimizer statistics data in the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables.
- You can view the last\_update column of the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables to see when statistics were last updated.
- You can manually modify the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables to force a specific query optimization plan or to test alternative plans without modifying the database.

The persistent optimizer statistics feature is enabled by default (innodb\_stats\_persistent=ON).

Non-persistent optimizer statistics are cleared on each server restart and after some other operations, and recomputed on the next table access. As a result, different estimates could be produced when recomputing statistics, leading to different choices in execution plans and variations in query performance.

This section also provides information about estimating ANALYZE TABLE complexity, which may be useful when attempting to achieve a balance between accurate statistics and ANALYZE TABLE execution time.

# <span id="page-110-0"></span>**17.8.10.1 Configuring Persistent Optimizer Statistics Parameters**

The persistent optimizer statistics feature improves plan stability by storing statistics to disk and making them persistent across server restarts so that the optimizer is more likely to make consistent choices each time for a given query.

Optimizer statistics are persisted to disk when innodb\_stats\_persistent=ON or when individual tables are defined with STATS\_PERSISTENT=1. innodb\_stats\_persistent is enabled by default.

Formerly, optimizer statistics were cleared when restarting the server and after some other types of operations, and recomputed on the next table access. Consequently, different estimates could be produced when recalculating statistics leading to different choices in query execution plans and variation in query performance.

Persistent statistics are stored in the mysql.innodb\_table\_stats and mysql.innodb\_index\_stats tables. See [InnoDB Persistent Statistics Tables.](#page-112-0)

If you prefer not to persist optimizer statistics to disk, see [Section 17.8.10.2, "Configuring Non-](#page-117-0)[Persistent Optimizer Statistics Parameters"](#page-117-0)

### **Configuring Automatic Statistics Calculation for Persistent Optimizer Statistics**

The innodb\_stats\_auto\_recalc variable, which is enabled by default, controls whether statistics are calculated automatically when a table undergoes changes to more than 10% of its rows. You can also configure automatic statistics recalculation for individual tables by specifying the STATS\_AUTO\_RECALC clause when creating or altering a table.

Because of the asynchronous nature of automatic statistics recalculation, which occurs in the background, statistics may not be recalculated instantly after running a DML operation that affects more than 10% of a table, even when innodb\_stats\_auto\_recalc is enabled. Statistics recalculation can be delayed by few seconds in some cases. If up-to-date statistics are required immediately, run ANALYZE TABLE to initiate a synchronous (foreground) recalculation of statistics. If innodb\_stats\_auto\_recalc is disabled, you can ensure the accuracy of optimizer statistics by executing the ANALYZE TABLE statement after making substantial changes to indexed columns. You might also consider adding ANALYZE TABLE to setup scripts that you run after loading data, and running ANALYZE TABLE on a schedule at times of low activity.

When an index is added to an existing table, or when a column is added or dropped, index statistics are calculated and added to the innodb\_index\_stats table regardless of the value of innodb\_stats\_auto\_recalc.

For a histogram with AUTO UPDATE enabled (see Histogram Statistics Analysis), automatic recalculation of persistent statistics also causes the histogram to be updated.

## **Configuring Optimizer Statistics Parameters for Individual Tables**

innodb\_stats\_persistent, innodb\_stats\_auto\_recalc, and innodb\_stats\_persistent\_sample\_pages are global variables. To override these systemwide settings and configure optimizer statistics parameters for individual tables, you can define STATS\_PERSISTENT, STATS\_AUTO\_RECALC, and STATS\_SAMPLE\_PAGES clauses in CREATE TABLE or ALTER TABLE statements.

- STATS\_PERSISTENT specifies whether to enable persistent statistics for an InnoDB table. The value DEFAULT causes the persistent statistics setting for the table to be determined by the innodb\_stats\_persistent setting. A value of 1 enables persistent statistics for the table, while a value of 0 disables the feature. After enabling persistent statistics for an individual table, use ANALYZE TABLE to calculate statistics after table data is loaded.
- STATS\_AUTO\_RECALC specifies whether to automatically recalculate persistent statistics. The value DEFAULT causes the persistent statistics setting for the table to be determined by the innodb\_stats\_auto\_recalc setting. A value of 1 causes statistics to be recalculated when 10% of table data has changed. A value 0 prevents automatic recalculation for the table. When using a value of 0, use ANALYZE TABLE to recalculate statistics after making substantial changes to the table.
- STATS\_SAMPLE\_PAGES specifies the number of index pages to sample when cardinality and other statistics are calculated for an indexed column, by an ANALYZE TABLE operation, for example.

All three clauses are specified in the following CREATE TABLE example:

```
CREATE TABLE `t1` (
`id` int(8) NOT NULL auto_increment,
`data` varchar(255),
`date` datetime,
PRIMARY KEY (`id`),
INDEX `DATE_IX` (`date`)
) ENGINE=InnoDB,
 STATS_PERSISTENT=1,
 STATS_AUTO_RECALC=1,
 STATS_SAMPLE_PAGES=25;
```

### **Configuring the Number of Sampled Pages for InnoDB Optimizer Statistics**

The optimizer uses estimated statistics about key distributions to choose the indexes for an execution plan, based on the relative selectivity of the index. Operations such as ANALYZE TABLE cause InnoDB to sample random pages from each index on a table to estimate the cardinality of the index. This sampling technique is known as a random dive.

The innodb\_stats\_persistent\_sample\_pages controls the number of sampled pages. You can adjust the setting at runtime to manage the quality of statistics estimates used by the optimizer. The default value is 20. Consider modifying the setting when encountering the following issues:

1. Statistics are not accurate enough and the optimizer chooses suboptimal plans, as shown in EXPLAIN output. You can check the accuracy of statistics by comparing the actual cardinality of an index (determined by running SELECT DISTINCT on the index columns) with the estimates in the mysql.innodb\_index\_stats table.

If it is determined that statistics are not accurate enough, the value of innodb\_stats\_persistent\_sample\_pages should be increased until the statistics estimates are sufficiently accurate. Increasing innodb\_stats\_persistent\_sample\_pages too much, however, could cause ANALYZE TABLE to run slowly.

2. ANALYZE TABLE is too slow. In this case innodb\_stats\_persistent\_sample\_pages should be decreased until ANALYZE TABLE execution time is acceptable. Decreasing the value too much, however, could lead to the first problem of inaccurate statistics and suboptimal query execution plans.

If a balance cannot be achieved between accurate statistics and ANALYZE TABLE execution time, consider decreasing the number of indexed columns in the table or limiting the number of partitions to reduce ANALYZE TABLE complexity. The number of columns in the table's primary key is also important to consider, as primary key columns are appended to each nonunique index.

For related information, see [Section 17.8.10.3, "Estimating ANALYZE TABLE Complexity for](#page-118-0) [InnoDB Tables"](#page-118-0).

### **Including Delete-marked Records in Persistent Statistics Calculations**

By default, InnoDB reads uncommitted data when calculating statistics. In the case of an uncommitted transaction that deletes rows from a table, delete-marked records are excluded when calculating row estimates and index statistics, which can lead to non-optimal execution plans for other transactions that are operating on the table concurrently using a transaction isolation level other than [READ](#page-65-2) [UNCOMMITTED](#page-65-2). To avoid this scenario, innodb\_stats\_include\_delete\_marked can be enabled to ensure that delete-marked records are included when calculating persistent optimizer statistics.

When innodb\_stats\_include\_delete\_marked is enabled, ANALYZE TABLE considers deletemarked records when recalculating statistics.

innodb\_stats\_include\_delete\_marked is a global setting that affects all InnoDB tables, and it is only applicable to persistent optimizer statistics.

# <span id="page-112-0"></span>**InnoDB Persistent Statistics Tables**

The persistent statistics feature relies on the internally managed tables in the mysql database, named innodb\_table\_stats and innodb\_index\_stats. These tables are set up automatically in all install, upgrade, and build-from-source procedures.

**Table 17.6 Columns of innodb\_table\_stats**

| Column name              | Description                                                          |
|--------------------------|----------------------------------------------------------------------|
| database_name            | Database name                                                        |
| table_name               | Table name, partition name, or subpartition name                     |
| last_update              | A timestamp indicating the last time that InnoDB<br>updated this row |
| n_rows                   | The number of rows in the table                                      |
| clustered_index_size     | The size of the primary index, in pages                              |
| sum_of_other_index_sizes | The total size of other (non-primary) indexes, in<br>pages           |

**Table 17.7 Columns of innodb\_index\_stats**

| Column name   | Description   |  |
|---------------|---------------|--|
| database_name | Database name |  |

| Column name      | Description                                                                       |
|------------------|-----------------------------------------------------------------------------------|
| table_name       | Table name, partition name, or subpartition name                                  |
| index_name       | Index name                                                                        |
| last_update      | A timestamp indicating the last time the row was<br>updated                       |
| stat_name        | The name of the statistic, whose value is reported<br>in the stat_value column    |
| stat_value       | The value of the statistic that is named in<br>stat_name column                   |
| sample_size      | The number of pages sampled for the estimate<br>provided in the stat_value column |
| stat_description | Description of the statistic that is named in the<br>stat_name column             |

The innodb\_table\_stats and innodb\_index\_stats tables include a last\_update column that shows when index statistics were last updated:

```
mysql> SELECT * FROM innodb_table_stats \G
*************************** 1. row ***************************
 database_name: sakila
 table_name: actor
 last_update: 2014-05-28 16:16:44
 n_rows: 200
 clustered_index_size: 1
sum_of_other_index_sizes: 1
...
```

```
mysql> SELECT * FROM innodb_index_stats \G
*************************** 1. row ***************************
 database_name: sakila
 table_name: actor
 index_name: PRIMARY
 last_update: 2014-05-28 16:16:44
 stat_name: n_diff_pfx01
 stat_value: 200
 sample_size: 1
 ...
```

The innodb\_table\_stats and innodb\_index\_stats tables can be updated manually, which makes it possible to force a specific query optimization plan or test alternative plans without modifying the database. If you manually update statistics, use the FLUSH TABLE tbl\_name statement to load the updated statistics.

Persistent statistics are considered local information, because they relate to the server instance. The innodb\_table\_stats and innodb\_index\_stats tables are therefore not replicated when automatic statistics recalculation takes place. If you run ANALYZE TABLE to initiate a synchronous recalculation of statistics, the statement is replicated (unless you suppressed logging for it), and recalculation takes place on replicas.

# <span id="page-113-0"></span>**InnoDB Persistent Statistics Tables Example**

The innodb\_table\_stats table contains one row for each table. The following example demonstrates the type of data collected.

Table t1 contains a primary index (columns a, b) secondary index (columns c, d), and unique index (columns e, f):

```
CREATE TABLE t1 (
a INT, b INT, c INT, d INT, e INT, f INT,
PRIMARY KEY (a, b), KEY i1 (c, d), UNIQUE KEY i2uniq (e, f)
) ENGINE=INNODB;
```

After inserting five rows of sample data, table t1 appears as follows:

```
mysql> SELECT * FROM t1;
+---+---+------+------+------+------+
| a | b | c | d | e | f |
+---+---+------+------+------+------+
| 1 | 1 | 10 | 11 | 100 | 101 |
| 1 | 2 | 10 | 11 | 200 | 102 |
| 1 | 3 | 10 | 11 | 100 | 103 |
| 1 | 4 | 10 | 12 | 200 | 104 |
| 1 | 5 | 10 | 12 | 100 | 105 |
+---+---+------+------+------+------+
```

To immediately update statistics, run ANALYZE TABLE (if innodb\_stats\_auto\_recalc is enabled, statistics are updated automatically within a few seconds assuming that the 10% threshold for changed table rows is reached):

```
mysql> ANALYZE TABLE t1;
+---------+---------+----------+----------+
| Table | Op | Msg_type | Msg_text |
+---------+---------+----------+----------+
| test.t1 | analyze | status | OK |
+---------+---------+----------+----------+
```

Table statistics for table t1 show the last time InnoDB updated the table statistics (2014-03-14 14:36:34), the number of rows in the table (5), the clustered index size (1 page), and the combined size of the other indexes (2 pages).

```
mysql> SELECT * FROM mysql.innodb_table_stats WHERE table_name like 't1'\G
*************************** 1. row ***************************
 database_name: test
 table_name: t1
 last_update: 2014-03-14 14:36:34
 n_rows: 5
 clustered_index_size: 1
sum_of_other_index_sizes: 2
```

The innodb\_index\_stats table contains multiple rows for each index. Each row in the innodb\_index\_stats table provides data related to a particular index statistic which is named in the stat\_name column and described in the stat\_description column. For example:

```
mysql> SELECT index_name, stat_name, stat_value, stat_description
 FROM mysql.innodb_index_stats WHERE table_name like 't1';
+------------+--------------+------------+-----------------------------------+
| index_name | stat_name | stat_value | stat_description |
+------------+--------------+------------+-----------------------------------+
| PRIMARY | n_diff_pfx01 | 1 | a |
| PRIMARY | n_diff_pfx02 | 5 | a,b |
| PRIMARY | n_leaf_pages | 1 | Number of leaf pages in the index |
| PRIMARY | size | 1 | Number of pages in the index |
| i1 | n_diff_pfx01 | 1 | c |
| i1 | n_diff_pfx02 | 2 | c,d |
| i1 | n_diff_pfx03 | 2 | c,d,a |
| i1 | n_diff_pfx04 | 5 | c,d,a,b |
| i1 | n_leaf_pages | 1 | Number of leaf pages in the index |
| i1 | size | 1 | Number of pages in the index |
| i2uniq | n_diff_pfx01 | 2 | e |
| i2uniq | n_diff_pfx02 | 5 | e,f |
| i2uniq | n_leaf_pages | 1 | Number of leaf pages in the index |
| i2uniq | size | 1 | Number of pages in the index |
+------------+--------------+------------+-----------------------------------+
```

The stat\_name column shows the following types of statistics:

- size: Where stat\_name=size, the stat\_value column displays the total number of pages in the index.
- n\_leaf\_pages: Where stat\_name=n\_leaf\_pages, the stat\_value column displays the number of leaf pages in the index.

• n\_diff\_pfxNN: Where stat\_name=n\_diff\_pfx01, the stat\_value column displays the number of distinct values in the first column of the index. Where stat\_name=n\_diff\_pfx02, the stat\_value column displays the number of distinct values in the first two columns of the index, and so on. Where stat\_name=n\_diff\_pfxNN, the stat\_description column shows a comma separated list of the index columns that are counted.

To further illustrate the n\_diff\_pfxNN statistic, which provides cardinality data, consider once again the t1 table example that was introduced previously. As shown below, the t1 table is created with a primary index (columns a, b), a secondary index (columns c, d), and a unique index (columns e, f):

```
CREATE TABLE t1 (
 a INT, b INT, c INT, d INT, e INT, f INT,
 PRIMARY KEY (a, b), KEY i1 (c, d), UNIQUE KEY i2uniq (e, f)
) ENGINE=INNODB;
```

After inserting five rows of sample data, table t1 appears as follows:

```
mysql> SELECT * FROM t1;
+---+---+------+------+------+------+
| a | b | c | d | e | f |
+---+---+------+------+------+------+
| 1 | 1 | 10 | 11 | 100 | 101 |
| 1 | 2 | 10 | 11 | 200 | 102 |
| 1 | 3 | 10 | 11 | 100 | 103 |
| 1 | 4 | 10 | 12 | 200 | 104 |
| 1 | 5 | 10 | 12 | 100 | 105 |
+---+---+------+------+------+------+
```

When you query the index\_name, stat\_name, stat\_value, and stat\_description, where stat\_name LIKE 'n\_diff%', the following result set is returned:

```
mysql> SELECT index_name, stat_name, stat_value, stat_description
 FROM mysql.innodb_index_stats
 WHERE table_name like 't1' AND stat_name LIKE 'n_diff%';
+------------+--------------+------------+------------------+
| index_name | stat_name | stat_value | stat_description |
+------------+--------------+------------+------------------+
| PRIMARY | n_diff_pfx01 | 1 | a |
| PRIMARY | n_diff_pfx02 | 5 | a,b |
| i1 | n_diff_pfx01 | 1 | c |
| i1 | n_diff_pfx02 | 2 | c,d |
| i1 | n_diff_pfx03 | 2 | c,d,a |
| i1 | n_diff_pfx04 | 5 | c,d,a,b |
| i2uniq | n_diff_pfx01 | 2 | e |
| i2uniq | n_diff_pfx02 | 5 | e,f |
+------------+--------------+------------+------------------+
```

For the PRIMARY index, there are two n\_diff% rows. The number of rows is equal to the number of columns in the index.

![](_page_115_Picture_9.jpeg)

#### **Note**

For nonunique indexes, InnoDB appends the columns of the primary key.

- Where index\_name=PRIMARY and stat\_name=n\_diff\_pfx01, the stat\_value is 1, which indicates that there is a single distinct value in the first column of the index (column a). The number of distinct values in column a is confirmed by viewing the data in column a in table t1, in which there is a single distinct value (1). The counted column (a) is shown in the stat\_description column of the result set.
- Where index\_name=PRIMARY and stat\_name=n\_diff\_pfx02, the stat\_value is 5, which indicates that there are five distinct values in the two columns of the index (a,b). The number of distinct values in columns a and b is confirmed by viewing the data in columns a and b in table t1, in which there are five distinct values: (1,1), (1,2), (1,3), (1,4) and (1,5). The counted columns (a,b) are shown in the stat\_description column of the result set.

For the secondary index (i1), there are four n\_diff% rows. Only two columns are defined for the secondary index (c,d) but there are four n\_diff% rows for the secondary index because InnoDB suffixes all nonunique indexes with the primary key. As a result, there are four n\_diff% rows instead of two to account for the both the secondary index columns (c,d) and the primary key columns (a,b).

- Where index\_name=i1 and stat\_name=n\_diff\_pfx01, the stat\_value is 1, which indicates that there is a single distinct value in the first column of the index (column c). The number of distinct values in column c is confirmed by viewing the data in column c in table t1, in which there is a single distinct value: (10). The counted column (c) is shown in the stat\_description column of the result set.
- Where index\_name=i1 and stat\_name=n\_diff\_pfx02, the stat\_value is 2, which indicates that there are two distinct values in the first two columns of the index (c,d). The number of distinct values in columns c an d is confirmed by viewing the data in columns c and d in table t1, in which there are two distinct values: (10,11) and (10,12). The counted columns (c,d) are shown in the stat\_description column of the result set.
- Where index\_name=i1 and stat\_name=n\_diff\_pfx03, the stat\_value is 2, which indicates that there are two distinct values in the first three columns of the index (c,d,a). The number of distinct values in columns c, d, and a is confirmed by viewing the data in column c, d, and a in table t1, in which there are two distinct values: (10,11,1) and (10,12,1). The counted columns (c,d,a) are shown in the stat\_description column of the result set.
- Where index\_name=i1 and stat\_name=n\_diff\_pfx04, the stat\_value is 5, which indicates that there are five distinct values in the four columns of the index (c,d,a,b). The number of distinct values in columns c, d, a and b is confirmed by viewing the data in columns c, d, a, and b in table t1, in which there are five distinct values: (10,11,1,1), (10,11,1,2), (10,11,1,3), (10,12,1,4), and (10,12,1,5). The counted columns (c,d,a,b) are shown in the stat\_description column of the result set.

For the unique index (i2uniq), there are two n\_diff% rows.

- Where index\_name=i2uniq and stat\_name=n\_diff\_pfx01, the stat\_value is 2, which indicates that there are two distinct values in the first column of the index (column e). The number of distinct values in column e is confirmed by viewing the data in column e in table t1, in which there are two distinct values: (100) and (200). The counted column (e) is shown in the stat\_description column of the result set.
- Where index\_name=i2uniq and stat\_name=n\_diff\_pfx02, the stat\_value is 5, which indicates that there are five distinct values in the two columns of the index (e,f). The number of distinct values in columns e and f is confirmed by viewing the data in columns e and f in table t1, in which there are five distinct values: (100,101), (200,102), (100,103), (200,104), and (100,105). The counted columns (e,f) are shown in the stat\_description column of the result set.

### **Retrieving Index Size Using the innodb\_index\_stats Table**

You can retrieve the index size for tables, partitions, or subpartitions can using the innodb\_index\_stats table. In the following example, index sizes are retrieved for table t1. For a definition of table t1 and corresponding index statistics, see [InnoDB Persistent Statistics Tables](#page-113-0) [Example.](#page-113-0)

```
mysql> SELECT SUM(stat_value) pages, index_name,
 SUM(stat_value)*@@innodb_page_size size
 FROM mysql.innodb_index_stats WHERE table_name='t1'
 AND stat_name = 'size' GROUP BY index_name;
+-------+------------+-------+
| pages | index_name | size |
+-------+------------+-------+
| 1 | PRIMARY | 16384 |
| 1 | i1 | 16384 |
| 1 | i2uniq | 16384 |
+-------+------------+-------+
```

For partitions or subpartitions, you can use the same query with a modified WHERE clause to retrieve index sizes. For example, the following query retrieves index sizes for partitions of table t1:

```
mysql> SELECT SUM(stat_value) pages, index_name,
 SUM(stat_value)*@@innodb_page_size size
 FROM mysql.innodb_index_stats WHERE table_name like 't1#P%'
 AND stat_name = 'size' GROUP BY index_name;
```

# <span id="page-117-0"></span>**17.8.10.2 Configuring Non-Persistent Optimizer Statistics Parameters**

This section describes how to configure non-persistent optimizer statistics. Optimizer statistics are not persisted to disk when innodb\_stats\_persistent=OFF or when individual tables are created or altered with STATS\_PERSISTENT=0. Instead, statistics are stored in memory, and are lost when the server is shut down. Statistics are also updated periodically by certain operations and under certain conditions.

Optimizer statistics are persisted to disk by default, enabled by the innodb\_stats\_persistent configuration option. For information about persistent optimizer statistics, see [Section 17.8.10.1,](#page-110-0) ["Configuring Persistent Optimizer Statistics Parameters".](#page-110-0)

### **Optimizer Statistics Updates**

Non-persistent optimizer statistics are updated when:

- Running ANALYZE TABLE.
- Running SHOW TABLE STATUS, SHOW INDEX, or querying the Information Schema TABLES or STATISTICS tables with the innodb\_stats\_on\_metadata option enabled.

The default setting for innodb\_stats\_on\_metadata is OFF. Enabling innodb\_stats\_on\_metadata may reduce access speed for schemas that have a large number of tables or indexes, and reduce stability of execution plans for queries that involve InnoDB tables. innodb\_stats\_on\_metadata is configured globally using a SET statement.

SET GLOBAL innodb\_stats\_on\_metadata=ON

![](_page_117_Picture_12.jpeg)

### **Note**

innodb\_stats\_on\_metadata only applies when optimizer statistics are configured to be non-persistent (when innodb\_stats\_persistent is disabled).

• Starting a mysql client with the --auto-rehash option enabled, which is the default. The autorehash option causes all InnoDB tables to be opened, and the open table operations cause statistics to be recalculated.

To improve the start up time of the mysql client and to updating statistics, you can turn off autorehash using the --disable-auto-rehash option. The auto-rehash feature enables automatic name completion of database, table, and column names for interactive users.

- A table is first opened.
- InnoDB detects that 1 / 16 of table has been modified since the last time statistics were updated.

### **Configuring the Number of Sampled Pages**

The MySQL query optimizer uses estimated statistics about key distributions to choose the indexes for an execution plan, based on the relative selectivity of the index. When InnoDB updates optimizer statistics, it samples random pages from each index on a table to estimate the cardinality of the index. (This technique is known as random dives.)

To give you control over the quality of the statistics estimate (and thus better information for the query optimizer), you can change the number of sampled pages using the parameter

innodb\_stats\_transient\_sample\_pages. The default number of sampled pages is 8, which could be insufficient to produce an accurate estimate, leading to poor index choices by the query optimizer. This technique is especially important for large tables and tables used in joins. Unnecessary full table scans for such tables can be a substantial performance issue. See Section 10.2.1.23, "Avoiding Full Table Scans" for tips on tuning such queries. innodb\_stats\_transient\_sample\_pages is a global parameter that can be set at runtime.

The value of innodb\_stats\_transient\_sample\_pages affects the index sampling for all InnoDB tables and indexes when innodb\_stats\_persistent=0. Be aware of the following potentially significant impacts when you change the index sample size:

- Small values like 1 or 2 can result in inaccurate estimates of cardinality.
- Increasing the innodb\_stats\_transient\_sample\_pages value might require more disk reads. Values much larger than 8 (say, 100), can cause a significant slowdown in the time it takes to open a table or execute SHOW TABLE STATUS.
- The optimizer might choose very different query plans based on different estimates of index selectivity.

Whatever value of innodb\_stats\_transient\_sample\_pages works best for a system, set the option and leave it at that value. Choose a value that results in reasonably accurate estimates for all tables in your database without requiring excessive I/O. Because the statistics are automatically recalculated at various times other than on execution of ANALYZE TABLE, it does not make sense to increase the index sample size, run ANALYZE TABLE, then decrease sample size again.

Smaller tables generally require fewer index samples than larger tables. If your database has many large tables, consider using a higher value for innodb\_stats\_transient\_sample\_pages than if you have mostly smaller tables.

# <span id="page-118-0"></span>**17.8.10.3 Estimating ANALYZE TABLE Complexity for InnoDB Tables**

ANALYZE TABLE complexity for InnoDB tables is dependent on:

- The number of pages sampled, as defined by innodb\_stats\_persistent\_sample\_pages.
- The number of indexed columns in a table
- The number of partitions. If a table has no partitions, the number of partitions is considered to be 1.

Using these parameters, an approximate formula for estimating ANALYZE TABLE complexity would be:

The value of innodb\_stats\_persistent\_sample\_pages \* number of indexed columns in a table \* the number of partitions

Typically, the greater the resulting value, the greater the execution time for ANALYZE TABLE.

![](_page_118_Picture_16.jpeg)

# **Note**

innodb\_stats\_persistent\_sample\_pages defines the number of pages sampled at a global level. To set the number of pages sampled for an individual table, use the STATS\_SAMPLE\_PAGES option with CREATE TABLE or ALTER TABLE. For more information, see [Section 17.8.10.1, "Configuring Persistent](#page-110-0) [Optimizer Statistics Parameters".](#page-110-0)

If innodb\_stats\_persistent=OFF, the number of pages sampled is defined by innodb\_stats\_transient\_sample\_pages. See [Section 17.8.10.2,](#page-117-0) ["Configuring Non-Persistent Optimizer Statistics Parameters"](#page-117-0) for additional information.

For a more in-depth approach to estimating ANALYZE TABLE complexity, consider the following example.

In [Big O notation](http://en.wikipedia.org/wiki/Big_O_notation), ANALYZE TABLE complexity is described as:

```
 O(n_sample
 * (n_cols_in_uniq_i
 + n_cols_in_non_uniq_i
 + n_cols_in_pk * (1 + n_non_uniq_i))
 * n_part)
```

#### where:

- n\_sample is the number of pages sampled (defined by innodb\_stats\_persistent\_sample\_pages)
- n\_cols\_in\_uniq\_i is total number of all columns in all unique indexes (not counting the primary key columns)
- n\_cols\_in\_non\_uniq\_i is the total number of all columns in all nonunique indexes
- n\_cols\_in\_pk is the number of columns in the primary key (if a primary key is not defined, InnoDB creates a single column primary key internally)
- n\_non\_uniq\_i is the number of nonunique indexes in the table
- n\_part is the number of partitions. If no partitions are defined, the table is considered to be a single partition.

Now, consider the following table (table t), which has a primary key (2 columns), a unique index (2 columns), and two nonunique indexes (two columns each):

```
CREATE TABLE t (
 a INT,
 b INT,
 c INT,
 d INT,
 e INT,
 f INT,
 g INT,
 h INT,
 PRIMARY KEY (a, b),
 UNIQUE KEY i1uniq (c, d),
 KEY i2nonuniq (e, f),
 KEY i3nonuniq (g, h)
);
```

For the column and index data required by the algorithm described above, query the mysql.innodb\_index\_stats persistent index statistics table for table t. The n\_diff\_pfx% statistics show the columns that are counted for each index. For example, columns a and b are counted for the primary key index. For the nonunique indexes, the primary key columns (a,b) are counted in addition to the user defined columns.

![](_page_119_Picture_13.jpeg)

# **Note**

For additional information about the InnoDB persistent statistics tables, see [Section 17.8.10.1, "Configuring Persistent Optimizer Statistics Parameters"](#page-110-0)

```
mysql> SELECT index_name, stat_name, stat_description
 FROM mysql.innodb_index_stats WHERE
 database_name='test' AND
 table_name='t' AND
 stat_name like 'n_diff_pfx%';
 +------------+--------------+------------------+
 | index_name | stat_name | stat_description |
 +------------+--------------+------------------+
 | PRIMARY | n_diff_pfx01 | a |
 | PRIMARY | n_diff_pfx02 | a,b |
 | i1uniq | n_diff_pfx01 | c |
 | i1uniq | n_diff_pfx02 | c,d |
 | i2nonuniq | n_diff_pfx01 | e |
```

```
 | i2nonuniq | n_diff_pfx02 | e,f |
 | i2nonuniq | n_diff_pfx03 | e,f,a |
 | i2nonuniq | n_diff_pfx04 | e,f,a,b |
 | i3nonuniq | n_diff_pfx01 | g |
 | i3nonuniq | n_diff_pfx02 | g,h |
 | i3nonuniq | n_diff_pfx03 | g,h,a |
 | i3nonuniq | n_diff_pfx04 | g,h,a,b |
 +------------+--------------+------------------+
```

Based on the index statistics data shown above and the table definition, the following values can be determined:

- n\_cols\_in\_uniq\_i, the total number of all columns in all unique indexes not counting the primary key columns, is 2 (c and d)
- n\_cols\_in\_non\_uniq\_i, the total number of all columns in all nonunique indexes, is 4 (e, f, g and h)
- n\_cols\_in\_pk, the number of columns in the primary key, is 2 (a and b)
- n\_non\_uniq\_i, the number of nonunique indexes in the table, is 2 (i2nonuniq and i3nonuniq))
- n\_part, the number of partitions, is 1.

You can now calculate innodb\_stats\_persistent\_sample\_pages \* (2 + 4 + 2 \* (1 + 2)) \* 1 to determine the number of leaf pages that are scanned. With innodb\_stats\_persistent\_sample\_pages set to the default value of 20, and with a default page size of 16 KiB (innodb\_page\_size=16384), you can then estimate that 20 \* 12 \* 16384 bytes are read for table t, or about 4 MiB.

![](_page_120_Picture_9.jpeg)

#### **Note**

All 4 MiB may not be read from disk, as some leaf pages may already be cached in the buffer pool.

# <span id="page-120-0"></span>**17.8.11 Configuring the Merge Threshold for Index Pages**

You can configure the MERGE\_THRESHOLD value for index pages. If the "page-full" percentage for an index page falls below the MERGE\_THRESHOLD value when a row is deleted or when a row is shortened by an UPDATE operation, InnoDB attempts to merge the index page with a neighboring index page. The default MERGE\_THRESHOLD value is 50, which is the previously hardcoded value. The minimum MERGE\_THRESHOLD value is 1 and the maximum value is 50.

When the "page-full" percentage for an index page falls below 50%, which is the default MERGE\_THRESHOLD setting, InnoDB attempts to merge the index page with a neighboring page. If both pages are close to 50% full, a page split can occur soon after the pages are merged. If this mergesplit behavior occurs frequently, it can have an adverse affect on performance. To avoid frequent merge-splits, you can lower the MERGE\_THRESHOLD value so that InnoDB attempts page merges at a lower "page-full" percentage. Merging pages at a lower page-full percentage leaves more room in index pages and helps reduce merge-split behavior.

The MERGE\_THRESHOLD for index pages can be defined for a table or for individual indexes. A MERGE\_THRESHOLD value defined for an individual index takes priority over a MERGE\_THRESHOLD value defined for the table. If undefined, the MERGE\_THRESHOLD value defaults to 50.

## **Setting MERGE\_THRESHOLD for a Table**

You can set the MERGE\_THRESHOLD value for a table using the table\_option COMMENT clause of the CREATE TABLE statement. For example:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id)
) COMMENT='MERGE_THRESHOLD=45';
```

You can also set the MERGE\_THRESHOLD value for an existing table using the table\_option COMMENT clause with ALTER TABLE:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id)
);
ALTER TABLE t1 COMMENT='MERGE_THRESHOLD=40';
```

# **Setting MERGE\_THRESHOLD for Individual Indexes**

To set the MERGE\_THRESHOLD value for an individual index, you can use the index\_option COMMENT clause with CREATE TABLE, ALTER TABLE, or CREATE INDEX, as shown in the following examples:

• Setting MERGE\_THRESHOLD for an individual index using CREATE TABLE:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id) COMMENT 'MERGE_THRESHOLD=40'
);
```

• Setting MERGE\_THRESHOLD for an individual index using ALTER TABLE:

```
CREATE TABLE t1 (
 id INT,
 KEY id_index (id)
);
ALTER TABLE t1 DROP KEY id_index;
ALTER TABLE t1 ADD KEY id_index (id) COMMENT 'MERGE_THRESHOLD=40';
```

• Setting MERGE\_THRESHOLD for an individual index using CREATE INDEX:

```
CREATE TABLE t1 (id INT);
CREATE INDEX id_index ON t1 (id) COMMENT 'MERGE_THRESHOLD=40';
```

![](_page_121_Picture_11.jpeg)

# **Note**

You cannot modify the MERGE\_THRESHOLD value at the index level for GEN\_CLUST\_INDEX, which is the clustered index created by InnoDB when an InnoDB table is created without a primary key or unique key index. You can only modify the MERGE\_THRESHOLD value for GEN\_CLUST\_INDEX by setting MERGE\_THRESHOLD for the table.

# **Querying the MERGE\_THRESHOLD Value for an Index**

The current MERGE\_THRESHOLD value for an index can be obtained by querying the INNODB\_INDEXES table. For example:

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_INDEXES WHERE NAME='id_index' \G
*************************** 1. row ***************************
 INDEX_ID: 91
 NAME: id_index
 TABLE_ID: 68
 TYPE: 0
 N_FIELDS: 1
 PAGE_NO: 4
 SPACE: 57
MERGE_THRESHOLD: 40
```

You can use SHOW CREATE TABLE to view the MERGE\_THRESHOLD value for a table, if explicitly defined using the table\_option COMMENT clause:

```
mysql> SHOW CREATE TABLE t2 \G
*************************** 1. row ***************************
 Table: t2
```

```
Create Table: CREATE TABLE `t2` (
 `id` int(11) DEFAULT NULL,
 KEY `id_index` (`id`) COMMENT 'MERGE_THRESHOLD=40'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

![](_page_122_Picture_2.jpeg)

#### **Note**

A MERGE\_THRESHOLD value defined at the index level takes priority over a MERGE\_THRESHOLD value defined for the table. If undefined, MERGE\_THRESHOLD defaults to 50% (MERGE\_THRESHOLD=50, which is the previously hardcoded value.

Likewise, you can use SHOW INDEX to view the MERGE\_THRESHOLD value for an index, if explicitly defined using the index\_option COMMENT clause:

```
mysql> SHOW INDEX FROM t2 \G
*************************** 1. row ***************************
 Table: t2
 Non_unique: 1
 Key_name: id_index
 Seq_in_index: 1
 Column_name: id
 Collation: A
 Cardinality: 0
 Sub_part: NULL
 Packed: NULL
 Null: YES
 Index_type: BTREE
 Comment:
Index_comment: MERGE_THRESHOLD=40
```

# **Measuring the Effect of MERGE\_THRESHOLD Settings**

The INNODB\_METRICS table provides two counters that can be used to measure the effect of a MERGE\_THRESHOLD setting on index page merges.

```
mysql> SELECT NAME, COMMENT FROM INFORMATION_SCHEMA.INNODB_METRICS
 WHERE NAME like '%index_page_merge%';
+-----------------------------+----------------------------------------+
| NAME | COMMENT |
+-----------------------------+----------------------------------------+
| index_page_merge_attempts | Number of index page merge attempts |
| index_page_merge_successful | Number of successful index page merges |
+-----------------------------+----------------------------------------+
```

When lowering the MERGE\_THRESHOLD value, the objectives are:

- A smaller number of page merge attempts and successful page merges
- A similar number of page merge attempts and successful page merges

A MERGE\_THRESHOLD setting that is too small could result in large data files due to an excessive amount of empty page space.

For information about using INNODB\_METRICS counters, see Section 17.15.6, "InnoDB INFORMATION\_SCHEMA Metrics Table".

# <span id="page-122-0"></span>**17.8.12 Enabling Automatic InnoDB Configuration for a Dedicated MySQL Server**

When the server is started with [--innodb-dedicated-server](#page-188-0), InnoDB automatically calculates values for and sets the following system variables:

- [innodb\\_buffer\\_pool\\_size](#page-197-0)
- innodb\_redo\_log\_capacity

![](_page_123_Picture_1.jpeg)

#### **Note**

innodb\_redo\_log\_capacity supersedes both innodb\_log\_file\_size and innodb\_log\_files\_in\_group, which were set by --innodbdedicated-server in older versions of MySQL, but which have since been deprecated. You should expect innodb\_log\_file\_size and innodb\_log\_files\_in\_group to be removed in a future version of MySQL.

In MySQL 8.0, innodb\_flush\_method was also set automatically by this option, but in MySQL 8.4, this is no longer the case.

You should consider using --innodb-dedicated-server only if the MySQL instance resides on a dedicated server where it can use all available system resources—for example, if you run MySQL Server in a Docker container or dedicated VM that runs MySQL only. using --innodb-dedicatedserver is not recommended if the MySQL instance shares system resources with other applications.

The value for each affected variable is determined and applied by --innodb-dedicated-server as described in the following list:

• [innodb\\_buffer\\_pool\\_size](#page-197-0)

Buffer pool size is calculated according to the amount of memory detected on the server, as shown in the following table:

**Table 17.8 Automatically Configured Buffer Pool Size**

| Detected Server Memory | Buffer Pool Size              |  |
|------------------------|-------------------------------|--|
| Less than 1GB          | 128MB (the default value)     |  |
| 1GB to 4GB             | detected server memory * 0.5  |  |
| Greater than 4GB       | detected server memory * 0.75 |  |

• innodb\_redo\_log\_capacity

Redo log capacity is calculated according to the number of logical processors available on the server. The formula is (number of available logical processors / 2) GB, with a maximum dynamic default value of 16 GB.

• innodb\_log\_file\_size (deprecated)

Log file size is set according to the automatically configured buffer pool size, as shown in the following table:

**Table 17.9 Automatically Configured Log File Size**

| Buffer Pool Size   | Log File Size |
|--------------------|---------------|
| Less than 8GB      | 512MB         |
| 8GB to 128GB       | 1024MB        |
| Greater than 128GB | 2048MB        |

• innodb\_log\_files\_in\_group (deprecated)

The number of log files is determined according to the automatically configured buffer pool size, as shown in the following table:

**Table 17.10 Automatically Configured Number of Log Files**

| Buffer Pool Size | Number of Log Files            |
|------------------|--------------------------------|
| Less than 8GB    | round(buffer pool size)        |
| 8GB to 128GB     | round(buffer pool size * 0.75) |

| Buffer Pool Size   | Number of Log Files |  |
|--------------------|---------------------|--|
| Greater than 128GB | 64                  |  |

![](_page_124_Picture_2.jpeg)

#### **Note**

The minimum value for innodb\_log\_files\_in\_group value is 2; this lower limit is enforced if the rounded buffer pool size value is less than this number.

If one of the variables listed previously is set explicitly in an option file or elsewhere, this explicit value is used, and a startup warning similar to this one is printed to stderr:

[Warning] [000000] InnoDB: Option innodb\_dedicated\_server is ignored for innodb\_buffer\_pool\_size because innodb\_buffer\_pool\_size=134217728 is specified explicitly.

Setting one variable explicitly does not prevent the automatic configuration of other options.

If the server is started with --innodb-dedicated-server and [innodb\\_buffer\\_pool\\_size](#page-197-0) is set explicitly, variable settings based on buffer pool size use the buffer pool size value calculated according to the amount of memory detected on the server rather than the explicitly defined buffer pool size value.

![](_page_124_Picture_9.jpeg)

#### **Note**

Automatic configuration settings are applied by --innodb-dedicatedserver only when the MySQL server is started. If you later set any of the affected variables explicitly, this overrides its predetermined value, and the value that was explicitly set is applied. Setting one of these variables to DEFAULT causes it to be set to the actual default value as shown in the variable's description in the Manual, and does not cause it to revert to the value set by --innodb-dedicated-server. The corresponding system variable innodb\_dedicated\_server is changed only by starting the server with - innodb-dedicated-server (or with --innodb-dedicated-server=ON or --innodb-dedicated-server=OFF); it is otherwise read-only.

# <span id="page-124-0"></span>**17.9 InnoDB Table and Page Compression**

This section provides information about the InnoDB table compression and InnoDB page compression features. The page compression feature is also referred to as transparent page compression.

Using the compression features of InnoDB, you can create tables where the data is stored in compressed form. Compression can help to improve both raw performance and scalability. The compression means less data is transferred between disk and memory, and takes up less space on disk and in memory. The benefits are amplified for tables with secondary indexes, because index data is compressed also. Compression can be especially important for SSD storage devices, because they tend to have lower capacity than HDD devices.