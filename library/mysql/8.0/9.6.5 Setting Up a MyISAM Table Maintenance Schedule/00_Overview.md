---
source: MySQL 8.0 Reference
title: 00_Overview
---

It is a good idea to perform table checks on a regular basis rather than waiting for problems to occur. One way to check and repair MyISAM tables is with the CHECK TABLE and REPAIR TABLE statements. See Section 15.7.3, "Table Maintenance Statements".

Another way to check tables is to use myisamchk. For maintenance purposes, you can use myisamchk -s. The -s option (short for --silent) causes myisamchk to run in silent mode, printing messages only when errors occur.

It is also a good idea to enable automatic MyISAM table checking. For example, whenever the machine has done a restart in the middle of an update, you usually need to check each table that could have

been affected before it is used further. (These are "expected crashed tables.") To cause the server to check MyISAM tables automatically, start it with the myisam\_recover\_options system variable set. See Section 7.1.8, "Server System Variables".

You should also check your tables regularly during normal system operation. For example, you can run a cron job to check important tables once a week, using a line like this in a crontab file:

```
35 0 * * 0 /path/to/myisamchk --fast --silent /path/to/datadir/*/*.MYI
```

This prints out information about crashed tables so that you can examine and repair them as necessary.

To start with, execute myisamchk -s each night on all tables that have been updated during the last 24 hours. As you see that problems occur infrequently, you can back off the checking frequency to once a week or so.

Normally, MySQL tables need little maintenance. If you are performing many updates to MyISAM tables with dynamic-sized rows (tables with VARCHAR, BLOB, or TEXT columns) or have tables with many deleted rows you may want to defragment/reclaim space from the tables from time to time. You can do this by using OPTIMIZE TABLE on the tables in question. Alternatively, if you can stop the mysqld server for a while, change location into the data directory and use this command while the server is stopped:

\$> **myisamchk -r -s --sort-index --myisam\_sort\_buffer\_size=16M \*/\*.MYI**

# Chapter 10 Optimization

# **Table of Contents**

| 10.1 Optimization Overview 1793                                                 |      |
|---------------------------------------------------------------------------------|------|
| 10.2 Optimizing SQL Statements 1794                                             |      |
| 10.2.1 Optimizing SELECT Statements 1794                                        |      |
| 10.2.2 Optimizing Subqueries, Derived Tables, View References, and Common Table |      |
| Expressions 1846                                                                |      |
| 10.2.3 Optimizing INFORMATION_SCHEMA Queries 1860                               |      |
| 10.2.4 Optimizing Performance Schema Queries 1863                               |      |
| 10.2.5 Optimizing Data Change Statements 1864                                   |      |
| 10.2.6 Optimizing Database Privileges 1865                                      |      |
| 10.2.7 Other Optimization Tips 1866                                             |      |
| 10.3 Optimization and Indexes 1866                                              |      |
| 10.3.1 How MySQL Uses Indexes 1866                                              |      |
| 10.3.2 Primary Key Optimization 1868                                            |      |
| 10.3.3 SPATIAL Index Optimization 1868                                          |      |
| 10.3.4 Foreign Key Optimization 1868                                            |      |
| 10.3.5 Column Indexes 1869                                                      |      |
| 10.3.6 Multiple-Column Indexes 1870                                             |      |
| 10.3.7 Verifying Index Usage 1871                                               |      |
| 10.3.8 InnoDB and MyISAM Index Statistics Collection 1872                       |      |
| 10.3.9 Comparison of B-Tree and Hash Indexes                                    | 1873 |
| 10.3.10 Use of Index Extensions 1874                                            |      |
| 10.3.11 Optimizer Use of Generated Column Indexes 1877                          |      |
| 10.3.12 Invisible Indexes 1878                                                  |      |
| 10.3.13 Descending Indexes 1880                                                 |      |
| 10.3.14 Indexed Lookups from TIMESTAMP Columns 1881                             |      |
| 10.4 Optimizing Database Structure 1883                                         |      |
| 10.4.1 Optimizing Data Size 1883                                                |      |
| 10.4.2 Optimizing MySQL Data Types 1885                                         |      |
| 10.4.3 Optimizing for Many Tables 1886                                          |      |
| 10.4.4 Internal Temporary Table Use in MySQL 1888                               |      |
| 10.4.5 Limits on Number of Databases and Tables 1892                            |      |
| 10.4.6 Limits on Table Size 1892                                                |      |
| 10.4.7 Limits on Table Column Count and Row Size                                | 1893 |
| 10.5 Optimizing for InnoDB Tables 1895                                          |      |
| 10.5.1 Optimizing Storage Layout for InnoDB Tables 1896                         |      |
| 10.5.2 Optimizing InnoDB Transaction Management 1896                            |      |
| 10.5.3 Optimizing InnoDB Read-Only Transactions 1897                            |      |
| 10.5.4 Optimizing InnoDB Redo Logging 1898                                      |      |
| 10.5.5 Bulk Data Loading for InnoDB Tables 1899                                 |      |
| 10.5.6 Optimizing InnoDB Queries 1901                                           |      |
| 10.5.7 Optimizing InnoDB DDL Operations 1901                                    |      |
| 10.5.8 Optimizing InnoDB Disk I/O 1901                                          |      |
| 10.5.9 Optimizing InnoDB Configuration Variables 1906                           |      |
| 10.5.10 Optimizing InnoDB for Systems with Many Tables 1907                     |      |
| 10.6 Optimizing for MyISAM Tables 1907                                          |      |
| 10.6.1 Optimizing MyISAM Queries 1907                                           |      |
| 10.6.2 Bulk Data Loading for MyISAM Tables                                      | 1908 |
| 10.6.3 Optimizing REPAIR TABLE Statements 1910                                  |      |
| 10.7 Optimizing for MEMORY Tables 1911                                          |      |
| 10.8 Understanding the Query Execution Plan 1911                                |      |
| 10.8.1 Optimizing Queries with EXPLAIN 1912                                     |      |
| 10.8.2 EXPLAIN Output Format 1912                                               |      |
|                                                                                 |      |

| 10.8.3 Extended EXPLAIN Output Format 1926                              |      |
|-------------------------------------------------------------------------|------|
| 10.8.4 Obtaining Execution Plan Information for a Named Connection 1928 |      |
| 10.8.5 Estimating Query Performance 1929                                |      |
| 10.9 Controlling the Query Optimizer 1929                               |      |
| 10.9.1 Controlling Query Plan Evaluation 1929                           |      |
| 10.9.2 Switchable Optimizations                                         | 1930 |
| 10.9.3 Optimizer Hints 1940                                             |      |
| 10.9.4 Index Hints 1954                                                 |      |
| 10.9.5 The Optimizer Cost Model                                         | 1957 |
| 10.9.6 Optimizer Statistics 1960                                        |      |
| 10.10 Buffering and Caching 1963                                        |      |
| 10.10.1 InnoDB Buffer Pool Optimization                                 | 1963 |
| 10.10.2 The MyISAM Key Cache 1964                                       |      |
| 10.10.3 Caching of Prepared Statements and Stored Programs 1968         |      |
| 10.11 Optimizing Locking Operations 1969                                |      |
| 10.11.1 Internal Locking Methods 1969                                   |      |
| 10.11.2 Table Locking Issues 1972                                       |      |
| 10.11.3 Concurrent Inserts 1973                                         |      |
| 10.11.4 Metadata Locking                                                | 1974 |
| 10.11.5 External Locking 1977                                           |      |
| 10.12 Optimizing the MySQL Server 1978                                  |      |
| 10.12.1 Optimizing Disk I/O 1978                                        |      |
| 10.12.2 Using Symbolic Links 1979                                       |      |
| 10.12.3 Optimizing Memory Use 1982                                      |      |
| 10.13 Measuring Performance (Benchmarking) 1989                         |      |
| 10.13.1 Measuring the Speed of Expressions and Functions 1989           |      |
|                                                                         |      |
| 10.13.2 Using Your Own Benchmarks 1990                                  |      |
| 10.13.3 Measuring Performance with performance_schema 1990              |      |
| 10.14 Examining Server Thread (Process) Information 1990                |      |
| 10.14.1 Accessing the Process List 1991                                 |      |
| 10.14.2 Thread Command Values 1992                                      |      |
| 10.14.3 General Thread States 1994                                      |      |
| 10.14.4 Replication Source Thread States 2001                           |      |
| 10.14.5 Replication I/O (Receiver) Thread States 2001                   |      |
| 10.14.6 Replication SQL Thread States                                   | 2003 |
| 10.14.7 Replication Connection Thread States                            | 2004 |
| 10.14.8 NDB Cluster Thread States 2005                                  |      |
| 10.14.9 Event Scheduler Thread States 2006                              |      |
| 10.15 Tracing the Optimizer 2006                                        |      |
| 10.15.1 Typical Usage 2006                                              |      |
| 10.15.2 System Variables Controlling Tracing 2006                       |      |
| 10.15.3 Traceable Statements 2007                                       |      |
| 10.15.4 Tuning Trace Purging                                            | 2007 |
| 10.15.5 Tracing Memory Usage 2008                                       |      |
| 10.15.6 Privilege Checking 2009                                         |      |
| 10.15.7 Interaction with thedebug Option 2009                           |      |
| 10.15.8 The optimizer_trace System Variable 2009                        |      |
| 10.15.9 The end_markers_in_json System Variable 2009                    |      |
| 10.15.10 Selecting Optimizer Features to Trace 2009                     |      |
| 10.15.11 Trace General Structure 2009                                   |      |
| 10.15.12 Example 2010                                                   |      |
| 10.15.13 Displaying Traces in Other Applications 2020                   |      |
| 10.15.14 Preventing the Use of Optimizer Trace 2020                     |      |
| 10.15.15 Testing Optimizer Trace 2020                                   |      |
| 10.15.16 Optimizer Trace Implementation                                 | 2020 |

