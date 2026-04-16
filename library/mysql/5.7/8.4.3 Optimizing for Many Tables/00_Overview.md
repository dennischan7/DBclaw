---
source: MySQL 5.7 Reference
title: 00_Overview
---

Some techniques for keeping individual queries fast involve splitting data across many tables. When the number of tables runs into the thousands or even millions, the overhead of dealing with all these tables becomes a new performance consideration.

## <span id="page-47-0"></span>**8.4.3.1 How MySQL Opens and Closes Tables**

When you execute a mysqladmin status command, you should see something like this:

```
Uptime: 426 Running threads: 1 Questions: 11082
Reloads: 1 Open tables: 12
```

The Open tables value of 12 can be somewhat puzzling if you have fewer than 12 tables.

MySQL is multithreaded, so there may be many clients issuing queries for a given table simultaneously. To minimize the problem with multiple client sessions having different states on the same table, the table is opened independently by each concurrent session. This uses additional memory but normally increases performance. With MyISAM tables, one extra file descriptor is required for the data file for each client that has the table open. (By contrast, the index file descriptor is shared between all sessions.)

The table\_open\_cache and max\_connections system variables affect the maximum number of files the server keeps open. If you increase one or both of these values, you may run up against a limit imposed by your operating system on the per-process number of open file descriptors. Many operating systems permit you to increase the open-files limit, although the method varies widely from system to system. Consult your operating system documentation to determine whether it is possible to increase the limit and how to do so.

table\_open\_cache is related to max\_connections. For example, for 200 concurrent running connections, specify a table cache size of at least 200 \* N, where N is the maximum number of tables per join in any of the queries which you execute. You must also reserve some extra file descriptors for temporary tables and files.

Make sure that your operating system can handle the number of open file descriptors implied by the table\_open\_cache setting. If table\_open\_cache is set too high, MySQL may run out of file descriptors and exhibit symptoms such as refusing connections or failing to perform queries.

Also take into account that the MyISAM storage engine needs two file descriptors for each unique open table. For a partitioned MyISAM table, two file descriptors are required for each partition of the opened table. (When MyISAM opens a partitioned table, it opens every partition of this table, whether or not a given partition is actually used. See MyISAM and partition file descriptor usage.) To increase the number of file descriptors available to MySQL, set the open\_files\_limit system variable. See Section B.3.2.16, "File Not Found and Similar Errors".

The cache of open tables is kept at a level of table\_open\_cache entries. The server autosizes the cache size at startup. To set the size explicitly, set the table\_open\_cache system variable at startup. MySQL may temporarily open more tables than this to execute queries, as described later in this section.

MySQL closes an unused table and removes it from the table cache under the following circumstances:

- When the cache is full and a thread tries to open a table that is not in the cache.
- When the cache contains more than table\_open\_cache entries and a table in the cache is no longer being used by any threads.
- When a table-flushing operation occurs. This happens when someone issues a FLUSH TABLES statement or executes a mysqladmin flush-tables or mysqladmin refresh command.

When the table cache fills up, the server uses the following procedure to locate a cache entry to use:

- Tables not currently in use are released, beginning with the table least recently used.
- If a new table must be opened, but the cache is full and no tables can be released, the cache is temporarily extended as necessary. When the cache is in a temporarily extended state and a table goes from a used to unused state, the table is closed and released from the cache.

A MyISAM table is opened for each concurrent access. This means the table needs to be opened twice if two threads access the same table or if a thread accesses the table twice in the same query (for example, by joining the table to itself). Each concurrent open requires an entry in the table cache. The first open of any MyISAM table takes two file descriptors: one for the data file and one for the index file. Each additional use of the table takes only one file descriptor for the data file. The index file descriptor is shared among all threads.

If you are opening a table with the HANDLER tbl\_name OPEN statement, a dedicated table object is allocated for the thread. This table object is not shared by other threads and is not closed until the thread calls HANDLER tbl\_name CLOSE or the thread terminates. When this happens, the table is put back in the table cache (if the cache is not full). See Section 13.2.4, "HANDLER Statement".

To determine whether your table cache is too small, check the Opened\_tables status variable, which indicates the number of table-opening operations since the server started:

```
mysql> SHOW GLOBAL STATUS LIKE 'Opened_tables';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| Opened_tables | 2741 |
+---------------+-------+
```

If the value is very large or increases rapidly, even when you have not issued many FLUSH TABLES statements, increase the table\_open\_cache value at server startup.

### **8.4.3.2 Disadvantages of Creating Many Tables in the Same Database**

If you have many MyISAM tables in the same database directory, open, close, and create operations are slow. If you execute SELECT statements on many different tables, there is a little overhead when the table cache is full, because for every table that has to be opened, another must be closed. You can reduce this overhead by increasing the number of entries permitted in the table cache.

# <span id="page-48-0"></span>**8.4.4 Internal Temporary Table Use in MySQL**

In some cases, the server creates internal temporary tables while processing statements. Users have no direct control over when this occurs.

The server creates temporary tables under conditions such as these:

