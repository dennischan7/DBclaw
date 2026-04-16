---
source: MySQL 5.7 Reference
title: 00_Overview
---

# <span id="page-195-1"></span>**13.8.1 DESCRIBE Statement**

The [DESCRIBE](#page-195-1) and [EXPLAIN](#page-195-0) statements are synonyms, used either to obtain information about table structure or query execution plans. For more information, see [Section 13.7.5.5, "SHOW COLUMNS](#page-138-0) [Statement",](#page-138-0) and [Section 13.8.2, "EXPLAIN Statement".](#page-195-0)

# <span id="page-195-0"></span>**13.8.2 EXPLAIN Statement**

```
{EXPLAIN | DESCRIBE | DESC}
 tbl_name [col_name | wild]
{EXPLAIN | DESCRIBE | DESC}
 [explain_type]
 {explainable_stmt | FOR CONNECTION connection_id}
explain_type: {
 EXTENDED
 | PARTITIONS
 | FORMAT = format_name
}
format_name: {
 TRADITIONAL
 | JSON
}
explainable_stmt: {
 SELECT statement
 | DELETE statement
 | INSERT statement
 | REPLACE statement
 | UPDATE statement
}
```

The [DESCRIBE](#page-195-1) and [EXPLAIN](#page-195-0) statements are synonyms. In practice, the [DESCRIBE](#page-195-1) keyword is more often used to obtain information about table structure, whereas [EXPLAIN](#page-195-0) is used to obtain a query execution plan (that is, an explanation of how MySQL would execute a query).

The following discussion uses the [DESCRIBE](#page-195-1) and [EXPLAIN](#page-195-0) keywords in accordance with those uses, but the MySQL parser treats them as completely synonymous.

- [Obtaining Table Structure Information](#page-195-2)
- [Obtaining Execution Plan Information](#page-196-0)

## <span id="page-195-2"></span>**Obtaining Table Structure Information**

[DESCRIBE](#page-195-1) provides information about the columns in a table:

```
mysql> DESCRIBE City;
```

| +++++++<br>  Field<br>  Type                                                                                                                                                      |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| +++++++<br>  Id<br>  int(11)   NO<br>  Name<br>  char(35)   NO<br>  Country<br>  char(3)   NO<br>  District<br>  char(20)   YES   MUL  <br>  Population   int(11)   NO<br>+++++++ |

[DESCRIBE](#page-195-1) is a shortcut for [SHOW COLUMNS](#page-138-0). These statements also display information for views. The description for [SHOW COLUMNS](#page-138-0) provides more information about the output columns. See [Section 13.7.5.5, "SHOW COLUMNS Statement".](#page-138-0)

By default, [DESCRIBE](#page-195-1) displays information about all columns in the table. col\_name, if given, is the name of a column in the table. In this case, the statement displays information only for the named column. wild, if given, is a pattern string. It can contain the SQL % and \_ wildcard characters. In this case, the statement displays output only for the columns with names matching the string. There is no need to enclose the string within quotation marks unless it contains spaces or other special characters.

The [DESCRIBE](#page-195-1) statement is provided for compatibility with Oracle.

The [SHOW CREATE TABLE](#page-142-0), [SHOW TABLE STATUS](#page-175-0), and [SHOW INDEX](#page-154-1) statements also provide information about tables. See [Section 13.7.5, "SHOW Statements"](#page-134-0).

# <span id="page-196-0"></span>**Obtaining Execution Plan Information**

The [EXPLAIN](#page-195-0) statement provides information about how MySQL executes statements:

- [EXPLAIN](#page-195-0) works with SELECT, DELETE, INSERT, REPLACE, and [UPDATE](#page-8-0) statements.
- When [EXPLAIN](#page-195-0) is used with an explainable statement, MySQL displays information from the optimizer about the statement execution plan. That is, MySQL explains how it would process the statement, including information about how tables are joined and in which order. For information about using [EXPLAIN](#page-195-0) to obtain execution plan information, see Section 8.8.2, "EXPLAIN Output Format".
- When [EXPLAIN](#page-195-0) is used with FOR CONNECTION connection\_id rather than an explainable statement, it displays the execution plan for the statement executing in the named connection. See Section 8.8.4, "Obtaining Execution Plan Information for a Named Connection".
- For SELECT statements, [EXPLAIN](#page-195-0) produces additional execution plan information that can be displayed using [SHOW WARNINGS](#page-182-0). See Section 8.8.3, "Extended EXPLAIN Output Format".

![](_page_196_Picture_12.jpeg)

### **Note**

In older MySQL releases, extended information was produced using [EXPLAIN EXTENDED](#page-195-0). That syntax is still recognized for backward compatibility but extended output is now enabled by default, so the EXTENDED keyword is superfluous and deprecated. Its use results in a warning, and it is removed from [EXPLAIN](#page-195-0) syntax in MySQL 8.0.

• [EXPLAIN](#page-195-0) is useful for examining queries involving partitioned tables. See Section 22.3.5, "Obtaining Information About Partitions".

![](_page_196_Picture_16.jpeg)

# **Note**

In older MySQL releases, partition information was produced using [EXPLAIN](#page-195-0) [PARTITIONS](#page-195-0). That syntax is still recognized for backward compatibility but partition output is now enabled by default, so the PARTITIONS keyword is superfluous and deprecated. Its use results in a warning, and it is removed from [EXPLAIN](#page-195-0) syntax in MySQL 8.0.

• The FORMAT option can be used to select the output format. TRADITIONAL presents the output in tabular format. This is the default if no FORMAT option is present. JSON format displays the information in JSON format.

For complex statements, the JSON output can be quite large; in particular, it can be difficult when reading it to pair the closing bracket and opening brackets; to cause the JSON structure's key, if it has one, to be repeated near the closing bracket, set end\_markers\_in\_json=ON. You should be aware that while this makes the output easier to read, it also renders the JSON invalid, causing JSON functions to raise an error.

[EXPLAIN](#page-195-0) requires the same privileges required to execute the explained statement. Additionally, [EXPLAIN](#page-195-0) also requires the SHOW VIEW privilege for any explained view.

With the help of [EXPLAIN](#page-195-0), you can see where you should add indexes to tables so that the statement executes faster by using indexes to find rows. You can also use [EXPLAIN](#page-195-0) to check whether the optimizer joins the tables in an optimal order. To give a hint to the optimizer to use a join order corresponding to the order in which the tables are named in a SELECT statement, begin the statement with SELECT STRAIGHT\_JOIN rather than just SELECT. (See Section 13.2.9, "SELECT Statement".)

The optimizer trace may sometimes provide information complementary to that of [EXPLAIN](#page-195-0). However, the optimizer trace format and content are subject to change between versions. For details, see Section 8.15, "Tracing the Optimizer".

If you have a problem with indexes not being used when you believe that they should be, run [ANALYZE](#page-116-0) [TABLE](#page-116-0) to update table statistics, such as cardinality of keys, that can affect the choices the optimizer makes. See [Section 13.7.2.1, "ANALYZE TABLE Statement"](#page-116-0).

![](_page_197_Picture_7.jpeg)

#### **Note**

MySQL Workbench has a Visual Explain capability that provides a visual representation of [EXPLAIN](#page-195-0) output. See [Tutorial: Using Explain to Improve](https://dev.mysql.com/doc/workbench/en/wb-tutorial-visual-explain-dbt3.md) [Query Performance](https://dev.mysql.com/doc/workbench/en/wb-tutorial-visual-explain-dbt3.md).

# <span id="page-197-0"></span>**13.8.3 HELP Statement**

HELP 'search\_string'

The [HELP](#page-197-0) statement returns online information from the MySQL Reference Manual. Its proper operation requires that the help tables in the mysql database be initialized with help topic information (see Section 5.1.14, "Server-Side Help Support").

The [HELP](#page-197-0) statement searches the help tables for the given search string and displays the result of the search. The search string is not case-sensitive.

The search string can contain the wildcard characters % and \_. These have the same meaning as for pattern-matching operations performed with the LIKE operator. For example, HELP 'rep%' returns a list of topics that begin with rep.

The HELP statement does not require a terminator such as ; or \G.

The HELP statement understands several types of search strings:

• At the most general level, use contents to retrieve a list of the top-level help categories:

HELP 'contents'

• For a list of topics in a given help category, such as Data Types, use the category name:

HELP 'data types'

• For help on a specific help topic, such as the ASCII() function or the CREATE TABLE statement, use the associated keyword or keywords:

```
HELP 'ascii'
HELP 'create table'
```

In other words, the search string matches a category, many topics, or a single topic. The following descriptions indicate the forms that the result set can take.

• Empty result

No match could be found for the search string.

```
Example: HELP 'fake'
Yields:
Nothing found
Please try to run 'help contents' for a list of all accessible topics
```

• Result set containing a single row

This means that the search string yielded a hit for the help topic. The result includes the following items:

- name: The topic name.
- description: Descriptive help text for the topic.
- example: One or more usage examples. (May be empty.)

```
Example: HELP 'log'
```

Yields:

```
Name: 'LOG'
Description:
Syntax:
LOG(X), LOG(B,X)
If called with one parameter, this function returns the natural
logarithm of X. If X is less than or equal to 0.0E0, the function
returns NULL and a warning "Invalid argument for logarithm" is
reported. Returns NULL if X or B is NULL.
The inverse of this function (when called with a single argument) is
the EXP() function.
URL: https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html
Examples:
mysql> SELECT LOG(2);
 -> 0.69314718055995
mysql> SELECT LOG(-2);
 -> NULL
```

• List of topics.

This means that the search string matched multiple help topics.

```
Example: HELP 'status'
```

Yields:

```
Many help items for your request exist.
To make a more specific request, please type 'help <item>',
where <item> is one of the following topics:
 FLUSH
 SHOW
 SHOW ENGINE
```

```
 SHOW FUNCTION STATUS
 SHOW MASTER STATUS
 SHOW PROCEDURE STATUS
 SHOW SLAVE STATUS
 SHOW STATUS
 SHOW TABLE STATUS
```

• List of topics.

A list is also displayed if the search string matches a category.

```
Example: HELP 'functions'
```

#### Yields:

```
You asked for help about help category: "Functions"
For more information, type 'help <item>', where <item> is one of the following
categories:
 Aggregate Functions and Modifiers
 Bit Functions
 Cast Functions and Operators
 Comparison Operators
 Date and Time Functions
 Encryption Functions
 Enterprise Encryption Functions
 Flow Control Functions
 GROUP BY Functions and Modifiers
 GTID
 Information Functions
 Locking Functions
 Logical Operators
 Miscellaneous Functions
 Numeric Functions
 Spatial Functions
 String Functions
 XML
```

# <span id="page-199-0"></span>**13.8.4 USE Statement**

```
USE db_name
```

The [USE](#page-199-0) statement tells MySQL to use the named database as the default (current) database for subsequent statements. This statement requires some privilege for the database or some object within it.

The named database remains the default until the end of the session or another [USE](#page-199-0) statement is issued:

```
USE db1;
SELECT COUNT(*) FROM mytable; # selects from db1.mytable
USE db2;
SELECT COUNT(*) FROM mytable; # selects from db2.mytable
```

The database name must be specified on a single line. Newlines in database names are not supported.

Making a particular database the default by means of the [USE](#page-199-0) statement does not preclude accessing tables in other databases. The following example accesses the author table from the db1 database and the editor table from the db2 database:

```
USE db1;
SELECT author_name,editor_name FROM author,db2.editor
 WHERE author.editor_id = db2.editor.editor_id;
```

# <span id="page-0-0"></span>Chapter 14 The InnoDB Storage Engine

# **Table of Contents**

| 14.1 Introduction to InnoDB                                    |      |
|----------------------------------------------------------------|------|
| 14.1.1 Benefits of Using InnoDB Tables                         | 2376 |
| 14.1.2 Best Practices for InnoDB Tables                        | 2377 |
| 14.1.3 Verifying that InnoDB is the Default Storage Engine     | 2377 |
| 14.1.4 Testing and Benchmarking with InnoDB                    | 2378 |
| 14.1.5 Turning Off InnoDB                                      | 2378 |
| 14.2 InnoDB and the ACID Model                                 |      |
| 14.3 InnoDB Multi-Versioning                                   | 2380 |
| 14.4 InnoDB Architecture                                       | 2381 |
| 14.5 InnoDB In-Memory Structures                               | 2382 |
| 14.5.1 Buffer Pool                                             | 2382 |
| 14.5.2 Change Buffer                                           | 2387 |
| 14.5.3 Adaptive Hash Index                                     | 2390 |
| 14.5.4 Log Buffer                                              | 2391 |
| 14.6 InnoDB On-Disk Structures                                 | 2391 |
| 14.6.1 Tables                                                  | 2391 |
| 14.6.2 Indexes                                                 | 2414 |
| 14.6.3 Tablespaces                                             | 2421 |
| 14.6.4 InnoDB Data Dictionary                                  |      |
| 14.6.5 Doublewrite Buffer                                      | 2436 |
| 14.6.6 Redo Log                                                |      |
| 14.6.7 Undo Logs                                               |      |
| 14.7 InnoDB Locking and Transaction Model                      |      |
| 14.7.1 InnoDB Locking                                          |      |
| 14.7.2 InnoDB Transaction Model                                |      |
| 14.7.3 Locks Set by Different SQL Statements in InnoDB         |      |
| 14.7.4 Phantom Rows                                            |      |
| 14.7.5 Deadlocks in InnoDB                                     |      |
| 14.8 InnoDB Configuration                                      |      |
| 14.8.1 InnoDB Startup Configuration                            |      |
| 14.8.2 Configuring InnoDB for Read-Only Operation              | 2463 |
| 14.8.3 InnoDB Buffer Pool Configuration                        |      |
| 14.8.4 Configuring the Memory Allocator for InnoDB             |      |
| 14.8.5 Configuring Thread Concurrency for InnoDB               |      |
| 14.8.6 Configuring the Number of Background InnoDB I/O Threads |      |
| 14.8.7 Using Asynchronous I/O on Linux                         |      |
| 14.8.8 Configuring InnoDB I/O Capacity                         |      |
| 14.8.9 Configuring Spin Lock Polling                           |      |
| 14.8.10 Purge Configuration                                    |      |
| 14.8.11 Configuring Optimizer Statistics for InnoDB            |      |
| 14.8.12 Configuring the Merge Threshold for Index Pages        |      |
| 14.9 InnoDB Table and Page Compression                         |      |
| 14.9.1 InnoDB Table Compression                                |      |
| 14.9.2 InnoDB Page Compression                                 |      |
| 14.10 InnoDB File-Format Management                            |      |
| 14.10.1 Enabling File Formats                                  |      |
| 14.10.2 Verifying File Format Compatibility                    |      |
| 14.10.3 Identifying the File Format in Use                     |      |
| 14.10.4 Modifying the File Format                              |      |
| 14.11 InnoDB Row Formats                                       |      |
| 14.12 InnoDB Disk I/O and File Space Management                |      |
| 14.12.1 InnoDB Disk I/O                                        | 2525 |

| 14.12.2 File Space Management                                                           | 2526 |
|-----------------------------------------------------------------------------------------|------|
| 14.12.3 InnoDB Checkpoints                                                              | 2527 |
| 14.12.4 Defragmenting a Table 2527                                                      |      |
| 14.12.5 Reclaiming Disk Space with TRUNCATE TABLE 2528                                  |      |
| 14.13 InnoDB and Online DDL 2528                                                        |      |
| 14.13.1 Online DDL Operations 2529                                                      |      |
| 14.13.2 Online DDL Performance and Concurrency 2541                                     |      |
| 14.13.3 Online DDL Space Requirements 2544                                              |      |
| 14.13.4 Simplifying DDL Statements with Online DDL 2545                                 |      |
| 14.13.5 Online DDL Failure Conditions 2545                                              |      |
| 14.13.6 Online DDL Limitations                                                          | 2546 |
| 14.14 InnoDB Data-at-Rest Encryption 2547                                               |      |
| 14.15 InnoDB Startup Options and System Variables                                       | 2551 |
| 14.16 InnoDB INFORMATION_SCHEMA Tables 2629                                             |      |
| 14.16.1 InnoDB INFORMATION_SCHEMA Tables about Compression 2629                         |      |
| 14.16.2 InnoDB INFORMATION_SCHEMA Transaction and Locking Information 2631              |      |
| 14.16.3 InnoDB INFORMATION_SCHEMA System Tables 2638                                    |      |
| 14.16.4 InnoDB INFORMATION_SCHEMA FULLTEXT Index Tables 2643                            |      |
| 14.16.5 InnoDB INFORMATION_SCHEMA Buffer Pool Tables 2646                               |      |
| 14.16.6 InnoDB INFORMATION_SCHEMA Metrics Table 2650                                    |      |
| 14.16.7 InnoDB INFORMATION_SCHEMA Temporary Table Info Table 2658                       |      |
| 14.16.8 Retrieving InnoDB Tablespace Metadata from INFORMATION_SCHEMA.FILES 2659        |      |
| 14.17 InnoDB Integration with MySQL Performance Schema 2661                             |      |
| 14.17.1 Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance Schema 2662 |      |
| 14.17.2 Monitoring InnoDB Mutex Waits Using Performance Schema 2664                     |      |
| 14.18 InnoDB Monitors 2668                                                              |      |
| 14.18.1 InnoDB Monitor Types 2668                                                       |      |
| 14.18.2 Enabling InnoDB Monitors 2668                                                   |      |
| 14.18.3 InnoDB Standard Monitor and Lock Monitor Output 2670                            |      |
| 14.19 InnoDB Backup and Recovery                                                        | 2675 |
| 14.19.1 InnoDB Backup 2675                                                              |      |
| 14.19.2 InnoDB Recovery 2676                                                            |      |
| 14.20 InnoDB and MySQL Replication 2679                                                 |      |
| 14.21 InnoDB memcached Plugin 2680                                                      |      |
| 14.21.1 Benefits of the InnoDB memcached Plugin 2681                                    |      |
| 14.21.2 InnoDB memcached Architecture 2682                                              |      |
| 14.21.3 Setting Up the InnoDB memcached Plugin 2683                                     |      |
| 14.21.4 Security Considerations for the InnoDB memcached Plugin 2688                    |      |
| 14.21.5 Writing Applications for the InnoDB memcached Plugin 2690                       |      |
| 14.21.6 The InnoDB memcached Plugin and Replication                                     | 2702 |
| 14.21.7 InnoDB memcached Plugin Internals                                               | 2705 |
|                                                                                         |      |
|                                                                                         |      |
| 14.21.8 Troubleshooting the InnoDB memcached Plugin 2710                                |      |
| 14.22 InnoDB Troubleshooting 2712                                                       |      |
| 14.22.1 Troubleshooting InnoDB I/O Problems 2713                                        |      |
| 14.22.2 Forcing InnoDB Recovery                                                         | 2713 |
| 14.22.3 Troubleshooting InnoDB Data Dictionary Operations 2715                          |      |
| 14.22.4 InnoDB Error Handling 2719                                                      |      |
| 14.23 InnoDB Limits 2719<br>14.24 InnoDB Restrictions and Limitations                   | 2721 |

# <span id="page-1-0"></span>**14.1 Introduction to InnoDB**

InnoDB is a general-purpose storage engine that balances high reliability and high performance. In MySQL 5.7, InnoDB is the default MySQL storage engine. Unless you have configured a different default storage engine, issuing a CREATE TABLE statement without an ENGINE clause creates an InnoDB table.

# **Key Advantages of InnoDB**

- Its DML operations follow the ACID model, with transactions featuring commit, rollback, and crashrecovery capabilities to protect user data. See [Section 14.2, "InnoDB and the ACID Model".](#page-5-2)
- Row-level locking and Oracle-style consistent reads increase multi-user concurrency and performance. See [Section 14.7, "InnoDB Locking and Transaction Model"](#page-65-0).
- InnoDB tables arrange your data on disk to optimize queries based on primary keys. Each InnoDB table has a primary key index called the clustered index that organizes the data to minimize I/O for primary key lookups. See [Section 14.6.2.1, "Clustered and Secondary Indexes"](#page-41-1).
- To maintain data integrity, InnoDB supports FOREIGN KEY constraints. With foreign keys, inserts, updates, and deletes are checked to ensure they do not result in inconsistencies across related tables. See Section 13.1.18.5, "FOREIGN KEY Constraints".

**Table 14.1 InnoDB Storage Engine Features**

| Feature                                                                                          | Support                                                                                                                       |
|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| B-tree indexes                                                                                   | Yes                                                                                                                           |
| Backup/point-in-time recovery (Implemented in<br>the server, rather than in the storage engine.) | Yes                                                                                                                           |
| Cluster database support                                                                         | No                                                                                                                            |
| Clustered indexes                                                                                | Yes                                                                                                                           |
| Compressed data                                                                                  | Yes                                                                                                                           |
| Data caches                                                                                      | Yes                                                                                                                           |
| Encrypted data                                                                                   | Yes (Implemented in the server via encryption<br>functions; In MySQL 5.7 and later, data-at-rest<br>encryption is supported.) |
| Foreign key support                                                                              | Yes                                                                                                                           |
| Full-text search indexes                                                                         | Yes (Support for FULLTEXT indexes is available<br>in MySQL 5.6 and later.)                                                    |
| Geospatial data type support                                                                     | Yes                                                                                                                           |
| Geospatial indexing support                                                                      | Yes (Support for geospatial indexing is available in<br>MySQL 5.7 and later.)                                                 |
| Hash indexes                                                                                     | No (InnoDB utilizes hash indexes internally for its<br>Adaptive Hash Index feature.)                                          |
| Index caches                                                                                     | Yes                                                                                                                           |
| Locking granularity                                                                              | Row                                                                                                                           |
| MVCC                                                                                             | Yes                                                                                                                           |
| Replication support (Implemented in the server,<br>rather than in the storage engine.)           | Yes                                                                                                                           |
| Storage limits                                                                                   | 64TB                                                                                                                          |
| T-tree indexes                                                                                   | No                                                                                                                            |
| Transactions                                                                                     | Yes                                                                                                                           |
| Update statistics for data dictionary                                                            | Yes                                                                                                                           |

To compare the features of InnoDB with other storage engines provided with MySQL, see the Storage Engine Features table in Chapter 15, Alternative Storage Engines.

# **InnoDB Enhancements and New Features**

For information about InnoDB enhancements and new features, refer to:

- The InnoDB enhancements list in Section 1.3, "What Is New in MySQL 5.7".
- The [Release Notes.](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/)

# **Additional InnoDB Information and Resources**

- For InnoDB-related terms and definitions, see the MySQL Glossary.
- For a forum dedicated to the InnoDB storage engine, see [MySQL Forums::InnoDB.](http://forums.mysql.com/list.php?22)
- InnoDB is published under the same GNU GPL License Version 2 (of June 1991) as MySQL. For more information on MySQL licensing, see<http://www.mysql.com/company/legal/licensing/>.

# <span id="page-3-0"></span>**14.1.1 Benefits of Using InnoDB Tables**

InnoDB tables have the following benefits:

- If the server unexpectedly exits because of a hardware or software issue, regardless of what was happening in the database at the time, you don't need to do anything special after restarting the database. InnoDB crash recovery automatically finalizes changes that were committed before the time of the crash, and undoes changes that were in process but not committed, permitting you to restart and continue from where you left off. See Section 14.19.2, "InnoDB Recovery".
- The InnoDB storage engine maintains its own buffer pool that caches table and index data in main memory as data is accessed. Frequently used data is processed directly from memory. This cache applies to many types of information and speeds up processing. On dedicated database servers, up to 80% of physical memory is often assigned to the buffer pool. See [Section 14.5.1, "Buffer Pool"](#page-9-1).
- If you split up related data into different tables, you can set up foreign keys that enforce referential integrity. See Section 13.1.18.5, "FOREIGN KEY Constraints".
- If data becomes corrupted on disk or in memory, a checksum mechanism alerts you to the bogus data before you use it. The [innodb\\_checksum\\_algorithm](#page-198-0) variable defines the checksum algorithm used by InnoDB.
- When you design a database with appropriate primary key columns for each table, operations involving those columns are automatically optimized. It is very fast to reference the primary key columns in WHERE clauses, ORDER BY clauses, GROUP BY clauses, and join operations. See [Section 14.6.2.1, "Clustered and Secondary Indexes"](#page-41-1).
- Inserts, updates, and deletes are optimized by an automatic mechanism called change buffering. InnoDB not only allows concurrent read and write access to the same table, it caches changed data to streamline disk I/O. See [Section 14.5.2, "Change Buffer".](#page-14-0)
- Performance benefits are not limited to large tables with long-running queries. When the same rows are accessed over and over from a table, the Adaptive Hash Index takes over to make these lookups even faster, as if they came out of a hash table. See [Section 14.5.3, "Adaptive Hash Index".](#page-17-0)
- You can compress tables and associated indexes. See [Section 14.9, "InnoDB Table and Page](#page-122-0) [Compression"](#page-122-0).
- You can encrypt your data. See [Section 14.14, "InnoDB Data-at-Rest Encryption"](#page-174-0).
- You can create and drop indexes and perform other DDL operations with much less impact on performance and availability. See [Section 14.13.1, "Online DDL Operations".](#page-156-0)
- Truncating a file-per-table tablespace is very fast and can free up disk space for the operating system to reuse rather than only InnoDB. See [Section 14.6.3.2, "File-Per-Table Tablespaces"](#page-51-0).

- The storage layout for table data is more efficient for BLOB and long text fields, with the DYNAMIC row format. See [Section 14.11, "InnoDB Row Formats"](#page-145-1).
- You can monitor the internal workings of the storage engine by querying INFORMATION\_SCHEMA tables. See Section 14.16, "InnoDB INFORMATION\_SCHEMA Tables".
- You can monitor the performance details of the storage engine by querying Performance Schema tables. See Section 14.17, "InnoDB Integration with MySQL Performance Schema".
- You can mix InnoDB tables with tables from other MySQL storage engines, even within the same statement. For example, you can use a join operation to combine data from InnoDB and MEMORY tables in a single query.
- InnoDB has been designed for CPU efficiency and maximum performance when processing large data volumes.
- InnoDB tables can handle large quantities of data, even on operating systems where file size is limited to 2GB.

For InnoDB-specific tuning techniques you can apply to your MySQL server and application code, see Section 8.5, "Optimizing for InnoDB Tables".

# <span id="page-4-0"></span>**14.1.2 Best Practices for InnoDB Tables**

This section describes best practices when using InnoDB tables.

- Specify a primary key for every table using the most frequently queried column or columns, or an auto-increment value if there is no obvious primary key.
- Use joins wherever data is pulled from multiple tables based on identical ID values from those tables. For fast join performance, define foreign keys on the join columns, and declare those columns with the same data type in each table. Adding foreign keys ensures that referenced columns are indexed, which can improve performance. Foreign keys also propagate deletes and updates to all affected tables, and prevent insertion of data in a child table if the corresponding IDs are not present in the parent table.
- Turn off autocommit. Committing hundreds of times a second puts a cap on performance (limited by the write speed of your storage device).
- Group sets of related DML operations into transactions by bracketing them with START TRANSACTION and COMMIT statements. While you don't want to commit too often, you also don't want to issue huge batches of INSERT, UPDATE, or DELETE statements that run for hours without committing.
- Do not use LOCK TABLES statements. InnoDB can handle multiple sessions all reading and writing to the same table at once without sacrificing reliability or high performance. To get exclusive write access to a set of rows, use the [SELECT ... FOR UPDATE](#page-76-0) syntax to lock just the rows you intend to update.
- Enable the innodb\_file\_per\_table variable or use general tablespaces to put the data and indexes for tables into separate files instead of the system tablespace. The innodb\_file\_per\_table variable is enabled by default.
- Evaluate whether your data and access patterns benefit from the InnoDB table or page compression features. You can compress InnoDB tables without sacrificing read/write capability.
- Run the server with the --sql\_mode=NO\_ENGINE\_SUBSTITUTION option to prevent tables from being created with storage engines that you do not want to use.

# <span id="page-4-1"></span>**14.1.3 Verifying that InnoDB is the Default Storage Engine**

Issue the SHOW ENGINES statement to view the available MySQL storage engines. Look for DEFAULT in the SUPPORT column.

mysql> SHOW ENGINES;

Alternatively, query the Information Schema ENGINES table.

mysql> SELECT \* FROM INFORMATION\_SCHEMA.ENGINES;

# <span id="page-5-0"></span>**14.1.4 Testing and Benchmarking with InnoDB**

If InnoDB is not the default storage engine, you can determine if your database server and applications work correctly with InnoDB by restarting the server with --default-storage-engine=InnoDB on the command line or with default-storage-engine=innodb defined in the [mysqld] section of the MySQL server option file.

Since changing the default storage engine only affects newly created tables, run your application installation and setup steps to confirm that everything installs properly, then exercise the application features to make sure the data loading, editing, and querying features work. If a table relies on a feature that is specific to another storage engine, you receive an error. In this case, add the ENGINE=other\_engine\_name clause to the CREATE TABLE statement to avoid the error.

If you did not make a deliberate decision about the storage engine, and you want to preview how certain tables work when created using InnoDB, issue the command ALTER TABLE table\_name ENGINE=InnoDB; for each table. Alternatively, to run test queries and other statements without disturbing the original table, make a copy:

```
CREATE TABLE ... ENGINE=InnoDB AS SELECT * FROM other_engine_table;
```

To assess performance with a full application under a realistic workload, install the latest MySQL server and run benchmarks.

Test the full application lifecycle, from installation, through heavy usage, and server restart. Kill the server process while the database is busy to simulate a power failure, and verify that the data is recovered successfully when you restart the server.

Test any replication configurations, especially if you use different MySQL versions and options on the source server and replicas.

# <span id="page-5-1"></span>**14.1.5 Turning Off InnoDB**

Oracle recommends InnoDB as the preferred storage engine for typical database applications, from single-user wikis and blogs running on a local system, to high-end applications pushing the limits of performance. In MySQL 5.7, InnoDB is the default storage engine for new tables.

![](_page_5_Picture_14.jpeg)

#### **Important**

InnoDB cannot be disabled. The [--skip-innodb](#page-184-0) option is deprecated and has no effect, and its use results in a warning. Expect it to be removed in a future MySQL release. This also applies to its synonyms (--innodb=OFF, - disable-innodb, and so forth).

# <span id="page-5-2"></span>**14.2 InnoDB and the ACID Model**

The ACID model is a set of database design principles that emphasize aspects of reliability that are important for business data and mission-critical applications. MySQL includes components such as the InnoDB storage engine that adhere closely to the ACID model so that data is not corrupted and results are not distorted by exceptional conditions such as software crashes and hardware malfunctions. When you rely on ACID-compliant features, you do not need to reinvent the wheel of consistency checking and crash recovery mechanisms. In cases where you have additional software safeguards, ultrareliable hardware, or an application that can tolerate a small amount of data loss or inconsistency, you can adjust MySQL settings to trade some of the ACID reliability for greater performance or throughput.

The following sections discuss how MySQL features, in particular the InnoDB storage engine, interact with the categories of the ACID model:

- **A**: atomicity.
- **C**: consistency.
- **I:**: isolation.
- **D**: durability.

# **Atomicity**

The **atomicity** aspect of the ACID model mainly involves InnoDB transactions. Related MySQL features include:

- The autocommit setting.
- The COMMIT statement.
- The ROLLBACK statement.

# **Consistency**

The **consistency** aspect of the ACID model mainly involves internal InnoDB processing to protect data from crashes. Related MySQL features include:

- The InnoDB doublewrite buffer. See [Section 14.6.5, "Doublewrite Buffer".](#page-63-1)
- InnoDB crash recovery. See InnoDB Crash Recovery.

# **Isolation**

The **isolation** aspect of the ACID model mainly involves InnoDB transactions, in particular the isolation level that applies to each transaction. Related MySQL features include:

- The autocommit setting.
- Transaction isolation levels and the SET TRANSACTION statement. See [Section 14.7.2.1,](#page-70-1) ["Transaction Isolation Levels".](#page-70-1)
- The low-level details of InnoDB locking. Details can be viewed in the INFORMATION\_SCHEMA tables. See Section 14.16.2, "InnoDB INFORMATION\_SCHEMA Transaction and Locking Information".

# **Durability**

The **durability** aspect of the ACID model involves MySQL software features interacting with your particular hardware configuration. Because of the many possibilities depending on the capabilities of your CPU, network, and storage devices, this aspect is the most complicated to provide concrete guidelines for. (And those guidelines might take the form of "buy new hardware".) Related MySQL features include:

- The InnoDB doublewrite buffer. See [Section 14.6.5, "Doublewrite Buffer".](#page-63-1)
- The innodb\_flush\_log\_at\_trx\_commit variable.
- The sync\_binlog variable.
- The innodb\_file\_per\_table variable.
- The write buffer in a storage device, such as a disk drive, SSD, or RAID array.
- A battery-backed cache in a storage device.
- The operating system used to run MySQL, in particular its support for the fsync() system call.

- An uninterruptible power supply (UPS) protecting the electrical power to all computer servers and storage devices that run MySQL servers and store MySQL data.
- Your backup strategy, such as frequency and types of backups, and backup retention periods.
- For distributed or hosted data applications, the particular characteristics of the data centers where the hardware for the MySQL servers is located, and network connections between the data centers.

# <span id="page-7-0"></span>**14.3 InnoDB Multi-Versioning**

InnoDB is a multi-version storage engine. It keeps information about old versions of changed rows to support transactional features such as concurrency and rollback. This information is stored in the system tablespace or undo tablespaces in a data structure called a rollback segment. See [Section 14.6.3.4, "Undo Tablespaces".](#page-58-0) InnoDB uses the information in the rollback segment to perform the undo operations needed in a transaction rollback. It also uses the information to build earlier versions of a row for a consistent read. See [Section 14.7.2.3, "Consistent Nonlocking Reads".](#page-74-0)

Internally, InnoDB adds three fields to each row stored in the database:

- A 6-byte DB\_TRX\_ID field indicates the transaction identifier for the last transaction that inserted or updated the row. Also, a deletion is treated internally as an update where a special bit in the row is set to mark it as deleted.
- A 7-byte DB\_ROLL\_PTR field called the roll pointer. The roll pointer points to an undo log record written to the rollback segment. If the row was updated, the undo log record contains the information necessary to rebuild the content of the row before it was updated.
- A 6-byte DB\_ROW\_ID field contains a row ID that increases monotonically as new rows are inserted. If InnoDB generates a clustered index automatically, the index contains row ID values. Otherwise, the DB\_ROW\_ID column does not appear in any index.

Undo logs in the rollback segment are divided into insert and update undo logs. Insert undo logs are needed only in transaction rollback and can be discarded as soon as the transaction commits. Update undo logs are used also in consistent reads, but they can be discarded only after there is no transaction present for which InnoDB has assigned a snapshot that in a consistent read could require the information in the update undo log to build an earlier version of a database row. For additional information about undo logs, see [Section 14.6.7, "Undo Logs"](#page-64-0).

It is recommend that you commit transactions regularly, including transactions that issue only consistent reads. Otherwise, InnoDB cannot discard data from the update undo logs, and the rollback segment may grow too big, filling up the tablespace in which it resides. For information about managing undo tablespaces, see [Section 14.6.3.4, "Undo Tablespaces".](#page-58-0)

The physical size of an undo log record in the rollback segment is typically smaller than the corresponding inserted or updated row. You can use this information to calculate the space needed for your rollback segment.

In the InnoDB multi-versioning scheme, a row is not physically removed from the database immediately when you delete it with an SQL statement. InnoDB only physically removes the corresponding row and its index records when it discards the update undo log record written for the deletion. This removal operation is called a purge, and it is quite fast, usually taking the same order of time as the SQL statement that did the deletion.

If you insert and delete rows in smallish batches at about the same rate in the table, the purge thread can start to lag behind and the table can grow bigger and bigger because of all the "dead" rows, making everything disk-bound and very slow. In such cases, throttle new row operations, and allocate more resources to the purge thread by tuning the innodb\_max\_purge\_lag system variable. For more information, see [Section 14.8.10, "Purge Configuration"](#page-108-0).

# **Multi-Versioning and Secondary Indexes**

InnoDB multiversion concurrency control (MVCC) treats secondary indexes differently than clustered indexes. Records in a clustered index are updated in-place, and their hidden system columns point undo log entries from which earlier versions of records can be reconstructed. Unlike clustered index records, secondary index records do not contain hidden system columns nor are they updated in-place.

When a secondary index column is updated, old secondary index records are delete-marked, new records are inserted, and delete-marked records are eventually purged. When a secondary index record is delete-marked or the secondary index page is updated by a newer transaction, InnoDB looks up the database record in the clustered index. In the clustered index, the record's DB\_TRX\_ID is checked, and the correct version of the record is retrieved from the undo log if the record was modified after the reading transaction was initiated.

If a secondary index record is marked for deletion or the secondary index page is updated by a newer transaction, the covering index technique is not used. Instead of returning values from the index structure, InnoDB looks up the record in the clustered index.

However, if the index condition pushdown (ICP) optimization is enabled, and parts of the WHERE condition can be evaluated using only fields from the index, the MySQL server still pushes this part of the WHERE condition down to the storage engine where it is evaluated using the index. If no matching records are found, the clustered index lookup is avoided. If matching records are found, even among delete-marked records, InnoDB looks up the record in the clustered index.

# <span id="page-8-0"></span>**14.4 InnoDB Architecture**

The following diagram shows in-memory and on-disk structures that comprise the InnoDB storage engine architecture. For information about each structure, see [Section 14.5, "InnoDB In-Memory](#page-9-0) [Structures",](#page-9-0) and [Section 14.6, "InnoDB On-Disk Structures"](#page-18-1).

![](_page_9_Picture_1.jpeg)

**Figure 14.1 InnoDB Architecture**

# <span id="page-9-0"></span>**14.5 InnoDB In-Memory Structures**

This section describes InnoDB in-memory structures and related topics.

# <span id="page-9-1"></span>**14.5.1 Buffer Pool**

The buffer pool is an area in main memory where InnoDB caches table and index data as it is accessed. The buffer pool permits frequently used data to be accessed directly from memory, which speeds up processing. On dedicated servers, up to 80% of physical memory is often assigned to the buffer pool.

For efficiency of high-volume read operations, the buffer pool is divided into pages that can potentially hold multiple rows. For efficiency of cache management, the buffer pool is implemented as a linked list of pages; data that is rarely used is aged out of the cache using a variation of the least recently used (LRU) algorithm.

Knowing how to take advantage of the buffer pool to keep frequently accessed data in memory is an important aspect of MySQL tuning.

## **Buffer Pool LRU Algorithm**

The buffer pool is managed as a list using a variation of the LRU algorithm. When room is needed to add a new page to the buffer pool, the least recently used page is evicted and a new page is added to the middle of the list. This midpoint insertion strategy treats the list as two sublists:

• At the head, a sublist of new ("young") pages that were accessed recently

• At the tail, a sublist of old pages that were accessed less recently

**Figure 14.2 Buffer Pool List**

![](_page_10_Picture_3.jpeg)

The algorithm keeps frequently used pages in the new sublist. The old sublist contains less frequently used pages; these pages are candidates for eviction.

By default, the algorithm operates as follows:

- 3/8 of the buffer pool is devoted to the old sublist.
- The midpoint of the list is the boundary where the tail of the new sublist meets the head of the old sublist.
- When InnoDB reads a page into the buffer pool, it initially inserts it at the midpoint (the head of the old sublist). A page can be read because it is required for a user-initiated operation such as an SQL query, or as part of a read-ahead operation performed automatically by InnoDB.
- Accessing a page in the old sublist makes it "young", moving it to the head of the new sublist. If the page was read because it was required by a user-initiated operation, the first access occurs immediately and the page is made young. If the page was read due to a read-ahead operation, the first access does not occur immediately and might not occur at all before the page is evicted.
- As the database operates, pages in the buffer pool that are not accessed "age" by moving toward the tail of the list. Pages in both the new and old sublists age as other pages are made new. Pages in the old sublist also age as pages are inserted at the midpoint. Eventually, a page that remains unused reaches the tail of the old sublist and is evicted.

By default, pages read by queries are immediately moved into the new sublist, meaning they stay in the buffer pool longer. A table scan, performed for a mysqldump operation or a SELECT statement

with no WHERE clause, for example, can bring a large amount of data into the buffer pool and evict an equivalent amount of older data, even if the new data is never used again. Similarly, pages that are loaded by the read-ahead background thread and accessed only once are moved to the head of the new list. These situations can push frequently used pages to the old sublist where they become subject to eviction. For information about optimizing this behavior, see [Section 14.8.3.3, "Making the](#page-96-0) [Buffer Pool Scan Resistant",](#page-96-0) and [Section 14.8.3.4, "Configuring InnoDB Buffer Pool Prefetching \(Read-](#page-97-0)[Ahead\)".](#page-97-0)

InnoDB Standard Monitor output contains several fields in the BUFFER POOL AND MEMORY section regarding operation of the buffer pool LRU algorithm. For details, see [Monitoring the Buffer Pool Using](#page-11-0) [the InnoDB Standard Monitor.](#page-11-0)

# **Buffer Pool Configuration**

You can configure the various aspects of the buffer pool to improve performance.

- Ideally, you set the size of the buffer pool to as large a value as practical, leaving enough memory for other processes on the server to run without excessive paging. The larger the buffer pool, the more InnoDB acts like an in-memory database, reading data from disk once and then accessing the data from memory during subsequent reads. See [Section 14.8.3.1, "Configuring InnoDB Buffer Pool Size"](#page-91-1).
- On 64-bit systems with sufficient memory, you can split the buffer pool into multiple parts to minimize contention for memory structures among concurrent operations. For details, see [Section 14.8.3.2,](#page-96-1) ["Configuring Multiple Buffer Pool Instances".](#page-96-1)
- You can keep frequently accessed data in memory regardless of sudden spikes of activity from operations that would bring large amounts of infrequently accessed data into the buffer pool. For details, see [Section 14.8.3.3, "Making the Buffer Pool Scan Resistant"](#page-96-0).
- You can control how and when to perform read-ahead requests to prefetch pages into the buffer pool asynchronously in anticipation that the pages are needed soon. For details, see [Section 14.8.3.4,](#page-97-0) ["Configuring InnoDB Buffer Pool Prefetching \(Read-Ahead\)"](#page-97-0).
- You can control when background flushing occurs and whether or not the rate of flushing is dynamically adjusted based on workload. For details, see [Section 14.8.3.5, "Configuring Buffer Pool](#page-98-0) [Flushing"](#page-98-0).
- You can configure how InnoDB preserves the current buffer pool state to avoid a lengthy warmup period after a server restart. For details, see [Section 14.8.3.6, "Saving and Restoring the Buffer Pool](#page-100-0) [State".](#page-100-0)

## <span id="page-11-0"></span>**Monitoring the Buffer Pool Using the InnoDB Standard Monitor**

InnoDB Standard Monitor output, which can be accessed using SHOW ENGINE INNODB STATUS, provides metrics regarding operation of the buffer pool. Buffer pool metrics are located in the BUFFER POOL AND MEMORY section of InnoDB Standard Monitor output:

```
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 2198863872
Dictionary memory allocated 776332
Buffer pool size 131072
Free buffers 124908
Database pages 5720
Old database pages 2071
Modified db pages 910
Pending reads 0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 4, not young 0
0.10 youngs/s, 0.00 non-youngs/s
Pages read 197, created 5523, written 5060
0.00 reads/s, 190.89 creates/s, 244.94 writes/s
Buffer pool hit rate 1000 / 1000, young-making rate 0 / 1000 not
```

```
0 / 1000
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read
ahead 0.00/s
LRU len: 5720, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
```

The following table describes buffer pool metrics reported by the InnoDB Standard Monitor.

Per second averages provided in InnoDB Standard Monitor output are based on the elapsed time since InnoDB Standard Monitor output was last printed.

**Table 14.2 InnoDB Buffer Pool Metrics**

| The total memory allocated for the buffer pool in                                                                                                                                             |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bytes.                                                                                                                                                                                        |
| The total memory allocated for the InnoDB data<br>dictionary in bytes.                                                                                                                        |
| The total size in pages allocated to the buffer pool.                                                                                                                                         |
| The total size in pages of the buffer pool free list.                                                                                                                                         |
| The total size in pages of the buffer pool LRU list.                                                                                                                                          |
| The total size in pages of the buffer pool old LRU<br>sublist.                                                                                                                                |
| The current number of pages modified in the<br>buffer pool.                                                                                                                                   |
| The number of buffer pool pages waiting to be<br>read into the buffer pool.                                                                                                                   |
| The number of old dirty pages within the buffer<br>pool to be written from the bottom of the LRU list.                                                                                        |
| The number of buffer pool pages to be flushed<br>during checkpointing.                                                                                                                        |
| The number of pending independent page writes<br>within the buffer pool.                                                                                                                      |
| The total number of pages made young in the<br>buffer pool LRU list (moved to the head of sublist<br>of "new" pages).                                                                         |
| The total number of pages not made young in the<br>buffer pool LRU list (pages that have remained in<br>the "old" sublist without being made young).                                          |
| The per second average of accesses to old pages<br>in the buffer pool LRU list that have resulted in<br>making pages young. See the notes that follow<br>this table for more information.     |
| The per second average of accesses to old pages<br>in the buffer pool LRU list that have resulted in not<br>making pages young. See the notes that follow<br>this table for more information. |
| The total number of pages read from the buffer<br>pool.                                                                                                                                       |
| The total number of pages created within the<br>buffer pool.                                                                                                                                  |
| The total number of pages written from the buffer<br>pool.                                                                                                                                    |
|                                                                                                                                                                                               |

| Name                         | Description                                                                                                                                           |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| reads/s                      | The per second average number of buffer pool<br>page reads per second.                                                                                |
| creates/s                    | The average number of buffer pool pages created<br>per second.                                                                                        |
| writes/s                     | The average number of buffer pool page writes<br>per second.                                                                                          |
| Buffer pool hit rate         | The buffer pool page hit rate for pages read from<br>the buffer pool vs from disk storage.                                                            |
| young-making rate            | The average hit rate at which page accesses have<br>resulted in making pages young. See the notes<br>that follow this table for more information.     |
| not (young-making rate)      | The average hit rate at which page accesses<br>have not resulted in making pages young. See the<br>notes that follow this table for more information. |
| Pages read ahead             | The per second average of read ahead<br>operations.                                                                                                   |
| Pages evicted without access | The per second average of the pages evicted<br>without being accessed from the buffer pool.                                                           |
| Random read ahead            | The per second average of random read ahead<br>operations.                                                                                            |
| LRU len                      | The total size in pages of the buffer pool LRU list.                                                                                                  |
| unzip_LRU len                | The length (in pages) of the buffer pool<br>unzip_LRU list.                                                                                           |
| I/O sum                      | The total number of buffer pool LRU list pages<br>accessed.                                                                                           |
| I/O cur                      | The total number of buffer pool LRU list pages<br>accessed in the current interval.                                                                   |
| I/O unzip sum                | The total number of buffer pool unzip_LRU list<br>pages decompressed.                                                                                 |
| I/O unzip cur                | The total number of buffer pool unzip_LRU list<br>pages decompressed in the current interval.                                                         |

#### **Notes**:

- The youngs/s metric is applicable only to old pages. It is based on the number of page accesses. There can be multiple accesses for a given page, all of which are counted. If you see very low youngs/s values when there are no large scans occurring, consider reducing the delay time or increasing the percentage of the buffer pool used for the old sublist. Increasing the percentage makes the old sublist larger so that it takes longer for pages in that sublist to move to the tail, which increases the likelihood that those pages are accessed again and made young. See [Section 14.8.3.3, "Making the Buffer Pool Scan Resistant".](#page-96-0)
- The non-youngs/s metric is applicable only to old pages. It is based on the number of page accesses. There can be multiple accesses for a given page, all of which are counted. If you do not see a higher non-youngs/s value when performing large table scans (and a higher youngs/s value), increase the delay value. See [Section 14.8.3.3, "Making the Buffer Pool Scan Resistant"](#page-96-0).
- The young-making rate accounts for all buffer pool page accesses, not just accesses for pages in the old sublist. The young-making rate and not rate do not normally add up to the overall buffer pool hit rate. Page hits in the old sublist cause pages to move to the new sublist, but page hits in the new sublist cause pages to move to the head of the list only if they are a certain distance from the head.

• not (young-making rate) is the average hit rate at which page accesses have not resulted in making pages young due to the delay defined by innodb\_old\_blocks\_time not being met, or due to page hits in the new sublist that did not result in pages being moved to the head. This rate accounts for all buffer pool page accesses, not just accesses for pages in the old sublist.

Buffer pool server status variables and the INNODB\_BUFFER\_POOL\_STATS table provide many of the same buffer pool metrics found in InnoDB Standard Monitor output. For more information, see Example 14.10, "Querying the INNODB\_BUFFER\_POOL\_STATS Table".

# <span id="page-14-0"></span>**14.5.2 Change Buffer**

The change buffer is a special data structure that caches changes to secondary index pages when those pages are not in the buffer pool. The buffered changes, which may result from INSERT, UPDATE, or DELETE operations (DML), are merged later when the pages are loaded into the buffer pool by other read operations.

**Figure 14.3 Change Buffer**

![](_page_14_Picture_6.jpeg)

Unlike clustered indexes, secondary indexes are usually nonunique, and inserts into secondary indexes happen in a relatively random order. Similarly, deletes and updates may affect secondary index pages that are not adjacently located in an index tree. Merging cached changes at a later time, when affected pages are read into the buffer pool by other operations, avoids substantial random access I/O that would be required to read secondary index pages into the buffer pool from disk.

Periodically, the purge operation that runs when the system is mostly idle, or during a slow shutdown, writes the updated index pages to disk. The purge operation can write disk blocks for a series of index values more efficiently than if each value were written to disk immediately.

Change buffer merging may take several hours when there are many affected rows and numerous secondary indexes to update. During this time, disk I/O is increased, which can cause a significant slowdown for disk-bound queries. Change buffer merging may also continue to occur after a transaction is committed, and even after a server shutdown and restart (see Section 14.22.2, "Forcing InnoDB Recovery" for more information).

In memory, the change buffer occupies part of the buffer pool. On disk, the change buffer is part of the system tablespace, where index changes are buffered when the database server is shut down.

The type of data cached in the change buffer is governed by the [innodb\\_change\\_buffering](#page-197-0) variable. For more information, see [Configuring Change Buffering.](#page-15-0) You can also configure the maximum change buffer size. For more information, see [Configuring the Change Buffer Maximum Size](#page-16-0). Change buffering is not supported for a secondary index if the index contains a descending index column or if the primary key includes a descending index column.

For answers to frequently asked questions about the change buffer, see Section A.16, "MySQL 5.7 FAQ: InnoDB Change Buffer".

## <span id="page-15-0"></span>**Configuring Change Buffering**

When INSERT, UPDATE, and DELETE operations are performed on a table, the values of indexed columns (particularly the values of secondary keys) are often in an unsorted order, requiring substantial I/O to bring secondary indexes up to date. The change buffer caches changes to secondary index entries when the relevant page is not in the buffer pool, thus avoiding expensive I/O operations by not immediately reading in the page from disk. The buffered changes are merged when the page is loaded into the buffer pool, and the updated page is later flushed to disk. The InnoDB main thread merges buffered changes when the server is nearly idle, and during a slow shutdown.

Because it can result in fewer disk reads and writes, change buffering is most valuable for workloads that are I/O-bound; for example, applications with a high volume of DML operations such as bulk inserts benefit from change buffering.

However, the change buffer occupies a part of the buffer pool, reducing the memory available to cache data pages. If the working set almost fits in the buffer pool, or if your tables have relatively few secondary indexes, it may be useful to disable change buffering. If the working data set fits entirely within the buffer pool, change buffering does not impose extra overhead, because it only applies to pages that are not in the buffer pool.

The [innodb\\_change\\_buffering](#page-197-0) variable controls the extent to which InnoDB performs change buffering. You can enable or disable buffering for inserts, delete operations (when index records are initially marked for deletion) and purge operations (when index records are physically deleted). An update operation is a combination of an insert and a delete. The default [innodb\\_change\\_buffering](#page-197-0) value is all.

Permitted [innodb\\_change\\_buffering](#page-197-0) values include:

• **all**

The default value: buffer inserts, delete-marking operations, and purges.

• **none**

Do not buffer any operations.

• **inserts**

Buffer insert operations.

• **deletes**

Buffer delete-marking operations.

• **changes**

Buffer both inserts and delete-marking operations.

• **purges**

Buffer physical deletion operations that happen in the background.

You can set the [innodb\\_change\\_buffering](#page-197-0) variable in the MySQL option file (my.cnf or my.ini) or change it dynamically with the SET GLOBAL statement, which requires privileges sufficient to set global system variables. See Section 5.1.8.1, "System Variable Privileges". Changing the setting affects the buffering of new operations; the merging of existing buffered entries is not affected.

## <span id="page-16-0"></span>**Configuring the Change Buffer Maximum Size**

The [innodb\\_change\\_buffer\\_max\\_size](#page-197-1) variable permits configuring the maximum size of the change buffer as a percentage of the total size of the buffer pool. By default, [innodb\\_change\\_buffer\\_max\\_size](#page-197-1) is set to 25. The maximum setting is 50.

Consider increasing [innodb\\_change\\_buffer\\_max\\_size](#page-197-1) on a MySQL server with heavy insert, update, and delete activity, where change buffer merging does not keep pace with new change buffer entries, causing the change buffer to reach its maximum size limit.

Consider decreasing [innodb\\_change\\_buffer\\_max\\_size](#page-197-1) on a MySQL server with static data used for reporting, or if the change buffer consumes too much of the memory space shared with the buffer pool, causing pages to age out of the buffer pool sooner than desired.

Test different settings with a representative workload to determine an optimal configuration. The [innodb\\_change\\_buffer\\_max\\_size](#page-197-1) variable is dynamic, which permits modifying the setting without restarting the server.

# **Monitoring the Change Buffer**

The following options are available for change buffer monitoring:

• InnoDB Standard Monitor output includes change buffer status information. To view monitor data, issue the SHOW ENGINE INNODB STATUS statement.

```
mysql> SHOW ENGINE INNODB STATUS\G
```

Change buffer status information is located under the INSERT BUFFER AND ADAPTIVE HASH INDEX heading and appears similar to the following:

```
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 0, seg size 2, 0 merges
merged operations:
 insert 0, delete mark 0, delete 0
discarded operations:
 insert 0, delete mark 0, delete 0
Hash table size 4425293, used cells 32, node heap has 1 buffer(s)
13577.57 hash searches/s, 202.47 non-hash searches/s
```

For more information, see Section 14.18.3, "InnoDB Standard Monitor and Lock Monitor Output".

• The Information Schema INNODB\_METRICS table provides most of the data points found in InnoDB Standard Monitor output plus other data points. To view change buffer metrics and a description of each, issue the following query:

```
mysql> SELECT NAME, COMMENT FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME LIKE '%ibuf%'\G
```

For INNODB\_METRICS table usage information, see Section 14.16.6, "InnoDB INFORMATION\_SCHEMA Metrics Table".

• The Information Schema INNODB\_BUFFER\_PAGE table provides metadata about each page in the buffer pool, including change buffer index and change buffer bitmap pages. Change buffer pages are identified by PAGE\_TYPE. IBUF\_INDEX is the page type for change buffer index pages, and IBUF\_BITMAP is the page type for change buffer bitmap pages.

![](_page_16_Picture_17.jpeg)

#### **Warning**

Querying the INNODB\_BUFFER\_PAGE table can introduce significant performance overhead. To avoid impacting performance, reproduce the issue you want to investigate on a test instance and run your queries on the test instance.

For example, you can query the INNODB\_BUFFER\_PAGE table to determine the approximate number of IBUF\_INDEX and IBUF\_BITMAP pages as a percentage of total buffer pool pages.

```
mysql> SELECT (SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE PAGE_TYPE LIKE 'IBUF%') AS change_buffer_pages,
 (SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE) AS total_pages,
 (SELECT ((change_buffer_pages/total_pages)*100))
 AS change_buffer_page_percentage;
+---------------------+-------------+-------------------------------+
| change_buffer_pages | total_pages | change_buffer_page_percentage |
+---------------------+-------------+-------------------------------+
| 25 | 8192 | 0.3052 |
+---------------------+-------------+-------------------------------+
```

For information about other data provided by the INNODB\_BUFFER\_PAGE table, see Section 24.4.2, "The INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE Table". For related usage information, see Section 14.16.5, "InnoDB INFORMATION\_SCHEMA Buffer Pool Tables".

• Performance Schema provides change buffer mutex wait instrumentation for advanced performance monitoring. To view change buffer instrumentation, issue the following query:

```
mysql> SELECT * FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%wait/synch/mutex/innodb/ibuf%';
+-------------------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------------------------------------------------+---------+-------+
| wait/synch/mutex/innodb/ibuf_bitmap_mutex | YES | YES |
| wait/synch/mutex/innodb/ibuf_mutex | YES | YES |
| wait/synch/mutex/innodb/ibuf_pessimistic_insert_mutex | YES | YES |
+-------------------------------------------------------+---------+-------+
```

For information about monitoring InnoDB mutex waits, see Section 14.17.2, "Monitoring InnoDB Mutex Waits Using Performance Schema".

# <span id="page-17-0"></span>**14.5.3 Adaptive Hash Index**

The adaptive hash index enables InnoDB to perform more like an in-memory database on systems with appropriate combinations of workload and sufficient memory for the buffer pool without sacrificing transactional features or reliability. The adaptive hash index is enabled by the [innodb\\_adaptive\\_hash\\_index](#page-188-0) variable, or turned off at server startup by --skip-innodbadaptive-hash-index.

Based on the observed pattern of searches, a hash index is built using a prefix of the index key. The prefix can be any length, and it may be that only some values in the B-tree appear in the hash index. Hash indexes are built on demand for the pages of the index that are accessed often.

If a table fits almost entirely in main memory, a hash index speeds up queries by enabling direct lookup of any element, turning the index value into a sort of pointer. InnoDB has a mechanism that monitors index searches. If InnoDB notices that queries could benefit from building a hash index, it does so automatically.

With some workloads, the speedup from hash index lookups greatly outweighs the extra work to monitor index lookups and maintain the hash index structure. Access to the adaptive hash index can sometimes become a source of contention under heavy workloads, such as multiple concurrent joins. Queries with LIKE operators and % wildcards also tend not to benefit. For workloads that do not benefit from the adaptive hash index, turning it off reduces unnecessary performance overhead. Because it is difficult to predict in advance whether the adaptive hash index feature is appropriate for a particular system and workload, consider running benchmarks with it enabled and disabled.

In MySQL 5.7, the adaptive hash index feature is partitioned. Each index is bound to a specific partition, and each partition is protected by a separate latch. Partitioning is controlled by the [innodb\\_adaptive\\_hash\\_index\\_parts](#page-188-1) variable. In earlier releases, the adaptive hash index feature was protected by a single latch which could become a point of contention under heavy workloads. The [innodb\\_adaptive\\_hash\\_index\\_parts](#page-188-1) variable is set to 8 by default. The maximum setting is 512.

You can monitor adaptive hash index use and contention in the SEMAPHORES section of SHOW ENGINE INNODB STATUS output. If there are numerous threads waiting on rw-latches created in btr0sea.c, consider increasing the number of adaptive hash index partitions or disabling the adaptive hash index.

For information about the performance characteristics of hash indexes, see Section 8.3.8, "Comparison of B-Tree and Hash Indexes".

# <span id="page-18-0"></span>**14.5.4 Log Buffer**

The log buffer is the memory area that holds data to be written to the log files on disk. Log buffer size is defined by the innodb\_log\_buffer\_size variable. The default size is 16MB. The contents of the log buffer are periodically flushed to disk. A large log buffer enables large transactions to run without the need to write redo log data to disk before the transactions commit. Thus, if you have transactions that update, insert, or delete many rows, increasing the size of the log buffer saves disk I/O.

The innodb\_flush\_log\_at\_trx\_commit variable controls how the contents of the log buffer are written and flushed to disk. The innodb\_flush\_log\_at\_timeout variable controls log flushing frequency.

For related information, see [Memory Configuration](#page-89-0), and Section 8.5.4, "Optimizing InnoDB Redo Logging".

# <span id="page-18-1"></span>**14.6 InnoDB On-Disk Structures**

This section describes InnoDB on-disk structures and related topics.

# <span id="page-18-2"></span>**14.6.1 Tables**

This section covers topics related to InnoDB tables.