This chapter explains how to optimize MySQL performance and provides examples. Optimization involves configuring, tuning, and measuring performance, at several levels. Depending on your job role (developer, DBA, or a combination of both), you might optimize at the level of individual SQL statements, entire applications, a single database server, or multiple networked database servers. Sometimes you can be proactive and plan in advance for performance, while other times you might troubleshoot a configuration or code issue after a problem occurs. Optimizing CPU and memory usage can also improve scalability, allowing the database to handle more load without slowing down.

# <span id="page-22-0"></span>**10.1 Optimization Overview**

Database performance depends on several factors at the database level, such as tables, queries, and configuration settings. These software constructs result in CPU and I/O operations at the hardware level, which you must minimize and make as efficient as possible. As you work on database performance, you start by learning the high-level rules and guidelines for the software side, and measuring performance using wall-clock time. As you become an expert, you learn more about what happens internally, and start measuring things such as CPU cycles and I/O operations.

Typical users aim to get the best database performance out of their existing software and hardware configurations. Advanced users look for opportunities to improve the MySQL software itself, or develop their own storage engines and hardware appliances to expand the MySQL ecosystem.

- [Optimizing at the Database Level](#page-22-1)
- [Optimizing at the Hardware Level](#page-23-2)
- [Balancing Portability and Performance](#page-23-3)

## <span id="page-22-1"></span>**Optimizing at the Database Level**

The most important factor in making a database application fast is its basic design:

- Are the tables structured properly? In particular, do the columns have the right data types, and does each table have the appropriate columns for the type of work? For example, applications that perform frequent updates often have many tables with few columns, while applications that analyze large amounts of data often have few tables with many columns.
- Are the right [indexes](#page-95-1) in place to make queries efficient?
- Are you using the appropriate storage engine for each table, and taking advantage of the strengths and features of each storage engine you use? In particular, the choice of a transactional storage engine such as [InnoDB](#page-124-0) or a nontransactional one such as [MyISAM](#page-136-1) can be very important for performance and scalability.

![](_page_22_Picture_13.jpeg)

#### **Note**

InnoDB is the default storage engine for new tables. In practice, the advanced InnoDB performance features mean that InnoDB tables often outperform the simpler MyISAM tables, especially for a busy database.

- Does each table use an appropriate row format? This choice also depends on the storage engine used for the table. In particular, compressed tables use less disk space and so require less disk I/O to read and write the data. Compression is available for all kinds of workloads with InnoDB tables, and for read-only MyISAM tables.
- Does the application use an appropriate [locking strategy](#page-198-0)? For example, by allowing shared access when possible so that database operations can run concurrently, and requesting exclusive access when appropriate so that critical operations get top priority. Again, the choice of storage engine is significant. The InnoDB storage engine handles most locking issues without involvement from you, allowing for better concurrency in the database and reducing the amount of experimentation and tuning for your code.
- Are all [memory areas used for caching](#page-192-0) sized correctly? That is, large enough to hold frequently accessed data, but not so large that they overload physical memory and cause paging. The main memory areas to configure are the InnoDB buffer pool and the MyISAM key cache.

# <span id="page-23-2"></span>**Optimizing at the Hardware Level**

Any database application eventually hits hardware limits as the database becomes more and more busy. A DBA must evaluate whether it is possible to tune the application or reconfigure the server to avoid these bottlenecks, or whether more hardware resources are required. System bottlenecks typically arise from these sources:

- Disk seeks. It takes time for the disk to find a piece of data. With modern disks, the mean time for this is usually lower than 10ms, so we can in theory do about 100 seeks a second. This time improves slowly with new disks and is very hard to optimize for a single table. The way to optimize seek time is to distribute the data onto more than one disk.
- Disk reading and writing. When the disk is at the correct position, we need to read or write the data. With modern disks, one disk delivers at least 10–20MB/s throughput. This is easier to optimize than seeks because you can read in parallel from multiple disks.
- CPU cycles. When the data is in main memory, we must process it to get our result. Having large tables compared to the amount of memory is the most common limiting factor. But with small tables, speed is usually not the problem.
- Memory bandwidth. When the CPU needs more data than can fit in the CPU cache, main memory bandwidth becomes a bottleneck. This is an uncommon bottleneck for most systems, but one to be aware of.

## <span id="page-23-3"></span>**Balancing Portability and Performance**

To use performance-oriented SQL extensions in a portable MySQL program, you can wrap MySQLspecific keywords in a statement within /\*! \*/ comment delimiters. Other SQL servers ignore the commented keywords. For information about writing comments, see Section 11.7, "Comments".

# <span id="page-23-0"></span>**10.2 Optimizing SQL Statements**

The core logic of a database application is performed through SQL statements, whether issued directly through an interpreter or submitted behind the scenes through an API. The tuning guidelines in this section help to speed up all kinds of MySQL applications. The guidelines cover SQL operations that read and write data, the behind-the-scenes overhead for SQL operations in general, and operations used in specific scenarios such as database monitoring.

# <span id="page-23-1"></span>**10.2.1 Optimizing SELECT Statements**

Queries, in the form of SELECT statements, perform all the lookup operations in the database. Tuning these statements is a top priority, whether to achieve sub-second response times for dynamic web pages, or to chop hours off the time to generate huge overnight reports.

Besides SELECT statements, the tuning techniques for queries also apply to constructs such as CREATE TABLE...AS SELECT, INSERT INTO...SELECT, and WHERE clauses in DELETE statements. Those statements have additional performance considerations because they combine write operations with the read-oriented query operations.

NDB Cluster supports a join pushdown optimization whereby a qualifying join is sent in its entirety to NDB Cluster data nodes, where it can be distributed among them and executed in parallel. For more information about this optimization, see Conditions for NDB pushdown joins.

The main considerations for optimizing queries are:

• To make a slow SELECT ... WHERE query faster, the first thing to check is whether you can add an index. Set up indexes on columns used in the WHERE clause, to speed up evaluation, filtering, and the final retrieval of results. To avoid wasted disk space, construct a small set of indexes that speed up many related queries used in your application.

Indexes are especially important for queries that reference different tables, using features such as joins and foreign keys. You can use the EXPLAIN statement to determine which indexes are used for a SELECT. See [Section 10.3.1, "How MySQL Uses Indexes"](#page-95-2) and [Section 10.8.1, "Optimizing Queries](#page-141-0) [with EXPLAIN"](#page-141-0).

- Isolate and tune any part of the query, such as a function call, that takes excessive time. Depending on how the query is structured, a function could be called once for every row in the result set, or even once for every row in the table, greatly magnifying any inefficiency.
- Minimize the number of full table scans in your queries, particularly for big tables.
- Keep table statistics up to date by using the ANALYZE TABLE statement periodically, so the optimizer has the information needed to construct an efficient execution plan.
- Learn the tuning techniques, indexing techniques, and configuration parameters that are specific to the storage engine for each table. Both InnoDB and MyISAM have sets of guidelines for enabling and sustaining high performance in queries. For details, see [Section 10.5.6, "Optimizing InnoDB](#page-130-0) [Queries"](#page-130-0) and [Section 10.6.1, "Optimizing MyISAM Queries"](#page-136-2).
- You can optimize single-query transactions for InnoDB tables, using the technique in [Section 10.5.3,](#page-126-0) ["Optimizing InnoDB Read-Only Transactions".](#page-126-0)
- Avoid transforming the query in ways that make it hard to understand, especially if the optimizer does some of the same transformations automatically.
- If a performance issue is not easily solved by one of the basic guidelines, investigate the internal details of the specific query by reading the EXPLAIN plan and adjusting your indexes, WHERE clauses, join clauses, and so on. (When you reach a certain level of expertise, reading the EXPLAIN plan might be your first step for every query.)
- Adjust the size and properties of the memory areas that MySQL uses for caching. With efficient use of the InnoDB buffer pool, MyISAM key cache, and the MySQL query cache, repeated queries run faster because the results are retrieved from memory the second and subsequent times.
- Even for a query that runs fast using the cache memory areas, you might still optimize further so that they require less cache memory, making your application more scalable. Scalability means that your application can handle more simultaneous users, larger requests, and so on without experiencing a big drop in performance.
- Deal with locking issues, where the speed of your query might be affected by other sessions accessing the tables at the same time.

### <span id="page-24-0"></span>**10.2.1.1 WHERE Clause Optimization**

This section discusses optimizations that can be made for processing WHERE clauses. The examples use SELECT statements, but the same optimizations apply for WHERE clauses in DELETE and UPDATE statements.

![](_page_24_Picture_14.jpeg)

#### **Note**

Because work on the MySQL optimizer is ongoing, not all of the optimizations that MySQL performs are documented here.

You might be tempted to rewrite your queries to make arithmetic operations faster, while sacrificing readability. Because MySQL does similar optimizations automatically, you can often avoid this work, and leave the query in a more understandable and maintainable form. Some of the optimizations performed by MySQL follow:

• Removal of unnecessary parentheses:

```
 ((a AND b) AND c OR (((a AND b) AND (c AND d))))
-> (a AND b AND c) OR (a AND b AND c AND d)
```

• Constant folding:

```
 (a<b AND b=c) AND a=5
-> b>5 AND b=c AND a=5
```

• Constant condition removal:

```
 (b>=5 AND b=5) OR (b=6 AND 5=5) OR (b=7 AND 5=6)
-> b=5 OR b=6
```

In MySQL 8.0.14 and later, this takes place during preparation rather than during the optimization phase, which helps in simplification of joins. See [Section 10.2.1.9, "Outer Join Optimization"](#page-49-0), for further information and examples.

- Constant expressions used by indexes are evaluated only once.
- Beginning with MySQL 8.0.16, comparisons of columns of numeric types with constant values are checked and folded or removed for invalid or out-of-rage values:

```
# CREATE TABLE t (c TINYINT UNSIGNED NOT NULL);
 SELECT * FROM t WHERE c < 256;
-≫ SELECT * FROM t WHERE 1;
```

See [Section 10.2.1.14, "Constant-Folding Optimization"](#page-59-0), for more information.

- COUNT(\*) on a single table without a WHERE is retrieved directly from the table information for MyISAM and MEMORY tables. This is also done for any NOT NULL expression when used with only one table.
- Early detection of invalid constant expressions. MySQL quickly detects that some SELECT statements are impossible and returns no rows.
- HAVING is merged with WHERE if you do not use GROUP BY or aggregate functions (COUNT(), MIN(), and so on).
- For each table in a join, a simpler WHERE is constructed to get a fast WHERE evaluation for the table and also to skip rows as soon as possible.
- All constant tables are read first before any other tables in the query. A constant table is any of the following:
  - An empty table or a table with one row.
  - A table that is used with a WHERE clause on a PRIMARY KEY or a UNIQUE index, where all index parts are compared to constant expressions and are defined as NOT NULL.

All of the following tables are used as constant tables:

```
SELECT * FROM t WHERE primary_key=1;
SELECT * FROM t1,t2
 WHERE t1.primary_key=1 AND t2.primary_key=t1.id;
```

- The best join combination for joining the tables is found by trying all possibilities. If all columns in ORDER BY and GROUP BY clauses come from the same table, that table is preferred first when joining.
- If there is an ORDER BY clause and a different GROUP BY clause, or if the ORDER BY or GROUP BY contains columns from tables other than the first table in the join queue, a temporary table is created.
- If you use the SQL\_SMALL\_RESULT modifier, MySQL uses an in-memory temporary table.
- Each table index is queried, and the best index is used unless the optimizer believes that it is more efficient to use a table scan. At one time, a scan was used based on whether the best index spanned more than 30% of the table, but a fixed percentage no longer determines the choice between using

an index or a scan. The optimizer now is more complex and bases its estimate on additional factors such as table size, number of rows, and I/O block size.

- In some cases, MySQL can read rows from the index without even consulting the data file. If all columns used from the index are numeric, only the index tree is used to resolve the query.
- Before each row is output, those that do not match the HAVING clause are skipped.

Some examples of queries that are very fast:

```
SELECT COUNT(*) FROM tbl_name;
SELECT MIN(key_part1),MAX(key_part1) FROM tbl_name;
SELECT MAX(key_part2) FROM tbl_name
 WHERE key_part1=constant;
SELECT ... FROM tbl_name
 ORDER BY key_part1,key_part2,... LIMIT 10;
SELECT ... FROM tbl_name
 ORDER BY key_part1 DESC, key_part2 DESC, ... LIMIT 10;
```

MySQL resolves the following queries using only the index tree, assuming that the indexed columns are numeric:

```
SELECT key_part1,key_part2 FROM tbl_name WHERE key_part1=val;
SELECT COUNT(*) FROM tbl_name
 WHERE key_part1=val1 AND key_part2=val2;
SELECT MAX(key_part2) FROM tbl_name GROUP BY key_part1;
```

The following queries use indexing to retrieve the rows in sorted order without a separate sorting pass:

```
SELECT ... FROM tbl_name
 ORDER BY key_part1,key_part2,... ;
SELECT ... FROM tbl_name
 ORDER BY key_part1 DESC, key_part2 DESC, ... ;
```

### <span id="page-26-1"></span>**10.2.1.2 Range Optimization**

The [range](#page-147-0) access method uses a single index to retrieve a subset of table rows that are contained within one or several index value intervals. It can be used for a single-part or multiple-part index. The following sections describe conditions under which the optimizer uses range access.

- [Range Access Method for Single-Part Indexes](#page-26-0)
- [Range Access Method for Multiple-Part Indexes](#page-28-0)
- [Equality Range Optimization of Many-Valued Comparisons](#page-29-0)
- [Skip Scan Range Access Method](#page-30-0)
- [Range Optimization of Row Constructor Expressions](#page-32-0)
- [Limiting Memory Use for Range Optimization](#page-32-1)

#### <span id="page-26-0"></span>**Range Access Method for Single-Part Indexes**

For a single-part index, index value intervals can be conveniently represented by corresponding conditions in the WHERE clause, denoted as range conditions rather than "intervals."

The definition of a range condition for a single-part index is as follows:

• For both BTREE and HASH indexes, comparison of a key part with a constant value is a range condition when using the =, <=>, IN(), IS NULL, or IS NOT NULL operators.

- Additionally, for BTREE indexes, comparison of a key part with a constant value is a range condition when using the >, <, >=, <=, BETWEEN, !=, or <> operators, or LIKE comparisons if the argument to LIKE is a constant string that does not start with a wildcard character.
- For all index types, multiple range conditions combined with OR or AND form a range condition.

"Constant value" in the preceding descriptions means one of the following:

- A constant from the query string
- A column of a [const](#page-145-0) or [system](#page-145-1) table from the same join
- The result of an uncorrelated subquery
- Any expression composed entirely from subexpressions of the preceding types

Here are some examples of queries with range conditions in the WHERE clause:

```
SELECT * FROM t1
 WHERE key_col > 1
 AND key_col < 10;
SELECT * FROM t1
 WHERE key_col = 1
 OR key_col IN (15,18,20);
SELECT * FROM t1
 WHERE key_col LIKE 'ab%'
 OR key_col BETWEEN 'bar' AND 'foo';
```

Some nonconstant values may be converted to constants during the optimizer constant propagation phase.

MySQL tries to extract range conditions from the WHERE clause for each of the possible indexes. During the extraction process, conditions that cannot be used for constructing the range condition are dropped, conditions that produce overlapping ranges are combined, and conditions that produce empty ranges are removed.

Consider the following statement, where key1 is an indexed column and nonkey is not indexed:

```
SELECT * FROM t1 WHERE
 (key1 < 'abc' AND (key1 LIKE 'abcde%' OR key1 LIKE '%b')) OR
 (key1 < 'bar' AND nonkey = 4) OR
 (key1 < 'uux' AND key1 > 'z');
```

The extraction process for key key1 is as follows:

1. Start with original WHERE clause:

```
(key1 < 'abc' AND (key1 LIKE 'abcde%' OR key1 LIKE '%b')) OR
(key1 < 'bar' AND nonkey = 4) OR
(key1 < 'uux' AND key1 > 'z')
```

2. Remove nonkey = 4 and key1 LIKE '%b' because they cannot be used for a range scan. The correct way to remove them is to replace them with TRUE, so that we do not miss any matching rows when doing the range scan. Replacing them with TRUE yields:

```
(key1 < 'abc' AND (key1 LIKE 'abcde%' OR TRUE)) OR
(key1 < 'bar' AND TRUE) OR
(key1 < 'uux' AND key1 > 'z')
```

- 3. Collapse conditions that are always true or false:
  - (key1 LIKE 'abcde%' OR TRUE) is always true
  - (key1 < 'uux' AND key1 > 'z') is always false

Replacing these conditions with constants yields:

```
(key1 < 'abc' AND TRUE) OR (key1 < 'bar' AND TRUE) OR (FALSE)
```

Removing unnecessary TRUE and FALSE constants yields:

```
(key1 < 'abc') OR (key1 < 'bar')
```

4. Combining overlapping intervals into one yields the final condition to be used for the range scan:

```
(key1 < 'bar')
```

In general (and as demonstrated by the preceding example), the condition used for a range scan is less restrictive than the WHERE clause. MySQL performs an additional check to filter out rows that satisfy the range condition but not the full WHERE clause.

The range condition extraction algorithm can handle nested AND/OR constructs of arbitrary depth, and its output does not depend on the order in which conditions appear in WHERE clause.

MySQL does not support merging multiple ranges for the [range](#page-147-0) access method for spatial indexes. To work around this limitation, you can use a UNION with identical SELECT statements, except that you put each spatial predicate in a different SELECT.

### <span id="page-28-0"></span>**Range Access Method for Multiple-Part Indexes**

Range conditions on a multiple-part index are an extension of range conditions for a single-part index. A range condition on a multiple-part index restricts index rows to lie within one or several key tuple intervals. Key tuple intervals are defined over a set of key tuples, using ordering from the index.

For example, consider a multiple-part index defined as key1(key\_part1, key\_part2, key\_part3), and the following set of key tuples listed in key order:

```
key_part1 key_part2 key_part3
 NULL 1 'abc'
 NULL 1 'xyz'
 NULL 2 'foo'
 1 1 'abc'
 1 1 'xyz'
 1 2 'abc'
 2 1 'aaa'
```

The condition key\_part1 = 1 defines this interval:

```
(1,-inf,-inf) <= (key_part1,key_part2,key_part3) < (1,+inf,+inf)
```

The interval covers the 4th, 5th, and 6th tuples in the preceding data set and can be used by the range access method.

By contrast, the condition key\_part3 = 'abc' does not define a single interval and cannot be used by the range access method.

The following descriptions indicate how range conditions work for multiple-part indexes in greater detail.

• For HASH indexes, each interval containing identical values can be used. This means that the interval can be produced only for conditions in the following form:

```
 key_part1 cmp const1
AND key_part2 cmp const2
AND ...
AND key_partN cmp constN;
```

Here, const1, const2, … are constants, cmp is one of the =, <=>, or IS NULL comparison operators, and the conditions cover all index parts. (That is, there are N conditions, one for each part of an N-part index.) For example, the following is a range condition for a three-part HASH index:

```
key_part1 = 1 AND key_part2 IS NULL AND key_part3 = 'foo'
```

For the definition of what is considered to be a constant, see [Range Access Method for Single-Part](#page-26-0) [Indexes](#page-26-0).

• For a BTREE index, an interval might be usable for conditions combined with AND, where each condition compares a key part with a constant value using =, <=>, IS NULL, >, <, >=, <=, !=, <>, BETWEEN, or LIKE 'pattern' (where 'pattern' does not start with a wildcard). An interval can be used as long as it is possible to determine a single key tuple containing all rows that match the condition (or two intervals if <> or != is used).

The optimizer attempts to use additional key parts to determine the interval as long as the comparison operator is =, <=>, or IS NULL. If the operator is >, <, >=, <=, !=, <>, BETWEEN, or LIKE, the optimizer uses it but considers no more key parts. For the following expression, the optimizer uses = from the first comparison. It also uses >= from the second comparison but considers no further key parts and does not use the third comparison for interval construction:

```
key_part1 = 'foo' AND key_part2 >= 10 AND key_part3 > 10
```

The single interval is:

```
('foo',10,-inf) < (key_part1,key_part2,key_part3) < ('foo',+inf,+inf)
```

It is possible that the created interval contains more rows than the initial condition. For example, the preceding interval includes the value ('foo', 11, 0), which does not satisfy the original condition.

• If conditions that cover sets of rows contained within intervals are combined with OR, they form a condition that covers a set of rows contained within the union of their intervals. If the conditions are combined with AND, they form a condition that covers a set of rows contained within the intersection of their intervals. For example, for this condition on a two-part index:

```
(key_part1 = 1 AND key_part2 < 2) OR (key_part1 > 5)
```

The intervals are:

```
(1,-inf) < (key_part1,key_part2) < (1,2)
(5,-inf) < (key_part1,key_part2)
```

In this example, the interval on the first line uses one key part for the left bound and two key parts for the right bound. The interval on the second line uses only one key part. The key\_len column in the EXPLAIN output indicates the maximum length of the key prefix used.

In some cases, key\_len may indicate that a key part was used, but that might be not what you would expect. Suppose that key\_part1 and key\_part2 can be NULL. Then the key\_len column displays two key part lengths for the following condition:

```
key_part1 >= 1 AND key_part2 < 2
```

But, in fact, the condition is converted to this:

```
key_part1 >= 1 AND key_part2 IS NOT NULL
```

For a description of how optimizations are performed to combine or eliminate intervals for range conditions on a single-part index, see [Range Access Method for Single-Part Indexes.](#page-26-0) Analogous steps are performed for range conditions on multiple-part indexes.

#### <span id="page-29-0"></span>**Equality Range Optimization of Many-Valued Comparisons**

Consider these expressions, where col\_name is an indexed column:

```
col_name IN(val1, ..., valN)
col_name = val1 OR ... OR col_name = valN
```

Each expression is true if col\_name is equal to any of several values. These comparisons are equality range comparisons (where the "range" is a single value). The optimizer estimates the cost of reading qualifying rows for equality range comparisons as follows:

- If there is a unique index on col\_name, the row estimate for each range is 1 because at most one row can have the given value.
- Otherwise, any index on col\_name is nonunique and the optimizer can estimate the row count for each range using dives into the index or index statistics.

With index dives, the optimizer makes a dive at each end of a range and uses the number of rows in the range as the estimate. For example, the expression col\_name IN (10, 20, 30) has three equality ranges and the optimizer makes two dives per range to generate a row estimate. Each pair of dives yields an estimate of the number of rows that have the given value.

Index dives provide accurate row estimates, but as the number of comparison values in the expression increases, the optimizer takes longer to generate a row estimate. Use of index statistics is less accurate than index dives but permits faster row estimation for large value lists.

The eq\_range\_index\_dive\_limit system variable enables you to configure the number of values at which the optimizer switches from one row estimation strategy to the other. To permit use of index dives for comparisons of up to N equality ranges, set eq\_range\_index\_dive\_limit to N + 1. To disable use of statistics and always use index dives regardless of N, set eq\_range\_index\_dive\_limit to 0.

To update table index statistics for best estimates, use ANALYZE TABLE.

Prior to MySQL 8.0, there is no way of skipping the use of index dives to estimate index usefulness, except by using the eq\_range\_index\_dive\_limit system variable. In MySQL 8.0, index dive skipping is possible for queries that satisfy all these conditions:

- The query is for a single table, not a join on multiple tables.
- A single-index FORCE INDEX index hint is present. The idea is that if index use is forced, there is nothing to be gained from the additional overhead of performing dives into the index.
- The index is nonunique and not a FULLTEXT index.
- No subquery is present.
- No DISTINCT, GROUP BY, or ORDER BY clause is present.

For EXPLAIN FOR CONNECTION, the output changes as follows if index dives are skipped:

- For traditional output, the rows and filtered values are NULL.
- For JSON output, rows\_examined\_per\_scan and rows\_produced\_per\_join do not appear, skip\_index\_dive\_due\_to\_force is true, and cost calculations are not accurate.

Without FOR CONNECTION, EXPLAIN output does not change when index dives are skipped.

After execution of a query for which index dives are skipped, the corresponding row in the Information Schema OPTIMIZER\_TRACE table contains an index\_dives\_for\_range\_access value of skipped\_due\_to\_force\_index.

### <span id="page-30-0"></span>**Skip Scan Range Access Method**

Consider the following scenario:

```
CREATE TABLE t1 (f1 INT NOT NULL, f2 INT NOT NULL, PRIMARY KEY(f1, f2));
INSERT INTO t1 VALUES
 (1,1), (1,2), (1,3), (1,4), (1,5),
 (2,1), (2,2), (2,3), (2,4), (2,5);
```

```
INSERT INTO t1 SELECT f1, f2 + 5 FROM t1;
INSERT INTO t1 SELECT f1, f2 + 10 FROM t1;
INSERT INTO t1 SELECT f1, f2 + 20 FROM t1;
INSERT INTO t1 SELECT f1, f2 + 40 FROM t1;
ANALYZE TABLE t1;
EXPLAIN SELECT f1, f2 FROM t1 WHERE f2 > 40;
```

To execute this query, MySQL can choose an index scan to fetch all rows (the index includes all columns to be selected), then apply the f2 > 40 condition from the WHERE clause to produce the final result set.

A range scan is more efficient than a full index scan, but cannot be used in this case because there is no condition on f1, the first index column. However, as of MySQL 8.0.13, the optimizer can perform multiple range scans, one for each value of f1, using a method called Skip Scan that is similar to Loose Index Scan (see [Section 10.2.1.17, "GROUP BY Optimization"](#page-65-0)):

- 1. Skip between distinct values of the first index part, f1 (the index prefix).
- 2. Perform a subrange scan on each distinct prefix value for the f2 > 40 condition on the remaining index part.

For the data set shown earlier, the algorithm operates like this:

- 1. Get the first distinct value of the first key part (f1 = 1).
- 2. Construct the range based on the first and second key parts (f1 = 1 AND f2 > 40).
- 3. Perform a range scan.
- 4. Get the next distinct value of the first key part (f1 = 2).
- 5. Construct the range based on the first and second key parts (f1 = 2 AND f2 > 40).
- 6. Perform a range scan.

Using this strategy decreases the number of accessed rows because MySQL skips the rows that do not qualify for each constructed range. This Skip Scan access method is applicable under the following conditions:

- Table T has at least one compound index with key parts of the form ([A\_1, ..., A\_k,] B\_1, ..., B\_m, C [, D\_1, ..., D\_n]). Key parts A and D may be empty, but B and C must be nonempty.
- The query references only one table.
- The query does not use GROUP BY or DISTINCT.
- The query references only columns in the index.
- The predicates on A\_1, ..., A\_k must be equality predicates and they must be constants. This includes the IN() operator.
- The query must be a conjunctive query; that is, an AND of OR conditions: (cond1(key\_part1) OR cond2(key\_part1)) AND (cond1(key\_part2) OR ...) AND ...
- There must be a range condition on C.
- Conditions on D columns are permitted. Conditions on D must be in conjunction with the range condition on C.

Use of Skip Scan is indicated in EXPLAIN output as follows:

• Using index for skip scan in the Extra column indicates that the loose index Skip Scan access method is used.

• If the index can be used for Skip Scan, the index should be visible in the possible\_keys column.

Use of Skip Scan is indicated in optimizer trace output by a "skip scan" element of this form:

```
"skip_scan_range": {
 "type": "skip_scan",
 "index": index_used_for_skip_scan,
 "key_parts_used_for_access": [key_parts_used_for_access],
 "range": [range]
}
```

You may also see a "best\_skip\_scan\_summary" element. If Skip Scan is chosen as the best range access variant, a "chosen\_range\_access\_summary" is written. If Skip Scan is chosen as the overall best access method, a "best\_access\_path" element is present.

Use of Skip Scan is subject to the value of the [skip\\_scan](#page-162-0) flag of the optimizer\_switch system variable. See [Section 10.9.2, "Switchable Optimizations".](#page-159-0) By default, this flag is on. To disable it, set [skip\\_scan](#page-162-0) to off.

In addition to using the optimizer\_switch system variable to control optimizer use of Skip Scan session-wide, MySQL supports optimizer hints to influence the optimizer on a per-statement basis. See [Section 10.9.3, "Optimizer Hints"](#page-169-0).

#### <span id="page-32-0"></span>**Range Optimization of Row Constructor Expressions**

The optimizer is able to apply the range scan access method to queries of this form:

```
SELECT ... FROM t1 WHERE ( col_1, col_2 ) IN (( 'a', 'b' ), ( 'c', 'd' ));
```

Previously, for range scans to be used, it was necessary to write the query as:

```
SELECT ... FROM t1 WHERE ( col_1 = 'a' AND col_2 = 'b' )
OR ( col_1 = 'c' AND col_2 = 'd' );
```

For the optimizer to use a range scan, queries must satisfy these conditions:

- Only IN() predicates are used, not NOT IN().
- On the left side of the IN() predicate, the row constructor contains only column references.
- On the right side of the IN() predicate, row constructors contain only runtime constants, which are either literals or local column references that are bound to constants during execution.
- On the right side of the IN() predicate, there is more than one row constructor.

For more information about the optimizer and row constructors, see [Section 10.2.1.22, "Row](#page-73-0) [Constructor Expression Optimization"](#page-73-0)

#### <span id="page-32-1"></span>**Limiting Memory Use for Range Optimization**

To control the memory available to the range optimizer, use the range\_optimizer\_max\_mem\_size system variable:

- A value of 0 means "no limit."
- With a value greater than 0, the optimizer tracks the memory consumed when considering the range access method. If the specified limit is about to be exceeded, the range access method is abandoned and other methods, including a full table scan, are considered instead. This could be less optimal. If this happens, the following warning occurs (where N is the current range\_optimizer\_max\_mem\_size value):

```
Warning 3170 Memory capacity of N bytes for
 'range_optimizer_max_mem_size' exceeded. Range
 optimization was not done for this query.
```

• For UPDATE and DELETE statements, if the optimizer falls back to a full table scan and the sql\_safe\_updates system variable is enabled, an error occurs rather than a warning because, in effect, no key is used to determine which rows to modify. For more information, see Using Safe-Updates Mode (--safe-updates).

For individual queries that exceed the available range optimization memory and for which the optimizer falls back to less optimal plans, increasing the range\_optimizer\_max\_mem\_size value may improve performance.

To estimate the amount of memory needed to process a range expression, use these guidelines:

• For a simple query such as the following, where there is one candidate key for the range access method, each predicate combined with OR uses approximately 230 bytes:

```
SELECT COUNT(*) FROM t
WHERE a=1 OR a=2 OR a=3 OR .. . a=N;
```

• Similarly for a query such as the following, each predicate combined with AND uses approximately 125 bytes:

```
SELECT COUNT(*) FROM t
WHERE a=1 AND b=1 AND c=1 ... N;
```

• For a query with IN() predicates:

```
SELECT COUNT(*) FROM t
WHERE a IN (1,2, ..., M) AND b IN (1,2, ..., N);
```

Each literal value in an IN() list counts as a predicate combined with OR. If there are two IN() lists, the number of predicates combined with OR is the product of the number of literal values in each list. Thus, the number of predicates combined with OR in the preceding case is M × N.

### <span id="page-33-0"></span>**10.2.1.3 Index Merge Optimization**

The Index Merge access method retrieves rows with multiple [range](#page-147-0) scans and merges their results into one. This access method merges index scans from a single table only, not scans across multiple tables. The merge can produce unions, intersections, or unions-of-intersections of its underlying scans.

Example queries for which Index Merge may be used:

```
SELECT * FROM tbl_name WHERE key1 = 10 OR key2 = 20;
SELECT * FROM tbl_name
 WHERE (key1 = 10 OR key2 = 20) AND non_key = 30;
SELECT * FROM t1, t2
 WHERE (t1.key1 IN (1,2) OR t1.key2 LIKE 'value%')
 AND t2.key1 = t1.some_col;
SELECT * FROM t1, t2
 WHERE t1.key1 = 1
 AND (t2.key1 = t1.some_col OR t2.key2 = t1.some_col2);
```

![](_page_33_Picture_15.jpeg)

### **Note**

The Index Merge optimization algorithm has the following known limitations:

• If your query has a complex WHERE clause with deep AND/OR nesting and MySQL does not choose the optimal plan, try distributing terms using the following identity transformations:

```
(x AND y) OR z => (x OR z) AND (y OR z)
(x OR y) AND z => (x AND z) OR (y AND z)
```

• Index Merge is not applicable to full-text indexes.

In EXPLAIN output, the Index Merge method appears as [index\\_merge](#page-146-0) in the type column. In this case, the key column contains a list of indexes used, and key\_len contains a list of the longest key parts for those indexes.

The Index Merge access method has several algorithms, which are displayed in the Extra field of EXPLAIN output:

```
• Using intersect(...)
• Using union(...)
• Using sort_union(...)
```

The following sections describe these algorithms in greater detail. The optimizer chooses between different possible Index Merge algorithms and other access methods based on cost estimates of the various available options.

- [Index Merge Intersection Access Algorithm](#page-34-0)
- [Index Merge Union Access Algorithm](#page-34-1)
- [Index Merge Sort-Union Access Algorithm](#page-35-0)
- [Influencing Index Merge Optimization](#page-35-1)

#### <span id="page-34-0"></span>**Index Merge Intersection Access Algorithm**

This access algorithm is applicable when a WHERE clause is converted to several range conditions on different keys combined with AND, and each condition is one of the following:

• An N-part expression of this form, where the index has exactly N parts (that is, all index parts are covered):

```
key_part1 = const1 AND key_part2 = const2 ... AND key_partN = constN
```

• Any range condition over the primary key of an InnoDB table.

#### Examples:

```
SELECT * FROM innodb_table
 WHERE primary_key < 10 AND key_col1 = 20;
SELECT * FROM tbl_name
 WHERE key1_part1 = 1 AND key1_part2 = 2 AND key2 = 2;
```

The Index Merge intersection algorithm performs simultaneous scans on all used indexes and produces the intersection of row sequences that it receives from the merged index scans.

If all columns used in the query are covered by the used indexes, full table rows are not retrieved (EXPLAIN output contains Using index in Extra field in this case). Here is an example of such a query:

```
SELECT COUNT(*) FROM t1 WHERE key1 = 1 AND key2 = 1;
```

If the used indexes do not cover all columns used in the query, full rows are retrieved only when the range conditions for all used keys are satisfied.

If one of the merged conditions is a condition over the primary key of an InnoDB table, it is not used for row retrieval, but is used to filter out rows retrieved using other conditions.

#### <span id="page-34-1"></span>**Index Merge Union Access Algorithm**

The criteria for this algorithm are similar to those for the Index Merge intersection algorithm. The algorithm is applicable when the table's WHERE clause is converted to several range conditions on different keys combined with OR, and each condition is one of the following:

• An N-part expression of this form, where the index has exactly N parts (that is, all index parts are covered):

```
key_part1 = const1 OR key_part2 = const2 ... OR key_partN = constN
```

- Any range condition over a primary key of an InnoDB table.
- A condition for which the Index Merge intersection algorithm is applicable.

#### Examples:

```
SELECT * FROM t1
 WHERE key1 = 1 OR key2 = 2 OR key3 = 3;
SELECT * FROM innodb_table
 WHERE (key1 = 1 AND key2 = 2)
 OR (key3 = 'foo' AND key4 = 'bar') AND key5 = 5;
```

#### <span id="page-35-0"></span>**Index Merge Sort-Union Access Algorithm**

This access algorithm is applicable when the WHERE clause is converted to several range conditions combined by OR, but the Index Merge union algorithm is not applicable.

#### Examples:

```
SELECT * FROM tbl_name
 WHERE key_col1 < 10 OR key_col2 < 20;
SELECT * FROM tbl_name
 WHERE (key_col1 > 10 OR key_col2 = 20) AND nonkey_col = 30;
```

The difference between the sort-union algorithm and the union algorithm is that the sort-union algorithm must first fetch row IDs for all rows and sort them before returning any rows.

#### <span id="page-35-1"></span>**Influencing Index Merge Optimization**

Use of Index Merge is subject to the value of the [index\\_merge](#page-161-0), [index\\_merge\\_intersection](#page-161-1), [index\\_merge\\_union](#page-161-2), and [index\\_merge\\_sort\\_union](#page-161-3) flags of the optimizer\_switch system variable. See [Section 10.9.2, "Switchable Optimizations".](#page-159-0) By default, all those flags are on. To enable only certain algorithms, set [index\\_merge](#page-161-0) to off, and enable only such of the others as should be permitted.

In addition to using the optimizer\_switch system variable to control optimizer use of the Index Merge algorithms session-wide, MySQL supports optimizer hints to influence the optimizer on a perstatement basis. See [Section 10.9.3, "Optimizer Hints".](#page-169-0)

### <span id="page-35-2"></span>**10.2.1.4 Hash Join Optimization**

By default, MySQL (8.0.18 and later) employs hash joins whenever possible. It is possible to control whether hash joins are employed using one of the [BNL](#page-174-0) and [NO\\_BNL](#page-174-0) optimizer hints, or by setting [block\\_nested\\_loop=on](#page-160-0) or block\_nested\_loop=off as part of the setting for the optimizer\_switch server system variable.

![](_page_35_Picture_17.jpeg)

#### **Note**

MySQL 8.0.18 supported setting a [hash\\_join](#page-161-4) flag in optimizer\_switch, as well as the optimizer hints [HASH\\_JOIN](#page-174-0) and NO\_HASH\_JOIN. In MySQL 8.0.19 and later, none of these have any effect any longer.

Beginning with MySQL 8.0.18, MySQL employs a hash join for any query for which each join has an equi-join condition, and in which there are no indexes that can be applied to any join conditions, such as this one:

```
SELECT *
```

```
FROM t1

JOIN t2

ON t1.c1=t2.c1;
```

A hash join can also be used when there are one or more indexes that can be used for single-table predicates.

A hash join is usually faster than and is intended to be used in such cases instead of the block nested loop algorithm (see Block Nested-Loop Join Algorithm) employed in previous versions of MySQL. Beginning with MySQL 8.0.20, support for block nested loop is removed, and the server employs a hash join wherever a block nested loop would have been used previously.

In the example just shown and the remaining examples in this section, we assume that the three tables t1, t2, and t3 have been created using the following statements:

```
CREATE TABLE t1 (c1 INT, c2 INT);
CREATE TABLE t2 (c1 INT, c2 INT);
CREATE TABLE t3 (c1 INT, c2 INT);
```

You can see that a hash join is being employed by using EXPLAIN, like this:

```
mysql> EXPLAIN
   -> SELECT * FROM t1
   -> JOIN t2 ON t1.c1=t2.c1\G
          ************** 1. row ***************
        id: 1
 select type: SIMPLE
  partitions: NULL
       type: ALL
possible_keys: NULL
        key: NULL
     key len: NULL
        ref: NULL
        rows: 1
    filtered: 100 00
      Extra: NULL
                 ****** 2. row ***************
         id: 1
 select type: SIMPLE
      table: t2
  partitions: NULL
        type: ALL
possible keys: NULL
        key: NULL
     key len: NULL
        ref: NULL
        rows: 1
    filtered: 100.00
       Extra: Using where; Using join buffer (hash join)
```

(Prior to MySQL 8.0.20, it was necessary to include the FORMAT=TREE option to see whether hash joins were being used for a given join.)

EXPLAIN ANALYZE also displays information about hash joins used.

The hash join is used for queries involving multiple joins as well, as long as at least one join condition for each pair of tables is an equi-join, like the query shown here:

```
SELECT * FROM t1

JOIN t2 ON (t1.c1 = t2.c1 AND t1.c2 < t2.c2)

JOIN t3 ON (t2.c1 = t3.c1);
```

In cases like the one just shown, which makes use of an inner join, any extra conditions which are not equi-joins are applied as filters after the join is executed. (For outer joins, such as left joins, semijoins, and antijoins, they are printed as part of the join.) This can be seen here in the output of EXPLAIN:

```
mysql> EXPLAIN FORMAT=TREE
```

```
 -> SELECT *
 -> FROM t1
 -> JOIN t2
 -> ON (t1.c1 = t2.c1 AND t1.c2 < t2.c2)
 -> JOIN t3
 -> ON (t2.c1 = t3.c1)\G
*************************** 1. row ***************************
EXPLAIN: -> Inner hash join (t3.c1 = t1.c1) (cost=1.05 rows=1)
 -> Table scan on t3 (cost=0.35 rows=1)
 -> Hash
 -> Filter: (t1.c2 < t2.c2) (cost=0.70 rows=1)
 -> Inner hash join (t2.c1 = t1.c1) (cost=0.70 rows=1)
 -> Table scan on t2 (cost=0.35 rows=1)
 -> Hash
 -> Table scan on t1 (cost=0.35 rows=1)
```

As also can be seen from the output just shown, multiple hash joins can be (and are) used for joins having multiple equi-join conditions.

Prior to MySQL 8.0.20, a hash join could not be used if any pair of joined tables did not have at least one equi-join condition, and the slower block nested loop algorithm was employed. In MySQL 8.0.20 and later, the hash join is used in such cases, as shown here:

```
mysql> EXPLAIN FORMAT=TREE
 -> SELECT * FROM t1
 -> JOIN t2 ON (t1.c1 = t2.c1)
 -> JOIN t3 ON (t2.c1 < t3.c1)\G
*************************** 1. row ***************************
EXPLAIN: -> Filter: (t1.c1 < t3.c1) (cost=1.05 rows=1)
 -> Inner hash join (no condition) (cost=1.05 rows=1)
 -> Table scan on t3 (cost=0.35 rows=1)
 -> Hash
 -> Inner hash join (t2.c1 = t1.c1) (cost=0.70 rows=1)
 -> Table scan on t2 (cost=0.35 rows=1)
 -> Hash
 -> Table scan on t1 (cost=0.35 rows=1)
```

(Additional examples are provided later in this section.)

A hash join is also applied for a Cartesian product—that is, when no join condition is specified, as shown here:

```
mysql> EXPLAIN FORMAT=TREE
 -> SELECT *
 -> FROM t1
 -> JOIN t2
 -> WHERE t1.c2 > 50\G
*************************** 1. row ***************************
EXPLAIN: -> Inner hash join (cost=0.70 rows=1)
 -> Table scan on t2 (cost=0.35 rows=1)
 -> Hash
 -> Filter: (t1.c2 > 50) (cost=0.35 rows=1)
 -> Table scan on t1 (cost=0.35 rows=1)
```

In MySQL 8.0.20 and later, it is no longer necessary for the join to contain at least one equi-join condition in order for a hash join to be used. This means that the types of queries which can be optimized using hash joins include those in the following list (with examples):

• Inner non-equi-join:

```
mysql> EXPLAIN FORMAT=TREE SELECT * FROM t1 JOIN t2 ON t1.c1 < t2.c1\G
*************************** 1. row ***************************
EXPLAIN: -> Filter: (t1.c1 < t2.c1) (cost=4.70 rows=12)
 -> Inner hash join (no condition) (cost=4.70 rows=12)
 -> Table scan on t2 (cost=0.08 rows=6)
 -> Hash
 -> Table scan on t1 (cost=0.85 rows=6)
```

• Semijoin:

```
mysql> EXPLAIN FORMAT=TREE SELECT * FROM t1
    -> WHERE t1.c1 IN (SELECT t2.c2 FROM t2)\G
*******************************
EXPLAIN: -> Hash semijoin (t2.c2 = t1.c1) (cost=0.70 rows=1)
    -> Table scan on t1 (cost=0.35 rows=1)
    -> Hash
    -> Table scan on t2 (cost=0.35 rows=1)
```

• Antijoin:

```
mysql> EXPLAIN FORMAT=TREE SELECT * FROM t2
```

· Left outer join:

```
mysql> EXPLAIN FORMAT=TREE SELECT * FROM t1 LEFT JOIN t2 ON t1.c1 = t2.c1\G
*************

EXPLAIN: -> Left hash join (t2.c1 = t1.c1) (cost=0.70 rows=1)
    -> Table scan on t1 (cost=0.35 rows=1)
    -> Hash
    -> Table scan on t2 (cost=0.35 rows=1)
```

• Right outer join (observe that MySQL rewrites all right outer joins as left outer joins):

```
mysql> EXPLAIN FORMAT=TREE SELECT * FROM t1 RIGHT JOIN t2 ON t1.c1 = t2.c1\G
**********************************
EXPLAIN: -> Left hash join (t1.c1 = t2.c1) (cost=0.70 rows=1)
    -> Table scan on t2 (cost=0.35 rows=1)
    -> Hash
    -> Table scan on t1 (cost=0.35 rows=1)
```

By default, MySQL 8.0.18 and later employs hash joins whenever possible. It is possible to control whether hash joins are employed using one of the BNL and NO BNL optimizer hints.

(MySQL 8.0.18 supported hash\_join=on or hash\_join=off as part of the setting for the optimizer\_switch server system variable as well as the optimizer hints HASH\_JOIN or NO HASH JOIN. In MySQL 8.0.19 and later, these no longer have any effect.)

Memory usage by hash joins can be controlled using the <code>join\_buffer\_size</code> system variable; a hash join cannot use more memory than this amount. When the memory required for a hash join exceeds the amount available, MySQL handles this by using files on disk. If this happens, you should be aware that the join may not succeed if a hash join cannot fit into memory and it creates more files than set for <code>open\_files\_limit</code>. To avoid such problems, make either of the following changes:

- Increase join buffer size so that the hash join does not spill over to disk.
- Increase open files limit.

Beginning with MySQL 8.0.18, join buffers for hash joins are allocated incrementally; thus, you can set <code>join\_buffer\_size</code> higher without small queries allocating very large amounts of RAM, but outer joins allocate the entire buffer. In MySQL 8.0.20 and later, hash joins are used for outer joins (including antijoins and semijoins) as well, so this is no longer an issue.

#### <span id="page-38-0"></span>10.2.1.5 Engine Condition Pushdown Optimization

This optimization improves the efficiency of direct comparisons between a nonindexed column and a constant. In such cases, the condition is "pushed down" to the storage engine for evaluation. This optimization can be used only by the NDB storage engine.

For NDB Cluster, this optimization can eliminate the need to send nonmatching rows over the network between the cluster's data nodes and the MySQL server that issued the query, and can speed up queries where it is used by a factor of 5 to 10 times over cases where condition pushdown could be but is not used.

Suppose that an NDB Cluster table is defined as follows:

```
CREATE TABLE t1 (
 a INT,
 b INT,
 KEY(a)
) ENGINE=NDB;
```

Engine condition pushdown can be used with queries such as the one shown here, which includes a comparison between a nonindexed column and a constant:

```
SELECT a, b FROM t1 WHERE b = 10;
```

The use of engine condition pushdown can be seen in the output of EXPLAIN:

```
mysql> EXPLAIN SELECT a, b FROM t1 WHERE b = 10\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: t1
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 10
 Extra: Using where with pushed condition
```

However, engine condition pushdown cannot be used with the following query:

```
SELECT a,b FROM t1 WHERE a = 10;
```

Engine condition pushdown is not applicable here because an index exists on column a. (An index access method would be more efficient and so would be chosen in preference to condition pushdown.)

Engine condition pushdown may also be employed when an indexed column is compared with a constant using a > or < operator:

```
mysql> EXPLAIN SELECT a, b FROM t1 WHERE a < 2\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: t1
 type: range
possible_keys: a
 key: a
 key_len: 5
 ref: NULL
 rows: 2
 Extra: Using where with pushed condition
```

Other supported comparisons for engine condition pushdown include the following:

```
• column [NOT] LIKE pattern
```

pattern must be a string literal containing the pattern to be matched; for syntax, see Section 14.8.1, "String Comparison Functions and Operators".

- column IS [NOT] NULL
- column IN (value\_list)

Each item in the value\_list must be a constant, literal value.

• column BETWEEN constant1 AND constant2

constant1 and constant2 must each be a constant, literal value.

In all of the cases in the preceding list, it is possible for the condition to be converted into the form of one or more direct comparisons between a column and a constant.

Engine condition pushdown is enabled by default. To disable it at server startup, set the optimizer\_switch system variable's [engine\\_condition\\_pushdown](#page-160-1) flag to off. For example, in a my.cnf file, use these lines:

```
[mysqld]
optimizer_switch=engine_condition_pushdown=off
```

At runtime, disable condition pushdown like this:

```
SET optimizer_switch='engine_condition_pushdown=off';
```

**Limitations.** Engine condition pushdown is subject to the following limitations:

- Engine condition pushdown is supported only by the NDB storage engine.
- Prior to NDB 8.0.18, columns could be compared with constants or expressions which evaluate to constant values only. In NDB 8.0.18 and later, columns can be compared with one another as long as they are of exactly the same type, including the same signedness, length, character set, precision, and scale, where these are applicable.
- Columns used in comparisons cannot be of any of the BLOB or TEXT types. This exclusion extends to JSON, BIT, and ENUM columns as well.
- A string value to be compared with a column must use the same collation as the column.
- Joins are not directly supported; conditions involving multiple tables are pushed separately where possible. Use extended EXPLAIN output to determine which conditions are actually pushed down. See [Section 10.8.3, "Extended EXPLAIN Output Format"](#page-155-0).

Previously, engine condition pushdown was limited to terms referring to column values from the same table to which the condition was being pushed. Beginning with NDB 8.0.16, column values from tables earlier in the query plan can also be referred to from pushed conditions. This reduces the number of rows which must be handled by the SQL node during join processing. Filtering can be also performed in parallel in the LDM threads, rather than in a single mysqld process. This has the potential to improve performance of queries by a significant margin.

Beginning with NDB 8.0.20, an outer join using a scan can be pushed if there are no unpushable conditions on any table used in the same join nest, or on any table in join nests above it on which it depends. This is also true for a semijoin, provided the optimization strategy employed is firstMatch (see [Section 10.2.2.1, "Optimizing IN and EXISTS Subquery Predicates with Semijoin](#page-75-1) [Transformations"\)](#page-75-1).

Join algorithms cannot be combined with referring columns from previous tables in the following two situations:

1. When any of the referred previous tables are in a join buffer. In this case, each row retrieved from the scan-filtered table is matched against every row in the buffer. This means that there is no single specific row from which column values can be fetched from when generating the scan filter.

2. When the column originates from a child operation in a pushed join. This is because rows referenced from ancestor operations in the join have not yet been retrieved when the scan filter is generated.

Beginning with NDB 8.0.27, columns from ancestor tables in a join can be pushed down, provided that they meet the requirements listed previously. An example of such a query, using the table t1 created previously, is shown here:

```
mysql> EXPLAIN 
 -> SELECT * FROM t1 AS x 
 -> LEFT JOIN t1 AS y 
 -> ON x.a=0 AND y.b>=3\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: x
 partitions: p0,p1
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 4
 filtered: 100.00
 Extra: NULL
*************************** 2. row ***************************
 id: 1
 select_type: SIMPLE
 table: y
 partitions: p0,p1
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 4
 filtered: 100.00
 Extra: Using where; Using pushed condition (`test`.`y`.`b` >= 3); Using join buffer (hash join)
2 rows in set, 2 warnings (0.00 sec)
```

### <span id="page-41-0"></span>**10.2.1.6 Index Condition Pushdown Optimization**

Index Condition Pushdown (ICP) is an optimization for the case where MySQL retrieves rows from a table using an index. Without ICP, the storage engine traverses the index to locate rows in the base table and returns them to the MySQL server which evaluates the WHERE condition for the rows. With ICP enabled, and if parts of the WHERE condition can be evaluated by using only columns from the index, the MySQL server pushes this part of the WHERE condition down to the storage engine. The storage engine then evaluates the pushed index condition by using the index entry and only if this is satisfied is the row read from the table. ICP can reduce the number of times the storage engine must access the base table and the number of times the MySQL server must access the storage engine.

Applicability of the Index Condition Pushdown optimization is subject to these conditions:

- ICP is used for the [range](#page-147-0), [ref](#page-146-1), [eq\\_ref](#page-146-2), and [ref\\_or\\_null](#page-146-3) access methods when there is a need to access full table rows.
- ICP can be used for InnoDB and MyISAM tables, including partitioned InnoDB and MyISAM tables.
- For InnoDB tables, ICP is used only for secondary indexes. The goal of ICP is to reduce the number of full-row reads and thereby reduce I/O operations. For InnoDB clustered indexes, the complete record is already read into the InnoDB buffer. Using ICP in this case does not reduce I/O.
- ICP is not supported with secondary indexes created on virtual generated columns. InnoDB supports secondary indexes on virtual generated columns.
- Conditions that refer to subqueries cannot be pushed down.

- Conditions that refer to stored functions cannot be pushed down. Storage engines cannot invoke stored functions.
- Triggered conditions cannot be pushed down. (For information about triggered conditions, see [Section 10.2.2.3, "Optimizing Subqueries with the EXISTS Strategy".](#page-80-0))
- (MySQL 8.0.30 and later:) Conditions cannot be pushed down to derived tables containing references to system variables.

To understand how this optimization works, first consider how an index scan proceeds when Index Condition Pushdown is not used:

- 1. Get the next row, first by reading the index tuple, and then by using the index tuple to locate and read the full table row.
- 2. Test the part of the WHERE condition that applies to this table. Accept or reject the row based on the test result.

Using Index Condition Pushdown, the scan proceeds like this instead:

- 1. Get the next row's index tuple (but not the full table row).
- 2. Test the part of the WHERE condition that applies to this table and can be checked using only index columns. If the condition is not satisfied, proceed to the index tuple for the next row.
- 3. If the condition is satisfied, use the index tuple to locate and read the full table row.
- 4. Test the remaining part of the WHERE condition that applies to this table. Accept or reject the row based on the test result.

EXPLAIN output shows Using index condition in the Extra column when Index Condition Pushdown is used. It does not show Using index because that does not apply when full table rows must be read.

Suppose that a table contains information about people and their addresses and that the table has an index defined as INDEX (zipcode, lastname, firstname). If we know a person's zipcode value but are not sure about the last name, we can search like this:

```
SELECT * FROM people
 WHERE zipcode='95054'
 AND lastname LIKE '%etrunia%'
 AND address LIKE '%Main Street%';
```

MySQL can use the index to scan through people with zipcode='95054'. The second part (lastname LIKE '%etrunia%') cannot be used to limit the number of rows that must be scanned, so without Index Condition Pushdown, this query must retrieve full table rows for all people who have zipcode='95054'.

With Index Condition Pushdown, MySQL checks the lastname LIKE '%etrunia%' part before reading the full table row. This avoids reading full rows corresponding to index tuples that match the zipcode condition but not the lastname condition.

Index Condition Pushdown is enabled by default. It can be controlled with the optimizer\_switch system variable by setting the [index\\_condition\\_pushdown](#page-161-5) flag:

```
SET optimizer_switch = 'index_condition_pushdown=off';
SET optimizer_switch = 'index_condition_pushdown=on';
```

See [Section 10.9.2, "Switchable Optimizations"](#page-159-0).

### <span id="page-42-0"></span>**10.2.1.7 Nested-Loop Join Algorithms**

MySQL executes joins between tables using a nested-loop algorithm or variations on it.

- [Nested-Loop Join Algorithm](#page-43-1)
- [Block Nested-Loop Join Algorithm](#page-43-0)

#### <span id="page-43-1"></span>**Nested-Loop Join Algorithm**

A simple nested-loop join (NLJ) algorithm reads rows from the first table in a loop one at a time, passing each row to a nested loop that processes the next table in the join. This process is repeated as many times as there remain tables to be joined.

Assume that a join between three tables t1, t2, and t3 is to be executed using the following join types:

```
Table Join Type
t1 range
t2 ref
t3 ALL
```

If a simple NLJ algorithm is used, the join is processed like this:

```
for each row in t1 matching range {
 for each row in t2 matching reference key {
 for each row in t3 {
 if row satisfies join conditions, send to client
 }
 }
}
```

Because the NLJ algorithm passes rows one at a time from outer loops to inner loops, it typically reads tables processed in the inner loops many times.

#### <span id="page-43-0"></span>**Block Nested-Loop Join Algorithm**

A Block Nested-Loop (BNL) join algorithm uses buffering of rows read in outer loops to reduce the number of times that tables in inner loops must be read. For example, if 10 rows are read into a buffer and the buffer is passed to the next inner loop, each row read in the inner loop can be compared against all 10 rows in the buffer. This reduces by an order of magnitude the number of times the inner table must be read.

Prior to MySQL 8.0.18, this algorithm was applied for equi-joins when no indexes could be used; in MySQL 8.0.18 and later, the hash join optimization is employed in such cases. Starting with MySQL 8.0.20, the block nested loop is no longer used by MySQL, and a hash join is employed for in all cases where the block nested loop was used previously. See [Section 10.2.1.4, "Hash Join Optimization".](#page-35-2)

MySQL join buffering has these characteristics:

- Join buffering can be used when the join is of type [ALL](#page-147-1) or [index](#page-147-2) (in other words, when no possible keys can be used, and a full scan is done, of either the data or index rows, respectively), or [range](#page-147-0). Use of buffering is also applicable to outer joins, as described in [Section 10.2.1.12, "Block Nested-](#page-54-0)[Loop and Batched Key Access Joins".](#page-54-0)
- A join buffer is never allocated for the first nonconstant table, even if it would be of type [ALL](#page-147-1) or [index](#page-147-2).
- Only columns of interest to a join are stored in its join buffer, not whole rows.
- The join\_buffer\_size system variable determines the size of each join buffer used to process a query.
- One buffer is allocated for each join that can be buffered, so a given query might be processed using multiple join buffers.
- A join buffer is allocated prior to executing the join and freed after the query is done.

For the example join described previously for the NLJ algorithm (without buffering), the join is done as follows using join buffering:

```
for each row in t1 matching range {
 for each row in t2 matching reference key {
 store used columns from t1, t2 in join buffer
 if buffer is full {
 for each row in t3 {
 for each t1, t2 combination in join buffer {
 if row satisfies join conditions, send to client
 }
 }
 empty join buffer
 }
 }
}
if buffer is not empty {
 for each row in t3 {
 for each t1, t2 combination in join buffer {
 if row satisfies join conditions, send to client
 }
 }
}
```

If S is the size of each stored t1, t2 combination in the join buffer and C is the number of combinations in the buffer, the number of times table t3 is scanned is:

```
(S * C)/join_buffer_size + 1
```

The number of t3 scans decreases as the value of join\_buffer\_size increases, up to the point when join\_buffer\_size is large enough to hold all previous row combinations. At that point, no speed is gained by making it larger.