- Evaluation of UNION statements, with some exceptions described later.
- Evaluation of some views, such those that use the TEMPTABLE algorithm, UNION, or aggregation.
- Evaluation of derived tables (see Section 13.2.10.8, "Derived Tables").

- Tables created for subquery or semijoin materialization (see [Section 8.2.2, "Optimizing Subqueries,](#page-13-0) [Derived Tables, and View References"](#page-13-0)).
- Evaluation of statements that contain an ORDER BY clause and a different GROUP BY clause, or for which the ORDER BY or GROUP BY contains columns from tables other than the first table in the join queue.
- Evaluation of DISTINCT combined with ORDER BY may require a temporary table.
- For queries that use the SQL\_SMALL\_RESULT modifier, MySQL uses an in-memory temporary table, unless the query also contains elements (described later) that require on-disk storage.
- To evaluate INSERT ... SELECT statements that select from and insert into the same table, MySQL creates an internal temporary table to hold the rows from the SELECT, then inserts those rows into the target table. See Section 13.2.5.1, "INSERT ... SELECT Statement".
- Evaluation of multiple-table UPDATE statements.
- Evaluation of GROUP\_CONCAT() or COUNT(DISTINCT) expressions.

To determine whether a statement requires a temporary table, use EXPLAIN and check the Extra column to see whether it says Using temporary (see [Section 8.8.1, "Optimizing Queries with](#page-68-0) [EXPLAIN"\)](#page-68-0). EXPLAIN does not necessarily say Using temporary for derived or materialized temporary tables.

Some query conditions prevent the use of an in-memory temporary table, in which case the server uses an on-disk table instead:

- Presence of a BLOB or TEXT column in the table. This includes user-defined variables having a string value because they are treated as BLOB or TEXT columns, depending on whether their value is a binary or nonbinary string, respectively.
- Presence of any string column with a maximum length larger than 512 (bytes for binary strings, characters for nonbinary strings) in the SELECT list, if UNION or UNION ALL is used.
- The SHOW COLUMNS and DESCRIBE statements use BLOB as the type for some columns, thus the temporary table used for the results is an on-disk table.

The server does not use a temporary table for UNION statements that meet certain qualifications. Instead, it retains from temporary table creation only the data structures necessary to perform result column typecasting. The table is not fully instantiated and no rows are written to or read from it; rows are sent directly to the client. The result is reduced memory and disk requirements, and smaller delay before the first row is sent to the client because the server need not wait until the last query block is executed. EXPLAIN and optimizer trace output reflects this execution strategy: The UNION RESULT query block is not present because that block corresponds to the part that reads from the temporary table.

These conditions qualify a UNION for evaluation without a temporary table:

- The union is UNION ALL, not UNION or UNION DISTINCT.
- There is no global ORDER BY clause.
- The union is not the top-level query block of an {INSERT | REPLACE} ... SELECT ... statement.

### **Internal Temporary Table Storage Engine**

An internal temporary table can be held in memory and processed by the MEMORY storage engine, or stored on disk by the InnoDB or MyISAM storage engine.

If an internal temporary table is created as an in-memory table but becomes too large, MySQL automatically converts it to an on-disk table. The maximum size for in-memory temporary tables is defined by the tmp\_table\_size or max\_heap\_table\_size value, whichever is smaller. This differs from MEMORY tables explicitly created with CREATE TABLE. For such tables, only the max\_heap\_table\_size variable determines how large a table can grow, and there is no conversion to on-disk format.

The internal\_tmp\_disk\_storage\_engine variable defines the storage engine the server uses to manage on-disk internal temporary tables. Permitted values are INNODB (the default) and MYISAM.

![](_page_50_Picture_3.jpeg)

#### **Note**

When using internal\_tmp\_disk\_storage\_engine=INNODB, queries that generate on-disk internal temporary tables that exceed InnoDB row or column limits return Row size too large or Too many columns errors. The workaround is to set internal\_tmp\_disk\_storage\_engine to MYISAM.

When an internal temporary table is created in memory or on disk, the server increments the Created\_tmp\_tables value. When an internal temporary table is created on disk, the server increments the Created\_tmp\_disk\_tables value. If too many internal temporary tables are created on disk, consider increasing the tmp\_table\_size and max\_heap\_table\_size settings.

## **Internal Temporary Table Storage Format**

In-memory temporary tables are managed by the MEMORY storage engine, which uses fixed-length row format. VARCHAR and VARBINARY column values are padded to the maximum column length, in effect storing them as CHAR and BINARY columns.

On-disk temporary tables are managed by the InnoDB or MyISAM storage engine (depending on the internal\_tmp\_disk\_storage\_engine setting). Both engines store temporary tables using dynamic-width row format. Columns take only as much storage as needed, which reduces disk I/O, space requirements, and processing time compared to on-disk tables that use fixed-length rows.

For statements that initially create an internal temporary table in memory, then convert it to an on-disk table, better performance might be achieved by skipping the conversion step and creating the table on disk to begin with. The big\_tables variable can be used to force disk storage of internal temporary tables.